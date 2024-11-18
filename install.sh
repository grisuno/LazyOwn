#!/bin/bash
sudo apt update
sudo apt install ltrace python3-xyzservices python3-venv
python3 -m venv env
source env/bin/activate
# pip install -r requirements.txt

pip install requests 
pip install python-libnmap 
pip install pwncat-cs 
pip install pwn 
pip install groq 
pip install PyPDF2 
pip install docx 
pip install python-docx 
pip install olefile 
pip install exifread 
pip install pycryptodome 
pip install impacket 
pip install pandas 
pip install colorama 
pip install tabulate 
pip install pyarrow 
pip install keyboard 
pip install flask-unsign 
pip install name-that-hash 
pip install certipy-ad 
pip install ast 
pip install pykeepass
pip install cmd2
pip install Pillow
pip install netaddr

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
