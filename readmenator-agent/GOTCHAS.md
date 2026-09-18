# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `core/logging.py` (score: 245.20)
- `utils.py` (score: 186.20)
- `cli/commands/_base.py` (score: 166.70)
- `skills/lazyown_mcp.py` (score: 146.10)
- `lazyown.py` (score: 120.30)
- `lazyc2.py` (score: 114.30)
- `core/console.py` (score: 94.50)
- `static/js/html2pdf.bundle.min.js` (score: 75.50)
- `cli/commands/misc_migrated.py` (score: 75.20)
- `lazygui/config/constants.py` (score: 67.40)

## Hotspots (complexity + centrality)

- `static/js/html2pdf.bundle.min.js` -- complexity: 1.0, centrality: 1.0, combined: 1.0
- `static/js/vis-network-9.1.2.min.js` -- complexity: 0.2, centrality: 0.8, combined: 0.6
- `static/js/vis-network.min.js` -- complexity: 0.2, centrality: 0.8, combined: 0.6
- `static/js/xterm.js` -- complexity: 0.1, centrality: 0.6, combined: 0.4
- `static/js/quill-2.0.3.js` -- complexity: 0.2, centrality: 0.6, combined: 0.4
- `skills/mcp_generated_tools.py` -- complexity: 0.9, centrality: 0.0, combined: 0.4
- `static/js/chart.min.js` -- complexity: 0.1, centrality: 0.5, combined: 0.3
- `lazyc2.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `tests/test_command_palette.py` -- complexity: 0.3, centrality: 0.0, combined: 0.2
- `static/js/bootstrap-5.3.0.bundle.min.js` -- complexity: 0.0, centrality: 0.2, combined: 0.1

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- `lazyc2/blueprints/__init__.py` -> `lazyc2/blueprints/auth.py` -> `lazyc2.py` -> `lazyc2/blueprints/__init__.py`

## Layer Violations

- `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access): presentation must not import data_access
- `poc_tui/test_app.py` (testing) -> `poc_tui/app.py` (presentation): testing must not import presentation
- `skills/lazyown_mcp.py` (presentation) -> `skills/lazyown_automapper.py` (data_access): presentation must not import data_access
- `skills/lazyown_mcp.py` (presentation) -> `modules/memory_store.py` (data_access): presentation must not import data_access
- `skills/lazyown_mcp.py` (presentation) -> `modules/memory_store.py` (data_access): presentation must not import data_access
- `skills/tests/test_autonomous_daemon.py` (testing) -> `skills/autonomous_daemon.py` (presentation): testing must not import presentation
- `skills/tests/test_autonomous_daemon.py` (testing) -> `skills/autonomous_daemon.py` (presentation): testing must not import presentation
- `skills/tests/test_autonomous_daemon.py` (testing) -> `skills/autonomous_daemon.py` (presentation): testing must not import presentation
- `skills/tests/test_autonomous_daemon.py` (testing) -> `skills/autonomous_daemon.py` (presentation): testing must not import presentation
- `skills/tests/test_autonomous_daemon.py` (testing) -> `skills/autonomous_daemon.py` (presentation): testing must not import presentation

## Dataflow Issues (INFERRED, review each lead)

- `banner.py:27` `image_to_bash` [UNCHECKED_ALLOC] `img`: Result of allocator stored in `img` is never checked against NULL.
- `cli/auto_crypto.py:260` `_load_or_create_salt` [UNCHECKED_ALLOC] `fd`: Result of allocator stored in `fd` is never checked against NULL.
- `cli/commands/dns_exfil.py:117` `do_dns_exfil_listen` [UNCHECKED_ALLOC] `sock`: Result of allocator stored in `sock` is never checked against NULL.
- `cli/commands/evasive_payload.py:648` `_apply_bypass` [UNCHECKED_ALLOC] `s`: Result of allocator stored in `s` is never checked against NULL.
- `cli/commands/exfiltration.py:1382` `do_exfil_dns` [UNCHECKED_ALLOC] `data`: Result of allocator stored in `data` is never checked against NULL.
- `cli/commands/exfiltration.py:1449` `do_exfil_http` [UNCHECKED_ALLOC] `file_hash`: Result of allocator stored in `file_hash` is never checked against NULL.
- `cli/commands/exfiltration.py:1578` `do_stage` [UNCHECKED_ALLOC] `data`: Result of allocator stored in `data` is never checked against NULL.
- `cli/commands/misc_migrated.py:342` `do_suggest_next` [UNCHECKED_ALLOC] `_idx`: Result of allocator stored in `_idx` is never checked against NULL.
- `cli/commands/persist_migrated.py:1184` `do_knokknok` [UNCHECKED_ALLOC] `client_socket`: Result of allocator stored in `client_socket` is never checked against NULL.
- `cli/commands/postexp_migrated.py:2272` `do_aes_pe` [UNCHECKED_ALLOC] `file`: Result of allocator stored in `file` is never checked against NULL.
