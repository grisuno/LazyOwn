#!/usr/bin/env python3
"""Auto-generated MCP tool handlers from command_index.json.

DO NOT EDIT BY HAND.  Re-generate with:
    python3 skills/mcp_tool_generator.py

This file is imported by lazyown_mcp.py to close the coverage gap between the 148 hand-written handlers and the 670+ CLI commands.
"""

from __future__ import annotations

from typing import Any


_COMMAND_MAP: dict[str, str] = {
    "lazyown_EOF": "Handle the end-of-file (EOF) condition",
    "lazyown_GET": "Execute the GET command",
    "lazyown_OPTIONS": "Execute the OPTIONS command",
    "lazyown_POST": "Execute the POST command",
    "lazyown_acknowledgearp": "Configures the system to acknowledge ARP requests by setting a kernel parameter",
    "lazyown_acknowledgeicmp": "Configures the system to respond to ICMP echo requests by setting a kernel parameter",
    "lazyown_aclpwn_py": "Executes the aclpwn.py tool to find and exploit ACL paths for privilege escalation in an Active Directory environment",
    "lazyown_ad_ldap_enum": "Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers)",
    "lazyown_adcs_check": "Check Active Directory Certificate Services for ESC1-ESC8 vulnerabilities",
    "lazyown_add2find": "Add a new custom command to the 'find' system, saved in user_commands.json",
    "lazyown_addalias": "Add a new alias with support for placeholders like {rhost}, {lhost}, {lport}, etc",
    "lazyown_addcli": "Add a client to execute c2 commands",
    "lazyown_addhosts": "Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name",
    "lazyown_addspn_py": "Executes the addspn.py tool to manage Service Principal Names (SPNs) on Active Directory accounts via LDAP",
    "lazyown_addusers": "Opens or creates the users.txt file in the sessions directory for editing using nano",
    "lazyown_adgetpass": "Generate a PowerShell script to extract Azure AD Connect credentials",
    "lazyown_adsso_spray": "Performs a password spray attack on Azure Active Directory Seamless Single Sign-On (SSO) using a specified list of users",
    "lazyown_adversary": "LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in adversary.json",
    "lazyown_adversary_yaml": "Execute adversary from YAML in lazyadversaries/*.yaml",
    "lazyown_aes_pe": "Encrypt with AES and random key to PE EXE file, to usage with loaders",
    "lazyown_ai_playbook": "Generate an offensive playbook from Nmap CSV + KB + Ollama",
    "lazyown_ai_toggle": "Toggle the in-process AI assistant on or off",
    "lazyown_aliass": "Prints all configured aliases and their associated commands",
    "lazyown_allin": "Execute the AlliN.py tool with various scan modes and parameters",
    "lazyown_alterx": "Executes the 'alterx' command for subdomain enumeration on the provided self.params['domain']. If 'alterx'",
    "lazyown_amass": "Executes Amass to perform a passive enumeration on a given domain",
    "lazyown_android_apk": "Generate a malicious APK with reverse shell payload",
    "lazyown_android_enum": "Enumerate an Android device connected via ADB",
    "lazyown_apache_users": "Performs enumeration of users from a target system using `apache-users`",
    "lazyown_applocker_csc": "Generate a csc.exe compile-and-execute AppLocker bypass",
    "lazyown_applocker_installutil": "Generate an InstallUtil.exe AppLocker bypass payload",
    "lazyown_applocker_msbuild": "Generate an MSBuild.exe AppLocker bypass payload",
    "lazyown_applocker_mshta": "Generate an mshta.exe AppLocker bypass payload",
    "lazyown_applocker_presentation": "Generate a PresentationHost.exe AppLocker bypass reference",
    "lazyown_applocker_regsvcs": "Generate a Regsvcs.exe/Regasm.exe AppLocker bypass payload",
    "lazyown_applocker_rundll32": "Generate a rundll32.exe AppLocker bypass via SCT scriptlet",
    "lazyown_apropos": "Search for commands matching the given parameter in the cmd interface and optionally extend the search using the system's `apropos` command",
    "lazyown_apt_playbook": "List, validate, and run APT playbooks based on public threat reports",
    "lazyown_apt_proxy": "Configures the local machine with internet access to act as an APT proxy for a machine without internet access",
    "lazyown_apt_repo": "Creates a comprehensive local APT repository with enhanced dependency resolution",
    "lazyown_arjun": "Executes an Arjun scan on the specified URL for parameter discovery",
    "lazyown_arpscan": "Executes an ARP scan using `arp-scan`",
    "lazyown_ask": "Ask the AI a question with current session context pre-loaded",
    "lazyown_asprevbase64": "Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard",
    "lazyown_assign": "assign a parameter value, persist to payload.json and refresh aliases",
    "lazyown_atomic_agent": "Generates and synchronizes atomic agent scripts",
    "lazyown_atomic_gen": "Generates test and cleanup scripts for a given Atomic Red Team technique ID",
    "lazyown_atomic_lazyown": "Execute atomic red-team tests via LazyOwn",
    "lazyown_atomic_tests": "Executes Atomic Red Team tests based on user-selected platform and test",
    "lazyown_attack_plan": "Executes a multi-step APT simulation plan based on Atomic Red Team test IDs",
    "lazyown_attack_surface": "Generate an attack surface summary from recon data",
    "lazyown_audit_complete_keys": "Print payload-aware completion suggestions for a partial command",
    "lazyown_autoblody": "Executes the autobloody tool for automating Active Directory privilege escalation paths",
    "lazyown_automsf": "Try to check if Vulnerable using the module passed by argument of lazyown example automsf exploit/windows/iis/iis_webdav_upload_asp to use in metasploit",
    "lazyown_autopivot": "Auto-detect internal networks and set up pivot tunnels",
    "lazyown_back": "Leave the current module context",
    "lazyown_backdoor_factory": "Creates a backdoored executable using `backdoor-factory`",
    "lazyown_banner": "Show the banner",
    "lazyown_banners": "Manage custom banners for the framework",
    "lazyown_base64decode": "Decodes a Base64 encoded string",
    "lazyown_base64encode": "Encodes a given string into Base64 format",
    "lazyown_batchnmap": "Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans",
    "lazyown_bbot": "Executes a BBOT scan to perform various reconnaissance tasks",
    "lazyown_beaconcfg": "Generate a C2 beacon profile with traffic morphing and domain fronting",
    "lazyown_bin2shellcode": "Converts a binary file to a shellcode string in C or Nim format",
    "lazyown_binarycheck": "Performs various checks on a selected binary to gather information and protections",
    "lazyown_bitm": "Browser-in-the-Middle attack manager",
    "lazyown_blazy": "Command blazy: Installs and runs blazy for multi-vulnerability web application scanning",
    "lazyown_bloodhound": "Perform LDAP enumeration using bloodhound-python with credentials from a file",
    "lazyown_bloodyAD": "Execute the bloodyAD.py command for a specific user or all users listed in the users.txt file",
    "lazyown_breacher": "Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities",
    "lazyown_browse": "Open the sessions/ TUI browser",
    "lazyown_c2": "Handle C2 server setup and agent compilation",
    "lazyown_c2_beacon_cmd": "Queue a command for execution on a connected beacon",
    "lazyown_c2_beacons": "List all active beacon sessions with their last-seen timestamps",
    "lazyown_c2_implant": "Generate a compiled implant payload for the target platform",
    "lazyown_c2_keygen": "Generate a fresh AES-256 key for beacon encryption",
    "lazyown_c2_quickstart": "Quick C2 setup: generate key, prepare implant dir, print beacon commands",
    "lazyown_c2asm": "Display C and ASM code side by side in a curses-based interface",
    "lazyown_cacti_exploit": "Automates the exploitation of the Cacti version 1.2.26 vulnerability",
    "lazyown_caldera": "Installs and starts the Caldera server",
    "lazyown_caldera_export": "Export a LazyOwn playbook to CALDERA ability YAML",
    "lazyown_caldera_import": "Import CALDERA abilities into LazyOwn playbooks",
    "lazyown_camphish": "Executes the camphish tool for Grab cam shots from target's phone front camera or PC webcam just sending a link",
    "lazyown_certipy": "Executes the Certipy tool to interact with Active Directory Certificate Services",
    "lazyown_certipy_ad": "Run certipy-ad against Active Directory Certificate Services",
    "lazyown_cewl": "Generate a wordlist from a website with cewl",
    "lazyown_chain": "Run autonomous exploitation chain: recon -> vuln -> exploit -> post-exploit",
    "lazyown_changeme": "Executes a changeme scan on a specified target URL or host",
    "lazyown_check_update": "Checks for updates by comparing the local version with the remote version",
    "lazyown_chisel": "Run chisel for quick tunneling",
    "lazyown_cicd_scan": "Scan CI/CD platform for security misconfigurations",
    "lazyown_cicd_secrets": "Scan build log for leaked secrets",
    "lazyown_clean": "Deletes files and directories in the `sessions` directory, excluding specified files and directories",
    "lazyown_clean_ad": "Clear Active Directory event logs and cached Kerberos tickets",
    "lazyown_clock": "Displays the current date and time, and runs a custom shell script",
    "lazyown_clone_site": "Clone a website and serve the files in sessions/{url_cloned}",
    "lazyown_cloud_buckets": "Enumerate cloud storage buckets for a given prefix",
    "lazyown_cloud_enum": "Enumerate cloud provider metadata, storage, and IAM",
    "lazyown_cloud_iam": "Enumerate cloud IAM roles and policies",
    "lazyown_cloud_metadata": "Harvest cloud instance metadata (AWS IMDS, Azure, GCP)",
    "lazyown_cloud_scan": "Full cloud security scan: metadata + buckets + IAM enumeration",
    "lazyown_cme": "Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target",
    "lazyown_collab_join": "Print the multi-operator collaboration join URL and SSE endpoint",
    "lazyown_commix": "Runs commix for command injection testing",
    "lazyown_config_banner": "Open a Powerlevel10k-style wizard to toggle prompt segments",
    "lazyown_conptyshell": "Download ConPtyShell and prepare a PowerShell run command",
    "lazyown_container_detect": "Auto-detect container runtime and escape primitives",
    "lazyown_container_escape": "Check current container for known escape vectors",
    "lazyown_convert_remcomsvc_from_file": "Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice format, prints a sample, and saves it to sessions/remcomsvc.go. see lazyaddon \u2026",
    "lazyown_cover_tracks": "Run all anti-forensics operations in sequence",
    "lazyown_cp": "Copies a file from the ExploitDB directory to the sessions directory",
    "lazyown_cports": "Generates a command to display TCP and UDP ports and copies it to the clipboard",
    "lazyown_crack_cisco_7_password": "Crack a Cisco Type 7 password hash and display the plaintext",
    "lazyown_crack_hashes": "Crack password hashes from a file using John the Ripper or Hashcat",
    "lazyown_create_session_json": "Create the session JSON report file",
    "lazyown_create_synthetic": "Create a basic synthetic playbook from Nmap CSV when LLM fails",
    "lazyown_createcookie": "Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value",
    "lazyown_createcredentials": "Creates a `credentials.txt` file in the `sessions` directory with the specified username and password",
    "lazyown_createdll": "Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux",
    "lazyown_createhash": "Creates a `hash.txt` file in the `sessions` directory with the specified hash value and analyzes it using `Name-the-hash`",
    "lazyown_createjsonmachine": "Create a new JSON payload file based on the template provided in payload.json",
    "lazyown_createjsonmachine_batch": "Create multiple JSON payload files based on a CSV input file from HackerOne",
    "lazyown_createmail": "Generate email permutations based on a full name and self.params['domain'], then save them to a file",
    "lazyown_createpayload": "Generates an obfuscated payload to evade AV detection using the payloadGenerator tool. thanks to smokeme",
    "lazyown_createrevshell": "Create a bash reverse shell script in sessions/",
    "lazyown_createtargets": "Create targets file from nmap scan",
    "lazyown_createusers_and_hashs": "Command createusers_and_hashs: Extracts usernames and hashes from a dump file",
    "lazyown_createwebshell": "Create web shells (JPG-disguised PHP, p0wny-shell, ASP)",
    "lazyown_createwinrevshell": "Create a Windows reverse shell (PowerShell)",
    "lazyown_cred": "Display the credentials stored in the `credentials.txt` file and copy the password to the clipboard",
    "lazyown_cred_mark_failed": "Mark a credential as failed against a host",
    "lazyown_cred_reuse": "Analyze captured credentials and suggest spray targets",
    "lazyown_creds_py": "Extract credentials from a file or command output",
    "lazyown_cron": "Schedules a command to run at a specified time",
    "lazyown_crunch": "Generate wordlists with crunch",
    "lazyown_crystal_ball": "Analyze linpeas/winpeas output and rank privesc vectors with exact commands",
    "lazyown_ctx": "Print a single-line operator context: rhost, lhost, domain, phase, os, creds",
    "lazyown_cubespraying": "Command cubespraying: Automates the installation and usage of CubeSpraying for performing credential spraying attacks",
    "lazyown_cve": "Search for a CVE using the CIRCL API",
    "lazyown_d3monizedshell": "Executes the D3m0n1z3dShell tool for persistence in Linux",
    "lazyown_dacledit": "Execute the dacledit.py command for a specific user or all users listed in the users.txt file",
    "lazyown_darkarmour": "Uses the darkarmour tool to generate an undetectable version of a PE executable",
    "lazyown_dashboard": "Launch the full-screen LazyOwn operator dashboard (Textual TUI)",
    "lazyown_davtest": "Tests WebDAV server configurations using `davtest`",
    "lazyown_db_creds": "List or add credentials",
    "lazyown_db_export": "Export database table to CSV",
    "lazyown_db_hosts": "List or add hosts in the active workspace",
    "lazyown_db_import": "Import scan results into the database",
    "lazyown_db_init": "Initialize the database (creates schema if not exists)",
    "lazyown_db_loot": "List or add loot items",
    "lazyown_db_notes": "List or add notes",
    "lazyown_db_services": "List all services in the active workspace",
    "lazyown_db_status": "Show entity counts for the active workspace",
    "lazyown_db_vulns": "List or add vulnerabilities",
    "lazyown_db_workspace": "Manage workspaces (list, create, switch, delete)",
    "lazyown_dcomexec": "Executes the Impacket dcomexec tool to run commands on a remote system using DCOM",
    "lazyown_decode": "Decode a string using the specified shift value and substitution key",
    "lazyown_decrypt": "Decrypt an XOR-encrypted file using the matching key",
    "lazyown_depconfuse": "Scan a requirements.txt for dependency confusion candidates",
    "lazyown_depscan": "Scan a directory tree for dependency files and flag risks",
    "lazyown_detect_edr": "Generate commands to detect EDR/AV on the target",
    "lazyown_dig": "Executes the `dig` command to query DNS information",
    "lazyown_digdug": "Executes Dig Dug to inflate the size of an executable file, leveraging pre-configured settings",
    "lazyown_dirsearch": "Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL",
    "lazyown_disableav": "Create a VBS script to attempt disabling Windows Defender",
    "lazyown_dmitry": "This function constructs and executes a command for the 'dmitry' tool",
    "lazyown_dns_beacon": "Start a DNS tunneling beacon",
    "lazyown_dns_beacon_status": "Show status of all DNS beacons",
    "lazyown_dns_exfil_listen": "Start a DNS exfiltration listener on UDP port 53",
    "lazyown_dnschef": "Executes the DNSChef tool to monitor DNS queries and intercept responses",
    "lazyown_dnsenum": "Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain",
    "lazyown_dnsmap": "Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain",
    "lazyown_dnstool_py": "Executes the dnstool.py tool to modify Active Directory-integrated DNS records",
    "lazyown_docker_enum": "Enumerate Docker host: containers, images, privileges, mounts",
    "lazyown_doctor": "Preflight environment health check \u2014 verify the install is ready",
    "lazyown_dominion": "Execute a fully automated Active Directory domain takeover",
    "lazyown_download_c2": "Download a file from the C2 implant via the upload command",
    "lazyown_download_exploit": "Downloads and sets up an exploit, optionally serving via HTTP",
    "lazyown_download_malwarebazar": "Download a malware sample from MalwareBazaar using its SHA256 hash",
    "lazyown_download_resources": "Downloads resources into the `sessions` directory",
    "lazyown_downloader": "Generate a downloader command for files in the sessions directory",
    "lazyown_dpapi_blob": "Decrypt a DPAPI blob offline",
    "lazyown_dpapi_harvest": "Harvest all DPAPI-protected credentials from the local machine",
    "lazyown_dpapi_masterkeys": "List and extract DPAPI master keys",
    "lazyown_dploot": "Run dploot to loot DPAPI-protected secrets",
    "lazyown_dr0p1t": "Execute the Dr0p1t tool to create a stealthy malware dropper",
    "lazyown_duckyspark": "duckyspark Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucleus",
    "lazyown_edr_detect": "Detect EDR/AV products on the target",
    "lazyown_edr_profile": "Generate an evasion profile based on detected EDR",
    "lazyown_edr_script": "Generate a PowerShell EDR detection script",
    "lazyown_emp3r0r": "Command emp3r0r Downloads and sets up the Emperor server for local exploitation",
    "lazyown_empire": "Generates payloads using PowerShell Empire with various options",
    "lazyown_encode": "Encodes a string using the specified shift value and substitution key",
    "lazyown_encoderpayload": "Applies various obfuscations to a given command line string to create multiple obfuscated versions",
    "lazyown_encodewinbase64": "Encodes a given payload into a Base64 encoded string suitable for Windows PowerShell execution",
    "lazyown_encrypt": "Encrypt a file with XOR using a caller-supplied key",
    "lazyown_engage": "Drive a single target through the full kill-chain in one command",
    "lazyown_enum4linux": "Performs enumeration of information from a target Linux/Unix system using `enum4linux`",
    "lazyown_enum4linux_ng": "Performs enumeration of information from a target system using `enum4linux-ng`",
    "lazyown_eternal": "Automates the EternalBlue (MS17-010) exploitation process using Metasploit",
    "lazyown_evasion": "Generate and manage C2 evasion profiles",
    "lazyown_evasive": "Generate detection-evading payloads with multiple obfuscation strategies",
    "lazyown_evasive_payload": "Generate an evasive payload with automatic AV/EDR bypass",
    "lazyown_event_log": "Show recent EventBus events. Usage: event_log [N] [category]",
    "lazyown_evidence": "Encode the 'sessions/' tree into a video file or decode one back",
    "lazyown_evil_ssdp": "Runs evil-ssdp with various options and user-selected templates",
    "lazyown_evilwinrm": "Drive Evil-WinRM through password, hash or kerberos-only auth",
    "lazyown_excelntdonut": "Generates an Excel 4.0 (XLM) macro from a provided C# source file using EXCELntDonut",
    "lazyown_exe2bin": "Trasnform file .exe into binary file",
    "lazyown_exe2donutbin": "Trasnform file .exe into donut binary file",
    "lazyown_exfil_auto": "Auto-detect flags and sensitive files, then exfiltrate",
    "lazyown_exfil_discord": "Exfiltrate a file via Discord webhook",
    "lazyown_exfil_dns": "Exfiltrate data via DNS tunneling",
    "lazyown_exfil_gcs": "Upload a file to Google Cloud Storage",
    "lazyown_exfil_http": "Exfiltrate a file via HTTP POST to a controlled server",
    "lazyown_exfil_s3": "Upload a file to an AWS S3 bucket",
    "lazyown_exfil_start_server": "Start all required exfiltration listeners",
    "lazyown_exfil_telegram": "Exfiltrate a file via Telegram Bot API",
    "lazyown_exit": "Exit the command line interface",
    "lazyown_explore": "Show exploration coverage and addon/tool suggestions per service",
    "lazyown_extract_ports": "Extracts open ports and IP address information from a specified file",
    "lazyown_extract_yaml": "Extract YAML from an existing debug file and try to create a playbook",
    "lazyown_eyewitness": "Run EyeWitness for web screenshot capture",
    "lazyown_eyewitness_py": "Automates EyeWitness installation and execution without requiring user input",
    "lazyown_feroxbuster": "Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing",
    "lazyown_filtering": "Applies various filtering techniques to the given command line by modifying each character or word appropriately",
    "lazyown_finalrecon": "Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host",
    "lazyown_find": "Automates command execution based on a list of aliases and commands",
    "lazyown_finger_user_enum": "Executes the `finger-user-enum` tool for enumerating users on the target host",
    "lazyown_fixel": "Fixes file permissions and line endings in the project directories",
    "lazyown_fixperm": "Fix permissions for LazyOwn shell scripts",
    "lazyown_follina": "Run the Follina (CVE-2022-30190) exploit setup",
    "lazyown_form": "Open an interactive form for a known command. Usage: form <command>",
    "lazyown_ftp": "Connects to an ftp host using credentials from a file and a specified port",
    "lazyown_fuzz": "Executes a web server fuzzing script with user-provided parameters",
    "lazyown_fz": "Fuzzy command finder. Usage: fz [query]. Empty lists every command",
    "lazyown_gencert": "Generates a certificate authority (CA), client certificate, and client key",
    "lazyown_generate": "Generate a payload",
    "lazyown_generate_playbook": "Generates a playbook that integrates Atomic Red Team tests and MITRE ATT&CK techniques",
    "lazyown_generate_revshell": "Generate a reverse shell in various programming languages",
    "lazyown_generatedic": "Generates a wordlist based on a target name and a list of characters, with various combinations",
    "lazyown_getTGT": "Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided credentials",
    "lazyown_get_avaible_actions": "Get list de supported acctions",
    "lazyown_getadusers": "Run impacket-GetADUsers to enumerate AD accounts on the DC",
    "lazyown_getcap": "Retrieve and display file capabilities on the system",
    "lazyown_getnpusers": "sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt",
    "lazyown_getnthash_py": "Recover the NT hash from a Kerberos U2U TGS via PKINITtools",
    "lazyown_gets4uticket_py": "Executes the gets4uticket.py tool from PKINITtools to request an S4U2Self service ticket using Kerberos",
    "lazyown_getseclist": "Get the SecLists wordlist from GitHub",
    "lazyown_gettgtpkinit_py": "Executes the gettgtpkinit.py tool from PKINITtools to request a TGT using Kerberos PKINIT with a PFX or PEM certificate",
    "lazyown_getuserspns": "Run impacket-GetUserSPNs to request roastable service tickets",
    "lazyown_gitdumper": "Install 'git-dumper' if missing and pull a remote '.git' tree",
    "lazyown_gitlab_enum": "Enumerate a GitLab instance",
    "lazyown_gmsadumper": "Run gMSADumper to read gMSA password blobs visible to the user",
    "lazyown_gobuster": "Uses `gobuster` for directory and virtual host fuzzing based on provided parameters. Supports directory enumeration and virtual host discovery",
    "lazyown_god_nodes": "Show the most-connected nodes (\"god nodes\") from the graph",
    "lazyown_gospherus": "Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads for various services",
    "lazyown_gospider": "Try gospider for web spidering",
    "lazyown_gowitness": "Run gowitness for web screenshot capture",
    "lazyown_gpt": "Query GPT/Groq AI for analysis and reporting",
    "lazyown_graph": "Generates a graph from JSON payload files containing URL, RHOST, and RPORT",
    "lazyown_graph_overlay": "Open the graph overlay over the graphify knowledge graph",
    "lazyown_graudit": "Executes the graudit command to perform a static code analysis with the specified options",
    "lazyown_greatSCT": "Executes the GreatSCT tool for generating payloads that bypass antivirus and application whitelisting solutions",
    "lazyown_grep_log": "Grep recent command outputs. Usage: grep_log <pattern> [--cmd <name>]",
    "lazyown_grisun0": "Creates and copies a shell command to add a new user, assign a password, add the user to the sudo group, and switch to the user",
    "lazyown_grisun0w": "Creates and copies a PowerShell command to add a new user, assign a password, add the user to the Administrators group, and switch to the user",
    "lazyown_groq": "Send a prompt to the Groq API using the configured 'api_key'",
    "lazyown_gtfo": "Look up a binary in GTFOBins and LOLBas parquet knowledge bases",
    "lazyown_gym": "Red Team Gym \u2014 gamified pentest training with ELO scoring",
    "lazyown_h": "Open a new window within a tmux session using the LazyOwn RedTeam Framework",
    "lazyown_hashcat": "Run hashcat password cracking",
    "lazyown_hex2shellcode": "Convert raw hex payload from msfvenom into NASM-compatible shellcode format",
    "lazyown_hex_to_plaintext": "Converts hexadecimal data from a file to plain text",
    "lazyown_hooks": "Conditional hooks management \u2014 list, enable, disable, add, remove rules",
    "lazyown_hooks_add": "Add a new conditional hook rule (JSON string)",
    "lazyown_hooks_enable": "Enable or disable a hook rule",
    "lazyown_hooks_fire": "Manually fire a hook event for testing",
    "lazyown_hooks_list": "List all conditional hook rules",
    "lazyown_hooks_remove": "Remove a hook rule by name",
    "lazyown_hostdiscover": "Discover active hosts in a subnet by performing a ping sweep",
    "lazyown_hound": "Executes the hound tool for Hound is a simple and light tool for information gathering and capture exact GPS coordinates",
    "lazyown_http_exfil_server": "Start a minimal HTTP exfiltration receiver",
    "lazyown_httprobe": "Executes the httprobe tool to probe domains for working HTTP and HTTPS servers",
    "lazyown_hunt": "Run an autonomous exploitation chain against a target",
    "lazyown_hydra": "Run Hydra for online password attacks",
    "lazyown_id_rsa": "Create an SSH private key file and connect to a remote host using SSH",
    "lazyown_ignorearp": "Configures the system to ignore ARP requests by setting a kernel parameter",
    "lazyown_ignoreicmp": "Configures the system to ignore ICMP echo requests by setting a kernel parameter",
    "lazyown_iis_webdav_upload_asp": "(CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit",
    "lazyown_img2cookie": "Generates an XSS payload that steals cookies via an image tag",
    "lazyown_img2vid": "Generates an MP4 video from PNG images found in the sessions/captured_images directory",
    "lazyown_internet_proxy": "Configures the local machine with internet access to act as a proxy for a machine without internet access",
    "lazyown_ip": "Displays IP addresses of network interfaces and copies the IP address from the `tun0` interface to the clipboard",
    "lazyown_ip2asn": "Command to get ASN for a given IP address",
    "lazyown_ip2hex": "Convert an IPv4 address into its hexadecimal representation",
    "lazyown_ipinfo": "Retrieves detailed information about an IP address using the ARIN API",
    "lazyown_ipp": "Displays IP addresses of network interfaces and prints the IP address from the `tun0` interface",
    "lazyown_issue_command_to_c2": "Exec command in the client using the C2. download: command you must put the file in sessions/temp_upload or use download_c2 command",
    "lazyown_ivy": "Generates payloads using Ivy with various options. Ivy is a payload creation framework for the execution of arbitrary VBA (macro) source code directly in memor\u2026",
    "lazyown_jenkins_enum": "Enumerate a Jenkins instance",
    "lazyown_john2hash": "Convert a hash to John the Ripper format",
    "lazyown_john2keepas": "List all .kdbx files in the 'sessions' directory, let the user select one, and run the",
    "lazyown_john2zip": "List all .zip files in the 'sessions' directory, let the user select one, and run the command",
    "lazyown_jwt_tool": "Uses the jwt_tool to analyze, tamper, or exploit JSON Web Tokens (JWTs)",
    "lazyown_k8s_enum": "Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC",
    "lazyown_k8s_pods": "List Kubernetes pods with security-relevant details",
    "lazyown_k8s_secrets": "List and decode Kubernetes secrets",
    "lazyown_karma": "Show ELO score, karma rank and exploration progress for this operator",
    "lazyown_keepass": "Open a .kdbx file and print the titles and contents of all entries. The password can be provided through",
    "lazyown_kerbrute": "Executes the Kerbrute tool to enumerate user accounts against a specified target self.params['domain'] controller",
    "lazyown_kick": "Handles the process of sending a spoofed ARP packet to a specified IP address with a given MAC address",
    "lazyown_knokknok": "Send special string to trigger a reverse shell, with the command 'c2 client_name'",
    "lazyown_krbrelayx_py": "Executes the krbrelayx.py tool for Kerberos relaying or unconstrained delegation abuse",
    "lazyown_kusa": "Runs the Kusanagi payload generator",
    "lazyown_l00t": "Unified loot: show, search, reuse, graph, and mark credentials",
    "lazyown_lab": "Manage local CTF practice labs",
    "lazyown_lateral_mov_lin": "Perform lateral movement by downloading and installing LazyOwn on a remote Linux machine",
    "lazyown_launchpad": "Searches for packages on Launchpad based on the provided search term and extracts codenames from the results. The distribution is extracted from the search ter\u2026",
    "lazyown_lazy_payload_keys": "List the keys currently present in the parent shell's payload",
    "lazyown_lazy_runtime": "Print interpreter, platform and core LazyOwn paths",
    "lazyown_lazynmap": "Runs the internal module `modules/lazynmap.sh` with target mode",
    "lazyown_lazypwn": "Executes the LazyPwn automated exploitation script",
    "lazyown_lazyreport": "Generate a professional red team report from session data",
    "lazyown_lazyscript": "Executes commands defined in a lazyscript file",
    "lazyown_lazywebshell": "Run LazyOwn webshell server on port 8888",
    "lazyown_ldapdomaindump": "Dumps LDAP information using `ldapdomaindump` with credentials from a file",
    "lazyown_ldapsearch": "Executes an LDAP search against a target remote host (self.params['rhost']) and saves the results",
    "lazyown_les": "Run Linux Exploit Suggester against a kernel version",
    "lazyown_lfi": "Exploits a potential Local File Inclusion (LFI) vulnerability by crafting",
    "lazyown_ligolo": "Run Ligolo-ng for advanced pivoting",
    "lazyown_links": "Displays a list of useful links and allows the user to select and copy a link to the clipboard",
    "lazyown_linpeas": "Serve 'linpeas.sh' over HTTP and print the target one-liner",
    "lazyown_list": "Lists all available scripts in the modules directory",
    "lazyown_listaliases": "List all available aliases",
    "lazyown_listener": "Manage C2 listeners: list, add, start, stop, remove",
    "lazyown_listener_go": "Configures and starts a listener for a specified victim",
    "lazyown_listener_py": "Configures and starts a listener for a specified victim",
    "lazyown_llm_budget": "Show the LLM daily cost budget, per call token cap, and current spend",
    "lazyown_load_session": "Load the session from the sessionLazyOwn.json file and display the status of various parameters",
    "lazyown_lock_target": "Acquire an advisory lock on a target to prevent tool collisions",
    "lazyown_login": "Authenticate against users.json (same users as lazyc2.py)",
    "lazyown_logout": "Log out the current CLI operator and clear the remember-me token",
    "lazyown_lol": "Exploits a target by injecting a malicious payload and collecting admin information",
    "lazyown_lookupsid": "Executes the Impacket lookupsid tool to enumerate SIDs on a target system",
    "lazyown_lookupsid_py": "Executes the LookupSID tool to perform SID enumeration on a target system",
    "lazyown_loot": "Alias for 'l00t' \u2014 unified loot (show/search/reuse/graph/mark)",
    "lazyown_loxs": "Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning",
    "lazyown_lynis": "Performs a Lynis audit on the specified remote system",
    "lazyown_macos_keychain": "Extract secrets from the macOS Keychain",
    "lazyown_macos_persist": "Generate macOS persistence via LaunchAgent",
    "lazyown_macos_tcc": "Generate macOS TCC (Transparency, Consent, Control) bypass",
    "lazyown_magicrecon": "Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and vulnerability scanning on specified targets",
    "lazyown_makerc": "Record session commands to a resource script",
    "lazyown_malwarebazar": "Search Malware Bazaar for malware samples",
    "lazyown_marketplace": "Discover and install community plugins, addons, and tools",
    "lazyown_marketplace_config": "Interactive marketplace manager (curses TUI)",
    "lazyown_medusa": "Run Medusa for online password attacks",
    "lazyown_metabigor": "Executes Metabigor commands for OSINT and scanning tasks with guided input or predefined arguments",
    "lazyown_mfa_bypass": "Enumerate and test MFA bypass techniques",
    "lazyown_mimikatzpy": "Run Mimikatz over Python (impacket style)",
    "lazyown_mitre_test": "Interacts with the MITRE ATT&CK framework using the STIX 2.0 format",
    "lazyown_mkrc": "Alias for makerc \u2014 record commands to a script",
    "lazyown_morse": "Interactive Morse Code Converter",
    "lazyown_mqtt_check_py": "Executes the MQTT check tool to verify credentials on a target system with optional SSL",
    "lazyown_ms08_067_netapi": "SMB CVE-2008-4250. Vulnerable using the module ms08_067_netapi of metasploit",
    "lazyown_msf": "Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells, and creating payloads",
    "lazyown_msfpc": "Generates payloads using MSFvenom Payload Creator (MSFPC)",
    "lazyown_msfrpc": "Connects to the msfrpcd daemon and allows remote control of Metasploit",
    "lazyown_msfshellcoder": "Generate shellcode in C format using msfvenom for either a custom command or a reverse shell payload",
    "lazyown_mssqlcli": "Attempts to connect to an MSSQL server using the mssqlclient.py tool with Windows authentication",
    "lazyown_mutate_shellcode": "Apply polymorphic mutation to shellcode for signature evasion",
    "lazyown_my_playbook": "Generates a playbook from your custom technique database",
    "lazyown_name_the_hash": "Identify hash type using nth after retrieving it with get_hash()",
    "lazyown_nano": "Opens or creates the file using line in the sessions directory for editing using nano",
    "lazyown_nbtscan": "Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range",
    "lazyown_nc": "Netcat listener or connect",
    "lazyown_neighbors": "Show graph neighbors of a node or command from the graphify graph",
    "lazyown_net_rpc_addmem": "Executes the net rpc group addmem command to add a user to a specified group in Active Directory",
    "lazyown_netexec": "Executes netexec with various options for network protocol operations",
    "lazyown_netview": "Executes the Impacket netview tool to list network shares on a specified target",
    "lazyown_news": "Show the Hacker News in the terminal",
    "lazyown_next": "Show next-step recommendations or execute the active autosuggest",
    "lazyown_ngrok": "Start ngrok tunnel",
    "lazyown_nikto": "Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host",
    "lazyown_nmapscript": "Perform an Nmap scan using a specified script and port",
    "lazyown_nmapscripthelp": "Provides help to find and display information about Nmap scripts",
    "lazyown_note": "Capture a quick operator note attached to the current target and phase",
    "lazyown_notify": "Command to trigger a toastr-like notification",
    "lazyown_ntpdate": "Synchronizes the system clock with a specified NTP server",
    "lazyown_nuclei": "Executes a Nuclei scan on a specified target URL or host",
    "lazyown_odat": "Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database",
    "lazyown_ofuscate_string": "Ofuscate a string into Go code",
    "lazyown_ofuscatesh": "Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it",
    "lazyown_ofuscatorps1": "Obfuscate a PowerShell script",
    "lazyown_op_create": "Create a new planned operation",
    "lazyown_op_list": "List all operations",
    "lazyown_op_pause": "Pause a running operation",
    "lazyown_op_plan": "Populate operation steps from a playbook YAML or via MITRE derive",
    "lazyown_op_report": "Generate a full report for an operation",
    "lazyown_op_resume": "Resume a paused operation",
    "lazyown_op_start": "Start (or resume) an operation",
    "lazyown_op_status": "Show the status of an operation",
    "lazyown_op_stop": "Stop a running operation",
    "lazyown_op_timeline": "Show the event timeline of an operation",
    "lazyown_openredirex": "Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities",
    "lazyown_openssl_sclient": "Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS connections",
    "lazyown_operator_create": "Create a new operator profile",
    "lazyown_operator_delete": "Delete an operator profile",
    "lazyown_operator_load": "Load effective config for an operator (team baseline + overrides)",
    "lazyown_operators": "List all operator profiles",
    "lazyown_opsec": "Score OPSEC risk for a LazyOwn command before execution",
    "lazyown_orchestrate": "Route a goal through the unified orchestrator and print the result",
    "lazyown_osmedeus": "Executes Osmedeus scans with guided input for various scanning scenarios",
    "lazyown_owneredit": "Executes the Impacket owneredit tool for manipulating ownership of Active Directory objects",
    "lazyown_package_squat": "Generate a malicious PyPI package for dependency confusion",
    "lazyown_padbuster": "Execute the PadBuster command for padding oracle attacks",
    "lazyown_palette_k": "Open the fuzzy Command-K palette overlay",
    "lazyown_paranoid_meterpreter": "Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracking",
    "lazyown_parsero": "Executes a parsero scan on a specified target URL or host",
    "lazyown_parth": "Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters",
    "lazyown_passtightvnc": "Decrypts TightVNC passwords using Metasploit",
    "lazyown_passwordspray": "Perform password spraying using crackmapexec with the provided parameters",
    "lazyown_path2hex": "Convert a binary path to x64 little-endian hex code for shellcode injection",
    "lazyown_payload": "Load parameters from a specified payload JSON file",
    "lazyown_penelope": "Command penelope: Installs and runs Penelope for handling reverse and bind shells",
    "lazyown_pentest_report": "Generate a professional penetration test report",
    "lazyown_pezorsh": "Executes the PEzor tool to pack executables or shellcode with custom configurations",
    "lazyown_phase": "Get or set the current kill-chain phase",
    "lazyown_phish_report": "Show campaign results and captured credentials",
    "lazyown_phish_serve": "Start a lightweight HTTP server for phishing landing pages",
    "lazyown_phish_wizard": "Interactive end-to-end phishing campaign wizard",
    "lazyown_ping": "Perform a ping to check host availability and infer the operating system based on TTL values",
    "lazyown_pip_proxy": "Configures the local machine with internet access to act as a pip proxy for a machine without internet access",
    "lazyown_pip_repo": "Sets up a local pip repository to serve Python packages for installation on a compromised machine without internet access",
    "lazyown_pipeline": "Declarative composition layer: run a YAML pipeline of LazyOwn commands",
    "lazyown_pivot": "Record a newly discovered pivot target or show the pivot chain",
    "lazyown_pivot_kill": "Kill all pivot tunnels and clean up",
    "lazyown_pivot_proxy": "Start a local SOCKS proxy through the pivot chain",
    "lazyown_pivot_scan": "Scan internal networks through the current pivot chain",
    "lazyown_plan": "Pick the next best technique to run for a target",
    "lazyown_plan_apply": "Run the planner, then auto-create and start an operation",
    "lazyown_plan_detail": "Show the full ranked plan (all candidates) for a target",
    "lazyown_pop": "Open a centered popup in the current tmux session to execute a shell command",
    "lazyown_portdiscover": "Scan all ports on a specified host to identify open ports",
    "lazyown_ports": "Lists all open TCP and UDP ports on the local system",
    "lazyown_portservicediscover": "Scan all ports on a specified host to identify open ports and associated services",
    "lazyown_powerserver": "This function generates a PowerShell script that retrieves reverse shell over http on a Windows system",
    "lazyown_powershell_cmd_stager": "Generate and execute a PowerShell command stager to run a .ps1 script",
    "lazyown_pre2k": "Executes the pre2k tool to query the self.params['domain'] for pre-Windows 2000 machine accounts or to pass a list of hostnames to test authentication",
    "lazyown_prev": "Show prerequisite commands for a verb (the chain's 'prev' arrow)",
    "lazyown_printerbug_py": "Executes the printerbug.py tool to trigger the SpoolService bug via RPC backconnect",
    "lazyown_privesc_suggest": "Quick alias for crystal_ball --auto",
    "lazyown_process_scans": "Processes CSV files with scan results and vulnerability data to generate a Shodan-like JSON database",
    "lazyown_proxy": "Runs a small proxy server to modify HTTP requests on the fly",
    "lazyown_psexec": "Executes the Impacket PSExec tool to attempt remote execution on the specified target",
    "lazyown_psexec_py": "Executes the Impacket PSExec tool to attempt remote execution on the specified target",
    "lazyown_pspy": "Serve the 'pspy' process monitor over HTTP",
    "lazyown_pth_net": "Executes the Pass-the-Hash (PTH) Net tool to change the password of an Active Directory account",
    "lazyown_pup": "Processes HTML content from a specified URL using the pup utility and a default CSS selector",
    "lazyown_pwd": "Displays the current working directory and lists files, and copies the current directory path to the clipboard",
    "lazyown_pwncat": "Runs `pwncat` with the specified port for listening. SELFINJECT",
    "lazyown_pwncatcs": "Start a pwncat-cs reverse shell listener",
    "lazyown_py3ttyup": "Copies a Python reverse shell command to the clipboard",
    "lazyown_pyautomate": "Automates the execution of pwntomate tools on XML configuration files",
    "lazyown_pykerbrute": "Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory accounts using Kerberos pre-authentication",
    "lazyown_pyoracle2": "Executes the pyOracle2 tool for performing padding oracle attacks",
    "lazyown_pywhisker": "Executes the pyWhisker tool for manipulating the msDS-KeyCredentialLink attribute of a target user or computer",
    "lazyown_qa": "Exits the application quickly without confirmation",
    "lazyown_rdp": "Reads credentials from a file, encrypts the password, and executes the RDP connection command",
    "lazyown_rdp_check_py": "Executes the RDP check tool to verify credentials or hash-based authentication on a target system",
    "lazyown_recon": "Performs reconnaissance on a specified self.params['domain'] using crt.sh (the target must be visible on internet), pup, httprobe, and EyeWitness",
    "lazyown_refill_password": "Generate a list of possible passwords by filling each asterisk in the input with user-specified characters",
    "lazyown_reg_py": "Query a remote registry hive with impacket-reg.py over hash auth",
    "lazyown_regeorg": "Executes the reGeorg tool for HTTP(s) tunneling through a SOCKS proxy",
    "lazyown_rejetto_hfs_exec": "HttpFileServer version 2.3. Vulnerable using the module rejetto_hfs_exec of metasploit",
    "lazyown_reload_addons": "Re-scan lazyaddons/ and plugins/ for changes; reloads what's new",
    "lazyown_report": "Generate enhanced professional penetration test reports",
    "lazyown_resource": "Run an enhanced resource script",
    "lazyown_responder": "Run Responder on the configured 'device' with elevated privileges",
    "lazyown_rev": "Copies a reverse shell one-liner to the clipboard",
    "lazyown_revwin": "Create a Windows reverse shell executable",
    "lazyown_rhost": "Copies the remote host (self.params['rhost']) to the clipboard and updates the command prompt",
    "lazyown_rich_tui": "Launch the Rich-based live dashboard TUI",
    "lazyown_rmfromfind": "Remove a custom command by index (as shown in 'find')",
    "lazyown_rnc": "Runs `nc` with rlwrap the specified port for listening",
    "lazyown_rocky": "Reduces a wordlist based on the specified password length",
    "lazyown_rot": "Apply a ROT (rotation) substitution cipher to the given string",
    "lazyown_rotate_aes": "Generate a new AES key and re-encrypt all sealed credentials",
    "lazyown_rotf": "Apply a ROT (rotation) substitution cipher to the given extension",
    "lazyown_route": "Route a natural-language prompt to a LazyOwn tool. Usage: route <prompt>",
    "lazyown_rpcclient": "Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using anonymous credentials",
    "lazyown_rpcdump": "Executes the `rpcdump.py` script to dump RPC services from a target host",
    "lazyown_rpcmap_py": "Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces",
    "lazyown_rrhost": "Updates the command prompt to include the remote host (self.params['rhost']) and current working directory",
    "lazyown_rsync": "Push the 'sessions/' tree to 'rhost' over SCP with sshpass",
    "lazyown_rubeus": "Copies a command to the clipboard for downloading and running Rubeus",
    "lazyown_run": "Runs a specific LazyOwn script or active module",
    "lazyown_samdump2": "Run samdump2 against 'sessions/SYSTEM' and 'sessions/SAM'",
    "lazyown_samrdump": "Run `impacket-samrdump` to dump SAM data from specified ports",
    "lazyown_sandbox": "Toggle or query Docker sandbox mode",
    "lazyown_sawks": "Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phishing simulations",
    "lazyown_scans": "List nmap scan files in sessions/ with age, size, and open ports",
    "lazyown_scarecrow": "Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode",
    "lazyown_scavenger": "Run the Scavenger post-exploitation data collector",
    "lazyown_scope": "Manage the authorized engagement scope and the scope-guard posture",
    "lazyown_scp": "Copies the local \"sessions\" directory to a remote host using scp, leveraging sshpass for automated authentication",
    "lazyown_seal_credentials": "Encrypt all sensitive values in payload.json using AES-256-GCM",
    "lazyown_search": "Search for modules by name, description, or author",
    "lazyown_searchhash": "Helps to find hash types in Hashcat by searching through its help output",
    "lazyown_secretsdump": "Run impacket-secretsdump for SAM, credentials, or NTDS payloads",
    "lazyown_seo": "Performs a web seo fingerprinting scan using `lazyseo.py`",
    "lazyown_serveralive2": "Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and retrieves the server bindings",
    "lazyown_service": "Creates a systemd service file for a specified binary and generates a script to enable and start the service",
    "lazyown_service_ssh": "Creates a systemd service file for a specified binary and generates a script to enable and start the service",
    "lazyown_sessionssh": "Execute a command to list active SSH connections",
    "lazyown_sessionsshstrace": "Attach strace to a running process and log output to a file",
    "lazyown_set": "Set a parameter \u2014 the unified 'set'/'assign' surface",
    "lazyown_set_proxychains": "Configure proxychains for the current session",
    "lazyown_setoolKits": "Executes the SEToolKit workflow to generate a Meterpreter payload",
    "lazyown_sh": "Executes a shell command directly from the LazyOwn interface",
    "lazyown_shadowsocks": "Execute the Shadowsocks tool to create a secure tunnel for network traffic",
    "lazyown_share_finding": "Share a finding or credential discovery with the team",
    "lazyown_sharpshooter": "Executes a payload creation framework for the retrieval and execution of arbitrary CSharp source code",
    "lazyown_shellcode": "Generate and manage shellcode",
    "lazyown_shellcode2elf": "Convert shellcode into an ELF file and infect it",
    "lazyown_shellcode2sylk": "Converts shellcode to SYLK format and saves the result to a file",
    "lazyown_shellcode_search": "Search the shell-storm API for shellcodes using the provided keywords",
    "lazyown_shellfire": "Runs Shellfire with various options and allows generating payloads",
    "lazyown_shellshock": "Executes a Shellshock attack against a target",
    "lazyown_sherlock": "Executes the Sherlock tool to find usernames across social networks",
    "lazyown_show": "Show params, modules, payloads, or active module options",
    "lazyown_shred": "Securely delete files by overwriting before removal",
    "lazyown_sireprat": "Command sireprat: Automates the setup and usage of SirepRAT to perform various attacks on a Windows IoT Core device",
    "lazyown_sitrep": "Print a unified operational situation report",
    "lazyown_skipfish": "This function executes the web security scanning tool Skipfish",
    "lazyown_sliver_server": "Starts the Sliver server and generates a client configuration file for connecting clients",
    "lazyown_smalldic": "Handles the creation of temporary files for users and passwords based on a small dictionary",
    "lazyown_smb_exfil": "Exfiltrate files to an SMB share on the attacker machine",
    "lazyown_smbattack": "Scans for hosts with SMB service open on port 445 in the specified target network",
    "lazyown_smbclient": "Interacts with SMB shares using the `smbclient` command to perform the following operations:",
    "lazyown_smbclient_impacket": "Interacts with SMB shares using the `smbclient` command to perform the following operations:",
    "lazyown_smbclient_py": "Interacts with SMB shares using the `smbclient.py` command to perform the following operations:",
    "lazyown_smbmap": "smbmap -H 10.10.10.3 [OPTIONS]",
    "lazyown_smbserver": "Stand up an Impacket SMB server with three relay variants",
    "lazyown_smtpuserenum": "Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method",
    "lazyown_snmpcheck": "Performs an SNMP check on the specified target host",
    "lazyown_snmpwalk": "Performs an SNMP check on the specified target host",
    "lazyown_socat": "Run socat for port forwarding",
    "lazyown_spool": "Log session output to a file",
    "lazyown_spraykatz": "Run SprayKatz for credential spraying",
    "lazyown_sqli": "Asks the user for the URL, database, table, and columns, and then executes the Python script",
    "lazyown_sqli_mssql_test": "Initiates a reverse MSSQL shell by starting an HTTP server to handle incoming connections and exfiltrate data",
    "lazyown_sqlmap": "Runs SQLMap against the target URL for SQL injection testing",
    "lazyown_sqsh": "Executes the Impacket sqsh tool for manipulating ownership of Active Directory objects",
    "lazyown_ss": "Search all exploit sources and map findings to the next LazyOwn command",
    "lazyown_ssh": "SSH to a remote host (custom port)",
    "lazyown_ssh_cmd": "Perform Remote Execution Command through SSH using configured start_user. See help grisun0 for backdoor user configuration",
    "lazyown_sshd": "Starts the SSH service and displays its status",
    "lazyown_sshexploit": "Exploits OpenSSH vulnerability CVE-2023-38408 via the PKCS#11 feature of the ssh-agent",
    "lazyown_sshkey": "Generate an SSH key pair",
    "lazyown_sslscan": "Run an SSL scan on the specified remote host",
    "lazyown_stage": "Stage data for exfiltration: compress, encrypt, and split",
    "lazyown_state_snapshot": "Show unified StateManager snapshot (DB + JSON caches)",
    "lazyown_status_bar": "Inspect, toggle and refresh the prompt status bar",
    "lazyown_status_tail": "Print live progress from the latest sessions/scan_*.partial file",
    "lazyown_stealth_off": "Disable stealth mode",
    "lazyown_stealth_on": "Enable stealth mode for subsequent operations",
    "lazyown_stormbreaker": "Command stormbreaker: Automates the installation and usage of Storm-Breaker for performing various network attacks",
    "lazyown_sudo": "Re-launch the framework with root privileges when missing",
    "lazyown_suggest_next": "Suggest next commands by walking the graph from recent activity",
    "lazyown_suid_check": "Print SUID/SGID enumeration commands ready to paste on the target",
    "lazyown_surface": "Render the network surface graph in the terminal",
    "lazyown_swaks": "Sends an email using `swaks` (Swiss Army Knife for SMTP)",
    "lazyown_sys": "Executes a shell command directly from the LazyOwn interface",
    "lazyown_tab": "Executes the `lazypyautogui.py` script with optional arguments",
    "lazyown_targetedKerberoas": "Executes the targetedKerberoast tool for extracting Kerberos service tickets",
    "lazyown_tasks": "View and manage the task queue from sessions/tasks.json",
    "lazyown_tcpdump_capture": "Starts packet capture using `tcpdump` on the specified interface",
    "lazyown_tcpdump_icmp": "Starts `tcpdump` to capture ICMP traffic on the specified interface",
    "lazyown_team_chat": "Send a message to all connected operators",
    "lazyown_team_status": "Show active operators and target locks",
    "lazyown_template_helper_serializer": "Handles the creation and serialization of a template helper",
    "lazyown_tenant": "Manage multi-tenancy: list, switch, or create engagement tenants",
    "lazyown_tgrep": "Search across all previous command outputs and session logs",
    "lazyown_ticketer": "Runs Impacket ticketer for golden/silver ticket creation",
    "lazyown_timeline_browser": "Open the timeline scrubber over the session report CSV",
    "lazyown_toast_clear": "Mark every pending toast event as seen without printing them",
    "lazyown_toctoc": "Sends a magic packet to the Chinese malware",
    "lazyown_tord": "Execute the tor.sh script with the specified port or default to port 80 if no port is provided",
    "lazyown_trace": "Traces the DNS information for a given self.params['domain'] using the FreeDNS service. (using freedns IP Not your IP)",
    "lazyown_transform": "Transforms the input string based on user-defined casing style",
    "lazyown_trufflehog": "Executes trufflehog to search for secrets in a given Git repository URL",
    "lazyown_tshark_analyze": "Analyzes a packet capture file using `tshark` based on the provided remote host IP",
    "lazyown_ttp_matrix": "Render the MITRE ATT&CK coverage matrix across all operations",
    "lazyown_ttp_rebuild": "Re-walk the operations directory to refresh the coverage matrix",
    "lazyown_ttp_show": "Show details for a single MITRE technique",
    "lazyown_tui_theme": "Switch the TUI colour theme used by the splash and styled output",
    "lazyown_unicode_WAFbypass": "We open a Netcat listener on port 443 and attempt to exploit NodeJS deserialization by sending the",
    "lazyown_unlock_target": "Release an advisory lock on a target",
    "lazyown_unseal_credentials": "Decrypt sealed credential values in payload.json for inspection",
    "lazyown_unzip": "Extract a zip archive located under 'sessions/'",
    "lazyown_upload_bypass": "Command upload_bypass: Automates the installation and execution of Upload_Bypass for performing file upload bypass tests",
    "lazyown_upload_c2": "upload command in the client using the C2 to upload a file",
    "lazyown_upload_gofile": "Upload a file from 'sessions/' to Gofile via its HTTP API",
    "lazyown_urldecode": "Decode a URL-encoded string",
    "lazyown_urlencode": "Encode a string for URL",
    "lazyown_use": "Select a module to work with",
    "lazyown_username_anarchy": "Generate usernames using the username-anarchy tool based on user input",
    "lazyown_utf": "Encode a given payload into UTF-16 escape sequences",
    "lazyown_v": "Open a new window within a tmux session using the LazyOwn RedTeam Framework",
    "lazyown_veil": "Generates payloads using Veil-Evasion with various options. Veil-Evasion is a payload creation framework",
    "lazyown_vpn": "Connect to a VPN by selecting from available .ovpn files",
    "lazyown_vscan": "Perform port scanning using vscan with the provided parameters",
    "lazyown_vuln_list": "List discovered vulnerabilities from the sessions database",
    "lazyown_vulns": "Display or manage vulnerabilities",
    "lazyown_waybackmachine": "Fetch URLs from the Wayback Machine for a given website",
    "lazyown_weevely": "Connect to PHP backdoor using Weevely, protected with the given password",
    "lazyown_weevelygen": "Generate a PHP backdoor using Weevely, protected with the given password",
    "lazyown_wfuzz": "Uses `wfuzz` to perform fuzzing based on provided parameters. This function supports various options for directory and file fuzzing",
    "lazyown_whatweb": "Performs a web technology fingerprinting scan using `whatweb`",
    "lazyown_whoami": "Show the currently logged-in CLI operator",
    "lazyown_wifipass": "This function generates a PowerShell script that retrieves saved Wi-Fi passwords on a Windows system",
    "lazyown_winbase64payload": "Creates a base64 encoded payload specifically for Windows to execute a PowerShell command or download a file using `self.params['lhost']`",
    "lazyown_windapsearch": "Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries",
    "lazyown_windapsearchscrapeusers": "Extracts usernames from a JSON output generated by go-windapsearch and appends them",
    "lazyown_winpeas": "Serve a winPEAS variant over HTTP and print the target one-liner",
    "lazyown_wipe_free": "Wipe free disk space to prevent forensic file recovery",
    "lazyown_wipe_logs": "Clear system log files on the remote target",
    "lazyown_wipe_timeline": "Scrub file timestamps and shell history on the target",
    "lazyown_wizard": "Guided first-run setup wizard \u2014 configure rhost, lhost, domain, wordlists and more",
    "lazyown_wmi_lateral": "Execute a command on a remote host via WMI",
    "lazyown_wmi_persist": "Create WMI Event Subscription persistence (fileless, no disk write)",
    "lazyown_wmi_scheduled_task": "Create a scheduled task for persistence via WMI",
    "lazyown_wmiexec": "Execute commands via WMI",
    "lazyown_wmiexecpro": "Executes wmiexec-pro with various options for WMI operations",
    "lazyown_wpscan": "Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning",
    "lazyown_wrapper": "Copies LFI php-wrapper payloads to the clipboard",
    "lazyown_www": "Starts a simple HTTP server on the configured port to serve payloads",
    "lazyown_xss": "Executes the XSS (Cross-Site Scripting) vulnerability testing procedure",
    "lazyown_xsstrike": "Command xsstrike: Installs and runs XSStrike for finding XSS vulnerabilities",
    "lazyown_yara_scan": "Scan files or directories with YARA rules for malware/IOCs",
}


def get_generated_tool_definitions() -> list:
    """Return list[types.Tool] entries for all generated tools."""
    from mcp import types as _types

    _tools: list = []
    for _tool, _desc in sorted(_COMMAND_MAP.items()):
        _tools.append(_types.Tool(
            name=_tool,
            description=_desc,
            inputSchema={
                "type": "object",
                "properties": {
                    "args": {
                        "type": "string",
                        "description": "Optional arguments to pass to the command.",
                        "default": "",
                    },
                },
            }
        ))
    return _tools


def register_all_generated_handlers(
    register_handler_fn,
    make_text_fn,
    run_lazyown_cmd_fn,
) -> int:
    """
    Register every generated handler via *register_handler_fn*.

    Called by lazyown_mcp.py after its infrastructure is ready. Returns the count registered.
    """
    _reg = 0

    async def _gen_EOF(arguments: dict, tool_name: str, _cmd='EOF') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_EOF')(_gen_EOF)
    _reg += 1

    async def _gen_GET(arguments: dict, tool_name: str, _cmd='GET') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_GET')(_gen_GET)
    _reg += 1

    async def _gen_OPTIONS(arguments: dict, tool_name: str, _cmd='OPTIONS') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_OPTIONS')(_gen_OPTIONS)
    _reg += 1

    async def _gen_POST(arguments: dict, tool_name: str, _cmd='POST') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_POST')(_gen_POST)
    _reg += 1

    async def _gen_acknowledgearp(arguments: dict, tool_name: str, _cmd='acknowledgearp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_acknowledgearp')(_gen_acknowledgearp)
    _reg += 1

    async def _gen_acknowledgeicmp(arguments: dict, tool_name: str, _cmd='acknowledgeicmp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_acknowledgeicmp')(_gen_acknowledgeicmp)
    _reg += 1

    async def _gen_aclpwn_py(arguments: dict, tool_name: str, _cmd='aclpwn_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_aclpwn_py')(_gen_aclpwn_py)
    _reg += 1

    async def _gen_ad_ldap_enum(arguments: dict, tool_name: str, _cmd='ad_ldap_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ad_ldap_enum')(_gen_ad_ldap_enum)
    _reg += 1

    async def _gen_adcs_check(arguments: dict, tool_name: str, _cmd='adcs_check') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_adcs_check')(_gen_adcs_check)
    _reg += 1

    async def _gen_add2find(arguments: dict, tool_name: str, _cmd='add2find') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_add2find')(_gen_add2find)
    _reg += 1

    async def _gen_addalias(arguments: dict, tool_name: str, _cmd='addalias') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_addalias')(_gen_addalias)
    _reg += 1

    async def _gen_addcli(arguments: dict, tool_name: str, _cmd='addcli') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_addcli')(_gen_addcli)
    _reg += 1

    async def _gen_addhosts(arguments: dict, tool_name: str, _cmd='addhosts') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_addhosts')(_gen_addhosts)
    _reg += 1

    async def _gen_addspn_py(arguments: dict, tool_name: str, _cmd='addspn_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_addspn_py')(_gen_addspn_py)
    _reg += 1

    async def _gen_addusers(arguments: dict, tool_name: str, _cmd='addusers') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_addusers')(_gen_addusers)
    _reg += 1

    async def _gen_adgetpass(arguments: dict, tool_name: str, _cmd='adgetpass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_adgetpass')(_gen_adgetpass)
    _reg += 1

    async def _gen_adsso_spray(arguments: dict, tool_name: str, _cmd='adsso_spray') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_adsso_spray')(_gen_adsso_spray)
    _reg += 1

    async def _gen_adversary(arguments: dict, tool_name: str, _cmd='adversary') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_adversary')(_gen_adversary)
    _reg += 1

    async def _gen_adversary_yaml(arguments: dict, tool_name: str, _cmd='adversary_yaml') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_adversary_yaml')(_gen_adversary_yaml)
    _reg += 1

    async def _gen_aes_pe(arguments: dict, tool_name: str, _cmd='aes_pe') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_aes_pe')(_gen_aes_pe)
    _reg += 1

    async def _gen_ai_playbook(arguments: dict, tool_name: str, _cmd='ai_playbook') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ai_playbook')(_gen_ai_playbook)
    _reg += 1

    async def _gen_ai_toggle(arguments: dict, tool_name: str, _cmd='ai_toggle') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ai_toggle')(_gen_ai_toggle)
    _reg += 1

    async def _gen_aliass(arguments: dict, tool_name: str, _cmd='aliass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_aliass')(_gen_aliass)
    _reg += 1

    async def _gen_allin(arguments: dict, tool_name: str, _cmd='allin') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_allin')(_gen_allin)
    _reg += 1

    async def _gen_alterx(arguments: dict, tool_name: str, _cmd='alterx') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_alterx')(_gen_alterx)
    _reg += 1

    async def _gen_amass(arguments: dict, tool_name: str, _cmd='amass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_amass')(_gen_amass)
    _reg += 1

    async def _gen_android_apk(arguments: dict, tool_name: str, _cmd='android_apk') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_android_apk')(_gen_android_apk)
    _reg += 1

    async def _gen_android_enum(arguments: dict, tool_name: str, _cmd='android_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_android_enum')(_gen_android_enum)
    _reg += 1

    async def _gen_apache_users(arguments: dict, tool_name: str, _cmd='apache_users') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_apache_users')(_gen_apache_users)
    _reg += 1

    async def _gen_applocker_csc(arguments: dict, tool_name: str, _cmd='applocker_csc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_csc')(_gen_applocker_csc)
    _reg += 1

    async def _gen_applocker_installutil(arguments: dict, tool_name: str, _cmd='applocker_installutil') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_installutil')(_gen_applocker_installutil)
    _reg += 1

    async def _gen_applocker_msbuild(arguments: dict, tool_name: str, _cmd='applocker_msbuild') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_msbuild')(_gen_applocker_msbuild)
    _reg += 1

    async def _gen_applocker_mshta(arguments: dict, tool_name: str, _cmd='applocker_mshta') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_mshta')(_gen_applocker_mshta)
    _reg += 1

    async def _gen_applocker_presentation(arguments: dict, tool_name: str, _cmd='applocker_presentation') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_presentation')(_gen_applocker_presentation)
    _reg += 1

    async def _gen_applocker_regsvcs(arguments: dict, tool_name: str, _cmd='applocker_regsvcs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_regsvcs')(_gen_applocker_regsvcs)
    _reg += 1

    async def _gen_applocker_rundll32(arguments: dict, tool_name: str, _cmd='applocker_rundll32') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_applocker_rundll32')(_gen_applocker_rundll32)
    _reg += 1

    async def _gen_apropos(arguments: dict, tool_name: str, _cmd='apropos') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_apropos')(_gen_apropos)
    _reg += 1

    async def _gen_apt_playbook(arguments: dict, tool_name: str, _cmd='apt_playbook') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_apt_playbook')(_gen_apt_playbook)
    _reg += 1

    async def _gen_apt_proxy(arguments: dict, tool_name: str, _cmd='apt_proxy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_apt_proxy')(_gen_apt_proxy)
    _reg += 1

    async def _gen_apt_repo(arguments: dict, tool_name: str, _cmd='apt_repo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_apt_repo')(_gen_apt_repo)
    _reg += 1

    async def _gen_arjun(arguments: dict, tool_name: str, _cmd='arjun') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_arjun')(_gen_arjun)
    _reg += 1

    async def _gen_arpscan(arguments: dict, tool_name: str, _cmd='arpscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_arpscan')(_gen_arpscan)
    _reg += 1

    async def _gen_ask(arguments: dict, tool_name: str, _cmd='ask') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ask')(_gen_ask)
    _reg += 1

    async def _gen_asprevbase64(arguments: dict, tool_name: str, _cmd='asprevbase64') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_asprevbase64')(_gen_asprevbase64)
    _reg += 1

    async def _gen_assign(arguments: dict, tool_name: str, _cmd='assign') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_assign')(_gen_assign)
    _reg += 1

    async def _gen_atomic_agent(arguments: dict, tool_name: str, _cmd='atomic_agent') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_atomic_agent')(_gen_atomic_agent)
    _reg += 1

    async def _gen_atomic_gen(arguments: dict, tool_name: str, _cmd='atomic_gen') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_atomic_gen')(_gen_atomic_gen)
    _reg += 1

    async def _gen_atomic_lazyown(arguments: dict, tool_name: str, _cmd='atomic_lazyown') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_atomic_lazyown')(_gen_atomic_lazyown)
    _reg += 1

    async def _gen_atomic_tests(arguments: dict, tool_name: str, _cmd='atomic_tests') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_atomic_tests')(_gen_atomic_tests)
    _reg += 1

    async def _gen_attack_plan(arguments: dict, tool_name: str, _cmd='attack_plan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_attack_plan')(_gen_attack_plan)
    _reg += 1

    async def _gen_attack_surface(arguments: dict, tool_name: str, _cmd='attack_surface') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_attack_surface')(_gen_attack_surface)
    _reg += 1

    async def _gen_audit_complete_keys(arguments: dict, tool_name: str, _cmd='audit_complete_keys') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_audit_complete_keys')(_gen_audit_complete_keys)
    _reg += 1

    async def _gen_autoblody(arguments: dict, tool_name: str, _cmd='autoblody') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_autoblody')(_gen_autoblody)
    _reg += 1

    async def _gen_automsf(arguments: dict, tool_name: str, _cmd='automsf') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_automsf')(_gen_automsf)
    _reg += 1

    async def _gen_autopivot(arguments: dict, tool_name: str, _cmd='autopivot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_autopivot')(_gen_autopivot)
    _reg += 1

    async def _gen_back(arguments: dict, tool_name: str, _cmd='back') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_back')(_gen_back)
    _reg += 1

    async def _gen_backdoor_factory(arguments: dict, tool_name: str, _cmd='backdoor_factory') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_backdoor_factory')(_gen_backdoor_factory)
    _reg += 1

    async def _gen_banner(arguments: dict, tool_name: str, _cmd='banner') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_banner')(_gen_banner)
    _reg += 1

    async def _gen_banners(arguments: dict, tool_name: str, _cmd='banners') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_banners')(_gen_banners)
    _reg += 1

    async def _gen_base64decode(arguments: dict, tool_name: str, _cmd='base64decode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_base64decode')(_gen_base64decode)
    _reg += 1

    async def _gen_base64encode(arguments: dict, tool_name: str, _cmd='base64encode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_base64encode')(_gen_base64encode)
    _reg += 1

    async def _gen_batchnmap(arguments: dict, tool_name: str, _cmd='batchnmap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_batchnmap')(_gen_batchnmap)
    _reg += 1

    async def _gen_bbot(arguments: dict, tool_name: str, _cmd='bbot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_bbot')(_gen_bbot)
    _reg += 1

    async def _gen_beaconcfg(arguments: dict, tool_name: str, _cmd='beaconcfg') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_beaconcfg')(_gen_beaconcfg)
    _reg += 1

    async def _gen_bin2shellcode(arguments: dict, tool_name: str, _cmd='bin2shellcode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_bin2shellcode')(_gen_bin2shellcode)
    _reg += 1

    async def _gen_binarycheck(arguments: dict, tool_name: str, _cmd='binarycheck') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_binarycheck')(_gen_binarycheck)
    _reg += 1

    async def _gen_bitm(arguments: dict, tool_name: str, _cmd='bitm') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_bitm')(_gen_bitm)
    _reg += 1

    async def _gen_blazy(arguments: dict, tool_name: str, _cmd='blazy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_blazy')(_gen_blazy)
    _reg += 1

    async def _gen_bloodhound(arguments: dict, tool_name: str, _cmd='bloodhound') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_bloodhound')(_gen_bloodhound)
    _reg += 1

    async def _gen_bloodyAD(arguments: dict, tool_name: str, _cmd='bloodyAD') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_bloodyAD')(_gen_bloodyAD)
    _reg += 1

    async def _gen_breacher(arguments: dict, tool_name: str, _cmd='breacher') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_breacher')(_gen_breacher)
    _reg += 1

    async def _gen_browse(arguments: dict, tool_name: str, _cmd='browse') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_browse')(_gen_browse)
    _reg += 1

    async def _gen_c2(arguments: dict, tool_name: str, _cmd='c2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2')(_gen_c2)
    _reg += 1

    async def _gen_c2_beacon_cmd(arguments: dict, tool_name: str, _cmd='c2_beacon_cmd') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2_beacon_cmd')(_gen_c2_beacon_cmd)
    _reg += 1

    async def _gen_c2_beacons(arguments: dict, tool_name: str, _cmd='c2_beacons') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2_beacons')(_gen_c2_beacons)
    _reg += 1

    async def _gen_c2_implant(arguments: dict, tool_name: str, _cmd='c2_implant') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2_implant')(_gen_c2_implant)
    _reg += 1

    async def _gen_c2_keygen(arguments: dict, tool_name: str, _cmd='c2_keygen') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2_keygen')(_gen_c2_keygen)
    _reg += 1

    async def _gen_c2_quickstart(arguments: dict, tool_name: str, _cmd='c2_quickstart') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2_quickstart')(_gen_c2_quickstart)
    _reg += 1

    async def _gen_c2asm(arguments: dict, tool_name: str, _cmd='c2asm') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_c2asm')(_gen_c2asm)
    _reg += 1

    async def _gen_cacti_exploit(arguments: dict, tool_name: str, _cmd='cacti_exploit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cacti_exploit')(_gen_cacti_exploit)
    _reg += 1

    async def _gen_caldera(arguments: dict, tool_name: str, _cmd='caldera') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_caldera')(_gen_caldera)
    _reg += 1

    async def _gen_caldera_export(arguments: dict, tool_name: str, _cmd='caldera_export') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_caldera_export')(_gen_caldera_export)
    _reg += 1

    async def _gen_caldera_import(arguments: dict, tool_name: str, _cmd='caldera_import') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_caldera_import')(_gen_caldera_import)
    _reg += 1

    async def _gen_camphish(arguments: dict, tool_name: str, _cmd='camphish') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_camphish')(_gen_camphish)
    _reg += 1

    async def _gen_certipy(arguments: dict, tool_name: str, _cmd='certipy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_certipy')(_gen_certipy)
    _reg += 1

    async def _gen_certipy_ad(arguments: dict, tool_name: str, _cmd='certipy_ad') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_certipy_ad')(_gen_certipy_ad)
    _reg += 1

    async def _gen_cewl(arguments: dict, tool_name: str, _cmd='cewl') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cewl')(_gen_cewl)
    _reg += 1

    async def _gen_chain(arguments: dict, tool_name: str, _cmd='chain') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_chain')(_gen_chain)
    _reg += 1

    async def _gen_changeme(arguments: dict, tool_name: str, _cmd='changeme') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_changeme')(_gen_changeme)
    _reg += 1

    async def _gen_check_update(arguments: dict, tool_name: str, _cmd='check_update') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_check_update')(_gen_check_update)
    _reg += 1

    async def _gen_chisel(arguments: dict, tool_name: str, _cmd='chisel') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_chisel')(_gen_chisel)
    _reg += 1

    async def _gen_cicd_scan(arguments: dict, tool_name: str, _cmd='cicd_scan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cicd_scan')(_gen_cicd_scan)
    _reg += 1

    async def _gen_cicd_secrets(arguments: dict, tool_name: str, _cmd='cicd_secrets') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cicd_secrets')(_gen_cicd_secrets)
    _reg += 1

    async def _gen_clean(arguments: dict, tool_name: str, _cmd='clean') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_clean')(_gen_clean)
    _reg += 1

    async def _gen_clean_ad(arguments: dict, tool_name: str, _cmd='clean_ad') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_clean_ad')(_gen_clean_ad)
    _reg += 1

    async def _gen_clock(arguments: dict, tool_name: str, _cmd='clock') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_clock')(_gen_clock)
    _reg += 1

    async def _gen_clone_site(arguments: dict, tool_name: str, _cmd='clone_site') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_clone_site')(_gen_clone_site)
    _reg += 1

    async def _gen_cloud_buckets(arguments: dict, tool_name: str, _cmd='cloud_buckets') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cloud_buckets')(_gen_cloud_buckets)
    _reg += 1

    async def _gen_cloud_enum(arguments: dict, tool_name: str, _cmd='cloud_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cloud_enum')(_gen_cloud_enum)
    _reg += 1

    async def _gen_cloud_iam(arguments: dict, tool_name: str, _cmd='cloud_iam') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cloud_iam')(_gen_cloud_iam)
    _reg += 1

    async def _gen_cloud_metadata(arguments: dict, tool_name: str, _cmd='cloud_metadata') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cloud_metadata')(_gen_cloud_metadata)
    _reg += 1

    async def _gen_cloud_scan(arguments: dict, tool_name: str, _cmd='cloud_scan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cloud_scan')(_gen_cloud_scan)
    _reg += 1

    async def _gen_cme(arguments: dict, tool_name: str, _cmd='cme') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cme')(_gen_cme)
    _reg += 1

    async def _gen_collab_join(arguments: dict, tool_name: str, _cmd='collab_join') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_collab_join')(_gen_collab_join)
    _reg += 1

    async def _gen_commix(arguments: dict, tool_name: str, _cmd='commix') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_commix')(_gen_commix)
    _reg += 1

    async def _gen_config_banner(arguments: dict, tool_name: str, _cmd='config_banner') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_config_banner')(_gen_config_banner)
    _reg += 1

    async def _gen_conptyshell(arguments: dict, tool_name: str, _cmd='conptyshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_conptyshell')(_gen_conptyshell)
    _reg += 1

    async def _gen_container_detect(arguments: dict, tool_name: str, _cmd='container_detect') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_container_detect')(_gen_container_detect)
    _reg += 1

    async def _gen_container_escape(arguments: dict, tool_name: str, _cmd='container_escape') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_container_escape')(_gen_container_escape)
    _reg += 1

    async def _gen_convert_remcomsvc_from_file(arguments: dict, tool_name: str, _cmd='convert_remcomsvc_from_file') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_convert_remcomsvc_from_file')(_gen_convert_remcomsvc_from_file)
    _reg += 1

    async def _gen_cover_tracks(arguments: dict, tool_name: str, _cmd='cover_tracks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cover_tracks')(_gen_cover_tracks)
    _reg += 1

    async def _gen_cp(arguments: dict, tool_name: str, _cmd='cp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cp')(_gen_cp)
    _reg += 1

    async def _gen_cports(arguments: dict, tool_name: str, _cmd='cports') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cports')(_gen_cports)
    _reg += 1

    async def _gen_crack_cisco_7_password(arguments: dict, tool_name: str, _cmd='crack_cisco_7_password') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_crack_cisco_7_password')(_gen_crack_cisco_7_password)
    _reg += 1

    async def _gen_crack_hashes(arguments: dict, tool_name: str, _cmd='crack_hashes') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_crack_hashes')(_gen_crack_hashes)
    _reg += 1

    async def _gen_create_session_json(arguments: dict, tool_name: str, _cmd='create_session_json') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_create_session_json')(_gen_create_session_json)
    _reg += 1

    async def _gen_create_synthetic(arguments: dict, tool_name: str, _cmd='create_synthetic') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_create_synthetic')(_gen_create_synthetic)
    _reg += 1

    async def _gen_createcookie(arguments: dict, tool_name: str, _cmd='createcookie') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createcookie')(_gen_createcookie)
    _reg += 1

    async def _gen_createcredentials(arguments: dict, tool_name: str, _cmd='createcredentials') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createcredentials')(_gen_createcredentials)
    _reg += 1

    async def _gen_createdll(arguments: dict, tool_name: str, _cmd='createdll') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createdll')(_gen_createdll)
    _reg += 1

    async def _gen_createhash(arguments: dict, tool_name: str, _cmd='createhash') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createhash')(_gen_createhash)
    _reg += 1

    async def _gen_createjsonmachine(arguments: dict, tool_name: str, _cmd='createjsonmachine') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createjsonmachine')(_gen_createjsonmachine)
    _reg += 1

    async def _gen_createjsonmachine_batch(arguments: dict, tool_name: str, _cmd='createjsonmachine_batch') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createjsonmachine_batch')(_gen_createjsonmachine_batch)
    _reg += 1

    async def _gen_createmail(arguments: dict, tool_name: str, _cmd='createmail') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createmail')(_gen_createmail)
    _reg += 1

    async def _gen_createpayload(arguments: dict, tool_name: str, _cmd='createpayload') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createpayload')(_gen_createpayload)
    _reg += 1

    async def _gen_createrevshell(arguments: dict, tool_name: str, _cmd='createrevshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createrevshell')(_gen_createrevshell)
    _reg += 1

    async def _gen_createtargets(arguments: dict, tool_name: str, _cmd='createtargets') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createtargets')(_gen_createtargets)
    _reg += 1

    async def _gen_createusers_and_hashs(arguments: dict, tool_name: str, _cmd='createusers_and_hashs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createusers_and_hashs')(_gen_createusers_and_hashs)
    _reg += 1

    async def _gen_createwebshell(arguments: dict, tool_name: str, _cmd='createwebshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createwebshell')(_gen_createwebshell)
    _reg += 1

    async def _gen_createwinrevshell(arguments: dict, tool_name: str, _cmd='createwinrevshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_createwinrevshell')(_gen_createwinrevshell)
    _reg += 1

    async def _gen_cred(arguments: dict, tool_name: str, _cmd='cred') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cred')(_gen_cred)
    _reg += 1

    async def _gen_cred_mark_failed(arguments: dict, tool_name: str, _cmd='cred_mark_failed') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cred_mark_failed')(_gen_cred_mark_failed)
    _reg += 1

    async def _gen_cred_reuse(arguments: dict, tool_name: str, _cmd='cred_reuse') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cred_reuse')(_gen_cred_reuse)
    _reg += 1

    async def _gen_creds_py(arguments: dict, tool_name: str, _cmd='creds_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_creds_py')(_gen_creds_py)
    _reg += 1

    async def _gen_cron(arguments: dict, tool_name: str, _cmd='cron') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cron')(_gen_cron)
    _reg += 1

    async def _gen_crunch(arguments: dict, tool_name: str, _cmd='crunch') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_crunch')(_gen_crunch)
    _reg += 1

    async def _gen_crystal_ball(arguments: dict, tool_name: str, _cmd='crystal_ball') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_crystal_ball')(_gen_crystal_ball)
    _reg += 1

    async def _gen_ctx(arguments: dict, tool_name: str, _cmd='ctx') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ctx')(_gen_ctx)
    _reg += 1

    async def _gen_cubespraying(arguments: dict, tool_name: str, _cmd='cubespraying') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cubespraying')(_gen_cubespraying)
    _reg += 1

    async def _gen_cve(arguments: dict, tool_name: str, _cmd='cve') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_cve')(_gen_cve)
    _reg += 1

    async def _gen_d3monizedshell(arguments: dict, tool_name: str, _cmd='d3monizedshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_d3monizedshell')(_gen_d3monizedshell)
    _reg += 1

    async def _gen_dacledit(arguments: dict, tool_name: str, _cmd='dacledit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dacledit')(_gen_dacledit)
    _reg += 1

    async def _gen_darkarmour(arguments: dict, tool_name: str, _cmd='darkarmour') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_darkarmour')(_gen_darkarmour)
    _reg += 1

    async def _gen_dashboard(arguments: dict, tool_name: str, _cmd='dashboard') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dashboard')(_gen_dashboard)
    _reg += 1

    async def _gen_davtest(arguments: dict, tool_name: str, _cmd='davtest') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_davtest')(_gen_davtest)
    _reg += 1

    async def _gen_db_creds(arguments: dict, tool_name: str, _cmd='db_creds') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_creds')(_gen_db_creds)
    _reg += 1

    async def _gen_db_export(arguments: dict, tool_name: str, _cmd='db_export') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_export')(_gen_db_export)
    _reg += 1

    async def _gen_db_hosts(arguments: dict, tool_name: str, _cmd='db_hosts') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_hosts')(_gen_db_hosts)
    _reg += 1

    async def _gen_db_import(arguments: dict, tool_name: str, _cmd='db_import') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_import')(_gen_db_import)
    _reg += 1

    async def _gen_db_init(arguments: dict, tool_name: str, _cmd='db_init') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_init')(_gen_db_init)
    _reg += 1

    async def _gen_db_loot(arguments: dict, tool_name: str, _cmd='db_loot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_loot')(_gen_db_loot)
    _reg += 1

    async def _gen_db_notes(arguments: dict, tool_name: str, _cmd='db_notes') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_notes')(_gen_db_notes)
    _reg += 1

    async def _gen_db_services(arguments: dict, tool_name: str, _cmd='db_services') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_services')(_gen_db_services)
    _reg += 1

    async def _gen_db_status(arguments: dict, tool_name: str, _cmd='db_status') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_status')(_gen_db_status)
    _reg += 1

    async def _gen_db_vulns(arguments: dict, tool_name: str, _cmd='db_vulns') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_vulns')(_gen_db_vulns)
    _reg += 1

    async def _gen_db_workspace(arguments: dict, tool_name: str, _cmd='db_workspace') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_db_workspace')(_gen_db_workspace)
    _reg += 1

    async def _gen_dcomexec(arguments: dict, tool_name: str, _cmd='dcomexec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dcomexec')(_gen_dcomexec)
    _reg += 1

    async def _gen_decode(arguments: dict, tool_name: str, _cmd='decode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_decode')(_gen_decode)
    _reg += 1

    async def _gen_decrypt(arguments: dict, tool_name: str, _cmd='decrypt') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_decrypt')(_gen_decrypt)
    _reg += 1

    async def _gen_depconfuse(arguments: dict, tool_name: str, _cmd='depconfuse') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_depconfuse')(_gen_depconfuse)
    _reg += 1

    async def _gen_depscan(arguments: dict, tool_name: str, _cmd='depscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_depscan')(_gen_depscan)
    _reg += 1

    async def _gen_detect_edr(arguments: dict, tool_name: str, _cmd='detect_edr') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_detect_edr')(_gen_detect_edr)
    _reg += 1

    async def _gen_dig(arguments: dict, tool_name: str, _cmd='dig') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dig')(_gen_dig)
    _reg += 1

    async def _gen_digdug(arguments: dict, tool_name: str, _cmd='digdug') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_digdug')(_gen_digdug)
    _reg += 1

    async def _gen_dirsearch(arguments: dict, tool_name: str, _cmd='dirsearch') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dirsearch')(_gen_dirsearch)
    _reg += 1

    async def _gen_disableav(arguments: dict, tool_name: str, _cmd='disableav') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_disableav')(_gen_disableav)
    _reg += 1

    async def _gen_dmitry(arguments: dict, tool_name: str, _cmd='dmitry') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dmitry')(_gen_dmitry)
    _reg += 1

    async def _gen_dns_beacon(arguments: dict, tool_name: str, _cmd='dns_beacon') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dns_beacon')(_gen_dns_beacon)
    _reg += 1

    async def _gen_dns_beacon_status(arguments: dict, tool_name: str, _cmd='dns_beacon_status') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dns_beacon_status')(_gen_dns_beacon_status)
    _reg += 1

    async def _gen_dns_exfil_listen(arguments: dict, tool_name: str, _cmd='dns_exfil_listen') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dns_exfil_listen')(_gen_dns_exfil_listen)
    _reg += 1

    async def _gen_dnschef(arguments: dict, tool_name: str, _cmd='dnschef') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dnschef')(_gen_dnschef)
    _reg += 1

    async def _gen_dnsenum(arguments: dict, tool_name: str, _cmd='dnsenum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dnsenum')(_gen_dnsenum)
    _reg += 1

    async def _gen_dnsmap(arguments: dict, tool_name: str, _cmd='dnsmap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dnsmap')(_gen_dnsmap)
    _reg += 1

    async def _gen_dnstool_py(arguments: dict, tool_name: str, _cmd='dnstool_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dnstool_py')(_gen_dnstool_py)
    _reg += 1

    async def _gen_docker_enum(arguments: dict, tool_name: str, _cmd='docker_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_docker_enum')(_gen_docker_enum)
    _reg += 1

    async def _gen_doctor(arguments: dict, tool_name: str, _cmd='doctor') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_doctor')(_gen_doctor)
    _reg += 1

    async def _gen_dominion(arguments: dict, tool_name: str, _cmd='dominion') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dominion')(_gen_dominion)
    _reg += 1

    async def _gen_download_c2(arguments: dict, tool_name: str, _cmd='download_c2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_download_c2')(_gen_download_c2)
    _reg += 1

    async def _gen_download_exploit(arguments: dict, tool_name: str, _cmd='download_exploit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_download_exploit')(_gen_download_exploit)
    _reg += 1

    async def _gen_download_malwarebazar(arguments: dict, tool_name: str, _cmd='download_malwarebazar') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_download_malwarebazar')(_gen_download_malwarebazar)
    _reg += 1

    async def _gen_download_resources(arguments: dict, tool_name: str, _cmd='download_resources') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_download_resources')(_gen_download_resources)
    _reg += 1

    async def _gen_downloader(arguments: dict, tool_name: str, _cmd='downloader') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_downloader')(_gen_downloader)
    _reg += 1

    async def _gen_dpapi_blob(arguments: dict, tool_name: str, _cmd='dpapi_blob') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dpapi_blob')(_gen_dpapi_blob)
    _reg += 1

    async def _gen_dpapi_harvest(arguments: dict, tool_name: str, _cmd='dpapi_harvest') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dpapi_harvest')(_gen_dpapi_harvest)
    _reg += 1

    async def _gen_dpapi_masterkeys(arguments: dict, tool_name: str, _cmd='dpapi_masterkeys') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dpapi_masterkeys')(_gen_dpapi_masterkeys)
    _reg += 1

    async def _gen_dploot(arguments: dict, tool_name: str, _cmd='dploot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dploot')(_gen_dploot)
    _reg += 1

    async def _gen_dr0p1t(arguments: dict, tool_name: str, _cmd='dr0p1t') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_dr0p1t')(_gen_dr0p1t)
    _reg += 1

    async def _gen_duckyspark(arguments: dict, tool_name: str, _cmd='duckyspark') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_duckyspark')(_gen_duckyspark)
    _reg += 1

    async def _gen_edr_detect(arguments: dict, tool_name: str, _cmd='edr_detect') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_edr_detect')(_gen_edr_detect)
    _reg += 1

    async def _gen_edr_profile(arguments: dict, tool_name: str, _cmd='edr_profile') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_edr_profile')(_gen_edr_profile)
    _reg += 1

    async def _gen_edr_script(arguments: dict, tool_name: str, _cmd='edr_script') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_edr_script')(_gen_edr_script)
    _reg += 1

    async def _gen_emp3r0r(arguments: dict, tool_name: str, _cmd='emp3r0r') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_emp3r0r')(_gen_emp3r0r)
    _reg += 1

    async def _gen_empire(arguments: dict, tool_name: str, _cmd='empire') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_empire')(_gen_empire)
    _reg += 1

    async def _gen_encode(arguments: dict, tool_name: str, _cmd='encode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_encode')(_gen_encode)
    _reg += 1

    async def _gen_encoderpayload(arguments: dict, tool_name: str, _cmd='encoderpayload') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_encoderpayload')(_gen_encoderpayload)
    _reg += 1

    async def _gen_encodewinbase64(arguments: dict, tool_name: str, _cmd='encodewinbase64') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_encodewinbase64')(_gen_encodewinbase64)
    _reg += 1

    async def _gen_encrypt(arguments: dict, tool_name: str, _cmd='encrypt') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_encrypt')(_gen_encrypt)
    _reg += 1

    async def _gen_engage(arguments: dict, tool_name: str, _cmd='engage') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_engage')(_gen_engage)
    _reg += 1

    async def _gen_enum4linux(arguments: dict, tool_name: str, _cmd='enum4linux') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_enum4linux')(_gen_enum4linux)
    _reg += 1

    async def _gen_enum4linux_ng(arguments: dict, tool_name: str, _cmd='enum4linux_ng') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_enum4linux_ng')(_gen_enum4linux_ng)
    _reg += 1

    async def _gen_eternal(arguments: dict, tool_name: str, _cmd='eternal') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_eternal')(_gen_eternal)
    _reg += 1

    async def _gen_evasion(arguments: dict, tool_name: str, _cmd='evasion') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evasion')(_gen_evasion)
    _reg += 1

    async def _gen_evasive(arguments: dict, tool_name: str, _cmd='evasive') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evasive')(_gen_evasive)
    _reg += 1

    async def _gen_evasive_payload(arguments: dict, tool_name: str, _cmd='evasive_payload') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evasive_payload')(_gen_evasive_payload)
    _reg += 1

    async def _gen_event_log(arguments: dict, tool_name: str, _cmd='event_log') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_event_log')(_gen_event_log)
    _reg += 1

    async def _gen_evidence(arguments: dict, tool_name: str, _cmd='evidence') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evidence')(_gen_evidence)
    _reg += 1

    async def _gen_evil_ssdp(arguments: dict, tool_name: str, _cmd='evil_ssdp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evil_ssdp')(_gen_evil_ssdp)
    _reg += 1

    async def _gen_evilwinrm(arguments: dict, tool_name: str, _cmd='evilwinrm') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_evilwinrm')(_gen_evilwinrm)
    _reg += 1

    async def _gen_excelntdonut(arguments: dict, tool_name: str, _cmd='excelntdonut') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_excelntdonut')(_gen_excelntdonut)
    _reg += 1

    async def _gen_exe2bin(arguments: dict, tool_name: str, _cmd='exe2bin') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exe2bin')(_gen_exe2bin)
    _reg += 1

    async def _gen_exe2donutbin(arguments: dict, tool_name: str, _cmd='exe2donutbin') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exe2donutbin')(_gen_exe2donutbin)
    _reg += 1

    async def _gen_exfil_auto(arguments: dict, tool_name: str, _cmd='exfil_auto') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_auto')(_gen_exfil_auto)
    _reg += 1

    async def _gen_exfil_discord(arguments: dict, tool_name: str, _cmd='exfil_discord') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_discord')(_gen_exfil_discord)
    _reg += 1

    async def _gen_exfil_dns(arguments: dict, tool_name: str, _cmd='exfil_dns') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_dns')(_gen_exfil_dns)
    _reg += 1

    async def _gen_exfil_gcs(arguments: dict, tool_name: str, _cmd='exfil_gcs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_gcs')(_gen_exfil_gcs)
    _reg += 1

    async def _gen_exfil_http(arguments: dict, tool_name: str, _cmd='exfil_http') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_http')(_gen_exfil_http)
    _reg += 1

    async def _gen_exfil_s3(arguments: dict, tool_name: str, _cmd='exfil_s3') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_s3')(_gen_exfil_s3)
    _reg += 1

    async def _gen_exfil_start_server(arguments: dict, tool_name: str, _cmd='exfil_start_server') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_start_server')(_gen_exfil_start_server)
    _reg += 1

    async def _gen_exfil_telegram(arguments: dict, tool_name: str, _cmd='exfil_telegram') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exfil_telegram')(_gen_exfil_telegram)
    _reg += 1

    async def _gen_exit(arguments: dict, tool_name: str, _cmd='exit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_exit')(_gen_exit)
    _reg += 1

    async def _gen_explore(arguments: dict, tool_name: str, _cmd='explore') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_explore')(_gen_explore)
    _reg += 1

    async def _gen_extract_ports(arguments: dict, tool_name: str, _cmd='extract_ports') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_extract_ports')(_gen_extract_ports)
    _reg += 1

    async def _gen_extract_yaml(arguments: dict, tool_name: str, _cmd='extract_yaml') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_extract_yaml')(_gen_extract_yaml)
    _reg += 1

    async def _gen_eyewitness(arguments: dict, tool_name: str, _cmd='eyewitness') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_eyewitness')(_gen_eyewitness)
    _reg += 1

    async def _gen_eyewitness_py(arguments: dict, tool_name: str, _cmd='eyewitness_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_eyewitness_py')(_gen_eyewitness_py)
    _reg += 1

    async def _gen_feroxbuster(arguments: dict, tool_name: str, _cmd='feroxbuster') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_feroxbuster')(_gen_feroxbuster)
    _reg += 1

    async def _gen_filtering(arguments: dict, tool_name: str, _cmd='filtering') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_filtering')(_gen_filtering)
    _reg += 1

    async def _gen_finalrecon(arguments: dict, tool_name: str, _cmd='finalrecon') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_finalrecon')(_gen_finalrecon)
    _reg += 1

    async def _gen_find(arguments: dict, tool_name: str, _cmd='find') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_find')(_gen_find)
    _reg += 1

    async def _gen_finger_user_enum(arguments: dict, tool_name: str, _cmd='finger_user_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_finger_user_enum')(_gen_finger_user_enum)
    _reg += 1

    async def _gen_fixel(arguments: dict, tool_name: str, _cmd='fixel') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_fixel')(_gen_fixel)
    _reg += 1

    async def _gen_fixperm(arguments: dict, tool_name: str, _cmd='fixperm') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_fixperm')(_gen_fixperm)
    _reg += 1

    async def _gen_follina(arguments: dict, tool_name: str, _cmd='follina') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_follina')(_gen_follina)
    _reg += 1

    async def _gen_form(arguments: dict, tool_name: str, _cmd='form') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_form')(_gen_form)
    _reg += 1

    async def _gen_ftp(arguments: dict, tool_name: str, _cmd='ftp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ftp')(_gen_ftp)
    _reg += 1

    async def _gen_fuzz(arguments: dict, tool_name: str, _cmd='fuzz') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_fuzz')(_gen_fuzz)
    _reg += 1

    async def _gen_fz(arguments: dict, tool_name: str, _cmd='fz') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_fz')(_gen_fz)
    _reg += 1

    async def _gen_gencert(arguments: dict, tool_name: str, _cmd='gencert') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gencert')(_gen_gencert)
    _reg += 1

    async def _gen_generate(arguments: dict, tool_name: str, _cmd='generate') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_generate')(_gen_generate)
    _reg += 1

    async def _gen_generate_playbook(arguments: dict, tool_name: str, _cmd='generate_playbook') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_generate_playbook')(_gen_generate_playbook)
    _reg += 1

    async def _gen_generate_revshell(arguments: dict, tool_name: str, _cmd='generate_revshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_generate_revshell')(_gen_generate_revshell)
    _reg += 1

    async def _gen_generatedic(arguments: dict, tool_name: str, _cmd='generatedic') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_generatedic')(_gen_generatedic)
    _reg += 1

    async def _gen_getTGT(arguments: dict, tool_name: str, _cmd='getTGT') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getTGT')(_gen_getTGT)
    _reg += 1

    async def _gen_get_avaible_actions(arguments: dict, tool_name: str, _cmd='get_avaible_actions') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_get_avaible_actions')(_gen_get_avaible_actions)
    _reg += 1

    async def _gen_getadusers(arguments: dict, tool_name: str, _cmd='getadusers') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getadusers')(_gen_getadusers)
    _reg += 1

    async def _gen_getcap(arguments: dict, tool_name: str, _cmd='getcap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getcap')(_gen_getcap)
    _reg += 1

    async def _gen_getnpusers(arguments: dict, tool_name: str, _cmd='getnpusers') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getnpusers')(_gen_getnpusers)
    _reg += 1

    async def _gen_getnthash_py(arguments: dict, tool_name: str, _cmd='getnthash_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getnthash_py')(_gen_getnthash_py)
    _reg += 1

    async def _gen_gets4uticket_py(arguments: dict, tool_name: str, _cmd='gets4uticket_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gets4uticket_py')(_gen_gets4uticket_py)
    _reg += 1

    async def _gen_getseclist(arguments: dict, tool_name: str, _cmd='getseclist') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getseclist')(_gen_getseclist)
    _reg += 1

    async def _gen_gettgtpkinit_py(arguments: dict, tool_name: str, _cmd='gettgtpkinit_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gettgtpkinit_py')(_gen_gettgtpkinit_py)
    _reg += 1

    async def _gen_getuserspns(arguments: dict, tool_name: str, _cmd='getuserspns') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_getuserspns')(_gen_getuserspns)
    _reg += 1

    async def _gen_gitdumper(arguments: dict, tool_name: str, _cmd='gitdumper') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gitdumper')(_gen_gitdumper)
    _reg += 1

    async def _gen_gitlab_enum(arguments: dict, tool_name: str, _cmd='gitlab_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gitlab_enum')(_gen_gitlab_enum)
    _reg += 1

    async def _gen_gmsadumper(arguments: dict, tool_name: str, _cmd='gmsadumper') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gmsadumper')(_gen_gmsadumper)
    _reg += 1

    async def _gen_gobuster(arguments: dict, tool_name: str, _cmd='gobuster') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gobuster')(_gen_gobuster)
    _reg += 1

    async def _gen_god_nodes(arguments: dict, tool_name: str, _cmd='god_nodes') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_god_nodes')(_gen_god_nodes)
    _reg += 1

    async def _gen_gospherus(arguments: dict, tool_name: str, _cmd='gospherus') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gospherus')(_gen_gospherus)
    _reg += 1

    async def _gen_gospider(arguments: dict, tool_name: str, _cmd='gospider') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gospider')(_gen_gospider)
    _reg += 1

    async def _gen_gowitness(arguments: dict, tool_name: str, _cmd='gowitness') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gowitness')(_gen_gowitness)
    _reg += 1

    async def _gen_gpt(arguments: dict, tool_name: str, _cmd='gpt') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gpt')(_gen_gpt)
    _reg += 1

    async def _gen_graph(arguments: dict, tool_name: str, _cmd='graph') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_graph')(_gen_graph)
    _reg += 1

    async def _gen_graph_overlay(arguments: dict, tool_name: str, _cmd='graph_overlay') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_graph_overlay')(_gen_graph_overlay)
    _reg += 1

    async def _gen_graudit(arguments: dict, tool_name: str, _cmd='graudit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_graudit')(_gen_graudit)
    _reg += 1

    async def _gen_greatSCT(arguments: dict, tool_name: str, _cmd='greatSCT') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_greatSCT')(_gen_greatSCT)
    _reg += 1

    async def _gen_grep_log(arguments: dict, tool_name: str, _cmd='grep_log') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_grep_log')(_gen_grep_log)
    _reg += 1

    async def _gen_grisun0(arguments: dict, tool_name: str, _cmd='grisun0') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_grisun0')(_gen_grisun0)
    _reg += 1

    async def _gen_grisun0w(arguments: dict, tool_name: str, _cmd='grisun0w') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_grisun0w')(_gen_grisun0w)
    _reg += 1

    async def _gen_groq(arguments: dict, tool_name: str, _cmd='groq') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_groq')(_gen_groq)
    _reg += 1

    async def _gen_gtfo(arguments: dict, tool_name: str, _cmd='gtfo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gtfo')(_gen_gtfo)
    _reg += 1

    async def _gen_gym(arguments: dict, tool_name: str, _cmd='gym') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_gym')(_gen_gym)
    _reg += 1

    async def _gen_h(arguments: dict, tool_name: str, _cmd='h') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_h')(_gen_h)
    _reg += 1

    async def _gen_hashcat(arguments: dict, tool_name: str, _cmd='hashcat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hashcat')(_gen_hashcat)
    _reg += 1

    async def _gen_hex2shellcode(arguments: dict, tool_name: str, _cmd='hex2shellcode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hex2shellcode')(_gen_hex2shellcode)
    _reg += 1

    async def _gen_hex_to_plaintext(arguments: dict, tool_name: str, _cmd='hex_to_plaintext') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hex_to_plaintext')(_gen_hex_to_plaintext)
    _reg += 1

    async def _gen_hooks(arguments: dict, tool_name: str, _cmd='hooks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks')(_gen_hooks)
    _reg += 1

    async def _gen_hooks_add(arguments: dict, tool_name: str, _cmd='hooks_add') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks_add')(_gen_hooks_add)
    _reg += 1

    async def _gen_hooks_enable(arguments: dict, tool_name: str, _cmd='hooks_enable') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks_enable')(_gen_hooks_enable)
    _reg += 1

    async def _gen_hooks_fire(arguments: dict, tool_name: str, _cmd='hooks_fire') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks_fire')(_gen_hooks_fire)
    _reg += 1

    async def _gen_hooks_list(arguments: dict, tool_name: str, _cmd='hooks_list') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks_list')(_gen_hooks_list)
    _reg += 1

    async def _gen_hooks_remove(arguments: dict, tool_name: str, _cmd='hooks_remove') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hooks_remove')(_gen_hooks_remove)
    _reg += 1

    async def _gen_hostdiscover(arguments: dict, tool_name: str, _cmd='hostdiscover') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hostdiscover')(_gen_hostdiscover)
    _reg += 1

    async def _gen_hound(arguments: dict, tool_name: str, _cmd='hound') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hound')(_gen_hound)
    _reg += 1

    async def _gen_http_exfil_server(arguments: dict, tool_name: str, _cmd='http_exfil_server') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_http_exfil_server')(_gen_http_exfil_server)
    _reg += 1

    async def _gen_httprobe(arguments: dict, tool_name: str, _cmd='httprobe') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_httprobe')(_gen_httprobe)
    _reg += 1

    async def _gen_hunt(arguments: dict, tool_name: str, _cmd='hunt') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hunt')(_gen_hunt)
    _reg += 1

    async def _gen_hydra(arguments: dict, tool_name: str, _cmd='hydra') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_hydra')(_gen_hydra)
    _reg += 1

    async def _gen_id_rsa(arguments: dict, tool_name: str, _cmd='id_rsa') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_id_rsa')(_gen_id_rsa)
    _reg += 1

    async def _gen_ignorearp(arguments: dict, tool_name: str, _cmd='ignorearp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ignorearp')(_gen_ignorearp)
    _reg += 1

    async def _gen_ignoreicmp(arguments: dict, tool_name: str, _cmd='ignoreicmp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ignoreicmp')(_gen_ignoreicmp)
    _reg += 1

    async def _gen_iis_webdav_upload_asp(arguments: dict, tool_name: str, _cmd='iis_webdav_upload_asp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_iis_webdav_upload_asp')(_gen_iis_webdav_upload_asp)
    _reg += 1

    async def _gen_img2cookie(arguments: dict, tool_name: str, _cmd='img2cookie') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_img2cookie')(_gen_img2cookie)
    _reg += 1

    async def _gen_img2vid(arguments: dict, tool_name: str, _cmd='img2vid') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_img2vid')(_gen_img2vid)
    _reg += 1

    async def _gen_internet_proxy(arguments: dict, tool_name: str, _cmd='internet_proxy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_internet_proxy')(_gen_internet_proxy)
    _reg += 1

    async def _gen_ip(arguments: dict, tool_name: str, _cmd='ip') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ip')(_gen_ip)
    _reg += 1

    async def _gen_ip2asn(arguments: dict, tool_name: str, _cmd='ip2asn') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ip2asn')(_gen_ip2asn)
    _reg += 1

    async def _gen_ip2hex(arguments: dict, tool_name: str, _cmd='ip2hex') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ip2hex')(_gen_ip2hex)
    _reg += 1

    async def _gen_ipinfo(arguments: dict, tool_name: str, _cmd='ipinfo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ipinfo')(_gen_ipinfo)
    _reg += 1

    async def _gen_ipp(arguments: dict, tool_name: str, _cmd='ipp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ipp')(_gen_ipp)
    _reg += 1

    async def _gen_issue_command_to_c2(arguments: dict, tool_name: str, _cmd='issue_command_to_c2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_issue_command_to_c2')(_gen_issue_command_to_c2)
    _reg += 1

    async def _gen_ivy(arguments: dict, tool_name: str, _cmd='ivy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ivy')(_gen_ivy)
    _reg += 1

    async def _gen_jenkins_enum(arguments: dict, tool_name: str, _cmd='jenkins_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_jenkins_enum')(_gen_jenkins_enum)
    _reg += 1

    async def _gen_john2hash(arguments: dict, tool_name: str, _cmd='john2hash') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_john2hash')(_gen_john2hash)
    _reg += 1

    async def _gen_john2keepas(arguments: dict, tool_name: str, _cmd='john2keepas') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_john2keepas')(_gen_john2keepas)
    _reg += 1

    async def _gen_john2zip(arguments: dict, tool_name: str, _cmd='john2zip') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_john2zip')(_gen_john2zip)
    _reg += 1

    async def _gen_jwt_tool(arguments: dict, tool_name: str, _cmd='jwt_tool') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_jwt_tool')(_gen_jwt_tool)
    _reg += 1

    async def _gen_k8s_enum(arguments: dict, tool_name: str, _cmd='k8s_enum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_k8s_enum')(_gen_k8s_enum)
    _reg += 1

    async def _gen_k8s_pods(arguments: dict, tool_name: str, _cmd='k8s_pods') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_k8s_pods')(_gen_k8s_pods)
    _reg += 1

    async def _gen_k8s_secrets(arguments: dict, tool_name: str, _cmd='k8s_secrets') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_k8s_secrets')(_gen_k8s_secrets)
    _reg += 1

    async def _gen_karma(arguments: dict, tool_name: str, _cmd='karma') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_karma')(_gen_karma)
    _reg += 1

    async def _gen_keepass(arguments: dict, tool_name: str, _cmd='keepass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_keepass')(_gen_keepass)
    _reg += 1

    async def _gen_kerbrute(arguments: dict, tool_name: str, _cmd='kerbrute') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_kerbrute')(_gen_kerbrute)
    _reg += 1

    async def _gen_kick(arguments: dict, tool_name: str, _cmd='kick') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_kick')(_gen_kick)
    _reg += 1

    async def _gen_knokknok(arguments: dict, tool_name: str, _cmd='knokknok') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_knokknok')(_gen_knokknok)
    _reg += 1

    async def _gen_krbrelayx_py(arguments: dict, tool_name: str, _cmd='krbrelayx_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_krbrelayx_py')(_gen_krbrelayx_py)
    _reg += 1

    async def _gen_kusa(arguments: dict, tool_name: str, _cmd='kusa') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_kusa')(_gen_kusa)
    _reg += 1

    async def _gen_l00t(arguments: dict, tool_name: str, _cmd='l00t') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_l00t')(_gen_l00t)
    _reg += 1

    async def _gen_lab(arguments: dict, tool_name: str, _cmd='lab') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lab')(_gen_lab)
    _reg += 1

    async def _gen_lateral_mov_lin(arguments: dict, tool_name: str, _cmd='lateral_mov_lin') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lateral_mov_lin')(_gen_lateral_mov_lin)
    _reg += 1

    async def _gen_launchpad(arguments: dict, tool_name: str, _cmd='launchpad') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_launchpad')(_gen_launchpad)
    _reg += 1

    async def _gen_lazy_payload_keys(arguments: dict, tool_name: str, _cmd='lazy_payload_keys') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazy_payload_keys')(_gen_lazy_payload_keys)
    _reg += 1

    async def _gen_lazy_runtime(arguments: dict, tool_name: str, _cmd='lazy_runtime') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazy_runtime')(_gen_lazy_runtime)
    _reg += 1

    async def _gen_lazynmap(arguments: dict, tool_name: str, _cmd='lazynmap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazynmap')(_gen_lazynmap)
    _reg += 1

    async def _gen_lazypwn(arguments: dict, tool_name: str, _cmd='lazypwn') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazypwn')(_gen_lazypwn)
    _reg += 1

    async def _gen_lazyreport(arguments: dict, tool_name: str, _cmd='lazyreport') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazyreport')(_gen_lazyreport)
    _reg += 1

    async def _gen_lazyscript(arguments: dict, tool_name: str, _cmd='lazyscript') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazyscript')(_gen_lazyscript)
    _reg += 1

    async def _gen_lazywebshell(arguments: dict, tool_name: str, _cmd='lazywebshell') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lazywebshell')(_gen_lazywebshell)
    _reg += 1

    async def _gen_ldapdomaindump(arguments: dict, tool_name: str, _cmd='ldapdomaindump') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ldapdomaindump')(_gen_ldapdomaindump)
    _reg += 1

    async def _gen_ldapsearch(arguments: dict, tool_name: str, _cmd='ldapsearch') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ldapsearch')(_gen_ldapsearch)
    _reg += 1

    async def _gen_les(arguments: dict, tool_name: str, _cmd='les') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_les')(_gen_les)
    _reg += 1

    async def _gen_lfi(arguments: dict, tool_name: str, _cmd='lfi') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lfi')(_gen_lfi)
    _reg += 1

    async def _gen_ligolo(arguments: dict, tool_name: str, _cmd='ligolo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ligolo')(_gen_ligolo)
    _reg += 1

    async def _gen_links(arguments: dict, tool_name: str, _cmd='links') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_links')(_gen_links)
    _reg += 1

    async def _gen_linpeas(arguments: dict, tool_name: str, _cmd='linpeas') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_linpeas')(_gen_linpeas)
    _reg += 1

    async def _gen_list(arguments: dict, tool_name: str, _cmd='list') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_list')(_gen_list)
    _reg += 1

    async def _gen_listaliases(arguments: dict, tool_name: str, _cmd='listaliases') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_listaliases')(_gen_listaliases)
    _reg += 1

    async def _gen_listener(arguments: dict, tool_name: str, _cmd='listener') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_listener')(_gen_listener)
    _reg += 1

    async def _gen_listener_go(arguments: dict, tool_name: str, _cmd='listener_go') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_listener_go')(_gen_listener_go)
    _reg += 1

    async def _gen_listener_py(arguments: dict, tool_name: str, _cmd='listener_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_listener_py')(_gen_listener_py)
    _reg += 1

    async def _gen_llm_budget(arguments: dict, tool_name: str, _cmd='llm_budget') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_llm_budget')(_gen_llm_budget)
    _reg += 1

    async def _gen_load_session(arguments: dict, tool_name: str, _cmd='load_session') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_load_session')(_gen_load_session)
    _reg += 1

    async def _gen_lock_target(arguments: dict, tool_name: str, _cmd='lock_target') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lock_target')(_gen_lock_target)
    _reg += 1

    async def _gen_login(arguments: dict, tool_name: str, _cmd='login') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_login')(_gen_login)
    _reg += 1

    async def _gen_logout(arguments: dict, tool_name: str, _cmd='logout') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_logout')(_gen_logout)
    _reg += 1

    async def _gen_lol(arguments: dict, tool_name: str, _cmd='lol') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lol')(_gen_lol)
    _reg += 1

    async def _gen_lookupsid(arguments: dict, tool_name: str, _cmd='lookupsid') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lookupsid')(_gen_lookupsid)
    _reg += 1

    async def _gen_lookupsid_py(arguments: dict, tool_name: str, _cmd='lookupsid_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lookupsid_py')(_gen_lookupsid_py)
    _reg += 1

    async def _gen_loot(arguments: dict, tool_name: str, _cmd='loot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_loot')(_gen_loot)
    _reg += 1

    async def _gen_loxs(arguments: dict, tool_name: str, _cmd='loxs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_loxs')(_gen_loxs)
    _reg += 1

    async def _gen_lynis(arguments: dict, tool_name: str, _cmd='lynis') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_lynis')(_gen_lynis)
    _reg += 1

    async def _gen_macos_keychain(arguments: dict, tool_name: str, _cmd='macos_keychain') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_macos_keychain')(_gen_macos_keychain)
    _reg += 1

    async def _gen_macos_persist(arguments: dict, tool_name: str, _cmd='macos_persist') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_macos_persist')(_gen_macos_persist)
    _reg += 1

    async def _gen_macos_tcc(arguments: dict, tool_name: str, _cmd='macos_tcc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_macos_tcc')(_gen_macos_tcc)
    _reg += 1

    async def _gen_magicrecon(arguments: dict, tool_name: str, _cmd='magicrecon') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_magicrecon')(_gen_magicrecon)
    _reg += 1

    async def _gen_makerc(arguments: dict, tool_name: str, _cmd='makerc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_makerc')(_gen_makerc)
    _reg += 1

    async def _gen_malwarebazar(arguments: dict, tool_name: str, _cmd='malwarebazar') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_malwarebazar')(_gen_malwarebazar)
    _reg += 1

    async def _gen_marketplace(arguments: dict, tool_name: str, _cmd='marketplace') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_marketplace')(_gen_marketplace)
    _reg += 1

    async def _gen_marketplace_config(arguments: dict, tool_name: str, _cmd='marketplace_config') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_marketplace_config')(_gen_marketplace_config)
    _reg += 1

    async def _gen_medusa(arguments: dict, tool_name: str, _cmd='medusa') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_medusa')(_gen_medusa)
    _reg += 1

    async def _gen_metabigor(arguments: dict, tool_name: str, _cmd='metabigor') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_metabigor')(_gen_metabigor)
    _reg += 1

    async def _gen_mfa_bypass(arguments: dict, tool_name: str, _cmd='mfa_bypass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mfa_bypass')(_gen_mfa_bypass)
    _reg += 1

    async def _gen_mimikatzpy(arguments: dict, tool_name: str, _cmd='mimikatzpy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mimikatzpy')(_gen_mimikatzpy)
    _reg += 1

    async def _gen_mitre_test(arguments: dict, tool_name: str, _cmd='mitre_test') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mitre_test')(_gen_mitre_test)
    _reg += 1

    async def _gen_mkrc(arguments: dict, tool_name: str, _cmd='mkrc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mkrc')(_gen_mkrc)
    _reg += 1

    async def _gen_morse(arguments: dict, tool_name: str, _cmd='morse') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_morse')(_gen_morse)
    _reg += 1

    async def _gen_mqtt_check_py(arguments: dict, tool_name: str, _cmd='mqtt_check_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mqtt_check_py')(_gen_mqtt_check_py)
    _reg += 1

    async def _gen_ms08_067_netapi(arguments: dict, tool_name: str, _cmd='ms08_067_netapi') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ms08_067_netapi')(_gen_ms08_067_netapi)
    _reg += 1

    async def _gen_msf(arguments: dict, tool_name: str, _cmd='msf') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_msf')(_gen_msf)
    _reg += 1

    async def _gen_msfpc(arguments: dict, tool_name: str, _cmd='msfpc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_msfpc')(_gen_msfpc)
    _reg += 1

    async def _gen_msfrpc(arguments: dict, tool_name: str, _cmd='msfrpc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_msfrpc')(_gen_msfrpc)
    _reg += 1

    async def _gen_msfshellcoder(arguments: dict, tool_name: str, _cmd='msfshellcoder') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_msfshellcoder')(_gen_msfshellcoder)
    _reg += 1

    async def _gen_mssqlcli(arguments: dict, tool_name: str, _cmd='mssqlcli') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mssqlcli')(_gen_mssqlcli)
    _reg += 1

    async def _gen_mutate_shellcode(arguments: dict, tool_name: str, _cmd='mutate_shellcode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_mutate_shellcode')(_gen_mutate_shellcode)
    _reg += 1

    async def _gen_my_playbook(arguments: dict, tool_name: str, _cmd='my_playbook') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_my_playbook')(_gen_my_playbook)
    _reg += 1

    async def _gen_name_the_hash(arguments: dict, tool_name: str, _cmd='name_the_hash') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_name_the_hash')(_gen_name_the_hash)
    _reg += 1

    async def _gen_nano(arguments: dict, tool_name: str, _cmd='nano') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nano')(_gen_nano)
    _reg += 1

    async def _gen_nbtscan(arguments: dict, tool_name: str, _cmd='nbtscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nbtscan')(_gen_nbtscan)
    _reg += 1

    async def _gen_nc(arguments: dict, tool_name: str, _cmd='nc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nc')(_gen_nc)
    _reg += 1

    async def _gen_neighbors(arguments: dict, tool_name: str, _cmd='neighbors') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_neighbors')(_gen_neighbors)
    _reg += 1

    async def _gen_net_rpc_addmem(arguments: dict, tool_name: str, _cmd='net_rpc_addmem') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_net_rpc_addmem')(_gen_net_rpc_addmem)
    _reg += 1

    async def _gen_netexec(arguments: dict, tool_name: str, _cmd='netexec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_netexec')(_gen_netexec)
    _reg += 1

    async def _gen_netview(arguments: dict, tool_name: str, _cmd='netview') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_netview')(_gen_netview)
    _reg += 1

    async def _gen_news(arguments: dict, tool_name: str, _cmd='news') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_news')(_gen_news)
    _reg += 1

    async def _gen_next(arguments: dict, tool_name: str, _cmd='next') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_next')(_gen_next)
    _reg += 1

    async def _gen_ngrok(arguments: dict, tool_name: str, _cmd='ngrok') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ngrok')(_gen_ngrok)
    _reg += 1

    async def _gen_nikto(arguments: dict, tool_name: str, _cmd='nikto') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nikto')(_gen_nikto)
    _reg += 1

    async def _gen_nmapscript(arguments: dict, tool_name: str, _cmd='nmapscript') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nmapscript')(_gen_nmapscript)
    _reg += 1

    async def _gen_nmapscripthelp(arguments: dict, tool_name: str, _cmd='nmapscripthelp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nmapscripthelp')(_gen_nmapscripthelp)
    _reg += 1

    async def _gen_note(arguments: dict, tool_name: str, _cmd='note') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_note')(_gen_note)
    _reg += 1

    async def _gen_notify(arguments: dict, tool_name: str, _cmd='notify') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_notify')(_gen_notify)
    _reg += 1

    async def _gen_ntpdate(arguments: dict, tool_name: str, _cmd='ntpdate') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ntpdate')(_gen_ntpdate)
    _reg += 1

    async def _gen_nuclei(arguments: dict, tool_name: str, _cmd='nuclei') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_nuclei')(_gen_nuclei)
    _reg += 1

    async def _gen_odat(arguments: dict, tool_name: str, _cmd='odat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_odat')(_gen_odat)
    _reg += 1

    async def _gen_ofuscate_string(arguments: dict, tool_name: str, _cmd='ofuscate_string') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ofuscate_string')(_gen_ofuscate_string)
    _reg += 1

    async def _gen_ofuscatesh(arguments: dict, tool_name: str, _cmd='ofuscatesh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ofuscatesh')(_gen_ofuscatesh)
    _reg += 1

    async def _gen_ofuscatorps1(arguments: dict, tool_name: str, _cmd='ofuscatorps1') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ofuscatorps1')(_gen_ofuscatorps1)
    _reg += 1

    async def _gen_op_create(arguments: dict, tool_name: str, _cmd='op_create') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_create')(_gen_op_create)
    _reg += 1

    async def _gen_op_list(arguments: dict, tool_name: str, _cmd='op_list') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_list')(_gen_op_list)
    _reg += 1

    async def _gen_op_pause(arguments: dict, tool_name: str, _cmd='op_pause') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_pause')(_gen_op_pause)
    _reg += 1

    async def _gen_op_plan(arguments: dict, tool_name: str, _cmd='op_plan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_plan')(_gen_op_plan)
    _reg += 1

    async def _gen_op_report(arguments: dict, tool_name: str, _cmd='op_report') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_report')(_gen_op_report)
    _reg += 1

    async def _gen_op_resume(arguments: dict, tool_name: str, _cmd='op_resume') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_resume')(_gen_op_resume)
    _reg += 1

    async def _gen_op_start(arguments: dict, tool_name: str, _cmd='op_start') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_start')(_gen_op_start)
    _reg += 1

    async def _gen_op_status(arguments: dict, tool_name: str, _cmd='op_status') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_status')(_gen_op_status)
    _reg += 1

    async def _gen_op_stop(arguments: dict, tool_name: str, _cmd='op_stop') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_stop')(_gen_op_stop)
    _reg += 1

    async def _gen_op_timeline(arguments: dict, tool_name: str, _cmd='op_timeline') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_op_timeline')(_gen_op_timeline)
    _reg += 1

    async def _gen_openredirex(arguments: dict, tool_name: str, _cmd='openredirex') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_openredirex')(_gen_openredirex)
    _reg += 1

    async def _gen_openssl_sclient(arguments: dict, tool_name: str, _cmd='openssl_sclient') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_openssl_sclient')(_gen_openssl_sclient)
    _reg += 1

    async def _gen_operator_create(arguments: dict, tool_name: str, _cmd='operator_create') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_operator_create')(_gen_operator_create)
    _reg += 1

    async def _gen_operator_delete(arguments: dict, tool_name: str, _cmd='operator_delete') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_operator_delete')(_gen_operator_delete)
    _reg += 1

    async def _gen_operator_load(arguments: dict, tool_name: str, _cmd='operator_load') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_operator_load')(_gen_operator_load)
    _reg += 1

    async def _gen_operators(arguments: dict, tool_name: str, _cmd='operators') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_operators')(_gen_operators)
    _reg += 1

    async def _gen_opsec(arguments: dict, tool_name: str, _cmd='opsec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_opsec')(_gen_opsec)
    _reg += 1

    async def _gen_orchestrate(arguments: dict, tool_name: str, _cmd='orchestrate') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_orchestrate')(_gen_orchestrate)
    _reg += 1

    async def _gen_osmedeus(arguments: dict, tool_name: str, _cmd='osmedeus') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_osmedeus')(_gen_osmedeus)
    _reg += 1

    async def _gen_owneredit(arguments: dict, tool_name: str, _cmd='owneredit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_owneredit')(_gen_owneredit)
    _reg += 1

    async def _gen_package_squat(arguments: dict, tool_name: str, _cmd='package_squat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_package_squat')(_gen_package_squat)
    _reg += 1

    async def _gen_padbuster(arguments: dict, tool_name: str, _cmd='padbuster') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_padbuster')(_gen_padbuster)
    _reg += 1

    async def _gen_palette_k(arguments: dict, tool_name: str, _cmd='palette_k') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_palette_k')(_gen_palette_k)
    _reg += 1

    async def _gen_paranoid_meterpreter(arguments: dict, tool_name: str, _cmd='paranoid_meterpreter') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_paranoid_meterpreter')(_gen_paranoid_meterpreter)
    _reg += 1

    async def _gen_parsero(arguments: dict, tool_name: str, _cmd='parsero') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_parsero')(_gen_parsero)
    _reg += 1

    async def _gen_parth(arguments: dict, tool_name: str, _cmd='parth') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_parth')(_gen_parth)
    _reg += 1

    async def _gen_passtightvnc(arguments: dict, tool_name: str, _cmd='passtightvnc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_passtightvnc')(_gen_passtightvnc)
    _reg += 1

    async def _gen_passwordspray(arguments: dict, tool_name: str, _cmd='passwordspray') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_passwordspray')(_gen_passwordspray)
    _reg += 1

    async def _gen_path2hex(arguments: dict, tool_name: str, _cmd='path2hex') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_path2hex')(_gen_path2hex)
    _reg += 1

    async def _gen_payload(arguments: dict, tool_name: str, _cmd='payload') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_payload')(_gen_payload)
    _reg += 1

    async def _gen_penelope(arguments: dict, tool_name: str, _cmd='penelope') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_penelope')(_gen_penelope)
    _reg += 1

    async def _gen_pentest_report(arguments: dict, tool_name: str, _cmd='pentest_report') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pentest_report')(_gen_pentest_report)
    _reg += 1

    async def _gen_pezorsh(arguments: dict, tool_name: str, _cmd='pezorsh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pezorsh')(_gen_pezorsh)
    _reg += 1

    async def _gen_phase(arguments: dict, tool_name: str, _cmd='phase') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_phase')(_gen_phase)
    _reg += 1

    async def _gen_phish_report(arguments: dict, tool_name: str, _cmd='phish_report') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_phish_report')(_gen_phish_report)
    _reg += 1

    async def _gen_phish_serve(arguments: dict, tool_name: str, _cmd='phish_serve') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_phish_serve')(_gen_phish_serve)
    _reg += 1

    async def _gen_phish_wizard(arguments: dict, tool_name: str, _cmd='phish_wizard') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_phish_wizard')(_gen_phish_wizard)
    _reg += 1

    async def _gen_ping(arguments: dict, tool_name: str, _cmd='ping') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ping')(_gen_ping)
    _reg += 1

    async def _gen_pip_proxy(arguments: dict, tool_name: str, _cmd='pip_proxy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pip_proxy')(_gen_pip_proxy)
    _reg += 1

    async def _gen_pip_repo(arguments: dict, tool_name: str, _cmd='pip_repo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pip_repo')(_gen_pip_repo)
    _reg += 1

    async def _gen_pipeline(arguments: dict, tool_name: str, _cmd='pipeline') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pipeline')(_gen_pipeline)
    _reg += 1

    async def _gen_pivot(arguments: dict, tool_name: str, _cmd='pivot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pivot')(_gen_pivot)
    _reg += 1

    async def _gen_pivot_kill(arguments: dict, tool_name: str, _cmd='pivot_kill') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pivot_kill')(_gen_pivot_kill)
    _reg += 1

    async def _gen_pivot_proxy(arguments: dict, tool_name: str, _cmd='pivot_proxy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pivot_proxy')(_gen_pivot_proxy)
    _reg += 1

    async def _gen_pivot_scan(arguments: dict, tool_name: str, _cmd='pivot_scan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pivot_scan')(_gen_pivot_scan)
    _reg += 1

    async def _gen_plan(arguments: dict, tool_name: str, _cmd='plan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_plan')(_gen_plan)
    _reg += 1

    async def _gen_plan_apply(arguments: dict, tool_name: str, _cmd='plan_apply') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_plan_apply')(_gen_plan_apply)
    _reg += 1

    async def _gen_plan_detail(arguments: dict, tool_name: str, _cmd='plan_detail') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_plan_detail')(_gen_plan_detail)
    _reg += 1

    async def _gen_pop(arguments: dict, tool_name: str, _cmd='pop') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pop')(_gen_pop)
    _reg += 1

    async def _gen_portdiscover(arguments: dict, tool_name: str, _cmd='portdiscover') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_portdiscover')(_gen_portdiscover)
    _reg += 1

    async def _gen_ports(arguments: dict, tool_name: str, _cmd='ports') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ports')(_gen_ports)
    _reg += 1

    async def _gen_portservicediscover(arguments: dict, tool_name: str, _cmd='portservicediscover') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_portservicediscover')(_gen_portservicediscover)
    _reg += 1

    async def _gen_powerserver(arguments: dict, tool_name: str, _cmd='powerserver') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_powerserver')(_gen_powerserver)
    _reg += 1

    async def _gen_powershell_cmd_stager(arguments: dict, tool_name: str, _cmd='powershell_cmd_stager') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_powershell_cmd_stager')(_gen_powershell_cmd_stager)
    _reg += 1

    async def _gen_pre2k(arguments: dict, tool_name: str, _cmd='pre2k') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pre2k')(_gen_pre2k)
    _reg += 1

    async def _gen_prev(arguments: dict, tool_name: str, _cmd='prev') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_prev')(_gen_prev)
    _reg += 1

    async def _gen_printerbug_py(arguments: dict, tool_name: str, _cmd='printerbug_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_printerbug_py')(_gen_printerbug_py)
    _reg += 1

    async def _gen_privesc_suggest(arguments: dict, tool_name: str, _cmd='privesc_suggest') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_privesc_suggest')(_gen_privesc_suggest)
    _reg += 1

    async def _gen_process_scans(arguments: dict, tool_name: str, _cmd='process_scans') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_process_scans')(_gen_process_scans)
    _reg += 1

    async def _gen_proxy(arguments: dict, tool_name: str, _cmd='proxy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_proxy')(_gen_proxy)
    _reg += 1

    async def _gen_psexec(arguments: dict, tool_name: str, _cmd='psexec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_psexec')(_gen_psexec)
    _reg += 1

    async def _gen_psexec_py(arguments: dict, tool_name: str, _cmd='psexec_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_psexec_py')(_gen_psexec_py)
    _reg += 1

    async def _gen_pspy(arguments: dict, tool_name: str, _cmd='pspy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pspy')(_gen_pspy)
    _reg += 1

    async def _gen_pth_net(arguments: dict, tool_name: str, _cmd='pth_net') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pth_net')(_gen_pth_net)
    _reg += 1

    async def _gen_pup(arguments: dict, tool_name: str, _cmd='pup') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pup')(_gen_pup)
    _reg += 1

    async def _gen_pwd(arguments: dict, tool_name: str, _cmd='pwd') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pwd')(_gen_pwd)
    _reg += 1

    async def _gen_pwncat(arguments: dict, tool_name: str, _cmd='pwncat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pwncat')(_gen_pwncat)
    _reg += 1

    async def _gen_pwncatcs(arguments: dict, tool_name: str, _cmd='pwncatcs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pwncatcs')(_gen_pwncatcs)
    _reg += 1

    async def _gen_py3ttyup(arguments: dict, tool_name: str, _cmd='py3ttyup') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_py3ttyup')(_gen_py3ttyup)
    _reg += 1

    async def _gen_pyautomate(arguments: dict, tool_name: str, _cmd='pyautomate') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pyautomate')(_gen_pyautomate)
    _reg += 1

    async def _gen_pykerbrute(arguments: dict, tool_name: str, _cmd='pykerbrute') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pykerbrute')(_gen_pykerbrute)
    _reg += 1

    async def _gen_pyoracle2(arguments: dict, tool_name: str, _cmd='pyoracle2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pyoracle2')(_gen_pyoracle2)
    _reg += 1

    async def _gen_pywhisker(arguments: dict, tool_name: str, _cmd='pywhisker') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_pywhisker')(_gen_pywhisker)
    _reg += 1

    async def _gen_qa(arguments: dict, tool_name: str, _cmd='qa') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_qa')(_gen_qa)
    _reg += 1

    async def _gen_rdp(arguments: dict, tool_name: str, _cmd='rdp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rdp')(_gen_rdp)
    _reg += 1

    async def _gen_rdp_check_py(arguments: dict, tool_name: str, _cmd='rdp_check_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rdp_check_py')(_gen_rdp_check_py)
    _reg += 1

    async def _gen_recon(arguments: dict, tool_name: str, _cmd='recon') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_recon')(_gen_recon)
    _reg += 1

    async def _gen_refill_password(arguments: dict, tool_name: str, _cmd='refill_password') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_refill_password')(_gen_refill_password)
    _reg += 1

    async def _gen_reg_py(arguments: dict, tool_name: str, _cmd='reg_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_reg_py')(_gen_reg_py)
    _reg += 1

    async def _gen_regeorg(arguments: dict, tool_name: str, _cmd='regeorg') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_regeorg')(_gen_regeorg)
    _reg += 1

    async def _gen_rejetto_hfs_exec(arguments: dict, tool_name: str, _cmd='rejetto_hfs_exec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rejetto_hfs_exec')(_gen_rejetto_hfs_exec)
    _reg += 1

    async def _gen_reload_addons(arguments: dict, tool_name: str, _cmd='reload_addons') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_reload_addons')(_gen_reload_addons)
    _reg += 1

    async def _gen_report(arguments: dict, tool_name: str, _cmd='report') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_report')(_gen_report)
    _reg += 1

    async def _gen_resource(arguments: dict, tool_name: str, _cmd='resource') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_resource')(_gen_resource)
    _reg += 1

    async def _gen_responder(arguments: dict, tool_name: str, _cmd='responder') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_responder')(_gen_responder)
    _reg += 1

    async def _gen_rev(arguments: dict, tool_name: str, _cmd='rev') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rev')(_gen_rev)
    _reg += 1

    async def _gen_revwin(arguments: dict, tool_name: str, _cmd='revwin') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_revwin')(_gen_revwin)
    _reg += 1

    async def _gen_rhost(arguments: dict, tool_name: str, _cmd='rhost') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rhost')(_gen_rhost)
    _reg += 1

    async def _gen_rich_tui(arguments: dict, tool_name: str, _cmd='rich_tui') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rich_tui')(_gen_rich_tui)
    _reg += 1

    async def _gen_rmfromfind(arguments: dict, tool_name: str, _cmd='rmfromfind') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rmfromfind')(_gen_rmfromfind)
    _reg += 1

    async def _gen_rnc(arguments: dict, tool_name: str, _cmd='rnc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rnc')(_gen_rnc)
    _reg += 1

    async def _gen_rocky(arguments: dict, tool_name: str, _cmd='rocky') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rocky')(_gen_rocky)
    _reg += 1

    async def _gen_rot(arguments: dict, tool_name: str, _cmd='rot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rot')(_gen_rot)
    _reg += 1

    async def _gen_rotate_aes(arguments: dict, tool_name: str, _cmd='rotate_aes') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rotate_aes')(_gen_rotate_aes)
    _reg += 1

    async def _gen_rotf(arguments: dict, tool_name: str, _cmd='rotf') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rotf')(_gen_rotf)
    _reg += 1

    async def _gen_route(arguments: dict, tool_name: str, _cmd='route') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_route')(_gen_route)
    _reg += 1

    async def _gen_rpcclient(arguments: dict, tool_name: str, _cmd='rpcclient') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rpcclient')(_gen_rpcclient)
    _reg += 1

    async def _gen_rpcdump(arguments: dict, tool_name: str, _cmd='rpcdump') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rpcdump')(_gen_rpcdump)
    _reg += 1

    async def _gen_rpcmap_py(arguments: dict, tool_name: str, _cmd='rpcmap_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rpcmap_py')(_gen_rpcmap_py)
    _reg += 1

    async def _gen_rrhost(arguments: dict, tool_name: str, _cmd='rrhost') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rrhost')(_gen_rrhost)
    _reg += 1

    async def _gen_rsync(arguments: dict, tool_name: str, _cmd='rsync') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rsync')(_gen_rsync)
    _reg += 1

    async def _gen_rubeus(arguments: dict, tool_name: str, _cmd='rubeus') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_rubeus')(_gen_rubeus)
    _reg += 1

    async def _gen_run(arguments: dict, tool_name: str, _cmd='run') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_run')(_gen_run)
    _reg += 1

    async def _gen_samdump2(arguments: dict, tool_name: str, _cmd='samdump2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_samdump2')(_gen_samdump2)
    _reg += 1

    async def _gen_samrdump(arguments: dict, tool_name: str, _cmd='samrdump') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_samrdump')(_gen_samrdump)
    _reg += 1

    async def _gen_sandbox(arguments: dict, tool_name: str, _cmd='sandbox') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sandbox')(_gen_sandbox)
    _reg += 1

    async def _gen_sawks(arguments: dict, tool_name: str, _cmd='sawks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sawks')(_gen_sawks)
    _reg += 1

    async def _gen_scans(arguments: dict, tool_name: str, _cmd='scans') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_scans')(_gen_scans)
    _reg += 1

    async def _gen_scarecrow(arguments: dict, tool_name: str, _cmd='scarecrow') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_scarecrow')(_gen_scarecrow)
    _reg += 1

    async def _gen_scavenger(arguments: dict, tool_name: str, _cmd='scavenger') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_scavenger')(_gen_scavenger)
    _reg += 1

    async def _gen_scope(arguments: dict, tool_name: str, _cmd='scope') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_scope')(_gen_scope)
    _reg += 1

    async def _gen_scp(arguments: dict, tool_name: str, _cmd='scp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_scp')(_gen_scp)
    _reg += 1

    async def _gen_seal_credentials(arguments: dict, tool_name: str, _cmd='seal_credentials') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_seal_credentials')(_gen_seal_credentials)
    _reg += 1

    async def _gen_search(arguments: dict, tool_name: str, _cmd='search') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_search')(_gen_search)
    _reg += 1

    async def _gen_searchhash(arguments: dict, tool_name: str, _cmd='searchhash') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_searchhash')(_gen_searchhash)
    _reg += 1

    async def _gen_secretsdump(arguments: dict, tool_name: str, _cmd='secretsdump') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_secretsdump')(_gen_secretsdump)
    _reg += 1

    async def _gen_seo(arguments: dict, tool_name: str, _cmd='seo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_seo')(_gen_seo)
    _reg += 1

    async def _gen_serveralive2(arguments: dict, tool_name: str, _cmd='serveralive2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_serveralive2')(_gen_serveralive2)
    _reg += 1

    async def _gen_service(arguments: dict, tool_name: str, _cmd='service') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_service')(_gen_service)
    _reg += 1

    async def _gen_service_ssh(arguments: dict, tool_name: str, _cmd='service_ssh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_service_ssh')(_gen_service_ssh)
    _reg += 1

    async def _gen_sessionssh(arguments: dict, tool_name: str, _cmd='sessionssh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sessionssh')(_gen_sessionssh)
    _reg += 1

    async def _gen_sessionsshstrace(arguments: dict, tool_name: str, _cmd='sessionsshstrace') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sessionsshstrace')(_gen_sessionsshstrace)
    _reg += 1

    async def _gen_set(arguments: dict, tool_name: str, _cmd='set') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_set')(_gen_set)
    _reg += 1

    async def _gen_set_proxychains(arguments: dict, tool_name: str, _cmd='set_proxychains') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_set_proxychains')(_gen_set_proxychains)
    _reg += 1

    async def _gen_setoolKits(arguments: dict, tool_name: str, _cmd='setoolKits') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_setoolKits')(_gen_setoolKits)
    _reg += 1

    async def _gen_sh(arguments: dict, tool_name: str, _cmd='sh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sh')(_gen_sh)
    _reg += 1

    async def _gen_shadowsocks(arguments: dict, tool_name: str, _cmd='shadowsocks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shadowsocks')(_gen_shadowsocks)
    _reg += 1

    async def _gen_share_finding(arguments: dict, tool_name: str, _cmd='share_finding') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_share_finding')(_gen_share_finding)
    _reg += 1

    async def _gen_sharpshooter(arguments: dict, tool_name: str, _cmd='sharpshooter') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sharpshooter')(_gen_sharpshooter)
    _reg += 1

    async def _gen_shellcode(arguments: dict, tool_name: str, _cmd='shellcode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellcode')(_gen_shellcode)
    _reg += 1

    async def _gen_shellcode2elf(arguments: dict, tool_name: str, _cmd='shellcode2elf') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellcode2elf')(_gen_shellcode2elf)
    _reg += 1

    async def _gen_shellcode2sylk(arguments: dict, tool_name: str, _cmd='shellcode2sylk') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellcode2sylk')(_gen_shellcode2sylk)
    _reg += 1

    async def _gen_shellcode_search(arguments: dict, tool_name: str, _cmd='shellcode_search') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellcode_search')(_gen_shellcode_search)
    _reg += 1

    async def _gen_shellfire(arguments: dict, tool_name: str, _cmd='shellfire') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellfire')(_gen_shellfire)
    _reg += 1

    async def _gen_shellshock(arguments: dict, tool_name: str, _cmd='shellshock') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shellshock')(_gen_shellshock)
    _reg += 1

    async def _gen_sherlock(arguments: dict, tool_name: str, _cmd='sherlock') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sherlock')(_gen_sherlock)
    _reg += 1

    async def _gen_show(arguments: dict, tool_name: str, _cmd='show') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_show')(_gen_show)
    _reg += 1

    async def _gen_shred(arguments: dict, tool_name: str, _cmd='shred') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_shred')(_gen_shred)
    _reg += 1

    async def _gen_sireprat(arguments: dict, tool_name: str, _cmd='sireprat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sireprat')(_gen_sireprat)
    _reg += 1

    async def _gen_sitrep(arguments: dict, tool_name: str, _cmd='sitrep') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sitrep')(_gen_sitrep)
    _reg += 1

    async def _gen_skipfish(arguments: dict, tool_name: str, _cmd='skipfish') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_skipfish')(_gen_skipfish)
    _reg += 1

    async def _gen_sliver_server(arguments: dict, tool_name: str, _cmd='sliver_server') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sliver_server')(_gen_sliver_server)
    _reg += 1

    async def _gen_smalldic(arguments: dict, tool_name: str, _cmd='smalldic') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smalldic')(_gen_smalldic)
    _reg += 1

    async def _gen_smb_exfil(arguments: dict, tool_name: str, _cmd='smb_exfil') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smb_exfil')(_gen_smb_exfil)
    _reg += 1

    async def _gen_smbattack(arguments: dict, tool_name: str, _cmd='smbattack') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbattack')(_gen_smbattack)
    _reg += 1

    async def _gen_smbclient(arguments: dict, tool_name: str, _cmd='smbclient') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbclient')(_gen_smbclient)
    _reg += 1

    async def _gen_smbclient_impacket(arguments: dict, tool_name: str, _cmd='smbclient_impacket') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbclient_impacket')(_gen_smbclient_impacket)
    _reg += 1

    async def _gen_smbclient_py(arguments: dict, tool_name: str, _cmd='smbclient_py') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbclient_py')(_gen_smbclient_py)
    _reg += 1

    async def _gen_smbmap(arguments: dict, tool_name: str, _cmd='smbmap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbmap')(_gen_smbmap)
    _reg += 1

    async def _gen_smbserver(arguments: dict, tool_name: str, _cmd='smbserver') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smbserver')(_gen_smbserver)
    _reg += 1

    async def _gen_smtpuserenum(arguments: dict, tool_name: str, _cmd='smtpuserenum') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_smtpuserenum')(_gen_smtpuserenum)
    _reg += 1

    async def _gen_snmpcheck(arguments: dict, tool_name: str, _cmd='snmpcheck') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_snmpcheck')(_gen_snmpcheck)
    _reg += 1

    async def _gen_snmpwalk(arguments: dict, tool_name: str, _cmd='snmpwalk') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_snmpwalk')(_gen_snmpwalk)
    _reg += 1

    async def _gen_socat(arguments: dict, tool_name: str, _cmd='socat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_socat')(_gen_socat)
    _reg += 1

    async def _gen_spool(arguments: dict, tool_name: str, _cmd='spool') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_spool')(_gen_spool)
    _reg += 1

    async def _gen_spraykatz(arguments: dict, tool_name: str, _cmd='spraykatz') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_spraykatz')(_gen_spraykatz)
    _reg += 1

    async def _gen_sqli(arguments: dict, tool_name: str, _cmd='sqli') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sqli')(_gen_sqli)
    _reg += 1

    async def _gen_sqli_mssql_test(arguments: dict, tool_name: str, _cmd='sqli_mssql_test') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sqli_mssql_test')(_gen_sqli_mssql_test)
    _reg += 1

    async def _gen_sqlmap(arguments: dict, tool_name: str, _cmd='sqlmap') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sqlmap')(_gen_sqlmap)
    _reg += 1

    async def _gen_sqsh(arguments: dict, tool_name: str, _cmd='sqsh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sqsh')(_gen_sqsh)
    _reg += 1

    async def _gen_ss(arguments: dict, tool_name: str, _cmd='ss') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ss')(_gen_ss)
    _reg += 1

    async def _gen_ssh(arguments: dict, tool_name: str, _cmd='ssh') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ssh')(_gen_ssh)
    _reg += 1

    async def _gen_ssh_cmd(arguments: dict, tool_name: str, _cmd='ssh_cmd') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ssh_cmd')(_gen_ssh_cmd)
    _reg += 1

    async def _gen_sshd(arguments: dict, tool_name: str, _cmd='sshd') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sshd')(_gen_sshd)
    _reg += 1

    async def _gen_sshexploit(arguments: dict, tool_name: str, _cmd='sshexploit') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sshexploit')(_gen_sshexploit)
    _reg += 1

    async def _gen_sshkey(arguments: dict, tool_name: str, _cmd='sshkey') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sshkey')(_gen_sshkey)
    _reg += 1

    async def _gen_sslscan(arguments: dict, tool_name: str, _cmd='sslscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sslscan')(_gen_sslscan)
    _reg += 1

    async def _gen_stage(arguments: dict, tool_name: str, _cmd='stage') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_stage')(_gen_stage)
    _reg += 1

    async def _gen_state_snapshot(arguments: dict, tool_name: str, _cmd='state_snapshot') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_state_snapshot')(_gen_state_snapshot)
    _reg += 1

    async def _gen_status_bar(arguments: dict, tool_name: str, _cmd='status_bar') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_status_bar')(_gen_status_bar)
    _reg += 1

    async def _gen_status_tail(arguments: dict, tool_name: str, _cmd='status_tail') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_status_tail')(_gen_status_tail)
    _reg += 1

    async def _gen_stealth_off(arguments: dict, tool_name: str, _cmd='stealth_off') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_stealth_off')(_gen_stealth_off)
    _reg += 1

    async def _gen_stealth_on(arguments: dict, tool_name: str, _cmd='stealth_on') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_stealth_on')(_gen_stealth_on)
    _reg += 1

    async def _gen_stormbreaker(arguments: dict, tool_name: str, _cmd='stormbreaker') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_stormbreaker')(_gen_stormbreaker)
    _reg += 1

    async def _gen_sudo(arguments: dict, tool_name: str, _cmd='sudo') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sudo')(_gen_sudo)
    _reg += 1

    async def _gen_suggest_next(arguments: dict, tool_name: str, _cmd='suggest_next') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_suggest_next')(_gen_suggest_next)
    _reg += 1

    async def _gen_suid_check(arguments: dict, tool_name: str, _cmd='suid_check') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_suid_check')(_gen_suid_check)
    _reg += 1

    async def _gen_surface(arguments: dict, tool_name: str, _cmd='surface') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_surface')(_gen_surface)
    _reg += 1

    async def _gen_swaks(arguments: dict, tool_name: str, _cmd='swaks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_swaks')(_gen_swaks)
    _reg += 1

    async def _gen_sys(arguments: dict, tool_name: str, _cmd='sys') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_sys')(_gen_sys)
    _reg += 1

    async def _gen_tab(arguments: dict, tool_name: str, _cmd='tab') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tab')(_gen_tab)
    _reg += 1

    async def _gen_targetedKerberoas(arguments: dict, tool_name: str, _cmd='targetedKerberoas') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_targetedKerberoas')(_gen_targetedKerberoas)
    _reg += 1

    async def _gen_tasks(arguments: dict, tool_name: str, _cmd='tasks') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tasks')(_gen_tasks)
    _reg += 1

    async def _gen_tcpdump_capture(arguments: dict, tool_name: str, _cmd='tcpdump_capture') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tcpdump_capture')(_gen_tcpdump_capture)
    _reg += 1

    async def _gen_tcpdump_icmp(arguments: dict, tool_name: str, _cmd='tcpdump_icmp') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tcpdump_icmp')(_gen_tcpdump_icmp)
    _reg += 1

    async def _gen_team_chat(arguments: dict, tool_name: str, _cmd='team_chat') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_team_chat')(_gen_team_chat)
    _reg += 1

    async def _gen_team_status(arguments: dict, tool_name: str, _cmd='team_status') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_team_status')(_gen_team_status)
    _reg += 1

    async def _gen_template_helper_serializer(arguments: dict, tool_name: str, _cmd='template_helper_serializer') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_template_helper_serializer')(_gen_template_helper_serializer)
    _reg += 1

    async def _gen_tenant(arguments: dict, tool_name: str, _cmd='tenant') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tenant')(_gen_tenant)
    _reg += 1

    async def _gen_tgrep(arguments: dict, tool_name: str, _cmd='tgrep') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tgrep')(_gen_tgrep)
    _reg += 1

    async def _gen_ticketer(arguments: dict, tool_name: str, _cmd='ticketer') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ticketer')(_gen_ticketer)
    _reg += 1

    async def _gen_timeline_browser(arguments: dict, tool_name: str, _cmd='timeline_browser') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_timeline_browser')(_gen_timeline_browser)
    _reg += 1

    async def _gen_toast_clear(arguments: dict, tool_name: str, _cmd='toast_clear') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_toast_clear')(_gen_toast_clear)
    _reg += 1

    async def _gen_toctoc(arguments: dict, tool_name: str, _cmd='toctoc') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_toctoc')(_gen_toctoc)
    _reg += 1

    async def _gen_tord(arguments: dict, tool_name: str, _cmd='tord') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tord')(_gen_tord)
    _reg += 1

    async def _gen_trace(arguments: dict, tool_name: str, _cmd='trace') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_trace')(_gen_trace)
    _reg += 1

    async def _gen_transform(arguments: dict, tool_name: str, _cmd='transform') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_transform')(_gen_transform)
    _reg += 1

    async def _gen_trufflehog(arguments: dict, tool_name: str, _cmd='trufflehog') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_trufflehog')(_gen_trufflehog)
    _reg += 1

    async def _gen_tshark_analyze(arguments: dict, tool_name: str, _cmd='tshark_analyze') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tshark_analyze')(_gen_tshark_analyze)
    _reg += 1

    async def _gen_ttp_matrix(arguments: dict, tool_name: str, _cmd='ttp_matrix') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ttp_matrix')(_gen_ttp_matrix)
    _reg += 1

    async def _gen_ttp_rebuild(arguments: dict, tool_name: str, _cmd='ttp_rebuild') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ttp_rebuild')(_gen_ttp_rebuild)
    _reg += 1

    async def _gen_ttp_show(arguments: dict, tool_name: str, _cmd='ttp_show') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_ttp_show')(_gen_ttp_show)
    _reg += 1

    async def _gen_tui_theme(arguments: dict, tool_name: str, _cmd='tui_theme') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_tui_theme')(_gen_tui_theme)
    _reg += 1

    async def _gen_unicode_WAFbypass(arguments: dict, tool_name: str, _cmd='unicode_WAFbypass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_unicode_WAFbypass')(_gen_unicode_WAFbypass)
    _reg += 1

    async def _gen_unlock_target(arguments: dict, tool_name: str, _cmd='unlock_target') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_unlock_target')(_gen_unlock_target)
    _reg += 1

    async def _gen_unseal_credentials(arguments: dict, tool_name: str, _cmd='unseal_credentials') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_unseal_credentials')(_gen_unseal_credentials)
    _reg += 1

    async def _gen_unzip(arguments: dict, tool_name: str, _cmd='unzip') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_unzip')(_gen_unzip)
    _reg += 1

    async def _gen_upload_bypass(arguments: dict, tool_name: str, _cmd='upload_bypass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_upload_bypass')(_gen_upload_bypass)
    _reg += 1

    async def _gen_upload_c2(arguments: dict, tool_name: str, _cmd='upload_c2') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_upload_c2')(_gen_upload_c2)
    _reg += 1

    async def _gen_upload_gofile(arguments: dict, tool_name: str, _cmd='upload_gofile') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_upload_gofile')(_gen_upload_gofile)
    _reg += 1

    async def _gen_urldecode(arguments: dict, tool_name: str, _cmd='urldecode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_urldecode')(_gen_urldecode)
    _reg += 1

    async def _gen_urlencode(arguments: dict, tool_name: str, _cmd='urlencode') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_urlencode')(_gen_urlencode)
    _reg += 1

    async def _gen_use(arguments: dict, tool_name: str, _cmd='use') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_use')(_gen_use)
    _reg += 1

    async def _gen_username_anarchy(arguments: dict, tool_name: str, _cmd='username_anarchy') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_username_anarchy')(_gen_username_anarchy)
    _reg += 1

    async def _gen_utf(arguments: dict, tool_name: str, _cmd='utf') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_utf')(_gen_utf)
    _reg += 1

    async def _gen_v(arguments: dict, tool_name: str, _cmd='v') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_v')(_gen_v)
    _reg += 1

    async def _gen_veil(arguments: dict, tool_name: str, _cmd='veil') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_veil')(_gen_veil)
    _reg += 1

    async def _gen_vpn(arguments: dict, tool_name: str, _cmd='vpn') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_vpn')(_gen_vpn)
    _reg += 1

    async def _gen_vscan(arguments: dict, tool_name: str, _cmd='vscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_vscan')(_gen_vscan)
    _reg += 1

    async def _gen_vuln_list(arguments: dict, tool_name: str, _cmd='vuln_list') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_vuln_list')(_gen_vuln_list)
    _reg += 1

    async def _gen_vulns(arguments: dict, tool_name: str, _cmd='vulns') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_vulns')(_gen_vulns)
    _reg += 1

    async def _gen_waybackmachine(arguments: dict, tool_name: str, _cmd='waybackmachine') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_waybackmachine')(_gen_waybackmachine)
    _reg += 1

    async def _gen_weevely(arguments: dict, tool_name: str, _cmd='weevely') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_weevely')(_gen_weevely)
    _reg += 1

    async def _gen_weevelygen(arguments: dict, tool_name: str, _cmd='weevelygen') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_weevelygen')(_gen_weevelygen)
    _reg += 1

    async def _gen_wfuzz(arguments: dict, tool_name: str, _cmd='wfuzz') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wfuzz')(_gen_wfuzz)
    _reg += 1

    async def _gen_whatweb(arguments: dict, tool_name: str, _cmd='whatweb') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_whatweb')(_gen_whatweb)
    _reg += 1

    async def _gen_whoami(arguments: dict, tool_name: str, _cmd='whoami') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_whoami')(_gen_whoami)
    _reg += 1

    async def _gen_wifipass(arguments: dict, tool_name: str, _cmd='wifipass') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wifipass')(_gen_wifipass)
    _reg += 1

    async def _gen_winbase64payload(arguments: dict, tool_name: str, _cmd='winbase64payload') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_winbase64payload')(_gen_winbase64payload)
    _reg += 1

    async def _gen_windapsearch(arguments: dict, tool_name: str, _cmd='windapsearch') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_windapsearch')(_gen_windapsearch)
    _reg += 1

    async def _gen_windapsearchscrapeusers(arguments: dict, tool_name: str, _cmd='windapsearchscrapeusers') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_windapsearchscrapeusers')(_gen_windapsearchscrapeusers)
    _reg += 1

    async def _gen_winpeas(arguments: dict, tool_name: str, _cmd='winpeas') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_winpeas')(_gen_winpeas)
    _reg += 1

    async def _gen_wipe_free(arguments: dict, tool_name: str, _cmd='wipe_free') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wipe_free')(_gen_wipe_free)
    _reg += 1

    async def _gen_wipe_logs(arguments: dict, tool_name: str, _cmd='wipe_logs') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wipe_logs')(_gen_wipe_logs)
    _reg += 1

    async def _gen_wipe_timeline(arguments: dict, tool_name: str, _cmd='wipe_timeline') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wipe_timeline')(_gen_wipe_timeline)
    _reg += 1

    async def _gen_wizard(arguments: dict, tool_name: str, _cmd='wizard') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wizard')(_gen_wizard)
    _reg += 1

    async def _gen_wmi_lateral(arguments: dict, tool_name: str, _cmd='wmi_lateral') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wmi_lateral')(_gen_wmi_lateral)
    _reg += 1

    async def _gen_wmi_persist(arguments: dict, tool_name: str, _cmd='wmi_persist') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wmi_persist')(_gen_wmi_persist)
    _reg += 1

    async def _gen_wmi_scheduled_task(arguments: dict, tool_name: str, _cmd='wmi_scheduled_task') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wmi_scheduled_task')(_gen_wmi_scheduled_task)
    _reg += 1

    async def _gen_wmiexec(arguments: dict, tool_name: str, _cmd='wmiexec') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wmiexec')(_gen_wmiexec)
    _reg += 1

    async def _gen_wmiexecpro(arguments: dict, tool_name: str, _cmd='wmiexecpro') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wmiexecpro')(_gen_wmiexecpro)
    _reg += 1

    async def _gen_wpscan(arguments: dict, tool_name: str, _cmd='wpscan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wpscan')(_gen_wpscan)
    _reg += 1

    async def _gen_wrapper(arguments: dict, tool_name: str, _cmd='wrapper') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_wrapper')(_gen_wrapper)
    _reg += 1

    async def _gen_www(arguments: dict, tool_name: str, _cmd='www') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_www')(_gen_www)
    _reg += 1

    async def _gen_xss(arguments: dict, tool_name: str, _cmd='xss') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_xss')(_gen_xss)
    _reg += 1

    async def _gen_xsstrike(arguments: dict, tool_name: str, _cmd='xsstrike') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_xsstrike')(_gen_xsstrike)
    _reg += 1

    async def _gen_yara_scan(arguments: dict, tool_name: str, _cmd='yara_scan') -> list:
        cmd = arguments.get("args", "")
        output = run_lazyown_cmd_fn(f"{_cmd} {cmd}".strip())
        return make_text_fn(tool_name, output)

    register_handler_fn('lazyown_yara_scan')(_gen_yara_scan)
    _reg += 1

    return _reg
