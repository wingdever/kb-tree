---
description: "Software engineering: applying systematic methods to build, test, deploy and maintain reliable software at scale"
描述: "软件工程：用系统方法在规模上构建、测试、部署与维护可靠软件"
name: "Software Engineering"
名称: "软件工程"
---

# 软件工程（Software Engineering）

软件工程是把**系统化、可度量的方法**应用于软件的开发、运行与维护——把不确定业务需求转化为一串受控的技术决策，在成本、时间、质量与风险的约束下交付可靠软件。核心价值是**受控的变更**：让团队持续交付、满足合规、适应变化，而不是反复重写。

软件工程降低风险但不消除不确定性——团队在建造中学习、用户改变行为、依赖演进、安全威胁演化、旧决策约束新决策。大多数业务不需要"为了美而美"的代码，而需要能上线产品、服务客户、满足合规、集成伙伴、无需反复重写就能适应的系统。

## 子树导航

| 子树 | 关注点 | 入口 |
|---|---|---|
| 软件生命周期 | 需求→设计→实现→测试→部署→维护的循环，需求工程与追溯 | `sdlc/sdlc.md` |
| 架构与设计 | 架构风格谱系、质量属性权衡、清洁/六边形/CQRS、单体与微服务 | `architecture/architecture.md` |
| 质量与测试 | 测试金字塔、单元/集成/契约/性能/安全测试、TDD/BDD、代码评审、左移 | `quality/quality.md` |
| 交付与运维 | CI/CD、部署策略、可观测性、SRE/SLI/SLO/错误预算、事故响应、平台工程 | `devops/devops.md` |
| 后端开发 | 在线服务的并发模型、限流背压、幂等与状态管理、服务设计 | `backend/backend.md` |
| 前端开发 | 浏览器渲染、事件循环、UI 状态、构建交付、性能安全与 Agent 界面 | `frontend/frontend.md` |
| 方法论 | Waterfall、Agile、Lean、Spiral、RAD 及选择依据 | `methodology/methodology.md` |
| 规格驱动开发 | 以可审查规格为真相源驱动 Agent 实现：四阶段工作流、三层框架、Spec Kit 与 Kiro | `spec-driven/spec-driven.md` |
| 氛围编程 | 自然语言描述意图、靠运行反馈引导的探索式编码：理念、Vibe & Verify、边界与失败模式 | `vibe-coding/vibe-coding.md` |
| 安全与隐私 | 威胁建模、安全默认、最小权限、隐私设计、安全左移 | `security/security.md` |
| 现代工程趋势 | AI 辅助开发、低代码/无代码、工具链即战略资产、持久技能 | `trends/trends.md` |
| 学习资源 | 开源软件工程书、DDIA 中文译本、系统设计面试资源与书单 | `learning/learning.md` |

## 一句话主线

**把模糊需求变成可验证规格，用架构把质量属性显式化，用分层测试与自动化把变更风险压到可发布，再用可观测性与反馈把生产中的学习送回下一轮需求。**

> 相关：计算机学科总览见 `../computer.md`；AI 工程（AI 应用的工程化）见 `../ai/ai.md`；AI Agent 的评估与可观测性见 `../ai/agent/eval/` 与 `../ai/agent/obs/`。
