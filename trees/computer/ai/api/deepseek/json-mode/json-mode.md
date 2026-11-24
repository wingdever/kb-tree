---
description: "DeepSeek JSON Output: response_format json_object, prompt requirements and failure behavior"
描述: "DeepSeek JSON 输出：response_format、提示词要求与失败行为"
name: "DeepSeek JSON Output"
名称: "JSON 输出"
---

# JSON 输出（JSON Output）

> 来源：DeepSeek JSON Output 官方指南。参数与失败行为变化快，以官方文档为准。

JSON Output 保证模型输出合法 JSON 字符串，便于结构化解析。它是 `response_format` 的一个取值。

## 启用条件

1. 设 `response_format: {"type": "json_object"}`。
2. 在 system 或 user prompt 中**包含 `json` 字样**，并**给出期望 JSON 格式的示例**来引导模型。
3. 合理设置 `max_tokens`，避免 JSON 字符串被中途截断。

> 只设 `response_format` 而不在提示词里提 JSON 或不给示例，模型可能不按预期格式输出。

## 失败行为

若模型输出无法被识别为 JSON，API 会把**非 JSON 内容替换为空格（`U+0020`）**。因此 `content` 可能只剩空格、看起来为空，但 `finish_reason` 仍可能是 `stop`。

应对：修改 prompt 强化格式约束；在代码里处理空 `content`（如重试请求）。若 `finish_reason: length`，表示输出超过 `max_tokens` 或对话超过最大上下文长度，JSON 可能被部分截断。

## 完整示例

```python
import json
from openai import OpenAI

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format.

EXAMPLE INPUT:
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    response_format={"type": "json_object"},
)

print(json.loads(response.choices[0].message.content))
```

输出：

```json
{
  "question": "Which is the longest river in the world?",
  "answer": "The Nile River"
}
```

## 一句话主线

**`response_format: json_object` + 提示词里写明 JSON 并给示例 + 足够的 `max_tokens`；解析前处理空 `content`，别把 `stop` 当成格式一定正确。**

