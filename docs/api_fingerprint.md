# 指纹管理接口

指纹规则的增删查、导入导出等。

- 查询指纹: GET /api/fingerprint/
- 添加指纹: POST /api/fingerprint/
- 删除指纹: POST /api/fingerprint/delete/
- 导出指纹: GET /api/fingerprint/export/
- 上传指纹: POST /api/fingerprint/upload/

## 字段说明

| 字段名      | 类型     | 是否必填 | 说明                                                                                                                         |
| ----------- | -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| name        | string   | 是       | 指纹名称                                                                                                                     |
| human_rule  | string   | 是       | 指纹规则。格式要求：由一个或多个“key="value"”表达式组成，多个表达式用“||”分隔，表示“或”关系。支持的 key 有 body（网页正文内容）、title（网页标题）、header（HTTP 响应头）、icon_hash（网站 favicon 的 hash 值，需为整数）。value 必须用英文双引号包裹，且长度大于6。例如：body="test.gif"、title="Apache"、header="Server: nginx"、icon_hash="116323821"，多条件示例：body="test.gif" || title="Apache"。不符合上述格式（如 key 不支持、value 未用双引号、长度过短等）会被判定为无效，接口会返回“规则无效”错误。 |
| _id         | string[] | 否       | 指纹ID列表，删除时使用                                                                                                       |

## 参数示例
```json
{
  "name": "指纹名称",
  "human_rule": "body=\"test.gif\" || title=\"Apache\"",
  "_id": ["指纹ID"]
}
```

## 返回示例
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "_id": "60f8c2b2e13e4b1e8c8b4567",
    "data": {
      "name": "Apache",
      "human_rule": "body=\"test.gif\" || title=\"Apache\""
    }
  }
}
```

## 错误示例
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
```