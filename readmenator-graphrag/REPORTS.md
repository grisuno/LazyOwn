# GraphRAG Community Reports

Entities: 20390 | Relationships: 63242 | Communities: 24 | Themes: 10 | Text units: 20278

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1000 files in 24 communities and 10 themes. Highest-impact communities: modules: lazyc2 (7.0), cli/commands (6.2), modules: autonomous_daemon (4.9). God nodes: core/logging.py, utils.py, cli/commands/_base.py, skills/lazyown_mcp.py, modules/lazy_loop.py.

- [modules: lazyc2] rating 7.0: `core/logging.py` ranks 1 by PageRank, 157 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 6.2: `utils.py` ranks 1 by PageRank, 114 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: autonomous_daemon] rating 4.9: `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [cli: status_bar] rating 3.9: `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: lazy_loop] rating 3.9: `core/config.py` ranks 1 by PageRank, 74 importers, 17 symbols: Configuration loader and Config wrapper.
- [unassigned files] rating 3.6: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [lazygui/panels] rating 1.8: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [cli: banner_config] rating 1.5: `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- Key entities: file:lazyc2.py, file:lazyown.py, file:utils.py, file:tests/test_categories.py, file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9
- Root rating = highest community rating.

## modules: lazyc2 + modules: autonomous_daemon +8 (`t0`, theme, rating 7.0)

Theme of 10 communities and 600 files: modules: lazyc2 (146 files, rating 7.0); modules: autonomous_daemon (116 files, rating 4.9); cli: status_bar (101 files, rating 3.9); modules: lazy_loop (79 files, rating 3.9); lazygui/panels (54 files, rating 1.8); cli: banner_config (40 files, rating 1.5); static/js (26 files, rating 0.8); skills/claude_md_orchestrator (17 files, rating 0.6); modules: surface_graph (15 files, rating 0.5); modules: network_opsec (6 files, rating 0.1).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 157 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `core/safe_exec.py` ranks 2 by PageRank, 47 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [modules: autonomous_daemon] `modules/world_model.py` ranks 2 by PageRank, 76 importers, 61 symbols: modules/world_model.py
- [cli: status_bar] `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli: status_bar] `cli/themes.py` ranks 2 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [modules: lazy_loop] `core/config.py` ranks 1 by PageRank, 74 importers, 17 symbols: Configuration loader and Config wrapper.
- [modules: lazy_loop] `modules/llm_factory.py` ranks 2 by PageRank, 49 importers, 25 symbols: LLM backend factory and selection utilities.
- Key entities: file:lazyc2.py, file:lazyown.py, file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: c0, c2, c3, c4, c5, c6, c7, c8, c9, c13
- Theme rating = highest child community rating.

## cli/commands + modules: kerberos_core +4 (`t2`, theme, rating 6.2)

Theme of 6 communities and 169 files: cli/commands (137 files, rating 6.2); modules: kerberos_core (7 files, rating 0.2); skills/hermes-lazyown (7 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 114 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [skills/hermes-lazyown] `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- [skills/hermes-lazyown] `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:utils.py, file:tests/test_categories.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py
- Children: c1, c10, c12, c15, c11, c14
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.6)

Theme of 1 communities and 216 files: unassigned files (216 files, rating 3.6).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c23
- Theme rating = highest child community rating.

## scripts: journal (`t3`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c16
- Theme rating = highest child community rating.

## modules/backdoor (`t4`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c17
- Theme rating = highest child community rating.

## poc_tui (`t5`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c18
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c19
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c20
- Theme rating = highest child community rating.

## test (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: test (2 files, rating 0.0).

- [test] `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- [test] `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59
- Children: c21
- Theme rating = highest child community rating.

## tools (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c22
- Theme rating = highest child community rating.

## modules: lazyc2 (`c0`, community, rating 7.0)

146 files under modules (py 145, js 1), mostly utility. Core file core/logging.py (PageRank 0.0722, imported by 157 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on cli: status_bar (45), modules: lazy_loop (43), cli/commands (39). Used by modules: autonomous_daemon (95), modules: lazy_loop (25), cli/commands (24).

- `core/logging.py` ranks 1 by PageRank, 157 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `core/safe_exec.py` ranks 2 by PageRank, 47 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/logging_config.py` ranks 3 by PageRank, 35 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `lazyc2.py`: 284 symbols, 252 connections (score 0.17).
- Dependency cycle: autonomous_daemon.py -> lazyown_mcp.py -> pipeline_engine.py -> autonomous_daemon.py.
- 39 layer violations, e.g. test_api_authz.py (testing) -> api_authz.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:lazyown.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/pipeline_engine.py, file:skills/lazyown_facts.py, file:tests/test_security_hardening_v4.py, file:tests/test_aci_planner.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 513.

## cli/commands (`c1`, community, rating 6.2)

137 files under cli/commands (py 136, c 1), mostly utility. Core file utils.py (PageRank 0.0271, imported by 114 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, needs_sudo, sudo_available. Depends on modules: autonomous_daemon (45), cli: status_bar (34), modules: lazyc2 (24). Used by modules: lazyc2 (39), modules: autonomous_daemon (26), modules: lazy_loop (22).

- `utils.py` ranks 1 by PageRank, 114 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 94 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 124 symbols, 203 connections (score 0.08).
- Hotspot `tests/test_security_hardening_v3.py`: 64 symbols, 107 connections (score 0.04).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:utils.py, file:tests/test_categories.py, file:cli/cli_enhancements.py, file:tests/test_security_hardening_v3.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_cli_command_sets.py, file:cli/commands/_base.py, file:cli/commands/misc_migrated.py
- Rating 6.2/10 = 7 x PageRank share 0.88 + 3 x risk 0.00. Internal imports: 411.

## modules: autonomous_daemon (`c2`, community, rating 4.9)

116 files under modules (py 116), mostly utility. Core file cli/commands/enum.py (PageRank 0.0267, imported by 23 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyc2 (95), modules: lazy_loop (42), cli: status_bar (31). Used by cli/commands (45), modules: lazy_loop (40), modules: lazyc2 (34).

- `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- `modules/world_model.py` ranks 2 by PageRank, 76 importers, 61 symbols: modules/world_model.py
- `modules/killchain.py` ranks 3 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- Hotspot `skills/lazyown_mcp.py`: 138 symbols, 447 connections (score 0.11).
- Hotspot `skills/autonomous_daemon.py`: 148 symbols, 256 connections (score 0.10).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:skills/tests/test_hive_mind.py, file:tests/test_engage_orchestrator.py
- Rating 4.9/10 = 7 x PageRank share 0.70 + 3 x risk 0.00. Internal imports: 694.

## cli: status_bar (`c3`, community, rating 3.9)

101 files under cli (py 100, c 1), mostly utility. Core file core/console.py (PageRank 0.0212, imported by 62 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: autonomous_daemon (26), cli/commands (21), modules: lazy_loop (17). Used by modules: lazyc2 (45), cli/commands (34), modules: autonomous_daemon (31).

- `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- `cli/themes.py` ranks 2 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `core/crypto.py` ranks 3 by PageRank, 15 importers, 7 symbols: Symmetric primitives used by the framework.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.09).
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Dataflow: 2 INFERRED issues (first: UNCHECKED_ALLOC in _run_single_search).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, file:tests/test_improvements_spec.py, sym:core/console.py::print_warn@149, file:tests/test_tips_engine.py, file:cli/status_bar.py, file:cli/tips_engine.py
- Rating 3.9/10 = 7 x PageRank share 0.56 + 3 x risk 0.00. Internal imports: 335.

## modules: lazy_loop (`c4`, community, rating 3.9)

79 files under tests (py 79), mostly utility. Core file core/config.py (PageRank 0.0132, imported by 74 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on modules: autonomous_daemon (40), modules: lazyc2 (25), cli/commands (22). Used by modules: lazyc2 (43), modules: autonomous_daemon (42), cli/commands (17).

- `core/config.py` ranks 1 by PageRank, 74 importers, 17 symbols: Configuration loader and Config wrapper.
- `modules/llm_factory.py` ranks 2 by PageRank, 49 importers, 25 symbols: LLM backend factory and selection utilities.
- `modules/lazy_loop.py` ranks 3 by PageRank, 165 importers, 440 symbols: Lazy autonomous loop for LazyOwn.
- Hotspot `modules/lazy_loop.py`: 440 symbols, 321 connections (score 0.26).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: llm_factory.py -> ai_model.py -> llm_factory.py.
- Taint: 3 paths reach this group via subprocess.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@727, sym:modules/lazy_loop.py::ExplorationGraph@835, file:tests/test_payload_schema.py, sym:modules/lazy_loop.py::ActivityLog@1138, file:modules/lazy_proxy.py
- Rating 3.9/10 = 7 x PageRank share 0.56 + 3 x risk 0.00. Internal imports: 590.

## unassigned files (`c23`, community, rating 3.6)

216 files under modules (py 115, sh 56, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0005, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c, file:modules/rootkit/mrhyde2.c
- Rating 3.6/10 = 7 x PageRank share 0.51 + 3 x risk 0.00. Internal imports: 0.

## lazygui/panels (`c5`, community, rating 1.8)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0081, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (6), modules: autonomous_daemon (3), cli: banner_config (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 181.

## cli: banner_config (`c6`, community, rating 1.5)

40 files under tests (py 38, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0063, imported by 20 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on cli/commands (15), modules: lazyc2 (4), modules: lazy_loop (4). Used by modules: lazyc2 (18), cli/commands (8), cli: status_bar (8).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- `modules/cli_auth.py` ranks 2 by PageRank, 19 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/engagement_hooks.py` ranks 3 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- 2 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:cli/banner_config.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_engagement_and_ping.py, file:cli/fuzzy_picker.py, file:lazyc2/addon_creator.py, file:tests/test_banner_config.py, file:cli/engagement_hooks.py
- Rating 1.5/10 = 7 x PageRank share 0.22 + 3 x risk 0.00. Internal imports: 168.

## static/js (`c7`, community, rating 0.8)

26 files under static/js (js 14, py 10, c 1, sh 1), mostly utility. Core file core/process.py (PageRank 0.0031, imported by 20 files): Process and subprocess utilities for the LazyOwn framework. Key abstractions: check_go_tool_installed, is_binary_present, handle_multiple_rhosts, wrapper, check_sudo, run. Depends on modules: lazy_loop (5), cli: status_bar (4), cli/commands (3). Used by cli/commands (9), modules: lazy_loop (8), cli: status_bar (5).

- `core/process.py` ranks 1 by PageRank, 20 importers, 12 symbols: Process and subprocess utilities for the LazyOwn framework.
- `cli/assign.py` ranks 2 by PageRank, 124 importers, 1 symbols: ``assign`` business logic.
- `cli/show.py` ranks 3 by PageRank, 59 importers, 1 symbols: Pretty-print the live payload for the operator.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 12 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:static/js/force-graph-1.43.5.min.js
- Rating 0.8/10 = 7 x PageRank share 0.11 + 3 x risk 0.00. Internal imports: 241.

## skills/claude_md_orchestrator (`c8`, community, rating 0.6)

17 files under skills/claude_md_orchestrator (py 17), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0040, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on modules: lazy_loop (2), cli/commands (1), modules: autonomous_daemon (1). Used by modules: lazyc2 (3), cli/commands (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Key entities: file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:skills/claude_md_orchestrator/validators.py, file:modules/lazyown_bprfuzzer.py, file:skills/claude_md_orchestrator/parser.py
- Rating 0.6/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 37.

## modules: surface_graph (`c9`, community, rating 0.5)

15 files under modules (py 15), mostly utility. Core file modules/osint_enrich.py (PageRank 0.0020, imported by 3 files): Keyless OSINT enrichment for finding evidence. Key abstractions: cve_lookup, reverse_dns, host_geo, domain_exposure, enrich_evidence, estorides_checkout. Depends on cli/commands (4), cli: status_bar (2), modules: lazy_loop (2). Used by modules: lazyc2 (6), modules: lazy_loop (5), cli/commands (4).

- `modules/osint_enrich.py` ranks 1 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- `modules/estorides_fusion.py` ranks 2 by PageRank, 8 importers, 11 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- `modules/finding_lifecycle.py` ranks 3 by PageRank, 11 importers, 26 symbols: Finding confirmation lifecycle: pending -> confirmed / rejected.
- Hotspot `cli/surface_graph.py`: 33 symbols, 15 connections (score 0.02).
- Hotspot `modules/finding_lifecycle.py`: 26 symbols, 18 connections (score 0.02).
- Key entities: file:cli/surface_graph.py, file:modules/finding_lifecycle.py, file:modules/intel_fusion.py, file:cli/surface_tui.py, file:cli/commands/database.py, file:modules/estorides_fusion.py, file:modules/attack_surface3d.py, file:modules/osint_enrich.py
- Rating 0.5/10 = 7 x PageRank share 0.07 + 3 x risk 0.00. Internal imports: 29.

## modules: kerberos_core (`c10`, community, rating 0.2)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0013, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## skills/hermes-lazyown (`c12`, community, rating 0.2)

7 files under skills/hermes-lazyown (py 7), mostly utility. Core file skills/hermes-lazyown/constants.py (PageRank 0.0027, imported by 6 files): Central constants for the Hermes-LazyOwn integration layer. Key abstractions: ConfigKeys, EnvKeys, Defaults, PhaseNames, Paths, lazyown_dir. Depends on cli/commands (1), modules: autonomous_daemon (1).

- `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- `skills/hermes-lazyown/config_bridge.py` ranks 3 by PageRank, 1 importers, 16 symbols: Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source.
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/output_compactor.py`: 20 symbols, 5 connections (score 0.01).
- Key entities: file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/hermes-lazyown/constants.py, file:skills/hermes-lazyown/executor.py, file:skills/hermes-lazyown/config_bridge.py, file:skills/hermes-lazyown/hermes_sync.py, file:skills/hermes-lazyown/claudemd_rules.py, sym:skills/hermes-lazyown/mcp_server.py::_handle_tool@346
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 11.

## contrib/legacy (`c15`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0038, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::caesar_cipher@13
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 4.

## modules: saas_attacks (`c11`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0005, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/k8s_attacks.py, file:modules/gcp_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 6.

## modules: network_opsec (`c13`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/log_tamper.py (PageRank 0.0006, imported by 3 files): Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. Key abstractions: LogTamperConfig, LogTamper, windows_clear_commands, linux_clear_commands, macos_clear_commands, generate_all. Depends on modules: lazyc2 (1), cli/commands (1).

- `modules/log_tamper.py` ranks 1 by PageRank, 3 importers, 9 symbols: Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.
- `modules/forensic_cleaner.py` ranks 2 by PageRank, 1 importers, 8 symbols: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- `modules/memory_cleaner.py` ranks 3 by PageRank, 1 importers, 7 symbols: Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear.
- Hotspot `modules/network_opsec.py`: 12 symbols, 8 connections (score 0.01).
- Hotspot `modules/timestomper.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/timestomper.py, file:modules/network_opsec.py, file:cli/commands/opsec_cleanup.py, file:modules/forensic_cleaner.py, file:modules/log_tamper.py, file:modules/memory_cleaner.py, sym:cli/commands/opsec_cleanup.py::do_network_opsec@342, sym:cli/commands/opsec_cleanup.py::do_timestomp@219
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 7.

## modules: polymorphic_engine (`c14`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0005, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 8.

## scripts: journal (`c16`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0012, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c17`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0009, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c18`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0009, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261, sym:poc_tui/plugin_loader.py::_replace_placeholders@41
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c19`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0009, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c20`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0009, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## test (`c21`, community, rating 0.0)

2 files under test (py 2), mostly infrastructure. Core file test/config.py (PageRank 0.0009, imported by 1 files): o config.py Key abstractions: encrypt_data, decrypt_data, send_command_via_web, get_encrypted_command, post_result, test_migrate.

- `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Hotspot `test/test_commands.py`: 15 symbols, 7 connections (score 0.01).
- Hotspot `test/config.py`: 2 symbols, 5 connections (score 0.00).
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59, sym:test/test_commands.py::send_command_via_web@36, file:test/config.py, sym:test/test_commands.py::test_download@138, sym:test/test_commands.py::test_discover@110, sym:test/test_commands.py::test_migrate@79, sym:test/test_commands.py::test_persistence@176
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c22`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0009, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
