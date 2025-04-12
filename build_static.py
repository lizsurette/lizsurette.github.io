import os
import sys
import shutil
import logging
from flask import render_template
from app import create_app
from app.services.post_service import PostService
from app.services.markdown_service import MarkdownService
from app.services.config_service import ConfigService
from flask import url_for

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app instance
app = create_app()

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
    with app.test_client() as client:
        # Generate index page
        logger.info("Generating index page")
        response = client.get('/')
        save_response(response, 'index.html')
        
        # Generate writings page
        logger.info("Generating writings page")
        response = client.get('/writings/')
        save_response(response, 'writings/index.html')
        
        # Generate games page
        logger.info("Generating games page")
        response = client.get('/games/')
        save_response(response, 'games/index.html')
        
        # Generate projects page
        logger.info("Generating projects page")
        response = client.get('/projects/')
        save_response(response, 'projects/index.html')
        
        # Generate apps page
        logger.info("Generating apps page")
        response = client.get('/apps/')
        save_response(response, 'apps/index.html')
        
        # Generate grocery list page
        logger.info("Generating grocery list page")
        response = client.get('/grocery-list/')
        save_response(response, 'grocery-list/index.html')
        
        # Generate snake game page
        logger.info("Generating snake game page")
        response = client.get('/snake/')
        save_response(response, 'snake/index.html')
        
        # Generate hangman game page
        logger.info("Generating hangman game page")
        response = client.get('/hangman/')
        save_response(response, 'hangman/index.html')
        
        # Generate strands game page
        logger.info("Generating strands game page")
        response = client.get('/strands/')
        save_response(response, 'strands/index.html')
        
        # Generate survival game page
        logger.info("Generating survival game page")
        response = client.get('/survival/')
        save_response(response, 'survival/index.html')
        
        # Generate blog post pages
        logger.info("Generating blog post pages")
        posts = get_posts()
        for post in posts:
            logger.info(f"Generating post: {post.slug}")
            post_html = render_template('post.html', post=post)
            post_dir = os.path.join('_site', 'posts', post.slug)
            os.makedirs(post_dir, exist_ok=True)
            with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(post_html)
            logger.info(f"Saved _site/posts/{post.slug}/index.html")

def save_response(response, path):
    """Save the response content to a file."""
    # Create directory if it doesn't exist
    dir_path = os.path.join('_site', os.path.dirname(path))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # Save the file
    file_path = os.path.join('_site', path)
    with open(file_path, 'wb') as f:
        f.write(response.data)
    logger.info(f"Saved {file_path}")

def copy_cname():
    """Copy CNAME file to the _site directory if it exists."""
    if os.path.exists('CNAME'):
        shutil.copy('CNAME', '_site/CNAME')
        logger.info("Copied CNAME file to _site directory")

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
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting static site generation...")

    # Clean _site directory
    if os.path.exists('_site'):
        shutil.rmtree('_site')
    os.makedirs('_site')
    logger.info("Cleaned _site directory")

    # Copy static assets
    if os.path.exists('app/static'):
        shutil.copytree('app/static', '_site/static')
        logger.info("Copied static assets to _site/static")

    # Copy CNAME file if it exists
    if os.path.exists('CNAME'):
        shutil.copy2('CNAME', '_site/CNAME')
        logger.info("Copied CNAME file to _site directory")

    # Generate pages
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():
        # Generate index page
        logger.info("Generating index page")
        index_html = render_template('index.html')
        os.makedirs('_site', exist_ok=True)
        with open('_site/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        logger.info("Saved _site/index.html")

        # Generate writings page
        logger.info("Generating writings page")
        writings_html = render_template('writings.html')
        os.makedirs('_site/writings', exist_ok=True)
        with open('_site/writings/index.html', 'w', encoding='utf-8') as f:
            f.write(writings_html)
        logger.info("Saved _site/writings/index.html")

        # Generate games page
        logger.info("Generating games page")
        games_html = render_template('games.html')
        os.makedirs('_site/games', exist_ok=True)
        with open('_site/games/index.html', 'w', encoding='utf-8') as f:
            f.write(games_html)
        logger.info("Saved _site/games/index.html")

        # Generate projects page
        logger.info("Generating projects page")
        projects_html = render_template('projects.html')
        os.makedirs('_site/projects', exist_ok=True)
        with open('_site/projects/index.html', 'w', encoding='utf-8') as f:
            f.write(projects_html)
        logger.info("Saved _site/projects/index.html")

        # Generate apps page
        logger.info("Generating apps page")
        apps_html = render_template('apps.html')
        os.makedirs('_site/apps', exist_ok=True)
        with open('_site/apps/index.html', 'w', encoding='utf-8') as f:
            f.write(apps_html)
        logger.info("Saved _site/apps/index.html")

        # Generate grocery list page
        logger.info("Generating grocery list page")
        grocery_list_html = render_template('grocery-list.html')
        os.makedirs('_site/grocery-list', exist_ok=True)
        with open('_site/grocery-list/index.html', 'w', encoding='utf-8') as f:
            f.write(grocery_list_html)
        logger.info("Saved _site/grocery-list/index.html")

        # Generate snake game page
        logger.info("Generating snake game page")
        snake_html = render_template('snake.html')
        os.makedirs('_site/snake', exist_ok=True)
        with open('_site/snake/index.html', 'w', encoding='utf-8') as f:
            f.write(snake_html)
        logger.info("Saved _site/snake/index.html")

        # Generate hangman game page
        logger.info("Generating hangman game page")
        hangman_html = render_template('hangman.html')
        os.makedirs('_site/hangman', exist_ok=True)
        with open('_site/hangman/index.html', 'w', encoding='utf-8') as f:
            f.write(hangman_html)
        logger.info("Saved _site/hangman/index.html")

        # Generate strands game page
        logger.info("Generating strands game page")
        strands_html = render_template('strands.html')
        os.makedirs('_site/strands', exist_ok=True)
        with open('_site/strands/index.html', 'w', encoding='utf-8') as f:
            f.write(strands_html)
        logger.info("Saved _site/strands/index.html")

        # Generate survival game page
        logger.info("Generating survival game page")
        survival_html = render_template('survival.html')
        os.makedirs('_site/survival', exist_ok=True)
        with open('_site/survival/index.html', 'w', encoding='utf-8') as f:
            f.write(survival_html)
        logger.info("Saved _site/survival/index.html")

        # Generate blog post pages
        logger.info("Generating blog post pages")
        posts = get_posts()
        for post in posts:
            logger.info(f"Generating post: {post.slug}")
            post_html = render_template('post.html', post=post)
            post_dir = os.path.join('_site', 'posts', post.slug)
            os.makedirs(post_dir, exist_ok=True)
            with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(post_html)
            logger.info(f"Saved _site/posts/{post.slug}/index.html")

    # Update static paths
    for root, _, files in os.walk('_site'):
        for file in files:
            if file.endswith('.html'):
                update_static_paths(os.path.join(root, file))

    # Update index paths
    update_index_paths('_site/index.html')

    logger.info("Static site generation completed successfully!") 