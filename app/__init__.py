import os
import logging
from flask import Flask, render_template
from flask_flatpages import FlatPages
from config import config
from app.services.markdown_service import MarkdownService
from app.repositories.post_repository import PostRepository
from app.models.exceptions import PostError, PostNotFoundError, PostMetadataError
from app.services.config_service import ConfigService

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name='default'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): The name of the configuration to use
        
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__, 
                template_folder=os.path.join(app_dir, 'templates'),
                static_folder=os.path.join(app_dir, 'static'),
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Set up logging
    from app.utils.logger import setup_logger
    setup_logger(app)
    
    # Create config service
    config_service = ConfigService(app.config)
    
    # Create markdown service
    markdown_service = MarkdownService(config_service)
    
    # Configure FlatPages with custom HTML renderer
    app.config['FLATPAGES_HTML_RENDERER'] = markdown_service.render
    app.pages = FlatPages(app)
    
    # Create post repository
    app.post_repository = PostRepository(
        posts_dir=app.config['FLATPAGES_ROOT'],
        render_markdown_func=markdown_service.render
    )
    
    # Register blueprints
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.post import post as post_blueprint
    app.register_blueprint(post_blueprint)
    
    # Register error handlers
    @app.errorhandler(PostNotFoundError)
    def handle_post_not_found(error):
        app.logger.error(f"Post not found: {error}")
        return render_template('error.html', 
                              title='Post Not Found', 
                              error=str(error)), 404
    
    @app.errorhandler(PostMetadataError)
    def handle_post_metadata_error(error):
        app.logger.error(f"Post metadata error: {error}")
        return render_template('error.html', 
                              title='Post Error', 
                              error=str(error)), 400
    
    @app.errorhandler(PostError)
    def handle_post_error(error):
        app.logger.error(f"Post error: {error}")
        return render_template('error.html', 
                              title='Post Error', 
                              error=str(error)), 500
    
    # Add context processor for date formatting
    @app.context_processor
    def utility_processor():
        def format_date(date):
            if isinstance(date, str):
                try:
                    from datetime import datetime
                    date = datetime.strptime(str(date), '%Y-%m-%d')
                except ValueError:
                    return date
            return date.strftime('%B %d, %Y')
        return dict(format_date=format_date)
    
    # Log startup information
    app.logger.info(f"Posts directory at startup: {app.config['FLATPAGES_ROOT']}")
    app.logger.info(f"Directory exists at startup: {os.path.exists(app.config['FLATPAGES_ROOT'])}")
    
    try:
        all_posts = app.post_repository.get_all_posts()
        app.logger.info(f"Number of valid posts at startup: {len(all_posts)}")
        for post in all_posts:
            app.logger.info(f"Post at startup: {post.path} - {post.title} - {post.date}")
    except Exception as e:
        app.logger.error(f"Error loading posts at startup: {e}")
    
    return app

def copy_static_assets():
    """
    Copy static assets to the build directory.
    This function is used by freeze.py to ensure all static assets are included in the build.
    """
    import shutil
    import os
    
    # Get the absolute path to the static directory
    static_dir = os.path.join(app_dir, 'static')
    build_dir = os.path.join(os.path.dirname(app_dir), 'build', 'static')
    
    # Create the build directory if it doesn't exist
    os.makedirs(build_dir, exist_ok=True)
    
    # Copy all static files
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, static_dir)
            dst_path = os.path.join(build_dir, rel_path)
            
            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(src_path, dst_path)

# Create the app instance
app = create_app()

# Export the app instance and copy_static_assets function
__all__ = ['app', 'copy_static_assets']
