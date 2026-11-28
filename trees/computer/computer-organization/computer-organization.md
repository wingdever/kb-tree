---
description: "Computer organization: ISA, CPU datapath and pipelining, memory hierarchy, virtual memory, I/O and parallel architecture"
描述: "计算机组成原理：ISA、CPU 数据通路与流水线、存储层次、虚拟内存、I/O 与并行架构"
name: "Computer Organization"
名称: "计算机组成原理"
---

# 计算机组成原理（Computer Organization）

计算机组成原理研究**计算如何在物理层面实现**。它与计算机体系结构的分工：体系结构（Architecture）定义软件可见的设计——指令集（ISA）、寻址方式、数据类型；组成（Organization）关注这些设计如何用 CPU 数据通路、控制逻辑、存储子系统、I/O 控制器实现。一句概括：**指令集定义"做什么"，微架构决定"怎么做"，总线决定"怎么连"，存储层次决定"多快取数"，并行与专用单元决定"能做多少"**。

这些不是考试题，而是**可观察行为的解释**：缓存友好的代码快一个数量级、分支预测影响循环性能、CPU-GPU 内存传输昂贵、内存延迟主导数据库负载。理解硬件在代码运行时实际做什么，才能做出多数从未学过组成原理的开发者做不到的工程决策。

## 一句话主线

**ISA 定义软硬件契约，微架构用流水线与乱序把它做快，存储层次用局部性掩盖 CPU 与内存的鸿沟，并行架构与专用单元突破单核上限，性能公式则把这一切变成可计算的取舍。**

## 参考资料

- Computer Organization and Design（Patterson & Hennessy）：https://shop.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6
- Computer Systems: A Programmer's Perspective（Bryant & O'Hallaron）：https://csapp.cs.cmu.edu/
