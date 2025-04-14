#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def main():
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
    
    # Copy all HTML files
    for html_file in Path(".").glob("**/*.html"):
        if "_site" in str(html_file):
            continue
        rel_path = html_file.parent.relative_to(".")
        dest = Path("_site") / rel_path / html_file.name
        os.makedirs(dest.parent, exist_ok=True)
        if html_file != dest:
            print(f"Copying {html_file} to {dest}")
            shutil.copy2(html_file, dest)
    
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
    important_dirs = ["app", "games", "factory", "snake", "hangman", "strands", "survival", "bubble", "maze", "gem-miner", "sudoku"]
    for dir_name in important_dirs:
        if os.path.exists(dir_name) and dir_name != "_site":
            src_dir = Path(dir_name)
            dest_dir = Path("_site") / dir_name
            if not os.path.exists(dest_dir):
                print(f"Copying directory {src_dir} to {dest_dir}")
                shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    
    print("Static site built successfully!")

if __name__ == "__main__":
    main() 