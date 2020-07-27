import os
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    REDIS_URL = os.getenv('REDIS_URL', 'http://localhost:6379')

    urllib.parse.uses_netloc.append('redis')
    url = urllib.parse.urlparse(REDIS_URL)

    RQ_DEFAULT_HOST = url.hostname
    RQ_DEFAULT_PORT = url.port
    RQ_DEFAULT_PASSWORD = url.password
    RQ_DEFAULT_DB = 0

    PAGINATION_DEFAULT_LIMIT = int(os.getenv('PAGINATION_DEFAULT_LIMIT', 10))
    PAGINATION_DEFAULT_OFFSET = int(os.getenv('PAGINATION_DEFAULT_OFFSET', 0))
    PAGINATION_DEFAULT_ORDER = os.getenv('PAGINATION_DEFAULT_ORDER', 'created')
    PAGINATION_DEFAULT_ORDER_DIRECTION = os.getenv(
        'PAGINATION_DEFAULT_ORDER_DIRECTION', 'desc')
    PAGINATION_MAX_LIMIT = int(os.getenv('PAGINATION_MAX_LIMIT', 100))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL', 'sqlite:///' + os.path.join(
            basedir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///' + os.path.join(
            basedir, 'data-test.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + os.path.join(
            basedir, 'data.sqlite'))
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
