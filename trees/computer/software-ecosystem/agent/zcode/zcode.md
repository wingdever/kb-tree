---
description: "ZCode by Z.ai: open-source agentic development environment with dynamic workflows"
描述: "Z.ai 的 ZCode：开源的 Agent 化开发环境与动态工作流"
name: "ZCode"
名称: "ZCode"
---

# ZCode

> 来源：ZCode 官方仓库与 2026 年开源报道。版本与功能变化快，以官方仓库为准。

ZCode 是 Z.ai（原智谱）的 **Agentic Development Environment**，2026-09 以 Apache-2.0 开源。本页是生态样本视角；机制见 `../../../ai/agent/`。

## 形态与厂商

- 厂商：Z.ai（原智谱），默认模型 GLM 系列，并支持接入 DeepSeek、Anthropic、OpenAI 兼容端点。
- 三形态统一进 `zcode` 命令：`zcode` 进 TUI、`zcode --web` 起本地 Web 工作台、Desktop 为 Electron 应用（Windows / macOS / Linux，x64 与 arm64）。
- 开源仓库 `zai-org/ZCode`，包含桌面端、Web 客户端、HTTP/WebSocket Server、共享 UI、Provider、Agent CLI 与 Agent Runtime；Agent Runtime 同时服务 Desktop 与 Web。

## 能力要点

- **Agent 居中**：文件管理、终端、Git 面板、浏览器预览围绕对话排布，面向长周期任务。
- **动态工作流**：用 Workflow 脚本编排多个 Sub-Agent，`/workflow` 启动。
- **配套能力**：Goal、Remote Control、Browser Use、Skill 导入、Zread 知识库、Git 可视化、多端跟进（飞书 / 微信 Bot 接入同一工作区）。
- **缓存命中**：生态报道称其在 DeepSeek 缓存命中率上表现突出——机制见 `../../../ai/api/deepseek/kv-cache/kv-cache.md`。

## 安全与来源背景

2026 年曾有旧版客户端工作区快照上传的隐私争议；厂商致歉并整改：v3.14.0 移除 Repo Wiki、切断本地仓库快照上传链路，并邀请第三方安全审查。**引用这段历史是为了选型时判断信任边界**，不是给产品定性；以当前版本与官方公告为准。

## 在树中的位置

- 名称撞车：另有个人项目 `zmccyy/ZCode--CLI--agent`，与本页无关。
- 同类样本：`../codebuddy/`、`../qodercn/`、`../trae/`。
- 动态工作流与多 Agent 见 `../../../ai/agent/multi/`；技能见 `../../../ai/agent/skill/`；渠道见 `../../../ai/agent/channel/`。

## 官方入口

GitHub 仓库 `zai-org/ZCode`（搜索即达）；产品信息以 Z.ai 官方页面为准。

## 一句话主线

**ZCode 是「开源 + Agent 居中 + 动态工作流」的国产 IDE 样本；选型时把 2026 年的隐私整改作为信任边界的具体案例来看。**

> 相关：Agent 子生态见 `../agent.md`；编码 Agent 见 `../../../ai/agent/coding/`。
