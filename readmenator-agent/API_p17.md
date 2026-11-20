# API (page 17 of 29)
Previous: [API_p16.md](API_p16.md)

## modules/llm_factory.py
Depends on: `core/llm_budget.py`, `core/llm_key_pool.py`, `modules/ai_model.py`, `modules/harness.py`, `modules/llm_client.py`, `modules/llm_orchestrator.py`, `modules/toposwarm_bridge.py`
Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/ai_model.py`, `modules/beacon_loop.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/lazyllmchat.py`, `modules/llm_adapter.py`, `modules/llm_orchestrator.py`, `modules/mcp_agent_bridge.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/sidequest.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/conftest.py`, `tests/test_ai_commands_llm.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_llm_resilience.py`, `tests/test_payload_schema.py`, `tests/test_vulnbot_fallback.py`, `tests/test_wizard_llm.py`
- `is_model_missing_error` (function) `modules/llm_factory.py:137` `def is_model_missing_error(message)` -- Return True when an error text means the model id is unavailable.
- `groq_model_chain` (function) `modules/llm_factory.py:157` `def groq_model_chain(config)` -- Return the ordered Groq model ids to try, configured model first.
- `default_model_for` (function) `modules/llm_factory.py:246` `def default_model_for(backend)` -- Return the default model identifier for a backend.
- `model_config_key` (function) `modules/llm_factory.py:267` `def model_config_key(backend)` -- Return the ``payload.json`` key holding a backend's model override.
- `api_key_config_key` (function) `modules/llm_factory.py:288` `def api_key_config_key(backend)` -- Return the ``payload.json`` key holding a backend's API key slot.
- `backend_requires_api_key` (function) `modules/llm_factory.py:313` `def backend_requires_api_key(backend)` -- Report whether a backend needs an API key to operate.
- `load_payload` (function) `modules/llm_factory.py:331` `def load_payload(payload_path)` -- Read ``payload.json`` from disk and return it as a dictionary.
- `get_llm_backend` (function) `modules/llm_factory.py:729` `def get_llm_backend(config, backend)` -- Return a concrete :class:`AIModel` selected by configuration.
- `get_llm_backend_raw` (function) `modules/llm_factory.py:828` `def get_llm_backend_raw(config, backend)` -- Return a raw :class:`AIModel` without the budget wrapper.
- `try_get_llm_backend` (function) `modules/llm_factory.py:850` `def try_get_llm_backend(config, backend)` -- Return a backend or ``None`` if construction fails for any reason.
- `stream_complete` (function) `modules/llm_factory.py:927` `def stream_complete(model, prompt, max_tokens, on_delta)` -- Completion that reports incremental deltas while it arrives.
- `complete` (function) `modules/llm_factory.py:998` `def complete(model, prompt, max_tokens, temperature)` -- Complete a prompt through one model spec; raise when unanswered.

## modules/llm_orchestrator.py
Depends on: `modules/lazy_engine.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/orchestrator_config.py`
Imported by: `lazyc2.py`, `modules/ai_fallback.py`, `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_vulnbot_fallback.py`
- `OrchestratorResult.ok` (method) `modules/llm_orchestrator.py:118` `def ok(self)` -- Return True when a chain member served the answer.
- `OrchestratorResult.display_text` (method) `modules/llm_orchestrator.py:123` `def display_text(self)` -- Return the notice-prefixed answer for operator-facing surfaces.
- `sort_members` (function) `modules/llm_orchestrator.py:130` `def sort_members(members)` -- Return a weight-sorted defensive copy of a member list.
- `pool_chain` (function) `modules/llm_orchestrator.py:148` `def pool_chain()` -- Return the failover chain governed by lazy_orchestrator.
- `backend_kind` (function) `modules/llm_orchestrator.py:175` `def backend_kind(model_spec)` -- Return the provider prefix of a model spec.
- `is_error_reply` (function) `modules/llm_orchestrator.py:192` `def is_error_reply(text)` -- Return True when a reply is a backend error banner, not content.
- `is_placeholder_key` (function) `modules/llm_orchestrator.py:211` `def is_placeholder_key(value)` -- Return True when a key value is a shipped placeholder, not a secret.
- `complete_with_fallback` (function) `modules/llm_orchestrator.py:349` `def complete_with_fallback(prompt, system, max_tokens, api_key, members, executor, health, record)` -- Complete a prompt through the lazy_orchestrator chain with failover.

## modules/llm_pool.py
Imported by: `cli/commands/ai.py`, `modules/lazy_loop.py`, `modules/llm_orchestrator.py`, `skills/autonomous_daemon.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_runner.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_tokens.py`
- `register_usage_sink` (function) `modules/llm_pool.py:45` `def register_usage_sink(sink)` -- Register an observer receiving (member, prompt_chars, completion_chars).
- `usage_sinks` (function) `modules/llm_pool.py:56` `def usage_sinks()` -- Return the registered usage observers.
- `shared_registry` (function) `modules/llm_pool.py:79` `def shared_registry(config)` -- Return the process-wide health registry (LAZY Registry parity).
- `HealthRegistry.__init__` (method) `modules/llm_pool.py:112` `def __init__(self, config)` -- Initialize counters from the persisted breaker state.
- `HealthRegistry.report_success` (method) `modules/llm_pool.py:164` `def report_success(self, member_id)` -- Clear failure state for a member.
- `HealthRegistry.report_failure` (method) `modules/llm_pool.py:172` `def report_failure(self, member_id, error)` -- Record a failure; auth/quota errors trip immediately.
- `HealthRegistry.healthy` (method) `modules/llm_pool.py:192` `def healthy(self, member_id)` -- Return True when a member may serve traffic.
- `LLMPool.__init__` (method) `modules/llm_pool.py:208` `def __init__(self, members, health, config)` -- Order members by descending rank (RR within equal rank).
- `LLMPool.members` (method) `modules/llm_pool.py:221` `def members(self)` -- Return chain members in order.
- `LLMPool.session_key` (method) `modules/llm_pool.py:225` `def session_key(self, conversation_id, role, index)` -- Build a sticky session header (LAZY session_header parity).
- `LLMPool.complete` (method) `modules/llm_pool.py:266` `def complete(self, prompt, max_tokens, session_key, overflow_dir)` -- Complete a prompt with pre-token failover across members.

## modules/llm_prompts.py
Depends on: `modules/colors.py`
Imported by: `cli/commands/ai.py`, `modules/llm_adapter.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_llm_prompts.py`
- `default_project_root` (function) `modules/llm_prompts.py:67` `def default_project_root()` -- Return the repository root that owns the LLM prompt configuration.
- `resolve_model` (function) `modules/llm_prompts.py:76` `def resolve_model(model)` -- Resolve an explicit model or fall back to the randomized Groq model.
- `truncate_message` (function) `modules/llm_prompts.py:95` `def truncate_message(message, max_chars)` -- Truncate a message with an ellipsis marker when it exceeds the limit.
- `LlmPromptConfig.from_defaults` (method) `modules/llm_prompts.py:130` `def from_defaults(cls, project_root)` -- Build a config rooted at the given project root.
- `LlmPromptConfig.knowledge_base_path` (method) `modules/llm_prompts.py:150` `def knowledge_base_path(self, domain)` -- Return the absolute path for a knowledge-base domain file.
- `LlmPromptConfig.load_payload_context` (method) `modules/llm_prompts.py:161` `def load_payload_context(self)` -- Load the operator context keyed by :data:`PAYLOAD_KEY_ORDER`.
- `LlmPromptConfig.load_event_tool_output` (method) `modules/llm_prompts.py:176` `def load_event_tool_output(self, event_name)` -- Load tool output attached to a named event in event_config.json.
- `LlmPromptConfig.load_plan_history` (method) `modules/llm_prompts.py:203` `def load_plan_history(self)` -- Load the session plan history text if present.
- `LlmPromptConfig.load_report_context` (method) `modules/llm_prompts.py:218` `def load_report_context(self)` -- Load the JSON artefacts consumed by the report template.
- `LlmPromptConfig.knowledge_store` (method) `modules/llm_prompts.py:238` `def knowledge_store(self, domain)` -- Build a knowledge store bound to a domain file.
- `LlmPromptConfig.render` (method) `modules/llm_prompts.py:249` `def render(self, template, base_prompt)` -- Render a named template with shared knowledge and context.
- `render_kb_tail` (function) `modules/llm_prompts.py:271` `def render_kb_tail(lines)` -- Join the most recent knowledge lines for embedding into a prompt.
- `KnowledgeStore.__init__` (method) `modules/llm_prompts.py:289` `def __init__(self, path)` -- Initialize a store bound to a single JSON file.
- `KnowledgeStore.load` (method) `modules/llm_prompts.py:297` `def load(self)` -- Load the knowledge-base records from disk.
- `KnowledgeStore.save` (method) `modules/llm_prompts.py:312` `def save(self, records)` -- Persist a full record list to disk, creating parent directories.
- `KnowledgeStore.add` (method) `modules/llm_prompts.py:324` `def add(self, prompt, response)` -- Append a prompt/response record to the knowledge base.
- `KnowledgeStore.relevant` (method) `modules/llm_prompts.py:335` `def relevant(self, prompt, limit)` -- Return knowledge responses whose text shares keywords with the prompt.

## modules/log_tamper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `LogTamper.__init__` (method) `modules/log_tamper.py:105` `def __init__(self, config)`
- `LogTamper.windows_clear_commands` (method) `modules/log_tamper.py:108` `def windows_clear_commands(self)` -- Generate Windows Event Log clearing commands.
- `LogTamper.linux_clear_commands` (method) `modules/log_tamper.py:176` `def linux_clear_commands(self)` -- Generate Linux log clearing commands.
- `LogTamper.macos_clear_commands` (method) `modules/log_tamper.py:243` `def macos_clear_commands(self)` -- Generate macOS log clearing commands.
- `LogTamper.generate_all` (method) `modules/log_tamper.py:295` `def generate_all(self)` -- Generate log tampering commands for all platforms.
- `LogTamper.auditd_disable_commands` (method) `modules/log_tamper.py:307` `def auditd_disable_commands(self)` -- Commands to temporarily disable or reconfigure auditd on Linux.
- `LogTamper.sysmon_disable_commands` (method) `modules/log_tamper.py:341` `def sysmon_disable_commands(self)` -- Commands to disable or degrade Sysmon on Windows.

## modules/logging_config.py
Depends on: `core/logging.py`
Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`
- `ColoredFormatter.format` (method) `modules/logging_config.py:39` `def format(self, record)`
- `JsonFormatter.format` (method) `modules/logging_config.py:72` `def format(self, record)`
- `CorrelationFilter.filter` (method) `modules/logging_config.py:94` `def filter(self, record)`
- `ResilientRotatingFileHandler.emit` (method) `modules/logging_config.py:116` `def emit(self, record)` -- Write one record, no-op after the file has become unwritable.
- `ResilientRotatingFileHandler.handleError` (method) `modules/logging_config.py:122` `def handleError(self, record)` -- Suppress the default per-record traceback; notify once via stderr.
- `set_correlation_id` (function) `modules/logging_config.py:134` `def set_correlation_id(cid)` -- Set the correlation ID for the current async/task context.
- `get_correlation_id` (function) `modules/logging_config.py:139` `def get_correlation_id()` -- Return the current correlation ID, or None.
- `clear_correlation_id` (function) `modules/logging_config.py:144` `def clear_correlation_id()` -- Reset the correlation ID for the current context.
- `configure` (function) `modules/logging_config.py:244` `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` -- Configure LazyOwn's centralized logging system.
- `get_logger` (function) `modules/logging_config.py:328` `def get_logger(name, level)` -- Get a logger with the given name.
- `set_level` (function) `modules/logging_config.py:357` `def set_level(name, level)` -- Set the log level for a specific logger.
- `set_quiet` (function) `modules/logging_config.py:367` `def set_quiet()` -- Silence all logging below WARNING level.
- `set_verbose` (function) `modules/logging_config.py:373` `def set_verbose()` -- Enable DEBUG level logging.
- `silence_module` (function) `modules/logging_config.py:379` `def silence_module(name)` -- Completely silence a noisy module.
- `reset` (function) `modules/logging_config.py:388` `def reset()` -- Reset the logging system to defaults.

## modules/loop/boundary.py
Imported by: `modules/agent_runner.py`, `modules/lazy_loop.py`, `tests/test_loop_boundary.py`, `tests/test_loop_citation_judge.py`
- `fence_result` (function) `modules/loop/boundary.py:34` `def fence_result(content)` -- Fence one tool result and append the short code-owned tail.
- `nonce` (function) `modules/loop/boundary.py:42` `def nonce()` -- Return a short random marker nonce.
- `fence` (function) `modules/loop/boundary.py:52` `def fence(label, content, value)` -- Wrap untrusted content between a nonce marker pair.
- `code_tail` (function) `modules/loop/boundary.py:75` `def code_tail()` -- Return the fixed code-owned boundary tail.
- `check_leakage` (function) `modules/loop/boundary.py:80` `def check_leakage(prompt)` -- Return marker tokens that do not appear exactly twice (unclosed fences).
- `wrap_context_section` (function) `modules/loop/boundary.py:93` `def wrap_context_section(label, content, sections)` -- Append a fenced section to a prompt sections list (convenience).
- `tail_sections` (function) `modules/loop/boundary.py:100` `def tail_sections(sections)` -- Join prompt sections and append the code-owned tail.

## modules/loop/control_plane.py
Depends on: `core/logging.py`
Imported by: `skills/autonomous_daemon.py`, `tests/test_control_plane.py`
- `precheck_control` (function) `modules/loop/control_plane.py:23` `def precheck_control(control, target, objective_id, step_n, emit, loop, wait_until_unpaused, poll_interval, max_wait)` -- Run the per-step operator control gate.

## modules/loop/daemon_reward.py
Depends on: `modules/atomic_exploit_bridge.py`
Imported by: `skills/autonomous_daemon.py`, `tests/test_daemon_reward_contract.py`
- `_Trainer.encode_state` (method) `modules/loop/daemon_reward.py:88` `def encode_state(self, task_type, engagement_phase, recent_reward_ema)`
- `_Trainer.update` (method) `modules/loop/daemon_reward.py:90` `def update(self, state, action, reward, next_state, candidates, detection_prob)`
- `_Trainer.save` (method) `modules/loop/daemon_reward.py:100` `def save(self)`
- `compute_step_reward` (function) `modules/loop/daemon_reward.py:126` `def compute_step_reward(output, command, phase, success, findings, prev_cmds)` -- Compute the multi-dimensional RL reward for one executed step.
- `record_rl_feedback` (function) `modules/loop/daemon_reward.py:189` `def record_rl_feedback(trainer, source, command, phase, output, success, findings, prev_cmds, prior_ema, detection_prob)` -- Apply one honest temporal-difference update for an executed step.

## modules/loop/decision_log.py
- `digest` (function) `modules/loop/decision_log.py:51` `def digest(text)` -- Return the stable short digest used to fingerprint a decision input.
- `context_digest` (function) `modules/loop/decision_log.py:90` `def context_digest(ctx)` -- Fingerprint a selection context independent of field ordering.
- `config_digest` (function) `modules/loop/decision_log.py:115` `def config_digest(config)` -- Fingerprint the config keys that change a decision's reproducibility.
- `new_run_id` (function) `modules/loop/decision_log.py:137` `def new_run_id()` -- Return a fresh identifier grouping all decisions of one loop run.
- `record` (function) `modules/loop/decision_log.py:192` `def record(rec, path)` -- Append one decision to the ledger, rotating it when oversized.
- `read_records` (function) `modules/loop/decision_log.py:221` `def read_records(path)` -- Return every decision row in order, for audit or deterministic replay.
- `filtered_rows` (function) `modules/loop/decision_log.py:248` `def filtered_rows(items)` -- Shape ``(command, reason)`` pairs into ledger-ready rejection rows.

## modules/loop/engine_proxy.py
Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/traffic_recorder.py`
Imported by: `modules/loop/__init__.py`
- `EngineProxyMixin.proxy_start` (method) `modules/loop/engine_proxy.py:16` `def proxy_start(self, host, port, task_id, trust, upstream)` -- Start the shared recorder proxy and apply its trust environment.
- `EngineProxyMixin.proxy_stop` (method) `modules/loop/engine_proxy.py:52` `def proxy_stop(self)` -- Stop the recorder proxy and clear its trust environment.
- `EngineProxyMixin.proxy_status` (method) `modules/loop/engine_proxy.py:60` `def proxy_status(self)` -- Return recorder proxy state (running, address, CA, exchanges).
- `EngineProxyMixin.proxy_env` (method) `modules/loop/engine_proxy.py:66` `def proxy_env(self)` -- Return the environment overrides that route tools via proxy.
- `EngineProxyMixin.ingest_proxy_traffic` (method) `modules/loop/engine_proxy.py:75` `def ingest_proxy_traffic(self, task_id, limit)` -- Mirror new recorder exchanges into the task traffic log.
- `EngineProxyMixin.search_proxy_body` (method) `modules/loop/engine_proxy.py:130` `def search_proxy_body(self, task_id, query, limit)` -- Full-text search proxy bodies scoped to one task's exchanges.

## modules/loop/evidence.py
Depends on: `modules/__init__.py`
Imported by: `modules/lazy_loop.py`, `tests/test_loop_evidence.py`
- `normalize_ws` (function) `modules/loop/evidence.py:25` `def normalize_ws(text)` -- Collapse whitespace runs to single spaces and strip.
- `verbatim_contains` (function) `modules/loop/evidence.py:30` `def verbatim_contains(quote, source)` -- Return True when the quote appears verbatim (whitespace-normalised).
- `extract_quote` (function) `modules/loop/evidence.py:37` `def extract_quote(text)` -- Extract the best quoted span from finding text (best effort).
- `CitationService.__init__` (method) `modules/loop/evidence.py:56` `def __init__(self, max_age_sec)`
- `CitationService.verify` (method) `modules/loop/evidence.py:59` `def verify(self, quote, traffic)` -- Search the task traffic log for the quote.
- `CitationService.replay` (method) `modules/loop/evidence.py:98` `def replay(self, command, executor, traffic)` -- Replay the stored PoC command once and verify the quote in output.
- `CitationService.annotate` (method) `modules/loop/evidence.py:127` `def annotate(self, finding, verification)` -- Merge a citation verification into a finding meta dict.
- `citation_service_from_orchestrator` (function) `modules/loop/evidence.py:138` `def citation_service_from_orchestrator()` -- Build the citation service from the active orchestrator profile.
- `citation_enabled` (function) `modules/loop/evidence.py:153` `def citation_enabled()` -- Return whether citation verification is enabled (default True).

## modules/loop/leases.py
Depends on: `modules/loop/state_db.py`
Imported by: `modules/lazy_loop.py`, `tests/test_loop_leases.py`
- `LeaseStore.__init__` (method) `modules/loop/leases.py:54` `def __init__(self, db_path)`
- `LeaseStore.try_claim` (method) `modules/loop/leases.py:69` `def try_claim(self, task_id, node_id, worker, ttl_sec)` -- Acquire or refresh the lease for one intent, or fail when held.
- `LeaseStore.heartbeat` (method) `modules/loop/leases.py:113` `def heartbeat(self, task_id, node_id, ttl_sec)` -- Extend one live lease; settled or expired leases do not extend.
- `LeaseStore.settle` (method) `modules/loop/leases.py:128` `def settle(self, task_id, node_id)` -- Mark the lease settled so the intent can never be claimed again.
- `LeaseStore.release` (method) `modules/loop/leases.py:142` `def release(self, task_id, node_id)` -- Drop the lease row so the intent becomes claimable again.
- `LeaseStore.active` (method) `modules/loop/leases.py:155` `def active(self, task_id, node_id)` -- Return True when an unexpired, unsettled lease exists.
- `LeaseStore.sweep` (method) `modules/loop/leases.py:169` `def sweep(self, now)` -- Drop expired live leases and return the freed claims.
- `LeaseStore.counts` (method) `modules/loop/leases.py:205` `def counts(self)` -- Return live, expired and settled lease counts (observability).

## modules/loop/objective_bootstrap.py
Depends on: `core/logging.py`, `modules/enrich.py`, `modules/goals.py`, `modules/intercept.py`, `modules/planner.py`
Imported by: `skills/autonomous_daemon.py`, `tests/test_objective_bootstrap.py`
- `bootstrap_objective` (function) `modules/loop/objective_bootstrap.py:46` `def bootstrap_objective(objective_id, objective_text, target, world_model, obs_parser, planner, emit, load_payload)` -- Run every once-per-objective setup step before the loop.

## modules/loop/planner_bridge.py
Depends on: `core/logging.py`, `modules/__init__.py`, `modules/planner.py`
Imported by: `modules/lazy_loop.py`, `tests/test_loop_planner_bridge.py`
- `planner_bridge_enabled` (function) `modules/loop/planner_bridge.py:22` `def planner_bridge_enabled()` -- Return whether the technique->intent bridge is enabled (default True).
- `technique_candidate_summary` (function) `modules/loop/planner_bridge.py:34` `def technique_candidate_summary(candidate)` -- Render one PlanCandidate as an intent summary line.
- `technique_intents` (function) `modules/loop/planner_bridge.py:45` `def technique_intents(target, max_candidates)` -- Run the technique planner for a target and return intent summaries.
- `bridge_candidates_for_task` (function) `modules/loop/planner_bridge.py:70` `def bridge_candidates_for_task(target, existing, max_candidates)` -- Return bridge candidate tuples the engine planner can consume.

## modules/loop/state_db.py
Imported by: `modules/loop/leases.py`, `modules/loop/tokens.py`
- `default_db_path` (function) `modules/loop/state_db.py:21` `def default_db_path()` -- Return the default loop state database path under sessions.
- `connect` (function) `modules/loop/state_db.py:26` `def connect(db_path)` -- Open a new WAL SQLite connection with a bounded lock wait.
- `thread_connection` (function) `modules/loop/state_db.py:44` `def thread_connection(db_path)` -- Return the per-thread connection for a database path.

## modules/loop/target_os.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `skills/autonomous_daemon.py`
- `detect_target_os` (function) `modules/loop/target_os.py:42` `def detect_target_os(target, loop)` -- Infer the target OS from ICMP TTL via a single ping probe.
- `os_id_for` (function) `modules/loop/target_os.py:93` `def os_id_for(detected_os)` -- Map an OS label to the LazyOwn canonical ``os_id`` string.
- `persist_detected_os` (function) `modules/loop/target_os.py:105` `def persist_detected_os(objective_id, target, detected_os, world_model, emit, load_payload, sessions_dir, payload_file)` -- Record the detected OS as ground truth across every consumer.

## modules/loop/tokens.py
Depends on: `modules/__init__.py`, `modules/loop/state_db.py`
Imported by: `modules/lazy_loop.py`, `tests/test_loop_tokens.py`
- `estimate_tokens` (function) `modules/loop/tokens.py:44` `def estimate_tokens(chars)` -- Estimate token count from character count (deterministic heuristic).
- `register_llm_sink` (function) `modules/loop/tokens.py:49` `def register_llm_sink()` -- Wire the ledger into the LLM pool usage sink (idempotent).
- `shared_ledger` (function) `modules/loop/tokens.py:64` `def shared_ledger()` -- Return the process-wide ledger bound to the default database.
- `TokenLedger.__init__` (method) `modules/loop/tokens.py:79` `def __init__(self, db_path)`
- `TokenLedger.charge_chars` (method) `modules/loop/tokens.py:89` `def charge_chars(self, member, prompt_chars, completion_chars, task_id, intent_id)` -- Charge one estimated-token usage row from raw characters.
- `TokenLedger.charge` (method) `modules/loop/tokens.py:104` `def charge(self, task_id, prompt_tokens, completion_tokens, intent_id, member)` -- Charge one explicit token usage row.
- `TokenLedger.usage` (method) `modules/loop/tokens.py:117` `def usage(self, task_id, intent_id)` -- Return prompt/completion/total token sums for a task or intent.
- `TokenLedger.reset` (method) `modules/loop/tokens.py:139` `def reset(self, task_id)` -- Delete usage rows for one task; returns removed count.
- `TokenLedger.counts` (method) `modules/loop/tokens.py:149` `def counts(self)` -- Return total rows and token sums (observability).
- `TerminationPolicy.from_orchestrator` (method) `modules/loop/tokens.py:182` `def from_orchestrator(cls)` -- Build the policy from the active orchestrator profile.
- `TerminationPolicy.wrapup_reserve` (method) `modules/loop/tokens.py:214` `def wrapup_reserve(self, max_tokens)` -- Return the reserved token count that the wrap-up must keep.
- `TerminationPolicy.guard` (method) `modules/loop/tokens.py:223` `def guard(self, task_id, ledger, intent_id)` -- Return the spend verdict and the action the loop must take.

## modules/loop/triage_scheduler.py
Imported by: `modules/lazy_loop.py`, `modules/loop/__init__.py`, `tests/test_triage_scheduler.py`
- `estimate_difficulty` (function) `modules/loop/triage_scheduler.py:36` `def estimate_difficulty(facts)` -- Estimate a target's difficulty in ``[0.0, 1.0]`` from known facts.
- `TriageScheduler.__init__` (method) `modules/loop/triage_scheduler.py:92` `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)` -- Initialize the scheduler with its policy thresholds.
- `TriageScheduler.should_stop` (method) `modules/loop/triage_scheduler.py:110` `def should_stop(self, record)` -- Return True when a target has burned its attempt budget unproductively.
- `TriageScheduler.route` (method) `modules/loop/triage_scheduler.py:122` `def route(self, record)` -- Return the worker tier for a target: ``general`` (hard) or ``soldier``.
- `TriageScheduler.order` (method) `modules/loop/triage_scheduler.py:133` `def order(self, records)` -- Return records ordered for draining.
- `normal_key` (function) `modules/loop/triage_scheduler.py:156` `def normal_key(record)`
- `salvage_key` (function) `modules/loop/triage_scheduler.py:163` `def salvage_key(record)`
- `TriageScheduler.pick_next` (method) `modules/loop/triage_scheduler.py:172` `def pick_next(self, records)` -- Return the single record to drain next, or None when empty.

## modules/loop/worker_agentic.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/guard_rules.py`, `modules/harness.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/lazy_skills.py`, `modules/loop/__init__.py`, `modules/outcome_attribution.py`
Imported by: `modules/loop/__init__.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_decision_log.py`, `tests/test_loop_deterministic_mode.py`, `tests/test_loop_verb_capabilities.py`, `tests/test_outcome_attribution.py`
- `run_command` (function) `modules/loop/worker_agentic.py:308` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/loop/worker_agentic.py:335` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/loop/worker_agentic.py:344` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/loop/worker_agentic.py:355` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/loop/worker_agentic.py:368` `def graph_state()` -- Compact exploration overview plus already-discovered assets.
- `shell_open` (function) `modules/loop/worker_agentic.py:400` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/loop/worker_agentic.py:404` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/loop/worker_agentic.py:408` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/loop/worker_agentic.py:416` `def job_output(job_id)` -- Return the tail of one background job's output.

## modules/loop_ai_bridge.py
Depends on: `core/config.py`, `modules/atomic_exploit_bridge.py`, `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/moe_router.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/mediation/telemetry_mediator.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`, `tests/test_mediation.py`
- `publish_loop_event` (function) `modules/loop_ai_bridge.py:74` `def publish_loop_event(task_id, worker, kind, text, severity)` -- Publish one loop activity to the unified bus and Hive memory.
- `assess_opsec` (function) `modules/loop_ai_bridge.py:125` `def assess_opsec(command, rhost)` -- Return a pre-execution OPSEC gate assessment, or None when unavailable.
- `intent_tool_class` (function) `modules/loop_ai_bridge.py:169` `def intent_tool_class(summary)` -- Return the coarse tool class an intent summary belongs to.
- `record_outcome_quality` (function) `modules/loop_ai_bridge.py:213` `def record_outcome_quality(worker, intent_summary, facts, findings)` -- Feed one intent's net yield back to MoE/RL as a decision-quality reward.
- `tool_class_yields` (function) `modules/loop_ai_bridge.py:240` `def tool_class_yields(summaries, phase)` -- Return the learned decision-quality yield for each candidate summary.
- `annotate_detection` (function) `modules/loop_ai_bridge.py:280` `def annotate_detection(command, action_category)` -- Return oracle details for one command, or None when unavailable.
- `moe_route` (function) `modules/loop_ai_bridge.py:304` `def moe_route(task_type, goal)` -- Return the MoE router's preferred expert for a task type, or None.
- `moe_record_outcome` (function) `modules/loop_ai_bridge.py:321` `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` -- Feed one execution outcome back to the MoE performance store.
- `rl_select` (function) `modules/loop_ai_bridge.py:340` `def rl_select(task_type, phase, candidates, deterministic)` -- Pick an expert with the RL policy; first candidate when unavailable.
- `rl_update` (function) `modules/loop_ai_bridge.py:362` `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.
- `rl_save` (function) `modules/loop_ai_bridge.py:385` `def rl_save()` -- Persist the RL tables after a run.
- `record_step` (function) `modules/loop_ai_bridge.py:407` `def record_step(task_id, worker, command, output, detection_prob)` -- Feed one executed command outcome to MoE and the RL trainer.
- `swan_available` (function) `modules/loop_ai_bridge.py:435` `def swan_available()` -- Return True when the SWAN orchestrator can be constructed.
- `swan_consult` (function) `modules/loop_ai_bridge.py:448` `def swan_consult(prompt, task_type, phase, timeout)` -- Ask SWAN for an ensemble answer; empty string when unavailable.
- `stream_enabled` (function) `modules/loop_ai_bridge.py:475` `def stream_enabled()` -- Return whether token streaming into the activity log is enabled.
- `ai_snapshot` (function) `modules/loop_ai_bridge.py:485` `def ai_snapshot()` -- Compact status of the wired AI stack for the operator log.

## modules/loop_audit.py
Depends on: `core/parsers.py`
Imported by: `modules/lazy_loop.py`
- `step_context` (function) `modules/loop_audit.py:80` `def step_context(task_id)` -- Annotate every command executed inside the block with step context.
- `audit_path` (function) `modules/loop_audit.py:109` `def audit_path(task_id)` -- Return the audit file path for one task.
- `LoopAudit.__init__` (method) `modules/loop_audit.py:123` `def __init__(self, task_id, path)` -- Bind the audit file and start the run clock.
- `LoopAudit.path` (method) `modules/loop_audit.py:131` `def path(self)` -- Return the timeline file path.
- `LoopAudit.record` (method) `modules/loop_audit.py:135` `def record(self, kind)` -- Append one event and enforce the file cap.
- `LoopAudit.run_start` (method) `modules/loop_audit.py:155` `def run_start(self, goal, target, rounds, workers, mode, profile)` -- Record the loop lifecycle start.
- `LoopAudit.preflight` (method) `modules/loop_audit.py:168` `def preflight(self, outcome)` -- Record the target preflight verdict.
- `LoopAudit.blocked` (method) `modules/loop_audit.py:178` `def blocked(self, source, reason, command, worker, intent)` -- Record a command that never ran because a gate blocked it.
- `LoopAudit.verdict` (method) `modules/loop_audit.py:189` `def verdict(self, verdict)` -- Record the independent goal-evaluation verdict.
- `LoopAudit.run_end` (method) `modules/loop_audit.py:203` `def run_end(self, status, rounds, verdict, error)` -- Record the loop lifecycle end with the final engine status.
- `LoopAudit.record_command` (method) `modules/loop_audit.py:216` `def record_command(self, command, output, duration, ok, task_id)` -- Record one executed command with its trigger context.
- `start` (function) `modules/loop_audit.py:320` `def start(task_id)` -- Create and register the audit for one task.
- `audit_for` (function) `modules/loop_audit.py:338` `def audit_for(task_id)` -- Return the active audit for one task, or None when not started.
- `stop` (function) `modules/loop_audit.py:349` `def stop(task_id)` -- Forget the registered audit for one task.
- `blocked_verbs` (function) `modules/loop_audit.py:360` `def blocked_verbs(task_id, min_count)` -- Return verbs a gate blocked at least ``min_count`` times in one run.
- `guard_rows` (function) `modules/loop_audit.py:392` `def guard_rows(task_id)` -- Return guard decisions recorded for one task.
- `activity_rows` (function) `modules/loop_audit.py:397` `def activity_rows(task_id)` -- Return engine activity rows for one task.
- `timeline` (function) `modules/loop_audit.py:447` `def timeline(task_id, audit)` -- Merge audit, guard and lifecycle rows into one timeline.
- `render` (function) `modules/loop_audit.py:537` `def render(task_id, limit, audit)` -- Render the merged campaign timeline for one task.
- `list_runs` (function) `modules/loop_audit.py:558` `def list_runs(limit)` -- Summarize every recorded loop run, newest first.
- `render_summary` (function) `modules/loop_audit.py:595` `def render_summary(summaries)` -- Render ``list_runs`` summaries as an operator table.

## modules/loop_guardrails.py
Depends on: `modules/__init__.py`
Imported by: `modules/chain_runner.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/loop/worker_memory.py`, `tests/test_loop_guardrails.py`, `tests/test_orchestrator_pacing.py`, `tests/test_pacing.py`, `tests/test_repeat_shapes.py`, `tests/test_writeback_hygiene.py`
- `RepeatDetector.__init__` (method) `modules/loop_guardrails.py:117` `def __init__(self, window)`
- `RepeatDetector.record` (method) `modules/loop_guardrails.py:125` `def record(self, command)` -- Add one executed command; returns True when the window fills.
- `RepeatDetector.stuck` (method) `modules/loop_guardrails.py:182` `def stuck(self)` -- True when the loop is visibly not progressing.
- `RepeatDetector.describe` (method) `modules/loop_guardrails.py:200` `def describe(self)` -- Human sentence of the stuck shape for activity lines.
- `RepeatDetector.oscillation_pair` (method) `modules/loop_guardrails.py:222` `def oscillation_pair(self)` -- Return the detected alternating pair, ('', '') when none.
- `RepeatDetector.cycle` (method) `modules/loop_guardrails.py:226` `def cycle(self)` -- Return the detected repeating block, empty when none.
- `RepeatDetector.last_commands` (method) `modules/loop_guardrails.py:230` `def last_commands(self)` -- Snapshot of the recent command window (oldest first).
- `RepeatDetector.reset` (method) `modules/loop_guardrails.py:234` `def reset(self)` -- Clear the window (operator intervention acknowledged).
- `EdrPacer.__init__` (method) `modules/loop_guardrails.py:258` `def __init__(self, duration_threshold)` -- Configure the pacer.
- `EdrPacer.parse_windows` (method) `modules/loop_guardrails.py:304` `def parse_windows(raw)` -- Parse ``HH:MM-HH:MM`` window strings into minute tuples.
- `EdrPacer.from_config` (method) `modules/loop_guardrails.py:326` `def from_config(cls)` -- Build a pacer from the orchestrator pacing configuration.
- `EdrPacer.observe` (method) `modules/loop_guardrails.py:357` `def observe(self, command, duration_sec, output)` -- Feed one executed step and update the telemetry estimate.
- `EdrPacer.decay` (method) `modules/loop_guardrails.py:379` `def decay(self, factor)` -- Cool the estimate down (call once per completed step).
- `EdrPacer.level` (method) `modules/loop_guardrails.py:385` `def level(self)` -- Current pacing level: 0 calm, 1 cautious, 2 stealth.
- `EdrPacer.signal` (method) `modules/loop_guardrails.py:395` `def signal(self)` -- Human-readable reason for the current level (may be empty).
- `EdrPacer.in_sleeper_window` (method) `modules/loop_guardrails.py:426` `def in_sleeper_window(self, now)` -- True when local time falls inside a configured quiet window.
- `EdrPacer.windows_delay` (method) `modules/loop_guardrails.py:432` `def windows_delay(windows, now)` -- Static quiet-window delay for callers without a pacer instance.
- `EdrPacer.sleeper_delay` (method) `modules/loop_guardrails.py:459` `def sleeper_delay(self, now)` -- Recommended sleep because of a quiet window (0 when outside).
- `EdrPacer.inter_step_delay` (method) `modules/loop_guardrails.py:472` `def inter_step_delay(self)` -- Recommended sleep before the next step at the current level.
- `EdrPacer.quieten` (method) `modules/loop_guardrails.py:489` `def quieten(self, command)` -- Return a quieter variant of the command at the current level.
- `EdrPacer.describe` (method) `modules/loop_guardrails.py:504` `def describe(self)` -- Return a snapshot of the pacer state for admin surfaces.
- `TargetLimiter.__init__` (method) `modules/loop_guardrails.py:527` `def __init__(self, max_concurrent)`
- `TargetLimiter.max_concurrent` (method) `modules/loop_guardrails.py:534` `def max_concurrent(self)` -- Configured upper bound of simultaneous targets.
- `TargetLimiter.active_targets` (method) `modules/loop_guardrails.py:539` `def active_targets(self)` -- How many distinct targets currently hold a slot.
- `TargetLimiter.slot` (method) `modules/loop_guardrails.py:545` `def slot(self, target)` -- Hold one of at most ``max_concurrent`` target slots.
- `FactVectorStore.__init__` (method) `modules/loop_guardrails.py:597` `def __init__(self, path, max_facts)`
- `FactVectorStore.path` (method) `modules/loop_guardrails.py:605` `def path(self)` -- Backing file path.
- `FactVectorStore.add` (method) `modules/loop_guardrails.py:626` `def add(self, text, meta)` -- Embed and store one fact; returns False for duplicates.
- `FactVectorStore.search` (method) `modules/loop_guardrails.py:660` `def search(self, query, k)` -- Return the ``k`` facts most similar to the query.
- `FactVectorStore.search_block` (method) `modules/loop_guardrails.py:690` `def search_block(self, query, k, max_chars)` -- Render retrieved facts as a prompt-ready block (may be empty).
- `FactVectorStore.clear` (method) `modules/loop_guardrails.py:699` `def clear(self)` -- Drop every fact (manual reset path).
- `FactVectorStore.save` (method) `modules/loop_guardrails.py:705` `def save(self)` -- Persist atomically; I/O errors never surface to the loop.
- `listing_forbidden` (function) `modules/loop_guardrails.py:759` `def listing_forbidden(command)` -- Return the listing veto reason, empty when the command may run.
- `ListingNoiseDetector.observe` (method) `modules/loop_guardrails.py:798` `def observe(self, command, output)` -- Return True when the step is a pure directory listing dump.

## modules/loop_manager.py
Depends on: `modules/loop_limits.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/loops.py`, `tests/test_beacon_menu.py`, `tests/test_loop_manager.py`
- `LoopValidationError.__init__` (method) `modules/loop_manager.py:91` `def __init__(self, field, message)` -- Store the offending field alongside the human message.
- `validate_target` (function) `modules/loop_manager.py:101` `def validate_target(raw)` -- Return the canonical string form of a validated IP address target.
- `validate_beacon_target` (function) `modules/loop_manager.py:124` `def validate_beacon_target(raw)` -- Return the canonical string form of a validated beacon client id.
- `sanitize_goal` (function) `modules/loop_manager.py:146` `def sanitize_goal(raw)` -- Return a safe goal string accepted by the loop parser.
- `clamp_int` (function) `modules/loop_manager.py:173` `def clamp_int(raw, field, default, minimum, maximum)` -- Parse and clamp an integer knob to the supported range.
- `clamp_float` (function) `modules/loop_manager.py:198` `def clamp_float(raw, field, default, minimum, maximum)` -- Parse and clamp a float knob to the supported range.
- `validate_loop_id` (function) `modules/loop_manager.py:223` `def validate_loop_id(loop_id)` -- Validate a loop id and return its normalized hex form.
- `LoopManager.__init__` (method) `modules/loop_manager.py:366` `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` -- Create the manager and its persistence lock.
- `LoopManager.loops_dir` (method) `modules/loop_manager.py:388` `def loops_dir(self)` -- Return the root directory for loop workspaces.
- `LoopManager.start` (method) `modules/loop_manager.py:392` `def start(self, spec, operator)` -- Validate, spawn and register one autonomous loop.
- `LoopManager.list_loops` (method) `modules/loop_manager.py:594` `def list_loops(self)` -- Return every registry record with refreshed live status.
- `LoopManager.get_loop` (method) `modules/loop_manager.py:629` `def get_loop(self, loop_id)` -- Return one registry record by id.
- `LoopManager.read_log` (method) `modules/loop_manager.py:648` `def read_log(self, loop_id, offset)` -- Read one chunk of a loop's output log.
- `LoopManager.stop` (method) `modules/loop_manager.py:715` `def stop(self, loop_id)` -- Stop one running loop by terminating its process group.
- `LoopManager.summary` (method) `modules/loop_manager.py:780` `def summary(self)` -- Return an aggregate view of loop activity for the report.
- `default_manager` (function) `modules/loop_manager.py:898` `def default_manager()` -- Return the process-wide loop manager singleton.

## modules/loop_preflight.py
Depends on: `modules/__init__.py`
- `lab_state_for` (function) `modules/loop_preflight.py:38` `def lab_state_for(target, scenarios, running, existing, ip_lookup)` -- Map a target IP to its lab scenario and container state.
- `probe_tcp_detailed` (function) `modules/loop_preflight.py:83` `def probe_tcp_detailed(target, ports, timeout)` -- Probe TCP ports in parallel and classify the answers.
- `probe_tcp` (function) `modules/loop_preflight.py:125` `def probe_tcp(target, ports, timeout)` -- Probe TCP ports in parallel and return the open ones.
- `check_target` (function) `modules/loop_preflight.py:145` `def check_target(target, ports, connect_timeout, lab)` -- Decide whether a loop may be spent against this target.
- `recovery_hint` (function) `modules/loop_preflight.py:211` `def recovery_hint(outcome)` -- Return the operator-facing recovery line for a failed preflight.

## modules/loop_progress.py
Depends on: `core/safe_console.py`
Imported by: `cli/lazy_monitor.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`, `tests/test_loop_progress.py`
- `snapshot_from_overview` (function) `modules/loop_progress.py:99` `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)` -- Build a snapshot from a graph overview dict plus task record.
- `snap_to_states` (function) `modules/loop_progress.py:123` `def snap_to_states(snapshot)` -- Infer done/active/pending per chain stage from a snapshot.
- `sanitize_line` (function) `modules/loop_progress.py:151` `def sanitize_line(line, keep_ansi)` -- Strip ANSI codes and carriage returns from a transcript line.
- `LoopProgress.live_mode` (method) `modules/loop_progress.py:195` `def live_mode(self)` -- True only when the sink supports a real live region.
- `LoopProgress.start` (method) `modules/loop_progress.py:202` `def start(self)` -- Open the Live display, or print the header in line mode.
- `LoopProgress.stop` (method) `modules/loop_progress.py:229` `def stop(self)` -- Freeze the final panel on screen (both modes).
- `LoopProgress.refresh` (method) `modules/loop_progress.py:246` `def refresh(self, snapshot)` -- Re-render milestones from a fresh snapshot (thread-safe).
- `LoopProgress.emit` (method) `modules/loop_progress.py:268` `def emit(self, line)` -- Print a transcript line above the live panel, colors preserved.

## modules/loop_triggers.py
Depends on: `modules/__init__.py`, `modules/auto_registry.py`, `modules/lazy_heat.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `modules/world_model.py`
Imported by: `cli/commands/netattack.py`, `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `tests/test_loop_trigger_hints.py`, `tests/test_orchestrator_triggers.py`, `tests/test_trigger_policy.py`
- `hint_fingerprint` (function) `modules/loop_triggers.py:28` `def hint_fingerprint(row)` -- Return the evidence signature of one hot-CVE candidate.
- `prune_hint_fingerprints` (function) `modules/loop_triggers.py:60` `def prune_hint_fingerprints(store, now, ttl)` -- Return only the fresh fingerprints of a stored fingerprint map.
- `TriggerStore.__init__` (method) `modules/loop_triggers.py:91` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/loop_triggers.py:101` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.upsert_defaults` (method) `modules/loop_triggers.py:123` `def upsert_defaults(self, seeds)` -- Merge declarative seeds without duplicating or re-enabling.
- `TriggerStore.remove` (method) `modules/loop_triggers.py:165` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.set_enabled` (method) `modules/loop_triggers.py:176` `def set_enabled(self, trigger_id, enabled)` -- Flip one trigger's enabled flag in place.
- `TriggerStore.list` (method) `modules/loop_triggers.py:190` `def list(self)` -- Return all triggers.
- `TriggerStore.ensure_service_trigger` (method) `modules/loop_triggers.py:194` `def ensure_service_trigger(self)` -- Register the catalog trigger once so services fire the loop.
- `TriggerStore.ensure_cve_hot_trigger` (method) `modules/loop_triggers.py:207` `def ensure_cve_hot_trigger(self)` -- Register the hot-CVE trigger once so fresh intel fires the loop.
- `TriggerStore.ensure_ad_surface_trigger` (method) `modules/loop_triggers.py:220` `def ensure_ad_surface_trigger(self)` -- Register the AD-surface trigger once so Windows identity fires it.
- `TriggerStore.due` (method) `modules/loop_triggers.py:233` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.
- `read_signing_evidence` (function) `modules/loop_triggers.py:499` `def read_signing_evidence(store_dir)` -- Load operator-attested SMB signing evidence per host.

## modules/macos_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `MacOSPayloadFactory.__init__` (method) `modules/macos_payloads.py:111` `def __init__(self, config, output_dir)`
- `MacOSPayloadFactory.generate_app_bundle` (method) `modules/macos_payloads.py:137` `def generate_app_bundle(self)` -- Generate a macOS .app bundle with embedded reverse shell.
- `MacOSPayloadFactory.generate_launchd_persistence` (method) `modules/macos_payloads.py:212` `def generate_launchd_persistence(self)` -- Generate a LaunchDaemon or LaunchAgent plist for persistence.
- `MacOSPayloadFactory.generate_tcc_bypass` (method) `modules/macos_payloads.py:268` `def generate_tcc_bypass(self)` -- Generate a TCC bypass script targeting common permissions.
- `MacOSPayloadFactory.generate_osascript_dropper` (method) `modules/macos_payloads.py:314` `def generate_osascript_dropper(self)` -- Generate an AppleScript-based dropper that downloads and executes a stage.
- `MacOSPayloadFactory.generate_swift_stager` (method) `modules/macos_payloads.py:335` `def generate_swift_stager(self)` -- Generate a Swift reverse shell stager.
- `MacOSPayloadFactory.generate_persistence_scripts` (method) `modules/macos_payloads.py:398` `def generate_persistence_scripts(self)` -- Generate all available macOS persistence scripts.
- `MacOSPayloadFactory.generate_phishing_dialog` (method) `modules/macos_payloads.py:447` `def generate_phishing_dialog(self)` -- Generate an AppleScript credential phishing dialog.
- `MacOSPayloadFactory.generate_all` (method) `modules/macos_payloads.py:470` `def generate_all(self)` -- Generate all macOS payload artifacts.
- `MacOSPayloadFactory.list_tcc_services` (method) `modules/macos_payloads.py:517` `def list_tcc_services()` -- Return the list of known TCC service identifiers.
- `MacOSPayloadFactory.list_persistence_methods` (method) `modules/macos_payloads.py:522` `def list_persistence_methods()` -- Return the list of available persistence methods for macOS.

## modules/mario.py
- `check_collision` (function) `modules/mario.py:105` `def check_collision(x, y, layer)`

## modules/mcp_agent_bridge.py
Depends on: `core/logging.py`, `modules/llm_factory.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/agent_result.py`, `skills/mcp_tools/agent_status.py`, `skills/mcp_tools/list_agents.py`, `skills/mcp_tools/run_agent.py`, `skills/mcp_tools/subagent_run.py`
- `get_agent_status` (function) `modules/mcp_agent_bridge.py:163` `def get_agent_status(agent_id)` -- Public: returns current status dict for an agent.
- `get_agent_result` (function) `modules/mcp_agent_bridge.py:188` `def get_agent_result(agent_id)` -- Public: returns final result + full action log.
- `list_agents` (function) `modules/mcp_agent_bridge.py:211` `def list_agents(limit)` -- List recent agents sorted by start time.
- `GroqAgentWorker.__init__` (method) `modules/mcp_agent_bridge.py:235` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `GroqAgentWorker.run` (method) `modules/mcp_agent_bridge.py:264` `def run(self)`
- `OllamaReActWorker.__init__` (method) `modules/mcp_agent_bridge.py:368` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `OllamaReActWorker.run` (method) `modules/mcp_agent_bridge.py:389` `def run(self)`
- `AgentBridgeWorker.__init__` (method) `modules/mcp_agent_bridge.py:471` `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)`
- `AgentBridgeWorker.run` (method) `modules/mcp_agent_bridge.py:478` `def run(self)`
- `start_agent` (function) `modules/mcp_agent_bridge.py:508` `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` -- Start an agent in a background thread.
- `dummy_runner` (function) `modules/mcp_agent_bridge.py:531` `def dummy_runner(cmd)`

## modules/mediation/chain_mediator.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`, `tests/test_guardrails.py`
- `LlmPoolPort.complete` (method) `modules/mediation/chain_mediator.py:16` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt through the LLM pool.
- `LlmPoolPort.has_members` (method) `modules/mediation/chain_mediator.py:34` `def has_members(self)` -- Report whether any LLM member is configured.
- `ChainMediator.__init__` (method) `modules/mediation/chain_mediator.py:53` `def __init__(self)` -- Start with the default pool port.
- `ChainMediator.register_llm_port` (method) `modules/mediation/chain_mediator.py:57` `def register_llm_port(self, port)` -- Replace the completion port (injection point for tests/gyms).
- `ChainMediator.llm` (method) `modules/mediation/chain_mediator.py:65` `def llm(self)` -- Return the completion port for pipeline requests.
- `ChainMediator.describe` (method) `modules/mediation/chain_mediator.py:73` `def describe(self)` -- Return mediator metadata for diagnostics.

## modules/mediation/contracts.py
Depends on: `modules/mediation/hub.py`
Imported by: `modules/loop/worker_memory.py`, `modules/mediation/__init__.py`, `modules/mediation/engine_mediator.py`, `modules/mediation/hub.py`, `tests/test_engine_mediator.py`
- `MediationDomains.is_known` (method) `modules/mediation/contracts.py:24` `def is_known(cls, domain)` -- Check whether a domain key is registered in the default set.
- `ActivityLogPort.read` (method) `modules/mediation/contracts.py:45` `def read(self, limit)` -- Return the latest activity records oldest-first.
- `LlmCompletionPort.complete` (method) `modules/mediation/contracts.py:61` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt with the configured LLM pool.
- `LlmCompletionPort.has_members` (method) `modules/mediation/contracts.py:79` `def has_members(self)` -- Report whether any LLM member is configured.
- `MediatorContract.describe` (method) `modules/mediation/contracts.py:90` `def describe(self)` -- Return introspection metadata for diagnostics.
- `MediationHubContract.mediator_for` (method) `modules/mediation/contracts.py:99` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `resolve` (function) `modules/mediation/contracts.py:104` `def resolve(domain)` -- Return the default-hub mediator for a domain key.

## modules/mediation/engine_mediator.py
Depends on: `modules/autonomous_exploit_engine.py`, `modules/mediation/contracts.py`, `modules/reactive_engine.py`
Imported by: `modules/mediation/hub.py`, `tests/test_engine_mediator.py`
- `ExploitRetryPort.retry_with_credentials` (method) `modules/mediation/engine_mediator.py:35` `def retry_with_credentials(self, target, credentials)` -- Queue one retry attempt per captured credential pair.
- `ReactionPort.analyse` (method) `modules/mediation/engine_mediator.py:52` `def analyse(self, output, command, platform)` -- Analyse one command's output for next-action decisions.
- `EngineMediator.describe` (method) `modules/mediation/engine_mediator.py:71` `def describe(self)` -- Return introspection metadata for diagnostics.
- `EngineMediator.retry_with_credentials` (method) `modules/mediation/engine_mediator.py:79` `def retry_with_credentials(self, target, credentials)` -- Queue captured credentials into the exploit engine's retry loop.
- `EngineMediator.analyse` (method) `modules/mediation/engine_mediator.py:100` `def analyse(self, output, command, platform)` -- Run reactive-engine analysis over one step's output.

## modules/mediation/feedback_mediator.py
Depends on: `modules/lazy_orchestrator_feedback.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `FeedbackMediator.describe` (method) `modules/mediation/feedback_mediator.py:18` `def describe(self)` -- Return mediator metadata for diagnostics.
- `FeedbackMediator.order_steps` (method) `modules/mediation/feedback_mediator.py:22` `def order_steps(self, steps, stack)` -- Reorder worker steps with cross-task priors.

## modules/mediation/hub.py
Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/engine_mediator.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
Imported by: `modules/loop/worker_memory.py`, `modules/mediation/__init__.py`, `modules/mediation/contracts.py`, `tests/test_mediation.py`
- `MediationHub.__init__` (method) `modules/mediation/hub.py:22` `def __init__(self)` -- Start with an empty registry.
- `MediationHub.register` (method) `modules/mediation/hub.py:26` `def register(self, mediator)` -- Register a mediator under its declared domain.
- `MediationHub.mediator_for` (method) `modules/mediation/hub.py:35` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `MediationHub.snapshot` (method) `modules/mediation/hub.py:46` `def snapshot(self)` -- Return high-level metadata for every registered mediator.
- `default_hub` (function) `modules/mediation/hub.py:75` `def default_hub()` -- Return a fresh default-configured hub (test-safe, no singleton).
- `get_hub` (function) `modules/mediation/hub.py:80` `def get_hub()` -- Return the process-wide hub, building it on first use.

## modules/mediation/intel_mediator.py
Depends on: `modules/lazy_intel.py`, `modules/lazy_loop.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `IntelMediator.__init__` (method) `modules/mediation/intel_mediator.py:18` `def __init__(self)` -- Start with no registered activity-log factory.
- `IntelMediator.register_activity_log_factory` (method) `modules/mediation/intel_mediator.py:22` `def register_activity_log_factory(self, factory)` -- Register the loop-side activity log factory.
- `IntelMediator.describe` (method) `modules/mediation/intel_mediator.py:32` `def describe(self)` -- Return mediator metadata for diagnostics.
- `IntelMediator.activity_records` (method) `modules/mediation/intel_mediator.py:39` `def activity_records(self, task_id, limit)` -- Return loop activity records for one task.
- `IntelMediator.record_routing_decision` (method) `modules/mediation/intel_mediator.py:64` `def record_routing_decision(self, task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `IntelMediator.record_routing_outcome` (method) `modules/mediation/intel_mediator.py:97` `def record_routing_outcome(self, task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `IntelMediator.mask_configured` (method) `modules/mediation/intel_mediator.py:133` `def mask_configured(self, text)` -- Strip operator-configured secrets from LLM-bound context.
- `IntelMediator.stack_signature` (method) `modules/mediation/intel_mediator.py:149` `def stack_signature(self, assets)` -- Return the target stack fingerprint string.

## modules/mediation/telemetry_mediator.py
Depends on: `modules/loop_ai_bridge.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `TelemetryMediator.describe` (method) `modules/mediation/telemetry_mediator.py:19` `def describe(self)` -- Return mediator metadata for diagnostics.
- `TelemetryMediator.publish_event` (method) `modules/mediation/telemetry_mediator.py:23` `def publish_event(self, task_id, worker, kind, text, severity)` -- Publish one loop activity event to listeners.
- `TelemetryMediator.annotate_detection` (method) `modules/mediation/telemetry_mediator.py:43` `def annotate_detection(self, command)` -- Return the detection annotation for one command.
- `TelemetryMediator.assess_opsec` (method) `modules/mediation/telemetry_mediator.py:59` `def assess_opsec(self, command, rhost)` -- Return the pre-execution OPSEC gate assessment for one command.
- `TelemetryMediator.record_outcome_quality` (method) `modules/mediation/telemetry_mediator.py:77` `def record_outcome_quality(self, worker, intent_summary, facts, findings)` -- Record one intent's net yield as a decision-quality reward.
- `TelemetryMediator.tool_class_yields` (method) `modules/mediation/telemetry_mediator.py:93` `def tool_class_yields(self, summaries, phase)` -- Return learned decision-quality yields for candidate summaries.
- `TelemetryMediator.record_step` (method) `modules/mediation/telemetry_mediator.py:111` `def record_step(self, task_id, worker, command, output, detection_prob)` -- Record one executed step for learning stores.
- `TelemetryMediator.swan_available` (method) `modules/mediation/telemetry_mediator.py:128` `def swan_available(self)` -- Return True when the SWAN ensemble is ready.
- `TelemetryMediator.swan_consult` (method) `modules/mediation/telemetry_mediator.py:137` `def swan_consult(self, prompt, task_type, phase, timeout)` -- Consult the SWAN ensemble with one prompt.
- `TelemetryMediator.moe_route` (method) `modules/mediation/telemetry_mediator.py:162` `def moe_route(self, task_type)` -- Return the preferred MoE expert for a task type.
- `TelemetryMediator.rl_select` (method) `modules/mediation/telemetry_mediator.py:178` `def rl_select(self, task_type, phase, candidates, deterministic)` -- Return the RL-preferred candidate name.
- `TelemetryMediator.moe_record_outcome` (method) `modules/mediation/telemetry_mediator.py:203` `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record one MoE outcome for learning.
- `TelemetryMediator.rl_update` (method) `modules/mediation/telemetry_mediator.py:219` `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.

## modules/memory_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `MemoryCleaner.__init__` (method) `modules/memory_cleaner.py:61` `def __init__(self, config)`
- `MemoryCleaner.windows_memory_cleanup` (method) `modules/memory_cleaner.py:64` `def windows_memory_cleanup(self)` -- Generate Windows memory artifact cleanup commands.
- `MemoryCleaner.linux_memory_cleanup` (method) `modules/memory_cleaner.py:151` `def linux_memory_cleanup(self)` -- Generate Linux memory artifact cleanup commands.
- `MemoryCleaner.macos_memory_cleanup` (method) `modules/memory_cleaner.py:206` `def macos_memory_cleanup(self)` -- Generate macOS memory artifact cleanup commands.
- `MemoryCleaner.generate_on_exit_script` (method) `modules/memory_cleaner.py:255` `def generate_on_exit_script(self)` -- Generate an on-exit cleanup script for beacons.

## modules/memory_embeddings.py
Imported by: `modules/memory_store.py`, `tests/test_memory_semantics.py`
- `embed` (function) `modules/memory_embeddings.py:50` `def embed(text)` -- Map text to a normalised 512-float histogram BLOB.
- `cosine` (function) `modules/memory_embeddings.py:75` `def cosine(a, b)` -- Cosine similarity of two embedding BLOBs; legacy/partial input -> 0.0.
- `semantic_top_k` (function) `modules/memory_embeddings.py:85` `def semantic_top_k(query, candidates, top_k)` -- Rank candidate (id, embedding) pairs against the query.
- `as_floats` (function) `modules/memory_embeddings.py:109` `def as_floats(blob)` -- Decode a BLOB into a mutable float array (diagnostics/tests).


Next: [API_p18.md](API_p18.md)
