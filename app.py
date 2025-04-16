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
from app.models.post import Post
from app.models.exceptions import PostError, PostNotFoundError, PostMetadataError, PostContentError, YAMLParsingError, MarkdownRenderingError
from app.repositories.post_repository import PostRepository
from app import create_app
from app.services.markdown_service import MarkdownService
from app.routes import main, post

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

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

app = create_app()

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
app.register_blueprint(main)
app.register_blueprint(post)

# Create a PostRepository instance
post_repository = PostRepository(os.path.join(app_dir, 'app', 'posts'), render_markdown)

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

@app.cli.command("build")
def build():
    """Build the static site."""
    logger.info("Building static site...")
    
    # Create _site directory if it doesn't exist
    if not os.path.exists("_site"):
        os.makedirs("_site")
    
    # Copy static files
    if os.path.exists("app/static"):
        import shutil
        shutil.copytree("app/static", "_site/static", dirs_exist_ok=True)
    
    # Generate HTML files for each route
    with app.test_request_context():
        # Generate index page
        with open("_site/index.html", "w") as f:
            f.write(render_template("index.html"))
        
        # Generate writings page
        posts = post_repository.get_all_posts()
        with open("_site/writings.html", "w") as f:
            f.write(render_template("writings.html", posts=posts))

        # Generate projects page
        with open("_site/projects.html", "w") as f:
            f.write(render_template("projects.html"))

        # Generate apps page
        with open("_site/apps.html", "w") as f:
            f.write(render_template("apps.html"))
        
        # Generate individual post pages
        for post in posts:
            post_dir = os.path.join("_site", "posts")
            os.makedirs(post_dir, exist_ok=True)
            with open(os.path.join(post_dir, f"{post.path}.html"), "w") as f:
                f.write(render_template("post.html", post=post))
    
    logger.info("Static site built successfully!")

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
    
    app.run(debug=True, port=5001) 