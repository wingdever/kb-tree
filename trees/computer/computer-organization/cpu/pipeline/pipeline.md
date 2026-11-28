---
description: "Instruction pipelining: stages, throughput, structural/data/control hazards, forwarding, stalling and branch prediction"
描述: "指令流水线：阶段划分、吞吐、结构/数据/控制冒险、转发、停顿与分支预测"
name: "Instruction Pipelining"
名称: "指令流水线"
---

# 指令流水线（Instruction Pipelining）

流水线把指令执行分成多个阶段，让不同指令在不同阶段同时推进。它提升的是**吞吐**（单位时间完成的指令数），而不是单条指令的延迟——单条指令仍要走完所有阶段，只是多条指令重叠执行。

## 五级流水线

经典模型：IF（取指）→ ID（译码/读寄存器）→ EX（执行/地址计算）→ MEM（访存）→ WB（写回）。理想情况下，5 级流水线在填满后每周期完成 1 条指令，吞吐接近流水线级数倍（忽略填充与冒险）。

关键在于各阶段之间的**流水线寄存器**保存中间结果；阶段时间由最慢的一段决定，因此平衡各段长度是设计要点。

## 三类冒险（Hazard）

冒险指下一条指令无法在预定周期执行，必须停顿或改变顺序。

- **结构冒险**：硬件资源冲突（如单端口内存同时被取指和访存）。对策：增加资源（分离的 I-Cache / D-Cache）、寄存器重命名。
- **数据冒险**：指令依赖前面指令尚未写回的结果。
  - RAW（读后写，真相关）：`add r1,r2,r3` 后 `sub r4,r1,r5`。
  - WAR / WAW（反相关 / 输出相关）：寄存器重命名可消除。
  - 对策：**转发（forwarding / bypass）**把 ALU 结果直接送给下游，不必等写回；无法转发时**停顿（stall / bubble）**。Load-use 冒险（load 后紧跟使用其结果）通常需要一个周期的停顿。
- **控制冒险**：分支/跳转改变 PC，而后续指令已进入流水线。
  - 对策：**静态预测**（总是取 / 不取）、**动态预测**（2 位饱和计数器、分支目标缓冲 BTB、返回地址栈 RAS）、**延迟槽**（在分支后放必执行指令）、**推测执行**。
  - 猜错代价：流水线越深，需要冲刷（flush）的指令越多，惩罚越大（常见 10–20 周期）。

## 分支预测

现代预测器组合多种机制：局部历史、全局历史、TAGE 类多分量预测器等，准确度可达 95% 以上。预测正确时几乎零成本；预测失败时需丢弃错误路径结果并回滚重命名状态，重新取指——这是深流水线的最大性能杀手之一。

## 深流水线的取舍

更深流水线 → 每段更短 → 主频更高；但分支惩罚、流水线寄存器开销与功耗随之上升。当预测失败率与停顿占比过高时，加深流水线反而降低实际 IPC。这也是"主频竞赛"让位于多核与专用单元的原因。

## 常见失败模式

- 只算理想加速比，忽略停顿与预测失败——真实程序受冒险显著拖累。
- 误以为转发能解决所有数据冒险：load-use 仍需停顿。
- 循环展开与访存模式不考虑分支预测器行为，导致可预测性下降。

## 参考资料

- Computer Organization and Design（Patterson & Hennessy）：https://shop.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6
- Computer Systems: A Programmer's Perspective（Bryant & O'Hallaron）：https://csapp.cs.cmu.edu/
