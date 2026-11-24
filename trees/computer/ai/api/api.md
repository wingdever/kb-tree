---
description: "Knowledge tree for API and tool-calling specifications"
描述: "API 与工具调用规范知识树导航"
name: "API and Tool-Calling Specs"
名称: "API 与工具调用规范"
---

# API 与工具调用规范知识树

本目录聚焦「照着写代码」——各厂商 Function Calling / Tool Use API 的字段结构、请求/响应 JSON 形状、控制参数与错误处理规范。每个知识点自成一个目录。

## 知识点目录

| 目录 | 内容 |
|---|---|
| `common/` | 六步循环、字段对照表、JSON Schema 规范、严格模式、ACI 工具设计 |
| `openai-function-calling/` | tools/tool_choice/tool_calls/tool 消息、strict 模式、并行、流式 |
| `anthropic-tool-use/` | tools/input_schema、tool_use/tool_result 块结构、并行、SDK 示例 |
| `gemini-function-calling/` | FunctionDeclaration/FunctionCallingConfig、FunctionCall/Response、automatic 模式 |
| `deepseek/` | 已展开为子树（15 个子知识点，覆盖官方 15 个端点）：三种对话格式及 Chat Completions 字段参考、FIM、工具/文件/模型/余额 API，以及错误码、限流、用量与定价（入口 `deepseek/deepseek.md`） |
| `mcp-tools/` | tools/list、tools/call、Tool 数据类型、结构化输出、两套错误处理 |
| `langchain-tools/` | @tool、args_schema、BaseTool、ToolNode、bind_tools、headless tools |
| `loop/` | 完整循环代码、并行/组合调用、流式聚合、错误自愈、工具设计清单 |

## 通用术语对照（先读这个）

| 概念 | OpenAI | Anthropic | Gemini | MCP |
|---|---|---|---|---|
| 声明工具 | `tools[].function` | `tools[]` | `tools[].function_declarations[]` | `tools/list` 返回的 `Tool` |
| 参数 schema | `function.parameters` | `input_schema` | `parameters`（OpenAPI Schema） | `inputSchema`（JSON Schema） |
| 模型请求调用 | `tool_calls[]` | `tool_use` block | `functionCall` part | `tools/call` 请求 |
| 调用 ID | `tool_calls[].id` | `tool_use.id` | `id` | JSON-RPC `id` |
| 返回工具结果 | `{"role":"tool",...}` | `tool_result` block | `FunctionResponse` part | `tools/call` result |

DeepSeek 兼容 OpenAI/Anthropic 两套格式（详见 `deepseek/`），扩展参数走 `extra_body`、strict 需 `/beta` base_url。

## 可靠性提示

模型版本、参数名、API 形态变化很快，记录的是 2026-11 形态，落地前对照官方文档。
