---
description: "Supervisor and manager patterns for delegating subtasks to workers"
描述: "把子任务委派给 worker 的监督者与管理模式"
name: "Orchestrator-Workers"
名称: "编排器-执行器"
---

# 编排器-执行器（Orchestrator-Workers）

这是最常用的多智能体模式：主导 Agent（监督者/编排器）协调流程，把子任务委派给专门的子 Agent（worker），每个 worker 完成后控制返回监督者，由监督者综合结果。

## 为什么是最常用

Anthropic 的研究系统是典范："主导 Agent 协调流程，同时把任务委派给并行运行的专门子 Agent"。控制集中在监督者、工作并行展开，是生产中最常见且稳健的模式。它对应的场景是：**子任务无法事先静态确定**——比如一次代码改动涉及哪些文件，编排器读了请求才知道。

## 两个变体

- **经典监督者**：主导者路由工作、收集结果。worker 作为独立 Agent 运行，返回文本结果。
- **工具调用式 / 管理者变体**：每个 worker 作为工具暴露给主导者，工具调用模型选择调用哪个。LangChain 在 2026 年推荐这个变体，因为它能更紧地控制**每个 Agent 看到什么上下文**。OpenAI Agents SDK 称为 "manager" 模式："当专家只需帮忙处理有界子任务、但不该接管面向用户的对话时使用"。

两者区别的关键在**对话所有权**：专家是否应该接管面向用户的会话？若只是后台处理有界子任务，用 manager（工具调用式）；若需要自主与用户对话，用经典 handoff。

## 层级扩展

层级（Hierarchical）把监督者变成"监督者的监督者"——团队之团队：

- LangGraph 文档："你可以通过让一个 supervisor 管理多个 supervisor 来创建多层级系统。"
- CrewAI 的 hierarchical process 自动分配 manager agent，委派任务并在继续前校验结果。
- 收益是规模——可以组合很多专家而不让一个监督者淹没在决策里；代价是每一层都让延迟与 token 成本相乘。

## 与并行化的区别

编排器-执行器与并行化（Parallelization）在拓扑上相似，关键差异在**灵活性**：

- 并行化的子任务是**预先固定**的（sectioning 分块、voting 投票）。
- 编排器-执行器的子任务**由编排器根据输入动态决定**。

因此编排器-执行器是五个模式中最贵的，planner 可能过度拆解——务必给 worker 数量和单任务预算设上限。

## 实现要点

- worker 应有隔离的角色与提示。
- 子任务结果用结构化 schema 回传，不要无格式散文。
- 编排器失败在没有重试逻辑时不可恢复——加重试与幂等。
- 给 worker 计数和预算上限，防止过度拆解烧光预算。
- 人在回路审批门可挂在监督者的综合输出之后。

