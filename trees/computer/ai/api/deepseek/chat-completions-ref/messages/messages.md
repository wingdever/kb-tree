---
description: "DeepSeek Chat Completions messages array: roles and content parts"
描述: "DeepSeek Chat Completions 的 messages 数组：角色与 content parts"
name: "Chat Messages Schema"
名称: "消息结构"
---

# messages[] 结构

> 来源：DeepSeek Chat Completions API 官方 API Reference。字段与约束变化快，以官方文档为准。

`messages` 是必填数组，至少 1 项，每项为以下角色之一：system、user、assistant、tool、latest reminder（官方 schema 列出但正文未展开该角色的字段）。各角色共有可选 `name`（`string`），用于区分同角色的参与者。

## system message

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `role` | `string` | 是 | 恒为 `system` |
| `content` | `string` | 是 | 系统消息内容 |
| `name` | `string` | 否 | 参与者名称 |

## user message

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `role` | `string` | 是 | 恒为 `user` |
| `content` | `string \| object[]` | 是 | 字符串，或 content parts 数组（用于图片/文件输入） |
| `name` | `string` | 否 | 参与者名称 |

### content parts

三种 part 以 `type` 区分：

**Text content part** — `{"type": "text", "text": "<文本>"}`，`type` 与 `text` 均必填。

**Image content part** — `type: "image_url"`，`image_url` 对象必填：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | `string` | 是 | http(s) URL（≤8192 字符）或 base64 data URL（`data:image/jpeg;base64,...`）；支持 JPEG/PNG/GIF/WebP |
| `detail` | `string` | 否 | `low` 降采样到 512×512（更快更省）；`high`/`original`/`auto` 保留原图 |

**File content part** — `type: "file"`：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file_id` | `string` | 二选一 | Files API 上传得到的文件 ID，形如 `file-api-...` |
| `file_data` | `string` | 二选一 | base64 data URL，如 `data:image/jpeg;base64,...` |
| `filename` | `string` | 否 | 仅与 `file_data` 同用时有效 |

`file_id` 与 `file_data` 必须**恰好提供一个**：都不传返回 400（`file must have a file_id or file_data`），都传返回 400（`file cannot have both file_id and file_data`）。

## assistant message

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `role` | `string` | 是 | 恒为 `assistant` |
| `content` | `string \| object[] \| null` | 是 | 消息内容 |
| `name` | `string` | 否 | 参与者名称 |
| `prefix` | `boolean` | 否（Beta） | true 时强制模型从该消息内容开始续写；需 Beta base_url，且必须是最后一条消息 |
| `reasoning_content` | `string \| null` | 否（Beta） | 思考模式下最后一条 assistant 消息的 CoT 输入，须与 `prefix: true` 同用 |

## tool message

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `role` | `string` | 是 | 恒为 `tool` |
| `content` | `string \| object[]` | 是 | 工具结果字符串，或 content parts 数组 |
| `tool_call_id` | `string` | 是 | 与助手消息 `tool_calls[].id` 匹配 |

## 常见陷阱

- 思考模式下继续工具调用，必须回传助手**完整** content 数组（含 `reasoning_content` 与 `tool_calls`）；只回传 ID 可能触发 400。
- Chat Completions 不支持在历史中间插入工具调用，需改用 Responses 或 Anthropic 格式。
- JSON 输出模式要求在 system/user 消息里明确指示模型生成 JSON。

## 一句话主线

**user/tool 的 content 可以是字符串或带 `type` 的 parts 数组；图片用 `image_url`、文件用 `file_id`/`file_data` 二选一，assistant 的 `prefix` 是 Beta 续写入口。**

