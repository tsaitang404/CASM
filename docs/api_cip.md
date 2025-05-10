# C段IP统计信息接口

提供对C段IP统计信息的查询和导出功能，支持按不同条件筛选C段信息。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询C段统计  | GET      | /api/cip/             | 获取C段IP统计信息列表    |
| 导出C段IP    | GET      | /api/cip/export/      | 导出C段IP信息            |

## 通用字段说明

### 基础查询参数

| 字段名        | 类型     | 是否必填 | 说明                     |
| ------------- | -------- | -------- | ------------------------ |
| cidr_ip       | string   | 否       | C段IP地址(如192.168.1.0/24)，支持模糊查询 |
| task_id       | string   | 否       | 关联的任务ID             |
| ip_count      | number   | 否       | IP个数                   |
| domain_count  | number   | 否       | 解析到该C段的域名个数    |
| page          | number   | 否       | 页码，默认为1            |
| size          | number   | 否       | 每页记录数，默认为10     |
| order         | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询C段统计信息

**请求方法与地址**：
```
GET /api/cip/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤C段统计信息。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 35,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "cidr_ip": "203.0.113.0/24",
      "ip_count": 56,
      "domain_count": 12,
      "ip_list": ["203.0.113.1", "203.0.113.2", "203.0.113.10"],
      "domain_list": ["example.com", "test.example.com"],
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "cidr_ip": "198.51.100.0/24",
      "ip_count": 23,
      "domain_count": 5,
      "ip_list": ["198.51.100.1", "198.51.100.5", "198.51.100.15"],
      "domain_list": ["example.org", "mail.example.org"],
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多C段记录
  ],
  "query": {
    "domain_count": {"$gt": 3}
  }
}
```

**响应字段说明**：

| 字段名                | 类型     | 说明                      |
| --------------------- | -------- | ------------------------- |
| total                 | number   | 符合条件的记录总数        |
| page                  | number   | 当前页码                  |
| size                  | number   | 每页记录数                |
| items                 | array    | C段IP记录数组             |
| items[].\_id          | string   | C段记录唯一ID             |
| items[].cidr_ip       | string   | C段IP CIDR表示法          |
| items[].ip_count      | number   | 该C段的IP数量             |
| items[].domain_count  | number   | 解析到该C段的域名数量     |
| items[].ip_list       | array    | IP地址列表（可能被截断）  |
| items[].domain_list   | array    | 关联域名列表（可能被截断）|
| items[].task_id       | string   | 关联任务ID                |
| items[].create_time   | string   | 创建时间，ISO8601格式     |
| query                 | object   | 查询参数                  |

### 2. 导出C段IP

**请求方法与地址**：
```
GET /api/cip/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的C段IP信息。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含C段IP信息，每行一条记录。文件命名格式为：`cip_{记录数}_{时间戳}.txt`。

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
    "error": "CIDR格式错误"
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