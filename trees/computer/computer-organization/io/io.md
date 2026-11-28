---
description: "I/O systems: programmed I/O, interrupts, DMA, device controllers, buses and memory-mapped versus isolated I/O"
描述: "I/O 系统：程序查询、中断、DMA、设备控制器、总线以及统一与独立编址"
name: "I/O System"
名称: "I/O 系统"
---

# I/O 系统（I/O System）

I/O 系统负责 CPU、内存与外部设备之间的数据交换。核心矛盾：设备速度远慢于 CPU，且种类繁杂——需要分层与标准化把差异隐藏起来。

## I/O 控制方式

- **程序查询（polling）**：CPU 反复检查设备状态寄存器。实现简单，但 CPU 空等，适合简单或低频率设备。
- **中断驱动（interrupt-driven）**：设备就绪时发中断，CPU 转去处理后再返回原任务。避免空等，但有中断处理开销；高频中断会淹没 CPU（中断风暴）。
- **DMA（直接内存访问）**：DMA 控制器直接在设备与内存间搬运数据，只在开始与结束时通知 CPU。适合大块传输（磁盘、网卡、GPU）。

演进逻辑：从"CPU 全程盯着"到"CPU 只在必要时参与"，把 CPU 从数据搬运中解放出来。

## 设备控制器与缓冲

设备控制器是设备与总线之间的接口，带状态/命令/数据寄存器和缓冲区。缓冲用于平滑速度差、批量传输。设备驱动则是操作系统中屏蔽控制器差异的软件层。

## 总线

总线连接 CPU、内存与 I/O：

- **PCIe**：主流高速外设总线，点对点链路、分层协议（事务层/数据链路层/物理层），按 lane 扩展（x1/x4/x16）。
- **DDR5**：主存接口，带宽与通道数是关键参数。
- **NVMe**：基于 PCIe 的固态盘协议，取代老旧的 SATA/AHCI，低延迟、高队列深度。
- 现代系统常是多层总线/互连：CPU 内互连、内存控制器、PCIe 根复合体、芯片组/南桥。

## 编址方式

- **统一编址（memory-mapped I/O）**：外设寄存器与内存共享地址空间，用普通访存指令操作外设（ARM、x86 主流）。优点是指令统一；缺点是占用地址空间、缓存需特别处理（设备寄存器不可缓存）。
- **独立编址（isolated I/O）**：I/O 地址空间独立，需专用 in/out 指令（早期 8051、x86 保留 I/O 端口空间）。

## 中断细节

- 可屏蔽中断 vs 不可屏蔽中断（NMI）；中断向量表/IDT 决定处理入口。
- 中断优先级与嵌套；关中断保护临界区。
- 中断下半部（bottom half / tasklet / 工作队列）：把耗时处理推迟，缩短中断禁用时间。
- DMA 与缓存一致性：设备写内存后，CPU 缓存可能有旧副本——需要一致性 DMA 或显式缓存无效化（invalidate）。

## 常见失败模式

- 用轮询处理高频设备，CPU 被空等耗尽。
- 中断处理函数做重活，导致中断丢失与延迟飙升。
- DMA 缓冲区未做缓存一致性处理，读到陈旧数据。
- 忽略设备寄存器不可缓存属性，编译器/硬件重排导致设备操作失效。

## 参考资料

- Computer Organization and Design（Patterson & Hennessy）：https://shop.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6
- Computer Systems: A Programmer's Perspective（Bryant & O'Hallaron）：https://csapp.cs.cmu.edu/
