---
description: "DeepSeek Lists Models API and the model metadata it exposes"
描述: "DeepSeek 模型列表接口及其返回的模型能力元数据"
name: "DeepSeek Models API"
名称: "模型 API"
---

# 模型 API（Lists Models）

> 来源：DeepSeek Lists Models 官方 API Reference。模型能力与规格变化快，以官方文档为准。

`GET https://api.deepseek.com/models` 列出当前可用模型。响应 `object: list`，`data[]` 每项是一个 model object。

## model object

- `id`：模型标识符，可直接用于其他 API 的 `model` 字段。
- `object`：恒为 `model`；`owned_by`：所属组织。
- `name`：展示名，用于模型选择器。
- `context_window`：上下文窗口总 token 容量（含输入与输出）。
- `max_output_tokens`：单次响应允许的最大输出 token，即 `max_tokens` 的上限。
- `input_modalities` / `output_modalities`：取值为 `text`、`image` 等；字段可能缺省。
- `effort`：`supported_levels`（思考模式下 `reasoning_effort` 可用档位，不含关闭思考的 `none`）与 `default_level`（未指定时的默认档位）。
- `api_capabilities.anthropic_messages.system_prompt_update`：取 `leading-only`（只有会话开头那条 system 生效）或 `in-history`（历史中最新 system 消息为完整有效系统提示，覆盖之前所有）。

## 为什么用接口而不是写死

模型版本、上下文窗口、模态与按协议开放的能力都会变。当前 `deepseek-flash` 由 DeepSeek-V4.1-Flash-1017 提供服务、`deepseek-v4-pro` 为 V4-Pro-0813，但应用应在启动时拉一次 `/models`，用返回的 `id`、`context_window`、`max_output_tokens`、`effort.supported_levels` 驱动 UI 与参数校验，而不是硬编码。

## 一句话主线

**`/models` 是模型能力的机器可读真相源：ID、上下文、输出上限、思考档位、按协议差异都从这里取。**

