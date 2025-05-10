# 计划任务接口

定时任务的增删查、停止、恢复等。

- 查询定时任务: GET /api/task_schedule/
- 创建定时任务: POST /api/task_schedule/
- 删除定时任务: POST /api/task_schedule/delete/
- 停止定时任务: POST /api/task_schedule/stop/
- 恢复定时任务: POST /api/task_schedule/recover/

参数示例：
```json
{
  "policy_id": "策略ID",
  "cron": "Cron表达式",
  "start_date": "开始时间",
  "task_tag": "任务类别"
}
```