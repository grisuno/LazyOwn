# Symbols (page 15 of 43)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `lazy_activity` | function | `modules/lazy_bridge.py:123` | `def lazy_activity(task_id)` |
| `lazy_assets` | function | `modules/lazy_bridge.py:99` | `def lazy_assets()` |
| `lazy_graph` | function | `modules/lazy_bridge.py:110` | `def lazy_graph(task_id)` |
| `lazy_guard_audit` | function | `modules/lazy_bridge.py:147` | `def lazy_guard_audit(task_id)` |
| `lazy_tasks` | function | `modules/lazy_bridge.py:88` | `def lazy_tasks()` |
| `lazy_traffic` | function | `modules/lazy_bridge.py:135` | `def lazy_traffic(task_id)` |
| `pull_findings_to_lifecycle` | function | `modules/lazy_bridge.py:286` | `def pull_findings_to_lifecycle()` |
| `pull_to_objectives` | function | `modules/lazy_bridge.py:251` | `def pull_to_objectives()` |
| `pull_to_world_model` | function | `modules/lazy_bridge.py:206` | `def pull_to_world_model()` |
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:361` | `def pull_traffic_to_recorder(progress)` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:429` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:454` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:519` | `def sync_all(progress)` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:219` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:242` | `def set_full_cli(enabled)` |
| `LazyEngine` | class | `modules/lazy_engine.py:55` | `class LazyEngine(LazyLoopEngine)` |
| `install_command_for` | function | `modules/lazy_installer.py:70` | `def install_command_for(tool)` |
| `installer_enabled` | function | `modules/lazy_installer.py:41` | `def installer_enabled()` |
| `intent_for` | function | `modules/lazy_installer.py:75` | `def intent_for(tool)` |
| `set_installer_enabled` | function | `modules/lazy_installer.py:58` | `def set_installer_enabled(enabled)` |
| `steps_for_install` | function | `modules/lazy_installer.py:88` | `def steps_for_install(text)` |
| `tool_from_intent` | function | `modules/lazy_installer.py:80` | `def tool_from_intent(text)` |
| `_append` | function | `modules/lazy_intel.py:70` | `def _append(record)` |
| `_is_ip_literal` | function | `modules/lazy_intel.py:274` | `def _is_ip_literal(value)` |
| `_log_path` | function | `modules/lazy_intel.py:35` | `def _log_path()` |
| `_mask` | function | `modules/lazy_intel.py:41` | `def _mask(text)` |
| `_now` | function | `modules/lazy_intel.py:30` | `def _now()` |
| `describe_command` | function | `modules/lazy_intel.py:105` | `def describe_command(command)` |
| `export_spans` | function | `modules/lazy_intel.py:324` | `def export_spans(task_id, out)` |
| `fuse_routing_decisions` | function | `modules/lazy_intel.py:285` | `def fuse_routing_decisions(task_id)` |
| `infer_source` | function | `modules/lazy_intel.py:79` | `def infer_source(command, intent_text)` |
| `mask_configured` | function | `modules/lazy_intel.py:228` | `def mask_configured(text)` |
| `read_decisions` | function | `modules/lazy_intel.py:202` | `def read_decisions(task_id, limit)` |
| `record_routing_decision` | function | `modules/lazy_intel.py:120` | `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | function | `modules/lazy_intel.py:160` | `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` |
| `stack_signature` | function | `modules/lazy_intel.py:254` | `def stack_signature(assets)` |
| `ActivityLog` | class | `modules/lazy_loop.py:1424` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2156` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:953` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:928` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2250` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:5324` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7279` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:6323` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:919` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1116` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:905` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6045` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1396` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1815` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2402` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:7603` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:942` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:6741` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:6426` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3035` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5225` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2334` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7205` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7309` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:7471` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:7498` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2604` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:7428` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2562` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:7161` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1557` | `class TrafficLog` |
| `TriggerStore` | class | `modules/lazy_loop.py:6592` | `class TriggerStore` |
| `Worker` | class | `modules/lazy_loop.py:3484` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:956` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1119` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1399` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1427` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1560` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1818` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2165` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2253` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2337` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2431` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2565` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2607` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3038` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3487` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5228` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:5332` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6048` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:6326` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6429` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:6595` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6758` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7164` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7282` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7431` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7474` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7628` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:3894` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4127` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:4153` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:4498` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:4316` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:4530` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:5467` | `def _apply_stored_bodies(self, bodies)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2100` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:4639` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:4962` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:8721` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:8757` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:5535` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:5349` | `def _bodies_path(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:9834` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3227` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:492` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:9154` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:4289` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:5337` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:4953` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3049` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:5527` | `def _content_versions(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:546` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3386` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4852` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3058` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:4628` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:6151` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:6147` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:4142` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:8672` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2426` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:588` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:508` | `def _encrypt_channel_secret(plaintext)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:8812` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2409` | `def _event_for(cls, path, item_id)` |
| `_find` | function | `modules/lazy_loop.py:5556` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:9730` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:3819` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:5495` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:9161` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:5544` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:3945` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_host_from_token` | function | `modules/lazy_loop.py:350` | `def _host_from_token(token)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:8183` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:243` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:5491` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5216` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:429` | `def _kill()` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3400` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:796` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:804` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:4728` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2437` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6331` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6600` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7168` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7286` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7435` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:5353` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:5341` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2172` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:756` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2176` | `def _load_task(self)` |
| `_mask_key` | function | `modules/lazy_loop.py:469` | `def _mask_key(match)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6021` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2121` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:9434` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:9408` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:9454` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:4651` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:5410` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:696` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1752` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:738` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:4218` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3218` | `def _origin_fact(self)` |
| `_parts` | method | `modules/lazy_loop.py:7750` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:970` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1141` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1837` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2572` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2612` | `def _persist(self)` |
| `_prior_steps` | method | `modules/lazy_loop.py:3596` | `def _prior_steps(self, intent)` |
| `_reader` | function | `modules/lazy_loop.py:4240` | `def _reader()` |
| `_record` | method | `modules/lazy_loop.py:6834` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:6909` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:7129` | `def _record_raw(self, member, prompt, reply, ok)` |
| `_refresh` | method | `modules/lazy_loop.py:2700` | `def _refresh(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:407` | `def _register_loop_executor(executor)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:6869` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:6206` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:5361` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:4876` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:484` | `def _restrict_file(path)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:6840` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:4667` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:8527` | `def _run_one(index_node)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:4940` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2441` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:5357` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:5345` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2183` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:766` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2187` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:3567` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:2033` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2023` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:6769` | `def _seed_defaults(self)` |
| `_send_email` | method | `modules/lazy_loop.py:6501` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:4253` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:4816` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3159` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:781` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:8198` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:8991` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3458` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:4186` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:5014` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:743` | `def _store_path(name)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:4890` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:237` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:9272` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:8375` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2083` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:3884` | `def _target_for(self, intent)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:4917` | `def _task_executed_commands(self)` |
| `_traffic_template` | function | `modules/lazy_loop.py:786` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:5562` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:413` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:257` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:578` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:4717` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:4198` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:6185` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:5382` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:8777` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:6222` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5074` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2374` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2669` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2192` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2576` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:6335` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:6604` | `def add(self, kind, arg, every_sec)` |
| `add` | method | `modules/lazy_loop.py:7290` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:7443` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:6441` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2803` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1196` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:7968` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:7986` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:6798` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1153` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:1844` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2822` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:9281` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2738` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1209` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1224` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1220` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:6240` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:7663` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1799` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:419` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2599` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:7215` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:1938` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2359` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1721` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:7186` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:7696` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:7181` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:9759` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:7935` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:5950` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1716` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:6433` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:1886` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2321` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1237` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1409` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1805` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:7573` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:2858` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:3556` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:5812` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:5661` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1298` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2583` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:6922` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:5893` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:7098` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1029` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1063` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:5608` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2616` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:7755` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2519` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:2975` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:974` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2660` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:8040` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:8074` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:9167` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2689` | `def dequeue_next(self)` |
| `digest_overview` | method | `modules/lazy_loop.py:5846` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:9300` | `def drain_queue(self, max_tasks)` |
| `due` | method | `modules/lazy_loop.py:6650` | `def due(self, task_id, graph, activity, assets, store)` |
| `edit_goal` | method | `modules/lazy_loop.py:8028` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1432` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:6539` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2678` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3012` | `def enrich_asset(value)` |
| `ensure_service_trigger` | method | `modules/lazy_loop.py:6637` | `def ensure_service_trigger(self)` |
| `ensure_target` | method | `modules/lazy_loop.py:7700` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2235` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1769` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:3620` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:5788` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2797` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1792` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:6418` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:9503` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:9562` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:9474` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:2909` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:2877` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3370` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6031` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1326` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:6377` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1471` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:6361` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1008` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1181` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1640` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2627` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:7463` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:7486` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:8315` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:9952` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:9697` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:4386` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1332` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:7087` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2341` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2467` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:7261` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:5501` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:9328` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:978` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:4417` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:4409` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:863` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:2842` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:2871` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2257` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1012` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1228` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2231` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2631` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:6633` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7299` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7333` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7439` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7490` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1358` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:7834` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2732` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:2937` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:7548` | `def log(self, task_id, limit, session)` |
| `lookup` | method | `modules/lazy_loop.py:1966` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:402` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:9883` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1019` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:7303` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:6793` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2592` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:5442` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1342` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2390` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:5620` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:7727` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1251` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1244` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:835` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2647` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:8219` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:7862` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1404` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2463` | `def pending(self)` |
| `plan` | method | `modules/lazy_loop.py:3066` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:151` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:8051` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:9121` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:9251` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:9201` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:9245` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:9237` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2673` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:6316` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:7115` | `def raw_entries(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1457` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1587` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:6381` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:3532` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1565` | `def record(self, kind, command, output, meta)` |
| `record_fact` | method | `modules/lazy_loop.py:1374` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | function | `modules/lazy_loop.py:4353` | `def record_fact(text)` |
| `record_fact` | method | `modules/lazy_loop.py:8325` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:7103` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2303` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2291` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:8332` | `def record_verdict(self, task_id, finding_id, verdict, note)` |
| `recorder_blob` | method | `modules/lazy_loop.py:1676` | `def recorder_blob(self, digest, part, offset, length)` |
| `recorder_body` | method | `modules/lazy_loop.py:1647` | `def recorder_body(self, digest)` |
| `refine` | method | `modules/lazy_loop.py:3145` | `def refine(self)` |
| `register_worker` | function | `modules/lazy_loop.py:598` | `def register_worker(worker)` |
| `reload` | method | `modules/lazy_loop.py:1274` | `def reload(self)` |
| `remove` | method | `modules/lazy_loop.py:2213` | `def remove(self, rule_id, action)` |
| `remove` | method | `modules/lazy_loop.py:6623` | `def remove(self, trigger_id)` |
| `remove` | method | `modules/lazy_loop.py:7453` | `def remove(self, name)` |
| `remove_channel` | method | `modules/lazy_loop.py:6488` | `def remove_channel(self, index)` |
| `remove_member` | method | `modules/lazy_loop.py:6807` | `def remove_member(self, name)` |
| `remove_rule` | method | `modules/lazy_loop.py:1855` | `def remove_rule(self, pattern)` |
| `reorder_evidence` | method | `modules/lazy_loop.py:1778` | `def reorder_evidence(self, finding_id, digests, graph)` |
| `repair_worker_command` | function | `modules/lazy_loop.py:272` | `def repair_worker_command(command, target)` |
| `report` | method | `modules/lazy_loop.py:6055` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `report_finding` | function | `modules/lazy_loop.py:4362` | `def report_finding(name, evidence, severity)` |
| `request` | method | `modules/lazy_loop.py:2445` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:2952` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:7355` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2651` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:8244` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:7873` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:5234` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:5310` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:8900` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_command` | function | `modules/lazy_loop.py:4327` | `def run_command(command, background)` |
| `run_round` | method | `modules/lazy_loop.py:8421` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:7312` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:7505` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:1045` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:460` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1543` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1601` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1513` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1612` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:9382` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:8267` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:7269` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:7564` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:7479` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:9260` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:7146` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2787` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:8011` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:1864` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2268` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2704` | `def set_llm_chain(self, task_id, members, active)` |
| `set_priority` | method | `modules/lazy_loop.py:6817` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:7108` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2762` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1185` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2635` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:6277` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:5927` | `def settlement_prompt(agent, reason)` |
| `shell_open` | function | `modules/lazy_loop.py:4401` | `def shell_open()` |
| `shell_send` | function | `modules/lazy_loop.py:4405` | `def shell_send(command)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:610` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:3390` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:4861` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:7784` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:8472` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:2008` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:7422` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:9677` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:2833` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:2853` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:5523` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:7889` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:7883` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:825` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:7917` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:7908` | `def task_traces(self, task_id, query, limit)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
