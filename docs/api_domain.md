# 域名信息接口

提供对域名的查询、导出和删除等管理功能，支持按不同条件筛选域名信息。

## API概览

| 接口功能   | HTTP方法 | 请求路径              | 说明                     |
| ---------- | -------- | --------------------- | ------------------------ |
| 查询域名   | GET      | /api/domain/          | 获取域名列表或特定域名信息 |
| 导出域名   | GET      | /api/domain/export/   | 导出域名信息             |
| 删除域名   | POST     | /api/domain/delete/   | 删除特定域名记录         |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                 |
| ----------- | -------- | -------- | -------------------- |
| domain      | string   | 否       | 域名，支持模糊查询   |
| record      | string   | 否       | 解析值，支持模糊查询 |
| type        | string   | 否       | 解析类型，如A、CNAME、MX等 |
| ips         | string   | 否       | IP地址，支持模糊查询 |
| source      | string   | 否       | 数据来源，支持模糊查询 |
| task_id     | string   | 否       | 关联的任务ID         |
| page        | number   | 否       | 页码，默认为1        |
| size        | number   | 否       | 每页记录数，默认为10 |
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

### 1. 查询域名

**请求方法与地址**：
```
GET /api/domain/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤域名。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 120,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "domain": "example.com",
      "type": "A",
      "record": "203.0.113.1",
      "ips": ["203.0.113.1"],
      "source": "brute",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "domain": "mail.example.com",
      "type": "CNAME",
      "record": "mailserver.example.net",
      "ips": ["203.0.113.2"],
      "source": "dns_query",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多域名记录
  ],
  "query": {
    "domain": "example"
  }
}
```

**响应字段说明**：

| 字段名              | 类型     | 说明                  |
| ------------------- | -------- | --------------------- |
| total               | number   | 符合条件的记录总数    |
| page                | number   | 当前页码              |
| size                | number   | 每页记录数            |
| items               | array    | 域名记录数组          |
| items[].\_id        | string   | 域名记录唯一ID        |
| items[].domain      | string   | 域名名称              |
| items[].type        | string   | 解析类型              |
| items[].record      | string   | 解析值                |
| items[].ips         | array    | 关联IP地址列表        |
| items[].source      | string   | 数据来源              |
| items[].task_id     | string   | 关联任务ID            |
| items[].create_time | string   | 创建时间，ISO8601格式 |
| query               | object   | 查询参数              |

### 2. 导出域名

**请求方法与地址**：
```
GET /api/domain/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的域名。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含域名信息，每行一个域名。文件命名格式为：`domain_{记录数}_{时间戳}.txt`。

### 3. 删除域名

**请求方法与地址**：
```
POST /api/domain/delete/
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
| _id    | string[]  | 是       | 要删除的域名记录ID列表 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明                 |
| --------- | --------- | -------------------- |
| data._id  | string[]  | 成功删除的域名记录ID列表 |

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
| data._id    | string | 相关域名记录ID（可选）   |

### 错误示例
参数无效：
```json
{
  "code": 400,
  "msg": "InvalidParameter",
  "data": {
    "error": "域名ID格式错误"
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