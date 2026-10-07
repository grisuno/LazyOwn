# API (page 14 of 20)
Previous: [API_p13.md](API_p13.md)

## modules/socks_proxy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/socks_proxy.py`, `modules/beacon_config_builder.py`, `tests/test_socks_proxy.py`
- `SocksReply.message` (method) `modules/socks_proxy.py:103` `def message(self)` -- Return a human-readable message for this reply code.
- `SocksSession.elapsed_seconds` (method) `modules/socks_proxy.py:144` `def elapsed_seconds(self)` -- Return seconds since session creation.
- `SocksSession.to_dict` (method) `modules/socks_proxy.py:149` `def to_dict(self)` -- Serialize session to dictionary.
- `SocksProxyConfig.to_dict` (method) `modules/socks_proxy.py:200` `def to_dict(self)` -- Serialize config to dictionary.
- `SocksProxyConfig.from_dict` (method) `modules/socks_proxy.py:219` `def from_dict(cls, raw)` -- Build config from dictionary.
- `SocksValidator.validate_config` (method) `modules/socks_proxy.py:254` `def validate_config(config)` -- Validate a SocksProxyConfig and return error messages.
- `SocksValidator.validate_request` (method) `modules/socks_proxy.py:311` `def validate_request(command, address_type, host, port, config)` -- Validate a SOCKS5 request against the proxy configuration.
- `SocksProxyEngine.__init__` (method) `modules/socks_proxy.py:392` `def __init__(self, config)`
- `SocksProxyEngine.config` (method) `modules/socks_proxy.py:398` `def config(self)` -- Return the current proxy configuration.
- `SocksProxyEngine.sessions` (method) `modules/socks_proxy.py:403` `def sessions(self)` -- Return active proxied sessions.
- `SocksProxyEngine.session_count` (method) `modules/socks_proxy.py:408` `def session_count(self)` -- Return the number of active sessions.
- `SocksProxyEngine.validate` (method) `modules/socks_proxy.py:412` `def validate(self, config)` -- Validate the configuration.
- `SocksProxyEngine.build_spec` (method) `modules/socks_proxy.py:424` `def build_spec(self)` -- Build a JSON-serializable proxy specification for beacon delivery.
- `SocksProxyEngine.create_session` (method) `modules/socks_proxy.py:447` `def create_session(self, session_id, target_host, target_port, beacon_client_id)` -- Create and track a new proxied session.
- `SocksProxyEngine.remove_session` (method) `modules/socks_proxy.py:482` `def remove_session(self, session_id)` -- Remove a session by ID.
- `SocksProxyEngine.get_session` (method) `modules/socks_proxy.py:489` `def get_session(self, session_id)` -- Return a session by ID, or None.
- `SocksProxyEngine.add_bytes` (method) `modules/socks_proxy.py:493` `def add_bytes(self, session_id, sent, received)` -- Update byte counters for a session.
- `SocksProxyEngine.cleanup_expired` (method) `modules/socks_proxy.py:503` `def cleanup_expired(self)` -- Remove sessions that have exceeded the timeout.
- `SocksProxyEngine.list_sessions` (method) `modules/socks_proxy.py:517` `def list_sessions(self)` -- Return a list of all active sessions as dictionaries.
- `SocksProxyEngine.from_dict` (method) `modules/socks_proxy.py:528` `def from_dict(cls, raw)` -- Build a SocksProxyEngine from a configuration dictionary.
- `SocksProxyEngine.from_payload` (method) `modules/socks_proxy.py:534` `def from_payload(cls, payload)` -- Build a SocksProxyEngine from a LazyOwn payload configuration.

## modules/staged_delivery.py
Imported by: `cli/commands/payload_arsenal.py`
- `StagedDeliveryFactory.__init__` (method) `modules/staged_delivery.py:83` `def __init__(self, config, output_dir)`
- `StagedDeliveryFactory.generate_hta` (method) `modules/staged_delivery.py:141` `def generate_hta(self)` -- Generate an HTA (HTML Application) dropper.
- `StagedDeliveryFactory.generate_vba_macro` (method) `modules/staged_delivery.py:178` `def generate_vba_macro(self)` -- Generate a VBA macro for Office documents (Word/Excel).
- `StagedDeliveryFactory.generate_xlm_macro` (method) `modules/staged_delivery.py:226` `def generate_xlm_macro(self)` -- Generate an Excel 4.0 (XLM) macro for legacy macro execution.
- `StagedDeliveryFactory.generate_lnk` (method) `modules/staged_delivery.py:244` `def generate_lnk(self)` -- Generate a Windows .lnk shortcut file with embedded command execution.
- `StagedDeliveryFactory.generate_iso` (method) `modules/staged_delivery.py:321` `def generate_iso(self, inner_files)` -- Generate an ISO 9660 image with an embedded payload autorun.
- `StagedDeliveryFactory.generate_vhd` (method) `modules/staged_delivery.py:390` `def generate_vhd(self, inner_files)` -- Generate a VHD (Virtual Hard Disk) image with embedded payloads.
- `StagedDeliveryFactory.generate_all` (method) `modules/staged_delivery.py:440` `def generate_all(self)` -- Generate all delivery formats for the current configuration.
- `StagedDeliveryFactory.generate_phishing_page` (method) `modules/staged_delivery.py:480` `def generate_phishing_page(self, template)` -- Generate a credential harvesting HTML page.

## modules/state_manager.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/event_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `lazyown.py`, `modules/conditional_hooks.py`, `modules/event_consumers.py`, `modules/unified_bridge.py`
- `StateManager.__init__` (method) `modules/state_manager.py:107` `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)`
- `StateManager.instance` (method) `modules/state_manager.py:129` `def instance(cls)`
- `StateManager.db` (method) `modules/state_manager.py:137` `def db(self)`
- `StateManager.workspace_id` (method) `modules/state_manager.py:145` `def workspace_id(self)`
- `StateManager.set_payload` (method) `modules/state_manager.py:164` `def set_payload(self, payload)`
- `StateManager.close` (method) `modules/state_manager.py:198` `def close(self)`
- `StateManager.add_host` (method) `modules/state_manager.py:209` `def add_host(self, address, mac, hostname, os, state)`
- `StateManager.get_host` (method) `modules/state_manager.py:225` `def get_host(self, address)`
- `StateManager.list_hosts` (method) `modules/state_manager.py:234` `def list_hosts(self)`
- `StateManager.advance_host` (method) `modules/state_manager.py:238` `def advance_host(self, address, new_state)`
- `StateManager.delete_host` (method) `modules/state_manager.py:254` `def delete_host(self, address)`
- `StateManager.add_service` (method) `modules/state_manager.py:266` `def add_service(self, host_address, port, protocol, name, product, version, state)`
- `StateManager.list_services` (method) `modules/state_manager.py:290` `def list_services(self, host_address)`
- `StateManager.add_credential` (method) `modules/state_manager.py:299` `def add_credential(self, host_address, username, password, realm, cred_type, origin)`
- `StateManager.list_credentials` (method) `modules/state_manager.py:322` `def list_credentials(self, host_address)`
- `StateManager.add_vulnerability` (method) `modules/state_manager.py:333` `def add_vulnerability(self, host_address, name, severity, description, refs)`
- `StateManager.list_vulnerabilities` (method) `modules/state_manager.py:352` `def list_vulnerabilities(self, host_address, severity)`
- `StateManager.add_loot` (method) `modules/state_manager.py:363` `def add_loot(self, name, loot_type, path, notes, host_address)`
- `StateManager.list_loot` (method) `modules/state_manager.py:385` `def list_loot(self)`
- `StateManager.add_note` (method) `modules/state_manager.py:391` `def add_note(self, data, note_type, host_address)`
- `StateManager.list_notes` (method) `modules/state_manager.py:406` `def list_notes(self)`
- `StateManager.import_nmap_xml` (method) `modules/state_manager.py:412` `def import_nmap_xml(self, xml_path)`
- `StateManager.import_nmap_from_facts` (method) `modules/state_manager.py:424` `def import_nmap_from_facts(self, facts)` -- Import hosts and services from a FactStore-style facts dict into DB.
- `StateManager.status` (method) `modules/state_manager.py:475` `def status(self)`
- `StateManager.get_world_model_cache` (method) `modules/state_manager.py:524` `def get_world_model_cache(self)`
- `StateManager.load_world_model` (method) `modules/state_manager.py:530` `def load_world_model(self)` -- Return a WorldModel instance populated from DB state.
- `StateManager.session_snapshot` (method) `modules/state_manager.py:565` `def session_snapshot(self)`
- `StateManager.export_csv` (method) `modules/state_manager.py:648` `def export_csv(self, table)`
- `StateManager.export_summary` (method) `modules/state_manager.py:652` `def export_summary(self)`
- `StateManager.get_state_manager` (method) `modules/state_manager.py:667` `def get_state_manager()`

## modules/sudo_tiocsti.py
Depends on: `core/logging.py`
- `get_controlling_tty` (function) `modules/sudo_tiocsti.py:44` `def get_controlling_tty()` -- Return (file_descriptor, tty_path) for the controlling terminal.
- `inject_byte` (function) `modules/sudo_tiocsti.py:55` `def inject_byte(fd, byte_char)` -- Inject a single byte via TIOCSTI; return success status.
- `inject_payload` (function) `modules/sudo_tiocsti.py:69` `def inject_payload(fd, payload, char_delay)` -- Inject a multi‑character payload.
- `get_sudo_pids_on_tty` (function) `modules/sudo_tiocsti.py:91` `def get_sudo_pids_on_tty(tty_path)` -- Return a list of PIDs that are running 'sudo' and have the same controlling terminal as the given tty_path.
- `sudo_cache_valid` (function) `modules/sudo_tiocsti.py:127` `def sudo_cache_valid()` -- Return True if sudo credentials are cached (i.e., sudo -n succeeds).
- `mode_poll` (function) `modules/sudo_tiocsti.py:138` `def mode_poll(fd, tty_path)` -- Poll for sudo processes; inject payload when sudo exits.
- `mode_prefill` (function) `modules/sudo_tiocsti.py:163` `def mode_prefill(fd)` -- Inject payload repeatedly, regardless of sudo state.
- `mode_cache` (function) `modules/sudo_tiocsti.py:173` `def mode_cache(fd)` -- Check sudo cache; if valid, inject sudo -i once.
- `main` (function) `modules/sudo_tiocsti.py:185` `def main()`

## modules/tel.py
- `get_machine_id` (function) `modules/tel.py:10` `def get_machine_id()`
- `get_version` (function) `modules/tel.py:22` `def get_version()`
- `to_numbers` (function) `modules/tel.py:33` `def to_numbers(hex_str)` -- Simula la función toNumbers de JavaScript
- `to_hex` (function) `modules/tel.py:37` `def to_hex(byte_list)` -- Simula la función toHex de JavaScript
- `decrypt_cookie` (function) `modules/tel.py:41` `def decrypt_cookie(encrypted, key, iv)` -- Descifra usando AES en modo CBC (como slowAES.decrypt(c,2,a,b))
- `main` (function) `modules/tel.py:47` `def main()` -- Sistema de telemetría de uso por instalación no invasiva.

## modules/threat_model.py
Depends on: `core/logging.py`
Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ThreatModelBuilder.build` (method) `modules/threat_model.py:270` `def build(self)`
- `ThreatModelBuilder.load` (method) `modules/threat_model.py:293` `def load(self)`
- `ThreatModelBuilder.get_builder` (method) `modules/threat_model.py:577` `def get_builder()`

## modules/timeline_narrator.py
Depends on: `modules/ai_fallback.py`
Imported by: `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `narrate` (function) `modules/timeline_narrator.py:129` `def narrate(api_key, force)` -- Generate and return the timeline narrative.
- `load_timeline` (function) `modules/timeline_narrator.py:164` `def load_timeline()` -- Return the last written timeline.md or empty string.

## modules/timestomper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `Timestomper.__init__` (method) `modules/timestomper.py:106` `def __init__(self, config)`
- `Timestomper.windows_timestomp_powershell` (method) `modules/timestomper.py:110` `def windows_timestomp_powershell(self)` -- Generate PowerShell commands for Windows file timestomping.
- `Timestomper.windows_timestomp_c` (method) `modules/timestomper.py:152` `def windows_timestomp_c(self)` -- Generate C code for Windows timestomping via SetFileTime API.
- `Timestomper.linux_timestomp_commands` (method) `modules/timestomper.py:200` `def linux_timestomp_commands(self)` -- Generate Linux commands for file timestomping.
- `Timestomper.macos_timestomp_commands` (method) `modules/timestomper.py:241` `def macos_timestomp_commands(self)` -- Generate macOS commands for file timestomping.
- `Timestomper.generate_random_timestamps` (method) `modules/timestomper.py:280` `def generate_random_timestamps(self, reference_ts, window_days)` -- Generate randomized timestamps within a window around the reference.
- `Timestomper.verify_timestamps` (method) `modules/timestomper.py:300` `def verify_timestamps(self, target_paths)` -- Verify timestamps on target files after modification.
- `Timestomper.summary` (method) `modules/timestomper.py:324` `def summary(self)` -- Return a summary of available timestomping capabilities.

## modules/tool_extractor.py
Depends on: `modules/agent_tool.py`
- `extract_tools_from_source` (function) `modules/tool_extractor.py:6` `def extract_tools_from_source(file_path, class_name, prefix)` -- Extrae AgentTool desde archivos Python (ideal para cmd2)

## modules/toposwarm_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/ai_fallback.py`, `modules/hive_invoke.py`, `modules/moe_router.py`, `modules/unified_bridge.py`, `skills/toposwarm_autonomous.py`
- `RoutedCall.lazyown_command` (method) `modules/toposwarm_bridge.py:77` `def lazyown_command(self)` -- Return the LazyOwn shell command string to execute this tool call.
- `OnlineFeedbackLoop.__init__` (method) `modules/toposwarm_bridge.py:289` `def __init__(self, maxsize)`
- `OnlineFeedbackLoop.register` (method) `modules/toposwarm_bridge.py:296` `def register(self, result, hidden)` -- Register a routing result as pending feedback.
- `OnlineFeedbackLoop.feedback` (method) `modules/toposwarm_bridge.py:311` `def feedback(self, result_id, good, comment, routing_head)` -- Apply feedback for a routing decision.
- `OnlineFeedbackLoop.pending_count` (method) `modules/toposwarm_bridge.py:373` `def pending_count(self)`
- `OnlineFeedbackLoop.stats` (method) `modules/toposwarm_bridge.py:376` `def stats(self)`
- `OnlineFeedbackLoop.load_feedback_for_training` (method) `modules/toposwarm_bridge.py:383` `def load_feedback_for_training(self)` -- Load persisted feedback for --finetune.
- `TopoSwarmBridge.__init__` (method) `modules/toposwarm_bridge.py:421` `def __init__(self)`
- `TopoSwarmBridge.available` (method) `modules/toposwarm_bridge.py:433` `def available(self)` -- True if TopoSwarm directory exists (even if model not loaded).
- `TopoSwarmBridge.model_loaded` (method) `modules/toposwarm_bridge.py:438` `def model_loaded(self)`
- `TopoSwarmBridge.feedback` (method) `modules/toposwarm_bridge.py:544` `def feedback(self, result_id, good, comment)` -- Optional user feedback on a routing decision.
- `TopoSwarmBridge.route` (method) `modules/toposwarm_bridge.py:568` `def route(self, prompt)` -- Route an operator prompt to a LazyOwn tool call.
- `TopoSwarmBridge.execute_via_orchestrator` (method) `modules/toposwarm_bridge.py:595` `def execute_via_orchestrator(self, prompt, no_model)` -- Execute a prompt through the full TopoSwarm orchestrator (subprocess).
- `TopoSwarmBridge.get_bridge` (method) `modules/toposwarm_bridge.py:626` `def get_bridge()` -- Return the module-level TopoSwarmBridge singleton (lazy init).

## modules/traffic_morpher.py
Imported by: `cli/commands/persist_migrated.py`
- `TrafficMorpher.__init__` (method) `modules/traffic_morpher.py:77` `def __init__(self)`
- `TrafficMorpher.get_random_http_headers` (method) `modules/traffic_morpher.py:81` `def get_random_http_headers(self)` -- Return a randomized set of HTTP headers mimicking a real browser.
- `TrafficMorpher.get_cdn_fronting_hosts` (method) `modules/traffic_morpher.py:91` `def get_cdn_fronting_hosts(self, provider, count)` -- Return CDN domains suitable for domain fronting.
- `TrafficMorpher.generate_traffic_padding` (method) `modules/traffic_morpher.py:108` `def generate_traffic_padding(self, min_bytes, max_bytes)` -- Generate random padding bytes to normalize packet sizes.
- `TrafficMorpher.generate_jitter` (method) `modules/traffic_morpher.py:125` `def generate_jitter(self, base_delay, jitter_pct)` -- Calculate a sleep delay with jitter.
- `TrafficMorpher.generate_dns_tunnel_payload` (method) `modules/traffic_morpher.py:138` `def generate_dns_tunnel_payload(self, data, domain)` -- Encode data as DNS query subdomains for tunneling.
- `TrafficMorpher.generate_icmp_exfil_payload` (method) `modules/traffic_morpher.py:164` `def generate_icmp_exfil_payload(self, data, chunk_size)` -- Generate ICMP echo payloads for data exfiltration.
- `TrafficMorpher.generate_websocket_masking` (method) `modules/traffic_morpher.py:190` `def generate_websocket_masking(self, data)` -- Apply WebSocket frame masking with random key.
- `TrafficMorpher.generate_cloudflare_worker_proxy_config` (method) `modules/traffic_morpher.py:205` `def generate_cloudflare_worker_proxy_config(self, c2_host, c2_port, auth_token)` -- Generate a Cloudflare Worker script that proxies C2 traffic.
- `TrafficMorpher.generate_beacon_profile` (method) `modules/traffic_morpher.py:270` `def generate_beacon_profile(self, name, protocol, jitter_pct, user_agent)` -- Generate a complete C2 beacon profile configuration.

## modules/ttp_coverage.py
Depends on: `core/logging.py`
Imported by: `cli/commands/caldera.py`
- `TTPCoverage.__init__` (method) `modules/ttp_coverage.py:68` `def __init__(self)`
- `TTPCoverage.rebuild_from_operations` (method) `modules/ttp_coverage.py:76` `def rebuild_from_operations(self)` -- Re-walk every operation on disk and refresh the matrix.
- `TTPCoverage.add` (method) `modules/ttp_coverage.py:125` `def add(self, technique_id, name, tactic, status, operation_id)`
- `TTPCoverage.compute_ready` (method) `modules/ttp_coverage.py:146` `def compute_ready(self, available_facts)` -- Return the techniques that could run given available facts.
- `TTPCoverage.matrix` (method) `modules/ttp_coverage.py:187` `def matrix(self)` -- Render a coloured-by-tactic table of all techniques.
- `TTPCoverage.status_by_id` (method) `modules/ttp_coverage.py:231` `def status_by_id(self, technique_id)`
- `TTPCoverage.to_dict` (method) `modules/ttp_coverage.py:234` `def to_dict(self)`
- `TTPCoverage.get_coverage` (method) `modules/ttp_coverage.py:260` `def get_coverage()` -- Return a fresh :class:`TTPCoverage`.

## modules/unified_bridge.py
Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/lazyown_bridge.py`, `modules/mcp_agent_bridge.py`, `modules/state_manager.py`, `modules/toposwarm_bridge.py`
Imported by: `lazyown.py`
- `RouteBackend.available` (method) `modules/unified_bridge.py:62` `def available(self)`
- `RouteBackend.route` (method) `modules/unified_bridge.py:65` `def route(self, prompt, context)`
- `KeywordBackend.available` (method) `modules/unified_bridge.py:95` `def available(self)`
- `KeywordBackend.route` (method) `modules/unified_bridge.py:98` `def route(self, prompt, context)`
- `LazyownBridgeBackend.available` (method) `modules/unified_bridge.py:119` `def available(self)`
- `LazyownBridgeBackend.route` (method) `modules/unified_bridge.py:126` `def route(self, prompt, context)`
- `TopoSwarmBackend.available` (method) `modules/unified_bridge.py:154` `def available(self)`
- `TopoSwarmBackend.route` (method) `modules/unified_bridge.py:162` `def route(self, prompt, context)`
- `UnifiedBridge.__init__` (method) `modules/unified_bridge.py:201` `def __init__(self)`
- `UnifiedBridge.get` (method) `modules/unified_bridge.py:212` `def get(cls)`
- `UnifiedBridge.set_publish_callback` (method) `modules/unified_bridge.py:217` `def set_publish_callback(self, cb)`
- `UnifiedBridge.route` (method) `modules/unified_bridge.py:237` `def route(self, prompt, context)` -- Route a natural-language prompt to the best LazyOwn tool.
- `UnifiedBridge.delegate` (method) `modules/unified_bridge.py:280` `def delegate(self, goal, backend, timeout)` -- Delegate a complex task to an internal AI agent.
- `UnifiedBridge.list_backends` (method) `modules/unified_bridge.py:332` `def list_backends(self)`
- `UnifiedBridge.route_prompt` (method) `modules/unified_bridge.py:355` `def route_prompt(prompt, context)` -- Convenience: route a prompt without instantiating UnifiedBridge.
- `UnifiedBridge.delegate_task` (method) `modules/unified_bridge.py:360` `def delegate_task(goal, backend)` -- Convenience: delegate a task to an AI agent.

## modules/unified_dashboard.py
Depends on: `cli/graph_advisor.py`, `core/logging.py`, `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/live_surface.py`, `modules/world_model.py`, `skills/hive_mind.py`, `skills/lazyown_policy.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_unified_dashboard.py`
- `UnifiedDashboard.__init__` (method) `modules/unified_dashboard.py:43` `def __init__(self, sessions_dir)`
- `UnifiedDashboard.build_unified_snapshot` (method) `modules/unified_dashboard.py:73` `def build_unified_snapshot(self)` -- Build a complete dashboard snapshot from all data sources.
- `UnifiedDashboard.render_unified` (method) `modules/unified_dashboard.py:167` `def render_unified(self)` -- Render the unified dashboard as a text string for CLI/TUI.
- `UnifiedDashboard.export_json` (method) `modules/unified_dashboard.py:248` `def export_json(self)` -- Export the unified snapshot as a JSON string.
- `UnifiedDashboard.get_unified_dashboard` (method) `modules/unified_dashboard.py:253` `def get_unified_dashboard(sessions_dir)` -- Return a module-level :class:`UnifiedDashboard` singleton.

## modules/venator.py
- `getUUID` (function) `modules/venator.py:37` `def getUUID()`
- `io_key` (function) `modules/venator.py:45` `def io_key(keyname)`
- `getSystemInfo` (function) `modules/venator.py:55` `def getSystemInfo(output_file)`
- `getVTResult` (function) `modules/venator.py:71` `def getVTResult(fileHash)`
- `getHash` (function) `modules/venator.py:100` `def getHash(file, ignoreVFlag)`
- `checkSignature` (function) `modules/venator.py:119` `def checkSignature(file, bundle)`
- `datetime_handler` (function) `modules/venator.py:186` `def datetime_handler(x)`
- `parseAgentsDaemons` (function) `modules/venator.py:190` `def parseAgentsDaemons(item, path)`
- `getLaunchAgents` (function) `modules/venator.py:261` `def getLaunchAgents(path, output_file, ignoreVFlag)`
- `getLaunchDaemons` (function) `modules/venator.py:275` `def getLaunchDaemons(path, output_file, ignoreVFlag)`
- `getUsers` (function) `modules/venator.py:289` `def getUsers(output_file)`
- `getSafariExtensions` (function) `modules/venator.py:309` `def getSafariExtensions(path, output_file)`
- `getChromeExtensions` (function) `modules/venator.py:327` `def getChromeExtensions(path, output_file)`
- `getChromeDownloads` (function) `modules/venator.py:357` `def getChromeDownloads(chromeHistoryDbPath, output_file)`
- `getFirefoxExtensions` (function) `modules/venator.py:398` `def getFirefoxExtensions(path, output_file)`
- `getInstallHistory` (function) `modules/venator.py:432` `def getInstallHistory(output_file)`
- `getCronJobs` (function) `modules/venator.py:449` `def getCronJobs(users, output_file)`
- `getEmond` (function) `modules/venator.py:465` `def getEmond(output_file)`
- `getKext` (function) `modules/venator.py:481` `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)`
- `getEnv` (function) `modules/venator.py:527` `def getEnv(output_file)`
- `getPeriodicScripts` (function) `modules/venator.py:541` `def getPeriodicScripts(output_file)`
- `getConnections` (function) `modules/venator.py:557` `def getConnections(output_file)`
- `SIPStatus` (function) `modules/venator.py:584` `def SIPStatus(output_file)`
- `GatekeeperStatus` (function) `modules/venator.py:598` `def GatekeeperStatus(output_file)`
- `parseApp` (function) `modules/venator.py:609` `def parseApp(app, ignoreVFlag)`
- `getLoginItems` (function) `modules/venator.py:651` `def getLoginItems(path, output_file, ignoreVFlag)`
- `getApps` (function) `modules/venator.py:681` `def getApps(path, output_file, ignoreVFlag)`
- `getEventTaps` (function) `modules/venator.py:704` `def getEventTaps(output_file)`
- `getBashHistory` (function) `modules/venator.py:724` `def getBashHistory(output_file, users)`
- `getShellStartupScripts` (function) `modules/venator.py:741` `def getShellStartupScripts(users, output_file)`
- `hmac_sha256` (function) `modules/venator.py:781` `def hmac_sha256(key, data)`
- `amzn_sig` (function) `modules/venator.py:785` `def amzn_sig(secret_access_key, data, aws_region, aws_service)`
- `amzn_canonical_req` (function) `modules/venator.py:795` `def amzn_canonical_req(filename_path, headers_list)`
- `s3_upload` (function) `modules/venator.py:807` `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)`

## modules/vuln_agent.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/agent_tool.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- `configure_logging` (function) `modules/vuln_agent.py:35` `def configure_logging(debug)`
- `LazyOwnShellWrapper.__init__` (method) `modules/vuln_agent.py:42` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/vuln_agent.py:84` `def execute_command(self, command)` -- Ejecuta un comando en la CLI y retorna el output
- `LazyOwnShellWrapper.get_available_commands` (method) `modules/vuln_agent.py:110` `def get_available_commands(self)` -- Retorna lista de comandos disponibles
- `VulnBotCLI.__init__` (method) `modules/vuln_agent.py:122` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.run_cli_command` (method) `modules/vuln_agent.py:188` `def run_cli_command(command)` -- Ejecuta un comando directamente en la CLI de pentesting
- `VulnBotCLI.read_file` (method) `modules/vuln_agent.py:208` `def read_file(path)`
- `VulnBotCLI.read_file_content` (method) `modules/vuln_agent.py:213` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vuln_agent.py:223` `def load_knowledge_base(self)`
- `VulnBotCLI.save_knowledge_base` (method) `modules/vuln_agent.py:229` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vuln_agent.py:233` `def get_relevant_knowledge(self, prompt)`
- `VulnBotCLI.add_to_knowledge_base` (method) `modules/vuln_agent.py:238` `def add_to_knowledge_base(self, prompt, response)`
- `VulnBotCLI.process_with_context` (method) `modules/vuln_agent.py:244` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.generate` (method) `modules/vuln_agent.py:280` `def generate()`
- `VulnBotCLI.parse_args` (method) `modules/vuln_agent.py:285` `def parse_args()`
- `VulnBotCLI.interactive_mode` (method) `modules/vuln_agent.py:297` `def interactive_mode(bot)`
- `VulnBotCLI.main` (method) `modules/vuln_agent.py:318` `def main()`

## modules/vuln_bot_cli.py
Depends on: `modules/vulnbot.py`
- `parse_args` (function) `modules/vuln_bot_cli.py:8` `def parse_args()`
- `main` (function) `modules/vuln_bot_cli.py:17` `def main()`

## modules/vulnbot.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/vuln_bot_cli.py`
- `VulnBotCLI.__init__` (method) `modules/vulnbot.py:29` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.list_files` (method) `modules/vulnbot.py:84` `def list_files(directory)` -- Lista archivos en un directorio
- `VulnBotCLI.read_file` (method) `modules/vulnbot.py:88` `def read_file(path)` -- Lee contenido de un archivo
- `VulnBotCLI.edit_file` (method) `modules/vulnbot.py:93` `def edit_file(path, content, old_text)` -- Crea o edita un archivo
- `VulnBotCLI.generate` (method) `modules/vulnbot.py:135` `def generate()`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vulnbot.py:140` `def load_knowledge_base(self)`
- `VulnBotCLI.save_knowledge_base` (method) `modules/vulnbot.py:146` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vulnbot.py:150` `def get_relevant_knowledge(self, prompt)`
- `VulnBotCLI.create_complex_prompt` (method) `modules/vulnbot.py:155` `def create_complex_prompt(self, base_prompt, history, knowledge)`
- `VulnBotCLI.read_file_content` (method) `modules/vulnbot.py:171` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_event_config` (method) `modules/vulnbot.py:177` `def load_event_config(self)`
- `VulnBotCLI.process_with_context` (method) `modules/vulnbot.py:185` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.stream_response` (method) `modules/vulnbot.py:201` `def stream_response(self, prompt)`
- `VulnBotCLI.generate` (method) `modules/vulnbot.py:202` `def generate()`
- `VulnBotCLI.add_to_knowledge_base` (method) `modules/vulnbot.py:207` `def add_to_knowledge_base(self, prompt, response)`

## modules/websocket_beacon.py
Depends on: `core/hardening.py`
- `WebSocketBeacon.__init__` (method) `modules/websocket_beacon.py:62` `def __init__(self, server_url, beacon_id, encryption_key, sleep_seconds, jitter_percent, ssl_verify, proxy)`
- `WebSocketBeacon.connect` (method) `modules/websocket_beacon.py:122` `def connect(self)` -- Establish WebSocket connection to the C2 server.
- `WebSocketBeacon.check_in` (method) `modules/websocket_beacon.py:157` `def check_in(self)` -- Send heartbeat and retrieve pending tasks.
- `WebSocketBeacon.send_result` (method) `modules/websocket_beacon.py:191` `def send_result(self, task_id, output, exit_code)` -- Send command execution result back to C2.
- `WebSocketBeacon.run` (method) `modules/websocket_beacon.py:214` `def run(self, command_handler)` -- Main beacon loop with check-in and command execution.
- `WebSocketBeacon.shutdown` (method) `modules/websocket_beacon.py:263` `def shutdown(self)` -- Gracefully shutdown the beacon.
- `WebSocketC2Handler.__init__` (method) `modules/websocket_beacon.py:288` `def __init__(self, host, port, ssl_context, beacon_callback, task_callback, result_callback)`
- `WebSocketC2Handler.start` (method) `modules/websocket_beacon.py:382` `def start(self)` -- Start the WebSocket C2 server.
- `WebSocketC2Handler.stop` (method) `modules/websocket_beacon.py:392` `def stop(self)` -- Stop the WebSocket C2 server.
- `WebSocketC2Handler.start_in_thread` (method) `modules/websocket_beacon.py:399` `def start_in_thread(self)` -- Start the WebSocket C2 server in a background thread.
- `WebSocketC2Handler.send_task` (method) `modules/websocket_beacon.py:416` `def send_task(self, beacon_id, command)` -- Send a command task to a specific beacon.
- `WebSocketC2Handler.list_beacons` (method) `modules/websocket_beacon.py:447` `def list_beacons(self)` -- List all connected beacons.
- `WebSocketC2Handler.remove_stale_beacons` (method) `modules/websocket_beacon.py:464` `def remove_stale_beacons(self, timeout)` -- Remove beacons that have not checked in within the timeout.

## modules/win_rootkit/backup.c
- `elp` (function) `modules/win_rootkit/backup.c:66` `void elp()`
- `ensure_pid_file_exists` (function) `modules/win_rootkit/backup.c:86` `void ensure_pid_file_exists()`
- `ensure_key_file_exists` (function) `modules/win_rootkit/backup.c:123` `void ensure_key_file_exists()`
- `ensure_hide_file_exists` (function) `modules/win_rootkit/backup.c:150` `void ensure_hide_file_exists()`
- `infect_command` (function) `modules/win_rootkit/backup.c:179` `void infect_command()`
- `handle_client` (function) `modules/win_rootkit/backup.c:204` `DWORD WINAPI handle_client(LPVOID client_socket)`
- `monitor_shell` (function) `modules/win_rootkit/backup.c:430` `DWORD WINAPI monitor_shell(LPVOID data)`
- `main` (function) `modules/win_rootkit/backup.c:540` `int main()`

## modules/win_rootkit/mrhyde.c
- `RunExperiment` (function) `modules/win_rootkit/mrhyde.c:19` `void __cdecl RunExperiment()` -- Define the RunExperiment function
- `load_hidden_pids` (function) `modules/win_rootkit/mrhyde.c:24` `void load_hidden_pids()`
- `load_hidden_files` (function) `modules/win_rootkit/mrhyde.c:47` `void load_hidden_files()`
- `FindProcessId` (function) `modules/win_rootkit/mrhyde.c:89` `DWORD FindProcessId(const char* processName)`
- `HideProcessByPID` (function) `modules/win_rootkit/mrhyde.c:115` `void HideProcessByPID(DWORD pid)`
- `search_pid` (function) `modules/win_rootkit/mrhyde.c:137` `BOOL search_pid()`
- `should_hide_pid` (function) `modules/win_rootkit/mrhyde.c:147` `BOOL should_hide_pid(DWORD pid)`
- `should_hide_file` (function) `modules/win_rootkit/mrhyde.c:161` `BOOL should_hide_file(const char* filename)`
- `HookedFindFirstFile` (function) `modules/win_rootkit/mrhyde.c:171` `HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData)` -- Hook para FindFirstFile
- `HookedFindNextFile` (function) `modules/win_rootkit/mrhyde.c:180` `BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData)` -- Hook para FindNextFile
- `HookedCreateToolhelp32Snapshot` (function) `modules/win_rootkit/mrhyde.c:189` `HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)` -- Hook para CreateToolhelp32Snapshot
- `HookedProcess32First` (function) `modules/win_rootkit/mrhyde.c:198` `BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` -- Hook para Process32First
- `HookedProcess32Next` (function) `modules/win_rootkit/mrhyde.c:210` `BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` -- Hook para Process32Next
- `HookFunctions` (function) `modules/win_rootkit/mrhyde.c:222` `void HookFunctions()` -- Función para realizar el hooking de las funciones
- `DllMain` (function) `modules/win_rootkit/mrhyde.c:272` `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`

## modules/win_rootkit/win_rin3_rootkit.cs
- `SID.GetUsernameFromPid` (method) `modules/win_rootkit/win_rin3_rootkit.cs:143`
- `SID.ShouldHidePid` (method) `modules/win_rootkit/win_rin3_rootkit.cs:201`
- `SID.HookFindFirstFile` (method) `modules/win_rootkit/win_rin3_rootkit.cs:212`
- `SID.HookCreateFile` (method) `modules/win_rootkit/win_rin3_rootkit.cs:224`

## modules/win_rootkit/win_ring3_rootkit.c
- `DownloadDLL` (function) `modules/win_rootkit/win_ring3_rootkit.c:79` `BOOL DownloadDLL(const char* url, PBYTE* buffer, DWORD* size)`
- `ReflectiveLoadDLL` (function) `modules/win_rootkit/win_ring3_rootkit.c:99` `BOOL ReflectiveLoadDLL(PBYTE dllBuffer, DWORD dllSize)`
- `initPIDArray` (function) `modules/win_rootkit/win_ring3_rootkit.c:146` `void initPIDArray(PIDArray *array)` -- Función para inicializar el arreglo de PIDs
- `addPID` (function) `modules/win_rootkit/win_ring3_rootkit.c:153` `void addPID(PIDArray *array, DWORD pid)` -- Función para agregar un PID al arreglo
- `freePIDArray` (function) `modules/win_rootkit/win_ring3_rootkit.c:162` `void freePIDArray(PIDArray *array)` -- Función para liberar la memoria del arreglo de PIDs
- `getPIDsFromTasklist` (function) `modules/win_rootkit/win_ring3_rootkit.c:166` `void getPIDsFromTasklist(PIDArray *pidArray)`
- `AddDllToAppInitDLLs` (function) `modules/win_rootkit/win_ring3_rootkit.c:191` `BOOL AddDllToAppInitDLLs(const char* dllPath)`
- `GetProcessIdByName` (function) `modules/win_rootkit/win_ring3_rootkit.c:240` `DWORD GetProcessIdByName(const char* processName)`
- `Gifted` (function) `modules/win_rootkit/win_ring3_rootkit.c:270` `BOOL Gifted(DWORD processId, const char* dllPath)`
- `elp` (function) `modules/win_rootkit/win_ring3_rootkit.c:362` `void elp()`
- `ensure_pid_file_exists` (function) `modules/win_rootkit/win_ring3_rootkit.c:382` `void ensure_pid_file_exists()`
- `ensure_key_file_exists` (function) `modules/win_rootkit/win_ring3_rootkit.c:419` `void ensure_key_file_exists()`
- `ensure_hide_file_exists` (function) `modules/win_rootkit/win_ring3_rootkit.c:446` `void ensure_hide_file_exists()`
- `giveGift` (function) `modules/win_rootkit/win_ring3_rootkit.c:475` `BOOL giveGift()`
- `handle_client` (function) `modules/win_rootkit/win_ring3_rootkit.c:526` `DWORD WINAPI handle_client(LPVOID client_socket)`
- `monitor_shell` (function) `modules/win_rootkit/win_ring3_rootkit.c:755` `DWORD WINAPI monitor_shell(LPVOID data)`
- `main` (function) `modules/win_rootkit/win_ring3_rootkit.c:865` `int main()`

## modules/win_rootkit/win_ring3_rootkit.cpp
- `get_username_from_pid` (function) `modules/win_rootkit/win_ring3_rootkit.cpp:42` `char* get_username_from_pid(DWORD pid)`
- `should_hide_pid` (function) `modules/win_rootkit/win_ring3_rootkit.cpp:65` `int should_hide_pid(const char* pid)`
- `hook_FindFirstFile` (function) `modules/win_rootkit/win_ring3_rootkit.cpp:75` `HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)`
- `hook_CreateFile` (function) `modules/win_rootkit/win_ring3_rootkit.cpp:85` `HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES ...`
- `DllMain` (function) `modules/win_rootkit/win_ring3_rootkit.cpp:94` `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`

## modules/world_model.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/pwn.py`, `cli/ops_commands.py`, `lazyc2.py`, `modules/exploit_recommender.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/live_surface.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/state_manager.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_moe_rl_swan.py`, `tests/test_ops_loot_phase.py`, `tests/test_phase1_data_gaps.py`, `tests/test_world_model_extended.py`
- `read_state_dict` (function) `modules/world_model.py:74` `def read_state_dict(path)` -- Read a world-model state dict, transparently decrypting at rest.
- `write_state_dict` (function) `modules/world_model.py:119` `def write_state_dict(path, data)` -- Atomically write a world-model state dict as plaintext.
- `HostState.rank` (method) `modules/world_model.py:161` `def rank(self)`
- `HostState.can_advance_to` (method) `modules/world_model.py:164` `def can_advance_to(self, next_state)`
- `NetworkGraph.__init__` (method) `modules/world_model.py:268` `def __init__(self)`
- `NetworkGraph.add_relation` (method) `modules/world_model.py:275` `def add_relation(self, relation)` -- Add a directed edge.
- `NetworkGraph.neighbors` (method) `modules/world_model.py:283` `def neighbors(self, node)` -- Return nodes reachable from *node* in one outbound hop.
- `NetworkGraph.in_degree` (method) `modules/world_model.py:287` `def in_degree(self, node)` -- Count edges pointing INTO *node*.
- `NetworkGraph.out_degree` (method) `modules/world_model.py:291` `def out_degree(self, node)` -- Count edges leaving *node*.
- `NetworkGraph.degree_centrality` (method) `modules/world_model.py:295` `def degree_centrality(self)` -- Return (node, centrality_score) pairs sorted descending by score.
- `NetworkGraph.pivot_candidates` (method) `modules/world_model.py:310` `def pivot_candidates(self, top_k)` -- Return the *top_k* highest-centrality nodes as pivot candidates.
- `NetworkGraph.to_dict` (method) `modules/world_model.py:332` `def to_dict(self)`
- `NetworkGraph.from_dict` (method) `modules/world_model.py:349` `def from_dict(cls, data)`
- `HostEntry.add_service` (method) `modules/world_model.py:374` `def add_service(self, svc)`
- `HostEntry.advance` (method) `modules/world_model.py:378` `def advance(self, new_state)` -- Advance state only if new_state is the next valid step.
- `HostEntry.to_dict` (method) `modules/world_model.py:386` `def to_dict(self)`
- `HostEntry.from_dict` (method) `modules/world_model.py:398` `def from_dict(cls, d)`
- `_PhaseDeriver.derive` (method) `modules/world_model.py:431` `def derive(self, hosts)`
- `WorldModel.__init__` (method) `modules/world_model.py:517` `def __init__(self, path)`
- `WorldModel.add_host` (method) `modules/world_model.py:533` `def add_host(self, ip)`
- `WorldModel.reset_host` (method) `modules/world_model.py:541` `def reset_host(self, ip)` -- Clear a single host's state back to UNSCANNED for a fresh scan.
- `WorldModel.advance_host` (method) `modules/world_model.py:551` `def advance_host(self, ip, new_state)`
- `WorldModel.add_service` (method) `modules/world_model.py:560` `def add_service(self, ip, port, name, version, protocol)`
- `WorldModel.add_note` (method) `modules/world_model.py:577` `def add_note(self, ip, note)`
- `WorldModel.set_os_hint` (method) `modules/world_model.py:584` `def set_os_hint(self, ip, os_hint)` -- Set the operating system hint for a host.
- `WorldModel.get_host` (method) `modules/world_model.py:598` `def get_host(self, ip)` -- Return a host entry by IP, or None if not found.
- `WorldModel.get_hosts_summary` (method) `modules/world_model.py:610` `def get_hosts_summary(self)` -- Return a mapping of IP -> state for all tracked hosts.
- `WorldModel.add_credential` (method) `modules/world_model.py:621` `def add_credential(self, value, host, service)`
- `WorldModel.link_credential_to_success` (method) `modules/world_model.py:653` `def link_credential_to_success(self, value, host)` -- Mark a credential as working for a specific host in the graph.
- `WorldModel.link_credential_to_failure` (method) `modules/world_model.py:674` `def link_credential_to_failure(self, value, host)` -- Mark a credential as rejected by a specific host in the graph.
- `WorldModel.add_vulnerability` (method) `modules/world_model.py:704` `def add_vulnerability(self, description, host, cve, severity)`
- `WorldModel.add_email` (method) `modules/world_model.py:710` `def add_email(self, address, host, context)`
- `WorldModel.add_domain` (method) `modules/world_model.py:716` `def add_domain(self, domain, host, context)`
- `WorldModel.update_from_findings` (method) `modules/world_model.py:730` `def update_from_findings(self, findings)` -- Integrate a list of Finding objects (from obs_parser.ObsParser).
- `WorldModel.consume_policy_facts` (method) `modules/world_model.py:803` `def consume_policy_facts(self, facts_path)` -- Ingest structured facts from FactStore's ``policy_facts.json``.
- `WorldModel.add_relation` (method) `modules/world_model.py:895` `def add_relation(self, source, target, relation, weight)` -- Add an arbitrary directed relationship to the network graph.
- `WorldModel.pivot_candidates` (method) `modules/world_model.py:916` `def pivot_candidates(self, top_k)` -- Return the top_k highest-centrality nodes as pivot candidates.
- `WorldModel.graph_snapshot` (method) `modules/world_model.py:924` `def graph_snapshot(self)` -- Return the full network graph as a serialisable dict.
- `WorldModel.get_phase` (method) `modules/world_model.py:931` `def get_phase(self)`
- `WorldModel.get_suggested_tools` (method) `modules/world_model.py:935` `def get_suggested_tools(self)`
- `WorldModel.to_context_string` (method) `modules/world_model.py:938` `def to_context_string(self)` -- Compact, LLM-readable summary of the current engagement state.
- `WorldModel.reload` (method) `modules/world_model.py:1042` `def reload(self)` -- Discard in-memory state and re-read from the persisted file.
- `WorldModel.reset` (method) `modules/world_model.py:1058` `def reset(self)` -- Clear all state and delete the persisted file.
- `WorldModel.snapshot` (method) `modules/world_model.py:1069` `def snapshot(self)` -- Return a plain-dict snapshot (for JSON serialisation).
- `WorldModel.get_world_model` (method) `modules/world_model.py:1090` `def get_world_model(path)` -- Return (or create) the module-level singleton WorldModel.

## modules/yaml_generator.py
Depends on: `modules/ai_model.py`, `modules/llm_factory.py`
- `YAMLPromptGenerator.__init__` (method) `modules/yaml_generator.py:18` `def __init__(self, provider, api_key)`
- `YAMLPromptGenerator.load_payload` (method) `modules/yaml_generator.py:25` `def load_payload(self)` -- Carga las variables desde payload.json
- `YAMLPromptGenerator.generate_prompt` (method) `modules/yaml_generator.py:54` `def generate_prompt(self, user_request)` -- Genera el prompt para la IA en inglés
- `YAMLPromptGenerator.extract_yaml_from_markdown` (method) `modules/yaml_generator.py:100` `def extract_yaml_from_markdown(self, text)` -- Extrae el primer bloque YAML entre ```yaml y ```
- `YAMLPromptGenerator.create_yaml_addon` (method) `modules/yaml_generator.py:109` `def create_yaml_addon(self, user_request, output_dir)` -- Genera el YAML y lo guarda en disco
- `YAMLPromptGenerator.main` (method) `modules/yaml_generator.py:140` `def main()`

## modules/yara_scanner.py
Imported by: `cli/commands/postexp_migrated.py`, `modules/intelligence_engine.py`
- `YaraScanner.__init__` (method) `modules/yara_scanner.py:30` `def __init__(self, rules_dir, auto_compile)`
- `YaraScanner.ensure_directory` (method) `modules/yara_scanner.py:40` `def ensure_directory(self)` -- Create the YARA rules directory if it does not exist.
- `YaraScanner.compile_all` (method) `modules/yara_scanner.py:53` `def compile_all(self)` -- Compile all .yar files in the rules directory.
- `YaraScanner.scan_file` (method) `modules/yara_scanner.py:97` `def scan_file(self, filepath, timeout)` -- Scan a single file with all compiled YARA rules.
- `YaraScanner.target` (method) `modules/yara_scanner.py:137` `def target()`
- `YaraScanner.scan_directory` (method) `modules/yara_scanner.py:186` `def scan_directory(self, directory, recursive, extensions, max_files)` -- Scan all files in a directory recursively.
- `YaraScanner.add_rule` (method) `modules/yara_scanner.py:255` `def add_rule(self, name, content)` -- Add a new YARA rule to the rules directory.
- `YaraScanner.list_rules` (method) `modules/yara_scanner.py:274` `def list_rules(self)` -- List all YARA rules in the rules directory.
- `YaraScanner.download_community_rules` (method) `modules/yara_scanner.py:295` `def download_community_rules(self)` -- Attempt to download community YARA rules from popular repositories.
- `YaraScanner.ioc_scan` (method) `modules/yara_scanner.py:327` `def ioc_scan(self, target_path, iocs)` -- Scan for IOCs (hashes, strings, registry keys) in a file/directory.
- `YaraScanner.create_default_rules` (method) `modules/yara_scanner.py:366` `def create_default_rules()` -- Create a set of default YARA rules for common threats.

## plugins/generate_c_reverse_shell.lua
- `generate_c_reverse_shell` (function) `plugins/generate_c_reverse_shell.lua:1`
- `all` (function) `plugins/generate_c_reverse_shell.lua:108`

## plugins/generate_cleanup_commands.lua
- `generate_cleanup_commands` (function) `plugins/generate_cleanup_commands.lua:3`

## plugins/generate_html_payload.lua
- `generate_html_payload` (function) `plugins/generate_html_payload.lua:1`

## plugins/generate_lateral_command.lua
- `generate_lateral_command` (function) `plugins/generate_lateral_command.lua:4`

## plugins/generate_linux_asm_reverse_shell.lua
- `generate_linux_asm_reverse_shell` (function) `plugins/generate_linux_asm_reverse_shell.lua:1`
- `all` (function) `plugins/generate_linux_asm_reverse_shell.lua:121`

## plugins/generate_linux_raw_shellcode.lua
- `generate_linux_raw_shellcode` (function) `plugins/generate_linux_raw_shellcode.lua:1`

## plugins/generate_lolbird.lua
- `write_file` (function) `plugins/generate_lolbird.lua:4`
- `read_file` (function) `plugins/generate_lolbird.lua:12`
- `xor_hex_string` (function) `plugins/generate_lolbird.lua:21`
- `xor_string` (function) `plugins/generate_lolbird.lua:31`
- `generate_lolbird_ps1` (function) `plugins/generate_lolbird.lua:44`
- `Xor` (function) `plugins/generate_lolbird.lua:64`

## plugins/generate_msfvenom_loader.lua
- `execute_command_to_file` (function) `plugins/generate_msfvenom_loader.lua:2`
- `read_file` (function) `plugins/generate_msfvenom_loader.lua:7`
- `hex_to_nasm` (function) `plugins/generate_msfvenom_loader.lua:18`
- `generate_loader` (function) `plugins/generate_msfvenom_loader.lua:49`
- `generate_msfvenom_loader` (function) `plugins/generate_msfvenom_loader.lua:104`

## plugins/generate_msfvenom_loader_windows.lua
- `generate_msfvenom_loader_windows` (function) `plugins/generate_msfvenom_loader_windows.lua:2`

## plugins/generate_reverse_shell.lua
- `generate_reverse_shell` (function) `plugins/generate_reverse_shell.lua:1`

## plugins/generate_stub.lua
- `write_file` (function) `plugins/generate_stub.lua:4`
- `read_file` (function) `plugins/generate_stub.lua:12`
- `xor_data` (function) `plugins/generate_stub.lua:21`
- `xor_string` (function) `plugins/generate_stub.lua:30`
- `generate_stub_ps1` (function) `plugins/generate_stub.lua:43`

## plugins/init_plugins.lua
- `load_plugin` (function) `plugins/init_plugins.lua:6`

## plugins/kerberos_harvest.lua
- `kerberos_harvest` (function) `plugins/kerberos_harvest.lua:1`

## plugins/lolbas_certutil_download_exec.lua
- `write_file` (function) `plugins/lolbas_certutil_download_exec.lua:5`
- `read_file` (function) `plugins/lolbas_certutil_download_exec.lua:13`
- `xor_data` (function) `plugins/lolbas_certutil_download_exec.lua:21`

## plugins/lolbas_certutil_exe.lua
- `run_msfvenom` (function) `plugins/lolbas_certutil_exe.lua:2`

## plugins/lolbas_wmic_xsl_execution.lua
- `write_file` (function) `plugins/lolbas_wmic_xsl_execution.lua:4`

## plugins/parse_nmap_with_xmlstarlet.lua
- `parse_nmap_with_xmlstarlet` (function) `plugins/parse_nmap_with_xmlstarlet.lua:1`

## plugins/run_nuclei_on_nmap_files.lua
- `run_nuclei_on_nmap_files` (function) `plugins/run_nuclei_on_nmap_files.lua:1`

## plugins/run_python_rev_c2.lua
- `run_python_rev_c2` (function) `plugins/run_python_rev_c2.lua:2`


Next: [API_p15.md](API_p15.md)
