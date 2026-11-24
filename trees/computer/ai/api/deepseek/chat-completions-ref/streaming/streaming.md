---
description: "DeepSeek Chat Completions SSE streaming chunks, terminator and final usage"
描述: "DeepSeek Chat Completions 的 SSE 增量块、结束符与末块用量"
name: "Chat Completions Streaming"
名称: "流式响应"
---

# 流式响应（SSE）

`stream: true` 时，响应以 **data-only server-sent events** 分块返回增量，消息流以 `data: [DONE]` 结束。

## chunk 形态

官方 schema 明确给出的流式约定：

- `stream_options` 必须与 `stream: true` 同用，否则 400。
- `include_usage: true` 时所有块都带 `usage` 字段，除最后一块外值为 `null`；不设置或为 false 时，除最后一块外都不含 `usage`。
- `data: [DONE]` 之前的最后一块在 `usage` 中给出整次请求的 token 统计。**不会单独下发只含 usage 的块**——统计附加在最后一个内容块上，该块的 `choices` 数组恰好只有 1 个元素，不含新增内容且 `finish_reason` 非 null。
- 增量内容采用 OpenAI 兼容形态：`choices[].delta` 逐块携带 `role`、`content`、`reasoning_content`、`tool_calls` 的片段；`tool_calls` 通过 `index` 拼接，`function.arguments` 是分片字符串，客户端需自己累积后 `json.loads`。具体字段形态以官方流式示例为准。
- `finish_reason` 在生成结束时出现，取值与非流式相同。

## 保活与解析

- 流式请求会夹带 `: keep-alive` 注释行；自行解析 SSE 时需忽略注释与空行，不要把 `data: [DONE]` 当成 JSON 块。
- 用量**只取最终块的 `usage`**，不要累加中间块的增量。
- `reasoning_content` 与 `content` 分别累积：思考模式下前者是推理过程，后者是最终答案。
- 在 `data: [DONE]` 之前关闭连接表示响应不完整——不要把它当成正常结束。

## 对照：Anthropic 格式不同

Anthropic Messages 格式也支持 `stream: true`，但事件名是 `message_start` / `content_block_start` / `content_block_delta` / `content_block_stop` / `message_delta` / `message_stop`，中间可夹 `ping`，且**不发送 `data: [DONE]`**；用量取 `message_delta.usage`。

## 一句话主线

**Chat Completions 的增量在 `choices[].delta`，以 `data: [DONE]` 结束，用量只在末块给一次；Anthropic 格式用另一套事件名且没有 `[DONE]`。**

## 参考资料

- DeepSeek Chat Completions API Reference：https://api-docs.deepseek.com
