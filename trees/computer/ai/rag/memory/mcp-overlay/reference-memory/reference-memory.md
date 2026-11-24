---
description: "MCP Reference Memory as a dsh memory server: local knowledge graph, substring search and explicit limits"
描述: "MCP Reference Memory 作为 dsh 记忆服务：本地知识图谱、子串检索与明确限制"
name: "MCP Reference Memory Server"
名称: "MCP 参考记忆服务"
---

# MCP Reference Memory

MCP Reference Memory 是 dsh 三份默认关闭的 MCP memory 参考配置之一，通过 `@deepseek-ai/dsh-mcp-client` 以 stdio 方式接入。它是三者中**唯一被官方指南说清数据模型与检索行为**的配置。

## 已文档化的接线信息

| 项 | 值 |
|---|---|
| 测试 pin | `@modelcontextprotocol/server-memory@2026.7.4`（commit `6dd0a683e198783e30feabf7abaf42f925bd18b1`） |
| 传输 | stdio |
| 安装 | `npm install --global @modelcontextprotocol/server-memory@2026.7.4` |
| 启用 | `dsh web --patch "$PWD/apps/cli/config/examples/mcp-memory/mcp-reference-memory.cordis.yml"` |
| 默认存储 | `$HOME/.dsh-mcp-reference-memory.jsonl`（不落在 npm 包目录） |
| 存储覆盖 | 启动 DSH 前设 `MEMORY_FILE_PATH` |

## 存什么、怎么读

- 存**本地知识图谱**：entity、relation、observation，落盘为 JSONL。
- 暴露工具：entity、relation、observation、read、search、open。
- 不需要模型或嵌入服务。

## 检索语义（重要）

搜索是**大小写不敏感的子串匹配**，匹配对象是 entity 名字、类型与 observation——**不是语义检索**。

服务器**不提供**：embeddings、自动摘要、冲突解决、遗忘策略。所以「相关但措辞不同」的记忆不会被召回；重复或矛盾的事实也不会自动合并或淘汰，治理责任完全在你这边。

## 未文档化的部分

官方指南没有说明它如何确定项目身份，也没有展开每个工具的具体调用细节。

## 验证要点

用一个唯一且非敏感的值：会话 A 写入并确认写工具成功；同 Host 新建会话 B（不复制 A 的对话）召回该值并使用。需要新会话，不需要重启 Host。

如果要验证「子串而非语义」这条限制，用同义不同词的问法做反例——按官方描述应当召回失败。

## 一句话主线

**它是可预测性最高的基线：本地知识图谱、子串匹配、零嵌入，但语义、冲突与遗忘都不管——先用它验证跨会话链路，再决定要不要更强的语义。**

## 参考资料

- DeepSeek Harness 指南：接入第三方记忆 MCP server，未附固定链接
