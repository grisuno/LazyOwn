# skills/mcp_tools

*Community 0 | 206 files | cohesion 0.63*

## Definition

This community groups 206 file(s) rooted at `skills/mcp_tools` with dominant language py (cohesion 0.63). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AVBlockedMatcher`, `AbstractReader`, `AbstractSelector`. Core file: `skills/autonomous_daemon.py` (142 symbols). Documented purpose: ExploitGym CLI command set — real-world exploit benchmark harness.  Wraps the sunblaze-ucb/exploitgym benchmark (userspace, V8, Linux kernel tasks) behind LazyO.

## Files

### `skills/mcp_tools` (143 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/__init__.py` | py | utility | 5 | yes |
| `skills/mcp_tools/_context.py` | py | utility | 1 | yes |
| `skills/mcp_tools/aci_plan.py` | py | utility | 1 | yes |
| `skills/mcp_tools/aci_replan.py` | py | utility | 1 | yes |

### `skills` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/autonomous_daemon.py` | py | utility | 142 | yes |
| `skills/autonomous_replay.py` | py | utility | 19 | yes |
| `skills/daemon_control.py` | py | utility | 27 | yes |

### `tests` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aci_planner.py` | py | testing | 95 | yes |
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |
| `tests/test_boyscout_contracts.py` | py | testing | 15 | yes |
| `tests/test_bridge_catalog_filtered.py` | py | testing | 20 | yes |

### `modules` (18 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/asset_graph.py` | py | utility | 1 | yes |
| `modules/atomic_enricher.py` | py | utility | 9 | yes |
| `modules/cve_matcher.py` | py | utility | 12 | yes |

### `skills/tests` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 91 | yes |
| `skills/tests/test_hive_mind.py` | py | testing | 95 | yes |
| `skills/tests/test_mcp_smoke.py` | py | testing | 5 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/exploitgym.py` | py | utility | 10 | yes |

### `scripts` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/lazy_opencode_config.py` | py | infrastructure | 6 | yes |

*... and 186 more files in this community.*


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
- `coverage_for` (function, `modules/asset_graph.py:12`) `def coverage_for(db, workspace_id, scope)` - Report tested scope assets versus total scope from the campaign db.
- `_parse_platforms` (function, `modules/atomic_enricher.py:122`) `def _parse_platforms(raw)` - Convert numpy array / list / string platform field → sorted list.
- `_parse_scope` (function, `modules/atomic_enricher.py:135`) `def _parse_scope(name)`
- `_parse_complexity` (function, `modules/atomic_enricher.py:142`) `def _parse_complexity(command)`
- `_parse_keyword_tags` (function, `modules/atomic_enricher.py:152`) `def _parse_keyword_tags(name, description)`
- `_tactic_prefix` (function, `modules/atomic_enricher.py:164`) `def _tactic_prefix(mitre_id)`
- `enrich` (function, `modules/atomic_enricher.py:173`) `def enrich(force)` - Build enriched parquet.  Skips if DST_PARQUET already exists (use force=True to rebuild).
- `_to_pylist` (function, `modules/atomic_enricher.py:204`) `def _to_pylist(val)` - Normalise numpy array / list / None → plain Python list of strings.
- `load_enriched` (function, `modules/atomic_enricher.py:215`) `def load_enriched()` - Load enriched parquet, building it first if it doesn't exist.
- `query_atomic` (function, `modules/atomic_enricher.py:232`) `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, li` - Structured query over the enriched Atomic Red Team technique catalogue.
- `CVEResult` (class, `modules/cve_matcher.py:51`) `class CVEResult`
- `CVEMatcher` (class, `modules/cve_matcher.py:60`) `class CVEMatcher` - Lookup CVEs for a given product/version using the NVD REST API 2.0.
- `__init__` (method, `modules/cve_matcher.py:70`) `def __init__(self, api_key, cache_dir)`
- `search` (method, `modules/cve_matcher.py:82`) `def search(self)` - Search CVEs by product / version keywords.
- `search_by_cpe` (method, `modules/cve_matcher.py:89`) `def search_by_cpe(self, cpe_name, max_results)` - Search CVEs by CPE 2.3 string.
- `_cache_path` (method, `modules/cve_matcher.py:95`) `def _cache_path(self, params)`
- `_load_cache` (method, `modules/cve_matcher.py:100`) `def _load_cache(self, params)`
- `_save_cache` (method, `modules/cve_matcher.py:112`) `def _save_cache(self, params, results)`
- `_rate_limit` (method, `modules/cve_matcher.py:121`) `def _rate_limit(self)`
- `_query` (method, `modules/cve_matcher.py:128`) `def _query(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 640
- Cross-boundary resolved imports (EXTRACTED): 284

## Connections

- [EXTRACTED] depends_on community 7 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
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
- Should skills/mcp_tools be split, given cohesion 0.63?

## Sources

- `cli/commands/exploitgym.py`
- `modules/asset_graph.py`
- `modules/atomic_enricher.py`
- `modules/cve_matcher.py`
- `modules/evasion_engine.py`
- `modules/event_engine.py`
- `modules/exploitgym_gym.py`
- `modules/golden_path.py`
- `modules/lazyown_bridge.py`
- `modules/llm_evaluator.py`
- `modules/mcp_agent_bridge.py`
- `modules/metrics.py`
- `modules/pipeline_engine.py`
- `modules/playbook_executor.py`
- `modules/reactive_engine.py`
- `modules/session_rag.py`
- `modules/session_reader.py`
- `modules/timeline_narrator.py`
- `modules/toolset.py`
- `scripts/lazy_opencode_config.py`
- *... and 186 more*
