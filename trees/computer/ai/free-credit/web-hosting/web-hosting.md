---
description: "Free hosting beyond Python PaaS: Vercel Hobby 100GB and 1M invocations, Netlify 100GB and 300 build minutes, Oracle Always Free ARM VM"
描述: "除 Python 托管之外的免费 hosting：静态站、前端平台、边缘函数与真机"
name: "Free Web Hosting"
名称: "免费 Web 托管"
---

# 免费 Web 托管

"Hosting" 这个词下面其实是四种完全不同的东西，混着比价必然错位：

- **静态站托管**：只发 HTML/CSS/JS，带宽与构建次数是主要额度。
- **前端平台 + Serverless**：静态资源加函数，函数按调用次数与 CPU 小时计。
- **边缘函数**：请求直接跑在 CDN 节点上，按请求数与 CPU 毫秒计。
- **虚拟机 / 容器**：给你一台真机，按核数与月流量计，是唯一能跑常驻进程的一类。

只想放个页面，前三类都够；要跑常驻 Agent、定时任务、数据库，只有第四类成立。

## 静态站与前端平台

**Vercel Hobby**（免费）：每月 **100GB 快速数据传输、100 万次函数调用、4 CPU 小时活跃 CPU、360 GB 小时预置内存、100 万次 CDN 请求**，单次构建上限 45 分钟、每天最多 100 次部署。两条容易忽略的条款：Hobby **仅限个人、非商业用途**；超出额度后不是扣费，而是**整个账号被暂停**，等 30 天才能恢复。

**Netlify Free**：约 100GB 带宽、300 构建分钟/月、12.5 万次函数请求、最多 500 个站点，允许商用，带表单与 Identity 的免费额度——这组数字来自第三方对比，接入前回官方定价页核对。

**Cloudflare Pages**：静态资源带宽不计量，这点和上面两家有本质差别——流量高峰不会变成账单；构建次数有月上限（第三方口径 500 次/月）。如果站点是纯静态且可能被突然推爆，这是最省心的一档。

## Git 平台自带的两层托管

"Git 账号有没有云托管"要分成两层看：**仓库本身就在云上**，另外还附赠一个**静态站点托管**。

- **代码托管**：GitHub 个人免费账号可建无限私有仓库（仓库建议 1GB 以内、单文件硬限 100MB）；Gitee 个人免费、私有仓库免费，免费版总仓库 5GB、单仓库 ≤500MB、单文件 ≤50MB；GitLab 免费档每项目 10GiB 存储。
- **静态站点**：三家都送 Pages。GitHub Pages 站点 ≤1GB、带宽软限 100GB/月、10 次构建/小时（改用自定义 Actions 构建则不受此限）、单次部署 10 分钟超时；**条款明确禁止把它当免费商用托管或 SaaS**，定位是个人与组织项目展示；只发静态文件，不支持 PHP/Python 这类服务端语言。GitLab Pages 免费、带 `*.gitlab.io` 与自定义域名，构建吃掉每月 400 CI 分钟。Gitee Pages 免费、支持 Jekyll/Hugo/Hexo，国内访问比 GitHub 稳。

所以答案是：**有，但只到"静态站"这一层**。要 API、要常驻进程、要数据库，Pages 给不了，得另配函数或真机。

## 通用 PaaS

以"实例小时"计费的 PaaS（例如 Render 那一类）适合"前后端 + 数据库一起试"，但额度按 workspace 每月发，一台服务 24 小时常驻就能吃光整月配额，且免费数据库会到期。它们的共同定位是**验证与演示**，不是长期生产。

## 真机：Oracle Always Free

这是主流云里唯一长期免费给**真虚拟机**的：每个租户 **2 台 AMD 微实例（各 1/8 OCPU、1GB 内存）**，外加 **ARM Ampere A1 共 2 OCPU / 12GB 内存**（可拆成 1 台或 2 台），按月给 **1,500 OCPU 小时 + 9,000 GB 小时**，配 **200GB 块存储**与 2 个 Autonomous Database。

必须知道的两件事：

- **额度被悄悄减半过**。2026 年 6 月，ARM 从 4 OCPU / 24GB 降到 2 OCPU / 12GB，官方文档现在的口径就是"相当于 2 OCPU、12GB"，旧教程里的 4/24 已经过时。
- **闲置会被回收**。长期没有负载的实例可能被回收，注册验证也以"难过"著称；想长期持有就得让它真的跑点东西。

它对 Agent 项目的价值很直接：一台 2 核 12GB 的 ARM 机器，足够跑常驻进程、自建 Postgres、挂 Cloudflare Tunnel 当入口，是"零成本常驻"唯一现实的选项。

## 谁能开通：三道门槛

Always Free 是"免费且无期限"，但不等于"谁都能开"。注册要过三关：

1. **主区域（home region）**。官方口径是"仅在提供商业 OCI 服务的区域开放"，而 OCI 的公开区域列表里没有中国大陆；注册时选不到大陆作为主区域，账号就建不起来。这是最根本的一道门。
2. **手机号验证**。多数账号需要一个可接收验证码的手机号，大陆号码在实际注册中经常收不到或被拒。
3. **信用卡/借记卡验证**。官方明确接受"像信用卡一样使用的借记卡"，但**不接受带 PIN 的借记卡、虚拟卡、一次性卡、预付卡**；验证时会有一笔临时冻结，通常 3–5 个工作日释放。

还有三条硬规则：每人只允许一个账号（禁止重复注册）、联系与开单信息必须"准确、有效、经同意使用"、**闲置 30 天以上可能被判定为废弃并暂停或终止**。

所以实际结论是：**有真实海外主体、海外手机号与实体卡的人可以长期白嫖这台 2C12G 的 ARM 机器；大陆个人用户基本开不出来**。用他人身份或虚构地址去注册属于违反服务条款，风险是封号加数据删除，不值得。

## 怎么选

| 需求 | 方案 |
|---|---|
| 纯静态博客/文档站 | Cloudflare Pages（带宽不计量） |
| 想跟代码放一起 | GitHub Pages / Gitee Pages（仅静态、禁商用托管） |
| Next.js 全栈、个人非商业 | Vercel Hobby |
| 要商用、要表单 | Netlify Free |
| 前后端 + 数据库快速验证 | 实例小时型 PaaS |
| 要常驻进程、要真机 | Oracle Always Free（ARM 2C12G，但需海外主体与实体卡） |

## 五个坑

1. **Hobby 禁商用**：Vercel 免费档写明个人/非商业用途，公司项目挂上去属于违反条款。
2. **100GB 比想象中薄**：按每页 1MB 算，10 万次浏览就接近上限；Vercel 与 Netlify 都会因此停服。
3. **免费额度会悄悄改**：Oracle 的 ARM 从 4C24G 减到 2C12G，旧教程照抄会低估风险。
4. **免费数据库有寿命**：PaaS 附赠的库通常 30 天到期，数据要外置。
5. **静态托管跑不了后台**：没有常驻进程、没有 cron、没有持久磁盘，Agent 的长任务必须换真机。

## 一句话主线

免费托管的选型顺序是**"先分清要静态还是要进程"**：静态站看带宽（Cloudflare 不计量最稳），前端全栈看调用数与商用条款（Vercel 便宜但限个人），要常驻就只有真机一条路（Oracle 的 ARM 实例是主流云里唯一的长期免费选项）。

## 参考资料

- Vercel Hobby 额度（100GB、100 万调用、4 CPU 小时、360 GB 小时）：https://vercel.com/docs/plans/hobby
- Vercel 计划说明（Hobby 超限暂停、Pro 起价）：https://vercel.com/docs/plans
- Vercel 限额（构建 45 分钟、每天 100 次部署、100 次/小时）：https://vercel.com/docs/limits
- Vercel 与 Netlify 免费档对比（Netlify 100GB/300 分钟/12.5 万请求、商用许可）：https://www.productsrelay.com/blog/vercel-vs-netlify-free-tier
- Vercel / Netlify / Cloudflare Pages 三方对比（带宽与构建口径）：https://gocodelab.com/en/blog/en-vercel-vs-netlify-vs-cloudflare-pages-2026
- Oracle Cloud 免费套餐（2 台 AMD 微实例、ARM 2 OCPU/12GB、200GB 块存储、2 个 Autonomous DB）：https://www.oracle.com/cn/cloud/free/?t=62s
- Oracle Always Free 文档（1,500 OCPU 小时 + 9,000 GB 小时、启动卷最小 47GB）：https://docs.oracle.com/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Oracle 2026-06 把 ARM 额度从 4 OCPU/24GB 减半（闲置回收与注册验证）：https://prodogon.com/blog/devops/deploy-free-app-oracle/
- Oracle 免费套餐 FAQ（仅商业 OCI 区域开放、需手机号与信用卡、每人一个账号、闲置 30 天可回收）：https://www.oracle.com/ca-en/cloud/free/faq/
- Oracle 官方文档（注册需手机号与信用卡、Always Free 只在 home region 发放）：https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- GitHub Pages 限额（站点 1GB、带宽 100GB/月、构建 10 次/小时、部署 10 分钟超时）：https://techie-joe.github.io/library/github-pages/
- GitHub Pages 条款（禁止当免费商用托管/SaaS、只发静态页）：https://convika.com/ar/compare/github-pages-commercial-use/
- GitLab Pages 文档（免费、自动 CI/CD 部署、自定义域名）：https://gitlab.com/gitlab-org/gitlab-foss/-/tree/master/doc/user/project/pages
- GitLab 免费档存储（每项目 10GiB）：https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/storage_usage_quotas.md
- Gitee 个人免费与 Pages（私有仓库免费、5GB 仓库、静态托管）：https://gitee.com/indexpage
