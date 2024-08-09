# Documentation by readmeneitor.py

## print_error
funcion para imprimir un error

## print_msg
funcion para imprimir un msg

## print_warn
funcion para imprimir un warn

## signal_handler
signal_handler it's to handle signal  of  control + c and show a message , how to exit, using , exit, q or qa commands. 

## check_rhost
chek if rhost is defined. and show a mesage of error if not

## check_lhost
chek if lhost is defined. and show a mesage of error if not

## check_lport
chek if lport is defined. and show a mesage of error if not

## is_binary_present
internal function to verify if binary is presents in O.S.

## handle_multiple_rhosts
internal function to implement multiples rhost to operate. 

## check_sudo
chek if is sudo privileges, and if not respawn the script with sudo privileges. 

## activate_virtualenv
Ejecutar el shell interactivo con el entorno virtual activado

## parse_proc_net_file
internal function to parse proc/net file

## get_open_ports
internal function to get open ports in the O.S.

## find_credentials
Expresión regular para encontrar posibles credenciales

## xor_encrypt_decrypt
XOR Encrypt or Decrypt data with a given key

## wrapper
internal wrapper of internal function to implement multiples rhost to operate. 

## __init__
Inicializador de la clase LazyOwnShell

## default
Handle undefined commands (including aliases).

## one_cmd
internal function to execute commands

## set
Set a parameter value. Usage: set <parameter> <value>

## show
Show the current parameter values

## list
List all available scripts in modules directory, they can use apart from the framework too.

## run
Run a specific LazyOwn script to see all scripts to run see: list or help list

## lazysearch
Run internal module modules/lazysearch.py 

## lazysearch_gui
Run internal module modules/LazyOwnExplorer.py

## lazyown
Run internal module modules/lazyown.py

## update_db
Run internal module modules/update_db.sh to update the db of binary exploitables from gtofbins

## lazynmap
Run internal module modules/lazynmap.sh implements multiple scans with nmap

## lazywerkzeugdebug
test werkzeug in debugmode Run internal module modules/lazywerkzeug.py

## lazygath
Run internal module modules/lazygat.sh

## lazynmapdiscovery
Run internal module modules/lazynmap.sh implements multiple scans with nmap

## lazysniff
Run internal module modules/lazysniff.py

## lazyftpsniff
Run internal module modules/lazyftpsniff.py

## lazynetbios
Run internal module modules/lazynetbios.py

## lazyhoneypot
Run internal module modules/lazyhoneypot.py

## lazygptcli
Run internal module modules/lazygptcli.py

## lazysearch_bot
Run internal module modules/lazysearch_bot.py

## lazymetaextract0r
Run internal module modules/lazyown_metaextract0r.py

## lazyownratcli
Run internal module modules/lazyownclient.py

## lazyownrat
Run internal module modules/lazyownserver.py

## lazybotnet
Run internal module modules/lazybotnet.py

## lazylfi2rce
Run internal module modules/lazylfi2rce.py

## lazylogpoisoning
Run internal module modules/lazylogpoisoning.py

## lazybotcli
Run internal module modules/lazybotcli.py

## lazyssh77enum
Run internal module modules/lazybrutesshuserenum.py

## lazyburpfuzzer
Run internal module modules/lazyown_burpfuzzer.py

## lazyreverse_shell
Run internal module modules/lazyreverse_shell.sh

## lazyarpspoofing
Run internal module modules/lazyarpspoofing.py

## lazyattack
Run internal module modules/lazyatack.sh

## lazymsfvenom
Run alias of msfvenom alias venom

## lazyaslrcheck
Aslr check if is active 

## lazypathhijacking
create a pathhijacking attack

## script
Run a script with the given arguments

## command
Run a command and print output in real-time

## payload
Load parameters from payload.json

## exit
Exit the command line interface.

## fixperm
Fix Perm LazyOwn shell

## lazywebshell
LazyOwn shell

## getcap
try get capabilities :)

## getseclist
get seclist :D

## smbclient
Lazy SMBCLient

## smbmap
smbmap -H 10.10.10.3 [OPTIONS]

## getnpusers
sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt

## psexec
Lazy impacket-psexec administrator@

## rpcdump
rpcdump.py -p 135 10.10.11.24

## dig
dig version.bind CHAOS TXT @DNS

## cp
cp {exploitdb}DNS

## dnsenum
dnsenum --dnsserver 10.10.11.24 --enum -p 0 -s 0 -o sessions/subdomains.txt -f {dnswordlist} ghost.htb

## dnsmap
dnsmap --dnsserver 10.10.11.24 --enum -p 0 -s 0 -o sessions/subdomains.txt -f {dnswordlist} ghost.htb

## whatweb
whatweb

## enum4linux
enum4linux -a target

## nbtscan
sudo nbtscan -r target

## rpcclient
rpcclient -U "" -N 10.10.10.10

## nikto
nikto -h 10.10.10.10

## openssl_sclient
openssl s_client -connect  10.10.10.10

## ss
searchsploit alias

## wfuzz
lazy alias to wfuzz parameters are sub, iis and extra options to wfuzz ex --hl=7 to hide when are 7 lines of response, etc

## gobuster
Lazy gobuster

## addhosts
sudo -- sh -c -e "echo '10.10.11.23 permx.htb' >> /etc/hosts;

## cme
crackmapexec smb 10.10.11.24

## ldapdomaindump
ldapdomaindump -u 'domain.local\Administrator' -p 'passadmin123' 10.10.11.23

## bloodhound
bloodhound-python -c All -u 'usuario' -p 'password' -ns 10.10.10.10

## ping
ping -c 1 10.10.10.10

## gospider
try gospider

## arpscan
try arp-scan

## lazypwn
LazyPwn

## fixel
to fix perms

## smbserver
Lazy imacket smbserver

## sqlmap
Lazy sqlmap try sqlmap -wizard if don't know how to use requests.txt file always start with req and first parameter

## proxy
Small proxy to modify the request on the fly...

## createwebshell
Crea una webshell disfrazada de jpg en el directorio sessions/

## createrevshell
Crea un script en el directorio sessions con una reverse shell con los datos en lhost y lport

## createwinrevshell
Crea un script en el directorio sessions con una reverse shell con los datos en lhost y lport

## createhash
Crea un archivo hash.txt en el directorio sessions

## createcredentials
Crea un archivo credentials.txt en el directorio sessions el forato debe ser: user:password

## createcookie
Crea un archivo cookie.txt en el directorio sessions con el formato de una cookie válida.

## download_resources
download resources in sessions

## download_exploit
download exploits in external/.exploits/

## dirsearch
dirsearch -u http://url.ext/ -x 403,404,400

## john2hash
example: sudo john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt -format=Raw-SHA512

## hashcat
hashcat -a 0 -m mode hash /usr/share/wordlists/rockyou.txt

## responder
sudo responder -I tun0

## ip
ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [[96m" iface"[0m] "a[1] }' and copy de ip to clipboard :)

## rhost
Copy rhost to clipboard

## banner
Show the banner

## py3ttyup
copy to clipboard tipical python3 -c 'import pty; pty.spawn ... bla bla blah...

## rev
Copy a revshell to clipboard

## img2cookie
Copy a malicious img tag to clipboard

## disableav
visual basic script to try to disable antivirus

## conptyshell
Download ConPtyShell in sessions directory and copy to clipboard the command :D

## pwncatcs
run pwncat-cs -lp <PORT> :)

## find
copy to clipboard this command always forgot :) find / -type f -perm -4000 2>/dev/null

## sh
execute some command direct in shell to avoid exit LazyOwn ;)

## pwd
'echo -e "[\e[96m`pwd`\e[0m]\e[34m" && ls && echo -en "\e[0m"'

## qa
Exit fast without confirmation

## ignorearp
echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore

## ignoreicmp
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all

## acknowledgearp
echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore

## acknowledgeicmp
echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all

## clock
Show the time to go sleep xD

## ports
Get all ports local

## ssh
Conecta a un host SSH usando credenciales desde un archivo y el puerto especificado.

## cports
Genera un comando para mostrar puertos TCP y UDP, y lo copia al portapapeles.

## vpn
Open vpn like htb vpn

## id_rsa
create id_rsa file, open nano sessions/id_rsa, usage like this: id_rsa username, open nano and you paste the private key, and run ssh command

## www
Start a web server with python3

## wrapper
copy to clipboard some wrapper to lfi

## samrdump
impacket-samrdump -port 445 10.10.10.10

## snmpcheck
snmp-check 10.10.10.10

## hydra
hydra -f -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt 10.10.11.9 -s 5000 https-get /v2/

## smtpuserenum
sudo smtp-user-enum -M VRFY -U /usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt -t 10.10.10.10

## sshd
sudo systemctl start ssh

## nmapscripthelp
help to know nmap scripts: nmap --script-help 'snmp*'

## searchhash
help to know search hashcat hash types: hashcat -h | grep -i <ARGUMENT>

## clean
delete all from sessions

## pyautomate
pyautomate automatization of tools to pwn a target all rights https://github.com/honze-net/pwntomate

## alias
Imprime todos los alias configurados.

## tcpdump_icmp
se pone en escucha con la interfaz señalada por argumento ej: tcpdump_icmp tun0

## winbase64payload
Crea un payload encodeado en base64 especial para windows para ejecutar un ps1 desde lhost

## revwin
Crea un payload encodeado en base64 especial para windows para ejecutar un ps1 desde lhost

## asprevbase64
create a base64 rev shell in asp, you need pass the base64 encodd payload, see help winbase64payload to create the payload base64 encoded

## rubeus
copia a la clipboard la borma de descargar Rubeus

## socat
run socat in ip:port seted by argument config the port 1080 in /etc/proxychains.conf

## chisel
run download_resources command to download and run chisel :D like ./chisel_linux_amd64 server -p 3333 --reverse -v

## msf
automate msfconsole scan or rev shell

## encrypt
Encrypt a file using XOR. Usage: encrypt <file_path> <key>

## decrypt
Decrypt a file using XOR. Usage: decrypt <file_path> <key>

## get_output
Devuelve la salida acumulada

