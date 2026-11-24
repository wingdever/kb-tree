---
description: "DeepSeek Chat Completions API reference: request, response, messages and streaming schemas"
描述: "DeepSeek Chat Completions 接口参考：请求、响应、消息与流式 schema"
name: "Chat Completions API Reference"
名称: "Chat Completions 接口参考"
---

# Chat Completions API Reference

> 来源：DeepSeek Chat Completions API 官方 API Reference。字段与约束变化快，以官方文档为准。

`POST https://api.deepseek.com/chat/completions`，根据输入上下文让模型补全对话。本节点按官方 schema 逐字段记录请求、响应、消息结构与流式增量，是对 `../formats/`、`../tool-calls/` 的字段级补全。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `request/` | Request `application/json` 全部顶层字段、嵌套对象、约束与行为规则 |
| `response/` | Responses `chat completion object` 全部字段树、`finish_reason` 取值、`usage` 明细 |
| `messages/` | `messages[]` 各角色消息与 content parts（text / image_url / file） |
| `streaming/` | 流式 SSE 的增量 chunk、`data: [DONE]`、末块 usage |

## 一句话主线

**请求侧 20 个顶层字段中有 6 个是 DeepSeek 扩展或工具相关；响应侧把 `choices[].message` 与 `usage` 两层展开，流式只在末块给一次完整用量。**

> 相关：端点与首个调用见 `../formats/`；工具调用循环见 `../tool-calls/`；strict 见 `../strict/`；缓存字段见 `../caching/`。
