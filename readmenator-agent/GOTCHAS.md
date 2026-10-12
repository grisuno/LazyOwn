# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `core/logging.py` (score: 243.20, imported by 121 files)
- `utils.py` (score: 210.40, imported by 87 files)
- `cli/commands/_base.py` (score: 182.70, imported by 89 files)
- `skills/lazyown_mcp.py` (score: 179.80, imported by 8 files)
- `modules/lazy_loop.py` (score: 152.00, imported by 38 files)
- `lazyc2.py` (score: 122.40)
- `lazyown.py` (score: 116.90, imported by 8 files)
- `core/console.py` (score: 101.10, imported by 50 files)
- `skills/autonomous_daemon.py` (score: 98.80, imported by 15 files)
- `core/config.py` (score: 87.70, imported by 41 files)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `modules/cli_auth.py` -- 10 direct, 124 total dependents
- `cli/engagement_hooks.py` -- 10 direct, 121 total dependents
- `core/logging.py` -- 50 direct, 121 total dependents
- `core/validators.py` -- 12 direct, 117 total dependents
- `core/hardening.py` -- 18 direct, 112 total dependents
- `core/process.py` -- 12 direct, 102 total dependents
- `skills/claude_md_orchestrator/models.py` -- 11 direct, 101 total dependents
- `skills/claude_md_orchestrator/config.py` -- 10 direct, 100 total dependents
- `cli/banner_config.py` -- 6 direct, 98 total dependents
- `core/parsers.py` -- 9 direct, 96 total dependents

## Hotspots (complexity + centrality)

- `static/js/html2pdf.bundle.min.js` -- complexity: 1.0, centrality: 0.6, combined: 0.8
- `static/js/3d-force-graph-1.73.4.min.js` -- complexity: 0.2, centrality: 1.0, combined: 0.7
- `skills/mcp_generated_tools.py` -- complexity: 0.9, centrality: 0.0, combined: 0.3
- `static/js/vis-network-9.1.2.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/vis-network.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/xterm.js` -- complexity: 0.1, centrality: 0.5, combined: 0.3
- `static/js/quill-2.0.3.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `modules/lazy_loop.py` -- complexity: 0.6, centrality: 0.0, combined: 0.3
- `static/js/chart.min.js` -- complexity: 0.1, centrality: 0.3, combined: 0.3
- `lazyc2.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2

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
- `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`

## Layer Violations

- `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access): presentation must not import data_access
- `tests/integration_autonomous_flow.py` (testing) -> `modules/moe_router.py` (presentation): testing must not import presentation
- `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation

## Dataflow Issues (INFERRED, review each lead)

- `banner.py:29` `image_to_bash` [UNCHECKED_ALLOC] `img`: Result of allocator stored in `img` is never checked against NULL.
- `cli/auto_crypto.py:272` `_load_or_create_salt` [UNCHECKED_ALLOC] `fd`: Result of allocator stored in `fd` is never checked against NULL.
- `cli/commands/dns_exfil.py:117` `do_dns_exfil_listen` [UNCHECKED_ALLOC] `sock`: Result of allocator stored in `sock` is never checked against NULL.
- `cli/commands/evasive_payload.py:648` `_apply_bypass` [UNCHECKED_ALLOC] `s`: Result of allocator stored in `s` is never checked against NULL.
- `cli/commands/exfiltration.py:1382` `do_exfil_dns` [UNCHECKED_ALLOC] `data`: Result of allocator stored in `data` is never checked against NULL.
- `cli/commands/exfiltration.py:1449` `do_exfil_http` [UNCHECKED_ALLOC] `file_hash`: Result of allocator stored in `file_hash` is never checked against NULL.
- `cli/commands/exfiltration.py:1578` `do_stage` [UNCHECKED_ALLOC] `data`: Result of allocator stored in `data` is never checked against NULL.
- `cli/commands/misc_migrated.py:333` `do_suggest_next` [UNCHECKED_ALLOC] `_idx`: Result of allocator stored in `_idx` is never checked against NULL.
- `cli/commands/persist_migrated.py:1186` `do_knokknok` [UNCHECKED_ALLOC] `client_socket`: Result of allocator stored in `client_socket` is never checked against NULL.
- `cli/commands/postexp_migrated.py:2599` `do_aes_pe` [UNCHECKED_ALLOC] `file`: Result of allocator stored in `file` is never checked against NULL.
