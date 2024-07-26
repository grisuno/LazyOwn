import os
import sys
import subprocess
import argparse
import ipaddress
from datetime import datetime
import numpy as np
import cv2
from scapy.all import sniff, Raw, IP, get_if_list

# Variables para almacenar datos de imágenes
image_data = {}
is_receiving_image = {}
image_format = {}

# Crear un directorio con la fecha actual
date_str = datetime.now().strftime('%Y-%m-%d')
os.makedirs(date_str, exist_ok=True)
# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()
def list_interfaces():
    command = "ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,\"\",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, \"/\"); print iface\" \"a[1] }'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    interfaces = []
    if output:
        lines = output.split('\n')
        for line in lines:
            iface, ip = line.split()
            interfaces.append((iface, ip))

    print("Interfaces disponibles (usando 'ip a show scope global'):")
    for idx, iface in enumerate(interfaces):
        print(f"{idx}: {iface[0]} - {iface[1]}")

    return interfaces

def choose_interface(interfaces):
    while True:
        try:
            choice = int(input("Selecciona el número de la interfaz: "))
            if 0 <= choice < len(interfaces):
                return interfaces[choice][0]
            else:
                print("Número inválido. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Debe ser un número.")

# Función para obtener la subred desde ip a show
def get_subnet_from_interface(interface):
    command = f"ip a show {interface} | awk '/inet / {{ split($2, a, \"/\"); print a[1]\"/\"a[2] }}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if output:
        return output
    return '0.0.0.0/0'

# Argumentos de línea de comandos
parser = argparse.ArgumentParser(description="Captura imágenes de la red")
parser.add_argument('-D', '--daemon', action='store_true', help='Ejecutar como demonio')
parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--ip', type=str, help='IP de la cámara para capturar paquetes')
group.add_argument('--all', action='store_true', help='Capturar paquetes de toda la red')
args = parser.parse_args()

# Listar interfaces y permitir al usuario elegir una
show_ifaces = list_interfaces()
iface_name = choose_interface(show_ifaces)

# Filtro para capturar tráfico en la subred o IP específica
if args.ip:
    filter_str = f"host {args.ip}"
elif args.all:
    subnet = get_subnet_from_interface(iface_name)
    filter_str = f"net {subnet}"

def handle_packet(packet):
    global image_data, is_receiving_image, image_format

    if IP in packet and Raw in packet:
        src_ip = packet[IP].src
        payload = packet[Raw].load

        if src_ip not in image_data:
            image_data[src_ip] = b''
            is_receiving_image[src_ip] = False
            image_format[src_ip] = None

        if is_receiving_image[src_ip]:
            image_data[src_ip] += payload

            # Detectar el final de la imagen según el formato
            if image_format[src_ip] == 'jpeg' and b'\xff\xd9' in payload:
                end_idx = image_data[src_ip].find(b'\xff\xd9') + 2
                save_image(src_ip, end_idx)
            elif image_format[src_ip] == 'png' and b'\x49\x45\x4e\x44\xae\x42\x60\x82' in payload:
                end_idx = image_data[src_ip].find(b'\x49\x45\x4e\x44\xae\x42\x60\x82') + 8
                save_image(src_ip, end_idx)
            elif image_format[src_ip] == 'bmp' and len(image_data[src_ip]) >= 54:
                file_size = int.from_bytes(image_data[src_ip][2:6], byteorder='little')
                if len(image_data[src_ip]) >= file_size:
                    save_image(src_ip, file_size)

        else:
            if b'\xff\xd8' in payload:
                image_format[src_ip] = 'jpeg'
                start_idx = payload.find(b'\xff\xd8')
                image_data[src_ip] = payload[start_idx:]
                is_receiving_image[src_ip] = True
            elif b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' in payload:
                image_format[src_ip] = 'png'
                start_idx = payload.find(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a')
                image_data[src_ip] = payload[start_idx:]
                is_receiving_image[src_ip] = True
            elif b'\x42\x4d' in payload:
                image_format[src_ip] = 'bmp'
                start_idx = payload.find(b'\x42\x4d')
                image_data[src_ip] = payload[start_idx:]
                is_receiving_image[src_ip] = True

def save_image(src_ip, end_idx):
    global image_data, is_receiving_image, image_format

    image_data[src_ip] = image_data[src_ip][:end_idx]
    try:
        np_arr = np.frombuffer(image_data[src_ip], np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is not None:
            if args.verbose:
                print(f"Imagen recibida de {src_ip}")

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ext = 'jpg' if image_format[src_ip] == 'jpeg' else image_format[src_ip]
            filename = f"{date_str}/image_{src_ip}_{timestamp}.{ext}"
            cv2.imwrite(filename, img)

            if not args.daemon:
                cv2.imshow(f"Camera Image from {src_ip}", img)
                cv2.waitKey(1)
    except Exception as e:
        print(f"Error processing image from {src_ip}: {e}")
    finally:
        image_data[src_ip] = b''
        is_receiving_image[src_ip] = False
        image_format[src_ip] = None

def run():
    if args.verbose:
        print(f"Capturando paquetes con filtro: {filter_str}...")
    sniff(iface=iface_name, prn=handle_packet, filter=filter_str)

def daemonize():
    if os.fork():
        sys.exit(0)  # Salir del proceso padre
    os.setsid()
    if os.fork():
        sys.exit(0)  # Salir del segundo proceso padre
    os.umask(0)
    os.chdir('/')
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as fd:
        os.dup2(fd.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as fd:
        os.dup2(fd.fileno(), sys.stdout.fileno())
        os.dup2(fd.fileno(), sys.stderr.fileno())
    atexit.register(lambda: os.remove('/tmp/capture_images_daemon.pid'))



if __name__ == '__main__':
    if args.daemon:
        daemonize()
        with open('/tmp/capture_images_daemon.pid', 'w+') as pidfile:
            pidfile.write(f"{os.getpid()}\n")
    run()

    if not args.daemon:
        cv2.destroyAllWindows()
