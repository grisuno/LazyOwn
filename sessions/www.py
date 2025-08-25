# www.py - Versión corregida
import http.server
import ssl
import sys
import os
import threading
import socket

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        try:
            super().end_headers()
        except (BrokenPipeError, ConnectionResetError):
            # Cliente cerró la conexión, no es error
            pass

    def finish(self):
        try:
            super().finish()
        except (BrokenPipeError, ConnectionResetError):
            pass

class SilentHTTPServer(http.server.HTTPServer):
    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (BrokenPipeError, ConnectionResetError, socket.error)):
            pass  # Silencia errores comunes de red
        else:
            super().handle_error(request, client_address)

def configure_ssl_context(certfile, keyfile, cafile=None, capath=None):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    if cafile or capath:
        context.verify_mode = ssl.CERT_REQUIRED
        if cafile:
            context.load_verify_locations(cafile=cafile)
        if capath:
            context.load_verify_locations(capath=capath)

    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    context.options |= ssl.OP_NO_COMPRESSION
    context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DH:!RC4')
    return context

def run_server(port, use_ssl=False, certfile=None, keyfile=None):
    server_address = ('', port)
    httpd = SilentHTTPServer(server_address, SimpleHTTPRequestHandler)
    
    if use_ssl:
        context = configure_ssl_context(certfile=certfile, keyfile=keyfile)
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