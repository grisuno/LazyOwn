# Postexp Phase Guide

Post-Exploitation — gather evidence, pivot and maintain situational awareness on a compromised host.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_add2find` | Add a new custom command to the 'find' system, saved in user_commands.json. | `lazyown.py` |
| `do_adversary` | LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in adversary.json | `lazyown.py` |
| `do_adversary_yaml` | Execute adversary from YAML in lazyadversaries/*.yaml | `lazyown.py` |
| `do_aes_pe` | Encrypt with AES and random key to PE EXE file, to usage with loaders. | `lazyown.py` |
| `do_apt_proxy` | Configures the local machine with internet access to act as an APT proxy for a machine without internet access. | `lazyown.py` |
| `do_apt_repo` | Creates a comprehensive local APT repository with enhanced dependency resolution. | `lazyown.py` |
| `do_atomic_lazyown` | Genera y ejecuta pruebas de Atomic Red Team usando el C2. | `lazyown.py` |
| `do_bin2shellcode` | Converts a binary file to a shellcode string in C or Nim format. | `lazyown.py` |
| `do_convert_remcomsvc_from_file` | Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice format, prints a sample, and saves it to sessions/remcomsvc.go. see lazyaddon … | `lazyown.py` |
| `do_cports` | Generates a command to display TCP and UDP ports and copies it to the clipboard. | `lazyown.py` |
| `do_create_synthetic` | Create a basic synthetic playbook from Nmap CSV when LLM fails. | `lazyown.py` |
| `do_createpayload` | Generates an obfuscated payload to evade AV detection using the payloadGenerator tool. thanks to smokeme | `lazyown.py` |
| `do_d3monizedshell` | Executes the D3m0n1z3dShell tool for persistence in Linux. | `lazyown.py` |
| `do_disableav` | Creates a Visual Basic Script (VBS) to attempt to disable antivirus settings. | `lazyown.py` |
| `do_exe2bin` | Trasnform file .exe into binary file. | `lazyown.py` |
| `do_exe2donutbin` | Trasnform file .exe into donut binary file. | `lazyown.py` |
| `do_extract_yaml` | Extract YAML from an existing debug file and try to create a playbook. | `lazyown.py` |
| `do_find` | Automates command execution based on a list of aliases and commands. | `lazyown.py` |
| `do_follina` | Executes the MSDT Follina exploit tool to create malicious documents for exploitation. | `lazyown.py` |
| `do_hex2shellcode` | Convert raw hex payload from msfvenom into NASM-compatible shellcode format. | `lazyown.py` |
| `do_internet_proxy` | Configures the local machine with internet access to act as a proxy for a machine without internet access. | `lazyown.py` |
| `do_issue_command_to_c2` | Exec command in the client using the C2. download: command you must put the file in sessions/temp_upload or use download_c2 command | `lazyown.py` |
| `do_lazywebshell` | Run LazyOwn webshell server. | `lazyown.py` |
| `do_mimikatzpy` | Executes the Impacket Mimikatz tool to interact with a target system for credential-related operations. | `lazyown.py` |
| `do_msfshellcoder` | Generate shellcode in C format using msfvenom for either a custom command or a reverse shell payload. | `lazyown.py` |
| `do_ofuscate_string` | Ofuscate a string into Go code. | `lazyown.py` |
| `do_ofuscatesh` | Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it. | `lazyown.py` |
| `do_ofuscatorps1` | Obfuscates a PowerShell script using various techniques. | `lazyown.py` |
| `do_path2hex` | Convert a binary path to x64 little-endian hex code for shellcode injection. | `lazyown.py` |
| `do_pezorsh` | Executes the PEzor tool to pack executables or shellcode with custom configurations. | `lazyown.py` |
| `do_pip_proxy` | Configures the local machine with internet access to act as a pip proxy for a machine without internet access. | `lazyown.py` |
| `do_pip_repo` | Sets up a local pip repository to serve Python packages for installation on a compromised machine without internet access. | `lazyown.py` |
| `do_powershell_cmd_stager` | Generate and execute a PowerShell command stager to run a .ps1 script. | `lazyown.py` |
| `do_rmfromfind` | Remove a custom command by index (as shown in 'find'). | `lazyown.py` |
| `do_rubeus` | Copies a command to the clipboard for downloading and running Rubeus. | `lazyown.py` |
| `do_scavenger` | Executes the Scavenger tool for multi-threaded post-exploitation scanning on target systems with SMB credentials. | `lazyown.py` |
| `do_scp` | Copies the local "sessions" directory to a remote host using scp, leveraging sshpass for automated authentication. | `lazyown.py` |
| `do_service_ssh` | Creates a systemd service file for a specified binary and generates a script to enable and start the service. | `lazyown.py` |
| `do_sessionsshstrace` | Attach strace to a running process and log output to a file. | `lazyown.py` |
| `do_shellcode` | Generates a Python one-liner to execute shellcode from a given URL. | `lazyown.py` |
| `do_shellcode2elf` | Convert shellcode into an ELF file and infect it. | `lazyown.py` |
| `do_shellcode2sylk` | Converts shellcode to SYLK format and saves the result to a file. | `lazyown.py` |
| `do_shellcode_search` | Search the shell-storm API for shellcodes using the provided keywords. | `lazyown.py` |
| `do_ssh_cmd` | Perform Remote Execution Command trow ssh using grisun0 user, see help grisun0 | `lazyown.py` |

## Next Phase

After completing the Postexp phase, proceed to:
**Persistence** (`docs/persist.md`) or **Lateral Movement** (`docs/lateral.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

