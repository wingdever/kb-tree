---
description: "Yunhu as an agent channel: official open API, webhook events, bot tools and streaming messages"
描述: "云湖作为 Agent 渠道：官方开放 API、Webhook 事件、机器人工具与流式消息"
name: "Yunhu Channel"
名称: "云湖渠道"
---

# 云湖渠道（Yunhu）

> 来源：云湖官网与官方 Bot 开发文档。接口、字段与能力范围变化快，以官方文档为准。

云湖（YunhuM3，yhchat.com）是**非腾讯**的即时通讯/社交平台，客户端与 Web 端都基于 Flutter，全平台可用。它有**官方开放的 API、SDK 与事件推送**，**没有个人号被风控封号的风险**。

## 为什么适合做 Agent 渠道

- **官方开放接口**：提供完整消息 API 与 SDK，支持各种事件推送，可作为机器人接入。
- **为生成式 AI 设计**：支持**流式消息输入输出**、Markdown / HTML 消息，适合模型逐段输出。
- **多种指令类型**：普通指令、直发指令、表单指令、交互指令；表单字段支持 input / textarea / select / radio / checkbox / switch。
- **平台能力**：消息云端存储、多设备同时在线、群成员不限人数；机器人可收到设置变更事件与表情包事件。
- **身份是机器人账号**，不接管真人 QQ/微信这类个人号，账号边界清晰。

## 接入模型

```
云湖用户 / 群 → 云湖平台事件 → Webhook POST → 适配层（bot_id + token）→ Agent 会话
Agent 回复 → 云湖开放 API（Send.*）→ 云湖消息
```

关键约束（来自官方适配器文档）：

- **事件里不含 bot_id**，必须在配置里显式指定 `bot_id`；每个 bot 配独立 `webhook_path`（如 `/webhook/bot1`），否则多机器人事件会混。
- 每个 bot 需要平台提供的 `token`，与 `bot_id` 一起配置。
- 发送侧指定目标：`To("user" | "group", id)`，第二个参数可传列表做批量；多 bot 用 `Using("bot1")` 选择。

## 工具面（官方适配器示例）

| 能力 | 示意 |
|---|---|
| 发送 / 编辑 / 撤回 | `Text`、`Edit(msg_id, ...)`、`Recall(msg_id)` |
| 流式输出 | `Stream("text", async_generator)`，每段 `yield` bytes |
| 公告看板 | `Board`、`DismissBoard`，可配 `Expire` / `ForMember`；不指定 `To()` 为全局 |
| 富格式 | Markdown / HTML，`content_type` 可指定 |
| 多 bot / 批量 | `Using(bot)`、`To(type, [id1, id2])` |

一个常见模式：先发「搜索中…」拿 `message_id`，耗时操作后用 `Edit` 更新成结果——流式场景则用 `Stream` 逐段推送。

## 与 dsh 生态的关系

本次检索**没有找到专门的 dsh 云湖渠道插件**。可行路线：

1. **通用桥接**：云湖 Webhook → 自建 HTTP 服务 → dsh headless（`dsh headless --session-id ...` 复用会话）→ 结果回写云湖 API。是外部服务编排。
2. **等待/寻找社区插件**：dsh 插件市场里有 `dsh-channels` 这类多平台渠道插件（微信 / QQ / 钉钉 / 飞书 / Telegram），但其文档未列出云湖；接入前应确认兼容矩阵。
3. **不要把云湖当 QQ 协议端**：云湖没有 OneBot 11 那套，它是自有开放 API + Webhook，适配层要自己写或找现成 adapter（如 Python 侧的 ErisPulse-YunhuAdapter）。

## 合规与安全

- 走官方开放接口，无 QQ 协议端那种违反用户协议的风险；但仍需遵守云湖平台规则与机器人政策。
- `token`、`bot_id` 属于凭据，写进配置而不是正文/代码，不提交到 git。
- Webhook 端点要校验来源，避免被第三方伪造事件。

## 一句话主线

**云湖是「官方 API + Webhook + 流式消息」的渠道：身份是机器人账号，没有个人号封号风险；代价是没有现成 dsh 插件，适配层要自己接。**

