---
description: "Free domain options in 2026: platform subdomains, non-profit third-level domains like eu.org, dead free TLDs, and at-cost registrars"
描述: "免费域名还剩哪几类：平台子域、公益三级域、已停摆的免费顶级域、成本价注册商"
name: "Free Domains"
名称: "免费域名"
---

# 免费域名

"免费域名"在 2026 年只剩两类真实存在的东西：**别人根域下的三级域名**（`xxx.eu.org`、`xxx.duckdns.org`），和**平台随部署附赠的子域**（`xxx.workers.dev`）。真正的顶级域名（`.com`、`.net`）没有免费渠道，曾经的 Freenom 系（`.tk/.ml/.ga/.cf/.gq`）已经停摆。

判断一个免费域名能不能用，只看三件事：**谁持有根域**、**能不能自己管 NS**、**政策变了会不会一夜失效**。

## 第一类：平台附赠的子域

部署平台会给每个项目一个默认域名，零配置、自动 HTTPS，代价是名字里带着平台标识：

- Cloudflare Workers / Pages：`*.workers.dev`、`*.pages.dev`
- Vercel / Netlify：`*.vercel.app`、`*.netlify.app`
- GitHub Pages / GitLab Pages：`*.github.io`、`*.gitlab.io`

这类额度等于"绑定平台"，账号被封或项目删除，域名同时消失；也拿不到自有邮箱（`info@xxx.vercel.app` 不是你的）。适合做演示、预览、Webhook 回调地址，不适合当品牌入口。

## 第二类：公益组织发的三级域名

这是免费域名里唯一能"自己管 NS"的一档，因此可以托管到任意 DNS 商、甚至接 Cloudflare 免费档。

- **eu.org**：1996 年运营至今的志愿者项目，发放 `xxx.eu.org`，**永久免费、没有到期概念**，支持自定义 NS 与 DNSSEC<RichMediaReference>["https://nic.eu.org/"]</RichMediaReference>。人工审核，通常几天到几周；申请前填的 NS 必须已经能为该域名提供解析（会做区域检查）；直属子域只接受 4 个字符以上的名字；验证邮件常被 Gmail 拒收，要换邮箱<RichMediaReference>["https://bbs.huaweicloud.com/blogs/511987"]</RichMediaReference>。
- **deSEC（dedyn.io）**：德国非营利 DNS 托管，免费、原生 DNSSEC、有 REST API，适合 DDNS 与自动化<RichMediaReference>["https://desec.io/#!/en/product/anydns"]</RichMediaReference>。但官方页面已注明 `dedyn.io` 的注册**暂停**，只能先当 DNS 托管用，新子域要等恢复。
- **DuckDNS**：`xxx.duckdns.org`，免费动态 DNS，token 更新、可无限建子域、只有基础 A/AAAA 记录、不支持绑自有域名<RichMediaReference>["https://www.duckdns.org/about.jsp"]</RichMediaReference>。给家用宽带、NAS、自建服务做入口最省事。
- **pp.ua**：免费但**按年续期、每年要重新激活**，手机号有配额限制，当天可用<RichMediaReference>["https://bbs.huaweicloud.com/blogs/511987"]</RichMediaReference>。
- **us.kg / dpdns.org 等 DigitalPlat 系**：需 GitHub 授权验证，可改 NS 到 Cloudflare；这条来自二手整理，条款与审核口径要自己核。

## 第三类：免费顶级域名已经没有了

Freenom 的 `.tk/.ml/.ga/.cf/.gq` 曾是最有名的"免费真域名"，2026 年已彻底停摆，历史上出现过上千万域名一夜失效的先例。任何现在宣称"免费送 `.com`"的渠道，基本是首年促销或代持，第二年按原价续，且所有权不在你手上。

## 最接近免费的真域名：成本价注册商

如果目的只是"便宜"，而不是"零成本"，成本价注册商是更稳的答案：Cloudflare Registrar 按注册局批发价销售与续费，**不加价、无隐藏费用**，附送 WHOIS 隐私与一键 DNSSEC，但注册的域名必须使用 Cloudflare DNS<RichMediaReference>["https://www.cloudflare.com/pg/registrar-domain-registration/"]</RichMediaReference>。它把"域名"从年费陷阱变成了接近成本的基础设施开销，且和免费档的 CDN、Tunnel 天然同栈。

## 四个坑

1. **不能备案**：免费三级域与多数小众 ccTLD 没有境内实名通道，绑国内服务器开站会被驳回，只能配境外或香港节点。
2. **所有权不属于你**：holder 是公益组织或平台，条款一改就能收回；不要用免费域承载支付、登录、邮件这类核心链路。
3. **信任度与 SEO 折价**：`brand.eu.org`、`shop.vercel.app` 在商务场景里明显掉价，搜索引擎对共享根域也常连带降权。
4. **隐性存活条件**：eu.org 靠联系人信息有效与解析存活维持、pp.ua 每年要激活、平台子域跟着账号走——注册当天截图留证，并挂一个到期/可用性监测。

## 一句话主线

免费域名买到的不是"域名"，而是**别人的根域下的一段租期**：能自管 NS 的（eu.org、deSEC）适合当长期个人入口，平台附赠的适合当临时回调地址，真要做品牌就买成本价域名，别在免费域上押核心业务。

## 参考资料

- EU.org 官方站（1996 年起提供免费子域，可自定义 NS）：https://nic.eu.org/
- EU.org 申请实录（审核周期、4 字符限制、Gmail 收不到验证信、NS 需预先生效）：https://bbs.huaweicloud.com/blogs/511987
- deSEC 官网（免费 DNS 托管、原生 DNSSEC、dedyn.io 注册暂停）：https://desec.io/#!/en/product/anydns
- DuckDNS 官方说明（免费 DDNS、duckdns.org 子域）：https://www.duckdns.org/about.jsp
- 免费域名渠道盘点（Freenom 停摆、us.kg 等渠道与备案/所有权风险）：https://m.tech.china.com/articles/20260805/202608051933575.html
- 免费域名指南（eu.org、js.org、is-a.dev 等三级域与商业限制）：https://www.keydal.net/blog/free-domain-guide-2026
- Cloudflare Registrar 官方（按成本价注册与续费、必须用 Cloudflare DNS、免费 WHOIS 隐私）：https://www.cloudflare.com/pg/registrar-domain-registration/
