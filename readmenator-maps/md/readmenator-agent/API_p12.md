# API (page 12 of 22)
Previous: [API_p11.md](API_p11.md)

## modules/lazy_agent.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`
- `model_timeout_sec` (function) `modules/lazy_agent.py:41` `def model_timeout_sec()` -- Return the hard per-turn model timeout from configuration.
- `tool_calling_enabled` (function) `modules/lazy_agent.py:57` `def tool_calling_enabled()` -- Return whether agentic tool calling is enabled by configuration.
- `max_iterations` (function) `modules/lazy_agent.py:72` `def max_iterations()` -- Return the bounded agent step budget from configuration.
- `resolve_agentic_model` (function) `modules/lazy_agent.py:83` `def resolve_agentic_model(exclude)` -- Return a raw tool-calling backend for the best pool member, or None.
- `ObservableAgentRunner.__init__` (method) `modules/lazy_agent.py:148` `def __init__(self, model, system_prompt, max_iterations, on_event)` -- Bind the model and the optional event sink (kind, name, text).
- `ObservableAgentRunner.run` (method) `modules/lazy_agent.py:168` `def run(self, user_input)` -- Base loop plus final-turn persistence for true resume.
- `ConversationStore.__init__` (method) `modules/lazy_agent.py:264` `def __init__(self, task_id)` -- Bind the conversation store for one task (``main`` when empty).
- `ConversationStore.intent_messages` (method) `modules/lazy_agent.py:273` `def intent_messages(self, intent_id)` -- Return the stored messages for one intent (resume seed).
- `ConversationStore.save_intent` (method) `modules/lazy_agent.py:278` `def save_intent(self, intent_id, messages)` -- Persist the tail of one intent conversation.
- `ConversationStore.session` (method) `modules/lazy_agent.py:287` `def session(self, session_id)` -- Return one main-agent session payload (empty when unknown).
- `ConversationStore.sessions` (method) `modules/lazy_agent.py:291` `def sessions(self)` -- List main-agent sessions with title, message count and age.
- `ConversationStore.save_session` (method) `modules/lazy_agent.py:305` `def save_session(self, session_id, messages, title)` -- Persist one main-agent session conversation tail.
- `ConversationStore.reset_intents` (method) `modules/lazy_agent.py:315` `def reset_intents(self)` -- Drop every stored intent conversation (fresh agent start).
- `register_tools` (function) `modules/lazy_agent.py:322` `def register_tools(runner, specs)` -- Register tool specs (name, description, func, parameters, required).
- `run_worker_session` (function) `modules/lazy_agent.py:335` `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` -- Run one agentic intent attempt with resume seeding.
- `run_main_session` (function) `modules/lazy_agent.py:374` `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` -- Run one main-agent turn, resuming the stored session conversation.
- `run_external_opencode` (function) `modules/lazy_agent.py:396` `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` -- Run one headless ``opencode run`` task with MCP tooling.
- `run_external_hermes` (function) `modules/lazy_agent.py:472` `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` -- Run one detached ``hermes chat --oneshot`` task.

## modules/lazy_bridge.py
Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_lazy_loop.py`
- `lazy_tasks` (function) `modules/lazy_bridge.py:88` `def lazy_tasks()` -- Load LAZY task registry.
- `lazy_assets` (function) `modules/lazy_bridge.py:99` `def lazy_assets()` -- Load LAZY asset nodes.
- `lazy_graph` (function) `modules/lazy_bridge.py:110` `def lazy_graph(task_id)` -- Load experiment graph for a task.
- `lazy_activity` (function) `modules/lazy_bridge.py:123` `def lazy_activity(task_id)` -- Load activity transcript for a task.
- `lazy_traffic` (function) `modules/lazy_bridge.py:135` `def lazy_traffic(task_id)` -- Load traffic log for a task.
- `lazy_guard_audit` (function) `modules/lazy_bridge.py:147` `def lazy_guard_audit(task_id)` -- Load guard audit for a task.
- `bridge_status` (function) `modules/lazy_bridge.py:159` `def bridge_status()` -- Summarize LAZY universe and last sync cursor.
- `pull_to_world_model` (function) `modules/lazy_bridge.py:206` `def pull_to_world_model()` -- Sync LAZY graphs and assets into LazyOwn world model.
- `pull_to_objectives` (function) `modules/lazy_bridge.py:251` `def pull_to_objectives()` -- Inject open LAZY tasks as LazyOwn objectives without duplicates.
- `pull_findings_to_lifecycle` (function) `modules/lazy_bridge.py:286` `def pull_findings_to_lifecycle()` -- Confirm LAZY finding nodes in LazyOwn finding lifecycle.
- `pull_traffic_to_recorder` (function) `modules/lazy_bridge.py:314` `def pull_traffic_to_recorder()` -- Mirror LAZY traffic logs into LazyOwn traffic recorder index.
- `push_objective_to_lazy` (function) `modules/lazy_bridge.py:344` `def push_objective_to_lazy(goal, scope)` -- Export a LazyOwn objective as an LAZY-compatible task draft.
- `push_tasks_to_c2` (function) `modules/lazy_bridge.py:369` `def push_tasks_to_c2(only)` -- Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).
- `sync_all` (function) `modules/lazy_bridge.py:434` `def sync_all()` -- Run full bidirectional pull plus lifecycle, traffic and board mirror.

## modules/lazy_cli_bridge.py
Depends on: `core/config.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`
- `cli_verbs` (function) `modules/lazy_cli_bridge.py:106` `def cli_verbs()` -- Return every discovered shell verb, cached by source mtime.
- `is_cli_verb` (function) `modules/lazy_cli_bridge.py:125` `def is_cli_verb(name)` -- Return True when name is a real shell command.
- `phase_for` (function) `modules/lazy_cli_bridge.py:131` `def phase_for(verb)` -- Map a verb to its kill-chain phase via keyword affinity.
- `risk_for` (function) `modules/lazy_cli_bridge.py:140` `def risk_for(verb)` -- Classify a verb as safe, exploit or high risk.
- `needs_target_for` (function) `modules/lazy_cli_bridge.py:150` `def needs_target_for(verb)` -- Return whether the verb usually carries a target argument.
- `build_cli_command` (function) `modules/lazy_cli_bridge.py:158` `def build_cli_command(verb, target)` -- Build a shell line for any CLI verb bound to target.
- `search_cli_verbs` (function) `modules/lazy_cli_bridge.py:185` `def search_cli_verbs(query, phase, limit)` -- Search the full CLI catalog by keyword and phase.
- `cli_catalog_for_phase` (function) `modules/lazy_cli_bridge.py:211` `def cli_catalog_for_phase(phase, limit)` -- Return a compact verb list for LLM prompt injection.
- `full_cli_enabled` (function) `modules/lazy_cli_bridge.py:219` `def full_cli_enabled()` -- Return whether the loop may route any CLI verb.
- `set_full_cli` (function) `modules/lazy_cli_bridge.py:242` `def set_full_cli(enabled)` -- Persist the full-CLI routing flag and return the new value.

## modules/lazy_installer.py
Depends on: `core/config.py`, `modules/auto_registry.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`
- `installer_enabled` (function) `modules/lazy_installer.py:41` `def installer_enabled()` -- Return whether the loop may resolve install intents.
- `set_installer_enabled` (function) `modules/lazy_installer.py:58` `def set_installer_enabled(enabled)` -- Persist the installer flag and return the stored value.
- `install_command_for` (function) `modules/lazy_installer.py:70` `def install_command_for(tool)` -- Return the allowlisted install recipe for one tool, or None.
- `intent_for` (function) `modules/lazy_installer.py:75` `def intent_for(tool)` -- Build the canonical install intent summary for one tool.
- `tool_from_intent` (function) `modules/lazy_installer.py:80` `def tool_from_intent(text)` -- Extract the tool name from an install intent, else empty string.
- `steps_for_install` (function) `modules/lazy_installer.py:88` `def steps_for_install(text)` -- Resolve an install intent to its recipe, or None.

## modules/lazy_intel.py
Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/world_model.py`, `utils.py`
Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `tests/test_loop_supervision.py`
- `infer_source` (function) `modules/lazy_intel.py:79` `def infer_source(command, intent_text)` -- Classify where a resolved step likely came from.
- `describe_command` (function) `modules/lazy_intel.py:105` `def describe_command(command)` -- Describe a command with phase and risk.
- `record_routing_decision` (function) `modules/lazy_intel.py:120` `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `record_routing_outcome` (function) `modules/lazy_intel.py:160` `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `read_decisions` (function) `modules/lazy_intel.py:202` `def read_decisions(task_id, limit)` -- Read routing records, optionally filtered by task.
- `mask_configured` (function) `modules/lazy_intel.py:228` `def mask_configured(text)` -- Mask only operator-configured credential values in live text.
- `stack_signature` (function) `modules/lazy_intel.py:254` `def stack_signature(assets)` -- Fingerprint the target stack from service assets.
- `fuse_routing_decisions` (function) `modules/lazy_intel.py:285` `def fuse_routing_decisions(task_id)` -- Fuse routing records into the world model as host notes.
- `export_spans` (function) `modules/lazy_intel.py:324` `def export_spans(task_id, out)` -- Export activity records as trace spans for observability.

## modules/lazy_loop.py
Depends on: `core/config.py`, `core/crypto.py`, `core/hardening.py`, `core/logging.py`, `core/process.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/finding_lifecycle.py`, `modules/intercept.py`, `modules/lazy_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_installer.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`, `modules/lazy_roles.py`, `modules/lazy_skills.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/loop_ai_bridge.py`, `modules/notify.py`, `modules/orchestrator_config.py`, `modules/selfupdate.py`, `modules/traffic_recorder.py`, `utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/lazy_orchestrator.py`, `lazyc2.py`, `lazyown.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_engine.py`, `modules/lazy_intel.py`, `modules/lazy_mentions.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_asset_gate.py`, `tests/test_auto_crypto.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_store_race.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`, `tests/test_security_codeql_batch.py`
- `plausible_command` (function) `modules/lazy_loop.py:150` `def plausible_command(command)` -- Reject obvious hallucinations such as ``nmap --block``.
- `loop_exiting` (function) `modules/lazy_loop.py:305` `def loop_exiting()` -- Return True once the shell is tearing the loop runtime down.
- `arm_exit_watchdog` (function) `modules/lazy_loop.py:322` `def arm_exit_watchdog(seconds)` -- Guarantee process death even with threads stuck in socket reads.
- `scrub_secrets` (function) `modules/lazy_loop.py:363` `def scrub_secrets(text)` -- Mask API keys/tokens before a string reaches logs or the panel.
- `wake_task` (function) `modules/lazy_loop.py:467` `def wake_task(task_id)` -- Signal a running engine that new work landed for its task.
- `register_worker` (function) `modules/lazy_loop.py:501` `def register_worker(worker)` -- Track a live Worker so shell exit can close its side channels.
- `unregister_worker` (function) `modules/lazy_loop.py:507` `def unregister_worker(worker)` -- Drop a finished Worker from the shutdown registry.
- `shutdown_loop_runtime` (function) `modules/lazy_loop.py:513` `def shutdown_loop_runtime(reason)` -- Tear down every loop-owned resource; safe on any exit path.
- `task_llm_chain` (function) `modules/lazy_loop.py:728` `def task_llm_chain(store, task_id)` -- Return the per-task LLM chain members (empty when unbound).
- `parse_judge_output` (function) `modules/lazy_loop.py:738` `def parse_judge_output(raw)` -- Parse strict judge JSON demanding decision and comment.
- `judge_command` (function) `modules/lazy_loop.py:766` `def judge_command(command, background, fail_action)` -- Ask the pool for a guard verdict, applying the configured fail policy.
- `AssetGraph.__init__` (method) `modules/lazy_loop.py:859` `def __init__(self)` -- Load persisted assets or start empty.
- `AssetGraph.dedupe_key` (method) `modules/lazy_loop.py:877` `def dedupe_key(self, kind, value, parent_id)` -- Compute program-owned dedupe key for an asset.
- `AssetGraph.insert` (method) `modules/lazy_loop.py:881` `def insert(self, kind, value, parent_id, meta, task_id)` -- Insert asset or return existing node with same dedupe key.
- `AssetGraph.get` (method) `modules/lazy_loop.py:911` `def get(self, asset_id)` -- Return asset by id or None.
- `AssetGraph.list` (method) `modules/lazy_loop.py:915` `def list(self, kind)` -- List assets optionally filtered by kind.
- `AssetGraph.mark_tested` (method) `modules/lazy_loop.py:922` `def mark_tested(self, asset_id)` -- Flag asset as tested by a worker intent.
- `AssetGraph.coverage` (method) `modules/lazy_loop.py:932` `def coverage(self, scope)` -- Compute tested/total coverage, optionally scoped.
- `AssetGraph.scoped` (method) `modules/lazy_loop.py:948` `def scoped(self, scope, kind)` -- List assets owned by the task scope via ownership matching.
- `AssetGraph.untested` (method) `modules/lazy_loop.py:961` `def untested(self, limit)` -- Return oldest untested assets up to limit.
- `AssetGraph.coverage_for` (method) `modules/lazy_loop.py:966` `def coverage_for(self, graph, scope)` -- Compute task-scoped coverage like the planner graph_overview.
- `AssetGraph.untested_for` (method) `modules/lazy_loop.py:994` `def untested_for(self, graph, scope, limit)` -- Return scope-filtered assets not yet covered by this task.
- `ExplorationGraph.__init__` (method) `modules/lazy_loop.py:1022` `def __init__(self, task_id)` -- Load task graph or start empty.
- `ExplorationGraph.add_node` (method) `modules/lazy_loop.py:1056` `def add_node(self, kind, text, state, priority, meta)` -- Append node and return it.
- `ExplorationGraph.get` (method) `modules/lazy_loop.py:1079` `def get(self, node_id)` -- Return node by id or None.
- `ExplorationGraph.set_state` (method) `modules/lazy_loop.py:1083` `def set_state(self, node_id, state)` -- Transition node state and persist.
- `ExplorationGraph.add_edge` (method) `modules/lazy_loop.py:1094` `def add_edge(self, src, dst, kind)` -- Link two existing nodes.
- `ExplorationGraph.anchor` (method) `modules/lazy_loop.py:1107` `def anchor(self, node_id, asset_id)` -- Anchor exploration node to a concrete asset.
- `ExplorationGraph.anchors_for` (method) `modules/lazy_loop.py:1118` `def anchors_for(self, node_id)` -- Return asset ids anchored to node.
- `ExplorationGraph.anchored_nodes` (method) `modules/lazy_loop.py:1122` `def anchored_nodes(self, asset_id)` -- Return exploration node ids anchored to asset.
- `ExplorationGraph.list` (method) `modules/lazy_loop.py:1126` `def list(self, kind, state)` -- List nodes optionally filtered by kind/state.
- `ExplorationGraph.children` (method) `modules/lazy_loop.py:1135` `def children(self, node_id, kind)` -- Return destination ids of outgoing edges.
- `ExplorationGraph.parents` (method) `modules/lazy_loop.py:1142` `def parents(self, node_id, kind)` -- Return source ids of incoming edges.
- `ExplorationGraph.overview` (method) `modules/lazy_loop.py:1149` `def overview(self)` -- Return planner-facing state summary like graph overview.
- `ExplorationGraph.reload` (method) `modules/lazy_loop.py:1172` `def reload(self)` -- Reload graph from disk, discarding in-memory state.
- `ExplorationGraph.compare_and_claim` (method) `modules/lazy_loop.py:1196` `def compare_and_claim(self, node_id)` -- CAS claim: reload, verify still open, then mark running.
- `ExplorationGraph.finding_signature` (method) `modules/lazy_loop.py:1224` `def finding_signature(self, text)` -- Normalize finding text into dedupe signature.
- `ExplorationGraph.has_finding` (method) `modules/lazy_loop.py:1230` `def has_finding(self, text)` -- Return existing finding with same signature or None.
- `ExplorationGraph.node_detail` (method) `modules/lazy_loop.py:1240` `def node_detail(self, node_id)` -- Full node view: text, state, meta, edges, anchors, trace tail.
- `ExplorationGraph.list_facts` (method) `modules/lazy_loop.py:1256` `def list_facts(self, query, limit, hot_full)` -- Keyword-filtered facts like list_facts.
- `ExplorationGraph.record_fact` (method) `modules/lazy_loop.py:1272` `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` -- Worker fact write like recordFact: deduped, anchored, done.
- `Frontier.__init__` (method) `modules/lazy_loop.py:1297` `def __init__(self, graph)` -- Bind frontier to a task graph.
- `Frontier.pending` (method) `modules/lazy_loop.py:1302` `def pending(self)` -- Return pending intents ordered by priority then id.
- `Frontier.claim_next` (method) `modules/lazy_loop.py:1307` `def claim_next(self)` -- Atomically claim highest-priority pending intent (cross-process CAS).
- `ActivityLog.__init__` (method) `modules/lazy_loop.py:1325` `def __init__(self, task_id)` -- Bind log to task.
- `ActivityLog.emit` (method) `modules/lazy_loop.py:1330` `def emit(self, worker, kind, text, intent_id, tool_use_id)` -- Append one activity record and return it.
- `ActivityLog.read` (method) `modules/lazy_loop.py:1355` `def read(self, limit)` -- Return most recent records up to limit.
- `ActivityLog.for_intent` (method) `modules/lazy_loop.py:1369` `def for_intent(self, intent_id)` -- Return records for one intent.
- `ActivityLog.trace` (method) `modules/lazy_loop.py:1373` `def trace(self, intent_id, query, step_id, limit)` -- Work-scoped trace view like get_worker_trace.
- `ActivityLog.search_all` (method) `modules/lazy_loop.py:1411` `def search_all(self, query, limit)` -- Global keyword search across every work in this task.
- `ActivityLog.search` (method) `modules/lazy_loop.py:1441` `def search(self, query, exclude_intent)` -- Search worker traces by keyword, excluding one intent like the planner.
- `TrafficLog.__init__` (method) `modules/lazy_loop.py:1458` `def __init__(self, task_id)` -- Bind log to task or global stream.
- `TrafficLog.record` (method) `modules/lazy_loop.py:1463` `def record(self, kind, command, output, meta)` -- Append one traffic record and return it.
- `TrafficLog.read` (method) `modules/lazy_loop.py:1485` `def read(self, limit)` -- Return most recent traffic records.
- `TrafficLog.search` (method) `modules/lazy_loop.py:1499` `def search(self, query, limit)` -- Full-text search over command/output like traffic_search.
- `TrafficLog.search_host` (method) `modules/lazy_loop.py:1510` `def search_host(self, host, port, limit)` -- Port-aware host search: same-host/different-port rows never mix.
- `TrafficLog.get` (method) `modules/lazy_loop.py:1538` `def get(self, digest)` -- Fetch one exchange by digest like traffic_get.
- `TrafficLog.recorder_body` (method) `modules/lazy_loop.py:1545` `def recorder_body(self, digest)` -- Return stored request/response bodies for one proxy exchange.
- `TrafficLog.recorder_blob` (method) `modules/lazy_loop.py:1574` `def recorder_blob(self, digest, part, offset, length)` -- Read a proxy body in ranges like the blob API.
- `TrafficLog.templates` (method) `modules/lazy_loop.py:1605` `def templates(self, limit)` -- Group exchanges by URL-template with counts like the proxy index.
- `TrafficLog.by_template` (method) `modules/lazy_loop.py:1614` `def by_template(self, template, limit)` -- Return exchanges matching one template substring.
- `TrafficLog.bind` (method) `modules/lazy_loop.py:1619` `def bind(self, finding_id, digest, graph, role, note)` -- Attach traffic digest to a finding like bind_finding_traffic.
- `TrafficLog.evidence` (method) `modules/lazy_loop.py:1667` `def evidence(self, finding_id, graph)` -- Return a finding's traffic evidences in display order.
- `TrafficLog.reorder_evidence` (method) `modules/lazy_loop.py:1676` `def reorder_evidence(self, finding_id, digests, graph)` -- Sort a finding's evidences; unlisted ones keep their tail order.
- `TrafficLog.export` (method) `modules/lazy_loop.py:1690` `def export(self, path, limit)` -- Dump recent exchanges to a JSON file like traffic archive export.
- `TrafficLog.archive` (method) `modules/lazy_loop.py:1697` `def archive(self, label)` -- Snapshot traffic stream into sessions/lazy/traffic_archive_*.
- `TrafficLog.clear` (method) `modules/lazy_loop.py:1703` `def clear(self)` -- Drop the traffic stream, returning the discarded record count.
- `Guard.__init__` (method) `modules/lazy_loop.py:1716` `def __init__(self, task_id)` -- Load rules and audit trail.
- `Guard.add_rule` (method) `modules/lazy_loop.py:1742` `def add_rule(self, pattern, action, reason, priority)` -- Register an intercept rule; higher priority evaluates first.
- `Guard.remove_rule` (method) `modules/lazy_loop.py:1753` `def remove_rule(self, pattern)` -- Delete rules matching pattern exactly.
- `Guard.set_judge` (method) `modules/lazy_loop.py:1762` `def set_judge(self, enabled, fail_action)` -- Enable/disable the LLM judge fallback for unmatched commands.
- `Guard.check` (method) `modules/lazy_loop.py:1784` `def check(self, tool, command, tool_use_id, source, intent_id)` -- Evaluate tool call and audit it, returning allow/ask/deny.
- `Guard.audit` (method) `modules/lazy_loop.py:1836` `def audit(self, limit, action, source, query)` -- Return recent audit entries with optional status/source/text filters.
- `Guard.lookup` (method) `modules/lazy_loop.py:1864` `def lookup(self, tool_use_id)` -- Jump to the exact execution behind an approval row.
- `Guard.stats` (method) `modules/lazy_loop.py:1906` `def stats(self)` -- Attribution counters over the audit trail.
- `AssetGate.__init__` (method) `modules/lazy_loop.py:2063` `def __init__(self, task_id)` -- Bind global list plus optional per-task lists.
- `AssetGate.add` (method) `modules/lazy_loop.py:2090` `def add(self, kind, pattern, note, action)` -- Register a block (global or task) or allow (task only) rule.
- `AssetGate.remove` (method) `modules/lazy_loop.py:2111` `def remove(self, rule_id, action)` -- Delete a rule by id; returns True when something was removed.
- `AssetGate.list` (method) `modules/lazy_loop.py:2129` `def list(self)` -- Return global block plus per-task block/allow rules.
- `AssetGate.evaluate` (method) `modules/lazy_loop.py:2133` `def evaluate(self, target)` -- Gate one target: allowed flag plus human-readable reason.
- `Budget.__init__` (method) `modules/lazy_loop.py:2151` `def __init__(self, store)` -- Bind budget counters to task store.
- `Budget.limits` (method) `modules/lazy_loop.py:2155` `def limits(self, task_id)` -- Return effective limits for task.
- `Budget.set_limits` (method) `modules/lazy_loop.py:2166` `def set_limits(self, task_id)` -- Persist budget limits for task.
- `Budget.usage` (method) `modules/lazy_loop.py:2179` `def usage(self, task_id)` -- Return consumed toolcalls/findings/rounds.
- `Budget.record_toolcall` (method) `modules/lazy_loop.py:2189` `def record_toolcall(self, task_id, intent_id)` -- Count one executed tool call.
- `Budget.record_round` (method) `modules/lazy_loop.py:2201` `def record_round(self, task_id)` -- Count one orchestrator round.
- `Budget.check` (method) `modules/lazy_loop.py:2219` `def check(self, task_id)` -- Return ok/exceeded decision with reason.
- `RuntimeTracker.__init__` (method) `modules/lazy_loop.py:2235` `def __init__(self, store)` -- Bind runtime to task store.
- `RuntimeTracker.heartbeat` (method) `modules/lazy_loop.py:2239` `def heartbeat(self, task_id)` -- Return live runtime snapshot.
- `RuntimeTracker.beat` (method) `modules/lazy_loop.py:2257` `def beat(self, task_id, workers)` -- Stamp heartbeat.
- `RuntimeTracker.abort` (method) `modules/lazy_loop.py:2272` `def abort(self, task_id, cause, detail)` -- Stamp abort cause like typed AbortCause.
- `RuntimeTracker.note_trigger` (method) `modules/lazy_loop.py:2288` `def note_trigger(self, task_id, trigger_id)` -- Advance scheduler watermark so restarts never re-fire.
- `InterceptQueue.__init__` (method) `modules/lazy_loop.py:2329` `def __init__(self, task_id)` -- Bind queue to task.
- `InterceptQueue.request` (method) `modules/lazy_loop.py:2343` `def request(self, tool, command, reason, tool_use_id)` -- Enqueue one ask decision and return pending entry.
- `InterceptQueue.pending` (method) `modules/lazy_loop.py:2361` `def pending(self)` -- Return pending entries ordered by id.
- `InterceptQueue.history` (method) `modules/lazy_loop.py:2365` `def history(self, page, per_page, states, query)` -- Paginated intercept history; pending stays fully visible.
- `InterceptQueue.decide` (method) `modules/lazy_loop.py:2417` `def decide(self, item_id, verdict)` -- Approve or deny one pending entry and wake its waiter.
- `InterceptQueue.wait` (method) `modules/lazy_loop.py:2431` `def wait(self, item_id, timeout_sec)` -- Block until decided or timeout; timeout denies safely.
- `TodoStore.__init__` (method) `modules/lazy_loop.py:2463` `def __init__(self, task_id)` -- Load persisted todos.
- `TodoStore.add` (method) `modules/lazy_loop.py:2474` `def add(self, text)` -- Append a serial step and return it.
- `TodoStore.complete` (method) `modules/lazy_loop.py:2481` `def complete(self, item_id)` -- Mark step done.
- `TodoStore.next_pending` (method) `modules/lazy_loop.py:2490` `def next_pending(self)` -- Return first pending step.
- `TodoStore.as_list` (method) `modules/lazy_loop.py:2497` `def as_list(self)` -- Return all steps.
- `TaskStore.__init__` (method) `modules/lazy_loop.py:2505` `def __init__(self)` -- Load task registry.
- `TaskStore.create` (method) `modules/lazy_loop.py:2514` `def create(self, goal, description)` -- Create task record and return it.
- `TaskStore.get` (method) `modules/lazy_loop.py:2525` `def get(self, task_id)` -- Return raw task record or None.
- `TaskStore.list` (method) `modules/lazy_loop.py:2529` `def list(self)` -- Return all task records.
- `TaskStore.set_status` (method) `modules/lazy_loop.py:2533` `def set_status(self, task_id, status)` -- Update task status.
- `TaskStore.pause` (method) `modules/lazy_loop.py:2545` `def pause(self, task_id)` -- Pause planner and workers like the planner Engine.Pause.
- `TaskStore.resume` (method) `modules/lazy_loop.py:2549` `def resume(self, task_id)` -- Resume a paused task back to running like the planner resumeTask.
- `TaskStore.delete` (method) `modules/lazy_loop.py:2558` `def delete(self, task_id)` -- Remove task record; per-task graph files are cleaned by caller.
- `TaskStore.active_count` (method) `modules/lazy_loop.py:2567` `def active_count(self, exclude)` -- Return how many tasks are currently running.
- `TaskStore.queue` (method) `modules/lazy_loop.py:2571` `def queue(self)` -- Return queued tasks in FIFO arrival order.
- `TaskStore.enqueue` (method) `modules/lazy_loop.py:2576` `def enqueue(self, task_id)` -- Mark a task queued with its arrival stamp.
- `TaskStore.dequeue_next` (method) `modules/lazy_loop.py:2587` `def dequeue_next(self)` -- Pop the oldest queued task and mark it running.
- `TaskStore.set_llm_chain` (method) `modules/lazy_loop.py:2602` `def set_llm_chain(self, task_id, members, active)` -- Bind a per-task LLM chain with a failover cursor.
- `TaskStore.llm_state` (method) `modules/lazy_loop.py:2630` `def llm_state(self, task_id)` -- Return the task LLM chain state (empty when unbound).
- `TaskStore.advance_llm` (method) `modules/lazy_loop.py:2636` `def advance_llm(self, task_id)` -- Advance the per-task active member after quota exhaustion.
- `TaskStore.set_skills` (method) `modules/lazy_loop.py:2660` `def set_skills(self, task_id, names, auto)` -- Pin skills for prompt injection and optionally toggle auto-match.
- `TaskStore.set_deadline` (method) `modules/lazy_loop.py:2685` `def set_deadline(self, task_id, timeout_sec)` -- Stamp absolute deadline like the planner deadline coordinator.
- `TaskStore.expired` (method) `modules/lazy_loop.py:2695` `def expired(self, task_id)` -- Report whether task deadline passed.
- `TaskStore.add_constraint` (method) `modules/lazy_loop.py:2701` `def add_constraint(self, task_id, ctype, text, scope)` -- Register allow/deny operation constraint like the planner set_constraints.
- `TaskStore.add_scope` (method) `modules/lazy_loop.py:2720` `def add_scope(self, task_id, kind, value, reason)` -- Register authorized asset scope like the planner add_task_scope.
- `TaskStore.steer` (method) `modules/lazy_loop.py:2731` `def steer(self, task_id, intent_id, message)` -- Attach mid-run correction to a running intent like steer_work.
- `TaskStore.kill` (method) `modules/lazy_loop.py:2740` `def kill(self, task_id, intent_id)` -- Flag a running intent for termination like kill_work.
- `TaskStore.steer_for` (method) `modules/lazy_loop.py:2751` `def steer_for(self, task_id, intent_id)` -- Return pending steer message for intent if any.
- `TaskStore.clear_steer` (method) `modules/lazy_loop.py:2756` `def clear_steer(self, task_id, intent_id)` -- Drop the pending steer message for an intent after delivery.
- `TaskStore.killed` (method) `modules/lazy_loop.py:2769` `def killed(self, task_id, intent_id)` -- Report whether intent was flagged for termination.
- `extract_scope_items` (function) `modules/lazy_loop.py:2775` `def extract_scope_items(goal_text, description)` -- Lift explicit asset scope from goal like the planner goalsScopeTail.
- `extract_constraint_items` (function) `modules/lazy_loop.py:2807` `def extract_constraint_items(goal_text, description)` -- Lift explicit allow/deny operation bounds like the planner goals decomposer.
- `load_intel_scores` (function) `modules/lazy_loop.py:2835` `def load_intel_scores()` -- Return host exposure scores from sessions/intel_summary.json.
- `resolve_target` (function) `modules/lazy_loop.py:2850` `def resolve_target(task_id, store, graph)` -- Resolve concrete target for worker commands from scope, assets, goal.
- `decompose_goals` (function) `modules/lazy_loop.py:2873` `def decompose_goals(goal_text, description)` -- Split goal text into verifiable objectives like the planner DecomposeGoals.
- `enrich_asset` (function) `modules/lazy_loop.py:2910` `def enrich_asset(value)` -- Synchronously enrich one asset with DNS and HTTP like the planner enrich.
- `Planner.__init__` (method) `modules/lazy_loop.py:2936` `def __init__(self, task_id, assets, graph, activity, store)` -- Bind planner to task collaborators.
- `Planner.plan` (method) `modules/lazy_loop.py:2964` `def plan(self, triggers)` -- Emit 0..N intents from current situation; most wakeups emit zero.
- `Planner.refine` (method) `modules/lazy_loop.py:3043` `def refine(self)` -- Re-plan pending intents against fresh outcomes, like plan refinement.
- `Planner.finalize` (method) `modules/lazy_loop.py:3259` `def finalize(self, reason)` -- Final planner round: park open intents and record the wrap-up.
- `sink` (function) `modules/lazy_loop.py:3279` `def sink(text)`
- `Worker.__init__` (method) `modules/lazy_loop.py:3376` `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` -- Bind worker to task collaborators.
- `Worker.rebind` (method) `modules/lazy_loop.py:3421` `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` -- Point a pooled worker at the collaborators of the current round.
- `Worker.close` (method) `modules/lazy_loop.py:3445` `def close(self)` -- Release the worker's shell session and shutdown registration.
- `Worker.execute` (method) `modules/lazy_loop.py:3509` `def execute(self, intent, executor, timeout_sec)` -- Run one intent to completion and write facts back.
- `run_command` (function) `modules/lazy_loop.py:4162` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/lazy_loop.py:4187` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/lazy_loop.py:4196` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/lazy_loop.py:4207` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/lazy_loop.py:4220` `def graph_state()` -- Compact exploration overview: intents, facts, findings.
- `shell_open` (function) `modules/lazy_loop.py:4235` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/lazy_loop.py:4239` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/lazy_loop.py:4243` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/lazy_loop.py:4251` `def job_output(job_id)` -- Return the tail of one background job's output.
- `sink` (function) `modules/lazy_loop.py:4689` `def sink(text)`
- `Retester.__init__` (method) `modules/lazy_loop.py:5071` `def __init__(self, graph, activity, traffic)` -- Bind retester to task collaborators.
- `Retester.retest` (method) `modules/lazy_loop.py:5077` `def retest(self, finding_id, executor, note)` -- Re-execute finding evidence to reproduced/fixed/inconclusive.
- `Retester.retest_context` (method) `modules/lazy_loop.py:5147` `def retest_context(self, finding_id)` -- Return finding + PoC + assets + constraints like get_finding_retest_context.
- `ColdCompactor.__init__` (method) `modules/lazy_loop.py:5169` `def __init__(self, graph, activity)` -- Bind compactor to task graph.
- `ColdCompactor.noa_archives` (method) `modules/lazy_loop.py:5279` `def noa_archives(self, limit)` -- List NOA raw archives for this task (newest first).
- `ColdCompactor.hot_set` (method) `modules/lazy_loop.py:5338` `def hot_set(self)` -- Compute hot nodes by reverse reachability from live intents.
- `ColdCompactor.structural_cold` (method) `modules/lazy_loop.py:5360` `def structural_cold(self, hot)` -- Return foldable non-hot nodes before debounce.
- `ColdCompactor.covered_members` (method) `modules/lazy_loop.py:5445` `def covered_members(self)` -- Return node ids already folded under active digests.
- `ColdCompactor.on_planner_round` (method) `modules/lazy_loop.py:5457` `def on_planner_round(self)` -- Advance round, maintain stamps, trigger background compaction.
- `ColdCompactor.compact` (method) `modules/lazy_loop.py:5498` `def compact(self, threshold, mode, debounce_sec)` -- Fold cold facts into digests like coldgraph minor/major.
- `ColdCompactor.expand` (method) `modules/lazy_loop.py:5625` `def expand(self, digest_id, role)` -- Restore digest members like expandDigest.
- `ColdCompactor.cold_index` (method) `modules/lazy_loop.py:5649` `def cold_index(self)` -- Group active digests by anchored asset.
- `ColdCompactor.unfolded` (method) `modules/lazy_loop.py:5667` `def unfolded(self, limit)` -- Return cold facts unfolded up to cap with a truncated flag.
- `ColdCompactor.digest_overview` (method) `modules/lazy_loop.py:5683` `def digest_overview(self)` -- Digest index: every digest with expandable members plus cold index.
- `constraint_block` (function) `modules/lazy_loop.py:5730` `def constraint_block(constraints, scope)` -- Render allow/deny bounds as highest-priority prompt block.
- `settlement_prompt` (function) `modules/lazy_loop.py:5764` `def settlement_prompt(agent, reason)` -- Build the wrap-up instruction used when a run budget ends.
- `build_prompt_context` (function) `modules/lazy_loop.py:5787` `def build_prompt_context(task_id, graph, assets, store, budget, top)` -- Assemble a bounded prompt context for planner/worker LLM calls.
- `finding_severity` (function) `modules/lazy_loop.py:5868` `def finding_severity(text, evidence)` -- Rank finding severity like the report renderer (critical first).
- `FindingService.__init__` (method) `modules/lazy_loop.py:5885` `def __init__(self, task_id, graph, activity, store)` -- Bind service to task collaborators.
- `FindingService.report` (method) `modules/lazy_loop.py:5892` `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` -- Register a finding with severity/evidence/dedupe like report_finding.
- `FindingService.apply_drafts` (method) `modules/lazy_loop.py:6049` `def apply_drafts(self)` -- Commit finished background reporter drafts onto their findings.
- `FindingService.set_status` (method) `modules/lazy_loop.py:6086` `def set_status(self, finding_id, status)` -- Transition finding status like the workflow disposition.
- `FindingService.update_report` (method) `modules/lazy_loop.py:6103` `def update_report(self, finding_id, report)` -- Write the narrative report and bump the evidence version.
- `FindingService.ranked` (method) `modules/lazy_loop.py:6125` `def ranked(self)` -- Findings ordered critical-first like the Markdown renderer.
- `EvidenceStore.__init__` (method) `modules/lazy_loop.py:6135` `def __init__(self, task_id)` -- Bind vault to task.
- `EvidenceStore.add` (method) `modules/lazy_loop.py:6144` `def add(self, finding_id, kind, body)` -- Attach evidence to a finding and return the record.
- `EvidenceStore.verify` (method) `modules/lazy_loop.py:6161` `def verify(self)` -- Return ids whose body fails the sha256 integrity check.
- `EvidenceStore.gc` (method) `modules/lazy_loop.py:6170` `def gc(self, valid_findings)` -- Drop evidence for findings no longer present; returns removed.
- `EvidenceStore.for_finding` (method) `modules/lazy_loop.py:6186` `def for_finding(self, finding_id)` -- Return evidence attached to one finding.
- `EvidenceStore.read` (method) `modules/lazy_loop.py:6190` `def read(self, evidence_id, offset, length)` -- Read one evidence body in bounded byte ranges.
- `EvidenceStore.export` (method) `modules/lazy_loop.py:6227` `def export(self, path)` -- Dump vault to a file for the report pipeline.
- `Notifier.__init__` (method) `modules/lazy_loop.py:6238` `def __init__(self, store)` -- Bind optional channel config from task store.
- `Notifier.channels` (method) `modules/lazy_loop.py:6242` `def channels(self)` -- Return configured channels (empty = log only).
- `Notifier.add_channel` (method) `modules/lazy_loop.py:6250` `def add_channel(self, kind, target, min_severity, extra)` -- Register a channel: log|webhook|file|slack|email with severity floor.
- `Notifier.remove_channel` (method) `modules/lazy_loop.py:6297` `def remove_channel(self, index)` -- Remove one channel by its 1-based list position.
- `Notifier.emit` (method) `modules/lazy_loop.py:6348` `def emit(self, task_id, event, data)` -- Fan out finding/status/task events; returns deliveries.
- `TriggerStore.__init__` (method) `modules/lazy_loop.py:6404` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/lazy_loop.py:6413` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.remove` (method) `modules/lazy_loop.py:6432` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.list` (method) `modules/lazy_loop.py:6442` `def list(self)` -- Return all triggers.
- `TriggerStore.ensure_service_trigger` (method) `modules/lazy_loop.py:6446` `def ensure_service_trigger(self)` -- Register the catalog trigger once so services fire the loop.
- `TriggerStore.due` (method) `modules/lazy_loop.py:6459` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.
- `LlmPool.__init__` (method) `modules/lazy_loop.py:6566` `def __init__(self)` -- Load member list and usage ledger paths.
- `LlmPool.members` (method) `modules/lazy_loop.py:6601` `def members(self)` -- Return configured chain in order, seeding defaults on first use.
- `LlmPool.add_member` (method) `modules/lazy_loop.py:6606` `def add_member(self, name, model, priority)` -- Append a chain member backed by llm_factory at call time.
- `LlmPool.remove_member` (method) `modules/lazy_loop.py:6615` `def remove_member(self, name)` -- Drop a chain member.
- `LlmPool.set_priority` (method) `modules/lazy_loop.py:6625` `def set_priority(self, name, priority)` -- Change one member's failover rank, keeping the rest untouched.
- `LlmPool.usage` (method) `modules/lazy_loop.py:6638` `def usage(self)` -- Return per-member call ledger like llm_usage.
- `LlmPool.complete` (method) `modules/lazy_loop.py:6730` `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` -- Fail over across members; empty string when no backend answers.
- `LlmPool.health` (method) `modules/lazy_loop.py:6895` `def health(self)` -- Return per-member health state for lazy_llm health.
- `LlmPool.context_budget` (method) `modules/lazy_loop.py:6906` `def context_budget(self)` -- Return the prompt context character budget (default 2000).
- `LlmPool.record_raw` (method) `modules/lazy_loop.py:6911` `def record_raw(self)` -- Return whether raw prompt/response recording is enabled.
- `LlmPool.set_record_raw` (method) `modules/lazy_loop.py:6916` `def set_record_raw(self, enabled)` -- Toggle raw prompt/response recording in the pool ledger.
- `LlmPool.raw_entries` (method) `modules/lazy_loop.py:6923` `def raw_entries(self, limit)` -- Return the most recent raw LLM exchanges.
- `LlmPool.set_context_budget` (method) `modules/lazy_loop.py:6954` `def set_context_budget(self, chars)` -- Persist the prompt context character budget.
- `ToolCatalog.__init__` (method) `modules/lazy_loop.py:6972` `def __init__(self)` -- Load binding table.
- `ToolCatalog.bindings` (method) `modules/lazy_loop.py:6989` `def bindings(self, agent)` -- Return bindings for one agent or the whole table.
- `ToolCatalog.bind` (method) `modules/lazy_loop.py:6994` `def bind(self, agent, tool)` -- Opt a tool into an agent lane.
- `ToolCatalog.unbind` (method) `modules/lazy_loop.py:7003` `def unbind(self, agent, tool)` -- Remove a tool from an agent lane.
- `SideQuestions.ask` (method) `modules/lazy_loop.py:7023` `def ask(self, task_id, question, pool, session)` -- Answer from graph overview + recent trace within a char budget.
- `SideQuestions.history` (method) `modules/lazy_loop.py:7069` `def history(self, task_id, session, limit)` -- Return persisted side exchanges, optionally one session only.
- `SideQuestions.sessions` (method) `modules/lazy_loop.py:7077` `def sessions(self, task_id)` -- Return side-question session names for a task.
- `CompanyScope.__init__` (method) `modules/lazy_loop.py:7090` `def __init__(self)` -- Load company table.
- `CompanyScope.add` (method) `modules/lazy_loop.py:7098` `def add(self, name, scope)` -- Register a company with an optional scope pattern.
- `CompanyScope.list` (method) `modules/lazy_loop.py:7107` `def list(self)` -- Return companies with asset counts.
- `CompanyScope.match` (method) `modules/lazy_loop.py:7111` `def match(self, value)` -- Return companies whose scope substring hits the value.
- `TaskArchive.save` (method) `modules/lazy_loop.py:7120` `def save(self, task_id)` -- Snapshot task record + graph + activity tail into one archive.
- `TaskArchive.list` (method) `modules/lazy_loop.py:7141` `def list(self)` -- Return archive snapshots with task + node counts.
- `TaskArchive.restore` (method) `modules/lazy_loop.py:7163` `def restore(self, path)` -- Restore one archive as a NEW task; returns the new task id.
- `TaskArchive.stats` (method) `modules/lazy_loop.py:7230` `def stats(self)` -- Aggregate counts across archives like archive aggregate stats.
- `TaskTemplate.__init__` (method) `modules/lazy_loop.py:7239` `def __init__(self)` -- Bind template table.
- `TaskTemplate.list` (method) `modules/lazy_loop.py:7247` `def list(self)` -- Return all templates.
- `TaskTemplate.add` (method) `modules/lazy_loop.py:7251` `def add(self, name, goal)` -- Register a template; names are unique (overwrite on clash).
- `TaskTemplate.remove` (method) `modules/lazy_loop.py:7261` `def remove(self, name)` -- Delete a template by name.
- `TaskTemplate.get` (method) `modules/lazy_loop.py:7271` `def get(self, name)` -- Return one template by name or None.
- `TaskCategory.__init__` (method) `modules/lazy_loop.py:7282` `def __init__(self, store)` -- Bind optional task store.
- `TaskCategory.set` (method) `modules/lazy_loop.py:7287` `def set(self, task_id, category)` -- Label a task; returns the mapping.
- `TaskCategory.get` (method) `modules/lazy_loop.py:7294` `def get(self, task_id)` -- Return the category for a task or empty string.
- `TaskCategory.list` (method) `modules/lazy_loop.py:7298` `def list(self, category)` -- Return task->category rows, optionally filtered.
- `TaskChat.say` (method) `modules/lazy_loop.py:7313` `def say(self, task_id, text, pool, session)` -- Append a human turn and answer from task context; returns both.
- `TaskChat.log` (method) `modules/lazy_loop.py:7356` `def log(self, task_id, limit, session)` -- Return recent conversation turns, optionally one session only.
- `TaskChat.sessions` (method) `modules/lazy_loop.py:7372` `def sessions(self, task_id)` -- Return session names active in a task.
- `TaskChat.clear` (method) `modules/lazy_loop.py:7381` `def clear(self, task_id, session)` -- Drop one session's turns, or the whole log when session is empty.
- `LazyLoopEngine.__init__` (method) `modules/lazy_loop.py:7436` `def __init__(self, shell)` -- Load shared stores.
- `LazyLoopEngine.bind_shell` (method) `modules/lazy_loop.py:7462` `def bind_shell(self, shell)` -- Attach the live shell so workers route auto/addon verbs via it.
- `LazyLoopEngine.ensure_target` (method) `modules/lazy_loop.py:7466` `def ensure_target(self, task_id, target, reason)` -- Register scope + asset for target like lazy_scope/lazy_asset.
- `LazyLoopEngine.orchestrate` (method) `modules/lazy_loop.py:7493` `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` -- Single entry for lazy_loop + auto_loop: create, scope, run, report.
- `LazyLoopEngine.create_task` (method) `modules/lazy_loop.py:7521` `def create_task(self, goal, description)` -- Create task, decompose goals, register scope, return summary.
- `LazyLoopEngine.spawn_task` (method) `modules/lazy_loop.py:7550` `def spawn_task(self, goal, source_task_ids, description)` -- Create a task read-only inheriting assets and findings.
- `LazyLoopEngine.list_tasks` (method) `modules/lazy_loop.py:7600` `def list_tasks(self)` -- Fleet view: every task with live intent/fact/finding counters.
- `LazyLoopEngine.pause_task` (method) `modules/lazy_loop.py:7628` `def pause_task(self, task_id, reason)` -- Pause another task from here (cross-task control).
- `LazyLoopEngine.resume_task` (method) `modules/lazy_loop.py:7639` `def resume_task(self, task_id)` -- Resume a paused task from here (cross-task control).
- `LazyLoopEngine.task_graph` (method) `modules/lazy_loop.py:7649` `def task_graph(self, task_id)` -- Graph overview of another task (get_task_graph parity).
- `LazyLoopEngine.task_findings` (method) `modules/lazy_loop.py:7655` `def task_findings(self, task_id)` -- Findings of another task with severity, status and report size.
- `LazyLoopEngine.task_traces` (method) `modules/lazy_loop.py:7674` `def task_traces(self, task_id, query, limit)` -- Worker traces of another task, keyword-filtered when asked.
- `LazyLoopEngine.task_node_detail` (method) `modules/lazy_loop.py:7683` `def task_node_detail(self, task_id, node_id)` -- Full node view of another task (get_task_node_detail parity).
- `LazyLoopEngine.update_finding_report` (method) `modules/lazy_loop.py:7689` `def update_finding_report(self, task_id, finding_id, report)` -- Write the narrative report of another task's finding.
- `LazyLoopEngine.broadcast_events` (method) `modules/lazy_loop.py:7701` `def broadcast_events(self, task_id, cursor, batch)` -- Return activity records after a line cursor (SSE resume parity).
- `LazyLoopEngine.add_hint` (method) `modules/lazy_loop.py:7734` `def add_hint(self, task_id, text)` -- Inject human steering hint read by the next planner round.
- `LazyLoopEngine.add_intent` (method) `modules/lazy_loop.py:7752` `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` -- Directly inject high-priority intent like the planner main-agent add_intent.
- `LazyLoopEngine.set_goals` (method) `modules/lazy_loop.py:7777` `def set_goals(self, task_id, specs)` -- Replace/append decomposed objectives like set_goals; wakes the task.
- `LazyLoopEngine.edit_goal` (method) `modules/lazy_loop.py:7794` `def edit_goal(self, task_id, goal_id, text)` -- Edit a goal node like the goals manager.
- `LazyLoopEngine.delete_goal` (method) `modules/lazy_loop.py:7806` `def delete_goal(self, task_id, goal_id)` -- Delete a goal node; done tasks with no goals left stay done.
- `LazyLoopEngine.preview_delete_intent` (method) `modules/lazy_loop.py:7817` `def preview_delete_intent(self, task_id, intent_id)` -- Estimate hard-delete cascade without mutating anything.
- `LazyLoopEngine.delete_intent` (method) `modules/lazy_loop.py:7840` `def delete_intent(self, task_id, intent_id, mode, reason)` -- Delete an intent in soft (fake) or hard (true) mode.
- `LazyLoopEngine.pause_intent` (method) `modules/lazy_loop.py:7985` `def pause_intent(self, task_id, intent_id)` -- Pause a runnable intent like the lazy worker interrupt.
- `LazyLoopEngine.resume_intent` (method) `modules/lazy_loop.py:8010` `def resume_intent(self, task_id, intent_id)` -- Resume a paused intent back to the claimable queue.
- `LazyLoopEngine.send_worker_message` (method) `modules/lazy_loop.py:8033` `def send_worker_message(self, task_id, intent_id, message, request_id)` -- Continue a paused worker intent with a human message.
- `LazyLoopEngine.goal_met` (method) `modules/lazy_loop.py:8081` `def goal_met(self, task_id, reason)` -- Declare the whole task complete like goal_met (weighted, audited).
- `LazyLoopEngine.record_fact` (method) `modules/lazy_loop.py:8091` `def record_fact(self, task_id, text, evidence, intent_id)` -- Operator-visible fact write like recordFact.
- `LazyLoopEngine.record_verdict` (method) `modules/lazy_loop.py:8098` `def record_verdict(self, task_id, finding_id, verdict, note)` -- Record an operator retest verdict on one finding.
- `LazyLoopEngine.run_round` (method) `modules/lazy_loop.py:8183` `def run_round(self, task_id, workers, executor, pool)` -- Run one orchestrated round invoking every subsystem in order.
- `stage_enabled` (function) `modules/lazy_loop.py:8234` `def stage_enabled(_name)`
- `LazyLoopEngine.run` (method) `modules/lazy_loop.py:8660` `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` -- Drive rounds until goals met, frontier drains, or budget exhausts.
- `LazyLoopEngine.prove_goal` (method) `modules/lazy_loop.py:8843` `def prove_goal(self, task_id, goal_id, evidence_id, reason)` -- Mark goal met with finding/fact evidence like the planner prove_goal.
- `LazyLoopEngine.delete_task` (method) `modules/lazy_loop.py:8889` `def delete_task(self, task_id)` -- Delete a task record plus every store file scoped to it.
- `LazyLoopEngine.proxy_start` (method) `modules/lazy_loop.py:8923` `def proxy_start(self, host, port, task_id, trust, upstream)` -- Start the shared recorder proxy and apply its trust environment.
- `LazyLoopEngine.proxy_stop` (method) `modules/lazy_loop.py:8959` `def proxy_stop(self)` -- Stop the recorder proxy and clear its trust environment.
- `LazyLoopEngine.proxy_status` (method) `modules/lazy_loop.py:8967` `def proxy_status(self)` -- Return recorder proxy state (running, address, CA, exchanges).
- `LazyLoopEngine.proxy_env` (method) `modules/lazy_loop.py:8973` `def proxy_env(self)` -- Return the environment overrides that route tools via proxy.
- `LazyLoopEngine.set_concurrency` (method) `modules/lazy_loop.py:8982` `def set_concurrency(self, limit)` -- Cap concurrently running tasks; 0 disables admission control.
- `LazyLoopEngine.admission_check` (method) `modules/lazy_loop.py:9003` `def admission_check(self, task_id)` -- Return whether a task may run now, queueing it when capped.
- `LazyLoopEngine.drain_queue` (method) `modules/lazy_loop.py:9022` `def drain_queue(self, max_tasks)` -- Run queued tasks FIFO while the concurrency cap allows.
- `LazyLoopEngine.ingest_proxy_traffic` (method) `modules/lazy_loop.py:9050` `def ingest_proxy_traffic(self, task_id, limit)` -- Mirror new recorder exchanges into the task traffic log.
- `LazyLoopEngine.search_proxy_body` (method) `modules/lazy_loop.py:9104` `def search_proxy_body(self, task_id, query, limit)` -- Full-text search proxy bodies scoped to one task's exchanges.
- `LazyLoopEngine.export_task_traffic` (method) `modules/lazy_loop.py:9196` `def export_task_traffic(self, task_id)` -- Export the task's proxy exchanges next to its archive.
- `LazyLoopEngine.export_evidence` (method) `modules/lazy_loop.py:9225` `def export_evidence(self, task_id, dest)` -- Freeze every task artefact into a hash-manifested zip package.
- `LazyLoopEngine.export_findings_report` (method) `modules/lazy_loop.py:9284` `def export_findings_report(self, task_id, path, fmt)` -- Render the severity-ranked report to Markdown, JSON or CSV.
- `LazyLoopEngine.status` (method) `modules/lazy_loop.py:9380` `def status(self, task_id)` -- Return full inspectable state for one task.
- `LazyLoopEngine.graph_overview` (method) `modules/lazy_loop.py:9400` `def graph_overview(self, task_id)` -- Return planner-facing overview plus coverage and scope.
- `LazyLoopEngine.broadcast` (method) `modules/lazy_loop.py:9462` `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` -- Paginated exploration timeline like the lazy broadcast board.
- `LazyLoopEngine.loop_graph` (method) `modules/lazy_loop.py:9586` `def loop_graph(self, task_id)` -- Return task graphs as ForceGraph-ready nodes/links.
- `LazyLoopEngine.graph_context` (method) `modules/lazy_loop.py:9655` `def graph_context(self, task_id, top)` -- Rank exploration topology to steer planner actions.

## modules/lazy_mentions.py
Depends on: `modules/lazy_loop.py`
Imported by: `cli/commands/lazyloop.py`, `lazyc2.py`, `skills/lazyown_mcp.py`, `tests/test_security_codeql_batch.py`
- `search_mentions_page` (function) `modules/lazy_mentions.py:193` `def search_mentions_page(kind, query, cursor)` -- Search one scroll page of mention candidates.
- `parse_mentions` (function) `modules/lazy_mentions.py:237` `def parse_mentions(message)` -- Parse @[kind#id] tokens trusting type plus numeric id only.
- `compose_message` (function) `modules/lazy_mentions.py:268` `def compose_message(message)` -- Append server-read snapshots for referenced records as data.

## modules/lazy_orchestrator_feedback.py
Depends on: `modules/lazy_cli_bridge.py`, `modules/lazy_intel.py`
Imported by: `modules/auto_registry.py`, `modules/lazy_loop.py`, `tests/test_loop_supervision.py`
- `adjust_from_usage` (function) `modules/lazy_orchestrator_feedback.py:61` `def adjust_from_usage(limit)` -- Fold routing outcomes into per-(phase, stack, verb) success priors.
- `verb_prior` (function) `modules/lazy_orchestrator_feedback.py:162` `def verb_prior(phase, verb, stack)` -- Return the success prior for one (phase, stack, verb) triple.
- `rank_verbs` (function) `modules/lazy_orchestrator_feedback.py:189` `def rank_verbs(phase, verbs, stack)` -- Order verbs by learned success rate, stable for cold verbs.
- `order_steps` (function) `modules/lazy_orchestrator_feedback.py:213` `def order_steps(steps, stack)` -- Reorder resolved step lines by stack-aware verb priors.
- `export_dataset` (function) `modules/lazy_orchestrator_feedback.py:238` `def export_dataset(out, limit)` -- Export instruction-tuning rows joined from decisions + outcomes.

## modules/lazy_proxy.py
Depends on: `core/logging.py`, `modules/backdoor/server.c`, `modules/traffic_recorder.py`
Imported by: `cli/commands/lazyops.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_security_codeql_batch.py`
- `detect_trust_target` (function) `modules/lazy_proxy.py:322` `def detect_trust_target()` -- Return the first existing system trust anchor directory and refresh command.
- `ca_trusted` (function) `modules/lazy_proxy.py:330` `def ca_trusted(ca_path)` -- Return True when the system anchor already holds this CA.
- `detect_nss_profiles` (function) `modules/lazy_proxy.py:349` `def detect_nss_profiles()` -- Return user NSS database directories (Firefox profiles + Chrome).
- `install_ca_nss` (function) `modules/lazy_proxy.py:364` `def install_ca_nss(ca_path, runner, profiles)` -- Install the recorder CA into user NSS databases via certutil.
- `install_ca_trust` (function) `modules/lazy_proxy.py:404` `def install_ca_trust(ca_path, runner)` -- Install the recorder CA into the system trust store.
- `CertificateAuthority.__init__` (method) `modules/lazy_proxy.py:458` `def __init__(self, pki_dir)` -- Load or create the CA under ``pki_dir``.
- `CertificateAuthority.context_for` (method) `modules/lazy_proxy.py:568` `def context_for(self, host)` -- Return the server TLS context for one host, generating on miss.
- `RecorderServer.__init__` (method) `modules/lazy_proxy.py:611` `def __init__(self, address, handler)`
- `RecorderServer.handle_error` (method) `modules/lazy_proxy.py:618` `def handle_error(self, request, client_address)` -- Silence client-side connection noise instead of tracebacks.
- `ProxyController.__init__` (method) `modules/lazy_proxy.py:638` `def __init__(self)` -- Prepare state; nothing binds until :meth:`start`.
- `ProxyController.start` (method) `modules/lazy_proxy.py:651` `def start(self, host, port, task_id, traffic_dir, upstream)` -- Bind the recorder proxy; idempotent while already running.
- `ProxyController.stop` (method) `modules/lazy_proxy.py:696` `def stop(self)` -- Shut the proxy down; safe when it was never started.
- `ProxyController.status` (method) `modules/lazy_proxy.py:712` `def status(self)` -- Report running state, address, CA path and exchange count.
- `ProxyController.recorder` (method) `modules/lazy_proxy.py:734` `def recorder(self)` -- Return the live recorder for ingestion, or None when stopped.
- `ProxyController.ca_path` (method) `modules/lazy_proxy.py:738` `def ca_path(self)` -- Return the CA certificate path for trust-store wiring.
- `ProxyHandler.log_message` (method) `modules/lazy_proxy.py:753` `def log_message(self, fmt)` -- Silence per-request logging; the recorder is the audit trail.
- `ProxyHandler.do_CONNECT` (method) `modules/lazy_proxy.py:757` `def do_CONNECT(self)` -- Terminate TLS for a CONNECT tunnel and record inner requests.
- `ProxyHandler.do_GET` (method) `modules/lazy_proxy.py:809` `def do_GET(self)` -- Forward every plain HTTP method through one path.
- `get_proxy` (function) `modules/lazy_proxy.py:1151` `def get_proxy()` -- Return the process-wide recorder proxy controller.
- `env_for_ca` (function) `modules/lazy_proxy.py:1160` `def env_for_ca(ca_path, host, port)` -- Build the environment overrides that route tools through the proxy.
- `apply_env` (function) `modules/lazy_proxy.py:1176` `def apply_env(ca_path, host, port)` -- Apply proxy env vars, returning the previous values for restore.
- `restore_env` (function) `modules/lazy_proxy.py:1183` `def restore_env(previous)` -- Restore environment values captured by :func:`apply_env`.

## modules/lazy_rbac.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`
- `Role.valid_roles` (method) `modules/lazy_rbac.py:62` `def valid_roles(cls)`
- `RBACUser.to_dict` (method) `modules/lazy_rbac.py:136` `def to_dict(self)`
- `RBACUser.from_dict` (method) `modules/lazy_rbac.py:140` `def from_dict(cls, data)`
- `RBACUser.get_role` (method) `modules/lazy_rbac.py:164` `def get_role(self)`
- `RBACUser.has_permission` (method) `modules/lazy_rbac.py:170` `def has_permission(self, permission)`
- `RBACUser.can_manage_role` (method) `modules/lazy_rbac.py:174` `def can_manage_role(self, target_role)` -- Check if this user can assign/manage the given role.
- `RBACUser.get_mfa_provisioning_uri` (method) `modules/lazy_rbac.py:182` `def get_mfa_provisioning_uri(self)`
- `RBACUser.verify_totp` (method) `modules/lazy_rbac.py:187` `def verify_totp(self, token)`
- `RBACUser.verify_recovery_code` (method) `modules/lazy_rbac.py:192` `def verify_recovery_code(self, code)`
- `RBACUser.consume_recovery_code` (method) `modules/lazy_rbac.py:200` `def consume_recovery_code(self, code)`
- `RBACStore.__init__` (method) `modules/lazy_rbac.py:213` `def __init__(self, users_path)`
- `RBACStore.load_all` (method) `modules/lazy_rbac.py:245` `def load_all(self)`
- `RBACStore.find_by_id` (method) `modules/lazy_rbac.py:249` `def find_by_id(self, user_id)`
- `RBACStore.find_by_username` (method) `modules/lazy_rbac.py:255` `def find_by_username(self, username)`
- `RBACStore.save` (method) `modules/lazy_rbac.py:261` `def save(self, user)`
- `RBACStore.create_user` (method) `modules/lazy_rbac.py:274` `def create_user(self, username, password_hash, role, tenant_id)`
- `RBACStore.delete_user` (method) `modules/lazy_rbac.py:295` `def delete_user(self, user_id)`
- `RBACStore.update_role` (method) `modules/lazy_rbac.py:304` `def update_role(self, user_id, new_role)`
- `RBACStore.enable_mfa` (method) `modules/lazy_rbac.py:314` `def enable_mfa(self, user_id)`
- `RBACStore.disable_mfa` (method) `modules/lazy_rbac.py:324` `def disable_mfa(self, user_id)`
- `RBACStore.consume_recovery_code` (method) `modules/lazy_rbac.py:334` `def consume_recovery_code(self, user_id, code)`
- `RBACStore.ensure_admin` (method) `modules/lazy_rbac.py:343` `def ensure_admin(self, username, password_hash)` -- Ensure at least one admin exists, creating one if needed.
- `TenantConfig.from_payload` (method) `modules/lazy_rbac.py:377` `def from_payload(cls, tenant_id, name, payload_path)`
- `TenantConfig.to_dict` (method) `modules/lazy_rbac.py:386` `def to_dict(self)`
- `TenantConfig.from_dict` (method) `modules/lazy_rbac.py:390` `def from_dict(cls, data)`
- `TenantManager.__init__` (method) `modules/lazy_rbac.py:397` `def __init__(self, payloads_dir, config_path, default_payload)`
- `TenantManager.list_tenants` (method) `modules/lazy_rbac.py:431` `def list_tenants(self)`
- `TenantManager.get_active` (method) `modules/lazy_rbac.py:434` `def get_active(self)`
- `TenantManager.get_active_payload_path` (method) `modules/lazy_rbac.py:439` `def get_active_payload_path(self)`
- `TenantManager.get_active_sessions_dir` (method) `modules/lazy_rbac.py:445` `def get_active_sessions_dir(self)`
- `TenantManager.get_payload_for_tenant` (method) `modules/lazy_rbac.py:451` `def get_payload_for_tenant(self, tenant_id)`
- `TenantManager.create_tenant` (method) `modules/lazy_rbac.py:457` `def create_tenant(self, name, base_payload)`
- `TenantManager.switch_tenant` (method) `modules/lazy_rbac.py:486` `def switch_tenant(self, tenant_id)`
- `TenantManager.delete_tenant` (method) `modules/lazy_rbac.py:495` `def delete_tenant(self, tenant_id)`
- `TenantManager.ensure_default_tenant` (method) `modules/lazy_rbac.py:504` `def ensure_default_tenant(self)`
- `init_rbac_store` (function) `modules/lazy_rbac.py:523` `def init_rbac_store(users_path)`
- `init_tenant_manager` (function) `modules/lazy_rbac.py:527` `def init_tenant_manager(payloads_dir, config_path, default_payload)`
- `require_role` (function) `modules/lazy_rbac.py:539` `def require_role()` -- Flask decorator: require one of the given roles.
- `decorator` (function) `modules/lazy_rbac.py:542` `def decorator(f)`
- `decorated` (function) `modules/lazy_rbac.py:544` `def decorated()`
- `require_permission` (function) `modules/lazy_rbac.py:565` `def require_permission()` -- Flask decorator: require specific permissions.
- `decorator` (function) `modules/lazy_rbac.py:568` `def decorator(f)`
- `decorated` (function) `modules/lazy_rbac.py:570` `def decorated()`
- `require_mfa` (function) `modules/lazy_rbac.py:596` `def require_mfa(f)` -- Decorator that enforces MFA before accessing protected routes.
- `decorated` (function) `modules/lazy_rbac.py:600` `def decorated()`
- `get_rbac_store` (function) `modules/lazy_rbac.py:639` `def get_rbac_store()`
- `set_rbac_store` (function) `modules/lazy_rbac.py:643` `def set_rbac_store(store)`
- `get_tenant_manager` (function) `modules/lazy_rbac.py:648` `def get_tenant_manager()`
- `set_tenant_manager` (function) `modules/lazy_rbac.py:655` `def set_tenant_manager(tm)`
- `check_cli_permission` (function) `modules/lazy_rbac.py:660` `def check_cli_permission(username, permission)` -- Check if a CLI user has the given permission.
- `get_user_role` (function) `modules/lazy_rbac.py:672` `def get_user_role(username)`
- `generate_mfa_qr_url` (function) `modules/lazy_rbac.py:680` `def generate_mfa_qr_url(secret, username)` -- Generate a QR code data URI for MFA setup (local, no external API).
- `generate_qr_svg` (function) `modules/lazy_rbac.py:689` `def generate_qr_svg(data)` -- Generate an SVG QR code image from text data.
- `gf_mul` (function) `modules/lazy_rbac.py:927` `def gf_mul(a, b)`

## modules/lazy_roles.py
Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`
- `list_roles` (function) `modules/lazy_roles.py:100` `def list_roles()` -- Return every Lazy role descriptor.
- `role_prompt` (function) `modules/lazy_roles.py:109` `def role_prompt(role, goal, context)` -- Build the system prompt for one role.
- `roles_for_phase` (function) `modules/lazy_roles.py:134` `def roles_for_phase(phase)` -- Return role names serving one kill-chain phase.
- `conformance` (function) `modules/lazy_roles.py:154` `def conformance(role)` -- Probe every pool member with role prompts, like provider conformance.

## modules/lazy_runner.py
Depends on: `cli/lazy_monitor.py`, `core/autonomous.py`, `core/terminal_guard.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/loop_progress.py`, `utils.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/mcp_bridge.py`, `cli/lazy_monitor.py`, `modules/tools/loop_smoke.py`, `tests/test_lazy_runner.py`
- `ThreadStdoutRouter.__init__` (method) `modules/lazy_runner.py:51` `def __init__(self, main_stream, spool)` -- Bind the real stream and the worker spool queue.
- `ThreadStdoutRouter.write` (method) `modules/lazy_runner.py:57` `def write(self, data)` -- Route main-thread writes to the terminal, worker writes to spool.
- `ThreadStdoutRouter.flush` (method) `modules/lazy_runner.py:68` `def flush(self)` -- Flush the real stream; the spool needs no flushing.
- `ThreadStdoutRouter.encoding` (method) `modules/lazy_runner.py:76` `def encoding(self)` -- Report the real stream encoding.
- `ThreadStdoutRouter.isatty` (method) `modules/lazy_runner.py:80` `def isatty(self)` -- Report whether the real stream is a terminal.
- `LoopRunConfig.clamped` (method) `modules/lazy_runner.py:107` `def clamped(self)` -- Clamp numeric knobs to the supported operating range.
- `parse_loop_line` (function) `modules/lazy_runner.py:137` `def parse_loop_line(line)` -- Parse one loop command line into a :class:`LoopRunConfig`.
- `build_executor` (function) `modules/lazy_runner.py:225` `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` -- Build the worker executor: shell verbs, custom tools, safe bash.
- `report_result` (function) `modules/lazy_runner.py:356` `def report_result(result)` -- Print the final outcome of one loop run.
- `stream` (function) `modules/lazy_runner.py:409` `def stream(text)`
- `run_loop` (function) `modules/lazy_runner.py:691` `def run_loop(shell, params, config)` -- Execute one complete loop run and return its summary.


Next: [API_p13.md](API_p13.md)
