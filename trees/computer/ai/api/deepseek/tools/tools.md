---
description: "DeepSeek standalone tool APIs: search, fetch, OCR, speech to text and text to speech"
描述: "DeepSeek 独立工具 API：搜索、抓取、OCR、语音识别与语音合成"
name: "DeepSeek Tool APIs"
名称: "工具 API"
---

# 工具 API（Search / Fetch / OCR / ASR / TTS）

> 来源：DeepSeek Search、Fetch、OCR、Speech to Text、Text to Speech 官方 API Reference 与指南。限制与计费变化快，以官方文档为准。

这些是可独立调用的能力，不走 `/chat/completions`；也能作为服务端工具在对话中启用（见 `../anthropic/`）。

| API | 端点 | 用途 | 计费方式 |
|---|---|---|---|
| Search | `POST /v1/tools/search` | 联网搜索，返回结构化结果 | 按成功请求计费 |
| Fetch | `POST /v1/tools/fetch` | 抓取网页并返回 Markdown | 按成功请求计费 |
| OCR | `POST /v1/tools/ocr` | 文档/图片逐页识别文字 | 按页计费 |
| Speech to Text | `POST /v1/tools/asr` | 音频转文字 | 按音频时长计费 |
| Text to Speech | `POST /v1/tools/tts` | 文字转语音，流式返回 | 按字符计费 |

具体价格见 `../ops/`。

## Search

请求体：`query`（1~128 字符，支持 `site:`、`-site:`、引号短语）、`count`（1~50，默认 10）、`ori_question`（触发搜索的原始问题，1~128 字符）、`localization`（IP，用于结果本地化）、`need_content`（是否在 `content` 返回正文，默认 false）。

响应 `results[]`：`rerank_score`（0~3，≥1.5 视为高质量）、`title`、`url`、`snippet`（100~200 字，供 UI 展示）、`summary`（600~800 字，供模型阅读）、`content`、`site_name`、`site_icon`、`date`（RFC 3339 UTC）、`authority`（0~4，-1 未知，≥3 为高权威）。

## Fetch

请求体 `url`（≤8192 字符，必须带 host 的 http(s) URL，不能含用户名密码）。响应 `title`、`content`（Markdown 正文）。

## OCR

`multipart/form-data`：`file`（带文件名）、`purpose` 取 `text_recognition`（Word/PowerPoint 直接抽文本，其他文件逐页识别）或 `rich_layout_recognition`（所有文件逐页识别）。

响应 `object: ocr.result`：`id`（`ocr-...`）、`page_count`、`pages[].index/text/finish_reason`（`stop` 完整、`length` 超长被截断）。`usage` 仅供参考，**不用于计费**。OCR 上传的文件不进入 Files API（见 `../files/`）。

## Speech to Text（ASR）

`multipart/form-data`：`file` 为 16 位 PCM WAV 或 Ogg Opus，整段音频一次上传。响应 `request_id`、`text`、`duration_ms`。文件限制见官方指南；常见错误 400/408/413/504 见 `../ops/`。

## Text to Speech（TTS）

请求体：`text`（非空）、`voice_id`（`stella` 女声 / `tide` 男声，默认 stella）、`format`（`wav` 或 `pcm`，默认 wav）、`filter_markdown`（默认 true，朗读前去除 Markdown 格式）。

HTTP 响应体直接流式输出音频：wav 为 `audio/wav`，pcm 为 24 kHz、16 位有符号单声道裸流 `audio/pcm`。若需边生成边发送文本，改用 WebSocket `wss://api.deepseek.com/v1/tools/tts`。

## 一句话主线

**五个独立端点各管一种能力：Search/Fetch 补信息，OCR/ASR/TTS 处理文件与语音；按次、按页、按时长、按字符分别计费。**

> 相关：对话内服务端 Web 工具见 `../anthropic/`；文件生命周期见 `../files/`；错误与限流见 `../ops/`。
