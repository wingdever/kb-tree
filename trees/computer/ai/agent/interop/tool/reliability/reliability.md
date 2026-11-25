---
description: "Tool-call reliability: schema-constrained decoding, failure taxonomy, validation and bounded retry"
描述: "工具调用可靠性：约束解码、失败分类、校验与受限重试"
name: "Tool Call Reliability"
名称: "工具调用可靠性"
---

# 工具调用可靠性

工具调用不是「把 schema 发过去就行」。上线后第一类事故几乎都来自这里：参数少了一个字段、JSON 被截断、模型编了个不存在的工具、批量调用里有一个失败导致整轮重来。可靠性工程的目标不是「让模型不犯错」，而是**让每次错误都能被识别、被归类、被有限次数地修掉，并且不把错误悄悄变成脏数据**。

## 先归类，再修

同一个「工具调用失败」可能来自五个完全不同的原因，修法互不通用：

| 失败类型 | 表现 | 修法方向 |
|---|---|---|
| 选择错误 | 挑错工具、编造不存在的工具名 | 缩小工具集、按上下文动态暴露、约束解码限制工具名 |
| 格式错误 | JSON 不合法、`string` 传成 `string[]`、引号/尾逗号 | 严格模式、schema 简化、容错解析 |
| 参数值错误 | 枚举越界、负金额、日期格式错、单位错 | `enum` 与 `description` 写清、业务校验、必要时投票 |
| 截断 | 参数流到一半停了 | 调大输出预算或缩小 schema；**不要修补** |
| 拒绝 / 安全停止 | 模型拒答，没有可解析对象 | 上报或走兜底，**不要盲目重试** |

> 判断：先统计失败类型的分布，再决定投入。若 90% 的失败是截断，加 repair 库是浪费；若多数是选择错误，改 schema 无效，该缩工具集。

## 第一层：用约束解码，而不是祈祷

两种「结构化输出」的保证强度差一个数量级：

- **JSON 模式**只保证语法合法，不保证字段对——模型仍能自创键名、漏必填。
- **schema 约束解码**把采样限制在 schema 的语法内，模型物理上无法吐出违反结构的 token。

主流厂商都已提供后者：OpenAI 的 `response_format: {type:"json_schema", strict:true}`、Gemini 的 `response_schema`；Claude 的等价做法是**强制工具调用**——把目标结构定义成工具的 `input_schema`，用 `tool_choice` 指定该工具，让模型「填参数」而不是「写 JSON」。这类模型在函数调用路径上最可靠。<RichMediaReference>["https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview"]</RichMediaReference>

严格模式有代价也有坑：schema 表达能力受限（例如要求所有字段进 `required`、禁止任意额外属性），部分特性（复杂的 `oneOf`、递归）可能被拒。用严格模式前先把 schema 降级到它支持的子集，否则会得到「请求被拒」而不是「输出更好」。

## 第二层：schema 本身要适合模型填写

技术合法但不利于模型填写的 schema，是隐蔽的失败源：

- **扁平优先**。嵌套超过三层后，模型容易迷失在「我在填哪个对象」，截断概率也上升。
- **每个字段写 `description`**，并且写格式而不只是语义：`"ISO 8601 date, e.g. 2026-07-14"` 比 `"date"` 有效得多。
- **`enum` 用足**。取值范围有限就穷举，这是免费的准确率。
- **几乎全部 `required`**。可选字段会诱导模型不一致地漏填；确实可能缺的，用可空类型 + 显式 `null`，而不是从 `required` 里拿掉。
- **用判别式对象替代松散联合**。加一个 `kind: "invoice" | "receipt"` 字段在自己代码里分支，比让模型在 `oneOf` 里挑形状稳定。
- **别把 200 个工具一次塞给模型**。工具越多，选择错误率越高，这也是「按上下文动态暴露」的理由。

## 第三层：先读终止信号，再解析

解析前必须看「这次生成是怎么停的」，这个字段是免费的诊断信息：

- `finish_reason: "length"` / `stop_reason: "max_tokens"` → **截断，属于预算问题**。修法是加预算或减输出，而不是把缺的括号补上——补括号等于替模型编造它没生成的字段，把截断洗成"自信的错误数据"。
- `refusal` / 内容安全停止 → **策略问题**。原样重发通常还是拒，应该上报、走兜底或换路径。
- 正常结束 → 这时解析才有意义。

顺序颠倒了，就会把截断当成"模型返回坏 JSON"，白烧一次重试。

## 第四层：校验 + 受限重试

即使有严格模式，也要把输出当外部输入校验：

1. 用真正的 schema 库（Zod / Pydantic / Ajv）做语义校验，而不是手写 if。
2. 失败后把**校验器的错误原文**回灌：「字段 total_amount 必须为正，收到 -12」，比重新问一遍有效得多。
3. 重试上限 2–3 次，且每次记录失败原因；连续失败说明问题在输入或 schema，不在运气。
4. **失败要响**。返回空对象或默认值是最坏的处理——一张坏 PDF 会静默变成 0 元发票进数据库。
5. 校验通过还要跑业务规则：日期不能是下世纪、金额不能为负、枚举之外的值不能放过。

在生产里可以盯三个比率：首解析成功率、修复回收率（失败里被救回的比例）、语义校验通过率。首解析低于 90% 通常说明没开严格模式或 schema 太复杂，这是该先修的地方。

## 第五层：工具端也要可靠

模型侧修好，工具侧仍会失败，而且更难归因：

- **超时与重试预算**：单次工具超时要短（几秒级），整轮要有总预算，否则一个挂起的工具吃掉整次 run。
- **幂等与去重**：写操作必须能按请求键去重，否则"重试"等于"重复下单"。恢复与重试的可靠性都建立在幂等上。
- **错误分类**：把「参数错（4xx，不该重试）」「瞬时错（429/5xx/超时，可退避重试）」「权限错（应上报给人）」分开；一律重试会把限流打成雪崩。
- **结果也要校验**：工具返回的结构同样按 schema 校验，避免下游拿到半截 JSON。
- **熔断**：连续失败的工具先摘掉再排查，不要让它每轮都烧一次预算。

## 并行调用：按 id 分桶，不要按顺序拼

一轮里多个工具调用会交错流式返回。必须按 `toolCallId` 分别累积参数，参数完整后再执行；某个调用失败时，把「该调用失败」作为独立结果回给模型，而不是让整轮作废。否则并行调用越多，参数被拼错的概率越高，而且错得难以复现。

## 常见反模式

- 用正则从自由文本里"抠" JSON，再当成可靠数据。
- 解析失败就 `json_repair` 一把梭，包括截断——把编造当成修复。
- 重试没有上限，或重试时不带错误信息。
- 严格模式开着，schema 里却塞了它不支持的特性，最后退回非严格路径还以为是模型不行。
- 只测「工具能不能调通」，不测「参数错了会不会被发现」。
- 失败静默降级成空结果，监控上一切正常。

## 参考资料

- Anthropic《Tool Use》文档（强制工具调用与 `input_schema`）：https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
- OpenAI《Structured Outputs》文档（`json_schema` 与 `strict`）：https://platform.openai.com/docs/guides/structured-outputs
- Anthropic《Writing effective tools for agents》（工具设计侧的经验）：https://www.anthropic.com/engineering/writing-tools-for-agents
- MCP 规范（工具原语与 schema）：https://modelcontextprotocol.io
- json_repair（容错解析，仅用于非严格路径）：https://github.com/mangiucugna/json_repair
- Outlines（约束解码实现）：https://github.com/dottxt-ai/outlines
- XGrammar（约束解码引擎）：https://github.com/mlc-ai/xgrammar
