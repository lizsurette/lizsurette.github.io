#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate static site
echo "Generating static site..."
python build_static.py

# Check if the static site was generated successfully
if [ -d "_site" ]; then
    echo "Static site generated successfully!"
    echo "You can test it locally by running: python -m http.server --directory _site"
    echo "To deploy to GitHub Pages, push your changes to the main branch."
else
    echo "Error: Static site generation failed!"
    exit 1
fi

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate
fi 