---
description: "Prompt engineering for agents: CoT, self-consistency, structured output, caching and eval-driven iteration"
描述: "Agent 提示词工程：思维链、自洽性、结构化输出、缓存与评估驱动迭代"
name: "Prompt Engineering"
名称: "提示词工程"
---

# Prompt 提示词工程

提示词工程已从"写 clever 提示"演化为一门软件工程学科——把提示词当代码：结构化格式、版本控制、测试、监控。对 Agent 而言，提示词是 harness 的一部分，但**很多事情不能靠提示词解决**（如 PII、合规），那些要靠中间件/护栏（见 `../hooks/`）。

## 推理技巧

- **思维链（CoT）**：让模型逐步推理再回答。zero-shot（"Let's think step by step"）或 few-shot（展示推理过程）。在多步算术、逻辑、规划上提升 10–40%；**在简单查找任务上反而有害**（引入推理错误机会）。
- **自洽性（Self-Consistency）**：高温采样多条推理链，对最终答案多数决。GSM8K 比单样本 CoT 高 17.9 分；代价是 N 倍 token。适合高风险、准确性优先于吞吐的任务。
- **思维树（ToT）**：多路径探索 + 评估剪枝，见 `../patterns/tree-search/`。
- **ReAct**：推理与工具调用交错，见 `../patterns/react/`。
- **宪法式 AI（Constitutional AI）**：定义原则 → 让模型批评自己的输出是否违反 → 修订。

> 重要：**扩展思考模型**（o 系列、Claude extended thinking、Gemini thinking）原生做逐步推理，别再加"think step by step"（冗余开销无收益）——用 `reasoning_effort` 等 API 参数控制思考深度。

## 系统提示结构

- **保持精炼**：150–300 词。超过 3000 token 注意力稀释；只在出现具体失败模式时加规则。
- **注意边界**：注意力在上下文首尾最强——核心指令与静态规则放开头，动态数据放中间，关键执行指令放末尾。
- **四块结构**：角色/目标 → 约束 → 上下文/数据 → 任务指令（末尾）。
- **正面表述优于否定**："别用要点 jargon" 让模型先处理被禁概念（粉红大象问题）→ 改写成"用连续段落、清晰易懂的术语"。
- **XML 标签分隔**：用 `<context>`、`<rules>` 等显式分隔组件，防注入、防上下文串味、帮模型解析动态载荷。OWASP LLM Top 10 把提示注入列为 #1 风险。

## 结构化输出

不要靠"返回 JSON"的自然语言请求——那 10–20% 的时候会失败并破坏下游解析器。做法：用 Pydantic/Zod 定义精确 schema，再用 provider 的 structured output API（OpenAI response_format + JSON schema、Anthropic tool definition）。**JSON mode 只保证语法有效，strict structured output 才约束形状**；两者都不证明提取值真实，要对源数据校验。

## 提示缓存

把静态前缀（人格、业务规则、固定 schema、长 few-shot 示例）放前面，动态内容放后面。Anthropic 缓存 token 收正常输入价的 10%（省 90%），OpenAI 收 50%（省 50%）。对大文档 + 多次调用（仅用户输入变化）价值最大。

## 工程实践

- **提示版本控制**：存 Git，语义化版本（major=格式破坏、minor=新特性、patch=措辞），带元数据（model/temperature/max_tokens），维护 changelog。
- **A/B 测试**：明确成功指标，流量均分，每变体 500+ 样本达统计显著。
- **评估驱动**：建 50–100 条代表性输入的 golden set + ground truth，每次提示改动跑自动回归（LLM-as-judge 或规则）。Stage 2→3（加质量指标与 A/B）是投入回报最大的跃迁；Stage 4（DSPy 自动优化）需要稳定评估标准 + 50+ 标注样例 + 高量重复。
- **错误处理**：指数退避重试、输出对 schema 校验后拒绝重试、fallback 提示、失败日志、监控提示漂移。

## 技术选择七问

1. 任务有单一可验证正确答案？→ Self-Consistency。
2. 涉及空间关系/逻辑依赖？→ Chain-of-Symbol。
3. 生产运行 >500 次？→ 投资 DSPy 编译。
4. 成本是硬约束？→ 低 reasoning effort + zero-shot。
5. 需探索多解路径？→ ToT（收益抵得上成本时）。
6. 给便宜模型生成提示？→ 用前沿模型 Meta-Prompting。
7. 输出格式不稳定？→ 加显式 schema + 角色约束。

> 相关：工具格式规范见 `../../api/common/`；中间件与提示裁剪见 `../hooks/`；推理模式见 `../patterns/`；评估见 `../eval/`。
