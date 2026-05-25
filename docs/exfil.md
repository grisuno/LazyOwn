# Exfil Phase Guide

Exfiltration — extract data, logs or loot from the target environment to the operator-controlled infrastructure.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_adgetpass` | Command adgetpass: Generates a PowerShell script to extract credentials from Azure AD Connect Sync. | `lazyown.py` |
| `do_decrypt` | Decrypts a file using XOR encryption. | `lazyown.py` |
| `do_download_c2` | Download a file from the command and control (C2) server. | `lazyown.py` |
| `do_dploot` | Executes the dploot tool to loot DPAPI related secrets from local or remote targets. | `lazyown.py` |
| `do_encrypt` | Encrypts a file using XOR encryption. | `lazyown.py` |
| `do_evidence` | Compresses the 'sessions' folder and encodes it into a video using the lazyown_infinitestorage.py script. | `lazyown.py` |
| `do_evilwinrm` | Execute the Evil-WinRM tool for authentication attempts on a specified target using either password or hash. | `lazyown.py` |
| `do_getadusers` | Executes the GetADUsers.py script to retrieve Active Directory users. | `lazyown.py` |
| `do_getnthash_py` | Executes the getnthash.py tool from PKINITtools to retrieve the NT hash using a Kerberos U2U TGS request. | `lazyown.py` |
| `do_getuserspns` | Run GetUserSPNs.py with the provided domain, username, password, and IP address. | `lazyown.py` |
| `do_gitdumper` | Install and execute the git-dumper tool to download Git repository content. | `lazyown.py` |
| `do_gmsadumper` | Executes the gMSADumper tool to read and parse gMSA password blobs accessible by the user. | `lazyown.py` |
| `do_reg_py` | Run reg.py with specified parameters to query the registry. | `lazyown.py` |
| `do_rsync` | Synchronizes the local "sessions" directory to a remote host using rsync, leveraging sshpass for automated authentication. | `lazyown.py` |
| `do_samdump2` | Run samdump2 with the SAM and SYSTEM file | `lazyown.py` |
| `do_secretsdump` | Run secretsdump.py with the provided domain, username, password, and IP address. | `lazyown.py` |
| `do_unzip` | Unzips a specified file from the sessions directory. | `lazyown.py` |
| `do_upload_gofile` | Uploads a file to Gofile storage. | `lazyown.py` |

## Next Phase

After completing the Exfil phase, proceed to:
**Reporting** (`docs/report.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

