# Subsystem: modules (page 5 of 10)
Previous: [KB_modules_p4.md](KB_modules_p4.md)

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
  - `encrypt_data` (function, line 17) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 32) `def decrypt_data(data, key)`
  - `check_sudo` (function, line 55) `def check_sudo()`
  - `checksum` (function, line 61) `def checksum(source_string)`
  - `send_icmp_packet` (function, line 78) `def send_icmp_packet(dest_addr, data, key)`
  - `receive_icmp_reply` (function, line 112) `def receive_icmp_reply(sock)`
  - `main` (function, line 124) `def main()`

## modules/icmp_server.py
- Doc: encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 32) `def check_sudo()`
  - `encrypt_data` (function, line 40) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 56) `def decrypt_data(data, key)`
  - `execute_command` (function, line 77) `def execute_command(command)`
  - `send_icmp_reply` (function, line 95) `def send_icmp_reply(sock, addr, data, key)`
  - `checksum` (function, line 114) `def checksum(source_string)`
  - `handle_packet` (function, line 131) `def handle_packet(packet, addr, key, sock)`
  - `listen_for_icmp` (function, line 155) `def listen_for_icmp(interface, key)`
  - `main` (function, line 181) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`
- Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`

## modules/img2bin.py
- Layer: utility
- Language: py
- Symbols:
  - `imagen_a_binario` (function, line 7) `def imagen_a_binario(imagen_input, binario_output, block_size)`
  - `main` (function, line 42) `def main()`

## modules/intelligence_engine.py
- Doc: IntelligenceEngine — unified collection→analysis→intelligence pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `IntelligenceConfig` (class, line 57) `class IntelligenceConfig`
  - `CollectedFact` (class, line 76) `class CollectedFact`
  - `IntelligenceAssessment` (class, line 91) `class IntelligenceAssessment`
  - `CounterIntelFinding` (class, line 106) `class CounterIntelFinding`
  - `IntelligenceEngine` (class, line 117) `class IntelligenceEngine`
  - `get_intelligence_engine` (method, line 870) `def get_intelligence_engine(config)`
  - `__init__` (method, line 140) `def __init__(self, config)`
  - `collect_from_scan` (method, line 151) `def collect_from_scan(self, target)`
  - `collect_from_tool` (method, line 229) `def collect_from_tool(self, output, tool, host)`
  - `collect_from_estorides` (method, line 266) `def collect_from_estorides(self, target)`
  - `collect_from_nuclei` (method, line 303) `def collect_from_nuclei(self, target)`
  - `collect_from_yara` (method, line 343) `def collect_from_yara(self, target_path)`
  - `collect_from_factstore` (method, line 380) `def collect_from_factstore(self)`
  - `analyze` (method, line 428) `def analyze(self)`
  - `_correlate_services_to_vulns` (method, line 445) `def _correlate_services_to_vulns(self)`
  - `_match_known_vulns` (method, line 487) `def _match_known_vulns(fact)`
  - `_correlate_creds_to_hosts` (method, line 515) `def _correlate_creds_to_hosts(self)`
  - `_correlate_domains_to_infrastructure` (method, line 536) `def _correlate_domains_to_infrastructure(self)`
  - `_rank_targets` (method, line 550) `def _rank_targets(self)`
  - `_detect_killchain_gaps` (method, line 588) `def _detect_killchain_gaps(self)`
  - `produce_intelligence` (method, line 628) `def produce_intelligence(self)`
  - `_map_category_to_mitre` (method, line 647) `def _map_category_to_mitre(category)`
  - `produce_counter_intelligence` (method, line 662) `def produce_counter_intelligence(self)`
  - `disseminate` (method, line 706) `def disseminate(self)`
  - `run_full_cycle` (method, line 789) `def run_full_cycle(self, target)`
  - `get_intel_report` (method, line 818) `def get_intel_report(self)`
  - `_is_placeholder` (method, line 864) `def _is_placeholder(value)`
- Depends on: `core/logging.py`, `modules/estorides_importer.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
- Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`

## modules/internal_discover.sh
- Layer: utility
- Language: sh

## modules/iptables_portforward.sh
- Layer: utility
- Language: sh
- Symbols:
  - `display_usage` (function, line 29)

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
  - `helm_tiller_abuse` (method, line 251) `def helm_tiller_abuse(self)`
  - `persistence_techniques` (method, line 279) `def persistence_techniques(self)`
  - `summary` (method, line 319) `def summary(self)`
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
  - `_prioritize_targets` (method, line 161) `def _prioritize_targets(self)`
  - `request_tgs_aes_only` (method, line 179) `def request_tgs_aes_only(self, user_spn)`
  - `request_tgs_rc4` (method, line 200) `def request_tgs_rc4(self, user_spn)`
  - `request_tgs` (method, line 211) `def request_tgs(self, user_spn, etype)`
  - `_build_hash_string` (method, line 240) `def _build_hash_string(self, spn, etype)`
  - `_hashcat_command` (method, line 266) `def _hashcat_command(hash_str, mode)`
  - `targeted_kerberoast` (method, line 272) `def targeted_kerberoast(self, high_value_only)`
  - `asreproast_check` (method, line 307) `def asreproast_check(self, usernames)`
  - `extract_hashes_from_pcap` (method, line 322) `def extract_hashes_from_pcap(self, pcap_path)`
  - `detect_kerberoasting_activity` (method, line 337) `def detect_kerberoasting_activity(self, event_log)`
  - `build_hashcat_batch` (method, line 376) `def build_hashcat_batch(self, output_path)`
  - `summary` (method, line 398) `def summary(self)`
  - `priority` (method, line 164) `def priority(target)`
- Depends on: `modules/kerberos_core.py`
- Imported by: `cli/commands/active_directory.py`

## modules/kerberos_core.py
- Doc: Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.
- Layer: utility
- Language: py
- Symbols:
  - `KerberosPrincipal` (class, line 137) `class KerberosPrincipal`
  - `EncryptedData` (class, line 155) `class EncryptedData`
  - `KerberosTicket` (class, line 170) `class KerberosTicket`
  - `PACSignature` (class, line 211) `class PACSignature`
  - `PACInfo` (class, line 226) `class PACInfo`
  - `TGSRequest` (class, line 247) `class TGSRequest`
  - `KerberosCrypto` (class, line 269) `class KerberosCrypto`
  - `KerberosCore` (class, line 405) `class KerberosCore`
  - `KerberosErrorParser` (class, line 681) `class KerberosErrorParser`
  - `TicketValidator` (class, line 700) `class TicketValidator`
  - `to_string` (method, line 150) `def to_string(self)`
  - `has_flag` (method, line 205) `def has_flag(self, flag_name)`
  - `__init__` (method, line 275) `def __init__(self)`
  - `derive_aes_key` (method, line 280) `def derive_aes_key(password, salt, etype)`
  - `derive_rc4_key` (method, line 316) `def derive_rc4_key(password)`
  - `aes_encrypt` (method, line 327) `def aes_encrypt(self, key, plaintext, usage)`
  - `aes_decrypt` (method, line 359) `def aes_decrypt(self, key, ciphertext, usage)`
  - `compute_checksum` (method, line 387) `def compute_checksum(key, data, etype)`
  - `__init__` (method, line 419) `def __init__(self, domain, dc_host, dc_ip)`
  - `get_supported_etypes` (method, line 425) `def get_supported_etypes(self)`
  - `build_as_req` (method, line 433) `def build_as_req(self, username, domain, password, etype)`
  - `build_tgs_req` (method, line 487) `def build_tgs_req(self, params)`
  - `parse_as_rep` (method, line 532) `def parse_as_rep(self, as_rep_data, key, etype)`
  - `parse_tgs_rep` (method, line 548) `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)`
  - `decrypt_ticket` (method, line 561) `def decrypt_ticket(self, ticket_data, key, etype)`
  - `parse_pac` (method, line 586) `def parse_pac(self, pac_data)`
  - `_parse_pac_buffer` (method, line 620) `def _parse_pac_buffer(pac, buf_type, buf_data)`
  - `_build_pa_enc_timestamp` (method, line 638) `def _build_pa_enc_timestamp(self, key, etype, timestamp)`
  - `_parse_kdc_rep` (method, line 651) `def _parse_kdc_rep(self, data, key, etype, rep_type)`
  - `_rc4_encrypt` (method, line 665) `def _rc4_encrypt(key, data, usage)`
  - `_rc4_decrypt` (method, line 674) `def _rc4_decrypt(key, data, usage)`
  - `parse_error` (method, line 685) `def parse_error(error_data)`
  - `is_expired` (method, line 704) `def is_expired(endtime, grace_period)`
  - `validate_flags` (method, line 717) `def validate_flags(ticket, required_flags)`
  - `validate_pac_checksums` (method, line 733) `def validate_pac_checksums(pac)`
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
  - `SkeletonKeyInjector` (class, line 565) `class SkeletonKeyInjector`
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
  - `detect_skeleton_key` (method, line 576) `def detect_skeleton_key(target_host, domain, dc_ip)`
  - `inject_command` (method, line 598) `def inject_command(target_host)`
  - `cleanup_command` (method, line 610) `def cleanup_command()`
- Depends on: `modules/kerberos_core.py`
- Imported by: `cli/commands/active_directory.py`

## modules/kill_chain_viz.py
- Doc: SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG.
- Layer: utility
- Language: py
- Symbols:
  - `_load_phases` (function, line 21) `def _load_phases(sessions)`
  - `_read_target` (function, line 31) `def _read_target()`
  - `_build_svg` (function, line 38) `def _build_svg(phases)`
  - `generate_html` (function, line 67) `def generate_html(target, sessions)`
  - `generate_svg` (function, line 98) `def generate_svg(target, sessions)`
- Depends on: `modules/killchain.py`
- Imported by: `lazyc2.py`

## modules/killchain.py
- Doc: Unified kill-chain — single source of truth consumed by all surfaces.
- Layer: utility
- Language: py
- Symbols:
  - `KillChainConfig` (class, line 39) `class KillChainConfig`
  - `PhaseStatus` (class, line 127) `class PhaseStatus`
  - `KillChain` (class, line 136) `class KillChain`
  - `get_killchain` (method, line 427) `def get_killchain()`
  - `world_model_path` (method, line 107) `def world_model_path(self)`
  - `phase_index` (method, line 111) `def phase_index(self, phase)`
  - `is_valid_phase` (method, line 118) `def is_valid_phase(self, phase)`
  - `config` (method, line 145) `def config()`
  - `phases` (method, line 150) `def phases()`
  - `phase_labels` (method, line 155) `def phase_labels()`
  - `phase_colors` (method, line 160) `def phase_colors()`
  - `phase_rich_colors` (method, line 165) `def phase_rich_colors()`
  - `engagement_phase_to_cli` (method, line 170) `def engagement_phase_to_cli(engagement_value)`
  - `cli_phase_to_host_state` (method, line 182) `def cli_phase_to_host_state(phase)`
  - `current_phase` (method, line 195) `def current_phase(world_model_path)`
  - `advance_phase` (method, line 242) `def advance_phase(new_phase, world_model_path)`
  - `get_progress` (method, line 305) `def get_progress(world_model_path)`
  - `compact_progress` (method, line 348) `def compact_progress(current_phase, phases_entered)`
  - `phases_for_display` (method, line 368) `def phases_for_display()`
  - `phase_index` (method, line 379) `def phase_index(phase)`
  - `snapshot` (method, line 384) `def snapshot(world_model_path)`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `scripts/devtools/core_smoke.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`

## modules/kivi.py
- Layer: utility
- Language: py
- Symbols:
  - `ReverseShellApp` (class, line 11) `class ReverseShellApp(App)`
  - `build` (method, line 12) `def build(self)`
  - `connect_to_server` (method, line 27) `def connect_to_server(self, instance)`

## modules/lazy_rbac.py
- Doc: modules/lazy_rbac.py
- Layer: presentation
- Language: py
- Symbols:
  - `Role` (class, line 55) `class Role(Enum)`
  - `Permission` (class, line 66) `class Permission(Enum)`
  - `_UsersFileUnreadable` (class, line 115) `class _UsersFileUnreadable(Exception)`
  - `RBACUser` (class, line 124) `class RBACUser`
  - `RBACStore` (class, line 211) `class RBACStore`
  - `_generate_recovery_codes` (method, line 358) `def _generate_recovery_codes(count)`
  - `TenantConfig` (class, line 373) `class TenantConfig`
  - `TenantManager` (class, line 399) `class TenantManager`
  - `_slugify` (method, line 519) `def _slugify(name)`
  - `init_rbac_store` (method, line 527) `def init_rbac_store(users_path)`
  - `init_tenant_manager` (method, line 531) `def init_tenant_manager(payloads_dir, config_path, default_payload)`
  - `require_role` (method, line 543) `def require_role()`
  - `require_permission` (method, line 569) `def require_permission()`
  - `require_mfa` (method, line 600) `def require_mfa(f)`
  - `_get_rbac_user` (method, line 623) `def _get_rbac_user(flask_user)`
  - `_get_rbac_store` (method, line 636) `def _get_rbac_store()`
  - `get_rbac_store` (method, line 643) `def get_rbac_store()`
  - `set_rbac_store` (method, line 647) `def set_rbac_store(store)`
  - `get_tenant_manager` (method, line 652) `def get_tenant_manager()`
  - `set_tenant_manager` (method, line 659) `def set_tenant_manager(tm)`
  - `check_cli_permission` (method, line 664) `def check_cli_permission(username, permission)`
  - `get_user_role` (method, line 676) `def get_user_role(username)`
  - `generate_mfa_qr_url` (method, line 684) `def generate_mfa_qr_url(secret, username)`
  - `generate_qr_svg` (method, line 693) `def generate_qr_svg(data)`
  - `_qr_choose_version` (method, line 745) `def _qr_choose_version(data)`
  - `_qr_ec_codewords` (method, line 753) `def _qr_ec_codewords(version)`
  - `_qr_encode_alphanumeric` (method, line 758) `def _qr_encode_alphanumeric(data, version)`
  - `_qr_data_bits_for_version` (method, line 813) `def _qr_data_bits_for_version(version)`
  - `_qr_blank_matrix` (method, line 824) `def _qr_blank_matrix(version)`
  - `_qr_place_dark_module` (method, line 833) `def _qr_place_dark_module(matrix, size, version)`
  - `_qr_add_format_info` (method, line 837) `def _qr_add_format_info(modules, size, ecl_bits, mask)`
  - `_qr_svg_error` (method, line 861) `def _qr_svg_error(msg)`
  - `_qr_place_finders` (method, line 870) `def _qr_place_finders(matrix, size)`
  - `_qr_place_timing` (method, line 880) `def _qr_place_timing(matrix, size)`
  - `_qr_data_bits_positions` (method, line 886) `def _qr_data_bits_positions(matrix, size)`
  - `_bits_to_bytes` (method, line 905) `def _bits_to_bytes(bits, data_bits)`
  - `_reed_solomon_encode` (method, line 916) `def _reed_solomon_encode(data, ec_words)`
  - `_qr_best_mask` (method, line 952) `def _qr_best_mask(modules, size)`
  - `_qr_apply_mask` (method, line 965) `def _qr_apply_mask(modules, size, mask)`
  - `_qr_penalty` (method, line 998) `def _qr_penalty(modules, size)`
  - `_qr_render_svg` (method, line 1060) `def _qr_render_svg(modules, size, modules_per_pixel)`
  - `valid_roles` (method, line 62) `def valid_roles(cls)`
  - `to_dict` (method, line 135) `def to_dict(self)`
  - `from_dict` (method, line 139) `def from_dict(cls, data)`
  - `get_role` (method, line 163) `def get_role(self)`
  - `has_permission` (method, line 169) `def has_permission(self, permission)`
  - `can_manage_role` (method, line 173) `def can_manage_role(self, target_role)`
  - `get_mfa_provisioning_uri` (method, line 181) `def get_mfa_provisioning_uri(self)`
  - `verify_totp` (method, line 188) `def verify_totp(self, token)`
  - `verify_recovery_code` (method, line 193) `def verify_recovery_code(self, code)`
  - `consume_recovery_code` (method, line 201) `def consume_recovery_code(self, code)`
  - `__init__` (method, line 214) `def __init__(self, users_path)`
  - `_read_users` (method, line 218) `def _read_users(self)`
  - `_write_users` (method, line 234) `def _write_users(self, users)`
  - `load_all` (method, line 247) `def load_all(self)`
  - `find_by_id` (method, line 251) `def find_by_id(self, user_id)`
  - `find_by_username` (method, line 257) `def find_by_username(self, username)`
  - `save` (method, line 263) `def save(self, user)`
  - `create_user` (method, line 276) `def create_user(self, username, password_hash, role, tenant_id)`
  - `delete_user` (method, line 297) `def delete_user(self, user_id)`
  - `update_role` (method, line 306) `def update_role(self, user_id, new_role)`
  - `enable_mfa` (method, line 316) `def enable_mfa(self, user_id)`
  - `disable_mfa` (method, line 326) `def disable_mfa(self, user_id)`
  - `consume_recovery_code` (method, line 336) `def consume_recovery_code(self, user_id, code)`
  - `ensure_admin` (method, line 345) `def ensure_admin(self, username, password_hash)`
  - `from_payload` (method, line 382) `def from_payload(cls, tenant_id, name, payload_path)`
  - `to_dict` (method, line 391) `def to_dict(self)`
  - `from_dict` (method, line 395) `def from_dict(cls, data)`
  - `__init__` (method, line 402) `def __init__(self, payloads_dir, config_path, default_payload)`
  - `_load_config` (method, line 415) `def _load_config(self)`
  - `_save_config` (method, line 426) `def _save_config(self)`
  - `list_tenants` (method, line 436) `def list_tenants(self)`
  - `get_active` (method, line 439) `def get_active(self)`
  - `get_active_payload_path` (method, line 444) `def get_active_payload_path(self)`
  - `get_active_sessions_dir` (method, line 450) `def get_active_sessions_dir(self)`
  - `get_payload_for_tenant` (method, line 456) `def get_payload_for_tenant(self, tenant_id)`
  - `create_tenant` (method, line 462) `def create_tenant(self, name, base_payload)`
  - `switch_tenant` (method, line 491) `def switch_tenant(self, tenant_id)`
  - `delete_tenant` (method, line 500) `def delete_tenant(self, tenant_id)`
  - `ensure_default_tenant` (method, line 509) `def ensure_default_tenant(self)`
  - `decorator` (method, line 546) `def decorator(f)`
  - `decorator` (method, line 572) `def decorator(f)`
  - `decorated` (method, line 604) `def decorated()`
  - `gf_mul` (method, line 929) `def gf_mul(a, b)`
  - `decorated` (method, line 548) `def decorated()`
  - `decorated` (method, line 574) `def decorated()`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`

## modules/lazyatack.sh
- Doc: Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `mostrar_ayuda` (function, line 21)
  - `validar_ip` (function, line 33)
  - `validar_url` (function, line 49)
  - `descargar_seclists` (function, line 107)
  - `escanear_puertos` (function, line 115)
  - `escanear_puertos_especificos` (function, line 121)
  - `enumerar_http` (function, line 127)
  - `iniciar_servidor_http` (function, line 133)
  - `configurar_netcat` (function, line 139)
  - `enviar_archivo_netcat` (function, line 145)
  - `verificar_conectividad` (function, line 151)
  - `verificar_curl` (function, line 158)
  - `configurar_shell_reversa` (function, line 165)
  - `escuchar_shell` (function, line 171)
  - `monitorear_procesos` (function, line 177)
  - `ejecutar_wfuzz` (function, line 188)
  - `comprobar_sudo` (function, line 194)
  - `explotar_lfi` (function, line 200)
  - `configurar_tty` (function, line 206)
  - `eliminar_archivos` (function, line 217)
  - `obtener_root_shell` (function, line 223)
  - `enumerar_suid` (function, line 230)
  - `listar_timers` (function, line 236)
  - `comprobar_rutas` (function, line 242)
  - `abusar_tar` (function, line 248)
  - `enumerar_puertos` (function, line 254)
  - `eliminar_contenedores_docker` (function, line 260)
  - `escanear_red` (function, line 266)
  - `menu_servidor` (function, line 272)
  - `menu_cliente` (function, line 307)

## modules/lazybrutesshuserenum.sh
- Doc: Función para manejar el interruptor de señal Ctrl+C
- Layer: utility
- Language: sh

## modules/lazyclonewars.sh
- Doc: Lista de repositorios (nombre y URL)
- Layer: utility
- Language: sh

## modules/lazycloud.py
- Doc: Cloud-native attack module for AWS, Azure, and GCP.
- Layer: utility
- Language: py
- Symbols:
  - `CloudResource` (class, line 59) `class CloudResource`
  - `CloudFinding` (class, line 70) `class CloudFinding`
  - `CloudMetadataHarvester` (class, line 80) `class CloudMetadataHarvester`
  - `CloudBucketEnumerator` (class, line 216) `class CloudBucketEnumerator`
  - `CloudIAMEnumerator` (class, line 315) `class CloudIAMEnumerator`
  - `CloudScanner` (class, line 359) `class CloudScanner`
  - `__init__` (method, line 83) `def __init__(self, timeout)`
  - `session` (method, line 88) `def session(self)`
  - `_get` (method, line 94) `def _get(self, url, headers)`
  - `harvest_aws` (method, line 110) `def harvest_aws(self)`
  - `harvest_azure` (method, line 155) `def harvest_azure(self)`
  - `harvest_gcp` (method, line 176) `def harvest_gcp(self)`
  - `harvest_all` (method, line 199) `def harvest_all(self)`
  - `__init__` (method, line 219) `def __init__(self, timeout)`
  - `session` (method, line 224) `def session(self)`
  - `_check_url` (method, line 230) `def _check_url(self, url)`
  - `enumerate_s3` (method, line 245) `def enumerate_s3(self, prefix, buckets)`
  - `enumerate_azure_storage` (method, line 272) `def enumerate_azure_storage(self, prefix, accounts)`
  - `enumerate_gcp_storage` (method, line 292) `def enumerate_gcp_storage(self, prefix, buckets)`
  - `enumerate_aws_iam` (method, line 318) `def enumerate_aws_iam(self, access_key, secret_key, session_token)`
  - `__init__` (method, line 362) `def __init__(self, target_domain, timeout)`
  - `full_scan` (method, line 369) `def full_scan(self, target_prefix, sessions_dir)`
  - `quick_metadata` (method, line 425) `def quick_metadata(self)`
  - `quick_buckets` (method, line 429) `def quick_buckets(self, prefix)`
  - `_aws_sig` (method, line 332) `def _aws_sig(key, msg)`
  - `_sign` (method, line 335) `def _sign(key, msg)`
- Imported by: `cli/commands/cloud.py`

## modules/lazycurl.sh
- Doc: Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `ctrl_c` (function, line 23)
  - `show_help` (function, line 29)
  - `execute_curl` (function, line 52)

## modules/lazyencoder_decoder.py
- Layer: utility
- Language: py
- Symbols:
  - `base64_encode` (function, line 4) `def base64_encode(data)`
  - `base64_decode` (function, line 8) `def base64_decode(data)`
  - `caesar_cipher` (function, line 13) `def caesar_cipher(text, shift)`
  - `caesar_decipher` (function, line 27) `def caesar_decipher(text, shift)`
  - `key_substitution` (function, line 31) `def key_substitution(text, key)`
  - `key_substitution_reverse` (function, line 47) `def key_substitution_reverse(text, key)`
  - `encode` (function, line 63) `def encode(data, shift, key)`
  - `encode_string` (function, line 75) `def encode_string(data, shift, key)`
  - `decode` (function, line 82) `def decode(data, shift, key)`
  - `decode_string` (function, line 94) `def decode_string(data, shift, key)`
- Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`

## modules/lazyevilwimrm.sh
- Doc: execute_evil_winrm: Función para ejecutar evil-winrm y verificar la salida
- Layer: utility
- Language: sh
- Symbols:
  - `execute_evil_winrm` (function, line 14)

## modules/lazygat.sh
- Doc: Nombre del script: lazygath.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh


Next: [KB_modules_p6.md](KB_modules_p6.md)
