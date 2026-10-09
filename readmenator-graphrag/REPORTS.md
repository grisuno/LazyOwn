# GraphRAG Community Reports

Entities: 18026 | Relationships: 53889 | Communities: 22 | Themes: 10 | Text units: 17848

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

897 files in 22 communities and 10 themes. Highest-impact communities: modules: autonomous_daemon (7.0), cli/commands (5.9), unassigned files (3.2). God nodes: core/logging.py, utils.py, cli/commands/_base.py, skills/lazyown_mcp.py, lazyc2.py.

- [modules: autonomous_daemon] rating 7.0: `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [cli/commands] rating 5.9: `utils.py` ranks 1 by PageRank, 102 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [unassigned files] rating 3.2: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [modules: wizard] rating 2.8: `core/console.py` ranks 1 by PageRank, 59 importers, 8 symbols: ANSI color constants and console output helpers.
- [cli] rating 2.7: `cli/themes.py` ranks 1 by PageRank, 16 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [lazyc2/security] rating 1.7: `core/crypto.py` ranks 1 by PageRank, 15 importers, 7 symbols: Symmetric primitives used by the framework.
- [lazygui/panels] rating 1.7: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [modules: world_model] rating 1.3: `modules/world_model.py` ranks 1 by PageRank, 74 importers, 61 symbols: modules/world_model.py
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:utils.py, file:tests/test_improvements_spec.py, file:skills/mcp_generated_tools.py, file:modules/exp.c
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9
- Root rating = highest community rating.

## modules: autonomous_daemon + modules: wizard +7 (`t0`, theme, rating 7.0)

Theme of 9 communities and 514 files: modules: autonomous_daemon (142 files, rating 7.0); modules: wizard (54 files, rating 2.8); cli (89 files, rating 2.7); lazyc2/security (63 files, rating 1.7); lazygui/panels (54 files, rating 1.7); modules: world_model (37 files, rating 1.3); skills/claude_md_orchestrator (30 files, rating 1.0); modules: lazy_rbac (23 files, rating 1.0); static/js (22 files, rating 0.5).

- [modules: autonomous_daemon] `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 2 by PageRank, 22 importers, 11 symbols: Enumeration command set.
- [modules: wizard] `core/console.py` ranks 1 by PageRank, 59 importers, 8 symbols: ANSI color constants and console output helpers.
- [modules: wizard] `core/payload_schema.py` ranks 2 by PageRank, 12 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- [cli] `cli/themes.py` ranks 1 by PageRank, 16 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [cli] `lazyown.py` ranks 2 by PageRank, 9 importers, 127 symbols: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date: 13/08/2024 License: GPL v3  Description: This file contains the definition of the logic in the LazyOwnShell class  ██╗      █████╗ ███████╗██╗   ██╗...
- [lazyc2/security] `core/crypto.py` ranks 1 by PageRank, 15 importers, 7 symbols: Symmetric primitives used by the framework.
- [lazyc2/security] `modules/db.py` ranks 2 by PageRank, 18 importers, 35 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, sym:core/console.py::print_msg@142, sym:core/console.py::print_error@136, file:tests/test_command_palette.py, file:lazyown.py, file:lazyc2.py, file:tests/test_addon_creator.py
- Children: c0, c4, c2, c3, c5, c6, c7, c8, c9
- Theme rating = highest child community rating.

## cli/commands + contrib/legacy +3 (`t2`, theme, rating 5.9)

Theme of 5 communities and 161 files: cli/commands (136 files, rating 5.9); contrib/legacy (5 files, rating 0.2); modules: kerberos_core (7 files, rating 0.1); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 102 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `cli/commands/_base.py` ranks 2 by PageRank, 89 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:utils.py, file:tests/test_improvements_spec.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c1, c13, c10, c11, c12
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.2)

Theme of 1 communities and 207 files: unassigned files (207 files, rating 3.2).

- [unassigned files] `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [unassigned files] `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- Key entities: file:skills/mcp_generated_tools.py, file:modules/exp.c
- Children: c21
- Theme rating = highest child community rating.

## scripts: journal (`t3`, theme, rating 0.1)

Theme of 1 communities and 3 files: scripts: journal (3 files, rating 0.1).

- [scripts: journal] `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- [scripts: journal] `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py
- Children: c14
- Theme rating = highest child community rating.

## modules/backdoor (`t4`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c15
- Theme rating = highest child community rating.

## poc_tui (`t5`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c16
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c17
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c18
- Theme rating = highest child community rating.

## test (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: test (2 files, rating 0.0).

- [test] `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- [test] `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@56
- Children: c19
- Theme rating = highest child community rating.

## tools (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c20
- Theme rating = highest child community rating.

## modules: autonomous_daemon (`c0`, community, rating 7.0)

142 files under modules (py 142), mostly utility. Core file core/logging.py (PageRank 0.0831, imported by 159 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on modules: world_model (31), cli/commands (30), cli (12). Used by cli/commands (51), lazyc2/security (27), cli (25).

- `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `cli/commands/enum.py` ranks 2 by PageRank, 22 importers, 11 symbols: Enumeration command set.
- `modules/logging_config.py` ranks 3 by PageRank, 37 importers, 21 symbols: Centralized logging configuration for the LazyOwn framework.
- Hotspot `skills/lazyown_mcp.py`: 105 symbols, 384 connections (score 0.10).
- Hotspot `skills/autonomous_daemon.py`: 132 symbols, 176 connections (score 0.09).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 26 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 2 paths reach this group via subprocess.
- Key entities: file:skills/lazyown_mcp.py, file:skills/autonomous_daemon.py, file:skills/lazyown_policy.py, file:tests/test_collab_and_onboarding.py, file:skills/hive_mind.py, file:core/logging.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 830.

## cli/commands (`c1`, community, rating 5.9)

136 files under cli/commands (py 135, js 1), mostly utility. Core file utils.py (PageRank 0.0386, imported by 102 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, parse_ip_mac, create_arp_packet. Depends on modules: autonomous_daemon (51), modules: world_model (42), cli (38). Used by static/js (75), lazyc2/security (65), modules: wizard (37).

- `utils.py` ranks 1 by PageRank, 102 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `cli/commands/_base.py` ranks 2 by PageRank, 89 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- `core/validators.py` ranks 3 by PageRank, 15 importers, 7 symbols: Input validators for runtime configuration values.
- Hotspot `tests/test_improvements_spec.py`: 160 symbols, 48 connections (score 0.10).
- Hotspot `utils.py`: 121 symbols, 191 connections (score 0.09).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 4 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 7 paths reach this group via subprocess.
- Key entities: file:utils.py, file:tests/test_improvements_spec.py, file:cli/banner_config.py, file:tests/test_security_hardening_v4.py, file:tests/test_categories.py, file:tests/test_cli_command_sets.py, sym:cli/commands/_base.py::LazyOwnCommandSet@51, file:cli/commands/_base.py
- Rating 5.9/10 = 7 x PageRank share 0.84 + 3 x risk 0.00. Internal imports: 438.

## unassigned files (`c21`, community, rating 3.2)

207 files under modules (py 105, sh 56, lua 26, c 12, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0005, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.37).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 1193 connections (score 0.12).
- Dataflow: 21 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/exp.c, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c
- Rating 3.2/10 = 7 x PageRank share 0.46 + 3 x risk 0.00. Internal imports: 0.

## modules: wizard (`c4`, community, rating 2.8)

54 files under modules (py 54), mostly utility. Core file core/console.py (PageRank 0.0315, imported by 59 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on cli/commands (37), modules: autonomous_daemon (18), cli (10). Used by cli/commands (22), cli (18), modules: autonomous_daemon (9).

- `core/console.py` ranks 1 by PageRank, 59 importers, 8 symbols: ANSI color constants and console output helpers.
- `core/payload_schema.py` ranks 2 by PageRank, 12 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- `modules/llm_factory.py` ranks 3 by PageRank, 25 importers, 21 symbols: LLM backend factory and selection utilities.
- Hotspot `tests/test_payload_schema.py`: 53 symbols, 20 connections (score 0.03).
- Hotspot `cli/wizard.py`: 45 symbols, 39 connections (score 0.03).
- Taint: 6 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _run_single_search).
- Key entities: sym:core/console.py::print_msg@142, sym:core/console.py::print_error@136, sym:core/console.py::print_warn@148, file:tests/test_payload_schema.py, file:cli/wizard.py, file:core/llm_budget.py, file:modules/ai_model.py, file:tests/test_llm_adapter_parity.py
- Rating 2.8/10 = 7 x PageRank share 0.40 + 3 x risk 0.00. Internal imports: 121.

## cli (`c2`, community, rating 2.7)

89 files under cli (py 88, js 1), mostly utility. Core file cli/themes.py (PageRank 0.0053, imported by 16 files): Theme registry for the LazyOwn TUI surfaces. Key abstractions: Theme, get_theme, theme_from_payload, LazyOwnShell, log_command, default. Depends on cli/commands (28), modules: autonomous_daemon (25), modules: wizard (18). Used by cli/commands (38), modules: autonomous_daemon (12), modules: wizard (10).

- `cli/themes.py` ranks 1 by PageRank, 16 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `lazyown.py` ranks 2 by PageRank, 9 importers, 127 symbols: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date: 13/08/2024 License: GPL v3  Description: This file contains the definition of the logic in the LazyOwnShell class  ██╗      █████╗ ███████╗██╗   ██╗...
- `cli/commands/containers.py` ranks 3 by PageRank, 9 importers, 7 symbols: Container and Kubernetes attack command set.
- Hotspot `tests/test_command_palette.py`: 237 symbols, 220 connections (score 0.16).
- Hotspot `lazyown.py`: 127 symbols, 185 connections (score 0.09).
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _emit_event).
- Key entities: file:tests/test_command_palette.py, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py, file:cli/cli_enhancements.py, file:cli/status_bar.py, file:cli/tips_engine.py, file:cli/palette_command.py
- Rating 2.7/10 = 7 x PageRank share 0.38 + 3 x risk 0.00. Internal imports: 323.

## lazyc2/security (`c3`, community, rating 1.7)

63 files under tests (py 62, c 1), mostly testing. Core file core/crypto.py (PageRank 0.0060, imported by 15 files): Symmetric primitives used by the framework. Key abstractions: generate_salt, derive_key, xor_encrypt_decrypt, generate_xor_key, AESencrypt, AESdecrypt. Depends on cli/commands (65), modules: autonomous_daemon (27), modules: world_model (13). Used by modules: autonomous_daemon (9), cli/commands (8), cli (3).

- `core/crypto.py` ranks 1 by PageRank, 15 importers, 7 symbols: Symmetric primitives used by the framework.
- `modules/db.py` ranks 2 by PageRank, 18 importers, 35 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- `lazyc2/security/constants.py` ranks 3 by PageRank, 4 importers, 0 symbols: Security constants and validation patterns for the LazyOwn C2 web layer.
- Hotspot `lazyc2.py`: 263 symbols, 230 connections (score 0.17).
- Hotspot `tests/test_addon_creator.py`: 86 symbols, 11 connections (score 0.05).
- 33 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Dataflow: 4 INFERRED issues (first: UNCHECKED_ALLOC in _load_or_create_salt).
- Surprising bridge: addon_creator.py <-> search.py (8 hops across communities).
- Key entities: file:lazyc2.py, file:tests/test_addon_creator.py, file:tests/test_security_hardening_v3.py, file:tests/test_security_lazyc2.py, file:modules/rootkit/rootkit.c, sym:lazyc2.py::index@2911, file:tests/test_core.py, file:tests/test_security_hardening_v5.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 138.

## lazygui/panels (`c5`, community, rating 1.7)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0092, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: autonomous_daemon (8), modules: world_model (1), modules: lazy_rbac (1). Used by static/js (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.04).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.7/10 = 7 x PageRank share 0.24 + 3 x risk 0.00. Internal imports: 181.

## modules: world_model (`c6`, community, rating 1.3)

37 files under modules (py 37), mostly utility. Core file modules/world_model.py (PageRank 0.0110, imported by 74 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on modules: autonomous_daemon (14), cli/commands (11), modules: wizard (2). Used by cli/commands (42), modules: autonomous_daemon (31), cli (13).

- `modules/world_model.py` ranks 1 by PageRank, 74 importers, 61 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 27 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `cli/commands/pwn.py` ranks 3 by PageRank, 4 importers, 8 symbols: Autonomous exploitation and LOLBAS command set.
- Hotspot `modules/world_model.py`: 61 symbols, 93 connections (score 0.04).
- Hotspot `cli/ops_commands.py`: 53 symbols, 73 connections (score 0.04).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:modules/world_model.py, file:cli/ops_commands.py, file:tests/test_killchain_unified_v2.py, file:cli/commands/exploit_migrated.py, file:modules/opsec_scorer.py, file:modules/killchain.py, file:modules/rich_tui.py, file:tests/test_world_model_extended.py
- Rating 1.3/10 = 7 x PageRank share 0.19 + 3 x risk 0.00. Internal imports: 85.

## skills/claude_md_orchestrator (`c7`, community, rating 1.0)

30 files under skills/claude_md_orchestrator (py 29, c 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0047, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on modules: autonomous_daemon (3), cli/commands (3), lazyc2/security (2). Used by cli/commands (3), modules: autonomous_daemon (2), lazyc2/security (2).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `modules/backdoor/server.c` ranks 2 by PageRank, 10 importers, 1 symbols.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `tests/test_security_sanitizers.py`: 45 symbols, 8 connections (score 0.03).
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in main).
- Key entities: file:tests/test_security_sanitizers.py, file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/hermes-lazyown/mcp_server.py, file:cli/commands/phishing_wizard.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py
- Rating 1.0/10 = 7 x PageRank share 0.15 + 3 x risk 0.00. Internal imports: 55.

## modules: lazy_rbac (`c8`, community, rating 1.0)

23 files under modules (py 21, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0076, imported by 20 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on cli/commands (18), modules: autonomous_daemon (3), modules: wizard (2). Used by cli (12), modules: autonomous_daemon (7), cli/commands (6).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- `modules/cli_auth.py` ranks 2 by PageRank, 18 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/engagement_hooks.py` ranks 3 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 857 connections (score 0.11).
- Hotspot `static/js/socket.io-4.3.2.min.js`: 15 symbols, 565 connections (score 0.07).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:modules/lazy_rbac.py, file:tests/test_engagement_and_ping.py, file:tests/test_infra_disposable.py, file:tests/test_engagement_elo_and_methodology.py, file:cli/engagement_hooks.py, file:modules/metrics.py, file:modules/c2_builder.py, file:modules/cli_auth.py
- Rating 1.0/10 = 7 x PageRank share 0.14 + 3 x risk 0.00. Internal imports: 142.

## static/js (`c9`, community, rating 0.5)

22 files under static/js (js 11, py 10, sh 1), mostly utility. Core file modules/colors.py (PageRank 0.0030, imported by 7 files): retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta... Key abstractions: retModel, delete_lines, no_html, format_payload, get_git_info, get_venv_info. Depends on cli/commands (75), cli (5), lazygui/panels (3). Used by cli/commands (10), lazyc2/security (2), modules: wizard (1).

- `modules/colors.py` ranks 1 by PageRank, 7 importers, 3 symbols: retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta...
- `cli/show.py` ranks 2 by PageRank, 59 importers, 1 symbols: Pretty-print the live payload for the operator.
- `lazyown-docker/init.sh` ranks 3 by PageRank, 29 importers, 0 symbols.
- Hotspot `static/js/html2pdf.bundle.min.js`: 695 symbols, 5934 connections (score 1.00).
- Hotspot `static/js/vis-network-9.1.2.min.js`: 135 symbols, 4878 connections (score 0.57).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in handle_request).
- Surprising bridge: __init__.py <-> state.py (8 hops across communities).
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:static/js/chart.min.js, file:static/js/quill-2.0.3.js, file:static/js/bootstrap-5.3.0.bundle.min.js, file:static/js/xterm.js, file:contrib/legacy/lazygptcli_unified.py
- Rating 0.5/10 = 7 x PageRank share 0.08 + 3 x risk 0.00. Internal imports: 88.

## contrib/legacy (`c13`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0048, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::base64_decode@8
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 4.

## modules: kerberos_core (`c10`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0015, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## modules: saas_attacks (`c11`, community, rating 0.1)

7 files under modules (py 7), mostly utility. Core file modules/aws_attacks.py (PageRank 0.0006, imported by 1 files): AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. Key abstractions: AWSConfig, AWSAttackEngine, enumerate_iam_permissions, lambda_backdoor, sts_role_chain, ec2_user_data_exfil. Depends on cli/commands (1).

- `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- `modules/entra_id_attacks.py` ranks 3 by PageRank, 1 importers, 12 symbols: Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.
- Hotspot `modules/saas_attacks.py`: 15 symbols, 5 connections (score 0.01).
- Hotspot `modules/entra_id_attacks.py`: 12 symbols, 7 connections (score 0.01).
- Key entities: file:modules/saas_attacks.py, file:modules/entra_id_attacks.py, file:modules/aws_attacks.py, file:modules/k8s_attacks.py, file:modules/gcp_attacks.py, file:modules/cross_cloud.py, file:cli/commands/cloud_attacks.py, sym:cli/commands/cloud_attacks.py::do_k8s_attack@302
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 6.

## modules: polymorphic_engine (`c12`, community, rating 0.1)

6 files under modules (py 6), mostly utility. Core file modules/dotnet_payload.py (PageRank 0.0006, imported by 2 files): .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. Key abstractions: DotNetPayloadConfig, DotNetPayloadFactory, list_templates, generate_source, compile, generate. Depends on cli/commands (1).

- `modules/dotnet_payload.py` ranks 1 by PageRank, 2 importers, 12 symbols: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- `modules/linux_advanced_payloads.py` ranks 2 by PageRank, 2 importers, 17 symbols: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- `modules/macos_payloads.py` ranks 3 by PageRank, 2 importers, 16 symbols: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Hotspot `modules/polymorphic_engine.py`: 19 symbols, 11 connections (score 0.01).
- Hotspot `modules/staged_delivery.py`: 18 symbols, 8 connections (score 0.01).
- Key entities: sym:modules/dotnet_payload.py::compile@408, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 8.

## scripts: journal (`c14`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0014, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c15`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0010, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c16`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0010, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 13 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@150, sym:poc_tui/plugin_loader.py::load_all@128, sym:poc_tui/plugin_loader.py::PluginSpec@28, sym:poc_tui/plugin_loader.py::_register_tool@250, sym:poc_tui/plugin_loader.py::_replace_placeholders@40
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c17`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0010, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c18`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0010, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## test (`c19`, community, rating 0.0)

2 files under test (py 2), mostly infrastructure. Core file test/config.py (PageRank 0.0010, imported by 1 files): o config.py Key abstractions: encrypt_data, decrypt_data, send_command_via_web, get_encrypted_command, post_result, test_migrate.

- `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Hotspot `test/test_commands.py`: 15 symbols, 7 connections (score 0.01).
- Hotspot `test/config.py`: 2 symbols, 5 connections (score 0.00).
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@56, sym:test/test_commands.py::send_command_via_web@35, file:test/config.py, sym:test/test_commands.py::test_download@123, sym:test/test_commands.py::test_discover@97, sym:test/test_commands.py::test_migrate@69, sym:test/test_commands.py::test_persistence@160
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c20`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0010, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@13, sym:tools/gen_demo_gifs.py::render@21, sym:tools/gen_demo_gifs.py::main@69, sym:tools/gen_demo_gifs_extra.py::main@47
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
