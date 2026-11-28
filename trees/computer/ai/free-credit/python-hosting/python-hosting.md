---
description: "Free Python hosting quotas: PythonAnywhere 100 CPU-seconds/day and 512MiB, Render 750 instance hours, Streamlit 2.7GB, HF Spaces 2 vCPU/16GB"
描述: "免费 Python 托管与 PaaS 额度：CPU-秒、实例小时、资源上限三种计量"
name: "Free Python Hosting"
名称: "免费 Python 托管"
---

# 免费 Python 托管

免费跑一个 Python 服务，额度有四种完全不同的给法：

- **CPU-秒配额**：只算真正占用的处理器时间，墙钟时间不算。PythonAnywhere 是这种。
- **实例小时**：算"服务醒着的小时数"，睡着的时段不扣。Render 是这种。
- **资源上限**：给固定的 CPU/内存/磁盘，跑多久都行但资源就那么多。Streamlit、Hugging Face Spaces 是这种。
- **免费硬件档**：给一档固定的机器规格，超出要换付费档。

这四类里，**只有"实例小时"会因为 24 小时常驻而被吃光**——750 小时对 31 天的月份（744 小时）刚好只够一台服务全月开着。

## PythonAnywhere：CPU-秒按天算

Beginner 免费档，不用绑卡：**1 个 web 应用**（只能跑在 `yourname.pythonanywhere.com` 子域）、**512MiB 磁盘**、**每天 100 CPU-秒**、**2 个控制台**。

几条与直觉相反的规则：

- 那 100 CPU-秒**只算控制台、定时任务、常驻任务，不算 web 应用**；web 应用有独立配额。所以"网页能跑"不代表"脚本能跑"。
- 超额后进程进 **tarpit**（低优先级继续跑），不会立刻被杀，但被判定影响他人时可能被终止。
- **出网走白名单**：免费账号只能访问约 6,500 个允许的站点（含 `api.openai.com`、`api.stripe.com`）。接自建 API、冷门第三方服务会直接连不上，这是最容易踩的一条。
- **闲置会过期**：免费 web 应用 1 个月没人登录续期就停止，2026 年 1 月起从 3 个月缩短到 1 个月。
- 免费档**没有自定义域名、没有 SSH、没有定时任务、没有 MySQL**（2026-01-15 之后注册的账号）。

它适合"一个 Flask/Django 小站 + 两个控制台调脚本"，不适合当常驻 Agent 的运行时。

## Render：实例小时按 workspace 算

Free 档：**0.1 CPU / 512MB RAM / 1 实例**，**每个 workspace 每月 750 实例小时**，附 100GB 出网带宽与 500 构建分钟。

关键细节：

- **闲置 15 分钟自动休眠**，下次请求约 1 分钟冷启动；休眠期间不扣实例小时。
- 750 小时 × 12 个月折算下来，**一台服务 24 小时常驻就刚好用完全部额度**，第二台一开就超额；超额后所有免费服务一起被挂起，等下月 1 日重置。
- 免费 Postgres **1GB、创建 30 天后到期**，再有 14 天宽限期，之后连数据一起删。
- **文件系统是临时的**：每次休眠/重启，写在磁盘上的上传文件、SQLite 库都会丢。

## 展示型：Streamlit 与 Hugging Face Spaces

这两个不是通用 PaaS，更像"把脚本变成网页"的托管：

- **Streamlit Community Cloud**：免费，资源上限约 **2 核 CPU / 2.7GB RAM / 50GB 存储**（0.078 核、690MB 起），**连续 7 天无访问自动休眠**，访问即唤醒。超限时页面直接显示"🤯 超出资源限制"。
- **Hugging Face Spaces**：CPU Basic 档免费，**2 vCPU / 16GB RAM / 50GB 临时磁盘**，免费硬件闲置约 48 小时后休眠；升级到 GPU 档按小时计费（T4 约 $0.60/小时）。

它们的共同优势是**不用管服务器**，把仓库一连就出公网地址；共同代价是**资源上限硬、休眠频繁、不能跑常驻后台任务**。

## 怎么选

| 需求 | 方案 |
|---|---|
| 一个 Flask/Django 小站 | PythonAnywhere（注意出网白名单） |
| 前后端 + 数据库一起试 | Render（注意 750 小时与数据库 30 天） |
| 数据分析看板、Demo 页 | Streamlit Community Cloud |
| 模型 Demo、Gradio 界面 | Hugging Face Spaces |
| 要常驻后台、要 cron | 都不合适，用一台便宜的 VPS |

## 五个坑

1. **额度计量单位不一样**：CPU-秒只算计算时间，实例小时算醒着的时间，资源上限根本不计时——按"能不能 24 小时常驻"先筛一遍。
2. **文件系统是临时的**：Render 与 Spaces 重启即清空，SQLite、上传文件必须外置到对象存储或托管数据库。
3. **免费数据库会过期**：Render 的 Postgres 30 天即到期，别把唯一一份数据放进去。
4. **出网可能被限制**：PythonAnywhere 免费档走白名单，调第三方 API 前先确认域名在名单里。
5. **闲置会被回收**：PythonAnywhere 1 个月不续期就停、Streamlit 7 天休眠、Spaces 48 小时休眠，演示前记得先唤醒。

## 一句话主线

免费 Python 托管的本质是**"用闲置回收换零成本"**：给得起的额度都假设你不会 24 小时常驻，一旦要常驻（尤其 Render 的 750 小时），免费档就会立刻见底。

## 参考资料

- PythonAnywhere 定价（Beginner 免费档：1 个应用、512MiB、100 CPU-秒/天、2 控制台）：https://www.pythonanywhere.com/pricing/
- PythonAnywhere 磁盘配额（免费账号 512MiB）：https://help.pythonanywhere.com/pages/DiskQuota
- PythonAnywhere 免费档细节（CPU-秒只算控制台/定时任务、出网白名单、1 个月过期）：https://agentdeals.dev/vendor/pythonanywhere
- Render Deploy for Free（750 实例小时、0.1 CPU/512MB、15 分钟休眠）：https://render.com/docs/free
- Render 免费档实测（750 小时≈一台常驻、临时文件系统、数据库 30 天到期）：https://justinmckelvey.com/blog/is-render-free
- Streamlit Community Cloud 资源上限（2 核/2.7GB/50GB、7 天休眠）：https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
- Hugging Face Spaces 硬件（CPU Basic 免费 2 vCPU/16GB/50GB、GPU 按小时）：https://huggingface.com/docs/hub/spaces-overview
- 免费托管横向对比（各家的休眠与额度口径汇总）：https://snapdeploy.dev/state-of-free-hosting
