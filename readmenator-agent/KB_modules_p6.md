# Subsystem: modules (page 6 of 15)
Previous: [KB_modules_p5.md](KB_modules_p5.md)

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
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: GPL v3...
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
- Doc: Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: GPL v3  Descripción: Bot de monitoreo de...
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

## modules/killchain.py
- Doc: Unified kill-chain — single source of truth consumed by all surfaces.
- Layer: utility
- Language: py
- Symbols:
  - `KillChainConfig` (class, line 38) `class KillChainConfig`
  - `PhaseStatus` (class, line 136) `class PhaseStatus`
  - `KillChain` (class, line 145) `class KillChain`
  - `get_killchain` (function, line 453) `def get_killchain()`
  - `world_model_path` (method, line 116) `def world_model_path(self)`
  - `phase_index` (method, line 120) `def phase_index(self, phase)`
  - `is_valid_phase` (method, line 127) `def is_valid_phase(self, phase)`
  - `config` (method, line 154) `def config()`
  - `phases` (method, line 159) `def phases()`
  - `phase_labels` (method, line 164) `def phase_labels()`
  - `phase_colors` (method, line 169) `def phase_colors()`
  - `phase_rich_colors` (method, line 174) `def phase_rich_colors()`
  - `engagement_phase_to_cli` (method, line 179) `def engagement_phase_to_cli(engagement_value)`
  - `cli_phase_to_host_state` (method, line 191) `def cli_phase_to_host_state(phase)`
  - `current_phase` (method, line 204) `def current_phase(world_model_path)`
  - `advance_phase` (method, line 251) `def advance_phase(new_phase, world_model_path, host)`
  - `get_progress` (method, line 328) `def get_progress(world_model_path)`
  - `compact_progress` (method, line 377) `def compact_progress(current_phase, phases_entered)`
  - `phases_for_display` (method, line 397) `def phases_for_display()`
  - `phase_index` (method, line 408) `def phase_index(phase)`
  - `snapshot` (method, line 413) `def snapshot(world_model_path)`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`

## modules/kivi.py
- Layer: utility
- Language: py
- Symbols:
  - `ReverseShellApp` (class, line 11) `class ReverseShellApp(App)`
  - `build` (method, line 12) `def build(self)`
  - `connect_to_server` (method, line 27) `def connect_to_server(self, instance)`

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
  - `_read_json` (function, line 47) `def _read_json(path, default)`
  - `_read_jsonl` (function, line 64) `def _read_jsonl(path)`
  - `lazy_tasks` (function, line 88) `def lazy_tasks()`
  - `lazy_assets` (function, line 99) `def lazy_assets()`
  - `lazy_graph` (function, line 110) `def lazy_graph(task_id)`
  - `lazy_activity` (function, line 123) `def lazy_activity(task_id)`
  - `lazy_traffic` (function, line 135) `def lazy_traffic(task_id)`
  - `lazy_guard_audit` (function, line 147) `def lazy_guard_audit(task_id)`
  - `bridge_status` (function, line 159) `def bridge_status()`
  - `_extract_hosts_from_graph` (function, line 180) `def _extract_hosts_from_graph(graph)`
  - `pull_to_world_model` (function, line 206) `def pull_to_world_model()`
  - `pull_to_objectives` (function, line 251) `def pull_to_objectives()`
  - `pull_findings_to_lifecycle` (function, line 286) `def pull_findings_to_lifecycle()`
  - `_read_new_traffic` (function, line 314) `def _read_new_traffic(path, offset)`
  - `_notify` (function, line 351) `def _notify(progress, text)`
  - `pull_traffic_to_recorder` (function, line 361) `def pull_traffic_to_recorder(progress)`
  - `push_objective_to_lazy` (function, line 429) `def push_objective_to_lazy(goal, scope)`
  - `push_tasks_to_c2` (function, line 454) `def push_tasks_to_c2(only)`
  - `sync_all` (function, line 519) `def sync_all(progress)`
  - `_record_sync` (function, line 545) `def _record_sync(action, summary)`
- Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
- Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_lazy_loop.py`

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
  - `full_cli_enabled` (function, line 219) `def full_cli_enabled()`
  - `set_full_cli` (function, line 242) `def set_full_cli(enabled)`
- Depends on: `core/config.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`


Next: [KB_modules_p7.md](KB_modules_p7.md)
