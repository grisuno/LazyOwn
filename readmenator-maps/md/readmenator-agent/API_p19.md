# API (page 19 of 25)
Previous: [API_p18.md](API_p18.md)

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
Imported by: `cli/commands/lazyops.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `skills/autonomous_daemon.py`, `tests/test_engage_gates.py`, `tests/test_lazy_bridge_traffic.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_proxy.py`, `tests/test_safety_gates.py`
- `url_template` (function) `modules/traffic_recorder.py:69` `def url_template(url)` -- Collapse numeric path segments so similar URLs group together.
- `TrafficRecorder.__init__` (method) `modules/traffic_recorder.py:94` `def __init__(self, base_dir)` -- Create storage directories and initialize the index.
- `TrafficRecorder.record` (method) `modules/traffic_recorder.py:138` `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...` -- Persist one exchange and return its descriptor.
- `TrafficRecorder.since` (method) `modules/traffic_recorder.py:230` `def since(self, rowid, limit)` -- Page exchanges newer than a rowid watermark for loop ingestion.
- `TrafficRecorder.latest_rowid` (method) `modules/traffic_recorder.py:247` `def latest_rowid(self)` -- Return the current max rowid (0 when the index is empty).
- `TrafficRecorder.query` (method) `modules/traffic_recorder.py:253` `def query(self, host, status, limit, offset, task)` -- Page exchanges with optional host, status and task filters.
- `TrafficRecorder.get_body` (method) `modules/traffic_recorder.py:275` `def get_body(self, exchange_id)` -- Load the stored body document for one exchange.
- `TrafficRecorder.read_body` (method) `modules/traffic_recorder.py:284` `def read_body(self, exchange_id, part, offset, length)` -- Read one body in ranges like a blob store.
- `TrafficRecorder.count` (method) `modules/traffic_recorder.py:317` `def count(self)` -- Return the total number of recorded exchanges.
- `TrafficRecorder.backfill_fts` (method) `modules/traffic_recorder.py:343` `def backfill_fts(self, batch)` -- Index stored bodies missing from the FTS table.
- `TrafficRecorder.search_body` (method) `modules/traffic_recorder.py:382` `def search_body(self, query, limit)` -- Full-text search request/response bodies.
- `TrafficRecorder.export_archive` (method) `modules/traffic_recorder.py:451` `def export_archive(self, path, limit, task)` -- Export the index plus bodies into a portable zip archive.
- `TrafficRecorder.import_archive` (method) `modules/traffic_recorder.py:493` `def import_archive(self, path)` -- Merge an archive exported by :meth:`export_archive`.
- `TrafficRecorder.import_inbox` (method) `modules/traffic_recorder.py:554` `def import_inbox(self, inbox_dir)` -- Import every zip dropped in the inbox, moving handled files away.
- `TrafficRecorder.gc` (method) `modules/traffic_recorder.py:587` `def gc(self, older_than_sec)` -- Delete exchanges older than a cut-off with their bodies and index rows.

## modules/trigger_policy.py
Depends on: `core/logging.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`
Imported by: `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_triggers.py`
- `validate_triggers` (function) `modules/trigger_policy.py:40` `def validate_triggers(raw)` -- Validate the raw ``triggers`` section of the orchestrator YAML.
- `seeds` (function) `modules/trigger_policy.py:87` `def seeds(raw)` -- Coerce validated trigger rows into seed dicts for the store.
- `read_policy` (function) `modules/trigger_policy.py:120` `def read_policy(path)` -- Read the shipped orchestrator YAML triggers section.
- `seed_store` (function) `modules/trigger_policy.py:146` `def seed_store(policy, store, task_id)` -- Merge declarative seeds into a persistent TriggerStore.
- `export_store` (function) `modules/trigger_policy.py:171` `def export_store(task_id)` -- Return the current store rows for TUI and API surfaces.
- `remove_seed` (function) `modules/trigger_policy.py:185` `def remove_seed(kind, arg, task_id)` -- Drop the first runtime trigger matching a declarative signature.

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
- `get_coverage` (function) `modules/ttp_coverage.py:260` `def get_coverage()` -- Return a fresh :class:`TTPCoverage`.

## modules/ttpscope_bridge.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/atomic_resolver.py`, `skills/lazyown_parquet_db.py`
Imported by: `skills/lazyown_mcp.py`
- `locate_binary` (function) `modules/ttpscope_bridge.py:82` `def locate_binary()` -- Return the ttpscope binary path, preferring the vendored build.
- `validate_object_id` (function) `modules/ttpscope_bridge.py:92` `def validate_object_id(raw)` -- Validate an ATT&CK object ID (T1059.001, G0016, S0002, ...).
- `validate_query` (function) `modules/ttpscope_bridge.py:100` `def validate_query(raw)` -- Validate a free-text search query.
- `validate_platform` (function) `modules/ttpscope_bridge.py:112` `def validate_platform(raw)` -- Validate a matrix platform filter (empty means all).
- `do_sync` (function) `modules/ttpscope_bridge.py:497` `def do_sync()` -- Download the Enterprise ATT&CK bundle via ttpscope sync.
- `do_search` (function) `modules/ttpscope_bridge.py:508` `def do_search(query)` -- Search IDs, names, aliases and descriptions.
- `do_show` (function) `modules/ttpscope_bridge.py:520` `def do_show(object_id)` -- Show one ATT&CK object and its relationships.
- `do_matrix` (function) `modules/ttpscope_bridge.py:535` `def do_matrix(platform)` -- Render the Enterprise matrix, optionally filtered by platform.
- `do_note` (function) `modules/ttpscope_bridge.py:551` `def do_note(object_id, text)` -- Append a timestamped research note.
- `do_notes` (function) `modules/ttpscope_bridge.py:570` `def do_notes(object_id)` -- Read research notes for an object.
- `do_chain` (function) `modules/ttpscope_bridge.py:582` `def do_chain(object_id, platform, limit)` -- Join ttpscope context with Atomic tests and parquet techniques.
- `run_action` (function) `modules/ttpscope_bridge.py:652` `def run_action(action)` -- Dispatch a validated action (used by CLI addons and MCP).
- `main` (function) `modules/ttpscope_bridge.py:679` `def main()` -- CLI entry point for the lazyaddon execute_command.

## modules/unified_bridge.py
Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/lazyown_bridge.py`, `modules/mcp_agent_bridge.py`, `modules/state_manager.py`, `modules/toposwarm_bridge.py`
Imported by: `lazyown.py`
- `RouteBackend.available` (method) `modules/unified_bridge.py:69` `def available(self)`
- `RouteBackend.route` (method) `modules/unified_bridge.py:72` `def route(self, prompt, context)`
- `KeywordBackend.available` (method) `modules/unified_bridge.py:102` `def available(self)`
- `KeywordBackend.route` (method) `modules/unified_bridge.py:105` `def route(self, prompt, context)`
- `LazyownBridgeBackend.available` (method) `modules/unified_bridge.py:126` `def available(self)`
- `LazyownBridgeBackend.route` (method) `modules/unified_bridge.py:134` `def route(self, prompt, context)`
- `TopoSwarmBackend.available` (method) `modules/unified_bridge.py:164` `def available(self)`
- `TopoSwarmBackend.route` (method) `modules/unified_bridge.py:173` `def route(self, prompt, context)`
- `UnifiedBridge.__init__` (method) `modules/unified_bridge.py:214` `def __init__(self)`
- `UnifiedBridge.get` (method) `modules/unified_bridge.py:225` `def get(cls)`
- `UnifiedBridge.set_publish_callback` (method) `modules/unified_bridge.py:230` `def set_publish_callback(self, cb)`
- `UnifiedBridge.route` (method) `modules/unified_bridge.py:253` `def route(self, prompt, context)` -- Route a natural-language prompt to the best LazyOwn tool.
- `UnifiedBridge.delegate` (method) `modules/unified_bridge.py:300` `def delegate(self, goal, backend, timeout, max_iterations)` -- Delegate a complex task to an internal AI agent.
- `UnifiedBridge.list_backends` (method) `modules/unified_bridge.py:461` `def list_backends(self)`
- `route_prompt` (function) `modules/unified_bridge.py:483` `def route_prompt(prompt, context)` -- Convenience: route a prompt without instantiating UnifiedBridge.
- `delegate_task` (function) `modules/unified_bridge.py:488` `def delegate_task(goal, backend)` -- Convenience: delegate a task to an AI agent.

## modules/unified_dashboard.py
Depends on: `cli/graph_advisor.py`, `core/logging.py`, `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/live_surface.py`, `modules/world_model.py`, `skills/hive_mind.py`, `skills/lazyown_policy.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_unified_dashboard.py`
- `UnifiedDashboard.__init__` (method) `modules/unified_dashboard.py:44` `def __init__(self, sessions_dir)`
- `UnifiedDashboard.build_unified_snapshot` (method) `modules/unified_dashboard.py:76` `def build_unified_snapshot(self)` -- Build a complete dashboard snapshot from all data sources.
- `UnifiedDashboard.render_unified` (method) `modules/unified_dashboard.py:170` `def render_unified(self)` -- Render the unified dashboard as a text string for CLI/TUI.
- `UnifiedDashboard.export_json` (method) `modules/unified_dashboard.py:251` `def export_json(self)` -- Export the unified snapshot as a JSON string.
- `get_unified_dashboard` (function) `modules/unified_dashboard.py:256` `def get_unified_dashboard(sessions_dir)` -- Return a module-level :class:`UnifiedDashboard` singleton.

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

## modules/verb_catalog.py
Depends on: `core/logging.py`, `modules/auto_registry.py`, `modules/lazy_cli_bridge.py`
Imported by: `cli/commands/verb_admin.py`, `cli/lazy_orchestrator.py`, `cli/session_brief.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_cli_bridge.py`, `modules/orchestrator_config.py`, `tests/test_loop_cli_catalog.py`, `tests/test_orchestrator_api.py`, `tests/test_session_brief.py`
- `index_commands` (function) `modules/verb_catalog.py:190` `def index_commands(config)` -- Return discovered shell commands as ``{name: {summary, phase}}``.
- `validate_catalog` (function) `modules/verb_catalog.py:230` `def validate_catalog(data)` -- Validate one raw catalog document.
- `load` (function) `modules/verb_catalog.py:263` `def load(config)` -- Return the raw catalog mapping ``{name: entry}``.
- `entries` (function) `modules/verb_catalog.py:296` `def entries(config)` -- Return the catalog with defaults filled in, cached briefly.
- `catalog_enabled` (function) `modules/verb_catalog.py:349` `def catalog_enabled(name, config)` -- Return the catalog state of one verb.
- `catalog_source` (function) `modules/verb_catalog.py:364` `def catalog_source(name, config)` -- Return the catalog source of one verb, ``None`` when unknown.
- `set_enabled` (function) `modules/verb_catalog.py:378` `def set_enabled(name, enabled, config)` -- Flip one verb in the YAML catalog atomically.
- `sync` (function) `modules/verb_catalog.py:415` `def sync(config)` -- Materialise the discovered shell catalogue into the YAML file.
- `stats` (function) `modules/verb_catalog.py:502` `def stats(config)` -- Summarise the catalog for the brief and the HTTP API.
- `search` (function) `modules/verb_catalog.py:516` `def search(query, config, phase, enabled, limit)` -- Search catalog entries by substring, phase and state.

## modules/verb_manifest.py
Depends on: `core/logging.py`, `modules/chain_registry.py`, `modules/world_model.py`
Imported by: `modules/chain_distill.py`, `modules/chain_runner.py`, `tests/test_verb_manifest.py`
- `FactPredicate.args` (method) `modules/verb_manifest.py:152` `def args(self)` -- Return the set corner arguments.
- `FactPredicate.is_wild` (method) `modules/verb_manifest.py:156` `def is_wild(self, key)` -- Return True when that argument is a ``{token}`` wildcard.
- `FactPredicate.matches` (method) `modules/verb_manifest.py:161` `def matches(self, other)` -- Return True when this fact instance satisfies the other.
- `parse_predicate` (function) `modules/verb_manifest.py:222` `def parse_predicate(data)` -- Parse one predicate mapping into a FactPredicate.
- `parse_manifest` (function) `modules/verb_manifest.py:296` `def parse_manifest(verb, data)` -- Validate and parse one manifest document entry.
- `manifests` (function) `modules/verb_manifest.py:371` `def manifests(path)` -- Return parsed manifests with a small TTL cache.
- `manifest_for` (function) `modules/verb_manifest.py:396` `def manifest_for(verb, path)` -- Return the manifest of one verb, or None when untyped.
- `facts_for_target` (function) `modules/verb_manifest.py:411` `def facts_for_target(host)` -- Project the world model facts of one host into predicates.
- `plan_check` (function) `modules/verb_manifest.py:467` `def plan_check(steps, tokens, path, facts)` -- Check a chain semantically: every typed precondition must be supplied.
- `coverage` (function) `modules/verb_manifest.py:522` `def coverage(total_verbs, path)` -- Summarise manifest coverage for registry reporting.

## modules/vuln_bot_cli.py
Depends on: `modules/vulnbot.py`
- `parse_args` (function) `modules/vuln_bot_cli.py:10` `def parse_args()`
- `main` (function) `modules/vuln_bot_cli.py:22` `def main()`

## modules/vulnbot.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/logging_config.py`
Imported by: `modules/vuln_bot_cli.py`, `tests/test_vulnbot_fallback.py`
- `VulnBotCLI.__init__` (method) `modules/vulnbot.py:38` `def __init__(self, provider, mode, debug, script_path)`
- `list_files` (function) `modules/vulnbot.py:149` `def list_files(directory)` -- Lista archivos en un directorio
- `read_file` (function) `modules/vulnbot.py:153` `def read_file(path)` -- Lee contenido de un archivo
- `edit_file` (function) `modules/vulnbot.py:158` `def edit_file(path, content, old_text)` -- Crea o edita un archivo
- `generate` (function) `modules/vulnbot.py:202` `def generate()`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vulnbot.py:208` `def load_knowledge_base(self)` -- Load the knowledge base in any known shape.
- `VulnBotCLI.save_knowledge_base` (method) `modules/vulnbot.py:224` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vulnbot.py:228` `def get_relevant_knowledge(self, prompt)` -- Return knowledge responses whose text shares keywords with the prompt.
- `VulnBotCLI.create_complex_prompt` (method) `modules/vulnbot.py:251` `def create_complex_prompt(self, base_prompt, history, knowledge)`
- `VulnBotCLI.read_file_content` (method) `modules/vulnbot.py:267` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_event_config` (method) `modules/vulnbot.py:273` `def load_event_config(self)`
- `VulnBotCLI.process_with_context` (method) `modules/vulnbot.py:281` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.stream_response` (method) `modules/vulnbot.py:297` `def stream_response(self, prompt)`
- `generate` (function) `modules/vulnbot.py:298` `def generate()`
- `VulnBotCLI.add_to_knowledge_base` (method) `modules/vulnbot.py:303` `def add_to_knowledge_base(self, prompt, response)` -- Append a prompt/response record in the canonical list format.

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
- `SID.GetUsernameFromPid` (method) `modules/win_rootkit/win_rin3_rootkit.cs:145`
- `SID.ShouldHidePid` (method) `modules/win_rootkit/win_rin3_rootkit.cs:203`
- `SID.HookFindFirstFile` (method) `modules/win_rootkit/win_rin3_rootkit.cs:214`
- `SID.HookCreateFile` (method) `modules/win_rootkit/win_rin3_rootkit.cs:226`

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

## modules/winbox_gym.py
Depends on: `core/hardening.py`, `core/logging.py`, `core/safe_exec.py`, `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`, `utils.py`
- `load_index` (function) `modules/winbox_gym.py:222` `def load_index(path)` -- Load the gym index, returning an empty mapping on failure.
- `vulnerabilities` (function) `modules/winbox_gym.py:227` `def vulnerabilities(path)` -- Return every indexed lab vector.
- `get` (function) `modules/winbox_gym.py:233` `def get(vuln_id, path)` -- Return one lab vector by id, or None.
- `chain_for` (function) `modules/winbox_gym.py:242` `def chain_for(vuln_id, path)` -- Return the resolved chain for one lab vector, or None.
- `exploit_for` (function) `modules/winbox_gym.py:252` `def exploit_for(vuln_id, path)` -- Return the exploit spec for one lab vector, or None.
- `validate_matrix` (function) `modules/winbox_gym.py:262` `def validate_matrix(path)` -- Validate the index, exploit files and chains as one matrix.
- `summary` (function) `modules/winbox_gym.py:311` `def summary(path)` -- Return counts by severity and service for operators.
- `binary_path` (function) `modules/winbox_gym.py:335` `def binary_path()` -- Resolve the winbox executable or None.
- `ensure_installed` (function) `modules/winbox_gym.py:340` `def ensure_installed(params, timeout)` -- Clone and pip-install the upstream WinBox repo when the binary is missing.
- `check_readiness` (function) `modules/winbox_gym.py:412` `def check_readiness(params)` -- Report WinBox lab readiness without installing anything.
- `ensure_prereqs` (function) `modules/winbox_gym.py:453` `def ensure_prereqs(timeout)` -- Install missing lab host prerequisites through apt-get.
- `ensure_lab_ready` (function) `modules/winbox_gym.py:822` `def ensure_lab_ready(params)` -- Bring the WinBox lab to attackable state in one idempotent call.
- `run_cli` (function) `modules/winbox_gym.py:924` `def run_cli(args, timeout)` -- Run one allowlisted winbox CLI action without a shell.
- `vm_status` (function) `modules/winbox_gym.py:1113` `def vm_status(timeout)` -- Query the WinBox VM state and address.
- `vm_ip` (function) `modules/winbox_gym.py:1148` `def vm_ip()` -- Return the lab VM IPv4 address, or an empty string.
- `resolve_target` (function) `modules/winbox_gym.py:1170` `def resolve_target()` -- Return the lab VM IP and mirror it into ``payload.json`` rhost.
- `ensure_vm_running` (function) `modules/winbox_gym.py:1184` `def ensure_vm_running(timeout)` -- Start the lab VM when it is not running.
- `record_artifact` (function) `modules/winbox_gym.py:1211` `def record_artifact(name, output)` -- Persist one CLI transcript under ``sessions/winbox``.
- `attack_readiness` (function) `modules/winbox_gym.py:1234` `def attack_readiness(params)` -- Report whether the autonomous loop can attack the lab right now.
- `main` (function) `modules/winbox_gym.py:1262` `def main()` -- CLI: list | validate | summary | readiness.

## modules/workspace.py
Imported by: `tests/test_lazy_loop.py`
- `root` (function) `modules/workspace.py:21` `def root()` -- Return (and create) the workspace root directory.
- `resolve` (function) `modules/workspace.py:27` `def resolve(rel)` -- Resolve a workspace-relative path, refusing escapes.
- `list_entries` (function) `modules/workspace.py:46` `def list_entries(rel)` -- List one directory with names, kinds and sizes.
- `read_text` (function) `modules/workspace.py:63` `def read_text(rel, limit)` -- Read one file, truncated to the byte limit.
- `write_text` (function) `modules/workspace.py:72` `def write_text(rel, content)` -- Write one file, creating parents; returns the character count.
- `make_dir` (function) `modules/workspace.py:83` `def make_dir(rel)` -- Create one directory (parents included).
- `remove` (function) `modules/workspace.py:90` `def remove(rel)` -- Delete a file or directory tree inside the workspace.

## modules/world_model.py
Depends on: `cli/commands/enum.py`, `core/hardening.py`, `core/logging.py`, `modules/cli_auth.py`, `modules/factsio.py`
Imported by: `cli/commands/campaign.py`, `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/netattack.py`, `cli/commands/privilege_escalation.py`, `cli/commands/pwn.py`, `cli/dashboard_tui.py`, `cli/ops_commands.py`, `cli/recommendation_signals.py`, `cli/session_brief.py`, `cli/session_resumer.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/services/backend.py`, `modules/atomic_exploit_bridge.py`, `modules/autonomous_exploit_engine.py`, `modules/beacon_recon.py`, `modules/estorides_importer.py`, `modules/event_consumers.py`, `modules/exploit_recommender.py`, `modules/golden_path.py`, `modules/gym_registry.py`, `modules/integrations/nuclei_parser.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_hostscore.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_osinfer.py`, `modules/lazy_surface_diff.py`, `modules/lazy_world_diff.py`, `modules/live_surface.py`, `modules/loop_triggers.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/professional_report.py`, `modules/redteam_gym.py`, `modules/sinks/world_diff.py`, `modules/sinks/world_model.py`, `modules/state_manager.py`, `modules/surface_ops.py`, `modules/unified_dashboard.py`, `modules/verb_manifest.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_beacon_recon_sink.py`, `tests/test_codeql_alert_fixes.py`, `tests/test_cve_pipeline.py`, `tests/test_estorides_fusion.py`, `tests/test_golden_path.py`, `tests/test_gym_cli.py`, `tests/test_gym_lifecycle.py`, `tests/test_gym_registry.py`, `tests/test_infra_disposable.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazynmap_post.py`, `tests/test_loop_cli_catalog.py`, `tests/test_loop_trigger_hints.py`, `tests/test_ops_loot_phase.py`, `tests/test_orchestrator_api.py`, `tests/test_phase1_data_gaps.py`, `tests/test_session_brief.py`, `tests/test_single_source_of_truth.py`, `tests/test_world_model_extended.py`
- `read_state_dict` (function) `modules/world_model.py:290` `def read_state_dict(path)` -- Read a world-model state dict, transparently decrypting at rest.
- `write_state_dict` (function) `modules/world_model.py:325` `def write_state_dict(path, data)` -- Atomically write a world-model state dict encrypted at rest.
- `HostState.rank` (method) `modules/world_model.py:382` `def rank(self)`
- `HostState.can_advance_to` (method) `modules/world_model.py:385` `def can_advance_to(self, next_state)`
- `NetworkGraph.__init__` (method) `modules/world_model.py:489` `def __init__(self)`
- `NetworkGraph.add_relation` (method) `modules/world_model.py:496` `def add_relation(self, relation)` -- Add a directed edge.
- `NetworkGraph.neighbors` (method) `modules/world_model.py:504` `def neighbors(self, node)` -- Return nodes reachable from *node* in one outbound hop.
- `NetworkGraph.in_degree` (method) `modules/world_model.py:508` `def in_degree(self, node)` -- Count edges pointing INTO *node*.
- `NetworkGraph.out_degree` (method) `modules/world_model.py:512` `def out_degree(self, node)` -- Count edges leaving *node*.
- `NetworkGraph.degree_centrality` (method) `modules/world_model.py:516` `def degree_centrality(self)` -- Return (node, centrality_score) pairs sorted descending by score.
- `NetworkGraph.pivot_candidates` (method) `modules/world_model.py:531` `def pivot_candidates(self, top_k)` -- Return the *top_k* highest-centrality nodes as pivot candidates.
- `NetworkGraph.to_dict` (method) `modules/world_model.py:553` `def to_dict(self)`
- `NetworkGraph.from_dict` (method) `modules/world_model.py:570` `def from_dict(cls, data)`
- `HostEntry.add_service` (method) `modules/world_model.py:595` `def add_service(self, svc)`
- `HostEntry.advance` (method) `modules/world_model.py:599` `def advance(self, new_state)` -- Advance state only if new_state is the next valid step.
- `HostEntry.to_dict` (method) `modules/world_model.py:607` `def to_dict(self)`
- `HostEntry.from_dict` (method) `modules/world_model.py:619` `def from_dict(cls, d)`
- `_PhaseDeriver.derive` (method) `modules/world_model.py:656` `def derive(self, hosts)`
- `WorldModel.__init__` (method) `modules/world_model.py:775` `def __init__(self, path)`
- `WorldModel.add_host` (method) `modules/world_model.py:791` `def add_host(self, ip)`
- `WorldModel.reset_host` (method) `modules/world_model.py:799` `def reset_host(self, ip)` -- Clear a single host's state back to UNSCANNED for a fresh scan.
- `WorldModel.remove_host` (method) `modules/world_model.py:809` `def remove_host(self, ip)` -- Remove one host from the model and persist the change.
- `WorldModel.advance_host` (method) `modules/world_model.py:825` `def advance_host(self, ip, new_state)`
- `WorldModel.add_service` (method) `modules/world_model.py:834` `def add_service(self, ip, port, name, version, protocol)`
- `WorldModel.add_note` (method) `modules/world_model.py:851` `def add_note(self, ip, note)`
- `WorldModel.set_os_hint` (method) `modules/world_model.py:858` `def set_os_hint(self, ip, os_hint)` -- Set the operating system hint for a host.
- `WorldModel.get_host` (method) `modules/world_model.py:872` `def get_host(self, ip)` -- Return a host entry by IP, or None if not found.
- `WorldModel.get_hosts_summary` (method) `modules/world_model.py:884` `def get_hosts_summary(self)` -- Return a mapping of IP -> state for all tracked hosts.
- `WorldModel.add_credential` (method) `modules/world_model.py:895` `def add_credential(self, value, host, service)`
- `WorldModel.link_credential_to_success` (method) `modules/world_model.py:927` `def link_credential_to_success(self, value, host)` -- Mark a credential as working for a specific host in the graph.
- `WorldModel.link_credential_to_failure` (method) `modules/world_model.py:948` `def link_credential_to_failure(self, value, host)` -- Mark a credential as rejected by a specific host in the graph.
- `WorldModel.add_vulnerability` (method) `modules/world_model.py:978` `def add_vulnerability(self, description, host, cve, severity)`
- `WorldModel.add_email` (method) `modules/world_model.py:984` `def add_email(self, address, host, context)`
- `WorldModel.add_domain` (method) `modules/world_model.py:990` `def add_domain(self, domain, host, context)`
- `WorldModel.update_from_findings` (method) `modules/world_model.py:1004` `def update_from_findings(self, findings)` -- Integrate a list of Finding objects (from obs_parser.ObsParser).
- `WorldModel.consume_policy_facts` (method) `modules/world_model.py:1077` `def consume_policy_facts(self, facts_path)` -- Ingest structured facts from FactStore's ``policy_facts.json``.
- `WorldModel.add_relation` (method) `modules/world_model.py:1216` `def add_relation(self, source, target, relation, weight)` -- Add an arbitrary directed relationship to the network graph.
- `WorldModel.pivot_candidates` (method) `modules/world_model.py:1237` `def pivot_candidates(self, top_k)` -- Return the top_k highest-centrality nodes as pivot candidates.
- `WorldModel.graph_snapshot` (method) `modules/world_model.py:1245` `def graph_snapshot(self)` -- Return the full network graph as a serialisable dict.
- `WorldModel.get_phase` (method) `modules/world_model.py:1252` `def get_phase(self)`
- `WorldModel.get_suggested_tools` (method) `modules/world_model.py:1256` `def get_suggested_tools(self)`
- `WorldModel.to_context_string` (method) `modules/world_model.py:1259` `def to_context_string(self)` -- Compact, LLM-readable summary of the current engagement state.
- `WorldModel.reload` (method) `modules/world_model.py:1367` `def reload(self)` -- Discard in-memory state and re-read from the persisted file.
- `WorldModel.reset` (method) `modules/world_model.py:1383` `def reset(self)` -- Clear all state and delete the persisted file.
- `WorldModel.snapshot` (method) `modules/world_model.py:1394` `def snapshot(self)` -- Return a plain-dict snapshot (for JSON serialisation).
- `WorldModel.read_section` (method) `modules/world_model.py:1410` `def read_section(self, key)` -- Return one allowlisted passthrough section.
- `WorldModel.write_section` (method) `modules/world_model.py:1427` `def write_section(self, key, value)` -- Persist one allowlisted passthrough section atomically.
- `get_world_model` (function) `modules/world_model.py:1455` `def get_world_model(path)` -- Return (or create) the module-level singleton WorldModel.

## modules/yaml_generator.py
Depends on: `modules/ai_model.py`, `modules/llm_factory.py`
- `YAMLPromptGenerator.__init__` (method) `modules/yaml_generator.py:18` `def __init__(self, provider, api_key)`
- `YAMLPromptGenerator.load_payload` (method) `modules/yaml_generator.py:25` `def load_payload(self)` -- Carga las variables desde payload.json
- `YAMLPromptGenerator.generate_prompt` (method) `modules/yaml_generator.py:54` `def generate_prompt(self, user_request)` -- Genera el prompt para la IA en inglés
- `YAMLPromptGenerator.extract_yaml_from_markdown` (method) `modules/yaml_generator.py:100` `def extract_yaml_from_markdown(self, text)` -- Extrae el primer bloque YAML entre ```yaml y ```
- `YAMLPromptGenerator.create_yaml_addon` (method) `modules/yaml_generator.py:109` `def create_yaml_addon(self, user_request, output_dir)` -- Genera el YAML y lo guarda en disco
- `main` (function) `modules/yaml_generator.py:141` `def main()`

## modules/yara_scanner.py
Imported by: `cli/commands/postexp_migrated.py`, `modules/intelligence_engine.py`
- `YaraScanner.__init__` (method) `modules/yara_scanner.py:31` `def __init__(self, rules_dir, auto_compile)`
- `YaraScanner.ensure_directory` (method) `modules/yara_scanner.py:41` `def ensure_directory(self)` -- Create the YARA rules directory if it does not exist.
- `YaraScanner.compile_all` (method) `modules/yara_scanner.py:54` `def compile_all(self)` -- Compile all .yar files in the rules directory.
- `YaraScanner.scan_file` (method) `modules/yara_scanner.py:98` `def scan_file(self, filepath, timeout)` -- Scan a single file with all compiled YARA rules.
- `target` (function) `modules/yara_scanner.py:137` `def target()`
- `YaraScanner.scan_directory` (method) `modules/yara_scanner.py:187` `def scan_directory(self, directory, recursive, extensions, max_files)` -- Scan all files in a directory recursively.
- `YaraScanner.add_rule` (method) `modules/yara_scanner.py:258` `def add_rule(self, name, content)` -- Add a new YARA rule to the rules directory.
- `YaraScanner.list_rules` (method) `modules/yara_scanner.py:277` `def list_rules(self)` -- List all YARA rules in the rules directory.
- `YaraScanner.download_community_rules` (method) `modules/yara_scanner.py:300` `def download_community_rules(self)` -- Attempt to download community YARA rules from popular repositories.
- `YaraScanner.ioc_scan` (method) `modules/yara_scanner.py:328` `def ioc_scan(self, target_path, iocs)` -- Scan for IOCs (hashes, strings, registry keys) in a file/directory.
- `create_default_rules` (function) `modules/yara_scanner.py:371` `def create_default_rules()` -- Create a set of default YARA rules for common threats.

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

## plugins/rundll32_sct_from_url.lua
- `write_file` (function) `plugins/rundll32_sct_from_url.lua:4`
- `read_file` (function) `plugins/rundll32_sct_from_url.lua:12`
- `base64_encode` (function) `plugins/rundll32_sct_from_url.lua:22`
- `generate_sct` (function) `plugins/rundll32_sct_from_url.lua:58`

## plugins/validate_shellcode.lua
- `hex_to_bytes` (function) `plugins/validate_shellcode.lua:2`
- `esc_hex_to_bytes` (function) `plugins/validate_shellcode.lua:21`
- `hex_list_to_byte_values` (function) `plugins/validate_shellcode.lua:65`
- `validate_shellcode` (function) `plugins/validate_shellcode.lua:81`

## plugins/visualize_network.lua
- `visualize_network` (function) `plugins/visualize_network.lua:1`


Next: [API_p20.md](API_p20.md)
