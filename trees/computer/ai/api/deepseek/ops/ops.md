---
description: "DeepSeek error codes, rate limits, token usage and pricing"
描述: "DeepSeek 错误码、限流、token 用量与定价"
name: "DeepSeek Operations Reference"
名称: "运维参考"
---

# 运维参考（错误码 / 限流 / 用量 / 定价）

> 来源：DeepSeek 官方 Error Codes、Rate Limit & Isolation、Token & Token Usage、Models & Pricing 页面。价格与限制随时调整，以官方页面为准。

## 错误码

| 状态 | 原因 | 处理 |
|---|---|---|
| 400 | 请求体格式错误 | 按错误信息改格式 |
| 401 | API key 错误 | 检查或重新申请 key |
| 402 | 余额不足 ||
| 408 | 请求超时（文件上传过慢，常见于 OCR/ASR） | 检查网络并重试，遵守文件大小限制 |
| 413 | 请求体过大（文件过大） | 减小文件 |
| 422 | 参数无效 | 按错误信息改参数 |
| 429 | 触发限流（过快或超并发/QPS） | 放慢请求，见下节 |
| 500 | 服务端错误 | 稍后重试，持续则联系官方 |
| 503 | 服务端过载 | 稍后重试 |
| 504 | 网关超时（OCR、文档上传等未完成） | 重试或发更小文件 |

## 限流与隔离

- 并发按**账户**计，与用哪个 API key 无关；一个请求从发出到响应完成都算一个并发。超出返回 429。
- 当前并发上限：`deepseek-flash` 2500，`deepseek-v4-pro` 500；可申请扩容，无额外费用。
- `user_id` 用于内容安全隔离、KVCache 隔离与调度隔离。普通账户所有 `user_id` 合并计算并发；扩容账户还会按每个 `user_id` 限额（值同上）。`user_id` 建议只用 ASCII 字母、数字、`_`、`-`，UTF-8 ≤512 字节，**不要放用户隐私**。
  - OpenAI 格式放在请求体 `user_id`，SDK 走 `extra_body={"user_id": ...}`；Anthropic 格式放在 `metadata.user_id`。
- 保活：非流式请求会持续返回空行，流式请求返回 `: keep-alive` 注释；自行解析 HTTP 响应时需跳过它们。若 10 分钟内未开始推理，服务端关闭连接。

## Token 用量

- 估算：1 个英文字符 ≈0.3 token，1 个中文字符 ≈0.6 token；实际以返回的 `usage` 为准。官方提供离线 tokenizer 包，图片 token 按尺寸估算并受上限约束。
- `usage` 常用字段：`prompt_tokens`、`prompt_cache_hit_tokens`、`prompt_cache_miss_tokens`、`completion_tokens`、`reasoning_tokens`（思考 token）、`safety_tokens`（`safety_check: high` 时，已计入 completion）、`server_tool_use`（搜索/抓取次数，全为 0 时省略）。流式响应取最终 usage，不要累加中间增量。

## 定价（每 1M token，USD）

| 项目 | `deepseek-flash` 平峰 / 高峰 | `deepseek-v4-pro` 平峰 / 高峰 |
|---|---|---|
| 输入 · 缓存命中 | $0.003 / $0.006 | $0.022 / $0.044 |
| 输入 · 缓存未命中 | $0.15 / $0.30 | $0.66 / $1.32 |
| 输出 | $0.6 / $1.2 | $1.98 / $3.96 |

高峰为周一至周五 01:00–04:00 与 06:00–10:00 UTC（中国法定节假日除外），其余时间平峰，平峰价为高峰价的一半。

独立工具 API：Search 与 Fetch 各 $0.75 / 1000 次成功请求；文件解析与 OCR $0.225 / 1000 页；TTS $0.45 / 1 万字符（限时半价 $0.225）；ASR $0.116 / 小时音频（限时半价 $0.058）。服务端 Web 工具（模型内触发的搜索与抓取）目前不单独计费，结果追加到模型上下文按 token 计费。

扣费优先使用赠送余额，其次充值余额。价格可能调整，落地前核对官方定价页。

## 一句话主线

**错误码决定重试还是改参数，限流决定并发设计，`usage` 决定成本归因——把三者接进监控，才能稳定压住账单。**

