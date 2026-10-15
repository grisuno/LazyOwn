# GraphRAG Community Reports

Entities: 20673 | Relationships: 64626 | Communities: 25 | Themes: 10 | Text units: 20561

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1019 files in 25 communities and 10 themes. Highest-impact communities: modules: lazyc2 (7.0), cli/commands: utils (6.2), modules: autonomous_daemon (3.8). God nodes: core/logging.py, utils.py, skills/lazyown_mcp.py, cli/commands/_base.py, modules/lazy_loop.py.

- [modules: lazyc2] rating 7.0: `core/logging.py` ranks 1 by PageRank, 163 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands: utils] rating 6.2: `utils.py` ranks 1 by PageRank, 115 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: autonomous_daemon] rating 3.8: `modules/world_model.py` ranks 1 by PageRank, 77 importers, 61 symbols: modules/world_model.py
- [unassigned files] rating 3.7: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [cli: status_bar] rating 3.7: `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: lazy_loop] rating 3.0: `core/config.py` ranks 1 by PageRank, 84 importers, 17 symbols: Configuration loader and Config wrapper.
- [lazygui/panels] rating 1.8: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [cli/commands: c2_profile_engine] rating 1.6: `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- Key entities: file:lazyc2.py, file:lazyown.py, file:utils.py, file:tests/test_security_hardening_v4.py, file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9
- Root rating = highest community rating.

## modules: lazyc2 + modules: autonomous_daemon +9 (`t0`, theme, rating 7.0)

Theme of 11 communities and 613 files: modules: lazyc2 (123 files, rating 7.0); modules: autonomous_daemon (113 files, rating 3.8); cli: status_bar (97 files, rating 3.7); modules: lazy_loop (70 files, rating 3.0); lazygui/panels (54 files, rating 1.8); cli/commands: c2_profile_engine (26 files, rating 1.6); modules: estorides_importer (50 files, rating 1.5); static/js (29 files, rating 1.2); cli: banner_config (29 files, rating 1.2); modules: surface_graph (15 files, rating 0.5); skills/hermes-lazyown (7 files, rating 0.2).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 163 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `modules/llm_factory.py` ranks 2 by PageRank, 49 importers, 28 symbols: LLM backend factory and selection utilities.
- [modules: autonomous_daemon] `modules/world_model.py` ranks 1 by PageRank, 77 importers, 61 symbols: modules/world_model.py
- [modules: autonomous_daemon] `modules/killchain.py` ranks 2 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- [cli: status_bar] `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli: status_bar] `cli/themes.py` ranks 2 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [modules: lazy_loop] `core/config.py` ranks 1 by PageRank, 84 importers, 17 symbols: Configuration loader and Config wrapper.
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 2 by PageRank, 187 importers, 456 symbols: Lazy autonomous loop for LazyOwn.
- Key entities: file:lazyc2.py, file:lazyown.py, file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: c1, c2, c3, c4, c5, c9, c6, c7, c8, c11, c14
- Theme rating = highest child community rating.

## cli/commands: utils + skills/claude_md_orchestrator +4 (`t2`, theme, rating 6.2)

Theme of 6 communities and 169 files: cli/commands: utils (127 files, rating 6.2); skills/claude_md_orchestrator (17 files, rating 0.6); modules: kerberos_core (7 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands: utils] `utils.py` ranks 1 by PageRank, 115 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands: utils] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [skills/claude_md_orchestrator] `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- [skills/claude_md_orchestrator] `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:utils.py, file:tests/test_security_hardening_v4.py, sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py
- Children: c0, c10, c12, c16, c13, c15
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.7)

Theme of 1 communities and 222 files: unassigned files (222 files, rating 3.7).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c24
- Theme rating = highest child community rating.

## scripts: journal (`t3`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c17
- Theme rating = highest child community rating.

## modules/backdoor (`t4`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c18
- Theme rating = highest child community rating.

## poc_tui (`t5`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c19
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c20
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c21
- Theme rating = highest child community rating.

## test (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: test (2 files, rating 0.0).

- [test] `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- [test] `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59
- Children: c22
- Theme rating = highest child community rating.

## tools (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c23
- Theme rating = highest child community rating.

## modules: lazyc2 (`c1`, community, rating 7.0)

123 files under modules (py 122, js 1), mostly utility. Core file core/logging.py (PageRank 0.0711, imported by 163 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on cli/commands: utils (43), cli: status_bar (39), modules: autonomous_daemon (28). Used by modules: autonomous_daemon (88), modules: lazy_loop (22), modules: estorides_importer (17).

- `core/logging.py` ranks 1 by PageRank, 163 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/llm_factory.py` ranks 2 by PageRank, 49 importers, 28 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 3 by PageRank, 8 importers, 39 symbols: Concrete language model backends for LazyOwn.
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `lazyc2.py`: 286 symbols, 269 connections (score 0.18).
- Dependency cycle: autonomous_daemon.py -> lazyown_mcp.py -> pipeline_engine.py -> autonomous_daemon.py.
- 14 layer violations, e.g. test_collab_and_onboarding.py (testing) -> collab_bp.py (presentation).
- Taint: 7 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:lazyown.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/pipeline_engine.py, file:skills/lazyown_facts.py, file:tests/test_aci_planner.py, file:tests/test_pipeline_engine.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 450.

## cli/commands: utils (`c0`, community, rating 6.2)

127 files under cli/commands (py 126, c 1), mostly utility. Core file utils.py (PageRank 0.0267, imported by 115 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, needs_sudo, sudo_available. Depends on modules: autonomous_daemon (40), cli: status_bar (29), modules: lazy_loop (23). Used by modules: lazyc2 (43), modules: lazy_loop (32), modules: autonomous_daemon (31).

- `utils.py` ranks 1 by PageRank, 115 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 94 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 124 symbols, 204 connections (score 0.08).
- Hotspot `tests/test_security_hardening_v3.py`: 64 symbols, 107 connections (score 0.04).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Key entities: file:utils.py, file:tests/test_security_hardening_v4.py, file:tests/test_categories.py, file:tests/test_security_hardening_v3.py, file:cli/cli_enhancements.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_cli_command_sets.py, file:cli/commands/_base.py
- Rating 6.2/10 = 7 x PageRank share 0.88 + 3 x risk 0.00. Internal imports: 425.

## modules: autonomous_daemon (`c2`, community, rating 3.8)

113 files under modules (py 113), mostly utility. Core file modules/world_model.py (PageRank 0.0096, imported by 77 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: lazyc2 (88), modules: lazy_loop (35), cli/commands: utils (31). Used by cli/commands: utils (40), modules: lazy_loop (34), modules: lazyc2 (28).

- `modules/world_model.py` ranks 1 by PageRank, 77 importers, 61 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `skills/autonomous_daemon.py` ranks 3 by PageRank, 111 importers, 148 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- Hotspot `skills/lazyown_mcp.py`: 142 symbols, 457 connections (score 0.11).
- Hotspot `skills/autonomous_daemon.py`: 148 symbols, 256 connections (score 0.10).
- Dependency cycle: lazyown_mcp.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in health_check).
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:skills/tests/test_hive_mind.py, file:tests/test_engage_orchestrator.py
- Rating 3.8/10 = 7 x PageRank share 0.54 + 3 x risk 0.00. Internal imports: 686.

## unassigned files (`c24`, community, rating 3.7)

222 files under modules (py 116, sh 61, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0004, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c, file:modules/rootkit/mrhyde2.c
- Rating 3.7/10 = 7 x PageRank share 0.52 + 3 x risk 0.00. Internal imports: 0.

## cli: status_bar (`c3`, community, rating 3.7)

97 files under cli (py 97), mostly utility. Core file core/console.py (PageRank 0.0207, imported by 62 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: autonomous_daemon (23), cli/commands: utils (15), modules: lazyc2 (11). Used by modules: lazyc2 (39), modules: autonomous_daemon (31), cli/commands: utils (29).

- `core/console.py` ranks 1 by PageRank, 62 importers, 11 symbols: ANSI color constants and console output helpers.
- `cli/themes.py` ranks 2 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `cli/commands/containers.py` ranks 3 by PageRank, 11 importers, 7 symbols: Container and Kubernetes attack command set.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.09).
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Dataflow: 2 INFERRED issues (first: UNCHECKED_ALLOC in _run_single_search).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, file:tests/test_improvements_spec.py, sym:core/console.py::print_warn@149, file:tests/test_tips_engine.py, file:cli/tips_engine.py, file:cli/status_bar.py
- Rating 3.7/10 = 7 x PageRank share 0.53 + 3 x risk 0.00. Internal imports: 320.

## modules: lazy_loop (`c4`, community, rating 3.0)

70 files under tests (py 70), mostly utility. Core file core/config.py (PageRank 0.0177, imported by 84 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on modules: autonomous_daemon (34), cli/commands: utils (32), modules: lazyc2 (22). Used by modules: autonomous_daemon (35), cli/commands: utils (23), modules: lazyc2 (20).

- `core/config.py` ranks 1 by PageRank, 84 importers, 17 symbols: Configuration loader and Config wrapper.
- `modules/lazy_loop.py` ranks 2 by PageRank, 187 importers, 456 symbols: Lazy autonomous loop for LazyOwn.
- `modules/__init__.py` ranks 3 by PageRank, 57 importers, 0 symbols.
- Hotspot `modules/lazy_loop.py`: 456 symbols, 386 connections (score 0.28).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: lazy_loop.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> lazy_loop.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@911, file:modules/lazy_proxy.py, sym:modules/lazy_loop.py::ExplorationGraph@1019, sym:modules/lazy_loop.py::ActivityLog@1327, file:cli/commands/lazyops.py
- Rating 3.0/10 = 7 x PageRank share 0.43 + 3 x risk 0.00. Internal imports: 579.

## lazygui/panels (`c5`, community, rating 1.8)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0079, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (6), cli/commands: c2_profile_engine (2), modules: autonomous_daemon (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 181.

## cli/commands: c2_profile_engine (`c9`, community, rating 1.6)

26 files under tests (py 26), mostly utility. Core file cli/commands/enum.py (PageRank 0.0263, imported by 23 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on cli/commands: utils (12), modules: lazyc2 (5), modules: lazy_loop (3). Used by modules: autonomous_daemon (15), modules: lazyc2 (6), cli: status_bar (3).

- `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- `modules/c2_profile_engine.py` ranks 2 by PageRank, 6 importers, 47 symbols: Extended malleable C2 profile engine with TLS, DNS, SMB, and WebSocket transports.
- `lazyc2/security/command_allowlist.py` ranks 3 by PageRank, 3 importers, 8 symbols: Command allowlist policy for the LazyOwn C2 ``/api/run`` endpoint.
- Hotspot `tests/test_c2_profile_engine.py`: 63 symbols, 4 connections (score 0.03).
- Hotspot `tests/test_socks_proxy.py`: 52 symbols, 3 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_c2_profile_engine.py, file:modules/c2_profile_engine.py, file:tests/test_bof_registry.py, file:tests/test_socks_proxy.py, file:tests/test_scope_guard.py, file:modules/bof_registry.py, file:tests/test_sleep_obfuscation.py, file:modules/socks_proxy.py
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 52.

## modules: estorides_importer (`c6`, community, rating 1.5)

50 files under tests (py 49, c 1), mostly utility. Core file core/crypto.py (PageRank 0.0053, imported by 17 files): Symmetric primitives used by the framework. Key abstractions: generate_salt, derive_key, xor_encrypt_decrypt, generate_xor_key, AESencrypt, AESdecrypt. Depends on modules: lazyc2 (17), modules: lazy_loop (16), cli/commands: utils (14). Used by cli/commands: utils (11), modules: lazyc2 (11), modules: autonomous_daemon (11).

- `core/crypto.py` ranks 1 by PageRank, 17 importers, 7 symbols: Symmetric primitives used by the framework.
- `modules/db.py` ranks 2 by PageRank, 24 importers, 37 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- `core/credential_vault.py` ranks 3 by PageRank, 6 importers, 8 symbols: Credential vault — AES-256-GCM encryption for sensitive config values.
- Hotspot `tests/test_addon_creator.py`: 86 symbols, 11 connections (score 0.05).
- Hotspot `tests/test_api_authz.py`: 48 symbols, 52 connections (score 0.03).
- 27 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _import_to_scope).
- Surprising bridge: __init__.py <-> state.py (8 hops across communities).
- Key entities: file:tests/test_addon_creator.py, file:modules/rootkit/rootkit.c, file:tests/test_core.py, file:modules/estorides_importer.py, file:modules/db.py, file:lazyc2/addon_creator.py, file:modules/opsec_scorer.py, file:tests/test_api_authz.py
- Rating 1.5/10 = 7 x PageRank share 0.21 + 3 x risk 0.00. Internal imports: 98.

## static/js (`c7`, community, rating 1.2)

29 files under static/js (js 14, py 13, c 1, sh 1), mostly utility. Core file core/payload_schema.py (PageRank 0.0110, imported by 13 files): Declarative schema and validation for ``payload.json``. Key abstractions: FieldKind, Severity, FieldSpec, ValidationIssue, field_for, coerce_value. Depends on modules: lazy_loop (19), cli/commands: utils (4), cli: status_bar (4). Used by cli/commands: utils (11), cli: status_bar (6), modules: autonomous_daemon (4).

- `core/payload_schema.py` ranks 1 by PageRank, 13 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- `core/process.py` ranks 2 by PageRank, 20 importers, 12 symbols: Process and subprocess utilities for the LazyOwn framework.
- `cli/assign.py` ranks 3 by PageRank, 124 importers, 1 symbols: ``assign`` business logic.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 9 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:tests/test_payload_schema.py
- Rating 1.2/10 = 7 x PageRank share 0.17 + 3 x risk 0.00. Internal imports: 251.

## cli: banner_config (`c8`, community, rating 1.2)

29 files under tests (py 27, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0060, imported by 20 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on cli/commands: utils (16), modules: lazyc2 (3), cli: status_bar (3). Used by modules: lazyc2 (14), cli: status_bar (8), cli/commands: utils (7).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- `modules/cli_auth.py` ranks 2 by PageRank, 19 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/engagement_hooks.py` ranks 3 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- Taint: 4 paths reach this group via subprocess.
- Key entities: file:cli/banner_config.py, file:modules/lazy_rbac.py, file:tests/test_engagement_and_ping.py, file:cli/fuzzy_picker.py, file:tests/test_banner_config.py, file:cli/engagement_hooks.py, file:tests/test_engagement_elo_and_methodology.py, file:tests/test_fuzzy_picker.py
- Rating 1.2/10 = 7 x PageRank share 0.18 + 3 x risk 0.00. Internal imports: 155.

## skills/claude_md_orchestrator (`c10`, community, rating 0.6)

17 files under skills/claude_md_orchestrator (py 17), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0034, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on cli/commands: utils (2), modules: lazyc2 (1), modules: lazy_loop (1). Used by modules: lazyc2 (3), cli/commands: utils (2), modules: lazy_loop (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:modules/lazyown_bprfuzzer.py
- Rating 0.6/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 37.

## modules: surface_graph (`c11`, community, rating 0.5)

15 files under modules (py 15), mostly utility. Core file modules/osint_enrich.py (PageRank 0.0020, imported by 3 files): Keyless OSINT enrichment for finding evidence. Key abstractions: cve_lookup, reverse_dns, host_geo, domain_exposure, enrich_evidence, estorides_checkout. Depends on cli/commands: utils (4), cli: status_bar (2), modules: lazyc2 (1). Used by modules: lazyc2 (6), cli/commands: utils (4), modules: lazy_loop (4).

- `modules/osint_enrich.py` ranks 1 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- `modules/estorides_fusion.py` ranks 2 by PageRank, 8 importers, 11 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- `modules/finding_lifecycle.py` ranks 3 by PageRank, 11 importers, 26 symbols: Finding confirmation lifecycle: pending -> confirmed / rejected.
- Hotspot `cli/surface_graph.py`: 33 symbols, 15 connections (score 0.02).
- Hotspot `modules/finding_lifecycle.py`: 26 symbols, 18 connections (score 0.02).
- Key entities: file:cli/surface_graph.py, file:modules/finding_lifecycle.py, file:modules/intel_fusion.py, file:cli/surface_tui.py, file:cli/commands/database.py, file:modules/attack_surface3d.py, file:modules/estorides_fusion.py, file:modules/osint_enrich.py
- Rating 0.5/10 = 7 x PageRank share 0.07 + 3 x risk 0.00. Internal imports: 29.

## modules: kerberos_core (`c12`, community, rating 0.2)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0013, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands: utils (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## skills/hermes-lazyown (`c14`, community, rating 0.2)

7 files under skills/hermes-lazyown (py 7), mostly utility. Core file skills/hermes-lazyown/constants.py (PageRank 0.0026, imported by 6 files): Central constants for the Hermes-LazyOwn integration layer. Key abstractions: ConfigKeys, EnvKeys, Defaults, PhaseNames, Paths, lazyown_dir. Depends on cli/commands: utils (1), modules: autonomous_daemon (1).

- `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- `skills/hermes-lazyown/config_bridge.py` ranks 3 by PageRank, 1 importers, 16 symbols: Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source.
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/output_compactor.py`: 20 symbols, 5 connections (score 0.01).
- Key entities: file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/hermes-lazyown/constants.py, file:skills/hermes-lazyown/executor.py, file:skills/hermes-lazyown/config_bridge.py, file:skills/hermes-lazyown/hermes_sync.py, file:skills/hermes-lazyown/claudemd_rules.py, sym:skills/hermes-lazyown/mcp_server.py::_handle_tool@346
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 11.

## contrib/legacy (`c16`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0037, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands: utils (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::caesar_cipher@13
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 4.

## modules: saas_attacks (`c13`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0005, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands: utils (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/k8s_attacks.py, file:modules/gcp_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c15`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0005, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands: utils (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 8.

## scripts: journal (`c17`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0012, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c18`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0008, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c19`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0008, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c20`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0008, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c21`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0008, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## test (`c22`, community, rating 0.0)

2 files under test (py 2), mostly infrastructure. Core file test/config.py (PageRank 0.0008, imported by 1 files): o config.py Key abstractions: encrypt_data, decrypt_data, send_command_via_web, get_encrypted_command, post_result, test_migrate.

- `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Hotspot `test/test_commands.py`: 15 symbols, 7 connections (score 0.01).
- Hotspot `test/config.py`: 2 symbols, 5 connections (score 0.00).
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59, sym:test/test_commands.py::send_command_via_web@36, file:test/config.py, sym:test/test_commands.py::test_download@138, sym:test/test_commands.py::test_discover@110, sym:test/test_commands.py::test_migrate@79, sym:test/test_commands.py::test_persistence@176
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c23`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0008, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
