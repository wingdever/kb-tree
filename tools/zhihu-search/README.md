# 知乎搜索（本机可用）

知乎开放平台的站内搜索接口，封装成一个命令行脚本，任何 Agent、定时任务或 shell 里都能直接调用。

## 一、先申请凭证（一次性，2 分钟）

1. 打开 `https://developer.zhihu.com`，用知乎账号注册登录。
2. 在「个人中心」申请新的 Access Secret，复制那串密钥。
3. 在知乎 App 内完成实名认证——没实名每天只有 10 次，实名后免费额度大幅提升。
4. 存到本机，二选一：

```bash
# 方式 A：写进配置文件（推荐，权限 600）
mkdir -p ~/.config/zhihu-search
printf '{"access_secret":"你的密钥"}\n' > ~/.config/zhihu-search/credentials.json
chmod 600 ~/.config/zhihu-search/credentials.json

# 方式 B：环境变量
export ZHIHU_ACCESS_SECRET="你的密钥"
```

匿名或未配置时脚本自动进入 `--mock` 模式，返回样例数据，链路可以先跑通。

## 二、用法

```bash
cd ~/Doubao/chats/38456041389940994/tools/zhihu-search

python3 zhihu_search.py "Agent 上下文工程怎么做"
python3 zhihu_search.py "RAG 切块粒度" --count 5
python3 zhihu_search.py "怎么理解 rag" --json        # 原始字段，便于二次处理
python3 zhihu_search.py --mock "任意关键词"           # 强制样例，验证流程
./zhihu --quota                                     # 查当天各接口已用/剩余
```

输出是人可读的标题、摘要、赞同数、评论数、作者与链接；`--json` 给管道用。

## 三、接口事实

| 项 | 值 |
|---|---|
| 端点 | `GET https://developer.zhihu.com/api/v1/content/zhihu_search` |
| 参数 | `Query`（必填，2-100 字）、`Count`（1-10，默认 10） |
| 鉴权 | 请求头 `Authorization: Bearer <Access Secret>` |
| 时间戳 | 请求头 `X-Request-Timestamp`，秒级 |
| 返回字段 | Title / ContentType / ContentID / ContentText / Url / VoteUpCount / CommentCount / AuthorName / EditTime / RankingScore |

额度按接口分池，各池独立计数、北京时间零点重置、不结转（2026-11 个人中心实测）：

| 接口 | 每日免费额度 |
|---|---|
| 知乎搜索 | 5,000 |
| 全网搜索 | 5,000 |
| 直答 | 100 |
| 热榜 | 100 |
| 问题发现 | 100 |
| 创作能力 | 500 |
| 知识库 | 500 |
| 小工具 | 10 |
| 知乎用户数据 | 10,000 |

额度是**每日**限免，不是每周，北京时间零点重置。

其中「小工具」只有两个接口：PDF 解析与 PPT 生成，额度 10 次；

未实名账号各接口每天只有 10 次；同账号下多个 Secret 共用份额度；超额按量计费（知乎搜索约 20 元/千次）。上线初期"每天 1000 次"是旧口径，别再照它规划。

## 四、错误码怎么读

这个接口有个坑：**出错时 HTTP 状态仍是 200**，真正的错误写在响应体的 `Code` / `Message` 里。实测无效密钥返回：

```json
{"Code":20001,"Message":"Authorization failed","Data":null}
```

脚本按 body 判定，不会把"鉴权失败"误报成"没搜到结果"：

- `Code 20001/20002`：Secret 无效、未实名或权限未开通。
- `Code 20003` 或 HTTP `429`：当日额度用完，等北京时间零点重置。
- 网络不可达：本机出网受限，换环境或稍后重试。

## 五、额度自查

```bash
./zhihu --quota          # 表格
./zhihu --quota --json   # 原始数组
```

走 `GET https://developer.zhihu.com/api/v1/quota`，返回 `TotalQuota` / `TotalUsed` / `RemainingQuota`，与个人中心同一套计数，调用本身不扣额度。

## 六、已验证

- `--mock` 模式：输出样例条目，链路正常。
- 假密钥真实请求：正确捕获 `Code 20001`，退出码 1，中文报错。
- 真实结果解析待你填入 Secret 后自测（字段映射按官方文档的 `Data.Items`）。

## 七、和全网搜索的区别

- `zhihu_search`：只搜知乎站内的问题、回答、文章，适合查经验贴、踩坑记录、真实使用感受。
- `global_search`：融合知乎与全网信源，适合查新闻与通用事实，`https://developer.zhihu.com/api/v1/content/global_search`。

需要时把 `API_URL` 换掉即可复用同一套鉴权逻辑。
