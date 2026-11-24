---
description: "DeepSeek Files API: upload, list, retrieve and delete files"
描述: "DeepSeek 文件 API：上传、列表、获取与删除"
name: "DeepSeek Files API"
名称: "文件 API"
---

# 文件 API（Files）

> 来源：DeepSeek Files API 官方 API Reference 与指南。字段与有效期规则变化快，以官方文档为准。

四个端点共用同一个 **file object**：

| 操作 | 端点 | 说明 |
|---|---|---|
| Upload File | `POST /files` | 上传图片或文档 |
| List Files | `GET /files` | 游标分页列出文件 |
| Retrieve File | `GET /files/:file_id` | 获取单个文件信息 |
| Delete File | `DELETE /files/:file_id` | 删除文件 |

## file object

`id`（形如 `file-api-...`，可在 Chat Completions 中引用）、`object`（恒为 `file`）、`bytes`、`created_at`（Unix 秒）、`filename`、`purpose`、`expires_at`（仅设置有效期时返回）。

`purpose` 三种：`user_data`（图片，供对话引用）、`text_recognition`、`rich_layout_recognition`（后两者用于文档解析）。`expires_at` 由上传时的 `expires_after[anchor]`（只能为 `created_at`）与 `expires_after[seconds]`（3600~2592000，即 1 小时~30 天）决定；两者必须成对出现，省略则永久保留。

## Upload File

`multipart/form-data`。图片支持 JPEG/PNG/GIF/WebP，格式从内容检测；上传文档时 `purpose` 必须放在 `file` 字段**之前**。文档只有解析成功后才出现在 List Files 里（解析见官方文档 File Parsing 指南）。OCR 识别走 `../tools/` 的独立端点，不把文件存入 Files API。

## List Files

查询参数：`after`（游标 file_id）、`limit`（1~1000，默认 1000）、`order`（`asc`/`desc`，默认 asc）、`purpose`（按用途过滤）。响应含 `data[]`、`first_id`、`last_id`、`has_more`，用首尾 id 做下一页游标。

## Retrieve / Delete

`GET /files/:file_id` 返回 file object；`DELETE /files/:file_id` 返回 `id`、`object`、`deleted`。

## 一句话主线

**上传拿 `file-api-...` id、在 Chat Completions 里用 `file_id` 引用；列表靠 `after` 游标翻页，有效期在上传时一次性设定。**

> 相关：图片输入与 Vision 见 `../formats/`；文档解析计费见 `../ops/`；对话中的文件引用见 `../tool-calls/`。
