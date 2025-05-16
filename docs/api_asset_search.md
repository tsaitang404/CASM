# 资产搜索接口

提供对资产域名、IP、站点、服务等的查询与导出功能。

## API概览

| 接口功能     | HTTP方法 | 请求路径                   | 说明                     |
| ------------ | -------- | -------------------------- | ------------------------ |
| 域名查询     | GET      | /api/asset_domain/         | 按条件查询域名资产       |
| 域名导出     | POST     | /api/batch_export/domain/  | 导出符合条件的域名资产   |
| IP查询       | GET      | /api/asset_ip/             | 按条件查询IP资产         |
| IP导出       | POST     | /api/batch_export/ip/      | 导出符合条件的IP资产     |
| 站点查询     | GET      | /api/asset_site/           | 按条件查询站点资产       |
| 站点导出     | POST     | /api/batch_export/site/    | 导出符合条件的站点资产   |
| URL导出      | POST     | /api/batch_export/url/     | 导出符合条件的URL列表    |
| 服务查询     | GET      | /api/service/              | 按条件查询服务资产       |

## 共通查询参数

以下参数适用于所有查询接口：

| 参数名      | 类型     | 是否必填 | 说明                              |
| ----------- | -------- | -------- | --------------------------------- |
| scope_id    | string   | 否       | 资产分组ID                        |
| page        | number   | 否       | 页码，默认为1                     |
| size        | number   | 否       | 每页记录数，默认为20              |
| sort_field  | string   | 否       | 排序字段                          |
| sort_order  | string   | 否       | 排序方式，"asc"或"desc"           |
| tag         | string   | 否       | 按标签筛选                        |
| task_id     | string[] | 否       | 任务ID列表，筛选特定任务发现的资产 |

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

| 字段名 | 类型   | 说明                                        |
| ------ | ------ | ------------------------------------------- |
| code   | number | 响应码，200表示成功，非200表示出错          |
| message| string | 响应消息，成功时为"success"，失败时为错误信息 |
| data   | object | 响应数据，不同API返回的数据结构不同         |

## 详细API说明

### 1. 域名查询

**请求方法与地址**：
```
GET /api/asset_domain/
```

**查询参数**：

| 参数名      | 类型     | 是否必填 | 说明                              |
| ----------- | -------- | -------- | --------------------------------- |
| domain      | string   | 否       | 域名关键字，支持模糊查询          |
| ip          | string   | 否       | 关联的IP地址                      |
| cname       | string   | 否       | CNAME记录                         |
| ns          | string   | 否       | NS记录                            |
| mx          | string   | 否       | MX记录                            |
| cdn         | boolean  | 否       | 是否使用CDN                       |
| registrar   | string   | 否       | 注册商                            |
| status      | string   | 否       | 状态，如"active"、"inactive"      |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 120,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "domain": "example.com",
        "ip": ["203.0.113.1", "203.0.113.2"],
        "cname": "www.example.net",
        "ns": ["ns1.example.net", "ns2.example.net"],
        "mx": ["mail.example.com"],
        "cdn": true,
        "registrar": "Example Registrar",
        "creation_date": "2010-01-01",
        "expiration_date": "2025-01-01",
        "tags": ["重要", "生产环境"],
        "update_time": "2023-05-10T08:30:00.000Z",
        "task_id": "60e8c2b2e13e4b1e8c8b1234"
      },
      // ...更多域名
    ]
  }
}
```

**响应字段说明**：

| 字段名                   | 类型     | 说明                      |
| ------------------------ | -------- | ------------------------- |
| data.total               | number   | 符合条件的记录总数        |
| data.page                | number   | 当前页码                  |
| data.size                | number   | 每页记录数                |
| data.items               | array    | 域名记录数组              |
| data.items[].\_id        | string   | 域名记录唯一ID            |
| data.items[].domain      | string   | 域名                      |
| data.items[].ip          | string[] | 关联的IP地址列表          |
| data.items[].cname       | string   | CNAME记录                 |
| data.items[].ns          | string[] | NS记录列表                |
| data.items[].mx          | string[] | MX记录列表                |
| data.items[].cdn         | boolean  | 是否使用CDN               |
| data.items[].registrar   | string   | 注册商名称                |
| data.items[].creation_date | string | 域名创建日期              |
| data.items[].expiration_date | string | 域名过期日期             |
| data.items[].tags        | string[] | 标签列表                  |
| data.items[].update_time | string   | 最后更新时间，ISO8601格式 |
| data.items[].task_id     | string   | 关联的任务ID              |

### 2. 域名导出

**请求方法与地址**：
```
POST /api/batch_export/domain/
```

**请求体**：
```json
{
  "domain": "example",
  "scope_id": "60f8c2b2e13e4b1e8c8b4570",
  "tag": "重要",
  "task_id": ["60e8c2b2e13e4b1e8c8b1234"],
  "format": "csv"
}
```

**参数说明**：

| 参数名      | 类型     | 是否必填 | 说明                               |
| ----------- | -------- | -------- | ---------------------------------- |
| domain      | string   | 否       | 域名关键字，支持模糊查询           |
| scope_id    | string   | 否       | 资产分组ID                         |
| tag         | string   | 否       | 按标签筛选                         |
| task_id     | string[] | 否       | 任务ID列表                         |
| format      | string   | 否       | 导出格式，支持"csv"、"json"，默认"csv" |

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含域名信息，根据选择的格式不同，包含的字段如下：

| 字段名         | 类型   | 说明                |
| -------------- | ------ | ------------------- |
| domain         | string | 域名                |
| ip             | string | 关联的IP地址(CSV格式中以逗号分隔) |
| cname          | string | CNAME记录           |
| ns             | string | NS记录(CSV格式中以逗号分隔) |
| mx             | string | MX记录(CSV格式中以逗号分隔) |
| cdn            | boolean| 是否使用CDN         |
| registrar      | string | 注册商名称          |
| creation_date  | string | 域名创建日期        |
| expiration_date| string | 域名过期日期        |
| tags           | string | 标签列表(CSV格式中以逗号分隔) |

### 3. IP查询

**请求方法与地址**：
```
GET /api/asset_ip/
```

**查询参数**：

| 参数名      | 类型     | 是否必填 | 说明                               |
| ----------- | -------- | -------- | ---------------------------------- |
| ip          | string   | 否       | IP地址，支持CIDR格式和模糊查询     |
| port        | number   | 否       | 开放端口                           |
| service     | string   | 否       | 服务名称                           |
| os          | string   | 否       | 操作系统                           |
| country     | string   | 否       | 国家/地区                          |
| province    | string   | 否       | 省份                               |
| city        | string   | 否       | 城市                               |
| isp         | string   | 否       | 运营商                             |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 85,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4568",
        "ip": "203.0.113.1",
        "ports": [80, 443, 22],
        "services": ["http", "https", "ssh"],
        "os": "Ubuntu 20.04",
        "country": "中国",
        "province": "广东",
        "city": "深圳",
        "isp": "电信",
        "tags": ["重要", "生产环境"],
        "update_time": "2023-05-10T09:30:00.000Z",
        "domains": ["example.com", "test.example.com"]
      },
      // ...更多IP
    ]
  }
}
```

**响应字段说明**：

| 字段名                   | 类型     | 说明                      |
| ------------------------ | -------- | ------------------------- |
| data.total               | number   | 符合条件的记录总数        |
| data.page                | number   | 当前页码                  |
| data.size                | number   | 每页记录数                |
| data.items               | array    | IP记录数组                |
| data.items[].\_id        | string   | IP记录唯一ID              |
| data.items[].ip          | string   | IP地址                    |
| data.items[].ports       | number[] | 开放端口列表              |
| data.items[].services    | string[] | 服务名称列表              |
| data.items[].os          | string   | 操作系统信息              |
| data.items[].country     | string   | 国家/地区                 |
| data.items[].province    | string   | 省份                      |
| data.items[].city        | string   | 城市                      |
| data.items[].isp         | string   | 运营商                    |
| data.items[].tags        | string[] | 标签列表                  |
| data.items[].update_time | string   | 最后更新时间，ISO8601格式 |
| data.items[].domains     | string[] | 关联域名列表              |

### 4. IP导出

**请求方法与地址**：
```
POST /api/batch_export/ip/
```

**请求体**：
```json
{
  "ip": "203.0.113",
  "port": 80,
  "service": "http",
  "scope_id": "60f8c2b2e13e4b1e8c8b4570",
  "tag": "重要",
  "task_id": ["60e8c2b2e13e4b1e8c8b1234"],
  "format": "csv"
}
```

**参数说明**：与IP查询接口相同，额外增加format参数

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含IP信息，根据选择的格式不同，包含的字段如下：

| 字段名      | 类型   | 说明                       |
| ----------- | ------ | -------------------------- |
| ip          | string | IP地址                     |
| ports       | string | 开放端口列表(CSV格式中以逗号分隔) |
| services    | string | 服务名称列表(CSV格式中以逗号分隔) |
| os          | string | 操作系统信息               |
| country     | string | 国家/地区                  |
| province    | string | 省份                       |
| city        | string | 城市                       |
| isp         | string | 运营商                     |
| tags        | string | 标签列表(CSV格式中以逗号分隔) |
| domains     | string | 关联域名列表(CSV格式中以逗号分隔) |

### 5. 站点查询

**请求方法与地址**：
```
GET /api/asset_site/
```

**查询参数**：

| 参数名      | 类型     | 是否必填 | 说明                                |
| ----------- | -------- | -------- | ----------------------------------- |
| url         | string   | 否       | URL地址或关键字                     |
| domain      | string   | 否       | 域名                                |
| ip          | string   | 否       | IP地址                              |
| title       | string   | 否       | 网页标题关键字                      |
| status      | string   | 否       | 站点状态，如"normal"、"unreachable" |
| fingerprint | string   | 否       | 指纹名称                            |
| favicon_hash| string   | 否       | 网站图标的哈希值                    |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 150,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4569",
        "url": "https://example.com",
        "domain": "example.com",
        "ip": "203.0.113.1",
        "title": "Example Website",
        "status": "normal",
        "fingerprint": "Nginx/1.18.0",
        "favicon_hash": "116323821",
        "response_code": 200,
        "response_time": 105,
        "content_length": 15678,
        "tags": ["重要", "生产环境"],
        "update_time": "2023-05-10T10:30:00.000Z",
        "screenshot_path": "/screenshots/example.com.png"
      },
      // ...更多站点
    ]
  }
}
```

**响应字段说明**：

| 字段名                    | 类型     | 说明                      |
| ------------------------- | -------- | ------------------------- |
| data.total                | number   | 符合条件的记录总数        |
| data.page                 | number   | 当前页码                  |
| data.size                 | number   | 每页记录数                |
| data.items                | array    | 站点记录数组              |
| data.items[].\_id         | string   | 站点记录唯一ID            |
| data.items[].url          | string   | 站点URL地址               |
| data.items[].domain       | string   | 站点所属域名              |
| data.items[].ip           | string   | 站点IP地址                |
| data.items[].title        | string   | 站点标题                  |
| data.items[].status       | string   | 站点状态                  |
| data.items[].fingerprint  | string   | 站点指纹信息              |
| data.items[].favicon_hash | string   | 网站图标的哈希值          |
| data.items[].response_code| number   | HTTP响应状态码            |
| data.items[].response_time| number   | 响应时间，单位毫秒        |
| data.items[].content_length| number  | 内容长度，单位字节        |
| data.items[].tags         | string[] | 标签列表                  |
| data.items[].update_time  | string   | 最后更新时间，ISO8601格式 |
| data.items[].screenshot_path| string | 站点截图路径              |

### 6. 站点导出

**请求方法与地址**：
```
POST /api/batch_export/site/
```

**请求体**：
```json
{
  "url": "example",
  "title": "Example",
  "fingerprint": "Nginx",
  "scope_id": "60f8c2b2e13e4b1e8c8b4570",
  "tag": "重要",
  "task_id": ["60e8c2b2e13e4b1e8c8b1234"],
  "format": "csv"
}
```

**参数说明**：与站点查询接口相同，额外增加format参数

**响应**：
文件下载（application/octet-stream或application/json）

**响应内容说明**：
导出的文件包含站点信息，根据选择的格式不同，包含的字段如下：

| 字段名        | 类型   | 说明                    |
| ------------- | ------ | ----------------------- |
| url           | string | 站点URL地址             |
| domain        | string | 站点所属域名            |
| ip            | string | 站点IP地址              |
| title         | string | 站点标题                |
| status        | string | 站点状态                |
| fingerprint   | string | 站点指纹信息            |
| favicon_hash  | string | 网站图标的哈希值        |
| response_code | number | HTTP响应状态码          |
| response_time | number | 响应时间，单位毫秒      |
| tags          | string | 标签列表(CSV格式中以逗号分隔) |

### 7. URL导出

**请求方法与地址**：
```
POST /api/batch_export/url/
```

**请求体**：
```json
{
  "domain": "example.com",
  "path": "/login",
  "scope_id": "60f8c2b2e13e4b1e8c8b4570",
  "tag": "重要",
  "task_id": ["60e8c2b2e13e4b1e8c8b1234"],
  "format": "txt"
}
```

**参数说明**：

| 参数名      | 类型     | 是否必填 | 说明                                |
| ----------- | -------- | -------- | ----------------------------------- |
| domain      | string   | 否       | 域名                                |
| path        | string   | 否       | URL路径关键字                       |
| scope_id    | string   | 否       | 资产分组ID                          |
| tag         | string   | 否       | 按标签筛选                          |
| task_id     | string[] | 否       | 任务ID列表                          |
| format      | string   | 否       | 导出格式，支持"txt"、"csv"、"json"  |

**响应**：
文件下载（text/plain、application/octet-stream或application/json）

**响应内容说明**：
导出格式不同，内容结构也不同：
- txt格式：每行一个完整URL
- csv格式：包含url、domain、path等字段的表格
- json格式：包含完整URL信息的JSON数组

### 8. 服务查询

**请求方法与地址**：
```
GET /api/service/
```

**查询参数**：

| 参数名       | 类型     | 是否必填 | 说明                     |
| ------------ | -------- | -------- | ------------------------ |
| service_name | string   | 否       | 服务名称                 |
| port         | number   | 否       | 端口号                   |
| ip           | string   | 否       | IP地址                   |
| protocol     | string   | 否       | 协议，如"tcp"、"udp"     |
| product      | string   | 否       | 产品名称                 |
| version      | string   | 否       | 版本号                   |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 75,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4570",
        "service_name": "http",
        "port": 80,
        "ip": "203.0.113.1",
        "protocol": "tcp",
        "product": "Nginx",
        "version": "1.18.0",
        "banner": "Nginx/1.18.0 (Ubuntu)",
        "tags": ["重要", "生产环境"],
        "update_time": "2023-05-10T11:30:00.000Z"
      },
      // ...更多服务
    ]
  }
}
```

**响应字段说明**：

| 字段名                    | 类型     | 说明                      |
| ------------------------- | -------- | ------------------------- |
| data.total                | number   | 符合条件的记录总数        |
| data.page                 | number   | 当前页码                  |
| data.size                 | number   | 每页记录数                |
| data.items                | array    | 服务记录数组              |
| data.items[].\_id         | string   | 服务记录唯一ID            |
| data.items[].service_name | string   | 服务名称                  |
| data.items[].port         | number   | 端口号                    |
| data.items[].ip           | string   | IP地址                    |
| data.items[].protocol     | string   | 协议类型                  |
| data.items[].product      | string   | 产品名称                  |
| data.items[].version      | string   | 版本号                    |
| data.items[].banner       | string   | 服务banner信息            |
| data.items[].tags         | string[] | 标签列表                  |
| data.items[].update_time  | string   | 最后更新时间，ISO8601格式 |

## 错误响应

### 通用错误码

| 错误码 | 描述                 | 说明                     |
| ------ | -------------------- | ------------------------ |
| 1000   | InternalError        | 服务器内部错误           |
| 1003   | NotFound             | 找不到请求的资源         |
| 1004   | InvalidParameter     | 参数无效                 |
| 1005   | ExportFailed         | 导出失败                 |

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
  "code": 1004,
  "message": "InvalidParameter",
  "data": {
    "error": "无效的IP地址格式"
  }
}
```

导出失败：
```json
{
  "code": 1005,
  "message": "ExportFailed",
  "data": {
    "error": "查询结果为空，无数据可导出"
  }
}
```