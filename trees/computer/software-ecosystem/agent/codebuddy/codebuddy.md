---
description: "CodeBuddy: Tencent Cloud agentic coding tool across CLI, IDE and cloud"
描述: "CodeBuddy：腾讯云的 CLI / IDE / 云三形态编码 Agent"
name: "CodeBuddy"
名称: "CodeBuddy"
---

# CodeBuddy

CodeBuddy 是腾讯云的编码 Agent，覆盖 **CLI / IDE / 云** 三种形态。本页是生态样本视角。

## 形态与厂商

- 厂商：腾讯云；国内站点 `copilot.tencent.com/cli`，海外 `codebuddy.ai/cli`。
- 安装：`npm install -g @tencent-ai/codebuddy-code`，命令 `codebuddy` / `cbc`；Node.js 18+。
- 本机已安装，CLI 在 `~/.nvm/versions/node/v24.22.1/bin/codebuddy`。

## 能力要点

- **终端原生**：管道友好（`git log | codebuddy "分析提交"`）、脚本集成、标准输入输出。
- **内置工具链**：文件编辑、命令运行、Git 操作、测试执行、智能提交。
- **扩展**：MCP 接第三方工具；Skills、Hooks、Subagents、斜杠命令；配置分层与环境变量。
- **A2A**：CLI 可作标准 A2A 客户端发现并调用其他授权 Agent，支持并行委派；`--a2a` 隐藏模式以 stdio 常驻服务供 SDK / CloudAgent 调用；`A2ASendMessage` 可带 URL 附件。
- **无头与后台**：headless `-p` 输出 text / json / stream-json；后台任务实时推送输出，可主动取消；`--output-format json` + `--json-schema` 得结构化输出。
- **精简产物**：`codebuddy-lite-wb` 面向 WorkBuddy 场景，冷启动更快、常驻内存更低。
## 官方入口

`https://www.codebuddy.cn/docs/cli/overview`；发布说明 `https://www.codebuddy.cn/docs/cli/release-notes/v2.143.0`。

## 一句话主线

**CodeBuddy 是「终端原生 + 云 IDE」双形态编码 Agent，差异化在 A2A 双向能力与 WorkBuddy 精简产物。**

## 参考资料

- CodeBuddy 官方文档与发布说明，未附固定链接
