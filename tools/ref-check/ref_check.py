#!/usr/bin/env python3
"""检查 review-queue.json 中的引用是否可达、是否到期。"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE = REPO / "skills/kb-tree/references/review-queue.json"
UA = "kb-tree-ref-check/1.0 (+https://gitee.com/wingdever/kb-tree)"


def curl_status(url, timeout):
    cmd = [
        "curl", "-L", "-sS", "-o", "/dev/null", "--max-time", str(timeout),
        "-w", "%{http_code} %{url_effective}", url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    except (OSError, subprocess.TimeoutExpired):
        return None, "curl failed"
    out = p.stdout.strip().split(maxsplit=1)
    if not out:
        return None, "curl empty"
    try:
        code = int(out[0])
    except ValueError:
        return None, out[0]
    final = out[1] if len(out) > 1 else url
    return (code if code else None), final


def fetch_status(url, timeout):
    if shutil.which("curl"):
        code, final = curl_status(url, timeout)
        if code is not None:
            return code, final
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.status, r.geturl()
            except urllib.error.HTTPError as e2:
                return e2.code, url
            except urllib.error.URLError as e2:
                return None, str(e2.reason)
        return e.code, url
    except urllib.error.URLError as e:
        return None, str(e.reason)


def main():
    ap = argparse.ArgumentParser(description="检查 review-queue.json 的引用")
    ap.add_argument("--queue", default=str(DEFAULT_QUEUE), help="队列 JSON 路径")
    ap.add_argument("--timeout", type=int, default=12, help="单条超时秒数")
    ap.add_argument("--strict", action="store_true", help="有失效或到期条目时返回非零")
    ap.add_argument("--json", action="store_true", help="输出 JSON 结果")
    args = ap.parse_args()

    queue = Path(args.queue)
    try:
        entries = json.loads(queue.read_text(encoding="utf-8")).get("entries", [])
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"读队列失败: {e}")

    today = dt.date.today()
    results = []
    for e in entries:
        status, final = fetch_status(e["url"], args.timeout)
        try:
            due = dt.date.fromisoformat(e["next_review"]) <= today
        except ValueError:
            due = False
        ok = status is not None and 200 <= status < 400
        results.append({
            "path": e.get("path", ""),
            "label": e.get("label", ""),
            "url": e["url"],
            "status": status,
            "final_url": final,
            "ok": ok,
            "due": due,
            "next_review": e.get("next_review", ""),
        })

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        bad = 0
        for r in results:
            mark = "OK" if r["ok"] and not r["due"] else ("DUE" if r["due"] and r["ok"] else "FAIL")
            if mark != "OK":
                bad += 1
            print(f"[{mark}] {r['status'] or '-':>4} {r['label']}  {r['path']}  next={r['next_review']}")
            if r["final_url"] and r["final_url"] != r["url"]:
                print(f"       -> {r['final_url']}")
        print(f"共 {len(results)} 条，异常 {bad} 条")
        if args.strict and bad:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
