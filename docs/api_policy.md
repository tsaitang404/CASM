# 策略配置接口

策略的增删查改及配置说明。

- 查询策略: GET /api/policy/
- 添加策略: POST /api/policy/add/
- 编辑策略: POST /api/policy/edit/
- 删除策略: POST /api/policy/delete/

参数示例：
```json
{
  "name": "策略名称",
  "desc": "描述",
  "policy": { ... },
  "policy_id": "策略ID"
}
```