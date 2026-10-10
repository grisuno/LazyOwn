# API (page 16 of 20)
Previous: [API_p15.md](API_p15.md)

## skills/hermes-lazyown/constants.py
Depends on: `modules/killchain.py`
Imported by: `skills/hermes-lazyown/claudemd_rules.py`, `skills/hermes-lazyown/config_bridge.py`, `skills/hermes-lazyown/executor.py`, `skills/hermes-lazyown/hermes_sync.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/hermes-lazyown/output_compactor.py`
- `Paths.lazyown_dir` (method) `skills/hermes-lazyown/constants.py:106` `def lazyown_dir()` -- Return the LazyOwn project root directory.
- `Paths.payload_file` (method) `skills/hermes-lazyown/constants.py:115` `def payload_file()` -- Return the path to payload.json.
- `Paths.sessions_dir` (method) `skills/hermes-lazyown/constants.py:120` `def sessions_dir()` -- Return the path to the sessions directory.
- `Paths.scan_file` (method) `skills/hermes-lazyown/constants.py:125` `def scan_file(rhost)` -- Return the expected nmap scan file for a target.
- `Paths.vulns_file` (method) `skills/hermes-lazyown/constants.py:130` `def vulns_file(rhost)` -- Return the expected vulnerability scan file for a target.
- `Paths.world_model_file` (method) `skills/hermes-lazyown/constants.py:135` `def world_model_file()` -- Return the path to world_model.json.
- `Paths.objectives_file` (method) `skills/hermes-lazyown/constants.py:140` `def objectives_file()` -- Return the path to objectives.jsonl.
- `Paths.tasks_file` (method) `skills/hermes-lazyown/constants.py:145` `def tasks_file()` -- Return the path to tasks.json.
- `Paths.soul_file` (method) `skills/hermes-lazyown/constants.py:150` `def soul_file()` -- Return the path to soul.md.
- `Paths.claude_md_file` (method) `skills/hermes-lazyown/constants.py:155` `def claude_md_file()` -- Return the path to CLAUDE.md.

## skills/hermes-lazyown/executor.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `ExecutionResult.__init__` (method) `skills/hermes-lazyown/executor.py:24` `def __init__(self, stdout, stderr, returncode, timed_out, duration_ms)`
- `ExecutionResult.combined` (method) `skills/hermes-lazyown/executor.py:39` `def combined(self)` -- Return stdout and stderr combined.
- `ExecutionResult.success` (method) `skills/hermes-lazyown/executor.py:47` `def success(self)` -- Return True if the command exited cleanly and did not time out.
- `LazyOwnExecutor.__init__` (method) `skills/hermes-lazyown/executor.py:66` `def __init__(self, lazyown_dir, timeout)`
- `LazyOwnExecutor.execute` (method) `skills/hermes-lazyown/executor.py:77` `def execute(self, command, timeout)` -- Execute a single LazyOwn command string.
- `LazyOwnExecutor.execute_batch` (method) `skills/hermes-lazyown/executor.py:98` `def execute_batch(self, commands, timeout)` -- Execute multiple commands in a single LazyOwn session.

## skills/hermes-lazyown/hermes_sync.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `CheckpointSerializer.__init__` (method) `skills/hermes-lazyown/hermes_sync.py:33` `def __init__(self, sessions_dir)`
- `CheckpointSerializer.write` (method) `skills/hermes-lazyown/hermes_sync.py:37` `def write(self, state)` -- Write a checkpoint to disk.
- `CheckpointSerializer.read` (method) `skills/hermes-lazyown/hermes_sync.py:49` `def read(self)` -- Read the latest checkpoint, or None if absent / stale.
- `CheckpointSerializer.clear` (method) `skills/hermes-lazyown/hermes_sync.py:64` `def clear(self)` -- Remove the checkpoint file.
- `ObjectiveTodoSync.__init__` (method) `skills/hermes-lazyown/hermes_sync.py:82` `def __init__(self, objectives_path)`
- `ObjectiveTodoSync.pending_objectives` (method) `skills/hermes-lazyown/hermes_sync.py:85` `def pending_objectives(self)` -- Return all pending objectives from objectives.jsonl.
- `ObjectiveTodoSync.mark_done` (method) `skills/hermes-lazyown/hermes_sync.py:106` `def mark_done(self, objective_text)` -- Mark an objective as done by appending a completion record.
- `ObjectiveTodoSync.inject_objective` (method) `skills/hermes-lazyown/hermes_sync.py:127` `def inject_objective(self, text, priority, notes)` -- Inject a new objective into the LazyOwn queue.
- `DelegationPlanner.plan_for_service` (method) `skills/hermes-lazyown/hermes_sync.py:154` `def plan_for_service(self, service, port, rhost)` -- Return a list of delegation task descriptors for a discovered service.
- `DelegationPlanner.plan_for_credential` (method) `skills/hermes-lazyown/hermes_sync.py:233` `def plan_for_credential(self, cred_type, value, rhost)` -- Return delegation tasks triggered by a newly found credential.

## skills/hermes-lazyown/mcp_server.py
Depends on: `modules/backdoor/server.c`, `skills/hermes-lazyown/claudemd_rules.py`, `skills/hermes-lazyown/config_bridge.py`, `skills/hermes-lazyown/constants.py`, `skills/hermes-lazyown/executor.py`, `skills/hermes-lazyown/hermes_sync.py`, `skills/hermes-lazyown/output_compactor.py`
- `list_tools` (function) `skills/hermes-lazyown/mcp_server.py:329` `def list_tools()`
- `call_tool` (function) `skills/hermes-lazyown/mcp_server.py:334` `def call_tool(name, arguments)` -- Dispatch incoming tool calls to the appropriate handler.
- `main` (function) `skills/hermes-lazyown/mcp_server.py:751` `def main()`

## skills/hermes-lazyown/output_compactor.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `CompactionResult.__init__` (method) `skills/hermes-lazyown/output_compactor.py:20` `def __init__(self, compacted, original_lines, compacted_lines)`
- `CompactionResult.reduction_ratio` (method) `skills/hermes-lazyown/output_compactor.py:26` `def reduction_ratio(self)` -- Return the ratio of lines removed (0.0 to 1.0).
- `CompactionStrategy.compact` (method) `skills/hermes-lazyown/output_compactor.py:40` `def compact(self, raw_output, tool_name)` -- Compact *raw_output* and return a CompactionResult.
- `ReconCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:55` `def compact(self, raw_output, tool_name)`
- `EnumCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:93` `def compact(self, raw_output, tool_name)`
- `ExploitCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:124` `def compact(self, raw_output, tool_name)`
- `PrivescCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:151` `def compact(self, raw_output, tool_name)`
- `DefaultCompaction.__init__` (method) `skills/hermes-lazyown/output_compactor.py:165` `def __init__(self, max_lines)`
- `DefaultCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:168` `def compact(self, raw_output, tool_name)`
- `OutputCompactor.__init__` (method) `skills/hermes-lazyown/output_compactor.py:196` `def __init__(self, default_max_lines)`
- `OutputCompactor.compact` (method) `skills/hermes-lazyown/output_compactor.py:200` `def compact(self, raw_output, phase, tool_name)` -- Compact *raw_output* according to *phase*.

## skills/hive_mind.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_parquet_db.py`
Imported by: `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`, `skills/swan_agent.py`, `skills/tests/test_hive_mind.py`, `skills/unified_orchestrator.py`
- `IReadableMemory.recall` (method) `skills/hive_mind.py:149` `def recall(self, query, top_k)` -- Return top_k items matching query.
- `IWritableMemory.store` (method) `skills/hive_mind.py:157` `def store(self, content)` -- Persist content and return an opaque event_id.
- `ICommandRunner.run` (method) `skills/hive_mind.py:175` `def run(self, command, timeout)` -- Execute command within timeout seconds and return text output.
- `ICommandRunner.name` (method) `skills/hive_mind.py:180` `def name(self)` -- Human-readable identifier for this runner.
- `EpisodicStore.__init__` (method) `skills/hive_mind.py:215` `def __init__(self, db_path)`
- `EpisodicStore.store` (method) `skills/hive_mind.py:235` `def store(self, content, agent_id, role, event_type, meta, session_tag)` -- Insert a row into hive_events and return event_id.
- `EpisodicStore.recall` (method) `skills/hive_mind.py:274` `def recall(self, query, top_k, role, event_type)` -- Keyword search via FTS5.
- `EpisodicStore.stats` (method) `skills/hive_mind.py:322` `def stats(self)` -- Return row counts for status reporting.
- `EpisodicStore.forget` (method) `skills/hive_mind.py:329` `def forget(self, older_than_hours, topic)` -- Delete old or topic-matching rows.
- `SemanticStore.__init__` (method) `skills/hive_mind.py:358` `def __init__(self, chroma_dir, episodic_fallback)`
- `SemanticStore.available` (method) `skills/hive_mind.py:380` `def available(self)` -- True when ChromaDB is operational.
- `SemanticStore.store` (method) `skills/hive_mind.py:386` `def store(self, content, agent_id, role, event_type, meta, session_tag, event_id)` -- Add a document to ChromaDB.
- `SemanticStore.recall` (method) `skills/hive_mind.py:434` `def recall(self, query, top_k, where)` -- Vector similarity search.
- `SemanticStore.count` (method) `skills/hive_mind.py:477` `def count(self)` -- Return number of vectors stored.
- `LongtermStore.store` (method) `skills/hive_mind.py:515` `def store(self, content)` -- Parquet store is read-only from here.
- `LongtermStore.recall` (method) `skills/hive_mind.py:519` `def recall(self, query, top_k)` -- Keyword search across Parquet knowledge files.
- `LongtermStore.build_default_hive_memory` (method) `skills/hive_mind.py:558` `def build_default_hive_memory(db_path)` -- Factory that creates HiveMemory with the default three-layer backend.
- `HiveMemory.__init__` (method) `skills/hive_mind.py:582` `def __init__(self, stores, episodic, semantic, longterm)`
- `HiveMemory.store` (method) `skills/hive_mind.py:596` `def store(self, content, agent_id, role, event_type, meta, session_tag)` -- Store content in all writable layers.
- `HiveMemory.recall_episodic` (method) `skills/hive_mind.py:633` `def recall_episodic(self, query, top_k, role, event_type)` -- Keyword search across hive episodic memory.
- `HiveMemory.recall_semantic` (method) `skills/hive_mind.py:647` `def recall_semantic(self, query, top_k, where)` -- Vector similarity search in ChromaDB.
- `HiveMemory.recall_longterm` (method) `skills/hive_mind.py:660` `def recall_longterm(self, query, top_k)` -- Keyword search across Parquet knowledge files.
- `HiveMemory.recall` (method) `skills/hive_mind.py:668` `def recall(self, query, top_k)` -- Unified recall: semantic (ChromaDB) + episodic (SQLite) + longterm (Parquet).
- `HiveMemory.stats` (method) `skills/hive_mind.py:694` `def stats(self)` -- Return combined statistics from all layers.
- `HiveMemory.forget` (method) `skills/hive_mind.py:704` `def forget(self, older_than_hours, topic)` -- Prune old or topic-matched entries.
- `HiveBus.__init__` (method) `skills/hive_mind.py:736` `def __init__(self)`
- `HiveBus.publish` (method) `skills/hive_mind.py:740` `def publish(self, msg)` -- Deliver msg to recipient mailbox (and to "*" broadcast).
- `HiveBus.receive` (method) `skills/hive_mind.py:746` `def receive(self, agent_id, max_msgs)` -- Drain mailbox for agent_id (includes broadcast).
- `HiveBus.ack_broadcast` (method) `skills/hive_mind.py:754` `def ack_broadcast(self, agent_id, msg_id)` -- Mark a broadcast message as seen by agent_id (minimal bus — no-op).
- `HiveBus.pending_count` (method) `skills/hive_mind.py:758` `def pending_count(self, agent_id)` -- Count messages waiting for agent_id.
- `ConsensusProtocol.__init__` (method) `skills/hive_mind.py:943` `def __init__(self, risk_assessor)`
- `ConsensusProtocol.evaluate` (method) `skills/hive_mind.py:946` `def evaluate(self, role, goal)` -- Run the consensus vote for the given (role, goal) pair.
- `DroneAgent.__init__` (method) `skills/hive_mind.py:1091` `def __init__(self, drone_id, role, goal, backend, memory, bus, max_iterations, api_key, model, runner, on_state_change)`
- `DroneAgent.start` (method) `skills/hive_mind.py:1128` `def start(self)` -- Spawn the drone thread.
- `DroneAgent.join` (method) `skills/hive_mind.py:1137` `def join(self, timeout)` -- Block until the drone thread finishes.
- `QueenBrain.__init__` (method) `skills/hive_mind.py:1301` `def __init__(self, memory, bus, pool, consensus)`
- `QueenBrain.plan` (method) `skills/hive_mind.py:1313` `def plan(self, goal, n_drones)` -- Decompose a high-level goal into per-drone task specs.
- `QueenBrain.dispatch` (method) `skills/hive_mind.py:1332` `def dispatch(self, tasks, backend, api_key, max_iterations)` -- Spawn one drone per task in parallel.
- `QueenBrain.plan_and_dispatch` (method) `skills/hive_mind.py:1405` `def plan_and_dispatch(self, goal, n_drones, backend, api_key, max_iterations)` -- Convenience: plan + dispatch in one call.
- `QueenBrain.collect` (method) `skills/hive_mind.py:1417` `def collect(self, drone_ids, timeout, poll_interval)` -- Wait for all drones to finish (up to timeout seconds).
- `QueenBrain.synthesize` (method) `skills/hive_mind.py:1447` `def synthesize(self, drone_ids, original_goal)` -- Read hive memory results for these drones and produce a synthesis summary.
- `QueenBrain.read_bus` (method) `skills/hive_mind.py:1471` `def read_bus(self)` -- Drain queen's mailbox from drone result messages.
- `DroneStateStore.__init__` (method) `skills/hive_mind.py:1513` `def __init__(self, db_path)`
- `DroneStateStore.upsert` (method) `skills/hive_mind.py:1523` `def upsert(self, state)` -- Insert or replace a drone state record.
- `DroneStateStore.load_all` (method) `skills/hive_mind.py:1553` `def load_all(self, limit)` -- Load all persisted drone states ordered by most recently updated.
- `DroneStateStore.mark_interrupted` (method) `skills/hive_mind.py:1588` `def mark_interrupted(self)` -- Called on daemon startup: any drone that was queued/running when the process died is now in an unknown state.
- `DroneStateStore.load_interrupted` (method) `skills/hive_mind.py:1609` `def load_interrupted(self)` -- Return all drones currently in 'interrupted' state.
- `DroneStateStore.delete_older_than` (method) `skills/hive_mind.py:1643` `def delete_older_than(self, days)` -- Prune records older than N days.
- `DronePool.__init__` (method) `skills/hive_mind.py:1673` `def __init__(self, memory, bus, state_store)`
- `DronePool.recover_from_store` (method) `skills/hive_mind.py:1687` `def recover_from_store(self)` -- Load persisted drone states from a previous run.
- `DronePool.spawn` (method) `skills/hive_mind.py:1708` `def spawn(self, role, goal, backend, api_key, model, max_iterations, runner)` -- Create and start a DroneAgent.
- `DronePool.requeue_interrupted` (method) `skills/hive_mind.py:1741` `def requeue_interrupted(self, backend, api_key, max_iterations)` -- Re-spawn all drones previously marked 'interrupted'.
- `DronePool.get_state` (method) `skills/hive_mind.py:1767` `def get_state(self, drone_id)` -- Return the current state snapshot for a drone, or None if unknown.
- `DronePool.list_all` (method) `skills/hive_mind.py:1776` `def list_all(self, limit)` -- Return a sorted list of drone summary dicts (most recent first).
- `DronePool.active_count` (method) `skills/hive_mind.py:1801` `def active_count(self)` -- Return number of live drones currently in queued or running state.
- `HiveMind.__init__` (method) `skills/hive_mind.py:1818` `def __init__(self)`
- `HiveMind.spawn` (method) `skills/hive_mind.py:1829` `def spawn(self, goal, role, backend, api_key, max_iterations)` -- Spawn a single drone.
- `HiveMind.spawn_hive` (method) `skills/hive_mind.py:1846` `def spawn_hive(self, goal, n_drones, backend, api_key, max_iterations)` -- Queen plans and dispatches multiple drones in parallel.
- `HiveMind.status` (method) `skills/hive_mind.py:1863` `def status(self)` -- Return hive-wide status dict including historical drones from previous runs.
- `HiveMind.recall` (method) `skills/hive_mind.py:1878` `def recall(self, query, top_k)` -- Unified recall from all memory layers.
- `HiveMind.drone_result` (method) `skills/hive_mind.py:1882` `def drone_result(self, drone_id)` -- Return result dict for a specific drone.
- `HiveMind.collect_and_synthesize` (method) `skills/hive_mind.py:1896` `def collect_and_synthesize(self, drone_ids, goal)` -- Synthesize results from multiple drones.
- `HiveMind.forget` (method) `skills/hive_mind.py:1900` `def forget(self, older_than_hours, topic)` -- Prune hive memory.
- `HiveMind.get_hive` (method) `skills/hive_mind.py:1911` `def get_hive()` -- Return the process-wide HiveMind singleton, creating it if necessary.
- `HiveMind.mcp_hive_spawn` (method) `skills/hive_mind.py:1926` `def mcp_hive_spawn(goal, role, n_drones, backend, max_iterations, api_key)` -- Spawn one or more hive drones for a goal.
- `HiveMind.mcp_hive_status` (method) `skills/hive_mind.py:1976` `def mcp_hive_status()` -- Return full hive status: active drones, memory stats, queen mailbox.
- `HiveMind.mcp_hive_recall` (method) `skills/hive_mind.py:1981` `def mcp_hive_recall(query, top_k)` -- Semantic + episodic + longterm recall from hive memory.
- `HiveMind.mcp_hive_plan` (method) `skills/hive_mind.py:1995` `def mcp_hive_plan(goal, n_drones)` -- Queen generates task decomposition without spawning drones.
- `HiveMind.mcp_hive_result` (method) `skills/hive_mind.py:2004` `def mcp_hive_result(drone_id)` -- Get result from a specific drone.
- `HiveMind.mcp_hive_collect` (method) `skills/hive_mind.py:2010` `def mcp_hive_collect(drone_ids_csv, goal)` -- Wait for drones to finish and return synthesized result. drone_ids_csv: comma-separated drone IDs.
- `HiveMind.mcp_hive_forget` (method) `skills/hive_mind.py:2021` `def mcp_hive_forget(older_than_hours, topic)` -- Prune hive memory.
- `HiveMind.mcp_hive_recover` (method) `skills/hive_mind.py:2027` `def mcp_hive_recover(backend, api_key, max_iterations)` -- Re-queue all drones that were interrupted by a previous process crash/restart.

## skills/lazyown_automapper.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_mcp.py`
- `AutoMapper.__init__` (method) `skills/lazyown_automapper.py:341` `def __init__(self, lazyown_dir)`
- `AutoMapper.rescan` (method) `skills/lazyown_automapper.py:364` `def rescan(self)` -- Force a rescan of all source directories.
- `AutoMapper.mcp_tools` (method) `skills/lazyown_automapper.py:368` `def mcp_tools(self)` -- Return list of mcp types.Tool objects for all discovered extensions.
- `AutoMapper.dispatch` (method) `skills/lazyown_automapper.py:389` `def dispatch(self, name, arguments, config, run_command_fn)` -- Execute a dynamic tool.
- `AutoMapper.update_skills_md` (method) `skills/lazyown_automapper.py:524` `def update_skills_md(self, skills_md_path)` -- Append / replace the auto-discovered section in skills/lazyown.md.
- `AutoMapper.stats` (method) `skills/lazyown_automapper.py:571` `def stats(self)`
- `AutoMapper.list_specs` (method) `skills/lazyown_automapper.py:581` `def list_specs(self)` -- Return raw spec dicts (useful for debugging / reporting).

## skills/lazyown_campaign.py
Depends on: `core/logging.py`, `modules/lesson_ingestor.py`, `modules/logging_config.py`
Imported by: `skills/lazyown_mcp.py`
- `is_ip_in_scope` (function) `skills/lazyown_campaign.py:64` `def is_ip_in_scope(ip, scope)` -- Return True if *ip* belongs to any entry in *scope*.
- `Campaign.is_active` (method) `skills/lazyown_campaign.py:148` `def is_active(self)` -- Return True when the campaign has not been completed yet.
- `Campaign.to_dict` (method) `skills/lazyown_campaign.py:152` `def to_dict(self)` -- Serialise to a plain dict suitable for JSON persistence.
- `Campaign.from_dict` (method) `skills/lazyown_campaign.py:157` `def from_dict(cls, data)` -- Deserialise from a dict loaded out of JSON.
- `LessonLearned.to_dict` (method) `skills/lazyown_campaign.py:189` `def to_dict(self)`
- `EpisodeReflectionEngine.__init__` (method) `skills/lazyown_campaign.py:256` `def __init__(self, hive_memory)` -- Parameters hive_memory: Optional HiveMemory instance for semantic storage.
- `EpisodeReflectionEngine.reflect` (method) `skills/lazyown_campaign.py:268` `def reflect(self, campaign)` -- Extract lessons from *campaign* and persist them.
- `CampaignStore.__init__` (method) `skills/lazyown_campaign.py:382` `def __init__(self, campaign_file)`
- `CampaignStore.load` (method) `skills/lazyown_campaign.py:395` `def load(self)` -- Load the current campaign from disk.
- `CampaignStore.create` (method) `skills/lazyown_campaign.py:414` `def create(self, name, scope, notes)` -- Create and persist a brand-new campaign.
- `CampaignStore.complete` (method) `skills/lazyown_campaign.py:445` `def complete(self, notes, run_reflection, hive_memory)` -- Mark the active campaign as completed and optionally run reflection.
- `CampaignStore.update_phase` (method) `skills/lazyown_campaign.py:500` `def update_phase(self, host, phase)` -- Set (or update) the attack phase for *host*.
- `CampaignStore.add_milestone` (method) `skills/lazyown_campaign.py:516` `def add_milestone(self, host, milestone_type, notes)` -- Record a milestone achievement for *host*.
- `CampaignStore.add_to_scope` (method) `skills/lazyown_campaign.py:540` `def add_to_scope(self, ip_or_cidr)` -- Append *ip_or_cidr* to the campaign scope (idempotent).
- `CampaignStore.in_scope` (method) `skills/lazyown_campaign.py:559` `def in_scope(self, ip)` -- Return True if *ip* falls within the campaign scope.
- `CampaignStore.summary` (method) `skills/lazyown_campaign.py:566` `def summary(self)` -- Return a human-readable multi-line summary of the campaign.
- `CampaignStore.main` (method) `skills/lazyown_campaign.py:667` `def main(argv)`

## skills/lazyown_claudemd.py
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `ClaudeMdLoader.__init__` (method) `skills/lazyown_claudemd.py:32` `def __init__(self, cwd)`
- `ClaudeMdLoader.load` (method) `skills/lazyown_claudemd.py:35` `def load(self)` -- Return merged instructions string from all applicable levels.
- `ClaudeMdLoader.list_files` (method) `skills/lazyown_claudemd.py:90` `def list_files(self)` -- Return metadata for all CLAUDE.md files that exist.
- `ClaudeMdLoader.create_user_file` (method) `skills/lazyown_claudemd.py:115` `def create_user_file(self, content)` -- Create/overwrite ~/.lazyown/CLAUDE.md.
- `ClaudeMdLoader.create_project_file` (method) `skills/lazyown_claudemd.py:121` `def create_project_file(self, content, local)` -- Create CLAUDE.md (or CLAUDE.local.md) in cwd.
- `ClaudeMdLoader.add_rule` (method) `skills/lazyown_claudemd.py:127` `def add_rule(self, rule_name, content)` -- Add a named rule file to .lazyown/rules/.
- `ClaudeMdLoader.status_text` (method) `skills/lazyown_claudemd.py:135` `def status_text(self)`

## skills/lazyown_context.py
Imported by: `skills/lazyown_mcp.py`, `skills/lazyown_session.py`, `skills/tests/test_harness_e2e.py`
- `CompactionResult.summary` (method) `skills/lazyown_context.py:57` `def summary(self)`
- `ContextCompactor.__init__` (method) `skills/lazyown_context.py:72` `def __init__(self, budget_override, snip_threshold, collapse_threshold)`
- `ContextCompactor.apply_budget` (method) `skills/lazyown_context.py:84` `def apply_budget(self, content, tool_name)` -- Hard-cap output.
- `ContextCompactor.snip` (method) `skills/lazyown_context.py:99` `def snip(self, content)` -- Remove duplicate consecutive lines (log noise).
- `ContextCompactor.microcompact` (method) `skills/lazyown_context.py:120` `def microcompact(self, content)` -- Strip known low-signal patterns.
- `ContextCompactor.collapse` (method) `skills/lazyown_context.py:136` `def collapse(self, content, tool_name)` -- Replace repetitive sections with a structural summary.
- `ContextCompactor.auto_compact_session` (method) `skills/lazyown_context.py:159` `def auto_compact_session(entries)` -- Template-based session summary when full pipeline is insufficient. entries: list of {"type": str, "data": dict} from...
- `ContextCompactor.compact` (method) `skills/lazyown_context.py:203` `def compact(self, content, tool_name)` -- Apply all applicable layers in order.
- `ContextCompactor.compact_output` (method) `skills/lazyown_context.py:237` `def compact_output(content, tool_name)` -- Convenience wrapper: compact and return string.

## skills/lazyown_daemon.py
Depends on: `core/logging.py`, `modules/event_engine.py`, `modules/logging_config.py`, `modules/session_state.py`, `modules/timeline_narrator.py`, `skills/sessions_watcher.py`
- `process_new_rows` (method) `skills/lazyown_daemon.py:108` `def process_new_rows()`
- `file_watcher_loop` (function) `skills/lazyown_daemon.py:150` `def file_watcher_loop(queue)` -- Watch sessions/ for new/modified files and dispatch handlers.
- `_Handler.on_created` (method) `skills/lazyown_daemon.py:201` `def on_created(self, event)`
- `_Handler.on_modified` (method) `skills/lazyown_daemon.py:205` `def on_modified(self, event)`
- `file_event_consumer` (function) `skills/lazyown_daemon.py:223` `def file_event_consumer(queue)` -- Consume FILE events from the queue and call _dispatch in executor.
- `event_engine_loop` (function) `skills/lazyown_daemon.py:240` `def event_engine_loop()` -- Tail CSV, match rules, emit events — every ENGINE_INTERVAL_S seconds.
- `heartbeat_loop` (function) `skills/lazyown_daemon.py:280` `def heartbeat_loop()` -- Emit HEARTBEAT event and write daemon_status.json every 30 seconds.
- `toposwarm_keepalive_loop` (function) `skills/lazyown_daemon.py:332` `def toposwarm_keepalive_loop()` -- Keeps the TopoSwarm MCP server alive as a subprocess.
- `cmd_run` (function) `skills/lazyown_daemon.py:453` `def cmd_run()` -- Run in foreground.
- `cmd_start` (function) `skills/lazyown_daemon.py:462` `def cmd_start()` -- Fork, detach, and run in background.
- `cmd_stop` (function) `skills/lazyown_daemon.py:495` `def cmd_stop()` -- Send SIGTERM to the running daemon.
- `cmd_status` (function) `skills/lazyown_daemon.py:513` `def cmd_status()` -- Print status from daemon_status.json.

## skills/lazyown_facts.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `cli/commands/mcp_bridge.py`, `lazyc2.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`, `skills/tests/test_facts.py`
- `Config.default` (method) `skills/lazyown_facts.py:45` `def default(cls)`
- `HostFacts.highest_access` (method) `skills/lazyown_facts.py:145` `def highest_access(self)`
- `HostFacts.open_ports` (method) `skills/lazyown_facts.py:156` `def open_ports(self)`
- `HostFacts.services_by_name` (method) `skills/lazyown_facts.py:159` `def services_by_name(self, name)`
- `INmapXmlParser.parse` (method) `skills/lazyown_facts.py:169` `def parse(self, xml_path)`
- `ITextOutputParser.can_parse` (method) `skills/lazyown_facts.py:217` `def can_parse(self, filename, content)`
- `ITextOutputParser.parse` (method) `skills/lazyown_facts.py:220` `def parse(self, host, content, source_file)`
- `ITextOutputParser.parse_extended` (method) `skills/lazyown_facts.py:228` `def parse_extended(self, host, content, source_file, port)` -- Extended parse including vulnerabilities and web paths.
- `CrackMapExecParser.can_parse` (method) `skills/lazyown_facts.py:250` `def can_parse(self, filename, content)`
- `CrackMapExecParser.parse` (method) `skills/lazyown_facts.py:257` `def parse(self, host, content, source_file)`
- `Enum4linuxParser.can_parse` (method) `skills/lazyown_facts.py:301` `def can_parse(self, filename, content)`
- `Enum4linuxParser.parse` (method) `skills/lazyown_facts.py:304` `def parse(self, host, content, source_file)`
- `SecretsdumpParser.can_parse` (method) `skills/lazyown_facts.py:341` `def can_parse(self, filename, content)`
- `SecretsdumpParser.parse` (method) `skills/lazyown_facts.py:346` `def parse(self, host, content, source_file)`
- `LdapParser.can_parse` (method) `skills/lazyown_facts.py:374` `def can_parse(self, filename, content)`
- `LdapParser.parse` (method) `skills/lazyown_facts.py:377` `def parse(self, host, content, source_file)`
- `KerbruteParser.can_parse` (method) `skills/lazyown_facts.py:403` `def can_parse(self, filename, content)`
- `KerbruteParser.parse` (method) `skills/lazyown_facts.py:406` `def parse(self, host, content, source_file)`
- `RpcclientParser.can_parse` (method) `skills/lazyown_facts.py:424` `def can_parse(self, filename, content)`
- `RpcclientParser.parse` (method) `skills/lazyown_facts.py:427` `def parse(self, host, content, source_file)`
- `GobusterFfufParser.can_parse` (method) `skills/lazyown_facts.py:447` `def can_parse(self, filename, content)`
- `GobusterFfufParser.parse` (method) `skills/lazyown_facts.py:450` `def parse(self, host, content, source_file)`
- `GobusterFfufParser.parse_extended` (method) `skills/lazyown_facts.py:453` `def parse_extended(self, host, content, source_file, port)`
- `NiktoParser.can_parse` (method) `skills/lazyown_facts.py:502` `def can_parse(self, filename, content)`
- `NiktoParser.parse` (method) `skills/lazyown_facts.py:505` `def parse(self, host, content, source_file)`
- `NiktoParser.parse_extended` (method) `skills/lazyown_facts.py:508` `def parse_extended(self, host, content, source_file, port)`
- `NucleiParser.can_parse` (method) `skills/lazyown_facts.py:545` `def can_parse(self, filename, content)`
- `NucleiParser.parse` (method) `skills/lazyown_facts.py:548` `def parse(self, host, content, source_file)`
- `NucleiParser.parse_extended` (method) `skills/lazyown_facts.py:551` `def parse_extended(self, host, content, source_file, port)`
- `SslscanParser.can_parse` (method) `skills/lazyown_facts.py:581` `def can_parse(self, filename, content)`
- `SslscanParser.parse` (method) `skills/lazyown_facts.py:584` `def parse(self, host, content, source_file)`
- `SslscanParser.parse_extended` (method) `skills/lazyown_facts.py:587` `def parse_extended(self, host, content, source_file, port)`
- `GenericOutputParser.can_parse` (method) `skills/lazyown_facts.py:635` `def can_parse(self, filename, content)`
- `GenericOutputParser.parse` (method) `skills/lazyown_facts.py:638` `def parse(self, host, content, source_file)`
- `FactStore.__init__` (method) `skills/lazyown_facts.py:677` `def __init__(self, cfg)`
- `FactStore.save` (method) `skills/lazyown_facts.py:727` `def save(self)`
- `FactStore.ingest_xml` (method) `skills/lazyown_facts.py:791` `def ingest_xml(self, xml_path)` -- Parse one nmap XML file, merge results, return count of new facts.
- `FactStore.ingest_text` (method) `skills/lazyown_facts.py:803` `def ingest_text(self, txt_path, host_hint)` -- Parse one tool output file, merge credential/share/access facts.
- `FactStore.parse_all` (method) `skills/lazyown_facts.py:859` `def parse_all(self, target)` -- Scan sessions/ for all nmap XML and txt files.
- `FactStore.get_host` (method) `skills/lazyown_facts.py:890` `def get_host(self, host)`
- `FactStore.all_hosts` (method) `skills/lazyown_facts.py:893` `def all_hosts(self)`
- `FactStore.context_for_command` (method) `skills/lazyown_facts.py:896` `def context_for_command(self, host, category)` -- Return a dict of substitution parameters for a command in the given attack category.
- `FactStore.summary` (method) `skills/lazyown_facts.py:986` `def summary(self, host)` -- Return a human-readable summary of stored facts.
- `ToolDefinition.create_tool_file` (method) `skills/lazyown_facts.py:1025` `def create_tool_file(toolname, command, trigger, active, tools_dir)` -- Write a new pwntomate .tool JSON file.
- `ToolDefinition.main` (method) `skills/lazyown_facts.py:1074` `def main()`

## skills/lazyown_groq_agents.py
Depends on: `modules/atomic_enricher.py`, `modules/lazyown_bridge.py`, `modules/reactive_engine.py`, `modules/session_rag.py`, `modules/session_reader.py`, `modules/threat_model.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`
Imported by: `skills/hive_mind.py`, `skills/lazyown_mcp.py`, `skills/swan_agent.py`, `tests/test_bridge_catalog_filtered.py`
- `GroqAgentPool.__init__` (method) `skills/lazyown_groq_agents.py:702` `def __init__(self)`
- `GroqAgentPool.spawn` (method) `skills/lazyown_groq_agents.py:706` `def spawn(self, goal, tools_filter, api_key, backend, max_iterations, system_prompt, block)` -- Spawn a new agent.
- `GroqAgentPool.status` (method) `skills/lazyown_groq_agents.py:778` `def status(self, agent_id)`
- `GroqAgentPool.result` (method) `skills/lazyown_groq_agents.py:794` `def result(self, agent_id)`
- `GroqAgentPool.list_all` (method) `skills/lazyown_groq_agents.py:807` `def list_all(self, limit)`
- `GroqAgentPool.get_pool` (method) `skills/lazyown_groq_agents.py:829` `def get_pool()`
- `GroqAgentPool.spawn_agent` (method) `skills/lazyown_groq_agents.py:838` `def spawn_agent(goal, tools_filter, api_key, backend, max_iterations, block)` -- Spawn a new Groq/Ollama agent.
- `GroqAgentPool.agent_status` (method) `skills/lazyown_groq_agents.py:857` `def agent_status(agent_id)`
- `GroqAgentPool.agent_result` (method) `skills/lazyown_groq_agents.py:861` `def agent_result(agent_id)`
- `GroqAgentPool.list_agents` (method) `skills/lazyown_groq_agents.py:865` `def list_agents(limit)`
- `GroqAgentPool.main` (method) `skills/lazyown_groq_agents.py:872` `def main()`

## skills/lazyown_hooks.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `HookRegistry.__init__` (method) `skills/lazyown_hooks.py:47` `def __init__(self)`
- `HookRegistry.register` (method) `skills/lazyown_hooks.py:56` `def register(self, event, handler)`
- `HookRegistry.run` (method) `skills/lazyown_hooks.py:59` `def run(self, event, context)` -- Run all handlers for event, chaining modified contexts.
- `HookRegistry.metrics` (method) `skills/lazyown_hooks.py:79` `def metrics(self)` -- Return aggregate hook execution counts.
- `HookRegistry.sandbox_hook` (method) `skills/lazyown_hooks.py:101` `def sandbox_hook(context)` -- PRE_TOOL_USE: block catastrophic shell commands before permission evaluation.
- `HookRegistry.rate_limit_hook` (method) `skills/lazyown_hooks.py:116` `def rate_limit_hook(context, window, limit)` -- PRE_TOOL_USE: prevent rapid-fire C2 commands (>5 per 2s).
- `HookRegistry.audit_hook` (method) `skills/lazyown_hooks.py:139` `def audit_hook(context, audit_path)` -- AUDIT: append a one-line JSON record of every tool call to the audit log.
- `HookRegistry.timing_hook` (method) `skills/lazyown_hooks.py:161` `def timing_hook(context)` -- POST_TOOL_USE: annotate result with wall-clock execution time.
- `HookRegistry.start_timer_hook` (method) `skills/lazyown_hooks.py:176` `def start_timer_hook(context)` -- PRE_TOOL_USE: record start time for timing_hook.
- `HookRegistry.build_default_registry` (method) `skills/lazyown_hooks.py:187` `def build_default_registry(sessions_dir)` -- Create a HookRegistry with the built-in safety hooks wired up.
- `HookRegistry.get_registry` (method) `skills/lazyown_hooks.py:224` `def get_registry(sessions_dir)`

## skills/lazyown_llm.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_facts.py`, `skills/lazyown_mcp.py`, `skills/lazyown_objective.py`
Imported by: `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`
- `LLMTool.openai_schema` (method) `skills/lazyown_llm.py:79` `def openai_schema(self)`
- `LLMBridge.__init__` (method) `skills/lazyown_llm.py:104` `def __init__(self, backend, model, api_key)`
- `LLMBridge.register_tool` (method) `skills/lazyown_llm.py:118` `def register_tool(self, name, description, parameters, func)`
- `LLMBridge.ask` (method) `skills/lazyown_llm.py:127` `def ask(self, goal, context, max_iterations, system_prompt)`
- `LLMBridge.run_command` (method) `skills/lazyown_llm.py:346` `def run_command(command)` -- Execute a LazyOwn shell command and return its output.
- `LLMBridge.read_nmap` (method) `skills/lazyown_llm.py:352` `def read_nmap(target)` -- Read the nmap scan file for the given target IP.
- `LLMBridge.read_plan` (method) `skills/lazyown_llm.py:369` `def read_plan()` -- Read the current attack plan from sessions/plan.txt.
- `LLMBridge.read_facts` (method) `skills/lazyown_llm.py:376` `def read_facts(target)` -- Return FactStore structured facts for a target (or all targets).
- `LLMBridge.read_objectives` (method) `skills/lazyown_llm.py:389` `def read_objectives(limit)` -- List the next N pending attack objectives.
- `LLMBridge.build_bridge` (method) `skills/lazyown_llm.py:438` `def build_bridge(backend, model, api_key, with_default_tools)` -- Create a ready-to-use LLMBridge with optional default LazyOwn tools.
- `LLMBridge.llm_ask` (method) `skills/lazyown_llm.py:468` `def llm_ask(goal, context, backend, model, api_key, max_iterations, system_prompt, extra_tools)` -- Single-call entry point for lazyown_mcp.py.
- `LLMBridge.main` (method) `skills/lazyown_llm.py:493` `def main()`

## skills/lazyown_mcp.py
Depends on: `cli/command_chain.py`, `cli/graph_advisor.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/recommendation.py`, `cli/recommendation_signals.py`, `core/llm_budget.py`, `core/logging.py`, `core/payload_schema.py`, `modules/ai_exploit_chain.py`, `modules/atomic_enricher.py`, `modules/auto_pivot.py`, `modules/autonomous_exploit_engine.py`, `modules/backdoor/server.c`, `modules/collab_bp.py`, `modules/cve_matcher.py`, `modules/dashboard_engine.py`, `modules/db.py`, `modules/evasion_engine.py`, `modules/event_bus.py`, `modules/event_engine.py`, `modules/exploit_recommender.py`, `modules/exploitgym_gym.py`, `modules/integrations/misp_export.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazyown_bridge.py`, `modules/llm_client.py`, `modules/llm_evaluator.py`, `modules/mcp_agent_bridge.py`, `modules/memory_store.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/obs_parser.py`, `modules/pipeline_engine.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/recommender.py`, `modules/session_rag.py`, `modules/session_reader.py`, `modules/session_state.py`, `modules/threat_model.py`, `modules/timeline_narrator.py`, `modules/unified_dashboard.py`, `modules/world_model.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/daemon_control.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_claudemd.py`, `skills/lazyown_context.py`, `skills/lazyown_facts.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_hooks.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_helpers.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_permissions.py`, `skills/lazyown_policy.py`, `skills/lazyown_session.py`, `skills/swan_agent.py`
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_opencode.py`, `skills/tests/test_mcp_smoke.py`, `tests/test_boyscout_contracts.py`, `tests/test_mcp_improvements.py`, `tests/test_rea_mcp.py`
- `register_handler` (function) `skills/lazyown_mcp.py:620` `def register_handler(tool_name)` -- Decorator that registers an async handler for *tool_name*.
- `coerce_value` (function) `skills/lazyown_mcp.py:870` `def coerce_value(k, v)`
- `list_tools` (function) `skills/lazyown_mcp.py:1745` `def list_tools()`
- `substitute_playbook_target` (function) `skills/lazyown_mcp.py:5664` `def substitute_playbook_target(command, target)` -- Substitute the {target} token in a playbook step command.
- `call_tool` (function) `skills/lazyown_mcp.py:5682` `def call_tool(name, arguments)`
- `text` (function) `skills/lazyown_mcp.py:5696` `def text(content)`
- `main` (function) `skills/lazyown_mcp.py:11560` `def main()`

## skills/lazyown_mcp_helpers.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_mcp_improvements.py`
- `is_likely_credential` (function) `skills/lazyown_mcp_helpers.py:37` `def is_likely_credential(value)` -- Score whether a string is plausibly a real credential.
- `evidence_freshness` (function) `skills/lazyown_mcp_helpers.py:67` `def evidence_freshness(path, threshold_seconds, now)` -- Return age + stale flag for an evidence file.
- `parse_task_value` (function) `skills/lazyown_mcp_helpers.py:125` `def parse_task_value(title)` -- Extract the embedded JSON-ish payload from a task title.
- `TaskAudit.audit_tasks` (method) `skills/lazyown_mcp_helpers.py:165` `def audit_tasks(tasks, min_confidence)` -- Classify each task as keep/drop with a reason.
- `TaskAudit.find_credential_provenance` (method) `skills/lazyown_mcp_helpers.py:196` `def find_credential_provenance(value, sessions_dir, csv_name)` -- Locate where a credential was first observed.
- `TaskAudit.evidence_grep` (method) `skills/lazyown_mcp_helpers.py:297` `def evidence_grep(pattern, sessions_dir, scope, max_matches, max_file_bytes, case_insensitive)` -- Grep through session artefacts.
- `TaskAudit.collect_pwntomate_evidence` (method) `skills/lazyown_mcp_helpers.py:376` `def collect_pwntomate_evidence(rhost, sessions_dir)` -- List pwntomate output dirs for a target with per-dir freshness.
- `TaskAudit.build_target_context` (method) `skills/lazyown_mcp_helpers.py:414` `def build_target_context(host, port, sessions_dir, payload, world_model)` -- Aggregate everything known about (host, port) into one structure.
- `TaskAudit.preflight_command` (method) `skills/lazyown_mcp_helpers.py:575` `def preflight_command(command, payload, sessions_dir)` -- Pre-flight a LazyOwn command without executing it.
- `JobStore.__init__` (method) `skills/lazyown_mcp_helpers.py:689` `def __init__(self, max_jobs)`
- `JobStore.submit` (method) `skills/lazyown_mcp_helpers.py:694` `def submit(self, command, runner, timeout)` -- Start a runner(command, timeout) in a background thread.
- `JobStore.status` (method) `skills/lazyown_mcp_helpers.py:727` `def status(self, job_id)`
- `JobStore.list` (method) `skills/lazyown_mcp_helpers.py:732` `def list(self, limit)`
- `JobStore.take_snapshot` (method) `skills/lazyown_mcp_helpers.py:747` `def take_snapshot(sessions_dir, payload, world_model, tasks)` -- Capture a lightweight snapshot of the campaign state.
- `JobStore.diff_snapshot` (method) `skills/lazyown_mcp_helpers.py:792` `def diff_snapshot(sessions_dir, payload, world_model, tasks)` -- Return what changed since the last snapshot.
- `JobStore.needs_confirmation` (method) `skills/lazyown_mcp_helpers.py:875` `def needs_confirmation(tool_name, arguments)` -- Return True if tool should require an explicit confirm=True flag.

## skills/lazyown_mcp_opencode.py
Depends on: `modules/backdoor/server.c`, `skills/lazyown_mcp.py`
- `list_tools` (function) `skills/lazyown_mcp_opencode.py:57` `def list_tools()` -- Expose the curated subset under short names, keeping original schemas.
- `call_tool` (function) `skills/lazyown_mcp_opencode.py:76` `def call_tool(name, arguments)` -- Proxy the short name to the full LazyOwn MCP handler.
- `main` (function) `skills/lazyown_mcp_opencode.py:84` `def main()`

## skills/lazyown_objective.py
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`, `skills/tests/test_objectives.py`
- `Objective.sort_key` (method) `skills/lazyown_objective.py:116` `def sort_key(self)`
- `ObjectiveStore.__init__` (method) `skills/lazyown_objective.py:131` `def __init__(self, path)`
- `ObjectiveStore.cleanup` (method) `skills/lazyown_objective.py:163` `def cleanup(self)` -- Expire pending objectives whose TTL has passed.
- `ObjectiveStore.inject` (method) `skills/lazyown_objective.py:193` `def inject(self, text, priority, source, context, notes)`
- `ObjectiveStore.complete` (method) `skills/lazyown_objective.py:243` `def complete(self, obj_id, notes)`
- `ObjectiveStore.block` (method) `skills/lazyown_objective.py:246` `def block(self, obj_id, reason)`
- `ObjectiveStore.skip` (method) `skills/lazyown_objective.py:249` `def skip(self, obj_id, reason)`
- `ObjectiveStore.start` (method) `skills/lazyown_objective.py:252` `def start(self, obj_id)`
- `ObjectiveStore.next_pending` (method) `skills/lazyown_objective.py:255` `def next_pending(self)`
- `ObjectiveStore.list_pending` (method) `skills/lazyown_objective.py:261` `def list_pending(self, limit)`
- `ObjectiveStore.list_all` (method) `skills/lazyown_objective.py:265` `def list_all(self, status, limit)`
- `ObjectiveStore.summary` (method) `skills/lazyown_objective.py:271` `def summary(self)`
- `ObjectiveStore.read_soul` (method) `skills/lazyown_objective.py:291` `def read_soul()`
- `ObjectiveStore.write_soul` (method) `skills/lazyown_objective.py:297` `def write_soul(content)`
- `ObjectiveStore.current_plan` (method) `skills/lazyown_objective.py:301` `def current_plan()`
- `ObjectiveStore.full_context_for_claude` (method) `skills/lazyown_objective.py:307` `def full_context_for_claude(target)` -- Return a single dict with everything Claude Code needs to reason about the next objective:  soul + pending...
- `SoulUpdater.__init__` (method) `skills/lazyown_objective.py:350` `def __init__(self)`
- `SoulUpdater.update_phase` (method) `skills/lazyown_objective.py:388` `def update_phase(self, phase)` -- Update the `Phase:` line inside ## Current Focus.
- `SoulUpdater.update_target` (method) `skills/lazyown_objective.py:392` `def update_target(self, target)` -- Update the `Target:` line inside ## Current Focus.
- `SoulUpdater.update_os` (method) `skills/lazyown_objective.py:396` `def update_os(self, os_name, target)` -- Record detected operating system for a target.
- `SoulUpdater.update_credentials` (method) `skills/lazyown_objective.py:403` `def update_credentials(self, creds)` -- Replace the ## Known Credentials section with discovered credentials.
- `SoulUpdater.update_access` (method) `skills/lazyown_objective.py:430` `def update_access(self, level, target, method)` -- Update achieved access level for a target.
- `SoulUpdater.update_vulnerabilities` (method) `skills/lazyown_objective.py:437` `def update_vulnerabilities(self, vulns)` -- Replace ## Key Vulnerabilities with the most severe findings.
- `SoulUpdater.main` (method) `skills/lazyown_objective.py:456` `def main()`

## skills/lazyown_parquet_db.py
Depends on: `core/logging.py`, `modules/atomic_enricher.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/mcp_bridge.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/tests/test_parquet_db.py`, `skills/update_knowledge.py`, `tests/test_core_modules.py`
- `ParquetDB.__init__` (method) `skills/lazyown_parquet_db.py:295` `def __init__(self, lazyown_dir)`
- `ParquetDB.sync` (method) `skills/lazyown_parquet_db.py:316` `def sync(self, csv_path)` -- Ingest sessions/LazyOwn_session_report.csv into session_knowledge.parquet.
- `ParquetDB.annotate` (method) `skills/lazyown_parquet_db.py:405` `def annotate(self, row_id, success, category, outcome)` -- Patch a row in session_knowledge.parquet by its id.
- `ParquetDB.annotate_rich` (method) `skills/lazyown_parquet_db.py:434` `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` -- Full annotation after real execution: stores output snippet + all metadata.
- `ParquetDB.query_session` (method) `skills/lazyown_parquet_db.py:490` `def query_session(self, phase, target, success_only, limit)` -- Query session_knowledge.parquet.
- `ParquetDB.query_knowledge` (method) `skills/lazyown_parquet_db.py:526` `def query_knowledge(self, keyword, parquet_name, columns, limit)` -- Search for keyword across one or all parquets in parquets/.
- `ParquetDB.query_atomic` (method) `skills/lazyown_parquet_db.py:576` `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team catalogue (parquets/techniques_enriched.parquet).
- `ParquetDB.context_for_phase` (method) `skills/lazyown_parquet_db.py:630` `def context_for_phase(self, phase, target, limit)` -- Return a rich context dict for MCP reasoning:
- `ParquetDB.stats` (method) `skills/lazyown_parquet_db.py:729` `def stats(self)`
- `ParquetDB.list_parquets` (method) `skills/lazyown_parquet_db.py:743` `def list_parquets(self)`
- `ParquetDB.train_classifier` (method) `skills/lazyown_parquet_db.py:748` `def train_classifier(self, min_rows)` -- Train a lightweight RandomForest classifier on session_knowledge.parquet.
- `ParquetDB.predict_success` (method) `skills/lazyown_parquet_db.py:843` `def predict_success(self, command, category)` -- Use the trained classifier to estimate probability of success.
- `ParquetDB.verify_model_integrity` (method) `skills/lazyown_parquet_db.py:892` `def verify_model_integrity(model_path, encoder_path, hash_path)` -- Verify SHA256 integrity of classifier model and encoder files.
- `ParquetDB.get_pdb` (method) `skills/lazyown_parquet_db.py:948` `def get_pdb(lazyown_dir)`
- `ParquetDB.main` (method) `skills/lazyown_parquet_db.py:961` `def main()`

## skills/lazyown_permissions.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `PermissionRule.to_dict` (method) `skills/lazyown_permissions.py:36` `def to_dict(self)`
- `PermissionSystem.__init__` (method) `skills/lazyown_permissions.py:103` `def __init__(self, sessions_dir)`
- `PermissionSystem.add_rule` (method) `skills/lazyown_permissions.py:145` `def add_rule(self, tool_pattern, action, condition, description)`
- `PermissionSystem.remove_rule` (method) `skills/lazyown_permissions.py:151` `def remove_rule(self, tool_pattern, action)`
- `PermissionSystem.set_mode` (method) `skills/lazyown_permissions.py:157` `def set_mode(self, mode)`
- `PermissionSystem.list_rules` (method) `skills/lazyown_permissions.py:162` `def list_rules(self)`
- `PermissionSystem.evaluate` (method) `skills/lazyown_permissions.py:167` `def evaluate(self, tool_name, arguments)` -- Returns (decision, reason). decision: "allow" | "deny" | "ask"
- `PermissionSystem.metrics` (method) `skills/lazyown_permissions.py:237` `def metrics(self)` -- Aggregate audit log into per-decision and per-tool counts.
- `PermissionSystem.status_text` (method) `skills/lazyown_permissions.py:279` `def status_text(self)`

## skills/lazyown_policy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/detection_oracle.py`, `modules/logging_config.py`
Imported by: `cli/recommendation_signals.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/swan_agent.py`, `tests/test_engage_orchestrator.py`, `tests/test_moe_rl_swan.py`, `tests/test_scope_bound_auto_gate.py`
- `Config.default` (method) `skills/lazyown_policy.py:82` `def default(cls)` -- Construct configuration anchored to this file's repository root.
- `Config.ollama_url` (method) `skills/lazyown_policy.py:123` `def ollama_url(self)` -- Full URL for the Ollama generate endpoint.
- `OutcomeType.infer_category` (method) `skills/lazyown_policy.py:267` `def infer_category(command, args)` -- Return the ActionCategory best matching the command and its arguments.
- `ClassificationResult.unknown` (method) `skills/lazyown_policy.py:317` `def unknown(cls, tier)` -- Produce a result indicating the tier could not classify.
- `EpisodeRecord.to_dict` (method) `skills/lazyown_policy.py:357` `def to_dict(self)` -- Serialise to a plain dict suitable for JSON encoding.
- `EpisodeRecord.from_dict` (method) `skills/lazyown_policy.py:362` `def from_dict(cls, d)` -- Deserialise from a dict produced by to_dict.
- `IOutputClassifier.classify` (method) `skills/lazyown_policy.py:376` `def classify(self, command, args, output, exit_code)` -- Classify the outcome of one command execution.
- `ExitCodeClassifier.classify` (method) `skills/lazyown_policy.py:401` `def classify(self, command, args, output, exit_code)` -- Return a low-confidence result based solely on the exit code.
- `HeuristicClassifier.classify` (method) `skills/lazyown_policy.py:444` `def classify(self, command, args, output, exit_code)` -- Scan output for known success or failure signatures.
- `_OllamaClassifierBase.__init__` (method) `skills/lazyown_policy.py:496` `def __init__(self, cfg, model, tier_name)`
- `_OllamaClassifierBase.classify` (method) `skills/lazyown_policy.py:570` `def classify(self, command, args, output, exit_code)` -- Send the command context to Ollama and parse the JSON reply.
- `OllamaSmallClassifier.__init__` (method) `skills/lazyown_policy.py:591` `def __init__(self, cfg)`
- `OllamaLargeClassifier.__init__` (method) `skills/lazyown_policy.py:601` `def __init__(self, cfg)`
- `UserInteractiveClassifier.classify` (method) `skills/lazyown_policy.py:616` `def classify(self, command, args, output, exit_code)` -- Prompt the operator and return their authoritative verdict.
- `CascadeClassifier.__init__` (method) `skills/lazyown_policy.py:666` `def __init__(self, cfg, interactive)`
- `CascadeClassifier.classify` (method) `skills/lazyown_policy.py:677` `def classify(self, command, args, output, exit_code)` -- Return the first sufficiently confident result, or the best available.
- `DetectionRiskAssessor.__init__` (method) `skills/lazyown_policy.py:715` `def __init__(self)`
- `DetectionRiskAssessor.assess_probability` (method) `skills/lazyown_policy.py:733` `def assess_probability(self, command, args, category)` -- Return detection probability in [0.0, 1.0].
- `DetectionRiskAssessor.is_high_risk` (method) `skills/lazyown_policy.py:746` `def is_high_risk(self, command, args, category)` -- Return True when detection probability meets or exceeds the threshold.
- `RewardCalculator.__init__` (method) `skills/lazyown_policy.py:773` `def __init__(self, cfg, risk_assessor)`
- `RewardCalculator.calculate` (method) `skills/lazyown_policy.py:783` `def calculate(self, category, outcome)` -- Return the reward integer for the given (category, outcome) pair.
- `RewardCalculator.calculate_with_detection` (method) `skills/lazyown_policy.py:798` `def calculate_with_detection(self, category, outcome, command, args)` -- Return (reward, detection_probability) for the given execution.
- `CSVSessionReader.__init__` (method) `skills/lazyown_policy.py:850` `def __init__(self, cfg)`
- `CSVSessionReader.read` (method) `skills/lazyown_policy.py:855` `def read(self)` -- Parse the CSV and return all classifiable rows as StepRecord instances.
- `IEpisodeStore.append_step` (method) `skills/lazyown_policy.py:903` `def append_step(self, step)` -- Add a step to the episode for its target, creating the episode if needed.
- `IEpisodeStore.load_all` (method) `skills/lazyown_policy.py:907` `def load_all(self)` -- Load every stored episode.
- `IEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:911` `def get_episode(self, target)` -- Return the episode for the given target, or None.
- `JSONLEpisodeStore.__init__` (method) `skills/lazyown_policy.py:923` `def __init__(self, cfg)`
- `JSONLEpisodeStore.append_step` (method) `skills/lazyown_policy.py:927` `def append_step(self, step)` -- Upsert the step into its target's episode and persist.
- `JSONLEpisodeStore.load_all` (method) `skills/lazyown_policy.py:947` `def load_all(self)` -- Deserialise all episodes from the .jsonl file.
- `JSONLEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:963` `def get_episode(self, target)` -- Return the episode for target, or None if not found.
- `TransitionTable.__init__` (method) `skills/lazyown_policy.py:987` `def __init__(self, cfg)`
- `TransitionTable.record` (method) `skills/lazyown_policy.py:993` `def record(self, from_state, to_category, outcome)` -- Increment the counter for the given transition and persist.
- `TransitionTable.query` (method) `skills/lazyown_policy.py:1003` `def query(self, from_state)` -- Return (next_category, success_rate, total_count) tuples for the given from_state, filtered by min_transition_count...
- `PolicyEngine.__init__` (method) `skills/lazyown_policy.py:1107` `def __init__(self, cfg, transitions)`
- `PolicyEngine.recommend` (method) `skills/lazyown_policy.py:1111` `def recommend(self, recent_steps)` -- Return up to top_k dicts with keys: category, reason, confidence, source.
- `SessionClassificationPipeline.__init__` (method) `skills/lazyown_policy.py:1202` `def __init__(self, cfg, interactive)`
- `SessionClassificationPipeline.process` (method) `skills/lazyown_policy.py:1210` `def process(self, target, command, args, output, exit_code, timestamp)` -- Classify, reward, store, and return a StepRecord for the given execution.
- `PolicyAdvisor.__init__` (method) `skills/lazyown_policy.py:1267` `def __init__(self, cfg)`
- `PolicyAdvisor.advise` (method) `skills/lazyown_policy.py:1272` `def advise(self, target)` -- Return the policy engine's recommendations for the given target.
- `PolicyAdvisor.episode_summary` (method) `skills/lazyown_policy.py:1277` `def episode_summary(self, target)` -- Return a high-level summary dict for the target's episode.
- `LazyOwnPolicyIntegration.__init__` (method) `skills/lazyown_policy.py:1302` `def __init__(self, cfg)`
- `LazyOwnPolicyIntegration.on_command_complete` (method) `skills/lazyown_policy.py:1307` `def on_command_complete(self, target, command, args, output, exit_code)` -- Classify a completed command and record it in the episode store.
- `LazyOwnPolicyIntegration.get_recommendations` (method) `skills/lazyown_policy.py:1318` `def get_recommendations(self, target)` -- Return ranked next-action recommendations for the target.
- `ApprovalOutcome.is_approved` (method) `skills/lazyown_policy.py:1365` `def is_approved(self)` -- True when the gate authorised execution.
- `ApprovalOutcome.is_denied` (method) `skills/lazyown_policy.py:1370` `def is_denied(self)` -- True when the gate denied execution.
- `IApprovalSink.announce` (method) `skills/lazyown_policy.py:1384` `def announce(self, request)` -- Publish the request so operators can see and resolve it.
- `IApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1388` `def resolution_for(self, approval_id)` -- Return the latest resolution for the request or None if pending.
- `FileApprovalSink.__init__` (method) `skills/lazyown_policy.py:1400` `def __init__(self, sessions_dir)`
- `FileApprovalSink.path` (method) `skills/lazyown_policy.py:1405` `def path(self)` -- Absolute path of the underlying JSONL file.
- `FileApprovalSink.announce` (method) `skills/lazyown_policy.py:1409` `def announce(self, request)`
- `FileApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1426` `def resolution_for(self, approval_id)`
- `BroadcastApprovalSink.__init__` (method) `skills/lazyown_policy.py:1463` `def __init__(self, narrator, file_sink)`
- `BroadcastApprovalSink.announce` (method) `skills/lazyown_policy.py:1471` `def announce(self, request)`
- `BroadcastApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1499` `def resolution_for(self, approval_id)`
- `StdinApprovalSink.__init__` (method) `skills/lazyown_policy.py:1513` `def __init__(self, stream)`
- `StdinApprovalSink.announce` (method) `skills/lazyown_policy.py:1523` `def announce(self, request)`
- `StdinApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1552` `def resolution_for(self, approval_id)`
- `CompositeApprovalSink.__init__` (method) `skills/lazyown_policy.py:1564` `def __init__(self, sinks)`
- `CompositeApprovalSink.announce` (method) `skills/lazyown_policy.py:1569` `def announce(self, request)`
- `CompositeApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1576` `def resolution_for(self, approval_id)`
- `ApprovalGate.__init__` (method) `skills/lazyown_policy.py:1634` `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)`
- `ApprovalGate.request` (method) `skills/lazyown_policy.py:1667` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome for the proposed execution.
- `ScopeBoundAutoGate.__init__` (method) `skills/lazyown_policy.py:1850` `def __init__(self, payload_path, in_scope_fn)`
- `ScopeBoundAutoGate.request` (method) `skills/lazyown_policy.py:1866` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome without ever prompting a human.
- `HistoryBootstrapper.__init__` (method) `skills/lazyown_policy.py:1928` `def __init__(self, cfg)`
- `HistoryBootstrapper.run` (method) `skills/lazyown_policy.py:1934` `def run(self)` -- Process all CSV rows and return the total number of steps indexed.
- `HistoryBootstrapper.main` (method) `skills/lazyown_policy.py:2036` `def main()` -- Parse CLI arguments and dispatch to the appropriate command handler.

## skills/lazyown_session.py
Depends on: `skills/lazyown_context.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `SessionTranscript.__init__` (method) `skills/lazyown_session.py:82` `def __init__(self, sessions_dir, session_id)`
- `SessionTranscript.append` (method) `skills/lazyown_session.py:106` `def append(self, event_type, data)` -- Append a single event.
- `SessionTranscript.get_recent` (method) `skills/lazyown_session.py:143` `def get_recent(self, n)` -- Return the last n events.
- `SessionTranscript.get_all` (method) `skills/lazyown_session.py:161` `def get_all(self)`
- `SessionTranscript.count` (method) `skills/lazyown_session.py:164` `def count(self)`
- `SessionTranscript.maybe_auto_compact` (method) `skills/lazyown_session.py:174` `def maybe_auto_compact(self, threshold)` -- If event count since the last compact_boundary exceeds threshold, generate a template summary of those events and...
- `SessionTranscript.add_compact_boundary` (method) `skills/lazyown_session.py:209` `def add_compact_boundary(self, summary, preserved_uuids)` -- Mark a compaction point.
- `SessionTranscript.fork` (method) `skills/lazyown_session.py:227` `def fork(self, new_id)` -- Create a new transcript forked from this one.
- `SessionTranscript.status_text` (method) `skills/lazyown_session.py:257` `def status_text(self)`
- `SessionTranscript.get_transcript` (method) `skills/lazyown_session.py:281` `def get_transcript(sessions_dir, session_id)` -- Return the active transcript singleton.
- `SessionTranscript.reset_transcript` (method) `skills/lazyown_session.py:294` `def reset_transcript(sessions_dir, session_id)` -- Force a new transcript (e.g., after fork or session reset).

## skills/mcp_generated_tools.py
- `get_generated_tool_definitions` (function) `skills/mcp_generated_tools.py:659` `def get_generated_tool_definitions()` -- Return list[types.Tool] entries for all generated tools.
- `register_all_generated_handlers` (function) `skills/mcp_generated_tools.py:684` `def register_all_generated_handlers(register_handler_fn, make_text_fn, run_lazyown_cmd_fn)` -- Register every generated handler via *register_handler_fn*.

## skills/mcp_tool_generator.py
- `load_command_index` (function) `skills/mcp_tool_generator.py:29` `def load_command_index()`
- `extract_commands` (function) `skills/mcp_tool_generator.py:34` `def extract_commands(index)` -- Return {command_name: summary} for all unique non-duplicate commands.
- `extract_existing_handlers` (function) `skills/mcp_tool_generator.py:55` `def extract_existing_handlers()` -- Parse lazyown_mcp.py for all defined MCP tool names.
- `sanitize_description` (function) `skills/mcp_tool_generator.py:72` `def sanitize_description(summary, max_len)` -- Truncate and clean a command summary for use as a tool description.
- `sanitize_docstring` (function) `skills/mcp_tool_generator.py:85` `def sanitize_docstring(text)` -- Escape backslashes and quotes for triple-quoted docstrings.
- `generate_module` (function) `skills/mcp_tool_generator.py:106` `def generate_module(commands, existing_handlers, limit)` -- Build the complete Python source for mcp_generated_tools.py.
- `verify_coverage` (function) `skills/mcp_tool_generator.py:203` `def verify_coverage(commands, existing_handlers)` -- Compare indexed commands against existing MCP tool coverage.
- `main` (function) `skills/mcp_tool_generator.py:220` `def main()`


Next: [API_p17.md](API_p17.md)
