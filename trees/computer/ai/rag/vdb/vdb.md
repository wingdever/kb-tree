---
description: "Knowledge tree for vector databases and ANN indexes"
描述: "向量数据库知识树导航"
name: "Vector Databases and ANN Indexes"
名称: "向量数据库"
---

# 向量数据库与 ANN 索引

向量数据库专门存"意思坐标"并毫秒级找相似，是 RAG 与语义搜索的底座。核心是用 ANN（近似最近邻）以一点召回换巨大速度。本主题已拆成 4 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `ann/` | HNSW/IVF/PQ/DiskANN/ScaNN 原理、工程经验、热冷分层 |
| `products/` | Pinecone/Milvus/Qdrant/Weaviate/pgvector 等对比、决策树、迁移路径 |
| `filter/` | pre/post-filter、自适应过滤、RBAC、元数据字段设计 |
| `cost/` | 成本三驱动、量化/降维/分层、版本化、上线清单 |

## 什么时候才需要

- **该上**：十万级以上向量、秒级返回、要与元数据混合过滤。
- **别上**：几百条资料（内存数组几毫秒搞定）、纯精确关键词匹配、强事务 OLTP。
- 2026 模式：前 90 天用嵌入式（LanceDB、Chroma、FAISS），毕业到生产再迁专用库。

> 相关：混合检索融合见 `../retrieval/`；元数据 RBAC 见 `../prod/`；降维见 `../embedding/`。
