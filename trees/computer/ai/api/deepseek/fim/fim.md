---
description: "DeepSeek FIM completion and chat prefix completion beta APIs"
描述: "DeepSeek 的 FIM 补全与 Chat Prefix 续写 Beta 接口"
name: "FIM and Chat Prefix"
名称: "FIM 与 Chat Prefix"
---

# FIM 与 Chat Prefix

> 来源：DeepSeek FIM Completion / Chat Prefix Completion 官方指南与 API Reference。Beta 形态变化快，以官方文档为准。

两者都是 Beta 特性，都需要 `base_url="https://api.deepseek.com/beta"`，但走**不同端点**：

| 特性 | 端点 | 输入方式 |
|---|---|---|
| FIM Completion | `POST /completions` | `prompt` + `suffix`，生成夹在中间的文本 |
| Chat Prefix Completion | `POST /chat/completions` | 最后一条 assistant 消息设 `prefix: true`，续写该消息 |

## FIM Completion API（Beta）

- 仅**非思考模式**支持。
- `prompt` 必填，为要补全的前缀；`suffix` 可选，为补全之后的后缀。
- 常用参数：`max_tokens`、`stop`（最多 16 个，每个非空且 ≤512 字节）、`temperature`（0~2）、`top_p`、`stream`、`stream_options.include_usage`、`logprobs`（0~20）、`echo`（回显 prompt，不能与 `suffix`/`logprobs` 同用）。
- `frequency_penalty`、`presence_penalty` 已废弃，传入不生效。

```json
{
  "model": "deepseek-flash",
  "prompt": "def add(a, b):\n    ",
  "suffix": "\n    return result",
  "max_tokens": 64
}
```

响应 `object` 为 `text_completion`；`choices[].finish_reason` 可能为 `stop`/`length`/`content_filter`/`insufficient_system_resource`/`aborted`。`usage` 含 `prompt_tokens`、`prompt_cache_hit_tokens`、`prompt_cache_miss_tokens`、`completion_tokens`、`reasoning_tokens`，启用 `safety_check: high` 时另有 `safety_tokens`（已计入 completion）。

流式以 `data: [DONE]` 结束；设置 `stream_options.include_usage: true` 时，最后一个内容块携带整次请求的 usage。

## Chat Prefix Completion（Beta）

- 走标准 Chat Completions；`messages` 的**最后一条必须是 `assistant`**，且设 `"prefix": true`。
- 下面的例子用 ```` ```python\n ```` 作为 assistant 前缀强制输出 Python 代码，并用 `stop` 阻止模型继续解释：

```python
from openai import OpenAI

client = OpenAI(api_key="<your api key>", base_url="https://api.deepseek.com/beta")

messages = [
    {"role": "user", "content": "Please write quick sort code"},
    {"role": "assistant", "content": "```python\n", "prefix": True},
]
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    stop=["```"],
)
print(response.choices[0].message.content)
```

- 思考模式下，最后一条 assistant 消息还可用 `reasoning_content` 传入 CoT 作为续写输入，须与 `prefix: true` 同用。
- 使用 Web 工具或内容安全时的续写有额外约定，见官方文档的 Web Tools - Continue Generation。

## 怎么选

- 已有后文、要补中间空洞 → FIM（`POST /completions`，仅非思考模式）。
- 已写好开头、要让模型接着写 → Chat Prefix（assistant `prefix: true`）。
- 普通问答与续写 → 标准 Chat Completions。

## 一句话主线

**FIM 用 `prompt` + `suffix` 补中间，Chat Prefix 用 `prefix: true` 续写开头；两者都要 `/beta`，别再把 FIM 写成 chat 消息角色。**

