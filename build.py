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
        if html_file.name == "index.html":
            # Handle root index.html
            dest = Path("_site") / html_file.parent.name / "index.html"
        else:
            # Handle other HTML files
            dest = Path("_site") / html_file.parent.name / html_file.name
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest.parent, exist_ok=True)
        
        # Copy the file
        shutil.copy2(html_file, dest)
    
    print("Static site built successfully!")

if __name__ == "__main__":
    main() 