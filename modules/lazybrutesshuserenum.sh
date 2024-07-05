#!/bin/bash

# Función para manejar el interruptor de señal Ctrl+C
trap 'echo "Script interrumpido."; exit 1;' INT

# Verificar si se pasaron dos argumentos
if [ $# -ne 2 ]; then
	echo "Uso: $0 <archivo> <host>"
	exit 1
fi

archivo="$1"
host="$2"

# Verificar si el archivo existe y es legible
if [ ! -f "$archivo" ]; then
	echo "Error: El archivo '$archivo' no existe o no es legible."
	exit 1
fi
# Leer el archivo línea por línea y ejecutar el comando para cada línea
while IFS= read -r line; do
	# Ejecutar el comando con los argumentos específicos y la línea actual del archivo
	./modules/lazyopenssh77enum2.py -t "$host" -u "$line"
done <"$1"
