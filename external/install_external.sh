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

download() {
    # Define la lista de comandos git clone
    commands=(
        "git clone https://github.com/amriunix/CVE-2007-2447.git .exploits/CVE-2007-2447"
        "git clone https://github.com/m3m0o/chamilo-lms-unauthenticated-big-upload-rce-poc.git .exploits/CVE-2023-4220"
        "git clone https://github.com/kimusan/pkwner.git .exploits/CVE-2021-4034"
        "git clone https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253.git .exploits/CVE-2023-30253"
        "git clone https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit .exploits/CVE-2022-37706"
        "git clone https://github.com/Arinerron/CVE-2022-0847-DirtyPipe-Exploit.git .exploits/CVE-2022-0847"
        "git clone https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits .exploits/CVE-2022-0847-2"
        "git clone https://github.com/joshuavanderpoll/CVE-2021-3129.git .exploit/CVE-2021-3129"
        "git clone https://github.com/xaitax/CVE-2024-21413-Microsoft-Outlook-Remote-Code-Execution-Vulnerability.git .exploit/CVE-2024-21413"
        "git clone https://github.com/peass-ng/PEASS-ng.git .exploit/PEASS-ng"
        "git clone https://github.com/elweth-sec/CVE-2023-2255.git .exploit/CVE-2023-2255"
        "git clone https://github.com/Hunt3r0x/CVE-2021-31630-HTB.git .exploit/CVE-2021-31630"
        "git clone https://github.com/AAlx0451/OneShot.git .exploit/WPSPixieDustAttack"
        "git clone https://github.com/chompie1337/SMBGhost_RCE_PoC.git .exploit/CVE-2020-0796"
        "git clone https://github.com/BloodHoundAD/SharpHound.git .exploit/SharpHound"
        "git clone https://github.com/spipm/Depix.git .exploit/Despixelation"
        "git clone https://github.com/padovah4ck/PSByPassCLM.git .exploit/PSByPassCLM"
        "git clone https://github.com/r3motecontrol/Ghostpack-CompiledBinaries .exploit/Ghostpack-CompiledBinaries"
        "git clone https://github.com/topotam/PetitPotam.git .exploit/PetitPotam"
        "git clone https://github.com/samratashok/nishang.git .exploit/nishang"
        "git clone https://github.com/antonioCoco/RunasCs.git .exploit/runascs"
        "git clone https://github.com/l0n3m4n/CVE-2024-6387.git .exploit/CVE-2024-6387"
        "git clone https://github.com/Syzik/DockerRegistryGrabber.git .exploit/DockerRegistryGrabber"
        "git clone https://github.com/ch4n3-yoon/django-pickleserializer-rce-poc.git .exploit/django-pickleserializer-rce-poc"
        "git clone https://github.com/xkaneiki/CVE-2023-0386 .exploit/CVE-2023-0386"
        "git clone https://github.com/7etsuo/CVE-2023-38408.git .exploit/CVE-2023-38408"
        "git clone https://github.com/prodigiousMind/CVE-2023-41425.git .exploit/CVE-2023-41425"
        "git clone https://github.com/whotwagner/logrotten.git .exploit/logrotten"
        "git clone https://github.com/urbanadventurer/username-anarchy.git .exploit/username_anarchy"
        "git clone https://github.com/telekom-security/tpotce.git .exploit/honeypots_tpotce"
    )
    # Imprime los últimos argumentos de cada comando
    echo "    [+] Seleccione el número del comando que desea clonar:"
    for i in "${!commands[@]}"; do
        echo "    [º] $i: ${commands[$i]##* }"
    done

    # Solicita al usuario que ingrese el número del comando que desea ejecutar
    read -p "    [*] Ingrese el número del comando: " choice

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
read -p "    [-] ¿Deseas salir del script? (s/n): " respuesta

if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
    echo "    [-] Saliendo del script..."
    exit 0
else
    download
    
fi
