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
    STATIC_FOLDER = os.path.join(APP_DIR, 'static')
    STATIC_URL_PATH = '/static'
    
    # Logging configuration
    LOG_DIR = os.path.join(APP_DIR, 'logs')
    LOG_FILE = 'lizsurette.log'
    LOG_LEVEL = 'INFO'
    
    # Site generation configuration
    SITE_DIR = os.path.join(APP_DIR, '_site')
    
    # Flask configuration
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True
    
    # Frozen-Flask configuration
    FREEZER_DESTINATION = os.path.join(APP_DIR, '_site')
    FREEZER_RELATIVE_URLS = False
    FREEZER_REMOVE_EXTRA_FILES = True
    FREEZER_DEFAULT_MIMETYPE = 'text/html'
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True
    
    @staticmethod
    def init_app(app):
        """Initialize application."""
        # Create necessary directories
        os.makedirs(os.path.join(app.config['APP_DIR'], '_site'), exist_ok=True)
        os.makedirs(os.path.join(app.config['APP_DIR'], 'logs'), exist_ok=True)

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