# 任务管理接口

任务的增删查改、同步、状态等。

- 查询任务: GET /api/task/
- 添加任务: POST /api/task/
- 停止任务: GET /api/task/stop/<task_id>
- 批量停止: POST /api/task/batch_stop/
- 删除任务: POST /api/task/delete/
- 重新运行: POST /api/task/restart/
- 任务同步: POST /api/task/sync/
- 获取同步范围: POST /api/task/sync_scope/

参数示例：
```json
{
  "name": "任务名称",
  "target": "任务目标",
  "status": "任务状态",
  "task_id": ["任务ID列表"],
  "page": 1,
  "size": 10
}
```