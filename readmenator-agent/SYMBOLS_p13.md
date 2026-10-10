# Symbols (page 13 of 38)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_is_cve` | method | `modules/integrations/misp_export.py:158` | `def _is_cve(finding)` |
| `_is_domain` | method | `modules/integrations/misp_export.py:178` | `def _is_domain(finding)` |
| `_is_hash` | method | `modules/integrations/misp_export.py:206` | `def _is_hash(finding)` |
| `_is_ip` | method | `modules/integrations/misp_export.py:118` | `def _is_ip(finding)` |
| `_is_service` | method | `modules/integrations/misp_export.py:233` | `def _is_service(finding)` |
| `_load_events` | method | `modules/integrations/misp_export.py:383` | `def _load_events(self, sdir)` |
| `_load_findings` | method | `modules/integrations/misp_export.py:365` | `def _load_findings(self, sdir)` |
| `_load_policy_facts` | method | `modules/integrations/misp_export.py:372` | `def _load_policy_facts(self, sdir)` |
| `_main` | method | `modules/integrations/misp_export.py:482` | `def _main()` |
| `_map_finding` | method | `modules/integrations/misp_export.py:443` | `def _map_finding(self, finding)` |
| `export_session` | method | `modules/integrations/misp_export.py:268` | `def export_session(self, sessions_dir, target)` |
| `get_exporter` | method | `modules/integrations/misp_export.py:469` | `def get_exporter()` |
| `map` | method | `modules/integrations/misp_export.py:90` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:106` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:126` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:146` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:166` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:192` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:221` | `def map(self, finding)` |
| `push_to_misp` | method | `modules/integrations/misp_export.py:330` | `def push_to_misp(self, event, url, api_key)` |
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
| `_main` | method | `modules/integrations/nuclei_bridge.py:456` | `def _main()` |
| `_matches` | method | `modules/integrations/nuclei_bridge.py:258` | `def _matches(tmpl, service_lower, cve_upper)` |
| `_normalise_tags` | method | `modules/integrations/nuclei_bridge.py:238` | `def _normalise_tags(raw)` |
| `_parse_regex` | method | `modules/integrations/nuclei_bridge.py:201` | `def _parse_regex(self, text, path)` |
| `_parse_template` | method | `modules/integrations/nuclei_bridge.py:162` | `def _parse_template(self, path)` |
| `_parse_yaml` | method | `modules/integrations/nuclei_bridge.py:172` | `def _parse_yaml(self, text, path)` |
| `build` | method | `modules/integrations/nuclei_bridge.py:141` | `def build(self)` |
| `get_bridge` | method | `modules/integrations/nuclei_bridge.py:443` | `def get_bridge()` |
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
| `_main` | method | `modules/integrations/searchsploit.py:356` | `def _main()` |
| `_parse` | method | `modules/integrations/searchsploit.py:133` | `def _parse(self, raw)` |
| `_query` | method | `modules/integrations/searchsploit.py:218` | `def _query(self, cve_id)` |
| `_rate_limit` | method | `modules/integrations/searchsploit.py:258` | `def _rate_limit()` |
| `_row_to_entry` | method | `modules/integrations/searchsploit.py:162` | `def _row_to_entry(self, row)` |
| `_run` | method | `modules/integrations/searchsploit.py:118` | `def _run(self, query)` |
| `enrich_findings` | method | `modules/integrations/searchsploit.py:300` | `def enrich_findings(self, findings)` |
| `get_client` | method | `modules/integrations/searchsploit.py:333` | `def get_client()` |
| `search_cve` | method | `modules/integrations/searchsploit.py:80` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:109` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:207` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:286` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:341` | `def search_cve(cve_id)` |
| `search_service` | method | `modules/integrations/searchsploit.py:84` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:112` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:210` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:293` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:346` | `def search_service(name, version)` |
| `_enrich_readmenator_fields` | function | `modules/intel_fusion.py:428` | `def _enrich_readmenator_fields(nodes, edges)` |
| `_family_color` | function | `modules/intel_fusion.py:95` | `def _family_color(name)` |
| `_fibonacci_sphere` | function | `modules/intel_fusion.py:610` | `def _fibonacci_sphere(count)` |
| `_file_pagerank` | function | `modules/intel_fusion.py:146` | `def _file_pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_host_mentions` | function | `modules/intel_fusion.py:139` | `def _host_mentions(text)` |
| `_load_json` | function | `modules/intel_fusion.py:112` | `def _load_json(path, default)` |
| `_node_doc` | function | `modules/intel_fusion.py:390` | `def _node_doc(node)` |
| `_read_lines` | function | `modules/intel_fusion.py:122` | `def _read_lines(path, limit)` |
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
| `get_intelligence_engine` | method | `modules/intelligence_engine.py:931` | `def get_intelligence_engine(config)` |
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
| `builtin_rules` | method | `modules/intercept.py:101` | `def builtin_rules()` |
| `check` | method | `modules/intercept.py:270` | `def check(self, tool, command)` |
| `decide` | method | `modules/intercept.py:220` | `def decide(self, approval_id, decision)` |
| `evaluate` | method | `modules/intercept.py:192` | `def evaluate(self, tool, command)` |
| `interceptor` | method | `modules/intercept.py:266` | `def interceptor(self)` |
| `matches` | method | `modules/intercept.py:68` | `def matches(self, tool, command)` |
| `observe` | method | `modules/intercept.py:282` | `def observe(self, output, source)` |
| `observe_post_tool` | method | `modules/intercept.py:144` | `def observe_post_tool(output)` |
| `pending_approvals` | method | `modules/intercept.py:234` | `def pending_approvals(self)` |
| `record_failure` | method | `modules/intercept.py:291` | `def record_failure(self, source)` |
| `remove_rule` | method | `modules/intercept.py:183` | `def remove_rule(self, pattern)` |
| `rules` | method | `modules/intercept.py:172` | `def rules(self)` |
| `scope_blocked` | method | `modules/intercept.py:131` | `def scope_blocked(target)` |
| `display_usage` | function | `modules/iptables_portforward.sh:29` | `` |
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
| `priority` | method | `modules/kerberoasting.py:172` | `def priority(target)` |
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
| `get_killchain` | method | `modules/killchain.py:440` | `def get_killchain()` |
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
| `IBudget` | class | `modules/lazy_contracts.py:78` | `class IBudget(Protocol)` |
| `ICompactor` | class | `modules/lazy_contracts.py:70` | `class ICompactor(Protocol)` |
| `IEnricher` | class | `modules/lazy_contracts.py:54` | `class IEnricher(Protocol)` |
| `IFinding` | class | `modules/lazy_contracts.py:102` | `class IFinding(Protocol)` |
| `IFrontier` | class | `modules/lazy_contracts.py:14` | `class IFrontier(Protocol)` |
| `IGuard` | class | `modules/lazy_contracts.py:46` | `class IGuard(Protocol)` |
| `ILlmPool` | class | `modules/lazy_contracts.py:141` | `class ILlmPool(Protocol)` |
| `INotifier` | class | `modules/lazy_contracts.py:121` | `class INotifier(Protocol)` |
| `IPlanner` | class | `modules/lazy_contracts.py:30` | `class IPlanner(Protocol)` |
| `IRetester` | class | `modules/lazy_contracts.py:62` | `class IRetester(Protocol)` |
| `IRuntime` | class | `modules/lazy_contracts.py:90` | `class IRuntime(Protocol)` |
| `IToolCatalog` | class | `modules/lazy_contracts.py:149` | `class IToolCatalog(Protocol)` |
| `ITrigger` | class | `modules/lazy_contracts.py:129` | `class ITrigger(Protocol)` |
| `IWorker` | class | `modules/lazy_contracts.py:38` | `class IWorker(Protocol)` |
| `abort` | method | `modules/lazy_contracts.py:97` | `def abort(self, task_id, cause, detail)` |
| `add` | method | `modules/lazy_contracts.py:132` | `def add(self, kind, arg, every_sec)` |
| `bind` | method | `modules/lazy_contracts.py:156` | `def bind(self, agent, tool)` |
| `bindings` | method | `modules/lazy_contracts.py:152` | `def bindings(self, agent)` |
| `check` | method | `modules/lazy_contracts.py:49` | `def check(self, tool, command)` |
| `check` | method | `modules/lazy_contracts.py:81` | `def check(self, task_id)` |
| `claim_next` | method | `modules/lazy_contracts.py:21` | `def claim_next(self)` |
| `compact` | method | `modules/lazy_contracts.py:73` | `def compact(self, threshold)` |
| `complete` | method | `modules/lazy_contracts.py:144` | `def complete(self, prompt, max_tokens)` |
| `due` | method | `modules/lazy_contracts.py:136` | `def due(self, task_id, graph, activity)` |
| `emit` | method | `modules/lazy_contracts.py:124` | `def emit(self, task_id, event, data)` |
| `enrich` | method | `modules/lazy_contracts.py:57` | `def enrich(self, value)` |
| `execute` | method | `modules/lazy_contracts.py:41` | `def execute(self, intent, executor)` |
| `heartbeat` | method | `modules/lazy_contracts.py:93` | `def heartbeat(self, task_id)` |
| `pending` | method | `modules/lazy_contracts.py:17` | `def pending(self)` |
| `plan` | method | `modules/lazy_contracts.py:33` | `def plan(self, triggers)` |
| `ranked` | method | `modules/lazy_contracts.py:116` | `def ranked(self)` |
| `record_toolcall` | method | `modules/lazy_contracts.py:85` | `def record_toolcall(self, task_id, intent_id)` |
| `release` | method | `modules/lazy_contracts.py:25` | `def release(self, node_id, state)` |
| `report` | method | `modules/lazy_contracts.py:105` | `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` |
| `retest` | method | `modules/lazy_contracts.py:65` | `def retest(self, finding_id, executor)` |
| `set_status` | method | `modules/lazy_contracts.py:112` | `def set_status(self, finding_id, status)` |
| `LazyEngine` | class | `modules/lazy_engine.py:51` | `class LazyEngine(LazyLoopEngine)` |
| `ActivityLog` | class | `modules/lazy_loop.py:612` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:905` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:186` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:161` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:1006` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:2164` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:2774` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:2369` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:152` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:349` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:138` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:2303` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:580` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:765` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:1158` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:2996` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:175` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:2583` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:2432` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:1541` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:2090` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:1090` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:2744` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:2806` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:2910` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:2938` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:1266` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:2867` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:1224` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:2706` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:660` | `class TrafficLog` |
| `TriggerStore` | class | `modules/lazy_loop.py:2500` | `class TriggerStore` |
| `Worker` | class | `modules/lazy_loop.py:1775` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:189` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:352` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:583` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:615` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:663` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:768` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:914` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1009` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:1093` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:1161` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1227` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1269` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1544` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:1778` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store)` |
| `__init__` | method | `modules/lazy_loop.py:2093` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:2167` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:2306` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:2372` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2435` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2503` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2598` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:2709` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:2777` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:2870` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:2913` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3011` | `def __init__(self)` |
| `_asset_candidates` | method | `modules/lazy_loop.py:849` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:1945` | `def _auto_approve(self, command)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:3324` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:3362` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_candidates` | method | `modules/lazy_loop.py:1645` | `def _candidates(self)` |
| `_check_goals` | method | `modules/lazy_loop.py:3455` | `def _check_goals(self, task_id, graph, activity)` |
| `_constraints` | method | `modules/lazy_loop.py:1554` | `def _constraints(self)` |
| `_denied` | method | `modules/lazy_loop.py:1559` | `def _denied(self, text)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:3288` | `def _drain_triggers(self, task_id, graph)` |
| `_goals_met` | method | `modules/lazy_loop.py:3462` | `def _goals_met(self, task_id)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:1709` | `def _llm_candidates(self, existing)` |
| `_load` | method | `modules/lazy_loop.py:1167` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:2377` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:2508` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:2713` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:2781` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:2874` | `def _load(self)` |
| `_load_global` | method | `modules/lazy_loop.py:921` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:105` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:925` | `def _load_task(self)` |
| `_match_gate_rule` | method | `modules/lazy_loop.py:870` | `def _match_gate_rule(rule, target)` |
| `_now` | function | `modules/lazy_loop.py:94` | `def _now()` |
| `_origin_fact` | method | `modules/lazy_loop.py:1636` | `def _origin_fact(self)` |
| `_parts` | method | `modules/lazy_loop.py:3064` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:203` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:374` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:781` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1234` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1274` | `def _persist(self)` |
| `_record` | method | `modules/lazy_loop.py:2647` | `def _record(self, member, ok, text)` |
| `_run` | method | `modules/lazy_loop.py:1957` | `def _run(self, command, executor)` |
| `_run_one` | method | `modules/lazy_loop.py:3243` | `def _run_one(index_node)` |
| `_save` | method | `modules/lazy_loop.py:1171` | `def _save(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:933` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:115` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:937` | `def _save_task(self, payload)` |
| `_scope_allows` | method | `modules/lazy_loop.py:1766` | `def _scope_allows(self, asset)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:1790` | `def _scope_allows_target(self, target)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:2608` | `def _seed_defaults(self)` |
| `_slug` | function | `modules/lazy_loop.py:122` | `def _slug(value)` |
| `_stall_intent` | method | `modules/lazy_loop.py:1741` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:1968` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:99` | `def _store_path(name)` |
| `_target_for` | method | `modules/lazy_loop.py:1937` | `def _target_for(self, intent)` |
| `_traffic_template` | function | `modules/lazy_loop.py:127` | `def _traffic_template(command)` |
| `_writeback` | method | `modules/lazy_loop.py:2003` | `def _writeback(self, intent, transcripts)` |
| `abort` | method | `modules/lazy_loop.py:1130` | `def abort(self, task_id, cause, detail)` |
| `add` | method | `modules/lazy_loop.py:942` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:1238` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:2381` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:2512` | `def add(self, kind, arg, every_sec)` |
| `add` | method | `modules/lazy_loop.py:2785` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:2882` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:2447` | `def add_channel(self, kind, target, min_severity)` |
| `add_constraint` | method | `modules/lazy_loop.py:1347` | `def add_constraint(self, task_id, ctype, text)` |
| `add_edge` | method | `modules/lazy_loop.py:415` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:3096` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:3103` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:2624` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:383` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:785` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:1360` | `def add_scope(self, task_id, kind, value, reason)` |
| `anchor` | method | `modules/lazy_loop.py:428` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:443` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:439` | `def anchors_for(self, node_id)` |
| `archive` | method | `modules/lazy_loop.py:749` | `def archive(self, label)` |
| `as_list` | method | `modules/lazy_loop.py:1261` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:2749` | `def ask(self, task_id, question, pool)` |
| `audit` | method | `modules/lazy_loop.py:821` | `def audit(self, limit)` |
| `beat` | method | `modules/lazy_loop.py:1115` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:729` | `def bind(self, finding_id, digest, graph)` |
| `bind` | method | `modules/lazy_loop.py:2725` | `def bind(self, agent, tool)` |
| `bindings` | method | `modules/lazy_loop.py:2720` | `def bindings(self, agent)` |
| `by_template` | method | `modules/lazy_loop.py:723` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:2439` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:806` | `def check(self, tool, command)` |
| `check` | method | `modules/lazy_loop.py:1077` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:456` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:593` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:755` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:2987` | `def clear(self, task_id)` |
| `compact` | method | `modules/lazy_loop.py:2172` | `def compact(self, threshold, mode)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:499` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:1245` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:2654` | `def complete(self, prompt, max_tokens)` |
| `constraint_block` | method | `modules/lazy_loop.py:2266` | `def constraint_block(constraints)` |
| `coverage` | method | `modules/lazy_loop.py:254` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:275` | `def coverage_for(self, graph, scope)` |
| `create` | method | `modules/lazy_loop.py:1278` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:3069` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:1191` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | method | `modules/lazy_loop.py:1488` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:207` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:1322` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:3151` | `def delete_goal(self, task_id, goal_id)` |
| `digest_overview` | method | `modules/lazy_loop.py:2242` | `def digest_overview(self)` |
| `due` | method | `modules/lazy_loop.py:2539` | `def due(self, task_id, graph, activity)` |

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
