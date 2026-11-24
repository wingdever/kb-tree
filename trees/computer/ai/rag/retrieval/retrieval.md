---
description: "Knowledge tree for recall, reranking and fusion algorithms"
描述: "检索算法：BM25、向量、混合检索与重排"
name: "Retrieval Algorithms"
名称: "检索算法"
---

# 检索算法：召回与精排

工程原则：**用轻量算法换取召回广度，再用昂贵算法换取排序精度**。两阶段流水线：召回（大中求快）→ 精排（准中求精）。本主题已拆成 3 个子知识点目录。

## 典型算法栈

> BGE/GTE 嵌入（Bi-Encoder）+ HNSW 向量索引 + BM25 词法召回 + RRF 融合 + Cross-Encoder 精排

规模不大或对延迟敏感时，先用 HNSW + BGE 跑通，再按需叠加 BM25 与重排。

