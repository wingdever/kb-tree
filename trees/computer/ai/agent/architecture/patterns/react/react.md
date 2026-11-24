---
description: "Baseline agent loop interleaving reasoning and tool calls"
描述: "把推理与工具调用交错的基线 Agent 循环"
name: "ReAct: Reasoning and Acting"
名称: "ReAct 推理-行动"
---

# ReAct（Reason + Act）：基线模式

ReAct 让模型把简短的推理步骤与行动（工具调用）交错进行：观察结果，再重复，直到完成。这是大多数框架实现的**基线 Agent 循环**。Yao et al. 2022, arXiv:2210.03629。

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

## 为什么有效

强制模型在输出"Action"之前先生成"Thought"字符串，等于给它处理时间——把生成的文本当作草稿纸（scratchpad memory）来理清逻辑，再提交工具调用。2023 年 ReAct 论文显示，在 HotpotQA 基准上，ReAct 式方法的幻觉率约 6%，而单纯的思维链（CoT）约 14%。

关键：Observation 来自**真实工具的外部信号**。

## 问题

- **慢且贵**：复杂任务可能循环 20 次，每轮都把完整对话历史来回传递。token 成本随步数近似平方增长（每步重读此前所有轨迹）。
- **易跑偏**：工具输出过长会让模型"迷失在中间"，偏离原始目标。
- **单链承诺**：从第一步就承诺一条推理链，进入错误框架后难以廉价回溯。

这些局限正是 Plan-and-Execute、ReWOO、树搜索试图解决的问题。

## 2026 演进：ReAct + Verifier

原始 ReAct 的 2026 升级版在每步观察上加一个**显式验证器**（小模型或确定性检查）做门禁：

- **胜出场景**：工具输出可验证（能编译？通过 lint？符合 schema？）。
- **失败场景**：错误是语义层面的、只在轨迹层级可见。
- 开销通常 <10%（验证器是小模型）。

在 2026 生产系统中，ReAct 通常是底座——自修正、验证器、记忆都叠加在它之上。

## 参考资料

- ReAct: Synergizing Reasoning and Acting in Language Models（arXiv:2210.03629）：https://arxiv.org/abs/2210.03629
