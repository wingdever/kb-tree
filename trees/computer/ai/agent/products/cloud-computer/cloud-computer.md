---
description: "Cloud-computer agents: four execution forms, the four questions that separate a real cloud PC from remote control, and security boundaries"
描述: "云电脑 Agent：四种执行形态、区分真云机与远控本机的四问，以及隔离与审计边界"
name: "Cloud Computer Agents"
名称: "云电脑 Agent"
---

# 云电脑 Agent

"云电脑 Agent"指 Agent 在厂商机房里的一台虚拟电脑上执行任务，用户关掉客户端也能继续跑。它和"远程操控自己电脑""云端浏览器沙箱"是三件不同的事，混着看会导致对连续性、权限与数据位置的误判。

执行形态与资源价格是两件事：这一页只判断**在哪跑、能不能常驻、数据落在哪、能不能审计**；免费额度、积分与订阅门槛属于采购成本问题，要用真实用量单独测算。

## 四种执行环境

| 形态 | 环境归属 | 关机后是否继续 | 数据在哪 |
|---|---|---|---|
| 自带云电脑 | 厂商云端独立实例 | 继续 | 云端工作区，可下载 |
| 云手机 | 厂商云端 Android 实例 | 继续 | 云端，隔离于真实手机 |
| 远控本机 | 用户自己的电脑 | 停止 | 本机 |
| 云端沙箱 | 厂商临时容器 | 通常回收 | 临时盘，闲置即销毁 |

豆包的工作任务模式把云电脑与"本地电脑模式"并列，云电脑在隔离环境里跑，产物存云端，本地关机也不影响任务<RichMediaReference>["https://www.doubao.com/legal/DoubaoAgentModeNotice"]</RichMediaReference>；它的云端沙箱闲置一段时间会销毁，装进去的工具与包不保留<RichMediaReference>["https://www.doubao.com/work/docs/zh-cn/articles/047323472965-work-task-mode"]</RichMediaReference>。

智谱 AutoGLM 2.0 走的是"云手机 + 云电脑"，目的明确：不占用用户的手机与电脑，任何设备都能发起任务<RichMediaReference>["https://developer.volcengine.com/articles/7540557887958057002"]</RichMediaReference>。阿里无影则把云电脑做成可托管 Agent 的"云工位"，提供 Windows 与 Linux 桌面与远程接管<RichMediaReference>["https://www.alibabacloud.com/zh/product/jvs"]</RichMediaReference>。

## 判据四问

1. 执行在谁的机房？
2. 客户端关闭后任务是否继续？
3. 有没有完整桌面（能装软件、开浏览器），而不只是 API 沙箱？
4. 普通消费者能否直接开通？

四问全"是"才是 C 端云电脑 Agent；第 3 问为"否"的，多数是浏览器或代码沙箱，不是云电脑。远控本机在第 1、2 问就出局：算力与在线状态仍归用户自己。

## 一台云电脑的实际规格

宣传页常只写"云端 Windows"，真实可用性由实例规格决定。以下是中国电信 TeleAgent 客户端"云电脑身份确认"面板给出的实测样本（2026 年 11 月）：

| 项目 | 配置 | 意味着什么 |
|---|---|---|
| 操作系统 | Windows Server 2022 Standard，64 位，Build 20348 | 服务器版内核，不是消费级 Windows 11 |
| CPU | Intel Xeon（Skylake）@ 2.99 GHz，4 vCPU | 2016 年前后的服务器架构，四核共享 |
| 内存 | 8 GB | 浏览器十余标签 + Office + 自动化脚本即接近上限 |
| 系统盘 C: | 120 GB（可用约 100 GB） | 装 IDE、浏览器、Office 后余量有限 |
| 数据盘 D: | 20 GB（可用约 19.4 GB） | 交付物、截图、录屏要尽快下载走 |
| 显卡 | 无独立 GPU（纯 CPU 虚拟机） | 本地推理不可行，模型调用必须走远端 API |

三条直接推论：

1. **无 GPU 决定了算力分工**。云机负责"操作"——点按、打开文件、跑浏览器；模型推理留给云端 API。想在云机上本地跑 7B 以上模型，这类实例做不到。
2. **Server 版系统限制了软件生态**。没有 Microsoft Store，部分消费级安装包要求客户端版 Windows，安卓子系统也不存在；镜像里预装什么，往往决定了能做什么。
3. **磁盘是隐性瓶颈**。系统盘百 GB 级、数据盘二十 GB 级，对"下载一堆安装包再试"的探索型任务很容易写满；长任务要把产物落到外部存储或对象存储。

选型时的问法应从"有没有云电脑"改成：**几个 vCPU、多少内存、系统盘与数据盘多大、有没有 GPU、系统是客户端版还是 Server 版、镜像能否自定义**。这几项答不清，产品大概率只是把浏览器塞进了容器。

## 形态选择

- **任务要跨应用点按、且必须用你本人账号与本地文件**：本机执行更合适，环境与权限都在你手里。
- **任务要跑几十分钟以上、你还会合上电脑**：自带云电脑，靠常驻性换连续性。
- **任务只碰网页**：浏览器沙箱足够，不必为完整桌面付费。
- **任务要在真实 App 里完成、又不能碰你的真手机**：云手机，隔离性优于本地自动化。
- **团队要统一管理、审计与回收**：云工位型平台，权限与镜像集中下发。

## 安全与合规

- **隔离**：云机应与真实设备隔离，敏感账号不登录在云机里。智谱明确选择放弃操作微信等隐私密集应用，并把动作做成可回放、可审计、可干预<RichMediaReference>["https://www.zhipuai.cn/zh/research/145"]</RichMediaReference>。
- **凭证**：让 Agent 在云机里登录你的账号，等于把凭证托管给第三方；要有撤销、二次确认与操作留痕。
- **临时性**：沙箱销毁会带走环境与文件，长任务要做产物落盘与检查点，否则一次回收就前功尽弃。
- **数据**：任务资料上传即产生处理关系，留存位置、跨境与删除方式要写进协议。
- **能力边界**：执行型 Agent 的失败是"真点了按钮"，不是"说错一句话"；高风险动作必须有人工确认点。

## 一句话主线

云电脑 Agent 的价值不在"云"，而在**执行环境可常驻、可隔离、可回放**；判断它属于哪一类，看环境归属和关机后的连续性，不看宣传里有没有"云"字。

## 参考资料

- 豆包：工作任务功能须知（云电脑模式、数据与产物存放）：https://www.doubao.com/legal/DoubaoAgentModeNotice
- 豆包：工作任务模式使用说明（云端沙箱闲置销毁、环境隔离）：https://www.doubao.com/work/docs/zh-cn/articles/047323472965-work-task-mode
- 智谱 AutoGLM 2.0：Agent + 云手机 + 云电脑范式：https://developer.volcengine.com/articles/7540557887958057002
- 智谱：AutoGLM 开源与研究说明（云手机隔离与审计设计）：https://www.zhipuai.cn/zh/research/145
- 阿里云无影 Agentic Computer（企业云工位与远程接管）：https://www.alibabacloud.com/zh/product/jvs
- 腾讯云：Computer Use Agent 云手机与云桌面（执行基座定位）：https://cloud.tencent.com/act/pro/cvp
- 36 氪：Claude Duet 评测（云端虚拟机形态与通知机制）：https://36kr.com/p/4036677968057223
