# Privesc Phase Guide

Privilege Escalation — elevate from standard user to root or SYSTEM by abusing misconfigurations or vulnerabilities.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_gtfo` | Look up a binary in GTFOBins / LOLBas and show exploitation techniques. | `lazyown.py` |
| `do_les` | Run Linux Exploit Suggester against the current target's kernel info. | `lazyown.py` |
| `do_linpeas` | Serve linpeas.sh via HTTP and print the one-liner to run on the target. | `lazyown.py` |
| `do_pspy` | Serve pspy (process spy without root) via HTTP for the target to download. | `lazyown.py` |
| `do_responder` | Runs Responder on a specified network interface with elevated privileges. | `lazyown.py` |
| `do_smbserver` | Sets up an SMB server using Impacket and creates an SCF file for SMB share access. | `lazyown.py` |
| `do_sudo` | Checks if the script is running with superuser (sudo) privileges, and if not, | `lazyown.py` |
| `do_suid_check` | Print SUID/SGID enumeration commands for the current target OS. | `lazyown.py` |
| `do_winpeas` | Serve winPEAS via HTTP and print the one-liner to run on the target. | `lazyown.py` |

## Next Phase

After completing the Privesc phase, proceed to:
**Post-Exploitation** (`docs/postexp.md`) or **Persistence** (`docs/persist.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

