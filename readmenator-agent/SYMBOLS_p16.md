# Symbols (page 16 of 50)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_rc4_decrypt` | method | `modules/kerberos_core.py:676` | `def _rc4_decrypt(key, data, usage)` |
| `_rc4_encrypt` | method | `modules/kerberos_core.py:667` | `def _rc4_encrypt(key, data, usage)` |
| `aes_decrypt` | method | `modules/kerberos_core.py:361` | `def aes_decrypt(self, key, ciphertext, usage)` |
| `aes_encrypt` | method | `modules/kerberos_core.py:329` | `def aes_encrypt(self, key, plaintext, usage)` |
| `build_as_req` | method | `modules/kerberos_core.py:435` | `def build_as_req(self, username, domain, password, etype)` |
| `build_tgs_req` | method | `modules/kerberos_core.py:489` | `def build_tgs_req(self, params)` |
| `compute_checksum` | method | `modules/kerberos_core.py:389` | `def compute_checksum(key, data, etype)` |
| `decrypt_ticket` | method | `modules/kerberos_core.py:563` | `def decrypt_ticket(self, ticket_data, key, etype)` |
| `derive_aes_key` | method | `modules/kerberos_core.py:282` | `def derive_aes_key(password, salt, etype)` |
| `derive_rc4_key` | method | `modules/kerberos_core.py:318` | `def derive_rc4_key(password)` |
| `get_supported_etypes` | method | `modules/kerberos_core.py:427` | `def get_supported_etypes(self)` |
| `has_flag` | method | `modules/kerberos_core.py:207` | `def has_flag(self, flag_name)` |
| `is_expired` | method | `modules/kerberos_core.py:706` | `def is_expired(endtime, grace_period)` |
| `parse_as_rep` | method | `modules/kerberos_core.py:534` | `def parse_as_rep(self, as_rep_data, key, etype)` |
| `parse_error` | method | `modules/kerberos_core.py:687` | `def parse_error(error_data)` |
| `parse_pac` | method | `modules/kerberos_core.py:588` | `def parse_pac(self, pac_data)` |
| `parse_tgs_rep` | method | `modules/kerberos_core.py:550` | `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)` |
| `to_string` | method | `modules/kerberos_core.py:152` | `def to_string(self)` |
| `validate_flags` | method | `modules/kerberos_core.py:719` | `def validate_flags(ticket, required_flags)` |
| `validate_pac_checksums` | method | `modules/kerberos_core.py:735` | `def validate_pac_checksums(pac)` |
| `DiamondTicketConfig` | class | `modules/kerberos_tickets.py:94` | `class DiamondTicketConfig` |
| `DiamondTicketForger` | class | `modules/kerberos_tickets.py:397` | `class DiamondTicketForger` |
| `GoldenTicketConfig` | class | `modules/kerberos_tickets.py:65` | `class GoldenTicketConfig` |
| `GoldenTicketForger` | class | `modules/kerberos_tickets.py:265` | `class GoldenTicketForger` |
| `SapphireTicketForger` | class | `modules/kerberos_tickets.py:462` | `class SapphireTicketForger` |
| `SilverTicketConfig` | class | `modules/kerberos_tickets.py:36` | `class SilverTicketConfig` |
| `SilverTicketForger` | class | `modules/kerberos_tickets.py:124` | `class SilverTicketForger` |
| `SkeletonKeyInjector` | class | `modules/kerberos_tickets.py:567` | `class SkeletonKeyInjector` |
| `__init__` | method | `modules/kerberos_tickets.py:131` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:272` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:405` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:469` | `def __init__(self, kerberos_core)` |
| `_assemble_tgt` | method | `modules/kerberos_tickets.py:368` | `def _assemble_tgt(self, config, flags, enc_part)` |
| `_build_diamond_pac` | method | `modules/kerberos_tickets.py:446` | `def _build_diamond_pac(self, config)` |
| `_build_enc_ticket_part` | method | `modules/kerberos_tickets.py:206` | `def _build_enc_ticket_part(self, config, start, end, flags, key, etype)` |
| `_build_golden_enc_part` | method | `modules/kerberos_tickets.py:346` | `def _build_golden_enc_part(self, config, start, end, flags, key)` |
| `_build_golden_pac` | method | `modules/kerberos_tickets.py:339` | `def _build_golden_pac(self, config)` |
| `_build_kirbi` | method | `modules/kerberos_tickets.py:235` | `def _build_kirbi(self, ticket, enc_part, etype)` |
| `_build_silver_pac` | method | `modules/kerberos_tickets.py:200` | `def _build_silver_pac(self, config, start, end)` |
| `_build_ticket_structure` | method | `modules/kerberos_tickets.py:225` | `def _build_ticket_structure(self, config, flags, enc_part)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:254` | `def _impacket_command(self, config)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:388` | `def _impacket_command(self, config)` |
| `_mimikatz_command` | method | `modules/kerberos_tickets.py:379` | `def _mimikatz_command(self, config)` |
| `_mimikatz_inject_command` | method | `modules/kerberos_tickets.py:244` | `def _mimikatz_inject_command(self, config)` |
| `_resolve_key` | method | `modules/kerberos_tickets.py:190` | `def _resolve_key(self, config)` |
| `_resolve_krbtgt_key` | method | `modules/kerberos_tickets.py:324` | `def _resolve_krbtgt_key(self, config)` |
| `cleanup_command` | method | `modules/kerberos_tickets.py:612` | `def cleanup_command()` |
| `detect_skeleton_key` | method | `modules/kerberos_tickets.py:578` | `def detect_skeleton_key(target_host, domain, dc_ip)` |
| `forge` | method | `modules/kerberos_tickets.py:134` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:275` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:408` | `def forge(self, config)` |
| `forge_rbcd` | method | `modules/kerberos_tickets.py:530` | `def forge_rbcd(self, machine_account_hash, target_service, domain, username)` |
| `forge_s4u2self` | method | `modules/kerberos_tickets.py:472` | `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)` |
| `inject_command` | method | `modules/kerberos_tickets.py:600` | `def inject_command(target_host)` |
| `_build_svg` | function | `modules/kill_chain_viz.py:34` | `def _build_svg(phases)` |
| `_load_phases` | function | `modules/kill_chain_viz.py:20` | `def _load_phases(sessions)` |
| `_read_target` | function | `modules/kill_chain_viz.py:27` | `def _read_target()` |
| `generate_html` | function | `modules/kill_chain_viz.py:69` | `def generate_html(target, sessions)` |
| `generate_svg` | function | `modules/kill_chain_viz.py:102` | `def generate_svg(target, sessions)` |
| `KillChain` | class | `modules/killchain.py:206` | `class KillChain` |
| `KillChainConfig` | class | `modules/killchain.py:99` | `class KillChainConfig` |
| `PhaseStatus` | class | `modules/killchain.py:197` | `class PhaseStatus` |
| `advance_phase` | method | `modules/killchain.py:312` | `def advance_phase(new_phase, world_model_path, host, extras)` |
| `cli_phase_to_host_state` | method | `modules/killchain.py:252` | `def cli_phase_to_host_state(phase)` |
| `compact_progress` | method | `modules/killchain.py:465` | `def compact_progress(current_phase, phases_entered)` |
| `config` | method | `modules/killchain.py:215` | `def config()` |
| `current_phase` | method | `modules/killchain.py:265` | `def current_phase(world_model_path)` |
| `engagement_phase_to_cli` | method | `modules/killchain.py:240` | `def engagement_phase_to_cli(engagement_value)` |
| `get_killchain` | function | `modules/killchain.py:566` | `def get_killchain()` |
| `get_progress` | method | `modules/killchain.py:416` | `def get_progress(world_model_path)` |
| `is_valid_phase` | method | `modules/killchain.py:188` | `def is_valid_phase(self, phase)` |
| `phase_colors` | method | `modules/killchain.py:230` | `def phase_colors()` |
| `phase_index` | method | `modules/killchain.py:181` | `def phase_index(self, phase)` |
| `phase_index` | method | `modules/killchain.py:496` | `def phase_index(phase)` |
| `phase_labels` | method | `modules/killchain.py:225` | `def phase_labels()` |
| `phase_rich_colors` | method | `modules/killchain.py:235` | `def phase_rich_colors()` |
| `phases` | method | `modules/killchain.py:220` | `def phases()` |
| `phases_for_display` | method | `modules/killchain.py:485` | `def phases_for_display()` |
| `snapshot` | method | `modules/killchain.py:501` | `def snapshot(world_model_path)` |
| `technique_for_phase` | method | `modules/killchain.py:541` | `def technique_for_phase(phase)` |
| `technique_for_phase` | function | `modules/killchain.py:571` | `def technique_for_phase(phase)` |
| `technique_for_vulnclass` | method | `modules/killchain.py:553` | `def technique_for_vulnclass(vulnclass)` |
| `technique_for_vulnclass` | function | `modules/killchain.py:576` | `def technique_for_vulnclass(vulnclass)` |
| `world_model_path` | method | `modules/killchain.py:177` | `def world_model_path(self)` |
| `ReverseShellApp` | class | `modules/kivi.py:11` | `class ReverseShellApp(App)` |
| `build` | method | `modules/kivi.py:12` | `def build(self)` |
| `connect_to_server` | method | `modules/kivi.py:27` | `def connect_to_server(self, instance)` |
| `_docker` | function | `modules/lab_runtime.py:107` | `def _docker()` |
| `_docker_compose` | function | `modules/lab_runtime.py:412` | `def _docker_compose(args)` |
| `_ensure_ad_lab` | function | `modules/lab_runtime.py:197` | `def _ensure_ad_lab(scenario, name)` |
| `apply_gym_migrations` | function | `modules/lab_runtime.py:242` | `def apply_gym_migrations(name)` |
| `container_ip` | function | `modules/lab_runtime.py:169` | `def container_ip(container_name)` |
| `container_name` | function | `modules/lab_runtime.py:164` | `def container_name(scenario)` |
| `docker_available` | function | `modules/lab_runtime.py:93` | `def docker_available()` |
| `ensure_range_secret` | function | `modules/lab_runtime.py:420` | `def ensure_range_secret(profile_dir)` |
| `ensure_web` | function | `modules/lab_runtime.py:183` | `def ensure_web(scenario, name)` |
| `existing_containers` | function | `modules/lab_runtime.py:131` | `def existing_containers()` |
| `range_compose` | function | `modules/lab_runtime.py:340` | `def range_compose(profile)` |
| `running_containers` | function | `modules/lab_runtime.py:115` | `def running_containers()` |
| `running_range_containers` | function | `modules/lab_runtime.py:148` | `def running_range_containers()` |
| `start` | function | `modules/lab_runtime.py:250` | `def start(scenario)` |
| `start_range` | function | `modules/lab_runtime.py:349` | `def start_range(profile)` |
| `stop` | function | `modules/lab_runtime.py:304` | `def stop(scenario)` |
| `stop_all` | function | `modules/lab_runtime.py:322` | `def stop_all()` |
| `stop_range` | function | `modules/lab_runtime.py:368` | `def stop_range(profile)` |
| `stop_ranges` | function | `modules/lab_runtime.py:379` | `def stop_ranges()` |
| `ConversationStore` | class | `modules/lazy_agent.py:261` | `class ConversationStore` |
| `ObservableAgentRunner` | class | `modules/lazy_agent.py:145` | `class ObservableAgentRunner(AgentRunner)` |
| `__init__` | method | `modules/lazy_agent.py:148` | `def __init__(self, model, system_prompt, max_iterations, on_event)` |
| `__init__` | method | `modules/lazy_agent.py:264` | `def __init__(self, task_id)` |
| `_call_model` | method | `modules/lazy_agent.py:174` | `def _call_model(self)` |
| `_deep_clean` | function | `modules/lazy_agent.py:237` | `def _deep_clean(value, _depth)` |
| `_enable_streaming` | function | `modules/lazy_agent.py:123` | `def _enable_streaming(runner, on_event)` |
| `_invoke` | function | `modules/lazy_agent.py:190` | `def _invoke()` |
| `_json_default` | function | `modules/lazy_agent.py:221` | `def _json_default(value)` |
| `_json_safe` | function | `modules/lazy_agent.py:253` | `def _json_safe(messages)` |
| `_kill` | function | `modules/lazy_agent.py:583` | `def _kill()` |
| `_load` | method | `modules/lazy_agent.py:269` | `def _load(self)` |
| `_process_tool_call` | method | `modules/lazy_agent.py:159` | `def _process_tool_call(self, tool_call)` |
| `_process_watchdog` | function | `modules/lazy_agent.py:578` | `def _process_watchdog(timeout_sec, process)` |
| `_session_from_line` | function | `modules/lazy_agent.py:556` | `def _session_from_line(line)` |
| `_tick` | function | `modules/lazy_agent.py:196` | `def _tick()` |
| `intent_messages` | method | `modules/lazy_agent.py:273` | `def intent_messages(self, intent_id)` |
| `max_iterations` | function | `modules/lazy_agent.py:72` | `def max_iterations()` |
| `model_timeout_sec` | function | `modules/lazy_agent.py:41` | `def model_timeout_sec()` |
| `register_tools` | function | `modules/lazy_agent.py:322` | `def register_tools(runner, specs)` |
| `reset_intents` | method | `modules/lazy_agent.py:315` | `def reset_intents(self)` |
| `resolve_agentic_model` | function | `modules/lazy_agent.py:83` | `def resolve_agentic_model(exclude)` |
| `run` | method | `modules/lazy_agent.py:168` | `def run(self, user_input)` |
| `run_external_hermes` | function | `modules/lazy_agent.py:472` | `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` |
| `run_external_opencode` | function | `modules/lazy_agent.py:396` | `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` |
| `run_main_session` | function | `modules/lazy_agent.py:374` | `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` |
| `run_worker_session` | function | `modules/lazy_agent.py:335` | `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` |
| `save_intent` | method | `modules/lazy_agent.py:278` | `def save_intent(self, intent_id, messages)` |
| `save_session` | method | `modules/lazy_agent.py:305` | `def save_session(self, session_id, messages, title)` |
| `session` | method | `modules/lazy_agent.py:287` | `def session(self, session_id)` |
| `sessions` | method | `modules/lazy_agent.py:291` | `def sessions(self)` |
| `tool_calling_enabled` | function | `modules/lazy_agent.py:57` | `def tool_calling_enabled()` |
| `_chain_data` | function | `modules/lazy_autofire.py:225` | `def _chain_data(target, fires)` |
| `_cooldown_filter` | function | `modules/lazy_autofire.py:180` | `def _cooldown_filter(fires, state, target, moment, chains_dir)` |
| `_existing_chain_tokens` | function | `modules/lazy_autofire.py:215` | `def _existing_chain_tokens(chains_dir, slug)` |
| `_fire_matches` | function | `modules/lazy_autofire.py:166` | `def _fire_matches(report)` |
| `_load_state` | function | `modules/lazy_autofire.py:281` | `def _load_state(path)` |
| `_save_state` | function | `modules/lazy_autofire.py:291` | `def _save_state(path, state)` |
| `_slug` | function | `modules/lazy_autofire.py:312` | `def _slug(text)` |
| `_stamp_cooldown` | function | `modules/lazy_autofire.py:305` | `def _stamp_cooldown(state, target, cves, moment)` |
| `autofire_armed` | function | `modules/lazy_autofire.py:41` | `def autofire_armed(payload)` |
| `consider_report` | function | `modules/lazy_autofire.py:53` | `def consider_report(report, chains_dir, state_path, armed, now)` |
| `fire_from_file` | function | `modules/lazy_autofire.py:105` | `def fire_from_file(target, feed_path)` |
| `status` | function | `modules/lazy_autofire.py:147` | `def status(payload, state_path)` |
| `sweep_state` | function | `modules/lazy_autofire.py:127` | `def sweep_state(state_path, now)` |
| `_data_dir` | function | `modules/lazy_bridge.py:35` | `def _data_dir()` |
| `_extract_hosts_from_graph` | function | `modules/lazy_bridge.py:184` | `def _extract_hosts_from_graph(graph)` |
| `_notify` | function | `modules/lazy_bridge.py:398` | `def _notify(progress, text)` |
| `_read_json` | function | `modules/lazy_bridge.py:51` | `def _read_json(path, default)` |
| `_read_jsonl` | function | `modules/lazy_bridge.py:68` | `def _read_jsonl(path)` |
| `_read_new_traffic` | function | `modules/lazy_bridge.py:361` | `def _read_new_traffic(path, offset)` |
| `_record_sync` | function | `modules/lazy_bridge.py:592` | `def _record_sync(action, summary)` |
| `bridge_status` | function | `modules/lazy_bridge.py:163` | `def bridge_status()` |
| `lazy_activity` | function | `modules/lazy_bridge.py:127` | `def lazy_activity(task_id)` |
| `lazy_assets` | function | `modules/lazy_bridge.py:103` | `def lazy_assets()` |
| `lazy_graph` | function | `modules/lazy_bridge.py:114` | `def lazy_graph(task_id)` |
| `lazy_guard_audit` | function | `modules/lazy_bridge.py:151` | `def lazy_guard_audit(task_id)` |
| `lazy_tasks` | function | `modules/lazy_bridge.py:92` | `def lazy_tasks()` |
| `lazy_traffic` | function | `modules/lazy_bridge.py:139` | `def lazy_traffic(task_id)` |
| `pull_findings_to_lifecycle` | function | `modules/lazy_bridge.py:333` | `def pull_findings_to_lifecycle()` |
| `pull_to_objectives` | function | `modules/lazy_bridge.py:298` | `def pull_to_objectives()` |
| `pull_to_world_model` | function | `modules/lazy_bridge.py:221` | `def pull_to_world_model()` |
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:408` | `def pull_traffic_to_recorder(progress)` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:476` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:501` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:566` | `def sync_all(progress)` |
| `_range_says` | function | `modules/lazy_checks.py:105` | `def _range_says(version, ranges)` |
| `extract_cve` | function | `modules/lazy_checks.py:51` | `def extract_cve(text)` |
| `extract_version` | function | `modules/lazy_checks.py:30` | `def extract_version(text)` |
| `interpret_checks` | function | `modules/lazy_checks.py:57` | `def interpret_checks(checks, cve, stored_version, ranges)` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `_verb_in_phase` | function | `modules/lazy_cli_bridge.py:219` | `def _verb_in_phase(row, phase)` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `catalog_cli_for_phase` | function | `modules/lazy_cli_bridge.py:240` | `def catalog_cli_for_phase(limit)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:274` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:297` | `def set_full_cli(enabled)` |
| `ContinuationRecord` | class | `modules/lazy_continuation.py:34` | `class ContinuationRecord` |
| `_dir` | function | `modules/lazy_continuation.py:58` | `def _dir()` |
| `_slug` | function | `modules/lazy_continuation.py:65` | `def _slug(target)` |
| `load` | function | `modules/lazy_continuation.py:132` | `def load(target)` |
| `recall_candidates` | function | `modules/lazy_continuation.py:159` | `def recall_candidates(target, limit)` |
| `record_path` | function | `modules/lazy_continuation.py:71` | `def record_path(target)` |
| `save` | function | `modules/lazy_continuation.py:83` | `def save(target, task_id, goal, status, settlement, findings, next_steps)` |
| `CredRow` | class | `modules/lazy_creds.py:30` | `class CredRow` |
| `as_lines` | function | `modules/lazy_creds.py:101` | `def as_lines(rows)` |
| `candidates` | function | `modules/lazy_creds.py:79` | `def candidates(limit)` |
| `count` | function | `modules/lazy_creds.py:96` | `def count()` |
| `export_pairs` | function | `modules/lazy_creds.py:106` | `def export_pairs(path, limit)` |
| `load` | function | `modules/lazy_creds.py:39` | `def load()` |
| `search` | function | `modules/lazy_creds.py:63` | `def search(query)` |
| `_advisory_cve_id` | function | `modules/lazy_cve_feed.py:398` | `def _advisory_cve_id(advisory)` |
| `_advisory_cvss` | function | `modules/lazy_cve_feed.py:407` | `def _advisory_cvss(advisory)` |
| `_advisory_matches_product` | function | `modules/lazy_cve_feed.py:421` | `def _advisory_matches_product(advisory, banner_words)` |
| `_cache_fresh` | function | `modules/lazy_cve_feed.py:104` | `def _cache_fresh(path, ttl_sec)` |
| `_cache_path` | function | `modules/lazy_cve_feed.py:95` | `def _cache_path(name)` |
| `_cached_advisories` | function | `modules/lazy_cve_feed.py:544` | `def _cached_advisories()` |
| `_env_flag` | function | `modules/lazy_cve_feed.py:90` | `def _env_flag(name, default)` |
| `_exploit_cves_from_text` | function | `modules/lazy_cve_feed.py:228` | `def _exploit_cves_from_text(text)` |
| `_fetch` | function | `modules/lazy_cve_feed.py:112` | `def _fetch(url)` |
| `_load_json` | function | `modules/lazy_cve_feed.py:150` | `def _load_json(name)` |
| `_osv_cache_path` | function | `modules/lazy_cve_feed.py:281` | `def _osv_cache_path(product)` |
| `_store_bytes` | function | `modules/lazy_cve_feed.py:134` | `def _store_bytes(name, payload)` |
| `_store_json` | function | `modules/lazy_cve_feed.py:142` | `def _store_json(name, data)` |
| `_worker` | function | `modules/lazy_cve_feed.py:696` | `def _worker()` |
| `convert_osv_ranges` | function | `modules/lazy_cve_feed.py:515` | `def convert_osv_ranges(affected)` |
| `correlate` | function | `modules/lazy_cve_feed.py:438` | `def correlate(product, version, allow_network)` |
| `cve_intel` | function | `modules/lazy_cve_feed.py:360` | `def cve_intel(cve_id, feeds, allow_network)` |
| `fetch_product_advisories` | function | `modules/lazy_cve_feed.py:291` | `def fetch_product_advisories(product, force)` |
| `hot_matches` | function | `modules/lazy_cve_feed.py:636` | `def hot_matches(services, allow_network)` |
| `load_epss` | function | `modules/lazy_cve_feed.py:192` | `def load_epss(force)` |
| `load_exploit_cves` | function | `modules/lazy_cve_feed.py:233` | `def load_exploit_cves(force)` |
| `load_kev` | function | `modules/lazy_cve_feed.py:158` | `def load_kev(force)` |
| `load_kev_matches` | function | `modules/lazy_cve_feed.py:594` | `def load_kev_matches(product, feeds)` |
| `load_msf_cves` | function | `modules/lazy_cve_feed.py:257` | `def load_msf_cves(force)` |
| `range_for_cve` | function | `modules/lazy_cve_feed.py:565` | `def range_for_cve(cve_id, allow_network)` |
| `refresh_feeds_async` | function | `modules/lazy_cve_feed.py:680` | `def refresh_feeds_async(products)` |
| `_drafts_dir` | function | `modules/lazy_drafts.py:27` | `def _drafts_dir()` |
| `drain` | function | `modules/lazy_drafts.py:34` | `def drain(engine)` |
| `LazyEngine` | class | `modules/lazy_engine.py:56` | `class LazyEngine(LazyLoopEngine)` |
| `_int` | function | `modules/lazy_exposure.py:410` | `def _int(value, fallback)` |
| `_live_fingerprint` | function | `modules/lazy_exposure.py:210` | `def _live_fingerprint()` |
| `_match_hot_key` | function | `modules/lazy_exposure.py:400` | `def _match_hot_key(row)` |
| `_shape_sightings` | function | `modules/lazy_exposure.py:370` | `def _shape_sightings(rows)` |
| `_short_refs` | function | `modules/lazy_exposure.py:365` | `def _short_refs(row)` |
| `_slug` | function | `modules/lazy_exposure.py:405` | `def _slug(text)` |
| `ensure_report` | function | `modules/lazy_exposure.py:56` | `def ensure_report(target, entries, refresh)` |
| `generate_report` | function | `modules/lazy_exposure.py:129` | `def generate_report(target, entries, sightings)` |
| `probe_checks` | function | `modules/lazy_exposure.py:257` | `def probe_checks(matches, feed)` |
| `publish_report` | function | `modules/lazy_exposure.py:314` | `def publish_report(report)` |
| `read_sightings` | function | `modules/lazy_exposure.py:97` | `def read_sightings(target, state_path)` |
| `refresh_if_stale` | function | `modules/lazy_exposure.py:418` | `def refresh_if_stale(target, entries)` |
| `save_report` | function | `modules/lazy_exposure.py:291` | `def save_report(report, path)` |
| `score_report` | function | `modules/lazy_exposure.py:219` | `def score_report(entries, bounded_unknown, services)` |
| `ExploitSighting` | class | `modules/lazy_feedmatch.py:123` | `class ExploitSighting` |
| `FeedEntry` | class | `modules/lazy_feedmatch.py:73` | `class FeedEntry` |
| `Sighting` | class | `modules/lazy_feedmatch.py:98` | `class Sighting` |
| `_cvss` | function | `modules/lazy_feedmatch.py:470` | `def _cvss(value)` |
| `_fixed_key` | function | `modules/lazy_feedmatch.py:316` | `def _fixed_key(rng)` |
| `_float` | function | `modules/lazy_feedmatch.py:478` | `def _float(value)` |
| `_map_kev_row` | function | `modules/lazy_feedmatch.py:187` | `def _map_kev_row(item)` |
| `_references` | function | `modules/lazy_feedmatch.py:464` | `def _references(raw)` |
| `bind_sighting` | function | `modules/lazy_feedmatch.py:337` | `def bind_sighting(sighting, entries)` |
| `entry_matches_product` | function | `modules/lazy_feedmatch.py:262` | `def entry_matches_product(entry, product)` |
| `feed_fingerprint` | function | `modules/lazy_feedmatch.py:486` | `def feed_fingerprint(entries)` |
| `feed_tier` | function | `modules/lazy_feedmatch.py:325` | `def feed_tier(entry)` |
| `is_os_sighting` | function | `modules/lazy_feedmatch.py:248` | `def is_os_sighting(name)` |
| `live_bindings` | function | `modules/lazy_feedmatch.py:411` | `def live_bindings(sighting, allow_network)` |
| `load_feed` | function | `modules/lazy_feedmatch.py:151` | `def load_feed(path)` |
| `parse_feed` | function | `modules/lazy_feedmatch.py:210` | `def parse_feed(entries)` |
| `unversioned_leads` | function | `modules/lazy_feedmatch.py:388` | `def unversioned_leads(sightings)` |
| `version_in_ranges` | function | `modules/lazy_feedmatch.py:280` | `def version_in_ranges(version, ranges)` |
| `FinalizerDecision` | class | `modules/lazy_finalizer.py:35` | `class FinalizerDecision` |
| `decide` | function | `modules/lazy_finalizer.py:72` | `def decide(status, candidate_verdict, facts, findings, confirmed, tested, pending_approvals, pending_plan_steps)` |
| `to_dict` | method | `modules/lazy_finalizer.py:58` | `def to_dict(self)` |
| `FindingValidationError` | class | `modules/lazy_findings.py:60` | `class FindingValidationError(ValueError)` |
| `FindingsLedger` | class | `modules/lazy_findings.py:539` | `class FindingsLedger` |
| `LedgerLimits` | class | `modules/lazy_findings.py:65` | `class LedgerLimits` |
| `__init__` | method | `modules/lazy_findings.py:542` | `def __init__(self, engagement_id, base_dir, limits, scrub)` |
| `_base_row` | function | `modules/lazy_findings.py:344` | `def _base_row(payload, bounds)` |
| `_now_iso` | function | `modules/lazy_findings.py:534` | `def _now_iso()` |
| `_row_from_verdict` | function | `modules/lazy_findings.py:294` | `def _row_from_verdict(payload, verdict, bounds)` |
| `append` | method | `modules/lazy_findings.py:606` | `def append(self, row)` |
| `build_handoff` | function | `modules/lazy_findings.py:481` | `def build_handoff(rows, status, rounds)` |
| `clamped` | method | `modules/lazy_findings.py:81` | `def clamped(self)` |
| `discard_row` | function | `modules/lazy_findings.py:382` | `def discard_row(reason, command, output, technique_id, engagement_id, target)` |
| `engagement_id_valid` | function | `modules/lazy_findings.py:91` | `def engagement_id_valid(value)` |
| `evidence_reject_reason` | function | `modules/lazy_findings.py:156` | `def evidence_reject_reason(state, evidence, min_output)` |
| `evidence_supported` | function | `modules/lazy_findings.py:281` | `def evidence_supported(evidence, min_output)` |
| `file_path` | method | `modules/lazy_findings.py:569` | `def file_path(self)` |
| `history` | method | `modules/lazy_findings.py:684` | `def history(self, finding_ref)` |
| `latest_state` | method | `modules/lazy_findings.py:696` | `def latest_state(self, finding_ref)` |
| `level_for_state_uplift` | function | `modules/lazy_findings.py:138` | `def level_for_state_uplift(level, state)` |
| `metadata_level` | function | `modules/lazy_findings.py:217` | `def metadata_level(payload)` |
| `normalize` | method | `modules/lazy_findings.py:573` | `def normalize(self, row)` |
| `normalize_finding` | function | `modules/lazy_findings.py:429` | `def normalize_finding(row, limits)` |
| `read` | method | `modules/lazy_findings.py:636` | `def read(self, cursor, limit)` |
| `row_from_event` | function | `modules/lazy_findings.py:230` | `def row_from_event(payload, limits)` |
| `rows` | method | `modules/lazy_findings.py:660` | `def rows(self)` |
| `severity_tier` | function | `modules/lazy_findings.py:116` | `def severity_tier(severity)` |
| `state_counts` | function | `modules/lazy_findings.py:191` | `def state_counts(rows)` |
| `technique_id_valid` | function | `modules/lazy_findings.py:103` | `def technique_id_valid(value)` |
| `backport_status` | function | `modules/lazy_heat.py:345` | `def backport_status(banner, fixed_revision)` |
| `classify_heat` | function | `modules/lazy_heat.py:71` | `def classify_heat(kev, epss, exploit, cvss)` |
| `compare_versions` | function | `modules/lazy_heat.py:157` | `def compare_versions(a, b)` |
| `cvss3_base_score` | function | `modules/lazy_heat.py:207` | `def cvss3_base_score(vector)` |
| `heat_of_severity` | function | `modules/lazy_heat.py:373` | `def heat_of_severity(severity)` |
| `heat_rank` | function | `modules/lazy_heat.py:392` | `def heat_rank(tier)` |
| `host_heat` | function | `modules/lazy_heat.py:404` | `def host_heat(tier_values, severity_levels, unscanned)` |
| `hottest` | function | `modules/lazy_heat.py:424` | `def hottest(tier_values)` |
| `label_for` | function | `modules/lazy_heat.py:438` | `def label_for(status, fixed_revision)` |
| `match_heat` | function | `modules/lazy_heat.py:94` | `def match_heat(tier, cvss, verdict, distro_status)` |
| `parse_distro_revision` | function | `modules/lazy_heat.py:306` | `def parse_distro_revision(banner)` |
| `parse_version` | function | `modules/lazy_heat.py:121` | `def parse_version(value, strict)` |
| `product_token` | function | `modules/lazy_heat.py:249` | `def product_token(value)` |
| `token_matches` | function | `modules/lazy_heat.py:272` | `def token_matches(haystack, needle)` |
| `version_in_range` | function | `modules/lazy_heat.py:165` | `def version_in_range(ver, rng)` |
| `_add` | function | `modules/lazy_hostscore.py:49` | `def _add(label, points)` |
| `_persist` | function | `modules/lazy_hostscore.py:182` | `def _persist(table, sessions_dir, now)` |
| `load_scores` | function | `modules/lazy_hostscore.py:193` | `def load_scores(sessions_dir)` |
| `rescore` | function | `modules/lazy_hostscore.py:96` | `def rescore(sessions_dir, allow_network, now)` |
| `score_host` | function | `modules/lazy_hostscore.py:34` | `def score_host(inputs)` |
| `install_command_for` | function | `modules/lazy_installer.py:70` | `def install_command_for(tool)` |
| `installer_enabled` | function | `modules/lazy_installer.py:41` | `def installer_enabled()` |
| `intent_for` | function | `modules/lazy_installer.py:75` | `def intent_for(tool)` |
| `set_installer_enabled` | function | `modules/lazy_installer.py:58` | `def set_installer_enabled(enabled)` |
| `steps_for_install` | function | `modules/lazy_installer.py:88` | `def steps_for_install(text)` |
| `tool_from_intent` | function | `modules/lazy_installer.py:80` | `def tool_from_intent(text)` |
| `_append` | function | `modules/lazy_intel.py:79` | `def _append(record)` |
| `_is_ip_literal` | function | `modules/lazy_intel.py:292` | `def _is_ip_literal(value)` |
| `_log_path` | function | `modules/lazy_intel.py:35` | `def _log_path()` |
| `_mask` | function | `modules/lazy_intel.py:41` | `def _mask(text)` |
| `_now` | function | `modules/lazy_intel.py:30` | `def _now()` |
| `describe_command` | function | `modules/lazy_intel.py:114` | `def describe_command(command)` |
| `export_spans` | function | `modules/lazy_intel.py:342` | `def export_spans(task_id, out)` |
| `fuse_routing_decisions` | function | `modules/lazy_intel.py:303` | `def fuse_routing_decisions(task_id)` |
| `infer_source` | function | `modules/lazy_intel.py:88` | `def infer_source(command, intent_text)` |
| `mask_configured` | function | `modules/lazy_intel.py:237` | `def mask_configured(text)` |
| `read_decisions` | function | `modules/lazy_intel.py:211` | `def read_decisions(task_id, limit)` |
| `record_routing_decision` | function | `modules/lazy_intel.py:129` | `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | function | `modules/lazy_intel.py:169` | `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` |
| `stack_signature` | function | `modules/lazy_intel.py:272` | `def stack_signature(assets)` |
| `_LINUX_LINE` | function | `modules/lazy_inventory.py:87` | `def _LINUX_LINE(line)` |
| `_WINDOWS_LINE` | function | `modules/lazy_inventory.py:104` | `def _WINDOWS_LINE(line)` |
| `_clean_entry` | function | `modules/lazy_inventory.py:114` | `def _clean_entry(product, version, os_hint)` |
| `inventory_blob` | function | `modules/lazy_inventory.py:49` | `def inventory_blob(platform)` |
| `os_platform_of` | function | `modules/lazy_inventory.py:157` | `def os_platform_of(entries)` |
| `parse_blob_output` | function | `modules/lazy_inventory.py:61` | `def parse_blob_output(text, platform)` |
| `to_sightings` | function | `modules/lazy_inventory.py:133` | `def to_sightings(entries, host)` |
| `_addon_run_pair` | function | `modules/lazy_ledger.py:89` | `def _addon_run_pair(rest)` |
| `_load` | function | `modules/lazy_ledger.py:121` | `def _load(sessions_dir)` |
| `_path` | function | `modules/lazy_ledger.py:114` | `def _path(sessions_dir)` |
| `_sort_key` | function | `modules/lazy_ledger.py:209` | `def _sort_key(pair)` |
| `fresh` | function | `modules/lazy_ledger.py:140` | `def fresh(verb, target, now, sessions_dir)` |
| `json_load` | function | `modules/lazy_ledger.py:133` | `def json_load(path)` |
| `key_from_command` | function | `modules/lazy_ledger.py:58` | `def key_from_command(command, target)` |
| `ledger_key` | function | `modules/lazy_ledger.py:53` | `def ledger_key(verb, target)` |
| `record` | function | `modules/lazy_ledger.py:164` | `def record(verb, target, ok, now, sessions_dir)` |
| `stale_first` | function | `modules/lazy_ledger.py:191` | `def stale_first(catalog, now, sessions_dir)` |
| `window_for` | function | `modules/lazy_ledger.py:32` | `def window_for(verb)` |
| `ActivityLog` | class | `modules/lazy_loop.py:1585` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2337` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1072` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1047` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2431` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:5503` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7538` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:6637` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1038` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1235` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1024` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6318` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1557` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1996` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2583` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:7862` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:1061` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:6927` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:6758` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3328` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5316` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2515` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7464` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7568` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:7730` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:7757` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2785` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:7687` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2743` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:7420` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1718` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4126` | `class Worker(WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1075` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1238` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1560` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1588` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1741` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1999` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2346` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2434` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2518` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2612` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2746` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2788` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3331` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4129` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5319` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:5511` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6321` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:6640` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6761` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:6944` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7423` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7541` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7690` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7733` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7887` | `def __init__(self, shell)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:5646` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:9898` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2281` | `def _asset_candidates(target)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5035` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9205` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:9241` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:5714` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:5528` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7040` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:10599` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3719` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:541` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:9816` | `def _check_goals(self, task_id, graph, activity)` |
| `_cold_path` | method | `modules/lazy_loop.py:5516` | `def _cold_path(self)` |
| `_constraints` | method | `modules/lazy_loop.py:3342` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:5706` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:3631` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:3543` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:595` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4019` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4975` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3351` | `def _denied(self, text)` |
| `_draft_report` | method | `modules/lazy_loop.py:6465` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:6461` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:9261` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9154` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2607` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:637` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:557` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:9829` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:9387` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2590` | `def _event_for(cls, path, item_id)` |
| `_find` | function | `modules/lazy_loop.py:5735` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:10495` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:4512` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:5674` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:9823` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:5723` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:4604` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_has_creds` | method | `modules/lazy_loop.py:3707` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:425` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:5308` | `def _host_like_target(target)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:8578` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:226` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:318` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:5670` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5299` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:504` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3166` | `def _lazy_policy()` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:3520` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:4033` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:915` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:923` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:2618` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6645` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7427` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7545` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7694` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:5532` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:5520` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2353` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:875` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2357` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6276` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2302` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10199` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:10173` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10219` | `def _maybe_selfupdate_check(self)` |
| `_noa_archive` | method | `modules/lazy_loop.py:5589` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:745` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1933` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:787` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:3661` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3511` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:3572` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8135` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3058` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1089` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1260` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2018` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2753` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2793` | `def _persist(self)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
