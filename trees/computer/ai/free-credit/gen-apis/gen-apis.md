---
description: "Free quotas for generative media APIs: 100 images per model, unlimited TTS for a 3-month trial at 2 concurrency, and why per-image pricing is scarce"
描述: "生成型免费 API：图像生成按张、语音合成按字符与时长，试用期与并发限制"
name: "Free Generation APIs"
名称: "生成型免费 API"
---

# 生成型免费 API

图像生成与语音合成属于"从零造内容"的接口，免费额度的形态和对话模型完全不同：不是送多少 token，而是**送多少张图、多少秒音频、多少字符**。额度普遍给得小气，原因是单次推理成本高——生成一张图要跑完整的扩散/自回归过程，合成一段语音要跑声学模型与声码器。

## 额度按什么单位给

| 模态 | 常见单位 | 平台典型做法 |
|---|---|---|
| 图像 | 张 | 每模型 100 张，一次性或按活动发放 |
| 视频 | 秒 | 数十秒到千余秒，随活动 |
| 语音合成 | 字符、请求次数、时长 | 试用期内不限量但限并发，或每月固定字符 |
| 语音识别 | 秒/小时 | 见识别类额度，按语音段计 |

换算时注意：图像按"张"、语音按"字符"，两者之间没有统一汇率；只有跨模态的模型（如把音频折算成 token 计费的语音大模型）才需要按 token 换算。

## 图像生成

阿里云百炼的免费额度里，图像和文本是两套口径：

- 文本类：每模型约 100 万 token，90 天。
- 图像类：`qwen-image` 系列**每个模型 100 张**，覆盖文生图、图生图、图像编辑。
- 视频类：Wan 系列约 1,650 秒，可用于文生视频、图生视频、参考生视频。

这三项与文本额度同属"开通即自动发放"的新人包，但**彼此独立**，不会互相抵扣；100 张的定位是"够把海报、商品图、广告创意各试一轮"，不够做素材批量生产。

边缘平台是另一条路：Cloudflare Workers AI 每天 10,000 Neurons 的免费额度同样覆盖文生图模型，按每张图的神经元消耗折算，张数取决于所选模型；好处是每天重置、不需要新用户资格，坏处是模型清单与效果要自己挑。

**警惕"无限免费"**：社区里流传的若干"无需注册、无水印、无限生成"站点，多数没有公开配额与条款，属于预览期或限速服务，不能进生产规划；判断标准是能否查到明确的额度页与计费单价。

## 语音合成（TTS）

阿里云智能语音交互的试用版是当前最宽松的一档：

- 新用户开通后可免费试用 3 个月，语音合成在试用期内**调用量不限**，并发限制为 2<RichMediaReference>["https://help.aliyun.com/zh/isi/getting-started/user-guide-for-non-developers"]</RichMediaReference>。
- 单次请求最多 300 字符（汉字、字母、标点各算 1 个），超出截断——长文要自己切片再拼接。
- 流式文本语音合成（CosyVoice 大模型）**不支持试用**，要商用版才能用<RichMediaReference>["https://help.aliyun.com/zh/isi/product-overview/faq-about-concurrency-and-monitoring"]</RichMediaReference>。
- 试用期内若升级商用再降回试用，并发会被置为 0，服务直接不可用，这个操作不可逆。

海外平台的额度按字符/月计，社区整理的常见口径是：Azure 语音每月数十万字符免费，Google 标准音色每月约 400 万字符、WaveNet 音色约 100 万字符——**这些数字来自第三方整理，接入前要回官方定价页核对**，且各家免费层通常限定标准音色、不含自定义声音克隆。

## 一句换算参考

语音大模型把音频折算成 token 计价时，常见口径是**每秒音频约 30 token**（单家文档口径，不同厂商不同）。按这个比例，1 分钟音频约 1,800 token，10 分钟约 1.8 万 token——这就是为什么"按 token 卖 TTS"看起来便宜，实际按分钟算并不便宜。

## 四个坑

1. **额度按模型切分**：图像 100 张是每个模型 100 张，换模型重新计，不是共享池。
2. **不限量但限并发**：TTS 试用期"调用量不限"配 2 路并发，批量配音会排队；并发是比总量更硬的天花板。
3. **字符上限**：300 字符/请求意味着 10 分钟有声书要切几十段，切分不当会出现语气断裂。
4. **降级不可逆**：部分平台从商用降回试用会把并发置 0，试用资格不是"随时可以退回去"的。

## 一句话主线

生成型免费额度是**按件计的试用装**：图像看张数、视频看秒数、语音看字符与并发；它够验证效果与风格，不够支撑批量生产，规划时先换算成"能产出多少件成品"。

## 参考资料

- 阿里云百炼：各模态免费额度（图像 100 张/模型、视频 1,650 秒、ASR 按月刷新）：https://developer.aliyun.com/article/1762121
- 阿里云百炼：新人权益说明（7000 万 token + 100 张图 + 50 秒视频）：https://developer.aliyun.com/article/1708352
- 阿里云智能语音交互：试用版规则（3 个月、语音合成不限量、并发 2）：https://help.aliyun.com/zh/isi/getting-started/user-guide-for-non-developers
- 阿里云智能语音交互：并发与 QPS 说明（CosyVoice 不支持试用、试用降级置 0）：https://help.aliyun.com/zh/isi/product-overview/faq-about-concurrency-and-monitoring
- 阿里云语音合成接口说明（单次 300 字符上限）：https://help.aliyun.com/zh/isi/user-guide/speech-synthesis-1/
- Cloudflare Workers AI 定价（每天 10,000 Neurons，覆盖文生图模型）：https://developers.cloudflare.com/workers-ai/platform/pricing
- 知乎：免费 AI 生图工具实测（"无限免费"类站点的线索来源，未核实条款）：https://zhuanlan.zhihu.com/p/2053535282918691138?utm_medium=openapi_platform&utm_source=b38f6831b176
- 知乎：TTS 旁白选型与各家免费字符额度（线索来源，数字需回官方页核对）：https://zhuanlan.zhihu.com/p/2106968548753068288?utm_medium=openapi_platform&utm_source=b38f6831b176
