import os
import json
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__name__)) # Sets application's base directory


def get_env(variable):
    '''
    A custom function that provides
    alternative lookup for enviroment variables
    '''

    try:
        return os.environ[variable]
    except KeyError:

        def get_from_file(variable):
            with open("configs.json", "r") as f:
                env_file = json.load(f)
            return env_file[variable]

        return get_from_file(variable)


class BaseConfig:
    '''
    Base configurations common to all
    the development environments
    '''

    SECRET_KEY = get_env("SECRET_KEY")
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    '''
    Convigurations for local environment
    '''

    DEBUG = True
    MONGODB_SETTINGS = {
        "db": get_env("DEV_DB"),
        "host": get_env("URI")
    }
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=20)
    JWT_CREATE_TOKEN_EXPIRES = timedelta(hours=20)


class ProductionConfig(BaseConfig):
    '''
    Configurations for production environment
    '''

    DEBUG = False
    MONGODB_SETTINGS = {
        "db": get_env("PROD_DB"),
        "host": get_env("URI")
    }
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=20)
    JWT_CREATE_TOKEN_EXPIRES = timedelta(hours=20)


class TestingConfig(BaseConfig):
    '''
    Configurations for writing tests
    '''

    TESTING = True
    MONGODB_SETTINGS = {
        "db": get_env("TEST_DB"),
        "host": get_env("URI")
    }
    JWT_ACCESS_TOKEN_EXPIRES = False


load_configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestingConfig,
}