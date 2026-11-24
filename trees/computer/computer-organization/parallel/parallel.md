---
description: "Parallel architecture: Flynn taxonomy, SIMD, multicore coherence, memory consistency, NUMA, GPU SIMT and Amdahl's law"
描述: "并行架构：Flynn 分类、SIMD、多核一致性、内存一致性模型、NUMA、GPU SIMT 与 Amdahl 定律"
name: "Parallel Architecture"
名称: "并行架构"
---

# 并行架构（Parallel Architecture）

当单核主频受功耗墙限制，并行成为提升算力的主路径。并行可以在多个层次发生：指令级（流水线/乱序）、数据级（SIMD）、线程级（多核）、请求级（多机/分布式）。

## Flynn 分类法

按指令流与数据流数量划分：

- **SISD**：单指令单数据——传统单核顺序执行。
- **SIMD**：单指令多数据——一条指令对一组数据同时操作，见下。
- **MISD**：多指令单数据——罕见，用于容错/流水线式处理。
- **MIMD**：多指令多数据——多核、多机，当前并行主流。

## SIMD

单指令多数据，用向量寄存器一次处理多个元素：

- x86：MMX / SSE / AVX / AVX-512；ARM：NEON / SVE；RISC-V：V 扩展。
- 应用：图像/音视频处理、科学计算、密码学、AI 算子。
- 收益取决于数据是否规整、是否能向量化；分支密集或非连续访问会削弱收益。编译器自动向量化与手写 intrinsics 是两种路径。

## 多核与缓存一致性

多核各有私有缓存时，**一致性（coherence）**保证"同一地址的多份副本一致"（MESI/MOESI，见 `../memory/cache/cache.md`）。**内存一致性模型（consistency）**则规定"多个地址读写操作的可见顺序"：

- **顺序一致性**：所有核看到单一全局顺序，最易推理但限制优化。
- **TSO（x86）**：允许写后读重排（store buffer 导致），其余保持较强顺序。
- **宽松一致性（ARM / RISC-V）**：更多重排自由，需程序员/编译器显式插入**内存屏障（fence/barrier）**保证同步语义。

锁、原子操作与内存屏障是并发正确的三件套。忽略一致性模型是并发 bug 的常见根源。

## NUMA 与大小核

- **NUMA（非一致内存访问）**：多路/多核系统中，访问本地内存比远程内存快；线程与内存绑定（affinity）可显著影响性能。
- **big.LITTLE 大小核**：性能核与能效核混合调度，移动端与部分服务器采用；调度策略决定能效比。
- **OpenMP / pthreads**：共享内存并行编程模型，需处理同步、负载均衡与虚假共享。

## GPU 架构

GPU 与 CPU 设计哲学不同：CPU 追求低延迟、强单线程；GPU 追求高吞吐、海量线程隐藏延迟。

- **SIMT（单指令多线程）**：一个指令广播给一组线程（warp/wavefront），各线程处理不同数据。
- **编程层次**（CUDA）：thread → block → grid；共享内存、全局内存、寄存器分级。
- **访存优化**：合并访问（coalescing）、共享内存复用、避免分支发散。
- **Tensor Core / AI 加速**：矩阵乘专用单元，支撑深度学习训练与推理，见 `../../ai/model/inference/`。
- CPU-GPU 数据传输（PCIe）昂贵，应减少传输次数、增大批量。

## 加速比定律

**Amdahl 定律**：

```
Speedup = 1 / ((1 - f) + f / s)
```

其中 f 是可并行部分占比，s 是其加速倍数。若只有 40% 可并行，即使无限快，理论最大加速也只有 `1 / 0.6 ≈ 1.67×`——**与核数无关**。它提醒我们：优化可并行部分之前，先看串行瓶颈。

**Gustafson 定律**：当问题规模随处理器数增长时，加速比可近线性——Amdahl 假设固定问题规模，Gustafson 假设固定时间扩展问题，两者视角不同。

## 常见失败模式

- 以为"核数翻倍性能翻倍"——受串行部分、内存带宽与同步开销限制。
- 忽略内存一致性模型，写出依赖"看起来顺序执行"的并发代码。
- GPU 程序分支发散、访存非合并，实际吞吐远低于峰值。
- NUMA 系统跨节点访存，性能悄然下降。

> 相关：缓存一致性协议见 `../memory/cache/cache.md`；存储层次见 `../memory/memory.md`；加速比与性能指标见 `../performance/performance.md`；AI 推理优化见 `../../ai/model/inference/`；计算机组成总览见 `../computer-organization.md`；计算机学科总览见 `../../computer.md`。
