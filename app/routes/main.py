from flask import Blueprint, render_template, current_app, abort, send_from_directory, redirect
import os

# Create the main blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Render the home page.
    
    Returns:
        str: The rendered home page
    """
    try:
        posts = current_app.post_repository.get_all_posts()
        return render_template('index.html', title='About Me', posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error in index route: {e}")
        return render_template('error.html', title='Error', error="An error occurred while loading the home page.")

@main.route('/writings')
@main.route('/writings/')
def writings():
    """
    Render the writings page.
    
    Returns:
        str: The rendered writings page
    """
    try:
        posts = current_app.post_repository.get_all_posts()
        return render_template('writings.html', title='Writings', posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error getting posts: {e}")
        return render_template('error.html', title='Error', error=str(e)), 500

@main.route('/games')
def games():
    """
    Render the games page.
    
    Returns:
        str: The rendered games page
    """
    return render_template('games.html', title='Games')

@main.route('/projects')
def projects():
    """
    Render the projects page.
    
    Returns:
        str: The rendered projects page
    """
    return render_template('projects.html', title='Projects')

@main.route('/apps')
def apps():
    """
    Render the apps page.
    
    Returns:
        str: The rendered apps page
    """
    return render_template('apps.html', title='AI Generated Apps')

@main.route('/grocery-list/')
def grocery_list():
    """
    Render the grocery list page.
    
    Returns:
        str: The rendered grocery list page
    """
    return render_template('grocery-list.html', title='Smart Grocery List')

@main.route('/snake/')
def snake():
    """
    Render the snake game page.
    
    Returns:
        str: The rendered snake game page
    """
    return render_template('snake.html', title='Snake Game')

@main.route('/hangman/')
def hangman():
    """
    Render the hangman game page.
    
    Returns:
        str: The rendered hangman game page
    """
    return render_template('hangman.html', title='Hangman Game')

@main.route('/strands/')
def strands():
    """
    Render the strands game page.
    
    Returns:
        str: The rendered strands game page
    """
    return render_template('strands.html', title='Strands Game')

@main.route('/survival/')
def survival():
    """
    Render the survival game page.
    
    Returns:
        str: The rendered survival game page
    """
    return render_template('survival.html', title='Survival Game')

@main.route('/category/<name>/')
def category(name):
    """
    Render a category page.
    
    Args:
        name (str): The name of the category
        
    Returns:
        str: The rendered category page
    """
    try:
        posts = current_app.post_repository.get_all_posts()
        
        # Filter posts by category
        category_posts = [post for post in posts if name.lower() in [cat.lower() for cat in post.categories]]
        
        return render_template('category.html', 
                             title=f'Posts in {name.title()}', 
                             category=name,
                             posts=category_posts)
    except Exception as e:
        current_app.logger.error(f"Error in category route: {e}")
        return render_template('error.html', title='Error', error="An error occurred while loading the category page.")

@main.route('/posts/<path:post_path>/')
def post(post_path):
    """
    Render a single post page.
    
    Args:
        post_path (str): The path of the post to render
        
    Returns:
        str: The rendered post page
    """
    try:
        # Remove any trailing slashes
        post_path = post_path.rstrip('/')
        
        # Get the post
        post = current_app.post_repository.get_post_by_path(post_path)
        
        if post is None:
            current_app.logger.error(f"Post not found: {post_path}")
            abort(404)
        
        # Get next and previous posts
        next_post = current_app.post_repository.get_next_post(post_path)
        prev_post = current_app.post_repository.get_prev_post(post_path)
        
        return render_template('post.html',
                             title=post.title,
                             post=post,
                             next_post=next_post,
                             prev_post=prev_post)
    except Exception as e:
        current_app.logger.error(f"Error rendering post {post_path}: {e}")
        return render_template('error.html', title='Error', error=str(e)), 500

@main.route('/maze/')
def maze():
    """
    Render the maze game page.
    
    Returns:
        str: The rendered maze game page
    """
    return render_template('maze.html', title='Maze Game')

@main.route('/bubble/')
def bubble():
    """
    Render the bubble shooter game page.
    
    Returns:
        str: The rendered bubble shooter game page
    """
    return render_template('bubble.html', title='Bubble Shooter')

@main.route('/sudoku/')
def sudoku():
    """
    Render the Sudoku game page.
    
    Returns:
        str: The rendered Sudoku game page
    """
    return render_template('sudoku.html', title='Sudoku Game')

@main.route('/gem-miner/')
def gem_miner():
    """
    Serve the Gem Miner game from the gem-miner directory.
    
    Returns:
        str: The gem miner game HTML file
    """
    # Get the absolute path to the gem-miner directory
    gem_miner_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gem-miner')
    return send_from_directory(gem_miner_dir, 'index.html')

@main.route('/gem-miner')
def gem_miner_redirect():
    """
    Redirect to the gem-miner route.
    
    Returns:
        redirect: Redirect to the gem-miner route
    """
    return redirect('/gem-miner/') 