class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///dev_db.mysql'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///prod_db.mysql'
