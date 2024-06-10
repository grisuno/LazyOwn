"""
main.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Cliente LazyOwn BotNet

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import socket
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import argparse
import binascii

KEY_SIZE = 16  # 16 bytes para AES-128, 24 bytes para AES-192, 32 bytes para AES-256

def encrypt(plaintext, key):
    plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return unpad(plaintext, AES.block_size).decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description='LazyOwnBotNet Client')
    parser.add_argument('--host', required=True, help='Host of the server')
    parser.add_argument('--port', type=int, required=True, help='Port of the server')
    parser.add_argument('--key', required=True, help='Encryption key (hex encoded)')
    args = parser.parse_args()

    host = args.host
    port = args.port
    key = binascii.unhexlify(args.key)[:KEY_SIZE]

    while True:
        cmd = input('cmd> ')
        if cmd.lower() == 'exit':
            break

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((host, port))
            conn.send(encrypt(cmd, key))

            data = conn.recv(4096)
            result = decrypt(data, key)
            print(result)

            conn.close()
        except Exception as e:
            print(f'[-] Error connecting to {host}:{port} - {e}')
            break

if __name__ == '__main__':
    BANNER = """
@@@        @@@@@@   @@@@@@@@  @@@ @@@   @@@@@@   @@@  @@@  @@@  @@@  @@@                          
@@@       @@@@@@@@  @@@@@@@@  @@@ @@@  @@@@@@@@  @@@  @@@  @@@  @@@@ @@@                          
@@!       @@!  @@@       @@!  @@! !@@  @@!  @@@  @@!  @@!  @@!  @@!@!@@@                          
!@!       !@!  @!@      !@!   !@! @!!  !@!  @!@  !@!  !@!  !@!  !@!!@!@!                          
@!!       @!@!@!@!     @!!     !@!@!   @!@  !@!  @!!  !!@  @!@  @!@ !!@!                          
!!!       !!!@!!!!    !!!       @!!!   !@!  !!!  !@!  !!!  !@!  !@!  !!!                          
!!:       !!:  !!!   !!:        !!:    !!:  !!!  !!:  !!:  !!:  !!:  !!!                          
 :!:      :!:  !:!  :!:         :!:    :!:  !:!  :!:  :!:  :!:  :!:  !:!                          
 :: ::::  ::   :::   :: ::::     ::    ::::: ::   :::: :: :::    ::   ::                          
: :: : :   :   : :  : :: : :     :      : :  :     :: :  : :    ::    :                           
                                                                                                  
                                                                                                  
@@@@@@@@  @@@@@@@    @@@@@@   @@@@@@@@@@   @@@@@@@@  @@@  @@@  @@@   @@@@@@   @@@@@@@   @@@  @@@  
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@  @@@  
@@!       @@!  @@@  @@!  @@@  @@! @@! @@!  @@!       @@!  @@!  @@!  @@!  @@@  @@!  @@@  @@!  !@@  
!@!       !@!  @!@  !@!  @!@  !@! !@! !@!  !@!       !@!  !@!  !@!  !@!  @!@  !@!  @!@  !@!  @!!  
@!!!:!    @!@!!@!   @!@!@!@!  @!! !!@ @!@  @!!!:!    @!!  !!@  @!@  @!@  !@!  @!@!!@!   @!@@!@!   
!!!!!:    !!@!@!    !!!@!!!!  !@!   ! !@!  !!!!!:    !@!  !!!  !@!  !@!  !!!  !!@!@!    !!@!!!    
!!:       !!: :!!   !!:  !!!  !!:     !!:  !!:       !!:  !!:  !!:  !!:  !!!  !!: :!!   !!: :!!   
:!:       :!:  !:!  :!:  !:!  :!:     :!:  :!:       :!:  :!:  :!:  :!:  !:!  :!:  !:!  :!:  !:!  
 ::       ::   :::  ::   :::  :::     ::    :: ::::   :::: :: :::   ::::: ::  ::   :::   ::  :::  
 :         :   : :   :   : :   :      :    : :: ::     :: :  : :     : :  :    :   : :   :   :::  
    
    [*] Iniciando: LazyBotCli [;,;]
    """
    print(BANNER)    
    main()
