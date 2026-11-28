# kb-tree 项目上下文

本文件记录 kb-tree 仓库的项目级约定，供在本仓库工作时读取；这些信息不放进全局记忆。

- 仓库：https://gitee.com/wingdever/kb-tree（公开）
- 主要维护子树：`trees/computer/ai/agent`
- 写作规范：`skills/kb-tree/SKILL.md`
- 新增节点：目录 + 同名 md + 四字段 front matter，配 `questions.jsonl` 与 `links.csv`
- 清单型节点：可加 `<节点名>.list.csv`，表头 `name,group,source,url,note`，一行一个条目
- 改完检查：`bash tools/check.sh`；单树检查用 `python3 skills/kb-tree/scripts/lint.py <树路径>`
- 外部来源：统一放文末 `## 参考资料`；官方条目写版本或日期，第三方写作者或机构
- 凭证：Gitee 凭证在仓库外 `~/.git-credentials`，不写入仓库、不打印明文

> 本文件只记项目约定，不记知识内容；知识内容仍由 `trees/` 下的节点承载。
