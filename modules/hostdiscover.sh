#!/bin/bash
JSON_FILE="payload.json"
OS_FILE="sessions/os.json"
STARTIP=$(jq -r '.startip' "$JSON_FILE")
STARTIP="${STARTIP%?}"
FILE="sessions/hostsdiscovery.txt" 
# Función para extraer IPs de la salida de arp -a y remover paréntesis
extract_ips_from_arp() {
  arp -a | awk '{if ($2 ~ /[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) {print $2}}' | sed 's/(\(.*\))/\1/g'
}

# Función para extraer IPs de la salida de netstat -tulnp (escuchando)
extract_listening_ips_from_netstat() {
  netstat -tulnp | grep 'Listen' | awk '{split($4, a, ":"); print a[1]}' | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}'
}

# Obtener IPs de arp
arp_ips=$(extract_ips_from_arp)

# Obtener IPs de netstat
netstat_ips=$(extract_listening_ips_from_netstat)

# Combinar y mostrar IPs únicas y guardar en archivo
(
  echo "$arp_ips"
  echo "$netstat_ips"
) | sort -u > $FILE

for i in $(seq 1 254); do
  if timeout 1 ping -c 1 $STARTIP$i &>/dev/null; then
    echo "$STARTIP$i" >> $FILE
  fi
done
sort -u $FILE -o $FILE