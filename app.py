from flask import Flask, render_template, url_for, abort
from flask_flatpages import FlatPages
from datetime import datetime
import os
import logging
import yaml
import markdown

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(app_dir, 'app', 'templates'),
            static_folder=os.path.join(app_dir, 'app', 'static'),
            static_url_path='/static')

# Configure Flask-FlatPages
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = '.markdown'
app.config['FLATPAGES_ROOT'] = os.path.join(app_dir, 'app', 'posts')
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['codehilite', 'fenced_code', 'tables']
app.config['FLATPAGES_EXTENSION_CONFIGS'] = {
    'codehilite': {
        'linenums': True
    }
}

def parse_yaml(content):
    """Parse YAML front matter."""
    try:
        if content.startswith('---'):
            # Find the second occurrence of ---
            end_idx = content.find('---', 3)
            if end_idx != -1:
                # Extract YAML content between the --- markers
                yaml_content = content[3:end_idx].strip()
                # Parse YAML content
                metadata = yaml.safe_load(yaml_content)
                # Get the rest of the content
                content = content[end_idx + 3:].strip()
                return metadata, content
    except Exception as e:
        logger.error(f"Error parsing YAML: {e}")
    return {}, content

# Initialize FlatPages with custom YAML parser
app.config['FLATPAGES_HTML_RENDERER'] = parse_yaml
pages = FlatPages(app)

def get_safe_post_meta(post):
    """Safely get post metadata"""
    try:
        # Get the raw content from the file
        post_path = os.path.join(app.config['FLATPAGES_ROOT'], post.path + '.markdown')
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the YAML front matter
        metadata, _ = parse_yaml(content)
        
        return {
            'path': getattr(post, 'path', ''),
            'title': metadata.get('title', ''),
            'date': metadata.get('date', ''),
            'categories': metadata.get('categories', [])
        }
    except Exception as e:
        logger.error(f"Error getting post meta: {e}")
        return {'path': '', 'title': '', 'date': '', 'categories': []}

@app.route('/')
def index():
    try:
        posts = [p for p in pages]
        logger.debug(f"Found {len(posts)} posts in index route")
        # Sort posts by date
        posts.sort(key=lambda x: get_safe_post_meta(x)['date'], reverse=True)
        return render_template('index.html', title='Home', posts=posts)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('index.html', title='Home', posts=[])

@app.route('/about/')
def about():
    return render_template('about.html', title='About')

@app.route('/writings/')
def writings():
    try:
        logger.debug(f"Posts directory: {app.config['FLATPAGES_ROOT']}")
        logger.debug(f"Directory exists: {os.path.exists(app.config['FLATPAGES_ROOT'])}")
        
        # List all files in the posts directory
        posts_dir = app.config['FLATPAGES_ROOT']
        if os.path.exists(posts_dir):
            files = os.listdir(posts_dir)
            logger.debug(f"Files in posts directory: {files}")
        
        posts = []
        for post in pages:
            try:
                meta = get_safe_post_meta(post)
                if meta['title'] and meta['date']:  # Only include posts with title and date
                    posts.append({
                        'path': post.path,
                        'meta': meta
                    })
            except Exception as e:
                logger.error(f"Error processing post: {e}")
        
        logger.debug(f"Number of valid posts: {len(posts)}")
        for post in posts:
            logger.debug(f"Post: {post}")
        
        # Sort posts by date
        posts.sort(key=lambda x: x['meta']['date'], reverse=True)
        return render_template('writings.html', title='Writings', posts=posts)
    except Exception as e:
        logger.error(f"Error in writings route: {e}")
        return render_template('writings.html', title='Writings', posts=[])

@app.route('/posts/<path:path>/')
def post(path):
    try:
        logger.debug(f"Requested post path: {path}")
        page = pages.get_or_404(path)
        
        # Get the raw content from the file
        post_path = os.path.join(app.config['FLATPAGES_ROOT'], path + '.markdown')
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the YAML front matter and content
        metadata, post_content = parse_yaml(content)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            post_content,
            extensions=['codehilite', 'fenced_code', 'tables', 'attr_list', 'def_list', 'abbr']
        )
        
        # Create a custom page object with the parsed content
        page.content = html_content
        page.meta = metadata
        
        # Get all posts and sort by date
        all_posts = []
        for post in pages:
            try:
                meta = get_safe_post_meta(post)
                if meta['title'] and meta['date']:  # Only include posts with title and date
                    all_posts.append({
                        'path': post.path,
                        'meta': meta
                    })
            except Exception as e:
                logger.error(f"Error processing post: {e}")
        
        # Sort posts by date
        all_posts.sort(key=lambda x: x['meta']['date'], reverse=True)
        
        # Find current post index
        current_index = -1
        for i, post in enumerate(all_posts):
            if post['path'] == path:
                current_index = i
                break
        
        # Get next and previous posts
        next_post = all_posts[current_index - 1] if current_index > 0 else None
        prev_post = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
        
        logger.debug(f"Found page: {metadata}")
        return render_template('post.html', 
                              page=page, 
                              title=metadata.get('title', ''),
                              next_post=next_post,
                              prev_post=prev_post)
    except Exception as e:
        logger.error(f"Error in post route: {e}")
        abort(404)

@app.route('/games/')
def games():
    return render_template('games.html', title='Games')

@app.route('/snake/')
def snake():
    return render_template('snake.html', title='Snake Game')

@app.route('/hangman/')
def hangman():
    return render_template('hangman.html', title='Hangman Game')

@app.route('/strands/')
def strands():
    return render_template('strands.html', title='Strands Game')

@app.route('/projects/')
def projects():
    return render_template('projects.html', title='Projects')

@app.context_processor
def utility_processor():
    def format_date(date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                return date
        return date.strftime('%B %d, %Y')
    return dict(format_date=format_date)

if __name__ == '__main__':
    logger.info(f"Posts directory at startup: {app.config['FLATPAGES_ROOT']}")
    logger.info(f"Directory exists at startup: {os.path.exists(app.config['FLATPAGES_ROOT'])}")
    
    try:
        all_posts = []
        for post in pages:
            try:
                meta = get_safe_post_meta(post)
                if meta['title'] and meta['date']:  # Only include posts with title and date
                    all_posts.append({
                        'path': post.path,
                        'meta': meta
                    })
            except Exception as e:
                logger.error(f"Error processing post at startup: {e}")
        
        logger.info(f"Number of valid posts at startup: {len(all_posts)}")
        for post in all_posts:
            logger.info(f"Post at startup: {post}")
    except Exception as e:
        logger.error(f"Error loading posts at startup: {e}")
    
    app.run(debug=True) 