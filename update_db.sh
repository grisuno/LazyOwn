#!/bin/bash

# Banner
echo "██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗"
echo "██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║"
echo "██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║"
echo "██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║"
echo "███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║"
echo "╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"
# instala los paquetes
pip install -r requirements.txt

echo "[*] pip install -r requirements.txt ..."
# Ejecuta search.py
echo "[*] Ejecutando search.py..."
python3 search.py

# Verifica si search.py se ejecutó correctamente
if [ $? -eq 0 ]; then
    echo "[+] search.py ejecutado con éxito."
    echo "[*] Ejecutando detailed_search.py..."
    python3 detailed_search.py

    # Verifica si detailed_search.py se ejecutó correctamente
    if [ $? -eq 0 ]; then
        echo "[+] detailed_search.py ejecutado con éxito."
        echo "[*] Ejecutando lazyown.py..."
        python3 lazyown.py
    else
        echo "[-] Error al ejecutar detailed_search.py."
        exit 1
    fi
else
    echo "[-] Error al ejecutar search.py."
    exit 1
fi
