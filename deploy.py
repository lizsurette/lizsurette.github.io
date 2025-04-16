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
from app import create_app

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_command(command, cwd=None, env=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, env=env)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        sys.exit(1)

def build_site():
    """Build the static site."""
    logger.info("Building static site...")
    
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Create _site directory if it doesn't exist
        if not os.path.exists('_site'):
            os.makedirs('_site')
        
        # Copy static files
        if os.path.exists('app/static'):
            shutil.copytree('app/static', '_site/static', dirs_exist_ok=True)
        
        # Initialize Flask app
        app = create_app()
        app.config['SERVER_NAME'] = None  # Remove server name to prevent redirect issues
        
        with app.test_client() as client:
            with app.app_context():
                # Generate index page
                response = client.get('/')
                with open('_site/index.html', 'wb') as f:
                    f.write(response.data)
                
                # Generate writings page
                os.makedirs('_site/writings', exist_ok=True)
                response = client.get('/writings')
                with open('_site/writings/index.html', 'wb') as f:
                    f.write(response.data)
                
                # Generate apps page
                os.makedirs('_site/apps', exist_ok=True)
                response = client.get('/apps')
                with open('_site/apps/index.html', 'wb') as f:
                    f.write(response.data)
                
                # Generate projects page
                os.makedirs('_site/projects', exist_ok=True)
                response = client.get('/projects')
                with open('_site/projects/index.html', 'wb') as f:
                    f.write(response.data)
                
                # Generate games page
                os.makedirs('_site/games', exist_ok=True)
                response = client.get('/games')
                with open('_site/games/index.html', 'wb') as f:
                    f.write(response.data)
                
                # Copy game directories
                for game_dir in ['bubble', 'factory', 'hangman', 'maze', 'snake', 'strands', 'sudoku']:
                    if os.path.exists(f'app/templates/{game_dir}'):
                        shutil.copytree(f'app/templates/{game_dir}', f'_site/{game_dir}', dirs_exist_ok=True)
                
                # Generate post pages
                posts_dir = os.path.join('app', 'posts')
                if os.path.exists(posts_dir):
                    for post_file in os.listdir(posts_dir):
                        if post_file.endswith('.md'):
                            post_name = os.path.splitext(post_file)[0]
                            os.makedirs(f'_site/posts/{post_name}', exist_ok=True)
                            response = client.get(f'/posts/{post_name}')
                            with open(f'_site/posts/{post_name}/index.html', 'wb') as f:
                                f.write(response.data)
                
                # Generate category pages
                categories = ['kubernetes', 'openshift', 'python', 'web-development']
                for category in categories:
                    os.makedirs(f'_site/category/{category}', exist_ok=True)
                    response = client.get(f'/category/{category}')
                    with open(f'_site/category/{category}/index.html', 'wb') as f:
                        f.write(response.data)
                
                # Generate error pages
                response = client.get('/error')
                with open('_site/error.html', 'wb') as f:
                    f.write(response.data)
                
                # Update URLs in all HTML files
                for root, dirs, files in os.walk('_site'):
                    for file in files:
                        if file.endswith('.html'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Calculate relative path to root
                            rel_path = os.path.relpath(root, '_site')
                            if rel_path == '.':
                                prefix = ''
                            else:
                                prefix = '../' * (len(rel_path.split(os.sep)))
                            
                            # Update static file paths
                            content = content.replace('href="/static/', f'href="{prefix}static/')
                            content = content.replace('src="/static/', f'src="{prefix}static/')
                            
                            # Update navigation links
                            content = content.replace('href="/"', f'href="{prefix}"')
                            content = content.replace('href="/writings/"', f'href="{prefix}writings/"')
                            content = content.replace('href="/games/"', f'href="{prefix}games/"')
                            content = content.replace('href="/projects/"', f'href="{prefix}projects/"')
                            content = content.replace('href="/apps/"', f'href="{prefix}apps/"')
                            
                            # Update post links
                            content = content.replace('href="/posts/', f'href="{prefix}posts/')
                            
                            # Update category links
                            content = content.replace('href="/category/', f'href="{prefix}category/')
                            
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
        
        logger.info("Static site built successfully!")
        return original_dir
    except Exception as e:
        logger.error(f"Error building site: {str(e)}")
        raise

def deploy_to_github_pages():
    """Deploy the built site to GitHub Pages."""
    logger.info("Deploying to GitHub Pages...")
    
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Always rebuild the site before deploying
        build_site()
        
        # Verify _site directory exists and has content
        if not os.path.exists("_site"):
            raise FileNotFoundError("_site directory not found after building")
        if not os.listdir("_site"):
            raise FileNotFoundError("_site directory is empty after building")
        
        # Create a temporary branch for deployment
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        temp_branch = f"gh-pages-{timestamp}"
        
        # Create and switch to temporary branch
        run_command(f"git checkout --orphan {temp_branch}")
        
        # Remove everything except _site
        run_command("git rm -rf .")
        run_command("git clean -fxd")
        
        # Copy _site contents to root
        for item in os.listdir("_site"):
            src = os.path.join("_site", item)
            dst = item
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        # Add .nojekyll file
        with open(".nojekyll", "w") as f:
            pass
        
        # Commit changes
        run_command("git add .")
        run_command('git commit -m "Deploy site"')
        
        # Push to gh-pages branch
        run_command("git push origin HEAD:gh-pages --force")
        
        logger.info("Site deployed successfully!")
        
        # Clean up
        run_command("git checkout main")
        try:
            run_command(f"git branch -D {temp_branch}")
        except:
            # Ignore errors if the branch doesn't exist
            pass
    finally:
        # Always change back to the original directory
        os.chdir(original_dir)

def serve_locally():
    """Serve the site locally for testing."""
    print("Serving site locally...")
    
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
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
            subprocess.run(["python", "-m", "http.server", "8081"])
        except KeyboardInterrupt:
            print("\nServer stopped.")
    finally:
        # Always change back to the original directory
        os.chdir(original_dir)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Build and deploy the site to GitHub Pages.")
    parser.add_argument("--build", action="store_true", help="Build the static site")
    parser.add_argument("--deploy", action="store_true", help="Deploy the site to GitHub Pages")
    parser.add_argument("--serve", action="store_true", help="Serve the site locally")
    
    args = parser.parse_args()
    
    if args.build:
        build_site()
    elif args.deploy:
        deploy_to_github_pages()
    elif args.serve:
        serve_locally()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 