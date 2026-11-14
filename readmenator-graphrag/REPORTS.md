# GraphRAG Community Reports

Entities: 27262 | Relationships: 89445 | Communities: 30 | Themes: 14 | Text units: 27152

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1627 files in 30 communities and 14 themes. Highest-impact communities: modules: lazyc2 (7.0), modules: lazyown (5.7), skills/mcp_tools (5.4). God nodes: skills/mcp_tools/_context.py, modules/lazy_loop.py, core/logging.py, modules/__init__.py, utils.py.

- [modules: lazyc2] rating 7.0: `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyown] rating 5.7: `core/config.py` ranks 1 by PageRank, 153 importers, 20 symbols: Configuration loader and Config wrapper.
- [skills/mcp_tools] rating 5.4: `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [cli/commands] rating 5.1: `modules/__init__.py` ranks 1 by PageRank, 320 importers, 0 symbols.
- [modules: lazy_loop] rating 4.8: `modules/lazy_loop.py` ranks 1 by PageRank, 324 importers, 481 symbols: Lazy autonomous loop for LazyOwn.
- [cli] rating 4.7: `core/validators.py` ranks 1 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [unassigned files] rating 3.4: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: world_model] rating 3.3: `modules/world_model.py` ranks 1 by PageRank, 156 importers, 70 symbols: modules/world_model.py
- Key entities: file:lazyc2.py, file:core/logging.py, file:lazyown.py, file:tests/test_security_hardening_v4.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13
- Root rating = highest community rating.

## modules: lazyc2 + skills/mcp_tools +7 (`t0`, theme, rating 7.0)

Theme of 9 communities and 776 files: modules: lazyc2 (135 files, rating 7.0); skills/mcp_tools (206 files, rating 5.4); cli (123 files, rating 4.7); modules: world_model (99 files, rating 3.3); modules: llm_budget (43 files, rating 1.8); modules: bof_registry (43 files, rating 1.8); static/js (43 files, rating 1.7); lazygui/panels (54 files, rating 1.5); skills/claude_md_orchestrator (30 files, rating 0.9).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [skills/mcp_tools] `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [skills/mcp_tools] `skills/autonomous_daemon.py` ranks 2 by PageRank, 117 importers, 142 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [cli] `core/validators.py` ranks 1 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [cli] `core/console.py` ranks 2 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: world_model] `modules/world_model.py` ranks 1 by PageRank, 156 importers, 70 symbols: modules/world_model.py
- [modules: world_model] `modules/killchain.py` ranks 2 by PageRank, 37 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- Key entities: file:lazyc2.py, file:core/logging.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:modules/world_model.py, file:cli/ops_commands.py
- Children: c4, c0, c5, c6, c10, c11, c9, c8, c13
- Theme rating = highest child community rating.

## modules: lazyown + modules: lazy_loop +3 (`t1`, theme, rating 5.7)

Theme of 5 communities and 413 files: modules: lazyown (139 files, rating 5.7); modules: lazy_loop (166 files, rating 4.8); modules: lazyown_facts (63 files, rating 1.7); modules/selection (37 files, rating 0.9); modules: defense_eval (8 files, rating 0.2).

- [modules: lazyown] `core/config.py` ranks 1 by PageRank, 153 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazyown] `core/hardening.py` ranks 2 by PageRank, 102 importers, 34 symbols: Centralized security hardening utilities for the LazyOwn framework.
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 324 importers, 481 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/auto_registry.py` ranks 2 by PageRank, 72 importers, 45 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- [modules: lazyown_facts] `modules/chain_registry.py` ranks 1 by PageRank, 77 importers, 21 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- [modules: lazyown_facts] `skills/lazyown_facts.py` ranks 2 by PageRank, 15 importers, 79 symbols: LazyOwn FactStore
- [modules/selection] `modules/selection/base.py` ranks 1 by PageRank, 33 importers, 4 symbols: The one shared contract for autonomous action selection.
- [modules/selection] `modules/selection/module.py` ranks 2 by PageRank, 5 importers, 2 symbols: Module selector: map goal/service mentions onto runnable registry modules.
- Key entities: file:lazyown.py, file:tests/test_security_hardening_v4.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:skills/lazyown_facts.py, file:modules/chain_runner.py, file:modules/rootkit/rootkit.c, file:tests/test_poc_registry.py
- Children: c3, c1, c7, c12, c14
- Theme rating = highest child community rating.

## cli/commands + contrib/legacy +3 (`t3`, theme, rating 5.1)

Theme of 5 communities and 164 files: cli/commands (139 files, rating 5.1); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `modules/__init__.py` ranks 1 by PageRank, 320 importers, 0 symbols.
- [cli/commands] `utils.py` ranks 2 by PageRank, 146 importers, 127 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c2, c18, c15, c16, c17
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 3.4)

Theme of 1 communities and 250 files: unassigned files (250 files, rating 3.4).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c29
- Theme rating = highest child community rating.

## tests (`t4`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c19
- Theme rating = highest child community rating.

## modules: memory_store (`t5`, theme, rating 0.1)

Theme of 1 communities and 3 files: modules: memory_store (3 files, rating 0.1).

- [modules: memory_store] `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- [modules: memory_store] `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py
- Children: c20
- Theme rating = highest child community rating.

## scripts: journal (`t6`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c21
- Theme rating = highest child community rating.

## poc_tui (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c25
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t11`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c26
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t12`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c27
- Theme rating = highest child community rating.

## tools (`t13`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c28
- Theme rating = highest child community rating.

## modules/backdoor (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c22
- Theme rating = highest child community rating.

## modules: lazy_netattack (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_netattack (2 files, rating 0.0).

- [modules: lazy_netattack] `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- [modules: lazy_netattack] `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py
- Children: c23
- Theme rating = highest child community rating.

## modules: lazy_triage (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_triage (2 files, rating 0.0).

- [modules: lazy_triage] `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- [modules: lazy_triage] `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py
- Children: c24
- Theme rating = highest child community rating.

## modules: lazyc2 (`c4`, community, rating 7.0)

135 files under tests (py 132, js 3), mostly utility. Core file core/logging.py (PageRank 0.0696, imported by 206 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on skills/mcp_tools (33), modules: lazyown (33), modules: world_model (33). Used by modules: lazyown (48), skills/mcp_tools (43), modules: world_model (30).

- `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `modules/logging_config.py` ranks 3 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `lazyc2.py`: 325 symbols, 336 connections (score 0.20).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 59 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:core/logging.py, file:tests/test_collab_and_onboarding.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_security_lazyc2.py, file:tests/test_moe_rl_swan.py, file:modules/collab_bp.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 394.

## modules: lazyown (`c3`, community, rating 5.7)

139 files under tests (py 138, js 1), mostly utility. Core file core/config.py (PageRank 0.0169, imported by 153 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (80), modules: lazy_loop (77), cli (53). Used by modules: lazy_loop (109), cli/commands (53), static/js (34).

- `core/config.py` ranks 1 by PageRank, 153 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/hardening.py` ranks 2 by PageRank, 102 importers, 34 symbols: Centralized security hardening utilities for the LazyOwn framework.
- `core/safe_exec.py` ranks 3 by PageRank, 67 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- Hotspot `lazyown.py`: 125 symbols, 214 connections (score 0.08).
- Hotspot `cli/orchestrator_assets_tabs.py`: 84 symbols, 139 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:lazyown.py, file:tests/test_security_hardening_v4.py, file:core/config.py, file:tests/test_winbox_gym.py, file:tests/test_cli_command_sets.py, file:tests/test_guardrails.py, file:cli/cli_enhancements.py, file:tests/test_security_hardening_v3.py
- Rating 5.7/10 = 7 x PageRank share 0.81 + 3 x risk 0.00. Internal imports: 577.

## skills/mcp_tools (`c0`, community, rating 5.4)

206 files under skills/mcp_tools (py 206), mostly utility. Core file skills/mcp_tools/_context.py (PageRank 0.0261, imported by 190 files): Dependency-injection context handed to every ``mcp_tools`` handler. Key abstractions: MCPContext, ICommandRunner, MCPCommandRunner, PTYCommandRunner, CommandRunnerChain, ICommandSelector. Depends on modules: lazyc2 (43), modules: world_model (27), cli/commands (19). Used by modules: lazyc2 (33), modules: lazy_loop (25), cli (22).

- `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 117 importers, 142 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `skills/hive_mind.py` ranks 3 by PageRank, 57 importers, 107 symbols: skills/hive_mind.py — LazyOwn Borg Hive Mind
- Hotspot `skills/autonomous_daemon.py`: 142 symbols, 293 connections (score 0.10).
- Hotspot `skills/lazyown_policy.py`: 126 symbols, 58 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> reactive_engine.py -> config.py.
- 2 layer violations, e.g. test_core_modules.py (testing) -> dashboard_bp.py (presentation).
- Surprising bridge: kerberos_core.py <-> lazy_opencode_config.py (9 hops across communities).
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:skills/mcp_tools/_context.py, file:skills/lazyown_mcp.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:skills/tests/test_hive_mind.py
- Rating 5.4/10 = 7 x PageRank share 0.77 + 3 x risk 0.00. Internal imports: 640.

## cli/commands (`c2`, community, rating 5.1)

139 files under cli/commands (py 139), mostly utility. Core file modules/__init__.py (PageRank 0.0228, imported by 320 files). Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, resolve_alias. Depends on modules: lazyown (53), modules: lazy_loop (19), cli (16). Used by modules: lazy_loop (135), modules: lazyown (80), cli (42).

- `modules/__init__.py` ranks 1 by PageRank, 320 importers, 0 symbols.
- `utils.py` ranks 2 by PageRank, 146 importers, 127 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `cli/commands/_base.py` ranks 3 by PageRank, 116 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 127 symbols, 237 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: utils.py -> config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> utils.py.
- Taint: 3 paths reach this group via subprocess.
- Dataflow: 9 INFERRED issues (first: UNCHECKED_ALLOC in image_to_bash).
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/__init__.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_categories.py, file:cli/commands/_base.py, file:cli/fuzzy_picker.py, file:tests/test_infra_disposable.py
- Rating 5.1/10 = 7 x PageRank share 0.73 + 3 x risk 0.00. Internal imports: 349.

## modules: lazy_loop (`c1`, community, rating 4.8)

166 files under tests (py 166), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0150, imported by 324 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on cli/commands (135), modules: lazyown (109), modules: world_model (47). Used by modules: lazyown (77), modules: llm_budget (36), modules/selection (21).

- `modules/lazy_loop.py` ranks 1 by PageRank, 324 importers, 481 symbols: Lazy autonomous loop for LazyOwn.
- `modules/auto_registry.py` ranks 2 by PageRank, 72 importers, 45 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- `modules/lazy_engine.py` ranks 3 by PageRank, 144 importers, 1 symbols: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Hotspot `modules/lazy_loop.py`: 481 symbols, 654 connections (score 0.31).
- Hotspot `tests/test_lazy_runner.py`: 145 symbols, 274 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 2 layer violations, e.g. test_orchestrator_api.py (testing) -> api_authz.py (presentation).
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in file_lock).
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1440, sym:modules/lazy_loop.py::ExplorationGraph@1543, sym:modules/lazy_loop.py::ActivityLog@1958, file:modules/lazy_proxy.py, file:modules/lazy_runner.py
- Rating 4.8/10 = 7 x PageRank share 0.68 + 3 x risk 0.00. Internal imports: 763.

## cli (`c5`, community, rating 4.7)

123 files under tests (py 123), mostly utility. Core file core/validators.py (PageRank 0.0134, imported by 19 files): Input validators for runtime configuration values. Key abstractions: check_rhost, check_lhost, check_lport, check_port, require_rhost, require_lhost. Depends on modules: world_model (51), cli/commands (42), modules: lazyown (32). Used by modules: lazyown (53), cli/commands (16), modules: lazy_loop (14).

- `core/validators.py` ranks 1 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `core/console.py` ranks 2 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `core/host_policy.py` ranks 3 by PageRank, 7 importers, 5 symbols: Single source of truth for host and network shape validation.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 161 symbols, 48 connections (score 0.09).
- 5 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in do_suggest_next).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py, file:cli/status_bar.py
- Rating 4.7/10 = 7 x PageRank share 0.67 + 3 x risk 0.00. Internal imports: 400.

## unassigned files (`c29`, community, rating 3.4)

250 files under modules (py 141, sh 63, lua 26, c 10, js 4, php 3, asm 1, cpp 1, cs 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0003, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `tests/test_attack_surface_addons.py`: 76 symbols, 5 connections (score 0.04).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_blacksandbeacon_addon.py, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.4/10 = 7 x PageRank share 0.48 + 3 x risk 0.00. Internal imports: 0.

## modules: world_model (`c6`, community, rating 3.3)

99 files under modules (py 99), mostly utility. Core file modules/world_model.py (PageRank 0.0140, imported by 156 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: lazyc2 (30), cli/commands (23), skills/mcp_tools (16). Used by cli (51), modules: lazy_loop (47), modules: lazyc2 (33).

- `modules/world_model.py` ranks 1 by PageRank, 156 importers, 70 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 37 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/lazy_heat.py` ranks 3 by PageRank, 12 importers, 15 symbols: Heat tiers and version math for CVE correlation.
- Hotspot `modules/world_model.py`: 70 symbols, 185 connections (score 0.05).
- Hotspot `cli/ops_commands.py`: 54 symbols, 75 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _emit_event).
- Key entities: file:modules/world_model.py, file:cli/ops_commands.py, file:cli/exploration.py, file:modules/obs_parser.py, file:modules/estorides_importer.py, file:tests/test_killchain_unified_v2.py, file:modules/playbook_engine.py, file:modules/killchain.py
- Rating 3.3/10 = 7 x PageRank share 0.48 + 3 x risk 0.00. Internal imports: 228.

## modules: llm_budget (`c10`, community, rating 1.8)

43 files under modules (py 43), mostly utility. Core file modules/llm_factory.py (PageRank 0.0095, imported by 66 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazy_loop (36), modules: lazyc2 (26), modules: lazyown (14). Used by modules: lazy_loop (47), skills/mcp_tools (10), cli (5).

- `modules/llm_factory.py` ranks 1 by PageRank, 66 importers, 31 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 11 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `tests/test_llm_orchestrator.py`: 89 symbols, 56 connections (score 0.05).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:tests/test_llm_adapter_parity.py, file:core/llm_budget.py, file:modules/lazy_agent.py, file:telegram_hermes.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 138.

## modules: bof_registry (`c11`, community, rating 1.8)

43 files under modules (py 43), mostly utility. Core file cli/commands/enum.py (PageRank 0.0184, imported by 26 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyown (17), modules: lazyc2 (12), cli/commands (8). Used by modules: lazyown (20), cli/commands (12), modules: lazyc2 (10).

- `cli/commands/enum.py` ranks 1 by PageRank, 26 importers, 11 symbols: Enumeration command set.
- `modules/opsec_scorer.py` ranks 2 by PageRank, 7 importers, 36 symbols: OPSEC scoring engine — pre-execution noise assessment and gated scoring.
- `modules/guardrails/contracts.py` ranks 3 by PageRank, 3 importers, 10 symbols: Contracts for the execution guardrail harness.
- Hotspot `tests/test_c2_profile_engine.py`: 63 symbols, 4 connections (score 0.03).
- Hotspot `modules/bof_registry.py`: 51 symbols, 27 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> opsec_scorer.py -> config.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_c2_profile_engine.py, file:modules/bof_registry.py, file:tests/test_bof_registry.py, file:modules/c2_profile_engine.py, file:tests/test_socks_proxy.py, file:tests/test_scope_guard.py, file:modules/bof_delivery.py, file:tests/test_sleep_obfuscation.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 92.

## modules: lazyown_facts (`c7`, community, rating 1.7)

63 files under tests (py 63), mostly testing. Core file modules/chain_registry.py (PageRank 0.0053, imported by 77 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, skip_pending, identifier, resolve, render_text. Depends on modules: lazyown (29), cli/commands (19), modules: lazy_loop (15). Used by modules: lazyown (30), modules: lazy_loop (11), modules/selection (10).

- `modules/chain_registry.py` ranks 1 by PageRank, 77 importers, 21 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `skills/lazyown_facts.py` ranks 2 by PageRank, 15 importers, 79 symbols: LazyOwn FactStore
- `modules/chain_runner.py` ranks 3 by PageRank, 23 importers, 49 symbols: Single execution engine for YAML orchestration chains.
- Hotspot `skills/lazyown_facts.py`: 79 symbols, 27 connections (score 0.04).
- Hotspot `modules/chain_runner.py`: 49 symbols, 69 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> chain_loop.py -> config.py.
- Key entities: file:skills/lazyown_facts.py, file:modules/chain_runner.py, sym:modules/chain_registry.py::ChainStep@104, file:modules/chain_registry.py, sym:modules/chain_runner.py::ChainRunner@231, file:cli/commands/command_and_control_migrated.py, file:tests/test_chain_runner.py, file:cli/apt_chain_support.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 200.

## static/js (`c9`, community, rating 1.7)

43 files under static/js (py 25, js 15, c 1, php 1, sh 1), mostly utility. Core file core/payload_schema.py (PageRank 0.0125, imported by 22 files): Declarative schema and validation for ``payload.json``. Key abstractions: FieldKind, Severity, FieldSpec, ValidationIssue, register_specs, unregister_specs. Depends on modules: lazyown (34), modules: world_model (18), skills/mcp_tools (12). Used by modules: lazyown (17), cli (10), modules: lazyc2 (3).

- `core/payload_schema.py` ranks 1 by PageRank, 22 importers, 33 symbols: Declarative schema and validation for ``payload.json``.
- `core/param_registry.py` ranks 2 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- `cli/assign.py` ranks 3 by PageRank, 131 importers, 1 symbols: ``assign`` business logic.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- Taint: 2 paths reach this group via subprocess.
- Dataflow: 6 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:tests/test_param_registry.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 290.

## lazygui/panels (`c8`, community, rating 1.5)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0047, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (7), modules: world_model (2), modules: bof_registry (2). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.5/10 = 7 x PageRank share 0.21 + 3 x risk 0.00. Internal imports: 181.

## modules/selection (`c12`, community, rating 0.9)

37 files under modules/selection (py 34, c 2, js 1), mostly utility. Core file modules/selection/base.py (PageRank 0.0043, imported by 33 files): The one shared contract for autonomous action selection. Key abstractions: SelectionContext, ActionDecision, Selector, propose, ModuleSelector, propose. Depends on modules: lazy_loop (21), cli/commands (10), modules: lazyown_facts (10). Used by skills/mcp_tools (4), modules: lazy_loop (3), static/js (1).

- `modules/selection/base.py` ranks 1 by PageRank, 33 importers, 4 symbols: The one shared contract for autonomous action selection.
- `modules/selection/module.py` ranks 2 by PageRank, 5 importers, 2 symbols: Module selector: map goal/service mentions onto runnable registry modules.
- `modules/selection/parquet.py` ranks 3 by PageRank, 6 importers, 4 symbols: Parquet selector: propose the command that most often succeeded before.
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 973 connections (score 0.08).
- Hotspot `tests/test_poc_registry.py`: 29 symbols, 23 connections (score 0.02).
- Dependency cycle: lazyown_parquet_db.py -> parquet.py -> lazyown_parquet_db.py.
- Key entities: file:modules/rootkit/rootkit.c, file:tests/test_poc_registry.py, file:modules/selection/base.py, file:tests/test_selection_technique.py, file:modules/selection/registry.py, file:tests/test_loop_fire_pending.py, sym:modules/selection/base.py::SelectionContext@20, file:tests/test_selection_technique_chain.py
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 94.

## skills/claude_md_orchestrator (`c13`, community, rating 0.9)

30 files under skills/claude_md_orchestrator (py 29, c 1), mostly utility. Core file modules/backdoor/server.c (PageRank 0.0028, imported by 16 files). Key abstractions: main, Stage, Severity, Contract, SadPath, Spec. Depends on cli/commands (4), modules: lazyown (1), modules: world_model (1). Used by modules: lazy_loop (5), cli/commands (4), modules: lazyc2 (3).

- `modules/backdoor/server.c` ranks 1 by PageRank, 16 importers, 1 symbols.
- `skills/claude_md_orchestrator/models.py` ranks 2 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 3 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- Hotspot `modules/browser_sync.py`: 44 symbols, 20 connections (score 0.03).
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in main).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:modules/browser_sync.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/claude_md_orchestrator/validators.py, file:skills/hermes-lazyown/output_compactor.py
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 56.

## modules: defense_eval (`c14`, community, rating 0.2)

8 files under modules (py 8), mostly testing. Core file modules/defense_eval.py (PageRank 0.0012, imported by 4 files): Detection rule replay over recorded attack and control logs. Key abstractions: RuleEvaluationError, Condition, Evaluation, DatasetSummary, RuleResult, to_dict. Depends on cli/commands (1), modules: lazyown (1), modules: lazyc2 (1). Used by modules: lazy_loop (3), modules: lazyown_facts (1).

- `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- `modules/defense_stages.py` ranks 3 by PageRank, 4 importers, 11 symbols: Orchestrator stage runners for defense validation and hunt verification.
- Hotspot `modules/defense_eval.py`: 17 symbols, 9 connections (score 0.01).
- Hotspot `modules/hunt_verify.py`: 16 symbols, 6 connections (score 0.01).
- Key entities: file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/defense_stages.py, sym:modules/defense_eval.py::evaluate_rule@322, file:tests/test_defense_eval.py, file:tests/test_hunt_verify.py, file:modules/closedloop.py, sym:modules/hunt_verify.py::verify_stages@232
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## contrib/legacy (`c18`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0023, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::caesar_cipher@13
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
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c17`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0003, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## tests (`c19`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0009, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, sym:tests/mutation_common.py::run_all@56, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## modules: memory_store (`c20`, community, rating 0.1)

3 files under modules (py 3), mostly data_access. Core file modules/memory_embeddings.py (PageRank 0.0007, imported by 2 files): Hashing-trick text embeddings for episodic memory recall. Key abstractions: EmbeddingError, embed, cosine, semantic_top_k, as_floats, MemoryEntry.

- `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- `tests/test_memory_semantics.py` ranks 3 by PageRank, 0 importers, 14 symbols: BDD tests for hashing embeddings and hybrid episodic recall.
- Hotspot `modules/memory_store.py`: 38 symbols, 13 connections (score 0.02).
- Hotspot `tests/test_memory_semantics.py`: 14 symbols, 8 connections (score 0.01).
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py, file:modules/memory_embeddings.py, sym:modules/memory_embeddings.py::embed@50, sym:modules/memory_store.py::get_memory_store@339, sym:modules/memory_store.py::_cli@381, sym:modules/memory_store.py::VectorSQLiteBackend@315, sym:tests/test_memory_semantics.py::_entry@14
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c21`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0007, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c22`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0005, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_netattack (`c23`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_netattack.py (PageRank 0.0005, imported by 1 files): Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. Key abstractions: AttackVectorVerdict, SurfaceEvidence, as_dict, surface_decision, hint_text, TestIdentity.

- `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Hotspot `tests/test_lazy_netattack.py`: 17 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_netattack.py`: 12 symbols, 4 connections (score 0.01).
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py, sym:modules/lazy_netattack.py::surface_decision@184, sym:modules/lazy_netattack.py::SurfaceEvidence@120, sym:tests/test_lazy_netattack.py::test_hint_text_shapes@102, sym:tests/test_lazy_netattack.py::test_linux_host_blocked@56, sym:modules/lazy_netattack.py::hint_text@311, sym:tests/test_lazy_netattack.py::ad_domain_controller@35
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_triage (`c24`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_triage.py (PageRank 0.0005, imported by 1 files): Triage doctrine: evidence floors, verdict algebra and signature dedup. Key abstractions: SignatureStore, rank, hard_evidence, apply_rules, signature_for, fresh_signature.

- `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Hotspot `tests/test_lazy_triage.py`: 11 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_triage.py`: 10 symbols, 6 connections (score 0.01).
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py, sym:modules/lazy_triage.py::fresh_signature@144, sym:modules/lazy_triage.py::hard_evidence@47, sym:modules/lazy_triage.py::_save@176, sym:modules/lazy_triage.py::SignatureStore@135, sym:modules/lazy_triage.py::signature_for@108, sym:modules/lazy_triage.py::apply_rules@80
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c25`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0005, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c26`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0005, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c27`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0005, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c28`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0005, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
