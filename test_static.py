import os
import http.server
import socketserver
import webbrowser
import time

def serve_static_site():
    """Serve the static site locally for testing."""
    # Change to the _site directory
    os.chdir('_site')
    
    # Set up the server
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving static site at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        
        # Open the browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        # Start the server
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == '__main__':
    # Check if _site directory exists
    if not os.path.exists('_site'):
        print("Error: _site directory not found. Run build_static.py first.")
        exit(1)
    
    # Serve the static site
    serve_static_site() 