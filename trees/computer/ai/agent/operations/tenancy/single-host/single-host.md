---
description: "Single-host multi-tenant deployment: cgroup slices, container hardening, disk quotas and isolation tests"
描述: "单机多租户落地：cgroup 限额、容器加固、磁盘配额与隔离验证"
name: "Single-Host Multi-Tenancy"
名称: "单机多租户落地"
---

# 单机多租户落地

一台轻量服务器（常见 2 核 4G）要同时服务多个租户，先接受一个前提：**大家共用一个内核，能做的是命名空间级隔离，不是硬件级隔离**。这个级别对同一组织的多个部门、或半信任的客户够用；对完全互不信任、还会跑任意代码的外部客户，容器只能降低风险，不能当安全边界——真要强隔离得上微虚拟机或加机器。

轻量机上真正会炸的通常不是内核逃逸，而是三件事：磁盘被写满、内存被吃光、进程数爆炸。所以优先级是**先把资源上限钉死，再谈隔离**。

## 先分清三类隔离

- **计算**：租户能跑什么、能占多少 CPU/内存/进程/磁盘。
- **数据**：文件、数据库、向量索引、缓存能不能互相看见。
- **身份与网络**：谁被允许声称自己是某租户、能往哪里出网。

三者要分别实现，只做其中一个都不算隔离。

## 按租户规模选形态

| 场景 | 形态 | 代价 |
|---|---|---|
| ≤ 5 个租户，每个要装依赖、跑工具 | 每租户一个长期容器 + 独立数据卷 + cgroup 限制 | 每容器约 50–100MB 常驻，2 核 4G 跑得动 |
| 10 个以上，主要是对话与检索、偶尔跑代码 | 单容器内每租户一个进程 + 独立 uid + systemd slice；代码执行按需起一次性 job 容器 | 最省内存，隔离靠进程级 |
| 完全互不信任且跑任意代码 | 一租户一微虚拟机，或 gVisor 收敛系统调用 | 轻量机上不现实，需要加机器或换托管沙箱 |

代码执行一律按需处理：每次调用起一次性容器或进程，跑完即销毁。长期开着的容器风险会累积——依赖被改、临时文件堆积、凭据残留。

## 主机层：先把上限钉死

**资源按租户切 slice。** systemd 原生支持，不用额外组件：

```ini
# /etc/systemd/system/agent-tenant-a.slice
[Slice]
CPUQuota=50%
MemoryMax=512M
TasksMax=64
IOWeight=100
```

- `CPUQuota` 按核的百分比算，50% 约等于半核；两个重租户就能吃满一台 2 核机，配额要留出系统余量。
- `TasksMax` 是防 fork bomb 最有效的一条，比事后 `pkill` 可靠。
- `MemoryMax` 一定要小于物理内存的总和，并且给宿主留出空间（见下条）。

**保护宿主自身不被拖死。** 给 sshd、systemd、监控进程设 `MemoryMin`，或调低它们的 `OOMScoreAdjust`。否则一个租户申请大内存时，内核可能挑系统进程下手，机器直接失联。

**磁盘按租户配额。** 轻量机最常见的事故是磁盘写满导致全系统写入失败：

```bash
# XFS 挂载需带 prjquota
mount -o prjquota /dev/vdb /srv
xfs_quota -x -c 'project -s -p /srv/tenants/a 1001' \
          -c 'limit -p bhard=20g 1001' /srv
```

目录结构建议 `/srv/tenants/<tenant>/`，每租户一个项目 id，配额随项目走。没有 XFS 时用独立卷（LVM thin 或 loop 文件加 `size`），本质是让「写满」只影响一个租户。

**日志要有轮转上限。** 容器日志配 `--log-opt max-size=10m --log-opt max-file=3`；宿主的 journald 也要设 `SystemMaxUse`。失控的调试输出几小时就能吃光 40G。

## 容器层：把权限收干净

每个租户容器的启动参数应该是这套：

```bash
docker run -d --name tenant-a \
  --user 10001:10001 \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 100 --memory 512m --cpus 0.5 \
  --network none \
  -v /srv/tenants/a:/data:rw \
  --log-opt max-size=10m --log-opt max-file=3 \
  agent-runtime:base
```

几条硬禁忌：

- **不挂 `/var/run/docker.sock`**：等于把宿主 root 交出去。
- **不用 `--privileged`**，不挂宿主可写目录，不进 host 网络。
- **默认断网**（`--network none`）：要出网时单独接一个只放行白名单域名的代理，并记录目标。
- **密钥不进环境变量**：容器内进程访问本地代理，代理持有凭证并只在允许域名上附加；被注入后打印 `env` 也拿不到真 key。

宿主机侧再加两道：内核保持更新（共享内核意味着内核漏洞就是所有租户的漏洞）；`seccomp` 用默认配置即可，若租户要跑不可信二进制，优先考虑 gVisor 而不是放宽权限。

## 数据层：过滤放在存储侧

- **关系库**：每租户独立 database 或 schema 最省心；共用表时开行级安全（RLS），让过滤在数据库层生效，应用漏写条件也拦得住。
- **向量库**：一租户一 collection 或一 partition；共用索引时检索必须带强制过滤，忘了带就是全库召回。
- **缓存**：键里带租户。提示缓存尤其危险——前缀相同的请求会跨租户命中，别把 A 的文档片段放进共享前缀。
- **对象存储与文件**：前缀或卷按租户划分，签名 URL 绑定租户。

## 身份层：租户 id 只认签名

从 token 的 claim 里取租户，绝不信 `X-Tenant-Id`、`?tenant=` 这类客户端可伪造的来源。一次请求只允许一个租户上下文；跨租户查询走独立的、显式审批的内部接口，不复用用户请求通道。

审计日志每条都要带：租户、用户、agent 版本、动作与参数、凭据 id。缺租户标签的日志，排障时只能全量搜。

## 怎么验证隔离真的成立

配置写完不等于隔离生效，四条探针必做：

1. **跨租户探针**：从租户 A 的 shell 里 `ls /srv/tenants/B`、访问 B 的服务端口、查 B 的 schema，全部必须失败。
2. **配额压测**：让 A 跑满 CPU、写满 20G、开 200 个进程，看 B 的延迟与错误率是否稳定；如果这时 SSH 都连不上，说明限额没生效。
3. **超时清理**：起一个死循环任务，确认到墙钟上限时被 cgroup 整体 kill，而不是只杀父进程留一堆孤儿。
4. **单租户恢复**：用 A 的快照单独回滚，不影响 B 的数据与在途任务。

## 常见失败模式

- 所有容器在同一个默认网桥里，租户间能互相访问端口。
- 用 `pkill -f` 清理超时任务，把同名系统进程一起杀掉；应按 cgroup 整体 kill。
- 单进程多租户架构复用一个全局连接池，租户上下文串线。
- 日志、临时文件、向量条目、备份没纳入租户维度，删租户时残留。
- 备份与恢复按整机做，一个租户的数据损坏只能全量恢复。

## 一个必须说清的边界

单机隔离做完，它仍然是一个单点故障。隔离解决"互相不干扰"，不解决"机器挂了"。轻量机的现实做法是每日快照 + 关键租户数据异地备份，并对租户声明可用性等级——不要在单机上承诺多租户的强隔离与高可用。

## 参考资料

- systemd 资源控制（slice、CPUQuota、MemoryMax、TasksMax）：https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html
- Linux cgroup v2 文档：https://docs.kernel.org/admin-guide/cgroup-v2.html
- Docker run 参数参考（read-only、cap-drop、pids-limit 等）：https://docs.docker.com/reference/cli/docker/container/run/
- gVisor 用户态内核：https://gvisor.dev
