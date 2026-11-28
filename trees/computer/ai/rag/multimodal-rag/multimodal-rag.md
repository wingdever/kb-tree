---
description: "Multimodal RAG: vision-based document retrieval, ColPali late interaction, unified embeddings and agentic vision RAG"
描述: "多模态 RAG：视觉文档检索、ColPali 晚期交互、统一嵌入与视觉 Agentic RAG"
name: "Multimodal RAG"
名称: "多模态 RAG"
---

# 多模态 RAG（视觉 RAG）

经典 RAG 是为纯文本构建的：解析 PDF → OCR 图片 → 切块 → 嵌入 → 检索。这条流水线在企业真实文档（年报、临床报告、工程图纸、幻灯片、监管申报）上静默失效——大部分意义活在视觉结构里：柱状图、双栏对比、流程图、印章签名、表格单元格里的脚注。OCR 把结构压成噪声文本，嵌入模型再也找不回它。

多模态 RAG 的核心立场：**页面图像本身就是块（unit of evidence）**。用视觉语言模型直接读页面，或用视觉编码器嵌入页面图像。

## 三条技术路线

### 1. 统一视觉嵌入（2026 混合语料默认）

Cohere Embed v4、voyage-multimodal-3.5 等把文本与图像放进同一嵌入空间——文本查询可检索图像，反之亦然，一个模型、每项一个向量。单向量模型在多数企业语料上已可与更重的 page-as-image 方案竞争，存储/运维画像与文本 RAG 相同——**最低风险、捕获大部分收益**。选型仍是在自有数据上 benchmark，而非榜单。

### 2. Page-as-image 晚期交互（保真度路线）

ColPali / ColQwen2.5 / ColNomic 跳过 OCR：把每页渲染成图像，视觉编码器切成大量 patch（如 32×32=1024 个 patch），**每个 patch 一个向量**。查询时把 query token 与所有 patch 做 MaxSim 晚期交互（ColBERT 思路）——每个 query token 找最匹配的 patch，最大值求和排名。"revenue"点亮表格里收入数字的 patch，"2024"点亮另一处——匹配是细粒度且空间的，不是整页模糊平均。

- **ColPali** 基于 PaliGemma-3B（SigLIP 视觉编码器 + Gemma-2B），端到端对比学习训练。ViDoRe 基准上平均 NDCG@5 **81.3**，远超文本基线（Unstructured + OCR + BGE-M3）的 66.1；索引快约 **18×**（0.39s/页 vs 7.2s/页）；零样本跨语言（英语训练、法语表现强）；晚期交互天然可解释（热力图显示模型看了哪里）。

### 3. 模块化 pipeline（OCR + 布局解析）

传统路线：PDF 解析、OCR、布局检测、切块、嵌入。优点是成熟、存储轻、适合干净文本密集文档；缺点是 OCR 错误硬编码进文本流（"8"读成"B"、两列合并），造成级联误差，且丢失字体、颜色、空间关系。

## 存储权衡（关键决策）

晚期交互模型每页存的是**每 patch 一个向量**，账要提前算清：

```
单向量（统一嵌入）：1 向量/页 × 1024 维 × 4 字节 ≈ 4 KB/页
ColPali 多向量：1024 patch/页 × 128 维 × 4 字节 ≈ 512 KB/页 ≈ 128× 存储
10 万页语料：单向量 ≈ 0.4 GB；ColPali ≈ 51 GB（量化前）
```

50–130× 的存储乘数正是**不默认上 page-as-image 的理由**——它抬高索引、内存、查询算力，还受向量库是否原生支持多向量限制。二值量化 + patch 剪枝能压回地面，但是要计划的工程，不是勾选框。

## 生成端：检索只是一半

多模态检索改变了交给生成器的东西：检索到页面图像，就必须传给**能看图的模型**（Gemini 3 Pro、GPT-5.x vision、Claude Opus 4、Qwen2.5-VL、InternVL2.5），文本 LLM 读不了你辛苦检索的图表。token 预算现在包含**不便宜且可能主导长上下文调用的 image tokens**。团队常设计漂亮的视觉检索器，却卡在生成器看不了图或 token 成本失控——**精确检索更重要**：传 2 页相关图像，而非 20 页，因为松散 top-k 的代价以 image token 计。

引用单位也变了：不是"doc.pdf 第 4 段"，而是 `{doc, page, bbox}`——UI 把引用区域高亮成裁剪图，这是监管领域可审计的硬要求。

## Agentic Vision RAG

不止单次"检索→回答"，而是 Agent 循环：planner 分解问题 → 每步调用工具（retrieve、extract_table、chart_to_data、calculator、sql、web_search）→ 观察加入状态 → 决定下一步或最终回答。循环有界（max 6–8 步），每次工具调用留日志，critic 步在返回前对照检索证据核验草稿。

判断"交互式 demo 是真好还是预录"：看骨干是否**逐帧接收动作**——多数生成模型一次性产出整段视频，无法实时响应动作。

## 何时用 / 不用

**用**：文档视觉密集（财报、科研论文、扫描表单、幻灯片，布局承载意义）；财务 PDF 上的 recall 跃升能证明索引成本合理；表格/图表/工程图/签章的视觉问答。

**不用**：干净的纯文本文档——经典文本 RAG 更简单更便宜；偶有 logo 的散文语料不值得多向量税。

成熟管道常**按文档类型路由**：混合检索（dense+sparse via RRF）+ 只为需要的文档类别加视觉索引。caption-and-index（用视觉模型描述图像再索引文字）是不能改检索栈时的 retrofit 方案。

## 评估

ViDoRe（视觉文档检索基准，含 DocVQA/InfoVQA 及能源、政府、医疗、AI 领域任务）；指标 NDCG@5、召回、bbox 引用准确性、生成答案的 groundedness。注意多数安全基准本身是机器生成的，存在循环评估问题。

## 参考资料

- CLIP: Learning Transferable Visual Models From Natural Language Supervision：https://arxiv.org/abs/2103.00020
- ColPali: Efficient Document Retrieval with Vision Language Models：https://arxiv.org/abs/2407.01449
