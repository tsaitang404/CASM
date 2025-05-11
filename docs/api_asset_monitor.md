# 资产监控接口

资产监控接口提供对网站和服务的状态监控、标签管理、导出与删除等功能。

## API概览

| 接口功能           | HTTP方法 | 请求路径                       | 说明                       |
| ------------------ | -------- | ------------------------------ | -------------------------- |
| 查询站点资产       | GET      | /api/asset_site/               | 查询站点资产信息           |
| 添加标签           | POST     | /api/asset_site/add_tag/       | 为站点资产添加标签         |
| 删除标签           | POST     | /api/asset_site/delete_tag/    | 删除站点资产的标签         |
| 删除站点           | DELETE   | /api/asset_site/{id}           | 删除特定站点(REST风格)     |
| 批量删除站点       | POST     | /api/asset_site/delete/        | 批量删除站点资产           |
| 保存站点到结果集   | GET      | /api/asset_site/save_result_set/| 将站点保存为可导出的结果集 |
| 导出站点           | GET      | /api/asset_site/export/        | 导出站点资产数据           |

## 通用字段说明

| 字段名      | 类型     | 是否必填 | 说明                                       |
| ----------- | -------- | -------- | ------------------------------------------ |
| _id         | string   | 否       | 站点ID，在更新和删除操作中使用             |
| url         | string   | 是       | 站点URL地址                                |
| tag         | string   | 否       | 标签名称                                   |
| tags        | string[] | 否       | 标签列表                                   |
| status      | string   | 否       | 站点状态，如"normal"、"unreachable"等      |
| title       | string   | 否       | 站点标题                                   |
| fingerprint | string   | 否       | 站点指纹                                   |

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

### 1. 查询站点资产

**请求方法与地址**：
```
GET /api/asset_site/
```

**查询参数**：

| 参数名     | 类型   | 是否必填 | 说明                           |
| ---------- | ------ | -------- | ------------------------------ |
| url        | string | 否       | 按URL筛选站点                  |
| status     | string | 否       | 按状态筛选，如"normal"、"unreachable"|
| title      | string | 否       | 按标题关键词筛选               |
| tag        | string | 否       | 按标签筛选                     |
| page       | number | 否       | 页码，默认为1                  |
| size       | number | 否       | 每页记录数，默认为20           |
| scope_id   | string | 否       | 资产分组ID                     |
| sort_field | string | 否       | 排序字段                       |
| sort_order | string | 否       | 排序方式，"asc"或"desc"        |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "url": "https://example.com",
        "status": "normal",
        "title": "Example Website",
        "fingerprint": "Nginx/1.18.0",
        "tags": ["重要", "生产环境"],
        "last_check_time": "2023-05-11T08:30:00.000Z",
        "response_time": 105,
        "screenshot_path": "/screenshots/example.com.png"
      }
      // ...更多站点
    ]
  }
}
```

**响应字段说明**：

| 字段名                   | 类型     | 说明                       |
| ------------------------ | -------- | -------------------------- |
| data.total               | number   | 符合条件的记录总数         |
| data.page                | number   | 当前页码                   |
| data.size                | number   | 每页记录数                 |
| data.items               | array    | 站点记录数组               |
| data.items[].\_id        | string   | 站点唯一ID                 |
| data.items[].url         | string   | 站点URL地址                |
| data.items[].status      | string   | 站点状态                   |
| data.items[].title       | string   | 站点标题                   |
| data.items[].fingerprint | string   | 站点识别的指纹信息         |
| data.items[].tags        | string[] | 站点标签列表               |
| data.items[].last_check_time | string | 最后检查时间，ISO8601格式 |
| data.items[].response_time  | number | 响应时间，单位毫秒        |
| data.items[].screenshot_path | string | 站点截图路径             |

### 2. 添加标签

**请求方法与地址**：
```
POST /api/asset_site/add_tag/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "tag": "重要"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "updated": 2,
    "tag": "重要"
  }
}
```

**响应字段说明**：

| 字段名      | 类型   | 说明                  |
| ----------- | ------ | --------------------- |
| data.updated | number | 成功添加标签的站点数量 |
| data.tag    | string | 添加的标签名称        |

### 3. 删除标签

**请求方法与地址**：
```
POST /api/asset_site/delete_tag/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"],
  "tag": "重要"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "updated": 2,
    "tag": "重要"
  }
}
```

**响应字段说明**：

| 字段名      | 类型   | 说明                  |
| ----------- | ------ | --------------------- |
| data.updated | number | 成功删除标签的站点数量 |
| data.tag    | string | 删除的标签名称        |

### 4. 删除站点

**方法1: 删除单个站点（REST风格）**

**请求方法与地址**：
```
DELETE /api/asset_site/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 站点ID   |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "deleted": 1
  }
}
```

**响应字段说明**：

| 字段名       | 类型    | 说明           |
| ------------ | ------- | -------------- |
| data.deleted | number  | 成功删除的数量 |

**方法2: 批量删除站点**

**请求方法与地址**：
```
POST /api/asset_site/delete/
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
  "code": 200,
  "message": "success",
  "data": {
    "deleted": 2
  }
}
```

**响应字段说明**：

| 字段名       | 类型    | 说明               |
| ------------ | ------- | ------------------ |
| data.deleted | number  | 成功删除的站点数量 |

### 5. 保存站点到结果集

**请求方法与地址**：
```
GET /api/asset_site/save_result_set/
```

**查询参数**：

| 参数名     | 类型   | 是否必填 | 说明                       |
| ---------- | ------ | -------- | -------------------------- |
| url        | string | 否       | 按URL筛选站点              |
| status     | string | 否       | 按状态筛选                 |
| title      | string | 否       | 按标题关键词筛选           |
| tag        | string | 否       | 按标签筛选                 |
| scope_id   | string | 否       | 资产分组ID                 |
| name       | string | 是       | 结果集名称                 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "result_set_id": "60f8c2b2e13e4b1e8c8b4590",
    "name": "重要站点导出-20230511",
    "count": 25
  }
}
```

**响应字段说明**：

| 字段名           | 类型   | 说明                   |
| ---------------- | ------ | ---------------------- |
| data.result_set_id | string | 创建的结果集ID         |
| data.name        | string | 结果集名称             |
| data.count       | number | 结果集中包含的站点数量 |

### 6. 导出站点

**请求方法与地址**：
```
GET /api/asset_site/export/
```

**查询参数**：

| 参数名      | 类型   | 是否必填 | 说明                           |
| ----------- | ------ | -------- | ------------------------------ |
| result_set_id | string | 是     | 结果集ID                       |
| format      | string | 否       | 导出格式，支持"csv"、"json"等，默认"csv" |

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含站点信息，根据选择的格式不同，包含的字段可能有所不同。通常包括：

| 字段名       | 类型   | 说明                |
| ------------ | ------ | ------------------- |
| url          | string | 站点URL地址         |
| title        | string | 站点标题            |
| status       | string | 站点状态            |
| fingerprint  | string | 站点指纹识别信息    |
| tags         | string | 站点标签（CSV格式中以逗号分隔） |
| response_time | number | 响应时间（毫秒）    |
| last_check_time | string | 最后检查时间      |

## 错误响应

### 通用错误码

| 错误码 | 描述                 | 说明               |
| ------ | -------------------- | ------------------ |
| 1000   | InternalError        | 服务器内部错误     |
| 1003   | NotFound             | 找不到请求的资源   |
| 1004   | InvalidParameter     | 参数无效           |
| 1005   | OperationFailed      | 操作失败           |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| message     | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.id     | string | 相关资源ID（可选）       |

### 错误示例
资源不存在：
```json
{
  "code": 1003,
  "message": "NotFound",
  "data": {
    "id": "不存在的站点ID"
  }
}
```

参数无效：
```json
{
  "code": 1004,
  "message": "InvalidParameter",
  "data": {
    "error": "缺少必要参数name"
  }
}
```