from flask_restx import Namespace, fields

api = Namespace('posts', description='Post related operations')

post = api.model('Post', {
    'id': fields.String(description='Local post i'),
    'title': fields.String(description='The post title'),
    'url': fields.String(description='The post title'),
    'created': fields.DateTime(description='Created'),
})
