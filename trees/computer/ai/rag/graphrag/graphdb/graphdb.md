---
description: "Graph databases: property graphs, Cypher/GQL, products and graph-versus-vector selection"
描述: "图数据库：属性图模型、查询语言、产品对比与图/向量选型"
name: "Graph Databases"
名称: "图数据库"
---

# 图数据库

图数据库以"节点-关系-属性"原生存储，沿显式连接遍历回答问题——它专为"谁通过什么、在几步内连到谁"这类查询而生，而这类查询在关系型数据库里要靠大量 JOIN。

一个关键区分：**图数据库是存储技术，知识图谱是放进它的内容**（本体 + 实体消歧后每个现实实体只出现一次）。把 CSV 灌进 Neo4j 而没有本体、实体解析和溯源，得到的是"图形状的孤岛"，不是语义层。图数据库只是 GraphRAG 的底座之一。

## 属性图模型

- **节点（Node）**：实体，有标签（类型）和属性。
- **关系（Relationship / Edge）**：节点间的有向连接，有类型和属性——关系本身是一等公民，可带权重、时间、置信度。
- **属性（Property）**：节点与边都可带多值属性。
- 早期用 RDF 三元组；现在是**属性图（Property Graph）**主流，更灵活。属性图模型 2024 年 4 月成为 ISO 标准 **GQL（ISO/IEC 39075:2024）**，类似 SQL 标准化关系查询。

建模要点：实体唯一（用唯一 ID/URI）、关系有方向、属性可多值。

## 查询语言

| 语言 | 代表产品 | 特点 |
|---|---|---|
| **Cypher** | Neo4j、Memgraph、NebulaGraph（部分兼容） | 声明式、ASCII-art 语法（`MATCH (p:Person)-[:KNOWS]->(f) RETURN f`），贴近 SQL，学习曲线平缓 |
| **Gremlin** | JanusGraph、Amazon Neptune | 命令式图遍历，灵活但复杂度高，适合遍历专家 |
| **nGQL** | NebulaGraph | 类 SQL，支持多数 openCypher 读语法，写语法不兼容 |
| **GSQL** | TigerGraph | 类存储过程，支持多数 openCypher 与 GQL 模式匹配，专有性强 |
| **SPARQL** | RDF 三元组库（Stardog、GraphDB） | 语义网标准，适合知识图谱与逻辑推理 |

AQL（ArangoDB）是统一多模型的类 SQL 语言。若已在 PostgreSQL 上，Apache AGE 扩展可在 Postgres 上跑 openCypher；`pg_graphql` 也能做类图查询——这是评估图数据库前的低成本入口。

## 主流产品对比（2026）

| 产品 | 架构 | 存储 | 查询语言 | 事务 | 最佳场景 |
|---|---|---|---|---|---|
| **Neo4j** | 单机/因果集群 | 原生图存储 | Cypher | 完整 ACID（写前日志） | 通用、入门首选、生态最成熟 |
| **Memgraph** | 内存 | 内存 | Cypher | — | 实时图分析、GraphRAG、AI 记忆 |
| **JanusGraph** | 分布式 | 依赖后端（Cassandra/HBase/Bigtable） | Gremlin | ACID（依赖后端）、最终一致 | 已有 Hadoop 存储栈、超大规模开源 |
| **TigerGraph** | 原生分布式并行 | 自研列式 | GSQL | 支持 | 欺诈/AML、供应链、大规模企业分析 |
| **NebulaGraph** | 存算分离分布式 | RocksDB（自研） | nGQL | 单行事务、Raft 即时一致 | 海量数据、社交/风控/推荐 |
| **Amazon Neptune** | 托管云 | AWS 托管（基于 Aurora） | Gremlin/SPARQL/openCypher | ACID | 免运维、AWS 生态 |
| **ArangoDB** | 单机/集群 | 自研多模型 | AQL | 强 ACID | 图+文档+键值统一 |

DB-Engines 2026-11 纯图数据库前五：Neo4j、Memgraph、JanusGraph、TigerGraph、NebulaGraph。

**选型原则**：零基础/通用首选 Neo4j（Cypher 像 SQL，上手最快，浏览器与 Bloom 可视化强）；超大规模横向扩展选 NebulaGraph；已有 Cassandra/HBase 选 JanusGraph；大规模分析选 TigerGraph；免运维选 Neptune。

## 图 vs 向量 vs 关系型

| 维度 | 关系型（SQL） | 图 | 向量 |
|---|---|---|---|
| 数据结构 | 严格表（行列） | 节点与边 | 高维浮点数组 |
| 查询机制 | 精确匹配（WHERE id=5） | 遍历（`MATCH (a)-[:KNOWS]->(b)`） | 最近邻（余弦相似度） |
| 灵活性 | 刚性 | 高度灵活的 schema | 无 schema（向量+元数据） |
| AI 集成 | Text-to-SQL | GraphRAG、Text-to-Cypher | 文档 RAG |
| 优势 | 聚合、ACID、生态成熟 | 多跳遍历、可解释路径 | 语义相似、开放域检索 |
| 劣势 | 多跳 JOIN 慢 | 不适合聚合/报表 | 不能做数学、聚合、唯一约束 |

经验法则：**90% 的软件用关系型就够；向量库只存语义文本做 RAG；只有遍历高度复杂的多跳实体关系时才上图库**。

基准证据：HippoRAG 2（ICML 2025）中强向量检索器在七个 QA 数据集平均 57.0 F1，Microsoft 社区 GraphRAG 仅 49.6——在直白事实问题上，图不如向量。2026 GraphRAG-Bench 也同意：简单事实检索基础 RAG 持平或胜出，图在复杂推理与跨语料总结才领先，且**图索引构建慢 40–57 倍**。

> 用向量回答"给我找到那段话"；用图回答"跨记录推导出答案"。混合流量下，混合方案胜过任一单独方案。

## 与 GraphRAG 的接口链

GraphRAG 的落地路径：**LLM 抽取实体关系 → 实体消歧 → 写入图库 → 遍历/Cypher 查询 → 拼上下文**。

- 大模型负责"抽取 + 推理"，图数据库负责"存储 + 查询"。
- Neo4j 官方 GraphRAG + LangChain/LlamaIndex 是主流方案；LightRAG 更便宜；Memgraph 主打实时 GraphRAG。
- **LLM 抽的三元组必须校验**（人工审核或置信度阈值），否则幻觉关系会污染图——合规与金融场景强制要求。
- 图查询的路径可解释，每条结果都有可追溯路径——这是向量相似度给不了的。

## 图算法与推理

图遍历（Path）、规则（Rule）、嵌入（Embedding）可推导隐含知识：如"A 是 B 的父亲、B 是 C 的父亲 → A 是 C 的祖父"。常见算法：最短路径、社区发现、中心性。Neo4j 原生遍历六跳关系在毫秒级，而递归 SQL CTE 超线性退化——这是架构差异，不是调参能弥补的。

## 常见误区

- 把图数据库等同于知识图谱（缺本体、实体解析、溯源）。
- 没有明确查询就建模——先定干系人每周会跑的查询，再建最小 schema。
- 跳过实体解析——重复节点摧毁遍历价值；实体解析本质二次复杂度，需人工判断，是工具支持最弱的一步。
- 把图当唯一真相源——无同步纪律与溯源（sourceSystem、lastUpdated、confidence），图会漂移。
- 本体过度工程——数据还没来就上 OWL 推理器和 500 类层级。
- 忽略访问控制——图查询暴露跨敏感边界的路径；在图 API 层按子图/标签限权，别写进 LLM 提示。
- 无界图探索——面向用户的"探索图" UI 若无限跳数/结果上限/成本估算，会导致组合爆炸。
- RDF 与属性图在同一领域双轨——工具、映射、认知负担翻倍；多图共存就在 API 层联邦。

## 何时不用

- 查询纯聚合（sum/count/GROUP BY）→ SQL 或数仓。
- 无跨系统身份问题（单应用单 schema、无 sameAs 需求）→ PostgreSQL + 递归 CTE 可能更简单（<20 实体类型时）。
- 语义相似主导（无关系结构的文档问答）→ 向量库。
- 不是每条边都要亚秒新鲜度——按 SLA 匹配架构，别浪费成本。

一个生产知识库常同时跑四种：OLTP 在 PostgreSQL、分析在数仓、相似在 Qdrant/Pinecone、关系在 Neo4j/GraphDB，在 API 层联邦。

> 相关：GraphRAG 范式见 `../graphrag.md`；图与向量混合检索见 `../../retrieval/`；元数据与 ACL 见 `../../vdb/filter/`；RAG 参考架构见 `../../basics/`。
