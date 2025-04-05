#!/bin/bash

# Kill any existing Python HTTP server processes
pkill -f "python -m http.server"
pkill -f "dev_server.py"

echo "Starting development server..."
echo "Visit http://localhost:8000 to view the site"
echo "Press Ctrl+C to stop the server"

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Make the dev server executable
chmod +x dev_server.py

# Start the development server directly (not in background)
python3 dev_server.py 