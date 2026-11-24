---
description: "Contrastive learning, hard negatives, MTEB and failure modes"
描述: "对比学习、困难负例挖掘、MTEB 评估与失败模式"
name: "Embedding Training and Evaluation"
名称: "嵌入模型训练与评估"
---

# 嵌入模型的训练与评估

## 训练目标（决定向量空间的几何）

嵌入空间的几何完全由训练目标决定。主要范式：

| 范式 | 做法 | 代表 |
|---|---|---|
| **预测式** | word2vec CBOW/skip-gram 预测上下文；LM 的 next-token 副产品 | word2vec、GPT/T5 |
| **MLM** | 掩码语言建模，双向 transformer 重建被掩 token | BERT/RoBERTa |
| **对比学习**（主流） | 拉近正样本、推远负样本，InfoNCE loss | BGE、E5、GTE、text-embedding-3 |
| **蒸馏** | cross-encoder 教师 → bi-encoder 学生，学教师的相似度分数 | 多种生产系统 |
| **生成式** | decoder-only 最后 token 隐状态作句向量 | E5-Mistral-7B、GTE-Qwen |
| **跨模态对齐** | 图文等配对对比学习 | CLIP、SigLIP、Gemini |

## InfoNCE loss（对比学习核心）

把批内其他样本当负样本，最大化正对互信息：

```
L = -log( exp(sim(q, p⁺)/τ) / Σ_j exp(sim(q, p_j)/τ) )
```

- τ 温度系数控制分布锐度。可学习 τ 比固定 τ 更有效。
- 正对构造定义模型学到何种"相似"：复述/NLI 蕴含/翻译等价用于句相似度；图文配对用于 CLIP；函数体与文档串用于 CodeBERT。
- SimCSE（Gao et al. 2021）：用 dropout 作为最小数据增强从单句造正对 + 批内负样本，无需标注即达 SOTA。

## 三阶段训练范式（现代 Embedding 模型）

1. **弱监督预训练**：(query, passage) 对（网络爬取/合成），大规模 InfoNCE，数百万~数亿对。
2. **有监督微调**：高质量标注（MS MARCO、NLI），加入**困难负样本挖掘**，更小批次精细对比。
3. **对比指令微调**：加任务描述前缀，区分检索/聚类/分类等下游任务表征需求。

## 困难负样本挖掘（Hard Negative Mining）

随机负样本太简单，模型会"偷懒"。困难负样本与锚点语义相似但不是正样本，显著提升区分力：

- 用 BM25 或较弱的嵌入模型检索出"差一点就对"的近 miss 负例。
- 朴素挖掘可能引入**假负例**（实际相关却标为负）——U-MARVEL 的策略：算所有候选相似度，过滤掉过高的（如 >0.7）避免假负例，再选 top-k 最难负例；与批内负例混合防坍塌。

这是 BGE/E5/Cohere 3 显著超过 ada-002 的主因。

## 蒸馏：reranker → embedding

用高精度但慢的 cross-encoder 教师，把知识蒸馏到快的 bi-encoder 学生，让学生近似教师的相似度分数同时保持独立编码的速度优势。目标是用单阶段嵌入达到 recall-then-rerank 的质量。

## MTEB 与评估

- **MTEB（Massive Text Embedding Benchmark）**：跨检索、分类、聚类等任务的标准基准。模型分数/价格随时间快速变化（如 NV-Embed-v2 曾 72.31、Gemini embedding 多语言 68.32、Qwen3-Embedding-8B 70.6）。
- **MTEB 不能替代自有数据评估**：它是跨任务平均且偏英语。高两分的模型在你的法律语料/代码/客服工单上可能更差。把榜单前 3–4 名当候选，再用自己的黄金集评估——那个数字才是唯一决定因素。
- 领域专用模型常在特定域超过总体排名更高的通用模型。
- 用**检索专属指标**（recall@k、MRR）在嵌入阶段单独评估，与端到端生成质量分开——详见 `../../eval/`。

## 失败模式

- **OOD 输入**：领域外查询可能因表层词重叠而几何误导，靠近无关内容。
- **语义粒度错配**：文章级/章节级/句子级需不同粒度，文档级模型可能检索不到精确段落——催生多粒度混合架构（见 `../../chunking/`）。
- **级联失败**：嵌入质量差 → 检索到边缘相关文档 → LLM 基于错误 grounding 自信答错；嵌入失败对终端用户不可见（输出流畅但错误）。
- **嵌入空间漂移**：模型更新需重嵌全部内容保持几何一致；过渡期查询用新嵌入对比旧文档嵌入会不稳定。热切换重索引与版本化嵌入空间是生产工程重点。

## 规模化规律

嵌入模型呈一致 scaling 行为：更大模型/更多数据/更长训练持续提升 MTEB（类似生成模型的 power law）。Qwen3-Embedding 显示 8B 模型（MTEB 70.6）显著高于同数据训练的 1B 模型。

> 相关：选型见 `../models/`；Matryoshka 降维见 `../matryoshka/`。
