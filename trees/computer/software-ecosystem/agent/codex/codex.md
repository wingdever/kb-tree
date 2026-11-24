---
description: "OpenAI Codex: a coding agent exposed through CLI, IDE extension, desktop app and cloud, with sandboxing and plan-based usage"
描述: "OpenAI Codex：通过 CLI、IDE 扩展、桌面 App 与云端提供的编码 Agent，含沙箱与套餐用量"
name: "OpenAI Codex"
名称: "OpenAI Codex"
---

# OpenAI Codex

> 来源：OpenAI Codex 官方文档与 openai/codex 仓库。产品形态、模型与计费方式变化快，以官方文档为准。

Codex 是 OpenAI 的**编码 Agent**：读取仓库、修改文件、运行命令与测试，并根据结果反复迭代直到完成任务。官方现在把它描述为**一个 Agent、多个客户端（surfaces）**——同一 Agent 通过 CLI、IDE 扩展、桌面 App 与云端四种入口提供，区别在运行位置，不在能力本身。它与 ChatGPT Work 并列：Chat 用于对话，Work 用于长步骤的通用工作，Codex 专攻软件开发；两者共用桌面 App，也共用同一份用量额度。

## 四种形态

- **CLI**：运行在开发者本机终端，面向本地仓库。可探索陌生代码、制定改动计划、编辑文件、运行本地工具链；支持 `AGENTS.md` 项目指令、worktree 与内置 Git 工具。`codex exec` 可嵌入脚本与 CI。主要用 Rust 编写，以 Apache-2.0 开源在 `openai/codex` 仓库。
- **IDE 扩展**：运行在 VS Code、VS Code Insiders、Cursor、Windsurf 等 VS Code 系编辑器中，围绕当前打开的文件与选区工作，在编辑器内审阅 diff。Xcode 与 JetBrains 通过各自集成方式接入。**它不是代码补全工具**，不提供边打边补的 inline autocomplete。
- **桌面 App**：ChatGPT 桌面应用内的 Codex，管理项目、文件与长时间任务，同一个 App 里可选 ChatGPT 或 Codex 开始对话。
- **云端**：运行在 OpenAI 托管的工作区，连接 GitHub 仓库后每个任务有独立 workspace，电脑休眠后任务继续运行；可并行多个任务，完成后展示改动与测试结果，由人审阅再提交或开 PR。入口包括网页、桌面 App 与手机端。另有 GitHub PR 自动代码审查与 Slack 集成。

## 登录、沙箱与管控

- **两条登录路径**：ChatGPT 账号走套餐额度；OpenAI API Key 按 API 标准价计费，适合 CI 与自动化，但不含云端功能（云端任务必须用 ChatGPT 账号登录）。
- **本地沙箱**：默认 workspace-write 沙箱、按需请求批准、网络默认关闭。管理员可通过 `requirements.toml` 禁止完全访问、禁止实时联网搜索、禁止未经批准的 MCP server。
- **其他运行路径**：可通过 `--oss` 跑在 Ollama / LM Studio 上，也可走 Amazon Bedrock；每条路径都会改变企业管控与功能可用性。
- **数据流向**：ChatGPT workspace 登录遵循该 workspace 的留存与驻留设置；API Key 登录遵循 API 组织的设置；本地 transcript 默认留在开发者机器上。

## 架构

Codex 的智能体逻辑集中在开源仓库 `openai/codex` 的 `codex-rs/` Rust workspace 中。理解它的关键是：**同一内核、多个客户端**——CLI、TUI、exec、桌面 App 与云端都是这一个内核的不同外壳。

### 分层

按依赖方向自上而下：

| 层 | 代表 crate | 职责 |
|---|---|---|
| 入口 | `cli`、`tui`、`exec`、`app-server` | 收集输入、渲染输出、管理进程生命周期，不承载业务逻辑 |
| 会话核心 | `core` | agent loop、turn 循环、工具路由、审批、上下文压缩、会话持久化 |
| 协议 | `protocol`、`app-server-protocol` | 定义 `Op` / `EventMsg` 内部协议与外部 JSON-RPC；TS schema 由 Rust 类型生成 |
| 模型客户端 | `model-provider`、`codex-api`、`codex-client`、`responses-api-proxy` | Responses API 封装、流式解析、重试、多端点支持 |
| 执行与沙箱 | `sandboxing`、`linux-sandbox`、`windows-sandbox-rs`、`mxc-sandbox`、`network-proxy`、`execpolicy`、`shell-command`、`tools` | 把模型动作翻译成受限的真实命令，施加文件与网络策略 |
| 状态 | `state`、`thread-store`、`rollout`、`history`、`memories` | 会话历史、线程状态、断点恢复 |
| 横切 | `config`、`login`、`keyring-store`、`analytics`、`otel`、`features` | 配置分层合并、认证、遥测、特性开关 |

npm 包 `@openai/codex` 只是下载并启动对应平台原生二进制的薄壳；构建在 `codex-rs/` 下进行。

### Agent loop

内核用一对异步 channel 连接客户端与执行流：**Submission Queue** 承载客户端发来的 `Op`，**Event Queue** 承载内核产生的 `EventMsg`。客户端只发 `Op`、只轮询事件，永不阻塞在模型推理上，因此 TUI 能在推理期间持续渲染流式 token 并处理按键。

一次会话有三层循环：最外层 `submission_loop` 持续接收 `Op` 直到 `Shutdown`；中层的 `run_turn` 把「从用户输入到最终 assistant 消息」定义为一次 turn，并在开始时捕获一份上下文快照（模型、cwd、指令、审批与沙箱策略、工具配置），保证模型所见与随后执行基于同一视图；内层 tool loop 反复「采样 → 执行工具 → 回灌结果」，直到模型不再请求工具、只产出 assistant 消息为止。

终止标志是 `needs_follow_up`：遇到工具调用置为真并继续，遇到普通 assistant 消息置为假并结束该轮。工具执行并非全部并行——需模型族声明支持、特性开关打开，且该工具被标记为并行安全；实现上用读写锁区分并行安全与非并行工具。

### 提示词与上下文

每次推理请求的 `input` 按固定顺序拼装：模型定制的 instructions、工具列表、当前沙箱下的权限声明、`config.toml` 里的 developer 指令、从 git 根到当前目录逐级聚合的 `AGENTS.md` 与技能元数据、环境上下文、用户消息。角色优先级 system > developer > user > assistant，使平台级安全规则不能被项目内指令覆盖。

Codex 不使用 `previous_response_id`，每轮带完整历史（为支持零数据保留客户），传输量随会话呈 O(n²) 增长。Prompt caching 靠**精确前缀匹配**把成本拉回 O(n)，这带来两条工程约束：工具枚举必须确定性（MCP 工具顺序不稳定曾导致每次推理都 cache miss），以及配置或目录变化时不要改老消息，而是**追加一条新消息**，以保住缓存前缀。会话超过阈值时调用 compaction 端点，用保留模型潜在理解的不透明载荷替换旧输入，而非普通文本摘要。

### 沙箱实现

Codex 不用 VM 或容器做默认隔离，而是用各平台原生沙箱约束「在用户现有环境中运行的命令」——理由是本地开发环境难以在容器里复现。统一入口 `spawn_command_under_sandbox` 接受命令、cwd、环境变量、权限剖面与可选网络代理，子进程继承父进程约束，因此限制覆盖整棵进程树。

权限剖面描述文件与网络规则。内置的 `:workspace` 剖面以 Git 仓库为根，工作区内可写但 `.git`、`.codex` 等只读，全盘宽读，默认禁网；另有 `:read-only` 与 `:danger-full-access`。配置按表递归合并、数组整体替换，这正是路径与域名规则用表而非数组表达的原因。

三平台实现不同：macOS 用 Seatbelt（SBPL 策略，以 `(deny default)` 开头，只放行本地代理端口）；Linux 用 bubblewrap 建挂载命名空间，再由内部启动器施加 seccomp-bpf 后 exec 用户命令，并通过 Unix socket 控制通道把 loopback 监听器 fd 交给沙箱外进程，实现网络代理穿透命名空间；Windows 从受限令牌 + ACL 迁移到 MXC。网络层先判定域名是否允许再做 DNS 解析，因为 DNS 查询本身会泄露主机名。

### 协议与客户端

内部协议是 `Op` 进、`EventMsg` 出；外部 app-server 用 JSON-RPC over stdio（省略 `jsonrpc` 字段，官方称 JSON-RPC lite），以 **thread / turn / item** 三原语暴露内核：thread 是持久会话，turn 是一次由用户输入发起的工作单元，item 是原子输入输出单元。协议全双工，服务端可在需要审批时反向发起请求并暂停 turn，等客户端回应。客户端连接前必须先 `initialize` 握手协商版本与特性。

之所以不直接用 MCP：把 Codex 暴露成 MCP server 时，在编辑器语境下维持 MCP 语义很困难，于是做了镜像 TUI loop 的 JSON-RPC。两者都包同一个内核，但 MCP 是工具中心，app-server 是 thread/turn/item 中心。脚本与 CI 用 `codex exec`，想让其他 Agent 把 Codex 当工具调用用 `codex mcp-server`，应用内以代码启动任务用 SDK。

### 开发资料与阅读路线

官方工程博客是理解设计意图的一手材料：Agent loop 篇讲 turn、Responses API 端点、提示词拼装与上下文；App Server 篇讲协议起源与进程结构；沙箱篇讲三平台实现与网络代理；另有 Windows 沙箱篇与「Codex as a Platform」讲开源边界。

源码阅读按依赖顺序：先读 CLI 入口与 `protocol/src/protocol.rs` 里的 `Op` / `EventMsg` 全貌，再读 `core/src/codex.rs` 的 channel 创建、`core/src/session/turn.rs` 的 `run_turn`，然后沿工具路由与编排器走到沙箱实现，最后看 app-server 如何把内部事件收敛成 JSON-RPC 通知。加协议的改动要同步各前端；加工具要在 handlers 实现并在 spec 中注册、声明沙箱与审批行为；TS schema 由 Rust 生成，不可手改。

注意一个常见误读：社区文章里的「RMCP (Remote Model Communication Protocol)」并不存在，RMCP 只是 Rust 版 MCP SDK 的名字，与 Codex 自有协议无关。仓库迭代极快，目录会漂移，把分层当心智模型，具体以本地 clone 的版本为准。

## 定位与边界

- 与 Claude Code、Cursor、GitHub Copilot 等编码 Agent 相比，Codex 的差异化是**同一 Agent 跨 CLI / IDE / 桌面 / 云端四种入口**，以及云端任务在电脑休眠后仍继续、以 PR 交付结果的闭环。
- 没有独立的 Codex 订阅：能力随 ChatGPT 各档套餐提供，各档开放的形态与额度不同，超出可用积分续用；也可走 API Key 按量付费。两条路径互不抵扣。
- Codex 只用 OpenAI 自家模型，不支持切换到其他厂商模型；模型与默认优先级随版本滚动，生产环境宜显式固定模型标识。

## 常见失败模式

- 以为 API Key 路径能用云端功能，结果 GitHub 审查、Slack 集成不可用。
- 忽略 Codex 与 ChatGPT Work 共用额度，并发使用导致额度快速耗尽。
- 把 IDE 扩展当代码补全工具，期待 inline 建议落空。
- 把云端任务当本地任务的等价替代：额度消耗口径不同，且依赖队列与可用性。
- 沙箱策略未集中配置就全员铺开，放开网络与 MCP 带来失控风险。
