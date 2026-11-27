---
description: "Free image and file storage: Qiniu 10GB monthly, Tencent COS 50GB for 6 months, Alibaba OSS 20GB for 3 months, GitHub LFS 10GiB, public image hosts"
描述: "免费图片与文件存储的额度边界：对象存储、仓库当图床、公共图床"
name: "Free Image & File Storage"
名称: "免费图片与文件存储"
---

# 免费图片与文件存储

图床和文件存储是两件不同的事，混着选最容易踩坑：

- **对象存储**：自己拿桶 + 自己绑 CDN，图片、附件、备份都能放，额度按"存储容量 + 流量 + 请求数"三项分别计。
- **公共图床**：把图传上去换一个外链，省事但不可控，免费档常常没有稳定直链。
- **仓库当图床**：把图片提交进 Git 仓库，靠 Pages 或 CDN 分发，适合博客与文档站。

判断一个免费额度能不能用，关键是看它**抵不抵流量**。国内对象存储的免费包通常只抵存储容量，访问产生的下行流量要另买。

## 国内对象存储的免费额度

| 平台 | 免费额度 | 有效期 | 只抵什么 |
|---|---|---|---|
| 七牛云 | 标准存储 10GB/月、CDN 回源 10GB/月、PUT/DELETE 10 万次/月、GET 100 万次/月，图片处理 10TB/月 | 每月自动发放，不结转 | 存储、回源流量、请求；外网流出流量无免费额度<RichMediaReference>["https://developer.qiniu.com/af/12968/freequota"]</RichMediaReference> |
| 腾讯云 COS | 个人 50GB、企业 1TB 标准存储 | 6 个月（180 天） | 仅标准存储容量；流量与请求需另购<RichMediaReference>["https://cloud.tencent.com/document/product/436/6240"]</RichMediaReference> |
| 阿里云 OSS | 20GB 标准存储 + 2GB 外网流出 + 20 万次请求 | 3 个月 | 仅标准存储（本地冗余）、外网流量、请求；图片处理不抵<RichMediaReference>["https://help.aliyun.com/zh/oss/free-quota-for-new-users"]</RichMediaReference> |

三家的差别在"续不续"：七牛是**每月重置的长期免费**，适合长期放着的小站点；腾讯和阿里是**一次性试用包**，到期后全部按量计费，测试完要么删桶要么付费。阿里在部分海外地域还能叠加每月 5GB，试用期内合计约 25GB/月。

## 仓库当图床

把图片放进 Git 仓库、用 Pages 或 CDN 分发，是零成本方案里最稳的一种，因为带宽由托管方出：

- GitHub Pages 对公开仓库的静态资源不限流量，适合博客配图与文档截图。
- 大文件走 Git LFS：GitHub Free/Pro 自带 **10 GiB 存储 + 10 GiB 下载带宽/月**，单文件上限 2 GB；Team 与 Enterprise 是 250 GiB<RichMediaReference>["https://techdows.com/download-git-lfs-for-pc-windows-11-10-mac.html"]</RichMediaReference>。注意普通 Git 仓库单文件硬上限 100 MB，超过就必须走 LFS。
- LFS 超出免费额度且预算上限设为 0 时，当月 LFS 操作会被直接阻断，不会偷偷扣费——这算是比较友好的失败方式。

仓库当图床的代价是**图片进了版本历史就删不掉**（除非重写历史），所以只适合放"一次定稿"的素材，不适合频繁替换的图。

## 公共图床

公共图床的免费档普遍存在一个隐性降级：**免费能上传，但直链与 API 被划进付费档**。以 ImgBB 为例，免费档单张上限 32 MB，而"直链（Direct Linking）"和"API Access"列在 Pro 权益里<RichMediaReference>["https://ibb.co"]</RichMediaReference>。这意味着程序化上传、稳定外链这些真正有用的能力，免费档可能拿不到。

公共图床的固有风险还有三条：图片可能因政策或长期无人访问被清理、外链有防盗链与 Referer 限制、服务关停时全部链接同时失效。所以它只适合临时分享，不适合当 Agent 产物的长期存储。

## 怎么选

- **博客/文档站的图**：仓库 + Pages 最省事，量大了再迁对象存储。
- **Agent 产出物（截图、PDF、音频）**：对象存储的免费包 + 自己的域名，别用公共图床。
- **纯临时分享**：公共图床，传完即弃，别写进正式文档。
- **长期沉淀**：挑"每月重置"的那一档（七牛这类），或者直接按量付费，成本比想象低。

## 四个坑

1. **免费包只抵存储**：腾讯 50GB 和阿里 20GB 都不含下行流量与请求，图被访问得多时，账单出在流量上而不是容量上。
2. **请求数单独计**：对象存储按 GET/PUT 次数收费，小文件多、刷新频繁的站点容易先撞请求额度。
3. **公共图床不给直链**：免费档拿不到稳定外链，程序化上传还可能要付费开 API。
4. **仓库体积不可逆**：图片一旦提交就进历史，10 GiB 的 LFS 额度用完只能清理或付费，删图也省不回容量。

## 一句话主线

免费存储的核心不是"给多少 GB"，而是**"存储免费、流量另算、请求另算"**：能长期用的只有每月重置的额度，一次性试用包适合验证方案，公共图床只适合临时分享。

## 参考资料

- 七牛云免费额度（10GB 存储/月、10GB 回源、PUT 10 万、GET 100 万、图片处理 10TB/月）：https://developer.qiniu.com/af/12968/freequota
- 七牛云免费额度须知（各项额度与超额计费方式）：https://developer.qiniu.com/af/kb/1574/free-credit-information?category=kb
- 腾讯云 COS 免费额度（个人 50GB、企业 1TB、6 个月，仅标准存储）：https://cloud.tencent.com/document/product/436/6240
- 腾讯云 COS 计费 FAQ（免费包不抵流量与请求）：https://cloud.tencent.com/document/faq/436/30747
- 阿里云 OSS 新用户免费试用（20GB/3 个月、2GB 外网流量、20 万请求）：https://help.aliyun.com/zh/oss/free-quota-for-new-users
- GitHub Free/Pro 的 LFS 额度与单文件上限（10 GiB 存储 + 10 GiB 带宽、单文件 2 GB）：https://techdows.com/download-git-lfs-for-pc-windows-11-10-mac.html
- ImgBB 免费图床（32 MB/张，直链与 API 属 Pro 权益）：https://ibb.co
- ImgBB API 文档（上传接口与 32 MB 限制）：https://www.api.imgbb.com/
