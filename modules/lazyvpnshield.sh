#!/bin/bash

# Author: Nisrin Ahmed aka Wh1teDrvg0n
# Modify: grisun0

RULES_DIR="./sessions"
RULES_FILE="$RULES_DIR/iptables.txt"

trap ctrl_c INT

function ctrl_c() {
	echo "    [;,;] Trapped CTRL-C"
	exit 1
}

function check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] Este script necesita permisos de superusuario. Relanzando con sudo..."
        sudo bash "$0" "$@"
        exit
    fi
}

check_sudo

mkdir -p "$RULES_DIR"


save_current_rules() {
# Función para guardar las reglas actuales
    echo "Guardando las reglas actuales en $RULES_FILE..."
    iptables-save > "$RULES_FILE"
    echo "Reglas guardadas."
}


show_current_rules() {
# Función para mostrar las reglas actuales
    iptables -L
    echo "Reglas actuales:"
    cat "$RULES_FILE"
}


apply_vpn_rules() {
# Función para aplicar las reglas específicas para la VPN
    echo "Aplicando reglas para asegurar la VPN..."
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -t nat -F
    iptables -t mangle -F
    iptables -F
    iptables -X
    iptables -Z

    ip6tables -P INPUT DROP
    ip6tables -P FORWARD DROP
    ip6tables -P OUTPUT DROP
    ip6tables -t nat -F
    ip6tables -t mangle -F
    ip6tables -F
    ip6tables -X
    ip6tables -Z

    iptables -A INPUT -p icmp -i tun0 -s $1 --icmp-type echo-request -j ACCEPT
    iptables -A INPUT -p icmp -i tun0 -s $1 --icmp-type echo-reply -j ACCEPT
    iptables -A INPUT -p icmp -i tun0 --icmp-type echo-request -j DROP  
    iptables -A INPUT -p icmp -i tun0 --icmp-type echo-reply -j DROP
    iptables -A OUTPUT -p icmp -o tun0 -d $1 --icmp-type echo-reply -j ACCEPT
    iptables -A OUTPUT -p icmp -o tun0 -d $1 --icmp-type echo-request -j ACCEPT
    iptables -A OUTPUT -p icmp -o tun0 --icmp-type echo-request -j DROP
    iptables -A OUTPUT -p icmp -o tun0 --icmp-type echo-reply -j DROP

    iptables -A INPUT -i tun0 -p tcp -s $1 -j ACCEPT
    iptables -A OUTPUT -o tun0 -p tcp -d $1 -j ACCEPT
    iptables -A INPUT -i tun0 -p udp -s $1 -j ACCEPT
    iptables -A OUTPUT -o tun0 -p udp -d $1 -j ACCEPT
    iptables -A INPUT -i tun0 -j DROP
    iptables -A OUTPUT -o tun0 -j DROP

    echo "Reglas para VPN aplicadas."
}


undo_and_restore_rules() {
# Función para deshacer las reglas y aplicar las guardadas
    echo "Deshaciendo las reglas actuales..."
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -t nat -F
    iptables -t mangle -F
    iptables -F
    iptables -X
    iptables -Z

    ip6tables -P INPUT DROP
    ip6tables -P FORWARD DROP
    ip6tables -P OUTPUT DROP
    ip6tables -t nat -F
    ip6tables -t mangle -F
    ip6tables -F
    ip6tables -X
    ip6tables -Z

    echo "Reglas deshechas. Aplicando reglas guardadas..."
    iptables-restore < "$RULES_FILE"
    echo "Reglas restauradas."
}


main() {
    save_current_rules
    show_current_rules
    read -p "¿Desea asegurar la VPN? (s/n): " respuesta
    if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
        apply_vpn_rules $1
    elif [[ "$respuesta" == "n" || "$respuesta" == "N" ]]; then
        undo_and_restore_rules
    else
        echo "Respuesta no válida. No se hicieron cambios."
    fi
}
main
