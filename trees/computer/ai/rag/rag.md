---
description: "Knowledge tree for retrieval-augmented generation engineering"
描述: "RAG 工程：切块、嵌入、索引、检索与评估的全链路"
name: "Retrieval-Augmented Generation"
名称: "检索增强生成"
---

# RAG 知识树

RAG（检索增强生成）让模型在查询时从自有数据中检索相关事实，而不是只依赖训练记忆。本目录把 RAG 工程拆成 19 个子知识点，每个自成一个目录、目录内放同名介绍 md。

知识库先要决定两件事：知识按什么形态组织、用什么存储要素承载。知识库形态与存储要素不是一回事，向量库、图数据库只是存储/索引要素。

## 摄取是第一道关口

RAG 的质量上限首先由“进来的数据”决定。数据源选错、抓取残缺、解析脏乱、去重不净，后面的切块、嵌入与检索都只是在放大噪声。摄取层要先把数据源、抓取、解析、去重、增量与质量串成一条可观测的链。

## 四步基线流水线

一条能落地的基线是：按章节结构与语义边界切块，把块转向量写入向量库，查询时向量与 BM25 并行召回并融合，最后用 Cross-Encoder 重排。四步分别守住语义、覆盖、精确与排序；这条**四步基线流水线**的接口、验收与失败定位单独展开。

## 一句话主线

从"检索而非记忆"的基础出发，把文档切好块、选对嵌入与索引、用混合检索与重排精排。

若想要一条**非向量的替代路线**——把知识编译成持续维护、Git 版本控制的可读 Wiki，它是 RAG 从解释器模式到编译器模式的演进。

## 参考资料

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（Lewis et al., 2020）：https://arxiv.org/abs/2005.11401
- Retrieval-Augmented Generation for Large Language Models: A Survey：https://arxiv.org/abs/2312.10997
