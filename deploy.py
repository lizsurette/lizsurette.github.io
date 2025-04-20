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
    logging.info("Building static site...")
    
    # Import build_static here to avoid circular imports
    from build_static import generate_static_files, clean_site_directory, copy_static_assets
    
    # Clean and prepare _site directory
    clean_site_directory()
    
    # Debug: Check if _site directory exists
    if os.path.exists("_site"):
        logging.info("_site directory exists after cleaning")
    else:
        logging.error("_site directory does not exist after cleaning")
    
    # Copy static assets
    copy_static_assets()
    
    # Debug: Check if _site directory exists after copying static assets
    if os.path.exists("_site"):
        logging.info("_site directory exists after copying static assets")
        logging.info(f"Contents: {os.listdir('_site')}")
    else:
        logging.error("_site directory does not exist after copying static assets")
    
    # Generate static files
    generate_static_files()
    
    # Debug: Check if _site directory exists after generating static files
    if os.path.exists("_site"):
        logging.info("_site directory exists after generating static files")
        logging.info(f"Contents: {os.listdir('_site')}")
    else:
        logging.error("_site directory does not exist after generating static files")
    
    # Copy any additional directories needed (only non-game directories)
    for directory in ['posts', 'survival']:
        if os.path.exists(directory):
            shutil.copytree(directory, f'_site/{directory}', dirs_exist_ok=True)
    
    logging.info("Static site built successfully.")
    return True

def deploy_to_github_pages():
    """Deploy the built site to GitHub Pages."""
    logger.info("Deploying to GitHub Pages...")
    
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    # Store the current branch name for recovery
    current_branch = None
    try:
        # Get current branch name
        current_branch = run_command("git rev-parse --abbrev-ref HEAD").strip()
        logger.info(f"Current branch: {current_branch}")
        
        # Check for uncommitted changes
        status = run_command("git status --porcelain")
        if status:
            logger.warning("You have uncommitted changes. These will be stashed.")
            run_command("git stash save 'Auto-stashed by deploy script'")
        
        # Always rebuild the site before deploying
        build_site()
        
        # Verify _site directory exists and has content
        if not os.path.exists("_site"):
            raise FileNotFoundError("_site directory not found after building")
        if not os.listdir("_site"):
            raise FileNotFoundError("_site directory is empty after building")
        
        # Debug: List contents of _site directory
        logger.info("Contents of _site directory:")
        for item in os.listdir("_site"):
            logger.info(f"  - {item}")
        
        # Create a temporary branch for deployment
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        temp_branch = f"gh-pages-{timestamp}"
        
        # Create and switch to temporary branch
        run_command(f"git checkout --orphan {temp_branch}")
        
        # Create a temporary directory to store _site contents
        temp_dir = "temp_site"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Copy _site contents to temporary directory
        for item in os.listdir("_site"):
            src = os.path.join("_site", item)
            dst = os.path.join(temp_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        logger.info(f"Copied _site contents to {temp_dir}")
        logger.info(f"Contents of {temp_dir}: {os.listdir(temp_dir)}")
        
        # Remove everything except _site
        run_command("git rm -rf .")
        run_command("git clean -fxd")
        logger.info("Removed everything from git")
        
        # Check if temp_dir still exists
        if os.path.exists(temp_dir):
            logger.info(f"{temp_dir} still exists after git clean")
        else:
            logger.error(f"{temp_dir} was removed by git clean")
            # Recreate the temporary directory
            os.makedirs(temp_dir)
            logger.info(f"Recreated {temp_dir}")
            
            # Copy _site contents to temporary directory again
            for item in os.listdir("_site"):
                src = os.path.join("_site", item)
                dst = os.path.join(temp_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            logger.info(f"Copied _site contents to {temp_dir} again")
        
        # Copy temporary directory contents to root
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = item
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        logger.info("Copied temporary directory contents to root")
        
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
        try:
            # Return to the original branch
            run_command(f"git checkout {current_branch}")
            logger.info(f"Returned to branch: {current_branch}")
            
            # Delete the temporary branch
            run_command(f"git branch -D {temp_branch}")
            logger.info(f"Deleted temporary branch: {temp_branch}")
            
            # Apply stashed changes if any
            if status:
                run_command("git stash pop")
                logger.info("Applied stashed changes")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            logger.error("You may need to manually restore your branch")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        # Try to recover the original branch
        if current_branch:
            try:
                run_command(f"git checkout {current_branch}")
                logger.info(f"Recovered to branch: {current_branch}")
            except:
                logger.error("Failed to recover original branch. Please check your git status.")
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