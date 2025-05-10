# 资产搜索接口

资产域名、IP、站点、服务等的查询与导出。

- 域名查询: GET /api/asset_domain/
- 域名导出: POST /api/batch_export/domain/
- IP查询: GET /api/asset_ip/
- IP导出: POST /api/batch_export/ip/
- 站点查询: GET /api/asset_site/
- 站点导出: POST /api/batch_export/site/
- URL导出: POST /api/batch_export/url/
- 服务查询: GET /api/service/

参数示例：
```json
{
  "domain": "域名",
  "ip": "IP地址",
  "site": "站点URL",
  "service_name": "服务名称",
  "task_id": ["任务ID列表"],
  "page": 1,
  "size": 10
}
```