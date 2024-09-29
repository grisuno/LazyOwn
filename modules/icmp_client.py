import os
import sys
import socket
import struct
import time
import hashlib
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()

ICMP_ECHO_REQUEST = 8

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data.encode(), AES.block_size))

def decrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)

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
    encrypted_data = encrypt_data(compressed_data.decode('latin-1'), key)
    
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
    except socket.error as e:
        print(f"Error al enviar el paquete: {e}")
    finally:
        sock.close()

def receive_icmp_reply(sock):
    try:
        reply, addr = sock.recvfrom(1024)
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
    main()
