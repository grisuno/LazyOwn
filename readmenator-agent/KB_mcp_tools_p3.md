# Subsystem: mcp_tools (page 3 of 4)
Previous: [KB_mcp_tools_p2.md](KB_mcp_tools_p2.md)

## skills/mcp_tools/llm_ask.py
- Doc: MCP tool ``lazyown_llm_ask`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 67) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_llm.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/lolbas_list.py
- Doc: MCP tool ``lazyown_lolbas_list``: list LOLBAS techniques from plugins.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/lolbas_use.py
- Doc: MCP tool ``lazyown_lolbas_use``: execute one LOLBAS technique.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 44) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/loop_smoke.py
- Doc: MCP tool ``lazyown_loop_smoke``: single-leg autonomous loop smoke test.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 65) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `modules/loop_limits.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/manage_permissions.py
- Doc: MCP tool ``lazyown_manage_permissions`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 56) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/memory_recall.py
- Doc: MCP tool ``lazyown_memory_recall`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 43) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`, `skills/mcp_tools/memory_store.py`

## skills/mcp_tools/memory_store.py
- Doc: MCP tool ``lazyown_memory_store`` (migrated from the call_tool dispatch chain).
- Layer: data_access
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`
- Imported by: `skills/mcp_tools/memory_recall.py`

## skills/mcp_tools/metrics_summary.py
- Doc: MCP tool ``lazyown_metrics_summary`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 40) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/metrics.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/misp_export.py
- Doc: MCP tool ``lazyown_misp_export`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 38) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/next_objective.py
- Doc: MCP tool ``lazyown_next_objective`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 29) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/opencode_config.py
- Doc: MCP tool ``lazyown_opencode_config``: point opencode/hermes at llama.cpp.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 38) `def handle(arguments, tool_name, ctx)`
- Depends on: `scripts/lazy_opencode_config.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/palette.py
- Doc: MCP tool ``lazyown_palette`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/palette.py`, `cli/palette_command.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/parquet_annotate.py
- Doc: MCP tool ``lazyown_parquet_annotate`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 51) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_parquet_db.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/parquet_query.py
- Doc: MCP tool ``lazyown_parquet_query`` (migrated from the call_tool dispatch chain).
- Layer: data_access
- Language: py
- Symbols:
  - `handle` (function, line 87) `def handle(arguments, tool_name, ctx)`
  - `_run_parquet_query` (function, line 105) `def _run_parquet_query()`
- Depends on: `skills/lazyown_parquet_db.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/phase_guide.py
- Doc: MCP tool ``lazyown_phase_guide`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 64) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/pipeline_list.py
- Doc: MCP tool ``lazyown_pipeline_list`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 18) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/pipeline_run.py
- Doc: MCP tool ``lazyown_pipeline_run`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 46) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/pipeline_status.py
- Doc: MCP tool ``lazyown_pipeline_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/pipeline_validate.py
- Doc: MCP tool ``lazyown_pipeline_validate`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/pivot_status.py
- Doc: MCP tool ``lazyown_pivot_status``: view pivot routes and suggestions.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 27) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/auto_pivot.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/playbook_generate.py
- Doc: MCP tool ``lazyown_playbook_generate`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 52) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/playbook_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/playbook_run.py
- Doc: MCP tool ``lazyown_playbook_run`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `_substitute_playbook_target` (function, line 16) `def _substitute_playbook_target(command, target)`
  - `handle` (function, line 55) `def handle(arguments, tool_name, ctx)`
  - `_mcp_executor` (function, line 94) `def _mcp_executor(command, target)`
- Depends on: `modules/playbook_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/policy_status.py
- Doc: MCP tool ``lazyown_policy_status`` (migrated from the call_tool dispatch chain).
- Layer: business_logic
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/poll_events.py
- Doc: MCP tool ``lazyown_poll_events`` (migrated from the call_tool dispatch chain).
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/rag_index.py
- Doc: MCP tool ``lazyown_rag_index`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/session_rag.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/rag_query.py
- Doc: MCP tool ``lazyown_rag_query`` (migrated from the call_tool dispatch chain).
- Layer: data_access
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/session_rag.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/rea.py
- Doc: MCP tool ``lazyown_rea``: reverse-engineer a local artifact via the REA CLI.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 95) `def handle(arguments, tool_name, ctx)`
  - `_fail` (function, line 107) `def _fail(message, remediation)`
  - `_run_rea` (function, line 181) `def _run_rea()`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/reactive_suggest.py
- Doc: MCP tool ``lazyown_reactive_suggest`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 50) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/reactive_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/read_prompt.py
- Doc: MCP tool ``lazyown_read_prompt`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
  - `_read_prompt` (function, line 46) `def _read_prompt()`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/read_session_file.py
- Doc: MCP tool ``lazyown_read_session_file`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/recommend_next.py
- Doc: MCP tool ``lazyown_recommend_next`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 25) `def handle(arguments, tool_name, ctx)`
  - `_fused_recommendations` (function, line 32) `def _fused_recommendations()`
- Depends on: `cli/recommendation.py`, `cli/recommendation_signals.py`, `modules/recommender.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/rich_tui_snapshot.py
- Doc: MCP tool ``lazyown_rich_tui_snapshot``: non-blocking Rich TUI snapshot.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 30) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/run_agent.py
- Doc: MCP tool ``lazyown_run_agent`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 50) `def handle(arguments, tool_name, ctx)`
  - `_runner` (function, line 68) `def _runner(cmd)`
- Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/run_api.py
- Doc: MCP tool ``lazyown_run_api`` (migrated from the call_tool dispatch chain).
- Layer: presentation
- Language: py
- Symbols:
  - `handle` (function, line 30) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/run_command.py
- Doc: MCP tool ``lazyown_run_command``: execute LazyOwn shell commands.
- Layer: utility
- Language: py
- Symbols:
  - `_publish_command_event` (function, line 61) `def _publish_command_event(command, output, operator, target)`
  - `handle` (function, line 82) `def handle(arguments, tool_name, ctx)`
  - `_run_with_fallback` (function, line 102) `def _run_with_fallback(cmd, to)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/run_command_async.py
- Doc: MCP tool ``lazyown_run_command_async`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/search_tools.py
- Doc: MCP tool ``lazyown_search_tools`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/searchsploit.py
- Doc: MCP tool ``lazyown_searchsploit`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 79) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/session_diff.py
- Doc: MCP tool ``lazyown_session_diff`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/session_init.py
- Doc: MCP tool ``lazyown_session_init`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 59) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/killchain.py`, `modules/lazyown_bridge.py`, `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/session_resume.py
- Doc: MCP tool ``lazyown_session_resume`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_session.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/session_state.py
- Doc: MCP tool ``lazyown_session_state`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/session_status.py
- Doc: MCP tool ``lazyown_session_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 43) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/session_reader.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/set_active_target.py
- Doc: MCP tool ``lazyown_set_active_target`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 35) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/set_config.py
- Doc: MCP tool ``lazyown_set_config``: set one key in payload.json.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
  - `coerce_value` (function, line 46) `def coerce_value(coerce_key, coerce_value_in)`
- Depends on: `core/payload_schema.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/soul.py
- Doc: MCP tool ``lazyown_soul`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 42) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/stealth.py
- Doc: MCP tool ``lazyown_stealth``: toggle stealth mode for later operations.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 35) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/subagent_run.py
- Doc: MCP tool ``lazyown_subagent_run`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 45) `def handle(arguments, tool_name, ctx)`
  - `_isolated_runner` (function, line 86) `def _isolated_runner(cmd)`
- Depends on: `modules/mcp_agent_bridge.py`, `skills/lazyown_session.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/swan_ensemble.py
- Doc: MCP tool ``lazyown_swan_ensemble`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 48) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`

## skills/mcp_tools/swan_route.py
- Doc: MCP tool ``lazyown_swan_route`` (migrated from the call_tool dispatch chain).
- Layer: presentation
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`

## skills/mcp_tools/swan_run.py
- Doc: MCP tool ``lazyown_swan_run`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 45) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`

## skills/mcp_tools/swan_status.py
- Doc: MCP tool ``lazyown_swan_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 23) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`

## skills/mcp_tools/target_context.py
- Doc: MCP tool ``lazyown_target_context`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/tasks_cleanup.py
- Doc: MCP tool ``lazyown_tasks_cleanup`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/threat_model.py
- Doc: MCP tool ``lazyown_threat_model`` (migrated from the call_tool dispatch chain).
- Layer: business_logic
- Language: py
- Symbols:
  - `handle` (function, line 44) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/timeline.py
- Doc: MCP tool ``lazyown_timeline`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/timeline_narrator.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/ttp_chain.py
- Doc: MCP tool ``lazyown_ttp_chain`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 47) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/atomic_resolver.py`, `modules/ttpscope_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/unified_dashboard.py
- Doc: MCP tool ``lazyown_unified_dashboard``: combined campaign dashboard.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/unified_dashboard.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/winbox_eventlogs.py
- Doc: MCP tool ``lazyown_winbox_eventlogs``: query guest Windows event logs.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 36) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/__init__.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/winbox_exec.py
- Doc: MCP tool ``lazyown_winbox_exec``: run a command inside the WinBox guest.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 38) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/__init__.py`, `skills/mcp_tools/_context.py`


Next: [KB_mcp_tools_p4.md](KB_mcp_tools_p4.md)
