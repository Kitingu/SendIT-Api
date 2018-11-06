import os
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True #Cross-Site Request Forgery
    SECRET = os.environ.get('JWT_SECRET_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {"development": DevelopmentConfig,
              'testing': TestingConfig,
              'staging': StagingConfig,
              'production': ProductionConfig
              }
