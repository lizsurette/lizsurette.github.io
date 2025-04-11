from app import create_app, pages, post_repository
from flask_frozen import Freezer
import os
import re
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the app instance
app = create_app()

# Configure the app for freezing
app.config['FREEZER_DESTINATION'] = '_site'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'

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

@freezer.register_generator
def post_urls():
    """Generate URLs for all blog posts."""
    logger.debug("Generating post URLs...")
    for post in post_repository.get_all_posts():
        logger.debug(f"Generating URL for post: {post.path}")
        yield 'post.view', {'path': post.path}

@freezer.register_generator
def index_urls():
    """Generate URL for index page."""
    logger.debug("Generating index URL...")
    yield 'main.index', {}

@freezer.register_generator
def writings_urls():
    """Generate URL for writings page."""
    logger.debug("Generating writings URL...")
    yield 'main.writings', {}

@freezer.register_generator
def games_urls():
    """Generate URL for games page."""
    logger.debug("Generating games URL...")
    yield 'main.games', {}

@freezer.register_generator
def projects_urls():
    """Generate URL for projects page."""
    logger.debug("Generating projects URL...")
    yield 'main.projects', {}

@freezer.register_generator
def apps_urls():
    """Generate URL for apps page."""
    logger.debug("Generating apps URL...")
    yield 'main.apps', {}

@freezer.register_generator
def grocery_list_urls():
    """Generate URL for grocery list page."""
    logger.debug("Generating grocery list URL...")
    yield 'main.grocery_list', {}

@freezer.register_generator
def snake_urls():
    """Generate URL for snake game page."""
    logger.debug("Generating snake URL...")
    yield 'main.snake', {}

@freezer.register_generator
def hangman_urls():
    """Generate URL for hangman game page."""
    logger.debug("Generating hangman URL...")
    yield 'main.hangman', {}

@freezer.register_generator
def strands_urls():
    """Generate URL for strands game page."""
    logger.debug("Generating strands URL...")
    yield 'main.strands', {}

@freezer.register_generator
def survival_urls():
    """Generate URL for survival game page."""
    logger.debug("Generating survival URL...")
    yield 'main.survival', {}

@freezer.register_generator
def static_urls():
    """Generate URLs for static files."""
    logger.debug("Generating static URLs...")
    for root, dirs, files in os.walk('app/static'):
        for file in files:
            if not file.startswith('.'):
                # Remove 'app/static/' prefix from the path
                rel_path = os.path.relpath(os.path.join(root, file), 'app/static')
                logger.debug(f"Generating URL for static file: {rel_path}")
                yield 'static', {'filename': rel_path}

if __name__ == '__main__':
    # Create _site directory if it doesn't exist
    if not os.path.exists('_site'):
        os.makedirs('_site')
    
    # Copy static assets before freezing
    copy_static_assets()
    
    # Freeze the site
    logger.info("Starting site freeze...")
    try:
        with app.test_request_context():
            freezer.freeze()
        logger.info("Site freeze completed successfully.")
    except Exception as e:
        logger.error(f"Error freezing site: {e}")
        raise
    
    # Update static file paths in generated HTML files
    logger.info("Updating static file paths...")
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
    logger.info("Static file paths updated successfully.") 