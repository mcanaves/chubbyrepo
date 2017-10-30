import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'SUPER SECRET KEY'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'chubby-cache'
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Configurations for Production."""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
