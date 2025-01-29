import http.server
import ssl
import sys
import os
import threading

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port, use_ssl=False, certfile=None, keyfile=None):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
    if use_ssl:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: sudo python3 www.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    certfile = '../cert.pem'
    keyfile = '../key.pem'

    os.chdir(os.getcwd())

    threading.Thread(target=run_server, args=(80, False)).start()

    threading.Thread(target=run_server, args=(port, True, certfile, keyfile)).start()
