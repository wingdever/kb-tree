---
description: "Next.js: a React framework for full-stack web applications, with App Router, Server and Client Components, Route Handlers and Server Actions"
描述: "Next.js：构建全栈 Web 应用的 React 框架，含 App Router、服务端/客户端组件、路由处理器与服务端动作"
name: "Next.js"
名称: "Next.js"
---

# Next.js

> 来源：Next.js 官方文档。框架 API 与渲染模型变化快，以官方文档为准。

Next.js 官方定义是**用于构建全栈 Web 应用的 React 框架**：用 React 组件构建界面，Next.js 提供额外的功能与优化，并自动配置 bundler、compiler 等底层工具。它不是一个微服务框架——没有服务发现、熔断、治理等机制；它的服务端能力用于在同一应用内处理数据获取、写入与 API 端点。把它归到前端/全栈一侧，是因为它统一了 UI 与服务端渲染、数据获取和路由。

## 两套路由

- **App Router**：较新的路由，支持 Server Components 等 React 新特性，内置 React canary 版本（含稳定的 React 19 改动与正在验证的新特性）。
- **Pages Router**：原有路由，仍受支持并持续改进，使用项目 `package.json` 里安装的 React 版本。

两种路由在侧边栏切换，新项目以 App Router 为主。

## App Router 核心能力

- **项目结构与约定**：用文件夹和文件约定组织路由；`layout.tsx`、`page.tsx`、`loading.tsx`、`error.tsx` 等 special files 对应布局、页面与状态 UI。
- **Server 与 Client Components**：同一应用里部分组件在服务端渲染、部分在客户端渲染。服务端组件可直接访问服务端数据源，客户端组件承担交互。二者分工是 App Router 的核心心智模型。
- **数据获取与流式**：服务端获取数据并把依赖数据的界面流式送出，避免整页等待最慢的数据源。
- **数据变更**：用 Server Functions / Server Actions 做写入，配合 `revalidatePath`、`revalidateTag`、`updateTag` 做缓存失效。
- **缓存与再验证**：缓存数据与 UI，支持基于时间与按需（on-demand）两种再验证策略；`cacheLife`、`cacheTag`、`unstable_cache` 等函数控制缓存生命周期。
- **Route Handlers**：用 Web Request / Response API 创建自定义请求处理器，即应用内的 HTTP 端点；`NextRequest`、`NextResponse` 是其扩展。
- **Proxy**：在请求完成前改写、重定向、修改请求头或直接响应，适合鉴权与路由前置逻辑。
- **错误处理**：区分预期错误与未捕获异常，分别用 error boundary 与全局错误处理。
- **内联优化**：内置图片优化、字体优化、metadata 与动态 OG 图片，以及 CSS 方案（Tailwind、CSS Modules、Global CSS 等）。
- **部署与升级**：支持部署到多种平台，并可升级到最新版或 canary。

## 定位与边界

Next.js 解决的是**单应用内的全栈问题**：UI 渲染、路由、数据获取与变更、缓存、API 端点。它不解决**多服务之间的治理问题**：服务发现、跨服务熔断、分布式追踪、服务间认证由专门的微服务基础设施处理。

因此常见组合是：前端与 BFF 用 Next.js，后端领域服务用独立服务；Next.js 的 Route Handlers 承担面向浏览器的聚合层，而不是替代后端服务。

## 常见失败模式

- 把 Server Component 写成重计算同步逻辑，拖慢服务端渲染。
- 在客户端组件里请求本可服务端直取的数据，丢失流式与缓存收益。
- 用 Route Handlers 堆出庞大后端，绕过服务边界与治理。
- 缓存失效策略与数据更新不同步，出现陈旧 UI。
- 混用两套路由且共享状态，增加维护成本。
