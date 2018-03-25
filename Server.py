from http.server import HTTPServer, BaseHTTPRequestHandler

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    #GET
    def do_GET(self):
        # Send response
        self.send_response(200)
        
        self.send_header('Context-type','text/html')
        self.end_headers()


        # Send message back
        message = "Hello"

        self.wfile.write(bytes(message, "utf8"))
        return

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



def run():
    print('starting server...')
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
   
if __name__ == '__main__':
    run()

