from os import environ

class BaseConfig:
    """Sets the base configuration variables"""
    SECRET_KEY = environ.get('SECRET_KEY')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Sets configuration variables for Development.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_SQL_DATABASE_URI')


class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_SQL_DATABASE_URI')


class StagingConfig(BaseConfig):
    """Configurations for Staging.
    """
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Configurations for Production.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_SQL_DATABASE_URI')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
