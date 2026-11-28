---
description: "AIDC site selection, Tier/redundancy, build vs retrofit and grid interconnection"
描述: "AIDC 的选址、Tier 与冗余、建设模式与并网"
name: "AIDC Planning and Site Selection"
名称: "规划、选址与建设"
---

# 规划、选址与建设

AIDC 的规划顺序常常是反的：先定地、再找电，最后发现电力不够。正确顺序是先算负载与电力，再选站址与建设模式；建筑只是结果的容器。

## 选址要素

- **电力**：可用容量、电价、并网排队、变电站距离与扩容可能；这是第一约束。
- **水**：水源、水质、排水与冷却方式；缺水地区要避免高水耗方案。
- **光纤**：到骨干网与客户的时延、多条运营商路径、跨境/跨城链路。
- **气候**：自然冷却窗口、极端温度、空气质量、洪水与地震风险。
- **政策与土地**：能耗指标、环评、土地性质、税收与补贴、当地产业政策。

## Tier 与可用性

Tier I–IV 描述的是冗余与可用性，不是算力密度或 AI 能力。高 Tier 意味着更多冗余与更高成本；AI 训练集群可能更看重电力容量、冷却能力与网络，而不是最高等级的双路冗余。

## 新建、改造与模块化

- **新建**：可按高密度机柜、液冷与高功率配电一次设计；周期长、资本开支大。
- **改造**：利用既有建筑与电力，成本较低；但层高、承重、管路与供电往往限制功率密度。
- **模块化/预制**：建设快、可扩展，适合分期投产；要确认接口、冷却与运维是否与主园区兼容。

## 并网与建设周期

电网接入、环评、能耗指标、土地与施工许可都会拉长周期。AI 需求变化快，分期建设比一次性建满更稳；但要避免“先建壳、后等电”的 stranded capacity。

## 一句话主线

先算电与水，再选地；先定负载与冷却，再定建筑；顺序错了，后面都是补救。

## 参考资料

- Uptime Institute Tier Standard（2026）：https://uptimeinstitute.com/tiers
- IEA Data Centres and Data Transmission Networks（2026）：https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks
