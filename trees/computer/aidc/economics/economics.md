---
description: "AIDC capex, opex, utilization, unit cost and the risks that decide whether AI compute is economic"
描述: "AIDC 的投资、运营成本、利用率、单位成本与经济风险"
name: "AIDC Economics and Utilization"
名称: "投资、成本与利用率"
---

# 投资、成本与利用率

AIDC 的经济性不是“每 GPU 多少钱”，而是“每 MW、每机柜、每 token 的全生命周期成本”与利用率的组合。建得起不等于用得起，用得起不等于算得划算。

## CAPEX

- **土地与建筑**：土地、土建、机电与消防；改造项目可复用部分，但层高与承重常限制密度。
- **电力与冷却**：变电站、UPS、柴发、母线、冷机、CDU、管路与水处理。
- **网络与 IT**：交换机、光模块、存储、GPU 服务器与集群管理。
- **设计与许可**：设计、环评、并网、能耗指标与认证。

CAPEX 要按“每 MW”和“每机柜”拆，不然不同规模项目无法比较。

## OPEX

- **电费**：最大单项；受电价、负载率、PUE 与需量电费影响。
- **水费与维护**：冷却水、水处理、滤材、冷媒与备件。
- **人力与运维**：值班、巡检、变更、消防与合规。
- **折旧与融资**：设备寿命短、技术迭代快，折旧假设会显著改变回报。
- **网络与云服务**：带宽、托管、软件许可与监控平台。

## 利用率

- **GPU 利用率**：训练任务是否有足够队列，推理是否有足够流量；闲置的 GPU 仍在吃电与折旧。
- **机柜/电力利用率**：电力容量批下来却用不满，会形成 stranded capacity。
- **超分与排队**：超分提高利用率，但会拉长尾延迟；要按 SLA 定策略。
- **需求波动**：训练与推理的峰谷不同，混合负载能提高整体利用率。

## 成本指标

- **每 MW 成本**：建设与运营的统一口径，便于跨项目比较。
- **每 GPU/每机柜成本**：适合机房与集群内部核算。
- **每 token/每任务成本**：把算力、电、网络与人工摊到业务单位，才是 AI 服务的真实成本。
- **TCO**：CAPEX + OPEX + 折旧 + 风险准备，不能只看采购价。

## 风险

- 电价上涨、需量电费与并网容量变化。
- GPU 技术迭代导致资产贬值；租赁与自建的风险不同。
- 利用率不足、客户流失与合同期限错配。
- 能耗指标、碳排与用水约束收紧。

## 一句话主线

AIDC 的账要按“MW、机柜、token”三层算；只看采购价，会把电费、折旧与闲置藏起来。

## 参考资料

- IEA Data Centres and Data Transmission Networks（2026）：https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks
- Uptime Institute Tier Standard（2026）：https://uptimeinstitute.com/tiers
