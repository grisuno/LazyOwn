# Symbols (page 13 of 52)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_load` | function | `modules/campaign_blacklist.py:27` | `def _load()` |
| `blocked_commands` | function | `modules/campaign_blacklist.py:63` | `def blocked_commands(category)` |
| `campaign_blacklist` | function | `modules/campaign_blacklist.py:53` | `def campaign_blacklist()` |
| `PendingStore` | class | `modules/chain_approval.py:114` | `class PendingStore` |
| `__init__` | method | `modules/chain_approval.py:117` | `def __init__(self, sessions_dir)` |
| `_audit` | function | `modules/chain_approval.py:91` | `def _audit(sessions_dir, event)` |
| `_audit_path` | function | `modules/chain_approval.py:73` | `def _audit_path(sessions_dir)` |
| `_clamp_timeout` | function | `modules/chain_approval.py:52` | `def _clamp_timeout(value)` |
| `_load` | method | `modules/chain_approval.py:125` | `def _load(self)` |
| `_now` | function | `modules/chain_approval.py:47` | `def _now()` |
| `_save` | method | `modules/chain_approval.py:141` | `def _save(self, payload)` |
| `_store_path` | function | `modules/chain_approval.py:68` | `def _store_path(sessions_dir)` |
| `approval_backend` | function | `modules/chain_approval.py:318` | `def approval_backend()` |
| `approve` | function | `modules/chain_approval.py:358` | `def approve(step_id, command)` |
| `build_c2_approver` | function | `modules/chain_approval.py:328` | `def build_c2_approver(printer, chain_name, run_id, timeout, poll_interval, sessions_dir, clock)` |
| `command_fingerprint` | function | `modules/chain_approval.py:78` | `def command_fingerprint(command)` |
| `create` | method | `modules/chain_approval.py:153` | `def create(self, chain, step_id, command, timeout, run_id, now_override)` |
| `decide` | method | `modules/chain_approval.py:229` | `def decide(self, request_id, allowed, decided_by, note, expired)` |
| `expire_stale` | method | `modules/chain_approval.py:282` | `def expire_stale(self, now)` |
| `get` | method | `modules/chain_approval.py:204` | `def get(self, request_id)` |
| `list` | method | `modules/chain_approval.py:215` | `def list(self, status)` |
| `DistillReport` | class | `modules/chain_distill.py:479` | `class DistillReport` |
| `StepDecision` | class | `modules/chain_distill.py:458` | `class StepDecision` |
| `_artifact_pins` | function | `modules/chain_distill.py:338` | `def _artifact_pins(command, output, target)` |
| `_command_index_phases` | function | `modules/chain_distill.py:249` | `def _command_index_phases()` |
| `_command_verb` | function | `modules/chain_distill.py:229` | `def _command_verb(command)` |
| `_excluded_host` | function | `modules/chain_distill.py:374` | `def _excluded_host(host, operator_deny)` |
| `_infer_target` | function | `modules/chain_distill.py:418` | `def _infer_target(rows, graph, operator_deny)` |
| `_is_doc_example` | function | `modules/chain_distill.py:310` | `def _is_doc_example(host)` |
| `_is_failed` | function | `modules/chain_distill.py:213` | `def _is_failed(row)` |
| `_is_prose` | function | `modules/chain_distill.py:198` | `def _is_prose(command)` |
| `_load_graph` | function | `modules/chain_distill.py:172` | `def _load_graph(path)` |
| `_load_traffic` | function | `modules/chain_distill.py:136` | `def _load_traffic(path)` |
| `_operator_deny` | function | `modules/chain_distill.py:400` | `def _operator_deny(sessions_dir)` |
| `_phase_for` | function | `modules/chain_distill.py:278` | `def _phase_for(command, manifest_phase)` |
| `_slug` | function | `modules/chain_distill.py:80` | `def _slug(text)` |
| `build_chain_data` | function | `modules/chain_distill.py:574` | `def build_chain_data(task, rows, graph, manifests)` |
| `distill` | function | `modules/chain_distill.py:687` | `def distill(task, sessions_dir, write, chains_dir)` |
| `dropped` | method | `modules/chain_distill.py:512` | `def dropped(self)` |
| `kept` | method | `modules/chain_distill.py:507` | `def kept(self)` |
| `locate_traces` | function | `modules/chain_distill.py:93` | `def locate_traces(task, sessions_dir)` |
| `note` | function | `modules/chain_distill.py:598` | `def note(row, kept, reason)` |
| `render` | method | `modules/chain_distill.py:543` | `def render(self, verbose)` |
| `to_dict` | method | `modules/chain_distill.py:516` | `def to_dict(self)` |
| `_default_store` | function | `modules/chain_facts.py:73` | `def _default_store()` |
| `_host_hint` | function | `modules/chain_facts.py:84` | `def _host_hint(output, phase, target_hint)` |
| `spool_chain_outputs` | function | `modules/chain_facts.py:24` | `def spool_chain_outputs(result, sessions_dir, fact_store_factory)` |
| `FamilyRegistry` | class | `modules/chain_family.py:62` | `class FamilyRegistry` |
| `__init__` | method | `modules/chain_family.py:70` | `def __init__(self, path)` |
| `_default_registry_path` | function | `modules/chain_family.py:172` | `def _default_registry_path()` |
| `_load` | method | `modules/chain_family.py:78` | `def _load(self)` |
| `_normalize_service` | function | `modules/chain_family.py:28` | `def _normalize_service(name)` |
| `_save` | method | `modules/chain_family.py:84` | `def _save(self, data)` |
| `_touch` | method | `modules/chain_family.py:90` | `def _touch(self, signature, chain)` |
| `best` | method | `modules/chain_family.py:117` | `def best(self, signature)` |
| `default_registry` | function | `modules/chain_family.py:179` | `def default_registry()` |
| `family_signature` | function | `modules/chain_family.py:35` | `def family_signature(facts)` |
| `record_association` | method | `modules/chain_family.py:105` | `def record_association(self, signature, chain, target)` |
| `record_win` | method | `modules/chain_family.py:111` | `def record_win(self, signature, chain, target)` |
| `transfer_note` | method | `modules/chain_family.py:153` | `def transfer_note(self, facts)` |
| `ChainStepBlocked` | class | `modules/chain_loop.py:123` | `class ChainStepBlocked(RuntimeError)` |
| `__init__` | method | `modules/chain_loop.py:126` | `def __init__(self, status, detail)` |
| `_build_runner` | function | `modules/chain_loop.py:255` | `def _build_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent)` |
| `_render_summary` | function | `modules/chain_loop.py:306` | `def _render_summary(result, chain_name)` |
| `_spool` | function | `modules/chain_loop.py:296` | `def _spool(result)` |
| `chain_mode` | function | `modules/chain_loop.py:35` | `def chain_mode()` |
| `guarded` | function | `modules/chain_loop.py:210` | `def guarded(step_command)` |
| `is_chain_command` | function | `modules/chain_loop.py:53` | `def is_chain_command(command)` |
| `on_step` | function | `modules/chain_loop.py:267` | `def on_step(outcome)` |
| `parse_chain_invocation` | function | `modules/chain_loop.py:58` | `def parse_chain_invocation(command)` |
| `run_chain_stepwise` | function | `modules/chain_loop.py:138` | `def run_chain_stepwise(worker, intent, command, executor, budget, intercept, retry_state)` |
| `stepwise_eligible` | function | `modules/chain_loop.py:93` | `def stepwise_eligible(chain, routable)` |
| `best_chain` | function | `modules/chain_match.py:139` | `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` |
| `load_rows` | function | `modules/chain_match.py:109` | `def load_rows(allow_lab, ttl)` |
| `normalize_tags` | function | `modules/chain_match.py:49` | `def normalize_tags(tags)` |
| `platform_ok` | function | `modules/chain_match.py:75` | `def platform_ok(platforms, os_hint)` |
| `reset_cache` | function | `modules/chain_match.py:101` | `def reset_cache()` |
| `score` | function | `modules/chain_match.py:86` | `def score(tags, phase, svc_tokens)` |
| `service_tokens` | function | `modules/chain_match.py:65` | `def service_tokens(services)` |
| `Chain` | class | `modules/chain_registry.py:158` | `class Chain` |
| `ChainStep` | class | `modules/chain_registry.py:104` | `class ChainStep` |
| `_eval` | function | `modules/chain_registry.py:360` | `def _eval(node)` |
| `_materialize` | function | `modules/chain_registry.py:681` | `def _materialize(name, raw, stack)` |
| `_nonneg_float` | function | `modules/chain_registry.py:737` | `def _nonneg_float(raw, ceiling)` |
| `_nonneg_int` | function | `modules/chain_registry.py:728` | `def _nonneg_int(raw)` |
| `_step_from_raw` | function | `modules/chain_registry.py:748` | `def _step_from_raw(item)` |
| `_when_tree` | function | `modules/chain_registry.py:311` | `def _when_tree(expression)` |
| `chain_preview_lines` | function | `modules/chain_registry.py:627` | `def chain_preview_lines(chain)` |
| `evaluate_when` | function | `modules/chain_registry.py:338` | `def evaluate_when(expression, variables)` |
| `generate_for_playbook` | function | `modules/chain_registry.py:893` | `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` |
| `get` | function | `modules/chain_registry.py:805` | `def get(name, chains_dir)` |
| `identifier` | method | `modules/chain_registry.py:152` | `def identifier(self)` |
| `load_all` | function | `modules/chain_registry.py:647` | `def load_all(chains_dir)` |
| `render_text` | function | `modules/chain_registry.py:219` | `def render_text(template, variables)` |
| `resolve` | method | `modules/chain_registry.py:176` | `def resolve(self, tokens)` |
| `scan_all` | function | `modules/chain_registry.py:810` | `def scan_all(chains_dir)` |
| `set_enabled` | function | `modules/chain_registry.py:870` | `def set_enabled(name, enabled, chains_dir)` |
| `skip_pending` | function | `modules/chain_registry.py:69` | `def skip_pending(path, max_age, now)` |
| `step_gate_verdict` | function | `modules/chain_registry.py:242` | `def step_gate_verdict(step, render, variables, dependency_reason)` |
| `validate_chain` | function | `modules/chain_registry.py:403` | `def validate_chain(data, filename, chains_dir)` |
| `ChainRunResult` | class | `modules/chain_runner.py:122` | `class ChainRunResult` |
| `ChainRunner` | class | `modules/chain_runner.py:231` | `class ChainRunner` |
| `ReplanContext` | class | `modules/chain_runner.py:184` | `class ReplanContext` |
| `StepOutcome` | class | `modules/chain_runner.py:65` | `class StepOutcome` |
| `__init__` | method | `modules/chain_runner.py:234` | `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff, total_timeout...` |
| `_all_json_objects` | function | `modules/chain_runner.py:1576` | `def _all_json_objects(text)` |
| `_apply_replanner` | method | `modules/chain_runner.py:948` | `def _apply_replanner(self, result, index, outcome, steps, step_index, variables, captured_keys)` |
| `_ask_approval` | method | `modules/chain_runner.py:1269` | `def _ask_approval(self, step_id, command)` |
| `_call` | method | `modules/chain_runner.py:1550` | `def _call(callback, timeout)` |
| `_deliver` | method | `modules/chain_runner.py:809` | `def _deliver(self, outcome)` |
| `_dependency_block` | method | `modules/chain_runner.py:1202` | `def _dependency_block(step, prior_verdicts)` |
| `_execute` | method | `modules/chain_runner.py:1385` | `def _execute(self, command, timeout, expect_exits)` |
| `_finalize_verdict` | method | `modules/chain_runner.py:546` | `def _finalize_verdict(self, result)` |
| `_first_json` | method | `modules/chain_runner.py:1340` | `def _first_json(output)` |
| `_is_verb` | method | `modules/chain_runner.py:1469` | `def _is_verb(self, command)` |
| `_load_json_events` | function | `modules/chain_runner.py:1597` | `def _load_json_events(path)` |
| `_notify` | method | `modules/chain_runner.py:939` | `def _notify(self, outcome)` |
| `_pace_after` | method | `modules/chain_runner.py:320` | `def _pace_after(self, outcome, started, step)` |
| `_pre_check_timeout` | method | `modules/chain_runner.py:1284` | `def _pre_check_timeout(self, step)` |
| `_promoted_sinks` | method | `modules/chain_runner.py:814` | `def _promoted_sinks(self, outcome)` |
| `_publish_step` | method | `modules/chain_runner.py:839` | `def _publish_step(self, outcome)` |
| `_raise_timeout` | function | `modules/chain_runner.py:1513` | `def _raise_timeout(_signum, _frame)` |
| `_record_replan_deviations` | method | `modules/chain_runner.py:998` | `def _record_replan_deviations(self, context)` |
| `_record_verdict` | method | `modules/chain_runner.py:1078` | `def _record_verdict(verdicts, outcome)` |
| `_render_command` | method | `modules/chain_runner.py:1354` | `def _render_command(self, template, variables, captured_keys)` |
| `_run_fallback_chain` | method | `modules/chain_runner.py:736` | `def _run_fallback_chain(self, result, variables, captured_keys, started)` |
| `_run_parallel_group` | method | `modules/chain_runner.py:642` | `def _run_parallel_group(self, group, executions, resumed_ok, variables, captured_keys, prior_verdicts)` |
| `_run_raw` | method | `modules/chain_runner.py:1533` | `def _run_raw(self, command, timeout, allowed)` |
| `_run_shell_verb` | method | `modules/chain_runner.py:1480` | `def _run_shell_verb(self, command, timeout)` |
| `_run_step` | method | `modules/chain_runner.py:1085` | `def _run_step(self, step, variables, captured_keys, prior_verdicts)` |
| `_run_verb_bounded` | method | `modules/chain_runner.py:1439` | `def _run_verb_bounded(self, command, limit)` |
| `_save_checkpoint` | method | `modules/chain_runner.py:1040` | `def _save_checkpoint(self, result, variables, captured_keys, next_index, state_name, verdicts)` |
| `_skip_remaining` | method | `modules/chain_runner.py:590` | `def _skip_remaining(self, steps, start, reason)` |
| `_store_capture` | method | `modules/chain_runner.py:1288` | `def _store_capture(self, step, output, outcome, variables, captured_keys)` |
| `_verb_timeout_on_main` | method | `modules/chain_runner.py:1420` | `def _verb_timeout_on_main(self, limit)` |
| `_verify_evidence` | method | `modules/chain_runner.py:1224` | `def _verify_evidence(self, step, outcome, variables)` |
| `_verify_timeout` | method | `modules/chain_runner.py:1278` | `def _verify_timeout(self, step)` |
| `_warn_parallel_group` | method | `modules/chain_runner.py:605` | `def _warn_parallel_group(self, result, first, group, steps, cursor)` |
| `applied_vars` | method | `modules/chain_runner.py:216` | `def applied_vars(self)` |
| `chain_proven` | method | `modules/chain_runner.py:178` | `def chain_proven(self)` |
| `insert_step` | method | `modules/chain_runner.py:206` | `def insert_step(self, step)` |
| `inserted` | method | `modules/chain_runner.py:221` | `def inserted(self)` |
| `ok` | method | `modules/chain_runner.py:94` | `def ok(self)` |
| `run` | method | `modules/chain_runner.py:359` | `def run(self)` |
| `set_var` | method | `modules/chain_runner.py:201` | `def set_var(self, name, value)` |
| `skip_rest` | method | `modules/chain_runner.py:211` | `def skip_rest(self)` |
| `skip_rest_flag` | method | `modules/chain_runner.py:226` | `def skip_rest_flag(self)` |
| `to_dict` | method | `modules/chain_runner.py:98` | `def to_dict(self)` |
| `to_dict` | method | `modules/chain_runner.py:153` | `def to_dict(self)` |
| `checkpoint_dir` | function | `modules/chain_state.py:26` | `def checkpoint_dir(base_dir)` |
| `list_checkpoints` | function | `modules/chain_state.py:80` | `def list_checkpoints(directory, limit, chain)` |
| `load_checkpoint` | function | `modules/chain_state.py:65` | `def load_checkpoint(directory, run_id)` |
| `new_run_id` | function | `modules/chain_state.py:33` | `def new_run_id(chain_name)` |
| `write_checkpoint` | function | `modules/chain_state.py:39` | `def write_checkpoint(directory, state)` |
| `_service_steps` | function | `modules/chain_synth.py:44` | `def _service_steps(host, services)` |
| `_slug` | function | `modules/chain_synth.py:31` | `def _slug(name)` |
| `_wordlist` | function | `modules/chain_synth.py:35` | `def _wordlist(param, fallback)` |
| `facts_for_target` | function | `modules/chain_synth.py:243` | `def facts_for_target(target)` |
| `synth_chain_data` | function | `modules/chain_synth.py:91` | `def synth_chain_data(playbook, target, services, has_creds, os_hint, include_c2, techniques)` |
| `synth_technique_chain_data` | function | `modules/chain_synth.py:272` | `def synth_technique_chain_data(target, techniques, os_hint)` |
| `write_generated_chain` | function | `modules/chain_synth.py:339` | `def write_generated_chain(data, chains_dir)` |
| `_candidate_files` | function | `modules/chain_tokens.py:115` | `def _candidate_files()` |
| `_load_host_facts` | function | `modules/chain_tokens.py:72` | `def _load_host_facts(host)` |
| `_mentions` | function | `modules/chain_tokens.py:125` | `def _mentions(path, needle)` |
| `_newest_creds_file` | function | `modules/chain_tokens.py:88` | `def _newest_creds_file(host)` |
| `build_tokens` | function | `modules/chain_tokens.py:24` | `def build_tokens(target, params)` |
| `CICDEnumerator` | class | `modules/cicd_enumerator.py:43` | `class CICDEnumerator` |
| `CICDFinding` | class | `modules/cicd_enumerator.py:33` | `class CICDFinding` |
| `__init__` | method | `modules/cicd_enumerator.py:54` | `def __init__(self, target_url, sessions_dir)` |
| `_check_azure_devops` | method | `modules/cicd_enumerator.py:230` | `def _check_azure_devops(self)` |
| `_check_bitbucket` | method | `modules/cicd_enumerator.py:266` | `def _check_bitbucket(self)` |
| `_check_github_actions` | method | `modules/cicd_enumerator.py:189` | `def _check_github_actions(self)` |
| `_check_gitlab` | method | `modules/cicd_enumerator.py:120` | `def _check_gitlab(self)` |
| `_check_jenkins` | method | `modules/cicd_enumerator.py:73` | `def _check_jenkins(self)` |
| `export_findings` | method | `modules/cicd_enumerator.py:387` | `def export_findings(self)` |
| `generate_ci_attack_matrix` | method | `modules/cicd_enumerator.py:322` | `def generate_ci_attack_matrix(self)` |
| `scan` | method | `modules/cicd_enumerator.py:60` | `def scan(self)` |
| `scan_build_log` | method | `modules/cicd_enumerator.py:297` | `def scan_build_log(self, log_content, source)` |
| `_clear_cli_session` | function | `modules/cli_auth.py:478` | `def _clear_cli_session()` |
| `_load_payload` | function | `modules/cli_auth.py:85` | `def _load_payload()` |
| `_load_users` | function | `modules/cli_auth.py:34` | `def _load_users()` |
| `_read_cli_session` | function | `modules/cli_auth.py:429` | `def _read_cli_session()` |
| `_save_payload` | function | `modules/cli_auth.py:100` | `def _save_payload(payload)` |
| `_save_users` | function | `modules/cli_auth.py:52` | `def _save_users(users)` |
| `_write_cli_session` | function | `modules/cli_auth.py:444` | `def _write_cli_session(username, elo, role)` |
| `_write_cli_session_raw` | function | `modules/cli_auth.py:462` | `def _write_cli_session_raw(data)` |
| `get_current_operator` | function | `modules/cli_auth.py:396` | `def get_current_operator()` |
| `login` | function | `modules/cli_auth.py:240` | `def login(username, password, remember)` |
| `logout` | function | `modules/cli_auth.py:293` | `def logout()` |
| `needs_login` | function | `modules/cli_auth.py:487` | `def needs_login()` |
| `register` | function | `modules/cli_auth.py:145` | `def register(username, password)` |
| `sync_elo_from_session` | function | `modules/cli_auth.py:408` | `def sync_elo_from_session(elo)` |
| `try_auto_login` | function | `modules/cli_auth.py:328` | `def try_auto_login()` |
| `user_exists` | function | `modules/cli_auth.py:122` | `def user_exists(username)` |
| `verify_password` | function | `modules/cli_auth.py:214` | `def verify_password(username, password)` |
| `whoami` | function | `modules/cli_auth.py:366` | `def whoami()` |
| `Comparison` | class | `modules/closedloop.py:55` | `class Comparison` |
| `RuleMetrics` | class | `modules/closedloop.py:32` | `class RuleMetrics` |
| `_metrics_for` | function | `modules/closedloop.py:77` | `def _metrics_for(result)` |
| `compare_rules` | function | `modules/closedloop.py:90` | `def compare_rules(baseline_rule, candidate_rule, target_logs, control_logs)` |
| `suggest_tuning` | function | `modules/closedloop.py:136` | `def suggest_tuning(candidate, baseline)` |
| `to_dict` | method | `modules/closedloop.py:42` | `def to_dict(self)` |
| `to_dict` | method | `modules/closedloop.py:66` | `def to_dict(self)` |
| `CloudEnumerator` | class | `modules/cloud_enum.py:23` | `class CloudEnumerator` |
| `__init__` | method | `modules/cloud_enum.py:34` | `def __init__(self, provider, session, timeout)` |
| `_check_aws_privesc` | method | `modules/cloud_enum.py:526` | `def _check_aws_privesc(data)` |
| `_enumerate_aws_iam` | method | `modules/cloud_enum.py:390` | `def _enumerate_aws_iam(self)` |
| `_enumerate_aws_metadata` | method | `modules/cloud_enum.py:96` | `def _enumerate_aws_metadata(self)` |
| `_enumerate_azure_iam` | method | `modules/cloud_enum.py:421` | `def _enumerate_azure_iam(self)` |
| `_enumerate_azure_metadata` | method | `modules/cloud_enum.py:146` | `def _enumerate_azure_metadata(self)` |
| `_enumerate_azure_storage` | method | `modules/cloud_enum.py:316` | `def _enumerate_azure_storage(self, target_bucket)` |
| `_enumerate_gcp_iam` | method | `modules/cloud_enum.py:477` | `def _enumerate_gcp_iam(self)` |
| `_enumerate_gcp_metadata` | method | `modules/cloud_enum.py:193` | `def _enumerate_gcp_metadata(self)` |
| `_enumerate_gcs` | method | `modules/cloud_enum.py:350` | `def _enumerate_gcs(self, target_bucket)` |
| `_enumerate_s3` | method | `modules/cloud_enum.py:274` | `def _enumerate_s3(self, target_bucket)` |
| `detect_provider` | method | `modules/cloud_enum.py:47` | `def detect_provider(self)` |
| `enumerate_iam` | method | `modules/cloud_enum.py:372` | `def enumerate_iam(self)` |
| `enumerate_metadata` | method | `modules/cloud_enum.py:75` | `def enumerate_metadata(self)` |
| `enumerate_storage` | method | `modules/cloud_enum.py:251` | `def enumerate_storage(self, target_bucket)` |
| `full_enumeration` | method | `modules/cloud_enum.py:576` | `def full_enumeration(self)` |
| `ColabEvent` | class | `modules/collab_bp.py:163` | `class ColabEvent` |
| `EventBus` | class | `modules/collab_bp.py:188` | `class EventBus` |
| `LockManager` | class | `modules/collab_bp.py:257` | `class LockManager` |
| `OperatorInfo` | class | `modules/collab_bp.py:176` | `class OperatorInfo` |
| `OperatorRegistry` | class | `modules/collab_bp.py:314` | `class OperatorRegistry` |
| `TargetLock` | class | `modules/collab_bp.py:250` | `class TargetLock` |
| `__init__` | method | `modules/collab_bp.py:198` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:263` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:319` | `def __init__(self)` |
| `_authenticated_operator` | function | `modules/collab_bp.py:90` | `def _authenticated_operator()` |
| `_check_collab_permission` | function | `modules/collab_bp.py:100` | `def _check_collab_permission(perm_name)` |
| `_collab_login_required` | function | `modules/collab_bp.py:120` | `def _collab_login_required(f)` |
| `_collab_permission_required` | function | `modules/collab_bp.py:136` | `def _collab_permission_required(perm_name)` |
| `_expire` | method | `modules/collab_bp.py:297` | `def _expire(self)` |
| `_expire` | method | `modules/collab_bp.py:350` | `def _expire(self)` |
| `acquire` | method | `modules/collab_bp.py:267` | `def acquire(self, target, operator, ttl_secs)` |
| `active_operators` | method | `modules/collab_bp.py:345` | `def active_operators(self)` |
| `all_locks` | method | `modules/collab_bp.py:292` | `def all_locks(self)` |
| `collab_ui` | function | `modules/collab_bp.py:396` | `def collab_ui()` |
| `decorated` | function | `modules/collab_bp.py:84` | `def decorated()` |
| `decorated` | function | `modules/collab_bp.py:124` | `def decorated()` |
| `decorated` | function | `modules/collab_bp.py:141` | `def decorated()` |
| `decorator` | function | `modules/collab_bp.py:139` | `def decorator(f)` |
| `generate` | function | `modules/collab_bp.py:424` | `def generate()` |
| `get_event_bus` | function | `modules/collab_bp.py:370` | `def get_event_bus()` |
| `get_lock_manager` | function | `modules/collab_bp.py:374` | `def get_lock_manager()` |
| `get_operator_registry` | function | `modules/collab_bp.py:378` | `def get_operator_registry()` |
| `heartbeat` | method | `modules/collab_bp.py:334` | `def heartbeat(self, name)` |
| `history` | function | `modules/collab_bp.py:537` | `def history()` |
| `join` | method | `modules/collab_bp.py:323` | `def join(self, name)` |
| `leave` | method | `modules/collab_bp.py:340` | `def leave(self, name)` |
| `lock` | function | `modules/collab_bp.py:483` | `def lock()` |
| `locks` | function | `modules/collab_bp.py:522` | `def locks()` |
| `login_required` | function | `modules/collab_bp.py:80` | `def login_required(f)` |
| `operators` | function | `modules/collab_bp.py:458` | `def operators()` |
| `publish` | method | `modules/collab_bp.py:219` | `def publish(self, event)` |
| `publish` | function | `modules/collab_bp.py:470` | `def publish()` |
| `publish_event` | function | `modules/collab_bp.py:382` | `def publish_event(type, payload, operator)` |
| `recent` | method | `modules/collab_bp.py:234` | `def recent(self, n)` |
| `release` | method | `modules/collab_bp.py:279` | `def release(self, target, operator)` |
| `reset` | method | `modules/collab_bp.py:238` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:304` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:356` | `def reset(self)` |
| `status` | method | `modules/collab_bp.py:287` | `def status(self, target)` |
| `stream` | function | `modules/collab_bp.py:411` | `def stream()` |
| `subscribe` | method | `modules/collab_bp.py:203` | `def subscribe(self, subscriber_id)` |
| `to_sse` | method | `modules/collab_bp.py:170` | `def to_sse(self)` |
| `unlock` | function | `modules/collab_bp.py:504` | `def unlock()` |
| `unsubscribe` | method | `modules/collab_bp.py:215` | `def unsubscribe(self, subscriber_id)` |
| `delete_lines` | function | `modules/colors.py:68` | `def delete_lines(content, to_delete)` |
| `no_html` | function | `modules/colors.py:74` | `def no_html(content)` |
| `retModel` | function | `modules/colors.py:40` | `def retModel()` |
| `CommandExecutor` | class | `modules/command_executor.py:106` | `class CommandExecutor` |
| `ExecutionResult` | class | `modules/command_executor.py:97` | `class ExecutionResult` |
| `__init__` | method | `modules/command_executor.py:118` | `def __init__(self)` |
| `_argv` | method | `modules/command_executor.py:173` | `def _argv(self, command)` |
| `_default_writer` | method | `modules/command_executor.py:291` | `def _default_writer(line)` |
| `_fire_hooks` | method | `modules/command_executor.py:394` | `def _fire_hooks(self, result)` |
| `_kill_process_group` | function | `modules/command_executor.py:77` | `def _kill_process_group(proc)` |
| `_needs_shell` | method | `modules/command_executor.py:165` | `def _needs_shell(self, command)` |
| `_publish_event` | method | `modules/command_executor.py:401` | `def _publish_event(self, result)` |
| `_run_capture` | method | `modules/command_executor.py:296` | `def _run_capture(self, command, timeout)` |
| `_run_stream` | method | `modules/command_executor.py:321` | `def _run_stream(self, command, timeout)` |
| `add_hook` | method | `modules/command_executor.py:127` | `def add_hook(self, hook)` |
| `clear_thread_stdin_devnull` | function | `modules/command_executor.py:64` | `def clear_thread_stdin_devnull()` |
| `clear_thread_timeout` | function | `modules/command_executor.py:46` | `def clear_thread_timeout()` |
| `get_executor` | function | `modules/command_executor.py:426` | `def get_executor()` |
| `instance` | method | `modules/command_executor.py:122` | `def instance(cls)` |
| `run` | method | `modules/command_executor.py:131` | `def run(self, command, timeout, stream)` |
| `run_passthrough` | method | `modules/command_executor.py:179` | `def run_passthrough(self, command, env)` |
| `run_tee` | method | `modules/command_executor.py:194` | `def run_tee(self, command)` |
| `run_with_tee` | method | `modules/command_executor.py:358` | `def run_with_tee(self, command, output_path, timeout)` |
| `set_thread_stdin_devnull` | function | `modules/command_executor.py:59` | `def set_thread_stdin_devnull(enabled)` |
| `set_thread_timeout` | function | `modules/command_executor.py:41` | `def set_thread_timeout(seconds)` |
| `thread_stdin_devnull` | function | `modules/command_executor.py:72` | `def thread_stdin_devnull()` |
| `thread_timeout` | function | `modules/command_executor.py:54` | `def thread_timeout()` |
| `ComplianceEngine` | class | `modules/compliance.py:632` | `class ComplianceEngine` |
| `ComplianceFinding` | class | `modules/compliance.py:620` | `class ComplianceFinding` |
| `EvidenceChain` | class | `modules/compliance.py:349` | `class EvidenceChain` |
| `EvidenceEntry` | class | `modules/compliance.py:340` | `class EvidenceEntry` |
| `__init__` | method | `modules/compliance.py:357` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/compliance.py:635` | `def __init__(self, sessions_dir)` |
| `_append_to_file` | method | `modules/compliance.py:403` | `def _append_to_file(self, entry)` |
| `_compliance_finding` | method | `modules/compliance.py:780` | `def _compliance_finding(fact)` |
| `_count_by_category` | method | `modules/compliance.py:772` | `def _count_by_category(self, findings)` |
| `_count_by_severity` | method | `modules/compliance.py:765` | `def _count_by_severity(self, findings)` |
| `_format_compliance_report_md` | method | `modules/compliance.py:861` | `def _format_compliance_report_md(self, report)` |
| `_hash_entry` | method | `modules/compliance.py:379` | `def _hash_entry(self, entry)` |
| `_load` | method | `modules/compliance.py:364` | `def _load(self)` |
| `_load_findings` | method | `modules/compliance.py:808` | `def _load_findings(self)` |
| `add_evidence` | method | `modules/compliance.py:927` | `def add_evidence(self, filepath, operator, description)` |
| `add_file` | method | `modules/compliance.py:383` | `def add_file(self, filepath, operator, description)` |
| `export_pdf` | function | `modules/compliance.py:449` | `def export_pdf(report_md, output_path, title, classification)` |
| `export_pdf` | method | `modules/compliance.py:857` | `def export_pdf(self, report, output_path)` |
| `export_to_cef` | function | `modules/compliance.py:572` | `def export_to_cef(findings, output_path, vendor, product, version)` |
| `export_to_elastic_ndjson` | function | `modules/compliance.py:533` | `def export_to_elastic_ndjson(findings, output_path, index_prefix)` |
| `generate_compliance_report` | method | `modules/compliance.py:710` | `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` |
| `get_chain_digest` | method | `modules/compliance.py:429` | `def get_chain_digest(self)` |
| `map_findings_to_compliance` | method | `modules/compliance.py:639` | `def map_findings_to_compliance(self, findings, frameworks)` |
| `to_report` | method | `modules/compliance.py:432` | `def to_report(self)` |
| `verify` | method | `modules/compliance.py:410` | `def verify(self)` |
| `verify_evidence_chain` | method | `modules/compliance.py:930` | `def verify_evidence_chain(self)` |
| `HookEngine` | class | `modules/conditional_hooks.py:258` | `class HookEngine` |
| `HookRule` | class | `modules/conditional_hooks.py:45` | `class HookRule` |
| `__init__` | method | `modules/conditional_hooks.py:270` | `def __init__(self)` |
| `_execute_action` | method | `modules/conditional_hooks.py:428` | `def _execute_action(self, action, context)` |
| `_execute_cred_reuse` | method | `modules/conditional_hooks.py:500` | `def _execute_cred_reuse(self, context)` |
| `_execute_local_command` | method | `modules/conditional_hooks.py:476` | `def _execute_local_command(command)` |
| `_execute_shell_command` | method | `modules/conditional_hooks.py:467` | `def _execute_shell_command(self, command, context)` |
| `_match_trigger` | method | `modules/conditional_hooks.py:369` | `def _match_trigger(self, rule_trigger, event, context)` |
| `_resolve_placeholders` | method | `modules/conditional_hooks.py:414` | `def _resolve_placeholders(self, text, context)` |
| `add_rule` | method | `modules/conditional_hooks.py:330` | `def add_rule(self, rule_dict)` |
| `can_fire` | method | `modules/conditional_hooks.py:56` | `def can_fire(self, now)` |
| `enable_rule` | method | `modules/conditional_hooks.py:359` | `def enable_rule(self, name, enabled)` |
| `fire` | method | `modules/conditional_hooks.py:516` | `def fire(self, event, context)` |
| `get_hook_engine` | function | `modules/conditional_hooks.py:586` | `def get_hook_engine()` |
| `get_rule` | method | `modules/conditional_hooks.py:575` | `def get_rule(self, name)` |
| `list_rules` | method | `modules/conditional_hooks.py:571` | `def list_rules(self)` |
| `load_rules` | method | `modules/conditional_hooks.py:290` | `def load_rules(self, path)` |
| `mark_fired` | method | `modules/conditional_hooks.py:65` | `def mark_fired(self)` |
| `register_action_handler` | method | `modules/conditional_hooks.py:277` | `def register_action_handler(self, action_type, handler)` |
| `remove_rule` | method | `modules/conditional_hooks.py:345` | `def remove_rule(self, name)` |
| `save_rules` | method | `modules/conditional_hooks.py:322` | `def save_rules(self, path)` |
| `set_placeholders` | method | `modules/conditional_hooks.py:286` | `def set_placeholders(self, placeholders)` |
| `to_dict` | method | `modules/conditional_hooks.py:69` | `def to_dict(self)` |
| `_ensure_loaded` | function | `modules/config_store.py:106` | `def _ensure_loaded()` |
| `_load` | function | `modules/config_store.py:113` | `def _load()` |
| `_persist` | function | `modules/config_store.py:131` | `def _persist()` |
| `_start_watcher` | function | `modules/config_store.py:143` | `def _start_watcher(interval)` |
| `_watch_loop` | function | `modules/config_store.py:148` | `def _watch_loop()` |
| `get_config` | function | `modules/config_store.py:53` | `def get_config(key, default)` |
| `init` | function | `modules/config_store.py:36` | `def init(path, watch)` |
| `reload_config` | function | `modules/config_store.py:90` | `def reload_config()` |
| `set_config` | function | `modules/config_store.py:66` | `def set_config()` |
| `set_config_dict` | function | `modules/config_store.py:80` | `def set_config_dict(updates)` |
| `stop_watcher` | function | `modules/config_store.py:96` | `def stop_watcher()` |
| `CredentialReuseEngine` | class | `modules/credential_reuse.py:55` | `class CredentialReuseEngine` |
| `ReuseCandidate` | class | `modules/credential_reuse.py:32` | `class ReuseCandidate` |
| `__init__` | method | `modules/credential_reuse.py:80` | `def __init__(self)` |
| `_build_command` | method | `modules/credential_reuse.py:196` | `def _build_command(self, username, password, host, target_services)` |
| `_load_cache` | method | `modules/credential_reuse.py:85` | `def _load_cache(self)` |
| `_save_cache` | method | `modules/credential_reuse.py:95` | `def _save_cache(self)` |
| `_score_candidate` | method | `modules/credential_reuse.py:144` | `def _score_candidate(self, username, password, source_host, target_host, target_services)` |
| `_subnet_distance` | method | `modules/credential_reuse.py:118` | `def _subnet_distance(self, ip_a, ip_b)` |
| `get_credential_reuse_engine` | function | `modules/credential_reuse.py:358` | `def get_credential_reuse_engine()` |
| `get_summary` | method | `modules/credential_reuse.py:338` | `def get_summary(self, candidates)` |
| `mark_confirmed` | method | `modules/credential_reuse.py:112` | `def mark_confirmed(self, username, password, host)` |
| `mark_failed` | method | `modules/credential_reuse.py:107` | `def mark_failed(self, username, password, host)` |
| `rank` | method | `modules/credential_reuse.py:226` | `def rank(self, hosts, creds, host_services, limit)` |
| `suggest_from_state_manager` | method | `modules/credential_reuse.py:278` | `def suggest_from_state_manager(self, state_manager, limit)` |
| `suggest_from_world_model` | method | `modules/credential_reuse.py:308` | `def suggest_from_world_model(self, world_model, limit)` |
| `to_dict` | method | `modules/credential_reuse.py:43` | `def to_dict(self)` |
| `CrossCloudAttackEngine` | class | `modules/cross_cloud.py:54` | `class CrossCloudAttackEngine` |
| `CrossCloudConfig` | class | `modules/cross_cloud.py:30` | `class CrossCloudConfig` |
| `__init__` | method | `modules/cross_cloud.py:64` | `def __init__(self, config)` |
| `aws_oidc_to_gcp` | method | `modules/cross_cloud.py:133` | `def aws_oidc_to_gcp(self)` |
| `azure_saml_to_aws` | method | `modules/cross_cloud.py:67` | `def azure_saml_to_aws(self)` |
| `detect_cross_cloud_federation` | method | `modules/cross_cloud.py:234` | `def detect_cross_cloud_federation(self)` |
| `entra_id_to_gcp_workforce_federation` | method | `modules/cross_cloud.py:204` | `def entra_id_to_gcp_workforce_federation(self)` |
| `gcp_oidc_to_azure` | method | `modules/cross_cloud.py:104` | `def gcp_oidc_to_azure(self)` |
| `multi_cloud_imds_harvesting` | method | `modules/cross_cloud.py:167` | `def multi_cloud_imds_harvesting(self)` |
| `summary` | method | `modules/cross_cloud.py:258` | `def summary(self)` |
| `_check_credentials` | function | `modules/ctf_capture.py:86` | `def _check_credentials(output)` |
| `_check_defense_report` | function | `modules/ctf_capture.py:123` | `def _check_defense_report(output)` |
| `_check_domain_enum` | function | `modules/ctf_capture.py:162` | `def _check_domain_enum(output)` |
| `_check_eventlog_rows` | function | `modules/ctf_capture.py:136` | `def _check_eventlog_rows(output)` |
| `_check_kerberos_ticket` | function | `modules/ctf_capture.py:149` | `def _check_kerberos_ticket(output)` |
| `_check_root_shell` | function | `modules/ctf_capture.py:53` | `def _check_root_shell(output)` |
| `_check_shadow_dump` | function | `modules/ctf_capture.py:66` | `def _check_shadow_dump(output)` |
| `_check_smb_shares` | function | `modules/ctf_capture.py:175` | `def _check_smb_shares(output)` |
| `_check_windows_os_enum` | function | `modules/ctf_capture.py:104` | `def _check_windows_os_enum(output)` |
| `_cli_capture` | function | `modules/ctf_capture.py:481` | `def _cli_capture(argv)` |
| `_expected_checkers` | function | `modules/ctf_capture.py:244` | `def _expected_checkers(entry)` |
| `_gather_evidence` | function | `modules/ctf_capture.py:457` | `def _gather_evidence(candidates)` |
| `_publish_capture_outcome` | function | `modules/ctf_capture.py:340` | `def _publish_capture_outcome(record)` |
| `_safe_dir` | function | `modules/ctf_capture.py:376` | `def _safe_dir(vuln_id)` |
| `capture` | function | `modules/ctf_capture.py:275` | `def capture(vuln_id, target, output, sessions_dir, catalogue)` |
| `evaluate_exploit_output` | function | `modules/ctf_capture.py:203` | `def evaluate_exploit_output(output)` |
| `list_records` | function | `modules/ctf_capture.py:407` | `def list_records(sessions_dir)` |
| `output_dir` | function | `modules/ctf_capture.py:40` | `def output_dir(sessions_dir)` |
| `record_path` | function | `modules/ctf_capture.py:363` | `def record_path(vuln_id, sessions_dir)` |
| `store_record` | function | `modules/ctf_capture.py:389` | `def store_record(record, sessions_dir)` |
| `summary` | function | `modules/ctf_capture.py:430` | `def summary(sessions_dir)` |
| `_catalogue_modules` | function | `modules/ctf_signalman.py:39` | `def _catalogue_modules()` |
| `_gather_evidence` | function | `modules/ctf_signalman.py:72` | `def _gather_evidence(search_bases)` |
| `catalogue_for` | function | `modules/ctf_signalman.py:53` | `def catalogue_for(scenario)` |
| `collect` | function | `modules/ctf_signalman.py:106` | `def collect(scenario, target, sessions_dir, search_bases)` |
| `render_scoreboard` | function | `modules/ctf_signalman.py:166` | `def render_scoreboard(report)` |
| `save_scoreboard` | function | `modules/ctf_signalman.py:193` | `def save_scoreboard(report, sessions_dir)` |
| `_load` | function | `modules/custom_tools.py:37` | `def _load()` |
| `_run_http` | function | `modules/custom_tools.py:198` | `def _run_http(tool, arg, on_output)` |
| `_save` | function | `modules/custom_tools.py:45` | `def _save(payload)` |
| `_store_file` | function | `modules/custom_tools.py:30` | `def _store_file()` |
| `_trigger_tokens` | function | `modules/custom_tools.py:122` | `def _trigger_tokens(raw)` |
| `add_tool` | function | `modules/custom_tools.py:52` | `def add_tool(name, kind, target, description, method, body, timeout, trigger)` |
| `get_tool` | function | `modules/custom_tools.py:114` | `def get_tool(name)` |
| `list_tools` | function | `modules/custom_tools.py:109` | `def list_tools()` |
| `match_tools` | function | `modules/custom_tools.py:128` | `def match_tools(text, limit)` |
| `remove_tool` | function | `modules/custom_tools.py:97` | `def remove_tool(name)` |
| `run_custom_tool_line` | function | `modules/custom_tools.py:151` | `def run_custom_tool_line(command, on_output)` |
| `run_tool` | function | `modules/custom_tools.py:170` | `def run_tool(name, arg, on_output)` |
| `CVEMatcher` | class | `modules/cve_matcher.py:60` | `class CVEMatcher` |
| `CVEResult` | class | `modules/cve_matcher.py:51` | `class CVEResult` |
| `__init__` | method | `modules/cve_matcher.py:70` | `def __init__(self, api_key, cache_dir)` |
| `_cache_path` | method | `modules/cve_matcher.py:95` | `def _cache_path(self, params)` |
| `_load_cache` | method | `modules/cve_matcher.py:100` | `def _load_cache(self, params)` |
| `_query` | method | `modules/cve_matcher.py:128` | `def _query(self)` |
| `_rate_limit` | method | `modules/cve_matcher.py:121` | `def _rate_limit(self)` |
| `_save_cache` | method | `modules/cve_matcher.py:112` | `def _save_cache(self, params, results)` |
| `get_matcher` | function | `modules/cve_matcher.py:198` | `def get_matcher()` |
| `search` | method | `modules/cve_matcher.py:82` | `def search(self)` |
| `search` | function | `modules/cve_matcher.py:206` | `def search(product, version, max_results)` |
| `search_by_cpe` | method | `modules/cve_matcher.py:89` | `def search_by_cpe(self, cpe_name, max_results)` |
| `ACEntry` | class | `modules/dacl_abuse.py:67` | `class ACEntry` |
| `ACLTarget` | class | `modules/dacl_abuse.py:91` | `class ACLTarget` |
| `DACLAbuseEngine` | class | `modules/dacl_abuse.py:113` | `class DACLAbuseEngine` |
| `__init__` | method | `modules/dacl_abuse.py:136` | `def __init__(self, domain, domain_sid, acl_data)` |
| `_calculate_severity` | method | `modules/dacl_abuse.py:384` | `def _calculate_severity(target)` |
| `_extract_cn` | method | `modules/dacl_abuse.py:414` | `def _extract_cn(dn)` |
| `_guess_object_type` | method | `modules/dacl_abuse.py:397` | `def _guess_object_type(dn)` |
| `_is_dangerous_ace` | method | `modules/dacl_abuse.py:379` | `def _is_dangerous_ace(ace)` |
| `adminsdholder_abuse_plan` | method | `modules/dacl_abuse.py:291` | `def adminsdholder_abuse_plan(self, target_sid)` |
| `compute_attack_chains` | method | `modules/dacl_abuse.py:224` | `def compute_attack_chains(self)` |
| `dcsync_rights_assignment_plan` | method | `modules/dacl_abuse.py:318` | `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` |
| `owner_takeover_plan` | method | `modules/dacl_abuse.py:348` | `def owner_takeover_plan(self, target_dn, attacker_sid)` |
| `parse_bloodhound_acls` | method | `modules/dacl_abuse.py:143` | `def parse_bloodhound_acls(self, edges)` |
| `parse_raw_aces` | method | `modules/dacl_abuse.py:182` | `def parse_raw_aces(self, raw_nthashes)` |
| `summary` | method | `modules/dacl_abuse.py:418` | `def summary(self)` |
| `_aggregate_data` | function | `modules/dashboard_bp.py:113` | `def _aggregate_data()` |
| `_count_lines` | function | `modules/dashboard_bp.py:103` | `def _count_lines(path)` |
| `_normalize_ts` | function | `modules/dashboard_bp.py:913` | `def _normalize_ts(raw)` |
| `_read_json` | function | `modules/dashboard_bp.py:93` | `def _read_json(path)` |
| `_read_jsonl` | function | `modules/dashboard_bp.py:71` | `def _read_jsonl(path, last_n)` |
| `_read_loot` | function | `modules/dashboard_bp.py:817` | `def _read_loot()` |
| `_read_loot_lines` | function | `modules/dashboard_bp.py:800` | `def _read_loot_lines(pattern)` |
| `_read_timeline` | function | `modules/dashboard_bp.py:934` | `def _read_timeline()` |
| `_require_login` | function | `modules/dashboard_bp.py:30` | `def _require_login()` |
| `dashboard_api_data` | function | `modules/dashboard_bp.py:784` | `def dashboard_api_data()` |
| `dashboard_index` | function | `modules/dashboard_bp.py:778` | `def dashboard_index()` |
| `dashboard_loot` | function | `modules/dashboard_bp.py:902` | `def dashboard_loot()` |
| `dashboard_timeline` | function | `modules/dashboard_bp.py:1017` | `def dashboard_timeline()` |
| `DashboardEdge` | class | `modules/dashboard_engine.py:111` | `class DashboardEdge` |
| `DashboardEngine` | class | `modules/dashboard_engine.py:118` | `class DashboardEngine` |
| `DashboardNode` | class | `modules/dashboard_engine.py:99` | `class DashboardNode` |
| `__init__` | method | `modules/dashboard_engine.py:139` | `def __init__(self, world_model)` |
| `_parse_nmap_xml_services` | function | `modules/dashboard_engine.py:39` | `def _parse_nmap_xml_services(sessions_dir)` |
| `_phase_icon` | method | `modules/dashboard_engine.py:398` | `def _phase_icon(phase)` |
| `build_snapshot` | method | `modules/dashboard_engine.py:160` | `def build_snapshot(self)` |
| `export_json` | method | `modules/dashboard_engine.py:408` | `def export_json(self, snapshot)` |
| `format_for_cli` | method | `modules/dashboard_engine.py:438` | `def format_for_cli(self, snapshot)` |
| `persist_snapshot` | method | `modules/dashboard_engine.py:421` | `def persist_snapshot(self, snapshot)` |
| `render_ascii_topology` | method | `modules/dashboard_engine.py:358` | `def render_ascii_topology(self, snapshot)` |
| `render_text_map` | method | `modules/dashboard_engine.py:276` | `def render_text_map(self, snapshot)` |
| `set_auto_pivot` | method | `modules/dashboard_engine.py:154` | `def set_auto_pivot(self, pivot)` |
| `set_evasion_engine` | method | `modules/dashboard_engine.py:157` | `def set_evasion_engine(self, evasion)` |
| `set_exploit_recommender` | method | `modules/dashboard_engine.py:151` | `def set_exploit_recommender(self, recommender)` |
| `set_world_model` | method | `modules/dashboard_engine.py:148` | `def set_world_model(self, model)` |
| `LazyOwnDB` | class | `modules/db.py:147` | `class LazyOwnDB` |
| `__init__` | method | `modules/db.py:159` | `def __init__(self, db_path)` |
| `_current_version` | method | `modules/db.py:192` | `def _current_version(self)` |
| `_cursor` | method | `modules/db.py:235` | `def _cursor(self)` |
| `_get_conn` | method | `modules/db.py:171` | `def _get_conn(self)` |
| `_init_schema` | method | `modules/db.py:186` | `def _init_schema(self)` |
| `_maybe_decrypt` | method | `modules/db.py:273` | `def _maybe_decrypt(self, value)` |
| `_maybe_encrypt` | method | `modules/db.py:251` | `def _maybe_encrypt(self, value)` |
| `_run_migrations` | method | `modules/db.py:197` | `def _run_migrations(self)` |
| `close` | method | `modules/db.py:804` | `def close(self)` |
| `cred_add` | method | `modules/db.py:557` | `def cred_add(self, host_id, username, password, realm, cred_type, origin)` |
| `cred_list` | method | `modules/db.py:577` | `def cred_list(self, workspace_id)` |
| `db_path` | method | `modules/db.py:182` | `def db_path(self)` |
| `default_workspace` | method | `modules/db.py:320` | `def default_workspace(self, name)` |
| `export_csv` | method | `modules/db.py:740` | `def export_csv(self, table, workspace_id)` |
| `get_db` | function | `modules/db.py:821` | `def get_db(db_path)` |

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
