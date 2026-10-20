# Subsystem: modules (page 6 of 16)
Previous: [KB_modules_p5.md](KB_modules_p5.md)

## modules/goals.py
- Doc: Goal decomposition round-0 with constraints and proof.
- Layer: utility
- Language: py
- Symbols:
  - `GoalSpec` (class, line 20) `class GoalSpec`
  - `TaskConstraints` (class, line 29) `class TaskConstraints`
  - `decompose_rule_based` (function, line 63) `def decompose_rule_based(objective_text, max_goals)`
  - `load_constraints` (function, line 83) `def load_constraints(payload)`
  - `constraint_block_text` (function, line 103) `def constraint_block_text(constraints)`
  - `GoalTracker` (class, line 117) `class GoalTracker`
  - `blocked` (method, line 35) `def blocked(self, command)`
  - `__init__` (method, line 120) `def __init__(self, goals)`
  - `goals` (method, line 125) `def goals(self)`
  - `prove_goal` (method, line 129) `def prove_goal(self, goal_text, evidence)`
  - `goal_met` (method, line 140) `def goal_met(self, opt_in)`
  - `all_achieved` (method, line 148) `def all_achieved(self)`
  - `open_goals` (method, line 152) `def open_goals(self)`
- Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`

## modules/gpo_abuse.py
- Doc: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Layer: utility
- Language: py
- Symbols:
  - `GPOInfo` (class, line 54) `class GPOInfo`
  - `GPOAbusePlan` (class, line 83) `class GPOAbusePlan`
  - `GPOAbuseEngine` (class, line 105) `class GPOAbuseEngine`
  - `__init__` (method, line 118) `def __init__(self, domain, dc_ip)`
  - `parse_gpo_list` (method, line 124) `def parse_gpo_list(self, raw_gpo_output)`
  - `parse_bloodhound_gpos` (method, line 160) `def parse_bloodhound_gpos(self, bloodhound_nodes)`
  - `plan_scheduled_task` (method, line 182) `def plan_scheduled_task(self, gpo, command, task_name)`
  - `plan_startup_script` (method, line 208) `def plan_startup_script(self, gpo, script_content, script_name)`
  - `plan_logon_script` (method, line 238) `def plan_logon_script(self, gpo, command)`
  - `plan_local_admin_addition` (method, line 266) `def plan_local_admin_addition(self, gpo, username, group)`
  - `plan_wmi_filter_abuse` (method, line 293) `def plan_wmi_filter_abuse(self, gpo, wmi_query)`
  - `plan_registry_preference` (method, line 322) `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)`
  - `plan_service_installation` (method, line 356) `def plan_service_installation(self, gpo, service_name, binary_path)`
  - `generate_all_plans` (method, line 382) `def generate_all_plans(self, command, username)`
  - `detect_risky_gpos` (method, line 406) `def detect_risky_gpos(self)`
  - `summary` (method, line 434) `def summary(self)`
- Imported by: `cli/commands/active_directory.py`

## modules/gui_askpass.sh
- Doc: — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this...
- Layer: utility
- Language: sh
- Symbols:
  - `has` (function, line 22)
  - `try_zenity` (function, line 24)
  - `try_yad` (function, line 28)
  - `try_ssh_askpass` (function, line 33)
  - `try_kdialog` (function, line 40)

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
- Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`

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

## modules/icmp_client.py
- Doc: encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- Layer: infrastructure
- Language: py
- Symbols:
  - `encrypt_data` (function, line 18) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 34) `def decrypt_data(data, key)`
  - `check_sudo` (function, line 57) `def check_sudo()`
  - `checksum` (function, line 64) `def checksum(source_string)`
  - `send_icmp_packet` (function, line 82) `def send_icmp_packet(dest_addr, data, key)`
  - `receive_icmp_reply` (function, line 117) `def receive_icmp_reply(sock)`
  - `main` (function, line 130) `def main()`

## modules/icmp_server.py
- Doc: encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 44) `def check_sudo()`
  - `encrypt_data` (function, line 55) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 71) `def decrypt_data(data, key)`
  - `execute_command` (function, line 93) `def execute_command(command)`
  - `send_icmp_reply` (function, line 112) `def send_icmp_reply(sock, addr, data, key)`
  - `checksum` (function, line 132) `def checksum(source_string)`
  - `handle_packet` (function, line 150) `def handle_packet(packet, addr, key, sock)`
  - `listen_for_icmp` (function, line 175) `def listen_for_icmp(interface, key)`
  - `main` (function, line 202) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`
- Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`

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
  - `_family_color` (function, line 95) `def _family_color(name)`
  - `node_id` (function, line 106) `def node_id(kind, value)`
  - `_load_json` (function, line 112) `def _load_json(path, default)`
  - `_read_lines` (function, line 122) `def _read_lines(path, limit)`
  - `_host_mentions` (function, line 139) `def _host_mentions(text)`
  - `_file_pagerank` (function, line 146) `def _file_pagerank(ids, pairs, alpha, max_iter, tol)`
  - `build_intel_graph` (function, line 176) `def build_intel_graph(sessions_dir, est_cap)`
  - `_node_doc` (function, line 390) `def _node_doc(node)`
  - `_symbol_list` (function, line 413) `def _symbol_list(node)`
  - `_enrich_readmenator_fields` (function, line 428) `def _enrich_readmenator_fields(nodes, edges)`
  - `group_colors` (function, line 512) `def group_colors(graph)`
  - `page_settings` (function, line 528) `def page_settings(graph)`
  - `build_analytics` (function, line 585) `def build_analytics(graph, summary)`
  - `_fibonacci_sphere` (function, line 610) `def _fibonacci_sphere(count)`
  - `_split_caps` (function, line 626) `def _split_caps(labels, sizes, points, lattice, out)`
  - `_unit` (function, line 651) `def _unit(vec)`
  - `build_bundle_payload` (function, line 659) `def build_bundle_payload(graph)`
  - `bundle_settings` (function, line 769) `def bundle_settings(graph)`
  - `assign_layout` (function, line 800) `def assign_layout(graph, mode)`
  - `write_summary` (function, line 865) `def write_summary(graph, sessions_dir)`
  - `add_node` (function, line 183) `def add_node(kind, value, label)`
  - `add_edge` (function, line 197) `def add_edge(src, dst, kind, evidence, weight)`
  - `tag_source` (function, line 205) `def tag_source(nid, source)`
- Depends on: `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`
- Imported by: `lazyc2.py`, `modules/attack_surface3d.py`, `modules/sinks/intel_graph.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_intel_fusion.py`

## modules/intelligence_engine.py
- Doc: IntelligenceEngine — unified collection→analysis→intelligence pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `IntelligenceConfig` (class, line 57) `class IntelligenceConfig`
  - `CollectedFact` (class, line 78) `class CollectedFact`
  - `IntelligenceAssessment` (class, line 93) `class IntelligenceAssessment`
  - `CounterIntelFinding` (class, line 108) `class CounterIntelFinding`
  - `IntelligenceEngine` (class, line 119) `class IntelligenceEngine`
  - `get_intelligence_engine` (function, line 931) `def get_intelligence_engine(config)`
  - `__init__` (method, line 142) `def __init__(self, config)`
  - `collect_from_scan` (method, line 153) `def collect_from_scan(self, target)`
  - `collect_from_tool` (method, line 255) `def collect_from_tool(self, output, tool, host)`
  - `collect_from_estorides` (method, line 292) `def collect_from_estorides(self, target)`
  - `collect_from_nuclei` (method, line 334) `def collect_from_nuclei(self, target)`
  - `collect_from_yara` (method, line 376) `def collect_from_yara(self, target_path)`
  - `collect_from_factstore` (method, line 415) `def collect_from_factstore(self)`
  - `analyze` (method, line 477) `def analyze(self)`
  - `_correlate_services_to_vulns` (method, line 494) `def _correlate_services_to_vulns(self)`
  - `_match_known_vulns` (method, line 537) `def _match_known_vulns(fact)`
  - `_correlate_creds_to_hosts` (method, line 565) `def _correlate_creds_to_hosts(self)`
  - `_correlate_domains_to_infrastructure` (method, line 588) `def _correlate_domains_to_infrastructure(self)`
  - `_rank_targets` (method, line 604) `def _rank_targets(self)`
  - `_detect_killchain_gaps` (method, line 644) `def _detect_killchain_gaps(self)`
  - `produce_intelligence` (method, line 685) `def produce_intelligence(self)`
  - `_map_category_to_mitre` (method, line 700) `def _map_category_to_mitre(category)`
  - `produce_counter_intelligence` (method, line 715) `def produce_counter_intelligence(self)`
  - `disseminate` (method, line 765) `def disseminate(self)`
  - `run_full_cycle` (method, line 845) `def run_full_cycle(self, target)`
  - `get_intel_report` (method, line 874) `def get_intel_report(self)`
  - `_is_placeholder` (method, line 925) `def _is_placeholder(value)`
- Depends on: `core/logging.py`, `modules/estorides_importer.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
- Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`

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
- Imported by: `cli/commands/daemon_ctl.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`

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


Next: [KB_modules_p7.md](KB_modules_p7.md)
