---
description: "Tracing, golden signals, cost and OpenTelemetry for agents"
描述: "Agent 的追踪、黄金信号、成本与 OpenTelemetry 可观测性"
name: "Production Observability"
名称: "生产可观测性"
---

# A8 生产可观测性

> 看不见内部的 Agent，就无法运维。可观测性不是可选工具，而是整个系统的控制面板。

市场已分化为追踪层（Langfuse、Helicone）与评估层（Braintrust、Phoenix），没有单一工具主导；OpenTelemetry 标准化正推动厂商中立的追踪。

## 三大集成方式

| 方式 | 代表 | 做法 | 适用 |
|---|---|---|---|
| **代理 / 网关式** | Helicone、Portkey | `App → Proxy Gateway → LLM Provider`，一行接入 | 快速部署、成本追踪 |
| **SDK / 装饰器式** | Langfuse、W&B Weave | `@observe()` 装饰函数 | 通用、灵活 |
| **OpenTelemetry 原生** | Phoenix、OpenLLMetry | 厂商中立，路由到任意后端 | 已有 OTel 体系、需换后端 |

## 平台对比（2026）

| 平台 | 类型 | 许可 | 免费层 | 强项 |
|---|---|---|---|---|
| **Langfuse** | 追踪 + 评估 + 提示管理 + AI 网关 | MIT | 50k observations/月 | 开源、可自托管、OTel 原生、框架无关、自托管最便宜 |
| **LangSmith** | LangChain 原生全套 | 商业 | 5k traces/月、1 席、14 天 | 与 LangChain/LangGraph 集成最紧、轨迹可视化、重放 |
| **Phoenix (Arize)** | OTel 原生评估 + 追踪 | Elastic License 2.0 | 自托管无事件上限 | 评估最成熟、OpenTelemetry 支持 |
| **Braintrust** | CI/CD 评估实验管理 | 商业 | 1M spans、$249/月档 | 数据集与实验管理、回归测试 |
| **Helicone** | 网关/代理 | 开源 | 有 | 一行接入、成本追踪 |
| **Datadog / New Relic / Honeycomb / Grafana Cloud** | 企业可观测平台 | 商业 | — | 与既有服务遥测同屏；Datadog 经 OTLP 接 GenAI span |

选型经验：Langfuse 自托管最便宜、最开放；LangSmith 与 LangChain 栈最紧；Arize 评估最成熟；Helicone 简单代理接入最强。深度可观测文化的团队，规模超过约每月百万次运行后，OTel + ClickHouse + Grafana 自建最具成本效益。成本示例：每月百万次运行、每次 12 span × 2KB、30 天留存 ≈ 压缩后 30GB/月，专家厂商按事件计费可达数千美元，自建 OTel+ClickHouse 接近个位数美元。

## 必须记录的字段

- Run id、parent run id、模型及版本、工具名与参数哈希、输出哈希。
- 延迟、token 用量、成本、结果、用户/租户标识。
- **用 OpenTelemetry GenAI 语义约定作为 schema；对载荷做哈希而非记录原文**。
- 多步 Agent：每次 LLM 调用一个 span、每次工具调用一个 span，挂在 run span 下。

生产环境在就"存什么、存哪里、存多久、谁能读"达成一致前，**不要开启内容捕获**。

## 黄金信号

传统 Golden Signals：延迟、流量、错误、饱和度。Agent 再加两项：

- **质量**：评估通过率（eval pass rate）
- **成本**：每运行成本 / 每成功任务成本

具体指标：

- **延迟**：端到端延迟、TTFT（首 token 时间）、P95/P99 尾延迟（平均值会骗人）。
- **流量**：每分钟运行数。
- **错误**：错误率、工具错误率、按 SLO 的延迟告警。
- **质量**：幻觉率（业界均值约 8.2%，最佳系统 0.7~1.3%）；通过率时间序列。
- **成本**：按用户/功能/会话追踪；对齐结果——每成功任务成本；按小时消费速率告警（循环 Agent 一下午能烧光预算，不要只看月度总额）。

## 给追踪附加质量分数

延迟和成本容易，判断 Agent 是否**正确**更难。常规做法：给产生答案的 trace 附加分数。

- **用户反馈**：赞/踩、"这没帮上忙"，按 trace ID 记录。
- **自动检查**：是否调对工具、返回合法 JSON、引用来源、未超步数限制。
- **模型打分评估**：另一个模型对样本流量打相关性、对检索文档忠实度、语气分。GenAI 语义约定已有 `gen_ai.evaluation.result` 事件；Langfuse、Phoenix 有自己的分数/标注 API。

按提示词版本和模型跟踪分数，让"让答案变差"的改动和"让答案变慢"的改动一样醒目。

## 质量漂移检测

抽样一部分运行，通过评估套件重放；把通过率作为时间序列跟踪；低于阈值告警。常见原因：模型、提示词、上游 API 变更。

## OpenTelemetry 实操起点

1. 用内置 OTel 支持的框架，或加插桩库；设 `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`。
2. 把 trace 经 **OpenTelemetry Collector** 路由——可在一处换后端、采样、丢弃或脱敏属性。
3. 通过 Collector 发往多个目的地：全部发到主可观测平台（Agent 延迟与错误和它调用的服务同屏），抽样带内容的副本发到 LLM 工具（给改提示词的人用）。
4. 加自己的属性：feature、tenant、prompt version。
5. 建四个面板：每分钟运行数与错误、延迟与 TTFT、每小时 token 与估算成本、每次运行的模型/工具调用数。
6. 为错误率、SLO 延迟、消费速率、超步数运行设告警。
7. 加反馈和小样本评估，每周复盘分数最差的 trace。

注意：OpenInference（Arize）是广泛使用的并行约定，属性名不同；混用库时要确认面板和查询覆盖两套名字。

## 本周可做的三件事

1. 每次运行一条带 OpenTelemetry GenAI 属性的 trace——不完美的追踪也好过没有追踪。
2. 对带标签集合做质量抽样-重放，从 50 个例子起步。
3. 对最重要的 SLO（端到端延迟或通过率）设消费速率告警。

## 工具栈分层（Langfuse 视角）

| 层 | 用途 |
|---|---|
| 检索与向量存储 | 知识层：文档库、嵌入、重排器、新鲜度管道 |
| 记忆框架 | 跨会话持久化、短期→长期流转 |
| 编排 | 运行中的工具调用、压缩、预算控制 |

调用量大的团队：可把全部遥测送主平台，抽样副本送 LLM 工具。Langfuse 网关位于应用与提供者之间，Rust 实现、低延迟，换 base URL 和 API key 即可无 SDK 追踪。

## 参考资料

- OpenTelemetry GenAI 语义约定：https://opentelemetry.io/docs/specs/semconv/gen-ai/
- Langfuse 文档：https://langfuse.com/docs
- LangSmith 文档：https://docs.smith.langchain.com
- Arize Phoenix 仓库：https://github.com/Arize-ai/phoenix
