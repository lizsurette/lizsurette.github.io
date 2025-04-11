import os
import sys
import shutil
import logging
from app import create_app
from flask import url_for

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app instance
app = create_app()

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
        from app import pages
        for post in pages:
            logger.info(f"Generating post: {post.path}")
            response = client.get(f'/post/{post.path}/')
            save_response(response, f'post/{post.path}/index.html')

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

def update_static_paths():
    """Update static file paths in HTML files to be relative."""
    for root, _, files in os.walk('_site'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace absolute paths with relative paths
                content = content.replace('href="/static/', 'href="../static/')
                content = content.replace('src="/static/', 'src="../static/')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Updated static paths in {file_path}")

if __name__ == '__main__':
    logger.info("Starting static site generation...")
    
    # Clean the site directory
    clean_site_directory()
    
    # Copy static assets
    copy_static_assets()
    
    # Generate static files
    generate_static_files()
    
    # Copy CNAME file
    copy_cname()
    
    # Update static paths
    update_static_paths()
    
    logger.info("Static site generation completed successfully!") 