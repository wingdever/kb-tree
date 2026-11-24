---
description: "Knowledge graphs, RAPTOR, semantic layers and query routing"
描述: "知识图谱、RAPTOR、语义层与按查询类型路由"
name: "GraphRAG and Structured Retrieval"
名称: "GraphRAG 与结构化检索"
---

# GraphRAG 与结构化检索

向量数据库把世界压平成向量列表；知识图谱保留结构。当问题需要跨多个相关块推理、而非检索单个最佳块时，图检索胜过向量相似度。本主题已拆成 6 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `graphdb/` | 图数据库底座：属性图模型、Cypher/GQL、Neo4j 等产品对比、图/向量/关系型选型 |
| `kg-construction/` | 知识图谱构建：本体、实体解析、溯源、增量更新、工具生态 |
| `ontology/` | 本体论：TBox/ABox、OWL/RDF/SHACL、能力问题驱动设计、LLM 构建、本体漂移与治理 |
| `raptor/` | 递归摘要树：软聚类、层级摘要、两种检索方式、成本权衡 |
| `semantic-layer/` | 语义层与指标平台：受治理定义、确定性 Text-to-SQL、准确率证据；已展开子树：`semantic-layer/text-to-sql/` |
| `frameworks/` | GraphRAG 实现选型：Microsoft / LightRAG / Graphiti / LazyGraphRAG 对比 |

## GraphRAG 范式

索引期用 LLM 从文本抽取实体与关系，建知识图谱（实体、关系、层级社区）；查询期遍历关系拼上下文。

- Microsoft GraphRAG 论文（Edge et al. 2024）：**局部问题与向量 RAG 相当，全局问题（"总结整个语料主题"）显著更好**，社区摘要对 Global 查询胜率 72–83%。
- 但 HippoRAG 2（ICML 2025）中强向量检索器平均 57.0 F1、社区 GraphRAG 仅 49.6——直白事实问题上图不如向量；图索引构建慢 40–57 倍。
- **适用**：高价值、低查询量语料——监管文件、研究文献、并购尽调、大型内部知识库；关系推理、可解释路径、全局综合。
- **过度设计**：多数查询是单实体事实的客服场景。

示例："中国供应链风险如何影响我们美国生产？"——向量可能只找到关于"中国"和"美国"的文章；GraphRAG 沿路径追踪：中国工厂 --供应--> 组件X --用于--> 美国产品Y。

## 查询路由（按类型选择检索策略）

这是整个 RAG 树的枢纽表——**一种检索策略打天下，是 Agent 自信地答错的根源**。

| 查询类型 | 路由到 |
|---|---|
| 精确查找 / 术语 / ID | 混合 RAG（BM25 + 向量，见 `../retrieval/`） |
| 关系 / 多跳 / 全局 | GraphRAG（见 `./frameworks/`、`./kg-construction/`） |
| 指标 / KPI / 结构化 | 语义层 / SQL（见 `./semantic-layer/`） |
| 全局主题 / 跨文档总结 | RAPTOR 层级摘要或 GraphRAG Global（见 `./raptor/`） |
| 最新 / 实时 | Web 搜索工具 |
| 私有文档 | 内部向量索引 |

## 一句话主线

先用查询路由判断问题类型（`查询路由`表）；需要结构化存储就选 `graphdb/` 并走 `kg-construction/` 构建；需要层级抽象用 `raptor/`；需要确定性数字走 `semantic-layer/`；要落地成系统就在 `frameworks/` 里按成本与全局查询需求选型——始终记住图是关系复杂场景的增强，不是 RAG 的替代。

## 工程要点

- 图检索的索引成本是真实的，务必确认问题真的需要关系推理再上。
- 多跳检索（agentic）与 GraphRAG 互补：前者靠 Agent 多次调用工具，后者靠图结构一次遍历。
- 元数据/ACL 必须贯穿图与向量两侧（见 `../prod/`）。

> 相关：Agentic RAG 的多跳场景见 `../agentic-rag/`；图与向量混合检索见 `../retrieval/`；RAG 工具箱总览见 `../basics/`；RAG 整体评估见 `../eval/`。
