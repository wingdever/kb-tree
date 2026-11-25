---
description: "Framework orchestration models, what frameworks actually buy, version traps and build-vs-buy"
描述: "多智能体框架的编排模型、框架真正买到的东西、版本陷阱与自研判断"
name: "Multi-Agent Framework Implementations"
名称: "多智能体框架实现"
---

# 多智能体框架实现

选择框架很大程度上决定了哪些模式容易实现。你选的框架决定了编排的"形状"。

但先摆正位置：**框架不是能力来源**。同一个模型、同一套工具，换框架后质量变化通常远小于换检索质量、换工具描述、换评估方式带来的变化。框架买到的是"状态、并发、可观测这些工程设施"，不是"更聪明的 Agent"。

## 框架映射

| 框架 | 编排模型 | 状态与持久化 | 甜点区 |
|---|---|---|---|
| **LangGraph** | 图 / 状态机，你定义节点和边 | 图状态 + 检查点，可中断恢复 | 可控、有状态、人在回路；分支/暂停恢复/可检查执行 |
| **CrewAI** | 基于角色的 crew（角色、目标、任务），顺序或 hierarchical process | 任务级流程，持久化较弱 | 快速搭专门角色团队；可读的声明式定义 |
| **AutoGen / AG2** | 对话式 Agent，群聊 + 管理者 | 会话内为主 | 对话与代码执行团队；对话式多智能体工作流 |
| **OpenAI Agents SDK** | 轻量 Agent + 工具 + handoffs + guardrails | 会话级（sessions） | 以交接为中心、带护栏的流程；manager 模式 |
| **Google ADK** | 会话/状态与编排分离 | 会话状态与编排解耦 | 会话状态与编排解耦 |
| **Microsoft Agent Framework** | concurrent 模式（对应 sectioning 并行化） | 工作流与 Agent 分层 | 并行扇出；从 AutoGen/Semantic Kernel 迁移 |

## 各框架与模式的对应

- **层级/监督者**：LangGraph 的 supervisor 模式、`create_supervisor()`（LangChain 更推荐直接用工具调用实现以控制上下文）；CrewAI 的 hierarchical process（自动 manager）；OpenAI Agents SDK 的 manager 模式。
- **网络/Swarm**：LangGraph 的 swarm 实现——Agent 直接交接，系统记住最后活跃的 Agent；OpenAI Agents SDK 的 handoffs（triage Agent 路由到专家，专家接管该轮）。
- **群体聊天**：AutoGen / AG2 的 group chat + speaker selection；LangGraph 的双节点互评模板。
- **顺序/流水线**：各框架都可用线性链实现；CrewAI 的 sequential process。
- **黑板/共享状态**：需要自定义共享工作区 + 控制组件；工具尚不成熟。

## 框架真正买到的三件事

| 能力 | 自己做要付出什么 | 框架给什么 |
|---|---|---|
| 状态与恢复 | 自己设计状态 schema、检查点、重放 | 图状态 + checkpointer，失败从最后节点续跑 |
| 人在回路 | 自己做中断、挂起、恢复、审批超时 | `interrupt` / 审批节点，暂停在边上等人 |
| 可观测 | 自己埋 trace、串 span、对齐成本 | 回调与追踪钩子，直接接评估平台 |

这三件事才是引入框架的理由。反过来，如果任务只需要"一个循环 + 几个工具 + 一次汇总"，框架带来的抽象成本会高于收益——读三层源码才能知道一次工具调用实际怎么走。

## 版本与文档陷阱

- **API 换代快**：同一条"监督者"能力，官方可能从专用构造函数改为"用工具调用自己实现"，旧教程与旧博客仍在传播前者。选型时以官方仓库当前版本为准，不以搜索排名第一的文章为准。
- **文档站会失效**：部分框架的文档站偶发不可达，仓库 README 与示例目录反而更稳；把仓库固定在参考资料里，比只写文档域名可靠。
- **归属与改名**：组织迁移、项目合并（如多智能体平台并入统一 Agent Framework）会让旧包名继续存在但不再更新，克隆/安装前先确认当前仓库。
- **版本锁定**：框架升级会改变默认行为（重试、并发、提示拼装），把版本写进依赖锁，并用回归集验证升级。

> 判断：框架选型的第一原则是"你能读到它的循环"。读不到执行路径的框架，出问题时只能靠猜；可读性比功能表更重要。

## 自研薄循环的判断

以下任意两条成立，就先用自研薄循环，不上框架：

- 循环逻辑能在 100 行内写完，且不需要持久化。
- 团队里没人能解释框架一次调用的完整路径。
- 需求是单 Agent + 工具，多智能体只是"可能以后要"。
- 关键约束在权限与审计上，而框架的默认放行策略要逆着改。

反过来，出现"长任务要断点续跑""多角色要共享状态""审批要卡在流程中间"这三类需求时，框架的收益才开始明显。

## 选择与取舍

- 追求**可控与可恢复**：LangGraph（状态图、检查点、人在回路）。
- 追求**快速角色化原型**：CrewAI（声明式 crew 定义快，但内置可观测性较弱）。
- 追求**对话/代码执行团队**：AutoGen（群聊范式，偏研究与对话）。
- 追求**交接与护栏**：OpenAI Agents SDK（handoff-centric + guardrails）。
- 追求**多语言/多云与企业集成**：Google ADK 或 Microsoft Agent Framework。
- 追求**贴近底层、最小依赖**：厂商 SDK 或自研薄循环。

## 实施规则

- 选一个你能调试的框架——框架不如工具/检索质量重要。
- 先让单个工具齐备的 Agent 跑通，再上框架的多智能体能力。
- 若引入框架，务必理解底层代码——对底层机制的错误假设是常见错误来源。
- 从厂商 SDK 或你写的薄循环起步，只有当状态管理、多智能体协调、持久化执行真正成为瓶颈时才引入更重的框架。
- 多智能体框架应"挣得自己的位置"——不要因为模式本身酷就用它。
- 把框架当依赖管理，不当架构：核心状态 schema、工具契约、验收标准要写在你自己能控制的层里，换框架时不至于重写。

## 一句话主线

框架的价值在**状态、中断、可观测**这三件工程设施上，不在"能不能多智能体"；选型的判据是能否读懂它的循环，而不是功能表长度。

## 参考资料

- LangGraph 官方文档：https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph 持久化与检查点：https://docs.langchain.com/oss/python/langgraph/persistence
- CrewAI 仓库：https://github.com/crewAIInc/crewAI
- AutoGen 仓库与文档：https://github.com/microsoft/autogen
- OpenAI Agents SDK 文档：https://openai.github.io/openai-agents-python/
- Google ADK 文档：https://google.github.io/adk-docs/
- Microsoft Agent Framework 文档：https://learn.microsoft.com/en-us/agent-framework/
