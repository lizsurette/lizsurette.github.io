import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from .markdown_service import MarkdownService
from .config_service import ConfigService
from app.models.post import Post
import re

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
                post = Post.from_file(str(file_path), self.markdown._render_markdown)
                if post:
                    self._posts[post.path] = post
            except Exception as e:
                print(f"Error loading post {file_path}: {str(e)}")
    
    def get_post(self, path: str) -> Optional[Post]:
        """Get a post by path.
        
        Args:
            path: Post path
            
        Returns:
            Post instance or None if not found
        """
        return self._posts.get(path)
    
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