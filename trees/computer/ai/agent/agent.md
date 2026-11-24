---
description: "Knowledge tree for designing, building and evaluating agents"
描述: "Agent 开发：基础、架构、互操作、工程、运维与进阶"
name: "Agent Engineering"
名称: "Agent 开发"
---

# Agent 领域

本目录是 Agent 开发的核心知识树。Agent = 模型 + harness（harness = agent-loop + memory + tool）。知识点按学习/生命周期阶段归成六个分组，每组是一个目录 + 同名介绍 md，子知识继续在其下展开。

## 六个分组

| 分组 | 关注什么 |
|---|---|
| **fundamentals** | Agent 的构成与上下文工程：循环、提示词、工作流、知识与记忆放在哪里 |
| **architecture** | 行动面（工具 / 代码 / 浏览器 / 桌面）、设计模式、多智能体、图式编排与生命周期钩子 |
| **interop** | 工具契约、MCP、技能、消息渠道，以及客户端与 Agent 间协议（A2A / ACP） |
| **engineering** | 构建方式、评测与黄金集、主流框架、安全与权限边界 |
| **operations** | 可观测性、成本与延迟、生产部署与灰度 |
| **advanced** | 编码 Agent 专项、学习路径与强化学习方向 |

分组的顺序对应 Agent 从设计到上线的生命周期：先想清楚它由什么组成，再决定它怎么动手、怎么与外部世界对接，然后用工程手段保证质量与安全，最后才谈规模化运行和专项深入。

