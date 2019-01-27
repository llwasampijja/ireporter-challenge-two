import os

base_directory = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True

runtime_mode = "development"
environment_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
