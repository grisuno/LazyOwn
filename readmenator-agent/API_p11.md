# API (page 11 of 24)
Previous: [API_p10.md](API_p10.md)

## modules/custom_tools.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/notify.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `tests/test_lazy_loop.py`
- `add_tool` (function) `modules/custom_tools.py:52` `def add_tool(name, kind, target, description, method, body, timeout, trigger)` -- Register or replace one custom tool.
- `remove_tool` (function) `modules/custom_tools.py:97` `def remove_tool(name)` -- Delete a tool by name.
- `list_tools` (function) `modules/custom_tools.py:109` `def list_tools()` -- Return every registered tool.
- `get_tool` (function) `modules/custom_tools.py:114` `def get_tool(name)` -- Find one tool by name.
- `match_tools` (function) `modules/custom_tools.py:128` `def match_tools(text, limit)` -- Rank tools whose name/description/trigger keywords appear in the text.
- `run_tool` (function) `modules/custom_tools.py:151` `def run_tool(name, arg, on_output)` -- Execute one custom tool and return its transcript.

## modules/cve_matcher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `CVEMatcher.__init__` (method) `modules/cve_matcher.py:70` `def __init__(self, api_key, cache_dir)`
- `CVEMatcher.search` (method) `modules/cve_matcher.py:82` `def search(self)` -- Search CVEs by product / version keywords.
- `CVEMatcher.search_by_cpe` (method) `modules/cve_matcher.py:89` `def search_by_cpe(self, cpe_name, max_results)` -- Search CVEs by CPE 2.3 string.
- `get_matcher` (function) `modules/cve_matcher.py:198` `def get_matcher()` -- Return (or create) the module-level singleton CVEMatcher.
- `search` (function) `modules/cve_matcher.py:206` `def search(product, version, max_results)` -- Module-level convenience wrapper.

## modules/dacl_abuse.py
Imported by: `cli/commands/active_directory.py`
- `DACLAbuseEngine.__init__` (method) `modules/dacl_abuse.py:136` `def __init__(self, domain, domain_sid, acl_data)`
- `DACLAbuseEngine.parse_bloodhound_acls` (method) `modules/dacl_abuse.py:143` `def parse_bloodhound_acls(self, edges)` -- Parse BloodHound edge data to extract exploitable ACLs.
- `DACLAbuseEngine.parse_raw_aces` (method) `modules/dacl_abuse.py:182` `def parse_raw_aces(self, raw_nthashes)` -- Parse raw ACE data from ntSecurityDescriptor parsing.
- `DACLAbuseEngine.compute_attack_chains` (method) `modules/dacl_abuse.py:224` `def compute_attack_chains(self)` -- Generate exploitation plans for all discovered ACL targets.
- `DACLAbuseEngine.adminsdholder_abuse_plan` (method) `modules/dacl_abuse.py:291` `def adminsdholder_abuse_plan(self, target_sid)` -- Generate an AdminSDHolder abuse plan.
- `DACLAbuseEngine.dcsync_rights_assignment_plan` (method) `modules/dacl_abuse.py:318` `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` -- Generate a DCSync rights assignment plan.
- `DACLAbuseEngine.owner_takeover_plan` (method) `modules/dacl_abuse.py:348` `def owner_takeover_plan(self, target_dn, attacker_sid)` -- Generate an ownership takeover plan.
- `DACLAbuseEngine.summary` (method) `modules/dacl_abuse.py:418` `def summary(self)` -- Return a summary of all DACL/SACL abuse findings.

## modules/dashboard_bp.py
Imported by: `lazyc2.py`, `tests/test_core_modules.py`, `tests/test_dashboard_routes.py`
- `dashboard_index` (function) `modules/dashboard_bp.py:778` `def dashboard_index()` -- Render the main SOC dashboard HTML page.
- `dashboard_api_data` (function) `modules/dashboard_bp.py:784` `def dashboard_api_data()` -- JSON snapshot of all dashboard data.
- `dashboard_loot` (function) `modules/dashboard_bp.py:902` `def dashboard_loot()` -- Render the loot browser: captured credentials, hashes and files.
- `dashboard_timeline` (function) `modules/dashboard_bp.py:1017` `def dashboard_timeline()` -- Render the campaign timeline: commands and events, newest first.

## modules/dashboard_engine.py
Imported by: `cli/commands/pwn.py`, `modules/rich_tui.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`
- `DashboardEngine.__init__` (method) `modules/dashboard_engine.py:139` `def __init__(self, world_model)`
- `DashboardEngine.set_world_model` (method) `modules/dashboard_engine.py:148` `def set_world_model(self, model)`
- `DashboardEngine.set_exploit_recommender` (method) `modules/dashboard_engine.py:151` `def set_exploit_recommender(self, recommender)`
- `DashboardEngine.set_auto_pivot` (method) `modules/dashboard_engine.py:154` `def set_auto_pivot(self, pivot)`
- `DashboardEngine.set_evasion_engine` (method) `modules/dashboard_engine.py:157` `def set_evasion_engine(self, evasion)`
- `DashboardEngine.build_snapshot` (method) `modules/dashboard_engine.py:160` `def build_snapshot(self)` -- Build a complete dashboard snapshot from all data sources.
- `DashboardEngine.render_text_map` (method) `modules/dashboard_engine.py:276` `def render_text_map(self, snapshot)` -- Render a text-based network map from a dashboard snapshot.
- `DashboardEngine.render_ascii_topology` (method) `modules/dashboard_engine.py:358` `def render_ascii_topology(self, snapshot)` -- Render an ASCII-art topology tree from a snapshot.
- `DashboardEngine.export_json` (method) `modules/dashboard_engine.py:408` `def export_json(self, snapshot)` -- Export dashboard snapshot as JSON string.
- `DashboardEngine.persist_snapshot` (method) `modules/dashboard_engine.py:421` `def persist_snapshot(self, snapshot)` -- Persist dashboard snapshot to sessions/dashboard_snapshot.json.
- `DashboardEngine.format_for_cli` (method) `modules/dashboard_engine.py:438` `def format_for_cli(self, snapshot)` -- Compact single-line status for CLI prompt integration.

## modules/db.py
Depends on: `core/config.py`, `core/crypto.py`, `core/logging.py`
Imported by: `cli/commands/campaign.py`, `cli/commands/collaboration.py`, `cli/commands/database.py`, `lazyc2/blueprints/api_v1.py`, `modules/autonomous_exploit_engine.py`, `modules/estorides_importer.py`, `modules/hash_cracker.py`, `modules/integrations/nuclei_parser.py`, `modules/opsec_scorer.py`, `modules/sinks/campaign_db.py`, `modules/state_manager.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_api_v1.py`, `tests/test_autonomous_ops.py`, `tests/test_daemon_loop.py`, `tests/test_db.py`, `tests/test_mutation_verification.py`, `tests/test_security_hardening.py`
- `LazyOwnDB.__init__` (method) `modules/db.py:159` `def __init__(self, db_path)`
- `LazyOwnDB.db_path` (method) `modules/db.py:182` `def db_path(self)` -- Path to the SQLite database file.
- `LazyOwnDB.migration_status` (method) `modules/db.py:222` `def migration_status(self)` -- Return the current and latest migration versions.
- `LazyOwnDB.workspace_create` (method) `modules/db.py:292` `def workspace_create(self, name, description)` -- Create a new workspace.
- `LazyOwnDB.workspace_list` (method) `modules/db.py:307` `def workspace_list(self)` -- Return all workspaces as dicts.
- `LazyOwnDB.workspace_get` (method) `modules/db.py:313` `def workspace_get(self, name)` -- Get a workspace by name, or None.
- `LazyOwnDB.default_workspace` (method) `modules/db.py:320` `def default_workspace(self, name)` -- Return the id of the named workspace, creating it when absent.
- `LazyOwnDB.workspace_delete` (method) `modules/db.py:333` `def workspace_delete(self, name)` -- Delete a workspace and all its data.
- `LazyOwnDB.host_add` (method) `modules/db.py:357` `def host_add(self, workspace_id, address, mac, hostname, os, state)` -- Add or update a host.
- `LazyOwnDB.host_delete` (method) `modules/db.py:390` `def host_delete(self, host_id)` -- Delete a host and its related data.
- `LazyOwnDB.host_list` (method) `modules/db.py:401` `def host_list(self, workspace_id)` -- List all hosts in a workspace.
- `LazyOwnDB.host_find` (method) `modules/db.py:410` `def host_find(self, workspace_id, query)` -- Search hosts by address, hostname, or os.
- `LazyOwnDB.service_add` (method) `modules/db.py:427` `def service_add(self, host_id, port, protocol, state, name, product, version)` -- Add a service to a host.
- `LazyOwnDB.service_list` (method) `modules/db.py:447` `def service_list(self, host_id)` -- List all services on a host.
- `LazyOwnDB.vuln_add` (method) `modules/db.py:460` `def vuln_add(self, host_id, name, severity, description, refs)` -- Add a vulnerability to a host.
- `LazyOwnDB.vuln_get` (method) `modules/db.py:478` `def vuln_get(self, vuln_id)` -- Return one vuln row with its host address, or None.
- `LazyOwnDB.vuln_update` (method) `modules/db.py:490` `def vuln_update(self, vuln_id, refs, severity, description)` -- Update mutable vuln fields; returns True when a row changed.
- `LazyOwnDB.vuln_list` (method) `modules/db.py:528` `def vuln_list(self, workspace_id, severity)` -- List vulns in workspace, optionally filtered by severity.
- `LazyOwnDB.cred_add` (method) `modules/db.py:557` `def cred_add(self, host_id, username, password, realm, cred_type, origin)` -- Add a credential (password encrypted at rest).
- `LazyOwnDB.cred_list` (method) `modules/db.py:577` `def cred_list(self, workspace_id)` -- List all creds in workspace (passwords decrypted).
- `LazyOwnDB.loot_add` (method) `modules/db.py:596` `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` -- Add a loot entry.
- `LazyOwnDB.loot_list` (method) `modules/db.py:615` `def loot_list(self, workspace_id)` -- List all loot in workspace.
- `LazyOwnDB.note_add` (method) `modules/db.py:631` `def note_add(self, workspace_id, data, note_type, host_id)` -- Add a note.
- `LazyOwnDB.note_list` (method) `modules/db.py:648` `def note_list(self, workspace_id)` -- List all notes in workspace.
- `LazyOwnDB.import_nmap_xml` (method) `modules/db.py:664` `def import_nmap_xml(self, workspace_id, xml_path)` -- Import an Nmap XML file into the database.
- `LazyOwnDB.export_csv` (method) `modules/db.py:740` `def export_csv(self, table, workspace_id)` -- Export a table to CSV string.
- `LazyOwnDB.status` (method) `modules/db.py:775` `def status(self, workspace_id)` -- Return counts for every entity type in a workspace.
- `LazyOwnDB.close` (method) `modules/db.py:804` `def close(self)` -- Close the database connection for the current thread.
- `get_db` (function) `modules/db.py:821` `def get_db(db_path)` -- Get or create a :class:`LazyOwnDB` instance.

## modules/delegation_attacks.py
Imported by: `cli/commands/active_directory.py`
- `DelegationEnumerator.__init__` (method) `modules/delegation_attacks.py:98` `def __init__(self, domain, raw_ldap_output)`
- `DelegationEnumerator.enumerate_from_uac_flags` (method) `modules/delegation_attacks.py:104` `def enumerate_from_uac_flags(self, accounts)` -- Enumerate delegation targets from parsed account data.
- `DelegationEnumerator.parse_bloodhound_output` (method) `modules/delegation_attacks.py:151` `def parse_bloodhound_output(self, bloodhound_json)` -- Parse BloodHound JSON output for delegation data.
- `DelegationEnumerator.find_unconstrained_targets` (method) `modules/delegation_attacks.py:181` `def find_unconstrained_targets(self)` -- Return all accounts with unconstrained delegation enabled.
- `DelegationEnumerator.find_constrained_targets` (method) `modules/delegation_attacks.py:189` `def find_constrained_targets(self)` -- Return all accounts with constrained delegation configured.
- `DelegationEnumerator.find_rbcd_targets` (method) `modules/delegation_attacks.py:197` `def find_rbcd_targets(self)` -- Return all accounts with RBCD configured.
- `DelegationEnumerator.find_dc_targets` (method) `modules/delegation_attacks.py:205` `def find_dc_targets(self)` -- Return domain controllers with delegation configured.
- `DelegationEnumerator.compute_attack_paths` (method) `modules/delegation_attacks.py:215` `def compute_attack_paths(self)` -- Compute delegation-based attack paths.
- `DelegationEnumerator.summary` (method) `modules/delegation_attacks.py:296` `def summary(self)` -- Return a summary of all delegation findings.

## modules/detailed_search.py
- `obtener_informacion` (function) `modules/detailed_search.py:40` `def obtener_informacion(url)`

## modules/detection_feed.py
Depends on: `core/logging.py`, `modules/detection_oracle.py`
Imported by: `modules/detection_oracle.py`, `tests/test_detection_feed.py`
- `DetectionFeed.__init__` (method) `modules/detection_feed.py:83` `def __init__(self, cache_dir, sources)`
- `DetectionFeed.update_rules` (method) `modules/detection_feed.py:92` `def update_rules(self, source)` -- Download and parse rules from the given source.
- `DetectionFeed.load_cached_rules` (method) `modules/detection_feed.py:246` `def load_cached_rules(self, source)` -- Load previously cached rules from disk.
- `DetectionFeed.adjust_from_feedback` (method) `modules/detection_feed.py:270` `def adjust_from_feedback(self, feedback_file)` -- Adjust rule probabilities based on historical detection feedback.
- `get_feed` (function) `modules/detection_feed.py:326` `def get_feed()` -- Return a module-level :class:`DetectionFeed` singleton.

## modules/detection_oracle.py
Depends on: `core/logging.py`, `modules/detection_feed.py`
Imported by: `modules/auto_purple.py`, `modules/detection_feed.py`, `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`, `tests/test_detection_feed.py`, `tests/test_loop_ai_bridge.py`, `tests/test_moe_rl_swan.py`
- `DetectionAssessment.is_high_risk` (method) `modules/detection_oracle.py:75` `def is_high_risk(self)` -- Return True when detection probability is 70% or higher.
- `DetectionAssessment.is_critical_risk` (method) `modules/detection_oracle.py:80` `def is_critical_risk(self)` -- Return True when detection probability is 90% or higher.
- `IDetectionOracle.assess` (method) `modules/detection_oracle.py:94` `def assess(self, command, args, action_category)` -- Return a full DetectionAssessment for the given action.
- `IDetectionOracle.probability` (method) `modules/detection_oracle.py:103` `def probability(self, command, args, action_category)` -- Return only the probability score in [0.0, 1.0].
- `DetectionOracle.__init__` (method) `modules/detection_oracle.py:332` `def __init__(self, rules, feed)`
- `DetectionOracle.refresh` (method) `modules/detection_oracle.py:336` `def refresh(self)` -- Update rules from the detection feed (if available).
- `DetectionOracle.assess` (method) `modules/detection_oracle.py:371` `def assess(self, command, args, action_category)`
- `DetectionOracle.probability` (method) `modules/detection_oracle.py:392` `def probability(self, command, args, action_category)`
- `get_oracle` (function) `modules/detection_oracle.py:478` `def get_oracle()` -- Return (or create) the module-level singleton DetectionOracle.

## modules/digest.py
Imported by: `modules/lazy_loop.py`, `skills/lazyown_mcp.py`
- `build_engine_digest` (function) `modules/digest.py:20` `def build_engine_digest(task_id, status, rounds, findings, facts, blocks, reaction_backlog)` -- Render the engine-loop markdown digest.
- `write_digest` (function) `modules/digest.py:71` `def write_digest(task_id, body, root)` -- Persist the digest beside the archives; returns the written path.
- `worker_results_digest` (function) `modules/digest.py:82` `def worker_results_digest(rows)` -- Extract displayed step lines and blocked bases from result dicts.

## modules/dns_beacon.py
Depends on: `core/safe_exec.py`
Imported by: `cli/commands/dns_exfil.py`
- `DNSBeacon.__init__` (method) `modules/dns_beacon.py:38` `def __init__(self, domain, dns_server, sleep_seconds, jitter_percent, dns_type, encode_method)`
- `DNSBeacon.check_in` (method) `modules/dns_beacon.py:105` `def check_in(self)` -- Send heartbeat and check for pending commands.
- `DNSBeacon.send_result` (method) `modules/dns_beacon.py:135` `def send_result(self, command, output, exit_code)` -- Send command output via DNS TXT queries.
- `DNSBeacon.run` (method) `modules/dns_beacon.py:171` `def run(self)` -- Main beacon loop: check-in -> execute command -> send result -> sleep.
- `DNSC2Server.__init__` (method) `modules/dns_beacon.py:211` `def __init__(self, domain, log_source, interface)`
- `DNSC2Server.register_beacon` (method) `modules/dns_beacon.py:225` `def register_beacon(self, beacon_id, hostname)` -- Register a new DNS beacon.
- `DNSC2Server.list_beacons` (method) `modules/dns_beacon.py:235` `def list_beacons(self)` -- List all registered DNS beacons.
- `DNSC2Server.send_task` (method) `modules/dns_beacon.py:239` `def send_task(self, beacon_id, command)` -- Queue a command for a DNS beacon.
- `DNSC2Server.process_query_log` (method) `modules/dns_beacon.py:248` `def process_query_log(self, line)` -- Process a single DNS query log line and extract beacon data.
- `DNSC2Server.get_results` (method) `modules/dns_beacon.py:327` `def get_results(self, beacon_id)` -- Get received results for a beacon.

## modules/domain_dominance.py
Depends on: `core/hardening.py`
Imported by: `cli/commands/lateral_migrated.py`, `tests/test_security_alerts_fix.py`
- `DomainDominance.__init__` (method) `modules/domain_dominance.py:103` `def __init__(self)`
- `DomainDominance.get_instance` (method) `modules/domain_dominance.py:110` `def get_instance(cls)`
- `DomainDominance.dominate` (method) `modules/domain_dominance.py:121` `def dominate(self, domain, dc_ip, username, password, ntlm_hash)` -- Execute the full AD dominance kill-chain.
- `DomainDominance.enumerate_domain` (method) `modules/domain_dominance.py:194` `def enumerate_domain(self, domain, dc_ip)` -- Enumerate the target domain topology.
- `DomainDominance.extract_credentials` (method) `modules/domain_dominance.py:227` `def extract_credentials(self, domain_info, known_creds)` -- Extract credentials using the discovered domain topology.
- `DomainDominance.escalate` (method) `modules/domain_dominance.py:260` `def escalate(self, domain_info, stash)` -- Escalate privileges and move laterally through the domain.
- `DomainDominance.persist` (method) `modules/domain_dominance.py:314` `def persist(self, domain_info)` -- Establish persistence mechanisms across the domain.

## modules/dotnet_payload.py
Imported by: `cli/commands/payload_arsenal.py`
- `DotNetPayloadFactory.__init__` (method) `modules/dotnet_payload.py:327` `def __init__(self, output_dir)`
- `DotNetPayloadFactory.list_templates` (method) `modules/dotnet_payload.py:364` `def list_templates()` -- Return available .NET payload template names.
- `DotNetPayloadFactory.generate_source` (method) `modules/dotnet_payload.py:389` `def generate_source(self, config)` -- Generate C# source code from a template.
- `DotNetPayloadFactory.compile` (method) `modules/dotnet_payload.py:403` `def compile(self, config, source_code)` -- Compile C# source to an assembly.
- `DotNetPayloadFactory.generate` (method) `modules/dotnet_payload.py:454` `def generate(self, config)` -- Generate a .NET payload — source code plus optional binary.
- `DotNetPayloadFactory.generate_powershell_reflective` (method) `modules/dotnet_payload.py:481` `def generate_powershell_reflective(self, config)` -- Generate a PowerShell script that reflectively loads a .NET assembly.
- `DotNetPayloadFactory.generate_inline_assembly` (method) `modules/dotnet_payload.py:500` `def generate_inline_assembly(self, config)` -- Generate self-decompiling inline .NET assembly load command.
- `DotNetPayloadFactory.to_format` (method) `modules/dotnet_payload.py:520` `def to_format(self, data, fmt)` -- Convert a payload result to the requested output format.

## modules/dpapi_harvester.py
Imported by: `cli/commands/dpapi.py`
- `DPAPIHarvester.__init__` (method) `modules/dpapi_harvester.py:79` `def __init__(self, sessions_dir, masterkey_path)`
- `DPAPIHarvester.harvest_all` (method) `modules/dpapi_harvester.py:90` `def harvest_all(self)` -- Run all harvesters and return all discovered credentials.
- `DATA_BLOB.export_credentials` (method) `modules/dpapi_harvester.py:367` `def export_credentials(self)` -- Export all harvested credentials to a text file.
- `DATA_BLOB.masterkey_report` (method) `modules/dpapi_harvester.py:386` `def masterkey_report(self)` -- Generate a master key report.

## modules/edr_detector.py
Imported by: `cli/commands/edr_detect.py`
- `EDRDetector.detect_local` (method) `modules/edr_detector.py:202` `def detect_local()` -- Detect EDR products on the local Windows machine.
- `EDRDetector.detect_remote_commands` (method) `modules/edr_detector.py:221` `def detect_remote_commands(remote_type)` -- Generate commands for remote EDR detection.
- `EDRDetector.generate_edr_check_script` (method) `modules/edr_detector.py:440` `def generate_edr_check_script(remote_type)` -- Generate a PowerShell script for comprehensive EDR detection.

## modules/eegg.sh
- `init_board` (function) `modules/eegg.sh:26` -- Inicializa el tablero con las piezas en sus posiciones iniciales
- `show_board` (function) `modules/eegg.sh:40` -- Función para mostrar el tablero
- `move_white_pawns` (function) `modules/eegg.sh:61` -- Movimiento de peones blancos y negros
- `move_black_pawns` (function) `modules/eegg.sh:78`

## modules/emulation_runner.py
Depends on: `core/logging.py`, `modules/apt_playbooks.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/outcome_bus.py`
Imported by: `modules/atomic_exploit_bridge.py`, `modules/playbook_engine.py`, `tests/test_emulation_runner.py`
- `EmulationResult.to_dict` (method) `modules/emulation_runner.py:53` `def to_dict(self)` -- Return a JSON-serializable view.
- `EmulationReport.executed` (method) `modules/emulation_runner.py:81` `def executed(self)` -- Return the number of tests that actually ran.
- `EmulationReport.shell` (method) `modules/emulation_runner.py:86` `def shell(self)` -- Return True when any test produced a shell signal.
- `EmulationReport.to_dict` (method) `modules/emulation_runner.py:90` `def to_dict(self)` -- Return the legacy bridge-shaped mapping plus v2 fields.
- `EmulationRunner.__init__` (method) `modules/emulation_runner.py:108` `def __init__(self, resolver, sessions_dir, shell_opener, remote_exec_fn, playbook_loader, outcome_recorder...` -- Bind optional collaborators; defaults load the shared modules lazily.
- `EmulationRunner.techniques_for_playbook` (method) `modules/emulation_runner.py:182` `def techniques_for_playbook(self, playbook, platform)` -- Return ordered unique technique IDs for one APT playbook.
- `EmulationRunner.run` (method) `modules/emulation_runner.py:202` `def run(self, target, techniques, playbook, platform, lhost, per_technique, include_manual, dry_run, executor...` -- Execute emulation tests and return the staged report.
- `EmulationRunner.run_steps` (method) `modules/emulation_runner.py:321` `def run_steps(self, steps, target, executor, platform, dry_run, source)` -- Execute already-resolved steps through one executor.

## modules/engage_summary.py
Depends on: `cli/recommendation_signals.py`, `modules/enrich.py`, `modules/evidence.py`
Imported by: `skills/unified_orchestrator.py`, `tests/test_engage_summary.py`
- `marker_lines` (function) `modules/engage_summary.py:35` `def marker_lines(text, limit)` -- Extract real log lines (``[+] ... [+]``) dropping panels and bars.
- `full_output` (function) `modules/engage_summary.py:51` `def full_output(step, sessions_dir)` -- Return the full step output from evidence, falling back to the tail.
- `held_scan_ports` (function) `modules/engage_summary.py:64` `def held_scan_ports(target, sessions_dir)` -- Parse held scan XMLs for open ports.
- `detail_for` (function) `modules/engage_summary.py:98` `def detail_for(tool, text, target, sessions_dir)` -- Extract the key facts from one step output for the summary.
- `next_actions` (function) `modules/engage_summary.py:150` `def next_actions(target, sessions_dir, limit)` -- Rank next actions via the unified recommendation engine.
- `render_text` (function) `modules/engage_summary.py:175` `def render_text(engagement_id, target, shell, steps, sessions_dir)` -- Render the console summary with per-step detail lines.
- `render_markdown` (function) `modules/engage_summary.py:210` `def render_markdown(engagement_id, target, shell, steps, next_list, sessions_dir)` -- Render the persisted per-engagement report.
- `write_report` (function) `modules/engage_summary.py:247` `def write_report(engagement_id, target, shell, steps, sessions_dir)` -- Persist the engagement report; return its relative path.

## modules/engagement_hooks.py
Depends on: `core/logging.py`, `modules/collab_bp.py`
Imported by: `modules/event_bus.py`, `modules/pipeline_engine.py`
- `EngagementEvent.now` (method) `modules/engagement_hooks.py:124` `def now(cls, kind, target, message, payload, severity)` -- Construct an event with a fresh id and current UTC timestamp.
- `EngagementEvent.render_line` (method) `modules/engagement_hooks.py:143` `def render_line(self)` -- Return a single-line operator-facing log entry.
- `INotificationSink.name` (method) `modules/engagement_hooks.py:155` `def name(self)` -- Stable channel identifier used for diagnostic logging.
- `INotificationSink.deliver` (method) `modules/engagement_hooks.py:159` `def deliver(self, event)` -- Deliver one event.
- `StreamEventSink.name` (method) `modules/engagement_hooks.py:178` `def name(self)`
- `StreamEventSink.deliver` (method) `modules/engagement_hooks.py:181` `def deliver(self, event)`
- `CollabNotificationSink.name` (method) `modules/engagement_hooks.py:213` `def name(self)`
- `CollabNotificationSink.deliver` (method) `modules/engagement_hooks.py:216` `def deliver(self, event)`
- `_OutboundHTTPSink.name` (method) `modules/engagement_hooks.py:252` `def name(self)`
- `_OutboundHTTPSink.deliver` (method) `modules/engagement_hooks.py:258` `def deliver(self, event)`
- `TelegramNotificationSink.name` (method) `modules/engagement_hooks.py:288` `def name(self)`
- `DiscordNotificationSink.name` (method) `modules/engagement_hooks.py:320` `def name(self)`
- `NotificationBroadcaster.__init__` (method) `modules/engagement_hooks.py:349` `def __init__(self, sinks)`
- `NotificationBroadcaster.default` (method) `modules/engagement_hooks.py:354` `def default(cls)` -- Return a broadcaster with the standard four-sink configuration.
- `NotificationBroadcaster.add` (method) `modules/engagement_hooks.py:365` `def add(self, sink)` -- Register an additional sink at runtime.
- `NotificationBroadcaster.deliver` (method) `modules/engagement_hooks.py:370` `def deliver(self, event)` -- Push event to all sinks.
- `EngagementNarrator.__init__` (method) `modules/engagement_hooks.py:393` `def __init__(self, broadcaster)`
- `EngagementNarrator.narrate` (method) `modules/engagement_hooks.py:400` `def narrate(self, kind, target, message, payload, severity)` -- Write one line + audit record and dispatch to every sink.
- `get_default_narrator` (function) `modules/engagement_hooks.py:482` `def get_default_narrator()` -- Return the process-wide default narrator (lazy singleton).
- `publish_shell_obtained` (function) `modules/engagement_hooks.py:491` `def publish_shell_obtained(client_id, primary_ip, hostname, user, platform, narrator)` -- Single entry point called by lazyc2.py on every beacon check-in.
- `append_approval_record` (function) `modules/engagement_hooks.py:564` `def append_approval_record(record)` -- Append one approval-pending record to sessions/engagement_approvals.jsonl.
- `list_pending_approvals` (function) `modules/engagement_hooks.py:575` `def list_pending_approvals()` -- Return every approval record whose status is still 'pending'.
- `resolve_approval` (function) `modules/engagement_hooks.py:601` `def resolve_approval(approval_id, decision, operator)` -- Append a resolution record for the given approval_id.
- `is_valid_target` (function) `modules/engagement_hooks.py:626` `def is_valid_target(value)` -- Validate that value is a dotted-quad IPv4 or a safe hostname token.

## modules/enrich.py
Imported by: `cli/commands/pwn.py`, `cli/commands/session_ops.py`, `modules/engage_summary.py`, `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`
- `scan_files_for` (function) `modules/enrich.py:40` `def scan_files_for(sessions_dir, target)` -- Return existing scan artefacts for a target.
- `should_rescan` (function) `modules/enrich.py:57` `def should_rescan(sessions_dir, target, fresh_sec)` -- Return True when no fresh scan artefact exists for target.
- `resolve_dns` (function) `modules/enrich.py:73` `def resolve_dns(target, timeout)` -- Resolve A/AAAA for a target with a bounded timeout.
- `fetch_http` (function) `modules/enrich.py:86` `def fetch_http(target, timeout)` -- Fetch HTTP headers for a target without following credentials.
- `EnrichEngine.__init__` (method) `modules/enrich.py:103` `def __init__(self, max_workers)` -- Create the pool and cooldown index.
- `EnrichEngine.submit` (method) `modules/enrich.py:108` `def submit(self, target)` -- Queue DNS+HTTP enrichment unless inside cooldown.
- `EnrichEngine.shutdown` (method) `modules/enrich.py:128` `def shutdown(self, wait)` -- Shut the pool down without blocking the loop by default.
- `shared_engine` (function) `modules/enrich.py:137` `def shared_engine()` -- Return the process-wide enrichment engine (LAZY parity).

## modules/entra_id_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `EntraIDAttackEngine.__init__` (method) `modules/entra_id_attacks.py:92` `def __init__(self, config)`
- `EntraIDAttackEngine.device_code_phish` (method) `modules/entra_id_attacks.py:96` `def device_code_phish(self, scope)` -- Initiate a device code phishing flow.
- `EntraIDAttackEngine.poll_device_code` (method) `modules/entra_id_attacks.py:129` `def poll_device_code(self, device_code, interval, timeout)` -- Poll for device code completion to retrieve tokens.
- `EntraIDAttackEngine.oauth_consent_grant` (method) `modules/entra_id_attacks.py:166` `def oauth_consent_grant(self, redirect_uri)` -- Generate an OAuth consent grant phishing URL.
- `EntraIDAttackEngine.service_principal_credential_theft` (method) `modules/entra_id_attacks.py:203` `def service_principal_credential_theft(self)` -- Plan service principal credential theft via app registration abuse.
- `EntraIDAttackEngine.managed_identity_abuse` (method) `modules/entra_id_attacks.py:235` `def managed_identity_abuse(self, resource)` -- Exploit Azure managed identities from compromised VMs/containers.
- `EntraIDAttackEngine.entra_connect_sync_abuse` (method) `modules/entra_id_attacks.py:266` `def entra_connect_sync_abuse(self)` -- Exploit Entra Connect Sync for on-prem to cloud privilege escalation.
- `EntraIDAttackEngine.conditional_access_bypass` (method) `modules/entra_id_attacks.py:307` `def conditional_access_bypass(self)` -- Techniques for bypassing Entra ID Conditional Access policies.
- `EntraIDAttackEngine.enumerate_tenant` (method) `modules/entra_id_attacks.py:345` `def enumerate_tenant(self)` -- Enumerate tenant information via Graph API.
- `EntraIDAttackEngine.summary` (method) `modules/entra_id_attacks.py:368` `def summary(self)`

## modules/estorides_fusion.py
Imported by: `cli/commands/surface.py`, `modules/attack_surface3d.py`, `modules/intel_fusion.py`, `tests/test_estorides_fusion.py`
- `estorides_checkout` (function) `modules/estorides_fusion.py:48` `def estorides_checkout()` -- Locate the estorides working copy.
- `find_export` (function) `modules/estorides_fusion.py:68` `def find_export(sessions_dir)` -- Find an estorides export, preferring the LazyOwn vocabulary file.
- `run_export` (function) `modules/estorides_fusion.py:84` `def run_export(sessions_dir, cli_path, timeout_sec)` -- Run ``estorides_cli.py graph --export lazyown`` into sessions/.
- `load_export` (function) `modules/estorides_fusion.py:128` `def load_export(path)` -- Load an export in either vocabulary into nodes/edges lists.
- `community_for` (function) `modules/estorides_fusion.py:180` `def community_for(kind, value)` -- Assign a campaign community to a fused entity.
- `merge_estorides` (function) `modules/estorides_fusion.py:187` `def merge_estorides(nodes, edges, est, cap)` -- Fuse estorides entities into graph nodes/edges in place.
- `find_lan_bundle` (function) `modules/estorides_fusion.py:268` `def find_lan_bundle(sessions_dir)` -- Find a LAN bundle deliverable, preferring LazyOwn vocabulary.
- `load_lan_bundle` (function) `modules/estorides_fusion.py:288` `def load_lan_bundle(path)` -- Load a LAN bundle file into nodes/edges lists.
- `split_lan_targets` (function) `modules/estorides_fusion.py:323` `def split_lan_targets(est)` -- Split a LAN payload into intel (all) and attack (hosts) views.

## modules/estorides_importer.py
Depends on: `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/estorides.py`, `modules/intelligence_engine.py`
- `ImportResult.success` (method) `modules/estorides_importer.py:110` `def success(self)`
- `ImportResult.to_dict` (method) `modules/estorides_importer.py:113` `def to_dict(self)`
- `SeedResult.new_assets` (method) `modules/estorides_importer.py:139` `def new_assets(self)`
- `extract_seeds_from_world_model` (function) `modules/estorides_importer.py:143` `def extract_seeds_from_world_model(world_model_path)` -- Extract IPs and domains from world_model.json as estorides seeds.
- `extract_seeds_from_hosts_file` (function) `modules/estorides_importer.py:175` `def extract_seeds_from_hosts_file(path)` -- Extract IPs/domains from hostsdiscovery.txt or similar.
- `extract_seeds_from_db` (function) `modules/estorides_importer.py:203` `def extract_seeds_from_db(db_path)` -- Extract hosts from LazyOwn database.
- `extract_seeds_from_scope` (function) `modules/estorides_importer.py:242` `def extract_seeds_from_scope(scope_entries)` -- Extract scoped IPs/domains from payload.json scope list.
- `run_estorides_discover` (function) `modules/estorides_importer.py:272` `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` -- Run estorides discover on a single seed.
- `run_estorides_run` (function) `modules/estorides_importer.py:332` `def run_estorides_run(query, out_json, timeout)` -- Run estorides run (single fan-out) on a query.
- `EstoridesCaseReader.__init__` (method) `modules/estorides_importer.py:388` `def __init__(self, db_path)`
- `EstoridesCaseReader.available` (method) `modules/estorides_importer.py:393` `def available(self)`
- `EstoridesCaseReader.list_cases` (method) `modules/estorides_importer.py:402` `def list_cases(self, limit)`
- `EstoridesCaseReader.get_entities` (method) `modules/estorides_importer.py:414` `def get_entities(self, case_id, entity_types, limit)` -- Fetch entities from the case store.
- `EstoridesCaseReader.get_host_entities` (method) `modules/estorides_importer.py:469` `def get_host_entities(self, case_id)` -- Get entities of host-related types (ipv4, ipv6, domain, url, asn).
- `EstoridesCaseReader.get_all_entities` (method) `modules/estorides_importer.py:473` `def get_all_entities(self, case_id)`
- `EstoridesCaseReader.stats` (method) `modules/estorides_importer.py:476` `def stats(self)`
- `EstoridesCaseReader.close` (method) `modules/estorides_importer.py:489` `def close(self)`
- `EstoridesStixParser.__init__` (method) `modules/estorides_importer.py:511` `def __init__(self, stix_path)`
- `EstoridesStixParser.available` (method) `modules/estorides_importer.py:515` `def available(self)`
- `EstoridesStixParser.parse` (method) `modules/estorides_importer.py:518` `def parse(self)` -- Parse a STIX 2.1 bundle into EstoridesEntity objects.
- `EstoridesStixParser.parse_by_type` (method) `modules/estorides_importer.py:552` `def parse_by_type(self, entity_types)` -- Parse STIX and group values by entity type.
- `find_lan_bundle_files` (function) `modules/estorides_importer.py:586` `def find_lan_bundle_files(lan_dir, sessions_dir)` -- Locate LAN bundle deliverables.
- `LanBundleReader.__init__` (method) `modules/estorides_importer.py:632` `def __init__(self, lan_dir)`
- `LanBundleReader.available` (method) `modules/estorides_importer.py:636` `def available(self)`
- `LanBundleReader.read_devices` (method) `modules/estorides_importer.py:639` `def read_devices(self)` -- Return raw device dicts from the inventory file.
- `LanBundleReader.parse` (method) `modules/estorides_importer.py:652` `def parse(self)` -- Parse LAN devices into entities (host, mac, domain).
- `LanBundleReader.attack_targets` (method) `modules/estorides_importer.py:683` `def attack_targets(self)` -- IPs actionable for the attack graph and auto_loop queue.
- `ensure_directories` (function) `modules/estorides_importer.py:694` `def ensure_directories()` -- Ensure sessions/ directories exist.
- `EstoridesToLazyOwnBridge.__init__` (method) `modules/estorides_importer.py:703` `def __init__(self, db_path, config_path)`
- `EstoridesToLazyOwnBridge.import_entities` (method) `modules/estorides_importer.py:711` `def import_entities(self, entities, add_to_scope, add_to_db)` -- Import entities into LazyOwn DB and optionally scope.
- `EstoridesToLazyOwnBridge.get_combined_surface` (method) `modules/estorides_importer.py:834` `def get_combined_surface(self)` -- Get the combined attack surface from LazyOwn DB + scope.
- `FeedbackLoop.__init__` (method) `modules/estorides_importer.py:892` `def __init__(self, max_iterations, max_depth, max_steps, timeout)`
- `FeedbackLoop.run` (method) `modules/estorides_importer.py:908` `def run(self, seed_methods)` -- Run the feedback loop.
- `export_combined_graph` (function) `modules/estorides_importer.py:1027` `def export_combined_graph(output_path)` -- Export the combined (Estorides + LazyOwn) graph as GraphML.

## modules/evasion_engine.py
Imported by: `cli/commands/evasive_payload.py`, `skills/lazyown_mcp.py`
- `EvasionEngine.__init__` (method) `modules/evasion_engine.py:130` `def __init__(self, config)`
- `EvasionEngine.set_config` (method) `modules/evasion_engine.py:136` `def set_config(self, config)`
- `EvasionEngine.generate_profile` (method) `modules/evasion_engine.py:244` `def generate_profile(self, os_family)`
- `EvasionEngine.rotate_profile` (method) `modules/evasion_engine.py:264` `def rotate_profile(self, os_family)`
- `EvasionEngine.get_active_profile` (method) `modules/evasion_engine.py:269` `def get_active_profile(self)`
- `EvasionEngine.get_beacon_config` (method) `modules/evasion_engine.py:272` `def get_beacon_config(self)`
- `EvasionEngine.morph_traffic` (method) `modules/evasion_engine.py:287` `def morph_traffic(self, config)`
- `EvasionEngine.get_history` (method) `modules/evasion_engine.py:328` `def get_history(self)`
- `EvasionEngine.profile_to_json` (method) `modules/evasion_engine.py:343` `def profile_to_json(self, profile)`

## modules/evasive_payloads.py
Imported by: `cli/commands/evasive_payload.py`
- `EvasivePayloadGenerator.__init__` (method) `modules/evasive_payloads.py:84` `def __init__(self)`
- `EvasivePayloadGenerator.generate_powershell_obfuscated` (method) `modules/evasive_payloads.py:138` `def generate_powershell_obfuscated(self, payload, obfuscation_level)` -- Generate an obfuscated PowerShell payload.
- `EvasivePayloadGenerator.generate_javascript_obfuscated` (method) `modules/evasive_payloads.py:178` `def generate_javascript_obfuscated(self, payload)` -- Generate an obfuscated JavaScript payload.
- `EvasivePayloadGenerator.generate_vba_obfuscated` (method) `modules/evasive_payloads.py:197` `def generate_vba_obfuscated(self, payload)` -- Generate an obfuscated VBA macro payload.
- `EvasivePayloadGenerator.generate_linux_evasive` (method) `modules/evasive_payloads.py:214` `def generate_linux_evasive(self, rhost, rport, technique)` -- Generate an evasive Linux reverse shell payload.
- `EvasivePayloadGenerator.generate_shellcode_loader_powershell` (method) `modules/evasive_payloads.py:239` `def generate_shellcode_loader_powershell(self, shellcode_b64, injection_technique)` -- Generate a PowerShell shellcode loader with AMSI bypass.
- `EvasivePayloadGenerator.generate_lolbas_execution` (method) `modules/evasive_payloads.py:284` `def generate_lolbas_execution(self, payload_url, technique)` -- Generate a LOLBAS-based payload execution command.
- `EvasivePayloadGenerator.generate_polymorphic_command` (method) `modules/evasive_payloads.py:334` `def generate_polymorphic_command(self, base_cmd, iterations)` -- Generate a polymorphic command that mutates at each execution.
- `EvasivePayloadGenerator.list_techniques` (method) `modules/evasive_payloads.py:374` `def list_techniques(self)` -- Return all available evasion techniques.

## modules/event_bus.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/collab_bp.py`, `modules/engagement_hooks.py`
Imported by: `lazyc2.py`, `lazyown.py`, `modules/command_executor.py`, `modules/event_consumers.py`, `modules/loop_ai_bridge.py`, `modules/sinks/event_bus.py`, `modules/state_manager.py`, `modules/unified_bridge.py`, `tests/test_loop_ai_bridge.py`
- `LazyEvent.to_dict` (method) `modules/event_bus.py:96` `def to_dict(self)`
- `LazyEvent.to_json` (method) `modules/event_bus.py:111` `def to_json(self)`
- `LazyEvent.from_dict` (method) `modules/event_bus.py:115` `def from_dict(cls, d)`
- `Sink.write` (method) `modules/event_bus.py:137` `def write(self, event)`
- `Sink.close` (method) `modules/event_bus.py:140` `def close(self)`
- `JsonlSink.__init__` (method) `modules/event_bus.py:146` `def __init__(self, filepath)`
- `JsonlSink.write` (method) `modules/event_bus.py:151` `def write(self, event)`
- `JsonlSink.close` (method) `modules/event_bus.py:159` `def close(self)`
- `CollabBusSink.__init__` (method) `modules/event_bus.py:166` `def __init__(self)`
- `CollabBusSink.write` (method) `modules/event_bus.py:181` `def write(self, event)`
- `CollabBusSink.close` (method) `modules/event_bus.py:198` `def close(self)`
- `EngagementSink.write` (method) `modules/event_bus.py:205` `def write(self, event)`
- `EngagementSink.close` (method) `modules/event_bus.py:226` `def close(self)`
- `UnifiedEventBus.__init__` (method) `modules/event_bus.py:255` `def __init__(self)`
- `UnifiedEventBus.instance` (method) `modules/event_bus.py:287` `def instance(cls)`
- `UnifiedEventBus.subscriber_count` (method) `modules/event_bus.py:295` `def subscriber_count(self)` -- Return the number of active subscribers across all registration types.
- `UnifiedEventBus.subscribe` (method) `modules/event_bus.py:300` `def subscribe(self, subscriber_id, callback)` -- Register a callback for all events.
- `UnifiedEventBus.subscribe_topic` (method) `modules/event_bus.py:305` `def subscribe_topic(self, subscriber_id, topic, callback)` -- Register a callback for events matching a topic.
- `UnifiedEventBus.subscribe_async` (method) `modules/event_bus.py:315` `def subscribe_async(self, subscriber_id)` -- Get a Queue for async event consumption (for SSE, WebSocket, etc.).
- `UnifiedEventBus.unsubscribe` (method) `modules/event_bus.py:327` `def unsubscribe(self, subscriber_id)` -- Remove all subscriptions for a subscriber.
- `UnifiedEventBus.publish` (method) `modules/event_bus.py:336` `def publish(self, event)` -- Publish an event via the bounded dispatch queue.
- `UnifiedEventBus.drain` (method) `modules/event_bus.py:354` `def drain(self)` -- Consume and drop all pending events from the dispatch queue.
- `UnifiedEventBus.shutdown` (method) `modules/event_bus.py:372` `def shutdown(self)` -- Shut down the event bus cleanly.
- `UnifiedEventBus.history` (method) `modules/event_bus.py:556` `def history(self, n, category)` -- Return recent events, optionally filtered by category.
- `UnifiedEventBus.history_since` (method) `modules/event_bus.py:564` `def history_since(self, since_ts)` -- Return all events since a given timestamp.
- `get_event_bus` (function) `modules/event_bus.py:570` `def get_event_bus()` -- Return the singleton UnifiedEventBus instance.
- `publish_event` (function) `modules/event_bus.py:575` `def publish_event(category, event_type, source, payload, severity, target, operator)` -- Convenience function to build and publish an event in one call.

## modules/event_consumers.py
Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/state_manager.py`
Imported by: `lazyc2.py`, `lazyown.py`, `skills/autonomous_daemon.py`
- `PhaseTracker.__init__` (method) `modules/event_consumers.py:156` `def __init__(self)`
- `PhaseTracker.__call__` (method) `modules/event_consumers.py:159` `def __call__(self, event)`
- `AutoRecommender.__init__` (method) `modules/event_consumers.py:204` `def __init__(self)`
- `AutoRecommender.__call__` (method) `modules/event_consumers.py:207` `def __call__(self, event)`
- `CredentialReactor.__call__` (method) `modules/event_consumers.py:282` `def __call__(self, event)`
- `SoulSync.__call__` (method) `modules/event_consumers.py:323` `def __call__(self, event)`
- `DashboardPusher.__call__` (method) `modules/event_consumers.py:361` `def __call__(self, event)`
- `wire_all_consumers` (function) `modules/event_consumers.py:380` `def wire_all_consumers(bus)` -- Register all event consumers on the UnifiedEventBus.
- `unwire_all_consumers` (function) `modules/event_consumers.py:409` `def unwire_all_consumers(bus)` -- Remove all event consumers from the bus.

## modules/event_engine.py
Imported by: `lazyc2.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`
- `load_rules` (function) `modules/event_engine.py:99` `def load_rules()` -- Load rules from event_rules.json, creating it with defaults if missing.
- `save_rules` (function) `modules/event_engine.py:110` `def save_rules(rules)`
- `add_rule` (function) `modules/event_engine.py:114` `def add_rule(rule)` -- Add or replace a rule by id.
- `process_new_rows` (function) `modules/event_engine.py:181` `def process_new_rows()` -- Read new rows from the session CSV since last watermark.
- `read_events` (function) `modules/event_engine.py:250` `def read_events(limit, status)` -- Return up to `limit` events matching `status` (pending/processed/all).
- `ack_event` (function) `modules/event_engine.py:270` `def ack_event(event_id)` -- Mark an event as processed.

## modules/evidence.py
Imported by: `modules/engage_summary.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_summary.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `hash_bytes` (function) `modules/evidence.py:37` `def hash_bytes(data)` -- Return the lowercase hex SHA-256 of data.
- `EvidenceStore.__init__` (method) `modules/evidence.py:57` `def __init__(self, base_dir)` -- Create vault directories.
- `EvidenceStore.blob_path` (method) `modules/evidence.py:65` `def blob_path(self, content_hash)` -- Resolve the canonical path for a validated hash.
- `EvidenceStore.put` (method) `modules/evidence.py:70` `def put(self, data)` -- Atomically store bytes and return their SHA-256 hash.
- `EvidenceStore.get` (method) `modules/evidence.py:90` `def get(self, content_hash)` -- Read and verify blob bytes for a hash.
- `EvidenceStore.exists` (method) `modules/evidence.py:98` `def exists(self, content_hash)` -- Return True when the blob exists on disk.
- `EvidenceStore.garbage_collect` (method) `modules/evidence.py:105` `def garbage_collect(self, referenced)` -- Remove unreferenced blobs older than the grace period.

## modules/exp.c
Imported by: `static/js/3d-force-graph-1.73.4.min.js`, `static/js/force-graph-1.43.5.min.js`
- `add_key` (function) `modules/exp.c:147` `static inline key_serial_t add_key(const char *type, const char *description, const void *payload...`
- `keyctl` (function) `modules/exp.c:151` `static inline long keyctl(int operation, unsigned long arg2, unsigned long arg3, unsigned long ar...`
- `bye` (function) `modules/exp.c:155` `void bye(char *info)`
- `do_error_exit` (function) `modules/exp.c:161` `void do_error_exit(char *info)`
- `bye2` (function) `modules/exp.c:167` `void bye2(char *info, char *arg)`
- `spray_keyring` (function) `modules/exp.c:172` `key_serial_t *spray_keyring(uint32_t start, uint32_t spray_size)`
- `spray_keyring_list_del_purpose` (function) `modules/exp.c:190` `key_serial_t *spray_keyring_list_del_purpose(uint32_t spray_size, uint64_t next, uint64_t prev, u...`
- `spray_keyring_list_overwrite_purpose` (function) `modules/exp.c:214` `key_serial_t *spray_keyring_list_overwrite_purpose(uint32_t spray_size, uint64_t len, uint64_t of...`
- `get_keyring_leak` (function) `modules/exp.c:248` `int get_keyring_leak(key_serial_t *id_buffer, uint32_t id_buffer_size)`
- `awake_partial_keys` (function) `modules/exp.c:271` `void awake_partial_keys(key_serial_t *id_buffer, uint32_t idx)`
- `release_keys` (function) `modules/exp.c:279` `void release_keys(key_serial_t *id_buffer, uint32_t id_buffer_size)`
- `release_partial_keys` (function) `modules/exp.c:290` `void release_partial_keys(key_serial_t *id_buffer, int i)`
- `unshare_setup` (function) `modules/exp.c:297` `void unshare_setup(uid_t uid, gid_t gid)`
- `set_stable_table_and_set` (function) `modules/exp.c:322` `void set_stable_table_and_set(struct mnl_socket* nl, const char *name)`
- `set_trigger_set_and_overwrite` (function) `modules/exp.c:385` `void set_trigger_set_and_overwrite(struct mnl_socket* nl, const char *name, const char *set_name)`
- `set_cpu_affinity` (function) `modules/exp.c:438` `void set_cpu_affinity(int cpu_n, pid_t pid)`
- `spray_mqueue` (function) `modules/exp.c:448` `void spray_mqueue(mqd_t mqdes, char *msgptr, int spray_size)`
- `gather_mqueue` (function) `modules/exp.c:463` `int gather_mqueue(mqd_t mqdes, int gather_size)`
- `gather_mqueue_nosave` (function) `modules/exp.c:485` `int gather_mqueue_nosave(mqd_t mqdes, int gather_size)`
- `spray_msg_msg` (function) `modules/exp.c:496` `void spray_msg_msg(unsigned int size, unsigned int amount, int qid)`
- `io_uring_setup` (function) `modules/exp.c:520` `static inline int io_uring_setup(uint32_t entries, struct io_uring_params *p)`
- `io_uring_register` (function) `modules/exp.c:524` `static inline int io_uring_register(int fd, unsigned int opcode, void *arg, unsigned int nr_args)`
- `spray_uring` (function) `modules/exp.c:529` `struct fd_uring *spray_uring(uint32_t spray_size, struct fd_uring *fd_buffer)`
- `release_uring` (function) `modules/exp.c:546` `void release_uring(struct fd_uring *fd_buffer, uint32_t buffer_size)`
- `release_partial_uring` (function) `modules/exp.c:554` `void release_partial_uring(struct fd_uring *fd_buffer, uint32_t buffer_idx)`
- `prepare_root_shell` (function) `modules/exp.c:559` `void prepare_root_shell(void)`
- `create_dummy_file` (function) `modules/exp.c:564` `void create_dummy_file(void)`
- `create_priv_file` (function) `modules/exp.c:572` `void create_priv_file(void)`
- `write_new_modprobe` (function) `modules/exp.c:582` `void write_new_modprobe()`
- `setup_modprobe_payload` (function) `modules/exp.c:601` `void setup_modprobe_payload()`
- `userland_T` (function) `modules/exp.c:605` `void userland_T(int *sema)`
- `sema_up` (function) `modules/exp.c:610` `void sema_up(int *sema)`
- `sema_down` (function) `modules/exp.c:615` `void sema_down(int *sema)`
- `main` (function) `modules/exp.c:620` `int main(int argc, char ** argv)`

## modules/exploit_chain.py
Depends on: `modules/outcome_bus.py`
Imported by: `cli/commands/exploit_migrated.py`
- `ExploitChain.__init__` (method) `modules/exploit_chain.py:292` `def __init__(self, rhost, rport, lhost, lport, sessions_dir, nmap_xml_path)`
- `ExploitChain.fingerprint_services` (method) `modules/exploit_chain.py:311` `def fingerprint_services(self, nmap_output)` -- Parse service information from all available nmap XML files.
- `ExploitChain.map_vulnerabilities` (method) `modules/exploit_chain.py:446` `def map_vulnerabilities(self)` -- Map discovered services to known vulnerabilities.
- `ExploitChain.generate_exploit_plan` (method) `modules/exploit_chain.py:499` `def generate_exploit_plan(self)` -- Generate a prioritized exploitation plan.
- `ExploitChain.get_post_exploit_commands` (method) `modules/exploit_chain.py:519` `def get_post_exploit_commands(self, platform)` -- Return recommended post-exploitation commands for the platform.
- `ExploitChain.generate_report` (method) `modules/exploit_chain.py:531` `def generate_report(self)` -- Generate a structured exploitation chain report.
- `ExploitChain.save_report` (method) `modules/exploit_chain.py:566` `def save_report(self, path)` -- Save the exploitation chain report to a file.

## modules/exploit_recommender.py
Depends on: `lazygui/version.py`, `modules/world_model.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/pwn.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`
- `parse_version` (function) `modules/exploit_recommender.py:25` `def parse_version(v)`
- `ExploitRecommender.__init__` (method) `modules/exploit_recommender.py:120` `def __init__(self, world_model)`
- `ExploitRecommender.set_world_model` (method) `modules/exploit_recommender.py:129` `def set_world_model(self, world_model)`
- `ExploitRecommender.set_nvd_api_key` (method) `modules/exploit_recommender.py:132` `def set_nvd_api_key(self, key)`
- `ExploitRecommender.match_services` (method) `modules/exploit_recommender.py:244` `def match_services(self, hosts)` -- Match discovered services against known CVEs with confidence scoring.
- `ExploitRecommender.recommend` (method) `modules/exploit_recommender.py:337` `def recommend(self, hosts, top_n)` -- Return top-N recommended exploits as structured dicts for MCP/CLI.
- `ExploitRecommender.persist_recommendations` (method) `modules/exploit_recommender.py:370` `def persist_recommendations(self, matches)` -- Save recommendations to sessions/ for audit and replay.
- `ExploitRecommender.format_for_llm` (method) `modules/exploit_recommender.py:390` `def format_for_llm(self, matches, max_items)` -- Format recommendations as compact text for LLM context injection.

## modules/exploitgym_gym.py
Depends on: `modules/redteam_gym.py`
Imported by: `cli/commands/exploitgym.py`, `skills/lazyown_mcp.py`, `tests/test_exploitgym_gym.py`
- `check_readiness` (function) `modules/exploitgym_gym.py:112` `def check_readiness(params)` -- Report whether the ExploitGym harness can run.
- `list_tasks` (function) `modules/exploitgym_gym.py:178` `def list_tasks(params, domain, limit)` -- List available ExploitGym tasks, optionally filtered by domain.
- `setup_harness` (function) `modules/exploitgym_gym.py:249` `def setup_harness(params, steps)` -- Automate ExploitGym installation (clone, deps, data, firewall, images).
- `pull_task` (function) `modules/exploitgym_gym.py:344` `def pull_task(task_id, params, timeout)` -- Pull the Docker image required by a task.
- `run_task` (function) `modules/exploitgym_gym.py:423` `def run_task(task_id, params, model, mitigations, timeout)` -- Run the agent against an ExploitGym task and capture the outcome.
- `verify_flag` (function) `modules/exploitgym_gym.py:548` `def verify_flag(task_id, params)` -- Verify whether a task flag was captured from a previous run.
- `score_task` (function) `modules/exploitgym_gym.py:565` `def score_task(task_id, success, techniques, params)` -- Award Red Team Gym ELO and leaderboard points for a task outcome.


Next: [API_p12.md](API_p12.md)
