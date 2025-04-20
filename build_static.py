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
        # Remove the entire directory and recreate it
        shutil.rmtree(site_dir)
    
    # Create the directory
    os.makedirs(site_dir)
    logger.info(f"Cleaned and created {site_dir} directory")

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
    
    # Generate games, apps, and projects pages
    pages = [
        ('games', 'Games'),
        ('apps', 'Apps'),
        ('projects', 'Projects')
    ]
    
    for page_name, title in pages:
        page_dir = os.path.join('_site', page_name)
        os.makedirs(page_dir, exist_ok=True)
        
        with app.test_request_context():
            page_html = render_template(f'{page_name}.html', title=title)
            with open(os.path.join(page_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(page_html)
    
    # Generate game pages
    games = ['snake', 'strands', 'sudoku', 'maze', 'gem-miner', 'hangman', 'bubble-shooter', 'survival']
    for game in games:
        try:
            # Create the game directory structure directly in _site
            game_dir = os.path.join('_site', game)
            os.makedirs(game_dir, exist_ok=True)
            
            # Map game names to their template names
            template_map = {
                'bubble-shooter': 'bubble.html',
                'survival': 'survival.html'  # Add explicit mapping for survival
            }
            
            # For games that should be copied directly from static directory
            static_only_games = {'gem-miner'}
            
            if game in static_only_games:
                # Copy directly from static directory
                static_game_dir = os.path.join('app', 'static', 'games', game)
                if os.path.exists(static_game_dir):
                    shutil.copytree(static_game_dir, game_dir, dirs_exist_ok=True)
                    logger.info(f"Copied static files for {game} game")
                else:
                    logger.error(f"Static directory not found for {game} game")
            else:
                # Use template rendering for other games
                template_name = template_map.get(game, f'{game}.html')
                with app.test_request_context():
                    game_html = render_template(template_name)
                    with open(os.path.join(game_dir, 'index.html'), 'w', encoding='utf-8') as f:
                        f.write(game_html)
                    logger.info(f"Generated {game} game page")
        except Exception as e:
            logger.error(f"Error generating {game} game page: {e}")
            # If template generation fails, try to copy from static directory
            try:
                static_game_dir = os.path.join('app', 'static', 'games', game)
                if os.path.exists(static_game_dir):
                    shutil.copytree(static_game_dir, game_dir, dirs_exist_ok=True)
                    logger.info(f"Copied static files for {game} game")
            except Exception as copy_error:
                logger.error(f"Error copying static files for {game} game: {copy_error}")
    
    logger.info("Static files generated successfully")

def update_static_paths(html_file):
    """Update static file paths in HTML files to be relative."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update image paths from GitHub URLs to local paths
    content = re.sub(
        r'src="https://github\.com/lizsurette/lizsurette\.github\.io/raw/main/static/img/_posts/([^"]+)"',
        r'src="../../static/img/_posts/\1"',
        content
    )
    
    # Update image paths from absolute paths to relative paths
    content = re.sub(
        r'src="/static/img/_posts/([^"]+)"',
        r'src="../../static/img/_posts/\1"',
        content
    )
    
    # Update navigation links to be relative
    content = re.sub(r'href="/', 'href="../../', content)
    
    # Update home link to be relative
    content = re.sub(r'href="([^"]*)" class="active">About Me</a>', r'href="../../" class="active">About Me</a>', content)
    
    # Update game links to point to the root directory
    content = re.sub(r'href="/games/([^"]+)"', r'href="/\1"', content)
    
    # Remove any remaining absolute paths that start with /
    content = re.sub(r'(href|src)="/', r'\1="../../', content)
    
    # Remove trailing slashes from URLs
    content = re.sub(r'(href|src)="([^"]+)/"', r'\1="\2"', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"Updated static paths in {html_file}")

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

    # Update game links to point to the root directory
    content = re.sub(r'href="/games/([^"]+)"', r'href="\1"', content)

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