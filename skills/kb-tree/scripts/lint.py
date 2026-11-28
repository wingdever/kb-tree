#!/usr/bin/env python3
"""知识树一致性巡检：结构、front matter、跨节点引用、来源痕迹、数字出处、重复断言、questions.jsonl。

用法：
    python3 skills/kb-tree/scripts/lint.py trees/computer/ai/agent
    python3 skills/kb-tree/scripts/lint.py trees/computer/ai/agent --strict   # 警告也算失败

退出码：0 无错误；1 有错误（或 --strict 下有警告）。
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from collections import defaultdict

FRONT_KEYS = ("description", "描述", "name", "名称")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []
warns = []


def err(path, msg, line=None):
    errors.append((path, line, msg))


def warn(path, msg, line=None):
    warns.append((path, line, msg))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_front(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[4:end]
    fields = {}
    for ln in block.splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if ":" not in ln:
            return None
        k, v = ln.split(":", 1)
        fields[k.strip()] = v.strip()
    return fields


def body_of(text):
    end = text.find("\n---", 3)
    return text[end + 4 :] if end != -1 else text


def sections(body):
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,3})\s+(.+)$", body, re.M)]


def check_structure(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("skills", ".git")]
        name = os.path.basename(dirpath)
        rel = os.path.relpath(dirpath, root)
        if rel != "." and not KEBAB.match(name):
            err(os.path.join(dirpath, "?"), f"目录名不是 kebab-case: {name}")
        if "README.md" in filenames:
            err(os.path.join(dirpath, "README.md"), "树内不允许 README.md")
        if rel == ".":
            continue
        if f"{name}.md" not in filenames:
            err(dirpath, f"缺少同名 md: {name}.md")
        for fn in filenames:
            if fn.endswith(".md"):
                base = fn[:-3]
                if not KEBAB.match(base):
                    err(os.path.join(dirpath, fn), f"文件名不是 kebab-case: {fn}")


def check_front(root, mds):
    for p in mds:
        text = read(p)
        fields = parse_front(text)
        if fields is None:
            err(p, "缺少或无法解析 front matter")
            continue
        extra = set(fields) - set(FRONT_KEYS)
        missing = set(FRONT_KEYS) - set(fields)
        if extra:
            err(p, f"front matter 多余字段: {sorted(extra)}")
        if missing:
            err(p, f"front matter 缺字段: {sorted(missing)}")
        for k, v in fields.items():
            if not (v.startswith('"') and v.endswith('"')):
                err(p, f"front matter 值未用双引号: {k}")
        if fields.get("name", "").strip('"') and not re.match(
            r"^[A-Za-z0-9 ,.:\-&/'()+]+$", fields["name"].strip('"')
        ):
            err(p, f"name 含非英文字符: {fields['name']}")


NO_SOURCE_PAGES = set()


def load_no_source_pages():
    """读取「确认无外部来源」清单，避免对着纯经验页反复报警。"""
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "no-source-pages.json")
    if not os.path.exists(here):
        return set()
    try:
        return {str(x) for x in json.load(open(here, encoding="utf-8")).get("pages", [])}
    except Exception:
        return set()


def check_sources(root, mds):
    for p in mds:
        text = read(p)
        if re.search(r"迁移自|原笔记|补抓|源于原笔记|另一来源", text):
            for i, ln in enumerate(text.splitlines(), 1):
                if re.search(r"迁移自|原笔记|补抓|源于原笔记|另一来源", ln):
                    err(p, "出现操作痕迹/含糊来源", i)
        body = body_of(text)
        secs = sections(body)
        if "参考资料" not in secs:
            if os.path.relpath(p, root) not in NO_SOURCE_PAGES:
                warn(p, "无「## 参考资料」小节（确认确实无外部来源）")
        else:
            last = [s for s in secs if not s.startswith(" ")]
            tail = body.rsplit("## 参考资料", 1)[0]
            after = body.split("## 参考资料", 1)[1]
            if re.search(r"^#{1,2}\s+\S", after, re.M):
                warn(p, "「参考资料」不是最后一节")
            if re.match(r"^\s*\n?#{1,2}\s", tail.splitlines()[-1] if tail.splitlines() else ""):
                pass


def check_cross_refs(root, mds):
    for p in mds:
        text = read(p)
        body = body_of(text).split("## 参考资料")[0]
        off = text[: len(text) - len(body)].count("\n")
        for i, ln in enumerate(body.splitlines(), 1):
            if re.search(r"\]\((?!https?://)([^)]+)\)", ln):
                err(p, "存在相对链接", i)
            if re.search(r">\s*相关[:：]", ln):
                err(p, "存在「> 相关」引用行", i)
            if re.search(r"(参见|详见|另见)", ln) and not re.search(r"(官方|官网|文档|论文|规范|标准|手册|链接|http)", ln):
                warn(p, "出现跨节点指引语", i + off)
            if re.search(r"(本树|本节点|兄弟节点)", ln):
                warn(p, "出现树结构元话术", i + off)


def node_names(mds):
    names = {}
    for p in mds:
        fields = parse_front(read(p)) or {}
        for k in ("名称", "name"):
            v = fields.get(k, "").strip('"').strip()
            if len(v) >= 5:
                names.setdefault(v, p)
    return names


CUE = re.compile(r"(参见|详见|另见)")


def norm_name(s):
    return re.sub(r"[\s（）()·\-—_/]+", "", s).lower()


def check_node_mentions(mds):
    names = node_names(mds)
    for p in mds:
        text = read(p)
        body = body_of(text).split("## 参考资料")[0]
        off = text[: len(text) - len(body)].count("\n")
        fields = parse_front(text) or {}
        own = {norm_name(fields.get(k, "").strip('"')) for k in ("name", "名称")}
        for i, ln in enumerate(body.splitlines(), 1):
            if not CUE.search(ln):
                continue
            for n, src in names.items():
                if norm_name(n) in own or n not in ln:
                    continue
                if len(n) >= 6:
                    warn(p, f"疑点名其他节点「{n}」", i + off)


NUM_PAT = re.compile(r"(\d+(?:\.\d+)?\s*[%％])|(\d+(?:\.\d+)?\s*(?:×|[xX]\b))|(\d+(?:\.\d+)?\s*倍)")

REGISTRY = {}


def norm_num(tok):
    return tok.replace(" ", "").replace("％", "%")


def load_registry():
    """读取人工核对过的数字登记表：{相对路径: {数字}}。"""
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "number-sources.json")
    if not os.path.exists(here):
        return {}
    try:
        data = json.load(open(here, encoding="utf-8"))
    except Exception:
        return {}
    out = defaultdict(set)
    for e in data.get("entries", []):
        for n in e.get("numbers", []):
            out[e.get("path", "")].add(norm_num(str(n)))
    return out


def check_numbers(mds, root):
    for p in mds:
        text = read(p)
        body = body_of(text).split("## 参考资料")[0]
        off = text[: len(text) - len(body)].count("\n")
        claim = re.compile(r"(研究|论文|报告|数据|统计|实验|调查|提升|降低|成功率|失败率|准确率|覆盖率)")
        for i, ln in enumerate(body.splitlines(), 1):
            if not NUM_PAT.search(ln):
                continue
            if "http" in ln or "arXiv" in ln or "=" in ln:
                continue
            if not claim.search(ln):
                continue
            registered = REGISTRY.get(os.path.relpath(p, root), set())
            unreg = [m.group(0) for m in NUM_PAT.finditer(ln) if norm_num(m.group(0)) not in registered]
            if not unreg:
                continue
            warn(p, "数字需核对出处（未登记 " + "、".join(unreg) + "）: " + ln.strip()[:60], i + off)


SENT_SPLIT = re.compile(r"[。！？]")


def check_duplicates(mds):
    index = defaultdict(list)
    for p in mds:
        body = body_of(read(p)).split("## 参考资料")[0]
        in_code = False
        for raw in body.splitlines():
            if raw.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            raw = raw.strip()
            if raw.startswith("|"):
                continue
            raw = raw.lstrip("-*>0123456789. ")
            for s in SENT_SPLIT.split(raw):
                s = re.sub(r"\s+", "", s)
                if len(s) < 18:
                    continue
                index[s].append(p)
    for s, ps in index.items():
        uniq = sorted(set(ps))
        if len(uniq) > 1:
            warn(" | ".join(os.path.basename(x) for x in uniq), f"重复断言: {s[:50]}")


def norm_q(q):
    return re.sub(r"[\s，。？！、,.\?!]+", "", q).lower()





def find_repo_root(root):
    cur = os.path.abspath(root)
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    parts = os.path.abspath(root).split(os.sep)
    if "trees" in parts:
        return os.sep.join(parts[: parts.index("trees")])
    return os.path.abspath(root)


def check_links(root, mds):
    repo_root = find_repo_root(root)
    files = 0
    rows_total = 0
    for md in mds:
        d = os.path.dirname(md)
        fp = os.path.join(d, "links.csv")
        if not os.path.exists(fp):
            err(fp, "缺 links.csv")
            continue
        files += 1
        body = body_of(read(md)).split("## 参考资料")[0]
        seen = set()
        try:
            with open(fp, encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    err(fp, "空文件，缺表头 term,target")
                    continue
                header[0] = header[0].lstrip("\ufeff")
                if [x.strip() for x in header] != ["term", "target"]:
                    err(fp, f"表头应为 term,target，实际为 {header}")
                for lineno, row in enumerate(reader, 2):
                    if not row or all(not x.strip() for x in row):
                        continue
                    rows_total += 1
                    if len(row) != 2:
                        err(fp, f"应为 2 列，实际 {len(row)} 列", lineno)
                        continue
                    term, target = row[0].strip(), row[1].strip()
                    if not term or not target:
                        err(fp, "term/target 不能为空", lineno)
                        continue
                    if term.startswith("{") or term.endswith("}"):
                        if not (term.startswith("{") and term.endswith("}")):
                            err(fp, f"词形组格式不完整: {term}", lineno)
                            continue
                        variants = [x.strip() for x in term[1:-1].split("|")]
                        if len(variants) < 2 or any(not x for x in variants):
                            err(fp, f"词形组至少要有两个非空词形: {term}", lineno)
                            continue
                        if any("{" in x or "}" in x for x in variants):
                            err(fp, f"词形组不支持嵌套: {term}", lineno)
                            continue
                        if len(set(variants)) != len(variants):
                            err(fp, f"词形组内有重复词形: {term}", lineno)
                            continue
                        if not any(v in body for v in variants):
                            err(fp, f"词形组内没有词在正文出现: {term}", lineno)
                    elif term not in body:
                        err(fp, f"term 未在正文出现: {term}", lineno)
                    if os.path.isabs(target) or ".." in target.split("/"):
                        err(fp, f"target 必须是仓库内相对路径: {target}", lineno)
                        continue
                    td = os.path.normpath(os.path.join(repo_root, target))
                    if not os.path.isdir(td):
                        err(fp, f"target 目录不存在: {target}", lineno)
                        continue
                    if not os.path.exists(os.path.join(td, os.path.basename(td) + ".md")):
                        err(fp, f"target 不是知识节点目录: {target}", lineno)
                    if os.path.normpath(td) == os.path.normpath(d):
                        err(fp, "target 不能指向自己", lineno)
                    key = (term, target)
                    if key in seen:
                        err(fp, f"重复行: {term} -> {target}", lineno)
                    seen.add(key)
        except (OSError, csv.Error) as e:
            err(fp, f"读 CSV 失败: {e}")
    return files, rows_total


OBJ_ENUM = {
    "realm": {"logical", "material", "symbolic"},
    "kind": {"thing", "event", "relation"},
    "generality": {"particular", "type"},
    "volatility": {"high", "medium", "low"},
}


def check_objects(mds):
    for md in mds:
        d = os.path.dirname(md)
        fp = os.path.join(d, "object.json")
        if not os.path.exists(fp):
            continue
        try:
            obj = json.loads(read(fp))
        except json.JSONDecodeError as e:
            err(fp, f"坏 JSON: {e}")
            continue
        if not isinstance(obj, dict):
            err(fp, "不是对象")
            continue
        for k, allowed in OBJ_ENUM.items():
            if k not in obj:
                if k in ("realm", "kind", "generality"):
                    err(fp, f"缺坐标 {k}")
                continue
            v = obj[k]
            if v not in allowed:
                err(fp, f"{k} 取值非法: {v}")
        for k in ("canonical", "verify"):
            if k in obj and not isinstance(obj[k], str):
                err(fp, f"{k} 应为字符串")


def check_questions_coverage(mds, verbose=False):
    missing = 0
    for md in mds:
        d = os.path.dirname(md)
        if os.path.exists(os.path.join(d, "questions.jsonl")):
            continue
        missing += 1
        heads = re.findall(r"^##\s+", read(md), re.M)
        if verbose and len(heads) >= 3:
            warn(md, f"缺 questions.jsonl（{len(heads)} 个二级标题可挂问题）")
    return missing


def check_questions(root):
    files = sorted(glob.glob(os.path.join(root, "**", "questions.jsonl"), recursive=True))
    primary = {}
    total = 0
    for fp in files:
        d = os.path.dirname(fp)
        base = os.path.basename(d)
        md = os.path.join(d, f"{base}.md")
        heads = set()
        if os.path.exists(md):
            heads = {m.group(1).strip() for m in re.finditer(r"^#{2,3}\s+(.+)$", read(md), re.M)}
        for lineno, line in enumerate(read(fp).splitlines(), 1):
            if not line.strip():
                continue
            total += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                err(fp, f"坏 JSON: {e}", lineno)
                continue
            if not isinstance(item, dict):
                err(fp, "不是对象", lineno)
                continue
            for k in ("q", "section"):
                if not isinstance(item.get(k), str) or not item[k].strip():
                    err(fp, f"缺字段 {k}", lineno)
            role = item.get("role", "primary")
            if role not in ("primary", "perspective"):
                err(fp, f"role 非法: {role}", lineno)
            if role == "perspective":
                owner = item.get("owner")
                if not owner:
                    err(fp, "perspective 缺 owner", lineno)
                elif not os.path.exists(os.path.normpath(os.path.join(d, owner))):
                    err(fp, f"owner 路径不存在: {owner}", lineno)
            if item.get("section") and item["section"] not in heads:
                err(fp, f"section 未命中标题: {item['section']}", lineno)
            if role == "primary" and isinstance(item.get("q"), str):
                k = norm_q(item["q"])
                if k in primary:
                    err(fp, f"primary 重复: {primary[k]}", lineno)
                else:
                    primary[k] = f"{os.path.relpath(fp, root)}:{lineno}"
    return len(files), total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--coverage", action="store_true", help="列出缺 questions 的节点")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    mds = sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
    mds = [p for p in mds if "/skills/" not in p]
    REGISTRY.update(load_registry())
    NO_SOURCE_PAGES.update(load_no_source_pages())

    check_structure(root)
    check_front(root, mds)
    check_sources(root, mds)
    check_cross_refs(root, mds)
    check_node_mentions(mds)
    check_numbers(mds, root)
    check_duplicates(mds)
    check_objects(mds)
    nlink_files, nlinks = check_links(root, mds)
    missing_q = check_questions_coverage(mds, args.coverage)
    nfiles, nq = check_questions(root)

    print(f"节点 md={len(mds)}  questions 文件={nfiles} 条目={nq}  links 文件={nlink_files} 条目={nlinks}  覆盖 {len(mds)-missing_q}/{len(mds)}")
    print(f"错误 {len(errors)}  警告 {len(warns)}")
    for p, ln, msg in errors:
        print(f"  E {os.path.relpath(p, root) if os.path.isabs(p) else p}:{ln or ''} {msg}")
    if args.strict or len(errors) == 0:
        for p, ln, msg in warns:
            print(f"  W {p}:{ln or ''} {msg}")
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
