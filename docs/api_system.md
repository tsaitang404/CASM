# 系统状态与通用接口

系统状态监控、批量导出等。

- 系统状态: GET /api/status/
- 批量导出站点: POST /api/batch_export/site/
- 批量导出域名: POST /api/batch_export/domain/
- 批量导出IP: POST /api/batch_export/ip/
- 批量导出URL: POST /api/batch_export/url/

参数示例：
```json
{
  "task_id": ["任务ID列表"]
}
```