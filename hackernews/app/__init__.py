import os

from flask import Flask
from flask_rq import RQ

from app.api_v1 import blueprint as api_v1
from app.database import db
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)

    RQ(app)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Register api blueprints
    app.register_blueprint(api_v1)

    return app
