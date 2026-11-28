---
description: "Model comparison, selection tree and input_type pitfalls"
描述: "嵌入模型对比、选择决策树与 input_type 陷阱"
name: "Embedding Model Selection"
名称: "嵌入模型选型"
---

# 嵌入模型选型

> 嵌入模型是向量检索的**质量天花板**——换索引配置很少能让召回提升超过 2–3 个百分点，而换模型可以。别选错。

## 主流模型（2026）

### 商业 API

| 模型 | 维度 | 上下文 | MTEB~ | 特点 |
|---|---|---|---|---|
| text-embedding-3-large (OpenAI) | 3072（可降维） | 8191 | 64.6 | Matryoshka，质量高 |
| text-embedding-3-small (OpenAI) | 1536（可降维） | 8191 | 62.3 | 性价比最优，$0.02/M tok |
| Embed v4 (Cohere) | 1024–1536 | 128k | 66+ | 多模态，int8/binary，Matryoshka |
| voyage-3-large (Voyage) | 1024–2048 | 32k | 67+ | 检索任务领先，代码/技术强 |
| Gemini Embedding (Google) | 3072（可降维） | 长 | 68+ | 多语言榜首 |

### 开源自托管

| 模型 | 维度 | 上下文 | 特点 |
|---|---|---|---|
| BGE-M3 | 1024 | 8192 | 100+ 语言；dense+sparse+late-interaction 三合一 |
| NV-Embed-v2 | 4096 | 32k | MTEB 开源 SOTA |
| multilingual-e5-large-instruct | 1024 | 512 | 最佳免费多语言 |
| gte-Qwen2-7B | 3584 | 32k–131k | 长上下文高质量 |
| nomic-embed-text-v2 | 768 | 8192 | 轻量快速 |
| all-MiniLM-L6-v2 | 384 | 256 | 极轻，CPU 可跑 |

## 选择决策树

```
预算有限？
├─ 是 → 自托管：多语言 → bge-m3 / multilingual-e5；英语 → nomic-embed
└─ 否 → API：追求质量 → voyage-3-large / Cohere v4；性价比 → text-embedding-3-small
需要多语言？→ bge-m3 / Cohere v4 / Gemini Embedding
长文档（>8K）？→ Cohere v4（128k）/ gte-Qwen2（32k）/ voyage-3（32k）
低延迟优先？→ nomic-embed-v2 / text-embedding-3-small
代码检索？→ voyage-code-3（通用文本模型在语法与 API 名上表现差）
```

起步建议：`bge-small-en-v1.5`（免费、快）或 `text-embedding-3-small`（托管、质量优）；只有测出质量差距才升级。

## input_type 不对称（静默的召回杀手）

非对称模型训练时让查询向量与文档向量处在"兼容但不同提示"的空间。两边用同样方式嵌入不会报错，但召回悄悄变差：

```python
# Cohere
co.embed(texts=[q], model="embed-v4", input_type="search_query")
co.embed(texts=[d], model="embed-v4", input_type="search_document")
# Voyage：input_type="query" / "document"
# e5/BGE：文本前缀 "query: " / "passage: "
# OpenAI 3-*：对称，无需 input_type
```

BGE/E5 需要不对称指令前缀（如 "Represent this sentence for searching relevant passages:"），省略会让检索下降 5–15%。指令微调编码器（E5-mistral-7b-instruct、Qwen3-Embedding-8B）用任务描述前缀条件化表征。

## 其他实践

- **内容哈希缓存嵌入**：语料增量更新时不重嵌未变文档。
- **版本化**：嵌入模型变更必须重嵌；过渡期维护两个索引双写。
- ada-002 已无理由用于新系统。
- **升级时机**：黄金集 recall@K 明显低于目标、领域重大切换、或新模型带来可观提升时，先在自有数据重测再升级。text-embedding-3-large 比 small 贵数倍，多数应用只多拿很小一截质量。

## 参考资料

- MTEB: Massive Text Embedding Benchmark：https://arxiv.org/abs/2210.07316
- BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings：https://arxiv.org/abs/2402.03216
- Text Embeddings by Weakly-Supervised Contrastive Pre-training（E5）：https://arxiv.org/abs/2212.03533
