---
description: "LLM Wiki fit, comparison with RAG subdomains and practical tooling"
描述: "LLM Wiki 适用性、与 RAG 各子领域对比及工具实践"
name: "LLM Wiki Practice"
名称: "LLM Wiki 实践"
---

# LLM Wiki 实践

## 为什么有效

- **知识积累**而非每次重置；每个声明都有可见来源与可见编辑历史，更可信。
- **查询更便宜**：中等规模（约 100 篇源）下，维护良好的 `index.md` + 目录路由常胜过搭建完整向量 RAG。
- **可纠正且持久**：你能修正 LLM 的错误并让修正"生根"——RAG 无法做到（下次查询仍从原始片段重新生成）。
- **冲突处理更诚实**：保留冲突双方 + 来源 + 时间，而非合成单一摘要——修正了 AI 摘要"悄悄抹平细微差别"的失败模式。

## 何时用 / 不用

**适用**：>100 份资料、信息随时间变化、需要纠正错误并让修正保持、愿意每周花几小时审阅 diff。

**不适用**：20 条笔记用 Obsidian 搜索就够；想要快速上手、易扩展的场景 RAG 更优（LLM Wiki 启动慢，但查询便宜、更易信任）。

## 与 RAG 各子领域的关系

| 维度 | LLM Wiki 的做法 | 对比 |
|---|---|---|
| 知识组织 | 双向链接 + 结构化页面 | 与 `../../graphrag/` 同源（知识图谱），但 Wiki 是**可读文档**，GraphRAG 是图遍历 |
| 检索 | 关键词 + 目录路由，刻意弱化向量 | 与 `../../retrieval/` 的混合检索路线相悖；部分实现仍用嵌入索引 |
| 增量维护 | 每源触发 10–15 页更新 | 与 `../../../agent/context/` 的 ACE"增量追加优于整体重写"思想一致 |
| 冲突处理 | 保留冲突双方 + 来源 + 时间 | 修正了 AI 摘要抹平细微差别的失败模式 |
| 持久化 | Git 版本控制、不可变 Raw | 与 `../../memory/` 的持久化存储相通 |

一句话：RAG 把决策放在**运行时**（每次查询检索），LLM Wiki 把决策前移到**摄入期**（资料进来就编译）。当循环本身成为成本瓶颈时，后者是值得考虑的替代。

## 工具与实践

- **Obsidian**：编辑器 + 图谱视图；Web Clipper 做网页摄入；Dataview 做结构化查询；Marp 从 Wiki 生成幻灯片。
- **qmd**：本地搜索。
- **Git**：版本控制。
- 社区实现：SwarmVault、WeKnora、Keppi、llmwiki-cli、OmegaWiki、Lore、WeSight（Obsidian 插件）。
- 起步：把 gist 贴进 Claude Code / Codex，共同设计 schema，Obsidian 开在旁边，一次摄入一份源直到流程成形。

## 诚实提醒

LLM Wiki 是**实践而非产品**——没有"注册即用"的按钮，工具生态像 2010 年的 dotfiles 管理，最好的那个就是你愿意持续用的。它要求你投入维护纪律，换来的是可积累、可纠正、可审计的知识资产。

> 相关：三层架构见 `../architecture/`；三操作生命周期见 `../lifecycle/`；作为对照的检索路线见 `../../retrieval/`、`../../graphrag/`。
