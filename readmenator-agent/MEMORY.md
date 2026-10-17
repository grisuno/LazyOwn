# Project Memory

> Cross-session context for agents. Sections 1-6 are regenerated from the source tree with zero LLM tokens: declared rules are quoted verbatim with `file:line`, measured baselines come from the scan. Section 7 is written by agents and humans and is preserved across rebuilds.

Generated from 1078 files at commit `2f44e17e04bd`. Read this first, then `readmenator-wiki/index.md`, then `readmenator . ask "<question>"` for anything specific.

## 1. Purpose and domain

- What it is: curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \ (`README.md:17`)
- Domain vocabulary (term, files): `command` (432), `modules` (416), `lazy` (400), `file` (386), `all` (376), `not` (370), `one` (362), `path` (353), `run` (351), `own` (348), `cli` (340), `json` (332), `name` (328), `without` (325), `set` (304)
- Subsystem `cli/commands`: 159 files, core `utils.py`: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024...
- Subsystem `modules: lazyc2`: 135 files, core `lazyc2.py`: is_insecure_credential: Check for weak or default credentials
- Subsystem `modules: lazy_loop`: 115 files, core `modules/lazy_loop.py`: Lazy autonomous loop for LazyOwn.
- Subsystem `cli`: 112 files, core `lazyown.py`: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date...
- Subsystem `modules: autonomous_daemon`: 109 files, core `skills/autonomous_daemon.py`: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- Subsystem `lazygui/panels`: 54 files, core `lazygui/services/teamserver_backend.py`: Teamserver backend with Socket.IO real-time and full HTTP API coverage.
- Subsystem `modules: llm_budget`: 35 files, core `core/llm_budget.py`: LLM budget cap and per call token counter.
- Subsystem `static/js`: 25 files, core `static/js/html2pdf.bundle.min.js`: o: 3.
- Business rules that the code cannot show live in section 7: record them there.

## 2. Workflow

Detected commands:
- `python -m pytest -q` (pyproject.toml)
- `lazyown --help` (pyproject.toml [project.scripts])
- `make help` (Makefile)
- `CI workflow agent-contract.yml` (.github/workflows/agent-contract.yml)
- `CI workflow attack_surface_scan.yml` (.github/workflows/attack_surface_scan.yml)
- `CI workflow audit.yml` (.github/workflows/audit.yml)
- `CI workflow bootstrap-smoke.yml` (.github/workflows/bootstrap-smoke.yml)
- `CI workflow ci.yml` (.github/workflows/ci.yml)
- `CI workflow codacy.yml` (.github/workflows/codacy.yml)
- `CI workflow docker-build.yml` (.github/workflows/docker-build.yml)
- `CI workflow docker-smoke.yml` (.github/workflows/docker-smoke.yml)
- `CI workflow docs-drift.yml` (.github/workflows/docs-drift.yml)

Session protocol:
1. Start: read this file, then `readmenator . fresh` (exit 1 means run `readmenator . --rebuild`).
2. Orient: `readmenator-wiki/index.md`; for a question use `readmenator . ask "<question>"` (local = entities + sources, `--global` = community reports).
3. Before editing a file: `grep -n '<file>' readmenator-agent/GOTCHAS.md readmenator-agent/SECURITY.md`.
4. After the change: run the tests above, then `readmenator . --rebuild` so the maps, wiki, and this file stay true.
5. End: record decisions, business rules, and gotchas with `readmenator . remember "<note>" --kind decision`.

## 3. Rules and constraints

Declared:
- `core/hardening.py`: Centralized security primitives — `safe_subprocess_run`, `safe_clipboard_copy`, `set_sshpass_env`, `escape_html_content`, `safe_path_join`, `validate_host`, `validate_network_cidr`, `validate_port_spec`, `require_encryption_key`, `defused_xml_parse`, `sanitize_filename`. (`AGENTS.md:74`)
- `core/safe_exec.py`: Safe command execution — `safe_system`, `safe_run_argv`, `safe_run_shell`, `safe_clear_screen`, `validate_url`, `safe_git_clone`, `safe_ip_show`, `safe_find_tool`, `safe_file_read`. (`AGENTS.md:75`)
- `cli/commands/`: CommandSets for **db_***, **search/use/back**, **generate**, **resource** — auto-registered at boot. (`AGENTS.md:76`)
- Start every session on `dev`, but SYNC it with `main` first: `git fetch origin main dev && git checkout dev && git merge --ff-only origin/main || git merge --no-edit origin/main`. Verify with `git merge-base --is-ancestor origin/main HEAD`. Never work on a stale `dev`. (`AGENTS.md:195`)
- Never commit directly to `main` or `pp`. (`AGENTS.md:196`)
- Feature branches: `feature/<description>` cut from `dev`. (`AGENTS.md:197`)
- Hotfix branches: `hotfix/<description>` cut from `main`, then back-merge to `pp` and `dev`. (`AGENTS.md:198`)
- When instructed to release, create a PR from `dev` to `pp` (or `pp` to `main`) and request human approval. (`AGENTS.md:199`)
- Extend `base.html`, `{% include %}` partials. (`CLAUDE.md:252`)
- Mark `|safe` only when you produced the HTML. (`CLAUDE.md:253`)
- Filenames match `validate_template_name`: `^[a-zA-Z0-9_-]+\.html$`. (`CLAUDE.md:254`)
- Use the [Issues tab](https://github.com/grisuno/LazyOwn/issues) for bugs and feature requests. (`CONTRIBUTING.md:58`)
- For **security vulnerabilities**, please report them responsibly (contact the maintainer privately if possible). (`CONTRIBUTING.md:59`)

Measured baseline:
- Security findings at medium or above: 0 (see `readmenator-agent/SECURITY.md`); do not add new ones.
- Dependency cycles: 72; layer violations: 67 (see `readmenator-agent/GOTCHAS.md`).

## 4. Style norms

Declared:
- One class `LazyOwnShell(cmd2.Cmd)`. Subclass `CommandSet` only when meaningfully orthogonal. (`CLAUDE.md:189`)
- Methods `do_<name>(self, line)`; docstring = `help <name>`. (`CLAUDE.md:190`)
- Args: `@with_argparser(parser)` for non-trivial; `@with_argument_list` for simple split. (`CLAUDE.md:191`)
- `@with_category('Recon')` etc. — keep existing names. (`CLAUDE.md:192`)
- Aliases: `aliases` dict at class level; payload-derived aliases use class-body `f""` (refresh on shell restart). (`CLAUDE.md:193`)
- `self.params` mirrors `payload.json`. Write back via `do_assign`/`do_set` only. (`CLAUDE.md:194`)
- [About coordinated disclosure of security vulnerabilities](https://docs.github.com/en/code-security/security-advisories/about-coordinated-disclosure-of-security-vulnerabilities) (`SECURITY.md:40`)
- [About repository security advisories](https://docs.github.com/en/code-security/security-advisories/about-repository-security-advisories) (`SECURITY.md:41`)

Measured baseline:
- py: 949 files, 18271 symbols; docstrings on 55% of symbols; functions snake_case (99%); types PascalCase (100%); median file 222 lines, max 12887.
- sh: 62 files, 204 symbols; docstrings on 41% of symbols; functions snake_case (100%); median file 78 lines, max 1539.
- lua: 26 files, 45 symbols; docstrings on 0% of symbols; functions snake_case (98%); median file 72 lines, max 261.
- js: 21 files, 1606 symbols; docstrings on 49% of symbols; functions snake_case (46%); types PascalCase (26%); median file 6 lines, max 9358.
- Tests: 296 files under ., modules, poc_tui; follow the existing naming (e.g. `test_lazyencoder_decoder.py`).

## 5. Minimum deliverables

Declared:
- **English only.** Identifiers, strings, logs, docstrings. Translate Spanish remnants when you touch them. (`CLAUDE.md:334`)
- **No comments.** Self-explanatory names + docstrings. Single-line note OK for non-obvious constraint or CVE ref. (`CLAUDE.md:335`)
- **No emojis** in code/logs/docs unless operator asked. Banner ASCII art OK. (`CLAUDE.md:336`)
- **Docstrings on every public function/class**: (`CLAUDE.md:337`)
- **No magic numbers** — constants in `class Config` (shared) or `UPPER_SNAKE_CASE` module-level. (`CLAUDE.md:350`)
- **No hardcoded paths/ports/IPs/wordlists/creds** — `payload.json` if reused, module constant if local. (`CLAUDE.md:351`)
- **S**: one reason to change per class/fn. (`CLAUDE.md:353`)
- **O**: extend via new addon/MCP tool/selector — don't edit hot paths. (`CLAUDE.md:354`)
- **L**: new selector honours `BaseSelector.suggest()` contract. (`CLAUDE.md:355`)
- **I**: small role-specific protocols (recon/exploit/cred/lateral/privesc). (`CLAUDE.md:356`)
- **D**: orchestration depends on `LLMBackend`/`MemoryStore`/`Selector` abstractions, not Groq/ChromaDB directly. (`CLAUDE.md:357`)
- **Consistency beats novelty** — when two patterns fit, pick the one already used. (`CLAUDE.md:358`)
- **No partial implementations** — end-to-end (CLI ↔ payload.json ↔ MCP ↔ `sessions/` artefact) or not merged. (`CLAUDE.md:359`)
- **No backwards-compat shims** for unshipped code — just change it. (`CLAUDE.md:360`)
- **Every new directory gets a README** (see §2 rules). No exceptions. (`CLAUDE.md:361`)
- **Boy-scout law (tech debt).** When a fix / refactor / new feature uncovers tech debt or a vulnerability that can be addressed **without breaking public surface or shipped behaviour**, address it in the same change and call it out in the PR body. Plan with `/graphify` first so the blast radius is understood — never refactor blindly. If the cleanup is unsafe within the change, open a follow-up task; do **not** silently leave the broken window. (`CLAUDE.md:362`)
- **Smart consolidation (DRY+SOLID).** When two or more code paths duplicate logic (~10 LOC or one decision tree), consolidate into a single class/function honouring SOLID. Shared values go to `class Config` / `payload.json` if globally reused, module-level `UPPER_SNAKE_CASE` if local. Refactor must keep every existing call site working and ship with tests that pin behaviour **before** the move. No silent simplifications — feature parity is mandatory. (`CLAUDE.md:363`)
- **Tests trend to 100%.** Every change ships with tests. If a touched module gains testable code, the change must raise coverage, not lower it. `pytest -q` must stay green. No `skip` / `xfail` without an issue link in the same PR. (`CLAUDE.md:364`)
- **Docs follow code.** When a public surface (CLI verb, MCP tool, payload key, blueprint route, addon schema) is added or renamed, update the matching `docs/<topic>.md` and regenerate `COMMANDS.md` / `UTILS.md` via `python3 readmeneitor.py lazyown.py` and `python3 readmeneitor.py utils.py`. Missing or empty docstrings on new public API block merge. Extend `readmeneitor.py` itself when a new source file deserves auto-generated reference docs. (`CLAUDE.md:365`)
- **Code Quality**: Code must be clean, readable, and follow project conventions. (`CONTRIBUTING.md:46`)
- **Tests**: Ensure all tests pass and new tests have been added for introduced changes. (`CONTRIBUTING.md:47`)
- **Documentation**: Significant changes must be well documented. (`CONTRIBUTING.md:48`)
- Fork the repository (`CONTRIBUTING.md:62`)
- Create a feature branch (`git checkout -b feature/amazing-feature`) (`CONTRIBUTING.md:63`)
- Make your changes (`CONTRIBUTING.md:64`)
- Ensure the code follows the existing style (`CONTRIBUTING.md:65`)
- Test your changes thoroughly (`CONTRIBUTING.md:66`)
- Submit a Pull Request with a clear description (`CONTRIBUTING.md:67`)

Measured baseline:
- Tests pass: `python -m pytest -q`.
- Docstring coverage stays at or above 53%.
- No new security findings at medium or above (current: 0).
- No new dependency cycles (current: 72).
- Files stay under 300 lines where possible (`readmenator . lint`).
- Docs refreshed: `readmenator . --rebuild`, and decisions recorded in section 7.

## 6. Risks to respect

- God nodes (changes ripple widely): `core/logging.py`, `utils.py`, `skills/lazyown_mcp.py`, `cli/commands/_base.py`, `modules/lazy_loop.py`
- Hotspots (complex and central): `static/js/html2pdf.bundle.min.js`, `static/js/3d-force-graph-1.73.4.min.js`, `skills/mcp_generated_tools.py`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`
- Cycle: `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- Cycle: `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- Cycle: `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- Full blast radius: `readmenator-agent/GOTCHAS.md`; findings: `readmenator-agent/SECURITY.md`.

## 7. Session log (preserved across rebuilds)

Append with `readmenator . remember "<note>" --kind <kind>` (kinds: business, decision, rule, workflow, style, deliverable, gotcha, todo, note) or the MCP tool `readmenator.remember`. Record business rules, decisions and their reasons, workflow changes, and anything the next session must not rediscover.

<!-- readmenator:memory:notes:begin -->
<!-- readmenator:memory:notes:end -->
