# API (page 15 of 21)
Previous: [API_p14.md](API_p14.md)

## modules/session_reader.py
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ImplantRecord.is_privileged` (method) `modules/session_reader.py:55` `def is_privileged(self)`
- `ImplantRecord.platform` (method) `modules/session_reader.py:60` `def platform(self)`
- `ImplantRecord.ip_list` (method) `modules/session_reader.py:69` `def ip_list(self)`
- `SessionSummary.active_client_ids` (method) `modules/session_reader.py:94` `def active_client_ids(self)`
- `SessionSummary.privileged_sessions` (method) `modules/session_reader.py:101` `def privileged_sessions(self)`
- `SessionSummary.unprivileged_sessions` (method) `modules/session_reader.py:108` `def unprivileged_sessions(self)`
- `SessionSummary.latest_for` (method) `modules/session_reader.py:114` `def latest_for(self, client_id)`
- `SessionSummary.task_by_status` (method) `modules/session_reader.py:118` `def task_by_status(self, status)`
- `AbstractReader.read` (method) `modules/session_reader.py:129` `def read(self, sessions_dir)`
- `ImplantCSVReader.read` (method) `modules/session_reader.py:157` `def read(self, sessions_dir)`
- `CommandOutputReader.read` (method) `modules/session_reader.py:199` `def read(self, sessions_dir)`
- `DiscoveredHostReader.read` (method) `modules/session_reader.py:217` `def read(self, sessions_dir)`
- `TaskReader.read` (method) `modules/session_reader.py:235` `def read(self, sessions_dir)`
- `TaskWriter.__init__` (method) `modules/session_reader.py:260` `def __init__(self, sessions_dir)`
- `TaskWriter.append` (method) `modules/session_reader.py:263` `def append(self, title, description, operator, status)`
- `TaskWriter.update_status` (method) `modules/session_reader.py:288` `def update_status(self, task_id, status)`
- `SessionAggregator.__init__` (method) `modules/session_reader.py:319` `def __init__(self, implant_reader, output_reader, host_reader, task_reader)`
- `SessionAggregator.aggregate` (method) `modules/session_reader.py:331` `def aggregate(self, sessions_dir)`
- `SessionAggregator.get_aggregator` (method) `modules/session_reader.py:347` `def get_aggregator()`

## modules/session_state.py
Imported by: `modules/recommender.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `build_state` (function) `modules/session_state.py:189` `def build_state()` -- Assemble and return the current session state dict.
- `refresh` (function) `modules/session_state.py:240` `def refresh()` -- Build state and persist to sessions/session_state.json.
- `load` (function) `modules/session_state.py:251` `def load()` -- Return the last written state, or build it fresh if stale/missing.

## modules/sidequestion.py
Imported by: `cli/commands/ai.py`, `tests/test_autonomous_ops.py`
- `SideQuestionService.__init__` (method) `modules/sidequestion.py:55` `def __init__(self, answer_fn, config)` -- Initialize registries with an optional answer function.
- `SideQuestionService.capture` (method) `modules/sidequestion.py:66` `def capture(self, task_id, text)` -- Freeze main-loop context into an immutable snapshot.
- `SideQuestionService.ask` (method) `modules/sidequestion.py:75` `def ask(self, snapshot_id, question)` -- Answer from a snapshot without touching main state.
- `SideQuestionService.cancel` (method) `modules/sidequestion.py:104` `def cancel(self, request_id)` -- Mark a pending request cancelled.
- `SideQuestionService.history` (method) `modules/sidequestion.py:113` `def history(self, limit, before)` -- Page request history newest first.

## modules/sleep_obfuscation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/sleep_obfuscation.py`, `modules/beacon_config_builder.py`, `tests/test_sleep_obfuscation.py`
- `SleepObfuscationConfig.to_dict` (method) `modules/sleep_obfuscation.py:129` `def to_dict(self)` -- Serialize to dictionary.
- `SleepObfuscationConfig.from_dict` (method) `modules/sleep_obfuscation.py:146` `def from_dict(cls, raw)` -- Build from dictionary.
- `SleepTechniqueCatalog.__init__` (method) `modules/sleep_obfuscation.py:170` `def __init__(self)`
- `SleepTechniqueCatalog.register` (method) `modules/sleep_obfuscation.py:173` `def register(self, technique)` -- Register a technique in the catalog.
- `SleepTechniqueCatalog.get` (method) `modules/sleep_obfuscation.py:177` `def get(self, name)` -- Retrieve a technique by name.
- `SleepTechniqueCatalog.list_all` (method) `modules/sleep_obfuscation.py:184` `def list_all(self)` -- Return all registered techniques sorted by detection resistance.
- `SleepTechniqueCatalog.list_by_platform` (method) `modules/sleep_obfuscation.py:192` `def list_by_platform(self, platform)` -- Return techniques supported on a given platform.
- `SleepTechniqueCatalog.list_names` (method) `modules/sleep_obfuscation.py:196` `def list_names(self)` -- Return sorted list of technique names.
- `SleepTechniqueValidator.validate` (method) `modules/sleep_obfuscation.py:369` `def validate(config, technique)` -- Validate config against a technique definition.
- `SleepTechniqueValidator.validate_config` (method) `modules/sleep_obfuscation.py:386` `def validate_config(config)` -- Validate the config itself for internal consistency.
- `SleepObfuscationEngine.__init__` (method) `modules/sleep_obfuscation.py:407` `def __init__(self, catalog)`
- `SleepObfuscationEngine.catalog` (method) `modules/sleep_obfuscation.py:416` `def catalog(self)` -- Return the technique catalog.
- `SleepObfuscationEngine.config` (method) `modules/sleep_obfuscation.py:421` `def config(self)` -- Return the active runtime configuration.
- `SleepObfuscationEngine.detection_resistance` (method) `modules/sleep_obfuscation.py:426` `def detection_resistance(self)` -- Return the detection resistance score of the active technique.
- `SleepObfuscationEngine.select` (method) `modules/sleep_obfuscation.py:442` `def select(self, technique_name)` -- Select a technique from the catalog.
- `SleepObfuscationEngine.configure` (method) `modules/sleep_obfuscation.py:449` `def configure(self, technique, overrides)` -- Build a validated SleepObfuscationConfig for a technique.
- `SleepObfuscationEngine.validate` (method) `modules/sleep_obfuscation.py:484` `def validate(self, config)` -- Validate configuration against the active technique.
- `SleepObfuscationEngine.recommend` (method) `modules/sleep_obfuscation.py:500` `def recommend(self, platform)` -- Recommend techniques for a platform sorted by detection resistance.
- `SleepObfuscationEngine.to_dict` (method) `modules/sleep_obfuscation.py:513` `def to_dict(self)` -- Serialize the entire engine state to a dictionary.
- `SleepObfuscationEngine.from_dict` (method) `modules/sleep_obfuscation.py:522` `def from_dict(cls, raw)` -- Build an engine from a serialized state dictionary.

## modules/socks_proxy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/socks_proxy.py`, `modules/beacon_config_builder.py`, `tests/test_socks_proxy.py`
- `SocksReply.message` (method) `modules/socks_proxy.py:103` `def message(self)` -- Return a human-readable message for this reply code.
- `SocksSession.elapsed_seconds` (method) `modules/socks_proxy.py:144` `def elapsed_seconds(self)` -- Return seconds since session creation.
- `SocksSession.to_dict` (method) `modules/socks_proxy.py:150` `def to_dict(self)` -- Serialize session to dictionary.
- `SocksProxyConfig.to_dict` (method) `modules/socks_proxy.py:199` `def to_dict(self)` -- Serialize config to dictionary.
- `SocksProxyConfig.from_dict` (method) `modules/socks_proxy.py:218` `def from_dict(cls, raw)` -- Build config from dictionary.
- `SocksValidator.validate_config` (method) `modules/socks_proxy.py:253` `def validate_config(config)` -- Validate a SocksProxyConfig and return error messages.
- `SocksValidator.validate_request` (method) `modules/socks_proxy.py:300` `def validate_request(command, address_type, host, port, config)` -- Validate a SOCKS5 request against the proxy configuration.
- `SocksProxyEngine.__init__` (method) `modules/socks_proxy.py:381` `def __init__(self, config)`
- `SocksProxyEngine.config` (method) `modules/socks_proxy.py:387` `def config(self)` -- Return the current proxy configuration.
- `SocksProxyEngine.sessions` (method) `modules/socks_proxy.py:392` `def sessions(self)` -- Return active proxied sessions.
- `SocksProxyEngine.session_count` (method) `modules/socks_proxy.py:397` `def session_count(self)` -- Return the number of active sessions.
- `SocksProxyEngine.validate` (method) `modules/socks_proxy.py:401` `def validate(self, config)` -- Validate the configuration.
- `SocksProxyEngine.build_spec` (method) `modules/socks_proxy.py:413` `def build_spec(self)` -- Build a JSON-serializable proxy specification for beacon delivery.
- `SocksProxyEngine.create_session` (method) `modules/socks_proxy.py:436` `def create_session(self, session_id, target_host, target_port, beacon_client_id)` -- Create and track a new proxied session.
- `SocksProxyEngine.remove_session` (method) `modules/socks_proxy.py:475` `def remove_session(self, session_id)` -- Remove a session by ID.
- `SocksProxyEngine.get_session` (method) `modules/socks_proxy.py:482` `def get_session(self, session_id)` -- Return a session by ID, or None.
- `SocksProxyEngine.add_bytes` (method) `modules/socks_proxy.py:486` `def add_bytes(self, session_id, sent, received)` -- Update byte counters for a session.
- `SocksProxyEngine.cleanup_expired` (method) `modules/socks_proxy.py:497` `def cleanup_expired(self)` -- Remove sessions that have exceeded the timeout.
- `SocksProxyEngine.list_sessions` (method) `modules/socks_proxy.py:511` `def list_sessions(self)` -- Return a list of all active sessions as dictionaries.
- `SocksProxyEngine.from_dict` (method) `modules/socks_proxy.py:522` `def from_dict(cls, raw)` -- Build a SocksProxyEngine from a configuration dictionary.
- `SocksProxyEngine.from_payload` (method) `modules/socks_proxy.py:528` `def from_payload(cls, payload)` -- Build a SocksProxyEngine from a LazyOwn payload configuration.

## modules/staged_delivery.py
Imported by: `cli/commands/payload_arsenal.py`
- `StagedDeliveryFactory.__init__` (method) `modules/staged_delivery.py:83` `def __init__(self, config, output_dir)`
- `StagedDeliveryFactory.generate_hta` (method) `modules/staged_delivery.py:134` `def generate_hta(self)` -- Generate an HTA (HTML Application) dropper.
- `StagedDeliveryFactory.generate_vba_macro` (method) `modules/staged_delivery.py:171` `def generate_vba_macro(self)` -- Generate a VBA macro for Office documents (Word/Excel).
- `StagedDeliveryFactory.generate_xlm_macro` (method) `modules/staged_delivery.py:219` `def generate_xlm_macro(self)` -- Generate an Excel 4.0 (XLM) macro for legacy macro execution.
- `StagedDeliveryFactory.generate_lnk` (method) `modules/staged_delivery.py:237` `def generate_lnk(self)` -- Generate a Windows .lnk shortcut file with embedded command execution.
- `StagedDeliveryFactory.generate_iso` (method) `modules/staged_delivery.py:301` `def generate_iso(self, inner_files)` -- Generate an ISO 9660 image with an embedded payload autorun.
- `StagedDeliveryFactory.generate_vhd` (method) `modules/staged_delivery.py:370` `def generate_vhd(self, inner_files)` -- Generate a VHD (Virtual Hard Disk) image with embedded payloads.
- `StagedDeliveryFactory.generate_all` (method) `modules/staged_delivery.py:420` `def generate_all(self)` -- Generate all delivery formats for the current configuration.
- `StagedDeliveryFactory.generate_phishing_page` (method) `modules/staged_delivery.py:460` `def generate_phishing_page(self, template)` -- Generate a credential harvesting HTML page.

## modules/state_manager.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/event_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `lazyown.py`, `modules/conditional_hooks.py`, `modules/event_consumers.py`, `modules/unified_bridge.py`
- `StateManager.__init__` (method) `modules/state_manager.py:107` `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)`
- `StateManager.instance` (method) `modules/state_manager.py:129` `def instance(cls)`
- `StateManager.db` (method) `modules/state_manager.py:137` `def db(self)`
- `StateManager.workspace_id` (method) `modules/state_manager.py:146` `def workspace_id(self)`
- `StateManager.set_payload` (method) `modules/state_manager.py:165` `def set_payload(self, payload)`
- `StateManager.close` (method) `modules/state_manager.py:202` `def close(self)`
- `StateManager.add_host` (method) `modules/state_manager.py:213` `def add_host(self, address, mac, hostname, os, state)`
- `StateManager.get_host` (method) `modules/state_manager.py:236` `def get_host(self, address)`
- `StateManager.list_hosts` (method) `modules/state_manager.py:245` `def list_hosts(self)`
- `StateManager.advance_host` (method) `modules/state_manager.py:249` `def advance_host(self, address, new_state)`
- `StateManager.delete_host` (method) `modules/state_manager.py:275` `def delete_host(self, address)`
- `StateManager.add_service` (method) `modules/state_manager.py:287` `def add_service(self, host_address, port, protocol, name, product, version, state)`
- `StateManager.list_services` (method) `modules/state_manager.py:319` `def list_services(self, host_address)`
- `StateManager.add_credential` (method) `modules/state_manager.py:328` `def add_credential(self, host_address, username, password, realm, cred_type, origin)`
- `StateManager.list_credentials` (method) `modules/state_manager.py:362` `def list_credentials(self, host_address)`
- `StateManager.add_vulnerability` (method) `modules/state_manager.py:373` `def add_vulnerability(self, host_address, name, severity, description, refs)`
- `StateManager.list_vulnerabilities` (method) `modules/state_manager.py:398` `def list_vulnerabilities(self, host_address, severity)`
- `StateManager.add_loot` (method) `modules/state_manager.py:411` `def add_loot(self, name, loot_type, path, notes, host_address)`
- `StateManager.list_loot` (method) `modules/state_manager.py:444` `def list_loot(self)`
- `StateManager.add_note` (method) `modules/state_manager.py:450` `def add_note(self, data, note_type, host_address)`
- `StateManager.list_notes` (method) `modules/state_manager.py:473` `def list_notes(self)`
- `StateManager.import_nmap_xml` (method) `modules/state_manager.py:479` `def import_nmap_xml(self, xml_path)`
- `StateManager.import_nmap_from_facts` (method) `modules/state_manager.py:495` `def import_nmap_from_facts(self, facts)` -- Import hosts and services from a FactStore-style facts dict into DB.
- `StateManager.status` (method) `modules/state_manager.py:550` `def status(self)`
- `StateManager.get_world_model_cache` (method) `modules/state_manager.py:606` `def get_world_model_cache(self)`
- `StateManager.load_world_model` (method) `modules/state_manager.py:612` `def load_world_model(self)` -- Return a WorldModel instance populated from DB state.
- `StateManager.session_snapshot` (method) `modules/state_manager.py:653` `def session_snapshot(self)`
- `StateManager.export_csv` (method) `modules/state_manager.py:757` `def export_csv(self, table)`
- `StateManager.export_summary` (method) `modules/state_manager.py:761` `def export_summary(self)`
- `StateManager.get_state_manager` (method) `modules/state_manager.py:776` `def get_state_manager()`

## modules/sudo_tiocsti.py
Depends on: `core/logging.py`
- `get_controlling_tty` (function) `modules/sudo_tiocsti.py:52` `def get_controlling_tty()` -- Return (file_descriptor, tty_path) for the controlling terminal.
- `inject_byte` (function) `modules/sudo_tiocsti.py:64` `def inject_byte(fd, byte_char)` -- Inject a single byte via TIOCSTI; return success status.
- `inject_payload` (function) `modules/sudo_tiocsti.py:79` `def inject_payload(fd, payload, char_delay)` -- Inject a multi‑character payload.
- `get_sudo_pids_on_tty` (function) `modules/sudo_tiocsti.py:102` `def get_sudo_pids_on_tty(tty_path)` -- Return a list of PIDs that are running 'sudo' and have the same controlling terminal as the given tty_path.
- `sudo_cache_valid` (function) `modules/sudo_tiocsti.py:139` `def sudo_cache_valid()` -- Return True if sudo credentials are cached (i.e., sudo -n succeeds).
- `mode_poll` (function) `modules/sudo_tiocsti.py:149` `def mode_poll(fd, tty_path)` -- Poll for sudo processes; inject payload when sudo exits.
- `mode_prefill` (function) `modules/sudo_tiocsti.py:175` `def mode_prefill(fd)` -- Inject payload repeatedly, regardless of sudo state.
- `mode_cache` (function) `modules/sudo_tiocsti.py:185` `def mode_cache(fd)` -- Check sudo cache; if valid, inject sudo -i once.
- `main` (function) `modules/sudo_tiocsti.py:198` `def main()`

## modules/surface_ops.py
Imported by: `cli/commands/surface.py`, `tests/test_estorides_fusion.py`
- `is_ipv4` (function) `modules/surface_ops.py:18` `def is_ipv4(value)` -- Return True for dotted-quad IPv4 literals with 0-255 octets.
- `parse_confirm` (function) `modules/surface_ops.py:26` `def parse_confirm(answer)` -- Return True for an affirmative scan confirmation answer.
- `discovery_targets` (function) `modules/surface_ops.py:31` `def discovery_targets(sessions_dir)` -- List every discovery IP across the sessions discovery files.
- `write_world_model_hosts` (function) `modules/surface_ops.py:50` `def write_world_model_hosts(document, sessions)` -- Append unknown estorides host IPs to world_model.json hosts.

## modules/tel.py
- `get_machine_id` (function) `modules/tel.py:10` `def get_machine_id()`
- `get_version` (function) `modules/tel.py:24` `def get_version()`
- `to_numbers` (function) `modules/tel.py:36` `def to_numbers(hex_str)` -- Simula la función toNumbers de JavaScript
- `to_hex` (function) `modules/tel.py:41` `def to_hex(byte_list)` -- Simula la función toHex de JavaScript
- `decrypt_cookie` (function) `modules/tel.py:46` `def decrypt_cookie(encrypted, key, iv)` -- Descifra usando AES en modo CBC (como slowAES.decrypt(c,2,a,b))
- `main` (function) `modules/tel.py:53` `def main()` -- Sistema de telemetría de uso por instalación no invasiva.

## modules/threat_model.py
Depends on: `core/logging.py`
Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ThreatModelBuilder.build` (method) `modules/threat_model.py:270` `def build(self)`
- `ThreatModelBuilder.load` (method) `modules/threat_model.py:293` `def load(self)`
- `ThreatModelBuilder.get_builder` (method) `modules/threat_model.py:592` `def get_builder()`

## modules/timeline_narrator.py
Depends on: `modules/ai_fallback.py`
Imported by: `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `narrate` (function) `modules/timeline_narrator.py:130` `def narrate(api_key, force)` -- Generate and return the timeline narrative.
- `load_timeline` (function) `modules/timeline_narrator.py:165` `def load_timeline()` -- Return the last written timeline.md or empty string.

## modules/timestomper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `Timestomper.__init__` (method) `modules/timestomper.py:106` `def __init__(self, config)`
- `Timestomper.windows_timestomp_powershell` (method) `modules/timestomper.py:110` `def windows_timestomp_powershell(self)` -- Generate PowerShell commands for Windows file timestomping.
- `Timestomper.windows_timestomp_c` (method) `modules/timestomper.py:152` `def windows_timestomp_c(self)` -- Generate C code for Windows timestomping via SetFileTime API.
- `Timestomper.linux_timestomp_commands` (method) `modules/timestomper.py:200` `def linux_timestomp_commands(self)` -- Generate Linux commands for file timestomping.
- `Timestomper.macos_timestomp_commands` (method) `modules/timestomper.py:241` `def macos_timestomp_commands(self)` -- Generate macOS commands for file timestomping.
- `Timestomper.generate_random_timestamps` (method) `modules/timestomper.py:280` `def generate_random_timestamps(self, reference_ts, window_days)` -- Generate randomized timestamps within a window around the reference.
- `Timestomper.verify_timestamps` (method) `modules/timestomper.py:300` `def verify_timestamps(self, target_paths)` -- Verify timestamps on target files after modification.
- `Timestomper.summary` (method) `modules/timestomper.py:326` `def summary(self)` -- Return a summary of available timestomping capabilities.

## modules/tool_extractor.py
Depends on: `modules/agent_tool.py`
- `extract_tools_from_source` (function) `modules/tool_extractor.py:6` `def extract_tools_from_source(file_path, class_name, prefix)` -- Extrae AgentTool desde archivos Python (ideal para cmd2)

## modules/toolset.py
Imported by: `skills/autonomous_daemon.py`
- `ToolSeed.builtin_seeds` (method) `modules/toolset.py:35` `def builtin_seeds()` -- Return the default graph-tool catalog (handlers stay in code).
- `ToolSeed.resolve` (method) `modules/toolset.py:72` `def resolve(agent, tool_key)` -- Return the seed when bound to agent, else None (LAZY ToolResolve).
- `ToolSeed.extract_tool` (method) `modules/toolset.py:105` `def extract_tool(command)` -- Split tool name with shlex; flag shell metacharacters.
- `ToolSeed.validate_shell` (method) `modules/toolset.py:128` `def validate_shell(role, command)` -- Check a shell command against the role allowlist.

## modules/toposwarm_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/ai_fallback.py`, `modules/hive_invoke.py`, `modules/llm_factory.py`, `modules/moe_router.py`, `modules/unified_bridge.py`, `skills/toposwarm_autonomous.py`
- `RoutedCall.lazyown_command` (method) `modules/toposwarm_bridge.py:81` `def lazyown_command(self)` -- Return the LazyOwn shell command string to execute this tool call.
- `OnlineFeedbackLoop.__init__` (method) `modules/toposwarm_bridge.py:296` `def __init__(self, maxsize)`
- `OnlineFeedbackLoop.register` (method) `modules/toposwarm_bridge.py:303` `def register(self, result, hidden)` -- Register a routing result as pending feedback.
- `OnlineFeedbackLoop.feedback` (method) `modules/toposwarm_bridge.py:318` `def feedback(self, result_id, good, comment, routing_head)` -- Apply feedback for a routing decision.
- `OnlineFeedbackLoop.pending_count` (method) `modules/toposwarm_bridge.py:379` `def pending_count(self)`
- `OnlineFeedbackLoop.stats` (method) `modules/toposwarm_bridge.py:382` `def stats(self)`
- `OnlineFeedbackLoop.load_feedback_for_training` (method) `modules/toposwarm_bridge.py:389` `def load_feedback_for_training(self)` -- Load persisted feedback for --finetune.
- `TopoSwarmBridge.__init__` (method) `modules/toposwarm_bridge.py:432` `def __init__(self)`
- `TopoSwarmBridge.available` (method) `modules/toposwarm_bridge.py:444` `def available(self)` -- True if TopoSwarm directory exists (even if model not loaded).
- `TopoSwarmBridge.model_loaded` (method) `modules/toposwarm_bridge.py:449` `def model_loaded(self)`
- `TopoSwarmBridge.feedback` (method) `modules/toposwarm_bridge.py:562` `def feedback(self, result_id, good, comment)` -- Optional user feedback on a routing decision.
- `TopoSwarmBridge.route` (method) `modules/toposwarm_bridge.py:586` `def route(self, prompt)` -- Route an operator prompt to a LazyOwn tool call.
- `TopoSwarmBridge.execute_via_orchestrator` (method) `modules/toposwarm_bridge.py:613` `def execute_via_orchestrator(self, prompt, no_model)` -- Execute a prompt through the full TopoSwarm orchestrator (subprocess).
- `TopoSwarmBridge.get_bridge` (method) `modules/toposwarm_bridge.py:645` `def get_bridge()` -- Return the module-level TopoSwarmBridge singleton (lazy init).

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

## modules/traffic_recorder.py
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `RecorderConfig.url_template` (method) `modules/traffic_recorder.py:54` `def url_template(url)` -- Collapse numeric path segments so similar URLs group together.
- `TrafficRecorder.__init__` (method) `modules/traffic_recorder.py:80` `def __init__(self, base_dir)` -- Create storage directories and initialize the index.
- `TrafficRecorder.record` (method) `modules/traffic_recorder.py:96` `def record(self, method, url, status, req_body, resp_body, content_type)` -- Persist one exchange and return its descriptor.
- `TrafficRecorder.query` (method) `modules/traffic_recorder.py:129` `def query(self, host, status, limit, offset)` -- Page exchanges with optional host and status filters.
- `TrafficRecorder.get_body` (method) `modules/traffic_recorder.py:148` `def get_body(self, exchange_id)` -- Load the stored body document for one exchange.
- `TrafficRecorder.count` (method) `modules/traffic_recorder.py:158` `def count(self)` -- Return the total number of recorded exchanges.

## modules/ttp_coverage.py
Depends on: `core/logging.py`
Imported by: `cli/commands/caldera.py`
- `TTPCoverage.__init__` (method) `modules/ttp_coverage.py:68` `def __init__(self)`
- `TTPCoverage.rebuild_from_operations` (method) `modules/ttp_coverage.py:76` `def rebuild_from_operations(self)` -- Re-walk every operation on disk and refresh the matrix.
- `TTPCoverage.add` (method) `modules/ttp_coverage.py:125` `def add(self, technique_id, name, tactic, status, operation_id)`
- `TTPCoverage.compute_ready` (method) `modules/ttp_coverage.py:149` `def compute_ready(self, available_facts)` -- Return the techniques that could run given available facts.
- `TTPCoverage.matrix` (method) `modules/ttp_coverage.py:190` `def matrix(self)` -- Render a coloured-by-tactic table of all techniques.
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
- `LazyownBridgeBackend.route` (method) `modules/unified_bridge.py:127` `def route(self, prompt, context)`
- `TopoSwarmBackend.available` (method) `modules/unified_bridge.py:157` `def available(self)`
- `TopoSwarmBackend.route` (method) `modules/unified_bridge.py:166` `def route(self, prompt, context)`
- `UnifiedBridge.__init__` (method) `modules/unified_bridge.py:207` `def __init__(self)`
- `UnifiedBridge.get` (method) `modules/unified_bridge.py:218` `def get(cls)`
- `UnifiedBridge.set_publish_callback` (method) `modules/unified_bridge.py:223` `def set_publish_callback(self, cb)`
- `UnifiedBridge.route` (method) `modules/unified_bridge.py:246` `def route(self, prompt, context)` -- Route a natural-language prompt to the best LazyOwn tool.
- `UnifiedBridge.delegate` (method) `modules/unified_bridge.py:293` `def delegate(self, goal, backend, timeout)` -- Delegate a complex task to an internal AI agent.
- `UnifiedBridge.list_backends` (method) `modules/unified_bridge.py:352` `def list_backends(self)`
- `UnifiedBridge.route_prompt` (method) `modules/unified_bridge.py:374` `def route_prompt(prompt, context)` -- Convenience: route a prompt without instantiating UnifiedBridge.
- `UnifiedBridge.delegate_task` (method) `modules/unified_bridge.py:379` `def delegate_task(goal, backend)` -- Convenience: delegate a task to an AI agent.

## modules/unified_dashboard.py
Depends on: `cli/graph_advisor.py`, `core/logging.py`, `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/live_surface.py`, `modules/world_model.py`, `skills/hive_mind.py`, `skills/lazyown_policy.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_unified_dashboard.py`
- `UnifiedDashboard.__init__` (method) `modules/unified_dashboard.py:44` `def __init__(self, sessions_dir)`
- `UnifiedDashboard.build_unified_snapshot` (method) `modules/unified_dashboard.py:76` `def build_unified_snapshot(self)` -- Build a complete dashboard snapshot from all data sources.
- `UnifiedDashboard.render_unified` (method) `modules/unified_dashboard.py:173` `def render_unified(self)` -- Render the unified dashboard as a text string for CLI/TUI.
- `UnifiedDashboard.export_json` (method) `modules/unified_dashboard.py:254` `def export_json(self)` -- Export the unified snapshot as a JSON string.
- `UnifiedDashboard.get_unified_dashboard` (method) `modules/unified_dashboard.py:259` `def get_unified_dashboard(sessions_dir)` -- Return a module-level :class:`UnifiedDashboard` singleton.

## modules/venator.py
- `getUUID` (function) `modules/venator.py:38` `def getUUID()`
- `io_key` (function) `modules/venator.py:49` `def io_key(keyname)`
- `getSystemInfo` (function) `modules/venator.py:66` `def getSystemInfo(output_file)`
- `getVTResult` (function) `modules/venator.py:83` `def getVTResult(fileHash)`
- `getHash` (function) `modules/venator.py:112` `def getHash(file, ignoreVFlag)`
- `checkSignature` (function) `modules/venator.py:132` `def checkSignature(file, bundle)`
- `datetime_handler` (function) `modules/venator.py:210` `def datetime_handler(x)`
- `parseAgentsDaemons` (function) `modules/venator.py:215` `def parseAgentsDaemons(item, path)`
- `getLaunchAgents` (function) `modules/venator.py:287` `def getLaunchAgents(path, output_file, ignoreVFlag)`
- `getLaunchDaemons` (function) `modules/venator.py:302` `def getLaunchDaemons(path, output_file, ignoreVFlag)`
- `getUsers` (function) `modules/venator.py:317` `def getUsers(output_file)`
- `getSafariExtensions` (function) `modules/venator.py:338` `def getSafariExtensions(path, output_file)`
- `getChromeExtensions` (function) `modules/venator.py:357` `def getChromeExtensions(path, output_file)`
- `getChromeDownloads` (function) `modules/venator.py:388` `def getChromeDownloads(chromeHistoryDbPath, output_file)`
- `getFirefoxExtensions` (function) `modules/venator.py:442` `def getFirefoxExtensions(path, output_file)`
- `getInstallHistory` (function) `modules/venator.py:477` `def getInstallHistory(output_file)`
- `getCronJobs` (function) `modules/venator.py:494` `def getCronJobs(users, output_file)`
- `getEmond` (function) `modules/venator.py:513` `def getEmond(output_file)`
- `getKext` (function) `modules/venator.py:530` `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)`
- `getEnv` (function) `modules/venator.py:577` `def getEnv(output_file)`
- `getPeriodicScripts` (function) `modules/venator.py:592` `def getPeriodicScripts(output_file)`
- `getConnections` (function) `modules/venator.py:609` `def getConnections(output_file)`
- `SIPStatus` (function) `modules/venator.py:637` `def SIPStatus(output_file)`
- `GatekeeperStatus` (function) `modules/venator.py:651` `def GatekeeperStatus(output_file)`
- `parseApp` (function) `modules/venator.py:663` `def parseApp(app, ignoreVFlag)`
- `getLoginItems` (function) `modules/venator.py:706` `def getLoginItems(path, output_file, ignoreVFlag)`
- `getApps` (function) `modules/venator.py:741` `def getApps(path, output_file, ignoreVFlag)`
- `getEventTaps` (function) `modules/venator.py:763` `def getEventTaps(output_file)`
- `getBashHistory` (function) `modules/venator.py:786` `def getBashHistory(output_file, users)`
- `getShellStartupScripts` (function) `modules/venator.py:804` `def getShellStartupScripts(users, output_file)`
- `hmac_sha256` (function) `modules/venator.py:842` `def hmac_sha256(key, data)`
- `amzn_sig` (function) `modules/venator.py:846` `def amzn_sig(secret_access_key, data, aws_region, aws_service)`
- `amzn_canonical_req` (function) `modules/venator.py:856` `def amzn_canonical_req(filename_path, headers_list)`
- `s3_upload` (function) `modules/venator.py:866` `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)`

## modules/vuln_agent.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/agent_tool.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- `configure_logging` (function) `modules/vuln_agent.py:36` `def configure_logging(debug)`
- `LazyOwnShellWrapper.__init__` (method) `modules/vuln_agent.py:44` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/vuln_agent.py:87` `def execute_command(self, command)` -- Ejecuta un comando en la CLI y retorna el output
- `LazyOwnShellWrapper.get_available_commands` (method) `modules/vuln_agent.py:113` `def get_available_commands(self)` -- Retorna lista de comandos disponibles
- `VulnBotCLI.__init__` (method) `modules/vuln_agent.py:126` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.run_cli_command` (method) `modules/vuln_agent.py:193` `def run_cli_command(command)` -- Ejecuta un comando directamente en la CLI de pentesting
- `VulnBotCLI.read_file` (method) `modules/vuln_agent.py:213` `def read_file(path)`
- `VulnBotCLI.read_file_content` (method) `modules/vuln_agent.py:219` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vuln_agent.py:229` `def load_knowledge_base(self)`
- `VulnBotCLI.save_knowledge_base` (method) `modules/vuln_agent.py:235` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vuln_agent.py:239` `def get_relevant_knowledge(self, prompt)`
- `VulnBotCLI.add_to_knowledge_base` (method) `modules/vuln_agent.py:244` `def add_to_knowledge_base(self, prompt, response)`
- `VulnBotCLI.process_with_context` (method) `modules/vuln_agent.py:250` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.generate` (method) `modules/vuln_agent.py:286` `def generate()`
- `VulnBotCLI.parse_args` (method) `modules/vuln_agent.py:292` `def parse_args()`
- `VulnBotCLI.interactive_mode` (method) `modules/vuln_agent.py:304` `def interactive_mode(bot)`
- `VulnBotCLI.main` (method) `modules/vuln_agent.py:325` `def main()`

## modules/vuln_bot_cli.py
Depends on: `modules/vulnbot.py`
- `parse_args` (function) `modules/vuln_bot_cli.py:10` `def parse_args()`
- `main` (function) `modules/vuln_bot_cli.py:22` `def main()`

## modules/vulnbot.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/vuln_bot_cli.py`
- `VulnBotCLI.__init__` (method) `modules/vulnbot.py:30` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.list_files` (method) `modules/vulnbot.py:86` `def list_files(directory)` -- Lista archivos en un directorio
- `VulnBotCLI.read_file` (method) `modules/vulnbot.py:90` `def read_file(path)` -- Lee contenido de un archivo
- `VulnBotCLI.edit_file` (method) `modules/vulnbot.py:95` `def edit_file(path, content, old_text)` -- Crea o edita un archivo
- `VulnBotCLI.generate` (method) `modules/vulnbot.py:139` `def generate()`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vulnbot.py:145` `def load_knowledge_base(self)`
- `VulnBotCLI.save_knowledge_base` (method) `modules/vulnbot.py:151` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vulnbot.py:155` `def get_relevant_knowledge(self, prompt)`
- `VulnBotCLI.create_complex_prompt` (method) `modules/vulnbot.py:160` `def create_complex_prompt(self, base_prompt, history, knowledge)`
- `VulnBotCLI.read_file_content` (method) `modules/vulnbot.py:176` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_event_config` (method) `modules/vulnbot.py:182` `def load_event_config(self)`
- `VulnBotCLI.process_with_context` (method) `modules/vulnbot.py:190` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.stream_response` (method) `modules/vulnbot.py:206` `def stream_response(self, prompt)`
- `VulnBotCLI.generate` (method) `modules/vulnbot.py:207` `def generate()`
- `VulnBotCLI.add_to_knowledge_base` (method) `modules/vulnbot.py:212` `def add_to_knowledge_base(self, prompt, response)`

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
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/pwn.py`, `cli/ops_commands.py`, `lazyc2.py`, `modules/exploit_recommender.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/live_surface.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/state_manager.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/integration_autonomous_flow.py`, `tests/test_autonomous_ops.py`, `tests/test_core_modules.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_moe_rl_swan.py`, `tests/test_ops_loot_phase.py`, `tests/test_phase1_data_gaps.py`, `tests/test_world_model_extended.py`
- `read_state_dict` (function) `modules/world_model.py:72` `def read_state_dict(path)` -- Read a world-model state dict, transparently decrypting at rest.
- `write_state_dict` (function) `modules/world_model.py:118` `def write_state_dict(path, data)` -- Atomically write a world-model state dict as plaintext.
- `HostState.rank` (method) `modules/world_model.py:160` `def rank(self)`
- `HostState.can_advance_to` (method) `modules/world_model.py:163` `def can_advance_to(self, next_state)`
- `NetworkGraph.__init__` (method) `modules/world_model.py:267` `def __init__(self)`
- `NetworkGraph.add_relation` (method) `modules/world_model.py:274` `def add_relation(self, relation)` -- Add a directed edge.
- `NetworkGraph.neighbors` (method) `modules/world_model.py:282` `def neighbors(self, node)` -- Return nodes reachable from *node* in one outbound hop.
- `NetworkGraph.in_degree` (method) `modules/world_model.py:286` `def in_degree(self, node)` -- Count edges pointing INTO *node*.
- `NetworkGraph.out_degree` (method) `modules/world_model.py:290` `def out_degree(self, node)` -- Count edges leaving *node*.
- `NetworkGraph.degree_centrality` (method) `modules/world_model.py:294` `def degree_centrality(self)` -- Return (node, centrality_score) pairs sorted descending by score.
- `NetworkGraph.pivot_candidates` (method) `modules/world_model.py:309` `def pivot_candidates(self, top_k)` -- Return the *top_k* highest-centrality nodes as pivot candidates.
- `NetworkGraph.to_dict` (method) `modules/world_model.py:331` `def to_dict(self)`
- `NetworkGraph.from_dict` (method) `modules/world_model.py:348` `def from_dict(cls, data)`
- `HostEntry.add_service` (method) `modules/world_model.py:373` `def add_service(self, svc)`
- `HostEntry.advance` (method) `modules/world_model.py:377` `def advance(self, new_state)` -- Advance state only if new_state is the next valid step.
- `HostEntry.to_dict` (method) `modules/world_model.py:385` `def to_dict(self)`
- `HostEntry.from_dict` (method) `modules/world_model.py:397` `def from_dict(cls, d)`
- `_PhaseDeriver.derive` (method) `modules/world_model.py:430` `def derive(self, hosts)`
- `WorldModel.__init__` (method) `modules/world_model.py:549` `def __init__(self, path)`
- `WorldModel.add_host` (method) `modules/world_model.py:565` `def add_host(self, ip)`
- `WorldModel.reset_host` (method) `modules/world_model.py:573` `def reset_host(self, ip)` -- Clear a single host's state back to UNSCANNED for a fresh scan.
- `WorldModel.advance_host` (method) `modules/world_model.py:583` `def advance_host(self, ip, new_state)`
- `WorldModel.add_service` (method) `modules/world_model.py:592` `def add_service(self, ip, port, name, version, protocol)`
- `WorldModel.add_note` (method) `modules/world_model.py:609` `def add_note(self, ip, note)`
- `WorldModel.set_os_hint` (method) `modules/world_model.py:616` `def set_os_hint(self, ip, os_hint)` -- Set the operating system hint for a host.
- `WorldModel.get_host` (method) `modules/world_model.py:630` `def get_host(self, ip)` -- Return a host entry by IP, or None if not found.
- `WorldModel.get_hosts_summary` (method) `modules/world_model.py:642` `def get_hosts_summary(self)` -- Return a mapping of IP -> state for all tracked hosts.
- `WorldModel.add_credential` (method) `modules/world_model.py:653` `def add_credential(self, value, host, service)`
- `WorldModel.link_credential_to_success` (method) `modules/world_model.py:685` `def link_credential_to_success(self, value, host)` -- Mark a credential as working for a specific host in the graph.
- `WorldModel.link_credential_to_failure` (method) `modules/world_model.py:706` `def link_credential_to_failure(self, value, host)` -- Mark a credential as rejected by a specific host in the graph.
- `WorldModel.add_vulnerability` (method) `modules/world_model.py:736` `def add_vulnerability(self, description, host, cve, severity)`
- `WorldModel.add_email` (method) `modules/world_model.py:742` `def add_email(self, address, host, context)`
- `WorldModel.add_domain` (method) `modules/world_model.py:748` `def add_domain(self, domain, host, context)`
- `WorldModel.update_from_findings` (method) `modules/world_model.py:762` `def update_from_findings(self, findings)` -- Integrate a list of Finding objects (from obs_parser.ObsParser).
- `WorldModel.consume_policy_facts` (method) `modules/world_model.py:835` `def consume_policy_facts(self, facts_path)` -- Ingest structured facts from FactStore's ``policy_facts.json``.
- `WorldModel.add_relation` (method) `modules/world_model.py:927` `def add_relation(self, source, target, relation, weight)` -- Add an arbitrary directed relationship to the network graph.
- `WorldModel.pivot_candidates` (method) `modules/world_model.py:948` `def pivot_candidates(self, top_k)` -- Return the top_k highest-centrality nodes as pivot candidates.
- `WorldModel.graph_snapshot` (method) `modules/world_model.py:956` `def graph_snapshot(self)` -- Return the full network graph as a serialisable dict.
- `WorldModel.get_phase` (method) `modules/world_model.py:963` `def get_phase(self)`
- `WorldModel.get_suggested_tools` (method) `modules/world_model.py:967` `def get_suggested_tools(self)`
- `WorldModel.to_context_string` (method) `modules/world_model.py:970` `def to_context_string(self)` -- Compact, LLM-readable summary of the current engagement state.
- `WorldModel.reload` (method) `modules/world_model.py:1078` `def reload(self)` -- Discard in-memory state and re-read from the persisted file.
- `WorldModel.reset` (method) `modules/world_model.py:1094` `def reset(self)` -- Clear all state and delete the persisted file.
- `WorldModel.snapshot` (method) `modules/world_model.py:1105` `def snapshot(self)` -- Return a plain-dict snapshot (for JSON serialisation).
- `WorldModel.get_world_model` (method) `modules/world_model.py:1126` `def get_world_model(path)` -- Return (or create) the module-level singleton WorldModel.

## modules/yaml_generator.py
Depends on: `modules/ai_model.py`, `modules/llm_factory.py`
- `YAMLPromptGenerator.__init__` (method) `modules/yaml_generator.py:18` `def __init__(self, provider, api_key)`
- `YAMLPromptGenerator.load_payload` (method) `modules/yaml_generator.py:25` `def load_payload(self)` -- Carga las variables desde payload.json
- `YAMLPromptGenerator.generate_prompt` (method) `modules/yaml_generator.py:54` `def generate_prompt(self, user_request)` -- Genera el prompt para la IA en inglés
- `YAMLPromptGenerator.extract_yaml_from_markdown` (method) `modules/yaml_generator.py:100` `def extract_yaml_from_markdown(self, text)` -- Extrae el primer bloque YAML entre ```yaml y ```
- `YAMLPromptGenerator.create_yaml_addon` (method) `modules/yaml_generator.py:109` `def create_yaml_addon(self, user_request, output_dir)` -- Genera el YAML y lo guarda en disco
- `YAMLPromptGenerator.main` (method) `modules/yaml_generator.py:141` `def main()`


Next: [API_p16.md](API_p16.md)
