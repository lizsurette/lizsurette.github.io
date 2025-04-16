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
        if os.path.exists("_site"):
            shutil.rmtree("_site")
        os.makedirs("_site")
        
        # Copy static files
        if os.path.exists("app/static"):
            shutil.copytree("app/static", "_site/static", dirs_exist_ok=True)
        
        # Import Flask app here to avoid circular imports
        from app import create_app
        app = create_app()
        
        # Generate HTML files for each route
        with app.test_client() as client:
            # Generate index page
            response = client.get('/')
            with open("_site/index.html", "w") as f:
                f.write(response.data.decode())
            
            # Generate writings page
            response = client.get('/writings')
            os.makedirs("_site/writings", exist_ok=True)
            with open("_site/writings/index.html", "w") as f:
                f.write(response.data.decode())
            
            # Generate apps page
            response = client.get('/apps')
            os.makedirs("_site/apps", exist_ok=True)
            with open("_site/apps/index.html", "w") as f:
                f.write(response.data.decode())
            
            # Generate projects page
            response = client.get('/projects')
            os.makedirs("_site/projects", exist_ok=True)
            with open("_site/projects/index.html", "w") as f:
                f.write(response.data.decode())
            
            # Generate games page
            response = client.get('/games')
            os.makedirs("_site/games", exist_ok=True)
            with open("_site/games/index.html", "w") as f:
                f.write(response.data.decode())
            
            # Generate individual post pages
            from app.repositories.post_repository import PostRepository
            post_repository = PostRepository(os.path.join('app', 'posts'), app.config['FLATPAGES_HTML_RENDERER'])
            posts = post_repository.get_all_posts()
            
            for post in posts:
                post_dir = os.path.join("_site", "posts")
                os.makedirs(post_dir, exist_ok=True)
                response = client.get(f'/posts/{post.path}')
                with open(os.path.join(post_dir, f"{post.path}.html"), "w") as f:
                    f.write(response.data.decode())
        
        # Copy game directories and their assets
        game_dirs = ['snake', 'hangman', 'strands', 'maze', 'bubble', 'gem-miner', 'survival', 'sudoku']
        for game_dir in game_dirs:
            if os.path.exists(game_dir):
                # Copy the game directory
                shutil.copytree(game_dir, f"_site/{game_dir}", dirs_exist_ok=True)
                
                # Copy any static assets from the game directory
                if os.path.exists(f"{game_dir}/static"):
                    shutil.copytree(f"{game_dir}/static", f"_site/static/{game_dir}", dirs_exist_ok=True)
        
        logger.info("Static site built successfully!")
        return original_dir
    except Exception as e:
        logger.error(f"Error building site: {str(e)}")
        raise e

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