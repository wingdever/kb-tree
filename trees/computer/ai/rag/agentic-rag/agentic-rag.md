---
description: "Agentic RAG: from linear pipeline to autonomous reasoning loop—patterns, self-correction and retrieval-as-tool"
描述: "Agentic RAG：从线性管道到自主推理循环——模式、自检与检索即工具"
name: "Agentic RAG"
名称: "Agentic RAG"
---

# Agentic RAG：让检索本身变得自主

"RAG 已死"的标题很偷懒——检索没死，它长大了，被吸收进更广的学科（上下文工程），并停止假装自己就是整个架构。

Agentic RAG 的核心：**用推理循环取代直线管道**。传统 RAG 只跑一次"检索→生成"；Agentic RAG 让 Agent 决定是否需要检索、检索什么、几轮、何时停止。一个典型循环：评估问题 → 规划与路由 → 检索 → 评估结果 → 改写/换源/再检索 → 生成带引用的答案。循环是重点——它能解决单次管道无法解决的问题，但也更慢更贵，所以需封顶迭代（通常 5–6 轮）并在触限时干净降级。

本主题已拆成 3 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `patterns/` | 核心模式：Router、ReAct、Plan-and-Execute、Multi-hop、Self-RAG、CRAG、Adaptive；single vs multi-agent |
| `self-correcting/` | 自检三机制深度对比：Self-RAG 反射 token、CRAG 检索评估三分支、Adaptive 复杂度路由 |
| `retrieval-as-tool/` | 架构转变：检索即工具、迭代循环的成本延迟、工程投入转移 |

## 一句话主线

先用 `patterns/` 选一个与问题复杂度匹配的架构（默认单 Agent Router）；当检索质量不稳时叠 `self-correcting/` 的自检循环；根本上是把检索从"确定性预处理"变成 `retrieval-as-tool/` 描述的"Agent 可调用决策"。记住：**Agentic RAG 是关系复杂场景的增强，不是 RAG 的替代**——成本 3–10×、延迟从 1–2s 升到 4–15s，需要先做 Adaptive 路由让简单查询走快路。

## 与兄弟目录的分工

- 检索/重排/融合算法见 `../retrieval/`；查询改写见 `../query-transform/`；切块见 `../chunking/`。
- 图检索见 `../graphrag/`；多模态检索见 `../multimodal-rag/`；评估见 `../eval/`；生产护栏见 `../prod/`。
- 关键提醒：上述前提都假设底层数据干净、最新、治理良好——自检循环救不了陈旧或脏数据。

> 核心判断：决策点不是"要不要用 Agentic RAG"，而是"哪类问题值得额外投入"。
