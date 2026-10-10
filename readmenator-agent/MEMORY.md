# Project Memory

> Cross-session context for agents. Sections 1-6 are regenerated from the source tree with zero LLM tokens: declared rules are quoted verbatim with `file:line`, measured baselines come from the scan. Section 7 is written by agents and humans and is preserved across rebuilds.

Generated from 898 files at commit `f888cc8541c0`. Read this first, then `readmenator-wiki/index.md`, then `readmenator . ask "<question>"` for anything specific.

## 1. Purpose and domain

- What it is: curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \ (`README.md:17`)
- Domain vocabulary (term, files): `command` (373), `modules` (342), `all` (330), `file` (325), `not` (317), `own` (307), `lazy` (304), `cli` (289), `json` (283), `path` (275), `run` (274), `name` (273), `set` (266), `commands` (252), `without` (250)
- Subsystem `modules: autonomous_daemon`: 142 files, core `skills/autonomous_daemon.py`: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- Subsystem `cli/commands`: 136 files, core `utils.py`: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024...
- Subsystem `cli`: 89 files, core `lazyown.py`: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date...
- Subsystem `lazyc2/security`: 63 files, core `lazyc2.py`: is_insecure_credential: Check for weak or default credentials
- Subsystem `modules: wizard`: 54 files, core `cli/wizard.py`: Guided first-run setup wizard for the LazyOwn framework.
- Subsystem `lazygui/panels`: 54 files, core `lazygui/services/teamserver_backend.py`: Teamserver backend with Socket.IO real-time and full HTTP API coverage.
- Subsystem `modules: world_model`: 37 files, core `modules/world_model.py`: modules/world_model.py
- Subsystem `skills/claude_md_orchestrator`: 30 files, core `skills/claude_md_orchestrator/models.py`: Data models for the claude_md_orchestrator skill.
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
- Extend `base.html`, `{% include %}` partials. (`CLAUDE.md:254`)
- Mark `|safe` only when you produced the HTML. (`CLAUDE.md:255`)
- Filenames match `validate_template_name`: `^[a-zA-Z0-9_-]+\.html$`. (`CLAUDE.md:256`)
- Use the [Issues tab](https://github.com/grisuno/LazyOwn/issues) for bugs and feature requests. (`CONTRIBUTING.md:58`)
- For **security vulnerabilities**, please report them responsibly (contact the maintainer privately if possible). (`CONTRIBUTING.md:59`)

Measured baseline:
- Security findings at medium or above: 0 (see `readmenator-agent/SECURITY.md`); do not add new ones.
- Dependency cycles: 21; layer violations: 65 (see `readmenator-agent/GOTCHAS.md`).

## 4. Style norms

Declared:
- One class `LazyOwnShell(cmd2.Cmd)`. Subclass `CommandSet` only when meaningfully orthogonal. (`CLAUDE.md:191`)
- Methods `do_<name>(self, line)`; docstring = `help <name>`. (`CLAUDE.md:192`)
- Args: `@with_argparser(parser)` for non-trivial; `@with_argument_list` for simple split. (`CLAUDE.md:193`)
- `@with_category('Recon')` etc. — keep existing names. (`CLAUDE.md:194`)
- Aliases: `aliases` dict at class level; payload-derived aliases use class-body `f""` (refresh on shell restart). (`CLAUDE.md:195`)
- `self.params` mirrors `payload.json`. Write back via `do_assign`/`do_set` only. (`CLAUDE.md:196`)
- [About coordinated disclosure of security vulnerabilities](https://docs.github.com/en/code-security/security-advisories/about-coordinated-disclosure-of-security-vulnerabilities) (`SECURITY.md:40`)
- [About repository security advisories](https://docs.github.com/en/code-security/security-advisories/about-repository-security-advisories) (`SECURITY.md:41`)

Measured baseline:
- py: 776 files, 15180 symbols; docstrings on 49% of symbols; functions snake_case (99%); types PascalCase (100%); median file 238 lines, max 11599.
- sh: 57 files, 202 symbols; docstrings on 41% of symbols; functions snake_case (100%); median file 73 lines, max 1532.
- lua: 26 files, 45 symbols; docstrings on 0% of symbols; functions snake_case (98%); median file 72 lines, max 261.
- js: 19 files, 1355 symbols; docstrings on 41% of symbols; functions snake_case (44%); types PascalCase (18%); median file 6 lines, max 9358.
- Tests: 207 files under ., modules, poc_tui; follow the existing naming (e.g. `test_lazyencoder_decoder.py`).

## 5. Minimum deliverables

Declared:
- **English only.** Identifiers, strings, logs, docstrings. Translate Spanish remnants when you touch them. (`CLAUDE.md:336`)
- **No comments.** Self-explanatory names + docstrings. Single-line note OK for non-obvious constraint or CVE ref. (`CLAUDE.md:337`)
- **No emojis** in code/logs/docs unless operator asked. Banner ASCII art OK. (`CLAUDE.md:338`)
- **Docstrings on every public function/class**: (`CLAUDE.md:339`)
- **No magic numbers** — constants in `class Config` (shared) or `UPPER_SNAKE_CASE` module-level. (`CLAUDE.md:352`)
- **No hardcoded paths/ports/IPs/wordlists/creds** — `payload.json` if reused, module constant if local. (`CLAUDE.md:353`)
- **S**: one reason to change per class/fn. (`CLAUDE.md:355`)
- **O**: extend via new addon/MCP tool/selector — don't edit hot paths. (`CLAUDE.md:356`)
- **L**: new selector honours `BaseSelector.suggest()` contract. (`CLAUDE.md:357`)
- **I**: small role-specific protocols (recon/exploit/cred/lateral/privesc). (`CLAUDE.md:358`)
- **D**: orchestration depends on `LLMBackend`/`MemoryStore`/`Selector` abstractions, not Groq/ChromaDB directly. (`CLAUDE.md:359`)
- **Consistency beats novelty** — when two patterns fit, pick the one already used. (`CLAUDE.md:360`)
- **No partial implementations** — end-to-end (CLI ↔ payload.json ↔ MCP ↔ `sessions/` artefact) or not merged. (`CLAUDE.md:361`)
- **No backwards-compat shims** for unshipped code — just change it. (`CLAUDE.md:362`)
- **Every new directory gets a README** (see §2 rules). No exceptions. (`CLAUDE.md:363`)
- **Boy-scout law (tech debt).** When a fix / refactor / new feature uncovers tech debt or a vulnerability that can be addressed **without breaking public surface or shipped behaviour**, address it in the same change and call it out in the PR body. Plan with `/graphify` first so the blast radius is understood — never refactor blindly. If the cleanup is unsafe within the change, open a follow-up task; do **not** silently leave the broken window. (`CLAUDE.md:364`)
- **Smart consolidation (DRY+SOLID).** When two or more code paths duplicate logic (~10 LOC or one decision tree), consolidate into a single class/function honouring SOLID. Shared values go to `class Config` / `payload.json` if globally reused, module-level `UPPER_SNAKE_CASE` if local. Refactor must keep every existing call site working and ship with tests that pin behaviour **before** the move. No silent simplifications — feature parity is mandatory. (`CLAUDE.md:365`)
- **Tests trend to 100%.** Every change ships with tests. If a touched module gains testable code, the change must raise coverage, not lower it. `pytest -q` must stay green. No `skip` / `xfail` without an issue link in the same PR. (`CLAUDE.md:366`)
- **Docs follow code.** When a public surface (CLI verb, MCP tool, payload key, blueprint route, addon schema) is added or renamed, update the matching `docs/<topic>.md` and regenerate `COMMANDS.md` / `UTILS.md` via `python3 readmeneitor.py lazyown.py` and `python3 readmeneitor.py utils.py`. Missing or empty docstrings on new public API block merge. Extend `readmeneitor.py` itself when a new source file deserves auto-generated reference docs. (`CLAUDE.md:367`)
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
- Docstring coverage stays at or above 47%.
- No new security findings at medium or above (current: 0).
- No new dependency cycles (current: 21).
- Files stay under 300 lines where possible (`readmenator . lint`).
- Docs refreshed: `readmenator . --rebuild`, and decisions recorded in section 7.

## 6. Risks to respect

- God nodes (changes ripple widely): `core/logging.py`, `utils.py`, `cli/commands/_base.py`, `skills/lazyown_mcp.py`, `lazyc2.py`
- Hotspots (complex and central): `static/js/html2pdf.bundle.min.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `static/js/xterm.js`, `static/js/quill-2.0.3.js`
- Cycle: `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- Cycle: `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- Cycle: `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- Cycle: `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- Cycle: `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- Full blast radius: `readmenator-agent/GOTCHAS.md`; findings: `readmenator-agent/SECURITY.md`.

## 7. Session log (preserved across rebuilds)

Append with `readmenator . remember "<note>" --kind <kind>` (kinds: business, decision, rule, workflow, style, deliverable, gotcha, todo, note) or the MCP tool `readmenator.remember`. Record business rules, decisions and their reasons, workflow changes, and anything the next session must not rediscover.

<!-- readmenator:memory:notes:begin -->
<!-- readmenator:memory:notes:end -->
