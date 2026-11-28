---
description: "RAPTOR: recursive abstractive tree of hierarchical summaries for multi-level retrieval"
描述: "RAPTOR：递归摘要树与多层级检索"
name: "RAPTOR: Recursive Abstraction Tree"
名称: "RAPTOR 递归抽象树"
---

# RAPTOR（递归抽象树）

RAPTOR（Recursive Abstractive Processing for Tree-Organized Retrieval）用递归聚类和摘要把文档组织成一棵层级树，让检索既命中底层细节、也能命中高层主题摘要。它不改变查询入口，而是重塑知识库的内部结构。

## 解决什么问题

传统 RAG 只检索切好的小块。当答案散落在不同章节（如论文的方法在 A 节、实验在 B 节、结论在 C 节），只取几个块就拼不出完整上下文。RAPTOR 让系统可以检索叶节点（细节）或高层摘要（宏观背景），按问题复杂度决定。

## 构建流程（自底向上）

1. **叶节点**：长文档切成小块，每块用嵌入模型（多为 SBERT 类，如 multi-qa-mpnet-base-cos-v1）向量化。
2. **聚类**：用层次聚类把语义相似的块分组。RAPTOR 的关键创新是**软聚类**（GMM 高斯混合模型）——一段文本可同时属于多个簇，比 K-means 硬切更贴近自然语言（一段落常含多主题）。聚类前用 UMAP 降维，簇数由 BIC（贝叶斯信息准则）动态确定。
3. **LLM 摘要**：对每个簇用 LLM 生成**抽象式摘要**（非抽取式照搬），作为上一层的父节点。
4. **递归向上**：父节点重新嵌入、再聚类、再摘要，直到无法/无需继续，最终收敛到一个根节点（代表全语料宏观叙事）。
5. **全部入索引**：叶节点、各层摘要、根节点**全部向量化纳入检索空间**。

## 两种检索方式

| 方式 | 做法 | 特点 |
|---|---|---|
| **树遍历（Tree Traversal）** | 自顶向下逐层：根比相似度选 top-k → 只进入这些父节点的子节点 → 逐层到底 | 垂直切片聚焦，但可能漏掉横向相关信息 |
| **折叠树（Collapsed Tree）** | 把整棵树拍平成一个集合（所有层级节点），一次性算相似度取全局 top-k 到 token 阈值 | **实测优于逐层遍历**——复杂主题问题需要同时看到高层摘要与底层细节 |

## 效果与成本

- 压缩率约 **72%**（相对原文）；父摘要长度约为子节点的 0.28 倍（摘要均长约 131 token，子节点约 85.6 token）。
- 在多跳推理与阅读理解上明显优于扁平检索。
- **代价**：构建需多次 LLM 调用（聚类+摘要），系统变复杂；源文档更新后可能要重建整棵树或受影响分支，比更新向量库切片麻烦。
- 现实权衡：精心优化的普通 RAG 常已达 80 分，RAPTOR 可能只到 85 分——为 5 分提升付出数倍维护成本。它是**特定复杂文档场景的特种武器，不是日常标配**。

## 何时用 / 不用

**用**：长文档、答案需跨多节综合、需要不同抽象层级上下文。

**不用**：简单事实查询、语料小、延迟敏感、语料频繁变动（重建成本高）。

## 参考资料

- RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval：https://arxiv.org/abs/2401.18059
- Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models：https://arxiv.org/abs/2409.04701
