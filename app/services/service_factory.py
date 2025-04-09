from typing import Dict, Type, Any
from .config_service import ConfigService
from .markdown_service import MarkdownService
from .template_service import TemplateService
from .static_service import StaticService
from .logging_service import LoggingService
from .post_service import PostService

class ServiceFactory:
    """Factory for creating and managing service instances."""
    
    _instances: Dict[Type, Any] = {}
    
    @classmethod
    def get_config_service(cls) -> ConfigService:
        """Get or create ConfigService instance.
        
        Returns:
            ConfigService instance
        """
        if ConfigService not in cls._instances:
            cls._instances[ConfigService] = ConfigService()
        return cls._instances[ConfigService]
        
    @classmethod
    def get_markdown_service(cls) -> MarkdownService:
        """Get or create MarkdownService instance.
        
        Returns:
            MarkdownService instance
        """
        if MarkdownService not in cls._instances:
            config = cls.get_config_service()
            cls._instances[MarkdownService] = MarkdownService(config)
        return cls._instances[MarkdownService]
        
    @classmethod
    def get_template_service(cls) -> TemplateService:
        """Get or create TemplateService instance.
        
        Returns:
            TemplateService instance
        """
        if TemplateService not in cls._instances:
            config = cls.get_config_service()
            cls._instances[TemplateService] = TemplateService(config)
        return cls._instances[TemplateService]
        
    @classmethod
    def get_static_service(cls) -> StaticService:
        """Get or create StaticService instance.
        
        Returns:
            StaticService instance
        """
        if StaticService not in cls._instances:
            config = cls.get_config_service()
            cls._instances[StaticService] = StaticService(config)
        return cls._instances[StaticService]
        
    @classmethod
    def get_logging_service(cls) -> LoggingService:
        """Get or create LoggingService instance.
        
        Returns:
            LoggingService instance
        """
        if LoggingService not in cls._instances:
            config = cls.get_config_service()
            cls._instances[LoggingService] = LoggingService(config)
        return cls._instances[LoggingService]
        
    @classmethod
    def get_post_service(cls) -> PostService:
        """Get or create PostService instance.
        
        Returns:
            PostService instance
        """
        if PostService not in cls._instances:
            config = cls.get_config_service()
            markdown = cls.get_markdown_service()
            cls._instances[PostService] = PostService(config, markdown)
        return cls._instances[PostService]
        
    @classmethod
    def reset(cls):
        """Reset all service instances."""
        cls._instances.clear()
        
    @classmethod
    def get_service(cls, service_class: Type) -> Any:
        """Get or create a service instance.
        
        Args:
            service_class: Service class
            
        Returns:
            Service instance
            
        Raises:
            ValueError: If service class is not supported
        """
        if service_class == ConfigService:
            return cls.get_config_service()
        elif service_class == MarkdownService:
            return cls.get_markdown_service()
        elif service_class == TemplateService:
            return cls.get_template_service()
        elif service_class == StaticService:
            return cls.get_static_service()
        elif service_class == LoggingService:
            return cls.get_logging_service()
        elif service_class == PostService:
            return cls.get_post_service()
        else:
            raise ValueError(f"Unsupported service class: {service_class}")
            
    @classmethod
    def register_service(cls, service_class: Type, instance: Any):
        """Register a service instance.
        
        Args:
            service_class: Service class
            instance: Service instance
        """
        cls._instances[service_class] = instance 