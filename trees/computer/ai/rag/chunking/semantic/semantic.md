---
description: "Semantic similarity and hierarchical parent-child chunking"
描述: "语义相似度切分与层级父子分块"
name: "Semantic and Parent-Child Chunking"
名称: "语义与父子切块"
---

# 语义切块与父子切块

## 语义分割（Semantic chunking）

计算每个句子的嵌入，相邻句子余弦相似度骤降处即主题边界。结果是变长、对应连贯主题的块，而非任意 token 计数。

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model,
)
```

- **代价**：索引期要嵌入每个句子（嵌入调用增至数倍），但 recall@5 通常提升一到两成。
- 2026 年 LlamaIndex 与 LangChain 都已把语义分割作为一等选项。
- 适合：主题不可预测切换的非结构化散文、topic 多样的文章；小规模语料（摄入成本可接受）。
- 不适合：结构化文档（结构切分几乎零成本达到同样连贯性）；结果依赖敏感度设置与嵌入模型。

## 层级 / 父子分块（Parent-Child，Small-to-Big）

索引小块（128–256 token）求精确匹配，命中后把父块（512–2048 token）喂给 LLM 求连贯。兼顾小块的精度与大块的上下文——把"匹配"与"回答"两件事解耦。

```
父块：完整章节（1024 token）← 送给 LLM
├── 子块 1（256 token）← 向量检索命中
├── 子块 2（256 token）
└── 子块 3（256 token）
```

- LlamaIndex `HierarchicalNodeParser`、LangChain `ParentDocumentRetriever` 实现此模式。
- **结构化文档生产 RAG 的推荐默认**。几乎任何生产系统都适用，尤其技术文档——精确句子需要周边章节才有用。
- 代价：需支持父子关系的存储；每次回答送更多文本，抬高运行成本；父块可能带入无关文本。
- 若只采用一种进阶策略，就选这个——实现成本适中、提升稳定。

## 怎么选

- homogeneous 散文（文章、报告）→ 语义分割 + 一到两成 overlap。
- 结构化文档（PDF、wiki、docs）→ 结构感知 + 父子检索。
- FAQ、文档 → 父子分块。
- 预算为零、量大 → 滑动窗口或结构感知。

## 参考资料

- Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models：https://arxiv.org/abs/2409.04701
- RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval：https://arxiv.org/abs/2401.18059
