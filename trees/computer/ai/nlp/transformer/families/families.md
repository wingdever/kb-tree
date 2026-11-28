---
description: "Transformer architecture families: encoder-only, decoder-only, encoder-decoder and why decoder-only won"
描述: "Transformer 架构形态族：encoder-only、decoder-only、encoder-decoder 与 decoder-only 的胜出"
name: "Transformer Architecture Families"
名称: "Transformer 架构形态族"
---

# Transformer 架构形态族

2017 原论文是 encoder-decoder：双向编码器读整个输入，因果解码器自回归生成并 cross-attend 编码器。但五年内几乎每个前沿 LLM（GPT-3/4、Claude、Llama、Gemini、Mistral、DeepSeek）都收敛到 **decoder-only**。理解这个收敛，是判断架构选型的基础。

## 三大家族

| 家族 | 注意力 | 训练目标 | 擅长 | 代表模型 |
|---|---|---|---|---|
| **Encoder-only** | 双向 | 掩码语言建模（填空） | 理解：分类、NER、embedding、检索 | BERT、RoBERTa、DeBERTa、E5 |
| **Decoder-only** | 因果（三角） | next-token prediction | 生成、chat、推理、通用任务 | GPT-4、Llama、Mistral、Claude、DeepSeek |
| **Encoder-decoder** | 双向 + 因果 + cross | 去噪/span corruption（seq2seq） | 翻译、摘要、结构化 seq2seq | T5、BART、mT5 |

**最深的差异是掩码**：双向让每个 token 看全序列（能理解、不能生成）；因果让 token i 只看 0..i（天然可生成）。encoder-decoder 两者都有，用 cross-attention 连接。

## 各自的 Block

- **Encoder Block**（BERT、T5 encoder）：`x → LN → MHA(self) → + → LN → FFN → + → out`。双向，无掩码，所有位置看所有位置。
- **Decoder Block**（GPT、T5 decoder）：`x → LN → MHA(masked self) → + → LN → MHA(cross) → + → LN → FFN → + → out`。三个子层，中间的 cross-attention 是 encoder→decoder 唯一的信息通道。纯 decoder-only（GPT）省略 cross-attention，只剩 masked self-attention + FFN。

## 为什么 decoder-only 赢了

1. **架构简单**：单栈、单注意力模式，无 encoder-decoder 管线与 cross-attention 协调。更少活动部件，更易在大规模工程化。
2. **单一目标产生通用能力**："预测下一个 token"是单个无标注目标，规模化时迫使模型学会文本能表达的一切。无需特定任务头、无需单独标注集——训练集就是互联网。
3. **简洁带来可预测的 scaling**：加参数、加数据、加算力，能力稳定提升——整个领域因此敢投入资源。
4. **In-context learning**：一个模型通过 prompt 处理数千任务，无需每任务微调。
5. **吸收其它家族的活**：足够规模后，decoder-only 能做分类、抽实体、摘要、翻译——"摘要"本质就是"继续写一段摘要"。
6. **KV Cache 简洁**：因果掩码让生成步间的 KV 复用简单（一个 cache）；encoder-decoder 要单独 cache cross-attention 的 K/V。

## 但没有淘汰其它家族

- **Encoder-only 仍是 embedding 与分类的主力**：语义搜索、检索、大规模聚类用双向编码器更快更省——每个 RAG 系统都靠 encoder 类模型把文本变成可搜索向量。高吞吐固定分类（如每天 5000 万封邮件标紧急/非紧急）用小微调 encoder 一次前向即可，远省于逐封 prompt 大模型。
- **Encoder-decoder 在固定变换仍占优**：生产翻译（Google）、固定 schema 的结构化变换、长输入短输出摘要——专用小模型胜过通用巨模。T5 把一切任务做成 text-to-text，靠前缀区分任务；span corruption 掩码连续片段（平均 3 token）生成，比 BERT 孤立 mask 更省算力。
- **BERT 训练细节**：MLM 替换 15% token（80% [MASK]、10% 随机、10% 不变），随机化是因为 [MASK] 在微调时不出现；NSP 被 RoBERTa 证明无用并移除。[CLS] 的最终态作整序列摘要用于分类。
- **大 decoder 也能做 embedding**：池化 hidden states 即可，但专用对比训练的 embedding 模型通常更好。

## 2026 新项目默认

**decoder-only**——生态与工具链都 decoder-first。但需要高质量文档向量时，选 encoder-only embedding 模型，别拿生成式大模型干 embedding 的活。

## 参考资料

- Attention Is All You Need（Vaswani et al., 2017）：https://arxiv.org/abs/1706.03762
- BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding：https://arxiv.org/abs/1810.04805
- Language Models are Few-Shot Learners（GPT-3）：https://arxiv.org/abs/2005.14165
- The Llama 3 Herd of Models：https://arxiv.org/abs/2407.21783
