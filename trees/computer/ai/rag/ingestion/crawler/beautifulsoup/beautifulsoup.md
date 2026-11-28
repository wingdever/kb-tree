---
description: "BeautifulSoup HTML/XML parsing library: tree navigation, selectors and extraction limits"
描述: "BeautifulSoup：HTML/XML 解析、树导航、选择器与抽取边界"
name: "BeautifulSoup"
名称: "BeautifulSoup 解析库"
---

# BeautifulSoup

BeautifulSoup 是 Python 的 HTML/XML 解析库，负责把响应文本变成一棵可导航的树。它属于爬虫的**解析环节**：不负责发请求、不执行 JavaScript、不管理调度；把它当成爬虫本体，会低估抓取链上的其他工作。

## 它在爬虫链路中的位置

一次抓取大致是：发现 URL → 发请求 → 拿到 HTML → **解析成树** → 抽正文/字段/链接。BeautifulSoup 只负责“解析成树”这一段：

- **上游**：需要有人把 HTML 取回来，并处理编码、重定向与状态码。
- **下游**：需要有人把抽出的文本去重、入库、更新；BeautifulSoup 不提供这些能力。
- **不负责**：JavaScript 渲染、反爬对抗、robots 判定、分布式调度。

所以它适合静态 HTML 或已经渲染完成的 DOM，不适合“页面正文只在浏览器里出现”的场景。

## 核心用法

- **构造**：`BeautifulSoup(html, "html.parser")` 或指定 `"lxml"`；传 bytes 时让库处理编码，避免先错误解码。
- **查找**：`find` / `find_all` 按标签与属性查；`select` / `select_one` 按 CSS 选择器查。
- **取值**：`get_text(strip=True)` 取文本；`attrs` 取属性；`parents` / `children` / `next_sibling` 走层级。
- **改树**：可以删导航、广告与脚本标签，再统一取正文；但不要在解析层做业务判断。

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "lxml")
title = soup.select_one("h1").get_text(strip=True)
links = [a.get("href") for a in soup.select("a[href]")]
```

## 解析器选择

| 解析器 | 特点 | 适用 |
|---|---|---|
| `html.parser` | Python 内置，无需额外依赖 | 中小页面、环境受限 |
| `lxml` | 快、容错好，依赖 C 库 | 大批量、结构复杂的 HTML |
| `html5lib` | 更接近浏览器解析，慢 | 需要 HTML5 容错语义时 |

> 判断：解析器会改变树的形状，尤其是坏 HTML；生产环境要固定解析器，并对样本做回归。

## 抽取正文的要点

- **先删噪声**：`script`、`style`、`nav`、`footer`、广告与登录弹层；再取正文，避免模板文本进索引。
- **按语义定位**：优先 `article`、`main`、`[role=main]`，其次按文本密度与链接比例判断。
- **保留字段**：标题、作者、发布时间、canonical、语言；能从 meta/JSON-LD 取就不要从正文猜。
- **输出规范化**：统一空白、去掉零宽字符、保留段落边界；不要把整页 `get_text()` 直接入库。

## 边界与常见坑

- **不执行 JS**：脚本渲染的正文在 BeautifulSoup 里看不到；需要渲染时换无头浏览器或找接口。
- **编码错误**：先按响应头/meta 解码，或直接传 bytes；错误解码会让中文变乱码。
- **解析器差异**：同一个坏页面，`html.parser` 与 `lxml` 可能给出不同树；规则要固定解析器。
- **选择器脆弱**：依赖 `div:nth-child(3)` 这类位置选择器，版式一改就断；优先语义属性与稳定 class。
- **大文件内存**：整页构建树会吃内存；超大文档用流式解析或专用抽取器，不要硬扛。
- **安全**：HTML 是不可信输入；不要执行其中的脚本，不要把抓取内容直接拼进 SQL/命令。

## 一句话主线

BeautifulSoup 把 HTML 变成可查询的树，解决“静态页面怎么稳定抽字段”；它只覆盖解析这一段，抓取、渲染、去重、更新仍要由整条链路补齐。

## 参考资料

- BeautifulSoup 4 官方文档（解析器与选择器说明）：https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- W3C HTML 规范（DOM 与文档语义）：https://html.spec.whatwg.org/
- CSS Selectors Level 4（选择器语义）：https://www.w3.org/TR/selectors-4/
