from flask import Flask
from flask_restx import Api

from app import routes
from app.utils import casm_update

casm_app = Flask(__name__)
casm_app.config['BUNDLE_ERRORS'] = True

authorizations = {
    "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Token"
    }
}

api = Api(casm_app, prefix="/api", doc="/api/doc", title='CASM backend API', authorizations=authorizations,
          description='CASM( Cyber Asset Survey & Mapping )网络空间测绘系统', security="ApiKeyAuth", version="2.6.2")

api.add_namespace(routes.task_ns)
api.add_namespace(routes.site_ns)
api.add_namespace(routes.domain_ns)
api.add_namespace(routes.ip_ns)
api.add_namespace(routes.url_ns)
api.add_namespace(routes.user_ns)
api.add_namespace(routes.image_ns)
api.add_namespace(routes.cert_ns)
api.add_namespace(routes.service_ns)
api.add_namespace(routes.fileleak_ns)
api.add_namespace(routes.export_ns)
api.add_namespace(routes.asset_scope_ns)
api.add_namespace(routes.asset_domain_ns)
api.add_namespace(routes.asset_ip_ns)
api.add_namespace(routes.asset_site_ns)
api.add_namespace(routes.scheduler_ns)
api.add_namespace(routes.poc_ns)
api.add_namespace(routes.vuln_ns)
api.add_namespace(routes.batch_export_ns)
api.add_namespace(routes.policy_ns)
api.add_namespace(routes.npoc_service_ns)
api.add_namespace(routes.task_fofa_ns)
api.add_namespace(routes.console_ns)
api.add_namespace(routes.cip_ns)
api.add_namespace(routes.fingerprint_ns)
api.add_namespace(routes.stat_finger_ns)
api.add_namespace(routes.github_task_ns)
api.add_namespace(routes.github_result_ns)
api.add_namespace(routes.github_scheduler_ns)
api.add_namespace(routes.github_monitor_result_ns)
api.add_namespace(routes.task_schedule_ns)
api.add_namespace(routes.nuclei_result_ns)
api.add_namespace(routes.wih_ns)
api.add_namespace(routes.asset_wih_ns)


casm_update()

if __name__ == '__main__':
    casm_app.run(debug=True, port=5018, host="0.0.0.0")
