---
description: "GraphRAG implementations compared: Microsoft GraphRAG, LightRAG, Graphiti, LazyGraphRAG, Neo4j+LangChain"
描述: "GraphRAG 实现选型：Microsoft GraphRAG、LightRAG、Graphiti 等对比"
name: "GraphRAG Frameworks and Selection"
名称: "GraphRAG 实现与选型"
---

# GraphRAG 实现与选型

几个框架主导 GraphRAG 空间，各自落在复杂度/成本/能力的曲线上不同点。选型的本质是"业务问题倒推需要哪类能力"，不是"哪家技术最强"。

## 主流方案对比

| 方案 | 定位 | 索引成本（500 页） | 索引时间 | 全局查询 | 增量更新 | 最适合 |
|---|---|---|---|---|---|---|
| **Microsoft GraphRAG** | 方法体系 + 工具链 | $50–200 | ~45 min | 优秀 | 复杂 | 大语料、全局综合、研发组织 |
| **LightRAG**（港大） | 轻量快速 | ~$0.50 | ~3 min | 有限 | 简单 | 中小团队、快速原型、成本敏感 |
| **LazyGraphRAG**（微软） | 成本杀手 | 近乎零（按需提取） | 查询时建图 | 中 | 原生 | 预算敏感、文档频繁更新 |
| **Graphiti (Zep)** | agent 记忆 / 时间图 | 随交互量 | 实时 | 非设计目标 | 原生 | 随时间演化的 agent 记忆 |
| **Neo4j + LangChain** | 工程自定义 | 中（schema 抽取） | — | 取决于自建 | 自建 | 领域专用、精确控制 |
| **Cognee** | 模块化记忆引擎 | 灵活 | — | — | 灵活 | 最大架构灵活性 |
| **TypeGraph** | TS 原生（Postgres） | — | — | — | — | Next.js/Vercel/TypeScript 栈 |

数据点：LightRAG GitHub stars（约 37.2k）已超微软官方 GraphRAG（约 34.1k）——社区对"轻量、快速、生产可用"的诉求超过对"功能全面、学术权威"的崇拜。

## 各方案要点

### Microsoft GraphRAG（重量级）

参考实现，完整实体抽取 + Leiden 社区检测 + 层级摘要。社区层级让"总结关于 X 的一切"这类全局查询无出其右。**DRIFT search**（2024 末）结合本地与全局搜索，复杂查询降本 40–60%。弱点：索引成本 brutal（500 页 $50–200、约 45 分钟），重索引要重跑全流程；生产需仔细成本监控。

### LightRAG（务实派）

剥离到本质：更简单的实体抽取、平坦图（无社区检测）、双层检索（low-level 实体 + high-level 概念）+ 图遍历与向量相似结合。以 **1/100 成本达到 GraphRAG 70–90% 质量**；平坦结构让增量更新直接。弱点：无层级社区摘要，全局主题查询（"所有文档的主要主题"）明显更差。

### LazyGraphRAG（成本杀手）

把 LLM 抽取推迟到查询时，索引成本近乎消失（百万文档索引从约 30,000 降到极低）。适合流式数据、成本敏感团队、探索式分析；代价是查询时延迟更高。

### Graphiti（时间图专家）

为 agent 记忆构建，非文档问答。每条边有有效期，正确处理"Alice 2025 前是 X 的 CTO，现在是 Y 的 CTO"。显式事实版本化、关系失效、时间感知检索。需 Neo4j；不适合大规模文档摄取。

### Neo4j + LangChain（工程自定义）

`Neo4jGraph` + `GraphCypherQAChain.from_llm(...)` 自建抽取/摘要流水线，灵活度高， upfront 工程量大。适合领域专用应用与精确控制。

## 检索模式

| 模式 | 做法 | 适用 |
|---|---|---|
| **Local** | 局部子图检索 | 具体实体、多跳关联查询 |
| **Global** | 社区摘要聚合 | 语料级主题/全局综合 |
| **Hybrid** | 两者结合 | 混合问题 |

生产 Multi-on：多数部署默认 Local，仅在查询明显是主题型时回退 Global；社区摘要在索引期预计算。

## 客观看待效果

- Microsoft GraphRAG 论文：约一百万 token 语料的全局 sensemaking 问题，在全面性与多样性上大幅优于向量 RAG；社区摘要对 Global 查询胜率 **72–83%**。
- 但 **HippoRAG 2（ICML 2025）**：强向量检索器七个 QA 数据集平均 57.0 F1，Microsoft 社区 GraphRAG 仅 49.6——直白事实问题上图不如向量。
- **GraphRAG-Bench（2026）**：简单事实检索基础 RAG 持平或胜出，图在复杂推理与跨语料总结才领先；图索引构建慢 **40–57 倍**。
- 多基准：GraphRAG-Bench novel/medical 分数各家差异大（Microsoft 50.93/45.16、LightRAG 45.09/62.59、TypeGraph 62.65/67.68）——同一框架在不同语料表现不一。

**结论**：GraphRAG 不是替代 RAG，而是关系复杂场景的增强。生产共识是**混合路由**——简单事实查询走向量，复杂推理走图，让合适的技术解决合适的问题。务必用自己语料做 A/B（Naive vs GraphRAG vs Hybrid，同一 LLM 底座），而非信论文分数。

## 工程成本（常被忽略）

三层成本：① **Schema 设计**——最难的不是框架而是本体， Goldman Sachs/Deloitte 等成功部署在写检索代码前投入数周做本体。② **图维护**——文档变化后要重抽实体、与现有节点对账（"Microsoft Corp" 与 "Microsoft" 同一吗？），增量更新是核心难题。③ **无界遍历**——设跳数与结果上限，否则组合爆炸。

