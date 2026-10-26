# GraphRAG Community Reports

Entities: 23444 | Relationships: 74665 | Communities: 24 | Themes: 11 | Text units: 23341

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

1186 files in 24 communities and 11 themes. Highest-impact communities: modules: autonomous_daemon (7.0), cli/commands (5.0), modules: lazy_loop (4.4). God nodes: core/logging.py, utils.py, modules/lazy_loop.py, skills/lazyown_mcp.py, cli/commands/_base.py.

- [modules: autonomous_daemon] rating 7.0: `core/logging.py` ranks 1 by PageRank, 192 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 5.0: `utils.py` ranks 1 by PageRank, 127 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazy_loop] rating 4.4: `core/config.py` ranks 1 by PageRank, 105 importers, 20 symbols: Configuration loader and Config wrapper.
- [cli] rating 3.3: `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 2.6: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: world_model] rating 1.7: `modules/world_model.py` ranks 1 by PageRank, 138 importers, 70 symbols: modules/world_model.py
- [modules: lazyc2] rating 1.4: `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [lazygui/panels] rating 1.2: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:utils.py, file:cli/banner_config.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
- Root rating = highest community rating.

## modules: autonomous_daemon + modules: lazy_loop +4 (`t0`, theme, rating 7.0)

Theme of 6 communities and 438 files: modules: autonomous_daemon (186 files, rating 7.0); modules: lazy_loop (126 files, rating 4.4); modules: lazyc2 (67 files, rating 1.4); core (22 files, rating 0.5); skills/claude_md_orchestrator (23 files, rating 0.5); modules: opsec_scorer (14 files, rating 0.3).

- [modules: autonomous_daemon] `core/logging.py` ranks 1 by PageRank, 192 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- [modules: lazy_loop] `core/config.py` ranks 1 by PageRank, 105 importers, 20 symbols: Configuration loader and Config wrapper.
- [modules: lazy_loop] `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- [modules: lazyc2] `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- [modules: lazyc2] `modules/db.py` ranks 2 by PageRank, 25 importers, 37 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- [core] `core/parsers.py` ranks 1 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- [core] `core/llm_budget.py` ranks 2 by PageRank, 20 importers, 45 symbols: LLM budget cap and per call token counter.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py
- Children: c0, c3, c4, c10, c9, c11
- Theme rating = highest child community rating.

## cli/commands + modules: kerberos_core +3 (`t3`, theme, rating 5.0)

Theme of 5 communities and 180 files: cli/commands (155 files, rating 5.0); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1); contrib/legacy (5 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 127 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- [modules: polymorphic_engine] `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- [modules: polymorphic_engine] `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- Key entities: file:utils.py, file:cli/banner_config.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py
- Children: c1, c12, c13, c14, c15
- Theme rating = highest child community rating.

## cli + modules: world_model +3 (`t1`, theme, rating 3.3)

Theme of 5 communities and 317 files: cli (126 files, rating 3.3); modules: world_model (63 files, rating 1.7); lazygui/panels (54 files, rating 1.2); modules: lazyown_facts (46 files, rating 0.9); static/js (28 files, rating 0.5).

- [cli] `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- [cli] `modules/killchain.py` ranks 2 by PageRank, 33 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- [modules: world_model] `modules/world_model.py` ranks 1 by PageRank, 138 importers, 70 symbols: modules/world_model.py
- [modules: world_model] `modules/outcome_bus.py` ranks 2 by PageRank, 26 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- [lazygui/panels] `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [lazygui/panels] `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- [modules: lazyown_facts] `modules/chain_registry.py` ranks 1 by PageRank, 49 importers, 17 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- [modules: lazyown_facts] `skills/lazyown_facts.py` ranks 2 by PageRank, 12 importers, 79 symbols: LazyOwn FactStore
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:modules/world_model.py, file:modules/atomic_exploit_bridge.py, sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:skills/lazyown_facts.py, file:modules/chain_runner.py
- Children: c2, c5, c6, c7, c8
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 2.6)

Theme of 1 communities and 234 files: unassigned files (234 files, rating 2.6).

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

## modules: autonomous_daemon (`c0`, community, rating 7.0)

186 files under modules (py 186), mostly utility. Core file core/logging.py (PageRank 0.0779, imported by 192 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: lazy_loop (70), modules: world_model (55), cli (40). Used by modules: lazy_loop (58), modules: lazyc2 (32), cli/commands (30).

- `core/logging.py` ranks 1 by PageRank, 192 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `cli/commands/enum.py` ranks 2 by PageRank, 25 importers, 11 symbols: Enumeration command set.
- `modules/llm_factory.py` ranks 3 by PageRank, 49 importers, 29 symbols: LLM backend factory and selection utilities.
- Hotspot `skills/lazyown_mcp.py`: 146 symbols, 494 connections (score 0.12).
- Hotspot `skills/autonomous_daemon.py`: 150 symbols, 267 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 17 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:core/logging.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_hive_mind.py, file:skills/tests/test_autonomous_daemon.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 1000.

## cli/commands (`c1`, community, rating 5.0)

155 files under cli/commands (py 154, c 1), mostly utility. Core file utils.py (PageRank 0.0233, imported by 127 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, lazyown_set_config, needs_sudo. Depends on cli (67), modules: lazy_loop (45), modules: autonomous_daemon (30). Used by modules: lazy_loop (51), modules: autonomous_daemon (37), cli (35).

- `utils.py` ranks 1 by PageRank, 127 importers, 126 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: AGPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/validators.py` ranks 2 by PageRank, 19 importers, 8 symbols: Input validators for runtime configuration values.
- `cli/commands/_base.py` ranks 3 by PageRank, 100 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- Hotspot `utils.py`: 126 symbols, 218 connections (score 0.09).
- Hotspot `cli/banner_config.py`: 120 symbols, 34 connections (score 0.07).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 6 paths reach this group via subprocess.
- Key entities: file:utils.py, file:cli/banner_config.py, file:tests/test_security_hardening_v4.py, file:tests/test_categories.py, sym:cli/commands/_base.py::LazyOwnCommandSet@53, file:tests/test_cli_command_sets.py, file:tests/test_security_hardening_v3.py, file:cli/cli_enhancements.py
- Rating 5.0/10 = 7 x PageRank share 0.71 + 3 x risk 0.00. Internal imports: 495.

## modules: lazy_loop (`c3`, community, rating 4.4)

126 files under tests (py 126), mostly utility. Core file core/config.py (PageRank 0.0174, imported by 105 files): Configuration loader and Config wrapper. Key abstractions: Config, as_params, overridden_keys, resolve_aes_key, load_payload, load_and_validate. Depends on modules: autonomous_daemon (58), cli/commands (51), modules: world_model (41). Used by modules: autonomous_daemon (70), cli/commands (45), cli (28).

- `core/config.py` ranks 1 by PageRank, 105 importers, 20 symbols: Configuration loader and Config wrapper.
- `core/payload_schema.py` ranks 2 by PageRank, 22 importers, 30 symbols: Declarative schema and validation for ``payload.json``.
- `modules/lazy_loop.py` ranks 3 by PageRank, 218 importers, 465 symbols: Lazy autonomous loop for LazyOwn.
- Hotspot `modules/lazy_loop.py`: 465 symbols, 480 connections (score 0.29).
- Hotspot `tests/test_lazy_runner.py`: 143 symbols, 264 connections (score 0.10).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 25 layer violations, e.g. test_api_authz.py (testing) -> api_authz.py (presentation).
- Taint: 3 paths reach this group via subprocess.
- Key entities: sym:modules/workspace.py::write_text@72, file:modules/lazy_loop.py, file:tests/test_lazy_runner.py, sym:modules/lazy_loop.py::get@1014, file:modules/lazy_proxy.py, file:tests/test_guardrails.py, sym:modules/lazy_loop.py::ExplorationGraph@1122, file:core/config.py
- Rating 4.4/10 = 7 x PageRank share 0.63 + 3 x risk 0.00. Internal imports: 886.

## cli (`c2`, community, rating 3.3)

126 files under tests (py 126), mostly utility. Core file core/console.py (PageRank 0.0169, imported by 65 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on modules: world_model (47), cli/commands (35), modules: autonomous_daemon (29). Used by cli/commands (67), modules: autonomous_daemon (40), static/js (21).

- `core/console.py` ranks 1 by PageRank, 65 importers, 11 symbols: ANSI color constants and console output helpers.
- `modules/killchain.py` ranks 2 by PageRank, 33 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `modules/cli_auth.py` ranks 3 by PageRank, 21 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.09).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 4 paths reach this group via subprocess.
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, sym:core/console.py::print_warn@149, file:tests/test_improvements_spec.py, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py
- Rating 3.3/10 = 7 x PageRank share 0.47 + 3 x risk 0.00. Internal imports: 507.

## unassigned files (`c23`, community, rating 2.6)

234 files under modules (py 126, sh 63, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0004, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.35).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 972 connections (score 0.08).
- Dataflow: 5 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:tests/test_broadcom_wps_addon.py, file:tests/test_dirtyinit_addon.py
- Rating 2.6/10 = 7 x PageRank share 0.37 + 3 x risk 0.00. Internal imports: 0.

## modules: world_model (`c5`, community, rating 1.7)

63 files under modules (py 63), mostly utility. Core file modules/world_model.py (PageRank 0.0151, imported by 138 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on cli/commands (27), modules: lazy_loop (27), modules: autonomous_daemon (22). Used by modules: autonomous_daemon (55), cli (47), modules: lazy_loop (41).

- `modules/world_model.py` ranks 1 by PageRank, 138 importers, 70 symbols: modules/world_model.py
- `modules/outcome_bus.py` ranks 2 by PageRank, 26 importers, 17 symbols: Single fan-out contract for engagement outcomes.
- `modules/atomic_exploit_bridge.py` ranks 3 by PageRank, 44 importers, 37 symbols: Atomic exploit catalogue bridge — one YAML per exploit under ``exploits/``.
- Hotspot `modules/world_model.py`: 70 symbols, 167 connections (score 0.05).
- Hotspot `cli/commands/exploit_migrated.py`: 52 symbols, 33 connections (score 0.03).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> loop_ai_bridge.py -> hive_mind.py -> lazyown_groq_agents.py -> lazyown_mcp.py -> exploitgym_gym.py -> redteam_gym.py -> config.py.
- 1 layer violations, e.g. test_c2_surfaces.py (testing) -> lazydeepseekcli.py (presentation).
- Dataflow: 4 INFERRED issues (first: UNCHECKED_ALLOC in validate_client_id).
- Key entities: file:modules/world_model.py, file:modules/atomic_exploit_bridge.py, file:cli/commands/exploit_migrated.py, file:tests/test_infra_disposable.py, file:modules/redteam_gym.py, file:modules/c2_builder.py, file:cli/surface_graph.py, file:modules/outcome_bus.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 161.

## modules: lazyc2 (`c4`, community, rating 1.4)

67 files under tests (py 65, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0059, imported by 21 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on modules: autonomous_daemon (32), modules: world_model (27), cli/commands (21). Used by modules: autonomous_daemon (25), cli (13), cli/commands (5).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 21 importers, 86 symbols: modules/lazy_rbac.py
- `modules/db.py` ranks 2 by PageRank, 25 importers, 37 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- `lazyc2/security/constants.py` ranks 3 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 306 symbols, 292 connections (score 0.19).
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 523 connections (score 0.06).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> autonomous_exploit_engine.py -> db.py -> config.py.
- 18 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_security_lazyc2.py, sym:lazyc2.py::index@3269, file:modules/collab_bp.py, file:modules/event_bus.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 154.

## lazygui/panels (`c6`, community, rating 1.2)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0065, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: autonomous_daemon (8), cli (1), modules: lazyc2 (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.2/10 = 7 x PageRank share 0.17 + 3 x risk 0.00. Internal imports: 181.

## modules: lazyown_facts (`c7`, community, rating 0.9)

46 files under tests (py 46), mostly utility. Core file modules/chain_registry.py (PageRank 0.0041, imported by 49 files): Chain registry - ordered orchestration chains from ``chains/*.yaml``. Key abstractions: ChainStep, Chain, identifier, resolve, evaluate_when, validate_chain. Depends on modules: autonomous_daemon (18), cli/commands (14), modules: lazy_loop (10). Used by modules: lazy_loop (22), modules: autonomous_daemon (7), modules: world_model (5).

- `modules/chain_registry.py` ranks 1 by PageRank, 49 importers, 17 symbols: Chain registry - ordered orchestration chains from ``chains/*.yaml``.
- `skills/lazyown_facts.py` ranks 2 by PageRank, 12 importers, 79 symbols: LazyOwn FactStore
- `modules/defense_eval.py` ranks 3 by PageRank, 4 importers, 17 symbols: Detection rule replay over recorded attack and control logs.
- Hotspot `skills/lazyown_facts.py`: 79 symbols, 24 connections (score 0.04).
- Hotspot `modules/chain_runner.py`: 41 symbols, 44 connections (score 0.03).
- Dependency cycle: orchestrator_config.py -> auto_registry.py -> lazy_orchestrator_feedback.py -> lazy_intel.py -> __init__.py -> chain_mediator.py -> lazy_loop.py -> defense_stages.py -> orchestrator_config.py.
- Key entities: file:skills/lazyown_facts.py, file:modules/chain_runner.py, file:cli/commands/command_and_control_migrated.py, file:skills/tests/test_facts.py, file:modules/chain_registry.py, file:tests/test_chain_runner.py, sym:modules/chain_registry.py::ChainStep@62, file:tests/test_chain_v24_core.py
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 124.

## core (`c10`, community, rating 0.5)

22 files under core (py 22), mostly utility. Core file core/parsers.py (PageRank 0.0031, imported by 10 files): Shared text kernel for the LazyOwn framework. Key abstractions: strip_ansi, BudgetExceeded, LLMBackendLike, ModelPrice, BudgetConfig, LedgerEntry. Depends on modules: autonomous_daemon (13), cli/commands (7), cli (7). Used by modules: autonomous_daemon (3), cli/commands (3), modules: lazyc2 (2).

- `core/parsers.py` ranks 1 by PageRank, 10 importers, 1 symbols: Shared text kernel for the LazyOwn framework.
- `core/llm_budget.py` ranks 2 by PageRank, 20 importers, 45 symbols: LLM budget cap and per call token counter.
- `core/dependencies.py` ranks 3 by PageRank, 3 importers, 23 symbols: Graceful optional-import handling for heavy third-party dependencies.
- Hotspot `core/llm_budget.py`: 45 symbols, 29 connections (score 0.03).
- Hotspot `tests/test_llm_adapter_parity.py`: 41 symbols, 24 connections (score 0.02).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:core/llm_budget.py, file:tests/test_llm_adapter_parity.py, file:telegram_hermes.py, file:tests/test_dependencies.py, file:modules/llm_prompts.py, file:discord_c2.py, file:telegram_c2.py, file:tests/test_llm_prompts.py
- Rating 0.5/10 = 7 x PageRank share 0.07 + 3 x risk 0.00. Internal imports: 47.

## static/js (`c8`, community, rating 0.5)

28 files under static/js (js 14, py 11, c 2, sh 1), mostly utility. Core file cli/assign.py (PageRank 0.0024, imported by 130 files): ``assign`` business logic. Key abstractions: apply_assign, format_payload, style, active_tokens, paint, render_prompt. Depends on cli (21), modules: lazy_loop (21), modules: autonomous_daemon (14). Used by cli/commands (8), cli (3), modules: lazy_loop (3).

- `cli/assign.py` ranks 1 by PageRank, 130 importers, 1 symbols: ``assign`` business logic.
- `cli/show.py` ranks 2 by PageRank, 59 importers, 1 symbols: Pretty-print the live payload for the operator.
- `lazyown-docker/init.sh` ranks 3 by PageRank, 36 importers, 0 symbols.
- Hotspot `static/js/html2pdf.bundle.min.js`: 738 symbols, 4927 connections (score 0.78).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 7838 connections (score 0.70).
- Dataflow: 9 INFERRED issues (first: UNCHECKED_ALLOC in spray_keyring_list_overwrite_purpose).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:tests/test_payload_schema.py
- Rating 0.5/10 = 7 x PageRank share 0.07 + 3 x risk 0.00. Internal imports: 245.

## skills/claude_md_orchestrator (`c9`, community, rating 0.5)

23 files under skills/claude_md_orchestrator (py 22, js 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0028, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on modules: autonomous_daemon (4), static/js (3), cli/commands (2). Used by cli/commands (2), modules: lazyc2 (2), modules: autonomous_daemon (1).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `skills/claude_md_orchestrator/config.py` ranks 2 by PageRank, 10 importers, 15 symbols: Centralized configuration for the claude_md_orchestrator skill.
- `modules/colors.py` ranks 3 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- Hotspot `static/js/xterm.js`: 62 symbols, 3665 connections (score 0.31).
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Key entities: sym:skills/claude_md_orchestrator/validators.py::group@69, file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:contrib/legacy/lazygptcli_unified.py, file:static/js/xterm.js, file:skills/claude_md_orchestrator/validators.py, file:skills/claude_md_orchestrator/config.py
- Rating 0.5/10 = 7 x PageRank share 0.08 + 3 x risk 0.00. Internal imports: 45.

## modules: opsec_scorer (`c11`, community, rating 0.3)

14 files under modules (py 14), mostly utility. Core file core/credential_vault.py (PageRank 0.0024, imported by 6 files): Credential vault — AES-256-GCM encryption for sensitive config values. Key abstractions: check_dangerous_defaults, seal_value, unseal_value, seal_payload, unseal_payload, rotate_aes_key. Depends on modules: lazy_loop (8), modules: autonomous_daemon (4), cli/commands (3). Used by cli/commands (1), cli (1).

- `core/credential_vault.py` ranks 1 by PageRank, 6 importers, 8 symbols: Credential vault — AES-256-GCM encryption for sensitive config values.
- `modules/opsec_scorer.py` ranks 2 by PageRank, 6 importers, 36 symbols: OPSEC scoring engine — pre-execution noise assessment and gated scoring.
- `modules/hash_cracker.py` ranks 3 by PageRank, 3 importers, 17 symbols: Hash cracking pipeline — John the Ripper and Hashcat integration.
- Hotspot `modules/opsec_scorer.py`: 36 symbols, 20 connections (score 0.02).
- Hotspot `tests/test_hash_cracker.py`: 22 symbols, 3 connections (score 0.01).
- Dependency cycle: config.py -> payload_schema.py -> llm_factory.py -> harness.py -> orchestrator_config.py -> auto_registry.py -> lazy_cli_bridge.py -> killchain.py -> world_model.py -> hardening.py -> credential_vault.py -> config.py.
- Key entities: file:modules/opsec_scorer.py, file:modules/hash_cracker.py, file:tests/test_opsec_scorer_consolidated.py, file:tests/test_hash_cracker.py, file:modules/timestomper.py, file:core/credential_vault.py, sym:modules/opsec_scorer.py::score@365, file:modules/network_opsec.py
- Rating 0.3/10 = 7 x PageRank share 0.04 + 3 x risk 0.00. Internal imports: 20.

## modules: kerberos_core (`c12`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0011, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c13`, community, rating 0.1)

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

## contrib/legacy (`c15`, community, rating 0.1)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0030, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 4.

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
- Rating 0.0/10 = 7 x PageRank share 0.00 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c19`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0007, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 14 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@161, sym:poc_tui/plugin_loader.py::_replace_placeholders@41, sym:poc_tui/plugin_loader.py::load_all@139, sym:poc_tui/plugin_loader.py::PluginSpec@29, sym:poc_tui/plugin_loader.py::_register_tool@261
- Rating 0.0/10 = 7 x PageRank share 0.00 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c20`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0007, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.00 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c21`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0007, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:tests/test_migrate_lazyown_generator.py::test_method_bodies_are_embedded_in_order@81
- Rating 0.0/10 = 7 x PageRank share 0.00 + 3 x risk 0.00. Internal imports: 1.

## tools (`c22`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0007, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.00 + 3 x risk 0.00. Internal imports: 1.
