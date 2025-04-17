import os
import sys
import shutil
import logging
import re
from flask import render_template, url_for
from app import create_app
from app.services.post_service import PostService
from app.services.markdown_service import MarkdownService
from app.services.config_service import ConfigService
from app.models.post import Post

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_posts():
    """Get all posts using PostService."""
    config_service = ConfigService()
    markdown_service = MarkdownService(config_service)
    post_service = PostService(config_service, markdown_service)
    return post_service.get_all_posts()

def clean_site_directory():
    """Clean the _site directory before generating static files."""
    site_dir = '_site'
    if os.path.exists(site_dir):
        # Remove HTML files but preserve directories
        for item in os.listdir(site_dir):
            item_path = os.path.join(site_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
    else:
        os.makedirs(site_dir)
    logger.info(f"Cleaned {site_dir} directory")

def copy_static_assets():
    """Copy static assets to the _site directory."""
    static_dir = os.path.join('app', 'static')
    site_static_dir = os.path.join('_site', 'static')
    
    if os.path.exists(site_static_dir):
        shutil.rmtree(site_static_dir)
    
    shutil.copytree(static_dir, site_static_dir)
    logger.info(f"Copied static assets to {site_static_dir}")

def generate_static_files():
    """Generate static files for the site."""
    logger.info("Generating static files...")
    
    app = create_app()
    
    # Generate index page
    with app.test_request_context():
        index_html = render_template('index.html')
        with open(os.path.join('_site', 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
    
    # Generate writings page
    with app.test_request_context():
        # Get all posts and ensure they have valid paths
        posts = get_posts()
        for post in posts:
            if not post.path or not post.path.strip():
                post.path = slugify(post.meta.title)
        
        writings_html = render_template('writings.html', posts=posts)
        os.makedirs(os.path.join('_site', 'writings'), exist_ok=True)
        with open(os.path.join('_site', 'writings', 'index.html'), 'w', encoding='utf-8') as f:
            f.write(writings_html)
    
    # Generate post pages
    for post in posts:
        post_path = post.path
        post_dir = os.path.join('_site', 'posts', post_path)
        os.makedirs(post_dir, exist_ok=True)
        
        with app.test_request_context():
            post_html = render_template('post.html', post=post)
            with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(post_html)
    
    logger.info("Static files generated successfully")

def update_static_paths(file_path):
    """Update static file paths in HTML files to be relative."""
    logger.info(f"Updating static paths in {file_path}")
    
    # Calculate the relative depth based on the file path
    relative_depth = len(file_path.split(os.sep)[1:-1])
    relative_prefix = '../' * relative_depth
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update static file paths
    content = content.replace('href="/static/', f'href="{relative_prefix}static/')
    content = content.replace('src="/static/', f'src="{relative_prefix}static/')
    
    # Update navigation links
    nav_links = ['writings', 'games', 'projects', 'apps']
    for link in nav_links:
        # Handle both with and without trailing slash
        content = content.replace(f'href="/{link}/"', f'href="{relative_prefix}{link}"')
        content = content.replace(f'href="/{link}"', f'href="{relative_prefix}{link}"')
    
    # Update home link
    content = content.replace('href="/"', f'href="{relative_prefix}"')
    
    # Update post links to use directory structure instead of .html files
    content = re.sub(
        r'href="/posts/([^"]+)\.html"',
        lambda m: f'href="{relative_prefix}posts/{m.group(1)}"',
        content
    )
    
    # Update empty post links (href="#") to use the data-path attribute
    content = re.sub(
        r'<a href="#">([^<]+)</a>',
        lambda m: f'<a href="{relative_prefix}posts/{m.group(1).lower().replace(" ", "-")}">{m.group(1)}</a>',
        content
    )
    
    # Remove any remaining absolute paths that start with /
    content = re.sub(r'(href|src)="/((?!/)([^"]+))"', rf'\1="{relative_prefix}\2"', content)
    
    # Remove trailing slashes from URLs
    content = re.sub(r'(href="[^"]+)/"', r'\1"', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"Updated static paths in {file_path}")

def slugify(text):
    """Convert text to a URL-friendly slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = re.sub(r'[\s]+', '-', text)
    # Remove special characters
    text = re.sub(r'[^\w\-]', '', text)
    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text

def update_index_paths(file_path):
    """Update paths in index.html to be relative to root."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update static file paths
    content = content.replace('href="/static/', 'href="static/')
    content = content.replace('src="/static/', 'src="static/')

    # Update navigation links
    content = content.replace('href="/"', 'href="./"')
    content = content.replace('href="/writings/"', 'href="writings/"')
    content = content.replace('href="/games/"', 'href="games/"')
    content = content.replace('href="/projects/"', 'href="projects/"')
    content = content.replace('href="/apps/"', 'href="apps/"')

    # Update post links to use directory structure
    content = re.sub(
        r'href="/posts/([^"]+)\.html"',
        lambda m: f'href="posts/{m.group(1)}"',
        content
    )
    
    # Remove trailing slashes from URLs
    content = content.replace('/">', '">')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    logging.info(f"Updated static paths in {file_path}")

if __name__ == '__main__':
    logger.info("Starting static site generation...")
    
    # Clean and prepare _site directory
    clean_site_directory()
    copy_static_assets()
    
    # Generate static files
    generate_static_files()
    
    # Update paths in generated files
    for root, dirs, files in os.walk('_site'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if file == 'index.html' and root == '_site':
                    update_index_paths(file_path)
                else:
                    update_static_paths(file_path)
    
    logger.info("Static site generation completed successfully!") 