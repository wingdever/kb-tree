---
description: "AG-UI 1.0: event-based protocol between agents and user-facing apps, its 31 events, transports and state sync"
描述: "AG-UI 1.0：Agent 与用户界面之间的事件协议，31 种事件、传输与状态同步"
name: "AG-UI Protocol"
名称: "Agent 用户交互协议"
---

# Agent 用户交互协议（AG-UI）

AG-UI 解决的是**「Agent ↔ 用户界面」这一段**。它假设 Agent 不是请求-响应式的：它要流式吐 token、在回答中途调工具、和维护一份前后端共享的状态、随时停下来等人审批、还会派生子 agent。每个框架都用自己的方式做这些事，前端就得为每个框架重写一遍接线——AG-UI 把这件事标准化成**一条双向的带类型事件流**。

MIT 许可。1.0 已发布为**冻结规范**，带 JSON Schema，TypeScript / Python / .NET 三套 SDK 由 schema 生成；1.0 与 0.x 双向兼容（0.x agent 可被 1.0 client 消费，反之亦然）。

## 形态：一次 POST + 一条事件流

客户端发起一次 run，就是向 Agent 端点发一个 HTTP POST，body 是 `RunAgentInput`：

| 字段 | 作用 |
|---|---|
| `threadId` | 会话线程标识，跨轮延续的锚点 |
| `runId` | 本次执行标识 |
| `parentRunId` | 可选，指向同线程内的前一次 run，用于分支与时间旅行（git 式只追加日志） |
| `messages` | 对话历史（`user` / `assistant` / `system` / `developer` / `tool`） |
| `tools` | **仅**前端声明的工具（UI 动作、审批、读页面状态）；后端自己的工具不进这个字段 |
| `state` | 当前共享状态（可选） |
| `context` | 上下文片段 |
| `forwardedProps` | 透传字段 |

Agent 回一条**事件流**。事件严格带类型、可校验，全部继承自 `BaseEvent`（`type`、`timestamp`、`rawEvent`）。协议对传输不设强制绑定：规范定义了 HTTP + SSE 与 HTTP + Protobuf 二进制两种绑定，WebSocket、webhook 也算合法传输；中间件层允许把任意框架的原生事件"翻译"成 AG-UI 兼容事件，而不要求原生格式一致。

最小可用 Agent 只需三段：`RUN_STARTED` → 若干 `TEXT_MESSAGE_*` → `RUN_FINISHED`。**只有 run 生命周期是必需的**，其余事件族按需长出来。

## 工具分两侧：前端工具与后端工具

`RunAgentInput.tools` 装的**只是前端工具**，不是 Agent 的全部工具。协议明确区分两类：

| | 后端工具 | 前端工具 |
|---|---|---|
| 定义在哪 | Agent 框架配置 / MCP Server / 服务端代码 | 前端，随每次 run 放进 `RunAgentInput.tools` |
| 谁执行 | 服务端（可能再走 MCP） | App（浏览器、移动端、终端） |
| 典型用途 | 查数据库、调 API、读写文件、代码执行 | 弹确认框、导航、读页面/表单状态、调用设备能力 |
| 需要下发 schema 吗 | 不需要，服务端自己知道 | 需要，因为能力随前端状态变化 |

前端工具存在的理由是**能力只在客户端成立**：Agent 想知道"用户当前选中的是哪段文本"、"这张表单填了什么但还没保存"、"这次部署要不要点确认"，这些信息根本不在服务端。把这类动作声明成工具让 Agent 回调，比让服务端猜或让用户复述要可靠。

反过来，**后端工具不该塞进 `tools`**。官方写得很直白：这个字段只用于客户端提供的工具，不是"Agent 能用的所有工具"的清单；后端工具应定义在后端框架里，或通过 Agent 能力声明暴露。把后端工具 schema 从客户端发出去，会让"工具权限"跟着客户端跑——任何能构造请求的客户端都能自称拥有一批高危工具。

几条实现上的约束：

- **工具结果要校验**。前端工具的结果回到 Agent 时是 `role:"tool"` 消息，本质是不可信输入；服务端不能因为它"看起来像自己的工具返回"就跳过校验。
- **失败必须显式**。`ToolMessage` 的 `error` 字段是唯一能区分"执行失败"与"成功返回了失败文案"的标记，缺了它 Agent 只能靠猜。
- **元数据挂在 tool call 上**。`TOOL_CALL_*` 的 `metadata` 累积到具体那次调用，而不是挂到拥有它的 assistant 消息上——一条消息可以带多个并行调用，挂到消息上结果会随交错顺序变化。
- **同名冲突**。前后端各有一个 `search` 时，到底谁执行、谁兜底，必须在接线层定死，不能依赖模型自己分辨。

> 判断：工具放哪侧，看「执行需要谁的上下文」。需要用户界面状态、用户权限或人在环确认 → 前端；需要数据、文件、外部系统 → 后端。两边都要的，做成前端发起、后端执行的组合，而不是把后端能力搬到前端。

### 常见前端工具清单

按用途分八类。清单是**设计参照**，不是必选集合——按产品实际界面裁剪，能用页面状态直接读的就别包成工具。

| 类别 | 典型工具 | 入参要点 | 回给 Agent 的结果 |
|---|---|---|---|
| 确认 / 审批 | `confirmAction`、`requestApproval` | 动作描述、风险等级、影响范围 | `approved` / `rejected` / `modified` 加用户备注 |
| 追问 / 澄清 | `askUser`、`requestChoice`、`requestInput` | 问题、候选项、是否允许自由输入、必填字段 | 用户输入或所选选项，结构化返回 |
| 导航 / 聚焦 | `navigateTo`、`focusElement`、`revealPanel`、`scrollTo` | 目标页面或元素 id、参数 | 是否成功、当前位置 |
| 读界面状态 | `getSelection`、`getFormDraft`、`getViewState`、`getOpenTabs` | 通常无参或指定容器 id | 选中文本与范围、未保存草稿、筛选与分页、打开的标签 |
| 渲染 / 展示 | `renderChart`、`renderTable`、`renderDiff`、`showPreview` | 结构化数据或规格（图表 spec、diff 双版本） | 渲染是否成功、组件句柄或快照 id |
| 编辑 / 写入（客户端侧） | `applyEdit`、`fillForm`、`insertText`、`undo` | 目标位置、内容或补丁 | 改后状态、是否触发冲突 |
| 设备 / 本地能力 | `pickFile`、`saveFile`、`copyToClipboard`、`captureScreenshot` | 类型过滤、路径或内容、格式 | 文件句柄或 URL、是否成功 |
| 提示 / 进度 | `notifyUser`、`reportProgress` | 文案、级别、步骤与百分比 | 仅确认送达 |

选型上有几条经验：

- **读优先于问**。当前选中文本这类信息用 `getSelection` 读，比让模型问用户“你选了什么”体验好得多，也少一轮往返。
- **一次只做一件事**。`doAction(action)` 这种万能工具会让模型在参数里自造语义，选择准确率明显下降；`navigateTo` 与 `applyEdit` 必须分开。
- **审批类工具要有风险分级**。`importance` 这类枚举让前端决定弹多重确认，而不是让模型自己判断“这个操作危险吗”。
- **结果是给模型看的**。返回结构化字符串（状态 + 关键字段），不要回一大段 UI 文案；失败必须设 `ToolMessage.error`。
- **敏感的读要单独评审**。`getClipboard`、`captureScreenshot` 这类能拿到用户私人内容的工具，等于把客户端隐私面暴露给模型，默认不给，按需临时授权。
- **按上下文动态暴露**。只在代码页暴露 `applyEdit`、只在表格页暴露 `renderTable`；一次全量塞进 `RunAgentInput.tools` 会拖低工具选择准确率。

## 事件：8 族、31 种

| 族 | 事件 | 用途 |
|---|---|---|
| 运行与步骤 | `RUN_STARTED` `RUN_FINISHED` `RUN_ERROR` `STEP_STARTED` `STEP_FINISHED` | 运行边界与可观测的进度分段 |
| 文本消息 | `TEXT_MESSAGE_START` `TEXT_MESSAGE_CONTENT` `TEXT_MESSAGE_END` `TEXT_MESSAGE_CHUNK` | token 级流式正文 |
| 工具调用 | `TOOL_CALL_START` `TOOL_CALL_ARGS` `TOOL_CALL_END` `TOOL_CALL_RESULT` `TOOL_CALL_CHUNK` | 工具参数流式下发与结果回填 |
| 状态 | `STATE_SNAPSHOT` `STATE_DELTA` `MESSAGES_SNAPSHOT` | 共享状态同步 |
| 推理 | `REASONING_START` `REASONING_MESSAGE_*` `REASONING_ENCRYPTED_VALUE` `REASONING_END` | 思考过程单列，不混入正文 |
| 活动 | `ACTIVITY_SNAPSHOT` `ACTIVITY_DELTA` | 长任务的进行中活动 |
| 子 Agent | `SUBAGENT_STARTED` `SUBAGENT_FINISHED` `SUBAGENT_ERROR` | 嵌套委派与事件归属 |
| 透传 | `RAW` `CUSTOM` | 原样透传与自定义扩展（如 token 用量） |

三种流式模式贯穿全协议：

- **Start–Content–End**：文本与工具调用都走这个骨架，`delta` 逐片追加。
- **Snapshot–Delta**：状态先用全量快照打底，之后只发增量。
- **Started–Finished/Error**：生命周期成对出现。

拼接规则很硬：文本按 `messageId` 累加，工具参数按 `toolCallId` 累加。**并行工具调用的事件会交错到达**，客户端必须按 id 分桶而不是按到达顺序拼接；`TOOL_CALL_END` 只表示参数发完，不代表工具执行成功，执行结果在 `TOOL_CALL_RESULT`。

## 状态同步

`STATE_SNAPSHOT` 给全量，`STATE_DELTA` 用 **JSON Patch（RFC 6902）** 只发变更，`MESSAGES_SNAPSHOT` 给完整对话历史。这样一份状态可以同时被前后端读写：前端改表单，Agent 读得到；Agent 改结构，前端立刻重渲染。相比"每轮把整份状态塞进 prompt"，增量同步省带宽也避免模型看到过期副本。

> 判断：状态放哪一侧要看谁需要实时性。前端需要即时反馈的状态放共享 store，只影响模型推理的中间结果留在服务端，不要为了"统一"把两者都塞进事件流。

## 人在环：中断与恢复

run 不必总是走到 `RUN_FINISHED` 的成功分支。1.0 里 `RUN_FINISHED` 的 `outcome` 是判别联合：`{type:"success"}` 或 `{type:"interrupt", interrupts:[...]}`。Agent 在需要审批、补充信息、或让用户在多个方案里选时以 interrupt 收尾；前端展示、用户批准/编辑/拒绝后，**下一次 run 带着恢复信息继续**。

这条设计的含义是：**HITL 不是"暂停一个长连接"，而是"结束一次 run、再开一次 run"**。因此恢复所需的上下文（已执行到哪、副作用做到哪）必须由服务端持久化，否则恢复会重放已完成的副作用。

### 中断与前端工具的分工

两套机制都能"等人"，但适用的等待性质不同，混用会让状态机变复杂：

| | 前端工具（`TOOL_CALL`） | 中断（`outcome:"interrupt"`） |
|---|---|---|
| 作用范围 | 一次工具往返，run 继续 | 结束本轮 run，控制权交给用户 |
| 等待时长 | 秒级，当前会话内 | 分钟到小时，可跨设备、跨天 |
| 恢复方式 | 前端执行完塞回 `ToolMessage`，同一 run 继续 | 下一次 run 带恢复信息重新开始 |
| 状态要求 | 服务端无需持久化中间态 | 服务端必须持久化 checkpoint 与本轮输入 |
| 典型场景 | "这段要部署，确认吗"、读当前选中文本、跳到某页 | 用户要离线审阅方案、多轮编辑同一份输入、等外部审批 |

判断标准很简单：**结果能在当前 run 内拿到，就用前端工具；需要结束 run 等人，就用 interrupt**。

两种误用各有代价。把审批做成前端工具，用户一离开页面 run 就卡在一个等待中的工具调用上，连接断了还得重放；把秒级确认做成中断，每次点个"确定"都要重启一轮 run，会话历史被切成碎片，前端状态与 checkpoint 也很难对齐。

还有一点：中断恢复**不等于重跑**。恢复时要把已完成的副作用记录带上（哪些写操作已生效、哪些工具已返回），否则模型会重新规划、把"已部署"再部署一遍。这类重复副作用在 HITL 里是最常见的线上事故。

## 生成式 UI 的边界

Agent 想在界面上渲染组件时，有两种分工：

- **AG-UI** 是**运行时载体**——把事件（包括 UI 意图载荷）从 Agent 送到 App。
- **A2UI / MCP Apps / Open-JSON-UI** 是**UI 规格**——描述"要展示什么组件树"。

别把两者混为一谈：A2UI 不是 AG-UI 的替代品，也不是它的子协议；AG-UI 只负责把那份声明送到能渲染它的客户端。

## 三条路径各管一段

| | AG-UI | MCP | A2A | ACP |
|---|---|---|---|---|
| 连接 | Agent ↔ 用户界面 | Agent ↔ 工具/数据 | Agent ↔ Agent | 编辑器 ↔ 编码 Agent |
| 典型载体 | HTTP/SSE、Protobuf 二进制 | JSON-RPC | JSON-RPC/gRPC/HTTP | JSON-RPC over stdio |
| 谁发起 | 前端应用 | Agent（作为客户端） | 协作方 Agent | 编辑器 |

一个 Agent 常常三者都用：AG-UI 面向用户，MCP 取工具，A2A 找别的 Agent；AG-UI 还能为"只会说 MCP 或 A2A"的 Agent 当前端外壳。

## 接入方式

- **客户端**：`HttpAgent`（TypeScript `@ag-ui/client`）连任意接受 `RunAgentInput` 的 POST 端点；Python 用 `ag-ui-protocol`；.NET 用 `AGUI.Client`。事件回调按类型分派（`onTextMessageContentEvent` 之类）。
- **前端栈**：CopilotKit 覆盖 React、Angular、Vue、React Native（同许可 MIT）；另有 Slack / Teams 通道、终端客户端、OpenBot。
- **框架侧内置**：LangChain/LangGraph、CrewAI、Mastra、Google ADK、Microsoft Agent Framework（`MapAGUIServer`）、AWS Strands、Pydantic AI、Agno、LlamaIndex 等，多数提供现成 endpoint 包装，把框架原生 stream 映射成 AG-UI 事件。
- **脚手架**：`npx create-ag-ui-app@latest` 直接生成「框架 + 前端」的可运行骨架。

## 服务端要决定的两件事

**有状态还是无状态**。无状态实现里，客户端每次把完整 `messages` 重发；有状态实现里，服务端按 `threadId` 挂一份 session，客户端只发新消息，并用 `parentRunId` 指认"这是在续哪一次 run"。后者省带宽，但要求会话持久化与隔离。

**事件 id 与可重放**。SSE 事件带递增 id，客户端记录"最后一条完整处理过的 id"，断线后用同一 `threadId` / `runId` 加 `afterSequence` 重连，只补发后续事件——**这是 attach，不是重跑**；换个 `runId` 重发等于重新执行，会重复副作用。明确停止要调 stop 接口，只关连接往往只断开了订阅，run 还在跑。

## 工程上的常见坑

- **只实现文本事件**。前端看不到工具调用与审批，产品只能当"更快的聊天框"，AG-UI 的价值全丢。
- **按到达顺序拼工具参数**。并行调用交错时参数被拼错，且错得很难复现。
- **SSE 被中间层缓冲**。反向代理开了响应缓冲，事件攒成一批才到，表现为"流卡住然后一次性刷出来"。
- **空闲超时杀连接**。服务端要发 SSE 保活注释（常见实现每 15 秒一条），代理的 idle timeout 要小于这个间隔；否则长思考时连接被掐。
- **把 `threadId` 当授权凭证**。官方明确这两个 id 是协议数据、不是身份凭证，鉴权必须另有机制，否则换个 id 就能读别人的会话。
- **中断恢复不带状态**。恢复时重新规划、重新执行已完成的写操作。
- **多端同时订阅同一线程**。两个客户端都在跑同一 `threadId`，状态 delta 互相覆盖；需要单写者或显式接管。
- **用文本事件承载工具结果**。前端无法结构化渲染，也破坏了 `TOOL_CALL_RESULT` 的语义。

## 什么时候不必用

纯单轮问答、没有共享状态也没有工具展示需求时，直接一次 HTTP 返回更快；自建私有协议只在"永远只有一个前端"时才划算——一旦要接第二个客户端（移动端、Slack、终端），重写接线的成本会超过一开始就用协议。

## 参考资料

- AG-UI 事件参考（8 族事件与字段）：https://docs.ag-ui.com/concepts/events
- AG-UI 工具概念（前端工具 vs 后端工具、工具调用生命周期、`error` 语义）：https://docs.ag-ui.com/concepts/tools
- AG-UI 核心架构（设计原则、`HttpAgent`、传输、状态）：https://docs.ag-ui.com/concepts/architecture
- 协议仓库与 1.0 变更说明（MIT）：https://github.com/ag-ui-protocol/ag-ui
- AG-UI 1.0 发布说明：https://www.copilotkit.ai/blog/ag-ui-1.0
- 微软 Agent Framework 的 AG-UI 接入（`MapAGUIServer`、SSE 保活、会话延续）：https://learn.microsoft.com/agent-framework/integrations/ag-ui/getting-started
- 阿里云 AgentCore 的 AG-UI 实践细节（事件 id、`afterSequence` 重连、stop 语义）：https://help.aliyun.com/zh/agentcore/ag-ui-protocol-reference
