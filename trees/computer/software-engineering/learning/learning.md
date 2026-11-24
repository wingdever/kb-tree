---
description: "Open-source books and systematic tutorials for learning software engineering"
描述: "软件工程的开源图书与系统教程"
name: "Software Engineering Learning Resources"
名称: "软件工程学习资源"
---

# 软件工程学习资源

只收系统成书、可在线读的资源。书单类仓库单独标注（它们指向别处的书，本身不是书）。star 数只作量级参考。

## 开源书与系统教程

| 仓库 / 站点 | 内容 | 在线 / 许可 |
|---|---|---|
| `se-edu/se-book` | 《Software Engineering for Self-Directed Learners》在线书：需求、设计、UML、OOP、测试、重构、Git、质量、团队协作、项目管理，章节可按路径学习 | GitHub 仓库在线读；许可未在核对中确认，不擅自标注 |
| `Vonng/ddia` | 《设计数据密集型应用》DDIA 中文翻译，第二版 14 章已全上线并持续校订，第一版另在 `/v1` | `ddia.vonng.com`；CC BY 4.0，但译者声明仅供学习研究、不用于公开分发或商用 |
| `donnemartin/system-design-primer` | 大规模系统设计资源索引 + 面试真题与示例解答 + Anki 抽认卡；有简体中文 README | GitHub 仓库；许可证未在核对中确认，不擅自标注 |
| `Admol/SystemDesign` | Alex Xu《System Design Interview》两卷中文翻译，卷一 15 章、卷二部分完成，进度用 checkbox 公开 | GitBook 在线；BSD-3-Clause，译者声明非商用 |
| 《凤凰架构》（周志明） | 中文原创架构书，作者官网提供 PDF，免费开源 | 作者站点提供 PDF |

## 书单类仓库（不是书本身）

| 仓库 | 指向什么 |
|---|---|
| `ZachGoldberg/Startup-CTO-Handbook` | 创业公司 CTO 的管理与技术手册，开源 |
| `jesselpalmer/the-engineering-managers-booklist` | 面向工程经理的书单 |
| `wambugucoder/SOFTWARE-ENGINEERING-BOOKS` | 软件工程书籍集合 |

## 怎么配本树读

但**示例解用来对照校准，不用来背诵**。

> 翻译类仓库的许可与声明各不相同：有的 CC BY 4.0 但要求非商用，有的 BSD-3-Clause，有的未声明。用于内训或再分发前按各自仓库核对，不要默认「开源即可商用」。

## 阅读路线

书与树节点交替推进，每阶段先跑通再扩展，并有可验收产出。

| 阶段 | 读什么 | 树节点 | 交付物 |
|---|---|---|---|
| 1. 全景与生命周期 | `se-edu/se-book` 的需求 → 设计 → 测试 → 部署路径 || 把一个真实小项目按阶段切开，写出每阶段的输入/输出 |
| 2. 架构与质量 | `Vonng/ddia` 第 1–3、6–8 章（权衡、数据模型、复制、分片、事务） || 用质量属性场景表描述一个系统的架构取舍，为关键模块写契约测试 |
| 3. 系统设计训练 | `donnemartin/system-design-primer`、`Admol/SystemDesign` 任选一题 || 限时做一道系统设计题，对照示例解校准，不背诵 |
| 4. 交付与运维 | se-book 的测试 / 重构 / Git 章节 || 给项目接上 CI、可观测性面板与回滚预案 |
| 5. 现代工程 | — || 用规格驱动方式重做一个小功能，记录规格与实现的偏差 |

主线：**生命周期定框架 → DDIA 定系统直觉 → 设计题练取舍 → 交付闭环 → 再接 AI 协作方式**。

## 一句话主线

**软件工程的开源学习资源分三类：完整在线书（se-book、DDIA 译本）、系统设计面试资源（primer、SystemDesign）、书单索引；按本树的生命周期阶段对照读，比按 star 排序更有效。**

