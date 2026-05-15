# modules

Python modules invoked by the CLI via `run <name>`, imported by `lazyc2.py`
at startup, or called from the autonomous daemon. This directory is the
extension point for features that are too large or too specialised to live in
`lazyown.py` or `utils.py` directly.

## Subdirectories

| Directory | Contents |
|-----------|---------|
| `backdoor/` | C source and headers for the Linux backdoor (`backdoor.c`, `server.c`, `keylogger.h`). Built with the included `Makefile`. |
| `rootkit/` | Linux kernel module rootkit research code (`mr.c`, `mrhyde2.c`, `modules.order`). For authorized kernel-level testing only. |
| `win_rootkit/` | Windows ring-3 rootkit sources (`mrhyde.c`, `win_ring3_rootkit.c/.cpp/.cs`). Cross-compiled for Windows target testing. |
| `cgi-bin/` | CGI-exploitable templates used in web application testing scenarios. |
| `integrations/` | Third-party tool bridges: MISP export, Nuclei scanner bridge, Searchsploit wrapper. |
| `sessions/` | Session-scoped module outputs written during an engagement (not the top-level `sessions/` directory). |
| `templates/` | Jinja2 template fragments used by module-level report generators. |
| `wordlist/` | Wordlist generation and mutation utilities. |

## Key modules

| File | Purpose |
|------|---------|
| `collab_bp.py` | Flask blueprint for multi-operator real-time collaboration: SSE event stream, target locking, operator registry, publish endpoint, team dashboard UI at `/collab/`. |
| `dashboard_bp.py` | Flask blueprint for the operator web dashboard at `/dashboard/`. |
| `c2_profile.py` | Malleable C2 profile parser and `BridgeSelector` catalog. Feeds the autonomous daemon with phase-tagged commands. |
| `agent_runner.py` | Groq / Ollama agent execution harness. Manages prompt construction, tool-call loops, and result formatting. |
| `ai_model.py` | LLM client abstraction. Dispatches to Groq, Ollama, or local DeepSeek depending on `payload.json` flags. |
| `apt_playbooks.py` | APT playbook engine: list, validate, run, and report on YAML-defined adversary simulations backed by `playbooks/*.yaml`. |
| `atomic_enricher.py` | Enriches Atomic Red Team tests with MITRE ATT&CK context from the parquet knowledge bases. |
| `bot.py` | Flask chatbot endpoint logic. Used by the AI bots routes in `lazyc2.py`. |
| `c2_builder.py` | Generates malleable C2 profile variants and beacon configuration files. |
| `categories.py` | Maps CLI commands to MITRE ATT&CK tactics. Used by the bridge catalog and the kill-chain phase guide. |
| `collab_bp.py` | See `collab_bp` above. |
| `config_store.py` | Thread-safe config read/write helper used by modules that need to update `payload.json` without going through the CLI. |
| `cve_matcher.py` | Matches discovered service versions against the local NVD cache and the parquet CVE dataset. |
| `detailed_search.py` | Full-text search across `sessions/` artefacts and the parquet knowledge bases. |
| `lazyaddon_creator.py` | Generates `lazyaddons/*.yaml` from a GitHub URL by fetching repo metadata and inferring install/execute commands. |
| `obs_parser.py` | Observation parser. Converts raw tool output (nmap, gobuster, etc.) into typed `Finding` objects consumed by `world_model.py`. |
| `playbook_engine.py` | YAML playbook executor. Derives playbooks from the current world model, executes steps, and records outcomes. |
| `world_model.py` | Engagement world model: hosts, services, credentials, phase, objectives. Serialised to `sessions/world_model.json`. |
| `amsi.c` | AMSI bypass research code (C, compiled for Windows testing). |

## Adding a module

1. Place the `.py` file here.
2. If the module provides a Flask blueprint, register it in `lazyc2.py` with
   `app.register_blueprint(bp, url_prefix="/your-prefix")`.
3. If the module is invoked from the CLI, add a `do_<name>` wrapper in
   `lazyown.py` that delegates to `run_command("python3 modules/name.py ...")`.
4. If the module needs `payload.json` values, import `Config` from
   `core.config` and call `Config(load_payload())` — do not read the file
   directly.
5. Single-feature helpers belong here; cross-cutting helpers shared with the
   C2 belong in `utils.py`.
