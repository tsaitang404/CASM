# 指纹管理接口

指纹规则的增删查、导入导出等。

## API概览

| 接口功能   | HTTP方法 | 请求路径                    | 说明                       |
| ---------- | -------- | --------------------------- | -------------------------- |
| 查询指纹   | GET      | /api/fingerprint/           | 获取指纹列表或特定指纹信息 |
| 添加指纹   | POST     | /api/fingerprint/           | 创建新的指纹规则           |
| 删除指纹   | DELETE   | /api/fingerprint/{id}       | 删除特定指纹规则           |
| 批量删除   | POST     | /api/fingerprint/delete/    | 批量删除指纹规则           |
| 导出指纹   | GET      | /api/fingerprint/export/    | 导出指纹规则为JSON文件     |
| 导入指纹   | POST     | /api/fingerprint/upload/    | 从文件导入指纹规则         |

## 通用字段说明

| 字段名      | 类型     | 是否必填 | 说明                                                                                                                         |
| ----------- | -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| name        | string   | 是       | 指纹名称                                                                                                                     |
| human_rule  | string   | 是       | 指纹规则。格式要求：由一个或多个"key="value""表达式组成，多个表达式用"||"分隔，表示"或"关系。支持的 key 有 body（网页正文内容）、title（网页标题）、header（HTTP 响应头）、icon_hash（网站 favicon 的 hash 值，需为整数）。value 必须用英文双引号包裹，且长度大于6。例如：body="test.gif"、title="Apache"、header="Server: nginx"、icon_hash="116323821"，多条件示例：body="test.gif" || title="Apache"。不符合上述格式（如 key 不支持、value 未用双引号、长度过短等）会被判定为无效，接口会返回"规则无效"错误。 |
| _id         | string   | 否       | 指纹ID，在更新和删除操作中使用                                                                                               |

## 通用响应格式

所有API响应都遵循以下格式：

```json
{
  "code": 0,       // 响应码，0表示成功，非0表示出错
  "msg": "Success", // 响应消息
  "data": {}       // 响应数据，格式因API而异
}
```

### 通用响应字段说明

| 字段名 | 类型   | 说明                                        |
| ------ | ------ | ------------------------------------------- |
| code   | number | 响应码，0表示成功，非0表示出错              |
| msg    | string | 响应消息，成功时为"Success"，失败时为错误信息 |
| data   | object | 响应数据，不同API返回的数据结构不同         |

## 详细API说明

### 1. 查询指纹

**请求方法与地址**：
```
GET /api/fingerprint/
```

**查询参数**：

| 参数名 | 类型   | 是否必填 | 说明                           |
| ------ | ------ | -------- | ------------------------------ |
| name   | string | 否       | 按指纹名称筛选                 |
| page   | number | 否       | 页码，默认为1                  |
| size   | number | 否       | 每页记录数，默认为20           |
| id     | string | 否       | 查询特定ID的指纹，精确匹配     |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 120,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "Apache",
        "human_rule": "body=\"test.gif\" || title=\"Apache\""
      },
      // ...更多指纹
    ]
  }
}
```

**响应字段说明**：

| 字段名      | 类型    | 说明                        |
| ----------- | ------- | --------------------------- |
| data.total  | number  | 符合条件的记录总数          |
| data.page   | number  | 当前页码                    |
| data.size   | number  | 每页记录数                  |
| data.items  | array   | 指纹记录数组                |
| data.items[].\_id    | string  | 指纹唯一ID         |
| data.items[].name    | string  | 指纹名称           |
| data.items[].human_rule | string | 指纹规则表达式   |

### 2. 添加指纹

**请求方法与地址**：
```
POST /api/fingerprint/
```

**请求体**：
```json
{
  "name": "指纹名称",
  "human_rule": "body=\"test.gif\" || title=\"Apache\""
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "Apache",
    "human_rule": "body=\"test.gif\" || title=\"Apache\""
  }
}
```

**响应字段说明**：

| 字段名         | 类型    | 说明                     |
| -------------- | ------- | ------------------------ |
| data.\_id      | string  | 新创建的指纹唯一ID       |
| data.name      | string  | 指纹名称                 |
| data.human_rule| string  | 指纹规则表达式           |

### 3. 删除指纹

**方法1: 删除单个指纹（REST风格）**

**请求方法与地址**：
```
DELETE /api/fingerprint/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 指纹ID   |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 1
  }
}
```

**响应字段说明**：

| 字段名       | 类型    | 说明           |
| ------------ | ------- | -------------- |
| data.deleted | number  | 成功删除的数量 |

**方法2: 批量删除指纹**

**请求方法与地址**：
```
POST /api/fingerprint/delete/
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
  "code": 0,
  "msg": "Success",
  "data": {
    "deleted": 2
  }
}
```

**响应字段说明**：

| 字段名       | 类型    | 说明               |
| ------------ | ------- | ------------------ |
| data.deleted | number  | 成功删除的指纹数量 |

### 4. 导出指纹

**请求方法与地址**：
```
GET /api/fingerprint/export/
```

**查询参数**：

| 参数名 | 类型   | 是否必填 | 说明                       |
| ------ | ------ | -------- | -------------------------- |
| name   | string | 否       | 按指纹名称筛选要导出的内容 |

**响应**：
文件下载（application/json）

**响应内容说明**：
导出的JSON文件包含指纹规则数组，每个规则包含以下字段：

| 字段名     | 类型   | 说明           |
| ---------- | ------ | -------------- |
| name       | string | 指纹名称       |
| human_rule | string | 指纹规则表达式 |

### 5. 导入指纹

**请求方法与地址**：
```
POST /api/fingerprint/upload/
```

**请求头**：
```
Content-Type: multipart/form-data
```

**请求参数**：

| 参数名 | 类型 | 是否必填 | 说明                               |
| ------ | ---- | -------- | ---------------------------------- |
| file   | file | 是       | 要上传的指纹文件，格式为JSON       |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "imported": 10,
    "duplicated": 2,
    "invalid": 1
  }
}
```

**响应字段说明**：

| 字段名          | 类型   | 说明                 |
| --------------- | ------ | ------------------- |
| data.imported   | number | 成功导入的指纹数量   |
| data.duplicated | number | 重复的指纹数量       |
| data.invalid    | number | 无效的指纹数量       |

## 错误响应

### 通用错误码

| 错误码 | 描述                   | 说明                       |
| ------ | ---------------------- | -------------------------- |
| 1000   | InternalError          | 服务器内部错误             |
| 1001   | RuleAlreadyExists      | 指纹规则已存在             |
| 1002   | RuleInvalid            | 指纹规则格式无效           |
| 1003   | NotFound               | 找不到请求的资源           |
| 1004   | InvalidParameter       | 参数无效                   |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.rule   | string | 相关规则信息（可选）     |
| data.id     | string | 相关资源ID（可选）       |

### 错误示例
规则已存在：
```json
{
  "code": 1001,
  "msg": "RuleAlreadyExists",
  "data": {
    "rule": "已存在的规则"
  }
}
```

规则无效：
```json
{
  "code": 1002,
  "msg": "RuleInvalid",
  "data": {
    "error": "Error evaluating expression: ... exception: ..."
  }
}