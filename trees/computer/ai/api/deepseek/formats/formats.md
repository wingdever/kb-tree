---
description: "DeepSeek API endpoints, model names, first call and thinking mode"
描述: "DeepSeek 的端点、模型、首个调用与思考模式"
name: "DeepSeek Endpoints and Models"
名称: "端点与模型"
---

# 端点与模型

DeepSeek API **兼容 OpenAI / Anthropic 格式**——改 base_url 即可用对应 SDK 接入。提供三种端点：

| 格式 | base_url | 说明 |
|---|---|---|
| **OpenAI Chat Completions** | `https://api.deepseek.com` | 默认，`/chat/completions` |
| **OpenAI Responses** | `https://api.deepseek.com` | `/responses`，无状态，需每轮带完整历史 |
| **Anthropic Messages** | `https://api.deepseek.com/anthropic` | `/anthropic/v1/messages` |
| **Beta** | `https://api.deepseek.com/beta` | 开启 strict 模式、8K max_tokens、FIM、Chat Prefix 等 Beta 特性 |

## 模型

| 模型名 | 说明 |
|---|---|
| `deepseek-flash` | 当前由 DeepSeek-V4.1-Flash-1017 提供服务，调用方式不变。旧名 `deepseek-v4-flash`、`deepseek-v4-flash-vision-exp` 仍接受但对应模型已退役，请求由 V4.1-Flash-1017 服务并按 Flash 价计费 |
| `deepseek-v4-pro` | 高端模型 |
| `deepseek-chat` / `deepseek-reasoner` | 已于 2026/07/24 弃用；为兼容分别对应 deepseek-v4-flash 的非思考/思考模式 |

## 首个调用（OpenAI 格式）

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "stream": false
  }'
```

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",   # 或 .../beta 开启 Beta
)
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "Hello"}],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},   # DeepSeek 扩展参数走 extra_body
)
print(response.choices[0].message.content)
```

> SDK 不原生支持的 DeepSeek 扩展参数（`thinking` 等）通过 `extra_body` 传入。

## 思考模式

- `thinking: {"type": "enabled" | "disabled"}`；`reasoning_effort` 控制思考强度。
- temperature 在思考模式固定为 1.0，在非思考模式有效（范围 0.0~2.0）。
- 思考模式下的工具调用从 DeepSeek-V3.2 起支持；继续工具调用时必须回传助手完整 content 数组（含 thinking 与 tool-use 块）。

## 一句话主线

**同一个 key、换 base_url 即可跨三种形态；扩展参数走 `extra_body`，思考模式决定 temperature 与工具回传方式。**

## 参考资料

- DeepSeek API 文档：https://api-docs.deepseek.com
