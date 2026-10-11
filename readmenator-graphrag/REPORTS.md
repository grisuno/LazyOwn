# GraphRAG Community Reports

Entities: 19327 | Relationships: 58379 | Communities: 26 | Themes: 11 | Text units: 19196

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

961 files in 26 communities and 11 themes. Highest-impact communities: cli/commands (7.0), modules: lazyown (6.0), modules: autonomous_daemon (5.1). God nodes: core/logging.py, utils.py, cli/commands/_base.py, skills/lazyown_mcp.py, lazyc2.py.

- [cli/commands] rating 7.0: `utils.py` ranks 1 by PageRank, 106 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazyown] rating 6.0: `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: autonomous_daemon] rating 5.1: `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [unassigned files] rating 4.4: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: lazy_sentinel4] rating 3.4: `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli: status_bar] rating 2.6: `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [static/js] rating 2.6: `core/config.py` ranks 1 by PageRank, 63 importers, 17 symbols: Configuration loader and Config wrapper.
- [lazygui/panels] rating 2.3: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- Key entities: file:utils.py, file:tests/test_categories.py, file:lazyown.py, file:tests/test_collab_and_onboarding.py, file:skills/lazyown_mcp.py, file:tests/test_improvements_spec.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
- Root rating = highest community rating.

## cli/commands + modules: kerberos_core +3 (`t3`, theme, rating 7.0)

Theme of 5 communities and 143 files: cli/commands (118 files, rating 7.0); modules: kerberos_core (7 files, rating 0.2); modules: saas_attacks (7 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 106 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:utils.py, file:tests/test_categories.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py
- Children: c0, c13, c14, c17, c16
- Theme rating = highest child community rating.

## modules: lazyown + modules: lazy_sentinel4 +4 (`t1`, theme, rating 6.0)

Theme of 6 communities and 229 files: modules: lazyown (70 files, rating 6.0); modules: lazy_sentinel4 (64 files, rating 3.4); cli: status_bar (61 files, rating 2.6); cli: banner_config (19 files, rating 1.0); cli: exploration (9 files, rating 0.4); modules: network_opsec (6 files, rating 0.1).

- [modules: lazyown] `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyown] `core/safe_exec.py` ranks 2 by PageRank, 47 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- [modules: lazy_sentinel4] `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: lazy_sentinel4] `modules/llm_factory.py` ranks 2 by PageRank, 27 importers, 22 symbols: LLM backend factory and selection utilities.
- [cli: status_bar] `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [cli: status_bar] `core/text_utils.py` ranks 2 by PageRank, 8 importers, 1 symbols: Shared text helpers for terminal surfaces.
- [cli: banner_config] `modules/cli_auth.py` ranks 1 by PageRank, 19 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- [cli: banner_config] `cli/engagement_hooks.py` ranks 2 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- Key entities: file:lazyown.py, file:tests/test_collab_and_onboarding.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, file:tests/test_tips_engine.py, file:cli/banner_config.py, file:tests/test_engagement_and_ping.py
- Children: c2, c3, c4, c10, c12, c15
- Theme rating = highest child community rating.

## modules: autonomous_daemon + static/js +5 (`t0`, theme, rating 5.1)

Theme of 7 communities and 359 files: modules: autonomous_daemon (115 files, rating 5.1); static/js (55 files, rating 2.6); lazygui/panels (54 files, rating 2.3); lazyc2/security (53 files, rating 2.0); modules: dashboard_tui (38 files, rating 1.9); skills/claude_md_orchestrator (19 files, rating 0.9); modules: lazy_loop (25 files, rating 0.9).

- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [modules: autonomous_daemon] `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 148 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [static/js] `core/config.py` ranks 1 by PageRank, 63 importers, 17 symbols: Configuration loader and Config wrapper.
- [static/js] `core/payload_schema.py` ranks 2 by PageRank, 13 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- [lazygui/panels] `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [lazygui/panels] `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- [lazyc2/security] `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- [lazyc2/security] `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- Key entities: file:skills/lazyown_mcp.py, file:tests/test_improvements_spec.py, file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:lazyc2.py, file:modules/lazy_rbac.py
- Children: c1, c5, c6, c7, c8, c11, c9
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 4.4)

Theme of 1 communities and 215 files: unassigned files (215 files, rating 4.4).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c25
- Theme rating = highest child community rating.

## tools (`t10`, theme, rating 0.1)

Theme of 1 communities and 2 files: tools (2 files, rating 0.1).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c24
- Theme rating = highest child community rating.

## scripts: journal (`t4`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c18
- Theme rating = highest child community rating.

## modules/backdoor (`t5`, theme, rating 0.1)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.1).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c19
- Theme rating = highest child community rating.

## poc_tui (`t6`, theme, rating 0.1)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.1).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c20
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t7`, theme, rating 0.1)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.1).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c21
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t8`, theme, rating 0.1)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.1).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c22
- Theme rating = highest child community rating.

## test (`t9`, theme, rating 0.1)

Theme of 1 communities and 2 files: test (2 files, rating 0.1).

- [test] `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- [test] `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59
- Children: c23
- Theme rating = highest child community rating.

## cli/commands (`c0`, community, rating 7.0)

118 files under cli/commands (py 117, c 1), mostly utility. Core file utils.py (PageRank 0.0283, imported by 106 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, parse_ip_mac, create_arp_packet. Depends on static/js (23), modules: dashboard_tui (23), modules: lazyown (19). Used by static/js (27), modules: lazyown (20), modules: autonomous_daemon (17).

- `utils.py` ranks 1 by PageRank, 106 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 93 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 121 symbols, 195 connections (score 0.08).
- Hotspot `tests/test_security_hardening_v3.py`: 64 symbols, 107 connections (score 0.04).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:utils.py, file:tests/test_categories.py, file:tests/test_security_hardening_v3.py, file:cli/cli_enhancements.py, sym:cli/commands/_base.py::LazyOwnCommandSet@52, file:tests/test_cli_command_sets.py, file:cli/commands/_base.py, file:cli/commands/misc_migrated.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 374.

## modules: lazyown (`c2`, community, rating 6.0)

70 files under modules (py 69, c 1), mostly utility. Core file core/logging.py (PageRank 0.0765, imported by 159 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on cli: status_bar (22), cli/commands (20), static/js (20). Used by modules: autonomous_daemon (73), lazyc2/security (27), modules: lazy_sentinel4 (24).

- `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `core/safe_exec.py` ranks 2 by PageRank, 47 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- `core/crypto.py` ranks 3 by PageRank, 15 importers, 7 symbols: Symmetric primitives used by the framework.
- Hotspot `lazyown.py`: 127 symbols, 191 connections (score 0.09).
- Hotspot `tests/test_collab_and_onboarding.py`: 91 symbols, 29 connections (score 0.05).
- Dependency cycle: autonomous_daemon.py -> lazyown_mcp.py -> pipeline_engine.py -> autonomous_daemon.py.
- 11 layer violations, e.g. test_api_v1.py (testing) -> api_authz.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:lazyown.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/pipeline_engine.py, file:tests/test_security_hardening_v4.py, file:tests/test_pipeline_engine.py, file:modules/rootkit/rootkit.c, file:modules/collab_bp.py
- Rating 6.0/10 = 7 x PageRank share 0.86 + 3 x risk 0.00. Internal imports: 277.

## modules: autonomous_daemon (`c1`, community, rating 5.1)

115 files under modules (py 115), mostly utility. Core file cli/commands/enum.py (PageRank 0.0279, imported by 23 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyown (73), modules: dashboard_tui (29), cli: status_bar (28). Used by static/js (18), cli/commands (14), modules: lazyown (13).

- `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 148 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `modules/llm_client.py` ranks 3 by PageRank, 6 importers, 11 symbols: LazyOwn Unified LLM Client
- Hotspot `skills/autonomous_daemon.py`: 148 symbols, 256 connections (score 0.10).
- Hotspot `skills/lazyown_mcp.py`: 125 symbols, 416 connections (score 0.10).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:tests/test_improvements_spec.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:skills/tests/test_hive_mind.py
- Rating 5.1/10 = 7 x PageRank share 0.73 + 3 x risk 0.00. Internal imports: 639.

## unassigned files (`c25`, community, rating 4.4)

215 files under modules (py 114, sh 56, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0005, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.37).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 1193 connections (score 0.08).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c, file:modules/rootkit/mrhyde2.c
- Rating 4.4/10 = 7 x PageRank share 0.63 + 3 x risk 0.00. Internal imports: 0.

## modules: lazy_sentinel4 (`c3`, community, rating 3.4)

64 files under modules (py 64), mostly utility. Core file core/console.py (PageRank 0.0209, imported by 62 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: lazyown (24), cli/commands (14), static/js (7). Used by modules: autonomous_daemon (19), cli/commands (15), static/js (14).

- `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/llm_factory.py` ranks 2 by PageRank, 27 importers, 22 symbols: LLM backend factory and selection utilities.
- `modules/logging_config.py` ranks 3 by PageRank, 37 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `tests/test_aci_planner.py`: 95 symbols, 85 connections (score 0.06).
- Hotspot `lazy_sentinel4.py`: 47 symbols, 31 connections (score 0.03).
- Taint: 3 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _run_single_search).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, sym:core/console.py::print_warn@149, file:tests/test_aci_planner.py, file:lazy_sentinel4.py, file:cli/wizard.py, file:core/llm_budget.py, file:modules/logging_config.py
- Rating 3.4/10 = 7 x PageRank share 0.49 + 3 x risk 0.00. Internal imports: 185.

## cli: status_bar (`c4`, community, rating 2.6)

61 files under tests (py 61), mostly utility. Core file cli/themes.py (PageRank 0.0052, imported by 17 files): Theme registry for the LazyOwn TUI surfaces. Key abstractions: Theme, get_theme, theme_from_payload, truncate_text, ContainerCommandSet, do_docker_enum. Depends on modules: lazy_sentinel4 (10), modules: autonomous_daemon (8), modules: lazyown (6). Used by modules: autonomous_daemon (28), modules: lazyown (22), cli/commands (19).

- `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `core/text_utils.py` ranks 2 by PageRank, 8 importers, 1 symbols: Shared text helpers for terminal surfaces.
- `cli/commands/containers.py` ranks 3 by PageRank, 9 importers, 7 symbols: Container and Kubernetes attack command set.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_tips_engine.py`: 67 symbols, 6 connections (score 0.04).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_command_palette.py, file:tests/test_tips_engine.py, file:cli/status_bar.py, file:cli/tips_engine.py, file:cli/palette_command.py, file:tests/test_phase1_data_gaps.py, file:poc_tui/app.py, file:cli/graph_advisor.py
- Rating 2.6/10 = 7 x PageRank share 0.38 + 3 x risk 0.00. Internal imports: 235.

## static/js (`c5`, community, rating 2.6)

55 files under static/js (py 39, js 14, c 1, sh 1), mostly utility. Core file core/config.py (PageRank 0.0116, imported by 63 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (27), modules: autonomous_daemon (18), modules: lazyown (18). Used by cli/commands (23), modules: lazyown (20), modules: lazy_sentinel4 (7).

- `core/config.py` ranks 1 by PageRank, 63 importers, 17 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 13 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- `core/process.py` ranks 3 by PageRank, 20 importers, 12 symbols: Process and subprocess utilities for the LazyOwn framework.
- Hotspot `static/js/html2pdf.bundle.min.js`: 695 symbols, 5934 connections (score 0.81).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 8744 connections (score 0.70).
- 1 layer violations, e.g. test_core_defaults.py (testing) -> api.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Dataflow: 12 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:tests/test_payload_schema.py
- Rating 2.6/10 = 7 x PageRank share 0.37 + 3 x risk 0.00. Internal imports: 327.

## lazygui/panels (`c6`, community, rating 2.3)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0087, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyown (6), modules: autonomous_daemon (2), lazyc2/security (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 2.3/10 = 7 x PageRank share 0.33 + 3 x risk 0.00. Internal imports: 181.

## lazyc2/security (`c7`, community, rating 2.0)

53 files under tests (py 51, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0067, imported by 20 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on modules: lazyown (27), modules: dashboard_tui (13), cli/commands (7). Used by cli: banner_config (5), modules: lazyown (4), cli/commands (2).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- `lazyc2/security/cors.py` ranks 3 by PageRank, 4 importers, 15 symbols: CORS origin allowlist policy for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 277 symbols, 242 connections (score 0.18).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 857 connections (score 0.08).
- 29 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _probe_bind).
- Key entities: file:lazyc2.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_security_lazyc2.py, sym:lazyc2.py::index@3026, sym:lazyc2.py::decoy@1898, file:lazyc2/addon_creator.py, file:tests/test_api_authz.py
- Rating 2.0/10 = 7 x PageRank share 0.28 + 3 x risk 0.00. Internal imports: 119.

## modules: dashboard_tui (`c8`, community, rating 1.9)

38 files under modules (py 38), mostly utility. Core file modules/world_model.py (PageRank 0.0104, imported by 75 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: autonomous_daemon (10), cli/commands (9), cli: status_bar (8). Used by modules: autonomous_daemon (29), cli/commands (23), static/js (17).

- `modules/world_model.py` ranks 1 by PageRank, 75 importers, 61 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `skills/hermes-lazyown/constants.py` ranks 3 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- Hotspot `modules/world_model.py`: 61 symbols, 94 connections (score 0.04).
- Hotspot `cli/dashboard_tui.py`: 64 symbols, 51 connections (score 0.04).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:cli/dashboard_tui.py, file:modules/world_model.py, file:cli/ops_commands.py, file:tests/test_killchain_unified_v2.py, file:cli/commands/exploit_migrated.py, file:modules/killchain.py, file:skills/hermes-lazyown/mcp_server.py, file:tests/test_world_model_extended.py
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 96.

## cli: banner_config (`c10`, community, rating 1.0)

19 files under tests (py 19), mostly utility. Core file modules/cli_auth.py (PageRank 0.0050, imported by 19 files): CLI authentication module — login against users.json with remember-me. Key abstractions: user_exists, register, verify_password, login, logout, try_auto_login. Depends on cli/commands (13), lazyc2/security (5), static/js (3). Used by modules: lazyown (8), cli/commands (7), modules: lazy_sentinel4 (4).

- `modules/cli_auth.py` ranks 1 by PageRank, 19 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/engagement_hooks.py` ranks 2 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- `cli/banner_config.py` ranks 3 by PageRank, 11 importers, 120 symbols: Configurable Neon Box banner for the LazyOwn interactive shell.
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Hotspot `tests/test_engagement_elo_and_methodology.py`: 43 symbols, 79 connections (score 0.03).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:cli/banner_config.py, file:tests/test_engagement_and_ping.py, file:cli/fuzzy_picker.py, file:tests/test_engagement_elo_and_methodology.py, file:cli/engagement_hooks.py, file:tests/test_banner_config.py, file:modules/cli_auth.py, file:tests/test_fuzzy_picker.py
- Rating 1.0/10 = 7 x PageRank share 0.14 + 3 x risk 0.00. Internal imports: 106.

## skills/claude_md_orchestrator (`c11`, community, rating 0.9)

19 files under skills/claude_md_orchestrator (py 18, js 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0042, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on static/js (3), modules: lazyown (2), modules: autonomous_daemon (1). Used by lazyc2/security (2), cli/commands (1), modules: lazy_sentinel4 (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `modules/colors.py` ranks 3 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- Hotspot `static/js/xterm.js`: 62 symbols, 3833 connections (score 0.30).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Key entities: file:skills/claude_md_orchestrator/models.py, file:static/js/xterm.js, file:contrib/legacy/lazygptcli_unified.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/parser.py, file:contrib/legacy/lazygptcli.py
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 41.

## modules: lazy_loop (`c9`, community, rating 0.9)

25 files under modules (py 25), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0021, imported by 12 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on modules: autonomous_daemon (11), cli/commands (9), modules: lazy_sentinel4 (5). Used by lazyc2/security (6), cli/commands (4), modules: autonomous_daemon (3).

- `modules/lazy_loop.py` ranks 1 by PageRank, 12 importers, 263 symbols: Lazy autonomous loop for LazyOwn.
- `modules/osint_enrich.py` ranks 2 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- `modules/estorides_fusion.py` ranks 3 by PageRank, 8 importers, 8 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- Hotspot `modules/lazy_loop.py`: 263 symbols, 55 connections (score 0.16).
- Hotspot `cli/commands/lazyops.py`: 49 symbols, 81 connections (score 0.03).
- Key entities: file:modules/lazy_loop.py, sym:modules/lazy_loop.py::get@233, file:cli/surface_graph.py, file:cli/commands/mcp_bridge.py, file:cli/commands/lazyops.py, file:modules/intel_fusion.py, file:cli/surface_tui.py, sym:modules/lazy_loop.py::list@237
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 94.

## cli: exploration (`c12`, community, rating 0.4)

9 files under cli (py 9), mostly testing. Core file cli/exploration.py (PageRank 0.0029, imported by 13 files): Exploration engine: trigger and OS aware addon/tool matching. Key abstractions: ExplorationConfig, DiscoveredService, AddonEntry, ToolEntry, CoverageReport, NmapXmlReader. Depends on modules: lazy_sentinel4 (2), cli: status_bar (1), modules: dashboard_tui (1). Used by cli/commands (5), modules: lazyown (4), modules: autonomous_daemon (2).

- `cli/exploration.py` ranks 1 by PageRank, 13 importers, 48 symbols: Exploration engine: trigger and OS aware addon/tool matching.
- `cli/recon_plan.py` ranks 2 by PageRank, 4 importers, 18 symbols: Reconnaissance plan generator built on top of :mod:`cli.exploration`.
- `cli/command_chain.py` ranks 3 by PageRank, 6 importers, 25 symbols: Command chain registry: explicit prerequisites and dynamic next steps.
- Hotspot `cli/exploration.py`: 48 symbols, 22 connections (score 0.03).
- Hotspot `tests/test_exploration_and_addons.py`: 36 symbols, 15 connections (score 0.02).
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _emit_event).
- Key entities: file:cli/exploration.py, file:tests/test_exploration_and_addons.py, file:tests/test_recon_plan.py, file:cli/recon_plan.py, file:cli/command_chain.py, file:tests/test_command_chain.py, file:cli/lazynmap_post.py, file:tests/test_lazynmap_post.py
- Rating 0.4/10 = 7 x PageRank share 0.05 + 3 x risk 0.00. Internal imports: 14.

## modules: kerberos_core (`c13`, community, rating 0.2)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0014, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c14`, community, rating 0.2)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0006, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 6.

## contrib/legacy (`c17`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0040, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::caesar_cipher@13
- Rating 0.2/10 = 7 x PageRank share 0.04 + 3 x risk 0.00. Internal imports: 4.

## modules: network_opsec (`c15`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/log_tamper.py (PageRank 0.0006, imported by 3 files): Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. Key abstractions: LogTamperConfig, LogTamper, windows_clear_commands, linux_clear_commands, macos_clear_commands, generate_all. Depends on cli/commands (1), modules: lazyown (1).

- `modules/log_tamper.py` ranks 1 by PageRank, 3 importers, 9 symbols: Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.
- `modules/forensic_cleaner.py` ranks 2 by PageRank, 1 importers, 8 symbols: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- `modules/memory_cleaner.py` ranks 3 by PageRank, 1 importers, 7 symbols: Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear.
- Hotspot `modules/network_opsec.py`: 12 symbols, 8 connections (score 0.01).
- Hotspot `modules/timestomper.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/timestomper.py, file:modules/network_opsec.py, file:cli/commands/opsec_cleanup.py, file:modules/forensic_cleaner.py, file:modules/log_tamper.py, file:modules/memory_cleaner.py, sym:cli/commands/opsec_cleanup.py::do_network_opsec@342, sym:cli/commands/opsec_cleanup.py::do_forensic_clean@162
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 7.

## modules: polymorphic_engine (`c16`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0006, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 8.

## scripts: journal (`c18`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0013, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c19`, community, rating 0.1)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0009, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c20`, community, rating 0.1)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0009, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261, sym:poc_tui/plugin_loader.py::_replace_placeholders@41
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c21`, community, rating 0.1)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0009, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c22`, community, rating 0.1)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0009, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## test (`c23`, community, rating 0.1)

2 files under test (py 2), mostly infrastructure. Core file test/config.py (PageRank 0.0009, imported by 1 files): o config.py Key abstractions: encrypt_data, decrypt_data, send_command_via_web, get_encrypted_command, post_result, test_migrate.

- `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Hotspot `test/test_commands.py`: 15 symbols, 7 connections (score 0.01).
- Hotspot `test/config.py`: 2 symbols, 5 connections (score 0.00).
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59, sym:test/test_commands.py::send_command_via_web@36, file:test/config.py, sym:test/test_commands.py::test_download@138, sym:test/test_commands.py::test_discover@110, sym:test/test_commands.py::test_migrate@79, sym:test/test_commands.py::test_persistence@176
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c24`, community, rating 0.1)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0009, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
