#!/usr/bin/env python3

"""
ia_network_analysis.py

Autor: grisun0
Fecha de creación: 30/01/2025
Licencia: GPL v3

Descripción: Bot de monitoreo de tráfico de red en tiempo real.
             Informa todo el tráfico (IPs, puertos, protocolos) y usa DeepSeek para detectar actividad sospechosa.
"""

import time
import json
import logging
import os
import requests
import argparse
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from scapy.layers.tls.record import TLS
from rich.console import Console
from rich.markdown import Markdown

# Configuración de logging
logging.basicConfig(filename='network_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"

console = Console()

def analyze_with_deepseek(packet_info, mode='console'):
    """
    Envía la información del paquete a DeepSeek para análisis avanzado.
    Devuelve la respuesta del modelo en chunks.
    """
    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            json={
                "model": DEEPSEEK_MODEL,
                "prompt": f"""
                Analyze the following network traffic and determine if there is suspicious activity.
                Respond with a JSON containing:
                - 'suspicious': true/false (if the activity is suspicious).
                - 'reason': a brief explanation of why it is suspicious (if applicable).
                - 'details': additional relevant information.

                Network traffic:
                {packet_info}
                """,
                "stream": True  
            },
            timeout=60,
            stream=True
        )

        if response.status_code == 200:
            full_response = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode('utf-8'))
                        chunk_response = json_chunk.get("response", "")
                        full_response += chunk_response
                        if mode == 'console':
                            console.print(chunk_response, end="")
                    except json.JSONDecodeError as e:
                        logging.error(f"Error decoding JSON: {e}")

            if mode == 'console':
                rich_markdown = Markdown(full_response)
                os.system('clear')
                console.print(rich_markdown)
            logging.info(f"DeepSeek Analysis Results:\n{full_response}")
        else:
            logging.error(f"Error communicating with DeepSeek API: {response.status_code}")
            console.print("Error communicating with DeepSeek API")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in request to DeepSeek: {e}")
        console.print("Error in request to DeepSeek")

def packet_callback(packet, mode='console'):
    """
    Callback para procesar cada paquete capturado.
    """
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = "ICMP" if ICMP in packet else "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
        packet_info = {
            "ip_src": ip_src,
            "ip_dst": ip_dst,
            "protocol": protocol,
            "details": {}
        }

        if TCP in packet:
            packet_info["details"]["src_port"] = packet[TCP].sport
            packet_info["details"]["dst_port"] = packet[TCP].dport
        elif UDP in packet:
            packet_info["details"]["src_port"] = packet[UDP].sport
            packet_info["details"]["dst_port"] = packet[UDP].dport
        elif ICMP in packet:
            packet_info["details"]["type"] = packet[ICMP].type
            packet_info["details"]["code"] = packet[ICMP].code

        if TCP in packet and Raw in packet:
            raw_data = packet[Raw].load
            if raw_data.startswith(b'\x16\x03'):  
                try:
                    tls = TLS(raw_data)
                    if hasattr(tls, 'handshake') and hasattr(tls.handshake, 'server_name'):
                        sni = tls.handshake.server_name
                        packet_info["details"]["sni"] = sni
                except Exception as e:
                    logging.error(f"Error analyzing TLS: {e}")

        logging.info(f"Traffic detected: {json.dumps(packet_info, indent=2)}")
        if mode == 'console':
            console.print(f"Traffic detected: {json.dumps(packet_info, indent=2)}")
            analyze_with_deepseek(json.dumps(packet_info, indent=2), mode)
        else:
            return json.dumps(packet_info, indent=2)

def start_monitoring(interface=None, timeout=30, mode='console'):
    """
    Inicia el monitoreo del tráfico de red.
    """
    console.print("Starting network traffic monitoring...")
    try:
        while True:
            sniff(prn=lambda packet: packet_callback(packet, mode), filter="ip", timeout=timeout, iface=interface, store=False)
            logging.info(f"Refreshing analysis... Next cycle in {timeout} seconds.")
            if mode == 'console':
                console.print(f"Refreshing analysis... Next cycle in {timeout} seconds.")
            time.sleep(timeout)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by the user.")
        if mode == 'console':
            console.print("Monitoring stopped by the user.")

def parse_args():
    parser = argparse.ArgumentParser(description='Network Monitor Bot')
    parser.add_argument('--mode', type=str, choices=['console', 'web'], default='console', help='Output mode: console or web')
    parser.add_argument('--interface', type=str, default=None, help='Network interface to monitor')
    parser.add_argument('--timeout', type=int, default=30, help='Time interval to refresh the analysis')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start_monitoring(interface=args.interface, timeout=args.timeout, mode=args.mode)