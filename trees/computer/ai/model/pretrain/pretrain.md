---
description: "Pretraining LLMs from scratch: data pipelines, mixture and curriculum, scaling laws and Chinchilla, evaluation"
描述: "从零预训练 LLM：数据管道、混合与课程、Scaling Law 与 Chinchilla、预训练评估"
name: "LLM Pretraining"
名称: "大模型预训练"
---

# 大模型预训练（Pretraining）

预训练是从零训练基座模型——把海量文本压缩进参数，建立语言与世界知识的基础。它和数据、算力、并行策略强绑定。

> 预训练是一笔" upfront 赌注"：需要预先承诺算力，耗时数周数月。这就是为什么微调现有模型成为主流——预训练成本只付一次，摊薄到数千下游任务。

## 数据管道

预训练语料来源：Common Crawl（PB 级、噪声大）、C4（清洗版约 750GB）、FineWeb、 Books1/2、Wikipedia、The Stack v2（代码，67.5TB）、The Pile（825GB、22 子集）、RedPajama、Common Pile v0.1（8TB、公有领域/开放许可）。

流水线（相对体积示意）：

```
Crawl → Clean → Deduplicate → Filter → Check contamination → Tokenize & pack
100%    78%       45%           30%          29%               29%
```

1. **提取与清洗**：HTML 提取纯文本、修 Unicode、语言识别、去样板（页眉页脚导航）。
2. **质量过滤**：启发式规则（句长、标点比例）或模型打分过滤低质文本。
3. **去重**：文档级与片段级，防"死记硬背"、提高泛化。
4. **污染检查**：验证 benchmark 评测集未泄漏进训练数据（网络爬抓取包含公开基准的问答副本，训练上去会让评测分数失效）——这与经典 ML 的数据泄漏等价。
5. **Tokenize & Pack**：把清洗后文本转 token ID，再把多文档背靠背打包成定长训练序列（文档间加分隔符），避免 padding token 浪费算力。
6. **隐私与安全**：移除 PII、有害内容。

## 数据混合与课程

- 语料按来源**特定比例混合**（网页、代码、书籍、论文、多语言），混合比例可测量地影响下游能力——如加入代码数据会提升通用推理，不只是代码能力。
- **数据课程（curriculum）**：训练过程中改变混合比例（如后期上采样高质量数据），而非全程单一固定分布。
- MoE 时代新问题：20:1 比例对总参数还是激活参数？早期证据倾向激活参数，仍在争论。

## Scaling Law 与 Chinchilla

**基础关系**（Kaplan et al. 2020 / Hoffmann et al. 2022，至今仍准）：loss 随参数 N、数据 D、算力 C 呈幂律下降，训练算力近似：

```
C ≈ 6 · N · D        （每参数每 token 约 6 FLOPs：前向+反向+更新）
```

**Chinchilla 结果**：固定算力下，模型规模与训练 token 应**等比例扩展**，约 **20 tokens/parameter**。Chinchilla（70B/1.4T）用与 Gopher（280B）相同算力却胜出——旧做法造了太大、训练不足的模型。同样算力下，compute-optimal 的小模型+多数据稳定胜过大模型+少数据。

工作流：定预算（GPU 数×小时×峰值 FLOPS）→ 定模型规模 → 目标 token = 参数×20 → 审计唯一 token 是否够 → 先训小代理模型看 loss 曲线（很快平=数据受限，持续降=可上更大模型）。

**局限与 2026 演进**：

- Chinchilla 的 20:1 是启发式，实际在 15:1–25:1 间漂移（数据质量高可少些、冗余多需多些），且**只适用于预训练阶段**——指令微调/RLHF 的规则不同（常 4:1–5:1，基础模型有未用容量，5 万高质量样本就能微调）。
- **训练最优 ≠ 推理最优**：训练是一次性成本，推理主导总拥有成本。Chinchilla 优化了错误目标——2026 实验室普遍**过度训练**换推理经济：推理最优比例达 100–2000 tokens/parameter。Epoch AI：开放权重模型的平均 token/参数从 2022 的 10 升到 2025 的 300（每年约三倍），极端如 Qwen3-0.6B 达 60,000:1。
- 新前沿：推理最优过度训练、test-time compute scaling、architecture-conditional laws（ICLR 2026 某论文报告推理吞吐明显提升）、post-training scaling（数据重复到几个 epoch 仍保留大部分唯一数据效果）。
- **数据墙**：Epoch AI 估计约 300 万亿 token 的高质量公开人类文本，预计 2026–2032 间耗尽。

## 从零预训练实操

1. **先定位**：数据是瓶颈不是模型——大多数团队不该从零预训练，微调/继续预训练更划算。
2. **定规模**：受显存约束，先小后大。
3. **建数据管道**：上述六步，版本化、可重试（解析器升级要能重处理，OCR 失败按页范围重试）。
4. **先跑代理实验**：小规模验证 loss 曲线与配比，再放大。
5. **算力现实**：C≈6ND 是理论值，真实 FLOPs 因通信同步约 0.5–0.7×；现代 H100/H200 集群可达 600+ TFLOPs。超 10²¹ FLOPs 后偏向更大模型（对指令微调模型），base 模型仍等比例。

## 预训练评估

主要看**训练 loss 曲线**与 held-out 的**困惑度（perplexity = e^cross-entropy loss**，越低越好，衡量模型对留出文本多"惊讶"），加上定期在标准 benchmark 上跑，跟踪能力涌现（而非只看终点）。监控数据管道各阶段损耗、重复率、污染检查。

## 参考资料

- Scaling Laws for Neural Language Models（Kaplan et al., 2020）：https://arxiv.org/abs/2001.08361
- Training Compute-Optimal Large Language Models（Chinchilla）：https://arxiv.org/abs/2203.15556
- Language Models are Few-Shot Learners（GPT-3）：https://arxiv.org/abs/2005.14165
