# 服务信息接口

提供对系统服务的查询功能，支持按不同条件筛选服务信息。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询服务     | GET      | /api/service/         | 获取服务列表或特定服务信息 |

## 通用字段说明

### 基础查询参数

| 字段名                | 类型     | 是否必填 | 说明                     |
| --------------------- | -------- | -------- | ------------------------ |
| service_name          | string   | 否       | 服务名称，支持模糊查询   |
| service_info.ip       | string   | 否       | IP地址，支持模糊查询     |
| service_info.port_id  | number   | 否       | 端口号                   |
| service_info.version  | string   | 否       | 系统服务版本，支持模糊查询 |
| service_info.product  | string   | 否       | 产品名称，支持模糊查询   |
| task_id               | string   | 否       | 关联的任务ID             |
| page                  | number   | 否       | 页码，默认为1            |
| size                  | number   | 否       | 每页记录数，默认为10     |
| order                 | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询服务

**请求方法与地址**：
```
GET /api/service/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤服务。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 45,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "service_name": "http",
      "service_info": [
        {
          "ip": "203.0.113.1",
          "port_id": 80,
          "product": "nginx",
          "version": "1.18.0"
        },
        {
          "ip": "203.0.113.2",
          "port_id": 80,
          "product": "nginx",
          "version": "1.18.0"
        }
      ],
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "service_name": "ssh",
      "service_info": [
        {
          "ip": "203.0.113.1",
          "port_id": 22,
          "product": "OpenSSH",
          "version": "8.2p1"
        }
      ],
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多服务记录
  ],
  "query": {
    "service_name": "http"
  }
}
```

**响应字段说明**：

| 字段名                        | 类型     | 说明                  |
| ----------------------------- | -------- | --------------------- |
| total                         | number   | 符合条件的记录总数    |
| page                          | number   | 当前页码              |
| size                          | number   | 每页记录数            |
| items                         | array    | 服务记录数组          |
| items[].\_id                  | string   | 服务记录唯一ID        |
| items[].service_name          | string   | 服务名称              |
| items[].service_info          | array    | 服务信息列表          |
| items[].service_info[].ip     | string   | IP地址                |
| items[].service_info[].port_id| number   | 端口号                |
| items[].service_info[].product| string   | 产品名称              |
| items[].service_info[].version| string   | 服务版本              |
| items[].task_id               | string   | 关联任务ID            |
| items[].create_time           | string   | 创建时间，ISO8601格式 |
| query                         | object   | 查询参数              |

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
| message     | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |

### 错误示例
参数无效：
```json
{
  "code": 400,
  "message": "InvalidParameter",
  "data": {
    "error": "端口号必须为整数"
  }
}
```

系统错误：
```json
{
  "code": 500,
  "message": "Error",
  "data": {
    "error": "数据库连接失败"
  }
}
```