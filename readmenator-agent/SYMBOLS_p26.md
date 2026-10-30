# Symbols (page 26 of 48)
Previous: [SYMBOLS_p25.md](SYMBOLS_p25.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `sandbox_hook` | function | `skills/lazyown_hooks.py:101` | `def sandbox_hook(context)` |
| `start_timer_hook` | function | `skills/lazyown_hooks.py:176` | `def start_timer_hook(context)` |
| `timing_hook` | function | `skills/lazyown_hooks.py:161` | `def timing_hook(context)` |
| `LLMBridge` | class | `skills/lazyown_llm.py:97` | `class LLMBridge` |
| `LLMTool` | class | `skills/lazyown_llm.py:71` | `class LLMTool` |
| `__init__` | method | `skills/lazyown_llm.py:104` | `def __init__(self, backend, model, api_key)` |
| `_ask_groq` | method | `skills/lazyown_llm.py:140` | `def _ask_groq(self, goal, context, max_iterations, system_prompt)` |
| `_ask_ollama_react` | method | `skills/lazyown_llm.py:238` | `def _ask_ollama_react(self, goal, context, max_iterations, system_prompt)` |
| `_call_tool` | method | `skills/lazyown_llm.py:318` | `def _call_tool(self, name, args)` |
| `_default_system_prompt` | function | `skills/lazyown_llm.py:455` | `def _default_system_prompt(tool_names)` |
| `_groq_request` | method | `skills/lazyown_llm.py:201` | `def _groq_request(self, messages, tools)` |
| `_make_default_tools` | function | `skills/lazyown_llm.py:334` | `def _make_default_tools(bridge)` |
| `_ollama_generate` | method | `skills/lazyown_llm.py:305` | `def _ollama_generate(self, prompt)` |
| `ask` | method | `skills/lazyown_llm.py:127` | `def ask(self, goal, context, max_iterations, system_prompt)` |
| `build_bridge` | function | `skills/lazyown_llm.py:438` | `def build_bridge(backend, model, api_key, with_default_tools)` |
| `llm_ask` | function | `skills/lazyown_llm.py:468` | `def llm_ask(goal, context, backend, model, api_key, max_iterations, system_prompt, extra_tools)` |
| `main` | function | `skills/lazyown_llm.py:493` | `def main()` |
| `openai_schema` | method | `skills/lazyown_llm.py:79` | `def openai_schema(self)` |
| `read_facts` | function | `skills/lazyown_llm.py:376` | `def read_facts(target)` |
| `read_nmap` | function | `skills/lazyown_llm.py:352` | `def read_nmap(target)` |
| `read_objectives` | function | `skills/lazyown_llm.py:389` | `def read_objectives(limit)` |
| `read_plan` | function | `skills/lazyown_llm.py:369` | `def read_plan()` |
| `register_tool` | method | `skills/lazyown_llm.py:118` | `def register_tool(self, name, description, parameters, func)` |
| `run_command` | function | `skills/lazyown_llm.py:346` | `def run_command(command)` |
| `_add` | function | `skills/lazyown_mcp.py:1778` | `def _add(user, secret, host, source, confirmed)` |
| `_blocking_run` | function | `skills/lazyown_mcp.py:10347` | `def _blocking_run()` |
| `_c2_creds` | function | `skills/lazyown_mcp.py:519` | `def _c2_creds()` |
| `_c2_request` | function | `skills/lazyown_mcp.py:529` | `def _c2_request(path, method, body)` |
| `_compact` | function | `skills/lazyown_mcp.py:398` | `def _compact(content, tool_name)` |
| `_compact_output_fn` | function | `skills/lazyown_mcp.py:408` | `def _compact_output_fn(c, t)` |
| `_create_tool_file` | function | `skills/lazyown_mcp.py:200` | `def _create_tool_file()` |
| `_decorator` | function | `skills/lazyown_mcp.py:611` | `def _decorator(func)` |
| `_deploy_beacon_sync` | function | `skills/lazyown_mcp.py:11085` | `def _deploy_beacon_sync()` |
| `_dispatch_perm_check` | function | `skills/lazyown_mcp.py:630` | `def _dispatch_perm_check(name, arguments)` |
| `_do_facts` | function | `skills/lazyown_mcp.py:1841` | `def _do_facts()` |
| `_ensure_aci` | function | `skills/lazyown_mcp.py:317` | `def _ensure_aci()` |
| `_ensure_auto` | function | `skills/lazyown_mcp.py:297` | `def _ensure_auto()` |
| `_ensure_automapper` | function | `skills/lazyown_mcp.py:242` | `def _ensure_automapper()` |
| `_ensure_bridge` | function | `skills/lazyown_mcp.py:99` | `def _ensure_bridge()` |
| `_ensure_engine` | function | `skills/lazyown_mcp.py:81` | `def _ensure_engine()` |
| `_ensure_facts` | function | `skills/lazyown_mcp.py:193` | `def _ensure_facts()` |
| `_ensure_hive` | function | `skills/lazyown_mcp.py:269` | `def _ensure_hive()` |
| `_ensure_llm` | function | `skills/lazyown_mcp.py:231` | `def _ensure_llm()` |
| `_ensure_narrator` | function | `skills/lazyown_mcp.py:172` | `def _ensure_narrator()` |
| `_ensure_objectives` | function | `skills/lazyown_mcp.py:211` | `def _ensure_objectives()` |
| `_ensure_pdb` | function | `skills/lazyown_mcp.py:252` | `def _ensure_pdb()` |
| `_ensure_policy` | function | `skills/lazyown_mcp.py:183` | `def _ensure_policy()` |
| `_ensure_recommender` | function | `skills/lazyown_mcp.py:125` | `def _ensure_recommender()` |
| `_ensure_state` | function | `skills/lazyown_mcp.py:114` | `def _ensure_state()` |
| `_fail` | function | `skills/lazyown_mcp.py:1023` | `def _fail(message, remediation)` |
| `_fused_recommendations` | function | `skills/lazyown_mcp.py:9148` | `def _fused_recommendations()` |
| `_get_claudemd` | function | `skills/lazyown_mcp.py:414` | `def _get_claudemd()` |
| `_get_hooks` | function | `skills/lazyown_mcp.py:372` | `def _get_hooks()` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:258` | `def _get_pdb(_)` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:338` | `def _get_pdb(_)` |
| `_get_perm_system` | function | `skills/lazyown_mcp.py:359` | `def _get_perm_system()` |
| `_get_transcript` | function | `skills/lazyown_mcp.py:385` | `def _get_transcript()` |
| `_h_ack_event` | function | `skills/lazyown_mcp.py:957` | `def _h_ack_event(arguments, tool_name)` |
| `_h_auto_pwn` | function | `skills/lazyown_mcp.py:1238` | `def _h_auto_pwn(arguments, tool_name)` |
| `_h_c2_status` | function | `skills/lazyown_mcp.py:969` | `def _h_c2_status(arguments, tool_name)` |
| `_h_credentials` | function | `skills/lazyown_mcp.py:1772` | `def _h_credentials(arguments, tool_name)` |
| `_h_dashboard_snapshot` | function | `skills/lazyown_mcp.py:1199` | `def _h_dashboard_snapshot(arguments, tool_name)` |
| `_h_db` | function | `skills/lazyown_mcp.py:676` | `def _h_db(arguments, tool_name)` |
| `_h_evasion_generate` | function | `skills/lazyown_mcp.py:1150` | `def _h_evasion_generate(arguments, tool_name)` |
| `_h_evasion_rotate` | function | `skills/lazyown_mcp.py:1165` | `def _h_evasion_rotate(arguments, tool_name)` |
| `_h_exploit_chain` | function | `skills/lazyown_mcp.py:1271` | `def _h_exploit_chain(arguments, tool_name)` |
| `_h_exploit_recommend` | function | `skills/lazyown_mcp.py:1126` | `def _h_exploit_recommend(arguments, tool_name)` |
| `_h_exploitgym_list` | function | `skills/lazyown_mcp.py:1865` | `def _h_exploitgym_list(arguments, tool_name)` |
| `_h_exploitgym_run` | function | `skills/lazyown_mcp.py:1881` | `def _h_exploitgym_run(arguments, tool_name)` |
| `_h_exploitgym_score` | function | `skills/lazyown_mcp.py:1901` | `def _h_exploitgym_score(arguments, tool_name)` |
| `_h_exploitgym_status` | function | `skills/lazyown_mcp.py:1851` | `def _h_exploitgym_status(arguments, tool_name)` |
| `_h_facts_show` | function | `skills/lazyown_mcp.py:1831` | `def _h_facts_show(arguments, tool_name)` |
| `_h_get_beacons` | function | `skills/lazyown_mcp.py:1232` | `def _h_get_beacons(arguments, tool_name)` |
| `_h_get_config` | function | `skills/lazyown_mcp.py:670` | `def _h_get_config(arguments, tool_name)` |
| `_h_get_llm_budget` | function | `skills/lazyown_mcp.py:808` | `def _h_get_llm_budget(arguments, tool_name)` |
| `_h_inject_objective` | function | `skills/lazyown_mcp.py:1752` | `def _h_inject_objective(arguments, tool_name)` |
| `_h_lazy_addon` | function | `skills/lazyown_mcp.py:1576` | `def _h_lazy_addon(arguments, tool_name)` |
| `_h_lazy_board` | function | `skills/lazyown_mcp.py:1351` | `def _h_lazy_board(arguments, tool_name)` |
| `_h_lazy_compact` | function | `skills/lazyown_mcp.py:1552` | `def _h_lazy_compact(arguments, tool_name)` |
| `_h_lazy_delete` | function | `skills/lazyown_mcp.py:1527` | `def _h_lazy_delete(arguments, tool_name)` |
| `_h_lazy_finding` | function | `skills/lazyown_mcp.py:1456` | `def _h_lazy_finding(arguments, tool_name)` |
| `_h_lazy_hint` | function | `skills/lazyown_mcp.py:1391` | `def _h_lazy_hint(arguments, tool_name)` |
| `_h_lazy_mention` | function | `skills/lazyown_mcp.py:1496` | `def _h_lazy_mention(arguments, tool_name)` |
| `_h_lazy_proxy` | function | `skills/lazyown_mcp.py:1431` | `def _h_lazy_proxy(arguments, tool_name)` |
| `_h_lazy_status` | function | `skills/lazyown_mcp.py:1331` | `def _h_lazy_status(arguments, tool_name)` |
| `_h_lazy_sync` | function | `skills/lazyown_mcp.py:1341` | `def _h_lazy_sync(arguments, tool_name)` |
| `_h_lazy_trace` | function | `skills/lazyown_mcp.py:1374` | `def _h_lazy_trace(arguments, tool_name)` |
| `_h_lazy_workspace` | function | `skills/lazyown_mcp.py:1410` | `def _h_lazy_workspace(arguments, tool_name)` |
| `_h_list_modules` | function | `skills/lazyown_mcp.py:870` | `def _h_list_modules(arguments, tool_name)` |
| `_h_lolbas_list` | function | `skills/lazyown_mcp.py:1604` | `def _h_lolbas_list(arguments, tool_name)` |
| `_h_lolbas_use` | function | `skills/lazyown_mcp.py:1644` | `def _h_lolbas_use(arguments, tool_name)` |
| `_h_loop_smoke` | function | `skills/lazyown_mcp.py:2139` | `def _h_loop_smoke(arguments, tool_name)` |
| `_h_opencode_config` | function | `skills/lazyown_mcp.py:2117` | `def _h_opencode_config(arguments, tool_name)` |
| `_h_pivot_status` | function | `skills/lazyown_mcp.py:1179` | `def _h_pivot_status(arguments, tool_name)` |
| `_h_rea` | function | `skills/lazyown_mcp.py:1011` | `def _h_rea(arguments, tool_name)` |
| `_h_rich_tui_snapshot` | function | `skills/lazyown_mcp.py:1718` | `def _h_rich_tui_snapshot(arguments, tool_name)` |
| `_h_run_command` | function | `skills/lazyown_mcp.py:892` | `def _h_run_command(arguments, tool_name)` |
| `_h_set_config` | function | `skills/lazyown_mcp.py:845` | `def _h_set_config(arguments, tool_name)` |
| `_h_stealth` | function | `skills/lazyown_mcp.py:1694` | `def _h_stealth(arguments, tool_name)` |
| `_h_unified_dashboard` | function | `skills/lazyown_mcp.py:1219` | `def _h_unified_dashboard(arguments, tool_name)` |
| `_h_winbox_eventlogs` | function | `skills/lazyown_mcp.py:2018` | `def _h_winbox_eventlogs(arguments, tool_name)` |
| `_h_winbox_exec` | function | `skills/lazyown_mcp.py:1965` | `def _h_winbox_exec(arguments, tool_name)` |
| `_h_winbox_gym_list` | function | `skills/lazyown_mcp.py:2061` | `def _h_winbox_gym_list(arguments, tool_name)` |
| `_h_winbox_gym_plan` | function | `skills/lazyown_mcp.py:2074` | `def _h_winbox_gym_plan(arguments, tool_name)` |
| `_h_winbox_gym_run` | function | `skills/lazyown_mcp.py:2092` | `def _h_winbox_gym_run(arguments, tool_name)` |
| `_h_winbox_snapshot` | function | `skills/lazyown_mcp.py:2040` | `def _h_winbox_snapshot(arguments, tool_name)` |
| `_h_winbox_status` | function | `skills/lazyown_mcp.py:1920` | `def _h_winbox_status(arguments, tool_name)` |
| `_h_winbox_tools` | function | `skills/lazyown_mcp.py:1995` | `def _h_winbox_tools(arguments, tool_name)` |
| `_h_winbox_vm` | function | `skills/lazyown_mcp.py:1935` | `def _h_winbox_vm(arguments, tool_name)` |
| `_handle_messages` | function | `skills/lazyown_mcp.py:12009` | `def _handle_messages(scope, receive, send)` |
| `_handle_sighup` | function | `skills/lazyown_mcp.py:11976` | `def _handle_sighup(signum, frame)` |
| `_handle_sse` | function | `skills/lazyown_mcp.py:12005` | `def _handle_sse(request)` |
| `_has_data` | function | `skills/lazyown_mcp.py:495` | `def _has_data(path)` |
| `_is_lab_target` | function | `skills/lazyown_mcp.py:552` | `def _is_lab_target(name)` |
| `_isolated_runner` | function | `skills/lazyown_mcp.py:11881` | `def _isolated_runner(cmd)` |
| `_launch` | function | `skills/lazyown_mcp.py:11445` | `def _launch()` |
| `_load` | function | `skills/lazyown_mcp.py:82` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:100` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:115` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:126` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:173` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:184` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:194` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:212` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:232` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:243` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:253` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:270` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:298` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:318` | `def _load(ns)` |
| `_load_crons` | function | `skills/lazyown_mcp.py:10983` | `def _load_crons()` |
| `_load_payload` | function | `skills/lazyown_mcp.py:486` | `def _load_payload()` |
| `_make_text` | function | `skills/lazyown_mcp.py:618` | `def _make_text(tool_name, content)` |
| `_mcp_executor` | function | `skills/lazyown_mcp.py:9519` | `def _mcp_executor(command, target)` |
| `_read_docstring` | function | `skills/lazyown_mcp.py:8256` | `def _read_docstring(cmd_name)` |
| `_read_prompt` | function | `skills/lazyown_mcp.py:9383` | `def _read_prompt()` |
| `_result` | function | `skills/lazyown_mcp.py:696` | `def _result(payload)` |
| `_run_campaign` | function | `skills/lazyown_mcp.py:11290` | `def _run_campaign()` |
| `_run_daemon` | function | `skills/lazyown_mcp.py:11360` | `def _run_daemon()` |
| `_run_lazyown_command` | function | `skills/lazyown_mcp.py:2195` | `def _run_lazyown_command(command, timeout)` |
| `_run_parquet_query` | function | `skills/lazyown_mcp.py:11224` | `def _run_parquet_query()` |
| `_run_rea` | function | `skills/lazyown_mcp.py:1098` | `def _run_rea()` |
| `_run_with_fallback` | function | `skills/lazyown_mcp.py:909` | `def _run_with_fallback(cmd, to)` |
| `_runner` | function | `skills/lazyown_mcp.py:7293` | `def _runner(cmd)` |
| `_save_crons` | function | `skills/lazyown_mcp.py:10994` | `def _save_crons(entries)` |
| `_save_payload` | function | `skills/lazyown_mcp.py:500` | `def _save_payload(data)` |
| `_sitrep_recommendations` | function | `skills/lazyown_mcp.py:135` | `def _sitrep_recommendations(limit)` |
| `_verified_context` | function | `skills/lazyown_mcp.py:542` | `def _verified_context()` |
| `call_tool` | function | `skills/lazyown_mcp.py:6866` | `def call_tool(name, arguments)` |
| `coerce_value` | function | `skills/lazyown_mcp.py:854` | `def coerce_value(k, v)` |
| `list_tools` | function | `skills/lazyown_mcp.py:2298` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp.py:11987` | `def main()` |
| `register_handler` | function | `skills/lazyown_mcp.py:604` | `def register_handler(tool_name)` |
| `substitute_playbook_target` | function | `skills/lazyown_mcp.py:6848` | `def substitute_playbook_target(command, target)` |
| `text` | function | `skills/lazyown_mcp.py:6880` | `def text(content)` |
| `JobRecord` | class | `skills/lazyown_mcp_helpers.py:672` | `class JobRecord` |
| `JobStore` | class | `skills/lazyown_mcp_helpers.py:686` | `class JobStore` |
| `TaskAudit` | class | `skills/lazyown_mcp_helpers.py:153` | `class TaskAudit` |
| `__init__` | method | `skills/lazyown_mcp_helpers.py:689` | `def __init__(self, max_jobs)` |
| `_format_age` | function | `skills/lazyown_mcp_helpers.py:112` | `def _format_age(seconds)` |
| `_worker` | function | `skills/lazyown_mcp_helpers.py:709` | `def _worker()` |
| `audit_tasks` | function | `skills/lazyown_mcp_helpers.py:165` | `def audit_tasks(tasks, min_confidence)` |
| `build_target_context` | function | `skills/lazyown_mcp_helpers.py:414` | `def build_target_context(host, port, sessions_dir, payload, world_model)` |
| `collect_pwntomate_evidence` | function | `skills/lazyown_mcp_helpers.py:376` | `def collect_pwntomate_evidence(rhost, sessions_dir)` |
| `diff_snapshot` | function | `skills/lazyown_mcp_helpers.py:792` | `def diff_snapshot(sessions_dir, payload, world_model, tasks)` |
| `evidence_freshness` | function | `skills/lazyown_mcp_helpers.py:67` | `def evidence_freshness(path, threshold_seconds, now)` |
| `evidence_grep` | function | `skills/lazyown_mcp_helpers.py:297` | `def evidence_grep(pattern, sessions_dir, scope, max_matches, max_file_bytes, case_insensitive)` |
| `find_credential_provenance` | function | `skills/lazyown_mcp_helpers.py:196` | `def find_credential_provenance(value, sessions_dir, csv_name)` |
| `is_likely_credential` | function | `skills/lazyown_mcp_helpers.py:37` | `def is_likely_credential(value)` |
| `list` | method | `skills/lazyown_mcp_helpers.py:732` | `def list(self, limit)` |
| `needs_confirmation` | function | `skills/lazyown_mcp_helpers.py:875` | `def needs_confirmation(tool_name, arguments)` |
| `parse_task_value` | function | `skills/lazyown_mcp_helpers.py:125` | `def parse_task_value(title)` |
| `preflight_command` | function | `skills/lazyown_mcp_helpers.py:575` | `def preflight_command(command, payload, sessions_dir)` |
| `status` | method | `skills/lazyown_mcp_helpers.py:727` | `def status(self, job_id)` |
| `submit` | method | `skills/lazyown_mcp_helpers.py:694` | `def submit(self, command, runner, timeout)` |
| `take_snapshot` | function | `skills/lazyown_mcp_helpers.py:747` | `def take_snapshot(sessions_dir, payload, world_model, tasks)` |
| `_call_harness_tool` | function | `skills/lazyown_mcp_opencode.py:126` | `def _call_harness_tool(name, arguments)` |
| `_harness_result` | function | `skills/lazyown_mcp_opencode.py:122` | `def _harness_result(payload)` |
| `_sync_harness` | function | `skills/lazyown_mcp_opencode.py:104` | `def _sync_harness()` |
| `call_tool` | function | `skills/lazyown_mcp_opencode.py:201` | `def call_tool(name, arguments)` |
| `list_tools` | function | `skills/lazyown_mcp_opencode.py:181` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp_opencode.py:211` | `def main()` |
| `Objective` | class | `skills/lazyown_objective.py:105` | `class Objective` |
| `ObjectiveStore` | class | `skills/lazyown_objective.py:123` | `class ObjectiveStore` |
| `SoulUpdater` | class | `skills/lazyown_objective.py:359` | `class SoulUpdater` |
| `__init__` | method | `skills/lazyown_objective.py:131` | `def __init__(self, path)` |
| `__init__` | method | `skills/lazyown_objective.py:379` | `def __init__(self)` |
| `_load_all` | method | `skills/lazyown_objective.py:138` | `def _load_all(self)` |
| `_now` | method | `skills/lazyown_objective.py:135` | `def _now(self)` |
| `_patch_line` | method | `skills/lazyown_objective.py:404` | `def _patch_line(self, key, value)` |
| `_patch_section` | method | `skills/lazyown_objective.py:389` | `def _patch_section(self, header, new_body)` |
| `_read` | method | `skills/lazyown_objective.py:384` | `def _read(self)` |
| `_save_all` | method | `skills/lazyown_objective.py:153` | `def _save_all(self, objs)` |
| `_text_hash` | method | `skills/lazyown_objective.py:159` | `def _text_hash(text)` |
| `_update_status` | method | `skills/lazyown_objective.py:229` | `def _update_status(self, obj_id, status, notes)` |
| `block` | method | `skills/lazyown_objective.py:246` | `def block(self, obj_id, reason)` |
| `cleanup` | method | `skills/lazyown_objective.py:163` | `def cleanup(self)` |
| `complete` | method | `skills/lazyown_objective.py:243` | `def complete(self, obj_id, notes)` |
| `current_plan` | function | `skills/lazyown_objective.py:330` | `def current_plan()` |
| `decompose_goal` | function | `skills/lazyown_objective.py:296` | `def decompose_goal(goal_text, target)` |
| `full_context_for_claude` | function | `skills/lazyown_objective.py:336` | `def full_context_for_claude(target)` |
| `inject` | method | `skills/lazyown_objective.py:193` | `def inject(self, text, priority, source, context, notes)` |
| `list_all` | method | `skills/lazyown_objective.py:265` | `def list_all(self, status, limit)` |
| `list_pending` | method | `skills/lazyown_objective.py:261` | `def list_pending(self, limit)` |
| `main` | function | `skills/lazyown_objective.py:485` | `def main()` |
| `next_pending` | method | `skills/lazyown_objective.py:255` | `def next_pending(self)` |
| `read_soul` | function | `skills/lazyown_objective.py:320` | `def read_soul()` |
| `skip` | method | `skills/lazyown_objective.py:249` | `def skip(self, obj_id, reason)` |
| `sort_key` | method | `skills/lazyown_objective.py:116` | `def sort_key(self)` |
| `start` | method | `skills/lazyown_objective.py:252` | `def start(self, obj_id)` |
| `summary` | method | `skills/lazyown_objective.py:271` | `def summary(self)` |
| `update_access` | method | `skills/lazyown_objective.py:459` | `def update_access(self, level, target, method)` |
| `update_credentials` | method | `skills/lazyown_objective.py:432` | `def update_credentials(self, creds)` |
| `update_os` | method | `skills/lazyown_objective.py:425` | `def update_os(self, os_name, target)` |
| `update_phase` | method | `skills/lazyown_objective.py:417` | `def update_phase(self, phase)` |
| `update_target` | method | `skills/lazyown_objective.py:421` | `def update_target(self, target)` |
| `update_vulnerabilities` | method | `skills/lazyown_objective.py:466` | `def update_vulnerabilities(self, vulns)` |
| `write_soul` | function | `skills/lazyown_objective.py:326` | `def write_soul(content)` |
| `ParquetDB` | class | `skills/lazyown_parquet_db.py:244` | `class ParquetDB` |
| `__init__` | method | `skills/lazyown_parquet_db.py:295` | `def __init__(self, lazyown_dir)` |
| `_build_cmd2_category_map` | function | `skills/lazyown_parquet_db.py:146` | `def _build_cmd2_category_map(lazyown_py)` |
| `_classify_row` | function | `skills/lazyown_parquet_db.py:203` | `def _classify_row(command, args, phase_hint)` |
| `_load_session` | method | `skills/lazyown_parquet_db.py:307` | `def _load_session(self)` |
| `_slim` | function | `skills/lazyown_parquet_db.py:932` | `def _slim(row)` |
| `_stable_id` | function | `skills/lazyown_parquet_db.py:178` | `def _stable_id(start, cmd, args, dest_ip)` |
| `annotate` | method | `skills/lazyown_parquet_db.py:405` | `def annotate(self, row_id, success, category, outcome)` |
| `annotate_rich` | method | `skills/lazyown_parquet_db.py:434` | `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` |
| `context_for_phase` | method | `skills/lazyown_parquet_db.py:632` | `def context_for_phase(self, phase, target, limit)` |
| `get_pdb` | function | `skills/lazyown_parquet_db.py:950` | `def get_pdb(lazyown_dir)` |
| `list_parquets` | method | `skills/lazyown_parquet_db.py:745` | `def list_parquets(self)` |
| `main` | function | `skills/lazyown_parquet_db.py:963` | `def main()` |
| `predict_success` | method | `skills/lazyown_parquet_db.py:845` | `def predict_success(self, command, category)` |
| `query_atomic` | method | `skills/lazyown_parquet_db.py:578` | `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `query_knowledge` | method | `skills/lazyown_parquet_db.py:526` | `def query_knowledge(self, keyword, parquet_name, columns, limit)` |
| `query_session` | method | `skills/lazyown_parquet_db.py:490` | `def query_session(self, phase, target, success_only, limit)` |
| `stats` | method | `skills/lazyown_parquet_db.py:731` | `def stats(self)` |
| `sync` | method | `skills/lazyown_parquet_db.py:316` | `def sync(self, csv_path)` |
| `train_classifier` | method | `skills/lazyown_parquet_db.py:750` | `def train_classifier(self, min_rows)` |
| `verify_model_integrity` | function | `skills/lazyown_parquet_db.py:894` | `def verify_model_integrity(model_path, encoder_path, hash_path)` |
| `PermissionMode` | class | `skills/lazyown_permissions.py:18` | `class PermissionMode(Enum)` |
| `PermissionRule` | class | `skills/lazyown_permissions.py:29` | `class PermissionRule` |
| `PermissionSystem` | class | `skills/lazyown_permissions.py:91` | `class PermissionSystem` |
| `__init__` | method | `skills/lazyown_permissions.py:103` | `def __init__(self, sessions_dir)` |
| `_audit` | method | `skills/lazyown_permissions.py:132` | `def _audit(self, tool, decision, reason, args)` |
| `_load` | method | `skills/lazyown_permissions.py:113` | `def _load(self)` |
| `_matches` | method | `skills/lazyown_permissions.py:219` | `def _matches(self, rule, tool_name, args)` |
| `_save` | method | `skills/lazyown_permissions.py:124` | `def _save(self)` |
| `add_rule` | method | `skills/lazyown_permissions.py:145` | `def add_rule(self, tool_pattern, action, condition, description)` |
| `evaluate` | method | `skills/lazyown_permissions.py:167` | `def evaluate(self, tool_name, arguments)` |
| `list_rules` | method | `skills/lazyown_permissions.py:162` | `def list_rules(self)` |
| `metrics` | method | `skills/lazyown_permissions.py:237` | `def metrics(self)` |
| `remove_rule` | method | `skills/lazyown_permissions.py:151` | `def remove_rule(self, tool_pattern, action)` |
| `set_mode` | method | `skills/lazyown_permissions.py:157` | `def set_mode(self, mode)` |
| `status_text` | method | `skills/lazyown_permissions.py:279` | `def status_text(self)` |
| `to_dict` | method | `skills/lazyown_permissions.py:36` | `def to_dict(self)` |
| `ActionCategory` | class | `skills/lazyown_policy.py:131` | `class ActionCategory(StrEnum)` |
| `ApprovalDecision` | class | `skills/lazyown_policy.py:1326` | `class ApprovalDecision(StrEnum)` |
| `ApprovalGate` | class | `skills/lazyown_policy.py:1606` | `class ApprovalGate` |
| `ApprovalOutcome` | class | `skills/lazyown_policy.py:1356` | `class ApprovalOutcome` |
| `ApprovalRequest` | class | `skills/lazyown_policy.py:1335` | `class ApprovalRequest` |
| `BroadcastApprovalSink` | class | `skills/lazyown_policy.py:1455` | `class BroadcastApprovalSink(IApprovalSink)` |
| `CSVSessionReader` | class | `skills/lazyown_policy.py:843` | `class CSVSessionReader` |
| `CascadeClassifier` | class | `skills/lazyown_policy.py:657` | `class CascadeClassifier` |
| `ClassificationResult` | class | `skills/lazyown_policy.py:306` | `class ClassificationResult` |
| `CompositeApprovalSink` | class | `skills/lazyown_policy.py:1556` | `class CompositeApprovalSink(IApprovalSink)` |
| `Config` | class | `skills/lazyown_policy.py:54` | `class Config` |
| `DetectionRiskAssessor` | class | `skills/lazyown_policy.py:701` | `class DetectionRiskAssessor` |
| `EpisodeRecord` | class | `skills/lazyown_policy.py:347` | `class EpisodeRecord` |
| `ExitCodeClassifier` | class | `skills/lazyown_policy.py:389` | `class ExitCodeClassifier(IOutputClassifier)` |
| `FileApprovalSink` | class | `skills/lazyown_policy.py:1392` | `class FileApprovalSink(IApprovalSink)` |
| `HeuristicClassifier` | class | `skills/lazyown_policy.py:434` | `class HeuristicClassifier(IOutputClassifier)` |
| `HistoryBootstrapper` | class | `skills/lazyown_policy.py:1922` | `class HistoryBootstrapper` |
| `IApprovalSink` | class | `skills/lazyown_policy.py:1375` | `class IApprovalSink(ABC)` |
| `IEpisodeStore` | class | `skills/lazyown_policy.py:899` | `class IEpisodeStore(ABC)` |
| `IOutputClassifier` | class | `skills/lazyown_policy.py:372` | `class IOutputClassifier(ABC)` |
| `JSONLEpisodeStore` | class | `skills/lazyown_policy.py:915` | `class JSONLEpisodeStore(IEpisodeStore)` |
| `LazyOwnPolicyIntegration` | class | `skills/lazyown_policy.py:1294` | `class LazyOwnPolicyIntegration` |
| `OllamaLargeClassifier` | class | `skills/lazyown_policy.py:598` | `class OllamaLargeClassifier(_OllamaClassifierBase)` |
| `OllamaSmallClassifier` | class | `skills/lazyown_policy.py:588` | `class OllamaSmallClassifier(_OllamaClassifierBase)` |
| `OutcomeType` | class | `skills/lazyown_policy.py:146` | `class OutcomeType(StrEnum)` |
| `OverrideRule` | class | `skills/lazyown_policy.py:1042` | `class OverrideRule` |
| `PolicyAdvisor` | class | `skills/lazyown_policy.py:1262` | `class PolicyAdvisor` |
| `PolicyEngine` | class | `skills/lazyown_policy.py:1097` | `class PolicyEngine` |
| `RewardCalculator` | class | `skills/lazyown_policy.py:754` | `class RewardCalculator` |
| `ScopeBoundAutoGate` | class | `skills/lazyown_policy.py:1820` | `class ScopeBoundAutoGate` |
| `SessionClassificationPipeline` | class | `skills/lazyown_policy.py:1194` | `class SessionClassificationPipeline` |
| `StdinApprovalSink` | class | `skills/lazyown_policy.py:1503` | `class StdinApprovalSink(IApprovalSink)` |
| `StepRecord` | class | `skills/lazyown_policy.py:330` | `class StepRecord` |
| `TransitionTable` | class | `skills/lazyown_policy.py:979` | `class TransitionTable` |
| `UserInteractiveClassifier` | class | `skills/lazyown_policy.py:608` | `class UserInteractiveClassifier(IOutputClassifier)` |
| `_OllamaClassifierBase` | class | `skills/lazyown_policy.py:487` | `class _OllamaClassifierBase(IOutputClassifier)` |
| `__init__` | method | `skills/lazyown_policy.py:496` | `def __init__(self, cfg, model, tier_name)` |
| `__init__` | method | `skills/lazyown_policy.py:591` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:601` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:666` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:715` | `def __init__(self)` |
| `__init__` | method | `skills/lazyown_policy.py:773` | `def __init__(self, cfg, risk_assessor)` |
| `__init__` | method | `skills/lazyown_policy.py:850` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:923` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:987` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1107` | `def __init__(self, cfg, transitions)` |
| `__init__` | method | `skills/lazyown_policy.py:1202` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:1267` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1302` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1400` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `skills/lazyown_policy.py:1463` | `def __init__(self, narrator, file_sink)` |
| `__init__` | method | `skills/lazyown_policy.py:1513` | `def __init__(self, stream)` |
| `__init__` | method | `skills/lazyown_policy.py:1564` | `def __init__(self, sinks)` |
| `__init__` | method | `skills/lazyown_policy.py:1634` | `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1850` | `def __init__(self, payload_path, in_scope_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1928` | `def __init__(self, cfg)` |
| `_apply_overrides` | method | `skills/lazyown_policy.py:1162` | `def _apply_overrides(self, recent_states)` |
| `_auto_approve_enabled` | method | `skills/lazyown_policy.py:1654` | `def _auto_approve_enabled(self)` |
| `_build_prompt` | method | `skills/lazyown_policy.py:503` | `def _build_prompt(self, command, args, output, exit_code)` |
| `_call_ollama` | method | `skills/lazyown_policy.py:525` | `def _call_ollama(self, prompt)` |
| `_cmd_analyze` | function | `skills/lazyown_policy.py:1977` | `def _cmd_analyze(cfg, args)` |
| `_cmd_bootstrap` | function | `skills/lazyown_policy.py:1970` | `def _cmd_bootstrap(cfg, _args)` |
| `_cmd_recommend` | function | `skills/lazyown_policy.py:1991` | `def _cmd_recommend(cfg, args)` |
| `_cmd_report` | function | `skills/lazyown_policy.py:2012` | `def _cmd_report(cfg, _args)` |
| `_default_fallback` | method | `skills/lazyown_policy.py:1171` | `def _default_fallback(self, current_state)` |
| `_default_in_scope` | function | `skills/lazyown_policy.py:1779` | `def _default_in_scope(target, entries)` |
| `_default_sleep` | function | `skills/lazyown_policy.py:1721` | `def _default_sleep(seconds)` |
| `_get_oracle` | method | `skills/lazyown_policy.py:718` | `def _get_oracle(self)` |
| `_is_gated` | method | `skills/lazyown_policy.py:1664` | `def _is_gated(self, phase)` |
| `_is_interactive` | method | `skills/lazyown_policy.py:1517` | `def _is_interactive(self)` |
| `_load` | method | `skills/lazyown_policy.py:1024` | `def _load(self)` |
| `_load_scope_guard` | function | `skills/lazyown_policy.py:1739` | `def _load_scope_guard()` |
| `_normalize_scope` | function | `skills/lazyown_policy.py:1800` | `def _normalize_scope(entries)` |
| `_parse_response` | method | `skills/lazyown_policy.py:540` | `def _parse_response(self, data, fallback)` |
| `_read_payload` | method | `skills/lazyown_policy.py:1859` | `def _read_payload(self)` |
| `_save` | method | `skills/lazyown_policy.py:1032` | `def _save(self)` |
| `_setup_logging` | function | `skills/lazyown_policy.py:1960` | `def _setup_logging(cfg)` |
| `_write_all` | method | `skills/lazyown_policy.py:970` | `def _write_all(self, episodes)` |
| `advise` | method | `skills/lazyown_policy.py:1272` | `def advise(self, target)` |
| `announce` | method | `skills/lazyown_policy.py:1384` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1409` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1471` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1523` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1569` | `def announce(self, request)` |
| `append_step` | method | `skills/lazyown_policy.py:903` | `def append_step(self, step)` |
| `append_step` | method | `skills/lazyown_policy.py:927` | `def append_step(self, step)` |
| `assess_probability` | method | `skills/lazyown_policy.py:733` | `def assess_probability(self, command, args, category)` |
| `calculate` | method | `skills/lazyown_policy.py:783` | `def calculate(self, category, outcome)` |
| `calculate_with_detection` | method | `skills/lazyown_policy.py:798` | `def calculate_with_detection(self, category, outcome, command, args)` |
| `classify` | method | `skills/lazyown_policy.py:376` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:401` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:444` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:570` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:616` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:677` | `def classify(self, command, args, output, exit_code)` |
| `default` | method | `skills/lazyown_policy.py:82` | `def default(cls)` |
| `episode_summary` | method | `skills/lazyown_policy.py:1277` | `def episode_summary(self, target)` |
| `from_dict` | method | `skills/lazyown_policy.py:362` | `def from_dict(cls, d)` |
| `get_episode` | method | `skills/lazyown_policy.py:911` | `def get_episode(self, target)` |
| `get_episode` | method | `skills/lazyown_policy.py:963` | `def get_episode(self, target)` |
| `get_recommendations` | method | `skills/lazyown_policy.py:1318` | `def get_recommendations(self, target)` |
| `infer_category` | function | `skills/lazyown_policy.py:267` | `def infer_category(command, args)` |
| `is_approved` | method | `skills/lazyown_policy.py:1365` | `def is_approved(self)` |
| `is_denied` | method | `skills/lazyown_policy.py:1370` | `def is_denied(self)` |
| `is_high_risk` | method | `skills/lazyown_policy.py:746` | `def is_high_risk(self, command, args, category)` |
| `load_all` | method | `skills/lazyown_policy.py:907` | `def load_all(self)` |
| `load_all` | method | `skills/lazyown_policy.py:947` | `def load_all(self)` |
| `main` | function | `skills/lazyown_policy.py:2036` | `def main()` |
| `ollama_url` | method | `skills/lazyown_policy.py:123` | `def ollama_url(self)` |
| `on_command_complete` | method | `skills/lazyown_policy.py:1307` | `def on_command_complete(self, target, command, args, output, exit_code)` |
| `path` | method | `skills/lazyown_policy.py:1405` | `def path(self)` |
| `process` | method | `skills/lazyown_policy.py:1210` | `def process(self, target, command, args, output, exit_code, timestamp)` |
| `query` | method | `skills/lazyown_policy.py:1003` | `def query(self, from_state)` |
| `read` | method | `skills/lazyown_policy.py:855` | `def read(self)` |
| `recommend` | method | `skills/lazyown_policy.py:1111` | `def recommend(self, recent_steps)` |
| `record` | method | `skills/lazyown_policy.py:993` | `def record(self, from_state, to_category, outcome)` |
| `request` | method | `skills/lazyown_policy.py:1667` | `def request(self, target, phase, command, reason)` |
| `request` | method | `skills/lazyown_policy.py:1866` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1388` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1426` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1499` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1552` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1576` | `def resolution_for(self, approval_id)` |
| `run` | method | `skills/lazyown_policy.py:1934` | `def run(self)` |
| `to_dict` | method | `skills/lazyown_policy.py:357` | `def to_dict(self)` |
| `unknown` | method | `skills/lazyown_policy.py:317` | `def unknown(cls, tier)` |
| `SessionTranscript` | class | `skills/lazyown_session.py:71` | `class SessionTranscript` |
| `__init__` | method | `skills/lazyown_session.py:82` | `def __init__(self, sessions_dir, session_id)` |
| `_init_meta` | method | `skills/lazyown_session.py:90` | `def _init_meta(self)` |
| `_redact_sensitive` | function | `skills/lazyown_session.py:47` | `def _redact_sensitive(value)` |
| `add_compact_boundary` | method | `skills/lazyown_session.py:209` | `def add_compact_boundary(self, summary, preserved_uuids)` |
| `append` | method | `skills/lazyown_session.py:106` | `def append(self, event_type, data)` |
| `count` | method | `skills/lazyown_session.py:164` | `def count(self)` |
| `fork` | method | `skills/lazyown_session.py:227` | `def fork(self, new_id)` |
| `get_all` | method | `skills/lazyown_session.py:161` | `def get_all(self)` |
| `get_recent` | method | `skills/lazyown_session.py:143` | `def get_recent(self, n)` |
| `get_transcript` | function | `skills/lazyown_session.py:281` | `def get_transcript(sessions_dir, session_id)` |
| `maybe_auto_compact` | method | `skills/lazyown_session.py:174` | `def maybe_auto_compact(self, threshold)` |
| `reset_transcript` | function | `skills/lazyown_session.py:294` | `def reset_transcript(sessions_dir, session_id)` |
| `status_text` | method | `skills/lazyown_session.py:257` | `def status_text(self)` |
| `_gen_EOF` | function | `skills/mcp_generated_tools.py:696` | `def _gen_EOF(arguments, tool_name, _cmd)` |
| `_gen_GET` | function | `skills/mcp_generated_tools.py:704` | `def _gen_GET(arguments, tool_name, _cmd)` |
| `_gen_OPTIONS` | function | `skills/mcp_generated_tools.py:712` | `def _gen_OPTIONS(arguments, tool_name, _cmd)` |
| `_gen_POST` | function | `skills/mcp_generated_tools.py:720` | `def _gen_POST(arguments, tool_name, _cmd)` |
| `_gen_acknowledgearp` | function | `skills/mcp_generated_tools.py:728` | `def _gen_acknowledgearp(arguments, tool_name, _cmd)` |
| `_gen_acknowledgeicmp` | function | `skills/mcp_generated_tools.py:736` | `def _gen_acknowledgeicmp(arguments, tool_name, _cmd)` |
| `_gen_aclpwn_py` | function | `skills/mcp_generated_tools.py:744` | `def _gen_aclpwn_py(arguments, tool_name, _cmd)` |
| `_gen_ad_ldap_enum` | function | `skills/mcp_generated_tools.py:752` | `def _gen_ad_ldap_enum(arguments, tool_name, _cmd)` |
| `_gen_adcs_check` | function | `skills/mcp_generated_tools.py:760` | `def _gen_adcs_check(arguments, tool_name, _cmd)` |
| `_gen_add2find` | function | `skills/mcp_generated_tools.py:768` | `def _gen_add2find(arguments, tool_name, _cmd)` |
| `_gen_addalias` | function | `skills/mcp_generated_tools.py:776` | `def _gen_addalias(arguments, tool_name, _cmd)` |
| `_gen_addcli` | function | `skills/mcp_generated_tools.py:784` | `def _gen_addcli(arguments, tool_name, _cmd)` |
| `_gen_addhosts` | function | `skills/mcp_generated_tools.py:792` | `def _gen_addhosts(arguments, tool_name, _cmd)` |
| `_gen_addspn_py` | function | `skills/mcp_generated_tools.py:800` | `def _gen_addspn_py(arguments, tool_name, _cmd)` |
| `_gen_addusers` | function | `skills/mcp_generated_tools.py:808` | `def _gen_addusers(arguments, tool_name, _cmd)` |
| `_gen_adgetpass` | function | `skills/mcp_generated_tools.py:816` | `def _gen_adgetpass(arguments, tool_name, _cmd)` |
| `_gen_adsso_spray` | function | `skills/mcp_generated_tools.py:824` | `def _gen_adsso_spray(arguments, tool_name, _cmd)` |
| `_gen_adversary` | function | `skills/mcp_generated_tools.py:832` | `def _gen_adversary(arguments, tool_name, _cmd)` |
| `_gen_adversary_yaml` | function | `skills/mcp_generated_tools.py:840` | `def _gen_adversary_yaml(arguments, tool_name, _cmd)` |
| `_gen_aes_pe` | function | `skills/mcp_generated_tools.py:848` | `def _gen_aes_pe(arguments, tool_name, _cmd)` |
| `_gen_ai_playbook` | function | `skills/mcp_generated_tools.py:856` | `def _gen_ai_playbook(arguments, tool_name, _cmd)` |
| `_gen_ai_toggle` | function | `skills/mcp_generated_tools.py:864` | `def _gen_ai_toggle(arguments, tool_name, _cmd)` |
| `_gen_aliass` | function | `skills/mcp_generated_tools.py:872` | `def _gen_aliass(arguments, tool_name, _cmd)` |
| `_gen_allin` | function | `skills/mcp_generated_tools.py:880` | `def _gen_allin(arguments, tool_name, _cmd)` |
| `_gen_alterx` | function | `skills/mcp_generated_tools.py:888` | `def _gen_alterx(arguments, tool_name, _cmd)` |
| `_gen_amass` | function | `skills/mcp_generated_tools.py:896` | `def _gen_amass(arguments, tool_name, _cmd)` |
| `_gen_android_apk` | function | `skills/mcp_generated_tools.py:904` | `def _gen_android_apk(arguments, tool_name, _cmd)` |
| `_gen_android_enum` | function | `skills/mcp_generated_tools.py:912` | `def _gen_android_enum(arguments, tool_name, _cmd)` |
| `_gen_apache_users` | function | `skills/mcp_generated_tools.py:920` | `def _gen_apache_users(arguments, tool_name, _cmd)` |
| `_gen_applocker_csc` | function | `skills/mcp_generated_tools.py:928` | `def _gen_applocker_csc(arguments, tool_name, _cmd)` |
| `_gen_applocker_installutil` | function | `skills/mcp_generated_tools.py:936` | `def _gen_applocker_installutil(arguments, tool_name, _cmd)` |
| `_gen_applocker_msbuild` | function | `skills/mcp_generated_tools.py:944` | `def _gen_applocker_msbuild(arguments, tool_name, _cmd)` |
| `_gen_applocker_mshta` | function | `skills/mcp_generated_tools.py:952` | `def _gen_applocker_mshta(arguments, tool_name, _cmd)` |
| `_gen_applocker_presentation` | function | `skills/mcp_generated_tools.py:960` | `def _gen_applocker_presentation(arguments, tool_name, _cmd)` |
| `_gen_applocker_regsvcs` | function | `skills/mcp_generated_tools.py:968` | `def _gen_applocker_regsvcs(arguments, tool_name, _cmd)` |
| `_gen_applocker_rundll32` | function | `skills/mcp_generated_tools.py:976` | `def _gen_applocker_rundll32(arguments, tool_name, _cmd)` |
| `_gen_apropos` | function | `skills/mcp_generated_tools.py:984` | `def _gen_apropos(arguments, tool_name, _cmd)` |
| `_gen_apt_playbook` | function | `skills/mcp_generated_tools.py:992` | `def _gen_apt_playbook(arguments, tool_name, _cmd)` |
| `_gen_apt_proxy` | function | `skills/mcp_generated_tools.py:1000` | `def _gen_apt_proxy(arguments, tool_name, _cmd)` |
| `_gen_apt_repo` | function | `skills/mcp_generated_tools.py:1008` | `def _gen_apt_repo(arguments, tool_name, _cmd)` |
| `_gen_arjun` | function | `skills/mcp_generated_tools.py:1016` | `def _gen_arjun(arguments, tool_name, _cmd)` |
| `_gen_arpscan` | function | `skills/mcp_generated_tools.py:1024` | `def _gen_arpscan(arguments, tool_name, _cmd)` |
| `_gen_ask` | function | `skills/mcp_generated_tools.py:1032` | `def _gen_ask(arguments, tool_name, _cmd)` |
| `_gen_asprevbase64` | function | `skills/mcp_generated_tools.py:1040` | `def _gen_asprevbase64(arguments, tool_name, _cmd)` |
| `_gen_assign` | function | `skills/mcp_generated_tools.py:1048` | `def _gen_assign(arguments, tool_name, _cmd)` |
| `_gen_atomic_agent` | function | `skills/mcp_generated_tools.py:1056` | `def _gen_atomic_agent(arguments, tool_name, _cmd)` |
| `_gen_atomic_gen` | function | `skills/mcp_generated_tools.py:1064` | `def _gen_atomic_gen(arguments, tool_name, _cmd)` |
| `_gen_atomic_lazyown` | function | `skills/mcp_generated_tools.py:1072` | `def _gen_atomic_lazyown(arguments, tool_name, _cmd)` |
| `_gen_atomic_tests` | function | `skills/mcp_generated_tools.py:1080` | `def _gen_atomic_tests(arguments, tool_name, _cmd)` |
| `_gen_attack_plan` | function | `skills/mcp_generated_tools.py:1088` | `def _gen_attack_plan(arguments, tool_name, _cmd)` |
| `_gen_attack_surface` | function | `skills/mcp_generated_tools.py:1096` | `def _gen_attack_surface(arguments, tool_name, _cmd)` |
| `_gen_audit_complete_keys` | function | `skills/mcp_generated_tools.py:1104` | `def _gen_audit_complete_keys(arguments, tool_name, _cmd)` |
| `_gen_autoblody` | function | `skills/mcp_generated_tools.py:1112` | `def _gen_autoblody(arguments, tool_name, _cmd)` |
| `_gen_automsf` | function | `skills/mcp_generated_tools.py:1120` | `def _gen_automsf(arguments, tool_name, _cmd)` |
| `_gen_autopivot` | function | `skills/mcp_generated_tools.py:1128` | `def _gen_autopivot(arguments, tool_name, _cmd)` |
| `_gen_back` | function | `skills/mcp_generated_tools.py:1136` | `def _gen_back(arguments, tool_name, _cmd)` |
| `_gen_backdoor_factory` | function | `skills/mcp_generated_tools.py:1144` | `def _gen_backdoor_factory(arguments, tool_name, _cmd)` |
| `_gen_banner` | function | `skills/mcp_generated_tools.py:1152` | `def _gen_banner(arguments, tool_name, _cmd)` |
| `_gen_banners` | function | `skills/mcp_generated_tools.py:1160` | `def _gen_banners(arguments, tool_name, _cmd)` |
| `_gen_base64decode` | function | `skills/mcp_generated_tools.py:1168` | `def _gen_base64decode(arguments, tool_name, _cmd)` |
| `_gen_base64encode` | function | `skills/mcp_generated_tools.py:1176` | `def _gen_base64encode(arguments, tool_name, _cmd)` |
| `_gen_batchnmap` | function | `skills/mcp_generated_tools.py:1184` | `def _gen_batchnmap(arguments, tool_name, _cmd)` |
| `_gen_bbot` | function | `skills/mcp_generated_tools.py:1192` | `def _gen_bbot(arguments, tool_name, _cmd)` |
| `_gen_beaconcfg` | function | `skills/mcp_generated_tools.py:1200` | `def _gen_beaconcfg(arguments, tool_name, _cmd)` |
| `_gen_bin2shellcode` | function | `skills/mcp_generated_tools.py:1208` | `def _gen_bin2shellcode(arguments, tool_name, _cmd)` |
| `_gen_binarycheck` | function | `skills/mcp_generated_tools.py:1216` | `def _gen_binarycheck(arguments, tool_name, _cmd)` |
| `_gen_bitm` | function | `skills/mcp_generated_tools.py:1224` | `def _gen_bitm(arguments, tool_name, _cmd)` |
| `_gen_blazy` | function | `skills/mcp_generated_tools.py:1232` | `def _gen_blazy(arguments, tool_name, _cmd)` |
| `_gen_bloodhound` | function | `skills/mcp_generated_tools.py:1240` | `def _gen_bloodhound(arguments, tool_name, _cmd)` |
| `_gen_bloodyAD` | function | `skills/mcp_generated_tools.py:1248` | `def _gen_bloodyAD(arguments, tool_name, _cmd)` |
| `_gen_breacher` | function | `skills/mcp_generated_tools.py:1256` | `def _gen_breacher(arguments, tool_name, _cmd)` |
| `_gen_browse` | function | `skills/mcp_generated_tools.py:1264` | `def _gen_browse(arguments, tool_name, _cmd)` |
| `_gen_c2` | function | `skills/mcp_generated_tools.py:1272` | `def _gen_c2(arguments, tool_name, _cmd)` |
| `_gen_c2_beacon_cmd` | function | `skills/mcp_generated_tools.py:1280` | `def _gen_c2_beacon_cmd(arguments, tool_name, _cmd)` |
| `_gen_c2_beacons` | function | `skills/mcp_generated_tools.py:1288` | `def _gen_c2_beacons(arguments, tool_name, _cmd)` |
| `_gen_c2_implant` | function | `skills/mcp_generated_tools.py:1296` | `def _gen_c2_implant(arguments, tool_name, _cmd)` |
| `_gen_c2_keygen` | function | `skills/mcp_generated_tools.py:1304` | `def _gen_c2_keygen(arguments, tool_name, _cmd)` |
| `_gen_c2_quickstart` | function | `skills/mcp_generated_tools.py:1312` | `def _gen_c2_quickstart(arguments, tool_name, _cmd)` |
| `_gen_c2asm` | function | `skills/mcp_generated_tools.py:1320` | `def _gen_c2asm(arguments, tool_name, _cmd)` |
| `_gen_cacti_exploit` | function | `skills/mcp_generated_tools.py:1328` | `def _gen_cacti_exploit(arguments, tool_name, _cmd)` |
| `_gen_caldera` | function | `skills/mcp_generated_tools.py:1336` | `def _gen_caldera(arguments, tool_name, _cmd)` |
| `_gen_caldera_export` | function | `skills/mcp_generated_tools.py:1344` | `def _gen_caldera_export(arguments, tool_name, _cmd)` |
| `_gen_caldera_import` | function | `skills/mcp_generated_tools.py:1352` | `def _gen_caldera_import(arguments, tool_name, _cmd)` |
| `_gen_camphish` | function | `skills/mcp_generated_tools.py:1360` | `def _gen_camphish(arguments, tool_name, _cmd)` |
| `_gen_certipy` | function | `skills/mcp_generated_tools.py:1368` | `def _gen_certipy(arguments, tool_name, _cmd)` |
| `_gen_certipy_ad` | function | `skills/mcp_generated_tools.py:1376` | `def _gen_certipy_ad(arguments, tool_name, _cmd)` |
| `_gen_cewl` | function | `skills/mcp_generated_tools.py:1384` | `def _gen_cewl(arguments, tool_name, _cmd)` |
| `_gen_chain` | function | `skills/mcp_generated_tools.py:1392` | `def _gen_chain(arguments, tool_name, _cmd)` |
| `_gen_changeme` | function | `skills/mcp_generated_tools.py:1400` | `def _gen_changeme(arguments, tool_name, _cmd)` |
| `_gen_check_update` | function | `skills/mcp_generated_tools.py:1408` | `def _gen_check_update(arguments, tool_name, _cmd)` |
| `_gen_chisel` | function | `skills/mcp_generated_tools.py:1416` | `def _gen_chisel(arguments, tool_name, _cmd)` |
| `_gen_cicd_scan` | function | `skills/mcp_generated_tools.py:1424` | `def _gen_cicd_scan(arguments, tool_name, _cmd)` |
| `_gen_cicd_secrets` | function | `skills/mcp_generated_tools.py:1432` | `def _gen_cicd_secrets(arguments, tool_name, _cmd)` |
| `_gen_clean` | function | `skills/mcp_generated_tools.py:1440` | `def _gen_clean(arguments, tool_name, _cmd)` |
| `_gen_clean_ad` | function | `skills/mcp_generated_tools.py:1448` | `def _gen_clean_ad(arguments, tool_name, _cmd)` |
| `_gen_clock` | function | `skills/mcp_generated_tools.py:1456` | `def _gen_clock(arguments, tool_name, _cmd)` |
| `_gen_clone_site` | function | `skills/mcp_generated_tools.py:1464` | `def _gen_clone_site(arguments, tool_name, _cmd)` |
| `_gen_cloud_buckets` | function | `skills/mcp_generated_tools.py:1472` | `def _gen_cloud_buckets(arguments, tool_name, _cmd)` |

Next: [SYMBOLS_p27.md](SYMBOLS_p27.md)
