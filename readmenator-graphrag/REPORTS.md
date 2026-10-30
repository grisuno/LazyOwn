# GraphRAG Community Reports

Entities: 24782 | Relationships: 79647 | Communities: 28 | Themes: 13 | Text units: 24682

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1278 files in 28 communities and 13 themes. Highest-impact communities: modules: autonomous_daemon (7.0), cli/commands (5.6), modules: world_model (3.8). God nodes: core/logging.py, modules/lazy_loop.py, utils.py, cli/commands/_base.py, skills/lazyown_mcp.py.

- [modules: autonomous_daemon] rating 7.0: `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 5.6: `utils.py` ranks 1 by PageRank, 135 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: world_model] rating 3.8: `modules/__init__.py` ranks 1 by PageRank, 201 importers, 0 symbols.
- [cli] rating 3.7: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 3.1: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: lazy_loop] rating 2.8: `modules/lazy_loop.py` ranks 1 by PageRank, 250 importers, 486 symbols: Lazy autonomous loop for LazyOwn.
- [static/js] rating 2.6: `core/config.py` ranks 1 by PageRank, 110 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazyown_facts] rating 1.8: `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py, file:utils.py, file:cli/banner_config.py, file:modules/world_model.py, file:poc_tui/app.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12
- Root rating = highest community rating.

## modules: autonomous_daemon + static/js +5 (`t0`, theme, rating 7.0)

Theme of 7 communities and 441 files: modules: autonomous_daemon (177 files, rating 7.0); static/js (64 files, rating 2.6); modules: llm_budget (41 files, rating 1.6); modules/guardrails (32 files, rating 1.4); lazygui/panels (54 files, rating 1.4); lazyc2/security (54 files, rating 1.3); skills/claude_md_orchestrator (19 files, rating 0.5).

- [modules: autonomous_daemon] `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: autonomous_daemon] `modules/logging_config.py` ranks 2 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- [static/js] `core/config.py` ranks 1 by PageRank, 110 importers, 20 symbols: Configuration loader and Config wrapper.
- [static/js] `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- [modules: llm_budget] `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- [modules: llm_budget] `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- [modules/guardrails] `cli/commands/enum.py` ranks 1 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- [modules/guardrails] `modules/guardrails/contracts.py` ranks 2 by PageRank, 3 importers, 10 symbols: Contracts for the execution guardrail harness.
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py, file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:tests/test_c2_profile_engine.py, file:tests/test_bof_registry.py
- Children: c0, c6, c9, c10, c8, c7, c11
- Theme rating = highest child community rating.

## cli/commands + cli +5 (`t1`, theme, rating 5.6)

Theme of 7 communities and 292 files: cli/commands (141 files, rating 5.6); cli (119 files, rating 3.7); skills/hermes-lazyown (7 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 135 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [cli] `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `modules/killchain.py` ranks 2 by PageRank, 36 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- [skills/hermes-lazyown] `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- [skills/hermes-lazyown] `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:utils.py, file:cli/banner_config.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py
- Children: c1, c2, c15, c17, c13, c14, c16
- Theme rating = highest child community rating.

## modules: world_model + modules: lazy_loop +2 (`t2`, theme, rating 3.8)

Theme of 4 communities and 283 files: modules: world_model (112 files, rating 3.8); modules: lazy_loop (99 files, rating 2.8); modules: lazyown_facts (64 files, rating 1.8); modules: defense_eval (8 files, rating 0.2).

- [modules: world_model] `modules/__init__.py` ranks 1 by PageRank, 201 importers, 0 symbols.
- [modules: world_model] `modules/world_model.py` ranks 2 by PageRank, 152 importers, 70 symbols: modules/world_model.py
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 250 importers, 486 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/auto_registry.py` ranks 2 by PageRank, 55 importers, 43 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- [modules: lazyown_facts] `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- [modules: lazyown_facts] `modules/chain_registry.py` ranks 2 by PageRank, 62 importers, 19 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- [modules: defense_eval] `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- [modules: defense_eval] `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- Key entities: file:modules/world_model.py, file:poc_tui/app.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:skills/lazyown_facts.py, file:tests/test_security_hardening_v4.py, file:modules/defense_eval.py, file:modules/hunt_verify.py
- Children: c3, c4, c5, c12
- Theme rating = highest child community rating.

## unassigned files (`t3`, theme, rating 3.1)

Theme of 1 communities and 241 files: unassigned files (241 files, rating 3.1).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c27
- Theme rating = highest child community rating.

## tests (`t4`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c18
- Theme rating = highest child community rating.

## scripts: journal (`t5`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c19
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c24
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t11`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c25
- Theme rating = highest child community rating.

## tools (`t12`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c26
- Theme rating = highest child community rating.

## modules/backdoor (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c20
- Theme rating = highest child community rating.

## modules: lazy_netattack (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_netattack (2 files, rating 0.0).

- [modules: lazy_netattack] `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- [modules: lazy_netattack] `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Key entities: file:modules/lazy_netattack.py, file:tests/test_lazy_netattack.py
- Children: c21
- Theme rating = highest child community rating.

## modules: lazy_triage (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_triage (2 files, rating 0.0).

- [modules: lazy_triage] `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- [modules: lazy_triage] `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py
- Children: c22
- Theme rating = highest child community rating.

## poc_tui (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c23
- Theme rating = highest child community rating.

## modules: autonomous_daemon (`c0`, community, rating 7.0)

177 files under modules (py 177), mostly utility. Core file core/logging.py (PageRank 0.0766, imported by 196 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: world_model (57), modules: lazyown_facts (37), modules: lazy_loop (27). Used by modules: llm_budget (36), modules: lazy_loop (34), lazyc2/security (34).

- `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/logging_config.py` ranks 2 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- `modules/factsio.py` ranks 3 by PageRank, 4 importers, 7 symbols: Canonical reader for the FactStore ``policy_facts.json`` document.
- Hotspot `skills/autonomous_daemon.py`: 157 symbols, 285 connections (score 0.11).
- Hotspot `skills/lazyown_mcp.py`: 131 symbols, 435 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 28 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py, file:skills/lazyown_policy.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 891.

## cli/commands (`c1`, community, rating 5.6)

141 files under cli/commands (py 140, c 1), mostly utility. Core file utils.py (PageRank 0.0224, imported by 135 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on cli (70), static/js (28), modules: autonomous_daemon (24). Used by modules: world_model (39), modules: lazy_loop (37), static/js (37).

- `utils.py` ranks 1 by PageRank, 135 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 106 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 126 symbols, 226 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Key entities: file:utils.py, file:cli/banner_config.py, file:tests/test_categories.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_winbox_gym.py, file:cli/commands/_base.py, file:tests/test_cli_command_sets.py, file:cli/cli_enhancements.py
- Rating 5.6/10 = 7 x PageRank share 0.79 + 3 x risk 0.00. Internal imports: 435.

## modules: world_model (`c3`, community, rating 3.8)

112 files under tests (py 112), mostly utility. Core file modules/__init__.py (PageRank 0.0163, imported by 201 files). Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: lazy_loop (53), cli/commands (39), static/js (27). Used by modules: lazy_loop (119), cli (61), modules: autonomous_daemon (57).

- `modules/__init__.py` ranks 1 by PageRank, 201 importers, 0 symbols.
- `modules/world_model.py` ranks 2 by PageRank, 152 importers, 70 symbols: modules/world_model.py
- `modules/outcome_bus.py` ranks 3 by PageRank, 41 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- Hotspot `modules/world_model.py`: 70 symbols, 181 connections (score 0.05).
- Hotspot `cli/orchestrator_assets_tabs.py`: 62 symbols, 109 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 2 layer violations, e.g. test_orchestrator_api.py (testing) -> api_authz.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:modules/world_model.py, file:poc_tui/app.py, file:poc_tui/test_app.py, file:modules/__init__.py, file:cli/orchestrator_assets_tabs.py, file:cli/lazy_orchestrator.py, file:modules/orchestrator_config.py, file:tests/test_infra_disposable.py
- Rating 3.8/10 = 7 x PageRank share 0.54 + 3 x risk 0.00. Internal imports: 381.

## cli (`c2`, community, rating 3.7)

119 files under tests (py 119), mostly utility. Core file core/console.py (PageRank 0.0159, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: world_model (61), modules: autonomous_daemon (32), cli/commands (32). Used by cli/commands (70), modules: autonomous_daemon (26), static/js (24).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/killchain.py` ranks 2 by PageRank, 36 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/cli_auth.py` ranks 3 by PageRank, 21 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 161 symbols, 48 connections (score 0.09).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py
- Rating 3.7/10 = 7 x PageRank share 0.53 + 3 x risk 0.00. Internal imports: 503.

## unassigned files (`c27`, community, rating 3.1)

241 files under modules (py 133, sh 63, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0003, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.1/10 = 7 x PageRank share 0.44 + 3 x risk 0.00. Internal imports: 0.

## modules: lazy_loop (`c4`, community, rating 2.8)

99 files under tests (py 99), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0137, imported by 250 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on modules: world_model (119), modules: llm_budget (45), cli/commands (37). Used by modules: world_model (53), modules: llm_budget (39), modules: autonomous_daemon (27).

- `modules/lazy_loop.py` ranks 1 by PageRank, 250 importers, 486 symbols: Lazy autonomous loop for LazyOwn.
- `modules/auto_registry.py` ranks 2 by PageRank, 55 importers, 43 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- `modules/lazy_cli_bridge.py` ranks 3 by PageRank, 17 importers, 14 symbols: Full CLI catalog for the Lazy autonomous loop.
- Hotspot `modules/lazy_loop.py`: 486 symbols, 584 connections (score 0.31).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1050, sym:modules/lazy_loop.py::ExplorationGraph@1158, sym:modules/lazy_loop.py::ActivityLog@1508, file:modules/lazy_proxy.py, file:tests/test_guardrails.py
- Rating 2.8/10 = 7 x PageRank share 0.40 + 3 x risk 0.00. Internal imports: 568.

## static/js (`c6`, community, rating 2.6)

64 files under tests (py 47, js 14, c 2, sh 1), mostly utility. Core file core/config.py (PageRank 0.0172, imported by 110 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (37), modules: autonomous_daemon (25), cli (24). Used by cli/commands (28), modules: world_model (27), modules: lazy_loop (19).

- `core/config.py` ranks 1 by PageRank, 110 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- `core/param_registry.py` ranks 3 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_core_defaults.py (testing) -> api.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:core/config.py
- Rating 2.6/10 = 7 x PageRank share 0.37 + 3 x risk 0.00. Internal imports: 351.

## modules: lazyown_facts (`c5`, community, rating 1.8)

64 files under tests (py 64), mostly utility. Core file core/safe_exec.py (PageRank 0.0080, imported by 62 files): Centralized safe command execution for the LazyOwn framework. Key abstractions: CommandInjectionError, UrlValidationError, needs_shell, safe_system, safe_run_argv, safe_run_shell. Depends on modules: autonomous_daemon (25), modules: world_model (23), cli/commands (20). Used by modules: autonomous_daemon (37), modules: world_model (19), modules: lazy_loop (13).

- `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/chain_registry.py` ranks 2 by PageRank, 62 importers, 19 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `modules/atomic_exploit_bridge.py` ranks 3 by PageRank, 51 importers, 39 symbols: Atomic exploit catalogue bridge — one YAML per exploit under ``exploits/``.
- Hotspot `skills/lazyown_facts.py`: 79 symbols, 24 connections (score 0.04).
- Hotspot `tests/test_security_hardening_v4.py`: 67 symbols, 67 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_facts.py, file:tests/test_security_hardening_v4.py, file:modules/chain_runner.py, file:modules/atomic_exploit_bridge.py, file:cli/commands/command_and_control_migrated.py, file:modules/chain_registry.py, sym:modules/chain_registry.py::ChainStep@102, file:modules/winbox_gym.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 248.

## modules: llm_budget (`c9`, community, rating 1.6)

41 files under modules (py 41), mostly utility. Core file modules/llm_factory.py (PageRank 0.0109, imported by 65 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazy_loop (39), modules: autonomous_daemon (36), modules: world_model (10). Used by modules: lazy_loop (45), modules: autonomous_daemon (10), cli/commands (4).

- `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `tests/test_llm_orchestrator.py`: 88 symbols, 55 connections (score 0.05).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Key entities: file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py, file:telegram_hermes.py, file:tests/test_dependencies.py
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 136.

## modules/guardrails (`c10`, community, rating 1.4)

32 files under tests (py 32), mostly utility. Core file cli/commands/enum.py (PageRank 0.0211, imported by 25 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on cli/commands (12), modules: autonomous_daemon (5), static/js (3). Used by modules: autonomous_daemon (14), cli (6), modules: world_model (5).

- `cli/commands/enum.py` ranks 1 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- `modules/guardrails/contracts.py` ranks 2 by PageRank, 3 importers, 10 symbols: Contracts for the execution guardrail harness.
- `modules/c2_profile_engine.py` ranks 3 by PageRank, 6 importers, 47 symbols: Extended malleable C2 profile engine with TLS, DNS, SMB, and WebSocket transports.
- Hotspot `tests/test_c2_profile_engine.py`: 63 symbols, 4 connections (score 0.03).
- Hotspot `tests/test_socks_proxy.py`: 52 symbols, 3 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_c2_profile_engine.py, file:tests/test_bof_registry.py, file:modules/c2_profile_engine.py, file:tests/test_socks_proxy.py, file:tests/test_scope_guard.py, file:modules/bof_registry.py, file:tests/test_sleep_obfuscation.py, file:modules/socks_proxy.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 63.

## lazygui/panels (`c8`, community, rating 1.4)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0060, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: autonomous_daemon (6), modules/guardrails (2), cli (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 181.

## lazyc2/security (`c7`, community, rating 1.3)

54 files under tests (py 52, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0056, imported by 21 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on modules: autonomous_daemon (34), modules: world_model (19), cli/commands (16). Used by modules: autonomous_daemon (8), cli (7), static/js (3).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- `lazyc2/security/cors.py` ranks 3 by PageRank, 4 importers, 15 symbols: CORS origin allowlist policy for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 313 symbols, 316 connections (score 0.19).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- 29 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _probe_bind).
- Key entities: file:lazyc2.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, sym:lazyc2.py::index@3331, file:tests/test_security_lazyc2.py, file:tests/test_loop_manager.py, sym:lazyc2.py::decoy@2055, file:tests/test_security_sanitizers.py
- Rating 1.3/10 = 7 x PageRank share 0.18 + 3 x risk 0.00. Internal imports: 123.

## skills/claude_md_orchestrator (`c11`, community, rating 0.5)

19 files under skills/claude_md_orchestrator (py 18, js 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0026, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on static/js (3), modules: autonomous_daemon (2), cli/commands (1). Used by cli/commands (2), lazyc2/security (2), modules: lazy_loop (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `modules/colors.py` ranks 3 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:skills/claude_md_orchestrator/models.py, file:contrib/legacy/lazygptcli_unified.py, file:static/js/xterm.js, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:skills/claude_md_orchestrator/parser.py
- Rating 0.5/10 = 7 x PageRank share 0.08 + 3 x risk 0.00. Internal imports: 41.

## modules: defense_eval (`c12`, community, rating 0.2)

8 files under modules (py 8), mostly testing. Core file modules/defense_eval.py (PageRank 0.0015, imported by 4 files): Detection rule replay over recorded attack and control logs. Key abstractions: RuleEvaluationError, Condition, Evaluation, DatasetSummary, RuleResult, to_dict. Depends on modules: world_model (2), modules: autonomous_daemon (1). Used by modules: lazy_loop (3), modules: lazyown_facts (1).

- `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- `modules/closedloop.py` ranks 3 by PageRank, 2 importers, 7 symbols: Closed-loop detection rule tuning: baseline vs candidate comparison.
- Hotspot `modules/defense_eval.py`: 17 symbols, 9 connections (score 0.01).
- Hotspot `modules/hunt_verify.py`: 16 symbols, 6 connections (score 0.01).
- Key entities: file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/defense_stages.py, sym:modules/defense_eval.py::evaluate_rule@322, file:tests/test_defense_eval.py, file:tests/test_hunt_verify.py, file:modules/closedloop.py, sym:modules/hunt_verify.py::verify_stages@232
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## skills/hermes-lazyown (`c15`, community, rating 0.2)

7 files under skills/hermes-lazyown (py 7), mostly utility. Core file skills/hermes-lazyown/constants.py (PageRank 0.0020, imported by 6 files): Central constants for the Hermes-LazyOwn integration layer. Key abstractions: ConfigKeys, EnvKeys, Defaults, PhaseNames, Paths, lazyown_dir. Depends on cli/commands (1), cli (1).

- `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- `skills/hermes-lazyown/config_bridge.py` ranks 3 by PageRank, 1 importers, 16 symbols: Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source.
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/output_compactor.py`: 20 symbols, 5 connections (score 0.01).
- Key entities: file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/hermes-lazyown/constants.py, file:skills/hermes-lazyown/executor.py, file:skills/hermes-lazyown/config_bridge.py, file:skills/hermes-lazyown/hermes_sync.py, file:skills/hermes-lazyown/claudemd_rules.py, sym:skills/hermes-lazyown/mcp_server.py::_handle_tool@346
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 11.

## contrib/legacy (`c17`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0029, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 4.

## modules: kerberos_core (`c13`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0010, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c14`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0004, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c16`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0004, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## tests (`c18`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0012, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, sym:tests/mutation_common.py::run_all@56, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c19`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0009, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c20`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0006, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_netattack (`c21`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_netattack.py (PageRank 0.0006, imported by 1 files): Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. Key abstractions: AttackVectorVerdict, SurfaceEvidence, as_dict, surface_decision, hint_text, TestIdentity.

- `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Hotspot `tests/test_lazy_netattack.py`: 17 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_netattack.py`: 12 symbols, 4 connections (score 0.01).
- Key entities: file:modules/lazy_netattack.py, file:tests/test_lazy_netattack.py, sym:modules/lazy_netattack.py::surface_decision@184, sym:modules/lazy_netattack.py::SurfaceEvidence@120, sym:tests/test_lazy_netattack.py::test_hint_text_shapes@102, sym:tests/test_lazy_netattack.py::test_linux_host_blocked@56, sym:modules/lazy_netattack.py::hint_text@311, sym:tests/test_lazy_netattack.py::ad_domain_controller@35
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_triage (`c22`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_triage.py (PageRank 0.0006, imported by 1 files): Triage doctrine: evidence floors, verdict algebra and signature dedup. Key abstractions: SignatureStore, rank, hard_evidence, apply_rules, signature_for, fresh_signature.

- `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Hotspot `tests/test_lazy_triage.py`: 11 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_triage.py`: 10 symbols, 6 connections (score 0.01).
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py, sym:modules/lazy_triage.py::apply_rules@80, sym:modules/lazy_triage.py::fresh_signature@144, sym:modules/lazy_triage.py::_save@176, sym:modules/lazy_triage.py::hard_evidence@47, sym:modules/lazy_triage.py::SignatureStore@135, sym:modules/lazy_triage.py::signature_for@108
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c23`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0006, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c24`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0006, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c25`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0006, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c26`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0006, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
