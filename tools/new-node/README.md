# new-node

按仓库规范创建一个知识节点骨架，避免漏建同名 md、`links.csv` 表头或问题夹具。

## 用法

在仓库根执行：

```bash
python3 tools/new-node/new_node.py trees/computer/ai/example \
  --name "示例概念" --desc "这个概念讲什么。"
```

生成：

- `trees/.../example/example.md`：四字段 front matter 与空的定义/边界/参考资料小节；
- `links.csv`：仅表头；
- `questions.jsonl`：空文件。

脚本只创建骨架，不写知识内容，也不改父文档；父文档仍不列子节点链接。
