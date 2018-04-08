from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

import requests


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    #GET
    def do_GET(self):
        # Send response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
        requests.get('http://127.0.0.1:8000')

        
httpd = HTTPServer(('localhost', 8000), testHTTPServer_RequestHandler)
httpd.serve_forever()
        