# 资产分组接口

资产分组用于对资产进行分类管理，便于对不同类型、不同业务线的资产进行统一管理和监控。

## API概览

| 接口功能     | HTTP方法 | 请求路径                    | 说明                       |
| ------------ | -------- | --------------------------- | -------------------------- |
| 查询资产分组 | GET      | /api/asset_scope/           | 获取资产分组列表或特定分组 |
| 添加资产分组 | POST     | /api/asset_scope/           | 创建新的资产分组           |
| 删除资产分组 | DELETE   | /api/asset_scope/{id}       | 删除特定资产分组(REST风格) |
| 批量删除分组 | POST     | /api/asset_scope/delete/    | 批量删除资产分组           |
| 编辑资产分组 | PUT      | /api/asset_scope/{id}       | 更新特定资产分组(REST风格) |
| 批量编辑分组 | POST     | /api/asset_scope/edit/      | 批量更新资产分组信息       |

## 通用字段说明

| 字段名 | 类型   | 是否必填 | 说明           |
| ------ | ------ | -------- | -------------- |
| name   | string | 是       | 资产分组名称   |
| desc   | string | 否       | 资产分组描述   |
| _id    | string | 否       | 资产分组唯一ID |

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

### 1. 查询资产分组

**请求方法与地址**：
```
GET /api/asset_scope/
```

**查询参数**：

| 参数名 | 类型   | 是否必填 | 说明                     |
| ------ | ------ | -------- | ------------------------ |
| name   | string | 否       | 按分组名称模糊筛选       |
| page   | number | 否       | 页码，默认为1            |
| size   | number | 否       | 每页记录数，默认为20     |
| id     | string | 否       | 查询特定ID的分组，精确匹配 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 10,
    "page": 1,
    "size": 20,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "核心业务系统",
        "desc": "公司核心业务系统资产分组",
        "create_time": "2023-01-15T08:30:00.000Z",
        "update_time": "2023-01-15T08:30:00.000Z"
      },
      // ...更多分组
    ]
  }
}
```

**响应字段说明**：

| 字段名                | 类型    | 说明                     |
| --------------------- | ------- | ------------------------ |
| data.total            | number  | 符合条件的记录总数       |
| data.page             | number  | 当前页码                 |
| data.size             | number  | 每页记录数               |
| data.items            | array   | 资产分组记录数组         |
| data.items[].\_id     | string  | 分组唯一ID               |
| data.items[].name     | string  | 分组名称                 |
| data.items[].desc     | string  | 分组描述                 |
| data.items[].create_time | string | 分组创建时间，ISO8601格式 |
| data.items[].update_time | string | 分组最后更新时间，ISO8601格式 |

### 2. 添加资产分组

**请求方法与地址**：
```
POST /api/asset_scope/
```

**请求体**：
```json
{
  "name": "核心业务系统",
  "desc": "公司核心业务系统资产分组"
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "核心业务系统",
    "desc": "公司核心业务系统资产分组",
    "create_time": "2023-05-11T14:30:00.000Z",
    "update_time": "2023-05-11T14:30:00.000Z"
  }
}
```

**响应字段说明**：

| 字段名          | 类型   | 说明                          |
| --------------- | ------ | ----------------------------- |
| data.\_id       | string | 新创建的分组唯一ID            |
| data.name       | string | 分组名称                      |
| data.desc       | string | 分组描述                      |
| data.create_time | string | 分组创建时间，ISO8601格式     |
| data.update_time | string | 分组最后更新时间，ISO8601格式 |

### 3. 删除资产分组

**方法1: 删除单个分组（REST风格）**

**请求方法与地址**：
```
DELETE /api/asset_scope/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 分组ID   |

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

**方法2: 批量删除分组**

**请求方法与地址**：
```
POST /api/asset_scope/delete/
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
| data.deleted | number  | 成功删除的分组数量 |

### 4. 编辑资产分组

**方法1: 编辑单个分组（REST风格）**

**请求方法与地址**：
```
PUT /api/asset_scope/{id}
```

**路径参数**：

| 参数名 | 类型   | 是否必填 | 说明     |
| ------ | ------ | -------- | -------- |
| id     | string | 是       | 分组ID   |

**请求体**：
```json
{
  "name": "更新后的分组名称",
  "desc": "更新后的分组描述"
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "name": "更新后的分组名称",
    "desc": "更新后的分组描述",
    "update_time": "2023-05-11T15:30:00.000Z"
  }
}
```

**响应字段说明**：

| 字段名          | 类型   | 说明                         |
| --------------- | ------ | ---------------------------- |
| data.\_id       | string | 分组唯一ID                   |
| data.name       | string | 更新后的分组名称             |
| data.desc       | string | 更新后的分组描述             |
| data.update_time | string | 分组更新时间，ISO8601格式    |

**方法2: 批量编辑分组**

**请求方法与地址**：
```
POST /api/asset_scope/edit/
```

**请求体**：
```json
{
  "_id": "60f8c2b2e13e4b1e8c8b4567",
  "name": "更新后的分组名称",
  "desc": "更新后的分组描述"
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "updated": 1,
    "item": {
      "_id": "60f8c2b2e13e4b1e8c8b4567",
      "name": "更新后的分组名称",
      "desc": "更新后的分组描述",
      "update_time": "2023-05-11T15:30:00.000Z"
    }
  }
}
```

**响应字段说明**：

| 字段名           | 类型    | 说明                         |
| ---------------- | ------- | ---------------------------- |
| data.updated     | number  | 成功更新的分组数量           |
| data.item        | object  | 更新后的分组信息             |
| data.item.\_id   | string  | 分组唯一ID                   |
| data.item.name   | string  | 更新后的分组名称             |
| data.item.desc   | string  | 更新后的分组描述             |
| data.item.update_time | string | 分组更新时间，ISO8601格式 |

## 错误响应

### 通用错误码

| 错误码 | 描述                 | 说明               |
| ------ | -------------------- | ------------------ |
| 1000   | InternalError        | 服务器内部错误     |
| 1001   | GroupNameExists      | 分组名称已存在     |
| 1003   | NotFound             | 找不到请求的资源   |
| 1004   | InvalidParameter     | 参数无效           |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.name   | string | 相关分组名称（可选）     |
| data.id     | string | 相关资源ID（可选）       |

### 错误示例
分组名称已存在：
```json
{
  "code": 1001,
  "msg": "GroupNameExists",
  "data": {
    "name": "已存在的分组名称"
  }
}
```

分组不存在：
```json
{
  "code": 1003,
  "msg": "NotFound",
  "data": {
    "id": "不存在的分组ID"
  }
}