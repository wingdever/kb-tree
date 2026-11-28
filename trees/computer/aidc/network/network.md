---
description: "East-west traffic, spine-leaf, InfiniBand/RoCE, topology and congestion control for AI clusters"
描述: "AIDC 的集群网络：东西向流量、叶脊、InfiniBand/RoCE、拓扑与拥塞控制"
name: "AIDC Cluster Network"
名称: "网络与集群互联"
---

# 网络与集群互联

AI 集群的瓶颈经常出现在网络，而不是 GPU。训练参数同步、推理请求分发、存储 checkpoint 都走东西向流量；网络设计不好，GPU 会一直等数据。

## 东西向与叶脊

- 传统数据中心以南北向为主；AI 集群以服务器之间的东西向为主，流量大、模式固定、对尾延迟敏感。
- 叶脊（spine-leaf）用两层交换把任意两台服务器控制在少数跳内，便于横向扩展与故障隔离。
- 大集群可用多平面、rail-optimized 等拓扑，把同一 GPU 序号或同一通信域聚在一条轨上，减少跨轨跳数。

## InfiniBand 与 RoCE

- **InfiniBand**：专用网络，低延迟、RDMA 成熟，适合紧耦合训练；成本与运维门槛较高。
- **RoCEv2**：在以太网上跑 RDMA，生态开放、成本较低；需要 PFC、ECN、拥塞控制与配置一致性，否则容易丢包与性能抖动。
- 选择不是“谁更快”，而是看团队运维能力、生态锁定、规模与预算。

## 拓扑与收敛

- **非阻塞/无收敛**：任意端口间可满速通信，成本高但尾延迟稳定。
- **收敛比**：上行带宽小于下行，能省钱，但训练同步时容易拥塞；收敛比要按流量模型算。
- **多轨**：把不同 GPU 或不同通信阶段分到不同轨，降低单轨热点。

## 存储与管理网络

训练 checkpoint、数据集与日志会占大量带宽。存储网络、管理网络与计算网络最好逻辑隔离；混跑会让一个大 checkpoint 拖慢整个训练任务。

## 无损与拥塞

- PFC 防丢包，但配置不当会引发暂停风暴；ECN 做主动拥塞标记，需要端到端调参。
- 集合通信（all-reduce、all-gather）对尾延迟极敏感；平均带宽够，不代表尾延迟达标。
- 监控要看端口误码、丢包、PFC 暂停、ECN 标记与流分布，而不是只看链路利用率。

## 一句话主线

AI 网络按“尾延迟 + 无损 + 可运维”设计；只看峰值带宽，训练仍会被偶发拥塞拖慢。

## 参考资料

- InfiniBand Trade Association（2026）：https://www.infinibandta.org/
- RoCE Initiative（2026）：https://www.roceinitiative.org/
