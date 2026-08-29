import hashlib
import os
import secrets
import socket
import struct
import sys
import time
import zlib

from Crypto.Cipher import AES

ICMP_ECHO_REQUEST = 8
ICMP_BUFFER_SIZE = 4096
AES_NONCE_LENGTH = 12
AES_TAG_LENGTH = 16

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


# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

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

def send_icmp_packet(dest_addr, data, key):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("Error: Este script requiere privilegios de administrador.")
        return

    packet_id = os.getpid() & 0xFFFF

    # Compress and encrypt data
    compressed_data = zlib.compress(data.encode())
    encrypted_data = encrypt_data(compressed_data, key)

    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, packet_id, 1)
    my_checksum = checksum(header + encrypted_data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), packet_id, 1)
    packet = header + encrypted_data

    try:
        sock.sendto(packet, (dest_addr, 1))
        print(f"Comando enviado a {dest_addr}: {data}")

        # Recibir respuesta
        encrypted_reply = receive_icmp_reply(sock)
        if encrypted_reply:
            decrypted_reply = decrypt_data(encrypted_reply, key)
            decompressed_reply = zlib.decompress(decrypted_reply)
            print(f"Respuesta del servidor: {decompressed_reply.decode()}")
        return
    except OSError as e:
        print(f"Error al enviar el paquete: {e}")
    finally:
        sock.close()

def receive_icmp_reply(sock):
    try:
        reply, addr = sock.recvfrom(ICMP_BUFFER_SIZE)
        icmp_header = reply[20:28]
        icmp_type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)
        if icmp_type == 0:  # ICMP echo reply
            encrypted_data = reply[28:]
            return encrypted_data
    except Exception as e:
        print(f"Error al recibir la respuesta: {str(e)}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Cliente ICMP para enviar comandos.')
    parser.add_argument('server_ip', help='IP del servidor')
    parser.add_argument('-i', '--interval', type=float, default=1.0, help='Intervalo entre comandos (segundos)')
    parser.add_argument('-p', '--password', required=True, help='Contraseña para encriptar los datos')
    args = parser.parse_args()

    key = hashlib.sha256(args.password.encode()).digest()

    print(f"Enviando comandos a {args.server_ip} cada {args.interval} segundos.")
    print("Presione Ctrl+C para salir.")

    try:
        while True:
            command = input("Ingrese el comando a enviar (o 'exit' para salir): ")
            if command.lower() == 'exit':
                break
            send_icmp_packet(args.server_ip, command, key)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")

if __name__ == "__main__":
    check_sudo()
    main()
