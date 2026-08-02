# LazyOwn — Hermes Agent Context

Project: LazyOwn RedTeam Framework
Repo: /home/grisun0/LazyOwn
Language: Python 3.11+, Bash
Domain: penetration testing, red teaming, C2 operations

---

## What this project is

LazyOwn is a professional pentest/red-team framework:

- **CLI** (`lazyown.py`): cmd2 shell with 606 commands and 126 aliases covering the full kill chain.
- **C2** (`lazyc2.py`): Flask + Socket.IO web dashboard, beacon protocol, phishing, multi-operator collaboration.
- **MCP** (`skills/lazyown_mcp.py`): 148 tools exposing the framework to AI agents.
- **DB** (`modules/db.py`): SQLite database layer — workspaces, hosts, services, vulns, creds, loot, notes, nmap import.
- **Module Registry** (`modules/module_registry.py`): Catalog of 120+ modules from lazyaddons, plugins, tools, playbooks — search, use, run workflow.
- **Payload Factory** (`modules/payload_factory.py`): Native payload generation (reverse shells, PowerShell, shellcode) with format conversion.
- **Resource Scripting** (`modules/resource_script.py`): Enhanced `.ls` scripts with variables, if/while/for, macros, spool.

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
- `modules/`: LLM clients, blueprints, world model, playbook engine, **db (SQLite)**, **module_registry (120+ modules)**, **payload_factory (native payloads)**.
- `parquets/`: columnar knowledge bases (GTFOBins, LOLBas, MITRE ATT&CK).
- `lazyaddons/`: 124 YAML tool integrations. `plugins/`: Lua + YAML plugins. `tools/`: pwntomate auto-jobs.
- `cli/commands/`: CommandSets for **db_***, **search/use/back**, **generate**, **resource** — auto-registered at boot.

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

For the full 148-tool reference see `skills/lazyown.md`.

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

## Branching model for autonomous agents

LazyOwn uses three branches. Autonomous agents (Claude, Groq, SWAN) operate on `dev`.

| Branch | Purpose | Agent role |
|--------|---------|------------|
| `dev`  | Active development, daily commits, feature integration. | **Agents work here.** Human operator reviews and merges. |
| `pp`   | Pre-production / staging. QA and integration tests. | Read-only for agents. Promotion from `dev` is human-approved. |
| `main` | Production releases. Tagged releases only. | Read-only for agents. `DEPLOY.sh` runs here. |

### Rules for agents

- Start every session on `dev` (`git checkout dev`).
- Never commit directly to `main` or `pp`.
- Feature branches: `feature/<description>` cut from `dev`.
- Hotfix branches: `hotfix/<description>` cut from `main`, then back-merge to `pp` and `dev`.
- When instructed to release, create a PR from `dev` to `pp` (or `pp` to `main`) and request human approval.

---

## Documentation hierarchy

| File | Lines | Purpose |
|------|-------|---------|
| `ESSENTIALS.md` | ~120 | 18 core commands for 80% of use |
| `CHEATSHEET.md` | ~300 | ~40 frequent commands by user goal |
| `QUICKSTART.md` | ~140 | First-time setup and onboarding |
| `skills/lazyown/SKILL.md` | ~120 | Hermes skill definition |
| `skills/lazyown.md` | ~1600 | Complete 148-tool MCP playbook |
| `COMMANDS.md` | ~1600 | Full 333-command reference (auto-generated) |
| `CLAUDE.md` | ~540 | Architecture and developer reference |

---

## Connectivity Contracts (v3 — unified killchain)

These modules were created to close the gaps between kill-chain phases,
suggestion surfaces, and operational state. Each file is autonomous with a
single contract.

### `modules/killchain.py` — Single Source of Truth for Kill-Chain (NEW v3)

**Contract:** ``KillChain`` is the canonical authority for kill-chain data — phases,
progress, mapping, and atomic updates. Every display surface imports from here.
No other file defines its own phases. See ``CLAUDE.md`` Sections 16 and 16.1.

**Transport:** state is read/written only via ``modules/world_model`` (transparent
decrypt of the ``world_model.json.encrypted`` sibling). Beacon history is owned by
``modules/beacon_history.py``. Exposed over HTTP at ``/api/killchain`` and
``/api/beacon_results/<client_id>``. C2 decrypts on boot and re-encrypts on exit.

### `cli/tips_engine.py` — Unified post-command tips engine

**Contract:** Coordinate all suggestion surfaces (kill-chain hints, protips,
curiosity, autosuggest, ELO/VRI rewards) into ONE postcmd hook. Replaces the
five fragmented hooks that previously competed for operator attention.

**Key types:**
- `TipsConfig` — Centralised config (paths, tables, thresholds, tip registries)
- `EngagementState` — Persisted cross-session metrics (ELO, badges, commands_seen)
- `TipsEngine` — Coordination engine. Constructor injects config + autosuggest handle.

**Usage:** `TipsEngine(config, autosuggest_engine).render(cmd, phase)`

**Tests:** `tests/test_tips_engine.py` (49 tests, 6 mutation-killed)

### `cli/auto_crypto.py` — Automatic session data encryption

**Contract:** Encrypt sensitive session files on app close and decrypt on authenticated
startup. Uses PBKDF2HMAC + Fernet (same as lazyenc.py). Never blocks the shell.

**Key types:**
- `AutoCryptoConfig` — protect_globs, sessions_dir, password_provider, auto_enabled
- `AutoCryptoEngine` — encrypt_session(), decrypt_session(), is_encrypted property

**Usage:** `engine.encrypt_session()` on exit, `engine.decrypt_session()` on startup

**Tests:** `tests/test_auto_crypto.py` (7 tests, 2 mutation-killed)

### `cli/reactive_hints.py` — Expanded kill-chain adjacency tables

**Contract:** `_KILL_CHAIN_NEXT` and `_PHASE_PRIORITY` now cover 60+ commands (was 20).
Missing commands added: auto_pwn, chain, hunt, nuclei, lazynuclei, yara_scan,
playbook_generate, playbook_run, campaign, collab_join, dashboard, encrypt, decrypt.

### `cli/protips.py` — Expanded tip registry with 6 categories

**Categories:** privesc, ai, ops, ecosystem, automation, security, collab, discovery.
New tips surface: auto_pwn, chain, hunt, nuclei, playbook_generate, encrypt, decrypt,
yara_scan, yara_marketplace, campaign, collab_join, dashboard, marketplace config,
nuclei_marketplace, palette.

### `cli/engagement_hooks.py` — Badges and expanded ELO coverage

**Badges awarded:** arsenal_master (100 commands), arsenal_legend (250), arsenal_god (500),
deep_recon (50/session), hacker_rank (3000 ELO), elite_rank (5000 ELO),
first_blood (5 commands), kill_chain_master (6 phases).

**ELO bonuses added:** auto_pwn (+30), chain (+20), hunt (+25), nuclei (+18),
yara_scan (+15), playbook_run (+15), playbook_generate (+12), collab_join (+8),
campaign (+10), encrypt/decrypt (+12), lazynuclei (+15), dashboard/marketplace (+5).

### `cli/recommendation_signals.py` — PlaybookSignal integration

**Contract:** New `PlaybookSignal` adapts `AptPlaybookEngine.list_playbooks()` into
concrete `Proposal` objects. Registered in `build_default_engine()` after the recon
signal, before the kill-chain fallback.

### `cli/commands/marketplace.py` — YARA + Nuclei marketplace

**New commands:** `yara_marketplace list|search|install|info|update|download-community`
and `nuclei_marketplace list|search|install|info|update [--severity <level>] [--cve <id>]`.
Both follow the same pattern as the existing addon marketplace.

### `lazyown.py` — Wiring (single unified hook + auto-crypto)

**Changes:**
1. Import `TipsEngine`, `AutoCryptoEngine`, `AutoCryptoConfig` at module level.
2. Initialise `self._tips_engine` and `self._auto_crypto` in `__init__`.
3. Register ONE postcmd hook: `self._unified_tips_hook` (replaces 5 hooks).
4. Register `atexit` handler for `self._run_auto_encrypt`.
5. `_run_auto_decrypt()` called at startup (after login).
6. `self._autosuggest` wired into tips_engine via `_tips_engine._autosuggest`.
7. Keep `_refresh_autosuggest` and `_read_recent_commands_for_autosuggest` for
   `do_next` and chain command compatibility.
