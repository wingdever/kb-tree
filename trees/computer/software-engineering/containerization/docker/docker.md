---
description: "Docker: a platform for building, running and shipping containerized applications, with Dockerfile, images, Compose and Engine"
描述: "Docker：构建、运行与交付容器化应用的平台，含 Dockerfile、镜像、Compose 与 Engine"
name: "Docker"
名称: "Docker"
---

# Docker

Docker 官方把应用开发定位为「构建、保护并交付容器化应用」（Build, secure, and ship containerized applications）。Docker 是**围绕容器化应用的平台与工具体系**，而不是容器本身；容器是它用来打包与运行的单元。

## 容器：隔离运行的进程

Docker 官方定义容器为「计算机上的一个普通进程，例如 Node.js server，但以隔离方式运行」。它具备三点：

- **自己的文件系统**：只见启动时提供的文件——自己的操作系统文件、运行时、库；看不到宿主机文件，其他项目也看不到它。
- **自己的系统视图**：见自己的进程、网络接口与主机名，而非宿主机的其余部分。
- **可设资源上限**：可以 cap 内存与 CPU 用量。

容器解决的问题是「在一台机器能跑、在另一台机器失败」：把应用与运行所需的一切打包，使它在每台装有 Docker 的机器上行为一致。因为依赖都在内部，容器不依赖宿主机装了什么；一个项目的后端可以跑 Node.js 22，另一个项目跑旧版 Node.js，互不影响；删除容器不改变机器上其他内容。通常按应用组成部分分别运行容器——一个给后端、一个给数据库，各自独立启停与替换。

## 与虚拟机的区别

官方定义虚拟机是「伪装成一整台计算机」来隔离软件：每个 VM 启动完整操作系统，包括自己的内核。容器不启动操作系统，仍是进程，共享宿主机内核。

- **启动与体积**：没有 guest OS 要启动，所以容器约 1 秒内启动、体积更小，一台机器能跑很多个。
- **隔离强度**：VM 更强——容器靠共享的内核彼此分隔，VM 靠 hypervisor 创建的硬件边界分隔。
- **实践中共存**：云服务器通常是 VM，每个 VM 上跑很多容器；macOS/Windows 上 Docker Desktop 会在它管理的一个小型 Linux VM 里跑 Linux 容器，因为 Linux 容器需要共享 Linux 内核。

## 平台组成

- **Docker Engine**：构建与运行容器的核心运行时。
- **Dockerfile**：定义镜像构建步骤的指令文件；每层指令生成一层，配合多阶段构建、缓存顺序等实践使用。
- **镜像**：分层只读模板，推送到 registry（如 Docker Hub）供分发。
- **Compose**：用 YAML 定义多容器应用的服务、网络与卷，一条命令启停整套环境。
- **Docker Desktop**：面向开发者的桌面应用，内置 Engine、CLI、Compose 与 UI，在 macOS/Windows 上以小型 Linux VM 承载 Linux 容器。

## 与 OCI 和编排的关系

Docker 的镜像和运行时遵守 OCI 规范，因此镜像能被其他符合 OCI 的工具消费；运行时链路是镜像经解包成为 bundle，再由底层运行时创建进程。生产规模的多节点部署通常由 Kubernetes 等编排平台接管，Docker 更多承担**构建镜像与本地/单机运行**的角色；Kubernetes 通过 CRI 调用容器运行时，而非直接调用 dockerd。

## 常见失败模式

- 把容器当轻量 VM：在容器里跑多个进程、装 SSH、原地改配置。
- 依赖宿主机已安装内容，破坏"一次构建、到处运行"的前提。
- 用可变 tag 分发镜像，同一 tag 在不同时间拉到不同内容。
- 镜像烘焙密钥，或把明文凭据打进层。
- 数据写进容器可写层而非 volume，容器替换时数据丢失。
- 用 Compose 跑多容器本地环境，却把这套配置直接当生产编排方案。

## 参考资料

- Docker 文档：https://docs.docker.com
