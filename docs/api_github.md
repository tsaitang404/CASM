# GitHub相关接口

GitHub任务、监控、结果管理等。

- 任务管理: GET/POST /api/github_task/
- 停止任务: POST /api/github_task/stop/
- 删除任务: POST /api/github_task/delete/
- 监控管理: GET/POST /api/github_scheduler/
- 更新监控: POST /api/github_scheduler/update/
- 删除监控: POST /api/github_scheduler/delete/
- 停止监控: POST /api/github_scheduler/stop/
- 恢复监控: POST /api/github_scheduler/recover/
- 任务结果: GET /api/github_result/
- 监控结果: GET /api/github_monitor_result/

参数示例：
```json
{
  "name": "任务名称",
  "keyword": "关键字",
  "_id": ["任务ID"]
}
```