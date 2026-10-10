# API (page 12 of 21)
Previous: [API_p11.md](API_p11.md)

## modules/lazy_loop.py
Depends on: `core/process.py`, `modules/auto_registry.py`, `modules/finding_lifecycle.py`, `modules/intercept.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/notify.py`
Imported by: `cli/commands/mcp_bridge.py`, `modules/lazy_engine.py`, `tests/test_asset_gate.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_engine.py`
- `AssetGraph.__init__` (method) `modules/lazy_loop.py:189` `def __init__(self)` -- Load persisted assets or start empty.
- `AssetGraph.dedupe_key` (method) `modules/lazy_loop.py:207` `def dedupe_key(self, kind, value, parent_id)` -- Compute program-owned dedupe key for an asset.
- `AssetGraph.insert` (method) `modules/lazy_loop.py:211` `def insert(self, kind, value, parent_id, meta)` -- Insert asset or return existing node with same dedupe key.
- `AssetGraph.get` (method) `modules/lazy_loop.py:233` `def get(self, asset_id)` -- Return asset by id or None.
- `AssetGraph.list` (method) `modules/lazy_loop.py:237` `def list(self, kind)` -- List assets optionally filtered by kind.
- `AssetGraph.mark_tested` (method) `modules/lazy_loop.py:244` `def mark_tested(self, asset_id)` -- Flag asset as tested by a worker intent.
- `AssetGraph.coverage` (method) `modules/lazy_loop.py:254` `def coverage(self, scope)` -- Compute tested/total coverage, optionally scoped.
- `AssetGraph.untested` (method) `modules/lazy_loop.py:270` `def untested(self, limit)` -- Return oldest untested assets up to limit.
- `AssetGraph.coverage_for` (method) `modules/lazy_loop.py:275` `def coverage_for(self, graph, scope)` -- Compute task-scoped coverage like the planner graph_overview.
- `AssetGraph.untested_for` (method) `modules/lazy_loop.py:313` `def untested_for(self, graph, scope, limit)` -- Return scope-filtered assets not yet covered by this task.
- `ExplorationGraph.__init__` (method) `modules/lazy_loop.py:352` `def __init__(self, task_id)` -- Load task graph or start empty.
- `ExplorationGraph.add_node` (method) `modules/lazy_loop.py:383` `def add_node(self, kind, text, state, priority, meta)` -- Append node and return it.
- `ExplorationGraph.get` (method) `modules/lazy_loop.py:400` `def get(self, node_id)` -- Return node by id or None.
- `ExplorationGraph.set_state` (method) `modules/lazy_loop.py:404` `def set_state(self, node_id, state)` -- Transition node state and persist.
- `ExplorationGraph.add_edge` (method) `modules/lazy_loop.py:415` `def add_edge(self, src, dst, kind)` -- Link two existing nodes.
- `ExplorationGraph.anchor` (method) `modules/lazy_loop.py:428` `def anchor(self, node_id, asset_id)` -- Anchor exploration node to a concrete asset.
- `ExplorationGraph.anchors_for` (method) `modules/lazy_loop.py:439` `def anchors_for(self, node_id)` -- Return asset ids anchored to node.
- `ExplorationGraph.anchored_nodes` (method) `modules/lazy_loop.py:443` `def anchored_nodes(self, asset_id)` -- Return exploration node ids anchored to asset.
- `ExplorationGraph.list` (method) `modules/lazy_loop.py:447` `def list(self, kind, state)` -- List nodes optionally filtered by kind/state.
- `ExplorationGraph.children` (method) `modules/lazy_loop.py:456` `def children(self, node_id, kind)` -- Return destination ids of outgoing edges.
- `ExplorationGraph.overview` (method) `modules/lazy_loop.py:463` `def overview(self)` -- Return planner-facing state summary like graph overview.
- `ExplorationGraph.reload` (method) `modules/lazy_loop.py:476` `def reload(self)` -- Reload graph from disk, discarding in-memory state.
- `ExplorationGraph.compare_and_claim` (method) `modules/lazy_loop.py:499` `def compare_and_claim(self, node_id)` -- CAS claim: reload, verify still open, then mark running.
- `ExplorationGraph.finding_signature` (method) `modules/lazy_loop.py:526` `def finding_signature(self, text)` -- Normalize finding text into dedupe signature.
- `ExplorationGraph.has_finding` (method) `modules/lazy_loop.py:532` `def has_finding(self, text)` -- Return existing finding with same signature or None.
- `ExplorationGraph.node_detail` (method) `modules/lazy_loop.py:542` `def node_detail(self, node_id)` -- Full node view: text, state, meta, edges, anchors, trace tail.
- `ExplorationGraph.list_facts` (method) `modules/lazy_loop.py:552` `def list_facts(self, query, limit, hot_full)` -- Keyword-filtered facts like list_facts.
- `ExplorationGraph.record_fact` (method) `modules/lazy_loop.py:567` `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` -- Worker fact write like recordFact: deduped, anchored, done.
- `Frontier.__init__` (method) `modules/lazy_loop.py:583` `def __init__(self, graph)` -- Bind frontier to a task graph.
- `Frontier.pending` (method) `modules/lazy_loop.py:588` `def pending(self)` -- Return pending intents ordered by priority then id.
- `Frontier.claim_next` (method) `modules/lazy_loop.py:593` `def claim_next(self)` -- Atomically claim highest-priority pending intent (cross-process CAS).
- `Frontier.release` (method) `modules/lazy_loop.py:607` `def release(self, node_id, state)` -- Return a running intent to a new state.
- `ActivityLog.__init__` (method) `modules/lazy_loop.py:615` `def __init__(self, task_id)` -- Bind log to task.
- `ActivityLog.emit` (method) `modules/lazy_loop.py:620` `def emit(self, worker, kind, text, intent_id)` -- Append one activity record and return it.
- `ActivityLog.read` (method) `modules/lazy_loop.py:628` `def read(self, limit)` -- Return most recent records up to limit.
- `ActivityLog.for_intent` (method) `modules/lazy_loop.py:642` `def for_intent(self, intent_id)` -- Return records for one intent.
- `ActivityLog.search` (method) `modules/lazy_loop.py:646` `def search(self, query, exclude_intent)` -- Search worker traces by keyword, excluding one intent like the planner.
- `TrafficLog.__init__` (method) `modules/lazy_loop.py:663` `def __init__(self, task_id)` -- Bind log to task or global stream.
- `TrafficLog.record` (method) `modules/lazy_loop.py:668` `def record(self, kind, command, output, meta)` -- Append one traffic record and return it.
- `TrafficLog.read` (method) `modules/lazy_loop.py:684` `def read(self, limit)` -- Return most recent traffic records.
- `TrafficLog.search` (method) `modules/lazy_loop.py:698` `def search(self, query, limit)` -- Full-text search over command/output like traffic_search.
- `TrafficLog.get` (method) `modules/lazy_loop.py:707` `def get(self, digest)` -- Fetch one exchange by digest like traffic_get.
- `TrafficLog.templates` (method) `modules/lazy_loop.py:714` `def templates(self, limit)` -- Group exchanges by URL-template with counts like the proxy index.
- `TrafficLog.by_template` (method) `modules/lazy_loop.py:723` `def by_template(self, template, limit)` -- Return exchanges matching one template substring.
- `TrafficLog.bind` (method) `modules/lazy_loop.py:729` `def bind(self, finding_id, digest, graph)` -- Attach traffic digest to a finding like bind_finding_traffic.
- `TrafficLog.export` (method) `modules/lazy_loop.py:742` `def export(self, path, limit)` -- Dump recent exchanges to a JSON file like traffic archive export.
- `TrafficLog.archive` (method) `modules/lazy_loop.py:749` `def archive(self, label)` -- Snapshot traffic stream into sessions/lazy/traffic_archive_*.
- `TrafficLog.clear` (method) `modules/lazy_loop.py:755` `def clear(self)` -- Drop the traffic stream, returning the discarded record count.
- `Guard.__init__` (method) `modules/lazy_loop.py:768` `def __init__(self, task_id)` -- Load rules and audit trail.
- `Guard.add_rule` (method) `modules/lazy_loop.py:785` `def add_rule(self, pattern, action, reason, priority)` -- Register an intercept rule; higher priority evaluates first.
- `Guard.remove_rule` (method) `modules/lazy_loop.py:797` `def remove_rule(self, pattern)` -- Delete rules matching pattern exactly.
- `Guard.check` (method) `modules/lazy_loop.py:806` `def check(self, tool, command)` -- Evaluate tool call and audit it, returning allow/ask/deny.
- `Guard.audit` (method) `modules/lazy_loop.py:821` `def audit(self, limit)` -- Return recent audit entries.
- `Guard.stats` (method) `modules/lazy_loop.py:835` `def stats(self)` -- Attribution counters over the audit trail.
- `AssetGate.__init__` (method) `modules/lazy_loop.py:914` `def __init__(self, task_id)` -- Bind global list plus optional per-task lists.
- `AssetGate.add` (method) `modules/lazy_loop.py:942` `def add(self, kind, pattern, note, action)` -- Register a block (global or task) or allow (task only) rule.
- `AssetGate.remove` (method) `modules/lazy_loop.py:966` `def remove(self, rule_id, action)` -- Delete a rule by id; returns True when something was removed.
- `AssetGate.list` (method) `modules/lazy_loop.py:984` `def list(self)` -- Return global block plus per-task block/allow rules.
- `AssetGate.evaluate` (method) `modules/lazy_loop.py:988` `def evaluate(self, target)` -- Gate one target: allowed flag plus human-readable reason.
- `Budget.__init__` (method) `modules/lazy_loop.py:1009` `def __init__(self, store)` -- Bind budget counters to task store.
- `Budget.limits` (method) `modules/lazy_loop.py:1013` `def limits(self, task_id)` -- Return effective limits for task.
- `Budget.set_limits` (method) `modules/lazy_loop.py:1024` `def set_limits(self, task_id)` -- Persist budget limits for task.
- `Budget.usage` (method) `modules/lazy_loop.py:1037` `def usage(self, task_id)` -- Return consumed toolcalls/findings/rounds.
- `Budget.record_toolcall` (method) `modules/lazy_loop.py:1047` `def record_toolcall(self, task_id, intent_id)` -- Count one executed tool call.
- `Budget.record_round` (method) `modules/lazy_loop.py:1059` `def record_round(self, task_id)` -- Count one orchestrator round.
- `Budget.check` (method) `modules/lazy_loop.py:1077` `def check(self, task_id)` -- Return ok/exceeded decision with reason.
- `RuntimeTracker.__init__` (method) `modules/lazy_loop.py:1093` `def __init__(self, store)` -- Bind runtime to task store.
- `RuntimeTracker.heartbeat` (method) `modules/lazy_loop.py:1097` `def heartbeat(self, task_id)` -- Return live runtime snapshot.
- `RuntimeTracker.beat` (method) `modules/lazy_loop.py:1115` `def beat(self, task_id, workers)` -- Stamp heartbeat.
- `RuntimeTracker.abort` (method) `modules/lazy_loop.py:1130` `def abort(self, task_id, cause, detail)` -- Stamp abort cause like typed AbortCause.
- `RuntimeTracker.note_trigger` (method) `modules/lazy_loop.py:1146` `def note_trigger(self, task_id, trigger_id)` -- Advance scheduler watermark so restarts never re-fire.
- `InterceptQueue.__init__` (method) `modules/lazy_loop.py:1161` `def __init__(self, task_id)` -- Bind queue to task.
- `InterceptQueue.request` (method) `modules/lazy_loop.py:1175` `def request(self, tool, command, reason)` -- Enqueue one ask decision and return pending entry.
- `InterceptQueue.pending` (method) `modules/lazy_loop.py:1186` `def pending(self)` -- Return pending entries ordered by id.
- `InterceptQueue.decide` (method) `modules/lazy_loop.py:1191` `def decide(self, item_id, verdict)` -- Approve or deny one pending entry.
- `InterceptQueue.wait` (method) `modules/lazy_loop.py:1204` `def wait(self, item_id, timeout_sec)` -- Block until decided or timeout; timeout denies safely.
- `TodoStore.__init__` (method) `modules/lazy_loop.py:1227` `def __init__(self, task_id)` -- Load persisted todos.
- `TodoStore.add` (method) `modules/lazy_loop.py:1238` `def add(self, text)` -- Append a serial step and return it.
- `TodoStore.complete` (method) `modules/lazy_loop.py:1245` `def complete(self, item_id)` -- Mark step done.
- `TodoStore.next_pending` (method) `modules/lazy_loop.py:1254` `def next_pending(self)` -- Return first pending step.
- `TodoStore.as_list` (method) `modules/lazy_loop.py:1261` `def as_list(self)` -- Return all steps.
- `TaskStore.__init__` (method) `modules/lazy_loop.py:1269` `def __init__(self)` -- Load task registry.
- `TaskStore.create` (method) `modules/lazy_loop.py:1278` `def create(self, goal, description)` -- Create task record and return it.
- `TaskStore.get` (method) `modules/lazy_loop.py:1289` `def get(self, task_id)` -- Return raw task record or None.
- `TaskStore.list` (method) `modules/lazy_loop.py:1293` `def list(self)` -- Return all task records.
- `TaskStore.set_status` (method) `modules/lazy_loop.py:1297` `def set_status(self, task_id, status)` -- Update task status.
- `TaskStore.pause` (method) `modules/lazy_loop.py:1309` `def pause(self, task_id)` -- Pause planner and workers like the planner Engine.Pause.
- `TaskStore.resume` (method) `modules/lazy_loop.py:1313` `def resume(self, task_id)` -- Resume a paused task back to running like the planner resumeTask.
- `TaskStore.delete` (method) `modules/lazy_loop.py:1322` `def delete(self, task_id)` -- Remove task record; per-task graph files are cleaned by caller.
- `TaskStore.set_deadline` (method) `modules/lazy_loop.py:1331` `def set_deadline(self, task_id, timeout_sec)` -- Stamp absolute deadline like the planner deadline coordinator.
- `TaskStore.expired` (method) `modules/lazy_loop.py:1341` `def expired(self, task_id)` -- Report whether task deadline passed.
- `TaskStore.add_constraint` (method) `modules/lazy_loop.py:1347` `def add_constraint(self, task_id, ctype, text)` -- Register allow/deny operation constraint like the planner set_constraints.
- `TaskStore.add_scope` (method) `modules/lazy_loop.py:1360` `def add_scope(self, task_id, kind, value, reason)` -- Register authorized asset scope like the planner add_task_scope.
- `TaskStore.steer` (method) `modules/lazy_loop.py:1371` `def steer(self, task_id, intent_id, message)` -- Attach mid-run correction to a running intent like steer_work.
- `TaskStore.kill` (method) `modules/lazy_loop.py:1380` `def kill(self, task_id, intent_id)` -- Flag a running intent for termination like kill_work.
- `TaskStore.steer_for` (method) `modules/lazy_loop.py:1391` `def steer_for(self, task_id, intent_id)` -- Return pending steer message for intent if any.
- `TaskStore.killed` (method) `modules/lazy_loop.py:1396` `def killed(self, task_id, intent_id)` -- Report whether intent was flagged for termination.
- `TaskStore.extract_scope_items` (method) `modules/lazy_loop.py:1402` `def extract_scope_items(goal_text, description)` -- Lift explicit asset scope from goal like the planner goalsScopeTail.
- `TaskStore.extract_constraint_items` (method) `modules/lazy_loop.py:1434` `def extract_constraint_items(goal_text, description)` -- Lift explicit allow/deny operation bounds like the planner goals decomposer.
- `TaskStore.load_intel_scores` (method) `modules/lazy_loop.py:1451` `def load_intel_scores()` -- Return host exposure scores from sessions/intel_summary.json.
- `TaskStore.resolve_target` (method) `modules/lazy_loop.py:1465` `def resolve_target(task_id, store, graph)` -- Resolve concrete target for worker commands from scope, assets, goal.
- `TaskStore.decompose_goals` (method) `modules/lazy_loop.py:1488` `def decompose_goals(goal_text, description)` -- Split goal text into verifiable objectives like the planner DecomposeGoals.
- `TaskStore.enrich_asset` (method) `modules/lazy_loop.py:1520` `def enrich_asset(value)` -- Synchronously enrich one asset with DNS and HTTP like the planner enrich.
- `Planner.__init__` (method) `modules/lazy_loop.py:1544` `def __init__(self, task_id, assets, graph, activity, store)` -- Bind planner to task collaborators.
- `Planner.plan` (method) `modules/lazy_loop.py:1567` `def plan(self, triggers)` -- Emit 0..N intents from current situation; most wakeups emit zero.
- `Worker.__init__` (method) `modules/lazy_loop.py:1778` `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store)` -- Bind worker to task collaborators.
- `Worker.execute` (method) `modules/lazy_loop.py:1823` `def execute(self, intent, executor, timeout_sec)` -- Run one intent to completion and write facts back.
- `Retester.__init__` (method) `modules/lazy_loop.py:2093` `def __init__(self, graph, activity, traffic)` -- Bind retester to task collaborators.
- `Retester.retest` (method) `modules/lazy_loop.py:2099` `def retest(self, finding_id, executor, note)` -- Re-execute finding evidence to reproduced/fixed/inconclusive.
- `Retester.retest_context` (method) `modules/lazy_loop.py:2153` `def retest_context(self, finding_id)` -- Return finding + PoC + assets + constraints like get_finding_retest_context.
- `ColdCompactor.__init__` (method) `modules/lazy_loop.py:2167` `def __init__(self, graph, activity)` -- Bind compactor to task graph.
- `ColdCompactor.compact` (method) `modules/lazy_loop.py:2172` `def compact(self, threshold, mode)` -- Fold cold facts into digests like coldgraph minor/major.
- `ColdCompactor.expand` (method) `modules/lazy_loop.py:2210` `def expand(self, digest_id)` -- Restore digest members like expandDigest.
- `ColdCompactor.unfolded` (method) `modules/lazy_loop.py:2227` `def unfolded(self, limit)` -- Return cold facts unfolded up to cap with a truncated flag.
- `ColdCompactor.digest_overview` (method) `modules/lazy_loop.py:2242` `def digest_overview(self)` -- Digest index: every digest with expandable members + body preview.
- `ColdCompactor.constraint_block` (method) `modules/lazy_loop.py:2266` `def constraint_block(constraints)` -- Render allow/deny bounds as highest-priority prompt block.
- `ColdCompactor.finding_severity` (method) `modules/lazy_loop.py:2289` `def finding_severity(text, evidence)` -- Rank finding severity like the report renderer (critical first).
- `FindingService.__init__` (method) `modules/lazy_loop.py:2306` `def __init__(self, task_id, graph, activity, store)` -- Bind service to task collaborators.
- `FindingService.report` (method) `modules/lazy_loop.py:2314` `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` -- Register a finding with severity/evidence/dedupe like report_finding.
- `FindingService.set_status` (method) `modules/lazy_loop.py:2347` `def set_status(self, finding_id, status)` -- Transition finding status like the workflow disposition.
- `FindingService.ranked` (method) `modules/lazy_loop.py:2363` `def ranked(self)` -- Findings ordered critical-first like the Markdown renderer.
- `EvidenceStore.__init__` (method) `modules/lazy_loop.py:2372` `def __init__(self, task_id)` -- Bind vault to task.
- `EvidenceStore.add` (method) `modules/lazy_loop.py:2381` `def add(self, finding_id, kind, body)` -- Attach evidence to a finding and return the record.
- `EvidenceStore.verify` (method) `modules/lazy_loop.py:2393` `def verify(self)` -- Return ids whose body fails the sha256 integrity check.
- `EvidenceStore.gc` (method) `modules/lazy_loop.py:2402` `def gc(self, valid_findings)` -- Drop evidence for findings no longer present; returns removed.
- `EvidenceStore.for_finding` (method) `modules/lazy_loop.py:2419` `def for_finding(self, finding_id)` -- Return evidence attached to one finding.
- `EvidenceStore.export` (method) `modules/lazy_loop.py:2424` `def export(self, path)` -- Dump vault to a file for the report pipeline.
- `Notifier.__init__` (method) `modules/lazy_loop.py:2435` `def __init__(self, store)` -- Bind optional channel config from task store.
- `Notifier.channels` (method) `modules/lazy_loop.py:2439` `def channels(self)` -- Return configured channels (empty = log only).
- `Notifier.add_channel` (method) `modules/lazy_loop.py:2447` `def add_channel(self, kind, target, min_severity)` -- Register a channel: log|webhook|file with severity floor.
- `Notifier.emit` (method) `modules/lazy_loop.py:2457` `def emit(self, task_id, event, data)` -- Fan out finding_created/status_changed; returns deliveries.
- `TriggerStore.__init__` (method) `modules/lazy_loop.py:2503` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/lazy_loop.py:2512` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.remove` (method) `modules/lazy_loop.py:2525` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.list` (method) `modules/lazy_loop.py:2535` `def list(self)` -- Return all triggers.
- `TriggerStore.due` (method) `modules/lazy_loop.py:2539` `def due(self, task_id, graph, activity)` -- Evaluate triggers like the scheduler tick; fires at most once each.
- `LlmPool.__init__` (method) `modules/lazy_loop.py:2598` `def __init__(self)` -- Load member list and usage ledger paths.
- `LlmPool.members` (method) `modules/lazy_loop.py:2619` `def members(self)` -- Return configured chain in order, seeding defaults on first use.
- `LlmPool.add_member` (method) `modules/lazy_loop.py:2624` `def add_member(self, name, model, priority)` -- Append a chain member backed by llm_factory at call time.
- `LlmPool.remove_member` (method) `modules/lazy_loop.py:2633` `def remove_member(self, name)` -- Drop a chain member.
- `LlmPool.usage` (method) `modules/lazy_loop.py:2643` `def usage(self)` -- Return per-member call ledger like llm_usage.
- `LlmPool.complete` (method) `modules/lazy_loop.py:2654` `def complete(self, prompt, max_tokens)` -- Fail over across members; empty string when no backend answers.
- `LlmPool.health` (method) `modules/lazy_loop.py:2694` `def health(self)` -- Return per-member health state for lazy_llm health.
- `ToolCatalog.__init__` (method) `modules/lazy_loop.py:2709` `def __init__(self)` -- Load binding table.
- `ToolCatalog.bindings` (method) `modules/lazy_loop.py:2720` `def bindings(self, agent)` -- Return bindings for one agent or the whole table.
- `ToolCatalog.bind` (method) `modules/lazy_loop.py:2725` `def bind(self, agent, tool)` -- Opt a tool into an agent lane.
- `ToolCatalog.unbind` (method) `modules/lazy_loop.py:2734` `def unbind(self, agent, tool)` -- Remove a tool from an agent lane.
- `SideQuestions.ask` (method) `modules/lazy_loop.py:2749` `def ask(self, task_id, question, pool)` -- Answer from graph overview + recent trace within a char budget.
- `CompanyScope.__init__` (method) `modules/lazy_loop.py:2777` `def __init__(self)` -- Load company table.
- `CompanyScope.add` (method) `modules/lazy_loop.py:2785` `def add(self, name, scope)` -- Register a company with an optional scope pattern.
- `CompanyScope.list` (method) `modules/lazy_loop.py:2795` `def list(self)` -- Return companies with asset counts.
- `CompanyScope.match` (method) `modules/lazy_loop.py:2799` `def match(self, value)` -- Return companies whose scope substring hits the value.
- `TaskArchive.save` (method) `modules/lazy_loop.py:2809` `def save(self, task_id)` -- Snapshot task record + graph + activity tail into one archive.
- `TaskArchive.list` (method) `modules/lazy_loop.py:2825` `def list(self)` -- Return archive snapshots with task + node counts.
- `TaskArchive.restore` (method) `modules/lazy_loop.py:2842` `def restore(self, path)` -- Restore one archive as a NEW task; returns the new task id.
- `TaskArchive.stats` (method) `modules/lazy_loop.py:2861` `def stats(self)` -- Aggregate counts across archives like archive aggregate stats.
- `TaskTemplate.__init__` (method) `modules/lazy_loop.py:2870` `def __init__(self)` -- Bind template table.
- `TaskTemplate.list` (method) `modules/lazy_loop.py:2878` `def list(self)` -- Return all templates.
- `TaskTemplate.add` (method) `modules/lazy_loop.py:2882` `def add(self, name, goal)` -- Register a template; names are unique (overwrite on clash).
- `TaskTemplate.remove` (method) `modules/lazy_loop.py:2892` `def remove(self, name)` -- Delete a template by name.
- `TaskTemplate.get` (method) `modules/lazy_loop.py:2902` `def get(self, name)` -- Return one template by name or None.
- `TaskCategory.__init__` (method) `modules/lazy_loop.py:2913` `def __init__(self, store)` -- Bind optional task store.
- `TaskCategory.set` (method) `modules/lazy_loop.py:2918` `def set(self, task_id, category)` -- Label a task; returns the mapping.
- `TaskCategory.get` (method) `modules/lazy_loop.py:2925` `def get(self, task_id)` -- Return the category for a task or empty string.
- `TaskCategory.list` (method) `modules/lazy_loop.py:2929` `def list(self, category)` -- Return task->category rows, optionally filtered.
- `TaskChat.say` (method) `modules/lazy_loop.py:2941` `def say(self, task_id, text, pool)` -- Append a human turn and answer from task context; returns both.
- `TaskChat.log` (method) `modules/lazy_loop.py:2973` `def log(self, task_id, limit)` -- Return recent conversation turns.
- `TaskChat.clear` (method) `modules/lazy_loop.py:2987` `def clear(self, task_id)` -- Drop the conversation log for a task.
- `LazyLoopEngine.__init__` (method) `modules/lazy_loop.py:3011` `def __init__(self)` -- Load shared stores.
- `LazyLoopEngine.ensure_target` (method) `modules/lazy_loop.py:3019` `def ensure_target(self, task_id, target, reason)` -- Register scope + asset for target like lazy_scope/lazy_asset.
- `LazyLoopEngine.orchestrate` (method) `modules/lazy_loop.py:3046` `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` -- Single entry for lazy_loop + auto_loop: create, scope, run, report.
- `LazyLoopEngine.create_task` (method) `modules/lazy_loop.py:3069` `def create_task(self, goal, description)` -- Create task, decompose goals, register scope, return summary.
- `LazyLoopEngine.add_hint` (method) `modules/lazy_loop.py:3096` `def add_hint(self, task_id, text)` -- Inject human steering hint read by the next planner round.
- `LazyLoopEngine.add_intent` (method) `modules/lazy_loop.py:3103` `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` -- Directly inject high-priority intent like the planner main-agent add_intent.
- `LazyLoopEngine.set_goals` (method) `modules/lazy_loop.py:3123` `def set_goals(self, task_id, specs)` -- Replace/append decomposed objectives like set_goals; wakes the task.
- `LazyLoopEngine.edit_goal` (method) `modules/lazy_loop.py:3139` `def edit_goal(self, task_id, goal_id, text)` -- Edit a goal node like the goals manager.
- `LazyLoopEngine.delete_goal` (method) `modules/lazy_loop.py:3151` `def delete_goal(self, task_id, goal_id)` -- Delete a goal node; done tasks with no goals left stay done.
- `LazyLoopEngine.goal_met` (method) `modules/lazy_loop.py:3162` `def goal_met(self, task_id, reason)` -- Declare the whole task complete like goal_met (weighted, audited).
- `LazyLoopEngine.record_fact` (method) `modules/lazy_loop.py:3172` `def record_fact(self, task_id, text, evidence, intent_id)` -- Operator-visible fact write like recordFact.
- `LazyLoopEngine.run_round` (method) `modules/lazy_loop.py:3180` `def run_round(self, task_id, workers, executor)` -- Run one orchestrated round invoking every subsystem in order.
- `LazyLoopEngine.run` (method) `modules/lazy_loop.py:3375` `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` -- Drive rounds until goals met, frontier drains, or budget exhausts.
- `LazyLoopEngine.prove_goal` (method) `modules/lazy_loop.py:3422` `def prove_goal(self, task_id, goal_id, evidence_id, reason)` -- Mark goal met with finding/fact evidence like the planner prove_goal.
- `LazyLoopEngine.status` (method) `modules/lazy_loop.py:3468` `def status(self, task_id)` -- Return full inspectable state for one task.
- `LazyLoopEngine.graph_overview` (method) `modules/lazy_loop.py:3483` `def graph_overview(self, task_id)` -- Return planner-facing overview plus coverage and scope.

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
- `TenantManager.init_rbac_store` (method) `modules/lazy_rbac.py:523` `def init_rbac_store(users_path)`
- `TenantManager.init_tenant_manager` (method) `modules/lazy_rbac.py:527` `def init_tenant_manager(payloads_dir, config_path, default_payload)`
- `TenantManager.require_role` (method) `modules/lazy_rbac.py:539` `def require_role()` -- Flask decorator: require one of the given roles.
- `TenantManager.decorator` (method) `modules/lazy_rbac.py:542` `def decorator(f)`
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:544` `def decorated()`
- `TenantManager.require_permission` (method) `modules/lazy_rbac.py:565` `def require_permission()` -- Flask decorator: require specific permissions.
- `TenantManager.decorator` (method) `modules/lazy_rbac.py:568` `def decorator(f)`
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:570` `def decorated()`
- `TenantManager.require_mfa` (method) `modules/lazy_rbac.py:596` `def require_mfa(f)` -- Decorator that enforces MFA before accessing protected routes.
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:600` `def decorated()`
- `TenantManager.get_rbac_store` (method) `modules/lazy_rbac.py:639` `def get_rbac_store()`
- `TenantManager.set_rbac_store` (method) `modules/lazy_rbac.py:643` `def set_rbac_store(store)`
- `TenantManager.get_tenant_manager` (method) `modules/lazy_rbac.py:648` `def get_tenant_manager()`
- `TenantManager.set_tenant_manager` (method) `modules/lazy_rbac.py:655` `def set_tenant_manager(tm)`
- `TenantManager.check_cli_permission` (method) `modules/lazy_rbac.py:660` `def check_cli_permission(username, permission)` -- Check if a CLI user has the given permission.
- `TenantManager.get_user_role` (method) `modules/lazy_rbac.py:672` `def get_user_role(username)`
- `TenantManager.generate_mfa_qr_url` (method) `modules/lazy_rbac.py:680` `def generate_mfa_qr_url(secret, username)` -- Generate a QR code data URI for MFA setup (local, no external API).
- `TenantManager.generate_qr_svg` (method) `modules/lazy_rbac.py:689` `def generate_qr_svg(data)` -- Generate an SVG QR code image from text data.
- `TenantManager.gf_mul` (method) `modules/lazy_rbac.py:927` `def gf_mul(a, b)`

## modules/lazyatack.sh
- `mostrar_ayuda` (function) `modules/lazyatack.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyatack.sh:33` -- Función para validar una dirección IP
- `validar_url` (function) `modules/lazyatack.sh:49` -- Función para validar URL
- `descargar_seclists` (function) `modules/lazyatack.sh:107` -- Función para descargar y extraer SecLists
- `escanear_puertos` (function) `modules/lazyatack.sh:115` -- Función para ejecutar escaneo de puertos con nmap
- `escanear_puertos_especificos` (function) `modules/lazyatack.sh:121` -- Función para escanear puertos específicos
- `enumerar_http` (function) `modules/lazyatack.sh:127` -- Función para enumerar servicios HTTP
- `iniciar_servidor_http` (function) `modules/lazyatack.sh:133` -- Función para iniciar servidor HTTP con Python
- `configurar_netcat` (function) `modules/lazyatack.sh:139` -- Función para configurar netcat
- `enviar_archivo_netcat` (function) `modules/lazyatack.sh:145` -- Función para enviar archivo mediante bash a netcat
- `verificar_conectividad` (function) `modules/lazyatack.sh:151` -- Función para verificar conectividad con ping y tcpdump
- `verificar_curl` (function) `modules/lazyatack.sh:158` -- Función para verificar conectividad con curl
- `configurar_shell_reversa` (function) `modules/lazyatack.sh:165` -- Función para configurar una shell reversa
- `escuchar_shell` (function) `modules/lazyatack.sh:171` -- Función para escuchar shell con netcat
- `monitorear_procesos` (function) `modules/lazyatack.sh:177` -- Función para monitorear procesos
- `ejecutar_wfuzz` (function) `modules/lazyatack.sh:188` -- Función para ejecutar wfuzz
- `comprobar_sudo` (function) `modules/lazyatack.sh:194` -- Función para comprobar permisos sudo
- `explotar_lfi` (function) `modules/lazyatack.sh:200` -- Función para explotar LFI
- `configurar_tty` (function) `modules/lazyatack.sh:206` -- Función para configurar TTY
- `eliminar_archivos` (function) `modules/lazyatack.sh:217` -- Función para eliminar archivos de forma segura
- `obtener_root_shell` (function) `modules/lazyatack.sh:223` -- Función para obtener root shell mediante Docker
- `enumerar_suid` (function) `modules/lazyatack.sh:230` -- Función para enumerar archivos con SUID
- `listar_timers` (function) `modules/lazyatack.sh:236` -- Función para listar timers de systemd
- `comprobar_rutas` (function) `modules/lazyatack.sh:242` -- Función para comprobar rutas de comandos
- `abusar_tar` (function) `modules/lazyatack.sh:248` -- Función para abusar de tar
- `enumerar_puertos` (function) `modules/lazyatack.sh:254` -- Función para enumerar puertos abiertos
- `eliminar_contenedores_docker` (function) `modules/lazyatack.sh:260` -- Función para eliminar contenedores Docker
- `escanear_red` (function) `modules/lazyatack.sh:266` -- Función para escanear red
- `menu_servidor` (function) `modules/lazyatack.sh:272` -- Función para mostrar menú en modo servidor
- `menu_cliente` (function) `modules/lazyatack.sh:307` -- Función para mostrar menú en modo cliente

## modules/lazycloud.py
Imported by: `cli/commands/cloud.py`
- `CloudMetadataHarvester.__init__` (method) `modules/lazycloud.py:111` `def __init__(self, timeout)`
- `CloudMetadataHarvester.session` (method) `modules/lazycloud.py:116` `def session(self)`
- `CloudMetadataHarvester.harvest_aws` (method) `modules/lazycloud.py:139` `def harvest_aws(self)` -- Harvest AWS EC2 instance metadata (IMDSv2 capable).
- `CloudMetadataHarvester.harvest_azure` (method) `modules/lazycloud.py:184` `def harvest_azure(self)` -- Harvest Azure instance metadata.
- `CloudMetadataHarvester.harvest_gcp` (method) `modules/lazycloud.py:208` `def harvest_gcp(self)` -- Harvest GCP instance metadata.
- `CloudMetadataHarvester.harvest_all` (method) `modules/lazycloud.py:231` `def harvest_all(self)` -- Try all three cloud providers sequentially.
- `CloudBucketEnumerator.__init__` (method) `modules/lazycloud.py:251` `def __init__(self, timeout)`
- `CloudBucketEnumerator.session` (method) `modules/lazycloud.py:256` `def session(self)`
- `CloudBucketEnumerator.enumerate_s3` (method) `modules/lazycloud.py:278` `def enumerate_s3(self, prefix, buckets)` -- Enumerate S3 buckets derived from a prefix.
- `CloudBucketEnumerator.enumerate_azure_storage` (method) `modules/lazycloud.py:303` `def enumerate_azure_storage(self, prefix, accounts)` -- Enumerate Azure Blob Storage accounts.
- `CloudBucketEnumerator.enumerate_gcp_storage` (method) `modules/lazycloud.py:321` `def enumerate_gcp_storage(self, prefix, buckets)` -- Enumerate GCP Storage buckets.
- `CloudIAMEnumerator.enumerate_aws_iam` (method) `modules/lazycloud.py:345` `def enumerate_aws_iam(self, access_key, secret_key, session_token)` -- Enumerate AWS IAM (requires valid credentials).
- `CloudScanner.__init__` (method) `modules/lazycloud.py:393` `def __init__(self, target_domain, timeout)`
- `CloudScanner.full_scan` (method) `modules/lazycloud.py:400` `def full_scan(self, target_prefix, sessions_dir)` -- Perform a comprehensive cloud security scan.
- `CloudScanner.quick_metadata` (method) `modules/lazycloud.py:456` `def quick_metadata(self)` -- Fast metadata-only harvest (no bucket enumeration).
- `CloudScanner.quick_buckets` (method) `modules/lazycloud.py:460` `def quick_buckets(self, prefix)` -- Fast S3-only bucket check.

## modules/lazycurl.sh
- `ctrl_c` (function) `modules/lazycurl.sh:23`
- `show_help` (function) `modules/lazycurl.sh:29` -- Función para mostrar la ayuda
- `execute_curl` (function) `modules/lazycurl.sh:52` -- Función para ejecutar el comando CURL

## modules/lazyencoder_decoder.py
Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`
- `base64_encode` (function) `modules/lazyencoder_decoder.py:4` `def base64_encode(data)`
- `base64_decode` (function) `modules/lazyencoder_decoder.py:8` `def base64_decode(data)`
- `caesar_cipher` (function) `modules/lazyencoder_decoder.py:13` `def caesar_cipher(text, shift)`
- `caesar_decipher` (function) `modules/lazyencoder_decoder.py:27` `def caesar_decipher(text, shift)`
- `key_substitution` (function) `modules/lazyencoder_decoder.py:31` `def key_substitution(text, key)`
- `key_substitution_reverse` (function) `modules/lazyencoder_decoder.py:47` `def key_substitution_reverse(text, key)`
- `encode` (function) `modules/lazyencoder_decoder.py:63` `def encode(data, shift, key)`
- `encode_string` (function) `modules/lazyencoder_decoder.py:75` `def encode_string(data, shift, key)`
- `decode` (function) `modules/lazyencoder_decoder.py:82` `def decode(data, shift, key)`
- `decode_string` (function) `modules/lazyencoder_decoder.py:94` `def decode_string(data, shift, key)`

## modules/lazyevilwimrm.sh
- `execute_evil_winrm` (function) `modules/lazyevilwimrm.sh:14` -- Función para ejecutar evil-winrm y verificar la salida

## modules/lazyk8s.py
Imported by: `cli/commands/containers.py`
- `DockerEnumerator.__init__` (method) `modules/lazyk8s.py:44` `def __init__(self, socket_path)`
- `DockerEnumerator.is_socket_accessible` (method) `modules/lazyk8s.py:47` `def is_socket_accessible(self)` -- Check if the Docker socket is readable/writable.
- `DockerEnumerator.list_containers` (method) `modules/lazyk8s.py:70` `def list_containers(self)` -- List all containers with extended information.
- `DockerEnumerator.list_images` (method) `modules/lazyk8s.py:94` `def list_images(self)` -- List all Docker images.
- `DockerEnumerator.inspect_container` (method) `modules/lazyk8s.py:118` `def inspect_container(self, container_id)` -- Get detailed configuration of a container (privileged, mounts, capabilities).
- `DockerEnumerator.check_privileged_containers` (method) `modules/lazyk8s.py:137` `def check_privileged_containers(self)` -- Find containers running with --privileged flag.
- `DockerEnumerator.check_sensitive_mounts` (method) `modules/lazyk8s.py:162` `def check_sensitive_mounts(self)` -- Find containers with sensitive host path mounts.
- `DockerEnumerator.check_docker_socket_mount` (method) `modules/lazyk8s.py:196` `def check_docker_socket_mount(self)` -- Find containers with the Docker socket mounted (escape vector).
- `DockerEnumerator.check_capabilities` (method) `modules/lazyk8s.py:217` `def check_capabilities(self)` -- Find containers with dangerous Linux capabilities.
- `DockerEnumerator.full_check` (method) `modules/lazyk8s.py:250` `def full_check(self)` -- Execute all Docker security checks and return aggregated results.
- `K8sEnumerator.__init__` (method) `modules/lazyk8s.py:267` `def __init__(self, kubeconfig, token, api_server)`
- `K8sEnumerator.list_pods` (method) `modules/lazyk8s.py:366` `def list_pods(self, namespace)` -- List pods in all namespaces or a specific namespace.
- `K8sEnumerator.list_namespaces` (method) `modules/lazyk8s.py:390` `def list_namespaces(self)` -- List all namespaces.
- `K8sEnumerator.list_secrets` (method) `modules/lazyk8s.py:410` `def list_secrets(self, namespace)` -- List secrets (without decoding values by default).
- `K8sEnumerator.list_service_accounts` (method) `modules/lazyk8s.py:462` `def list_service_accounts(self, namespace)` -- List service accounts and their attached roles.
- `K8sEnumerator.check_rbac` (method) `modules/lazyk8s.py:498` `def check_rbac(self)` -- Check current user's RBAC permissions.
- `K8sEnumerator.check_pod_escape_vectors` (method) `modules/lazyk8s.py:530` `def check_pod_escape_vectors(self)` -- Check for pod escape vectors in the current pod.
- `K8sEnumerator.full_check` (method) `modules/lazyk8s.py:582` `def full_check(self, sessions_dir)` -- Execute all Kubernetes security checks.
- `ContainerEscapeTechniques.detect_current_environment` (method) `modules/lazyk8s.py:684` `def detect_current_environment()` -- Detect if running inside a container and identify escape opportunities.
- `ContainerRuntimeDetector.detect_runtime` (method) `modules/lazyk8s.py:803` `def detect_runtime()` -- Detect container runtime from multiple indicators.
- `ContainerRuntimeDetector.detect_mounts` (method) `modules/lazyk8s.py:874` `def detect_mounts()` -- Detect dangerous mounts in the current container.
- `ContainerRuntimeDetector.detect_dangerous_capabilities` (method) `modules/lazyk8s.py:921` `def detect_dangerous_capabilities()` -- Detect dangerous Linux capabilities in the current container.
- `ContainerRuntimeDetector.auto_detect_all` (method) `modules/lazyk8s.py:992` `def auto_detect_all()` -- Run comprehensive container escape auto-detection.

## modules/lazylynis.sh
- `check_sudo` (function) `modules/lazylynis.sh:32` -- Función para verificar y relanzar con sudo si es necesario

## modules/lazymasscan.sh
- `ctrl_c` (function) `modules/lazymasscan.sh:20`
- `extract_ports_info` (function) `modules/lazymasscan.sh:74`
- `run_masscan_script` (function) `modules/lazymasscan.sh:94`
- `print_row` (function) `modules/lazymasscan.sh:117`

## modules/lazynmap.sh
- `cleanup` (function) `modules/lazynmap.sh:29`
- `ctrl_c` (function) `modules/lazynmap.sh:38`
- `fix_sessions_owner` (function) `modules/lazynmap.sh:67` -- Best-effort ownership fixup: scans run under sudo leave root-owned files behind, and only root can chown those.
- `nmaptest` (function) `modules/lazynmap.sh:122`
- `discover_network` (function) `modules/lazynmap.sh:142`
- `extract_ports_info` (function) `modules/lazynmap.sh:811`
- `run_nmap_script` (function) `modules/lazynmap.sh:837`
- `print_row` (function) `modules/lazynmap.sh:870`

## modules/lazyown_bprfuzzer.py
Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`
- `load_headers_from_file` (function) `modules/lazyown_bprfuzzer.py:93` `def load_headers_from_file(file_path)`
- `load_data_from_file` (function) `modules/lazyown_bprfuzzer.py:99` `def load_data_from_file(file_path)`
- `signal_handler` (function) `modules/lazyown_bprfuzzer.py:105` `def signal_handler(sig, frame)`
- `ProxyHandler.do_GET` (method) `modules/lazyown_bprfuzzer.py:115` `def do_GET(self)`
- `ProxyHandler.do_POST` (method) `modules/lazyown_bprfuzzer.py:118` `def do_POST(self)`
- `ProxyHandler.run_proxy` (method) `modules/lazyown_bprfuzzer.py:162` `def run_proxy(port)`
- `ProxyHandler.edit_file_with_nano` (method) `modules/lazyown_bprfuzzer.py:169` `def edit_file_with_nano(content)`
- `ProxyHandler.send_request` (method) `modules/lazyown_bprfuzzer.py:179` `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` -- Envía una solicitud HTTP y devuelve la respuesta.
- `ProxyHandler.repeater` (method) `modules/lazyown_bprfuzzer.py:203` `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` -- Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
- `ProxyHandler.lazyfuzz` (method) `modules/lazyown_bprfuzzer.py:233` `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` -- Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
- `ProxyHandler.parse_arguments` (method) `modules/lazyown_bprfuzzer.py:278` `def parse_arguments()` -- Parsear los argumentos de la línea de comandos.
- `ProxyHandler.main` (method) `modules/lazyown_bprfuzzer.py:302` `def main()`

## modules/lazyown_bridge.py
Depends on: `modules/killchain.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`
- `CatalogEntry.build_command` (method) `modules/lazyown_bridge.py:63` `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` -- Return 'command [args]' with known values substituted.
- `CatalogEntry.matches_service` (method) `modules/lazyown_bridge.py:94` `def matches_service(self, services)`
- `CatalogEntry.matches_os` (method) `modules/lazyown_bridge.py:104` `def matches_os(self, os_hint)`
- `CommandCatalog.__init__` (method) `modules/lazyown_bridge.py:118` `def __init__(self)`
- `CommandCatalog.by_phase` (method) `modules/lazyown_bridge.py:3946` `def by_phase(self, phase)`
- `CommandCatalog.by_mitre` (method) `modules/lazyown_bridge.py:3952` `def by_mitre(self, technique_id)`
- `CommandCatalog.by_service` (method) `modules/lazyown_bridge.py:3956` `def by_service(self, service_name)`
- `CommandCatalog.by_tag` (method) `modules/lazyown_bridge.py:3960` `def by_tag(self, tag)`
- `CommandCatalog.by_os` (method) `modules/lazyown_bridge.py:3963` `def by_os(self, os_hint)`
- `CommandCatalog.all_phases` (method) `modules/lazyown_bridge.py:3966` `def all_phases(self)`
- `CommandCatalog.get` (method) `modules/lazyown_bridge.py:3969` `def get(self, command)`
- `CommandCatalog.count` (method) `modules/lazyown_bridge.py:3975` `def count(self)`
- `AbstractSelector.select` (method) `modules/lazyown_bridge.py:3986` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ServiceAwareSelector.select` (method) `modules/lazyown_bridge.py:4005` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `MitreAlignedSelector.__init__` (method) `modules/lazyown_bridge.py:4045` `def __init__(self, technique_id)`
- `MitreAlignedSelector.select` (method) `modules/lazyown_bridge.py:4049` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `TagSelector.__init__` (method) `modules/lazyown_bridge.py:4074` `def __init__(self, tag)`
- `TagSelector.select` (method) `modules/lazyown_bridge.py:4078` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ContextEnricher.enrich` (method) `modules/lazyown_bridge.py:4106` `def enrich(self, entry, target, world_snapshot)`
- `PhaseMapper.canonical_kill_chain_order` (method) `modules/lazyown_bridge.py:4204` `def canonical_kill_chain_order()` -- Return the canonical 8-phase order from KillChain (single source of truth).
- `PhaseMapper.to_bridge_phase` (method) `modules/lazyown_bridge.py:4210` `def to_bridge_phase(self, wm_phase)`
- `PhaseMapper.kill_chain_order` (method) `modules/lazyown_bridge.py:4223` `def kill_chain_order(self)` -- Ordered list of bridge phases following the kill chain.
- `BridgeDispatcher.__init__` (method) `modules/lazyown_bridge.py:4239` `def __init__(self, catalog, selector, enricher, phase_mapper)`
- `BridgeDispatcher.suggest` (method) `modules/lazyown_bridge.py:4251` `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` -- Return (command_string, entry) or None.
- `BridgeDispatcher.suggest_sequence` (method) `modules/lazyown_bridge.py:4296` `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` -- Return up to `limit` non-excluded suggestions for the phase.
- `BridgeDispatcher.suggest_for_wm_phase` (method) `modules/lazyown_bridge.py:4325` `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
- `BridgeDispatcher.list_phase` (method) `modules/lazyown_bridge.py:4343` `def list_phase(self, phase)`
- `BridgeDispatcher.all_phases` (method) `modules/lazyown_bridge.py:4347` `def all_phases(self)`
- `BridgeDispatcher.catalog_summary` (method) `modules/lazyown_bridge.py:4350` `def catalog_summary(self)`
- `BridgeDispatcher.catalog_summary_filtered` (method) `modules/lazyown_bridge.py:4358` `def catalog_summary_filtered(self, phase, os_hint)` -- Return a kill-chain summary restricted to a phase and target OS.
- `BridgeDispatcher.catalog_count` (method) `modules/lazyown_bridge.py:4395` `def catalog_count(self)`
- `BridgeDispatcher.phase_kill_chain` (method) `modules/lazyown_bridge.py:4398` `def phase_kill_chain(self)`
- `BridgeDispatcher.get_dispatcher` (method) `modules/lazyown_bridge.py:4409` `def get_dispatcher()`

## modules/lazyown_metaextract0r.py
- `signal_handler` (function) `modules/lazyown_metaextract0r.py:42` `def signal_handler(sig, frame)`
- `extract_pdf_metadata` (function) `modules/lazyown_metaextract0r.py:51` `def extract_pdf_metadata(file_path)`
- `extract_docx_metadata` (function) `modules/lazyown_metaextract0r.py:62` `def extract_docx_metadata(file_path)`
- `extract_ole_metadata` (function) `modules/lazyown_metaextract0r.py:73` `def extract_ole_metadata(file_path)`
- `extract_image_metadata` (function) `modules/lazyown_metaextract0r.py:85` `def extract_image_metadata(file_path)`
- `extract_metadata` (function) `modules/lazyown_metaextract0r.py:96` `def extract_metadata(file_path)`
- `find_and_extract_metadata` (function) `modules/lazyown_metaextract0r.py:109` `def find_and_extract_metadata(directory, output_file)`
- `parse_arguments` (function) `modules/lazyown_metaextract0r.py:130` `def parse_arguments()` -- Parse command-line arguments.
- `main` (function) `modules/lazyown_metaextract0r.py:140` `def main()`

## modules/lazyown_parquet_tool.py
- `highlight_term` (function) `modules/lazyown_parquet_tool.py:34` `def highlight_term(text, term)` -- Highlight the search term in the given text.
- `search_in_parquet` (function) `modules/lazyown_parquet_tool.py:39` `def search_in_parquet(term, parquet_files)` -- Search for a term in the given Parquet files and return matching rows.
- `buscar_binarios` (function) `modules/lazyown_parquet_tool.py:53` `def buscar_binarios(args)` -- Search for binaries with special permissions and generate a results CSV.
- `ejecutar_opciones` (function) `modules/lazyown_parquet_tool.py:136` `def ejecutar_opciones()` -- Execute options based on the found data.

## modules/lazyownclient.py
- `signal_handler` (function) `modules/lazyownclient.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownclient.py:51` `def pad(s)`
- `encrypt` (function) `modules/lazyownclient.py:55` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownclient.py:62` `def decrypt(ciphertext, key)`
- `handle_command` (function) `modules/lazyownclient.py:69` `def handle_command(cmd, key)`
- `main` (function) `modules/lazyownclient.py:198` `def main()`

## modules/lazyownerweb.py
Depends on: `core/logging.py`, `modules/logging_config.py`
- `send_request` (function) `modules/lazyownerweb.py:36` `def send_request(url, params, method)`
- `test_injection` (function) `modules/lazyownerweb.py:49` `def test_injection(url, payloads, param_name, detection_strings, method)`
- `main` (function) `modules/lazyownerweb.py:59` `def main()`

## modules/lazyownserver.py
- `signal_handler` (function) `modules/lazyownserver.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownserver.py:42` `def pad(s)`
- `encrypt` (function) `modules/lazyownserver.py:46` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownserver.py:53` `def decrypt(ciphertext, key)`
- `handle_client` (function) `modules/lazyownserver.py:60` `def handle_client(conn, addr, key)`
- `main` (function) `modules/lazyownserver.py:97` `def main()`

## modules/lazypsexec.sh
- `execute_psexec` (function) `modules/lazypsexec.sh:15` -- Función para ejecutar psexec y verificar la salida

## modules/lazyreverse_shell.sh
- `mostrar_ayuda` (function) `modules/lazyreverse_shell.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyreverse_shell.sh:31` -- Validar dirección IP

## modules/lazyvpnshield.sh
- `ctrl_c` (function) `modules/lazyvpnshield.sh:11`
- `check_sudo` (function) `modules/lazyvpnshield.sh:16`
- `save_current_rules` (function) `modules/lazyvpnshield.sh:29`
- `show_current_rules` (function) `modules/lazyvpnshield.sh:37`
- `apply_vpn_rules` (function) `modules/lazyvpnshield.sh:45`
- `undo_and_restore_rules` (function) `modules/lazyvpnshield.sh:86`
- `main` (function) `modules/lazyvpnshield.sh:113`

## modules/lazywps.sh
- `ctrl_c` (function) `modules/lazywps.sh:9`

## modules/lesson_ingestor.py
Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`
- `LessonLearned.from_dict` (method) `modules/lesson_ingestor.py:66` `def from_dict(cls, d)`
- `LessonIngestor.__init__` (method) `modules/lesson_ingestor.py:86` `def __init__(self, lessons_file, router, trainer, boost_reward)`
- `LessonIngestor.ingest` (method) `modules/lesson_ingestor.py:125` `def ingest(self, lesson)` -- Apply a single lesson to the MoE performance store and RL Q-table.
- `LessonIngestor.ingest_all` (method) `modules/lesson_ingestor.py:185` `def ingest_all(self, lessons)` -- Ingest a batch of lessons.
- `LessonIngestor.ingest_campaign_lessons` (method) `modules/lesson_ingestor.py:222` `def ingest_campaign_lessons(lessons_file)` -- Module-level convenience function to ingest all campaign lessons.


Next: [API_p13.md](API_p13.md)
