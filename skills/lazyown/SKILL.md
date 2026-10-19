---
name: lazyown
description: "LazyOwn RedTeam Framework — penetration testing and C2 via MCP"
version: 1.1.0
author: grisun0
license: AGPL-3.0-only
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, pentest, c2, mcp, lazyown, security]
    homepage: https://github.com/grisuno/LazyOwn
    related_skills: [toposwarm]
---

# LazyOwn RedTeam Framework

You are operating the LazyOwn professional red-team framework via its MCP server.

- **Repo**: the current working directory (the checkout that holds `payload.json`)
- **MCP entry**: `skills/lazyown_mcp.py` (~131 tools)
- **Shell**: `./run` → `lazyown.py` (724+ commands, 126 aliases)
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

## Calling The MCP From An Agent — No Ad-Hoc Drivers

Agents MUST call the MCP server through the shipped stdio client — never by
writing throwaway drivers or pasted snippets in `/tmp`, and never by
executing attack tooling by hand from the agent shell.

```bash
# One tool call (exit 0 = answer, 1 tool-error, 4 transport/timeout, 3 no mcp package)
python3 scripts/mcp_call.py lazyown_campaign_sitrep '{"format":"json"}' --timeout 150

# Debug a server-side crash (server stderr captured, agent stderr separate)
python3 scripts/mcp_call.py lazyown_auto_loop '{...}' --timeout 900 \
    --server-stderr sessions/mcp_server_stderr.log
```

Contract enforced by `scripts/mcp_call.py`:

- Repository and virtualenv (`env/`, `venv`, `.venv`) are resolved from the
  script location — no user-specific absolute paths anywhere.
- Parent env flows to the server (`AUTO_USE_LLM=1`, `AUTO_USE_SWAN=1`,
  credentials, master password).
- Server is spawned per call; long chains are acceptable, keep `--timeout`
  larger than the longest step (`lazyown_run_command` takes its own
  `timeout` argument in the JSON payload).

Operating discipline:

1. Every action against a target goes through an MCP tool call — `apt_chain`,
   the atomic sweep and the autonomous loop included (via
   `lazyown_run_command`).
2. Never re-implement exploit logic inside the agent session (`nc`,
   `msfconsole`, `sshpass`, `python -c` probes are forbidden).
3. Evidence lives under `sessions/` — `sessions/chains/*.json` for chain runs,
   `sessions/atomic_exploit_<target>_*.json` for sweeps, `lazy_finding list
   --task <id>` for loop outcome.

---

## Metasploitable 2 Gym — Standard Flow

```python
# 0. Consistency check (index playbook vs chains vs exploits)
lazyown_run_command("gym_ms2 validate")

# 1. Lab services: docker image auto-starts only rmi/irc/vnc/druby;
#    the full surface needs the standard MS2 daemons before scanning.
# 2. Configure + scan once
lazyown_set_config(key="rhost", value="<lab-ip>")
lazyown_run_command("lazynmap")          # writes sessions/scan_<rhost>.nmap.xml

# 3. Chain per vector (45 indexed vulnerabilities, 1 chain each)
lazyown_run_command("apt_chain gym_metasploitable_ms2_<id> <lab-ip> --json")

# 4. Sweep everything (pwntomate-style, from scan XML)
lazyown_run_command(
    "python3 modules/atomic_exploit_bridge.py auto --target <lab-ip>"
    " --max-attempts 40 --no-stop"
)

# 5. Autonomous loop + evidence
#    lazyown_auto_loop(target=..., max_steps=8, stop_on_high_value_success=false)
```

The matrix (45 vectors) is validated by `modules/metasploitable_gym.py`:
PHASE discipline still applies; the vsftpd root backdoor alone is never an
acceptable engagement outcome.

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
| 4 | `skills/lazyown.md` | Complete 131-tool MCP playbook |
| 5 | `COMMANDS.md` | Full 333-command reference (auto-generated) |
| 6 | `CLAUDE.md` | Architecture and developer reference |

---

## Branching Model

LazyOwn uses three branches. As an autonomous agent, you operate on `dev`.

| Branch | Purpose | Your role |
|--------|---------|-----------|
| `dev`  | Active development, feature integration, daily commits. | **You work here.** |
| `pp`   | Pre-production / staging. QA and integration tests. | Read-only. Human approves promotion from `dev`. |
| `main` | Production releases. Tagged releases only. | Read-only. `DEPLOY.sh` runs here. |

### Rules

- Start every session on `dev` (`git checkout dev`).
- Never commit directly to `main` or `pp`.
- Feature branches: `feature/<description>` cut from `dev`.
- Hotfix branches: `hotfix/<description>` cut from `main`, then back-merge to `pp` and `dev`.
- When asked to release, create a PR and request human approval.

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
