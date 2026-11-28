---
description: "Transformer architecture knowledge tree: internals, block structure, model families, MoE and DeepSeek-V3"
描述: "Transformer 架构知识树：内部机制、Block 结构、架构形态族、MoE 与 DeepSeek-V3"
name: "Transformer Architecture"
名称: "Transformer 架构"
---

# Transformer 架构

注意力堆叠取代了循环结构，成为当代语言模型的基本构件。2017 年 Vaswani 论文的六个设计决策把单个注意力层变成可堆叠的 Block——此后所有模型（encoder-only 的 BERT、decoder-only 的 GPT、encoder-decoder 的 T5）都继承同一骨架。本主题已拆成 5 个子知识点目录。

## 一句话主线

骨架自 2017 未变，2026 的改进集中在位置编码、归一化、激活、专家化与注意力压缩。

