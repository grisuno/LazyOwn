# Symbols (page 17 of 50)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `add_member` | method | `modules/lazy_loop.py:6984` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1272` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2025` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3003` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10046` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2919` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1370` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1385` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1381` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:6554` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:7924` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1980` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:494` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2780` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:7474` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2119` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2540` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1902` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:7445` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8001` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:7440` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:10524` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:8330` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:6197` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1897` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:6765` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2067` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2502` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1398` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1570` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1986` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:7832` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3039` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4201` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:5991` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:5840` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1459` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2764` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7135` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:6072` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:7311` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1148` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1182` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:5787` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2797` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8140` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2700` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3268` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1093` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2841` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:8435` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:8469` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:9932` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2870` | `def dequeue_next(self)` |
| `digest_of` | method | `modules/lazy_loop.py:1724` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6025` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10065` | `def drain_queue(self, max_tasks)` |
| `edit_goal` | method | `modules/lazy_loop.py:8423` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1593` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:6871` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2859` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3305` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8085` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2416` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1950` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4236` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:5967` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2978` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1973` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:6750` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10268` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:10327` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10239` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3124` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3092` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:4003` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6286` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1487` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:6709` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1632` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:6693` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1127` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1300` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1821` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2808` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:7722` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:7745` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:8710` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:10717` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:10462` | `def graph_overview(self, task_id)` |
| `has_finding` | method | `modules/lazy_loop.py:1493` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:7300` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2522` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2648` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:7520` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:5680` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:10093` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:1097` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `judge_command` | function | `modules/lazy_loop.py:982` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:3023` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:3052` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2438` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1131` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1389` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2412` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2812` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7558` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7592` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7698` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7749` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1519` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8229` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2913` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3216` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:7807` | `def log(self, task_id, limit, session)` |
| `looks_like_prose` | function | `modules/lazy_loop.py:199` | `def looks_like_prose(command)` |
| `lookup` | method | `modules/lazy_loop.py:2147` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:477` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:10648` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1138` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:7562` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:6979` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2773` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:5621` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1503` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2571` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:5799` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:8112` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1412` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1405` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:954` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2828` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:8614` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:8257` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1565` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2644` | `def pending(self)` |
| `persist` | method | `modules/lazy_loop.py:1304` | `def persist(self)` |
| `plan` | method | `modules/lazy_loop.py:3359` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:175` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:8446` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:9783` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:10016` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:9966` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:10010` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:10002` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2854` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:6630` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:7328` | `def raw_entries(self, limit)` |
| `raw_entries_for_task` | method | `modules/lazy_loop.py:7342` | `def raw_entries_for_task(self, task_id, limit)` |
| `read` | method | `modules/lazy_loop.py:1618` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1768` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:6713` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:4177` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1746` | `def record(self, kind, command, output, meta)` |
| `record_call` | method | `modules/lazy_loop.py:7026` | `def record_call(self, member, ok, text)` |
| `record_fact` | method | `modules/lazy_loop.py:1535` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | method | `modules/lazy_loop.py:8720` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:7316` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2484` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2472` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:8727` | `def record_verdict(self, task_id, finding_id, verdict, note)` |
| `record_worker_traces` | function | `modules/lazy_loop.py:810` | `def record_worker_traces(task_id, worker, intent_id, transcripts, state, path)` |
| `recorder_blob` | method | `modules/lazy_loop.py:1857` | `def recorder_blob(self, digest, part, offset, length)` |
| `recorder_body` | method | `modules/lazy_loop.py:1828` | `def recorder_body(self, digest)` |
| `refine` | method | `modules/lazy_loop.py:3438` | `def refine(self)` |
| `register_worker` | function | `modules/lazy_loop.py:647` | `def register_worker(worker)` |
| `reload` | method | `modules/lazy_loop.py:1435` | `def reload(self)` |
| `remove` | method | `modules/lazy_loop.py:2394` | `def remove(self, rule_id, action)` |
| `remove` | method | `modules/lazy_loop.py:7712` | `def remove(self, name)` |
| `remove_channel` | method | `modules/lazy_loop.py:6820` | `def remove_channel(self, index)` |
| `remove_member` | method | `modules/lazy_loop.py:6993` | `def remove_member(self, name)` |
| `remove_rule` | method | `modules/lazy_loop.py:2036` | `def remove_rule(self, pattern)` |
| `reorder_evidence` | method | `modules/lazy_loop.py:1959` | `def reorder_evidence(self, finding_id, digests, graph)` |
| `repair_worker_command` | function | `modules/lazy_loop.py:347` | `def repair_worker_command(command, target)` |
| `report` | method | `modules/lazy_loop.py:6354` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `request` | method | `modules/lazy_loop.py:2626` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:3245` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:7614` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2832` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:8639` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:8268` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:5325` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:5489` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:9500` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_round` | method | `modules/lazy_loop.py:8877` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:7571` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:7764` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:1164` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:517` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1704` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1782` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1674` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1793` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:10147` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:8662` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:7528` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:7823` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:7738` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:10025` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:7405` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2968` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:8406` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:2045` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2449` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2885` | `def set_llm_chain(self, task_id, members, active)` |
| `set_node_meta` | method | `modules/lazy_loop.py:1327` | `def set_node_meta(self, node_id, meta)` |
| `set_node_state` | method | `modules/lazy_loop.py:1308` | `def set_node_state(self, node_id, state)` |
| `set_priority` | method | `modules/lazy_loop.py:7003` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:7321` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2943` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1346` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2816` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:6591` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:6106` | `def settlement_prompt(agent, reason)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:659` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:4023` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:4984` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:8179` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:8928` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:2189` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:7681` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:10442` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:3014` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:3034` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:5702` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:8284` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:8278` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:944` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:8312` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:8303` | `def task_traces(self, task_id, query, limit)` |
| `templates` | method | `modules/lazy_loop.py:1888` | `def templates(self, limit)` |
| `terminal_hint` | function | `modules/lazy_loop.py:6167` | `def terminal_hint(reason, state)` |
| `trace` | method | `modules/lazy_loop.py:1636` | `def trace(self, intent_id, query, step_id, limit)` |
| `unbind` | method | `modules/lazy_loop.py:7454` | `def unbind(self, agent, tool)` |
| `unfolded` | method | `modules/lazy_loop.py:6009` | `def unfolded(self, limit)` |
| `unregister_worker` | function | `modules/lazy_loop.py:653` | `def unregister_worker(worker)` |
| `untested` | method | `modules/lazy_loop.py:1177` | `def untested(self, limit)` |
| `untested_for` | method | `modules/lazy_loop.py:1210` | `def untested_for(self, graph, scope, limit)` |
| `update_finding_report` | method | `modules/lazy_loop.py:8318` | `def update_finding_report(self, task_id, finding_id, report)` |
| `update_report` | method | `modules/lazy_loop.py:6608` | `def update_report(self, finding_id, report)` |
| `usage` | method | `modules/lazy_loop.py:2462` | `def usage(self, task_id)` |
| `usage` | method | `modules/lazy_loop.py:7016` | `def usage(self)` |
| `verify` | method | `modules/lazy_loop.py:6673` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2714` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:613` | `def wake_task(task_id)` |
| `MatchStore` | class | `modules/lazy_match_policy.py:124` | `class MatchStore` |
| `__init__` | method | `modules/lazy_match_policy.py:127` | `def __init__(self, sessions_dir)` |
| `_key` | method | `modules/lazy_match_policy.py:170` | `def _key(identity)` |
| `_load` | method | `modules/lazy_match_policy.py:203` | `def _load(self)` |
| `_save_frame` | method | `modules/lazy_match_policy.py:214` | `def _save_frame(self, store)` |
| `_version_in_range` | function | `modules/lazy_match_policy.py:66` | `def _version_in_range(version, ranges)` |
| `close` | method | `modules/lazy_match_policy.py:181` | `def close(self, identity, reason, now)` |
| `closed_reason` | method | `modules/lazy_match_policy.py:196` | `def closed_reason(self, identity)` |
| `has_standing` | function | `modules/lazy_match_policy.py:107` | `def has_standing(match)` |
| `is_os_sighting` | function | `modules/lazy_match_policy.py:79` | `def is_os_sighting(product, cpe)` |
| `rows` | method | `modules/lazy_match_policy.py:177` | `def rows(self)` |
| `strand_from_sighting` | function | `modules/lazy_match_policy.py:37` | `def strand_from_sighting(sighting)` |
| `strand_rank` | function | `modules/lazy_match_policy.py:102` | `def strand_rank(strand)` |
| `upsert` | method | `modules/lazy_match_policy.py:132` | `def upsert(self, identity, sighting, now)` |
| `InvalidCursor` | class | `modules/lazy_mentions.py:52` | `class InvalidCursor(ValueError)` |
| `LazyMention` | class | `modules/lazy_mentions.py:35` | `class LazyMention` |
| `LazyMentionPage` | class | `modules/lazy_mentions.py:45` | `class LazyMentionPage` |
| `_asset_hits` | function | `modules/lazy_mentions.py:167` | `def _asset_hits(kind, query)` |
| `_collect_candidates` | function | `modules/lazy_mentions.py:91` | `def _collect_candidates(kind, query)` |
| `_company_hits` | function | `modules/lazy_mentions.py:142` | `def _company_hits(query)` |
| `_decode_cursor` | function | `modules/lazy_mentions.py:64` | `def _decode_cursor(cursor, scope, query)` |
| `_encode_cursor` | function | `modules/lazy_mentions.py:56` | `def _encode_cursor(last_id, last_kind, exact, scope, query)` |
| `_finding_hits` | function | `modules/lazy_mentions.py:108` | `def _finding_hits(query)` |
| `_literal_match` | function | `modules/lazy_mentions.py:84` | `def _literal_match(haystack, query)` |
| `_load_snapshot` | function | `modules/lazy_mentions.py:296` | `def _load_snapshot(kind, ref_id)` |
| `_store_glob` | function | `modules/lazy_mentions.py:186` | `def _store_glob(pattern)` |
| `compose_message` | function | `modules/lazy_mentions.py:268` | `def compose_message(message)` |
| `parse_mentions` | function | `modules/lazy_mentions.py:237` | `def parse_mentions(message)` |
| `search_mentions_page` | function | `modules/lazy_mentions.py:193` | `def search_mentions_page(kind, query, cursor)` |
| `AttackVectorVerdict` | class | `modules/lazy_netattack.py:88` | `class AttackVectorVerdict` |
| `SurfaceEvidence` | class | `modules/lazy_netattack.py:120` | `class SurfaceEvidence` |
| `_ad_hosts` | function | `modules/lazy_netattack.py:161` | `def _ad_hosts(evidence)` |
| `_ad_in` | function | `modules/lazy_netattack.py:303` | `def _ad_in(evidence, host)` |
| `_downgrade_candidates` | function | `modules/lazy_netattack.py:179` | `def _downgrade_candidates(evidence, windows)` |
| `_signing_not_required` | function | `modules/lazy_netattack.py:173` | `def _signing_not_required(host, evidence)` |
| `_signing_required` | function | `modules/lazy_netattack.py:297` | `def _signing_required(host, evidence)` |
| `_svc_blob` | function | `modules/lazy_netattack.py:136` | `def _svc_blob(hosts, evidence)` |
| `_windows_hosts` | function | `modules/lazy_netattack.py:146` | `def _windows_hosts(evidence)` |
| `as_dict` | method | `modules/lazy_netattack.py:107` | `def as_dict(self)` |
| `hint_text` | function | `modules/lazy_netattack.py:311` | `def hint_text(verdict)` |
| `surface_decision` | function | `modules/lazy_netattack.py:184` | `def surface_decision(evidence)` |
| `ObjectiveCandidate` | class | `modules/lazy_objective_queue.py:35` | `class ObjectiveCandidate` |
| `_load_records` | function | `modules/lazy_objective_queue.py:66` | `def _load_records(path)` |
| `_objectives_path` | function | `modules/lazy_objective_queue.py:49` | `def _objectives_path()` |
| `_save_records` | function | `modules/lazy_objective_queue.py:91` | `def _save_records(path, records)` |
| `_update_status` | function | `modules/lazy_objective_queue.py:153` | `def _update_status(objective_id, status, notes)` |
| `mark_started` | function | `modules/lazy_objective_queue.py:177` | `def mark_started(objective_id, task_id)` |
| `objective_ids_from_text` | function | `modules/lazy_objective_queue.py:235` | `def objective_ids_from_text(text)` |
| `pending_objectives` | function | `modules/lazy_objective_queue.py:105` | `def pending_objectives(limit, target)` |
| `settle` | function | `modules/lazy_objective_queue.py:196` | `def settle(objective_id, task_id, success)` |
| `OobHit` | class | `modules/lazy_oob.py:41` | `class OobHit` |
| `_CanaryHandler` | class | `modules/lazy_oob.py:63` | `class _CanaryHandler(BaseHTTPRequestHandler)` |
| `_configured_lhost` | function | `modules/lazy_oob.py:172` | `def _configured_lhost()` |
| `_record` | method | `modules/lazy_oob.py:66` | `def _record(self)` |
| `_respond` | method | `modules/lazy_oob.py:82` | `def _respond(self)` |
| `as_dict` | method | `modules/lazy_oob.py:51` | `def as_dict(self)` |
| `do_GET` | method | `modules/lazy_oob.py:92` | `def do_GET(self)` |
| `do_HEAD` | method | `modules/lazy_oob.py:102` | `def do_HEAD(self)` |
| `do_POST` | method | `modules/lazy_oob.py:97` | `def do_POST(self)` |
| `hits` | function | `modules/lazy_oob.py:204` | `def hits(token)` |
| `is_running` | function | `modules/lazy_oob.py:249` | `def is_running()` |
| `log_message` | method | `modules/lazy_oob.py:107` | `def log_message(self, fmt)` |
| `new_token` | function | `modules/lazy_oob.py:167` | `def new_token()` |
| `record_hit` | function | `modules/lazy_oob.py:112` | `def record_hit(hit)` |
| `reset` | function | `modules/lazy_oob.py:241` | `def reset()` |
| `start` | function | `modules/lazy_oob.py:128` | `def start(host, port)` |
| `stop` | function | `modules/lazy_oob.py:220` | `def stop()` |
| `url` | function | `modules/lazy_oob.py:184` | `def url(token)` |
| `_dataset_path` | function | `modules/lazy_orchestrator_feedback.py:47` | `def _dataset_path()` |
| `_key` | function | `modules/lazy_orchestrator_feedback.py:228` | `def _key(line)` |
| `_load_priors` | function | `modules/lazy_orchestrator_feedback.py:144` | `def _load_priors()` |
| `_normalize` | function | `modules/lazy_orchestrator_feedback.py:129` | `def _normalize(priors)` |
| `_priors_path` | function | `modules/lazy_orchestrator_feedback.py:41` | `def _priors_path()` |
| `_reward_of` | function | `modules/lazy_orchestrator_feedback.py:53` | `def _reward_of(outcome)` |
| `adjust_from_usage` | function | `modules/lazy_orchestrator_feedback.py:61` | `def adjust_from_usage(limit)` |
| `export_dataset` | function | `modules/lazy_orchestrator_feedback.py:238` | `def export_dataset(out, limit)` |
| `order_steps` | function | `modules/lazy_orchestrator_feedback.py:213` | `def order_steps(steps, stack)` |
| `rank_verbs` | function | `modules/lazy_orchestrator_feedback.py:189` | `def rank_verbs(phase, verbs, stack)` |
| `verb_prior` | function | `modules/lazy_orchestrator_feedback.py:162` | `def verb_prior(phase, verb, stack)` |
| `addon_target_os` | function | `modules/lazy_osinfer.py:130` | `def addon_target_os(name)` |
| `host_os_for_target` | function | `modules/lazy_osinfer.py:239` | `def host_os_for_target(target)` |
| `infer_from_banner` | function | `modules/lazy_osinfer.py:97` | `def infer_from_banner(text)` |
| `infer_from_ping_output` | function | `modules/lazy_osinfer.py:72` | `def infer_from_ping_output(output)` |
| `infer_from_ttl` | function | `modules/lazy_osinfer.py:47` | `def infer_from_ttl(ttl)` |
| `learn_from_transcripts` | function | `modules/lazy_osinfer.py:330` | `def learn_from_transcripts(target, transcripts)` |
| `merge_os` | function | `modules/lazy_osinfer.py:118` | `def merge_os(current, new)` |
| `os_compatible` | function | `modules/lazy_osinfer.py:194` | `def os_compatible(verb_os, host_os)` |
| `remember_host_os` | function | `modules/lazy_osinfer.py:287` | `def remember_host_os(target, os_name, reason)` |
| `verb_compatible_with_host` | function | `modules/lazy_osinfer.py:216` | `def verb_compatible_with_host(command, host_os)` |
| `verb_target_os` | function | `modules/lazy_osinfer.py:157` | `def verb_target_os(command)` |
| `RenderedCheck` | class | `modules/lazy_probes.py:47` | `class RenderedCheck` |
| `_need_port` | function | `modules/lazy_probes.py:97` | `def _need_port(params)` |
| `_render_http_probe` | function | `modules/lazy_probes.py:207` | `def _render_http_probe(params)` |
| `_render_nse_script` | function | `modules/lazy_probes.py:249` | `def _render_nse_script(params)` |
| `_render_nuclei_template` | function | `modules/lazy_probes.py:234` | `def _render_nuclei_template(params)` |
| `_render_package_version` | function | `modules/lazy_probes.py:263` | `def _render_package_version(params)` |
| `_render_service_state` | function | `modules/lazy_probes.py:290` | `def _render_service_state(params)` |
| `_render_version_banner` | function | `modules/lazy_probes.py:189` | `def _render_version_banner(params)` |
| `check_errors` | function | `modules/lazy_probes.py:108` | `def check_errors(kind, params)` |
| `range_text` | function | `modules/lazy_probes.py:70` | `def range_text(ranges)` |
| `render_check` | function | `modules/lazy_probes.py:156` | `def render_check(kind, params)` |
| `render_checks` | function | `modules/lazy_probes.py:177` | `def render_checks(checks)` |
| `CertificateAuthority` | class | `modules/lazy_proxy.py:623` | `class CertificateAuthority` |
| `ProxyController` | class | `modules/lazy_proxy.py:803` | `class ProxyController` |
| `ProxyHandler` | class | `modules/lazy_proxy.py:915` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `RecorderServer` | class | `modules/lazy_proxy.py:775` | `class RecorderServer(ThreadingHTTPServer)` |
| `_PinnedHTTPConnection` | class | `modules/lazy_proxy.py:381` | `class _PinnedHTTPConnection(HTTPConnection)` |
| `_PinnedHTTPSConnection` | class | `modules/lazy_proxy.py:394` | `class _PinnedHTTPSConnection(HTTPSConnection)` |
| `__init__` | method | `modules/lazy_proxy.py:384` | `def __init__(self, host, port)` |
| `__init__` | method | `modules/lazy_proxy.py:397` | `def __init__(self, host, port)` |
| `__init__` | method | `modules/lazy_proxy.py:626` | `def __init__(self, pki_dir)` |
| `__init__` | method | `modules/lazy_proxy.py:779` | `def __init__(self, address, handler)` |
| `__init__` | method | `modules/lazy_proxy.py:806` | `def __init__(self)` |
| `_cert_stem` | function | `modules/lazy_proxy.py:485` | `def _cert_stem(host)` |
| `_default_traffic_dir` | function | `modules/lazy_proxy.py:439` | `def _default_traffic_dir()` |
| `_dial_pinned` | function | `modules/lazy_proxy.py:329` | `def _dial_pinned(ips, port)` |
| `_ensure_ca` | method | `modules/lazy_proxy.py:638` | `def _ensure_ca(self)` |
| `_forward_plain` | method | `modules/lazy_proxy.py:989` | `def _forward_plain(self)` |
| `_handle_websocket` | method | `modules/lazy_proxy.py:1209` | `def _handle_websocket(self, scheme, host, port, path, url, req_headers)` |
| `_host_syntax_valid` | function | `modules/lazy_proxy.py:153` | `def _host_syntax_valid(host)` |
| `_https_connection` | function | `modules/lazy_proxy.py:428` | `def _https_connection(host, port)` |
| `_is_lab_host` | function | `modules/lazy_proxy.py:416` | `def _is_lab_host(host)` |
| `_is_metadata_hostname` | function | `modules/lazy_proxy.py:141` | `def _is_metadata_hostname(host)` |
| `_is_metadata_ip` | function | `modules/lazy_proxy.py:127` | `def _is_metadata_ip(value)` |
| `_make_handler` | function | `modules/lazy_proxy.py:911` | `def _make_handler()` |
| `_maybe_tls` | method | `modules/lazy_proxy.py:1183` | `def _maybe_tls(sock, scheme, host)` |
| `_open_target` | method | `modules/lazy_proxy.py:1161` | `def _open_target(self, scheme, host, port)` |
| `_parse_upstream` | function | `modules/lazy_proxy.py:444` | `def _parse_upstream(spec)` |
| `_proxy_allow_private` | function | `modules/lazy_proxy.py:105` | `def _proxy_allow_private()` |
| `_proxy_insecure_tls` | function | `modules/lazy_proxy.py:117` | `def _proxy_insecure_tls()` |
| `_proxy_trust_ca` | function | `modules/lazy_proxy.py:122` | `def _proxy_trust_ca()` |
| `_read_headers_from` | method | `modules/lazy_proxy.py:1199` | `def _read_headers_from(sock, limit)` |
| `_record` | method | `modules/lazy_proxy.py:1294` | `def _record(self, scheme, host, port, url, status, req_headers, resp_headers, req_body, resp_body, content_type, error)` |
| `_relay` | method | `modules/lazy_proxy.py:1063` | `def _relay(self, scheme, host, port, path, url, headers, body)` |
| `_resolved_ips` | function | `modules/lazy_proxy.py:169` | `def _resolved_ips(host)` |
| `_run_root` | function | `modules/lazy_proxy.py:510` | `def _run_root(argv)` |
| `_safe_send_error` | method | `modules/lazy_proxy.py:971` | `def _safe_send_error(self, code, message)` |
| `_server_class` | function | `modules/lazy_proxy.py:771` | `def _server_class()` |
| `_sha256` | function | `modules/lazy_proxy.py:764` | `def _sha256()` |
| `_upstream_auth_header` | function | `modules/lazy_proxy.py:475` | `def _upstream_auth_header(auth)` |
| `_upstream_tls_context` | function | `modules/lazy_proxy.py:236` | `def _upstream_tls_context(server_hostname)` |
| `_utc` | function | `modules/lazy_proxy.py:757` | `def _utc(timestamp)` |
| `_validate_proxy_target` | function | `modules/lazy_proxy.py:183` | `def _validate_proxy_target(host, port, scheme)` |
| `_validate_upstream_path` | function | `modules/lazy_proxy.py:265` | `def _validate_upstream_path(path)` |
| `_write_leaf` | method | `modules/lazy_proxy.py:693` | `def _write_leaf(self, host, cert_path, key_path)` |
| `apply_env` | function | `modules/lazy_proxy.py:1361` | `def apply_env(ca_path, host, port)` |
| `ca_path` | method | `modules/lazy_proxy.py:906` | `def ca_path(self)` |
| `ca_trusted` | function | `modules/lazy_proxy.py:498` | `def ca_trusted(ca_path)` |
| `connect` | method | `modules/lazy_proxy.py:389` | `def connect(self)` |
| `connect` | method | `modules/lazy_proxy.py:410` | `def connect(self)` |
| `connect_pinned` | function | `modules/lazy_proxy.py:355` | `def connect_pinned(host, ips, port, scheme)` |
| `context_for` | method | `modules/lazy_proxy.py:736` | `def context_for(self, host)` |
| `detect_nss_profiles` | function | `modules/lazy_proxy.py:517` | `def detect_nss_profiles()` |
| `detect_trust_target` | function | `modules/lazy_proxy.py:490` | `def detect_trust_target()` |
| `do_CONNECT` | method | `modules/lazy_proxy.py:925` | `def do_CONNECT(self)` |
| `do_GET` | method | `modules/lazy_proxy.py:978` | `def do_GET(self)` |
| `env_for_ca` | function | `modules/lazy_proxy.py:1345` | `def env_for_ca(ca_path, host, port)` |
| `get_proxy` | function | `modules/lazy_proxy.py:1336` | `def get_proxy()` |
| `handle_error` | method | `modules/lazy_proxy.py:786` | `def handle_error(self, request, client_address)` |
| `install_ca_nss` | function | `modules/lazy_proxy.py:532` | `def install_ca_nss(ca_path, runner, profiles)` |
| `install_ca_trust` | function | `modules/lazy_proxy.py:572` | `def install_ca_trust(ca_path, runner)` |
| `log_message` | method | `modules/lazy_proxy.py:921` | `def log_message(self, fmt)` |
| `recorder` | method | `modules/lazy_proxy.py:902` | `def recorder(self)` |
| `resolve_validated_target` | function | `modules/lazy_proxy.py:282` | `def resolve_validated_target(host, port, scheme)` |
| `restore_env` | function | `modules/lazy_proxy.py:1368` | `def restore_env(previous)` |
| `start` | method | `modules/lazy_proxy.py:819` | `def start(self, host, port, task_id, traffic_dir, upstream)` |
| `status` | method | `modules/lazy_proxy.py:880` | `def status(self)` |
| `stop` | method | `modules/lazy_proxy.py:864` | `def stop(self)` |
| `tls_lab_unverified_allowed` | function | `modules/lazy_proxy.py:253` | `def tls_lab_unverified_allowed(host)` |
| `Permission` | class | `modules/lazy_rbac.py:66` | `class Permission(Enum)` |
| `RBACStore` | class | `modules/lazy_rbac.py:210` | `class RBACStore` |
| `RBACUser` | class | `modules/lazy_rbac.py:124` | `class RBACUser` |
| `Role` | class | `modules/lazy_rbac.py:55` | `class Role(Enum)` |
| `TenantConfig` | class | `modules/lazy_rbac.py:368` | `class TenantConfig` |
| `TenantManager` | class | `modules/lazy_rbac.py:394` | `class TenantManager` |
| `_UsersFileUnreadable` | class | `modules/lazy_rbac.py:115` | `class _UsersFileUnreadable(Exception)` |
| `__init__` | method | `modules/lazy_rbac.py:213` | `def __init__(self, users_path)` |
| `__init__` | method | `modules/lazy_rbac.py:397` | `def __init__(self, payloads_dir, config_path, default_payload)` |
| `_bits_to_bytes` | function | `modules/lazy_rbac.py:903` | `def _bits_to_bytes(bits, data_bits)` |
| `_generate_recovery_codes` | function | `modules/lazy_rbac.py:356` | `def _generate_recovery_codes(count)` |
| `_get_rbac_store` | function | `modules/lazy_rbac.py:632` | `def _get_rbac_store()` |
| `_get_rbac_user` | function | `modules/lazy_rbac.py:619` | `def _get_rbac_user(flask_user)` |
| `_load_config` | method | `modules/lazy_rbac.py:410` | `def _load_config(self)` |
| `_qr_add_format_info` | function | `modules/lazy_rbac.py:836` | `def _qr_add_format_info(modules, size, ecl_bits, mask)` |
| `_qr_apply_mask` | function | `modules/lazy_rbac.py:963` | `def _qr_apply_mask(modules, size, mask)` |
| `_qr_best_mask` | function | `modules/lazy_rbac.py:950` | `def _qr_best_mask(modules, size)` |
| `_qr_blank_matrix` | function | `modules/lazy_rbac.py:823` | `def _qr_blank_matrix(version)` |
| `_qr_choose_version` | function | `modules/lazy_rbac.py:744` | `def _qr_choose_version(data)` |
| `_qr_data_bits_for_version` | function | `modules/lazy_rbac.py:812` | `def _qr_data_bits_for_version(version)` |
| `_qr_data_bits_positions` | function | `modules/lazy_rbac.py:884` | `def _qr_data_bits_positions(matrix, size)` |
| `_qr_ec_codewords` | function | `modules/lazy_rbac.py:752` | `def _qr_ec_codewords(version)` |
| `_qr_encode_alphanumeric` | function | `modules/lazy_rbac.py:757` | `def _qr_encode_alphanumeric(data, version)` |
| `_qr_penalty` | function | `modules/lazy_rbac.py:996` | `def _qr_penalty(modules, size)` |
| `_qr_place_dark_module` | function | `modules/lazy_rbac.py:832` | `def _qr_place_dark_module(matrix, size, version)` |
| `_qr_place_finders` | function | `modules/lazy_rbac.py:869` | `def _qr_place_finders(matrix, size)` |
| `_qr_place_timing` | function | `modules/lazy_rbac.py:878` | `def _qr_place_timing(matrix, size)` |
| `_qr_render_svg` | function | `modules/lazy_rbac.py:1058` | `def _qr_render_svg(modules, size, modules_per_pixel)` |
| `_qr_svg_error` | function | `modules/lazy_rbac.py:860` | `def _qr_svg_error(msg)` |
| `_read_users` | method | `modules/lazy_rbac.py:217` | `def _read_users(self)` |
| `_reed_solomon_encode` | function | `modules/lazy_rbac.py:914` | `def _reed_solomon_encode(data, ec_words)` |
| `_save_config` | method | `modules/lazy_rbac.py:421` | `def _save_config(self)` |
| `_slugify` | function | `modules/lazy_rbac.py:514` | `def _slugify(name)` |
| `_write_users` | method | `modules/lazy_rbac.py:232` | `def _write_users(self, users)` |
| `can_manage_role` | method | `modules/lazy_rbac.py:174` | `def can_manage_role(self, target_role)` |
| `check_cli_permission` | function | `modules/lazy_rbac.py:660` | `def check_cli_permission(username, permission)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:200` | `def consume_recovery_code(self, code)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:334` | `def consume_recovery_code(self, user_id, code)` |
| `create_tenant` | method | `modules/lazy_rbac.py:457` | `def create_tenant(self, name, base_payload)` |
| `create_user` | method | `modules/lazy_rbac.py:274` | `def create_user(self, username, password_hash, role, tenant_id)` |
| `decorated` | function | `modules/lazy_rbac.py:544` | `def decorated()` |
| `decorated` | function | `modules/lazy_rbac.py:570` | `def decorated()` |
| `decorated` | function | `modules/lazy_rbac.py:600` | `def decorated()` |
| `decorator` | function | `modules/lazy_rbac.py:542` | `def decorator(f)` |
| `decorator` | function | `modules/lazy_rbac.py:568` | `def decorator(f)` |
| `delete_tenant` | method | `modules/lazy_rbac.py:495` | `def delete_tenant(self, tenant_id)` |
| `delete_user` | method | `modules/lazy_rbac.py:295` | `def delete_user(self, user_id)` |
| `disable_mfa` | method | `modules/lazy_rbac.py:324` | `def disable_mfa(self, user_id)` |
| `enable_mfa` | method | `modules/lazy_rbac.py:314` | `def enable_mfa(self, user_id)` |
| `ensure_admin` | method | `modules/lazy_rbac.py:343` | `def ensure_admin(self, username, password_hash)` |
| `ensure_default_tenant` | method | `modules/lazy_rbac.py:504` | `def ensure_default_tenant(self)` |
| `find_by_id` | method | `modules/lazy_rbac.py:249` | `def find_by_id(self, user_id)` |
| `find_by_username` | method | `modules/lazy_rbac.py:255` | `def find_by_username(self, username)` |
| `from_dict` | method | `modules/lazy_rbac.py:140` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/lazy_rbac.py:390` | `def from_dict(cls, data)` |
| `from_payload` | method | `modules/lazy_rbac.py:377` | `def from_payload(cls, tenant_id, name, payload_path)` |
| `generate_mfa_qr_url` | function | `modules/lazy_rbac.py:680` | `def generate_mfa_qr_url(secret, username)` |
| `generate_qr_svg` | function | `modules/lazy_rbac.py:689` | `def generate_qr_svg(data)` |
| `get_active` | method | `modules/lazy_rbac.py:434` | `def get_active(self)` |
| `get_active_payload_path` | method | `modules/lazy_rbac.py:439` | `def get_active_payload_path(self)` |
| `get_active_sessions_dir` | method | `modules/lazy_rbac.py:445` | `def get_active_sessions_dir(self)` |
| `get_mfa_provisioning_uri` | method | `modules/lazy_rbac.py:182` | `def get_mfa_provisioning_uri(self)` |
| `get_payload_for_tenant` | method | `modules/lazy_rbac.py:451` | `def get_payload_for_tenant(self, tenant_id)` |
| `get_rbac_store` | function | `modules/lazy_rbac.py:639` | `def get_rbac_store()` |
| `get_role` | method | `modules/lazy_rbac.py:164` | `def get_role(self)` |
| `get_tenant_manager` | function | `modules/lazy_rbac.py:648` | `def get_tenant_manager()` |
| `get_user_role` | function | `modules/lazy_rbac.py:672` | `def get_user_role(username)` |
| `gf_mul` | function | `modules/lazy_rbac.py:927` | `def gf_mul(a, b)` |
| `has_permission` | method | `modules/lazy_rbac.py:170` | `def has_permission(self, permission)` |
| `init_rbac_store` | function | `modules/lazy_rbac.py:523` | `def init_rbac_store(users_path)` |
| `init_tenant_manager` | function | `modules/lazy_rbac.py:527` | `def init_tenant_manager(payloads_dir, config_path, default_payload)` |
| `list_tenants` | method | `modules/lazy_rbac.py:431` | `def list_tenants(self)` |
| `load_all` | method | `modules/lazy_rbac.py:245` | `def load_all(self)` |
| `require_mfa` | function | `modules/lazy_rbac.py:596` | `def require_mfa(f)` |
| `require_permission` | function | `modules/lazy_rbac.py:565` | `def require_permission()` |
| `require_role` | function | `modules/lazy_rbac.py:539` | `def require_role()` |
| `save` | method | `modules/lazy_rbac.py:261` | `def save(self, user)` |
| `set_rbac_store` | function | `modules/lazy_rbac.py:643` | `def set_rbac_store(store)` |
| `set_tenant_manager` | function | `modules/lazy_rbac.py:655` | `def set_tenant_manager(tm)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
