---
description: "Engram as a dsh MCP memory server: self-managed storage and project selection"
描述: "Engram 作为 dsh 记忆服务：自管存储与项目选择"
name: "Engram Memory Server"
名称: "Engram 记忆服务"
---

# Engram

> 来源：DeepSeek Harness 官方指南 Connect a third-party memory MCP server。第三方配置仅为互操作示例，非背书；pin、路径与环境变量以官方文档为准。

Engram 是 dsh 三份默认关闭的 MCP memory 参考配置之一，通过 `@deepseek-ai/dsh-mcp-client` 以 stdio 方式接入。它的特点是**自己管存储和项目选择**。

## 已文档化的接线信息

| 项 | 值 |
|---|---|
| 测试 pin | `v1.20.0`（commit `ba9e46ced152c37a7cb9e576153c41995873e2fc`） |
| 传输 | stdio |
| 前置 | Go 1.25.10+，或对应 release 二进制 |
| 安装 | `go install github.com/Gentleman-Programming/engram/cmd/engram@v1.20.0` |
| 启用 | `dsh web --patch "$PWD/apps/cli/config/examples/mcp-memory/engram.cordis.yml"` |
| 默认存储 | `~/.engram` |
| 存储覆盖 | `ENGRAM_DATA_DIR` |
| 项目覆盖 | `ENGRAM_PROJECT` |

## 已文档化的行为

- Engram 自己负责存储与项目选择。
- 默认从 DSH 工作目录识别 Git 项目。
- `ENGRAM_DATA_DIR` 与 `ENGRAM_PROJECT` 作为环境变量覆盖传入（官方指南未展开两者如何具体改变行为）。

## 官方文档未展开的部分

这份指南**没有说明** Engram 存什么、召回/检索怎么工作、是否需要 LLM 或嵌入服务，也没有列出 Engram 特有的限制。这些都要查 Engram 自己的文档；不要因为 pin 写在这里就假设它的检索语义已被 dsh 验证或背书。

## 验证要点

用一个唯一且非敏感的值：会话 A 写入并确认写工具成功；同 Host 新建会话 B（不复制 A 的对话）召回该值并使用。需要新会话，不需要重启 Host。

由于项目选择由 Engram 自己决定，验证时要保持工作目录与 `ENGRAM_PROJECT` 不变——换了作用域却召回不到，不等于记忆丢失。

## 一句话主线

**Engram 把存储和项目隔离都收在自己手里，两个环境变量可直接覆盖；但官方指南只教接线，检索语义与依赖要查它自己的文档。**

> 相关：三份配置的横向边界见 `../`；另外两种选择见 `../memorix/`、`../reference-memory/`。
