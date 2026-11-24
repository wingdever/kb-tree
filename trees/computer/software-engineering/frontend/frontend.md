---
description: "Frontend development: browser rendering, event loop, UI state, build and delivery, performance, security and agent-facing UI"
描述: "前端开发：浏览器渲染、事件循环、UI 状态、构建交付、性能、安全与面向 Agent 的界面"
name: "Frontend Development"
名称: "前端开发"
---

# 前端开发（Frontend Development）

> 来源：web.dev Core Web Vitals 与 MDN JavaScript 执行模型等官方文档。指标、阈值与浏览器行为变化快，以官方文档为准。

前端开发关注**用户如何看见和操作服务**：浏览器如何渲染、事件如何调度、UI 状态如何组织、代码如何构建交付、性能与安全边界在哪。它与 `../backend/` 的分工是：后端处理「一个请求进来后服务端怎样正确完成」，前端处理「结果怎样变成可交互的界面，以及用户动作怎样变成请求」。

两者共用同一套机制的不同形态：「并发」在后端是线程/协程与限流，在前端是事件循环与微任务；「状态」在后端是会话外置，在前端是组件状态与本地存储；「缓存」在后端是服务端缓存，在前端是 HTTP 缓存与浏览器存储。

## 浏览器与渲染模型

- **DOM 与样式**：HTML 解析成 DOM 树，CSS 形成 CSSOM，两者合成渲染树；布局计算几何位置，绘制生成像素，合成把层交给 GPU。
- **重排与重绘**：改几何属性触发 layout + paint，只改颜色等多只触发 paint；批量读写、用 transform/opacity 做动画可避开重排。
- **事件循环**：JS 是单线程 + 事件循环。调用栈执行同步代码，异步回调作为 job 入队；HTML 事件循环把 job 分为 task 与 microtask，**微任务队列先清空**再取下一个 task；每个 job 运行到完成（run-to-completion）才让位。单个 job 过长会阻塞点击/滚动——这是「把长任务切片」的根据。

事件循环与后端的并发模型对照见 `../backend/`，底层的并行与一致性见 `../../computer-organization/parallel/parallel.md`。

## UI 状态与组件

- **声明式 UI**：描述「状态 → 界面」的映射，而不是手工操作 DOM；组件是状态与视图的边界。
- **状态分层**：服务端数据（缓存）、会话状态、组件局部状态、URL 状态各归其位；把不该共享的状态提到全局是常见复杂度来源。
- **双向数据流与表单**：输入受控/非受控、校验时机、提交与错误呈现；与后端的幂等键配合避免重复提交。
- **组件边界**：接口最小化、状态就近、可复用与可测试——与 `../architecture/` 的模块化取舍同源。

## 构建与交付

- **模块与打包**：ES modules、依赖图、tree shaking、code splitting；构建产物要可复现。
- **sourcemap 与调试**：生产错误需能映射回源码；与 `../devops/` 的可观测性打通。
- **交付形态**：CSR（客户端渲染，首屏依赖 JS）、SSR（服务端渲染首屏）、静态生成、hydration；选择取决于首屏、SEO、交互复杂度与部署约束。
- **资源加载**：`async`/`defer`、预加载、缓存策略；与 HTTP 缓存、CDN 的边界在 `../devops/`。

## 性能与体验

Core Web Vitals 三项（稳定指标，75 分位评估）：

| 指标 | 衡量 | 良好阈值 |
|---|---|---|
| LCP | 最大内容元素何时可见（加载） | ≤ 2.5 秒 |
| INP | 交互到下一帧的响应（互动性） | ≤ 200 毫秒 |
| CLS | 视觉稳定性，意外布局偏移 | ≤ 0.1 |

INP 于 2024 年取代 FID 成为稳定指标。指标会被更好的替代者淘汰，不要把它们当永恒标准。长列表虚拟化、图片尺寸预留、字体加载策略分别对应 LCP / CLS 的常见失败。

## 安全边界

- **XSS**：不可信内容插入 DOM 前转义；CSP 限制可执行来源。
- **CSRF**：跨站请求伪造依赖浏览器自动带凭证；用 SameSite Cookie、token 或自定义头防御。
- **同源与跨域**：CORS 是浏览器的资源读取策略，不是鉴权机制；鉴权仍在服务端，见 `../security/`。
- **敏感数据**：前端存储（localStorage / Cookie）不是安全保险箱，token 泄露面比服务端大。

## 与 Agent 的关系

- **流式渲染**：Agent 逐 token 输出，前端要增量追加而非等完整响应；SSE / WebSocket 的解析、断线重连、游标续传是前端职责，协议侧见 `../../ai/api/deepseek/chat-completions-ref/streaming/`。
- **工具调用可视化**：把 `tool_calls`、观察结果与推理过程渲染成可审计的轨迹，避免用户只看到最终答案；状态结构见 `../../ai/agent/tool/`。
- **人在回路**：审批门、interrupt、状态编辑需要前端提供明确的操作点与回滚能力，见 `../../ai/agent/langgraph/`。
- **Browser Use / Computer Use**：Agent 反过来驱动浏览器，DOM 成为工具面，见 `../../ai/agent/browser-use/` 与 `../../ai/agent/computer-use/`。
- **前端作为渠道**：Web UI 是自建渠道之一（无第三方协议风险、要自己做鉴权与部署），见 `../../ai/agent/channel/`。
- **可观测性对接**：前端把用户交互与 Agent 事件上报，串进同一条 trace，见 `../../ai/agent/obs/`。

## 学习资源

| 资源 | 内容 | 许可 / 入口 |
|---|---|---|
| The Modern JavaScript Tutorial（`javascript.info`） | JS 语言 + 浏览器：DOM、事件、网络请求、存储、Web Components；页面标注 2026-11-20 更新 | 免费在线 `javascript.info` |
| Front End Interview Handbook（`yangshun/front-end-interview-handbook`） | HTML/CSS/JS 知识题、前端系统设计、按公司分类的面试题 | MIT，`frontendinterviewhandbook.com` |
| Full Stack Open | React / Redux / TypeScript / Node / GraphQL / Next.js，14 部分，含测试与 CI/CD、容器 | CC BY-NC-SA 3.0（禁商用），`fullstackopen.com` |

## 常见失败模式

- 长任务阻塞事件循环，导致 INP 恶化。
- 无界状态提升，组件耦合、渲染范围失控。
- 图片/字体无尺寸预留，CLS 飙升。
- 把 CORS 当鉴权，把 localStorage 当安全存储。
- 流式渲染只显示最终答案，隐藏工具调用与失败轨迹，用户无法审计。
- Agent 前端缺审批与回滚入口，人在回路退化成装饰。

## 一句话主线

**前端是「状态到界面」的映射层：浏览器模型定边界，状态与构建定结构，性能与安全定底线；在 AI 工程里还要把流式轨迹、工具调用与审批门变成可审计的界面。**

> 相关：软件工程总览见 `../software-engineering.md`；后端开发见 `../backend/`；质量与测试见 `../quality/`；安全见 `../security/`；架构见 `../architecture/`；运维见 `../devops/`。
