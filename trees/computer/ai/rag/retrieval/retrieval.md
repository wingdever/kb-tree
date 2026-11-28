---
description: "Knowledge tree for recall, reranking and fusion algorithms"
描述: "检索算法：BM25、向量、混合检索与重排"
name: "Retrieval Algorithms"
名称: "检索算法"
---

# 检索算法：召回与精排

检索分两段：先用便宜算法铺开候选，再用贵模型精排；预算花在排序端，广度靠召回端。本主题已拆成 3 个子知识点目录。

## 典型算法栈

> BGE/GTE 嵌入（Bi-Encoder）+ HNSW 向量索引 + BM25 词法召回 + RRF 融合 + Cross-Encoder 精排

规模不大或对延迟敏感时，先用 HNSW + BGE 跑通，再按需叠加 BM25 与重排。

## 参考资料

- Introduction to Information Retrieval（Manning et al.）：https://nlp.stanford.edu/IR-book/
- ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT：https://arxiv.org/abs/2004.12832
