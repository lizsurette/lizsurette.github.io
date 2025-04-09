from typing import Dict, Any, Tuple
import markdown
from pathlib import Path
import yaml
import re

class MarkdownService:
    """Service for processing markdown content."""
    
    def __init__(self, config_service):
        """Initialize the markdown service.
        
        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.md = markdown.Markdown(
            extensions=self.config.markdown_extensions,
            extension_configs=self.config.markdown_extension_configs
        )
        
    def process_file(self, file_path: str) -> Tuple[Dict[str, Any], str]:
        """Process a markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Tuple of (metadata, content)
        """
        with open(file_path, 'r') as f:
            content = f.read()
            
        return self.process_content(content)
        
    def process_content(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Process markdown content.
        
        Args:
            content: Markdown content string
            
        Returns:
            Tuple of (metadata, content)
        """
        metadata, content = self._extract_front_matter(content)
        html_content = self._render_markdown(content)
        
        return metadata, html_content
        
    def _extract_front_matter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML front matter from content.
        
        Args:
            content: Markdown content string
            
        Returns:
            Tuple of (metadata, content)
        """
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            return {}, content
            
        try:
            metadata = yaml.safe_load(match.group(1))
            content = content[match.end():]
            return metadata or {}, content
        except yaml.YAMLError as e:
            print(f"Error parsing front matter: {e}")
            return {}, content
            
    def _render_markdown(self, content: str) -> str:
        """Render markdown content to HTML.
        
        Args:
            content: Markdown content string
            
        Returns:
            HTML content string
        """
        self.md.reset()
        return self.md.convert(content)
        
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get metadata from markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Dictionary of metadata
        """
        with open(file_path, 'r') as f:
            content = f.read()
            
        metadata, _ = self._extract_front_matter(content)
        return metadata
        
    def get_content(self, file_path: str) -> str:
        """Get rendered HTML content from markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            HTML content string
        """
        with open(file_path, 'r') as f:
            content = f.read()
            
        _, content = self._extract_front_matter(content)
        return self._render_markdown(content)
        
    def get_excerpt(self, content: str, length: int = 200) -> str:
        """Get excerpt from markdown content.
        
        Args:
            content: Markdown content string
            length: Maximum length of excerpt
            
        Returns:
            Excerpt string
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', content)
        
        # Remove markdown syntax
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'[*_~`]', '', text)
        
        # Get first paragraph
        paragraphs = text.split('\n\n')
        if not paragraphs:
            return ''
            
        excerpt = paragraphs[0].strip()
        
        # Truncate if needed
        if len(excerpt) > length:
            excerpt = excerpt[:length] + '...'
            
        return excerpt 