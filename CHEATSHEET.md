# LazyOwn Cheatsheet — Frequent Commands by Goal

This is the second-level reference. Start with `ESSENTIALS.md` first. Use this when you need the next layer of detail. For the full 606+ command catalog, see `COMMANDS.md`.

---

## Configuration

| Goal | Command |
|------|---------|
| Set target IP | `assign rhost 10.10.11.5` |
| Set attacker IP | `assign lhost 10.10.14.3` |
| Set domain | `assign domain target.htb` |
| Set credentials | `assign start_user admin` / `assign start_pass Password123` |
| Guided setup | `wizard` |
| Check readiness | `wizard --check` |
| Read current config | `get` (shows payload.json) |

---

## Target Discovery and Recon

| Goal | Command |
|------|---------|
| Confirm target alive + OS guess | `ping` |
| Full TCP port scan | `lazynmap` |
| Batch scan a range | `batchnmap` |
| Host discovery sweep | `hosts_discover` |
| ARP scan local net | `arpscan` |
| Parse scan into structured data | `auto_populate` |
| See what was discovered | `facts_show` |
| AI recommends next step | `recommend_next` |

---

## Web Enumeration

| Goal | Command |
|------|---------|
| Fingerprint web tech | `ww` |
| Directory brute-force | `gobuster` |
| Fast web fuzzer | `ffuf` |
| Web vuln scan | `nikto` |
| Directory search | `dirsearch` |
| Web crawler | `gospider` |
| Full web recon | `finalrecon` |
| SQL injection test | `sqlmap` |
| Command injection test | `commix` |
| Web fuzzing | `wfuzz` |

---

## Network / DNS Enumeration

| Goal | Command |
|------|---------|
| DNS records / zone transfer | `dig` |
| DNS brute-force | `dnsenum` |
| Subdomain discovery | `get_all_domains` |

---

## SMB / LDAP / Active Directory

| Goal | Command |
|------|---------|
| SMB/LDAP enumeration | `enum4linux` |
| Crackmapexec SMB | `cme` |
| LDAP full dump | `ldapdomaindump` |
| AS-REP roasting | `getnpusers` |
| RID cycling | `nxcridbrute` |
| Bloodhound collection | `bloodhound` |
| Dump credentials | `secretsdump` |
| Remote WinRM shell | `evil` |
| Remote execution | `psexec` |
| NTLM relay | `ntlmrelayx` |
| Poison LLMNR/NBT-NS | `responder` |
| Coercion | `coerce_plus` |

---

## Exploitation

| Goal | Command |
|------|---------|
| Search multi-source exploits | `ss apache 2.4.49` |
| Generate payload | `venom` |
| Start metasploit handler | `msf` |
| Generate + deliver beacon | `lazymsfvenom` |
| Linux C beacon (BOF) | `blacksandbeacon` |
| ExploitGym harness readiness | `egym status` |
| List ExploitGym tasks | `egym list kernel --limit 5` |
| Run exploit benchmark task | `egym run cve-XXXX --model claude` |
| Score ExploitGym result (ELO) | `egym score cve-XXXX` |

---

## Post-Exploitation / Privilege Escalation

| Goal | Command |
|------|---------|
| Linux PE auto-check | `linpeas` |
| Windows PE auto-check | `winpeas` |
| Find capabilities | `getcap` |
| Show captured creds | `creds` |
| Show captured hashes | `hash` |
| Fix permissions | `fixperm` |

---

## Lateral Movement

| Goal | Command |
|------|---------|
| SSH command execution | `ssh_cmd` |
| SCP file transfer | `scp` |
| Interactive SMB | `smbclient` |
| Dump secrets remotely | `secretsdump` |
| WinRM shell | `evil` |
| PSExec remote exec | `psexec` |

---

## Marketplace, YARA & Nuclei

| Goal | Command |
|------|---------|
| Browse YARA rules | `yara_marketplace list` |
| Search YARA rules | `yara_marketplace search ransomware` |
| Install YARA rule | `yara_marketplace install ransomware_detection` |
| YARA rule info | `yara_marketplace info c2_framework_detection` |
| Browse Nuclei templates | `nuclei_marketplace list` |
| Search Nuclei by CVE | `nuclei_marketplace search --cve CVE-2024-xxxx` |
| Search Nuclei by severity | `nuclei_marketplace search --severity critical` |
| Install Nuclei template | `nuclei_marketplace install cve-2024-xxxx` |
| Scan target with YARA | `yara_scan /path/to/file` |
| Run Nuclei against rhost | `nuclei` |
| Browse community addons | `marketplace list` |
| Install community addon | `marketplace install <name>` |
| Update all marketplace items | `marketplace update` |

## Autonomous & Threat-Informed

| Goal | Command |
|------|---------|
| Autonomous kill chain | `auto_pwn` |
| Threat-informed recon | `hunt` |
| Chain commands | `chain` |
| Auto attack loop | `auto_loop` |
| Generate playbook | `playbook_generate` |
| Run playbook | `playbook_run` |

---

## C2 / Implant Management

| Goal | Command |
|------|---------|
| Start C2 server | `lazyc2` |
| Open C2 dashboard | `cc` |
| Team collaboration URL | `collab_join <handle>` |
| Download beacon | `download_c2` |
| Generate revshell | `createrevshell` |
| Generate webshell | `createwebshell` |
| Backdoor via netcat | `backdoor` |

---

## Reporting and Awareness

| Goal | Command |
|------|---------|
| Campaign sitrep | `campaign_sitrep` |
| Session state snapshot | `session_state` |
| List captured credentials | `credentials` |
| TUI dashboard | `dashboard` |
| Generate report | `report` |
| Red-team timeline | `timeline` |

---

## Autonomous / AI

| Goal | Command |
|------|---------|
| AI recommends next step | `recommend_next` |
| Autonomous attack loop | `auto_loop` |
| Generate playbook | `playbook_generate` |
| Run playbook | `playbook_run` |
| Query knowledge base | `parquet_query` |
| Semantic search sessions | `rag_query` |
| Threat model | `threat_model` |
| LLM daily cost cap | `llm_budget` |

---

## Security & Crypto

| Goal | Command |
|------|---------|
| Encrypt file | `encrypt <path> <key>` |
| Decrypt file | `decrypt <path> <key>` |
| YARA scan | `yara_scan <file>` |
| YARA marketplace | `yara_marketplace list` |
| Nuclei scan | `nuclei` |
| Nuclei marketplace | `nuclei_marketplace list` |
| AppLocker bypass | `applocker_bypass_csc` |
| EDR detection | `edr_detect` |
| DPAPI harvest | `dpapi_harvest` |
| MFA bypass toolkit | `mfa_bypass` |

---

## Command Abstraction Reminder

All commands above auto-inject values from `payload.json`. You never write:

```
nmap -sC -sV -p- 10.10.11.5
gobuster dir -u http://10.10.11.5 -w /usr/share/wordlists/dirbuster.txt
```

You write:

```
lazynmap
gobuster
```

The framework reads `rhost`, `wordlist`, `lhost`, `lport`, `domain`, `start_user`, `start_pass` from `payload.json` and builds the full command with optimal flags automatically.

---

## Progressive Documentation

| Level | File | Lines | Use when |
|-------|------|-------|----------|
| 1 | `ESSENTIALS.md` | ~120 | You are new or need the golden path |
| 2 | `CHEATSHEET.md` | ~300 | You know the basics, need the next layer |
| 3 | `QUICKSTART.md` | ~200 | Setting up for the first time |
| 4 | `COMMANDS.md` | ~1600 | You need the complete 606+ command reference |
| 5 | `skills/lazyown.md` | ~1600 | You are an AI operator using MCP tools |
| 6 | `CLAUDE.md` | ~540 | You are developing or extending the framework |
