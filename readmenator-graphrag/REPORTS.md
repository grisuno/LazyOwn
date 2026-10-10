# GraphRAG Community Reports

Entities: 19166 | Relationships: 57705 | Communities: 23 | Themes: 11 | Text units: 19034

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

944 files in 23 communities and 11 themes. Highest-impact communities: cli/commands (7.0), modules: lazyc2 (5.0), modules: autonomous_daemon (4.1). God nodes: core/logging.py, utils.py, cli/commands/_base.py, skills/lazyown_mcp.py, lazyc2.py.

- [cli/commands] rating 7.0: `utils.py` ranks 1 by PageRank, 104 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [modules: lazyc2] rating 5.0: `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: autonomous_daemon] rating 4.1: `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [modules: quill-2.0.3] rating 3.6: `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- [unassigned files] rating 3.4: `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- [cli] rating 2.7: `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [lazygui/panels] rating 1.8: `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [modules: world_model] rating 1.4: `modules/world_model.py` ranks 1 by PageRank, 75 importers, 61 symbols: modules/world_model.py
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py
- Children: t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
- Root rating = highest community rating.

## cli/commands + modules: kerberos_core +3 (`t3`, theme, rating 7.0)

Theme of 5 communities and 186 files: cli/commands (161 files, rating 7.0); modules: kerberos_core (7 files, rating 0.2); contrib/legacy (5 files, rating 0.2); modules: saas_attacks (7 files, rating 0.1); modules: polymorphic_engine (6 files, rating 0.1).

- [cli/commands] `utils.py` ranks 1 by PageRank, 104 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- [cli/commands] `cli/commands/_base.py` ranks 2 by PageRank, 92 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- [modules: kerberos_core] `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- [modules: kerberos_core] `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- [contrib/legacy] `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- [contrib/legacy] `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- [modules: saas_attacks] `modules/aws_attacks.py` ranks 1 by PageRank, 1 importers, 11 symbols: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- [modules: saas_attacks] `modules/cross_cloud.py` ranks 2 by PageRank, 1 importers, 10 symbols: Cross-cloud identity paths — multi-cloud identity federation abuse.
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:modules/saas_attacks.py, file:modules/entra_id_attacks.py
- Children: c0, c10, c14, c11, c12
- Theme rating = highest child community rating.

## modules: lazyc2 + modules: autonomous_daemon +4 (`t0`, theme, rating 5.0)

Theme of 6 communities and 342 files: modules: lazyc2 (89 files, rating 5.0); modules: autonomous_daemon (114 files, rating 4.1); lazygui/panels (54 files, rating 1.8); modules: world_model (37 files, rating 1.4); skills/claude_md_orchestrator (28 files, rating 1.0); modules: lazy_loop (20 files, rating 0.6).

- [modules: lazyc2] `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- [modules: lazyc2] `modules/db.py` ranks 2 by PageRank, 24 importers, 35 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- [modules: autonomous_daemon] `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- [modules: autonomous_daemon] `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 148 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- [lazygui/panels] `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- [lazygui/panels] `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- [modules: world_model] `modules/world_model.py` ranks 1 by PageRank, 75 importers, 61 symbols: modules/world_model.py
- [modules: world_model] `modules/killchain.py` ranks 2 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py, sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:modules/world_model.py, file:cli/ops_commands.py
- Children: c2, c1, c5, c6, c7, c9
- Theme rating = highest child community rating.

## modules: quill-2.0.3 + cli +2 (`t2`, theme, rating 3.6)

Theme of 4 communities and 191 files: modules: quill-2.0.3 (75 files, rating 3.6); cli (85 files, rating 2.7); lazyc2/blueprints (26 files, rating 1.1); static/js (5 files, rating 0.1).

- [modules: quill-2.0.3] `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- [modules: quill-2.0.3] `core/payload_schema.py` ranks 2 by PageRank, 12 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- [cli] `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- [cli] `lazyown.py` ranks 2 by PageRank, 9 importers, 127 symbols: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date: 13/08/2024 License: GPL v3  Description: This file contains the definition of the logic in the LazyOwnShell class  ██╗      █████╗ ███████╗██╗   ██╗...
- [lazyc2/blueprints] `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- [lazyc2/blueprints] `modules/cli_auth.py` ranks 2 by PageRank, 18 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- [static/js] `cli/style.py` ranks 1 by PageRank, 10 importers, 4 symbols: Centralised TUI style tokens for the LazyOwn operator surface.
- [static/js] `modules/search.py` ranks 2 by PageRank, 9 importers, 0 symbols: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: webscrapper gtofbins  ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗ ██║...
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, file:tests/test_command_palette.py, file:lazyown.py, file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:static/js/jquery-3.5.1.slim.min.js, file:cli/style.py
- Children: c4, c3, c8, c13
- Theme rating = highest child community rating.

## unassigned files (`t1`, theme, rating 3.4)

Theme of 1 communities and 210 files: unassigned files (210 files, rating 3.4).

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
- Children: c15
- Theme rating = highest child community rating.

## tools (`t10`, theme, rating 0.0)

Theme of 1 communities and 2 files: tools (2 files, rating 0.0).

- [tools] `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- [tools] `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py
- Children: c21
- Theme rating = highest child community rating.

## modules/backdoor (`t5`, theme, rating 0.0)

Theme of 1 communities and 2 files: modules/backdoor (2 files, rating 0.0).

- [modules/backdoor] `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- [modules/backdoor] `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h
- Children: c16
- Theme rating = highest child community rating.

## poc_tui (`t6`, theme, rating 0.0)

Theme of 1 communities and 2 files: poc_tui (2 files, rating 0.0).

- [poc_tui] `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- [poc_tui] `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py
- Children: c17
- Theme rating = highest child community rating.

## scripts: check_contract_manifest (`t7`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: check_contract_manifest (2 files, rating 0.0).

- [scripts: check_contract_manifest] `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- [scripts: check_contract_manifest] `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176
- Children: c18
- Theme rating = highest child community rating.

## scripts: migrate_lazyown (`t8`, theme, rating 0.0)

Theme of 1 communities and 2 files: scripts: migrate_lazyown (2 files, rating 0.0).

- [scripts: migrate_lazyown] `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- [scripts: migrate_lazyown] `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py
- Children: c19
- Theme rating = highest child community rating.

## test (`t9`, theme, rating 0.0)

Theme of 1 communities and 2 files: test (2 files, rating 0.0).

- [test] `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- [test] `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59
- Children: c20
- Theme rating = highest child community rating.

## cli/commands (`c0`, community, rating 7.0)

161 files under cli/commands (py 148, js 10, c 2, sh 1), mostly utility. Core file utils.py (PageRank 0.0371, imported by 104 files): Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗... Key abstractions: MyServer, SimpleHTTPRequestHandler, IP2ASN, VulnerabilityScanner, parse_ip_mac, create_arp_packet. Depends on modules: world_model (41), cli (39), modules: autonomous_daemon (37). Used by modules: autonomous_daemon (54), modules: quill-2.0.3 (47), cli (28).

- `utils.py` ranks 1 by PageRank, 104 importers, 121 symbols: Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024 License: GPL v3  Description: This file contains the logic for all functions used in the LazyOwnShell class.  ██╗      █████╗ ███████╗██╗   ██╗...
- `cli/commands/_base.py` ranks 2 by PageRank, 92 importers, 7 symbols: Base class for phase-scoped ``CommandSet`` modules.
- `core/validators.py` ranks 3 by PageRank, 15 importers, 7 symbols: Input validators for runtime configuration values.
- Hotspot `static/js/html2pdf.bundle.min.js`: 695 symbols, 5934 connections (score 0.81).
- Hotspot `static/js/3d-force-graph-1.73.4.min.js`: 176 symbols, 8744 connections (score 0.70).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 6 layer violations, e.g. test_help_ui_command_set.py (testing) -> help_ui.py (presentation).
- Taint: 9 paths reach this group via subprocess.
- Key entities: file:static/js/html2pdf.bundle.min.js, file:static/js/3d-force-graph-1.73.4.min.js, file:utils.py, file:tests/test_improvements_spec.py, file:static/js/vis-network-9.1.2.min.js, file:static/js/vis-network.min.js, file:modules/exp.c, file:cli/banner_config.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 697.

## modules: lazyc2 (`c2`, community, rating 5.0)

89 files under modules (py 88, js 1), mostly utility. Core file core/logging.py (PageRank 0.0798, imported by 159 files): Structured JSON-lines logging for the LazyOwn framework. Key abstractions: StructuredLogConfig, StructuredLogger, format, format, makeRecord, get_logger. Depends on cli/commands (25), modules: world_model (17), modules: autonomous_daemon (11). Used by modules: autonomous_daemon (68), cli/commands (23), modules: quill-2.0.3 (21).

- `core/logging.py` ranks 1 by PageRank, 159 importers, 12 symbols: Structured JSON-lines logging for the LazyOwn framework.
- `modules/db.py` ranks 2 by PageRank, 24 importers, 35 symbols: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- `modules/toposwarm_bridge.py` ranks 3 by PageRank, 7 importers, 22 symbols: modules/toposwarm_bridge.py
- Hotspot `static/js/xterm.js`: 62 symbols, 3833 connections (score 0.30).
- Hotspot `lazyc2.py`: 271 symbols, 242 connections (score 0.17).
- Dependency cycle: autonomous_daemon.py -> lazyown_mcp.py -> pipeline_engine.py -> autonomous_daemon.py.
- 34 layer violations, e.g. test_api_authz.py (testing) -> api_authz.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:lazyc2.py, file:tests/test_collab_and_onboarding.py, file:core/logging.py, file:modules/pipeline_engine.py, file:tests/test_pipeline_engine.py, file:tests/test_security_lazyc2.py, sym:lazyc2.py::index@2957, file:modules/collab_bp.py
- Rating 5.0/10 = 7 x PageRank share 0.71 + 3 x risk 0.00. Internal imports: 300.

## modules: autonomous_daemon (`c1`, community, rating 4.1)

114 files under modules (py 113, js 1), mostly utility. Core file cli/commands/enum.py (PageRank 0.0283, imported by 23 files): Enumeration command set. Key abstractions: EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap, do_getnpusers. Depends on modules: lazyc2 (68), cli/commands (54), modules: world_model (29). Used by cli/commands (37), modules: lazyc2 (11), modules: lazy_loop (11).

- `cli/commands/enum.py` ranks 1 by PageRank, 23 importers, 11 symbols: Enumeration command set.
- `skills/autonomous_daemon.py` ranks 2 by PageRank, 111 importers, 148 symbols: skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
- `modules/llm_client.py` ranks 3 by PageRank, 6 importers, 11 symbols: LazyOwn Unified LLM Client
- Hotspot `static/js/chart.min.js`: 88 symbols, 2829 connections (score 0.24).
- Hotspot `skills/autonomous_daemon.py`: 148 symbols, 256 connections (score 0.10).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- 21 layer violations, e.g. integration_autonomous_flow.py (testing) -> moe_router.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Key entities: file:skills/autonomous_daemon.py, file:skills/lazyown_mcp.py, file:skills/lazyown_policy.py, file:skills/hive_mind.py, file:tests/test_core_modules.py, file:skills/tests/test_autonomous_daemon.py, file:static/js/chart.min.js, file:skills/tests/test_hive_mind.py
- Rating 4.1/10 = 7 x PageRank share 0.58 + 3 x risk 0.00. Internal imports: 636.

## modules: quill-2.0.3 (`c4`, community, rating 3.6)

75 files under modules (py 74, js 1), mostly utility. Core file core/console.py (PageRank 0.0326, imported by 64 files): ANSI color constants and console output helpers. Key abstractions: colors_enabled, format_line, print_error, print_msg, print_warn, print_succ. Depends on cli/commands (47), modules: lazyc2 (21), cli (10). Used by cli/commands (33), cli (20), modules: autonomous_daemon (19).

- `core/console.py` ranks 1 by PageRank, 64 importers, 11 symbols: ANSI color constants and console output helpers.
- `core/payload_schema.py` ranks 2 by PageRank, 12 importers, 27 symbols: Declarative schema and validation for ``payload.json``.
- `modules/llm_factory.py` ranks 3 by PageRank, 27 importers, 22 symbols: LLM backend factory and selection utilities.
- Hotspot `static/js/quill-2.0.3.js`: 124 symbols, 3449 connections (score 0.31).
- Hotspot `tests/test_aci_planner.py`: 95 symbols, 85 connections (score 0.06).
- Taint: 4 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _run_single_search).
- Key entities: sym:core/console.py::print_msg@143, sym:core/console.py::print_error@137, sym:core/console.py::print_warn@149, file:tests/test_aci_planner.py, file:static/js/quill-2.0.3.js, file:tests/test_payload_schema.py, file:lazy_sentinel4.py, file:cli/wizard.py
- Rating 3.6/10 = 7 x PageRank share 0.52 + 3 x risk 0.00. Internal imports: 208.

## unassigned files (`c22`, community, rating 3.4)

210 files under modules (py 109, sh 56, lua 26, c 11, js 4, asm 1, cpp 1, cs 1, php 1), mostly utility. Core file .claude/skills/run-lazyown/driver.sh (PageRank 0.0005, imported by 0 files): Build and drive LazyOwn inside its Docker sandbox (Debian container). Key abstractions: increment_version, update_section_html, get_commit_type, usage, log, fail.

- `.claude/skills/run-lazyown/driver.sh` ranks 1 by PageRank, 0 importers, 0 symbols: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- `DEPLOY.sh` ranks 2 by PageRank, 0 importers, 3 symbols: update_section_html: Función para actualizar una sección específica
- `__init__.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `skills/mcp_generated_tools.py`: 645 symbols, 2 connections (score 0.37).
- Hotspot `static/js/select2-4.1.0.min.js`: 3 symbols, 1193 connections (score 0.08).
- Dataflow: 8 INFERRED issues (first: UNCHECKED_ALLOC in exploit).
- Key entities: file:skills/mcp_generated_tools.py, file:modules/rootkit/mrhyde3.c, file:tests/test_packaging.py, file:tests/test_attack_surface_addons.py, file:tests/test_blacksandbeacon_addon.py, file:modules/rootkit/mrhyde.c, file:modules/rootkit/mr.c, file:modules/rootkit/mrhyde2.c
- Rating 3.4/10 = 7 x PageRank share 0.49 + 3 x risk 0.00. Internal imports: 0.

## cli (`c3`, community, rating 2.7)

85 files under cli (py 85), mostly utility. Core file cli/themes.py (PageRank 0.0053, imported by 17 files): Theme registry for the LazyOwn TUI surfaces. Key abstractions: Theme, get_theme, theme_from_payload, LazyOwnShell, log_command, default. Depends on cli/commands (28), modules: quill-2.0.3 (20), modules: lazyc2 (17). Used by cli/commands (39), modules: autonomous_daemon (24), modules: quill-2.0.3 (10).

- `cli/themes.py` ranks 1 by PageRank, 17 importers, 3 symbols: Theme registry for the LazyOwn TUI surfaces.
- `lazyown.py` ranks 2 by PageRank, 9 importers, 127 symbols: lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date: 13/08/2024 License: GPL v3  Description: This file contains the definition of the logic in the LazyOwnShell class  ██╗      █████╗ ███████╗██╗   ██╗...
- `core/text_utils.py` ranks 3 by PageRank, 8 importers, 1 symbols: Shared text helpers for terminal surfaces.
- Hotspot `tests/test_command_palette.py`: 238 symbols, 220 connections (score 0.15).
- Hotspot `lazyown.py`: 127 symbols, 187 connections (score 0.09).
- 1 layer violations, e.g. test_exploration_and_addons.py (testing) -> exploration_view.py (presentation).
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in _emit_event).
- Key entities: file:tests/test_command_palette.py, file:lazyown.py, file:cli/dashboard_tui.py, file:tests/test_tips_engine.py, file:cli/cli_enhancements.py, file:cli/status_bar.py, file:cli/tips_engine.py, file:cli/palette_command.py
- Rating 2.7/10 = 7 x PageRank share 0.39 + 3 x risk 0.00. Internal imports: 313.

## lazygui/panels (`c5`, community, rating 1.8)

54 files under lazygui/panels (py 54), mostly utility. Core file lazygui/config/constants.py (PageRank 0.0087, imported by 34 files): Immutable application constants. Key abstractions: WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants, KeybindingConstants. Depends on modules: lazyc2 (6), modules: autonomous_daemon (2), modules: world_model (1). Used by cli/commands (3).

- `lazygui/config/constants.py` ranks 1 by PageRank, 34 importers, 14 symbols: Immutable application constants.
- `lazygui/services/models.py` ranks 2 by PageRank, 20 importers, 15 symbols: Immutable domain types consumed by the UI.
- `lazygui/theme/tokens.py` ranks 3 by PageRank, 11 importers, 1 symbols: Design tokens describing a single theme.
- Hotspot `tests/test_lazygui_backend.py`: 59 symbols, 13 connections (score 0.03).
- Hotspot `tests/test_lazygui_graph_widget.py`: 51 symbols, 11 connections (score 0.03).
- 1 layer violations, e.g. test_lazygui_graph_widget.py (testing) -> graph_view.py (presentation).
- Key entities: sym:lazygui/services/event_log.py::extend@42, file:tests/test_lazygui_models.py, file:tests/test_lazygui_backend.py, file:tests/test_lazygui_graph_widget.py, file:lazygui/services/teamserver_backend.py, file:lazygui/widgets/graph_view.py, file:lazygui/services/backend.py, file:lazygui/windows/main_window.py
- Rating 1.8/10 = 7 x PageRank share 0.26 + 3 x risk 0.00. Internal imports: 181.

## modules: world_model (`c6`, community, rating 1.4)

37 files under modules (py 37), mostly utility. Core file modules/world_model.py (PageRank 0.0105, imported by 75 files): modules/world_model.py Key abstractions: HostState, EngagementPhase, ServiceInfo, CredentialEntry, VulnerabilityEntry, EmailEntry. Depends on cli/commands (11), modules: autonomous_daemon (10), modules: lazyc2 (6). Used by cli/commands (41), modules: autonomous_daemon (29), modules: lazyc2 (17).

- `modules/world_model.py` ranks 1 by PageRank, 75 importers, 61 symbols: modules/world_model.py
- `modules/killchain.py` ranks 2 by PageRank, 28 importers, 21 symbols: Unified kill-chain — single source of truth consumed by all surfaces.
- `cli/commands/pwn.py` ranks 3 by PageRank, 4 importers, 8 symbols: Autonomous exploitation and LOLBAS command set.
- Hotspot `modules/world_model.py`: 61 symbols, 94 connections (score 0.04).
- Hotspot `cli/ops_commands.py`: 53 symbols, 73 connections (score 0.04).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:modules/world_model.py, file:cli/ops_commands.py, file:tests/test_killchain_unified_v2.py, file:cli/commands/exploit_migrated.py, file:modules/opsec_scorer.py, file:modules/killchain.py, file:tests/test_world_model_extended.py, file:modules/rich_tui.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 85.

## lazyc2/blueprints (`c8`, community, rating 1.1)

26 files under tests (py 24, js 2), mostly utility. Core file modules/lazy_rbac.py (PageRank 0.0072, imported by 20 files): modules/lazy_rbac.py Key abstractions: Role, Permission, RBACUser, RBACStore, TenantConfig, TenantManager. Depends on cli/commands (7), modules: lazyc2 (2), modules: autonomous_daemon (1). Used by modules: lazyc2 (11), cli (10), cli/commands (8).

- `modules/lazy_rbac.py` ranks 1 by PageRank, 20 importers, 86 symbols: modules/lazy_rbac.py
- `modules/cli_auth.py` ranks 2 by PageRank, 18 importers, 18 symbols: CLI authentication module — login against users.json with remember-me.
- `cli/engagement_hooks.py` ranks 3 by PageRank, 82 importers, 32 symbols: Curiosity-driven engagement engine for LazyOwn.
- Hotspot `static/js/socket.io-4.0.0.min.js`: 32 symbols, 857 connections (score 0.08).
- Hotspot `modules/lazy_rbac.py`: 86 symbols, 41 connections (score 0.05).
- Dependency cycle: engagement_hooks.py -> cli_auth.py -> engagement_hooks.py.
- 2 layer violations, e.g. operations.py (presentation) -> storage.py (data_access).
- Taint: 3 paths reach this group via subprocess.
- Key entities: file:modules/lazy_rbac.py, file:tests/test_addon_creator.py, file:tests/test_engagement_and_ping.py, file:lazyc2/addon_creator.py, file:tests/test_engagement_elo_and_methodology.py, file:cli/engagement_hooks.py, file:modules/cli_auth.py, file:tests/test_engagement_command_gate.py
- Rating 1.1/10 = 7 x PageRank share 0.16 + 3 x risk 0.00. Internal imports: 129.

## skills/claude_md_orchestrator (`c7`, community, rating 1.0)

28 files under skills/claude_md_orchestrator (py 27, c 1), mostly utility. Core file skills/claude_md_orchestrator/models.py (PageRank 0.0045, imported by 15 files): Data models for the claude_md_orchestrator skill. Key abstractions: Stage, Severity, Contract, SadPath, Spec, TestSuite. Depends on cli/commands (5), modules: autonomous_daemon (3), modules: quill-2.0.3 (1). Used by modules: lazyc2 (4), cli/commands (3), modules: autonomous_daemon (2).

- `skills/claude_md_orchestrator/models.py` ranks 1 by PageRank, 15 importers, 32 symbols: Data models for the claude_md_orchestrator skill.
- `modules/backdoor/server.c` ranks 2 by PageRank, 10 importers, 1 symbols.
- `skills/claude_md_orchestrator/parser.py` ranks 3 by PageRank, 4 importers, 13 symbols: Parser that turns a CLAUDE.md into actionable contracts.
- Hotspot `skills/claude_md_orchestrator/models.py`: 32 symbols, 23 connections (score 0.02).
- Hotspot `skills/hermes-lazyown/mcp_server.py`: 28 symbols, 26 connections (score 0.02).
- Dependency cycle: utils.py -> parser.py -> models.py -> enum.py -> _base.py -> utils.py.
- Taint: 1 paths reach this group via subprocess.
- Dataflow: 1 INFERRED issues (first: UNCHECKED_ALLOC in main).
- Key entities: file:skills/claude_md_orchestrator/models.py, file:modules/security_sanitizers.py, file:skills/hermes-lazyown/mcp_server.py, file:cli/commands/phishing_wizard.py, file:skills/hermes-lazyown/output_compactor.py, file:skills/claude_md_orchestrator/config.py, file:skills/claude_md_orchestrator/orchestrator.py, file:skills/claude_md_orchestrator/validators.py
- Rating 1.0/10 = 7 x PageRank share 0.15 + 3 x risk 0.00. Internal imports: 53.

## modules: lazy_loop (`c9`, community, rating 0.6)

20 files under modules (py 20), mostly utility. Core file modules/lazy_loop.py (PageRank 0.0021, imported by 12 files): Lazy autonomous loop for LazyOwn. Key abstractions: ExplorationNode, ExplorationEdge, AssetNode, LazyTask, AssetGraph, ExplorationGraph. Depends on cli/commands (13), modules: autonomous_daemon (11), modules: quill-2.0.3 (3). Used by modules: lazyc2 (6), modules: autonomous_daemon (3).

- `modules/lazy_loop.py` ranks 1 by PageRank, 12 importers, 263 symbols: Lazy autonomous loop for LazyOwn.
- `modules/osint_enrich.py` ranks 2 by PageRank, 3 importers, 13 symbols: Keyless OSINT enrichment for finding evidence.
- `modules/estorides_fusion.py` ranks 3 by PageRank, 8 importers, 8 symbols: Estorides intel fusion: merge OSINT graph entities into campaign graphs.
- Hotspot `modules/lazy_loop.py`: 263 symbols, 55 connections (score 0.16).
- Hotspot `cli/commands/lazyops.py`: 49 symbols, 81 connections (score 0.03).
- Key entities: file:modules/lazy_loop.py, sym:modules/lazy_loop.py::get@233, file:cli/commands/mcp_bridge.py, file:cli/commands/lazyops.py, file:modules/intel_fusion.py, sym:modules/lazy_loop.py::list@237, file:tests/test_asset_gate.py, sym:modules/lazy_loop.py::ExplorationGraph@349
- Rating 0.6/10 = 7 x PageRank share 0.09 + 3 x risk 0.00. Internal imports: 88.

## modules: kerberos_core (`c10`, community, rating 0.2)

7 files under modules (py 7), mostly utility. Core file modules/kerberos_core.py (PageRank 0.0014, imported by 2 files): Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. Key abstractions: KerberosPrincipal, EncryptedData, KerberosTicket, PACSignature, PACInfo, TGSRequest. Depends on cli/commands (1).

- `modules/kerberos_core.py` ranks 1 by PageRank, 2 importers, 35 symbols: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- `modules/delegation_attacks.py` ranks 2 by PageRank, 2 importers, 12 symbols: Active Directory delegation enumeration and abuse.
- `modules/gpo_abuse.py` ranks 3 by PageRank, 2 importers, 16 symbols: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Hotspot `modules/kerberos_core.py`: 35 symbols, 17 connections (score 0.02).
- Hotspot `modules/kerberos_tickets.py`: 34 symbols, 8 connections (score 0.02).
- Surprising bridge: kerberos_core.py <-> search.py (9 hops across communities).
- Key entities: file:modules/kerberos_core.py, file:modules/kerberos_tickets.py, file:modules/kerberoasting.py, file:modules/gpo_abuse.py, file:modules/dacl_abuse.py, file:modules/delegation_attacks.py, file:cli/commands/active_directory.py, sym:modules/kerberos_tickets.py::forge@134
- Rating 0.2/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 9.

## contrib/legacy (`c14`, community, rating 0.2)

5 files under contrib/legacy (py 5), mostly utility. Core file modules/lazyencoder_decoder.py (PageRank 0.0046, imported by 5 files). Key abstractions: base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution, key_substitution_reverse. Used by cli/commands (1).

- `modules/lazyencoder_decoder.py` ranks 1 by PageRank, 5 importers, 10 symbols.
- `contrib/legacy/lazycreate_webshell.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `contrib/legacy/lazylogpoisoning.py` ranks 3 by PageRank, 0 importers, 3 symbols.
- Hotspot `modules/lazyencoder_decoder.py`: 10 symbols, 6 connections (score 0.01).
- Hotspot `contrib/legacy/lazylogpoisoning.py`: 3 symbols, 7 connections (score 0.00).
- Key entities: file:modules/lazyencoder_decoder.py, file:contrib/legacy/lazylogpoisoning.py, file:contrib/legacy/lazyreversentlmv2.py, sym:modules/lazyencoder_decoder.py::decode_string@94, sym:modules/lazyencoder_decoder.py::encode_string@75, sym:modules/lazyencoder_decoder.py::base64_encode@4, sym:modules/lazyencoder_decoder.py::decode@82, sym:modules/lazyencoder_decoder.py::caesar_cipher@13
- Rating 0.2/10 = 7 x PageRank share 0.03 + 3 x risk 0.00. Internal imports: 4.

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
- Key entities: sym:modules/dotnet_payload.py::compile@403, file:modules/polymorphic_engine.py, file:modules/linux_advanced_payloads.py, file:modules/macos_payloads.py, file:modules/staged_delivery.py, file:modules/dotnet_payload.py, file:cli/commands/payload_arsenal.py, sym:cli/commands/payload_arsenal.py::do_linux_advanced_payload@401
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 8.

## static/js (`c13`, community, rating 0.1)

5 files under static/js (py 3, js 2), mostly utility. Core file cli/style.py (PageRank 0.0013, imported by 10 files): Centralised TUI style tokens for the LazyOwn operator surface. Key abstractions: style, active_tokens, paint, render_prompt, e, p. Depends on cli/commands (3), cli (1). Used by cli/commands (3), modules: quill-2.0.3 (1).

- `cli/style.py` ranks 1 by PageRank, 10 importers, 4 symbols: Centralised TUI style tokens for the LazyOwn operator surface.
- `modules/search.py` ranks 2 by PageRank, 9 importers, 0 symbols: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: webscrapper gtofbins  ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗ ██║...
- `lazyc2/state.py` ranks 3 by PageRank, 1 importers, 0 symbols: Global C2 server state — namespace for shared mutable objects.
- Hotspot `static/js/jquery-3.5.1.slim.min.js`: 6 symbols, 1254 connections (score 0.09).
- Hotspot `static/js/showdown-2.1.0.min.js`: 5 symbols, 747 connections (score 0.05).
- Surprising bridge: __init__.py <-> search.py (9 hops across communities).
- Key entities: file:static/js/jquery-3.5.1.slim.min.js, file:cli/style.py, file:static/js/showdown-2.1.0.min.js, sym:cli/style.py::style@49, file:modules/search.py, file:lazyc2/state.py, sym:cli/style.py::active_tokens@68, sym:cli/style.py::paint@84
- Rating 0.1/10 = 7 x PageRank share 0.02 + 3 x risk 0.00. Internal imports: 16.

## scripts: journal (`c15`, community, rating 0.1)

3 files under scripts (py 3), mostly utility. Core file scripts/journal.py (PageRank 0.0013, imported by 2 files): Read-before-you-write journal over GitHub Discussions. Key abstractions: JournalError, JournalConfig, Journal, from_git_remote, repo_id, category_id.

- `scripts/journal.py` ranks 1 by PageRank, 2 importers, 14 symbols: Read-before-you-write journal over GitHub Discussions.
- `scripts/read_journal.py` ranks 2 by PageRank, 0 importers, 2 symbols: Print the recent engineering journal before a change is written.
- `tests/test_journal.py` ranks 3 by PageRank, 0 importers, 10 symbols: Tests for the GitHub Discussions engineering journal.
- Hotspot `scripts/journal.py`: 14 symbols, 10 connections (score 0.01).
- Hotspot `tests/test_journal.py`: 10 symbols, 5 connections (score 0.01).
- Key entities: sym:scripts/journal.py::post@206, file:scripts/journal.py, file:tests/test_journal.py, file:scripts/read_journal.py, sym:scripts/journal.py::_graphql@163, sym:scripts/journal.py::from_git_remote@71, sym:scripts/journal.py::Journal@149, sym:scripts/journal.py::JournalError@48
- Rating 0.1/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 2.

## modules/backdoor (`c16`, community, rating 0.0)

2 files under modules/backdoor (c 1, h 1), mostly utility. Core file modules/backdoor/keylogger.h (PageRank 0.0009, imported by 1 files). Key abstractions: logg, bzero, bootRun, str_cut, Shell, WinMain.

- `modules/backdoor/keylogger.h` ranks 1 by PageRank, 1 importers, 1 symbols.
- `modules/backdoor/backdoor.c` ranks 2 by PageRank, 0 importers, 5 symbols.
- Hotspot `modules/backdoor/backdoor.c`: 5 symbols, 13 connections (score 0.00).
- Hotspot `modules/backdoor/keylogger.h`: 1 symbols, 1 connections (score 0.00).
- Dataflow: 3 INFERRED issues (first: UNCHECKED_ALLOC in str_cut).
- Key entities: file:modules/backdoor/backdoor.c, file:modules/backdoor/keylogger.h, sym:modules/backdoor/keylogger.h::logg@1, sym:modules/backdoor/backdoor.c::Shell@84, sym:modules/backdoor/backdoor.c::WinMain@125, sym:modules/backdoor/backdoor.c::bootRun@18, sym:modules/backdoor/backdoor.c::bzero@14, sym:modules/backdoor/backdoor.c::str_cut@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## poc_tui (`c17`, community, rating 0.0)

2 files under poc_tui (py 2), mostly infrastructure. Core file poc_tui/config.py (PageRank 0.0009, imported by 1 files): Payload.json configuration manager for the TUI shell. Key abstractions: PayloadConfig, reload, save, get, set, keys.

- `poc_tui/config.py` ranks 1 by PageRank, 1 importers, 11 symbols: Payload.json configuration manager for the TUI shell.
- `poc_tui/plugin_loader.py` ranks 2 by PageRank, 0 importers, 22 symbols: Unified plugin loader — YAML addons, Lua plugins, and .tool files.
- Hotspot `poc_tui/plugin_loader.py`: 22 symbols, 13 connections (score 0.01).
- Hotspot `poc_tui/config.py`: 11 symbols, 6 connections (score 0.01).
- Key entities: sym:poc_tui/config.py::items@44, file:poc_tui/plugin_loader.py, file:poc_tui/config.py, sym:poc_tui/plugin_loader.py::_register_yaml_addon@150, sym:poc_tui/plugin_loader.py::load_all@128, sym:poc_tui/plugin_loader.py::PluginSpec@28, sym:poc_tui/plugin_loader.py::_register_tool@250, sym:poc_tui/plugin_loader.py::_replace_placeholders@40
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: check_contract_manifest (`c18`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/check_contract_manifest.py (PageRank 0.0009, imported by 1 files): Verify that documented contracts still exist on disk. Key abstractions: ManifestConfig, check_manifest, main, test_default_manifest_is_consistent, test_missing_module_reference_is_reported, test_missing_public_import_is_reported.

- `scripts/check_contract_manifest.py` ranks 1 by PageRank, 1 importers, 13 symbols: Verify that documented contracts still exist on disk.
- `tests/test_contract_manifest.py` ranks 2 by PageRank, 0 importers, 4 symbols: Tests for the contract manifest drift checker.
- Hotspot `scripts/check_contract_manifest.py`: 13 symbols, 7 connections (score 0.01).
- Hotspot `tests/test_contract_manifest.py`: 4 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/check_contract_manifest.py, sym:scripts/check_contract_manifest.py::check_manifest@176, file:tests/test_contract_manifest.py, sym:scripts/check_contract_manifest.py::_dotted_symbol_exists@112, sym:scripts/check_contract_manifest.py::ManifestConfig@34, sym:scripts/check_contract_manifest.py::_iter_table_cells@127, sym:tests/test_contract_manifest.py::test_dotted_symbol_exists_uses_ast_not_import@47, sym:tests/test_contract_manifest.py::test_missing_module_reference_is_reported@24
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## scripts: migrate_lazyown (`c19`, community, rating 0.0)

2 files under scripts (py 2), mostly testing. Core file scripts/migrate_lazyown.py (PageRank 0.0009, imported by 1 files): Staged migration script: extract do_* methods from lazyown.py into cli/commands/. Key abstractions: extract_method, rewrite_globals, build_migrated_module, main, test_generated_module_parses, test_all_is_static_and_matches_class_name.

- `scripts/migrate_lazyown.py` ranks 1 by PageRank, 1 importers, 6 symbols: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- `tests/test_migrate_lazyown_generator.py` ranks 2 by PageRank, 0 importers, 6 symbols: Regression guard for the ``cli/commands`` migration generator.
- Hotspot `scripts/migrate_lazyown.py`: 6 symbols, 6 connections (score 0.00).
- Hotspot `tests/test_migrate_lazyown_generator.py`: 6 symbols, 4 connections (score 0.00).
- Key entities: file:scripts/migrate_lazyown.py, file:tests/test_migrate_lazyown_generator.py, sym:scripts/migrate_lazyown.py::build_migrated_module@124, sym:scripts/migrate_lazyown.py::main@173, sym:tests/test_migrate_lazyown_generator.py::_module_all@27, sym:tests/test_migrate_lazyown_generator.py::test_all_is_static_and_matches_class_name@62, sym:tests/test_migrate_lazyown_generator.py::test_compound_phase_title_casing@68, sym:scripts/migrate_lazyown.py::rewrite_globals@96
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## test (`c20`, community, rating 0.0)

2 files under test (py 2), mostly infrastructure. Core file test/config.py (PageRank 0.0009, imported by 1 files): o config.py Key abstractions: encrypt_data, decrypt_data, send_command_via_web, get_encrypted_command, post_result, test_migrate.

- `test/config.py` ranks 1 by PageRank, 1 importers, 2 symbols: o config.py
- `test/test_commands.py` ranks 2 by PageRank, 0 importers, 15 symbols: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- Hotspot `test/test_commands.py`: 15 symbols, 7 connections (score 0.01).
- Hotspot `test/config.py`: 2 symbols, 5 connections (score 0.00).
- Key entities: file:test/test_commands.py, sym:test/test_commands.py::post_result@59, sym:test/test_commands.py::send_command_via_web@36, file:test/config.py, sym:test/test_commands.py::test_download@138, sym:test/test_commands.py::test_discover@110, sym:test/test_commands.py::test_migrate@79, sym:test/test_commands.py::test_persistence@176
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.

## tools (`c21`, community, rating 0.0)

2 files under tools (py 2), mostly utility. Core file tools/gen_demo_gifs.py (PageRank 0.0009, imported by 1 files): Generate LazyOwn demo GIFs without external services. Key abstractions: font, render, main, main.

- `tools/gen_demo_gifs.py` ranks 1 by PageRank, 1 importers, 3 symbols: Generate LazyOwn demo GIFs without external services.
- `tools/gen_demo_gifs_extra.py` ranks 2 by PageRank, 0 importers, 1 symbols: Additional LazyOwn demo GIFs.
- Hotspot `tools/gen_demo_gifs.py`: 3 symbols, 3 connections (score 0.00).
- Hotspot `tools/gen_demo_gifs_extra.py`: 1 symbols, 4 connections (score 0.00).
- Key entities: file:tools/gen_demo_gifs.py, file:tools/gen_demo_gifs_extra.py, sym:tools/gen_demo_gifs.py::font@14, sym:tools/gen_demo_gifs.py::render@22, sym:tools/gen_demo_gifs.py::main@70, sym:tools/gen_demo_gifs_extra.py::main@49
- Rating 0.0/10 = 7 x PageRank share 0.01 + 3 x risk 0.00. Internal imports: 1.
