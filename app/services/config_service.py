import os
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class AppConfig:
    """Application configuration settings."""
    # Directory paths
    posts_dir: str
    static_dir: str
    templates_dir: str
    
    # Site settings
    site_title: str
    site_description: str
    site_url: str
    
    # Markdown settings
    markdown_extensions: list
    markdown_config: dict
    
    # Development settings
    debug: bool
    host: str
    port: int

class ConfigService:
    """Service for managing application configuration."""
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize the configuration service.
        
        Args:
            config_path: Path to config file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Dictionary containing configuration
        """
        if not self.config_path.exists():
            return self._get_default_config()
            
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Dictionary containing default configuration
        """
        return {
            'site': {
                'title': 'My Blog',
                'description': 'A blog about things',
                'author': 'Author Name',
                'url': 'http://localhost:5000'
            },
            'posts': {
                'dir': 'app/posts',
                'per_page': 10,
                'date_format': '%Y-%m-%d'
            },
            'markdown': {
                'extensions': [
                    'markdown.extensions.fenced_code',
                    'markdown.extensions.tables',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.nl2br'
                ],
                'extension_configs': {
                    'markdown.extensions.codehilite': {
                        'css_class': 'highlight'
                    }
                }
            },
            'static': {
                'dir': 'app/static',
                'cache_timeout': 3600
            }
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        
    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    @property
    def posts_dir(self) -> str:
        """Get posts directory path."""
        return self.get('posts.dir', 'app/posts')
        
    @property
    def static_dir(self) -> str:
        """Get static files directory path."""
        return self.get('static.dir', 'app/static')
        
    @property
    def site_title(self) -> str:
        """Get site title."""
        return self.get('site.title', 'My Blog')
        
    @property
    def site_description(self) -> str:
        """Get site description."""
        return self.get('site.description', 'A blog about things')
        
    @property
    def site_author(self) -> str:
        """Get site author."""
        return self.get('site.author', 'Author Name')
        
    @property
    def site_url(self) -> str:
        """Get site URL."""
        return self.get('site.url', 'http://localhost:5000')
        
    @property
    def posts_per_page(self) -> int:
        """Get number of posts per page."""
        return self.get('posts.per_page', 10)
        
    @property
    def date_format(self) -> str:
        """Get date format string."""
        return self.get('posts.date_format', '%Y-%m-%d')
        
    @property
    def markdown_extensions(self) -> list:
        """Get markdown extensions."""
        return self.get('markdown.extensions', [])
        
    @property
    def markdown_extension_configs(self) -> dict:
        """Get markdown extension configurations."""
        return self.get('markdown.extension_configs', {})
        
    @property
    def static_cache_timeout(self) -> int:
        """Get static files cache timeout."""
        return self.get('static.cache_timeout', 3600)
    
    def load_from_env(self):
        """Load configuration from environment variables."""
        # Directory paths
        if 'POSTS_DIR' in os.environ:
            self.config['posts']['dir'] = os.environ['POSTS_DIR']
        if 'STATIC_DIR' in os.environ:
            self.config['static']['dir'] = os.environ['STATIC_DIR']
        if 'TEMPLATES_DIR' in os.environ:
            self.config['templates_dir'] = os.environ['TEMPLATES_DIR']
            
        # Site settings
        if 'SITE_TITLE' in os.environ:
            self.config['site']['title'] = os.environ['SITE_TITLE']
        if 'SITE_DESCRIPTION' in os.environ:
            self.config['site']['description'] = os.environ['SITE_DESCRIPTION']
        if 'SITE_URL' in os.environ:
            self.config['site']['url'] = os.environ['SITE_URL']
            
        # Development settings
        if 'DEBUG' in os.environ:
            self.config['debug'] = os.environ['DEBUG'].lower() == 'true'
        if 'HOST' in os.environ:
            self.config['host'] = os.environ['HOST']
        if 'PORT' in os.environ:
            self.config['port'] = int(os.environ['PORT'])
    
    def get_config(self) -> AppConfig:
        """Get the current configuration.
        
        Returns:
            AppConfig object containing all settings
        """
        return AppConfig(
            # Directory paths
            posts_dir=str(self.posts_dir),
            static_dir=str(self.static_dir),
            templates_dir=str(self.templates_dir),
            
            # Site settings
            site_title=self.site_title,
            site_description=self.site_description,
            site_url=self.site_url,
            
            # Markdown settings
            markdown_extensions=self.markdown_extensions,
            markdown_config=self.markdown_extension_configs,
            
            # Development settings
            debug=self.config['debug'],
            host=self.config['host'],
            port=self.config['port']
        )
    
    def update_config(self, **kwargs):
        """Update configuration settings.
        
        Args:
            **kwargs: Key-value pairs of settings to update
        """
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            else:
                raise ValueError(f"Invalid configuration key: {key}") 