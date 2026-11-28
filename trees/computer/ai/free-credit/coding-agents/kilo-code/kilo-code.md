---
description: "Kilo Code Auto Free: 200 free model requests per hour per IP"
描述: "Kilo Code Auto Free：每 IP 每小时 200 次免费模型请求"
name: "Kilo Code Auto Free"
名称: "Kilo Code Auto Free"
---

# Kilo Code Auto Free

Kilo Code 是开源 Coding Agent，个人平台免费；它的 Auto Free 档把请求路由到可用免费模型，按 IP 限流。


## 免费额度

Auto Free（`kilo-auto/free`）$0，每 IP 每小时 200 次请求；平台个人版 $0；付费模型、Kilo Pass、云 Agent 计算另计。

## 接入方式

VS Code、JetBrains 与 CLI 都有入口；CLI 可被自有 Agent 调用；免费档的模型路由与限流由 Kilo 控制。

## 限制与风险

每小时 200 次，按 IP 共享，团队/多进程会互相挤占；免费模型可能记录 Prompt，敏感代码不要走 Auto Free；模型质量与可用性动态变化。

## 适合谁

适合个人与低频自动化；敏感代码、商业项目应切 BYOK 或付费路由。

## 参考资料

- https://kilo.ai/docs/getting-started/rate-limits-and-costs
- https://kilo.ai/pricing/
