---
description: "Comparison of mainstream agent frameworks and selection guide"
描述: "主流 Agent 框架对比与选型指南"
name: "Agent Framework Comparison"
名称: "主流框架对比"
---

# 04 主流框架对比

## 核心判断：框架要"挣得自己的位置"

> 从厂商 SDK 或你自己写的薄循环开始，只有当状态管理、多智能体协调或持久化执行真正成为瓶颈时，才引入更重的框架。

不要自己从零写编排循环——但**至少亲手写一个 Agent**，哪怕之后改用框架。理由：理解模型在哪里被允许决定、你的代码在哪里掌控，是工程师与"提示词调整者"的区别。

## 框架/方式对比

| 框架 / 方式 | 核心优势 | 适用场景 | 取舍 |
|---|---|---|---|
| **LangChain / LangGraph** | 模块化、状态驱动的 Agent 循环；LangGraph 把 Agent 建模为带持久化检查点的显式状态图 | 复杂、有状态、多步骤的自主工作流；分支、暂停/恢复、可检查执行 | 流行方案里学习曲线最陡 |
| **Deep Agents** | 生产级 harness：内置规划、记忆、上下文管理、子智能体、执行环境 | 长运行、大上下文、任务关键型工作 | 抽象更重 |
| **LlamaIndex** | 以检索为核心，索引与查询抽象 | 核心任务是在私有数据上推理的 Agent | 编排能力相对弱 |
| **CrewAI** | 面向角色化的多智能体快速原型，声明式定义更易读 | 多智能体协作；快速产出第一个 Agent | 内置可观测性较弱 |
| **AutoGen（Microsoft）** | 对话式多智能体工作流 | 多智能体对话协作 | 偏研究/对话范式 |
| **厂商 SDK**（Claude Agent SDK、OpenAI Agents SDK 等） | 贴近底层 API、抽象少、控制最强、依赖面小 | 想要最大控制、最少依赖 | 需自己搭更多基础设施 |
| **纯代码 / 自研循环** | 完全控制、自定义工具、理解 Agent 真正原理 | 学习、深度定制 | 需要编程能力与更多搭建工作 |
| **无代码平台**（如 n8n） | 非程序员、快速原型 | 不写代码、快速验证 | 对逻辑与集成的控制较少 |

对初学者，LangChain 或 Anthropic Claude API 通常提供简单性与能力的最佳平衡。

## 参考实现与工程实录

框架给的是原语；要理解一个 Agent 实际怎么组织，读一份可运行的实现比读框架榜单更有效。按学习目的分组。

### 读代码学原理

| 项目 | 值得看的地方 |
|---|---|
| **Pi** | 极简终端 agent：扩展、技能、提示模板之外几乎不多做，可 headless 运行；适合看清每个零件 |
| **smolagents** | 模型用「写 Python 代码」代替 JSON tool call，自己的代码很少；最快理解 agent loop |
| **Aider** | diff/patch 编辑 + git 原生；学模型如何安全改代码并自动提交 |
| **Mini-Kode / tau** | 为可读性设计的参考实现；tau 小到能从头读到尾 |
| **Claw Code + Claurst** | 按 Claude Code 架构的干净重写与配套剖析；看权限模型、持久会话、技能系统 |

### 现成 harness（可参考架构，不必自研）

| 项目 | 定位 |
|---|---|
| **Deep Agents** | 架在 LangGraph 上：规划、上下文隔离子智能体、文件系统、沙箱 shell、摘要、人工审批；每块可替换 |
| **OpenHands** | 自主软件工程 agent，沙箱执行 |
| **DeerFlow** | 长运行 super-agent：子智能体 + 持久记忆 + 沙箱，面向小时级任务 |
| **Hermes Agent** | 自改进闭环：成功后自己写技能、持久记忆、定时调度 |
| **OpenClaw / ZeroClaw / nanobot** | 常驻型谱系：生态广 / 单二进制带审批门禁 / 小 Python 代码库 |
| **dsh** | 插件化 harness：模型、工具、技能、调度、界面都是插件 |

### 专项能力

- **Browser Use** — web 交互层，常与编排框架搭配。
- **Letta** — 以记忆为核心抽象。
- **opendevops** — 安全样本：模型拿不到 shell，只能按 argv 调用并走默认拒绝策略，配预算止损与审计账本。

### 工程实录

OpenAI《Harness engineering: leveraging Codex in an agent-first world》（2026-02）：五个月、约 100 万行代码、1500 个合并 PR、零手写代码。可迁移的做法：`AGENTS.md` 约 100 行当目录而非百科、结构化文档当真相源、让 agent 定期做文档园艺、输出自评循环、把清理规则变成机械检查的金律。

### 怎么读

- 先读最小闭环，再读带状态与子智能体的实现；顺序：`../examples/` → smolagents / Pi → `../langgraph/` → harness。
- 榜单排名和 star 数变化快，按「想学什么」选项目，不按排名选。
- 框架之外的共识：强 tool-calling 模型配一个朴素循环，常胜过弱模型配复杂图；先手写一次循环再决定要不要框架。

## LangChain 开源技术栈：三层抽象

LangChain 把生态组织成三层，每层建立在前一层之上，可在抽象与控制之间按需选择：

1. **Deep Agents**：生产级 harness，内置上下文管理、子智能体抽象、长期记忆和技能；为长运行、大上下文任务设计，能让 Agent 拥有记忆、工具、技能和文件系统访问，并把工作委派给上下文隔离的子智能体。
2. **LangChain**：核心 Agent 循环（`create_agent`，构建于 LangGraph 之上）以及模型、推理提供者、工具、消息、MCP、中间件的构建块；适合围绕标准循环组装自己的 harness，或在循环周围加中间件、护栏、动态上下文、人工审核、业务逻辑。
3. **LangGraph**：承载生产 Agent 的持久化引擎，低层原语，支持确定性与 Agent 步骤的混合；图模型 + 持久引擎，具备 human-in-the-loop 控制、容错、流式、持久化与可观测性。适合标准循环装不下的场景，或需要显式建模复杂状态转换、多智能体显式协调的场景。

三者可独立使用也可叠加；随需求变化可在层间迁移。配套：LangSmith 负责追踪、评估与监控（框架无关，任何 LLM 应用都能接入）。

### 官方推荐的学习路径（LangChain Learn）

- **快速上手**：语义搜索、RAG Agent、SQL Agent（带人工审核）、语音 Agent。
- **深入定制（LangGraph）**：自定义 RAG Agent、自定义 SQL Agent。
- **多智能体**：子智能体（个人助手）、交接（客服）、路由（知识库）、技能（按需加载上下文的 SQL 助手）。
- **概念**：记忆、上下文工程、Graph API、Functional API。

## MCP（Model Context Protocol）

Anthropic 开源的 Model Context Protocol 让 Agent 以标准化、安全的方式动态获取上下文，调用本地数据库或第三方 API，解决智能体与外部世界的"数据孤岛"问题。主流框架与 SDK 已普遍支持 MCP，把工具/数据源接入做成可复用协议，而不是每个项目重复写集成代码。

## Anthropic 官方提及的框架

Anthropic 的指南列出了几类可帮助实现 agentic 系统的框架：

- **Claude Agent SDK**（Anthropic 官方）
- **Strands Agents SDK**（AWS）
- **Rivet**：拖拽式 GUI LLM 工作流构建器
- **Vellum**：用于构建和测试复杂工作流的 GUI 工具

框架的价值在于简化调用 LLM、定义与解析工具、串联调用等标准底层任务，让你快速起步。代价是引入额外抽象层，可能遮蔽底层提示词与响应、让调试变难，也容易在简单方案就够用时诱发不必要的复杂度。

Anthropic 的建议很明确：**开发者应先直接使用 LLM API**——许多模式几行代码就能实现。如果用框架，务必理解底层代码；对底层机制的错误假设是常见错误来源。进入生产时，不要犹豫减少抽象层、改用基础组件构建。

## 选型建议汇总

- 任务能拆成固定子任务 → 先考虑 Workflow / 提示链，不要上 Agent 框架。
- 核心是私有数据问答 → LlamaIndex 或 LangGraph 自建 RAG。
- 核心是复杂状态与可控执行 → LangGraph。
- 多角色快速原型 → CrewAI。
- 追求与控制、最小依赖 → 厂商 SDK 或自己写薄循环。
- 框架只是工具：**先让正常路径跑通，再考虑样式与边界防御**；框架应随瓶颈出现而引入，而非一开始就堆满。
