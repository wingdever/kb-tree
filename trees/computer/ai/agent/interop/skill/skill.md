---
description: "Agent skills: portable contracts, SKILL.md spec, progressive disclosure and Graph-of-Skills composition"
描述: "Agent 技能：可移植契约、SKILL.md 规范、渐进式披露与技能图组合"
name: "Agent Skills"
名称: "Agent 技能"
---

# Skill 技能

技能是为智能体提供的**结构化、可发现、可复用的操作指南**。它把能力打包成可移植契约——这是 Agent 工程里"约束意义"的重要一层。

## 目录结构

标准骨架：

```text
skills/<skill-name>/        # 技能名必须 kebab-case（如 pdf-processing）
├── SKILL.md             # 必需：元数据与核心指令入口
├── references/          # 可选：详细参考文档、决策表、长文本
├── assets/              # 可选：模板文件（HTML、Markdown 模板）
└── scripts/             # 可选：确定性验证脚本（格式检查、路径校验）
```

关键规则：

- **命名强制**：文件夹名与 SKILL.md 的 `name` 字段必须用 kebab-case（小写字母、数字、连字符）且**完全一致**。
大小写敏感；技能文件夹内**禁止 README.md**。
- **职责分离**：SKILL.md 只承载核心流程与索引；超过约 100 行的详细内容移到 `references/`；模板放 `assets/`；`scripts/` 仅用于确定性校验逻辑，而非 LLM 驱动逻辑。
- **扁平并列**：多个技能逻辑上属于一个领域时，用共同名称前缀。

## SKILL.md 编写规范

内容分元数据（YAML Frontmatter）与正文（Markdown）。

### YAML Frontmatter

文件顶部必须由 `---` 包裹的 YAML 块——这是 AI 发现与触发技能的依据。

- 必需：`name`、`description`
- 可选：`license`、`compatibility`、`metadata`、`allowed-tools`、`disabled-model-invocation`

description 范例——好描述同时明确**能力**与**触发场景**：

```yaml
# 好
description: >
  Extracts text and tables from PDF files, fills forms, merges PDFs.
  Use when working with PDFs or when user mentions PDF, form,
  or document extraction.

# 糟
description: Helps with PDFs.
```

### Markdown 正文（渐进式披露）

正文是 AI 执行任务时的操作指南，遵循**渐进式披露**：SKILL.md 保持精炼，详细内容分层。

- 核心流程置正文：工作流指令、触发示例、少于 3 分支的简单决策树。
- 详细信息外置：超过 50 行的复杂决策表、参考矩阵、案例研究放 `references/`，供 AI 按需加载以省上下文 token。
- 篇幅控制：主 SKILL.md 建议 500 行以内。

## 技能怎么被选中

技能不会被"自动懂"，它靠 description 参与检索与决策。这决定了描述该怎么写：

- **写触发场景，不只写能力**：`Extracts tables from PDFs` 是能力描述，`Use when the user uploads a PDF or asks to extract tables` 才是触发条件。缺触发条件的技能几乎不会被召回。
- **写用户会说的词**：用户的说法、同义词、常见错写都要覆盖；写成内部术语表就只能被内部人触发。
- **写边界**：明确"不处理什么"，能挡掉一半误触发（比如"不处理纯本地文件操作"）。
- **名字要能预测内容**：kebab-case 的短名本身就是检索词的一部分，`pdf-form-fill` 比 `document-helper` 更容易命中。

> 判断：技能被召回的准确率主要取决于 description，而不是正文写得多好。正文只在"选中之后"起作用——选不中，写得再细也没人看。

## 什么时候不该做成技能

技能适合"每次做法一致、但需要判断"的流程。以下情况做成技能反而增加负担：

- **纯确定性操作**：格式转换、字段校验这类，写成脚本让模型调用即可，不需要一份供模型阅读的指南。
- **一次性任务**：为一次交付写规范的成本高于直接做完。
- **事实性知识**：产品参数、政策条款这类会变的事实，应该进检索库，而不是固化在技能正文里。
- **需要跨会话状态**：技能是无状态的说明文档，需要记忆与状态的部分应交给运行时。

## 版本与演进

技能是长期资产，改动要考虑兼容：

- **破坏性改动要显式**：改目录名、改必填字段、改输出约定，都属于破坏性变更，需要版本号或新技能名，而不是原地覆盖。
- **正文与脚本同源**：`scripts/` 里的校验逻辑如果与正文描述不一致，模型会按正文做、按脚本被拒，产生难查的失败。
- **可验证**：给技能配一两个"照做之后应该得到什么"的样例，改动后能自查是否还成立。
- **随仓库走**：技能与使用它的代码放在同一个仓库，避免"代码改了、技能还是旧的"。

## 技能关系管理

**Graph-of-Skills（GoS）**：离线阶段把技能包解析成可执行技能图，显式构建技能间的**依赖边**与**工作流边**。这把"一堆技能"变成可编排、可组合的图。

组合、依赖、编排、检索是技能工程的四个维度。技能与工具的区别：技能是"怎么做"的知识包（可含流程、规则、模板），工具是"做什么"的可执行接口。

## 与其他层次的关系

| 层 | 提供什么 | 类比 |
|---|---|---|
| 技能 | 按需加载的程序性知识 | 操作手册 |
| 工具 | 确定性可执行接口 | 工具箱 |
| 本体/契约 | 共享词汇与类型约束 | 领域词典 |
| 提示 | 单次任务的指令 | 口头交代 |

## 一句话主线

技能的本质是**把"怎么做"从提示词里搬进一个可发现、可版本化、按需加载的包里**；它的收益来自可复用与省上下文，代价是必须把触发条件和边界写清楚。

## 参考资料

- Agent Skills 官方规范：agentskills.io —— 对目录结构、字段定义与描述写法最权威。
- Microsoft Learn — Agent Skills：详细说明"渐进式披露"等核心设计模式。

