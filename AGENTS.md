# LazyOwn — Hermes Agent Context

Project: LazyOwn RedTeam Framework
Repo: /home/grisun0/LazyOwn
Language: Python 3.11+, Bash
Domain: penetration testing, red teaming, C2 operations

---

## What this project is

LazyOwn is a professional pentest/red-team framework:

- **CLI** (`lazyown.py`): cmd2 shell with 333+ commands and 200+ aliases covering the full kill chain.
- **C2** (`lazyc2.py`): Flask + Socket.IO web dashboard, beacon protocol, phishing, multi-operator collaboration.
- **MCP** (`skills/lazyown_mcp.py`): ~131 tools exposing the framework to AI agents.

All configuration lives in `payload.json`. All campaign state lives in `sessions/` (gitignored, never delete without confirmation).

---

## Architecture

```
Hermes Agent -> MCP -> skills/lazyown_mcp.py -> lazyown.py (CLI) / lazyc2.py (C2)
                                   |
                            payload.json (config)
                                   |
                            sessions/ (state)
```

- `utils.py`: shared helpers, Config class, run_command wrapper. Imported by both CLI and C2.
- `skills/`: MCP server, autonomous daemon, hive mind, SWAN (MoE+RL), policy engine, parquet DB.
- `modules/`: LLM clients, blueprints, world model, playbook engine.
- `parquets/`: columnar knowledge bases (GTFOBins, LOLBas, MITRE ATT&CK).
- `lazyaddons/`: 76 YAML tool integrations. `plugins/`: Lua plugins. `tools/`: pwntomate auto-jobs.

---

## Coding standards (check before editing)

1. English only — identifiers, strings, logs, docstrings.
2. No comments — self-explanatory names + docstrings only.
3. No emojis in code/logs/docs (banners excepted).
4. Docstrings on every public function/class (Args/Returns/Raises).
5. No magic numbers — constants in Config or UPPER_SNAKE_CASE module-level.
6. No hardcoded paths/ports/IPs/wordlists/creds — use `payload.json`.
7. SOLID: single responsibility, open for extension, Liskov-compatible selectors, small interfaces, depend on abstractions.
8. Every new directory gets a `README.md` immediately.

---

## How to add a new CLI command

1. Add `do_<name>(self, line)` near related commands in `lazyown.py`.
2. Read inputs from `self.params` (payload.json) — never accept rhost/lhost as positional args when in payload.
3. Validate with `check_rhost` / `check_lhost` / `check_lport` from `utils.py`.
4. Execute via `run_command(cmd_str)` — captures output, strips ANSI, CSV-logs.
5. Write artefacts to `sessions/...` with stable filenames.
6. Add one natural short alias (or none).
7. If the command has a kill-chain phase, add it to the bridge catalog so `auto_loop` sees it.

Do NOT import `lazyc2` from CLI. Do NOT write to `payload.json` outside `do_assign` / `do_set` / `lazyown_set_config`.

---

## Hermes integration

### Loading this skill

```bash
# Option A: install from repo
hermes skills install /home/grisun0/LazyOwn/skills/lazyown/SKILL.md

# Option B: auto-discovered via AGENTS.md when cwd is /home/grisun0/LazyOwn
```

### The LazyOwn Soul

Read `soul.md` at the start of every engagement. It is the operating philosophy — not documentation, not rules, but the spirit that guides every decision.

```bash
cat soul.md
```

Key principles: evidence over assumption, abstraction over mechanics, phase discipline, situational awareness first, the 80/20 rule, document for the next shift, ask the machine when uncertain, professional over theatrical, configuration is code, collaboration is not optional.

### MCP registration

```bash
bash /home/grisun0/LazyOwn/scripts/setup_hermes_mcp.sh
```

### Key files Hermes should read

| File | When | Why |
|------|------|-----|
| `payload.json` | Every turn | Active config — rhost, lhost, domain, creds, flags |
| `sessions/scan_<rhost>.nmap` | Before recon | Prior scan results — never re-run if exists |
| `sessions/world_model.json` | Before decisions | Current phase, discovered hosts, creds, access level |
| `sessions/objectives.jsonl` | Before planning | Active attack objectives queue |
| `sessions/credentials*.txt` | Before lateral/privesc | Captured creds for target |

---

## Essential MCP tools (7)

| Tool | When to use |
|------|-------------|
| `lazyown_campaign_sitrep` | Start of every shift. Aggregates all campaign state |
| `lazyown_session_init` | Start of every session. Checks scans, phase, objectives |
| `lazyown_set_config` | Set target, attacker IP, domain, credentials |
| `lazyown_run_command` | Execute any LazyOwn shell command (alias auto-injects payload.json) |
| `lazyown_auto_populate` | After any nmap scan — parses XML into world_model |
| `lazyown_facts_show` | After auto_populate — displays discovered ports, services, versions |
| `lazyown_recommend_next` | When unsure what to do — Groq ranks 3-5 next commands |

For the full 95-tool reference see `skills/lazyown.md`.

---

## Hermes-native workflows

- Use `todo` tool to track objectives derived from `lazyown_inject_objective`.
- Use `delegate_task` for parallel research (CVE analysis, exploit search, OSINT).
- Use `cronjob` for scheduled recon scans or beacon health checks.
- Use `session_search` to recall past LazyOwn sessions and avoid repeating failed approaches.

---

## Troubleshooting

**MCP tools not appearing**: run `/reload-mcp` or restart Hermes session.

**LazyOwn shell not responding**: check that `payload.json` exists and has `rhost` set.

**Sessions/ files missing**: verify you are in `/home/grisun0/LazyOwn` and `sessions/` is writable.

**C2 not starting**: ensure `lhost` and `c2_port` are set in payload.json; check `cert.pem` / `key.pem` exist.

---

## Documentation hierarchy

| File | Lines | Purpose |
|------|-------|---------|
| `ESSENTIALS.md` | ~120 | 18 core commands for 80% of use |
| `CHEATSHEET.md` | ~300 | ~40 frequent commands by user goal |
| `QUICKSTART.md` | ~140 | First-time setup and onboarding |
| `skills/lazyown/SKILL.md` | ~120 | Hermes skill definition |
| `skills/lazyown.md` | ~1600 | Complete 95-tool MCP playbook |
| `COMMANDS.md` | ~5000 | Full 333-command reference (auto-generated) |
| `CLAUDE.md` | ~540 | Architecture and developer reference |
