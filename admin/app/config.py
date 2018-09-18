class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:111111@localhost/LUMP' #'sqlite:///../../src/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True
