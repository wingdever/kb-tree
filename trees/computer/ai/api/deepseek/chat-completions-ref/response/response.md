---
description: "DeepSeek Chat Completions response schema: choices, message, logprobs and usage"
描述: "DeepSeek Chat Completions 响应 schema：choices、message、logprobs 与 usage"
name: "Chat Completions Response Schema"
名称: "响应字段"
---

# Response Schema（chat completion object）

## 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | `string` | 是 | 该聊天补全的唯一标识符 |
| `choices` | `object[]` | 是 | 模型生成的补全选择列表 |
| `created` | `integer` | 是 | 创建时间，Unix 秒 |
| `model` | `string` | 是 | 生成该补全的模型名 |
| `system_fingerprint` | `string` | 是 | 后端配置指纹 |
| `object` | `string` | 是 | 恒为 `chat.completion` |
| `usage` | `object` | 否 | 本次请求的用量统计 |

## choices[]

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `finish_reason` | `string` | 是 | 停止原因，取值见下表 |
| `index` | `integer` | 是 | 该选择在列表中的索引 |
| `message` | `object` | 是 | 模型生成的消息 |
| `logprobs` | `object \| null` | 是 | 该选择的对数概率信息 |

### finish_reason 取值

| 值 | 含义 |
|---|---|
| `stop` | 自然停止或遇到 `stop` 序列 |
| `length` | 达到上下文长度或 `max_tokens` 限制 |
| `content_filter` | 输出触发过滤策略被过滤 |
| `tool_calls` | 模型进行了工具调用 |
| `insufficient_system_resource` | 推理资源不足，生成被打断 |
| `aborted` | 生成过程被中断 |

## choices[].message

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content` | `string \| null` | 是 | 补全内容 |
| `reasoning_content` | `string \| null` | 否 | 仅思考模式；最终答案之前的推理内容 |
| `tool_calls` | `object[]` | 否 | 模型生成的工具调用 |
| `role` | `string` | 是 | 恒为 `assistant` |
| `annotations` | `object[]` | 否 | 联网工具返回，`content` 中的引用 |
| `server_tool_calls` | `object[]` | 否 | DeepSeek 扩展；服务端工具调用，每元素一步，下一轮原样回传 |
| `title` | `string` | 否 | DeepSeek 扩展；`title.enabled: true` 时返回会话标题 |
| `refusal` | `string` | 否 | 请求中图片未通过内容安全审核时，指出被拦截的图片 |

### tool_calls[]

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | `string` | 是 | 工具调用 ID |
| `type` | `string` | 是 | 目前仅 `function` |
| `function` | `object` | 是 | 被调用的函数 |

`function`：`name`（`string`，必填，函数名）、`arguments`（`string`，必填，JSON 字符串形式的参数）。注意模型不保证生成合法 JSON，也可能臆造未定义的参数——调用前在代码里校验。

## choices[].logprobs

`content`（`object[] | null`，必填）：输出 token 的对数概率列表。`reasoning_content`（`object[] | null`）：思考 token 的对数概率列表。

两处列表的元素结构相同：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `token` | `string` | 是 | 输出的 token |
| `logprob` | `number` | 是 | 对数概率；`-9999.0` 表示该 token 概率极小、不在 top 20 |
| `bytes` | `integer[] \| null` | 是 | token 的 UTF-8 字节表示；无字节表示时为 null |
| `top_logprobs` | `object[]` | 是 | 该位置 top N token 及其对数概率；元素结构与本表相同（无嵌套 top_logprobs） |

## usage

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `completion_tokens` | `integer` | 是 | 生成 completion 的 token 数 |
| `prompt_tokens` | `integer` | 是 | 用户 prompt 的 token 数，等于命中 + 未命中 |
| `prompt_tokens_details` | `object` | 是 | prompt token 明细 |
| `total_tokens` | `integer` | 是 | prompt + completion 的总 token 数 |
| `completion_tokens_details` | `object` | 否 | completion token 明细 |

`prompt_tokens_details`：`cached_tokens`（`integer`，命中上下文缓存的 token 数，同 `prompt_cache_hit_tokens`）、`prompt_cache_hit_tokens`（必填）、`prompt_cache_miss_tokens`（必填）。

`completion_tokens_details`：`reasoning_tokens`（推理/思维链 token 数）、`safety_tokens`（`integer` ≥0；安全审核 token，已包含在 `completion_tokens` 中，仅 `safety_check: high` 时返回）、`server_tool_use`（`object`，使用联网工具时返回，各项计数全为 0 时省略）。

`server_tool_use`：`tool_search`（搜索次数，不含图片搜索）、`tool_fetch`（网页抓取次数）、`tool_image_search`（图片搜索次数），均为 `integer` ≥0。

## 一句话主线

**顶层只有 7 个字段，复杂度集中在 `choices[].message` 的 9 个字段与 `usage` 的两层明细；`finish_reason` 的 6 个取值是分支处理的关键。**

## 参考资料

- DeepSeek Chat Completions API Reference：https://api-docs.deepseek.com
