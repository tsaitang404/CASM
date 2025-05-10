# 指纹统计信息接口

提供对指纹统计信息的查询功能，支持按不同条件筛选统计结果。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询指纹统计 | GET      | /api/stat_finger/     | 获取指纹统计信息列表     |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                     |
| ----------- | -------- | -------- | ------------------------ |
| name        | string   | 否       | 指纹名称，支持模糊查询   |
| task_id     | string   | 否       | 关联的任务ID             |
| cnt         | number   | 否       | 数目                     |
| page        | number   | 否       | 页码，默认为1            |
| size        | number   | 否       | 每页记录数，默认为10     |
| order       | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询指纹统计

**请求方法与地址**：
```
GET /api/stat_finger/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤指纹统计信息。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 25,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "name": "nginx",
      "cnt": 156,
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "name": "apache",
      "cnt": 87,
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4569",
      "name": "iis",
      "cnt": 43,
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:34:00.000Z"
    }
    // ... 更多指纹统计记录
  ],
  "query": {
    "cnt": {"$gt": 10}
  }
}
```

**响应字段说明**：

| 字段名            | 类型     | 说明                  |
| ----------------- | -------- | --------------------- |
| total             | number   | 符合条件的记录总数    |
| page              | number   | 当前页码              |
| size              | number   | 每页记录数            |
| items             | array    | 指纹统计记录数组      |
| items[].\_id      | string   | 指纹统计记录唯一ID    |
| items[].name      | string   | 指纹名称              |
| items[].cnt       | number   | 数目                  |
| items[].task_id   | string   | 关联任务ID            |
| items[].create_time | string | 创建时间，ISO8601格式 |
| query             | object   | 查询参数              |

## 错误响应

### 通用错误码

| 错误码 | 描述                | 说明                 |
| ------ | ------------------- | -------------------- |
| 500    | Error               | 系统异常             |
| 401    | NotLogin            | 用户未登录           |
| 400    | InvalidParameter    | 参数无效             |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |

### 错误示例
参数无效：
```json
{
  "code": 400,
  "msg": "InvalidParameter",
  "data": {
    "error": "数目必须为整数"
  }
}
```

系统错误：
```json
{
  "code": 500,
  "msg": "Error",
  "data": {
    "error": "数据库连接失败"
  }
}
```