---
description: "Universal function-calling flow, field mapping and JSON Schema rules"
描述: "函数调用通用流程、字段对照与 JSON Schema 规范"
name: "Common Tool-Calling Specification"
名称: "工具调用通用规范"
---

# 01 工具调用通用规范

## 一句话本质

**模型从不运行你的代码。** 它收到一份函数声明（名称、参数、用途描述），返回一个结构化请求——调用哪个函数、传什么参数。你的应用负责执行，把结果回灌给模型。

- **声明（declaration）**：你给模型的工具定义。
- **工具调用（tool call）**：模型返回的结构化请求。
- **工具输出（tool output）**：你执行后返回的结果，须引用具体的 call id。

> 声明决定模型会怎样调用。描述模糊 → 参数模糊。把描述当成"在给一个细心的助手解释这个工具"来写。

## 六步循环（所有厂商通用）

1. 定义一份工具列表（函数 + JSON Schema 参数）随请求发给模型。
2. 模型决定调用零个、一个或多个工具，返回工具调用请求（含参数）。
3. 你的代码解析参数、**校验**、执行对应函数。
4. 把工具输出（带 call id）作为新消息回灌。
5. 再次请求模型，得到最终答案或更多工具调用。
6. 重复直到模型不再请求工具，或触发停止条件（迭代/token/时间上限）。

三条生产性质：

- **终止性**：循环在"响应没有工具调用"时结束。若不收敛，必须封顶迭代，否则卡住的 Agent 会永远烧 token。
- **并行性**：模型可在一轮请求多个独立函数；并发执行，按 id 映射结果。
- **组合性**：有依赖的工具链式调用——先 `get_location()`，再 `get_weather(location)`。

## 工具定义规范（JSON Schema）

一个工具定义通常包含：

| 字段 | 要求 |
|---|---|
| `name` | 唯一标识符。通用约束：`^[a-zA-Z0-9_-]+$`，长度 ≤64。多数厂商建议/要求 snake_case，含空格或特殊字符常被拒绝。 |
| `description` | 说清工具做什么、何时用/何时不用、返回什么。这是模型选工具的主要依据。 |
| `parameters` / `inputSchema` | JSON Schema 对象，描述参数。必填项用 `required` 列出。 |
| `strict`（部分厂商） | 是否强制模型严格按 schema 生成参数。 |

### Schema 编写规范

- 每个参数都要有清晰 `description` 和 `type`。
- 区分必填与可选：`required` 数组。
- 枚举用 `enum`，限定取值范围。
- 对象用 `type: "object"` + `properties`；数组用 `type: "array"` + `items`。
- **严格模式**（OpenAI 风格）额外要求：
  - 每个 object 必须 `additionalProperties: false`
  - `properties` 中所有字段都必须列入 `required`
  - 可选字段通过 type 里加 `"null"` 表示（如 `"type": ["string", "null"]`）
- 无参数工具的合法写法：`{"type":"object","additionalProperties":false}`（推荐）或 `{"type":"object"}`。

### 工具设计即 ACI（Agent-Computer Interface）

- **少而精**：给出任务所需的最小工具集。两个工具可能做同一件事时，模型会选错。
- **描述三要素**：做什么、何时用、返回什么。把参数名和描述当给初级开发者的 docstring 写。
- **校验输入输出**：绝不把模型生成的参数直接传入破坏性操作；做 schema 校验、范围检查、清洗。
- **可推理的错误**：返回"未找到该 ID 的客户"这类模型能理解的错误，而非原始堆栈。
- **危险动作门禁**：转账、删除、对外发送需要显式确认或人工批准。
- **格式选择**：让格式贴近模型在文本中自然见过的样子；给模型足够 token 先"思考"；避免让它做精确行数统计或字符串转义。
- **防错（poka-yoke）**：改参数设计让错误更难发生——如把相对路径改为强制绝对路径。

## 回灌工具结果的通用规则

- 每条工具调用都必须有**对应的结果**，用 call id 关联。LangGraph 的 ToolNode 会强制这一点，缺失则抛 `ValueError`。
- 并行调用的结果可以按任意顺序返回（id 用于正确匹配），但 Gemini 要求 `FunctionResponse` 的 parts **顺序与 `functionCall` 完全一致**，且 `name` 对应。
- 推理模型（如带 thinking 的）返回的推理项/签名 often 需要原样回传——Gemini 的 `thought_signature`、OpenAI reasoning items 都必须带回，否则多步工具使用会丢上下文。

## 流式工具调用

流式时，工具调用的参数以增量 delta 分片到达（OpenAI `delta.tool_calls`，Gemini `step.delta`）。**必须先聚合分片、重建完整参数，再执行**——未能重建部分参数是流式 Agent 循环的经典 bug。

## 控制模式对照

| 需求 | OpenAI `tool_choice` | Anthropic `tool_choice` | Gemini `mode` |
|---|---|---|---|
| 模型自行决定（默认） | `"auto"` | `{"type":"auto"}` | `AUTO` |
| 禁止工具调用 | `"none"` | —（不传 tools） | `NONE` |
| 至少调用一个 | `"required"` | `{"type":"any"}` | `ANY` |
| 强制特定函数 | `{"type":"function","name":...}` | `{"type":"tool","name":...}` | `ANY` + `allowed_function_names` |
| 限制可选子集 | `allowed_tools` 参数 | — | `allowed_function_names` |

## 安全规范（跨厂商）

- 把工具返回的任何数据视为**不可信**（工具描述投毒、资源提示注入）。
- 最小权限：短期、窄 scope 凭据；密钥不进提示词/日志。
- 打破"致命三要素"：私有数据 + 不可信内容 + 对外通道三者不能同时具备。
- 出口白名单 + 出口监控；高风险动作人工审批。
- 用普通代码（确定性护栏）授权每次工具调用，而非指望模型自觉。
