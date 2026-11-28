---
description: "Fixed-size, sentence, recursive and structure-aware chunking"
描述: "固定大小、句子、递归字符与文档结构感知切块法"
name: "Basic Chunking Methods"
名称: "基础切块法"
---

# 基础切块法

切块是 RAG 管道中最容易"静默失败"的环节——它决定的检索单元，对答案质量的影响超过几乎任何其他参数。多数团队选一个默认配置就再也不回头看。

核心权衡：**小块检索精确但缺上下文；大块保留上下文但匹配不准**。没有通用最佳块大小。

## 方法对照

| 方法 | 怎么切 | 检索精度 | 上下文质量 | 索引成本 |
|---|---|---|---|---|
| 固定大小（token 数） | 每 N token | 中 | 中 | 极低 |
| 固定大小 + overlap | 每 N token，滑动 M | 中~高 | 中 | 极低 |
| 句子分割 | 句子边界 | 高 | 低（块太小） | 低 |
| 递归字符分割 | 分隔符层级 | 中~高 | 中 | 低 |
| 文档结构感知 | 标题、章节、表格 | 高（结构化文档） | 很高 | 低~中 |

## 固定大小 + overlap

512 token 块 + 10% overlap（51 token）是经典起点。易实现、大小一致，但对语义边界盲目——讲合同截止日的句子可能跨两个块，两边都丢含义。适合快速原型、高度同质的纯文本。

## 句子分割

按句子边界切。精度高但块太小、上下文差，适合转录稿、叙述性文本。

## 递归字符分割

按段落→换行→空格的层级切。良好基线，让边界落在完整想法上。但看不到页面布局，表格可能被切断，标题可能与它介绍的文本分离。

## 文档结构感知

对 PDF/HTML/Markdown，先按标题和章节切，再在章节内用语义或固定大小。表格应作为整体保留（绝不从中间切断），代码块作为原子块。工具：LlamaParse、Unstructured.io。

**worked example**（40 页员工手册，含标题、表格、交叉引用）：

- 固定 512 token → ~80 块，几块从句中开始，一块含"产假表格后半 + 报销政策前半"——问休假额度得到基于碎片的自信错误答案。
- 递归分割修复句中问题，但表格仍被切（表格不是段落）。
- 结构感知按标题切 → ~30 块，每块对应一条真实政策，表格完整保留。

## 块大小经验

- 精确检索（FAQ）：200–500 token。
- 上下文检索（技术文档）：500–1000 token。
- 长生成：1000–2000 token。
- 起点：512 token + 10–20% overlap，再按评估迭代。

## 参考资料

- LangChain Text Splitters 文档：https://python.langchain.com/docs/concepts/text_splitters/
- Anthropic: Introducing Contextual Retrieval：https://www.anthropic.com/news/contextual-retrieval
