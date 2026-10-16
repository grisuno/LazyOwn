# Symbols (page 15 of 41)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `add_intent` | method | `modules/lazy_loop.py:7758` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:6612` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1056` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:1747` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2725` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:9009` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2641` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1112` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1127` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1123` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:6054` | `def apply_drafts(self)` |
| `archive` | method | `modules/lazy_loop.py:1702` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:322` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2502` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:7029` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:1841` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2262` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1624` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:7000` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:7468` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:6995` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:9468` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:7707` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:5792` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1619` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:6247` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:1789` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2224` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1140` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1312` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1708` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:7387` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:2761` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:3450` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:5654` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:5503` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1201` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2486` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:6736` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:5735` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:6912` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:932` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:966` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:5450` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2519` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:7527` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2422` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:2878` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:877` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2563` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:7812` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:7846` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:8895` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2592` | `def dequeue_next(self)` |
| `digest_overview` | method | `modules/lazy_loop.py:5688` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:9028` | `def drain_queue(self, max_tasks)` |
| `due` | method | `modules/lazy_loop.py:6464` | `def due(self, task_id, graph, activity, assets, store)` |
| `edit_goal` | method | `modules/lazy_loop.py:7800` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1335` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:6353` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2581` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:2915` | `def enrich_asset(value)` |
| `ensure_service_trigger` | method | `modules/lazy_loop.py:6451` | `def ensure_service_trigger(self)` |
| `ensure_target` | method | `modules/lazy_loop.py:7472` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2138` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1672` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:3514` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:5630` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2700` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1695` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:6232` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:9231` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:9290` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:9202` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:2812` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:2780` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3264` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:5873` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1229` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:6191` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1374` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:6175` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:911` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1084` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1543` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2530` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:7277` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:7300` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:8087` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:9661` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:9406` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:4225` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1235` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:6901` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2244` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2370` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:7075` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:5343` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:9056` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:881` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:4256` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:4248` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:766` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:2745` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:2774` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2160` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:915` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1131` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2134` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2534` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:6447` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7113` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7147` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7253` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7304` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1261` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:7606` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2635` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:2840` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:7362` | `def log(self, task_id, limit, session)` |
| `lookup` | method | `modules/lazy_loop.py:1869` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:305` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:9592` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:922` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:7117` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:6607` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2495` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:5284` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1245` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2293` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:5462` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:7499` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1154` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1147` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:738` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2550` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:7991` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:7634` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1307` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2366` | `def pending(self)` |
| `plan` | method | `modules/lazy_loop.py:2969` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:150` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:7823` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:8849` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:8979` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:8929` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:8973` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:8965` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2576` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:6130` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:6929` | `def raw_entries(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1360` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1490` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:6195` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:3426` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1468` | `def record(self, kind, command, output, meta)` |
| `record_fact` | method | `modules/lazy_loop.py:1277` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | function | `modules/lazy_loop.py:4192` | `def record_fact(text)` |
| `record_fact` | method | `modules/lazy_loop.py:8097` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:6917` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2206` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2194` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:8104` | `def record_verdict(self, task_id, finding_id, verdict, note)` |
| `recorder_blob` | method | `modules/lazy_loop.py:1579` | `def recorder_blob(self, digest, part, offset, length)` |
| `recorder_body` | method | `modules/lazy_loop.py:1550` | `def recorder_body(self, digest)` |
| `refine` | method | `modules/lazy_loop.py:3048` | `def refine(self)` |
| `register_worker` | function | `modules/lazy_loop.py:501` | `def register_worker(worker)` |
| `reload` | method | `modules/lazy_loop.py:1177` | `def reload(self)` |
| `remove` | method | `modules/lazy_loop.py:2116` | `def remove(self, rule_id, action)` |
| `remove` | method | `modules/lazy_loop.py:6437` | `def remove(self, trigger_id)` |
| `remove` | method | `modules/lazy_loop.py:7267` | `def remove(self, name)` |
| `remove_channel` | method | `modules/lazy_loop.py:6302` | `def remove_channel(self, index)` |
| `remove_member` | method | `modules/lazy_loop.py:6621` | `def remove_member(self, name)` |
| `remove_rule` | method | `modules/lazy_loop.py:1758` | `def remove_rule(self, pattern)` |
| `reorder_evidence` | method | `modules/lazy_loop.py:1681` | `def reorder_evidence(self, finding_id, digests, graph)` |
| `report` | method | `modules/lazy_loop.py:5897` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `report_finding` | function | `modules/lazy_loop.py:4201` | `def report_finding(name, evidence, severity)` |
| `request` | method | `modules/lazy_loop.py:2348` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:2855` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:7169` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2554` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:8016` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:7645` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:5082` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:5152` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:8666` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_command` | function | `modules/lazy_loop.py:4167` | `def run_command(command, background)` |
| `run_round` | method | `modules/lazy_loop.py:8189` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:7126` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:7319` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:948` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:363` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1446` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1504` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1416` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1515` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:9110` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:8039` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:7083` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:7378` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:7293` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:8988` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:6960` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2690` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:7783` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:1767` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2171` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2607` | `def set_llm_chain(self, task_id, members, active)` |
| `set_priority` | method | `modules/lazy_loop.py:6631` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:6922` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2665` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1088` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2538` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:6091` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:5769` | `def settlement_prompt(agent, reason)` |
| `shell_open` | function | `modules/lazy_loop.py:4240` | `def shell_open()` |
| `shell_send` | function | `modules/lazy_loop.py:4244` | `def shell_send(command)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:513` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:3284` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:4694` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:7556` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:8240` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:1911` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:7236` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:9386` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:2736` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:2756` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:5365` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:7661` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:7655` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:728` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:7689` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:7680` | `def task_traces(self, task_id, query, limit)` |
| `templates` | method | `modules/lazy_loop.py:1610` | `def templates(self, limit)` |
| `trace` | method | `modules/lazy_loop.py:1378` | `def trace(self, intent_id, query, step_id, limit)` |
| `traffic_search` | function | `modules/lazy_loop.py:4212` | `def traffic_search(query)` |
| `unbind` | method | `modules/lazy_loop.py:7009` | `def unbind(self, agent, tool)` |
| `unfolded` | method | `modules/lazy_loop.py:5672` | `def unfolded(self, limit)` |
| `unregister_worker` | function | `modules/lazy_loop.py:507` | `def unregister_worker(worker)` |
| `untested` | method | `modules/lazy_loop.py:961` | `def untested(self, limit)` |
| `untested_for` | method | `modules/lazy_loop.py:994` | `def untested_for(self, graph, scope, limit)` |
| `update_finding_report` | method | `modules/lazy_loop.py:7695` | `def update_finding_report(self, task_id, finding_id, report)` |
| `update_report` | method | `modules/lazy_loop.py:6108` | `def update_report(self, finding_id, report)` |
| `usage` | method | `modules/lazy_loop.py:2184` | `def usage(self, task_id)` |
| `usage` | method | `modules/lazy_loop.py:6644` | `def usage(self)` |
| `verify` | method | `modules/lazy_loop.py:6166` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2436` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:467` | `def wake_task(task_id)` |
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
| `switch_tenant` | method | `modules/lazy_rbac.py:486` | `def switch_tenant(self, tenant_id)` |
| `to_dict` | method | `modules/lazy_rbac.py:136` | `def to_dict(self)` |
| `to_dict` | method | `modules/lazy_rbac.py:386` | `def to_dict(self)` |
| `update_role` | method | `modules/lazy_rbac.py:304` | `def update_role(self, user_id, new_role)` |
| `valid_roles` | method | `modules/lazy_rbac.py:62` | `def valid_roles(cls)` |
| `verify_recovery_code` | method | `modules/lazy_rbac.py:192` | `def verify_recovery_code(self, code)` |
| `verify_totp` | method | `modules/lazy_rbac.py:187` | `def verify_totp(self, token)` |
| `conformance` | function | `modules/lazy_roles.py:154` | `def conformance(role)` |
| `list_roles` | function | `modules/lazy_roles.py:100` | `def list_roles()` |
| `role_prompt` | function | `modules/lazy_roles.py:109` | `def role_prompt(role, goal, context)` |
| `roles_for_phase` | function | `modules/lazy_roles.py:134` | `def roles_for_phase(phase)` |
| `LoopRunConfig` | class | `modules/lazy_runner.py:90` | `class LoopRunConfig` |
| `ThreadStdoutRouter` | class | `modules/lazy_runner.py:41` | `class ThreadStdoutRouter(TextIOBase)` |
| `__init__` | method | `modules/lazy_runner.py:51` | `def __init__(self, main_stream, spool)` |
| `_abort_run` | function | `modules/lazy_runner.py:298` | `def _abort_run(engine, task_id, reason)` |
| `_bootstrap` | function | `modules/lazy_runner.py:380` | `def _bootstrap(scan_target, executor)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:524` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:250` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:510` | `def _format_activity(record)` |
| `_overview` | function | `modules/lazy_runner.py:500` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:539` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:317` | `def _prepare_engine(engine, shell, config, params)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:242` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:446` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:656` | `def _run_plain(engine, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:394` | `def _run_with_progress(engine, config)` |
| `_start_proxy` | function | `modules/lazy_runner.py:331` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:634` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:129` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:121` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:773` | `def _tty_available()` |
| `_write` | function | `modules/lazy_runner.py:646` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:225` | `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` |
| `clamped` | method | `modules/lazy_runner.py:107` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:76` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:68` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:80` | `def isatty(self)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:137` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:356` | `def report_result(result)` |
| `run_loop` | function | `modules/lazy_runner.py:691` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:409` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:57` | `def write(self, data)` |
| `_payload_value` | function | `modules/lazy_sandbox.py:41` | `def _payload_value(key, default)` |
| `_sandbox_executor` | function | `modules/lazy_sandbox.py:265` | `def _sandbox_executor(command)` |
| `container_name` | function | `modules/lazy_sandbox.py:67` | `def container_name(task_id)` |
| `container_running` | function | `modules/lazy_sandbox.py:94` | `def container_running(task_id)` |
| `docker_available` | function | `modules/lazy_sandbox.py:73` | `def docker_available()` |
| `ensure_container` | function | `modules/lazy_sandbox.py:112` | `def ensure_container(task_id, image)` |
| `exec_command` | function | `modules/lazy_sandbox.py:180` | `def exec_command(task_id, command, timeout_sec, image)` |
| `executor_for` | function | `modules/lazy_sandbox.py:251` | `def executor_for(task_id, image)` |
| `image_available` | function | `modules/lazy_sandbox.py:78` | `def image_available(image)` |
| `image_name` | function | `modules/lazy_sandbox.py:52` | `def image_name(configured)` |
| `remove_container` | function | `modules/lazy_sandbox.py:214` | `def remove_container(task_id)` |
| `status` | function | `modules/lazy_sandbox.py:223` | `def status(task_id)` |
| `_hermes_config_path` | function | `modules/lazy_skill_mirror.py:112` | `def _hermes_config_path()` |
| `_hermes_frontmatter` | function | `modules/lazy_skill_mirror.py:45` | `def _hermes_frontmatter(name, fields)` |
| `_split_frontmatter` | function | `modules/lazy_skill_mirror.py:30` | `def _split_frontmatter(text)` |
| `available_skills` | function | `modules/lazy_skill_mirror.py:67` | `def available_skills()` |
| `mirror_all` | function | `modules/lazy_skill_mirror.py:106` | `def mirror_all()` |
| `mirror_skill` | function | `modules/lazy_skill_mirror.py:78` | `def mirror_skill(name)` |
| `register_external_dirs` | function | `modules/lazy_skill_mirror.py:117` | `def register_external_dirs()` |
| `_frontmatter` | function | `modules/lazy_skills.py:28` | `def _frontmatter(text)` |
| `_load` | function | `modules/lazy_skills.py:53` | `def _load(path)` |
| `_skill_files` | function | `modules/lazy_skills.py:42` | `def _skill_files()` |
| `get_skill` | function | `modules/lazy_skills.py:91` | `def get_skill(name)` |
| `list_skills` | function | `modules/lazy_skills.py:85` | `def list_skills()` |
| `match_skills` | function | `modules/lazy_skills.py:102` | `def match_skills(text, limit)` |
| `skills_context` | function | `modules/lazy_skills.py:118` | `def skills_context(text, explicit, auto, budget)` |
| `_digest` | function | `modules/lazy_summarizer.py:100` | `def _digest(older, complete)` |
| `_text_of` | function | `modules/lazy_summarizer.py:26` | `def _text_of(record)` |
| `_truncate_records` | function | `modules/lazy_summarizer.py:126` | `def _truncate_records(records, budget)` |
| `should_compact` | function | `modules/lazy_summarizer.py:35` | `def should_compact(used_chars, budget_chars)` |
| `summarize_chain` | function | `modules/lazy_summarizer.py:50` | `def summarize_chain(records, budget_chars, complete)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
