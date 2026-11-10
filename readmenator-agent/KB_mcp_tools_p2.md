# Subsystem: mcp_tools (page 2 of 4)
Previous: [KB_mcp_tools.md](KB_mcp_tools.md)

## skills/mcp_tools/deploy_beacon.py
- Doc: MCP tool ``lazyown_deploy_beacon`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 40) `def handle(arguments, tool_name, ctx)`
  - `_deploy_beacon_sync` (function, line 45) `def _deploy_beacon_sync()`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/discover_commands.py
- Doc: MCP tool ``lazyown_discover_commands`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 52) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/engage_approve.py
- Doc: MCP tool ``lazyown_engage_approve`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 40) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/engage_list_pending.py
- Doc: MCP tool ``lazyown_engage_list_pending`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 21) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/engage_status.py
- Doc: MCP tool ``lazyown_engage_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 31) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/engage_target.py
- Doc: MCP tool ``lazyown_engage_target`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 57) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/eval_quality.py
- Doc: MCP tool ``lazyown_eval_quality`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 38) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/llm_evaluator.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/evasion_generate.py
- Doc: MCP tool ``lazyown_evasion_generate``: generate a C2 malleable profile.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/evasion_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/evasion_rotate.py
- Doc: MCP tool ``lazyown_evasion_rotate``: rotate to a fresh evasion profile.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 27) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/evasion_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/evidence_grep.py
- Doc: MCP tool ``lazyown_evidence_grep`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 47) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploit_chain.py
- Doc: MCP tool ``lazyown_exploit_chain``: AI-driven multi-step exploit chaining.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploit_recommend.py
- Doc: MCP tool ``lazyown_exploit_recommend``: rank exploits from the world model.
- Layer: utility
- Language: py
- Symbols:
  - `_has_data` (function, line 17) `def _has_data(path)`
  - `handle` (function, line 44) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploitgym_list.py
- Doc: MCP tool ``lazyown_exploitgym_list``: list ExploitGym tasks.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploitgym_run.py
- Doc: MCP tool ``lazyown_exploitgym_run``: run the agent against a task.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 48) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploitgym_score.py
- Doc: MCP tool ``lazyown_exploitgym_score``: award gym ELO for a task outcome.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/exploitgym_status.py
- Doc: MCP tool ``lazyown_exploitgym_status``: report ExploitGym readiness.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/facts_show.py
- Doc: MCP tool ``lazyown_facts_show``: show structured facts from the session.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
  - `_do_facts` (function, line 49) `def _do_facts()`
- Depends on: `skills/lazyown_facts.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/fast_run.py
- Doc: MCP tool ``lazyown_fast_run`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 49) `def handle(arguments, tool_name, ctx)`
  - `_launch` (function, line 89) `def _launch()`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/generate_report.py
- Doc: MCP tool ``lazyown_generate_report`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/get_beacons.py
- Doc: MCP tool ``lazyown_get_beacons``: list connected C2 beacons.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 20) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/get_config.py
- Doc: MCP tool ``lazyown_get_config``: read the current payload.json config.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/get_llm_budget.py
- Doc: MCP tool ``lazyown_get_llm_budget``: read the LLM cost budget status.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `core/llm_budget.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/graph_neighbors.py
- Doc: MCP tool ``lazyown_graph_neighbors`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/graph_search.py
- Doc: MCP tool ``lazyown_graph_search`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/graph_suggest_next.py
- Doc: MCP tool ``lazyown_graph_suggest_next`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 35) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/graph_summary.py
- Doc: MCP tool ``lazyown_graph_summary`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 25) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/groq_agent.py
- Doc: MCP tool ``lazyown_groq_agent`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 70) `def handle(arguments, tool_name, ctx)`
  - `_blocking_run` (function, line 110) `def _blocking_run()`
- Depends on: `skills/lazyown_groq_agents.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/harness_status.py
- Doc: MCP tool ``lazyown_harness_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 23) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/heartbeat_status.py
- Doc: MCP tool ``lazyown_heartbeat_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 20) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_collect.py
- Doc: MCP tool ``lazyown_hive_collect`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_forget.py
- Doc: MCP tool ``lazyown_hive_forget`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 25) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_plan.py
- Doc: MCP tool ``lazyown_hive_plan`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_recall.py
- Doc: MCP tool ``lazyown_hive_recall`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 29) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_recover.py
- Doc: MCP tool ``lazyown_hive_recover`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 31) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_result.py
- Doc: MCP tool ``lazyown_hive_result`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 22) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_spawn.py
- Doc: MCP tool ``lazyown_hive_spawn`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/hive_status.py
- Doc: MCP tool ``lazyown_hive_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 21) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/inject_objective.py
- Doc: MCP tool ``lazyown_inject_objective``: queue a new attack objective.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 52) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/job_status.py
- Doc: MCP tool ``lazyown_job_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_addon.py
- Doc: MCP tool ``lazyown_lazy_addon``: list or match lazyaddon triggers.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 27) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/auto_registry.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_board.py
- Doc: MCP tool ``lazyown_lazy_board``: paginated broadcast board view.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_compact.py
- Doc: MCP tool ``lazyown_lazy_compact``: manage cold-compaction digests.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 35) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_loop.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_delete.py
- Doc: MCP tool ``lazyown_lazy_delete``: soft/hard delete a task intent.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_loop.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_finding.py
- Doc: MCP tool ``lazyown_lazy_finding``: report a finding into the loop engine.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- Imported by: `modules/lazy_mentions.py`

## skills/mcp_tools/lazy_hint.py
- Doc: MCP tool ``lazyown_lazy_hint``: add a hint node to a task.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_intel.py
- Doc: MCP tool ``lazyown_lazy_intel`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 53) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/__init__.py`, `modules/lazy_exposure.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_mention.py
- Doc: MCP tool ``lazyown_lazy_mention``: search mention sources, paginated.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_mentions.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_proxy.py
- Doc: MCP tool ``lazyown_lazy_proxy``: control the lazy-engine proxy.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_status.py
- Doc: MCP tool ``lazyown_lazy_status``: report lazy-bridge status.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 19) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_sync.py
- Doc: MCP tool ``lazyown_lazy_sync``: sync all lazy-bridge sources.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 19) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_trace.py
- Doc: MCP tool ``lazyown_lazy_trace``: search a task activity log.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 29) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazy_workspace.py
- Doc: MCP tool ``lazyown_lazy_workspace``: list/read/write workspace files.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 30) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/__init__.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lazysearch.py
- Doc: MCP tool ``lazyown_lazysearch`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 48) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_search.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_addons.py
- Doc: MCP tool ``lazyown_list_addons`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 20) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_agents.py
- Doc: MCP tool ``lazyown_list_agents`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_event_rules.py
- Doc: MCP tool ``lazyown_list_event_rules`` (migrated from the call_tool dispatch chain).
- Layer: business_logic
- Language: py
- Symbols:
  - `handle` (function, line 25) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_modules.py
- Doc: MCP tool ``lazyown_list_modules``: list modules and scripts in modules/.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 27) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/module_registry.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_params.py
- Doc: MCP tool ``lazyown_list_params`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
- Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_plugins.py
- Doc: MCP tool ``lazyown_list_plugins`` (migrated from the call_tool dispatch chain).
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 17) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_sessions.py
- Doc: MCP tool ``lazyown_list_sessions`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/list_targets.py
- Doc: MCP tool ``lazyown_list_targets`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 30) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`


Next: [KB_mcp_tools_p3.md](KB_mcp_tools_p3.md)
