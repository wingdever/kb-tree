---
description: "DeepSeek API reference: chat formats, FIM, tool, file, model and balance APIs, limits and pricing"
描述: "DeepSeek API 参考：对话格式、FIM、工具/文件/模型/余额接口、限流与定价"
name: "DeepSeek API Specification"
名称: "DeepSeek API 规范"
---

# 08 DeepSeek API 规范

> 来源：DeepSeek API 官方文档。端点、模型名与计费规则变化快，以官方文档为准。

DeepSeek API 兼容 OpenAI / Anthropic 形态，换 base_url 与少量扩展参数即可接入现有 SDK。本主题覆盖官方 API Reference 的 15 个端点，按端点形态与工程主题拆成 15 个子知识点。

## 建议阅读顺序


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

