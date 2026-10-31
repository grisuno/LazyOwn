# Symbols (page 17 of 49)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `edit_goal` | method | `modules/lazy_loop.py:9180` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1587` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7676` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2853` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3265` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8852` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2410` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1944` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4177` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6772` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2972` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1967` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7555` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10903` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:10962` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10874` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3084` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3052` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3883` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:7091` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1481` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:7514` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1626` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:7498` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1121` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1294` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1815` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2802` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:8527` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:8550` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:9467` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:11352` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:11097` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:5245` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1487` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:8105` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2516` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2642` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:8325` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:6485` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:10728` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:1091` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:5276` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:5268` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:976` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:3017` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:3046` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2432` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1125` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1383` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2406` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2806` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8363` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8397` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8503` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8554` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1513` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8986` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2907` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3176` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:8612` | `def log(self, task_id, limit, session)` |
| `looks_like_prose` | function | `modules/lazy_loop.py:193` | `def looks_like_prose(command)` |
| `lookup` | method | `modules/lazy_loop.py:2141` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:471` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:11283` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1132` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:8367` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:7784` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2767` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:6426` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1497` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2565` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:6604` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:8879` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1406` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1399` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:948` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2822` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:9371` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:9014` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1559` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2638` | `def pending(self)` |
| `persist` | method | `modules/lazy_loop.py:1298` | `def persist(self)` |
| `plan` | method | `modules/lazy_loop.py:3319` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:169` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:9203` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:10418` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:10651` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:10601` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:10645` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:10637` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2848` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:7435` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:8133` | `def raw_entries(self, limit)` |
| `raw_entries_for_task` | method | `modules/lazy_loop.py:8147` | `def raw_entries_for_task(self, task_id, limit)` |
| `read` | method | `modules/lazy_loop.py:1612` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1762` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:7518` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:4057` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1740` | `def record(self, kind, command, output, meta)` |
| `record_call` | method | `modules/lazy_loop.py:7831` | `def record_call(self, member, ok, text)` |
| `record_fact` | method | `modules/lazy_loop.py:1529` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | function | `modules/lazy_loop.py:5212` | `def record_fact(text)` |
| `record_fact` | method | `modules/lazy_loop.py:9477` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:8121` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2478` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2466` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:9484` | `def record_verdict(self, task_id, finding_id, verdict, note)` |
| `record_worker_traces` | function | `modules/lazy_loop.py:804` | `def record_worker_traces(task_id, worker, intent_id, transcripts, state, path)` |
| `recorder_blob` | method | `modules/lazy_loop.py:1851` | `def recorder_blob(self, digest, part, offset, length)` |
| `recorder_body` | method | `modules/lazy_loop.py:1822` | `def recorder_body(self, digest)` |
| `refine` | method | `modules/lazy_loop.py:3398` | `def refine(self)` |
| `register_worker` | function | `modules/lazy_loop.py:641` | `def register_worker(worker)` |
| `reload` | method | `modules/lazy_loop.py:1429` | `def reload(self)` |
| `remove` | method | `modules/lazy_loop.py:2388` | `def remove(self, rule_id, action)` |
| `remove` | method | `modules/lazy_loop.py:8517` | `def remove(self, name)` |
| `remove_channel` | method | `modules/lazy_loop.py:7625` | `def remove_channel(self, index)` |
| `remove_member` | method | `modules/lazy_loop.py:7798` | `def remove_member(self, name)` |
| `remove_rule` | method | `modules/lazy_loop.py:2030` | `def remove_rule(self, pattern)` |
| `reorder_evidence` | method | `modules/lazy_loop.py:1953` | `def reorder_evidence(self, finding_id, digests, graph)` |
| `repair_worker_command` | function | `modules/lazy_loop.py:341` | `def repair_worker_command(command, target)` |
| `report` | method | `modules/lazy_loop.py:7159` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `report_finding` | function | `modules/lazy_loop.py:5221` | `def report_finding(name, evidence, severity)` |
| `request` | method | `modules/lazy_loop.py:2620` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:3205` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:8419` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2826` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:9396` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:9025` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:6130` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:6294` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:10139` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_command` | function | `modules/lazy_loop.py:5186` | `def run_command(command, background)` |
| `run_round` | method | `modules/lazy_loop.py:9634` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:8376` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:8569` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:1158` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:511` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1698` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1776` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1668` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1787` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:10782` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:9419` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:8333` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:8628` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:8543` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:10660` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:8210` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2962` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:9163` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:2039` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2443` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2879` | `def set_llm_chain(self, task_id, members, active)` |
| `set_node_meta` | method | `modules/lazy_loop.py:1321` | `def set_node_meta(self, node_id, meta)` |
| `set_node_state` | method | `modules/lazy_loop.py:1302` | `def set_node_state(self, node_id, state)` |
| `set_priority` | method | `modules/lazy_loop.py:7808` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:8126` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2937` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1340` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2810` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:7396` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:6911` | `def settlement_prompt(agent, reason)` |
| `shell_open` | function | `modules/lazy_loop.py:5260` | `def shell_open()` |
| `shell_send` | function | `modules/lazy_loop.py:5264` | `def shell_send(command)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:653` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:3903` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:5739` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:8936` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:9685` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:2183` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:8486` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:11077` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:3008` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:3028` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:6507` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:9041` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:9035` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:938` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:9069` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:9060` | `def task_traces(self, task_id, query, limit)` |
| `templates` | method | `modules/lazy_loop.py:1882` | `def templates(self, limit)` |
| `terminal_hint` | function | `modules/lazy_loop.py:6972` | `def terminal_hint(reason, state)` |
| `trace` | method | `modules/lazy_loop.py:1630` | `def trace(self, intent_id, query, step_id, limit)` |
| `traffic_search` | function | `modules/lazy_loop.py:5232` | `def traffic_search(query)` |
| `unbind` | method | `modules/lazy_loop.py:8259` | `def unbind(self, agent, tool)` |
| `unfolded` | method | `modules/lazy_loop.py:6814` | `def unfolded(self, limit)` |
| `unregister_worker` | function | `modules/lazy_loop.py:647` | `def unregister_worker(worker)` |
| `untested` | method | `modules/lazy_loop.py:1171` | `def untested(self, limit)` |
| `untested_for` | method | `modules/lazy_loop.py:1204` | `def untested_for(self, graph, scope, limit)` |
| `update_finding_report` | method | `modules/lazy_loop.py:9075` | `def update_finding_report(self, task_id, finding_id, report)` |
| `update_report` | method | `modules/lazy_loop.py:7413` | `def update_report(self, finding_id, report)` |
| `usage` | method | `modules/lazy_loop.py:2456` | `def usage(self, task_id)` |
| `usage` | method | `modules/lazy_loop.py:7821` | `def usage(self)` |
| `verify` | method | `modules/lazy_loop.py:7478` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2708` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:607` | `def wake_task(task_id)` |
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
| `switch_tenant` | method | `modules/lazy_rbac.py:486` | `def switch_tenant(self, tenant_id)` |
| `to_dict` | method | `modules/lazy_rbac.py:136` | `def to_dict(self)` |
| `to_dict` | method | `modules/lazy_rbac.py:386` | `def to_dict(self)` |
| `update_role` | method | `modules/lazy_rbac.py:304` | `def update_role(self, user_id, new_role)` |
| `valid_roles` | method | `modules/lazy_rbac.py:62` | `def valid_roles(cls)` |
| `verify_recovery_code` | method | `modules/lazy_rbac.py:192` | `def verify_recovery_code(self, code)` |
| `verify_totp` | method | `modules/lazy_rbac.py:187` | `def verify_totp(self, token)` |
| `_expire` | function | `modules/lazy_reaper.py:92` | `def _expire(store, task_id)` |
| `_log` | function | `modules/lazy_reaper.py:115` | `def _log(log_path, row)` |
| `reap` | function | `modules/lazy_reaper.py:30` | `def reap(store, log_path, now, stale_seconds)` |
| `conformance` | function | `modules/lazy_roles.py:154` | `def conformance(role)` |
| `list_roles` | function | `modules/lazy_roles.py:100` | `def list_roles()` |
| `role_prompt` | function | `modules/lazy_roles.py:109` | `def role_prompt(role, goal, context)` |
| `roles_for_phase` | function | `modules/lazy_roles.py:134` | `def roles_for_phase(phase)` |
| `LoopRunConfig` | class | `modules/lazy_runner.py:94` | `class LoopRunConfig` |
| `ThreadStdoutRouter` | class | `modules/lazy_runner.py:45` | `class ThreadStdoutRouter(TextIOBase)` |
| `__init__` | method | `modules/lazy_runner.py:55` | `def __init__(self, main_stream, spool)` |
| `_abort_run` | function | `modules/lazy_runner.py:411` | `def _abort_run(engine, task_id, reason)` |
| `_apply_budget` | function | `modules/lazy_runner.py:613` | `def _apply_budget(engine, task_id, budget)` |
| `_bootstrap` | function | `modules/lazy_runner.py:592` | `def _bootstrap(scan_target, executor)` |
| `_budget_declined` | function | `modules/lazy_runner.py:626` | `def _budget_declined(config)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:772` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:363` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:758` | `def _format_activity(record)` |
| `_limited` | function | `modules/lazy_runner.py:1150` | `def _limited()` |
| `_maybe_phishing_fallback` | function | `modules/lazy_runner.py:475` | `def _maybe_phishing_fallback(result, config, params)` |
| `_overview` | function | `modules/lazy_runner.py:748` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:801` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:430` | `def _prepare_engine(engine, shell, config, params)` |
| `_print_handoff` | function | `modules/lazy_runner.py:567` | `def _print_handoff(handoff)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:355` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:694` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:919` | `def _run_plain(engine, config)` |
| `_run_targets_file` | function | `modules/lazy_runner.py:1124` | `def _run_targets_file(shell, params, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:642` | `def _run_with_progress(engine, config)` |
| `_stall_thresholds` | function | `modules/lazy_runner.py:787` | `def _stall_thresholds(verb_timeout)` |
| `_start_proxy` | function | `modules/lazy_runner.py:450` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:897` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:164` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:156` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:1111` | `def _tty_available()` |
| `_work_one` | function | `modules/lazy_runner.py:1147` | `def _work_one(target)` |
| `_write` | function | `modules/lazy_runner.py:909` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:338` | `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` |
| `clamped` | method | `modules/lazy_runner.py:120` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:80` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:72` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:84` | `def isatty(self)` |
| `load_targets_file` | function | `modules/lazy_runner.py:954` | `def load_targets_file(path)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:172` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:521` | `def report_result(result)` |
| `resolve_loop_defaults` | function | `modules/lazy_runner.py:302` | `def resolve_loop_defaults(config)` |
| `run_loop` | function | `modules/lazy_runner.py:1009` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:657` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:61` | `def write(self, data)` |
| `_payload_value` | function | `modules/lazy_sandbox.py:41` | `def _payload_value(key, default)` |
| `_sandbox_executor` | function | `modules/lazy_sandbox.py:265` | `def _sandbox_executor(command)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
