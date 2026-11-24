---
description: "DeepSeek Chat Completions tool calling: loop, tool_calls structure and mid-conversation limits"
描述: "DeepSeek Chat Completions 工具调用：循环、tool_calls 结构与中间插入限制"
name: "DeepSeek Tool Calling"
名称: "DeepSeek 工具调用"
---

# 工具调用（Chat Completions 格式，OpenAI 兼容）

> 来源：DeepSeek API 官方文档。字段与参数变化快，以官方文档为准。

## 完整示例（非思考模式）

```python
from openai import OpenAI

client = OpenAI(api_key="<your api key>", base_url="https://api.deepseek.com")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather of a location, the user should supply a location first.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"],
        },
    },
}]

messages = [{"role": "user", "content": "How's the weather in Hangzhou, Zhejiang?"}]

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        tools=tools,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return response.choices[0].message

message = send_messages(messages)
tool = message.tool_calls[0]          # id / type / function.name / function.arguments
messages.append(message)              # 助手消息（含 tool_calls）加入历史

messages.append({
    "role": "tool",
    "tool_call_id": tool.id,
    "content": "24℃",
})
message = send_messages(messages)
print(message.content)                # "The current temperature in Hangzhou is 24°C."
```

执行流程：

1. 用户问天气
2. 模型返回 `get_weather({location: 'Hangzhou'})`
3. 应用执行函数并把结果传给模型
4. 模型返回自然语言答案

> 模型本身不执行函数——`get_weather` 的具体功能由你提供。

## tool_calls 结构（OpenAI 兼容）

助手消息的 `tool_calls[]` 每项：

| 字段 | 说明 |
|---|---|
| `id` | 工具调用唯一 ID |
| `type` | `"function"` |
| `function.name` | 函数名 |
| `function.arguments` | JSON 字符串形式的参数，需 `json.loads` |

回灌：`{"role": "tool", "tool_call_id": <id>, "content": <结果字符串>}`。

## 对话中间插入工具调用

| API 格式 | 中间插入工具调用 | 中间插入 system 消息 |
|---|---|---|
| Anthropic API（`/messages`） | 支持 | 支持 |
| Responses API（`/responses`） | 支持 | 支持 |
| Chat Completions（`/chat/completions`） | **不支持** | 支持 |

> 需要在对话历史中间插入非模型生成的工具调用时，改用 Anthropic API 或 Responses API。

## 一句话主线

**标准 OpenAI 循环直接可用，扩展参数走 `extra_body`；唯一硬限制是 Chat Completions 不能在历史中间插入工具调用。**

