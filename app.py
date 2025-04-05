from flask import Flask, render_template, url_for, abort, send_from_directory
from flask_flatpages import FlatPages
from datetime import datetime
import os
import logging
import yaml
import markdown
import shutil
import re

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

def extract_yaml_and_content(content):
    """Extract YAML front matter and content from a markdown file using regex."""
    metadata = {}
    post_content = content
    
    # Use regex to find the first YAML front matter block
    # This pattern looks for the first --- block and captures everything between the first and second ---
    pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1).strip()
        try:
            # Parse the YAML content
            metadata = yaml.safe_load(yaml_content)
            if metadata is None:
                metadata = {}
            
            # Get the rest of the content after the first YAML block
            post_content = content[match.end():].strip()
            
        except Exception as e:
            logger.error(f"YAML parsing error: {e}")
            metadata = {}
    
    return metadata, post_content

def parse_yaml(content):
    """Parse YAML front matter."""
    try:
        metadata, content = extract_yaml_and_content(content)
        return metadata, content
    except Exception as e:
        logger.error(f"Error parsing YAML: {e}")
        return {}, content

def render_markdown(text):
    """Render markdown text to HTML."""
    try:
        # Process image URLs before rendering markdown
        # Convert GitHub URLs to local static URLs
        github_pattern = r'https://github\.com/lizsurette/lizsurette\.github\.io/raw/main/static/img/_posts/([^)]+)'
        text = re.sub(github_pattern, r'/static/img/_posts/\1', text)
        
        # Also handle img tags with src attributes
        img_pattern = r'<img src="https://github\.com/lizsurette/lizsurette\.github\.io/raw/main/static/img/_posts/([^"]+)"'
        text = re.sub(img_pattern, r'<img src="/static/img/_posts/\1"', text)
        
        return markdown.markdown(
            text,
            extensions=['codehilite', 'fenced_code', 'tables', 'attr_list', 'def_list', 'abbr']
        )
    except Exception as e:
        logger.error(f"Error rendering markdown: {e}")
        return text

# Configure FlatPages with custom YAML parser and HTML renderer
app.config['FLATPAGES_HTML_RENDERER'] = render_markdown
app.config['FLATPAGES_YAML_PARSER'] = parse_yaml
pages = FlatPages(app)

def get_safe_post_meta(post):
    """Safely get post metadata"""
    try:
        # Get the raw content of the post
        raw_content = post.body
        
        # Extract YAML front matter using a more robust method
        metadata = {}
        
        # Find the first YAML block
        yaml_pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
        match = re.match(yaml_pattern, raw_content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1).strip()
            try:
                # Parse the YAML content
                metadata = yaml.safe_load(yaml_content)
                if metadata is None:
                    metadata = {}
            except Exception as e:
                logger.error(f"YAML parsing error in {post.path}: {e}")
                metadata = {}
        
        # Get and clean the title
        title = metadata.get('title', '')
        if isinstance(title, str):
            # Remove any extra quotes and whitespace
            title = title.strip().strip('"\'')
        
        # Get other metadata
        path = getattr(post, 'path', '')
        date = metadata.get('date')
        categories = metadata.get('categories', [])
        
        # Ensure we have valid data
        if not title or not date:
            logger.warning(f"Missing required metadata for post {path}")
            return None
            
        return {
            'path': path,
            'title': title,
            'date': date,
            'categories': categories
        }
    except Exception as e:
        logger.error(f"Error getting post meta: {e}")
        return None

def get_posts():
    """Get all posts with metadata"""
    try:
        posts = []
        for post in pages:
            try:
                meta = get_safe_post_meta(post)
                if meta and meta['title'] and meta['date']:  # Only include posts with title and date
                    posts.append({
                        'path': post.path,
                        'title': meta['title'],
                        'date': meta['date'],
                        'categories': meta['categories']
                    })
            except Exception as e:
                logger.error(f"Error processing post: {e}")
        
        # Sort posts by date
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts
    except Exception as e:
        logger.error(f"Error getting posts: {e}")
        return []

def get_posts_directly():
    """Get all posts by reading markdown files directly from the filesystem"""
    try:
        posts = []
        posts_dir = os.path.join(app_dir, 'app', 'posts')
        
        # Get all markdown files in the posts directory
        for filename in os.listdir(posts_dir):
            if filename.endswith('.markdown'):
                file_path = os.path.join(posts_dir, filename)
                
                try:
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract the path (filename without extension)
                    path = os.path.splitext(filename)[0]
                    
                    # Extract YAML front matter using regex
                    yaml_pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
                    match = re.match(yaml_pattern, content, re.DOTALL)
                    
                    if match:
                        yaml_content = match.group(1).strip()
                        try:
                            # Parse the YAML content
                            metadata = yaml.safe_load(yaml_content)
                            
                            # Extract required fields
                            title = metadata.get('title', '')
                            date_str = metadata.get('date', '')
                            categories = metadata.get('categories', [])
                            
                            # Clean up title
                            if isinstance(title, str):
                                title = title.strip().strip('"\'')
                            
                            # Parse date
                            try:
                                if isinstance(date_str, str):
                                    date = datetime.strptime(date_str, '%Y-%m-%d')
                                else:
                                    date = date_str
                            except ValueError:
                                logger.warning(f"Invalid date format in {path}: {date_str}")
                                continue
                            
                            # Add to posts list if we have the required fields
                            if title and date:
                                # Create a post object that matches the template's expectations
                                post_obj = {
                                    'meta': {
                                        'title': title,
                                        'date': date,
                                        'categories': categories
                                    },
                                    'path': path
                                }
                                posts.append(post_obj)
                        except Exception as e:
                            logger.error(f"Error parsing YAML in {path}: {e}")
                except Exception as e:
                    logger.error(f"Error reading file {filename}: {e}")
        
        # Sort posts by date
        posts.sort(key=lambda x: x['meta']['date'], reverse=True)
        return posts
    except Exception as e:
        logger.error(f"Error getting posts directly: {e}")
        return []

@app.route('/')
def index():
    posts = get_posts_directly()
    return render_template('index.html', title='Home', posts=posts)

@app.route('/writings/')
def writings():
    posts = get_posts_directly()
    return render_template('writings.html', title='Writings', posts=posts)

@app.route('/posts/<path:path>/')
def post(path):
    try:
        logger.debug(f"Attempting to get post: {path}")
        
        # Get the post file path
        post_file = os.path.join(app_dir, 'app', 'posts', f"{path}.markdown")
        
        if not os.path.exists(post_file):
            logger.error(f"Post file not found: {post_file}")
            return abort(404)
        
        # Read the file content
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML front matter and content
        yaml_pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
        match = re.match(yaml_pattern, content, re.DOTALL)
        
        if not match:
            logger.error(f"No YAML front matter found in {path}")
            return abort(404)
        
        yaml_content = match.group(1).strip()
        post_content = content[match.end():].strip()
        
        # Parse the YAML content
        try:
            metadata = yaml.safe_load(yaml_content)
        except Exception as e:
            logger.error(f"Error parsing YAML in {path}: {e}")
            return abort(500)
        
        # Extract required fields
        title = metadata.get('title', '')
        date_str = metadata.get('date', '')
        categories = metadata.get('categories', [])
        
        # Clean up title
        if isinstance(title, str):
            title = title.strip().strip('"\'')
        
        # Parse date
        try:
            if isinstance(date_str, str):
                date = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date = date_str
        except ValueError:
            logger.warning(f"Invalid date format in {path}: {date_str}")
            date = None
        
        # Get all posts for navigation
        all_posts = get_posts_directly()
        
        # Find current post index
        current_index = -1
        for i, p in enumerate(all_posts):
            if p['path'] == path:
                current_index = i
                break
        
        # Get next and previous posts
        next_post = all_posts[current_index - 1] if current_index > 0 else None
        prev_post = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
        
        # Create a post object that matches the template's expectations
        post_obj = {
            'meta': {
                'title': title,
                'date': date,
                'categories': categories
            },
            'content': render_markdown(post_content),
            'path': path
        }
        
        return render_template('post.html', 
                             post=post_obj,
                             next_post=next_post,
                             prev_post=prev_post)
    except Exception as e:
        logger.error(f"Error in post route: {e}")
        logger.error(f"Post path: {path}")
        return abort(404)

@app.route('/games/')
def games():
    return render_template('games.html', title='Games')

@app.route('/projects/')
def projects():
    return render_template('projects.html', title='Projects')

@app.route('/apps/')
def apps():
    return render_template('apps.html', title='AI Generated Apps')

@app.route('/grocery-list/')
def grocery_list():
    return render_template('grocery-list.html', title='Smart Grocery List')

@app.route('/snake/')
def snake():
    return render_template('snake.html', title='Snake Game')

@app.route('/hangman/')
def hangman():
    return render_template('hangman.html', title='Hangman Game')

@app.route('/strands/')
def strands():
    return render_template('strands.html', title='Strands Game')

# Add a function to copy static assets during site generation
def copy_static_assets():
    try:
        # Create _site/static directory if it doesn't exist
        site_static_dir = os.path.join('_site', 'static')
        if not os.path.exists(site_static_dir):
            os.makedirs(site_static_dir)
        
        # Copy static assets
        app_static_dir = os.path.join('app', 'static')
        if os.path.exists(app_static_dir):
            for item in os.listdir(app_static_dir):
                src = os.path.join(app_static_dir, item)
                dst = os.path.join(site_static_dir, item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
    except Exception as e:
        logger.error(f"Error copying static assets: {e}")

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
    
    # Copy static assets when running in development
    copy_static_assets()
    
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