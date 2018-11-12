class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../src/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    IMAGE_DOMAIN = 'http://localhost:5001'


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True
