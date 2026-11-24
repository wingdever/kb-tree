---
description: "Yunhu platform: Flutter IM, official bot ecosystem, open API, event push and built-in AI capabilities"
描述: "云湖平台：Flutter IM、官方机器人生态、开放 API、事件推送与内置 AI 能力"
name: "Yunhu Platform"
名称: "云湖平台"
---

# 云湖（YunhuM3）

> 来源：云湖官网、开放文档与 Bot 开发文档。接口、字段与能力范围变化快，以官方文档为准。

云湖（yhchat.com）是**非腾讯**的社交聊天平台，客户端与 Web 端都基于 Flutter，由北京九万智达科技有限公司运营。本页从**平台本身**展开；把它作为 Agent 渠道的接入细节见 `../../../ai/agent/channel/yunhu/`。

## 平台形态

- **全平台**：macOS、Windows、Android、iOS、Linux、鸿蒙、Web；客户端与网页版都是 Flutter。
- **多设备**：同一账号可在多台设备同时登录并同时收到消息。
- **云端存储**：消息存云端，任意设备可查历史。
- **群能力**：群成员不限制人数，另设「全员大群」包含所有用户。
- **消息格式**：支持 Markdown 与 HTML、GIF、撤回不限时。
- **流式消息**：原生支持流式输入输出，面向生成式 AI 场景。

## 身份与机器人生态

平台身份是**机器人账号**，不接管用户的真人账号：

- 官方机器人、服务监控机器人、RSS 订阅机器人等。
- 依托开放服务接口，用户可自建机器人。
- 指令类型：普通指令、直发指令、表单指令、交互指令。
- 表单字段类型：input / textarea / select / radio / checkbox / switch。
- 事件：新成员入群、好友添加、表情包事件、机器人设置变更（`yunhu_bot_setting`）、快捷菜单。

机器人接入配置的关键约束：**事件里不含 bot_id**，必须在配置里显式指定；每个 bot 配独立 `webhook_path`，否则多机器人事件会混在一起。每个 bot 需要平台提供的 `token`。

## 开放接口

官方开放文档按以下结构组织：

| 分组 | 内容 |
|---|---|
| 接入准备 | 开发须知、服务端 API 列表、服务端错误代码 |
| 消息管理 | 发送与操作消息 |
| 群组管理 | 群相关操作 |
| 看板管理 | 公告看板 |
| 事件订阅 | Webhook 与事件推送 |
| SDK | 官方 SDK 与非官方 SDK（如 Python 侧的 ErisPulse-YunhuAdapter） |

常见发送能力（以适配器形态为例）：`Text`、`Edit(msg_id, ...)`、`Recall(msg_id)`、`Stream(type, async_generator)`、`Board` / `DismissBoard`（配 `Expire`、`ForMember`）、多 bot 用 `Using(bot)`、批量用 `To(type, [id1, id2])`。

典型模式：先发「搜索中…」拿 `message_id`，耗时操作后用 `Edit` 更新为结果；流式输出用 `Stream` 逐段推送 bytes。

## 内置 AI 能力

- **多模型**：兼容 DeepSeek、通义千问、豆包等，支持任意符合 OpenAI API 标准的模型接入与切换。
- **知识库**：内置 RAG 引擎，处理 TXT、CSV 等文档，做语义检索。
- **智能体框架**：自然语言指令配置自动化任务，支持多步骤任务与 MCP 上下文协议。
- **可视化流程**：拖拽式设计复杂流程，实时校验节点参数与循环依赖。
- **插件生态**：标准化接入规范，支持 API Key / OAuth2.0 认证。
- **安全合规**：细粒度权限、审计日志、数据隔离，支持云托管与私有化部署。

## 与 Agent 渠道的关系

本页是平台视角的**主宿主**：讲云湖是什么、给谁什么身份、开放什么能力。`../../../ai/agent/channel/yunhu/` 是同一关系在「Agent 渠道接入」视角下的挂载——讲 bot_id / webhook_path 怎么接、dsh 没有现成插件时如何通用桥接。两处文字不同是正常的。

## 一句话主线

**云湖是「Flutter 全平台 + 官方机器人身份 + 开放 API/Webhook + 内置 AI」的社交平台；作为生态样本，它把身份风险降到最低，把接口与流式能力开放给开发者。**

> 相关：软件生态总览见 `../../`；Agent 渠道接入见 `../../../ai/agent/channel/yunhu/`；API 规范见 `../../../ai/api/api.md`。
