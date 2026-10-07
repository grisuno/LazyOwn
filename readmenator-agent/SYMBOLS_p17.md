# Symbols (page 17 of 35)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_decrypt` | method | `modules/websocket_beacon.py:97` | `def _decrypt(self, data)` |
| `_encrypt` | method | `modules/websocket_beacon.py:91` | `def _encrypt(self, data)` |
| `_handle_connection` | method | `modules/websocket_beacon.py:310` | `def _handle_connection(self, websocket, path)` |
| `_jittered_sleep` | method | `modules/websocket_beacon.py:114` | `def _jittered_sleep(self)` |
| `_run_loop` | method | `modules/websocket_beacon.py:410` | `def _run_loop(self, loop)` |
| `check_in` | method | `modules/websocket_beacon.py:157` | `def check_in(self)` |
| `connect` | method | `modules/websocket_beacon.py:122` | `def connect(self)` |
| `list_beacons` | method | `modules/websocket_beacon.py:447` | `def list_beacons(self)` |
| `remove_stale_beacons` | method | `modules/websocket_beacon.py:464` | `def remove_stale_beacons(self, timeout)` |
| `run` | method | `modules/websocket_beacon.py:214` | `def run(self, command_handler)` |
| `send_result` | method | `modules/websocket_beacon.py:191` | `def send_result(self, task_id, output, exit_code)` |
| `send_task` | method | `modules/websocket_beacon.py:416` | `def send_task(self, beacon_id, command)` |
| `shutdown` | method | `modules/websocket_beacon.py:263` | `def shutdown(self)` |
| `start` | method | `modules/websocket_beacon.py:382` | `def start(self)` |
| `start_in_thread` | method | `modules/websocket_beacon.py:399` | `def start_in_thread(self)` |
| `stop` | method | `modules/websocket_beacon.py:392` | `def stop(self)` |
| `BUFFER_SIZE` | macro | `modules/win_rootkit/backup.c:18` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/win_rootkit/backup.c:27` | `` |
| `HIDE_FILE` | macro | `modules/win_rootkit/backup.c:21` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/win_rootkit/backup.c:22` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/win_rootkit/backup.c:19` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/win_rootkit/backup.c:24` | `#define PASSWORD` |
| `PID_FILE` | macro | `modules/win_rootkit/backup.c:20` | `#define PID_FILE` |
| `PORT` | macro | `modules/win_rootkit/backup.c:17` | `#define PORT` |
| `VirtualFile` | struct | `modules/win_rootkit/backup.c:33` | `` |
| `elp` | function | `modules/win_rootkit/backup.c:66` | `void elp()` |
| `ensure_hide_file_exists` | function | `modules/win_rootkit/backup.c:150` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/win_rootkit/backup.c:123` | `void ensure_key_file_exists()` |
| `ensure_pid_file_exists` | function | `modules/win_rootkit/backup.c:86` | `void ensure_pid_file_exists()` |
| `handle_client` | function | `modules/win_rootkit/backup.c:204` | `DWORD WINAPI handle_client(LPVOID client_socket)` |
| `infect_command` | function | `modules/win_rootkit/backup.c:179` | `void infect_command()` |
| `main` | function | `modules/win_rootkit/backup.c:540` | `int main()` |
| `monitor_shell` | function | `modules/win_rootkit/backup.c:430` | `DWORD WINAPI monitor_shell(LPVOID data)` |
| `DllMain` | function | `modules/win_rootkit/mrhyde.c:272` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `FILE_HIDE_PATH` | macro | `modules/win_rootkit/mrhyde.c:9` | `#define FILE_HIDE_PATH` |
| `FindProcessId` | function | `modules/win_rootkit/mrhyde.c:89` | `DWORD FindProcessId(const char* processName)` |
| `HideProcessByPID` | function | `modules/win_rootkit/mrhyde.c:115` | `void HideProcessByPID(DWORD pid)` |
| `HookFunctions` | function | `modules/win_rootkit/mrhyde.c:222` | `void HookFunctions()` |
| `HookedCreateToolhelp32Snapshot` | function | `modules/win_rootkit/mrhyde.c:189` | `HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)` |
| `HookedFindFirstFile` | function | `modules/win_rootkit/mrhyde.c:171` | `HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData)` |
| `HookedFindNextFile` | function | `modules/win_rootkit/mrhyde.c:180` | `BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData)` |
| `HookedProcess32First` | function | `modules/win_rootkit/mrhyde.c:198` | `BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` |
| `HookedProcess32Next` | function | `modules/win_rootkit/mrhyde.c:210` | `BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` |
| `MAX_HIDE_PIDS` | macro | `modules/win_rootkit/mrhyde.c:7` | `#define MAX_HIDE_PIDS` |
| `PID_FILE_PATH` | macro | `modules/win_rootkit/mrhyde.c:8` | `#define PID_FILE_PATH` |
| `RunExperiment` | function | `modules/win_rootkit/mrhyde.c:19` | `void __cdecl RunExperiment()` |
| `load_hidden_files` | function | `modules/win_rootkit/mrhyde.c:47` | `void load_hidden_files()` |
| `load_hidden_pids` | function | `modules/win_rootkit/mrhyde.c:24` | `void load_hidden_pids()` |
| `search_pid` | function | `modules/win_rootkit/mrhyde.c:137` | `BOOL search_pid()` |
| `should_hide_file` | function | `modules/win_rootkit/mrhyde.c:161` | `BOOL should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/win_rootkit/mrhyde.c:147` | `BOOL should_hide_pid(DWORD pid)` |
| `GetUsernameFromPid` | method | `modules/win_rootkit/win_rin3_rootkit.cs:143` | `` |
| `HookCreateFile` | method | `modules/win_rootkit/win_rin3_rootkit.cs:224` | `` |
| `HookFindFirstFile` | method | `modules/win_rootkit/win_rin3_rootkit.cs:212` | `` |
| `SECURITY_ATTRIBUTES` | class | `modules/win_rootkit/win_rin3_rootkit.cs:64` | `` |
| `SID` | class | `modules/win_rootkit/win_rin3_rootkit.cs:136` | `` |
| `SID_AND_ATTRIBUTES` | class | `modules/win_rootkit/win_rin3_rootkit.cs:129` | `` |
| `ShouldHidePid` | method | `modules/win_rootkit/win_rin3_rootkit.cs:201` | `` |
| `TOKEN_USER` | class | `modules/win_rootkit/win_rin3_rootkit.cs:123` | `` |
| `WIN32_FIND_DATA` | class | `modules/win_rootkit/win_rin3_rootkit.cs:47` | `` |
| `WinRing3Rootkit` | class | `modules/win_rootkit/win_rin3_rootkit.cs:30` | `` |
| `AddDllToAppInitDLLs` | function | `modules/win_rootkit/win_ring3_rootkit.c:191` | `BOOL AddDllToAppInitDLLs(const char* dllPath)` |
| `BUFFER_SIZE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:19` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/win_rootkit/win_ring3_rootkit.c:28` | `` |
| `DownloadDLL` | function | `modules/win_rootkit/win_ring3_rootkit.c:79` | `BOOL DownloadDLL(const char* url, PBYTE* buffer, DWORD* size)` |
| `GetProcessIdByName` | function | `modules/win_rootkit/win_ring3_rootkit.c:240` | `DWORD GetProcessIdByName(const char* processName)` |
| `Gifted` | function | `modules/win_rootkit/win_ring3_rootkit.c:270` | `BOOL Gifted(DWORD processId, const char* dllPath)` |
| `HIDE_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:22` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:23` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/win_rootkit/win_ring3_rootkit.c:20` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/win_rootkit/win_ring3_rootkit.c:25` | `#define PASSWORD` |
| `PIDArray` | struct | `modules/win_rootkit/win_ring3_rootkit.c:40` | `` |
| `PID_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:21` | `#define PID_FILE` |
| `PORT` | macro | `modules/win_rootkit/win_ring3_rootkit.c:18` | `#define PORT` |
| `ReflectiveLoadDLL` | function | `modules/win_rootkit/win_ring3_rootkit.c:99` | `BOOL ReflectiveLoadDLL(PBYTE dllBuffer, DWORD dllSize)` |
| `VirtualFile` | struct | `modules/win_rootkit/win_ring3_rootkit.c:34` | `` |
| `addPID` | function | `modules/win_rootkit/win_ring3_rootkit.c:153` | `void addPID(PIDArray *array, DWORD pid)` |
| `elp` | function | `modules/win_rootkit/win_ring3_rootkit.c:362` | `void elp()` |
| `ensure_hide_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:446` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:419` | `void ensure_key_file_exists()` |
| `ensure_pid_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:382` | `void ensure_pid_file_exists()` |
| `freePIDArray` | function | `modules/win_rootkit/win_ring3_rootkit.c:162` | `void freePIDArray(PIDArray *array)` |
| `getPIDsFromTasklist` | function | `modules/win_rootkit/win_ring3_rootkit.c:166` | `void getPIDsFromTasklist(PIDArray *pidArray)` |
| `giveGift` | function | `modules/win_rootkit/win_ring3_rootkit.c:475` | `BOOL giveGift()` |
| `handle_client` | function | `modules/win_rootkit/win_ring3_rootkit.c:526` | `DWORD WINAPI handle_client(LPVOID client_socket)` |
| `initPIDArray` | function | `modules/win_rootkit/win_ring3_rootkit.c:146` | `void initPIDArray(PIDArray *array)` |
| `main` | function | `modules/win_rootkit/win_ring3_rootkit.c:865` | `int main()` |
| `monitor_shell` | function | `modules/win_rootkit/win_ring3_rootkit.c:755` | `DWORD WINAPI monitor_shell(LPVOID data)` |
| `DllMain` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:94` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `HIDDEN_DIR` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:32` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:33` | `#define HIDDEN_FILE` |
| `HIDE_USER` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:34` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:35` | `#define MAX_HIDE_PIDS` |
| `get_username_from_pid` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:42` | `char* get_username_from_pid(DWORD pid)` |
| `hook_CreateFile` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:85` | `HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES ...` |
| `hook_FindFirstFile` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:75` | `HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)` |
| `should_hide_pid` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:65` | `int should_hide_pid(const char* pid)` |
| `CredentialEntry` | class | `modules/world_model.py:189` | `class CredentialEntry` |
| `DomainEntry` | class | `modules/world_model.py:215` | `class DomainEntry` |
| `EmailEntry` | class | `modules/world_model.py:207` | `class EmailEntry` |
| `EngagementPhase` | class | `modules/world_model.py:168` | `class EngagementPhase(StrEnum)` |
| `HostEntry` | class | `modules/world_model.py:365` | `class HostEntry` |
| `HostState` | class | `modules/world_model.py:152` | `class HostState(StrEnum)` |
| `NetworkGraph` | class | `modules/world_model.py:245` | `class NetworkGraph` |
| `NetworkRelation` | class | `modules/world_model.py:223` | `class NetworkRelation` |
| `ServiceInfo` | class | `modules/world_model.py:180` | `class ServiceInfo` |
| `VulnerabilityEntry` | class | `modules/world_model.py:198` | `class VulnerabilityEntry` |
| `WorldModel` | class | `modules/world_model.py:509` | `class WorldModel` |
| `_PhaseDeriver` | class | `modules/world_model.py:417` | `class _PhaseDeriver` |
| `__init__` | method | `modules/world_model.py:268` | `def __init__(self)` |
| `__init__` | method | `modules/world_model.py:517` | `def __init__(self, path)` |
| `_derive_crypto_key` | function | `modules/world_model.py:58` | `def _derive_crypto_key(password, salt)` |
| `_load` | method | `modules/world_model.py:1018` | `def _load(self)` |
| `_master_password` | function | `modules/world_model.py:69` | `def _master_password()` |
| `_save` | method | `modules/world_model.py:998` | `def _save(self)` |
| `add_credential` | method | `modules/world_model.py:621` | `def add_credential(self, value, host, service)` |
| `add_domain` | method | `modules/world_model.py:716` | `def add_domain(self, domain, host, context)` |
| `add_email` | method | `modules/world_model.py:710` | `def add_email(self, address, host, context)` |
| `add_host` | method | `modules/world_model.py:533` | `def add_host(self, ip)` |
| `add_note` | method | `modules/world_model.py:577` | `def add_note(self, ip, note)` |
| `add_relation` | method | `modules/world_model.py:275` | `def add_relation(self, relation)` |
| `add_relation` | method | `modules/world_model.py:895` | `def add_relation(self, source, target, relation, weight)` |
| `add_service` | method | `modules/world_model.py:374` | `def add_service(self, svc)` |
| `add_service` | method | `modules/world_model.py:560` | `def add_service(self, ip, port, name, version, protocol)` |
| `add_vulnerability` | method | `modules/world_model.py:704` | `def add_vulnerability(self, description, host, cve, severity)` |
| `advance` | method | `modules/world_model.py:378` | `def advance(self, new_state)` |
| `advance_host` | method | `modules/world_model.py:551` | `def advance_host(self, ip, new_state)` |
| `can_advance_to` | method | `modules/world_model.py:164` | `def can_advance_to(self, next_state)` |
| `consume_policy_facts` | method | `modules/world_model.py:803` | `def consume_policy_facts(self, facts_path)` |
| `degree_centrality` | method | `modules/world_model.py:295` | `def degree_centrality(self)` |
| `derive` | method | `modules/world_model.py:431` | `def derive(self, hosts)` |
| `from_dict` | method | `modules/world_model.py:349` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/world_model.py:398` | `def from_dict(cls, d)` |
| `get_host` | method | `modules/world_model.py:598` | `def get_host(self, ip)` |
| `get_hosts_summary` | method | `modules/world_model.py:610` | `def get_hosts_summary(self)` |
| `get_phase` | method | `modules/world_model.py:931` | `def get_phase(self)` |
| `get_suggested_tools` | method | `modules/world_model.py:935` | `def get_suggested_tools(self)` |
| `get_world_model` | method | `modules/world_model.py:1090` | `def get_world_model(path)` |
| `graph_snapshot` | method | `modules/world_model.py:924` | `def graph_snapshot(self)` |
| `in_degree` | method | `modules/world_model.py:287` | `def in_degree(self, node)` |
| `link_credential_to_failure` | method | `modules/world_model.py:674` | `def link_credential_to_failure(self, value, host)` |
| `link_credential_to_success` | method | `modules/world_model.py:653` | `def link_credential_to_success(self, value, host)` |
| `neighbors` | method | `modules/world_model.py:283` | `def neighbors(self, node)` |
| `out_degree` | method | `modules/world_model.py:291` | `def out_degree(self, node)` |
| `pivot_candidates` | method | `modules/world_model.py:310` | `def pivot_candidates(self, top_k)` |
| `pivot_candidates` | method | `modules/world_model.py:916` | `def pivot_candidates(self, top_k)` |
| `rank` | method | `modules/world_model.py:161` | `def rank(self)` |
| `read_state_dict` | function | `modules/world_model.py:74` | `def read_state_dict(path)` |
| `reload` | method | `modules/world_model.py:1042` | `def reload(self)` |
| `reset` | method | `modules/world_model.py:1058` | `def reset(self)` |
| `reset_host` | method | `modules/world_model.py:541` | `def reset_host(self, ip)` |
| `set_os_hint` | method | `modules/world_model.py:584` | `def set_os_hint(self, ip, os_hint)` |
| `snapshot` | method | `modules/world_model.py:1069` | `def snapshot(self)` |
| `to_context_string` | method | `modules/world_model.py:938` | `def to_context_string(self)` |
| `to_dict` | method | `modules/world_model.py:332` | `def to_dict(self)` |
| `to_dict` | method | `modules/world_model.py:386` | `def to_dict(self)` |
| `update_from_findings` | method | `modules/world_model.py:730` | `def update_from_findings(self, findings)` |
| `write_state_dict` | function | `modules/world_model.py:119` | `def write_state_dict(path, data)` |
| `YAMLPromptGenerator` | class | `modules/yaml_generator.py:17` | `class YAMLPromptGenerator` |
| `__init__` | method | `modules/yaml_generator.py:18` | `def __init__(self, provider, api_key)` |
| `_load_model` | method | `modules/yaml_generator.py:32` | `def _load_model(self)` |
| `create_yaml_addon` | method | `modules/yaml_generator.py:109` | `def create_yaml_addon(self, user_request, output_dir)` |
| `extract_yaml_from_markdown` | method | `modules/yaml_generator.py:100` | `def extract_yaml_from_markdown(self, text)` |
| `generate_prompt` | method | `modules/yaml_generator.py:54` | `def generate_prompt(self, user_request)` |
| `load_payload` | method | `modules/yaml_generator.py:25` | `def load_payload(self)` |
| `main` | method | `modules/yaml_generator.py:140` | `def main()` |
| `YaraScanner` | class | `modules/yara_scanner.py:22` | `class YaraScanner` |
| `__init__` | method | `modules/yara_scanner.py:30` | `def __init__(self, rules_dir, auto_compile)` |
| `_format_match` | method | `modules/yara_scanner.py:162` | `def _format_match(self, match)` |
| `_load_external_vars` | method | `modules/yara_scanner.py:44` | `def _load_external_vars(self)` |
| `_scan_with_timeout` | method | `modules/yara_scanner.py:129` | `def _scan_with_timeout(self, filepath, externals, timeout)` |
| `_sha256` | method | `modules/yara_scanner.py:247` | `def _sha256(filepath)` |
| `add_rule` | method | `modules/yara_scanner.py:255` | `def add_rule(self, name, content)` |
| `compile_all` | method | `modules/yara_scanner.py:53` | `def compile_all(self)` |
| `create_default_rules` | method | `modules/yara_scanner.py:366` | `def create_default_rules()` |
| `download_community_rules` | method | `modules/yara_scanner.py:295` | `def download_community_rules(self)` |
| `ensure_directory` | method | `modules/yara_scanner.py:40` | `def ensure_directory(self)` |
| `ioc_scan` | method | `modules/yara_scanner.py:327` | `def ioc_scan(self, target_path, iocs)` |
| `list_rules` | method | `modules/yara_scanner.py:274` | `def list_rules(self)` |
| `scan_directory` | method | `modules/yara_scanner.py:186` | `def scan_directory(self, directory, recursive, extensions, max_files)` |
| `scan_file` | method | `modules/yara_scanner.py:97` | `def scan_file(self, filepath, timeout)` |
| `target` | method | `modules/yara_scanner.py:137` | `def target()` |
| `all` | function | `plugins/generate_c_reverse_shell.lua:108` | `` |
| `generate_c_reverse_shell` | function | `plugins/generate_c_reverse_shell.lua:1` | `` |
| `generate_cleanup_commands` | function | `plugins/generate_cleanup_commands.lua:3` | `` |
| `generate_html_payload` | function | `plugins/generate_html_payload.lua:1` | `` |
| `generate_lateral_command` | function | `plugins/generate_lateral_command.lua:4` | `` |
| `all` | function | `plugins/generate_linux_asm_reverse_shell.lua:121` | `` |
| `generate_linux_asm_reverse_shell` | function | `plugins/generate_linux_asm_reverse_shell.lua:1` | `` |
| `generate_linux_raw_shellcode` | function | `plugins/generate_linux_raw_shellcode.lua:1` | `` |
| `Xor` | function | `plugins/generate_lolbird.lua:64` | `` |
| `generate_lolbird_ps1` | function | `plugins/generate_lolbird.lua:44` | `` |
| `read_file` | function | `plugins/generate_lolbird.lua:12` | `` |
| `write_file` | function | `plugins/generate_lolbird.lua:4` | `` |
| `xor_hex_string` | function | `plugins/generate_lolbird.lua:21` | `` |
| `xor_string` | function | `plugins/generate_lolbird.lua:31` | `` |
| `execute_command_to_file` | function | `plugins/generate_msfvenom_loader.lua:2` | `` |
| `generate_loader` | function | `plugins/generate_msfvenom_loader.lua:49` | `` |
| `generate_msfvenom_loader` | function | `plugins/generate_msfvenom_loader.lua:104` | `` |
| `hex_to_nasm` | function | `plugins/generate_msfvenom_loader.lua:18` | `` |
| `read_file` | function | `plugins/generate_msfvenom_loader.lua:7` | `` |
| `generate_msfvenom_loader_windows` | function | `plugins/generate_msfvenom_loader_windows.lua:2` | `` |
| `generate_reverse_shell` | function | `plugins/generate_reverse_shell.lua:1` | `` |
| `generate_stub_ps1` | function | `plugins/generate_stub.lua:43` | `` |
| `read_file` | function | `plugins/generate_stub.lua:12` | `` |
| `write_file` | function | `plugins/generate_stub.lua:4` | `` |
| `xor_data` | function | `plugins/generate_stub.lua:21` | `` |
| `xor_string` | function | `plugins/generate_stub.lua:30` | `` |
| `load_plugin` | function | `plugins/init_plugins.lua:6` | `` |
| `kerberos_harvest` | function | `plugins/kerberos_harvest.lua:1` | `` |
| `read_file` | function | `plugins/lolbas_certutil_download_exec.lua:13` | `` |
| `write_file` | function | `plugins/lolbas_certutil_download_exec.lua:5` | `` |
| `xor_data` | function | `plugins/lolbas_certutil_download_exec.lua:21` | `` |
| `run_msfvenom` | function | `plugins/lolbas_certutil_exe.lua:2` | `` |
| `write_file` | function | `plugins/lolbas_wmic_xsl_execution.lua:4` | `` |
| `parse_nmap_with_xmlstarlet` | function | `plugins/parse_nmap_with_xmlstarlet.lua:1` | `` |
| `run_nuclei_on_nmap_files` | function | `plugins/run_nuclei_on_nmap_files.lua:1` | `` |
| `run_python_rev_c2` | function | `plugins/run_python_rev_c2.lua:2` | `` |
| `base64_encode` | function | `plugins/rundll32_sct_from_url.lua:22` | `` |
| `generate_sct` | function | `plugins/rundll32_sct_from_url.lua:58` | `` |
| `read_file` | function | `plugins/rundll32_sct_from_url.lua:12` | `` |
| `write_file` | function | `plugins/rundll32_sct_from_url.lua:4` | `` |
| `esc_hex_to_bytes` | function | `plugins/validate_shellcode.lua:21` | `` |
| `hex_list_to_byte_values` | function | `plugins/validate_shellcode.lua:65` | `` |
| `hex_to_bytes` | function | `plugins/validate_shellcode.lua:2` | `` |
| `validate_shellcode` | function | `plugins/validate_shellcode.lua:81` | `` |
| `visualize_network` | function | `plugins/visualize_network.lua:1` | `` |
| `DashboardPanel` | class | `poc_tui/app.py:137` | `class DashboardPanel(Static)` |
| `LazyOwnTUI` | class | `poc_tui/app.py:297` | `class LazyOwnTUI(App)` |
| `OutputPanel` | class | `poc_tui/app.py:240` | `class OutputPanel(VerticalScroll)` |
| `PluginBrowser` | class | `poc_tui/app.py:195` | `class PluginBrowser(Static)` |
| `ShellBackend` | class | `poc_tui/app.py:44` | `class ShellBackend` |
| `__init__` | method | `poc_tui/app.py:47` | `def __init__(self, base_dir)` |
| `__init__` | method | `poc_tui/app.py:140` | `def __init__(self, base_dir)` |
| `__init__` | method | `poc_tui/app.py:198` | `def __init__(self)` |
| `__init__` | method | `poc_tui/app.py:248` | `def __init__(self)` |
| `__init__` | method | `poc_tui/app.py:394` | `def __init__(self, base_dir)` |
| `_auto_refresh_dashboard` | method | `poc_tui/app.py:464` | `def _auto_refresh_dashboard(self)` |
| `_drain_queue` | method | `poc_tui/app.py:495` | `def _drain_queue(self)` |
| `_guess_category` | method | `poc_tui/app.py:223` | `def _guess_category(name, help_text)` |
| `_init_backend` | method | `poc_tui/app.py:429` | `def _init_backend()` |
| `_log` | method | `poc_tui/app.py:255` | `def _log(self)` |
| `_on_backend_ready` | method | `poc_tui/app.py:444` | `def _on_backend_ready(self)` |
| `_show_result` | method | `poc_tui/app.py:525` | `def _show_result(self, result)` |
| `_tab_complete` | method | `poc_tui/app.py:605` | `def _tab_complete(self, inp)` |
| `_work` | method | `poc_tui/app.py:510` | `def _work()` |
| `action_clear_output` | method | `poc_tui/app.py:539` | `def action_clear_output(self)` |
| `action_quit` | method | `poc_tui/app.py:561` | `def action_quit(self)` |
| `action_refresh_dashboard` | method | `poc_tui/app.py:555` | `def action_refresh_dashboard(self)` |
| `action_tab_complete` | method | `poc_tui/app.py:544` | `def action_tab_complete(self)` |
| `action_toggle_sidebar` | method | `poc_tui/app.py:549` | `def action_toggle_sidebar(self)` |
| `append_command` | method | `poc_tui/app.py:268` | `def append_command(self, cmd)` |
| `append_error` | method | `poc_tui/app.py:283` | `def append_error(self, text)` |
| `append_result` | method | `poc_tui/app.py:273` | `def append_result(self, text, success)` |
| `append_system` | method | `poc_tui/app.py:287` | `def append_system(self, text)` |
| `compose` | method | `poc_tui/app.py:144` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:201` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:252` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:405` | `def compose(self)` |
| `execute_command` | method | `poc_tui/app.py:470` | `def execute_command(self, cmd_str)` |
| `get_aliases` | method | `poc_tui/app.py:119` | `def get_aliases(self)` |
| `get_commands` | method | `poc_tui/app.py:106` | `def get_commands(self)` |
| `import_shell_class` | method | `poc_tui/app.py:53` | `def import_shell_class(self)` |
| `main` | method | `poc_tui/app.py:629` | `def main()` |
| `on_command_submitted` | method | `poc_tui/app.py:577` | `def on_command_submitted(self, event)` |
| `on_key` | method | `poc_tui/app.py:586` | `def on_key(self, event)` |
| `on_mount` | method | `poc_tui/app.py:418` | `def on_mount(self)` |
| `refresh_data` | method | `poc_tui/app.py:165` | `def refresh_data(self, backend, cmd_count)` |
| `run` | method | `poc_tui/app.py:83` | `def run(self, cmd)` |
| `start` | method | `poc_tui/app.py:71` | `def start(self)` |
| `stop` | method | `poc_tui/app.py:124` | `def stop(self)` |
| `update_commands` | method | `poc_tui/app.py:207` | `def update_commands(self, commands)` |
| `write_markup` | method | `poc_tui/app.py:263` | `def write_markup(self, text)` |
| `write_renderable` | method | `poc_tui/app.py:258` | `def write_renderable(self, renderable)` |
| `PayloadConfig` | class | `poc_tui/config.py:12` | `class PayloadConfig` |
| `__contains__` | method | `poc_tui/config.py:53` | `def __contains__(self, key)` |
| `__getitem__` | method | `poc_tui/config.py:47` | `def __getitem__(self, key)` |
| `__post_init__` | method | `poc_tui/config.py:18` | `def __post_init__(self)` |
| `__setitem__` | method | `poc_tui/config.py:50` | `def __setitem__(self, key, value)` |
| `get` | method | `poc_tui/config.py:35` | `def get(self, key, default)` |
| `items` | method | `poc_tui/config.py:44` | `def items(self)` |
| `keys` | method | `poc_tui/config.py:41` | `def keys(self)` |
| `reload` | method | `poc_tui/config.py:21` | `def reload(self)` |
| `save` | method | `poc_tui/config.py:28` | `def save(self)` |
| `set` | method | `poc_tui/config.py:38` | `def set(self, key, value)` |
| `PluginLoader` | class | `poc_tui/plugin_loader.py:73` | `class PluginLoader` |
| `PluginSpec` | class | `poc_tui/plugin_loader.py:28` | `class PluginSpec` |
| `_LuaAppProxy` | class | `poc_tui/plugin_loader.py:280` | `class _LuaAppProxy` |
| `__init__` | method | `poc_tui/plugin_loader.py:80` | `def __init__(self, config, base_dir)` |
| `__init__` | method | `poc_tui/plugin_loader.py:283` | `def __init__(self, config)` |
| `_list_files` | method | `poc_tui/plugin_loader.py:120` | `def _list_files(self, directory)` |
| `_load_lua_plugins` | method | `poc_tui/plugin_loader.py:212` | `def _load_lua_plugins(self)` |
| `_load_tool_files` | method | `poc_tui/plugin_loader.py:237` | `def _load_tool_files(self)` |
| `_load_yaml_addons` | method | `poc_tui/plugin_loader.py:137` | `def _load_yaml_addons(self)` |
| `_lua_register` | method | `poc_tui/plugin_loader.py:103` | `def _lua_register(self, name, func)` |
| `_register_tool` | method | `poc_tui/plugin_loader.py:250` | `def _register_tool(self, data)` |
| `_register_yaml_addon` | method | `poc_tui/plugin_loader.py:150` | `def _register_yaml_addon(self, data)` |
| `_replace_placeholders` | method | `poc_tui/plugin_loader.py:40` | `def _replace_placeholders(command, params)` |
| `_setup_lua` | method | `poc_tui/plugin_loader.py:94` | `def _setup_lua(self)` |
| `_subst` | method | `poc_tui/plugin_loader.py:43` | `def _subst(match)` |
| `_validate_clone_url` | method | `poc_tui/plugin_loader.py:51` | `def _validate_clone_url(url)` |
| `load_all` | method | `poc_tui/plugin_loader.py:128` | `def load_all(self)` |
| `one_cmd` | method | `poc_tui/plugin_loader.py:290` | `def one_cmd(self, cmd)` |
| `params` | method | `poc_tui/plugin_loader.py:287` | `def params(self)` |
| `wrapper` | method | `poc_tui/plugin_loader.py:106` | `def wrapper(arg)` |
| `wrapper` | method | `poc_tui/plugin_loader.py:161` | `def wrapper(arg)` |
| `wrapper` | method | `poc_tui/plugin_loader.py:258` | `def wrapper(arg)` |
| `main` | function | `poc_tui/run.py:9` | `def main()` |
| `TestLazyOwnTUIApp` | class | `poc_tui/test_app.py:100` | `class TestLazyOwnTUIApp` |
| `TestShellBackend` | class | `poc_tui/test_app.py:32` | `class TestShellBackend` |
| `_make_backend` | function | `poc_tui/test_app.py:26` | `def _make_backend()` |
| `_run_async` | function | `poc_tui/test_app.py:17` | `def _run_async(coro)` |
| `_t` | method | `poc_tui/test_app.py:106` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:115` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:126` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:136` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:152` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:165` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:182` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:198` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:210` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:225` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:235` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:248` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:270` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:291` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:307` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:321` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:342` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:361` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:374` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:399` | `def _t()` |
| `_t` | method | `poc_tui/test_app.py:414` | `def _t()` |
| `test_app_creates` | method | `poc_tui/test_app.py:101` | `def test_app_creates(self)` |
| `test_app_starts_stops` | method | `poc_tui/test_app.py:105` | `def test_app_starts_stops(self)` |
| `test_backend_ready` | method | `poc_tui/test_app.py:234` | `def test_backend_ready(self)` |
| `test_buffer_cleared` | method | `poc_tui/test_app.py:86` | `def test_buffer_cleared(self)` |
| `test_busy_command_shows_running_indicator` | method | `poc_tui/test_app.py:373` | `def test_busy_command_shows_running_indicator(self)` |
| `test_command_output_visible_in_screenshot` | method | `poc_tui/test_app.py:411` | `def test_command_output_visible_in_screenshot(self)` |
| `test_commands_queue_serialized` | method | `poc_tui/test_app.py:318` | `def test_commands_queue_serialized(self)` |
| `test_execute_help` | method | `poc_tui/test_app.py:135` | `def test_execute_help(self)` |
| `test_focus_returns_after_command` | method | `poc_tui/test_app.py:341` | `def test_focus_returns_after_command(self)` |
| `test_get_aliases` | method | `poc_tui/test_app.py:71` | `def test_get_aliases(self)` |
| `test_get_commands` | method | `poc_tui/test_app.py:62` | `def test_get_commands(self)` |
| `test_history_down` | method | `poc_tui/test_app.py:181` | `def test_history_down(self)` |
| `test_history_up` | method | `poc_tui/test_app.py:164` | `def test_history_up(self)` |
| `test_init_sets_base_dir` | method | `poc_tui/test_app.py:33` | `def test_init_sets_base_dir(self)` |
| `test_input_cleared_after_submit` | method | `poc_tui/test_app.py:151` | `def test_input_cleared_after_submit(self)` |
| `test_input_has_focus` | method | `poc_tui/test_app.py:125` | `def test_input_has_focus(self)` |
| `test_layout_all_panels_render_in_screenshot` | method | `poc_tui/test_app.py:392` | `def test_layout_all_panels_render_in_screenshot(self)` |
| `test_output_renders_ansi_codes` | method | `poc_tui/test_app.py:358` | `def test_output_renders_ansi_codes(self)` |
| `test_panels_visible` | method | `poc_tui/test_app.py:114` | `def test_panels_visible(self)` |
| `test_q_is_quit_not_shell_alias` | method | `poc_tui/test_app.py:288` | `def test_q_is_quit_not_shell_alias(self)` |
| `test_quit` | method | `poc_tui/test_app.py:224` | `def test_quit(self)` |
| `test_quit_word_not_sent_to_backend` | method | `poc_tui/test_app.py:304` | `def test_quit_word_not_sent_to_backend(self)` |
| `test_run_before_start` | method | `poc_tui/test_app.py:37` | `def test_run_before_start(self)` |
| `test_run_help` | method | `poc_tui/test_app.py:55` | `def test_run_help(self)` |
| `test_run_show` | method | `poc_tui/test_app.py:48` | `def test_run_show(self)` |
| `test_set_and_show` | method | `poc_tui/test_app.py:78` | `def test_set_and_show(self)` |
| `test_set_updates_dashboard` | method | `poc_tui/test_app.py:247` | `def test_set_updates_dashboard(self)` |
| `test_show_command_output_in_log` | method | `poc_tui/test_app.py:269` | `def test_show_command_output_in_log(self)` |
| `test_start_and_stop` | method | `poc_tui/test_app.py:42` | `def test_start_and_stop(self)` |
| `test_tab_complete` | method | `poc_tui/test_app.py:197` | `def test_tab_complete(self)` |
| `test_toggle_sidebar` | method | `poc_tui/test_app.py:209` | `def test_toggle_sidebar(self)` |
| `_build_substitutions` | function | `pwntomate.py:94` | `def _build_substitutions(host_addr, port, toolname_value, basedir_value)` |
| `_run_tool` | function | `pwntomate.py:146` | `def _run_tool(cmd)` |
| `build_command_map` | function | `readmeneitor.py:95` | `def build_command_map(index_data)` |
| `convert_to_html` | function | `readmeneitor.py:332` | `def convert_to_html(md_path, html_path)` |
| `extract_docstrings_from_dir` | function | `readmeneitor.py:152` | `def extract_docstrings_from_dir(dirpath)` |
| `extract_docstrings_from_file` | function | `readmeneitor.py:123` | `def extract_docstrings_from_file(filepath)` |
| `extract_functions_from_file` | function | `readmeneitor.py:200` | `def extract_functions_from_file(filepath)` |
| `group_commands_by_phase` | function | `readmeneitor.py:178` | `def group_commands_by_phase(cmd_map)` |
| `load_command_index` | function | `readmeneitor.py:74` | `def load_command_index(index_path)` |
| `main` | function | `readmeneitor.py:364` | `def main()` |
| `write_commands_md` | function | `readmeneitor.py:266` | `def write_commands_md(cmd_map, docstrings, groups, output_path)` |
| `write_utils_md` | function | `readmeneitor.py:232` | `def write_utils_md(functions, output_path)` |
| `banner` | function | `run_topoexploit_agent.sh:29` | `` |
| `start_api` | function | `run_topoexploit_agent.sh:38` | `` |
| `MigrationError` | class | `scripts/activate_migrations.py:28` | `class MigrationError(Exception)` |
| `activate_migrated_file` | method | `scripts/activate_migrations.py:75` | `def activate_migrated_file(migrated_path, dry_run)` |
| `extract_command_names` | method | `scripts/activate_migrations.py:42` | `def extract_command_names(migrated_path)` |
| `find_in_lazyown` | method | `scripts/activate_migrations.py:52` | `def find_in_lazyown(command_names)` |
| `find_migrated_sets` | method | `scripts/activate_migrations.py:32` | `def find_migrated_sets()` |
| `main` | method | `scripts/activate_migrations.py:88` | `def main()` |
| `remove_from_lazyown` | method | `scripts/activate_migrations.py:62` | `def remove_from_lazyown(locations, dry_run)` |
| `classify_os` | function | `scripts/backfill_addon_os_trigger.py:104` | `def classify_os(filename)` |
| `known_trigger` | function | `scripts/backfill_addon_os_trigger.py:121` | `def known_trigger(name)` |
| `main` | function | `scripts/backfill_addon_os_trigger.py:175` | `def main()` |
| `patch` | function | `scripts/backfill_addon_os_trigger.py:141` | `def patch(path)` |
| `render_trigger` | function | `scripts/backfill_addon_os_trigger.py:127` | `def render_trigger(trigger)` |
| `ManifestConfig` | class | `scripts/check_contract_manifest.py:34` | `class ManifestConfig` |
| `__post_init__` | method | `scripts/check_contract_manifest.py:53` | `def __post_init__(self)` |
| `_collect_doc_imports` | method | `scripts/check_contract_manifest.py:163` | `def _collect_doc_imports(text)` |
| `_dotted_symbol_exists` | method | `scripts/check_contract_manifest.py:112` | `def _dotted_symbol_exists(token, config)` |
| `_extract_dotted_tokens` | method | `scripts/check_contract_manifest.py:209` | `def _extract_dotted_tokens(text, config)` |
| `_extract_path_tokens` | method | `scripts/check_contract_manifest.py:138` | `def _extract_path_tokens(text, config)` |
| `_iter_table_cells` | method | `scripts/check_contract_manifest.py:127` | `def _iter_table_cells(text)` |
| `_module_path` | method | `scripts/check_contract_manifest.py:100` | `def _module_path(module, config)` |
| `_resolve` | method | `scripts/check_contract_manifest.py:58` | `def _resolve(self, path)` |
| `_resolve_reference` | method | `scripts/check_contract_manifest.py:154` | `def _resolve_reference(token, config)` |
| `_top_level_names` | method | `scripts/check_contract_manifest.py:72` | `def _top_level_names(path)` |
| `check_manifest` | method | `scripts/check_contract_manifest.py:176` | `def check_manifest(config)` |
| `main` | method | `scripts/check_contract_manifest.py:229` | `def main(argv)` |
| `AuditConfig` | class | `scripts/devtools/command_audit.py:25` | `class AuditConfig` |
| `argparser_commands` | method | `scripts/devtools/command_audit.py:40` | `def argparser_commands(config)` |
| `audit` | method | `scripts/devtools/command_audit.py:65` | `def audit(config)` |
| `main` | method | `scripts/devtools/command_audit.py:105` | `def main(argv)` |
| `SmokeConfig` | class | `scripts/devtools/core_smoke.py:20` | `class SmokeConfig` |
| `check_calls` | method | `scripts/devtools/core_smoke.py:81` | `def check_calls()` |
| `check_surfaces` | method | `scripts/devtools/core_smoke.py:64` | `def check_surfaces(config)` |
| `main` | method | `scripts/devtools/core_smoke.py:118` | `def main()` |
| `build_sbom` | function | `scripts/generate_sbom.py:74` | `def build_sbom(with_ml)` |
| `collect_components` | function | `scripts/generate_sbom.py:37` | `def collect_components(with_ml)` |
| `main` | function | `scripts/generate_sbom.py:92` | `def main()` |
| `parse_requirement` | function | `scripts/generate_sbom.py:25` | `def parse_requirement(line)` |
| `project_version` | function | `scripts/generate_sbom.py:68` | `def project_version()` |
| `Journal` | class | `scripts/journal.py:149` | `class Journal` |
| `JournalConfig` | class | `scripts/journal.py:53` | `class JournalConfig` |
| `JournalError` | class | `scripts/journal.py:48` | `class JournalError(RuntimeError)` |
| `_build_parser` | method | `scripts/journal.py:245` | `def _build_parser()` |
| `_default_runner` | method | `scripts/journal.py:124` | `def _default_runner(args)` |
| `_git_remote_slug` | method | `scripts/journal.py:114` | `def _git_remote_slug()` |
| `_graphql` | method | `scripts/journal.py:163` | `def _graphql(self, query, variables)` |
| `_run_git` | method | `scripts/journal.py:90` | `def _run_git(args)` |
| `category_id` | method | `scripts/journal.py:192` | `def category_id(self)` |
| `entries` | method | `scripts/journal.py:223` | `def entries(self, limit)` |
| `from_git_remote` | method | `scripts/journal.py:71` | `def from_git_remote(cls, remote, category)` |
| `main` | method | `scripts/journal.py:264` | `def main(argv)` |
| `post` | method | `scripts/journal.py:206` | `def post(self, title, body)` |
| `repo_id` | method | `scripts/journal.py:184` | `def repo_id(self)` |
| `_append_methods` | function | `scripts/migrate_commandsets.py:83` | `def _append_methods(clean_path, methods)` |
| `_extract_method_source` | function | `scripts/migrate_commandsets.py:38` | `def _extract_method_source(source, method_name)` |
| `_find_class_end` | function | `scripts/migrate_commandsets.py:69` | `def _find_class_end(source_lines)` |
| `_method_names_from_file` | function | `scripts/migrate_commandsets.py:52` | `def _method_names_from_file(filepath)` |
| `main` | function | `scripts/migrate_commandsets.py:158` | `def main()` |
| `merge_phase` | function | `scripts/migrate_commandsets.py:117` | `def merge_phase(phase, dry_run)` |
| `_category_from_decorator` | function | `scripts/migrate_lazyown.py:70` | `def _category_from_decorator(decorator)` |
| `_indent_level` | function | `scripts/migrate_lazyown.py:84` | `def _indent_level(line)` |
| `build_migrated_module` | function | `scripts/migrate_lazyown.py:124` | `def build_migrated_module(phase, category, methods)` |
| `extract_method` | function | `scripts/migrate_lazyown.py:88` | `def extract_method(source, node)` |
| `main` | function | `scripts/migrate_lazyown.py:173` | `def main()` |
| `rewrite_globals` | function | `scripts/migrate_lazyown.py:96` | `def rewrite_globals(method_source)` |
| `changed_sources` | function | `scripts/mutate.sh:33` | `` |
| `runners` | function | `scripts/mutate.sh:29` | `` |
| `usage` | function | `scripts/mutate.sh:40` | `` |
| `fail` | function | `scripts/publish_wiki.sh:38` | `` |
| `log` | function | `scripts/publish_wiki.sh:37` | `` |
| `write_c2_api` | function | `scripts/publish_wiki.sh:150` | `` |
| `write_footer` | function | `scripts/publish_wiki.sh:207` | `` |
| `write_home` | function | `scripts/publish_wiki.sh:58` | `` |
| `write_installation` | function | `scripts/publish_wiki.sh:92` | `` |
| `write_plugins` | function | `scripts/publish_wiki.sh:174` | `` |
| `write_sidebar` | function | `scripts/publish_wiki.sh:188` | `` |
| `_build_parser` | function | `scripts/read_journal.py:19` | `def _build_parser()` |
| `main` | function | `scripts/read_journal.py:29` | `def main(argv)` |
| `check` | function | `scripts/smoke_onboarding.sh:8` | `` |
| `canonical_command_count` | function | `scripts/sync_doc_stats.py:87` | `def canonical_command_count(root)` |
| `main` | function | `scripts/sync_doc_stats.py:165` | `def main()` |
| `measure_stats` | function | `scripts/sync_doc_stats.py:109` | `def measure_stats(root)` |
| `project_version` | function | `scripts/sync_doc_stats.py:100` | `def project_version(root)` |
| `render` | function | `scripts/sync_doc_stats.py:136` | `def render(template, stats)` |
| `sync` | function | `scripts/sync_doc_stats.py:141` | `def sync(check, stats, root)` |
| `bdd_modules` | function | `scripts/test_bdd.sh:33` | `` |
| `changed_tests` | function | `scripts/test_bdd.sh:37` | `` |
| `check_doc_counts` | function | `scripts/top_tier_check.py:70` | `def check_doc_counts(commands, mcp, addons)` |
| `check_release_inputs` | function | `scripts/top_tier_check.py:108` | `def check_release_inputs()` |
| `check_tracked_secrets` | function | `scripts/top_tier_check.py:81` | `def check_tracked_secrets()` |
| `check_versions` | function | `scripts/top_tier_check.py:52` | `def check_versions()` |
| `count_addons` | function | `scripts/top_tier_check.py:48` | `def count_addons()` |
| `count_cli_commands` | function | `scripts/top_tier_check.py:32` | `def count_cli_commands()` |
| `count_mcp_tools` | function | `scripts/top_tier_check.py:43` | `def count_mcp_tools()` |
| `fail` | function | `scripts/top_tier_check.py:23` | `def fail(message)` |
| `main` | function | `scripts/top_tier_check.py:116` | `def main()` |
| `ok` | function | `scripts/top_tier_check.py:28` | `def ok(message)` |
| `build_technique_index` | function | `scripts/update_apt_atomic_ids.py:22` | `def build_technique_index(atomics_path)` |
| `update_playbooks` | function | `scripts/update_apt_atomic_ids.py:46` | `def update_playbooks(index, playbook_dir)` |
| `check` | function | `scripts/validate_agent_contract.sh:23` | `` |
| `ACIEngine` | class | `skills/aci_planner.py:570` | `class ACIEngine` |
| `ACIGoal` | class | `skills/aci_planner.py:126` | `class ACIGoal` |
| `ACIPlan` | class | `skills/aci_planner.py:162` | `class ACIPlan` |
| `ACIPlanner` | class | `skills/aci_planner.py:426` | `class ACIPlanner` |
| `ACIReflector` | class | `skills/aci_planner.py:764` | `class ACIReflector` |
| `AttackPhase` | class | `skills/aci_planner.py:137` | `class AttackPhase` |
| `__init__` | method | `skills/aci_planner.py:438` | `def __init__(self, api_key, objectives_file, plan_file)` |
| `__init__` | method | `skills/aci_planner.py:581` | `def __init__(self, api_key, plan_file, objectives_file, history_file, replan_threshold)` |
| `__init__` | method | `skills/aci_planner.py:774` | `def __init__(self, lessons_file)` |
| `_archive_plan` | method | `skills/aci_planner.py:239` | `def _archive_plan(plan, history_file)` |
| `_build_parser` | method | `skills/aci_planner.py:955` | `def _build_parser()` |
| `_build_phases_from_llm` | method | `skills/aci_planner.py:486` | `def _build_phases_from_llm(self, raw, goal, phase_filter)` |
| `_build_phases_static` | method | `skills/aci_planner.py:511` | `def _build_phases_static(self, goal, phase_filter)` |
| `_count_blocked` | method | `skills/aci_planner.py:750` | `def _count_blocked(self, plan)` |
| `_count_objectives_by_status` | method | `skills/aci_planner.py:266` | `def _count_objectives_by_status(obj_ids, objectives_file)` |
| `_inject_all_objectives` | method | `skills/aci_planner.py:539` | `def _inject_all_objectives(self, plan)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
