# API (page 3 of 23)
Previous: [API_p2.md](API_p2.md)

## cli/commands/orchestration.py
Depends on: `cli/commands/_base.py`, `cli/reasoning_stream.py`, `core/console.py`
Imported by: `tests/test_improvements_spec.py`
- `run_with_spinner` (function) `cli/commands/orchestration.py:94` `def run_with_spinner(execute)` -- Run a blocking orchestrator call with a live reasoning spinner.
- `OrchestrationCommandSet.do_status_bar` (method) `cli/commands/orchestration.py:190` `def do_status_bar(self, args)` -- Inspect, toggle and refresh the prompt status bar.
- `OrchestrationCommandSet.do_orchestrate` (method) `cli/commands/orchestration.py:216` `def do_orchestrate(self, args)` -- Route a goal through the unified orchestrator and print the result.

## cli/commands/payload_arsenal.py
Depends on: `cli/commands/_base.py`, `modules/dotnet_payload.py`, `modules/linux_advanced_payloads.py`, `modules/macos_payloads.py`, `modules/polymorphic_engine.py`, `modules/staged_delivery.py`
- `PayloadArsenalCommandSet.do_dotnet_payload` (method) `cli/commands/payload_arsenal.py:29` `def do_dotnet_payload(self, line)` -- Generate a .NET/C# payload.
- `PayloadArsenalCommandSet.do_arsenal_show` (method) `cli/commands/payload_arsenal.py:114` `def do_arsenal_show(self, line)` -- Show payload arsenal items.
- `PayloadArsenalCommandSet.do_staged_delivery` (method) `cli/commands/payload_arsenal.py:172` `def do_staged_delivery(self, line)` -- Generate staged delivery artifacts (HTA, VBA, LNK, ISO, VHD).
- `PayloadArsenalCommandSet.do_polymorphic` (method) `cli/commands/payload_arsenal.py:261` `def do_polymorphic(self, line)` -- Apply polymorphic mutation to shellcode.
- `PayloadArsenalCommandSet.do_macos_payload` (method) `cli/commands/payload_arsenal.py:328` `def do_macos_payload(self, line)` -- Generate macOS payloads (.app bundles, persistence, TCC bypass).
- `PayloadArsenalCommandSet.do_linux_advanced_payload` (method) `cli/commands/payload_arsenal.py:401` `def do_linux_advanced_payload(self, line)` -- Generate advanced Linux payloads (LD_PRELOAD, eBPF, PAM, kernel module).

## cli/commands/payload_generation.py
Depends on: `cli/commands/_base.py`, `modules/payload_factory.py`, `utils.py`
- `PayloadCommandSet.do_generate` (method) `cli/commands/payload_generation.py:37` `def do_generate(self, line)` -- Generate a payload.

## cli/commands/persist.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PersistenceCommandSet.do_createwebshell` (method) `cli/commands/persist.py:33` `def do_createwebshell(self, line)` -- Create web shells (JPG-disguised PHP, p0wny-shell, ASP).
- `PersistenceCommandSet.do_createrevshell` (method) `cli/commands/persist.py:47` `def do_createrevshell(self, line)` -- Create a bash reverse shell script in sessions/.
- `PersistenceCommandSet.do_createwinrevshell` (method) `cli/commands/persist.py:61` `def do_createwinrevshell(self, line)` -- Create a Windows reverse shell (PowerShell).
- `PersistenceCommandSet.do_conptyshell` (method) `cli/commands/persist.py:73` `def do_conptyshell(self, line)` -- Download ConPtyShell and prepare a PowerShell run command.
- `PersistenceCommandSet.do_pwncatcs` (method) `cli/commands/persist.py:89` `def do_pwncatcs(self, line)` -- Start a pwncat-cs reverse shell listener.
- `PersistenceCommandSet.do_revwin` (method) `cli/commands/persist.py:99` `def do_revwin(self, line)` -- Create a Windows reverse shell executable.
- `PersistenceCommandSet.do_wmi_persist` (method) `cli/commands/persist.py:112` `def do_wmi_persist(self, line)` -- Create WMI Event Subscription persistence (fileless, no disk write).
- `PersistenceCommandSet.do_wmi_lateral` (method) `cli/commands/persist.py:170` `def do_wmi_lateral(self, line)` -- Execute a command on a remote host via WMI.
- `PersistenceCommandSet.do_wmi_scheduled_task` (method) `cli/commands/persist.py:209` `def do_wmi_scheduled_task(self, line)` -- Create a scheduled task for persistence via WMI.

## cli/commands/persist_migrated.py
Depends on: `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/hardening.py`, `modules/traffic_morpher.py`, `utils.py`
Imported by: `tests/test_backdoor_random.py`
- `PersistMigratedCommandSet.generate_backdoor_username` (method) `cli/commands/persist_migrated.py:37` `def generate_backdoor_username()` -- Generate a random backdoor username (same shape as C2 operators).
- `PersistMigratedCommandSet.generate_backdoor_password` (method) `cli/commands/persist_migrated.py:43` `def generate_backdoor_password()` -- Generate a random backdoor password safe for assign, chpasswd and CLIs.
- `PersistMigratedCommandSet.resolve_backdoor_creds` (method) `cli/commands/persist_migrated.py:53` `def resolve_backdoor_creds(params)` -- Return configured creds, or fresh random ones when unset.
- `PersistMigratedCommandSet.do_pwncat` (method) `cli/commands/persist_migrated.py:91` `def do_pwncat(self, line)` -- Runs `pwncat` with the specified port for listening.
- `PersistMigratedCommandSet.do_ftp` (method) `cli/commands/persist_migrated.py:135` `def do_ftp(self, line)` -- Connects to an ftp host using credentials from a file and a specified port.
- `PersistMigratedCommandSet.do_rdp` (method) `cli/commands/persist_migrated.py:194` `def do_rdp(self, line)` -- Reads credentials from a file, encrypts the password, and executes the RDP connection command.
- `PersistMigratedCommandSet.do_grisun0` (method) `cli/commands/persist_migrated.py:268` `def do_grisun0(self, line)` -- Creates and copies a shell command to add a new user, assign a password, add the user to the sudo group, and switch...
- `PersistMigratedCommandSet.do_grisun0w` (method) `cli/commands/persist_migrated.py:312` `def do_grisun0w(self, line)` -- Creates and copies a PowerShell command to add a new user, assign a password, add the user to the Administrators...
- `PersistMigratedCommandSet.do_asprevbase64` (method) `cli/commands/persist_migrated.py:354` `def do_asprevbase64(self, line)` -- Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard.
- `PersistMigratedCommandSet.do_weevelygen` (method) `cli/commands/persist_migrated.py:392` `def do_weevelygen(self, line)` -- Generate a PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_weevely` (method) `cli/commands/persist_migrated.py:432` `def do_weevely(self, line)` -- Connect to PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_backdoor_factory` (method) `cli/commands/persist_migrated.py:478` `def do_backdoor_factory(self, line)` -- Creates a backdoored executable using `backdoor-factory`.
- `PersistMigratedCommandSet.do_msfpc` (method) `cli/commands/persist_migrated.py:524` `def do_msfpc(self, line)` -- Generates payloads using MSFvenom Payload Creator (MSFPC).
- `PersistMigratedCommandSet.do_ivy` (method) `cli/commands/persist_migrated.py:605` `def do_ivy(self, line)` -- Generates payloads using Ivy with various options.
- `PersistMigratedCommandSet.do_veil` (method) `cli/commands/persist_migrated.py:705` `def do_veil(self, line)` -- Generates payloads using Veil-Evasion with various options.
- `PersistMigratedCommandSet.do_scarecrow` (method) `cli/commands/persist_migrated.py:779` `def do_scarecrow(self, line)` -- Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode. to create the...
- `PersistMigratedCommandSet.do_generate_revshell` (method) `cli/commands/persist_migrated.py:897` `def do_generate_revshell(self, line)` -- Generate a reverse shell in various programming languages.
- `PersistMigratedCommandSet.do_dr0p1t` (method) `cli/commands/persist_migrated.py:963` `def do_dr0p1t(self, line)` -- Execute the Dr0p1t tool to create a stealthy malware dropper.
- `PersistMigratedCommandSet.do_paranoid_meterpreter` (method) `cli/commands/persist_migrated.py:1026` `def do_paranoid_meterpreter(self, line)` -- Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracking.
- `PersistMigratedCommandSet.do_setoolKits` (method) `cli/commands/persist_migrated.py:1114` `def do_setoolKits(self, line)` -- Executes the SEToolKit workflow to generate a Meterpreter payload and configure the multi-handler using LHOST and...
- `PersistMigratedCommandSet.do_darkarmour` (method) `cli/commands/persist_migrated.py:1147` `def do_darkarmour(self, line)` -- Uses the darkarmour tool to generate an undetectable version of a PE executable.
- `PersistMigratedCommandSet.do_knokknok` (method) `cli/commands/persist_migrated.py:1215` `def do_knokknok(self, line)` -- Send special string to trigger a reverse shell, with the command 'c2 client_name' create a listener shell script to...
- `PersistMigratedCommandSet.do_listener_go` (method) `cli/commands/persist_migrated.py:1250` `def do_listener_go(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_listener_py` (method) `cli/commands/persist_migrated.py:1317` `def do_listener_py(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_service` (method) `cli/commands/persist_migrated.py:1384` `def do_service(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PersistMigratedCommandSet.do_toctoc` (method) `cli/commands/persist_migrated.py:1457` `def do_toctoc(self, line)` -- Sends a magic packet to the Chinese malware.
- `PersistMigratedCommandSet.do_beaconcfg` (method) `cli/commands/persist_migrated.py:1480` `def do_beaconcfg(self, line)` -- Generate a C2 beacon profile with traffic morphing and domain fronting.

## cli/commands/phishing_wizard.py
Depends on: `cli/commands/_base.py`, `modules/backdoor/server.c`, `modules/phishing_orchestrator.py`, `utils.py`
- `PhishingWizardCommandSet.do_phish_wizard` (method) `cli/commands/phishing_wizard.py:190` `def do_phish_wizard(self, line)` -- Interactive end-to-end phishing campaign wizard.
- `PhishingWizardCommandSet.do_phish_serve` (method) `cli/commands/phishing_wizard.py:361` `def do_phish_serve(self, line)` -- Start a lightweight HTTP server for phishing landing pages.
- `PhishingHandler.log_message` (method) `cli/commands/phishing_wizard.py:389` `def log_message(self, format)`
- `PhishingHandler.do_GET` (method) `cli/commands/phishing_wizard.py:392` `def do_GET(self)`
- `PhishingHandler.do_POST` (method) `cli/commands/phishing_wizard.py:407` `def do_POST(self)`
- `PhishingHandler.do_OPTIONS` (method) `cli/commands/phishing_wizard.py:427` `def do_OPTIONS(self)`
- `PhishingHandler.do_phish_report` (method) `cli/commands/phishing_wizard.py:443` `def do_phish_report(self, line)` -- Show campaign results and captured credentials.
- `do_phisher` (function) `cli/commands/phishing_wizard.py:637` `def do_phisher(self, line)` -- Launch a phishing campaign against a target domain.

## cli/commands/pivoting.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
- `PivotingCommandSet.do_autopivot` (method) `cli/commands/pivoting.py:44` `def do_autopivot(self, line)` -- Auto-detect internal networks and set up pivot tunnels.
- `PivotingCommandSet.do_pivot_status` (method) `cli/commands/pivoting.py:118` `def do_pivot_status(self, line)` -- Show the current pivot chain state.
- `PivotingCommandSet.do_pivot_kill` (method) `cli/commands/pivoting.py:137` `def do_pivot_kill(self, line)` -- Kill all pivot tunnels and clean up.
- `PivotingCommandSet.do_pivot_scan` (method) `cli/commands/pivoting.py:171` `def do_pivot_scan(self, line)` -- Scan internal networks through the current pivot chain.
- `PivotingCommandSet.do_pivot_proxy` (method) `cli/commands/pivoting.py:224` `def do_pivot_proxy(self, line)` -- Start a local SOCKS proxy through the pivot chain.

## cli/commands/postexp.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PostExploitationCommandSet.do_lazywebshell` (method) `cli/commands/postexp.py:32` `def do_lazywebshell(self, line)` -- Run LazyOwn webshell server on port 8888.
- `PostExploitationCommandSet.do_disableav` (method) `cli/commands/postexp.py:45` `def do_disableav(self, line)` -- Create a VBS script to attempt disabling Windows Defender.
- `PostExploitationCommandSet.do_mimikatzpy` (method) `cli/commands/postexp.py:59` `def do_mimikatzpy(self, line)` -- Run Mimikatz over Python (impacket style).
- `PostExploitationCommandSet.do_scavenger` (method) `cli/commands/postexp.py:64` `def do_scavenger(self, line)` -- Run the Scavenger post-exploitation data collector.
- `PostExploitationCommandSet.do_follina` (method) `cli/commands/postexp.py:69` `def do_follina(self, line)` -- Run the Follina (CVE-2022-30190) exploit setup.
- `PostExploitationCommandSet.do_shellcode` (method) `cli/commands/postexp.py:74` `def do_shellcode(self, line)` -- Generate and manage shellcode.
- `PostExploitationCommandSet.do_ofuscatorps1` (method) `cli/commands/postexp.py:82` `def do_ofuscatorps1(self, line)` -- Obfuscate a PowerShell script.
- `PostExploitationCommandSet.do_atomic_lazyown` (method) `cli/commands/postexp.py:87` `def do_atomic_lazyown(self, line)` -- Execute atomic red-team tests via LazyOwn.

## cli/commands/postexp_migrated.py
Depends on: `cli/commands/_base.py`, `modules/yara_scanner.py`, `utils.py`
- `PostexpMigratedCommandSet.do_find` (method) `cli/commands/postexp_migrated.py:37` `def do_find(self, line)` -- Automates command execution based on a list of aliases and commands.
- `PostexpMigratedCommandSet.do_cports` (method) `cli/commands/postexp_migrated.py:533` `def do_cports(self, line)` -- Generates a command to display TCP and UDP ports and copies it to the clipboard.
- `PostexpMigratedCommandSet.do_rubeus` (method) `cli/commands/postexp_migrated.py:578` `def do_rubeus(self, line)` -- Copies a command to the clipboard for downloading and running Rubeus.
- `PostexpMigratedCommandSet.do_sessionsshstrace` (method) `cli/commands/postexp_migrated.py:618` `def do_sessionsshstrace(self, line)` -- Attach strace to a running process and log output to a file.
- `PostexpMigratedCommandSet.do_powershell_cmd_stager` (method) `cli/commands/postexp_migrated.py:669` `def do_powershell_cmd_stager(self, line)` -- Generate and execute a PowerShell command stager to run a .ps1 script.
- `PostexpMigratedCommandSet.do_shellcode_search` (method) `cli/commands/postexp_migrated.py:706` `def do_shellcode_search(self, line)` -- Search the shell-storm API for shellcodes using the provided keywords.
- `PostexpMigratedCommandSet.do_shellcode2sylk` (method) `cli/commands/postexp_migrated.py:754` `def do_shellcode2sylk(self, line)` -- Converts shellcode to SYLK format and saves the result to a file.
- `PostexpMigratedCommandSet.do_pezorsh` (method) `cli/commands/postexp_migrated.py:799` `def do_pezorsh(self, line)` -- Executes the PEzor tool to pack executables or shellcode with custom configurations.
- `PostexpMigratedCommandSet.do_pip_repo` (method) `cli/commands/postexp_migrated.py:872` `def do_pip_repo(self, line)` -- Sets up a local pip repository to serve Python packages for installation on a compromised machine without internet...
- `PostexpMigratedCommandSet.do_apt_repo` (method) `cli/commands/postexp_migrated.py:984` `def do_apt_repo(self, line)` -- Creates a comprehensive local APT repository with enhanced dependency resolution.
- `resolve_and_download_dependencies` (function) `cli/commands/postexp_migrated.py:1030` `def resolve_and_download_dependencies(package_name)` -- Recursively resolve and download package dependencies with enhanced checks
- `PostexpMigratedCommandSet.do_createpayload` (method) `cli/commands/postexp_migrated.py:1233` `def do_createpayload(self, line)` -- Generates an obfuscated payload to evade AV detection using the payloadGenerator tool. thanks to smokeme
- `PostexpMigratedCommandSet.do_bin2shellcode` (method) `cli/commands/postexp_migrated.py:1285` `def do_bin2shellcode(self, line)` -- Converts a binary file to a shellcode string in C or Nim format.
- `PostexpMigratedCommandSet.do_exe2bin` (method) `cli/commands/postexp_migrated.py:1375` `def do_exe2bin(self, line)` -- Trasnform file .exe into binary file.
- `PostexpMigratedCommandSet.do_exe2donutbin` (method) `cli/commands/postexp_migrated.py:1402` `def do_exe2donutbin(self, line)` -- Trasnform file .exe into donut binary file.
- `PostexpMigratedCommandSet.do_issue_command_to_c2` (method) `cli/commands/postexp_migrated.py:1426` `def do_issue_command_to_c2(self, line)` -- Exec command in the client using the C2. download: command you must put the file in sessions/temp_upload or use...
- `PostexpMigratedCommandSet.do_d3monizedshell` (method) `cli/commands/postexp_migrated.py:1450` `def do_d3monizedshell(self, line)` -- Executes the D3m0n1z3dShell tool for persistence in Linux.
- `PostexpMigratedCommandSet.do_scp` (method) `cli/commands/postexp_migrated.py:1483` `def do_scp(self, line)` -- Copies the local "sessions" directory to a remote host using scp, leveraging sshpass for automated authentication.
- `PostexpMigratedCommandSet.do_apt_proxy` (method) `cli/commands/postexp_migrated.py:1579` `def do_apt_proxy(self, line)` -- Configures the local machine with internet access to act as an APT proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_pip_proxy` (method) `cli/commands/postexp_migrated.py:1635` `def do_pip_proxy(self, line)` -- Configures the local machine with internet access to act as a pip proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_internet_proxy` (method) `cli/commands/postexp_migrated.py:1693` `def do_internet_proxy(self, line)` -- Configures the local machine with internet access to act as a proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_shellcode2elf` (method) `cli/commands/postexp_migrated.py:1755` `def do_shellcode2elf(self, line)` -- Convert shellcode into an ELF file and infect it.
- `PostexpMigratedCommandSet.do_ssh_cmd` (method) `cli/commands/postexp_migrated.py:1837` `def do_ssh_cmd(self, line)` -- Perform Remote Execution Command through SSH using configured start_user.
- `PostexpMigratedCommandSet.do_service_ssh` (method) `cli/commands/postexp_migrated.py:1866` `def do_service_ssh(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PostexpMigratedCommandSet.do_ofuscatesh` (method) `cli/commands/postexp_migrated.py:1940` `def do_ofuscatesh(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_ofuscate_payload` (method) `cli/commands/postexp_migrated.py:1970` `def do_ofuscate_payload(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_adversary` (method) `cli/commands/postexp_migrated.py:1997` `def do_adversary(self, line)` -- LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in adversary.json
- `PostexpMigratedCommandSet.do_ofuscate_string` (method) `cli/commands/postexp_migrated.py:2145` `def do_ofuscate_string(self, line)` -- Ofuscate a string into Go code.
- `PostexpMigratedCommandSet.do_path2hex` (method) `cli/commands/postexp_migrated.py:2187` `def do_path2hex(self, line)` -- Convert a binary path to x64 little-endian hex code for shellcode injection.
- `PostexpMigratedCommandSet.do_hex2shellcode` (method) `cli/commands/postexp_migrated.py:2234` `def do_hex2shellcode(self, line)` -- Convert raw hex payload from msfvenom into NASM-compatible shellcode format.
- `PostexpMigratedCommandSet.do_create_synthetic` (method) `cli/commands/postexp_migrated.py:2291` `def do_create_synthetic(self, line)` -- Create a basic synthetic playbook from Nmap CSV when LLM fails.
- `PostexpMigratedCommandSet.do_extract_yaml` (method) `cli/commands/postexp_migrated.py:2343` `def do_extract_yaml(self, line)` -- Extract YAML from an existing debug file and try to create a playbook.
- `PostexpMigratedCommandSet.do_convert_remcomsvc_from_file` (method) `cli/commands/postexp_migrated.py:2405` `def do_convert_remcomsvc_from_file(self, arg)` -- Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice format, prints a sample, and saves...
- `PostexpMigratedCommandSet.do_adversary_yaml` (method) `cli/commands/postexp_migrated.py:2439` `def do_adversary_yaml(self, line)` -- Execute adversary from YAML in lazyadversaries/*.yaml Syntax: adversary [id] [l|r|n]
- `PostexpMigratedCommandSet.do_add2find` (method) `cli/commands/postexp_migrated.py:2524` `def do_add2find(self, line)` -- Add a new custom command to the 'find' system, saved in user_commands.json.
- `PostexpMigratedCommandSet.do_rmfromfind` (method) `cli/commands/postexp_migrated.py:2552` `def do_rmfromfind(self, line)` -- Remove a custom command by index (as shown in 'find').
- `PostexpMigratedCommandSet.do_aes_pe` (method) `cli/commands/postexp_migrated.py:2581` `def do_aes_pe(self, line)` -- Encrypt with AES and random key to PE EXE file, to usage with loaders.
- `PostexpMigratedCommandSet.do_yara_scan` (method) `cli/commands/postexp_migrated.py:2610` `def do_yara_scan(self, line)` -- Scan files or directories with YARA rules for malware/IOCs.

## cli/commands/privilege_escalation.py
Depends on: `cli/commands/_base.py`, `utils.py`
Imported by: `tests/test_shell_semantics.py`
- `PrivilegeEscalationCommandSet.do_smbserver` (method) `cli/commands/privilege_escalation.py:139` `def do_smbserver(self, line)` -- Stand up an Impacket SMB server with three relay variants.
- `PrivilegeEscalationCommandSet.do_responder` (method) `cli/commands/privilege_escalation.py:197` `def do_responder(self, line)` -- Run Responder on the configured ``device`` with elevated privileges.
- `PrivilegeEscalationCommandSet.do_sudo` (method) `cli/commands/privilege_escalation.py:222` `def do_sudo(self, line)` -- Re-launch the framework with root privileges when missing.
- `PrivilegeEscalationCommandSet.do_linpeas` (method) `cli/commands/privilege_escalation.py:235` `def do_linpeas(self, line)` -- Serve ``linpeas.sh`` over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_winpeas` (method) `cli/commands/privilege_escalation.py:271` `def do_winpeas(self, line)` -- Serve a winPEAS variant over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_les` (method) `cli/commands/privilege_escalation.py:310` `def do_les(self, line)` -- Run Linux Exploit Suggester against a kernel version.
- `PrivilegeEscalationCommandSet.do_suid_check` (method) `cli/commands/privilege_escalation.py:350` `def do_suid_check(self, line)` -- Print SUID/SGID enumeration commands ready to paste on the target.
- `PrivilegeEscalationCommandSet.do_pspy` (method) `cli/commands/privilege_escalation.py:369` `def do_pspy(self, line)` -- Serve the ``pspy`` process monitor over HTTP.
- `PrivilegeEscalationCommandSet.do_gtfo` (method) `cli/commands/privilege_escalation.py:403` `def do_gtfo(self, line)` -- Look up a binary in GTFOBins and LOLBas parquet knowledge bases.
- `PrivilegeEscalationCommandSet.do_whoami_priv` (method) `cli/commands/privilege_escalation.py:450` `def do_whoami_priv(self, line)` -- Print privilege enumeration commands for the target OS.
- `PrivilegeEscalationCommandSet.do_sudo_privesc` (method) `cli/commands/privilege_escalation.py:512` `def do_sudo_privesc(self, line)` -- Analyse sudo -l output and cross-reference with GTFOBins.
- `PrivilegeEscalationCommandSet.do_printspoofer` (method) `cli/commands/privilege_escalation.py:610` `def do_printspoofer(self, line)` -- Serve PrintSpoofer over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_juicypotato` (method) `cli/commands/privilege_escalation.py:632` `def do_juicypotato(self, line)` -- Serve JuicyPotato over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_privesc_cmd_by_os` (method) `cli/commands/privilege_escalation.py:754` `def do_privesc_cmd_by_os(self, line)` -- Prepare and send a linpeas/winpeas command to a C2 client.

## cli/commands/purple_team.py
Depends on: `cli/commands/_base.py`, `cli/purple_tui.py`, `core/config.py`, `modules/auto_purple.py`
- `PurpleTeamCommandSet.do_purple_exec` (method) `cli/commands/purple_team.py:144` `def do_purple_exec(self, line)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamCommandSet.do_purple_test` (method) `cli/commands/purple_team.py:203` `def do_purple_test(self, args)` -- Test if LazyOwnBT would detect a command (no execution).
- `PurpleTeamCommandSet.do_purple_score` (method) `cli/commands/purple_team.py:223` `def do_purple_score(self, line)` -- Show current engagement detection score.
- `PurpleTeamCommandSet.do_purple_report` (method) `cli/commands/purple_team.py:271` `def do_purple_report(self, line)` -- Generate full engagement report with datasets.
- `PurpleTeamCommandSet.do_purple_methods` (method) `cli/commands/purple_team.py:285` `def do_purple_methods(self, line)` -- List available LazyOwnBT detection methods.
- `PurpleTeamCommandSet.do_purple_config` (method) `cli/commands/purple_team.py:297` `def do_purple_config(self, args)` -- Show or update purple team configuration (payload.json).
- `PurpleTeamCommandSet.do_purple_dashboard` (method) `cli/commands/purple_team.py:350` `def do_purple_dashboard(self, line)` -- Launch the Purple Team TUI dashboard.
- `PurpleTeamCommandSet.do_purple_history` (method) `cli/commands/purple_team.py:367` `def do_purple_history(self, args)` -- Show recent purple team action results.

## cli/commands/pwn.py
Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `core/validators.py`, `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `modules/dashboard_engine.py`, `modules/enrich.py`, `modules/exploit_recommender.py`, `modules/rich_tui.py`, `modules/world_model.py`, `utils.py`
Imported by: `contrib/legacy/lazybinenc.py`, `contrib/legacy/lazypwn.py`, `contrib/legacy/lazyvsftp.py`, `contrib/legacy/sql.py`
- `PwnCommandSet.do_auto_pwn` (method) `cli/commands/pwn.py:35` `def do_auto_pwn(self, line)` -- Run the full autonomous exploitation chain against the target.
- `PwnCommandSet.do_rich_tui` (method) `cli/commands/pwn.py:109` `def do_rich_tui(self, line)` -- Launch the Rich-based live dashboard TUI.
- `PwnCommandSet.do_exploit_chain` (method) `cli/commands/pwn.py:158` `def do_exploit_chain(self, line)` -- AI-driven multi-step exploit chaining with fallback strategies.
- `PwnCommandSet.do_lolbas_list` (method) `cli/commands/pwn.py:245` `def do_lolbas_list(self, line)` -- List available LOLBAS (Living Off The Land) techniques from plugins.
- `PwnCommandSet.do_lolbas_use` (method) `cli/commands/pwn.py:302` `def do_lolbas_use(self, line)` -- Execute a specific LOLBAS technique.
- `PwnCommandSet.do_stealth_on` (method) `cli/commands/pwn.py:394` `def do_stealth_on(self, line)` -- Enable stealth mode for subsequent operations.
- `PwnCommandSet.do_stealth_off` (method) `cli/commands/pwn.py:422` `def do_stealth_off(self, line)` -- Disable stealth mode.

## cli/commands/recon.py
Depends on: `cli/commands/_base.py`, `cli/exploit_advisor.py`, `cli/lazynmap_post.py`, `core/console.py`, `modules/intelligence_engine.py`, `utils.py`
- `ReconCommandSet.do_batchnmap` (method) `cli/commands/recon.py:47` `def do_batchnmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.
- `ReconCommandSet.do_lazynmap` (method) `cli/commands/recon.py:74` `def do_lazynmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` with target mode.
- `ReconCommandSet.do_dig` (method) `cli/commands/recon.py:154` `def do_dig(self, line)` -- Executes the `dig` command to query DNS information.
- `ReconCommandSet.do_dnsenum` (method) `cli/commands/recon.py:186` `def do_dnsenum(self, line)` -- Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.
- `ReconCommandSet.do_dnsmap` (method) `cli/commands/recon.py:222` `def do_dnsmap(self, line)` -- Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.
- `ReconCommandSet.do_whatweb` (method) `cli/commands/recon.py:255` `def do_whatweb(self, line)` -- Performs a web technology fingerprinting scan using `whatweb`.
- `ReconCommandSet.do_nbtscan` (method) `cli/commands/recon.py:292` `def do_nbtscan(self, line)` -- Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.
- `ReconCommandSet.do_nikto` (method) `cli/commands/recon.py:320` `def do_nikto(self, line)` -- Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_finalrecon` (method) `cli/commands/recon.py:429` `def do_finalrecon(self, line)` -- Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_openssl_sclient` (method) `cli/commands/recon.py:461` `def do_openssl_sclient(self, line)` -- Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS...
- `ReconCommandSet.do_ss` (method) `cli/commands/recon.py:491` `def do_ss(self, line)` -- Search all exploit sources and map findings to the next LazyOwn command.
- `ReconCommandSet.do_wfuzz` (method) `cli/commands/recon.py:654` `def do_wfuzz(self, line)` -- Uses `wfuzz` to perform fuzzing based on provided parameters.

## cli/commands/recon_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/commands/_base.py`, `cli/surface_tui.py`, `core/config.py`, `utils.py`
- `ReconMigratedCommandSet.do_surface` (method) `cli/commands/recon_migrated.py:43` `def do_surface(self, line)` -- Render the network surface graph in the terminal.
- `ReconMigratedCommandSet.do_getcap` (method) `cli/commands/recon_migrated.py:97` `def do_getcap(self, line)` -- Retrieve and display file capabilities on the system.
- `ReconMigratedCommandSet.do_launchpad` (method) `cli/commands/recon_migrated.py:131` `def do_launchpad(self, line)` -- Searches for packages on Launchpad based on the provided search term and extracts codenames from the results.
- `ReconMigratedCommandSet.do_ping` (method) `cli/commands/recon_migrated.py:177` `def do_ping(self, line)` -- Perform a ping to check host availability and infer the operating system based on TTL values.
- `ReconMigratedCommandSet.do_gospider` (method) `cli/commands/recon_migrated.py:285` `def do_gospider(self, line)` -- Try gospider for web spidering.
- `ReconMigratedCommandSet.do_proxy` (method) `cli/commands/recon_migrated.py:373` `def do_proxy(self, line)` -- Runs a small proxy server to modify HTTP requests on the fly.
- `ReconMigratedCommandSet.do_ports` (method) `cli/commands/recon_migrated.py:411` `def do_ports(self, line)` -- Lists all open TCP and UDP ports on the local system.
- `ReconMigratedCommandSet.do_tcpdump_icmp` (method) `cli/commands/recon_migrated.py:453` `def do_tcpdump_icmp(self, line)` -- Starts `tcpdump` to capture ICMP traffic on the specified interface.
- `ReconMigratedCommandSet.do_tcpdump_capture` (method) `cli/commands/recon_migrated.py:486` `def do_tcpdump_capture(self, line)` -- Starts packet capture using `tcpdump` on the specified interface.
- `ReconMigratedCommandSet.do_tshark_analyze` (method) `cli/commands/recon_migrated.py:527` `def do_tshark_analyze(self, line)` -- Analyzes a packet capture file using `tshark` based on the provided remote host IP.
- `ReconMigratedCommandSet.do_waybackmachine` (method) `cli/commands/recon_migrated.py:593` `def do_waybackmachine(self, line)` -- Fetch URLs from the Wayback Machine for a given website.
- `ReconMigratedCommandSet.do_sslscan` (method) `cli/commands/recon_migrated.py:633` `def do_sslscan(self, line)` -- Run an SSL scan on the specified remote host.
- `ReconMigratedCommandSet.do_graudit` (method) `cli/commands/recon_migrated.py:674` `def do_graudit(self, line)` -- Executes the graudit command to perform a static code analysis with the specified options.
- `ReconMigratedCommandSet.do_sherlock` (method) `cli/commands/recon_migrated.py:705` `def do_sherlock(self, line)` -- Executes the Sherlock tool to find usernames across social networks.
- `ReconMigratedCommandSet.do_trufflehog` (method) `cli/commands/recon_migrated.py:746` `def do_trufflehog(self, line)` -- Executes trufflehog to search for secrets in a given Git repository URL.
- `ReconMigratedCommandSet.do_apache_users` (method) `cli/commands/recon_migrated.py:784` `def do_apache_users(self, line)` -- Performs enumeration of users from a target system using `apache-users`.
- `ReconMigratedCommandSet.do_trace` (method) `cli/commands/recon_migrated.py:831` `def do_trace(self, line)` -- Traces the DNS information for a given self.params['domain'] using the FreeDNS service.
- `ReconMigratedCommandSet.do_alterx` (method) `cli/commands/recon_migrated.py:874` `def do_alterx(self, line)` -- Executes the 'alterx' command for subdomain enumeration on the provided self.params['domain'].
- `ReconMigratedCommandSet.do_windapsearchscrapeusers` (method) `cli/commands/recon_migrated.py:951` `def do_windapsearchscrapeusers(self, line)` -- Extracts usernames from a JSON output generated by go-windapsearch and appends them to the file sessions/users.txt.
- `ReconMigratedCommandSet.do_cve` (method) `cli/commands/recon_migrated.py:987` `def do_cve(self, line)` -- Search for a CVE using the CIRCL API.
- `ReconMigratedCommandSet.do_serveralive2` (method) `cli/commands/recon_migrated.py:1036` `def do_serveralive2(self, line)` -- Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and retrieves the server bindings.
- `ReconMigratedCommandSet.do_binarycheck` (method) `cli/commands/recon_migrated.py:1070` `def do_binarycheck(self, line)` -- Performs various checks on a selected binary to gather information and protections.
- `ReconMigratedCommandSet.do_dnstool_py` (method) `cli/commands/recon_migrated.py:1115` `def do_dnstool_py(self, line)` -- Executes the dnstool.py tool to modify Active Directory-integrated DNS records.
- `ReconMigratedCommandSet.do_metabigor` (method) `cli/commands/recon_migrated.py:1161` `def do_metabigor(self, line)` -- Executes Metabigor commands for OSINT and scanning tasks with guided input or predefined arguments.
- `ReconMigratedCommandSet.do_httprobe` (method) `cli/commands/recon_migrated.py:1237` `def do_httprobe(self, line)` -- Executes the httprobe tool to probe domains for working HTTP and HTTPS servers.
- `ReconMigratedCommandSet.do_recon` (method) `cli/commands/recon_migrated.py:1280` `def do_recon(self, line)` -- Performs reconnaissance on a specified self.params['domain'] using crt.sh (the target must be visible on internet)...
- `ReconMigratedCommandSet.do_dnschef` (method) `cli/commands/recon_migrated.py:1334` `def do_dnschef(self, line)` -- Executes the DNSChef tool to monitor DNS queries and intercept responses.
- `ReconMigratedCommandSet.do_ipinfo` (method) `cli/commands/recon_migrated.py:1369` `def do_ipinfo(self, line)` -- Retrieves detailed information about an IP address using the ARIN API.

## cli/commands/redteam_gym.py
Depends on: `cli/commands/_base.py`, `modules/redteam_gym.py`, `utils.py`
- `RedTeamGymCommandSet.do_gym` (method) `cli/commands/redteam_gym.py:39` `def do_gym(self, line)` -- Red Team Gym — gamified pentest training with ELO scoring.

## cli/commands/resource_scripting.py
Depends on: `cli/commands/_base.py`, `modules/resource_script.py`, `utils.py`
- `on_cmd` (function) `cli/commands/resource_scripting.py:35` `def on_cmd(cmd)`
- `on_print` (function) `cli/commands/resource_scripting.py:39` `def on_print(msg)`
- `ResourceCommandSet.do_resource` (method) `cli/commands/resource_scripting.py:49` `def do_resource(self, line)` -- Run an enhanced resource script.
- `ResourceCommandSet.do_makerc` (method) `cli/commands/resource_scripting.py:88` `def do_makerc(self, line)` -- Record session commands to a resource script.
- `ResourceCommandSet.do_spool` (method) `cli/commands/resource_scripting.py:122` `def do_spool(self, line)` -- Log session output to a file.
- `ResourceCommandSet.do_mkrc` (method) `cli/commands/resource_scripting.py:152` `def do_mkrc(self, line)` -- Alias for makerc — record commands to a script.

## cli/commands/scan.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanCommandSet.do_gobuster` (method) `cli/commands/scan.py:56` `def do_gobuster(self, line)` -- Uses `gobuster` for directory and virtual host fuzzing based on provided parameters.
- `ScanCommandSet.do_arpscan` (method) `cli/commands/scan.py:129` `def do_arpscan(self, line)` -- Executes an ARP scan using `arp-scan`.
- `ScanCommandSet.do_dirsearch` (method) `cli/commands/scan.py:170` `def do_dirsearch(self, line)` -- Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL.
- `ScanCommandSet.do_dmitry` (method) `cli/commands/scan.py:213` `def do_dmitry(self, line)` -- This function constructs and executes a command for the 'dmitry' tool.
- `ScanCommandSet.do_feroxbuster` (method) `cli/commands/scan.py:248` `def do_feroxbuster(self, line)` -- Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing.
- `ScanCommandSet.do_nmapscript` (method) `cli/commands/scan.py:316` `def do_nmapscript(self, line)` -- Perform an Nmap scan using a specified script and port.
- `ScanCommandSet.do_nuclei` (method) `cli/commands/scan.py:350` `def do_nuclei(self, line)` -- Executes a Nuclei scan on a specified target URL or host.
- `ScanCommandSet.do_amass` (method) `cli/commands/scan.py:392` `def do_amass(self, line)` -- Executes Amass to perform a passive enumeration on a given domain.
- `ScanCommandSet.do_bbot` (method) `cli/commands/scan.py:422` `def do_bbot(self, line)` -- Executes a BBOT scan to perform various reconnaissance tasks.
- `ScanCommandSet.do_osmedeus` (method) `cli/commands/scan.py:473` `def do_osmedeus(self, line)` -- Executes Osmedeus scans with guided input for various scanning scenarios.
- `ScanCommandSet.do_magicrecon` (method) `cli/commands/scan.py:548` `def do_magicrecon(self, line)` -- Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and...
- `ScanCommandSet.do_hostdiscover` (method) `cli/commands/scan.py:606` `def do_hostdiscover(self, line)` -- Discover active hosts in a subnet by performing a ping sweep.
- `ScanCommandSet.do_portdiscover` (method) `cli/commands/scan.py:664` `def do_portdiscover(self, line)` -- Scan all ports on a specified host to identify open ports.
- `ScanCommandSet.do_portservicediscover` (method) `cli/commands/scan.py:724` `def do_portservicediscover(self, line)` -- Scan all ports on a specified host to identify open ports and associated services.
- `ScanCommandSet.do_skipfish` (method) `cli/commands/scan.py:789` `def do_skipfish(self, line)` -- This function executes the web security scanning tool Skipfish using the provided configuration and parameters.
- `ScanCommandSet.do_vscan` (method) `cli/commands/scan.py:839` `def do_vscan(self, line)` -- Perform port scanning using vscan with the provided parameters.

## cli/commands/scan_migrated.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanMigratedCommandSet.do_cme` (method) `cli/commands/scan_migrated.py:37` `def do_cme(self, line)` -- Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target.
- `ScanMigratedCommandSet.do_ldapdomaindump` (method) `cli/commands/scan_migrated.py:176` `def do_ldapdomaindump(self, line)` -- Dumps LDAP information using `ldapdomaindump` with credentials from a file.
- `ScanMigratedCommandSet.do_bloodhound` (method) `cli/commands/scan_migrated.py:218` `def do_bloodhound(self, line)` -- Perform LDAP enumeration using bloodhound-python with credentials from a file.
- `ScanMigratedCommandSet.do_swaks` (method) `cli/commands/scan_migrated.py:267` `def do_swaks(self, line)` -- Sends an email using `swaks` (Swiss Army Knife for SMTP).
- `ScanMigratedCommandSet.do_samrdump` (method) `cli/commands/scan_migrated.py:306` `def do_samrdump(self, line)` -- Run `impacket-samrdump` to dump SAM data from specified ports.
- `ScanMigratedCommandSet.do_lynis` (method) `cli/commands/scan_migrated.py:361` `def do_lynis(self, line)` -- Performs a Lynis audit on the specified remote system.
- `ScanMigratedCommandSet.do_snmpcheck` (method) `cli/commands/scan_migrated.py:390` `def do_snmpcheck(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_snmpwalk` (method) `cli/commands/scan_migrated.py:417` `def do_snmpwalk(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_smtpuserenum` (method) `cli/commands/scan_migrated.py:444` `def do_smtpuserenum(self, line)` -- Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.
- `ScanMigratedCommandSet.do_sessionssh` (method) `cli/commands/scan_migrated.py:483` `def do_sessionssh(self, line)` -- Execute a command to list active SSH connections.
- `ScanMigratedCommandSet.do_smbattack` (method) `cli/commands/scan_migrated.py:507` `def do_smbattack(self, line)` -- Scans for hosts with SMB service open on port 445 in the specified target network.
- `find_tgts` (function) `cli/commands/scan_migrated.py:536` `def find_tgts(subnet)` -- Finds and returns a list of target hosts with port 445 open in the specified subnet.
- `setup_handler` (function) `cli/commands/scan_migrated.py:562` `def setup_handler(config_file, lhost, lport)` -- Sets up a Metasploit multi/handler configuration in the given config file.
- `conficker_exploit` (function) `cli/commands/scan_migrated.py:582` `def conficker_exploit(config_file, host, lhost, lport)` -- Configures and writes a Metasploit exploit for the Conficker vulnerability to the given config file.
- `smb_brute` (function) `cli/commands/scan_migrated.py:602` `def smb_brute(config_file, host, passwd_file, lhost, lport)` -- Configures and writes a Metasploit SMB brute force exploit for the given host to the provided config file.
- `ScanMigratedCommandSet.do_parsero` (method) `cli/commands/scan_migrated.py:667` `def do_parsero(self, line)` -- Executes a parsero scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_changeme` (method) `cli/commands/scan_migrated.py:699` `def do_changeme(self, line)` -- Executes a changeme scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_enum4linux_ng` (method) `cli/commands/scan_migrated.py:730` `def do_enum4linux_ng(self, line)` -- Performs enumeration of information from a target system using `enum4linux-ng`.
- `ScanMigratedCommandSet.do_fuzz` (method) `cli/commands/scan_migrated.py:770` `def do_fuzz(self, line)` -- Executes a web server fuzzing script with user-provided parameters.
- `ScanMigratedCommandSet.do_kerbrute` (method) `cli/commands/scan_migrated.py:815` `def do_kerbrute(self, line)` -- Executes the Kerbrute tool to enumerate user accounts against a specified target self.params['domain'] controller.
- `ScanMigratedCommandSet.do_davtest` (method) `cli/commands/scan_migrated.py:901` `def do_davtest(self, line)` -- Tests WebDAV server configurations using `davtest`.
- `ScanMigratedCommandSet.do_evil_ssdp` (method) `cli/commands/scan_migrated.py:942` `def do_evil_ssdp(self, line)` -- Runs evil-ssdp with various options and user-selected templates.
- `ScanMigratedCommandSet.do_netexec` (method) `cli/commands/scan_migrated.py:988` `def do_netexec(self, line)` -- Executes netexec with various options for network protocol operations.
- `install_netexec` (function) `cli/commands/scan_migrated.py:1015` `def install_netexec()`
- `install_netexec_pipx` (function) `cli/commands/scan_migrated.py:1020` `def install_netexec_pipx()`
- `ScanMigratedCommandSet.do_allin` (method) `cli/commands/scan_migrated.py:1241` `def do_allin(self, line)` -- Execute the AlliN.py tool with various scan modes and parameters.
- `ScanMigratedCommandSet.do_windapsearch` (method) `cli/commands/scan_migrated.py:1312` `def do_windapsearch(self, line)` -- Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries.
- `ScanMigratedCommandSet.do_ldapsearch` (method) `cli/commands/scan_migrated.py:1440` `def do_ldapsearch(self, line)` -- Executes an LDAP search against a target remote host (self.params['rhost']) and saves the results.
- `ScanMigratedCommandSet.do_arjun` (method) `cli/commands/scan_migrated.py:1501` `def do_arjun(self, line)` -- Executes an Arjun scan on the specified URL for parameter discovery.
- `ScanMigratedCommandSet.do_finger_user_enum` (method) `cli/commands/scan_migrated.py:1569` `def do_finger_user_enum(self, line)` -- Executes the `finger-user-enum` tool for enumerating users on the target host.
- `ScanMigratedCommandSet.do_wpscan` (method) `cli/commands/scan_migrated.py:1615` `def do_wpscan(self, line)` -- Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning.
- `ScanMigratedCommandSet.do_loxs` (method) `cli/commands/scan_migrated.py:1678` `def do_loxs(self, line)` -- Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_blazy` (method) `cli/commands/scan_migrated.py:1722` `def do_blazy(self, line)` -- Command blazy: Installs and runs blazy for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_parth` (method) `cli/commands/scan_migrated.py:1771` `def do_parth(self, line)` -- Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters.
- `ScanMigratedCommandSet.do_breacher` (method) `cli/commands/scan_migrated.py:1840` `def do_breacher(self, line)` -- Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities.
- `ScanMigratedCommandSet.do_openredirex` (method) `cli/commands/scan_migrated.py:1902` `def do_openredirex(self, line)` -- Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities.
- `ScanMigratedCommandSet.do_odat` (method) `cli/commands/scan_migrated.py:1970` `def do_odat(self, line)` -- Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database.
- `ScanMigratedCommandSet.do_rpcmap_py` (method) `cli/commands/scan_migrated.py:2088` `def do_rpcmap_py(self, line)` -- Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.
- `ScanMigratedCommandSet.do_pykerbrute` (method) `cli/commands/scan_migrated.py:2131` `def do_pykerbrute(self, line)` -- Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory...
- `ScanMigratedCommandSet.do_netview` (method) `cli/commands/scan_migrated.py:2201` `def do_netview(self, line)` -- Executes the Impacket netview tool to list network shares on a specified target.
- `ScanMigratedCommandSet.do_rdp_check_py` (method) `cli/commands/scan_migrated.py:2265` `def do_rdp_check_py(self, line)` -- Executes the RDP check tool to verify credentials or hash-based authentication on a target system.
- `ScanMigratedCommandSet.do_mqtt_check_py` (method) `cli/commands/scan_migrated.py:2330` `def do_mqtt_check_py(self, line)` -- Executes the MQTT check tool to verify credentials on a target system with optional SSL.
- `ScanMigratedCommandSet.do_lookupsid_py` (method) `cli/commands/scan_migrated.py:2385` `def do_lookupsid_py(self, line)` -- Executes the LookupSID tool to perform SID enumeration on a target system.
- `ScanMigratedCommandSet.do_lookupsid` (method) `cli/commands/scan_migrated.py:2458` `def do_lookupsid(self, line)` -- Executes the Impacket lookupsid tool to enumerate SIDs on a target system.
- `ScanMigratedCommandSet.do_certipy_ad` (method) `cli/commands/scan_migrated.py:2520` `def do_certipy_ad(self, line)` -- Run certipy-ad against Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_certipy` (method) `cli/commands/scan_migrated.py:2584` `def do_certipy(self, line)` -- Executes the Certipy tool to interact with Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_sawks` (method) `cli/commands/scan_migrated.py:2678` `def do_sawks(self, line)` -- Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phishing simulations.
- `ScanMigratedCommandSet.do_ad_ldap_enum` (method) `cli/commands/scan_migrated.py:2715` `def do_ad_ldap_enum(self, line)` -- Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers) through LDAP, collecting...
- `ScanMigratedCommandSet.do_net_rpc_addmem` (method) `cli/commands/scan_migrated.py:2769` `def do_net_rpc_addmem(self, line)` -- Executes the net rpc group addmem command to add a user to a specified group in Active Directory.
- `ScanMigratedCommandSet.do_pre2k` (method) `cli/commands/scan_migrated.py:2815` `def do_pre2k(self, line)` -- Executes the pre2k tool to query the self.params['domain'] for pre-Windows 2000 machine accounts or to pass a list...
- `ScanMigratedCommandSet.do_hound` (method) `cli/commands/scan_migrated.py:2908` `def do_hound(self, line)` -- Executes the hound tool for Hound is a simple and light tool for information gathering and capture exact GPS coordinates

## cli/commands/security.py
Depends on: `cli/commands/_base.py`, `core/config.py`, `core/console.py`, `core/credential_vault.py`, `modules/hash_cracker.py`, `modules/opsec_scorer.py`
- `SecurityCommandSet.do_opsec` (method) `cli/commands/security.py:26` `def do_opsec(self, line)` -- Score OPSEC risk for a LazyOwn command before execution.
- `SecurityCommandSet.do_seal_credentials` (method) `cli/commands/security.py:106` `def do_seal_credentials(self, _line)` -- Encrypt all sensitive values in payload.json using AES-256-GCM.
- `SecurityCommandSet.do_rotate_aes` (method) `cli/commands/security.py:127` `def do_rotate_aes(self, _line)` -- Generate a new AES key and re-encrypt all sealed credentials.
- `SecurityCommandSet.do_unseal_credentials` (method) `cli/commands/security.py:150` `def do_unseal_credentials(self, _line)` -- Decrypt sealed credential values in payload.json for inspection.
- `SecurityCommandSet.do_crack_hashes` (method) `cli/commands/security.py:170` `def do_crack_hashes(self, line)` -- Crack password hashes from a file using John the Ripper or Hashcat.
- `SecurityCommandSet.complete_opsec` (method) `cli/commands/security.py:267` `def complete_opsec(self, text, line, begidx, endidx)`
- `SecurityCommandSet.complete_crack_hashes` (method) `cli/commands/security.py:276` `def complete_crack_hashes(self, text, line, begidx, endidx)`

## cli/commands/session_ops.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/chain_mode.py`, `cli/commands/_base.py`, `cli/config_history.py`, `cli/ops_commands.py`, `cli/session_resumer.py`, `cli/show.py`, `core/config.py`, `core/payload_schema.py`, `modules/autonomous_exploit_engine.py`, `modules/enrich.py`, `modules/lazy_loop.py`, `modules/lazy_rbac.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `skills/autonomous_daemon.py`, `utils.py`
Imported by: `tests/test_auto_crypto.py`, `tests/test_lazy_runner.py`, `tests/test_session_ops_command_set.py`
- `SessionOpsCommandSet.do_note` (method) `cli/commands/session_ops.py:79` `def do_note(self, line)` -- Capture a quick operator note attached to the current target and phase.
- `SessionOpsCommandSet.do_l00t` (method) `cli/commands/session_ops.py:104` `def do_l00t(self, line)` -- Unified loot: show, search, reuse, graph, and mark credentials.
- `SessionOpsCommandSet.do_loot` (method) `cli/commands/session_ops.py:153` `def do_loot(self, line)` -- Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).
- `SessionOpsCommandSet.do_pivot` (method) `cli/commands/session_ops.py:161` `def do_pivot(self, line)` -- Record a newly discovered pivot target or show the pivot chain.
- `SessionOpsCommandSet.do_tasks` (method) `cli/commands/session_ops.py:186` `def do_tasks(self, line)` -- View and manage the task queue from sessions/tasks.json.
- `SessionOpsCommandSet.do_scans` (method) `cli/commands/session_ops.py:219` `def do_scans(self, line)` -- List nmap scan files in sessions/ with age, size, and open ports.
- `SessionOpsCommandSet.do_sitrep` (method) `cli/commands/session_ops.py:236` `def do_sitrep(self, line)` -- Print a unified operational situation report.
- `SessionOpsCommandSet.do_assign` (method) `cli/commands/session_ops.py:253` `def do_assign(self, line)` -- assign a parameter value, persist to payload.json and refresh aliases.
- `SessionOpsCommandSet.do_tenant` (method) `cli/commands/session_ops.py:317` `def do_tenant(self, line)` -- Manage multi-tenancy: list, switch, or create engagement tenants.
- `SessionOpsCommandSet.do_scope` (method) `cli/commands/session_ops.py:390` `def do_scope(self, line)` -- Manage the authorized engagement scope and the scope-guard posture.
- `SessionOpsCommandSet.do_show` (method) `cli/commands/session_ops.py:456` `def do_show(self, line)` -- Show params, modules, payloads, or active module options.
- `SessionOpsCommandSet.do_list` (method) `cli/commands/session_ops.py:532` `def do_list(self, line)` -- Lists all available scripts in the modules directory.
- `SessionOpsCommandSet.do_run` (method) `cli/commands/session_ops.py:561` `def do_run(self, line)` -- Runs a specific LazyOwn script or active module.
- `SessionOpsCommandSet.do_payload` (method) `cli/commands/session_ops.py:600` `def do_payload(self, line)` -- Load parameters from a specified payload JSON file.
- `SessionOpsCommandSet.do_next` (method) `cli/commands/session_ops.py:651` `def do_next(self, line)` -- Show next-step recommendations or execute the active autosuggest.
- `SessionOpsCommandSet.do_frontier` (method) `cli/commands/session_ops.py:695` `def do_frontier(self, line)` -- Preview the planner intents the autonomous loops would run next.
- `SessionOpsCommandSet.do_traces` (method) `cli/commands/session_ops.py:739` `def do_traces(self, line)` -- Show recent autonomous step traces with evidence and traffic ids.
- `SessionOpsCommandSet.do_chainmode` (method) `cli/commands/session_ops.py:820` `def do_chainmode(self, line)` -- Toggle interactive kill-chain chaining after every command.
- `SessionOpsCommandSet.do_engage` (method) `cli/commands/session_ops.py:871` `def do_engage(self, line)` -- Drive a single target through the full kill-chain in one command.
- `SessionOpsCommandSet.do_pipeline` (method) `cli/commands/session_ops.py:998` `def do_pipeline(self, line)` -- Declarative composition layer: run a YAML pipeline of LazyOwn commands.
- `SessionOpsCommandSet.do_lazyscript` (method) `cli/commands/session_ops.py:1089` `def do_lazyscript(self, line)` -- Executes commands defined in a lazyscript file.
- `SessionOpsCommandSet.do_hunt` (method) `cli/commands/session_ops.py:1121` `def do_hunt(self, line)` -- Run an autonomous exploitation chain against a target.
- `SessionOpsCommandSet.do_resume` (method) `cli/commands/session_ops.py:1212` `def do_resume(self, line)` -- Browse previous sessions and load a target from a past engagement.
- `SessionOpsCommandSet.do_getseclist` (method) `cli/commands/session_ops.py:1234` `def do_getseclist(self, line)` -- Get the SecLists wordlist from GitHub.
- `SessionOpsCommandSet.do_download_resources` (method) `cli/commands/session_ops.py:1272` `def do_download_resources(self, line)` -- Downloads resources into the `sessions` directory.
- `SessionOpsCommandSet.do_collab_join` (method) `cli/commands/session_ops.py:1305` `def do_collab_join(self, line)` -- Print the multi-operator collaboration join URL and SSE endpoint.
- `SessionOpsCommandSet.do_kick` (method) `cli/commands/session_ops.py:1336` `def do_kick(self, line)` -- Handles the process of sending a spoofed ARP packet to a specified IP address with a given MAC address.
- `SessionOpsCommandSet.do_qa` (method) `cli/commands/session_ops.py:1385` `def do_qa(self, line)` -- Exits the application quickly without confirmation.
- `SessionOpsCommandSet.do_clock` (method) `cli/commands/session_ops.py:1447` `def do_clock(self, line)` -- Displays the current date and time, and runs a custom shell script.
- `SessionOpsCommandSet.do_gencert` (method) `cli/commands/session_ops.py:1495` `def do_gencert(self, line)` -- Generates a certificate authority (CA), client certificate, and client key.
- `SessionOpsCommandSet.do_load_session` (method) `cli/commands/session_ops.py:1507` `def do_load_session(self, line)` -- Load the session from the sessionLazyOwn.json file and display the status of various parameters.
- `SessionOpsCommandSet.do_clone_site` (method) `cli/commands/session_ops.py:1557` `def do_clone_site(self, line)` -- Clone a website and serve the files in sessions/{url_cloned}.
- `SessionOpsCommandSet.do_msfshellcoder` (method) `cli/commands/session_ops.py:1603` `def do_msfshellcoder(self, line)` -- Generate shellcode in C format using msfvenom for either a custom command or a reverse shell payload.

## cli/commands/shellsys.py
Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `utils.py`
Imported by: `tests/test_shellsys_command_set.py`
- `ShellSysCommandSet.do_sh` (method) `cli/commands/shellsys.py:30` `def do_sh(self, line)` -- Executes a shell command directly from the LazyOwn interface.
- `ShellSysCommandSet.do_sys` (method) `cli/commands/shellsys.py:62` `def do_sys(self, line)` -- Executes a shell command directly from the LazyOwn interface.
- `ShellSysCommandSet.do_pwd` (method) `cli/commands/shellsys.py:110` `def do_pwd(self, line)` -- Displays the current working directory and lists files, and copies the current directory path to the clipboard.
- `ShellSysCommandSet.do_nano` (method) `cli/commands/shellsys.py:146` `def do_nano(self, line)` -- Opens or creates the file using line in the sessions directory for editing using nano.
- `ShellSysCommandSet.do_cron` (method) `cli/commands/shellsys.py:170` `def do_cron(self, line)` -- Schedules a command to run at a specified time.
- `lazyrun_command` (function) `cli/commands/shellsys.py:205` `def lazyrun_command()`
- `ShellSysCommandSet.do_clean` (method) `cli/commands/shellsys.py:216` `def do_clean(self, line)` -- Deletes files and directories in the `sessions` directory, excluding specified files and directories.
- `ShellSysCommandSet.do_fixperm` (method) `cli/commands/shellsys.py:303` `def do_fixperm(self, line)` -- Fix permissions for LazyOwn shell scripts.
- `ShellSysCommandSet.do_fixel` (method) `cli/commands/shellsys.py:336` `def do_fixel(self, line)` -- Fixes file permissions and line endings in the project directories.
- `ShellSysCommandSet.do_pop` (method) `cli/commands/shellsys.py:369` `def do_pop(self, line)` -- Open a centered popup in the current tmux session to execute a shell command.
- `ShellSysCommandSet.do_tab` (method) `cli/commands/shellsys.py:406` `def do_tab(self, line)` -- Executes the `lazypyautogui.py` script with optional arguments.

## cli/commands/sleep_obfuscation.py
Depends on: `cli/commands/_base.py`, `modules/sleep_obfuscation.py`, `utils.py`
- `SleepObfuscationCommandSet.do_sleep_list` (method) `cli/commands/sleep_obfuscation.py:23` `def do_sleep_list(self, line)` -- List available sleep obfuscation techniques.
- `SleepObfuscationCommandSet.do_sleep_info` (method) `cli/commands/sleep_obfuscation.py:50` `def do_sleep_info(self, line)` -- Show detailed information about a sleep obfuscation technique.
- `SleepObfuscationCommandSet.do_sleep_configure` (method) `cli/commands/sleep_obfuscation.py:82` `def do_sleep_configure(self, line)` -- Configure the active sleep obfuscation technique.

## cli/commands/socks_proxy.py
Depends on: `cli/commands/_base.py`, `modules/socks_proxy.py`, `utils.py`
- `SocksProxyCommandSet.do_socks_config` (method) `cli/commands/socks_proxy.py:25` `def do_socks_config(self, line)` -- Show or configure the SOCKS5 proxy.
- `SocksProxyCommandSet.do_socks_sessions` (method) `cli/commands/socks_proxy.py:75` `def do_socks_sessions(self, line)` -- List active SOCKS proxy sessions.
- `SocksProxyCommandSet.do_socks_export` (method) `cli/commands/socks_proxy.py:94` `def do_socks_export(self, line)` -- Export SOCKS5 proxy specification for beacon delivery.

## cli/commands/supply_chain.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `SupplyChainCommandSet.do_depconfuse` (method) `cli/commands/supply_chain.py:95` `def do_depconfuse(self, line)` -- Scan a requirements.txt for dependency confusion candidates.
- `SupplyChainCommandSet.do_package_squat` (method) `cli/commands/supply_chain.py:140` `def do_package_squat(self, line)` -- Generate a malicious PyPI package for dependency confusion.
- `SupplyChainCommandSet.do_depscan` (method) `cli/commands/supply_chain.py:216` `def do_depscan(self, line)` -- Scan a directory tree for dependency files and flag risks.
- `is_internal_name` (function) `cli/commands/supply_chain.py:450` `def is_internal_name(name)` -- Check if a package name looks internal/private.

## cli/commands/surface.py
Depends on: `cli/commands/_base.py`, `modules/attack_surface3d.py`, `modules/estorides_fusion.py`, `modules/surface_ops.py`, `utils.py`
- `SurfaceCommandSet.do_scandiscovery` (method) `cli/commands/surface.py:43` `def do_scandiscovery(self, line)` -- Scan every discovery IP with operator confirmation.
- `SurfaceCommandSet.do_estorides_intel` (method) `cli/commands/surface.py:86` `def do_estorides_intel(self, line)` -- Fuse estorides OSINT entities into the campaign intel graphs.

## cli/commands/ux.py
Depends on: `cli/commands/_base.py`, `cli/config_history.py`, `cli/fuzzy_match.py`, `cli/output_mode.py`, `cli/session_hud.py`, `cli/toast_bus.py`, `core/config.py`, `core/console.py`, `utils.py`
- `UxCommandSet.do_hud` (method) `cli/commands/ux.py:46` `def do_hud(self, line)` -- Session counters: elapsed time, commands run, material captured.
- `UxCommandSet.do_undo` (method) `cli/commands/ux.py:85` `def do_undo(self, line)` -- Revert the last assign/set configuration change.
- `UxCommandSet.do_config_diff` (method) `cli/commands/ux.py:115` `def do_config_diff(self, line)` -- Show what changed since the session started.
- `UxCommandSet.do_cheat` (method) `cli/commands/ux.py:140` `def do_cheat(self, line)` -- Render a cheatsheet section inside the shell.
- `UxCommandSet.do_toast` (method) `cli/commands/ux.py:167` `def do_toast(self, line)` -- Raise a toast notification inside the cmd2 shell.
- `UxCommandSet.do_suggest` (method) `cli/commands/ux.py:261` `def do_suggest(self, line)` -- Fuzzy command suggestion for typos and fragments.

## cli/config_history.py
Imported by: `cli/commands/session_ops.py`, `cli/commands/ux.py`
- `ConfigHistory.capture_baseline` (method) `cli/config_history.py:30` `def capture_baseline(self, state)` -- Store session-start snapshot used by diff.
- `ConfigHistory.push` (method) `cli/config_history.py:38` `def push(self, state)` -- Push a snapshot before mutation.
- `ConfigHistory.undo` (method) `cli/config_history.py:48` `def undo(self)` -- Pop the newest snapshot.
- `ConfigHistory.diff` (method) `cli/config_history.py:58` `def diff(self, current)` -- Compare current state against the baseline.
- `ConfigHistory.depth` (method) `cli/config_history.py:76` `def depth(self)` -- Return number of stored undo steps.
- `get_shell_history` (function) `cli/config_history.py:81` `def get_shell_history(shell)` -- Return the ConfigHistory bound to a shell, creating it on demand.
- `track_before` (function) `cli/config_history.py:104` `def track_before(history, state)` -- Capture baseline on first use then push a pre-mutation snapshot.

## cli/config_status.py
Depends on: `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `ConfigStatus.__init__` (method) `cli/config_status.py:70` `def __init__(self, params, config)`
- `ConfigStatus.render_status` (method) `cli/config_status.py:89` `def render_status(self)` -- Render the grouped configuration status table.
- `ConfigStatus.render_quick_check` (method) `cli/config_status.py:129` `def render_quick_check(self)` -- Quick check: show only required fields that are not set.

## cli/confirm.py
Imported by: `cli/commands/ai.py`, `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/infra.py`
- `confirm` (function) `cli/confirm.py:27` `def confirm(question, default, yes_values)` -- Ask a yes/no question, never raising on non-interactive stdin.

## cli/contextual_help.py
Depends on: `cli/palette.py`, `cli/phase_labels.py`, `core/console.py`
Imported by: `cli/commands/help_ui.py`, `tests/test_phase_labels.py`
- `ContextualHelp.__init__` (method) `cli/contextual_help.py:176` `def __init__(self, aliases, params, config)`
- `ContextualHelp.get_command_info` (method) `cli/contextual_help.py:188` `def get_command_info(self, name)` -- Return enriched info for a command, or None if not found.
- `ContextualHelp.render_command_help` (method) `cli/contextual_help.py:208` `def render_command_help(self, name)` -- Render contextual help for a single command.
- `ContextualHelp.render_phase_commands` (method) `cli/contextual_help.py:261` `def render_phase_commands(self, phase)` -- Render all commands for a given phase.
- `ContextualHelp.render_requirements_status` (method) `cli/contextual_help.py:281` `def render_requirements_status(self)` -- Show which requirements are met for the current session.

## cli/dashboard_layout.py
Imported by: `cli/dashboard_tui.py`
- `layout_mode` (function) `cli/dashboard_layout.py:28` `def layout_mode(width, config)` -- Return the layout bucket for a terminal width.
- `hidden_panels` (function) `cli/dashboard_layout.py:45` `def hidden_panels(mode)` -- Return panel ids hidden in the given layout mode.

## cli/dashboard_tui.py
Depends on: `cli/commands/containers.py`, `cli/dashboard_layout.py`, `cli/graph_advisor.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/recommendation_signals.py`, `cli/toast_bus.py`, `modules/killchain.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_dashboard_tui.py`
- `CommandRequested.__init__` (method) `cli/dashboard_tui.py:100` `def __init__(self, command)`
- `PhaseSelected.__init__` (method) `cli/dashboard_tui.py:108` `def __init__(self, phase)`
- `dispatch_command` (function) `cli/dashboard_tui.py:113` `def dispatch_command(command, timeout)` -- Run one LazyOwn command headlessly and capture its output.
- `TargetPanel.get_selection` (method) `cli/dashboard_tui.py:335` `def get_selection(self, selection)` -- Override to prevent IndexError when selection offsets exceed text length.
- `TargetPanel.render_content` (method) `cli/dashboard_tui.py:348` `def render_content(self, payload, world)`
- `TargetPanel.update_data` (method) `cli/dashboard_tui.py:374` `def update_data(self, payload, world)`
- `KillChainPanel.__init__` (method) `cli/dashboard_tui.py:393` `def __init__(self)`
- `KillChainPanel.update_data` (method) `cli/dashboard_tui.py:397` `def update_data(self, progress)` -- Render kill-chain progress.
- `KillChainPanel.on_click` (method) `cli/dashboard_tui.py:418` `def on_click(self, event)` -- Select the phase whose row was clicked.
- `ConfigPanel.update_data` (method) `cli/dashboard_tui.py:442` `def update_data(self, payload)`
- `CommandsPanel.update_data` (method) `cli/dashboard_tui.py:472` `def update_data(self, commands)`
- `ReasoningPanel.update_data` (method) `cli/dashboard_tui.py:507` `def update_data(self, entries)` -- Render the most recent daemon decisions, newest first.
- `OpsPanel.update_data` (method) `cli/dashboard_tui.py:544` `def update_data(self, world, tasks, creds, hashes, beacons, cred_lines)`
- `HintBar.__init__` (method) `cli/dashboard_tui.py:610` `def __init__(self)`
- `HintBar.compose` (method) `cli/dashboard_tui.py:615` `def compose(self)`
- `HintBar.update_data` (method) `cli/dashboard_tui.py:619` `def update_data(self, hints)` -- Replace the hint buttons with one button per suggestion.
- `HintBar.on_button_pressed` (method) `cli/dashboard_tui.py:644` `def on_button_pressed(self, event)` -- Run the clicked suggestion as if it had been typed.
- `ToastPanel.update_data` (method) `cli/dashboard_tui.py:671` `def update_data(self, payload, sessions_dir, width)` -- Render the latest notifications for the active theme.
- `NextStepsPanel.update_data` (method) `cli/dashboard_tui.py:718` `def update_data(self, recommendations)`
- `LazyOwnDashboard.__init__` (method) `cli/dashboard_tui.py:807` `def __init__(self, payload_path, sessions_dir)`
- `LazyOwnDashboard.compose` (method) `cli/dashboard_tui.py:836` `def compose(self)`
- `LazyOwnDashboard.on_mount` (method) `cli/dashboard_tui.py:855` `def on_mount(self)`
- `LazyOwnDashboard.on_input_submitted` (method) `cli/dashboard_tui.py:860` `def on_input_submitted(self, event)` -- Run the typed command and clear the input.
- `LazyOwnDashboard.on_command_requested` (method) `cli/dashboard_tui.py:872` `def on_command_requested(self, event)` -- Dispatch a command in a worker so the UI never blocks.
- `LazyOwnDashboard.on_phase_selected` (method) `cli/dashboard_tui.py:912` `def on_phase_selected(self, event)` -- Filter the center panel to a phase chosen by clicking the kill chain.
- `LazyOwnDashboard.action_refresh_data` (method) `cli/dashboard_tui.py:923` `def action_refresh_data(self)`
- `LazyOwnDashboard.action_toggle_compact` (method) `cli/dashboard_tui.py:926` `def action_toggle_compact(self)` -- Toggle the compact single-column layout for narrow terminals.
- `LazyOwnDashboard.action_screenshot` (method) `cli/dashboard_tui.py:956` `def action_screenshot(self)` -- Save an SVG screenshot next to the sessions directory.
- `LazyOwnDashboard.action_export_snapshot` (method) `cli/dashboard_tui.py:967` `def action_export_snapshot(self)` -- Export the current dashboard data as JSON for automation.
- `LazyOwnDashboard.action_next_phase` (method) `cli/dashboard_tui.py:987` `def action_next_phase(self)` -- Advance to the next kill-chain phase and refresh the display.
- `LazyOwnDashboard.action_prev_phase` (method) `cli/dashboard_tui.py:991` `def action_prev_phase(self)` -- Step back to the previous kill-chain phase.
- `launch` (function) `cli/dashboard_tui.py:1064` `def launch(payload_path, sessions_dir)` -- Launch the dashboard and block until the user quits.

## cli/doctor.py
Depends on: `cli/wizard.py`, `core/console.py`, `core/profiles.py`
Imported by: `cli/commands/help_ui.py`
- `DoctorReport.failures` (method) `cli/doctor.py:119` `def failures(self)` -- Return the checks whose status is :data:`STATUS_FAIL`.
- `DoctorReport.warnings` (method) `cli/doctor.py:124` `def warnings(self)` -- Return the checks whose status is :data:`STATUS_WARN`.
- `DoctorReport.healthy` (method) `cli/doctor.py:129` `def healthy(self)` -- Return ``True`` when no check failed (warnings are tolerated).
- `DoctorReport.overall_status` (method) `cli/doctor.py:134` `def overall_status(self)` -- Return the worst status across every check.
- `check_python_version` (function) `cli/doctor.py:143` `def check_python_version(version_info)` -- Verify the interpreter satisfies :data:`MIN_PYTHON_VERSION`.
- `check_virtualenv` (function) `cli/doctor.py:172` `def check_virtualenv()` -- Report whether the framework is running inside its virtual environment.
- `check_packages` (function) `cli/doctor.py:209` `def check_packages(specs, finder)` -- Verify every dependency in ``specs`` is importable without importing it.
- `check_certificates` (function) `cli/doctor.py:248` `def check_certificates(root)` -- Verify the self-signed C2 certificate pair exists.
- `check_payload` (function) `cli/doctor.py:269` `def check_payload(root)` -- Verify ``payload.json`` exists in the repository root.
- `check_seclists` (function) `cli/doctor.py:289` `def check_seclists(finder)` -- Verify a SecLists installation is discoverable on disk.
- `check_command_index` (function) `cli/doctor.py:313` `def check_command_index(root)`
- `check_external_tools` (function) `cli/doctor.py:343` `def check_external_tools(checker)` -- Adapt :func:`cli.wizard.check_binaries` into preflight check results.
- `gather_report` (function) `cli/doctor.py:368` `def gather_report(root)` -- Run every preflight check and collect the results without printing.
- `render_report` (function) `cli/doctor.py:406` `def render_report(report, console)` -- Render a :class:`DoctorReport` as a rich table with a summary banner.
- `run` (function) `cli/doctor.py:451` `def run(root, console)` -- Gather and render the preflight report.
- `fix_report` (function) `cli/doctor.py:468` `def fix_report(report)` -- Interactively offer to fix every failure and warning in the report.


Next: [API_p4.md](API_p4.md)
