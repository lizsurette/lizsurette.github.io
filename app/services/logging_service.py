import logging
from typing import Optional
from pathlib import Path
import sys
from datetime import datetime

class LoggingService:
    """Service for handling application logging."""
    
    def __init__(self, config_service):
        """Initialize the logging service.
        
        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up the application logger.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger('app')
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Add formatters to handlers
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def debug(self, message: str, *args, **kwargs):
        """Log debug message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.debug(message, *args, **kwargs)
        
    def info(self, message: str, *args, **kwargs):
        """Log info message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.info(message, *args, **kwargs)
        
    def warning(self, message: str, *args, **kwargs):
        """Log warning message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.warning(message, *args, **kwargs)
        
    def error(self, message: str, *args, **kwargs):
        """Log error message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.error(message, *args, **kwargs)
        
    def critical(self, message: str, *args, **kwargs):
        """Log critical message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.critical(message, *args, **kwargs)
        
    def exception(self, message: str, *args, **kwargs):
        """Log exception message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.exception(message, *args, **kwargs)
        
    def set_level(self, level: int):
        """Set logging level.
        
        Args:
            level: Logging level
        """
        self.logger.setLevel(level)
        
    def add_handler(self, handler: logging.Handler):
        """Add a handler to the logger.
        
        Args:
            handler: Logging handler
        """
        self.logger.addHandler(handler)
        
    def remove_handler(self, handler: logging.Handler):
        """Remove a handler from the logger.
        
        Args:
            handler: Logging handler
        """
        self.logger.removeHandler(handler)
        
    def get_logger(self) -> logging.Logger:
        """Get the logger instance.
        
        Returns:
            Logger instance
        """
        return self.logger 