import socket
import tempfile
import subprocess
import keyboard
import threading
import os
import sys
import signal


# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print(
            "[S] Este script necesita permisos de superusuario. Relanzando con sudo..."
        )
        args = ["sudo", sys.executable] + sys.argv
        os.execvpe("sudo", args, os.environ)


# Manejar la interrupción de Ctrl+C
def signal_handler(sig, frame):
    print("\n [->] Captura interrumpida.")
    sys.exit(0)


def get_ip_from_url(url):
    puerto = 80
    try:
        # Extraer el nombre de dominio de la URL
        if url.startswith("http://"):
            url = url[7:]
            puerto = 80
        elif url.startswith("https://"):
            url = url[8:]
            puerto = 443
        # Eliminar cualquier ruta después del dominio
        url = url.split("/")[0]

        # Resolver el nombre de dominio en una dirección IP
        ip_address = socket.gethostbyname(url)
        return f"{ip_address}:{puerto}"
    except socket.gaierror as e:
        print(f"Error resolviendo {url}: {e}")
        return None


def handle_request(client_socket, address):
    print(f"[C->] Conexión entrante de {address}")

    request = client_socket.recv(4096)
    print(f"[R] {request}")
    temp_req = request.decode("utf-8")
    method = temp_req.split(" ")
    print(len(method))
    if len(method) < 1:
        print("error")
        return
    url = method[1]
    ipmaspuerto = get_ip_from_url(url)
    ip = ipmaspuerto.split(":")
    puerto = ip[1]
    ip = ip[0]
    print(f"{ip}:{puerto}")
    # Guardar la solicitud en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(request)
        temp_filename = temp.name

    # Esperar a que se presione 'espacio+e' para abrir `nano`
    print("[!] Presiona 'espacio+e' para editar la solicitud...")
    keyboard.wait("space+e")

    # Abrir nano con el archivo temporal
    subprocess.run(["nano", temp_filename])

    # Leer el contenido editado
    with open(temp_filename, "rb") as temp:
        modified_request = temp.read()

    try:
        # Crear una conexión al servidor de destino
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(
            f"[*] Conectando al servidor de destino en {ip}:{puerto}"
        )  # Asegúrate de cambiar a la IP y puerto correctos
        server_socket.connect((ip, int(puerto)))
        server_socket.send(modified_request)

        # Obtener la respuesta del servidor
        response = server_socket.recv(4096)
        server_socket.close()

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


def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(("0.0.0.0", 8888))
    proxy_socket.listen(5)
    print("[;,;] Servidor proxy escuchando en el puerto 8888...")

    while True:
        client_socket, address = proxy_socket.accept()
        client_handler = threading.Thread(
            target=handle_request, args=(client_socket, address)
        )
        client_handler.start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    check_sudo()
    start_proxy()
