#!/bin/bash
# Inspired by https://github.com/IHA089/S-Tor.git
# Author: https://github.com/IHA089
# Thanks to the author for the awesome script. I only rewrote it in bash and added sudo check.

check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] This script requires superuser permissions. Relaunching with sudo..."
        sudo "$0" --vpn "$VPN" "${@/#--vpn*/}"
        exit
    fi
}

check_sudo "$@"

check_tor() {
    if command -v tor &> /dev/null; then
        return 0
    else
        return 1
    fi
}

install_tor() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install tor -y
    else
        echo "You are using $OSTYPE, but this tool is only designed for Linux."
        exit 1
    fi
}

torrc_conf() {
    local filename="$1"
    if [[ -f "$filename" ]]; then
        grep -qxF 'HiddenServiceDir /var/lib/tor/hidden_service/' "$filename" || echo 'HiddenServiceDir /var/lib/tor/hidden_service/' | sudo tee -a "$filename"
        grep -qxF 'HiddenServicePort 80 127.0.0.1:80' "$filename" || echo 'HiddenServicePort 80 127.0.0.1:80' | sudo tee -a "$filename"
    else
        echo "torrc file not present in your system"
    fi
}

torrc_conf_stop() {
    local filename="$1"
    if [[ -f "$filename" ]]; then
        sudo sed -i '/HiddenServiceDir \/var\/lib\/tor\/hidden_service\//d' "$filename"
        sudo sed -i '/HiddenServicePort 80 127.0.0.1:80/d' "$filename"
    else
        echo "torrc file not present in your system"
    fi
}

start_server() {
    local port="$1"
    python3 -m http.server "$port"
}

start_netcat() {
    local port="$1"
    nc -lvnp "$port"
}

start_lazyc2() {
    local port="$1"
    python3 modules/lazyc2.py "$port"
}

main() {
    local port="${1:-80}" # Set default port to 80 if not provided

    echo "Select mode:"
    echo "1. Start HTTP Server"
    echo "2. Start Netcat Listener"
    echo "3. Start LazyC2 Server"
    read -p "Enter choice (1, 2, or 3): " choice

    if ! check_tor; then
        echo "Tor is not installed on your system"
        echo "Installing tor...."
        install_tor
    fi

    local filename="/etc/tor/torrc"
    
    torrc_conf "$filename"
    sudo service tor start
    
    if [[ -f "/var/lib/tor/hidden_service/hostname" ]]; then
        local url
        url=$(cat /var/lib/tor/hidden_service/hostname)
        echo "Onion URL ::: http://$url"
    else
        echo "Hidden service hostname file not found"
    fi
    
    trap 'echo "Stopping..."; sudo service tor stop; torrc_conf_stop "$filename"; exit' INT

    case $choice in
        1)
            start_server "$port"
            ;;
        2)
            start_netcat "$port"
            ;;
        3)
            start_lazyc2 "$port"
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
}

main "$@"
