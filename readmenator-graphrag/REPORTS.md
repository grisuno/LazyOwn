# GraphRAG Community Reports

Entities: 27260 | Relationships: 89348 | Communities: 28 | Themes: 13 | Text units: 27149

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1622 files in 28 communities and 13 themes. Highest-impact communities: modules: lazyc2 (7.0), cli/commands (6.3), skills/mcp_tools (5.6). God nodes: skills/mcp_tools/_context.py, modules/lazy_loop.py, core/logging.py, modules/__init__.py, utils.py.

- [modules: lazyc2] rating 7.0: `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 6.3: `modules/__init__.py` ranks 1 by PageRank, 318 importers, 0 symbols.
- [skills/mcp_tools] rating 5.6: `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [modules: lazyown] rating 4.9: `core/config.py` ranks 1 by PageRank, 145 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazy_loop] rating 3.9: `modules/lazy_loop.py` ranks 1 by PageRank, 320 importers, 478 symbols: Lazy autonomous loop for LazyOwn.
- [cli] rating 3.7: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 3.3: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: lazyown_facts] rating 2.7: `modules/chain_registry.py` ranks 1 by PageRank, 74 importers, 20 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- Key entities: file:lazyc2.py, file:skills/lazyown_policy.py, file:utils.py, file:cli/banner_config.py, file:skills/autonomous_daemon.py, file:skills/hive_mind.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12
- Root rating = highest community rating.

## modules: lazyc2 + skills/mcp_tools +11 (`t0`, theme, rating 7.0)

Theme of 13 communities and 1180 files: modules: lazyc2 (142 files, rating 7.0); skills/mcp_tools (222 files, rating 5.6); modules: lazyown (104 files, rating 4.9); modules: lazy_loop (138 files, rating 3.9); cli (129 files, rating 3.7); modules: lazyown_facts (101 files, rating 2.7); modules: autonomous_exploit_engine (93 files, rating 2.7); modules: world_model (65 files, rating 2.4); modules: bof_registry (48 files, rating 1.9); modules: llm_budget (46 files, rating 1.9); lazygui/panels (54 files, rating 1.4); skills/claude_md_orchestrator (30 files, rating 0.9); modules: defense_eval (8 files, rating 0.2).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [skills/mcp_tools] `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- [skills/mcp_tools] `skills/autonomous_daemon.py` ranks 2 by PageRank, 117 importers, 142 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [modules: lazyown] `core/config.py` ranks 1 by PageRank, 145 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazyown] `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 33 symbols: Declarative schema and validation for ``payload.json``.
- [modules: lazy_loop] `modules/lazy_loop.py` ranks 1 by PageRank, 320 importers, 478 symbols: Lazy autonomous loop for LazyOwn.
- [modules: lazy_loop] `modules/lazy_engine.py` ranks 2 by PageRank, 143 importers, 1 symbols: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Key entities: file:lazyc2.py, file:skills/lazyown_policy.py, file:skills/autonomous_daemon.py, file:skills/hive_mind.py, file:lazyown.py, file:tests/test_winbox_gym.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: c2, c0, c5, c3, c4, c6, c7, c8, c10, c11, c9, c12, c13
- Theme rating = highest child community rating.

## cli/commands + modules: kerberos_core +2 (`t2`, theme, rating 6.3)

Theme of 4 communities and 168 files: cli/commands (148 files, rating 6.3); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `modules/__init__.py` ranks 1 by PageRank, 318 importers, 0 symbols.
- [cli/commands] `utils.py` ranks 2 by PageRank, 145 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- [modules: polymorphic_engine] `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- [modules: polymorphic_engine] `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py
- Children: c1, c14, c15, c16
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.3)

Theme of 1 communities and 250 files: unassigned files (250 files, rating 3.3).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c27
- Theme rating = highest child community rating.

## tests (`t3`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c17
- Theme rating = highest child community rating.

## modules: memory_store (`t4`, theme, rating 0.1)

Theme of 1 communities and 3 files: modules: memory_store (3 files, rating 0.1).

- [modules: memory_store] `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- [modules: memory_store] `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py
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
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py
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

## modules: lazyc2 (`c2`, community, rating 7.0)

142 files under tests (py 139, js 3), mostly utility. Core file core/logging.py (PageRank 0.0697, imported by 206 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on skills/mcp_tools (47), modules: lazyown (33), modules: world_model (24). Used by skills/mcp_tools (51), modules: lazyown (36), modules: llm_budget (27).

- `core/logging.py` ranks 1 by PageRank, 206 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/lazy_rbac.py` ranks 2 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `modules/logging_config.py` ranks 3 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `lazyc2.py`: 325 symbols, 336 connections (score 0.20).
- Hotspot `skills/lazyown_policy.py`: 126 symbols, 58 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 36 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:skills/lazyown_policy.py, file:core/logging.py, file:tests/test_collab_and_onboarding.py, file:tests/test_engage_orchestrator.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_security_lazyc2.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 415.

## cli/commands (`c1`, community, rating 6.3)

148 files under cli/commands (py 148), mostly utility. Core file modules/__init__.py (PageRank 0.0226, imported by 318 files). Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on modules: lazyown (38), modules: lazyc2 (17), skills/mcp_tools (16). Used by modules: lazy_loop (116), modules: lazyown (88), cli (51).

- `modules/__init__.py` ranks 1 by PageRank, 318 importers, 0 symbols.
- `utils.py` ranks 2 by PageRank, 145 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 3 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- Hotspot `utils.py`: 126 symbols, 236 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: utils.py -> config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> utils.py.
- Taint: 4 paths reach this group via subprocess.
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in image_to_bash).
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/__init__.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_categories.py, file:cli/commands/_base.py, file:cli/fuzzy_picker.py, file:tests/test_infra_disposable.py
- Rating 6.3/10 = 7 x PageRank share 0.90 + 3 x risk 0.00. Internal imports: 360.

## skills/mcp_tools (`c0`, community, rating 5.6)

222 files under skills/mcp_tools (py 222), mostly utility. Core file skills/mcp_tools/_context.py (PageRank 0.0261, imported by 190 files): Dependency-injection context handed to every ``mcp_tools`` handler. Key abstractions: MCPContext, ICommandRunner, MCPCommandRunner, PTYCommandRunner, CommandRunnerChain, ICommandSelector. Depends on modules: lazyc2 (51), cli/commands (20), modules: world_model (15). Used by modules: lazyc2 (47), modules: lazy_loop (22), cli (22).

- `skills/mcp_tools/_context.py` ranks 1 by PageRank, 190 importers, 1 symbols: Dependency-injection context handed to every ``mcp_tools`` handler.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 117 importers, 142 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `skills/hive_mind.py` ranks 3 by PageRank, 57 importers, 107 symbols: skills/hive_mind.py — LazyOwn Borg Hive Mind
- Hotspot `skills/autonomous_daemon.py`: 142 symbols, 293 connections (score 0.10).
- Hotspot `skills/hive_mind.py`: 107 symbols, 88 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> reactive_engine.py -> config.py.
- 2 layer violations, e.g. test_core_modules.py (testing) -> dashboard_bp.py (presentation).
- Surprising bridge: kerberos_core.py <-> lazy_opencode_config.py (9 hops across communities).
- Key entities: file:skills/autonomous_daemon.py, file:skills/hive_mind.py, file:skills/mcp_tools/_context.py, file:skills/lazyown_mcp.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:skills/tests/test_hive_mind.py, file:modules/pipeline_engine.py
- Rating 5.6/10 = 7 x PageRank share 0.80 + 3 x risk 0.00. Internal imports: 691.

## modules: lazyown (`c5`, community, rating 4.9)

104 files under tests (py 104), mostly utility. Core file core/config.py (PageRank 0.0166, imported by 145 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli/commands (88), modules: lazy_loop (64), cli (53). Used by modules: lazy_loop (73), cli/commands (38), cli (36).

- `core/config.py` ranks 1 by PageRank, 145 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 33 symbols: Declarative schema and validation for ``payload.json``.
- `core/hardening.py` ranks 3 by PageRank, 102 importers, 34 symbols: Centralized security hardening utilities for the LazyOwn framework.
- Hotspot `lazyown.py`: 125 symbols, 213 connections (score 0.08).
- Hotspot `cli/orchestrator_assets_tabs.py`: 84 symbols, 139 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 25 layer violations, e.g. test_api_authz.py (testing) -> api_authz.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:lazyown.py, file:tests/test_winbox_gym.py, file:core/config.py, file:tests/test_cli_command_sets.py, file:tests/test_guardrails.py, file:cli/cli_enhancements.py, file:tests/test_security_hardening_v3.py, file:cli/orchestrator_assets_tabs.py
- Rating 4.9/10 = 7 x PageRank share 0.70 + 3 x risk 0.00. Internal imports: 508.

## modules: lazy_loop (`c3`, community, rating 3.9)

138 files under tests (py 138), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0152, imported by 320 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on cli/commands (116), modules: lazyown (73), modules: lazyown_facts (49). Used by modules: lazyown (64), modules: llm_budget (31), modules: lazyown_facts (25).

- `modules/lazy_loop.py` ranks 1 by PageRank, 320 importers, 478 symbols: Lazy autonomous loop for LazyOwn.
- `modules/lazy_engine.py` ranks 2 by PageRank, 143 importers, 1 symbols: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- `modules/lazy_cli_bridge.py` ranks 3 by PageRank, 18 importers, 15 symbols: Full CLI catalog for the Lazy autonomous loop.
- Hotspot `modules/lazy_loop.py`: 478 symbols, 662 connections (score 0.31).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 266 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in file_lock).
- Surprising bridge: kerberos_core.py <-> selector_manager.py (9 hops across communities).
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1324, sym:modules/lazy_loop.py::ExplorationGraph@1432, sym:modules/lazy_loop.py::ActivityLog@1885, file:modules/lazy_proxy.py, file:modules/lazy_runner.py
- Rating 3.9/10 = 7 x PageRank share 0.56 + 3 x risk 0.00. Internal imports: 621.

## cli (`c4`, community, rating 3.7)

129 files under tests (py 110, js 16, c 1, php 1, sh 1), mostly utility. Core file core/console.py (PageRank 0.0131, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: world_model (63), cli/commands (51), modules: lazyown (36). Used by modules: lazyown (53), skills/mcp_tools (12), modules: lazy_loop (12).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `cli/themes.py` ranks 2 by PageRank, 18 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `core/safe_subprocess.py` ranks 3 by PageRank, 6 importers, 7 symbols: Safe subprocess runner for the LazyOwn framework.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- 5 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in do_suggest_next).
- Key entities: file:static/js/html2pdf.bundle.min.js, sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:static/js/3d-force-graph-1.73.4.min.js, file:tests/test_improvements_spec.py, file:static/js/vis-network-9.1.2.min.js
- Rating 3.7/10 = 7 x PageRank share 0.52 + 3 x risk 0.00. Internal imports: 624.

## unassigned files (`c27`, community, rating 3.3)

250 files under modules (py 141, sh 63, lua 26, c 10, js 4, php 3, asm 1, cpp 1, cs 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0003, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `tests/test_attack_surface_addons.py`: 76 symbols, 5 connections (score 0.04).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_blacksandbeacon_addon.py, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.3/10 = 7 x PageRank share 0.47 + 3 x risk 0.00. Internal imports: 0.

## modules: lazyown_facts (`c6`, community, rating 2.7)

101 files under tests (py 98, c 2, js 1), mostly utility. Core file modules/chain_registry.py (PageRank 0.0052, imported by 74 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, skip_pending, identifier, resolve, evaluate_when. Depends on cli/commands (32), modules: lazy_loop (25), modules: autonomous_exploit_engine (24). Used by modules: lazy_loop (49), modules: lazyown (20), skills/mcp_tools (13).

- `modules/chain_registry.py` ranks 1 by PageRank, 74 importers, 20 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `modules/selection/base.py` ranks 2 by PageRank, 33 importers, 4 symbols: The one shared contract for autonomous action selection.
- `modules/auto_registry.py` ranks 3 by PageRank, 69 importers, 45 symbols: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 973 connections (score 0.08).
- Hotspot `skills/lazyown_facts.py`: 79 symbols, 27 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- Key entities: file:skills/lazyown_facts.py, file:modules/chain_runner.py, file:modules/auto_registry.py, file:modules/rootkit/rootkit.c, sym:modules/chain_registry.py::ChainStep@104, file:modules/chain_registry.py, file:cli/commands/command_and_control_migrated.py, sym:modules/chain_runner.py::ChainRunner@235
- Rating 2.7/10 = 7 x PageRank share 0.38 + 3 x risk 0.00. Internal imports: 322.

## modules: autonomous_exploit_engine (`c7`, community, rating 2.7)

93 files under modules (py 93), mostly utility. Core file core/safe_exec.py (PageRank 0.0073, imported by 67 files): Centralized safe command execution for the LazyOwn framework. Key abstractions: CommandInjectionError, UrlValidationError, needs_shell, safe_system, safe_run_argv, safe_run_shell. Depends on cli/commands (26), modules: lazy_loop (25), modules: world_model (20). Used by modules: lazy_loop (33), modules: lazyown_facts (24), modules: lazyc2 (16).

- `core/safe_exec.py` ranks 1 by PageRank, 67 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/outcome_bus.py` ranks 2 by PageRank, 46 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- `modules/lazy_heat.py` ranks 3 by PageRank, 12 importers, 15 symbols: Heat tiers and version math for CVE correlation.
- Hotspot `tests/test_security_hardening_v4.py`: 67 symbols, 67 connections (score 0.04).
- Hotspot `modules/autonomous_exploit_engine.py`: 46 symbols, 65 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_security_hardening_v4.py, file:modules/atomic_exploit_bridge.py, file:modules/autonomous_exploit_engine.py, file:modules/outcome_bus.py, file:modules/winbox_gym.py, file:modules/intel_fusion.py, file:tests/test_atomic_exploit_bridge.py, file:core/safe_exec.py
- Rating 2.7/10 = 7 x PageRank share 0.39 + 3 x risk 0.00. Internal imports: 231.

## modules: world_model (`c8`, community, rating 2.4)

65 files under tests (py 65), mostly utility. Core file modules/world_model.py (PageRank 0.0143, imported by 157 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: lazyc2 (24), skills/mcp_tools (16), modules: autonomous_exploit_engine (11). Used by cli (63), modules: lazyown (25), modules: lazyc2 (24).

- `modules/world_model.py` ranks 1 by PageRank, 157 importers, 70 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 38 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/factsio.py` ranks 3 by PageRank, 4 importers, 7 symbols: Canonical reader for the FactStore ``policy_facts.json`` document.
- Hotspot `modules/world_model.py`: 70 symbols, 186 connections (score 0.05).
- Hotspot `cli/dashboard_tui.py`: 64 symbols, 53 connections (score 0.04).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in _emit_event).
- Key entities: file:modules/world_model.py, file:cli/dashboard_tui.py, file:cli/ops_commands.py, file:tests/test_phase1_data_gaps.py, file:cli/exploration.py, file:cli/recommendation_signals.py, file:modules/estorides_importer.py, file:tests/test_killchain_unified_v2.py
- Rating 2.4/10 = 7 x PageRank share 0.34 + 3 x risk 0.00. Internal imports: 172.

## modules: bof_registry (`c10`, community, rating 1.9)

48 files under modules (py 48), mostly utility. Core file cli/commands/enum.py (PageRank 0.0184, imported by 26 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyc2 (12), cli/commands (11), modules: lazyown (11). Used by modules: lazyown (21), cli/commands (11), modules: lazyc2 (11).

- `cli/commands/enum.py` ranks 1 by PageRank, 26 importers, 11 symbols: Enumeration command set.
- `modules/failure_verdict.py` ranks 2 by PageRank, 7 importers, 8 symbols: Failure verdict contract: classify one failed execution into an action.
- `modules/opsec_scorer.py` ranks 3 by PageRank, 7 importers, 36 symbols: OPSEC scoring engine — pre-execution noise assessment and gated scoring.
- Hotspot `tests/test_c2_profile_engine.py`: 63 symbols, 4 connections (score 0.03).
- Hotspot `modules/bof_registry.py`: 51 symbols, 27 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> opsec_scorer.py -> config.py.
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_c2_profile_engine.py, file:modules/bof_registry.py, file:tests/test_bof_registry.py, file:modules/c2_profile_engine.py, file:tests/test_socks_proxy.py, file:tests/test_scope_guard.py, file:modules/bof_delivery.py, file:tests/test_sleep_obfuscation.py
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 100.

## modules: llm_budget (`c11`, community, rating 1.9)

46 files under modules (py 46), mostly utility. Core file modules/llm_factory.py (PageRank 0.0096, imported by 66 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazy_loop (31), modules: lazyc2 (27), modules: lazyown (14). Used by modules: lazy_loop (41), skills/mcp_tools (6), modules: lazyown (5).

- `modules/llm_factory.py` ranks 1 by PageRank, 66 importers, 31 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 11 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `tests/test_llm_orchestrator.py`: 89 symbols, 56 connections (score 0.05).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> __init__.py -> worker_agentic.py -> lazy_agent.py -> loop_ai_bridge.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> engine_mediator.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:tests/test_llm_adapter_parity.py, file:core/llm_budget.py, file:tests/test_dependencies.py, file:modules/lazy_agent.py
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 135.

## lazygui/panels (`c9`, community, rating 1.4)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0047, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (7), modules: world_model (2), modules: bof_registry (2). Used by cli (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.4/10 = 7 x PageRank share 0.21 + 3 x risk 0.00. Internal imports: 181.

## skills/claude_md_orchestrator (`c12`, community, rating 0.9)

30 files under skills/claude_md_orchestrator (py 29, c 1), mostly utility. Core file modules/backdoor/server.c (PageRank 0.0028, imported by 16 files). Key abstractions: main, Stage, Severity, Contract, SadPath, Spec. Depends on cli/commands (4), modules: lazyown (1), modules: world_model (1). Used by modules: lazy_loop (5), cli/commands (4), modules: lazyc2 (3).

- `modules/backdoor/server.c` ranks 1 by PageRank, 16 importers, 1 symbols.
- `skills/claude_md_orchestrator/models.py` ranks 2 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 3 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- Hotspot `modules/browser_sync.py`: 44 symbols, 20 connections (score 0.03).
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in main).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:modules/browser_sync.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/claude_md_orchestrator/validators.py, file:skills/hermes-lazyown/output_compactor.py
- Rating 0.9/10 = 7 x PageRank share 0.12 + 3 x risk 0.00. Internal imports: 56.

## modules: defense_eval (`c13`, community, rating 0.2)

8 files under modules (py 8), mostly testing. Core file modules/defense_eval.py (PageRank 0.0012, imported by 4 files): Detection rule replay over recorded attack and control logs. Key abstractions: RuleEvaluationError, Condition, Evaluation, DatasetSummary, RuleResult, to_dict. Depends on cli/commands (1), modules: lazyc2 (1), modules: lazyown (1). Used by modules: lazy_loop (3), modules: lazyown_facts (1).

- `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- `modules/closedloop.py` ranks 3 by PageRank, 2 importers, 7 symbols: Closed-loop detection rule tuning: baseline vs candidate comparison.
- Hotspot `modules/defense_eval.py`: 17 symbols, 9 connections (score 0.01).
- Hotspot `modules/hunt_verify.py`: 16 symbols, 6 connections (score 0.01).
- Key entities: file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/defense_stages.py, sym:modules/defense_eval.py::evaluate_rule@322, file:tests/test_defense_eval.py, file:tests/test_hunt_verify.py, file:modules/closedloop.py, sym:modules/hunt_verify.py::verify_stages@232
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## modules: kerberos_core (`c14`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0008, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, sym:modules/kerberos_tickets.py::forge@134, file:cli/commands/active_directory.py
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c15`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0003, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/gcp_attacks.py, file:modules/k8s_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c16`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0003, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## tests (`c17`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0009, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, sym:tests/mutation_common.py::run_all@56, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## modules: memory_store (`c18`, community, rating 0.1)

3 files under modules (py 3), mostly data_access. Core file modules/memory_embeddings.py (PageRank 0.0007, imported by 2 files): Hashing-trick text embeddings for episodic memory recall. Key abstractions: EmbeddingError, embed, cosine, semantic_top_k, as_floats, MemoryEntry.

- `modules/memory_embeddings.py` ranks 1 by PageRank, 2 importers, 7 symbols: Hashing-trick text embeddings for episodic memory recall.
- `modules/memory_store.py` ranks 2 by PageRank, 1 importers, 38 symbols: — Episodic memory for the LazyOwn auto_loop.
- `tests/test_memory_semantics.py` ranks 3 by PageRank, 0 importers, 14 symbols: BDD tests for hashing embeddings and hybrid episodic recall.
- Hotspot `modules/memory_store.py`: 38 symbols, 13 connections (score 0.02).
- Hotspot `tests/test_memory_semantics.py`: 14 symbols, 8 connections (score 0.01).
- Key entities: file:modules/memory_store.py, file:tests/test_memory_semantics.py, file:modules/memory_embeddings.py, sym:modules/memory_embeddings.py::embed@50, sym:modules/memory_store.py::get_memory_store@339, sym:modules/memory_store.py::_cli@381, sym:modules/memory_store.py::VectorSQLiteBackend@315, sym:tests/test_memory_semantics.py::_entry@14
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c19`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0007, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c20`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0005, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_netattack (`c21`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_netattack.py (PageRank 0.0005, imported by 1 files): Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. Key abstractions: AttackVectorVerdict, SurfaceEvidence, as_dict, surface_decision, hint_text, TestIdentity.

- `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Hotspot `tests/test_lazy_netattack.py`: 17 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_netattack.py`: 12 symbols, 4 connections (score 0.01).
- Key entities: file:tests/test_lazy_netattack.py, file:modules/lazy_netattack.py, sym:modules/lazy_netattack.py::surface_decision@184, sym:modules/lazy_netattack.py::SurfaceEvidence@120, sym:tests/test_lazy_netattack.py::test_hint_text_shapes@102, sym:tests/test_lazy_netattack.py::test_linux_host_blocked@56, sym:modules/lazy_netattack.py::hint_text@311, sym:tests/test_lazy_netattack.py::ad_domain_controller@35
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_triage (`c22`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_triage.py (PageRank 0.0005, imported by 1 files): Triage doctrine: evidence floors, verdict algebra and signature dedup. Key abstractions: SignatureStore, rank, hard_evidence, apply_rules, signature_for, fresh_signature.

- `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Hotspot `tests/test_lazy_triage.py`: 11 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_triage.py`: 10 symbols, 6 connections (score 0.01).
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py, sym:modules/lazy_triage.py::fresh_signature@144, sym:modules/lazy_triage.py::hard_evidence@47, sym:modules/lazy_triage.py::_save@176, sym:modules/lazy_triage.py::SignatureStore@135, sym:modules/lazy_triage.py::signature_for@108, sym:modules/lazy_triage.py::apply_rules@80
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c23`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0005, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c24`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0005, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c25`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0005, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c26`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0005, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
