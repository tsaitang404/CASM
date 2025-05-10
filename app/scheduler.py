import sys
from bson import ObjectId
from app.utils import conn_db as conn
from app import utils
from app import celerytask
import time
from app.modules import CeleryAction, SchedulerStatus, AssetScopeType
from app.helpers import task_schedule, asset_site_monitor, asset_wih_monitor

logger = utils.get_logger()

domain_monitor_options = {
    'domain_brute': True,
    'domain_brute_type': 'big',
    'alt_dns': False,
    'casm_search': True,
    'port_scan_type': 'test',
    'port_scan': True,
    'dns_query_plugin': True,
    'site_identify': False
}

ip_monitor_options = {
    'port_scan_type': 'test',
    'port_scan': True,
    'site_identify': False
}


def add_job(domain, scope_id, options=None, interval=60 * 1, name="", scope_type=AssetScopeType.DOMAIN):
    logger.info("add {} job {} {} {}".format(scope_type, interval, domain, scope_id))
    if options is None:
        if scope_type == AssetScopeType.DOMAIN:
            options = domain_monitor_options
        if scope_type == AssetScopeType.IP:
            options = ip_monitor_options

    # 对IP任务域名监测选项设置为False
    disable_options = {
        "domain_brute": False,
        "alt_dns": False,
        "dns_query_plugin": False,
        "casm_search": False
    }

    if scope_type == AssetScopeType.IP:
        options.update(disable_options)

    current_time = int(time.time()) + 30
    item = {
        "domain": domain,
        "scope_id": scope_id,
        "interval": interval,
        "next_run_time": current_time,
        "next_run_date": utils.time2date(current_time),
        "last_run_time": 0,
        "last_run_date": "-",
        "run_number": 0,
        "status": SchedulerStatus.RUNNING,
        "monitor_options": options,
        "name": name,
        "scope_type": scope_type

    }
    conn('scheduler').insert(item)

    return str(item["_id"])


def add_asset_site_monitor_job(scope_id, name, interval=60 * 1):
    current_time = int(time.time()) + 30

    item = {
        "domain": "资产站点更新",
        "scope_id": scope_id,
        "interval": interval,
        "next_run_time": current_time,
        "next_run_date": utils.time2date(current_time),
        "last_run_time": 0,
        "last_run_date": "-",
        "run_number": 0,
        "status": SchedulerStatus.RUNNING,
        "monitor_options": {},
        "name": name,
        "scope_type": "site_update_monitor"
    }
    conn('scheduler').insert(item)

    return str(item["_id"])


def add_asset_wih_monitor_job(scope_id, name, interval=60 * 1):
    current_time = int(time.time()) + 30

    item = {
        "domain": "资产分组 WIH 更新",
        "scope_id": scope_id,
        "interval": interval,
        "next_run_time": current_time,
        "next_run_date": utils.time2date(current_time),
        "last_run_time": 0,
        "last_run_date": "-",
        "run_number": 0,
        "status": SchedulerStatus.RUNNING,
        "monitor_options": {},
        "name": name,
        "scope_type": "wih_update_monitor"
    }
    conn('scheduler').insert(item)

    return str(item["_id"])


def delete_job(job_id):
    ret = conn("scheduler").delete_one({"_id": ObjectId(job_id)})
    return ret


def stop_job(job_id):
    item = find_job(job_id)
    item["next_run_date"] = "-"
    item["next_run_time"] = sys.maxsize
    item["status"] = SchedulerStatus.STOP
    query = {"_id": ObjectId(job_id)}
    ret = conn('scheduler').find_one_and_replace(query, item)
    return ret


def recover_job(job_id):
    current_time = int(time.time()) + 30
    item = find_job(job_id)

    next_run_time = current_time + item["interval"]
    item["next_run_date"] = utils.time2date(next_run_time)
    item["next_run_time"] = next_run_time
    item["status"] = SchedulerStatus.RUNNING
    query = {"_id": ObjectId(job_id)}
    ret = conn('scheduler').find_one_and_replace(query, item)
    return ret


def find_job(job_id):
    query = {"_id": ObjectId(job_id)}
    item = conn('scheduler').find_one(query)
    return item


def all_job():
    items = []
    for item in conn('scheduler').find():
        items.append(item)
    return items


def submit_job(domain, job_id, scope_id, options=None, name="", scope_type=AssetScopeType.DOMAIN):
    monitor_options = domain_monitor_options.copy()
    if scope_type == AssetScopeType.IP:
        monitor_options = ip_monitor_options.copy()

    if options is None:
        options = {}

    monitor_options.update(options)

    task_data = {
        "domain": domain,
        "scope_id": scope_id,
        "job_id": job_id,
        "type": scope_type,
        "monitor_options": monitor_options,
        "name": name
    }

    if scope_type == AssetScopeType.DOMAIN:
        task_options = {
            "celery_action": CeleryAction.DOMAIN_EXEC_TASK,
            "data": task_data
        }
        celery_id = celerytask.casm_task.delay(options=task_options)
        logger.info("submit domain job {} {} {}".format(celery_id, domain, scope_id))

    if scope_type == AssetScopeType.IP:
        task_options = {
            "celery_action": CeleryAction.IP_EXEC_TASK,
            "data": task_data
        }
        celery_id = celerytask.casm_task.delay(options=task_options)
        logger.info("submit ip job {} {} {}".format(celery_id, domain, scope_id))


def update_job_run(job_id):
    curr_time = int(time.time())
    item = find_job(job_id)
    if not item:
        return
    item["next_run_time"] = curr_time + item["interval"]
    item["next_run_date"] = utils.time2date(item["next_run_time"])
    item["last_run_time"] = curr_time
    item["last_run_date"] = utils.time2date(curr_time)
    item["run_number"] += 1
    query = {"_id": item["_id"]}
    conn('scheduler').find_one_and_replace(query, item)


def asset_monitor_scheduler():
    curr_time = int(time.time())
    # 只获取实际的调度任务
    for item in conn('scheduler').find({"scope_type": {"$exists": True}}):
        try:
            if not item.get("next_run_time"):
                logger.warning(f"Task {item.get('_id')} missing next_run_time field, setting default value")
                item["next_run_time"] = curr_time + 30
                item["next_run_date"] = utils.time2date(item["next_run_time"])
                query = {"_id": item["_id"]}
                conn('scheduler').find_one_and_replace(query, item)
                continue

            if item.get("status") == SchedulerStatus.STOP:
                continue

            if item["next_run_time"] <= curr_time:
                domain = item.get("domain", "")
                scope_id = item.get("scope_id", "")
                options = item.get("monitor_options", {})
                name = item.get("name", "")
                scope_type = item.get("scope_type")

                if scope_type == "site_update_monitor":
                    asset_site_monitor.submit_asset_site_monitor_job(scope_id=scope_id,
                                                                     name=name,
                                                                     scheduler_id=str(item["_id"]))

                elif scope_type == "wih_update_monitor":
                    asset_wih_monitor.submit_asset_wih_monitor_job(scope_id=scope_id,
                                                                   name=name,
                                                                   scheduler_id=str(item["_id"]))

                else:
                    submit_job(domain=domain, job_id=str(item["_id"]),
                               scope_id=scope_id, options=options,
                               name=name, scope_type=scope_type)

                item["next_run_time"] = curr_time + item.get("interval", 3600)
                item["next_run_date"] = utils.time2date(item["next_run_time"])
                query = {"_id": item["_id"]}
                conn('scheduler').find_one_and_replace(query, item)

        except Exception as e:
            logger.exception(e)


def register_scheduler_status():
    """注册调度器状态到casm数据库的scheduler集合中"""
    current_time = int(time.time())
    status_data = {
        "status": "running",
        "start_time": current_time,
        "uptime": "0h",
        "tasks_total": 0,
        "tasks_active": 0,
        "last_update": current_time
    }
    
    db = conn('scheduler', 'casm')
    # 删除任何已存在的记录
    db.delete_many({"_id": {"$exists": True}})
    # 创建新记录
    db.insert_one(status_data)

class SchedulerStatusMonitor:
    """调度器状态监控器，负责维护调度器状态"""
    HEARTBEAT_TIMEOUT = 60  # 60秒超时

    @classmethod
    def check_and_reset_dead_scheduler(cls):
        """检查并重置已经停止的调度器状态"""
        try:
            current_time = int(time.time())
            scheduler = conn('scheduler', 'casm').find_one({})
            
            if scheduler:
                last_update = scheduler.get('last_update', 0)
                if current_time - last_update > cls.HEARTBEAT_TIMEOUT:
                    # 更新状态为stopped
                    conn('scheduler', 'casm').update_one(
                        {"_id": scheduler["_id"]},
                        {
                            "$set": {
                                "status": "stopped",
                                "message": "调度器已停止运行(心跳超时)",
                                "tasks_active": 0
                            }
                        }
                    )
                    logger.warning("检测到调度器心跳超时，已将状态更新为stopped")
        except Exception as e:
            logger.error(f"检查调度器状态时发生错误: {str(e)}")

def update_scheduler_status():
    """更新调度器状态"""
    current_time = int(time.time())
    db = conn('scheduler', 'casm')
    scheduler_status = db.find_one({})
    
    if not scheduler_status:
        register_scheduler_status()
        return
        
    start_time = scheduler_status['start_time']
    uptime_seconds = current_time - start_time
    uptime_hours = uptime_seconds / 3600
    
    # 计算活跃任务数 - 注意这里使用的是默认数据库的scheduler集合
    total_tasks = conn('scheduler').count_documents({"scope_type": {"$exists": True}})
    active_tasks = conn('scheduler').count_documents({
        "scope_type": {"$exists": True}, 
        "status": SchedulerStatus.RUNNING
    })
    
    update_data = {
        "status": "running",
        "uptime": f"{uptime_hours:.1f}h",
        "tasks_total": total_tasks,
        "tasks_active": active_tasks,
        "last_update": current_time
    }
    
    db.update_one({"_id": scheduler_status["_id"]}, {"$set": update_data})

def run_forever():
    from app.utils.github_task import github_task_scheduler
    logger.info("start scheduler server ")
    
    # 注册调度器状态
    register_scheduler_status()
    
    # 检查并重置可能存在的已停止调度器状态
    SchedulerStatusMonitor.check_and_reset_dead_scheduler()
    
    while True:
        try:
            # 资产监控任务调度
            asset_monitor_scheduler()

            # Github 监控任务调度
            github_task_scheduler()

            # 计划任务调度
            task_schedule.task_scheduler()

            # 更新调度器状态
            update_scheduler_status()

            # 检查并重置其他已停止的调度器状态
            SchedulerStatusMonitor.check_and_reset_dead_scheduler()

            time.sleep(58)
        except Exception as e:
            logger.exception(e)
            # 发生异常时也要更新状态
            try:
                conn('scheduler', 'casm').update_one({}, {"$set": {"status": "error"}})
            except:
                pass


if __name__ == '__main__':
    run_forever()
