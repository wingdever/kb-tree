---
description: "Gemini FunctionDeclaration, configs and function response parts"
描述: "Gemini 的函数声明、调用配置与响应部件"
name: "Gemini Function Calling"
名称: "Gemini 函数调用"
---

# 04 Gemini Function Calling

> 来源：Google Gemini Function Calling 官方文档。模型名与 API 形态变化快，落地前以官方文档为准。

## 核心理念

模型**不直接调用函数**——它生成结构化数据，指定函数名和建议参数。你的应用执行外部 API 并把结果回灌。

## 声明函数（FunctionDeclaration）

按 **OpenAPI 3.0 Schema** 格式定义。字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | string | 必填。以字母或下划线开头；只允许 `a-z A-Z 0-9 _ . -`，最长 64。 |
| `description` | optional string | 用途描述，模型据此决定如何/是否调用——强烈建议提供。 |
| `parameters` | optional Schema | OpenAPI JSON Schema Object 格式的参数描述。 |
| `response` | optional Schema | 输出的 OpenAPI Schema 格式描述。 |

### Schema 字段（OpenAPI 3.0 子集）

| 字段 | 说明 |
|---|---|
| `type` | 枚举：`STRING`、`INTEGER`、`BOOLEAN`、`NUMBER`、`ARRAY`、`OBJECT` |
| `description` | 数据描述 |
| `enum` | 原始类型的可选值 |
| `items` | `ARRAY` 元素类型（Schema[]） |
| `properties` | `OBJECT` 的属性 |
| `required` | `OBJECT` 的必填属性 |
| `nullable` | 是否可为 null |

限制：每次请求最多 **128** 个函数声明。

## 请求语法（REST / generateContent）

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/${MODEL_ID}:generateContent \
  -d '{
    "contents": [{ ... }],
    "tools": [{
      "function_declarations": [ { ... } ]
    }]
  }'
```

## FunctionCallingConfig（工具调用控制）

| 字段 | 说明 |
|---|---|
| `mode` | `AUTO`（默认，模型自行决定函数调用或自然语言）/ `NONE`（不函数调用）/ `ANY`（强制函数调用） |
| `allowed_function_names` | 仅 `ANY` 时设置；限定模型从这些函数中选择，须匹配 `FunctionDeclaration.name` |
| `stream_function_call_arguments` | true 时分块增量返回函数参数，默认 false |

```python
config = types.GenerateContentConfig(
    tools=[get_weather_tool],
    function_calling_config=types.FunctionCallingConfig(
        mode=types.FunctionCallingMode.ANY,
        allowed_function_names=["get_weather"],
    ),
)
```

Gemini SDK 的 `tool_choice`（Python `GenerateContentConfig(tool_choice=...)`）常用模式：`"auto"`、`"any"`、`"none"`、`"validated"`（强制遵守 schema，减少畸形调用）、`allowed_tools`（限制可选函数）。

## functionCall 与 functionResponse

### functionCall（模型返回）

| 字段 | 说明 |
|---|---|
| `name` | 要调用的函数名 |
| `args` | JSON 对象格式的参数与值 |
| `id` | 可选。v1beta1 API、Gemini 3 及之后支持；执行后回传匹配 id |
| `thought_signature` | 不透明 token，封装模型内部推理状态。若存在，**下一轮必须带回**，以维持多步工具使用的上下文 |

示例：

```json
{
  "candidates": [{
    "content": {
      "role": "model",
      "parts": [{
        "function_call": {
          "name": "get_current_weather",
          "args": { "location": "Boston, MA" }
        }
      }]
    }
  }]
}
```

### functionResponse（回灌结果）

| 字段 | 说明 |
|---|---|
| `name` | 对应的函数名 |
| `response` | JSON 对象格式的函数输出 |
| `id` | 可选。匹配对应 `functionCall.id` |
| `parts` | 可选多模态部分（图片、音频、视频） |

### 顺序规则（重要）

不要把 `functionCall` 与 `functionResponse` parts 跨轮交错。为确保每个 response 匹配正确的 call，`FunctionResponse` parts 必须按模型返回的 `functionCall` parts **完全相同的顺序**放在 parts 数组中，且每个 `functionResponse.name` 对应相应 `functionCall.name`。此位置顺序规则适用于所有支持的 Gemini 模型与 API 版本。

## 带思考（thinking）的函数调用

启用 thinking 时，必须从模型响应对象取 `thought_signature`，回灌函数执行结果时一并带回。

## Automatic Function Calling（SDK 自动执行）

Google Gen AI SDK 可直接把 Python 函数作为工具传入，SDK 自动执行调用循环：

```python
from google import genai
from google.genai import types

client = genai.Client()

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(tools=[get_current_weather]),
)
```

禁用自动执行：

```python
config = types.GenerateContentConfig(
    tools=[get_current_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
function_calls = response.function_calls   # 手动处理
```

`maximum_remote_calls` 控制自动函数调用轮数（默认 10）。ANY 模式下默认自动执行直到超过上限。

## 手动声明与调用

```python
from google.genai import types

function = types.FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"}
        },
        "required": ["location"],
    },
)
tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(tools=[tool]),
)

call = response.function_calls[0]
result = {"result": get_current_weather(**call.args)}
response_part = types.Part.from_function_response(name=call.name, response=result)
```

## 端到端 Agent 循环

```python
def run_agent(prompt, tools, tool_functions, max_iterations=5):
    messages = [{"role": "user", "contents": prompt}]
    for _ in range(max_iterations):
        resp = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=messages,
            config=types.GenerateContentConfig(tools=tools),
        )
        calls = resp.function_calls or []
        if not calls:
            return resp.text                      # 最终答案
        for call in calls:
            fn = tool_functions.get(call.name)
            result = fn(**call.args) if fn else "unknown tool"
            messages.append({"role": "model", "parts": [call.__original__]})
            messages.append({
                "role": "user",
                "parts": [types.FunctionResponse(name=call.name, response={"result": result})],
            })
    return resp.text                              # 到达迭代上限，优雅降级
```

三条生产性质：终止（无工具调用时结束，封顶迭代）；并行（一轮多个独立函数，并发执行按 id 映射）；组合（依赖工具链式调用）。

## MCP 支持（实验性）

Google Gen AI SDK 可把本地 MCP server 作为工具直接传入（通过 `mcp.ClientSession`、`StdioServerParameters`、`stdio_client`）。

## 并行函数调用注意事项

- 并行返回多个 `functionCall` 时，回灌的 `functionResponse` 顺序必须与之一致。
- 不要在多个轮次间交错 functionCall / functionResponse parts。
