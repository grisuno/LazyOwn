# Subsystem: mcp_tools (page 1 of 4)
Pages: [KB_mcp_tools.md](KB_mcp_tools.md), [KB_mcp_tools_p2.md](KB_mcp_tools_p2.md), [KB_mcp_tools_p3.md](KB_mcp_tools_p3.md), [KB_mcp_tools_p4.md](KB_mcp_tools_p4.md)

## skills/mcp_tools/__init__.py
- Doc: Auto-discovered one-file-per-tool registry for the LazyOwn MCP server.
- Layer: utility
- Language: py
- Symbols:
  - `iter_tool_modules` (function, line 30) `def iter_tool_modules()`
  - `iter_schemas` (function, line 51) `def iter_schemas()`
  - `register_handlers` (function, line 57) `def register_handlers(handlers, ctx)`
  - `_async_wrap` (function, line 79) `def _async_wrap(arguments, tool_name, _handle)`
  - `_sync_wrap` (function, line 85) `def _sync_wrap(arguments, tool_name, _handle)`
- Depends on: `skills/mcp_tools/_context.py`
- Imported by: `skills/lazyown_mcp.py`

## skills/mcp_tools/_context.py
- Doc: Dependency-injection context handed to every ``mcp_tools`` handler.
- Layer: utility
- Language: py
- Symbols:
  - `MCPContext` (class, line 21) `class MCPContext`
- Imported by: `skills/lazyown_mcp.py`, `skills/mcp_tools/__init__.py`, `skills/mcp_tools/aci_plan.py`, `skills/mcp_tools/aci_replan.py`, `skills/mcp_tools/aci_status.py`, `skills/mcp_tools/ack_event.py`, `skills/mcp_tools/add_rule.py`, `skills/mcp_tools/add_target.py`, `skills/mcp_tools/agent_result.py`, `skills/mcp_tools/agent_status.py`, `skills/mcp_tools/apt_chain.py`, `skills/mcp_tools/atomic_clean.py`, `skills/mcp_tools/atomic_resolve.py`, `skills/mcp_tools/atomic_search.py`, `skills/mcp_tools/atomic_shell.py`, `skills/mcp_tools/auto_loop.py`, `skills/mcp_tools/auto_populate.py`, `skills/mcp_tools/auto_pwn.py`, `skills/mcp_tools/autonomous_events.py`, `skills/mcp_tools/autonomous_inject.py`, `skills/mcp_tools/autonomous_replay.py`, `skills/mcp_tools/autonomous_start.py`, `skills/mcp_tools/autonomous_status.py`, `skills/mcp_tools/autonomous_stop.py`, `skills/mcp_tools/bridge_suggest.py`, `skills/mcp_tools/c2_adversary.py`, `skills/mcp_tools/c2_command.py`, `skills/mcp_tools/c2_notes.py`, `skills/mcp_tools/c2_profile.py`, `skills/mcp_tools/c2_redop.py`, `skills/mcp_tools/c2_script.py`, `skills/mcp_tools/c2_search_agent.py`, `skills/mcp_tools/c2_status.py`, `skills/mcp_tools/c2_vuln_analysis.py`, `skills/mcp_tools/campaign.py`, `skills/mcp_tools/campaign_lessons.py`, `skills/mcp_tools/campaign_sitrep.py`, `skills/mcp_tools/campaign_tasks.py`, `skills/mcp_tools/claudemd.py`, `skills/mcp_tools/collab_publish.py`, `skills/mcp_tools/command_help.py`, `skills/mcp_tools/command_next.py`, `skills/mcp_tools/command_prev.py`, `skills/mcp_tools/create_addon.py`, `skills/mcp_tools/create_param.py`, `skills/mcp_tools/create_tool.py`, `skills/mcp_tools/credentials.py`, `skills/mcp_tools/cron_schedule.py`, `skills/mcp_tools/cve_search.py`, `skills/mcp_tools/daemon.py`, `skills/mcp_tools/daemon_approve.py`, `skills/mcp_tools/daemon_focus.py`, `skills/mcp_tools/daemon_mode.py`, `skills/mcp_tools/daemon_pause.py`, `skills/mcp_tools/daemon_resume.py`, `skills/mcp_tools/daemon_status.py`, `skills/mcp_tools/daemon_veto.py`, `skills/mcp_tools/dashboard_snapshot.py`, `skills/mcp_tools/db.py`, `skills/mcp_tools/delete_param.py`, `skills/mcp_tools/deploy_beacon.py`, `skills/mcp_tools/discover_commands.py`, `skills/mcp_tools/engage_approve.py`, `skills/mcp_tools/engage_list_pending.py`, `skills/mcp_tools/engage_status.py`, `skills/mcp_tools/engage_target.py`, `skills/mcp_tools/eval_quality.py`, `skills/mcp_tools/evasion_generate.py`, `skills/mcp_tools/evasion_rotate.py`, `skills/mcp_tools/evidence_grep.py`, `skills/mcp_tools/exploit_chain.py`, `skills/mcp_tools/exploit_recommend.py`, `skills/mcp_tools/exploitgym_list.py`, `skills/mcp_tools/exploitgym_run.py`, `skills/mcp_tools/exploitgym_score.py`, `skills/mcp_tools/exploitgym_status.py`, `skills/mcp_tools/facts_show.py`, `skills/mcp_tools/fast_run.py`, `skills/mcp_tools/generate_report.py`, `skills/mcp_tools/get_beacons.py`, `skills/mcp_tools/get_config.py`, `skills/mcp_tools/get_llm_budget.py`, `skills/mcp_tools/graph_neighbors.py`, `skills/mcp_tools/graph_search.py`, `skills/mcp_tools/graph_suggest_next.py`, `skills/mcp_tools/graph_summary.py`, `skills/mcp_tools/groq_agent.py`, `skills/mcp_tools/harness_status.py`, `skills/mcp_tools/heartbeat_status.py`, `skills/mcp_tools/hive_collect.py`, `skills/mcp_tools/hive_forget.py`, `skills/mcp_tools/hive_plan.py`, `skills/mcp_tools/hive_recall.py`, `skills/mcp_tools/hive_recover.py`, `skills/mcp_tools/hive_result.py`, `skills/mcp_tools/hive_spawn.py`, `skills/mcp_tools/hive_status.py`, `skills/mcp_tools/inject_objective.py`, `skills/mcp_tools/job_status.py`, `skills/mcp_tools/lazy_addon.py`, `skills/mcp_tools/lazy_board.py`, `skills/mcp_tools/lazy_compact.py`, `skills/mcp_tools/lazy_delete.py`, `skills/mcp_tools/lazy_finding.py`, `skills/mcp_tools/lazy_hint.py`, `skills/mcp_tools/lazy_intel.py`, `skills/mcp_tools/lazy_mention.py`, `skills/mcp_tools/lazy_proxy.py`, `skills/mcp_tools/lazy_status.py`, `skills/mcp_tools/lazy_sync.py`, `skills/mcp_tools/lazy_trace.py`, `skills/mcp_tools/lazy_workspace.py`, `skills/mcp_tools/lazysearch.py`, `skills/mcp_tools/list_addons.py`, `skills/mcp_tools/list_agents.py`, `skills/mcp_tools/list_event_rules.py`, `skills/mcp_tools/list_modules.py`, `skills/mcp_tools/list_params.py`, `skills/mcp_tools/list_plugins.py`, `skills/mcp_tools/list_sessions.py`, `skills/mcp_tools/list_targets.py`, `skills/mcp_tools/llm_ask.py`, `skills/mcp_tools/lolbas_list.py`, `skills/mcp_tools/lolbas_use.py`, `skills/mcp_tools/loop_smoke.py`, `skills/mcp_tools/manage_permissions.py`, `skills/mcp_tools/memory_recall.py`, `skills/mcp_tools/memory_store.py`, `skills/mcp_tools/metrics_summary.py`, `skills/mcp_tools/misp_export.py`, `skills/mcp_tools/next_objective.py`, `skills/mcp_tools/opencode_config.py`, `skills/mcp_tools/palette.py`, `skills/mcp_tools/parquet_annotate.py`, `skills/mcp_tools/parquet_query.py`, `skills/mcp_tools/phase_guide.py`, `skills/mcp_tools/pipeline_list.py`, `skills/mcp_tools/pipeline_run.py`, `skills/mcp_tools/pipeline_status.py`, `skills/mcp_tools/pipeline_validate.py`, `skills/mcp_tools/pivot_status.py`, `skills/mcp_tools/playbook_generate.py`, `skills/mcp_tools/playbook_run.py`, `skills/mcp_tools/policy_status.py`, `skills/mcp_tools/poll_events.py`, `skills/mcp_tools/rag_index.py`, `skills/mcp_tools/rag_query.py`, `skills/mcp_tools/rea.py`, `skills/mcp_tools/reactive_suggest.py`, `skills/mcp_tools/read_prompt.py`, `skills/mcp_tools/read_session_file.py`, `skills/mcp_tools/recommend_next.py`, `skills/mcp_tools/rich_tui_snapshot.py`, `skills/mcp_tools/run_agent.py`, `skills/mcp_tools/run_api.py`, `skills/mcp_tools/run_command.py`, `skills/mcp_tools/run_command_async.py`, `skills/mcp_tools/search_tools.py`, `skills/mcp_tools/searchsploit.py`, `skills/mcp_tools/session_diff.py`, `skills/mcp_tools/session_init.py`, `skills/mcp_tools/session_resume.py`, `skills/mcp_tools/session_state.py`, `skills/mcp_tools/session_status.py`, `skills/mcp_tools/set_active_target.py`, `skills/mcp_tools/set_config.py`, `skills/mcp_tools/soul.py`, `skills/mcp_tools/stealth.py`, `skills/mcp_tools/subagent_run.py`, `skills/mcp_tools/swan_ensemble.py`, `skills/mcp_tools/swan_route.py`, `skills/mcp_tools/swan_run.py`, `skills/mcp_tools/swan_status.py`, `skills/mcp_tools/target_context.py`, `skills/mcp_tools/tasks_cleanup.py`, `skills/mcp_tools/threat_model.py`, `skills/mcp_tools/timeline.py`, `skills/mcp_tools/ttp_chain.py`, `skills/mcp_tools/unified_dashboard.py`, `skills/mcp_tools/winbox_eventlogs.py`, `skills/mcp_tools/winbox_exec.py`, `skills/mcp_tools/winbox_gym_list.py`, `skills/mcp_tools/winbox_gym_plan.py`, `skills/mcp_tools/winbox_gym_run.py`, `skills/mcp_tools/winbox_snapshot.py`, `skills/mcp_tools/winbox_status.py`, `skills/mcp_tools/winbox_tools.py`, `skills/mcp_tools/winbox_vm.py`, `tests/test_mcp_tools_registry.py`, `tests/test_rea_mcp.py`

## skills/mcp_tools/aci_plan.py
- Doc: MCP tool ``lazyown_aci_plan`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 63) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/aci_replan.py
- Doc: MCP tool ``lazyown_aci_replan`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/aci_status.py
- Doc: MCP tool ``lazyown_aci_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/ack_event.py
- Doc: MCP tool ``lazyown_ack_event``: mark an event as processed.
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/add_rule.py
- Doc: MCP tool ``lazyown_add_rule`` (migrated from the call_tool dispatch chain).
- Layer: business_logic
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/add_target.py
- Doc: MCP tool ``lazyown_add_target`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 48) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/agent_result.py
- Doc: MCP tool ``lazyown_agent_result`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 31) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/agent_status.py
- Doc: MCP tool ``lazyown_agent_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/apt_chain.py
- Doc: MCP tool ``lazyown_apt_chain`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 93) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/chain_registry.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/atomic_clean.py
- Doc: MCP tool ``lazyown_atomic_clean`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 45) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/atomic_exploit_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/atomic_resolve.py
- Doc: MCP tool ``lazyown_atomic_resolve`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 49) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/atomic_enricher.py`, `modules/atomic_resolver.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/atomic_search.py
- Doc: MCP tool ``lazyown_atomic_search`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 74) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/atomic_enricher.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/atomic_shell.py
- Doc: MCP tool ``lazyown_atomic_shell`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/atomic_exploit_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/auto_loop.py
- Doc: MCP tool ``lazyown_auto_loop`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 48) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_runner.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/auto_populate.py
- Doc: MCP tool ``lazyown_auto_populate`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/auto_pwn.py
- Doc: MCP tool ``lazyown_auto_pwn``: run the full autonomous exploitation chain.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 47) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_events.py
- Doc: MCP tool ``lazyown_autonomous_events`` (migrated from the call_tool dispatch chain).
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_inject.py
- Doc: MCP tool ``lazyown_autonomous_inject`` (migrated from the call_tool dispatch chain).
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_replay.py
- Doc: MCP tool ``lazyown_autonomous_replay`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 53) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_start.py
- Doc: MCP tool ``lazyown_autonomous_start`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 40) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_status.py
- Doc: MCP tool ``lazyown_autonomous_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 21) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/autonomous_stop.py
- Doc: MCP tool ``lazyown_autonomous_stop`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 18) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/bridge_suggest.py
- Doc: MCP tool ``lazyown_bridge_suggest`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 104) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_adversary.py
- Doc: MCP tool ``lazyown_c2_adversary`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_command.py
- Doc: MCP tool ``lazyown_c2_command`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_notes.py
- Doc: MCP tool ``lazyown_c2_notes`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 38) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_profile.py
- Doc: MCP tool ``lazyown_c2_profile`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_redop.py
- Doc: MCP tool ``lazyown_c2_redop`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_script.py
- Doc: MCP tool ``lazyown_c2_script`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_search_agent.py
- Doc: MCP tool ``lazyown_c2_search_agent`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_status.py
- Doc: MCP tool ``lazyown_c2_status``: check C2 reachability and dashboard data.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 20) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/c2_vuln_analysis.py
- Doc: MCP tool ``lazyown_c2_vuln_analysis`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/campaign.py
- Doc: MCP tool ``lazyown_campaign`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 46) `def handle(arguments, tool_name, ctx)`
  - `_run_campaign` (function, line 50) `def _run_campaign()`
- Depends on: `skills/lazyown_campaign.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/campaign_lessons.py
- Doc: MCP tool ``lazyown_campaign_lessons`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 39) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/campaign_sitrep.py
- Doc: MCP tool ``lazyown_campaign_sitrep`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 46) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/killchain.py`, `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/campaign_tasks.py
- Doc: MCP tool ``lazyown_campaign_tasks`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 66) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/session_reader.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/claudemd.py
- Doc: MCP tool ``lazyown_claudemd`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 43) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/collab_publish.py
- Doc: MCP tool ``lazyown_collab_publish`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 41) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/collab_bp.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/command_help.py
- Doc: MCP tool ``lazyown_command_help`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 31) `def handle(arguments, tool_name, ctx)`
  - `_read_docstring` (function, line 42) `def _read_docstring(cmd_name)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/command_next.py
- Doc: MCP tool ``lazyown_command_next`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 45) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/command_prev.py
- Doc: MCP tool ``lazyown_command_prev`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 31) `def handle(arguments, tool_name, ctx)`
- Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/create_addon.py
- Doc: MCP tool ``lazyown_create_addon`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 115) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/create_param.py
- Doc: MCP tool ``lazyown_create_param`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 47) `def handle(arguments, tool_name, ctx)`
- Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/create_tool.py
- Doc: MCP tool ``lazyown_create_tool`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 55) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/lazyown_facts.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/credentials.py
- Doc: MCP tool ``lazyown_credentials``: aggregate captured credentials.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 32) `def handle(arguments, tool_name, ctx)`
  - `_add` (function, line 37) `def _add(user, secret, host, source, confirmed)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/cron_schedule.py
- Doc: MCP tool ``lazyown_cron_schedule`` (migrated from the call_tool dispatch chain).
- Layer: infrastructure
- Language: py
- Symbols:
  - `handle` (function, line 55) `def handle(arguments, tool_name, ctx)`
  - `_load_crons` (function, line 60) `def _load_crons()`
  - `_save_crons` (function, line 71) `def _save_crons(entries)`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/cve_search.py
- Doc: MCP tool ``lazyown_cve_search`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 42) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/cve_matcher.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon.py
- Doc: MCP tool ``lazyown_daemon`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 34) `def handle(arguments, tool_name, ctx)`
  - `_run_daemon` (function, line 38) `def _run_daemon()`
- Depends on: `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_approve.py
- Doc: MCP tool ``lazyown_daemon_approve`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_focus.py
- Doc: MCP tool ``lazyown_daemon_focus`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_mode.py
- Doc: MCP tool ``lazyown_daemon_mode`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 33) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_pause.py
- Doc: MCP tool ``lazyown_daemon_pause`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 21) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_resume.py
- Doc: MCP tool ``lazyown_daemon_resume`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 20) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_status.py
- Doc: MCP tool ``lazyown_daemon_status`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 22) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/daemon_veto.py
- Doc: MCP tool ``lazyown_daemon_veto`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 37) `def handle(arguments, tool_name, ctx)`
- Depends on: `skills/daemon_control.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/dashboard_snapshot.py
- Doc: MCP tool ``lazyown_dashboard_snapshot``: render the live network map.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 28) `def handle(arguments, tool_name, ctx)`
- Depends on: `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/world_model.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/db.py
- Doc: MCP tool ``lazyown_db``: query and mutate the LazyOwn SQLite database.
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 62) `def handle(arguments, tool_name, ctx)`
  - `_result` (function, line 84) `def _result(payload)`
- Depends on: `modules/db.py`, `skills/mcp_tools/_context.py`

## skills/mcp_tools/delete_param.py
- Doc: MCP tool ``lazyown_delete_param`` (migrated from the call_tool dispatch chain).
- Layer: utility
- Language: py
- Symbols:
  - `handle` (function, line 26) `def handle(arguments, tool_name, ctx)`
- Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`


Next: [KB_mcp_tools_p2.md](KB_mcp_tools_p2.md)
