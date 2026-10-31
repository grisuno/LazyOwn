# GraphRAG Community Reports

Entities: 25187 | Relationships: 81201 | Communities: 29 | Themes: 14 | Text units: 25093

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1309 files in 29 communities and 14 themes. Highest-impact communities: cli/commands (7.0), modules: lazyown_mcp (6.7), modules: lazy_loop (6.5). God nodes: core/logging.py, modules/lazy_loop.py, utils.py, cli/commands/_base.py, modules/__init__.py.

- [cli/commands] rating 7.0: `utils.py` ranks 1 by PageRank, 140 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazyown_mcp] rating 6.7: `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazy_loop] rating 6.5: `modules/__init__.py` ranks 1 by PageRank, 228 importers, 0 symbols.
- [cli] rating 4.4: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 3.2: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [static/js] rating 2.4: `core/config.py` ranks 1 by PageRank, 113 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: chain_runner] rating 2.3: `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- [modules: llm_budget] rating 1.7: `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- Key entities: file:utils.py, file:cli/banner_config.py, file:skills/lazyown_mcp.py, file:tests/test_collab_and_onboarding.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13
- Root rating = highest community rating.

## cli/commands + contrib/legacy +3 (`t4`, theme, rating 7.0)

Theme of 5 communities and 183 files: cli/commands (158 files, rating 7.0); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 140 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c1, c18, c13, c14, c16
- Theme rating = highest child community rating.

## modules: lazyown_mcp + static/js +3 (`t0`, theme, rating 6.7)

Theme of 5 communities and 339 files: modules: lazyown_mcp (158 files, rating 6.7); static/js (49 files, rating 2.4); lazygui/panels (54 files, rating 1.5); lazyc2/security (55 files, rating 1.4); skills/claude_md_orchestrator (23 files, rating 0.7).

- [modules: lazyown_mcp] `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyown_mcp] `modules/logging_config.py` ranks 2 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- [static/js] `core/config.py` ranks 1 by PageRank, 113 importers, 20 symbols: Configuration loader and Config wrapper.
- [static/js] `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- [lazygui/panels] `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [lazygui/panels] `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- [lazyc2/security] `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [lazyc2/security] `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- Key entities: file:skills/lazyown_mcp.py, file:tests/test_collab_and_onboarding.py, file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:lazyc2.py, file:modules/lazy_rbac.py
- Children: c2, c7, c6, c5, c10
- Theme rating = highest child community rating.

## modules: lazy_loop + modules: chain_runner +3 (`t1`, theme, rating 6.5)

Theme of 5 communities and 320 files: modules: lazy_loop (184 files, rating 6.5); modules: chain_runner (81 files, rating 2.3); modules: llm_budget (41 files, rating 1.7); modules: defense_eval (8 files, rating 0.2); modules/guardrails (6 files, rating 0.2).

- [modules: lazy_loop] `modules/__init__.py` ranks 1 by PageRank, 228 importers, 0 symbols.
- [modules: lazy_loop] `modules/world_model.py` ranks 2 by PageRank, 157 importers, 70 symbols: modules/world_model.py
- [modules: chain_runner] `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- [modules: chain_runner] `modules/chain_registry.py` ranks 2 by PageRank, 63 importers, 19 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- [modules: llm_budget] `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- [modules: llm_budget] `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- [modules: defense_eval] `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- [modules: defense_eval] `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_security_hardening_v4.py, file:modules/chain_runner.py, file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/defense_eval.py, file:modules/hunt_verify.py
- Children: c0, c4, c9, c12, c17
- Theme rating = highest child community rating.

## cli + modules: autonomous_daemon +2 (`t3`, theme, rating 4.4)

Theme of 4 communities and 205 files: cli (138 files, rating 4.4); modules: autonomous_daemon (42 files, rating 1.2); modules: exploit_migrated (18 files, rating 0.4); skills/hermes-lazyown (7 files, rating 0.2).

- [cli] `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `modules/killchain.py` ranks 2 by PageRank, 37 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- [modules: autonomous_daemon] `modules/selection/base.py` ranks 1 by PageRank, 17 importers, 4 symbols: The one shared contract for autonomous action selection.
- [modules: autonomous_daemon] `skills/autonomous_daemon.py` ranks 2 by PageRank, 113 importers, 157 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [modules: exploit_migrated] `cli/commands/pwn.py` ranks 1 by PageRank, 3 importers, 8 symbols: Autonomous exploitation and LOLBAS command set.
- [modules: exploit_migrated] `lazygui/version.py` ranks 2 by PageRank, 3 importers, 0 symbols: Single source of truth for the package version string.
- [skills/hermes-lazyown] `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- [skills/hermes-lazyown] `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:cli/commands/exploit_migrated.py, file:modules/rich_tui.py, file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py
- Children: c3, c8, c11, c15
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 3.2)

Theme of 1 communities and 241 files: unassigned files (241 files, rating 3.2).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c
- Children: c28
- Theme rating = highest child community rating.

## tests (`t5`, theme, rating 0.1)

Theme of 1 communities and 4 files: tests (4 files, rating 0.1).

- [tests] `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- [tests] `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py
- Children: c19
- Theme rating = highest child community rating.

## scripts: journal (`t6`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c20
- Theme rating = highest child community rating.

## poc_tui (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c24
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t11`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c25
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t12`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c26
- Theme rating = highest child community rating.

## tools (`t13`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c27
- Theme rating = highest child community rating.

## modules/backdoor (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c21
- Theme rating = highest child community rating.

## modules: lazy_netattack (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_netattack (2 files, rating 0.0).

- [modules: lazy_netattack] `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- [modules: lazy_netattack] `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Key entities: file:modules/lazy_netattack.py, file:tests/test_lazy_netattack.py
- Children: c22
- Theme rating = highest child community rating.

## modules: lazy_triage (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules: lazy_triage (2 files, rating 0.0).

- [modules: lazy_triage] `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- [modules: lazy_triage] `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py
- Children: c23
- Theme rating = highest child community rating.

## cli/commands (`c1`, community, rating 7.0)

158 files under cli/commands (py 157, c 1), mostly utility. Core file utils.py (PageRank 0.0225, imported by 140 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on modules: lazy_loop (52), cli (30), static/js (21). Used by cli (62), modules: lazy_loop (38), modules: lazyown_mcp (28).

- `utils.py` ranks 1 by PageRank, 140 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- `cli/commands/_base.py` ranks 3 by PageRank, 111 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 126 symbols, 231 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 2 layer violations, e.g. test_security_hardening_v5.py (testing) -> addons.py (presentation).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:utils.py, file:cli/banner_config.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_categories.py, file:tests/test_winbox_gym.py, file:cli/commands/_base.py, file:tests/test_security_hardening_v3.py, file:core/hardening.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 424.

## modules: lazyown_mcp (`c2`, community, rating 6.7)

158 files under modules (py 158), mostly utility. Core file core/logging.py (PageRank 0.0757, imported by 196 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: lazy_loop (64), modules: autonomous_daemon (32), modules: chain_runner (30). Used by lazyc2/security (36), modules: autonomous_daemon (33), modules: chain_runner (29).

- `core/logging.py` ranks 1 by PageRank, 196 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/logging_config.py` ranks 2 by PageRank, 33 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- `modules/db.py` ranks 3 by PageRank, 29 importers, 37 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- Hotspot `skills/lazyown_mcp.py`: 131 symbols, 445 connections (score 0.11).
- Hotspot `tests/test_core_modules.py`: 94 symbols, 191 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 14 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py, file:skills/lazyown_facts.py, file:modules/pipeline_engine.py
- Rating 6.7/10 = 7 x PageRank share 0.96 + 3 x risk 0.00. Internal imports: 667.

## modules: lazy_loop (`c0`, community, rating 6.5)

184 files under tests (py 184), mostly testing. Core file modules/__init__.py (PageRank 0.0184, imported by 228 files). Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: chain_runner (46), modules: llm_budget (46), cli/commands (38). Used by cli (66), modules: lazyown_mcp (64), cli/commands (52).

- `modules/__init__.py` ranks 1 by PageRank, 228 importers, 0 symbols.
- `modules/world_model.py` ranks 2 by PageRank, 157 importers, 70 symbols: modules/world_model.py
- `modules/lazy_loop.py` ranks 3 by PageRank, 263 importers, 489 symbols: Lazy autonomous loop for LazyOwn.
- Hotspot `modules/lazy_loop.py`: 489 symbols, 603 connections (score 0.31).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 2 layer violations, e.g. test_orchestrator_api.py (testing) -> api_authz.py (presentation).
- Surprising bridge: search.py <-> test_lazy_match_policy.py (9 hops across communities).
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1121, file:modules/world_model.py, sym:modules/lazy_loop.py::ExplorationGraph@1229, sym:modules/lazy_loop.py::ActivityLog@1579, file:modules/lazy_proxy.py
- Rating 6.5/10 = 7 x PageRank share 0.92 + 3 x risk 0.00. Internal imports: 1035.

## cli (`c3`, community, rating 4.4)

138 files under tests (py 137, js 1), mostly utility. Core file core/console.py (PageRank 0.0156, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: lazy_loop (66), cli/commands (62), modules: lazyown_mcp (27). Used by static/js (34), modules: lazy_loop (31), cli/commands (30).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/killchain.py` ranks 2 by PageRank, 37 importers, 25 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/cli_auth.py` ranks 3 by PageRank, 21 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 161 symbols, 48 connections (score 0.09).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 5 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py
- Rating 4.4/10 = 7 x PageRank share 0.63 + 3 x risk 0.00. Internal imports: 629.

## unassigned files (`c28`, community, rating 3.2)

241 files under modules (py 133, sh 63, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0003, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 3.2/10 = 7 x PageRank share 0.46 + 3 x risk 0.00. Internal imports: 0.

## static/js (`c7`, community, rating 2.4)

49 files under static/js (py 33, js 13, c 2, sh 1), mostly utility. Core file core/config.py (PageRank 0.0171, imported by 113 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on cli (34), cli/commands (22), modules: lazy_loop (17). Used by modules: lazy_loop (36), cli (27), cli/commands (21).

- `core/config.py` ranks 1 by PageRank, 113 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- `core/param_registry.py` ranks 3 by PageRank, 19 importers, 17 symbols: Operator-managed parameter registry.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- Taint: 3 paths reach this group via subprocess.
- Dataflow: 10 INFERRED issues (first: UNCHECKED_ALLOC in do_knokknok).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:core/config.py
- Rating 2.4/10 = 7 x PageRank share 0.34 + 3 x risk 0.00. Internal imports: 314.

## modules: chain_runner (`c4`, community, rating 2.3)

81 files under tests (py 81), mostly utility. Core file core/safe_exec.py (PageRank 0.0079, imported by 62 files): Centralized safe command execution for the LazyOwn framework. Key abstractions: CommandInjectionError, UrlValidationError, needs_shell, safe_system, safe_run_argv, safe_run_shell. Depends on modules: lazy_loop (51), modules: lazyown_mcp (29), cli/commands (21). Used by modules: lazy_loop (46), modules: lazyown_mcp (30), cli/commands (10).

- `core/safe_exec.py` ranks 1 by PageRank, 62 importers, 14 symbols: Centralized safe command execution for the LazyOwn framework.
- `modules/chain_registry.py` ranks 2 by PageRank, 63 importers, 19 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `modules/outcome_bus.py` ranks 3 by PageRank, 46 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- Hotspot `tests/test_security_hardening_v4.py`: 67 symbols, 67 connections (score 0.04).
- Hotspot `modules/atomic_exploit_bridge.py`: 39 symbols, 100 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:tests/test_security_hardening_v4.py, file:modules/chain_runner.py, file:modules/atomic_exploit_bridge.py, file:cli/commands/command_and_control_migrated.py, file:modules/chain_registry.py, sym:modules/chain_registry.py::ChainStep@102, file:modules/outcome_bus.py, file:modules/winbox_gym.py
- Rating 2.3/10 = 7 x PageRank share 0.33 + 3 x risk 0.00. Internal imports: 284.

## modules: llm_budget (`c9`, community, rating 1.7)

41 files under modules (py 41), mostly utility. Core file modules/llm_factory.py (PageRank 0.0107, imported by 65 files): LLM backend factory and selection utilities. Key abstractions: LLMBackendUnavailableError, LLMBackendNotSupportedError, is_model_missing_error, groq_model_chain, default_model_for, model_config_key. Depends on modules: lazy_loop (49), modules: lazyown_mcp (21), modules: autonomous_daemon (16). Used by modules: lazy_loop (46), modules: lazyown_mcp (6), cli/commands (4).

- `modules/llm_factory.py` ranks 1 by PageRank, 65 importers, 30 symbols: LLM backend factory and selection utilities.
- `modules/ai_model.py` ranks 2 by PageRank, 10 importers, 39 symbols: Concrete language model backends for LazyOwn.
- `core/parsers.py` ranks 3 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- Hotspot `tests/test_llm_orchestrator.py`: 88 symbols, 55 connections (score 0.05).
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 1 layer violations, e.g. test_vulnbot_fallback.py (testing) -> vulnbot.py (presentation).
- Taint: 5 paths reach this group via subprocess.
- Key entities: file:tests/test_llm_orchestrator.py, file:modules/llm_factory.py, file:modules/ai_model.py, file:modules/agent_runner.py, file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py, file:telegram_hermes.py, file:tests/test_dependencies.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 136.

## lazygui/panels (`c6`, community, rating 1.5)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0058, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyown_mcp (6), cli/commands (2), modules: lazy_loop (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.5/10 = 7 x PageRank share 0.21 + 3 x risk 0.00. Internal imports: 181.

## lazyc2/security (`c5`, community, rating 1.4)

55 files under tests (py 53, js 2), mostly testing. Core file modules/lazy_rbac.py (PageRank 0.0055, imported by 21 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on modules: lazyown_mcp (36), modules: lazy_loop (22), cli/commands (17). Used by cli/commands (11), modules: lazyown_mcp (8), cli (7).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `lazyc2/security/constants.py` ranks 2 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- `lazyc2/security/cors.py` ranks 3 by PageRank, 4 importers, 15 symbols: CORS origin allowlist policy for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 313 symbols, 316 connections (score 0.19).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- 30 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 7 INFERRED issues (first: UNCHECKED_ALLOC in _probe_bind).
- Key entities: file:lazyc2.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, sym:lazyc2.py::index@3331, file:tests/test_security_lazyc2.py, file:tests/test_loop_manager.py, sym:lazyc2.py::decoy@2055, file:tests/test_api_authz.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 126.

## modules: autonomous_daemon (`c8`, community, rating 1.2)

42 files under tests (py 42), mostly utility. Core file modules/selection/base.py (PageRank 0.0031, imported by 17 files): The one shared contract for autonomous action selection. Key abstractions: SelectionContext, ActionDecision, Selector, propose, ICommandRunner, MCPCommandRunner. Depends on modules: lazyown_mcp (33), modules: lazy_loop (32), modules: chain_runner (6). Used by modules: lazyown_mcp (32), modules: lazy_loop (22), modules: llm_budget (16).

- `modules/selection/base.py` ranks 1 by PageRank, 17 importers, 4 symbols: The one shared contract for autonomous action selection.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 113 importers, 157 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `modules/detection_oracle.py` ranks 3 by PageRank, 23 importers, 18 symbols: modules/detection_oracle.py
- Hotspot `skills/autonomous_daemon.py`: 157 symbols, 291 connections (score 0.11).
- Hotspot `skills/lazyown_policy.py`: 126 symbols, 58 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> llm_orchestrator.py -> lazy_engine.py -> lazy_loop.py -> loop_triggers.py -> trigger_policy.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> contracts.py -> hub.py -> telemetry_mediator.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> autonomous_daemon.py -> planner.py -> playbook_engine.py -> emulation_runner.py -> atomic_exploit_bridge.py -> config.py.
- 14 layer violations, e.g. test_moe_rl_swan.py (testing) -> moe_router.py (presentation).
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:skills/tests/test_autonomous_daemon.py, file:tests/test_engage_orchestrator.py, file:tests/test_moe_rl_swan.py, file:skills/swan_agent.py, file:modules/moe_router.py, file:tests/test_scope_bound_auto_gate.py
- Rating 1.2/10 = 7 x PageRank share 0.18 + 3 x risk 0.00. Internal imports: 230.

## skills/claude_md_orchestrator (`c10`, community, rating 0.7)

23 files under skills/claude_md_orchestrator (py 22, js 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0026, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on cli/commands (3), static/js (3), modules: lazyown_mcp (2). Used by cli/commands (2), lazyc2/security (2), modules: lazy_loop (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:contrib/legacy/lazygptcli_unified.py, file:static/js/xterm.js, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py
- Rating 0.7/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 45.

## modules: exploit_migrated (`c11`, community, rating 0.4)

18 files under modules (py 18), mostly utility. Core file cli/commands/pwn.py (PageRank 0.0012, imported by 3 files): Autonomous exploitation and LOLBAS command set. Key abstractions: PwnCommandSet, do_auto_pwn, do_rich_tui, do_exploit_chain, do_lolbas_list, do_lolbas_use. Depends on cli/commands (8), modules: lazy_loop (7), modules: lazyown_mcp (7). Used by modules: lazyown_mcp (7), modules: lazy_loop (3), cli (1).

- `cli/commands/pwn.py` ranks 1 by PageRank, 3 importers, 8 symbols: Autonomous exploitation and LOLBAS command set.
- `lazygui/version.py` ranks 2 by PageRank, 3 importers, 0 symbols: Single source of truth for the package version string.
- `modules/dashboard_engine.py` ranks 3 by PageRank, 6 importers, 16 symbols: Live Network Map Dashboard for LazyOwn.
- Hotspot `cli/commands/exploit_migrated.py`: 52 symbols, 33 connections (score 0.03).
- Hotspot `modules/exploit_chain.py`: 19 symbols, 11 connections (score 0.01).
- Dependency cycle: hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> unified_dashboard.py -> hive_mind.py.
- Key entities: file:cli/commands/exploit_migrated.py, file:modules/rich_tui.py, file:modules/exploit_recommender.py, file:modules/dashboard_engine.py, file:modules/exploit_chain.py, file:modules/unified_dashboard.py, file:tests/test_unified_dashboard.py, file:modules/adcs_attacks.py
- Rating 0.4/10 = 7 x PageRank share 0.05 + 3 x risk 0.00. Internal imports: 22.

## modules: defense_eval (`c12`, community, rating 0.2)

8 files under modules (py 8), mostly testing. Core file modules/defense_eval.py (PageRank 0.0014, imported by 4 files): Detection rule replay over recorded attack and control logs. Key abstractions: RuleEvaluationError, Condition, Evaluation, DatasetSummary, RuleResult, to_dict. Depends on modules: lazy_loop (2), modules: lazyown_mcp (1). Used by modules: lazy_loop (3), modules: chain_runner (1).

- `modules/defense_eval.py` ranks 1 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- `modules/hunt_verify.py` ranks 2 by PageRank, 3 importers, 16 symbols: Evidence verdict verification for hunting and chain stages.
- `modules/closedloop.py` ranks 3 by PageRank, 2 importers, 7 symbols: Closed-loop detection rule tuning: baseline vs candidate comparison.
- Hotspot `modules/defense_eval.py`: 17 symbols, 9 connections (score 0.01).
- Hotspot `modules/hunt_verify.py`: 16 symbols, 6 connections (score 0.01).
- Key entities: file:modules/defense_eval.py, file:modules/hunt_verify.py, file:modules/defense_stages.py, sym:modules/defense_eval.py::evaluate_rule@322, file:tests/test_defense_eval.py, file:tests/test_hunt_verify.py, file:modules/closedloop.py, sym:modules/hunt_verify.py::verify_stages@232
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 9.

## skills/hermes-lazyown (`c15`, community, rating 0.2)

7 files under skills/hermes-lazyown (py 7), mostly utility. Core file skills/hermes-lazyown/constants.py (PageRank 0.0019, imported by 6 files): Central constants for the Hermes-LazyOwn integration layer. Key abstractions: ConfigKeys, EnvKeys, Defaults, PhaseNames, Paths, lazyown_dir. Depends on cli/commands (1), cli (1).

- `skills/hermes-lazyown/constants.py` ranks 1 by PageRank, 6 importers, 15 symbols: Central constants for the Hermes-LazyOwn integration layer.
- `skills/hermes-lazyown/claudemd_rules.py` ranks 2 by PageRank, 1 importers, 14 symbols: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.
- `skills/hermes-lazyown/config_bridge.py` ranks 3 by PageRank, 1 importers, 16 symbols: Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source.
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/output_compactor.py`: 20 symbols, 5 connections (score 0.01).
- Key entities: file:skills/hermes-lazyown/mcp_server.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/hermes-lazyown/constants.py, file:skills/hermes-lazyown/executor.py, file:skills/hermes-lazyown/config_bridge.py, file:skills/hermes-lazyown/hermes_sync.py, file:skills/hermes-lazyown/claudemd_rules.py, sym:skills/hermes-lazyown/mcp_server.py::_handle_tool@346
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 11.

## modules/guardrails (`c17`, community, rating 0.2)

6 files under modules/guardrails (py 6), mostly utility. Core file modules/guardrails/contracts.py (PageRank 0.0010, imported by 3 files): Contracts for the execution guardrail harness. Key abstractions: TaskClass, RunTicket, GuardrailContract, HarnessAdminPort, is_known, describe. Depends on cli/commands (1). Used by modules: lazy_loop (8), modules: chain_runner (1), modules: llm_budget (1).

- `modules/guardrails/contracts.py` ranks 1 by PageRank, 3 importers, 10 symbols: Contracts for the execution guardrail harness.
- `modules/guardrails/__init__.py` ranks 2 by PageRank, 9 importers, 0 symbols: Operator-facing guardrail harness: tiers, capacity, checkpoints.
- `modules/guardrails/advisories.py` ranks 3 by PageRank, 2 importers, 15 symbols: Non-blocking advisories and feature degradation.
- Hotspot `modules/guardrails/budget.py`: 16 symbols, 7 connections (score 0.01).
- Hotspot `modules/guardrails/advisories.py`: 15 symbols, 5 connections (score 0.01).
- Key entities: file:modules/guardrails/advisories.py, file:modules/guardrails/budget.py, file:modules/guardrails/harness.py, file:modules/guardrails/contracts.py, file:modules/guardrails/checkpoints.py, sym:modules/guardrails/checkpoints.py::CheckpointLedger@18, sym:modules/guardrails/harness.py::reset_global_harness@241, file:modules/guardrails/__init__.py
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 10.

## contrib/legacy (`c18`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0028, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

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

## tests (`c19`, community, rating 0.1)

4 files under tests (py 4), mostly testing. Core file tests/mutation_common.py (PageRank 0.0012, imported by 3 files): Shared driver for curated mutation runners. Key abstractions: backup_files, restore_files, run_tests, title, run_all, main.

- `tests/mutation_common.py` ranks 1 by PageRank, 3 importers, 5 symbols: Shared driver for curated mutation runners.
- `tests/run_mutation_loop_cli_catalog.py` ranks 2 by PageRank, 0 importers, 1 symbols: Mutation runner for the planner catalog visibility contract.
- `tests/run_mutation_trigger_policy.py` ranks 3 by PageRank, 0 importers, 1 symbols: Mutation runner for the trigger policy contract.
- Hotspot `tests/mutation_common.py`: 5 symbols, 7 connections (score 0.00).
- Hotspot `tests/run_mutation_loop_cli_catalog.py`: 1 symbols, 5 connections (score 0.00).
- Key entities: sym:tests/mutation_common.py::title@49, file:tests/mutation_common.py, file:tests/run_mutation_loop_cli_catalog.py, file:tests/run_mutation_trigger_policy.py, file:tests/run_mutation_verb_catalog.py, sym:tests/mutation_common.py::run_all@56, sym:tests/mutation_common.py::restore_files@30, sym:tests/mutation_common.py::backup_files@20
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 3.

## scripts: journal (`c20`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0009, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c21`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0006, imported by 1 files). Key abstractions: logg, bzero, RUNKEY_NAME, bootRun, str_cut, Shell.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 6 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 6 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::RUNKEY_NAME@17, sym:modules/backdoor/backdoor.c::Shell@88, sym:modules/backdoor/backdoor.c::WinMain@129, sym:modules/backdoor/backdoor.c::bootRun@22, sym:modules/backdoor/backdoor.c::bzero@14
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_netattack (`c22`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_netattack.py (PageRank 0.0006, imported by 1 files): Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. Key abstractions: AttackVectorVerdict, SurfaceEvidence, as_dict, surface_decision, hint_text, TestIdentity.

- `modules/lazy_netattack.py` ranks 1 by PageRank, 1 importers, 12 symbols: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.
- `tests/test_lazy_netattack.py` ranks 2 by PageRank, 0 importers, 17 symbols: Tests for modules.lazy_netattack — Windows attack-surface adjudication.
- Hotspot `tests/test_lazy_netattack.py`: 17 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_netattack.py`: 12 symbols, 4 connections (score 0.01).
- Key entities: file:modules/lazy_netattack.py, file:tests/test_lazy_netattack.py, sym:modules/lazy_netattack.py::surface_decision@184, sym:modules/lazy_netattack.py::SurfaceEvidence@120, sym:tests/test_lazy_netattack.py::test_hint_text_shapes@102, sym:tests/test_lazy_netattack.py::test_linux_host_blocked@56, sym:modules/lazy_netattack.py::hint_text@311, sym:tests/test_lazy_netattack.py::module@18
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## modules: lazy_triage (`c23`, community, rating 0.0)

2 files under modules (py 2), mostly testing. Core file modules/lazy_triage.py (PageRank 0.0006, imported by 1 files): Triage doctrine: evidence floors, verdict algebra and signature dedup. Key abstractions: SignatureStore, rank, hard_evidence, apply_rules, signature_for, fresh_signature.

- `modules/lazy_triage.py` ranks 1 by PageRank, 1 importers, 10 symbols: Triage doctrine: evidence floors, verdict algebra and signature dedup.
- `tests/test_lazy_triage.py` ranks 2 by PageRank, 0 importers, 11 symbols: Lazy triage doctrine: evidence floor algebra and signature dedup.
- Hotspot `tests/test_lazy_triage.py`: 11 symbols, 4 connections (score 0.01).
- Hotspot `modules/lazy_triage.py`: 10 symbols, 6 connections (score 0.01).
- Key entities: file:modules/lazy_triage.py, file:tests/test_lazy_triage.py, sym:modules/lazy_triage.py::apply_rules@80, sym:modules/lazy_triage.py::fresh_signature@144, sym:modules/lazy_triage.py::_save@176, sym:modules/lazy_triage.py::hard_evidence@47, sym:modules/lazy_triage.py::SignatureStore@135, sym:modules/lazy_triage.py::signature_for@108
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c24`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0006, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c25`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0006, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c26`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0006, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c27`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0006, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
