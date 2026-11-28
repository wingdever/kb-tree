---
description: "Knowledge tree for splitting documents into retrieval units"
描述: "切块策略：八种方法、父子块与上下文增强"
name: "Chunking Strategies"
名称: "切块策略"
---

# 切块策略（Chunking）

切块定义检索单元，选错不会报错，只会让答案变差。方法从固定窗口、语义分割到上下文增强与父子结构，成本与召回差异很大。

块越小匹配越尖、上下文越少；块越大信息越全、噪声越多。不存在通用最优，只能按语料与查询分布扫参数。本主题已拆成 5 个子知识点目录。

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
- 有标题层级的文档先按结构切，再叠父子粒度检索。
- 引用密集长文档 → Contextual / Late；高价值小集合 → Agentic。
绝不从中间切断表格与代码块。
- 生产推荐组合：**Contextual + Parent-Child**（recall@5 90.5%）。

## 一句话主线

从基础方法起步，按文档结构升级到语义/父子，对脱离文档就失去意义的块做上下文增强。

