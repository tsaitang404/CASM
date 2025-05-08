## CASM( Cyber Asset Survey & Mapping )网络空间测绘系统


### 简介

“网络空间测绘系统”是本项目的名称，英文为 Cyber Asset Survey & Mapping（CASM）。该系统旨在对互联网资产进行快速侦察和关联分析，帮助安全团队或渗透测试人员建立基础资产信息库，发现潜在的薄弱点和攻击面。通过自动化的资产发现、端口扫描、服务识别、指纹识别等功能，系统能够有效支持资产管理和安全防护工作，是网络安全领域的重要工具。

### 修改内容
1. 容器以centos8为基础镜像
2. 默认情况在单docker运行demo
3. 使用反向代理源（Vault源）
4. 使用反向代理pip源
5. 加入指纹库(eHole`1017`、ehole_magic`24981`、EHole_magic_magic`25715`、FingerprintHub`2839`、dismap`4598`，去重后`21545`，可以手动更新，使用CASM导出的格式，或者直接改json文件通过docker内源码安装)`docker快速安装没有ehole_magic相关指纹，去重后5k多，可以手动更新`
6. nmap组件
7. nuclei组件
8. tools下NPoC、casm_files、geoip
9.  数据库优化 增大超时时间
10. 高并发支持
11. 使用反向代理docker官方源

### 系统要求

建议采用**Docker内源码安装**方式运行。
系统配置建议：CPU:4线程 内存:8G 带宽:10M。


如遇mongod服务问题导致`timeout of 12000ms exceeded`，请尝试在docker启动中加入路径`-v /sys/fs/cgroup:/sys/fs/cgroup`

### Docker 内源码安装

```bass
docker run --privileged -it -d -p 5003:5003 --name=casm --restart=always centos /usr/sbin/init
docker exec -it casm bash
# docker内运行，通过源码安装CASM
curl https://raw.githubusercontent.com/tsaitang404/CASM/master/misc/setup-casm.sh >install.sh
bash install.sh
exit
```

docker内执行后直接exit退出即可


### 源码安装

如果在其他目录可以创建软连接，且安装了四个服务分别为`casm-web`, `casm-worker`, `casm-worker-github`, `casm-scheduler`

```
wget https://raw.githubusercontent.com/tsaitang404/CASM/master/misc/setup-casm.sh
chmod +x setup-casm.sh
./setup-casm.sh
```

### 查看服务状态

```
systemctl status casm-web
systemctl status casm-worker
systemctl status casm-worker-github
systemctl status casm-scheduler
```

# 删除镜像
docker rmi casm

# 改poc，poc位置/opt/NPoC
docker exec -it casm bash
systemctl restart casm*

# 改指纹，/opt/CASM/tools/指纹数据.json
docker exec -it casm bash
cd /opt/CASM && python3.6 tools/add_finger.py
```
### 特性

1. 域名资产发现和整理
2. IP/IP 段资产整理
3. 端口扫描和服务识别
4. WEB 站点指纹识别
5. 资产分组管理和搜索
6. 任务策略配置
7. 计划任务和周期任务
8. Github 关键字监控
9. 域名/IP 资产监控
10. 站点变化监控
11. 文件泄漏等风险检测
12. nuclei PoC 调用



### 任务选项说明

| 编号 | 选项            | 说明                                                         |
| ---- | --------------- | ------------------------------------------------------------ |
| 1    | 任务名称        | 任务名称                                                     |
| 2    | 任务目标        | 任务目标，支持IP，IP段和域名。可一次性下发多个目标           |
| 3    | 域名爆破类型    | 对域名爆破字典大小, 大字典：常用2万字典大小。测试：少数几个字典，常用于测试功能是否正常 |
| 4    | 端口扫描类型    | ALL：全部端口，TOP1000：常用top 1000端口，TOP100：常用top 100端口，测试：少数几个端口 |
| 5    | 域名爆破        | 是否开启域名爆破                                             |
| 6    | DNS字典智能生成 | 根据已有的域名生成字典进行爆破                               |
| 7    | 域名查询插件    | 已支持的数据源为13个，`alienvault`, `certspotter`,`crtsh`,`fofa`,`hunter` 等 |
| 8    | 历史查询        | 对casm历史任务结果进行查询用于本次任务                        |
| 9    | 端口扫描        | 是否开启端口扫描，不开启站点会默认探测80,443                 |
| 10   | 服务识别        | 是否进行服务识别，有可能会被防火墙拦截导致结果为空           |
| 11   | 操作系统识别    | 是否进行操作系统识别，有可能会被防火墙拦截导致结果为空       |
| 12   | SSL 证书获取    | 对端口进行SSL 证书获取                                       |
| 13   | 跳过CDN         | 对判定为CDN的IP, 将不会扫描端口，并认为80，443是端口是开放的 |
| 14   | 站点识别        | 对站点进行指纹识别                                           |
| 15   | 搜索引擎调用    | 利用搜索引擎搜索下发的目标爬取对应的URL和子域名              |
| 16   | 站点爬虫        | 利用静态爬虫对站点进行爬取对应的URL                          |
| 17   | 站点截图        | 对站点首页进行截图                                           |
| 18   | 文件泄露        | 对站点进行文件泄露检测，会被WAF拦截                          |
| 19   | Host 碰撞       | 对vhost配置不当进行检测                                      |
| 20   | nuclei 调用     | 调用nuclei 默认PoC 对站点进行检测 ，会被WAF拦截，请谨慎使用该功能 |
| 21   | WIH 调用        | 调用 WebInfoHunter 工具在JS中收集域名,AK/SK等信息            |
| 22   | WIH 监控任务    | 对资产分组中的站点周期性 调用 WebInfoHunter 工具在JS中域名等信息进行监控 |

### FAQ


