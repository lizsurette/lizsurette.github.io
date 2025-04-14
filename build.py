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
    
    # Copy static assets
    if os.path.exists("static"):
        shutil.copytree("static", "_site/static", dirs_exist_ok=True)
    
    # Copy HTML files
    for html_file in Path(".").glob("**/*.html"):
        # Skip files in _site directory
        if "_site" in str(html_file):
            continue
            
        # Calculate destination path
        if html_file.name == "index.html":
            # For index.html files, maintain directory structure
            rel_path = html_file.parent.relative_to(".")
            dest = Path("_site") / rel_path / "index.html"
        else:
            # For other HTML files, maintain directory structure
            rel_path = html_file.parent.relative_to(".")
            dest = Path("_site") / rel_path / html_file.name
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest.parent, exist_ok=True)
        
        # Only copy if source and destination are different
        if html_file != dest:
            print(f"Copying {html_file} to {dest}")
            shutil.copy2(html_file, dest)
    
    print("Static site built successfully!")

if __name__ == "__main__":
    main() 