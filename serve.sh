#!/bin/bash

# Check if the static site exists
if [ ! -d "_site" ]; then
    echo "Static site not found. Generating it now..."
    ./deploy.sh
fi

# Start a simple HTTP server to test the static site
echo "Starting HTTP server to test the static site..."
echo "Visit http://localhost:8000 to view the site"
echo "Press Ctrl+C to stop the server"

cd _site
python -m http.server 8000 