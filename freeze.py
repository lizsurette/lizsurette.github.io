from app import app, copy_static_assets
from flask_frozen import Freezer
import os
import re

# Initialize the freezer
freezer = Freezer(app)

# Configure the freezer for GitHub Pages
freezer.base_url = 'https://lizsurette.github.io/'
freezer.static_ignore = ['*.pyc', '*.pyo', '*.pyd', '__pycache__', '.git']

# Add all routes to the freezer
@freezer.register_generator
def post():
    for post in app.pages:
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
    # Create build directory if it doesn't exist
    if not os.path.exists('build'):
        os.makedirs('build')
    
    # Copy static assets before freezing
    copy_static_assets()
    
    # Configure Frozen-Flask to use the build directory
    app.config['FREEZER_DESTINATION'] = 'build'
    app.config['FREEZER_BASE_URL'] = freezer.base_url
    
    # Freeze the site
    freezer.freeze()
    
    # Update static file paths in generated HTML files
    for root, dirs, files in os.walk('build'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace relative static paths with absolute paths
                content = content.replace('../static/', '/static/')
                content = content.replace('./static/', '/static/')
                content = content.replace('src="/static/', 'src="static/')
                content = content.replace('href="/static/', 'href="static/')
                
                # Replace relative game paths with absolute paths
                content = content.replace('href="../snake/"', 'href="snake/"')
                content = content.replace('href="../hangman/"', 'href="hangman/"')
                content = content.replace('href="../strands/"', 'href="strands/"')
                content = content.replace('href="/snake/"', 'href="snake/"')
                content = content.replace('href="/hangman/"', 'href="hangman/"')
                content = content.replace('href="/strands/"', 'href="strands/"')
                
                with open(file_path, 'w') as f:
                    f.write(content) 