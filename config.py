import os


class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='b\x12\xd2D\xdb\xe9\xd9\x01\xe2,\xfd\xb5\xd6\xa7~\x06\xc7\xe6\xe9\xc1d\xff_\x8e\xa2\x81F\x07\xdc=>\x03\n')


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True