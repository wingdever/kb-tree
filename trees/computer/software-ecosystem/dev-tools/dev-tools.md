---
description: "Developer tools ecosystem: IDEs, extension markets, LSP, coding agents and standardized extension bundles"
描述: "开发工具生态：IDE、扩展市场、LSP、编码 Agent 与标准化扩展包"
name: "Developer Tools Ecosystem"
名称: "开发工具生态"
---

# 开发工具生态

开发工具生态是 Agent 落地最密集的环境：编辑器、终端、扩展市场、语言服务器、编码 Agent 与配置约定叠在一起，决定 Agent 能读什么代码、能调用什么工具、能改多深的项目。

## 分层结构

| 层 | 代表 | 作用 |
|---|---|---|
| 编辑器 / IDE | VS Code、JetBrains 系列、Cursor、Zed、Neovim | 写代码的主界面；扩展生态与 AI 能力的宿主 |
| 扩展机制 | VS Code 扩展市场、Language Server Protocol（LSP） | 把语言能力、调试、格式化做成可复用插件 |
| 编码 Agent | Claude Code、OpenAI Codex、Cline、OpenCode、Kiro、Gemini CLI | 在终端或编辑器里执行多步任务：读代码、改文件、跑命令 |
| 扩展包 | Skills（`SKILL.md`）、Custom Agents、Hooks、MCP 配置、Slash Commands | 把能力做成可安装、可分发的单元 |
| 配置约定 | `AGENTS.md`、`CLAUDE.md`、项目级规则文件 | 把构建命令、测试流程、编码约定写成 Agent 可读的常驻上下文 |

## 标准化扩展包

2026 年的趋势是把散落的配置封装成**可安装的插件单元**：

| 组件 | 形态 | 作用 |
|---|---|---|
| Custom Agents | `.agent.md` 一类文件 | 定义专门角色、工具配置与系统提示 |
| Skills | `SKILL.md` + 脚本 | 按需加载的离散能力 |
| Hooks | 事件处理器 | 在 SessionStart / PreToolUse 等生命周期点拦截、校验、注入 |
| MCP Server 配置 | `.mcp.json` 一类文件 | 声明外部数据源与工具连接 |
| Slash Commands | `/code-review` 一类命令 | 触发多步工作流的显式入口 |

这些组件让「同一个能力在不同 IDE / CLI 间复用」成为可能，降低框架锁定；代价是配置面变大，需要版本化与审核。

## 选型维度

- **宿主形态**：IDE 插件（Cline、Copilot）、终端 Agent（Claude Code、OpenCode、Codex）、云任务（云端 Codex / Devin）、桌面 IDE（Cursor、Antigravity）。
- **模型策略**：厂商绑定（Claude Code 用 Claude、Codex 用 GPT）vs provider-agnostic（OpenCode、Cline 支持本地模型与任意 OpenAI 兼容 API）。
- **扩展深度**：只装 Skills/MCP 的执行环境 vs 能自定义 Agent、Hooks 与命令的完整插件体系。
- **配置可移植**：`AGENTS.md` 被多家 Agent 尊重，适合做跨工具的项目级约定；`CLAUDE.md` 只对 Claude Code 生效，层级更细。

## 与树中其它节点的关系

- Skills 的机制见 `../../ai/agent/skill/`；Hooks 见 `../../ai/agent/hooks/`。
- MCP 协议与工具接入见 `../../ai/agent/mcp/`、`../../ai/api/mcp-tools/`。
- 编码 Agent 的选型与实践见 `../../ai/agent/coding/`；提示与上下文约定见 `../../ai/agent/prompt/`。

## 一句话主线

**开发工具生态的核心是「可插拔」：IDE / 终端是宿主，LSP 与扩展市场是连接面，Skills / Hooks / MCP / AGENTS.md 是 Agent 能力的分发格式。**

> 相关：软件生态总览见 `../`；IM 子生态见 `../im/`；协作办公生态见 `../collaboration/`。
