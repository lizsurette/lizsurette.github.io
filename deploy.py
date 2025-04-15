#!/usr/bin/env python3
"""
Deployment script for lizsurette.github.io
This script handles building and deploying the site to GitHub Pages.
"""

import os
import shutil
import subprocess
import argparse
from pathlib import Path
import re
import logging
import markdown
import yaml

def build_site():
    """Build the static site."""
    print("Building static site...")
    
    # Clean _site directory if it exists
    if os.path.exists("_site"):
        shutil.rmtree("_site")
    
    # Create _site directory and static subdirectories
    os.makedirs("_site/static/css", exist_ok=True)
    os.makedirs("_site/static/js", exist_ok=True)
    os.makedirs("_site/static/img", exist_ok=True)
    
    # Copy all CSS files from app/static/css to _site/static/css
    if os.path.exists("app/static/css"):
        for css_file in Path("app/static/css").glob("*.css"):
            dest = Path("_site/static/css") / css_file.name
            print(f"Copying {css_file} to {dest}")
            shutil.copy2(css_file, dest)
    
    # Copy all JS files from app/static/js to _site/static/js
    if os.path.exists("app/static/js"):
        for js_file in Path("app/static/js").glob("*.js"):
            dest = Path("_site/static/js") / js_file.name
            print(f"Copying {js_file} to {dest}")
            shutil.copy2(js_file, dest)
    
    # Copy all image files from app/static/img to _site/static/img
    if os.path.exists("app/static/img"):
        for img_file in Path("app/static/img").glob("**/*.*"):
            rel_path = img_file.relative_to("app/static/img")
            dest = Path("_site/static/img") / rel_path
            os.makedirs(dest.parent, exist_ok=True)
            print(f"Copying {img_file} to {dest}")
            shutil.copy2(img_file, dest)
    
    # Copy all HTML files and fix static asset paths
    for html_file in Path(".").glob("**/*.html"):
        if "_site" in str(html_file):
            continue
        rel_path = html_file.parent.relative_to(".")
        dest = Path("_site") / rel_path / html_file.name
        os.makedirs(dest.parent, exist_ok=True)
        
        # Read the HTML file
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Calculate relative path to root
        depth = len(dest.parent.relative_to("_site").parts)
        path_to_root = "../" * depth if depth > 0 else "./"
        
        # Fix url_for references
        content = re.sub(
            r'url_for\(\'static\', filename=\'([^\']+)\'\)', 
            f'{path_to_root}static/\\1', 
            content
        )
        content = re.sub(
            r'url_for\(\'main\.([^\']+)\'\)', 
            f'{path_to_root}\\1/', 
            content
        )
        
        # Fix relative paths to static assets
        content = re.sub(
            r'(href|src)="static/',
            f'\\1="{path_to_root}static/',
            content
        )
        content = re.sub(
            r'(href|src)="/static/',
            f'\\1="{path_to_root}static/',
            content
        )
        
        # Fix navigation links
        content = re.sub(
            r'href="/([^"]+)/"',
            f'href="{path_to_root}\\1/"',
            content
        )
        
        # Fix specific game links
        content = re.sub(
            r'href="/gem-miner/"',
            f'href="{path_to_root}gem-miner/"',
            content
        )
        
        # Write the modified content
        with open(dest, "w", encoding="utf-8") as f:
            print(f"Writing {dest} with fixed paths")
            f.write(content)
    
    # Copy any other important directories
    important_dirs = ["app", "games", "gem-miner", "snake", "hangman", "strands", "survival", "bubble", "maze", "sudoku"]
    for dir_name in important_dirs:
        if os.path.exists(dir_name) and dir_name != "_site":
            src_dir = Path(dir_name)
            dest_dir = Path("_site") / dir_name
            if not os.path.exists(dest_dir):
                print(f"Copying directory {src_dir} to {dest_dir}")
                shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    
    print("Static site built successfully!")

def deploy_to_github_pages():
    """Deploy the site to GitHub Pages."""
    print("Deploying to GitHub Pages...")
    
    # Check if we're already on the gh-pages branch
    current_branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                   check=True, capture_output=True, text=True).stdout.strip()
    
    if current_branch == "gh-pages":
        print("Already on gh-pages branch. Switching to main first.")
        subprocess.run(["git", "checkout", "main"], check=True)
    
    # Create a new branch
    subprocess.run(["git", "checkout", "--orphan", "gh-pages-temp"], check=True)
    
    # Add all files
    subprocess.run(["git", "add", "-A"], check=True)
    
    # Commit changes
    subprocess.run(["git", "commit", "-m", "Deploy to GitHub Pages"], check=True)
    
    # Delete the gh-pages branch if it exists
    try:
        subprocess.run(["git", "push", "origin", "--delete", "gh-pages"], check=True)
        print("Deleted existing gh-pages branch")
    except subprocess.CalledProcessError:
        print("gh-pages branch does not exist or could not be deleted")
    
    # Rename the temporary branch to gh-pages
    subprocess.run(["git", "branch", "-m", "gh-pages"], check=True)
    
    # Push to GitHub Pages
    subprocess.run(["git", "push", "-f", "origin", "gh-pages"], check=True)
    
    # Switch back to main branch
    subprocess.run(["git", "checkout", "main"], check=True)
    
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
    main() 