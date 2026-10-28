# API (page 16 of 25)
Previous: [API_p15.md](API_p15.md)

## modules/loop_manager.py
Imported by: `lazyc2.py`, `tests/test_loop_manager.py`
- `LoopValidationError.__init__` (method) `modules/loop_manager.py:90` `def __init__(self, field, message)` -- Store the offending field alongside the human message.
- `validate_target` (function) `modules/loop_manager.py:100` `def validate_target(raw)` -- Return the canonical string form of a validated IP address target.
- `sanitize_goal` (function) `modules/loop_manager.py:123` `def sanitize_goal(raw)` -- Return a safe goal string accepted by the loop parser.
- `clamp_int` (function) `modules/loop_manager.py:150` `def clamp_int(raw, field, default, minimum, maximum)` -- Parse and clamp an integer knob to the supported range.
- `clamp_float` (function) `modules/loop_manager.py:175` `def clamp_float(raw, field, default, minimum, maximum)` -- Parse and clamp a float knob to the supported range.
- `validate_loop_id` (function) `modules/loop_manager.py:200` `def validate_loop_id(loop_id)` -- Validate a loop id and return its normalized hex form.
- `LoopManager.__init__` (method) `modules/loop_manager.py:327` `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` -- Create the manager and its persistence lock.
- `LoopManager.loops_dir` (method) `modules/loop_manager.py:349` `def loops_dir(self)` -- Return the root directory for loop workspaces.
- `LoopManager.start` (method) `modules/loop_manager.py:353` `def start(self, spec, operator)` -- Validate, spawn and register one autonomous loop.
- `LoopManager.list_loops` (method) `modules/loop_manager.py:493` `def list_loops(self)` -- Return every registry record with refreshed live status.
- `LoopManager.get_loop` (method) `modules/loop_manager.py:528` `def get_loop(self, loop_id)` -- Return one registry record by id.
- `LoopManager.read_log` (method) `modules/loop_manager.py:547` `def read_log(self, loop_id, offset)` -- Read one chunk of a loop's output log.
- `LoopManager.stop` (method) `modules/loop_manager.py:614` `def stop(self, loop_id)` -- Stop one running loop by terminating its process group.
- `LoopManager.summary` (method) `modules/loop_manager.py:679` `def summary(self)` -- Return an aggregate view of loop activity for the report.

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
Imported by: `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `tests/test_loop_trigger_hints.py`, `tests/test_orchestrator_triggers.py`, `tests/test_trigger_policy.py`
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
- `TriggerStore.due` (method) `modules/loop_triggers.py:220` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.

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
Imported by: `modules/unified_bridge.py`, `skills/lazyown_mcp.py`
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
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `MediationDomains.is_known` (method) `modules/mediation/contracts.py:23` `def is_known(cls, domain)` -- Check whether a domain key is registered in the default set.
- `ActivityLogPort.read` (method) `modules/mediation/contracts.py:44` `def read(self, limit)` -- Return the latest activity records oldest-first.
- `LlmCompletionPort.complete` (method) `modules/mediation/contracts.py:60` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt with the configured LLM pool.
- `LlmCompletionPort.has_members` (method) `modules/mediation/contracts.py:78` `def has_members(self)` -- Report whether any LLM member is configured.
- `MediatorContract.describe` (method) `modules/mediation/contracts.py:89` `def describe(self)` -- Return introspection metadata for diagnostics.
- `MediationHubContract.mediator_for` (method) `modules/mediation/contracts.py:98` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `resolve` (function) `modules/mediation/contracts.py:103` `def resolve(domain)` -- Return the default-hub mediator for a domain key.

## modules/mediation/feedback_mediator.py
Depends on: `modules/lazy_orchestrator_feedback.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `FeedbackMediator.describe` (method) `modules/mediation/feedback_mediator.py:18` `def describe(self)` -- Return mediator metadata for diagnostics.
- `FeedbackMediator.order_steps` (method) `modules/mediation/feedback_mediator.py:22` `def order_steps(self, steps, stack)` -- Reorder worker steps with cross-task priors.

## modules/mediation/hub.py
Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/contracts.py`, `tests/test_mediation.py`
- `MediationHub.__init__` (method) `modules/mediation/hub.py:22` `def __init__(self)` -- Start with an empty registry.
- `MediationHub.register` (method) `modules/mediation/hub.py:26` `def register(self, mediator)` -- Register a mediator under its declared domain.
- `MediationHub.mediator_for` (method) `modules/mediation/hub.py:35` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `MediationHub.snapshot` (method) `modules/mediation/hub.py:46` `def snapshot(self)` -- Return high-level metadata for every registered mediator.
- `default_hub` (function) `modules/mediation/hub.py:73` `def default_hub()` -- Return a fresh default-configured hub (test-safe, no singleton).
- `get_hub` (function) `modules/mediation/hub.py:78` `def get_hub()` -- Return the process-wide hub, building it on first use.

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
- `TelemetryMediator.record_step` (method) `modules/mediation/telemetry_mediator.py:59` `def record_step(self, task_id, worker, command, output, detection_prob)` -- Record one executed step for learning stores.
- `TelemetryMediator.swan_available` (method) `modules/mediation/telemetry_mediator.py:76` `def swan_available(self)` -- Return True when the SWAN ensemble is ready.
- `TelemetryMediator.swan_consult` (method) `modules/mediation/telemetry_mediator.py:85` `def swan_consult(self, prompt, task_type, phase, timeout)` -- Consult the SWAN ensemble with one prompt.
- `TelemetryMediator.moe_route` (method) `modules/mediation/telemetry_mediator.py:110` `def moe_route(self, task_type)` -- Return the preferred MoE expert for a task type.
- `TelemetryMediator.rl_select` (method) `modules/mediation/telemetry_mediator.py:126` `def rl_select(self, task_type, phase, candidates, deterministic)` -- Return the RL-preferred candidate name.
- `TelemetryMediator.moe_record_outcome` (method) `modules/mediation/telemetry_mediator.py:151` `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record one MoE outcome for learning.
- `TelemetryMediator.rl_update` (method) `modules/mediation/telemetry_mediator.py:167` `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.

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

## modules/memory_store.py
Depends on: `modules/memory_embeddings.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`, `tests/test_memory_semantics.py`
- `StorageBackend.save` (method) `modules/memory_store.py:99` `def save(self, entry)`
- `StorageBackend.search` (method) `modules/memory_store.py:102` `def search(self, query, top_k)`
- `StorageBackend.by_host` (method) `modules/memory_store.py:105` `def by_host(self, host, top_k)`
- `StorageBackend.by_service` (method) `modules/memory_store.py:108` `def by_service(self, service, top_k)`
- `StorageBackend.all_entries` (method) `modules/memory_store.py:111` `def all_entries(self, limit)`
- `StorageBackend.close` (method) `modules/memory_store.py:114` `def close(self)`
- `SQLiteBackend.__init__` (method) `modules/memory_store.py:133` `def __init__(self, db_path)`
- `SQLiteBackend.save` (method) `modules/memory_store.py:148` `def save(self, entry)`
- `SQLiteBackend.search` (method) `modules/memory_store.py:180` `def search(self, query, top_k)`
- `SQLiteBackend.by_host` (method) `modules/memory_store.py:192` `def by_host(self, host, top_k)`
- `SQLiteBackend.by_service` (method) `modules/memory_store.py:203` `def by_service(self, service, top_k)`
- `SQLiteBackend.all_entries` (method) `modules/memory_store.py:215` `def all_entries(self, limit)`
- `SQLiteBackend.stats_raw` (method) `modules/memory_store.py:225` `def stats_raw(self)`
- `SQLiteBackend.close` (method) `modules/memory_store.py:232` `def close(self)`
- `MemoryStore.__init__` (method) `modules/memory_store.py:240` `def __init__(self, backend)`
- `MemoryStore.remember` (method) `modules/memory_store.py:243` `def remember(self, session_id, host, tool, command, output, findings, success)`
- `MemoryStore.recall` (method) `modules/memory_store.py:270` `def recall(self, query, top_k)`
- `MemoryStore.recall_by_host` (method) `modules/memory_store.py:273` `def recall_by_host(self, host, top_k)`
- `MemoryStore.recall_for_service` (method) `modules/memory_store.py:276` `def recall_for_service(self, service_name, top_k)`
- `MemoryStore.recall_hybrid` (method) `modules/memory_store.py:279` `def recall_hybrid(self, query, top_k)` -- FTS5 keyword hits first; semantic fallback when keywords miss.
- `MemoryStore.stats` (method) `modules/memory_store.py:292` `def stats(self)`
- `MemoryStore.export_finetuning_dataset` (method) `modules/memory_store.py:300` `def export_finetuning_dataset(self, path)`
- `VectorSQLiteBackend.save` (method) `modules/memory_store.py:320` `def save(self, entry)`
- `VectorSQLiteBackend.search_semantic` (method) `modules/memory_store.py:328` `def search_semantic(self, query, top_k)`
- `get_memory_store` (function) `modules/memory_store.py:339` `def get_memory_store()`
- `remember` (function) `modules/memory_store.py:348` `def remember(session_id, host, tool, command, output, findings, success)`
- `recall` (function) `modules/memory_store.py:360` `def recall(query, top_k)`
- `recall_hybrid` (function) `modules/memory_store.py:364` `def recall_hybrid(query, top_k)`

## modules/metasploitable_gym.py
Depends on: `core/logging.py`, `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`
Imported by: `cli/commands/redteam_gym.py`, `modules/ctf_capture.py`, `tests/test_metasploitable_gym.py`
- `load_index` (function) `modules/metasploitable_gym.py:42` `def load_index(path)` -- Load the gym index, returning an empty mapping on failure.
- `vulnerabilities` (function) `modules/metasploitable_gym.py:47` `def vulnerabilities(path)` -- Return every indexed vulnerability.
- `get` (function) `modules/metasploitable_gym.py:53` `def get(vuln_id, path)` -- Return one vulnerability by id, or None.
- `chain_for` (function) `modules/metasploitable_gym.py:62` `def chain_for(vuln_id, path)` -- Return the resolved chain for one vulnerability, or None.
- `exploit_for` (function) `modules/metasploitable_gym.py:72` `def exploit_for(vuln_id, path)` -- Return the exploit spec for one vulnerability, or None.
- `validate_matrix` (function) `modules/metasploitable_gym.py:82` `def validate_matrix(path)` -- Validate the index, exploit files and chains as one matrix.
- `summary` (function) `modules/metasploitable_gym.py:138` `def summary(path)` -- Return counts by severity and service for operators.
- `main` (function) `modules/metasploitable_gym.py:157` `def main()` -- CLI: list | validate | info | chain.

## modules/metasploitable_migrations.py
Depends on: `core/safe_exec.py`
Imported by: `modules/lab_runtime.py`, `tests/test_metasploitable_migrations.py`
- `build_migrations` (function) `modules/metasploitable_migrations.py:194` `def build_migrations(subnet)` -- Return the ordered migration list with the docker subnet applied.
- `apply_migrations` (function) `modules/metasploitable_migrations.py:354` `def apply_migrations(container, subnet)` -- Run every migration on the gym container, skipping applied ones.

## modules/metrics.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `lazyown.py`, `modules/c2_builder.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_metrics.py`
- `MetricsRegistry.__init__` (method) `modules/metrics.py:63` `def __init__(self)` -- Create an empty registry with its own lock.
- `MetricsRegistry.inc` (method) `modules/metrics.py:69` `def inc(self, name, labels, value)` -- Increment the named counter for the given labels.
- `MetricsRegistry.get` (method) `modules/metrics.py:87` `def get(self, name, labels)` -- Return the current value of a counter.
- `MetricsRegistry.prometheus_text` (method) `modules/metrics.py:107` `def prometheus_text(self)` -- Render every counter in Prometheus text exposition format.
- `MetricRecord.to_dict` (method) `modules/metrics.py:167` `def to_dict(self)` -- Return the record as a JSON-serialisable dictionary.
- `MetricsWriter.__init__` (method) `modules/metrics.py:189` `def __init__(self, path)` -- Initialise the writer.
- `MetricsWriter.path` (method) `modules/metrics.py:201` `def path(self)` -- Return the JSONL destination path.
- `MetricsWriter.append` (method) `modules/metrics.py:206` `def append(self, record)` -- Append a single record to disk.
- `MetricsAggregator.summarize` (method) `modules/metrics.py:254` `def summarize(cls, records, window_seconds, now_utc)` -- Compute aggregate statistics over the supplied records.
- `MetricsRecorder.__init__` (method) `modules/metrics.py:339` `def __init__(self, writer)` -- Initialise the recorder.
- `MetricsRecorder.path` (method) `modules/metrics.py:350` `def path(self)` -- Return the JSONL path used by the underlying writer.
- `MetricsRecorder.record` (method) `modules/metrics.py:355` `def record(self, command, args, duration_ms, success, exit_code, source)` -- Persist a single command-execution telemetry record.
- `MetricsRecorder.summarize` (method) `modules/metrics.py:416` `def summarize(self, window_seconds)` -- Return aggregate statistics over recorded events.
- `MetricsRecorder.tail` (method) `modules/metrics.py:430` `def tail(self, n)` -- Return the most recent *n* records, newest first.
- `get_recorder` (function) `modules/metrics.py:452` `def get_recorder()` -- Return the process-wide :class:`MetricsRecorder` singleton.
- `reset_recorder_for_tests` (function) `modules/metrics.py:466` `def reset_recorder_for_tests(writer)` -- Replace the module-level recorder with a fresh instance.

## modules/mfa_bypass.py
Imported by: `cli/commands/cicd.py`
- `MFABypassEngine.__init__` (method) `modules/mfa_bypass.py:128` `def __init__(self, sessions_dir)`
- `MFABypassEngine.enumerate_techniques` (method) `modules/mfa_bypass.py:133` `def enumerate_techniques(self, target)` -- Enumerate viable MFA bypass techniques for a given target.
- `MFABypassEngine.generate_phishing_templates` (method) `modules/mfa_bypass.py:153` `def generate_phishing_templates(self, target)` -- Generate phishing templates tailored for MFA bypass.
- `MFABypassEngine.mfa_conditional_access_scan` (method) `modules/mfa_bypass.py:223` `def mfa_conditional_access_scan(self, domain)` -- Scan for conditional access policy gaps.
- `MFABypassEngine.replay_oauth_token` (method) `modules/mfa_bypass.py:252` `def replay_oauth_token(self, access_token, refresh_token)` -- Test if an OAuth2 token is still valid and can be replayed.
- `MFABypassEngine.saml_golden_ticket_check` (method) `modules/mfa_bypass.py:278` `def saml_golden_ticket_check(self, adfs_server)` -- Check for ADFS token signing certificate exposure.
- `MFABypassEngine.export_report` (method) `modules/mfa_bypass.py:303` `def export_report(self)` -- Export MFA bypass results to a JSON report.

## modules/module_registry.py
Depends on: `core/logging.py`
Imported by: `cli/commands/marketplace.py`, `cli/commands/misc_migrated.py`, `cli/commands/module_manager.py`, `cli/commands/session_ops.py`, `skills/lazyown_mcp.py`, `tests/test_module_registry.py`
- `ModuleInfo.__init__` (method) `modules/module_registry.py:172` `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...`
- `ModuleInfo.to_dict` (method) `modules/module_registry.py:202` `def to_dict(self)`
- `ModuleRegistry.__init__` (method) `modules/module_registry.py:235` `def __init__(self, base_dir)`
- `ModuleRegistry.get_instance` (method) `modules/module_registry.py:241` `def get_instance(cls, base_dir)` -- Return the singleton registry instance.
- `ModuleRegistry.scan` (method) `modules/module_registry.py:247` `def scan(self)` -- Scan all module directories and return the full list.
- `ModuleRegistry.rescan` (method) `modules/module_registry.py:260` `def rescan(self)` -- Force a full rescan and return modules.
- `ModuleRegistry.get` (method) `modules/module_registry.py:269` `def get(self, name)` -- Get a module by name.
- `ModuleRegistry.search` (method) `modules/module_registry.py:275` `def search(self, query, module_type, category, enabled_only, include_deprecated)` -- Search indexed modules.
- `ModuleRegistry.deprecated_modules` (method) `modules/module_registry.py:315` `def deprecated_modules(self)` -- Return all deprecated modules.
- `ModuleRegistry.by_type` (method) `modules/module_registry.py:321` `def by_type(self, module_type)` -- Shorthand for ``search(module_type=module_type)``.
- `ModuleRegistry.summary` (method) `modules/module_registry.py:325` `def summary(self)` -- Return counts by module type.
- `format_module_table` (function) `modules/module_registry.py:542` `def format_module_table(modules, cols)` -- Format a list of modules as an aligned text table.
- `format_module_detail` (function) `modules/module_registry.py:589` `def format_module_detail(m)` -- Format a single module's full metadata.

## modules/moe_router.py
Depends on: `core/logging.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/lesson_ingestor.py`, `modules/loop_ai_bridge.py`, `skills/swan_agent.py`, `tests/integration_autonomous_flow.py`, `tests/test_moe_rl_swan.py`, `tests/test_moe_router_check_regression.py`
- `ExpertProfile.is_local` (method) `modules/moe_router.py:96` `def is_local(self)`
- `ExpertPerformance.update` (method) `modules/moe_router.py:115` `def update(self, reward, detection_prob)`
- `IExpertSelector.select` (method) `modules/moe_router.py:261` `def select(self, candidates, task_type, performance_store, deterministic)` -- Return the selected expert from candidates.
- `ExpertPerformanceStore.__init__` (method) `modules/moe_router.py:283` `def __init__(self, path)`
- `ExpertPerformanceStore.record` (method) `modules/moe_router.py:298` `def record(self, expert_id, task_type, reward, detection_prob)` -- Update performance for (expert, task_type) and persist.
- `ExpertPerformanceStore.get` (method) `modules/moe_router.py:316` `def get(self, expert_id, task_type)`
- `ExpertPerformanceStore.all_for_task` (method) `modules/moe_router.py:321` `def all_for_task(self, task_type)`
- `ExpertPerformanceStore.performance_bonus` (method) `modules/moe_router.py:325` `def performance_bonus(self, expert_id, task_type)` -- Return a bonus scalar in [-0.3, +0.5] based on EMA reward history.
- `SoftmaxSelector.__init__` (method) `modules/moe_router.py:377` `def __init__(self, temperature)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:381` `def temperature(self)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:385` `def temperature(self, value)`
- `SoftmaxSelector.select` (method) `modules/moe_router.py:388` `def select(self, candidates, task_type, performance_store, deterministic)`
- `ExpertAvailabilityChecker.__init__` (method) `modules/moe_router.py:443` `def __init__(self)`
- `ExpertAvailabilityChecker.is_available` (method) `modules/moe_router.py:447` `def is_available(self, expert, api_key)`
- `MoERouter.__init__` (method) `modules/moe_router.py:500` `def __init__(self, experts, selector, performance_store, api_key)`
- `MoERouter.route` (method) `modules/moe_router.py:515` `def route(self, task_type, goal, deterministic)` -- Return the single best expert for the given task_type.
- `MoERouter.ensemble` (method) `modules/moe_router.py:547` `def ensemble(self, task_type, goal, n)` -- Return up to *n* distinct experts for ensemble execution.
- `adjusted_weight` (function) `modules/moe_router.py:562` `def adjusted_weight(ep)`
- `MoERouter.record_outcome` (method) `modules/moe_router.py:575` `def record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record the outcome of an expert execution.
- `MoERouter.top_experts_for_task` (method) `modules/moe_router.py:589` `def top_experts_for_task(self, task_type, top_k)` -- Return (expert, adjusted_weight) sorted descending for diagnostics.
- `MoERouter.get_expert` (method) `modules/moe_router.py:605` `def get_expert(self, expert_id)` -- Return expert by ID, or None.
- `MoERouter.status_report` (method) `modules/moe_router.py:609` `def status_report(self)` -- Return a diagnostic snapshot of all experts and their weights.
- `get_router` (function) `modules/moe_router.py:684` `def get_router(api_key)` -- Return (or create) the module-level singleton MoERouter.

## modules/morse.py
- `reverse_morse_code` (function) `modules/morse.py:98` `def reverse_morse_code()` -- Build the reverse lookup table from Morse code to characters.
- `text_to_morse` (function) `modules/morse.py:109` `def text_to_morse(text, config)` -- Convert plain text to Morse code.
- `morse_to_text` (function) `modules/morse.py:130` `def morse_to_text(morse_code, config)` -- Convert Morse code back to plain text.
- `clear_screen` (function) `modules/morse.py:157` `def clear_screen(config)` -- Reset the terminal screen using a bounded subprocess call.
- `read_choice` (function) `modules/morse.py:171` `def read_choice(config)` -- Read and validate the menu choice from standard input.
- `run_driver` (function) `modules/morse.py:186` `def run_driver(config)` -- Run the interactive Morse code conversion loop.

## modules/mysql_hookandroot_lib.c
- `reverse_shell` (function) `modules/mysql_hookandroot_lib.c:74` `void reverse_shell(void)` -- fork & send a bash shell to the attacker before starting mysqld
- `execvp` (function) `modules/mysql_hookandroot_lib.c:128` `int execvp(const char* filename, char* const argv[])` -- execvp() hook

## modules/network_opsec.py
Imported by: `cli/commands/opsec_cleanup.py`
- `NetworkOpsecEngine.__init__` (method) `modules/network_opsec.py:83` `def __init__(self, config)`
- `NetworkOpsecEngine.configure_proxy_chain` (method) `modules/network_opsec.py:87` `def configure_proxy_chain(self, chain_type)` -- Configure a proxy chain for C2 communication.
- `NetworkOpsecEngine.check_canary_tokens` (method) `modules/network_opsec.py:131` `def check_canary_tokens(self)` -- Check if the target has canary token / deception technology.
- `NetworkOpsecEngine.analyze_traffic_with_canary_check` (method) `modules/network_opsec.py:179` `def analyze_traffic_with_canary_check(self, target_host, target_port)` -- Analyze whether target traffic is being intercepted or analyzed.
- `NetworkOpsecEngine.dns_over_https_config` (method) `modules/network_opsec.py:246` `def dns_over_https_config(self)` -- Generate DNS-over-HTTPS configuration for proxy and system.
- `NetworkOpsecEngine.source_port_randomize` (method) `modules/network_opsec.py:269` `def source_port_randomize(self)` -- Randomize source port for outbound connections.
- `NetworkOpsecEngine.connection_jitter_schedule` (method) `modules/network_opsec.py:294` `def connection_jitter_schedule(self, beacon_interval)` -- Generate a jitter schedule for beacon connections.
- `NetworkOpsecEngine.canary_detection_setup` (method) `modules/network_opsec.py:317` `def canary_detection_setup(self)` -- Set up canary detection for the engagement.
- `NetworkOpsecEngine.summary` (method) `modules/network_opsec.py:349` `def summary(self)`

## modules/nmap2csv.py
- `dottedquad_to_num` (function) `modules/nmap2csv.py:126` `def dottedquad_to_num(ip)` -- Convert decimal dotted quad string IP to long integer
- `num_to_dottedquad` (function) `modules/nmap2csv.py:133` `def num_to_dottedquad(n)` -- Convert long int IP to dotted quad string
- `unique_match_from_list` (function) `modules/nmap2csv.py:140` `def unique_match_from_list(list)` -- Check the list for a potential pattern match
- `extract_matching_pattern` (function) `modules/nmap2csv.py:156` `def extract_matching_pattern(regex, group_name, unfiltered_list)` -- Return the desired group_name from a list of matching patterns
- `Host.__init__` (method) `modules/nmap2csv.py:177` `def __init__(self, ip, fqdn)`
- `Host.add_port` (method) `modules/nmap2csv.py:188` `def add_port(self, port)`
- `Host.get_ip_num_format` (method) `modules/nmap2csv.py:192` `def get_ip_num_format(self)`
- `Host.get_ip_dotted_format` (method) `modules/nmap2csv.py:195` `def get_ip_dotted_format(self)`
- `Host.get_fqdn` (method) `modules/nmap2csv.py:198` `def get_fqdn(self)`
- `Host.get_rdns_record` (method) `modules/nmap2csv.py:201` `def get_rdns_record(self)`
- `Host.get_port_list` (method) `modules/nmap2csv.py:204` `def get_port_list(self)`
- `Host.get_port_number_list` (method) `modules/nmap2csv.py:207` `def get_port_number_list(self)`
- `Host.get_port_protocol_list` (method) `modules/nmap2csv.py:216` `def get_port_protocol_list(self)`
- `Host.get_port_service_list` (method) `modules/nmap2csv.py:225` `def get_port_service_list(self)`
- `Host.get_port_version_list` (method) `modules/nmap2csv.py:234` `def get_port_version_list(self)`
- `Host.get_port_script_list` (method) `modules/nmap2csv.py:243` `def get_port_script_list(self)`
- `Host.get_os` (method) `modules/nmap2csv.py:252` `def get_os(self)`
- `Host.get_mac_address` (method) `modules/nmap2csv.py:255` `def get_mac_address(self)`
- `Host.get_mac_address_vendor` (method) `modules/nmap2csv.py:258` `def get_mac_address_vendor(self)`
- `Host.get_network_distance` (method) `modules/nmap2csv.py:261` `def get_network_distance(self)`
- `Host.set_fqdn` (method) `modules/nmap2csv.py:265` `def set_fqdn(self, fqdn)`
- `Host.set_rdns_record` (method) `modules/nmap2csv.py:268` `def set_rdns_record(self, rdns_record)`
- `Host.set_os` (method) `modules/nmap2csv.py:271` `def set_os(self, os)`
- `Host.set_mac` (method) `modules/nmap2csv.py:274` `def set_mac(self, mac_address, mac_address_vendor)`
- `Host.set_network_distance` (method) `modules/nmap2csv.py:278` `def set_network_distance(self, network_distance)`
- `Port.__init__` (method) `modules/nmap2csv.py:283` `def __init__(self, number, protocol, service, version, script)`
- `Port.get_number` (method) `modules/nmap2csv.py:290` `def get_number(self)`
- `Port.get_protocol` (method) `modules/nmap2csv.py:293` `def get_protocol(self)`
- `Port.get_service` (method) `modules/nmap2csv.py:296` `def get_service(self)`
- `Port.get_version` (method) `modules/nmap2csv.py:299` `def get_version(self)`
- `Port.get_script` (method) `modules/nmap2csv.py:302` `def get_script(self)`
- `Port.set_service` (method) `modules/nmap2csv.py:305` `def set_service(self, service)`
- `Port.set_version` (method) `modules/nmap2csv.py:308` `def set_version(self, version)`
- `Port.set_script` (method) `modules/nmap2csv.py:311` `def set_script(self, script)`
- `split_grepable_match` (function) `modules/nmap2csv.py:315` `def split_grepable_match(raw_string)` -- Split the raw line to a neat Host object
- `parse` (function) `modules/nmap2csv.py:362` `def parse(fd)` -- Parse the data according to several regexes
- `parse_xml` (function) `modules/nmap2csv.py:492` `def parse_xml(xml_file)` -- Parse the XML file
- `is_format_valid` (function) `modules/nmap2csv.py:572` `def is_format_valid(fmt)` -- Check for the supplied custom output format
- `formatted_item` (function) `modules/nmap2csv.py:606` `def formatted_item(host, format_item)` -- return the attribute value related to the host
- `repeat_attributes` (function) `modules/nmap2csv.py:639` `def repeat_attributes(attribute_list)` -- repeat attribute lists to the maximum for the
- `generate_csv` (function) `modules/nmap2csv.py:653` `def generate_csv(fd, results, options)` -- Generate a plain ';' separated csv file with the desired or default attribute format
- `main` (function) `modules/nmap2csv.py:688` `def main()`

## modules/notify.py
Imported by: `modules/custom_tools.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `static/js/chart.min.js`, `tests/test_autonomous_ops.py`, `tests/test_lazy_loop.py`, `tests/test_security_codeql_batch.py`
- `severity_rank` (function) `modules/notify.py:31` `def severity_rank(severity, config)` -- Return the comparable order for a severity label.
- `mask_secrets` (function) `modules/notify.py:39` `def mask_secrets(text, config)` -- Replace known secret prefixes with a redaction marker.
- `url_allowed` (function) `modules/notify.py:57` `def url_allowed(url)` -- SSRF dial-guard for webhook delivery (LAZY parity).
- `post_url_validated` (function) `modules/notify.py:145` `def post_url_validated(url, data, timeout)` -- POST data to a webhook URL after SSRF validation, guarding redirects.
- `_GuardRedirect.redirect_request` (method) `modules/notify.py:159` `def redirect_request(self, req, fp, code, msg, headers, newurl)`
- `Notifier.__init__` (method) `modules/notify.py:207` `def __init__(self, config)` -- Initialize with shared notification constants.
- `Notifier.should_send` (method) `modules/notify.py:215` `def should_send(self, message, channel)` -- Apply event, severity, keyword and scope gates (LAZY parity).
- `Notifier.render` (method) `modules/notify.py:238` `def render(self, message)` -- Render masked Markdown text for a message.
- `Notifier.dispatch` (method) `modules/notify.py:244` `def dispatch(self, message, channels)` -- Fan out to eligible channels and journal deliveries.
- `Notifier.flush_digest` (method) `modules/notify.py:260` `def flush_digest(self, max_age_sec)` -- Emit one digest per channel when due (default 30m, LAZY parity).

## modules/nuclei_templates_sync.py
- `repo_root` (function) `modules/nuclei_templates_sync.py:39` `def repo_root()` -- Return the LazyOwn repository root derived from this file location.
- `canonical_dest` (function) `modules/nuclei_templates_sync.py:48` `def canonical_dest(subdir)` -- Return the canonical marketplace destination for a source.
- `run` (function) `modules/nuclei_templates_sync.py:60` `def run(argv, cwd)` -- Run a subprocess capturing output as text without raising.
- `ensure_git_available` (function) `modules/nuclei_templates_sync.py:73` `def ensure_git_available()` -- Abort with a clear message when the git binary is missing.
- `clone_templates` (function) `modules/nuclei_templates_sync.py:84` `def clone_templates(repo, staging)` -- Shallow-clone the template repository into the staging directory.
- `strip_git_traces` (function) `modules/nuclei_templates_sync.py:113` `def strip_git_traces(tree)` -- Remove every .git file or directory under the staged tree.
- `count_templates` (function) `modules/nuclei_templates_sync.py:132` `def count_templates(tree)` -- Count Nuclei template files under a directory tree.
- `replace_dest` (function) `modules/nuclei_templates_sync.py:144` `def replace_dest(src, dest, expected)` -- Atomically replace the destination with the staged tree contents.
- `same_remote` (function) `modules/nuclei_templates_sync.py:168` `def same_remote(path, repo)` -- Check whether an existing clone points at the expected remote.
- `normalize` (function) `modules/nuclei_templates_sync.py:179` `def normalize(url)`
- `refresh_existing_clone` (function) `modules/nuclei_templates_sync.py:188` `def refresh_existing_clone(path, repo)` -- Fast-forward an existing clean clone of the same remote.
- `validate_subset` (function) `modules/nuclei_templates_sync.py:209` `def validate_subset(dest, subset)` -- Validate a template subset with the nuclei binary when available.
- `build_parser` (function) `modules/nuclei_templates_sync.py:238` `def build_parser()` -- Build the command line parser for the sync script.
- `sync` (function) `modules/nuclei_templates_sync.py:263` `def sync(name, repo, dest, refresh_existing, skip_validate)` -- Clone, clean, and install one template source.
- `resolve_plan` (function) `modules/nuclei_templates_sync.py:308` `def resolve_plan(args)` -- Resolve the requested sources into (name, repo, dest) work items.
- `main` (function) `modules/nuclei_templates_sync.py:337` `def main(argv)` -- Entry point for the template sync script.

## modules/obs_parser.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `modules/intelligence_engine.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/sinks/world_model.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`, `tests/test_daemon_loop.py`, `tests/test_phase1_data_gaps.py`
- `Observation.by_type` (method) `modules/obs_parser.py:83` `def by_type(self, ftype)`
- `Observation.has` (method) `modules/obs_parser.py:86` `def has(self, ftype)`
- `Extractor.extract` (method) `modules/obs_parser.py:99` `def extract(self, text, host)` -- Return all findings of this type found in *text*.
- `_ExtractorRegistry.__init__` (method) `modules/obs_parser.py:106` `def __init__(self)`
- `_ExtractorRegistry.register` (method) `modules/obs_parser.py:109` `def register(self, extractor)`
- `_ExtractorRegistry.run_all` (method) `modules/obs_parser.py:112` `def run_all(self, text, host)`
- `_IPExtractor.extract` (method) `modules/obs_parser.py:134` `def extract(self, text, host)`
- `_CredentialExtractor.extract` (method) `modules/obs_parser.py:175` `def extract(self, text, host)`
- `_ServiceVersionExtractor.extract` (method) `modules/obs_parser.py:198` `def extract(self, text, host)`
- `_PathExtractor.extract` (method) `modules/obs_parser.py:224` `def extract(self, text, host)`
- `_UsernameExtractor.extract` (method) `modules/obs_parser.py:245` `def extract(self, text, host)`
- `_HashExtractor.extract` (method) `modules/obs_parser.py:271` `def extract(self, text, host)`
- `_CVEExtractor.extract` (method) `modules/obs_parser.py:288` `def extract(self, text, host)`
- `_DomainExtractor.extract` (method) `modules/obs_parser.py:305` `def extract(self, text, host)`
- `_EmailExtractor.extract` (method) `modules/obs_parser.py:323` `def extract(self, text, host)`
- `_ErrorExtractor.extract` (method) `modules/obs_parser.py:345` `def extract(self, text, host)`
- `_CloudIdentityExtractor.extract` (method) `modules/obs_parser.py:367` `def extract(self, text, host)`
- `_SuccessDetector.is_success` (method) `modules/obs_parser.py:407` `def is_success(self, text)`
- `ObsParser.__init__` (method) `modules/obs_parser.py:431` `def __init__(self)`
- `ObsParser.register` (method) `modules/obs_parser.py:450` `def register(self, extractor)` -- Register an additional Extractor (Open/Closed extension point).
- `ObsParser.parse` (method) `modules/obs_parser.py:454` `def parse(self, output, host, tool)` -- Parse *output* and return an Observation.
- `get_parser` (function) `modules/obs_parser.py:500` `def get_parser()` -- Return (or create) the module-level singleton ObsParser.
- `parse` (function) `modules/obs_parser.py:508` `def parse(output, host, tool)` -- Module-level convenience wrapper.

## modules/operation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/apt_playbooks.py`, `modules/obs_parser.py`, `modules/playbook_engine.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`
- `Operation.to_dict` (method) `modules/operation.py:98` `def to_dict(self)`
- `Operation.from_dict` (method) `modules/operation.py:116` `def from_dict(cls, d)`
- `Operation.save` (method) `modules/operation.py:134` `def save(self)`
- `Operation.log_event` (method) `modules/operation.py:143` `def log_event(self, step_index, step_name, status, summary, findings_count, error)`
- `Operation.record_facts` (method) `modules/operation.py:164` `def record_facts(self, findings)`
- `OperationManager.__init__` (method) `modules/operation.py:183` `def __init__(self)`
- `OperationManager.list` (method) `modules/operation.py:187` `def list(self)` -- List all persisted operations.
- `OperationManager.get` (method) `modules/operation.py:199` `def get(self, op_id)`
- `OperationManager.create` (method) `modules/operation.py:206` `def create(self, name, target, apt_name, description)` -- Create a new planned operation.
- `OperationManager.plan_from_apt` (method) `modules/operation.py:225` `def plan_from_apt(self, op, playbook_yaml_path)` -- Populate steps from an APT playbook YAML (or fall back to a derived MITRE playbook).
- `OperationManager.start` (method) `modules/operation.py:287` `def start(self, op_id, executor)` -- Start or resume a planned operation.
- `OperationManager.pause` (method) `modules/operation.py:369` `def pause(self, op_id)`
- `OperationManager.resume` (method) `modules/operation.py:378` `def resume(self, op_id, executor)`
- `OperationManager.stop` (method) `modules/operation.py:386` `def stop(self, op_id)`
- `OperationManager.status` (method) `modules/operation.py:396` `def status(self, op_id)` -- Return a structured status dict for an operation.
- `OperationManager.timeline` (method) `modules/operation.py:425` `def timeline(self, op_id)`
- `OperationManager.report` (method) `modules/operation.py:431` `def report(self, op_id)`
- `get_manager` (function) `modules/operation.py:471` `def get_manager()` -- Return a fresh :class:`OperationManager`.

## modules/operator_profiles.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `cli/commands/automation.py`
- `OperatorProfile.to_dict` (method) `modules/operator_profiles.py:57` `def to_dict(self)`
- `OperatorProfileManager.__init__` (method) `modules/operator_profiles.py:88` `def __init__(self)`
- `OperatorProfileManager.create_profile` (method) `modules/operator_profiles.py:192` `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` -- Create a new operator profile.
- `OperatorProfileManager.load_profile` (method) `modules/operator_profiles.py:260` `def load_profile(self, username)` -- Load an operator profile.
- `OperatorProfileManager.update_profile` (method) `modules/operator_profiles.py:276` `def update_profile(self, username)` -- Update fields on an existing profile.
- `OperatorProfileManager.delete_profile` (method) `modules/operator_profiles.py:289` `def delete_profile(self, username)` -- Delete an operator profile and its directory.
- `OperatorProfileManager.list_profiles` (method) `modules/operator_profiles.py:300` `def list_profiles(self)` -- Return all operator profiles.
- `OperatorProfileManager.touch_activity` (method) `modules/operator_profiles.py:312` `def touch_activity(self, username)` -- Update last_active timestamp.
- `OperatorProfileManager.set_attribute` (method) `modules/operator_profiles.py:319` `def set_attribute(self, username, key, value)` -- Set a custom attribute on an operator profile.
- `OperatorProfileManager.get_attribute` (method) `modules/operator_profiles.py:328` `def get_attribute(self, username, key, default)` -- Get a custom attribute from an operator profile.
- `OperatorProfileManager.log_action` (method) `modules/operator_profiles.py:335` `def log_action(self, username, action, details)` -- Append an audited action to the operator's audit log.
- `OperatorProfileManager.effective_config` (method) `modules/operator_profiles.py:360` `def effective_config(self, username)` -- Merge team baseline (payload.json) with per-operator overrides.
- `get_operator_profile_manager` (function) `modules/operator_profiles.py:398` `def get_operator_profile_manager()` -- Return the singleton :class:`OperatorProfileManager`.

## modules/opsec_scorer.py
Depends on: `cli/commands/enum.py`, `core/config.py`, `core/logging.py`, `modules/db.py`, `modules/killchain.py`
Imported by: `cli/commands/opsec_cleanup.py`, `cli/commands/security.py`, `tests/test_opsec_scorer.py`, `tests/test_opsec_scorer_consolidated.py`
- `OpsecScore.to_dict` (method) `modules/opsec_scorer.py:288` `def to_dict(self)` -- Return the score serialized as a plain dictionary.
- `OpsecScorer.__init__` (method) `modules/opsec_scorer.py:343` `def __init__(self, payload, world_model)`
- `OpsecScorer.evasion_active` (method) `modules/opsec_scorer.py:352` `def evasion_active(self)`
- `OpsecScorer.traffic_morphing_active` (method) `modules/opsec_scorer.py:357` `def traffic_morphing_active(self)`
- `OpsecScorer.score` (method) `modules/opsec_scorer.py:365` `def score(self, command, rhost, phase_override)` -- Score an OPSEC risk for ``command`` against ``rhost``.
- `OpsecScorer.score_batch` (method) `modules/opsec_scorer.py:413` `def score_batch(self, commands, rhost)` -- Score multiple commands and return {command: OpsecScore}.
- `OpsecScorer.suggest_mitigations` (method) `modules/opsec_scorer.py:417` `def suggest_mitigations(self, command, detectable_by)` -- Return mitigation suggestions for a given command.
- `OpsecScorerV2.__init__` (method) `modules/opsec_scorer.py:617` `def __init__(self, context)`
- `OpsecScorerV2.assess` (method) `modules/opsec_scorer.py:622` `def assess(self, command, extra_context)` -- Assess OPSEC risk for a command in the current context.
- `OpsecScorerV2.should_allow` (method) `modules/opsec_scorer.py:696` `def should_allow(self, command)` -- Quick gating check - returns (allowed, score).
- `OpsecScorerV2.get_trend` (method) `modules/opsec_scorer.py:709` `def get_trend(self)` -- Analyze OPSEC risk trend over the session.
- `score_command` (function) `modules/opsec_scorer.py:811` `def score_command(command, payload, rhost)` -- Convenience function: score a single command without creating a scorer instance.

## modules/orchestrator_config.py
Depends on: `core/config.py`, `core/logging.py`, `modules/auto_registry.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyops.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/auto_registry.py`, `modules/defense_stages.py`, `modules/harness.py`, `modules/lazy_loop.py`, `modules/llm_orchestrator.py`, `modules/loop_ai_bridge.py`, `modules/trigger_policy.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_harness_mode.py`, `tests/test_lazy_orchestrator.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_yaml.py`, `tests/test_outcome_bus.py`
- `reload` (function) `modules/orchestrator_config.py:113` `def reload()` -- Invalidate every merged view after an external configuration change.
- `profiles` (function) `modules/orchestrator_config.py:232` `def profiles()` -- Return every resolved profile, including inherited values.
- `active_profile` (function) `modules/orchestrator_config.py:257` `def active_profile()` -- Return the profile selected by the payload, falling back safely.
- `profile_config` (function) `modules/orchestrator_config.py:269` `def profile_config(name)` -- Return one resolved profile by name, or the active profile.
- `set_profile` (function) `modules/orchestrator_config.py:276` `def set_profile(name)` -- Persist the active profile name.
- `set_harness` (function) `modules/orchestrator_config.py:300` `def set_harness(enabled)` -- Persist the deterministic-harness toggle in the payload.
- `limits` (function) `modules/orchestrator_config.py:332` `def limits()` -- Return resolved numeric limits for the active profile.
- `budget` (function) `modules/orchestrator_config.py:339` `def budget()` -- Return resolved budgets for the active profile.
- `chain_defaults` (function) `modules/orchestrator_config.py:346` `def chain_defaults()` -- Return the default chain and playbook for the active profile.
- `sinks` (function) `modules/orchestrator_config.py:355` `def sinks()` -- Return outcome sink toggles for the active profile plus payload overrides.
- `stages` (function) `modules/orchestrator_config.py:366` `def stages()` -- Merged stage view: enabled flag, label, firing condition and params.
- `stage_enabled` (function) `modules/orchestrator_config.py:396` `def stage_enabled(name)` -- Return whether one pipeline stage is enabled (unknown = enabled).
- `stage_params` (function) `modules/orchestrator_config.py:402` `def stage_params(name)` -- Return the resolved parameter mapping of one stage.
- `set_stage` (function) `modules/orchestrator_config.py:407` `def set_stage(name, enabled)` -- Persist the enabled flag of one stage.
- `effective_verbs` (function) `modules/orchestrator_config.py:432` `def effective_verbs()` -- Merged auto-verb view: built-ins plus operator overrides, additions and catalog.
- `verb_config` (function) `modules/orchestrator_config.py:524` `def verb_config(name)` -- Return the merged configuration of one auto verb, or None.
- `verb_enabled` (function) `modules/orchestrator_config.py:533` `def verb_enabled(name)` -- Return whether one auto verb may be proposed or executed.
- `upsert_verb` (function) `modules/orchestrator_config.py:539` `def upsert_verb(name)` -- Create or update one auto-verb override in the payload.
- `remove_verb` (function) `modules/orchestrator_config.py:596` `def remove_verb(name)` -- Remove a custom verb, or disable a built-in one.
- `reset` (function) `modules/orchestrator_config.py:617` `def reset()` -- Drop every orchestrator override (back to YAML defaults).
- `validate_config` (function) `modules/orchestrator_config.py:624` `def validate_config(data)` -- Validate one raw orchestration mapping.

## modules/osint_enrich.py
Imported by: `modules/finding_lifecycle.py`, `tests/test_finding_lifecycle.py`
- `cve_lookup` (function) `modules/osint_enrich.py:122` `def cve_lookup(cve_id, sessions_dir)` -- Assemble OSV advisory + KEV flag + EPSS score for one CVE id.
- `reverse_dns` (function) `modules/osint_enrich.py:161` `def reverse_dns(ip, sessions_dir)` -- Best-effort PTR hostname for an IP (HackerTarget, then DoH).
- `host_geo` (function) `modules/osint_enrich.py:183` `def host_geo(ip, sessions_dir)` -- Country/org/ISP for an IP via the keyless ip-api endpoint.
- `domain_exposure` (function) `modules/osint_enrich.py:198` `def domain_exposure(domain, sessions_dir)` -- Count public urlscan.io results for a domain (no key needed).
- `enrich_evidence` (function) `modules/osint_enrich.py:213` `def enrich_evidence(items, sessions_dir)` -- Append keyless OSINT verdicts to CVE mentions inside evidence items.


Next: [API_p17.md](API_p17.md)
