import os
import logging
from typing import List, Optional
from app.models.post import Post
from app.models.exceptions import PostError

logger = logging.getLogger(__name__)

class PostRepository:
    """
    Repository for managing blog posts.
    
    This class handles the retrieval and management of blog posts
    from the filesystem.
    """
    
    def __init__(self, posts_dir: str, render_markdown_func=None):
        """
        Initialize the PostRepository.
        
        Args:
            posts_dir (str): Directory containing the markdown files
            render_markdown_func (callable, optional): Function to render markdown to HTML
        """
        self.posts_dir = posts_dir
        self.render_markdown_func = render_markdown_func
    
    def get_all_posts(self) -> List[Post]:
        """
        Get all posts from the posts directory.
        
        Returns:
            List[Post]: A list of Post objects
        """
        posts = []
        
        try:
            # Get all markdown files in the posts directory
            for filename in os.listdir(self.posts_dir):
                if filename.endswith('.markdown'):
                    file_path = os.path.join(self.posts_dir, filename)
                    
                    try:
                        # Create post from file
                        post = Post.from_file(file_path, self.render_markdown_func)
                        if post:
                            posts.append(post)
                    except PostError as e:
                        # Log the error but continue processing other posts
                        logger.warning(f"Skipping post {filename}: {e}")
        except Exception as e:
            logger.error(f"Error getting posts: {e}")
        
        # Sort posts by date
        posts.sort(key=lambda x: x.date, reverse=True)
        return posts
    
    def get_post_by_path(self, path: str) -> Optional[Post]:
        """
        Get a post by its path.
        
        Args:
            path (str): The path of the post
            
        Returns:
            Optional[Post]: The Post object if found, None otherwise
        """
        # Remove any trailing slashes
        path = path.rstrip('/')
        
        # Try to find the post file
        for filename in os.listdir(self.posts_dir):
            if filename.endswith('.markdown'):
                # Remove date prefix and extension for comparison
                file_path = os.path.join(self.posts_dir, filename)
                try:
                    post = Post.from_file(file_path, self.render_markdown_func)
                    if post.path == path:
                        return post
                except PostError:
                    continue
        
        return None
    
    def get_next_post(self, current_path: str) -> Optional[Post]:
        """
        Get the next post in chronological order.
        
        Args:
            current_path (str): The path of the current post
            
        Returns:
            Optional[Post]: The next Post object if found, None otherwise
        """
        posts = self.get_all_posts()
        
        # Find current post index
        current_index = -1
        for i, post in enumerate(posts):
            if post.path == current_path:
                current_index = i
                break
        
        # Get next post
        if current_index > 0:
            return posts[current_index - 1]
        return None
    
    def get_prev_post(self, current_path: str) -> Optional[Post]:
        """
        Get the previous post in chronological order.
        
        Args:
            current_path (str): The path of the current post
            
        Returns:
            Optional[Post]: The previous Post object if found, None otherwise
        """
        posts = self.get_all_posts()
        
        # Find current post index
        current_index = -1
        for i, post in enumerate(posts):
            if post.path == current_path:
                current_index = i
                break
        
        # Get previous post
        if current_index < len(posts) - 1:
            return posts[current_index + 1]
        return None 