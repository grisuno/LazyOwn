# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `core/logging.py` (score: 317.20, imported by 158 files)
- `utils.py` (score: 244.60, imported by 103 files)
- `modules/lazy_loop.py` (score: 236.70, imported by 60 files)
- `skills/lazyown_mcp.py` (score: 203.50, imported by 8 files)
- `cli/commands/_base.py` (score: 200.70, imported by 98 files)
- `modules/world_model.py` (score: 165.00, imported by 74 files)
- `lazyc2.py` (score: 145.10)
- `modules/__init__.py` (score: 136.00, imported by 68 files)
- `core/config.py` (score: 130.00, imported by 62 files)
- `lazyown.py` (score: 124.40, imported by 9 files)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `core/logging.py` -- 50 direct, 158 total dependents
- `core/crypto.py` -- 11 direct, 132 total dependents
- `skills/claude_md_orchestrator/models.py` -- 11 direct, 119 total dependents
- `skills/claude_md_orchestrator/config.py` -- 10 direct, 117 total dependents
- `modules/backdoor/server.c` -- 13 direct, 116 total dependents
- `cli/engagement_hooks.py` -- 10 direct, 114 total dependents
- `core/process.py` -- 13 direct, 112 total dependents
- `core/parsers.py` -- 9 direct, 109 total dependents
- `core/safe_subprocess.py` -- 6 direct, 109 total dependents
- `modules/lazyencoder_decoder.py` -- 5 direct, 108 total dependents

## Hotspots (complexity + centrality)

- `static/js/html2pdf.bundle.min.js` -- complexity: 1.0, centrality: 0.6, combined: 0.8
- `static/js/3d-force-graph-1.73.4.min.js` -- complexity: 0.2, centrality: 1.0, combined: 0.7
- `skills/mcp_generated_tools.py` -- complexity: 0.9, centrality: 0.0, combined: 0.3
- `static/js/vis-network-9.1.2.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/vis-network.min.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `static/js/xterm.js` -- complexity: 0.1, centrality: 0.5, combined: 0.3
- `static/js/quill-2.0.3.js` -- complexity: 0.2, centrality: 0.4, combined: 0.3
- `modules/lazy_loop.py` -- complexity: 0.6, centrality: 0.1, combined: 0.3
- `static/js/chart.min.js` -- complexity: 0.1, centrality: 0.3, combined: 0.3
- `lazyc2.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`

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
