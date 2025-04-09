import os

class Config:
    """Base configuration."""
    # Get the absolute path to the app directory
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Flask-FlatPages configuration
    FLATPAGES_ROOT = os.path.join(APP_DIR, 'app', 'posts')
    FLATPAGES_EXTENSION = '.markdown'
    FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'fenced_code', 'tables']
    FLATPAGES_EXTENSION_CONFIGS = {
        'codehilite': {
            'css_class': 'highlight',
            'linenums': True
        }
    }
    
    # Static files configuration
    STATIC_FOLDER = os.path.join(APP_DIR, 'app', 'static')
    STATIC_URL_PATH = '/static'
    
    # Logging configuration
    LOG_DIR = os.path.join(APP_DIR, 'logs')
    LOG_FILE = 'lizsurette.log'
    LOG_LEVEL = 'INFO'
    
    # Site generation configuration
    SITE_DIR = os.path.join(APP_DIR, '_site')
    
    @staticmethod
    def init_app(app):
        """Initialize application."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    LOG_LEVEL = 'DEBUG'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 