from flask import Blueprint
from flask_restx import Api

from .api.endpoints.posts import api as posts_endpoint

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint, title='Hacker News Grabber API',
          version='1.0',
          description='Get news from https://news.ycombinator.com/',)

api.add_namespace(posts_endpoint)
