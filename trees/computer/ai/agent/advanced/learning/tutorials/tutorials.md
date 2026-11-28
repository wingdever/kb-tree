---
description: "Curated hands-on tutorials for learning AI agent development: official SDK quickstarts, framework guides, courses and Chinese open-source labs"
描述: "AI Agent 开发教程清单：官方 SDK 快速入门、框架教程、系统课程与中文开源实战"
name: "AI Agent Development Tutorials"
名称: "AI Agent 开发教程"
---

# AI Agent 开发教程

“所有教程”没有可穷举的边界：新课程每月出现，旧教程的 API 会过期。这里给的是一个**可核验的教程全集口径**：截至 2026-11-29 仍可访问、以动手为主、能落到一个可运行 Agent 的公开教程；优先官方或维护良好的来源，排除纯营销课、纯概念长文、已停止维护的旧版本教程和零散博客。

按学习目标分成五类：**官方 SDK 与平台快速入门、框架官方教程、系统课程、中文与开源实战、专题与进阶**。书与理论读物不在这里重复，本页只收“跟着做能跑起来”的材料；逐条清单不再铺在正文，而是按表填写到清单文件。

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

## 教程清单

逐条清单在 `tutorials.list.csv`，一行一个教程，列为 `name, group, source, url, note`。正文只保留分类与选择判断，增删教程时直接改表，不再改 Markdown 表格。

| 列 | 填什么 |
|---|---|
| `name` | 教程名称，同一节点内唯一 |
| `group` | 五类之一：官方 SDK 与平台快速入门 / 框架官方教程 / 系统课程 / 中文与开源实战 / 专题与进阶 |
| `source` | 提供方：公司、社区、作者或课程平台 |
| `url` | 教程直达链接，必须是 `http` 或 `https` |
| `note` | 一句话说明“学完能做出什么”，不写营销话术 |

五个分组的口径：

- **官方 SDK 与平台快速入门**：由 SDK 或云平台维护的 quickstart、codelab 与官方示例，用来第一次跑通完整循环。
- **框架官方教程**：LangChain、LangGraph、LlamaIndex、CrewAI、PydanticAI、smolagents、Agno 等框架自己维护的教程，用来理解它的抽象。
- **系统课程**：带章节、练习或证书的课程，用来补“为什么”和评估方法。
- **中文与开源实战**：中文成书、开源教材与可运行仓库，用来补中文表达与完整项目。
- **专题与进阶**：语音、实时、Harness、生产原则与 Cookbook 示例，用来补单点能力。

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
