---
description: "RAG Triad, four-layer evaluation and RAGAS"
描述: "RAG Triad、四层评估方案与 RAGAS"
name: "RAG Evaluation"
名称: "RAG 评估"
---

# RAG 评估

不能衡量就无法改进。多数生产 RAG 系统被低估测量——黄金集是 PoC 期手工做的，六个月没更新，语料翻倍、查询分布漂移，没人信面板上的数字。

## RAG Triad（核心三问）

| 指标 | 问什么 |
|---|---|
| **Context Relevance** | 检索到的块相关吗？（Precision / Recall） |
| **Groundedness**（Faithfulness） | 答案的每句话都被检索上下文支撑吗？（无幻觉） |
| **Answer Relevance** | 答案真的回答了用户的问题吗？ |

## 四层最低可行方案

1. **仅检索指标**：在维护的回归集上算 Recall@k、Precision@k、MRR、nDCG；集合至少每季度刷新，代表生产查询分布。
2. **生成质量**：Faithfulness、Answer Relevance，用 LLM-as-judge 并针对人工标注切片校准；RAGAS 已是操作基线。
3. **失败模式目录**：幻觉、过度拒答、过时答案、权限泄露、归因错位——分类、随时间跟踪、驱动具体修复，而非当作无差别的"模型错误"。
4. **生产样本管道**：少量真实流量（通常 0.5–5%）每周回流到回归集，使评估分布跟随生产分布而非历史分布。

## RAGAS 核心算法

- **Faithfulness**：先用 LLM 把答案拆成独立声明，再逐条判断能否从检索上下文推断——暴露"检索到了但没用"或"编造了上下文没有的内容"。
- **Context Precision**：相关文档是否排在更靠前位置，反映召回与精排的整体排序质量。

把这些指标建在 50–200 条黄金查询集上，每次调整嵌入模型、索引参数、重排策略都跑一遍，让选型从凭感觉变有数据支撑。

## 评估工具

- **RAGAS**：无参考 RAG 指标（faithfulness、context precision/recall、answer relevancy），Apache 2.0，事实上的操作基线。
- **Arize Phoenix**：OTel 原生追踪 + 评估，生产监控。
- **DeepEval**：pytest 风格本地评估，50+ 指标。

## Agentic RAG 的评估难题

评估问题从"检索到正确的块了吗？"变成 **"Agent 构造了正确的检索计划了吗？"**——多数 RAG 评估套件还没测好这个。轨迹级评估见 `../../agent/eval/`。

## 常见失败（与评估对应）

- 单向量检索无重排序（2022 vintage，仍在多数企业生产）。
- 黄金集过期、无人维护。
- 数据质量：垃圾进→幻觉出。策展语料、版本化、定期离线检查检索召回漂移。
- 陈旧信息：每块打发布日期与来源标签，检索器可对新鲜度打分。
- **权限泄露**：见 `../prod/` 的 RBAC。

> 相关：Agent 评估的三层与六指标见 `../../agent/eval/`；模型层评测基准见 `../../model/eval/`。
