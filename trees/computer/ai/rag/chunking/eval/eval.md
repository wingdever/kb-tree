---
description: "Measuring and tuning chunking quality: metrics, golden sets, sweeps and failure diagnosis"
描述: "切块评估与调优：指标、黄金集、参数扫描与失败诊断"
name: "Chunking Evaluation and Tuning"
名称: "切块评估与调优"
---

# 切块评估与调优

切块质量只能由**下游任务表现**衡量，不能靠块看起来是否整齐。最好的切块策略，是让检索器找到正确证据、让生成器产出有依据答案的那一个。"切块是最容易静默失败的环节"这句话要落地，靠的就是本页的方法。

## 核心原则

- **先建评估集，再调参数**。没有 held-out QA 集的 sweep 只是一张无法挑选赢家的表格。
- **分离检索评估与生成评估**。坏答案可能来自检索差、提示弱、缺引用或生成设置，而不只是切块。
- **优化 answer-coverage@k，而非裸 recall@k**：更小的块总会抬高 recall@k（每文档块更多、进 top-k 概率更大），但不代表答案真正可用。
- **保留文档结构**作为元数据（标题、章节路径、页码、来源 URL、时间戳），让检索到的块可被正确解读。

## 评估集长什么样

每行 QA 需要带**来源跨度（source span）**：

| 字段 | 作用 |
|---|---|
| `query` | 真实用户会问的问题 |
| `answer` | 标准答案 |
| `source_doc_id` | 答案所在的文档 |
| `source_span` | 答案在文档中的字符/token 范围 |

没有 `source_span` 就只能算端到端答案准确率，无法单独判断"正确的块是否被检索到"——而这正是切块 sweep 的意义所在。规模：50–200 条（含事实查找、多跳、依赖元数据/章节边界的模糊查询）。合成标签会骗人，尽量人工标注。

## 四个关键指标

| 指标 | 定义 | 为什么重要 |
|---|---|---|
| **recall@k** | source_doc 出现在 top-k 的查询比例 | 粗粒度检索信号，不关心块边界 |
| **answer-coverage@k** | 检索到的块完整包含 source_span 的查询比例 | **边界敏感指标**，答案被切跨块会在此失败——要优化的就是它 |
| **boundary-failure-rate** | source_span 被切到两个检索块的比例 | 直接度量本页要解决的失败模式 |
| **avg-chunks-per-doc** | 该配置下每文档平均块数 | 成本代理（更多块 = 更多嵌入 = 更多钱） |

补充指标：precision@k（检索块中相关的比例，低说明 overlap 过大或混入样板文本）、MRR（第一个相关块的排名）、answer groundedness（答案是否被检索块支撑）、context utilization（提示词中有用证据 vs 重复标题/页脚/重叠内容的比例）、延迟与成本。

块级质量也可用免标注代理：句嵌入的**块内相似度减跨边界相似度**（coherence）、边界是否切在自然语言断点、块熵（低熵多为重复/样板）。

## Sweep 流程（对照实验）

1. **定网格**：块大小 × overlap。常见起点：300/50、500/100、700/100 token；overlap 取 0/10/20/30%。上界由嵌入模型最大输入（如 text-embedding-3-large 8191、voyage-3 32k）与语料 p90 长度共同决定。
2. **每个格子**：用该配置重切语料 → 用固定嵌入模型嵌入 → 建索引 → 对评估集每条查 top-k → 打四个指标。
3. **成本提示**：1000 文档 + 100 查询 + text-embedding-3-large 的默认网格（5 尺寸 × 4 overlap = 20 格）通常 $10–30、30–60 分钟；先告知成本让用户决定是否裁剪。
4. **选赢家**：在可接受成本内 answer-coverage@k 最高的格子。别为了 2 点覆盖提升让嵌入账单翻三倍。
5. **比 splitter**：只在最佳（size, overlap）格子上重跑各 splitter，选胜出的结构感知切分器。
6. **写进配置**：把结论（chunk_size、overlap、splitter、审计日期、最佳 answer-coverage@k）写进切块配置文件注释，防止未来维护者悄悄改回去。

## 失败诊断（按类别看）

每次测试后人工看 5–10 个失败案例，分类驱动调整：

| 现象 | 可能原因 | 调整 |
|---|---|---|
| 相关块从没被检索到 | 边界差、缺同义词元数据、样板文本、嵌入模型不合适 | 改边界、给元数据加同义词、去样板、换嵌入 |
| 块检索到了但答案不完整 | 上下文不足 | 加邻近块、加大 overlap、用父子分层检索 |
| 返回大量近重复块 | overlap 过大、模板重复 | 降 overlap、去重、索引前折叠重复模板 |
| 答案有引用但错 | 生成/提示问题，非切块 | 检查提示与生成设置 |

## 切换嵌入模型要重新调

不同模型的最优 token 区间不同。从适配 512 token 的模型换到适配 8192 的模型，切块策略应随之改变——**换模型必须重跑 sweep**。

## 何时不必上重武器

若问题简单、语料小（几十条），固定切块 +  keywords 搜索就够。**结构化搜索**（早融合、多向量）能否定切块质量的价值，但那属于检索层。

## 参考资料

- BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models：https://arxiv.org/abs/2104.08663
- RAGAS: Automated Evaluation of Retrieval Augmented Generation：https://arxiv.org/abs/2309.15217
