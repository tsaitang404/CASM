# 任务管理接口

提供对任务的创建、查询、停止、删除、重启等管理功能，支持资产发现任务和风险巡航任务等多种类型。

## API概览

| 接口功能     | HTTP方法 | 请求路径                    | 说明                       |
| ------------ | -------- | --------------------------- | -------------------------- |
| 查询任务     | GET      | /api/task/                  | 获取任务列表或特定任务信息 |
| 添加任务     | POST     | /api/task/                  | 创建新的任务               |
| 停止任务     | GET      | /api/task/stop/{task_id}    | 停止特定任务               |
| 批量停止任务 | POST     | /api/task/batch_stop/       | 批量停止多个任务           |
| 删除任务     | POST     | /api/task/delete/           | 删除任务及相关资源         |
| 重新运行任务 | POST     | /api/task/restart/          | 重新运行已完成的任务       |
| 同步任务结果 | POST     | /api/task/sync/             | 将任务结果同步到资产组     |
| 获取同步范围 | POST     | /api/task/sync_scope/       | 查询目标可同步的资产组     |
| 基于策略任务 | POST     | /api/task/policy/           | 通过策略下发任务           |
| 导出任务报告 | GET      | /api/export/{task_id}       | 导出任务资产报告           |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                           |
| ----------- | -------- | -------- | ------------------------------ |
| name        | string   | 否       | 任务名称，支持模糊查询         |
| target      | string   | 否       | 任务目标，支持模糊查询         |
| status      | string   | 否       | 任务状态，如"waiting"、"done"、"error" |
| _id         | string   | 否       | 任务ID                         |
| task_tag    | string   | 否       | 任务标签，如"task"、"risk_cruising" |
| page        | number   | 否       | 页码，默认为1                  |
| size        | number   | 否       | 每页记录数，默认为10           |

### 任务选项参数

| 字段名                    | 类型     | 是否必填 | 说明                        |
| ------------------------- | -------- | -------- | --------------------------- |
| domain_brute              | boolean  | 否       | 是否开启域名爆破            |
| domain_brute_type         | string   | 否       | 域名爆破类型，支持"test"、"small"、"large" |
| port_scan                 | boolean  | 否       | 是否开启端口扫描            |
| port_scan_type            | string   | 否       | 端口扫描类型，支持"test"、"top100"、"top1000"、"all"、"custom" |
| port_custom               | string   | 否       | 自定义端口，如"80,443,22"   |
| service_detection         | boolean  | 否       | 是否开启服务识别            |
| service_brute             | boolean  | 否       | 是否开启服务弱口令爆破      |
| os_detection              | boolean  | 否       | 是否开启操作系统识别        |
| site_identify             | boolean  | 否       | 是否开启站点指纹识别        |
| site_capture              | boolean  | 否       | 是否开启站点截图            |
| file_leak                 | boolean  | 否       | 是否开启敏感文件泄露扫描    |
| search_engines            | boolean  | 否       | 是否调用搜索引擎收集信息    |
| site_spider               | boolean  | 否       | 是否开启站点爬虫            |
| alt_dns                   | boolean  | 否       | 是否开启智能DNS字典生成     |
| ssl_cert                  | boolean  | 否       | 是否收集SSL证书信息         |
| dns_query_plugin          | boolean  | 否       | 是否开启DNS插件查询         |
| skip_scan_cdn_ip          | boolean  | 否       | 是否跳过CDN IP端口扫描      |
| nuclei_scan               | boolean  | 否       | 是否开启nuclei扫描          |
| findvhost                 | boolean  | 否       | 是否开启Host碰撞检测        |
| web_info_hunter           | boolean  | 否       | 是否开启JS信息收集          |

## 通用响应格式

所有API响应都遵循以下格式：

```json
{
  "code": 200,       // 响应码，200表示成功，非200表示出错
  "message": "success", // 响应消息
  "data": {}       // 响应数据，格式因API而异
}
```

### 通用响应字段说明

| 字段名   | 类型   | 说明                                        |
| -------- | ------ | ------------------------------------------- |
| code     | number | 响应码，200表示成功，非200表示出错          |
| message  | string | 响应消息，成功时为"success"，失败时为错误信息 |
| data     | object | 响应数据，不同API返回的数据结构不同         |

## 详细API说明

### 1. 查询任务

**请求方法与地址**：
```
GET /api/task/
```

**查询参数**：

通用字段说明中的基础查询参数，以及：

| 参数名                    | 类型     | 是否必填 | 说明                           |
| ------------------------- | -------- | -------- | ------------------------------ |
| options.domain_brute      | boolean  | 否       | 过滤是否开启域名爆破的任务     |
| options.port_scan         | boolean  | 否       | 过滤是否开启端口扫描的任务     |
| options.site_identify     | boolean  | 否       | 过滤是否开启站点识别的任务     |
| statistic.site_cnt        | number   | 否       | 过滤站点数量等于指定值的任务   |
| statistic.site_cnt__gt    | number   | 否       | 过滤站点数量大于指定值的任务   |
| statistic.site_cnt__lt    | number   | 否       | 过滤站点数量小于指定值的任务   |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 120,
    "page": 1,
    "size": 10,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "示例任务",
        "target": "example.com",
        "status": "done",
        "task_tag": "task",
        "type": "domain",
        "start_time": "2023-05-10T08:30:00.000Z",
        "end_time": "2023-05-10T09:15:00.000Z",
        "options": {
          "domain_brute": true,
          "port_scan": true,
          "site_identify": true
        },
        "statistic": {
          "domain_cnt": 12,
          "ip_cnt": 8,
          "site_cnt": 6
        }
      }
    ]
  }
}
```

**响应字段说明**：

| 字段名                    | 类型     | 说明                        |
| ------------------------- | -------- | --------------------------- |
| data.total                | number   | 符合条件的记录总数          |
| data.page                 | number   | 当前页码                    |
| data.size                 | number   | 每页记录数                  |
| data.items                | array    | 任务记录数组                |
| data.items[].\_id         | string   | 任务唯一ID                  |
| data.items[].name         | string   | 任务名称                    |
| data.items[].target       | string   | 任务目标                    |
| data.items[].status       | string   | 任务状态                    |
| data.items[].task_tag     | string   | 任务标签                    |
| data.items[].type         | string   | 任务类型                    |
| data.items[].start_time   | string   | 任务开始时间                |
| data.items[].end_time     | string   | 任务结束时间                |
| data.items[].options      | object   | 任务选项配置                |
| data.items[].statistic    | object   | 任务结果统计信息            |

### 2. 添加任务

**请求方法与地址**：
```
POST /api/task/
```

**请求体**：
```json
{
  "name": "示例任务",
  "target": "example.com",
  "domain_brute": true,
  "domain_brute_type": "small",
  "port_scan": true,
  "port_scan_type": "top100",
  "service_detection": true,
  "site_identify": true,
  "site_capture": true,
  "file_leak": false,
  "search_engines": true
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "items": [
    {
      "name": "示例任务",
      "target": "example.com",
      "start_time": "-",
      "status": "waiting",
      "type": "domain",
      "task_tag": "task",
      "options": {
        "domain_brute": true,
        "domain_brute_type": "small",
        "port_scan": true,
        "port_scan_type": "top100",
        "service_detection": true,
        "site_identify": true,
        "site_capture": true,
        "file_leak": false,
        "search_engines": true
      },
      "end_time": "-",
      "service": [],
      "celery_id": "abcdef1234567890",
      "task_id": "60f8c2b2e13e4b1e8c8b4567",
      "create_time": "2023-05-11T08:30:00.000Z"
    }
  ]
}
```

**响应字段说明**：

| 字段名            | 类型    | 说明                     |
| ----------------- | ------- | ------------------------ |
| items             | array   | 创建的任务列表           |
| items[].task_id   | string  | 任务唯一ID               |
| items[].name      | string  | 任务名称                 |
| items[].target    | string  | 任务目标                 |
| items[].status    | string  | 任务状态                 |
| items[].type      | string  | 任务类型                 |
| items[].task_tag  | string  | 任务标签                 |
| items[].celery_id | string  | Celery任务ID             |
| items[].options   | object  | 任务配置选项             |

### 3. 停止任务

**方法1: 停止单个任务**

**请求方法与地址**：
```
GET /api/task/stop/{task_id}
```

**路径参数**：

| 参数名   | 类型   | 是否必填 | 说明     |
| -------- | ------ | -------- | -------- |
| task_id  | string | 是       | 任务ID   |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "60f8c2b2e13e4b1e8c8b4567"
  }
}
```

**方法2: 批量停止任务**

**请求方法与地址**：
```
POST /api/task/batch_stop/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {}
}
```

### 4. 删除任务

**请求方法与地址**：
```
POST /api/task/delete/
```

**请求体**：
```json
{
  "del_task_data": true,
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名        | 类型      | 是否必填 | 说明                           |
| ------------- | --------- | -------- | ------------------------------ |
| del_task_data | boolean   | 否       | 是否删除任务数据，默认为false  |
| task_id       | string[]  | 是       | 要删除的任务ID列表             |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

### 5. 重新运行任务

**请求方法与地址**：
```
POST /api/task/restart/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名  | 类型      | 是否必填 | 说明                |
| ------- | --------- | -------- | ------------------- |
| task_id | string[]  | 是       | 要重启的任务ID列表  |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

### 6. 同步任务结果

**请求方法与地址**：
```
POST /api/task/sync/
```

**请求体**：
```json
{
  "task_id": "60f8c2b2e13e4b1e8c8b4567",
  "scope_id": "60f8c2b2e13e4b1e8c8b5678"
}
```

**参数说明**：

| 参数名   | 类型   | 是否必填 | 说明        |
| -------- | ------ | -------- | ----------- |
| task_id  | string | 是       | 任务ID      |
| scope_id | string | 是       | 资产分组ID  |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "task_id": "60f8c2b2e13e4b1e8c8b4567"
  }
}
```

### 7. 获取同步范围

**请求方法与地址**：
```
POST /api/task/sync_scope/
```

**请求体**：
```json
{
  "target": "example.com"
}
```

**参数说明**：

| 参数名 | 类型   | 是否必填 | 说明           |
| ------ | ------ | -------- | -------------- |
| target | string | 是       | 需要同步的目标 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b5678",
        "name": "核心资产组",
        "desc": "公司核心业务系统"
      }
    ]
  }
}
```

### 8. 基于策略任务

**请求方法与地址**：
```
POST /api/task/policy/
```

**请求体**：
```json
{
  "name": "策略任务示例",
  "task_tag": "task",
  "target": "example.com",
  "policy_id": "60f8c2b2e13e4b1e8c8b6789"
}
```

**参数说明**：

| 参数名       | 类型   | 是否必填 | 说明                                     |
| ------------ | ------ | -------- | ---------------------------------------- |
| name         | string | 是       | 任务名称                                 |
| task_tag     | string | 是       | 任务标签，可选值："task"、"risk_cruising" |
| target       | string | 是       | 任务目标                                 |
| policy_id    | string | 是       | 策略ID                                   |
| result_set_id| string | 否       | 结果集ID(仅风险巡航任务可用)             |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "items": [
      {
        "name": "策略任务示例",
        "target": "example.com",
        "status": "waiting",
        "type": "domain",
        "task_tag": "task",
        "task_id": "60f8c2b2e13e4b1e8c8b7890"
      }
    ]
  }
}
```

### 9. 导出任务报告

**请求方法与地址**：
```
GET /api/export/{task_id}
```

**路径参数**：

| 参数名  | 类型   | 是否必填 | 说明   |
| ------- | ------ | -------- | ------ |
| task_id | string | 是       | 任务ID |

**响应**：
Excel文件下载(application/octet-stream)

**响应内容说明**：
Excel文件包含多个工作表，包含以下内容：
- 站点信息：站点URL、标题、指纹、状态码等
- IP信息：IP地址、开放端口、地理位置、运营商等
- 服务信息：服务名称、端口、产品版本等
- 域名信息：域名、解析类型、记录值、关联IP等
- 资产统计：端口、服务、产品统计信息等

## 错误响应

### 通用错误码

| 错误码 | 描述                   | 说明                   |
| ------ | ---------------------- | ---------------------- |
| 102    | CeleryIdNotFound       | 没有找到Celery ID      |
| 103    | NotFoundTask           | 没有找到任务           |
| 104    | TaskIsRunning          | 任务运行中             |
| 105    | TaskIsDone             | 任务已经完成           |
| 1001   | ResultSetIDNotFound    | 结果集ID没有找到       |
| 1002   | ResultSetIsEmpty       | 结果集中目标为空       |
| 1100   | PolicyIDNotFound       | 策略不存在             |
| 1101   | TaskTargetIsEmpty      | 任务目标为空           |
| 500    | Error                  | 系统异常               |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.task_id| string | 任务ID（可选）           |

### 错误示例
任务未找到：
```json
{
  "code": 103,
  "msg": "NotFoundTask",
  "data": {
    "task_id": "不存在的任务ID"
  }
}
```

任务正在运行：
```json
{
  "code": 104,
  "msg": "TaskIsRunning",
  "data": {
    "task_id": "60f8c2b2e13e4b1e8c8b4567"
  }
}
```

任务目标为空：
```json
{
  "code": 1101,
  "msg": "TaskTargetIsEmpty",
  "data": {
    "target": ""
  }
}
```