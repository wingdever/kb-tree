---
description: "Browser-use agents: DOM versus vision perception, browser-agent frameworks, production patterns and safety"
描述: "浏览器 Agent：DOM 与视觉两种感知、框架对照、生产模式与安全边界"
name: "Browser-Use Agents"
名称: "浏览器 Agent"
---

# 浏览器 Agent（Browser Use）

浏览器 Agent 让模型**驱动真实浏览器完成任务**：填表、检索、下单、抓取。提供角色、标签、层级与文本，而整台电脑的截图没有这种结构。这个差异决定它能比通用桌面 Agent 更便宜、更确定，但也只能覆盖浏览器内的事。

## 两种感知方式

| 方式 | 原理 | 优点 | 代价 |
|---|---|---|---|
| **结构化（DOM / a11y 树）** | 读元素角色、名称、引用，给出带类型的动作空间 | 快、省 token、确定性强；无需视觉模型 | 改版、canvas、iframe 内虚拟 DOM 易失效 |
| **视觉（截图 + 视觉模型）** | 看渲染结果，按坐标点击 | 对改版与无语义界面鲁棒 | 慢、贵（每步约数倍到十几倍），像素定位会误判 |

这是组织整个领域的主轴：各框架都是混合体，区别在**默认用哪一端**。生产常见做法是结构化为主、视觉兜底——选择器在 canvas 或反爬界面持续失败时再切视觉或 Computer Use。

## 框架对照

| 框架 | 定位 | 感知默认 | 许可 |
|---|---|---|---|
| **Browser Use** | Python 的 agent 库，模型写 Python 在持久 REPL 里通过 CDP 驱动浏览器 | DOM 为主，视觉可选 | MIT |
| **Stagehand** | TypeScript，架在 Playwright 上的 AI 增强层：四个原语，稳定处用脚本、不确定处才调模型 | DOM + 代码混合 | MIT |
| **Skyvern** | 视觉优先的 RPA 平台：Planner → Actor（截图点坐标）→ Validator | 视觉为主 | AGPL-3.0 |
| **Playwright MCP** | 把浏览器暴露成 MCP 工具面，不带自己的 agent 循环 | a11y 树 | Apache-2.0 |
| **Playwright** | 底层确定性自动化库，非 AI 产品 | 选择器 / a11y | Apache-2.0 |

选型看交付目标：嵌入式页面副驾 → 页内 / a11y 方案；无人值守批处理 → Browser Use；TypeScript 工程管线 → Stagehand；旧系统无语义页面 → 视觉方案；确定性流程 → Playwright。

## Browser Use 的架构

核心极简：**模型 + 持久 REPL + CDP**。模型写一个 Python cell（如 `new_tab(url)`、`bu.click(41)`、`js(...)`），REPL 在真实 Chrome 上执行，结果回灌模型；任务结束调 `finish(result)`。

要点：

- 浏览器后端可选云端、全新本地 Chromium、或带远程调试的现有 Chrome（复用登录态）。
- 支持结构化输出、自定义工具、上传下载、续任务与持久 session。
- 官方强调**钉死版本**（`==`，不用 `>=`）——项目迭代快，发布会破坏兼容性。
- 云端提供隐身浏览器、代理与 CAPTCHA 代解；`type_secret()` 传敏感值。

## 成本与生产模式

每一步都可能是一次模型调用：新颖任务可接受，重复流程很贵。**生产里的做法是分层**：把稳定步骤固化成确定性脚本（Playwright 一类），只把需要判断的少数步骤交给 Browser Use；视觉路线每步都要一张截图加一次推理，比直接读 DOM 更贵，常见任务上的成功率也更低。

可观测性必需：记录轨迹、动作高亮、失败判定与 prompt injection 检测。Browser Use 的运行后 judge 会给出 `success`、`failure_reason`、`prompt_injection_detected` 等信号——这些是评估输入，不是保证。

## 安全边界

- **不是沙箱**：域名 allow/block、`type_secret()` 的红acted输出都是约束而非隔离；模型写的 Python 能读到值，截图和 JS 也能泄露。
- **提示注入**：网页内容是不可信输入，可能劫持 Agent 目标；把页面文本当工具结果看待，关键操作要人审批。
- **登录态与凭据**：复用现有 Chrome profile 意味着复用浏览器里的一切，隔离账号优于共享 profile。
- **合规**：云端代解 CAPTCHA、 residential proxy 等能力涉及平台条款；越要自己承担规则责任。

## 与树中其它节点的关系

- 感知与工具面建立在 DOM / a11y 上。

## 一句话主线

**浏览器 Agent 的价值来自「浏览器自带结构」：默认用 DOM/a11y 求快求稳，视觉只在必要时兜底；生产上把重复流程交给确定性脚本，把需要推理的少数步骤交给 Agent，并用审计与审批兜住不可信页面。**

## 参考资料

- Browser Use 官方仓库：https://github.com/browser-use/browser-use
- Playwright 官方文档：https://playwright.dev
