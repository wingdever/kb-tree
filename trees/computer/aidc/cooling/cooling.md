---
description: "Air cooling limits, direct-to-chip liquid cooling, immersion and free cooling in AI data centers"
描述: "AIDC 的风冷边界、冷板液冷、浸没式与自然冷却"
name: "AIDC Cooling and Liquid Cooling"
名称: "制冷与液冷"
---

# 制冷与液冷

AIDC 的散热问题不是“空调够不够冷”，而是“能不能把机柜里的热量稳定带走”。功率密度上升后，风冷会先遇到风量、风压与送回风路径的边界，液冷才进入主选方案。

## 风冷的边界

- 风冷靠空气带走热量；机柜功率越高，所需风量越大，风扇能耗、噪声与热点越难控制。
- 冷热通道隔离、盲板、送风温度与回风路径都会影响效果；只加空调不提风量，往往解决不了局部热点。
- 风冷适合中低功率密度；高密度 GPU 机柜若继续用风冷，容易出现“机房整体不热、单柜过热”。

## 冷板液冷

- 冷板贴在 GPU/CPU 上，通过 CDU 与二次侧循环把热量带到室外或冷冻水系统。
- 关键部件：冷板、快接头、软管、CDU、漏液检测、水质与压差监控。
- 好处是换热效率高、噪音低、机柜功率密度可提升；代价是漏液风险、维护复杂度与设施改造。
- 冷板液冷不是“只换服务器”；它改变机柜布局、供电、管路与运维流程。

## 浸没式液冷

- 单相浸没：服务器浸在绝缘液体中，靠液体自然对流/循环散热；维护与兼容性是重点。
- 两相浸没：靠相变换热，效率高但液体与密封要求更高。
- 适合极高密度或特殊场景；不是所有服务器、线缆与光模块都适合浸没。

## 自然冷却与余热

- 自然冷却利用室外低温空气或干冷器，减少压缩机运行；适合气候条件合适、空气质量可控的地区。
- 余热回收可用于区域供暖或工艺预热，但需要稳定的热需求与配套管网。
- 自然冷却不是“免费冷却”：水质、过滤、结露、腐蚀与季节波动都要处理。

## 一句话主线

先看功率密度选冷却方式，再设计管路、漏液检测与运维；液冷不是配件，是设施级改造。

## 参考资料

- ASHRAE Thermal Guidelines for Data Processing Environments（2026）：https://www.ashrae.org/technical-resources/bookstore/thermal-guidelines-for-data-processing-environments
- Open Compute Project（2026）：https://www.opencompute.org/
