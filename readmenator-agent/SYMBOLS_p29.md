# Symbols (page 29 of 51)
Previous: [SYMBOLS_p28.md](SYMBOLS_p28.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_gen_wizard` | function | `skills/mcp_generated_tools.py:5748` | `def _gen_wizard(arguments, tool_name, _cmd)` |
| `_gen_wmi_lateral` | function | `skills/mcp_generated_tools.py:5756` | `def _gen_wmi_lateral(arguments, tool_name, _cmd)` |
| `_gen_wmi_persist` | function | `skills/mcp_generated_tools.py:5764` | `def _gen_wmi_persist(arguments, tool_name, _cmd)` |
| `_gen_wmi_scheduled_task` | function | `skills/mcp_generated_tools.py:5772` | `def _gen_wmi_scheduled_task(arguments, tool_name, _cmd)` |
| `_gen_wmiexec` | function | `skills/mcp_generated_tools.py:5780` | `def _gen_wmiexec(arguments, tool_name, _cmd)` |
| `_gen_wmiexecpro` | function | `skills/mcp_generated_tools.py:5788` | `def _gen_wmiexecpro(arguments, tool_name, _cmd)` |
| `_gen_wpscan` | function | `skills/mcp_generated_tools.py:5796` | `def _gen_wpscan(arguments, tool_name, _cmd)` |
| `_gen_wrapper` | function | `skills/mcp_generated_tools.py:5804` | `def _gen_wrapper(arguments, tool_name, _cmd)` |
| `_gen_www` | function | `skills/mcp_generated_tools.py:5812` | `def _gen_www(arguments, tool_name, _cmd)` |
| `_gen_xss` | function | `skills/mcp_generated_tools.py:5820` | `def _gen_xss(arguments, tool_name, _cmd)` |
| `_gen_xsstrike` | function | `skills/mcp_generated_tools.py:5828` | `def _gen_xsstrike(arguments, tool_name, _cmd)` |
| `_gen_yara_scan` | function | `skills/mcp_generated_tools.py:5836` | `def _gen_yara_scan(arguments, tool_name, _cmd)` |
| `get_generated_tool_definitions` | function | `skills/mcp_generated_tools.py:659` | `def get_generated_tool_definitions()` |
| `register_all_generated_handlers` | function | `skills/mcp_generated_tools.py:684` | `def register_all_generated_handlers(register_handler_fn, make_text_fn, run_lazyown_cmd_fn)` |
| `ensure_optional` | function | `skills/mcp_lazy.py:18` | `def ensure_optional(namespace, flag, loader)` |
| `_build_tool_schema` | function | `skills/mcp_tool_generator.py:91` | `def _build_tool_schema(command_param_name)` |
| `extract_commands` | function | `skills/mcp_tool_generator.py:34` | `def extract_commands(index)` |
| `extract_existing_handlers` | function | `skills/mcp_tool_generator.py:55` | `def extract_existing_handlers()` |
| `generate_module` | function | `skills/mcp_tool_generator.py:106` | `def generate_module(commands, existing_handlers, limit)` |
| `load_command_index` | function | `skills/mcp_tool_generator.py:29` | `def load_command_index()` |
| `main` | function | `skills/mcp_tool_generator.py:220` | `def main()` |
| `sanitize_description` | function | `skills/mcp_tool_generator.py:72` | `def sanitize_description(summary, max_len)` |
| `sanitize_docstring` | function | `skills/mcp_tool_generator.py:85` | `def sanitize_docstring(text)` |
| `verify_coverage` | function | `skills/mcp_tool_generator.py:203` | `def verify_coverage(commands, existing_handlers)` |
| `_async_wrap` | function | `skills/mcp_tools/__init__.py:79` | `def _async_wrap(arguments, tool_name, _handle)` |
| `_sync_wrap` | function | `skills/mcp_tools/__init__.py:85` | `def _sync_wrap(arguments, tool_name, _handle)` |
| `iter_schemas` | function | `skills/mcp_tools/__init__.py:51` | `def iter_schemas()` |
| `iter_tool_modules` | function | `skills/mcp_tools/__init__.py:30` | `def iter_tool_modules()` |
| `register_handlers` | function | `skills/mcp_tools/__init__.py:57` | `def register_handlers(handlers, ctx)` |
| `MCPContext` | class | `skills/mcp_tools/_context.py:21` | `class MCPContext` |
| `handle` | function | `skills/mcp_tools/aci_plan.py:63` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/aci_replan.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/aci_status.py:26` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/ack_event.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/add_rule.py:41` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/add_target.py:48` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/agent_result.py:31` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/agent_status.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/apt_chain.py:93` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/atomic_clean.py:45` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/atomic_resolve.py:49` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/atomic_search.py:74` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/atomic_shell.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/auto_loop.py:48` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/auto_populate.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/auto_pwn.py:47` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_events.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_inject.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_replay.py:53` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_start.py:40` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_status.py:21` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/autonomous_stop.py:18` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/bridge_suggest.py:104` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_adversary.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_command.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_notes.py:38` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_profile.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_redop.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_script.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_search_agent.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_status.py:20` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/c2_vuln_analysis.py:32` | `def handle(arguments, tool_name, ctx)` |
| `_run_campaign` | function | `skills/mcp_tools/campaign.py:50` | `def _run_campaign()` |
| `handle` | function | `skills/mcp_tools/campaign.py:46` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/campaign_lessons.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/campaign_sitrep.py:46` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/campaign_tasks.py:66` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/claudemd.py:43` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/collab_publish.py:41` | `def handle(arguments, tool_name, ctx)` |
| `_read_docstring` | function | `skills/mcp_tools/command_help.py:42` | `def _read_docstring(cmd_name)` |
| `handle` | function | `skills/mcp_tools/command_help.py:31` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/command_next.py:45` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/command_prev.py:31` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/create_addon.py:115` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/create_param.py:47` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/create_tool.py:55` | `def handle(arguments, tool_name, ctx)` |
| `_add` | function | `skills/mcp_tools/credentials.py:37` | `def _add(user, secret, host, source, confirmed)` |
| `handle` | function | `skills/mcp_tools/credentials.py:32` | `def handle(arguments, tool_name, ctx)` |
| `_load_crons` | function | `skills/mcp_tools/cron_schedule.py:60` | `def _load_crons()` |
| `_save_crons` | function | `skills/mcp_tools/cron_schedule.py:71` | `def _save_crons(entries)` |
| `handle` | function | `skills/mcp_tools/cron_schedule.py:55` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/cve_search.py:42` | `def handle(arguments, tool_name, ctx)` |
| `_run_daemon` | function | `skills/mcp_tools/daemon.py:38` | `def _run_daemon()` |
| `handle` | function | `skills/mcp_tools/daemon.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_approve.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_focus.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_mode.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_pause.py:21` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_resume.py:20` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_status.py:22` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/daemon_veto.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/dashboard_snapshot.py:28` | `def handle(arguments, tool_name, ctx)` |
| `_result` | function | `skills/mcp_tools/db.py:84` | `def _result(payload)` |
| `handle` | function | `skills/mcp_tools/db.py:62` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/delete_param.py:26` | `def handle(arguments, tool_name, ctx)` |
| `_deploy_beacon_sync` | function | `skills/mcp_tools/deploy_beacon.py:45` | `def _deploy_beacon_sync()` |
| `handle` | function | `skills/mcp_tools/deploy_beacon.py:40` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/discover_commands.py:52` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/engage_approve.py:40` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/engage_list_pending.py:21` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/engage_status.py:31` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/engage_target.py:57` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/eval_quality.py:38` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/evasion_generate.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/evasion_rotate.py:27` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/evidence_grep.py:47` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/exploit_chain.py:41` | `def handle(arguments, tool_name, ctx)` |
| `_has_data` | function | `skills/mcp_tools/exploit_recommend.py:17` | `def _has_data(path)` |
| `handle` | function | `skills/mcp_tools/exploit_recommend.py:44` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/exploitgym_list.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/exploitgym_run.py:48` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/exploitgym_score.py:41` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/exploitgym_status.py:26` | `def handle(arguments, tool_name, ctx)` |
| `_do_facts` | function | `skills/mcp_tools/facts_show.py:49` | `def _do_facts()` |
| `handle` | function | `skills/mcp_tools/facts_show.py:39` | `def handle(arguments, tool_name, ctx)` |
| `_launch` | function | `skills/mcp_tools/fast_run.py:89` | `def _launch()` |
| `handle` | function | `skills/mcp_tools/fast_run.py:49` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/generate_report.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/get_beacons.py:20` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/get_config.py:26` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/get_llm_budget.py:26` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/graph_neighbors.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/graph_search.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/graph_suggest_next.py:35` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/graph_summary.py:25` | `def handle(arguments, tool_name, ctx)` |
| `_blocking_run` | function | `skills/mcp_tools/groq_agent.py:110` | `def _blocking_run()` |
| `handle` | function | `skills/mcp_tools/groq_agent.py:70` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/harness_status.py:23` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/heartbeat_status.py:20` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_collect.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_forget.py:25` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_plan.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_recall.py:29` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_recover.py:31` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_result.py:22` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_spawn.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/hive_status.py:21` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/inject_objective.py:52` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/job_status.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_addon.py:27` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_board.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_compact.py:35` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_delete.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_finding.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_hint.py:26` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_intel.py:53` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_mention.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_proxy.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_status.py:19` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_sync.py:19` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_trace.py:29` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazy_workspace.py:30` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lazysearch.py:48` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_addons.py:20` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_agents.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_event_rules.py:25` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_modules.py:27` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_params.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_plugins.py:17` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_sessions.py:26` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/list_targets.py:30` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/llm_ask.py:67` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lolbas_list.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/lolbas_use.py:44` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/loop_smoke.py:65` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/manage_permissions.py:56` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/memory_recall.py:43` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/memory_store.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/metrics_summary.py:40` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/misp_export.py:38` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/next_objective.py:29` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/opencode_config.py:38` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/palette.py:41` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/parquet_annotate.py:51` | `def handle(arguments, tool_name, ctx)` |
| `_run_parquet_query` | function | `skills/mcp_tools/parquet_query.py:105` | `def _run_parquet_query()` |
| `handle` | function | `skills/mcp_tools/parquet_query.py:87` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/phase_guide.py:64` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/pipeline_list.py:18` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/pipeline_run.py:46` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/pipeline_status.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/pipeline_validate.py:28` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/pivot_status.py:27` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/playbook_generate.py:52` | `def handle(arguments, tool_name, ctx)` |
| `_mcp_executor` | function | `skills/mcp_tools/playbook_run.py:94` | `def _mcp_executor(command, target)` |
| `_substitute_playbook_target` | function | `skills/mcp_tools/playbook_run.py:16` | `def _substitute_playbook_target(command, target)` |
| `handle` | function | `skills/mcp_tools/playbook_run.py:55` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/policy_status.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/poll_events.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/rag_index.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/rag_query.py:39` | `def handle(arguments, tool_name, ctx)` |
| `_fail` | function | `skills/mcp_tools/rea.py:107` | `def _fail(message, remediation)` |
| `_run_rea` | function | `skills/mcp_tools/rea.py:181` | `def _run_rea()` |
| `handle` | function | `skills/mcp_tools/rea.py:95` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/reactive_suggest.py:50` | `def handle(arguments, tool_name, ctx)` |
| `_read_prompt` | function | `skills/mcp_tools/read_prompt.py:46` | `def _read_prompt()` |
| `handle` | function | `skills/mcp_tools/read_prompt.py:41` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/read_session_file.py:26` | `def handle(arguments, tool_name, ctx)` |
| `_fused_recommendations` | function | `skills/mcp_tools/recommend_next.py:32` | `def _fused_recommendations()` |
| `handle` | function | `skills/mcp_tools/recommend_next.py:25` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/rich_tui_snapshot.py:30` | `def handle(arguments, tool_name, ctx)` |
| `_runner` | function | `skills/mcp_tools/run_agent.py:68` | `def _runner(cmd)` |
| `handle` | function | `skills/mcp_tools/run_agent.py:50` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/run_api.py:30` | `def handle(arguments, tool_name, ctx)` |
| `_publish_command_event` | function | `skills/mcp_tools/run_command.py:61` | `def _publish_command_event(command, output, operator, target)` |
| `_run_with_fallback` | function | `skills/mcp_tools/run_command.py:102` | `def _run_with_fallback(cmd, to)` |
| `handle` | function | `skills/mcp_tools/run_command.py:82` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/run_command_async.py:39` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/search_tools.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/searchsploit.py:79` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/session_diff.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/session_init.py:59` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/session_resume.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/session_state.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/session_status.py:43` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/set_active_target.py:35` | `def handle(arguments, tool_name, ctx)` |
| `coerce_value` | function | `skills/mcp_tools/set_config.py:46` | `def coerce_value(coerce_key, coerce_value_in)` |
| `handle` | function | `skills/mcp_tools/set_config.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/soul.py:42` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/stealth.py:35` | `def handle(arguments, tool_name, ctx)` |
| `_isolated_runner` | function | `skills/mcp_tools/subagent_run.py:86` | `def _isolated_runner(cmd)` |
| `handle` | function | `skills/mcp_tools/subagent_run.py:45` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/swan_ensemble.py:48` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/swan_route.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/swan_run.py:45` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/swan_status.py:23` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/target_context.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/tasks_cleanup.py:37` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/threat_model.py:44` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/timeline.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/ttp_chain.py:47` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/unified_dashboard.py:34` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_eventlogs.py:36` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_exec.py:38` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_gym_list.py:21` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_gym_plan.py:32` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_gym_run.py:33` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_snapshot.py:29` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_status.py:22` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_tools.py:29` | `def handle(arguments, tool_name, ctx)` |
| `handle` | function | `skills/mcp_tools/winbox_vm.py:36` | `def handle(arguments, tool_name, ctx)` |
| `_Handler` | class | `skills/sessions_watcher.py:375` | `class _Handler(FileSystemEventHandler)` |
| `_append_event` | function | `skills/sessions_watcher.py:96` | `def _append_event(ev)` |
| `_call_ollama` | function | `skills/sessions_watcher.py:141` | `def _call_ollama(prompt)` |
| `_dispatch` | function | `skills/sessions_watcher.py:346` | `def _dispatch(path)` |
| `_emit` | function | `skills/sessions_watcher.py:123` | `def _emit(event_type, severity, suggest, source)` |
| `_extract_target_from_filename` | function | `skills/sessions_watcher.py:331` | `def _extract_target_from_filename(name)` |
| `_generate_plan_from_nmap` | function | `skills/sessions_watcher.py:154` | `def _generate_plan_from_nmap(nmap_path)` |
| `_handle_nmap_txt` | function | `skills/sessions_watcher.py:204` | `def _handle_nmap_txt(path)` |
| `_handle_nmap_xml` | function | `skills/sessions_watcher.py:229` | `def _handle_nmap_xml(path)` |
| `_handle_plan_updated` | function | `skills/sessions_watcher.py:318` | `def _handle_plan_updated(path)` |
| `_handle_tool_output` | function | `skills/sessions_watcher.py:257` | `def _handle_tool_output(path)` |
| `_minimal_plan_from_nmap` | function | `skills/sessions_watcher.py:175` | `def _minimal_plan_from_nmap(content)` |
| `_run_poll_loop` | function | `skills/sessions_watcher.py:402` | `def _run_poll_loop()` |
| `_run_watchdog` | function | `skills/sessions_watcher.py:388` | `def _run_watchdog()` |
| `_scan` | function | `skills/sessions_watcher.py:406` | `def _scan()` |
| `main` | function | `skills/sessions_watcher.py:430` | `def main()` |
| `on_created` | method | `skills/sessions_watcher.py:376` | `def on_created(self, event)` |
| `on_modified` | method | `skills/sessions_watcher.py:380` | `def on_modified(self, event)` |
| `add_nopasswd` | function | `skills/setup.sh:92` | `` |
| `die` | function | `skills/setup.sh:17` | `` |
| `info` | function | `skills/setup.sh:15` | `` |
| `paths_for_sudo` | function | `skills/setup.sh:61` | `` |
| `warn` | function | `skills/setup.sh:16` | `` |
| `EnsembleResult` | class | `skills/swan_agent.py:183` | `class EnsembleResult` |
| `ExpertExecutor` | class | `skills/swan_agent.py:332` | `class ExpertExecutor` |
| `ExpertVote` | class | `skills/swan_agent.py:172` | `class ExpertVote` |
| `IResultAggregator` | class | `skills/swan_agent.py:205` | `class IResultAggregator(ABC)` |
| `ISwanOrchestrator` | class | `skills/swan_agent.py:222` | `class ISwanOrchestrator(ABC)` |
| `OutcomeEvaluator` | class | `skills/swan_agent.py:464` | `class OutcomeEvaluator` |
| `SwanOrchestrator` | class | `skills/swan_agent.py:555` | `class SwanOrchestrator(ISwanOrchestrator)` |
| `SwanResult` | class | `skills/swan_agent.py:146` | `class SwanResult` |
| `WeightedTextAggregator` | class | `skills/swan_agent.py:252` | `class WeightedTextAggregator(IResultAggregator)` |
| `__init__` | method | `skills/swan_agent.py:572` | `def __init__(self, executor, evaluator, aggregator, api_key)` |
| `_base_reward` | method | `skills/swan_agent.py:508` | `def _base_reward(self, status, task_type)` |
| `_build_synthesis` | method | `skills/swan_agent.py:284` | `def _build_synthesis(task_type, goal, experts)` |
| `_content_boost` | method | `skills/swan_agent.py:516` | `def _content_boost(output, base_reward)` |
| `_detection_prob` | method | `skills/swan_agent.py:540` | `def _detection_prob(goal, task_type)` |
| `_get_hive_memory` | method | `skills/swan_agent.py:919` | `def _get_hive_memory(self)` |
| `_get_router` | method | `skills/swan_agent.py:908` | `def _get_router(self)` |
| `_get_trainer` | method | `skills/swan_agent.py:914` | `def _get_trainer(self)` |
| `_import_detection_oracle` | function | `skills/swan_agent.py:118` | `def _import_detection_oracle()` |
| `_import_policy` | function | `skills/swan_agent.py:127` | `def _import_policy()` |
| `_import_router` | function | `skills/swan_agent.py:106` | `def _import_router()` |
| `_import_trainer` | function | `skills/swan_agent.py:112` | `def _import_trainer()` |
| `_invoke` | method | `skills/swan_agent.py:394` | `def _invoke(self, backend, model, goal, task_type, api_key, timeout)` |
| `_load_key` | method | `skills/swan_agent.py:930` | `def _load_key()` |
| `_load_payload_key` | method | `skills/swan_agent.py:452` | `def _load_payload_key()` |
| `_next_task_type` | method | `skills/swan_agent.py:893` | `def _next_task_type(task_type)` |
| `_parallel_execute` | method | `skills/swan_agent.py:778` | `def _parallel_execute(self, experts, goal, task_type, timeout)` |
| `_post_execution_update` | method | `skills/swan_agent.py:827` | `def _post_execution_update(self, expert_id, task_type, reward, detection_prob, state_key, next_state, candidate_ids...` |
| `_store_to_hive` | method | `skills/swan_agent.py:860` | `def _store_to_hive(self, result, reward, detection_prob)` |
| `_tools_for_task` | method | `skills/swan_agent.py:417` | `def _tools_for_task(task_type)` |
| `aggregate` | method | `skills/swan_agent.py:209` | `def aggregate(self, task_type, goal, votes)` |
| `aggregate` | method | `skills/swan_agent.py:264` | `def aggregate(self, task_type, goal, votes)` |
| `ensemble_run` | method | `skills/swan_agent.py:236` | `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` |
| `ensemble_run` | method | `skills/swan_agent.py:680` | `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` |
| `evaluate` | method | `skills/swan_agent.py:479` | `def evaluate(self, result, task_type)` |
| `execute` | method | `skills/swan_agent.py:351` | `def execute(self, expert_id, backend, model, goal, task_type, timeout, api_key)` |
| `get_swan` | function | `skills/swan_agent.py:1039` | `def get_swan(api_key)` |
| `is_success` | method | `skills/swan_agent.py:167` | `def is_success(self)` |
| `mcp_swan_ensemble` | function | `skills/swan_agent.py:968` | `def mcp_swan_ensemble(task_type, goal, n_experts, phase)` |
| `mcp_swan_route` | function | `skills/swan_agent.py:1003` | `def mcp_swan_route(task_type, goal)` |
| `mcp_swan_run` | function | `skills/swan_agent.py:945` | `def mcp_swan_run(task_type, goal, phase)` |
| `mcp_swan_status` | function | `skills/swan_agent.py:996` | `def mcp_swan_status()` |
| `run` | method | `skills/swan_agent.py:226` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `run` | method | `skills/swan_agent.py:592` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `status` | method | `skills/swan_agent.py:763` | `def status(self)` |
| `CapturingSelector` | class | `skills/tests/test_autonomous_daemon.py:343` | `class CapturingSelector(ICommandSelector)` |
| `TestCascadeStrategy` | class | `skills/tests/test_autonomous_daemon.py:296` | `class TestCascadeStrategy` |
| `TestCommandRunnerChain` | class | `skills/tests/test_autonomous_daemon.py:134` | `class TestCommandRunnerChain` |
| `TestEmitEvent` | class | `skills/tests/test_autonomous_daemon.py:486` | `class TestEmitEvent` |
| `TestFallbackSelector` | class | `skills/tests/test_autonomous_daemon.py:205` | `class TestFallbackSelector` |
| `TestInjectToTasksJson` | class | `skills/tests/test_autonomous_daemon.py:360` | `class TestInjectToTasksJson` |
| `TestMCPAutonomousInject` | class | `skills/tests/test_autonomous_daemon.py:537` | `class TestMCPAutonomousInject` |
| `TestMCPAutonomousStatus` | class | `skills/tests/test_autonomous_daemon.py:610` | `class TestMCPAutonomousStatus` |
| `TestMCPCommandRunner` | class | `skills/tests/test_autonomous_daemon.py:88` | `class TestMCPCommandRunner` |
| `TestObjectiveLoopUnit` | class | `skills/tests/test_autonomous_daemon.py:666` | `class TestObjectiveLoopUnit` |
| `TestPTYCommandRunner` | class | `skills/tests/test_autonomous_daemon.py:59` | `class TestPTYCommandRunner` |
| `TestParquetSelector` | class | `skills/tests/test_autonomous_daemon.py:248` | `class TestParquetSelector` |
| `TestUpdateTaskStatus` | class | `skills/tests/test_autonomous_daemon.py:437` | `class TestUpdateTaskStatus` |
| `_R` | class | `skills/tests/test_autonomous_daemon.py:140` | `class _R(ICommandRunner)` |
| `_S` | class | `skills/tests/test_autonomous_daemon.py:303` | `class _S(ICommandSelector)` |
| `_failing_run_async` | function | `skills/tests/test_autonomous_daemon.py:784` | `def _failing_run_async(objective_id, objective_text, target)` |
| `_fake_run_async` | function | `skills/tests/test_autonomous_daemon.py:721` | `def _fake_run_async(objective_id, objective_text, target)` |
| `_make_mock_objective` | method | `skills/tests/test_autonomous_daemon.py:683` | `def _make_mock_objective(self)` |
| `_make_mock_store` | method | `skills/tests/test_autonomous_daemon.py:550` | `def _make_mock_store(self)` |
| `_make_runner` | method | `skills/tests/test_autonomous_daemon.py:137` | `def _make_runner(self, name, result, raises)` |
| `_make_selector` | method | `skills/tests/test_autonomous_daemon.py:299` | `def _make_selector(self, returns)` |
| `_next_pending` | function | `skills/tests/test_autonomous_daemon.py:706` | `def _next_pending()` |
| `_next_pending` | function | `skills/tests/test_autonomous_daemon.py:772` | `def _next_pending()` |
| `_patch_paths` | function | `skills/tests/test_autonomous_daemon.py:32` | `def _patch_paths(tmp_path)` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:745` | `def _run_loop()` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:807` | `def _run_loop()` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:831` | `def _run_loop()` |
| `_stop_patchers` | function | `skills/tests/test_autonomous_daemon.py:49` | `def _stop_patchers(patchers)` |
| `_write_tasks` | method | `skills/tests/test_autonomous_daemon.py:450` | `def _write_tasks(self, tasks)` |
| `name` | method | `skills/tests/test_autonomous_daemon.py:142` | `def name(self)` |
| `run` | method | `skills/tests/test_autonomous_daemon.py:145` | `def run(self, command, timeout)` |
| `select` | method | `skills/tests/test_autonomous_daemon.py:304` | `def select(self, target, phase, context)` |
| `select` | method | `skills/tests/test_autonomous_daemon.py:344` | `def select(self, target, phase, context)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:363` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:440` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:489` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:540` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:613` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:673` | `def setup_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:369` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:446` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:495` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:546` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:619` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:679` | `def teardown_method(self)` |
| `test_always_returns_decision` | method | `skills/tests/test_autonomous_daemon.py:208` | `def test_always_returns_decision(self)` |
| `test_appends_new_task` | method | `skills/tests/test_autonomous_daemon.py:382` | `def test_appends_new_task(self)` |
| `test_block_called_on_execution_failure` | method | `skills/tests/test_autonomous_daemon.py:760` | `def test_block_called_on_execution_failure(self)` |
| `test_complete_called_after_successful_execution` | method | `skills/tests/test_autonomous_daemon.py:692` | `def test_complete_called_after_successful_execution(self)` |
| `test_contains_expected_fields` | method | `skills/tests/test_autonomous_daemon.py:631` | `def test_contains_expected_fields(self)` |
| `test_correct_schema` | method | `skills/tests/test_autonomous_daemon.py:394` | `def test_correct_schema(self)` |
| `test_creates_file_if_missing` | method | `skills/tests/test_autonomous_daemon.py:373` | `def test_creates_file_if_missing(self)` |
| `test_delegates_to_mcp_when_available` | method | `skills/tests/test_autonomous_daemon.py:114` | `def test_delegates_to_mcp_when_available(self)` |
| `test_event_has_required_fields` | method | `skills/tests/test_autonomous_daemon.py:511` | `def test_event_has_required_fields(self)` |
| `test_falls_back_to_second_on_exception` | method | `skills/tests/test_autonomous_daemon.py:162` | `def test_falls_back_to_second_on_exception(self)` |
| `test_handles_existing_invalid_json` | method | `skills/tests/test_autonomous_daemon.py:421` | `def test_handles_existing_invalid_json(self)` |
| `test_ignores_missing_title` | method | `skills/tests/test_autonomous_daemon.py:465` | `def test_ignores_missing_title(self)` |
| `test_implements_icommand_runner` | method | `skills/tests/test_autonomous_daemon.py:76` | `def test_implements_icommand_runner(self)` |
| `test_injects_to_objective_store_and_tasks_json` | method | `skills/tests/test_autonomous_daemon.py:562` | `def test_injects_to_objective_store_and_tasks_json(self)` |
| `test_instantiation` | method | `skills/tests/test_autonomous_daemon.py:62` | `def test_instantiation(self)` |
| `test_instantiation` | method | `skills/tests/test_autonomous_daemon.py:91` | `def test_instantiation(self)` |
| `test_loop_disabled_when_objective_store_missing` | method | `skills/tests/test_autonomous_daemon.py:821` | `def test_loop_disabled_when_objective_store_missing(self)` |
| `test_merges_status_file_when_present` | method | `skills/tests/test_autonomous_daemon.py:650` | `def test_merges_status_file_when_present(self)` |
| `test_multiple_emits_append_lines` | method | `skills/tests/test_autonomous_daemon.py:521` | `def test_multiple_emits_append_lines(self)` |
| `test_name_property` | method | `skills/tests/test_autonomous_daemon.py:69` | `def test_name_property(self)` |
| `test_name_property` | method | `skills/tests/test_autonomous_daemon.py:98` | `def test_name_property(self)` |
| `test_name_reflects_all_runners` | method | `skills/tests/test_autonomous_daemon.py:182` | `def test_name_reflects_all_runners(self)` |
| `test_passes_context_to_selectors` | method | `skills/tests/test_autonomous_daemon.py:337` | `def test_passes_context_to_selectors(self)` |
| `test_raises_when_all_fail` | method | `skills/tests/test_autonomous_daemon.py:172` | `def test_raises_when_all_fail(self)` |
| `test_raises_when_import_fails` | method | `skills/tests/test_autonomous_daemon.py:105` | `def test_raises_when_import_fails(self)` |
| `test_requires_at_least_one_runner` | method | `skills/tests/test_autonomous_daemon.py:192` | `def test_requires_at_least_one_runner(self)` |
| `test_respects_fail_counts` | method | `skills/tests/test_autonomous_daemon.py:275` | `def test_respects_fail_counts(self)` |
| `test_returns_assigned_id` | method | `skills/tests/test_autonomous_daemon.py:412` | `def test_returns_assigned_id(self)` |
| `test_returns_candidate_when_pdb_has_history` | method | `skills/tests/test_autonomous_daemon.py:259` | `def test_returns_candidate_when_pdb_has_history(self)` |
| `test_returns_command_decision_type` | method | `skills/tests/test_autonomous_daemon.py:216` | `def test_returns_command_decision_type(self)` |
| `test_returns_error_string_when_store_unavailable` | method | `skills/tests/test_autonomous_daemon.py:596` | `def test_returns_error_string_when_store_unavailable(self)` |
| `test_returns_false_when_file_missing` | method | `skills/tests/test_autonomous_daemon.py:473` | `def test_returns_false_when_file_missing(self)` |
| `test_returns_first_non_none_result` | method | `skills/tests/test_autonomous_daemon.py:309` | `def test_returns_first_non_none_result(self)` |
| `test_returns_json_with_both_ids` | method | `skills/tests/test_autonomous_daemon.py:581` | `def test_returns_json_with_both_ids(self)` |
| `test_returns_none_when_pdb_unavailable` | method | `skills/tests/test_autonomous_daemon.py:251` | `def test_returns_none_when_pdb_unavailable(self)` |
| `test_returns_valid_json` | method | `skills/tests/test_autonomous_daemon.py:623` | `def test_returns_valid_json(self)` |
| `test_running_is_false_when_no_daemon` | method | `skills/tests/test_autonomous_daemon.py:641` | `def test_running_is_false_when_no_daemon(self)` |
| `test_source_is_fallback` | method | `skills/tests/test_autonomous_daemon.py:225` | `def test_source_is_fallback(self)` |
| `test_unknown_phase_returns_decision` | method | `skills/tests/test_autonomous_daemon.py:233` | `def test_unknown_phase_returns_decision(self)` |
| `test_updates_existing_task` | method | `skills/tests/test_autonomous_daemon.py:455` | `def test_updates_existing_task(self)` |
| `test_uses_fallback_when_all_none` | method | `skills/tests/test_autonomous_daemon.py:325` | `def test_uses_fallback_when_all_none(self)` |
| `test_uses_first_runner_when_successful` | method | `skills/tests/test_autonomous_daemon.py:152` | `def test_uses_first_runner_when_successful(self)` |
| `test_writes_valid_json_line` | method | `skills/tests/test_autonomous_daemon.py:499` | `def test_writes_valid_json_line(self)` |
| `TestCrackMapExecParser` | class | `skills/tests/test_facts.py:61` | `class TestCrackMapExecParser` |
| `TestEnum4linuxParser` | class | `skills/tests/test_facts.py:81` | `class TestEnum4linuxParser` |
| `TestFactStore` | class | `skills/tests/test_facts.py:300` | `class TestFactStore` |
| `TestGobusterParser` | class | `skills/tests/test_facts.py:149` | `class TestGobusterParser` |
| `TestKerbruteParser` | class | `skills/tests/test_facts.py:119` | `class TestKerbruteParser` |
| `TestNiktoParser` | class | `skills/tests/test_facts.py:176` | `class TestNiktoParser` |
| `TestNmapXmlParser` | class | `skills/tests/test_facts.py:246` | `class TestNmapXmlParser` |
| `TestNucleiParser` | class | `skills/tests/test_facts.py:196` | `class TestNucleiParser` |
| `TestRpcclientParser` | class | `skills/tests/test_facts.py:138` | `class TestRpcclientParser` |
| `TestSecretsdumpParser` | class | `skills/tests/test_facts.py:105` | `class TestSecretsdumpParser` |
| `TestSslscanParser` | class | `skills/tests/test_facts.py:218` | `class TestSslscanParser` |
| `_make_config` | function | `skills/tests/test_facts.py:42` | `def _make_config(tmp_path)` |
| `test_context_for_command` | method | `skills/tests/test_facts.py:322` | `def test_context_for_command(self, tmp_path)` |
| `test_context_for_unknown_host` | method | `skills/tests/test_facts.py:356` | `def test_context_for_unknown_host(self, tmp_path)` |
| `test_crackmapexec_parser` | method | `skills/tests/test_facts.py:62` | `def test_crackmapexec_parser(self)` |
| `test_crackmapexec_pwned` | method | `skills/tests/test_facts.py:73` | `def test_crackmapexec_pwned(self)` |
| `test_dedup_creds` | method | `skills/tests/test_facts.py:429` | `def test_dedup_creds(self, tmp_path)` |
| `test_enum4linux_access_when_results` | method | `skills/tests/test_facts.py:97` | `def test_enum4linux_access_when_results(self)` |
| `test_enum4linux_parser` | method | `skills/tests/test_facts.py:82` | `def test_enum4linux_parser(self)` |
| `test_factstore_dedup` | method | `skills/tests/test_facts.py:301` | `def test_factstore_dedup(self, tmp_path)` |
| `test_factstore_save_and_reload` | method | `skills/tests/test_facts.py:363` | `def test_factstore_save_and_reload(self, tmp_path)` |
| `test_gobuster_multiple_paths` | method | `skills/tests/test_facts.py:162` | `def test_gobuster_multiple_paths(self)` |
| `test_gobuster_parser_parse_extended` | method | `skills/tests/test_facts.py:150` | `def test_gobuster_parser_parse_extended(self)` |
| `test_ingest_text_crackmapexec` | method | `skills/tests/test_facts.py:416` | `def test_ingest_text_crackmapexec(self, tmp_path)` |
| `test_ingest_xml` | method | `skills/tests/test_facts.py:390` | `def test_ingest_xml(self, tmp_path)` |
| `test_kerbrute_multiple_users` | method | `skills/tests/test_facts.py:129` | `def test_kerbrute_multiple_users(self)` |
| `test_kerbrute_parser` | method | `skills/tests/test_facts.py:120` | `def test_kerbrute_parser(self)` |
| `test_nikto_cve_line` | method | `skills/tests/test_facts.py:189` | `def test_nikto_cve_line(self)` |
| `test_nikto_parser_parse_extended` | method | `skills/tests/test_facts.py:177` | `def test_nikto_parser_parse_extended(self)` |
| `test_nmap_xml_parse` | method | `skills/tests/test_facts.py:270` | `def test_nmap_xml_parse(self, tmp_path)` |
| `test_nmap_xml_parse_invalid` | method | `skills/tests/test_facts.py:286` | `def test_nmap_xml_parse_invalid(self, tmp_path)` |
| `test_nuclei_multiple_severities` | method | `skills/tests/test_facts.py:209` | `def test_nuclei_multiple_severities(self)` |
| `test_nuclei_parser_parse_extended` | method | `skills/tests/test_facts.py:197` | `def test_nuclei_parser_parse_extended(self)` |
| `test_rpcclient_parser` | method | `skills/tests/test_facts.py:139` | `def test_rpcclient_parser(self)` |
| `test_secretsdump_parser` | method | `skills/tests/test_facts.py:106` | `def test_secretsdump_parser(self)` |
| `test_sslscan_dedup` | method | `skills/tests/test_facts.py:231` | `def test_sslscan_dedup(self)` |
| `test_sslscan_parser_parse_extended` | method | `skills/tests/test_facts.py:219` | `def test_sslscan_parser_parse_extended(self)` |
| `check` | function | `skills/tests/test_harness_e2e.py:33` | `def check(label, cond, hint)` |
| `main` | function | `skills/tests/test_harness_e2e.py:391` | `def main()` |
| `test_auto_compact` | function | `skills/tests/test_harness_e2e.py:263` | `def test_auto_compact(tmp)` |
| `test_claudemd` | function | `skills/tests/test_harness_e2e.py:228` | `def test_claudemd(tmp)` |
| `test_compaction` | function | `skills/tests/test_harness_e2e.py:98` | `def test_compaction()` |
| `test_hooks` | function | `skills/tests/test_harness_e2e.py:182` | `def test_hooks(tmp)` |
| `test_integration` | function | `skills/tests/test_harness_e2e.py:332` | `def test_integration(tmp)` |
| `test_metrics` | function | `skills/tests/test_harness_e2e.py:300` | `def test_metrics(tmp)` |
| `test_permissions` | function | `skills/tests/test_harness_e2e.py:47` | `def test_permissions(tmp)` |
| `test_transcript` | function | `skills/tests/test_harness_e2e.py:143` | `def test_transcript(tmp)` |
| `TestDronePool` | class | `skills/tests/test_hive_mind.py:346` | `class TestDronePool` |
| `TestDronePoolWithPersistence` | class | `skills/tests/test_hive_mind.py:770` | `class TestDronePoolWithPersistence` |
| `TestDroneStateStore` | class | `skills/tests/test_hive_mind.py:673` | `class TestDroneStateStore` |
| `TestEpisodicStore` | class | `skills/tests/test_hive_mind.py:72` | `class TestEpisodicStore` |
| `TestHiveBus` | class | `skills/tests/test_hive_mind.py:293` | `class TestHiveBus` |
| `TestHiveMemory` | class | `skills/tests/test_hive_mind.py:226` | `class TestHiveMemory` |
| `TestHiveMind` | class | `skills/tests/test_hive_mind.py:509` | `class TestHiveMind` |
| `TestMCPHandlers` | class | `skills/tests/test_hive_mind.py:575` | `class TestMCPHandlers` |
| `TestQueenBrain` | class | `skills/tests/test_hive_mind.py:428` | `class TestQueenBrain` |
| `TestSemanticStore` | class | `skills/tests/test_hive_mind.py:152` | `class TestSemanticStore` |
| `_build_hive_and_patch` | method | `skills/tests/test_hive_mind.py:588` | `def _build_hive_and_patch(self)` |
| `_instant_run` | function | `skills/tests/test_hive_mind.py:405` | `def _instant_run(self_inner)` |
| `_make_episodic` | function | `skills/tests/test_hive_mind.py:32` | `def _make_episodic(tmp_path)` |
| `_make_hive` | method | `skills/tests/test_hive_mind.py:519` | `def _make_hive(self)` |
| `_make_hive_memory` | function | `skills/tests/test_hive_mind.py:49` | `def _make_hive_memory(tmp_path)` |
| `_make_pool` | method | `skills/tests/test_hive_mind.py:356` | `def _make_pool(self)` |
| `_make_pool_with_store` | method | `skills/tests/test_hive_mind.py:780` | `def _make_pool_with_store(self)` |
| `_make_queen` | method | `skills/tests/test_hive_mind.py:438` | `def _make_queen(self)` |
| `_make_semantic` | function | `skills/tests/test_hive_mind.py:39` | `def _make_semantic(tmp_path, episodic)` |
| `_make_state` | method | `skills/tests/test_hive_mind.py:688` | `def _make_state(self, status)` |
| `_make_store` | method | `skills/tests/test_hive_mind.py:683` | `def _make_store(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:75` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:155` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:229` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:296` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:349` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:431` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:512` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:578` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:676` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:773` | `def setup_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:79` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:159` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:233` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:353` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:435` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:516` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:584` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:680` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:777` | `def teardown_method(self)` |
| `test_active_count_decrements_when_done` | method | `skills/tests/test_hive_mind.py:401` | `def test_active_count_decrements_when_done(self)` |
| `test_broadcast_received_by_everyone` | method | `skills/tests/test_hive_mind.py:312` | `def test_broadcast_received_by_everyone(self)` |
| `test_count_returns_zero_when_unavailable` | method | `skills/tests/test_hive_mind.py:212` | `def test_count_returns_zero_when_unavailable(self)` |
| `test_delete_older_than_removes_stale` | method | `skills/tests/test_hive_mind.py:750` | `def test_delete_older_than_removes_stale(self)` |
| `test_dispatch_returns_drone_ids` | method | `skills/tests/test_hive_mind.py:480` | `def test_dispatch_returns_drone_ids(self)` |
| `test_drone_result_unknown_id` | method | `skills/tests/test_hive_mind.py:557` | `def test_drone_result_unknown_id(self)` |
| `test_fallback_to_episodic_when_chroma_unavailable` | method | `skills/tests/test_hive_mind.py:179` | `def test_fallback_to_episodic_when_chroma_unavailable(self)` |
| `test_forget_by_topic` | method | `skills/tests/test_hive_mind.py:132` | `def test_forget_by_topic(self)` |
| `test_forget_delegates_to_episodic` | method | `skills/tests/test_hive_mind.py:277` | `def test_forget_delegates_to_episodic(self)` |
| `test_forget_old_events` | method | `skills/tests/test_hive_mind.py:121` | `def test_forget_old_events(self)` |
| `test_forget_returns_int` | method | `skills/tests/test_hive_mind.py:563` | `def test_forget_returns_int(self)` |

Next: [SYMBOLS_p30.md](SYMBOLS_p30.md)
