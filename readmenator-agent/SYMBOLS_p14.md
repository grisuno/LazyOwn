# Symbols (page 14 of 41)
Previous: [SYMBOLS_p13.md](SYMBOLS_p13.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_split_caps` | function | `modules/intel_fusion.py:626` | `def _split_caps(labels, sizes, points, lattice, out)` |
| `_symbol_list` | function | `modules/intel_fusion.py:413` | `def _symbol_list(node)` |
| `_unit` | function | `modules/intel_fusion.py:651` | `def _unit(vec)` |
| `add_edge` | function | `modules/intel_fusion.py:197` | `def add_edge(src, dst, kind, evidence, weight)` |
| `add_node` | function | `modules/intel_fusion.py:183` | `def add_node(kind, value, label)` |
| `assign_layout` | function | `modules/intel_fusion.py:800` | `def assign_layout(graph, mode)` |
| `build_analytics` | function | `modules/intel_fusion.py:585` | `def build_analytics(graph, summary)` |
| `build_bundle_payload` | function | `modules/intel_fusion.py:659` | `def build_bundle_payload(graph)` |
| `build_intel_graph` | function | `modules/intel_fusion.py:176` | `def build_intel_graph(sessions_dir, est_cap)` |
| `bundle_settings` | function | `modules/intel_fusion.py:769` | `def bundle_settings(graph)` |
| `group_colors` | function | `modules/intel_fusion.py:512` | `def group_colors(graph)` |
| `node_id` | function | `modules/intel_fusion.py:106` | `def node_id(kind, value)` |
| `page_settings` | function | `modules/intel_fusion.py:528` | `def page_settings(graph)` |
| `tag_source` | function | `modules/intel_fusion.py:205` | `def tag_source(nid, source)` |
| `write_summary` | function | `modules/intel_fusion.py:865` | `def write_summary(graph, sessions_dir)` |
| `CollectedFact` | class | `modules/intelligence_engine.py:78` | `class CollectedFact` |
| `CounterIntelFinding` | class | `modules/intelligence_engine.py:108` | `class CounterIntelFinding` |
| `IntelligenceAssessment` | class | `modules/intelligence_engine.py:93` | `class IntelligenceAssessment` |
| `IntelligenceConfig` | class | `modules/intelligence_engine.py:57` | `class IntelligenceConfig` |
| `IntelligenceEngine` | class | `modules/intelligence_engine.py:119` | `class IntelligenceEngine` |
| `__init__` | method | `modules/intelligence_engine.py:142` | `def __init__(self, config)` |
| `_correlate_creds_to_hosts` | method | `modules/intelligence_engine.py:565` | `def _correlate_creds_to_hosts(self)` |
| `_correlate_domains_to_infrastructure` | method | `modules/intelligence_engine.py:588` | `def _correlate_domains_to_infrastructure(self)` |
| `_correlate_services_to_vulns` | method | `modules/intelligence_engine.py:494` | `def _correlate_services_to_vulns(self)` |
| `_detect_killchain_gaps` | method | `modules/intelligence_engine.py:644` | `def _detect_killchain_gaps(self)` |
| `_is_placeholder` | method | `modules/intelligence_engine.py:925` | `def _is_placeholder(value)` |
| `_map_category_to_mitre` | method | `modules/intelligence_engine.py:700` | `def _map_category_to_mitre(category)` |
| `_match_known_vulns` | method | `modules/intelligence_engine.py:537` | `def _match_known_vulns(fact)` |
| `_rank_targets` | method | `modules/intelligence_engine.py:604` | `def _rank_targets(self)` |
| `analyze` | method | `modules/intelligence_engine.py:477` | `def analyze(self)` |
| `collect_from_estorides` | method | `modules/intelligence_engine.py:292` | `def collect_from_estorides(self, target)` |
| `collect_from_factstore` | method | `modules/intelligence_engine.py:415` | `def collect_from_factstore(self)` |
| `collect_from_nuclei` | method | `modules/intelligence_engine.py:334` | `def collect_from_nuclei(self, target)` |
| `collect_from_scan` | method | `modules/intelligence_engine.py:153` | `def collect_from_scan(self, target)` |
| `collect_from_tool` | method | `modules/intelligence_engine.py:255` | `def collect_from_tool(self, output, tool, host)` |
| `collect_from_yara` | method | `modules/intelligence_engine.py:376` | `def collect_from_yara(self, target_path)` |
| `disseminate` | method | `modules/intelligence_engine.py:765` | `def disseminate(self)` |
| `get_intel_report` | method | `modules/intelligence_engine.py:874` | `def get_intel_report(self)` |
| `get_intelligence_engine` | function | `modules/intelligence_engine.py:931` | `def get_intelligence_engine(config)` |
| `produce_counter_intelligence` | method | `modules/intelligence_engine.py:715` | `def produce_counter_intelligence(self)` |
| `produce_intelligence` | method | `modules/intelligence_engine.py:685` | `def produce_intelligence(self)` |
| `run_full_cycle` | method | `modules/intelligence_engine.py:845` | `def run_full_cycle(self, target)` |
| `Guard` | class | `modules/intercept.py:255` | `class Guard` |
| `InterceptAction` | class | `modules/intercept.py:21` | `class InterceptAction(str, Enum)` |
| `InterceptConfig` | class | `modules/intercept.py:33` | `class InterceptConfig` |
| `InterceptRule` | class | `modules/intercept.py:50` | `class InterceptRule` |
| `InterceptVerdict` | class | `modules/intercept.py:92` | `class InterceptVerdict` |
| `Interceptor` | class | `modules/intercept.py:154` | `class Interceptor` |
| `PendingApproval` | class | `modules/intercept.py:77` | `class PendingApproval` |
| `__init__` | method | `modules/intercept.py:157` | `def __init__(self, rules, ask_timeout_sec, timeout_action)` |
| `__init__` | method | `modules/intercept.py:258` | `def __init__(self, interceptor)` |
| `__post_init__` | method | `modules/intercept.py:61` | `def __post_init__(self)` |
| `add_rule` | method | `modules/intercept.py:177` | `def add_rule(self, rule)` |
| `approval_status` | method | `modules/intercept.py:249` | `def approval_status(self, approval_id)` |
| `attribution` | method | `modules/intercept.py:301` | `def attribution(self)` |
| `audit_log` | method | `modules/intercept.py:296` | `def audit_log(self, limit)` |
| `builtin_rules` | function | `modules/intercept.py:101` | `def builtin_rules()` |
| `check` | method | `modules/intercept.py:270` | `def check(self, tool, command)` |
| `decide` | method | `modules/intercept.py:220` | `def decide(self, approval_id, decision)` |
| `evaluate` | method | `modules/intercept.py:192` | `def evaluate(self, tool, command)` |
| `interceptor` | method | `modules/intercept.py:266` | `def interceptor(self)` |
| `matches` | method | `modules/intercept.py:68` | `def matches(self, tool, command)` |
| `observe` | method | `modules/intercept.py:282` | `def observe(self, output, source)` |
| `observe_post_tool` | function | `modules/intercept.py:144` | `def observe_post_tool(output)` |
| `pending_approvals` | method | `modules/intercept.py:234` | `def pending_approvals(self)` |
| `record_failure` | method | `modules/intercept.py:291` | `def record_failure(self, source)` |
| `remove_rule` | method | `modules/intercept.py:183` | `def remove_rule(self, pattern)` |
| `rules` | method | `modules/intercept.py:172` | `def rules(self)` |
| `scope_blocked` | function | `modules/intercept.py:131` | `def scope_blocked(target)` |
| `display_usage` | function | `modules/iptables_portforward.sh:29` | `` |
| `JsonlTail` | class | `modules/jsonl_tail.py:14` | `class JsonlTail` |
| `__init__` | method | `modules/jsonl_tail.py:17` | `def __init__(self, path)` |
| `read_new` | method | `modules/jsonl_tail.py:22` | `def read_new(self, limit)` |
| `K8SAttackEngine` | class | `modules/k8s_attacks.py:77` | `class K8SAttackEngine` |
| `K8sConfig` | class | `modules/k8s_attacks.py:57` | `class K8sConfig` |
| `__init__` | method | `modules/k8s_attacks.py:87` | `def __init__(self, config)` |
| `enumerate_rbac` | method | `modules/k8s_attacks.py:90` | `def enumerate_rbac(self)` |
| `etcd_access_exploitation` | method | `modules/k8s_attacks.py:222` | `def etcd_access_exploitation(self)` |
| `helm_tiller_abuse` | method | `modules/k8s_attacks.py:250` | `def helm_tiller_abuse(self)` |
| `kubelet_anonymous_auth_abuse` | method | `modules/k8s_attacks.py:198` | `def kubelet_anonymous_auth_abuse(self)` |
| `persistence_techniques` | method | `modules/k8s_attacks.py:278` | `def persistence_techniques(self)` |
| `privileged_pod_escape` | method | `modules/k8s_attacks.py:118` | `def privileged_pod_escape(self)` |
| `service_account_token_theft` | method | `modules/k8s_attacks.py:173` | `def service_account_token_theft(self)` |
| `summary` | method | `modules/k8s_attacks.py:318` | `def summary(self)` |
| `KerberoastHash` | class | `modules/kerberoasting.py:59` | `class KerberoastHash` |
| `KerberoastTarget` | class | `modules/kerberoasting.py:38` | `class KerberoastTarget` |
| `KerberoastingEngine` | class | `modules/kerberoasting.py:79` | `class KerberoastingEngine` |
| `__init__` | method | `modules/kerberoasting.py:95` | `def __init__(self, domain, dc_ip, username, password, hash)` |
| `_build_hash_string` | method | `modules/kerberoasting.py:248` | `def _build_hash_string(self, spn, etype)` |
| `_hashcat_command` | method | `modules/kerberoasting.py:268` | `def _hashcat_command(hash_str, mode)` |
| `_prioritize_targets` | method | `modules/kerberoasting.py:169` | `def _prioritize_targets(self)` |
| `asreproast_check` | method | `modules/kerberoasting.py:306` | `def asreproast_check(self, usernames)` |
| `build_hashcat_batch` | method | `modules/kerberoasting.py:379` | `def build_hashcat_batch(self, output_path)` |
| `detect_kerberoasting_activity` | method | `modules/kerberoasting.py:336` | `def detect_kerberoasting_activity(self, event_log)` |
| `enumerate_spns` | method | `modules/kerberoasting.py:112` | `def enumerate_spns(self, ldap_output, bloodhound_data)` |
| `extract_hashes_from_pcap` | method | `modules/kerberoasting.py:321` | `def extract_hashes_from_pcap(self, pcap_path)` |
| `priority` | function | `modules/kerberoasting.py:172` | `def priority(target)` |
| `request_tgs` | method | `modules/kerberoasting.py:219` | `def request_tgs(self, user_spn, etype)` |
| `request_tgs_aes_only` | method | `modules/kerberoasting.py:187` | `def request_tgs_aes_only(self, user_spn)` |
| `request_tgs_rc4` | method | `modules/kerberoasting.py:208` | `def request_tgs_rc4(self, user_spn)` |
| `summary` | method | `modules/kerberoasting.py:401` | `def summary(self)` |
| `targeted_kerberoast` | method | `modules/kerberoasting.py:271` | `def targeted_kerberoast(self, high_value_only)` |
| `EncryptedData` | class | `modules/kerberos_core.py:157` | `class EncryptedData` |
| `KerberosCore` | class | `modules/kerberos_core.py:407` | `class KerberosCore` |
| `KerberosCrypto` | class | `modules/kerberos_core.py:271` | `class KerberosCrypto` |
| `KerberosErrorParser` | class | `modules/kerberos_core.py:683` | `class KerberosErrorParser` |
| `KerberosPrincipal` | class | `modules/kerberos_core.py:139` | `class KerberosPrincipal` |
| `KerberosTicket` | class | `modules/kerberos_core.py:172` | `class KerberosTicket` |
| `PACInfo` | class | `modules/kerberos_core.py:228` | `class PACInfo` |
| `PACSignature` | class | `modules/kerberos_core.py:213` | `class PACSignature` |
| `TGSRequest` | class | `modules/kerberos_core.py:249` | `class TGSRequest` |
| `TicketValidator` | class | `modules/kerberos_core.py:702` | `class TicketValidator` |
| `__init__` | method | `modules/kerberos_core.py:277` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_core.py:421` | `def __init__(self, domain, dc_host, dc_ip)` |
| `_build_pa_enc_timestamp` | method | `modules/kerberos_core.py:640` | `def _build_pa_enc_timestamp(self, key, etype, timestamp)` |
| `_parse_kdc_rep` | method | `modules/kerberos_core.py:653` | `def _parse_kdc_rep(self, data, key, etype, rep_type)` |
| `_parse_pac_buffer` | method | `modules/kerberos_core.py:622` | `def _parse_pac_buffer(pac, buf_type, buf_data)` |
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
| `KillChain` | class | `modules/killchain.py:145` | `class KillChain` |
| `KillChainConfig` | class | `modules/killchain.py:38` | `class KillChainConfig` |
| `PhaseStatus` | class | `modules/killchain.py:136` | `class PhaseStatus` |
| `advance_phase` | method | `modules/killchain.py:251` | `def advance_phase(new_phase, world_model_path)` |
| `cli_phase_to_host_state` | method | `modules/killchain.py:191` | `def cli_phase_to_host_state(phase)` |
| `compact_progress` | method | `modules/killchain.py:364` | `def compact_progress(current_phase, phases_entered)` |
| `config` | method | `modules/killchain.py:154` | `def config()` |
| `current_phase` | method | `modules/killchain.py:204` | `def current_phase(world_model_path)` |
| `engagement_phase_to_cli` | method | `modules/killchain.py:179` | `def engagement_phase_to_cli(engagement_value)` |
| `get_killchain` | function | `modules/killchain.py:440` | `def get_killchain()` |
| `get_progress` | method | `modules/killchain.py:315` | `def get_progress(world_model_path)` |
| `is_valid_phase` | method | `modules/killchain.py:127` | `def is_valid_phase(self, phase)` |
| `phase_colors` | method | `modules/killchain.py:169` | `def phase_colors()` |
| `phase_index` | method | `modules/killchain.py:120` | `def phase_index(self, phase)` |
| `phase_index` | method | `modules/killchain.py:395` | `def phase_index(phase)` |
| `phase_labels` | method | `modules/killchain.py:164` | `def phase_labels()` |
| `phase_rich_colors` | method | `modules/killchain.py:174` | `def phase_rich_colors()` |
| `phases` | method | `modules/killchain.py:159` | `def phases()` |
| `phases_for_display` | method | `modules/killchain.py:384` | `def phases_for_display()` |
| `snapshot` | method | `modules/killchain.py:400` | `def snapshot(world_model_path)` |
| `world_model_path` | method | `modules/killchain.py:116` | `def world_model_path(self)` |
| `ReverseShellApp` | class | `modules/kivi.py:11` | `class ReverseShellApp(App)` |
| `build` | method | `modules/kivi.py:12` | `def build(self)` |
| `connect_to_server` | method | `modules/kivi.py:27` | `def connect_to_server(self, instance)` |
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
| `_data_dir` | function | `modules/lazy_bridge.py:35` | `def _data_dir()` |
| `_extract_hosts_from_graph` | function | `modules/lazy_bridge.py:180` | `def _extract_hosts_from_graph(graph)` |
| `_read_json` | function | `modules/lazy_bridge.py:47` | `def _read_json(path, default)` |
| `_read_jsonl` | function | `modules/lazy_bridge.py:64` | `def _read_jsonl(path)` |
| `_record_sync` | function | `modules/lazy_bridge.py:449` | `def _record_sync(action, summary)` |
| `bridge_status` | function | `modules/lazy_bridge.py:159` | `def bridge_status()` |
| `lazy_activity` | function | `modules/lazy_bridge.py:123` | `def lazy_activity(task_id)` |
| `lazy_assets` | function | `modules/lazy_bridge.py:99` | `def lazy_assets()` |
| `lazy_graph` | function | `modules/lazy_bridge.py:110` | `def lazy_graph(task_id)` |
| `lazy_guard_audit` | function | `modules/lazy_bridge.py:147` | `def lazy_guard_audit(task_id)` |
| `lazy_tasks` | function | `modules/lazy_bridge.py:88` | `def lazy_tasks()` |
| `lazy_traffic` | function | `modules/lazy_bridge.py:135` | `def lazy_traffic(task_id)` |
| `pull_findings_to_lifecycle` | function | `modules/lazy_bridge.py:286` | `def pull_findings_to_lifecycle()` |
| `pull_to_objectives` | function | `modules/lazy_bridge.py:251` | `def pull_to_objectives()` |
| `pull_to_world_model` | function | `modules/lazy_bridge.py:206` | `def pull_to_world_model()` |
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:314` | `def pull_traffic_to_recorder()` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:344` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:369` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:434` | `def sync_all()` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:219` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:242` | `def set_full_cli(enabled)` |
| `LazyEngine` | class | `modules/lazy_engine.py:55` | `class LazyEngine(LazyLoopEngine)` |
| `install_command_for` | function | `modules/lazy_installer.py:70` | `def install_command_for(tool)` |
| `installer_enabled` | function | `modules/lazy_installer.py:41` | `def installer_enabled()` |
| `intent_for` | function | `modules/lazy_installer.py:75` | `def intent_for(tool)` |
| `set_installer_enabled` | function | `modules/lazy_installer.py:58` | `def set_installer_enabled(enabled)` |
| `steps_for_install` | function | `modules/lazy_installer.py:88` | `def steps_for_install(text)` |
| `tool_from_intent` | function | `modules/lazy_installer.py:80` | `def tool_from_intent(text)` |
| `_append` | function | `modules/lazy_intel.py:70` | `def _append(record)` |
| `_is_ip_literal` | function | `modules/lazy_intel.py:274` | `def _is_ip_literal(value)` |
| `_log_path` | function | `modules/lazy_intel.py:35` | `def _log_path()` |
| `_mask` | function | `modules/lazy_intel.py:41` | `def _mask(text)` |
| `_now` | function | `modules/lazy_intel.py:30` | `def _now()` |
| `describe_command` | function | `modules/lazy_intel.py:105` | `def describe_command(command)` |
| `export_spans` | function | `modules/lazy_intel.py:324` | `def export_spans(task_id, out)` |
| `fuse_routing_decisions` | function | `modules/lazy_intel.py:285` | `def fuse_routing_decisions(task_id)` |
| `infer_source` | function | `modules/lazy_intel.py:79` | `def infer_source(command, intent_text)` |
| `mask_configured` | function | `modules/lazy_intel.py:228` | `def mask_configured(text)` |
| `read_decisions` | function | `modules/lazy_intel.py:202` | `def read_decisions(task_id, limit)` |
| `record_routing_decision` | function | `modules/lazy_intel.py:120` | `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | function | `modules/lazy_intel.py:160` | `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` |
| `stack_signature` | function | `modules/lazy_intel.py:254` | `def stack_signature(assets)` |
| `ActivityLog` | class | `modules/lazy_loop.py:1327` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2059` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:856` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:831` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2153` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:5166` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7093` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:6137` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:822` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1019` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:808` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:5887` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1299` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1718` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2305` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:7417` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:845` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:6555` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:6240` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:2938` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5073` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2237` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7019` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7123` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:7285` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:7312` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2507` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:7242` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2465` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:6975` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1460` | `class TrafficLog` |
| `TriggerStore` | class | `modules/lazy_loop.py:6406` | `class TriggerStore` |
| `Worker` | class | `modules/lazy_loop.py:3378` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:859` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1022` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1302` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1330` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1463` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1721` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2068` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2156` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2240` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2334` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2468` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2510` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:2941` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3381` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5076` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:5174` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:5890` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:6140` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6243` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:6409` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6572` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:6978` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7096` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7245` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7288` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7442` | `def __init__(self, shell)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:3967` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:3993` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:4337` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:4156` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:4369` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:5309` | `def _apply_stored_bodies(self, bodies)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2003` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:4478` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:4836` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:8487` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:8523` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:5377` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:5191` | `def _bodies_path(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:9543` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3130` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:395` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:8882` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:4129` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:5179` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:4827` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:2952` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:5369` | `def _content_versions(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:449` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3280` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4685` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:2961` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:4467` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:5965` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:5961` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:3982` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:8438` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2329` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:491` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:411` | `def _encrypt_channel_secret(plaintext)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:8578` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2312` | `def _event_for(cls, path, item_id)` |
| `_find` | function | `modules/lazy_loop.py:5398` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:9439` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:3712` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:5337` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:8889` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:5386` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:3785` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_host_from_token` | function | `modules/lazy_loop.py:253` | `def _host_from_token(token)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:7955` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:242` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:5333` | `def _is_live_intent(self, node)` |
| `_kill` | function | `modules/lazy_loop.py:332` | `def _kill()` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3294` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:699` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:707` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:4567` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2340` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6145` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6414` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6982` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7100` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7249` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:5195` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:5183` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2075` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:659` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2079` | `def _load_task(self)` |
| `_mask_key` | function | `modules/lazy_loop.py:372` | `def _mask_key(match)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:5863` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2024` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:9162` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:9136` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:9182` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:4490` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:5252` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:599` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1655` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:641` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:4058` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3121` | `def _origin_fact(self)` |
| `_parts` | method | `modules/lazy_loop.py:7522` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:873` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1044` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1740` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2475` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2515` | `def _persist(self)` |
| `_prior_steps` | method | `modules/lazy_loop.py:3490` | `def _prior_steps(self, intent)` |
| `_reader` | function | `modules/lazy_loop.py:4080` | `def _reader()` |
| `_record` | method | `modules/lazy_loop.py:6648` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:6723` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:6943` | `def _record_raw(self, member, prompt, reply, ok)` |
| `_refresh` | method | `modules/lazy_loop.py:2603` | `def _refresh(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:310` | `def _register_loop_executor(executor)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:6683` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:6020` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:5203` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:4709` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:387` | `def _restrict_file(path)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:6654` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:4506` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:8293` | `def _run_one(index_node)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:4773` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2344` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:5199` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:5187` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2086` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:669` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2090` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:3461` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:1936` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:1926` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:6583` | `def _seed_defaults(self)` |
| `_send_email` | method | `modules/lazy_loop.py:6315` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:4093` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:4649` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3062` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:684` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:7970` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:8754` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3352` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:4026` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:4888` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:646` | `def _store_path(name)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:4723` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:236` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:9000` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:8145` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:1986` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:3777` | `def _target_for(self, intent)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:4750` | `def _task_executed_commands(self)` |
| `_traffic_template` | function | `modules/lazy_loop.py:689` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:5404` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:316` | `def _unregister_loop_executor(executor)` |
| `_wake_event` | function | `modules/lazy_loop.py:481` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:4556` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:4038` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:5999` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:5224` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:8543` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:6036` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:4948` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2277` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2572` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2095` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2479` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:6149` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:6418` | `def add(self, kind, arg, every_sec)` |
| `add` | method | `modules/lazy_loop.py:7104` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:7257` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:6255` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2706` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1099` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:7740` | `def add_hint(self, task_id, text)` |

Next: [SYMBOLS_p15.md](SYMBOLS_p15.md)
