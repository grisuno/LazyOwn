# Symbols (page 17 of 48)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `queue` | method | `modules/lazy_loop.py:2757` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:7306` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:7986` | `def raw_entries(self, limit)` |
| `raw_entries_for_task` | method | `modules/lazy_loop.py:8000` | `def raw_entries_for_task(self, task_id, limit)` |
| `read` | method | `modules/lazy_loop.py:1541` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1671` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:7371` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:3986` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1649` | `def record(self, kind, command, output, meta)` |
| `record_call` | method | `modules/lazy_loop.py:7684` | `def record_call(self, member, ok, text)` |
| `record_fact` | method | `modules/lazy_loop.py:1458` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | function | `modules/lazy_loop.py:5084` | `def record_fact(text)` |
| `record_fact` | method | `modules/lazy_loop.py:9330` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:7974` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2387` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2375` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:9337` | `def record_verdict(self, task_id, finding_id, verdict, note)` |
| `recorder_blob` | method | `modules/lazy_loop.py:1760` | `def recorder_blob(self, digest, part, offset, length)` |
| `recorder_body` | method | `modules/lazy_loop.py:1731` | `def recorder_body(self, digest)` |
| `refine` | method | `modules/lazy_loop.py:3307` | `def refine(self)` |
| `register_worker` | function | `modules/lazy_loop.py:640` | `def register_worker(worker)` |
| `reload` | method | `modules/lazy_loop.py:1358` | `def reload(self)` |
| `remove` | method | `modules/lazy_loop.py:2297` | `def remove(self, rule_id, action)` |
| `remove` | method | `modules/lazy_loop.py:8370` | `def remove(self, name)` |
| `remove_channel` | method | `modules/lazy_loop.py:7478` | `def remove_channel(self, index)` |
| `remove_member` | method | `modules/lazy_loop.py:7651` | `def remove_member(self, name)` |
| `remove_rule` | method | `modules/lazy_loop.py:1939` | `def remove_rule(self, pattern)` |
| `reorder_evidence` | method | `modules/lazy_loop.py:1862` | `def reorder_evidence(self, finding_id, digests, graph)` |
| `repair_worker_command` | function | `modules/lazy_loop.py:340` | `def repair_worker_command(command, target)` |
| `report` | method | `modules/lazy_loop.py:7030` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `report_finding` | function | `modules/lazy_loop.py:5093` | `def report_finding(name, evidence, severity)` |
| `request` | method | `modules/lazy_loop.py:2529` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:3114` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:8272` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2735` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:9249` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:8878` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:6002` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:6166` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:9975` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_command` | function | `modules/lazy_loop.py:5058` | `def run_command(command, background)` |
| `run_round` | method | `modules/lazy_loop.py:9470` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:8229` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:8422` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:1087` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:510` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1627` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1685` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1597` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1696` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:10610` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:9272` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:8186` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:8481` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:8396` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:10488` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:8063` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2871` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:9016` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:1948` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2352` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2788` | `def set_llm_chain(self, task_id, members, active)` |
| `set_node_meta` | method | `modules/lazy_loop.py:1250` | `def set_node_meta(self, node_id, meta)` |
| `set_node_state` | method | `modules/lazy_loop.py:1231` | `def set_node_state(self, node_id, state)` |
| `set_priority` | method | `modules/lazy_loop.py:7661` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:7979` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2846` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1269` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2719` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:7267` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:6783` | `def settlement_prompt(agent, reason)` |
| `shell_open` | function | `modules/lazy_loop.py:5132` | `def shell_open()` |
| `shell_send` | function | `modules/lazy_loop.py:5136` | `def shell_send(command)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:652` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:3832` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:5611` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:8789` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:9521` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:2092` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:8339` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:10905` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:2917` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:2937` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:6379` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:8894` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:8888` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:867` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:8922` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:8913` | `def task_traces(self, task_id, query, limit)` |
| `templates` | method | `modules/lazy_loop.py:1791` | `def templates(self, limit)` |
| `terminal_hint` | function | `modules/lazy_loop.py:6844` | `def terminal_hint(reason, state)` |
| `trace` | method | `modules/lazy_loop.py:1559` | `def trace(self, intent_id, query, step_id, limit)` |
| `traffic_search` | function | `modules/lazy_loop.py:5104` | `def traffic_search(query)` |
| `unbind` | method | `modules/lazy_loop.py:8112` | `def unbind(self, agent, tool)` |
| `unfolded` | method | `modules/lazy_loop.py:6686` | `def unfolded(self, limit)` |
| `unregister_worker` | function | `modules/lazy_loop.py:646` | `def unregister_worker(worker)` |
| `untested` | method | `modules/lazy_loop.py:1100` | `def untested(self, limit)` |
| `untested_for` | method | `modules/lazy_loop.py:1133` | `def untested_for(self, graph, scope, limit)` |
| `update_finding_report` | method | `modules/lazy_loop.py:8928` | `def update_finding_report(self, task_id, finding_id, report)` |
| `update_report` | method | `modules/lazy_loop.py:7284` | `def update_report(self, finding_id, report)` |
| `usage` | method | `modules/lazy_loop.py:2365` | `def usage(self, task_id)` |
| `usage` | method | `modules/lazy_loop.py:7674` | `def usage(self)` |
| `verify` | method | `modules/lazy_loop.py:7342` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2617` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:606` | `def wake_task(task_id)` |
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
| `_apply_budget` | function | `modules/lazy_runner.py:606` | `def _apply_budget(engine, task_id, budget)` |
| `_bootstrap` | function | `modules/lazy_runner.py:592` | `def _bootstrap(scan_target, executor)` |
| `_budget_declined` | function | `modules/lazy_runner.py:619` | `def _budget_declined(config)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:765` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:363` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:751` | `def _format_activity(record)` |
| `_limited` | function | `modules/lazy_runner.py:1143` | `def _limited()` |
| `_maybe_phishing_fallback` | function | `modules/lazy_runner.py:475` | `def _maybe_phishing_fallback(result, config, params)` |
| `_overview` | function | `modules/lazy_runner.py:741` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:794` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:430` | `def _prepare_engine(engine, shell, config, params)` |
| `_print_handoff` | function | `modules/lazy_runner.py:567` | `def _print_handoff(handoff)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:355` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:687` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:912` | `def _run_plain(engine, config)` |
| `_run_targets_file` | function | `modules/lazy_runner.py:1117` | `def _run_targets_file(shell, params, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:635` | `def _run_with_progress(engine, config)` |
| `_stall_thresholds` | function | `modules/lazy_runner.py:780` | `def _stall_thresholds(verb_timeout)` |
| `_start_proxy` | function | `modules/lazy_runner.py:450` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:890` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:164` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:156` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:1104` | `def _tty_available()` |
| `_work_one` | function | `modules/lazy_runner.py:1140` | `def _work_one(target)` |
| `_write` | function | `modules/lazy_runner.py:902` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:338` | `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` |
| `clamped` | method | `modules/lazy_runner.py:120` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:80` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:72` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:84` | `def isatty(self)` |
| `load_targets_file` | function | `modules/lazy_runner.py:947` | `def load_targets_file(path)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:172` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:521` | `def report_result(result)` |
| `resolve_loop_defaults` | function | `modules/lazy_runner.py:302` | `def resolve_loop_defaults(config)` |
| `run_loop` | function | `modules/lazy_runner.py:1002` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:650` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:61` | `def write(self, data)` |
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
| `ScopeVerdict` | class | `modules/lazy_scope.py:50` | `class ScopeVerdict` |
| `_ResolveCache` | class | `modules/lazy_scope.py:65` | `class _ResolveCache` |
| `_address_denied` | function | `modules/lazy_scope.py:319` | `def _address_denied(address, denylist)` |
| `_entry_denied` | function | `modules/lazy_scope.py:332` | `def _entry_denied(text, lowered, denylist)` |
| `_keep` | function | `modules/lazy_scope.py:143` | `def _keep(start, value)` |
| `_looks_like_address` | function | `modules/lazy_scope.py:193` | `def _looks_like_address(text)` |
| `_networks_of` | function | `modules/lazy_scope.py:307` | `def _networks_of(entries)` |
| `command_scope_verdict` | function | `modules/lazy_scope.py:351` | `def command_scope_verdict(command, resolver, allowlist, denylist)` |
| `extract_hosts` | function | `modules/lazy_scope.py:130` | `def extract_hosts(text)` |
| `get` | method | `modules/lazy_scope.py:70` | `def get(self, name, now)` |
| `is_lab_address` | function | `modules/lazy_scope.py:105` | `def is_lab_address(address)` |
| `put` | method | `modules/lazy_scope.py:89` | `def put(self, name, values, now)` |
| `read_allowlist` | function | `modules/lazy_scope.py:231` | `def read_allowlist(sessions_dir)` |
| `read_denylist` | function | `modules/lazy_scope.py:243` | `def read_denylist(sessions_dir)` |
| `read_scope_file` | function | `modules/lazy_scope.py:209` | `def read_scope_file(name, sessions_dir)` |
| `resolve_addresses` | function | `modules/lazy_scope.py:164` | `def resolve_addresses(name, now)` |
| `scope_verdict` | function | `modules/lazy_scope.py:255` | `def scope_verdict(target, resolver, allowlist, denylist)` |
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
| `_load_previous` | function | `modules/lazy_surface_diff.py:149` | `def _load_previous(path)` |
| `_port_number` | function | `modules/lazy_surface_diff.py:85` | `def _port_number(key)` |
| `changed_hosts` | function | `modules/lazy_surface_diff.py:253` | `def changed_hosts(limit, sessions_dir)` |
| `current_snapshots` | function | `modules/lazy_surface_diff.py:160` | `def current_snapshots(world)` |
| `diff_hosts` | function | `modules/lazy_surface_diff.py:93` | `def diff_hosts(before, after)` |
| `fingerprint` | function | `modules/lazy_surface_diff.py:79` | `def fingerprint(state)` |
| `last_diff` | function | `modules/lazy_surface_diff.py:234` | `def last_diff(sessions_dir)` |
| `refresh` | function | `modules/lazy_surface_diff.py:186` | `def refresh(world, sessions_dir)` |
| `snapshot_host` | function | `modules/lazy_surface_diff.py:52` | `def snapshot_host(host)` |
| `SignatureStore` | class | `modules/lazy_triage.py:135` | `class SignatureStore` |
| `__init__` | method | `modules/lazy_triage.py:138` | `def __init__(self, sessions_dir, ttl)` |
| `_load` | method | `modules/lazy_triage.py:166` | `def _load(self)` |
| `_save` | method | `modules/lazy_triage.py:176` | `def _save(self, store)` |
| `apply_rules` | function | `modules/lazy_triage.py:80` | `def apply_rules(verdict, kind, facts)` |
| `fresh_signature` | method | `modules/lazy_triage.py:144` | `def fresh_signature(self, signature, now)` |
| `hard_evidence` | function | `modules/lazy_triage.py:47` | `def hard_evidence(kind, facts)` |
| `rank` | function | `modules/lazy_triage.py:42` | `def rank(verdict)` |
| `reset` | method | `modules/lazy_triage.py:162` | `def reset(self)` |
| `signature_for` | function | `modules/lazy_triage.py:108` | `def signature_for(kind, fields)` |
| `_add` | function | `modules/lazy_verify.py:104` | `def _add(kind, command, check_port)` |
| `_cap` | function | `modules/lazy_verify.py:52` | `def _cap(text, cap)` |
| `_host_port` | function | `modules/lazy_verify.py:57` | `def _host_port(finding_text, poc)` |
| `_nmap_available` | function | `modules/lazy_verify.py:133` | `def _nmap_available()` |
| `plan_checks` | function | `modules/lazy_verify.py:84` | `def plan_checks(finding_text, poc)` |
| `run_check` | function | `modules/lazy_verify.py:143` | `def run_check(check, executor)` |
| `verdict_from_checks` | function | `modules/lazy_verify.py:214` | `def verdict_from_checks(checks_results)` |
| `verify_finding` | function | `modules/lazy_verify.py:232` | `def verify_finding(finding_text, poc, executor)` |
| `SurfaceChange` | class | `modules/lazy_world_diff.py:65` | `class SurfaceChange` |
| `_as_change` | function | `modules/lazy_world_diff.py:192` | `def _as_change(change)` |
| `_changes_path` | function | `modules/lazy_world_diff.py:172` | `def _changes_path(sessions_dir)` |
| `_default_probe` | function | `modules/lazy_world_diff.py:415` | `def _default_probe(ip, port, scheme, host)` |
| `_default_resolve` | function | `modules/lazy_world_diff.py:406` | `def _default_resolve(host)` |
| `_load_changes` | function | `modules/lazy_world_diff.py:176` | `def _load_changes(sessions_dir)` |
| `_port_number` | function | `modules/lazy_world_diff.py:124` | `def _port_number(key)` |
| `campaign_snapshots` | function | `modules/lazy_world_diff.py:312` | `def campaign_snapshots(sessions_dir)` |
| `diff_snapshots` | function | `modules/lazy_world_diff.py:131` | `def diff_snapshots(before, after)` |
| `find_ghost_hosts` | function | `modules/lazy_world_diff.py:489` | `def find_ghost_hosts(candidates, snapshots, checker, resolver, cap)` |
| `ghost_endpoints` | function | `modules/lazy_world_diff.py:366` | `def ghost_endpoints(snapshot, limit)` |
| `ghost_state_apply` | function | `modules/lazy_world_diff.py:447` | `def ghost_state_apply(host, answers, sessions_dir, now)` |
| `host_snapshot` | function | `modules/lazy_world_diff.py:78` | `def host_snapshot(world, ip)` |
| `load_ghosts` | function | `modules/lazy_world_diff.py:435` | `def load_ghosts(sessions_dir)` |
| `load_host_snapshots` | function | `modules/lazy_world_diff.py:290` | `def load_host_snapshots(sessions_dir)` |
| `name_resolves` | function | `modules/lazy_world_diff.py:395` | `def name_resolves(host, resolver)` |
| `prune_changes` | function | `modules/lazy_world_diff.py:270` | `def prune_changes(sessions_dir, keep_days)` |
| `recent_changes` | function | `modules/lazy_world_diff.py:260` | `def recent_changes(sessions_dir, days, host)` |
| `record_changes` | function | `modules/lazy_world_diff.py:200` | `def record_changes(changes, sessions_dir, now)` |
| `save_host_snapshots` | function | `modules/lazy_world_diff.py:301` | `def save_host_snapshots(snapshots, sessions_dir)` |
| `snapshot_engagement` | function | `modules/lazy_world_diff.py:528` | `def snapshot_engagement(sessions_dir, now, world)` |
| `snapshot_fingerprint` | function | `modules/lazy_world_diff.py:119` | `def snapshot_fingerprint(state)` |
| `abusar_tar` | function | `modules/lazyatack.sh:248` | `` |
| `comprobar_rutas` | function | `modules/lazyatack.sh:242` | `` |
| `comprobar_sudo` | function | `modules/lazyatack.sh:194` | `` |
| `configurar_netcat` | function | `modules/lazyatack.sh:139` | `` |
| `configurar_shell_reversa` | function | `modules/lazyatack.sh:165` | `` |
| `configurar_tty` | function | `modules/lazyatack.sh:206` | `` |
| `descargar_seclists` | function | `modules/lazyatack.sh:107` | `` |
| `ejecutar_wfuzz` | function | `modules/lazyatack.sh:188` | `` |
| `eliminar_archivos` | function | `modules/lazyatack.sh:217` | `` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
