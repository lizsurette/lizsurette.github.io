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
    
    # Create _site directory
    os.makedirs("_site", exist_ok=True)
    
    # Copy all static assets
    if os.path.exists("static"):
        shutil.copytree("static", "_site/static", dirs_exist_ok=True)
    
    # Copy all CSS files
    for css_file in Path(".").glob("**/*.css"):
        if "_site" in str(css_file):
            continue
        rel_path = css_file.parent.relative_to(".")
        dest = Path("_site") / rel_path / css_file.name
        os.makedirs(dest.parent, exist_ok=True)
        if css_file != dest:
            print(f"Copying {css_file} to {dest}")
            shutil.copy2(css_file, dest)
    
    # Copy all JS files
    for js_file in Path(".").glob("**/*.js"):
        if "_site" in str(js_file):
            continue
        rel_path = js_file.parent.relative_to(".")
        dest = Path("_site") / rel_path / js_file.name
        os.makedirs(dest.parent, exist_ok=True)
        if js_file != dest:
            print(f"Copying {js_file} to {dest}")
            shutil.copy2(js_file, dest)
    
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
    
    # Copy all image files
    for img_file in Path(".").glob("**/*.{png,jpg,jpeg,gif,svg,ico}"):
        if "_site" in str(img_file):
            continue
        rel_path = img_file.parent.relative_to(".")
        dest = Path("_site") / rel_path / img_file.name
        os.makedirs(dest.parent, exist_ok=True)
        if img_file != dest:
            print(f"Copying {img_file} to {dest}")
            shutil.copy2(img_file, dest)
    
    # Copy any other important directories
    important_dirs = ["app", "games", "gem-miner", "snake", "hangman", "strands", "survival", "bubble", "maze", "sudoku"]
    for dir_name in important_dirs:
        if os.path.exists(dir_name) and dir_name != "_site":
            src_dir = Path(dir_name)
            dest_dir = Path("_site") / dir_name
            if not os.path.exists(dest_dir):
                print(f"Copying directory {src_dir} to {dest_dir}")
                shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    
    # Create posts directory structure
    posts_dir = Path("_site") / "posts"
    os.makedirs(posts_dir, exist_ok=True)
    
    # Create a mapping of post titles to their slugs
    post_title_to_slug = {}
    
    # Get all markdown files from app/posts directory
    if os.path.exists("app/posts"):
        for post_file in Path("app/posts").glob("*.markdown"):
            # Extract post slug from filename
            post_slug = post_file.stem
            # Remove date prefix if present
            if re.match(r'^\d{4}-\d{2}-\d{2}-', post_slug):
                post_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post_slug)
            
            # Read the post file to get the title and content
            with open(post_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Split front matter and content
            _, front_matter, markdown_content = content.split("---", 2)
            metadata = yaml.safe_load(front_matter)
            post_title = metadata.get("title", "")
            post_title_to_slug[post_title] = post_slug
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
            
            # Create directory for this post
            post_dir = posts_dir / post_slug
            os.makedirs(post_dir, exist_ok=True)
            
            # Create a complete HTML file for this post
            with open(post_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post_title}</title>
    <link rel="stylesheet" href="../../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../../static/css/font-awesome.min.css">
    <link rel="stylesheet" href="../../static/css/style.css">
    <link rel="stylesheet" href="../../static/css/navigation.css">
    <link rel="stylesheet" href="../../static/css/syntax.css">
    <link rel="stylesheet" href="../../static/css/thickbox.css">
    <link rel="stylesheet" href="../../static/css/projects.css">
    <link rel="stylesheet" href="../../static/css/super-search.css">
    <link rel="stylesheet" href="../../static/css/fonts.css">
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="about">
                <!-- Social links removed from here -->
            </div>
            <hr>
            <nav class="main-nav">
                <ul>
                    <li><a href="../../">About Me</a></li>
                    <li><a href="../../writings/" class="active">Writings</a></li>
                    <li><a href="../../games/">Games</a></li>
                    <li><a href="../../projects/">Projects</a></li>
                    <li><a href="../../apps/">Apps</a></li>
                </ul>
            </nav>
        </div>
        <div class="content">
            <article class="post">
                <header class="page-header">
                    <h1>{post_title}</h1>
                </header>
                <div class="post-content">
                    {html_content}
                </div>
            </article>
        </div>
    </div>
</body>
</html>""")
    
    # Fix post URLs in writings.html
    writings_file = Path("_site") / "writings" / "index.html"
    if writings_file.exists():
        with open(writings_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create a new content with fixed URLs
        new_content = content
        
        # Find all post items
        post_items = re.finditer(r'<li class="post-item" data-title="([^"]*)" data-date="([^"]*)"[^>]*>(.*?)</li>', content, re.DOTALL)
        
        for post_item in post_items:
            post_title = post_item.group(1)
            post_date = post_item.group(2)
            post_content = post_item.group(3)
            
            # Find the corresponding slug
            if post_title in post_title_to_slug:
                post_slug = post_title_to_slug[post_title]
                
                # Create the new post item with the correct URL
                new_post_item = f'<li class="post-item" data-title="{post_title}" data-date="{post_date}">{post_content}</li>'
                new_post_item = re.sub(r'<a href="../posts//">', f'<a href="../posts/{post_slug}/">', new_post_item)
                
                # Replace the old post item with the new one
                new_content = new_content.replace(post_item.group(0), new_post_item)
        
        with open(writings_file, "w", encoding="utf-8") as f:
            f.write(new_content)
    
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