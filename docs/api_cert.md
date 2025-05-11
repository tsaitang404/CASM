# 证书信息接口

提供SSL证书的查询和删除等功能，支持按各种属性进行筛选查询。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询证书     | GET      | /api/cert/            | 获取证书列表或特定证书信息 |
| 删除证书     | POST     | /api/cert/delete/     | 删除特定证书记录         |

## 通用字段说明

### 基础查询参数

| 字段名                         | 类型     | 是否必填 | 说明                     |
| ------------------------------ | -------- | -------- | ------------------------ |
| ip                             | string   | 否       | IP地址，支持模糊查询     |
| port                           | number   | 否       | 端口号                   |
| cert.subject_dn                | string   | 否       | 主题名称，支持模糊查询   |
| cert.issuer_dn                 | string   | 否       | 签发者名称，支持模糊查询 |
| cert.serial_number             | string   | 否       | 序列号，支持模糊查询     |
| cert.validity.start            | string   | 否       | 有效期开始时间           |
| cert.validity.end              | string   | 否       | 有效期结束时间           |
| cert.fingerprint.sha256        | string   | 否       | SHA-256指纹              |
| cert.fingerprint.sha1          | string   | 否       | SHA-1指纹                |
| cert.fingerprint.md5           | string   | 否       | MD5指纹                  |
| cert.extensions.subjectAltName | string   | 否       | 主题备用名称，支持模糊查询 |
| task_id                        | string   | 否       | 关联的任务ID             |
| page                           | number   | 否       | 页码，默认为1            |
| size                           | number   | 否       | 每页记录数，默认为10     |
| order                          | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询证书

**请求方法与地址**：
```
GET /api/cert/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤证书。

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
      "ip": "203.0.113.1",
      "port": 443,
      "cert": {
        "subject_dn": "CN=example.com,O=Example Inc,L=Beijing,C=CN",
        "issuer_dn": "CN=DigiCert SHA2 Secure Server CA,O=DigiCert Inc,C=US",
        "serial_number": "0A:BC:DE:F1:23:45:67:89",
        "validity": {
          "start": "2023-01-01T00:00:00.000Z",
          "end": "2024-01-01T23:59:59.000Z"
        },
        "fingerprint": {
          "sha256": "a1b2c3d4e5f6...",
          "sha1": "a1b2c3d4e5f6...",
          "md5": "a1b2c3d4..."
        },
        "extensions": {
          "subjectAltName": ["example.com", "www.example.com", "*.example.com"]
        }
      },
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    }
    // ... 更多证书记录
  ],
  "query": {
    "cert.extensions.subjectAltName": "example.com"
  }
}
```

**响应字段说明**：

| 字段名                              | 类型     | 说明                  |
| ----------------------------------- | -------- | --------------------- |
| total                               | number   | 符合条件的记录总数    |
| page                                | number   | 当前页码              |
| size                                | number   | 每页记录数            |
| items                               | array    | 证书记录数组          |
| items[].\_id                        | string   | 证书记录唯一ID        |
| items[].ip                          | string   | IP地址                |
| items[].port                        | number   | 端口号                |
| items[].cert                        | object   | 证书信息              |
| items[].cert.subject_dn             | string   | 主题名称              |
| items[].cert.issuer_dn              | string   | 签发者名称            |
| items[].cert.serial_number          | string   | 序列号                |
| items[].cert.validity               | object   | 有效期信息            |
| items[].cert.validity.start         | string   | 有效期开始时间        |
| items[].cert.validity.end           | string   | 有效期结束时间        |
| items[].cert.fingerprint            | object   | 指纹信息              |
| items[].cert.fingerprint.sha256     | string   | SHA-256指纹           |
| items[].cert.fingerprint.sha1       | string   | SHA-1指纹             |
| items[].cert.fingerprint.md5        | string   | MD5指纹               |
| items[].cert.extensions             | object   | 扩展信息              |
| items[].cert.extensions.subjectAltName | array | 主题备用名称列表      |
| items[].task_id                     | string   | 关联任务ID            |
| items[].create_time                 | string   | 创建时间，ISO8601格式 |
| query                               | object   | 查询参数              |

### 2. 删除证书

**请求方法与地址**：
```
POST /api/cert/delete/
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
| _id    | string[]  | 是       | 要删除的证书记录ID列表 |

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
| data._id  | string[]  | 成功删除的证书记录ID列表 |

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
    "error": "证书ID格式错误"
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