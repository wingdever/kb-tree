---
description: "Agentic AI Foundation: neutral Linux Foundation home for agent protocols and open building blocks"
描述: "Agentic AI Foundation：Agent 协议与开放构件的 Linux Foundation 中立治理机构"
name: "Agentic AI Foundation"
名称: "Agentic AI 基金会"
---

# Agentic AI Foundation（AAIF）

> 来源：AAIF 官网、Linux Foundation 公告与各项目官方博客。项目清单与成员数增长快，以官方页面为准。

AAIF 是 Linux Foundation 下的**定向基金**，给 Agent 开放协议与构件提供中立治理。它的存在本身就是结论：**协议之争没有赢家，最后落在非营利机构**——Google 的 A2A、Anthropic 的 MCP、IBM 已并入 A2A 的 ACP，都不再由单一厂商控制。

## 官方入口

- AAIF 官网：`https://aaif.io/`（工作组列表、博客）
- Linux Foundation 成立公告：搜索 `linuxfoundation.org` 的 “announces the formation of the Agentic AI Foundation”
- A2A 加入 AAIF：AAIF 博客 `aaif.io/blog/a2a-joins-aaif`
- MCP 加入 AAIF：`blog.modelcontextprotocol.io` 的 2025-12-09 公告

## 为什么会出现

2024-11 Anthropic 发布 MCP，2025-04 Google 发布 A2A，IBM 推 ACP，浏览器厂商各有实验——每个实验室都想拥有 Agent 连接层。整合并非技术胜负，而是治理选择：AAIF 官网的表述是「互联网靠开放协议运行，Agentic AI 也将如此」。

2025-12-09 Linux Foundation 宣布成立 AAIF，**三个创始项目**：Anthropic 的 **MCP**、Block 的 **goose**（本地优先 Agent 框架）、OpenAI 的 **AGENTS.md** 约定。白金成员为 AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAI——在模型与云上直接竞争的八家公司共同资助同一套底层协议。

## 托管项目栈

按层次看，AAIF 已覆盖一个完整栈（项目数从最初 3 个增长到 2026 年的约 10 个）：

| 层 | 项目 | 作用 |
|---|---|---|
| 指令 | **AGENTS.md** | 项目级 Agent 约定，跨仓库与工具链 |
| 运行时 | **goose** | 本地优先的开源 Agent 框架 |
| 工具 | **MCP** | Agent ↔ 工具 / 数据；2025-12 同日捐赠，官方称当时已有 10,000+ server、9700 万次月 SDK 下载 |
| Agent 间 | **A2A** | 2025-06 进 Linux Foundation，**2026-08 加入 AAIF**；v1.0 稳定版在 2026-03 |
| 流量 | **agentgateway** / **Agent Router** | Agent 流量路由、策略与可观测 |
| 技能 / 环境 | **Agent Skills**、**Open Responses**、**OpenEnv**、**OpenSandbox** | 2026-10 新增的四个项目 |

浏览器层留在 AAIF 之外：WebMCP 在 W3C 做社区草案，由 Google / Microsoft 工程师编辑，Chrome 149 开了 origin trial。**不同场所，同一原则：不让单一厂商掌钥匙**。

## 治理方式

- **治理委员会**管战略与财务，**每个项目保留技术自治**：MCP 有自己的维护者与 SEP 流程。
- **技术指导委员会（TSC）**由多家公司代表组成；A2A 的 TSC 为八家公司。
- 会员规模：成立时不足 40 家，2026-08 报道约 250 家（不同来源对层级计数口径不同，只作量级参考）。
- 中立治理的实际价值：采购与架构评审问「厂商弃用怎么办」时，「Linux Foundation 项目 + 多公司 TSC」比「某厂商规范」是更可靠的答案。

## 对工程决策的意义

- **协议战争基本结束**：MCP 与 A2A 是互补层，且同处一个治理屋檐。等着看谁赢的架构决策可以落地了——MCP 给 Agent 工具，A2A 让 Agent 跨组织协作。
- **标准化 ≠ 互操作**：规范统一了线路格式，没有统一语义；两个 MCP server 可能暴露不同工具名，实现质量与部署纪律仍归各团队。
- **治理集中也有代价**：一个基金会的决策影响面更大；MCP 在快速普及期积累过 40+ CVE 与工具投毒攻击类，A2A 的跨组织信任是更难的问题。授权与 Agent 身份是值得持续盯的两处。
- **选型建议**：优先基于开放标准构建，不绑定单一厂商的专有集成格式。切换成本从「重写」降为「迁移」。

## 与树中其它节点的关系


## 一句话主线

**AAIF 把 Agent 的关键协议与构件放进 Linux Foundation 的中立治理下——竞争留在模型与产品层，连接层成为公共基础设施；它的成立标志着协议战争以「无人独占」收场。**

