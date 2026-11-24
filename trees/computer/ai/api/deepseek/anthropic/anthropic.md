---
description: "DeepSeek Anthropic Messages compatibility: models, tools, content blocks, server tools and streaming"
描述: "DeepSeek Anthropic Messages 兼容：模型映射、工具字段、消息块、服务端工具与流式"
name: "DeepSeek Anthropic Compatibility"
名称: "Anthropic 兼容"
---

# Anthropic Messages API 兼容

> 来源：Anthropic Messages 规范与 DeepSeek 兼容说明。字段与支持范围变化快，以官方文档为准。

base_url：`https://api.deepseek.com/anthropic`。认证：`x-api-key: <KEY>` 或 `Authorization: Bearer <KEY>`。

```python
import anthropic

client = anthropic.Anthropic()   # ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic

message = client.messages.create(
    model="deepseek-flash",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Hi, how are you?"}]}],
)
```

## 模型名映射

- `claude-opus*` → `deepseek-v4-pro`（按 V4 Pro 价计费）
- `claude-haiku*` / `claude-sonnet*` → `deepseek-flash`
- 其他 `claude*` → `deepseek-flash`
- 非 `claude` 开头的不支持模型名 → 400

## 工具字段（Anthropic 格式）

**tools**：客户端工具提供 `name`、`input_schema`、可选 `description`，**省略 `type`**。传 `type:"custom"` 给客户端工具会返回 422。Web 工具需声明 server tools `deepseek_web_search`、`deepseek_read_url`（不能与其他 server tools 一起声明）。

| 字段 | 支持情况 |
|---|---|
| `name` | 完全支持 |
| `input_schema` | 完全支持 |
| `description` | 完全支持 |
| `cache_control` | 忽略 |

**tool_choice**：

| 值 | 支持情况 |
|---|---|
| `none` | 完全支持 |
| `auto` | 支持（`disable_parallel_tool_use` 被忽略） |
| `any` | 非思考模式强制工具调用；思考模式下若声明了 server tool 视为 auto，仅客户端工具则返回 400 |
| `tool`（指定命名工具） | 非思考模式选择指定客户端工具；思考模式返回 400 |

## 返回工具结果（Anthropic 格式）

多轮时每轮都在 `messages` 带完整历史。含客户端 `tool_use` 块的助手消息之后，**下一条必须是 `user` 角色**，并为每个工具调用包含一个 `tool_result`（`tool_use_id` 匹配）。把**所有 `tool_result` 块放在该 user 消息的任何文本之前**。

思考模式继续工具调用时，须回传助手完整 `content` 数组（含 thinking 与 tool-use 块）。若省略 thinking 内容，服务可能用工具调用 ID 尝试恢复；恢复失败则返回 400。不要依赖自动恢复。

## 消息类型支持要点

| content block | 支持情况 |
|---|---|
| text | 完全支持 |
| image | `deepseek-flash` 支持 user 消息和 tool_result 中的图片；assistant 消息中图片返回 400。`deepseek-v4-pro` 不处理图片，替换为 `[Unsupported Image]`。`source.type` 可为 base64（jpeg/png/gif/webp）、url、file（file 需 header `anthropic-beta: files-api-2025-04-14`） |
| document | `file`、`text` source 在 user 消息支持 |
| thinking | 支持 |
| tool_use | `id`、`input`、`name` 完全支持 |
| tool_result | `tool_use_id`、`content` 完全支持；`is_error` 被忽略 |
| server_tool_use / web_search_tool_result | 支持 |
| redacted_thinking / code_execution_tool_result / mcp_tool_use / mcp_tool_result / container_upload / search_result | 不支持 |

## 其他参数

- `max_tokens`：支持，HTTP 请求中可选，默认/有效上限取决于模型、思考模式与强度；Anthropic SDK 要求此参数。
- `temperature`：0.0~2.0，非思考模式有效，思考模式固定 1.0。
- `top_p`：依模型而定（详见官方文档）；`tool_choice={"type":"none"}` 即使提供 tools 也禁用工具调用。
- `stop_sequences`：完全支持，最多 16 个，每个非空字符串 ≤512 字节（UTF-8）。
- `thinking`：`type: enabled/disabled`，`adaptive` 视为 enabled，`budget_tokens` 忽略。
- `output_config`：仅 `effort` 支持。
- `top_k`、`container`、`mcp_servers`、`service_tier`、`anthropic-version` 忽略。
- DeepSeek 扩展：`safety_check: {"level":"high"}` 开启内容安全；`title: {"enabled":true}` 返回会话标题。

## 服务端 Web 工具

`server_tool_use` 块描述服务端执行的工具，含 `id`、`name`、`input`、`caller`。Web 搜索中 `name` 为 `web_search`，`input` 含 `query`，`caller` 为 `{"type":"direct"}`；匹配的 `web_search_tool_result` 用相同 `tool_use_id`。**服务执行搜索并继续生成答案，客户端无需执行工具或提供 tool_result**。

`usage.server_tool_use`：`web_search_requests`（尝试次数，含被拒/无效/失败，可超 max_uses）、`tool_search`（成功且返回结果≥1 的搜索次数，按调用计非按结果条计）。无搜索尝试时省略该对象；声明工具不保证出现。非流式读 `usage.server_tool_use`，流式读最终 `message_delta.usage.server_tool_use`。

## 流式（Anthropic 格式）

`stream: true` 返回 SSE：以 `message_start` 开始，内容块发 `content_block_start`/`content_block_delta`/`content_block_stop`，以 `message_delta`、`message_stop` 结束，中间可夹 `ping`。**不发送 `data: [DONE]`**。

用最终 `message_delta.usage` 作为请求 token 用量，不要与 `message_start` 的初始用量相加。`input_tokens` 不含缓存命中，`cache_read_input_tokens` 为命中量，`cache_creation_input_tokens` 当前为 0；总输入 = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`。在 `message_stop` 前关闭连接表示响应不完整。

## 一句话主线

**换 base_url 和认证头即可用 Anthropic SDK 接入；字段等价但有专属差异——工具省略 `type`、`tool_result` 必须在文本前、思考模式回传完整内容、流式用量取最终 delta。**

> 相关：工具调用循环见 `../tool-calls/`；Responses 的中间插入能力见 `../responses/`；缓存命中计费见 `../caching/`。
