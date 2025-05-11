# IP信息接口

提供对IP的查询、导出和删除等功能，支持按多种条件筛选IP信息及导出相关数据。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询IP       | GET      | /api/ip/              | 获取IP列表或特定IP信息   |
| 导出IP端口   | GET      | /api/ip/export/       | 导出IP端口信息           |
| 导出域名     | GET      | /api/ip/export_domain/ | 从IP中导出关联的域名     |
| 导出IP       | GET      | /api/ip/export_ip/    | 从IP中导出IP地址         |
| 删除IP       | POST     | /api/ip/delete/       | 删除特定IP记录           |

## 通用字段说明

### 基础查询参数

| 字段名                | 类型     | 是否必填 | 说明                     |
| --------------------- | -------- | -------- | ------------------------ |
| ip                    | string   | 否       | IP地址，支持模糊查询     |
| domain                | string   | 否       | 关联域名，支持模糊查询   |
| port_info.port_id     | number   | 否       | 端口号                   |
| port_info.service_name | string  | 否       | 系统服务名称，支持模糊查询 |
| port_info.version     | string   | 否       | 系统服务版本，支持模糊查询 |
| port_info.product     | string   | 否       | 产品名称，支持模糊查询   |
| os_info.name          | string   | 否       | 操作系统名称，支持模糊查询 |
| task_id               | string   | 否       | 关联的任务ID             |
| ip_type               | string   | 否       | IP类型，如PUBLIC（公网）、PRIVATE（内网） |
| cdn_name              | string   | 否       | CDN厂商名称，支持模糊查询 |
| geo_asn.number        | number   | 否       | AS号码                   |
| geo_asn.organization  | string   | 否       | AS组织名称，支持模糊查询 |
| geo_city.region_name  | string   | 否       | 地理区域名称，支持模糊查询 |
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

### 1. 查询IP

**请求方法与地址**：
```
GET /api/ip/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤IP。

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
      "ip": "203.0.113.1",
      "domain": ["example.com", "test.example.com"],
      "port_info": [
        {
          "port_id": 80,
          "service_name": "http",
          "product": "nginx",
          "version": "1.18.0"
        },
        {
          "port_id": 443,
          "service_name": "https",
          "product": "nginx",
          "version": "1.18.0"
        }
      ],
      "os_info": {
        "name": "Linux",
        "accuracy": 95
      },
      "ip_type": "PUBLIC",
      "cdn_name": "",
      "geo_asn": {
        "number": 12345,
        "organization": "Example ISP"
      },
      "geo_city": {
        "region_name": "Beijing",
        "country": "CN"
      },
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    }
    // ... 更多IP记录
  ],
  "query": {
    "ip_type": "PUBLIC"
  }
}
```

**响应字段说明**：

| 字段名                        | 类型     | 说明                  |
| ----------------------------- | -------- | --------------------- |
| total                         | number   | 符合条件的记录总数    |
| page                          | number   | 当前页码              |
| size                          | number   | 每页记录数            |
| items                         | array    | IP记录数组            |
| items[].\_id                  | string   | IP记录唯一ID          |
| items[].ip                    | string   | IP地址                |
| items[].domain                | array    | 关联域名列表          |
| items[].port_info             | array    | 端口信息列表          |
| items[].port_info[].port_id   | number   | 端口号                |
| items[].port_info[].service_name | string | 系统服务名称         |
| items[].port_info[].product   | string   | 产品名称              |
| items[].port_info[].version   | string   | 系统服务版本          |
| items[].os_info               | object   | 操作系统信息          |
| items[].os_info.name          | string   | 操作系统名称          |
| items[].ip_type               | string   | IP类型                |
| items[].cdn_name              | string   | CDN厂商名称           |
| items[].geo_asn               | object   | AS信息                |
| items[].geo_city              | object   | 地理位置信息          |
| items[].task_id               | string   | 关联任务ID            |
| items[].create_time           | string   | 创建时间，ISO8601格式 |
| query                         | object   | 查询参数              |

### 2. 导出IP端口

**请求方法与地址**：
```
GET /api/ip/export/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的IP端口信息。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含IP端口信息，格式为"IP:端口"，每行一条记录。文件命名格式为：`ip_{记录数}_{时间戳}.txt`。

### 3. 导出域名

**请求方法与地址**：
```
GET /api/ip/export_domain/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的域名。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含与筛选条件匹配的IP相关联的域名，每行一个域名。文件命名格式为：`ip_domain_{记录数}_{时间戳}.txt`。

### 4. 导出IP

**请求方法与地址**：
```
GET /api/ip/export_ip/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于筛选要导出的IP地址。

**响应**：
文件下载（text/plain或application/octet-stream）

**响应内容说明**：
导出的文件包含与筛选条件匹配的IP地址，每行一个IP地址。文件命名格式为：`ip_ip_{记录数}_{时间戳}.txt`。

### 5. 删除IP

**请求方法与地址**：
```
POST /api/ip/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明              |
| ------ | --------- | -------- | ----------------- |
| _id    | string[]  | 是       | 要删除的IP记录ID列表 |

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

| 字段名    | 类型      | 说明              |
| --------- | --------- | ----------------- |
| data._id  | string[]  | 成功删除的IP记录ID列表 |

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
    "error": "IP格式错误"
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