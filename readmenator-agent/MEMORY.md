# Project Memory

> Cross-session context for agents. Sections 1-6 are regenerated from the source tree with zero LLM tokens: declared rules are quoted verbatim with `file:line`, measured baselines come from the scan. Section 7 is written by agents and humans and is preserved across rebuilds.

Generated from 1138 files at commit `3572cf8f9c41`. Read this first, then `readmenator-wiki/index.md`, then `readmenator . ask "<question>"` for anything specific.

## 1. Purpose and domain

- What it is: curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \ (`README.md:17`)
- Domain vocabulary (term, files): `command` (463), `modules` (439), `file` (420), `lazy` (413), `one` (401), `not` (390), `all` (386), `path` (381), `run` (377), `own` (360), `cli` (357), `name` (353), `json` (349), `without` (349), `set` (324)
- Subsystem `modules: autonomous_daemon`: 163 files, core `skills/autonomous_daemon.py`: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- Subsystem `cli/commands: utils`: 148 files, core `utils.py`: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024...
- Subsystem `cli`: 117 files, core `lazyown.py`: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date...
- Subsystem `modules: lazy_loop`: 115 files, core `modules/lazy_loop.py`: Lazy autonomous loop for LazyOwn.
- Subsystem `modules: lazyc2`: 72 files, core `lazyc2.py`: is_insecure_credential: Check for weak or default credentials
- Subsystem `lazygui/panels`: 54 files, core `lazygui/services/teamserver_backend.py`: Teamserver backend with Socket.IO real-time and full HTTP API coverage.
- Subsystem `static/js`: 43 files, core `static/js/html2pdf.bundle.min.js`: o: 3.
- Subsystem `modules: lazyown_facts`: 32 files, core `skills/lazyown_facts.py`: LazyOwn FactStore
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
- Dependency cycles: 58; layer violations: 69 (see `readmenator-agent/GOTCHAS.md`).

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
- py: 1007 files, 19192 symbols; docstrings on 55% of symbols; functions snake_case (99%); types PascalCase (100%); median file 221 lines, max 13286.
- sh: 64 files, 257 symbols; docstrings on 32% of symbols; functions snake_case (100%); median file 79 lines, max 1539.
- lua: 26 files, 45 symbols; docstrings on 0% of symbols; functions snake_case (98%); median file 72 lines, max 261.
- js: 21 files, 1606 symbols; docstrings on 49% of symbols; functions snake_case (46%); types PascalCase (26%); median file 6 lines, max 9358.
- Tests: 327 files under ., modules, poc_tui; follow the existing naming (e.g. `test_lazyencoder_decoder.py`).

## 5. Minimum deliverables

Declared:
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
- No new dependency cycles (current: 58).
- Files stay under 300 lines where possible (`readmenator . lint`).
- Docs refreshed: `readmenator . --rebuild`, and decisions recorded in section 7.

## 6. Risks to respect

- God nodes (changes ripple widely): `core/logging.py`, `utils.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `cli/commands/_base.py`
- Hotspots (complex and central): `static/js/html2pdf.bundle.min.js`, `static/js/3d-force-graph-1.73.4.min.js`, `skills/mcp_generated_tools.py`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- Cycle: `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- Full blast radius: `readmenator-agent/GOTCHAS.md`; findings: `readmenator-agent/SECURITY.md`.

## 7. Session log (preserved across rebuilds)

Append with `readmenator . remember "<note>" --kind <kind>` (kinds: business, decision, rule, workflow, style, deliverable, gotcha, todo, note) or the MCP tool `readmenator.remember`. Record business rules, decisions and their reasons, workflow changes, and anything the next session must not rediscover.

<!-- readmenator:memory:notes:begin -->
- 2026-10-19 [note] Full suite run tracked the additions of modules/verb_manifest.py, modules/chain_distill.py and CLI chain_distill; new tests live in tests/test_verb_manifest.py and tests/test_chain_distill.py --kind decision
- 2026-10-19 [decision] Typed verb manifests live in config/verb_manifests.yaml (version 1): closed fact vocabulary (host_known, service_open, os, credentials, access, session, artifact, scan_completed, services_discovered, min_version_collected, c2, fact) with host/port/service/os/scope/level/kind/path/name/state corner args; verbose verb_manifest manifests()/plan_check()/facts_for_target()/coverage() APIs; plan_check is injectable with facts list so callers can bypass world-model projection
- 2026-10-19 [decision] chain_distill policy v1: streams only kind=bash rows, drops empty-output/failure-signature/prose lines, dedupes by digest then rendered line, tokenises target from goal text then frequency, keeps intent id + digest lineage in step description, guards nmap steps with sessions/scan_{target}.nmap.xml via skip_if_exists, writes chains/distill_<task>_<goal>.yaml enabled=false only when chain_registry.validate_chain passes
- 2026-10-20 [decision] Retry/resume shipped: retry status|chain|loop CLI (cli/commands/retry_ops.py + cli/retry_support.py, modules/retry_session.py); ChainRunner command_filter; utils.sudo_available honors armed retry askpass; end-of-run retry offers in do_apt_chain + lazy_runner report_result. Tests tests/test_retry_session.py 15.
- 2026-10-20 [decision] Metasploitable2 docker lab: three documented-failing vectors now validate via lab migrations in modules/metasploitable_migrations.py (bind-udp-fallback python2.5 DNS responder, nfs-mountd-fallback userspace rpc.mountd, rlogin-root-trust /root/.rhosts + loopback hosts.allow) and spec edits (ms2_dns_recursion full dig; ms2_rlogin_trust rsh+docker-exec fallback). Verified [SHELL] x3 on a fresh container.
- 2026-10-20 [decision] pytest census chunked 12-chunk run green 5781/0 after fixing 7 failures: stale cli/command_index.json (regenerated 837), RetryOpsCommandSet missing phase/category attrs, ruff cli F401/I001 F821 YamlEditorModal import, unformatted cli files, unused Panel/Text imports in lazyown.py, CLAUDE.md test count 265 to 276, CLAUDE.md size over 40KB budget (moved section 10 to docs/coding_standards.md and 16b to docs/lint_contract.md), stale gym test object stub lacking owner attr
- 2026-10-20 [decision] lazyaddons surface as loop verbs: verb_catalog indexes enabled lazyaddons/*.yaml as addon:<name> pseudo-verbs (off by default, phase from category, trigger tokens as keywords); steps_for('auto addon:x') maps to 'lazy addon x [target]'; VerbCatalogConfig.addons_dir injectable (None keeps sandbox single-surface); docs updated (README short sentences + links, autonomous-loop.md Retry/Distill/Catalog sections, lazyaddons-yaml.md verb section, CHEATSHEET rows, COMMANDS.md regen)
<!-- readmenator:memory:notes:end -->
