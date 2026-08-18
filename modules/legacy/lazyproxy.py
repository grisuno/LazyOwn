import os
import signal
import socket
import subprocess
import sys
import tempfile
import threading

import keyboard
from colors import *  # noqa: F403

BANNER = f"""{GREEN}{BG_BLACK}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠴⠶⠖⠒⠛⠛⠀⠀⠀⠒⠒⢰⠖⢠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣭⠷⠞⠉⠫⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠈⠉⠒⠲⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣷⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⢄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡾⢋⠷⣻⣿⣟⢿⣿⠿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠸⣄⠀⠀⠀⠀
⠀⠀⠀⣀⣾⣯⢶⣿⣾⣿⡟⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢦⠀⠀⠀
⠀⠀⢠⣿⣿⣤⣽⣿⣿⣿⣃⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⢀⣽⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣦⣴⣆⣀⣀⣀⣀⢀⠀⠀⣐⠄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⢀⣀⠴⠶⠛⠛⠛⠛⠛⠳⠶⣶⣦⡀⠀⠀⠘
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠐⠤⣯⣀⡰⡋⣡⣐⣶⣽⣶⣶⣾⣿⣷⣶⣤⣝⡣⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⣿⣿⣿⣿⣿⣿⣿⣭⡿⣿⡋⠉⠙⢿⡦⠀⠀⠀⠀⠀⠀⠀⢀⣌⣼⡩⢻⣷⣿⣿⣿⣿⣿⣿⡏⣛⢿⣿⣿⡿⠃⢰⠀⠀
⠀⢿⣿⣿⣿⣿⣿⣿⣛⠿⣷⣄⣙⣿⠿⠿⠟⠛⣿⣿⣜⣶⡂⡉⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⢻⣾⡛⠛⢿⠿⠿⠟⢻⣧⣽⣿⠿⠋⠀⠄⢸⣧⠔
⠀⠘⢿⣿⣿⣿⣿⢿⣿⣿⣷⣾⣭⣿⣿⣟⣛⣛⣛⣛⢿⣽⣿⣧⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠃⣿⡿⠿⠿⠿⠿⢻⣛⣛⣋⣉⣁⠤⠒⠒⠂⣠⣿⠏⠀
⠀⠀⠈⠻⢿⣿⣿⣶⣄⣉⠉⠉⠉⠉⠉⠛⠉⠉⠁⠉⠁⢹⢻⣿⣏⢹⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⣀⣴⠿⠝⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣷⣶⣶⣶⣦⣴⣴⣾⢬⡤⢬⡜⠛⠀⢾⢿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠶⣦⣤⣄⣤⣐⣢⣤⣴⣾⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣯⣤⣄⡤⣄⣠⡤⣄⣀⠀⠀⠀⠀⡀⠀⠀⠀⡀⠀⠀⢀⣠⣤⣴⣤⣤⢹⣿⣿⣿⡿⠛⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣬⣥⣤⡴⠶⠶⠖⠒⠛⠋⠉⡩⢁⣼⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡓⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⢶⣧⣻⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠾⠀⠀⠀⠀⠀⠀⠀⠀⣀⡜⠼⣷⣸⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣶⣄⣀⣀⣀⡀⠀⢀⠀⠀⣠⡼⣋⣪⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡟⠙⡀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⡿⡁⡟⣡⢀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢛⠀⣸⠆⠈⠹⠀⠀⠀⠀⠀⠀⠀{RED}{BG_BLACK}
    [⚠] Starting 👽 LazyOwn ☠ Proxy ☠ [;,;] {RESET}"""


# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("    [S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ["sudo", sys.executable] + sys.argv
        os.execvpe("sudo", args, os.environ)

# Manejar la interrupción de Ctrl+C
def signal_handler(sig, frame):
    print("\n    [->] Captura interrumpida.")
    sys.exit(0)

# Hexdump para visualizar datos
def hexdump(src, length=16):
    result = []
    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join([f"{b:02X}" for b in s])
        text = ''.join([chr(b) if 0x20 <= b < 0x7F else '.' for b in s])
        result.append(f"{i:04X}   {hexa:<{length * 3}}   {text}")
    print('\n'.join(result))


# Recibir datos del socket con un timeout
def receive_from(connection):
    buffer = b''
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except TimeoutError:
        pass
    return buffer

# Modificar solicitudes antes de enviarlas al servidor remoto
def request_handler(buffer):
    print(buffer)
    return buffer

# Modificar respuestas antes de enviarlas al cliente local
def response_handler(buffer):
    print(buffer)
    return buffer

# Resolver una URL a su dirección IP
def get_ip_from_url(url):
    puerto = 80
    try:
        if url.startswith("http://"):
            url = url[7:]
            puerto = 80
        elif url.startswith("https://"):
            url = url[8:]
            puerto = 443
        url = url.split("/")[0]
        ip_address = socket.gethostbyname(url)
        return f"{ip_address}:{puerto}"
    except socket.gaierror as e:
        print(f"Error resolviendo {url}: {e}")
        return None

# Manejar la solicitud entrante y permitir su edición
def handle_request(client_socket, address):
    print(f"[C->] Conexión entrante de {address}")

    request = receive_from(client_socket)
    print("[R] Solicitud recibida:")
    hexdump(request)
    temp_req = request.decode("utf-8")
    method = temp_req.split(" ")
    if len(method) < 1:
        print("Error en la solicitud.")
        return

    url = method[1]
    ipmaspuerto = get_ip_from_url(url)
    if ipmaspuerto:
        ip, puerto = ipmaspuerto.split(":")
    else:
        print("No se pudo resolver la IP del URL.")
        client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        client_socket.close()
        return

    print(f"{ip}:{puerto}")

    # Guardar la solicitud en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(request)
        temp_filename = temp.name

    # Adquirir el lock antes de editar la solicitud
    edit_lock.acquire()

    try:
        # Esperar a que se presione 'espacio+e' para abrir `nano`
        print("[!] Presiona 'espacio+e' para editar la solicitud...")
        keyboard.wait("space+e")

        # Abrir nano con el archivo temporal
        subprocess.run(["nano", temp_filename])

        # Leer el contenido editado
        with open(temp_filename, "rb") as temp:
            modified_request = temp.read()

        # Aplicar el manejador de solicitudes
        modified_request = request_handler(modified_request)

        try:
            # Crear una conexión al servidor de destino
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[*] Conectando al servidor de destino en {ip}:{puerto}")
            server_socket.connect((ip, int(puerto)))
            server_socket.send(modified_request)

            # Obtener la respuesta del servidor
            response = receive_from(server_socket)
            server_socket.close()

            # Aplicar el manejador de respuestas
            response = response_handler(response)

            # Enviar la respuesta de vuelta al cliente
            client_socket.send(response)
        except socket.gaierror as e:
            print(f"[e] Error de conexión (gaierror): {e}")
            client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        except ConnectionRefusedError as e:
            print(f"[e] Error de conexión: {e}")
            client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        except Exception as e:
            print(f"[e] Error inesperado: {e}")
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            client_socket.close()
    finally:
        # Liberar el lock después de editar la solicitud
        edit_lock.release()

# Iniciar el proxy
def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(("127.0.0.1", 8888))
    proxy_socket.listen(5)
    print(f"{YELLOW}    [;,;] Servidor proxy escuchando en el puerto 8888...")

    while True:
        client_socket, address = proxy_socket.accept()
        client_handler = threading.Thread(
            target=handle_request, args=(client_socket, address)
        )
        client_handler.start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    edit_lock = threading.Lock()

    check_sudo()
    print(BANNER)
    start_proxy()
