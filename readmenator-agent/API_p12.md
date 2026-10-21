# API (page 12 of 24)
Previous: [API_p11.md](API_p11.md)

## modules/forensic_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `ForensicCleaner.__init__` (method) `modules/forensic_cleaner.py:67` `def __init__(self, config)`
- `ForensicCleaner.windows_cleanup` (method) `modules/forensic_cleaner.py:70` `def windows_cleanup(self)` -- Generate Windows forensic artifact cleanup commands.
- `ForensicCleaner.linux_cleanup` (method) `modules/forensic_cleaner.py:165` `def linux_cleanup(self)` -- Generate Linux forensic artifact cleanup commands.
- `ForensicCleaner.macos_cleanup` (method) `modules/forensic_cleaner.py:193` `def macos_cleanup(self)` -- Generate macOS forensic artifact cleanup commands.
- `ForensicCleaner.windows_prefetch_parse` (method) `modules/forensic_cleaner.py:221` `def windows_prefetch_parse(self, prefetch_path)` -- Parse Prefetch files to identify what the attacker should clean.
- `ForensicCleaner.amcache_parse` (method) `modules/forensic_cleaner.py:259` `def amcache_parse(self)` -- Parse Amcache registry entries for evidence of execution.

## modules/gcp_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `GCPAttackEngine.__init__` (method) `modules/gcp_attacks.py:90` `def __init__(self, config)`
- `GCPAttackEngine.enumerate_iam_policy` (method) `modules/gcp_attacks.py:93` `def enumerate_iam_policy(self, resource)` -- Enumerate IAM policies for projects, folders, or organizations.
- `GCPAttackEngine.service_account_impersonation` (method) `modules/gcp_attacks.py:119` `def service_account_impersonation(self)` -- Exploit service account impersonation for privilege escalation.
- `GCPAttackEngine.cloud_functions_backdoor` (method) `modules/gcp_attacks.py:144` `def cloud_functions_backdoor(self)` -- Backdoor Cloud Functions for privilege escalation.
- `GCPAttackEngine.compute_engine_metadata_exfil` (method) `modules/gcp_attacks.py:173` `def compute_engine_metadata_exfil(self)` -- Exfiltrate GCE instance metadata and service account tokens.
- `GCPAttackEngine.gcs_enumeration` (method) `modules/gcp_attacks.py:194` `def gcs_enumeration(self)` -- Enumerate Cloud Storage buckets for sensitive data.
- `GCPAttackEngine.cloudbuild_abuse` (method) `modules/gcp_attacks.py:230` `def cloudbuild_abuse(self)` -- Abuse Cloud Build for privilege escalation.
- `GCPAttackEngine.organization_escalation` (method) `modules/gcp_attacks.py:261` `def organization_escalation(self)` -- Escalate from project-level to organization-level access.
- `GCPAttackEngine.summary` (method) `modules/gcp_attacks.py:297` `def summary(self)`

## modules/generate_tools.py
- `extract_cmd2_tools` (function) `modules/generate_tools.py:6` `def extract_cmd2_tools(script_path)`

## modules/goals.py
Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`
- `TaskConstraints.blocked` (method) `modules/goals.py:35` `def blocked(self, command)` -- Return the blocking constraint or empty string.
- `decompose_rule_based` (function) `modules/goals.py:63` `def decompose_rule_based(objective_text, max_goals)` -- Split objective text into goal specs without an LLM (deterministic).
- `load_constraints` (function) `modules/goals.py:83` `def load_constraints(payload)` -- Build constraints from payload config (deny wins, LAZY parity).
- `constraint_block_text` (function) `modules/goals.py:103` `def constraint_block_text(constraints)` -- Render the constraint block injected at max priority (LAZY parity).
- `GoalTracker.__init__` (method) `modules/goals.py:120` `def __init__(self, goals)` -- Bind to an initial goal list.
- `GoalTracker.goals` (method) `modules/goals.py:125` `def goals(self)` -- Return a copy of tracked goals.
- `GoalTracker.prove_goal` (method) `modules/goals.py:129` `def prove_goal(self, goal_text, evidence)` -- Mark one goal achieved from evidence; return True when found.
- `GoalTracker.goal_met` (method) `modules/goals.py:140` `def goal_met(self, opt_in)` -- End the whole task; requires explicit opt-in (default unbound).
- `GoalTracker.all_achieved` (method) `modules/goals.py:148` `def all_achieved(self)` -- Return True when every goal is achieved.
- `GoalTracker.open_goals` (method) `modules/goals.py:152` `def open_goals(self)` -- Return goals still open.

## modules/gpo_abuse.py
Imported by: `cli/commands/active_directory.py`
- `GPOAbuseEngine.__init__` (method) `modules/gpo_abuse.py:118` `def __init__(self, domain, dc_ip)`
- `GPOAbuseEngine.parse_gpo_list` (method) `modules/gpo_abuse.py:124` `def parse_gpo_list(self, raw_gpo_output)` -- Parse Get-GPO or ldapsearch output for GPO information.
- `GPOAbuseEngine.parse_bloodhound_gpos` (method) `modules/gpo_abuse.py:160` `def parse_bloodhound_gpos(self, bloodhound_nodes)` -- Parse BloodHound GPO nodes for abusable policies.
- `GPOAbuseEngine.plan_scheduled_task` (method) `modules/gpo_abuse.py:182` `def plan_scheduled_task(self, gpo, command, task_name)` -- Plan a GPO-backed scheduled task for immediate code execution.
- `GPOAbuseEngine.plan_startup_script` (method) `modules/gpo_abuse.py:208` `def plan_startup_script(self, gpo, script_content, script_name)` -- Plan a GPO startup script for persistence via SYSVOL.
- `GPOAbuseEngine.plan_logon_script` (method) `modules/gpo_abuse.py:238` `def plan_logon_script(self, gpo, command)` -- Plan a GPO user logon script for user-triggered code execution.
- `GPOAbuseEngine.plan_local_admin_addition` (method) `modules/gpo_abuse.py:266` `def plan_local_admin_addition(self, gpo, username, group)` -- Plan adding a user to the local Administrators group via GPO preferences.
- `GPOAbuseEngine.plan_wmi_filter_abuse` (method) `modules/gpo_abuse.py:293` `def plan_wmi_filter_abuse(self, gpo, wmi_query)` -- Plan WMI filter abuse for targeted GPO scope control.
- `GPOAbuseEngine.plan_registry_preference` (method) `modules/gpo_abuse.py:322` `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` -- Plan a registry modification via GPO preferences.
- `GPOAbuseEngine.plan_service_installation` (method) `modules/gpo_abuse.py:356` `def plan_service_installation(self, gpo, service_name, binary_path)` -- Plan a service installation via GPO for SYSTEM-level persistence.
- `GPOAbuseEngine.generate_all_plans` (method) `modules/gpo_abuse.py:382` `def generate_all_plans(self, command, username)` -- Generate all abuse plans for the discovered GPOs.
- `GPOAbuseEngine.detect_risky_gpos` (method) `modules/gpo_abuse.py:406` `def detect_risky_gpos(self)` -- Identify GPOs with risky configurations for post-compromise cleanup.
- `GPOAbuseEngine.summary` (method) `modules/gpo_abuse.py:434` `def summary(self)` -- Return a summary of GPO abuse capabilities.

## modules/gui_askpass.sh
- `has` (function) `modules/gui_askpass.sh:22` -- ── helpers ───────────────────────────────────────────────────────────────────
- `try_zenity` (function) `modules/gui_askpass.sh:24`
- `try_yad` (function) `modules/gui_askpass.sh:28`
- `try_ssh_askpass` (function) `modules/gui_askpass.sh:33`
- `try_kdialog` (function) `modules/gui_askpass.sh:40`

## modules/gym_registry.py
Depends on: `core/logging.py`, `modules/world_model.py`
Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`
- `slugify` (function) `modules/gym_registry.py:92` `def slugify(value)` -- Return a safe gym identifier.
- `validate_definition` (function) `modules/gym_registry.py:110` `def validate_definition(data, filename)` -- Validate one gym definition mapping.
- `definition_path` (function) `modules/gym_registry.py:155` `def definition_path(gym_id, directory)` -- Resolve one gym YAML file inside the gyms directory.
- `load_definitions` (function) `modules/gym_registry.py:207` `def load_definitions(directory)` -- Load every valid gym definition.
- `scan_definitions` (function) `modules/gym_registry.py:239` `def scan_definitions(directory)` -- Return one row per YAML file, including invalid files.
- `create_definition` (function) `modules/gym_registry.py:300` `def create_definition(gym_id)` -- Create one gym definition YAML.
- `update_definition_yaml` (function) `modules/gym_registry.py:369` `def update_definition_yaml(gym_id, text, directory)` -- Parse, validate and atomically rewrite one definition.
- `delete_definition` (function) `modules/gym_registry.py:402` `def delete_definition(gym_id, directory)` -- Delete one definition unless it has active runs.
- `normalize_operator` (function) `modules/gym_registry.py:495` `def normalize_operator(value)` -- Return a bounded operator label.
- `read_state` (function) `modules/gym_registry.py:501` `def read_state()` -- Read the persistent gym state from the world model.
- `write_state` (function) `modules/gym_registry.py:520` `def write_state(state)` -- Persist one state document to the world model.
- `start_run` (function) `modules/gym_registry.py:579` `def start_run(challenge_id, definitions)` -- Start one run and persist it.
- `get_active_runs` (function) `modules/gym_registry.py:637` `def get_active_runs(selector, operator)` -- Return active runs, enriched with elapsed time.
- `select_run` (function) `modules/gym_registry.py:663` `def select_run(selector)` -- Resolve one active run.
- `stop_runs` (function) `modules/gym_registry.py:695` `def stop_runs(selector)` -- Stop one or every active run.
- `pop_run` (function) `modules/gym_registry.py:724` `def pop_run(selector)` -- Resolve and remove one run, returning its final state.
- `state_summary` (function) `modules/gym_registry.py:751` `def state_summary()` -- Return counters used by status output and the TUI.
- `new_run_token` (function) `modules/gym_registry.py:761` `def new_run_token()` -- Return an unguessable token for external integrations.

## modules/hash_cracker.py
Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`
- `HashCracker.__init__` (method) `modules/hash_cracker.py:164` `def __init__(self, wordlist, rules, use_hashcat, timeout)`
- `HashCracker.identify` (method) `modules/hash_cracker.py:186` `def identify(self, line)` -- Identify the hash type of a single line.
- `HashCracker.identify_file` (method) `modules/hash_cracker.py:273` `def identify_file(self, filepath)` -- Parse a hash file and group hashes by type.
- `HashCracker.crack_hash` (method) `modules/hash_cracker.py:295` `def crack_hash(self, hash_value, hash_type, wordlist)` -- Attempt to crack a single hash.
- `HashCracker.crack_file` (method) `modules/hash_cracker.py:349` `def crack_file(self, filepath, wordlist, hash_types)` -- Crack all hashes in a file.
- `HashCracker.import_to_db` (method) `modules/hash_cracker.py:405` `def import_to_db(self, results, rhost, workspace_name)` -- Import cracked results into the LazyOwnDB credentials table.
- `crack_secretsdump_output` (function) `modules/hash_cracker.py:695` `def crack_secretsdump_output(filepath, wordlist, rhost)` -- Convenience function: crack a secretsdump output file and import results.

## modules/hive_invoke.py
Depends on: `modules/toposwarm_bridge.py`
- `main` (function) `modules/hive_invoke.py:255` `def main(argv)`

## modules/hostdiscover.sh
- `extract_ips_from_arp` (function) `modules/hostdiscover.sh:21`
- `extract_listening_ips_from_netstat` (function) `modules/hostdiscover.sh:26`

## modules/ia_code_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `CodeAnalyzer.__init__` (method) `modules/ia_code_analysis.py:33` `def __init__(self, mode)`
- `CodeAnalyzer.analyze_directory` (method) `modules/ia_code_analysis.py:37` `def analyze_directory(self, directory)` -- Recursively analyzes all source code files in the specified directory.
- `CodeAnalyzer.analyze_code_file` (method) `modules/ia_code_analysis.py:49` `def analyze_code_file(self, file_path)` -- Analyzes the content of the source code file.
- `analyze_with_deepseek` (function) `modules/ia_code_analysis.py:66` `def analyze_with_deepseek(code_content, file_path, mode)` -- Sends the code content to DeepSeek for analysis.
- `save_results_to_json` (function) `modules/ia_code_analysis.py:123` `def save_results_to_json(results, file_path)` -- Saves the analysis results to JSON files.
- `start_analysis` (function) `modules/ia_code_analysis.py:169` `def start_analysis(code_dir, mode)` -- Starts the analysis of the specified code directory.
- `parse_args` (function) `modules/ia_code_analysis.py:178` `def parse_args()`

## modules/ia_logs_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `LogFileHandler.__init__` (method) `modules/ia_logs_analysis.py:59` `def __init__(self, mode)`
- `LogFileHandler.on_modified` (method) `modules/ia_logs_analysis.py:64` `def on_modified(self, event)` -- Triggered when a log file is modified.
- `LogFileHandler.analyze_log_file` (method) `modules/ia_logs_analysis.py:75` `def analyze_log_file(self, file_path)` -- Analyzes the content of the modified log file.
- `analyze_with_deepseek` (function) `modules/ia_logs_analysis.py:94` `def analyze_with_deepseek(log_content, mode)` -- Sends log content to DeepSeek for advanced analysis.
- `start_monitoring` (function) `modules/ia_logs_analysis.py:147` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/ia_logs_analysis.py:168` `def parse_args()`

## modules/ia_network_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `analyze_with_deepseek` (function) `modules/ia_network_analysis.py:39` `def analyze_with_deepseek(packet_info, mode)` -- Envía la información del paquete a DeepSeek para análisis avanzado.
- `packet_callback` (function) `modules/ia_network_analysis.py:91` `def packet_callback(packet, mode)` -- Callback para procesar cada paquete capturado.
- `start_monitoring` (function) `modules/ia_network_analysis.py:130` `def start_monitoring(interface, timeout, mode)` -- Inicia el monitoreo del tráfico de red.
- `parse_args` (function) `modules/ia_network_analysis.py:154` `def parse_args()`

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
- `get_exporter` (function) `modules/integrations/misp_export.py:469` `def get_exporter()` -- Return the module-level MISPExporter singleton.

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
- `get_bridge` (function) `modules/integrations/nuclei_bridge.py:443` `def get_bridge()` -- Return the module-level NucleiBridge singleton.
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
- `get_client` (function) `modules/integrations/searchsploit.py:333` `def get_client()` -- Return the module-level SearchsploitClient singleton.
- `search_cve` (function) `modules/integrations/searchsploit.py:341` `def search_cve(cve_id)` -- Module-level convenience: search by CVE id.
- `search_service` (function) `modules/integrations/searchsploit.py:346` `def search_service(name, version)` -- Module-level convenience: search by service name and version.

## modules/intel_fusion.py
Depends on: `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`
Imported by: `lazyc2.py`, `modules/attack_surface3d.py`, `modules/sinks/intel_graph.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_intel_fusion.py`
- `node_id` (function) `modules/intel_fusion.py:106` `def node_id(kind, value)` -- Deterministic node id from kind + normalized value.
- `build_intel_graph` (function) `modules/intel_fusion.py:176` `def build_intel_graph(sessions_dir, est_cap)` -- Fuse all session artefacts into one C2-centred intel graph.
- `add_node` (function) `modules/intel_fusion.py:183` `def add_node(kind, value, label)` -- Insert node or merge extra fields into the existing one.
- `add_edge` (function) `modules/intel_fusion.py:197` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation.
- `tag_source` (function) `modules/intel_fusion.py:205` `def tag_source(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `group_colors` (function) `modules/intel_fusion.py:512` `def group_colors(graph)` -- Stable colors for layer/language groupings (ReadMenator contract).
- `page_settings` (function) `modules/intel_fusion.py:528` `def page_settings(graph)` -- Explorer page settings with ReadMenator physics sizes (exact values).
- `build_analytics` (function) `modules/intel_fusion.py:585` `def build_analytics(graph, summary)` -- Side-panel analytics (attribution funnel + intel summary).
- `build_bundle_payload` (function) `modules/intel_fusion.py:659` `def build_bundle_payload(graph)` -- Derive the circular/spherical bundle payload from a fused graph.
- `bundle_settings` (function) `modules/intel_fusion.py:769` `def bundle_settings(graph)` -- Bundle page settings with ReadMenator sizes (exact values).
- `assign_layout` (function) `modules/intel_fusion.py:800` `def assign_layout(graph, mode)` -- Attach x/y/z for radial/spherical modes; force modes stay free.
- `write_summary` (function) `modules/intel_fusion.py:865` `def write_summary(graph, sessions_dir)` -- Score host exposure and suggest intents for the autonomous planner.

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
- `get_intelligence_engine` (function) `modules/intelligence_engine.py:931` `def get_intelligence_engine(config)` -- Return the module-level singleton IntelligenceEngine.

## modules/intercept.py
Depends on: `cli/commands/enum.py`
Imported by: `cli/commands/daemon_ctl.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `InterceptRule.matches` (method) `modules/intercept.py:68` `def matches(self, tool, command)` -- Return True when this rule matches the tool call surface.
- `builtin_rules` (function) `modules/intercept.py:101` `def builtin_rules()` -- Return the default destructive and exfiltration guard rules.
- `scope_blocked` (function) `modules/intercept.py:131` `def scope_blocked(target)` -- Return the matching global scope suffix or empty (LAZY parity).
- `observe_post_tool` (function) `modules/intercept.py:144` `def observe_post_tool(output)` -- Classify post-execution output (LAZY Guard.postToolUse parity).
- `Interceptor.__init__` (method) `modules/intercept.py:157` `def __init__(self, rules, ask_timeout_sec, timeout_action)` -- Initialize with rules sorted by descending priority.
- `Interceptor.rules` (method) `modules/intercept.py:172` `def rules(self)` -- Return a copy of the active rule list.
- `Interceptor.add_rule` (method) `modules/intercept.py:177` `def add_rule(self, rule)` -- Add a rule and keep priority ordering.
- `Interceptor.remove_rule` (method) `modules/intercept.py:183` `def remove_rule(self, pattern)` -- Remove the first rule matching pattern text.
- `Interceptor.evaluate` (method) `modules/intercept.py:192` `def evaluate(self, tool, command)` -- Evaluate a tool call and return the verdict.
- `Interceptor.decide` (method) `modules/intercept.py:220` `def decide(self, approval_id, decision)` -- Resolve a pending approval with approve or deny.
- `Interceptor.pending_approvals` (method) `modules/intercept.py:234` `def pending_approvals(self)` -- List unresolved approvals, expiring timed-out ones per policy.
- `Interceptor.approval_status` (method) `modules/intercept.py:249` `def approval_status(self, approval_id)` -- Fetch a single approval record by id.
- `Guard.__init__` (method) `modules/intercept.py:258` `def __init__(self, interceptor)` -- Initialize audit log with an optional interceptor.
- `Guard.interceptor` (method) `modules/intercept.py:266` `def interceptor(self)` -- Expose the underlying interceptor.
- `Guard.check` (method) `modules/intercept.py:270` `def check(self, tool, command)` -- Audit the call then evaluate intercept rules (trace id kept).
- `Guard.observe` (method) `modules/intercept.py:282` `def observe(self, output, source)` -- Classify output and attribute blocked/error counters.
- `Guard.record_failure` (method) `modules/intercept.py:291` `def record_failure(self, source)` -- Attribute a post-execution failure to a source.
- `Guard.audit_log` (method) `modules/intercept.py:296` `def audit_log(self, limit)` -- Return the most recent audit entries.
- `Guard.attribution` (method) `modules/intercept.py:301` `def attribution(self)` -- Return failure attribution counters.

## modules/iptables_portforward.sh
- `display_usage` (function) `modules/iptables_portforward.sh:29`

## modules/jsonl_tail.py
Imported by: `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_runner.py`
- `JsonlTail.__init__` (method) `modules/jsonl_tail.py:17` `def __init__(self, path)` -- Bind the tail to one file path.
- `JsonlTail.read_new` (method) `modules/jsonl_tail.py:22` `def read_new(self, limit)` -- Return new complete records since the last call.

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
- `priority` (function) `modules/kerberoasting.py:172` `def priority(target)`
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
Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazy_cli_bridge.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`
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
- `KillChain.advance_phase` (method) `modules/killchain.py:251` `def advance_phase(new_phase, world_model_path, host)` -- Advance the kill-chain phase for connected surfaces.
- `KillChain.get_progress` (method) `modules/killchain.py:328` `def get_progress(world_model_path)` -- Return the current kill-chain progress as a list of status objects.
- `KillChain.compact_progress` (method) `modules/killchain.py:377` `def compact_progress(current_phase, phases_entered)` -- Return a compact single-line progress indicator ``[R>E>X>P>L]``.
- `KillChain.phases_for_display` (method) `modules/killchain.py:397` `def phases_for_display()` -- Return an ordered ``(key, label, hex_color)`` triple for every phase.
- `KillChain.phase_index` (method) `modules/killchain.py:408` `def phase_index(phase)` -- Return the zero-based index of a canonical phase.
- `KillChain.snapshot` (method) `modules/killchain.py:413` `def snapshot(world_model_path)` -- Return a single, render-agnostic snapshot of the whole kill-chain.
- `get_killchain` (function) `modules/killchain.py:453` `def get_killchain()` -- Return the ``KillChain`` class as a module-level entry point.

## modules/kivi.py
- `ReverseShellApp.build` (method) `modules/kivi.py:12` `def build(self)`
- `ReverseShellApp.connect_to_server` (method) `modules/kivi.py:27` `def connect_to_server(self, instance)`

## modules/lazy_agent.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`
- `model_timeout_sec` (function) `modules/lazy_agent.py:41` `def model_timeout_sec()` -- Return the hard per-turn model timeout from configuration.
- `tool_calling_enabled` (function) `modules/lazy_agent.py:57` `def tool_calling_enabled()` -- Return whether agentic tool calling is enabled by configuration.
- `max_iterations` (function) `modules/lazy_agent.py:72` `def max_iterations()` -- Return the bounded agent step budget from configuration.
- `resolve_agentic_model` (function) `modules/lazy_agent.py:83` `def resolve_agentic_model(exclude)` -- Return a raw tool-calling backend for the best pool member, or None.
- `ObservableAgentRunner.__init__` (method) `modules/lazy_agent.py:148` `def __init__(self, model, system_prompt, max_iterations, on_event)` -- Bind the model and the optional event sink (kind, name, text).
- `ObservableAgentRunner.run` (method) `modules/lazy_agent.py:168` `def run(self, user_input)` -- Base loop plus final-turn persistence for true resume.
- `ConversationStore.__init__` (method) `modules/lazy_agent.py:264` `def __init__(self, task_id)` -- Bind the conversation store for one task (``main`` when empty).
- `ConversationStore.intent_messages` (method) `modules/lazy_agent.py:273` `def intent_messages(self, intent_id)` -- Return the stored messages for one intent (resume seed).
- `ConversationStore.save_intent` (method) `modules/lazy_agent.py:278` `def save_intent(self, intent_id, messages)` -- Persist the tail of one intent conversation.
- `ConversationStore.session` (method) `modules/lazy_agent.py:287` `def session(self, session_id)` -- Return one main-agent session payload (empty when unknown).
- `ConversationStore.sessions` (method) `modules/lazy_agent.py:291` `def sessions(self)` -- List main-agent sessions with title, message count and age.
- `ConversationStore.save_session` (method) `modules/lazy_agent.py:305` `def save_session(self, session_id, messages, title)` -- Persist one main-agent session conversation tail.
- `ConversationStore.reset_intents` (method) `modules/lazy_agent.py:315` `def reset_intents(self)` -- Drop every stored intent conversation (fresh agent start).
- `register_tools` (function) `modules/lazy_agent.py:322` `def register_tools(runner, specs)` -- Register tool specs (name, description, func, parameters, required).
- `run_worker_session` (function) `modules/lazy_agent.py:335` `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` -- Run one agentic intent attempt with resume seeding.
- `run_main_session` (function) `modules/lazy_agent.py:374` `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` -- Run one main-agent turn, resuming the stored session conversation.
- `run_external_opencode` (function) `modules/lazy_agent.py:396` `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` -- Run one headless ``opencode run`` task with MCP tooling.
- `run_external_hermes` (function) `modules/lazy_agent.py:472` `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` -- Run one detached ``hermes chat --oneshot`` task.

## modules/lazy_bridge.py
Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_lazy_loop.py`
- `lazy_tasks` (function) `modules/lazy_bridge.py:88` `def lazy_tasks()` -- Load LAZY task registry.
- `lazy_assets` (function) `modules/lazy_bridge.py:99` `def lazy_assets()` -- Load LAZY asset nodes.
- `lazy_graph` (function) `modules/lazy_bridge.py:110` `def lazy_graph(task_id)` -- Load experiment graph for a task.
- `lazy_activity` (function) `modules/lazy_bridge.py:123` `def lazy_activity(task_id)` -- Load activity transcript for a task.
- `lazy_traffic` (function) `modules/lazy_bridge.py:135` `def lazy_traffic(task_id)` -- Load traffic log for a task.
- `lazy_guard_audit` (function) `modules/lazy_bridge.py:147` `def lazy_guard_audit(task_id)` -- Load guard audit for a task.
- `bridge_status` (function) `modules/lazy_bridge.py:159` `def bridge_status()` -- Summarize LAZY universe and last sync cursor.
- `pull_to_world_model` (function) `modules/lazy_bridge.py:206` `def pull_to_world_model()` -- Sync LAZY graphs and assets into LazyOwn world model.
- `pull_to_objectives` (function) `modules/lazy_bridge.py:251` `def pull_to_objectives()` -- Inject open LAZY tasks as LazyOwn objectives without duplicates.
- `pull_findings_to_lifecycle` (function) `modules/lazy_bridge.py:286` `def pull_findings_to_lifecycle()` -- Confirm LAZY finding nodes in LazyOwn finding lifecycle.
- `pull_traffic_to_recorder` (function) `modules/lazy_bridge.py:361` `def pull_traffic_to_recorder(progress)` -- Mirror new LAZY traffic rows into the LazyOwn recorder index.
- `push_objective_to_lazy` (function) `modules/lazy_bridge.py:429` `def push_objective_to_lazy(goal, scope)` -- Export a LazyOwn objective as an LAZY-compatible task draft.
- `push_tasks_to_c2` (function) `modules/lazy_bridge.py:454` `def push_tasks_to_c2(only)` -- Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).
- `sync_all` (function) `modules/lazy_bridge.py:519` `def sync_all(progress)` -- Run full bidirectional pull plus lifecycle, traffic and board mirror.

## modules/lazy_cli_bridge.py
Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`
- `cli_verbs` (function) `modules/lazy_cli_bridge.py:106` `def cli_verbs()` -- Return every discovered shell verb, cached by source mtime.
- `is_cli_verb` (function) `modules/lazy_cli_bridge.py:125` `def is_cli_verb(name)` -- Return True when name is a real shell command.
- `phase_for` (function) `modules/lazy_cli_bridge.py:131` `def phase_for(verb)` -- Map a verb to its kill-chain phase via keyword affinity.
- `risk_for` (function) `modules/lazy_cli_bridge.py:140` `def risk_for(verb)` -- Classify a verb as safe, exploit or high risk.
- `needs_target_for` (function) `modules/lazy_cli_bridge.py:150` `def needs_target_for(verb)` -- Return whether the verb usually carries a target argument.
- `build_cli_command` (function) `modules/lazy_cli_bridge.py:158` `def build_cli_command(verb, target)` -- Build a shell line for any CLI verb bound to target.
- `search_cli_verbs` (function) `modules/lazy_cli_bridge.py:185` `def search_cli_verbs(query, phase, limit)` -- Search the full CLI catalog by keyword and phase.
- `cli_catalog_for_phase` (function) `modules/lazy_cli_bridge.py:211` `def cli_catalog_for_phase(phase, limit)` -- Return a compact verb list for LLM prompt injection.
- `catalog_cli_for_phase` (function) `modules/lazy_cli_bridge.py:219` `def catalog_cli_for_phase(limit)` -- Return enabled catalog commands for the current kill-chain phase.
- `full_cli_enabled` (function) `modules/lazy_cli_bridge.py:253` `def full_cli_enabled()` -- Return whether the loop may route any CLI verb.
- `set_full_cli` (function) `modules/lazy_cli_bridge.py:276` `def set_full_cli(enabled)` -- Persist the full-CLI routing flag and return the new value.

## modules/lazy_installer.py
Depends on: `core/config.py`, `modules/auto_registry.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`
- `installer_enabled` (function) `modules/lazy_installer.py:41` `def installer_enabled()` -- Return whether the loop may resolve install intents.
- `set_installer_enabled` (function) `modules/lazy_installer.py:58` `def set_installer_enabled(enabled)` -- Persist the installer flag and return the stored value.
- `install_command_for` (function) `modules/lazy_installer.py:70` `def install_command_for(tool)` -- Return the allowlisted install recipe for one tool, or None.
- `intent_for` (function) `modules/lazy_installer.py:75` `def intent_for(tool)` -- Build the canonical install intent summary for one tool.
- `tool_from_intent` (function) `modules/lazy_installer.py:80` `def tool_from_intent(text)` -- Extract the tool name from an install intent, else empty string.
- `steps_for_install` (function) `modules/lazy_installer.py:88` `def steps_for_install(text)` -- Resolve an install intent to its recipe, or None.

## modules/lazy_intel.py
Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/world_model.py`, `utils.py`
Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`
- `infer_source` (function) `modules/lazy_intel.py:79` `def infer_source(command, intent_text)` -- Classify where a resolved step likely came from.
- `describe_command` (function) `modules/lazy_intel.py:105` `def describe_command(command)` -- Describe a command with phase and risk.
- `record_routing_decision` (function) `modules/lazy_intel.py:120` `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `record_routing_outcome` (function) `modules/lazy_intel.py:160` `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `read_decisions` (function) `modules/lazy_intel.py:202` `def read_decisions(task_id, limit)` -- Read routing records, optionally filtered by task.
- `mask_configured` (function) `modules/lazy_intel.py:228` `def mask_configured(text)` -- Mask only operator-configured credential values in live text.
- `stack_signature` (function) `modules/lazy_intel.py:254` `def stack_signature(assets)` -- Fingerprint the target stack from service assets.
- `fuse_routing_decisions` (function) `modules/lazy_intel.py:285` `def fuse_routing_decisions(task_id)` -- Fuse routing records into the world model as host notes.
- `export_spans` (function) `modules/lazy_intel.py:324` `def export_spans(task_id, out)` -- Export activity records as trace spans for observability.


Next: [API_p13.md](API_p13.md)
