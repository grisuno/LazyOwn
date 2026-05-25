# Persist Phase Guide

Persistence — install implants, scheduled tasks or backdoors to retain access across reboots and credential changes.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_asprevbase64` | Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard. | `lazyown.py` |
| `do_backdoor_factory` | Creates a backdoored executable using `backdoor-factory`. | `lazyown.py` |
| `do_conptyshell` | Downloads ConPtyShell and prepares a PowerShell command for remote access. | `lazyown.py` |
| `do_createrevshell` | Creates a bash reverse shell script in the `sessions` directory with the specified `lhost` and `lport` values. | `lazyown.py` |
| `do_createwebshell` | Creates a web shell disguised as a `.jpg` file in the `sessions` directory. | `lazyown.py` |
| `do_createwinrevshell` | Creates a PowerShell reverse shell script in the `sessions` directory with the specified `lhost` and `lport` values. | `lazyown.py` |
| `do_darkarmour` | Uses the darkarmour tool to generate an undetectable version of a PE executable. | `lazyown.py` |
| `do_dr0p1t` | Execute the Dr0p1t tool to create a stealthy malware dropper. | `lazyown.py` |
| `do_ftp` | Connects to an ftp host using credentials from a file and a specified port. | `lazyown.py` |
| `do_generate_revshell` | Generate a reverse shell in various programming languages. | `lazyown.py` |
| `do_grisun0` | Creates and copies a shell command to add a new user `grisun0`, assign a password, add the user to the sudo group, and switch to the user. | `lazyown.py` |
| `do_grisun0w` | Creates and copies a PowerShell command to add a new user `grisun0`, assign a password, add the user to the Administrators group, and switch to the user. | `lazyown.py` |
| `do_ivy` | Generates payloads using Ivy with various options. Ivy is a payload creation framework for the execution of arbitrary VBA (macro) source code directly in memor… | `lazyown.py` |
| `do_knokknok` | Send special string to trigger a reverse shell, with the command 'c2 client_name' | `lazyown.py` |
| `do_listener_go` | Configures and starts a listener for a specified victim. | `lazyown.py` |
| `do_listener_py` | Configures and starts a listener for a specified victim. | `lazyown.py` |
| `do_msfpc` | Generates payloads using MSFvenom Payload Creator (MSFPC). | `lazyown.py` |
| `do_paranoid_meterpreter` | Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracking. | `lazyown.py` |
| `do_pwncat` | Runs `pwncat` with the specified port for listening. SELFINJECT | `lazyown.py` |
| `do_pwncatcs` | Runs `pwncat-cs` with the specified port for listening. | `lazyown.py` |
| `do_rdp` | Reads credentials from a file, encrypts the password, and executes the RDP connection command. | `lazyown.py` |
| `do_revwin` | Creates a base64 encoded PowerShell reverse shell payload specifically for Windows to execute a `.ps1` script from `lhost`. | `lazyown.py` |
| `do_scarecrow` | Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode. | `lazyown.py` |
| `do_service` | Creates a systemd service file for a specified binary and generates a script to enable and start the service. | `lazyown.py` |
| `do_setoolKits` | Executes the SEToolKit workflow to generate a Meterpreter payload | `lazyown.py` |
| `do_ssh` | Connects to an SSH host using credentials from a file and a specified port. | `lazyown.py` |
| `do_toctoc` | Sends a magic packet to the Chinese malware. | `lazyown.py` |
| `do_veil` | Generates payloads using Veil-Evasion with various options. Veil-Evasion is a payload creation framework | `lazyown.py` |
| `do_weevely` | Connect to PHP backdoor using Weevely, protected with the given password. | `lazyown.py` |
| `do_weevelygen` | Generate a PHP backdoor using Weevely, protected with the given password. | `lazyown.py` |

## Next Phase

After completing the Persist phase, proceed to:
**Credential Access** (`docs/cred.md`) or **Lateral Movement** (`docs/lateral.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

