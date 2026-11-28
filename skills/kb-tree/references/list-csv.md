# 附属清单 list.csv

## 用途

`<节点名>.list.csv` 用来承载节点里**可枚举的条目**：教程、工具、厂商、API、论文、产品、渠道等。一个条目一行，像填表一样维护；Markdown 正文只保留定义、分类、判断与选择建议，不再铺大表。

它解决两个问题：

- 条目多时，Markdown 表格难改、易错位，增删一行要动整段；
- 条目是结构化数据，应该能被脚本统计、去重、导出，而不是埋在正文里。

## 文件形态

- 文件名固定为 `<节点目录名>.list.csv`，放在该节点目录下。例如节点目录 `tutorials/` 对应 `tutorials.list.csv`。
- UTF-8，首行必须是表头：
  `name,group,source,url,note`
- 每行一个条目，字段用英文逗号分隔；字段含逗号、双引号或换行时按 RFC 4180 加双引号转义。
- 它是 C 层附属文件，不是知识节点，不套四字段 front matter，不计入“目录 + 同名 md”自检；缺失合法。

## 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | 是 | 条目名称，同一文件内唯一；写正式名称，不写“点这里” |
| `group` | 是 | 条目所属分组，取值由本页定义并在正文说明；同一文件内保持稳定 |
| `source` | 是 | 提供方：公司、社区、作者、课程平台或维护方 |
| `url` | 是 | 直达链接，必须以 `http://` 或 `https://` 开头；不写搜索结果页、短链或需登录的地址 |
| `note` | 否 | 一句话说明“它是什么/学完能做什么”，不写营销话术；可留空 |

`group` 不是自由标签堆场。一个节点内的分组应当能回答“读者按什么分类找条目”，通常三到六组；分组定义写进 Markdown 正文，CSV 只填组名。

## 规则

1. **一行一个对象**。不要把多个教程塞进一行，也不要用换行符在单元格里堆列表。
2. **`name` 唯一**。同名条目要么合并，要么在名称里加限定词（语言、版本、平台）。
3. **`url` 必须可直接访问**。官方文档、仓库、课程页优先；拿不到稳定链接时，不要把猜测的 URL 填进去。
4. **正文与清单分工**。正文写“怎么选、为什么这样分、常见坑”；清单写“有哪些、在哪、是什么”。正文不再重复整张表。
5. **清单不替代来源标注**。关键结论与数字仍在正文的 `## 参考资料` 交代；清单只提供入口。
6. **不把清单当导航**。它不是子节点目录，也不表达节点之间的上下位关系；节点关系仍放 `links.csv`。

## 示例

```csv
name,group,source,url,note
OpenAI Agents SDK — Python Quickstart,官方快速入门,OpenAI,https://openai.github.io/openai-agents-python/quickstart/,第一个文本 Agent 与工具循环
LangGraph — Introduction,框架教程,LangChain Academy,https://academy.langchain.com/courses/intro-to-langgraph,状态图、记忆与 human-in-the-loop
```

正文对应写法：

```markdown
## 教程清单

逐条清单在 `tutorials.list.csv`，一行一个教程，列为 `name, group, source, url, note`。
```

## 校验

巡检脚本会检查文件名、表头、列数、必填字段、`url` 协议与 `name` 重复。可直接运行：

```python
import csv, glob, os

HEADER = ['name', 'group', 'source', 'url', 'note']
for fp in sorted(glob.glob('**/*.list.csv', recursive=True)):
    d = os.path.dirname(fp)
    assert os.path.basename(fp) == os.path.basename(d) + '.list.csv', fp
    rows = list(csv.reader(open(fp, encoding='utf-8')))
    assert rows and rows[0] == HEADER, fp
    names = set()
    for i, row in enumerate(rows[1:], 2):
        assert len(row) == 5, (fp, i)
        name, group, source, url, note = [x.strip() for x in row]
        assert name and group and source and url, (fp, i)
        assert url.startswith(('http://', 'https://')), (fp, i)
        assert name not in names, (fp, i, 'duplicate name')
        names.add(name)
print('ok')
```

`skills/kb-tree/scripts/lint.py` 已内置同一组检查；`bash tools/check.sh` 会把它纳入全树巡检。
