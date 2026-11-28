---
description: "OpenAI Codex: included in ChatGPT Free and Go with plan-dependent limits"
描述: "OpenAI Codex：ChatGPT Free/Go 也包含，额度随套餐变化"
name: "OpenAI Codex"
名称: "OpenAI Codex"
---

# OpenAI Codex

Codex 不再只属于付费档：OpenAI 官方帮助中心明确它包含在 ChatGPT 所有套餐中，包括 Free 与 Go；但 Codex Cloud 不包含在 Free/Go。


## 免费额度

Free 与 Go 可使用 Codex 桌面端、CLI、IDE 扩展与网页入口，具体用量上限随套餐变化，官方未公布固定条数；Codex Cloud 仅 Plus/Pro/Business/Enterprise 等符合条件账号可用。

## 接入方式

官方 CLI `codex` 是最适合自有 Agent 调用的入口：登录 ChatGPT 账号即可，事件流与工作区行为可被包装；免费额度低，适合低频或兜底。

## 限制与风险

Free/Go 额度小且不公开；Codex Cloud 不可用；模型可用性随套餐变化；不适合高并发或长周期任务。

## 适合谁

适合已有 ChatGPT 账号的个人做低频 Agent 调用；生产应走付费 API 或付费套餐。

## 参考资料

- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://openai.com/codex/
