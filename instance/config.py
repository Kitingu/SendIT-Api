import os
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True #Cross-Site Request Forgery
    SECRET_KEY = os.getenv('SECRET_KEY') or "asdfg"
    DATABASE_URI=os.getenv('DATABASE_URI')
    PROPAGATE_EXCEPTIONS=True


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv('DATABASE_URI')


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URI = os.getenv('TESTDB_URI')


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {'development': DevelopmentConfig,
              'testing': TestingConfig,
              'staging': StagingConfig,
              'production': ProductionConfig
              }
