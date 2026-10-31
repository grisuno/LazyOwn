# modules: autonomous_daemon

*Community 8 | 42 files | cohesion 0.49*

## Definition

This community groups 42 file(s) rooted at `tests` with dominant language py (cohesion 0.49). Central symbols: `ActionCategory`, `ActionDecision`, `AdversarySelector`, `Anchor`, `ApprovalDecision`, `ApprovalGate`, `ApprovalOutcome`, `ApprovalRequest`. Core file: `skills/autonomous_daemon.py` (157 symbols). Documented purpose: Global asset truth store joined to per-task exploration chains.  Ports the LAZY dual-graph contract. Asset nodes deduplicate by a computed key. Exploration node.

## Files

### `tests` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |
| `tests/test_chain_selector.py` | py | testing | 12 | yes |
| `tests/test_daemon_control.py` | py | testing | 29 | yes |
| `tests/test_detection_dampening.py` | py | testing | 5 | yes |
| `tests/test_detection_feed.py` | py | testing | 19 | yes |

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/asset_graph.py` | py | utility | 17 | yes |
| `modules/chain_match.py` | py | utility | 7 | yes |
| `modules/detection_feed.py` | py | utility | 13 | yes |
| `modules/detection_oracle.py` | py | utility | 18 | yes |
| `modules/engage_summary.py` | py | utility | 8 | yes |

### `modules/selection` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/selection/__init__.py` | py | utility | 0 | yes |
| `modules/selection/adversary.py` | py | utility | 6 | yes |
| `modules/selection/atomic.py` | py | utility | 2 | yes |
| `modules/selection/base.py` | py | utility | 4 | yes |
| `modules/selection/chain.py` | py | utility | 3 | yes |

### `skills` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/autonomous_daemon.py` | py | utility | 157 | yes |
| `skills/autonomous_replay.py` | py | utility | 19 | yes |
| `skills/daemon_control.py` | py | utility | 27 | yes |
| `skills/lazyown_policy.py` | py | business_logic | 126 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |

*... and 22 more files in this community.*


## Key Symbols

- `GraphConfig` (class, `modules/asset_graph.py:17`) `class GraphConfig` - Centralized constants for graph behavior.
- `asset_key` (function, `modules/asset_graph.py:28`) `def asset_key(asset_type, value, parent_key)` - Compute the stable deduplication key for an asset.
- `AssetNode` (class, `modules/asset_graph.py:36`) `class AssetNode` - Single truth asset in the global graph.
- `ExplorationNode` (class, `modules/asset_graph.py:50`) `class ExplorationNode` - Single step in a task exploration chain.
- `Anchor` (class, `modules/asset_graph.py:63`) `class Anchor` - Join between an exploration node and an asset node.
- `AssetGraph` (class, `modules/asset_graph.py:70`) `class AssetGraph` - Thread-safe dual graph with bidirectional anchor lookup.
- `__init__` (method, `modules/asset_graph.py:73`) `def __init__(self, config)` - Initialize empty graphs and anchor indexes.
- `upsert_asset` (method, `modules/asset_graph.py:82`) `def upsert_asset(self, asset_type, value, parent_key, company)` - Insert or refresh an asset and return the canonical node.
- `add_node` (method, `modules/asset_graph.py:108`) `def add_node(self, task_id, kind, text, parent_id, payload)` - Append an exploration node to a task chain.
- `add_fact` (method, `modules/asset_graph.py:123`) `def add_fact(self, task_id, text, parent_id, payload)` - Append a fact node to a task chain.
- `add_finding` (method, `modules/asset_graph.py:128`) `def add_finding(self, task_id, text, parent_id, payload)` - Append a finding node to a task chain.
- `anchor` (method, `modules/asset_graph.py:133`) `def anchor(self, exploration_id, key)` - Link an exploration node to an asset key.
- `assets_for_node` (method, `modules/asset_graph.py:145`) `def assets_for_node(self, exploration_id)` - List assets anchored to one exploration node.
- `nodes_for_asset` (method, `modules/asset_graph.py:151`) `def nodes_for_asset(self, key)` - List exploration nodes anchored to one asset.
- `coverage` (method, `modules/asset_graph.py:157`) `def coverage(self, task_id)` - Report tested versus total assets for a task.
- `mirror_to_campaign` (method, `modules/asset_graph.py:170`) `def mirror_to_campaign(self, db, world_model, workspace_id)` - Mirror graph assets into the campaign database and world model.
- `coverage_for` (function, `modules/asset_graph.py:214`) `def coverage_for(db, workspace_id, scope)` - Report tested scope assets versus total scope from the campaign db.
- `normalize_tags` (function, `modules/chain_match.py:49`) `def normalize_tags(tags)` - Return a chain's tags lowercased and aliased to the shared vocabulary.
- `service_tokens` (function, `modules/chain_match.py:65`) `def service_tokens(services)` - Normalise discovered service names into the chain tag vocabulary.
- `platform_ok` (function, `modules/chain_match.py:75`) `def platform_ok(platforms, os_hint)` - Return True when a chain's platforms admit the target OS hint.
- `score` (function, `modules/chain_match.py:86`) `def score(tags, phase, svc_tokens)` - Score one chain's tags for the phase and discovered services.
- `reset_cache` (function, `modules/chain_match.py:101`) `def reset_cache()` - Clear the process-wide registry scan cache (tests, long-lived loops).
- `load_rows` (function, `modules/chain_match.py:109`) `def load_rows(allow_lab, ttl)` - Return enabled, valid, non-lab chain rows, cached for the TTL.
- `best_chain` (function, `modules/chain_match.py:139`) `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` - Return the ``(name, reason)`` of the best matching chain, or None.
- `FeedResult` (class, `modules/detection_feed.py:64`) `class FeedResult` - Result of a feed update operation.
- `DetectionFeed` (class, `modules/detection_feed.py:73`) `class DetectionFeed` - Fetches and adjusts detection rules from external sources.
- `__init__` (method, `modules/detection_feed.py:83`) `def __init__(self, cache_dir, sources)`
- `update_rules` (method, `modules/detection_feed.py:92`) `def update_rules(self, source)` - Download and parse rules from the given source.
- `_parse_sigma_feed` (method, `modules/detection_feed.py:125`) `def _parse_sigma_feed(self, text)` - Parse raw Sigma YAML text into SigmaRule objects.
- `_extract_log_source` (method, `modules/detection_feed.py:172`) `def _extract_log_source(self, doc)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 230
- Cross-boundary resolved imports (EXTRACTED): 181

## Connections

- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/daemon_ctl.py imports skills/daemon_control.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/sinks/findings.py` -> `modules/orchestrator_config.py`
- [cycle] `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/orchestrator_config.py`
- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/swan_agent.py` -> `skills/hive_mind.py`
- [cycle] `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/swan_agent.py` -> `skills/lazyown_groq_agents.py`
- [cycle] `modules/detection_oracle.py` -> `modules/detection_feed.py` -> `modules/detection_oracle.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [layer strict] `tests/integration_autonomous_flow.py` (testing) -> `modules/moe_router.py` (presentation)
- [layer strict] `tests/test_moe_rl_swan.py` (testing) -> `modules/moe_router.py` (presentation)
- [layer strict] `tests/test_moe_rl_swan.py` (testing) -> `modules/moe_router.py` (presentation)

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: autonomous_daemon changed?
- Should modules: autonomous_daemon be split, given cohesion 0.49?

## Sources

- `modules/asset_graph.py`
- `modules/chain_match.py`
- `modules/detection_feed.py`
- `modules/detection_oracle.py`
- `modules/engage_summary.py`
- `modules/enrich.py`
- `modules/evidence.py`
- `modules/goals.py`
- `modules/moe_router.py`
- `modules/rl_trainer.py`
- `modules/selection/__init__.py`
- `modules/selection/adversary.py`
- `modules/selection/atomic.py`
- `modules/selection/base.py`
- `modules/selection/chain.py`
- `modules/selection/cred_spray.py`
- `modules/selection/intel.py`
- `modules/selection/playbook.py`
- `modules/selection/registry.py`
- `modules/toolset.py`
- *... and 22 more*
