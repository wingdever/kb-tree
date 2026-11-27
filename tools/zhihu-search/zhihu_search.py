#!/usr/bin/env python3
"""知乎站内搜索（知乎开放平台 zhihu_search 接口）命令行封装。

凭证优先级：环境变量 ZHIHU_ACCESS_SECRET > ~/.config/zhihu-search/credentials.json
没有凭证时自动进入 --mock 模式（返回内置样例，方便验证流程），不会发真实请求。

用法：
    python3 zhihu_search.py "怎么理解 RAG 的切块"
    python3 zhihu_search.py "Agent 上下文工程" --count 5 --json
    python3 zhihu_search.py --mock "任意关键词"
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://developer.zhihu.com/api/v1/content/zhihu_search"
QUOTA_URL = "https://developer.zhihu.com/api/v1/quota"
CRED_PATH = os.path.expanduser("~/.config/zhihu-search/credentials.json")
TIMEOUT = 20
MAX_COUNT = 10  # 官方上限：单次最多 10 条

MOCK_ITEMS = [
    {
        "Title": "【样例】如何在 Agent 里做检索增强",
        "ContentType": "Answer",
        "ContentText": "这是 --mock 模式返回的样例数据，用于验证脚本链路，不代表真实搜索结果。",
        "Url": "https://www.zhihu.com/question/000000/answer/000000",
        "VoteUpCount": 0,
        "CommentCount": 0,
        "AuthorName": "mock",
    }
]


def load_secret():
    secret = os.environ.get("ZHIHU_ACCESS_SECRET", "").strip()
    if secret:
        return secret
    if os.path.exists(CRED_PATH):
        try:
            with open(CRED_PATH, encoding="utf-8") as f:
                return (json.load(f).get("access_secret") or "").strip()
        except (json.JSONDecodeError, OSError):
            return ""
    return ""


def search(query, count=10, secret=None):
    """调用官方接口，返回 items 列表。失败抛 RuntimeError。"""
    if not secret:
        raise RuntimeError("缺少 Access Secret：设置 ZHIHU_ACCESS_SECRET 或写入 " + CRED_PATH)
    count = max(1, min(int(count), MAX_COUNT))
    params = urllib.parse.urlencode({"Query": query, "Count": count})
    req = urllib.request.Request(
        API_URL + "?" + params,
        headers={
            "Authorization": "Bearer " + secret,
            "X-Request-Timestamp": str(int(time.time())),
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")[:200]
        if e.code == 401:
            raise RuntimeError("鉴权失败（401）：Access Secret 无效或未实名开通权限。%s" % body)
        if e.code == 429:
            raise RuntimeError("触发限流（429）：当日免费额度可能已用完，北京时间零点重置。%s" % body)
        raise RuntimeError("HTTP %s: %s" % (e.code, body))
    except urllib.error.URLError as e:
        raise RuntimeError("网络不可达：%s" % e.reason)

    # 接口在鉴权/额度出错时仍返回 HTTP 200，错误写在 body 的 Code/Message 里
    code = payload.get("Code", payload.get("code"))
    if code not in (None, 0, 200):
        msg = payload.get("Message") or payload.get("message") or "未知错误"
        if code in (20001, 20002, 401):
            raise RuntimeError("鉴权失败（Code %s：%s）：Access Secret 无效、未实名或权限未开通。" % (code, msg))
        if code in (20003, 429):
            raise RuntimeError("额度或限流问题（Code %s：%s）：当日免费额度可能已用完，北京时间零点重置。" % (code, msg))
        raise RuntimeError("接口返回错误（Code %s：%s）" % (code, msg))

    data = payload.get("Data") or payload.get("data") or {}
    items = data.get("Items") or data.get("items") or []
    return items


def fetch_quota(secret=None):
    """查询当日各接口额度：返回 [{APIID, APIName, TotalQuota, TotalUsed, RemainingQuota}]"""
    if not secret:
        raise RuntimeError("缺少 Access Secret：设置 ZHIHU_ACCESS_SECRET 或写入 " + CRED_PATH)
    req = urllib.request.Request(
        QUOTA_URL,
        headers={
            "Authorization": "Bearer " + secret,
            "X-Request-Timestamp": str(int(time.time())),
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s：%s" % (e.code, e.read().decode("utf-8", "ignore")[:200]))
    except urllib.error.URLError as e:
        raise RuntimeError("网络不可达：%s" % e.reason)
    if payload.get("Code") not in (0, 200):
        raise RuntimeError("接口返回错误（Code %s：%s）" % (payload.get("Code"), payload.get("Message")))
    return payload.get("Data") or []


def render_quota(rows):
    if not rows:
        return "没有拿到额度数据"
    lines = ["%-14s %-8s %-8s %-8s" % ("接口", "已用", "上限", "剩余")]
    for r in rows:
        lines.append("%-14s %-8s %-8s %-8s" % (
            r.get("APIName", "-"), r.get("TotalUsed", "-"),
            r.get("TotalQuota", "-"), r.get("RemainingQuota", "-")))
    return "\n".join(lines)


def strip_highlight(text):
    return (text or "").replace("<em>", "").replace("</em>", "").replace("<b>", "").replace("</b>", "")


def render(query, items):
    if not items:
        return "没有搜到结果：%s" % query
    lines = ["知乎搜索：%s（%d 条）" % (query, len(items))]
    for i, it in enumerate(items, 1):
        title = strip_highlight(it.get("Title"))
        snippet = strip_highlight(it.get("ContentText"))
        if len(snippet) > 160:
            snippet = snippet[:160] + "…"
        lines.append("%d. %s" % (i, title))
        if snippet:
            lines.append("   %s" % snippet)
        meta = "   %s｜赞同 %s｜评论 %s｜%s" % (
            it.get("ContentType", "-"),
            it.get("VoteUpCount", "-"),
            it.get("CommentCount", "-"),
            it.get("AuthorName", "-"),
        )
        lines.append(meta)
        if it.get("Url"):
            lines.append("   %s" % it["Url"])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="知乎站内搜索")
    ap.add_argument("query", nargs="?", help="搜索关键词")
    ap.add_argument("--count", type=int, default=10, help="返回条数，1-10，默认 10")
    ap.add_argument("--json", action="store_true", help="输出原始 JSON")
    ap.add_argument("--mock", action="store_true", help="强制使用样例数据，不发真实请求")
    ap.add_argument("--quota", action="store_true", help="查询当日各接口免费额度，不执行搜索")
    args = ap.parse_args()

    if args.quota:
        secret = load_secret()
        if not secret:
            print("缺少 Access Secret，无法查询额度。配置方法见 README.md", file=sys.stderr)
            return 1
        try:
            rows = fetch_quota(secret)
        except RuntimeError as e:
            print("查询失败：%s" % e, file=sys.stderr)
            return 1
        print(json.dumps(rows, ensure_ascii=False, indent=2) if args.json else render_quota(rows))
        return 0

    if not args.query:
        ap.print_help()
        return 2

    secret = "" if args.mock else load_secret()
    if not secret:
        print("[mock] 未检测到 Access Secret，使用样例数据。配置方法见 README.md", file=sys.stderr)
        items = MOCK_ITEMS
    else:
        try:
            items = search(args.query, args.count, secret)
        except RuntimeError as e:
            print("调用失败：%s" % e, file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(render(args.query, items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
