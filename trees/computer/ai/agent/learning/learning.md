---
description: "Learning resources for AI agents: books, courses, websites and software by learning stage"
描述: "AI Agent 学习资源：按学习阶段整理的图书、课程、网址与软件"
name: "AI Agent Learning Resources"
名称: "AI Agent 学习资源"
---

# AI Agent 学习资源

资源按「解决什么问题」分，不按热度排。书与课程更新慢但时效有限——**框架 API 会过期，循环与评估原理不会**；选资源时先问它教的是思考方式还是某个版本的工具语法。

## 图书

| 书 | 适合解决什么 | 阶段 |
|---|---|---|
| **Build a Large Language Model from Scratch**（Raschka） | 从零理解分词、Transformer、预训练；Agent 的底层模型直觉 | 基础 |
| **Hands-On Large Language Models**（Alammar / Grootendorst） | 图示化理解 LLM 工作原理 | 基础 |
| **An Illustrated Guide to AI Agents**（Alammar / Grootendorst） | 电子书 2026-09-02、纸质 2026-10-06；300+ 图讲记忆、工具、规划、评估、多智能体；代码是裸 API 手写 TinyAgent | 入门，理解而非上线 |
| **《深入理解 AI Agent：设计原理与工程实践》**（李博杰，AgentBook） | 中文开源教程，V2.0 / 2026-09-02，CC BY-NC-SA；10 章 + 40+ 实验，`Agent = LLM + 上下文 + 工具`，强调「原则驱动」而非 Demo；站点 `agentbook.minims.cn`，仓库 `bojieli/ai-agent-book` | 中文入门与动手；章节与本树 context / memory / tool / eval / multi 高度对应 |
| **AI Agents in Action, 2e**（Lanham） | 五层模型（persona / actions / reasoning / memory / evaluation）；OpenAI Agents SDK、MCP、A2A、Phoenix 追踪 | 动手实现 |
| **Agentic Design Patterns**（Gulli） | 21 个可复用模式，案头参考；有免费预印本与 notebook 可先试读 | 模式参考 |
| **AI Engineering**（Chip Huyen） | 评估、失败模式、可观测性；把 Agent 放在基础模型应用的全景里 | 生产视角 |
| **Designing Multi-Agent Systems**（Dibia） | 框架无关的多智能体：顺序/并行/监督/计划/handoff/群聊；含 agent UX 与成本委派 | 多智能体进阶 |
| **Building Agentic AI Systems**（Biswas / Talukdar） | 架构总览、编排角色、治理与安全；企业场景 | 架构视角 |
| **Designing Data-Intensive Applications**（Kleppmann） | 存储、复制、流、事务、一致性——Agent 的记忆库、任务队列、审计日志的后端基础 | 系统基础 |
| **Human Compatible**（Russell） | 对齐、目标不确定性、监督与授权边界；设计审批流与升级策略时的镜头 | 治理与产品 |

## 开源书 / 在线教程

中文开源教程这条线与上面的出版书互补：可逐章对照源码、通常免费在线读。只收**系统成书**的仓库，零散教程不在此列。star 数波动大，只作量级参考。

| 仓库 | 内容 | 阅读 / 许可 |
|---|---|---|
| `bojieli/ai-agent-book` | AgentBook，《深入理解 AI Agent》，10 章 + 40+ 实验，原则驱动 | `agentbook.minims.cn`，CC BY-NC-SA |
| `datawhalechina/hello-agents` | 《从零开始构建智能体》：原理 → 经典范式 → 上下文工程 / 记忆检索 / 多智能体通信 → 实战案例与毕业设计 | 在线 `datawhalechina.github.io/hello-agents/`，Datawhale 开源社区 |
| `didilili/ai-agents-from-zero` | 从提示词到企业级 RAG / Agent 一条线；含面试题库、案例汇总、更新日志 | 在线 `didilili.github.io/ai-agents-from-zero/`，MIT |
| `datawhalechina/deepagents-in-action` | 基于 LangChain / LangGraph / Deep Agents：harness、上下文管理、子 Agent、Skills、长期记忆、HITL；9 章 + 2 准备篇，每章文字 + 视频 | 在线 `datawhalechina.github.io/deepagents-in-action/`，内容 CC BY-NC-SA 4.0、网站源码 MIT |
| `GenerativeAgents/agent-book` | notebook 形态的 Agent 书 | GitHub 仓库 |
| `cxbxmxcx/GPT-Agents` | Manning《GPT-Agents》配套仓库 | GitHub 仓库 |

Harness 方向的专题书（与 `../hooks/`、`../skill/`、`../context/` 对应）：

| 仓库 | 内容 |
|---|---|
| `lintsinghua/claude-code-book` | 《御舆：解码 Agent Harness》，42 万字、15 章，从对话循环到自建 harness |
| `wquguru/harness-books` | 两本讲 harness：约束、查询循环、上下文治理、多 Agent 验证 |
| `ciembor/agent-rules-books` | 把 Clean Code / Refactoring / DDD / Clean Architecture 写成 AGENTS.md 规则与 skills |

学术向：`harvard-edge/cs249r_book` ——《Machine Learning Systems》四卷本，含 Agentic AI 与 Physical AI 卷，站点 `mlsysbook.ai`。

> GitHub 搜索 `agent book` 噪声很大（会命中 AI 写的小说、翻译 skill 等）。按「系统成书 + 可在线读 + 与本树节点有对应」筛选，比按 star 排序可靠。

## 网址与课程

| 资源 | 地址 | 用途 |
|---|---|---|
| Hugging Face AI Agents Course | `https://huggingface.co/learn/agents-course/en/unit0/introduction` | 免费、从基础到进阶，覆盖 smolagents / LangGraph / Agentic RAG / 评估；有练习与证书 |
| Microsoft AI Agents for Beginners | GitHub 仓库搜索 `microsoft/ai-agents-for-beginners` | 18 课，一课一主题，例子可运行，多语言 |
| Anthropic《Building Effective Agents》 | `https://www.anthropic.com/research/building-effective-agents` | 工作流 vs Agent 的经典短文，原文 2024-12-19；页内注明「Much of the tooling landscape… has changed since December 2024」 |
| Claude Academy（Anthropic 官方） | `https://www.anthropic.com/learn`；开发者课程 `https://academy.claude.com/collections/build-with-claude` | Claude、Claude Code、工具使用、MCP、skills 等免费课程 |
| OpenAI《A Practical Guide to Building Agents》 | `https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf` | 官方构建指南，编排、护栏与 Agents SDK |
| OpenAI Agents SDK 文档 | `https://openai.github.io/openai-agents-python/` | Agents / tools / handoffs / guardrails / sessions / tracing |
| LangChain Academy | `https://academy.langchain.com/courses/intro-to-langgraph` | LangGraph 官方课：state、持久化、human-in-the-loop、部署 |
| LangGraph Essentials | `https://academy.langchain.com/courses/langgraph-essentials-python` | 节点、边、条件边、记忆、interrupt |
| LangGraph 官方文档 | `https://docs.langchain.com/oss/python/langgraph/overview` | StateGraph、checkpoint、memory、HITL |
| DeepLearning.AI《AI Agents in LangGraph》 | `https://www.deeplearning.ai/courses/ai-agents-in-langgraph` | 页面标注 Updated Nov 4, 2026；1h47m、9 课；手写 Agent 再用 LangGraph 重构，含 Agentic Search 与持久化 |
| DeepLearning.AI《Agentic AI》 | 站内搜索 | Andrew Ng 讲反思、工具、规划、多智能体与评估 |
| freeCodeCamp 开源 LLM Agent Handbook | `https://www.freecodecamp.org/news/the-open-source-llm-agent-handbook/` | 免费文字教程，发布于 2025-06-03；讲 Agent 循环、LangGraph 与 CrewAI，无配套视频 |
| MCP 官方文档 | `https://modelcontextprotocol.io` | 工具与数据接入的开放标准 |

> 课程教的是厂商的心智模型，这没问题——但要分清自己是在学概念、学实现，还是学产品工作流。旧文章的日期要看：被广泛引用的《Building Effective Agents》已加注说明部分工具形态变化。

## 软件与平台

| 类别 | 代表 | 学习中的用途 |
|---|---|---|
| 编码 Agent | Claude Code、OpenAI Codex、Cursor、Cline、OpenCode、Kiro、Gemini CLI、Antigravity | 读真实 Agent 的系统提示、工具面与权限模型 |
| 编排框架 | LangGraph、LlamaIndex、CrewAI、AutoGen、Google ADK、smolagents | 把循环、状态、多智能体从手写代码迁移到框架 |
| 本地实验 | Ollama、LM Studio、llama.cpp | 跑本地/开放权重模型，避免 API 成本 |
| 可观测 | LangSmith、Arize Phoenix | 追踪每一次模型与工具调用；评估而非肉眼判断 |
| 无代码自动化 | n8n | 工作流视角，理解「什么时候不该用 Agent」 |
| 免费实验场 | Google AI Studio、Hugging Face Spaces | 免费额度与免费托管，用来跑学习原型 |

## 开源书阅读路线

专门针对上面的开源书，与「一条学习路径」（书 / 课程 / 软件混合）互补。每阶段有可验收产出，框架 API 会变，交付物比章节数更重要。

| 阶段 | 读哪本 | 树节点 | 交付物 |
|---|---|---|---|
| 1. 建立心智模型 | `hello-agents` 前半（原理、范式）+ `ai-agent-book` 第 1 章 | `../intro/`、`../workflow/` | 用「Agent = LLM + 上下文 + 工具」复述一个真实 Agent，并说明它为什么不是工作流 |
| 2. 手写最小循环 | `ai-agents-from-zero` 前几章，或 `hello-agents` 经典范式实战 | `../examples/`、`../patterns/` | 裸 API + 2–3 个工具 + 一个循环，不用框架 |
| 3. 上下文与记忆 | `ai-agent-book` 第 2–3 章 + `hello-agents` 上下文/记忆部分 | `../context/`、`../../rag/memory/`、`../knowledge-strategy/` | 设计短期/长期记忆分层，并说明缓存命中的前提 |
| 4. 工具与 MCP | `ai-agent-book` 第 4 章 + `deepagents-in-action` 的 harness / Skills 章 | `../tool/`、`../mcp/`、`../skill/` | 写一个符合工具契约的 MCP server，并给出错误参数的处理 |
| 5. 评估与工程化 | `ai-agent-book` 第 6 章 + `ai-agents-from-zero` 面试题库（系统设计题） | `../eval/`、`../prod/`、`../obs/` | 建 20 条轨迹黄金集，跑一次评估并定位失败 case |
| 6. Harness 专项（可选分支） | `claude-code-book` 15 章 → `harness-books` → `agent-rules-books` | `../hooks/`、`../coding/`、`../prompt/` | 拆解一个真实 harness 的生命周期钩子与权限边界，写成 rules |
| 7. 多智能体与进阶 | `ai-agent-book` 第 10 章 + `hello-agents` 多智能体实战 | `../multi/`、`../patterns/` | 对比单 Agent 与多 Agent 在同一任务上的成本和质量 |
| 8. 学术纵深（可选） | `harvard-edge/cs249r_book` 的 Agentic AI 卷 | `../../model/`、`../rl/` | 写一份「后训练如何影响 Agent 工具调用」的综述 |

主线：**先建立模型直觉 → 手写循环 → 逐层加上下文/记忆/工具 → 用评估兜底 → 再按兴趣分支到 harness 或多智能体**。

## 一条学习路径

1. **先读短文建立判断**：Anthropic《Building Effective Agents》+ 本树 `../intro/`、`../workflow/`——先能区分工作流与 Agent。
2. **裸 API 手写一次**：不用框架，给模型 2–3 个工具和一个循环。理解框架在抽象什么；本树 `../examples/` 有最小模板。
3. **补模式与评估**：Hugging Face 课程或 Andrew Ng 的 Agentic AI 课；对照本树 `../patterns/`、`../eval/`。
4. **选一个生产 SDK 深入**：OpenAI Agents SDK / LangGraph / Google ADK 三选一，读完整文档并上线一个带追踪的 Agent；对照本树 `../frameworks/`、`../langgraph/`。
5. **补系统与治理**：`../prod/`、`../obs/`、`../safety/`，再读 Chip Huyen 与 Kleppmann。

顺序的理由：先学循环与评估，再学框架 API——框架会变，循环与评估不会。

## 一句话主线

**AI Agent 的学习主线是「先手写循环建立直觉 → 用模式与评估补判断 → 选一个 SDK 做生产 → 补系统与治理」；书与课程按这条线各取一段，不按榜单全读。**

> 相关：Agent 入门见 `../intro/`；构建流程见 `../build/`；框架选型见 `../frameworks/`；评估见 `../eval/`。
