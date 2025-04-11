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

# Add all routes to the freezer
@freezer.register_generator
def post():
    for post in pages:
        yield {'path': post.path}

@freezer.register_generator
def index():
    yield {}

@freezer.register_generator
def writings():
    yield {}

@freezer.register_generator
def games():
    yield {}

@freezer.register_generator
def projects():
    yield {}

@freezer.register_generator
def apps():
    yield {}

@freezer.register_generator
def grocery_list():
    yield {}

@freezer.register_generator
def snake():
    yield {}

@freezer.register_generator
def hangman():
    yield {}

@freezer.register_generator
def strands():
    yield {}

@freezer.register_generator
def static():
    for root, dirs, files in os.walk('app/static'):
        for file in files:
            if not file.startswith('.'):
                yield {'filename': os.path.join(root, file).replace('app/static/', '')}

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