#!/usr/bin/env python3
"""按知识树规范创建一个空节点骨架。"""
import argparse
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def quote(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ap = argparse.ArgumentParser(description="创建知识树节点骨架")
    ap.add_argument("path", help="节点目录，如 trees/computer/ai/new-node")
    ap.add_argument("--name", required=True, help="中文名称")
    ap.add_argument("--name-en", help="英文 name，默认取目录名")
    ap.add_argument("--desc", help="中文描述，默认由名称生成")
    ap.add_argument("--desc-en", help="英文 description，默认同 --desc")
    args = ap.parse_args()

    p = Path(args.path)
    if not p.is_absolute():
        p = REPO / p
    rel = p.relative_to(REPO)
    if not rel.parts or rel.parts[0] != "trees":
        raise SystemExit("节点必须放在 trees/ 下")
    slug = p.name
    if not KEBAB.match(slug):
        raise SystemExit(f"目录名必须是 kebab-case: {slug}")
    if p.exists():
        raise SystemExit(f"目录已存在: {rel}")

    name_en = args.name_en or slug
    desc = args.desc or f"{args.name}的说明待补。"
    desc_en = args.desc_en or desc
    p.mkdir(parents=True)
    md = p / f"{slug}.md"
    md.write_text(
        "---\n"
        f"description: {quote(desc_en)}\n"
        f"描述: {quote(desc)}\n"
        f"name: {quote(name_en)}\n"
        f"名称: {quote(args.name)}\n"
        "---\n\n"
        f"# {args.name}\n\n"
        "## 定义\n\n"
        "## 边界\n\n"
        "## 参考资料\n\n",
        encoding="utf-8",
    )
    (p / "links.csv").write_text("term,target\n", encoding="utf-8")
    (p / "questions.jsonl").write_text("", encoding="utf-8")
    print(f"已创建 {rel}/")
    print("  同名 md / links.csv 表头 / questions.jsonl")
    print("下一步：补正文与一手来源，再按正文用词登记 links.csv。")


if __name__ == "__main__":
    main()
