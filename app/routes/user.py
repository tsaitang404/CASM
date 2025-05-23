from flask import request
from flask_restx import fields, Namespace
from app.utils import get_logger
from app import utils
from . import Resource
from app.modules import ErrorMsg

ns = Namespace('user', description="管理员登录认证")

logger = get_logger()



login_fields = ns.model('Login', {
    'username': fields.String(required=True, description="用户名"),
    'password': fields.String(required=True, description="密码"),
})


@ns.route('/login')
class Login(Resource):

    @ns.expect(login_fields)
    def post(self):
        """
        用户登录
        """
        args = self.parse_args(login_fields)


        return build_data(utils.user_login(**args))


@ns.route('/info')
class UserInfo(Resource):
    def get(self):
        """
        验证用户 token 有效性并返回用户信息
        """
        user_info = utils.user_login_header()
        if user_info:
            return build_data(user_info)
        else:
            return build_data(None)


@ns.route('/logout')
class Logout(Resource):

    def get(self):
        """
        用户退出
        """
        token = request.headers.get("Token")
        utils.user_logout(token)

        return build_data({})


change_pass_fields = ns.model('ChangePass', {
    'old_password': fields.String(required=True, description="旧密码"),
    'new_password': fields.String(required=True, description="新密码"),
    'check_password': fields.String(required=True, description="确认密码"),
})


@ns.route('/change_pass')
class ChangePass(Resource):
    @ns.expect(change_pass_fields)
    def post(self):
        """
        密码修改
        """
        args = self.parse_args(change_pass_fields)
        ret = ErrorMsg.Success.copy()
        # 获取当前登录的用户名
        user_info = utils.user_login_header()
        if not user_info:
            ret["code"] = 401
            ret["message"] = "用户未登录"
            return ret
            
        username = user_info.get("username")
        token = user_info.get("token")

        if args["new_password"] != args["check_password"]:
            ret["code"] = 301
            ret["message"] = "新密码和确定密码不一致"
            return ret

        if not args["new_password"]:
            ret["code"] = 302
            ret["message"] = "新密码不能为空"
            return ret

        # 使用用户名和旧密码验证用户身份
        if utils.change_pass(username, args["old_password"], args["new_password"]):
            # 修改成功后注销用户
            utils.user_logout(token)
        else:
            ret["message"] = "旧密码错误"
            ret["code"] = 303

        return ret


def build_data(data):
    ret = ErrorMsg.Success.copy()
    if data:
        ret["data"] = data
    else:
        ret["code"] = 401
    return ret


