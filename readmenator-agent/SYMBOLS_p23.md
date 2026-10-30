# Symbols (page 23 of 48)
Previous: [SYMBOLS_p22.md](SYMBOLS_p22.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `WIN32_FIND_DATA` | class | `modules/win_rootkit/win_rin3_rootkit.cs:47` | `` |
| `WinRing3Rootkit` | class | `modules/win_rootkit/win_rin3_rootkit.cs:32` | `` |
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
| `_c_locale_process_env` | function | `modules/winbox_gym.py:190` | `def _c_locale_process_env()` |
| `_canonical_state` | function | `modules/winbox_gym.py:164` | `def _canonical_state(raw)` |
| `_clean_snapshot_present` | function | `modules/winbox_gym.py:508` | `def _clean_snapshot_present()` |
| `_complete_partial_build` | function | `modules/winbox_gym.py:645` | `def _complete_partial_build(notify)` |
| `_emit_notify` | function | `modules/winbox_gym.py:179` | `def _emit_notify(notifier, message)` |
| `_guest_probe_z_drive` | function | `modules/winbox_gym.py:767` | `def _guest_probe_z_drive()` |
| `_guest_probe_z_drive_retries` | function | `modules/winbox_gym.py:781` | `def _guest_probe_z_drive_retries()` |
| `_install_disk_is_substantial` | function | `modules/winbox_gym.py:537` | `def _install_disk_is_substantial()` |
| `_load_yaml` | function | `modules/winbox_gym.py:205` | `def _load_yaml(path)` |
| `_missing_prereqs` | function | `modules/winbox_gym.py:407` | `def _missing_prereqs()` |
| `_prereq_path` | function | `modules/winbox_gym.py:392` | `def _prereq_path(name)` |
| `_recover_partial_build` | function | `modules/winbox_gym.py:705` | `def _recover_partial_build(notify, build_timeout)` |
| `_repair_guest_ntfs` | function | `modules/winbox_gym.py:588` | `def _repair_guest_ntfs(notify)` |
| `_stream_command` | function | `modules/winbox_gym.py:1002` | `def _stream_command(argv)` |
| `_verify_provisioning` | function | `modules/winbox_gym.py:798` | `def _verify_provisioning(notify)` |
| `_vm_built_from` | function | `modules/winbox_gym.py:1164` | `def _vm_built_from(status)` |
| `_wait_for_shutdown` | function | `modules/winbox_gym.py:560` | `def _wait_for_shutdown(timeout, notify)` |
| `_winbox_disk_path` | function | `modules/winbox_gym.py:634` | `def _winbox_disk_path()` |
| `attack_readiness` | function | `modules/winbox_gym.py:1234` | `def attack_readiness(params)` |
| `binary_path` | function | `modules/winbox_gym.py:335` | `def binary_path()` |
| `chain_for` | function | `modules/winbox_gym.py:242` | `def chain_for(vuln_id, path)` |
| `check_readiness` | function | `modules/winbox_gym.py:412` | `def check_readiness(params)` |
| `ensure_installed` | function | `modules/winbox_gym.py:340` | `def ensure_installed(params, timeout)` |
| `ensure_lab_ready` | function | `modules/winbox_gym.py:822` | `def ensure_lab_ready(params)` |
| `ensure_prereqs` | function | `modules/winbox_gym.py:453` | `def ensure_prereqs(timeout)` |
| `ensure_vm_running` | function | `modules/winbox_gym.py:1184` | `def ensure_vm_running(timeout)` |
| `exploit_for` | function | `modules/winbox_gym.py:252` | `def exploit_for(vuln_id, path)` |
| `get` | function | `modules/winbox_gym.py:233` | `def get(vuln_id, path)` |
| `load_index` | function | `modules/winbox_gym.py:222` | `def load_index(path)` |
| `main` | function | `modules/winbox_gym.py:1262` | `def main()` |
| `record_artifact` | function | `modules/winbox_gym.py:1211` | `def record_artifact(name, output)` |
| `resolve_target` | function | `modules/winbox_gym.py:1170` | `def resolve_target()` |
| `run_cli` | function | `modules/winbox_gym.py:924` | `def run_cli(args, timeout)` |
| `summary` | function | `modules/winbox_gym.py:311` | `def summary(path)` |
| `validate_matrix` | function | `modules/winbox_gym.py:262` | `def validate_matrix(path)` |
| `vm_ip` | function | `modules/winbox_gym.py:1148` | `def vm_ip()` |
| `vm_status` | function | `modules/winbox_gym.py:1113` | `def vm_status(timeout)` |
| `vulnerabilities` | function | `modules/winbox_gym.py:227` | `def vulnerabilities(path)` |
| `list_entries` | function | `modules/workspace.py:46` | `def list_entries(rel)` |
| `make_dir` | function | `modules/workspace.py:83` | `def make_dir(rel)` |
| `read_text` | function | `modules/workspace.py:63` | `def read_text(rel, limit)` |
| `remove` | function | `modules/workspace.py:90` | `def remove(rel)` |
| `resolve` | function | `modules/workspace.py:27` | `def resolve(rel)` |
| `root` | function | `modules/workspace.py:21` | `def root()` |
| `write_text` | function | `modules/workspace.py:72` | `def write_text(rel, content)` |
| `CredentialEntry` | class | `modules/world_model.py:410` | `class CredentialEntry` |
| `DomainEntry` | class | `modules/world_model.py:436` | `class DomainEntry` |
| `EmailEntry` | class | `modules/world_model.py:428` | `class EmailEntry` |
| `EngagementPhase` | class | `modules/world_model.py:389` | `class EngagementPhase(StrEnum)` |
| `HostEntry` | class | `modules/world_model.py:586` | `class HostEntry` |
| `HostState` | class | `modules/world_model.py:373` | `class HostState(StrEnum)` |
| `NetworkGraph` | class | `modules/world_model.py:466` | `class NetworkGraph` |
| `NetworkRelation` | class | `modules/world_model.py:444` | `class NetworkRelation` |
| `ServiceInfo` | class | `modules/world_model.py:401` | `class ServiceInfo` |
| `VulnerabilityEntry` | class | `modules/world_model.py:419` | `class VulnerabilityEntry` |
| `WorldModel` | class | `modules/world_model.py:767` | `class WorldModel` |
| `_PhaseDeriver` | class | `modules/world_model.py:642` | `class _PhaseDeriver` |
| `__init__` | method | `modules/world_model.py:489` | `def __init__(self)` |
| `__init__` | method | `modules/world_model.py:775` | `def __init__(self, path)` |
| `_cred_value` | method | `modules/world_model.py:1204` | `def _cred_value(cred)` |
| `_decrypt_payload_text` | function | `modules/world_model.py:218` | `def _decrypt_payload_text(text, password, salt)` |
| `_derive_crypto_key` | function | `modules/world_model.py:76` | `def _derive_crypto_key(password, salt)` |
| `_encrypt_payload` | function | `modules/world_model.py:198` | `def _encrypt_payload(payload, password, salt)` |
| `_load` | method | `modules/world_model.py:1337` | `def _load(self)` |
| `_load_or_create_salt` | function | `modules/world_model.py:155` | `def _load_or_create_salt(salt_path)` |
| `_machine_password` | function | `modules/world_model.py:85` | `def _machine_password()` |
| `_master_password` | function | `modules/world_model.py:126` | `def _master_password()` |
| `_read_encrypted_dict` | function | `modules/world_model.py:257` | `def _read_encrypted_dict(path)` |
| `_save` | method | `modules/world_model.py:1318` | `def _save(self)` |
| `add_credential` | method | `modules/world_model.py:895` | `def add_credential(self, value, host, service)` |
| `add_domain` | method | `modules/world_model.py:990` | `def add_domain(self, domain, host, context)` |
| `add_email` | method | `modules/world_model.py:984` | `def add_email(self, address, host, context)` |
| `add_host` | method | `modules/world_model.py:791` | `def add_host(self, ip)` |
| `add_note` | method | `modules/world_model.py:851` | `def add_note(self, ip, note)` |
| `add_relation` | method | `modules/world_model.py:496` | `def add_relation(self, relation)` |
| `add_relation` | method | `modules/world_model.py:1216` | `def add_relation(self, source, target, relation, weight)` |
| `add_service` | method | `modules/world_model.py:595` | `def add_service(self, svc)` |
| `add_service` | method | `modules/world_model.py:834` | `def add_service(self, ip, port, name, version, protocol)` |
| `add_vulnerability` | method | `modules/world_model.py:978` | `def add_vulnerability(self, description, host, cve, severity)` |
| `advance` | method | `modules/world_model.py:599` | `def advance(self, new_state)` |
| `advance_host` | method | `modules/world_model.py:825` | `def advance_host(self, ip, new_state)` |
| `can_advance_to` | method | `modules/world_model.py:385` | `def can_advance_to(self, next_state)` |
| `consume_policy_facts` | method | `modules/world_model.py:1077` | `def consume_policy_facts(self, facts_path)` |
| `degree_centrality` | method | `modules/world_model.py:516` | `def degree_centrality(self)` |
| `derive` | method | `modules/world_model.py:656` | `def derive(self, hosts)` |
| `from_dict` | method | `modules/world_model.py:570` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/world_model.py:619` | `def from_dict(cls, d)` |
| `get_host` | method | `modules/world_model.py:872` | `def get_host(self, ip)` |
| `get_hosts_summary` | method | `modules/world_model.py:884` | `def get_hosts_summary(self)` |
| `get_phase` | method | `modules/world_model.py:1252` | `def get_phase(self)` |
| `get_suggested_tools` | method | `modules/world_model.py:1256` | `def get_suggested_tools(self)` |
| `get_world_model` | function | `modules/world_model.py:1455` | `def get_world_model(path)` |
| `graph_snapshot` | method | `modules/world_model.py:1245` | `def graph_snapshot(self)` |
| `in_degree` | method | `modules/world_model.py:508` | `def in_degree(self, node)` |
| `link_credential_to_failure` | method | `modules/world_model.py:948` | `def link_credential_to_failure(self, value, host)` |
| `link_credential_to_success` | method | `modules/world_model.py:927` | `def link_credential_to_success(self, value, host)` |
| `neighbors` | method | `modules/world_model.py:504` | `def neighbors(self, node)` |
| `out_degree` | method | `modules/world_model.py:512` | `def out_degree(self, node)` |
| `pivot_candidates` | method | `modules/world_model.py:531` | `def pivot_candidates(self, top_k)` |
| `pivot_candidates` | method | `modules/world_model.py:1237` | `def pivot_candidates(self, top_k)` |
| `rank` | method | `modules/world_model.py:382` | `def rank(self)` |
| `read_section` | method | `modules/world_model.py:1410` | `def read_section(self, key)` |
| `read_state_dict` | function | `modules/world_model.py:290` | `def read_state_dict(path)` |
| `reload` | method | `modules/world_model.py:1367` | `def reload(self)` |
| `remove_host` | method | `modules/world_model.py:809` | `def remove_host(self, ip)` |
| `reset` | method | `modules/world_model.py:1383` | `def reset(self)` |
| `reset_host` | method | `modules/world_model.py:799` | `def reset_host(self, ip)` |
| `set_os_hint` | method | `modules/world_model.py:858` | `def set_os_hint(self, ip, os_hint)` |
| `snapshot` | method | `modules/world_model.py:1394` | `def snapshot(self)` |
| `to_context_string` | method | `modules/world_model.py:1259` | `def to_context_string(self)` |
| `to_dict` | method | `modules/world_model.py:553` | `def to_dict(self)` |
| `to_dict` | method | `modules/world_model.py:607` | `def to_dict(self)` |
| `update_from_findings` | method | `modules/world_model.py:1004` | `def update_from_findings(self, findings)` |
| `write_section` | method | `modules/world_model.py:1427` | `def write_section(self, key, value)` |
| `write_state_dict` | function | `modules/world_model.py:325` | `def write_state_dict(path, data)` |
| `YAMLPromptGenerator` | class | `modules/yaml_generator.py:17` | `class YAMLPromptGenerator` |
| `__init__` | method | `modules/yaml_generator.py:18` | `def __init__(self, provider, api_key)` |
| `_load_model` | method | `modules/yaml_generator.py:32` | `def _load_model(self)` |
| `create_yaml_addon` | method | `modules/yaml_generator.py:109` | `def create_yaml_addon(self, user_request, output_dir)` |
| `extract_yaml_from_markdown` | method | `modules/yaml_generator.py:100` | `def extract_yaml_from_markdown(self, text)` |
| `generate_prompt` | method | `modules/yaml_generator.py:54` | `def generate_prompt(self, user_request)` |
| `load_payload` | method | `modules/yaml_generator.py:25` | `def load_payload(self)` |
| `main` | function | `modules/yaml_generator.py:141` | `def main()` |
| `YaraScanner` | class | `modules/yara_scanner.py:23` | `class YaraScanner` |
| `__init__` | method | `modules/yara_scanner.py:31` | `def __init__(self, rules_dir, auto_compile)` |
| `_format_match` | method | `modules/yara_scanner.py:162` | `def _format_match(self, match)` |
| `_load_external_vars` | method | `modules/yara_scanner.py:45` | `def _load_external_vars(self)` |
| `_scan_with_timeout` | method | `modules/yara_scanner.py:129` | `def _scan_with_timeout(self, filepath, externals, timeout)` |
| `_sha256` | method | `modules/yara_scanner.py:250` | `def _sha256(filepath)` |
| `add_rule` | method | `modules/yara_scanner.py:258` | `def add_rule(self, name, content)` |
| `compile_all` | method | `modules/yara_scanner.py:54` | `def compile_all(self)` |
| `create_default_rules` | function | `modules/yara_scanner.py:371` | `def create_default_rules()` |
| `download_community_rules` | method | `modules/yara_scanner.py:300` | `def download_community_rules(self)` |
| `ensure_directory` | method | `modules/yara_scanner.py:41` | `def ensure_directory(self)` |
| `ioc_scan` | method | `modules/yara_scanner.py:328` | `def ioc_scan(self, target_path, iocs)` |
| `list_rules` | method | `modules/yara_scanner.py:277` | `def list_rules(self)` |
| `scan_directory` | method | `modules/yara_scanner.py:187` | `def scan_directory(self, directory, recursive, extensions, max_files)` |
| `scan_file` | method | `modules/yara_scanner.py:98` | `def scan_file(self, filepath, timeout)` |
| `target` | function | `modules/yara_scanner.py:137` | `def target()` |
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
| `_init_backend` | function | `poc_tui/app.py:429` | `def _init_backend()` |
| `_log` | method | `poc_tui/app.py:255` | `def _log(self)` |
| `_on_backend_ready` | method | `poc_tui/app.py:444` | `def _on_backend_ready(self)` |
| `_show_result` | method | `poc_tui/app.py:525` | `def _show_result(self, result)` |
| `_tab_complete` | method | `poc_tui/app.py:605` | `def _tab_complete(self, inp)` |
| `_work` | function | `poc_tui/app.py:510` | `def _work()` |
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
| `main` | function | `poc_tui/app.py:629` | `def main()` |
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
| `PluginLoader` | class | `poc_tui/plugin_loader.py:84` | `class PluginLoader` |
| `PluginSpec` | class | `poc_tui/plugin_loader.py:29` | `class PluginSpec` |
| `_LuaAppProxy` | class | `poc_tui/plugin_loader.py:291` | `class _LuaAppProxy` |
| `__init__` | method | `poc_tui/plugin_loader.py:91` | `def __init__(self, config, base_dir)` |
| `__init__` | method | `poc_tui/plugin_loader.py:294` | `def __init__(self, config)` |
| `_list_files` | method | `poc_tui/plugin_loader.py:131` | `def _list_files(self, directory)` |
| `_load_lua_plugins` | method | `poc_tui/plugin_loader.py:223` | `def _load_lua_plugins(self)` |
| `_load_tool_files` | method | `poc_tui/plugin_loader.py:248` | `def _load_tool_files(self)` |
| `_load_yaml_addons` | method | `poc_tui/plugin_loader.py:148` | `def _load_yaml_addons(self)` |
| `_lua_register` | method | `poc_tui/plugin_loader.py:114` | `def _lua_register(self, name, func)` |
| `_register_tool` | method | `poc_tui/plugin_loader.py:261` | `def _register_tool(self, data)` |
| `_register_yaml_addon` | method | `poc_tui/plugin_loader.py:161` | `def _register_yaml_addon(self, data)` |
| `_replace_placeholders` | function | `poc_tui/plugin_loader.py:41` | `def _replace_placeholders(command, params)` |
| `_setup_lua` | method | `poc_tui/plugin_loader.py:105` | `def _setup_lua(self)` |
| `_subst` | function | `poc_tui/plugin_loader.py:52` | `def _subst(match)` |
| `_validate_clone_url` | function | `poc_tui/plugin_loader.py:62` | `def _validate_clone_url(url)` |
| `load_all` | method | `poc_tui/plugin_loader.py:139` | `def load_all(self)` |
| `one_cmd` | method | `poc_tui/plugin_loader.py:301` | `def one_cmd(self, cmd)` |
| `params` | method | `poc_tui/plugin_loader.py:298` | `def params(self)` |
| `wrapper` | function | `poc_tui/plugin_loader.py:117` | `def wrapper(arg)` |
| `wrapper` | function | `poc_tui/plugin_loader.py:172` | `def wrapper(arg)` |
| `wrapper` | function | `poc_tui/plugin_loader.py:269` | `def wrapper(arg)` |
| `main` | function | `poc_tui/run.py:9` | `def main()` |
| `TestLazyOwnTUIApp` | class | `poc_tui/test_app.py:100` | `class TestLazyOwnTUIApp` |
| `TestShellBackend` | class | `poc_tui/test_app.py:32` | `class TestShellBackend` |
| `_make_backend` | function | `poc_tui/test_app.py:26` | `def _make_backend()` |
| `_run_async` | function | `poc_tui/test_app.py:17` | `def _run_async(coro)` |
| `_t` | function | `poc_tui/test_app.py:106` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:115` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:126` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:136` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:152` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:165` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:182` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:198` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:210` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:225` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:235` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:248` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:270` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:291` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:307` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:321` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:342` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:361` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:374` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:399` | `def _t()` |
| `_t` | function | `poc_tui/test_app.py:414` | `def _t()` |
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
| `_build_substitutions` | function | `pwntomate.py:113` | `def _build_substitutions(host_addr, port, toolname_value, basedir_value, tunnel)` |
| `_fix_sessions_owner` | function | `pwntomate.py:143` | `def _fix_sessions_owner()` |
| `_run_tool` | function | `pwntomate.py:203` | `def _run_tool(cmd)` |
| `build_command_map` | function | `readmeneitor.py:104` | `def build_command_map(index_data)` |
| `convert_to_html` | function | `readmeneitor.py:343` | `def convert_to_html(md_path, html_path)` |
| `extract_docstrings_from_dir` | function | `readmeneitor.py:161` | `def extract_docstrings_from_dir(dirpath)` |
| `extract_docstrings_from_file` | function | `readmeneitor.py:132` | `def extract_docstrings_from_file(filepath)` |
| `extract_functions_from_file` | function | `readmeneitor.py:209` | `def extract_functions_from_file(filepath)` |
| `group_commands_by_phase` | function | `readmeneitor.py:187` | `def group_commands_by_phase(cmd_map)` |
| `load_command_index` | function | `readmeneitor.py:83` | `def load_command_index(index_path)` |
| `main` | function | `readmeneitor.py:379` | `def main()` |
| `normalize_trailing_newline` | function | `readmeneitor.py:74` | `def normalize_trailing_newline(output_path)` |
| `write_commands_md` | function | `readmeneitor.py:276` | `def write_commands_md(cmd_map, docstrings, groups, output_path)` |
| `write_utils_md` | function | `readmeneitor.py:241` | `def write_utils_md(functions, output_path)` |
| `banner` | function | `run_topoexploit_agent.sh:29` | `` |
| `start_api` | function | `run_topoexploit_agent.sh:38` | `` |
| `MigrationError` | class | `scripts/activate_migrations.py:28` | `class MigrationError(Exception)` |
| `activate_migrated_file` | function | `scripts/activate_migrations.py:75` | `def activate_migrated_file(migrated_path, dry_run)` |
| `extract_command_names` | function | `scripts/activate_migrations.py:42` | `def extract_command_names(migrated_path)` |
| `find_in_lazyown` | function | `scripts/activate_migrations.py:52` | `def find_in_lazyown(command_names)` |
| `find_migrated_sets` | function | `scripts/activate_migrations.py:32` | `def find_migrated_sets()` |
| `main` | function | `scripts/activate_migrations.py:88` | `def main()` |
| `remove_from_lazyown` | function | `scripts/activate_migrations.py:62` | `def remove_from_lazyown(locations, dry_run)` |
| `classify_os` | function | `scripts/backfill_addon_os_trigger.py:104` | `def classify_os(filename)` |
| `known_trigger` | function | `scripts/backfill_addon_os_trigger.py:121` | `def known_trigger(name)` |
| `main` | function | `scripts/backfill_addon_os_trigger.py:175` | `def main()` |
| `patch` | function | `scripts/backfill_addon_os_trigger.py:141` | `def patch(path)` |
| `render_trigger` | function | `scripts/backfill_addon_os_trigger.py:127` | `def render_trigger(trigger)` |
| `apply_interface` | function | `scripts/broadcom_wps_drive.sh:166` | `` |
| `detect_interface` | function | `scripts/broadcom_wps_drive.sh:151` | `` |
| `die` | function | `scripts/broadcom_wps_drive.sh:55` | `` |
| `do_doctor` | function | `scripts/broadcom_wps_drive.sh:348` | `` |
| `do_monitor` | function | `scripts/broadcom_wps_drive.sh:235` | `` |
| `do_status` | function | `scripts/broadcom_wps_drive.sh:325` | `` |
| `do_unmonitor` | function | `scripts/broadcom_wps_drive.sh:247` | `` |
| `elevate` | function | `scripts/broadcom_wps_drive.sh:200` | `` |
| `ensure_monitor_mode` | function | `scripts/broadcom_wps_drive.sh:259` | `` |
| `has_scapy` | function | `scripts/broadcom_wps_drive.sh:231` | `` |
| `have_sudo` | function | `scripts/broadcom_wps_drive.sh:194` | `` |
| `interface_mode` | function | `scripts/broadcom_wps_drive.sh:210` | `` |
| `interface_up` | function | `scripts/broadcom_wps_drive.sh:216` | `` |
| `is_root` | function | `scripts/broadcom_wps_drive.sh:190` | `` |
| `is_wireless` | function | `scripts/broadcom_wps_drive.sh:162` | `` |
| `log` | function | `scripts/broadcom_wps_drive.sh:53` | `` |
| `main` | function | `scripts/broadcom_wps_drive.sh:404` | `` |
| `parse_flags` | function | `scripts/broadcom_wps_drive.sh:81` | `` |
| `payload_value` | function | `scripts/broadcom_wps_drive.sh:61` | `` |
| `python_bin` | function | `scripts/broadcom_wps_drive.sh:227` | `` |
| `resolve_interface` | function | `scripts/broadcom_wps_drive.sh:170` | `` |
| `run_fingerprint` | function | `scripts/broadcom_wps_drive.sh:268` | `` |
| `run_yara` | function | `scripts/broadcom_wps_drive.sh:308` | `` |
| `usage` | function | `scripts/broadcom_wps_drive.sh:57` | `` |
| `warn` | function | `scripts/broadcom_wps_drive.sh:54` | `` |
| `ManifestConfig` | class | `scripts/check_contract_manifest.py:34` | `class ManifestConfig` |
| `__post_init__` | method | `scripts/check_contract_manifest.py:53` | `def __post_init__(self)` |
| `_collect_doc_imports` | function | `scripts/check_contract_manifest.py:163` | `def _collect_doc_imports(text)` |
| `_dotted_symbol_exists` | function | `scripts/check_contract_manifest.py:112` | `def _dotted_symbol_exists(token, config)` |
| `_extract_dotted_tokens` | function | `scripts/check_contract_manifest.py:209` | `def _extract_dotted_tokens(text, config)` |
| `_extract_path_tokens` | function | `scripts/check_contract_manifest.py:138` | `def _extract_path_tokens(text, config)` |
| `_iter_table_cells` | function | `scripts/check_contract_manifest.py:127` | `def _iter_table_cells(text)` |
| `_module_path` | function | `scripts/check_contract_manifest.py:100` | `def _module_path(module, config)` |
| `_resolve` | method | `scripts/check_contract_manifest.py:58` | `def _resolve(self, path)` |
| `_resolve_reference` | function | `scripts/check_contract_manifest.py:154` | `def _resolve_reference(token, config)` |
| `_top_level_names` | function | `scripts/check_contract_manifest.py:72` | `def _top_level_names(path)` |
| `check_manifest` | function | `scripts/check_contract_manifest.py:176` | `def check_manifest(config)` |
| `main` | function | `scripts/check_contract_manifest.py:229` | `def main(argv)` |
| `AuditConfig` | class | `scripts/devtools/command_audit.py:25` | `class AuditConfig` |
| `argparser_commands` | function | `scripts/devtools/command_audit.py:40` | `def argparser_commands(config)` |
| `audit` | function | `scripts/devtools/command_audit.py:65` | `def audit(config)` |
| `main` | function | `scripts/devtools/command_audit.py:105` | `def main(argv)` |
| `SmokeConfig` | class | `scripts/devtools/core_smoke.py:20` | `class SmokeConfig` |
| `check_calls` | function | `scripts/devtools/core_smoke.py:81` | `def check_calls()` |
| `check_surfaces` | function | `scripts/devtools/core_smoke.py:64` | `def check_surfaces(config)` |
| `main` | function | `scripts/devtools/core_smoke.py:118` | `def main()` |
| `compile_activity` | function | `scripts/dirtyinit_drive.sh:255` | `` |
| `die` | function | `scripts/dirtyinit_drive.sh:67` | `` |
| `do_auto` | function | `scripts/dirtyinit_drive.sh:382` | `` |
| `do_build` | function | `scripts/dirtyinit_drive.sh:265` | `` |
| `do_doctor` | function | `scripts/dirtyinit_drive.sh:468` | `` |
| `do_extract` | function | `scripts/dirtyinit_drive.sh:393` | `` |
| `do_help` | function | `scripts/dirtyinit_drive.sh:525` | `` |
| `do_install` | function | `scripts/dirtyinit_drive.sh:329` | `` |
| `do_launch` | function | `scripts/dirtyinit_drive.sh:340` | `` |
| `do_logs` | function | `scripts/dirtyinit_drive.sh:418` | `` |
| `do_run` | function | `scripts/dirtyinit_drive.sh:412` | `` |
| `do_stage` | function | `scripts/dirtyinit_drive.sh:402` | `` |
| `do_status` | function | `scripts/dirtyinit_drive.sh:423` | `` |
| `find_android_jar` | function | `scripts/dirtyinit_drive.sh:173` | `` |
| `find_build_tools` | function | `scripts/dirtyinit_drive.sh:166` | `` |
| `find_java_tool` | function | `scripts/dirtyinit_drive.sh:201` | `` |
| `find_ndk` | function | `scripts/dirtyinit_drive.sh:152` | `` |
| `find_ndk_clang` | function | `scripts/dirtyinit_drive.sh:185` | `` |
| `find_sdk` | function | `scripts/dirtyinit_drive.sh:141` | `` |
| `log` | function | `scripts/dirtyinit_drive.sh:65` | `` |
| `main` | function | `scripts/dirtyinit_drive.sh:529` | `` |
| `pack_apk` | function | `scripts/dirtyinit_drive.sh:211` | `` |
| `parse_flags` | function | `scripts/dirtyinit_drive.sh:89` | `` |
| `payload_value` | function | `scripts/dirtyinit_drive.sh:69` | `` |
| `require_adb` | function | `scripts/dirtyinit_drive.sh:130` | `` |
| `require_device` | function | `scripts/dirtyinit_drive.sh:134` | `` |
| `tap_button` | function | `scripts/dirtyinit_drive.sh:348` | `` |
| `warn` | function | `scripts/dirtyinit_drive.sh:66` | `` |
| `build_sbom` | function | `scripts/generate_sbom.py:74` | `def build_sbom(with_ml)` |
| `collect_components` | function | `scripts/generate_sbom.py:37` | `def collect_components(with_ml)` |
| `main` | function | `scripts/generate_sbom.py:92` | `def main()` |
| `parse_requirement` | function | `scripts/generate_sbom.py:25` | `def parse_requirement(line)` |
| `project_version` | function | `scripts/generate_sbom.py:68` | `def project_version()` |
| `Journal` | class | `scripts/journal.py:149` | `class Journal` |
| `JournalConfig` | class | `scripts/journal.py:53` | `class JournalConfig` |
| `JournalError` | class | `scripts/journal.py:48` | `class JournalError(RuntimeError)` |
| `_build_parser` | function | `scripts/journal.py:245` | `def _build_parser()` |
| `_default_runner` | function | `scripts/journal.py:124` | `def _default_runner(args)` |
| `_git_remote_slug` | function | `scripts/journal.py:114` | `def _git_remote_slug()` |
| `_graphql` | method | `scripts/journal.py:163` | `def _graphql(self, query, variables)` |
| `_run_git` | function | `scripts/journal.py:90` | `def _run_git(args)` |
| `category_id` | method | `scripts/journal.py:192` | `def category_id(self)` |
| `entries` | method | `scripts/journal.py:223` | `def entries(self, limit)` |
| `from_git_remote` | method | `scripts/journal.py:71` | `def from_git_remote(cls, remote, category)` |
| `main` | function | `scripts/journal.py:264` | `def main(argv)` |
| `post` | method | `scripts/journal.py:206` | `def post(self, title, body)` |
| `repo_id` | method | `scripts/journal.py:184` | `def repo_id(self)` |
| `healthy` | function | `scripts/lazy_llamacpp_serve.sh:33` | `` |
| `ask` | function | `scripts/lazy_llamacpp_setup.sh:40` | `` |
| `_backup` | function | `scripts/lazy_opencode_config.py:29` | `def _backup(path)` |
| `_hermes_path` | function | `scripts/lazy_opencode_config.py:41` | `def _hermes_path()` |
| `_opencode_path` | function | `scripts/lazy_opencode_config.py:36` | `def _opencode_path()` |
| `main` | function | `scripts/lazy_opencode_config.py:150` | `def main(argv)` |
| `patch_hermes` | function | `scripts/lazy_opencode_config.py:93` | `def patch_hermes(host)` |
| `patch_opencode` | function | `scripts/lazy_opencode_config.py:46` | `def patch_opencode(set_default, host)` |
| `_LoopSettings` | class | `scripts/mcp_call.py:52` | `class _LoopSettings` |
| `_ToolAnswer` | class | `scripts/mcp_call.py:43` | `class _ToolAnswer` |
| `__init__` | method | `scripts/mcp_call.py:46` | `def __init__(self, text, is_error)` |
| `_build_parser` | function | `scripts/mcp_call.py:152` | `def _build_parser()` |
| `_call_once` | function | `scripts/mcp_call.py:116` | `def _call_once(settings, command)` |

Next: [SYMBOLS_p24.md](SYMBOLS_p24.md)
