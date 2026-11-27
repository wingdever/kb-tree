---
description: "Free CI and cloud dev quotas: GitHub Actions 2,000 minutes, GitLab 400 minutes, Codespaces 120 core-hours and 15GB storage"
描述: "免费 CI/CD 与云端开发环境：分钟数、core-hours、存储三种计费单位"
name: "Free CI & Cloud Dev"
名称: "免费 CI/CD 与云端开发"
---

# 免费 CI/CD 与云端开发

这条线的免费额度用三种完全不同的单位计量，换算前要先分清：

- **CI 分钟**：跑流水线的时间，按分钟累计。
- **core-hours**：云端开发环境按"核数 × 小时"扣，2 核跑 1 小时 = 2 core-hours。
- **存储**：仓库、制品、开发环境磁盘，按月占用量计。

同样是"免费 60 小时"，在 2 核机器上就是 120 core-hours；开 8 核只够 15 小时。核数选错，额度消耗速度差四倍。

## GitHub：CI 与云端环境

**GitHub Actions** 免费档每月 2,000 分钟，**公开仓库不计分钟**；私有仓库超出后按分钟计费<RichMediaReference>["http://raw.githubusercontent.com/api-evangelist/github-actions/refs/heads/main/plans/github-actions-plans-pricing.yml"]</RichMediaReference>。对个人项目来说，把仓库设为公开是最直接的省钱手段——开源项目的 CI 基本等于无限。

**Codespaces** 给个人的免费额度是**每月 120 core-hours**（即 2 核机器跑 60 小时）+ **15GB 存储**<RichMediaReference>["http://pullreminders.com/features/codespaces"]</RichMediaReference>。它的计费细节值得注意：环境**闲置 30 分钟自动暂停**，暂停后不再扣 core-hours，所以"开着不用"不会持续烧额度<RichMediaReference>["https://learn.microsoft.com/en-in/copilot/employee-self-service/get-started-codespaces"]</RichMediaReference>。

按核数换算：2 核 60 小时、4 核 30 小时、8 核 15 小时。写代码、改配置用 2 核足够；只有编译大项目或跑容器编排才需要往上加。

## GitLab：CI 分钟更少，但公开项目有额外通道

GitLab.com 免费档每月 **400 计算分钟**，每个项目 10 GiB 存储（Git 仓库与 LFS 合计），私有顶级群组限 5 人<RichMediaReference>["http://www.shturl.cc/de56e50529789f51869c4c50cf08183b"]</RichMediaReference>。400 分钟大约是"每天跑两三次、每次几分钟"的量，跑一次超过 10 分钟的流水线很快就会见底。

开源项目、教育机构与符合条件的初创可以申请额外额度（口径为每月 50,000 分钟），这是 GitLab 免费档之外的一条正式通道。

## 怎么组合

| 需求 | 方案 |
|---|---|
| 公开项目跑 CI | GitHub Actions（公开仓库不计分钟） |
| 私有小项目跑测试 | GitHub Actions 2,000 分钟 + GitLab 400 分钟双账号 |
| 需要浏览器里的完整 IDE | Codespaces 2 核 + 15GB，闲置自动暂停 |
| 需要固定算力跑长任务 | 自建 runner（用自己的机器，平台不收分钟费） |

自建 runner 是另一条路：GitHub 与 GitLab 都允许把自己的机器挂成 runner，平台侧不扣分钟，成本变成"你自己的电和机器"。对小团队来说，一台闲置的旧笔记本就够。

## 四个坑

1. **核数决定消耗速度**：Codespaces 的 120 core-hours 在 8 核机器上只有 15 小时，默认别选大机型。
2. **公开与私有的差别极大**：Actions 公开仓库不计分钟，私有仓库按月限流；把能开源的仓库开源，是最省额度的操作。
3. **存储单独计**：Codespaces 15GB、GitLab 10GiB 都是独立上限，开发环境里塞满依赖或模型，会先撞存储而不是算力。
4. **CI 分钟不是墙钟时间**：排队、拉镜像、缓存未命中的时间都会计入，优化缓存比换平台更有效。

## 一句话主线

免费 CI/CD 的核心是**"公开换额度、小核换时长、自建换上限"**：能开源的仓库开源，开发环境选最小核数，长期跑重活就挂自己的 runner。

## 参考资料

- GitHub Actions 免费额度（私有仓库 2,000 分钟/月、公开仓库不计分钟）：http://raw.githubusercontent.com/api-evangelist/github-actions/refs/heads/main/plans/github-actions-plans-pricing.yml
- GitHub Codespaces 免费额度（120 core-hours、15GB 存储、按核数折算）：http://pullreminders.com/features/codespaces
- Codespaces 闲置 30 分钟自动暂停：https://learn.microsoft.com/en-in/copilot/employee-self-service/get-started-codespaces
- GitLab 免费档（400 计算分钟/月、10 GiB 存储、私有群组 5 人）：http://www.shturl.cc/de56e50529789f51869c4c50cf08183b
