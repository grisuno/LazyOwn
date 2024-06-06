import os
import sys
import time
import signal
from scapy.all import *
from impacket.nmb import NetBIOS, NetBIOSError
from scapy.layers.netbios import NBNSQueryRequest, NBNSQueryResponse

def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()
# Manejar la interrupción de Ctrl+C
def signal_handler(sig, frame):
    print('\n [->] Ataque interrumpido.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Función para escanear NetBIOS y obtener nombres de host
def scan_netbios(ip_range):
    netbios = NetBIOS()
    for ip in ip_range:
        try:
            name = netbios.getnodestatus(ip)
            if name:
                print(f"[+] NetBIOS Name for {ip}: {name}")
        except NetBIOSError as e:
            print(f"[-] Error scanning {ip}: {e}")
        except Exception as e:
            print(f"[-] Unexpected error scanning {ip}: {e}")

# Función para enviar un paquete ARP y verificar la respuesta
def check_arp(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answered_list:
        for element in answered_list:
            print(f"[+] ARP Response from {element[1].psrc}: {element[1].hwsrc}")
    else:
        print(f"[-] No ARP response from {ip}")

# Función para enviar una consulta NetBIOS y verificar la respuesta
def check_netbios(ip):
    packet = IP(dst=ip)/UDP(dport=137)/NBNSQueryRequest(QUESTION_NAME=b'*' + b'\x00'*15, QUESTION_TYPE=0x0020, QUESTION_CLASS=0x0001)
    response = sr1(packet, timeout=2, verbose=False)
    if response and response.haslayer(NBNSQueryResponse):
        nbns_response = response.getlayer(NBNSQueryResponse)
        for rr in nbns_response.an:
            print(f"[+] NetBIOS Response from {ip}:")
            print(f"    NAME: {rr.RR_NAME.decode().strip()}")
            print(f"    TYPE: {rr.RR_TYPE}")
            print(f"    CLASS: {rr.RR_CLASS}")
            print(f"    TTL: {rr.TTL}")
            print(f"    LENGTH: {rr.RDLENGTH}")
            print(f"    ADDR: {rr.RDATA}")
    else:
        print(f"[-] No NetBIOS response from {ip}")

# Función para generar un rango de IPs
def generate_ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    temp = start[:]
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        temp[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range

# Main function
if __name__ == "__main__":
    BANNER = """
    ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
    ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
    ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
    ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
    [*] Iniciando: LazyNetBios Atack [;,;]
    """    
    print(BANNER)       
    time.sleep(2)
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_ip> <end_ip>")
        sys.exit(1)

    start_ip = sys.argv[1]
    end_ip = sys.argv[2]

    ip_range = generate_ip_range(start_ip, end_ip)

    print("[*] Scanning NetBIOS...")
    scan_netbios(ip_range)

    for ip in ip_range:
        print(f"[*] Checking {ip}...")
        check_arp(ip)
        check_netbios(ip)
