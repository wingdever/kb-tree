---
description: "Open-source books and tutorials for learning RAG engineering"
描述: "RAG 工程的开源图书与系统教程"
name: "RAG Learning Resources"
名称: "RAG 学习资源"
---

# RAG 学习资源

收「系统成书 + 可在线读 + 与本树节点有对应」的开源教程，零散代码片段不在此列。star 数只作量级参考。

## 中文系统教程

| 仓库 | 内容 | 在线 / 许可 |
|---|---|---|
| `datawhalechina/all-in-rag` | 《RAG 技术全栈指南》：数据加载 → 文本分块 → 嵌入/向量库 → 混合检索 → 查询构建/Text2SQL → 生成与评估 → 图 RAG 实战；约 10 章 + Extra | `datawhalechina.github.io/all-in-rag/`；README 明确 **CC BY-NC-SA 4.0**（第三方「无 license」的说法不准确） |
| RagGuide（仓库地址未核实） | 来源称 10 章从 RAG 基础到生产部署，含 LightRAG / GraphRAG、LangGraph、法律医疗案例与六套面试题库；技术栈 LangChain + LM Studio + ChromaDB | 来源称 Apache-2.0；**仓库地址未在来源中给出，使用前需自行核实** |

## 配套代码与英文书

| 仓库 | 对应内容 |
|---|---|
| `towardsai/ragbook-notebooks` | Towards AI《Building LLMs for Production》配套 notebook |
| `Nipi64310/RAG-Book` | 《大模型 RAG 实战》代码与资料汇总 |
| `tomasonjo/kg-rag` | 用 Neo4j 搭图谱的 GraphRAG 实践仓库 |
| `abhinav-kimothi/A-Simple-Guide-to-RAG` | 《A Simple Introduction to RAG》示例与插图源码 |

## 怎么配本树读


> 这类教程跨多个工具与框架（Milvus、Neo4j、LangChain 等），版本变动快；跟练时锁定仓库推荐的版本，不要把某个教程的 API 写法当通用规范。

## 阅读路线

书与树节点交替推进，每阶段先跑通再扩展，并有可验收产出。

| 阶段 | 读什么 | 交付物 |
|---|---|---|
| 1. 建立心智模型 | `all-in-rag` 第 1 章 + 配套代码 | 裸代码写一个四步 RAG：加载 → 分块 → 嵌入 → 检索 → 生成，不依赖框架 |
| 2. 管道部件 | 同教程第 2–3 章（数据、嵌入、向量库、Milvus） | 同一语料上对比两种分块策略与两种索引配置，记录 Recall@k |
| 3. 检索与查询 | 第 4 章（混合检索、查询构建、Text2SQL、查询重构） | 搭出 BM25 + 向量 + RRF + rerank 的流水线，说明每步为何需要 |
| 4. 评估与保障 | 第 6 章 + `towardsai/ragbook-notebooks` | 建一个 20 条问题的黄金集，跑 RAG Triad，定位失败 case |
| 5. 进阶二选一 | 任一进阶资料 | 同一批问题分别走向量 RAG、GraphRAG、Wiki 编译，写对比结论 |

主线：**先跑通最小管道 → 再逐部件优化并有指标 → 最后按场景选高级形态**。

## 一句话主线

**中文 RAG 开源教程以 `all-in-rag` 最系统；按「数据 → 索引 → 检索 → 生成 → 评估」的顺序对照本树节点读，比按仓库顺序读更能建立结构感。**

