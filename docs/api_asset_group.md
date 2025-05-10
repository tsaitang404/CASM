# 资产分组接口

资产分组相关接口。

- 查询资产分组: GET /api/asset_scope/
- 添加资产分组: POST /api/asset_scope/
- 删除资产分组: POST /api/asset_scope/delete/
- 编辑资产分组: POST /api/asset_scope/edit/

参数示例：
```json
{
  "name": "分组名称",
  "desc": "描述",
  "_id": "分组ID"
}
```