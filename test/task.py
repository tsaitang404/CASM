import unittest
from app import celerytask
from app.utils import conn_db as conn
from app.modules import CeleryAction

task_data = {
    'name': '自动化测试',
    'target': 'www.tophant.com',
    'start_time': '-',
    'status': 'waiting',
    'type': 'domain',
    "task_tag": "task",  # 标记为正常下发的任务
    'options': {
        'domain_brute': True,
        'domain_brute_type': 'test',
        'port_scan_type': 'custom',
        'port_custom': '80,443,22',
        'host_timeout_type': 'custom',
        'host_timeout': 130,
        'port_parallelism': 12,
        'port_min_rate': 13,
        'port_scan': True,
        'service_detection': False,
        'service_brute': False,
        'os_detection': False,
        'site_identify': True,
        'site_capture': True,
        'file_leak': False,
        'alt_dns': False,
        'site_spider': True,
        'search_engines': True,
        'ssl_cert': False,
        'casm_search': True,
        'dns_query_plugin': False
    }
}


def submit_task(task_data):
    """
    将任务数据提交到数据库，并通过 Celery 框架将任务分发到相应的队列中执行

    参数:
        task_data (dict): 包含任务数据的字典

    返回:
        dict: 更新后的任务数据字典
    """
    # 将任务数据插入到数据库的 task 集合中
    conn('task').insert_one(task_data)
    
    # 从任务数据中弹出 _id 字段，并将其转换为字符串，作为任务的唯一标识
    task_id = str(task_data.pop("_id"))
    
    # 将任务的唯一标识添加到任务数据中
    task_data["task_id"] = task_id

    # 根据任务的类型设置 Celery 任务的动作
    celery_action = CeleryAction.DOMAIN_TASK
    if task_data["type"] == "domain":
        celery_action = CeleryAction.DOMAIN_TASK
    elif task_data["type"] == "ip":
        celery_action = CeleryAction.IP_TASK

    # 构建 Celery 任务的选项字典，包含任务动作和任务数据
    task_options = {
        "celery_action": celery_action,
        "data": task_data
    }

    # 通过 Celery 框架将任务分发到相应的队列中执行
    celerytask.casm_task(options=task_options)

    # 返回更新后的任务数据字典
    return task_data


def test_exec_task(self):
    """
    测试执行任务的功能

    该测试用例首先调用 submit_task 函数提交一个任务，然后检查数据库中是否存在相应的记录。
    它验证了在任务数据中指定的域名和 IP 地址是否被正确处理，并且根据任务选项中的设置，
    检查了是否进行了端口扫描并在数据库中保存了相应的结果。

    参数:
        self (TestExecTask): 测试类的实例

    返回:
        None
    """
    # 提交任务数据
    submit_task(task_data)

    # 构建查询条件，用于检索任务的唯一标识
    query = {"task_id": task_data["task_id"]}

    # 验证 site 集合中是否存在至少一条记录
    self.assertTrue(len(list(conn("site").find(query))) >= 1)

    # 验证 domain 集合中是否存在至少一条记录
    self.assertTrue(len(list(conn("domain").find(query))) >= 1)

    # 如果任务选项中指定了进行端口扫描
    if task_data["options"]["port_scan"]:
        # 验证 ip 集合中是否存在至少一条记录
        self.assertTrue(len(list(conn("ip").find(query))) >= 1)


if __name__ == '__main__':
    unittest.main()