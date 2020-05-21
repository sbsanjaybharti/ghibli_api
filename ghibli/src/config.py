import os
from flask import Flask
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Security secret key
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

    """
    Connection variable
    """
    DOMAIN = os.getenv('DOMAIN')
    GHIBLI_API = os.getenv('GHIBLI_API')
    CACHE_TYPE = "simple"

class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 10

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    CACHE_DEFAULT_TIMEOUT = 0
    GHIBLI_API = os.getenv('GHIBLI_API')

class ProductionConfig(Config):
    DEBUG = False
    CACHE_DEFAULT_TIMEOUT = 60

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    config = {
        "DEBUG": True,  # some Flask specific configs
        "CACHE_TYPE": app.config['CACHE_TYPE'],  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": app.config['CACHE_DEFAULT_TIMEOUT']
    }
    app.config.from_mapping(config)
    return app