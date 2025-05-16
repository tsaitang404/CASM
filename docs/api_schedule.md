# 计划任务接口

提供对计划任务的创建、查询、停止、删除和恢复等管理功能，支持定时任务和周期任务两种类型。

## API概览

| 接口功能     | HTTP方法 | 请求路径                      | 说明                       |
| ------------ | -------- | ----------------------------- | -------------------------- |
| 查询计划任务 | GET      | /api/task_schedule/           | 获取计划任务列表或特定任务信息 |
| 添加计划任务 | POST     | /api/task_schedule/           | 创建新的计划任务           |
| 删除计划任务 | POST     | /api/task_schedule/delete/    | 删除计划任务               |
| 停止计划任务 | POST     | /api/task_schedule/stop/      | 停止计划任务               |
| 恢复计划任务 | POST     | /api/task_schedule/recover/   | 恢复已停止的计划任务       |

## 通用字段说明

### 基础查询参数

| 字段名          | 类型     | 是否必填 | 说明                                 |
| --------------- | -------- | -------- | ------------------------------------ |
| name            | string   | 否       | 计划任务名称，支持模糊查询           |
| target          | string   | 否       | 任务目标，支持模糊查询               |
| policy_name     | string   | 否       | 策略名称                             |
| schedule_type   | string   | 否       | 计划类型，如"future_scan"、"recurrent_scan" |
| schedule_status | string   | 否       | 状态，如"scheduled"、"stop"          |
| page            | number   | 否       | 页码，默认为1                        |
| size            | number   | 否       | 每页记录数，默认为10                 |

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

### 1. 查询计划任务

**请求方法与地址**：
```
GET /api/task_schedule/
```

**查询参数**：

通用字段说明中的基础查询参数。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 15,
    "page": 1,
    "size": 10,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "每周资产扫描",
        "target": "example.com",
        "task_tag": "task",
        "schedule_type": "recurrent_scan",
        "policy_id": "60f8c2b2e13e4b1e8c8b6789",
        "policy_name": "标准资产发现策略",
        "cron": "0 0 0 * * 1",
        "status": "scheduled",
        "run_number": 3,
        "last_run_time": 1651334400,
        "last_run_date": "2022-05-01T00:00:00.000Z",
        "next_run_date": "2022-05-08T00:00:00.000Z"
      }
    ]
  }
}
```

**响应字段说明**：

| 字段名                      | 类型     | 说明                        |
| --------------------------- | -------- | --------------------------- |
| data.total                  | number   | 符合条件的记录总数          |
| data.page                   | number   | 当前页码                    |
| data.size                   | number   | 每页记录数                  |
| data.items                  | array    | 计划任务记录数组            |
| data.items[].\_id           | string   | 计划任务唯一ID              |
| data.items[].name           | string   | 任务名称                    |
| data.items[].target         | string   | 任务目标                    |
| data.items[].task_tag       | string   | 任务标签                    |
| data.items[].schedule_type  | string   | 计划类型                    |
| data.items[].policy_id      | string   | 策略ID                      |
| data.items[].policy_name    | string   | 策略名称                    |
| data.items[].cron           | string   | Cron表达式(周期任务)        |
| data.items[].start_date     | string   | 开始日期(定时任务)          |
| data.items[].status         | string   | 任务状态                    |
| data.items[].run_number     | number   | 已执行次数                  |
| data.items[].last_run_time  | number   | 上次执行时间戳              |
| data.items[].last_run_date  | string   | 上次执行日期                |
| data.items[].next_run_date  | string   | 下次执行日期                |

### 2. 添加计划任务

**请求方法与地址**：
```
POST /api/task_schedule/
```

**请求体**：
```json
{
  "name": "每周资产扫描",
  "target": "example.com",
  "schedule_type": "recurrent_scan",
  "policy_id": "60f8c2b2e13e4b1e8c8b6789",
  "cron": "0 0 0 * * 1",
  "task_tag": "task"
}
```

**参数说明**：

| 参数名        | 类型     | 是否必填 | 说明                                     |
| ------------- | -------- | -------- | ---------------------------------------- |
| name          | string   | 是       | 计划任务名称                             |
| target        | string   | 是       | 任务目标，如域名、IP或URL                |
| schedule_type | string   | 是       | 计划类型，可选值："future_scan"(定时任务)、"recurrent_scan"(周期任务) |
| policy_id     | string   | 是       | 策略ID                                   |
| cron          | string   | 条件性   | Cron表达式，周期任务(recurrent_scan)必填 |
| start_date    | string   | 条件性   | 开始时间，定时任务(future_scan)必填      |
| task_tag      | string   | 是       | 任务标签，可选值："task"(资产发现任务)、"risk_cruising"(风险巡航任务) |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "每周资产扫描",
    "target": "example.com",
    "task_tag": "task",
    "schedule_type": "recurrent_scan",
    "policy_id": "60f8c2b2e13e4b1e8c8b6789",
    "policy_name": "标准资产发现策略",
    "cron": "0 0 0 * * 1",
    "start_date": "",
    "start_time": 0,
    "status": "scheduled",
    "run_number": 0,
    "last_run_time": 0,
    "last_run_date": "-",
    "next_run_date": "2022-05-08T00:00:00.000Z"
  }
}
```

**响应字段说明**：

| 字段名        | 类型     | 说明                        |
| ------------- | -------- | --------------------------- |
| data.\_id     | string   | 新创建的计划任务ID          |
| data.name     | string   | 任务名称                    |
| data.target   | string   | 任务目标                    |
| data.status   | string   | 任务状态                    |
| data.cron     | string   | Cron表达式(周期任务)        |
| data.next_run_date | string | 下次执行日期              |

### 3. 删除计划任务

**请求方法与地址**：
```
POST /api/task_schedule/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                 |
| ------ | --------- | -------- | -------------------- |
| _id    | string[]  | 是       | 要删除的计划任务ID列表 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明                     |
| --------- | --------- | ------------------------ |
| data._id  | string[]  | 被删除的计划任务ID列表   |

### 4. 停止计划任务

**请求方法与地址**：
```
POST /api/task_schedule/stop/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                 |
| ------ | --------- | -------- | -------------------- |
| _id    | string[]  | 是       | 要停止的计划任务ID列表 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明                     |
| --------- | --------- | ------------------------ |
| data._id  | string[]  | 已停止的计划任务ID列表   |

### 5. 恢复计划任务

**请求方法与地址**：
```
POST /api/task_schedule/recover/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                 |
| ------ | --------- | -------- | -------------------- |
| _id    | string[]  | 是       | 要恢复的计划任务ID列表 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明                     |
| --------- | --------- | ------------------------ |
| data._id  | string[]  | 已恢复的计划任务ID列表   |

## 错误响应

### 通用错误码

| 错误码 | 描述                   | 说明                   |
| ------ | ---------------------- | ---------------------- |
| 1100   | PolicyIDNotFound       | 策略不存在             |
| 1101   | TaskTargetIsEmpty      | 任务目标为空           |
| 1502   | CronError              | Cron表达式错误         |
| 1601   | TaskScheduleTypeInvalid| 计划任务类型错误       |
### 时间字段校验逻辑

时间字段需要满足以下校验规则：

1. **格式要求**：
  - 必须为有效的日期时间格式，支持 ISO8601 格式（例如：`2023-05-01T08:30:00.000Z`）。
  - 不支持非标准格式的日期时间字符串。

2. **范围校验**：
  - 时间字段不能为过去的时间（即必须为当前时间或未来时间）。
  - 如果时间字段为计划任务的开始时间，必须晚于当前系统时间。

3. **错误响应**：
  - 如果时间字段无效，接口将返回错误码 `1602`，并附带错误描述 `"DateInvalid"`。

示例错误响应：
| 1602   | DateInvalid            | 时间错误               |
| 1603   | TaskScheduleNotFound   | 计划任务未找到         |
| 1604   | FutureDateInvalid      | 定时任务开始时间已过期  |
| 500    | Error                  | 系统异常               |

### 错误响应字段说明

| 字段名       | 类型    | 说明                     |
| ------------ | ------- | ------------------------ |
| code         | number  | 错误码                   |
| message      | string  | 错误类型描述             |
| data.error   | string  | 详细错误信息（可选）     |
| data._id     | string[]| 相关计划任务ID（可选）   |
| data.target  | string  | 相关任务目标（可选）     |

### 错误示例
计划任务未找到：
```json
{
  "code": 1603,
  "message": "TaskScheduleNotFound",
  "data": {
    "_id": ["不存在的计划任务ID"]
  }
}
```

Cron表达式错误：
```json
{
  "code": 1502,
  "message": "CronError",
  "data": {
    "cron": "无效的Cron表达式"
  }
}
```

计划任务类型错误：
```json
{
  "code": 1601,
  "message": "TaskScheduleTypeInvalid",
  "data": {
    "schedule_type": "无效的计划类型"
  }
}
```