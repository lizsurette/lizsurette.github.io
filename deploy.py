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

def run_command(command, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        sys.exit(1)

def build_site():
    """Build the static site using Flask."""
    logger.info("Building static site...")
    
    # Create _site directory if it doesn't exist
    if os.path.exists("_site"):
        shutil.rmtree("_site")
    os.makedirs("_site")
    
    # Copy static files
    if os.path.exists("app/static"):
        shutil.copytree("app/static", "_site/static", dirs_exist_ok=True)
    
    # Run Flask app to generate HTML files
    env = os.environ.copy()
    env["FLASK_APP"] = "app.py"
    env["FLASK_ENV"] = "production"
    run_command("flask build", env=env)
    
    logger.info("Static site built successfully!")

def deploy_to_github_pages():
    """Deploy the built site to GitHub Pages."""
    logger.info("Deploying to GitHub Pages...")
    
    # Create a temporary branch for deployment
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_branch = f"gh-pages-{timestamp}"
    
    try:
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
        
    finally:
        # Clean up
        run_command("git checkout main")
        run_command(f"git branch -D {temp_branch}")

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
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        logger.error("Please specify --build, --deploy, or --build --deploy")
        sys.exit(1)
    
    args = sys.argv[1:]
    
    if "--build" in args:
        build_site()
    
    if "--deploy" in args:
        deploy_to_github_pages()

if __name__ == "__main__":
    main() 