---
description: "Language model families: n-gram, Markov, RNN and the BERT/GPT/XLNet/RoBERTa landscape"
描述: "语言模型谱系：n-gram、马尔可夫、RNN 与 BERT/GPT/XLNet/RoBERTa"
name: "Language Model Families"
名称: "语言模型谱系"
---

# 语言模型谱系

从统计语言模型到预训练 Transformer，理解演进有助于判断"什么时候该用哪一类"。

## 小模型（统计与早期神经）

### n-gram 模型

基于统计语言模型：把文本按字节做大小为 N 的滑动窗口，形成长度 N 的字节片段（gram）序列。统计所有 gram 出现频度，按阈值过滤形成关键 gram 列表——即文本的向量特征空间，每种 gram 是一个特征维度。

### 马尔可夫模型（Markov Model）

统计模型，广泛用于语音识别、词性自动标注、音字转换、概率文法等 NLP 领域。复杂语音识别问题通过**隐含马尔可夫模型（HMM）**可非常简单地表述、解决，长期被视为实现快速精确语音识别的最成功方法。

### RNN（循环神经网络）

引入循环结构处理序列，是 Transformer 之前的主流。长距离依赖建模弱（梯度消失/爆炸），被 Transformer 取代。

## 大模型（预训练 Transformer）

### BERT（Bidirectional Encoder Representations from Transformers）

Google 2018 提出的深度学习 NLP 模型，用于文本分类、问答、语言理解。基于 Transformer 编码器，用**掩码语言建模（MLM）+ 下一句预测（NSP）**联合训练——双向上下文。适合理解类任务。

### GPT-3（Generative Pre-trained Transformer 3）

OpenAI 的自回归语言模型，用深度学习生成类人文本。第三代 GPT，45TB 文本训练（书籍、文章、网页），能做问答、摘要、翻译。自回归 = 单向、逐 token 生成。

### XLNet

Google AI Language 提出，改进问答、自然语言推理、文本分类。基于 Transformer，结合自注意力与循环以更好捕捉长距离依赖——排列语言建模（permutation LM）。

### RoBERTa

Facebook AI 基于 BERT 的优化版：以自监督方式利用无监督数据，对超参数调优更鲁棒、处理更长序列。去掉 NSP、动态掩码、更大 batch。

## 谱系对比要点

| 模型 | 架构 | 训练目标 | 适合 |
|---|---|---|---|
| n-gram / HMM | 统计 | 频数/转移概率 | 资源受限、可解释基线 |
| RNN | 循环 | next-token | 序列（已被取代） |
| BERT | Transformer Encoder | MLM + NSP | 理解、分类、NER |
| GPT 系列 | Transformer Decoder | 自回归 LM | 生成、开放任务 |
| XLNet | Transformer-XL | 排列 LM | 长距离依赖 |
| RoBERTa | Transformer Encoder | 改进 MLM | 鲁棒理解 |

现代主流 decoder-only LLM（Llama、Qwen、GPT-4+）的架构深潜见 `../transformer/`，预训练见 `../../model/pretrain/`，微调见 `../../model/peft/`。

> 相关：Transformer 架构与注意力见 `../transformer/`；预训练与 Scaling Law 见 `../../model/pretrain/`；模型蒸馏见 `../../model/distill/`；评测见 `../../model/eval/`。
