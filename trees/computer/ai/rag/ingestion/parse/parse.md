---
description: "Parsing crawled content into clean text and metadata: HTML, structured data, PDF and OCR"
描述: "爬取内容解析：HTML、结构化数据、PDF 与 OCR 转成干净文本和元数据"
name: "Content Parsing"
名称: "内容解析"
---

# 内容解析

解析把响应变成可索引的文本与字段。它决定了正文是否完整、标题与时间是否可信、导航与广告是否被清掉；同一批页面，解析质量不同，检索效果会差一个档次。

## HTML：先找正文，再抽字段

- **DOM 解析**：用解析器构建 DOM，再按 CSS 选择器或 XPath 抽节点；不要用正则切 HTML，嵌套与属性顺序会让规则很快失效。
- **正文抽取**：按语义标签（`article`、`main`）、密度、链接比例与文本长度判断正文块；导航、侧栏、评论、页脚要单独剔除。
- **字段抽取**：标题、作者、发布时间、栏目、语言、 canonical URL；优先用页面自带的元数据，而不是从正文猜。
- **结构化数据**：JSON-LD、Microdata、OpenGraph 常带作者、日期、类型；它们比版式稳定，但可能缺失或过期。

## PDF 与 Office

PDF 先取文本层；扫描件没有文本层时才走 OCR。表格要保留行列结构，不能把单元格拼成一段。Office 文档按段落、标题层级与表格解析，避免把样式当成语义。

OCR 的代价是错误率与版式依赖：能拿到原始 PDF 文本层或源文件，就不要用截图识别。识别结果要保留页码与坐标，方便回溯。

## 输出契约

每条解析结果至少包含：

- `text`：去噪后的正文；
- `title` / `author` / `published_at` / `language`；
- `canonical_url` 与最终 URL；
- `fetched_at`、`content_hash`、`parser_version`；
- `source` 与许可证/授权标记。

没有 `fetched_at` 与 `parser_version`，后续无法判断新鲜度，也无法在解析器升级后做回归。

## 常见失败

- **只取 `<body>` 全文**：导航与广告一起进索引，检索结果被模板文本污染。
- **正则切 HTML**：遇到嵌套、注释、属性换行就断；应使用 DOM。
- **时间从正文猜**：页面有多个日期（发布、更新、评论），猜错会让新鲜度判断失真。
- **忽略编码**：不按响应头与 meta charset 解码，中文变乱码。
- **表格被拍平**：行列关系丢失，数字与表头对不上。

## 一句话主线

解析要先用 DOM 找正文、再用元数据抽字段，PDF 优先文本层、扫描件才 OCR；输出必须带来源、时间与解析器版本，才能被检索与复算。

## 参考资料

- W3C HTML 规范（DOM 与文档语义）：https://html.spec.whatwg.org/
- JSON-LD 官方规范（结构化数据格式）：https://www.w3.org/TR/json-ld11/
- PDF 规范（ISO 32000，文本层与文档结构）：https://www.iso.org/standard/75839.html
