---
description: "Knowledge tree for designing, building and evaluating agents"
描述: "Agent 开发知识树导航"
name: "Agent Engineering"
名称: "Agent 开发"
---

# Agent 领域

本目录是 Agent 开发的核心知识树。Agent = 模型 + harness（harness = agent-loop + memory + tool）。下面每个知识点都是一个独立目录，目录内放该知识点的详细介绍。

## 知识点目录

| 目录 | 内容 |
|---|---|
| `intro/` | 定义、Chatbot/Workflow/Agent 对比、认知循环、核心组件、高价值场景 |
| `learning/` | 学习资源：按阶段整理的图书、课程网址与软件平台 |
| `knowledge-strategy/` | 综述：RAG 之外的模型外知识与会话外记忆方案对照与选型 |
| `patterns/` | 已展开为子树：react、plan-exec、Anthropic 5+1 模式、状态机与 DAG、ACI 三原则、self-correct、rewoo、tree-search（入口见 `patterns/patterns.md`） |
| `build/` | 九步构建流程、models、工具设计、评估、上线清单 |
| `eval/` | 三层评估（答案/轨迹/逐轮）、六指标、LLM-as-judge、框架与基准 |
| `context/` | context rot/collapse、ACE、提示缓存、记忆层级、六战术 |
| `multi/` | 已展开为子树：design、arch、orchestrator、handoff、A2A 协议、building、consensus、failure、frameworks（入口见 `multi/multi.md`） |
| `mcp/` | host-client-server、能力协商、原语、传输、安全、企业架构 |
| `channel/` | 综述：把外部消息系统桥接到 Agent 会话；含 dsh 的 QQ 渠道接入（入口 `channel/channel.md`） |
| `langgraph/` | 状态图、reducer、检查点、崩溃恢复、interrupt 审批、流式 |
| `safety/` | 致命三要素、双 LLM、CaMeL、威胁-控制映射、合规 |
| `obs/` | OTel 语义约定、黄金信号、平台对比、成本、漂移检测 |
| `coding/` | 脚手架差距、SWE-bench、主流工具、Computer Use、学习路径 |
| `browser-use/` | 浏览器 Agent：DOM 与视觉感知、框架对照、生产模式与安全边界 |
| `computer-use/` | 计算机操作 Agent：截图-坐标循环、厂商方案、OSWorld 基准与安全边界 |
| `action-surface/` | 行动面谱系：-use 家族、共享工具调用链与行动面选择 |
| `protocols/` | 互操作协议：MCP / A2A / ACP 同名消歧与按「对面是谁」选型 |
| `rl/` | Agent 训练与 RLVR、GRPO、多轮 rollout、奖励设计 |
| `frameworks/` | LangChain/LangGraph/LlamaIndex/CrewAI/AutoGen/SDK 选型 |
| `examples/` | react 模板、Function Calling、LangChain、CrewAI 可运行示例 |
| `prod/` | 护栏、评估、obs、成本优化、常见陷阱 |
| `prompt/` | CoT/自洽性/ToT、系统提示结构、结构化输出、提示缓存、评估驱动迭代 |
| `tool/` | 工具契约、schema、权限、幂等、中介层、注册表、测试与反模式 |
| `hooks/` | 生命周期拦截器、事件体系、中间件 hooks、上下文管理、时间旅行 |
| `skill/` | 可移植契约、SKILL.md 规范、渐进式披露、Graph-of-Skills |
| `workflow/` | 确定性 DAG、可配置节点、workflow-vs-agent 光谱、混合架构 |

## 建议阅读顺序

入门：intro → patterns → build → examples。深入：eval / context / multi / langgraph / safety。工程化：obs / prod。专项：coding / rl。选型：knowledge-strategy。渠道：channel。资源：learning。

工具调用的具体 API 字段规范见 `../api/`，检索增强见 `../rag/`，模型本身见 `../model/`。
