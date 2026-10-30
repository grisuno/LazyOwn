# API (page 14 of 25)
Previous: [API_p13.md](API_p13.md)

## modules/lazy_loop.py
Depends on: `core/config.py`, `core/crypto.py`, `core/hardening.py`, `core/logging.py`, `core/process.py`, `modules/__init__.py`, `modules/auto_loop_memory.py`, `modules/auto_registry.py`, `modules/autonomous_exploit_engine.py`, `modules/custom_tools.py`, `modules/defense_stages.py`, `modules/digest.py`, `modules/finding_lifecycle.py`, `modules/guardrails/__init__.py`, `modules/harness.py`, `modules/intercept.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_hostscore.py`, `modules/lazy_installer.py`, `modules/lazy_intel.py`, `modules/lazy_ledger.py`, `modules/lazy_orchestrator_feedback.py`, `modules/lazy_reaper.py`, `modules/lazy_roles.py`, `modules/lazy_skills.py`, `modules/lazy_world_diff.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/loop_ai_bridge.py`, `modules/loop_guardrails.py`, `modules/loop_triggers.py`, `modules/mediation/__init__.py`, `modules/module_registry.py`, `modules/notify.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/progress_ledger.py`, `modules/reaction_bridge.py`, `modules/reactive_engine.py`, `modules/selfupdate.py`, `modules/sinks/findings.py`, `modules/traffic_recorder.py`, `modules/trigger_policy.py`, `modules/world_model.py`, `skills/lazyown_policy.py`, `utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/lazy_orchestrator.py`, `cli/retry_support.py`, `lazyc2.py`, `lazyown.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_engine.py`, `modules/lazy_ledger.py`, `modules/lazy_mentions.py`, `modules/lazy_osinfer.py`, `modules/lazy_reaper.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/loop_triggers.py`, `modules/mediation/chain_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/reaction_bridge.py`, `modules/sinks/chain_feed.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_asset_gate.py`, `tests/test_auto_crypto.py`, `tests/test_failure_memory_veto.py`, `tests/test_guardrails.py`, `tests/test_harness_mode.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_ledger.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_lazy_worker_safety.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cli_catalog.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_nmap_guard.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_store_race.py`, `tests/test_loop_supervision.py`, `tests/test_loop_trigger_hints.py`, `tests/test_loop_worker_traces.py`, `tests/test_mcp_auto_loop_wrapper.py`, `tests/test_module_registry_bridge.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_triggers.py`, `tests/test_orchestrator_yaml.py`, `tests/test_pi_leg.py`, `tests/test_policy_planner_signal.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_codeql_batch.py`, `tests/test_session_brief.py`, `tests/test_sink_chain_feed.py`, `tests/test_trigger_policy.py`, `tests/test_world_diff_retest.py`
- `plausible_command` (function) `modules/lazy_loop.py:168` `def plausible_command(command)` -- Reject obvious hallucinations such as ``nmap --block``.
- `repair_worker_command` (function) `modules/lazy_loop.py:289` `def repair_worker_command(command, target)` -- Normalize one LLM-proposed worker command.
- `loop_exiting` (function) `modules/lazy_loop.py:419` `def loop_exiting()` -- Return True once the shell is tearing the loop runtime down.
- `arm_exit_watchdog` (function) `modules/lazy_loop.py:436` `def arm_exit_watchdog(seconds)` -- Guarantee process death even with threads stuck in socket reads.
- `scrub_secrets` (function) `modules/lazy_loop.py:459` `def scrub_secrets(text)` -- Mask API keys/tokens before a string reaches logs or the panel.
- `wake_task` (function) `modules/lazy_loop.py:555` `def wake_task(task_id)` -- Signal a running engine that new work landed for its task.
- `register_worker` (function) `modules/lazy_loop.py:589` `def register_worker(worker)` -- Track a live Worker so shell exit can close its side channels.
- `unregister_worker` (function) `modules/lazy_loop.py:595` `def unregister_worker(worker)` -- Drop a finished Worker from the shutdown registry.
- `shutdown_loop_runtime` (function) `modules/lazy_loop.py:601` `def shutdown_loop_runtime(reason)` -- Tear down every loop-owned resource; safe on any exit path.
- `task_llm_chain` (function) `modules/lazy_loop.py:816` `def task_llm_chain(store, task_id)` -- Return the per-task LLM chain members (empty when unbound).
- `parse_judge_output` (function) `modules/lazy_loop.py:826` `def parse_judge_output(raw)` -- Parse strict judge JSON demanding decision and comment.
- `judge_command` (function) `modules/lazy_loop.py:854` `def judge_command(command, background, fail_action)` -- Ask the pool for a guard verdict, applying the configured fail policy.
- `AssetGraph.__init__` (method) `modules/lazy_loop.py:947` `def __init__(self)` -- Load persisted assets or start empty.
- `AssetGraph.dedupe_key` (method) `modules/lazy_loop.py:965` `def dedupe_key(self, kind, value, parent_id)` -- Compute program-owned dedupe key for an asset.
- `AssetGraph.insert` (method) `modules/lazy_loop.py:969` `def insert(self, kind, value, parent_id, meta, task_id)` -- Insert asset or return existing node with same dedupe key.
- `AssetGraph.get` (method) `modules/lazy_loop.py:999` `def get(self, asset_id)` -- Return asset by id or None.
- `AssetGraph.list` (method) `modules/lazy_loop.py:1003` `def list(self, kind)` -- List assets optionally filtered by kind.
- `AssetGraph.mark_tested` (method) `modules/lazy_loop.py:1010` `def mark_tested(self, asset_id)` -- Flag asset as tested by a worker intent.
- `AssetGraph.coverage` (method) `modules/lazy_loop.py:1020` `def coverage(self, scope)` -- Compute tested/total coverage, optionally scoped.
- `AssetGraph.scoped` (method) `modules/lazy_loop.py:1036` `def scoped(self, scope, kind)` -- List assets owned by the task scope via ownership matching.
- `AssetGraph.untested` (method) `modules/lazy_loop.py:1049` `def untested(self, limit)` -- Return oldest untested assets up to limit.
- `AssetGraph.coverage_for` (method) `modules/lazy_loop.py:1054` `def coverage_for(self, graph, scope)` -- Compute task-scoped coverage like the planner graph_overview.
- `AssetGraph.untested_for` (method) `modules/lazy_loop.py:1082` `def untested_for(self, graph, scope, limit)` -- Return scope-filtered assets not yet covered by this task.
- `ExplorationGraph.__init__` (method) `modules/lazy_loop.py:1110` `def __init__(self, task_id)` -- Load task graph or start empty.
- `ExplorationGraph.add_node` (method) `modules/lazy_loop.py:1144` `def add_node(self, kind, text, state, priority, meta)` -- Append node and return it.
- `ExplorationGraph.get` (method) `modules/lazy_loop.py:1172` `def get(self, node_id)` -- Return node by id or None.
- `ExplorationGraph.persist` (method) `modules/lazy_loop.py:1176` `def persist(self)` -- Persist in-memory node/edge state to disk (public write path).
- `ExplorationGraph.set_node_state` (method) `modules/lazy_loop.py:1180` `def set_node_state(self, node_id, state)` -- Transition node state, stamp ``updated`` and persist.
- `ExplorationGraph.set_node_meta` (method) `modules/lazy_loop.py:1199` `def set_node_meta(self, node_id, meta)` -- Replace one node's metadata mapping, stamp ``updated``, persist.
- `ExplorationGraph.set_state` (method) `modules/lazy_loop.py:1218` `def set_state(self, node_id, state)` -- Transition node state and persist.
- `ExplorationGraph.add_edge` (method) `modules/lazy_loop.py:1229` `def add_edge(self, src, dst, kind)` -- Link two existing nodes.
- `ExplorationGraph.anchor` (method) `modules/lazy_loop.py:1242` `def anchor(self, node_id, asset_id)` -- Anchor exploration node to a concrete asset.
- `ExplorationGraph.anchors_for` (method) `modules/lazy_loop.py:1253` `def anchors_for(self, node_id)` -- Return asset ids anchored to node.
- `ExplorationGraph.anchored_nodes` (method) `modules/lazy_loop.py:1257` `def anchored_nodes(self, asset_id)` -- Return exploration node ids anchored to asset.
- `ExplorationGraph.list` (method) `modules/lazy_loop.py:1261` `def list(self, kind, state)` -- List nodes optionally filtered by kind/state.
- `ExplorationGraph.children` (method) `modules/lazy_loop.py:1270` `def children(self, node_id, kind)` -- Return destination ids of outgoing edges.
- `ExplorationGraph.parents` (method) `modules/lazy_loop.py:1277` `def parents(self, node_id, kind)` -- Return source ids of incoming edges.
- `ExplorationGraph.overview` (method) `modules/lazy_loop.py:1284` `def overview(self)` -- Return planner-facing state summary like graph overview.
- `ExplorationGraph.reload` (method) `modules/lazy_loop.py:1307` `def reload(self)` -- Reload graph from disk, discarding in-memory state.
- `ExplorationGraph.compare_and_claim` (method) `modules/lazy_loop.py:1331` `def compare_and_claim(self, node_id)` -- CAS claim: reload, verify still open, then mark running.
- `ExplorationGraph.finding_signature` (method) `modules/lazy_loop.py:1359` `def finding_signature(self, text)` -- Normalize finding text into dedupe signature.
- `ExplorationGraph.has_finding` (method) `modules/lazy_loop.py:1365` `def has_finding(self, text)` -- Return existing finding with same signature or None.
- `ExplorationGraph.node_detail` (method) `modules/lazy_loop.py:1375` `def node_detail(self, node_id)` -- Full node view: text, state, meta, edges, anchors, trace tail.
- `ExplorationGraph.list_facts` (method) `modules/lazy_loop.py:1391` `def list_facts(self, query, limit, hot_full)` -- Keyword-filtered facts like list_facts.
- `ExplorationGraph.record_fact` (method) `modules/lazy_loop.py:1407` `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` -- Worker fact write like recordFact: deduped, anchored, done.
- `Frontier.__init__` (method) `modules/lazy_loop.py:1432` `def __init__(self, graph)` -- Bind frontier to a task graph.
- `Frontier.pending` (method) `modules/lazy_loop.py:1437` `def pending(self)` -- Return pending intents ordered by priority then id.
- `Frontier.claim_next` (method) `modules/lazy_loop.py:1442` `def claim_next(self)` -- Atomically claim highest-priority pending intent (cross-process CAS).
- `ActivityLog.__init__` (method) `modules/lazy_loop.py:1460` `def __init__(self, task_id)` -- Bind log to task.
- `ActivityLog.emit` (method) `modules/lazy_loop.py:1465` `def emit(self, worker, kind, text, intent_id, tool_use_id)` -- Append one activity record and return it.
- `ActivityLog.read` (method) `modules/lazy_loop.py:1490` `def read(self, limit)` -- Return most recent records up to limit.
- `ActivityLog.for_intent` (method) `modules/lazy_loop.py:1504` `def for_intent(self, intent_id)` -- Return records for one intent.
- `ActivityLog.trace` (method) `modules/lazy_loop.py:1508` `def trace(self, intent_id, query, step_id, limit)` -- Work-scoped trace view like get_worker_trace.
- `ActivityLog.search_all` (method) `modules/lazy_loop.py:1546` `def search_all(self, query, limit)` -- Global keyword search across every work in this task.
- `ActivityLog.search` (method) `modules/lazy_loop.py:1576` `def search(self, query, exclude_intent)` -- Search worker traces by keyword, excluding one intent like the planner.
- `TrafficLog.__init__` (method) `modules/lazy_loop.py:1593` `def __init__(self, task_id)` -- Bind log to task or global stream.
- `TrafficLog.record` (method) `modules/lazy_loop.py:1598` `def record(self, kind, command, output, meta)` -- Append one traffic record and return it.
- `TrafficLog.read` (method) `modules/lazy_loop.py:1620` `def read(self, limit)` -- Return most recent traffic records.
- `TrafficLog.search` (method) `modules/lazy_loop.py:1634` `def search(self, query, limit)` -- Full-text search over command/output like traffic_search.
- `TrafficLog.search_host` (method) `modules/lazy_loop.py:1645` `def search_host(self, host, port, limit)` -- Port-aware host search: same-host/different-port rows never mix.
- `TrafficLog.get` (method) `modules/lazy_loop.py:1673` `def get(self, digest)` -- Fetch one exchange by digest like traffic_get.
- `TrafficLog.recorder_body` (method) `modules/lazy_loop.py:1680` `def recorder_body(self, digest)` -- Return stored request/response bodies for one proxy exchange.
- `TrafficLog.recorder_blob` (method) `modules/lazy_loop.py:1709` `def recorder_blob(self, digest, part, offset, length)` -- Read a proxy body in ranges like the blob API.
- `TrafficLog.templates` (method) `modules/lazy_loop.py:1740` `def templates(self, limit)` -- Group exchanges by URL-template with counts like the proxy index.
- `TrafficLog.by_template` (method) `modules/lazy_loop.py:1749` `def by_template(self, template, limit)` -- Return exchanges matching one template substring.
- `TrafficLog.bind` (method) `modules/lazy_loop.py:1754` `def bind(self, finding_id, digest, graph, role, note)` -- Attach traffic digest to a finding like bind_finding_traffic.
- `TrafficLog.evidence` (method) `modules/lazy_loop.py:1802` `def evidence(self, finding_id, graph)` -- Return a finding's traffic evidences in display order.
- `TrafficLog.reorder_evidence` (method) `modules/lazy_loop.py:1811` `def reorder_evidence(self, finding_id, digests, graph)` -- Sort a finding's evidences; unlisted ones keep their tail order.
- `TrafficLog.export` (method) `modules/lazy_loop.py:1825` `def export(self, path, limit)` -- Dump recent exchanges to a JSON file like traffic archive export.
- `TrafficLog.archive` (method) `modules/lazy_loop.py:1832` `def archive(self, label)` -- Snapshot traffic stream into sessions/lazy/traffic_archive_*.
- `TrafficLog.clear` (method) `modules/lazy_loop.py:1838` `def clear(self)` -- Drop the traffic stream, returning the discarded record count.
- `Guard.__init__` (method) `modules/lazy_loop.py:1851` `def __init__(self, task_id)` -- Load rules and audit trail.
- `Guard.add_rule` (method) `modules/lazy_loop.py:1877` `def add_rule(self, pattern, action, reason, priority)` -- Register an intercept rule; higher priority evaluates first.
- `Guard.remove_rule` (method) `modules/lazy_loop.py:1888` `def remove_rule(self, pattern)` -- Delete rules matching pattern exactly.
- `Guard.set_judge` (method) `modules/lazy_loop.py:1897` `def set_judge(self, enabled, fail_action)` -- Enable/disable the LLM judge fallback for unmatched commands.
- `Guard.check` (method) `modules/lazy_loop.py:1919` `def check(self, tool, command, tool_use_id, source, intent_id)` -- Evaluate tool call and audit it, returning allow/ask/deny.
- `Guard.audit` (method) `modules/lazy_loop.py:1971` `def audit(self, limit, action, source, query)` -- Return recent audit entries with optional status/source/text filters.
- `Guard.lookup` (method) `modules/lazy_loop.py:1999` `def lookup(self, tool_use_id)` -- Jump to the exact execution behind an approval row.
- `Guard.stats` (method) `modules/lazy_loop.py:2041` `def stats(self)` -- Attribution counters over the audit trail.
- `AssetGate.__init__` (method) `modules/lazy_loop.py:2198` `def __init__(self, task_id)` -- Bind global list plus optional per-task lists.
- `AssetGate.add` (method) `modules/lazy_loop.py:2225` `def add(self, kind, pattern, note, action)` -- Register a block (global or task) or allow (task only) rule.
- `AssetGate.remove` (method) `modules/lazy_loop.py:2246` `def remove(self, rule_id, action)` -- Delete a rule by id; returns True when something was removed.
- `AssetGate.list` (method) `modules/lazy_loop.py:2264` `def list(self)` -- Return global block plus per-task block/allow rules.
- `AssetGate.evaluate` (method) `modules/lazy_loop.py:2268` `def evaluate(self, target)` -- Gate one target: allowed flag plus human-readable reason.
- `Budget.__init__` (method) `modules/lazy_loop.py:2286` `def __init__(self, store)` -- Bind budget counters to task store.
- `Budget.limits` (method) `modules/lazy_loop.py:2290` `def limits(self, task_id)` -- Return effective limits for task.
- `Budget.set_limits` (method) `modules/lazy_loop.py:2301` `def set_limits(self, task_id)` -- Persist budget limits for task.
- `Budget.usage` (method) `modules/lazy_loop.py:2314` `def usage(self, task_id)` -- Return consumed toolcalls/findings/rounds.
- `Budget.record_toolcall` (method) `modules/lazy_loop.py:2324` `def record_toolcall(self, task_id, intent_id)` -- Count one executed tool call.
- `Budget.record_round` (method) `modules/lazy_loop.py:2336` `def record_round(self, task_id)` -- Count one orchestrator round.
- `Budget.check` (method) `modules/lazy_loop.py:2354` `def check(self, task_id)` -- Return ok/exceeded decision with reason.
- `RuntimeTracker.__init__` (method) `modules/lazy_loop.py:2370` `def __init__(self, store)` -- Bind runtime to task store.
- `RuntimeTracker.heartbeat` (method) `modules/lazy_loop.py:2374` `def heartbeat(self, task_id)` -- Return live runtime snapshot.
- `RuntimeTracker.beat` (method) `modules/lazy_loop.py:2392` `def beat(self, task_id, workers)` -- Stamp heartbeat.
- `RuntimeTracker.abort` (method) `modules/lazy_loop.py:2407` `def abort(self, task_id, cause, detail)` -- Stamp abort cause like typed AbortCause.
- `RuntimeTracker.note_trigger` (method) `modules/lazy_loop.py:2423` `def note_trigger(self, task_id, trigger_id)` -- Advance scheduler watermark so restarts never re-fire.
- `InterceptQueue.__init__` (method) `modules/lazy_loop.py:2464` `def __init__(self, task_id)` -- Bind queue to task.
- `InterceptQueue.request` (method) `modules/lazy_loop.py:2478` `def request(self, tool, command, reason, tool_use_id)` -- Enqueue one ask decision and return pending entry.
- `InterceptQueue.pending` (method) `modules/lazy_loop.py:2496` `def pending(self)` -- Return pending entries ordered by id.
- `InterceptQueue.history` (method) `modules/lazy_loop.py:2500` `def history(self, page, per_page, states, query)` -- Paginated intercept history; pending stays fully visible.
- `InterceptQueue.decide` (method) `modules/lazy_loop.py:2552` `def decide(self, item_id, verdict)` -- Approve or deny one pending entry and wake its waiter.
- `InterceptQueue.wait` (method) `modules/lazy_loop.py:2566` `def wait(self, item_id, timeout_sec)` -- Block until decided or timeout; timeout denies safely.
- `TodoStore.__init__` (method) `modules/lazy_loop.py:2598` `def __init__(self, task_id)` -- Load persisted todos.
- `TodoStore.add` (method) `modules/lazy_loop.py:2609` `def add(self, text)` -- Append a serial step and return it.
- `TodoStore.complete` (method) `modules/lazy_loop.py:2616` `def complete(self, item_id)` -- Mark step done.
- `TodoStore.next_pending` (method) `modules/lazy_loop.py:2625` `def next_pending(self)` -- Return first pending step.
- `TodoStore.as_list` (method) `modules/lazy_loop.py:2632` `def as_list(self)` -- Return all steps.
- `TaskStore.__init__` (method) `modules/lazy_loop.py:2640` `def __init__(self)` -- Load task registry.
- `TaskStore.create` (method) `modules/lazy_loop.py:2649` `def create(self, goal, description)` -- Create task record and return it.
- `TaskStore.get` (method) `modules/lazy_loop.py:2660` `def get(self, task_id)` -- Return raw task record or None.
- `TaskStore.list` (method) `modules/lazy_loop.py:2664` `def list(self)` -- Return all task records.
- `TaskStore.set_status` (method) `modules/lazy_loop.py:2668` `def set_status(self, task_id, status)` -- Update task status.
- `TaskStore.pause` (method) `modules/lazy_loop.py:2680` `def pause(self, task_id)` -- Pause planner and workers like the planner Engine.Pause.
- `TaskStore.resume` (method) `modules/lazy_loop.py:2684` `def resume(self, task_id)` -- Resume a paused task back to running like the planner resumeTask.
- `TaskStore.delete` (method) `modules/lazy_loop.py:2693` `def delete(self, task_id)` -- Remove task record; per-task graph files are cleaned by caller.
- `TaskStore.active_count` (method) `modules/lazy_loop.py:2702` `def active_count(self, exclude)` -- Return how many tasks are currently running.
- `TaskStore.queue` (method) `modules/lazy_loop.py:2706` `def queue(self)` -- Return queued tasks in FIFO arrival order.
- `TaskStore.enqueue` (method) `modules/lazy_loop.py:2711` `def enqueue(self, task_id)` -- Mark a task queued with its arrival stamp.
- `TaskStore.dequeue_next` (method) `modules/lazy_loop.py:2722` `def dequeue_next(self)` -- Pop the oldest queued task and mark it running.
- `TaskStore.set_llm_chain` (method) `modules/lazy_loop.py:2737` `def set_llm_chain(self, task_id, members, active)` -- Bind a per-task LLM chain with a failover cursor.
- `TaskStore.llm_state` (method) `modules/lazy_loop.py:2765` `def llm_state(self, task_id)` -- Return the task LLM chain state (empty when unbound).
- `TaskStore.advance_llm` (method) `modules/lazy_loop.py:2771` `def advance_llm(self, task_id)` -- Advance the per-task active member after quota exhaustion.
- `TaskStore.set_skills` (method) `modules/lazy_loop.py:2795` `def set_skills(self, task_id, names, auto)` -- Pin skills for prompt injection and optionally toggle auto-match.
- `TaskStore.set_deadline` (method) `modules/lazy_loop.py:2820` `def set_deadline(self, task_id, timeout_sec)` -- Stamp absolute deadline like the planner deadline coordinator.
- `TaskStore.expired` (method) `modules/lazy_loop.py:2830` `def expired(self, task_id)` -- Report whether task deadline passed.
- `TaskStore.add_constraint` (method) `modules/lazy_loop.py:2836` `def add_constraint(self, task_id, ctype, text, scope)` -- Register allow/deny operation constraint like the planner set_constraints.
- `TaskStore.add_scope` (method) `modules/lazy_loop.py:2855` `def add_scope(self, task_id, kind, value, reason)` -- Register authorized asset scope like the planner add_task_scope.
- `TaskStore.steer` (method) `modules/lazy_loop.py:2866` `def steer(self, task_id, intent_id, message)` -- Attach mid-run correction to a running intent like steer_work.
- `TaskStore.kill` (method) `modules/lazy_loop.py:2875` `def kill(self, task_id, intent_id)` -- Flag a running intent for termination like kill_work.
- `TaskStore.steer_for` (method) `modules/lazy_loop.py:2886` `def steer_for(self, task_id, intent_id)` -- Return pending steer message for intent if any.
- `TaskStore.clear_steer` (method) `modules/lazy_loop.py:2891` `def clear_steer(self, task_id, intent_id)` -- Drop the pending steer message for an intent after delivery.
- `TaskStore.killed` (method) `modules/lazy_loop.py:2904` `def killed(self, task_id, intent_id)` -- Report whether intent was flagged for termination.
- `extract_scope_items` (function) `modules/lazy_loop.py:2910` `def extract_scope_items(goal_text, description)` -- Lift explicit asset scope from goal like the planner goalsScopeTail.
- `extract_constraint_items` (function) `modules/lazy_loop.py:2942` `def extract_constraint_items(goal_text, description)` -- Lift explicit allow/deny operation bounds like the planner goals decomposer.
- `load_intel_scores` (function) `modules/lazy_loop.py:3034` `def load_intel_scores()` -- Return host exposure scores for plan prioritisation.
- `resolve_target` (function) `modules/lazy_loop.py:3063` `def resolve_target(task_id, store, graph)` -- Resolve concrete target for worker commands from scope, assets, goal.
- `decompose_goals` (function) `modules/lazy_loop.py:3086` `def decompose_goals(goal_text, description)` -- Split goal text into verifiable objectives like the planner DecomposeGoals.
- `enrich_asset` (function) `modules/lazy_loop.py:3123` `def enrich_asset(value)` -- Synchronously enrich one asset with DNS and HTTP like the planner enrich.
- `Planner.__init__` (method) `modules/lazy_loop.py:3149` `def __init__(self, task_id, assets, graph, activity, store)` -- Bind planner to task collaborators.
- `Planner.plan` (method) `modules/lazy_loop.py:3177` `def plan(self, triggers)` -- Emit 0..N intents from current situation; most wakeups emit zero.
- `Planner.refine` (method) `modules/lazy_loop.py:3256` `def refine(self)` -- Re-plan pending intents against fresh outcomes, like plan refinement.
- `Planner.finalize` (method) `modules/lazy_loop.py:3662` `def finalize(self, reason)` -- Final planner round: park open intents and record the wrap-up.
- `sink` (function) `modules/lazy_loop.py:3682` `def sink(text)`
- `Worker.__init__` (method) `modules/lazy_loop.py:3788` `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` -- Bind worker to task collaborators.
- `Worker.rebind` (method) `modules/lazy_loop.py:3836` `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` -- Point a pooled worker at the collaborators of the current round.
- `Worker.close` (method) `modules/lazy_loop.py:3860` `def close(self)` -- Release the worker's shell session and shutdown registration.
- `Worker.execute` (method) `modules/lazy_loop.py:3956` `def execute(self, intent, executor, timeout_sec)` -- Run one intent to completion and write facts back.
- `run_command` (function) `modules/lazy_loop.py:4896` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/lazy_loop.py:4922` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/lazy_loop.py:4931` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/lazy_loop.py:4942` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/lazy_loop.py:4955` `def graph_state()` -- Compact exploration overview: intents, facts, findings.
- `shell_open` (function) `modules/lazy_loop.py:4970` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/lazy_loop.py:4974` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/lazy_loop.py:4978` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/lazy_loop.py:4986` `def job_output(job_id)` -- Return the tail of one background job's output.
- `sink` (function) `modules/lazy_loop.py:5444` `def sink(text)`
- `Retester.__init__` (method) `modules/lazy_loop.py:5820` `def __init__(self, graph, activity, traffic)` -- Bind retester to task collaborators.
- `Retester.retest` (method) `modules/lazy_loop.py:5826` `def retest(self, finding_id, executor, note)` -- Re-execute finding evidence to reproduced/fixed/inconclusive.
- `Retester.retest_context` (method) `modules/lazy_loop.py:5990` `def retest_context(self, finding_id)` -- Return finding + PoC + assets + constraints like get_finding_retest_context.
- `ColdCompactor.__init__` (method) `modules/lazy_loop.py:6012` `def __init__(self, graph, activity)` -- Bind compactor to task graph.
- `ColdCompactor.noa_archives` (method) `modules/lazy_loop.py:6122` `def noa_archives(self, limit)` -- List NOA raw archives for this task (newest first).
- `ColdCompactor.hot_set` (method) `modules/lazy_loop.py:6181` `def hot_set(self)` -- Compute hot nodes by reverse reachability from live intents.
- `ColdCompactor.structural_cold` (method) `modules/lazy_loop.py:6203` `def structural_cold(self, hot)` -- Return foldable non-hot nodes before debounce.
- `ColdCompactor.covered_members` (method) `modules/lazy_loop.py:6288` `def covered_members(self)` -- Return node ids already folded under active digests.
- `ColdCompactor.on_planner_round` (method) `modules/lazy_loop.py:6300` `def on_planner_round(self)` -- Advance round, maintain stamps, trigger background compaction.
- `ColdCompactor.compact` (method) `modules/lazy_loop.py:6341` `def compact(self, threshold, mode, debounce_sec)` -- Fold cold facts into digests like coldgraph minor/major.
- `ColdCompactor.expand` (method) `modules/lazy_loop.py:6468` `def expand(self, digest_id, role)` -- Restore digest members like expandDigest.
- `ColdCompactor.cold_index` (method) `modules/lazy_loop.py:6492` `def cold_index(self)` -- Group active digests by anchored asset.
- `ColdCompactor.unfolded` (method) `modules/lazy_loop.py:6510` `def unfolded(self, limit)` -- Return cold facts unfolded up to cap with a truncated flag.
- `ColdCompactor.digest_overview` (method) `modules/lazy_loop.py:6526` `def digest_overview(self)` -- Digest index: every digest with expandable members plus cold index.
- `constraint_block` (function) `modules/lazy_loop.py:6573` `def constraint_block(constraints, scope)` -- Render allow/deny bounds as highest-priority prompt block.
- `settlement_prompt` (function) `modules/lazy_loop.py:6607` `def settlement_prompt(agent, reason)` -- Build the wrap-up instruction used when a run budget ends.
- `build_prompt_context` (function) `modules/lazy_loop.py:6636` `def build_prompt_context(task_id, graph, assets, store, budget, top)` -- Assemble a bounded prompt context for planner/worker LLM calls.
- `finding_severity` (function) `modules/lazy_loop.py:6725` `def finding_severity(text, evidence)` -- Rank finding severity like the report renderer (critical first).
- `FindingService.__init__` (method) `modules/lazy_loop.py:6760` `def __init__(self, task_id, graph, activity, store)` -- Bind service to task collaborators.
- `FindingService.report` (method) `modules/lazy_loop.py:6792` `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` -- Register a finding with severity/evidence/dedupe like report_finding.
- `FindingService.apply_drafts` (method) `modules/lazy_loop.py:6992` `def apply_drafts(self)` -- Commit finished background reporter drafts onto their findings.
- `FindingService.set_status` (method) `modules/lazy_loop.py:7029` `def set_status(self, finding_id, status)` -- Transition finding status like the workflow disposition.
- `FindingService.update_report` (method) `modules/lazy_loop.py:7046` `def update_report(self, finding_id, report)` -- Write the narrative report and bump the evidence version.
- `FindingService.ranked` (method) `modules/lazy_loop.py:7068` `def ranked(self)` -- Findings ordered critical-first like the Markdown renderer.
- `EvidenceStore.__init__` (method) `modules/lazy_loop.py:7078` `def __init__(self, task_id)` -- Bind vault to task.
- `EvidenceStore.add` (method) `modules/lazy_loop.py:7087` `def add(self, finding_id, kind, body)` -- Attach evidence to a finding and return the record.
- `EvidenceStore.verify` (method) `modules/lazy_loop.py:7104` `def verify(self)` -- Return ids whose body fails the sha256 integrity check.
- `EvidenceStore.gc` (method) `modules/lazy_loop.py:7113` `def gc(self, valid_findings)` -- Drop evidence for findings no longer present; returns removed.
- `EvidenceStore.for_finding` (method) `modules/lazy_loop.py:7129` `def for_finding(self, finding_id)` -- Return evidence attached to one finding.
- `EvidenceStore.read` (method) `modules/lazy_loop.py:7133` `def read(self, evidence_id, offset, length)` -- Read one evidence body in bounded byte ranges.
- `EvidenceStore.export` (method) `modules/lazy_loop.py:7170` `def export(self, path)` -- Dump vault to a file for the report pipeline.
- `Notifier.__init__` (method) `modules/lazy_loop.py:7181` `def __init__(self, store)` -- Bind optional channel config from task store.
- `Notifier.channels` (method) `modules/lazy_loop.py:7185` `def channels(self)` -- Return configured channels (empty = log only).
- `Notifier.add_channel` (method) `modules/lazy_loop.py:7193` `def add_channel(self, kind, target, min_severity, extra)` -- Register a channel: log|webhook|file|slack|email with severity floor.
- `Notifier.remove_channel` (method) `modules/lazy_loop.py:7240` `def remove_channel(self, index)` -- Remove one channel by its 1-based list position.
- `Notifier.emit` (method) `modules/lazy_loop.py:7291` `def emit(self, task_id, event, data)` -- Fan out finding/status/task events; returns deliveries.
- `LlmPool.__init__` (method) `modules/lazy_loop.py:7364` `def __init__(self)` -- Load member list and usage ledger paths.
- `LlmPool.members` (method) `modules/lazy_loop.py:7399` `def members(self)` -- Return configured chain in order, seeding defaults on first use.
- `LlmPool.add_member` (method) `modules/lazy_loop.py:7404` `def add_member(self, name, model, priority)` -- Append a chain member backed by llm_factory at call time.
- `LlmPool.remove_member` (method) `modules/lazy_loop.py:7413` `def remove_member(self, name)` -- Drop a chain member.
- `LlmPool.set_priority` (method) `modules/lazy_loop.py:7423` `def set_priority(self, name, priority)` -- Change one member's failover rank, keeping the rest untouched.
- `LlmPool.usage` (method) `modules/lazy_loop.py:7436` `def usage(self)` -- Return per-member call ledger like llm_usage.
- `LlmPool.record_call` (method) `modules/lazy_loop.py:7446` `def record_call(self, member, ok, text)` -- Append one ledger row for external failover callers.
- `LlmPool.complete` (method) `modules/lazy_loop.py:7555` `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` -- Fail over across members; empty string when no backend answers.
- `LlmPool.health` (method) `modules/lazy_loop.py:7720` `def health(self)` -- Return per-member health state for lazy_llm health.
- `LlmPool.context_budget` (method) `modules/lazy_loop.py:7731` `def context_budget(self)` -- Return the prompt context character budget (default 2000).
- `LlmPool.record_raw` (method) `modules/lazy_loop.py:7736` `def record_raw(self)` -- Return whether raw prompt/response recording is enabled.
- `LlmPool.set_record_raw` (method) `modules/lazy_loop.py:7741` `def set_record_raw(self, enabled)` -- Toggle raw prompt/response recording in the pool ledger.
- `LlmPool.raw_entries` (method) `modules/lazy_loop.py:7748` `def raw_entries(self, limit)` -- Return the most recent raw LLM exchanges.
- `LlmPool.raw_entries_for_task` (method) `modules/lazy_loop.py:7762` `def raw_entries_for_task(self, task_id, limit)` -- Return the most recent raw LLM exchanges recorded for one task.
- `LlmPool.set_context_budget` (method) `modules/lazy_loop.py:7825` `def set_context_budget(self, chars)` -- Persist the prompt context character budget.
- `ToolCatalog.__init__` (method) `modules/lazy_loop.py:7843` `def __init__(self)` -- Load binding table.
- `ToolCatalog.bindings` (method) `modules/lazy_loop.py:7860` `def bindings(self, agent)` -- Return bindings for one agent or the whole table.
- `ToolCatalog.bind` (method) `modules/lazy_loop.py:7865` `def bind(self, agent, tool)` -- Opt a tool into an agent lane.
- `ToolCatalog.unbind` (method) `modules/lazy_loop.py:7874` `def unbind(self, agent, tool)` -- Remove a tool from an agent lane.
- `SideQuestions.ask` (method) `modules/lazy_loop.py:7894` `def ask(self, task_id, question, pool, session)` -- Answer from graph overview + recent trace within a char budget.
- `SideQuestions.history` (method) `modules/lazy_loop.py:7940` `def history(self, task_id, session, limit)` -- Return persisted side exchanges, optionally one session only.
- `SideQuestions.sessions` (method) `modules/lazy_loop.py:7948` `def sessions(self, task_id)` -- Return side-question session names for a task.
- `CompanyScope.__init__` (method) `modules/lazy_loop.py:7961` `def __init__(self)` -- Load company table.
- `CompanyScope.add` (method) `modules/lazy_loop.py:7969` `def add(self, name, scope)` -- Register a company with an optional scope pattern.
- `CompanyScope.list` (method) `modules/lazy_loop.py:7978` `def list(self)` -- Return companies with asset counts.
- `CompanyScope.match` (method) `modules/lazy_loop.py:7982` `def match(self, value)` -- Return companies whose scope substring hits the value.
- `TaskArchive.save` (method) `modules/lazy_loop.py:7991` `def save(self, task_id)` -- Snapshot task record + graph + activity tail into one archive.
- `TaskArchive.list` (method) `modules/lazy_loop.py:8012` `def list(self)` -- Return archive snapshots with task + node counts.
- `TaskArchive.restore` (method) `modules/lazy_loop.py:8034` `def restore(self, path)` -- Restore one archive as a NEW task; returns the new task id.
- `TaskArchive.stats` (method) `modules/lazy_loop.py:8101` `def stats(self)` -- Aggregate counts across archives like archive aggregate stats.
- `TaskTemplate.__init__` (method) `modules/lazy_loop.py:8110` `def __init__(self)` -- Bind template table.
- `TaskTemplate.list` (method) `modules/lazy_loop.py:8118` `def list(self)` -- Return all templates.
- `TaskTemplate.add` (method) `modules/lazy_loop.py:8122` `def add(self, name, goal)` -- Register a template; names are unique (overwrite on clash).
- `TaskTemplate.remove` (method) `modules/lazy_loop.py:8132` `def remove(self, name)` -- Delete a template by name.
- `TaskTemplate.get` (method) `modules/lazy_loop.py:8142` `def get(self, name)` -- Return one template by name or None.
- `TaskCategory.__init__` (method) `modules/lazy_loop.py:8153` `def __init__(self, store)` -- Bind optional task store.
- `TaskCategory.set` (method) `modules/lazy_loop.py:8158` `def set(self, task_id, category)` -- Label a task; returns the mapping.
- `TaskCategory.get` (method) `modules/lazy_loop.py:8165` `def get(self, task_id)` -- Return the category for a task or empty string.
- `TaskCategory.list` (method) `modules/lazy_loop.py:8169` `def list(self, category)` -- Return task->category rows, optionally filtered.
- `TaskChat.say` (method) `modules/lazy_loop.py:8184` `def say(self, task_id, text, pool, session)` -- Append a human turn and answer from task context; returns both.
- `TaskChat.log` (method) `modules/lazy_loop.py:8227` `def log(self, task_id, limit, session)` -- Return recent conversation turns, optionally one session only.
- `TaskChat.sessions` (method) `modules/lazy_loop.py:8243` `def sessions(self, task_id)` -- Return session names active in a task.
- `TaskChat.clear` (method) `modules/lazy_loop.py:8252` `def clear(self, task_id, session)` -- Drop one session's turns, or the whole log when session is empty.
- `LazyLoopEngine.__init__` (method) `modules/lazy_loop.py:8307` `def __init__(self, shell)` -- Load shared stores.
- `LazyLoopEngine.apply_profile` (method) `modules/lazy_loop.py:8342` `def apply_profile(self, name)` -- Apply one orchestrator profile to this engine.
- `LazyLoopEngine.bind_shell` (method) `modules/lazy_loop.py:8383` `def bind_shell(self, shell)` -- Attach the live shell so workers route auto/addon verbs via it.
- `LazyLoopEngine.ensure_target` (method) `modules/lazy_loop.py:8467` `def ensure_target(self, task_id, target, reason)` -- Register scope + asset for target like lazy_scope/lazy_asset.
- `LazyLoopEngine.orchestrate` (method) `modules/lazy_loop.py:8494` `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` -- Single entry for lazy_loop + auto_loop: create, scope, run, report.
- `LazyLoopEngine.create_task` (method) `modules/lazy_loop.py:8522` `def create_task(self, goal, description)` -- Create task, decompose goals, register scope, return summary.
- `LazyLoopEngine.spawn_task` (method) `modules/lazy_loop.py:8551` `def spawn_task(self, goal, source_task_ids, description)` -- Create a task read-only inheriting assets and findings.
- `LazyLoopEngine.list_tasks` (method) `modules/lazy_loop.py:8601` `def list_tasks(self)` -- Fleet view: every task with live intent/fact/finding counters.
- `LazyLoopEngine.pause_task` (method) `modules/lazy_loop.py:8629` `def pause_task(self, task_id, reason)` -- Pause another task from here (cross-task control).
- `LazyLoopEngine.resume_task` (method) `modules/lazy_loop.py:8640` `def resume_task(self, task_id)` -- Resume a paused task from here (cross-task control).
- `LazyLoopEngine.task_graph` (method) `modules/lazy_loop.py:8650` `def task_graph(self, task_id)` -- Graph overview of another task (get_task_graph parity).
- `LazyLoopEngine.task_findings` (method) `modules/lazy_loop.py:8656` `def task_findings(self, task_id)` -- Findings of another task with severity, status and report size.
- `LazyLoopEngine.task_traces` (method) `modules/lazy_loop.py:8675` `def task_traces(self, task_id, query, limit)` -- Worker traces of another task, keyword-filtered when asked.
- `LazyLoopEngine.task_node_detail` (method) `modules/lazy_loop.py:8684` `def task_node_detail(self, task_id, node_id)` -- Full node view of another task (get_task_node_detail parity).
- `LazyLoopEngine.update_finding_report` (method) `modules/lazy_loop.py:8690` `def update_finding_report(self, task_id, finding_id, report)` -- Write the narrative report of another task's finding.
- `LazyLoopEngine.broadcast_events` (method) `modules/lazy_loop.py:8702` `def broadcast_events(self, task_id, cursor, batch)` -- Return activity records after a line cursor (SSE resume parity).
- `LazyLoopEngine.add_hint` (method) `modules/lazy_loop.py:8735` `def add_hint(self, task_id, text)` -- Inject human steering hint read by the next planner round.
- `LazyLoopEngine.add_intent` (method) `modules/lazy_loop.py:8753` `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` -- Directly inject high-priority intent like the planner main-agent add_intent.
- `LazyLoopEngine.set_goals` (method) `modules/lazy_loop.py:8778` `def set_goals(self, task_id, specs)` -- Replace/append decomposed objectives like set_goals; wakes the task.
- `LazyLoopEngine.edit_goal` (method) `modules/lazy_loop.py:8795` `def edit_goal(self, task_id, goal_id, text)` -- Edit a goal node like the goals manager.
- `LazyLoopEngine.delete_goal` (method) `modules/lazy_loop.py:8807` `def delete_goal(self, task_id, goal_id)` -- Delete a goal node; done tasks with no goals left stay done.
- `LazyLoopEngine.preview_delete_intent` (method) `modules/lazy_loop.py:8818` `def preview_delete_intent(self, task_id, intent_id)` -- Estimate hard-delete cascade without mutating anything.
- `LazyLoopEngine.delete_intent` (method) `modules/lazy_loop.py:8841` `def delete_intent(self, task_id, intent_id, mode, reason)` -- Delete an intent in soft (fake) or hard (true) mode.
- `LazyLoopEngine.pause_intent` (method) `modules/lazy_loop.py:8986` `def pause_intent(self, task_id, intent_id)` -- Pause a runnable intent like the lazy worker interrupt.
- `LazyLoopEngine.resume_intent` (method) `modules/lazy_loop.py:9011` `def resume_intent(self, task_id, intent_id)` -- Resume a paused intent back to the claimable queue.
- `LazyLoopEngine.send_worker_message` (method) `modules/lazy_loop.py:9034` `def send_worker_message(self, task_id, intent_id, message, request_id)` -- Continue a paused worker intent with a human message.
- `LazyLoopEngine.goal_met` (method) `modules/lazy_loop.py:9082` `def goal_met(self, task_id, reason)` -- Declare the whole task complete like goal_met (weighted, audited).
- `LazyLoopEngine.record_fact` (method) `modules/lazy_loop.py:9092` `def record_fact(self, task_id, text, evidence, intent_id)` -- Operator-visible fact write like recordFact.
- `LazyLoopEngine.record_verdict` (method) `modules/lazy_loop.py:9099` `def record_verdict(self, task_id, finding_id, verdict, note)` -- Record an operator retest verdict on one finding.
- `LazyLoopEngine.run_round` (method) `modules/lazy_loop.py:9232` `def run_round(self, task_id, workers, executor, pool)` -- Run one orchestrated round invoking every subsystem in order.
- `stage_enabled` (function) `modules/lazy_loop.py:9283` `def stage_enabled(_name)`
- `LazyLoopEngine.run` (method) `modules/lazy_loop.py:9737` `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` -- Drive rounds until goals met, frontier drains, or budget exhausts.
- `LazyLoopEngine.prove_goal` (method) `modules/lazy_loop.py:10016` `def prove_goal(self, task_id, goal_id, evidence_id, reason)` -- Mark goal met with finding/fact evidence like the planner prove_goal.
- `LazyLoopEngine.delete_task` (method) `modules/lazy_loop.py:10157` `def delete_task(self, task_id)` -- Delete a task record plus every store file scoped to it.
- `LazyLoopEngine.proxy_start` (method) `modules/lazy_loop.py:10191` `def proxy_start(self, host, port, task_id, trust, upstream)` -- Start the shared recorder proxy and apply its trust environment.
- `LazyLoopEngine.proxy_stop` (method) `modules/lazy_loop.py:10227` `def proxy_stop(self)` -- Stop the recorder proxy and clear its trust environment.
- `LazyLoopEngine.proxy_status` (method) `modules/lazy_loop.py:10235` `def proxy_status(self)` -- Return recorder proxy state (running, address, CA, exchanges).
- `LazyLoopEngine.proxy_env` (method) `modules/lazy_loop.py:10241` `def proxy_env(self)` -- Return the environment overrides that route tools via proxy.
- `LazyLoopEngine.set_concurrency` (method) `modules/lazy_loop.py:10250` `def set_concurrency(self, limit)` -- Cap concurrently running tasks; 0 disables admission control.
- `LazyLoopEngine.admission_check` (method) `modules/lazy_loop.py:10271` `def admission_check(self, task_id)` -- Return whether a task may run now, queueing it when capped.
- `LazyLoopEngine.drain_queue` (method) `modules/lazy_loop.py:10290` `def drain_queue(self, max_tasks)` -- Run queued tasks FIFO while the concurrency cap allows.
- `LazyLoopEngine.ingest_proxy_traffic` (method) `modules/lazy_loop.py:10318` `def ingest_proxy_traffic(self, task_id, limit)` -- Mirror new recorder exchanges into the task traffic log.
- `LazyLoopEngine.search_proxy_body` (method) `modules/lazy_loop.py:10372` `def search_proxy_body(self, task_id, query, limit)` -- Full-text search proxy bodies scoped to one task's exchanges.
- `LazyLoopEngine.export_task_traffic` (method) `modules/lazy_loop.py:10464` `def export_task_traffic(self, task_id)` -- Export the task's proxy exchanges next to its archive.
- `LazyLoopEngine.export_evidence` (method) `modules/lazy_loop.py:10493` `def export_evidence(self, task_id, dest)` -- Freeze every task artefact into a hash-manifested zip package.
- `LazyLoopEngine.export_findings_report` (method) `modules/lazy_loop.py:10552` `def export_findings_report(self, task_id, path, fmt)` -- Render the severity-ranked report to Markdown, JSON or CSV.
- `LazyLoopEngine.status` (method) `modules/lazy_loop.py:10667` `def status(self, task_id)` -- Return full inspectable state for one task.
- `LazyLoopEngine.graph_overview` (method) `modules/lazy_loop.py:10687` `def graph_overview(self, task_id)` -- Return planner-facing overview plus coverage and scope.
- `LazyLoopEngine.broadcast` (method) `modules/lazy_loop.py:10749` `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` -- Paginated exploration timeline like the lazy broadcast board.
- `LazyLoopEngine.loop_graph` (method) `modules/lazy_loop.py:10873` `def loop_graph(self, task_id)` -- Return task graphs as ForceGraph-ready nodes/links.
- `LazyLoopEngine.graph_context` (method) `modules/lazy_loop.py:10942` `def graph_context(self, task_id, top)` -- Rank exploration topology to steer planner actions.

## modules/lazy_match_policy.py
Depends on: `modules/lazy_heat.py`
Imported by: `tests/test_lazy_match_policy.py`
- `strand_from_sighting` (function) `modules/lazy_match_policy.py:37` `def strand_from_sighting(sighting)` -- Classify one product sighting per the doctrine.
- `is_os_sighting` (function) `modules/lazy_match_policy.py:79` `def is_os_sighting(product, cpe)` -- Return True when the sighting names an operating system.
- `strand_rank` (function) `modules/lazy_match_policy.py:102` `def strand_rank(strand)` -- Return the merge precedence of a strand.
- `has_standing` (function) `modules/lazy_match_policy.py:107` `def has_standing(match)` -- Return True when humans or durable evidence touched a match.
- `MatchStore.__init__` (method) `modules/lazy_match_policy.py:127` `def __init__(self, sessions_dir)` -- Bind the store file under sessions/lazy.
- `MatchStore.upsert` (method) `modules/lazy_match_policy.py:132` `def upsert(self, identity, sighting, now)` -- Record one sighting under the dedupe identity.
- `MatchStore.rows` (method) `modules/lazy_match_policy.py:177` `def rows(self)` -- Return every stored row.
- `MatchStore.close` (method) `modules/lazy_match_policy.py:181` `def close(self, identity, reason, now)` -- Close one row, keeping its reason and reopening block.
- `MatchStore.closed_reason` (method) `modules/lazy_match_policy.py:196` `def closed_reason(self, identity)` -- Return the persisted closure reason, or '' when open or unknown.

## modules/lazy_mentions.py
Depends on: `modules/lazy_loop.py`
Imported by: `cli/commands/lazyloop.py`, `lazyc2.py`, `skills/lazyown_mcp.py`, `tests/test_security_codeql_batch.py`
- `search_mentions_page` (function) `modules/lazy_mentions.py:193` `def search_mentions_page(kind, query, cursor)` -- Search one scroll page of mention candidates.
- `parse_mentions` (function) `modules/lazy_mentions.py:237` `def parse_mentions(message)` -- Parse @[kind#id] tokens trusting type plus numeric id only.
- `compose_message` (function) `modules/lazy_mentions.py:268` `def compose_message(message)` -- Append server-read snapshots for referenced records as data.

## modules/lazy_netattack.py
Imported by: `tests/test_lazy_netattack.py`
- `AttackVectorVerdict.as_dict` (method) `modules/lazy_netattack.py:107` `def as_dict(self)` -- Return one JSON-safe view.
- `surface_decision` (function) `modules/lazy_netattack.py:184` `def surface_decision(evidence)` -- Grade the Windows network-attack families from evidence bags.
- `hint_text` (function) `modules/lazy_netattack.py:311` `def hint_text(verdict)` -- Shape one loop hint line for a verdict.

## modules/lazy_oob.py
Depends on: `modules/backdoor/server.c`
- `OobHit.as_dict` (method) `modules/lazy_oob.py:51` `def as_dict(self)` -- Return the JSON-serialisable row.
- `_CanaryHandler.do_GET` (method) `modules/lazy_oob.py:92` `def do_GET(self)` -- Record a GET callback.
- `_CanaryHandler.do_POST` (method) `modules/lazy_oob.py:97` `def do_POST(self)` -- Record a POST callback (body discarded).
- `_CanaryHandler.do_HEAD` (method) `modules/lazy_oob.py:102` `def do_HEAD(self)` -- Record a HEAD callback.
- `_CanaryHandler.log_message` (method) `modules/lazy_oob.py:107` `def log_message(self, fmt)` -- Silence the default stderr access log.
- `record_hit` (function) `modules/lazy_oob.py:112` `def record_hit(hit)` -- Store one hit in memory and append it to the JSONL mirror.
- `start` (function) `modules/lazy_oob.py:128` `def start(host, port)` -- Start (or reuse) the canary listener.
- `new_token` (function) `modules/lazy_oob.py:167` `def new_token()` -- Return one URL-safe callback token.
- `url` (function) `modules/lazy_oob.py:184` `def url(token)` -- Return the callback URL for a token (latest when omitted).
- `hits` (function) `modules/lazy_oob.py:204` `def hits(token)` -- Return recorded hits, optionally filtered by token.
- `stop` (function) `modules/lazy_oob.py:220` `def stop()` -- Shut the canary down and report how many hits it saw.
- `reset` (function) `modules/lazy_oob.py:241` `def reset()` -- Clear recorded hits and stop the listener (operator/test utility).
- `is_running` (function) `modules/lazy_oob.py:249` `def is_running()` -- Return whether the canary listener is alive.

## modules/lazy_orchestrator_feedback.py
Depends on: `modules/lazy_cli_bridge.py`, `modules/lazy_intel.py`
Imported by: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/mediation/feedback_mediator.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`
- `adjust_from_usage` (function) `modules/lazy_orchestrator_feedback.py:61` `def adjust_from_usage(limit)` -- Fold routing outcomes into per-(phase, stack, verb) success priors.
- `verb_prior` (function) `modules/lazy_orchestrator_feedback.py:162` `def verb_prior(phase, verb, stack)` -- Return the success prior for one (phase, stack, verb) triple.
- `rank_verbs` (function) `modules/lazy_orchestrator_feedback.py:189` `def rank_verbs(phase, verbs, stack)` -- Order verbs by learned success rate, stable for cold verbs.
- `order_steps` (function) `modules/lazy_orchestrator_feedback.py:213` `def order_steps(steps, stack)` -- Reorder resolved step lines by stack-aware verb priors.
- `export_dataset` (function) `modules/lazy_orchestrator_feedback.py:238` `def export_dataset(out, limit)` -- Export instruction-tuning rows joined from decisions + outcomes.

## modules/lazy_osinfer.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/world_model.py`
- `infer_from_ttl` (function) `modules/lazy_osinfer.py:47` `def infer_from_ttl(ttl)` -- Infer the remote OS family from a reply's TTL value.
- `infer_from_ping_output` (function) `modules/lazy_osinfer.py:72` `def infer_from_ping_output(output)` -- Read ``ttl=``/``TTL=`` from ping output and classify the OS.
- `infer_from_banner` (function) `modules/lazy_osinfer.py:97` `def infer_from_banner(text)` -- Infer the OS family from service names or banner text.
- `merge_os` (function) `modules/lazy_osinfer.py:118` `def merge_os(current, new)` -- Merge two inferred OS hints; a confident value wins.
- `addon_target_os` (function) `modules/lazy_osinfer.py:130` `def addon_target_os(name)` -- Return the ``os:`` field of one lazyaddon manifest.
- `verb_target_os` (function) `modules/lazy_osinfer.py:157` `def verb_target_os(command)` -- Return the OS family one command line targets.
- `os_compatible` (function) `modules/lazy_osinfer.py:194` `def os_compatible(verb_os, host_os)` -- Whether a verb's target OS may run against a host's inferred OS.
- `verb_compatible_with_host` (function) `modules/lazy_osinfer.py:216` `def verb_compatible_with_host(command, host_os)` -- Gate one command line against a host's inferred OS.
- `host_os_for_target` (function) `modules/lazy_osinfer.py:239` `def host_os_for_target(target)` -- Return the remembered OS for one target host.
- `remember_host_os` (function) `modules/lazy_osinfer.py:287` `def remember_host_os(target, os_name, reason)` -- Persist an inferred OS on the asset graph and world model.
- `learn_from_transcripts` (function) `modules/lazy_osinfer.py:330` `def learn_from_transcripts(target, transcripts)` -- Infer and remember the host OS from executed step outputs.

## modules/lazy_proxy.py
Depends on: `core/hardening.py`, `core/logging.py`, `modules/backdoor/server.c`, `modules/traffic_recorder.py`
Imported by: `cli/commands/lazyops.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_codeql_batch.py`
- `tls_lab_unverified_allowed` (function) `modules/lazy_proxy.py:253` `def tls_lab_unverified_allowed(host)` -- Return True only when a lab host has explicit self-signed opt-in.
- `resolve_validated_target` (function) `modules/lazy_proxy.py:282` `def resolve_validated_target(host, port, scheme)` -- Validate a target and return its pinned IP literals.
- `connect_pinned` (function) `modules/lazy_proxy.py:355` `def connect_pinned(host, ips, port, scheme)` -- Open a socket to a pinned validated IP, wrapping TLS for https.
- `_PinnedHTTPConnection.__init__` (method) `modules/lazy_proxy.py:384` `def __init__(self, host, port)` -- Store pinned IPs; hostname is kept for headers only.
- `_PinnedHTTPConnection.connect` (method) `modules/lazy_proxy.py:389` `def connect(self)` -- Dial the pinned IP so DNS cannot re-resolve to another host.
- `_PinnedHTTPSConnection.__init__` (method) `modules/lazy_proxy.py:397` `def __init__(self, host, port)` -- Store pinned IPs and the verifying TLS context.
- `_PinnedHTTPSConnection.connect` (method) `modules/lazy_proxy.py:410` `def connect(self)` -- Dial the pinned IP and verify the cert against the hostname.
- `detect_trust_target` (function) `modules/lazy_proxy.py:490` `def detect_trust_target()` -- Return the first existing system trust anchor directory and refresh command.
- `ca_trusted` (function) `modules/lazy_proxy.py:498` `def ca_trusted(ca_path)` -- Return True when the system anchor already holds this CA.
- `detect_nss_profiles` (function) `modules/lazy_proxy.py:517` `def detect_nss_profiles()` -- Return user NSS database directories (Firefox profiles + Chrome).
- `install_ca_nss` (function) `modules/lazy_proxy.py:532` `def install_ca_nss(ca_path, runner, profiles)` -- Install the recorder CA into user NSS databases via certutil.
- `install_ca_trust` (function) `modules/lazy_proxy.py:572` `def install_ca_trust(ca_path, runner)` -- Install the recorder CA into the system trust store.
- `CertificateAuthority.__init__` (method) `modules/lazy_proxy.py:626` `def __init__(self, pki_dir)` -- Load or create the CA under ``pki_dir``.
- `CertificateAuthority.context_for` (method) `modules/lazy_proxy.py:736` `def context_for(self, host)` -- Return the server TLS context for one host, generating on miss.
- `RecorderServer.__init__` (method) `modules/lazy_proxy.py:779` `def __init__(self, address, handler)`
- `RecorderServer.handle_error` (method) `modules/lazy_proxy.py:786` `def handle_error(self, request, client_address)` -- Silence client-side connection noise instead of tracebacks.
- `ProxyController.__init__` (method) `modules/lazy_proxy.py:806` `def __init__(self)` -- Prepare state; nothing binds until :meth:`start`.
- `ProxyController.start` (method) `modules/lazy_proxy.py:819` `def start(self, host, port, task_id, traffic_dir, upstream)` -- Bind the recorder proxy; idempotent while already running.
- `ProxyController.stop` (method) `modules/lazy_proxy.py:864` `def stop(self)` -- Shut the proxy down; safe when it was never started.
- `ProxyController.status` (method) `modules/lazy_proxy.py:880` `def status(self)` -- Report running state, address, CA path and exchange count.
- `ProxyController.recorder` (method) `modules/lazy_proxy.py:902` `def recorder(self)` -- Return the live recorder for ingestion, or None when stopped.
- `ProxyController.ca_path` (method) `modules/lazy_proxy.py:906` `def ca_path(self)` -- Return the CA certificate path for trust-store wiring.
- `ProxyHandler.log_message` (method) `modules/lazy_proxy.py:921` `def log_message(self, fmt)` -- Silence per-request logging; the recorder is the audit trail.
- `ProxyHandler.do_CONNECT` (method) `modules/lazy_proxy.py:925` `def do_CONNECT(self)` -- Terminate TLS for a CONNECT tunnel and record inner requests.
- `ProxyHandler.do_GET` (method) `modules/lazy_proxy.py:978` `def do_GET(self)` -- Forward every plain HTTP method through one path.
- `get_proxy` (function) `modules/lazy_proxy.py:1336` `def get_proxy()` -- Return the process-wide recorder proxy controller.
- `env_for_ca` (function) `modules/lazy_proxy.py:1345` `def env_for_ca(ca_path, host, port)` -- Build the environment overrides that route tools through the proxy.
- `apply_env` (function) `modules/lazy_proxy.py:1361` `def apply_env(ca_path, host, port)` -- Apply proxy env vars, returning the previous values for restore.
- `restore_env` (function) `modules/lazy_proxy.py:1368` `def restore_env(previous)` -- Restore environment values captured by :func:`apply_env`.

## modules/lazy_rbac.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/app_factory.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`
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

## modules/lazy_reaper.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/lazy_loop.py`, `tests/test_lazy_reaper.py`
- `reap` (function) `modules/lazy_reaper.py:30` `def reap(store, log_path, now, stale_seconds)` -- Expire tasks whose heartbeat is provably stale.

## modules/lazy_roles.py
Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`
- `list_roles` (function) `modules/lazy_roles.py:100` `def list_roles()` -- Return every Lazy role descriptor.
- `role_prompt` (function) `modules/lazy_roles.py:109` `def role_prompt(role, goal, context)` -- Build the system prompt for one role.
- `roles_for_phase` (function) `modules/lazy_roles.py:134` `def roles_for_phase(phase)` -- Return role names serving one kill-chain phase.
- `conformance` (function) `modules/lazy_roles.py:154` `def conformance(role)` -- Probe every pool member with role prompts, like provider conformance.

## modules/lazy_runner.py
Depends on: `cli/lazy_monitor.py`, `core/autonomous.py`, `core/hardening.py`, `core/terminal_guard.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/loop_guardrails.py`, `modules/loop_progress.py`, `utils.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/mcp_bridge.py`, `cli/commands/retry_ops.py`, `cli/lazy_monitor.py`, `modules/tools/loop_smoke.py`, `tests/test_lazy_runner.py`, `tests/test_loop_budget.py`, `tests/test_loop_multi_target.py`, `tests/test_loop_nmap_guard.py`, `tests/test_orchestrator_yaml.py`
- `ThreadStdoutRouter.__init__` (method) `modules/lazy_runner.py:55` `def __init__(self, main_stream, spool)` -- Bind the real stream and the worker spool queue.
- `ThreadStdoutRouter.write` (method) `modules/lazy_runner.py:61` `def write(self, data)` -- Route main-thread writes to the terminal, worker writes to spool.
- `ThreadStdoutRouter.flush` (method) `modules/lazy_runner.py:72` `def flush(self)` -- Flush the real stream; the spool needs no flushing.
- `ThreadStdoutRouter.encoding` (method) `modules/lazy_runner.py:80` `def encoding(self)` -- Report the real stream encoding.
- `ThreadStdoutRouter.isatty` (method) `modules/lazy_runner.py:84` `def isatty(self)` -- Report whether the real stream is a terminal.
- `LoopRunConfig.clamped` (method) `modules/lazy_runner.py:120` `def clamped(self)` -- Clamp numeric knobs to the supported operating range.
- `parse_loop_line` (function) `modules/lazy_runner.py:172` `def parse_loop_line(line)` -- Parse one loop command line into a :class:`LoopRunConfig`.
- `resolve_loop_defaults` (function) `modules/lazy_runner.py:302` `def resolve_loop_defaults(config)` -- Fill unset rounds and workers from the selected orchestrator profile.
- `build_executor` (function) `modules/lazy_runner.py:338` `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` -- Build the worker executor: shell verbs, custom tools, safe bash.
- `report_result` (function) `modules/lazy_runner.py:521` `def report_result(result)` -- Print the final outcome of one loop run.
- `stream` (function) `modules/lazy_runner.py:650` `def stream(text)`
- `load_targets_file` (function) `modules/lazy_runner.py:947` `def load_targets_file(path)` -- Read and validate one target per line from a scope file.
- `run_loop` (function) `modules/lazy_runner.py:1002` `def run_loop(shell, params, config)` -- Execute one complete loop run and return its summary.

## modules/lazy_sandbox.py
Depends on: `core/config.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_runner.py`
- `image_name` (function) `modules/lazy_sandbox.py:52` `def image_name(configured)` -- Resolve the sandbox image name.
- `container_name` (function) `modules/lazy_sandbox.py:67` `def container_name(task_id)` -- Return the deterministic container name for one task.
- `docker_available` (function) `modules/lazy_sandbox.py:73` `def docker_available()` -- Return True when the docker CLI is on PATH.
- `image_available` (function) `modules/lazy_sandbox.py:78` `def image_available(image)` -- Return True when the sandbox image exists locally.
- `container_running` (function) `modules/lazy_sandbox.py:94` `def container_running(task_id)` -- Return the container name when it is up, else empty string.
- `ensure_container` (function) `modules/lazy_sandbox.py:112` `def ensure_container(task_id, image)` -- Start the per-task container when needed, return its name or error.
- `exec_command` (function) `modules/lazy_sandbox.py:180` `def exec_command(task_id, command, timeout_sec, image)` -- Run one Lazy shell verb inside the task container.
- `remove_container` (function) `modules/lazy_sandbox.py:214` `def remove_container(task_id)` -- Stop and remove the task container.
- `status` (function) `modules/lazy_sandbox.py:223` `def status(task_id)` -- Describe sandbox readiness and containers.
- `executor_for` (function) `modules/lazy_sandbox.py:251` `def executor_for(task_id, image)` -- Build a worker executor routing shell verbs into the sandbox.


Next: [API_p15.md](API_p15.md)
