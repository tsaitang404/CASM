# Celery任务执行与管理接口

提供对 Celery 任务的执行、状态查询和管理功能，支持各种类型的任务执行和撤销。

## API概览

| 接口功能       | HTTP方法 | 请求路径                      | 说明                       |
| -------------- | -------- | ----------------------------- | -------------------------- |
| 获取任务类型   | GET      | /api/celery_task/types/       | 获取所有支持的任务类型     |
| 查询任务列表   | GET      | /api/celery_task/             | 获取所有任务的列表         |
| 创建执行任务   | POST     | /api/celery_task/             | 创建并执行一个新任务       |
| 查询任务状态   | GET      | /api/celery_task/{celery_id}/ | 获取特定任务的状态和详情   |
| 终止任务       | DELETE   | /api/celery_task/{celery_id}/ | 终止并撤销特定任务         |
| 撤销任务       | POST     | /api/celery_task/revoke/      | 通过POST请求撤销任务       |
| 批量撤销任务   | POST     | /api/celery_task/batch_revoke/| 批量撤销多个任务           |
| 活跃任务列表   | GET      | /api/celery_task/active/      | 获取所有活跃任务的列表     |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                           |
| ----------- | -------- | -------- | ------------------------------ |
| celery_id   | string   | 否       | Celery任务ID                   |
| status      | string   | 否       | 任务状态，如"PENDING"、"SUCCESS"、"FAILURE" |
| task_type   | string   | 否       | 任务类型                       |
| page        | number   | 否       | 页码，默认为1                  |
| size        | number   | 否       | 每页记录数，默认为10           |

### 任务状态说明

| 状态名称      | 说明                                 |
| ------------- | ------------------------------------ |
| PENDING       | 任务等待执行                         |
| STARTED       | 任务已开始执行                       |
| RETRY         | 任务执行失败，正在重试               |
| SUCCESS       | 任务执行成功                         |
| FAILURE       | 任务执行失败                         |
| REVOKED       | 任务被撤销                           |

### 任务类型说明

| 类型名称               | 说明                 | 对应值              |
| --------------------- | -------------------- | ------------------- |
| 常规域名任务           | 域名扫描任务         | domain_task         |
| 常规IP任务             | IP扫描任务           | ip_task             |
| PoC运行任务            | 漏洞验证任务         | run_risk_cruising   |
| 域名同步任务           | 同步域名任务         | domain_task_sync_task|
| Fofa查询任务          | Fofa平台查询任务     | fofa_task           |
| 域名监测任务           | 域名监控任务         | domain_exec_task    |
| IP监测任务             | IP监控任务           | ip_exec_task        |
| Github泄露任务         | Github信息泄露检测   | github_task_task    |
| Github泄露监控任务     | Github信息泄露监控   | github_task_monitor |
| 资产站点更新任务       | 更新资产站点信息     | asset_site_update   |
| 资产站点添加任务       | 添加资产站点         | add_asset_site_task |
| 资产WIH更新任务        | 更新资产WIH信息      | asset_wih_update    |

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

### 1. 获取任务类型

**请求方法与地址**：
```
GET /api/celery_task/types/
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "task_types": {
      "domain_task": "常规域名任务",
      "ip_task": "常规IP任务",
      "run_risk_cruising": "PoC运行任务",
      "domain_task_sync_task": "域名同步任务",
      "fofa_task": "Fofa查询任务",
      "domain_exec_task": "域名监测任务",
      "ip_exec_task": "IP监测任务",
      "github_task_task": "Github泄露任务",
      "github_task_monitor": "Github泄露监控任务",
      "asset_site_update": "资产站点更新任务",
      "add_asset_site_task": "资产站点添加任务",
      "asset_wih_update": "资产WIH更新任务"
    }
  }
}
```

### 2. 查询任务列表

**请求方法与地址**：
```
GET /api/celery_task/
```

**查询参数**：

通用字段说明中的基础查询参数均可用于过滤任务列表。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 25,
    "page": 1,
    "size": 10,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "示例任务",
        "target": "example.com",
        "status": "SUCCESS",
        "type": "domain",
        "task_tag": "task",
        "task_type": "domain_task",
        "start_time": "2023-07-10T08:30:00.000Z",
        "end_time": "2023-07-10T09:15:00.000Z",
        "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32"
      },
      // 更多任务...
    ]
  }
}
```

### 3. 创建执行任务

**请求方法与地址**：
```
POST /api/celery_task/
```

**请求体**：
```json
{
  "task_type": "domain_task",
  "data": {
    "name": "示例域名任务",
    "target": "example.com",
    "type": "domain",
    "task_tag": "task",
    "options": {
      "domain_brute": true,
      "domain_brute_type": "small",
      "port_scan": true,
      "site_identify": true
    }
  }
}
```

**参数说明**：

| 参数名     | 类型   | 是否必填 | 说明                      |
| ---------- | ------ | -------- | ------------------------- |
| task_type  | string | 是       | 任务类型                  |
| data       | object | 是       | 任务数据，格式根据任务类型而定 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
    "status": "PENDING"
  }
}
```

### 4. 查询任务状态

**请求方法与地址**：
```
GET /api/celery_task/{celery_id}/
```

**路径参数**：

| 参数名     | 类型   | 是否必填 | 说明        |
| ---------- | ------ | -------- | ----------- |
| celery_id  | string | 是       | Celery任务ID|

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
    "status": "SUCCESS",
    "task_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "示例任务",
    "target": "example.com",
    "type": "domain",
    "task_tag": "task",
    "start_time": "2023-07-10T08:30:00.000Z",
    "end_time": "2023-07-10T09:15:00.000Z"
  }
}
```

### 5. 终止任务

**请求方法与地址**：
```
DELETE /api/celery_task/{celery_id}/
```

**路径参数**：

| 参数名     | 类型   | 是否必填 | 说明        |
| ---------- | ------ | -------- | ----------- |
| celery_id  | string | 是       | Celery任务ID|

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
    "status": "revoked"
  }
}
```

### 6. 撤销任务

**请求方法与地址**：
```
POST /api/celery_task/revoke/
```

**请求体**：
```json
{
  "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
  "terminate": true
}
```

**参数说明**：

| 参数名     | 类型    | 是否必填 | 说明                              |
| ---------- | ------- | -------- | --------------------------------- |
| celery_id  | string  | 是       | Celery任务ID                      |
| terminate  | boolean | 否       | 是否终止任务进程，默认为true      |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
    "status": "revoked"
  }
}
```

### 7. 批量撤销任务

**请求方法与地址**：
```
POST /api/celery_task/batch_revoke/
```

**请求体**：
```json
{
  "celery_ids": ["c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32", "d7b2f1c4-6374-5e9d-bf49-g6d5g0be8d43"],
  "terminate": true
}
```

**参数说明**：

| 参数名     | 类型       | 是否必填 | 说明                              |
| ---------- | ---------- | -------- | --------------------------------- |
| celery_ids | string[]   | 是       | Celery任务ID列表                  |
| terminate  | boolean    | 否       | 是否终止任务进程，默认为true      |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "celery_id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
        "status": "revoked"
      },
      {
        "celery_id": "d7b2f1c4-6374-5e9d-bf49-g6d5g0be8d43",
        "status": "revoked"
      }
    ]
  }
}
```

### 8. 活跃任务列表

**请求方法与地址**：
```
GET /api/celery_task/active/
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "active_tasks": [
      {
        "id": "c6a1e0b3-5263-4d8c-ae38-f5c4f9ad7c32",
        "name": "app.celerytask.casm_task",
        "args": [],
        "kwargs": {"options": {"celery_action": "domain_task", "data": {"task_id": "60f8c2b2e13e4b1e8c8b4567"}}},
        "type": "worker1@host",
        "hostname": "worker1@host",
        "time_start": 1689012345.6789,
        "worker": "celery@worker1",
        "state": "active"
      },
      // 更多任务...
    ]
  }
}
```

## 错误响应

### 通用错误码

| 错误码 | 描述                   | 说明                   |
| ------ | ---------------------- | ---------------------- |
| 102    | CeleryIdNotFound       | 没有找到Celery ID      |
| 103    | NotFoundTask           | 没有找到任务           |
| 104    | TaskIsRunning          | 任务运行中             |
| 105    | TaskIsDone             | 任务已经完成           |
| 500    | Error                  | 系统异常               |

### 错误响应示例

```json
{
  "code": 102,
  "message": "CeleryIdNotFound",
  "data": {
    "celery_id": "不存在的Celery ID"
  }
}
```