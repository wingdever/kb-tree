---
description: "LLM Wiki: compile knowledge once into a persistent, self-maintained Markdown wiki as an alternative to RAG"
描述: "LLM Wiki：把知识一次性编译成持久自维护的 Markdown Wiki，作为 RAG 的替代路线"
name: "LLM Wiki"
名称: "LLM Wiki"
---

# LLM Wiki：把知识"编译"成持续维护的 Wiki

LLM Wiki 是 2026 年 4 月提出的模式：让 LLM 把原始资料**一次性编译**成一份持久化、结构化、持续更新的 Markdown Wiki，之后所有问答都基于这本编译好的 Wiki，而不是每次从原始文档重新检索拼凑。它是 RAG 的一种**替代/演进路线**——不是检索技术，而是一套知识组织范式。

本主题已拆成 3 个子知识点目录。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `architecture/` | 核心理念（解释器 vs 编译器）、三层架构 Raw/Wiki/Schema |
| `lifecycle/` | 三操作 Ingest/Query/Lint、六类查询模板 |
| `practice/` | 为什么有效/何时用、与 RAG 各子领域关系、工具与实践 |

## 核心理念一句话

| 类比 | RAG | LLM Wiki |
|---|---|---|
| 模式 | 解释器（JIT） | 编译器（AOT） |
| 行为 | 每次查询重新解析、检索、综合 | 资料进来先编译好，查询直接用成品 |
| 比喻 | 考试前一晚翻遍课本找知识点 | 平时整理成学霸笔记，考试直接看笔记 |

经典 RAG 的问题：模型"每个问题都从零重新发现知识，没有积累"。一句口诀：**Obsidian 是 IDE，LLM 是程序员，Wiki 是代码库**（wiki 就是编译产物）。思维源头是 1945 年的 Memex——带联想路径的个人知识存储。

## 一句话主线

理解 `architecture/` 的三层架构（Raw 不可变 → Wiki 由 LLM 维护 → Schema 规则层）→ 用 `lifecycle/` 的 Ingest/Query/Lint 循环让知识复利 → 对照 `practice/` 判断是否适合你的场景。核心承诺：**知识积累而非每次重置，每个声明有可见来源与编辑历史，错误可纠正且能"生根"**。

## 与 RAG 树的关系

它与 `../graphrag/` 同源（知识图谱）但 Wiki 是**可读文档**、GraphRAG 是图遍历；检索路线上刻意弱化向量（与 `../retrieval/` 相悖）；增量维护与 `../../agent/context/` 的 ACE"增量追加优于整体重写"一致；持久化与 `../memory/` 相通。

> 诚实提醒：LLM Wiki 是**实践而非产品**——没有"注册即用"的按钮，工具生态像 2010 年的 dotfiles 管理，最好用的那个就是你愿意持续用的。
