---
description: "Agent handoff payloads, in-framework messaging and A2A communication"
描述: "Agent 交接三要素、框架内消息与跨框架 A2A 通信"
name: "Handoff and Communication"
名称: "交接与通信"
---

# 交接与通信（Handoff & Communication）

多智能体之间如何传递控制权与信息，是架构的血管。要分清两层：**框架内通信**与**跨框架/厂商通信**。

## 交接携带什么

一次 handoff 通常携带三样东西：

1. **中间结果本身**：下一个 Agent 继续工作所需的实际输出（检索到的记录、草稿段落）。
2. **置信度分数**：发送方对自己输出的确定程度，帮助编排器决定继续下发还是打回重做。
3. **人工复核标记**：遇到超出范围的东西时，触发验证 Agent 或人工介入。

## 框架内通信

- **消息传递 + 共享图状态**（LangGraph）：Agent 通过图的共享状态交换信息。
- **显式 handoff**（OpenAI Agents SDK）：把对话历史转给另一个 Agent——被委派的 Agent 接收对话历史并接管，成为"当前活跃 Agent"直到该轮结束。
- **共享完整轨迹**：Cognition 的实践规则："共享上下文，共享完整 Agent 轨迹，而不只是单条消息"——丢掉轨迹的交接丢失了隐含决策。

## 跨框架/厂商通信：A2A 协议

Agent 由不同团队、框架或公司构建时，跨边界那一跳必须落在标准信封上，不要自造消息格式——否则每接一个伙伴写一次适配器，鉴权、能力发现与长任务状态也没法复用。

选型看三件事：对方是否用签名 Agent Card 做能力发现，是否支持 task 生命周期与状态回传，鉴权是否按 OAuth 资源服务器隔离。交接质量仍靠自己这一侧：验收标准写进任务描述，结果按可校验的 Artifact 收，失败按 task 状态收口。

## 共享状态与黑板模式

Agent 也可以通过读写共享工作区（黑板）而非直接消息传递来协作：

- 解耦好——Agent 不需要彼此知道对方存在。
- 代价是状态管理复杂，需要版本化状态、乐观并发、显式 ACK 来避免竞态与状态漂移。
- 黑板是 1980 年代 AI 模式的复兴，2026 年在信息发现任务上有 13–57% 的相对提升报告，但工具不成熟，属新兴方向。

## 通信的可靠性

- 消息丢失：对关键消息要求显式 ACK（重试直到确认）。
- 消息被误解：要求结构化格式，不要自由文本。
- 信息过载：监控 token 数，截断或摘要。
- 上下文过时：给所有上下文打时间戳。
- 竞态：给 handoff 编号排序；共享资源加锁或排队。

## 参考资料

- A2A 协议规范：https://a2a-protocol.org/latest/specification/
- AutoGen 论文（消息传递与交接）：https://arxiv.org/abs/2308.08155
- Anthropic 多 Agent 研究系统（委派与上下文隔离）：https://www.anthropic.com/engineering/multi-agent-research-system
