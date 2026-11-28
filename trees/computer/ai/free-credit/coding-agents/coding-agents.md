---
description: "A verified list of consumer coding agents with free quotas, their quota types and integration levels"
描述: "有免费额度的 C 端 Coding Agent 清单：额度类型、接入性与边界"
name: "Coding Agents with Free Quotas"
名称: "有免费额度的 C 端 Coding Agent"
---

# 有免费额度的 C 端 Coding Agent

这份清单按三个条件收口：**C 端可自助注册、能规划并修改代码、官方公开了免费额度或长期免费层**。纯 API 模型额度、纯开源但必须自带 Key 的客户端、一次性内测资格不单独算。截至 2026 年 11 月，能公开核验的有 20 个；其中 CodeBuddy 与 WorkBuddy 共用同一积分池，所以是 20 个产品、不是 20 份独立额度。产品调价频繁，额度以账号账单页为准。

## 清单

| 产品 | 免费额度 | 免费类型 | 接入性 |
|---|---|---|---|
| GitHub Copilot Free | 2,000 次补全 + 50 次对话/月，含 Agent 模式与 CLI | 长期免费 | 中：官方 CLI |
| Cursor Free | 有限 Agent/Chat，未公布固定条数 | 长期免费 | 弱：IDE/CLI 为主 |
| Windsurf Free | 25 prompt credits/月，另有零积分模型 | 长期免费 | 弱：IDE |
| Amazon Q Developer Free | 50 次 Agent 请求/月 | 长期免费 | 中：官方 CLI |
| OpenAI Codex | ChatGPT Free/Go 包含，额度随套餐 | 长期免费 | 强：官方 CLI/SDK |
| Google Antigravity Free | 每周基础 Agent 额度，未公布固定条数 | 长期免费 | 强：CLI/SDK/IDE |
| Qwen Code | 1,000 次请求/天 | 每日额度 | 强：开源 CLI |
| iFlow CLI | 个人免费，内置 Kimi K2/Qwen3 Coder/GLM | 长期免费 | 强：开源 CLI |
| Kilo Code Auto Free | 200 次请求/小时/IP | 长期免费 | 中：CLI/IDE |
| Trae Free | 国内 500 积分/月；国际版有限用量 | 每月额度 | 弱：IDE/云端任务 |
| CodeBuddy Free | 100 积分/月 + 30 积分/活跃日；与 WorkBuddy 共用同一积分池 | 每月额度 | 强：CLI/SDK/OpenAPI |
| WorkBuddy Free | 国内 500 积分/月 + 签到 100/天；国际版 100 + 30/天；与 CodeBuddy 共用同一积分池 | 每月额度 | 中：OpenAPI |
| Qoder Free | 2 周 Pro 试用 + 300 Credits | 限时试用 | 中：CLI/IDE |
| Baidu Comate Free | 5,000 积分，之后 Auto 免费模式每日限额 | 一次性 + 每日 | 弱：IDE |
| Huawei CodeArts Free | 500 积分/月 + 50 积分/天（口径有差异） | 每月 + 每日 | 中：CLI/TUI/IDE |
| ZCode Free Trial | 5 天，每天 800 万 GLM tokens | 限时试用 | 弱：桌面端 |
| JetBrains AI Free | 3 AI credits/30 天 + 无限补全 | 每月额度 | 弱：IDE |
| Bolt.new Free | 100 万 tokens/月，每日 30 万 | 每月额度 | 弱：Web UI |
| Lovable Free | 5 credits/天，每月上限 30 | 每日 + 月上限 | 弱：Web UI |
| v0 Free | $5 credits/月 + 7 条消息/天 | 每月额度 | 弱：Web UI |

## 额度类型

- **每月积分/credits**：Trae、CodeBuddy、WorkBuddy、JetBrains、Bolt、Lovable、v0。适合按月做预算，但积分单价和任务消耗不透明。
- **每日请求/额度**：Qwen Code、Kilo Code、Comate 的 Auto 模式、CodeArts 的每日赠送。适合连续轻量使用，不适合突发大批量。
- **一次性试用**：Qoder、ZCode、CodeBuddy 的新手积分与 Pro 试用。只能验证能力，不能当长期额度。
- **免费模型池**：iFlow CLI、Windsurf 的零积分模型、Kilo Auto Free。额度不按条数封顶，但模型质量、限流与数据政策会变。

## 接入性分级

- **强接入**：有官方 CLI/SDK/OpenAPI，能作为子进程或工具被自有 Agent 调用。代表：Codex、Qwen Code、iFlow CLI、CodeBuddy、Antigravity、Kilo Code。
- **中接入**：有官方 CLI 或 OpenAPI，但免费档额度小、认证绕、或产品定位不完全匹配。代表：Copilot、Amazon Q、WorkBuddy、CodeArts、Qoder。
- **弱接入**：只有 IDE/桌面/Web UI，没有公开 API。代表：Cursor、Windsurf、Trae、Comate、ZCode、JetBrains AI、Bolt、Lovable、v0。接它们只能做浏览器/桌面自动化，不适合生产。

## 共同限制

- **同厂共享池不能叠加**：CodeBuddy 与 WorkBuddy 共用同一账号积分池，WorkBuddy 每日签到 100 积分也进入同一池；不能把两个产品的额度相加。其他厂商也可能有同类共享规则，按账号页为准。
- **免费额度不是 API 配额**：产品内积分、对话次数、token 包，不等于可以自由调用 API 的配额；能否自动化要看条款与开放平台。
- **绑定个人账号**：多数免费档只限一个自然人一个账号，禁止共享、拼号、批量注册、换号刷额度。
- **额度与模型会变**：免费档常用 Auto 路由、限时活动、容量调度；今天能用的模型明天可能降级。
- **无 SLA**：免费档没有可用性承诺，限流、排队、停服都可能发生；不能把产品后端建在免费档上。
- **数据政策不同**：免费模型可能记录 Prompt 用于改进服务；敏感代码不要走免费路由。

## 边界与排除

- **Claude Code**：Free 档不包含，需 Pro/Max/Team 或 API 额度。
- **Gemini CLI / Gemini Code Assist 个人版**：Google 已从 2026-06-18 起停止为个人免费档提供服务，迁移到 Antigravity；旧配额页仍可能显示 1,000 次/天，不能当现行额度。
- **Firebase Studio**：2026-06-22 起停止新工作区与注册，2027-03-22 停服；只保留存量用户。
- **Replit Starter**：2026-11 起不再向新用户开放，只有存量用户还有免费档。
- **Warp Free**：终端免费，但免费档不含 Warp 托管的 AI 用量，需要 BYOK 或按量购买，不算免费算力。
- **CodeGeeX、iFlyCode、Tabnine**：有免费补全或基础功能，但不是能多步自主改代码的 Agent；未列入本清单。
- **Cline、Roo Code、OpenCode**：客户端开源免费，但模型要自带 Key，不算官方免费算力。
- **Kimi Code、Claude Code、Devin**：没有长期免费 Agent 额度，未列入。

## 怎么选

- 要接进自有 Agent：先试 **Codex、Qwen Code、iFlow CLI、CodeBuddy、Antigravity、Kilo Code**；它们有官方 CLI/SDK，适配成本最低。
- 要在 IDE 里日常用：**Copilot、Cursor、Windsurf、Trae、Comate、CodeArts、Qoder** 更合适，但别指望当 API。
- 要做 Vibe Coding 原型：**Bolt、Lovable、v0** 额度直观，但只有 UI，不适合后台集成。
- 要生产：免费档只做实验与兜底，正式容量走付费 API、企业版或 Coding Plan。

## 维护方式

每月复核一次三件事：免费档是否还在、额度数字是否变化、条款是否允许自动化。清单里的“截至 2026-11”不是永久承诺；产品一旦改价，节点要同步更新，不能拿旧截图当现行规则。

## 参考资料

- GitHub Copilot 套餐：https://github.com/features/copilot/plans
- Cursor 模型与定价：https://cursor.com/docs/models-and-pricing
- Windsurf 额度文档：https://docs.windsurf.com/windsurf/accounts/usage
- Amazon Q Developer 定价：https://aws.amazon.com/q/developer/pricing/
- OpenAI Codex 与 ChatGPT 套餐：https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Google Antigravity 定价：https://antigravity.google/pricing/
- Qwen Code 仓库：https://github.com/QwenLM/qwen-code
- iFlow CLI：https://cli.iflow.cn/
- Kilo Code 限额：https://kilo.ai/docs/getting-started/rate-limits-and-costs
- Trae 国内定价：https://www.trae.cn/pricing
- CodeBuddy 订阅：https://www.codebuddy.ai/docs/ide/Account/Subscription
- WorkBuddy 定价：https://www.workbuddy.cn/pricing/
- Qoder 计费：https://help.aliyun.com/zh/lingma/product-overview/product-billing/
- Baidu Comate 定价：https://comate.baidu.com/zh/pricing
- Huawei CodeArts 定价：https://codearts.huaweicloud.com/pricing.html
- ZCode 配置与试用：https://zcode.z.ai/en/docs/configuration
- JetBrains AI 定价：https://www.jetbrains.com/store/ai/
- Bolt 定价：https://bolt.new/pricing
- Lovable 定价：https://lovable.dev/pricing
- v0 定价：https://v0.app/docs/pricing
- Gemini Code Assist 个人版停服说明：https://developers.google.cn/gemini-code-assist/resources/faqs
- Firebase Studio 停服说明：https://firebase.google.cn/docs/studio/get-started
- Replit Starter 说明：https://docs.replit.com/billing/plans/starter-plan
