# Lateral Phase Guide

Lateral Movement — traverse the network using valid credentials, tunnels or remote execution techniques.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_addcli` | Add a client to execute c2 commands | `lazyown.py` |
| `do_bloodyAD` | Execute the bloodyAD.py command for a specific user or all users listed in the users.txt file. | `lazyown.py` |
| `do_chisel` | Automates the setup and execution of Chisel server and client for tunneling and port forwarding. | `lazyown.py` |
| `do_dcomexec` | Executes the Impacket dcomexec tool to run commands on a remote system using DCOM. | `lazyown.py` |
| `do_getTGT` | Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided credentials. | `lazyown.py` |
| `do_gospherus` | Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads for various services. | `lazyown.py` |
| `do_id_rsa` | Create an SSH private key file and connect to a remote host using SSH. | `lazyown.py` |
| `do_lateral_mov_lin` | Perform lateral movement by downloading and installing LazyOwn on a remote Linux machine. | `lazyown.py` |
| `do_ligolo` | Automates the setup and execution of Ligolo server and client for tunneling and port forwarding. | `lazyown.py` |
| `do_mssqlcli` | Attempts to connect to an MSSQL server using the mssqlclient.py tool with Windows authentication. | `lazyown.py` |
| `do_nc` | Runs `nc` with the specified port for listening. | `lazyown.py` |
| `do_ngrok` | Set up and run ngrok on a specified local port. If ngrok is not installed, it will | `lazyown.py` |
| `do_penelope` | Command penelope: Installs and runs Penelope for handling reverse and bind shells. | `lazyown.py` |
| `do_regeorg` | Executes the reGeorg tool for HTTP(s) tunneling through a SOCKS proxy. | `lazyown.py` |
| `do_rnc` | Runs `nc` with rlwrap  the specified port for listening. | `lazyown.py` |
| `do_set_proxychains` | Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico | `lazyown.py` |
| `do_shadowsocks` | Execute the Shadowsocks tool to create a secure tunnel for network traffic. | `lazyown.py` |
| `do_socat` | Sets up and runs a `socat` tunnel with SOCKS4A proxy support. | `lazyown.py` |
| `do_sshd` | Starts the SSH service and displays its status. | `lazyown.py` |
| `do_stormbreaker` | Command stormbreaker: Automates the installation and usage of Storm-Breaker for performing various network attacks. | `lazyown.py` |
| `do_targetedKerberoas` | Executes the targetedKerberoast tool for extracting Kerberos service tickets. | `lazyown.py` |
| `do_tord` | Execute the tor.sh script with the specified port or default to port 80 if no port is provided. | `lazyown.py` |
| `do_upload_c2` | upload command in the client using the C2 to upload a file | `lazyown.py` |
| `do_vpn` | Connect to a VPN by selecting from available .ovpn files. | `lazyown.py` |
| `do_wifipass` | This function generates a PowerShell script that retrieves saved Wi-Fi passwords on a Windows system. | `lazyown.py` |
| `do_wmiexec` | Executes the Impacket WMIExec tool to run commands on a target system using WMI. | `lazyown.py` |
| `do_wmiexecpro` | Executes wmiexec-pro with various options for WMI operations. | `lazyown.py` |

## Next Phase

After completing the Lateral phase, proceed to:
**Exfiltration** (`docs/exfil.md`) or **Persistence** (`docs/persist.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

