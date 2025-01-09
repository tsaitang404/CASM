from flask_restx import Resource, Api, reqparse, fields, Namespace
from app.utils import get_logger, auth
from . import base_query_fields, CASMResource, get_casm_parser

ns = Namespace('url', description="URL信息")

logger = get_logger()

base_search_fields = {
    'fld': fields.String(required=False, description="IP"),
    'site': fields.String(description="域名"),
    'url': fields.String(required=False, description="URL"),
    'content_length': fields.Integer(description="body 长度"),
    'status_code': fields.Integer(description="状态码"),
    'title': fields.String(description="标题"),
    'source': fields.String(description="来源"),
    "task_id": fields.String(description="任务ID")
}

base_search_fields.update(base_query_fields)


@ns.route('/')
class CASMUrl(CASMResource):
    parser = get_casm_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        URL信息查询
        """
        args = self.parser.parse_args()
        data = self.build_data(args=args, collection='url')

        return data


@ns.route('/export/')
class CASMUrlExport(CASMResource):
    parser = get_casm_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        URL 导出
        """
        args = self.parser.parse_args()
        response = self.send_export_file(args=args, _type="url")

        return response
