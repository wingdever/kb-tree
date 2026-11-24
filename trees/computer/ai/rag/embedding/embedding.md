---
description: "Knowledge tree for embedding model selection and training"
描述: "嵌入模型知识树导航"
name: "Embedding Models"
名称: "嵌入模型"
---

# 嵌入模型

> 嵌入模型是向量检索的**质量天花板**——换索引配置很少能让召回提升超过 2–3 个百分点，而换模型可以。别选错。

本主题已拆成 3 个子知识点目录，每个自成一个目录、目录内放同名 md。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `models/` | 商业/开源模型对比、选择决策树、input_type 不对称陷阱、升级时机 |
| `training/` | 训练目标（对比学习/InfoNCE）、三阶段范式、困难负例挖掘、MTEB 与失败模式 |
| `matryoshka/` | MRL 原理、降维操作、存储账、与量化的配合 |

## 阅读顺序

先看 `models/` 选定模型；想理解为什么这样选、模型质量从何而来读 `training/`；关心向量库成本读 `matryoshka/`。

> 相关：切块见 `../chunking/`；向量库存储见 `../vdb/`；评估见 `../eval/`。
