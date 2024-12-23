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
        "git clone https://github.com/amriunix/CVE-2007-2447.git .exploit/CVE-2007-2447"
        "git clone https://github.com/m3m0o/chamilo-lms-unauthenticated-big-upload-rce-poc.git .exploit/CVE-2023-4220"
        "git clone https://github.com/kimusan/pkwner.git .exploit/CVE-2021-4034"
        "git clone https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253.git .exploit/CVE-2023-30253"
        "git clone https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit .exploit/CVE-2022-37706"
        "git clone https://github.com/Arinerron/CVE-2022-0847-DirtyPipe-Exploit.git .exploit/CVE-2022-0847"
        "git clone https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits .exploit/CVE-2022-0847-2"
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
        "git clone https://github.com/6abd/horus.git .exploit/horus_osint"
        "git clone https://github.com/whoamipwn/troll-a .exploit/troll_a_extract_secrets"
        "git clone https://github.com/n0mi1k/apk2url.git .exploit/apk2url"
        "git clone https://github.com/edoardottt/pphack.git .exploit/pphack_scan_prototipepolution"
        "git clone https://github.com/caio-ishikawa/netscout.git .exploit/netscout_osint"
        "git clone https://github.com/nemesida-waf/waf-bypass.git .exploit/waf_byspass"
        "git clone https://github.com/sAjibuu/Upload_Bypass.git .exploit/upload_bypass"
        "git clone https://github.com/justakazh/sicat .exploit/sicat_vuln_hunter"
        "git clone https://github.com/r0oth3x49/ghauri.git .exploit/ghauri_sqli"
        "git clone https://github.com/Mr-Robert0/Logsensor.git .exploit/logsensor_login_scanner_vuln"
        "git clone https://github.com/mhaskar/Octopus.git .exploit/octopus_c2_powershells"
        "git clone https://github.com/blacklanternsecurity/bbot .exploit/bbot_osint"
        "git clone https://github.com/epinna/weevely3.git .exploit/weevely_phpshell"
        "git clone https://github.com/RedSiege/Jigsaw.git .exploit/jigsaw_RandomizeShellcodes"
        "git clone https://github.com/naksyn/Pyramid.git .exploit/Pyramid"
        "git clone https://github.com/naksyn/ModuleShifting.git .exploit/ModuleShifting_usewith_Pyramid"
        "git clone https://github.com/xkaneiki/CVE-2023-0386.git .exploit/CVE-2023-0386"
        "git clone https://github.com/ropnop/kerbrute.git .exploit/kerbrute"
        "git clone https://github.com/CravateRouge/bloodyAD.git .exploit/bloodyAD"
        "git clone https://github.com/4w4k3/BeeLogger.git .exploit/Beelogger"
        "git clone https://github.com/optiv/Ivy.git .exploit/Ivi_shellcodes"
        "git clone https://github.com/H454NSec/CVE-2023-42793.git .exploit/CVE-2023-42793"
        "git clone https://github.com/stealthcopter/deepce.git .exploit/deepce_dockerpentest"
        "git clone https://github.com/Veil-Framework/Veil.git .exploit/Veil"
        "git clone https://github.com/ultrasecurity/Storm-Breaker.git .exploit/Storm_breaker"
        "git clone https://github.com/devanshbatham/paramspider .exploit/paramspider"
        "git clone https://github.com/S3cur3Th1sSh1t/WinPwn.git .exploit/WinPwn"
        "git clone https://github.com/t3l3machus/hoaxshell.git .exploit/hoaxshell"
        "git clone https://github.com/hannob/snallygaster.git .exploit/snallygaster"
        "git clone https://github.com/proabiral/inception.git .exploit/incpetion"
        "git clone https://github.com/projectdiscovery/pdtm.git .exploit/pdtm_installnulei"
        "git clone https://github.com/vulnersCom/getsploit.git .exploit/getsploit"
        "git clone https://github.com/m8sec/enumdb.git .exploit/enumdb"
        "git clone https://github.com/commixproject/commix.git .exploit/commix"
        "git clone https://github.com/codingo/NoSQLMap.git .exploit/nosqlmap"
        "git clone https://github.com/michelin/ChopChop.git .exploit/ChopChop"
        "git clone https://github.com/SecWiki/windows-kernel-exploits.git .exploit/windows-kernel-exploits"
        "git clone https://github.com/DeimosC2/DeimosC2.git .exploit/DeimosC2"
        "git clone https://github.com/t3l3machus/Villain.git .exploit/villain"
        "git clone https://github.com/cobbr/Covenant.git .exploit/CovenantC2"
        "git clone https://github.com/jm33-m0/emp3r0r.git .exploit/emp3r0r"
        "git clone https://github.com/bats3c/shad0w.git .exploit/shadowC2"
        "git clone https://github.com/unix-thrust/beurk.git .exploit/beurk_rootkit"
        "git cloen https://github.com/arthaud/git-dumper.git .exploit/git-dumper"
        "git clone https://github.com/ropnop/windapsearch.git .exploit/windap"
        "git clone https://github.com/cytopia/badchars.git .exploit/badchars"
        "git clone https://github.com/worawit/MS17-010.git .exploits/MS17EternalBlue"
        "git clone https://github.com/synacktiv/CVE-2023-35001.git .exploit/CVE-2023-35001"
        "git clone https://github.com/jakabakos/CVE-2023-36664-Ghostscript-command-injection.git .exploit/CVE-2023-36664"
        "git clone https://github.com/dirkjanm/adconnectdump.git .exploit/adconnectdump"
        "git clone https://github.com/SafeBreach-Labs/EDRaser .exploit/EDRaser"
        "git clone https://github.com/SafeBreach-Labs/pwndsh.git .exploit/pwndsh"
        "git cloen https://github.com/SafeBreach-Labs/QuickShell.git .exploit/QuickShell"
        "git clone https://github.com/MHaggis/notes.git .exploit/notes_powershellz"
        "git clone https://github.com/Flangvik/SharpCollection.git .exploit/SharpCollection"
        "git clone https://github.com/antonioCoco/RoguePotato.git .exploit/RougePotato"
        "git clone https://github.com/BloodHoundAD/BloodHound.git .exploit/BloodHoud"
        "git clone https://github.com/S3cur3Th1sSh1t/PowerSharpPack.git .exploit/PowerSharpPack"
        "git clone https://github.com/garrettfoster13/sccmhunter.git .exploit/sccmhunter"
        "git clone https://github.com/roughiz/Webmin-1.910-Exploit-Script.git .exploit/Webmin-1.910-Exploit"
        "git clone https://github.com/liquidsec/pyOracle2.git .exploit/pyOracle2"
        "git clone https://github.com/Friends-Security/SharpExclusionFinder.git .exploit/SharpExclusionFinder"
        "git clone https://github.com/paranoidninja/0xdarkvortex-MalwareDevelopment.git .exploit/prometheus"
        "git clone https://github.com/edunavajas/linux-personalized.git .exploit/linux-personalized "
        "git clone https://github.com/dafthack/MailSniper.git .exploit/mailSniper"
        "git clone https://github.com/lefayjey/linWinPwn.git .exploit/linWinPwn"
        "git clone https://github.com/Raptoratack/ADTools.git .exploit/ADT00lz"
        "git clone https://github.com/ticarpi/jwt_tool.git .exploit/jwt_tool"
        "git clone https://github.com/RedSiege/Chromatophore.git .exploit/Chromatophore"
        "git clone https://github.com/RedSiege/WMIOps.git .exploit/WMIOps"
        "git clone https://github.com/makuga01/CVE-2024-48990-PoC.git .exploit/CVE-2024-48990-PoC"
        "git clone https://github.com/r3dcl1ff/nuclei-templates.git .exploit/nuclei-templates"
        "git clone https://github.com/S3cur3Th1sSh1t/Creds.git .exploit/scripts_variados"
        "git clone https://github.com/incredibleindishell/BruteShark.git .exploit/BlueShark"
        "git clone https://github.com/Hackplayers/PsCabesha-tools.git .exploit/PsCabeshaps1"
        "git clone https://github.com/clymb3r/PowerShell.git .exploit/PowerShell_privesc"
        "git clone https://github.com/grisuno/binary.git .exploit/grisun0_compiled_windows_binaries"
        "git clone https://github.com/Leo4j/Amnesiac.git .exploit/Amnesiac"
        "git clone https://github.com/JoelGMSec/AutoRDPwn.git .exploit/AutoRDPwn"
        "git clone https://github.com/JoelGMSec/Kitsune.git .exploit/Kitsune"
        "git clone https://github.com/owalid/consul-rce.git .exploit/consul_rce"
        "git clone https://github.com/t3l3machus/psudohash.git .exploit/pseudohash"
        "git clone https://github.com/cxnturi0n/convoC2.git .exploit/teamsc2convoc2"
        "git clone https://github.com/FuzzySecurity/Sharp-Suite.git .exploit/SharpSuit"
        "git clone https://github.com/FuzzySecurity/DLL-Template.git .exploit/dlltemplate"
        "git clone https://github.com/FuzzySecurity/Unix-PrivEsc.git .exploit/unixprivesc"
    )
    
    echo "    [+] Choice the number option to clone:"
    for i in "${!commands[@]}"; do
        echo "    [º] $i: ${commands[$i]##* }"
    done
    read -p "    [*] Enter the choice: " choice
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 0 && choice < ${#commands[@]} )); then
        echo "    [*] Executing: ${commands[$choice]}"
        ${commands[$choice]}
    else
        echo "    [-] error choice a number between 0 or $((${#commands[@]} - 1))."
    fi
}
download
read -p "    [-] do you want exit? (y/n): " respuesta

if [[ "$respuesta" == "y" || "$respuesta" == "Y" ]]; then
    echo "    [-] Exit from LazyDownloadScript..."
    exit 0
else
    download
    
fi
