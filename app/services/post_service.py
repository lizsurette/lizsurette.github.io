import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from .markdown_service import MarkdownService
from .config_service import ConfigService
import re

@dataclass
class Post:
    """Data class representing a blog post."""
    title: str
    date: datetime
    content: str
    slug: str
    categories: List[str]
    metadata: Dict[str, Any]
    
    @property
    def url(self) -> str:
        """Get the URL for this post."""
        return f"/writings/{self.slug}"
    
    @property
    def formatted_date(self) -> str:
        """Get the formatted date string."""
        return self.date.strftime("%B %d, %Y")

class PostService:
    """Service for managing blog posts."""
    
    def __init__(self, config_service: ConfigService, markdown_service: MarkdownService):
        """Initialize the post service.
        
        Args:
            config_service: ConfigService instance
            markdown_service: MarkdownService instance
        """
        self.config = config_service
        self.markdown = markdown_service
        self.posts_dir = Path(self.config.posts_dir)
        self._posts: Dict[str, Post] = {}
        self._load_posts()
    
    def _load_posts(self) -> None:
        """Load all posts from the posts directory."""
        for file_path in self.posts_dir.glob("*.markdown"):
            try:
                post = self._load_post(file_path)
                if post:
                    self._posts[post.slug] = post
            except Exception as e:
                print(f"Error loading post {file_path}: {str(e)}")
    
    def _load_post(self, file_path: Path) -> Optional[Post]:
        """Load a single post from a markdown file.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Post object if successful, None otherwise
        """
        metadata, content = self.markdown.process_file(file_path)
        
        # Extract required fields
        title = metadata.get('title')
        date_str = metadata.get('date')
        categories = metadata.get('categories', [])
        
        if not all([title, date_str]):
            return None
            
        try:
            # Handle both string and datetime objects
            if isinstance(date_str, str):
                date = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                date = date_str
        except ValueError:
            return None
            
        # Generate slug from filename
        slug = file_path.stem
        
        return Post(
            title=title,
            date=date,
            content=content,
            slug=slug,
            categories=categories,
            metadata=metadata
        )
    
    def get_post(self, slug: str) -> Optional[Post]:
        """Get a post by slug.
        
        Args:
            slug: Post slug
            
        Returns:
            Post instance or None if not found
        """
        return self._posts.get(slug)
    
    def get_all_posts(self) -> List[Post]:
        """Get all posts.
        
        Returns:
            List of Post instances
        """
        return sorted(
            self._posts.values(),
            key=lambda p: p.date,
            reverse=True
        )
    
    def get_posts_by_category(self, category: str) -> List[Post]:
        """Get posts by category.
        
        Args:
            category: Category name
            
        Returns:
            List of Post instances
        """
        return sorted(
            [p for p in self._posts.values() if category in p.categories],
            key=lambda p: p.date,
            reverse=True
        )
    
    def get_posts_by_tag(self, tag: str) -> List[Post]:
        """Get posts by tag.
        
        Args:
            tag: Tag name
            
        Returns:
            List of Post instances
        """
        return sorted(
            [p for p in self._posts.values() if tag in p.metadata.get('tags', [])],
            key=lambda p: p.date,
            reverse=True
        )
    
    def get_categories(self) -> List[str]:
        """Get all categories.
        
        Returns:
            List of category names
        """
        categories = set()
        for post in self._posts.values():
            categories.update(post.categories)
        return sorted(list(categories))
    
    def get_tags(self) -> List[str]:
        """Get all tags.
        
        Returns:
            List of tag names
        """
        tags = set()
        for post in self._posts.values():
            tags.update(post.metadata.get('tags', []))
        return sorted(list(tags)) 