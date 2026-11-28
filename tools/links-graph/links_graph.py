#!/usr/bin/env python3
"""统计和查询 links.csv 构成的对象级词项图。"""
import argparse
import csv
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def node_dirs(root):
    nodes = set()
    for md in root.rglob("*.md"):
        if md.stem == md.parent.name:
            nodes.add(str(md.parent.relative_to(REPO)))
    return nodes


def load_graph(root):
    nodes = node_dirs(root)
    edges = []
    broken = []
    for fp in root.rglob("links.csv"):
        source = str(fp.parent.relative_to(REPO))
        try:
            with fp.open(encoding="utf-8", newline="") as f:
                rows = list(csv.reader(f))
        except (OSError, csv.Error) as e:
            broken.append((source, "", f"读 CSV 失败: {e}"))
            continue
        for row in rows[1:]:
            if len(row) != 2 or not row[0].strip() or not row[1].strip():
                broken.append((source, "", "列数或空值异常"))
                continue
            term, target = row[0].strip(), row[1].strip()
            if target not in nodes:
                broken.append((source, target, "目标节点不存在"))
                continue
            edges.append({"source": source, "term": term, "target": target})
    return nodes, edges, broken


def degree(nodes, edges):
    out = {n: 0 for n in nodes}
    inc = {n: 0 for n in nodes}
    for e in edges:
        out[e["source"]] = out.get(e["source"], 0) + 1
        inc[e["target"]] = inc.get(e["target"], 0) + 1
    return out, inc


def show_node(nodes, edges, label):
    if label not in nodes:
        raise SystemExit(f"找不到节点: {label}")
    ins = [e for e in edges if e["target"] == label]
    outs = [e for e in edges if e["source"] == label]
    print(f"节点: {label}")
    print(f"入边 {len(ins)} 条")
    for e in ins:
        print(f"  {e['source']}  [{e['term']}]")
    print(f"出边 {len(outs)} 条")
    for e in outs:
        print(f"  [{e['term']}] -> {e['target']}")


def stats(nodes, edges, broken, top):
    out, inc = degree(nodes, edges)
    populated = sum(1 for n in nodes if out.get(n, 0))
    empty = len(nodes) - populated
    zero_in = sum(1 for n in nodes if not inc.get(n, 0))
    orphans = sum(1 for n in nodes if not out.get(n, 0) and not inc.get(n, 0))
    print(f"节点 {len(nodes)}  links 文件 {len(nodes)}  边 {len(edges)}")
    print(f"有出边 {populated}  仅表头 {empty}  零入边 {zero_in}  双向皆零 {orphans}  目标异常 {len(broken)}")
    print("\n被引用最多:")
    for n, c in sorted(inc.items(), key=lambda x: (-x[1], x[0]))[:top]:
        if c:
            print(f"  {c:3d}  {n}")
    print("\n出边最多:")
    for n, c in sorted(out.items(), key=lambda x: (-x[1], x[0]))[:top]:
        if c:
            print(f"  {c:3d}  {n}")
    print("\n零出边示例:")
    for n in sorted(n for n in nodes if not out.get(n, 0))[:top]:
        print(f"  {n}")
    if broken:
        print("\n目标异常:")
        for s, t, why in broken[:top]:
            print(f"  {s}: {t or '-'} ({why})")


def main():
    ap = argparse.ArgumentParser(description="统计和查询 links.csv 对象级词项图")
    ap.add_argument("root", nargs="?", default="trees", help="要分析的树根，默认 trees")
    ap.add_argument("--node", help="查看某个节点的入边与出边，路径相对仓库根")
    ap.add_argument("--json", metavar="PATH", help="把 nodes/edges/stats 写到 JSON 文件")
    ap.add_argument("--top", type=int, default=12, help="排行榜与示例条数，默认 12")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_absolute():
        root = REPO / root
    if not root.exists():
        raise SystemExit(f"根目录不存在: {root}")

    nodes, edges, broken = load_graph(root)
    if args.node:
        show_node(nodes, edges, args.node)
        return
    stats(nodes, edges, broken, args.top)
    if args.json:
        out, inc = degree(nodes, edges)
        data = {
            "root": str(root.relative_to(REPO)),
            "nodes": sorted(nodes),
            "edges": edges,
            "stats": {
                "nodes": len(nodes),
                "edges": len(edges),
                "populated": sum(1 for n in nodes if out.get(n, 0)),
                "zero_out": sum(1 for n in nodes if not out.get(n, 0)),
                "zero_in": sum(1 for n in nodes if not inc.get(n, 0)),
                "orphans": sum(1 for n in nodes if not out.get(n, 0) and not inc.get(n, 0)),
                "broken": len(broken),
            },
        }
        Path(args.json).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nJSON 已写入 {args.json}")


if __name__ == "__main__":
    main()
