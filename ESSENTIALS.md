# LazyOwn Essentials — The Commands You Actually Need

This is the 80/20 reference. 18 commands cover the majority of engagements. Everything else lives in `CHEATSHEET.md` and `COMMANDS.md`.

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
| 5 | `auto_populate` | Parse scan into structured data | Populates `sessions/world_model.json` with services, versions, OS |
| 6 | `facts_show` | Display discovered facts | Quick read of what the scan found: ports, services, versions |
| 7 | `recommend_next` | AI-ranked next steps | Groq suggests the 3-5 best commands for current phase |

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

## Where the full lists live

| Need | File |
|------|------|
| 40 most frequent commands by goal | `CHEATSHEET.md` |
| All 333 commands with descriptions | `COMMANDS.md` (auto-generated) |
| All 200+ aliases | `COMMANDS.md` alias section |
| Full MCP tool reference (131 tools) | `skills/lazyown.md` |
| Architecture and dev reference | `CLAUDE.md` |
