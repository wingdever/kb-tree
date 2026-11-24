# questions.jsonl 编写与校验规范

每个节点目录可放一份 `questions.jsonl`，把该节点能回答的问题列为机器可读的检索夹具。它是 C 层附属文件：不是知识节点，不套四字段 front matter，不计入"目录 + 同名 md"自检，跳过 md 相关校验。文件缺失合法，表示该节点未策展问题。

## 文件形态

- 文件名固定 `questions.jsonl`，每行一个 JSON 对象，空行跳过，空文件合法。
- 不用外层 `{"questions": [...]}` 包裹——文件名已表明它是问题清单。
- 字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `q` | string | 是 | 自然语言问题 |
| `section` | string | 是 | 答案所在小节，逐字匹配同级同名 md 的 H2/H3 标题文本 |
| `role` | string | 否 | `primary`（默认）或 `perspective` |
| `aliases` | string[] | 否 | 同义问法 |
| `owner` | string | `perspective` 时必填 | 主宿主目录的相对路径 |

## 规则

1. `section` 必须逐字匹配同级同名 md 的 H2/H3 标题文本，不用 slug；标题改名后由校验脚本发现。
2. 同一问题（去除标点、归一空白后比较）在整棵树里最多一个 `primary`，其余必须是 `perspective` 并给出 `owner`。
3. `owner` 指向该问题主宿主的目录，用相对路径；它是容器层引用，不算知识交叉引用。
4. 问题是真实查询，不是标题改写；看标题即可回答的问题不要收录。
5. 全局检索索引由脚本遍历所有 `questions.jsonl` 生成，不另建 index 文件。

## 校验脚本（可直接用）

```python
import os, re, json, glob

def norm(q):
    return re.sub(r'[\s，。？！、,.\?!]+', '', q).lower()

files = sorted(glob.glob('**/questions.jsonl', recursive=True))
primary = {}
problems = []
for fp in files:
    d = os.path.dirname(fp)
    md = os.path.join(d, os.path.basename(d) + '.md')
    headings = set()
    if os.path.exists(md):
        text = open(md, encoding='utf-8').read()
        headings = {m.group(1).strip() for m in re.finditer(r'^#{2,3}\s+(.+)$', text, re.M)}
    for lineno, line in enumerate(open(fp, encoding='utf-8'), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as e:
            problems.append((fp, lineno, f'bad json: {e}'))
            continue
        if not isinstance(item, dict):
            problems.append((fp, lineno, 'not an object'))
            continue
        for k in ('q', 'section'):
            if not isinstance(item.get(k), str) or not item[k].strip():
                problems.append((fp, lineno, f'missing {k}'))
        role = item.get('role', 'primary')
        if role not in ('primary', 'perspective'):
            problems.append((fp, lineno, f'bad role: {role}'))
        if role == 'perspective' and not item.get('owner'):
            problems.append((fp, lineno, 'perspective without owner'))
        if item.get('section') and item['section'] not in headings:
            problems.append((fp, lineno, f'section not found: {item["section"]}'))
        owner = item.get('owner')
        if owner and not os.path.exists(os.path.normpath(os.path.join(d, owner))):
            problems.append((fp, lineno, f'owner missing: {owner}'))
        if role == 'primary' and isinstance(item.get('q'), str):
            key = norm(item['q'])
            if key in primary:
                problems.append((fp, lineno, f'duplicate primary: {primary[key]}'))
            else:
                primary[key] = f'{fp}:{lineno}'
print(f'files={len(files)} problems={len(problems)}')
for p in problems:
    print(' ', p)
```
