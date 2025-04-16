#!/usr/bin/env python3
"""
Deployment script for lizsurette.github.io
This script handles building and deploying the site to GitHub Pages.
"""

import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path
import re
import logging
import markdown
import yaml
from datetime import datetime

def build_site():
    """Build the static site."""
    print("Building static site...")
    
    # Clean _site directory if it exists
    if os.path.exists("_site"):
        shutil.rmtree("_site")
    
    # Create _site directory
    os.makedirs("_site", exist_ok=True)
    
    # Copy app/static to _site/static
    if os.path.exists("app/static"):
        shutil.copytree("app/static", "_site/static", dirs_exist_ok=True)
    
    # Copy root static files if they exist
    if os.path.exists("static"):
        for item in os.listdir("static"):
            src = os.path.join("static", item)
            dst = os.path.join("_site/static", item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
    
    # Copy CSS files from app directory
    for css_file in os.listdir("app/static/css"):
        if css_file.endswith(".css"):
            src = os.path.join("app/static/css", css_file)
            dst = os.path.join("_site/static/css", css_file)
            shutil.copy2(src, dst)
            print(f"Copying {src} to {dst}")
    
    # Copy JS files from app directory
    for js_file in os.listdir("app/static/js"):
        if js_file.endswith(".js"):
            src = os.path.join("app/static/js", js_file)
            dst = os.path.join("_site/static/js", js_file)
            shutil.copy2(src, dst)
            print(f"Copying {src} to {dst}")
    
    # Copy HTML files from app directory
    for html_file in os.listdir("app/templates"):
        if html_file.endswith(".html"):
            src = os.path.join("app/templates", html_file)
            dst = os.path.join("_site", html_file)
            shutil.copy2(src, dst)
            print(f"Writing {dst} with fixed paths")
    
    # Process markdown files
    if os.path.exists("app/posts"):
        # Create posts directory
        os.makedirs("_site/posts", exist_ok=True)
        
        # Get all markdown files
        markdown_files = [f for f in os.listdir("app/posts") if f.endswith(".markdown")]
        
        # Create a list of posts for the writings page
        posts = []
        
        for md_file in markdown_files:
            # Extract post path (filename without extension)
            post_path = os.path.splitext(md_file)[0]
            
            # Read markdown content
            with open(os.path.join("app/posts", md_file), 'r') as f:
                content = f.read()
            
            # Split front matter and content
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1]
                markdown_content = parts[2]
                
                # Parse front matter
                meta = yaml.safe_load(front_matter)
                
                # Add to posts list
                posts.append({
                    'path': post_path,
                    'meta': meta,
                    'content': markdown_content
                })
                
                # Convert markdown to HTML
                html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'codehilite'])
                
                # Create HTML file
                post_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta.get('title', 'Post')} - Liz Blanchard</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/font-awesome.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/syntax.css">
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-8 col-md-offset-2">
                <article class="post">
                    <header class="post-header">
                        <h1>{meta.get('title', 'Post')}</h1>
                        <div class="post-meta">
                            <span class="post-date">{meta.get('date', '')}</span>
                        </div>
                    </header>
                    <div class="post-content">
                        {html_content}
                    </div>
                </article>
                <div class="post-navigation">
                    <a href="/writings.html" class="btn btn-default">Back to Writings</a>
                </div>
            </div>
        </div>
    </div>
    <script src="/static/js/jquery-1.11.0.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>"""
                
                # Write HTML file
                with open(os.path.join("_site/posts", f"{post_path}.html"), 'w') as f:
                    f.write(post_html)
                
                print(f"Created HTML file for {post_path}")
        
        # Create writings.html with post list
        writings_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Writings - Liz Blanchard</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/font-awesome.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-8 col-md-offset-2">
                <article class="post">
                    <header class="page-header">
                        <h1>Writings</h1>
                    </header>
                    <div class="post-content">
                        <ul class="posts">
"""
        
        # Sort posts by date (newest first)
        posts.sort(key=lambda x: x['meta'].get('date', ''), reverse=True)
        
        for post in posts:
            date_str = post['meta'].get('date', '')
            title = post['meta'].get('title', 'Untitled')
            path = post['path']
            
            writings_html += f"""                            <li class="post-item">
                                <i><span>{date_str}</span></i> &raquo; 
                                <a href="/posts/{path}.html">{title}</a>
                            </li>
"""
        
        writings_html += """                        </ul>
                    </div>
                </article>
            </div>
        </div>
    </div>
    <script src="/static/js/jquery-1.11.0.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>"""
        
        # Write writings.html
        with open(os.path.join("_site", "writings.html"), 'w') as f:
            f.write(writings_html)
        
        print("Created writings.html with post list")
    
    print("Static site built successfully!")

def deploy_to_github_pages():
    """Deploy the built site to GitHub Pages"""
    print("Deploying to GitHub Pages...")
    
    # Make sure we're on main branch
    run_command("git checkout main")
    
    # Build the site
    build_site()
    
    # Create a new orphan branch for gh-pages
    run_command("git checkout --orphan gh-pages-temp")
    
    # Clean the new branch
    for item in os.listdir("."):
        if item != ".git" and item != "_site":
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    # Copy built site
    for item in os.listdir("_site"):
        src = os.path.join("_site", item)
        if os.path.isdir(src):
            shutil.copytree(src, item, dirs_exist_ok=True)
        else:
            shutil.copy2(src, item)
    
    # Remove _site directory
    shutil.rmtree("_site")
    
    # Commit changes
    run_command('git add .')
    run_command('git commit -m "Deploy to GitHub Pages"')
    
    # Delete the old gh-pages branch locally and remotely
    run_command("git branch -D gh-pages")
    run_command("git push origin --delete gh-pages")
    
    # Rename the temporary branch to gh-pages
    run_command("git branch -m gh-pages")
    
    # Push the new gh-pages branch
    run_command("git push -f origin gh-pages")
    
    # Switch back to main
    run_command("git checkout main")
    
    print("Deployment to GitHub Pages completed successfully!")

def serve_locally():
    """Serve the site locally for testing."""
    print("Serving site locally...")
    
    # Check if _site directory exists
    if not os.path.exists("_site"):
        print("Error: _site directory does not exist. Please build the site first.")
        return
    
    # Change to _site directory
    os.chdir("_site")
    
    # Start a simple HTTP server
    print("Starting server at http://localhost:8081")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(["python", "-m", "http.server", "8081"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
    finally:
        # Change back to the original directory
        os.chdir("..")

def update_static_paths(html_content, is_root=False):
    """Update static file paths in HTML content to be relative"""
    # Handle both Flask url_for generated paths and direct paths
    replacements = [
        ('href="/static/', 'href="static/' if is_root else 'href="../static/'),
        ('src="/static/', 'src="static/' if is_root else 'src="../static/'),
        ('href="static/', 'href="static/' if is_root else 'href="../static/'),
        ('src="static/', 'src="static/' if is_root else 'src="../static/'),
        ('href="./static/', 'href="static/' if is_root else 'href="../static/'),
        ('src="./static/', 'src="static/' if is_root else 'src="../static/'),
    ]
    
    # Update navigation links to be relative
    replacements.extend([
        ('href="/writings"', 'href="writings"' if is_root else 'href="../writings"'),
        ('href="/projects"', 'href="projects"' if is_root else 'href="../projects"'),
        ('href="/games"', 'href="games"' if is_root else 'href="../games"'),
        ('href="/apps"', 'href="apps"' if is_root else 'href="../apps"'),
        ('href="/"', 'href="."' if is_root else 'href="../"'),
        ('href="./"', 'href="."' if is_root else 'href="../"'),
    ])
    
    # Update post links to be relative
    for old, new in replacements:
        html_content = html_content.replace(old, new)
    
    return html_content

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy lizsurette.github.io to GitHub Pages")
    parser.add_argument("--build", action="store_true", help="Build the static site")
    parser.add_argument("--deploy", action="store_true", help="Deploy to GitHub Pages")
    parser.add_argument("--serve", action="store_true", help="Serve the site locally")
    parser.add_argument("--all", action="store_true", help="Build, deploy, and serve the site")
    
    args = parser.parse_args()
    
    if args.all:
        build_site()
        deploy_to_github_pages()
        serve_locally()
    else:
        if args.build:
            build_site()
        if args.deploy:
            deploy_to_github_pages()
        if args.serve:
            serve_locally()
        
        if not (args.build or args.deploy or args.serve):
            parser.print_help()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--build":
            build_site()
        elif sys.argv[1] == "--deploy":
            deploy_to_github_pages()
        elif sys.argv[1] == "--build-deploy":
            deploy_to_github_pages()
    else:
        print("Usage: python deploy.py [--build|--deploy|--build-deploy]")
        sys.exit(1) 