from flask import Flask, render_template, url_for, abort, send_from_directory
from flask_flatpages import FlatPages
from datetime import datetime
import os
import logging
import yaml
import markdown
import shutil
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

# Custom exceptions
class PostError(Exception):
    """Base exception for post-related errors."""
    pass

class PostNotFoundError(PostError):
    """Raised when a post cannot be found."""
    pass

class PostMetadataError(PostError):
    """Raised when there's an error with post metadata."""
    pass

class PostContentError(PostError):
    """Raised when there's an error with post content."""
    pass

class YAMLParsingError(PostError):
    """Raised when there's an error parsing YAML front matter."""
    pass

class MarkdownRenderingError(PostError):
    """Raised when there's an error rendering markdown content."""
    pass

def render_markdown(text):
    """Render markdown text to HTML."""
    extensions = [
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.abbr'
    ]
    return markdown.markdown(text, extensions=extensions)

app = Flask(__name__, 
            template_folder=os.path.join(app_dir, 'app', 'templates'),
            static_folder=os.path.join(app_dir, 'app', 'static'),
            static_url_path='/static')

# Configure Flask-FlatPages
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = '.markdown'
app.config['FLATPAGES_ROOT'] = os.path.join(app_dir, 'app', 'posts')
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['codehilite', 'fenced_code', 'tables']
app.config['FLATPAGES_EXTENSION_CONFIGS'] = {
    'codehilite': {
        'linenums': True
    }
}
app.config['FLATPAGES_HTML_RENDERER'] = render_markdown

# Initialize FlatPages
pages = FlatPages(app)

# Register blueprints
from app.routes.main import main as main_blueprint
from app.routes.post import post as post_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(post_blueprint)

@dataclass
class Post:
    """Represents a blog post with its metadata and content."""
    path: str
    title: str
    date: datetime
    categories: List[str]
    content: str = ""
    html_content: str = ""
    
    @property
    def meta(self) -> Dict[str, Any]:
        """Return metadata in the format expected by templates."""
        return {
            'title': self.title,
            'date': self.date,
            'categories': self.categories
        }
    
    @classmethod
    def from_file(cls, file_path: str) -> Optional['Post']:
        """Create a Post object from a markdown file."""
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
            
            # Render markdown content
            try:
                post.html_content = render_markdown(post_content)
            except Exception as e:
                logger.error(f"Error rendering markdown in {path}: {e}")
                raise MarkdownRenderingError(f"Error rendering markdown in {path}: {e}")
            
            return post
        except PostError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating post from file {file_path}: {e}")
            raise PostError(f"Unexpected error creating post from file {file_path}: {e}")

class PostRepository:
    """Repository for managing blog posts."""
    
    def __init__(self, posts_dir: str):
        self.posts_dir = posts_dir
    
    def get_all_posts(self) -> List[Post]:
        """Get all posts from the posts directory."""
        posts = []
        
        try:
            # Get all markdown files in the posts directory
            for filename in os.listdir(self.posts_dir):
                if filename.endswith('.markdown'):
                    file_path = os.path.join(self.posts_dir, filename)
                    
                    try:
                        # Create post from file
                        post = Post.from_file(file_path)
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
        """Get a post by its path."""
        file_path = os.path.join(self.posts_dir, f"{path}.markdown")
        
        try:
            return Post.from_file(file_path)
        except PostNotFoundError:
            logger.error(f"Post file not found: {file_path}")
            return None
        except PostError as e:
            logger.error(f"Error getting post {path}: {e}")
            return None
    
    def get_next_post(self, current_path: str) -> Optional[Post]:
        """Get the next post in chronological order."""
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
        """Get the previous post in chronological order."""
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

# Create a PostRepository instance
post_repository = PostRepository(os.path.join(app_dir, 'app', 'posts'))

# Add a function to copy static assets during site generation
def copy_static_assets():
    try:
        # Create _site/static directory if it doesn't exist
        site_static_dir = os.path.join('_site', 'static')
        if not os.path.exists(site_static_dir):
            os.makedirs(site_static_dir)
        
        # Copy static assets
        static_dir = os.path.join('app', 'static')
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, static_dir)
                dst_path = os.path.join(site_static_dir, rel_path)
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
                
        logger.info("Static assets copied successfully")
    except Exception as e:
        logger.error(f"Error copying static assets: {e}")
        raise

@app.context_processor
def utility_processor():
    def format_date(date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                return date
        return date.strftime('%B %d, %Y')
    return dict(format_date=format_date)

if __name__ == '__main__':
    logger.info(f"Posts directory at startup: {app.config['FLATPAGES_ROOT']}")
    logger.info(f"Directory exists at startup: {os.path.exists(app.config['FLATPAGES_ROOT'])}")
    
    # Copy static assets when running in development
    copy_static_assets()
    
    try:
        all_posts = post_repository.get_all_posts()
        logger.info(f"Number of valid posts at startup: {len(all_posts)}")
        for post in all_posts:
            logger.info(f"Post at startup: {post.path} - {post.title} - {post.date}")
    except Exception as e:
        logger.error(f"Error loading posts at startup: {e}")
    
    app.run(debug=True) 