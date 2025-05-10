# 资产监控接口

站点状态监控、标签管理、站点导出、删除等。

- 站点状态监控: GET /api/asset_site/monitor/
- 添加标签: POST /api/asset_site/add_tag/
- 删除标签: POST /api/asset_site/delete_tag/
- 删除站点: POST /api/asset_site/delete/
- 保存站点到结果集: GET /api/asset_site/save_result_set/

参数示例：
```json
{
  "tag": "标签名称",
  "_id": "站点ID"
}
```