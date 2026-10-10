# API (page 11 of 20)
Previous: [API_p10.md](API_p10.md)

## modules/icmp_client.py
- `encrypt_data` (function) `modules/icmp_client.py:18` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_client.py:34` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `check_sudo` (function) `modules/icmp_client.py:57` `def check_sudo()`
- `checksum` (function) `modules/icmp_client.py:64` `def checksum(source_string)`
- `send_icmp_packet` (function) `modules/icmp_client.py:82` `def send_icmp_packet(dest_addr, data, key)`
- `receive_icmp_reply` (function) `modules/icmp_client.py:117` `def receive_icmp_reply(sock)`
- `main` (function) `modules/icmp_client.py:130` `def main()`

## modules/icmp_server.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `check_sudo` (function) `modules/icmp_server.py:44` `def check_sudo()`
- `encrypt_data` (function) `modules/icmp_server.py:55` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_server.py:71` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `execute_command` (function) `modules/icmp_server.py:93` `def execute_command(command)`
- `send_icmp_reply` (function) `modules/icmp_server.py:112` `def send_icmp_reply(sock, addr, data, key)`
- `checksum` (function) `modules/icmp_server.py:132` `def checksum(source_string)`
- `handle_packet` (function) `modules/icmp_server.py:150` `def handle_packet(packet, addr, key, sock)`
- `listen_for_icmp` (function) `modules/icmp_server.py:175` `def listen_for_icmp(interface, key)`
- `main` (function) `modules/icmp_server.py:202` `def main()`

## modules/img2bin.py
- `imagen_a_binario` (function) `modules/img2bin.py:7` `def imagen_a_binario(imagen_input, binario_output, block_size)`
- `main` (function) `modules/img2bin.py:43` `def main()`

## modules/integrations/misp_export.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `FindingMapper.map` (method) `modules/integrations/misp_export.py:90` `def map(self, finding)` -- Convert *finding* to a MISPAttribute.
- `IPMapper.map` (method) `modules/integrations/misp_export.py:106` `def map(self, finding)`
- `CredentialMapper.map` (method) `modules/integrations/misp_export.py:126` `def map(self, finding)`
- `CVEMapper.map` (method) `modules/integrations/misp_export.py:146` `def map(self, finding)`
- `DomainMapper.map` (method) `modules/integrations/misp_export.py:166` `def map(self, finding)`
- `HashMapper.map` (method) `modules/integrations/misp_export.py:192` `def map(self, finding)`
- `ServiceMapper.map` (method) `modules/integrations/misp_export.py:221` `def map(self, finding)`
- `MISPExporter.__init__` (method) `modules/integrations/misp_export.py:263` `def __init__(self, mappers)`
- `MISPExporter.export_session` (method) `modules/integrations/misp_export.py:268` `def export_session(self, sessions_dir, target)` -- Read policy_facts.json and events.jsonl from *sessions_dir*, map all findings, and return a populated MISPEvent.
- `MISPExporter.to_json` (method) `modules/integrations/misp_export.py:299` `def to_json(self, event)` -- Serialise *event* to a MISP-compatible JSON string.
- `MISPExporter.save` (method) `modules/integrations/misp_export.py:322` `def save(self, event, path)` -- Write the MISP event JSON to *path* and return the resolved path.
- `MISPExporter.push_to_misp` (method) `modules/integrations/misp_export.py:330` `def push_to_misp(self, event, url, api_key)` -- HTTP-push the event to a live MISP instance.
- `_DictFinding.__init__` (method) `modules/integrations/misp_export.py:454` `def __init__(self, data)`
- `_DictFinding.get_exporter` (method) `modules/integrations/misp_export.py:469` `def get_exporter()` -- Return the module-level MISPExporter singleton.

## modules/integrations/nuclei_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`
- `TemplateSelector.select` (method) `modules/integrations/nuclei_bridge.py:91` `def select(self, services, cves)` -- Return templates relevant to the provided *services* and *cves*.
- `LocalTemplateIndex.__init__` (method) `modules/integrations/nuclei_bridge.py:114` `def __init__(self, templates_dir)`
- `LocalTemplateIndex.select` (method) `modules/integrations/nuclei_bridge.py:121` `def select(self, services, cves)`
- `LocalTemplateIndex.build` (method) `modules/integrations/nuclei_bridge.py:141` `def build(self)` -- Force a (re)build of the template index.
- `NucleiRunner.__init__` (method) `modules/integrations/nuclei_bridge.py:288` `def __init__(self)`
- `NucleiRunner.run` (method) `modules/integrations/nuclei_bridge.py:293` `def run(self, target, templates, output_dir)` -- Execute nuclei against *target* using the provided *templates*.
- `NucleiRunner.run_for_findings` (method) `modules/integrations/nuclei_bridge.py:326` `def run_for_findings(self, target, findings, output_dir, selector)` -- Convenience: extract services/CVEs from *findings*, select templates, run.
- `NucleiBridge.__init__` (method) `modules/integrations/nuclei_bridge.py:396` `def __init__(self, selector, runner)`
- `NucleiBridge.scan` (method) `modules/integrations/nuclei_bridge.py:404` `def scan(self, target, findings, dry_run)` -- Select templates from *findings* and run nuclei against *target*.
- `NucleiBridge.list_templates` (method) `modules/integrations/nuclei_bridge.py:427` `def list_templates(self, services, cves)` -- Return matching templates without running nuclei.
- `NucleiBridge.get_bridge` (method) `modules/integrations/nuclei_bridge.py:443` `def get_bridge()` -- Return the module-level NucleiBridge singleton.
- `_F.__init__` (method) `modules/integrations/nuclei_bridge.py:484` `def __init__(self, ftype, value)`

## modules/integrations/nuclei_parser.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/integrations/nuclei_bridge.py`, `modules/world_model.py`
Imported by: `modules/intelligence_engine.py`, `tests/test_nuclei_parser.py`
- `NucleiFinding.mitre_tactic` (method) `modules/integrations/nuclei_parser.py:87` `def mitre_tactic(self)`
- `NucleiFinding.exploit_probability` (method) `modules/integrations/nuclei_parser.py:95` `def exploit_probability(self)`
- `NucleiParser.__init__` (method) `modules/integrations/nuclei_parser.py:109` `def __init__(self, sessions_dir)`
- `NucleiParser.parse_text` (method) `modules/integrations/nuclei_parser.py:115` `def parse_text(self, text)` -- Parse raw nuclei text output (table format).
- `NucleiParser.parse_json` (method) `modules/integrations/nuclei_parser.py:134` `def parse_json(self, json_text)` -- Parse nuclei JSON output (``-jsonl`` or ``-json`` format).
- `NucleiParser.parse_file` (method) `modules/integrations/nuclei_parser.py:177` `def parse_file(self, filepath)` -- Parse nuclei output from a file (auto-detects format).
- `NucleiParser.import_to_db` (method) `modules/integrations/nuclei_parser.py:196` `def import_to_db(self, findings, rhost, workspace_name)` -- Import parsed findings into the LazyOwnDB vulnerabilities table.
- `NucleiParser.enrich_world_model` (method) `modules/integrations/nuclei_parser.py:262` `def enrich_world_model(self, findings, rhost)` -- Feed parsed findings into the WorldModel for autonomous decision-making.
- `NucleiParser.generate_recommendations` (method) `modules/integrations/nuclei_parser.py:300` `def generate_recommendations(self, findings, rhost)` -- Generate actionable LazyOwn command recommendations from findings.
- `NucleiParser.scan_and_import` (method) `modules/integrations/nuclei_parser.py:328` `def scan_and_import(self, target, templates, services, cves, workspace_name)` -- Run nuclei scan against target, parse output, and import to DB/WorldModel.

## modules/integrations/searchsploit.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `tests/test_core_modules.py`
- `ExploitSource.search_cve` (method) `modules/integrations/searchsploit.py:80` `def search_cve(self, cve_id)` -- Return exploits matching *cve_id* (e.g. 'CVE-2021-41773').
- `ExploitSource.search_service` (method) `modules/integrations/searchsploit.py:84` `def search_service(self, name, version)` -- Return exploits matching the service *name* and optional *version*.
- `SearchsploitCLI.__init__` (method) `modules/integrations/searchsploit.py:102` `def __init__(self)`
- `SearchsploitCLI.search_cve` (method) `modules/integrations/searchsploit.py:109` `def search_cve(self, cve_id)`
- `SearchsploitCLI.search_service` (method) `modules/integrations/searchsploit.py:112` `def search_service(self, name, version)`
- `ExploitDBAPI.__init__` (method) `modules/integrations/searchsploit.py:201` `def __init__(self)`
- `ExploitDBAPI.search_cve` (method) `modules/integrations/searchsploit.py:207` `def search_cve(self, cve_id)`
- `ExploitDBAPI.search_service` (method) `modules/integrations/searchsploit.py:210` `def search_service(self, name, version)`
- `SearchsploitClient.__init__` (method) `modules/integrations/searchsploit.py:278` `def __init__(self, primary, fallback)`
- `SearchsploitClient.search_cve` (method) `modules/integrations/searchsploit.py:286` `def search_cve(self, cve_id)` -- Return exploits for *cve_id*, trying CLI then API.
- `SearchsploitClient.search_service` (method) `modules/integrations/searchsploit.py:293` `def search_service(self, name, version)` -- Return exploits for *name*/*version*, trying CLI then API.
- `SearchsploitClient.enrich_findings` (method) `modules/integrations/searchsploit.py:300` `def enrich_findings(self, findings)` -- Takes an ObsParser Finding list, extracts CVEs and service_versions, returns ``{cve_or_service: [ExploitEntry, ...]}``.
- `SearchsploitClient.get_client` (method) `modules/integrations/searchsploit.py:333` `def get_client()` -- Return the module-level SearchsploitClient singleton.
- `SearchsploitClient.search_cve` (method) `modules/integrations/searchsploit.py:341` `def search_cve(cve_id)` -- Module-level convenience: search by CVE id.
- `SearchsploitClient.search_service` (method) `modules/integrations/searchsploit.py:346` `def search_service(name, version)` -- Module-level convenience: search by service name and version.

## modules/intelligence_engine.py
Depends on: `core/logging.py`, `modules/estorides_importer.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`
- `IntelligenceEngine.__init__` (method) `modules/intelligence_engine.py:142` `def __init__(self, config)`
- `IntelligenceEngine.collect_from_scan` (method) `modules/intelligence_engine.py:153` `def collect_from_scan(self, target)` -- Parse nmap XML into structured facts.
- `IntelligenceEngine.collect_from_tool` (method) `modules/intelligence_engine.py:255` `def collect_from_tool(self, output, tool, host)` -- Parse tool output into structured facts using ObsParser.
- `IntelligenceEngine.collect_from_estorides` (method) `modules/intelligence_engine.py:292` `def collect_from_estorides(self, target)` -- Run estorides OSINT aggregator and collect findings.
- `IntelligenceEngine.collect_from_nuclei` (method) `modules/intelligence_engine.py:334` `def collect_from_nuclei(self, target)` -- Run nuclei vulnerability scanner and collect findings.
- `IntelligenceEngine.collect_from_yara` (method) `modules/intelligence_engine.py:376` `def collect_from_yara(self, target_path)` -- Scan with YARA rules and collect IOC matches.
- `IntelligenceEngine.collect_from_factstore` (method) `modules/intelligence_engine.py:415` `def collect_from_factstore(self)` -- Ingest structured facts from FactStore policy_facts.json.
- `IntelligenceEngine.analyze` (method) `modules/intelligence_engine.py:477` `def analyze(self)` -- Correlate collected facts into structured intelligence.
- `IntelligenceEngine.produce_intelligence` (method) `modules/intelligence_engine.py:685` `def produce_intelligence(self)` -- Grade and enrich intelligence assessments with MITRE mappings.
- `IntelligenceEngine.produce_counter_intelligence` (method) `modules/intelligence_engine.py:715` `def produce_counter_intelligence(self)` -- Assess what we exposed and what can detect us.
- `IntelligenceEngine.disseminate` (method) `modules/intelligence_engine.py:765` `def disseminate(self)` -- Write intelligence to WorldModel, killchain, and report file.
- `IntelligenceEngine.run_full_cycle` (method) `modules/intelligence_engine.py:845` `def run_full_cycle(self, target)` -- Execute the complete intelligence cycle for a target.
- `IntelligenceEngine.get_intel_report` (method) `modules/intelligence_engine.py:874` `def get_intel_report(self)` -- Produce a structured JSON intelligence report.
- `IntelligenceEngine.get_intelligence_engine` (method) `modules/intelligence_engine.py:931` `def get_intelligence_engine(config)` -- Return the module-level singleton IntelligenceEngine.

## modules/iptables_portforward.sh
- `display_usage` (function) `modules/iptables_portforward.sh:29`

## modules/k8s_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `K8SAttackEngine.__init__` (method) `modules/k8s_attacks.py:87` `def __init__(self, config)`
- `K8SAttackEngine.enumerate_rbac` (method) `modules/k8s_attacks.py:90` `def enumerate_rbac(self)` -- Enumerate RBAC permissions for the current identity.
- `K8SAttackEngine.privileged_pod_escape` (method) `modules/k8s_attacks.py:118` `def privileged_pod_escape(self)` -- Plan a privileged pod escape.
- `K8SAttackEngine.service_account_token_theft` (method) `modules/k8s_attacks.py:173` `def service_account_token_theft(self)` -- Steal service account tokens across namespaces for lateral movement.
- `K8SAttackEngine.kubelet_anonymous_auth_abuse` (method) `modules/k8s_attacks.py:198` `def kubelet_anonymous_auth_abuse(self)` -- Exploit kubelet anonymous authentication.
- `K8SAttackEngine.etcd_access_exploitation` (method) `modules/k8s_attacks.py:222` `def etcd_access_exploitation(self)` -- Exploit etcd database access for complete cluster compromise.
- `K8SAttackEngine.helm_tiller_abuse` (method) `modules/k8s_attacks.py:250` `def helm_tiller_abuse(self)` -- Abuse Helm (v2 Tiller or v3 RBAC) for privilege escalation.
- `K8SAttackEngine.persistence_techniques` (method) `modules/k8s_attacks.py:278` `def persistence_techniques(self)` -- Kubernetes persistence techniques for long-term access.
- `K8SAttackEngine.summary` (method) `modules/k8s_attacks.py:318` `def summary(self)`

## modules/kerberoasting.py
Depends on: `modules/kerberos_core.py`
Imported by: `cli/commands/active_directory.py`
- `KerberoastingEngine.__init__` (method) `modules/kerberoasting.py:95` `def __init__(self, domain, dc_ip, username, password, hash)`
- `KerberoastingEngine.enumerate_spns` (method) `modules/kerberoasting.py:112` `def enumerate_spns(self, ldap_output, bloodhound_data)` -- Enumerate kerberoastable service principals.
- `KerberoastingEngine.priority` (method) `modules/kerberoasting.py:172` `def priority(target)`
- `KerberoastingEngine.request_tgs_aes_only` (method) `modules/kerberoasting.py:187` `def request_tgs_aes_only(self, user_spn)` -- Request a TGS ticket using only AES encryption (evades RC4 detection).
- `KerberoastingEngine.request_tgs_rc4` (method) `modules/kerberoasting.py:208` `def request_tgs_rc4(self, user_spn)` -- Request a TGS ticket using RC4-HMAC (mode 13100 for Hashcat).
- `KerberoastingEngine.request_tgs` (method) `modules/kerberoasting.py:219` `def request_tgs(self, user_spn, etype)` -- Request a TGS service ticket for kerberoasting.
- `KerberoastingEngine.targeted_kerberoast` (method) `modules/kerberoasting.py:271` `def targeted_kerberoast(self, high_value_only)` -- Perform targeted Kerberoasting on enumerated SPNs.
- `KerberoastingEngine.asreproast_check` (method) `modules/kerberoasting.py:306` `def asreproast_check(self, usernames)` -- Check which users do NOT require Kerberos pre-authentication (AS-REP roastable).
- `KerberoastingEngine.extract_hashes_from_pcap` (method) `modules/kerberoasting.py:321` `def extract_hashes_from_pcap(self, pcap_path)` -- Extract Kerberoast hashes from a PCAP/PCAPNG network capture.
- `KerberoastingEngine.detect_kerberoasting_activity` (method) `modules/kerberoasting.py:336` `def detect_kerberoasting_activity(self, event_log)` -- Analyze Windows Event Logs for signs of Kerberoasting attacks.
- `KerberoastingEngine.build_hashcat_batch` (method) `modules/kerberoasting.py:379` `def build_hashcat_batch(self, output_path)` -- Build a batch file with all extracted hashes for Hashcat cracking.
- `KerberoastingEngine.summary` (method) `modules/kerberoasting.py:401` `def summary(self)` -- Return a summary of kerberoasting operations.

## modules/kerberos_core.py
Imported by: `modules/kerberoasting.py`, `modules/kerberos_tickets.py`
- `KerberosPrincipal.to_string` (method) `modules/kerberos_core.py:152` `def to_string(self)`
- `KerberosTicket.has_flag` (method) `modules/kerberos_core.py:207` `def has_flag(self, flag_name)`
- `KerberosCrypto.__init__` (method) `modules/kerberos_core.py:277` `def __init__(self)`
- `KerberosCrypto.derive_aes_key` (method) `modules/kerberos_core.py:282` `def derive_aes_key(password, salt, etype)` -- Derive an AES Kerberos key from a password using string-to-key.
- `KerberosCrypto.derive_rc4_key` (method) `modules/kerberos_core.py:318` `def derive_rc4_key(password)` -- Derive RC4-HMAC Kerberos key from password (hash = MD4(UTF16LE(password))).
- `KerberosCrypto.aes_encrypt` (method) `modules/kerberos_core.py:329` `def aes_encrypt(self, key, plaintext, usage)` -- AES encrypt with Kerberos ciphertext stealing (CTS) mode.
- `KerberosCrypto.aes_decrypt` (method) `modules/kerberos_core.py:361` `def aes_decrypt(self, key, ciphertext, usage)` -- AES decrypt with Kerberos CTS mode.
- `KerberosCrypto.compute_checksum` (method) `modules/kerberos_core.py:389` `def compute_checksum(key, data, etype)` -- Compute a Kerberos checksum using HMAC-SHA1-96-AES.
- `KerberosCore.__init__` (method) `modules/kerberos_core.py:421` `def __init__(self, domain, dc_host, dc_ip)`
- `KerberosCore.get_supported_etypes` (method) `modules/kerberos_core.py:427` `def get_supported_etypes(self)` -- Return encryption types supported by this implementation.
- `KerberosCore.build_as_req` (method) `modules/kerberos_core.py:435` `def build_as_req(self, username, domain, password, etype)` -- Build an AS-REQ message for TGT retrieval.
- `KerberosCore.build_tgs_req` (method) `modules/kerberos_core.py:489` `def build_tgs_req(self, params)` -- Build a TGS-REQ message for service ticket retrieval.
- `KerberosCore.parse_as_rep` (method) `modules/kerberos_core.py:534` `def parse_as_rep(self, as_rep_data, key, etype)` -- Parse an AS-REP response and extract the TGT and session key.
- `KerberosCore.parse_tgs_rep` (method) `modules/kerberos_core.py:550` `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)` -- Parse a TGS-REP response and extract the service ticket.
- `KerberosCore.decrypt_ticket` (method) `modules/kerberos_core.py:563` `def decrypt_ticket(self, ticket_data, key, etype)` -- Decrypt the encrypted portion of a Kerberos ticket.
- `KerberosCore.parse_pac` (method) `modules/kerberos_core.py:588` `def parse_pac(self, pac_data)` -- Parse a Privilege Attribute Certificate (PAC) from decrypted auth data.
- `KerberosErrorParser.parse_error` (method) `modules/kerberos_core.py:687` `def parse_error(error_data)` -- Extract error code, message, and client/server realm from a KRB-ERROR.
- `TicketValidator.is_expired` (method) `modules/kerberos_core.py:706` `def is_expired(endtime, grace_period)` -- Check if a ticket has expired.
- `TicketValidator.validate_flags` (method) `modules/kerberos_core.py:719` `def validate_flags(ticket, required_flags)` -- Check that a ticket has all required flags.
- `TicketValidator.validate_pac_checksums` (method) `modules/kerberos_core.py:735` `def validate_pac_checksums(pac)` -- Validate PAC server and KDC checksums.

## modules/kerberos_tickets.py
Depends on: `modules/kerberos_core.py`
Imported by: `cli/commands/active_directory.py`
- `SilverTicketForger.__init__` (method) `modules/kerberos_tickets.py:131` `def __init__(self)`
- `SilverTicketForger.forge` (method) `modules/kerberos_tickets.py:134` `def forge(self, config)` -- Forge a silver ticket for the specified service.
- `GoldenTicketForger.__init__` (method) `modules/kerberos_tickets.py:272` `def __init__(self)`
- `GoldenTicketForger.forge` (method) `modules/kerberos_tickets.py:275` `def forge(self, config)` -- Forge a golden ticket TGT.
- `DiamondTicketForger.__init__` (method) `modules/kerberos_tickets.py:405` `def __init__(self)`
- `DiamondTicketForger.forge` (method) `modules/kerberos_tickets.py:408` `def forge(self, config)` -- Forge a diamond ticket with PAC enhancement.
- `SapphireTicketForger.__init__` (method) `modules/kerberos_tickets.py:469` `def __init__(self, kerberos_core)`
- `SapphireTicketForger.forge_s4u2self` (method) `modules/kerberos_tickets.py:472` `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)` -- Generate a TGS-REQ for S4U2self service ticket.
- `SapphireTicketForger.forge_rbcd` (method) `modules/kerberos_tickets.py:530` `def forge_rbcd(self, machine_account_hash, target_service, domain, username)` -- Generate exploit instructions for resource-based constrained delegation.
- `SkeletonKeyInjector.detect_skeleton_key` (method) `modules/kerberos_tickets.py:578` `def detect_skeleton_key(target_host, domain, dc_ip)` -- Check if skeleton key is active on a DC.
- `SkeletonKeyInjector.inject_command` (method) `modules/kerberos_tickets.py:600` `def inject_command(target_host)` -- Generate mimikatz command for skeleton key injection on a DC.
- `SkeletonKeyInjector.cleanup_command` (method) `modules/kerberos_tickets.py:612` `def cleanup_command()` -- Generate LSASS restart command to remove skeleton key patch.

## modules/kill_chain_viz.py
Depends on: `modules/killchain.py`
Imported by: `lazyc2.py`
- `generate_html` (function) `modules/kill_chain_viz.py:69` `def generate_html(target, sessions)`
- `generate_svg` (function) `modules/kill_chain_viz.py:102` `def generate_svg(target, sessions)`

## modules/killchain.py
Depends on: `core/logging.py`, `modules/world_model.py`
Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `scripts/devtools/core_smoke.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`
- `KillChainConfig.world_model_path` (method) `modules/killchain.py:116` `def world_model_path(self)` -- Return the resolved path to world_model.json.
- `KillChainConfig.phase_index` (method) `modules/killchain.py:120` `def phase_index(self, phase)` -- Return the positional index of a canonical phase in the kill chain.
- `KillChainConfig.is_valid_phase` (method) `modules/killchain.py:127` `def is_valid_phase(self, phase)` -- Return True when ``phase`` is a recognised canonical phase.
- `KillChain.config` (method) `modules/killchain.py:154` `def config()` -- Return the centralised configuration.
- `KillChain.phases` (method) `modules/killchain.py:159` `def phases()` -- Return the canonical 8-phase tuple.
- `KillChain.phase_labels` (method) `modules/killchain.py:164` `def phase_labels()` -- Return the canonical phase label mapping.
- `KillChain.phase_colors` (method) `modules/killchain.py:169` `def phase_colors()` -- Return the canonical phase hex-color mapping.
- `KillChain.phase_rich_colors` (method) `modules/killchain.py:174` `def phase_rich_colors()` -- Return the canonical phase rich-terminal color mapping.
- `KillChain.engagement_phase_to_cli` (method) `modules/killchain.py:179` `def engagement_phase_to_cli(engagement_value)` -- Map a ``WorldModel.EngagementPhase`` value to the CLI phase key.
- `KillChain.cli_phase_to_host_state` (method) `modules/killchain.py:191` `def cli_phase_to_host_state(phase)` -- Map a CLI phase to a ``WorldModel.HostState`` value.
- `KillChain.current_phase` (method) `modules/killchain.py:204` `def current_phase(world_model_path)` -- Derive the current kill-chain phase.
- `KillChain.advance_phase` (method) `modules/killchain.py:251` `def advance_phase(new_phase, world_model_path)` -- Advance the kill-chain phase for all connected surfaces.
- `KillChain.get_progress` (method) `modules/killchain.py:315` `def get_progress(world_model_path)` -- Return the current kill-chain progress as a list of status objects.
- `KillChain.compact_progress` (method) `modules/killchain.py:364` `def compact_progress(current_phase, phases_entered)` -- Return a compact single-line progress indicator ``[R>E>X>P>L]``.
- `KillChain.phases_for_display` (method) `modules/killchain.py:384` `def phases_for_display()` -- Return an ordered ``(key, label, hex_color)`` triple for every phase.
- `KillChain.phase_index` (method) `modules/killchain.py:395` `def phase_index(phase)` -- Return the zero-based index of a canonical phase.
- `KillChain.snapshot` (method) `modules/killchain.py:400` `def snapshot(world_model_path)` -- Return a single, render-agnostic snapshot of the whole kill-chain.
- `KillChain.get_killchain` (method) `modules/killchain.py:440` `def get_killchain()` -- Return the ``KillChain`` class as a module-level entry point.

## modules/kivi.py
- `ReverseShellApp.build` (method) `modules/kivi.py:12` `def build(self)`
- `ReverseShellApp.connect_to_server` (method) `modules/kivi.py:27` `def connect_to_server(self, instance)`

## modules/lazy_rbac.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`
- `Role.valid_roles` (method) `modules/lazy_rbac.py:62` `def valid_roles(cls)`
- `RBACUser.to_dict` (method) `modules/lazy_rbac.py:136` `def to_dict(self)`
- `RBACUser.from_dict` (method) `modules/lazy_rbac.py:140` `def from_dict(cls, data)`
- `RBACUser.get_role` (method) `modules/lazy_rbac.py:164` `def get_role(self)`
- `RBACUser.has_permission` (method) `modules/lazy_rbac.py:170` `def has_permission(self, permission)`
- `RBACUser.can_manage_role` (method) `modules/lazy_rbac.py:174` `def can_manage_role(self, target_role)` -- Check if this user can assign/manage the given role.
- `RBACUser.get_mfa_provisioning_uri` (method) `modules/lazy_rbac.py:182` `def get_mfa_provisioning_uri(self)`
- `RBACUser.verify_totp` (method) `modules/lazy_rbac.py:187` `def verify_totp(self, token)`
- `RBACUser.verify_recovery_code` (method) `modules/lazy_rbac.py:192` `def verify_recovery_code(self, code)`
- `RBACUser.consume_recovery_code` (method) `modules/lazy_rbac.py:200` `def consume_recovery_code(self, code)`
- `RBACStore.__init__` (method) `modules/lazy_rbac.py:213` `def __init__(self, users_path)`
- `RBACStore.load_all` (method) `modules/lazy_rbac.py:245` `def load_all(self)`
- `RBACStore.find_by_id` (method) `modules/lazy_rbac.py:249` `def find_by_id(self, user_id)`
- `RBACStore.find_by_username` (method) `modules/lazy_rbac.py:255` `def find_by_username(self, username)`
- `RBACStore.save` (method) `modules/lazy_rbac.py:261` `def save(self, user)`
- `RBACStore.create_user` (method) `modules/lazy_rbac.py:274` `def create_user(self, username, password_hash, role, tenant_id)`
- `RBACStore.delete_user` (method) `modules/lazy_rbac.py:295` `def delete_user(self, user_id)`
- `RBACStore.update_role` (method) `modules/lazy_rbac.py:304` `def update_role(self, user_id, new_role)`
- `RBACStore.enable_mfa` (method) `modules/lazy_rbac.py:314` `def enable_mfa(self, user_id)`
- `RBACStore.disable_mfa` (method) `modules/lazy_rbac.py:324` `def disable_mfa(self, user_id)`
- `RBACStore.consume_recovery_code` (method) `modules/lazy_rbac.py:334` `def consume_recovery_code(self, user_id, code)`
- `RBACStore.ensure_admin` (method) `modules/lazy_rbac.py:343` `def ensure_admin(self, username, password_hash)` -- Ensure at least one admin exists, creating one if needed.
- `TenantConfig.from_payload` (method) `modules/lazy_rbac.py:377` `def from_payload(cls, tenant_id, name, payload_path)`
- `TenantConfig.to_dict` (method) `modules/lazy_rbac.py:386` `def to_dict(self)`
- `TenantConfig.from_dict` (method) `modules/lazy_rbac.py:390` `def from_dict(cls, data)`
- `TenantManager.__init__` (method) `modules/lazy_rbac.py:397` `def __init__(self, payloads_dir, config_path, default_payload)`
- `TenantManager.list_tenants` (method) `modules/lazy_rbac.py:431` `def list_tenants(self)`
- `TenantManager.get_active` (method) `modules/lazy_rbac.py:434` `def get_active(self)`
- `TenantManager.get_active_payload_path` (method) `modules/lazy_rbac.py:439` `def get_active_payload_path(self)`
- `TenantManager.get_active_sessions_dir` (method) `modules/lazy_rbac.py:445` `def get_active_sessions_dir(self)`
- `TenantManager.get_payload_for_tenant` (method) `modules/lazy_rbac.py:451` `def get_payload_for_tenant(self, tenant_id)`
- `TenantManager.create_tenant` (method) `modules/lazy_rbac.py:457` `def create_tenant(self, name, base_payload)`
- `TenantManager.switch_tenant` (method) `modules/lazy_rbac.py:486` `def switch_tenant(self, tenant_id)`
- `TenantManager.delete_tenant` (method) `modules/lazy_rbac.py:495` `def delete_tenant(self, tenant_id)`
- `TenantManager.ensure_default_tenant` (method) `modules/lazy_rbac.py:504` `def ensure_default_tenant(self)`
- `TenantManager.init_rbac_store` (method) `modules/lazy_rbac.py:523` `def init_rbac_store(users_path)`
- `TenantManager.init_tenant_manager` (method) `modules/lazy_rbac.py:527` `def init_tenant_manager(payloads_dir, config_path, default_payload)`
- `TenantManager.require_role` (method) `modules/lazy_rbac.py:539` `def require_role()` -- Flask decorator: require one of the given roles.
- `TenantManager.decorator` (method) `modules/lazy_rbac.py:542` `def decorator(f)`
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:544` `def decorated()`
- `TenantManager.require_permission` (method) `modules/lazy_rbac.py:565` `def require_permission()` -- Flask decorator: require specific permissions.
- `TenantManager.decorator` (method) `modules/lazy_rbac.py:568` `def decorator(f)`
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:570` `def decorated()`
- `TenantManager.require_mfa` (method) `modules/lazy_rbac.py:596` `def require_mfa(f)` -- Decorator that enforces MFA before accessing protected routes.
- `TenantManager.decorated` (method) `modules/lazy_rbac.py:600` `def decorated()`
- `TenantManager.get_rbac_store` (method) `modules/lazy_rbac.py:639` `def get_rbac_store()`
- `TenantManager.set_rbac_store` (method) `modules/lazy_rbac.py:643` `def set_rbac_store(store)`
- `TenantManager.get_tenant_manager` (method) `modules/lazy_rbac.py:648` `def get_tenant_manager()`
- `TenantManager.set_tenant_manager` (method) `modules/lazy_rbac.py:655` `def set_tenant_manager(tm)`
- `TenantManager.check_cli_permission` (method) `modules/lazy_rbac.py:660` `def check_cli_permission(username, permission)` -- Check if a CLI user has the given permission.
- `TenantManager.get_user_role` (method) `modules/lazy_rbac.py:672` `def get_user_role(username)`
- `TenantManager.generate_mfa_qr_url` (method) `modules/lazy_rbac.py:680` `def generate_mfa_qr_url(secret, username)` -- Generate a QR code data URI for MFA setup (local, no external API).
- `TenantManager.generate_qr_svg` (method) `modules/lazy_rbac.py:689` `def generate_qr_svg(data)` -- Generate an SVG QR code image from text data.
- `TenantManager.gf_mul` (method) `modules/lazy_rbac.py:927` `def gf_mul(a, b)`

## modules/lazyatack.sh
- `mostrar_ayuda` (function) `modules/lazyatack.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyatack.sh:33` -- Función para validar una dirección IP
- `validar_url` (function) `modules/lazyatack.sh:49` -- Función para validar URL
- `descargar_seclists` (function) `modules/lazyatack.sh:107` -- Función para descargar y extraer SecLists
- `escanear_puertos` (function) `modules/lazyatack.sh:115` -- Función para ejecutar escaneo de puertos con nmap
- `escanear_puertos_especificos` (function) `modules/lazyatack.sh:121` -- Función para escanear puertos específicos
- `enumerar_http` (function) `modules/lazyatack.sh:127` -- Función para enumerar servicios HTTP
- `iniciar_servidor_http` (function) `modules/lazyatack.sh:133` -- Función para iniciar servidor HTTP con Python
- `configurar_netcat` (function) `modules/lazyatack.sh:139` -- Función para configurar netcat
- `enviar_archivo_netcat` (function) `modules/lazyatack.sh:145` -- Función para enviar archivo mediante bash a netcat
- `verificar_conectividad` (function) `modules/lazyatack.sh:151` -- Función para verificar conectividad con ping y tcpdump
- `verificar_curl` (function) `modules/lazyatack.sh:158` -- Función para verificar conectividad con curl
- `configurar_shell_reversa` (function) `modules/lazyatack.sh:165` -- Función para configurar una shell reversa
- `escuchar_shell` (function) `modules/lazyatack.sh:171` -- Función para escuchar shell con netcat
- `monitorear_procesos` (function) `modules/lazyatack.sh:177` -- Función para monitorear procesos
- `ejecutar_wfuzz` (function) `modules/lazyatack.sh:188` -- Función para ejecutar wfuzz
- `comprobar_sudo` (function) `modules/lazyatack.sh:194` -- Función para comprobar permisos sudo
- `explotar_lfi` (function) `modules/lazyatack.sh:200` -- Función para explotar LFI
- `configurar_tty` (function) `modules/lazyatack.sh:206` -- Función para configurar TTY
- `eliminar_archivos` (function) `modules/lazyatack.sh:217` -- Función para eliminar archivos de forma segura
- `obtener_root_shell` (function) `modules/lazyatack.sh:223` -- Función para obtener root shell mediante Docker
- `enumerar_suid` (function) `modules/lazyatack.sh:230` -- Función para enumerar archivos con SUID
- `listar_timers` (function) `modules/lazyatack.sh:236` -- Función para listar timers de systemd
- `comprobar_rutas` (function) `modules/lazyatack.sh:242` -- Función para comprobar rutas de comandos
- `abusar_tar` (function) `modules/lazyatack.sh:248` -- Función para abusar de tar
- `enumerar_puertos` (function) `modules/lazyatack.sh:254` -- Función para enumerar puertos abiertos
- `eliminar_contenedores_docker` (function) `modules/lazyatack.sh:260` -- Función para eliminar contenedores Docker
- `escanear_red` (function) `modules/lazyatack.sh:266` -- Función para escanear red
- `menu_servidor` (function) `modules/lazyatack.sh:272` -- Función para mostrar menú en modo servidor
- `menu_cliente` (function) `modules/lazyatack.sh:307` -- Función para mostrar menú en modo cliente

## modules/lazycloud.py
Imported by: `cli/commands/cloud.py`
- `CloudMetadataHarvester.__init__` (method) `modules/lazycloud.py:111` `def __init__(self, timeout)`
- `CloudMetadataHarvester.session` (method) `modules/lazycloud.py:116` `def session(self)`
- `CloudMetadataHarvester.harvest_aws` (method) `modules/lazycloud.py:139` `def harvest_aws(self)` -- Harvest AWS EC2 instance metadata (IMDSv2 capable).
- `CloudMetadataHarvester.harvest_azure` (method) `modules/lazycloud.py:184` `def harvest_azure(self)` -- Harvest Azure instance metadata.
- `CloudMetadataHarvester.harvest_gcp` (method) `modules/lazycloud.py:208` `def harvest_gcp(self)` -- Harvest GCP instance metadata.
- `CloudMetadataHarvester.harvest_all` (method) `modules/lazycloud.py:231` `def harvest_all(self)` -- Try all three cloud providers sequentially.
- `CloudBucketEnumerator.__init__` (method) `modules/lazycloud.py:251` `def __init__(self, timeout)`
- `CloudBucketEnumerator.session` (method) `modules/lazycloud.py:256` `def session(self)`
- `CloudBucketEnumerator.enumerate_s3` (method) `modules/lazycloud.py:278` `def enumerate_s3(self, prefix, buckets)` -- Enumerate S3 buckets derived from a prefix.
- `CloudBucketEnumerator.enumerate_azure_storage` (method) `modules/lazycloud.py:303` `def enumerate_azure_storage(self, prefix, accounts)` -- Enumerate Azure Blob Storage accounts.
- `CloudBucketEnumerator.enumerate_gcp_storage` (method) `modules/lazycloud.py:321` `def enumerate_gcp_storage(self, prefix, buckets)` -- Enumerate GCP Storage buckets.
- `CloudIAMEnumerator.enumerate_aws_iam` (method) `modules/lazycloud.py:345` `def enumerate_aws_iam(self, access_key, secret_key, session_token)` -- Enumerate AWS IAM (requires valid credentials).
- `CloudScanner.__init__` (method) `modules/lazycloud.py:393` `def __init__(self, target_domain, timeout)`
- `CloudScanner.full_scan` (method) `modules/lazycloud.py:400` `def full_scan(self, target_prefix, sessions_dir)` -- Perform a comprehensive cloud security scan.
- `CloudScanner.quick_metadata` (method) `modules/lazycloud.py:456` `def quick_metadata(self)` -- Fast metadata-only harvest (no bucket enumeration).
- `CloudScanner.quick_buckets` (method) `modules/lazycloud.py:460` `def quick_buckets(self, prefix)` -- Fast S3-only bucket check.

## modules/lazycurl.sh
- `ctrl_c` (function) `modules/lazycurl.sh:23`
- `show_help` (function) `modules/lazycurl.sh:29` -- Función para mostrar la ayuda
- `execute_curl` (function) `modules/lazycurl.sh:52` -- Función para ejecutar el comando CURL

## modules/lazyencoder_decoder.py
Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`
- `base64_encode` (function) `modules/lazyencoder_decoder.py:4` `def base64_encode(data)`
- `base64_decode` (function) `modules/lazyencoder_decoder.py:8` `def base64_decode(data)`
- `caesar_cipher` (function) `modules/lazyencoder_decoder.py:13` `def caesar_cipher(text, shift)`
- `caesar_decipher` (function) `modules/lazyencoder_decoder.py:27` `def caesar_decipher(text, shift)`
- `key_substitution` (function) `modules/lazyencoder_decoder.py:31` `def key_substitution(text, key)`
- `key_substitution_reverse` (function) `modules/lazyencoder_decoder.py:47` `def key_substitution_reverse(text, key)`
- `encode` (function) `modules/lazyencoder_decoder.py:63` `def encode(data, shift, key)`
- `encode_string` (function) `modules/lazyencoder_decoder.py:75` `def encode_string(data, shift, key)`
- `decode` (function) `modules/lazyencoder_decoder.py:82` `def decode(data, shift, key)`
- `decode_string` (function) `modules/lazyencoder_decoder.py:94` `def decode_string(data, shift, key)`

## modules/lazyevilwimrm.sh
- `execute_evil_winrm` (function) `modules/lazyevilwimrm.sh:14` -- Función para ejecutar evil-winrm y verificar la salida

## modules/lazyk8s.py
Imported by: `cli/commands/containers.py`
- `DockerEnumerator.__init__` (method) `modules/lazyk8s.py:44` `def __init__(self, socket_path)`
- `DockerEnumerator.is_socket_accessible` (method) `modules/lazyk8s.py:47` `def is_socket_accessible(self)` -- Check if the Docker socket is readable/writable.
- `DockerEnumerator.list_containers` (method) `modules/lazyk8s.py:70` `def list_containers(self)` -- List all containers with extended information.
- `DockerEnumerator.list_images` (method) `modules/lazyk8s.py:94` `def list_images(self)` -- List all Docker images.
- `DockerEnumerator.inspect_container` (method) `modules/lazyk8s.py:118` `def inspect_container(self, container_id)` -- Get detailed configuration of a container (privileged, mounts, capabilities).
- `DockerEnumerator.check_privileged_containers` (method) `modules/lazyk8s.py:137` `def check_privileged_containers(self)` -- Find containers running with --privileged flag.
- `DockerEnumerator.check_sensitive_mounts` (method) `modules/lazyk8s.py:162` `def check_sensitive_mounts(self)` -- Find containers with sensitive host path mounts.
- `DockerEnumerator.check_docker_socket_mount` (method) `modules/lazyk8s.py:196` `def check_docker_socket_mount(self)` -- Find containers with the Docker socket mounted (escape vector).
- `DockerEnumerator.check_capabilities` (method) `modules/lazyk8s.py:217` `def check_capabilities(self)` -- Find containers with dangerous Linux capabilities.
- `DockerEnumerator.full_check` (method) `modules/lazyk8s.py:250` `def full_check(self)` -- Execute all Docker security checks and return aggregated results.
- `K8sEnumerator.__init__` (method) `modules/lazyk8s.py:267` `def __init__(self, kubeconfig, token, api_server)`
- `K8sEnumerator.list_pods` (method) `modules/lazyk8s.py:366` `def list_pods(self, namespace)` -- List pods in all namespaces or a specific namespace.
- `K8sEnumerator.list_namespaces` (method) `modules/lazyk8s.py:390` `def list_namespaces(self)` -- List all namespaces.
- `K8sEnumerator.list_secrets` (method) `modules/lazyk8s.py:410` `def list_secrets(self, namespace)` -- List secrets (without decoding values by default).
- `K8sEnumerator.list_service_accounts` (method) `modules/lazyk8s.py:462` `def list_service_accounts(self, namespace)` -- List service accounts and their attached roles.
- `K8sEnumerator.check_rbac` (method) `modules/lazyk8s.py:498` `def check_rbac(self)` -- Check current user's RBAC permissions.
- `K8sEnumerator.check_pod_escape_vectors` (method) `modules/lazyk8s.py:530` `def check_pod_escape_vectors(self)` -- Check for pod escape vectors in the current pod.
- `K8sEnumerator.full_check` (method) `modules/lazyk8s.py:582` `def full_check(self, sessions_dir)` -- Execute all Kubernetes security checks.
- `ContainerEscapeTechniques.detect_current_environment` (method) `modules/lazyk8s.py:684` `def detect_current_environment()` -- Detect if running inside a container and identify escape opportunities.
- `ContainerRuntimeDetector.detect_runtime` (method) `modules/lazyk8s.py:803` `def detect_runtime()` -- Detect container runtime from multiple indicators.
- `ContainerRuntimeDetector.detect_mounts` (method) `modules/lazyk8s.py:874` `def detect_mounts()` -- Detect dangerous mounts in the current container.
- `ContainerRuntimeDetector.detect_dangerous_capabilities` (method) `modules/lazyk8s.py:921` `def detect_dangerous_capabilities()` -- Detect dangerous Linux capabilities in the current container.
- `ContainerRuntimeDetector.auto_detect_all` (method) `modules/lazyk8s.py:992` `def auto_detect_all()` -- Run comprehensive container escape auto-detection.

## modules/lazylynis.sh
- `check_sudo` (function) `modules/lazylynis.sh:32` -- Función para verificar y relanzar con sudo si es necesario

## modules/lazymasscan.sh
- `ctrl_c` (function) `modules/lazymasscan.sh:20`
- `extract_ports_info` (function) `modules/lazymasscan.sh:74`
- `run_masscan_script` (function) `modules/lazymasscan.sh:94`
- `print_row` (function) `modules/lazymasscan.sh:117`

## modules/lazynmap.sh
- `cleanup` (function) `modules/lazynmap.sh:29`
- `ctrl_c` (function) `modules/lazynmap.sh:38`
- `fix_sessions_owner` (function) `modules/lazynmap.sh:67` -- Best-effort ownership fixup: scans run under sudo leave root-owned files behind, and only root can chown those.
- `nmaptest` (function) `modules/lazynmap.sh:122`
- `discover_network` (function) `modules/lazynmap.sh:142`
- `extract_ports_info` (function) `modules/lazynmap.sh:811`
- `run_nmap_script` (function) `modules/lazynmap.sh:837`
- `print_row` (function) `modules/lazynmap.sh:870`

## modules/lazyown_bprfuzzer.py
Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`
- `load_headers_from_file` (function) `modules/lazyown_bprfuzzer.py:93` `def load_headers_from_file(file_path)`
- `load_data_from_file` (function) `modules/lazyown_bprfuzzer.py:99` `def load_data_from_file(file_path)`
- `signal_handler` (function) `modules/lazyown_bprfuzzer.py:105` `def signal_handler(sig, frame)`
- `ProxyHandler.do_GET` (method) `modules/lazyown_bprfuzzer.py:115` `def do_GET(self)`
- `ProxyHandler.do_POST` (method) `modules/lazyown_bprfuzzer.py:118` `def do_POST(self)`
- `ProxyHandler.run_proxy` (method) `modules/lazyown_bprfuzzer.py:162` `def run_proxy(port)`
- `ProxyHandler.edit_file_with_nano` (method) `modules/lazyown_bprfuzzer.py:169` `def edit_file_with_nano(content)`
- `ProxyHandler.send_request` (method) `modules/lazyown_bprfuzzer.py:179` `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` -- Envía una solicitud HTTP y devuelve la respuesta.
- `ProxyHandler.repeater` (method) `modules/lazyown_bprfuzzer.py:203` `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` -- Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
- `ProxyHandler.lazyfuzz` (method) `modules/lazyown_bprfuzzer.py:233` `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` -- Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
- `ProxyHandler.parse_arguments` (method) `modules/lazyown_bprfuzzer.py:278` `def parse_arguments()` -- Parsear los argumentos de la línea de comandos.
- `ProxyHandler.main` (method) `modules/lazyown_bprfuzzer.py:302` `def main()`

## modules/lazyown_bridge.py
Depends on: `modules/killchain.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`
- `CatalogEntry.build_command` (method) `modules/lazyown_bridge.py:63` `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` -- Return 'command [args]' with known values substituted.
- `CatalogEntry.matches_service` (method) `modules/lazyown_bridge.py:94` `def matches_service(self, services)`
- `CatalogEntry.matches_os` (method) `modules/lazyown_bridge.py:104` `def matches_os(self, os_hint)`
- `CommandCatalog.__init__` (method) `modules/lazyown_bridge.py:118` `def __init__(self)`
- `CommandCatalog.by_phase` (method) `modules/lazyown_bridge.py:3946` `def by_phase(self, phase)`
- `CommandCatalog.by_mitre` (method) `modules/lazyown_bridge.py:3952` `def by_mitre(self, technique_id)`
- `CommandCatalog.by_service` (method) `modules/lazyown_bridge.py:3956` `def by_service(self, service_name)`
- `CommandCatalog.by_tag` (method) `modules/lazyown_bridge.py:3960` `def by_tag(self, tag)`
- `CommandCatalog.by_os` (method) `modules/lazyown_bridge.py:3963` `def by_os(self, os_hint)`
- `CommandCatalog.all_phases` (method) `modules/lazyown_bridge.py:3966` `def all_phases(self)`
- `CommandCatalog.get` (method) `modules/lazyown_bridge.py:3969` `def get(self, command)`
- `CommandCatalog.count` (method) `modules/lazyown_bridge.py:3975` `def count(self)`
- `AbstractSelector.select` (method) `modules/lazyown_bridge.py:3986` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ServiceAwareSelector.select` (method) `modules/lazyown_bridge.py:4005` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `MitreAlignedSelector.__init__` (method) `modules/lazyown_bridge.py:4045` `def __init__(self, technique_id)`
- `MitreAlignedSelector.select` (method) `modules/lazyown_bridge.py:4049` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `TagSelector.__init__` (method) `modules/lazyown_bridge.py:4074` `def __init__(self, tag)`
- `TagSelector.select` (method) `modules/lazyown_bridge.py:4078` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ContextEnricher.enrich` (method) `modules/lazyown_bridge.py:4106` `def enrich(self, entry, target, world_snapshot)`
- `PhaseMapper.canonical_kill_chain_order` (method) `modules/lazyown_bridge.py:4204` `def canonical_kill_chain_order()` -- Return the canonical 8-phase order from KillChain (single source of truth).
- `PhaseMapper.to_bridge_phase` (method) `modules/lazyown_bridge.py:4210` `def to_bridge_phase(self, wm_phase)`
- `PhaseMapper.kill_chain_order` (method) `modules/lazyown_bridge.py:4223` `def kill_chain_order(self)` -- Ordered list of bridge phases following the kill chain.
- `BridgeDispatcher.__init__` (method) `modules/lazyown_bridge.py:4239` `def __init__(self, catalog, selector, enricher, phase_mapper)`
- `BridgeDispatcher.suggest` (method) `modules/lazyown_bridge.py:4251` `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` -- Return (command_string, entry) or None.
- `BridgeDispatcher.suggest_sequence` (method) `modules/lazyown_bridge.py:4296` `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` -- Return up to `limit` non-excluded suggestions for the phase.
- `BridgeDispatcher.suggest_for_wm_phase` (method) `modules/lazyown_bridge.py:4325` `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
- `BridgeDispatcher.list_phase` (method) `modules/lazyown_bridge.py:4343` `def list_phase(self, phase)`
- `BridgeDispatcher.all_phases` (method) `modules/lazyown_bridge.py:4347` `def all_phases(self)`
- `BridgeDispatcher.catalog_summary` (method) `modules/lazyown_bridge.py:4350` `def catalog_summary(self)`
- `BridgeDispatcher.catalog_summary_filtered` (method) `modules/lazyown_bridge.py:4358` `def catalog_summary_filtered(self, phase, os_hint)` -- Return a kill-chain summary restricted to a phase and target OS.
- `BridgeDispatcher.catalog_count` (method) `modules/lazyown_bridge.py:4395` `def catalog_count(self)`
- `BridgeDispatcher.phase_kill_chain` (method) `modules/lazyown_bridge.py:4398` `def phase_kill_chain(self)`
- `BridgeDispatcher.get_dispatcher` (method) `modules/lazyown_bridge.py:4409` `def get_dispatcher()`

## modules/lazyown_metaextract0r.py
- `signal_handler` (function) `modules/lazyown_metaextract0r.py:42` `def signal_handler(sig, frame)`
- `extract_pdf_metadata` (function) `modules/lazyown_metaextract0r.py:51` `def extract_pdf_metadata(file_path)`
- `extract_docx_metadata` (function) `modules/lazyown_metaextract0r.py:62` `def extract_docx_metadata(file_path)`
- `extract_ole_metadata` (function) `modules/lazyown_metaextract0r.py:73` `def extract_ole_metadata(file_path)`
- `extract_image_metadata` (function) `modules/lazyown_metaextract0r.py:85` `def extract_image_metadata(file_path)`
- `extract_metadata` (function) `modules/lazyown_metaextract0r.py:96` `def extract_metadata(file_path)`
- `find_and_extract_metadata` (function) `modules/lazyown_metaextract0r.py:109` `def find_and_extract_metadata(directory, output_file)`
- `parse_arguments` (function) `modules/lazyown_metaextract0r.py:130` `def parse_arguments()` -- Parse command-line arguments.
- `main` (function) `modules/lazyown_metaextract0r.py:140` `def main()`

## modules/lazyown_parquet_tool.py
- `highlight_term` (function) `modules/lazyown_parquet_tool.py:34` `def highlight_term(text, term)` -- Highlight the search term in the given text.
- `search_in_parquet` (function) `modules/lazyown_parquet_tool.py:39` `def search_in_parquet(term, parquet_files)` -- Search for a term in the given Parquet files and return matching rows.
- `buscar_binarios` (function) `modules/lazyown_parquet_tool.py:53` `def buscar_binarios(args)` -- Search for binaries with special permissions and generate a results CSV.
- `ejecutar_opciones` (function) `modules/lazyown_parquet_tool.py:136` `def ejecutar_opciones()` -- Execute options based on the found data.

## modules/lazyownclient.py
- `signal_handler` (function) `modules/lazyownclient.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownclient.py:51` `def pad(s)`
- `encrypt` (function) `modules/lazyownclient.py:55` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownclient.py:62` `def decrypt(ciphertext, key)`
- `handle_command` (function) `modules/lazyownclient.py:69` `def handle_command(cmd, key)`
- `main` (function) `modules/lazyownclient.py:198` `def main()`

## modules/lazyownerweb.py
Depends on: `core/logging.py`, `modules/logging_config.py`
- `send_request` (function) `modules/lazyownerweb.py:36` `def send_request(url, params, method)`
- `test_injection` (function) `modules/lazyownerweb.py:49` `def test_injection(url, payloads, param_name, detection_strings, method)`
- `main` (function) `modules/lazyownerweb.py:59` `def main()`

## modules/lazyownserver.py
- `signal_handler` (function) `modules/lazyownserver.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownserver.py:42` `def pad(s)`
- `encrypt` (function) `modules/lazyownserver.py:46` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownserver.py:53` `def decrypt(ciphertext, key)`
- `handle_client` (function) `modules/lazyownserver.py:60` `def handle_client(conn, addr, key)`
- `main` (function) `modules/lazyownserver.py:97` `def main()`

## modules/lazypsexec.sh
- `execute_psexec` (function) `modules/lazypsexec.sh:15` -- Función para ejecutar psexec y verificar la salida

## modules/lazyreverse_shell.sh
- `mostrar_ayuda` (function) `modules/lazyreverse_shell.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyreverse_shell.sh:31` -- Validar dirección IP

## modules/lazyvpnshield.sh
- `ctrl_c` (function) `modules/lazyvpnshield.sh:11`
- `check_sudo` (function) `modules/lazyvpnshield.sh:16`
- `save_current_rules` (function) `modules/lazyvpnshield.sh:29`
- `show_current_rules` (function) `modules/lazyvpnshield.sh:37`
- `apply_vpn_rules` (function) `modules/lazyvpnshield.sh:45`
- `undo_and_restore_rules` (function) `modules/lazyvpnshield.sh:86`
- `main` (function) `modules/lazyvpnshield.sh:113`


Next: [API_p12.md](API_p12.md)
