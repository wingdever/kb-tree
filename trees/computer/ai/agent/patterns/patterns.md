---
description: "Vocabulary of core agent architectures and design patterns"
描述: "Agent 核心架构与设计模式的词汇表导航"
name: "Core Architectures and Design Patterns"
名称: "核心架构与设计模式"
---

# 核心架构与设计模式

这一章是 Agent 设计的"词汇表"。少数几种模式覆盖了绝大多数真实系统，不必发明新架构。本目录把每种模式拆成独立子知识点。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `react/` | 基线循环、提示模板、为什么有效、问题、ReAct + Verifier 演进 |
| `plan-exec/` | 规划器/执行器分离、优势局限、规划税、与 ReWOO/编排器的关系 |
| `anthropic/` | 5 + 1 模式：提示链/路由/并行化/编排器-执行器/评估器-优化器/自主智能体 |
| `stategraph/` | 显式状态图、人工审批节点、reducer、检查点、条件边、interrupt |
| `aci/` | 简单/透明/ACI 三原则、工具格式、poka-yoke、框架取舍 |
| `self-correct/` | Reflexion / Self-Refine / CRITIC、错误信号来源、Detect-then-Patch |
| `rewoo/` | 无观察推理、三角色、占位变量 DAG、token 节省与适应性权衡 |
| `tree-search/` | ToT / GoT / MCTS / LATS、 evaluator 前提、成本与适用 |

## 两条主线

**循环与规划**：`ReAct`（交错推理行动）→ `Plan-and-Execute`（先规划后执行）→ `ReWOO`（规划与观察彻底解耦）→ `树搜索`（多路径探索与回溯）。

**组合与质量**：`Anthropic工作流模式`（五种可组合的工作流 + 自主 Agent）→ `状态机与DAG`（用显式图管关键控制流）→ `ACI与三原则`（工具与简洁性）→ `自我修正族`（让输出更可靠）。

## 一句话主线

从最简单的 ReAct 循环起步，按任务需要用 Plan-and-Execute / ReWOO 降本、用 Anthropic 的工作流模式组合，关键处用状态机接管控制流，用 ACI 原则设计工具，用自我修正与树搜索提质——但始终"先建评估器，再加复杂度"。
