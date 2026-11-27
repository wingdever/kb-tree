---
description: "Configurable multi-server client: node manifests, per-node TLS and auth, and push architecture"
描述: "可配置多服务器客户端：节点清单、按节点 TLS/鉴权与推送架构"
name: "Multi-Server Client"
名称: "多服务器客户端"
---

# 多服务器客户端

通用客户端不是"设置里能填多个 URL"这么简单，而是把**服务器当作一等对象**。每个节点有身份、地址、证书策略、凭据、推送方式与能力集；用户选择当前节点，客户端按节点建立连接，节点之间不能串数据。

## 两种角色

- **普通用户**：添加节点、扫码、登录、切换、聊天；不需要知道端口、证书、备案或 Firebase。
- **节点管理员**：部署服务、处理 TLS、开放端口、完成备案、配置 FCM 或 relay、生成邀请；可以承担复杂操作。

产品分工应该收敛成一句话：**用户侧只扫一个码，管理员侧把复杂度封装成节点清单与命令行工具。**

## 节点清单

服务器管理员生成一份节点清单，App 读取后完成接入：

```json
{
  "schema": "agent-node/v1",
  "serverId": "srv-xxx",
  "name": "我的云主机",
  "baseUrl": "https://203.0.113.10:8443",
  "apiVersion": "v1",
  "tls": { "mode": "pinned", "spki": ["sha256/..."] },
  "pairing": { "code": "one-time-code", "expiresAt": "2026-11-26T12:00:00Z" },
  "push": {
    "mode": "fcm",
    "projectId": "...",
    "applicationId": "...",
    "apiKey": "...",
    "senderId": "..."
  },
  "capabilities": ["chat", "sse", "files"]
}
```

清单里**不能放长期设备 token**，只能放一次性配对 code；长期 token 在配对成功后由服务端签发，客户端存进 Keychain/Keystore。清单里也**不能放 FCM service account key**，那属于服务器侧秘密；客户端只需要 Firebase 的客户端配置。

二维码可以只放一个短链接，App 打开后拉取清单；这样清单可以更新，二维码不必随配置变化重新打印。

## 用户加入流程

1. 扫码或打开邀请链接；
2. 校验 `baseUrl` 与 TLS 指纹；
3. 调 `GET /api/meta` 确认 `serverId`、版本、能力；
4. 用一次性 code 换设备 token；
5. 保存节点，设为当前节点。

用户界面只展示：

- 节点名称与在线状态；
- 能力（有没有文件、终端、推送）；
- 最近连接时间；
- 切换与删除。

不展示 FCM 项目、证书链、端口、备案状态这些管理员概念。

## 每节点 TLS

| 模式 | 服务器 | App 行为 |
|---|---|---|
| `system` | 公共 CA 证书 | 用系统信任链验证，用户零配置 |
| `pinned` | 自签或私有 CA | 只信任清单里的 SPKI 指纹，用户不用装 CA |
| `insecure-local` | 私有网络 HTTP | 仅允许 localhost、Tailscale 等，公网禁用 |

多服务器不等于每个服务器都要自签。管理员能用公共 CA 就用公共 CA；没有域名或端口受限时，才用自签加 pin。App 不能因为一个自签节点就全局关闭证书校验，每个 profile 独立判断。

证书轮换也要按节点处理：公共 CA 续期对 App 透明；自签证书换 pin 时要提示用户确认，不能静默换信任。

## 每节点凭据与数据隔离

- **token 按节点存**：不同服务器不共享 token；删除节点时撤销本地凭据。
- **本地数据按节点隔离**：会话、消息、草稿、文件缓存都带 `profileId`，避免 A 服务器的会话出现在 B 服务器。
- **连接按节点切换**：同一时刻只保持一个活跃连接；切换时关闭旧 WS/SSE、保存草稿，再连新节点。
- **身份按 `serverId` 识别**：同一服务器的域名/IP 变化不应变成两个节点；不同服务器即使同名也要分开。
- **同一服务器多账号**：用 `serverId + accountId` 区分，避免覆盖凭据。

> 判断：多服务器最容易出的问题不是"连不上"，而是"串数据"：草稿发错节点、旧 token 被新节点复用、删除节点后缓存还在。数据隔离要在第一版做，不能等出问题再补。

## 推送：三条路线

Android-only 让方案比双端简单，但 FCM 的项目归属问题仍然存在：**registration token 属于某个 Firebase 项目，不同项目的服务器不能直接给该 token 发消息。**

| 路线 | 管理员配置 | 用户配置 | App 复杂度 |
|---|---|---|---|
| 每服务器自带 FCM 项目 | 建 Firebase 项目、加 App 包名与签名指纹、保管 service account | 扫码 | 高：多 FirebaseApp、每节点 token |
| 中央 relay | 配 relay 地址与节点密钥 | 扫码 | 低：App 只依赖一个 FCM 项目 |
| 不做原生推送 | 无 | 扫码 | 最低：前台 WS/SSE |

### 每服务器自带 FCM

管理员侧的复杂度可以接受，但 App 侧仍要支持：

- 按节点初始化不同的 FirebaseApp；
- 每个项目分别注册 token，并保存 `profileId -> token` 映射；
- token 刷新时更新对应服务器；
- 删除节点时向服务器注销 token；
- 每个 Firebase 项目都要登记 App 包名与签名指纹。

这能把复杂度从用户侧移走，但不能让 App 侧的多项目适配消失。它适合"管理员愿意自建、且不依赖中心 relay"的高级路径。

### 中央 relay

App 只依赖一个 FCM 项目；每个服务器只拿 relay 地址和节点身份，不持有 FCM service account。服务器把事件发给 relay，relay 按"设备—节点"绑定关系推送。

这是用户侧最轻的方案，代价是引入中心服务、元数据与信任问题；通知内容应尽量少，敏感内容让用户打开 App 再拉取。

### 不做原生推送

Android 还可以用前台服务保持 WS/SSE、UnifiedPush/ntfy 或 WorkManager 定期拉取。它们各自有代价：前台服务耗电且有常驻通知，UnifiedPush 需要 distributor，WorkManager 不实时。

如果第一版只要求"打开 App 能实时聊"，可以明确不做后台推送；未读消息等下次打开再同步。

## 管理员 CLI

管理员侧可以复杂，但要有可重复的工具，而不是手工拼配置：

```bash
agent node init
agent node tls --mode public-ca
agent node push --mode fcm
agent node invite --expires 10m
```

`agent node invite` 输出二维码或链接，包含地址、`serverId`、TLS 模式与指纹、一次性 code、推送模式与客户端配置。App 只消费这份清单，不关心管理员怎么配出来。

## 常见失败模式

- 把长期 token 写进二维码或节点清单，邀请链接泄露即长期失守。
- 把 FCM service account key 放进 App 或节点清单，等于把推送权限发给所有用户。
- 每个自建服务器都配 FCM，但 App 没有多 FirebaseApp 支持，最后只有最后一个项目能推。
- 中央 relay 给所有服务器同一个全局 key，任一节点都能推所有设备。
- 自签节点换证书后 App 仍信任旧 pin，或者干脆全局关闭校验。
- 切换节点只换 baseUrl，不关闭旧连接，两个节点的事件混在一起。
- 本地缓存不按 profile 隔离，删除节点后旧会话仍然出现。
- 同一服务器换了地址，App 当成新节点，凭据与会话重复。

## 一句话主线

多服务器客户端的关键不是"支持多个地址"，而是**把节点做成带身份、凭据、证书策略与推送能力的配置对象**；用户只扫码，管理员承担复杂配置，App 负责隔离与切换。

## 参考资料

- Firebase Cloud Messaging 文档（Android 客户端与服务端推送）：https://firebase.google.com/docs/cloud-messaging
- FCM HTTP v1 API（服务端发送与凭据）：https://firebase.google.com/docs/cloud-messaging/migrate-v1
- UnifiedPush（Android 去中心化推送协议）：https://unifiedpush.org/
- Android 前台服务（长连接与常驻通知的约束）：https://developer.android.com/develop/background-work/services/fgs
- Android WorkManager（后台定期任务与延迟约束）：https://developer.android.com/topic/libraries/architecture/workmanager
- Android Keystore（设备凭据的安全存储）：https://developer.android.com/privacy-and-security/keystore
