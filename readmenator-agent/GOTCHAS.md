# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `core/logging.py` (score: 243.20)
- `utils.py` (score: 178.40)
- `skills/lazyown_mcp.py` (score: 148.10)
- `cli/commands/_base.py` (score: 144.50)
- `lazyown.py` (score: 116.20)
- `lazyc2.py` (score: 114.30)
- `core/console.py` (score: 104.50)
- `cli/commands/misc_migrated.py` (score: 100.10)
- `modules/world_model.py` (score: 84.10)
- `static/js/html2pdf.bundle.min.js` (score: 75.50)

## Hotspots (complexity + centrality)

- `static/js/html2pdf.bundle.min.js` -- complexity: 1.0, centrality: 1.0, combined: 1.0
- `static/js/vis-network-9.1.2.min.js` -- complexity: 0.2, centrality: 0.8, combined: 0.6
- `static/js/vis-network.min.js` -- complexity: 0.2, centrality: 0.8, combined: 0.6
- `static/js/xterm.js` -- complexity: 0.1, centrality: 0.6, combined: 0.4
- `static/js/quill-2.0.3.js` -- complexity: 0.2, centrality: 0.6, combined: 0.4
- `skills/mcp_generated_tools.py` -- complexity: 0.9, centrality: 0.0, combined: 0.4
- `static/js/chart.min.js` -- complexity: 0.1, centrality: 0.5, combined: 0.3
- `lazyc2.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `mutants/tests/test_command_palette.py` -- complexity: 0.3, centrality: 0.0, combined: 0.2
- `tests/test_command_palette.py` -- complexity: 0.3, centrality: 0.0, combined: 0.2

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py`
- `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py`
- `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py`
- `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py`
- `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py`
- `lazyc2/blueprints/__init__.py` -> `lazyc2/blueprints/auth.py` -> `lazyc2.py`

## Layer Violations

- `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access): presentation must not import data_access
- `mutants/tests/integration_autonomous_flow.py` (testing) -> `modules/moe_router.py` (presentation): testing must not import presentation
- `mutants/tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
- `mutants/tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation): testing must not import presentation
