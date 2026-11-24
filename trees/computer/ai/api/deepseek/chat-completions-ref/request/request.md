---
description: "DeepSeek Chat Completions request body fields, nested objects and constraints"
描述: "DeepSeek Chat Completions 请求体字段、嵌套对象与约束"
name: "Chat Completions Request Schema"
名称: "请求字段"
---

# Request Schema（application/json）

## 顶层字段

| 字段 | 类型 | 必填 | 默认 / 约束 | 说明 |
|---|---|---|---|---|
| `messages` | `object[]` | 是 | 至少 1 项 | 对话消息列表，按 role 排序 |
| `model` | `string` | 是 | `deepseek-flash` / `deepseek-v4-pro` | 模型 ID |
| `thinking` | `object \| null` | 否 | 省略时为 null | 思考模式开关；提供时 `type` 必填，优先级高于 `reasoning_effort` |
| `reasoning_effort` | `string` | 否 | 默认 `high` | `none`/`low`/`high`/`max`；兼容映射 `minimal`→`low`，`medium`/`xhigh`→`high` |
| `max_tokens` | `integer \| null` | 否 | 1~384K（393216） | 非思考默认 8K，思考默认 64K，`max` 档 128K；输入+输出受模型上下文长度限制 |
| `response_format` | `object \| null` | 否 | 省略/普通文本 | 提供时 `type` 必填；`json_object` 启用 JSON 输出 |
| `stop` | `string \| string[] \| null` | 否 | `null` | 最多 16 个序列，每个非空且 ≤512 字节 UTF-8 |
| `stream` | `boolean \| null` | 否 | `false` | true 时以 SSE 返回增量，以 `data: [DONE]` 结束 |
| `stream_options` | `object \| null` | 否 | `null` | 必须与 `stream: true` 同用，否则 400 |
| `temperature` | `number \| null` | 否 | 1；0~2 | 思考模式下不生效 |
| `top_p` | `number \| null` | 否 | >0 且 ≤1 | 实际生效值依模型与模式，见下文 |
| `tools` | `object[] \| null` | 否 | — | 可调用工具列表，名称必须唯一 |
| `tool_choice` | `string \| object \| null` | 否 | 无 tools 为 `none`，有 tools 为 `auto` | `none`/`auto`/`required`/指定工具对象 |
| `safety_check` | `object \| null` | 否 | 默认检查 | DeepSeek 扩展，风控开关 |
| `title` | `object \| null` | 否 | — | DeepSeek 扩展，返回会话标题 |
| `logprobs` | `boolean \| null` | 否 | `false` | 是否返回输出 token 的对数概率 |
| `top_logprobs` | `integer \| null` | 否 | `null`；0~20 | 每位置返回 top N token 的对数概率，需 `logprobs: true` |
| `user_id` | `nullable` | 否 | — | 建议 ASCII 字母/数字/`_`/`-`，UTF-8 ≤512 字节，不含隐私 |
| `frequency_penalty` | `nullable` | 否（已废弃） | — | 不再支持，传入无效 |
| `presence_penalty` | `nullable` | 否（已废弃） | — | 不再支持，传入无效 |

## 嵌套对象

### thinking

`type`（`string`，必填）：`enabled` 思考模式，`disabled` 非思考模式。

### response_format

`type`（`string`，必填）：`text` 或 `json_object`。`json_object` 保证输出是合法 JSON，但**必须在 system/user 消息里同时指示模型生成 JSON**；若模型输出无法识别为 JSON，非 JSON 内容会被替换成空格（内容看起来为空，`finish_reason` 仍可能是 `stop`）；`finish_reason: length` 表示超过 `max_tokens` 或上下文上限，内容可能被截断。

### stream_options

`include_usage`（`boolean`）：true 时所有块带 `usage`，除最后一块外均为 `null`；无论是否设置，`data: [DONE]` 前最后一块的 `usage` 都是整次请求的统计。

### tools[]

每项为 `oneOf`：Function 工具、DeepSeek 联网搜索工具 `deepseek_web_search`、阅读链接工具 `deepseek_read_url`。

Function 工具：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | `string` | 是 | 恒为 `function` |
| `function` | `object` | 是 | 函数定义 |
| `function.description` | `string` | 否 | 供模型理解何时调用 |
| `function.name` | `string` | 是 | a-z/A-Z/0-9/`_`/`-`，最长 128 |
| `function.parameters` | `object` | 否 | JSON Schema；省略表示无参数 |
| `function.strict` | `boolean` | 否 | 严格 schema 模式，仅 Beta 可用 |

### tool_choice

- 字符串：`none`（不调用）、`auto`（可选）、`required`（必须调用）。
- 指定工具对象：`{"type": "function", "function": {"name": "my_function"}}`。
- 思考模式不支持 `required` 和指定工具，返回 400；声明联网工具时 `required` 按 `auto` 处理。

### safety_check / title

- `safety_check.level`（必填）：`low`（默认检查，等同不传）或 `high`（开启基础风控）。
- `title.enabled`（必填）：true 时响应带会话标题。

## 行为规则

- `thinking.type` 优先于 `reasoning_effort`；两者都省略时默认开启思考。
- `temperature` 思考模式下不生效。
- `top_p` 实际生效值：
  - `deepseek-flash`：思考模式默认 1.0，低于 0.95 按 0.95 处理；非思考模式恒为 1.0，传入值被忽略。
  - `deepseek-v4-pro`：思考模式启用工具调用时恒为 0.95，否则恒为 1.0，传入值被忽略；非思考模式使用传入值，默认 1.0。即使提供 `tools`，`tool_choice: "none"` 也会关闭工具调用。

## 一句话主线

**六个必填/核心字段搭起请求骨架，DeepSeek 扩展字段（`thinking`、`safety_check`、`title`、`user_id`）走标准参数而非 `extra_body`（HTTP 直连场景）；SDK 不原生支持的才走 `extra_body`。**

## 参考资料

- DeepSeek Chat Completions API Reference：https://api-docs.deepseek.com
