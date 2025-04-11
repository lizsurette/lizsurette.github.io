from flask import Blueprint, render_template, current_app
from app.models.exceptions import PostError

# Create the post blueprint
post = Blueprint('post', __name__)

@post.route('/posts/<path:path>/')
def post_detail(path):
    """
    Render a blog post.
    
    Args:
        path (str): The path of the post
        
    Returns:
        str: The rendered post page
    """
    try:
        current_app.logger.debug(f"Attempting to get post: {path}")
        
        # Get the post repository from app context
        post_repository = current_app.post_repository
        
        # Get the post from the repository
        post_obj = post_repository.get_post_by_path(path)
        
        if not post_obj:
            current_app.logger.error(f"Post not found: {path}")
            return render_template('error.html', title='Post Not Found', error=f"The post '{path}' could not be found.")
        
        # Get next and previous posts
        next_post = post_repository.get_next_post(path)
        prev_post = post_repository.get_prev_post(path)
        
        # Create a post object that matches the template's expectations
        post_data = {
            'meta': post_obj.meta,
            'content': post_obj.html_content,
            'path': post_obj.path
        }
        
        return render_template('post.html', 
                             post=post_data,
                             next_post=next_post,
                             prev_post=prev_post)
    except PostError as e:
        current_app.logger.error(f"Post error in post route: {e}")
        return render_template('error.html', title='Post Error', error=str(e))
    except Exception as e:
        current_app.logger.error(f"Error in post route: {e}")
        current_app.logger.error(f"Post path: {path}")
        return render_template('error.html', title='Error', error="An error occurred while loading the post.") 