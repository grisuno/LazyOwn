# Subsystem: loop

## modules/loop/__init__.py
- Layer: utility
- Language: py
- Depends on: `modules/loop/engine_proxy.py`, `modules/loop/triage_scheduler.py`, `modules/loop/worker_agentic.py`, `modules/loop/worker_execution.py`, `modules/loop/worker_gating.py`, `modules/loop/worker_memory.py`
- Imported by: `modules/lazy_loop.py`, `modules/loop/worker_agentic.py`, `modules/sidequest.py`, `tests/test_lazy_scope.py`, `tests/test_loop_decision_log.py`, `tests/test_loop_deterministic_mode.py`, `tests/test_sidequest.py`

## modules/loop/decision_log.py
- Doc: Reproducible decision ledger for the autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `digest` (function, line 51) `def digest(text)`
  - `_canonical` (function, line 68) `def _canonical(value)`
  - `context_digest` (function, line 90) `def context_digest(ctx)`
  - `config_digest` (function, line 115) `def config_digest(config)`
  - `new_run_id` (function, line 137) `def new_run_id()`
  - `DecisionRecord` (class, line 143) `class DecisionRecord`
  - `_rotate` (function, line 182) `def _rotate(path)`
  - `record` (function, line 192) `def record(rec, path)`
  - `read_records` (function, line 221) `def read_records(path)`
  - `filtered_rows` (function, line 248) `def filtered_rows(items)`

## modules/loop/engine_proxy.py
- Doc: EngineProxyMixin: Recorder-proxy lifecycle and traffic ingestion for the loop engine.
- Layer: utility
- Language: py
- Symbols:
  - `EngineProxyMixin` (class, line 4) `class EngineProxyMixin`
  - `proxy_start` (method, line 16) `def proxy_start(self, host, port, task_id, trust, upstream)`
  - `proxy_stop` (method, line 52) `def proxy_stop(self)`
  - `proxy_status` (method, line 60) `def proxy_status(self)`
  - `proxy_env` (method, line 66) `def proxy_env(self)`
  - `ingest_proxy_traffic` (method, line 75) `def ingest_proxy_traffic(self, task_id, limit)`
  - `search_proxy_body` (method, line 130) `def search_proxy_body(self, task_id, query, limit)`
  - `_maybe_proxy_gc` (method, line 157) `def _maybe_proxy_gc(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/traffic_recorder.py`
- Imported by: `modules/loop/__init__.py`

## modules/loop/triage_scheduler.py
- Doc: Difficulty-triage scheduling for the autonomous multi-target loop.
- Layer: infrastructure
- Language: py
- Symbols:
  - `_clamp01` (function, line 31) `def _clamp01(value)`
  - `estimate_difficulty` (function, line 36) `def estimate_difficulty(facts)`
  - `_item` (function, line 73) `def _item(record)`
  - `TriageScheduler` (class, line 85) `class TriageScheduler`
  - `__init__` (method, line 92) `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)`
  - `should_stop` (method, line 110) `def should_stop(self, record)`
  - `route` (method, line 122) `def route(self, record)`
  - `order` (method, line 133) `def order(self, records)`
  - `pick_next` (method, line 172) `def pick_next(self, records)`
  - `normal_key` (function, line 156) `def normal_key(record)`
  - `salvage_key` (function, line 163) `def salvage_key(record)`
- Imported by: `modules/lazy_loop.py`, `modules/loop/__init__.py`, `tests/test_triage_scheduler.py`

## modules/loop/worker_agentic.py
- Doc: WorkerAgenticMixin: Tool-calling agent loop and LLM step planning for a loop worker.
- Layer: utility
- Language: py
- Symbols:
  - `_is_destructive_or_malformed` (function, line 43) `def _is_destructive_or_malformed(command)`
  - `_capable_member_chain` (function, line 60) `def _capable_member_chain(members)`
  - `_planner_temperature` (function, line 87) `def _planner_temperature()`
  - `_verb_of` (function, line 102) `def _verb_of(command)`
  - `_loop_deterministic` (function, line 112) `def _loop_deterministic()`
  - `_is_placeholder_steps` (function, line 129) `def _is_placeholder_steps(steps)`
  - `_strip_command` (function, line 143) `def _strip_command(raw)`
  - `_extract_llm_commands` (function, line 148) `def _extract_llm_commands(reply)`
  - `_try_json_commands` (function, line 189) `def _try_json_commands(text)`
  - `WorkerAgenticMixin` (class, line 225) `class WorkerAgenticMixin`
  - `_push` (function, line 170) `def _push(value)`
  - `_agent_checkpoint` (method, line 235) `def _agent_checkpoint(self, intent)`
  - `_drain_steer` (method, line 252) `def _drain_steer(self, intent)`
  - `_agent_preflight` (method, line 263) `def _agent_preflight(self, intent, command)`
  - `_agent_tools` (method, line 296) `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)`
  - `_agent_verb_catalog` (method, line 480) `def _agent_verb_catalog(self)`
  - `_agent_os_hint` (method, line 508) `def _agent_os_hint(self, intent)`
  - `_agent_system_prompt` (method, line 524) `def _agent_system_prompt(self, intent)`
  - `_agentic_try` (method, line 568) `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)`
  - `_with_llm_steps` (method, line 668) `def _with_llm_steps(self, intent, steps, prior_text)`
  - `_llm_steps` (method, line 720) `def _llm_steps(self, intent, prior_text)`
  - `_blocked_verbs` (method, line 878) `def _blocked_verbs(self)`
  - `_guard_rules` (method, line 896) `def _guard_rules(self)`
  - `_record_llm_decision` (method, line 918) `def _record_llm_decision(self, intent, prompt, reply, candidates, chosen, filtered)`
  - `_decision_context` (method, line 970) `def _decision_context(self, intent)`
  - `_guard_filter` (method, line 1016) `def _guard_filter(self, intent, candidates)`
  - `_record_deterministic_decision` (method, line 1047) `def _record_deterministic_decision(self, intent, candidates, chosen, filtered)`
  - `run_command` (function, line 308) `def run_command(command, background)`
  - `record_fact` (function, line 335) `def record_fact(text)`
  - `report_finding` (function, line 344) `def report_finding(name, evidence, severity)`
  - `traffic_search` (function, line 355) `def traffic_search(query)`
  - `graph_state` (function, line 368) `def graph_state()`
  - `shell_open` (function, line 383) `def shell_open()`
  - `shell_send` (function, line 387) `def shell_send(command)`
  - `job_status` (function, line 391) `def job_status(job_id)`
  - `job_output` (function, line 399) `def job_output(job_id)`
- Depends on: `core/config.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/guard_rules.py`, `modules/harness.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/lazy_skills.py`, `modules/loop/__init__.py`, `modules/outcome_attribution.py`
- Imported by: `modules/loop/__init__.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_decision_log.py`, `tests/test_loop_deterministic_mode.py`, `tests/test_outcome_attribution.py`

## modules/loop/worker_execution.py
- Doc: WorkerExecutionMixin: Command execution, background jobs and persistent-shell lifecycle for a...
- Layer: utility
- Language: py
- Symbols:
  - `WorkerExecutionMixin` (class, line 10) `class WorkerExecutionMixin`
  - `_start_background_job` (method, line 22) `def _start_background_job(self, command, intent, transcripts)`
  - `_open_shell_session` (method, line 55) `def _open_shell_session(self, intent)`
  - `_send_shell` (method, line 90) `def _send_shell(self, command, intent, timeout_sec)`
  - `_close_shell_session` (method, line 126) `def _close_shell_session(self)`
  - `_denied` (method, line 153) `def _denied(self, command)`
  - `_auto_approve` (method, line 164) `def _auto_approve(self, command)`
  - `_missing_tool` (method, line 176) `def _missing_tool(self, command)`
  - `_run` (method, line 192) `def _run(self, command, executor)`
  - `_resolved_command` (method, line 239) `def _resolved_command(self, command)`
  - `_work` (function, line 35) `def _work()`
  - `_reader` (function, line 77) `def _reader()`
- Depends on: `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/lazy_loop.py`, `utils.py`
- Imported by: `modules/loop/__init__.py`

## modules/loop/worker_gating.py
- Doc: WorkerGatingMixin: Scope, operating-system and privilege gates for a loop worker.
- Layer: utility
- Language: py
- Symbols:
  - `WorkerGatingMixin` (class, line 6) `class WorkerGatingMixin`
  - `_scope_allows_target` (method, line 17) `def _scope_allows_target(self, target)`
  - `_lab_scope_default` (method, line 48) `def _lab_scope_default(self, target)`
  - `_os_gate` (method, line 80) `def _os_gate(self, intent, command)`
  - `_learn_os` (method, line 106) `def _learn_os(self, intent, command, output)`
  - `_sudo_guard` (method, line 130) `def _sudo_guard(self, intent, command)`
  - `_command_in_scope` (method, line 157) `def _command_in_scope(self, command)`
- Depends on: `modules/__init__.py`, `modules/intercept.py`, `modules/lazy_loop.py`, `utils.py`
- Imported by: `modules/loop/__init__.py`

## modules/loop/worker_memory.py
- Doc: WorkerMemoryMixin: Durable and in-session memory behaviour for a loop worker.
- Layer: utility
- Language: py
- Symbols:
  - `WorkerMemoryMixin` (class, line 6) `class WorkerMemoryMixin`
  - `_failure_memory` (method, line 18) `def _failure_memory(self)`
  - `_fact_memory_store` (method, line 38) `def _fact_memory_store(self)`
  - `_remember_fact` (method, line 46) `def _remember_fact(self, intent, command, output)`
  - `_recall_facts` (method, line 55) `def _recall_facts(self, query, k)`
  - `_absorb_reaction` (method, line 62) `def _absorb_reaction(self, intent, command, output)`
  - `_attribute_outcome` (method, line 122) `def _attribute_outcome(self, intent, command, output)`
- Depends on: `modules/auto_loop_memory.py`, `modules/lazy_loop.py`, `modules/loop_guardrails.py`, `modules/mediation/contracts.py`, `modules/mediation/hub.py`, `modules/outcome_attribution.py`, `modules/reaction_bridge.py`, `modules/world_model.py`
- Imported by: `modules/loop/__init__.py`
