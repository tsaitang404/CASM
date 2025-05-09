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
        workers = {
            "casm-worker": self._check_service_status("casm-worker"),
            "casm-worker-github": self._check_service_status("casm-worker-github"),
            "casm-scheduler": self._check_service_status("casm-scheduler")
        }
        return workers

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