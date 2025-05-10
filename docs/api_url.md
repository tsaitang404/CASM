# URL信息接口

提供对URL的查询和导出功能，支持按多种条件筛选URL信息。

## API概览

| 接口功能   | HTTP方法 | 请求路径          | 说明                     |
| ---------- | -------- | ----------------- | ------------------------ |
| 查询URL    | GET      | /api/url/         | 获取URL列表或特定URL信息 |
| 导出URL    | GET      | /api/url/export/  | 导出URL信息             |

## 通用字段说明

### 基础查询参数

| 字段名          | 类型     | 是否必填 | 说明                     |
| --------------- | -------- | -------- | ------------------------ |
| fld             | string   | 否       | IP地址，支持模糊查询     |
| site            | string   | 否       | 域名，支持模糊查询       |
| url             | string   | 否       | URL，支持模糊查询        |
| content_length  | number   | 否       | 响应内容长度             |
| status_code     | number   | 否       | HTTP状态码               |
| title           | string   | 否       | 页面标题，支持模糊查询   |
| source          | string   | 否       | 来源，支持模糊查询       |
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

### 1. 查询URL

**请求方法与地址**：
```
GET /api/url/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤URL。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 356,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "url": "http://example.com/login",
      "fld": "203.0.113.1",
      "site": "example.com",
      "content_length": 4526,
      "status_code": 200,
      "title": "Login - Example Site",
      "source": "spider",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "url": "http://example.com/about",
      "fld": "203.0.113.1",
      "site": "example.com",
      "content_length": 8952,
      "status_code": 200,
      "title": "About Us - Example Site",
      "source": "spider",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:31:00.000Z"
    }
    // ... 更多URL记录
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
| items                 | array    | URL记录数组           |
| items[].\_id          | string   | URL记录唯一ID         |
| items[].url           | string   | URL地址               |
| items[].fld           | string   | IP地址                |
| items[].site          | string   | 所属域名              |
| items[].content_length| number   | 响应内容长度          |
| items[].status_code   | number   | HTTP状态码            |
| items[].title         | string   | 页面标题              |
| items[].source        | string   | 来源                  |
| items[].task_id       | string   | 关联任务ID            |
| items[].create_time   | string   | 创建时间，ISO8601格式 |
| query                 | object   | 查询参数              |

### 2. 导出URL

**请求方法与地址**：
```
GET /api/url/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的URL。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含URL信息，每行一个URL。文件命名格式为：`url_{记录数}_{时间戳}.txt`。

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
    "error": "状态码必须为整数"
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