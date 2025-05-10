# POC信息接口

POC插件的查询、同步、清空等。

- 查询POC: GET /api/poc/
- 同步POC: GET /api/poc/sync/
- 清空POC: GET /api/poc/delete/

参数示例：
```json
{
  "plugin_name": "POC名称ID",
  "app_name": "应用名称"
}
```