import os
import sys
import shutil
import logging
from flask import render_template, url_for
from app import create_app
from app.services.post_service import PostService
from app.services.markdown_service import MarkdownService
from app.services.config_service import ConfigService

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
        shutil.rmtree(site_dir)
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
    """Generate static HTML files for all routes."""
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost'
    
    with app.test_request_context():
        # Generate index page
        logger.info("Generating index page")
        index_html = render_template('index.html', title='About Me')
        os.makedirs('_site', exist_ok=True)
        
        with open('_site/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        # Generate writings page
        logger.info("Generating writings page")
        posts = get_posts()
        writings_html = render_template('writings.html', title='Writings', posts=posts)
        os.makedirs('_site/writings', exist_ok=True)
        
        with open('_site/writings/index.html', 'w', encoding='utf-8') as f:
            f.write(writings_html)
        
        # Generate post pages
        logger.info("Generating post pages")
        for post in posts:
            # Skip posts with empty paths
            if not post.path or post.path.strip() == '':
                logger.warning(f"Skipping post with empty path: {post.title}")
                continue
                
            # Create directory for post
            post_dir = os.path.join('_site', 'posts', post.path)
            os.makedirs(post_dir, exist_ok=True)
            
            # Generate post HTML
            post_html = render_template('post.html', post=post)
            
            # Write post HTML
            with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(post_html)
            
            logger.info(f"Generated post: {post.path}")
        
        # Generate games page
        logger.info("Generating games page")
        games_html = render_template('games.html', title='Games')
        os.makedirs('_site/games', exist_ok=True)
        
        with open('_site/games/index.html', 'w', encoding='utf-8') as f:
            f.write(games_html)
        
        # Generate game pages
        game_dirs = ['sudoku', 'hangman', 'snake', 'maze', 'bubble', 'gem-miner', 'survival', 'strands']
        for game_dir in game_dirs:
            if os.path.exists(os.path.join('app', 'templates', f'{game_dir}.html')):
                logger.info(f"Generating {game_dir} page")
                game_html = render_template(f'{game_dir}.html', title=game_dir.capitalize())
                os.makedirs(f'_site/{game_dir}', exist_ok=True)
                
                with open(f'_site/{game_dir}/index.html', 'w', encoding='utf-8') as f:
                    f.write(game_html)
        
        # Generate projects page
        logger.info("Generating projects page")
        projects_html = render_template('projects.html', title='Projects')
        os.makedirs('_site/projects', exist_ok=True)
        
        with open('_site/projects/index.html', 'w', encoding='utf-8') as f:
            f.write(projects_html)
        
        # Generate error page
        logger.info("Generating error page")
        error_html = render_template('error.html', title='Error', error='Page not found')
        os.makedirs('_site/error', exist_ok=True)
        
        with open('_site/error/index.html', 'w', encoding='utf-8') as f:
            f.write(error_html)
        
        logger.info("Static site generation completed")

def update_static_paths(file_path):
    """Update static file paths in HTML files to be relative."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update static file paths
    content = content.replace('href="/static/', 'href="../static/')
    content = content.replace('src="/static/', 'src="../static/')

    # Update navigation links
    content = content.replace('href="/"', 'href="../"')
    content = content.replace('href="/writings/"', 'href="../writings/"')
    content = content.replace('href="/games/"', 'href="../games/"')
    content = content.replace('href="/projects/"', 'href="../projects/"')
    content = content.replace('href="/apps/"', 'href="../apps/"')

    # Update post links
    content = content.replace('href="/posts/', 'href="../posts/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    logging.info(f"Updated static paths in {file_path}")

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

    # Update post links
    content = content.replace('href="/posts/', 'href="posts/')

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