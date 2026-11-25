---
description: "Exposing a cloud agent publicly: trusted TLS, PWA constraints, ICP filing and access alternatives"
描述: "云端 Agent 公网入口：受信任 HTTPS、PWA 限制、ICP 备案与接入替代方案"
name: "Public Entry and Hosting"
名称: "公网入口与托管"
---

# 公网入口与托管

把云端 Agent 暴露到公网，看起来只是"开个端口、绑个域名"，实际要同时过三道**互相独立**的门：

- **入口层**：连接是否受浏览器信任，证书、域名、反向代理是否配好；
- **客户端层**：用户能不能把 Web 页面装成 App，Service Worker 能不能注册；
- **主机层**：服务器所在地是否允许这个网站在公网提供服务，需不需要备案。

三道门任意一道缺失，手机端表现通常是"能打开但不像 App"或"根本打不开"，而不是一个明确的报错。

## 三道门不能互相替代

| 门槛 | 解决什么 | 不能替代什么 |
|---|---|---|
| 受信任 HTTPS | 浏览器不报证书错误，Service Worker 可注册 | 不能替代主机备案，也不能替代应用鉴权 |
| PWA 安装 | 手机主屏图标、独立窗口、离线壳 | 不能替代 HTTPS，不能替代后端鉴权 |
| ICP 备案 | 中国内地服务器合法提供 Web 服务 | 不能替代 TLS，也不能让 HTTP 变成安全上下文 |

> 判断：先把这三件事拆开评估，再选方案；把它们合成一句"买个域名就能手机访问"，最后一定会在证书、安装或备案其中一处卡住。

## 入口层：反向代理与 TLS

公网入口通常由 Caddy、Nginx 或云厂商的负载均衡承担，Agent 进程自己不直接监听公网。入口层负责四件事：

- **TLS 终止**：持有证书，处理握手，把明文请求转发给本机应用；
- **HTTP 到 HTTPS 跳转**：80 端口只做跳转，业务只走 443；
- **WebSocket 升级**：终端的双向连接要能穿过代理，不能只转发普通 HTTP；
- **静态资源与反向代理**：同一个域名下区分页面、API 与升级请求。

Caddy 是 Go 编写的 Web 服务器与反向代理，不是项目的 npm 依赖。它的便利在于自动申请和续期 Let's Encrypt 证书、自动配置 80 到 443 跳转、默认可处理 WebSocket 升级。Nginx 加 certbot 也能做同样的事，只是证书续期与配置拆分要自己维护。

自动 HTTPS 需要一个**能被公共 CA 验证的域名**。裸 IP 通常拿不到浏览器信任的证书；自签证书能加密，但默认不被信任。Caddy 的自动 HTTPS 不能绕过这个前提。

入口层不是鉴权层。Caddy 的 basic auth 可以再加一道门，但它不能替代应用层的 token、cookie、Origin 校验与权限检查。公网扫描会主动发现开放端口，单用户服务也不能假设"没人知道地址"。

## 域名、证书与 PWA 安装

PWA 的安装条件不是"有个网页"这么宽。浏览器要求：

- 通过 **HTTPS** 提供，或者从 `localhost` / `127.0.0.1` 这种本地开发地址提供；
- 有 **Web App Manifest**，包含名称、图标、`start_url`、`display` 等字段；
- 注册 **Service Worker**，并且它能提供基本的离线体验。

公开 HTTP 页面通常还能"添加到主屏幕"，但那多数只是快捷方式：没有 Service Worker，没有离线壳，也没有真正的安装提示。Android Chrome 的完整 PWA 安装基本要求 HTTPS；iOS Safari 的"添加到主屏幕"入口更宽松，但同样不等于完整的 PWA 能力。

> 判断：如果产品目标只是"手机浏览器能聊天"，HTTP 也能用；一旦目标写成"装到主屏、像 App 一样打开、断网有壳"，就必须按 PWA 的 HTTPS 条件设计，不能事后补。

域名通常按年付费，价格随后缀与注册商变化。证书可以免费，Let's Encrypt、ZeroSSL、Cloudflare 都能签发受信任的 DV 证书；付费 DV/OV/EV 不是 PWA 的必需项。真正可能产生持续成本的是域名，而不是证书。

## Service Worker 的 HTTPS 判定

Service Worker 只在**安全上下文**中可用。公网 HTTP 不是安全上下文，注册会直接失败；`http://localhost` 与 `127.0.0.1` 被特殊视为可信，所以本地开发可以不用证书。

HTTPS 还要看证书是否被浏览器信任：

| 场景 | Service Worker |
|---|---|
| 公网 HTTP | 一定拒绝 |
| `http://localhost` / `127.0.0.1` | 允许 |
| HTTPS + 受信任证书 | 允许 |
| HTTPS + 自签证书，只在警告页点"继续访问" | Chrome / Chromium 拒绝；Firefox 取决于证书例外；Safari 通常要求系统级信任 |
| HTTPS + 自签证书，已装进系统或浏览器信任库 | 允许 |
| Chrome 开发参数忽略证书错误 | 仅测试环境可绕过 |

关键在脚本抓取：普通页面可以点"继续访问"，但浏览器去抓 `sw.js` 时，证书错误是致命的。Chrome 不会给 Service Worker 脚本再来一次"继续访问"的机会，常见报错是：

```text
SecurityError: Failed to register a ServiceWorker:
An SSL certificate error occurred when fetching the script.
```

所以"自签 HTTPS 也能用 PWA"只在证书被显式信任时成立。把自签 CA 装进系统信任库可以做到，但让每台手机都装一次 CA，不适合作为公开服务的方案。

> 判断：面向自己的手机做实验，可以装自签 CA；面向任何其他设备，直接用公共 CA 签发的证书，不要把"点过继续访问"当成受信任。

## 中国内地服务器与 ICP 备案

域名解析到**中国内地服务器**，并且对外提供 Web 服务，需要先完成 ICP 备案；备案成功后才能正常开通域名访问。域名解析到中国香港或其他境外服务器，通常不需要工信部 ICP 备案，但仍有属地内容合规与公安备案等要求，具体以服务商与属地管理部门为准。

备案对域名有一组硬条件：

- 域名在有效期内；
- 域名完成实名认证，且实名主体与备案主体一致；
- 域名后缀是工信部批复的顶级域名；
- 域名在工信部批准的注册服务机构注册；境外注册商注册的域名不能直接备案，要先转入境内有资质服务商；
- 备案信息与实际网站内容、主体性质相符。

"国内服务器必须配国内域名"更准确的说法是：**必须配一个可备案的域名**。`.com`、`.cn` 等工信部批复后缀都可以，不要求使用 `.cn`；关键是注册商资质、实名主体与备案流程，而不是后缀本身。

> 判断：免费二级域名通常不能用于备案。备案核验要求域名由备案主体依法注册所有，而免费子域名的所有权、实名主体与注册商资质通常都不满足；即使能解析，也过不了备案核验。

备案不是 PWA 的技术要求，而是中国内地主机提供 Web 服务的合规要求。它不会让 HTTP 变成安全上下文，也不会替代证书；反过来，配了 HTTPS 也不等于完成备案。

## 公网入口方案对比

| 方案 | 域名 | ICP 备案 | PWA | 适用 |
|---|---|---|---|---|
| 中国内地服务器 + 可备案域名 | 需要，按年付费 | 需要 | 可以 | 合规长期运行，愿意走备案流程 |
| 中国香港/海外服务器 + 域名 | 需要，按年付费 | 通常不需要工信备案 | 可以 | 个人项目、快速上线，接受跨境延迟 |
| Cloudflare Quick Tunnel | 不需要 | 不适用 | 可以，但地址不稳定 | 临时演示、开发预览 |
| IM 长连接机器人 | 不需要 | 不需要 | 不是 PWA | 手机聊天式交互，Agent 主动出站连 IM |
| Tailscale 私有网络 | 不需要 | 不需要 | 可以，但仅私有 | 自己设备访问，不面向公网 |
| 公网 HTTP | 可不用 | 内地服务器仍需要 | 不能完整安装 | 只做普通网页，不推荐长期 |

### Cloudflare Quick Tunnel 的真实边界

Quick Tunnel 不需要账号与域名，会生成一个 `trycloudflare.com` 随机子域名，通过 Cloudflare 边缘提供受信任 HTTPS。它适合临时把本机服务给外部看一眼。

但它有三个硬限制：地址每次启动都变、没有 uptime 保证、**不支持 SSE**。对依赖流式事件的 Agent UI，最后一条几乎是致命的；地址变化还会让已安装的 PWA 失去原 origin。它只应出现在测试与演示场景。

> 判断：Quick Tunnel 可以证明"HTTPS 和 PWA 能跑"，但不能作为长期公网入口；它改变的是入口路径，不改变主机所在地的备案义务。

### IM 长连接机器人

IM 机器人如果走**长连接模式**，由 Agent 主动出站连接 IM 平台，不需要公网 IP、域名或 ICP 备案；用户在手机 IM 里直接聊天。这条路牺牲的是自定义 UI 与富交互，换来的是零公网入口与现成的移动端推送。

如果机器人走 **webhook 模式**，平台要回调一个公网 URL，仍然需要公网入口、域名与 TLS；两种模式不能混为一谈。

### Tailscale 私有网络

Tailscale 把设备放进一个私有虚拟网络，手机装客户端后可以直接访问云主机，不需要公网端口、域名或备案。它适合"只有我自己用"的场景，不适合"任何人打开链接就能用"的公开服务。

## 鉴权与能力收窄

公网入口一旦打开，应用层必须自己兜住：

- **单用户也要登录**：一个长期 token 换签名 cookie，`HttpOnly`、`Secure`、`SameSite=Strict`；轮换 token 让旧 cookie 失效。
- **API 与 WebSocket 都要校验**：`/api/call`、`/terminal` 的 upgrade 请求不能绕过鉴权；只在页面上加登录框没有意义。
- **同源与 Origin 校验**：CORS 只允许自己的公网 origin；写操作校验 `Origin`，降低 CSRF 面。
- **登录限流**：失败次数、IP、时间窗都要限；否则单 token 会被在线爆破。
- **能力默认收窄**：公网默认关闭终端与渠道管理；工具权限默认 `ask`；文件访问限制在工作区。
- **进程只绑回环**：Agent 监听 `127.0.0.1`，公网只开 443，由入口层转发。
- **容器不留后门**：非 root、只读根、不挂 `docker.sock`、不挂宿主 home 与 SSH 凭据。

> 判断：公网入口的安全基线不是"加一个密码"，而是"入口层只做 TLS，应用层做身份，能力层做收窄"；三层各管一件事，不能互相替代。

## 常见失败模式

- 以为公网 HTTP 也能装 PWA，做到安装提示阶段才发现 Service Worker 注册失败。
- 自签 HTTPS 只在浏览器警告页点了"继续访问"，页面能开，但 `sw.js` 抓取被证书错误拦住。
- 以为免费二级域名可以备案，买完服务器才发现域名核验过不了。
- 中国内地服务器没备案就开 80/443，域名被阻断或接入被停。
- 把 Caddy 的 basic auth 当成应用鉴权，`/api/call` 仍然可以被直接调用。
- 只开了 443，却让 Agent 监听 `0.0.0.0`，绕过入口层直连端口。
- 用 Quick Tunnel 跑生产，SSE 不通、地址漂移，PWA 安装后指向旧 origin。
- IM 机器人选了 webhook 模式，却按"不需要公网入口"做部署。
- 域名或入口地址更换后，旧 PWA 仍指向旧 origin，用户打开的是失效壳。

## 一句话主线

公网访问的难点不是"把端口打开"，而是同时满足三件事：**受信任的入口、可安装的客户端、可合规的主机**；三者各自成立，手机端才会从"能打开"变成"能长期用"。

## 参考资料

- MDN《Making PWAs installable》（HTTPS、manifest、Service Worker 的安装条件）：https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
- W3C《Secure Contexts》（安全上下文的规范定义）：https://w3c.github.io/webappsec-secure-contexts/
- Chromium《Service Worker FAQ》（Service Worker 的 HTTPS 与证书错误行为）：https://www.chromium.org/blink/serviceworker/service-worker-faq/
- Cloudflare《Quick Tunnels》（临时 trycloudflare.com 地址、限制与 SSE 不支持说明）：https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
- 腾讯云《ICP 备案域名》（域名实名、注册商资质与备案核验要求）：https://cloud.tencent.cn/document/product/243/18905
- 阿里云《域名准备与检查》（工信部批复后缀、实名主体与境外注册商转入要求）：https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/prepare-and-check-the-domain-name
- 阿里云《备案流程 FAQ》（中国内地服务器备案、非内地服务器免工信备案的说明）：https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-process-faq
- Caddy《Automatic HTTPS》（自动证书与域名前提）：https://caddyserver.com/docs/automatic-https
