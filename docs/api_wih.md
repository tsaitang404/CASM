# WEB Info Hunter接口

提供对WEB Info Hunter信息的查询、导出和删除功能，支持按不同条件筛选WIH记录。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询WIH信息  | GET      | /api/wih/             | 获取WEB Info Hunter信息列表 |
| 导出WIH信息  | GET      | /api/wih/export/      | 导出WEB Info Hunter信息  |
| 删除WIH信息  | POST     | /api/wih/delete/      | 删除特定WEB Info Hunter记录 |

## 通用字段说明

### 基础查询参数

| 字段名           | 类型     | 是否必填 | 说明                     |
| ---------------- | -------- | -------- | ------------------------ |
| record_type      | string   | 否       | 记录类型，支持模糊查询   |
| record_type__neq | string   | 否       | 记录类型不等于（全匹配） |
| record_type__not | string   | 否       | 记录类型不包含           |
| content          | string   | 否       | 内容，支持模糊查询       |
| source           | string   | 否       | 来源JS URL，支持模糊查询 |
| site             | string   | 否       | 站点URL，支持模糊查询    |
| task_id          | string   | 否       | 关联的任务ID             |
| page             | number   | 否       | 页码，默认为1            |
| size             | number   | 否       | 每页记录数，默认为10     |
| order            | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询WIH信息

**请求方法与地址**：
```
GET /api/wih/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤WIH信息。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 52,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "record_type": "email",
      "content": "contact@example.com",
      "source": "https://example.com/main.js",
      "site": "example.com",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "record_type": "api_key",
      "content": "sk_live_abcdefghijklmnopqrstuvwxyz0123456789",
      "source": "https://example.com/payment.js",
      "site": "example.com",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多WIH记录
  ],
  "query": {
    "record_type": "email"
  }
}
```

**响应字段说明**：

| 字段名              | 类型     | 说明                  |
| ------------------- | -------- | --------------------- |
| total               | number   | 符合条件的记录总数    |
| page                | number   | 当前页码              |
| size                | number   | 每页记录数            |
| items               | array    | WIH记录数组           |
| items[].\_id        | string   | WIH记录唯一ID         |
| items[].record_type | string   | 记录类型              |
| items[].content     | string   | 内容                  |
| items[].source      | string   | 来源JS URL            |
| items[].site        | string   | 站点URL               |
| items[].task_id     | string   | 关联任务ID            |
| items[].create_time | string   | 创建时间，ISO8601格式 |
| query               | object   | 查询参数              |

### 2. 导出WIH信息

**请求方法与地址**：
```
GET /api/wih/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的WIH信息。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含WIH信息，每行一条记录。文件命名格式为：`wih_{记录数}_{时间戳}.txt`。

### 3. 删除WIH信息

**请求方法与地址**：
```
POST /api/wih/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明               |
| ------ | --------- | -------- | ------------------ |
| _id    | string[]  | 是       | 要删除的WIH记录ID列表 |

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

| 字段名    | 类型      | 说明               |
| --------- | --------- | ------------------ |
| data._id  | string[]  | 成功删除的WIH记录ID列表 |

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
    "error": "WIH记录ID格式错误"
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