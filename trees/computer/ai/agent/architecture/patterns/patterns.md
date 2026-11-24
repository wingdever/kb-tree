---
description: "Vocabulary of core agent architectures and design patterns"
描述: "Agent 核心架构与设计模式的词汇表导航"
name: "Core Architectures and Design Patterns"
名称: "核心架构与设计模式"
---

# 核心架构与设计模式

这一章是 Agent 设计的"词汇表"。少数几种模式覆盖了绝大多数真实系统，不必发明新架构。本目录把每种模式拆成独立子知识点。

## 两条主线

**循环与规划**：`ReAct`（交错推理行动）→ `Plan-and-Execute`（先规划后执行）→ `ReWOO`（规划与观察彻底解耦）→ `树搜索`（多路径探索与回溯）。

**组合与质量**：`Anthropic工作流模式`（五种可组合的工作流 + 自主 Agent）→ `状态机与DAG`（用显式图管关键控制流）→ `ACI与三原则`（工具与简洁性）→ `自我修正族`（让输出更可靠）。

## 一句话主线

从最简单的 ReAct 循环起步，按任务需要用 Plan-and-Execute / ReWOO 降本、用 Anthropic 的工作流模式组合，关键处用状态机接管控制流，用 ACI 原则设计工具，用自我修正与树搜索提质——但始终"先建评估器，再加复杂度"。
