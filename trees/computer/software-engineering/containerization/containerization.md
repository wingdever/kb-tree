---
description: "Containerization and deployment: image layers, OCI runtime, Kubernetes objects, reconciliation, probes, resources, rollouts, Helm, GitOps and hardening"
描述: "容器化与部署：镜像分层、OCI 运行时、Kubernetes 对象、调谐循环、探针、资源、滚动发布、Helm、GitOps 与加固"
name: "Containerization and Deployment"
名称: "容器化部署"
---

# 容器化部署（Containerization and Deployment）

容器化部署把应用及其依赖打包成可移植的不可变制品，再由编排平台按声明的目标状态运行。它解决的是"构建一次、到处运行"与"期望状态自动维持"两件事；它不等于必须上 Kubernetes，也不等于自动获得强隔离。

## 容器不是轻量虚拟机

容器本质上是**带受限视图的 Linux 进程**，共享宿主机内核；虚拟机运行独立 guest kernel，由 Hypervisor 提供硬件级虚拟化。容器镜像 MB 级、秒级甚至毫秒级启动，虚拟机 GB 级、分钟级启动；但容器隔离强度是进程级，弱于虚拟机的机器级隔离，逃逸风险更高。

隔离靠两套内核原语配合：namespaces 决定"能看到什么"（pid、net、mnt、ipc、uts、user 等视图），cgroups 决定"能用多少"（CPU、内存、IO、PID 数上限）。再叠加 capabilities、seccomp、AppArmor/SELinux 与 rootfs 切换构成完整边界。因为共享内核，宿主内核漏洞或配置失当会直接暴露宿主机——普通容器不宜作为强多租户的硬隔离边界；需要更强隔离时用沙箱运行时（gVisor、Kata）并通过 RuntimeClass 调度。

## 镜像分层与构建

镜像是多条只读层堆叠的只读模板，Dockerfile 中每条指令生成一层；容器启动时在顶层追加一个**可写层**，所有写入只发生在这一层。UnionFS（主流为 OverlayFS）把多层合并为统一视图：修改下层文件触发写时复制（CoW），删除通过 whiteout 标记隐藏下层文件。多个容器共享全部只读层，只各自持有可写层，因此节省磁盘并加快分发。CoW 意味着大文件修改有 IO 开销，IO 敏感数据应走 volume。

构建要点：

- **多阶段构建**：构建阶段装编译器与 SDK，最终阶段只 `COPY --from=` 编译产物，显著缩小体积与攻击面。
- **基础镜像**：优先官方镜像与可信发布者镜像，尽量小；构建与生产用两种镜像，生产用更瘦的运行时镜像。Alpine、distroless、语言 slim 变体是常见选择——少装包等于少一片漏洞暴露面。
- **指令顺序服务缓存**：变化少的（装系统包）在前，变化频繁的（复制应用代码）在后；`apt-get update` 必须与 `apt-get install` 写在同一条 RUN 中，结尾清理包列表。
- **.dockerignore**：排除 `.git`、依赖目录、本地虚拟环境与 `.env`、`.pem` 等，避免进入构建上下文。
- **标签可变、摘要固定**：tag 会被发布方重新指向新版本；严格锁定时用 `FROM image@sha256:...`，代价是放弃自动安全修复，应配合受控更新流程而非长期依赖 `:latest`。
- **运行时卫生**：容器尽量 ephemeral，一个容器一个关注点；`ENTRYPOINT` 用 exec 形式让应用成为 PID 1 以接收信号；`USER` 切非 root 并显式指定 UID/GID；`WORKDIR` 用绝对路径；在 CI 中构建并测试镜像。

镜像要**定期重建**而不是原地修改：`--pull` 拉取更新后的基础镜像，`--no-cache` 重跑全部指令，两者作用不同且可合用。

## OCI 规范与运行时

Open Container Initiative 定义三个规范：image-spec（镜像归档格式、manifest 与 config schema）、runtime-spec（如何执行解包到磁盘的 filesystem bundle）、distribution-spec（registry 拉取/推送 API）。典型链路是：拉取 OCI 镜像 → 解包为 OCI Runtime filesystem bundle → 由 OCI Runtime 执行。低层运行时（runc、crun）真正创建进程，高层运行时（containerd、CRI-O）负责拉镜像、解层、网络与生命周期，Kubernetes 通过 CRI 调用它们。这条链路解释了为什么 Kubernetes 早已不直接用 dockerd。

## Kubernetes 核心对象

集群控制面由 kube-apiserver（唯一前端，可水平扩展）、etcd（唯一数据源，必须备份）、kube-scheduler 与 kube-controller-manager 构成；节点侧有 kubelet、kube-proxy（CNI 自带转发时可不需要）与容器运行时，CNI 插件负责 Pod IP 与连通性。

| 对象 | 定位 | 关键事实 |
|---|---|---|
| Pod | 最小可部署单元，一个或多个共享网络命名空间与存储卷的容器 | Pod 是临时的，IP 会变 |
| Deployment | 为无状态工作负载提供 Pod 与 ReplicaSet 的声明式更新 | 仅 `.spec.template` 变更触发 rollout；扩缩容不触发 |
| Service | 为一组 Pod 提供稳定 IP/DNS 与负载均衡 | 因 Pod 临时而需要固定入口；由 kube-proxy 实现转发 |
| Ingress | 集群外 HTTP/HTTPS 入口规则 | 需 Ingress Controller 按 host/path 路由到 Service |
| ConfigMap | 非机密键值配置，上限 1 MiB | 不提供保密或加密；卷挂载会最终一致地自动更新，环境变量注入不会 |
| Secret | 少量敏感数据 | 默认在 etcd 中未加密；`data` 是 base64 编码，不是加密 |

ConfigMap 与 Secret 都支持 `immutable: true` 以防误改并降低 apiserver 负载，代价是只能删除重建。Secret 的安全实践至少包括：etcd 静态加密、RBAC 最小权限、限制可访问的容器、考虑外部密钥存储。明文 Secret 绝不进 Git。

## 声明式与调谐循环

Kubernetes 的运行模型由三件东西构成：**目标状态、当前观测状态、reconcile 流程**。链路是：用户提交 YAML → API Server 认证、鉴权与准入后写入 etcd 作为目标记录 → 控制器通过 watch/informer/workqueue 感知变化 → 在 reconcile 中创建、更新或删除下游对象 → 持续循环。控制器只看"当前 vs 期望"的差异，彼此不直接交互，用水平触发保证不漏事件。

这是自愈能力的全部秘密，也是排障的钥匙：Pod 反复 OOM 往往是 requests/limits 配错，Service 不通往往是 selector 没匹配上标签。声明式的另一面是**不要在集群里手工改**——下游改动会被控制器拉回，这正是 GitOps 成立的前提。

## 健康检查与资源约束

三类探针各司其职：

- **startupProbe**：仅在启动时执行，成功前 liveness/readiness 都不运行，专门给慢启动留时间；阈值乘积要覆盖最坏启动时间。
- **livenessProbe**：判断进程是否卡死，失败达阈值则重启容器。必须只反映**不可恢复故障**，不要检查依赖——数据库抖一下就重启所有副本会变成级联故障。
- **readinessProbe**：判断是否可以接流量，失败时把 Pod IP 从匹配 Service 的 EndpointSlice 中移除；适合恢复期与过载期摘流。

探针支持 exec、httpGet（2xx–3xx 算成功）、tcpSocket 与 gRPC。资源 requests 决定调度，limits 由 kubelet/内核强制。内存**不可压缩**，超 limit 触发 OOMKill，不设内存 limit 的容器可能拖垮整节点；CPU **可压缩**，超 limit 只是被节流，表现为难以定位的尾延迟。requests 全等于 limits 为 Guaranteed，部分小于为 Burstable，完全未设为 BestEffort 且最先被驱逐——生产工作负载应用前两类。

## 滚动更新与回滚

Deployment 仅在 `.spec.template` 变更时触发 rollout，扩缩容不触发也不创建 revision——这解释了为什么回滚只回滚模板部分。默认策略 RollingUpdate 用两个旋钮：`maxUnavailable`（默认 25%，可降到 0）与 `maxSurge`（默认 25%），二者不能同时为 0。过程是新建 ReplicaSet → 逐步扩容 → 同步缩容旧 RS → 旧 RS 归零；滚动中途再次更新会立即改道而不等旧 rollout 完成。

新 Pod 卡在 `ImagePullBackOff` 时控制器会按 `maxUnavailable` 停止扩大新 RS；`progressDeadlineSeconds`（默认 600s）超时后状态给出 `Progressing=False / reason=ProgressDeadlineExceeded`，但 Kubernetes **只报告状态、不自动动作**，自动回滚要上层工具（Argo Rollouts、Flagger）。回滚用 `kubectl rollout history` / `kubectl rollout undo`；历史由 `revisionHistoryLimit` 控制，设为 0 就无法回滚。`.spec.selector` 创建后不可变，必须重建。

## 包管理与 GitOps

Helm 是 Kubernetes 的包管理器，核心概念是 Chart（Chart.yaml + values.yaml + templates/ 的包）、Repository 与 Release（一次安装的运行实例，每次 install/upgrade/rollback 产生新 revision），用 Go template 渲染，支持 rollback 与生命周期 hooks。Kustomize 是无模板的配置定制工具，用 base + overlay 与 strategic-merge/JSON6902 patch 表达环境差异，已内置于 kubectl。

判据按消费者划分：要打包给他人安装、要版本与依赖图、要 release 生命周期与回滚、要安装社区软件 → Helm；只是管理自己环境之间的差异、想要可评审的纯 YAML diff → Kustomize。现实主流是两者并用：Helm 装第三方、Kustomize 覆盖自有配置。

GitOps 四条原则：声明式、版本化且不可变、由目标环境内的 agent 自动拉取、持续协调纠正偏差。后两条是它与"YAML 存 Git"的本质分界。收益是流水线不再需要生产集群凭证、每次生产变更都有 commit 审计链、`git revert` 即回滚、漂移自动纠正、指向仓库即可重建集群。常用结构是应用仓库与配置仓库分离，配置仓库内 base + overlays，环境晋升改为改镜像 tag 的 PR，并开启 selfHeal 与 prune。Argo CD 与 Flux 是两类主流实现。

## 不可变基础设施

不可变基础设施指部署后不再修改、只做替换：更新应用、改配置、打补丁的方式是构建带变更的新制品并部署替换，而不是登录服务器修改。收益是消除配置漂移、回滚等于重新部署上一版制品、天然产生审计轨迹、与自动扩缩容契合。载体可以是虚拟机镜像（Packer + Terraform）或容器镜像。制品中永远不要烘焙密钥，运行时从密钥管理系统获取动态凭证。容器侧的另一半是运行时 `readOnlyRootFilesystem: true`，要求所有写路径（通常至少 `/tmp`）挂 emptyDir。

## 容器安全加固

权威基线包括 NSA/CISA Kubernetes 加固指南、CIS Kubernetes Benchmark、NIST SP 800-190 与 Pod Security Standards。PodSecurityPolicy 已被移除，继任者是 Pod Security Admission（通过命名空间标签在 Privileged / Baseline / Restricted 三档间强制执行）。Restricted 档的关键字段：

- `allowPrivilegeEscalation: false`——不写时默认是 true，"字段缺失"本身就是发现项。
- `runAsNonRoot: true` 且 `runAsUser` 不为 0——容器级 `runAsUser: 0` 会推翻 Pod 级设置，两层都要查；distroless 镜像需配数字 UID。
- `seccompProfile.type` 为 RuntimeDefault 或 Localhost，Unconfined 与不设置都不允许。
- `capabilities.drop: ["ALL"]`，最多加回 `NET_BIND_SERVICE`；禁 hostPath 等卷类型，禁 hostNetwork/hostPID/hostIPC。
- 进阶项：`readOnlyRootFilesystem: true`、`automountServiceAccountToken: false`（不需要调 API 的进程留着 SA token 只是给攻击者送礼）。

非 root 最好在构建期落实（Dockerfile `USER` + 显式 UID/GID），而非只在部署期兜底。镜像扫描应前置到构建期并配合准入拦截，但扫描耗时、误判与"镜像里检测到漏洞但代码不走那条路径"的假阳性要求策略支持例外清单与风险评分；构建时扫干净的镜像几天后就会出现新 CVE，注册表与运行时的持续扫描同样必需。供应链方面用 digest 而非可变 tag、签名并校验、每个构建产出 SBOM。

## 成本与复杂度权衡

容器化不等于必须上 Kubernetes。单应用、中等流量时，Docker Compose、托管容器服务或 Serverless 容器能用低得多的运维开销提供编排能力。Kubernetes 的正当理由是多个需独立扩缩的服务、零停机发布与自愈式替换失败容器。

成本不只是集群账单：

- **镜像体积即弹性速度**：节点拉 GB 级镜像要几分钟，自动扩缩容会被拉长。
- **复杂度账单**：控制面、CRI、CNI、CSI、Ingress Controller、策略引擎、GitOps 控制器逐层叠加，每层都要人维护、升级、排障。
- **资源账单**：requests 设高集群缩不下去，设低调度不准或被驱逐；CPU limit 是典型的"省钱换尾延迟"决策。
- **可用性成本**：PodDisruptionBudget、反亲和与拓扑打散省下的资源，会在节点升级或 spot 回收时一次性还回去。
- **安全成本**：Restricted 加固会让部分镜像起不来（要写 `/tmp`、绑定低端口），必须改镜像而不是放宽策略。

落地顺序建议：先容器化（Dockerfile 卫生 + 非 root + 扫描）→ 本地用 Compose 跑多服务 → 需要编排时先试托管容器平台 → 确有多服务独立扩缩与零停机需求再上托管 Kubernetes → 之后依次引入 Helm/Kustomize、探针与资源约束、Pod Security Admission 与 NetworkPolicy、GitOps，最后才谈渐进式发布与多集群。

## 常见失败模式

- 把容器当轻量 VM，在容器里跑多个进程、装 SSH、原地改配置。
- 不设内存 limit，或用 BestEffort 跑生产负载。
- livenessProbe 检查依赖，下游抖动引发全副本重启的级联故障。
- 用可变 tag 部署，同一 tag 在不同时间拉到不同内容。
- 镜像烘焙密钥，或把明文 Secret 提交进 Git。
- 只在准入时扫描镜像，既拖慢 Pod 启动又产生大量误判；缺少持续扫描。
- 集群里手工改资源，被控制器拉回后反复排查"配置丢失"。
- 一次上齐 Helm、GitOps、服务网格、渐进式发布，复杂度超出团队维护能力。

## 参考资料

- Docker 构建最佳实践：https://docs.docker.com
- OCI 规范：https://opencontainers.org
- Kubernetes 文档：https://kubernetes.io/docs
- OpenGitOps 原则：https://opengitops.dev
- NSA/CISA Kubernetes 加固指南，未附固定链接
