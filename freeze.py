from app import app, pages
from flask_frozen import Freezer
import os
import re
import shutil

def copy_static_assets():
    """Copy static assets to the _site directory."""
    static_dir = os.path.join('app', 'static')
    site_static_dir = os.path.join('_site', 'static')
    
    if os.path.exists(site_static_dir):
        shutil.rmtree(site_static_dir)
    
    shutil.copytree(static_dir, site_static_dir)

# Initialize the freezer
freezer = Freezer(app)

# Configure the freezer for GitHub Pages
freezer.base_url = 'https://lizsurette.github.io/'
freezer.static_ignore = ['*.pyc', '*.pyo', '*.pyd', '__pycache__', '.git']

def post_urls():
    """Generate URLs for blog posts."""
    from app import post_repository
    for post in post_repository.get_all_posts():
        yield 'post.view', {'path': post.path}

def index_urls():
    """Generate URL for index page."""
    yield 'main.index', {}

def writings_urls():
    """Generate URL for writings page."""
    yield 'main.writings', {}

def games_urls():
    """Generate URL for games page."""
    yield 'main.games', {}

def projects_urls():
    """Generate URL for projects page."""
    yield 'main.projects', {}

def apps_urls():
    """Generate URL for apps page."""
    yield 'main.apps', {}

def grocery_list_urls():
    """Generate URL for grocery list page."""
    yield 'main.grocery_list', {}

def snake_urls():
    """Generate URL for snake game page."""
    yield 'main.snake', {}

def hangman_urls():
    """Generate URL for hangman game page."""
    yield 'main.hangman', {}

def strands_urls():
    """Generate URL for strands game page."""
    yield 'main.strands', {}

def survival_urls():
    """Generate URL for survival game page."""
    yield 'main.survival', {}

def static_urls():
    """Generate URLs for static files."""
    for root, dirs, files in os.walk('app/static'):
        for file in files:
            if not file.startswith('.'):
                # Remove 'app/static/' prefix from the path
                rel_path = os.path.relpath(os.path.join(root, file), 'app/static')
                yield 'static', {'filename': rel_path}

# Add URL generators
freezer.url_generators.extend([
    post_urls,
    index_urls,
    writings_urls,
    games_urls,
    projects_urls,
    apps_urls,
    grocery_list_urls,
    snake_urls,
    hangman_urls,
    strands_urls,
    survival_urls,
    static_urls
])

if __name__ == '__main__':
    # Create _site directory if it doesn't exist
    if not os.path.exists('_site'):
        os.makedirs('_site')
    
    # Copy static assets before freezing
    copy_static_assets()
    
    # Freeze the site
    freezer.freeze()
    
    # Update static file paths in generated HTML files
    for root, dirs, files in os.walk('_site'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace relative static paths with absolute paths
                content = content.replace('../static/', '/static/')
                content = content.replace('./static/', '/static/')
                
                # Replace relative game paths with absolute paths
                content = content.replace('href="../snake/"', 'href="/snake/"')
                content = content.replace('href="../hangman/"', 'href="/hangman/"')
                content = content.replace('href="../strands/"', 'href="/strands/"')
                
                with open(file_path, 'w') as f:
                    f.write(content) 