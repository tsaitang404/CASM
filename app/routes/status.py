from flask_restx import Resource, Api, reqparse, fields, Namespace
from app.utils import get_logger, auth
from . import Resource
from app import utils
from app.utils.conn import ConnMongo
from app.config import Config
import pika
import subprocess
import os

ns = Namespace('status', description="系统状态信息")

logger = get_logger()

@ns.route('/')
class Status(Resource):
    @auth
    def get(self):
        """
        获取系统组件状态
        """
        status = {
            "mongodb": self._check_mongodb(),
            "rabbitmq": self._check_rabbitmq(),
            "scheduler": self._check_scheduler(),
            "workers": self._check_workers(),
            "assets": self._get_assets_count()
        }
        
        return utils.build_ret("Success", status)

    def _check_mongodb(self):
        """检查MongoDB连接状态"""
        try:
            conn = ConnMongo().conn
            # 执行ping命令检查连接
            conn.admin.command('ping')
            return {
                "status": "running",
                "message": "MongoDB连接正常"
            }
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            return {
                "status": "error",
                "message": f"MongoDB连接失败: {str(e)}"
            }

    def _check_rabbitmq(self):
        """检查RabbitMQ连接状态"""
        try:
            # 从配置中获取RabbitMQ连接URL
            rabbitmq_url = Config.CELERY_BROKER_URL

            # 尝试连接RabbitMQ
            parameters = pika.URLParameters(rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            connection.close()
            return {
                "status": "running",
                "message": "RabbitMQ连接正常"
            }
        except Exception as e:
            logger.error(f"RabbitMQ连接失败: {str(e)}")
            return {
                "status": "error",
                "message": f"RabbitMQ连接失败: {str(e)}"
            }
        except Exception as e:
            logger.error(f"RabbitMQ连接失败: {str(e)}")
            return {
                "status": "error",
                "message": f"RabbitMQ连接失败: {str(e)}"
            }

    def _check_workers(self):
        """检查Worker服务状态"""
        try:
            conn = ConnMongo().conn
            
            # 获取所有worker节点
            workers = list(conn.casm.workers.find({}, {'_id': 0}))
            active_workers = [w for w in workers if w['status'] == 'running']
            
            # 获取Celery Worker状态
            worker_stats = {
                "total": len(workers),
                "active": len(active_workers),
                "nodes": []
            }
            
            for worker in workers:
                node_info = {
                    "name": worker['name'],
                    "status": worker['status'],
                    "tasks_processed": worker.get('tasks_processed', 0),
                    "uptime": worker.get('uptime', '0h')
                }
                if worker['status'] != 'running':
                    node_info['error'] = worker.get('error', 'Unknown error')
                    
                worker_stats['nodes'].append(node_info)
                
            return worker_stats
            
        except Exception as e:
            logger.error(f"获取Worker状态失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取Worker状态失败: {str(e)}"
            }

    def _check_scheduler(self):
        """检查调度器状态"""
        try:
            conn = ConnMongo().conn
            scheduler = conn.casm.scheduler.find_one({}, {'_id': 0})
            
            if not scheduler:
                return {
                    "status": "stopped",
                    "message": "调度器未运行"
                }
                
            return {
                "status": scheduler['status'],
                "uptime": scheduler.get('uptime', '0h'),
                "tasks_total": scheduler.get('tasks_total', 0),
                "tasks_active": scheduler.get('tasks_active', 0)
            }
            
        except Exception as e:
            logger.error(f"获取调度器状态失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取调度器状态失败: {str(e)}"
            }

    def _check_service_status(self, service_name):
        """检查系统服务状态"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            status = result.stdout.strip()
            
            if status == 'active':
                return {
                    "status": "running",
                    "message": f"{service_name}服务运行正常"
                }
            else:
                return {
                    "status": "stopped",
                    "message": f"{service_name}服务未运行"
                }
        except Exception as e:
            logger.error(f"检查{service_name}服务状态失败: {str(e)}")
            return {
                "status": "error", 
                "message": f"检查服务状态失败: {str(e)}"
            }

    def _get_assets_count(self):
        """获取各类资产数量统计"""
        try:
            conn = ConnMongo().conn
            return {
                "domains": conn.casm.domain.count_documents({}),
                "ips": conn.casm.ip.count_documents({}),
                "sites": conn.casm.site.count_documents({}),
                "services": conn.casm.service.count_documents({}),
                "vulnerabilities": conn.casm.vuln.count_documents({}),
                "certificates": conn.casm.cert.count_documents({})
            }
        except Exception as e:
            logger.error(f"获取资产统计失败: {str(e)}")
            return {
                "error": f"获取资产统计失败: {str(e)}"
            }