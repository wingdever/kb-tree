---
description: "Transformer architecture knowledge tree: internals, block structure, model families, MoE and DeepSeek-V3"
描述: "Transformer 架构知识树：内部机制、Block 结构、架构形态族、MoE 与 DeepSeek-V3"
name: "Transformer Architecture"
名称: "Transformer 架构"
---

# Transformer 架构

Transformer 是现代NLP与大模型的基石架构。2017 年 Vaswani 论文的六个设计决策把单个注意力层变成可堆叠的 Block——此后所有模型（encoder-only 的 BERT、decoder-only 的 GPT、encoder-decoder 的 T5）都继承同一骨架。本主题已拆成 5 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `internals/` | 自注意力矩阵六步、位置编码（正弦/RoPE）、Prefill/Decode、KV Cache、复杂度、注意力变体 |
| `block/` | Block 结构：残差、LayerNorm/RMSNorm、FFN/SwiGLU、pre-norm vs post-norm、参数量 |
| `families/` | 架构形态族：encoder-only / decoder-only / encoder-decoder，为什么 decoder-only 胜出 |
| `moe/` | 混合专家：router、top-k、负载均衡、细粒度/共享专家、专家并行 |
| `deepseek-v3/` | 架构案例：MLA、DeepSeekMoE、MTP、DualPipe、FP8 |

## 一句话主线

先看 `internals/` 搞清注意力与两阶段推理的数学；再看 `block/` 理解一个 Block 由什么构成、如何堆到百层；`families/` 讲三种架构形态的取舍与 decoder-only 的胜利；`moe/` 讲稀疏条件激活如何解耦容量与算力；`deepseek-v3/` 把这些部件组装成一个真实的 671B 生产架构。骨架自 2017 未变，2026 的改进集中在位置编码、归一化、激活、专家化与注意力压缩。

> 相关：推理引擎与量化见 `../../model/inference/`；预训练见 `../../model/pretrain/`；分词见 `../../model/tokenizer/`；Embedding 见 `../../rag/embedding/`。
