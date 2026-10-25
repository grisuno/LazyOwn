# Symbols (page 15 of 45)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `save` | method | `modules/integrations/misp_export.py:322` | `def save(self, event, path)` |
| `to_json` | method | `modules/integrations/misp_export.py:299` | `def to_json(self, event)` |
| `LocalTemplateIndex` | class | `modules/integrations/nuclei_bridge.py:104` | `class LocalTemplateIndex(TemplateSelector)` |
| `NucleiBridge` | class | `modules/integrations/nuclei_bridge.py:389` | `class NucleiBridge` |
| `NucleiRunner` | class | `modules/integrations/nuclei_bridge.py:279` | `class NucleiRunner` |
| `NucleiTemplate` | class | `modules/integrations/nuclei_bridge.py:71` | `class NucleiTemplate` |
| `TemplateSelector` | class | `modules/integrations/nuclei_bridge.py:87` | `class TemplateSelector(ABC)` |
| `_F` | class | `modules/integrations/nuclei_bridge.py:483` | `class _F` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:114` | `def __init__(self, templates_dir)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:288` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:396` | `def __init__(self, selector, runner)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:484` | `def __init__(self, ftype, value)` |
| `_build_command` | method | `modules/integrations/nuclei_bridge.py:343` | `def _build_command(self, target, templates, output_dir)` |
| `_ensure_built` | method | `modules/integrations/nuclei_bridge.py:158` | `def _ensure_built(self)` |
| `_extract_context` | method | `modules/integrations/nuclei_bridge.py:370` | `def _extract_context(findings)` |
| `_extract_cve_from_tags` | method | `modules/integrations/nuclei_bridge.py:246` | `def _extract_cve_from_tags(tags)` |
| `_extract_cve_from_text` | method | `modules/integrations/nuclei_bridge.py:253` | `def _extract_cve_from_text(text)` |
| `_main` | function | `modules/integrations/nuclei_bridge.py:456` | `def _main()` |
| `_matches` | method | `modules/integrations/nuclei_bridge.py:258` | `def _matches(tmpl, service_lower, cve_upper)` |
| `_normalise_tags` | method | `modules/integrations/nuclei_bridge.py:238` | `def _normalise_tags(raw)` |
| `_parse_regex` | method | `modules/integrations/nuclei_bridge.py:201` | `def _parse_regex(self, text, path)` |
| `_parse_template` | method | `modules/integrations/nuclei_bridge.py:162` | `def _parse_template(self, path)` |
| `_parse_yaml` | method | `modules/integrations/nuclei_bridge.py:172` | `def _parse_yaml(self, text, path)` |
| `build` | method | `modules/integrations/nuclei_bridge.py:141` | `def build(self)` |
| `get_bridge` | function | `modules/integrations/nuclei_bridge.py:443` | `def get_bridge()` |
| `list_templates` | method | `modules/integrations/nuclei_bridge.py:427` | `def list_templates(self, services, cves)` |
| `run` | method | `modules/integrations/nuclei_bridge.py:293` | `def run(self, target, templates, output_dir)` |
| `run_for_findings` | method | `modules/integrations/nuclei_bridge.py:326` | `def run_for_findings(self, target, findings, output_dir, selector)` |
| `scan` | method | `modules/integrations/nuclei_bridge.py:404` | `def scan(self, target, findings, dry_run)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:91` | `def select(self, services, cves)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:121` | `def select(self, services, cves)` |
| `NucleiFinding` | class | `modules/integrations/nuclei_parser.py:71` | `class NucleiFinding` |
| `NucleiParser` | class | `modules/integrations/nuclei_parser.py:99` | `class NucleiParser` |
| `__init__` | method | `modules/integrations/nuclei_parser.py:109` | `def __init__(self, sessions_dir)` |
| `_finding_to_dict` | method | `modules/integrations/nuclei_parser.py:504` | `def _finding_to_dict(finding)` |
| `_parse_json_obj` | method | `modules/integrations/nuclei_parser.py:412` | `def _parse_json_obj(self, obj)` |
| `_parse_line` | method | `modules/integrations/nuclei_parser.py:393` | `def _parse_line(self, line)` |
| `_recommend_for_finding` | method | `modules/integrations/nuclei_parser.py:468` | `def _recommend_for_finding(self, finding, rhost)` |
| `_summarize` | method | `modules/integrations/nuclei_parser.py:517` | `def _summarize(findings)` |
| `enrich_world_model` | method | `modules/integrations/nuclei_parser.py:262` | `def enrich_world_model(self, findings, rhost)` |
| `exploit_probability` | method | `modules/integrations/nuclei_parser.py:95` | `def exploit_probability(self)` |
| `generate_recommendations` | method | `modules/integrations/nuclei_parser.py:300` | `def generate_recommendations(self, findings, rhost)` |
| `import_to_db` | method | `modules/integrations/nuclei_parser.py:196` | `def import_to_db(self, findings, rhost, workspace_name)` |
| `mitre_tactic` | method | `modules/integrations/nuclei_parser.py:87` | `def mitre_tactic(self)` |
| `parse_file` | method | `modules/integrations/nuclei_parser.py:177` | `def parse_file(self, filepath)` |
| `parse_json` | method | `modules/integrations/nuclei_parser.py:134` | `def parse_json(self, json_text)` |
| `parse_text` | method | `modules/integrations/nuclei_parser.py:115` | `def parse_text(self, text)` |
| `scan_and_import` | method | `modules/integrations/nuclei_parser.py:328` | `def scan_and_import(self, target, templates, services, cves, workspace_name)` |
| `ExploitDBAPI` | class | `modules/integrations/searchsploit.py:193` | `class ExploitDBAPI(ExploitSource)` |
| `ExploitEntry` | class | `modules/integrations/searchsploit.py:60` | `class ExploitEntry` |
| `ExploitSource` | class | `modules/integrations/searchsploit.py:76` | `class ExploitSource(ABC)` |
| `SearchsploitCLI` | class | `modules/integrations/searchsploit.py:93` | `class SearchsploitCLI(ExploitSource)` |
| `SearchsploitClient` | class | `modules/integrations/searchsploit.py:271` | `class SearchsploitClient` |
| `__init__` | method | `modules/integrations/searchsploit.py:102` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:201` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:278` | `def __init__(self, primary, fallback)` |
| `_extract_cve` | method | `modules/integrations/searchsploit.py:183` | `def _extract_cve(text)` |
| `_main` | function | `modules/integrations/searchsploit.py:356` | `def _main()` |
| `_parse` | method | `modules/integrations/searchsploit.py:133` | `def _parse(self, raw)` |
| `_query` | method | `modules/integrations/searchsploit.py:218` | `def _query(self, cve_id)` |
| `_rate_limit` | method | `modules/integrations/searchsploit.py:258` | `def _rate_limit()` |
| `_row_to_entry` | method | `modules/integrations/searchsploit.py:162` | `def _row_to_entry(self, row)` |
| `_run` | method | `modules/integrations/searchsploit.py:118` | `def _run(self, query)` |
| `enrich_findings` | method | `modules/integrations/searchsploit.py:300` | `def enrich_findings(self, findings)` |
| `get_client` | function | `modules/integrations/searchsploit.py:333` | `def get_client()` |
| `search_cve` | method | `modules/integrations/searchsploit.py:80` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:109` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:207` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:286` | `def search_cve(self, cve_id)` |
| `search_cve` | function | `modules/integrations/searchsploit.py:341` | `def search_cve(cve_id)` |
| `search_service` | method | `modules/integrations/searchsploit.py:84` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:112` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:210` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:293` | `def search_service(self, name, version)` |
| `search_service` | function | `modules/integrations/searchsploit.py:346` | `def search_service(name, version)` |
| `_enrich_readmenator_fields` | function | `modules/intel_fusion.py:456` | `def _enrich_readmenator_fields(nodes, edges)` |
| `_family_color` | function | `modules/intel_fusion.py:95` | `def _family_color(name)` |
| `_fibonacci_sphere` | function | `modules/intel_fusion.py:684` | `def _fibonacci_sphere(count)` |
| `_file_pagerank` | function | `modules/intel_fusion.py:146` | `def _file_pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_host_mentions` | function | `modules/intel_fusion.py:139` | `def _host_mentions(text)` |
| `_load_json` | function | `modules/intel_fusion.py:112` | `def _load_json(path, default)` |
| `_node_doc` | function | `modules/intel_fusion.py:418` | `def _node_doc(node)` |
| `_read_lines` | function | `modules/intel_fusion.py:122` | `def _read_lines(path, limit)` |
| `_split_caps` | function | `modules/intel_fusion.py:700` | `def _split_caps(labels, sizes, points, lattice, out)` |
| `_symbol_list` | function | `modules/intel_fusion.py:441` | `def _symbol_list(node)` |
| `_unit` | function | `modules/intel_fusion.py:729` | `def _unit(vec)` |
| `add_edge` | function | `modules/intel_fusion.py:200` | `def add_edge(src, dst, kind, evidence, weight)` |
| `add_node` | function | `modules/intel_fusion.py:182` | `def add_node(kind, value, label)` |
| `assign_layout` | function | `modules/intel_fusion.py:884` | `def assign_layout(graph, mode)` |
| `build_analytics` | function | `modules/intel_fusion.py:650` | `def build_analytics(graph, summary)` |
| `build_bundle_payload` | function | `modules/intel_fusion.py:737` | `def build_bundle_payload(graph)` |
| `build_intel_graph` | function | `modules/intel_fusion.py:176` | `def build_intel_graph(sessions_dir, est_cap)` |
| `bundle_settings` | function | `modules/intel_fusion.py:853` | `def bundle_settings(graph)` |
| `group_colors` | function | `modules/intel_fusion.py:577` | `def group_colors(graph)` |
| `node_id` | function | `modules/intel_fusion.py:106` | `def node_id(kind, value)` |
| `page_settings` | function | `modules/intel_fusion.py:593` | `def page_settings(graph)` |
| `tag_source` | function | `modules/intel_fusion.py:214` | `def tag_source(nid, source)` |
| `write_summary` | function | `modules/intel_fusion.py:949` | `def write_summary(graph, sessions_dir)` |
| `CollectedFact` | class | `modules/intelligence_engine.py:78` | `class CollectedFact` |
| `CounterIntelFinding` | class | `modules/intelligence_engine.py:108` | `class CounterIntelFinding` |
| `IntelligenceAssessment` | class | `modules/intelligence_engine.py:93` | `class IntelligenceAssessment` |
| `IntelligenceConfig` | class | `modules/intelligence_engine.py:57` | `class IntelligenceConfig` |
| `IntelligenceEngine` | class | `modules/intelligence_engine.py:119` | `class IntelligenceEngine` |
| `__init__` | method | `modules/intelligence_engine.py:142` | `def __init__(self, config)` |
| `_correlate_creds_to_hosts` | method | `modules/intelligence_engine.py:604` | `def _correlate_creds_to_hosts(self)` |
| `_correlate_domains_to_infrastructure` | method | `modules/intelligence_engine.py:627` | `def _correlate_domains_to_infrastructure(self)` |
| `_correlate_services_to_vulns` | method | `modules/intelligence_engine.py:533` | `def _correlate_services_to_vulns(self)` |
| `_detect_killchain_gaps` | method | `modules/intelligence_engine.py:683` | `def _detect_killchain_gaps(self)` |
| `_is_placeholder` | method | `modules/intelligence_engine.py:964` | `def _is_placeholder(value)` |
| `_map_category_to_mitre` | method | `modules/intelligence_engine.py:739` | `def _map_category_to_mitre(category)` |
| `_match_known_vulns` | method | `modules/intelligence_engine.py:576` | `def _match_known_vulns(fact)` |
| `_rank_targets` | method | `modules/intelligence_engine.py:643` | `def _rank_targets(self)` |
| `analyze` | method | `modules/intelligence_engine.py:516` | `def analyze(self)` |
| `collect_from_estorides` | method | `modules/intelligence_engine.py:292` | `def collect_from_estorides(self, target)` |
| `collect_from_factstore` | method | `modules/intelligence_engine.py:415` | `def collect_from_factstore(self)` |
| `collect_from_nuclei` | method | `modules/intelligence_engine.py:334` | `def collect_from_nuclei(self, target)` |
| `collect_from_scan` | method | `modules/intelligence_engine.py:153` | `def collect_from_scan(self, target)` |
| `collect_from_tool` | method | `modules/intelligence_engine.py:255` | `def collect_from_tool(self, output, tool, host)` |
| `collect_from_yara` | method | `modules/intelligence_engine.py:376` | `def collect_from_yara(self, target_path)` |
| `disseminate` | method | `modules/intelligence_engine.py:804` | `def disseminate(self)` |
| `get_intel_report` | method | `modules/intelligence_engine.py:913` | `def get_intel_report(self)` |
| `get_intelligence_engine` | function | `modules/intelligence_engine.py:970` | `def get_intelligence_engine(config)` |
| `produce_counter_intelligence` | method | `modules/intelligence_engine.py:754` | `def produce_counter_intelligence(self)` |
| `produce_intelligence` | method | `modules/intelligence_engine.py:724` | `def produce_intelligence(self)` |
| `run_full_cycle` | method | `modules/intelligence_engine.py:884` | `def run_full_cycle(self, target)` |
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
| `KillChain` | class | `modules/killchain.py:147` | `class KillChain` |
| `KillChainConfig` | class | `modules/killchain.py:40` | `class KillChainConfig` |
| `PhaseStatus` | class | `modules/killchain.py:138` | `class PhaseStatus` |
| `advance_phase` | method | `modules/killchain.py:253` | `def advance_phase(new_phase, world_model_path, host, extras)` |
| `cli_phase_to_host_state` | method | `modules/killchain.py:193` | `def cli_phase_to_host_state(phase)` |
| `compact_progress` | method | `modules/killchain.py:406` | `def compact_progress(current_phase, phases_entered)` |
| `config` | method | `modules/killchain.py:156` | `def config()` |
| `current_phase` | method | `modules/killchain.py:206` | `def current_phase(world_model_path)` |
| `engagement_phase_to_cli` | method | `modules/killchain.py:181` | `def engagement_phase_to_cli(engagement_value)` |
| `get_killchain` | function | `modules/killchain.py:482` | `def get_killchain()` |
| `get_progress` | method | `modules/killchain.py:357` | `def get_progress(world_model_path)` |
| `is_valid_phase` | method | `modules/killchain.py:129` | `def is_valid_phase(self, phase)` |
| `phase_colors` | method | `modules/killchain.py:171` | `def phase_colors()` |
| `phase_index` | method | `modules/killchain.py:122` | `def phase_index(self, phase)` |
| `phase_index` | method | `modules/killchain.py:437` | `def phase_index(phase)` |
| `phase_labels` | method | `modules/killchain.py:166` | `def phase_labels()` |
| `phase_rich_colors` | method | `modules/killchain.py:176` | `def phase_rich_colors()` |
| `phases` | method | `modules/killchain.py:161` | `def phases()` |
| `phases_for_display` | method | `modules/killchain.py:426` | `def phases_for_display()` |
| `snapshot` | method | `modules/killchain.py:442` | `def snapshot(world_model_path)` |
| `world_model_path` | method | `modules/killchain.py:118` | `def world_model_path(self)` |
| `ReverseShellApp` | class | `modules/kivi.py:11` | `class ReverseShellApp(App)` |
| `build` | method | `modules/kivi.py:12` | `def build(self)` |
| `connect_to_server` | method | `modules/kivi.py:27` | `def connect_to_server(self, instance)` |
| `_docker` | function | `modules/lab_runtime.py:95` | `def _docker()` |
| `_docker_compose` | function | `modules/lab_runtime.py:349` | `def _docker_compose(args)` |
| `apply_gym_migrations` | function | `modules/lab_runtime.py:185` | `def apply_gym_migrations(name)` |
| `container_ip` | function | `modules/lab_runtime.py:157` | `def container_ip(container_name)` |
| `container_name` | function | `modules/lab_runtime.py:152` | `def container_name(scenario)` |
| `docker_available` | function | `modules/lab_runtime.py:81` | `def docker_available()` |
| `ensure_range_secret` | function | `modules/lab_runtime.py:357` | `def ensure_range_secret(profile_dir)` |
| `ensure_web` | function | `modules/lab_runtime.py:171` | `def ensure_web(scenario, name)` |
| `existing_containers` | function | `modules/lab_runtime.py:119` | `def existing_containers()` |
| `range_compose` | function | `modules/lab_runtime.py:277` | `def range_compose(profile)` |
| `running_containers` | function | `modules/lab_runtime.py:103` | `def running_containers()` |
| `running_range_containers` | function | `modules/lab_runtime.py:136` | `def running_range_containers()` |
| `start` | function | `modules/lab_runtime.py:193` | `def start(scenario)` |
| `start_range` | function | `modules/lab_runtime.py:286` | `def start_range(profile)` |
| `stop` | function | `modules/lab_runtime.py:241` | `def stop(scenario)` |
| `stop_all` | function | `modules/lab_runtime.py:259` | `def stop_all()` |
| `stop_range` | function | `modules/lab_runtime.py:305` | `def stop_range(profile)` |
| `stop_ranges` | function | `modules/lab_runtime.py:316` | `def stop_ranges()` |
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
| `_notify` | function | `modules/lazy_bridge.py:351` | `def _notify(progress, text)` |
| `_read_json` | function | `modules/lazy_bridge.py:47` | `def _read_json(path, default)` |
| `_read_jsonl` | function | `modules/lazy_bridge.py:64` | `def _read_jsonl(path)` |
| `_read_new_traffic` | function | `modules/lazy_bridge.py:314` | `def _read_new_traffic(path, offset)` |
| `_record_sync` | function | `modules/lazy_bridge.py:545` | `def _record_sync(action, summary)` |
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
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:361` | `def pull_traffic_to_recorder(progress)` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:429` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:454` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:519` | `def sync_all(progress)` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `catalog_cli_for_phase` | function | `modules/lazy_cli_bridge.py:219` | `def catalog_cli_for_phase(limit)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:253` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:276` | `def set_full_cli(enabled)` |
| `LazyEngine` | class | `modules/lazy_engine.py:55` | `class LazyEngine(LazyLoopEngine)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:1430` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2162` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:959` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:934` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2256` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:5431` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7261` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:6438` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:925` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1122` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:911` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6160` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1402` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1821` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2408` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:7585` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:948` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:6710` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:6541` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3041` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5332` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2340` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7187` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7291` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:7453` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:7480` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2610` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:7410` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2568` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:7143` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1563` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:3499` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:962` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1125` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1405` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1433` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1566` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1824` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2171` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2259` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2343` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2437` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2571` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2613` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3044` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3502` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5335` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:5439` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6163` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:6441` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6544` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:6727` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7146` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7264` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7413` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7456` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7610` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:3986` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4220` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:4246` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:4591` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:4409` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:4623` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:5574` | `def _apply_stored_bodies(self, bodies)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2106` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:4732` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5069` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:8801` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:8837` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:5642` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:5456` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:6809` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:9938` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3233` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:498` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:9258` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:4382` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:5444` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:5060` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3055` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:5634` | `def _content_versions(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:552` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3392` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4959` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3064` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:4721` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:6266` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:6262` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:4235` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:8752` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2432` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:594` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:514` | `def _encrypt_channel_secret(plaintext)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:8892` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2415` | `def _event_for(cls, path, item_id)` |
| `_fact_memory_store` | method | `modules/lazy_loop.py:3964` | `def _fact_memory_store(self)` |
| `_find` | function | `modules/lazy_loop.py:5663` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:9834` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:3888` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:5602` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:9265` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:5651` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:4038` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_host_from_token` | function | `modules/lazy_loop.py:356` | `def _host_from_token(token)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
