---
description: "Reusing open-source agent clients: ACP editors, AG-UI frontends, MCP chat UIs and their limits"
描述: "复用开源客户端：ACP 编辑器、AG-UI 前端、MCP 聊天站及其边界"
name: "Open-Source Client Options"
名称: "开源客户端接入选型"
---

# 开源客户端接入选型

自研客户端是最贵的一步。好消息是：**只要你的 agent 说对协议，就有一批开源客户端可以直接拿来用**。坏消息是"说对协议"在不同接入位上是三件不同的事——ACP 管编辑器、AG-UI 管自有前端、MCP 管聊天站点，能力和边界完全不同。

## 三条路径对照

| 接入位 | 协议 | 你实现什么 | 可直接用的开源客户端 | 关键代价 |
|---|---|---|---|---|
| IDE / 桌面 | ACP（Agent Client Protocol） | ACP Agent 端（JSON-RPC 会话、权限请求、文件与终端能力） | Zed、Athas、AcpAgent Client、Alchemist Coder、OpenACP | 原生是本地 stdio，云端要加传输桥（含 fs 代理） |
| 自有 Web / App | AG-UI | 事件流端点（typed events + HTTP/SSE） | CopilotKit（React / Angular / Vue / React Native）、Channels（Slack / Teams 等） | 前端仍需接入 SDK，不是零改造 |
| 自托管聊天站 | MCP（+ 各家的 Agent API） | MCP Server（工具、资源、提示） | LibreChat、Open WebUI、LobeChat | 工具级接入，拿不到完整会话控制 |

## ACP：编辑器与桌面客户端

ACP 是 Apache 许可的开放标准，定位是「任意 agent 接入任意编辑环境」。协议层面管四件事：会话生命周期、流式输出、权限请求、文件与终端转发——最后一项带来的好处是**权限边界留在宿主**，agent 不直接拿用户的文件系统。

官方维护了一份客户端生态清单，其中开源实现包括：

- **Zed**：协议发起方，最完整的参考客户端；JetBrains 侧也已接入。
- **Athas**：Tauri + Rust 的轻量代码编辑器，内置 ACP 会话，支持从 ACP Registry 一键安装 agent。
- **AcpAgent Client**（GPL-3.0）：基于官方 Rust SDK 的多 agent 桌面客户端，带文件浏览、内嵌终端与 ACP 流量检查器。
- **Alchemist Coder**（AGPL-3.0）：把 Claude Code / Codex 当 ACP agent 跑，带 agent 树、内联权限与 diff、git worktree 隔离、多 agent 竞技场。
- **OpenACP**：自托管桥，把 ACP agent 接到 Telegram / Discord / Slack，实时流式回传工具调用。

**云端场景的关键坑**：ACP 的经典传输是编辑器**拉起本地子进程**走 JSON-RPC over stdio。你的 agent 跑在云电脑上时，必须自己补一层传输桥（WebSocket/HTTP ↔ stdio），否则编辑器根本够不到它。这类桥已有开源实现可参考，但协议本身仍在演进——2026 年 7 月已出 v2 草案，重点是把更多会话状态表达清楚。桥不只是转发消息，还要代理文件系统，见下一节。

## 文件在哪一侧：agent 不碰盘

被编辑的代码默认在**客户端那一侧（client-side）**，不是 agent 那边。ACP 的文件系统方法只允许 agent 在「Client's environment」里读写文本文件：`fs/read_text_file` / `fs/write_text_file` 都是 agent 发给客户端的请求，由客户端拿自己的磁盘执行。

这条设计带来三个后果：

- **能读到未保存的编辑状态**。agent 通过客户端取内容，所以看到的是编辑器缓冲区，而不是磁盘上可能已经过时的版本。
- **能力要协商**。`initialize` 返回的 `clientCapabilities.fs.readTextFile` / `writeTextFile` 为 false 或缺失时，agent 不允许调用对应方法。跨客户端行为不一致，多半卡在这里。
- **路径语义由客户端定义**。请求里 `path` 是绝对路径，但"这个绝对路径指向哪台机器的哪个盘"完全取决于客户端实现。协议里不存在"agent 直接读云盘"的形态。

所以"文件树在本地还是云上"取决于客户端跑在哪，一共有三种拓扑：

| 拓扑 | 文件树位置 | 相对 agent 而言 | 代价 |
|---|---|---|---|
| 本地编辑器 + 本地 agent | 用户电脑 | 本地 | 经典形态，无桥，能力最完整 |
| 云桌面里的编辑器 + 云侧 agent | 云电脑 | 本地 | 最省事：编辑器与 agent 同机，桥都不用做，本质仍是经典形态 |
| 本地编辑器 + 云端 agent | 用户电脑 | 远端 | 桥必须同时实现**文件系统代理**与终端代理 |

第三种是多数"云 agent 接入 IDE"的真实形态，也是最容易做坏的一种。桥要处理的事不止转 JSON-RPC：

- **路径映射**：客户端传来的绝对路径是本地语义，云侧 agent 看到的路径空间不同，需要一个显式映射或虚拟挂载，不能直接拼字符串。
- **一致性**：两端可能同时改同一文件（用户手改 + agent 写），要有版本号或 mtime 校验与冲突回退，否则静默覆盖。
- **断线恢复**：文件读请求是同步等待的，桥断了 agent 就卡死；要有超时、重试与可重放的请求编号。
- **非文本内容**：协议只规定了文本读写，图片、二进制、大文件要么走客户端能力扩展，要么退回终端命令处理。
- **审批仍在客户端**：写文件与跑命令的权限询问由客户端弹窗，云侧 agent 不能自己"授权自己"；审计日志要两端都有，否则出问题查不清是谁改的。

第三种还有一个变体：把工作区也搬到云上，编辑器远程打开云侧目录。此时编辑与执行都在云上，退化成第二种拓扑，代价转移到"编辑器要支持远程文件系统"。

写设计文档时建议用 **client-side / agent-side** 而不是"本地/云"来表述：第二种拓扑里两边都在云上，文件却仍在 client-side，"本地/云"这种说法会直接把人说晕。

### 常见误解

- "云 agent 可以直接读我的云盘"——ACP 里 agent 没有直接文件权限，所有读写都经客户端。
- "接了传输桥就能跑"——只转消息不代理 fs，agent 一读文件就超时。
- "文件在云上，客户端不用管"——客户端仍需承担读写、审批与冲突检测，它才是文件侧的责任方。

## AG-UI：自有前端

三条路径里，AG-UI 对云端 agent 最友好：它本身就是 HTTP 上的双向事件流，不需要传输桥，也不需要把编辑器搬到云上——你要做的只是一个接受 `RunAgentInput`、回事件流的端点。

代价在前端侧：客户端不是一个装好就能连的二进制，而是要接 CopilotKit 这套 SDK（React / Angular / Vue / React Native）。也就是说"复用客户端"在这里复用的是一个前端框架，界面仍是你自己的。

## MCP：自托管聊天 UI

如果目标是"给用户一个现成聊天站"，LibreChat、Open WebUI、LobeChat 都能自托管并支持 MCP：你的能力以 MCP Server 暴露，它们当工具调用。

- **LibreChat**：MCP 配置最成熟（原生 `librechat.yaml`），另有 Agents、Subagents、Skills、Code Interpreter 隔离执行，以及企业级 SSO（OAuth/SAML/LDAP）。
- **Open WebUI**：部署最简单（单容器），MCP 走 Pipelines，灵活但要多配一层。
- **LobeChat**：模型覆盖面最广，MCP 支持较晚（2025 年底）但可用。

**边界要说清**：这是工具级接入。它们不会替你接管终端、文件树、审批流；会话状态也留在它们那边。想要完整会话控制，就要走各家自己的 Agent API（例如远程 agent 背后挂 Responses、Agent Channels 之类的能力），而这条路每家都不一样，等于重新做适配。

## 怎么选

- 用户要在 IDE 里结对改代码 → 做 ACP，接受传输桥的成本。
- 用户要在你自己的产品界面里用 → 做 AG-UI，前端可控性最高。
- 用户只想要一个能聊、能用工具的站点，且不介意界面长什么样 → 做 MCP Server，接 LibreChat 这类现成 UI。

三者不互斥：很多产品的做法是 MCP 暴露工具、AG-UI 给自有前端、ACP 留给 IDE 用户，共用同一套 agent 核心。

## 常见失败模式

- 只实现了协议的一半（如 ACP 没有权限请求），客户端一用就卡在审批环节。
- 云端 agent 直接照搬 stdio 传输，编辑器连不上，误以为是协议不兼容。
- 以为接上 AG-UI 就自动有前端，实际还要写 SDK 集成与样式。
- 把 MCP 当成"完整客户端接入"，结果发现改不了会话、拿不到终端。
- 客户端版本升级后事件字段变化，没做 schema 校验与降级。
- 一次接三种客户端却不统一 agent 核心，行为在不同端漂移。

## 什么时候不必复用

需要独特的交互形态（定制可视化、多 agent 协同面板、复杂审批流）时，现成客户端的抽象会成为天花板；此时自研前端 + 复用协议（而不是复用客户端）更划算。协议是公共的，界面不是。

## 参考资料

- ACP 文件系统方法（fs/read_text_file、fs/write_text_file 与能力协商）：https://agentclientprotocol.com/protocol/file-system
- ACP 客户端生态清单：https://agentclientprotocol.com/get-started/clients
- Zed：Agent Client Protocol（Apache 许可）：https://zed.dev/acp
- AG-UI 1.0 规范发布说明：https://www.copilotkit.ai/blog/ag-ui-1.0
- AG-UI 协议仓库（MIT）：https://github.com/ag-ui-protocol/ag-ui
- CopilotKit 前端栈（MIT）：https://github.com/CopilotKit/CopilotKit
- LibreChat（MCP、Agents、Code Interpreter）：https://www.librechat.ai/
- 自托管聊天 UI 对比（LibreChat / Open WebUI / LobeChat 的 MCP 支持）：https://www.cloudhostreview.com/article/librechat-vs-openwebui-vs-lobechat-self-hosted-ai-chat-vps-2026
