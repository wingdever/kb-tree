---
description: "Modern software engineering concerns: AI-assisted development, LLM integration, low-code, platform tooling and durable skills"
描述: "现代软件工程关切：AI 辅助开发、LLM 集成、低代码、平台化工具链与持久技能"
name: "Modern Software Engineering Trends"
名称: "现代软件工程趋势"
---

# 现代软件工程趋势（Modern Software Engineering Trends）

工程实践随技术供给持续演进。下面几项在当下已经从"尝鲜"变成工程决策中的常规变量。

## AI 融入开发

- **AI 辅助编程工具**（Copilot、Claude 等）成为标准预期，覆盖补全、生成、重构、解释、测试生成。
- **LLM API 集成**、提示工程、AI 安全与伦理成为开发者技能栈的一部分；相关 Agent 工程方法见 `../../ai/agent/` 与 `../../ai/agent/prompt/`。
- **人类角色转向指导、评估与整合 AI 产出**：审查生成代码、验证行为、把控边界，而不是逐行编写。
- 风险点：生成代码的许可证与来源、隐蔽 bug、对生成结果的过度信任——AI 产出同样需要测试与评审（`../quality/quality.md`）。

## 低代码 / 无代码

成为技术组合的标准部分，适合业务逻辑简单、有稳定 API 集成、变更速度优先的场景。必须设边界与集中治理：避免逻辑重复、影子 IT、不可迁移的锁定。复杂领域、强性能或强合规场景仍需专业工程。

## 平台化与工具链即战略资产

成熟团队把工具链当战略资产：内部开发者门户、标准化环境、可复用流水线降低配置漂移，平台工程团队提供"黄金路径"（`../devops/devops.md`）。工具链和基础设施代码一样，需要版本化、评审与维护。

## 持久技能与变化技能

- **不过时的根基**：数据结构、算法、网络基础、操作系统原理（见 `../../computer-organization/`）——技术栈更替时这些仍可迁移。
- **必备工程技能**：云熟练度、容器化、基础设施即代码（Terraform / Pulumi）、可观测性（Prometheus / Grafana / ELK）。
- **愈发决定性的软技能**：与非技术干系人沟通、拆解复杂问题、在不确定性下做权衡、写清楚决策依据。

## 工程判断

趋势是输入而非指令。采用任何新实践前先问：它解决的是不是我们真实存在的问题？引入的复杂度是否被收益覆盖？能否回退？——这与架构权衡（`../architecture/architecture.md`）是同一种思维。

> 相关：规格驱动开发（AI 辅助开发的工程化范式）见 `../spec-driven/spec-driven.md`；软件工程总览见 `../software-engineering.md`；AI 应用工程化见 `../../ai/ai.md`；计算机学科总览见 `../../computer.md`。
