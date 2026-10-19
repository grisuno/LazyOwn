# GraphRAG Community Reports

Entities: 21816 | Relationships: 69031 | Communities: 23 | Themes: 10 | Text units: 21698

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1098 files in 23 communities and 10 themes. Highest-impact communities: cli/commands (7.0), modules: lazyc2 (6.8), cli (4.1). God nodes: core/logging.py, utils.py, skills/lazyown_mcp.py, modules/lazy_loop.py, cli/commands/_base.py.

- [cli/commands] rating 7.0: `utils.py` ranks 1 by PageRank, 118 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazyc2] rating 6.8: `core/logging.py` ranks 1 by PageRank, 176 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli] rating 4.1: `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: autonomous_daemon] rating 4.0: `cli/commands/enum.py` ranks 1 by PageRank, 24 importers, 11 symbols: Enumeration command set.
- [modules: lazy_loop] rating 3.7: `modules/lazy_loop.py` ranks 1 by PageRank, 193 importers, 461 symbols: Lazy autonomous loop for LazyOwn.
- [unassigned files] rating 3.6: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: llm_budget] rating 2.1: `modules/llm_factory.py` ranks 1 by PageRank, 49 importers, 28 symbols: LLM backend factory and selection utilities.
- [lazygui/panels] rating 1.7: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- Key entities: file:utils.py, file:tests/test_improvements_spec.py, file:lazyc2.py, file:tests/test_collab_and_onboarding.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9
- Root rating = highest community rating.

## cli/commands + contrib/legacy +3 (`t2`, theme, rating 7.0)

Theme of 5 communities and 187 files: cli/commands (162 files, rating 7.0); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 118 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:utils.py, file:tests/test_improvements_spec.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c0, c15, c12, c13, c14
- Theme rating = highest child community rating.

## modules: lazyc2 + cli +5 (`t0`, theme, rating 6.8)

Theme of 7 communities and 484 files: modules: lazyc2 (141 files, rating 6.8); cli (112 files, rating 4.1); modules: autonomous_daemon (115 files, rating 4.0); lazygui/panels (54 files, rating 1.7); static/js (31 files, rating 0.9); modules: lazyown_facts (22 files, rating 0.6); modules: opsec_scorer (9 files, rating 0.2).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 176 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `core/safe_exec.py` ranks 2 by PageRank, 59 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- [cli] `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `modules/killchain.py` ranks 2 by PageRank, 29 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 1 by PageRank, 24 importers, 11 symbols: Enumeration command set.
- [modules: autonomous_daemon] `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 150 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [lazygui/panels] `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [lazygui/panels] `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py
- Children: c1, c3, c2, c5, c7, c9, c11
- Theme rating = highest child community rating.

## modules: lazy_loop + modules: llm_budget +2 (`t3`, theme, rating 3.7)

Theme of 4 communities and 178 files: modules: lazy_loop (99 files, rating 3.7); modules: llm_budget (35 files, rating 2.1); skills/claude_md_orchestrator (29 files, rating 0.9); modules: surface_graph (15 files, rating 0.4).

- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 193 importers, 461 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/world_model.py` ranks 2 by PageRank, 79 importers, 64 symbols: modules/world_model.py
- [modules: llm_budget] `modules/llm_factory.py` ranks 1 by PageRank, 49 importers, 28 symbols: LLM backend factory and selection utilities.
- [modules: llm_budget] `core/payload_schema.py` ranks 2 by PageRank, 14 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- [skills/claude_md_orchestrator] `modules/backdoor/server.c` ranks 1 by PageRank, 13 importers, 1 symbols.
- [skills/claude_md_orchestrator] `skills/claude_md_orchestrator/models.py` ranks 2 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- [modules: surface_graph] `modules/osint_enrich.py` ranks 1 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- [modules: surface_graph] `modules/estorides_fusion.py` ranks 2 by PageRank, 8 importers, 11 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_payload_schema.py, file:modules/ai_model.py, sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:cli/surface_graph.py, file:modules/finding_lifecycle.py
- Children: c4, c6, c8, c10
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.6)

Theme of 1 communities and 236 files: unassigned files (236 files, rating 3.6).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c22
- Theme rating = highest child community rating.

## scripts: journal (`t4`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c16
- Theme rating = highest child community rating.

## modules/backdoor (`t5`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c17
- Theme rating = highest child community rating.

## poc_tui (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c18
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c19
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c20
- Theme rating = highest child community rating.

## tools (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c21
- Theme rating = highest child community rating.

## cli/commands (`c0`, community, rating 7.0)

162 files under cli/commands (py 161, c 1), mostly utility. Core file utils.py (PageRank 0.0250, imported by 118 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, needs_sudo, sudo_available. Depends on cli (73), modules: lazyc2 (32), modules: autonomous_daemon (28). Used by modules: lazy_loop (52), cli (40), modules: autonomous_daemon (32).

- `utils.py` ranks 1 by PageRank, 118 importers, 124 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 95 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.09).
- Hotspot `utils.py`: 124 symbols, 207 connections (score 0.08).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 7 paths reach this group via subprocess.
- Key entities: file:utils.py, file:tests/test_improvements_spec.py, file:cli/banner_config.py, file:tests/test_categories.py, file:tests/test_security_hardening_v3.py, file:tests/test_cli_command_sets.py, file:cli/cli_enhancements.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 506.

## modules: lazyc2 (`c1`, community, rating 6.8)

141 files under modules (py 139, js 2), mostly utility. Core file core/logging.py (PageRank 0.0754, imported by 176 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: lazy_loop (42), cli/commands (30), cli (18). Used by modules: autonomous_daemon (97), cli/commands (32), cli (26).

- `core/logging.py` ranks 1 by PageRank, 176 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `core/safe_exec.py` ranks 2 by PageRank, 59 importers, 12 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/lazy_rbac.py` ranks 3 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- Hotspot `lazyc2.py`: 288 symbols, 274 connections (score 0.18).
- Hotspot `tests/test_aci_planner.py`: 95 symbols, 85 connections (score 0.06).
- Dependency cycle: autonomous_daemon.py -> pipeline_engine.py -> autonomous_daemon.py.
- 42 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/lazy_rbac.py, file:modules/pipeline_engine.py, file:tests/test_security_hardening_v4.py, file:tests/test_aci_planner.py, file:tests/test_addon_creator.py
- Rating 6.8/10 = 7 x PageRank share 0.97 + 3 x risk 0.00. Internal imports: 492.

## cli (`c3`, community, rating 4.1)

112 files under tests (py 112), mostly utility. Core file core/console.py (PageRank 0.0189, imported by 64 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: lazy_loop (57), cli/commands (40), modules: lazyc2 (26). Used by cli/commands (73), modules: autonomous_daemon (45), modules: lazyc2 (18).

- `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/killchain.py` ranks 2 by PageRank, 29 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/cli_auth.py` ranks 3 by PageRank, 20 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `lazyown.py`: 129 symbols, 203 connections (score 0.09).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py, file:cli/status_bar.py
- Rating 4.1/10 = 7 x PageRank share 0.58 + 3 x risk 0.00. Internal imports: 470.

## modules: autonomous_daemon (`c2`, community, rating 4.0)

115 files under modules (py 115), mostly utility. Core file cli/commands/enum.py (PageRank 0.0244, imported by 24 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyc2 (97), modules: lazy_loop (66), cli (45). Used by cli/commands (28), modules: lazy_loop (24), modules: lazyc2 (15).

- `cli/commands/enum.py` ranks 1 by PageRank, 24 importers, 11 symbols: Enumeration command set.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 150 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `modules/detection_oracle.py` ranks 3 by PageRank, 20 importers, 17 symbols: modules/detection_oracle.py
- Hotspot `skills/lazyown_mcp.py`: 146 symbols, 488 connections (score 0.12).
- Hotspot `skills/autonomous_daemon.py`: 150 symbols, 259 connections (score 0.10).
- Dependency cycle: auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> auto_registry.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py, file:skills/tests/test_autonomous_daemon.py, sym:skills/lazyown_mcp.py::call_tool@6496
- Rating 4.0/10 = 7 x PageRank share 0.57 + 3 x risk 0.00. Internal imports: 671.

## modules: lazy_loop (`c4`, community, rating 3.7)

99 files under tests (py 99), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0110, imported by 193 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on cli/commands (52), modules: autonomous_daemon (24), modules: lazyc2 (22). Used by modules: autonomous_daemon (66), cli (57), modules: lazyc2 (42).

- `modules/lazy_loop.py` ranks 1 by PageRank, 193 importers, 461 symbols: Lazy autonomous loop for LazyOwn.
- `modules/world_model.py` ranks 2 by PageRank, 79 importers, 64 symbols: modules/world_model.py
- `modules/__init__.py` ranks 3 by PageRank, 88 importers, 0 symbols.
- Hotspot `modules/lazy_loop.py`: 461 symbols, 421 connections (score 0.28).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> auto_registry.py.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1008, file:modules/world_model.py, file:modules/lazy_proxy.py, sym:modules/lazy_loop.py::ExplorationGraph@1116, file:cli/lazy_orchestrator.py
- Rating 3.7/10 = 7 x PageRank share 0.53 + 3 x risk 0.00. Internal imports: 682.

## unassigned files (`c22`, community, rating 3.6)

236 files under modules (py 130, sh 61, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0004, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c, file:modules/rootkit/mrhyde2.c
- Rating 3.6/10 = 7 x PageRank share 0.51 + 3 x risk 0.00. Internal imports: 0.

## modules: llm_budget (`c6`, community, rating 2.1)

35 files under modules (py 35), mostly utility. Core file modules/llm_factory.py (PageRank 0.0136, imported by 49 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on cli/commands (23), modules: lazyc2 (12), cli (7). Used by modules: lazy_loop (14), modules: lazyc2 (10), modules: autonomous_daemon (9).

- `modules/llm_factory.py` ranks 1 by PageRank, 49 importers, 28 symbols: LLM backend factory and selection utilities.
- `core/payload_schema.py` ranks 2 by PageRank, 14 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- `modules/ai_model.py` ranks 3 by PageRank, 8 importers, 39 symbols: Concrete language model backends for LazyOwn.
- Hotspot `tests/test_payload_schema.py`: 53 symbols, 20 connections (score 0.03).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: llm_factory.py -> ai_model.py -> llm_factory.py.
- Taint: 4 paths reach this group via subprocess.
- Key entities: file:tests/test_payload_schema.py, file:modules/ai_model.py, file:modules/llm_factory.py, file:modules/agent_runner.py, file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py, file:core/payload_schema.py, file:tests/test_dependencies.py
- Rating 2.1/10 = 7 x PageRank share 0.30 + 3 x risk 0.00. Internal imports: 89.

## lazygui/panels (`c5`, community, rating 1.7)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0072, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (7), modules: autonomous_daemon (2), cli (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 181.

## static/js (`c7`, community, rating 0.9)

31 files under static/js (js 15, py 14, c 1, sh 1), mostly utility. Core file core/process.py (PageRank 0.0028, imported by 20 files): Process and subprocess utilities for the LazyOwn framework. Key abstractions: check_go_tool_installed, is_binary_present, handle_multiple_rhosts, wrapper, check_sudo, run. Depends on cli/commands (4), cli (4), modules: lazyc2 (3). Used by cli/commands (27), modules: llm_budget (7), modules: lazy_loop (4).

- `core/process.py` ranks 1 by PageRank, 20 importers, 12 symbols: Process and subprocess utilities for the LazyOwn framework.
- `cli/assign.py` ranks 2 by PageRank, 127 importers, 1 symbols: ``assign`` business logic.
- `modules/colors.py` ranks 3 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:static/js/force-graph-1.43.5.min.js
- Rating 0.9/10 = 7 x PageRank share 0.12 + 3 x risk 0.00. Internal imports: 236.

## skills/claude_md_orchestrator (`c8`, community, rating 0.9)

29 files under skills/claude_md_orchestrator (py 28, c 1), mostly utility. Core file modules/backdoor/server.c (PageRank 0.0034, imported by 13 files). Key abstractions: main, Stage, Severity, Contract, SadPath, Spec. Depends on cli/commands (6), modules: autonomous_daemon (3), cli (1). Used by cli/commands (4), modules: lazy_loop (4), modules: lazyc2 (3).

- `modules/backdoor/server.c` ranks 1 by PageRank, 13 importers, 1 symbols.
- `skills/claude_md_orchestrator/models.py` ranks 2 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 3 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in main).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/claude_md_orchestrator/validators.py, file:skills/hermes-lazyown/output_compactor.py, file:cli/commands/phishing_wizard.py
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 54.

## modules: lazyown_facts (`c9`, community, rating 0.6)

22 files under modules (py 22), mostly utility. Core file modules/chain_registry.py (PageRank 0.0026, imported by 33 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, identifier, resolve, evaluate_when, validate_chain. Depends on modules: lazy_loop (18), cli/commands (10), modules: lazyc2 (10). Used by modules: lazy_loop (14), modules: autonomous_daemon (12), modules: lazyc2 (2).

- `modules/chain_registry.py` ranks 1 by PageRank, 33 importers, 17 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `skills/lazyown_facts.py` ranks 2 by PageRank, 11 importers, 79 symbols: LazyOwn FactStore
- `modules/atomic_resolver.py` ranks 3 by PageRank, 15 importers, 27 symbols: Central MITRE ATT&CK <-> Atomic Red Team translator.
- Hotspot `skills/lazyown_facts.py`: 79 symbols, 23 connections (score 0.04).
- Hotspot `cli/commands/command_and_control_migrated.py`: 32 symbols, 71 connections (score 0.02).
- Dependency cycle: atomic_exploit_bridge.py -> emulation_runner.py -> atomic_exploit_bridge.py.
- Key entities: file:skills/lazyown_facts.py, file:cli/commands/command_and_control_migrated.py, file:skills/tests/test_facts.py, file:modules/chain_runner.py, file:tests/test_chain_runner.py, file:modules/atomic_resolver.py, file:tests/test_chain_v24_core.py, file:modules/chain_registry.py
- Rating 0.6/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 63.

## modules: surface_graph (`c10`, community, rating 0.4)

15 files under modules (py 15), mostly utility. Core file modules/osint_enrich.py (PageRank 0.0019, imported by 3 files): Keyless OSINT enrichment for finding evidence. Key abstractions: cve_lookup, reverse_dns, host_geo, domain_exposure, enrich_evidence, estorides_checkout. Depends on cli/commands (4), modules: lazy_loop (2), modules: lazyc2 (1). Used by modules: lazyc2 (6), modules: lazy_loop (6), cli/commands (4).

- `modules/osint_enrich.py` ranks 1 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- `modules/estorides_fusion.py` ranks 2 by PageRank, 8 importers, 11 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- `modules/finding_lifecycle.py` ranks 3 by PageRank, 11 importers, 26 symbols: Finding confirmation lifecycle: pending -> confirmed / rejected.
- Hotspot `cli/surface_graph.py`: 33 symbols, 15 connections (score 0.02).
- Hotspot `modules/finding_lifecycle.py`: 26 symbols, 18 connections (score 0.02).
- Key entities: file:cli/surface_graph.py, file:modules/finding_lifecycle.py, file:modules/intel_fusion.py, file:cli/surface_tui.py, file:modules/attack_surface3d.py, file:modules/estorides_fusion.py, file:modules/osint_enrich.py, file:cli/commands/database.py
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 29.

## modules: opsec_scorer (`c11`, community, rating 0.2)

9 files under modules (py 9), mostly utility. Core file modules/opsec_scorer.py (PageRank 0.0012, imported by 6 files): OPSEC scoring engine — pre-execution noise assessment and gated scoring. Key abstractions: RiskLevel, GateAction, OpsecContext, OpsecScore, GatedOpsecScore, OpsecScorer. Depends on cli/commands (2), modules: lazyc2 (2), modules: autonomous_daemon (1). Used by cli/commands (3).

- `modules/opsec_scorer.py` ranks 1 by PageRank, 6 importers, 36 symbols: OPSEC scoring engine — pre-execution noise assessment and gated scoring.
- `modules/log_tamper.py` ranks 2 by PageRank, 3 importers, 9 symbols: Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.
- `modules/forensic_cleaner.py` ranks 3 by PageRank, 1 importers, 8 symbols: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- Hotspot `modules/opsec_scorer.py`: 36 symbols, 20 connections (score 0.02).
- Hotspot `tests/test_opsec_scorer_consolidated.py`: 22 symbols, 3 connections (score 0.01).
- Key entities: file:modules/opsec_scorer.py, file:tests/test_opsec_scorer_consolidated.py, file:modules/timestomper.py, sym:modules/opsec_scorer.py::score@365, file:modules/network_opsec.py, file:cli/commands/opsec_cleanup.py, file:modules/forensic_cleaner.py, file:tests/test_opsec_scorer.py
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 10.

## contrib/legacy (`c15`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0034, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 4.

## modules: kerberos_core (`c12`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0012, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c13`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0005, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c14`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0005, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## scripts: journal (`c16`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0011, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c17`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0008, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c18`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0008, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c19`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0008, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c20`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0008, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c21`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0008, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
