# skills/mcp_tools

*Community 0 | 226 files | cohesion 0.62*

## Definition

This community groups 226 file(s) rooted at `skills/mcp_tools` with dominant language py (cohesion 0.62). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AVBlockedMatcher`, `AbstractReader`, `AbstractSelector`. Core file: `skills/mcp_generated_tools.py` (645 symbols). Documented purpose: Phase-scoped CommandSet modules.  Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping commands that share a kill-chain phase or attack do.

## Files

### `skills/mcp_tools` (144 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/__init__.py` | py | utility | 5 | yes |
| `skills/mcp_tools/_context.py` | py | utility | 1 | yes |
| `skills/mcp_tools/aci_plan.py` | py | utility | 1 | yes |

### `tests` (27 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aci_planner.py` | py | testing | 95 | yes |
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |
| `tests/test_boyscout_contracts.py` | py | testing | 15 | yes |

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/asset_graph.py` | py | utility | 1 | yes |
| `modules/atomic_enricher.py` | py | utility | 9 | yes |
| `modules/cve_matcher.py` | py | utility | 12 | yes |

### `skills` (21 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/autonomous_daemon.py` | py | utility | 140 | yes |
| `skills/autonomous_replay.py` | py | utility | 19 | yes |

### `skills/tests` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 91 | yes |
| `skills/tests/test_hive_mind.py` | py | testing | 95 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/exploitgym.py` | py | utility | 10 | yes |

### `modules/loop` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/loop/objective_bootstrap.py` | py | infrastructure | 2 | yes |
| `modules/loop/target_os.py` | py | utility | 3 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/graph_advisor.py` | py | utility | 52 | yes |

### `scripts` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/lazy_opencode_config.py` | py | infrastructure | 6 | yes |

*... and 206 more files in this community.*


## Key Symbols

- `ExploitGymCommandSet` (class, `cli/commands/exploitgym.py:36`) `class ExploitGymCommandSet(LazyOwnCommandSet)` - ExploitGym — realistic vulnerability-to-exploit benchmark tasks.
- `do_exploitgym` (method, `cli/commands/exploitgym.py:43`) `def do_exploitgym(self, line)` - ExploitGym — real-world exploit benchmark via containerised tasks.
- `_egym_status` (method, `cli/commands/exploitgym.py:90`) `def _egym_status(self, _args)` - Show ExploitGym harness readiness.
- `_egym_setup` (method, `cli/commands/exploitgym.py:120`) `def _egym_setup(self, args)` - Automate the ExploitGym harness installation.
- `_egym_list` (method, `cli/commands/exploitgym.py:149`) `def _egym_list(self, args)` - List ExploitGym tasks, optionally filtered by domain.
- `_egym_pull` (method, `cli/commands/exploitgym.py:181`) `def _egym_pull(self, args)` - Pull the Docker image for a task.
- `_egym_run` (method, `cli/commands/exploitgym.py:198`) `def _egym_run(self, args)` - Run the agent against an ExploitGym task.
- `_egym_verify` (method, `cli/commands/exploitgym.py:245`) `def _egym_verify(self, args)` - Verify a captured flag on record for a task.
- `_egym_score` (method, `cli/commands/exploitgym.py:258`) `def _egym_score(self, args)` - Award Red Team Gym ELO for a task outcome.
- `_egym_docs` (method, `cli/commands/exploitgym.py:289`) `def _egym_docs(self, _args)` - Print the ExploitGym evaluation documentation link.
- `GraphAdvisorConfig` (class, `cli/graph_advisor.py:50`) `class GraphAdvisorConfig` - Centralised constants for the graph advisor.
- `GraphNode` (class, `cli/graph_advisor.py:98`) `class GraphNode` - Immutable view onto a node loaded from the graphify JSON.
- `to_summary` (method, `cli/graph_advisor.py:109`) `def to_summary(self)` - Return a small, JSON-safe summary suitable for MCP responses.
- `GraphEdge` (class, `cli/graph_advisor.py:122`) `class GraphEdge` - Immutable view onto an edge loaded from the graphify JSON.
- `to_summary` (method, `cli/graph_advisor.py:132`) `def to_summary(self)`
- `ScoredNode` (class, `cli/graph_advisor.py:143`) `class ScoredNode` - Node plus its score and match position metadata.
- `GraphLoader` (class, `cli/graph_advisor.py:151`) `class GraphLoader` - Load a graphify JSON file with per-process ``(path, mtime)`` cache.
- `__init__` (method, `cli/graph_advisor.py:156`) `def __init__(self, config)`
- `resolve_path` (method, `cli/graph_advisor.py:160`) `def resolve_path(self, override)` - Resolve which graphify JSON file to load.
- `load` (method, `cli/graph_advisor.py:184`) `def load(self, override)`
- `clear_cache` (method, `cli/graph_advisor.py:207`) `def clear_cache(cls)`
- `GraphIndex` (class, `cli/graph_advisor.py:211`) `class GraphIndex` - In-memory index over a graphify graph for O(1) lookups.
- `__init__` (method, `cli/graph_advisor.py:214`) `def __init__(self, data)`
- `_build` (method, `cli/graph_advisor.py:223`) `def _build(self)`
- `nodes` (method, `cli/graph_advisor.py:277`) `def nodes(self)`
- `get` (method, `cli/graph_advisor.py:280`) `def get(self, node_id)`
- `neighbors` (method, `cli/graph_advisor.py:283`) `def neighbors(self, node_id)`
- `edges_between` (method, `cli/graph_advisor.py:286`) `def edges_between(self, source, target)`
- `community_members` (method, `cli/graph_advisor.py:289`) `def community_members(self, community_id)`
- `degree` (method, `cli/graph_advisor.py:292`) `def degree(self, node_id)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 715
- Cross-boundary resolved imports (EXTRACTED): 312

## Connections

- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/loop/target_os.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/lazy_engine.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` -> `modules/lazy_loop.py`

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` be broken with an interface?
- What would break if the most connected file in skills/mcp_tools changed?
- Should skills/mcp_tools be split, given cohesion 0.62?

## Sources

- `cli/commands/__init__.py`
- `cli/commands/exploitgym.py`
- `cli/graph_advisor.py`
- `modules/asset_graph.py`
- `modules/atomic_enricher.py`
- `modules/cve_matcher.py`
- `modules/detection_feed.py`
- `modules/detection_oracle.py`
- `modules/engage_summary.py`
- `modules/enrich.py`
- `modules/evasion_engine.py`
- `modules/event_engine.py`
- `modules/evidence.py`
- `modules/exploitgym_gym.py`
- `modules/golden_path.py`
- `modules/lazyown_bridge.py`
- `modules/llm_evaluator.py`
- `modules/loop/objective_bootstrap.py`
- `modules/loop/target_os.py`
- `modules/mcp_agent_bridge.py`
- *... and 206 more*
