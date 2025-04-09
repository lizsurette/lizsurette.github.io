from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import re
import yaml
import logging

logger = logging.getLogger(__name__)

@dataclass
class Post:
    """
    Represents a blog post with its metadata and content.
    
    Attributes:
        path (str): The unique path identifier for the post
        title (str): The title of the post
        date (datetime): The publication date of the post
        categories (List[str]): Categories the post belongs to
        content (str): The raw markdown content
        html_content (str): The rendered HTML content
    """
    path: str
    title: str
    date: datetime
    categories: List[str]
    content: str = ""
    html_content: str = ""
    
    @property
    def meta(self) -> Dict[str, Any]:
        """
        Return metadata in the format expected by templates.
        
        Returns:
            Dict[str, Any]: A dictionary containing the post metadata
        """
        return {
            'title': self.title,
            'date': self.date,
            'categories': self.categories
        }
    
    @classmethod
    def from_file(cls, file_path: str, render_markdown_func=None) -> Optional['Post']:
        """
        Create a Post object from a markdown file.
        
        Args:
            file_path (str): Path to the markdown file
            render_markdown_func (callable, optional): Function to render markdown to HTML
            
        Returns:
            Optional[Post]: A Post object if successful, None otherwise
            
        Raises:
            PostNotFoundError: If the file does not exist
            PostContentError: If there's an error reading the file
            PostMetadataError: If there's an error with the post metadata
            YAMLParsingError: If there's an error parsing the YAML front matter
        """
        from app.models.exceptions import (
            PostNotFoundError, PostContentError, PostMetadataError, YAMLParsingError
        )
        
        try:
            # Extract the path (filename without extension)
            path = os.path.splitext(os.path.basename(file_path))[0]
            
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"Post file not found: {file_path}")
                raise PostNotFoundError(f"Post file not found: {file_path}")
            
            # Read the file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except IOError as e:
                logger.error(f"Error reading file {file_path}: {e}")
                raise PostContentError(f"Error reading file {file_path}: {e}")
            
            # Extract YAML front matter and content
            yaml_pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
            match = re.match(yaml_pattern, content, re.DOTALL)
            
            if not match:
                logger.warning(f"No YAML front matter found in {path}")
                raise PostMetadataError(f"No YAML front matter found in {path}")
            
            yaml_content = match.group(1).strip()
            post_content = content[match.end():].strip()
            
            # Parse the YAML content
            try:
                metadata = yaml.safe_load(yaml_content)
                if metadata is None:
                    metadata = {}
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML in {path}: {e}")
                raise YAMLParsingError(f"Error parsing YAML in {path}: {e}")
            
            # Extract required fields
            title = metadata.get('title', '')
            date_str = metadata.get('date', '')
            categories = metadata.get('categories', [])
            
            # Validate required fields
            if not title:
                logger.warning(f"Missing title in {path}")
                raise PostMetadataError(f"Missing title in {path}")
            
            if not date_str:
                logger.warning(f"Missing date in {path}")
                raise PostMetadataError(f"Missing date in {path}")
            
            # Clean up title
            if isinstance(title, str):
                title = title.strip().strip('"\'')
            
            # Parse date
            try:
                if isinstance(date_str, str):
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    date = date_str
            except ValueError:
                logger.warning(f"Invalid date format in {path}: {date_str}")
                raise PostMetadataError(f"Invalid date format in {path}: {date_str}")
            
            # Create post object
            post = cls(
                path=path,
                title=title,
                date=date,
                categories=categories,
                content=post_content
            )
            
            # Render markdown content if render function is provided
            if render_markdown_func:
                try:
                    post.html_content = render_markdown_func(post_content)
                except Exception as e:
                    logger.error(f"Error rendering markdown in {path}: {e}")
                    from app.models.exceptions import MarkdownRenderingError
                    raise MarkdownRenderingError(f"Error rendering markdown in {path}: {e}")
            
            return post
        except (PostNotFoundError, PostContentError, PostMetadataError, YAMLParsingError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating post from file {file_path}: {e}")
            from app.models.exceptions import PostError
            raise PostError(f"Unexpected error creating post from file {file_path}: {e}") 