from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

import requests

class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def send_post_request(data):
    r = requests.post('http://127.0.0.1:8002', data)
    print(r.text)


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    #GET
    def do_GET(self):
        # Send response
        self.send_response(200)
        
        self.send_header('Context-type','text/html')
        self.end_headers()


        # Send message back
        message = "Hello"

        self.wfile.write(bytes(message.encode()))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        new_cipher2 = AESCipher(key='mykey2')
        decrypted2 = new_cipher2.decrypt(body)
        print(" Decryption Layer 2: ", decrypted2, '\n')
        message = bytes(decrypted2, 'utf-8')
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(message)
     #   response.write(decrypted)
        self.wfile.write(response.getvalue())
        send_post_request(message)



def run():
    print('starting server...')
    server_address = ('localhost', 8001)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


   
if __name__ == '__main__':
    run()
   
   
