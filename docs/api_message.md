# 消息系统接口

## API概览

| 功能         | 方法 | 路径                | 说明           |
| ------------ | ---- | ------------------- | -------------- |
| 推送消息     | POST | /api/message/       | 新增一条消息（支持监控信息推送） |
| 查询消息     | GET  | /api/message/       | 查询消息列表   |
| 标记为已读   | POST | /api/message/read/  | 批量/单条已读  |

> 监控任务（如站点监控、资产监控等）可通过本消息系统接口推送监控结果或告警信息，便于统一查看和管理。

## 字段说明

| 字段名      | 类型      | 说明         |
| ----------- | --------- | ------------ |
| _id         | string    | 消息ID       |
| content     | string    | 消息内容     |
| type        | string    | 消息类型（如 task, monitor, alert 等） |
| create_time | datetime  | 创建时间     |
| read        | boolean   | 是否已读     |

## 示例

### 推送消息（监控信息）

POST /api/message/

```json
{
  "content": "资产组A有2个站点状态异常，请及时处理。",
  "type": "monitor"
}
```

### 查询消息

GET /api/message/?page=1&size=10&read=0

### 标记为已读

POST /api/message/read/

```json
{
  "_id": ["消息ID1", "消息ID2"]
}
```
