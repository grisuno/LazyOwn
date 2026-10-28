# GraphRAG Community Reports

Entities: 23922 | Relationships: 76419 | Communities: 24 | Themes: 11 | Text units: 23820

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1208 files in 24 communities and 11 themes. Highest-impact communities: modules: lazyown_mcp (7.0), cli/commands (5.4), modules: lazy_loop (3.9). God nodes: core/logging.py, utils.py, modules/lazy_loop.py, skills/lazyown_mcp.py, cli/commands/_base.py.

- [modules: lazyown_mcp] rating 7.0: `core/logging.py` ranks 1 by PageRank, 195 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 5.4: `utils.py` ranks 1 by PageRank, 130 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazy_loop] rating 3.9: `modules/lazy_loop.py` ranks 1 by PageRank, 225 importers, 467 symbols: Lazy autonomous loop for LazyOwn.
- [modules: world_model] rating 3.4: `modules/world_model.py` ranks 1 by PageRank, 148 importers, 70 symbols: modules/world_model.py
- [unassigned files] rating 3.1: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [cli] rating 2.9: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: html2pdf.bundle.min] rating 2.6: `core/config.py` ranks 1 by PageRank, 106 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: llm_budget] rating 1.7: `modules/llm_factory.py` ranks 1 by PageRank, 64 importers, 30 symbols: LLM backend factory and selection utilities.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:utils.py, file:cli/banner_config.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
- Root rating = highest community rating.

## modules: lazyown_mcp + modules: lazy_loop +7 (`t0`, theme, rating 7.0)

Theme of 9 communities and 659 files: modules: lazyown_mcp (157 files, rating 7.0); modules: lazy_loop (117 files, rating 3.9); cli (93 files, rating 2.9); modules: html2pdf.bundle.min (74 files, rating 2.6); modules: llm_budget (44 files, rating 1.7); lazyc2/security (59 files, rating 1.4); lazygui/panels (54 files, rating 1.4); modules: chain_runner (38 files, rating 0.9); skills/claude_md_orchestrator (23 files, rating 0.6).

- [modules: lazyown_mcp] `core/logging.py` ranks 1 by PageRank, 195 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyown_mcp] `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 225 importers, 467 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/__init__.py` ranks 2 by PageRank, 167 importers, 0 symbols.
- [cli] `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `modules/cli_auth.py` ranks 2 by PageRank, 21 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- [modules: html2pdf.bundle.min] `core/config.py` ranks 1 by PageRank, 106 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: html2pdf.bundle.min] `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js
- Children: c0, c2, c4, c5, c8, c6, c7, c9, c10
- Theme rating = highest child community rating.

## cli/commands + contrib/legacy +3 (`t2`, theme, rating 5.4)

Theme of 5 communities and 174 files: cli/commands (149 files, rating 5.4); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 130 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c1, c15, c11, c12, c14
- Theme rating = highest child community rating.

## modules: world_model + skills/hermes-lazyown (`t3`, theme, rating 3.4)

Theme of 2 communities and 117 files: modules: world_model (110 files, rating 3.4); skills/hermes-lazyown (7 files, rating 0.2).

- [modules: world_model] `modules/world_model.py` ranks 1 by PageRank, 148 importers, 70 symbols: modules/world_model.py
- [modules: world_model] `core/safe_exec.py` ranks 2 by PageRank, 60 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- [skills/hermes-lazyown] `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- [skills/hermes-lazyown] `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- Key entities: file:modules/world_model.py, file:tests/test_security_hardening_v4.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py
- Children: c3, c13
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.1)

Theme of 1 communities and 241 files: unassigned files (241 files, rating 3.1).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c23
- Theme rating = highest child community rating.

## tests (`t4`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c16
- Theme rating = highest child community rating.

## scripts: journal (`t5`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c17
- Theme rating = highest child community rating.

## tools (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c22
- Theme rating = highest child community rating.

## modules/backdoor (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c18
- Theme rating = highest child community rating.

## poc_tui (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c19
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c20
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c21
- Theme rating = highest child community rating.

## modules: lazyown_mcp (`c0`, community, rating 7.0)

157 files under modules (py 157), mostly utility. Core file core/logging.py (PageRank 0.0777, imported by 195 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: world_model (54), modules: lazy_loop (44), cli/commands (26). Used by modules: world_model (44), lazyc2/security (35), modules: llm_budget (28).

- `core/logging.py` ranks 1 by PageRank, 195 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- `modules/logging_config.py` ranks 3 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `skills/lazyown_mcp.py`: 155 symbols, 512 connections (score 0.12).
- Hotspot `skills/autonomous_daemon.py`: 150 symbols, 267 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> reactive_engine.py -> config.py.
- 28 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 890.

## cli/commands (`c1`, community, rating 5.4)

149 files under cli/commands (py 148, c 1), mostly utility. Core file utils.py (PageRank 0.0231, imported by 130 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on modules: world_model (49), cli (36), modules: html2pdf.bundle.min (31). Used by modules: lazy_loop (39), modules: html2pdf.bundle.min (35), cli (30).

- `utils.py` ranks 1 by PageRank, 130 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 101 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 126 symbols, 221 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:utils.py, file:cli/banner_config.py, file:tests/test_categories.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_cli_command_sets.py, file:cli/cli_enhancements.py, file:tests/test_security_hardening_v3.py, file:cli/commands/_base.py
- Rating 5.4/10 = 7 x PageRank share 0.78 + 3 x risk 0.00. Internal imports: 453.

## modules: lazy_loop (`c2`, community, rating 3.9)

117 files under tests (py 117), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0122, imported by 225 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on modules: world_model (50), modules: llm_budget (49), cli/commands (39). Used by modules: world_model (47), modules: lazyown_mcp (44), modules: html2pdf.bundle.min (30).

- `modules/lazy_loop.py` ranks 1 by PageRank, 225 importers, 467 symbols: Lazy autonomous loop for LazyOwn.
- `modules/__init__.py` ranks 2 by PageRank, 167 importers, 0 symbols.
- `modules/auto_registry.py` ranks 3 by PageRank, 52 importers, 43 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- Hotspot `modules/lazy_loop.py`: 467 symbols, 493 connections (score 0.29).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> reactive_engine.py -> config.py.
- 2 layer violations, e.g. test_orchestrator_api.py (testing) -> api_authz.py (presentation).
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1017, file:tests/test_llm_orchestrator.py, file:modules/lazy_proxy.py, sym:modules/lazy_loop.py::ExplorationGraph@1125, file:tests/test_guardrails.py
- Rating 3.9/10 = 7 x PageRank share 0.56 + 3 x risk 0.00. Internal imports: 808.

## modules: world_model (`c3`, community, rating 3.4)

110 files under tests (py 110), mostly utility. Core file modules/world_model.py (PageRank 0.0162, imported by 148 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: lazy_loop (47), modules: lazyown_mcp (44), cli/commands (27). Used by modules: lazyown_mcp (54), modules: lazy_loop (50), cli/commands (49).

- `modules/world_model.py` ranks 1 by PageRank, 148 importers, 70 symbols: modules/world_model.py
- `core/safe_exec.py` ranks 2 by PageRank, 60 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/killchain.py` ranks 3 by PageRank, 33 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- Hotspot `modules/world_model.py`: 70 symbols, 177 connections (score 0.05).
- Hotspot `tests/test_security_hardening_v4.py`: 67 symbols, 66 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 2 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:modules/world_model.py, file:tests/test_security_hardening_v4.py, file:cli/dashboard_tui.py, file:cli/ops_commands.py, file:cli/exploration.py, file:tests/test_phase1_data_gaps.py, file:cli/graph_advisor.py, file:modules/atomic_exploit_bridge.py
- Rating 3.4/10 = 7 x PageRank share 0.49 + 3 x risk 0.00. Internal imports: 362.

## unassigned files (`c23`, community, rating 3.1)

241 files under modules (py 133, sh 63, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0004, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.1/10 = 7 x PageRank share 0.44 + 3 x risk 0.00. Internal imports: 0.

## cli (`c4`, community, rating 2.9)

93 files under tests (py 93), mostly utility. Core file core/console.py (PageRank 0.0166, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on cli/commands (30), modules: world_model (25), modules: lazyown_mcp (23). Used by cli/commands (36), modules: lazyown_mcp (21), modules: world_model (14).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/cli_auth.py` ranks 2 by PageRank, 21 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/themes.py` ranks 3 by PageRank, 18 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.09).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> cli_auth.py -> engagement_hooks.py -> config.py.
- Taint: 3 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _load_or_create_salt).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:lazyown.py, file:tests/test_tips_engine.py, file:cli/status_bar.py
- Rating 2.9/10 = 7 x PageRank share 0.41 + 3 x risk 0.00. Internal imports: 425.

## modules: html2pdf.bundle.min (`c5`, community, rating 2.6)

74 files under tests (py 57, js 14, c 2, sh 1), mostly utility. Core file core/config.py (PageRank 0.0174, imported by 106 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (35), modules: lazy_loop (30), modules: lazyown_mcp (27). Used by modules: lazy_loop (33), cli/commands (31), cli (19).

- `core/config.py` ranks 1 by PageRank, 106 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- `core/param_registry.py` ranks 3 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> reactive_engine.py -> config.py.
- 1 layer violations, e.g. test_core_defaults.py (testing) -> api.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:core/config.py
- Rating 2.6/10 = 7 x PageRank share 0.38 + 3 x risk 0.00. Internal imports: 378.

## modules: llm_budget (`c8`, community, rating 1.7)

44 files under modules (py 44), mostly utility. Core file modules/llm_factory.py (PageRank 0.0115, imported by 64 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazyown_mcp (28), modules: lazy_loop (26), cli/commands (7). Used by modules: lazy_loop (49), modules: lazyown_mcp (13), modules: html2pdf.bundle.min (5).

- `modules/llm_factory.py` ranks 1 by PageRank, 64 importers, 30 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Hotspot `tests/test_llm_adapter_parity.py`: 42 symbols, 26 connections (score 0.02).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> reactive_engine.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py, file:telegram_hermes.py, file:tests/test_dependencies.py, file:modules/lazy_agent.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 116.

## lazyc2/security (`c6`, community, rating 1.4)

59 files under tests (py 57, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0059, imported by 21 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on modules: world_model (36), modules: lazyown_mcp (35), cli/commands (15). Used by cli (13), modules: lazyown_mcp (10), modules: world_model (3).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- `lazyc2/security/cors.py` ranks 3 by PageRank, 4 importers, 15 symbols: CORS origin allowlist policy for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 311 symbols, 312 connections (score 0.19).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- 29 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _probe_bind).
- Key entities: file:lazyc2.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, sym:lazyc2.py::index@3331, file:tests/test_security_lazyc2.py, file:modules/event_bus.py, file:tests/test_loop_manager.py, sym:lazyc2.py::decoy@2055
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 149.

## lazygui/panels (`c7`, community, rating 1.4)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0064, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyown_mcp (8), modules: world_model (2), lazyc2/security (1). Used by modules: html2pdf.bundle.min (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 181.

## modules: chain_runner (`c9`, community, rating 0.9)

38 files under tests (py 38), mostly utility. Core file modules/chain_registry.py (PageRank 0.0042, imported by 52 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, identifier, resolve, evaluate_when, validate_chain. Depends on modules: world_model (17), modules: lazyown_mcp (13), cli/commands (13). Used by modules: lazy_loop (15), modules: world_model (6), modules: lazyown_mcp (2).

- `modules/chain_registry.py` ranks 1 by PageRank, 52 importers, 17 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `modules/defense_eval.py` ranks 2 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/chain_runner.py` ranks 3 by PageRank, 14 importers, 41 symbols: Single execution engine for YAML orchestration chains.
- Hotspot `modules/chain_runner.py`: 41 symbols, 45 connections (score 0.03).
- Hotspot `cli/commands/command_and_control_migrated.py`: 34 symbols, 79 connections (score 0.02).
- Key entities: file:modules/chain_runner.py, file:cli/commands/command_and_control_migrated.py, file:modules/chain_registry.py, file:tests/test_chain_runner.py, sym:modules/chain_registry.py::ChainStep@62, file:tests/test_chain_v24_core.py, file:tests/test_f4_hardening.py, sym:modules/chain_runner.py::ChainRunner@215
- Rating 0.9/10 = 7 x PageRank share 0.12 + 3 x risk 0.00. Internal imports: 107.

## skills/claude_md_orchestrator (`c10`, community, rating 0.6)

23 files under skills/claude_md_orchestrator (py 22, js 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0028, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on modules: lazyown_mcp (3), modules: html2pdf.bundle.min (3), cli/commands (2). Used by cli/commands (2), lazyc2/security (2), modules: lazyown_mcp (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `modules/colors.py` ranks 3 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:contrib/legacy/lazygptcli_unified.py, file:static/js/xterm.js, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py
- Rating 0.6/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 45.

## skills/hermes-lazyown (`c13`, community, rating 0.2)

7 files under skills/hermes-lazyown (py 7), mostly utility. Core file skills/hermes-lazyown/constants.py (PageRank 0.0021, imported by 6 files): Central constants for the Hermes-LazyOwn integration layer. Key abstractions: ConfigKeys, EnvKeys, Defaults, PhaseNames, Paths, lazyown_dir. Depends on cli/commands (1), modules: world_model (1).

- `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- `skills/hermes-lazyown/config_bridge.py` ranks 3 by PageRank, 1 importers, 16 symbols: Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source.
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/output_compactor.py`: 20 symbols, 5 connections (score 0.01).
- Key entities: file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/hermes-lazyown/constants.py, file:skills/hermes-lazyown/executor.py, file:skills/hermes-lazyown/config_bridge.py, file:skills/hermes-lazyown/hermes_sync.py, file:skills/hermes-lazyown/claudemd_rules.py, sym:skills/hermes-lazyown/mcp_server.py::_handle_tool@346
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 11.

## contrib/legacy (`c15`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0030, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 4.

## modules: kerberos_core (`c11`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0010, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c12`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0004, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c14`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0004, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## tests (`c16`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0013, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, sym:tests/mutation_common.py::run_all@56, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c17`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0010, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c18`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0007, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c19`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0007, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c20`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0007, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c21`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0007, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c22`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0007, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
