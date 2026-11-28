---
description: "Integrating consumer coding agents through official SDK, CLI, or OpenAPI; quota and terms boundaries"
描述: "C 端 coding agent 接入：官方 SDK、CLI、OpenAPI 与免费额度边界"
name: "Consumer Coding Agent Integration"
名称: "C 端 Coding Agent 接入"
---

# C 端 Coding Agent 接入

结论先说：**能接，但只接官方可编程入口；免费额度不等于 API 配额。** 一个 C 端 coding agent 只要有 Agent SDK、非交互 CLI 或 OpenAPI/OAuth，就可以被自己的 Agent 当成外部工具调用；只有 UI 的产品，技术上也能用浏览器自动化，但不适合生产。

## 四种入口

| 入口 | 形态 | 可接入性 | 主要风险 |
| --- | --- | --- | --- |
| Agent SDK | TypeScript / Python SDK，程序化创建会话、流式收消息 | 最好 | 版本变动、登录态与配额 |
| 非交互 CLI | `-p/--print`、`--output-format stream-json`、`--mcp-config` | 好，适合子进程适配 | 进程管理、超时、输出解析 |
| OpenAPI / OAuth | 第三方应用授权，拿 access token 调接口 | 好，适合 SaaS | 应用审核、权限范围、用户同意 |
| UI / 浏览器自动化 | 点击、截图、模拟输入 | 最后手段 | 脆弱、封号、违反条款 |
| 逆向私有接口 | 抓包、复用 token | 不建议 | 不稳定、法律与账号风险 |

## 具体到 WorkBuddy / CodeBuddy

- **CodeBuddy** 同时有 IDE、插件与 CLI，并提供 Agent SDK（TypeScript/Python）。SDK 支持复用 CLI 登录态或 API Key 认证，可以程序化创建会话、流式接收消息。
- **CodeBuddy CLI** 支持 `-p/--print` 非交互执行、`stream-json` 输入输出与 MCP 配置；适合被上层 Agent 作为子进程调用，再解析事件流。
- **WorkBuddy** 开放平台提供 OAuth 2.1 授权码流程，第三方应用拿到 access token 后调用 Open API；适合“用户授权后替用户执行”的接入，不是拿一个免费账号当公共后端。
- 公开定价显示体验版有免费积分（如每月 500 积分），但积分是产品内计量；能否通过 SDK/OpenAPI 调用、是否消耗同一份额度，要以开放平台与条款为准。

## 推荐接入契约

不要只封装一个 `run(prompt)`。外部 coding agent 是一个有会话、有工作区、有副作用的过程，契约至少要有：

- `submit(task, workspace, constraints) -> run_id`：任务、仓库快照、允许目录、时间与费用预算。
- `stream_events(run_id)`：计划、工具调用、文件变更、命令输出、错误、完成事件。
- `cancel(run_id)`：超时、用户取消、策略拦截时能干净停止。
- `collect_artifacts(run_id)`：补丁、日志、测试结果、生成文件。
- `health()` / `quota()`：登录态、额度、速率限制、模型可用性。

## 推荐架构

1. **适配器进程**：把 SDK 或 CLI 包在一个独立进程/容器里，不让主 Agent 直接持有供应商 token。
2. **工作区沙箱**：只挂载任务需要的仓库目录；命令、网络与文件写入按最小权限限制。
3. **事件流解析**：把供应商的 stream-json 或 SDK message 归一化成自己的事件协议。
4. **预算与超时**：按任务设 token、费用、轮次与墙钟上限；超限先取消再回收。
5. **凭据保管**：token 放密钥库，不进提示词、不进模型上下文、不写日志。
6. **审计与回滚**：记录谁在什么工作区调用了哪个外部 Agent；代码变更先出补丁，不自动合并。
7. **降级路径**：免费额度耗尽或登录态失效时，切到备用模型/工具，不要让主流程卡死。

## 免费额度的真实边界

- 免费额度通常绑定个人账号，不能共享、 pooling、批量注册或换号规避限额。
- 免费层常有速率限制、并发限制、模型降级与功能限制；复杂任务一次会消耗多次调用。
- 免费额度可能随时调整或取消；把产品后端建在免费 C 端套餐上，等于把 SLA 建在别人的促销政策上。
- 是否允许自动化、第三方封装、对外提供服务，要看服务条款；技术能跑不等于条款允许。
- 生产用途优先走付费 API、企业版或正式开放平台，免费额度只做实验与低频兜底。

## 什么时候不该接

- 产品没有官方 SDK/CLI/OpenAPI，只能靠浏览器点击。
- 条款禁止自动化、转售、共享账号或第三方封装。
- 需要高并发、稳定 SLA、团队多租户或审计留痕。
- 任务涉及敏感代码、生产凭据或不可逆操作，而对方权限模型不透明。
- 供应商登录态依赖个人浏览器，无法安全托管。

## 一句话主线

C 端 coding agent 可以作为“外部 Agent 工具”接入，但入口必须是官方的 SDK、非交互 CLI 或 OpenAPI；免费额度只能做实验，不能当生产后端。

## 参考资料

- CodeBuddy Agent SDK 文档（2026）：https://www.codebuddy.ai/docs/zh/cli/sdk
- CodeBuddy CLI 参考（2026）：https://www.codebuddy.ai/docs/cli/reference
- CodeBuddy MCP 文档（2026）：https://www.codebuddy.ai/docs/cli/mcp
- WorkBuddy 开放平台 Open API（OAuth 2.1）：https://open.workbuddy.cn/docs/openapi
- WorkBuddy 定价与体验版额度（2026）：https://www.workbuddy.cn/pricing/
- CodeBuddy 定价与体验版额度（2026）：https://copilot.tencent.com/pricing
- WorkBuddy 免费额度政策（2026）：https://www.workbuddy.cn/llms.txt
