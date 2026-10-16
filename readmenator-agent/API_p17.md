# API (page 17 of 23)
Previous: [API_p16.md](API_p16.md)

## modules/traffic_recorder.py
Imported by: `cli/commands/lazyops.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_proxy.py`, `tests/test_safety_gates.py`
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
- `UnifiedDashboard.render_unified` (method) `modules/unified_dashboard.py:173` `def render_unified(self)` -- Render the unified dashboard as a text string for CLI/TUI.
- `UnifiedDashboard.export_json` (method) `modules/unified_dashboard.py:254` `def export_json(self)` -- Export the unified snapshot as a JSON string.
- `get_unified_dashboard` (function) `modules/unified_dashboard.py:259` `def get_unified_dashboard(sessions_dir)` -- Return a module-level :class:`UnifiedDashboard` singleton.

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

## modules/vuln_bot_cli.py
Depends on: `modules/vulnbot.py`
- `parse_args` (function) `modules/vuln_bot_cli.py:10` `def parse_args()`
- `main` (function) `modules/vuln_bot_cli.py:22` `def main()`

## modules/vulnbot.py
Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/vuln_bot_cli.py`
- `VulnBotCLI.__init__` (method) `modules/vulnbot.py:30` `def __init__(self, provider, mode, debug, script_path)`
- `list_files` (function) `modules/vulnbot.py:86` `def list_files(directory)` -- Lista archivos en un directorio
- `read_file` (function) `modules/vulnbot.py:90` `def read_file(path)` -- Lee contenido de un archivo
- `edit_file` (function) `modules/vulnbot.py:95` `def edit_file(path, content, old_text)` -- Crea o edita un archivo
- `generate` (function) `modules/vulnbot.py:139` `def generate()`
- `VulnBotCLI.load_knowledge_base` (method) `modules/vulnbot.py:145` `def load_knowledge_base(self)`
- `VulnBotCLI.save_knowledge_base` (method) `modules/vulnbot.py:151` `def save_knowledge_base(self, kb)`
- `VulnBotCLI.get_relevant_knowledge` (method) `modules/vulnbot.py:155` `def get_relevant_knowledge(self, prompt)`
- `VulnBotCLI.create_complex_prompt` (method) `modules/vulnbot.py:160` `def create_complex_prompt(self, base_prompt, history, knowledge)`
- `VulnBotCLI.read_file_content` (method) `modules/vulnbot.py:176` `def read_file_content(self, file_path)`
- `VulnBotCLI.load_event_config` (method) `modules/vulnbot.py:182` `def load_event_config(self)`
- `VulnBotCLI.process_with_context` (method) `modules/vulnbot.py:190` `def process_with_context(self, file_path, event)`
- `VulnBotCLI.stream_response` (method) `modules/vulnbot.py:206` `def stream_response(self, prompt)`
- `generate` (function) `modules/vulnbot.py:207` `def generate()`
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
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/pwn.py`, `cli/ops_commands.py`, `lazyc2.py`, `modules/atomic_exploit_bridge.py`, `modules/exploit_recommender.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_intel.py`, `modules/live_surface.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/state_manager.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/integration_autonomous_flow.py`, `tests/test_autonomous_ops.py`, `tests/test_core_modules.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_moe_rl_swan.py`, `tests/test_ops_loot_phase.py`, `tests/test_phase1_data_gaps.py`, `tests/test_world_model_extended.py`
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
- `get_world_model` (function) `modules/world_model.py:1126` `def get_world_model(path)` -- Return (or create) the module-level singleton WorldModel.

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

## poc_tui/app.py
Depends on: `cli/commands/containers.py`, `lazyown.py`
Imported by: `poc_tui/__main__.py`, `poc_tui/run.py`, `poc_tui/test_app.py`
- `ShellBackend.__init__` (method) `poc_tui/app.py:47` `def __init__(self, base_dir)`
- `ShellBackend.import_shell_class` (method) `poc_tui/app.py:53` `def import_shell_class(self)` -- Import LazyOwnShell in the main thread (required for signal handlers).
- `ShellBackend.start` (method) `poc_tui/app.py:71` `def start(self)` -- Instantiate LazyOwnShell (must be called from main thread).
- `ShellBackend.run` (method) `poc_tui/app.py:83` `def run(self, cmd)` -- Execute a command and return its captured output.
- `ShellBackend.get_commands` (method) `poc_tui/app.py:106` `def get_commands(self)` -- Return {command_name: help_text} from the live shell.
- `ShellBackend.get_aliases` (method) `poc_tui/app.py:119` `def get_aliases(self)`
- `ShellBackend.stop` (method) `poc_tui/app.py:124` `def stop(self)`
- `DashboardPanel.__init__` (method) `poc_tui/app.py:140` `def __init__(self, base_dir)`
- `DashboardPanel.compose` (method) `poc_tui/app.py:144` `def compose(self)`
- `DashboardPanel.refresh_data` (method) `poc_tui/app.py:165` `def refresh_data(self, backend, cmd_count)` -- Pull latest state from the LIVE shell params (not stale disk file).
- `PluginBrowser.__init__` (method) `poc_tui/app.py:198` `def __init__(self)`
- `PluginBrowser.compose` (method) `poc_tui/app.py:201` `def compose(self)`
- `PluginBrowser.update_commands` (method) `poc_tui/app.py:207` `def update_commands(self, commands)`
- `OutputPanel.__init__` (method) `poc_tui/app.py:248` `def __init__(self)`
- `OutputPanel.compose` (method) `poc_tui/app.py:252` `def compose(self)`
- `OutputPanel.write_renderable` (method) `poc_tui/app.py:258` `def write_renderable(self, renderable)` -- Write a Rich renderable (no markup parsing applied).
- `OutputPanel.write_markup` (method) `poc_tui/app.py:263` `def write_markup(self, text)` -- Write a trusted internal string with Rich markup.
- `OutputPanel.append_command` (method) `poc_tui/app.py:268` `def append_command(self, cmd)`
- `OutputPanel.append_result` (method) `poc_tui/app.py:273` `def append_result(self, text, success)` -- Write real shell output, converting ANSI — never markup-parsed.
- `OutputPanel.append_error` (method) `poc_tui/app.py:283` `def append_error(self, text)` -- Write a TUI-side error message (plain, no markup from unsafe text).
- `OutputPanel.append_system` (method) `poc_tui/app.py:287` `def append_system(self, text)` -- Write a TUI-side status message.
- `LazyOwnTUI.__init__` (method) `poc_tui/app.py:394` `def __init__(self, base_dir)`
- `LazyOwnTUI.compose` (method) `poc_tui/app.py:405` `def compose(self)`
- `LazyOwnTUI.on_mount` (method) `poc_tui/app.py:418` `def on_mount(self)` -- Start the real cmd2 shell backend.
- `LazyOwnTUI.execute_command` (method) `poc_tui/app.py:470` `def execute_command(self, cmd_str)` -- Send command to real cmd2 shell, display captured output.
- `LazyOwnTUI.action_clear_output` (method) `poc_tui/app.py:539` `def action_clear_output(self)`
- `LazyOwnTUI.action_tab_complete` (method) `poc_tui/app.py:544` `def action_tab_complete(self)`
- `LazyOwnTUI.action_toggle_sidebar` (method) `poc_tui/app.py:549` `def action_toggle_sidebar(self)`
- `LazyOwnTUI.action_refresh_dashboard` (method) `poc_tui/app.py:555` `def action_refresh_dashboard(self)`
- `LazyOwnTUI.action_quit` (method) `poc_tui/app.py:561` `def action_quit(self)` -- Clean shutdown: drop the queue, stop the shell, exit the app.
- `LazyOwnTUI.on_command_submitted` (method) `poc_tui/app.py:577` `def on_command_submitted(self, event)`
- `LazyOwnTUI.on_key` (method) `poc_tui/app.py:586` `def on_key(self, event)`
- `main` (function) `poc_tui/app.py:629` `def main()`

## poc_tui/config.py
Imported by: `poc_tui/plugin_loader.py`
- `PayloadConfig.reload` (method) `poc_tui/config.py:21` `def reload(self)` -- Re-read payload.json from disk.
- `PayloadConfig.save` (method) `poc_tui/config.py:28` `def save(self)` -- Persist current state back to payload.json.
- `PayloadConfig.get` (method) `poc_tui/config.py:35` `def get(self, key, default)`
- `PayloadConfig.set` (method) `poc_tui/config.py:38` `def set(self, key, value)`
- `PayloadConfig.keys` (method) `poc_tui/config.py:41` `def keys(self)`
- `PayloadConfig.items` (method) `poc_tui/config.py:44` `def items(self)`

## poc_tui/plugin_loader.py
Depends on: `poc_tui/config.py`
- `PluginLoader.__init__` (method) `poc_tui/plugin_loader.py:91` `def __init__(self, config, base_dir)`
- `wrapper` (function) `poc_tui/plugin_loader.py:117` `def wrapper(arg)`
- `PluginLoader.load_all` (method) `poc_tui/plugin_loader.py:139` `def load_all(self)` -- Load yaml addons, lua plugins, and .tool files.
- `wrapper` (function) `poc_tui/plugin_loader.py:172` `def wrapper(arg)`
- `wrapper` (function) `poc_tui/plugin_loader.py:269` `def wrapper(arg)`
- `_LuaAppProxy.__init__` (method) `poc_tui/plugin_loader.py:294` `def __init__(self, config)`
- `_LuaAppProxy.params` (method) `poc_tui/plugin_loader.py:298` `def params(self)`
- `_LuaAppProxy.one_cmd` (method) `poc_tui/plugin_loader.py:301` `def one_cmd(self, cmd)`

## poc_tui/run.py
Depends on: `poc_tui/app.py`
- `main` (function) `poc_tui/run.py:9` `def main()`

## readmeneitor.py
- `normalize_trailing_newline` (function) `readmeneitor.py:74` `def normalize_trailing_newline(output_path)` -- Collapse a generated file tail to exactly one newline.
- `load_command_index` (function) `readmeneitor.py:83` `def load_command_index(index_path)` -- Load and parse the command index JSON file.
- `build_command_map` (function) `readmeneitor.py:104` `def build_command_map(index_data)` -- Build a lookup dict from command name to its metadata.
- `extract_docstrings_from_file` (function) `readmeneitor.py:132` `def extract_docstrings_from_file(filepath)` -- Parse a single Python file with AST and extract docstrings of ``do_*`` methods.
- `extract_docstrings_from_dir` (function) `readmeneitor.py:161` `def extract_docstrings_from_dir(dirpath)` -- Recursively scan a directory for Python files and extract all ``do_*`` docstrings.
- `group_commands_by_phase` (function) `readmeneitor.py:187` `def group_commands_by_phase(cmd_map)` -- Group command names by their kill-chain phase.
- `extract_functions_from_file` (function) `readmeneitor.py:209` `def extract_functions_from_file(filepath)` -- Parse a Python file with AST and extract docstrings of public functions.
- `write_utils_md` (function) `readmeneitor.py:241` `def write_utils_md(functions, output_path)` -- Generate UTILS.md with a helper-function reference for ``utils.py``.
- `write_commands_md` (function) `readmeneitor.py:276` `def write_commands_md(cmd_map, docstrings, groups, output_path)` -- Generate COMMANDS.md with a table of contents and per-phase command reference.
- `convert_to_html` (function) `readmeneitor.py:343` `def convert_to_html(md_path, html_path)` -- Convert the generated Markdown file to HTML using pandoc.
- `main` (function) `readmeneitor.py:379` `def main()` -- Entry point: scan sources, load metadata, and generate reference docs.

## run_topoexploit_agent.sh
- `banner` (function) `run_topoexploit_agent.sh:29`
- `start_api` (function) `run_topoexploit_agent.sh:38`

## scripts/activate_migrations.py
- `find_migrated_sets` (function) `scripts/activate_migrations.py:32` `def find_migrated_sets()` -- Return paths to all *_migrated.py files using PendingCommandSet.
- `extract_command_names` (function) `scripts/activate_migrations.py:42` `def extract_command_names(migrated_path)` -- Extract do_* method names from a migrated CommandSet file.
- `find_in_lazyown` (function) `scripts/activate_migrations.py:52` `def find_in_lazyown(command_names)` -- Return {name: (start_line, end_line)} for commands in lazyown.py.
- `remove_from_lazyown` (function) `scripts/activate_migrations.py:62` `def remove_from_lazyown(locations, dry_run)` -- Remove the specified do_* methods from lazyown.py.
- `activate_migrated_file` (function) `scripts/activate_migrations.py:75` `def activate_migrated_file(migrated_path, dry_run)` -- Change PendingCommandSet to LazyOwnCommandSet in the migrated file.
- `main` (function) `scripts/activate_migrations.py:88` `def main()`

## scripts/backfill_addon_os_trigger.py
- `classify_os` (function) `scripts/backfill_addon_os_trigger.py:104` `def classify_os(filename)` -- Return a MITRE-platform string for the addon based on filename.
- `known_trigger` (function) `scripts/backfill_addon_os_trigger.py:121` `def known_trigger(name)` -- Return the curated trigger tuple for an addon, or ``()``.
- `render_trigger` (function) `scripts/backfill_addon_os_trigger.py:127` `def render_trigger(trigger)` -- Render the trigger field as inline YAML matching the project style.
- `patch` (function) `scripts/backfill_addon_os_trigger.py:141` `def patch(path)` -- Return the new file content with ``os`` and ``trigger`` inserted.
- `main` (function) `scripts/backfill_addon_os_trigger.py:175` `def main()` -- Walk every addon and rewrite files that need backfilling.

## scripts/check_contract_manifest.py
Imported by: `tests/test_contract_manifest.py`
- `check_manifest` (function) `scripts/check_contract_manifest.py:176` `def check_manifest(config)` -- Return the list of documented contracts that are missing on disk.
- `main` (function) `scripts/check_contract_manifest.py:229` `def main(argv)` -- Run the manifest check and return the process exit code.

## scripts/devtools/command_audit.py
Depends on: `lazyown.py`
- `argparser_commands` (function) `scripts/devtools/command_audit.py:40` `def argparser_commands(config)` -- Return the command names decorated with ``@with_argparser``.
- `audit` (function) `scripts/devtools/command_audit.py:65` `def audit(config)` -- Run the dispatch and parser audit.
- `main` (function) `scripts/devtools/command_audit.py:105` `def main(argv)` -- Run the audit and return the process exit code.

## scripts/devtools/core_smoke.py
Depends on: `core/hardening.py`, `core/payload_schema.py`, `modules/db.py`, `modules/killchain.py`, `modules/payload_factory.py`
- `check_surfaces` (function) `scripts/devtools/core_smoke.py:64` `def check_surfaces(config)` -- Return the dotted names that are missing from the imported modules.
- `check_calls` (function) `scripts/devtools/core_smoke.py:81` `def check_calls()` -- Exercise a small safe subset of the public API.
- `main` (function) `scripts/devtools/core_smoke.py:118` `def main()` -- Run the smoke check and return the process exit code.


Next: [API_p18.md](API_p18.md)
