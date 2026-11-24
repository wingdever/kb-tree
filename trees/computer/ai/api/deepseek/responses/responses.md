---
description: "DeepSeek Responses API: stateless multi-turn, input items and image input"
描述: "DeepSeek Responses API：无状态多轮、input item 与图片输入"
name: "DeepSeek Responses API"
名称: "Responses API"
---

# Responses API（`/responses`）

OpenAI Responses API 格式，**无状态**：服务和对话不存服务端，多轮需每轮在 `input` 带完整历史。

## 输入项

- `input`：字符串，或 input item 列表。item 类型：`message`/`function_call`/`function_call_output`/`custom_tool_call`/`custom_tool_call_output`/`reasoning`/`web_search_call`，其他类型忽略。
- 消息角色：`user`/`assistant`/`system`/`developer`（developer 按 user 处理）。
- `call_id`：`function_call`/`function_call_output` 的配对 ID，必须非空唯一，每个 function_call 必须有匹配的 function_call_output。
- `function_call` item 含 `name`、`arguments`（JSON 字符串）；`function_call_output` 含 `output`。
- `instructions`：系统级指令，插入为上下文第一条 system 消息。
- `reasoning.effort`：`none/low/high/max`（`minimal`→`low`，`medium`/`xhigh`→`high` 兼容映射）。
- 图片：`deepseek-flash` 在 user/developer 消息及 function_call_output 中支持 `input_image`；system/assistant 消息中的图片返回 400。不支持文件输入。

> 在对话中间插入工具调用请用 Responses 或 Anthropic API——Chat Completions 做不到。

## 一句话主线

**每轮带全量历史、用 `call_id` 配对工具结果与调用——无状态换来的好处是可以在历史中间插入工具调用。**

## 参考资料

- DeepSeek API 文档：https://api-docs.deepseek.com
