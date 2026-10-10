# API (page 10 of 20)
Previous: [API_p9.md](API_p9.md)

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
Imported by: `cli/commands/campaign.py`, `cli/commands/collaboration.py`, `cli/commands/database.py`, `lazyc2/blueprints/api_v1.py`, `modules/autonomous_exploit_engine.py`, `modules/estorides_importer.py`, `modules/hash_cracker.py`, `modules/integrations/nuclei_parser.py`, `modules/opsec_scorer.py`, `modules/state_manager.py`, `scripts/devtools/core_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_api_v1.py`, `tests/test_db.py`, `tests/test_mutation_verification.py`, `tests/test_security_hardening.py`
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
- `LazyOwnDB.vuln_list` (method) `modules/db.py:478` `def vuln_list(self, workspace_id, severity)` -- List vulns in workspace, optionally filtered by severity.
- `LazyOwnDB.cred_add` (method) `modules/db.py:507` `def cred_add(self, host_id, username, password, realm, cred_type, origin)` -- Add a credential (password encrypted at rest).
- `LazyOwnDB.cred_list` (method) `modules/db.py:527` `def cred_list(self, workspace_id)` -- List all creds in workspace (passwords decrypted).
- `LazyOwnDB.loot_add` (method) `modules/db.py:546` `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` -- Add a loot entry.
- `LazyOwnDB.loot_list` (method) `modules/db.py:565` `def loot_list(self, workspace_id)` -- List all loot in workspace.
- `LazyOwnDB.note_add` (method) `modules/db.py:581` `def note_add(self, workspace_id, data, note_type, host_id)` -- Add a note.
- `LazyOwnDB.note_list` (method) `modules/db.py:598` `def note_list(self, workspace_id)` -- List all notes in workspace.
- `LazyOwnDB.import_nmap_xml` (method) `modules/db.py:614` `def import_nmap_xml(self, workspace_id, xml_path)` -- Import an Nmap XML file into the database.
- `LazyOwnDB.export_csv` (method) `modules/db.py:690` `def export_csv(self, table, workspace_id)` -- Export a table to CSV string.
- `LazyOwnDB.status` (method) `modules/db.py:725` `def status(self, workspace_id)` -- Return counts for every entity type in a workspace.
- `LazyOwnDB.close` (method) `modules/db.py:754` `def close(self)` -- Close the database connection for the current thread.
- `LazyOwnDB.get_db` (method) `modules/db.py:771` `def get_db(db_path)` -- Get or create a :class:`LazyOwnDB` instance.

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
- `DetectionFeed.get_feed` (method) `modules/detection_feed.py:326` `def get_feed()` -- Return a module-level :class:`DetectionFeed` singleton.

## modules/detection_oracle.py
Depends on: `core/logging.py`, `modules/detection_feed.py`
Imported by: `modules/auto_purple.py`, `modules/detection_feed.py`, `skills/autonomous_daemon.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`, `tests/test_detection_feed.py`, `tests/test_moe_rl_swan.py`
- `DetectionAssessment.is_high_risk` (method) `modules/detection_oracle.py:75` `def is_high_risk(self)` -- Return True when detection probability is 70% or higher.
- `DetectionAssessment.is_critical_risk` (method) `modules/detection_oracle.py:80` `def is_critical_risk(self)` -- Return True when detection probability is 90% or higher.
- `IDetectionOracle.assess` (method) `modules/detection_oracle.py:94` `def assess(self, command, args, action_category)` -- Return a full DetectionAssessment for the given action.
- `IDetectionOracle.probability` (method) `modules/detection_oracle.py:103` `def probability(self, command, args, action_category)` -- Return only the probability score in [0.0, 1.0].
- `DetectionOracle.__init__` (method) `modules/detection_oracle.py:332` `def __init__(self, rules, feed)`
- `DetectionOracle.refresh` (method) `modules/detection_oracle.py:336` `def refresh(self)` -- Update rules from the detection feed (if available).
- `DetectionOracle.assess` (method) `modules/detection_oracle.py:371` `def assess(self, command, args, action_category)`
- `DetectionOracle.probability` (method) `modules/detection_oracle.py:392` `def probability(self, command, args, action_category)`
- `DetectionOracle.get_oracle` (method) `modules/detection_oracle.py:478` `def get_oracle()` -- Return (or create) the module-level singleton DetectionOracle.

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
Imported by: `cli/commands/lateral_migrated.py`
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
- `EngagementNarrator.get_default_narrator` (method) `modules/engagement_hooks.py:482` `def get_default_narrator()` -- Return the process-wide default narrator (lazy singleton).
- `EngagementNarrator.publish_shell_obtained` (method) `modules/engagement_hooks.py:491` `def publish_shell_obtained(client_id, primary_ip, hostname, user, platform, narrator)` -- Single entry point called by lazyc2.py on every beacon check-in.
- `EngagementNarrator.append_approval_record` (method) `modules/engagement_hooks.py:564` `def append_approval_record(record)` -- Append one approval-pending record to sessions/engagement_approvals.jsonl.
- `EngagementNarrator.list_pending_approvals` (method) `modules/engagement_hooks.py:575` `def list_pending_approvals()` -- Return every approval record whose status is still 'pending'.
- `EngagementNarrator.resolve_approval` (method) `modules/engagement_hooks.py:601` `def resolve_approval(approval_id, decision, operator)` -- Append a resolution record for the given approval_id.
- `EngagementNarrator.is_valid_target` (method) `modules/engagement_hooks.py:626` `def is_valid_target(value)` -- Validate that value is a dotted-quad IPv4 or a safe hostname token.

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

## modules/estorides_importer.py
Depends on: `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/estorides.py`, `modules/intelligence_engine.py`
- `ImportResult.success` (method) `modules/estorides_importer.py:110` `def success(self)`
- `ImportResult.to_dict` (method) `modules/estorides_importer.py:113` `def to_dict(self)`
- `SeedResult.new_assets` (method) `modules/estorides_importer.py:139` `def new_assets(self)`
- `SeedResult.extract_seeds_from_world_model` (method) `modules/estorides_importer.py:143` `def extract_seeds_from_world_model(world_model_path)` -- Extract IPs and domains from world_model.json as estorides seeds.
- `SeedResult.extract_seeds_from_hosts_file` (method) `modules/estorides_importer.py:175` `def extract_seeds_from_hosts_file(path)` -- Extract IPs/domains from hostsdiscovery.txt or similar.
- `SeedResult.extract_seeds_from_db` (method) `modules/estorides_importer.py:203` `def extract_seeds_from_db(db_path)` -- Extract hosts from LazyOwn database.
- `SeedResult.extract_seeds_from_scope` (method) `modules/estorides_importer.py:242` `def extract_seeds_from_scope(scope_entries)` -- Extract scoped IPs/domains from payload.json scope list.
- `SeedResult.run_estorides_discover` (method) `modules/estorides_importer.py:272` `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` -- Run estorides discover on a single seed.
- `SeedResult.run_estorides_run` (method) `modules/estorides_importer.py:332` `def run_estorides_run(query, out_json, timeout)` -- Run estorides run (single fan-out) on a query.
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
- `EstoridesStixParser.ensure_directories` (method) `modules/estorides_importer.py:579` `def ensure_directories()` -- Ensure sessions/ directories exist.
- `EstoridesToLazyOwnBridge.__init__` (method) `modules/estorides_importer.py:588` `def __init__(self, db_path, config_path)`
- `EstoridesToLazyOwnBridge.import_entities` (method) `modules/estorides_importer.py:596` `def import_entities(self, entities, add_to_scope, add_to_db)` -- Import entities into LazyOwn DB and optionally scope.
- `EstoridesToLazyOwnBridge.get_combined_surface` (method) `modules/estorides_importer.py:719` `def get_combined_surface(self)` -- Get the combined attack surface from LazyOwn DB + scope.
- `FeedbackLoop.__init__` (method) `modules/estorides_importer.py:777` `def __init__(self, max_iterations, max_depth, max_steps, timeout)`
- `FeedbackLoop.run` (method) `modules/estorides_importer.py:793` `def run(self, seed_methods)` -- Run the feedback loop.
- `FeedbackLoop.export_combined_graph` (method) `modules/estorides_importer.py:912` `def export_combined_graph(output_path)` -- Export the combined (Estorides + LazyOwn) graph as GraphML.

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
Imported by: `lazyc2.py`, `lazyown.py`, `modules/command_executor.py`, `modules/event_consumers.py`, `modules/state_manager.py`, `modules/unified_bridge.py`, `skills/lazyown_mcp.py`
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
- `UnifiedEventBus.get_event_bus` (method) `modules/event_bus.py:570` `def get_event_bus()` -- Return the singleton UnifiedEventBus instance.
- `UnifiedEventBus.publish_event` (method) `modules/event_bus.py:575` `def publish_event(category, event_type, source, payload, severity, target, operator)` -- Convenience function to build and publish an event in one call.

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
- `DashboardPusher.wire_all_consumers` (method) `modules/event_consumers.py:380` `def wire_all_consumers(bus)` -- Register all event consumers on the UnifiedEventBus.
- `DashboardPusher.unwire_all_consumers` (method) `modules/event_consumers.py:409` `def unwire_all_consumers(bus)` -- Remove all event consumers from the bus.

## modules/event_engine.py
Imported by: `lazyc2.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`
- `load_rules` (function) `modules/event_engine.py:99` `def load_rules()` -- Load rules from event_rules.json, creating it with defaults if missing.
- `save_rules` (function) `modules/event_engine.py:110` `def save_rules(rules)`
- `add_rule` (function) `modules/event_engine.py:114` `def add_rule(rule)` -- Add or replace a rule by id.
- `process_new_rows` (function) `modules/event_engine.py:181` `def process_new_rows()` -- Read new rows from the session CSV since last watermark.
- `read_events` (function) `modules/event_engine.py:250` `def read_events(limit, status)` -- Return up to `limit` events matching `status` (pending/processed/all).
- `ack_event` (function) `modules/event_engine.py:270` `def ack_event(event_id)` -- Mark an event as processed.

## modules/exp.c
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
- `parse_version` (method) `modules/exploit_recommender.py:25` `def parse_version(v)`
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

## modules/fast_run_service.sh
- `log_timestamp` (function) `modules/fast_run_service.sh:69` -- # # Logging primitives.
- `log_info` (function) `modules/fast_run_service.sh:73`
- `log_warn` (function) `modules/fast_run_service.sh:77`
- `log_error` (function) `modules/fast_run_service.sh:81`
- `require_root` (function) `modules/fast_run_service.sh:89` -- # # Pre-flight checks.
- `require_deps` (function) `modules/fast_run_service.sh:97`
- `require_paths` (function) `modules/fast_run_service.sh:113`
- `prepare_runtime_dirs` (function) `modules/fast_run_service.sh:126`
- `load_config` (function) `modules/fast_run_service.sh:139`
- `config_truthy` (function) `modules/fast_run_service.sh:155`
- `pid_file_for` (function) `modules/fast_run_service.sh:166` -- # # PID-file primitives.
- `log_file_for` (function) `modules/fast_run_service.sh:171`
- `read_pid_value` (function) `modules/fast_run_service.sh:176`
- `is_pid_alive` (function) `modules/fast_run_service.sh:189`
- `is_service_running` (function) `modules/fast_run_service.sh:194`
- `write_pid_file` (function) `modules/fast_run_service.sh:201`
- `ensure_log_file` (function) `modules/fast_run_service.sh:211`
- `spawn_as_target_user` (function) `modules/fast_run_service.sh:228` -- # # Process spawn primitives.
- `spawn_as_root` (function) `modules/fast_run_service.sh:247`
- `terminate_pid_tree` (function) `modules/fast_run_service.sh:264`
- `stop_named_service` (function) `modules/fast_run_service.sh:292`
- `chown_project_tree` (function) `modules/fast_run_service.sh:310` -- # # Ownership maintenance.
- `start_chown_watcher` (function) `modules/fast_run_service.sh:315`
- `start_lazyc2_service` (function) `modules/fast_run_service.sh:342` -- # # Concrete service launchers.
- `start_www_service` (function) `modules/fast_run_service.sh:356`
- `start_vpn_service` (function) `modules/fast_run_service.sh:363`
- `start_discord_service` (function) `modules/fast_run_service.sh:380`
- `start_telegram_service` (function) `modules/fast_run_service.sh:390`
- `start_cloudflare_service` (function) `modules/fast_run_service.sh:400`
- `start_ollama_service` (function) `modules/fast_run_service.sh:410`
- `managed_services_in_order` (function) `modules/fast_run_service.sh:429` -- # # Service registry.
- `cmd_start` (function) `modules/fast_run_service.sh:445` -- # # Lifecycle commands.
- `cmd_stop` (function) `modules/fast_run_service.sh:465`
- `cmd_restart` (function) `modules/fast_run_service.sh:480`
- `cmd_status` (function) `modules/fast_run_service.sh:486`
- `cmd_logs` (function) `modules/fast_run_service.sh:505`
- `cmd_chown_now` (function) `modules/fast_run_service.sh:521`
- `usage` (function) `modules/fast_run_service.sh:528`
- `main` (function) `modules/fast_run_service.sh:557` -- # # Entry point. require_root re-executes under sudo and never returns there; # the case-arm dispatch is reached...

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

## modules/hash_cracker.py
Depends on: `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`
- `HashCracker.__init__` (method) `modules/hash_cracker.py:168` `def __init__(self, wordlist, rules, use_hashcat, timeout)`
- `HashCracker.identify` (method) `modules/hash_cracker.py:190` `def identify(self, line)` -- Identify the hash type of a single line.
- `HashCracker.identify_file` (method) `modules/hash_cracker.py:277` `def identify_file(self, filepath)` -- Parse a hash file and group hashes by type.
- `HashCracker.crack_hash` (method) `modules/hash_cracker.py:299` `def crack_hash(self, hash_value, hash_type, wordlist)` -- Attempt to crack a single hash.
- `HashCracker.crack_file` (method) `modules/hash_cracker.py:353` `def crack_file(self, filepath, wordlist, hash_types)` -- Crack all hashes in a file.
- `HashCracker.import_to_db` (method) `modules/hash_cracker.py:409` `def import_to_db(self, results, rhost, workspace_name)` -- Import cracked results into the LazyOwnDB credentials table.
- `HashCracker.crack_secretsdump_output` (method) `modules/hash_cracker.py:699` `def crack_secretsdump_output(filepath, wordlist, rhost)` -- Convenience function: crack a secretsdump output file and import results.

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
- `CodeAnalyzer.analyze_with_deepseek` (method) `modules/ia_code_analysis.py:66` `def analyze_with_deepseek(code_content, file_path, mode)` -- Sends the code content to DeepSeek for analysis.
- `CodeAnalyzer.save_results_to_json` (method) `modules/ia_code_analysis.py:123` `def save_results_to_json(results, file_path)` -- Saves the analysis results to JSON files.
- `CodeAnalyzer.start_analysis` (method) `modules/ia_code_analysis.py:169` `def start_analysis(code_dir, mode)` -- Starts the analysis of the specified code directory.
- `CodeAnalyzer.parse_args` (method) `modules/ia_code_analysis.py:178` `def parse_args()`

## modules/ia_logs_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `LogFileHandler.__init__` (method) `modules/ia_logs_analysis.py:59` `def __init__(self, mode)`
- `LogFileHandler.on_modified` (method) `modules/ia_logs_analysis.py:64` `def on_modified(self, event)` -- Triggered when a log file is modified.
- `LogFileHandler.analyze_log_file` (method) `modules/ia_logs_analysis.py:75` `def analyze_log_file(self, file_path)` -- Analyzes the content of the modified log file.
- `LogFileHandler.analyze_with_deepseek` (method) `modules/ia_logs_analysis.py:94` `def analyze_with_deepseek(log_content, mode)` -- Sends log content to DeepSeek for advanced analysis.
- `LogFileHandler.start_monitoring` (method) `modules/ia_logs_analysis.py:147` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `LogFileHandler.parse_args` (method) `modules/ia_logs_analysis.py:168` `def parse_args()`

## modules/ia_network_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `analyze_with_deepseek` (function) `modules/ia_network_analysis.py:39` `def analyze_with_deepseek(packet_info, mode)` -- Envía la información del paquete a DeepSeek para análisis avanzado.
- `packet_callback` (function) `modules/ia_network_analysis.py:91` `def packet_callback(packet, mode)` -- Callback para procesar cada paquete capturado.
- `start_monitoring` (function) `modules/ia_network_analysis.py:130` `def start_monitoring(interface, timeout, mode)` -- Inicia el monitoreo del tráfico de red.
- `parse_args` (function) `modules/ia_network_analysis.py:154` `def parse_args()`


Next: [API_p11.md](API_p11.md)
