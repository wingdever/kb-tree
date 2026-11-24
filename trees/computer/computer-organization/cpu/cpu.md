---
description: "CPU microarchitecture: instruction cycle, datapath components, superscalar, out-of-order execution and branch prediction"
描述: "CPU 微架构：指令周期、数据通路部件、超标量、乱序执行与分支预测"
name: "CPU Microarchitecture"
名称: "CPU 微架构"
---

# CPU 微架构（CPU Microarchitecture）

ISA 定义"做什么"，微架构决定"怎么做"。微架构的目标是在真实负载下尽可能提高**每周期指令数（IPC）**，同时控制功耗与面积。

## 指令周期

取指（IF）→ 译码（ID）→ 执行（EX）→ 访存（MEM）→ 写回（WB）。这是经典的五级顺序执行模型；现代处理器把每级再细分，并用流水线、乱序与推测并行化。

## 数据通路部件

- **控制器（CU）**：编排 CPU 操作，产生控制信号。
- **ALU**：算术与逻辑运算。
- **寄存器组**：最快的存储，靠近执行单元。
- **地址生成单元（AGU）**：计算访存地址。
- **内存管理单元（MMU）**：处理虚拟内存与保护，见 `../memory/virtual/virtual.md`。
- **总线接口 / 缓存控制器**：连接存储层次，见 `../memory/memory.md`。
- **流水线寄存器**：分隔各阶段，保存中间结果。

## 从顺序到超标量

- **流水线**：把指令执行分阶段并行化，提升吞吐而非单条延迟，详见 `pipeline/pipeline.md`。
- **超标量（superscalar）**：每周期发射多条指令到多个执行单元。
- **乱序执行（out-of-order）**：指令按数据就绪程度执行，而非程序顺序；用**重排序缓冲（ROB）**保证结果按序提交（commit），对外表现为顺序语义。寄存器重命名消除 WAW/WAR 伪相关。
- **分支预测与推测执行**：猜测分支走向，提前执行后续指令；猜对则掩盖控制冒险，猜错则回滚（flush）。现代预测器准确度可达 95% 以上。
- **更深流水线**：更高主频，但分支惩罚与功耗上升——这是"主频竞赛"终被多核取代的原因之一。

## 后端调度

指令经过译码/重命名后进入发射队列（issue queue），等待操作数就绪后分发到执行端口；执行结果通过旁路网络（bypass network）转发给依赖指令，而非等写回寄存器。ROB 按序提交保证精确异常（precise exception）——异常发生时，状态等同于出错指令之前全部完成、之后全部未执行。

## 性能视角

CPU 时间 = 指令数 × CPI / 主频，见 `../performance/performance.md`。微架构的所有努力都可归入三类：减少指令数（ISA / 编译器）、降低 CPI（流水线 / 乱序 / 预测）、提升主频（工艺 / 流水线深度），而功耗墙让第三类越来越受限。

## 常见失败模式

- 以为"主频越高越快"——不同 ISA / 微架构的 IPC 差异巨大，主频不可跨架构比较。
- 忽略推测执行的副作用：Spectre / Meltdown 等微架构侧信道（见 `../trends/trends.md`）。
- 把乱序执行理解为"程序语义乱序"——对外仍按序提交，乱序只是内部优化。

> 相关：流水线与冒险详见 `pipeline/pipeline.md`；ISA 定义见 `../isa/isa.md`；存储层次见 `../memory/memory.md`；性能指标见 `../performance/performance.md`；计算机组成总览见 `../computer-organization.md`；计算机学科总览见 `../../computer.md`。
