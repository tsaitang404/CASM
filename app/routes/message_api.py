from flask_restx import Resource, Namespace, reqparse, fields
from app.utils import get_logger, auth, build_ret
from app.utils.conn import ConnMongo
from datetime import datetime

ns = Namespace('message', description="消息系统")
logger = get_logger()

message_model = ns.model('Message', {
    '_id': fields.String(readonly=True),
    'content': fields.String(required=True, description='消息内容'),
    'type': fields.String(description='消息类型'),
    'create_time': fields.DateTime(description='创建时间'),
    'read': fields.Boolean(description='是否已读', default=False)
})

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('size', type=int, default=10)
parser.add_argument('read', type=int, choices=[0, 1], required=False, help='0未读,1已读,不传为全部')

@ns.route('/')
class MessageList(Resource):
    @auth
    @ns.expect(parser)
    def get(self):
        """查询消息列表"""
        args = parser.parse_args()
        page = args['page']
        size = args['size']
        query = {}
        if args.get('read') is not None:
            query['read'] = bool(args['read'])
        db = ConnMongo().conn.casm.message
        total = db.count_documents(query)
        items = list(db.find(query).sort('create_time', -1).skip((page-1)*size).limit(size))
        for x in items:
            x['_id'] = str(x['_id'])
        return build_ret("Success", {
            "total": total,
            "page": page,
            "size": size,
            "items": items
        })

    @auth
    @ns.expect(message_model)
    def post(self):
        """推送新消息"""
        data = ns.payload
        item = {
            "content": data.get("content"),
            "type": data.get("type", ""),
            "create_time": datetime.utcnow(),
            "read": False
        }
        db = ConnMongo().conn.casm.message
        db.insert_one(item)
        return build_ret("Success", {"inserted": True})

@ns.route('/read/')
class MessageRead(Resource):
    @auth
    def post(self):
        """批量/单条标记为已读"""
        data = ns.payload
        ids = data.get("_id")
        if not ids:
            return build_ret("InvalidParameter", {"error": "_id不能为空"})
        if not isinstance(ids, list):
            ids = [ids]
        db = ConnMongo().conn.casm.message
        from bson import ObjectId
        result = db.update_many({"_id": {"$in": [ObjectId(i) for i in ids]}}, {"$set": {"read": True}})
        return build_ret("Success", {"updated": result.modified_count})
