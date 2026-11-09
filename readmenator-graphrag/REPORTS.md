# GraphRAG Community Reports

Entities: 25996 | Relationships: 84607 | Communities: 31 | Themes: 14 | Text units: 25879

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1526 files in 31 communities and 14 themes. Highest-impact communities: cli/commands (7.0), modules: lazyc2 (6.6), skills/mcp_tools (5.4). God nodes: skills/mcp_tools/_context.py, core/logging.py, modules/lazy_loop.py, utils.py, modules/__init__.py.

- [cli/commands] rating 7.0: `modules/__init__.py` ranks 1 by PageRank, 264 importers, 0 symbols.
- [modules: lazyc2] rating 6.6: `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [skills/mcp_tools] rating 5.4: `skills/mcp_tools/_context.py` ranks 1 by PageRank, 176 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [modules: lazyown] rating 4.3: `core/config.py` ranks 1 by PageRank, 120 importers, 20 symbols: Configuration loader and Config wrapper.
- [cli] rating 3.1: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 3.1: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: lazy_loop] rating 3.1: `modules/lazy_loop.py` ranks 1 by PageRank, 286 importers, 458 symbols: Lazy autonomous loop for LazyOwn.
- [modules: chain_runner] rating 2.3: `modules/chain_registry.py` ranks 1 by PageRank, 71 importers, 20 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- Key entities: file:utils.py, file:cli/banner_config.py, file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13
- Root rating = highest community rating.

## cli/commands + modules: lazyown +6 (`t2`, theme, rating 7.0)

Theme of 8 communities and 314 files: cli/commands (166 files, rating 7.0); modules: lazyown (109 files, rating 4.3); modules: defense_eval (8 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: network_opsec (6 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `modules/__init__.py` ranks 1 by PageRank, 264 importers, 0 symbols.
- [cli/commands] `utils.py` ranks 2 by PageRank, 141 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazyown] `core/config.py` ranks 1 by PageRank, 120 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazyown] `modules/world_model.py` ranks 2 by PageRank, 157 importers, 70 symbols: modules/world_model.py
- [modules: defense_eval] `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- [modules: defense_eval] `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:utils.py, file:cli/banner_config.py, file:lazyown.py, file:modules/world_model.py, file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py
- Children: c1, c5, c14, c19, c15, c16, c17, c18
- Theme rating = highest child community rating.

## modules: lazyc2 + modules: chain_runner +5 (`t1`, theme, rating 6.6)

Theme of 7 communities and 407 files: modules: lazyc2 (141 files, rating 6.6); modules: chain_runner (90 files, rating 2.3); static/js (49 files, rating 1.7); modules: llm_budget (37 files, rating 1.5); lazygui/panels (54 files, rating 1.4); modules/guardrails (22 files, rating 1.3); skills/claude_md_orchestrator (14 files, rating 0.4).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [modules: chain_runner] `modules/chain_registry.py` ranks 1 by PageRank, 71 importers, 20 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- [modules: chain_runner] `modules/selection/base.py` ranks 2 by PageRank, 29 importers, 4 symbols: The one shared contract for autonomous action selection.
- [static/js] `core/payload_schema.py` ranks 1 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- [static/js] `core/param_registry.py` ranks 2 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- [modules: llm_budget] `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- [modules: llm_budget] `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, sym:modules/workspace.py::write_text@72, file:modules/chain_runner.py, file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py
- Children: c2, c6, c9, c10, c8, c11, c13
- Theme rating = highest child community rating.

## skills/mcp_tools + cli +3 (`t0`, theme, rating 5.4)

Theme of 5 communities and 536 files: skills/mcp_tools (222 files, rating 5.4); cli (114 files, rating 3.1); modules: lazy_loop (110 files, rating 3.1); modules: atomic_exploit_bridge (73 files, rating 1.8); modules: dashboard_engine (17 files, rating 0.3).

- [skills/mcp_tools] `skills/mcp_tools/_context.py` ranks 1 by PageRank, 176 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [skills/mcp_tools] `skills/autonomous_daemon.py` ranks 2 by PageRank, 120 importers, 158 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [cli] `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `cli/themes.py` ranks 2 by PageRank, 18 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 286 importers, 458 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/lazy_engine.py` ranks 2 by PageRank, 143 importers, 1 symbols: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- [modules: atomic_exploit_bridge] `modules/outcome_bus.py` ranks 1 by PageRank, 46 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- [modules: atomic_exploit_bridge] `modules/lazy_heat.py` ranks 2 by PageRank, 12 importers, 15 symbols: Heat tiers and version math for CVE correlation.
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, file:modules/atomic_exploit_bridge.py, file:modules/outcome_bus.py
- Children: c0, c3, c4, c7, c12
- Theme rating = highest child community rating.

## unassigned files (`t3`, theme, rating 3.1)

Theme of 1 communities and 245 files: unassigned files (245 files, rating 3.1).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c30
- Theme rating = highest child community rating.

## tests (`t4`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c20
- Theme rating = highest child community rating.

## modules: memory_store (`t5`, theme, rating 0.1)

Theme of 1 communities and 3 files: modules: memory_store (3 files, rating 0.1).

- [modules: memory_store] `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- [modules: memory_store] `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py
- Children: c21
- Theme rating = highest child community rating.

## scripts: journal (`t6`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c22
- Theme rating = highest child community rating.

## poc_tui (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c26
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t11`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c27
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t12`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c28
- Theme rating = highest child community rating.

## tools (`t13`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c29
- Theme rating = highest child community rating.

## modules/backdoor (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c23
- Theme rating = highest child community rating.

## modules: lazy_netattack (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_netattack (2 files, rating 0.0).

- [modules: lazy_netattack] `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- [modules: lazy_netattack] `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py
- Children: c24
- Theme rating = highest child community rating.

## modules: lazy_triage (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_triage (2 files, rating 0.0).

- [modules: lazy_triage] `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- [modules: lazy_triage] `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py
- Children: c25
- Theme rating = highest child community rating.

## cli/commands (`c1`, community, rating 7.0)

166 files under cli/commands (py 166), mostly utility. Core file modules/__init__.py (PageRank 0.0215, imported by 264 files). Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on modules: lazyown (33), modules: lazyc2 (30), modules: atomic_exploit_bridge (26). Used by modules: lazy_loop (114), modules: lazyown (94), cli (48).

- `modules/__init__.py` ranks 1 by PageRank, 264 importers, 0 symbols.
- `utils.py` ranks 2 by PageRank, 141 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 3 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- Hotspot `utils.py`: 126 symbols, 232 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 2 layer violations, e.g. test_security_hardening_v5.py (testing) -> addons.py (presentation).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:utils.py, file:cli/banner_config.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:modules/__init__.py, file:tests/test_security_hardening_v4.py, file:tests/test_categories.py, file:tests/test_winbox_gym.py, file:cli/commands/_base.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 474.

## modules: lazyc2 (`c2`, community, rating 6.6)

141 files under modules (py 138, js 2, c 1), mostly utility. Core file core/logging.py (PageRank 0.0712, imported by 196 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: lazyown (47), cli/commands (27), skills/mcp_tools (16). Used by skills/mcp_tools (57), modules: lazyown (46), cli/commands (30).

- `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `modules/logging_config.py` ranks 3 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `lazyc2.py`: 313 symbols, 316 connections (score 0.19).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 18 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/lazy_rbac.py, file:skills/lazyown_facts.py, file:tests/test_addon_creator.py, sym:lazyc2.py::index@3331, file:tests/test_security_lazyc2.py
- Rating 6.6/10 = 7 x PageRank share 0.94 + 3 x risk 0.00. Internal imports: 359.

## skills/mcp_tools (`c0`, community, rating 5.4)

222 files under skills/mcp_tools (py 222), mostly utility. Core file skills/mcp_tools/_context.py (PageRank 0.0255, imported by 176 files): Dependency-injection context handed to every ``mcp_tools`` handler. Key abstractions: MCPContext, ICommandRunner, MCPCommandRunner, PTYCommandRunner, CommandRunnerChain, ICommandSelector. Depends on modules: lazyc2 (57), modules: lazyown (24), cli/commands (23). Used by modules: lazy_loop (29), modules: llm_budget (18), cli (17).

- `skills/mcp_tools/_context.py` ranks 1 by PageRank, 176 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 120 importers, 158 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `modules/detection_oracle.py` ranks 3 by PageRank, 23 importers, 18 symbols: modules/detection_oracle.py
- Hotspot `skills/autonomous_daemon.py`: 158 symbols, 304 connections (score 0.11).
- Hotspot `skills/lazyown_policy.py`: 126 symbols, 58 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Surprising bridge: kerberos_core.py <-> lazy_opencode_config.py (9 hops across communities).
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:skills/lazyown_mcp.py, file:skills/mcp_tools/_context.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py, file:skills/tests/test_autonomous_daemon.py
- Rating 5.4/10 = 7 x PageRank share 0.78 + 3 x risk 0.00. Internal imports: 795.

## modules: lazyown (`c5`, community, rating 4.3)

109 files under tests (py 109), mostly utility. Core file core/config.py (PageRank 0.0157, imported by 120 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (94), modules: lazy_loop (49), modules: lazyc2 (46). Used by cli (67), modules: lazy_loop (62), modules: lazyc2 (47).

- `core/config.py` ranks 1 by PageRank, 120 importers, 20 symbols: Configuration loader and Config wrapper.
- `modules/world_model.py` ranks 2 by PageRank, 157 importers, 70 symbols: modules/world_model.py
- `modules/killchain.py` ranks 3 by PageRank, 38 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- Hotspot `lazyown.py`: 124 symbols, 211 connections (score 0.08).
- Hotspot `modules/world_model.py`: 70 symbols, 186 connections (score 0.05).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- 24 layer violations, e.g. test_api_authz.py (testing) -> api_authz.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:lazyown.py, file:modules/world_model.py, file:tests/test_cli_command_sets.py, file:cli/cli_enhancements.py, file:tests/test_guardrails.py, file:core/config.py, file:cli/ops_commands.py, file:tests/test_c2_profile_engine.py
- Rating 4.3/10 = 7 x PageRank share 0.62 + 3 x risk 0.00. Internal imports: 502.

## cli (`c3`, community, rating 3.1)

114 files under tests (py 114), mostly utility. Core file core/console.py (PageRank 0.0137, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: lazyown (67), cli/commands (48), skills/mcp_tools (17). Used by modules: lazyown (41), cli/commands (16), skills/mcp_tools (15).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `cli/themes.py` ranks 2 by PageRank, 18 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `core/text_utils.py` ranks 3 by PageRank, 8 importers, 1 symbols: Shared text helpers for terminal surfaces.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 161 symbols, 48 connections (score 0.09).
- 6 layer violations, e.g. test_core_defaults.py (testing) -> api.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 2 INFERRED issues (first: UNCHECKED_ALLOC in do_suggest_next).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py, file:cli/tips_engine.py
- Rating 3.1/10 = 7 x PageRank share 0.45 + 3 x risk 0.00. Internal imports: 383.

## unassigned files (`c30`, community, rating 3.1)

245 files under modules (py 137, sh 63, lua 26, c 10, js 3, php 3, asm 1, cpp 1, cs 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0003, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `tests/test_attack_surface_addons.py`: 76 symbols, 5 connections (score 0.04).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.1/10 = 7 x PageRank share 0.44 + 3 x risk 0.00. Internal imports: 0.

## modules: lazy_loop (`c4`, community, rating 3.1)

110 files under tests (py 110), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0141, imported by 286 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on cli/commands (114), modules: lazyown (62), modules: chain_runner (39). Used by modules: chain_runner (54), modules: lazyown (49), modules: llm_budget (31).

- `modules/lazy_loop.py` ranks 1 by PageRank, 286 importers, 458 symbols: Lazy autonomous loop for LazyOwn.
- `modules/lazy_engine.py` ranks 2 by PageRank, 143 importers, 1 symbols: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- `modules/lazy_cli_bridge.py` ranks 3 by PageRank, 18 importers, 15 symbols: Full CLI catalog for the Lazy autonomous loop.
- Hotspot `modules/lazy_loop.py`: 458 symbols, 596 connections (score 0.29).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 266 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in health_check).
- Surprising bridge: kerberos_core.py <-> selector_manager.py (9 hops across communities).
- Key entities: file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1127, sym:modules/lazy_loop.py::ExplorationGraph@1235, sym:modules/lazy_loop.py::ActivityLog@1585, file:modules/lazy_proxy.py, file:cli/commands/lazyops.py, file:tests/test_mediation.py
- Rating 3.1/10 = 7 x PageRank share 0.44 + 3 x risk 0.00. Internal imports: 478.

## modules: chain_runner (`c6`, community, rating 2.3)

90 files under tests (py 87, c 2, js 1), mostly utility. Core file modules/chain_registry.py (PageRank 0.0055, imported by 71 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, skip_pending, identifier, resolve, evaluate_when. Depends on modules: lazy_loop (54), cli/commands (36), modules: atomic_exploit_bridge (21). Used by modules: lazy_loop (39), modules: lazyown (22), skills/mcp_tools (18).

- `modules/chain_registry.py` ranks 1 by PageRank, 71 importers, 20 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `modules/selection/base.py` ranks 2 by PageRank, 29 importers, 4 symbols: The one shared contract for autonomous action selection.
- `modules/auto_registry.py` ranks 3 by PageRank, 68 importers, 45 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 973 connections (score 0.08).
- Hotspot `modules/auto_registry.py`: 45 symbols, 124 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/chain_runner.py, file:modules/auto_registry.py, file:modules/rootkit/rootkit.c, sym:modules/chain_registry.py::ChainStep@104, file:modules/chain_registry.py, file:cli/commands/command_and_control_migrated.py, file:tests/test_lazy_loop.py
- Rating 2.3/10 = 7 x PageRank share 0.32 + 3 x risk 0.00. Internal imports: 290.

## modules: atomic_exploit_bridge (`c7`, community, rating 1.8)

73 files under modules (py 73), mostly utility. Core file modules/outcome_bus.py (PageRank 0.0041, imported by 46 files): Single fan-out contract for engagement outcomes. Key abstractions: OutcomeEvent, OutcomeBus, host_value, key, to_dict, reset. Depends on cli/commands (30), modules: lazyown (24), modules: lazy_loop (22). Used by modules: lazy_loop (28), cli/commands (26), modules: chain_runner (21).

- `modules/outcome_bus.py` ranks 1 by PageRank, 46 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- `modules/lazy_heat.py` ranks 2 by PageRank, 12 importers, 15 symbols: Heat tiers and version math for CVE correlation.
- `modules/atomic_exploit_bridge.py` ranks 3 by PageRank, 52 importers, 39 symbols: Atomic exploit catalogue bridge — one YAML per exploit under ``exploits/``.
- Hotspot `modules/atomic_exploit_bridge.py`: 39 symbols, 100 connections (score 0.03).
- Hotspot `modules/intel_fusion.py`: 35 symbols, 48 connections (score 0.02).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Key entities: file:modules/atomic_exploit_bridge.py, file:modules/outcome_bus.py, file:modules/intel_fusion.py, file:modules/payload_factory.py, file:cli/surface_graph.py, file:tests/test_payload_factory.py, file:modules/finding_lifecycle.py, file:tests/test_lazy_feedmatch.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 144.

## static/js (`c9`, community, rating 1.7)

49 files under static/js (py 30, js 16, c 1, php 1, sh 1), mostly utility. Core file core/payload_schema.py (PageRank 0.0121, imported by 22 files): Declarative schema and validation for ``payload.json``. Key abstractions: FieldKind, Severity, FieldSpec, ValidationIssue, register_specs, unregister_specs. Depends on modules: lazyown (46), skills/mcp_tools (14), cli/commands (14). Used by cli (13), modules: lazyown (13), cli/commands (4).

- `core/payload_schema.py` ranks 1 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- `core/param_registry.py` ranks 2 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- `core/process.py` ranks 3 by PageRank, 21 importers, 12 symbols: Process and subprocess utilities for the LazyOwn framework.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- Taint: 2 paths reach this group via subprocess.
- Dataflow: 9 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:tests/test_payload_schema.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 310.

## modules: llm_budget (`c10`, community, rating 1.5)

37 files under modules (py 37), mostly utility. Core file modules/llm_factory.py (PageRank 0.0099, imported by 65 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazy_loop (31), skills/mcp_tools (18), modules: lazyc2 (15). Used by modules: lazy_loop (39), skills/mcp_tools (6), cli (4).

- `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `tests/test_llm_orchestrator.py`: 88 symbols, 55 connections (score 0.05).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:tests/test_llm_adapter_parity.py, file:core/llm_budget.py, file:telegram_hermes.py, file:modules/lazy_agent.py
- Rating 1.5/10 = 7 x PageRank share 0.22 + 3 x risk 0.00. Internal imports: 124.

## lazygui/panels (`c8`, community, rating 1.4)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0050, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (7), modules: lazyown (2), modules/guardrails (2). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 181.

## modules/guardrails (`c11`, community, rating 1.3)

22 files under modules/guardrails (py 22), mostly utility. Core file cli/commands/enum.py (PageRank 0.0185, imported by 25 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on skills/mcp_tools (5), cli/commands (4), modules: lazyc2 (3). Used by modules: lazyown (21), skills/mcp_tools (9), cli/commands (6).

- `cli/commands/enum.py` ranks 1 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- `modules/guardrails/contracts.py` ranks 2 by PageRank, 3 importers, 10 symbols: Contracts for the execution guardrail harness.
- `modules/sleep_obfuscation.py` ranks 3 by PageRank, 5 importers, 28 symbols: Sleep obfuscation engine for beacon memory evasion.
- Hotspot `tests/test_socks_proxy.py`: 52 symbols, 3 connections (score 0.03).
- Hotspot `tests/test_bof_registry.py`: 51 symbols, 6 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_bof_registry.py, file:tests/test_socks_proxy.py, file:tests/test_scope_guard.py, file:modules/bof_registry.py, file:tests/test_sleep_obfuscation.py, file:modules/socks_proxy.py, file:modules/sleep_obfuscation.py, file:cli/commands/enum.py
- Rating 1.3/10 = 7 x PageRank share 0.18 + 3 x risk 0.00. Internal imports: 33.

## skills/claude_md_orchestrator (`c13`, community, rating 0.4)

14 files under skills/claude_md_orchestrator (py 14), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0022, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on modules: lazy_loop (16), modules: chain_runner (3), modules: lazyc2 (2). Used by cli/commands (2), modules: lazyc2 (1), static/js (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `tests/test_security_codeql_batch.py`: 37 symbols, 58 connections (score 0.02).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:skills/claude_md_orchestrator/models.py, file:tests/test_security_codeql_batch.py, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:skills/claude_md_orchestrator/parser.py, sym:skills/claude_md_orchestrator/validators.py::finditer@81
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 34.

## modules: dashboard_engine (`c12`, community, rating 0.3)

17 files under modules (py 17), mostly utility. Core file cli/commands/pwn.py (PageRank 0.0010, imported by 3 files): Autonomous exploitation and LOLBAS command set. Key abstractions: PwnCommandSet, do_auto_pwn, do_rich_tui, do_exploit_chain, do_lolbas_list, do_lolbas_use. Depends on modules: lazyown (9), skills/mcp_tools (7), cli/commands (6). Used by modules: lazyc2 (1), modules: lazy_loop (1).

- `cli/commands/pwn.py` ranks 1 by PageRank, 3 importers, 8 symbols: Autonomous exploitation and LOLBAS command set.
- `lazygui/version.py` ranks 2 by PageRank, 3 importers, 0 symbols: Single source of truth for the package version string.
- `modules/dashboard_engine.py` ranks 3 by PageRank, 6 importers, 16 symbols: Live Network Map Dashboard for LazyOwn.
- Hotspot `modules/exploit_recommender.py`: 16 symbols, 21 connections (score 0.01).
- Hotspot `tests/test_unified_dashboard.py`: 18 symbols, 4 connections (score 0.01).
- Key entities: file:modules/rich_tui.py, file:modules/exploit_recommender.py, file:modules/dashboard_engine.py, file:modules/unified_dashboard.py, file:tests/test_unified_dashboard.py, file:cli/commands/pwn.py, file:contrib/legacy/lazypwn.py, sym:modules/live_surface.py::build_live_graph@72
- Rating 0.3/10 = 7 x PageRank share 0.05 + 3 x risk 0.00. Internal imports: 23.

## modules: defense_eval (`c14`, community, rating 0.2)

8 files under modules (py 8), mostly testing. Core file modules/defense_eval.py (PageRank 0.0012, imported by 4 files): Detection rule replay over recorded attack and control logs. Key abstractions: RuleEvaluationError, Condition, Evaluation, DatasetSummary, RuleResult, to_dict. Depends on cli/commands (1), modules: lazyc2 (1), modules: lazyown (1). Used by modules: lazy_loop (3), modules: chain_runner (1).

- `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- `modules/closedloop.py` ranks 3 by PageRank, 2 importers, 7 symbols: Closed-loop detection rule tuning: baseline vs candidate comparison.
- Hotspot `modules/defense_eval.py`: 17 symbols, 9 connections (score 0.01).
- Hotspot `modules/hunt_verify.py`: 16 symbols, 6 connections (score 0.01).
- Key entities: file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/defense_stages.py, sym:modules/defense_eval.py::evaluate_rule@322, file:tests/test_defense_eval.py, file:tests/test_hunt_verify.py, file:modules/closedloop.py, sym:modules/hunt_verify.py::verify_stages@232
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## contrib/legacy (`c19`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0024, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 4.

## modules: kerberos_core (`c15`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0008, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, sym:modules/kerberos_tickets.py::forge@134, file:cli/commands/active_directory.py
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c16`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0003, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/k8s_attacks.py, file:modules/gcp_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 6.

## modules: network_opsec (`c17`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/log_tamper.py (PageRank 0.0004, imported by 3 files): Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. Key abstractions: LogTamperConfig, LogTamper, windows_clear_commands, linux_clear_commands, macos_clear_commands, generate_all. Depends on cli/commands (1), modules: lazyown (1).

- `modules/log_tamper.py` ranks 1 by PageRank, 3 importers, 9 symbols: Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.
- `modules/forensic_cleaner.py` ranks 2 by PageRank, 1 importers, 8 symbols: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- `modules/memory_cleaner.py` ranks 3 by PageRank, 1 importers, 7 symbols: Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear.
- Hotspot `modules/network_opsec.py`: 12 symbols, 8 connections (score 0.01).
- Hotspot `modules/timestomper.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/timestomper.py, file:modules/network_opsec.py, file:cli/commands/opsec_cleanup.py, file:modules/forensic_cleaner.py, file:modules/log_tamper.py, file:modules/memory_cleaner.py, sym:cli/commands/opsec_cleanup.py::do_network_opsec@342, sym:cli/commands/opsec_cleanup.py::do_forensic_clean@162
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 7.

## modules: polymorphic_engine (`c18`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0003, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## tests (`c20`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0010, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, sym:tests/mutation_common.py::run_all@56, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## modules: memory_store (`c21`, community, rating 0.1)

3 files under modules (py 3), mostly data_access. Core file modules/memory_embeddings.py (PageRank 0.0007, imported by 2 files): Hashing-trick text embeddings for episodic memory recall. Key abstractions: EmbeddingError, embed, cosine, semantic_top_k, as_floats, MemoryEntry.

- `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- `tests/test_memory_semantics.py` ranks 3 by PageRank, 0 importers, 14 symbols: BDD tests for hashing embeddings and hybrid episodic recall.
- Hotspot `modules/memory_store.py`: 38 symbols, 13 connections (score 0.02).
- Hotspot `tests/test_memory_semantics.py`: 14 symbols, 8 connections (score 0.01).
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py, file:modules/memory_embeddings.py, sym:modules/memory_embeddings.py::embed@50, sym:modules/memory_store.py::get_memory_store@339, sym:modules/memory_store.py::_cli@381, sym:modules/memory_store.py::VectorSQLiteBackend@315, sym:tests/test_memory_semantics.py::_entry@14
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c22`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0008, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c23`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0005, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_netattack (`c24`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_netattack.py (PageRank 0.0005, imported by 1 files): Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. Key abstractions: AttackVectorVerdict, SurfaceEvidence, as_dict, surface_decision, hint_text, TestIdentity.

- `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Hotspot `tests/test_lazy_netattack.py`: 17 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_netattack.py`: 12 symbols, 4 connections (score 0.01).
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py, sym:modules/lazy_netattack.py::surface_decision@184, sym:modules/lazy_netattack.py::SurfaceEvidence@120, sym:tests/test_lazy_netattack.py::test_hint_text_shapes@102, sym:tests/test_lazy_netattack.py::test_linux_host_blocked@56, sym:modules/lazy_netattack.py::hint_text@311, sym:tests/test_lazy_netattack.py::ad_domain_controller@35
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_triage (`c25`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_triage.py (PageRank 0.0005, imported by 1 files): Triage doctrine: evidence floors, verdict algebra and signature dedup. Key abstractions: SignatureStore, rank, hard_evidence, apply_rules, signature_for, fresh_signature.

- `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Hotspot `tests/test_lazy_triage.py`: 11 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_triage.py`: 10 symbols, 6 connections (score 0.01).
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py, sym:modules/lazy_triage.py::apply_rules@80, sym:modules/lazy_triage.py::fresh_signature@144, sym:modules/lazy_triage.py::_save@176, sym:modules/lazy_triage.py::hard_evidence@47, sym:modules/lazy_triage.py::SignatureStore@135, sym:modules/lazy_triage.py::signature_for@108
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c26`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0005, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c27`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0005, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c28`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0005, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c29`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0005, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
