from app import app, pages, copy_static_assets
from flask_frozen import Freezer
import os

# Initialize the freezer
freezer = Freezer(app)

# Add all routes to the freezer
@freezer.register_generator
def post():
    for page in pages:
        yield {'path': page.path}

@freezer.register_generator
def index():
    yield {}

@freezer.register_generator
def about():
    yield {}

@freezer.register_generator
def writings():
    yield {}

@freezer.register_generator
def projects():
    yield {}

@freezer.register_generator
def games():
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
    # Register static files
    static_dir = os.path.join('app', 'static')
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), static_dir)
                yield {'filename': rel_path}

if __name__ == '__main__':
    # Create _site directory if it doesn't exist
    if not os.path.exists('_site'):
        os.makedirs('_site')
    
    # Copy static assets before freezing
    copy_static_assets()
    
    # Freeze the site
    freezer.freeze() 