---
description: "NLP knowledge tree: transformer internals, intent recognition, information structures, language models and applications"
描述: "NLP 知识树：Transformer 内部机制、意图识别、信息结构、语言模型与应用"
name: "Natural Language Processing"
名称: "自然语言处理"
---

# NLP 知识树

自然语言处理是让机器理解与生成语言的技术领域。本目录覆盖 Transformer 内部机制、意图识别、世界信息结构、语言模型谱系与典型应用。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `transformer/` | 已展开为子树：internals、block、families、moe、deepseek-v3（入口见 `transformer/transformer.md`） |
| `intent/` | 意图识别、槽位填充、歧义澄清、分层 pipeline、意图生成 |
| `information/` | 世界信息结构十表、分层、RDF 三元组（与本体论强相关） |
| `models/` | 小模型（n-gram/马尔可夫/RNN）与大模型谱系（BERT/GPT-3/XLNet/RoBERTa） |
| `applications/` | NLP 任务分类、数据集来源、文本预处理、spaCy |
| `machine-translation/` | 机器翻译：四代演进、seq2seq/attention/Transformer、多语言数据、BLEU/COMET 评测、LLM 混合系统 |

## 建议阅读顺序

基础：`models/`（语言模型演进）→ `transformer/`（核心架构）。工程：`applications/`（任务与预处理）→ `intent/`（Agent 前置能力）。专项：`machine-translation/`（Transformer 的出生地）。理论：`information/`（世界建模与本体）。

## 与其他领域的关系

Transformer 的推理优化（KV Cache、FlashAttention、GQA）在 `../model/inference/` 有工程视角；意图识别是 Agent 路由的基础，见 `../agent/multi/design/`；信息结构与本体论见 `../rag/graphrag/ontology/`；词嵌入与分词见 `../rag/embedding/` 与 `../model/tokenizer/`。
