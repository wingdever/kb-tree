---
description: "Code hosting ecosystem: forges, pull requests, CI and how agents act on repositories"
描述: "代码托管生态：代码托管平台、PR、CI 与 Agent 如何操作仓库"
name: "Code Hosting Ecosystem"
名称: "代码托管生态"
---

# 代码托管生态

代码托管生态回答「代码资产放在哪、协作流程怎么走、Agent 如何安全地操作仓库」。它不只是 Git 仓库——PR / Issue / CI / 规则集构成一层治理面，Agent 的权限必须落在这层治理里。

## 平台谱系

| 平台 | 形态 | 强项 | 边界 |
|---|---|---|---|
| **GitHub** | 公有云 + Enterprise / 私有化 | 开源生态最大、PR 体验成熟、Copilot 与 AI 能力领先 | 高级安全特性需额外付费；私有化运维复杂 |
| **GitLab** | SaaS / 自托管 | DevOps 全链路一体化，CI/CD 内建，权限与安全扫描成熟 | 自托管资源占用高；企业版许可成本不低 |
| **Gitee** | SaaS / 私有化 | 国内本地化、中文支持、合规与信创适配 | 国际插件生态相对薄弱 |
| **Bitbucket** | 云 / Data Center | 与 Jira、Confluence 深度集成 | 独立 CI 能力较弱 |
| **Gitea / Forgejo** | 轻量自托管 | 单二进制、部署简单、社区驱动 | 企业级权限、审计、安全能力有限 |
| **Gerrit** | 自托管 | patch-set 评审、强制审批门禁 | 操作模型复杂，只支持 Git |

选型不是比较功能表，而是比较**合规负载、已有技术栈、代码是否必须在自有基础设施上**：合规审计优先 GitLab 自托管；已用 Atlassian 优先 Bitbucket；成本敏感且要全控优先 Gitea / Forgejo。

## Agent 接入：两层 MCP

代码托管生态里 Agent 的操作面分两层，缺一层就不完整：

| 层 | 对象 | 代表 | 能力 |
|---|---|---|---|
| **本地 Git MCP** | 磁盘上的工作树 | `mcp-server-git` | log / diff / blame / 分支 / 状态，不需要 token |
| **Forge MCP** | 托管平台的 API | GitHub / GitLab / Gitea MCP | 仓库、Issue、PR、CI、 Governance、安全告警 |

关键现实：

- **没有跨平台 MCP**。GitHub 的 MCP 管不了 GitLab 的 PR；同时用多家平台就并装多个 server，让 Agent 按仓库选工具。
- **官方与社区差距大**。GitHub 官方 MCP 最成熟（OAuth、远程托管、完整 API 覆盖）；GitLab 官方 MCP 从 19.5 起 GA，内置在实例 `/api/v4/mcp`；Gitea/Forgejo、Bitbucket 主要靠社区 server。
- **GitHub MCP 的工具集**：默认启用 `context`/`repos`/`issues`/`pull_requests`/`users`；可按需开启 `actions`/`code_quality`/`code_security`/`governance`/`projects` 等。支持 `--read-only`——写工具即使显式请求也会被跳过。
- **鉴权**：远程 OAuth 或 PAT；PAT 优先于 OAuth。PAT 要用最小权限、分项目分环境、定期轮换，不提交进 git。

## Agent 能做什么

- **仓库**：浏览代码、读文件与目录树、分析提交、创建/更新内容、发 release、fork、删除（需确认流程）。
- **Issue**：搜索/读取/创建/更新，打标签、设里程碑、子 issue 层级、指派 Copilot 处理。
- **PR**：创建与更新、请求评审、批量留行级评论、处理 review feedback、检查通过后再合并。
- **CI**：列出/触发 workflow，读 job 与 artifact 日志，失败诊断。
- **治理与安全**：ruleset、required checks、code scanning、Dependabot、secret scanning 告警读取与更新。

## 治理：Agent 写代码的真正瓶颈

多位实践者的共同结论：**Agent 工作流的主要收益来自评审与分支层，不是来自 Agent 离仓库有多近**。分支规则、必需检查、合并队列才是阻止两个 Agent 互相覆盖的机制——这是策略问题，不是接口问题。

- 把 PR 模板、required reviewers、CI 检查写成 ruleset，而不是靠提示词约束 Agent。
- 给 Agent 独立 token 与最小权限，写操作与读操作分凭证。
- 只读模式用于探索与评审，写模式只在本任务需要的工具集上开启。
- 审计日志保留：谁能合并、谁触发了流水线、Agent 改了哪些规则。

## 迁移成本提示

Git 历史迁移以分钟计（镜像克隆 + 推送分支标签），但围绕它的东西要周计：CI 流水线要重写重测、secrets / deploy keys / webhooks / 机器人 / SSO 组映射 / 规则集都要重建。**先双跑一个完整发布周期再切换**——两边都推、两边都跑构建，新流水线绿了一个周期后再改部署目标。

## 与树中其它节点的关系

CI/CD 的部署侧归云原生与 DevOps 子生态（尚未展开）。

## 一句话主线

**代码托管生态是「Git 工作树 + Forge 治理面 + 两层 MCP」的组合；Agent 能操作仓库，但真正保证安全的是分支规则、必需检查与最小权限，而不是接口有多顺。**

## 参考资料

- GitHub MCP Server 仓库：https://github.com/github/github-mcp-server
