#!/usr/bin/env python3
"""
Import packages
"""
import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Common for all environment
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
    """
    Use for development environment
    """
    DEBUG = True
    CACHE_SERVER = os.getenv('CACHE_SERVER')
    CACHE_PORT = os.getenv('CACHE_PORT')
    """Cache key"""
    LAST_MODI_KEY = 'last_modification_key'
    LIST_FILM_KEY = 'movie_list_key'
    LIST_DATA_KEY = 'movie_data_key'


class TestingConfig(Config):
    """
    Use for testing environment
    """
    DEBUG = True
    TESTING = True
    CACHE_SERVER = os.getenv('CACHE_SERVER')
    CACHE_PORT = os.getenv('CACHE_PORT')
    GHIBLI_API = os.getenv('GHIBLI_API')
    """Cache key"""
    LAST_MODI_KEY = 'test_last_modification_key'
    LIST_FILM_KEY = 'test_movie_list_key'
    LIST_DATA_KEY = 'test_movie_data_key'


class ProductionConfig(Config):
    """
    Use for production environment
    """
    DEBUG = False
    CACHE_DEFAULT_TIMEOUT = 60


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY


def create_app(config_name):
    """
    Use to create app and setting environment
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    config = {
        "DEBUG": True,  # some Flask specific configs
        # "CACHE_TYPE": app.config['CACHE_TYPE'],  # Flask-Caching related configs
        # "CACHE_DEFAULT_TIMEOUT": app.config['CACHE_DEFAULT_TIMEOUT']
    }
    app.config.from_mapping(config)
    return app
