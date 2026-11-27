---
description: "GitHub, Inc. as a Microsoft subsidiary: no mainland China entity, cross-border billing in USD, and what that means for contracts, invoicing and access"
描述: "GitHub 的主体位置：微软全资子公司、中国大陆无运营法人、美元跨境结算，对合同、发票与访问的实际影响"
name: "GitHub, Inc."
名称: "GitHub（GitHub, Inc.）"
---

# GitHub（GitHub, Inc.）

GitHub 是一个品牌，也是一个独立法人：GitHub, Inc.，总部在旧金山。它在 2018 年被微软以股票交易方式整体收购，此后作为微软子公司独立运营，财报并入微软的智能云分部。它在中国大陆没有注册运营主体，也没有本地机房。

## 主体结构

| 项 | 内容 |
|---|---|
| 运营主体 | GitHub, Inc.，美国加利福尼亚州旧金山 |
| 上层持股 | Microsoft Corporation 全资持有，2018 年 10 月 25 日完成交割 |
| 交易对价 | 约 75 亿美元的股票对价，含已归属员工权益的现金支付与赔偿托管 |
| 财报归属 | 并入微软智能云分部（Intelligent Cloud） |
| 中国境内法人 | 无 |

"微软的子公司"不等于"微软签约"。GitHub 的付费订阅、企业合同与数据处理条款，相对方是 GitHub, Inc.，不是微软（中国）。

## 在中国大陆的实际状态

- **没有本地实体**：无境内注册公司、无 ICP 备案主体，因此不提供境内增值税发票，也没有境内投诉与监管对接窗口。
- **没有本地节点**：所有请求经跨境出口，晚高峰丢包与超时是常态，`raw.githubusercontent.com` 等子域更容易被单独限制。
- **不是全面封禁，但不稳定**：长期处于"能访问但时快时慢"的状态；偶发配置事故会造成更大范围的不可达。
- **一次典型事故**：2025 年 4 月 12 日至 13 日，一次配置变更导致未登录用户从中国访问失败，官方事后说明受影响比例约为匿名请求的 4%，随后回滚。
- **账号与数据**：账号体系、仓库数据、Actions 日志都存在境外，受美国法律与 GitHub 自身条款约束。

## 产品与主体的对应

- **代码托管、Pull Request、Issues、Pages、Actions、Packages**：由 GitHub, Inc. 提供，免费与付费额度按账号类型划分。
- **GitHub Copilot**：同为 GitHub 的产品线，订阅与计费在 GitHub 侧完成，模型能力来自多家供应商。
- **GitHub Enterprise Server**：可私有化部署在自己机房，代码不出境，但许可与支持合同仍与 GitHub, Inc. 签订。
- **GitHub Enterprise Cloud（ghe.com 等托管形态）**：数据在 GitHub 或其云基础设施上，跨境属性不变。
- **教育版与开源免费额度**：减免的是费用，不改变主体与数据位置。

## 对合作方的含义

- **合同相对方**：企业采购的相对方是 GitHub, Inc.；它没有境内法人可以替代签约。
- **付款与票据**：以美元计价，通过国际信用卡或对公跨境支付；拿到的是境外收据或发票，境内报销需财务提前确认。
- **数据合规**：个人信息与代码数据在境外处理，涉及个人信息出境的场景要单独评估，不能靠"反正在境外"回避申报义务。
- **服务连续性**：跨境链路与政策变化都会影响可用性，关键流水线应有镜像或自建备份方案。
- **争议解决**：适用美国法律与 GitHub 条款约定的管辖，跨境维权成本高。

## 怎么核实

1. 看订单与账单页面写的收款方全称，付费订阅的收款方是 GitHub, Inc.。
2. 看微软年报的并购披露与分部归属，确认 GitHub 的合并口径。
3. 查 GitHub 官方状态页的历史事故，判断"访问失败"是平台故障还是链路问题。
4. 企业采购把"签约主体、收款主体、数据存放地、争议管辖"四项写进合同评审表。

## 常见误区

- **以为微软账号等于 GitHub 账号**：两者账号体系独立，企业订阅也不通用。
- **以为在国内能开增值税发票**：没有境内主体，开不出境内发票。
- **把偶发不可达当成永久封禁**：多数是链路或配置问题，但也不能据此认为"稳定可用"。
- **用个人账号承载公司代码**：账号归属、审计与离职交接都会出问题，企业应使用组织账号。
- **忽略 Actions 的跨境依赖**：构建机在境外，拉取依赖与推送镜像都可能超时。

## 一句话主线

GitHub 的主体是"微软全资持有的美国公司、境内零法人"：**代码托管可以免费用，但合同、票据、数据位置和争议管辖都在境外**——它适合做开发协作，不适合被当成境内合规基础设施。

## 参考资料

- Microsoft 2018 年 12 月季度 10-Q（GitHub 收购对价与分部归属）：https://microsoft.gcs-web.com/static-files/88061c80-0a06-40d3-962f-ad6e6d0e4625
- 微软官方新闻稿：Microsoft to acquire GitHub for $7.5 billion：https://news.microsoft.com/en-my/2018/06/05/microsoft-to-acquire-github-for-7-5-billion/
- GitHub Status：中国未登录用户访问受阻事件报告：https://www.githubstatus.com/incidents/jfvgcls9swln
- GitHub 官方文档（计费、企业版与数据驻留说明入口）：https://docs.github.com
