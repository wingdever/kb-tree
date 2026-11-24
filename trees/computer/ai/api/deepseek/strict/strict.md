---
description: "DeepSeek beta strict mode: enabling conditions and supported JSON Schema"
描述: "DeepSeek Beta strict 模式：启用条件与 JSON Schema 支持范围"
name: "DeepSeek Strict Mode"
名称: "严格模式"
---

# strict 模式（Beta）

> 来源：DeepSeek API 官方文档。Beta 参数与 Schema 支持范围变化快，以官方文档为准。

模型输出 Function 调用时严格遵循 JSON Schema，确保输出符合定义。思考与非思考模式均可用。

## 启用条件

1. `base_url="https://api.deepseek.com/beta"` 开启 Beta（见 `../formats/`）
2. tools 列表中**所有** function 都设 `"strict": true`
3. 服务端校验 JSON Schema，不符合规范或含不支持类型则返回错误

## 定义样例

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "strict": true,
    "description": "Get weather of a location, the user should supply a location first.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}
      },
      "required": ["location"],
      "additionalProperties": false
    }
  }
}
```

## 支持的 JSON Schema 类型

`object`、`string`、`number`、`integer`、`boolean`、`array`、`enum`、`anyOf`，以及 `$def`/`$ref`。

| 类型 | 支持的参数 / 约束 |
|---|---|
| **object** | 所有属性必须 `required`，且 `additionalProperties: false` |
| **string** | 支持 `pattern`（正则）、`format`（`email`/`hostname`/`ipv4`/`ipv6`/`uuid`）；**不支持** `minLength`/`maxLength` |
| **number/integer** | 支持 `const`、`default`、`minimum`、`maximum`、`exclusiveMinimum`、`exclusiveMaximum`、`multipleOf` |
| **array** | 支持 `items`；**不支持** `minItems`/`maxItems` |
| **enum** | 限定为若干选项之一，如 `["pending","processing","shipped","cancelled"]` |
| **anyOf** | 匹配多个 schema 之一，如账户为邮箱或 11 位手机号 |
| **$def/$ref** | 用 `$def` 定义模块、`$ref` 引用以减少重复，也支持递归结构 |

anyOf 示例：

```json
{
  "type": "object",
  "properties": {
    "account": {
      "anyOf": [
        {"type": "string", "format": "email", "description": "可以是电子邮件地址"},
        {"type": "string", "pattern": "^\\d{11}$", "description": "或11位手机号码"}
      ]
    }
  }
}
```

string 示例：

```json
{
  "type": "object",
  "properties": {
    "user_email": {"type": "string", "description": "The user's email address", "format": "email"},
    "zip_code": {"type": "string", "description": "Six digit postal code", "pattern": "^\\d{6}$"}
  }
}
```

## 一句话主线

**Beta 通道 + 全部工具 strict + 受限 Schema 子集：转换前先把 schema 按支持的类型与约束改写，否则请求直接报错。**

> 相关：基础工具调用见 `../tool-calls/`；通用 Schema 规范见 `../../common/common.md`。
