---
description: "Memorix as a dsh MCP memory server: local heuristic mode, project identity and storage overrides"
描述: "Memorix 作为 dsh 的 MCP 记忆服务：本地启发式模式、项目身份与存储覆盖"
name: "Memorix Memory Server"
名称: "Memorix 记忆服务"
---

# Memorix

Memorix 是 dsh 三份默认关闭的 MCP memory 参考配置之一，通过 `@deepseek-ai/dsh-mcp-client` 以 stdio 方式接入。

## 已文档化的接线信息

| 项 | 值 |
|---|---|
| 测试 pin | `memorix@1.3.0`（commit `500792cad3144142293bfbb20acb4841c9f7fcfa`） |
| 传输 | stdio |
| 前置 | Node 22.18+ |
| 安装 | `npm install --global memorix@1.3.0` |
| 启用 | `dsh web --patch "$PWD/apps/cli/config/examples/mcp-memory/memorix.cordis.yml"` |
| 默认存储 | `~/.memorix/data` |
| 存储覆盖 | 启动 DSH 前设 `MEMORIX_DATA_DIR` |
| 可选 provider 配置 | `~/.memorix/config.toml` 或项目 `memorix.toml` |

## 已文档化的行为

- 可在**本地启发式模式**运行，不需要 LLM 或 embedding 服务。
- 示例沿用 DSH 工作目录的 Git 项目身份。

## 官方文档未展开的部分

这份指南**没有说明** Memorix 存什么、召回/检索怎么工作，也没有说明支持哪些可选 provider、何时需要它们。要用这些能力，需要读 Memorix 自己的文档；不要把「本地启发式」当成已理解的检索语义。

## 验证要点

用干净会话检验持久化：旧会话里的上下文不算数，必须在同 Host 的新会话中召回。

## 一句话主线

**Memorix 的优势是本地启发式、零 LLM/嵌入依赖且项目身份自动取工作目录；但官方指南只给了接线，检索语义要查它自己的文档。**

## 参考资料

- DeepSeek Harness 指南：接入第三方记忆 MCP server，未附固定链接
