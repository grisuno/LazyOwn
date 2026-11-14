# Symbols (page 20 of 52)
Previous: [SYMBOLS_p19.md](SYMBOLS_p19.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `sysmon_disable_commands` | method | `modules/log_tamper.py:341` | `def sysmon_disable_commands(self)` |
| `windows_clear_commands` | method | `modules/log_tamper.py:108` | `def windows_clear_commands(self)` |
| `ColoredFormatter` | class | `modules/logging_config.py:36` | `class ColoredFormatter(Formatter)` |
| `CorrelationFilter` | class | `modules/logging_config.py:91` | `class CorrelationFilter(Filter)` |
| `JsonFormatter` | class | `modules/logging_config.py:53` | `class JsonFormatter(Formatter)` |
| `ResilientRotatingFileHandler` | class | `modules/logging_config.py:103` | `class ResilientRotatingFileHandler(RotatingFileHandler)` |
| `_ensure_log_dir_writable` | function | `modules/logging_config.py:156` | `def _ensure_log_dir_writable(log_dir)` |
| `_use_json_format` | function | `modules/logging_config.py:235` | `def _use_json_format()` |
| `clear_correlation_id` | function | `modules/logging_config.py:144` | `def clear_correlation_id()` |
| `configure` | function | `modules/logging_config.py:244` | `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` |
| `emit` | method | `modules/logging_config.py:116` | `def emit(self, record)` |
| `filter` | method | `modules/logging_config.py:94` | `def filter(self, record)` |
| `format` | method | `modules/logging_config.py:39` | `def format(self, record)` |
| `format` | method | `modules/logging_config.py:72` | `def format(self, record)` |
| `get_correlation_id` | function | `modules/logging_config.py:139` | `def get_correlation_id()` |
| `get_logger` | function | `modules/logging_config.py:328` | `def get_logger(name, level)` |
| `handleError` | method | `modules/logging_config.py:122` | `def handleError(self, record)` |
| `reset` | function | `modules/logging_config.py:388` | `def reset()` |
| `set_correlation_id` | function | `modules/logging_config.py:134` | `def set_correlation_id(cid)` |
| `set_level` | function | `modules/logging_config.py:357` | `def set_level(name, level)` |
| `set_quiet` | function | `modules/logging_config.py:367` | `def set_quiet()` |
| `set_verbose` | function | `modules/logging_config.py:373` | `def set_verbose()` |
| `silence_module` | function | `modules/logging_config.py:379` | `def silence_module(name)` |
| `DecisionRecord` | class | `modules/loop/decision_log.py:143` | `class DecisionRecord` |
| `_canonical` | function | `modules/loop/decision_log.py:68` | `def _canonical(value)` |
| `_rotate` | function | `modules/loop/decision_log.py:182` | `def _rotate(path)` |
| `config_digest` | function | `modules/loop/decision_log.py:115` | `def config_digest(config)` |
| `context_digest` | function | `modules/loop/decision_log.py:90` | `def context_digest(ctx)` |
| `digest` | function | `modules/loop/decision_log.py:51` | `def digest(text)` |
| `filtered_rows` | function | `modules/loop/decision_log.py:248` | `def filtered_rows(items)` |
| `new_run_id` | function | `modules/loop/decision_log.py:137` | `def new_run_id()` |
| `read_records` | function | `modules/loop/decision_log.py:221` | `def read_records(path)` |
| `record` | function | `modules/loop/decision_log.py:192` | `def record(rec, path)` |
| `EngineProxyMixin` | class | `modules/loop/engine_proxy.py:4` | `class EngineProxyMixin` |
| `_maybe_proxy_gc` | method | `modules/loop/engine_proxy.py:157` | `def _maybe_proxy_gc(self)` |
| `ingest_proxy_traffic` | method | `modules/loop/engine_proxy.py:75` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `proxy_env` | method | `modules/loop/engine_proxy.py:66` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/loop/engine_proxy.py:16` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/loop/engine_proxy.py:60` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/loop/engine_proxy.py:52` | `def proxy_stop(self)` |
| `search_proxy_body` | method | `modules/loop/engine_proxy.py:130` | `def search_proxy_body(self, task_id, query, limit)` |
| `TriageScheduler` | class | `modules/loop/triage_scheduler.py:85` | `class TriageScheduler` |
| `__init__` | method | `modules/loop/triage_scheduler.py:92` | `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)` |
| `_clamp01` | function | `modules/loop/triage_scheduler.py:31` | `def _clamp01(value)` |
| `_item` | function | `modules/loop/triage_scheduler.py:73` | `def _item(record)` |
| `estimate_difficulty` | function | `modules/loop/triage_scheduler.py:36` | `def estimate_difficulty(facts)` |
| `normal_key` | function | `modules/loop/triage_scheduler.py:156` | `def normal_key(record)` |
| `order` | method | `modules/loop/triage_scheduler.py:133` | `def order(self, records)` |
| `pick_next` | method | `modules/loop/triage_scheduler.py:172` | `def pick_next(self, records)` |
| `route` | method | `modules/loop/triage_scheduler.py:122` | `def route(self, record)` |
| `salvage_key` | function | `modules/loop/triage_scheduler.py:163` | `def salvage_key(record)` |
| `should_stop` | method | `modules/loop/triage_scheduler.py:110` | `def should_stop(self, record)` |
| `WorkerAgenticMixin` | class | `modules/loop/worker_agentic.py:225` | `class WorkerAgenticMixin` |
| `_agent_checkpoint` | method | `modules/loop/worker_agentic.py:235` | `def _agent_checkpoint(self, intent)` |
| `_agent_os_hint` | method | `modules/loop/worker_agentic.py:508` | `def _agent_os_hint(self, intent)` |
| `_agent_preflight` | method | `modules/loop/worker_agentic.py:263` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/loop/worker_agentic.py:524` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/loop/worker_agentic.py:296` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agent_verb_catalog` | method | `modules/loop/worker_agentic.py:480` | `def _agent_verb_catalog(self)` |
| `_agentic_try` | method | `modules/loop/worker_agentic.py:568` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_blocked_verbs` | method | `modules/loop/worker_agentic.py:878` | `def _blocked_verbs(self)` |
| `_capable_member_chain` | function | `modules/loop/worker_agentic.py:60` | `def _capable_member_chain(members)` |
| `_decision_context` | method | `modules/loop/worker_agentic.py:970` | `def _decision_context(self, intent)` |
| `_drain_steer` | method | `modules/loop/worker_agentic.py:252` | `def _drain_steer(self, intent)` |
| `_extract_llm_commands` | function | `modules/loop/worker_agentic.py:148` | `def _extract_llm_commands(reply)` |
| `_guard_filter` | method | `modules/loop/worker_agentic.py:1016` | `def _guard_filter(self, intent, candidates)` |
| `_guard_rules` | method | `modules/loop/worker_agentic.py:896` | `def _guard_rules(self)` |
| `_is_destructive_or_malformed` | function | `modules/loop/worker_agentic.py:43` | `def _is_destructive_or_malformed(command)` |
| `_is_placeholder_steps` | function | `modules/loop/worker_agentic.py:129` | `def _is_placeholder_steps(steps)` |
| `_llm_steps` | method | `modules/loop/worker_agentic.py:720` | `def _llm_steps(self, intent, prior_text)` |
| `_loop_deterministic` | function | `modules/loop/worker_agentic.py:112` | `def _loop_deterministic()` |
| `_planner_temperature` | function | `modules/loop/worker_agentic.py:87` | `def _planner_temperature()` |
| `_push` | function | `modules/loop/worker_agentic.py:170` | `def _push(value)` |
| `_record_deterministic_decision` | method | `modules/loop/worker_agentic.py:1047` | `def _record_deterministic_decision(self, intent, candidates, chosen, filtered)` |
| `_record_llm_decision` | method | `modules/loop/worker_agentic.py:918` | `def _record_llm_decision(self, intent, prompt, reply, candidates, chosen, filtered)` |
| `_strip_command` | function | `modules/loop/worker_agentic.py:143` | `def _strip_command(raw)` |
| `_try_json_commands` | function | `modules/loop/worker_agentic.py:189` | `def _try_json_commands(text)` |
| `_verb_of` | function | `modules/loop/worker_agentic.py:102` | `def _verb_of(command)` |
| `_with_llm_steps` | method | `modules/loop/worker_agentic.py:668` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `graph_state` | function | `modules/loop/worker_agentic.py:368` | `def graph_state()` |
| `job_output` | function | `modules/loop/worker_agentic.py:399` | `def job_output(job_id)` |
| `job_status` | function | `modules/loop/worker_agentic.py:391` | `def job_status(job_id)` |
| `record_fact` | function | `modules/loop/worker_agentic.py:335` | `def record_fact(text)` |
| `report_finding` | function | `modules/loop/worker_agentic.py:344` | `def report_finding(name, evidence, severity)` |
| `run_command` | function | `modules/loop/worker_agentic.py:308` | `def run_command(command, background)` |
| `shell_open` | function | `modules/loop/worker_agentic.py:383` | `def shell_open()` |
| `shell_send` | function | `modules/loop/worker_agentic.py:387` | `def shell_send(command)` |
| `traffic_search` | function | `modules/loop/worker_agentic.py:355` | `def traffic_search(query)` |
| `WorkerExecutionMixin` | class | `modules/loop/worker_execution.py:10` | `class WorkerExecutionMixin` |
| `_auto_approve` | method | `modules/loop/worker_execution.py:164` | `def _auto_approve(self, command)` |
| `_close_shell_session` | method | `modules/loop/worker_execution.py:126` | `def _close_shell_session(self)` |
| `_denied` | method | `modules/loop/worker_execution.py:153` | `def _denied(self, command)` |
| `_missing_tool` | method | `modules/loop/worker_execution.py:176` | `def _missing_tool(self, command)` |
| `_open_shell_session` | method | `modules/loop/worker_execution.py:55` | `def _open_shell_session(self, intent)` |
| `_reader` | function | `modules/loop/worker_execution.py:77` | `def _reader()` |
| `_resolved_command` | method | `modules/loop/worker_execution.py:239` | `def _resolved_command(self, command)` |
| `_run` | method | `modules/loop/worker_execution.py:192` | `def _run(self, command, executor)` |
| `_send_shell` | method | `modules/loop/worker_execution.py:90` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_start_background_job` | method | `modules/loop/worker_execution.py:22` | `def _start_background_job(self, command, intent, transcripts)` |
| `_work` | function | `modules/loop/worker_execution.py:35` | `def _work()` |
| `WorkerGatingMixin` | class | `modules/loop/worker_gating.py:6` | `class WorkerGatingMixin` |
| `_command_in_scope` | method | `modules/loop/worker_gating.py:157` | `def _command_in_scope(self, command)` |
| `_lab_scope_default` | method | `modules/loop/worker_gating.py:48` | `def _lab_scope_default(self, target)` |
| `_learn_os` | method | `modules/loop/worker_gating.py:106` | `def _learn_os(self, intent, command, output)` |
| `_os_gate` | method | `modules/loop/worker_gating.py:80` | `def _os_gate(self, intent, command)` |
| `_scope_allows_target` | method | `modules/loop/worker_gating.py:17` | `def _scope_allows_target(self, target)` |
| `_sudo_guard` | method | `modules/loop/worker_gating.py:130` | `def _sudo_guard(self, intent, command)` |
| `WorkerMemoryMixin` | class | `modules/loop/worker_memory.py:6` | `class WorkerMemoryMixin` |
| `_absorb_reaction` | method | `modules/loop/worker_memory.py:62` | `def _absorb_reaction(self, intent, command, output)` |
| `_attribute_outcome` | method | `modules/loop/worker_memory.py:122` | `def _attribute_outcome(self, intent, command, output)` |
| `_fact_memory_store` | method | `modules/loop/worker_memory.py:38` | `def _fact_memory_store(self)` |
| `_failure_memory` | method | `modules/loop/worker_memory.py:18` | `def _failure_memory(self)` |
| `_recall_facts` | method | `modules/loop/worker_memory.py:55` | `def _recall_facts(self, query, k)` |
| `_remember_fact` | method | `modules/loop/worker_memory.py:46` | `def _remember_fact(self, intent, command, output)` |
| `_hive_store` | function | `modules/loop_ai_bridge.py:101` | `def _hive_store(task_id, worker, kind, text)` |
| `_open` | function | `modules/loop_ai_bridge.py:104` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:260` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:285` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:307` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:326` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:347` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:369` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:390` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:424` | `def _open()` |
| `_singleton` | function | `modules/loop_ai_bridge.py:50` | `def _singleton(key, factory)` |
| `_stage` | function | `modules/loop_ai_bridge.py:64` | `def _stage(name, default)` |
| `ai_snapshot` | function | `modules/loop_ai_bridge.py:469` | `def ai_snapshot()` |
| `annotate_detection` | function | `modules/loop_ai_bridge.py:280` | `def annotate_detection(command, action_category)` |
| `assess_opsec` | function | `modules/loop_ai_bridge.py:125` | `def assess_opsec(command, rhost)` |
| `intent_tool_class` | function | `modules/loop_ai_bridge.py:169` | `def intent_tool_class(summary)` |
| `moe_record_outcome` | function | `modules/loop_ai_bridge.py:321` | `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` |
| `moe_route` | function | `modules/loop_ai_bridge.py:304` | `def moe_route(task_type, goal)` |
| `publish_loop_event` | function | `modules/loop_ai_bridge.py:74` | `def publish_loop_event(task_id, worker, kind, text, severity)` |
| `record_outcome_quality` | function | `modules/loop_ai_bridge.py:213` | `def record_outcome_quality(worker, intent_summary, facts, findings)` |
| `record_step` | function | `modules/loop_ai_bridge.py:404` | `def record_step(task_id, worker, command, output, detection_prob)` |
| `rl_save` | function | `modules/loop_ai_bridge.py:385` | `def rl_save()` |
| `rl_select` | function | `modules/loop_ai_bridge.py:340` | `def rl_select(task_type, phase, candidates, deterministic)` |
| `rl_update` | function | `modules/loop_ai_bridge.py:362` | `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` |
| `stream_enabled` | function | `modules/loop_ai_bridge.py:459` | `def stream_enabled()` |
| `swan_available` | function | `modules/loop_ai_bridge.py:419` | `def swan_available()` |
| `swan_consult` | function | `modules/loop_ai_bridge.py:432` | `def swan_consult(prompt, task_type, phase, timeout)` |
| `tool_class_yields` | function | `modules/loop_ai_bridge.py:240` | `def tool_class_yields(summaries, phase)` |
| `LoopAudit` | class | `modules/loop_audit.py:114` | `class LoopAudit` |
| `__init__` | method | `modules/loop_audit.py:123` | `def __init__(self, task_id, path)` |
| `_activity_event` | function | `modules/loop_audit.py:401` | `def _activity_event(row, start_ts)` |
| `_append` | method | `modules/loop_audit.py:273` | `def _append(self, event)` |
| `_clean` | function | `modules/loop_audit.py:56` | `def _clean(text, limit)` |
| `_consume_context` | function | `modules/loop_audit.py:103` | `def _consume_context()` |
| `_first_token` | function | `modules/loop_audit.py:61` | `def _first_token(command)` |
| `_fmt_offset` | function | `modules/loop_audit.py:439` | `def _fmt_offset(offset)` |
| `_guard_event` | function | `modules/loop_audit.py:389` | `def _guard_event(row, start_ts)` |
| `_output_tail` | function | `modules/loop_audit.py:71` | `def _output_tail(output)` |
| `_read` | method | `modules/loop_audit.py:303` | `def _read(path)` |
| `_read_jsonl` | function | `modules/loop_audit.py:355` | `def _read_jsonl(path)` |
| `_render_event` | function | `modules/loop_audit.py:444` | `def _render_event(event)` |
| `_timeline_event` | function | `modules/loop_audit.py:378` | `def _timeline_event(audit_row, start_ts)` |
| `_trim` | method | `modules/loop_audit.py:288` | `def _trim(self)` |
| `_ts` | function | `modules/loop_audit.py:370` | `def _ts(row)` |
| `activity_rows` | function | `modules/loop_audit.py:365` | `def activity_rows(task_id)` |
| `audit_for` | function | `modules/loop_audit.py:338` | `def audit_for(task_id)` |
| `audit_path` | function | `modules/loop_audit.py:109` | `def audit_path(task_id)` |
| `blocked` | method | `modules/loop_audit.py:178` | `def blocked(self, source, reason, command, worker, intent)` |
| `guard_rows` | function | `modules/loop_audit.py:360` | `def guard_rows(task_id)` |
| `list_runs` | function | `modules/loop_audit.py:526` | `def list_runs(limit)` |
| `path` | method | `modules/loop_audit.py:131` | `def path(self)` |
| `preflight` | method | `modules/loop_audit.py:168` | `def preflight(self, outcome)` |
| `record` | method | `modules/loop_audit.py:135` | `def record(self, kind)` |
| `record_command` | method | `modules/loop_audit.py:216` | `def record_command(self, command, output, duration, ok, task_id)` |
| `render` | function | `modules/loop_audit.py:505` | `def render(task_id, limit, audit)` |
| `render_summary` | function | `modules/loop_audit.py:563` | `def render_summary(summaries)` |
| `run_end` | method | `modules/loop_audit.py:203` | `def run_end(self, status, rounds, verdict, error)` |
| `run_start` | method | `modules/loop_audit.py:155` | `def run_start(self, goal, target, rounds, workers, mode, profile)` |
| `start` | function | `modules/loop_audit.py:320` | `def start(task_id)` |
| `step_context` | function | `modules/loop_audit.py:80` | `def step_context(task_id)` |
| `stop` | function | `modules/loop_audit.py:349` | `def stop(task_id)` |
| `timeline` | function | `modules/loop_audit.py:415` | `def timeline(task_id, audit)` |
| `verdict` | method | `modules/loop_audit.py:189` | `def verdict(self, verdict)` |
| `EdrPacer` | class | `modules/loop_guardrails.py:242` | `class EdrPacer` |
| `Fact` | class | `modules/loop_guardrails.py:86` | `class Fact` |
| `FactVectorStore` | class | `modules/loop_guardrails.py:589` | `class FactVectorStore` |
| `ListingNoiseDetector` | class | `modules/loop_guardrails.py:787` | `class ListingNoiseDetector` |
| `RepeatDetector` | class | `modules/loop_guardrails.py:95` | `class RepeatDetector` |
| `TargetLimiter` | class | `modules/loop_guardrails.py:519` | `class TargetLimiter` |
| `__init__` | method | `modules/loop_guardrails.py:117` | `def __init__(self, window)` |
| `__init__` | method | `modules/loop_guardrails.py:258` | `def __init__(self, duration_threshold)` |
| `__init__` | method | `modules/loop_guardrails.py:527` | `def __init__(self, max_concurrent)` |
| `__init__` | method | `modules/loop_guardrails.py:597` | `def __init__(self, path, max_facts)` |
| `__len__` | method | `modules/loop_guardrails.py:609` | `def __len__(self)` |
| `_alternating` | method | `modules/loop_guardrails.py:214` | `def _alternating(self)` |
| `_load` | method | `modules/loop_guardrails.py:726` | `def _load(self)` |
| `_periodic_cycle` | method | `modules/loop_guardrails.py:161` | `def _periodic_cycle(entries)` |
| `_strict_alternating` | method | `modules/loop_guardrails.py:156` | `def _strict_alternating(entries)` |
| `_tokenize` | method | `modules/loop_guardrails.py:613` | `def _tokenize(text)` |
| `_update_oscillation` | method | `modules/loop_guardrails.py:142` | `def _update_oscillation(self)` |
| `_vectorize` | method | `modules/loop_guardrails.py:618` | `def _vectorize(tokens)` |
| `_window_seconds_until_end` | method | `modules/loop_guardrails.py:401` | `def _window_seconds_until_end(windows, now)` |
| `active_targets` | method | `modules/loop_guardrails.py:539` | `def active_targets(self)` |
| `add` | method | `modules/loop_guardrails.py:626` | `def add(self, text, meta)` |
| `clear` | method | `modules/loop_guardrails.py:699` | `def clear(self)` |
| `cycle` | method | `modules/loop_guardrails.py:226` | `def cycle(self)` |
| `decay` | method | `modules/loop_guardrails.py:379` | `def decay(self, factor)` |
| `describe` | method | `modules/loop_guardrails.py:200` | `def describe(self)` |
| `describe` | method | `modules/loop_guardrails.py:504` | `def describe(self)` |
| `from_config` | method | `modules/loop_guardrails.py:326` | `def from_config(cls)` |
| `in_sleeper_window` | method | `modules/loop_guardrails.py:426` | `def in_sleeper_window(self, now)` |
| `inter_step_delay` | method | `modules/loop_guardrails.py:472` | `def inter_step_delay(self)` |
| `last_commands` | method | `modules/loop_guardrails.py:230` | `def last_commands(self)` |
| `level` | method | `modules/loop_guardrails.py:385` | `def level(self)` |
| `listing_forbidden` | function | `modules/loop_guardrails.py:759` | `def listing_forbidden(command)` |
| `max_concurrent` | method | `modules/loop_guardrails.py:534` | `def max_concurrent(self)` |
| `observe` | method | `modules/loop_guardrails.py:357` | `def observe(self, command, duration_sec, output)` |
| `observe` | method | `modules/loop_guardrails.py:798` | `def observe(self, command, output)` |
| `oscillation_pair` | method | `modules/loop_guardrails.py:222` | `def oscillation_pair(self)` |
| `parse_windows` | method | `modules/loop_guardrails.py:304` | `def parse_windows(raw)` |
| `path` | method | `modules/loop_guardrails.py:605` | `def path(self)` |
| `quieten` | method | `modules/loop_guardrails.py:489` | `def quieten(self, command)` |
| `record` | method | `modules/loop_guardrails.py:125` | `def record(self, command)` |
| `reset` | method | `modules/loop_guardrails.py:234` | `def reset(self)` |
| `save` | method | `modules/loop_guardrails.py:705` | `def save(self)` |
| `search` | method | `modules/loop_guardrails.py:660` | `def search(self, query, k)` |
| `search_block` | method | `modules/loop_guardrails.py:690` | `def search_block(self, query, k, max_chars)` |
| `signal` | method | `modules/loop_guardrails.py:395` | `def signal(self)` |
| `sleeper_delay` | method | `modules/loop_guardrails.py:459` | `def sleeper_delay(self, now)` |
| `slot` | method | `modules/loop_guardrails.py:545` | `def slot(self, target)` |
| `stuck` | method | `modules/loop_guardrails.py:182` | `def stuck(self)` |
| `windows_delay` | method | `modules/loop_guardrails.py:432` | `def windows_delay(windows, now)` |
| `LoopManager` | class | `modules/loop_manager.py:314` | `class LoopManager` |
| `LoopNotFoundError` | class | `modules/loop_manager.py:94` | `class LoopNotFoundError(KeyError)` |
| `LoopSpec` | class | `modules/loop_manager.py:262` | `class LoopSpec` |
| `LoopValidationError` | class | `modules/loop_manager.py:85` | `class LoopValidationError(ValueError)` |
| `__init__` | method | `modules/loop_manager.py:88` | `def __init__(self, field, message)` |
| `__init__` | method | `modules/loop_manager.py:325` | `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` |
| `_load_registry_locked` | method | `modules/loop_manager.py:817` | `def _load_registry_locked(self)` |
| `_loop_command` | function | `modules/loop_manager.py:282` | `def _loop_command(spec)` |
| `_now_iso` | function | `modules/loop_manager.py:215` | `def _now_iso()` |
| `_pid_alive` | function | `modules/loop_manager.py:244` | `def _pid_alive(pid, start_ticks)` |
| `_process_start_ticks` | function | `modules/loop_manager.py:220` | `def _process_start_ticks(pid)` |
| `_prune_locked` | method | `modules/loop_manager.py:768` | `def _prune_locked(self)` |
| `_read_outcome` | method | `modules/loop_manager.py:529` | `def _read_outcome(workspace)` |
| `_reap` | method | `modules/loop_manager.py:470` | `def _reap(self, loop_id, process)` |
| `_refresh_log_bytes` | method | `modules/loop_manager.py:570` | `def _refresh_log_bytes(self, record)` |
| `_remove_workspace` | method | `modules/loop_manager.py:793` | `def _remove_workspace(self, loop_id)` |
| `_resolve_log_path` | method | `modules/loop_manager.py:641` | `def _resolve_log_path(self, record)` |
| `_save_registry_locked` | method | `modules/loop_manager.py:832` | `def _save_registry_locked(self, records)` |
| `_spawn_locked` | method | `modules/loop_manager.py:392` | `def _spawn_locked(self, spec, operator)` |
| `_update_status_locked` | method | `modules/loop_manager.py:715` | `def _update_status_locked(self, loop_id, status)` |
| `_write_workspace_metadata` | method | `modules/loop_manager.py:512` | `def _write_workspace_metadata(record)` |
| `clamp_float` | function | `modules/loop_manager.py:173` | `def clamp_float(raw, field, default, minimum, maximum)` |
| `clamp_int` | function | `modules/loop_manager.py:148` | `def clamp_int(raw, field, default, minimum, maximum)` |
| `default_manager` | function | `modules/loop_manager.py:850` | `def default_manager()` |
| `get_loop` | method | `modules/loop_manager.py:581` | `def get_loop(self, loop_id)` |
| `list_loops` | method | `modules/loop_manager.py:546` | `def list_loops(self)` |
| `loops_dir` | method | `modules/loop_manager.py:347` | `def loops_dir(self)` |
| `read_log` | method | `modules/loop_manager.py:600` | `def read_log(self, loop_id, offset)` |
| `sanitize_goal` | function | `modules/loop_manager.py:121` | `def sanitize_goal(raw)` |
| `start` | method | `modules/loop_manager.py:351` | `def start(self, spec, operator)` |
| `stop` | method | `modules/loop_manager.py:667` | `def stop(self, loop_id)` |
| `summary` | method | `modules/loop_manager.py:732` | `def summary(self)` |
| `validate_loop_id` | function | `modules/loop_manager.py:198` | `def validate_loop_id(loop_id)` |
| `validate_target` | function | `modules/loop_manager.py:98` | `def validate_target(raw)` |
| `_probe` | function | `modules/loop_preflight.py:107` | `def _probe(port)` |
| `check_target` | function | `modules/loop_preflight.py:145` | `def check_target(target, ports, connect_timeout, lab)` |
| `lab_state_for` | function | `modules/loop_preflight.py:38` | `def lab_state_for(target, scenarios, running, existing, ip_lookup)` |
| `probe_tcp` | function | `modules/loop_preflight.py:125` | `def probe_tcp(target, ports, timeout)` |
| `probe_tcp_detailed` | function | `modules/loop_preflight.py:83` | `def probe_tcp_detailed(target, ports, timeout)` |
| `recovery_hint` | function | `modules/loop_preflight.py:211` | `def recovery_hint(outcome)` |
| `LoopProgress` | class | `modules/loop_progress.py:169` | `class LoopProgress` |
| `LoopSnapshot` | class | `modules/loop_progress.py:80` | `class LoopSnapshot` |
| `__post_init__` | method | `modules/loop_progress.py:182` | `def __post_init__(self)` |
| `_footer` | method | `modules/loop_progress.py:306` | `def _footer(self, snapshot, elapsed)` |
| `_header` | method | `modules/loop_progress.py:282` | `def _header(self)` |
| `_milestone_line` | method | `modules/loop_progress.py:289` | `def _milestone_line(self, snapshot, states, current)` |
| `_render` | method | `modules/loop_progress.py:324` | `def _render(self, snapshot)` |
| `emit` | method | `modules/loop_progress.py:268` | `def emit(self, line)` |
| `live_mode` | method | `modules/loop_progress.py:195` | `def live_mode(self)` |
| `refresh` | method | `modules/loop_progress.py:246` | `def refresh(self, snapshot)` |
| `sanitize_line` | function | `modules/loop_progress.py:151` | `def sanitize_line(line, keep_ansi)` |
| `snap_to_states` | function | `modules/loop_progress.py:123` | `def snap_to_states(snapshot)` |
| `snapshot_from_overview` | function | `modules/loop_progress.py:99` | `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)` |
| `start` | method | `modules/loop_progress.py:202` | `def start(self)` |
| `stop` | method | `modules/loop_progress.py:229` | `def stop(self)` |
| `TriggerStore` | class | `modules/loop_triggers.py:88` | `class TriggerStore` |
| `__init__` | method | `modules/loop_triggers.py:91` | `def __init__(self, task_id)` |
| `_core` | function | `modules/loop_triggers.py:81` | `def _core()` |
| `_load` | method | `modules/loop_triggers.py:97` | `def _load(self)` |
| `add` | method | `modules/loop_triggers.py:101` | `def add(self, kind, arg, every_sec)` |
| `due` | method | `modules/loop_triggers.py:233` | `def due(self, task_id, graph, activity, assets, store)` |
| `ensure_ad_surface_trigger` | method | `modules/loop_triggers.py:220` | `def ensure_ad_surface_trigger(self)` |
| `ensure_cve_hot_trigger` | method | `modules/loop_triggers.py:207` | `def ensure_cve_hot_trigger(self)` |
| `ensure_service_trigger` | method | `modules/loop_triggers.py:194` | `def ensure_service_trigger(self)` |
| `hint_fingerprint` | function | `modules/loop_triggers.py:28` | `def hint_fingerprint(row)` |
| `list` | method | `modules/loop_triggers.py:190` | `def list(self)` |
| `prune_hint_fingerprints` | function | `modules/loop_triggers.py:60` | `def prune_hint_fingerprints(store, now, ttl)` |
| `read_signing_evidence` | function | `modules/loop_triggers.py:499` | `def read_signing_evidence(store_dir)` |
| `remove` | method | `modules/loop_triggers.py:165` | `def remove(self, trigger_id)` |
| `set_enabled` | method | `modules/loop_triggers.py:176` | `def set_enabled(self, trigger_id, enabled)` |
| `upsert_defaults` | method | `modules/loop_triggers.py:123` | `def upsert_defaults(self, seeds)` |
| `MacOSPayloadConfig` | class | `modules/macos_payloads.py:60` | `class MacOSPayloadConfig` |
| `MacOSPayloadFactory` | class | `modules/macos_payloads.py:88` | `class MacOSPayloadFactory` |
| `__init__` | method | `modules/macos_payloads.py:111` | `def __init__(self, config, output_dir)` |
| `_adho_codesign` | method | `modules/macos_payloads.py:192` | `def _adho_codesign(self, app_dir)` |
| `_obfuscate_shell` | method | `modules/macos_payloads.py:116` | `def _obfuscate_shell(self, code)` |
| `_reverse_shell_command` | method | `modules/macos_payloads.py:122` | `def _reverse_shell_command(self)` |
| `generate_all` | method | `modules/macos_payloads.py:470` | `def generate_all(self)` |
| `generate_app_bundle` | method | `modules/macos_payloads.py:137` | `def generate_app_bundle(self)` |
| `generate_launchd_persistence` | method | `modules/macos_payloads.py:212` | `def generate_launchd_persistence(self)` |
| `generate_osascript_dropper` | method | `modules/macos_payloads.py:314` | `def generate_osascript_dropper(self)` |
| `generate_persistence_scripts` | method | `modules/macos_payloads.py:398` | `def generate_persistence_scripts(self)` |
| `generate_phishing_dialog` | method | `modules/macos_payloads.py:447` | `def generate_phishing_dialog(self)` |
| `generate_swift_stager` | method | `modules/macos_payloads.py:335` | `def generate_swift_stager(self)` |
| `generate_tcc_bypass` | method | `modules/macos_payloads.py:268` | `def generate_tcc_bypass(self)` |
| `list_persistence_methods` | method | `modules/macos_payloads.py:522` | `def list_persistence_methods()` |
| `list_tcc_services` | method | `modules/macos_payloads.py:517` | `def list_tcc_services()` |
| `check_collision` | function | `modules/mario.py:105` | `def check_collision(x, y, layer)` |
| `AgentBridgeWorker` | class | `modules/mcp_agent_bridge.py:468` | `class AgentBridgeWorker` |
| `GroqAgentWorker` | class | `modules/mcp_agent_bridge.py:234` | `class GroqAgentWorker` |
| `OllamaReActWorker` | class | `modules/mcp_agent_bridge.py:367` | `class OllamaReActWorker` |
| `__init__` | method | `modules/mcp_agent_bridge.py:235` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:368` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:471` | `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)` |
| `_agent_file` | function | `modules/mcp_agent_bridge.py:141` | `def _agent_file(agent_id)` |
| `_make_client` | function | `modules/mcp_agent_bridge.py:39` | `def _make_client(backend)` |
| `_ollama_chat` | function | `modules/mcp_agent_bridge.py:92` | `def _ollama_chat(model, messages, max_tokens, timeout)` |
| `_parse` | method | `modules/mcp_agent_bridge.py:381` | `def _parse(self, text)` |
| `_read_log` | function | `modules/mcp_agent_bridge.py:150` | `def _read_log(agent_id)` |
| `_tools` | method | `modules/mcp_agent_bridge.py:248` | `def _tools(self)` |
| `_write_log` | function | `modules/mcp_agent_bridge.py:145` | `def _write_log(agent_id, entry)` |
| `dummy_runner` | function | `modules/mcp_agent_bridge.py:531` | `def dummy_runner(cmd)` |
| `get_agent_result` | function | `modules/mcp_agent_bridge.py:188` | `def get_agent_result(agent_id)` |
| `get_agent_status` | function | `modules/mcp_agent_bridge.py:163` | `def get_agent_status(agent_id)` |
| `list_agents` | function | `modules/mcp_agent_bridge.py:211` | `def list_agents(limit)` |
| `run` | method | `modules/mcp_agent_bridge.py:264` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:389` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:478` | `def run(self)` |
| `start_agent` | function | `modules/mcp_agent_bridge.py:508` | `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` |
| `ChainMediator` | class | `modules/mediation/chain_mediator.py:48` | `class ChainMediator` |
| `LlmPoolPort` | class | `modules/mediation/chain_mediator.py:13` | `class LlmPoolPort` |
| `__init__` | method | `modules/mediation/chain_mediator.py:53` | `def __init__(self)` |
| `complete` | method | `modules/mediation/chain_mediator.py:16` | `def complete(self, prompt, max_tokens, task_id)` |
| `describe` | method | `modules/mediation/chain_mediator.py:73` | `def describe(self)` |
| `has_members` | method | `modules/mediation/chain_mediator.py:34` | `def has_members(self)` |
| `llm` | method | `modules/mediation/chain_mediator.py:65` | `def llm(self)` |
| `register_llm_port` | method | `modules/mediation/chain_mediator.py:57` | `def register_llm_port(self, port)` |
| `ActivityLogPort` | class | `modules/mediation/contracts.py:36` | `class ActivityLogPort(Protocol)` |
| `LlmCompletionPort` | class | `modules/mediation/contracts.py:58` | `class LlmCompletionPort(Protocol)` |
| `MediationDomains` | class | `modules/mediation/contracts.py:12` | `class MediationDomains` |
| `MediationHubContract` | class | `modules/mediation/contracts.py:96` | `class MediationHubContract(Protocol)` |
| `MediatorContract` | class | `modules/mediation/contracts.py:85` | `class MediatorContract(Protocol)` |
| `complete` | method | `modules/mediation/contracts.py:61` | `def complete(self, prompt, max_tokens, task_id)` |
| `describe` | method | `modules/mediation/contracts.py:90` | `def describe(self)` |
| `has_members` | method | `modules/mediation/contracts.py:79` | `def has_members(self)` |
| `is_known` | method | `modules/mediation/contracts.py:24` | `def is_known(cls, domain)` |
| `mediator_for` | method | `modules/mediation/contracts.py:99` | `def mediator_for(self, domain)` |
| `read` | method | `modules/mediation/contracts.py:45` | `def read(self, limit)` |
| `resolve` | function | `modules/mediation/contracts.py:104` | `def resolve(domain)` |
| `EngineMediator` | class | `modules/mediation/engine_mediator.py:66` | `class EngineMediator` |
| `ExploitRetryPort` | class | `modules/mediation/engine_mediator.py:32` | `class ExploitRetryPort(Protocol)` |
| `ReactionPort` | class | `modules/mediation/engine_mediator.py:49` | `class ReactionPort(Protocol)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:52` | `def analyse(self, output, command, platform)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:100` | `def analyse(self, output, command, platform)` |
| `describe` | method | `modules/mediation/engine_mediator.py:71` | `def describe(self)` |
| `retry_with_credentials` | method | `modules/mediation/engine_mediator.py:35` | `def retry_with_credentials(self, target, credentials)` |
| `retry_with_credentials` | method | `modules/mediation/engine_mediator.py:79` | `def retry_with_credentials(self, target, credentials)` |
| `FeedbackMediator` | class | `modules/mediation/feedback_mediator.py:13` | `class FeedbackMediator` |
| `describe` | method | `modules/mediation/feedback_mediator.py:18` | `def describe(self)` |
| `order_steps` | method | `modules/mediation/feedback_mediator.py:22` | `def order_steps(self, steps, stack)` |
| `MediationHub` | class | `modules/mediation/hub.py:19` | `class MediationHub` |
| `__init__` | method | `modules/mediation/hub.py:22` | `def __init__(self)` |
| `_build_default` | function | `modules/mediation/hub.py:55` | `def _build_default()` |
| `default_hub` | function | `modules/mediation/hub.py:75` | `def default_hub()` |
| `get_hub` | function | `modules/mediation/hub.py:80` | `def get_hub()` |
| `mediator_for` | method | `modules/mediation/hub.py:35` | `def mediator_for(self, domain)` |
| `register` | method | `modules/mediation/hub.py:26` | `def register(self, mediator)` |
| `snapshot` | method | `modules/mediation/hub.py:46` | `def snapshot(self)` |
| `IntelMediator` | class | `modules/mediation/intel_mediator.py:13` | `class IntelMediator` |
| `__init__` | method | `modules/mediation/intel_mediator.py:18` | `def __init__(self)` |
| `activity_records` | method | `modules/mediation/intel_mediator.py:39` | `def activity_records(self, task_id, limit)` |
| `describe` | method | `modules/mediation/intel_mediator.py:32` | `def describe(self)` |
| `mask_configured` | method | `modules/mediation/intel_mediator.py:133` | `def mask_configured(self, text)` |
| `record_routing_decision` | method | `modules/mediation/intel_mediator.py:64` | `def record_routing_decision(self, task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | method | `modules/mediation/intel_mediator.py:97` | `def record_routing_outcome(self, task_id, intent_id, command, state, facts, findings, stack)` |
| `register_activity_log_factory` | method | `modules/mediation/intel_mediator.py:22` | `def register_activity_log_factory(self, factory)` |
| `stack_signature` | method | `modules/mediation/intel_mediator.py:149` | `def stack_signature(self, assets)` |
| `TelemetryMediator` | class | `modules/mediation/telemetry_mediator.py:14` | `class TelemetryMediator` |
| `annotate_detection` | method | `modules/mediation/telemetry_mediator.py:43` | `def annotate_detection(self, command)` |
| `assess_opsec` | method | `modules/mediation/telemetry_mediator.py:59` | `def assess_opsec(self, command, rhost)` |
| `describe` | method | `modules/mediation/telemetry_mediator.py:19` | `def describe(self)` |
| `moe_record_outcome` | method | `modules/mediation/telemetry_mediator.py:203` | `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` |
| `moe_route` | method | `modules/mediation/telemetry_mediator.py:162` | `def moe_route(self, task_type)` |
| `publish_event` | method | `modules/mediation/telemetry_mediator.py:23` | `def publish_event(self, task_id, worker, kind, text, severity)` |
| `record_outcome_quality` | method | `modules/mediation/telemetry_mediator.py:77` | `def record_outcome_quality(self, worker, intent_summary, facts, findings)` |
| `record_step` | method | `modules/mediation/telemetry_mediator.py:111` | `def record_step(self, task_id, worker, command, output, detection_prob)` |
| `rl_select` | method | `modules/mediation/telemetry_mediator.py:178` | `def rl_select(self, task_type, phase, candidates, deterministic)` |
| `rl_update` | method | `modules/mediation/telemetry_mediator.py:219` | `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` |
| `swan_available` | method | `modules/mediation/telemetry_mediator.py:128` | `def swan_available(self)` |
| `swan_consult` | method | `modules/mediation/telemetry_mediator.py:137` | `def swan_consult(self, prompt, task_type, phase, timeout)` |
| `tool_class_yields` | method | `modules/mediation/telemetry_mediator.py:93` | `def tool_class_yields(self, summaries, phase)` |
| `MemoryCleaner` | class | `modules/memory_cleaner.py:50` | `class MemoryCleaner` |
| `MemoryCleanerConfig` | class | `modules/memory_cleaner.py:22` | `class MemoryCleanerConfig` |
| `__init__` | method | `modules/memory_cleaner.py:61` | `def __init__(self, config)` |
| `generate_on_exit_script` | method | `modules/memory_cleaner.py:255` | `def generate_on_exit_script(self)` |
| `linux_memory_cleanup` | method | `modules/memory_cleaner.py:151` | `def linux_memory_cleanup(self)` |
| `macos_memory_cleanup` | method | `modules/memory_cleaner.py:206` | `def macos_memory_cleanup(self)` |
| `windows_memory_cleanup` | method | `modules/memory_cleaner.py:64` | `def windows_memory_cleanup(self)` |
| `EmbeddingError` | class | `modules/memory_embeddings.py:30` | `class EmbeddingError(ValueError)` |
| `_fnv1a` | function | `modules/memory_embeddings.py:34` | `def _fnv1a(data)` |
| `_tokens` | function | `modules/memory_embeddings.py:41` | `def _tokens(text)` |
| `as_floats` | function | `modules/memory_embeddings.py:109` | `def as_floats(blob)` |
| `cosine` | function | `modules/memory_embeddings.py:75` | `def cosine(a, b)` |
| `embed` | function | `modules/memory_embeddings.py:50` | `def embed(text)` |
| `semantic_top_k` | function | `modules/memory_embeddings.py:85` | `def semantic_top_k(query, candidates, top_k)` |
| `MemoryEntry` | class | `modules/memory_store.py:84` | `class MemoryEntry` |
| `MemoryStore` | class | `modules/memory_store.py:237` | `class MemoryStore` |
| `SQLiteBackend` | class | `modules/memory_store.py:132` | `class SQLiteBackend(StorageBackend)` |
| `StorageBackend` | class | `modules/memory_store.py:97` | `class StorageBackend(ABC)` |
| `VectorSQLiteBackend` | class | `modules/memory_store.py:315` | `class VectorSQLiteBackend(SQLiteBackend)` |
| `__init__` | method | `modules/memory_store.py:133` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/memory_store.py:240` | `def __init__(self, backend)` |
| `_cli` | function | `modules/memory_store.py:381` | `def _cli()` |
| `_connect` | method | `modules/memory_store.py:139` | `def _connect(self)` |
| `_fetch` | method | `modules/memory_store.py:175` | `def _fetch(self, sql, params)` |
| `_print_entries` | function | `modules/memory_store.py:368` | `def _print_entries(entries)` |
| `_row_to_entry` | function | `modules/memory_store.py:117` | `def _row_to_entry(row)` |
| `all_entries` | method | `modules/memory_store.py:111` | `def all_entries(self, limit)` |
| `all_entries` | method | `modules/memory_store.py:215` | `def all_entries(self, limit)` |
| `by_host` | method | `modules/memory_store.py:105` | `def by_host(self, host, top_k)` |
| `by_host` | method | `modules/memory_store.py:192` | `def by_host(self, host, top_k)` |
| `by_service` | method | `modules/memory_store.py:108` | `def by_service(self, service, top_k)` |
| `by_service` | method | `modules/memory_store.py:203` | `def by_service(self, service, top_k)` |
| `close` | method | `modules/memory_store.py:114` | `def close(self)` |
| `close` | method | `modules/memory_store.py:232` | `def close(self)` |
| `export_finetuning_dataset` | method | `modules/memory_store.py:300` | `def export_finetuning_dataset(self, path)` |
| `get_memory_store` | function | `modules/memory_store.py:339` | `def get_memory_store()` |
| `recall` | method | `modules/memory_store.py:270` | `def recall(self, query, top_k)` |
| `recall` | function | `modules/memory_store.py:360` | `def recall(query, top_k)` |
| `recall_by_host` | method | `modules/memory_store.py:273` | `def recall_by_host(self, host, top_k)` |
| `recall_for_service` | method | `modules/memory_store.py:276` | `def recall_for_service(self, service_name, top_k)` |
| `recall_hybrid` | method | `modules/memory_store.py:279` | `def recall_hybrid(self, query, top_k)` |
| `recall_hybrid` | function | `modules/memory_store.py:364` | `def recall_hybrid(query, top_k)` |
| `remember` | method | `modules/memory_store.py:243` | `def remember(self, session_id, host, tool, command, output, findings, success)` |
| `remember` | function | `modules/memory_store.py:348` | `def remember(session_id, host, tool, command, output, findings, success)` |
| `save` | method | `modules/memory_store.py:99` | `def save(self, entry)` |
| `save` | method | `modules/memory_store.py:148` | `def save(self, entry)` |
| `save` | method | `modules/memory_store.py:320` | `def save(self, entry)` |
| `search` | method | `modules/memory_store.py:102` | `def search(self, query, top_k)` |
| `search` | method | `modules/memory_store.py:180` | `def search(self, query, top_k)` |
| `search_semantic` | method | `modules/memory_store.py:328` | `def search_semantic(self, query, top_k)` |
| `stats` | method | `modules/memory_store.py:292` | `def stats(self)` |
| `stats_raw` | method | `modules/memory_store.py:225` | `def stats_raw(self)` |
| `_load_yaml` | function | `modules/metasploitable_gym.py:30` | `def _load_yaml(path)` |
| `chain_for` | function | `modules/metasploitable_gym.py:62` | `def chain_for(vuln_id, path)` |
| `exploit_for` | function | `modules/metasploitable_gym.py:72` | `def exploit_for(vuln_id, path)` |
| `get` | function | `modules/metasploitable_gym.py:53` | `def get(vuln_id, path)` |
| `load_index` | function | `modules/metasploitable_gym.py:42` | `def load_index(path)` |
| `main` | function | `modules/metasploitable_gym.py:157` | `def main()` |
| `summary` | function | `modules/metasploitable_gym.py:138` | `def summary(path)` |
| `validate_matrix` | function | `modules/metasploitable_gym.py:82` | `def validate_matrix(path)` |
| `vulnerabilities` | function | `modules/metasploitable_gym.py:47` | `def vulnerabilities(path)` |
| `Migration` | class | `modules/metasploitable_migrations.py:129` | `class Migration` |
| `_core_services_apply` | function | `modules/metasploitable_migrations.py:180` | `def _core_services_apply()` |
| `_docker_exec` | function | `modules/metasploitable_migrations.py:150` | `def _docker_exec(container, script, payload, timeout)` |
| `apply_migrations` | function | `modules/metasploitable_migrations.py:354` | `def apply_migrations(container, subnet)` |
| `build_migrations` | function | `modules/metasploitable_migrations.py:194` | `def build_migrations(subnet)` |
| `MetricRecord` | class | `modules/metrics.py:146` | `class MetricRecord` |
| `MetricsAggregator` | class | `modules/metrics.py:226` | `class MetricsAggregator` |
| `MetricsRecorder` | class | `modules/metrics.py:332` | `class MetricsRecorder` |
| `MetricsRegistry` | class | `modules/metrics.py:54` | `class MetricsRegistry` |
| `MetricsWriter` | class | `modules/metrics.py:181` | `class MetricsWriter` |
| `__init__` | method | `modules/metrics.py:63` | `def __init__(self)` |
| `__init__` | method | `modules/metrics.py:189` | `def __init__(self, path)` |
| `__init__` | method | `modules/metrics.py:339` | `def __init__(self, writer)` |
| `_labels_key` | function | `modules/metrics.py:126` | `def _labels_key(labels)` |
| `_percentile` | method | `modules/metrics.py:234` | `def _percentile(values, percentile)` |
| `_read_all` | method | `modules/metrics.py:388` | `def _read_all(self)` |
| `append` | method | `modules/metrics.py:206` | `def append(self, record)` |
| `get` | method | `modules/metrics.py:87` | `def get(self, name, labels)` |
| `get_recorder` | function | `modules/metrics.py:452` | `def get_recorder()` |
| `inc` | method | `modules/metrics.py:69` | `def inc(self, name, labels, value)` |
| `path` | method | `modules/metrics.py:201` | `def path(self)` |
| `path` | method | `modules/metrics.py:350` | `def path(self)` |
| `prometheus_text` | method | `modules/metrics.py:107` | `def prometheus_text(self)` |
| `record` | method | `modules/metrics.py:355` | `def record(self, command, args, duration_ms, success, exit_code, source)` |
| `reset_recorder_for_tests` | function | `modules/metrics.py:466` | `def reset_recorder_for_tests(writer)` |
| `summarize` | method | `modules/metrics.py:254` | `def summarize(cls, records, window_seconds, now_utc)` |
| `summarize` | method | `modules/metrics.py:416` | `def summarize(self, window_seconds)` |
| `tail` | method | `modules/metrics.py:430` | `def tail(self, n)` |
| `to_dict` | method | `modules/metrics.py:167` | `def to_dict(self)` |
| `MFABypassEngine` | class | `modules/mfa_bypass.py:121` | `class MFABypassEngine` |
| `MFABypassResult` | class | `modules/mfa_bypass.py:113` | `class MFABypassResult` |
| `MFATarget` | class | `modules/mfa_bypass.py:103` | `class MFATarget` |
| `__init__` | method | `modules/mfa_bypass.py:128` | `def __init__(self, sessions_dir)` |
| `enumerate_techniques` | method | `modules/mfa_bypass.py:133` | `def enumerate_techniques(self, target)` |
| `export_report` | method | `modules/mfa_bypass.py:303` | `def export_report(self)` |

Next: [SYMBOLS_p21.md](SYMBOLS_p21.md)
