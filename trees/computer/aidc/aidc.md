---
description: "AI data centers: workloads, power, cooling, network, planning, operations, efficiency and economics"
描述: "AI 数据中心（AIDC）：负载、供电、制冷、网络、规划、运维、能效与成本"
name: "AI Data Center (AIDC)"
名称: "AI 数据中心"
---

# AI 数据中心（AIDC）

AIDC 是行业对“以 AI 训练与推理为主要负载”的数据中心的简称，也有人把它理解为“AI-ready data center”。它不是“机房里放了几台 GPU”，而是供电、制冷、网络、机柜、运维与成本一起为高功率密度 AI 负载重新设计的一套设施。

## 与 IDC、超算的区别

| 类型 | 主要负载 | 典型特征 | 设计重心 |
|---|---|---|---|
| 通用 IDC | Web、数据库、企业应用 | 机柜功率较低、风冷为主、网络通用 | 可用性、托管、成本 |
| AIDC | 大模型训练、推理、Agent 服务 | 高功率机柜、GPU 集群、液冷/混合冷却、高速互联 | 电力、散热、集群网络、利用率 |
| 超算中心 | 科学计算、仿真、HPC | 紧耦合集群、InfiniBand、CPU/GPU 混合 | 浮点性能、互联、任务调度 |

三者有交集：AIDC 可能采用超算的高速互联，也可能托管在通用 IDC 里；区别在主要负载与设计取舍，不在建筑名称。

## 八个系统

- **负载与算力形态**：训练还是推理、GPU 集群规模、机柜功率密度、超节点与 scale-up/scale-out。
- **供电与配电**：市电引入、变压器、UPS、柴发、ATS、PDU/母线、2N 与 N+1。
- **制冷与液冷**：风冷、冷板液冷、浸没式、CDU、冷冻水与自然冷却。
- **网络与集群互联**：叶脊拓扑、RoCE/InfiniBand、东西向流量、无损与拥塞控制。
- **规划、选址与建设**：电力容量、水资源、光纤时延、气候、政策、Tier 与模块化。
- **运维、监控与可靠性**：DCIM/BMS/EPMS、漏液检测、消防、变更管理、SLA。
- **能效、水耗与合规**：PUE、WUE、CUE、可再生能源、并网与能耗指标。
- **投资、成本与利用率**：CAPEX/OPEX、每 MW 成本、电价、利用率与 stranded capacity。

## 一句话主线

AIDC 的瓶颈通常不在 GPU，而在电、冷、网、运维与利用率；任何一项短板都会把算力变成昂贵的闲置。

## 参考资料

- Uptime Institute Tier Standard（2026）：https://uptimeinstitute.com/tiers
- ASHRAE Thermal Guidelines for Data Processing Environments（2026）：https://www.ashrae.org/technical-resources/bookstore/thermal-guidelines-for-data-processing-environments
- IEA Data Centres and Data Transmission Networks（2026）：https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks
