---
description: "MCP tools/list, tools/call, tool types, output schema and errors"
描述: "MCP 的工具列表、调用、数据类型、结构化输出与错误处理"
name: "MCP Tools Specification"
名称: "MCP 工具协议规范"
---

# 05 MCP Tools 协议规范

MCP 允许 server 暴露可被语言模型调用的工具。每个工具由唯一 `name` 标识，含描述 schema 的元数据。基于 JSON-RPC 2.0。请求示例省略 `_meta`（`io.modelcontextprotocol/protocolVersion`、`clientInfo`、`clientCapabilities`），**每个请求必须包含必需 `_meta` 字段**。

> 来源：Model Context Protocol 官方规范（server/tools）。协议版本持续演进，以官方规范为准。

## 能力声明

支持工具的 server **必须**声明 `tools` 能力：

```json
{
  "capabilities": {
    "tools": { "listChanged": true }
  }
}
```

`listChanged` 表示工具列表变化时是否发通知。声明了 `tools` 能力的 server **必须**响应 `tools/list` 请求返回当前可用工具集。该集合可以为空、可随时间变化，但**不得因连接而异**，也不得作为同一连接上其他请求的副作用而变化。集合**可以**按请求携带的授权而变化（如只返回调用者 scope 允许的工具），因为凭据是按请求输入而非连接状态。Server **应**以确定性顺序返回工具——这使 client 能可靠缓存工具列表，并在工具进入模型上下文时提升 LLM 提示缓存命中率。

## 协议消息

### 列出工具（tools/list）

支持分页与缓存。

请求：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": { "cursor": "optional-cursor-value" }
}
```

响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "tools": [{
      "name": "get_weather",
      "title": "Weather Information Provider",
      "description": "Get current weather information for a location",
      "inputSchema": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "City name or zip code"}
        },
        "required": ["location"]
      },
      "icons": [{"src": "https://example.com/weather-icon.png", "mimeType": "image/png", "sizes": ["48x48"]}]
    }],
    "nextCursor": "next-page-cursor",
    "ttlMs": 300000,
    "cacheScope": "public"
  }
}
```

### 调用工具（tools/call）

请求：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {"location": "New York"}
  }
}
```

响应：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "resultType": "complete",
    "content": [{
      "type": "text",
      "text": "Current weather in New York:\nTemperature: 72°F\nConditions: Partly cloudy"
    }],
    "isError": false
  }
}
```

### 需要输入的响应（InputRequiredResult / elicitation）

Server 可返回 `resultType: "input_required"` 表示需要先补充输入。请求携带 `inputResponses` 和（若 server 提供）`requestState`：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "github_login": {
        "method": "elicitation/create",
        "params": {
          "mode": "form",
          "message": "Please provide your GitHub username",
          "requestedSchema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
          }
        }
      }
    },
    "requestState": "eyJsb2NhdGlvbiI6Ik5ldyBZb3JrIn0..."
  }
}
```

重试时（**JSON-RPC id 必须与初次不同**）：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {"location": "New York"},
    "inputResponses": {
      "github_login": {"action": "accept", "content": {"name": "octocat"}}
    },
    "requestState": "eyJsb2NhdGlvbiI6Ik5ldyBZb3JrIn0..."
  }
}
```

### 列表变化通知

声明 `listChanged` 的 server 应向打开了 `subscriptions/listen` 流且 `toolsListChanged: true` 的 client 发送：

```json
{"jsonrpc": "2.0", "method": "notifications/tools/list_changed"}
```

## Tool 数据类型

| 字段 | 说明 |
|---|---|
| `name` | 工具唯一标识 |
| `title` | 可选，展示用人类可读名 |
| `description` | 功能的人类可读描述 |
| `icons` | 可选，UI 展示图标数组 |
| `inputSchema` | JSON Schema 定义预期参数；无 `$schema` 时默认 2020-12；**必须是合法 JSON Schema 对象（非 null）** |
| `outputSchema` | 可选，输出的 JSON Schema |
| `annotations` | 可选，描述工具行为属性 |

**无参数工具**的合法写法：

- `{"type":"object","additionalProperties":false}` —— 推荐，显式只接受空对象
- `{"type":"object"}` —— 接受任何对象（含带属性的）

### x-mcp-header 注解

inputSchema 的属性可带 `x-mcp-header`，把参数值暴露为 HTTP header。使用 Streamable HTTP 传输的 client **必须**拒绝违反约束的 x-mcp-header 工具定义（排除出 tools/list 结果并记警告，而非让单个畸形工具阻断其他工具）；其他传输（stdio）可完全忽略。

```json
{
  "name": "execute_sql",
  "description": "Execute SQL on Google Cloud Spanner",
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": {"type": "string", "description": "The region", "x-mcp-header": "Region"},
      "query": {"type": "string", "description": "The SQL query"}
    },
    "required": ["region", "query"]
  }
}
```

调用传 `"region": "us-west1"` 时，client 加 header `Mcp-Param-Region: us-west1`。**不要用 x-mcp-header 标记敏感参数**（密码、API key、token、PII）——header 值对网络中间人可见。

## Tool Result 数据类型

结果可含结构化或非结构化内容。

**非结构化内容**在 `content` 字段，可含多个不同类型项（text、image、audio、resource link、embedded resource），均支持可选 annotations（audience、priority、lastModified）。

资源链接：

```json
{
  "type": "resource_link",
  "uri": "file:///project/src/main.rs",
  "name": "main.rs",
  "description": "Primary application entry point",
  "mimeType": "text/x-rust"
}
```

嵌入资源：

```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///project/src/main.rs",
    "mimeType": "text/x-rust",
    "text": "fn main() {\n    println!(\"Hello world!\");\n}"
  },
  "annotations": {"audience": ["user", "assistant"], "priority": 0.7, "lastModified": "2025-05-03T14:30:00Z"}
}
```

**结构化内容**在 `structuredContent` 字段，为符合 `outputSchema` 的任意 JSON 值。为向后兼容，返回结构化内容的工具**也应**在 TextContent block 中返回序列化 JSON。注意：`structuredContent` 是 server 产生的结果数据，与 LLM"结构化输出"（schema 约束的模型生成）无关。

提供 outputSchema 时：

- Server **必须**提供符合 schema 的结构化结果
- Client **应**按 schema 校验结构化结果

```json
{
  "name": "get_weather_data",
  "description": "Get current weather data for a location",
  "inputSchema": {
    "type": "object",
    "properties": {"location": {"type": "string"}},
    "required": ["location"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": {"type": "number", "description": "Temperature in celsius"},
      "conditions": {"type": "string"},
      "humidity": {"type": "number"}
    },
    "required": ["temperature", "conditions", "humidity"]
  }
}
```

合法响应：

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "resultType": "complete",
    "content": [{
      "type": "text",
      "text": "{\"temperature\": 22.5, \"conditions\": \"Partly cloudy\", \"humidity\": 65}"
    }],
    "structuredContent": {"temperature": 22.5, "conditions": "Partly cloudy", "humidity": 65}
  }
}
```

## 错误处理（两套机制）

1. **协议错误**（请求结构问题，模型较难修复）：未知工具、格式错误、server 错误。标准 JSON-RPC error：

```json
{"jsonrpc": "2.0", "id": 3, "error": {"code": -32602, "message": "Unknown tool: invalid_tool_name"}}
```

2. **工具执行错误**（含可操作反馈，模型可自我纠正重试）：API 失败、输入校验错误、业务逻辑错误。在结果中用 `isError: true`：

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "resultType": "complete",
    "content": [{
      "type": "text",
      "text": "Invalid departure date: must be in the future. Current date is 08/08/2025."
    }],
    "isError": true
  }
}
```

Client **应**把工具执行错误提供给语言模型以启用自我纠正；协议错误可以提供但模型较难成功恢复。

## 安全

Client **必须**把工具注解视为不可信，除非来自可信 server。
