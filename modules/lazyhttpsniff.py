#!/usr/bin/env python3
# _*_ coding: utf8 _*_

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
print(BANNER)

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

def sniffer_http(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        if pkt[TCP].dport == 80 or pkt[TCP].sport == 80 or pkt[TCP].dport == 443 or pkt[TCP].sport == 443:
            data = pkt[Raw].load.decode('utf-8', errors='ignore')
            print(f"HTTP Packet: {data}")

def main():
    args = parse_arguments()
    if args.interface:
        print("[;,;] Lazy HTTP Sniffer Runing...")
        sniff(iface=args.interface, filter="tcp port 80", prn=sniffer_http)
    else:
        print("interface must be set")

if __name__ == "__main__":
    main()
