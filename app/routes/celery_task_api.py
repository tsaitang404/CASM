#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask_restx import Resource, Api, fields, Namespace
from bson import ObjectId
from celery.result import AsyncResult
from app import celerytask, utils
from app.utils import get_logger, auth, build_ret, conn_db
from . import base_query_fields, Resource, get_parser
from app.modules import TaskStatus, ErrorMsg, CeleryAction

ns = Namespace('celery_task', description="Celery任务执行与管理")
logger = get_logger()

# 基本查询字段
base_search_fields = {
    'celery_id': fields.String(description="Celery任务ID"),
    'status': fields.String(description="任务状态"),
    'task_type': fields.String(description="任务类型"),
}

base_search_fields.update(base_query_fields)

# 定义支持的任务类型列表，用于查询和API文档
supported_task_types = {
    CeleryAction.DOMAIN_TASK: "常规域名任务",
    CeleryAction.IP_TASK: "常规IP任务",
    CeleryAction.RUN_RISK_CRUISING: "PoC运行任务",
    CeleryAction.DOMAIN_TASK_SYNC_TASK: "域名同步任务",
    CeleryAction.FOFA_TASK: "Fofa查询任务",
    CeleryAction.DOMAIN_EXEC_TASK: "域名监测任务",
    CeleryAction.IP_EXEC_TASK: "IP监测任务",
    CeleryAction.GITHUB_TASK_TASK: "Github泄露任务",
    CeleryAction.GITHUB_TASK_MONITOR: "Github泄露监控任务",
    CeleryAction.ASSET_SITE_UPDATE: "资产站点更新任务",
    CeleryAction.ADD_ASSET_SITE_TASK: "资产站点添加任务",
    CeleryAction.ASSET_WIH_UPDATE: "资产WIH更新任务"
}

# 定义任务提交模型
execute_task_fields = ns.model('ExecuteTask', {
    'task_type': fields.String(required=True, description="任务类型", enum=list(supported_task_types.keys())),
    'data': fields.Raw(required=True, description="任务数据，格式根据任务类型而定")
})

# 定义任务停止模型
revoke_task_fields = ns.model('RevokeTask', {
    'celery_id': fields.String(required=True, description="Celery任务ID"),
    'terminate': fields.Boolean(required=False, default=True, description="是否终止任务进程")
})

# 定义批量任务停止模型
batch_revoke_tasks_fields = ns.model('BatchRevokeTasks', {
    'celery_ids': fields.List(fields.String(required=True, description="Celery任务ID列表")),
    'terminate': fields.Boolean(required=False, default=True, description="是否终止任务进程")
})


@ns.route('/types/')
class TaskTypes(Resource):
    @auth
    def get(self):
        """
        获取所有支持的任务类型
        """
        return build_ret(ErrorMsg.Success, {"task_types": supported_task_types})


@ns.route('/')
class CeleryTaskList(Resource):
    parser = get_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询Celery任务列表
        """
        args = self.parser.parse_args()
        # 从task表和github_task表中查询celery任务
        query = {}
        
        if args.get('celery_id'):
            query['celery_id'] = args.get('celery_id')
        
        if args.get('status'):
            query['status'] = args.get('status')
            
        # 不直接查询task_type，因为在数据库中没有这个字段
        # 可以通过type字段推断
        
        # 分页参数 - 修复类型转换问题
        page = args.get('page')
        page = int(page) if page is not None else 1
        
        size = args.get('size')
        size = int(size) if size is not None else 10
        
        skip = (page - 1) * size
        
        # 从task表查询
        task_data = utils.conn_db('task').find(query).skip(skip).limit(size)
        github_task_data = utils.conn_db('github_task').find(query).skip(skip).limit(size)
        
        # 合并结果
        results = []
        for item in task_data:
            item['_id'] = str(item['_id'])
            if 'type' in item:
                # 根据type字段推断task_type
                task_type = self._infer_task_type(item)
                item['task_type'] = task_type
            results.append(item)
            
        for item in github_task_data:
            item['_id'] = str(item['_id'])
            item['task_type'] = CeleryAction.GITHUB_TASK_TASK
            results.append(item)
            
        # 总数
        total_tasks = utils.conn_db('task').count_documents(query)
        total_github_tasks = utils.conn_db('github_task').count_documents(query)
        total = total_tasks + total_github_tasks
        
        return build_ret(ErrorMsg.Success, {
            "total": total,
            "page": page,
            "size": size,
            "items": results
        })
    
    def _infer_task_type(self, item):
        """根据type和task_tag字段推断task_type"""
        task_type = item.get('type', '')
        task_tag = item.get('task_tag', '')
        
        if task_type == 'domain' and task_tag == 'task':
            return CeleryAction.DOMAIN_TASK
        elif task_type == 'ip' and task_tag == 'task':
            return CeleryAction.IP_TASK
        elif task_type == 'risk_cruising':
            return CeleryAction.RUN_RISK_CRUISING
        elif task_type == 'fofa':
            return CeleryAction.FOFA_TASK
        elif task_type == 'domain' and task_tag == 'monitor':
            return CeleryAction.DOMAIN_EXEC_TASK
        elif task_type == 'ip' and task_tag == 'monitor':
            return CeleryAction.IP_EXEC_TASK
        elif task_type == 'asset_site_update':
            return CeleryAction.ASSET_SITE_UPDATE
        elif task_type == 'asset_site_add':
            return CeleryAction.ADD_ASSET_SITE_TASK
        elif task_type == 'asset_wih_update':
            return CeleryAction.ASSET_WIH_UPDATE
        
        return "unknown"
    
    @auth
    @ns.expect(execute_task_fields)
    def post(self):
        """
        创建并执行Celery任务
        """
        args = self.parse_args(execute_task_fields)
        task_type = args.get('task_type')
        data = args.get('data')
        
        if task_type not in supported_task_types:
            return build_ret(ErrorMsg.Error, {"error": f"不支持的任务类型: {task_type}"})
        
        # 构造任务选项
        task_options = {
            "celery_action": task_type,
            "data": data
        }
        
        try:
            # 根据任务类型决定队列
            if task_type in [CeleryAction.GITHUB_TASK_TASK, CeleryAction.GITHUB_TASK_MONITOR]:
                celery_task = celerytask.github
            else:
                celery_task = celerytask.casm_task
                
            # 提交任务
            result = celery_task.delay(options=task_options)
            celery_id = result.id
            
            # 如果数据中包含_id字段，更新数据库中的celery_id
            if '_id' in data and data.get('_id'):
                task_id = data.get('_id')
                collection = 'github_task' if task_type in [CeleryAction.GITHUB_TASK_TASK, CeleryAction.GITHUB_TASK_MONITOR] else 'task'
                utils.conn_db(collection).update_one(
                    {'_id': ObjectId(task_id)},
                    {'$set': {'celery_id': celery_id}}
                )
            
            return build_ret(ErrorMsg.Success, {
                "celery_id": celery_id,
                "status": "PENDING"
            })
        except Exception as e:
            logger.exception(f"创建任务失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"创建任务失败: {str(e)}"})


@ns.route('/<string:celery_id>/')
class CeleryTaskDetail(Resource):
    @auth
    def get(self, celery_id):
        """
        获取Celery任务状态
        """
        try:
            # 尝试从数据库查找任务信息，而不是依赖Celery的结果后端
            task_info = utils.conn_db('task').find_one({'celery_id': celery_id})
            if not task_info:
                # 可能是Github任务
                task_info = utils.conn_db('github_task').find_one({'celery_id': celery_id})
            
            if not task_info:
                return build_ret(ErrorMsg.CeleryIdNotFound, {"celery_id": celery_id})
                
            # 从数据库获取状态
            status = task_info.get('status', 'UNKNOWN')
            
            # 尝试使用Celery API获取状态，但如果失败则使用数据库中的状态
            try:
                task_result = AsyncResult(celery_id, app=celerytask.celery)
                celery_status = task_result.status
                # 如果能成功获取Celery状态，则使用它
                status = celery_status
            except Exception as e:
                logger.debug(f"无法从Celery获取状态，使用数据库状态: {e}")
                # 继续使用从数据库获取的状态
                pass
            
            result = {
                "celery_id": celery_id,
                "status": status,
            }
            
            if task_info:
                task_info['_id'] = str(task_info['_id'])
                result.update({
                    "task_id": task_info.get('_id') or task_info.get('task_id'),
                    "name": task_info.get('name'),
                    "target": task_info.get('target'),
                    "type": task_info.get('type'),
                    "task_tag": task_info.get('task_tag'),
                    "start_time": task_info.get('start_time'),
                    "end_time": task_info.get('end_time'),
                })
                
            return build_ret(ErrorMsg.Success, result)
        except Exception as e:
            logger.exception(f"获取任务状态失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"获取任务状态失败: {str(e)}"})
    
    @auth
    def delete(self, celery_id):
        """
        撤销/终止Celery任务
        """
        try:
            control = celerytask.celery.control
            control.revoke(celery_id, signal='SIGTERM', terminate=True)
            
            # 更新数据库中的任务状态
            update_data = {"$set": {"status": TaskStatus.STOP, "end_time": utils.curr_date()}}
            utils.conn_db('task').update_one({'celery_id': celery_id}, update_data)
            utils.conn_db('github_task').update_one({'celery_id': celery_id}, update_data)
            
            return build_ret(ErrorMsg.Success, {"celery_id": celery_id, "status": "revoked"})
        except Exception as e:
            logger.exception(f"撤销任务失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"撤销任务失败: {str(e)}"})


@ns.route('/revoke/')
class RevokeCeleryTask(Resource):
    @auth
    @ns.expect(revoke_task_fields)
    def post(self):
        """
        通过POST方法撤销/终止Celery任务
        """
        args = self.parse_args(revoke_task_fields)
        celery_id = args.get('celery_id')
        terminate = args.get('terminate', True)
        
        try:
            control = celerytask.celery.control
            control.revoke(celery_id, signal='SIGTERM' if terminate else None, terminate=terminate)
            
            # 更新数据库中的任务状态
            update_data = {"$set": {"status": TaskStatus.STOP, "end_time": utils.curr_date()}}
            utils.conn_db('task').update_one({'celery_id': celery_id}, update_data)
            utils.conn_db('github_task').update_one({'celery_id': celery_id}, update_data)
            
            return build_ret(ErrorMsg.Success, {"celery_id": celery_id, "status": "revoked"})
        except Exception as e:
            logger.exception(f"撤销任务失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"撤销任务失败: {str(e)}"})


@ns.route('/batch_revoke/')
class BatchRevokeCeleryTask(Resource):
    @auth
    @ns.expect(batch_revoke_tasks_fields)
    def post(self):
        """
        批量撤销/终止Celery任务
        """
        args = self.parse_args(batch_revoke_tasks_fields)
        celery_ids = args.get('celery_ids', [])
        terminate = args.get('terminate', True)
        
        if not celery_ids:
            return build_ret(ErrorMsg.Error, {"error": "celery_ids不能为空"})
            
        try:
            control = celerytask.celery.control
            results = []
            
            for celery_id in celery_ids:
                control.revoke(celery_id, signal='SIGTERM' if terminate else None, terminate=terminate)
                
                # 更新数据库中的任务状态
                update_data = {"$set": {"status": TaskStatus.STOP, "end_time": utils.curr_date()}}
                utils.conn_db('task').update_one({'celery_id': celery_id}, update_data)
                utils.conn_db('github_task').update_one({'celery_id': celery_id}, update_data)
                
                results.append({"celery_id": celery_id, "status": "revoked"})
                
            return build_ret(ErrorMsg.Success, {"results": results})
        except Exception as e:
            logger.exception(f"批量撤销任务失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"批量撤销任务失败: {str(e)}"})


@ns.route('/active/')
class ActiveCeleryTasks(Resource):
    @auth
    def get(self):
        """
        获取活跃的Celery任务列表
        """
        try:
            # 使用inspect获取正在运行的任务
            i = celerytask.celery.control.inspect()
            active_tasks = i.active() or {}
            scheduled_tasks = i.scheduled() or {}
            reserved_tasks = i.reserved() or {}
            
            # 合并所有任务
            all_active_tasks = []
            
            # 处理活跃任务
            for worker, tasks in active_tasks.items():
                for task in tasks:
                    task['worker'] = worker
                    task['state'] = 'active'
                    all_active_tasks.append(task)
                    
            # 处理计划任务
            for worker, tasks in scheduled_tasks.items():
                for task_data in tasks:
                    task = task_data.get('request', {})
                    task['worker'] = worker
                    task['state'] = 'scheduled'
                    task['eta'] = task_data.get('eta')
                    all_active_tasks.append(task)
                    
            # 处理预留任务
            for worker, tasks in reserved_tasks.items():
                for task in tasks:
                    task['worker'] = worker
                    task['state'] = 'reserved'
                    all_active_tasks.append(task)
            
            return build_ret(ErrorMsg.Success, {"active_tasks": all_active_tasks})
        except Exception as e:
            logger.exception(f"获取活跃任务失败: {str(e)}")
            return build_ret(ErrorMsg.Error, {"error": f"获取活跃任务失败: {str(e)}"})