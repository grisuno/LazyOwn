# API (page 19 of 25)
Previous: [API_p18.md](API_p18.md)

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
Imported by: `cli/commands/campaign.py`, `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/privilege_escalation.py`, `cli/commands/pwn.py`, `cli/dashboard_tui.py`, `cli/ops_commands.py`, `cli/recommendation_signals.py`, `cli/session_brief.py`, `cli/session_resumer.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/services/backend.py`, `modules/atomic_exploit_bridge.py`, `modules/autonomous_exploit_engine.py`, `modules/beacon_recon.py`, `modules/estorides_importer.py`, `modules/event_consumers.py`, `modules/exploit_recommender.py`, `modules/golden_path.py`, `modules/gym_registry.py`, `modules/integrations/nuclei_parser.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_osinfer.py`, `modules/lazy_surface_diff.py`, `modules/lazy_world_diff.py`, `modules/live_surface.py`, `modules/loop_triggers.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/professional_report.py`, `modules/redteam_gym.py`, `modules/sinks/world_diff.py`, `modules/sinks/world_model.py`, `modules/state_manager.py`, `modules/surface_ops.py`, `modules/unified_dashboard.py`, `modules/verb_manifest.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_beacon_recon_sink.py`, `tests/test_codeql_alert_fixes.py`, `tests/test_cve_pipeline.py`, `tests/test_estorides_fusion.py`, `tests/test_golden_path.py`, `tests/test_gym_cli.py`, `tests/test_gym_lifecycle.py`, `tests/test_gym_registry.py`, `tests/test_infra_disposable.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazynmap_post.py`, `tests/test_loop_cli_catalog.py`, `tests/test_loop_trigger_hints.py`, `tests/test_ops_loot_phase.py`, `tests/test_orchestrator_api.py`, `tests/test_phase1_data_gaps.py`, `tests/test_session_brief.py`, `tests/test_single_source_of_truth.py`, `tests/test_world_model_extended.py`
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

## scripts/broadcom_wps_drive.sh
- `log` (function) `scripts/broadcom_wps_drive.sh:53`
- `warn` (function) `scripts/broadcom_wps_drive.sh:54`
- `die` (function) `scripts/broadcom_wps_drive.sh:55`
- `usage` (function) `scripts/broadcom_wps_drive.sh:57`
- `payload_value` (function) `scripts/broadcom_wps_drive.sh:61`
- `parse_flags` (function) `scripts/broadcom_wps_drive.sh:81`
- `detect_interface` (function) `scripts/broadcom_wps_drive.sh:151`
- `is_wireless` (function) `scripts/broadcom_wps_drive.sh:162`
- `apply_interface` (function) `scripts/broadcom_wps_drive.sh:166`
- `resolve_interface` (function) `scripts/broadcom_wps_drive.sh:170`
- `is_root` (function) `scripts/broadcom_wps_drive.sh:190`
- `have_sudo` (function) `scripts/broadcom_wps_drive.sh:194`
- `elevate` (function) `scripts/broadcom_wps_drive.sh:200`
- `interface_mode` (function) `scripts/broadcom_wps_drive.sh:210`
- `interface_up` (function) `scripts/broadcom_wps_drive.sh:216`
- `python_bin` (function) `scripts/broadcom_wps_drive.sh:227`
- `has_scapy` (function) `scripts/broadcom_wps_drive.sh:231`
- `do_monitor` (function) `scripts/broadcom_wps_drive.sh:235`
- `do_unmonitor` (function) `scripts/broadcom_wps_drive.sh:247`
- `ensure_monitor_mode` (function) `scripts/broadcom_wps_drive.sh:259`
- `run_fingerprint` (function) `scripts/broadcom_wps_drive.sh:268`
- `run_yara` (function) `scripts/broadcom_wps_drive.sh:308`
- `do_status` (function) `scripts/broadcom_wps_drive.sh:325`
- `do_doctor` (function) `scripts/broadcom_wps_drive.sh:348`
- `main` (function) `scripts/broadcom_wps_drive.sh:404`

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

## scripts/dirtyinit_drive.sh
- `log` (function) `scripts/dirtyinit_drive.sh:65`
- `warn` (function) `scripts/dirtyinit_drive.sh:66`
- `die` (function) `scripts/dirtyinit_drive.sh:67`
- `payload_value` (function) `scripts/dirtyinit_drive.sh:69`
- `parse_flags` (function) `scripts/dirtyinit_drive.sh:89`
- `require_adb` (function) `scripts/dirtyinit_drive.sh:130`
- `require_device` (function) `scripts/dirtyinit_drive.sh:134`
- `find_sdk` (function) `scripts/dirtyinit_drive.sh:141`
- `find_ndk` (function) `scripts/dirtyinit_drive.sh:152`
- `find_build_tools` (function) `scripts/dirtyinit_drive.sh:166`
- `find_android_jar` (function) `scripts/dirtyinit_drive.sh:173`
- `find_ndk_clang` (function) `scripts/dirtyinit_drive.sh:185`
- `find_java_tool` (function) `scripts/dirtyinit_drive.sh:201`
- `pack_apk` (function) `scripts/dirtyinit_drive.sh:211`
- `compile_activity` (function) `scripts/dirtyinit_drive.sh:255`
- `do_build` (function) `scripts/dirtyinit_drive.sh:265`
- `do_install` (function) `scripts/dirtyinit_drive.sh:329`
- `do_launch` (function) `scripts/dirtyinit_drive.sh:340`
- `tap_button` (function) `scripts/dirtyinit_drive.sh:348`
- `do_auto` (function) `scripts/dirtyinit_drive.sh:382`
- `do_extract` (function) `scripts/dirtyinit_drive.sh:393`
- `do_stage` (function) `scripts/dirtyinit_drive.sh:402`
- `do_run` (function) `scripts/dirtyinit_drive.sh:412`
- `do_logs` (function) `scripts/dirtyinit_drive.sh:418`
- `do_status` (function) `scripts/dirtyinit_drive.sh:423`
- `do_doctor` (function) `scripts/dirtyinit_drive.sh:468`
- `do_help` (function) `scripts/dirtyinit_drive.sh:525`
- `main` (function) `scripts/dirtyinit_drive.sh:529`

## scripts/generate_sbom.py
- `parse_requirement` (function) `scripts/generate_sbom.py:25` `def parse_requirement(line)` -- Split one requirements line into (name, pinned_version|None).
- `collect_components` (function) `scripts/generate_sbom.py:37` `def collect_components(with_ml)` -- Parse requirements files into CycloneDX components, deduplicated.
- `project_version` (function) `scripts/generate_sbom.py:68` `def project_version()` -- Read the package version from pyproject.toml.
- `build_sbom` (function) `scripts/generate_sbom.py:74` `def build_sbom(with_ml)` -- Assemble the CycloneDX document.
- `main` (function) `scripts/generate_sbom.py:92` `def main()` -- CLI entry point.

## scripts/journal.py
Imported by: `scripts/read_journal.py`, `tests/test_journal.py`
- `JournalConfig.from_git_remote` (method) `scripts/journal.py:71` `def from_git_remote(cls, remote, category)` -- Build a config from the ``origin`` remote of the current checkout.
- `Journal.repo_id` (method) `scripts/journal.py:184` `def repo_id(self)` -- The GraphQL node id of the repository.
- `Journal.category_id` (method) `scripts/journal.py:192` `def category_id(self)` -- The GraphQL node id of the journal category.
- `Journal.post` (method) `scripts/journal.py:206` `def post(self, title, body)` -- Create a journal entry and return its number, url, and title.
- `Journal.entries` (method) `scripts/journal.py:223` `def entries(self, limit)` -- Return the most recently updated journal entries.
- `main` (function) `scripts/journal.py:264` `def main(argv)` -- Run the journal CLI and return the process exit code.

## scripts/lazy_llamacpp_serve.sh
- `healthy` (function) `scripts/lazy_llamacpp_serve.sh:33`

## scripts/lazy_llamacpp_setup.sh
- `ask` (function) `scripts/lazy_llamacpp_setup.sh:40`

## scripts/lazy_opencode_config.py
Imported by: `skills/lazyown_mcp.py`
- `patch_opencode` (function) `scripts/lazy_opencode_config.py:46` `def patch_opencode(set_default, host)` -- Merge the llamacpp provider into the opencode config.
- `patch_hermes` (function) `scripts/lazy_opencode_config.py:93` `def patch_hermes(host)` -- Point the hermes config at the local llama.cpp server.
- `main` (function) `scripts/lazy_opencode_config.py:150` `def main(argv)` -- CLI entry: ``--target opencode|hermes|both [--set-default]``.

## scripts/mcp_call.py
- `_ToolAnswer.__init__` (method) `scripts/mcp_call.py:46` `def __init__(self, text, is_error)`
- `main` (function) `scripts/mcp_call.py:173` `def main(argv)` -- Parse the CLI, execute one MCP tool and print its answer.

## scripts/migrate_commandsets.py
- `merge_phase` (function) `scripts/migrate_commandsets.py:117` `def merge_phase(phase, dry_run)` -- Merge one phase's migrated methods into its clean file.
- `main` (function) `scripts/migrate_commandsets.py:158` `def main()`


Next: [API_p20.md](API_p20.md)
