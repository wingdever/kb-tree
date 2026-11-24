---
description: "QoderCN: Alibaba's terminal coding agent with six working modes and headless execution"
描述: "QoderCN：阿里的终端编码 Agent，六种工作方式与无头执行"
name: "QoderCN"
名称: "QoderCN"
---

# QoderCN

QoderCN 是阿里旗下 Qoder 的国内 CLI 形态（国际版称 Qoder），面向终端开发者。本页是生态样本视角。

## 形态与厂商

- 厂商：阿里；国际文档 `docs.qoder.com`，国内命令 `qoderclicn`，本机已安装。
- 核心是「Agent + 工具 + 权限 + 上下文」四要素：规划步骤、调工具、有副作用操作前按权限确认。

## 六种工作方式

| 方式 | 用途 |
|---|---|
| 交互模式 | 默认，边聊边做 |
| Plan | 先规划确认再动手 |
| Goal | 设完成条件，持续工作直到达成 |
| 定时任务 | 指定时间运行一次或按日历重复 |
| `/loop` | 固定间隔重复同一任务 |
| Headless | 脚本 / CI 中运行，输出结构化结果 |

这套方式把「一次性对话」扩展成**长-running 与调度**，是它与多数 CLI Agent 的显著差异。

## 能力要点

- 内置工具：文件读写编辑、目录浏览、Shell、Grep / Glob、Web 搜索与抓取。
- 扩展：MCP 接外部服务；Skills、Plugins、Subagents、Hooks、自定义命令。
- 记忆与知识库：记住项目约定与团队知识。
- 权限：配置文件分层（用户 / 项目），`--allowed-tools` / `--disallowed-tools`、`--max-turns`、`--yolo`。
- 支持 worktree、会话续接（`-c` / `-r`）、TUI 中的 `!` Bash 与 `#` 记忆模式。
## 官方入口

`https://docs.qoder.com/zh/cli/overview`；国内 CLI 帮助见阿里云帮助中心搜索 “Using the CLI / Qoder CN CLI”。

## 一句话主线

**QoderCN 的差异点是六种工作方式与调度能力，把 CLI Agent 从「一问一答」拉到「定时任务 + 目标驱动」的长运行场景。**

## 参考资料

- Qoder 官方文档：https://qoder.com
