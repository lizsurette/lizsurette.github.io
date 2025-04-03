#!/bin/bash

# Check if there are any changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit."
    exit 0
fi

# Ask for a commit message
echo "Enter a commit message:"
read commit_message

# If no commit message was provided, use a default
if [ -z "$commit_message" ]; then
    commit_message="Update website"
fi

# Add all changes
git add .

# Commit changes
git commit -m "$commit_message"

# Push changes to GitHub
echo "Pushing changes to GitHub..."
git push origin main

echo "Changes pushed successfully!"
echo "The site will be automatically deployed to GitHub Pages." 