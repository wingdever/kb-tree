---
description: "Ontology: formal domain semantics, TBox/ABox, OWL/RDF/SHACL, competency-question design and governance"
描述: "本体论：形式化领域语义、TBox/ABox、OWL/RDF/SHACL 与能力问题驱动设计"
name: "Ontology Engineering"
名称: "本体论与本体工程"
---

# 本体论（Ontology）

本体是对一个领域**概念、属性、关系与规则**的形式化定义——它区分知识图谱与单纯的图数据库，也是 Agent 的"业务地图"与跨调用的"意义承诺"。一句业内判断：**智能体无法学习它无法命名的东西**（Your AI agent can't learn what it can't name）。

本体一定是语义的表达，而不是数据库结构的定义——企业多个系统可能有不同的"客户表"，但语义层"客户"只有一个含义。

## 本体 vs Schema vs Taxonomy

| 概念 | 定义 | 例子 |
|---|---|---|
| **Taxonomy（分类法）** | 层级类别，"is-a kind of" 链接 | "Laptop narrower than Electronics"；产品类目、ICD 诊断树 |
| **Schema（模式）** | 存储结构：有哪些节点标签、关系类型、属性，适用哪些约束 | "every Order must have exactly one Customer"；唯一 ID、必填国家 |
| **Ontology（本体）** | 形式语义：类、带 domain/range 的关系、规则，让软件能检查一致性、推断新事实 | "if A owns >half of B, A controls B"；SUBSIDIARY_OF 可传递；Person 与 LegalEntity 互斥 |

Taxonomy 常是本体的组成部分。本体用 URI 标识、开放世界语义（OWL），schema 是封闭的存储结构。

## TBox 与 ABox

- **TBox（Terminology）**：术语层——类、属性、关系、约束（本体本身）。
- **ABox（Assertions）**：实例层——数据三元组（具体事实）。

TBox 治理 ABox，两者用不同工作流演进。生产实践中 TBox 放 RDF/OWL 文件版本化在 Git，ABox 在 Neo4j 等图库；用显式映射表（`:Employee → ex:Employee`）对齐，CI 检查新标签有 TBox 对应或记录在案的例外。

## 技术栈

| 标准 | 作用 |
|---|---|
| **RDF** | W3C 三元组（subject-predicate-object），主体与谓词是全局唯一 IRI，知识图谱的"线格式" |
| **RDFS** | 基础词汇：类、子类、属性、domain/range |
| **OWL** | 丰富逻辑：等价、互斥、基数、传递/逆属性，reasoner 可推断事实、检测矛盾；**开放世界**（缺失=未知，非假） |
| **SHACL** | 对 RDF 数据按 shape 校验（**封闭世界**），报违规——补 OWL 不擅长的"每个客户必须有邮箱"检查 |
| **SKOS** | 分类法/受控词表：preferred label、broader/narrower，适合搜索与内容管理 |
| **SPARQL** | RDF 查询语言，能力问题落地为 SPARQL 测试 |

**经验**：RDFS + SHACL 覆盖多数企业 KG；只有需要自动推理时才上 OWL。OWL 管意义（开放世界），SHACL 管数据质量（封闭世界），两者并用。先用 RDFS/SHACL 起步，别一上来就 OWL 推理器和 500 类层级。

**属性图 vs RDF**：需要形式语义、SHACL 标准校验、跨工具可移植 → RDF/OWL；遍历速度与开发者熟悉度更重要 → 属性图。很多团队用中立语言（如 LinkML）建模一次，生成 OWL、SHACL、JSON Schema、SQL，保持选择可逆。复用 FIBO、schema.org、SNOMED 等已有本体，别从零造词。

## 能力问题驱动设计（Competency Questions）

能力问题是本体必须能回答的自然语言问题（"本季度有未结续约的活跃客户有哪些？"）。它**既是设计规格，也是验收测试**，是判断本体是否完整的标准方法。

设计流程：

1. **范围**：一个领域、一个 agent、20–40 个能力问题就是可控项目；**别在任何 agent 使用前建模全公司**——那是会卡死的做法。
2. **复用与枚举术语**：先查已有本体，再列术语；LLM 几分钟能从语料起草术语表，但**起草便宜、判断昂贵**——每个变更要领域 owner 审核。
3. **定义类与层级**：top-down / bottom-up / middle-out，顶层锚定到上层本体而非自造根节点。
4. **定义属性**：对象属性 vs 数据类型属性，domain/range 只在确实成立时声明——错误的 domain 断言会悄悄重新分类实例而非拒绝它们（开放世界的直接后果）。
5. **约束与实例**：基数、取值限制；OWL 管意义、SHACL 管校验；实例由 ETL 与 LLM 抽取批量灌入，自动化校验而非肉眼看。

**把能力问题变成可执行测试**：每个问题映射为一个或多个 SPARQL 查询——验证查询（ASK 期望 true，问"能不能答"）+ 证伪查询（ASK 期望 false，问"是否允许了不该允许的答案"）。查询与本体放同一仓库（一问题一文件），刻意构造含反例的 fixture 数据（如证书过期的执行者），每次变更自动跑。**从未执行过的能力问题只是愿望，不是需求**。

循环的演进：2001 年是"建模→看→改"，2026 年是"建模→跑测试→读失败→改"。

## LLM 与本体

- **LLM 起草**：可快速提出类与映射，但不能决定业务含义。2026 企业 KG 本体构建研究报 fuzzy match F1 0.724（Data 域），在范围界定与层级上有局限；ESWC 2025 研究（arXiv 2503.05388）发现元认知提示 + 设计模式能让前沿模型在 10 个本体 100 个能力问题上超过新手本体工程师——**起草便宜，判断不便宜**。
- **本体驱动 Agent**：共享本体取代散落的局部信念状态，消除多 Agent 协调漂移；typed graph tool call（`get_contract_parties(contract_id)` 返回符合本体 schema 的结构化对象）比自由文本检索更精确、可审计。本体约束在领域逻辑层阻断无效推理路径。
- **Agent 提议的图变更必须人工审核**——无审核更新共享本体会导致全舰队漂移，比单 Agent 幻觉更糟。
- **企业本体 vs 语义层**：语义层定义指标与维度让数字算得一致（回答"多少收入"），本体定义数字背后的实体、关系、规则与动作（回答"哪个客户、哪份合同、Agent 下一步能做什么"）。Agent 两者都需要。

## 本体漂移与动态演进

静态本体在业务转型时会**本体漂移（Ontology Drift）**——过时的分类体系让新知识被塞进"垃圾桶"实体，造成语义丢失。2026 共识：Agent 记忆管理问题与本体动态演进同源，系统需具备**类型发现、异常检测、实体消歧合并、无效分类剪枝**能力。

Evontree 等框架少样本自适应演进：挖掘 LLM 内部领域概念划分 → 引入人类专家提炼的少量高质量"本体规则"校验抽取一致性 → 自蒸馏精准 QA 对微调注回参数。

## 企业治理

- **所有权**：业务域 owner 拥有每个概念的含义，小型建模团队拥有结构/标准/发布流程，数据工程拥有源系统映射。没有具名 owner，定义会漂移、Agent 给冲突答案、无人有权裁决。
- **版本化**：版本化 namespace URI、`owl:deprecated`、替换指针、每环境 pin 版本；模块化（product.owl、supplier.owl）让团队独立编辑。
- **RFC 工作流**：提案文档含能力问题、拟加术语、对现有 ABox 映射的影响、steward 审核、merge 前 CI SPARQL 回归。
- **健康检查**：未使用类数、按源分的 SHACL 违规率、RFC 周期、能力测试通过率、ABox 覆盖率。活跃企业 KG 至少季度复审。
- **自主而非租用**：本体承载企业运作方式，是制度性知识；用 OWL/SHACL/SKOS/LinkML 等开放格式保存在自己可控基础设施上，换平台不必重建。

## 何时过度工程

单团队、无跨系统共享、无合规推理需求——标签约定可能就够。本体是活工件，"完成"指当前范围被证明覆盖，不是彻底完备。

