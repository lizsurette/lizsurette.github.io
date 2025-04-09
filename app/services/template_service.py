from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class TemplateService:
    """Service for rendering templates."""
    
    def __init__(self, config_service):
        """Initialize the template service.
        
        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.env = Environment(
            loader=FileSystemLoader('app/templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['date'] = self._date_filter
        self.env.filters['excerpt'] = self._excerpt_filter
        
    def render(self, template_name: str, **context) -> str:
        """Render a template.
        
        Args:
            template_name: Name of template file
            **context: Template context variables
            
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
        
    def render_string(self, template_string: str, **context) -> str:
        """Render a template string.
        
        Args:
            template_string: Template string
            **context: Template context variables
            
        Returns:
            Rendered HTML string
        """
        template = self.env.from_string(template_string)
        return template.render(**context)
        
    def _date_filter(self, value: str, format: str = None) -> str:
        """Format date string.
        
        Args:
            value: Date string
            format: Date format string
            
        Returns:
            Formatted date string
        """
        if not value:
            return ''
            
        from datetime import datetime
        date_format = format or self.config.date_format
        
        try:
            date = datetime.strptime(value, '%Y-%m-%d')
            return date.strftime(date_format)
        except ValueError:
            return value
            
    def _excerpt_filter(self, content: str, length: int = 200) -> str:
        """Get excerpt from content.
        
        Args:
            content: HTML content
            length: Maximum length
            
        Returns:
            Excerpt string
        """
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', content)
        
        # Get first paragraph
        paragraphs = text.split('\n\n')
        if not paragraphs:
            return ''
            
        excerpt = paragraphs[0].strip()
        
        # Truncate if needed
        if len(excerpt) > length:
            excerpt = excerpt[:length] + '...'
            
        return excerpt
        
    def get_template(self, name: str):
        """Get a template.
        
        Args:
            name: Template name
            
        Returns:
            Template object
        """
        return self.env.get_template(name)
        
    def add_filter(self, name: str, filter_func):
        """Add a custom filter.
        
        Args:
            name: Filter name
            filter_func: Filter function
        """
        self.env.filters[name] = filter_func
        
    def add_global(self, name: str, value: Any):
        """Add a global variable.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.env.globals[name] = value 