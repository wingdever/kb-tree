---
description: "Curated hands-on tutorials for learning AI agent development: official SDK quickstarts, framework guides, courses and Chinese open-source labs"
描述: "AI Agent 开发教程清单：官方 SDK 快速入门、框架教程、系统课程与中文开源实战"
name: "AI Agent Development Tutorials"
名称: "AI Agent 开发教程"
---

# AI Agent 开发教程

“所有教程”没有可穷举的边界：新课程每月出现，旧教程的 API 会过期。这里给的是一个**可核验的教程全集口径**：截至 2026-11-29 仍可访问、以动手为主、能落到一个可运行 Agent 的公开教程；优先官方或维护良好的来源，排除纯营销课、纯概念长文、已停止维护的旧版本教程和零散博客。

按学习目标分成五类：**官方 SDK 与平台快速入门、框架官方教程、系统课程、中文与开源实战、专题与进阶**。书与理论读物不在这里重复，本页只收“跟着做能跑起来”的材料。

## 收录口径

- **可运行**：有安装步骤、代码或 notebook，能独立跑出一个 Agent，而不是只讲概念。
- **可核验**：官方文档、官方课程、大学/平台课程，或有维护记录的公开仓库。
- **当前可用**：优先 2026 年仍在更新的入口；旧教程仍列出时，会标明它教的是旧 API 还是稳定原理。
- **不重复**：同一产品的 Python/TypeScript 入口算两个教程；同一课程的旧版与新版只收新版。
- **不承诺“穷尽”**：收费训练营、企业内训、已下架视频不在公开清单内；新教程出现后应增补而不是把本页当永久目录。

## 按目标选教程

| 你现在要解决什么 | 先看什么 | 为什么 |
|---|---|---|
| 第一次跑通一个 Agent | OpenAI Agents SDK Quickstart、Google ADK Quickstart、Claude Agent SDK Quickstart | 三份都是官方最小闭环，装完就能看到一个完整循环 |
| 中文入门、想系统读 | AgentBook、Hello-Agents | 中文成书 + 实验，覆盖原理到实战 |
| 想学框架而不是某个厂商 | LangGraph Academy、CrewAI Quickstart、PydanticAI | 状态图、角色协作、类型化三种典型路线 |
| 做多智能体 | AutoGen AgentChat、CrewAI、LangGraph 多智能体教程 | 对话式、角色式、图式三种编排 |
| 做生产部署 | Bedrock AgentCore、Microsoft Foundry、Cloudflare Agents | 都从本地脚手架走到云端运行与观测 |
| 做 RAG Agent | LlamaIndex Starter、DeepLearning.AI Agentic RAG | 检索、工具调用、评估串成一条线 |
| 做 MCP 工具接入 | Hugging Face MCP Course、Microsoft MCP for Beginners | 协议、服务器/客户端、权限与部署 |
| 做评估与可观测 | LangSmith Essentials、Hugging Face 课程评估单元 | 先能看见轨迹，再谈优化 |
| 拆真实 Harness | claude-code-book、harness-books、Deep Agents 教程 | 从循环、上下文治理到子 Agent 与权限 |

## 官方 SDK 与平台快速入门

这些教程由 SDK 或云平台自己维护，优点是 API 与当前版本一致，缺点是只教自家抽象。

| 教程 | 提供方 | 你会做出什么 | 地址 |
|---|---|---|---|
| OpenAI Agents SDK — Python Quickstart | OpenAI | 第一个文本 Agent，加工具、会话与追踪 | https://openai.github.io/openai-agents-python/quickstart/ |
| OpenAI Agents SDK — TypeScript Quickstart | OpenAI | 用 TypeScript 跑通 Agent 与工具循环 | https://openai.github.io/openai-agents-js/quickstart/ |
| OpenAI Agents SDK — Examples | OpenAI | handoff、guardrail、session、sandbox、voice 等完整示例 | https://github.com/openai/openai-agents-python/tree/main/examples |
| Claude Agent SDK — Quickstart | Anthropic | 一个能读代码、找 bug 并修复的编码 Agent | https://code.claude.com/docs/en/agent-sdk/quickstart |
| Google ADK — Python Quickstart | Google | 多工具 Agent，本地 CLI 与 Dev UI | https://google.github.io/adk-docs/get-started/python/ |
| Google ADK — Multi-tool Quickstart | Google | 多语言入口，最小 Agent + 工具 | https://google.github.io/adk-docs/get-started/quickstart/ |
| Google Codelab — Building AI Agents with ADK | Google | 跟着 Cloud Shell 一步步做出个人助理 | https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation |
| Microsoft Agent Framework — Your First Agent | Microsoft | 第一个 Agent，再逐步加工具、会话、记忆、工作流 | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent |
| Microsoft AI Agents for Beginners | Microsoft | 多课代码样例，覆盖工具、规划、多 Agent、RAG、MCP | https://github.com/microsoft/ai-agents-for-beginners |
| Semantic Kernel — Quickstart | Microsoft | 用插件与 Agent 抽象做出可调用工具的 Agent | https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide |
| AutoGen — AgentChat Tutorial | Microsoft | 双 Agent 对话、群聊、代码执行与 MCP 工具 | https://microsoft.github.io/autogen/stable/ |
| Amazon Bedrock Agents — Create Agent | AWS | 配置模型、动作组与知识库的托管 Agent | https://docs.aws.amazon.com/bedrock/latest/userguide/agents-create.html |
| Amazon Bedrock AgentCore — CLI Quickstart | AWS | 脚手架、本地测试、部署并调用云端 Agent | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html |
| Microsoft Foundry — Prompt Agent Quickstart | Microsoft | 在 Foundry 创建带指令与工具的托管 Agent | https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstarts/prompt-agent |
| Vercel AI SDK — Agents Guide | Vercel | 用 TypeScript 写工具循环并部署为 API | https://vercel.com/docs/agents |
| Cloudflare Agents — First Durable Agent | Cloudflare | 跑在 Durable Object 上的持久化 Agent | https://developers.cloudflare.com/agents/getting-started/quick-start/ |
| Letta — Quickstart | Letta | 带长期记忆的 Agent，云端或本地 CLI | https://docs.letta.com/quickstart |
| Mastra — Run Your First Agent | Mastra | 完整项目脚手架、Studio 调试与工具 | https://mastra.ai/learn/run-your-first-agent |

## 框架官方教程

框架教程的价值是教你它的抽象，不是教你 Agent 的全部。选一个深入，不要把每个框架的 hello world 都刷一遍。

| 教程 | 提供方 | 你会做出什么 | 地址 |
|---|---|---|---|
| LangChain — Agents | LangChain | 用 `create_agent` 做工具调用、middleware、结构化输出 | https://docs.langchain.com/oss/python/langchain/agents |
| LangGraph — Introduction | LangChain Academy | 从手写循环过渡到状态图、记忆、human-in-the-loop、部署 | https://academy.langchain.com/courses/intro-to-langgraph |
| LangGraph — Essentials | LangChain Academy | 节点、边、条件边、记忆与 interrupt 的最小闭环 | https://academy.langchain.com/courses/langgraph-essentials-python |
| LangSmith — Essentials | LangChain Academy | 追踪、数据集、评估与回归 | https://academy.langchain.com/courses/langsmith-essentials |
| LlamaIndex — Starter Tutorial | LlamaIndex | 用本地模型做计算器 Agent，再加 RAG | https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/ |
| LlamaIndex — Building an Agent | LlamaIndex | FunctionAgent、工具调用与多 Agent 入口 | https://developers.llamaindex.ai/python/framework/understanding/agent/ |
| CrewAI — Quickstart | CrewAI | 角色化 Crew + Flow 的完整项目 | https://docs.crewai.com/en/quickstart |
| PydanticAI — Agents | Pydantic | 类型安全、依赖注入、结构化输出的 Agent | https://ai.pydantic.dev/ |
| smolagents — Guided Tour | Hugging Face | CodeAgent、工具调用与多 Agent 管理 | https://huggingface.co/docs/smolagents/guided_tour |
| Agno — Setup and Quickstart | Agno | 带知识库、记忆与 AgentOS 服务的 Agent | https://docs.agno.com/sdk/setup |

## 系统课程

系统课程适合补“为什么”，但不要用课程替代项目。免费/付费状态以课程页为准。

| 课程 | 提供方 | 你会得到什么 | 地址 |
|---|---|---|---|
| AI Agents Course | Hugging Face | 从基础到 smolagents / LlamaIndex / LangGraph，含练习与证书 | https://huggingface.co/learn/agents-course/en/unit0/introduction |
| Agentic AI | DeepLearning.AI | Andrew Ng 讲反思、工具、规划、多 Agent 与评估 | https://www.deeplearning.ai/courses/agentic-ai/ |
| AI Agents in LangGraph | DeepLearning.AI | 手写 Agent 再用 LangGraph 重构，含持久化与 Agentic Search | https://www.deeplearning.ai/courses/ai-agents-in-langgraph |
| Multi AI Agent Systems with crewAI | DeepLearning.AI | 角色分工、任务委派与 Crew 协作 | https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai/ |
| AI Agentic Design Patterns with AutoGen | DeepLearning.AI | 反思、工具、规划、多 Agent 等模式的 AutoGen 实现 | https://www.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/ |
| Building Agentic RAG with LlamaIndex | DeepLearning.AI | 检索、路由、工具调用与 Agentic RAG | https://www.deeplearning.ai/courses/building-agentic-rag-with-llamaindex/ |
| Functions, Tools and Agents with LangChain | DeepLearning.AI | function calling、工具、输出解析与对话循环 | https://www.deeplearning.ai/courses/functions-tools-agents-langchain/ |
| Generative AI for Beginners | Microsoft | 生成式 AI 基础，含 Agent 相关课节 | https://github.com/microsoft/generative-ai-for-beginners |
| Claude Academy | Anthropic | Claude、Claude Code、工具使用、MCP、skills 的官方课 | https://www.anthropic.com/learn |
| MCP for Beginners | Microsoft | 跨语言 MCP 课程，覆盖服务器、客户端、安全与部署 | https://github.com/microsoft/mcp-for-beginners |
| MCP Course | Hugging Face | 从协议到端到端应用，含练习与证书 | https://huggingface.co/learn/mcp-course/unit0/introduction |
| Open Source LLM Agent Handbook | freeCodeCamp | 免费文字教程：Agent 循环、LangGraph、CrewAI | https://www.freecodecamp.org/news/the-open-source-llm-agent-handbook/ |

## 中文与开源实战

中文材料优先选“成书 + 可运行代码 + 持续维护”的仓库；只收系统教程，不收零散翻译。

| 教程 | 维护方 | 内容 | 地址 |
|---|---|---|---|
| Hello-Agents《从零开始构建智能体》 | Datawhale | 原理、经典范式、上下文与记忆、多 Agent、实战案例 | https://github.com/datawhalechina/hello-agents |
| AgentBook《深入理解 AI Agent》 | 李博杰 | 原则驱动，10 章 + 实验，强调 `Agent = LLM + 上下文 + 工具` | https://github.com/bojieli/ai-agent-book |
| ai-agents-from-zero | didilili | 从提示词到企业级 RAG / Agent，含面试题库与案例 | https://github.com/didilili/ai-agents-from-zero |
| Deep Agents in Action | Datawhale | 基于 LangGraph / Deep Agents：harness、上下文、子 Agent、Skills、HITL | https://github.com/datawhalechina/deepagents-in-action |
| Claude Code Book《御舆》 | lintsinghua | 从对话循环到自建 harness，拆解真实编码 Agent | https://github.com/lintsinghua/claude-code-book |
| Harness Books | wquguru | 约束、查询循环、上下文治理、多 Agent 验证 | https://github.com/wquguru/harness-books |
| Agent Rules Books | ciembor | 把 Clean Code / DDD / Clean Architecture 写成 AGENTS.md 规则 | https://github.com/ciembor/agent-rules-books |
| Machine Learning Systems | Harvard Edge | 含 Agentic AI 与 Physical AI 卷的系统教材 | https://github.com/harvard-edge/cs249r_book |

## 专题与进阶

| 教程 / 指南 | 提供方 | 解决什么 | 地址 |
|---|---|---|---|
| Realtime Agents Quickstart | OpenAI | 低延迟语音 Agent、打断与实时工具调用 | https://openai.github.io/openai-agents-python/realtime/quickstart/ |
| Voice Pipeline Quickstart | OpenAI | STT → Agent → TTS 的语音流水线 | https://openai.github.io/openai-agents-python/voice/quickstart/ |
| 12-Factor Agents | HumanLayer | 生产 Agent 的十二条工程原则，适合对照自己的 harness | https://github.com/humanlayer/12-factor-agents |
| OpenAI Cookbook | OpenAI | 官方示例集：工具、RAG、评估、多 Agent、微调 | https://cookbook.openai.com/ |
| Anthropic Cookbook | Anthropic | Claude 工具调用、检索、Agent 与评估 notebook | https://github.com/anthropics/claude-cookbooks |

## 不算教程但该先读

这些材料不教你一步步写代码，但决定你会不会把教程学歪。

- Anthropic《Building Effective Agents》：先分清工作流与 Agent，再决定要不要循环与工具。原文 2024-12-19，页面已注明部分工具形态变化。
- OpenAI《A Practical Guide to Building Agents》：官方构建指南，讲编排、护栏与上线前的判断。
- Google《Agents》白皮书：从产品与架构角度解释 Agent 的能力边界，适合给非工程干系人看。
- 12-Factor Agents：把“能跑的 demo”变成“能维护的系统”的检查表。

## 常见坑

- **把教程当规范**：教程为了短，常省略异常、权限、成本与评估；上线前必须补。
- **学框架 API 而不是循环**：框架会换，`模型 → 工具 → 结果 → 再决策` 的循环不会。
- **只跑 hello world**：没有真实工具、真实数据和失败注入，学不到 harness 的关键部分。
- **忽略版本**：Agent SDK 与云平台 API 变化快，先看文档日期与迁移说明。
- **没有评估**：能演示不等于稳定；至少建一组黄金任务与失败分类。
- **默认权限过大**：文件、shell、网络与凭证权限要按最小必要给，教程里的 `allow all` 不能照搬。

## 一句话主线

**先跟一个官方 Quickstart 跑通完整循环，再用一门系统课补判断，然后选一个框架深入并把评估、权限与部署补齐；教程负责带你入门，不负责替你定义生产边界。**

## 参考资料

- OpenAI Agents SDK 文档：https://openai.github.io/openai-agents-python/
- Claude Agent SDK 文档：https://code.claude.com/docs/en/agent-sdk/overview
- Google ADK 文档：https://google.github.io/adk-docs/get-started/
- Microsoft AI Agents for Beginners：https://github.com/microsoft/ai-agents-for-beginners
- Hugging Face AI Agents Course：https://huggingface.co/learn/agents-course/en/unit0/introduction
- LangChain Academy：https://academy.langchain.com/
- DeepLearning.AI 课程目录：https://www.deeplearning.ai/courses/
- Microsoft MCP for Beginners：https://github.com/microsoft/mcp-for-beginners
- Hugging Face MCP Course：https://huggingface.co/learn/mcp-course/unit0/introduction
- Vercel AI SDK Agents：https://vercel.com/docs/agents
