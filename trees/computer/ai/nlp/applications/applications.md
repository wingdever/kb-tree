---
description: "NLP application tasks, dataset sources, text preprocessing pipeline and spaCy"
描述: "NLP 应用任务、数据集来源、文本预处理流水线与 spaCy"
name: "NLP Applications and Preprocessing"
名称: "NLP 应用与预处理"
---

# NLP 应用与预处理

## 任务分类

**分类与识别（classification / recognition）**：

- 文本分类：意图分类、新闻标题分类
- Fraud Detection & Prevention：流氓信件与欺诈信息检测
- NER（Named Entity Recognition）：命名实体识别

**生成（generate）**：

- Chatbots、虚拟助手、对话式 AI
- 摘要生成
- 数据注释（Data Annotation）
- 专家系统问答
- 推荐系统
- 代码生成
- 文档处理

## 数据集来源

Kaggle、Google Dataset Search、Hugging Face、Data.gov、Wikipedia database。

## 文本预处理

基础操作：lowercase（字母小写化）、removing stop words（清除停用词）、tokenizing（文本转 token 序列）、word embedding（词向量）。

九项功能：

1. 分句（sentencizer）
2. 分词（Tokenization）
3. 词性标注（POS tagging）
4. 识别停用词（Stop words）
5. 命名实体识别（NER）
6. 依存分析（Dependency Parsing）
7. 词性还原（Lemmatization）
8. 提取名词短语（Noun Chunks）
9. 指代消解（Coreference Resolution）

**spaCy**：文本预处理库，`pip install spacy`，`python -m spacy download en`（英文）/ `de`（德文）。

## 典型模型

Transformer 是复杂 NLP 应用的常见选择：Google BERT、OpenAI GPT-3。

## 与 RAG 预处理的关系

这里的文本预处理与 RAG 摄入阶段的清洗一脉相承，但目标不同：NLP 预处理为特征工程与模型输入，RAG 预处理为检索单元的边界与元数据。分句/分词质量同样决定下游效果。

## 参考资料

- Speech and Language Processing（Jurafsky & Martin, 3rd ed.）：https://web.stanford.edu/~jurafsky/slp3/
- A Survey of Large Language Models：https://arxiv.org/abs/2303.18223
