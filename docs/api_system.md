# 系统状态与通用接口

提供系统状态监控、各类资产批量导出等功能。

## API概览

| 接口功能     | HTTP方法 | 请求路径                    | 说明                       |
| ------------ | -------- | --------------------------- | -------------------------- |
| 系统状态     | GET      | /api/status/                | 获取系统组件状态信息       |
| 批量导出站点 | POST     | /api/batch_export/site/     | 批量导出站点资产           |
| 批量导出域名 | POST     | /api/batch_export/domain/   | 批量导出域名资产           |
| 批量导出IP   | POST     | /api/batch_export/ip/       | 批量导出IP资产             |
| 批量导出URL  | POST     | /api/batch_export/url/      | 批量导出URL资产            |
| 批量导出IP端口 | POST   | /api/batch_export/ip_port/  | 批量导出IP端口信息         |
| 批量导出C段  | POST     | /api/batch_export/cip/      | 批量导出C段信息            |
| 批量导出WIH  | POST     | /api/batch_export/wih/      | 批量导出JS信息资产         |
| 批量导出资产分组IP | POST | /api/batch_export/asset_ip/ | 导出资产分组中的IP       |
| 批量导出资产分组域名 | POST | /api/batch_export/asset_domain/ | 导出资产分组中的域名 |
| 批量导出资产分组站点 | POST | /api/batch_export/asset_site/ | 导出资产分组中的站点 |
| 批量导出资产分组WIH | POST | /api/batch_export/asset_wih/ | 导出资产分组中的JS信息 |

## 通用请求参数

### 任务批量导出参数

| 字段名      | 类型     | 是否必填 | 说明                           |
| ----------- | -------- | -------- | ------------------------------ |
| task_id     | string[] | 是       | 任务ID列表                     |
| format      | string   | 否       | 导出格式，支持"txt"、"csv"、"json"(默认为txt) |

### 资产分组批量导出参数

| 字段名      | 类型     | 是否必填 | 说明                           |
| ----------- | -------- | -------- | ------------------------------ |
| scope_id    | string[] | 是       | 资产分组ID列表                 |
| format      | string   | 否       | 导出格式，支持"txt"、"csv"、"json"(默认为txt) |

## 通用响应格式

所有API响应都遵循以下格式：

```json
{
  "code": 0,       // 响应码，0表示成功，非0表示出错
  "msg": "Success", // 响应消息
  "data": {}       // 响应数据，格式因API而异
}
```

### 通用响应字段说明

| 字段名 | 类型   | 说明                                        |
| ------ | ------ | ------------------------------------------- |
| code   | number | 响应码，0表示成功，非0表示出错              |
| msg    | string | 响应消息，成功时为"Success"，失败时为错误信息 |
| data   | object | 响应数据，不同API返回的数据结构不同         |

## 详细API说明

### 1. 系统状态

**请求方法与地址**：
```
GET /api/status/
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "mongodb": {
      "status": "running",
      "message": "MongoDB连接正常"
    },
    "rabbitmq": {
      "status": "running",
      "message": "RabbitMQ连接正常"
    },
    "scheduler": {
      "status": "running",
      "uptime": "5d 4h",
      "tasks_total": 120,
      "tasks_active": 5
    },
    "workers": {
      "total": 4,
      "active": 3,
      "nodes": [
        {
          "name": "worker1",
          "status": "running",
          "tasks_processed": 267,
          "uptime": "5d 2h"
        },
        {
          "name": "worker2",
          "status": "running",
          "tasks_processed": 198,
          "uptime": "4d 18h"
        },
        {
          "name": "worker3",
          "status": "running",
          "tasks_processed": 145,
          "uptime": "3d 9h"
        },
        {
          "name": "worker4",
          "status": "stopped",
          "tasks_processed": 0,
          "uptime": "0h",
          "error": "Connection refused"
        }
      ]
    },
    "assets": {
      "domains": 1253,
      "ips": 784,
      "sites": 526,
      "services": 1892,
      "vulnerabilities": 47,
      "certificates": 238
    }
  }
}
```

**响应字段说明**：

| 字段名                | 类型    | 说明                     |
| --------------------- | ------- | ------------------------ |
| data.mongodb          | object  | MongoDB状态信息          |
| data.mongodb.status   | string  | 状态:"running"或"error"  |
| data.mongodb.message  | string  | 状态描述信息             |
| data.rabbitmq         | object  | RabbitMQ状态信息         |
| data.scheduler        | object  | 调度器状态信息           |
| data.scheduler.uptime | string  | 调度器运行时间           |
| data.workers          | object  | Worker服务状态信息       |
| data.workers.total    | number  | Worker节点总数           |
| data.workers.active   | number  | 活动Worker节点数         |
| data.workers.nodes    | array   | 各Worker节点详情         |
| data.assets           | object  | 资产统计信息             |
| data.assets.domains   | number  | 域名资产总数             |
| data.assets.ips       | number  | IP资产总数               |
| data.assets.sites     | number  | 站点资产总数             |

### 2. 批量导出站点

**请求方法与地址**：
```
POST /api/batch_export/site/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "format": "csv"
}
```

**参数说明**：
通用请求参数中的任务批量导出参数。

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含站点信息，根据选择的格式不同，内容结构也不同：
- txt格式：每行一个站点URL
- csv格式：包含url、title、status、fingerprint等字段的表格数据
- json格式：包含完整站点信息的JSON数组

### 3. 批量导出域名

**请求方法与地址**：
```
POST /api/batch_export/domain/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "format": "txt"
}
```

**参数说明**：
通用请求参数中的任务批量导出参数。

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含域名信息，根据选择的格式不同，内容结构也不同：
- txt格式：每行一个域名
- csv格式：包含domain、type、record等字段的表格数据
- json格式：包含完整域名信息的JSON数组

### 4. 批量导出IP

**请求方法与地址**：
```
POST /api/batch_export/ip/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "format": "txt"
}
```

**参数说明**：
通用请求参数中的任务批量导出参数。

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含IP信息，根据选择的格式不同，内容结构也不同：
- txt格式：每行一个IP地址
- csv格式：包含ip、location、carrier等字段的表格数据
- json格式：包含完整IP信息的JSON数组

### 5. 批量导出URL

**请求方法与地址**：
```
POST /api/batch_export/url/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "format": "txt"
}
```

**参数说明**：
通用请求参数中的任务批量导出参数。

**响应**：
文件下载（text/plain、application/octet-stream或application/json）

**响应内容说明**：
导出格式不同，内容结构也不同：
- txt格式：每行一个完整URL
- csv格式：包含url、domain、path等字段的表格
- json格式：包含完整URL信息的JSON数组

### 6. 批量导出IP端口

**请求方法与地址**：
```
POST /api/batch_export/ip_port/
```

**请求体**：
```json
{
  "task_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：
通用请求参数中的任务批量导出参数。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含IP和端口组合（格式如：192.168.1.1:80），每行一个IP:端口组合。

## 错误响应

### 通用错误码

| 错误码 | 描述                   | 说明                       |
| ------ | ---------------------- | -------------------------- |
| 500    | Error                  | 系统异常                   |
| 401    | NotLogin               | 用户未登录                 |
| 402    | TaskNotFound           | 未找到指定任务             |
| 403    | ExportFormatNotSupport | 不支持的导出格式           |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.task_id| string | 相关任务ID（可选）       |

### 错误示例
任务不存在：
```json
{
  "code": 402,
  "msg": "TaskNotFound",
  "data": {
    "task_id": "不存在的任务ID"
  }
}
```

格式不支持：
```json
{
  "code": 403,
  "msg": "ExportFormatNotSupport",
  "data": {
    "format": "不支持的格式"
  }
}
```