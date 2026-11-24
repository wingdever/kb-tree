---
description: "Knowledge tree for splitting documents into retrieval units"
描述: "切块策略：八种方法、父子块与上下文增强"
name: "Chunking Strategies"
名称: "切块策略"
---

# 切块策略（Chunking）

切块是 RAG 管道中最容易"静默失败"的环节——它决定的检索单元，对答案质量的影响超过几乎任何其他参数。多数团队选一个默认配置就再也不回头看。

核心权衡：**小块检索精确但缺上下文；大块保留上下文但匹配不准**。没有通用最佳块大小。本主题已拆成 5 个子知识点目录。

## 八种方法总成本对照（每 1000 文档）

| 方法 | Recall@5 | 成本 | 索引延迟 | 适用 |
|---|---|---|---|---|
| Semantic | 83.5% | $0.01 | ~2s/doc | 主题切换的非结构化散文 |
| Agentic | 85.8% | $2.00 | ~30s/doc | 高价值关键文档 |
| Late (Jina) | 85.7% | $0.01 | ~3s/doc | 引用密集长文档 |
| **Contextual** | 88.2% | $0.50 | ~15s/doc（最佳 ROI） | 通用首选 |
| Parent-child | 84.1% | $0.01 | ~1s/doc | FAQ、结构化文档 |
| Sliding window | 79.2% | $0.00 | ~0.1s/doc | 量大、预算为零 |
| Structure-aware | 82.8% | $0.00 | ~0.5s/doc | 有标题/章节结构 |
| Propositions | 86.3% | $1.50 | ~20s/doc | 事实核查、最大精度 |

## 怎么选（速查）

- 同质散文 → 语义分割 + 10–15% overlap。
- 结构化文档（PDF、wiki、docs）→ 结构感知 + 父子检索。
- 引用密集长文档 → Contextual / Late；高价值小集合 → Agentic。
绝不从中间切断表格与代码块。
- 生产推荐组合：**Contextual + Parent-Child**（recall@5 90.5%）。

## 一句话主线

从基础方法起步，按文档结构升级到语义/父子，对脱离文档就失去意义的块做上下文增强。

