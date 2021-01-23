"""Serve a local directory via a SimpleHTTPRequestHandler

This can be useful for testing the react frontend against
a local spider run.

Usage:
    python server.py <spider_output_directory> <port>
"""

import argparse
import socketserver
from http.server import SimpleHTTPRequestHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    directory = args.directory
    port = args.port

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def end_headers(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            SimpleHTTPRequestHandler.end_headers(self)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = "http://localhost:{}".format(port)
        print("Serving directory '{}' at: {}".format(directory, url))
        httpd.serve_forever()
