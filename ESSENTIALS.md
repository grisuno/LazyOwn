# LazyOwn Essentials — The Commands You Actually Need

This is the 80/20 reference. 18 commands cover the majority of engagements. Everything else lives in `CHEATSHEET.md` and `COMMANDS.md` (741 commands).

---

## The Golden Path (every engagement)

```
ping -> lazynmap -> auto_populate -> facts_show -> recommend_next
```

| # | Command | What it does | Why it matters |
|---|---------|--------------|----------------|
| 1 | `assign rhost 10.10.11.5` | Set target IP | Every command reads this from payload.json |
| 2 | `assign lhost 10.10.14.3` | Set your IP | Used by beacon callbacks, C2, payloads |
| 3 | `ping` | ICMP TTL probe | TTL ~64 = Linux, ~128 = Windows. Sets `os_id` automatically |
| 4 | `lazynmap` | Full port scan | Writes to `sessions/scan_<rhost>.nmap`. Never re-run if file exists |
| 5 | `auto_populate` | Parse scan into payload context | Fills `domain`, `os_id`, services and first creds from the nmap XML into `payload.json` |
| 6 | `facts_show` | Display discovered facts | Quick read of what the scan found: ports, services, versions (`--refresh` re-parses `sessions/`) |
| 7 | `recommend_next` | Ranked next steps | Local engine fuses policy + recon plan + knowledge graph into the 3-5 best commands for the current phase — no API key needed |

---

## One command — `engage`

When you just want a shell, `engage` runs the whole golden path for you:

```
engage 10.10.11.5
```

It chains `ping` → `lazynmap` → `auto_populate` → enum → exploit-search →
initial-access on the target, auto-switching to the next tool when a step
fails. With `auto_approve` false in `payload.json` it pauses at gated phases
for your go-ahead, so you stay in control. Useful flags:

| Flag | Effect |
|------|--------|
| `engage <ip> --background` | Detach into a worker; tail it with `engage --status` |
| `engage --pending` | List phases awaiting your approval |
| `engage --approve <id>` / `engage --deny <id>` | Resolve a pending gate |

Every action is narrated to `sessions/engagement.log` and broadcast to
connected teammates. Run the manual seven-step path above when you want to
understand or control each step; reach for `engage` when you want speed.

---

## One goal — `orchestrate`

`engage` walks a fixed chain. `orchestrate` hands a free-text goal to the
autonomous backends and lets them plan the steps:

```
orchestrate "gain initial access and dump hashes"
```

| Form | Effect |
|------|--------|
| `orchestrate "<goal>"` | Auto-routes to the best backend (daemon, hive or swan) |
| `orchestrate "<goal>" --mode daemon` | Force the objective-driven daemon (`auto_loop "<goal>"` is a shortcut for this) |
| `orchestrate "<goal>" --mode hive` | Queen/drone swarm with shared memory |
| `orchestrate "<goal>" --mode swan` | MoE+RL router, learns from outcomes |

The daemon backend is fully local and works offline. LLM-backed reasoning
uses `api_key` (Groq) when set and falls back to the local Ollama runtime
when it is not — if neither is available the shell tells you at startup
instead of failing silently.

---

## By Goal — not by phase

### I found a web service

| Command | What it does |
|---------|-------------|
| `ww` | whatweb fingerprint |
| `gobuster` | Directory brute-force (uses `rhost` + `dirwordlist`) |
| `ffuf` | Fast web fuzzer (uses `rhost` + `url`) |
| `finalrecon` | All-in-one web recon |
| `ss apache 2.4.49` | Search exploits for discovered version |

### I found SMB / Windows

| Command | What it does |
|---------|-------------|
| `enum4linux` | SMB/LDAP enumeration |
| `cme` | Crackmapexec (requires `domain` + `start_user`/`start_pass`) |
| `getnpusers` | AS-REP roasting |
| `secretsdump` | Dumps NTDS / SAM / LSA secrets (needs creds) |
| `bloodhound` | AD attack path mapping (needs creds) |
| `evil` | evil-winrm shell (needs creds) |
| `psexec` | Remote execution (needs creds) |

### I found Linux / SSH

| Command | What it does |
|---------|-------------|
| `ssh_cmd` | Run command over SSH (uses `rhost` + `start_user`/`start_pass`) |
| `scp` | File transfer over SSH |
| `linpeas` | Privilege escalation auto-checker |

### I need a shell / payload

| Command | What it does |
|---------|-------------|
| `venom` | Generate msfvenom payload (uses `lhost` + `lport` + `os_id`) |
| `msf` | Start metasploit handler |
| `createrevshell` | Reverse shell one-liner generator |
| `blacksandbeacon` | Compile C beacon with BOF support |

### I have credentials and want to move

| Command | What it does |
|---------|-------------|
| `secretsdump` | Extract hashes and secrets |
| `evil` | WinRM shell |
| `psexec` | Execute remotely |
| `bloodhound` | Map AD paths |

### I need situational awareness

| Command | What it does |
|---------|-------------|
| `creds` | Show captured credentials (`cat sessions/credentials*`) |
| `hash` | Show captured hashes (`cat sessions/hash*`) |
| `dashboard` | TUI with target, phase, commands, hints |
| `collab_join alice` | Team dashboard URL |

---

## The Three Rules

1. **Never write raw tool flags.** `lazynmap` auto-injects `rhost`. `gobuster` auto-injects `rhost`, `dirwordlist`. Always use the alias.
2. **Read `sessions/` before repeating work.** If `scan_<rhost>.nmap` exists, read it. Do not re-scan.
3. **Ping first, always.** OS detection determines the entire tool chain. AD tools against Linux is wasted time.

---

## New in v0.2.158 — Commands you should know

| Command | What it does | Why it matters |
|---------|--------------|----------------|
| `yara_marketplace list` | Browse 10 built-in YARA rules (ransomware, C2, webshells, privesc) | Signature-based threat detection |
| `nuclei_marketplace list` | Browse 500+ Nuclei templates | Automated vulnerability scanning |
| `auto_pwn` | Autonomous kill-chain walk | Recon to exploitation without manual steps |
| `hunt` | Threat-informed discovery | Maps known TTPs to discovered services |
| `yara_scan <file>` | Scan files/dirs with YARA rules | Malware and IoC detection |
| `nuclei` | Run Nuclei templates against rhost | CVD/CVE vulnerability scanning |
| `marketplace update` | Update all addons/plugins/tools/rules | Keep your toolkit current |
| `collab_join handle` | Print team dashboard URL | Multi-operator collaboration |
| `encrypt` / `decrypt` | PBKDF2HMAC + Fernet file crypto | Secure session data |
| `campaign_sitrep` | Full situation report | Current state at a glance |

---

## Where the full lists live

| Need | File |
|------|------|
| 50 frequent commands by goal | `CHEATSHEET.md` |
| All 741 commands with descriptions | `COMMANDS.md` (auto-generated) |
| All 126 aliases | `COMMANDS.md` alias section |
| Full MCP tool reference (153 tools) | `skills/lazyown.md` |
| Architecture and dev reference | `CLAUDE.md` |
| Honest framework comparison | `COMPARISON.md` |
