---
description: "Free email and notification channels: Email Routing inbound, Resend/Brevo outbound quotas, ntfy/Server酱/IM webhook push limits"
描述: "免费邮箱与推送通道的额度：收信转发、发信 API、手机与 IM 触达"
name: "Free Email & Push"
名称: "免费邮箱与推送"
---

# 免费邮箱与推送

"免费发通知"其实是三条互不相干的链路，混在一起谈最容易算错额度：

- **入站收信**：给自己的域名开邮箱地址，收到后转发到已有邮箱。
- **出站发信**：程序主动发验证码、告警、日报。
- **推送触达**：不经过邮箱，直接把消息落到手机或 IM 群。

三条链路的免费额度形态完全不同：入站通常按"规则数"限制、出站按"封数/天"限制、推送按"条数/天"或"次/分钟"限制。

## 入站：给自己的域名开邮箱

Cloudflare Email Routing 是这一档的天花板：所有套餐免费，前提是域名托管在 Cloudflare DNS。可以为域名创建任意数量的自定义地址（`support@`、`billing@`、甚至 catch-all），邮件转发到你指定的邮箱，**Cloudflare 不存储也不访问邮件内容**。

它的硬限制写在文档里：每个域最多 200 条路由规则、每个账号最多 200 个已验证目标地址、单封入站邮件上限 25 MiB；一个规则只能映射到一个目标或一个 Worker，要一对多就得用 Worker 里多次调用转发。

这套组合的实际价值是：**注册各种服务时不再暴露主邮箱**，垃圾邮件在转发层就被拦掉，而且完全不花钱。

## 出站：发信 API 的免费额度

| 平台 | 免费额度 | 关键细节 |
|---|---|---|
| Resend | 3,000 封/月，**100 封/天** | 收信也计入配额；3 个域名、3 个收件箱；数据保留 30 天 |
| Brevo | 300 封/天（9,000/月），永久免费 | 超限的事务邮件最多 1,000 封进重试队列，再多直接不投递 |
| Cloudflare Email Sending | Workers Free 档可发，但**只能发到已验证目标地址** | 要发给任意收件人需 Workers Paid + 已接入发送域名 |

Resend 的日限是 UTC 自然日（00:00–24:00），不是滚动 24 小时；一封邮件多个收件人（To/CC/BCC）按多人分别计数，这一点最容易把额度算爆。Brevo 的 300 封/天同样不累积，当天没用完不结转。

## 推送：手机与 IM 的免费通道

| 通道 | 免费额度 | 特点 |
|---|---|---|
| ntfy 公共实例 | **250 条/天**（按访客 IP 计），留存 12 小时 | 无需账号、一个 HTTP PUT 就发；topic 名就是密码 |
| ntfy 自建 | 不限条数 | 单个 Go 二进制，官方 apt/Docker 源，数据自己拿 |
| Server酱 Turbo | **5 条/天**，每分钟 50 条 | 推微信/企微/钉钉/飞书/Bark/PushDeer，一个 SendKey 打通多落点 |
| 飞书自定义机器人 | 免费，**100 次/分钟、5 次/秒**，请求体 ≤20 KB | 群 webhook 即插即用，不需要管理员审核 |
| Bark | iOS 客户端免费，服务端开源自建 | 官方服务器可用；自建则完全无配额 |
| 企业微信 / 钉钉群机器人 | 免费 webhook | 频率限制按各自文档，社区常见口径 20 条/分钟，接入前核对 |

ntfy 的公共实例按 IP 计额，同一出口 IP 下的所有设备共享那 250 条；同一 `/64` IPv6 网段也会被当作一个访客，所以家宽或云主机上跑多个服务时很容易提前打满。要长期稳定，自建是正解。

## 一套零成本组合

个人 Agent 项目可以这样拼：

1. **入站**：域名挂 Cloudflare DNS，Email Routing 开 catch-all，所有回信进主邮箱。
2. **出站**：Resend 免费档发验证码与关键告警（100 封/天对个人足够），量大再切 Brevo。
3. **推送**：日常状态走 ntfy 公共实例，重要的走飞书群机器人或 Bark；要隐私就自建 ntfy。

整条链路只有域名可能有成本，邮件与推送都是 0。

## 四个坑

1. **发信域名必须验三件套**：SPF、DKIM、DMARC。不配就进垃圾箱，配错会直接被拒；Resend/Brevo 都要求域名验证后才允许发。
2. **共享 IP 的信誉**：免费档用的是共享发送池，同一池里有人滥发就会拖累你的送达率；关键邮件不要只用免费档。
3. **双重限额**：出站常同时有"每天"和"每月"两个上限，取先撞到的那个；Resend 是 100/天 + 3,000/月，Brevo 是 300/天。
4. **推送通道的保密性**：公共 ntfy 没有端到端加密，topic 名可被猜到就人人可读；Server酱 的免费额度每天只有 5 条，循环里逐条发必然打满，先聚合再发。

## 一句话主线

免费通知的成本结构是**"入站几乎无限、出站按天掐、推送按条掐"**：收信可以敞开用，发信要按"能发多少封关键邮件"规划，推送要按"一天真正需要叫醒人几次"规划，其余的都该合并成摘要。

## 参考资料

- Cloudflare Email Routing 概览（所有套餐免费、不存储邮件、需 Cloudflare DNS）：https://developers.cloudflare.com/email-routing/
- Cloudflare Email Service 限额（200 规则/域、200 目标/账号、25 MiB、Free 档仅发已验证地址）：https://developers.cloudflare.com/email-service/platform/limits/
- Resend 定价（免费 3,000 封/月、100 封/天）：https://resend.com/pricing
- Resend 配额说明（收信也计数、UTC 自然日、多收件人分别计数）：https://resend.com/docs/knowledge-base/account-quotas-and-limits
- Brevo 免费计划限制（300 封/天、超限重试队列 1,000 封）：https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan
- Server酱 额度与频率（免费 5 条/天、50 条/分钟、会员 1,000 条/天）：https://sct.ftqq.com/docs/getting-started/faq/
- Server酱 通道对比（微信/企微/群机器人/Bark/PushDeer）：https://sct.ftqq.com/docs/getting-started/channels/
- 飞书自定义机器人频控（100 次/分钟、5 次/秒、请求体 20 KB）：https://open.feishu.cn/document/server-docs/api-call-guide/frequency-control?lang=zh-CN
- ntfy 官网（开源、公共实例与自建、Pro 档位）：https://ntfy.sh/
- ntfy 公共实例限额实测（250 条/天/访客、IPv6 /64 共享计额）：https://deallocatedobjects.com/posts/self-hosted-ntfy-and-the-shared-ipv6-quota-behind-my-429s
