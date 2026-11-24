---
description: "Text-to-SQL: schema linking, validation, benchmarks, failure modes and security guardrails"
描述: "Text-to-SQL：Schema 链接、校验、基准、失败模式与安全护栏"
name: "Text-to-SQL"
名称: "自然语言转 SQL"
---

# Text-to-SQL（自然语言转 SQL）

Text-to-SQL 让用户用自然语言查询结构化数据——LLM 针对数据库 schema 生成 SQL。它在管理良好的领域做内部分析已进入生产可用，但成败几乎完全取决于**上下文工程**，而非模型本身：干净基准上问题近乎解决（BIRD 约 83%），而未经准备的企业 schema 实际成功率仅 **10–30%**——这就是"企业悬崖"。

一个 2026 的重要转向：更强的模式是 **text-to-semantic 而非 text-to-SQL**——Agent 输出结构化请求（measure、dimension、filter、time grain）给语义层，由层确定性地编译出安全 SQL。本页讲生成技术本身，二者互补。

## 五阶段管线

现代 NL2SQL 不是把 schema 一股脑塞进提示词，而是多阶段管线——理解管线是诊断失败的前提：

1. **Schema 检索与链接（Schema Linking）**：找出与问题相关的表和列。小库 trivial，企业仓库数学上无法暴力（LinkedIn 数百万张表）。LinkedIn SQL Bot 用漏斗：按访问热度过滤 → 向量相似检索 → LLM 重排到 7 张最相关表。Uber QueryGPT 用"workspace"按领域（Mobility/Ads）策展表与 SQL 样本，意图分类 Agent 先路由。**Schema linking 是单一最大杠杆**。
2. **上下文组装**：高信号载荷 = 表/列定义 + 已验证的问-SQL 对（few-shot）+ 业务规则与指标定义 + 格式约束。Lloyds Banking Group 给 schema 加同义词、缩写、验证过的示例查询，exact match 从 80% 升到 86.1%——**单一调整胜过换更新模型**。
3. **SQL 生成**：注意方言（多在 SQLite 基准训练，迁到 PostgreSQL/BigQuery/Snowflake  measurable 下降）与非确定性（同提示两次结果不同；Salesforce Horizon 每提示生成 10 个候选、按相似度选最一致的）。
4. **校验**：语法（EXPLAIN/PARSE）、schema（引用的表列真实存在）、自纠正（失败把错误回灌重试）。LinkedIn SQL Bot 首次失败会回退去拉完全不同的表。
5. **执行与结果**：原始表、图表或自然语言摘要（摘要是感知延迟的大头，流式化可隐藏 SQL 生成的往返）。

Agentic 循环优于一次性翻译：schema 探索 → 对活库执行 → 从执行反馈自纠正，**第一次纠正增益最大，之后递减**。

## Schema 增强（不是原始 DDL）

把原始 `CREATE TABLE` 换成带自然语言注释的增强 schema：每列加用途描述、外键指向、取值含义（如 `ship_region -- 交付地理区域 EMEA/AMER/APAC`）。这些注释是引导模型的提示 token，不是装饰。大 schema 下对 schema 描述做检索（"最小可行 schema"），同时对分类列给样本值、标注已知数据陷阱。

跨表上下文（把邻近表的 schema 纳入打分）在多表同名列时降歧义 30–40%。

## 基准与现实差距

| 基准 | 测什么 | 最好成绩（2026-11） |
|---|---|---|
| Spider 1.0 (2018) | 小而干净库上的单查询 | >85%，基本解决 |
| BIRD (2023) | 更脏更大库 + 外部知识 + VES | 83.40%（AT&T AskData）；人类专家上限约 93% |
| Spider 2.0 (2024) | 真实企业工作流，~800–1000 列库，多步 | code-agent 基线 17.0%（o1-preview 17.1%），远低于 Spider 1.0 的 91.2% |
| BIRD-Interact | 歧义问题 | 前沿模型单独用约 33% |
| BIRD-Ent / Spider-Ent | 企业 schema | 39.1% / 60.5% |

**基准准确率常高估生产 20–40 个百分点**（schema 更干净、问题歧义更少）。GPT-4 Turbo 在 BIRD 上无增强约 60%，加 schema linking + few-shot + 执行反馈后升到约 76%。

评估用**执行准确率（execution accuracy）而非字符串相似度**：两条返回相同行的 SQL 就是同一答案，EM 因别名/join 顺序不同会冤枉正确答案（常比执行准确率低 20–30%）。同时分别跟踪 SQL 有效率和执行准确率——模型可达 100% 有效率但只有 60% 准确率，用户感受到的只有后者。

## 失败模式分类（"跑了"不等于"对了"）

| 错误类 | 症状 | 修复 |
|---|---|---|
| 错误 join 路径 | 重复行、SUM 膨胀（fan-out：订单×3 明细×2 支付 = 6 行） | FK 提示 + 显式 join 链 few-shot；声明关系基数、批准 join 路径；每次 join 前后测行数 |
| 幻觉列 | "column X does not exist" | 对活 catalog 校验标识符；裁剪 schema 块 |
| 错误聚合粒度 | 平均的平均、缺 GROUP BY | 标注 grain 的 few-shot 示例 |
| 指标歧义 | revenue 指 gross/net/booked/recognized 中哪个？ | 先查受治理指标定义，再生成 SQL |
| 日期误判 | "上季度"解析到训练时代 | 注入当前日期、时区、财年规则 |
| 静默空结果 | 明明有数据却返回 0 行 | 零行重试 + 重过滤提示 |
| 越界 | 查询碰到非白名单表 | allow-list 拒绝，再问澄清 |
| 方言不兼容 | PostgreSQL/BigQuery 函数报错 | 目标方言的 EXPLAIN dry-run |

最危险的是**看似合理的错误数字**：查询无错运行、结果看着对，但错误 join 或缺过滤悄悄扭曲——验证 SQL 的人若只看答案不看 SQL，就会把错误带上董事会。

## 提高准确率的工程手段（有证据）

- **DIN-SQL**（schema-link → 分类 → 生成 → 自纠正）：Spider 85.3%，比朴素 few-shot 高约 10 分。
- **RAG over schema + values**：向量 schema 检索 +3.85%（BIRD）/+2.67%（Spider）；Vanna 打包 DDL/文档/SQL 检索。
- **DAIL-SQL**（遮蔽问题 + 查询相似度选例）：Spider 86.6%，第一。
- **自纠正/重试**：第一次纠正增益最大（+4 pts 量级），之后递减；执行反馈修复 40–60% 初始失败。
- **执行引导解码**：中途剪枝错误部分程序，WikiSQL 83.8%。
- **候选生成 + 排序**（CHASE-SQL 多策略候选 + 成对选择器）：BIRD 73.0%。
- **CoT / SQL-of-Thought**：复杂多表查询显式推理降逻辑错误约 40%；查询分解对嵌套/相关子查询尤有效。
- **执行准确率 RL**（ExCoT 只用执行准确率作 DPO 信号，无需奖励模型）。

## 安全护栏（纵深防御）

最危险的误判是"提示词里写只读就够了"——**提示是建议，数据库角色 + AST 级校验才是强制**（只读 role 对策展视图的 SELECT 已被实践绕过，如某 Postgres MCP server）。

- 数据库层强制只读：专用 role 只 SELECT 策展视图，读副本让写入不可能。
- 行级安全在数据库层、传递用户身份实现，而非让 LLM 在 WHERE 里请求。
- 把数据库内容和 schema 注释当作**不可信输入**——检索到的行可能带来提示注入。
- 执行前：EXPLAIN/dry-run、行数限制、超时；执行后：合理性检查、向用户展示生成的 SQL 与解释。
- 歧义时反问用户而非猜测——一行澄清问题比一个错误数字便宜且可信。**注入当前日期/时区/财年**——这一个遗漏比其它所有原因合计造成更多日期错误。

## 成本与延迟

输入 token 主导成本：schema 块通常是每请求最大组件且每轮重发，所以**检索式裁剪既是准确率手段也是成本手段**。结构化输出（JSON schema）去掉 markdown 围栏与解析代码。积极缓存：规范化问题（小写、去标点停用词）哈希后缓存 SQL，仪表盘重复问同样二十个问题，60–80% 命中率现实；结果用短 TTL 单独缓存。按难度路由：小模型判"能否回答"+摘要，中模型写 SQL，失败修复后才升级前沿模型。

## 工具生态

- **Vanna**（MIT）：对问-SQL 对做 RAG，2.0 起 agent-based，带用户身份/审计；领域库上 50–100 个示例后达 80–90%。
- **Wren AI**：开源 GenBI，自带语义层，适合受治理的企业 BI。
- **Snowflake Cortex Analyst**：维护良好的 YAML 语义模型下 85–90%（DABStep Hard 89.9%）。
- **Databricks Genie**：借 Unity Catalog 上下文，企业查询 90%。
- **LangChain / MAC-SQL / MCP DB 工具**：工具箱抽象、多 Agent 协作、直连数据库的 MCP server（Google MCP Toolbox for Databases 等）。

Vanna 2.0 适合嵌入式开发工具，Wren AI 适合受治理企业 BI——解决不同问题，不是同一定价档。

