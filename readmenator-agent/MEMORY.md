# Project Memory

> Cross-session context for agents. Sections 1-6 are regenerated from the source tree with zero LLM tokens: declared rules are quoted verbatim with `file:line`, measured baselines come from the scan. Section 7 is written by agents and humans and is preserved across rebuilds.

Generated from 1266 files at commit `230476b24269`. Read this first, then `readmenator-wiki/index.md`, then `readmenator . ask "<question>"` for anything specific.

## 1. Purpose and domain

- What it is: curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \ (`README.md:17`)
- Domain vocabulary (term, files): `modules` (513), `command` (505), `one` (490), `lazy` (476), `file` (471), `path` (431), `run` (429), `not` (428), `all` (407), `without` (399), `name` (394), `json` (391), `cli` (379), `own` (379), `set` (353)
- Subsystem `modules: autonomous_daemon`: 158 files, core `skills/autonomous_daemon.py`: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- Subsystem `cli/commands`: 135 files, core `utils.py`: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024...
- Subsystem `cli`: 115 files, core `lazyown.py`: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date...
- Subsystem `modules: world_model`: 113 files, core `modules/world_model.py`: modules/world_model.py
- Subsystem `modules: lazy_loop`: 109 files, core `modules/lazy_loop.py`: Lazy autonomous loop for LazyOwn.
- Subsystem `modules: lazyc2`: 76 files, core `lazyc2.py`: is_insecure_credential: Check for weak or default credentials
- Subsystem `static/js`: 64 files, core `static/js/html2pdf.bundle.min.js`: o: 3.
- Subsystem `modules: lazyown_facts`: 59 files, core `skills/lazyown_facts.py`: LazyOwn FactStore
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
- Dependency cycles: 120; layer violations: 70 (see `readmenator-agent/GOTCHAS.md`).

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
- py: 1135 files, 21163 symbols; docstrings on 56% of symbols; functions snake_case (99%); types PascalCase (100%); median file 209 lines, max 12026.
- sh: 64 files, 258 symbols; docstrings on 33% of symbols; functions snake_case (100%); median file 79 lines, max 1539.
- lua: 26 files, 45 symbols; docstrings on 0% of symbols; functions snake_case (98%); median file 72 lines, max 261.
- js: 21 files, 1606 symbols; docstrings on 49% of symbols; functions snake_case (46%); types PascalCase (26%); median file 6 lines, max 9358.
- Tests: 396 files under ., modules, poc_tui; follow the existing naming (e.g. `test_lazyencoder_decoder.py`).

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
- Docstring coverage stays at or above 54%.
- No new security findings at medium or above (current: 0).
- No new dependency cycles (current: 120).
- Files stay under 300 lines where possible (`readmenator . lint`).
- Docs refreshed: `readmenator . --rebuild`, and decisions recorded in section 7.

## 6. Risks to respect

- God nodes (changes ripple widely): `core/logging.py`, `modules/lazy_loop.py`, `utils.py`, `cli/commands/_base.py`, `skills/lazyown_mcp.py`
- Hotspots (complex and central): `static/js/html2pdf.bundle.min.js`, `static/js/3d-force-graph-1.73.4.min.js`, `skills/mcp_generated_tools.py`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`
- Cycle: `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- Cycle: `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- Cycle: `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- Cycle: `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- Cycle: `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
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
- 2026-10-25 [decision] zone.ci audit cross-check on dev (0.2.160 claims): confirmed JA3 simulating c2_profile_engine.py:158; socks specification-only modules/socks_proxy.py:8; static AES {key} embedded implant_crypt.go:1799; plaintext /config.json implant_crypt.go:1716; beacon HMAC default off lazyc2.py:3526 (server impl exists, gated c2_require_beacon_hmac); rootkit LISTENER_IP hardcoded modules/rootkit/rootkit.c:28; backdoor Hacked runkey+MessageBox modules/backdoor/backdoor.c:38,158; auto-privesc now first-check...
- 2026-10-25 [note] Audit remediation P0-P4 applied on feature/audit-remediation-p0: beacon HMAC default-on + per-build rat_key bootstrap via core.config.ensure_rat_key; implant signs wire body and seeds baked-in defaults; noisy check-in pipelines behind auto_privesc_on_checkin/auto_discover_on_checkin (default off); rootkit/backdoor operator-identity hardcodes guarded; hygiene_audit command + audit_hygiene chain; lazyown_set_config sanctioned writer in utils
- 2026-10-25 [decision] Audit wave 2 (rotative session secrets) applied: core/session_secrets.py rotates aes_key (sessions/key.aes 32B 0600) + rat_key (64 hex) + session_magic (32 hex); C2 boot rotates when rotate_keys_on_boot=true; _beacon_signature_guard re-reads rat_key from payload.json per request and encrypt_data/decrypt_data reload key.aes on byte change so out-of-process rotation never strands the running C2; clean (shellsys.do_clean) deletes key.aes + c2_lab.json then rotates; payload.json writes now MERGE...
- 2026-10-27 [decision] WinBox gym (totekuh/winbox) integrated as second Red Team Gym scenario: modules/winbox_gym.py is the single control plane (catalogue playbooks/gym_winbox.yaml + exploits/winbox_*.yaml + chains/gym_winbox_*.yaml + safe allowlisted CLI adapter); cli/commands/winbox_gym.py exposes the winbox shell command; lazyaddons/winbox.yaml registers upstream repo as trigger-only addon (name collides with built-in do_winbox by design); gym_matrix_runner and ctf_capture take an injectable catalogue param (me...
- 2026-10-27 [decision] WinBox lab bootstrap is one command: winbox up / winbox setup / gym start <winbox challenge> all call winbox_gym.ensure_lab_ready (install -> ensure_prereqs via sudo -n apt-get -> iso download -> winbox setup -y -> up -> rhost bind), idempotent and fail-fast with manual guidance when sudo needs a password; the lazyaddons/winbox.yaml install_command mirrors the same apt-get install line + pip install -e . with --break-system-packages fallback for PEP 668; gym start auto-launches apt_chain <cha...
- 2026-10-29 [decision] vulnerator-ai adoption: lazy_findings ledger (fail-closed confirmed evidence), progress_ledger 3-strikes handoff, engagement modes pentest/redteam/ctf, scope denylist priority, ATT&CK technique_id via killchain mapping — all config in orchestrator.yaml profiles + payload overrides
- 2026-10-29 [decision] apt_ad_lab_karrab chain: Karrab AD methodology mapped to Samba DC lab — 9 new vectors (passpol T1201, kerbrute_userenum T1087.002, asreproast T1558.005, passspray T1110.003 policy-gated fixture password only, gpp_sysvol T1552.006, user_desc_secrets T1552.008, gmsa_enum T1552.006, delegation_enum T1558.003, dcsync_validation T1003.006); gym_ad_lab matrix now 14 vectors; chain vuln defaults must match playbook ids (ad_<slug> not ad_lab_<slug>); AS-REP roast via LDAP userAccountControl 4194304 n...
- 2026-10-29 [decision] ad_surface trigger (loop_triggers TRIGGER_KINDS + ensure_ad_surface_trigger + lazy_loop run_round seeding from yaml 'triggers: - kind: ad_surface every_sec: 1800'): grades mitm6/LLMNR/SMB-relay/NTLMv1-downgrade viability via modules/lazy_netattack.SurfaceEvidence (services + os_hint + operator-attested signing at sessions/smb_signing.json via lazy_netattack attest); grades land as hint nodes with fingerprint dedupe — kinetic steps NEVER auto-run, consent tokens gate chains (apt_ad_windows def...
<!-- readmenator:memory:notes:end -->
