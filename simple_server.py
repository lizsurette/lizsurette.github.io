#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add cache-control headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    # Change to the _site directory
    os.chdir('_site')
    
    # Start the server
    port = 8000
    print(f"Starting server with no-cache headers on port {port}...")
    print("Visit http://localhost:8000 to view the site")
    print("Press Ctrl+C to stop the server")
    
    httpd = HTTPServer(('localhost', port), NoCacheHandler)
    httpd.serve_forever() 