from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import re
import yaml
import logging
from app.models.exceptions import PostError

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
        metadata (Dict[str, Any]): Additional metadata from front matter
    """
    path: str
    title: str
    date: datetime
    categories: List[str]
    content: str = ""
    html_content: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values after dataclass initialization."""
        if self.metadata is None:
            self.metadata = {}
        if not isinstance(self.categories, list):
            self.categories = []
    
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
    def from_file(cls, file_path: str, render_markdown_func=None) -> 'Post':
        """
        Create a Post object from a markdown file.
        
        Args:
            file_path (str): Path to the markdown file
            render_markdown_func (callable, optional): Function to render markdown to HTML
            
        Returns:
            Post: A Post object
            
        Raises:
            PostError: If there is an error reading or parsing the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split front matter and content
            parts = content.split('---', 2)
            if len(parts) < 3:
                raise PostError("Invalid post format: missing front matter")
                
            # Parse front matter
            front_matter = parts[1].strip()
            post_content = parts[2].strip()
            
            # Parse metadata
            metadata = {}
            for line in front_matter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            # Get required fields
            title = metadata.get('title')
            date_str = metadata.get('date')
            
            # Get path from filename
            filename = os.path.basename(file_path)
            # Remove .markdown extension
            path = os.path.splitext(filename)[0]
            # Remove date prefix (YYYY-MM-DD-) if present
            path = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', path)
            
            # Ensure path is not empty and properly formatted
            if not path or path.isspace():
                # If path is empty, use the title to create a slug
                if title:
                    path = re.sub(r'[^a-z0-9]+', '-', title.lower())
                    path = re.sub(r'^-+|-+$', '', path)  # Remove leading/trailing hyphens
                else:
                    # If both path and title are empty, use a default
                    path = "untitled-post"
            
            # Ensure path doesn't contain double slashes
            path = path.replace('//', '/')
            
            if not all([title, date_str]):
                raise PostError("Missing required fields in front matter")
            
            # Parse date
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise PostError("Invalid date format in front matter")
            
            # Render markdown if function provided
            html_content = None
            if render_markdown_func:
                html_content = render_markdown_func(post_content)
            
            # Create post object
            return cls(
                title=title,
                date=date,
                path=path,
                content=post_content,
                html_content=html_content,
                metadata=metadata,
                categories=metadata.get('categories', [])
            )
            
        except IOError as e:
            raise PostError(f"Error reading post file: {e}")
        except Exception as e:
            raise PostError(f"Error creating post: {e}") 