# ref-check

检查 `skills/kb-tree/references/review-queue.json` 中的引用是否可达，以及是否到了复查日期。它只做网络可达性检查，不判断内容是否仍然正确；到期项仍需人工对照原文。

## 用法

```bash
python3 tools/ref-check/ref_check.py
python3 tools/ref-check/ref_check.py --strict
python3 tools/ref-check/ref_check.py --json
```

- `OK`：HTTP 2xx/3xx，且未到复查日。
- `DUE`：可达，但已到 `next_review`，应人工核对内容与版本。
- `FAIL`：网络错误或 HTTP 4xx/5xx，需人工确认是否失效或被反爬拦截。
- `--strict`：出现 `DUE` 或 `FAIL` 时返回 1，可用于定期检查。

队列字段：`path` 指向节点目录，`label` 是引用说明，`url` 是原链接，`volatility` 是波动等级，`last_checked` 是上次人工核对日期，`next_review` 是下次复查日期。
