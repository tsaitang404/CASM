# CASM API接口规范文档

CASM(Cyber Asset Survey & Mapping)网络空间测绘系统 API 文档
版本: 2.6.2

## 代码位置说明

所有API接口都在 `/data/CASM/app/main.py` 中注册，具体实现位于 `/data/CASM/app/routes/` 目录下：

### 核心功能接口
- 任务管理: `/app/routes/task.py`
- 策略管理: `/app/routes/policy.py`
- Fofa任务: `/app/routes/taskFofa.py`
- Github任务: `/app/routes/github_task.py`
- 定时任务: `/app/routes/task_schedule.py`

### 资产管理接口
- 域名资产: `/app/routes/assetDomain.py`
- IP资产: `/app/routes/assetIP.py`
- 站点资产: `/app/routes/assetSite.py`
- 资产范围: `/app/routes/assetScope.py`

### 扫描结果接口
- 域名信息: `/app/routes/domain.py`
- IP信息: `/app/routes/ip.py`
- 站点信息: `/app/routes/site.py`
- URL信息: `/app/routes/url.py`
- 服务信息: `/app/routes/service.py`
- 文件泄露: `/app/routes/fileleak.py`
- 证书信息: `/app/routes/cert.py`
- 漏洞信息: `/app/routes/vuln.py`

### 工具与插件接口
- POC管理: `/app/routes/poc.py`
- 指纹识别: `/app/routes/fingerprint.py`
- 指纹统计: `/app/routes/stat_finger.py`
- NPOC服务: `/app/routes/npoc_service.py`
- Nuclei结果: `/app/routes/nuclei_result.py`
- Web信息收集: `/app/routes/wih.py`

### 系统功能接口
- 用户管理: `/app/routes/user.py`
- 导出功能: `/app/routes/export.py`
- 调度管理: `/app/routes/scheduler.py`
- 控制台: `/app/routes/console.py`
- 批量导出: `/app/routes/batchExport.py`

## API 认证
所有接口都需要在请求头中携带 Token 进行认证：
```
Header: {
    "Token": "your-auth-token"
}
```

## 接口清单

### 1. 策略管理 (/api/policy)

#### 1.1 添加策略
- 请求方法: POST
- 路径: /api/policy/add/
- 描述: 新增一个策略配置
- 实现位置: `/app/routes/policy.py`
- 请求参数:
  ```json
  {
    "name": "策略名称",  // 必填
    "desc": "策略描述信息",  // 可选
    "policy": {  // 必填
      "domain_config": {  // 域名配置
        "domain_brute": false,  // 是否开启域名爆破
        "domain_brute_type": "test",  // 域名爆破类型: test/big/bigbig
        "alt_dns": false,  // 是否开启DNS字典智能生成
        "dns_query_plugin": false,  // 是否开启DNS查询插件
        "casm_search": false,  // 是否开启CASM搜索
        "search_engines": false  // 是否开启搜索引擎
      },
      "ip_config": {  // IP配置
        "port_scan": true,  // 是否开启端口扫描
        "port_scan_type": "test",  // 端口扫描类型: test/top100/top1000
        "port_custom": "80,443",  // 自定义端口
        "exclude_ports": "",  // 排除端口
        "service_detection": false,  // 是否开启服务识别
        "os_detection": false,  // 是否开启系统识别
        "host_timeout": 0,  // 主机超时时间
        "port_parallelism": 32,  // 端口扫描并发数
        "port_min_rate": 60  // 最小扫描速率
      },
      "site_config": {  // 站点配置
        "site_identify": false,  // 是否开启站点识别
        "site_capture": false,  // 是否开启站点截图
        "site_spider": false,  // 是否开启站点爬虫
        "web_info_hunter": false,  // 是否开启WEB JS信息收集
        "nuclei_scan": false  // 是否开启nuclei扫描
      },
      "file_leak": false,  // 是否开启文件泄露扫描
      "npoc_service_detection": false,  // 是否开启Python服务识别
      "poc_config": [  // POC插件配置
        {
          "plugin_name": "插件名称ID",  // 插件名称
          "enable": true  // 是否启用
        }
      ],
      "brute_config": [  // 弱口令爆破配置
        {
          "plugin_name": "插件名称ID",  // 插件名称
          "enable": true  // 是否启用
        }
      ],
      "scope_config": {  // 资产范围配置
        "scope_id": "资产组范围ID"  // 资产组ID
      }
    }
  }
  ```

#### 1.2 编辑策略
- 请求方法: POST
- 路径: /api/policy/edit/
- 描述: 编辑现有策略配置
- 实现位置: `/app/routes/policy.py`
- 请求参数:
  ```json
  {
    "policy_id": "603c65316591e73dd717d176",  // 必填，策略ID
    "policy_data": {  // 必填，需要更新的策略数据，结构同添加策略
      "name": "更新后的策略名称",
      "desc": "更新后的描述",
      "policy": {
        // 同添加策略中的policy结构
      }
    }
  }
  ```

#### 1.3 删除策略
- 请求方法: POST  
- 路径: /api/policy/delete/
- 描述: 删除指定策略
- 实现位置: `/app/routes/policy.py`
- 请求参数:
  ```json
  {
    "policy_id": ["603c65316591e73dd717d176"]  // 必填，策略ID列表
  }
  ```

#### 响应格式
```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "policy_id": ["603c65316591e73dd717d176"]  // 被操作的策略ID
  }
}
```

#### 策略配置说明

1. 域名配置(domain_config)：
   - domain_brute: 域名爆破开关
   - domain_brute_type: 爆破字典类型(test/big/bigbig)
   - alt_dns: DNS智能生成开关
   - dns_query_plugin: DNS查询插件开关
   - casm_search: CASM搜索开关
   - search_engines: 搜索引擎调用开关

2. IP配置(ip_config)：
   - port_scan: 端口扫描开关
   - port_scan_type: 端口扫描类型(test/top100/top1000)
   - port_custom: 自定义端口列表
   - exclude_ports: 排除端口列表
   - service_detection: 服务识别开关
   - os_detection: 系统识别开关
   - host_timeout: 主机扫描超时时间
   - port_parallelism: 端口扫描并发数
   - port_min_rate: 最小扫描速率

3. 站点配置(site_config)：
   - site_identify: 站点识别开关
   - site_capture: 站点截图开关
   - site_spider: 站点爬虫开关
   - web_info_hunter: WEB JS信息收集开关
   - nuclei_scan: nuclei扫描开关

4. 漏洞检测配置：
   - file_leak: 文件泄露扫描开关
   - npoc_service_detection: Python服务识别开关
   - poc_config: POC插件配置列表
   - brute_config: 弱口令爆破配置列表

5. 资产范围配置(scope_config)：
   - scope_id: 关联的资产组ID

### 2. 任务管理 (/api/task)

#### 2.1 任务查询
- 请求方法: GET
- 路径: /api/task/
- 描述: 任务信息查询
- 查询参数:
  ```json
  {
    "name": "任务名称",
    "target": "任务目标",
    "status": "任务状态",
    "_id": "任务ID",
    "task_tag": "任务标签", 
    "page": "页码",
    "size": "每页数量",
    "options.domain_brute": "是否开启域名爆破",
    "options.domain_brute_type": "域名爆破类型",
    "options.port_scan": "是否开启端口扫描",
    "options.service_detection": "是否开启服务识别",
    "options.service_brute": "是否开启服务弱口令爆破",
    "options.os_detection": "是否开启操作系统识别",
    "options.site_identify": "是否开启站点识别",
    "options.file_leak": "是否开启文件泄露扫描",
    "options.alt_dns": "是否开启DNS字典智能生成",
    "options.search_engines": "是否开启搜索引擎调用"
  }
  ```

#### 2.2 添加任务
- 请求方法: POST
- 路径: /api/task/
- 描述: 提交新任务
- 请求参数:
  ```json
  {
    "name": "任务名称",
    "target": "任务目标"
  }
  ```

#### 2.3 停止任务
- 请求方法: GET
- 路径: /api/task/stop/<task_id>
- 描述: 停止指定任务

#### 2.4 批量停止任务
- 请求方法: POST
- 路径: /api/task/batch_stop/
- 描述: 批量停止任务
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

#### 2.5 删除任务
- 请求方法: POST
- 路径: /api/task/delete/
- 描述: 删除任务
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"],
    "del_task_data": false  // 是否同时删除任务数据
  }
  ```

#### 2.6 重新运行任务
- 请求方法: POST
- 路径: /api/task/restart/
- 描述: 重新下发任务
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

#### 2.7 任务同步
- 请求方法: POST
- 路径: /api/task/sync/
- 描述: 任务资产同步到资产组
- 请求参数:
  ```json
  {
    "task_id": "任务ID",
    "scope_id": "资产范围ID"
  }
  ```

#### 2.8 获取同步范围
- 请求方法: POST
- 路径: /api/task/sync_scope/
- 描述: 根据目标找到要同步的资产分组ID
- 请求参数:
  ```json
  {
    "target": "需要同步的目标"
  }
  ```

### 任务相关状态说明

#### 任务状态(status)
- WAITING: 等待中
- DONE: 已完成
- STOP: 已停止
- ERROR: 出错

#### 任务类型(task_tag)
- task: 资产发现任务
- risk_cruising: 风险巡航任务
- monitor: 监控任务

#### 任务目标类别(type)
- IP: IP任务
- DOMAIN: 域名任务
- RISK_CRUISING: 风险巡航任务

### 任务配置选项说明

任务支持的配置选项包括：
- domain_brute: 域名爆破
- domain_brute_type: 域名爆破类型(test/big/bigbig)
- port_scan: 端口扫描
- service_detection: 服务识别
- service_brute: 服务弱口令爆破
- os_detection: 操作系统识别
- site_identify: 站点识别
- site_capture: 站点截图
- file_leak: 文件泄露扫描
- search_engines: 搜索引擎调用
- site_spider: 站点爬虫
- casm_search: CASM搜索
- alt_dns: DNS字典智能生成
- ssl_cert: SSL证书获取
- dns_query_plugin: DNS查询插件
- skip_scan_cdn_ip: 跳过扫描CDN IP
- nuclei_scan: Nuclei扫描
- findvhost: 虚拟主机扫描
- web_info_hunter: Web信息收集

### 响应格式举例

查询任务列表响应:
```json
{
  "code": 200,
  "message": "success", 
  "items": [
    {
      "_id": "任务ID",
      "name": "任务名称",
      "target": "任务目标",
      "status": "任务状态",
      "type": "任务类型",
      "task_tag": "任务标签",
      "start_time": "开始时间",
      "end_time": "结束时间",
      "options": {
        // 任务配置选项
      },
      "service": []  // 任务执行的服务列表
    }
  ],
  "total": 总数量,
  "page": 当前页码,
  "size": 每页数量
}
```

### 3. Fofa任务 (/api/task_fofa)

#### 3.1 测试Fofa查询
- 请求方法: POST
- 路径: /api/task_fofa/test
- 描述: 测试Fofa查询连接
- 请求参数:
  ```json
  {
    "query": "Fofa查询语句"
  }
  ```

#### 3.2 提交Fofa任务
- 请求方法: POST
- 路径: /api/task_fofa/submit
- 描述: 提交Fofa查询任务
- 请求参数:
  ```json
  {
    "query": "Fofa查询语句",
    "name": "任务名称",
    "policy_id": "策略ID"
  }
  ```

### 4. 批量导出 (/api/batch_export)

#### 4.1 站点导出
- 请求方法: POST
- 路径: /api/batch_export/site/
- 描述: 批量导出站点信息
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

#### 4.2 域名导出
- 请求方法: POST
- 路径: /api/batch_export/domain/
- 描述: 批量导出域名信息
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

#### 4.3 IP导出
- 请求方法: POST
- 路径: /api/batch_export/ip/
- 描述: 批量导出IP信息
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

#### 4.4 URL导出
- 请求方法: POST
- 路径: /api/batch_export/url/
- 描述: 批量导出URL信息
- 请求参数:
  ```json
  {
    "task_id": ["任务ID列表"]
  }
  ```

### 5. 资产管理

#### 5.1 资产域名 (/api/asset_domain)

##### 5.1.1 添加资产域名
- 请求方法: POST
- 路径: /api/asset_domain/
- 描述: 添加资产域名
- 请求参数:
  ```json
  {
    "domain": "域名",
    "scope_id": "资产组范围ID",
    "policy_id": "策略ID"
  }
  ```

##### 5.1.2 删除资产域名
- 请求方法: POST
- 路径: /api/asset_domain/delete/
- 描述: 删除资产域名
- 请求参数:
  ```json
  {
    "_id": ["资产域名ID"]
  }
  ```

#### 5.2 资产站点 (/api/asset_site)
相关资产站点接口...

### 6. 文件泄露管理 (/api/fileleak)

#### 6.1 文件泄露查询
- 请求方法: GET
- 路径: /api/fileleak/
- 描述: 文件泄露信息查询
- 查询参数:
  ```json
  {
    "url": "URL",
    "site": "站点",
    "content_length": "body长度",
    "status_code": "状态码",
    "title": "标题",
    "task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 6.2 删除文件泄露
- 请求方法: POST
- 路径: /api/fileleak/delete/
- 描述: 删除文件泄露记录
- 请求参数:
  ```json
  {
    "_id": ["文件泄露记录ID"]
  }
  ```

### 7. 域名任务 (/api/domain)

#### 7.1 域名任务配置选项
支持的配置选项：
- domain_brute: 域名爆破
- domain_brute_type: 域名爆破类型(test/big/bigbig)
- port_scan_type: 端口扫描类型
- port_scan: 是否开启端口扫描
- service_detection: 是否开启服务识别
- service_brute: 是否开启服务弱口令爆破
- os_detection: 是否开启操作系统识别
- site_identify: 是否开启站点识别
- site_capture: 是否开启站点截图
- file_leak: 是否开启文件泄露扫描
- alt_dns: 是否开启DNS字典智能生成
- ssl_cert: 是否开启SSL证书获取
- skip_scan_cdn_ip: 是否跳过扫描CDN IP
- dns_query_plugin: 是否开启DNS查询插件
- nuclei_scan: 是否开启nuclei扫描
- findvhost: 是否开启虚拟主机扫描
- web_info_hunter: 是否开启WEB信息收集

### 8. GitHub任务 (/api/github_task)

#### 8.1 提交GitHub任务
- 请求方法: POST
- 路径: /api/github_task/
- 描述: 下发GitHub监控任务

#### 8.2 删除GitHub任务
- 请求方法: POST
- 路径: /api/github_task/delete/
- 描述: 删除GitHub任务

#### 8.3 停止GitHub任务
- 请求方法: POST
- 路径: /api/github_task/stop/
- 描述: 停止正在运行的GitHub任务

### 9. Nuclei扫描 (/api/nuclei_result)

#### 9.1 Nuclei扫描结果查询
- 请求方法: GET
- 路径: /api/nuclei_result/
- 描述: 查询Nuclei扫描结果

### 10. 调度器 (/api/scheduler)

#### 10.1 任务调度
- 请求方法: POST
- 路径: /api/scheduler/
- 描述: 任务调度配置

### 11. 证书管理 (/api/cert)

#### 11.1 证书查询
- 请求方法: GET
- 路径: /api/cert/
- 描述: 查询SSL证书信息
- 查询参数:
  ```json
  {
    "ip": "IP地址",
    "port": "端口号",
    "cert.subject_dn": "主题名称",
    "cert.issuer_dn": "签发者名称",
    "cert.serial_number": "序列号",
    "cert.validity.start": "开始时间",
    "cert.validity.end": "结束时间",
    "cert.fingerprint.sha256": "SHA-256指纹",
    "cert.fingerprint.sha1": "SHA-1指纹",
    "cert.fingerprint.md5": "MD5指纹",
    "cert.extensions.subjectAltName": "备用名称",
    "task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 11.2 删除证书
- 请求方法: POST
- 路径: /api/cert/delete/
- 描述: 删除SSL证书记录
- 请求参数:
  ```json
  {
    "_id": ["证书记录ID"]
  }
  ```

### 12. 服务管理 (/api/service)

#### 12.1 服务查询
- 请求方法: GET
- 路径: /api/service/
- 描述: 系统服务信息查询
- 查询参数:
  ```json
  {
    "service_name": "系统服务名称",
    "service_info.ip": "IP地址",
    "service_info.port_id": "端口号",
    "service_info.version": "系统服务版本",
    "service_info.product": "产品名称",
    "task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

### 13. 定时任务 (/api/task_schedule)

#### 13.1 创建定时任务
- 请求方法: POST
- 路径: /api/task_schedule/
- 描述: 创建定时执行的任务
- 请求参数:
  ```json
  {
    "policy_id": "策略ID",
    "cron": "Cron表达式",
    "start_date": "开始时间",
    "task_tag": "任务类别(task|risk_cruising)"
  }
  ```

#### 13.2 删除定时任务
- 请求方法: POST
- 路径: /api/task_schedule/delete/
- 描述: 删除定时任务
- 请求参数:
  ```json
  {
    "_id": ["计划任务ID列表"]
  }
  ```

#### 13.3 停止定时任务
- 请求方法: POST
- 路径: /api/task_schedule/stop/
- 描述: 停止定时任务
- 请求参数:
  ```json
  {
    "_id": ["计划任务ID列表"]
  }
  ```

#### 13.4 恢复定时任务
- 请求方法: POST
- 路径: /api/task_schedule/recover/
- 描述: 恢复已停止的定时任务
- 请求参数:
  ```json
  {
    "_id": ["计划任务ID列表"]
  }
  ```

### 14. POC管理 (/api/poc)

#### 14.1 POC信息查询
- 请求方法: GET
- 路径: /api/poc/
- 描述: 查询POC插件信息
- 查询参数:
  ```json
  {
    "plugin_name": "POC名称ID",
    "app_name": "应用名称",
    "scheme": "支持的协议",
    "vul_name": "漏洞名称",
    "plugin_type": "插件类别(poc/brute)",
    "update_date": "更新时间",
    "category": "POC分类",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 14.2 同步POC信息
- 请求方法: GET
- 路径: /api/poc/sync/
- 描述: 更新POC插件信息

#### 14.3 清空POC信息
- 请求方法: GET
- 路径: /api/poc/delete/
- 描述: 清空所有POC插件信息

### 15. 指纹识别 (/api/fingerprint)

#### 15.1 指纹查询
- 请求方法: GET
- 路径: /api/fingerprint/
- 描述: 查询指纹信息
- 查询参数:
  ```json
  {
    "name": "指纹名称",
    "update_date__dgt": "更新时间大于",
    "update_date__dlt": "更新时间小于",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 15.2 添加指纹
- 请求方法: POST
- 路径: /api/fingerprint/
- 描述: 添加新的指纹规则
- 请求参数:
  ```json
  {
    "name": "指纹名称",
    "human_rule": "指纹规则"
  }
  ```

#### 15.3 删除指纹
- 请求方法: POST
- 路径: /api/fingerprint/delete/
- 描述: 删除指纹信息
- 请求参数:
  ```json
  {
    "_id": ["指纹ID"]
  }
  ```

#### 15.4 导出指纹
- 请求方法: GET
- 路径: /api/fingerprint/export/
- 描述: 导出指纹规则

#### 15.5 上传指纹
- 请求方法: POST
- 路径: /api/fingerprint/upload/
- 描述: 批量上传指纹规则
- 请求参数:
  - Content-Type: multipart/form-data
  - 参数名: file
  - 文件格式: JSON

### 16. NPOC服务识别 (/api/npoc_service)

#### 16.1 服务识别查询
- 请求方法: GET
- 路径: /api/npoc_service/
- 描述: 查询NPOC服务识别结果
- 查询参数:
  ```json
  {
    "scheme": "系统服务名称",
    "host": "主机地址",
    "port": "端口号",
    "target": "目标",
    "task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

### 17. 漏洞管理 (/api/vuln)

#### 17.1 漏洞查询
- 请求方法: GET
- 路径: /api/vuln/
- 描述: 漏洞信息查询
- 实现位置: `/app/routes/vuln.py`
- 查询参数:
  ```json
  {
    "plg_name": "插件ID",
    "plg_type": "漏洞类别",
    "vul_name": "漏洞名称",
    "app_name": "应用名称",
    "target": "目标地址",
    "task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 17.2 删除漏洞
- 请求方法: POST
- 路径: /api/vuln/delete/
- 描述: 删除漏洞信息
- 请求参数:
  ```json
  {
    "_id": ["漏洞记录ID列表"]
  }
  ```

### 18. 指纹统计 (/api/stat_finger)

#### 18.1 指纹统计查询
- 请求方法: GET
- 路径: /api/stat_finger/
- 描述: 查询指纹统计信息
- 实现位置: `/app/routes/stat_finger.py`
- 查询参数:
  ```json
  {
    "name": "指纹名称",
    "task_id": "任务ID",
    "cnt": "出现次数",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "name": "Apache",
        "cnt": 15,
        "task_id": "603c65316591e73dd717d176"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10
  }
}
```

### 指纹规则说明

指纹识别支持多种匹配规则：
1. html: 页面内容匹配
2. title: 网站标题匹配
3. headers: HTTP响应头匹配
4. favicon_hash: 图标哈希值匹配

规则格式示例：
```json
{
  "html": ["特征字符串"],
  "title": ["标题关键字"],
  "headers": ["响应头特征"],
  "favicon_hash": ["图标哈希值"]
}
```

指纹规则转换映射关系：
- html -> body
- title -> title
- headers -> header
- favicon_hash -> icon_hash

### 19. GitHub信息收集

#### 19.1 GitHub任务管理 (/api/github_task)

##### 19.1.1 任务信息查询
- 请求方法: GET
- 路径: /api/github_task/
- 描述: 查询GitHub任务信息
- 实现位置: `/app/routes/github_task.py`
- 查询参数:
  ```json
  {
    "name": "任务名称",
    "keyword": "搜索关键字",
    "status": "任务状态",
    "_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

##### 19.1.2 添加任务
- 请求方法: POST
- 路径: /api/github_task/
- 描述: 添加GitHub信息收集任务
- 请求参数:
  ```json
  {
    "name": "任务名称",  // 必填
    "keyword": "搜索关键字"  // 必填
  }
  ```

##### 19.1.3 停止任务
- 请求方法: POST
- 路径: /api/github_task/stop/
- 描述: 停止正在运行的GitHub任务
- 请求参数:
  ```json
  {
    "_id": ["任务ID列表"]  // 必填
  }
  ```

##### 19.1.4 删除任务
- 请求方法: POST
- 路径: /api/github_task/delete/
- 描述: 删除GitHub任务及其结果
- 请求参数:
  ```json
  {
    "_id": ["任务ID列表"]  // 必填
  }
  ```

#### 19.2 GitHub监控管理 (/api/github_scheduler)

##### 19.2.1 监控任务查询
- 请求方法: GET
- 路径: /api/github_scheduler/
- 描述: 查询GitHub监控任务信息
- 实现位置: `/app/routes/github_scheduler.py`
- 查询参数:
  ```json
  {
    "name": "任务名称",
    "keyword": "监控关键字",
    "status": "监控状态",
    "page": "页码",
    "size": "每页数量"
  }
  ```

##### 19.2.2 添加监控
- 请求方法: POST
- 路径: /api/github_scheduler/
- 描述: 添加GitHub定时监控任务
- 请求参数:
  ```json
  {
    "name": "监控名称",  // 必填
    "keyword": "监控关键字",  // 必填
    "cron": "Cron表达式"  // 必填，定时任务表达式
  }
  ```

##### 19.2.3 更新监控
- 请求方法: POST
- 路径: /api/github_scheduler/update/
- 描述: 修改GitHub监控任务
- 请求参数:
  ```json
  {
    "_id": "监控任务ID",  // 必填
    "name": "新监控名称",  // 可选
    "keyword": "新监控关键字",  // 可选
    "cron": "新Cron表达式"  // 可选
  }
  ```

##### 19.2.4 删除监控
- 请求方法: POST
- 路径: /api/github_scheduler/delete/
- 描述: 删除GitHub监控任务
- 请求参数:
  ```json
  {
    "_id": ["监控任务ID列表"]  // 必填
  }
  ```

##### 19.2.5 停止监控
- 请求方法: POST
- 路径: /api/github_scheduler/stop/
- 描述: 停止GitHub监控任务
- 请求参数:
  ```json
  {
    "_id": ["监控任务ID列表"]  // 必填
  }
  ```

##### 19.2.6 恢复监控
- 请求方法: POST
- 路径: /api/github_scheduler/recover/
- 描述: 恢复已停止的GitHub监控任务
- 请求参数:
  ```json
  {
    "_id": ["监控任务ID列表"]  // 必填
  }
  ```

#### 19.3 GitHub结果管理

##### 19.3.1 任务结果查询 (/api/github_result)
- 请求方法: GET
- 路径: /api/github_result/
- 描述: 查询GitHub任务的检索结果
- 实现位置: `/app/routes/github_result.py`
- 查询参数:
  ```json
  {
    "path": "文件路径",
    "repo_full_name": "仓库名称",
    "human_content": "内容",
    "github_task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

##### 19.3.2 监控结果查询 (/api/github_monitor_result)
- 请求方法: GET
- 路径: /api/github_monitor_result/
- 描述: 查询GitHub监控的结果
- 实现位置: `/app/routes/github_monitor_result.py`
- 查询参数:
  ```json
  {
    "path": "文件路径",
    "repo_full_name": "仓库名称",
    "human_content": "内容",
    "keyword": "关键字",
    "github_scheduler_id": "监控任务ID",
    "github_task_id": "任务ID",
    "page": "页码",
    "size": "每页数量"
  }
  ```

#### GitHub任务状态说明
- WAITING: 等待执行
- SEARCH: 正在搜索
- FETCH: 正在获取内容
- DONE: 已完成
- STOP: 已停止
- ERROR: 出错

#### GitHub监控状态说明
- RUNNING: 正在运行
- STOP: 已停止
- ERROR: 运行出错

## 响应格式
所有接口统一返回格式：
```json
{
  "code": 200,  // 状态码，200表示成功
  "message": "Success",  // 状态信息
  "data": {}  // 返回的数据
}
```

## 注意事项
1. 所有请求需要在header中携带Token进行认证
2. 策略配置中的插件配置需要确保插件在系统中存在
3. 批量导出接口支持多个任务ID同时导出
4. Fofa相关接口需要系统配置了有效的Fofa API Key

## 错误码说明

各接口可能返回的错误码：
- Success: 操作成功
- NotFoundTaskID: 未找到任务ID
- TaskTargetIsEmpty: 任务目标为空
- ExcludePortsInvalid: 排除端口配置无效
- FofaKeyError: Fofa Key未配置
- FofaConnectError: Fofa连接错误

## 特殊功能说明

### 风险巡航任务
系统支持通过POC配置进行风险巡航任务：
1. 支持服务识别（纯Python实现）
2. 支持自定义POC插件配置
3. 支持自定义爆破插件配置
4. 支持自定义资产范围配置

### 指纹识别功能
1. 支持Web指纹识别规则管理
2. 支持规则导入导出
3. 支持批量规则上传
4. 支持网站标题、header、favicon等多维度规则匹配