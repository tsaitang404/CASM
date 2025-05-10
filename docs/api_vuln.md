# 漏洞信息接口

提供对漏洞信息的查询和删除功能，支持按不同条件筛选漏洞记录。

## API概览

| 接口功能     | HTTP方法 | 请求路径              | 说明                     |
| ------------ | -------- | --------------------- | ------------------------ |
| 查询漏洞     | GET      | /api/vuln/            | 获取漏洞记录列表         |
| 删除漏洞     | POST     | /api/vuln/delete/     | 删除特定漏洞记录         |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                     |
| ----------- | -------- | -------- | ------------------------ |
| plg_name    | string   | 否       | 插件ID，支持模糊查询     |
| plg_type    | string   | 否       | 漏洞类别，支持模糊查询   |
| vul_name    | string   | 否       | 漏洞名称，支持模糊查询   |
| app_name    | string   | 否       | 应用名称，支持模糊查询   |
| target      | string   | 否       | 目标，支持模糊查询       |
| task_id     | string   | 否       | 关联的任务ID             |
| page        | number   | 否       | 页码，默认为1            |
| size        | number   | 否       | 每页记录数，默认为10     |
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

### 1. 查询漏洞

**请求方法与地址**：
```
GET /api/vuln/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤漏洞。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "page": 1,
  "size": 10,
  "total": 25,
  "items": [
    {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "plg_name": "thinkphp_rce",
      "plg_type": "RCE",
      "vul_name": "ThinkPHP 远程命令执行漏洞",
      "app_name": "ThinkPHP",
      "target": "http://example.com/",
      "detail": {
        "payload": "/index.php?s=/index/think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=whoami",
        "response": "apache\n",
        "risk": "high"
      },
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "plg_name": "struts2_045",
      "plg_type": "RCE",
      "vul_name": "Struts2 S2-045 远程命令执行漏洞",
      "app_name": "Apache Struts2",
      "target": "http://example.org/admin/",
      "detail": {
        "payload": "Content-Type: %{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Poc',1234*1234)}.multipart/form-data",
        "response": "X-Poc: 1522756",
        "risk": "critical"
      },
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多漏洞记录
  ],
  "query": {
    "plg_type": "RCE"
  }
}
```

**响应字段说明**：

| 字段名                | 类型     | 说明                  |
| --------------------- | -------- | --------------------- |
| total                 | number   | 符合条件的记录总数    |
| page                  | number   | 当前页码              |
| size                  | number   | 每页记录数            |
| items                 | array    | 漏洞记录数组          |
| items[].\_id          | string   | 漏洞记录唯一ID        |
| items[].plg_name      | string   | 插件ID                |
| items[].plg_type      | string   | 漏洞类别              |
| items[].vul_name      | string   | 漏洞名称              |
| items[].app_name      | string   | 应用名称              |
| items[].target        | string   | 目标URL或主机         |
| items[].detail        | object   | 漏洞详情              |
| items[].task_id       | string   | 关联任务ID            |
| items[].create_time   | string   | 创建时间，ISO8601格式 |
| query                 | object   | 查询参数              |

### 2. 删除漏洞

**请求方法与地址**：
```
POST /api/vuln/delete/
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
| _id    | string[]  | 是       | 要删除的漏洞记录ID列表   |

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

| 字段名    | 类型      | 说明                     |
| --------- | --------- | ------------------------ |
| data._id  | string[]  | 成功删除的漏洞记录ID列表 |

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
    "error": "漏洞ID格式错误"
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