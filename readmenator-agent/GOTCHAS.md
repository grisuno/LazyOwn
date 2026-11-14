# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `skills/mcp_tools/_context.py` (score: 380.10, imported by 190 files)
- `modules/lazy_loop.py` (score: 348.10, imported by 97 files)
- `core/logging.py` (score: 335.20, imported by 167 files)
- `modules/__init__.py` (score: 298.00, imported by 149 files)
- `utils.py` (score: 270.70, imported by 116 files)
- `cli/commands/_base.py` (score: 226.70, imported by 111 files)
- `modules/world_model.py` (score: 181.00, imported by 82 files)
- `core/config.py` (score: 168.00, imported by 81 files)
- `lazyc2.py` (score: 156.50)
- `skills/autonomous_daemon.py` (score: 134.20, imported by 25 files)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `skills/mcp_tools/_context.py` -- 50 direct, 190 total dependents
- `core/logging.py` -- 50 direct, 167 total dependents
- `modules/__init__.py` -- 50 direct, 149 total dependents
- `skills/lazyown_policy.py` -- 10 direct, 143 total dependents
- `core/process.py` -- 12 direct, 137 total dependents
- `modules/c2_surfaces.py` -- 5 direct, 137 total dependents
- `modules/osint_enrich.py` -- 2 direct, 136 total dependents
- `modules/chain_match.py` -- 5 direct, 135 total dependents
- `modules/finding_lifecycle.py` -- 8 direct, 135 total dependents
- `modules/selection/atomic.py` -- 5 direct, 135 total dependents

## Hotspots (complexity + centrality)

- `static/js/html2pdf.bundle.min.js` -- complexity: 1.0, centrality: 0.6, combined: 0.8
- `static/js/3d-force-graph-1.73.4.min.js` -- complexity: 0.2, centrality: 1.0, combined: 0.7
- `skills/mcp_generated_tools.py` -- complexity: 0.9, centrality: 0.0, combined: 0.3
- `static/js/vis-network-9.1.2.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/vis-network.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/xterm.js` -- complexity: 0.1, centrality: 0.5, combined: 0.3
- `modules/lazy_loop.py` -- complexity: 0.7, centrality: 0.1, combined: 0.3
- `static/js/quill-2.0.3.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/chart.min.js` -- complexity: 0.1, centrality: 0.3, combined: 0.3
- `lazyc2.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `core/config.py`

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
- `cli/commands/persist_migrated.py:1240` `do_knokknok` [UNCHECKED_ALLOC] `client_socket`: Result of allocator stored in `client_socket` is never checked against NULL.
- `cli/commands/postexp_migrated.py:2599` `do_aes_pe` [UNCHECKED_ALLOC] `file`: Result of allocator stored in `file` is never checked against NULL.
