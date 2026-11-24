---
description: "Anthropic tools, input_schema, tool_use and tool_result blocks"
描述: "Anthropic 的工具定义、输入 schema 与工具调用块结构"
name: "Anthropic Tool Use"
名称: "Anthropic 工具使用"
---

# 03 Anthropic Tool Use

## tools 参数

请求顶层传 `tools` 数组，每项是一个工具定义：

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Unit for temperature"
      }
    },
    "required": ["location"]
  }
}
```

字段：

| 字段 | 说明 |
|---|---|
| `name` | 工具唯一名称，建议 snake_case |
| `description` | 用途描述，模型据此判断何时调用——写清楚 |
| `input_schema` | JSON Schema 对象，定义输入参数 |

较新版本还提供 `input_examples`（输入示例，帮助模型理解用法）等字段。

## tool_choice 控制

| 值 | 行为 |
|---|---|
| `{"type":"auto"}`（默认） | 模型自行决定是否调用工具 |
| `{"type":"any"}` | 模型必须调用某个工具 |
| `{"type":"tool","name":"get_weather"}` | 强制调用指定工具 |

## 工具调用流程（Messages API）

1. 带 `tools` 和 `tool_choice` 发消息请求。
2. 若模型决定调用工具，响应 `stop_reason` 为 `"tool_use"`，`content` 数组中出现 **`tool_use` block**：

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "get_weather",
  "input": { "location": "San Francisco, CA", "unit": "celsius" }
}
```

3. 你的代码用 `input` 执行对应函数。
4. 把工具结果作为**新的 user 消息**回灌，消息 content 含 **`tool_result` block**：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "15 degrees celsius"
    }
  ]
}
```

错误处理时 `tool_result` 用 `is_error: true`：

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01A09q90qw90lq9",
  "content": "Error: location not found",
  "is_error": true
}
```

5. 再次请求模型，得到最终文本响应。

**关键规则**：每个 `tool_use` block 必须有对应的 `tool_result`，用 `tool_use_id` 关联。可以在一个 user 消息里放多个 `tool_result` block（并行调用的结果）。

## 并行工具调用

模型可在一轮响应中返回多个 `tool_use` block。执行后把所有对应的 `tool_result` block 放进同一个 user 消息 content 数组回灌。

## 严格工具使用（Strict Tool Use）

类似 OpenAI strict 模式，让 `input` 严格符合 `input_schema`：在工具定义上加 `strict: true`，此时 schema 需满足受限 JSON Schema 子集（如所有字段 required、对象 closed）。具体约束以官方文档为准。

## 客户端 vs 服务端工具

- **客户端工具**（本节）：你定义 schema、你执行、你回灌结果。
- **服务端工具**：模型厂商在服务端执行（如 web search、code execution），结果自动进入对话。

## 工具设计要点（Anthropic 官方强调）

- 工具定义与文档要和提示词一样精雕细琢（ACI 原则）。
- 给模型足够 token 在写之前先思考。
- 让格式贴近自然文本；避免格式开销（精确行数统计、字符串转义）。
- 好工具定义含：示例用法、边界情况、输入格式要求、与其他工具的清晰边界。
- 防错（poka-yoke）：改参数设计让错误更难发生。
- 构建 SWE-bench Agent 时，打磨工具花的时间超过打磨提示词。

## SDK 示例（ anthropic Python ）

```python
import anthropic

client = anthropic.Anthropic()

tools = [{
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"}
        },
        "required": ["location"],
    },
}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = get_weather(**tool_use.input)
    messages = [
        {"role": "user", "content": "What's the weather in San Francisco?"},
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
            }],
        },
    ]
    final = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
```

## 参考资料

- Anthropic Tool Use 文档：https://docs.anthropic.com/en/docs/build-with-claude/tool-use
