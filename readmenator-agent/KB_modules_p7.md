# Subsystem: modules (page 7 of 18)
Previous: [KB_modules_p6.md](KB_modules_p6.md)

## modules/gym_registry.py
- Doc: Gym definitions and persistent run state.
- Layer: utility
- Language: py
- Symbols:
  - `_yaml_module` (function, line 85) `def _yaml_module()`
  - `slugify` (function, line 92) `def slugify(value)`
  - `validate_definition` (function, line 110) `def validate_definition(data, filename)`
  - `definition_path` (function, line 155) `def definition_path(gym_id, directory)`
  - `_read_yaml` (function, line 178) `def _read_yaml(path)`
  - `_normalize_definition` (function, line 188) `def _normalize_definition(data)`
  - `load_definitions` (function, line 207) `def load_definitions(directory)`
  - `scan_definitions` (function, line 239) `def scan_definitions(directory)`
  - `_write_yaml` (function, line 282) `def _write_yaml(path, data)`
  - `create_definition` (function, line 300) `def create_definition(gym_id)`
  - `update_definition_yaml` (function, line 369) `def update_definition_yaml(gym_id, text, directory)`
  - `delete_definition` (function, line 402) `def delete_definition(gym_id, directory)`
  - `_empty_state` (function, line 442) `def _empty_state()`
  - `_world_model` (function, line 447) `def _world_model()`
  - `_sanitize_state` (function, line 454) `def _sanitize_state(raw)`
  - `normalize_operator` (function, line 495) `def normalize_operator(value)`
  - `read_state` (function, line 501) `def read_state()`
  - `write_state` (function, line 520) `def write_state(state)`
  - `_merge_legacy` (function, line 532) `def _merge_legacy(state)`
  - `_next_run_id` (function, line 569) `def _next_run_id(state)`
  - `start_run` (function, line 579) `def start_run(challenge_id, definitions)`
  - `_matches` (function, line 625) `def _matches(run, selector)`
  - `get_active_runs` (function, line 637) `def get_active_runs(selector, operator)`
  - `select_run` (function, line 663) `def select_run(selector)`
  - `stop_runs` (function, line 695) `def stop_runs(selector)`
  - `pop_run` (function, line 724) `def pop_run(selector)`
  - `state_summary` (function, line 751) `def state_summary()`
  - `new_run_token` (function, line 761) `def new_run_token()`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`, `tests/test_winbox_gym.py`

## modules/gym_winbox_runner.py
- Doc: Ordered WinBox gym matrix runner.
- Layer: utility
- Language: py
- Symbols:
  - `plan_matrix` (function, line 21) `def plan_matrix(target, sessions_dir, only, top_k)`
  - `run_matrix` (function, line 51) `def run_matrix(target)`
  - `report` (function, line 118) `def report(sessions_dir)`
  - `chain_available` (function, line 130) `def chain_available(vuln_id)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_registry.py`

## modules/harness.py
- Doc: Deterministic harness gate for the LazyOwn loop.
- Layer: utility
- Language: py
- Symbols:
  - `harness_enabled` (function, line 30) `def harness_enabled()`
  - `gate` (function, line 65) `def gate(name)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/orchestrator_config.py`
- Imported by: `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop/worker_agentic.py`, `skills/lazyown_mcp_opencode.py`

## modules/hash_cracker.py
- Doc: Hash cracking pipeline — John the Ripper and Hashcat integration.
- Layer: utility
- Language: py
- Symbols:
  - `CrackResult` (class, line 127) `class CrackResult`
  - `HashIdentifier` (class, line 140) `class HashIdentifier`
  - `HashCracker` (class, line 151) `class HashCracker`
  - `crack_secretsdump_output` (function, line 695) `def crack_secretsdump_output(filepath, wordlist, rhost)`
  - `__init__` (method, line 164) `def __init__(self, wordlist, rules, use_hashcat, timeout)`
  - `_resolve_wordlist` (method, line 178) `def _resolve_wordlist(self)`
  - `identify` (method, line 186) `def identify(self, line)`
  - `identify_file` (method, line 273) `def identify_file(self, filepath)`
  - `crack_hash` (method, line 295) `def crack_hash(self, hash_value, hash_type, wordlist)`
  - `crack_file` (method, line 349) `def crack_file(self, filepath, wordlist, hash_types)`
  - `import_to_db` (method, line 405) `def import_to_db(self, results, rhost, workspace_name)`
  - `_crack_hashcat` (method, line 454) `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_hashcat` (method, line 500) `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)`
  - `_crack_john` (method, line 560) `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_john` (method, line 610) `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)`
  - `_parse_hashcat_output` (method, line 671) `def _parse_hashcat_output(stdout, stderr, original)`
  - `_parse_john_show` (method, line 686) `def _parse_john_show(show_output, original)`
- Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
- Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`

## modules/hive_invoke.py
- Doc: modules/hive_invoke.py
- Layer: utility
- Language: py
- Symbols:
  - `_get_toposwarm` (function, line 50) `def _get_toposwarm()`
  - `_find_claude` (function, line 115) `def _find_claude()`
  - `_parse_argv` (function, line 120) `def _parse_argv(argv)`
  - `_run_print_mode` (function, line 150) `def _run_print_mode(prompt, effort, claude_bin)`
  - `_run_interactive_mode` (function, line 172) `def _run_interactive_mode(prompt, effort, claude_bin)`
  - `_run_toposwarm_mode` (function, line 205) `def _run_toposwarm_mode(prompt, effort, bridge)`
  - `main` (function, line 255) `def main(argv)`
- Depends on: `modules/toposwarm_bridge.py`

## modules/hostdiscover.sh
- Layer: utility
- Language: sh
- Symbols:
  - `extract_ips_from_arp` (function, line 21)
  - `extract_listening_ips_from_netstat` (function, line 26)

## modules/hunt_verify.py
- Doc: Evidence verdict verification for hunting and chain stages.
- Layer: utility
- Language: py
- Symbols:
  - `EventRecord` (class, line 48) `class EventRecord`
  - `StageSpec` (class, line 60) `class StageSpec`
  - `Observation` (class, line 73) `class Observation`
  - `StageAssessment` (class, line 85) `class StageAssessment`
  - `Verification` (class, line 116) `class Verification`
  - `_unique` (function, line 140) `def _unique(values)`
  - `field_present` (function, line 152) `def field_present(fields, field_name)`
  - `_field_present` (function, line 172) `def _field_present(event, field_name)`
  - `_scalar_present` (function, line 177) `def _scalar_present(value)`
  - `_stage_matches` (function, line 188) `def _stage_matches(spec, event)`
  - `validate_specs` (function, line 197) `def validate_specs(specs)`
  - `verify_stages` (function, line 232) `def verify_stages(specs, observations, events, scope_covered)`
  - `_assess_stage` (function, line 310) `def _assess_stage(spec, observations, events, complete, warnings)`
  - `to_dict` (method, line 99) `def to_dict(self)`
  - `chain_proven` (method, line 124) `def chain_proven(self)`
  - `to_dict` (method, line 130) `def to_dict(self)`
- Imported by: `modules/chain_runner.py`, `modules/defense_stages.py`, `tests/test_hunt_verify.py`

## modules/ia_code_analysis.py
- Doc: CodeAnalyzer: Analyzes source code in a directory and its subdirectories.
- Layer: utility
- Language: py
- Symbols:
  - `CodeAnalyzer` (class, line 28) `class CodeAnalyzer`
  - `analyze_with_deepseek` (function, line 66) `def analyze_with_deepseek(code_content, file_path, mode)`
  - `save_results_to_json` (function, line 123) `def save_results_to_json(results, file_path)`
  - `start_analysis` (function, line 169) `def start_analysis(code_dir, mode)`
  - `parse_args` (function, line 178) `def parse_args()`
  - `__init__` (method, line 33) `def __init__(self, mode)`
  - `analyze_directory` (method, line 37) `def analyze_directory(self, directory)`
  - `analyze_code_file` (method, line 49) `def analyze_code_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_logs_analysis.py
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: AGPL v3...
- Layer: utility
- Language: py
- Symbols:
  - `LogFileHandler` (class, line 54) `class LogFileHandler(FileSystemEventHandler)`
  - `analyze_with_deepseek` (function, line 94) `def analyze_with_deepseek(log_content, mode)`
  - `start_monitoring` (function, line 147) `def start_monitoring(log_dir, mode)`
  - `parse_args` (function, line 168) `def parse_args()`
  - `__init__` (method, line 59) `def __init__(self, mode)`
  - `on_modified` (method, line 64) `def on_modified(self, event)`
  - `analyze_log_file` (method, line 75) `def analyze_log_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_network_analysis.py
- Doc: Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: AGPL v3  Descripción: Bot de monitoreo de...
- Layer: utility
- Language: py
- Symbols:
  - `analyze_with_deepseek` (function, line 39) `def analyze_with_deepseek(packet_info, mode)`
  - `packet_callback` (function, line 91) `def packet_callback(packet, mode)`
  - `start_monitoring` (function, line 130) `def start_monitoring(interface, timeout, mode)`
  - `parse_args` (function, line 154) `def parse_args()`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/img2bin.py
- Layer: utility
- Language: py
- Symbols:
  - `imagen_a_binario` (function, line 7) `def imagen_a_binario(imagen_input, binario_output, block_size)`
  - `main` (function, line 43) `def main()`

## modules/intel_fusion.py
- Doc: Sessions attack-intel fusion: data -> information -> intelligence.
- Layer: utility
- Language: py
- Symbols:
  - `_service_cve_matches` (function, line 83) `def _service_cve_matches(service_name, version_text, svc)`
  - `_extract_cve_id` (function, line 133) `def _extract_cve_id(vuln)`
  - `_family_color` (function, line 181) `def _family_color(name)`
  - `node_id` (function, line 192) `def node_id(kind, value)`
  - `_load_json` (function, line 198) `def _load_json(path, default)`
  - `_read_lines` (function, line 208) `def _read_lines(path, limit)`
  - `_host_mentions` (function, line 225) `def _host_mentions(text)`
  - `_file_pagerank` (function, line 230) `def _file_pagerank(ids, pairs, alpha, max_iter, tol)`
  - `build_intel_graph` (function, line 260) `def build_intel_graph(sessions_dir, est_cap)`
  - `_node_doc` (function, line 555) `def _node_doc(node)`
  - `_symbol_list` (function, line 578) `def _symbol_list(node)`
  - `_enrich_readmenator_fields` (function, line 593) `def _enrich_readmenator_fields(nodes, edges)`
  - `group_colors` (function, line 714) `def group_colors(graph)`
  - `page_settings` (function, line 730) `def page_settings(graph)`
  - `build_analytics` (function, line 787) `def build_analytics(graph, summary)`
  - `_fibonacci_sphere` (function, line 821) `def _fibonacci_sphere(count)`
  - `_split_caps` (function, line 837) `def _split_caps(labels, sizes, points, lattice, out)`
  - `_unit` (function, line 866) `def _unit(vec)`
  - `build_bundle_payload` (function, line 874) `def build_bundle_payload(graph)`
  - `bundle_settings` (function, line 990) `def bundle_settings(graph)`
  - `assign_layout` (function, line 1021) `def assign_layout(graph, mode)`
  - `_score_lines` (function, line 1086) `def _score_lines(host_value, detail)`
  - `_svg_text` (function, line 1124) `def _svg_text(value)`
  - `_svg_attr` (function, line 1131) `def _svg_attr(value)`
  - `_svg_rank` (function, line 1136) `def _svg_rank(node)`
  - `svg_selection` (function, line 1147) `def svg_selection(graph, cap_nodes)`
  - `_svg_place` (function, line 1165) `def _svg_place(ids)`
  - `_svg_host_of` (function, line 1182) `def _svg_host_of(node)`
  - `relations_svg` (function, line 1187) `def relations_svg(graph, cap_nodes)`
  - `_recency_lines` (function, line 1261) `def _recency_lines(sessions_dir, host_value)`
  - `_ghost_lines` (function, line 1279) `def _ghost_lines(sessions_dir, host_value)`
  - `write_summary` (function, line 1296) `def write_summary(graph, sessions_dir)`
  - `add_node` (function, line 266) `def add_node(kind, value, label)`
  - `add_edge` (function, line 284) `def add_edge(src, dst, kind, evidence, weight)`
  - `tag_source` (function, line 300) `def tag_source(nid, source)`
- Depends on: `modules/__init__.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`, `modules/lazy_world_diff.py`, `modules/world_model.py`
- Imported by: `lazyc2.py`, `modules/attack_surface3d.py`, `modules/sinks/intel_graph.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_cve_pipeline.py`, `tests/test_intel_fusion.py`

## modules/intelligence_engine.py
- Doc: IntelligenceEngine — unified collection→analysis→intelligence pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `IntelligenceConfig` (class, line 58) `class IntelligenceConfig`
  - `CollectedFact` (class, line 79) `class CollectedFact`
  - `IntelligenceAssessment` (class, line 94) `class IntelligenceAssessment`
  - `CounterIntelFinding` (class, line 109) `class CounterIntelFinding`
  - `IntelligenceEngine` (class, line 120) `class IntelligenceEngine`
  - `get_intelligence_engine` (function, line 1126) `def get_intelligence_engine(config)`
  - `__init__` (method, line 143) `def __init__(self, config)`
  - `_newest_scan_xml_with_versions` (method, line 154) `def _newest_scan_xml_with_versions(self, target)`
  - `_xml_scan_weight` (method, line 177) `def _xml_scan_weight(self, xml_path)`
  - `_xml_has_versions` (method, line 193) `def _xml_has_versions(self, xml_path)`
  - `collect_from_scan` (method, line 197) `def collect_from_scan(self, target)`
  - `_collect_from_scan_xml` (method, line 237) `def _collect_from_scan_xml(self, xml_path, target)`
  - `collect_from_tool` (method, line 326) `def collect_from_tool(self, output, tool, host)`
  - `collect_from_estorides` (method, line 363) `def collect_from_estorides(self, target)`
  - `collect_from_nuclei` (method, line 405) `def collect_from_nuclei(self, target)`
  - `collect_from_yara` (method, line 447) `def collect_from_yara(self, target_path)`
  - `collect_from_factstore` (method, line 486) `def collect_from_factstore(self)`
  - `analyze` (method, line 587) `def analyze(self)`
  - `_correlate_services_to_vulns` (method, line 604) `def _correlate_services_to_vulns(self)`
  - `_match_vulns_versioned` (method, line 649) `def _match_vulns_versioned(self, fact)`
  - `_legacy_match_rows` (method, line 679) `def _legacy_match_rows(self, fact)`
  - `_match_known_vulns` (method, line 708) `def _match_known_vulns(fact)`
  - `_correlate_creds_to_hosts` (method, line 736) `def _correlate_creds_to_hosts(self)`
  - `_correlate_domains_to_infrastructure` (method, line 759) `def _correlate_domains_to_infrastructure(self)`
  - `_rank_targets` (method, line 775) `def _rank_targets(self)`
  - `_detect_killchain_gaps` (method, line 815) `def _detect_killchain_gaps(self)`
  - `produce_intelligence` (method, line 856) `def produce_intelligence(self)`
  - `_map_category_to_mitre` (method, line 871) `def _map_category_to_mitre(category)`
  - `produce_counter_intelligence` (method, line 886) `def produce_counter_intelligence(self)`
  - `disseminate` (method, line 936) `def disseminate(self)`
  - `run_full_cycle` (method, line 1040) `def run_full_cycle(self, target)`
  - `get_intel_report` (method, line 1069) `def get_intel_report(self)`
  - `_is_placeholder` (method, line 1120) `def _is_placeholder(value)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/estorides_importer.py`, `modules/factsio.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/lazy_heat.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
- Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `tests/test_intelligence_engine.py`, `tests/test_single_source_of_truth.py`

## modules/intercept.py
- Doc: User-configurable tool-call interception layer with human-in-loop approvals.
- Layer: utility
- Language: py
- Symbols:
  - `InterceptAction` (class, line 21) `class InterceptAction(str, Enum)`
  - `InterceptConfig` (class, line 33) `class InterceptConfig`
  - `InterceptRule` (class, line 50) `class InterceptRule`
  - `PendingApproval` (class, line 77) `class PendingApproval`
  - `InterceptVerdict` (class, line 92) `class InterceptVerdict`
  - `builtin_rules` (function, line 101) `def builtin_rules()`
  - `scope_blocked` (function, line 131) `def scope_blocked(target)`
  - `observe_post_tool` (function, line 144) `def observe_post_tool(output)`
  - `Interceptor` (class, line 154) `class Interceptor`
  - `Guard` (class, line 255) `class Guard`
  - `__post_init__` (method, line 61) `def __post_init__(self)`
  - `matches` (method, line 68) `def matches(self, tool, command)`
  - `__init__` (method, line 157) `def __init__(self, rules, ask_timeout_sec, timeout_action)`
  - `rules` (method, line 172) `def rules(self)`
  - `add_rule` (method, line 177) `def add_rule(self, rule)`
  - `remove_rule` (method, line 183) `def remove_rule(self, pattern)`
  - `evaluate` (method, line 192) `def evaluate(self, tool, command)`
  - `decide` (method, line 220) `def decide(self, approval_id, decision)`
  - `pending_approvals` (method, line 234) `def pending_approvals(self)`
  - `approval_status` (method, line 249) `def approval_status(self, approval_id)`
  - `__init__` (method, line 258) `def __init__(self, interceptor)`
  - `interceptor` (method, line 266) `def interceptor(self)`
  - `check` (method, line 270) `def check(self, tool, command)`
  - `observe` (method, line 282) `def observe(self, output, source)`
  - `record_failure` (method, line 291) `def record_failure(self, source)`
  - `audit_log` (method, line 296) `def audit_log(self, limit)`
  - `attribution` (method, line 301) `def attribution(self)`
- Depends on: `cli/commands/enum.py`
- Imported by: `cli/commands/daemon_ctl.py`, `modules/lazy_loop.py`, `modules/loop/worker_gating.py`, `skills/autonomous_daemon.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`

## modules/internal_discover.sh
- Layer: utility
- Language: sh

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
  - `KillChainConfig` (class, line 99) `class KillChainConfig`
  - `PhaseStatus` (class, line 197) `class PhaseStatus`
  - `KillChain` (class, line 206) `class KillChain`
  - `get_killchain` (function, line 566) `def get_killchain()`
  - `technique_for_phase` (function, line 571) `def technique_for_phase(phase)`
  - `technique_for_vulnclass` (function, line 576) `def technique_for_vulnclass(vulnclass)`
  - `world_model_path` (method, line 177) `def world_model_path(self)`
  - `phase_index` (method, line 181) `def phase_index(self, phase)`
  - `is_valid_phase` (method, line 188) `def is_valid_phase(self, phase)`
  - `config` (method, line 215) `def config()`
  - `phases` (method, line 220) `def phases()`
  - `phase_labels` (method, line 225) `def phase_labels()`
  - `phase_colors` (method, line 230) `def phase_colors()`
  - `phase_rich_colors` (method, line 235) `def phase_rich_colors()`
  - `engagement_phase_to_cli` (method, line 240) `def engagement_phase_to_cli(engagement_value)`
  - `cli_phase_to_host_state` (method, line 252) `def cli_phase_to_host_state(phase)`
  - `current_phase` (method, line 265) `def current_phase(world_model_path)`
  - `advance_phase` (method, line 312) `def advance_phase(new_phase, world_model_path, host, extras)`
  - `get_progress` (method, line 416) `def get_progress(world_model_path)`
  - `compact_progress` (method, line 465) `def compact_progress(current_phase, phases_entered)`
  - `phases_for_display` (method, line 485) `def phases_for_display()`
  - `phase_index` (method, line 496) `def phase_index(phase)`
  - `snapshot` (method, line 501) `def snapshot(world_model_path)`
  - `technique_for_phase` (method, line 541) `def technique_for_phase(phase)`
  - `technique_for_vulnclass` (method, line 553) `def technique_for_vulnclass(vulnclass)`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/lazy_orchestrator.py`, `cli/lazynmap_post.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/mcp_tools/campaign_sitrep.py`, `skills/mcp_tools/session_init.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`, `tests/test_lazy_loop.py`, `tests/test_single_source_of_truth.py`


Next: [KB_modules_p8.md](KB_modules_p8.md)
