---
description: "Product comparison, decision tree and migration paths"
描述: "向量数据库产品对比、决策树与迁移路径"
name: "Vector Database Selection"
名称: "向量数据库产品选型"
---

# 向量数据库产品选型

## 什么时候才需要

- **该上**：十万级以上向量、秒级返回、要与元数据混合过滤。
- **别上**：几百条资料（内存数组几毫秒搞定）、纯精确关键词匹配、强事务 OLTP。
- 2026 模式：项目前 90 天先用嵌入式（LanceDB、Chroma、FAISS），毕业到生产再迁专用库。迁移非零成本但路径成熟。

## 主流产品对比（2026）

| 产品 | 形态 | 索引 | 规模 | 滤波 | 特点 |
|---|---|---|---|---|---|
| **Pinecone** | 全托管 SaaS | 自研（称从未用 HNSW） | 数十亿+ | 中 | 免运维、贵、锁定控制面、无本地部署、无开箱 BM25 |
| **Milvus/Zilliz** | 开源分布式 | HNSW/IVF/DiskANN/GPU | 百亿+ | 好 | 大规模、运维复杂（etcd/MinIO） |
| **Qdrant** | 开源 Rust | HNSW + payload | 十亿+ | 优秀 | 过滤下推最干净、QPS/vCPU 高 |
| **Weaviate** | 开源+云 | HNSW + 倒排 | 数亿+ | 好 | 混合搜索、模块系统、对象模型灵活 |
| **Chroma** | 嵌入式 | HNSW | 千~百万 | — | LangChain 默认、POC 首选 |
| **pgvector** | Postgres 扩展 | HNSW/IVFFlat | 1 亿+ | 优秀(SQL) | 已有 Postgres 时成本最优 |
| **LanceDB** | 嵌入式/S3 | IVF-PQ/HNSW | 1 亿+ | 好 | 本地分析、S3 后端 |
| **Elasticsearch/OpenSearch** | 搜索引擎 | HNSW (Lucene) | 数十亿 | 优秀 | 已有 Lucene 集群时混合检索最佳 |
| **Vespa** | 开源搜索引擎 | HNSW + 结构化过滤 | 数十亿 | 优秀 | 多向量/张量，支持 ColBERT |

## 选择决策树

- 数据在 Postgres 且 <5000 万向量 → **pgvector + HNSW**（运维成本难被击败）。
- 需横向扩展过十亿 → **Milvus 或 Pinecone**。
- 需丰富元数据过滤且从零开始 → **Qdrant**（过滤下推最干净）。
- 开箱即用混合关键词+向量 → **Vespa / Elasticsearch / OpenSearch**。
- 个人 Demo → **Chroma**；上生产免运维 → **Pinecone**；大规模开源可控 → **Milvus**。
- 需要 learned sparse（SPLADE/ELSER）→ Elasticsearch / OpenSearch / Pinecone sparse index。

## 延迟与吞吐经验

- 内存 HNSW（Qdrant、Weaviate、Pinecone）在 100 万向量并发下 top-k 约个位数~低两位数毫秒。
- Milvus 多一跳查询节点，p99 偏高除非超配。
- pgvector HNSW 接近内存阵营；IVFFlat 需调 `lists` 否则退化。
- Qdrant 的 Rust 核心每 vCPU QPS 高于 Python 绑定路径。

## 迁移是必然

典型路径：阶段 1 pgvector（快速实现）→ 阶段 2 专用向量库（数据/查询复杂度增长）→ 阶段 3 检索平台（混合排序 + 重排 + 可观测）。

从第一天为迁移设计：保持 chunk ID 稳定、元数据版本化嵌入模型、解耦摄入与检索服务、抽象查询层避免 Provider 切换变成全应用重写。

> 相关：索引算法原理见 `../ann/`；过滤见 `../filter/`；成本见 `../cost/`。
