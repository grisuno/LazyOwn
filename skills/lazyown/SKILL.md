---
name: lazyown
description: "LazyOwn RedTeam Framework — penetration testing and C2 via MCP"
version: 1.1.0
author: grisun0
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, pentest, c2, mcp, lazyown, security]
    homepage: https://github.com/grisuno/LazyOwn
    related_skills: [toposwarm]
---

# LazyOwn RedTeam Framework

You are operating the LazyOwn professional red-team framework via its MCP server.

- **Repo**: `/home/grisun0/LazyOwn`
- **MCP entry**: `skills/lazyown_mcp.py` (~95 tools)
- **Shell**: `./run` → `lazyown.py` (333+ commands, 200+ aliases)
- **State**: `payload.json` (config) + `sessions/` (campaign artefacts)

---

## The LazyOwn Soul

Read `soul.md` at the start of every engagement. It defines the operating philosophy: evidence over assumption, abstraction over mechanics, phase discipline, situational awareness first, the 80/20 rule, document for the next shift, ask the machine when uncertain, professional over theatrical, configuration is code, collaboration is not optional.

Ten hard stops are listed there. No exceptions.

---

## Every Session Starts Here

```python
# 1. Situation report — reads world_model, tasks, objectives, creds, daemon
lazyown_campaign_sitrep()

# 2. Session init — checks scans, pwntomate, phase, objectives
lazyown_session_init()
```

**Do not re-run nmap or pwntomate if `sessions/scan_<rhost>.nmap` already exists.**

---

## The Golden Path

```python
# 1. Configure target
lazyown_set_config(key="rhost", value="10.10.11.5")
lazyown_set_config(key="domain", value="target.htb")

# 2. OS detection — TTL ~64 = Linux, ~128 = Windows
lazyown_run_command("ping")

# 3. Full port scan (auto-injects rhost)
lazyown_run_command("lazynmap")

# 4. Parse results into structured state
lazyown_auto_populate(target="10.10.11.5")
lazyown_facts_show(target="10.10.11.5")

# 5. AI-ranked next steps
lazyown_recommend_next()
```

---

## The One Rule

LazyOwn commands are **high-level abstractions** that auto-inject values from `payload.json`. **Never write raw tool flags.**

```python
# CORRECT — payload.json supplies rhost, wordlist, etc.
lazyown_run_command("lazynmap")
lazyown_run_command("gobuster")
lazyown_run_command("secretsdump")

# WRONG — never do this
nmap -sC -sV -p- 10.10.11.5
gobuster dir -u http://10.10.11.5 -w /usr/share/wordlists/dirbuster.txt
```

---

## Seven Tools You Need

| Tool | When to use |
|------|-------------|
| `lazyown_campaign_sitrep` | Start of every shift. Aggregates all campaign state into one briefing |
| `lazyown_session_init` | Start of every session. Checks existing scans, phase, objectives |
| `lazyown_set_config` | Set target, attacker IP, domain, credentials |
| `lazyown_run_command` | Execute any LazyOwn shell command (alias auto-injects payload.json values) |
| `lazyown_auto_populate` | After any nmap scan — parses XML into structured world_model |
| `lazyown_facts_show` | After auto_populate — displays discovered ports, services, versions |
| `lazyown_recommend_next` | When unsure what to do next — Groq ranks 3-5 next commands |

---

## Three Rules

1. **Read `sessions/` before any tool.** Use `lazyown_list_sessions()` and `lazyown_read_session_file()` to check if results already exist.
2. **Identify OS before enumeration.** `ping` first. Never run AD tools against Linux or SSH brute against Windows.
3. **Use abstract commands.** Never write raw flags when a LazyOwn alias exists.

---

## Progressive Documentation

| Level | File | Purpose |
|-------|------|---------|
| 1 | `ESSENTIALS.md` | 18 commands that cover 80% of engagements |
| 2 | `CHEATSHEET.md` | ~40 frequent commands grouped by user goal |
| 3 | `QUICKSTART.md` | First-time setup and onboarding |
| 4 | `skills/lazyown.md` | Complete 95-tool MCP playbook |
| 5 | `COMMANDS.md` | Full 333-command reference (auto-generated) |
| 6 | `CLAUDE.md` | Architecture and developer reference |

---

## Setup

```bash
# 1. Clone and install
git clone https://github.com/grisuno/LazyOwn.git
cd LazyOwn
bash install.sh

# 2. Register MCP server in Hermes
bash scripts/setup_hermes_mcp.sh

# 3. Restart Hermes session or run /reload-mcp
```
