# Enum Phase Guide

Enumeration — interrogate discovered services, map shares, users and attack surface after initial access.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_ad_ldap_enum` | Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers) | `lazyown.py` |
| `do_allin` | Execute the AlliN.py tool with various scan modes and parameters. | `lazyown.py` |
| `do_amass` | Executes Amass to perform a passive enumeration on a given domain. | `cli/commands/scan.py` |
| `do_arjun` | Executes an Arjun scan on the specified URL for parameter discovery. | `lazyown.py` |
| `do_arpscan` | Executes an ARP scan using `arp-scan`. | `cli/commands/scan.py` |
| `do_batchnmap` | Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans. | `cli/commands/recon.py` |
| `do_bbot` | Executes a BBOT scan to perform various reconnaissance tasks. | `cli/commands/scan.py` |
| `do_blazy` | Command blazy: Installs and runs blazy for multi-vulnerability web application scanning. | `lazyown.py` |
| `do_bloodhound` | Perform LDAP enumeration using bloodhound-python with credentials from a file. | `lazyown.py` |
| `do_breacher` | Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities. | `lazyown.py` |
| `do_certipy` | Executes the Certipy tool to interact with Active Directory Certificate Services. | `lazyown.py` |
| `do_certipy_ad` |  | `lazyown.py` |
| `do_changeme` | Executes a changeme scan on a specified target URL or host. | `lazyown.py` |
| `do_cme` | Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target. | `lazyown.py` |
| `do_davtest` | Tests WebDAV server configurations using `davtest`. | `lazyown.py` |
| `do_dirsearch` | Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL. | `cli/commands/scan.py` |
| `do_dmitry` | This function constructs and executes a command for the 'dmitry' tool. | `cli/commands/scan.py` |
| `do_enum4linux` | Performs enumeration of information from a target Linux/Unix system using `enum4linux`. | `cli/commands/enum.py` |
| `do_enum4linux_ng` | Performs enumeration of information from a target system using `enum4linux-ng`. | `lazyown.py` |
| `do_evil_ssdp` | Runs evil-ssdp with various options and user-selected templates. | `lazyown.py` |
| `do_feroxbuster` | Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing. | `cli/commands/scan.py` |
| `do_finger_user_enum` | Executes the `finger-user-enum` tool for enumerating users on the target host. | `lazyown.py` |
| `do_fuzz` | Executes a web server fuzzing script with user-provided parameters. | `lazyown.py` |
| `do_getnpusers` | sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt | `cli/commands/enum.py` |
| `do_gobuster` | Uses `gobuster` for directory and virtual host fuzzing based on provided parameters. Supports directory enumeration and virtual host discovery. | `cli/commands/scan.py` |
| `do_hostdiscover` | Discover active hosts in a subnet by performing a ping sweep. | `cli/commands/scan.py` |
| `do_hound` | Executes the hound tool for Hound is a simple and light tool for information gathering and capture exact GPS coordinates | `lazyown.py` |
| `do_kerbrute` | Executes the Kerbrute tool to enumerate user accounts against a specified target domain controller. | `lazyown.py` |
| `do_lazynmap` | Runs the internal module `modules/lazynmap.sh` with target mode. | `cli/commands/recon.py` |
| `do_ldapdomaindump` | Dumps LDAP information using `ldapdomaindump` with credentials from a file. | `lazyown.py` |
| `do_ldapsearch` | Executes an LDAP search against a target remote host (rhost) and saves the results. | `lazyown.py` |
| `do_lookupsid` | Executes the Impacket lookupsid tool to enumerate SIDs on a target system. | `lazyown.py` |
| `do_lookupsid_py` | Executes the LookupSID tool to perform SID enumeration on a target system. | `lazyown.py` |
| `do_loxs` | Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning. | `lazyown.py` |
| `do_lynis` | Performs a Lynis audit on the specified remote system. | `lazyown.py` |
| `do_magicrecon` | Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and vulnerability scanning on specified targets. | `cli/commands/scan.py` |
| `do_mqtt_check_py` | Executes the MQTT check tool to verify credentials on a target system with optional SSL. | `lazyown.py` |
| `do_nbtscan` | Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range. | `cli/commands/recon.py` |
| `do_net_rpc_addmem` | Executes the net rpc group addmem command to add a user to a specified group in Active Directory. | `lazyown.py` |
| `do_netexec` | Executes netexec with various options for network protocol operations. | `lazyown.py` |
| `do_netview` | Executes the Impacket netview tool to list network shares on a specified target. | `lazyown.py` |
| `do_nikto` | Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host. | `cli/commands/recon.py` |
| `do_nmapscript` | Perform an Nmap scan using a specified script and port. | `cli/commands/scan.py` |
| `do_nuclei` | Executes a Nuclei scan on a specified target URL or host. | `cli/commands/scan.py` |
| `do_odat` | Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database. | `lazyown.py` |
| `do_openredirex` | Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities. | `lazyown.py` |
| `do_osmedeus` | Executes Osmedeus scans with guided input for various scanning scenarios. | `cli/commands/scan.py` |
| `do_parsero` | Executes a parsero scan on a specified target URL or host. | `lazyown.py` |
| `do_parth` | Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters. | `lazyown.py` |
| `do_portdiscover` | Scan all ports on a specified host to identify open ports. | `cli/commands/scan.py` |
| `do_portservicediscover` | Scan all ports on a specified host to identify open ports and associated services. | `cli/commands/scan.py` |
| `do_pre2k` | Executes the pre2k tool to query the domain for pre-Windows 2000 machine accounts or to pass a list of hostnames to test authentication. | `lazyown.py` |
| `do_pykerbrute` | Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory accounts using Kerberos pre-authentication. | `lazyown.py` |
| `do_rdp_check_py` | Executes the RDP check tool to verify credentials or hash-based authentication on a target system. | `lazyown.py` |
| `do_rpcclient` | Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using anonymous credentials. | `cli/commands/enum.py` |
| `do_rpcdump` | Executes the `rpcdump.py` script to dump RPC services from a target host. | `cli/commands/enum.py` |
| `do_rpcmap_py` | Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces. | `lazyown.py` |
| `do_samrdump` | Run `impacket-samrdump` to dump SAM data from specified ports. | `lazyown.py` |
| `do_sawks` | Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phishing simulations. | `lazyown.py` |
| `do_sessionssh` | Ejecuta un comando para listar las conexiones SSH activas. | `lazyown.py` |
| `do_skipfish` | This function executes the web security scanning tool Skipfish | `cli/commands/scan.py` |
| `do_smbattack` | Scans for hosts with SMB service open on port 445 in the specified target network. | `lazyown.py` |
| `do_smbclient` | Interacts with SMB shares using the `smbclient` command to perform the following operations: | `cli/commands/enum.py` |
| `do_smbclient_impacket` | Interacts with SMB shares using the `smbclient` command to perform the following operations: | `cli/commands/enum.py` |
| `do_smbclient_py` | Interacts with SMB shares using the `smbclient.py` command to perform the following operations: | `cli/commands/enum.py` |
| `do_smbmap` | smbmap -H 10.10.10.3 [OPTIONS] | `cli/commands/enum.py` |
| `do_smtpuserenum` | Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method. | `lazyown.py` |
| `do_snmpcheck` | Performs an SNMP check on the specified target host. | `lazyown.py` |
| `do_snmpwalk` | Performs an SNMP check on the specified target host. | `lazyown.py` |
| `do_swaks` | Sends an email using `swaks` (Swiss Army Knife for SMTP). | `lazyown.py` |
| `do_vscan` | Perform port scanning using vscan with the provided parameters. | `cli/commands/scan.py` |
| `do_wfuzz` | Uses `wfuzz` to perform fuzzing based on provided parameters. This function supports various options for directory and file fuzzing. | `cli/commands/recon.py` |
| `do_windapsearch` | Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries. | `lazyown.py` |
| `do_wpscan` | Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning. | `lazyown.py` |

## Next Phase

After completing the Enum phase, proceed to:
**Exploitation** (`docs/exploit.md`) or **Credential Access** (`docs/cred.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

