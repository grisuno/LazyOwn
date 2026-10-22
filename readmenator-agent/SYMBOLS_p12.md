# Symbols (page 12 of 44)
Previous: [SYMBOLS_p11.md](SYMBOLS_p11.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `PayloadConfigAdapter` | class | `modules/c2_messaging_base.py:117` | `class PayloadConfigAdapter` |
| `SecureSessionManager` | class | `modules/c2_messaging_base.py:9` | `class SecureSessionManager` |
| `__getitem__` | method | `modules/c2_messaging_base.py:129` | `def __getitem__(self, key)` |
| `__init__` | method | `modules/c2_messaging_base.py:22` | `def __init__(self, max_failed_attempts, lockout_duration, rate_limit, session_timeout)` |
| `__init__` | method | `modules/c2_messaging_base.py:124` | `def __init__(self, config_dict)` |
| `check_lockout` | method | `modules/c2_messaging_base.py:46` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `modules/c2_messaging_base.py:61` | `def check_rate_limit(self, user_id)` |
| `create_session` | method | `modules/c2_messaging_base.py:79` | `def create_session(self, user_id, client_id)` |
| `get` | method | `modules/c2_messaging_base.py:132` | `def get(self, key, default)` |
| `get_client` | method | `modules/c2_messaging_base.py:111` | `def get_client(self, user_id)` |
| `register_failed_attempt` | method | `modules/c2_messaging_base.py:37` | `def register_failed_attempt(self, user_id)` |
| `set_client` | method | `modules/c2_messaging_base.py:106` | `def set_client(self, user_id, client_id)` |
| `validate_session` | method | `modules/c2_messaging_base.py:89` | `def validate_session(self, user_id)` |
| `C2Profile` | class | `modules/c2_profile.py:81` | `class C2Profile` |
| `HttpConfig` | class | `modules/c2_profile.py:62` | `class HttpConfig` |
| `ProfileApplier` | class | `modules/c2_profile.py:520` | `class ProfileApplier` |
| `ProfileLoader` | class | `modules/c2_profile.py:187` | `class ProfileLoader` |
| `ProfileRegistry` | class | `modules/c2_profile.py:449` | `class ProfileRegistry` |
| `ProfileValidator` | class | `modules/c2_profile.py:155` | `class ProfileValidator` |
| `SleepConfig` | class | `modules/c2_profile.py:54` | `class SleepConfig` |
| `StagerConfig` | class | `modules/c2_profile.py:72` | `class StagerConfig` |
| `__init__` | method | `modules/c2_profile.py:457` | `def __init__(self)` |
| `_config_for` | method | `modules/c2_profile.py:144` | `def _config_for(self, method)` |
| `_make_aggressive_profile` | function | `modules/c2_profile.py:385` | `def _make_aggressive_profile()` |
| `_make_debug_profile` | function | `modules/c2_profile.py:410` | `def _make_debug_profile()` |
| `_make_default_profile` | function | `modules/c2_profile.py:308` | `def _make_default_profile()` |
| `_make_stealth_profile` | function | `modules/c2_profile.py:339` | `def _make_stealth_profile()` |
| `apply_to_response` | method | `modules/c2_profile.py:529` | `def apply_to_response(profile, response)` |
| `apply_to_session` | method | `modules/c2_profile.py:554` | `def apply_to_session(profile, session)` |
| `build_headers` | method | `modules/c2_profile.py:128` | `def build_headers(self, method)` |
| `from_dict` | method | `modules/c2_profile.py:215` | `def from_dict(d)` |
| `from_yaml` | method | `modules/c2_profile.py:200` | `def from_yaml(path)` |
| `get` | method | `modules/c2_profile.py:473` | `def get(self, name)` |
| `get_beacon_config` | method | `modules/c2_profile.py:567` | `def get_beacon_config(profile)` |
| `get_profile` | function | `modules/c2_profile.py:620` | `def get_profile(name)` |
| `get_registry` | function | `modules/c2_profile.py:595` | `def get_registry()` |
| `get_uri` | method | `modules/c2_profile.py:117` | `def get_uri(self, method)` |
| `jitter_delay` | method | `modules/c2_profile.py:101` | `def jitter_delay(self)` |
| `list_names` | method | `modules/c2_profile.py:485` | `def list_names(self)` |
| `list_profiles` | function | `modules/c2_profile.py:625` | `def list_profiles()` |
| `load_from_directory` | method | `modules/c2_profile.py:493` | `def load_from_directory(self, path)` |
| `register` | method | `modules/c2_profile.py:464` | `def register(self, name, profile)` |
| `save` | method | `modules/c2_profile.py:282` | `def save(profile, path)` |
| `to_dict` | method | `modules/c2_profile.py:254` | `def to_dict(profile)` |
| `validate` | method | `modules/c2_profile.py:162` | `def validate(self, profile)` |
| `DnsProfile` | class | `modules/c2_profile_engine.py:205` | `class DnsProfile` |
| `ProfileEngine` | class | `modules/c2_profile_engine.py:611` | `class ProfileEngine` |
| `ProfileRotator` | class | `modules/c2_profile_engine.py:441` | `class ProfileRotator` |
| `ProfileValidator` | class | `modules/c2_profile_engine.py:503` | `class ProfileValidator` |
| `RotationSlot` | class | `modules/c2_profile_engine.py:414` | `class RotationSlot` |
| `SmbProfile` | class | `modules/c2_profile_engine.py:289` | `class SmbProfile` |
| `TlsProfile` | class | `modules/c2_profile_engine.py:117` | `class TlsProfile` |
| `TransportType` | class | `modules/c2_profile_engine.py:404` | `class TransportType(Enum)` |
| `WebSocketProfile` | class | `modules/c2_profile_engine.py:349` | `class WebSocketProfile` |
| `__init__` | method | `modules/c2_profile_engine.py:453` | `def __init__(self, slots)` |
| `__init__` | method | `modules/c2_profile_engine.py:627` | `def __init__(self, tls_profile, dns_profile, smb_profile, websocket_profile, rotation_slots)` |
| `_default_slots` | method | `modules/c2_profile_engine.py:709` | `def _default_slots(self)` |
| `active_transport` | method | `modules/c2_profile_engine.py:668` | `def active_transport(self)` |
| `build_query_subdomain` | method | `modules/c2_profile_engine.py:231` | `def build_query_subdomain(self, data, packet_id)` |
| `current_slot` | method | `modules/c2_profile_engine.py:460` | `def current_slot(self)` |
| `dns_profile` | method | `modules/c2_profile_engine.py:648` | `def dns_profile(self)` |
| `from_config` | method | `modules/c2_profile_engine.py:771` | `def from_config(cls, config)` |
| `from_dict` | method | `modules/c2_profile_engine.py:173` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:261` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:319` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:375` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:747` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/c2_profile_engine.py:766` | `def from_payload(cls, payload)` |
| `get_active_profile_dict` | method | `modules/c2_profile_engine.py:685` | `def get_active_profile_dict(self)` |
| `get_all_profiles_dict` | method | `modules/c2_profile_engine.py:699` | `def get_all_profiles_dict(self)` |
| `get_cipher_suites` | method | `modules/c2_profile_engine.py:144` | `def get_cipher_suites(self)` |
| `get_ja3_hash` | method | `modules/c2_profile_engine.py:155` | `def get_ja3_hash(self)` |
| `is_available` | method | `modules/c2_profile_engine.py:429` | `def is_available(self)` |
| `list_slots` | method | `modules/c2_profile_engine.py:487` | `def list_slots(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:469` | `def rotate(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:672` | `def rotate(self)` |
| `rotator` | method | `modules/c2_profile_engine.py:663` | `def rotator(self)` |
| `smb_profile` | method | `modules/c2_profile_engine.py:653` | `def smb_profile(self)` |
| `tls_profile` | method | `modules/c2_profile_engine.py:643` | `def tls_profile(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:188` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:274` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:333` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:389` | `def to_dict(self)` |
| `touch` | method | `modules/c2_profile_engine.py:436` | `def touch(self)` |
| `transport` | method | `modules/c2_profile_engine.py:465` | `def transport(self)` |
| `validate` | method | `modules/c2_profile_engine.py:676` | `def validate(self)` |
| `validate_all` | method | `modules/c2_profile_engine.py:591` | `def validate_all(self, tls, dns, smb, websocket)` |
| `validate_dns` | method | `modules/c2_profile_engine.py:536` | `def validate_dns(profile)` |
| `validate_smb` | method | `modules/c2_profile_engine.py:556` | `def validate_smb(profile)` |
| `validate_tls` | method | `modules/c2_profile_engine.py:511` | `def validate_tls(profile)` |
| `validate_websocket` | method | `modules/c2_profile_engine.py:576` | `def validate_websocket(profile)` |
| `websocket_profile` | method | `modules/c2_profile_engine.py:658` | `def websocket_profile(self)` |
| `_normalize_task_title` | function | `modules/c2_surfaces.py:256` | `def _normalize_task_title(title)` |
| `_read_json` | function | `modules/c2_surfaces.py:42` | `def _read_json(path, default)` |
| `_stamp` | function | `modules/c2_surfaces.py:68` | `def _stamp()` |
| `_write_json` | function | `modules/c2_surfaces.py:54` | `def _write_json(path, data)` |
| `append_note` | function | `modules/c2_surfaces.py:155` | `def append_note(line, sessions_dir)` |
| `group_tasks_for_display` | function | `modules/c2_surfaces.py:261` | `def group_tasks_for_display(tasks)` |
| `publish_banner` | function | `modules/c2_surfaces.py:73` | `def publish_banner(hostname, port, protocol, service, extra, sessions_dir)` |
| `publish_cve` | function | `modules/c2_surfaces.py:115` | `def publish_cve(title, description, operator, risk, sessions_dir)` |
| `refresh_session_report` | function | `modules/c2_surfaces.py:229` | `def refresh_session_report(timeout)` |
| `register_loot_event` | function | `modules/c2_surfaces.py:184` | `def register_loot_event(name, path_glob, description, event_config)` |
| `severity_to_risk` | function | `modules/c2_surfaces.py:251` | `def severity_to_risk(severity)` |
| `days_in_month` | function | `modules/cal.sh:14` | `` |
| `first_day_of_month` | function | `modules/cal.sh:31` | `` |
| `is_leap_year` | function | `modules/cal.sh:4` | `` |
| `DistillReport` | class | `modules/chain_distill.py:333` | `class DistillReport` |
| `StepDecision` | class | `modules/chain_distill.py:312` | `class StepDecision` |
| `_command_verb` | function | `modules/chain_distill.py:225` | `def _command_verb(command)` |
| `_infer_target` | function | `modules/chain_distill.py:280` | `def _infer_target(rows, graph)` |
| `_is_failed` | function | `modules/chain_distill.py:209` | `def _is_failed(row)` |
| `_is_prose` | function | `modules/chain_distill.py:194` | `def _is_prose(command)` |
| `_load_graph` | function | `modules/chain_distill.py:168` | `def _load_graph(path)` |
| `_load_traffic` | function | `modules/chain_distill.py:132` | `def _load_traffic(path)` |
| `_phase_for` | function | `modules/chain_distill.py:245` | `def _phase_for(command, manifest_phase)` |
| `_slug` | function | `modules/chain_distill.py:76` | `def _slug(text)` |
| `build_chain_data` | function | `modules/chain_distill.py:428` | `def build_chain_data(task, rows, graph, manifests)` |
| `distill` | function | `modules/chain_distill.py:537` | `def distill(task, sessions_dir, write, chains_dir)` |
| `dropped` | method | `modules/chain_distill.py:366` | `def dropped(self)` |
| `kept` | method | `modules/chain_distill.py:361` | `def kept(self)` |
| `locate_traces` | function | `modules/chain_distill.py:89` | `def locate_traces(task, sessions_dir)` |
| `note` | function | `modules/chain_distill.py:452` | `def note(row, kept, reason)` |
| `render` | method | `modules/chain_distill.py:397` | `def render(self, verbose)` |
| `to_dict` | method | `modules/chain_distill.py:370` | `def to_dict(self)` |
| `Chain` | class | `modules/chain_registry.py:90` | `class Chain` |
| `ChainStep` | class | `modules/chain_registry.py:55` | `class ChainStep` |
| `_eval` | function | `modules/chain_registry.py:242` | `def _eval(node)` |
| `_materialize` | function | `modules/chain_registry.py:469` | `def _materialize(name, raw, stack)` |
| `_render` | function | `modules/chain_registry.py:164` | `def _render(template, variables)` |
| `_step_from_raw` | function | `modules/chain_registry.py:515` | `def _step_from_raw(item)` |
| `_when_tree` | function | `modules/chain_registry.py:193` | `def _when_tree(expression)` |
| `evaluate_when` | function | `modules/chain_registry.py:220` | `def evaluate_when(expression, variables)` |
| `generate_for_playbook` | function | `modules/chain_registry.py:638` | `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` |
| `get` | function | `modules/chain_registry.py:550` | `def get(name, chains_dir)` |
| `identifier` | method | `modules/chain_registry.py:84` | `def identifier(self)` |
| `load_all` | function | `modules/chain_registry.py:435` | `def load_all(chains_dir)` |
| `render_text_token_braces` | function | `modules/chain_registry.py:430` | `def render_text_token_braces(text)` |
| `resolve` | method | `modules/chain_registry.py:107` | `def resolve(self, tokens)` |
| `scan_all` | function | `modules/chain_registry.py:555` | `def scan_all(chains_dir)` |
| `set_enabled` | function | `modules/chain_registry.py:615` | `def set_enabled(name, enabled, chains_dir)` |
| `validate_chain` | function | `modules/chain_registry.py:285` | `def validate_chain(data, filename, chains_dir)` |
| `ChainRunResult` | class | `modules/chain_runner.py:86` | `class ChainRunResult` |
| `ChainRunner` | class | `modules/chain_runner.py:185` | `class ChainRunner` |
| `ReplanContext` | class | `modules/chain_runner.py:130` | `class ReplanContext` |
| `StepOutcome` | class | `modules/chain_runner.py:46` | `class StepOutcome` |
| `__init__` | method | `modules/chain_runner.py:188` | `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff, total_timeout...` |
| `_apply_replanner` | method | `modules/chain_runner.py:614` | `def _apply_replanner(self, result, index, outcome, steps, step_index, variables, captured_keys)` |
| `_ask_approval` | method | `modules/chain_runner.py:794` | `def _ask_approval(self, step_id, command)` |
| `_call` | method | `modules/chain_runner.py:973` | `def _call(callback, timeout)` |
| `_execute` | method | `modules/chain_runner.py:894` | `def _execute(self, command, timeout, expect_exits)` |
| `_first_json` | method | `modules/chain_runner.py:865` | `def _first_json(output)` |
| `_is_verb` | method | `modules/chain_runner.py:927` | `def _is_verb(self, command)` |
| `_notify` | method | `modules/chain_runner.py:605` | `def _notify(self, outcome)` |
| `_pre_check_timeout` | method | `modules/chain_runner.py:809` | `def _pre_check_timeout(self, step)` |
| `_render_command` | method | `modules/chain_runner.py:879` | `def _render_command(self, template, variables, captured_keys)` |
| `_run_fallback_chain` | method | `modules/chain_runner.py:535` | `def _run_fallback_chain(self, result, variables, captured_keys, started)` |
| `_run_parallel_group` | method | `modules/chain_runner.py:443` | `def _run_parallel_group(self, group, executions, resumed_ok, variables, captured_keys)` |
| `_run_raw` | method | `modules/chain_runner.py:956` | `def _run_raw(self, command, timeout, allowed)` |
| `_run_shell_verb` | method | `modules/chain_runner.py:938` | `def _run_shell_verb(self, command)` |
| `_run_step` | method | `modules/chain_runner.py:698` | `def _run_step(self, step, variables, captured_keys)` |
| `_save_checkpoint` | method | `modules/chain_runner.py:663` | `def _save_checkpoint(self, result, variables, captured_keys, next_index, state_name)` |
| `_skip_remaining` | method | `modules/chain_runner.py:428` | `def _skip_remaining(self, steps, start, reason)` |
| `_store_capture` | method | `modules/chain_runner.py:813` | `def _store_capture(self, step, output, outcome, variables, captured_keys)` |
| `_verify_timeout` | method | `modules/chain_runner.py:803` | `def _verify_timeout(self, step)` |
| `applied_vars` | method | `modules/chain_runner.py:162` | `def applied_vars(self)` |
| `insert_step` | method | `modules/chain_runner.py:152` | `def insert_step(self, step)` |
| `inserted` | method | `modules/chain_runner.py:167` | `def inserted(self)` |
| `ok` | method | `modules/chain_runner.py:63` | `def ok(self)` |
| `render_text` | function | `modules/chain_runner.py:177` | `def render_text(template, variables)` |
| `run` | method | `modules/chain_runner.py:258` | `def run(self)` |
| `set_var` | method | `modules/chain_runner.py:147` | `def set_var(self, name, value)` |
| `skip_rest` | method | `modules/chain_runner.py:157` | `def skip_rest(self)` |
| `skip_rest_flag` | method | `modules/chain_runner.py:172` | `def skip_rest_flag(self)` |
| `to_dict` | method | `modules/chain_runner.py:67` | `def to_dict(self)` |
| `to_dict` | method | `modules/chain_runner.py:106` | `def to_dict(self)` |
| `checkpoint_dir` | function | `modules/chain_state.py:26` | `def checkpoint_dir(base_dir)` |
| `list_checkpoints` | function | `modules/chain_state.py:80` | `def list_checkpoints(directory, limit, chain)` |
| `load_checkpoint` | function | `modules/chain_state.py:65` | `def load_checkpoint(directory, run_id)` |
| `new_run_id` | function | `modules/chain_state.py:33` | `def new_run_id(chain_name)` |
| `write_checkpoint` | function | `modules/chain_state.py:39` | `def write_checkpoint(directory, state)` |
| `_service_steps` | function | `modules/chain_synth.py:42` | `def _service_steps(host, services)` |
| `_slug` | function | `modules/chain_synth.py:29` | `def _slug(name)` |
| `_wordlist` | function | `modules/chain_synth.py:33` | `def _wordlist(param, fallback)` |
| `facts_for_target` | function | `modules/chain_synth.py:224` | `def facts_for_target(target)` |
| `synth_chain_data` | function | `modules/chain_synth.py:89` | `def synth_chain_data(playbook, target, services, has_creds, os_hint, include_c2)` |
| `write_generated_chain` | function | `modules/chain_synth.py:253` | `def write_generated_chain(data, chains_dir)` |
| `_candidate_files` | function | `modules/chain_tokens.py:120` | `def _candidate_files()` |
| `_load_host_facts` | function | `modules/chain_tokens.py:77` | `def _load_host_facts(host)` |
| `_mentions` | function | `modules/chain_tokens.py:130` | `def _mentions(path, needle)` |
| `_newest_creds_file` | function | `modules/chain_tokens.py:93` | `def _newest_creds_file(host)` |
| `build_tokens` | function | `modules/chain_tokens.py:29` | `def build_tokens(target, params)` |
| `token_keys` | function | `modules/chain_tokens.py:24` | `def token_keys()` |
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
| `_count_by_category` | method | `modules/compliance.py:772` | `def _count_by_category(self, findings)` |
| `_count_by_severity` | method | `modules/compliance.py:765` | `def _count_by_severity(self, findings)` |
| `_format_compliance_report_md` | method | `modules/compliance.py:835` | `def _format_compliance_report_md(self, report)` |
| `_hash_entry` | method | `modules/compliance.py:379` | `def _hash_entry(self, entry)` |
| `_load` | method | `modules/compliance.py:364` | `def _load(self)` |
| `_load_findings` | method | `modules/compliance.py:779` | `def _load_findings(self)` |
| `add_evidence` | method | `modules/compliance.py:901` | `def add_evidence(self, filepath, operator, description)` |
| `add_file` | method | `modules/compliance.py:383` | `def add_file(self, filepath, operator, description)` |
| `export_pdf` | function | `modules/compliance.py:449` | `def export_pdf(report_md, output_path, title, classification)` |
| `export_pdf` | method | `modules/compliance.py:831` | `def export_pdf(self, report, output_path)` |
| `export_to_cef` | function | `modules/compliance.py:572` | `def export_to_cef(findings, output_path, vendor, product, version)` |
| `export_to_elastic_ndjson` | function | `modules/compliance.py:533` | `def export_to_elastic_ndjson(findings, output_path, index_prefix)` |
| `generate_compliance_report` | method | `modules/compliance.py:710` | `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` |
| `get_chain_digest` | method | `modules/compliance.py:429` | `def get_chain_digest(self)` |
| `map_findings_to_compliance` | method | `modules/compliance.py:639` | `def map_findings_to_compliance(self, findings, frameworks)` |
| `to_report` | method | `modules/compliance.py:432` | `def to_report(self)` |
| `verify` | method | `modules/compliance.py:410` | `def verify(self)` |
| `verify_evidence_chain` | method | `modules/compliance.py:904` | `def verify_evidence_chain(self)` |
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
| `_load` | function | `modules/custom_tools.py:37` | `def _load()` |
| `_run_http` | function | `modules/custom_tools.py:179` | `def _run_http(tool, arg, on_output)` |
| `_save` | function | `modules/custom_tools.py:45` | `def _save(payload)` |
| `_store_file` | function | `modules/custom_tools.py:30` | `def _store_file()` |
| `_trigger_tokens` | function | `modules/custom_tools.py:122` | `def _trigger_tokens(raw)` |
| `add_tool` | function | `modules/custom_tools.py:52` | `def add_tool(name, kind, target, description, method, body, timeout, trigger)` |
| `get_tool` | function | `modules/custom_tools.py:114` | `def get_tool(name)` |
| `list_tools` | function | `modules/custom_tools.py:109` | `def list_tools()` |
| `match_tools` | function | `modules/custom_tools.py:128` | `def match_tools(text, limit)` |
| `remove_tool` | function | `modules/custom_tools.py:97` | `def remove_tool(name)` |
| `run_tool` | function | `modules/custom_tools.py:151` | `def run_tool(name, arg, on_output)` |
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
| `host_add` | method | `modules/db.py:357` | `def host_add(self, workspace_id, address, mac, hostname, os, state)` |
| `host_delete` | method | `modules/db.py:390` | `def host_delete(self, host_id)` |
| `host_find` | method | `modules/db.py:410` | `def host_find(self, workspace_id, query)` |
| `host_list` | method | `modules/db.py:401` | `def host_list(self, workspace_id)` |
| `import_nmap_xml` | method | `modules/db.py:664` | `def import_nmap_xml(self, workspace_id, xml_path)` |
| `loot_add` | method | `modules/db.py:596` | `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` |
| `loot_list` | method | `modules/db.py:615` | `def loot_list(self, workspace_id)` |
| `migration_status` | method | `modules/db.py:222` | `def migration_status(self)` |
| `note_add` | method | `modules/db.py:631` | `def note_add(self, workspace_id, data, note_type, host_id)` |
| `note_list` | method | `modules/db.py:648` | `def note_list(self, workspace_id)` |

Next: [SYMBOLS_p13.md](SYMBOLS_p13.md)
