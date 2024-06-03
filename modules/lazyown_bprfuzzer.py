import argparse
import json
import requests
import signal
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Global flag for graceful shutdown
should_exit = False
BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: LazyOwn Fuzzer and Repeater Cli Assistent [;,;]
"""
print(BANNER)
def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] Saliendo...")
    should_exit = True

signal.signal(signal.SIGINT, signal_handler)

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def _handle_request(self, method):
        url = self.path
        headers = dict(self.headers)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else None

        try:
            response = requests.request(method, url, headers=headers, data=body)
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
        except requests.RequestException as e:
            self.send_error(500, f'[e] Proxy Error: {e}')

def run_proxy(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f'[P] Proxy ejecutándose en el puerto {port}')
    httpd.serve_forever()

def edit_file_with_nano(content):
    with tempfile.NamedTemporaryFile(delete=False, mode='w+') as temp_file:
        temp_file.write(content)
        temp_file.flush()
        subprocess.run(['nano', temp_file.name])
        temp_file.seek(0)
        edited_content = temp_file.read()
    return edited_content

def send_request(url, method='GET', headers=None, params=None, data=None, json_data=None, proxies=None, hide_code=None):
    """
    Envía una solicitud HTTP y devuelve la respuesta.
    """
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data, json=json_data, proxies=proxies)
        
        if hide_code and response.status_code == hide_code:
            return None
        
        print(f"[S] Solicitud {method} a {url} enviada.")
        print(f"[C] Código de estado: {response.status_code}")
        print("[H] Encabezados de la respuesta:")
        print(response.headers)
        print("[R] Contenido de la respuesta:")
        print(response.text)
        return response
    except requests.RequestException as e:
        print(f"[E] Error en la solicitud: {e}")
        return None

def repeater(url, method, headers, params, data, json_data, proxies, hide_code):
    """
    Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
    """
    while not should_exit:
        
        print("[*] \n--- Nueva iteración del Repeater ---")
        
        headers_json = json.dumps(headers, indent=4)
        edited_headers = edit_file_with_nano(headers_json)
        headers = json.loads(edited_headers)

        data_json = json.dumps(data, indent=4)
        edited_data = edit_file_with_nano(data_json)
        data = json.loads(edited_data)

        response = send_request(url, method, headers, params, data, json_data, proxies, hide_code)
        if response is not None and response.headers.get('Content-Type') == 'application/json':
            try:
                response_json = response.json()
                print("[J] Contenido de la respuesta en JSON:")
                print(json.dumps(response_json, indent=4))
            except ValueError:
                print("[e] La respuesta no es un JSON válido")
        
        repeat = input("[?] ¿Quieres repetir la solicitud? (s/n): ").strip().lower()
        if repeat != 's':
            print("[R] Finalizando el Repeater.")
            break

def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code):
    """
    Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
    """
    with open(wordlist_path, 'r') as f:
        words = f.read().splitlines()
    
    for word in words:
        if should_exit:
            break
        
        # Convertir los encabezados, datos y parámetros a cadenas JSON
        headers_json = json.dumps(headers)
        data_json = json.dumps(data)
        params_json = json.dumps(params)
        json_data_json = json.dumps(json_data)

        # Reemplazar LAZYFUZZ en las cadenas JSON
        headers_json = headers_json.replace("LAZYFUZZ", word)
        data_json = data_json.replace("LAZYFUZZ", word)
        params_json = params_json.replace("LAZYFUZZ", word)
        json_data_json = json_data_json.replace("LAZYFUZZ", word)

        # Convertir las cadenas JSON de nuevo a diccionarios
        headers = json.loads(headers_json)
        data = json.loads(data_json)
        params = json.loads(params_json)
        json_data = json.loads(json_data_json)

        # Reemplazar LAZYFUZZ en la URL
        fuzzed_url = url.replace("LAZYFUZZ", word)
        
        response = send_request(fuzzed_url, method, headers, params, data, json_data, proxies, hide_code)
        if response is not None:
           
            print(f"\n--- [*] Nueva iteración del Fuzzing con {word} ---")
            
            if response.headers.get('Content-Type') == 'application/json':
                try:
                    response_json = response.json()
                    print("[J] Contenido de la respuesta en JSON:")
                    print(json.dumps(response_json, indent=4))
                except ValueError:
                    print("[e] La respuesta no es un JSON válido")

def parse_arguments():
    """
    Parsear los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description='Script HTTP Repeater y Fuzzer')
    parser.add_argument('--url', required=True, help='URL a la que se enviará la solicitud')
    parser.add_argument('--method', default='GET', help='Método HTTP (GET, POST, PUT, DELETE, etc.)')
    parser.add_argument('--headers', type=json.loads, default='{}', help='Encabezados de la solicitud en formato JSON')
    parser.add_argument('--params', type=json.loads, default='{}', help='Parámetros de la URL en formato JSON')
    parser.add_argument('--data', type=json.loads, default='{}', help='Datos del formulario en formato JSON')
    parser.add_argument('--json_data', type=json.loads, default='{}', help='Datos JSON para la solicitud en formato JSON')
    parser.add_argument('--proxy_port', type=int, default=8080, help='Puerto del proxy interno')
    parser.add_argument('-w', '--wordlist', help='Ruta del diccionario para el modo fuzzing')
    parser.add_argument('-hc', '--hide_code', type=int, help='Código de estado HTTP para ocultar en la salida')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Iniciar el proxy en segundo plano
    proxy_thread = threading.Thread(target=run_proxy, args=(args.proxy_port,), daemon=True)
    proxy_thread.start()

    proxies = {
        'http': f'http://localhost:{args.proxy_port}',
        'https': f'http://localhost:{args.proxy_port}'
    }

    print(f"[P] Configuración del proxy: {proxies}")

    if args.wordlist:
        lazyfuzz(args.url, args.method, args.headers, args.params, args.data, args.json_data, proxies, args.wordlist, args.hide_code)
    else:
        repeater(args.url, args.method, args.headers, args.params, args.data, args.json_data, proxies, args.hide_code)
