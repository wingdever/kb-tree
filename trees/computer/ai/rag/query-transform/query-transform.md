---
description: "Query transformation for RAG: HyDE, multi-query, step-back, decomposition and routed rewriting"
描述: "RAG 查询变换：HyDE、多路查询、Step-back、分解与路由式改写"
name: "Query Transformation"
名称: "查询变换"
---

# 查询变换（Query Transformation）

查询变换是 RAG 管道中**检索前**的阶段：把用户的原始问题重写、扩展、抽象或分解，再跑向量搜索——让检索器匹配"含义"而非"原始措辞"。也叫 query rewriting / query expansion / pre-retrieval enhancement。

RAG 系统的质量取决于中间那一步搜索。用户问题含糊、用词与文档不同、或是多跳问题时，向量搜索返回弱匹配，模型只能在稀薄上下文上作答——查询变换正是解药。

## 四大技术与对应失败模式

| 技术 | 做法 | 修复的失败模式 | 避免用于 |
|---|---|---|---|
| **HyDE**（假设文档嵌入） | 先让模型起草一个"假答案"，用它的嵌入而非问题去检索 | 短查询、口语 vs 正式文档的词汇鸿沟 | 精确事实查询、LLM 不了解的领域、时间敏感问题 |
| **Multi-Query**（多路查询） | 生成 3–5 个改写版本，各自检索后合并 | 措辞单一、表述分散 | 严格延迟预算 |
| **Step-back**（后退提示） | 先抽象出更宏观的问题检索背景概念，再钻取细节 | 规则+案例类问题（先找 governing rule） | 纯事实查找 |
| **Decomposition**（分解） | 把复合多跳问题拆成子查询，分别检索再融合 | 复合问题、多跳 | 原子问题 |

每种技术只修一种失败——**按生产日志里反复出现的失败模式选技术，而非挑"最好"的那个**。

## 成本与风险

每次改写都付三项结构性成本：**一次额外 LLM 调用**、**漂移**（改写收窄了本想扩展的范围）、**幻觉内容**（用编造的文本给检索接地）。HyDE 在检索调优模型出现后优势缩小且依赖语料——正式参考语料与对话式查询仍有 benefit，精确匹配反而有害。**默认从 multi-query + RRF 起步**（约 20 行、便宜、最可靠的单点收益），HyDE/step-back/decomposition 放到路由后面，各自用自有 recall 数字证明值得。

## 路由：生产实践的主流

生产已从"固定改写一步"转向 **router 逐问题决定**：是否变换、用哪种技术。复合问题需要分解 + 路由而非单次改写；RAG-Fusion 把分解后的查询结果用 RRF 融合回一个排序列表。

- 路由种类：pass-through（直通，默认）、hyde、multi-query、step-back、decomposition、graphrag-global。
- 用 100–300 条真实问题（各标注应检索的 chunk id）建标注集，报告**每种路由的 recall@k**——HyDE 可能大幅提升含糊问题却轻微伤害查找，平均值会掩盖两者。
- 路由默认 pass-through，只为赢回 recall 且延迟可接受的类型开变换。

## 与重排 / 上下文检索的区别

三者常被混为一谈，但调试方向完全不同：

- **查询变换**作用于检索**前**，通过改写问题扩大"被找到"的范围。
- **重排**作用于检索**后**，重排已返回的候选。
- 变换的问题表现为"文档根本没被检索到"；重排的问题表现为"对了但排得太后"。强管道两者都做：改写+融合提高召回，重排融合列表提高精度。

## 工程要点

- 从第一天起**同时记录原始 query 与改写后的 query**（或 queries）——检索开始返回无关结果时，才能判断是模型编造了误导改写，还是嵌入相似度本身就是瓶颈，事后无法重建。
- 改写调用要**无工具**、把输出当数据、绝不执行它产生的东西（用户文本会流入改写提示）。
- 防约束漂移：每份提示保留"保留版本号/日期/产品名"的指令，并加几条 eval case 检查。
- **原始 query 始终参与检索**（multi-query 的 `include_original=True`）——原始往往命中最好，变体是补充。
- 按 chunk_id 去重，否则 5 变体 × top10 = 50 块重复塞给模型。
- 结构化输出（JSON 字符串数组）优于按行切分——模型一旦给答案编号就崩。
- 改写用小模型（gpt-5-mini、Claude Haiku、自托管 8B），延迟用户可感；改写与原始搜索**并行**，改写超时就用原始结果——渐进增强，绝不硬依赖。按归一化 query 缓存改写，文档/客服流量重复度高，缓存把常见 query 变成零附加延迟。

## 框架支持

LangChain `MultiQueryRetriever` 从单问题生成多个变体并返回去重并集；LlamaIndex `HyDEQueryTransform` 配 `TransformQueryEngine` 包裹任意 retriever 透明应用变换。

## 参考资料

- Precise Zero-Shot Dense Retrieval without Relevance Labels（HyDE）：https://arxiv.org/abs/2212.10496
- RAG-Fusion: a New Take on Retrieval-Augmented Generation：https://arxiv.org/abs/2402.03367
