---
description: "LLM Wiki three-layer architecture: Raw Sources, LLM-maintained Wiki and the Schema rule layer"
描述: "LLM Wiki 三层架构：原始素材层、LLM 维护的知识库层与规则层"
name: "LLM Wiki Architecture"
名称: "LLM Wiki 三层架构"
---

# LLM Wiki 三层架构

LLM Wiki 的全部结构都是纯文本、Git 可版本控制的三层。理解三层的职责边界，是理解这个模式的关键。

## 第一层：Raw Sources（原始素材层，`raw/`）

- 所有原始文件：论文、PDF、网页剪藏、代码、图片、会议记录。
- **不可变（Immutable）**——LLM 只有读权限，绝不修改。
- 作用：**事实基准（Ground Truth）**。Wiki 万一乱了，能从这层重建；也是审计轨迹的源头。

## 第二层：Wiki（知识库层，`wiki/`）—— 核心

LLM 自动生成并维护的一堆 Markdown 文件。页面类型：

- 实体页（人物、公司、模型）
- 概念页（Transformer、RAG、编译器模式）
- 综述页、对比页
- 索引页 `index.md`（相当于程序的符号表）
- 日志页 `log.md`（只追加的构建日志）

关键规则：

- **LLM 完全拥有**——你只读，AI 负责写、更新、维护。
- 页面带 YAML front-matter（title、tags、source list、timestamp）。
- 所有页面用 `[[双向链接]]` 关联，形成知识图谱；用 `[[sources/...]]` 指回原始出处。

## 第三层：Schema（规则层，`CLAUDE.md` / `AGENTS.md` / `SCHEMA.md`）

用自然语言写的规范，告诉 LLM 怎么干活：

- Wiki 页面怎么命名？概念页要包含哪些章节？
- 发现新旧知识矛盾怎么处理？
- 新增资料后要更新哪些页面？什么算"声明"？何时合并/拆分？

作用：把"放飞自我"的聊天机器人变成守纪律、标准化的 Wiki 管理员。**这是最重要的文件**——它控制 Agent 如何构建与维护整个 Wiki。

## 三层的编译类比

| 层 | 编译类比 | 谁修改 |
|---|---|---|
| Raw Sources | 源代码 / 输入 | 人（只有人能加素材） |
| Wiki | 编译产物（binary） | LLM 完全拥有 |
| Schema | 编译器规则 / 构建配置 | 人与 LLM 共同演进 |

一致性来自这个边界：Raw 不可变保证可重建，Wiki 由 LLM 维护保证持续更新，Schema 保证更新方式可控——三者缺一，Wiki 就会退化为混乱的笔记堆。

> 相关：三操作如何维护这三层见 `../lifecycle/`；与 RAG 各子领域的对比见 `../practice/`；本体论的"开放世界语义 vs 封闭世界校验"思想见 `../../graphrag/ontology/`。
