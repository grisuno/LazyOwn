"""
main.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: LazyOwn HoneyPot

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import socket
import paramiko
import threading
import logging
import os
import time
import json
import argparse
from scapy.all import sniff, IP, TCP
import smtplib
from email.mime.text import MIMEText

def parse_args():
    parser = argparse.ArgumentParser(description='SSH Honeypot')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='IP address to bind the honeypot')
    parser.add_argument('--port', type=int, default=2222, help='Port to bind the honeypot')
    parser.add_argument('--downloads_dir', type=str, default='downloads', help='Directory to save downloaded files')
    parser.add_argument('--log_file', type=str, default='honeypot.log', help='Log file path')
    parser.add_argument('--commands_log', type=str, default='commands.log', help='Commands log file path')
    parser.add_argument('--downloads_log', type=str, default='downloads.log', help='Downloads log file path')
    parser.add_argument('--smtp_server', type=str, default='smtp.gmail.com', help='SMTP server for sending alerts')
    parser.add_argument('--smtp_port', type=int, default=587, help='SMTP server port')
    parser.add_argument('--email_from', type=str, required=True, help='Email address to send alerts from')
    parser.add_argument('--email_to', type=str, required=True, help='Email address to send alerts to')
    parser.add_argument('--email_subject', type=str, default='Honeypot Alert', help='Subject of alert emails')
    parser.add_argument('--email_username', type=str, required=True, help='Username for the SMTP server')
    parser.add_argument('--email_password', type=str, required=True, help='Password for the SMTP server')
    return parser.parse_args()

# Configuración de registro
def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Generar la clave RSA si no existe
def generate_rsa_key(key_filename):
    if not os.path.exists(key_filename):
        os.system(f'ssh-keygen -t rsa -b 2048 -f {key_filename} -N ""')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logging.info(f"Login attempt with username: {username} and password: {password}")
        alert_admin(f"Login attempt with username: {username} and password: {password}")
        return paramiko.AUTH_FAILED

def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)
        
        server = Server()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            logging.error("SSH negotiation failed")
            return
        
        chan = transport.accept(20)
        if chan is None:
            logging.error("No channel")
            return

        chan.send("Welcome to the SSH honeypot!\n")
        
        while True:
            command = chan.recv(1024).decode('utf-8')
            if not command:
                break
            logging.info(f"Command received: {command}")
            log_command(command, commands_log)
            chan.send(f"Command '{command}' received.\n")
            
            if command.startswith('wget') or command.startswith('curl'):
                handle_file_download(command, downloads_dir, downloads_log)
            
        chan.close()
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
    finally:
        client_socket.close()

def handle_file_download(command, downloads_dir, downloads_log):
    try:
        if 'wget' in command:
            url = command.split(' ')[1]
        elif 'curl' in command:
            url = command.split(' ')[2]
        
        filename = url.split('/')[-1]
        os.system(f"wget {url} -O {downloads_dir}/{filename}")
        logging.info(f"File downloaded: {filename}")
        log_downloaded_file(filename, url, downloads_log)
    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")

def log_command(command, commands_log):
    with open(commands_log, 'a') as f:
        f.write(f"{time.ctime()} - Command: {command}\n")

def log_downloaded_file(filename, url, downloads_log):
    with open(downloads_log, 'a') as f:
        f.write(f"{time.ctime()} - File: {filename}, URL: {url}\n")

def analyze_traffic():
    def process_packet(packet):
        if packet.haslayer(TCP) and packet.haslayer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            logging.info(f"Traffic - SRC: {ip_src}:{tcp_sport} DST: {ip_dst}:{tcp_dport}")
    
    sniff(prn=process_packet, filter="tcp", store=0)

def alert_admin(message):
    args = parse_args()
    try:
        msg = MIMEText(message)
        msg['Subject'] = args.email_subject
        msg['From'] = args.email_from
        msg['To'] = args.email_to
        
        server = smtplib.SMTP(args.smtp_server, args.smtp_port)
        server.starttls()
        server.login(args.email_username, args.email_password)
        server.sendmail(args.email_from, [args.email_to], msg.as_string())
        server.quit()
        
        logging.info(f"Alert sent: {message}")
    except Exception as e:
        logging.error(f"Failed to send alert: {str(e)}")

def main():
    args = parse_args()

    setup_logging(args.log_file)
    generate_rsa_key('test_rsa.key')
    host_key = paramiko.RSAKey(filename='test_rsa.key')

    if not os.path.exists(args.downloads_dir):
        os.makedirs(args.downloads_dir)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((args.host, args.port))
    server.listen(100)
    
    logging.info("Honeypot started and listening for connections...")
    
    threading.Thread(target=analyze_traffic, daemon=True).start()
    
    while True:
        client_socket, addr = server.accept()
        logging.info(f"Connection from {addr}")
        threading.Thread(target=handle_connection, args=(client_socket, host_key, args.commands_log, args.downloads_log, args.downloads_dir)).start()

if __name__ == "__main__":
    BANNER = """
    ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
    ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
    ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
    ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
    [*] Iniciando: LazyOwn Honeypot [;,;]
    """
    print(BANNER)    
    main()
