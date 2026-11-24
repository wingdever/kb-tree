---
description: "Framework orchestration models for multi-agent systems"
描述: "多智能体框架的编排模型与取舍"
name: "Multi-Agent Framework Implementations"
名称: "多智能体框架实现"
---

# 多智能体框架实现

选择框架很大程度上决定了哪些模式容易实现。你选的框架决定了编排的"形状"。

## 框架映射

| 框架 | 编排模型 | 甜点区 |
|---|---|---|
| **LangGraph** | 图 / 状态机，你定义节点和边 | 可控、有状态、人在回路；分支/暂停恢复/可检查执行 |
| **CrewAI** | 基于角色的 crew（角色、目标、任务），顺序或 hierarchical process | 快速搭专门角色团队；可读的声明式定义 |
| **AutoGen / AG2** | 对话式 Agent，群聊 + 管理者 | 对话与代码执行团队；对话式多智能体工作流 |
| **OpenAI Agents SDK** | 轻量 Agent + 工具 + handoffs + guardrails | 以交接为中心、带护栏的流程；manager 模式 |
| **Google ADK** | 会话/状态与编排分离 | 会话状态与编排解耦 |
| **Microsoft Agent Framework** | concurrent 模式（对应 sectioning 并行化） | 并行扇出 |

## 各框架与模式的对应

- **层级/监督者**：LangGraph 的 supervisor、`create_supervisor()`（LangChain 2026 更推荐直接用工具调用实现以控制上下文）；CrewAI 的 hierarchical process（自动 manager）；OpenAI Agents SDK 的 manager 模式。
- **网络/Swarm**：LangGraph 的 swarm 实现——Agent 直接交接，系统记住最后活跃的 Agent；OpenAI Agents SDK 的 handoffs（triage Agent 路由到专家，专家接管该轮）。
- **群体聊天**：AutoGen / AG2 的 group chat + speaker selection；LangGraph 的双节点互评模板。
- **顺序/流水线**：各框架都可用线性链实现；CrewAI 的 sequential process。
- **黑板/共享状态**：需要自定义共享工作区 + 控制组件；工具尚不成熟。

## 选择与取舍

- 追求**可控与可恢复**：LangGraph（状态图、检查点、人在回路）。
- 追求**快速角色化原型**：CrewAI（声明式 crew 定义快，但内置可观测性较弱）。
- 追求**对话/代码执行团队**：AutoGen（群聊范式，偏研究与对话）。
- 追求**交接与护栏**：OpenAI Agents SDK（handoff-centric + guardrails）。
- 追求**贴近底层、最小依赖**：厂商 SDK 或自研薄循环。

## 实施规则

- 选一个你能调试的框架——框架不如工具/检索质量重要。
- 先让单个工具齐备的 Agent 跑通，再上框架的多智能体能力。
- 若引入框架，务必理解底层代码——对底层机制的错误假设是常见错误来源。
- 从厂商 SDK 或你写的薄循环起步，只有当状态管理、多智能体协调、持久化执行真正成为瓶颈时才引入更重的框架。
- 多智能体框架应"挣得自己的位置"——不要因为模式本身酷就用它。

> 相关：五种架构模式见 `../arch/`；编排器-执行器细节见 `../orchestrator/`；失效模式见 `../failure/`。
