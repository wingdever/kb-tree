---
description: "OpenAI tools, tool_choice, tool_calls, strict mode and streaming"
描述: "OpenAI 的工具定义、控制参数、严格模式与流式调用"
name: "OpenAI Function Calling"
名称: "OpenAI 函数调用"
---

# 02 OpenAI Function Calling

两种集成：**Responses API**（新）与 **Chat Completions API**。GPT-6 Astra / GPT-6.1 Sol 的 tool calling 需用 Responses API；Chat Completions 示例用 GPT-5.6 Terra（reasoning 关闭）。

> 来源：OpenAI Function Calling 官方文档。API 形态与模型名变化快，以官方文档为准。

## 核心五步流程

1. 带 `tools` 向模型发请求。
2. 接收模型返回的 tool call。
3. 应用侧用工具调用的参数执行代码。
4. 带工具输出再次请求模型。
5. 收到最终响应（或更多 tool calls）。

## 定义函数（Chat Completions 形态）

```json
{
  "type": "function",
  "function": {
    "name": "get_horoscope",
    "description": "Get today's horoscope for an astrological sign.",
    "parameters": {
      "type": "object",
      "properties": {
        "sign": {
          "type": "string",
          "description": "An astrological sign like Taurus or Aquarius"
        }
      },
      "required": ["sign"],
      "additionalProperties": false
    },
    "strict": true
  }
}
```

### FunctionDefinition 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | string | 必填。只允许 `a-z A-Z 0-9 _ -`，最长 64。 |
| `description` | optional string | 描述函数做什么，供模型判断何时/如何调用。 |
| `parameters` | optional FunctionParameters | JSON Schema 对象。省略则定义空参数函数。 |
| `strict` | optional boolean/null（默认 false） | true 时模型严格按 schema 生成参数；仅支持 JSON Schema 子集。 |

工具类型 `type` 目前支持 `function` 与 `custom`（自由文本/语法格式，本手册聚焦 function）。

## 完整代码示例（Chat Completions）

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_horoscope",
        "description": "Get today's horoscope for an astrological sign.",
        "parameters": {
            "type": "object",
            "properties": {
                "sign": {"type": "string", "description": "An astrological sign like Taurus or Aquarius"}
            },
            "required": ["sign"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}]

def get_horoscope(sign):
    return f"{sign}: Next Tuesday you will befriend a baby otter."

messages = [{"role": "user", "content": "What is my horoscope? I am an Aquarius."}]

response = client.chat.completions.create(model="gpt-5.5", messages=messages, tools=tools)
messages.append(response.choices[0].message)   # 把助手消息（含 tool_calls）加入历史

for tool_call in response.choices[0].message.tool_calls or []:
    if tool_call.function.name == "get_horoscope":
        args = json.loads(tool_call.function.arguments)
        result = get_horoscope(args["sign"])
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps({"horoscope": result}),
        })

response = client.chat.completions.create(model="gpt-5.5", messages=messages, tools=tools)
print(response.choices[0].message.content)
```

要点：模型返回的 `tool_calls` 每个含 `id`、`function.name`、`function.arguments`（JSON 字符串，需 `json.loads`）。回灌时用 `role: "tool"` + `tool_call_id` + `content`（字符串）。

## tool_choice 控制

| 值 | 行为 |
|---|---|
| `"auto"`（默认） | 调用零个、一个或多个函数 |
| `"required"` | 至少调用一个函数 |
| `"none"` | 不调用函数（等效不传 tools） |
| `{"type":"function","name":"get_weather"}` | 强制调用指定函数 |
| `{"type":"allowed_tools","mode":"auto","tools":[...]}` | 限制可调用的工具子集；`mode` 为 `auto` 或 `required` |

`allowed_tools` 的价值：限制可用子集但**不修改传入的 tools 列表**，从而最大化 prompt caching 收益。

```json
"tool_choice": {
  "type": "allowed_tools",
  "mode": "auto",
  "tools": [
    {"type": "function", "name": "get_weather"},
    {"type": "function", "name": "search_docs"}
  ]
}
```

## 并行函数调用（parallel_tool_calls）

- GPT-5 起，模型可在一轮并行调用多个函数（内置工具参与时也可并行，但内置工具本身不能进入并行批次）。
- 设 `parallel_tool_calls: false` 可确保每轮只调用零或一个工具。
- 微调模型若一轮调用多个函数，这些调用会禁用 strict 模式。
- `gpt-4.1-nano-2025-04-14` 快照开启并行时偶尔对同一工具重复调用，建议对该快照禁用。

## Strict 模式

Strict 基于 Structured Outputs，要求：

- `parameters` 中每个 object 都设 `additionalProperties: false`
- `properties` 中所有字段都列入 `required`
- 可选字段用 `"type": ["string", "null"]` 表示

若 `strict: true` 而 schema 不满足，请求被拒绝并返回缺失约束详情。省略 `strict` 时：Responses 会尝试把 schema 规范化为 strict，不兼容则回退到非严格 best-effort（响应中显示 `strict: false`）；Chat Completions 默认非严格。Responses 中显式设 `strict: false` 可退出 strict。

局限：部分 JSON Schema 特性不支持。微调模型的 schema 在首次请求时被处理并缓存，schema 每次变化可能导致更高延迟；缓存的 schema 不适用零数据保留。

## 流式工具调用

设 `stream: true`，`delta.tool_calls` 增量到达。**必须聚合 delta 成完整 `tool_calls` 再执行**。Responses API 会为每个函数调用发 `response.output_item.added` 事件，随后是 `response.function_call_arguments.*` 事件。

## 推理模型注意事项

对 GPT-5、o4-mini 等推理模型，带工具调用的响应中返回的 reasoning items **必须连同工具输出一起回传**。

## 内置工具与工具搜索

- 内置工具：web search、file search、computer use、MCP server 访问等。
- 工具搜索（tool search）：函数很多或 schema 很大时，延迟加载很少用的工具。仅 `gpt-5.4` 及之后支持 `tool_search`。
- Agents API sessions：用 Functions 注册函数并处理 session action 请求。

## 函数定义最佳实践

- 显式描述函数目的、每个参数（及格式）、输出代表什么。
- 用 system prompt 说明何时（以及何时不）用每个函数——明确告诉模型该做什么。
- 包含示例与边界案例，尤其用于纠正反复出现的失败（注意：加示例可能损害推理模型性能）。
- 对延迟加载工具：详细指南放函数描述，namespace 描述保持简洁。
