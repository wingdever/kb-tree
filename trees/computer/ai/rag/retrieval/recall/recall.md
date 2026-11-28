---
description: "Bi-Encoder, BM25, SPLADE learned sparse and dense recall signals"
描述: "双编码器、BM25、SPLADE 学习稀疏与稠密召回信号"
name: "Recall: Sparse and Dense"
名称: "召回"
---

# 召回：Bi-Encoder、稠密与稀疏

工程原则：**用轻量算法换取召回广度，再用昂贵算法换取排序精度**。两阶段流水线：召回（大中求快）→ 精排。

## Bi-Encoder（双编码器）

用同一个编码器分别处理查询和文档，各生成固定长度向量，用余弦相似度或内积衡量。文档向量在入库时预计算并建索引，查询时只编码一次查询 + ANN 搜索。

- **代价**：查询与文档无 token 级交互，相关性判断粗略；遇否定、逻辑约束、精确术语易失准——这正是精排要弥补的。
- BGE、E5 属此家族，对比学习训练，核心 loss 是 InfoNCE。

## 三种检索信号对照

| 维度 | BM25（稀疏） | SPLADE（学习稀疏） | 稠密向量 |
|---|---|---|---|
| 精确匹配 | 优秀 | 好 | 差 |
| 语义匹配 | 无 | 好 | 优秀 |
| 稀有词 | 优秀 | 好 | 不可靠 |
| 同义词 | 无（除非手工词表） | 好 | 优秀 |
| 速度 | 极快 | 快 | 快（需 ANN） |
| 索引 | 倒排索引 | 倒排索引 | 向量索引（HNSW/IVF） |
| 存储 | 小 | 中 | 大 |
| 搭建复杂度 | 极简 | 需训练模型 | 需嵌入模型 |

**没有单一信号处处胜出**——这正是混合检索存在的原因。

## BM25

基于词频与逆文档频率的经典稀疏检索，30 年主导词法搜索。无监督、可解释、不需训练数据，擅长精确匹配版本号、错误码、产品名。

## SPLADE（学习稀疏检索）

Sparse Lexical and Expansion Retrieval：用 transformer（BERT MLM head）输出词表上的稀疏权重向量（~100–300 非零维），既保留精确匹配能力，又学到语义扩展（搜 "car" 自动加权 "vehicle/automobile/sedan"）。

- 直接存入标准倒排索引，评分是词匹配点积——本质是"学权重的 BM25"。
- **最强优势是 zero-shot 跨域泛化**（BEIR 上 sparse-only SOTA）；有标注数据做域内微调时，微调的稠密检索器可追平或超过它。
- ELSER（Elastic）、Pinecone sparse、OpenSearch neural sparse、miniCOIL（Qdrant）是 2026 生产方案。
- **代价**：需训练数据（<10k 相关对时 BM25+稠密重排常更优）；查询延迟 50–200ms（查询扩展 + transformer 前向）。
- **inference-free 模式**：所有扩展在索引期做，查询期只查学到的权重，接近 BM25 速度。

> 经验：为了让 transformer 花费可摊薄——在索引期付（摊销）还是查询期付（每次账单），是真正的架构选择。

## 向量召回

暴力扫描不可行，需 ANN 索引。HNSW 是多数 RAG 场景的稳妥默认。

## 典型召回栈

> BGE/GTE 嵌入（Bi-Encoder）+ HNSW 向量索引 + BM25 词法召回 + RRF 融合

若知识库不大或对延迟敏感，先用 HNSW + BGE 跑通，再按需叠加 BM25。

## 参考资料

- Introduction to Information Retrieval（Manning et al.）：https://nlp.stanford.edu/IR-book/
- SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking：https://arxiv.org/abs/2107.05720
