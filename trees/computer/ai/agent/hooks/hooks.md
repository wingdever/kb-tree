---
description: "Agent hooks and middleware: lifecycle interceptors, event taxonomy and deterministic policies around the loop"
描述: "Agent Hooks 与中间件：生命周期拦截器、事件体系与环绕循环的确定性策略"
name: "Agent Hooks and Middleware"
名称: "Agent Hooks 与中间件"
---

# Hooks 与中间件

Hooks 是在 Agent 生命周期关键节点上可注册的回调。实现上常借助事件机制，但**重点不是发事件，而是在特定时机插入逻辑**——可以修改输入输出、阻止执行、改变下一步走向，即"生命周期拦截器 + 回调"，能够干预流程。

为什么需要：很多事情不能靠提示词解决（PII 脱敏、合规、重试、限流、人在回路）。这些是**确定性策略，必须每次都触发**——你无法用提示词实现 HIPAA 合规。中间件让这些策略在运行时环绕 Agent 循环的每个步骤确定性执行。

## 事件类型体系

工作流生命周期：

| 事件 | 含义 |
|---|---|
| `WORKFLOW_STARTED` / `WORKFLOW_COMPLETED` | 工作流开始 / 完成 |
| `AGENT_STARTED` / `AGENT_COMPLETED` | Agent 开始 / 完成 |

执行状态：

| 事件 | 含义 |
|---|---|
| `TOOL_INVOKED` | 工具调用 |
| `TOOL_OBSERVATION` | 工具返回 |
| `AGENT_THINKING` | 思考中 |
| `ERROR_OCCURRED` | 出错 |

工作流控制：

| 事件 | 含义 |
|---|---|
| `WORKFLOW_PAUSED` / `WORKFLOW_RESUMED` / `WORKFLOW_CANCELLED` | 暂停 / 恢复 / 取消 |
| `APPROVAL_REQUESTED` / `APPROVAL_DECISION` | 请求审批 / 审批结果 |

LLM 事件：

| 事件 | 含义 |
|---|---|
| `LLM_PROMPT` | 发给 LLM 的内容 |
| `LLM_PARTIAL` | LLM 增量输出 |
| `LLM_OUTPUT` | LLM 最终输出 |

## LangChain v1 中间件（2026 主流实现）

Middleware 通过 hooks 在每步前后运行自定义逻辑，可组合：

| Hook | 时机 | 用途 |
|---|---|---|
| `before_agent` | 调用 Agent 前一次 | 加载记忆、连接资源、校验初始输入 |
| `before_model` | 每次模型调用前 | 裁剪历史、PII 检查后再进 LLM |
| `wrap_model_call` | 环绕每次模型调用 | 缓存、重试、动态换模型/工具 |
| `wrap_tool_call` | 环绕每次工具调用 | 注入上下文、拦截结果、门控哪些工具真执行 |
| `after_model` | 模型响应后、工具执行前 | 人在回路最自然的位置 |
| `after_agent` | Agent 完成后一次 | 保存结果、通知、清理 |

内置中间件：`PIIMiddleware`、`ModelRetryMiddleware`、`ModelFallbackMiddleware`、`ToolCallLimitMiddleware`、`SummarizationMiddleware`、`HumanInTheLoopMiddleware`、`OpenAIModerationMiddleware`。自定义则继承 `AgentMiddleware` 实现任意 hook。

## 典型用途

- **业务逻辑与合规**：PII 脱敏、内容审核——必须每次确定性触发。
- **动态 Agent 控制**：按状态注入工具、任务中途换模型、随上下文更新系统提示。如 `LLMToolSelectorMiddleware` 在 `wrap_model_call` 里跑快速 LLM 选相关工具，减少主调用的工具上下文膨胀。
- **上下文管理**：接近 token 上限时摘要（`SummarizationMiddleware` 实现 `before_model`）、把冗长工具输入输出卸载到文件系统（`wrap_tool_call`）——**上下文工程是运行时问题，不是一次性提示问题**。
- **生产就绪**：模型/工具重试、fallback、人在回路中断。

## 与运行时的关系

Middleware 不是独立运行时——hooks 在 `create_agent` 返回的编译后 LangGraph 内运行。可把整个 Agent（含中间件）作为节点或子图放进更大 StateGraph，所有 hooks 继续生效。这让护栏与埋点不是"best effort"，而是无论流式、暂停/恢复、重试、后台运行都环绕每个模型/工具调用、在你预期的精确点执行。

中间件还能**封顶昂贵操作**：能调用付费 API 的 Agent 需要硬上限，否则困惑的模型会调用五十次烧光预算——`ToolCallLimitMiddleware` 处理。

## 可观测性与时间旅行

围绕 middleware 的追踪给出完整执行树（模型调用、工具调用、子 Agent、middleware hooks）。时间旅行：每个 super-step 写检查点，可从历史任一检查点分叉、改状态、重放——LLM 调用、工具调用、中断在重放时重新触发，走真实 Agent 循环而非桩。用于调试"为何选了工具 A 而非 B"、对比两个提示、从错误状态回退。

> 相关：状态机与检查点见 `../patterns/stategraph/`；上下文管理见 `../context/`；护栏与安全见 `../safety/`；LangGraph 见 `../langgraph/`。
