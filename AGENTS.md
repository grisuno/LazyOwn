# LazyOwn - Hermes Agent Context

Project: LazyOwn RedTeam Framework
Repo root: the working directory that holds `payload.json` and `lazyown.py`
Language: Python 3.11+, Bash
Domain: penetration testing, red teaming, C2 operations

> **Role routing:** this file is for an agent that modifies the repository.
> `CORE.md` is for an agent that consumes LazyOwn as a dependency. `CLAUDE.md`
> is the shared durable contract. Load only the file that matches the role.

---

## What this project is

LazyOwn is a professional pentest/red-team framework:

- **CLI** (`lazyown.py`): cmd2 shell with 837 commands and 130 aliases covering the full kill chain.
- **C2** (`lazyc2.py`): Flask + Socket.IO web dashboard, beacon protocol, phishing, multi-operator collaboration.
- **MCP** (`skills/lazyown_mcp.py`): 176 tools exposing the framework to AI agents.
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
- `modules/`: LLM clients, blueprints, world model, playbook engine, **db (SQLite)**, **module_registry (120+ modules)**, **payload_factory (native payloads)**, **orchestrator_config (YAML profiles)**, **chain_registry/chain_runner (chain v2)**, **outcome_bus (sink fan-out)**, **emulation_runner (Atomic execution)**, **metasploitable_gym (MS2 matrix)**, **gym_registry (YAML gyms + world-model runs)**, **addon_updater (git updates)**.
- `parquets/`: columnar knowledge bases (GTFOBins, LOLBas, MITRE ATT&CK).
- `lazyaddons/`: 124 YAML tool integrations. `plugins/`: Lua + YAML plugins. `tools/`: pwntomate auto-jobs.

---

## Security hardening (SDD+TDD+BDD)

Critical security fixes applied with full test coverage. Run: `pytest tests/test_security_hardening.py tests/test_security_hardening_v2.py tests/test_security_hardening_v3.py tests/test_security_hardening_v4.py -v`

| Fix | File | Contract |
|-----|------|----------|
| SQL injection prevention | `modules/db.py` | Table name allowlist via `VALID_TABLES` frozenset |
| LIKE escape injection | `modules/db.py` | Special LIKE chars escaped with `ESCAPE '\\'` |
| Timing-safe auth | `lazyc2.py` | `hmac.compare_digest` replaces `==` in `check_auth` |
| SafeRunner shell=False | `core/safe_subprocess.py` | `subprocess.run(argv, shell=False)` |
| pickle removed | `utils.py` | RCE vector eliminated |
| Hardcoded secrets removed | `utils.py` | `secrets.token_hex`/`secrets.token_urlsafe` at runtime |
| Config constants consolidated | `modules/ai_fallback.py`, `cli/commands/ai.py` | Import from `modules/llm_factory` |
| Credential encryption logging | `modules/db.py` | Warnings instead of silent plaintext fallback |
| CORS dev fallback expanded | `lazyc2/security/cors.py` | Always includes `127.0.0.1` + `localhost` + `lhost` |
| Hardcoded credentials removed | `cli/commands/postexp_migrated.py`, `cli/commands/report_migrated.py`, `cli/commands/exploit_migrated.py`, `templates/index.html` | All passwords read from config or require explicit input |
| Command injection in AI module | `cli/commands/ai.py` | `os.system` replaced with `subprocess.run` list-form; API key via env var |
| SSH credential injection | `cli/commands/postexp_migrated.py` | `sshpass -e` + `SSHPASS` env var replaces `sshpass -p` |
| DNS command allowlist | `lazyc2.py` | `_DNS_COMMAND_ALLOWLIST` frozenset + length cap |
| Safe shell execution | `cli/commands/misc_migrated.py` | `do_sys` uses `subprocess.run` with output capture |
| Credential encryption at rest | `modules/phishing_orchestrator.py` | AES-256-GCM encryption for harvested passwords |
| URL injection prevention | `poc_tui/plugin_loader.py` | `_validate_clone_url` rejects metacharacters; git clone uses subprocess list-form |
| os.system eliminated | `modules/morse.py`, `modules/c2_builder.py`, `modules/bot.py`, `modules/ia_*.py` | Replaced with subprocess.run or Python-native operations |
| shell=False enforced | `lazyc2.py` | `execute_command` uses `shlex.split` + `shell=False` |
| Hardcoded paths removed | `telegram_hermes.py`, `modules/c2_builder.py`, `cli/commands/anti_forensics.py` | Replaced with Path.home() or shutil.which |
| Placeholder injection prevention | `modules/conditional_hooks.py` | `shlex.quote` applied to all placeholder values before shell insertion |
- `core/hardening.py`: Centralized security primitives — `safe_subprocess_run`, `safe_clipboard_copy`, `set_sshpass_env`, `escape_html_content`, `safe_path_join`, `validate_host`, `validate_network_cidr`, `validate_port_spec`, `require_encryption_key`, `defused_xml_parse`, `sanitize_filename`.
- `core/safe_exec.py`: Safe command execution — `safe_system`, `safe_run_argv`, `safe_run_shell`, `safe_clear_screen`, `validate_url`, `safe_git_clone`, `safe_ip_show`, `safe_find_tool`, `safe_file_read`.
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
# Option A: install from repo (run from the repository root)
hermes skills install skills/lazyown/SKILL.md

# Option B: auto-discovered via AGENTS.md when the cwd is the repository root
```

### The LazyOwn Soul

Read `soul.md` at the start of every engagement. It is the operating philosophy — not documentation, not rules, but the spirit that guides every decision.

```bash
cat soul.md
```

Key principles: evidence over assumption, abstraction over mechanics, phase discipline, situational awareness first, the 80/20 rule, document for the next shift, ask the machine when uncertain, professional over theatrical, configuration is code, collaboration is not optional.

### MCP registration

```bash
bash scripts/setup_hermes_mcp.sh
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

For the full 173-tool reference see `skills/lazyown.md`.

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

**Sessions/ files missing**: verify you are in the repository root and `sessions/` is writable.

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

- Start every session on `dev`, but SYNC it with `main` first: `git fetch origin main dev && git checkout dev && git merge --ff-only origin/main || git merge --no-edit origin/main`. Verify with `git merge-base --is-ancestor origin/main HEAD`. Never work on a stale `dev`.
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
| `skills/lazyown.md` | ~1600 | Complete 173-tool MCP playbook |
| `COMMANDS.md` | ~1600 | Full 837-command reference (auto-generated) |
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

### `modules/chain_approval.py` — C2 human-in-the-loop approval gate (v4)

**Contract:** ARTEX intercept doctrine, adapted. `PendingStore` holds pending
`confirm`-step requests in `sessions/chain_pending.json` (id, chain, step_id,
command + SHA-256 fingerprint, deadline, status pending/approved/denied/expired)
and appends every transition to the audit trail `sessions/chain_audit.jsonl`.
`build_c2_approver` routes a confirm step to that pending list and polls
failure-closed: deadline expiry (swept by `expire_stale`) or any store error
votes deny.

**Backend selection:** `LAZYOWN_APPROVAL_BACKEND=c2` routes confirm steps to the
C2 pending list; the default keeps the interactive CLI approver, and
`LAZYOWN_APPROVAL_TIMEOUT` bounds the window (300s default).

**Surfaces:** CLI `apt_chain approvals [list|approve|deny] [id]`, C2
`GET /api/chain_approvals[?status=pending]` and
`POST /api/chain_approvals/<16-hex-id>/decide` (`decision: approve|deny`,
`decided_by=c2`). Unknown or already-decided ids answer 404; malformed ids and
verdicts answer 400. **Tests:** `tests/test_chain_approval_c2.py` (15 tests).

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

### `modules/winbox_gym.py` — WinBox lab (v5 — self-healing isolated Windows gym)

**Contract:** WinBox (https://github.com/totekuh/winbox) is the second Red
Team Gym scenario (`scenario: winbox`): an isolated headless Windows VM
(Server Core 2022/2025, Win11, Win10) driven through QEMU/libvirt from the
operator host. The module is the single control plane: gym catalogue
(`playbooks/gym_winbox.yaml` index ↔ `exploits/winbox_*.yaml` ↔
`chains/gym_winbox_*.yaml`), safe CLI adapter (allowlisted actions,
`subprocess` list-form, `sessions/winbox/` transcripts) and readiness
gating (guidance-only when the binary or prerequisites are missing).

- CLI: `winbox status|up|down|exec|tools|eventlogs|net|av|applocker|snapshot|resolve|gym`
  (`cli/commands/winbox_gym.py`). `winbox up` / `winbox setup` are the
  FULL idempotent bootstrap (upstream repo clone+pip, `sudo -n apt-get`
  prereqs via `ensure_prereqs`, `winbox iso download`, `winbox setup -y`
  via `ensure_lab_ready`, boot, rhost bind) — gym start for a winbox
  challenge runs the same bootstrap then auto-launches the chain.
  Destructive actions require `-y` (`destroy` is allowlisted).
- Self-healing bootstrap (`ensure_lab_ready`): every stage emits live
  progress through a `notify` callback and long stages stream their child
  output through a pty (`sessions/winbox/*.log` keeps the transcript with
  ANSI intact). Step order: install → prereqs → snapshot gate → iso →
  setup → recovery → up → provision gating → resolve.
- Mid-install recovery: when `winbox setup` exits on an in-flight
  install (false/real timeout), the module waits for the guest to shut
  down (grace 3600s), then completes winbox phases 2-4 (offline
  virt-customize injection, boot-for-provisioning with WinFsp/virtiofs
  in-guest install, nwfilter, `clean` snapshot) by calling the upstream
  installer internals with the process locale forced to C. A substantial
  disk (≥ 4GB) with no `clean` snapshot triggers the same completion; a
  tiny/absent disk falls back to `winbox destroy -y` + one full rebuild,
  loudly. Nothing is ever silently skipped: every stage records ok/fail
  in the returned `stages` map and the CLI prints the stage table.
- Post-provisioning invariant: after the VM is up, a Z: probe
  (`if exist Z:\` via guest agent) runs unconditionally; a missing drive
  triggers one idempotent `winbox provision` re-run and a re-probe; a
  persistent failure is a loud stage failure.
- Locale hardening: all winbox/virsh children run with `LANG=C LC_ALL=C`
  (`safe_subprocess_run` gained `extra_env`), and VM state strings are
  normalized through `_canonical_state` (English + Spanish aliases),
  so no state gate depends on shell locale.
- Gym: `gyms/winbox_*.yaml` (4 challenges), matrix via
  `modules/gym_winbox_runner.py` reusing `gym_matrix_runner`/`ctf_capture`
  with the catalogue injected as a parameter (Metasploitable 2 stays the default).
- APT chain: `chains/apt_winbox_windows.yaml` — Windows golden path
  (scan → SMB/RDP mapping → exploit sweep → SYSTEM exec → posture →
  LockBit playbook emulation → event-log evidence → snapshot).
- MCP: 9 `lazyown_winbox_*` tools; agents can also attach the upstream
  `winbox mcp` server (97 research tools) directly.
- Skill: `skills/winbox/SKILL.md`. Lazyaddon: `lazyaddons/winbox.yaml`
  (trigger-only registration; the shell command is the built-in CommandSet).

### `modules/ad_gym.py` — AD lab gym (v1 — disposable Docker Samba DC)

**Contract:** the `ad-lab` scenario is a single `nowsci/samba-domain`
container (Kerberos 88, LDAP 389, SMB 445, Kpasswd 749): boots in ~90s,
destroyed with `lab stop ad-lab`. `LAB_SCENARIOS["ad-lab"]` carries env
(DOMAIN `lazylab.local`, documented fixture password constants in
`lab_runtime`) and `privileged: true` (Samba sysvol ACL provisioning
denies it otherwise); `start()` forwards `env`/`privileged` generically
and `_ensure_ad_lab` idempotently creates the `svc_sql` SPN fixture.
No ports are published: attacks go to the container IP on the Docker
bridge.

- Catalogue mirrors `metasploitable_gym`: `playbooks/gym_ad_lab.yaml`
  index ↔ `exploits/ad_lab_*.yaml` ↔ `chains/gym_ad_lab_*.yaml`
  (5 vectors: LDAP enum, SMB shares, RID cycling, SAMR null-session
  enum, default-cred validation), golden path `chains/apt_ad_lab.yaml`.
  `gym start ad_lab_apt` auto-launches the chain with the container IP
  (auto-launch now covers every docker scenario with a chain, not just
  winbox).
- Evidence: `ctf_capture` gained `kerberos_ticket` (masked),
  `domain_enum` (LDAP/SAMR/RID) and `smb_shares` checkers.
- Lab fixture note: impacket `KRB_AP_ERR_INAPP_CKSUM` makes TGS-roasting
  unavailable against this Samba KDC build, so the kerberoast vector was
  replaced by the null-session SAMR enum that the lab does expose.

### `modules/lazy_creds.py` + `modules/lazy_oob.py` — awesome-redteam adoption (v1)

**lazycreds:** default-credential knowledge base
(`modules/data/default_creds.csv`, ~3.4k vendor/user/pass triples from
the open DefaultCreds-Cheat-Sheet, MIT, via threekiii/awesome-redteam).
Pure file reads: `search`, `candidates` (frequency-ranked spray list),
`export_pairs` (user:pass file for sprayers). Shell: `lazycreds <query> |
--top <n> | --export <file>`.

**lazyoob:** local HTTP callback canary for blind SSRF/RCE: binds to
`lhost` (payload.json) with token paths `/oob/<token>`, records hits in
memory + `sessions/oob_hits.jsonl`, never parses or proxies anything.
Shell: `lazyoob start|url|hits|stop`.

**Playbook:** `playbooks/web_exploitation_awesome.yaml` — 40x-bypass
(headers, verbs, path normalisation, proxy confusion) and SQLi
(error/boolean/time-based) technique steps distilled from the same
collection.

<!-- readmenator-agent-kb-link -->
## Project Knowledge Base (MUST read before coding)

Generated offline by [ReadMenator](https://github.com/grisuno/ReadMenator) (zero-token static analysis). Humans: `KNOWLEDGE_BASE.md`.

0. Memory: `cat readmenator-agent/MEMORY.md` (business rules, workflow, constraints, style, done criteria, session log). Record new decisions with `readmenator . remember "<note>" --kind decision`.
1. Freshness: `readmenator . fresh` (exit 1 means stale: run `readmenator . --rebuild`). Without the CLI, compare `git_commit` in `readmenator-agent/MANIFEST.json` with `git log -1`.
2. Orient: `ls *.md readmenator-agent/ readmenator-wiki/`, then read `readmenator-wiki/index.md` (big picture, communities, god nodes).
3. Locate: `grep -n '<keyword>' readmenator-agent/INDEX*.md readmenator-agent/SYMBOLS*.md` before any `glob` over sources; for questions use `readmenator . ask "<question>"` (GraphRAG, `--global` for overviews).
4. Context: `cat readmenator-agent/KB_<subsystem>.md` for the subsystem you touch.
5. Before editing: `grep -n '<file>' readmenator-agent/GOTCHAS.md readmenator-agent/SECURITY.md` (blast radius, cycles, findings).

Also: `API*.md` (public functions, one line each), `ARCHITECTURE*.md` (dependency pairs), `recipes/*.md` (grounded task steps). Large docs are paged as `NAME_p2.md`, so always grep with `NAME*.md`.

    pip install readmenator && readmenator . --rebuild
<!-- /readmenator-agent-kb-link -->
