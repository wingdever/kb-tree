---
description: "Qwen Code: open-source CLI with 1,000 free requests per day via Qwen OAuth"
描述: "Qwen Code：开源 CLI，Qwen OAuth 每天 1,000 次免费请求"
name: "Qwen Code"
名称: "Qwen Code"
---

# Qwen Code

Qwen Code 是阿里开源的终端 Coding Agent，官方提供 Qwen OAuth 免费层；它属于“开源客户端 + 官方托管额度”，不是纯 BYOK。


## 免费额度

Qwen OAuth 免费层每天 1,000 次请求；早期文档写 2,000 次/天，已调整为 1,000；一次提示可能触发多个模型请求；免费额度与 Qwen Code 账号绑定。

## 接入方式

官方开源 CLI，支持 MCP、工具调用与多轮 Agent；最适合直接子进程接入，也可包成 MCP 工具；额度与登录态由 Qwen 管理。

## 限制与风险

每天 1,000 次请求，按请求而非按任务计；免费模型与额度可能调整；高并发会触发限流；不适合商业 SLA。

## 适合谁

最适合个人开发者做日常 Agent 编码与自动化；也是自有 Agent 接入成本最低的免费 CLI 之一。

## 参考资料

- https://github.com/QwenLM/qwen-code
- https://qwen.ai/blog?id=4074cca80393150c248e508aa62983f9cb7d27cd&from=research.latest-advancements-list
