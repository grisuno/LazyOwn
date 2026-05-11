# CLAUDE.md — LazyOwn RedTeam Framework

This file is the durable, version-controlled context every Claude session must read before
touching this repository. It uses prompt engineering, context engineering and
spec-driven development with explicit happy paths and sad paths so that any agent — human
or model — can produce changes that fit the framework instead of fighting it.

> Audience: Claude (Sonnet/Opus) operating via Claude Code, the LazyOwn MCP server,
> or the `lazyown` skill. Source of truth for code lives in `lazyown.py`, `lazyc2.py`,
> `utils.py`, `payload.json`, and the `skills/`, `modules/`, `templates/` directories.

---

## 0. North Star — what LazyOwn is

LazyOwn is a professional **red team / penetration testing framework**. It bundles:

- A **cmd2-based interactive CLI** (`lazyown.py`) with 333+ attack commands and
  200+ aliases covering the full kill chain.
- A **Flask + Jinja2 + Socket.IO C2 server** (`lazyc2.py`) with 84 routes, 54
  templates, malleable HTTP profiles, an XOR-stub Go beacon, and a phishing
  module backed by SQLite + Groq AI.
- A shared **utility layer** (`utils.py`) with ~138 helpers: payload loading, ANSI
  output, prompt rendering, key/cert generation, NVD/ExploitAlert/PacketStorm
  scrapers, ARP spoofing primitives, etc.
- A **skills layer** (`skills/`) hosting the **MCP server**, autonomous daemon,
  hive-mind multi-agent system, MoE+RL SWAN orchestrator, parquet knowledge
  base, policy engine, and Groq/Ollama agents.
- An **extension layer**: `lazyaddons/*.yaml` (declarative tool integration),
  `plugins/*.lua` (Lua scripting via lupa), and `tools/*.tool` (pwntomate
  service-triggered jobs).

The **MCP layer sits on top of everything** and exposes ~95 `lazyown_*` tools to
Claude Code. The CLI uses **cmd2**. The C2 uses **Flask** with **Jinja2**.

---

## 1. Entry points and how to launch

### Launching the framework — `./run`

```sh
./run                       # interactive shell
./run --no-banner           # quiet
./run -s                    # require sudo
./run -p sessions/foo.json  # alternate payload
./run -c 'lazynmap'         # exec one command then exit
```

`./run` is a thin shell wrapper that:
1. Activates the virtualenv at `env/`.
2. Executes `python3 -W ignore lazyown.py "$@"`.

`lazyown.py` is **the only entrypoint that should be launched directly by the
operator**. All other Python files are imported, executed via `do_run`, called
from MCP, or spawned by the autonomous daemon — never invoked manually.

### Full-stack launch — `fast_run_as_r00t.sh`

`bash fast_run_as_r00t.sh --no-attach --vpn 1` runs **as root** inside a tmux
session named `lazyown_sessions`:
- Starts the C2 (`lazyc2.py`) on `lhost:c2_port` with self-signed TLS.
- Spawns nmap recon and the auto-loop selector cascade.
- `sleep_start` (default `333` seconds, see `payload.json`) MUST elapse before
  the loop fires its first command — never timeout below that value.

### MCP — Claude Code integration

```sh
claude mcp add lazyown python3 /home/grisun0/LazyOwn/skills/lazyown_mcp.py
```

After registration, restart with `bash skills/mcp_restart.sh` after any code
change that affects `skills/lazyown_mcp.py` or modules imported at startup.

---

## 2. Repository map — where things live

| Path | Role |
|------|------|
| `lazyown.py` | cmd2 shell, ~27k LOC. Defines `class LazyOwnShell(cmd2.Cmd)` and ~280 `do_*` commands. Single source of truth for the CLI. |
| `lazyc2.py` | Flask + Socket.IO C2 server, 84 routes, decoy site, phishing blueprint, dashboard, terminal, listener, /pty xterm. |
| `utils.py` | Shared helpers (`Config`, `load_payload`, `getprompt`, `print_msg`, `run_command`, `xor_encrypt_decrypt`, `generate_certificates`, ANSI constants, etc.). |
| `payload.json` | The **only** runtime configuration file. Keys are read by every component. Persists across runs. |
| `templates/` | 54 Jinja2 templates: `index.html`, `terminal.html`, `surface.html`, `connect.html`, `decoy.html`, `phishing/`, `landing_pages/`, `emails/`, etc. |
| `static/` | CSS/JS assets, dashboard, body_report.json (PDF report fields), icons. |
| `modules/` | Python modules invoked via `run <name>` or imported by lazyc2 (LLM clients, dashboards, parsers, exploits). |
| `skills/` | MCP server + autonomous AI stack (mcp, hive_mind, swan, daemon, policy, parquet_db). |
| `sessions/` | Authoritative campaign state — never delete without confirmation. |
| `parquets/` | Knowledge bases: GTFOBins, LOLBas, MITRE ATT&CK, Atomic Red Team, session_knowledge. |
| `plugins/` | Lua plugins (lupa runtime). |
| `lazyaddons/` | Declarative YAML tool integrations. |
| `tools/` | pwntomate `.tool` files auto-applied to nmap-discovered services. |
| `external/` | Vendored upstreams (atomic-red-team, etc.). |
| `lazyscripts/` | `.ls` scripts — small recipes loaded with `run_script`. |

---

## 3. The `payload.json` contract — single source of configuration

`payload.json` is loaded by `utils.load_payload()` and wrapped in `class Config`
(see `utils.py:3229`). Every component — CLI, C2, MCP, agents — reads from this
one file. **Nothing is hardcoded; nothing is duplicated; if a value would be
used in more than one place, it lives here.**

Critical keys (full list in `payload.json`):

| Key | Purpose |
|-----|---------|
| `rhost`, `lhost`, `rport`, `lport` | Target / attacker IPs and ports |
| `c2_port`, `c2_user`, `c2_pass` | C2 listener socket and basic auth |
| `domain`, `subdomain`, `os_id` | Target context (os_id 1=lin/2=win) |
| `start_user`, `start_pass` | Initial creds, auto-injected when discovered |
| `wordlist`, `usrwordlist`, `dirwordlist`, `dnswordlist`, `iiswordlist` | SecLists paths |
| `c2_maleable_route` | URI prefix beacons use (default `/pleasesubscribe/v1/users/`) |
| `user_agent_*`, `url_trafic_*` | Malleable C2 profile overrides |
| `sleep`, `sleep_start` | Beacon jitter and auto-loop bootstrap delay |
| `api_key` | Groq key (used by report.py and AI agents) |
| `enable_telegram_c2`, `enable_discord_c2`, `enable_ia`, `enable_deepseek`, `enable_cloudflare`, `run_in_memory`, `enable_c2_implant_debug`, `enable_c2_debug` | Boolean feature flags |
| `c2_daily_limit`, `c2_hour_limit`, `c2_login_limit` | flask-limiter strings |
| `targets` | Multi-target list with status, ports, tags, notes |
| `rat_key` | XOR key for stub/beacon encoding |
| `device`, `startip`, `endip` | Network discovery range |

### Reading vs writing config

- **CLI in-process**: `self.params[key]` (set by `do_assign`/`do_set`, written
  back to `payload.json` on save).
- **External code**: `from utils import Config, load_payload; cfg = Config(load_payload())`.
- **MCP**: `lazyown_get_config()` / `lazyown_set_config(key, value)`.

If a value needs to persist across processes (CLI ↔ C2 ↔ daemon ↔ MCP), it
**must** go through `payload.json`. Do not invent ad-hoc JSON files unless they
represent a genuinely different domain (e.g. `sessions/world_model.json`,
`sessions/tasks.json`, `sessions/objectives.jsonl`).

---

## 4. Architecture in one picture

```
┌────────────────────────────────────────────────────────────────┐
│                         operator / Claude                      │
└──────┬───────────────────────┬────────────────────┬────────────┘
       │ ./run                 │ MCP                │ Web UI / phishing
       ▼                       ▼                    ▼
 ┌─────────────┐       ┌──────────────────┐   ┌───────────────────┐
 │ lazyown.py  │◄──────│ skills/lazyown_  │   │   lazyc2.py       │
 │ (cmd2 CLI)  │       │ mcp.py (~95 fns) │   │ Flask + Socket.IO │
 │ class       │       └────────┬─────────┘   │ + Jinja2 + DNS    │
 │ LazyOwn-    │                │             │ + xterm /pty      │
 │ Shell       │                ▼             └─────────┬─────────┘
 └──────┬──────┘       ┌──────────────────┐             │
        │              │ skills/          │             │
        │              │ - autonomous_    │             │
        │              │   daemon         │             │
        │              │ - hive_mind      │             │
        │              │ - swan_agent     │             │
        │              │ - lazyown_policy │             │
        │              │ - parquet_db     │             │
        │              └────────┬─────────┘             │
        │                       │                       │
        ▼                       ▼                       ▼
        ┌────────────────────────────────────────────────────┐
        │   utils.py (Config, load_payload, run_command, …)  │
        ├────────────────────────────────────────────────────┤
        │   payload.json   (single source of configuration)  │
        ├────────────────────────────────────────────────────┤
        │   sessions/      (authoritative campaign state)    │
        │   parquets/      (knowledge bases)                 │
        │   templates/     (Jinja2)                          │
        │   modules/, plugins/, lazyaddons/, tools/          │
        └────────────────────────────────────────────────────┘
```

`lazyown.py` and `lazyc2.py` both import from `utils.py` and read `payload.json`.
The MCP server reuses `LazyOwnShell` to execute commands — there is no second
implementation of the CLI.

---

## 5. CLI — `lazyown.py` (cmd2)

### Conventions

- Class: `LazyOwnShell(cmd2.Cmd)` — one class, one shell. Subclass `CommandSet`
  only if a feature is meaningfully orthogonal (rarely needed; existing commands
  go on the main class).
- Command method: `do_<name>(self, line)` — name is the CLI verb.
- Help string: a docstring on the method. cmd2 surfaces it via `help <name>`.
- Argument parsing: prefer `@with_argparser(parser)` for any non-trivial flag
  set; use `@with_argument_list` for simple split.
- Categories: `@with_category('Recon')` etc. Keep the existing category names.
- Aliases: register in the `aliases` dict at class level (see lines ~114-260).
  Aliases that need `payload.json` values use `f""` strings interpolated at
  class-body load time — this is intentional; they refresh on shell restart.
- Persistent params: `self.params` is the in-memory mirror of `payload.json`.
  Always write back via the existing `do_assign` / `do_set` flow so changes
  survive restart.

### Adding a command — happy path

1. Pick the right phase category and place the new method near related commands.
2. Read every input from `self.params` — never accept `rhost`/`lhost`/etc. as a
   positional argument when the value is in `payload.json`.
3. Validate with `check_rhost` / `check_lhost` / `check_lport` from `utils.py`.
4. Execute via `run_command(cmd_str)` (utils) so output is captured, ANSI is
   stripped for logs, and CSV logging fires.
5. Write artefacts to `sessions/...` using stable, documented filenames.
6. Add an alias if there is a natural short form (and only one).
7. If the new command should also be runnable from MCP, no extra work — MCP
   exposes every `do_*` automatically through `lazyown_run_command`.
8. If the new command has a phase, add it to the bridge catalog
   (`modules/c2_profile.py` or wherever `BridgeSelector` reads from) so the
   autonomous loop can find it.

### Adding a command — sad paths

- **Missing payload key** — call `check_rhost(rhost)` before use; if it returns
  `False`, print an error and `return` (do not raise).
- **External binary missing** — guard with `is_binary_present(name)` and emit a
  `print_warn` with install instructions; do not silently fall back.
- **Long-running tool** — never set a timeout below the documented runtime
  (e.g. `lazynmap` ≥ 30 min). Detach with `subprocess.Popen` and emit a
  `print_msg` pointing at the artefact path.
- **OS mismatch** — read `sessions/os.json` (or `payload.json["os_id"]`) and
  refuse if Linux-only command is invoked against a Windows target. The
  fallback maps in the daemon already enforce this; the CLI should mirror it.
- **Sensitive output** — never print secrets to stdout; write to
  `sessions/credentials*.txt` or `sessions/hash*.txt` and tell the user where.

### What NOT to do

- Do not import `lazyc2` from CLI commands. The CLI must run without Flask.
- Do not write to `payload.json` from anywhere except `do_assign`, `do_set`,
  `lazyown_set_config`, and `auto_populate`. Concurrent writers race.
- Do not hardcode a wordlist, port, or IP — use `self.params` keys.
- Do not introduce a new `print_*` style; reuse `print_msg` / `print_warn` /
  `print_error` from `utils.py` so colours and logging stay consistent.

---

## 6. C2 — `lazyc2.py` (Flask + Jinja2 + Socket.IO)

### Surface

- `app = Flask(__name__, static_folder='static')` (line ~1610).
- `socketio = SocketIO(app, async_mode='threading', transports=['websocket'])`
  with namespaces `/listener`, `/pty`, `/terminal`.
- `flask-limiter` enforces `c2_daily_limit`, `c2_hour_limit`, `c2_login_limit`
  from `payload.json`.
- 84 HTTP routes covering: landing/dashboard, malleable beacon protocol
  (`/command/<client_id>`, `<route_maleable><client_id>`), file upload/download,
  short-URL beacons, phishing campaigns, terminal/PTY, surface graph,
  Bloodhound zip ingest, AI bots (chatbot/vuln/taskbot/script/redop/adversary),
  and a JSON dashboard at `/api/dashboard`.
- Blueprints registered at runtime: `phishing_bp`, `dashboard_bp` (under
  `/dashboard`), `collab_bp` (under `/collab`).
- Auth: HTTP Basic via `requires_auth` (uses `c2_user` / `c2_pass`) plus
  `flask-login` for the operator UI.
- DNS server: `dnslib`-based custom resolver started in a daemon thread.
- Watcher: `watchdog.Observer` reacting to file events configured in
  `event_config.json`.

### Adding a route — happy path

1. Decide if the endpoint is **operator-only** (apply `@requires_auth`) or
   **beacon-facing** (apply both the canonical path **and** the malleable
   `f'{route_maleable}<...>'` alias as existing routes do).
2. Render templates with `render_template('foo.html', ctx=...)`. Pass typed
   context, not raw request data.
3. Validate every path / template name with `validate_route_path`,
   `validate_template_name`, and `is_safe_template_path` — these helpers exist
   for a reason; never bypass them.
4. Persist state via the existing helpers:
   - JSON files: `load_routes` / `save_routes`, `load_short_urls`, etc., which
     write atomically (`*.tmp` → `os.rename`) and chmod 600.
   - SQLite: open/close via `sqlite3.connect(DB_PATH)` and `with` blocks.
5. Log with `logger = logging.getLogger(__name__)` to `sessions/access.log`.
6. If the new endpoint emits Socket.IO events, reuse the existing namespaces.
7. New Jinja2 templates go in `templates/`. Extend `base.html`. Reuse
   `header.html`, `nav.html`, `footer.html` partials.

### Adding a route — sad paths

- **Path traversal** — always pass through `is_safe_template_path` before
  `render_template`. Reject any path that escapes `templates/`.
- **CSRF / auth bypass** — beacon routes accept POST without CSRF by design
  (implants don't carry CSRF tokens), but operator UI mutations must require
  auth and (where possible) a session cookie.
- **Decoy fall-through** — when the request's IP is not 127.0.0.1 nor `lhost`,
  the `decoy()` view renders `decoy.html` (a fake landing site that captures
  webcam/audio). Do not break this: every operator-only route must check
  authentication AND the request origin.
- **Hardcoded ports** — bind to `lport` / `c2_port` from `payload.json`, never
  literal numbers (the existing `app.run(host='0.0.0.0', port=lport, ...)` is
  the pattern).
- **TLS** — `cert.pem` / `key.pem` are generated by `gen_cert.sh`; the C2
  always serves over HTTPS in PROD.
- **Phishing routes** — register on `phishing_bp` (template_folder
  `templates/phishing`), not on `app` directly.

### Adding a Jinja2 template

- Extend `base.html` and `{% include %}` the layout partials.
- All user-facing strings must be escapable; mark `|safe` only when the input
  is provably HTML you produced.
- Template filenames are validated by `validate_template_name`
  (`^[a-zA-Z0-9_-]+\.html$`). Keep that pattern.

---

## 7. Shared utilities — `utils.py`

`utils.py` is the **only** module both `lazyown.py` and `lazyc2.py` import from.
It exposes ~138 functions plus the `Config`, `VulnerabilityScanner`, `MyServer`,
`SimpleHTTPRequestHandler`, and `IP2ASN` classes.

Use these instead of reinventing them:

| Need | Use |
|------|-----|
| Read `payload.json` | `load_payload()` then wrap in `Config(...)` |
| ANSI coloured output | `print_msg`, `print_warn`, `print_error` |
| Run a shell command and capture | `run_command(cmd)` |
| XOR-encrypt for stub/beacon | `xor_encrypt_decrypt(data, key)` |
| Generate self-signed TLS | `generate_certificates()` |
| Enrich exploit search | `find_ss`, `find_ea`, `find_ps`, `nvddb`, `exploitalert`, `packetstormsecurity` |
| HTTP request building | `generate_http_req(host, port, uri, ...)` |
| Validate inputs | `check_rhost`, `check_lhost`, `check_lport` |
| Tmux session bootstrap | `ensure_tmux_session(name)` |
| Emails / users / passwords | `generate_emails`, `get_users_dic`, `crack_password` |

`utils.py` is intentionally large; keep new helpers here only when they are
shared between the CLI and the C2. Single-feature helpers belong in
`modules/<feature>.py`.

There are currently **two** `class Config` definitions in `utils.py` (3229 and
3328). The second is a duplicate — do not add a third; if you must edit
`Config`, deduplicate first in a separate change.

---

## 8. MCP layer — `skills/lazyown_mcp.py`

The MCP server exposes ~95 tools to Claude Code. It **never re-implements** CLI
or C2 functionality; it imports `LazyOwnShell` (or composes shell + REST + file
reads) and calls existing methods.

Adding an MCP tool — happy path:

1. The underlying functionality must already exist as a `do_*` command, a CLI
   helper in `utils.py`, or a C2 endpoint. If not, add it there first.
2. Register the tool with the MCP server's tool decorator. Name it
   `lazyown_<verb>_<noun>` (e.g. `lazyown_get_config`).
3. Document parameters as JSONSchema. Mark required vs optional explicitly.
4. Return structured JSON (objects / lists), not free-form prose. Claude reads
   the result; downstream agents pipeline the JSON.
5. After editing the MCP server, run `bash skills/mcp_restart.sh` so the next
   tool call picks up the new code.

Sad paths:

- **Tool name collision** — the MCP discovers addons (`lazyaddons/*.yaml`),
  plugins (`plugins/*.lua`), and pwntomate `.tool` files at startup. Picking a
  generic name shadows them; prefix unambiguously.
- **Long-running calls** — tools that wrap `lazynmap` / `pwntomate` must run
  detached and return immediately, with a follow-up `*_status` tool to poll.
- **Stale config** — never cache `payload.json` inside the MCP process across
  calls. Always re-read it; the operator may have set keys via the CLI.

---

## 9. Sessions/ — campaign state, treat as authoritative

`sessions/` is the **only** durable, cross-process location for engagement
state. Never delete its contents without explicit operator confirmation.

Conventions (consumers depend on these exact names):

| File | Producer | Consumer |
|------|----------|----------|
| `scan_<rhost>.nmap`, `scan_<rhost>.nmap.xml` | `do_lazynmap` | autonomous_daemon, pwntomate, FactStore |
| `vulns_<rhost>.nmap` | `do_lazynmap` (vuln scripts) | reactive_engine |
| `<ip>/<port>/<tool>/*.txt` | pwntomate | bridge_suggest, threat_model |
| `logs/command_<tool>output<domain>.txt` | run_command CSV logger | facts_show |
| `LazyOwn_session_report.csv` | every command | timeline_narrator, threat_model |
| `credentials*.txt`, `hash*.txt` | reactive_engine, do_responder, etc. | every later phase |
| `world_model.json` | autonomous_daemon | session_state, recommend_next |
| `tasks.json` | campaign_tasks | sitrep, dashboard |
| `objectives.jsonl` | inject_objective | autonomous_daemon |
| `sessionLazyOwn.json` | shell shutdown / shift handoff | sitrep, c2_notes |
| `os.json` | do_ping, beacon ground truth | every selector |
| `events.jsonl`, `autonomous_events.jsonl` | event_engine, daemon | poll_events |
| `campaign_lessons.jsonl` | EpisodeReflectionEngine | next campaign |
| `policy_facts.json` | policy engine | dashboard |
| `captured_images/` | decoy site | operator review |
| `keyword_fallback_index.json` | rag fallback when ChromaDB absent | rag_query |

Before any tool runs:
1. `ls sessions/` to see what already exists.
2. Read it. If the answer is already there, do not re-scan.

---

## 10. Coding standards — non-negotiable

These rules are enforced by review. Code that violates them is rejected.

1. **English only.** Identifiers, strings, log messages, docstrings — all
   English. The existing codebase has a few Spanish docstrings; do not add new
   ones, and prefer translating when you touch the surrounding lines.
2. **No comments.** Self-explanatory names + docstrings only. The only
   acceptable inline comment is a single-line note about a non-obvious
   constraint or a CVE reference.
3. **No emojis** in code, log strings, or docs unless the operator explicitly
   asked. The banner art and ASCII logo are not emojis and are allowed.
4. **Docstrings on every public function and class.** Format:
   ```python
   def foo(bar: str) -> dict:
       """One-sentence summary.

       Args:
           bar: …

       Returns:
           …

       Raises:
           …
       """
   ```
5. **No magic numbers.** Constants live in `class Config` (when shared across
   the framework) or as `UPPER_SNAKE_CASE` module-level constants.
6. **No hardcoded paths, ports, IPs, wordlists, credentials.** If the value
   would be reused, put it in `payload.json`. If it is purely local to a
   module, use a module constant.
7. **SOLID** — every change must respect:
   - **S**ingle responsibility: one reason to change per class / function.
   - **O**pen/closed: extend via new addon YAML / new MCP tool / new selector
     subclass — do not edit a hot path to special-case one target.
   - **L**iskov substitution: any new selector must honour the
     `BaseSelector.suggest()` contract.
   - **I**nterface segregation: small, role-specific protocols (recon,
     exploit, cred, lateral, privesc).
   - **D**ependency inversion: high-level orchestration depends on the abstract
     `LLMBackend`, `MemoryStore`, `Selector` — never on Groq or ChromaDB
     directly.
8. **Best architecture for the problem.** When two patterns fit, pick the one
   already in use elsewhere in the codebase. Consistency beats novelty.
9. **No partial implementations.** Either the feature works end-to-end (CLI ↔
   payload.json ↔ MCP ↔ sessions/ artefact) or it isn't merged.
10. **No backwards-compatibility shims** for code that hasn't shipped to
    operators yet. Just change it.

---

## 11. Spec-driven development — happy path / sad path discipline

For every change, write down (in commit message or PR body — not in the code):

### Happy path
- Trigger: who/what calls this?
- Inputs: which `payload.json` keys, which CLI args, which MCP params?
- Successful outcome: which file in `sessions/`, which event, which return
  value?
- Observable signal: what does the operator see?

### Sad paths (enumerate at least these)
- Required `payload.json` key missing or empty.
- External binary or wordlist not installed.
- Network unreachable / timeout / TLS error.
- Target OS does not match command (Windows tool against Linux box, etc.).
- Output already exists in `sessions/` — must not redo destructive work.
- Concurrent writer on the same artefact (CLI + daemon both running).
- AV/EDR detected on the target — reactive_engine raises `escalate_evasion`.
- Operator interrupts (SIGINT) — `signal_handler` must clean up tmux/sockets.
- Long-running tool exceeds the documented runtime — never auto-kill, log and
  continue.
- Phishing template / route name fails validation — render the form again with
  a flash error, never `500`.

Every command and every route gets at least 6 sad paths considered. If a sad
path has no defensive code, justify it explicitly (e.g. "trust internal call
from `do_assign`, validated upstream").

---

## 12. Prompt and context engineering for the agents

When this codebase invokes Claude/Groq/Ollama (via `lazyown_llm_ask`,
`swan_run`, `hive_spawn`, `groq_agent`):

1. **System prompt** — set the persona explicitly (`sessions/soul.md` is the
   canonical persona file). Include hard stops (PII, customer-of-customer,
   destructive ops).
2. **Context window** — include only what changes the next decision:
   - Current phase from `world_model.json`.
   - The 3 most recent commands and outputs from `LazyOwn_session_report.csv`.
   - Top-3 pivot candidates from `world_model.NetworkGraph.centrality()`.
   - Active objective from `objectives.jsonl`.
   - Captured creds (only the ones relevant to the current target).
3. **Tool catalogue** — pass the bridge catalog filtered to the current phase
   and OS, never the full 347 commands.
4. **Output contract** — request structured JSON (`{"command": "...",
   "reasoning": "...", "mitre": "Txxx"}`); reject free-form prose.
5. **Reward shaping** — every executed step is scored by the Detection Oracle
   and OutcomeEvaluator; the reward is propagated to the RL Q-table and MoE
   expert weights. New selectors must emit a reward in `[0, 1]` to participate.

`sessions/soul.md` is the only file that can carry persistent persona/policy
between sessions. Use `lazyown_soul(action="write", content=...)` to update it.

---

## 13. Extending the framework — pick the right surface

| Goal | Surface |
|------|---------|
| Wrap an existing GitHub tool | `lazyaddons/<name>.yaml` (declarative) |
| Add a one-liner / payload generator | `plugins/<name>.lua` |
| Auto-run on a discovered service | `tools/<name>.tool` (pwntomate) |
| New CLI command | `do_<name>` in `lazyown.py` |
| New web UI page or beacon endpoint | `lazyc2.py` route + Jinja2 template |
| New MCP tool | `skills/lazyown_mcp.py` |
| New autonomous selector | subclass `BaseSelector` in `skills/autonomous_daemon.py` |
| New AI agent persona | `skills/lazyown_groq_agents.py` registry |
| New knowledge base | new parquet under `parquets/` + `lazyown_parquet_query` mode |

Adding `do_*` for something that already works as a YAML addon is a smell —
the YAML system exists precisely so you don't have to touch Python.

---

## 14. Things this framework deliberately does NOT do

- **Detection evasion as the primary feature.** Stealth modules exist but the
  framework is for authorized red team / pentesting. Do not add features whose
  only purpose is to evade defenders without an authorized engagement context.
- **Persist secrets in git.** `cert.pem`, `key.pem`, `payload.json`'s
  `api_key`, and `sessions/credentials*` must never be committed.
- **Run on Windows as a host.** `lazyown.py` exits if `os.name == 'nt'`. The
  framework targets Linux/macOS operators attacking Linux/Windows victims.
- **Mock infrastructure in tests.** `tests/` exercise real modules; integration
  tests like `tests/integration_autonomous_flow.py` run against fixtures in
  `sessions/` — never mock the C2 or the autonomous daemon.

---

## 15. Quick command cheatsheet for Claude

```
# Start of every session
lazyown_session_init()
lazyown_campaign_sitrep()

# Configure
lazyown_set_config(key="rhost", value="10.10.11.5")
lazyown_set_config(key="domain", value="target.htb")
lazyown_get_config()

# Phase-driven recon
lazyown_phase_guide(phase="recon")
lazyown_run_command("ping")
lazyown_run_command("lazynmap")
lazyown_auto_populate(target="10.10.11.5")
lazyown_facts_show(target="10.10.11.5", refresh=True)

# Knowledge before action
lazyown_searchsploit(query="<service> <version>")
lazyown_parquet_query(mode="context", phase="enum", target="10.10.11.5")
lazyown_rag_query(query="…", n=5)

# Execute and learn
lazyown_run_command("<verb>")
lazyown_reactive_suggest(output="<raw output>", command="<verb>", platform="linux")

# Autonomy
lazyown_auto_loop(target="10.10.11.5", max_steps=10)
lazyown_autonomous_start(max_steps_per_objective=15)
lazyown_swan_ensemble(task_type="…", task="…", phase="…")
lazyown_hive_spawn(goal="…", n_drones=4, roles=["recon","exploit","cred","lateral"])

# Reporting
lazyown_generate_report(target="10.10.11.5", include_timeline=True)
lazyown_report_update(action="auto_fill")
lazyown_misp_export()
```

---

## 15a. Graph-aware navigation — `graphify` + `cli/graph_advisor.py`

LazyOwn ships a knowledge graph of itself, built by the `/graphify` skill and
stored under `graphify-out/graph_lazyown.json` (~1500 nodes, ~2900 edges,
14 communities). The graph is consumed at runtime by
`cli/graph_advisor.py` (SOLID, single file, fully tested in
`tests/test_graph_advisor.py`) and surfaced in three places so neither
humans nor agents have to re-read the JSON.

**CLI**

```
graph_search <query> [limit]           # fuzzy rank nodes by label/id/source
neighbors <node> [depth] [limit]       # walk the graph outward from one node
god_nodes [N]                          # most-connected nodes (core abstractions)
suggest_next [seeds...] [N]            # next-command recommendation; reads
                                       # sessions/LazyOwn_session_report.csv
                                       # when no seeds are passed
```

The shell's `default()` hook now uses the same advisor to surface
"did you mean…?" suggestions when an unknown `do_*` is typed.

**MCP**

```
lazyown_graph_summary()                # node/edge/community counts; sanity check
lazyown_graph_search(query, limit)     # fuzzy node search, budget_tokens aware
lazyown_graph_neighbors(node, depth)   # layered adjacency walk with edge metadata
lazyown_graph_suggest_next(recent)     # next-step recommendation from recent
                                       # activity (or pass an explicit seed list)
```

Every MCP graph tool accepts `budget_tokens` (default 1500) and trims its
JSON response in-place so list-of-results responses never blow an agent's
context window. When the graph is missing, every tool returns
`{"available": false, "reason": "..."}` so callers can react cleanly.

**Refreshing the graph**

```
/graphify .                            # full build (LLM-backed semantic
                                       # extraction for docs/papers, AST for code)
/graphify . --update                   # incremental; code-only edits skip the LLM
```

The advisor caches by `(path, mtime)` so a fresh `/graphify` rebuild is
picked up automatically on the next CLI command or MCP call without
restarting the shell or the MCP server.

---

## 15b. Operator UX — inline hints + TUI dashboard

### Inline reactive hints — `cli/reactive_hints.py`

A `register_postcmd_hook` callback fires after every `do_*` command and
prints a single dim line of next-step suggestions before the next prompt:

```
  ↳ do_gobuster · do_enum4linux · do_ffuf
```

Rules:

- Suggestions come from `GraphAdvisor.suggest_next()` — structurally grounded,
  not a generic list.
- Commands on `SKIP_COMMANDS` (help, exit, dashboard, set, palette, …) never
  produce hints.
- Controlled by `enable_inline_hints` in `payload.json` (default `true`).
  Operators disable with `set enable_inline_hints false`.
- When the graph is absent the hook is a no-op — no error, no output.
- Never adds latency beyond graph lookup time (< 1 ms after first load).

Implementation notes for contributors:

- `render_inline_hints(advisor, last_command, limit, enabled)` is the only
  public surface. The caller owns the advisor instance.
- Output goes through `rich.console.Console` so ANSI colours are handled
  correctly on all terminals and piped output.
- The hook must return `data` unchanged — cmd2 passes `PostcommandData` by
  reference through the chain.

### Operator TUI dashboard — `cli/dashboard_tui.py`

`dashboard` (CLI command) launches a full-screen Textual application that
blocks the shell while open (like `htop` or `lazygit`). Press **Q** to quit
and return to the cmd2 prompt.

Architecture:

- `LazyOwnDashboard(App)` — the Textual root; accepts `payload_path` and
  `sessions_dir` so tests and alternate configs work cleanly.
- Widget hierarchy: `TargetPanel` → `KillChainPanel` + `ConfigPanel` →
  `CommandsPanel` → `OpsPanel` → `HintBar`.
- `_do_refresh()` is called on mount and every `REFRESH_INTERVAL` (5s) via
  `set_interval`. Each widget receives typed data dicts — no widget touches
  the filesystem directly.
- `launch(payload_path, sessions_dir)` is the only public entry point.
  `do_dashboard` in `lazyown.py` calls it after a try/import guard.

Data helpers (all pure, tested independently):

| Helper | Source |
|--------|--------|
| `_read_json(path)` | Any JSON file; returns `{}` on error |
| `_read_recent_commands(limit)` | `sessions/LazyOwn_session_report.csv` |
| `_count_lines_in_glob(pattern)` | `sessions/credentials*.txt` etc. |
| `_beacon_count()` | `sessions/beacons.json` |
| `_graph_hints(limit)` | `graphify-out/graph_lazyown.json` via `GraphAdvisor` |

Requires `pip install textual` (added to `install.sh` and `requirements`).

---

## 16. Read these next

- `README.md` — public-facing feature list (long, marketing-flavoured).
- `COMMANDS.md` — exhaustive list of every CLI command.
- `UTILS.md` — auto-generated reference for `utils.py`.
- `CHANGELOG.md` — release history, useful for context on any flag you don't
  recognise.
- `skills/lazyown.md` — full MCP playbook (mandatory reading before any MCP
  session).
- `skills/README.md` — skills layer architecture.

When in doubt: read `payload.json`, read `sessions/`, then write code.
