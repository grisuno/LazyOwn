#!/bin/bash
JSON_FILE="payload.json"
OS_FILE="sessions/os.json"
STARTIP=$(jq -r '.startip' "$JSON_FILE")
RHOST=$(jq -r '.rhost' "$JSON_FILE")
LHOST=$(jq -r '.lhost' "$JSON_FILE")
STARTIP="${STARTIP%?}"
FILE="sessions/hostsdiscovery.txt" 
MAX_PINGS=254
TIMEOUT=3
PARALLEL_JOBS=50
./modules/lazynmap.sh -d &> /dev/null 2>&1
extract_ips_from_arp() {
  arp -a | awk '{if ($2 ~ /[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) {print $2}}' | sed 's/(\(.*\))/\1/g'
}

extract_listening_ips_from_netstat() {
  netstat -tulnp | grep 'Listen' | awk '{split($4, a, ":"); print a[1]}' | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}'
}

arp_ips=$(extract_ips_from_arp)
netstat_ips=$(extract_listening_ips_from_netstat)

(
  echo "$arp_ips"
  echo "$netstat_ips"
) | sort -u > $FILE

echo "$RHOST" >> $FILE
echo "$LHOST" >> $FILE

awk -F';' 'NR > 1 {print $1}' scan_discovery* | sort -u >> $FILE

parallel -j "$PARALLEL_JOBS" timeout "$TIMEOUT" ping -c 1 "$STARTIP"{.} ::: $(seq 1 "$MAX_PINGS") >> "$FILE"

sort -u $FILE -o $FILE
