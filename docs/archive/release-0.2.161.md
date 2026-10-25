## v0.2.161 Highlights

### Unified kill-chain (single source of truth)
- `modules/killchain.py` computes the phase; every surface (CLI `/killchain`,
  `/api/killchain`, C2 `/api/data`+`/api/dashboard`, GUI2 panel) renders its
  `snapshot()`.
- Beacon command history per implant: `/api/beacon_results/<client_id>`,
  backed by `modules/beacon_history.py` (JSONL, path-safe).
- CLI `/killchain auto on|off|N` live auto-refresh; flags
  `killchain_auto_every` / `killchain_auto_on_phase_change`.
- C2 decrypts session state on boot and re-encrypts on clean exit, so beacons
  and the kill-chain reflect real values while the server runs.

### Marketplace (YARA + Nuclei)
Browse, search, and install from a unified marketplace TUI:
- `yara_marketplace list|search|install|info` -- 10 built-in rules (ransomware, C2, webshells, obfuscation, privesc)
- `nuclei_marketplace list|search|install|info` -- 500+ templates from `~/nuclei-templates`
- `marketplace list|search|install|update` -- 137 YAML addons, 57 plugins, 69 tools

### auto_pwn & hunt
- `auto_pwn` -- autonomous kill-chain walk from recon to exploitation
- `hunt` -- threat-informed recon: maps known TTPs to discovered services

### Reactive Intelligence
- Post-command tips engine: kill-chain hints, protips, curiosity rewards
- ELO rating, badges (First Blood, Arsenal Master, Kill Chain Master)
- Inline reactive hints: "next command" suggestions after every action

### Auto Crypto
Transparent session encryption on exit / decryption on startup via PBKDF2HMAC + Fernet.

### New Playbooks
7 APT profiles: Azure Graph API, CICD Poisoning, Entra Connect, macOS TCC, OAuth Token Theft, SCCM/MECM, VDI Breakout.

### Interactive Chain Mode
`chainmode on` starts a world-model-driven chaining flow: after every command
the shell offers ranked next steps (Enter = top suggestion, `1..N` = ranked
alternative, any command = override, `skip` = manual, ESC/Ctrl+C/`off` =
leave). Invalid picks re-prompt instead of silently skipping, and the flow
auto-pauses after `max_steps` chained commands. State persists in
`sessions/chain_mode.json` (atomic writes). Contract: `cli/chain_mode.py` +
`cli/command_chain.py`.

### Feature Polish (UX + security hardening)
- Evidence-backed inline hints: every suggestion carries verb, confidence
  (`[0, 99]`, never a dishonest 100%), reason, and provenance. Contract:
  `cli/reactive_hints.py` + `cli/recommendation_signals.py`.
- Unified tips engine rendered entirely through rich (no raw ANSI escapes);
  registry tip text can never break markup rendering. Contract:
  `cli/tips_engine.py`.
- `cli/noise_verbs.py` is the single source of truth for the non-actionable
  verb lists shared by hints, tips, and chain mode.
- Tenant-bound API keys: `core/api_authz.py` now implements the documented
  rotation grace window, copies permissions from the rotated key (regression
  fixed), returns JSON 401/403 (safe with `TRAP_HTTP_EXCEPTIONS`), and the
  C2 `/api/health/tenant` endpoint is actually enforced. Mutation gate:
  `tests/run_mutation_api_authz.py` (7/7 killed).
- `core/logging.py` `install_json_handler` preserves pre-existing handlers
  and is idempotent.
- Structured ELO sync honours redirected user-store paths and tests are
  host-login independent.

### Security Hardening (SDD+TDD+BDD)

Centralized security primitives in `core/hardening.py` with 48 BDD-style tests
(`tests/test_security_hardening_v3.py`). Run with:
```bash
pytest tests/test_security_hardening.py tests/test_security_hardening_v2.py tests/test_security_hardening_v3.py -v
mutmut run  # 122/228 killed, 53.5% kill rate on core/hardening.py
```

**Key fixes applied:**
- `shell=True` eliminated from `anti_forensics.py`, `pivoting.py`, `icmp_server.py`, `resource_script.py`, `command_executor.py`, `postexp_migrated.py` (22 instances)
- `os.system()` eliminated from `persist_migrated.py`, `cloud.py`, `lazyown.py` (4 instances), `misc_migrated.py`
- `os.popen()` eliminated from `websocket_beacon.py`, `evasive_payload.py`
- `sshpass -p` replaced with `sshpass -e` + env var across 4 files (C2, lateral, exfil, persist)
- Hardcoded encryption key removed from `phishing_orchestrator.py` (ENCRYPTION_KEY mandatory)
- XSS in C2 banner fixed with `html.escape()`
- Command injection via rhost in clipboard fixed with `safe_clipboard_copy()`
- cmd2 `CMD_ATTR_HELP_CATEGORY` renamed to `COMMAND_ATTR_HELP_CATEGORY` (cmd2 4.2.2 compat)

---
