---
description: "AIDC operations: monitoring, DCIM/BMS/EPMS, leak and fire safety, change control and SLA"
描述: "AIDC 运维：监控、DCIM/BMS/EPMS、漏液与消防、变更与 SLA"
name: "AIDC Operations and Reliability"
名称: "运维、监控与可靠性"
---

# 运维、监控与可靠性

AIDC 的运维不是“看空调和电表”，而是把电力、热、网络、算力与安全放进同一套可观测与响应机制。高密度机房的故障传播更快，手工巡检不够。

## 监控对象

- **电力**：进线、变压器、UPS、柴发、母线、PDU、机柜功率与负载率。
- **热**：送风/回风温度、机柜进风温度、热点、冷板流量、CDU 压差与水温。
- **环境**：漏水、湿度、烟感、消防、门禁与视频。
- **网络**：端口误码、丢包、PFC 暂停、ECN 标记、链路利用率与尾延迟。
- **算力与存储**：GPU 利用率、温度、降频、ECC、checkpoint 与存储带宽。

## DCIM、BMS 与 EPMS

- **DCIM**：资产、容量、机柜、连接与变更；回答“哪里有什么、还剩多少容量”。
- **BMS**：楼宇与暖通，控制冷机、水泵、风机与阀门。
- **EPMS**：电力监控，计量、告警、电能质量与配电状态。

三者要打通，否则“电力告警”与“热告警”无法关联到同一机柜。

## 漏液、热失控与消防

- 液冷回路要装漏液检测绳/点式传感器，报警要能定位到机柜与接头。
- 锂电池与高密度电源要关注热失控、隔离与消防联动；灭火介质要适合电气火灾。
- 消防演练要覆盖断电、断水、误喷与人员疏散，不只是按按钮。

## 变更与演练

- 任何配电、管路、网络与固件变更都要有变更单、影响范围、回滚方案与窗口。
- 定期做切换演练：UPS、柴发、ATS、冷却切换、网络主备；记录实际切换时间与失败点。
- 故障域要能隔离：一排、一个 CDU、一台交换机故障，不应拖垮整个集群。

## SLA 与故障域

SLA 要写清可用性、响应时间、恢复时间、赔付与例外；内部还要定义 RTO/RPO 与降级模式。高可用不是“没有故障”，而是“故障时能限界”。

## 一句话主线

运维的目标不是零告警，而是故障可发现、可定位、可隔离、可恢复；四件事缺一，密度越高风险越大。

## 参考资料

- Uptime Institute Tier Standard（2026）：https://uptimeinstitute.com/tiers
- ASHRAE Thermal Guidelines for Data Processing Environments（2026）：https://www.ashrae.org/technical-resources/bookstore/thermal-guidelines-for-data-processing-environments
