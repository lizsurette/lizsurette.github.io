#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import os

class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add cache-control headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Log the request
        print(f"GET {self.path}")
        
        # Check if the file exists
        file_path = self.translate_path(self.path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # File exists, serve it
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            # File doesn't exist, return 404
            self.send_error(404, "File not found")
            return

if __name__ == '__main__':
    port = 8000
    print(f"Starting development server on port {port}...")
    print("Visit http://localhost:8000 to view the site")
    print("Press Ctrl+C to stop the server")
    
    # Change to the _site directory if it exists, otherwise use current directory
    if os.path.exists('_site'):
        os.chdir('_site')
        print("Serving from _site directory")
    else:
        print("Serving from current directory")
    
    httpd = HTTPServer(('localhost', port), NoCacheHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
        sys.exit(0) 