# GitHub相关接口

提供GitHub任务创建、执行、监控和结果管理功能，用于发现代码仓库中的敏感信息泄露。

## API概览

| 接口功能   | HTTP方法 | 请求路径                      | 说明                       |
| ---------- | -------- | ----------------------------- | -------------------------- |
| 任务列表   | GET      | /api/github_task/             | 获取所有GitHub搜索任务列表 |
| 创建任务   | POST     | /api/github_task/             | 创建新的GitHub搜索任务     |
| 停止任务   | POST     | /api/github_task/stop/        | 停止正在执行的搜索任务     |
| 删除任务   | DELETE   | /api/github_task/{id}         | 删除特定任务(REST风格)     |
| 批量删除任务 | POST   | /api/github_task/delete/      | 批量删除搜索任务           |
| 监控列表   | GET      | /api/github_scheduler/        | 获取所有GitHub监控任务列表 |
| 创建监控   | POST     | /api/github_scheduler/        | 创建新的GitHub监控任务     |
| 更新监控   | PUT      | /api/github_scheduler/{id}    | 更新特定监控任务(REST风格) |
| 批量更新监控 | POST   | /api/github_scheduler/update/ | 批量更新监控任务           |
| 删除监控   | DELETE   | /api/github_scheduler/{id}    | 删除特定监控任务(REST风格) |
| 批量删除监控 | POST   | /api/github_scheduler/delete/ | 批量删除监控任务           |
| 停止监控   | POST     | /api/github_scheduler/stop/   | 停止特定监控任务           |
| 恢复监控   | POST     | /api/github_scheduler/recover/| 恢复已停止的监控任务       |
| 查询任务结果 | GET    | /api/github_result/           | 查询GitHub搜索任务的结果   |
| 查询监控结果 | GET    | /api/github_monitor_result/   | 查询GitHub监控的结果       |

## GitHub搜索任务管理

### 1. 获取任务列表

**请求方法与地址**：
```
GET /api/github_task/
```

**查询参数**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| name        | string | 否       | 按任务名称筛选(模糊匹配)       |
| keyword     | string | 否       | 按搜索关键字筛选               |
| status      | string | 否       | 按任务状态筛选，如"running"、"finished"、"stopped" |
| page        | number | 否       | 页码，默认为1                  |
| size        | number | 否       | 每页记录数，默认为20           |
| sort_field  | string | 否       | 排序字段，如"create_time"      |
| sort_order  | string | 否       | 排序方式，"asc"或"desc"        |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 15,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "密钥泄露扫描",
        "keyword": "password OR secret OR token",
        "scope": "org:example-org",
        "status": "finished",
        "progress": 100,
        "result_count": 24,
        "create_time": "2023-05-10T08:30:00.000Z",
        "finish_time": "2023-05-10T09:15:00.000Z",
        "creator": "admin"
      },
      // ...更多任务
    ]
  }
}
```

### 2. 创建任务

**请求方法与地址**：
```
POST /api/github_task/
```

**请求体**：
```json
{
  "name": "密钥泄露扫描",
  "keyword": "password OR secret OR token",
  "scope": "org:example-org",
  "description": "扫描组织仓库中的密钥泄露",
  "token_id": "60f8c2b2e13e4b1e8c8b5000"
}
```

**参数说明**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| name        | string | 是       | 任务名称                       |
| keyword     | string | 是       | GitHub搜索关键字               |
| scope       | string | 否       | 搜索范围，如"org:example-org"  |
| description | string | 否       | 任务描述                       |
| token_id    | string | 否       | GitHub Token ID，为空则使用系统默认Token |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "密钥泄露扫描",
    "keyword": "password OR secret OR token",
    "scope": "org:example-org",
    "status": "running",
    "progress": 0,
    "create_time": "2023-05-11T08:30:00.000Z",
    "creator": "admin"
  }
}
```

### 3. 停止任务

**请求方法与地址**：
```
POST /api/github_task/stop/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型     | 是否必填 | 说明             |
| ------ | -------- | -------- | ---------------- |
| _id    | string[] | 是       | 要停止的任务ID列表 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "stopped": 2
  }
}
```

### 4. 删除任务

**方法1: 删除单个任务（REST风格）**

**请求方法与地址**：
```
DELETE /api/github_task/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 任务ID   |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 1
  }
}
```

**方法2: 批量删除任务**

**请求方法与地址**：
```
POST /api/github_task/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 2
  }
}
```

## GitHub监控任务管理

### 1. 获取监控列表

**请求方法与地址**：
```
GET /api/github_scheduler/
```

**查询参数**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| name        | string | 否       | 按监控名称筛选(模糊匹配)       |
| keyword     | string | 否       | 按搜索关键字筛选               |
| status      | string | 否       | 按监控状态筛选，如"running"、"stopped" |
| page        | number | 否       | 页码，默认为1                  |
| size        | number | 否       | 每页记录数，默认为20           |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 8,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4569",
        "name": "密钥泄露监控",
        "keyword": "password OR secret OR token",
        "scope": "org:example-org",
        "status": "running",
        "cron": "0 0 */12 * * *",
        "next_time": "2023-05-11T12:00:00.000Z",
        "last_time": "2023-05-11T00:00:00.000Z",
        "description": "每12小时执行一次",
        "create_time": "2023-05-01T08:30:00.000Z",
        "creator": "admin"
      },
      // ...更多监控
    ]
  }
}
```

### 2. 创建监控

**请求方法与地址**：
```
POST /api/github_scheduler/
```

**请求体**：
```json
{
  "name": "密钥泄露监控",
  "keyword": "password OR secret OR token",
  "scope": "org:example-org",
  "cron": "0 0 */12 * * *",
  "description": "每12小时执行一次",
  "token_id": "60f8c2b2e13e4b1e8c8b5000"
}
```

**参数说明**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| name        | string | 是       | 监控名称                       |
| keyword     | string | 是       | GitHub搜索关键字               |
| scope       | string | 否       | 搜索范围，如"org:example-org"  |
| cron        | string | 是       | Cron表达式，定义监控执行频率   |
| description | string | 否       | 监控描述                       |
| token_id    | string | 否       | GitHub Token ID，为空则使用系统默认Token |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4569",
    "name": "密钥泄露监控",
    "keyword": "password OR secret OR token",
    "scope": "org:example-org",
    "status": "running",
    "cron": "0 0 */12 * * *",
    "next_time": "2023-05-11T12:00:00.000Z",
    "create_time": "2023-05-11T08:30:00.000Z",
    "creator": "admin"
  }
}
```

### 3. 更新监控

**方法1: 更新单个监控（REST风格）**

**请求方法与地址**：
```
PUT /api/github_scheduler/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 监控ID   |

**请求体**：
```json
{
  "name": "更新后的监控名称",
  "keyword": "updated keyword OR secret OR token",
  "scope": "org:example-org",
  "cron": "0 0 */6 * * *",
  "description": "每6小时执行一次"
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4569",
    "name": "更新后的监控名称",
    "keyword": "updated keyword OR secret OR token",
    "scope": "org:example-org",
    "status": "running",
    "cron": "0 0 */6 * * *",
    "next_time": "2023-05-11T12:00:00.000Z",
    "description": "每6小时执行一次",
    "update_time": "2023-05-11T09:30:00.000Z"
  }
}
```

**方法2: 批量更新监控**

**请求方法与地址**：
```
POST /api/github_scheduler/update/
```

**请求体**：
```json
{
  "_id": "60f8c2b2e13e4b1e8c8b4569",
  "name": "更新后的监控名称",
  "keyword": "updated keyword OR secret OR token",
  "cron": "0 0 */6 * * *"
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "updated": 1
  }
}
```

### 4. 删除监控

**方法1: 删除单个监控（REST风格）**

**请求方法与地址**：
```
DELETE /api/github_scheduler/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 监控ID   |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 1
  }
}
```

**方法2: 批量删除监控**

**请求方法与地址**：
```
POST /api/github_scheduler/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4569", "60f8c2b2e13e4b1e8c8b4570"]
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 2
  }
}
```

### 5. 停止监控

**请求方法与地址**：
```
POST /api/github_scheduler/stop/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4569", "60f8c2b2e13e4b1e8c8b4570"]
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "stopped": 2
  }
}
```

### 6. 恢复监控

**请求方法与地址**：
```
POST /api/github_scheduler/recover/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4569", "60f8c2b2e13e4b1e8c8b4570"]
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "recovered": 2
  }
}
```

## GitHub结果查询

### 1. 查询任务结果

**请求方法与地址**：
```
GET /api/github_result/
```

**查询参数**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| task_id     | string | 否       | 任务ID                         |
| repo        | string | 否       | 按仓库名筛选                   |
| content     | string | 否       | 按内容关键字筛选               |
| page        | number | 否       | 页码，默认为1                  |
| size        | number | 否       | 每页记录数，默认为20           |
| sort_field  | string | 否       | 排序字段                       |
| sort_order  | string | 否       | 排序方式，"asc"或"desc"        |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 24,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4571",
        "task_id": "60f8c2b2e13e4b1e8c8b4567",
        "repo": "example-org/project",
        "path": "config/settings.yml",
        "url": "https://github.com/example-org/project/blob/main/config/settings.yml",
        "content": "api_token: abcdef1234567890",
        "matches": ["api_token"],
        "create_time": "2023-05-10T09:10:00.000Z",
        "status": "unread"
      },
      // ...更多结果
    ]
  }
}
```

### 2. 查询监控结果

**请求方法与地址**：
```
GET /api/github_monitor_result/
```

**查询参数**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| monitor_id  | string | 否       | 监控任务ID                     |
| repo        | string | 否       | 按仓库名筛选                   |
| content     | string | 否       | 按内容关键字筛选               |
| status      | string | 否       | 按状态筛选，如"read"、"unread" |
| page        | number | 否       | 页码，默认为1                  |
| size        | number | 否       | 每页记录数，默认为20           |
| sort_field  | string | 否       | 排序字段                       |
| sort_order  | string | 否       | 排序方式，"asc"或"desc"        |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 18,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4572",
        "monitor_id": "60f8c2b2e13e4b1e8c8b4569",
        "repo": "example-org/project",
        "path": "config/settings.yml",
        "url": "https://github.com/example-org/project/blob/main/config/settings.yml",
        "content": "api_token: abcdef1234567890",
        "matches": ["api_token"],
        "create_time": "2023-05-11T00:10:00.000Z",
        "status": "unread",
        "batch": "20230511000000"
      },
      // ...更多结果
    ]
  }
}
```

## 错误响应

### 通用错误码

| 错误码 | 描述                 | 说明                     |
| ------ | -------------------- | ------------------------ |
| 1000   | InternalError        | 服务器内部错误           |
| 1003   | NotFound             | 找不到请求的资源         |
| 1004   | InvalidParameter     | 参数无效                 |
| 1006   | DuplicateName        | 名称重复                 |
| 1007   | TokenInvalid         | GitHub Token无效或过期   |
| 1008   | RateLimitExceeded    | GitHub API请求超限       |

### 错误示例
资源不存在：
```json
{
  "code": 1003,
  "msg": "NotFound",
  "data": {
    "id": "不存在的任务ID"
  }
}
```

名称重复：
```json
{
  "code": 1006,
  "msg": "DuplicateName",
  "data": {
    "name": "已存在的任务名称"
  }
}
```

Token无效：
```json
{
  "code": 1007,
  "msg": "TokenInvalid",
  "data": {
    "error": "GitHub API认证失败"
  }
}
```