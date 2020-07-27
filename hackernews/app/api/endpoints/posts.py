# from redis import Redis
from sqlalchemy import desc
from flask_restx import Namespace, Resource, fields

from app.api.parsers import request_parser
from app.database.models import Post

api = Namespace('posts', description='Post related operations')

post = api.model('Post', {
    'id': fields.String(description='Local post id'),
    'title': fields.String(description='The post title'),
    'url': fields.String(description='The post title'),
    'created': fields.DateTime(description='Created'),
    'created_hn': fields.DateTime(description='Created HN'),
})


@api.route('/')
class PostList(Resource):
    @api.marshal_list_with(post)
    @api.param('order', 'title | created | id | url')
    @api.param('dir', 'asc | desc')
    @api.param('limit')
    @api.param('offset')
    def get(self):
        """List all post"""
        args = request_parser()

        query = Post.query

        ordering = args.get('order')

        if args['dir'] == 'desc':
            ordering = desc(ordering)

        query = query.order_by(ordering)
        query = query.limit(args['limit'])
        query = query.offset(args['offset'])
        query = query.all()

        return query, 200
