# MITRE ATT&CK Coverage Matrix

Mapping of LazyOwn capabilities to MITRE ATT&CK Enterprise tactics and
techniques. Updated 2026-05-17. The intent is honesty, not credit: a row
without strong evidence is marked `partial` or `none`, never `yes`.

Verify a claim by running the listed command, addon, or skill and observing
that the artefact lands in `sessions/`. If a row is wrong, open an issue
with the failing reproducer.

Categories below mirror the kill-chain layout used by the CLI
(`utils.py:recon_category` and friends). Each LazyOwn category maps onto
one or more ATT&CK tactics.

---

## TA0043 — Reconnaissance

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Active Scanning: Scanning IP Blocks | T1595.001 | `do_lazynmap`, `do_amass`, `do_arpscan` | yes |
| Active Scanning: Vulnerability Scanning | T1595.002 | `do_nikto`, `do_wpscan`, `modules/integrations/nuclei_bridge.py` | yes |
| Gather Victim Host Information | T1592 | `do_enum4linux`, `do_enum4linux_ng` | yes |
| Search Open Websites/Domains | T1593 | `do_amass`, OSINT skills | partial |
| Search Open Technical Databases | T1596 | `find_ss`, `find_ea`, `nvddb`, `packetstormsecurity` | yes |
| Phishing for Information | T1598 | phishing blueprint + SMTP tracker | yes |

## TA0042 — Resource Development

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Acquire Infrastructure: Domains | T1583.001 | manual; documented in QUICKSTART | none |
| Develop Capabilities: Malware | T1587.001 | Go beacon, BlackSandBeacon, Windows beacon addon | yes |
| Develop Capabilities: Code Signing Certificates | T1587.002 | `gen_cert.sh`, `generate_certificates()` | partial |
| Obtain Capabilities: Exploits | T1588.005 | `searchsploit`, ExploitAlert scrapers | yes |
| Stage Capabilities: Upload Malware | T1608.001 | C2 staging routes, `sessions/<artefact>` | yes |
| Stage Capabilities: Drive-by Target | T1608.004 | decoy site + landing pages | yes |

## TA0001 — Initial Access

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Phishing: Spearphishing Link | T1566.002 | phishing blueprint + tracker | yes |
| Phishing: Spearphishing Attachment | T1566.001 | phishing blueprint with attachment templates | yes |
| Drive-by Compromise | T1189 | landing pages + decoy capture | partial |
| Exploit Public-Facing Application | T1190 | `do_sqlmap`, `do_nikto`, `do_wpscan` | yes |
| Valid Accounts | T1078 | `start_user` / `start_pass` payload keys, `do_hydra` | yes |
| External Remote Services | T1133 | RDP/SSH probing via nmap and `do_responder` | partial |

## TA0002 — Execution

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Command and Scripting Interpreter: Bash | T1059.004 | beacon + `do_run` | yes |
| Command and Scripting Interpreter: PowerShell | T1059.001 | `do_empire`, Windows beacon | yes |
| Command and Scripting Interpreter: Python | T1059.006 | impacket suite | yes |
| Native API | T1106 | Windows beacon NT API, BlackSandBeacon direct syscalls | yes |
| Inter-Process Communication | T1559 | BOF runtime + Unix sockets | partial |
| User Execution: Malicious File | T1204.002 | phishing payload templates | yes |

## TA0003 — Persistence

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Account Manipulation | T1098 | post-exploitation utilities | partial |
| Boot or Logon Autostart Execution | T1547 | `modules/rootkit/`, addons | partial |
| Scheduled Task/Job | T1053 | `do_cron` | yes |
| Server Software Component: Web Shell | T1505.003 | reverse-shell generators | yes |
| Create or Modify System Process | T1543 | `modules/rootkit/` Linux LKM | yes |

## TA0004 — Privilege Escalation

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Abuse Elevation Control Mechanism: Sudo | T1548.003 | GTFOBins parquet KB | yes |
| Exploitation for Privilege Escalation | T1068 | `searchsploit` integration, reactive_engine | yes |
| Process Injection | T1055 | Windows beacon Early Bird APC | yes |
| Setuid and Setgid | T1548.001 | GTFOBins parquet KB | yes |

## TA0005 — Defense Evasion

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Obfuscated Files or Information | T1027 | Go beacon Garble obfuscation, XOR stub | yes |
| Indicator Removal: File Deletion | T1070.004 | manual (no first-class surface) | none |
| Masquerading | T1036 | decoy site, malleable C2 user-agents | yes |
| Reflective Code Loading | T1620 | Windows BOF + Linux BOF dlopen | yes |
| Direct Volume Access / Direct Syscalls | T1006 | BlackSandBeacon direct syscalls | yes |
| Use Alternate Authentication Material | T1550 | Kerberos relay tooling | partial |

## TA0006 — Credential Access

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| OS Credential Dumping: LSASS Memory | T1003.001 | `do_mimikatzpy` | yes |
| OS Credential Dumping: NTDS | T1003.003 | impacket secretsdump | yes |
| OS Credential Dumping: /etc/shadow | T1003.008 | post-exploitation utilities | yes |
| Brute Force: Password Cracking | T1110.002 | `do_john2hash`, `do_hashcat` | yes |
| Brute Force: Credential Stuffing | T1110.004 | `do_hydra` | yes |
| Credentials from Password Stores | T1555 | `do_john2keepas`, browser addons | partial |
| Steal or Forge Kerberos Tickets | T1558 | impacket suite | yes |
| Adversary-in-the-Middle: LLMNR Poisoning | T1557.001 | `do_responder` | yes |

## TA0007 — Discovery

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Account Discovery | T1087 | `do_enum4linux`, AD enumeration | yes |
| Domain Trust Discovery | T1482 | `do_bloodhound` | yes |
| Network Share Discovery | T1135 | impacket smbclient | yes |
| Network Service Discovery | T1046 | `do_lazynmap` | yes |
| Permission Groups Discovery | T1069 | BloodHound | yes |
| Process Discovery | T1057 | post-exploitation utilities | yes |
| Remote System Discovery | T1018 | network_discovery, `do_lazynmap` | yes |
| System Information Discovery | T1082 | `auto_populate` | yes |

## TA0008 — Lateral Movement

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Remote Services: SMB/Windows Admin Shares | T1021.002 | `do_psexec`, `do_psexec_py` | yes |
| Remote Services: WinRM | T1021.006 | `do_evilwinrm` | yes |
| Remote Services: SSH | T1021.004 | beacon SSH module | yes |
| Use Alternate Authentication Material: Pass the Hash | T1550.002 | impacket suite | yes |
| Lateral Tool Transfer | T1570 | `do_chisel`, `do_socat`, `do_ligolo` | yes |

## TA0009 — Collection

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Audio Capture | T1123 | decoy site capture | partial |
| Video Capture | T1125 | decoy site capture | partial |
| Data from Local System | T1005 | beacon download command | yes |
| Data from Network Shared Drive | T1039 | impacket suite | yes |
| Screen Capture | T1113 | `do_eyewitness`, `do_gowitness` (operator-side, web only) | partial |

## TA0011 — Command and Control

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Application Layer Protocol: Web Protocols | T1071.001 | Flask C2 + malleable profile | yes |
| Application Layer Protocol: DNS | T1071.004 | built-in `dnslib` resolver | yes |
| Data Encoding: Standard Encoding | T1132.001 | beacon JSON + base64 | yes |
| Data Obfuscation | T1001 | XOR stub, AES-256 channel | yes |
| Dynamic Resolution: Domain Generation Algorithms | T1568.002 | manual | none |
| Encrypted Channel: Symmetric Cryptography | T1573.001 | AES-256 beacon channel | yes |
| Encrypted Channel: Asymmetric Cryptography | T1573.002 | TLS via `gen_cert.sh` | yes |
| Fallback Channels | T1008 | short-URL beacon routes | yes |
| Ingress Tool Transfer | T1105 | C2 staging endpoints | yes |
| Proxy: Internal Proxy | T1090.001 | `do_chisel`, `do_ligolo`, `do_socat` | yes |
| Proxy: Multi-hop Proxy | T1090.003 | chained chisel + ligolo | partial |
| Web Service | T1102 | decoy site fallthrough | partial |

## TA0010 — Exfiltration

| Technique | ATT&CK ID | LazyOwn surface | Status |
|---|---|---|---|
| Exfiltration Over C2 Channel | T1041 | beacon upload command | yes |
| Exfiltration Over Alternative Protocol: DNS | T1048.003 | DNS resolver | partial |
| Exfiltration Over Web Service: Cloud Storage | T1567.002 | manual | none |
| Scheduled Transfer | T1029 | scheduling addons | partial |

## TA0040 — Impact

LazyOwn does not implement destructive impact techniques (T1485 data
destruction, T1486 ransomware, T1490 inhibit system recovery, T1499
endpoint DoS, T1496 resource hijacking). These belong to malicious actors
and are out of scope for an authorised red-team framework. Requests to add
them will be rejected.

---

## Adversary emulation profiles

`playbooks/` ships seven named-actor YAML profiles: `apt_apt28.yaml`,
`apt_apt29.yaml`, `apt_apt41.yaml`, `apt_conti.yaml`, `apt_fin7.yaml`,
`apt_lazarus.yaml`, `apt_lockbit.yaml`. Each maps a sequence of LazyOwn
commands onto MITRE technique IDs so an operator can replay a campaign
end-to-end for purple-team validation. Separately, `lazyadversaries/`
holds technique-level building blocks (AMSI, persistence, shellcode
injection) that the playbooks compose.

Run a profile with:

```
playbook_generate <profile>
playbook_run <profile>
```

The reward shaping in `skills/autonomous_daemon.py` scores each step
against the technique it was tagged with, so detection telemetry can be
correlated back to ATT&CK directly.

---

## What this matrix is not

- It is **not** a guarantee that every technique works against every target
  out of the box. Many require operator judgement (correct OS, correct
  privilege, correct service version).
- It is **not** a substitute for reading the relevant `do_*` docstring,
  addon YAML, or `parquets/` knowledge base.
- It is **not** updated automatically. When you add a `do_*` covering a new
  technique, edit the table in the same change. A row added here without
  a working command will be removed at review.
