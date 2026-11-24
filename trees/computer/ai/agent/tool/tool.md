---
description: "Agent tool design: contracts, schemas, permissions, idempotency, mediation, registry and testing"
描述: "Agent 工具设计：契约、schema、权限、幂等、中介层、注册表与测试"
name: "Agent Tool Design"
名称: "Agent 工具设计"
---

# Agent 工具设计

工具是 Agent 影响世界的唯一途径：**你设计的工具，决定了 Agent 有多有用，以及一次错误或操纵能造成多大破坏**。API 层的字段规范见 `../../api/`，本页讲工程设计。

## 工具契约（Tool Contract）

每个工具是一份"小型受治理的应用接口"：单一目的、显式输入 schema、明确权限边界、可预测的错误响应、审计轨迹。避免给 Agent 一个"什么都能跑"的宽泛能力——多个聚焦工具提供更好控制。

契约字段：名称、模型能理解的目的段落、输入 schema（类型/约束/示例）、输出 schema、副作用说明、后果级别（read / reversible write / irreversible or external）、所需权限、失败模式。先写**工具注册表**：每个工具记录 owner、目的、访问数据、影响系统、预期用户、操作限制。

**ACI（Agent-Computer Interface）原则**：像给开发者写 docstring 一样写工具描述。

## Schema 设计

- 模型看到**紧致无歧义的 schema** 才成功。宽松的自由文本字段诱发幻觉与畸形载荷。
- 偏好小而扁平的 schema，除非层级确有必要。
- 货币、数量、单位显式表示，避免静默换算。
- 写操作加 `idempotency_key`（幂等）、`trace_id`（关联）；返回结构化结果含 `status`、`resource_ids`、版本号（并发控制）。
- 少而精：从最小高信号工具集起步，合并重叠动作、淘汰少用工具。工具膨胀增加混淆与错误率。
- 名字即 affordance：用精确、去歧义的动词名词，避免跨工具同义词。描述一句话讲清前提与效果，把关键约束写在显眼处。
- 2–5 个真实示例胜过一长段描述；别用玩具数据训练模型错误调用。

## 权限与爆炸半径

- **最小权限 + 显式 scope**：每个工具只给完成声明目的所需最小访问，读写分离，低影响写与不可逆动作分离。
- 权限给调用的用户/服务/工作流，**不只是给模型**。服务端做 tenant/identity/ownership/role/resource scope 检查。
- 提示词里"只访问此客户记录"是上下文，不能替代访问控制。凭据不进提示词与工具参数。
- 策略在代码里（中介层），不在提示词里。ABAC/RBAC 在工具边界强制。
- 高风险工具（资金、批量更新、对外发送）：HITL 审批门，审批 payload 可读可重放。
- **dry-run 模式**：`dry_run` 参数校验并返回计划而不执行副作用。
- 审计：记录 who/what/when/why，含提示词、选中工具、参数（PII 最小化）、结果。

## 幂等与执行安全

- 模型可能在超时后重复请求，应用可能重试不确定结果。任何 create/send/charge/publish/update 工具都要幂等策略：接受唯一 operation key，存结果，重复时返回原结果。
- 非幂等动作用两阶段：先创建 proposed action，再显式确认/审批后执行。
- 每个外部调用设超时；接受 caller 提供的 deadline，超限干净中止。
- 只重试可能临时的错误（网络），用有上限的指数退避 + 抖动；不重试校验/权限/业务规则拒绝。
- 多步副作用用事务或补偿动作（Saga，如 `cancel_invoice_draft`）。
- 断路器：错误率或延迟超阈值就跳闸，快速失败让 Agent 换方案。
- 沙箱执行代码/文件/网络；出口白名单；写工具幂等；超时；绝不把原始凭据暴露给模型。

## 中介层（Mediation Layer）

所有工具调用经过一个层：schema 校验 → 权限检查 → 策略限制（金额上限、速率、允许目标）→ 后果分类并路由门控动作去审批 → 通过适配器执行（超时）→ 全程日志。适配器把系统怪癖与工具契约隔离。

## 结构化结果与错误

- 返回符合 schema 的结果，按上下文定量（大结果给带引用的摘要而非全量）。
- "先看再截断"：截断的结果看着完整会误导模型；摘要显式表达压缩（"显示 247 条中的 5 条，更多请用 offset=5 再调"）。
- 错误必须结构化且有信息量：什么失败、是否可重试、Agent 可以做什么。区分无效输入/未授权/依赖不可用/冲突更新/速率限制/未知结果。**失败 ≠ 空**：返回 null 或空数组会让模型以为"没结果"而非"出错了"。
- 人类可读值优先（即使数据库用整数码，在工具边界转换）。
- 结果内容对注入而言是不可信输入。

## 工具注册表模式

集中定义，可组合，schema 与实现共置。`ToolRegistry`：`register(fn, schema, requires_auth)` 作装饰器、`get_schemas(names)` 返回注入提示的 schema、`execute(name, params, context)` 按上下文执行。支持**动态工具加载**——只注入与当前任务相关的工具，而非全集（见 `../context/` 的成本讨论）。

上架即校验（fail-closed）：缺契约、名字对不上、描述空/过短、无 examples 都在注册阶段失败；生产/CI 开 `require_contract` 模式。

## 常见反模式

- **God Tool**：一个工具通过 `action` 参数做所有事——难安全使用、难测试、逼模型理解内部 API。
- **Silent Failure**：失败返回 null/空数组。
- **Ambiguous Schema**：参数不写格式、有效值、何时省略可选参数，逼模型猜且猜得不一致。
- **Undifferentiated Toolkit**：多个工具能力重叠、描述无区分 → 随机选择。
- **Non-Idempotent Side Effect**：写工具无去重 → 重试产生双倍副作用（发两封邮件、下两次单）。
- **Raw Code Return**：返回 HTTP 状态码、整数枚举、数据库码，模型得猜 `status: 3` 是什么。

## 测试

工具是 Agent 栈里最可测的部分（输入输出确定性）。三层：

1. **单元测试**：happy path、空结果、每类错误、幂等（同 key 调两次只一次副作用）、schema 合法性。
2. **对抗测试**：通过参数注入、通过结果注入、越界查询、批量更新、数据外泄尝试。
3. **轨迹评估**：模拟环境里验证工具选择正确、参数有效、门控遵守、错误恢复。
4. **Shadow mode / 金丝雀**：先 observe-only 对比人类/旧行为，再小流量灰度、自动回滚。

> 相关：API 字段规范见 `../../api/common/`；工具在 Agent 循环里的调用见 `../../api/loop/`；ACI 三原则见 `../patterns/aci/`；提示注入防御见 `../safety/`。
