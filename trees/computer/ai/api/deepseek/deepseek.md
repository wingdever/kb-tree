---
description: "DeepSeek API reference: chat formats, FIM, tool, file, model and balance APIs, limits and pricing"
描述: "DeepSeek API 参考：对话格式、FIM、工具/文件/模型/余额接口、限流与定价"
name: "DeepSeek API Specification"
名称: "DeepSeek API 规范"
---

# 08 DeepSeek API 规范

> 来源：DeepSeek API 官方文档。端点、模型名与计费规则变化快，以官方文档为准。

DeepSeek API 兼容 OpenAI / Anthropic 形态，换 base_url 与少量扩展参数即可接入现有 SDK。本主题覆盖官方 API Reference 的 15 个端点，按端点形态与工程主题拆成 15 个子知识点。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `formats/` | 三种端点、模型名、首个调用、思考模式与扩展参数传入方式 |
| `chat-completions-ref/` | Chat Completions 字段级参考：Request、Response、messages content parts 与流式 chunk |
| `tool-calls/` | Chat Completions 工具调用完整循环、tool_calls 结构、中间插入的限制 |
| `strict/` | Beta strict 模式的启用条件、JSON Schema 支持范围与样例 |
| `responses/` | Responses API 的无状态多轮、input item 类型、call_id 与图片输入 |
| `anthropic/` | Anthropic Messages 兼容：模型映射、工具字段、消息块、服务端 Web 工具与流式 |
| `caching/` | 上下文缓存机制、命中统计、成本构成与省钱清单 |
| `kv-cache/` | 官方 Context Caching 指南：前缀单元完整匹配、持久化时机、命中字段与边界 |
| `json-mode/` | 官方 JSON Output 指南：response_format、提示词要求、失败行为与示例 |
| `fim/` | Beta 的两种续写：FIM（`POST /completions`）与 Chat Prefix（assistant `prefix: true`） |
| `tools/` | 五个独立工具 API：Search、Fetch、OCR、ASR、TTS |
| `files/` | 文件 API 四端点：上传、列表、获取、删除 |
| `models/` | `GET /models` 与模型能力元数据 |
| `balance/` | `GET /user/balance` 与扣费顺序 |
| `ops/` | 错误码、限流、token 用量与定价 |

## 建议阅读顺序

接入：`formats` → `tool-calls`；字段细查：`chat-completions-ref`。加固：`strict` → `caching` → `kv-cache` / `json-mode`。需要中间插入或 Anthropic SDK：`responses` / `anthropic`。续写：`fim`。扩展能力：`tools` → `files` → `models`。运维：`ops` → `balance`。

## 与 OpenAI 原生 Function Calling 的关键差异

| 维度 | OpenAI 原生 | DeepSeek |
|---|---|---|
| 扩展参数 | 标准参数 | `thinking` 等扩展需走 `extra_body`（OpenAI SDK 不原生支持） |
| strict 模式 | 常规可用 | **Beta**，需 `/beta` base_url，且所有 function 都设 strict |
| strict 支持类型 | 较广 | 仅 object/string/number/integer/boolean/array/enum/anyOf（+ $def/$ref），且若不支持的类型会报错 |
| string 约束 | minLength/maxLength 等 | 不支持 minLength/maxLength；支持 pattern/format(email/hostname/ipv4/ipv6/uuid) |
| 中间插入工具调用 | Responses 支持 | Chat Completions **不支持**，需换 Anthropic/Responses |
| 思考模式工具调用 | reasoning items 回传 | 须回传完整 thinking content；仅 ID 自动恢复可能 400 |
| Anthropic 格式 tool_choice=tool | 无 | 思考模式返回 400；any 在思考模式仅客户端工具也 400 |
| 模型名 | 官方名 | Claude 名按规则映射，非 claude 开头的不支持名返回 400 |

## 上线前对照

- [ ] 用正确 base_url（默认 /beta/anthropic）
- [ ] 扩展参数走 extra_body
- [ ] strict 模式满足 schema 约束（全 required + additionalProperties:false）
- [ ] 思考模式回传完整 content（含 thinking）
- [ ] 中间插入工具调用用 Responses/Anthropic，不用 Chat Completions
- [ ] Anthropic 格式 tool_result 放在 user 消息文本之前，tool_use_id 匹配
- [ ] 流式用量取 message_delta.usage，不与初始相加
- [ ] 长前缀场景设计缓存结构，并把命中率纳入监控
- [ ] FIM / Chat Prefix 走 /beta，并确认所用模型支持
- [ ] 错误码与限流接入重试和并发控制，文件类 API 遵守大小限制
- [ ] 用 `usage` 字段核对缓存命中与 token 计费，监控命中率与余额

## 一句话主线

**三种对话端点共用一套工具语义，差异集中在扩展参数、strict 的 Beta 限制与思考模式的回传要求；FIM、独立工具与文件接口补齐能力面，缓存、限流与定价决定成本和稳定性下限。**

> 相关：通用函数调用流程见 `../common/common.md`；完整调用循环见 `../loop/loop.md`；API 子树导航见 `../api.md`。
