import http.server
import socketserver
from pathlib import Path


def main():
    root = Path(__file__).parent.resolve()
    handler = http.server.SimpleHTTPRequestHandler
    # Change working directory so files serve from frontend/
    import os

    os.chdir(root)
    with socketserver.TCPServer(("0.0.0.0", 8080), handler) as httpd:
        print("Serving frontend on http://localhost:8080")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
