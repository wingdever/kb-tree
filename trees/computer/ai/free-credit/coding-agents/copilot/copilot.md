---
description: "GitHub Copilot Free: 2,000 completions and 50 chat requests per month, agent mode and CLI included"
描述: "GitHub Copilot 免费版：每月 2,000 次补全、50 次对话，含 Agent 模式与 CLI"
name: "GitHub Copilot Free"
名称: "GitHub Copilot Free"
---

# GitHub Copilot Free

GitHub Copilot 的免费层是长期免费档，不是一次性试用；它把补全、对话、Agent 模式与 Copilot CLI 打包进个人 GitHub 账号。


## 免费额度

每月 2,000 次行内补全、50 次对话请求（含 Copilot Edits）；免费档只能用 Auto 模型选择；Agent 模式与 Copilot CLI 包含在内；Cloud Agent、代码审查、第三方 Agent 不包含。

## 接入方式

官方入口是 IDE 插件与 Copilot CLI；免费档的 CLI 可被上层 Agent 作为子进程调用，但认证绑定 GitHub 账号，且只有 50 次对话额度，适合低频实验。

## 限制与风险

50 次对话对多步 Agent 任务很快耗尽；免费档不能选模型；组织已分配 Copilot 席位的用户不能回退到 Free；Cloud Agent 与代码审查不可用。

## 适合谁

适合验证 Copilot 工作流、做轻量补全与单轮问答；不适合作为自有 Agent 的稳定后端。

## 参考资料

- https://github.com/features/copilot/plans
- https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot
- https://github.blog/changelog/2025-02-11-github-copilot-chat-and-github-copilot-extension-now-available-for-free-on-github-mobile-and-github-cli/
