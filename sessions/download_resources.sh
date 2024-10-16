#!/bin/bash
################################################################################
# Nombre del script: download_resources.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 31/07/2024
# Descripción: Este script contiene la lógica principal de la aplicación. download_resources
# Licencia: GPL v3
################################################################################
# Función para manejar señales (como Ctrl+C)
trap ctrl_c INT

function ctrl_c() {
	echo "    [;,;] Trapped CTRL-C Saliendo ..."
	exit 1
}
#Wgets 
download() {

    # Define la lista de comandos wget
    commands=(
        "wget https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/raw/master/Rubeus.exe"
        "wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1"
        "wget https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerUp/PowerUp.ps1"
        "wget https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_amd64.gz"
        "wget https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_windows_amd64.gz"
        "wget https://github.com/valorisa/socat-1.8.0.0_for_Windows/raw/main/socat-1.8.0.0.zip"
        "wget https://github.com/antonioCoco/RunasCs/releases/download/v1.5/RunasCs.zip"
        "wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh"
        "wget https://github.com/prodigiousMind/revshell/archive/refs/heads/main.zip"
        "wget https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit"
        "wget https://github.com/ly4k/PwnKit/raw/main/PwnKit32"
        "wget https://github.com/icsharpcode/AvaloniaILSpy/releases/download/v7.2-rc/Linux.x64.Release.zip"
        "wget https://github.com/RedSiege/WMImplant/raw/master/WMImplant.ps1"
        "wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-client_linux"
        "wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-client_windows.exe"
        "wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-client_macos"
        "wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.7.2-alpha/ligolo-ng_proxy_0.7.2-alpha_linux_amd64.tar.gz"
        "wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.7.2-alpha/ligolo-ng_agent_0.7.2-alpha_windows_amd64.zip"
        "wget https://github.com/dafthack/DomainPasswordSpray/raw/master/DomainPasswordSpray.ps1"
        "wget https://github.com/DeimosC2/DeimosC2/releases/download/1.1.0/DeimosC2_linux.zip"
        "wget https://github.com/DeimosC2/DeimosC2/releases/download/1.1.0/DeimosC2_windows.zip"
        "wget https://github.com/Dliv3/Venom/releases/download/v1.1.0/Venom.v1.1.0.7z"
        "wget https://github.com/P1-Team/AlliN/raw/main/AlliN.py"
        "wget https://github.com/baiyies/PowerOneLiner/raw/main/one_liner_generator.py"
        "wget https://raw.githubusercontent.com/jakub-przepiora/ps-scan-Prestashop-scanner/refs/heads/main/ps-scan.py"
        "wget https://raw.githubusercontent.com/samratashok/nishang/refs/heads/master/Shells/Invoke-PowerShellTcp.ps1"
        "wget https://raw.githubusercontent.com/rebootuser/LinEnum/refs/heads/master/LinEnum.sh"
        "wget https://eternallybored.org/misc/netcat/netcat-win32-1.12.zip"
        "wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/refs/heads/dev/Recon/PowerView.ps1"
    )

    # Imprime los últimos argumentos de cada comando
    echo "    [+] Seleccione el número del comando que desea descargar:"
    for i in "${!commands[@]}"; do
        echo "$i: ${commands[$i]##* }"
    done

    # Solicita al usuario que ingrese el número del comando que desea ejecutar
    read -p "    [+] Ingrese el número del comando: " choice

    # Verifica que la entrada sea un número válido
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 0 && choice < ${#commands[@]} )); then
        echo "    [*] Ejecutando: ${commands[$choice]}"
        ${commands[$choice]}
    else
        echo "    [-] Entrada no válida. Por favor, ingrese un número entre 0 y $((${#commands[@]} - 1))."
    fi
}
download
# Preguntar al usuario si quiere salir
read -p "    [?] ¿Deseas salir del script? (s/n): " respuesta

if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
    echo "    [*] Saliendo del script..."
    exit 0
else
    download
    
fi

# git clone https://github.com/honze-net/pwntomate.git ./pyautomate its great but dont work on python3 so i change to work in python3, so i add permanent to sessions directory if you want can clone the original proyect here.