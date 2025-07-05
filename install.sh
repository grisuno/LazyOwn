#!/bin/bash
sudo apt update
sudo apt install ltrace python3-xyzservices python3-venv nmap xsltproc
python3 -m venv env
source env/bin/activate
# pip3 install -r requirements.txt
mkdir vpn
mkdir banners
mkdir -p sessions/logs
pip3 install requests 
pip3 install python-libnmap 
pip3 install pwncat-cs 
pip3 install pwn 
pip3 install groq 
pip3 install PyPDF2 
pip3 install docx 
pip3 install python-docx 
pip3 install olefile 
pip3 install exifread 
pip3 install pycryptodome 
pip3 install impacket 
pip3 install pandas 
pip3 install colorama 
pip3 install tabulate 
pip3 install pyarrow 
pip3 install keyboard 
pip3 install flask-unsign 
pip3 install name-that-hash 
pip3 install certipy-ad 
pip3 install ast 
pip3 install pykeepass
pip3 install cmd2
pip3 install Pillow
pip3 install netaddr
pip3 install stix2
pip3 install pyautogui
pip3 install networkx 
pip3 install pyvis
pip3 install markdown
pip3 install scapy
pip3 install watchdog
pip3 install flask-login 
pip3 instal flask-wtf 
pip3 install bcrypt
pip3 install pyyaml
pip3 install bs4
pip3 install dnslib
pip3 python-telegram-bot 
pip3 install nest_asyncio
pip3 install rich
pip3 install flask_socketio
pip3 install autobloody
pip3 install minikerberos
pip3 install tinydb
pip3 install msldap
pip3 install prettytable
pip3 install fire
pip3 install wget
pip3 install pypykatz
pip3 install donut
pip3 install uro
pip3 install lupa
pip3 install flask_sock
pip3 install donut-shellcode
pip3 install flask_limiter
pip3 install aiosmtpd
pip3 install yagmail
pip3 install validators
pip3 install ua_parser
pip3 install pdf2image
pip3 install python-magic

curl -fsSL https://ollama.com/install.sh | sh

git clone https://github.com/grisuno/LazyOwnInfiniteStorage.git ./modules_ext/lazyown_infinitestorage
chmod +x /modules_ext/lazyown_infinitestorage/install.sh

URL="https://raw.githubusercontent.com/grisuno/LazyOwnEncoderDecoder/main/lazyencoder_decoder.py"

DEST_FILE="modules/lazyencoder_decoder.py"
if [[ -f "$DEST_FILE" ]]; then
	echo "El archivo $DEST_FILE ya existe. borrando..."
	rm -rf "$DEST_FILE"
fi

download_with_wget() {
	wget -O "$DEST_FILE" "$URL"
}

download_with_curl() {
	curl -o "$DEST_FILE" "$URL"
}

if command -v wget &>/dev/null; then
	echo "wget encontrado. Descargando con wget..."
	download_with_wget
elif command -v curl &>/dev/null; then
	echo "wget no encontrado. Descargando con curl..."
	download_with_curl
else
	echo "Ni wget ni curl están instalados. Por favor, instala uno de ellos para continuar."
	exit 1
fi

if [[ -f "$DEST_FILE" ]]; then
	echo "Archivo descargado exitosamente: $DEST_FILE"
else
	echo "Error al descargar el archivo."
	exit 1
fi
