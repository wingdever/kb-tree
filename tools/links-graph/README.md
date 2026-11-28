# links-graph

统计 `links.csv` 构成的对象级词项图：哪些节点被引用最多、哪些只有表头、哪些双向皆零，以及目标异常。它只读 `links.csv`，不修改知识文档。

## 用法

在仓库根执行：

```bash
python3 tools/links-graph/links_graph.py
python3 tools/links-graph/links_graph.py --top 20
python3 tools/links-graph/links_graph.py --node trees/computer/ai/rag/embedding
python3 tools/links-graph/links_graph.py --json /tmp/links-graph.json
```

`--node` 查看某个节点的入边和出边；`--json` 输出机器可读的 `nodes` / `edges` / `stats`，可用于检索侧建图。

## 输出口径

- `边`：`links.csv` 的每一行算一条边；词形组 `{RAG|检索增强生成}` 仍是一条边，不按组内词形拆开。
- `零出边`：只有表头的节点。正文自足，不代表异常。
- `零入边`：没有被任何页面登记为目标的节点。
- `双向皆零`：既没有出边也没有入边，通常是尚未策展的叶子或待补链接的高价值页。
- `目标异常`：`target` 不是已存在的知识节点目录；正式巡检仍以 `lint.py` 为准。
