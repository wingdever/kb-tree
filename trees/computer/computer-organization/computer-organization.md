---
description: "Computer organization: ISA, CPU datapath and pipelining, memory hierarchy, virtual memory, I/O and parallel architecture"
描述: "计算机组成原理：ISA、CPU 数据通路与流水线、存储层次、虚拟内存、I/O 与并行架构"
name: "Computer Organization"
名称: "计算机组成原理"
---

# 计算机组成原理（Computer Organization）

计算机组成原理研究**计算如何在物理层面实现**。它与计算机体系结构的分工：体系结构（Architecture）定义软件可见的设计——指令集（ISA）、寻址方式、数据类型；组成（Organization）关注这些设计如何用 CPU 数据通路、控制逻辑、存储子系统、I/O 控制器实现。一句概括：**指令集定义"做什么"，微架构决定"怎么做"，总线决定"怎么连"，存储层次决定"多快取数"，并行与专用单元决定"能做多少"**。

这些不是考试题，而是**可观察行为的解释**：缓存友好的代码快 10×、分支预测影响循环性能、CPU-GPU 内存传输昂贵、内存延迟主导数据库负载。理解硬件在代码运行时实际做什么，才能做出多数从未学过组成原理的开发者做不到的工程决策。

## 子树导航

| 子树 | 关注点 | 入口 |
|---|---|---|
| 指令集架构 | ISA 作为软硬件契约、RISC/CISC、寻址、大小端、冯·诺依曼与哈佛 | `isa/isa.md` |
| 处理器与数据通路 | 指令周期、控制器/ALU/MMU、超标量、乱序执行、分支预测 | `cpu/cpu.md` |
| 存储层次 | 局部性、缓存机制、多核一致性、内存墙、虚拟内存与 TLB | `memory/memory.md` |
| I/O 系统 | 程序查询/中断/DMA、设备控制器、总线、统一与独立编址 | `io/io.md` |
| 并行架构 | Flynn 分类、SIMD、多核与一致性模型、NUMA、GPU/SIMT、Amdahl 定律 | `parallel/parallel.md` |
| 性能指标 | CPU 时间公式、CPI/IPC、MIPS/FLOPS、加速比定律、基准测试 | `performance/performance.md` |
| 实践与工具 | 为什么要学、gem5/VENUS/Logisim/perf/cachegrind、推荐教材 | `practice/practice.md` |
| 硬件趋势 | Chiplet、HBM、NPU/TPU、RISC-V、存内计算、微架构安全 | `trends/trends.md` |

## 一句话主线

**ISA 定义软硬件契约，微架构用流水线与乱序把它做快，存储层次用局部性掩盖 CPU 与内存的鸿沟，并行架构与专用单元突破单核上限，性能公式则把这一切变成可计算的取舍。**

> 相关：计算机学科总览见 `../computer.md`；软件工程（本知识的工程应用侧）见 `../software-engineering/`；AI 芯片与推理优化见 `../ai/model/inference/`。
