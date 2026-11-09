# API (page 23 of 27)
Previous: [API_p22.md](API_p22.md)

## skills/mcp_tools/campaign_lessons.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_lessons.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_lessons MCP tool.

## skills/mcp_tools/campaign_sitrep.py
Depends on: `modules/killchain.py`, `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_sitrep.py:46` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_sitrep MCP tool.

## skills/mcp_tools/campaign_tasks.py
Depends on: `modules/session_reader.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_tasks.py:66` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_tasks MCP tool.

## skills/mcp_tools/collab_publish.py
Depends on: `modules/collab_bp.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/collab_publish.py:41` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_collab_publish MCP tool.

## skills/mcp_tools/command_help.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_help.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_help MCP tool.

## skills/mcp_tools/command_next.py
Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_next.py:45` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_next MCP tool.

## skills/mcp_tools/command_prev.py
Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_prev.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_prev MCP tool.

## skills/mcp_tools/create_addon.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/create_addon.py:115` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_create_addon MCP tool.

## skills/mcp_tools/create_param.py
Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/create_param.py:47` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_create_param MCP tool.

## skills/mcp_tools/credentials.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/credentials.py:32` `def handle(arguments, tool_name, ctx)` -- Collect, dedupe and format credentials from all session sources.

## skills/mcp_tools/cron_schedule.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/cron_schedule.py:55` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_cron_schedule MCP tool.

## skills/mcp_tools/cve_search.py
Depends on: `modules/cve_matcher.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/cve_search.py:42` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_cve_search MCP tool.

## skills/mcp_tools/daemon.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon.py:34` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon MCP tool.

## skills/mcp_tools/daemon_approve.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_approve.py:37` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_approve MCP tool.

## skills/mcp_tools/daemon_focus.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_focus.py:33` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_focus MCP tool.

## skills/mcp_tools/daemon_mode.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_mode.py:33` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_mode MCP tool.

## skills/mcp_tools/daemon_pause.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_pause.py:21` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_pause MCP tool.

## skills/mcp_tools/daemon_resume.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_resume.py:20` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_resume MCP tool.

## skills/mcp_tools/daemon_status.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_status.py:22` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_status MCP tool.

## skills/mcp_tools/daemon_veto.py
Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/daemon_veto.py:37` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_daemon_veto MCP tool.

## skills/mcp_tools/dashboard_snapshot.py
Depends on: `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/dashboard_snapshot.py:28` `def handle(arguments, tool_name, ctx)` -- Build and persist a dashboard snapshot, returning map and topology.

## skills/mcp_tools/db.py
Depends on: `modules/db.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/db.py:62` `def handle(arguments, tool_name, ctx)` -- Dispatch one SQLite campaign-database operation and return its result.

## skills/mcp_tools/delete_param.py
Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/delete_param.py:26` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_delete_param MCP tool.

## skills/mcp_tools/deploy_beacon.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/deploy_beacon.py:40` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_deploy_beacon MCP tool.

## skills/mcp_tools/discover_commands.py
Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/discover_commands.py:52` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_discover_commands MCP tool.

## skills/mcp_tools/engage_approve.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/engage_approve.py:40` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_engage_approve MCP tool.

## skills/mcp_tools/engage_list_pending.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/engage_list_pending.py:21` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_engage_list_pending MCP tool.

## skills/mcp_tools/engage_status.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/engage_status.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_engage_status MCP tool.

## skills/mcp_tools/engage_target.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/engage_target.py:57` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_engage_target MCP tool.

## skills/mcp_tools/eval_quality.py
Depends on: `modules/llm_evaluator.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/eval_quality.py:38` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_eval_quality MCP tool.

## skills/mcp_tools/evasion_generate.py
Depends on: `modules/evasion_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/evasion_generate.py:36` `def handle(arguments, tool_name, ctx)` -- Generate an evasion profile for the requested OS family as JSON.

## skills/mcp_tools/evasion_rotate.py
Depends on: `modules/evasion_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/evasion_rotate.py:27` `def handle(arguments, tool_name, ctx)` -- Rotate the active evasion profile and return it as JSON.

## skills/mcp_tools/evidence_grep.py
Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/evidence_grep.py:47` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_evidence_grep MCP tool.

## skills/mcp_tools/exploit_chain.py
Depends on: `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploit_chain.py:41` `def handle(arguments, tool_name, ctx)` -- Build and run an adaptive exploit chain, returning plan and results.

## skills/mcp_tools/exploit_recommend.py
Depends on: `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploit_recommend.py:44` `def handle(arguments, tool_name, ctx)` -- Rank exploit matches for discovered services and return them as JSON.

## skills/mcp_tools/exploitgym_list.py
Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploitgym_list.py:39` `def handle(arguments, tool_name, ctx)` -- List ExploitGym tasks, optionally filtered by domain.

## skills/mcp_tools/exploitgym_run.py
Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploitgym_run.py:48` `def handle(arguments, tool_name, ctx)` -- Run the agent against an ExploitGym task (containerised only).

## skills/mcp_tools/exploitgym_score.py
Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploitgym_score.py:41` `def handle(arguments, tool_name, ctx)` -- Award Red Team Gym ELO for an ExploitGym task outcome.

## skills/mcp_tools/exploitgym_status.py
Depends on: `modules/exploitgym_gym.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/exploitgym_status.py:26` `def handle(arguments, tool_name, ctx)` -- Report ExploitGym harness readiness without installing anything.

## skills/mcp_tools/facts_show.py
Depends on: `skills/lazyown_facts.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/facts_show.py:39` `def handle(arguments, tool_name, ctx)` -- Return the fact-store summary for a target, optionally re-parsing first.

## skills/mcp_tools/fast_run.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/fast_run.py:49` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_fast_run MCP tool.

## skills/mcp_tools/generate_report.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/generate_report.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_generate_report MCP tool.

## skills/mcp_tools/get_beacons.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/get_beacons.py:20` `def handle(arguments, tool_name, ctx)` -- Query the C2 for connected clients and return the JSON list.

## skills/mcp_tools/get_config.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/get_config.py:26` `def handle(arguments, tool_name, ctx)` -- Return the full ``payload.json`` as pretty-printed JSON text.

## skills/mcp_tools/get_llm_budget.py
Depends on: `core/llm_budget.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/get_llm_budget.py:26` `def handle(arguments, tool_name, ctx)` -- Return the LLM budget status, or an unavailable marker on failure.

## skills/mcp_tools/graph_neighbors.py
Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/graph_neighbors.py:33` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_graph_neighbors MCP tool.

## skills/mcp_tools/graph_search.py
Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/graph_search.py:36` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_graph_search MCP tool.

## skills/mcp_tools/graph_suggest_next.py
Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/graph_suggest_next.py:35` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_graph_suggest_next MCP tool.

## skills/mcp_tools/graph_summary.py
Depends on: `cli/graph_advisor.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/graph_summary.py:25` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_graph_summary MCP tool.

## skills/mcp_tools/groq_agent.py
Depends on: `skills/lazyown_groq_agents.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/groq_agent.py:70` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_groq_agent MCP tool.

## skills/mcp_tools/heartbeat_status.py
Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/heartbeat_status.py:20` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_heartbeat_status MCP tool.

## skills/mcp_tools/hive_collect.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_collect.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_collect MCP tool.

## skills/mcp_tools/hive_forget.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_forget.py:25` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_forget MCP tool.

## skills/mcp_tools/hive_plan.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_plan.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_plan MCP tool.

## skills/mcp_tools/hive_recall.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_recall.py:29` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_recall MCP tool.

## skills/mcp_tools/hive_recover.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_recover.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_recover MCP tool.

## skills/mcp_tools/hive_result.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_result.py:22` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_result MCP tool.

## skills/mcp_tools/hive_spawn.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_spawn.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_spawn MCP tool.

## skills/mcp_tools/hive_status.py
Depends on: `skills/hive_mind.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/hive_status.py:21` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_hive_status MCP tool.

## skills/mcp_tools/inject_objective.py
Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/inject_objective.py:52` `def handle(arguments, tool_name, ctx)` -- Inject one objective into the queue and report the new pending count.

## skills/mcp_tools/lazy_addon.py
Depends on: `modules/auto_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_addon.py:27` `def handle(arguments, tool_name, ctx)` -- List addon triggers or return matches for a service as JSON.

## skills/mcp_tools/lazy_board.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_board.py:36` `def handle(arguments, tool_name, ctx)` -- Return one page of the broadcast board as JSON.

## skills/mcp_tools/lazy_compact.py
Depends on: `modules/lazy_loop.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_compact.py:35` `def handle(arguments, tool_name, ctx)` -- Dispatch the compaction action and return its result as JSON.

## skills/mcp_tools/lazy_delete.py
Depends on: `modules/lazy_loop.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_delete.py:33` `def handle(arguments, tool_name, ctx)` -- Delete or preview-delete an intent and return the result as JSON.

## skills/mcp_tools/lazy_finding.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
Imported by: `modules/lazy_mentions.py`
- `handle` (function) `skills/mcp_tools/lazy_finding.py:34` `def handle(arguments, tool_name, ctx)` -- Persist a finding node and return its record as JSON.

## skills/mcp_tools/lazy_hint.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_hint.py:26` `def handle(arguments, tool_name, ctx)` -- Create a hint node and return its record as JSON.

## skills/mcp_tools/lazy_intel.py
Depends on: `modules/__init__.py`, `modules/lazy_exposure.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_intel.py:53` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_lazy_intel MCP tool.

## skills/mcp_tools/lazy_mention.py
Depends on: `modules/lazy_mentions.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_mention.py:28` `def handle(arguments, tool_name, ctx)` -- Return one page of mention items plus the next cursor as JSON.

## skills/mcp_tools/lazy_proxy.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_proxy.py:39` `def handle(arguments, tool_name, ctx)` -- Dispatch the proxy action and return its status as JSON.

## skills/mcp_tools/lazy_status.py
Depends on: `modules/lazy_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_status.py:19` `def handle(arguments, tool_name, ctx)` -- Return the lazy-bridge status snapshot as JSON.

## skills/mcp_tools/lazy_sync.py
Depends on: `modules/lazy_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_sync.py:19` `def handle(arguments, tool_name, ctx)` -- Run a full lazy-bridge sync and return its result as JSON.

## skills/mcp_tools/lazy_trace.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_trace.py:29` `def handle(arguments, tool_name, ctx)` -- Return up to the hit cap of matching activity-log entries as JSON.

## skills/mcp_tools/lazy_workspace.py
Depends on: `modules/__init__.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazy_workspace.py:30` `def handle(arguments, tool_name, ctx)` -- Dispatch the workspace action and return its result as JSON.

## skills/mcp_tools/lazysearch.py
Depends on: `modules/lazy_search.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lazysearch.py:48` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_lazysearch MCP tool.

## skills/mcp_tools/list_addons.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_addons.py:20` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_addons MCP tool.

## skills/mcp_tools/list_agents.py
Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_agents.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_agents MCP tool.

## skills/mcp_tools/list_event_rules.py
Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_event_rules.py:25` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_event_rules MCP tool.

## skills/mcp_tools/list_modules.py
Depends on: `modules/module_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_modules.py:27` `def handle(arguments, tool_name, ctx)` -- Return discovered modules as JSON, optionally filtered by type.

## skills/mcp_tools/list_params.py
Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_params.py:36` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_params MCP tool.

## skills/mcp_tools/list_plugins.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_plugins.py:17` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_plugins MCP tool.

## skills/mcp_tools/list_sessions.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_sessions.py:26` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_sessions MCP tool.

## skills/mcp_tools/list_targets.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/list_targets.py:30` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_list_targets MCP tool.

## skills/mcp_tools/llm_ask.py
Depends on: `skills/lazyown_llm.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/llm_ask.py:67` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_llm_ask MCP tool.

## skills/mcp_tools/lolbas_list.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lolbas_list.py:34` `def handle(arguments, tool_name, ctx)` -- Return LOLBAS techniques discovered in plugin YAML files as JSON.

## skills/mcp_tools/lolbas_use.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/lolbas_use.py:44` `def handle(arguments, tool_name, ctx)` -- Resolve and run one LOLBAS technique, returning command and output.

## skills/mcp_tools/loop_smoke.py
Depends on: `modules/lazy_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/loop_smoke.py:65` `def handle(arguments, tool_name, ctx)` -- Run a one-leg loop smoke test and return the goal verdict.

## skills/mcp_tools/memory_recall.py
Depends on: `skills/mcp_tools/_context.py`, `skills/mcp_tools/memory_store.py`
- `handle` (function) `skills/mcp_tools/memory_recall.py:43` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_memory_recall MCP tool.

## skills/mcp_tools/memory_store.py
Depends on: `skills/mcp_tools/_context.py`
Imported by: `skills/mcp_tools/memory_recall.py`
- `handle` (function) `skills/mcp_tools/memory_store.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_memory_store MCP tool.

## skills/mcp_tools/metrics_summary.py
Depends on: `modules/metrics.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/metrics_summary.py:40` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_metrics_summary MCP tool.

## skills/mcp_tools/misp_export.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/misp_export.py:38` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_misp_export MCP tool.

## skills/mcp_tools/next_objective.py
Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/next_objective.py:29` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_next_objective MCP tool.

## skills/mcp_tools/opencode_config.py
Depends on: `scripts/lazy_opencode_config.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/opencode_config.py:38` `def handle(arguments, tool_name, ctx)` -- Patch opencode/hermes configs to the local llama.cpp server.

## skills/mcp_tools/palette.py
Depends on: `cli/palette.py`, `cli/palette_command.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/palette.py:41` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_palette MCP tool.

## skills/mcp_tools/parquet_annotate.py
Depends on: `skills/lazyown_parquet_db.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/parquet_annotate.py:51` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_parquet_annotate MCP tool.

## skills/mcp_tools/parquet_query.py
Depends on: `skills/lazyown_parquet_db.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/parquet_query.py:87` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_parquet_query MCP tool.

## skills/mcp_tools/phase_guide.py
Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/phase_guide.py:64` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_phase_guide MCP tool.

## skills/mcp_tools/pipeline_list.py
Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/pipeline_list.py:18` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_pipeline_list MCP tool.

## skills/mcp_tools/pipeline_run.py
Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/pipeline_run.py:46` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_pipeline_run MCP tool.

## skills/mcp_tools/pipeline_status.py
Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/pipeline_status.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_pipeline_status MCP tool.

## skills/mcp_tools/pipeline_validate.py
Depends on: `modules/pipeline_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/pipeline_validate.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_pipeline_validate MCP tool.

## skills/mcp_tools/pivot_status.py
Depends on: `modules/auto_pivot.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/pivot_status.py:27` `def handle(arguments, tool_name, ctx)` -- Return active routes, proxychains config and next-pivot suggestion.

## skills/mcp_tools/playbook_generate.py
Depends on: `modules/playbook_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/playbook_generate.py:52` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_playbook_generate MCP tool.

## skills/mcp_tools/poll_events.py
Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/poll_events.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_poll_events MCP tool.

## skills/mcp_tools/rag_index.py
Depends on: `modules/session_rag.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/rag_index.py:37` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_rag_index MCP tool.

## skills/mcp_tools/rag_query.py
Depends on: `modules/session_rag.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/rag_query.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_rag_query MCP tool.

## skills/mcp_tools/rea.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/rea.py:95` `def handle(arguments, tool_name, ctx)` -- Run one REA CLI action against a local artifact and return a JSON envelope.

## skills/mcp_tools/reactive_suggest.py
Depends on: `modules/reactive_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/reactive_suggest.py:50` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_reactive_suggest MCP tool.

## skills/mcp_tools/read_prompt.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/read_prompt.py:41` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_read_prompt MCP tool.

## skills/mcp_tools/read_session_file.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/read_session_file.py:26` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_read_session_file MCP tool.

## skills/mcp_tools/rich_tui_snapshot.py
Depends on: `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/rich_tui_snapshot.py:30` `def handle(arguments, tool_name, ctx)` -- Return a non-interactive snapshot of the Rich TUI dashboard as JSON.

## skills/mcp_tools/run_api.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/run_api.py:30` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_run_api MCP tool.

## skills/mcp_tools/run_command.py
Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/run_command.py:82` `def handle(arguments, tool_name, ctx)` -- Pre-flight, confirm, execute and record one or more shell commands.

## skills/mcp_tools/searchsploit.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/searchsploit.py:79` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_searchsploit MCP tool.

## skills/mcp_tools/session_diff.py
Depends on: `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/session_diff.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_session_diff MCP tool.

## skills/mcp_tools/session_state.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/session_state.py:33` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_session_state MCP tool.

## skills/mcp_tools/session_status.py
Depends on: `modules/session_reader.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/session_status.py:43` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_session_status MCP tool.

## skills/mcp_tools/set_active_target.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/set_active_target.py:35` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_set_active_target MCP tool.

## skills/mcp_tools/set_config.py
Depends on: `core/payload_schema.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/set_config.py:36` `def handle(arguments, tool_name, ctx)` -- Coerce and persist one payload key, refusing to null an existing value.
- `coerce_value` (function) `skills/mcp_tools/set_config.py:46` `def coerce_value(coerce_key, coerce_value_in)`

## skills/mcp_tools/soul.py
Depends on: `skills/lazyown_objective.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/soul.py:42` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_soul MCP tool.

## skills/mcp_tools/stealth.py
Depends on: `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/stealth.py:35` `def handle(arguments, tool_name, ctx)` -- Set the stealth level on the exploit engine and persist it to config.

## skills/mcp_tools/swan_ensemble.py
Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`
- `handle` (function) `skills/mcp_tools/swan_ensemble.py:48` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_swan_ensemble MCP tool.

## skills/mcp_tools/swan_route.py
Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`
- `handle` (function) `skills/mcp_tools/swan_route.py:37` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_swan_route MCP tool.

## skills/mcp_tools/swan_run.py
Depends on: `skills/mcp_tools/_context.py`, `skills/swan_agent.py`
- `handle` (function) `skills/mcp_tools/swan_run.py:45` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_swan_run MCP tool.


Next: [API_p24.md](API_p24.md)
