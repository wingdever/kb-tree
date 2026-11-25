---
description: "Baseline agent loop interleaving reasoning and tool calls: cost structure, limits, verifier variant"
描述: "把推理与工具调用交错的基线循环、成本结构、局限与验证器变体"
name: "ReAct: Reasoning and Acting"
名称: "ReAct 推理-行动"
---

# ReAct（Reason + Act）：基线模式

ReAct 让模型把简短的推理步骤与行动（工具调用）交错进行：观察结果，再重复，直到完成。这是大多数框架实现的**基线 Agent 循环**。Yao et al. 2022, arXiv:2210.03629。

几乎所有后续模式都是对它的局部改造：把"边想边做"换成"先规划再做"、把"每步重读全部历史"换成"压缩后回填"、把"单链"换成"多分支搜索"。理解它的成本结构，才知道该改哪一处。

## 循环

1. 接收目标
2. 简短推理（Thought）
3. 选择并调用工具（Action）
4. 观察工具结果（Observation）
5. 重复
6. 输出最终答案或触发停止条件

## ReAct 提示模板示例

```
Question: {user_query}
Thought: I need to find the user's billing history. I will use the SQL tool.
Action: execute_sql
Action Input: SELECT * FROM billing WHERE user_id = 123;
Observation: [后端执行 SQL 并返回结果行]
Thought: I have the billing data. Now I need to summarize it.
Final Answer: The user paid $50 last month.
```

这是论文时代的文本协议。现在多数模型支持原生工具调用（结构化参数 + 结构化结果），模板里的 `Action:` 字段已由 API 承担；**但"先写推理再提交调用"的顺序仍然有效**——它给了模型一个草稿纸。

## 为什么有效

强制模型在输出"Action"之前先生成"Thought"字符串，等于给它处理时间——把生成的文本当作草稿纸（scratchpad memory）来理清逻辑，再提交工具调用。2023 年 ReAct 论文报告，在 HotpotQA 基准上，ReAct 式方法的事实错误率明显低于纯思维链（论文给出的量级是 6% 对 14%）。

关键：Observation 来自**真实工具的外部信号**。模型的推理可以错，但工具返回值不会因为它想得漂亮而变；每轮都用外部事实纠偏一次，这是它比一次性长推理更可靠的根本原因。

## 成本结构

ReAct 的开销几乎全部来自"每步重读历史"：

- 第 n 步的输入 = 系统提示 + 目标 + 前 n−1 轮的推理与观察。步数增加，输入线性增长，累计 token 近似平方增长。
- 工具返回越长，后面每一步都替它付一次钱；一次返回 10K token，二十步就是 200K 的重复读入。
- 延迟方面，每步都要等一次完整生成 + 一次工具往返，串行叠加；步数越多，尾延迟越明显。

> 判断：优化 ReAct 的正确顺序是"减少步数 → 减少每步输入 → 减少工具返回体积"，而不是先换更快的模型。把观察压成结构化摘要，通常比换模型省得更多。

## 问题

- **慢且贵**：复杂任务可能循环 20 次，每轮都把完整对话历史来回传递。
- **易跑偏**：工具输出过长会让模型"迷失在中间"，偏离原始目标。
- **单链承诺**：从第一步就承诺一条推理链，进入错误框架后难以廉价回溯。
- **无主动收手**：模型往往不知道自己已经完成，或反复做同一动作；停止条件必须由外部设定。

这些局限指向三类改造方向：**先规划再执行**（把探索成本前移）、**压缩观察再回填**（控制每步输入）、**把单链升级为搜索**（允许回溯）。

## 何时不该用 ReAct

ReAct 是默认，但不是普适：

- **流程固定且步骤可枚举**：直接写代码编排，省掉每步的推理开销。
- **必须强一致、可审计**：每步路径必须可复现，ReAct 的随机性会让审计变难。
- **延迟极敏感**：每步一次模型+工具往返，串行十几步的等待用户能感知。
- **工具少且确定**：一次调用就能拿到全部信息时，多轮推理只是多花钱。

## 最小实现清单

一个能上线的 ReAct 循环，至少要有这六件：

1. **步数与预算上限**：`max_steps`、token 上限、墙上时间上限，三者任一触发即退出。
2. **工具参数校验**：执行前按 schema 校验，非法参数以错误信息回填，不进执行层。
3. **观察压缩**：工具结果超过阈值先摘要或截断，原文留引用。
4. **重复检测**：同一工具 + 同一参数连续出现两次，直接判为卡死并转失败路径。
5. **失败回填**：把错误分类（超时/权限/参数/空结果）后回给模型，而不是抛异常终止。
6. **轨迹记录**：每步的推理、调用、结果、耗时、token 都落盘，用于回放与评估。

## ReAct + Verifier

原始 ReAct 的常见升级是在每步观察上加一个**显式验证器**（小模型或确定性检查）做门禁：

- **胜出场景**：工具输出可验证（能编译？通过 lint？符合 schema？）。
- **失败场景**：错误是语义层面的、只在轨迹层级可见。
- 开销通常远小于一次模型调用（验证器是小模型或纯代码检查）。

在生产系统里，ReAct 通常是底座——自修正、验证器、记忆都叠加在它之上，而不是替换它。

## 一句话主线

ReAct 的可靠性来自**每一步都被外部事实纠偏一次**，代价是每步都要重付上下文；它的所有变体，本质上都是在"少付一点"和"多纠一次"之间重新分配预算。

## 参考资料

- ReAct: Synergizing Reasoning and Acting in Language Models（arXiv:2210.03629）：https://arxiv.org/abs/2210.03629
- Anthropic 工程博客《Building effective agents》：https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK 文档（工具调用与循环）：https://openai.github.io/openai-agents-python/
