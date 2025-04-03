from flask import Flask
from flask_flatpages import FlatPages
import os

# Get the absolute path to the app directory
app_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = os.path.join(app_dir, 'app', 'posts')
pages = FlatPages(app)

# Print the posts directory path
print(f"Posts directory: {app.config['FLATPAGES_ROOT']}")
print(f"Directory exists: {os.path.exists(app.config['FLATPAGES_ROOT'])}")

# Get all posts
posts = [p for p in pages]

# Print the number of posts and their details
print(f"Number of posts: {len(posts)}")
for post in posts:
    print(f"Post: {post.path}, Title: {post.meta.get('title')}, Date: {post.meta.get('date')}")
    print(f"Post meta: {post.meta}") 