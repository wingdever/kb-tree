---
description: "Agent action surfaces: the -use family, the shared tool-call chain and how to choose an action surface"
描述: "Agent 行动面：-use 家族、共享的工具调用链与行动面选择"
name: "Agent Action Surfaces"
名称: "Agent 行动面谱系"
---

# Agent 行动面谱系

`-use` 已经成为一组命名家族：tool use、computer use、browser use、code use……它们**不是不同技术，而是同一个动作链的不同外壳**。本节点写这组家族的全貌、共同骨架与选择顺序。

## 官方入口

- CodeBuddy Code CLI 文档：`https://www.codebuddy.cn/docs/cli/`（无头模式、A2A 协作、最佳实践）
- Qoder CN CLI 概览：`https://docs.qoder.com/zh/cli/overview`；阿里云帮助中心 `help.aliyun.com` 的 “Using the CLI”
- ACP 注册表：`https://zed.dev/acp`

## `-use` 家族

| 名称 | 行动面 |
|---|---|
| **tool use** | 母概念：模型填工具名 + 参数，宿主执行 |
| **code / shell use** | 终端与文件：读写文件、跑命令、改仓库 |
| **browser use** | 网页：DOM / a11y 或截图，限定在浏览器 |
| **computer use** | 整个桌面：截图 + 坐标 + 按键 |
| **phone use** | 两种含义：Agent 驱动手机 GUI；或手机作为窗口远程监督别处运行的会话 |
| **web use** | 搜索 / 抓取作为工具，不改界面 |
| **api / connector use** | 结构化调用云应用、MCP server |
| **agent use** | 把另一个 Agent 客户端当工具：A2A / ACP / headless CLI |

## 去魅：同一条动作链

产品名叫 Browser Agent、Coding Agent、Operator、Computer Use，差别只在**宿主暴露了哪张工具表**。共同链条四步：

1. **声明**：宿主给出 `tools[]` / `inputSchema` 或 computer-use 工具。
2. **提议**：模型填工具名与参数对象，产出 `tool_call` / `computer_call` —— 它**不执行**。
3. **门禁**：宿主校验 schema、套 allowlist、决定是否等人工审批。
4. **写回**：截图、stdout 或 API 响应变成下一轮可见的对象。

**Agent 不拥有浏览器、shell 或手机**——真正点击、敲命令、调 API 的都是宿主。所以迁移成本多在宿主侧（工具表与权限），不在模型侧；选型也应该按工具表看，不按产品名看。

## 三种机制收敛

| 机制 | 怎么行动 |
|---|---|
| **UI 控制** | 截图 + 点击 / 按键，覆盖无 API 的遗留系统 |
| **API / connector 调用** | 结构化工具与 MCP，生产集成默认选择 |
| **终端与文件系统** | 读写文件、跑命令，coding agent 的主场 |

Browser use 是「UI 控制」里被 DOM / a11y 约束得更紧的特例，不是第四种机制；web use 与 api use 落在第二类。

## phone use 的两个含义

- **Agent 驱动手机界面**：视觉模型看手机 GUI 并操作（下单、设置、导航），对应受约束程度更低的视觉路线，坐标/界面识别是主要失败点。
- **手机作为监督窗口**：Agent 会话跑在常开的机器或云环境，手机只承担会话持久化、审批通知、看 diff —— 价值是「中断驱动」而非在小屏上写代码。后者属于渠道与人在回路的话题。

## 选择顺序

**有 API 走 API → 稳定高流量流程用脚本 / RPA → 没有接口且界面多变才上 GUI**。

- 工具表里有对应工具，才谈得上能力；没有浏览器工具就不能上网，没有 Bash 就不能交付可运行补丁。
- 按可恢复性决定门禁：不可逆动作（支付、提交、删除）必须人工审批。
- 把 `-use` 当产品标签会误导——判断依据永远是宿主暴露的工具、权限与回滚能力。
- **agent use 的边界不同**：这里选的不是一张工具表，而是另一个 Agent 的提示词 + 工具集 + 权限面，等于外包一部分控制权。外部 CLI 子进程通常一次性返回、无中途进度、无法 steer。调用形态有 A2A、ACP、headless CLI 三种，CodeBuddy 与 QoderCN 均提供后两种。

## 常见误区

- 以为模型「自己在浏览 / 自己在执行」——它只产出调用对象。
- 忽略工具的权限面，把 UI 控制当无风险操作。
- 有 API 却用 computer use，承担不必要的延迟与成本。
- 把 phone use 的两种含义混为一谈，按「手机能跑 Agent」设计架构。

## 一句话主线

**`-use` 家族是按行动面命名的一组外壳：模型提议、宿主执行是共同骨架；按工具表选型，按可恢复性设门禁，有 API 就别走 GUI。**

