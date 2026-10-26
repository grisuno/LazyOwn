# Subsystem: modules (page 7 of 16)
Previous: [KB_modules_p6.md](KB_modules_p6.md)

## modules/iptables_portforward.sh
- Layer: utility
- Language: sh
- Symbols:
  - `display_usage` (function, line 29)

## modules/jsonl_tail.py
- Doc: Incremental JSONL reader shared by the monitor TUI and the loop runner.
- Layer: utility
- Language: py
- Symbols:
  - `JsonlTail` (class, line 14) `class JsonlTail`
  - `__init__` (method, line 17) `def __init__(self, path)`
  - `read_new` (method, line 22) `def read_new(self, limit)`
- Imported by: `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_runner.py`

## modules/jwtexploit.py
- Layer: utility
- Language: py

## modules/k8s_attacks.py
- Doc: Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse.
- Layer: utility
- Language: py
- Symbols:
  - `K8sConfig` (class, line 57) `class K8sConfig`
  - `K8SAttackEngine` (class, line 77) `class K8SAttackEngine`
  - `__init__` (method, line 87) `def __init__(self, config)`
  - `enumerate_rbac` (method, line 90) `def enumerate_rbac(self)`
  - `privileged_pod_escape` (method, line 118) `def privileged_pod_escape(self)`
  - `service_account_token_theft` (method, line 173) `def service_account_token_theft(self)`
  - `kubelet_anonymous_auth_abuse` (method, line 198) `def kubelet_anonymous_auth_abuse(self)`
  - `etcd_access_exploitation` (method, line 222) `def etcd_access_exploitation(self)`
  - `helm_tiller_abuse` (method, line 250) `def helm_tiller_abuse(self)`
  - `persistence_techniques` (method, line 278) `def persistence_techniques(self)`
  - `summary` (method, line 318) `def summary(self)`
- Imported by: `cli/commands/cloud_attacks.py`

## modules/kerberoasting.py
- Doc: Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration.
- Layer: utility
- Language: py
- Symbols:
  - `KerberoastTarget` (class, line 38) `class KerberoastTarget`
  - `KerberoastHash` (class, line 59) `class KerberoastHash`
  - `KerberoastingEngine` (class, line 79) `class KerberoastingEngine`
  - `__init__` (method, line 95) `def __init__(self, domain, dc_ip, username, password, hash)`
  - `enumerate_spns` (method, line 112) `def enumerate_spns(self, ldap_output, bloodhound_data)`
  - `_prioritize_targets` (method, line 169) `def _prioritize_targets(self)`
  - `request_tgs_aes_only` (method, line 187) `def request_tgs_aes_only(self, user_spn)`
  - `request_tgs_rc4` (method, line 208) `def request_tgs_rc4(self, user_spn)`
  - `request_tgs` (method, line 219) `def request_tgs(self, user_spn, etype)`
  - `_build_hash_string` (method, line 248) `def _build_hash_string(self, spn, etype)`
  - `_hashcat_command` (method, line 268) `def _hashcat_command(hash_str, mode)`
  - `targeted_kerberoast` (method, line 271) `def targeted_kerberoast(self, high_value_only)`
  - `asreproast_check` (method, line 306) `def asreproast_check(self, usernames)`
  - `extract_hashes_from_pcap` (method, line 321) `def extract_hashes_from_pcap(self, pcap_path)`
  - `detect_kerberoasting_activity` (method, line 336) `def detect_kerberoasting_activity(self, event_log)`
  - `build_hashcat_batch` (method, line 379) `def build_hashcat_batch(self, output_path)`
  - `summary` (method, line 401) `def summary(self)`
  - `priority` (function, line 172) `def priority(target)`
- Depends on: `modules/kerberos_core.py`
- Imported by: `cli/commands/active_directory.py`

## modules/kerberos_core.py
- Doc: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- Layer: utility
- Language: py
- Symbols:
  - `KerberosPrincipal` (class, line 139) `class KerberosPrincipal`
  - `EncryptedData` (class, line 157) `class EncryptedData`
  - `KerberosTicket` (class, line 172) `class KerberosTicket`
  - `PACSignature` (class, line 213) `class PACSignature`
  - `PACInfo` (class, line 228) `class PACInfo`
  - `TGSRequest` (class, line 249) `class TGSRequest`
  - `KerberosCrypto` (class, line 271) `class KerberosCrypto`
  - `KerberosCore` (class, line 407) `class KerberosCore`
  - `KerberosErrorParser` (class, line 683) `class KerberosErrorParser`
  - `TicketValidator` (class, line 702) `class TicketValidator`
  - `to_string` (method, line 152) `def to_string(self)`
  - `has_flag` (method, line 207) `def has_flag(self, flag_name)`
  - `__init__` (method, line 277) `def __init__(self)`
  - `derive_aes_key` (method, line 282) `def derive_aes_key(password, salt, etype)`
  - `derive_rc4_key` (method, line 318) `def derive_rc4_key(password)`
  - `aes_encrypt` (method, line 329) `def aes_encrypt(self, key, plaintext, usage)`
  - `aes_decrypt` (method, line 361) `def aes_decrypt(self, key, ciphertext, usage)`
  - `compute_checksum` (method, line 389) `def compute_checksum(key, data, etype)`
  - `__init__` (method, line 421) `def __init__(self, domain, dc_host, dc_ip)`
  - `get_supported_etypes` (method, line 427) `def get_supported_etypes(self)`
  - `build_as_req` (method, line 435) `def build_as_req(self, username, domain, password, etype)`
  - `build_tgs_req` (method, line 489) `def build_tgs_req(self, params)`
  - `parse_as_rep` (method, line 534) `def parse_as_rep(self, as_rep_data, key, etype)`
  - `parse_tgs_rep` (method, line 550) `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)`
  - `decrypt_ticket` (method, line 563) `def decrypt_ticket(self, ticket_data, key, etype)`
  - `parse_pac` (method, line 588) `def parse_pac(self, pac_data)`
  - `_parse_pac_buffer` (method, line 622) `def _parse_pac_buffer(pac, buf_type, buf_data)`
  - `_build_pa_enc_timestamp` (method, line 640) `def _build_pa_enc_timestamp(self, key, etype, timestamp)`
  - `_parse_kdc_rep` (method, line 653) `def _parse_kdc_rep(self, data, key, etype, rep_type)`
  - `_rc4_encrypt` (method, line 667) `def _rc4_encrypt(key, data, usage)`
  - `_rc4_decrypt` (method, line 676) `def _rc4_decrypt(key, data, usage)`
  - `parse_error` (method, line 687) `def parse_error(error_data)`
  - `is_expired` (method, line 706) `def is_expired(endtime, grace_period)`
  - `validate_flags` (method, line 719) `def validate_flags(ticket, required_flags)`
  - `validate_pac_checksums` (method, line 735) `def validate_pac_checksums(pac)`
- Imported by: `modules/kerberoasting.py`, `modules/kerberos_tickets.py`

## modules/kerberos_tickets.py
- Doc: Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets.
- Layer: utility
- Language: py
- Symbols:
  - `SilverTicketConfig` (class, line 36) `class SilverTicketConfig`
  - `GoldenTicketConfig` (class, line 65) `class GoldenTicketConfig`
  - `DiamondTicketConfig` (class, line 94) `class DiamondTicketConfig`
  - `SilverTicketForger` (class, line 124) `class SilverTicketForger`
  - `GoldenTicketForger` (class, line 265) `class GoldenTicketForger`
  - `DiamondTicketForger` (class, line 397) `class DiamondTicketForger`
  - `SapphireTicketForger` (class, line 462) `class SapphireTicketForger`
  - `SkeletonKeyInjector` (class, line 567) `class SkeletonKeyInjector`
  - `__init__` (method, line 131) `def __init__(self)`
  - `forge` (method, line 134) `def forge(self, config)`
  - `_resolve_key` (method, line 190) `def _resolve_key(self, config)`
  - `_build_silver_pac` (method, line 200) `def _build_silver_pac(self, config, start, end)`
  - `_build_enc_ticket_part` (method, line 206) `def _build_enc_ticket_part(self, config, start, end, flags, key, etype)`
  - `_build_ticket_structure` (method, line 225) `def _build_ticket_structure(self, config, flags, enc_part)`
  - `_build_kirbi` (method, line 235) `def _build_kirbi(self, ticket, enc_part, etype)`
  - `_mimikatz_inject_command` (method, line 244) `def _mimikatz_inject_command(self, config)`
  - `_impacket_command` (method, line 254) `def _impacket_command(self, config)`
  - `__init__` (method, line 272) `def __init__(self)`
  - `forge` (method, line 275) `def forge(self, config)`
  - `_resolve_krbtgt_key` (method, line 324) `def _resolve_krbtgt_key(self, config)`
  - `_build_golden_pac` (method, line 339) `def _build_golden_pac(self, config)`
  - `_build_golden_enc_part` (method, line 346) `def _build_golden_enc_part(self, config, start, end, flags, key)`
  - `_assemble_tgt` (method, line 368) `def _assemble_tgt(self, config, flags, enc_part)`
  - `_mimikatz_command` (method, line 379) `def _mimikatz_command(self, config)`
  - `_impacket_command` (method, line 388) `def _impacket_command(self, config)`
  - `__init__` (method, line 405) `def __init__(self)`
  - `forge` (method, line 408) `def forge(self, config)`
  - `_build_diamond_pac` (method, line 446) `def _build_diamond_pac(self, config)`
  - `__init__` (method, line 469) `def __init__(self, kerberos_core)`
  - `forge_s4u2self` (method, line 472) `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)`
  - `forge_rbcd` (method, line 530) `def forge_rbcd(self, machine_account_hash, target_service, domain, username)`
  - `detect_skeleton_key` (method, line 578) `def detect_skeleton_key(target_host, domain, dc_ip)`
  - `inject_command` (method, line 600) `def inject_command(target_host)`
  - `cleanup_command` (method, line 612) `def cleanup_command()`
- Depends on: `modules/kerberos_core.py`
- Imported by: `cli/commands/active_directory.py`

## modules/kill_chain_viz.py
- Doc: SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG.
- Layer: utility
- Language: py
- Symbols:
  - `_load_phases` (function, line 20) `def _load_phases(sessions)`
  - `_read_target` (function, line 27) `def _read_target()`
  - `_build_svg` (function, line 34) `def _build_svg(phases)`
  - `generate_html` (function, line 69) `def generate_html(target, sessions)`
  - `generate_svg` (function, line 102) `def generate_svg(target, sessions)`
- Depends on: `modules/killchain.py`
- Imported by: `lazyc2.py`

## modules/killchain.py
- Doc: Unified kill-chain — single source of truth consumed by all surfaces.
- Layer: utility
- Language: py
- Symbols:
  - `KillChainConfig` (class, line 40) `class KillChainConfig`
  - `PhaseStatus` (class, line 138) `class PhaseStatus`
  - `KillChain` (class, line 147) `class KillChain`
  - `get_killchain` (function, line 482) `def get_killchain()`
  - `world_model_path` (method, line 118) `def world_model_path(self)`
  - `phase_index` (method, line 122) `def phase_index(self, phase)`
  - `is_valid_phase` (method, line 129) `def is_valid_phase(self, phase)`
  - `config` (method, line 156) `def config()`
  - `phases` (method, line 161) `def phases()`
  - `phase_labels` (method, line 166) `def phase_labels()`
  - `phase_colors` (method, line 171) `def phase_colors()`
  - `phase_rich_colors` (method, line 176) `def phase_rich_colors()`
  - `engagement_phase_to_cli` (method, line 181) `def engagement_phase_to_cli(engagement_value)`
  - `cli_phase_to_host_state` (method, line 193) `def cli_phase_to_host_state(phase)`
  - `current_phase` (method, line 206) `def current_phase(world_model_path)`
  - `advance_phase` (method, line 253) `def advance_phase(new_phase, world_model_path, host, extras)`
  - `get_progress` (method, line 357) `def get_progress(world_model_path)`
  - `compact_progress` (method, line 406) `def compact_progress(current_phase, phases_entered)`
  - `phases_for_display` (method, line 426) `def phases_for_display()`
  - `phase_index` (method, line 437) `def phase_index(phase)`
  - `snapshot` (method, line 442) `def snapshot(world_model_path)`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/lazynmap_post.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazy_cli_bridge.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`, `tests/test_single_source_of_truth.py`

## modules/kivi.py
- Layer: utility
- Language: py
- Symbols:
  - `ReverseShellApp` (class, line 11) `class ReverseShellApp(App)`
  - `build` (method, line 12) `def build(self)`
  - `connect_to_server` (method, line 27) `def connect_to_server(self, instance)`

## modules/lab_runtime.py
- Doc: Lab runtime: Docker lifecycle for practice targets and cyber ranges.
- Layer: utility
- Language: py
- Symbols:
  - `docker_available` (function, line 81) `def docker_available()`
  - `_docker` (function, line 95) `def _docker()`
  - `running_containers` (function, line 103) `def running_containers()`
  - `existing_containers` (function, line 119) `def existing_containers()`
  - `running_range_containers` (function, line 136) `def running_range_containers()`
  - `container_name` (function, line 152) `def container_name(scenario)`
  - `container_ip` (function, line 157) `def container_ip(container_name)`
  - `ensure_web` (function, line 171) `def ensure_web(scenario, name)`
  - `apply_gym_migrations` (function, line 185) `def apply_gym_migrations(name)`
  - `start` (function, line 193) `def start(scenario)`
  - `stop` (function, line 241) `def stop(scenario)`
  - `stop_all` (function, line 259) `def stop_all()`
  - `range_compose` (function, line 277) `def range_compose(profile)`
  - `start_range` (function, line 286) `def start_range(profile)`
  - `stop_range` (function, line 305) `def stop_range(profile)`
  - `stop_ranges` (function, line 316) `def stop_ranges()`
  - `_docker_compose` (function, line 349) `def _docker_compose(args)`
  - `ensure_range_secret` (function, line 357) `def ensure_range_secret(profile_dir)`
- Depends on: `modules/metasploitable_migrations.py`

## modules/lazy_agent.py
- Doc: Agentic tool-calling bridge for the loop and the main agent.
- Layer: utility
- Language: py
- Symbols:
  - `model_timeout_sec` (function, line 41) `def model_timeout_sec()`
  - `tool_calling_enabled` (function, line 57) `def tool_calling_enabled()`
  - `max_iterations` (function, line 72) `def max_iterations()`
  - `resolve_agentic_model` (function, line 83) `def resolve_agentic_model(exclude)`
  - `_enable_streaming` (function, line 123) `def _enable_streaming(runner, on_event)`
  - `ObservableAgentRunner` (class, line 145) `class ObservableAgentRunner(AgentRunner)`
  - `_json_default` (function, line 221) `def _json_default(value)`
  - `_deep_clean` (function, line 237) `def _deep_clean(value, _depth)`
  - `_json_safe` (function, line 253) `def _json_safe(messages)`
  - `ConversationStore` (class, line 261) `class ConversationStore`
  - `register_tools` (function, line 322) `def register_tools(runner, specs)`
  - `run_worker_session` (function, line 335) `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)`
  - `run_main_session` (function, line 374) `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)`
  - `run_external_opencode` (function, line 396) `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)`
  - `run_external_hermes` (function, line 472) `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)`
  - `_session_from_line` (function, line 556) `def _session_from_line(line)`
  - `_process_watchdog` (function, line 578) `def _process_watchdog(timeout_sec, process)`
  - `__init__` (method, line 148) `def __init__(self, model, system_prompt, max_iterations, on_event)`
  - `_process_tool_call` (method, line 159) `def _process_tool_call(self, tool_call)`
  - `run` (method, line 168) `def run(self, user_input)`
  - `_call_model` (method, line 174) `def _call_model(self)`
  - `__init__` (method, line 264) `def __init__(self, task_id)`
  - `_load` (method, line 269) `def _load(self)`
  - `intent_messages` (method, line 273) `def intent_messages(self, intent_id)`
  - `save_intent` (method, line 278) `def save_intent(self, intent_id, messages)`
  - `session` (method, line 287) `def session(self, session_id)`
  - `sessions` (method, line 291) `def sessions(self)`
  - `save_session` (method, line 305) `def save_session(self, session_id, messages, title)`
  - `reset_intents` (method, line 315) `def reset_intents(self)`
  - `_kill` (function, line 583) `def _kill()`
  - `_invoke` (function, line 190) `def _invoke()`
  - `_tick` (function, line 196) `def _tick()`
- Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
- Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`

## modules/lazy_bridge.py
- Doc: Bidirectional LAZY <-> LazyOwn bridge.
- Layer: utility
- Language: py
- Symbols:
  - `_data_dir` (function, line 35) `def _data_dir()`
  - `_read_json` (function, line 51) `def _read_json(path, default)`
  - `_read_jsonl` (function, line 68) `def _read_jsonl(path)`
  - `lazy_tasks` (function, line 92) `def lazy_tasks()`
  - `lazy_assets` (function, line 103) `def lazy_assets()`
  - `lazy_graph` (function, line 114) `def lazy_graph(task_id)`
  - `lazy_activity` (function, line 127) `def lazy_activity(task_id)`
  - `lazy_traffic` (function, line 139) `def lazy_traffic(task_id)`
  - `lazy_guard_audit` (function, line 151) `def lazy_guard_audit(task_id)`
  - `bridge_status` (function, line 163) `def bridge_status()`
  - `_extract_hosts_from_graph` (function, line 184) `def _extract_hosts_from_graph(graph)`
  - `pull_to_world_model` (function, line 221) `def pull_to_world_model()`
  - `pull_to_objectives` (function, line 298) `def pull_to_objectives()`
  - `pull_findings_to_lifecycle` (function, line 333) `def pull_findings_to_lifecycle()`
  - `_read_new_traffic` (function, line 361) `def _read_new_traffic(path, offset)`
  - `_notify` (function, line 398) `def _notify(progress, text)`
  - `pull_traffic_to_recorder` (function, line 408) `def pull_traffic_to_recorder(progress)`
  - `push_objective_to_lazy` (function, line 476) `def push_objective_to_lazy(goal, scope)`
  - `push_tasks_to_c2` (function, line 501) `def push_tasks_to_c2(only)`
  - `sync_all` (function, line 566) `def sync_all(progress)`
  - `_record_sync` (function, line 592) `def _record_sync(action, summary)`
- Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
- Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_cve_pipeline.py`, `tests/test_lazy_loop.py`

## modules/lazy_cli_bridge.py
- Doc: Full CLI catalog for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_source_files` (function, line 74) `def _source_files()`
  - `_source_mtimes` (function, line 82) `def _source_mtimes()`
  - `_discover` (function, line 93) `def _discover()`
  - `cli_verbs` (function, line 106) `def cli_verbs()`
  - `is_cli_verb` (function, line 125) `def is_cli_verb(name)`
  - `phase_for` (function, line 131) `def phase_for(verb)`
  - `risk_for` (function, line 140) `def risk_for(verb)`
  - `needs_target_for` (function, line 150) `def needs_target_for(verb)`
  - `build_cli_command` (function, line 158) `def build_cli_command(verb, target)`
  - `search_cli_verbs` (function, line 185) `def search_cli_verbs(query, phase, limit)`
  - `cli_catalog_for_phase` (function, line 211) `def cli_catalog_for_phase(phase, limit)`
  - `catalog_cli_for_phase` (function, line 219) `def catalog_cli_for_phase(limit)`
  - `full_cli_enabled` (function, line 253) `def full_cli_enabled()`
  - `set_full_cli` (function, line 276) `def set_full_cli(enabled)`
- Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`

## modules/lazy_cve_feed.py
- Doc: Keyless CVE intelligence feeds and version-aware service correlation.
- Layer: utility
- Language: py
- Symbols:
  - `_env_flag` (function, line 90) `def _env_flag(name, default)`
  - `_cache_path` (function, line 95) `def _cache_path(name)`
  - `_cache_fresh` (function, line 104) `def _cache_fresh(path, ttl_sec)`
  - `_fetch` (function, line 112) `def _fetch(url)`
  - `_store_bytes` (function, line 134) `def _store_bytes(name, payload)`
  - `_store_json` (function, line 142) `def _store_json(name, data)`
  - `_load_json` (function, line 150) `def _load_json(name)`
  - `load_kev` (function, line 158) `def load_kev(force)`
  - `load_epss` (function, line 192) `def load_epss(force)`
  - `_exploit_cves_from_text` (function, line 228) `def _exploit_cves_from_text(text)`
  - `load_exploit_cves` (function, line 233) `def load_exploit_cves(force)`
  - `load_msf_cves` (function, line 257) `def load_msf_cves(force)`
  - `_osv_cache_path` (function, line 281) `def _osv_cache_path(product)`
  - `fetch_product_advisories` (function, line 291) `def fetch_product_advisories(product, force)`
  - `cve_intel` (function, line 360) `def cve_intel(cve_id, feeds, allow_network)`
  - `_advisory_cve_id` (function, line 398) `def _advisory_cve_id(advisory)`
  - `_advisory_cvss` (function, line 407) `def _advisory_cvss(advisory)`
  - `_advisory_matches_product` (function, line 421) `def _advisory_matches_product(advisory, banner_words)`
  - `correlate` (function, line 438) `def correlate(product, version, allow_network)`
  - `load_kev_matches` (function, line 526) `def load_kev_matches(product, feeds)`
  - `hot_matches` (function, line 568) `def hot_matches(services, allow_network)`
  - `refresh_feeds_async` (function, line 612) `def refresh_feeds_async(products)`
  - `_worker` (function, line 628) `def _worker()`
- Depends on: `modules/lazy_heat.py`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`

## modules/lazy_engine.py
- Doc: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Layer: utility
- Language: py
- Symbols:
  - `LazyEngine` (class, line 55) `class LazyEngine(LazyLoopEngine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `cli/commands/lazyloop.py`, `cli/commands/lazyops.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `modules/lazy_loop.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`, `tests/test_session_brief.py`

## modules/lazy_heat.py
- Doc: Heat tiers and version math for CVE correlation.
- Layer: utility
- Language: py
- Symbols:
  - `classify_heat` (function, line 68) `def classify_heat(kev, epss, exploit, cvss)`
  - `match_heat` (function, line 91) `def match_heat(tier, cvss, verdict, distro_status)`
  - `parse_version` (function, line 118) `def parse_version(value, strict)`
  - `compare_versions` (function, line 154) `def compare_versions(a, b)`
  - `version_in_range` (function, line 162) `def version_in_range(ver, rng)`
  - `cvss3_base_score` (function, line 204) `def cvss3_base_score(vector)`
  - `product_token` (function, line 246) `def product_token(value)`
  - `token_matches` (function, line 269) `def token_matches(haystack, needle)`
  - `parse_distro_revision` (function, line 303) `def parse_distro_revision(banner)`
  - `backport_status` (function, line 342) `def backport_status(banner, fixed_revision)`
  - `label_for` (function, line 370) `def label_for(status, fixed_revision)`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_cve_feed.py`

## modules/lazy_installer.py
- Doc: Capability installer for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `installer_enabled` (function, line 41) `def installer_enabled()`
  - `set_installer_enabled` (function, line 58) `def set_installer_enabled(enabled)`
  - `install_command_for` (function, line 70) `def install_command_for(tool)`
  - `intent_for` (function, line 75) `def intent_for(tool)`
  - `tool_from_intent` (function, line 80) `def tool_from_intent(text)`
  - `steps_for_install` (function, line 88) `def steps_for_install(text)`
- Depends on: `core/config.py`, `modules/auto_registry.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`

## modules/lazy_intel.py
- Doc: Intel feed from the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_now` (function, line 30) `def _now()`
  - `_log_path` (function, line 35) `def _log_path()`
  - `_mask` (function, line 41) `def _mask(text)`
  - `_append` (function, line 79) `def _append(record)`
  - `infer_source` (function, line 88) `def infer_source(command, intent_text)`
  - `describe_command` (function, line 114) `def describe_command(command)`
  - `record_routing_decision` (function, line 129) `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)`
  - `record_routing_outcome` (function, line 169) `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)`
  - `read_decisions` (function, line 211) `def read_decisions(task_id, limit)`
  - `mask_configured` (function, line 237) `def mask_configured(text)`
  - `stack_signature` (function, line 272) `def stack_signature(assets)`
  - `_is_ip_literal` (function, line 292) `def _is_ip_literal(value)`
  - `fuse_routing_decisions` (function, line 303) `def fuse_routing_decisions(task_id)`
  - `export_spans` (function, line 342) `def export_spans(task_id, out)`
- Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/mediation/__init__.py`, `modules/world_model.py`, `utils.py`
- Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/mediation/intel_mediator.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`


Next: [KB_modules_p8.md](KB_modules_p8.md)
