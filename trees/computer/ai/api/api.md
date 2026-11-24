---
description: "Knowledge tree for API and tool-calling specifications"
描述: "各厂商工具调用 API 的规范、字段与错误处理"
name: "API and Tool-Calling Specs"
名称: "API 与工具调用规范"
---

# API 与工具调用规范知识树

本目录聚焦「照着写代码」——各厂商 Function Calling / Tool Use API 的字段结构、请求/响应 JSON 形状、控制参数与错误处理规范。每个知识点自成一个目录。

## 通用术语对照（先读这个）

| 概念 | OpenAI | Anthropic | Gemini | MCP |
|---|---|---|---|---|
| 声明工具 | `tools[].function` | `tools[]` | `tools[].function_declarations[]` | `tools/list` 返回的 `Tool` |
| 参数 schema | `function.parameters` | `input_schema` | `parameters`（OpenAPI Schema） | `inputSchema`（JSON Schema） |
| 模型请求调用 | `tool_calls[]` | `tool_use` block | `functionCall` part | `tools/call` 请求 |
| 调用 ID | `tool_calls[].id` | `tool_use.id` | `id` | JSON-RPC `id` |
| 返回工具结果 | `{"role":"tool",...}` | `tool_result` block | `FunctionResponse` part | `tools/call` result |

DeepSeek 兼容 OpenAI/Anthropic 两套格式，扩展参数走 `extra_body`、strict 需 `/beta` base_url。

## 可靠性提示

模型版本、参数名、API 形态变化很快，记录的是 2026-11 形态，落地前对照官方文档。
