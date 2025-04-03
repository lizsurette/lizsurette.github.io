import os
import sys
import shutil
from app import app
from flask_frozen import Freezer

# Initialize Freezer
freezer = Freezer(app)

# Define the output directory
freezer.config['FREEZER_DESTINATION'] = '_site'
freezer.config['FREEZER_RELATIVE_URLS'] = True
freezer.config['FREEZER_DESTINATION_IGNORE'] = ['.git', '.github', 'CNAME']

# Define the routes to freeze
@freezer.register_generator
def post():
    # Get all posts
    from app import pages
    for post in pages:
        yield {'path': post.path}

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
    
    # Start a simple HTTP server to test the static site
    print("Starting HTTP server to test the static site...")
    print("Visit http://localhost:8000 to view the site")
    print("Press Ctrl+C to stop the server")
    
    os.chdir('_site')
    os.system('python -m http.server 8000') 