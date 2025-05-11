# POC信息接口

提供POC(Proof of Concept)插件的查询、同步、清空等功能。

## API概览

| 接口功能   | HTTP方法 | 请求路径          | 说明                     |
| ---------- | -------- | ----------------- | ------------------------ |
| 查询POC    | GET      | /api/poc/         | 获取POC列表或特定POC信息 |
| 同步POC    | GET      | /api/poc/sync/    | 更新并同步POC信息到数据库|
| 清空POC    | GET      | /api/poc/delete/  | 清空数据库中的所有POC信息|

## 通用字段说明

| 字段名       | 类型     | 是否必填 | 说明                                        |
| ------------ | -------- | -------- | ------------------------------------------- |
| plugin_name  | string   | 否       | POC名称ID，用于精确查询特定POC              |
| app_name     | string   | 否       | 应用名称，用于查询特定应用的POC             |
| scheme       | string   | 否       | 支持的协议，如http、https、ssh等            |
| vul_name     | string   | 否       | 漏洞名称                                    |
| plugin_type  | string   | 否       | 插件类别，可选值：'poc'、'brute'            |
| update_date  | string   | 否       | 更新时间                                    |
| category     | string   | 否       | POC分类                                     |
| page         | number   | 否       | 页码，默认为1                               |
| size         | number   | 否       | 每页记录数，默认为10                        |

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

### 1. 查询POC

**请求方法与地址**：
```
GET /api/poc/
```

**查询参数**：

通用字段说明中的所有字段均可作为查询参数。

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 256,
    "page": 1,
    "size": 10,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "plugin_name": "springboot_actuator_unauthorized",
        "app_name": "Spring Boot",
        "vul_name": "Spring Boot Actuator未授权访问",
        "plugin_type": "poc",
        "scheme": "http",
        "update_date": "2022-05-01",
        "category": "信息泄露",
        "description": "Spring Boot Actuator未经授权访问可能导致敏感信息泄露"
      },
      {
        "_id": "60f8c2b2e13e4b1e8c8b4568",
        "plugin_name": "tomcat_weak_password",
        "app_name": "Tomcat",
        "vul_name": "Tomcat默认弱口令",
        "plugin_type": "brute",
        "scheme": "http",
        "update_date": "2022-04-15",
        "category": "弱口令",
        "description": "Tomcat管理界面存在默认或弱口令"
      }
      // ... 更多POC信息
    ]
  }
}
```

**响应字段说明**：

| 字段名                    | 类型     | 说明                 |
| ------------------------- | -------- | -------------------- |
| data.total                | number   | 符合条件的记录总数   |
| data.page                 | number   | 当前页码             |
| data.size                 | number   | 每页记录数           |
| data.items                | array    | POC记录数组          |
| data.items[].\_id         | string   | POC唯一ID            |
| data.items[].plugin_name  | string   | POC名称ID            |
| data.items[].app_name     | string   | 应用名称             |
| data.items[].vul_name     | string   | 漏洞名称             |
| data.items[].plugin_type  | string   | 插件类别             |
| data.items[].scheme       | string   | 支持的协议           |
| data.items[].update_date  | string   | 更新时间             |
| data.items[].category     | string   | POC分类              |
| data.items[].description  | string   | 漏洞描述             |

### 2. 同步POC

**请求方法与地址**：
```
GET /api/poc/sync/
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "plugin_cnt": 256
  }
}
```

**响应字段说明**：

| 字段名         | 类型    | 说明           |
| -------------- | ------- | -------------- |
| data.plugin_cnt| number  | 同步的插件数量 |

### 3. 清空POC

**请求方法与地址**：
```
GET /api/poc/delete/
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "delete_cnt": 256
  }
}
```

**响应字段说明**：

| 字段名         | 类型    | 说明           |
| -------------- | ------- | -------------- |
| data.delete_cnt| number  | 删除的记录数量 |

## 错误响应

### 通用错误码

| 错误码 | 描述              | 说明               |
| ------ | ----------------- | ------------------ |
| 500    | Error             | 系统异常           |
| 401    | NotLogin          | 用户未登录         |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| message     | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |

### 错误示例
用户未登录：
```json
{
  "code": 401,
  "message": "NotLogin",
  "data": {}
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