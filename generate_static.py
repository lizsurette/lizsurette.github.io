import os
import sys
import shutil
from app import app
from flask_frozen import Freezer

# Initialize Freezer
freezer = Freezer(app)

# Configure Freezer
app.config['FREEZER_DESTINATION'] = '_site'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git', '.github', 'CNAME']

# Define the routes to freeze
@freezer.register_generator
def post():
    # Get all posts
    from app import pages
    for post in pages:
        yield {'path': post.path}

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

if __name__ == '__main__':
    # Clean the output directory
    if os.path.exists('_site'):
        shutil.rmtree('_site')
    
    # Create the output directory
    os.makedirs('_site', exist_ok=True)
    
    # Copy CNAME file to the output directory
    if os.path.exists('CNAME'):
        shutil.copy('CNAME', '_site/CNAME')
    
    # Freeze the application
    freezer.freeze()
    
    print("Static site generated in _site directory") 