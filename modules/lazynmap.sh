#!/bin/bash

################################################################################
# Nombre del script: lazynmap.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 09/06/2024
# Descripción: Este script contiene la lógica principal de la aplicación. lazynmap
# Licencia: GPL v3
################################################################################
# Banner
echo "██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗"
echo "██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║"
echo "██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║"
echo "██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║"
echo "███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║"
echo "╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"
echo "LazyNmap...:::...::.::......::::....::..::::..:::..:::...:::..:"

# Función para manejar señales (como Ctrl+C)
trap ctrl_c INT

function ctrl_c() {
  echo "[;,;] Trapped CTRL-C"
  exit 1
}

# Verificar si se ha proporcionado el objetivo
if [ $# -lt 1 ]; then
  echo "[?] Uso: $0 -t <objetivo>"
  exit 1
fi

# Inicializar variables
TARGET=""
DISCOVER_NETWORK=false

# Obtener los parámetros
while getopts "t:d" opt; do
  case ${opt} in
    t )
      TARGET=$OPTARG
      ;;
    d )
      DISCOVER_NETWORK=true
      ;;
    \? )
      echo "[?] Uso: $0 -t <objetivo> [-d]"
      exit 1
      ;;
  esac
done

if [ -z "$TARGET" ] && [ "$DISCOVER_NETWORK" = false ]; then
  echo "[?] Uso: $0 -t <objetivo> [-d]"
  exit 1
fi

# Función para descubrir la red local
discover_network() {
  echo "[+] Descubriendo la red local..."
  local subnet=$(ip -o -f inet addr show | awk '/scope global/ {print $4}')
  for net in $subnet; do
    echo "[-] Escaneando la subred $net..."
    sudo nmap -sn $net -oG network_discovery
    echo "[+] Hosts activos en la red $net:"
    grep "Up" network_discovery | awk '{print $2}'
  done
}

if [ "$DISCOVER_NETWORK" = true ]; then
  discover_network
  exit 0
fi

# Medir el tiempo de inicio
START_TIME=$(date +%s)

# Realizar el escaneo inicial para encontrar puertos abiertos
echo "[-] Realizando escaneo inicial para encontrar puertos abiertos..."
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn $TARGET -oG puertos

# Extraer la información de puertos y direcciones IP del archivo de resultados de Nmap
extract_ports_info() {
  local file=$1
  ports=$(grep -oP '\d{1,5}/open' $file | awk '{print $1}' FS='/' | xargs | tr ' ' ',')
  ip_address=$(grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' $file | sort -u | head -n 1)
  echo -e "\n[*] Extrayendo información...\n"
  echo -e "\t[*] Dirección IP: $ip_address"
  echo -e "\t[*] Puertos abiertos: $ports\n"
}

# Extraer y mostrar la información de los puertos
extract_ports_info "puertos"

# Extraer los puertos abiertos del archivo de salida
PORTS=$(grep -oP '\d{1,5}/open/tcp' puertos | awk -F/ '{print $1}' | tr '\n' ',' | sed 's/,$//')

if [ -z "$PORTS" ]; then
  echo "[!] No se encontraron puertos abiertos en el objetivo $TARGET"
  exit 1
fi

echo "[+] Puertos abiertos encontrados: $PORTS"

# Función para ejecutar el segundo comando Nmap en un puerto específico
run_nmap_script() {
  PORT=$1
  echo "[;,;] Escaneando el puerto $PORT en el objetivo $TARGET..."
  sudo nmap -p $PORT -sCV $TARGET -oN "scan_${TARGET}_${PORT}.nmap"
}

export -f run_nmap_script
export TARGET

# Ejecutar el segundo comando Nmap en los puertos encontrados usando xargs para paralelizar
echo $PORTS | tr ',' '\n' | xargs -P 0 -I {} bash -c 'run_nmap_script "$@"' _ {}

# Verificar si hay archivos "scan_*.nmap" disponibles
SCANS=$(ls -1 scan_*.nmap 2>/dev/null)

# Verificar si se encontraron puertos abiertos y archivos de escaneo
if [ -z "$PORTS" ]; then
  echo "[-] No se encontraron puertos abiertos en el archivo 'puertos'"
  exit 1
fi

if [ -z "$SCANS" ]; then
  echo "[-] No se encontraron archivos de escaneo (scan_*.nmap)"
  exit 1
fi

# Función para imprimir una fila de la tabla
print_row() {
  printf "| %-10s | %-60s |\n" "$1" "$2"
}

# Imprimir encabezados de tabla
echo "+------------+--------------------------------------------------------------+"
print_row "Puerto" "Información del Escaneo"
echo "+------------+--------------------------------------------------------------+"

# Iterar sobre cada puerto y buscar su información en los archivos de escaneo
for PORT in $(echo $PORTS | tr ',' ' '); do
  INFO=""
  # Iterar sobre cada archivo de escaneo
  for SCAN_FILE in $SCANS; do
    # Extraer la información del escaneo correspondiente al puerto
    SCAN_INFO=$(grep -A 10 "$PORT/tcp" "$SCAN_FILE" | grep -v "$PORT/tcp")
    if [ -n "$SCAN_INFO" ]; then
      INFO="$SCAN_INFO"
      break
    fi
  done
  # Imprimir la información del puerto
  print_row "$PORT" "$INFO"
done

# Imprimir el final de la tabla
echo "+------------+--------------------------------------------------------------+"

# Medir el tiempo de finalización
END_TIME=$(date +%s)
EXECUTION_TIME=$(($END_TIME - $START_TIME))

echo "[t] El tiempo total de ejecución fue: $EXECUTION_TIME segundos"
