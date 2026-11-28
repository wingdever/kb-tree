---
description: "Capability benchmark matrix, failure modes and evaluation methodology"
描述: "模型能力基准矩阵、失效模式与评测方法论"
name: "Model Evaluation and Benchmarks"
名称: "模型评测与基准"
---

# M6 模型评测与基准

> 与 Agent 评估（advanced/A1）互补：这里评的是**模型能力**，A1 评的是**Agent 行为与轨迹**。一个高分模型可能是糟糕的 Agent，反之亦然。

## 能力维度 × 测量范式矩阵（2026）

| 能力维度 | 代表指标 | 测量范式 | 2026 状态 |
|---|---|---|---|
| 通用知识 | MMLU / MMLU-Pro | 静态 MCQ | MMLU 饱和（92%+）；Pro 仍有区分度 |
| 专家推理 | GPQA Diamond / HLE / FrontierMath | 博士/研究级静态 | 主力换代指标；GPQA Diamond 六成五到七成 |
| 数学推理 | GSM8K / MATH / AIME | CoT 评分 | GSM8K 饱和；AIME 仍有区分度 |
| 编码 | HumanEval / SWE-bench Verified | pass@1 / 轨迹 | HumanEval 饱和且污染；SWE-bench 是主战场 |
| 对话偏好 | Chatbot Arena Elo / MT-Bench / AlpacaEval | 人类盲选 / LLM-as-Judge | Arena 持续有效；后两者饱和 |
| 指令遵循 | IFEval / IFBench | 可验证约束 | 顶部接近饱和（96%+） |
| 智能体执行 | τ-bench / SWE-bench / GAIA / OSWorld | 多步轨迹评测 | 区分度最高；τ-bench ~65–75% |
| 长上下文 | RULER / NIAH / NoLiMa | 合成任务 | 有效上下文与标称差 30–60 分 |
| 多模态 | MMMU / MMMU-Pro | 学科 MCQ | 顶部 ~86–87%，未饱和 |
| 安全与真实性 | TruthfulQA / HarmBench / BBQ | 静态 / 红队 | 覆盖严重不足，无 Tier A 基准 |

越靠下的维度，越接近 2026 年真正拉开差距的地方。知识类静态基准已无法区分前沿模型；智能体执行、长上下文、多模态仍在产出有统计意义的分差。

## 六大类基准详解

### 知识与推理

- **MMLU**：57 学科、14042 道 MCQ，锚定早期 scaling  debate。2026 前沿模型 88–92%，天花板接近标签噪声——1 分差距换种提示格式就不复存在。用来**排除坏候选**，而非给前沿排名。
- **MMLU-Pro**：更难的抗污染变体，但 2026 也接近饱和（Gemini 3 Pro ~90.1%、Claude Opus 4.5 ~89.5%）。
- **GPQA Diamond**：198 道生物/物理/化学博士级题，设计为"搜索也做不出"——有联网的非专家仅 ~34%，博士专家 ~65%。抗污染黄金标准。
- **HLE（Humanity's Last Exam）**：专家级知识，~35%，远未饱和。
- **ARC-AGI-2**：测流体智力（抽象模式），top ~85% 但人类平均 60%。
- **TruthfulQA**：真实性。

### 数学

GSM8K（8500 道小学数学）、MATH（12500 竞赛题）大多饱和。AIME-25 是 post-cutoff 压力测试仍有区分度。FrontierMath 最难、抗记忆。**注意**：GSM-Identity 研究把数值换成数学等价但不直观的表达式后，数学专用模型保持性能、通用模型显著下降——揭示"形式记忆 vs 语义理解"困境。

### 编码

- **HumanEval**（164 手写 Python 题）、**MBPP**（974 入门题）：饱和且覆盖函数补全而非工程。
- **SWE-bench**：2294 个真实 GitHub issue（12 个 Python 仓库），按补丁是否通过项目测试集打分。**SWE-bench Verified** 是人工筛可解的 500 题子集。2026 年 2 月 OpenAI 宣布弃用 Verified（测试设计缺陷 + 污染）。SWE-bench Pro 更难、更贴近生产。
- **LiveCodeBench**：在已知训练截止后出新题，抗污染，更可信的编码信号。

### 智能体 / 工具使用

- **BFCL（Berkeley Function Calling Leaderboard V4）**：单轮/多轮/并行/agentic 场景的函数调用准确率，附带成本与延迟。
- **τ-bench / τ²-bench**：模拟航空/零售多步工具使用、对话接地、失败恢复；τ² 为更难后继，双控制设置用 pass^k 衡量可靠性。
- **GAIA / OSWorld / WebArena / Terminal-Bench**：真实环境任务。

### 长上下文

NIAH（大海捞针）、RULER、LongBench v2、U-NIAH。关键发现：**有效上下文与标称上下文存在 30–60 分差距**——标称 128K 不代表真能用好 128K。

### 多模态

MMMU / MMMU-Pro（大学学科 MCQ）、MathVista、ChartQA、DocVQA、VideoMME。

## 四种失效模式（读排行榜前先记住）

1. **饱和（Saturation）**：SOTA 持续 >90% 时基准失去区分度。MMLU 2023 即饱和才催生 MMLU-Pro，后者 2026 也逼近饱和。
2. **污染（Contamination）**：基准公开，解答进入训练数据，下一代模型"分更高"部分因为见过答案。OpenAI 已确认 SWE-bench Verified 在所有前沿模型上的训练数据泄漏。
3. **奖励黑客（Reward hacking）**：Agent 优化被测量的东西。Berkeley "How We Broke Top AI Agent Benchmarks" 显示几乎每个主流 Agent 基准都能靠利用环境 bug、文件系统技巧、成功检测启发式刷到近 100%，而没真正完成任务。
4. **代理污染（Contamination-by-proxy）**：基准未逐字进训练数据，但结构相似内容进了。见过 2015–2023 所有竞赛题的模型能靠识别模板"解"LeetCode 式基准。

## 怎么读一个分数

- 它是**某项特定能力的上界**：高 MMLU-Pro 分不表示模型"聪明"，只表示它会答 MMLU-Pro 格式的 MCQ。
- 它是**训练体制的证据**：特定基准响应特定训练投入（RLHF、长上下文、工具微调）。高分 = 该能力被投入过。
- 它是**污染敏感的代理**：越新的基准通常越可信；临近饱和的老基准本质是记忆测试。
- 它**不是面向用户的指标**：LMArena 偏好分追踪用户感受，可能与基准表现大相径庭。

## 评测方法论

- **LMArena（Chatbot Arena）**：匿名用户成对偏好投票，拟合 Elo/Bradley-Terry。最强的公开偏好信号、较难游戏（投票持续产生）。局限：匿名、短上下文。
- **LLM-as-Judge**：用模型按量表打分，灵活但有长度、位置、自我偏好偏差且非确定——适合作留出样本离线打分，不适合逐轮打标。
- **pass@k**：多次尝试至少一次成功的概率，衡量可靠性（τ²-bench 用 pass^k）。
- **Golden set**：带标签的精选集（50–200 条起），每次改嵌入/索引/重排都跑一遍，让选型从凭感觉变有数据支撑。
- **污染检测**：post-cutoff 题、变体测试（如 GSM-Identity）。

## 公开基准 vs 私有评测

> 公开基准塑造候选名单，私有评测决定上线哪个。

公开基准用于筛掉不靠谱候选；真正决定发布的是在你自己的流量、你自己的 rubric 上的评测。生产 RAG 的最低可行评测四层：检索指标 + 生成质量 + 失败模式目录 + 生产样本回流。

## 参考资料

- MMLU: Measuring Massive Multitask Language Understanding：https://arxiv.org/abs/2009.03300
- HELM: Holistic Evaluation of Language Models：https://arxiv.org/abs/2211.09110
- GPQA: A Graduate-Level Google-Proof Q&A Benchmark：https://arxiv.org/abs/2311.12022
- HumanEval: Evaluating Large Language Models Trained on Code：https://arxiv.org/abs/2107.03374
