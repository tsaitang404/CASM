# 站点信息接口

提供对站点的查询、导出、标签管理和删除等功能，支持按多种条件筛选站点信息。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询站点     | GET      | /api/site/            | 获取站点列表或特定站点信息 |
| 导出站点     | GET      | /api/site/export/     | 导出站点信息             |
| 保存结果集   | GET      | /api/site/save_result_set/ | 保存站点查询结果为结果集 |
| 添加站点标签 | POST     | /api/site/add_tag/    | 为站点添加标签           |
| 删除站点标签 | POST     | /api/site/delete_tag/ | 删除站点的特定标签       |
| 删除站点     | POST     | /api/site/delete/     | 删除特定站点记录         |

## 通用字段说明

### 基础查询参数

| 字段名        | 类型     | 是否必填 | 说明                 |
| ------------- | -------- | -------- | -------------------- |
| site          | string   | 否       | 站点URL，支持模糊查询 |
| hostname      | string   | 否       | 主机名，支持模糊查询 |
| ip            | string   | 否       | IP地址，支持模糊查询 |
| title         | string   | 否       | 网页标题，支持模糊查询 |
| http_server   | string   | 否       | Web服务器类型，支持模糊查询 |
| headers       | string   | 否       | HTTP响应头，支持模糊查询 |
| finger.name   | string   | 否       | 指纹名称，支持模糊查询 |
| status        | number   | 否       | HTTP状态码           |
| favicon.hash  | number   | 否       | favicon哈希值        |
| task_id       | string   | 否       | 关联的任务ID         |
| tag           | string   | 否       | 标签，支持模糊查询   |
| page          | number   | 否       | 页码，默认为1        |
| size          | number   | 否       | 每页记录数，默认为10 |
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

### 1. 查询站点

**请求方法与地址**：
```
GET /api/site/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤站点。

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
      "site": "http://example.com",
      "hostname": "example.com",
      "ip": "203.0.113.1",
      "title": "Example Website",
      "http_server": "nginx/1.18.0",
      "status": 200,
      "finger": [
        {
          "name": "Nginx",
          "confidence": 90
        }
      ],
      "favicon": {
        "hash": 123456789
      },
      "tag": ["重要", "生产环境"],
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "site": "https://blog.example.com",
      "hostname": "blog.example.com",
      "ip": "203.0.113.2",
      "title": "Example Blog",
      "http_server": "Apache/2.4.46",
      "status": 200,
      "finger": [
        {
          "name": "WordPress",
          "confidence": 95
        }
      ],
      "favicon": {
        "hash": 987654321
      },
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:35:00.000Z"
    }
    // ... 更多站点记录
  ],
  "query": {
    "status": 200
  }
}
```

**响应字段说明**：

| 字段名                | 类型     | 说明                  |
| --------------------- | -------- | --------------------- |
| total                 | number   | 符合条件的记录总数    |
| page                  | number   | 当前页码              |
| size                  | number   | 每页记录数            |
| items                 | array    | 站点记录数组          |
| items[].\_id          | string   | 站点记录唯一ID        |
| items[].site          | string   | 站点URL               |
| items[].hostname      | string   | 主机名                |
| items[].ip            | string   | IP地址                |
| items[].title         | string   | 网页标题              |
| items[].http_server   | string   | Web服务器类型         |
| items[].status        | number   | HTTP状态码            |
| items[].finger        | array    | 指纹信息数组          |
| items[].finger[].name | string   | 指纹名称              |
| items[].favicon       | object   | favicon信息           |
| items[].tag           | array    | 标签列表              |
| items[].task_id       | string   | 关联任务ID            |
| items[].create_time   | string   | 创建时间，ISO8601格式 |
| query                 | object   | 查询参数              |

### 2. 导出站点

**请求方法与地址**：
```
GET /api/site/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的站点。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含站点URL信息，每行一个站点URL。文件命名格式为：`site_{记录数}_{时间戳}.txt`。

### 3. 保存结果集

**请求方法与地址**：
```
GET /api/site/save_result_set/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要保存的站点结果集。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "result_set_id": "60f8c2b2e13e4b1e8c8b4570",
    "result_total": 15,
    "type": "site"
  }
}
```

**响应字段说明**：

| 字段名              | 类型     | 说明                   |
| ------------------- | -------- | ---------------------- |
| data.result_set_id  | string   | 结果集唯一ID           |
| data.result_total   | number   | 结果集中站点的总数     |
| data.type           | string   | 结果集类型，固定为"site" |

### 4. 添加站点标签

**请求方法与地址**：
```
POST /api/site/add_tag/
```

**请求体**：
```json
{
  "_id": "60f8c2b2e13e4b1e8c8b4567",
  "tag": "重要"
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明             |
| ------ | --------- | -------- | ---------------- |
| _id    | string    | 是       | 站点记录ID       |
| tag    | string    | 是       | 要添加的标签名称 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "tag": "重要"
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明             |
| --------- | --------- | ---------------- |
| data.tag  | string    | 成功添加的标签名 |

### 5. 删除站点标签

**请求方法与地址**：
```
POST /api/site/delete_tag/
```

**请求体**：
```json
{
  "_id": "60f8c2b2e13e4b1e8c8b4567",
  "tag": "重要"
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明             |
| ------ | --------- | -------- | ---------------- |
| _id    | string    | 是       | 站点记录ID       |
| tag    | string    | 是       | 要删除的标签名称 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "tag": "重要"
  }
}
```

**响应字段说明**：

| 字段名    | 类型      | 说明             |
| --------- | --------- | ---------------- |
| data.tag  | string    | 成功删除的标签名 |

### 6. 删除站点

**请求方法与地址**：
```
POST /api/site/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                |
| ------ | --------- | -------- | ------------------- |
| _id    | string[]  | 是       | 要删除的站点记录ID列表 |

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

| 字段名    | 类型      | 说明                |
| --------- | --------- | ------------------- |
| data._id  | string[]  | 成功删除的站点记录ID列表 |

## 错误响应

### 通用错误码

| 错误码 | 描述                | 说明                 |
| ------ | ------------------- | -------------------- |
| 500    | Error               | 系统异常             |
| 401    | NotLogin            | 用户未登录           |
| 400    | InvalidParameter    | 参数无效             |
| 1200   | SiteIdNotFound      | 站点ID不存在         |
| 1201   | SiteTagIsExist      | 站点标签已存在       |
| 1202   | SiteTagNotExist     | 站点标签不存在       |
| 1400   | QueryResultIsEmpty  | 查询结果为空         |

### 错误响应字段说明

| 字段名        | 类型   | 说明                     |
| ------------- | ------ | ------------------------ |
| code          | number | 错误码                   |
| message       | string | 错误类型描述             |
| data.error    | string | 详细错误信息（可选）     |
| data.site_id  | string | 相关站点ID（可选）       |
| data.tag      | string | 相关标签名（可选）       |

### 错误示例
站点ID不存在：
```json
{
  "code": 1200,
  "message": "SiteIdNotFound",
  "data": {
    "site_id": "不存在的站点ID"
  }
}
```

站点标签已存在：
```json
{
  "code": 1201,
  "message": "SiteTagIsExist",
  "data": {
    "tag": "已存在的标签"
  }
}
```

查询结果为空：
```json
{
  "code": 1400,
  "message": "QueryResultIsEmpty",
  "data": {}
}
```
