from flask import Blueprint, render_template, abort, current_app
from app.models.exceptions import PostError

# Create the post blueprint
post = Blueprint('post', __name__, url_prefix='/posts')

@post.route('/<path:path>/')
def view(path):
    """
    Render a blog post.
    
    Args:
        path: The path of the post
        
    Returns:
        str: The rendered post
    """
    try:
        from app import post_repository
        post_obj = post_repository.get_post_by_path(path)
        
        if not post_obj:
            abort(404)
        
        # Get previous and next posts for navigation
        prev_post = post_repository.get_prev_post(path)
        next_post = post_repository.get_next_post(path)
            
        return render_template('post.html', 
                             post=post_obj,
                             prev_post=prev_post,
                             next_post=next_post)
    except PostError as e:
        current_app.logger.error(f"Error in post route: {e}")
        return render_template('error.html', title='Error', error=str(e)), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error in post route: {e}")
        return render_template('error.html', title='Error', error="An unexpected error occurred."), 500 