from flask import Blueprint, render_template, current_app

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
        from app import post_repository
        posts = post_repository.get_all_posts()
        return render_template('index.html', title='Home', posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error in index route: {e}")
        return render_template('error.html', title='Error', error="An error occurred while loading the home page.")

@main.route('/writings/')
def writings():
    """
    Render the writings page.
    
    Returns:
        str: The rendered writings page
    """
    try:
        from app import post_repository
        posts = post_repository.get_all_posts()
        return render_template('writings.html', title='Writings', posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error in writings route: {e}")
        return render_template('error.html', title='Error', error="An error occurred while loading the writings page.")

@main.route('/games/')
def games():
    """
    Render the games page.
    
    Returns:
        str: The rendered games page
    """
    return render_template('games.html', title='Games')

@main.route('/projects/')
def projects():
    """
    Render the projects page.
    
    Returns:
        str: The rendered projects page
    """
    return render_template('projects.html', title='Projects')

@main.route('/apps/')
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