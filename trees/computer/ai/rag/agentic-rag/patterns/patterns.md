---
description: "Agentic RAG architecture patterns: Router, ReAct, Plan-and-Execute, Multi-hop, Self-RAG, CRAG, Adaptive and agent cardinality"
描述: "Agentic RAG 架构模式：路由、ReAct、规划执行、多跳、自检与 Agent 数量"
name: "Agentic RAG Patterns"
名称: "Agentic RAG 架构模式"
---

# Agentic RAG 架构模式

Agentic RAG 不是单一算法，而是一族共享"Agent-in-the-loop"原则的模式。文献与实践收敛出约 5–7 种反复出现的模式，可任意组合——生产系统常同时用两三种。理解每种的**机制**才能按问题选，而非盲目跟风名字。

## 核心模式

| 模式 | 机制 | 适合 | 失效于 |
|---|---|---|---|
| **Router RAG** | 轻量分类器把查询路由到一种检索策略（向量/SQL/API/直接回答），无检索循环 | 查询类型界限清晰、各有最优路径 | 含糊问题、需多策略组合 |
| **ReAct** | 推理与检索动作交错：想→检索→观察→再想，每步据上一步调整 | 路径事先不可知、需透明可解释 | 推理漂移、同一动作打转、token 空耗 |
| **Plan-and-Execute** | 先产出完整检索计划（子查询序列），再（常并行）执行，最后综合 | 子查询独立的复合问题；并行性好，延迟近 2× 标准 RAG | 每步依赖上一步时弱于 ReAct |
| **Multi-hop** | 分解复杂问题为子问题，链式检索（每个查询依赖上一个的结果）， planner + aggregator | 答案散在多文档、单一块装不下 | 分解错→错误传播污染下游 |
| **Self-RAG** | 模型发射反射 token，自适应决定检索、评估证据、批判自身输出 | 事实性要求高（法律/医疗/金融）；需微调模型 | 模型自评能力差（弱模型自信批准错答）；闭源 API 不可用 |
| **CRAG**（Corrective RAG） | 生成前加检索评估器，按相关性走正确/含糊/错误三分支，错误时 web 兜底 | 检索质量不稳（多数生产系统）；最易部署 | 评估器校准差；web 兜底延迟高 |
| **Adaptive RAG** | 查询分类器在检索前按复杂度分流：简单跳过、中等单跳、复杂走完整循环 | 混合负载、成本敏感；60–70% 查询是简单的 | 误分类（复杂查询走廉价路径，无恢复） |

关键分工一句话：**Self-RAG 评答案、CRAG 评文档、Adaptive 评问题**。三者正交可组合——Adaptive 决定检索多少，CRAG/Self-RAG 决定检索好不好。

## Agent 数量：single vs multi

| 维度 | 单 Agent（Router） | 多 Agent |
|---|---|---|
| 协调 | 一个循环处理检索→评分→生成 | 编排器委派给专门 Agent（planner/retriever/critic/synthesizer） |
| 延迟成本 | 低，LLM 调用少 | 高，调用与交接多 |
| 调试 | 简单，单一决策路径 | 难，需逐 Agent 追踪 |
| 适合 | 聚焦领域、严格延迟预算 | 广域、跨领域、并行子任务 |
| 失效 | 循环卡住或过度检索 | Agent 分歧或重复劳动 |

单 Agent（一个 router + 一个强模型）是**最简单也最常见**的形态，足以应付直接检索需求。多 Agent 能力随成本同步增长——架构应匹配系统实际会被问到的最难问题，而非想象中的 hardest case。

## 循环的解剖

典型 agentic RAG 循环五步：

1. **评估查询**：是否需要检索？问题表面下真正在问什么？
2. **规划与路由**：拆成子查询，每个路由到最可能回答的源/工具。
3. **检索**：搜索选定源，拉取候选证据。
4. **评估与精炼**：证据是否回答问题？弱则改写查询、换源、再搜。
5. **生成**：证据充分后，综合成带引用的答案。

循环需有界（迭代上限、成本预算），触限时干净降级到已有最佳证据。LangGraph 因其 checkpoint 让每步可追踪、可暂停（人工审批）、可重放，是 2026 生产最常用控制流运行时；LlamaIndex Workflows 常见于单管道检索重的变体。

## 选择建议

- 默认从单 Agent Router 起步——多数场景够了。
- 检索质量不稳 → 加 CRAG（外部评估器，便宜、易部署）。
- 事实性极关键且能微调模型 → Self-RAG；闭源 API 模型 → 排除 Self-RAG。
- 混合负载成本敏感 → Adaptive 路由先行（简单查询走快路，可为净负成本）。
- 跨源、并行子任务、需专门角色 → 多 Agent；但先证明单 Agent 不够。

> 相关：三种自检机制的深度对比见 `../self-correcting/`；架构转变与成本延迟见 `../retrieval-as-tool/`；查询改写见 `../../query-transform/`；多智能体协作见 `../../../agent/multi/`。
