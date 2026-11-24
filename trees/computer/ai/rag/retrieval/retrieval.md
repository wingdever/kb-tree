---
description: "Knowledge tree for recall, reranking and fusion algorithms"
描述: "检索算法知识树导航"
name: "Retrieval Algorithms"
名称: "检索算法"
---

# 检索算法：召回与精排

工程原则：**用轻量算法换取召回广度，再用昂贵算法换取排序精度**。两阶段流水线：召回（大中求快）→ 精排（准中求精）。本主题已拆成 3 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `recall/` | Bi-Encoder、BM25、SPLADE 学习稀疏、稠密检索、三种信号对照 |
| `rerank/` | Cross-Encoder、ColBERT 延迟交互、LLM-as-reranker、何时跳过重排 |
| `fusion/` | RRF/分数归一化、改写/分解/HyDE、完整流水线、自适应检索 |

## 典型算法栈

> BGE/GTE 嵌入（Bi-Encoder）+ HNSW 向量索引 + BM25 词法召回 + RRF 融合 + Cross-Encoder 精排

规模不大或对延迟敏感时，先用 HNSW + BGE 跑通，再按需叠加 BM25 与重排。

> 相关：ANN 索引见 `../vdb/`；验证见 `../eval/`。
