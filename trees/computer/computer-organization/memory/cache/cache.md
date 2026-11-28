---
description: "Cache organization: line size, mapping, write policies, replacement, 3C misses, AMAT and cache coherence protocols"
描述: "缓存组织：缓存行、映射方式、写策略、替换算法、3C 失效、AMAT 与一致性协议"
name: "CPU Cache"
名称: "CPU 缓存"
---

# CPU 缓存（CPU Cache）

缓存利用局部性，把最近/附近访问的数据保留在靠近 CPU 的小容量高速存储中，以掩盖 CPU 与主存的速度差。

## 缓存组织

地址被切分为 **tag | index | offset**：offset 在缓存行内定位字节，index 选缓存组（set），tag 判断是否是目标数据。

- **缓存行（cache line）**：常见 64B，是缓存与主存之间传输的最小单位。即使只读 1 字节，也会加载整行——这是空间局部性的物理体现。
- **直接映射**：每行只对应一个位置，实现简单但冲突失效多。
- **组相联**：每组可放多行（如 8 路），冲突与硬件复杂度折中，现代主流。
- **全相联**：任意行可放任意位置，失效最少但比较电路昂贵，用于小容量（如 TLB）。

## 命中与失效

- **命中（hit）**：tag 匹配且有效位有效，直接取数。
- **失效（miss）**：从下一层加载整行；若缓存满，按替换策略淘汰一行。
- **平均内存访问时间**：`AMAT = 命中时间 + 失效率 × 失效惩罚`。三者任一恶化都会拉慢程序。

## 写策略

- **写回（write-back）**：只改缓存，标脏（dirty），被淘汰时才写回主存——写带宽低，但需维护脏位。
- **写穿（write-through）**：每次写同时更新缓存与下一层——实现简单、一致性好，但写带宽高。
- **写分配 vs 非写分配**：写失效时是否把该行加载到缓存，通常与写回/写穿搭配选择。

## 替换策略

LRU（最近最少使用）理论最优但硬件实现昂贵；**伪 LRU**、随机、时钟近似算法被广泛使用。对大容量缓存，LRU 的边际收益有限。

## 3C 失效模型

- **Compulsory（强制性）**：第一次访问必然失效，可用预取缓解。
- **Capacity（容量性）**：缓存装不下工作集，增大容量才能缓解。
- **Conflict（冲突性）**：组相联下多行争用同一组，提高相联度或改进数据布局可缓解。

## 多核一致性（MESI / MOESI）

每个缓存行带状态：

- **M（Modified）**：已修改、与主存不一致、仅本核持有——写回主存后转 E/S。
- **E（Exclusive）**：干净、仅本核持有——写操作无需广播。
- **S（Shared）**：干净、多核可能共有——写前需使其他副本失效（RFO, Read For Ownership）。
- **I（Invalid）**：无效。MOESI 增加 O（Owned）状态，指定一个核负责写回，减少写回流量。

**伪共享（false sharing）**：不同核修改同一缓存行的不同变量，因行粒度一致性而互相使对方失效，性能骤降。对策：按缓存行对齐/填充热数据。

## 常见失败模式

- 数据结构布局无视缓存行：热字段分散、跨行访问、伪共享。
- 随机访问模式破坏空间局部性，缓存形同虚设。
- 多核程序忽略伪共享，误判为算法本身慢。

## 参考资料

- Computer Organization and Design（Patterson & Hennessy）：https://shop.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6
- Computer Systems: A Programmer's Perspective（Bryant & O'Hallaron）：https://csapp.cs.cmu.edu/
