import os
import logging
from flask import Flask, render_template
from flask_flatpages import FlatPages
from app.services.config_service import ConfigService
from app.services.markdown_service import MarkdownService
from app.models.exceptions import PostError, PostNotFoundError, PostMetadataError

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

# Global variables to avoid circular imports
app = None
pages = None
post_repository = None

def create_app(config_name='default'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): The name of the configuration to use
        
    Returns:
        Flask: The configured Flask application
    """
    # Import necessary modules
    from app.repositories.post_repository import PostRepository
    from app.utils.logger import setup_logger
    
    # Create new Flask app instance
    app = Flask(__name__, 
                template_folder=os.path.join(app_dir, 'templates'),
                static_folder=os.path.join(app_dir, 'static'),
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(ConfigService())
    
    # Set up logging
    setup_logger(app)
    
    # Create config service
    config_service = ConfigService()
    
    # Create markdown service
    markdown_service = MarkdownService(config_service)
    
    # Configure FlatPages with custom HTML renderer
    app.config['FLATPAGES_HTML_RENDERER'] = markdown_service._render_markdown
    pages = FlatPages(app)
    
    # Create post repository
    post_repository = PostRepository(
        posts_dir=app.config['FLATPAGES_ROOT'],
        render_markdown_func=markdown_service._render_markdown
    )
    
    # Store post_repository in app context
    app.post_repository = post_repository
    
    # Register blueprints and error handlers
    register_blueprints(app)
    register_error_handlers(app)
    
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
        all_posts = post_repository.get_all_posts()
        app.logger.info(f"Number of valid posts at startup: {len(all_posts)}")
        for post in all_posts:
            app.logger.info(f"Post at startup: {post.path} - {post.title} - {post.date}")
    except Exception as e:
        app.logger.error(f"Error loading posts at startup: {e}")
    
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes import main, post, games
    app.register_blueprint(main.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(games.bp)

def register_error_handlers(app):
    """Register error handlers."""
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

# Export the create_app function
__all__ = ['create_app']
