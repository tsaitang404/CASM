# 文件泄漏信息接口

提供对文件泄漏信息的查询和删除功能，支持按不同条件筛选泄漏记录。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询泄漏信息 | GET      | /api/fileleak/        | 获取文件泄漏记录列表     |
| 删除泄漏信息 | POST     | /api/fileleak/delete/ | 删除特定文件泄漏记录     |

## 通用字段说明

### 基础查询参数

| 字段名          | 类型     | 是否必填 | 说明                     |
| --------------- | -------- | -------- | ------------------------ |
| url             | string   | 否       | 泄漏文件URL，支持模糊查询 |
| site            | string   | 否       | 所属站点，支持模糊查询   |
| content_length  | number   | 否       | 响应内容长度             |
| status_code     | number   | 否       | HTTP状态码               |
| title           | string   | 否       | 页面标题，支持模糊查询   |
| task_id         | string   | 否       | 关联的任务ID             |
| page            | number   | 否       | 页码，默认为1            |
| size            | number   | 否       | 每页记录数，默认为10     |
| order           | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询文件泄漏信息

**请求方法与地址**：
```
GET /api/fileleak/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤文件泄漏记录。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 28,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "url": "http://example.com/.git/config",
      "site": "example.com",
      "content_length": 4526,
      "status_code": 200,
      "title": "Index of /.git/config",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "url": "http://example.com/backup.zip",
      "site": "example.com",
      "content_length": 152384,
      "status_code": 200,
      "title": "backup.zip",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多泄漏记录
  ],
  "query": {
    "site": "example.com"
  }
}
```

**响应字段说明**：

| 字段名                | 类型     | 说明                  |
| --------------------- | -------- | --------------------- |
| total                 | number   | 符合条件的记录总数    |
| page                  | number   | 当前页码              |
| size                  | number   | 每页记录数            |
| items                 | array    | 泄漏记录数组          |
| items[].\_id          | string   | 泄漏记录唯一ID        |
| items[].url           | string   | 泄漏文件URL           |
| items[].site          | string   | 所属站点              |
| items[].content_length| number   | 响应内容长度          |
| items[].status_code   | number   | HTTP状态码            |
| items[].title         | string   | 页面标题              |
| items[].task_id       | string   | 关联任务ID            |
| items[].create_time   | string   | 创建时间，ISO8601格式 |
| query                 | object   | 查询参数              |

### 2. 删除文件泄漏信息

**请求方法与地址**：
```
POST /api/fileleak/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                     |
| ------ | --------- | -------- | ------------------------ |
| _id    | string[]  | 是       | 要删除的文件泄漏记录ID列表 |

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
| data._id  | string[]  | 成功删除的文件泄漏记录ID列表 |

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
    "error": "文件泄漏ID格式错误"
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