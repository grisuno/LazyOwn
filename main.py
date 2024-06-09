from flask import Flask, request, jsonify, render_template, Response
from app import LazyOwnShell
import subprocess

app = Flask(__name__)
shell = LazyOwnShell()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
def run_command():
    data = request.json
    command = data.get('command')
    
    if not command:
        return jsonify({"error": "No command provided"}), 400

    try:
        output = shell.onecmd(command)
        output = get_output()
        return jsonify({"result": output}), 200
    except Exception as e:
        #return jsonify({"error": str(e)}), 500

@app.route('/api/set', methods=['POST'])
def set_param():
    data = request.json
    param = data.get('param')
    value = data.get('value')

    if not param or not value:
        return jsonify({"error": "Param and value are required"}), 400

    try:
        shell.do_set(f"{param} {value}")
        return jsonify({"result": f"{param} set to {value}"}), 200
    except Exception as e:
        #return jsonify({"error": str(e)}), 500

@app.route('/api/show', methods=['GET'])
def show_params():
    params = shell.params
    return jsonify(params)

@app.route('/api/list', methods=['GET'])
def list_scripts():
    scripts = shell.scripts
    return jsonify(scripts)

@app.route('/api/payload', methods=['POST'])
def load_payload():
    try:
        shell.do_payload('')
        return jsonify({"result": "Payload loaded successfully"}), 200
    except Exception as e:
        #return jsonify({"error": str(e)}), 500

@app.route('/api/output', methods=['GET'])
def get_output():
    global shell
    output = shell.output  # Obtener la salida acumulada de la shell
    return jsonify({"output": output})  # Devolver la salida como un objeto JSON

if __name__ == '__main__':
    app.run(debug=False)
