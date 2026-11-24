---
description: "DeepSeek Harness MCP memory overlay: three default-off reference servers Memorix, MCP Reference Memory and Engram"
描述: "DeepSeek Harness 的 MCP 记忆挂载：三份默认关闭的参考配置 Memorix、MCP Reference Memory 与 Engram"
name: "MCP Memory Overlay"
名称: "MCP 记忆挂载"
---

# MCP Memory Overlay（dsh）

> 来源：DeepSeek Harness 官方指南 Connect a third-party memory MCP server。第三方配置仅为互操作示例，非背书；pin、路径与环境变量以官方文档为准。

DeepSeek Harness（dsh）内置的会话日志与自动压缩都不跨会话。跨会话记忆可以通过 `@deepseek-ai/dsh-mcp-client` 挂载外部 MCP memory server——官方给了三份**默认关闭**的参考配置。

## 分工边界

dsh 只做四件事：解析 Cordis overlay、启动 stdio 子进程或连接 Streamable HTTP、发现 MCP 工具、把它们暴露为 `mcp__<serverName>__<tool>`。工具发现是异步的，要等 `mcp__...` 出现后再做验证。

dsh **不**下载 server、不初始化数据库、不选模型与 embedding provider、不开云账号、不迁移厂商数据、不监管独立的 HTTP 服务。安装、身份、鉴权、模型、嵌入、持久化与许可都由 provider 负责。

三份配置是互操作示例，官方明确声明「不表示背书、推荐、合作或持续支持」。

## 三份参考配置

| 系统 | 测试 pin | 传输 | 前置 | 默认存储 |
|---|---|---|---|---|
| Memorix | `memorix@1.3.0`（`500792cad3144142293bfbb20acb4841c9f7fcfa`） | stdio | Node 22.18+ | `~/.memorix/data` |
| MCP Reference Memory | `@modelcontextprotocol/server-memory@2026.7.4`（`6dd0a683e198783e30feabf7abaf42f925bd18b1`） | stdio | npm 全局安装 | `$HOME/.dsh-mcp-reference-memory.jsonl` |
| Engram | `v1.20.0`（`ba9e46ced152c37a7cb9e576153c41995873e2fc`） | stdio | Go 1.25.10+ 或对应二进制 | `~/.engram` |

## 选型与学习顺序

按**学习成本**从易到难：MCP Reference Memory → Memorix → Engram。这排的是「学会它要面对多少未知量」，不是能力强弱——最简单的那个语义也最弱。

| 维度 | Reference Memory | Memorix | Engram |
|---|---|---|---|
| 数据模型是否写明 | 写明：知识图谱 + entity/relation/observation | 未文档化 | 未文档化 |
| 检索行为是否写明 | 写明：大小写不敏感子串匹配 | 未文档化 | 未文档化 |
| 能否直接检查存储 | 能，单一 JSONL，路径固定 | 有默认目录，格式未知 | 有默认目录，格式未知 |
| 安装摩擦 | npm（dsh 本身是 Node） | npm | Go 工具链，或对应二进制 |
| 需额外读第三方文档 | 基本不需要 | 需要（检索语义、provider） | 需要（存什么、怎么召回、是否要 LLM/嵌入） |
| 行为可预测性 | 高，实验能解释结果 | 中低 | 低 |

- **先学 Reference Memory**：官方把存什么、怎么召回、缺什么都写清了，存储是能直接打开的单一 JSONL。用它把「MCP 挂载与跨会话召回」这条链路和「记忆聪不聪明」分开理解。代价是语义相近但措辞不同的记忆召不回来。
- **再学 Memorix**：安装同样简单，本地启发式模式不需要 LLM 或嵌入服务；但数据模型与检索语义未文档化，必须读它自己的文档或拆 `~/.memorix/data`，未知量变多。
- **最后学 Engram**：多了 Go 前置（可用二进制绕过），且它自管存储与项目选择，两个环境变量覆盖只被当作覆盖提了一句。存什么、怎么召回、是否要 LLM/嵌入都没写——召回失败时无法判断是作用域、检索语义还是配置导致的。

学的时候固定同一套验证动作——唯一测试值、会话 A 写入、同 Host 新会话 B 召回、用召回值做事，全程不改作用域——只换 provider。这样每一步的差异都落在记忆语义上，而不是接线是否通；从 Engram 上手会把接线问题与 provider 内部行为混在一起排查。

## 启用、持久化与关闭

- 单次启用：`dsh web --patch <overlay 路径>`，路径可以是复制到任意位置的副本；三选一，不叠加。
- 跨运行保留：把所选文件那条 `insert` patch 合并进 `$DSH_HOME/profiles/<name>/cordis.patch.yml`（单 profile）或 `$DSH_HOME/cordis.patch.yml`（全机）。**不要覆盖已有文件**——里面可能有其它 patch。
- 关闭：启动时不带 `--patch` 即为全关；若已合并进 patch 层，删掉那条 insert 再 reload/重启。断开连接与删除已存记忆是两件事，官方未给通用删除流程，需查 provider 自己的文档。

## 验证跨会话召回

用一个唯一且非敏感的值，全程保持 provider 的存储作用域不变：

1. 会话 A：让它记住该值，确认调用了写工具且返回成功。
2. 同一 Host 新建会话 B（**不复制** A 的对话），问该值，确认调用了 search/recall 工具并返回结果。
3. 在 B 里用召回值做一件事，确认答案确实用上了它。

需要新会话，但**不需要重启 Host**。若工具描述没稳定触发记忆行为，可在模型指令里加一句「用户要求记住时调用写工具；历史可能相关时先检索记忆」——这是补充，不替代 dsh 的系统人格。

## 运维要点

- stdio 桥在启动子进程前会剔除名字像凭据的环境变量和所有 `DSH_*` 变量；可选上游 secret 写进该行的 `config.env`，不要直接写进 YAML。
- MCP 子进程崩溃时自动重连（backoff）并重新同步工具；重连预算耗尽后工具被注销，直到 reload 或重启。
- 三份 pin 针对当时版本；dsh 仍是开发者预览，升级前先核对 `dsh --version` 与官方 pin。

## 一句话主线

**dsh 只负责把外部 MCP memory server 的工具挂进模型，存储与语义全归 provider；三份配置默认关闭，验证要跨新会话而不是同会话复述。**

