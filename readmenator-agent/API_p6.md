# API (page 6 of 24)
Previous: [API_p5.md](API_p5.md)

## contrib/legacy/lazyhttpreverseshell.py
Depends on: `modules/backdoor/server.c`
- `encrypt` (function) `contrib/legacy/lazyhttpreverseshell.py:14` `def encrypt(data)`
- `decrypt` (function) `contrib/legacy/lazyhttpreverseshell.py:17` `def decrypt(data)`
- `compress` (function) `contrib/legacy/lazyhttpreverseshell.py:20` `def compress(data)`
- `decompress` (function) `contrib/legacy/lazyhttpreverseshell.py:23` `def decompress(data)`
- `reverse_http_shell_client` (function) `contrib/legacy/lazyhttpreverseshell.py:26` `def reverse_http_shell_client(lhost, rhost, rport)`
- `reverse_http_shell_server` (function) `contrib/legacy/lazyhttpreverseshell.py:50` `def reverse_http_shell_server(lhost, lport)`
- `RequestHandler.do_GET` (method) `contrib/legacy/lazyhttpreverseshell.py:52` `def do_GET(self)`
- `RequestHandler.do_POST` (method) `contrib/legacy/lazyhttpreverseshell.py:65` `def do_POST(self)`
- `parse_arguments` (function) `contrib/legacy/lazyhttpreverseshell.py:88` `def parse_arguments(args)`

## contrib/legacy/lazykeygen.py
- `pad` (function) `contrib/legacy/lazykeygen.py:8` `def pad(s)`
- `encrypt` (function) `contrib/legacy/lazykeygen.py:11` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazykeygen.py:17` `def decrypt(ciphertext, key)`
- `generate_key` (function) `contrib/legacy/lazykeygen.py:23` `def generate_key(length)`
- `main` (function) `contrib/legacy/lazykeygen.py:26` `def main()`

## contrib/legacy/lazylfi2rce.py
- `signal_handler` (function) `contrib/legacy/lazylfi2rce.py:29` `def signal_handler(sig, frame)`
- `check_lfi_success` (function) `contrib/legacy/lazylfi2rce.py:35` `def check_lfi_success(response_text)`
- `check_rfi_success` (function) `contrib/legacy/lazylfi2rce.py:39` `def check_rfi_success(response_text)`
- `main` (function) `contrib/legacy/lazylfi2rce.py:43` `def main()`

## contrib/legacy/lazyllmchat.py
Depends on: `modules/ai_model.py`, `modules/llm_factory.py`
- `LazyOwnShellBridge.__init__` (method) `contrib/legacy/lazyllmchat.py:25` `def __init__(self, script_path)`
- `no_history_init` (function) `contrib/legacy/lazyllmchat.py:38` `def no_history_init(self_)`
- `LazyOwnShellBridge.execute` (method) `contrib/legacy/lazyllmchat.py:65` `def execute(self, command)`
- `target` (function) `contrib/legacy/lazyllmchat.py:70` `def target()`
- `SessionContextProvider.__init__` (method) `contrib/legacy/lazyllmchat.py:105` `def __init__(self, session_path)`
- `SessionContextProvider.get_last_lines` (method) `contrib/legacy/lazyllmchat.py:108` `def get_last_lines(self, count)`
- `PromptBuilder.for_command_analysis` (method) `contrib/legacy/lazyllmchat.py:133` `def for_command_analysis(command, output, context, history)`
- `PromptBuilder.for_direct_query` (method) `contrib/legacy/lazyllmchat.py:149` `def for_direct_query(query, context, history)`
- `LLMEngine.__init__` (method) `contrib/legacy/lazyllmchat.py:164` `def __init__(self)`
- `LLMEngine.is_ready` (method) `contrib/legacy/lazyllmchat.py:179` `def is_ready(self)`
- `LLMEngine.ask` (method) `contrib/legacy/lazyllmchat.py:182` `def ask(self, prompt)`
- `LLMEngine.get_history_text` (method) `contrib/legacy/lazyllmchat.py:194` `def get_history_text(self)`
- `LazyOwnPromptRenderer.render` (method) `contrib/legacy/lazyllmchat.py:208` `def render(self)`
- `LazyOwnPromptRenderer.banner` (method) `contrib/legacy/lazyllmchat.py:223` `def banner(self)`
- `LazyOwnLLMChat.__init__` (method) `contrib/legacy/lazyllmchat.py:235` `def __init__(self)`
- `LazyOwnLLMChat.run` (method) `contrib/legacy/lazyllmchat.py:280` `def run(self, initial_query)`
- `main` (function) `contrib/legacy/lazyllmchat.py:309` `def main()`

## contrib/legacy/lazylogpoisoning.py
Depends on: `modules/lazyencoder_decoder.py`
- `ensure_http_prefix` (function) `contrib/legacy/lazylogpoisoning.py:39` `def ensure_http_prefix(url)`
- `signal_handler` (function) `contrib/legacy/lazylogpoisoning.py:45` `def signal_handler(sig, frame)`
- `main` (function) `contrib/legacy/lazylogpoisoning.py:53` `def main()`

## contrib/legacy/lazymariadb_rce_cve_2016-662.py
- `info` (function) `contrib/legacy/lazymariadb_rce_cve_2016-662.py:59` `def info(str)`
- `errmsg` (function) `contrib/legacy/lazymariadb_rce_cve_2016-662.py:63` `def errmsg(str)`
- `shutdown` (function) `contrib/legacy/lazymariadb_rce_cve_2016-662.py:67` `def shutdown(code)`

## contrib/legacy/lazymidm.py
- `get_mac` (function) `contrib/legacy/lazymidm.py:12` `def get_mac(ip)`
- `spoof` (function) `contrib/legacy/lazymidm.py:18` `def spoof(target_ip, spoof_ip)`
- `restore` (function) `contrib/legacy/lazymidm.py:27` `def restore(target_ip, spoof_ip)`
- `mitm` (function) `contrib/legacy/lazymidm.py:37` `def mitm(target_ip, gateway_ip)`
- `start_sslstrip` (function) `contrib/legacy/lazymidm.py:50` `def start_sslstrip(port)`
- `start_tcpdump` (function) `contrib/legacy/lazymidm.py:54` `def start_tcpdump(interface, output_file)`
- `setup_monitor_mode` (function) `contrib/legacy/lazymidm.py:58` `def setup_monitor_mode(interface)`
- `main` (function) `contrib/legacy/lazymidm.py:68` `def main()`

## contrib/legacy/lazymitmap.py
- `print_header` (function) `contrib/legacy/lazymitmap.py:45` `def print_header()`
- `run_cmd_write` (function) `contrib/legacy/lazymitmap.py:49` `def run_cmd_write(cmd_args, s)` -- Write a file using sudo.
- `write_file` (function) `contrib/legacy/lazymitmap.py:63` `def write_file(path, s)`
- `append_file` (function) `contrib/legacy/lazymitmap.py:67` `def append_file(path, s)` -- Append to the file, don't overwrite.
- `create_dir` (function) `contrib/legacy/lazymitmap.py:72` `def create_dir(directory)` -- Create directory with sudo if it does not exist.
- `set_permissions` (function) `contrib/legacy/lazymitmap.py:77` `def set_permissions(directory, permissions)` -- Set directory permissions with sudo.
- `install_dependencies` (function) `contrib/legacy/lazymitmap.py:84` `def install_dependencies()` -- Install required dependencies.
- `backup_file` (function) `contrib/legacy/lazymitmap.py:121` `def backup_file(filepath)` -- Backup a given file.
- `restore_file` (function) `contrib/legacy/lazymitmap.py:128` `def restore_file(filepath)` -- Restore a backed-up file.
- `restart_service` (function) `contrib/legacy/lazymitmap.py:138` `def restart_service(service)` -- Restart a given service.
- `flush_iptables` (function) `contrib/legacy/lazymitmap.py:145` `def flush_iptables()` -- Flush iptables rules.
- `setup_network_manager` (function) `contrib/legacy/lazymitmap.py:153` `def setup_network_manager(ap_iface)` -- Setup NetworkManager configuration for the AP interface.
- `configure_dnsmasq` (function) `contrib/legacy/lazymitmap.py:163` `def configure_dnsmasq(ap_iface, ap_ip_range_start, ap_ip_range_end, ap_ip_gateway, dns_ip_1, dns_ip_2, sslstrip)` -- Configure dnsmasq based on SSLSTRIP usage.
- `configure_hostapd` (function) `contrib/legacy/lazymitmap.py:195` `def configure_hostapd(ap_iface, ssid, channel, wpa_passphrase)` -- Configure hostapd based on user input.
- `setup_iptables` (function) `contrib/legacy/lazymitmap.py:228` `def setup_iptables(ap_iface, ap_ip, net_iface)` -- Setup iptables rules.
- `set_speed_limit` (function) `contrib/legacy/lazymitmap.py:248` `def set_speed_limit(ap_iface, speed_up, speed_down)` -- Set speed limit for the clients.
- `start_services` (function) `contrib/legacy/lazymitmap.py:254` `def start_services(ap_iface, script_path, sslstrip, wireshark, driftnet, tshark)` -- Start necessary services based on user input.
- `cleanup` (function) `contrib/legacy/lazymitmap.py:315` `def cleanup()` -- Cleanup actions to restore system state.
- `signal_handler` (function) `contrib/legacy/lazymitmap.py:324` `def signal_handler(sig, frame)`

## contrib/legacy/lazynetbios.py
- `check_sudo` (function) `contrib/legacy/lazynetbios.py:30` `def check_sudo()`
- `signal_handler` (function) `contrib/legacy/lazynetbios.py:38` `def signal_handler(sig, frame)`
- `scan_netbios` (function) `contrib/legacy/lazynetbios.py:45` `def scan_netbios(ip_range)`
- `check_arp` (function) `contrib/legacy/lazynetbios.py:58` `def check_arp(ip)`
- `check_netbios` (function) `contrib/legacy/lazynetbios.py:71` `def check_netbios(ip)`
- `send_nbns_spoof` (function) `contrib/legacy/lazynetbios.py:90` `def send_nbns_spoof(target_ip, target_name, spoof_ip, trans_id)`
- `generate_ip_range` (function) `contrib/legacy/lazynetbios.py:115` `def generate_ip_range(start_ip, end_ip)`

## contrib/legacy/lazyntlrelayx.py
- `parse_hash_file` (function) `contrib/legacy/lazyntlrelayx.py:5` `def parse_hash_file(file_path)`
- `ntlm_relay` (function) `contrib/legacy/lazyntlrelayx.py:52` `def ntlm_relay(target_ip, credentials)`

## contrib/legacy/lazyopenssh77enum2.py
Depends on: `core/logging.py`
- `add_boolean` (function) `contrib/legacy/lazyopenssh77enum2.py:19` `def add_boolean()`
- `service_accept` (function) `contrib/legacy/lazyopenssh77enum2.py:30` `def service_accept()`
- `invalid_username` (function) `contrib/legacy/lazyopenssh77enum2.py:36` `def invalid_username()`
- `check_user` (function) `contrib/legacy/lazyopenssh77enum2.py:50` `def check_user(username)`

## contrib/legacy/lazyphishingai.py
Depends on: `core/logging.py`
Imported by: `modules/llm_adapter.py`
- `clean_think` (function) `contrib/legacy/lazyphishingai.py:28` `def clean_think(texto)`
- `clean_yaml` (function) `contrib/legacy/lazyphishingai.py:31` `def clean_yaml(texto)`
- `truncate_message` (function) `contrib/legacy/lazyphishingai.py:37` `def truncate_message(message, max_chars)`
- `configure_logging` (function) `contrib/legacy/lazyphishingai.py:42` `def configure_logging(debug)`
- `create_complex_prompt` (function) `contrib/legacy/lazyphishingai.py:46` `def create_complex_prompt(base_prompt, history, knowledge_base)`
- `load_knowledge_base` (function) `contrib/legacy/lazyphishingai.py:101` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazyphishingai.py:110` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazyphishingai.py:117` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazyphishingai.py:122` `def get_relevant_knowledge(prompt)`
- `process_prompt_local_yaml` (function) `contrib/legacy/lazyphishingai.py:132` `def process_prompt_local_yaml(prompt, debug, mode, output_file)`
- `generate` (function) `contrib/legacy/lazyphishingai.py:155` `def generate()`
- `parse_args` (function) `contrib/legacy/lazyphishingai.py:192` `def parse_args()`

## contrib/legacy/lazyproxy.py
Depends on: `modules/colors.py`
- `check_sudo` (function) `contrib/legacy/lazyproxy.py:40` `def check_sudo()`
- `signal_handler` (function) `contrib/legacy/lazyproxy.py:47` `def signal_handler(sig, frame)`
- `hexdump` (function) `contrib/legacy/lazyproxy.py:52` `def hexdump(src, length)`
- `receive_from` (function) `contrib/legacy/lazyproxy.py:63` `def receive_from(connection)`
- `request_handler` (function) `contrib/legacy/lazyproxy.py:77` `def request_handler(buffer)`
- `response_handler` (function) `contrib/legacy/lazyproxy.py:82` `def response_handler(buffer)`
- `get_ip_from_url` (function) `contrib/legacy/lazyproxy.py:87` `def get_ip_from_url(url)`
- `handle_request` (function) `contrib/legacy/lazyproxy.py:104` `def handle_request(client_socket, address)`
- `start_proxy` (function) `contrib/legacy/lazyproxy.py:183` `def start_proxy()`

## contrib/legacy/lazypwn.py
Depends on: `cli/commands/pwn.py`
- `BinaryFinder.__init__` (method) `contrib/legacy/lazypwn.py:25` `def __init__(self)`
- `BinaryFinder.find_suid_binaries` (method) `contrib/legacy/lazypwn.py:28` `def find_suid_binaries(self)`
- `BinaryFinder.find_capabilities_binaries` (method) `contrib/legacy/lazypwn.py:36` `def find_capabilities_binaries(self)`
- `BinaryFinder.find_executable_binaries` (method) `contrib/legacy/lazypwn.py:44` `def find_executable_binaries(self)`
- `BinaryFinder.find_specific_name_binaries` (method) `contrib/legacy/lazypwn.py:52` `def find_specific_name_binaries(self, names)`
- `BinaryFinder.process_output` (method) `contrib/legacy/lazypwn.py:61` `def process_output(self, output)`
- `BinaryFinder.get_found_binaries` (method) `contrib/legacy/lazypwn.py:67` `def get_found_binaries(self)`
- `BinaryAttacker.__init__` (method) `contrib/legacy/lazypwn.py:71` `def __init__(self, binary_path)`
- `BinaryAttacker.analyze_with_ltrace` (method) `contrib/legacy/lazypwn.py:76` `def analyze_with_ltrace(self)`
- `BinaryAttacker.extract_strings` (method) `contrib/legacy/lazypwn.py:83` `def extract_strings(self)`
- `BinaryAttacker.prepare_attack` (method) `contrib/legacy/lazypwn.py:90` `def prepare_attack(self)`
- `BinaryAttacker.exploit_with_pwntools` (method) `contrib/legacy/lazypwn.py:170` `def exploit_with_pwntools(self)`
- `main` (function) `contrib/legacy/lazypwn.py:181` `def main()`

## contrib/legacy/lazypwnkit.py
- `rmrf` (function) `contrib/legacy/lazypwnkit.py:8` `def rmrf(path)` -- Elimina recursivamente un directorio y su contenido.
- `create_exploit_environment` (function) `contrib/legacy/lazypwnkit.py:13` `def create_exploit_environment()` -- Crea el entorno necesario para el exploit.
- `cleanup_exploit_environment` (function) `contrib/legacy/lazypwnkit.py:31` `def cleanup_exploit_environment()` -- Limpia el entorno creado para el exploit.
- `execute_exploit` (function) `contrib/legacy/lazypwnkit.py:37` `def execute_exploit(cmd)` -- Ejecuta el exploit.
- `main` (function) `contrib/legacy/lazypwnkit.py:79` `def main()`

## contrib/legacy/lazyreversentlmv2.py
Depends on: `modules/lazyencoder_decoder.py`
- `parse_hash_file` (function) `contrib/legacy/lazyreversentlmv2.py:11` `def parse_hash_file(file_path)`
- `reverse_shell` (function) `contrib/legacy/lazyreversentlmv2.py:58` `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, callback_port)`

## contrib/legacy/lazysearch.py
- `highlight_term` (function) `contrib/legacy/lazysearch.py:29` `def highlight_term(text, term)`
- `search_in_parquet` (function) `contrib/legacy/lazysearch.py:32` `def search_in_parquet(term, parquet_files)`
- `main` (function) `contrib/legacy/lazysearch.py:44` `def main()`

## contrib/legacy/lazysearch_bot.py
Depends on: `core/logging.py`
- `signal_handler` (function) `contrib/legacy/lazysearch_bot.py:59` `def signal_handler(sig, frame)`
- `show_help` (function) `contrib/legacy/lazysearch_bot.py:65` `def show_help(message)`
- `check_api_key` (function) `contrib/legacy/lazysearch_bot.py:69` `def check_api_key()`
- `configure_logging` (function) `contrib/legacy/lazysearch_bot.py:75` `def configure_logging(debug)`
- `parse_args` (function) `contrib/legacy/lazysearch_bot.py:79` `def parse_args()`
- `create_complex_prompt` (function) `contrib/legacy/lazysearch_bot.py:86` `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function) `contrib/legacy/lazysearch_bot.py:109` `def execute_command(command)`
- `load_knowledge_base` (function) `contrib/legacy/lazysearch_bot.py:112` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazysearch_bot.py:118` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazysearch_bot.py:122` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazysearch_bot.py:127` `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function) `contrib/legacy/lazysearch_bot.py:135` `def transform_knowledge_base(client)`
- `main` (function) `contrib/legacy/lazysearch_bot.py:158` `def main()`

## contrib/legacy/lazyseo.py
Depends on: `modules/colors.py`
- `Config.__init__` (method) `contrib/legacy/lazyseo.py:15` `def __init__(self, config_dict)`
- `load_payload` (function) `contrib/legacy/lazyseo.py:23` `def load_payload()`
- `make_request` (function) `contrib/legacy/lazyseo.py:28` `def make_request(url, retries, timeout)`
- `results` (function) `contrib/legacy/lazyseo.py:49` `def results(file)`
- `crawl` (function) `contrib/legacy/lazyseo.py:57` `def crawl(url)`
- `ffuf` (function) `contrib/legacy/lazyseo.py:66` `def ffuf()`
- `analyze_seo` (function) `contrib/legacy/lazyseo.py:76` `def analyze_seo(url)`

## contrib/legacy/lazysmbrelay.py
Depends on: `core/logging.py`, `utils.py`
- `check_sudo` (function) `contrib/legacy/lazysmbrelay.py:15` `def check_sudo()`
- `start_smb_server` (function) `contrib/legacy/lazysmbrelay.py:27` `def start_smb_server()`
- `start_smb_relay` (function) `contrib/legacy/lazysmbrelay.py:35` `def start_smb_relay(target, command)`
- `CustomSMBRelayServer.__init__` (method) `contrib/legacy/lazysmbrelay.py:42` `def __init__(self)`
- `CustomSMBRelayServer.handleData` (method) `contrib/legacy/lazysmbrelay.py:46` `def handleData(self)`
- `CustomSMBRelayServer.execute_remote_command` (method) `contrib/legacy/lazysmbrelay.py:50` `def execute_remote_command(self)`

## contrib/legacy/lazysniff.py
- `check_sudo` (function) `contrib/legacy/lazysniff.py:41` `def check_sudo()`
- `signal_handler` (function) `contrib/legacy/lazysniff.py:50` `def signal_handler(sig, frame)`
- `setup_curses` (function) `contrib/legacy/lazysniff.py:57` `def setup_curses()`
- `restore_curses` (function) `contrib/legacy/lazysniff.py:66` `def restore_curses(stdscr)`
- `show_banner` (function) `contrib/legacy/lazysniff.py:73` `def show_banner(stdscr, banner)`
- `process_packet` (function) `contrib/legacy/lazysniff.py:80` `def process_packet(packet, packets, win_top, win_bottom)`
- `analyze_packet` (function) `contrib/legacy/lazysniff.py:90` `def analyze_packet(packet)`
- `capture_packets` (function) `contrib/legacy/lazysniff.py:112` `def capture_packets(interface, count, filter, pcap_file, packets, win_top, win_bottom)`
- `main_curses` (function) `contrib/legacy/lazysniff.py:118` `def main_curses(stdscr, packets, interface, count, filter, pcap_file)`
- `parse_arguments` (function) `contrib/legacy/lazysniff.py:188` `def parse_arguments()`
- `main` (function) `contrib/legacy/lazysniff.py:197` `def main()`

## contrib/legacy/lazysqli.py
- `send_payload` (function) `contrib/legacy/lazysqli.py:13` `def send_payload(payload, url, s, sql_time)`
- `sqli_dichotomie` (function) `contrib/legacy/lazysqli.py:30` `def sqli_dichotomie(payload_brute, offset, url, s, sql_time)`
- `sqli_thread` (function) `contrib/legacy/lazysqli.py:51` `def sqli_thread(url, db, table, col, sql_time, threads)`
- `main` (function) `contrib/legacy/lazysqli.py:89` `def main(args)`

## contrib/legacy/lazyssh.py
Depends on: `core/logging.py`
- `execute` (function) `contrib/legacy/lazyssh.py:13` `def execute(hostname, port, command)`

## contrib/legacy/lazyvsftp.py
Depends on: `cli/commands/pwn.py`
- `connect` (function) `contrib/legacy/lazyvsftp.py:7` `def connect(host, port)`
- `exploit` (function) `contrib/legacy/lazyvsftp.py:16` `def exploit(host, port)`
- `handle_backdoor` (function) `contrib/legacy/lazyvsftp.py:61` `def handle_backdoor(s)`

## contrib/legacy/sql.py
Depends on: `cli/commands/pwn.py`
- `def_handler` (function) `contrib/legacy/sql.py:8` `def def_handler(sig, frame)`
- `getUnicode` (function) `contrib/legacy/sql.py:15` `def getUnicode(sqli)`
- `makeRequest` (function) `contrib/legacy/sql.py:22` `def makeRequest(sqli_modified)`

## core/api_authz.py
Imported by: `lazyc2/app_factory.py`, `lazyc2/blueprints/api.py`, `tests/test_api_authz.py`, `tests/test_api_v1.py`, `tests/test_orchestrator_api.py`
- `ApiKey.to_dict` (method) `core/api_authz.py:94` `def to_dict(self)`
- `ApiKey.from_dict` (method) `core/api_authz.py:107` `def from_dict(cls, data)`
- `ApiKey.is_expired` (method) `core/api_authz.py:119` `def is_expired(self)`
- `ApiKey.is_retired` (method) `core/api_authz.py:124` `def is_retired(self)`
- `ApiKey.has_permission` (method) `core/api_authz.py:127` `def has_permission(self, permission)`
- `ApiKey.has_all_permissions` (method) `core/api_authz.py:130` `def has_all_permissions(self, permissions)`
- `ApiKeyStore.__init__` (method) `core/api_authz.py:170` `def __init__(self, config)`
- `ApiKeyStore.config` (method) `core/api_authz.py:176` `def config(self)` -- The configuration this store was built with.
- `ApiKeyStore.list_keys` (method) `core/api_authz.py:217` `def list_keys(self, tenant_id)` -- List all active keys, optionally filtered by *tenant_id*.
- `ApiKeyStore.find_by_hash` (method) `core/api_authz.py:229` `def find_by_hash(self, key_hash)` -- Look up a key record by its SHA-256 hash.
- `ApiKeyStore.create_key` (method) `core/api_authz.py:238` `def create_key(self, tenant_id, label, permissions, expires_in_days)` -- Create a new API key and return ``(ApiKey, plaintext_secret)``.
- `ApiKeyStore.revoke_key` (method) `core/api_authz.py:273` `def revoke_key(self, label, tenant_id)` -- Revoke every key with *label* within *tenant_id*.
- `ApiKeyStore.validate_key` (method) `core/api_authz.py:287` `def validate_key(self, plaintext)` -- Validate a plaintext API key and return the ApiKey record.
- `ApiKeyStore.rotate_key` (method) `core/api_authz.py:309` `def rotate_key(self, label, tenant_id)` -- Rotate an existing key by label.
- `require_api_auth` (function) `core/api_authz.py:365` `def require_api_auth(store, permissions, require_tenant)` -- Flask-route decorator that enforces API-key + tenant authorization.
- `decorator` (function) `core/api_authz.py:405` `def decorator(f)`
- `decorated` (function) `core/api_authz.py:407` `def decorated()`
- `create_api_token` (function) `core/api_authz.py:440` `def create_api_token(store, tenant_id, label, permissions, expires_in_days)` -- Create an API key and return the one-time plaintext token.

## core/autonomous.py
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/mcp_bridge.py`, `lazyown.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`
- `is_autonomous` (function) `core/autonomous.py:21` `def is_autonomous()` -- Return True while an autonomous loop run owns the process.
- `autonomous_mode` (function) `core/autonomous.py:27` `def autonomous_mode()` -- Suppress interactive prompts for the duration of a loop run.

## core/command_bridge.py
Depends on: `lazyown.py`
Imported by: `tests/test_core_command_bridge.py`
- `CommandBridge.__init__` (method) `core/command_bridge.py:18` `def __init__(self)`
- `CommandBridge.ready` (method) `core/command_bridge.py:25` `def ready(self)` -- Whether the bridge has been successfully initialized.
- `CommandBridge.error` (method) `core/command_bridge.py:30` `def error(self)` -- Error message if initialization failed, or None.
- `CommandBridge.onecmd` (method) `core/command_bridge.py:65` `def onecmd(self, command)` -- Execute a LazyOwn internal command via the shell.
- `CommandBridge.one_cmd` (method) `core/command_bridge.py:89` `def one_cmd(self, command)` -- Execute a command using the shell's one_cmd method.
- `CommandBridge.execute` (method) `core/command_bridge.py:110` `def execute(self, command)` -- Alias for one_cmd.
- `get_bridge` (function) `core/command_bridge.py:126` `def get_bridge()` -- Get or create the singleton CommandBridge instance.

## core/config.py
Depends on: `core/logging.py`, `core/payload_schema.py`
Imported by: `cli/aliases.py`, `cli/commands/bof_registry.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/defaults.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/params_ops.py`, `cli/commands/persist_migrated.py`, `cli/commands/purple_team.py`, `cli/commands/recon_migrated.py`, `cli/commands/security.py`, `cli/commands/session_ops.py`, `cli/commands/ux.py`, `cli/engagement_hooks.py`, `cli/orchestrator_assets_tabs.py`, `core/__init__.py`, `core/credential_vault.py`, `core/hardening.py`, `core/prompt.py`, `lazyc2/blueprints/api.py`, `lazyown.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/c2_profile_engine.py`, `modules/cli_auth.py`, `modules/config_store.py`, `modules/db.py`, `modules/harness.py`, `modules/lazy_agent.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_installer.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/reactive_engine.py`, `modules/redteam_gym.py`, `skills/lazyown_mcp.py`, `tests/test_aes_key_propagation.py`, `tests/test_cli_assign.py`, `tests/test_cli_command_sets.py`, `tests/test_core.py`, `tests/test_core_config.py`, `tests/test_guardrails.py`, `tests/test_improvements_spec.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_runner.py`, `tests/test_loop_supervision.py`, `tests/test_orchestrator_yaml.py`, `utils.py`
- `Config.__init__` (method) `core/config.py:219` `def __init__(self, config_dict, sessions_dir)`
- `Config.as_params` (method) `core/config.py:234` `def as_params(self)` -- Return a shallow copy of the underlying parameter dictionary.
- `Config.overridden_keys` (method) `core/config.py:244` `def overridden_keys(self)` -- Return sorted list of keys that were overridden via ``LAZYOWN_*`` env vars.
- `resolve_aes_key` (function) `core/config.py:261` `def resolve_aes_key(config_dict)` -- Return a 32-byte AES key derived from config, disk, or randomness.
- `load_payload` (function) `core/config.py:327` `def load_payload(path)` -- Load and return the JSON payload at ``path``.
- `load_and_validate` (function) `core/config.py:345` `def load_and_validate(path)` -- Load ``payload.json``, validate against the schema, and return a result dict.
- `save_payload` (function) `core/config.py:396` `def save_payload(payload, path)` -- Atomically write ``payload`` as pretty-printed JSON to ``path``.

## core/console.py
Imported by: `cli/command_explorer.py`, `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/orchestration.py`, `cli/commands/recon.py`, `cli/commands/security.py`, `cli/commands/ux.py`, `cli/config_status.py`, `cli/contextual_help.py`, `cli/doctor.py`, `cli/exploit_advisor.py`, `cli/exploration_view.py`, `cli/protips.py`, `cli/reactive_hints.py`, `cli/session_resumer.py`, `cli/splash.py`, `cli/surface_tui.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `cli/tutorial.py`, `cli/wizard.py`, `contrib/legacy/lazybinenc.py`, `core/__init__.py`, `core/error_advice.py`, `core/http.py`, `core/network.py`, `core/process.py`, `core/safe_console.py`, `core/validators.py`, `key.py`, `lazy_sentinel4.py`, `lazyown.py`, `modules/apt_playbooks.py`, `modules/atomic_cli.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/lilsplunky.py`, `modules/privesc_predictor.py`, `modules/rich_tui.py`, `tests/test_console_stdio.py`, `tests/test_core.py`, `tests/test_exploration_and_addons.py`, `tests/test_lazy_parity.py`, `tests/test_loop_progress.py`, `tests/test_scope_guard_integration.py`, `tests/test_session_brief.py`, `tests/test_toast_bus.py`, `tests/test_tui_splash.py`, `tests/test_tui_style.py`, `tests/test_tui_themes.py`, `utils.py`
- `colors_enabled` (function) `core/console.py:98` `def colors_enabled()` -- Return False when NO_COLOR or ANSI_COLORS_DISABLED is set.
- `format_line` (function) `core/console.py:121` `def format_line(prefix, message, glyph)` -- Build a single log line with standard prefix and sanitized message.
- `print_error` (function) `core/console.py:137` `def print_error(error)` -- Print a red error message to stdout (never raises on broken pipes).
- `print_msg` (function) `core/console.py:143` `def print_msg(msg)` -- Print a green informational message to stdout (never raises).
- `print_warn` (function) `core/console.py:149` `def print_warn(warn)` -- Print a magenta/yellow warning message to stdout (never raises).
- `print_succ` (function) `core/console.py:155` `def print_succ(msg)` -- Print a bright green success message to stdout (never raises).
- `ensure_blocking_stdio` (function) `core/console.py:161` `def ensure_blocking_stdio()` -- Restore blocking mode on stdio fds inherited as non-blocking.
- `write_stdout` (function) `core/console.py:180` `def write_stdout(text)` -- Write ``text`` to stdout, tolerating non-blocking or broken pipes.

## core/credential_vault.py
Depends on: `core/config.py`, `core/crypto.py`, `core/logging.py`
Imported by: `cli/commands/security.py`, `core/hardening.py`, `lazyown.py`, `tests/test_credential_vault.py`
- `check_dangerous_defaults` (function) `core/credential_vault.py:63` `def check_dangerous_defaults(payload)` -- Scan payload for unchanged default credential values.
- `seal_value` (function) `core/credential_vault.py:93` `def seal_value(plaintext, key)` -- Encrypt a single credential value.
- `unseal_value` (function) `core/credential_vault.py:112` `def unseal_value(sealed, key)` -- Decrypt a sealed credential value.
- `seal_payload` (function) `core/credential_vault.py:141` `def seal_payload(payload, key)` -- Return a copy of ``payload`` with all sensitive values encrypted.
- `unseal_payload` (function) `core/credential_vault.py:164` `def unseal_payload(payload, key)` -- Return a copy of ``payload`` with all sealed values decrypted.
- `rotate_aes_key` (function) `core/credential_vault.py:186` `def rotate_aes_key(payload, current_key)` -- Generate a new AES key, re-encrypt all sealed values under it.
- `generate_secure_defaults` (function) `core/credential_vault.py:215` `def generate_secure_defaults()` -- Generate cryptographically random default values for sensitive keys.

## core/crypto.py
Imported by: `cli/auto_crypto.py`, `cli/commands/exfiltration.py`, `core/__init__.py`, `core/credential_vault.py`, `modules/db.py`, `modules/lazy_loop.py`, `modules/phishing_orchestrator.py`, `modules/rootkit/rootkit.c`, `tests/test_core.py`, `utils.py`
- `generate_salt` (function) `core/crypto.py:24` `def generate_salt(length)` -- Generate a cryptographically random salt.
- `derive_key` (function) `core/crypto.py:36` `def derive_key(password, salt)` -- Derive a Fernet-compatible key from a password using PBKDF2HMAC.
- `xor_encrypt_decrypt` (function) `core/crypto.py:67` `def xor_encrypt_decrypt(data, key)` -- Return ``bytearray`` produced by XOR-ing each byte of ``data`` with ``key``.
- `generate_xor_key` (function) `core/crypto.py:83` `def generate_xor_key(length)` -- Generate a random XOR key of the given length as a hex string.
- `AESencrypt` (function) `core/crypto.py:98` `def AESencrypt(plaintext, key)` -- Encrypt ``plaintext`` with AES-256-GCM using a random nonce.
- `AESdecrypt` (function) `core/crypto.py:123` `def AESdecrypt(data, key)` -- Decrypt data produced by ``AESencrypt``.
- `dropFile` (function) `core/crypto.py:154` `def dropFile(key, ciphertext)` -- Write AES key and ciphertext to ``sessions/cipher.bin`` and ``sessions/key.bin``.

## core/defaults.py
Imported by: `cli/commands/cred_migrated.py`, `cli/commands/defaults.py`, `lazyc2/blueprints/api.py`, `lazyown.py`, `modules/autonomous_exploit_engine.py`, `modules/hash_cracker.py`, `tests/test_security_codeql_batch.py`
- `load_defaults` (function) `core/defaults.py:21` `def load_defaults(path)` -- Load and cache the defaults document.
- `clear_cache` (function) `core/defaults.py:44` `def clear_cache()` -- Drop cached documents (tests only).
- `get` (function) `core/defaults.py:49` `def get(section, key, default)` -- Return ``defaults[section][key]`` or ``default`` when absent.
- `default_lport` (function) `core/defaults.py:63` `def default_lport()` -- Return the fallback listener port as an int.
- `default_rport` (function) `core/defaults.py:72` `def default_rport()` -- Return the fallback remote port as an int.
- `rockyou_wordlist` (function) `core/defaults.py:81` `def rockyou_wordlist()` -- Return the default wordlist path.
- `common_wordlists` (function) `core/defaults.py:90` `def common_wordlists()` -- Return the ordered wordlist fallback candidates.
- `sessions_dir` (function) `core/defaults.py:100` `def sessions_dir()` -- Return the sessions directory path.

## core/dependencies.py
Imported by: `core/__init__.py`, `tests/test_dependencies.py`, `utils.py`
- `MissingDependencyError.__init__` (method) `core/dependencies.py:45` `def __init__(self, import_name, pip_package, feature)` -- Build a remediation-oriented error message.
- `_DeferredImport.__init__` (method) `core/dependencies.py:115` `def __init__(self, spec)` -- Store the dependency spec used to build remediation errors.
- `_DeferredImport.__call__` (method) `core/dependencies.py:136` `def __call__(self)` -- Reject calling a missing dependency.
- `optional_import` (function) `core/dependencies.py:183` `def optional_import(import_name)` -- Import an optional module, returning a deferred proxy when absent.
- `optional_attr` (function) `core/dependencies.py:209` `def optional_attr(import_name, attr)` -- Import an attribute from an optional module, deferring failure.
- `DependencyReport.missing` (method) `core/dependencies.py:278` `def missing(self)` -- Return the optional Python dependencies that are not installed.
- `DependencyReport.ok` (method) `core/dependencies.py:283` `def ok(self)` -- Return ``True`` when every declared dependency is present.
- `probe_python_dependency` (function) `core/dependencies.py:288` `def probe_python_dependency(spec)` -- Probe a single Python dependency by importing it.
- `collect_dependency_report` (function) `core/dependencies.py:312` `def collect_dependency_report()` -- Probe every declared optional Python dependency.
- `format_report` (function) `core/dependencies.py:323` `def format_report(report)` -- Render a :class:`DependencyReport` as an aligned, human-readable block.
- `main` (function) `core/dependencies.py:368` `def main()` -- Print the optional-dependency report and return a process exit code.

## core/error_advice.py
Depends on: `core/console.py`
- `ErrorAdvice.docs_url` (method) `core/error_advice.py:35` `def docs_url(self, config)` -- Return absolute documentation URL for this advice.
- `get_advice` (function) `core/error_advice.py:74` `def get_advice(key)` -- Return advice for key or None when unknown.
- `render_advice` (function) `core/error_advice.py:86` `def render_advice(key, config)` -- Render advice as four plain lines with explicit level tags.

## core/errors.py
Depends on: `cli/commands/enum.py`
Imported by: `core/__init__.py`
- `LazyOwnError.__init__` (method) `core/errors.py:61` `def __init__(self, message, error_code)`
- `LazyOwnError.to_dict` (method) `core/errors.py:66` `def to_dict(self)` -- Return a serialisable dict with code, type, and message.
- `ConfigError.__init__` (method) `core/errors.py:81` `def __init__(self, message, error_code)`
- `TargetError.__init__` (method) `core/errors.py:88` `def __init__(self, message, error_code)`
- `AuthError.__init__` (method) `core/errors.py:95` `def __init__(self, message, error_code)`
- `ToolError.__init__` (method) `core/errors.py:102` `def __init__(self, message, error_code)`
- `PayloadError.__init__` (method) `core/errors.py:109` `def __init__(self, message, error_code)`
- `DatabaseError.__init__` (method) `core/errors.py:116` `def __init__(self, message, error_code)`
- `NetworkError.__init__` (method) `core/errors.py:123` `def __init__(self, message, error_code)`
- `PermissionError.__init__` (method) `core/errors.py:130` `def __init__(self, message, error_code)`
- `ValidationError.__init__` (method) `core/errors.py:137` `def __init__(self, message, error_code)`

## core/executor.py
Depends on: `core/logging.py`
Imported by: `tests/test_core_executor.py`
- `safe_run` (function) `core/executor.py:96` `def safe_run(command)`
- `safe_run` (function) `core/executor.py:98` `def safe_run(command)`
- `safe_run` (function) `core/executor.py:101` `def safe_run(command)` -- Execute a command with logging and timeout.
- `run_shell` (function) `core/executor.py:149` `def run_shell(cmd)` -- Execute a shell command and return its stdout.

## core/hardening.py
Depends on: `core/config.py`, `core/credential_vault.py`, `core/host_policy.py`, `core/logging.py`
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/exfiltration.py`, `cli/commands/lateral_migrated.py`, `cli/commands/nethelpers.py`, `cli/commands/persist_migrated.py`, `cli/commands/pivoting.py`, `core/process.py`, `core/reverse_shell_secret.py`, `core/safe_subprocess.py`, `lazyc2.py`, `lazyown.py`, `modules/atomic_cli.py`, `modules/domain_dominance.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_runner.py`, `modules/phishing_orchestrator.py`, `modules/websocket_beacon.py`, `modules/world_model.py`, `scripts/devtools/core_smoke.py`, `skills/claude_md_orchestrator/validators.py`, `skills/lazyown_mcp.py`, `tests/test_host_policy.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_hardening_v3.py`, `tests/test_shell_semantics.py`
- `reject_option_injection` (function) `core/hardening.py:85` `def reject_option_injection(argv)` -- Reject argument-injection payloads in argv.
- `escape_powershell_single_quoted` (function) `core/hardening.py:104` `def escape_powershell_single_quoted(value)` -- Escape a value for embedding in a PowerShell single-quoted string.
- `terminal_env` (function) `core/hardening.py:129` `def terminal_env(base)` -- Return a child environment that keeps ANSI colors on a pipe.
- `safe_subprocess_run` (function) `core/hardening.py:150` `def safe_subprocess_run(argv)` -- Execute a command via subprocess without shell interpretation.
- `safe_clipboard_copy` (function) `core/hardening.py:195` `def safe_clipboard_copy(content)` -- Copy content to system clipboard without shell interpretation.
- `build_sshpass_command` (function) `core/hardening.py:234` `def build_sshpass_command(password, ssh_args)` -- Build an sshpass command using SSHPASS env var (sshpass -e).
- `set_sshpass_env` (function) `core/hardening.py:263` `def set_sshpass_env(password)` -- Create an environment dict with SSHPASS set for sshpass -e.
- `escape_html_content` (function) `core/hardening.py:282` `def escape_html_content(value)` -- Escape HTML special characters to prevent XSS.
- `safe_path_join` (function) `core/hardening.py:294` `def safe_path_join(base_dir, user_path)` -- Join base_dir and user_path safely, preventing path traversal.
- `validate_network_cidr` (function) `core/hardening.py:320` `def validate_network_cidr(cidr)` -- Validate a network CIDR notation string.
- `validate_port_spec` (function) `core/hardening.py:332` `def validate_port_spec(ports)` -- Validate a port specification string.
- `validate_host` (function) `core/hardening.py:348` `def validate_host(host)` -- Validate a hostname or IP address.
- `require_encryption_key` (function) `core/hardening.py:368` `def require_encryption_key(env_key, secret_file)` -- Require a proper encryption key; never fall back to a static default.
- `defused_xml_parse` (function) `core/hardening.py:396` `def defused_xml_parse(source)` -- Parse XML safely using defusedxml.
- `sanitize_filename` (function) `core/hardening.py:418` `def sanitize_filename(filename, max_length)` -- Sanitize a filename by removing dangerous characters.
- `tls_secure_context` (function) `core/hardening.py:438` `def tls_secure_context(extra_ca)` -- Build a verifying client TLS context with a TLS 1.2 floor.
- `tls_lab_unverified_allowed` (function) `core/hardening.py:463` `def tls_lab_unverified_allowed(host)` -- Return True only when unverified lab TLS is explicitly opted in.
- `tls_lab_fallback_context` (function) `core/hardening.py:490` `def tls_lab_fallback_context()` -- Build the gated unverified context for lab self-signed hosts.
- `validate_upstream_path` (function) `core/hardening.py:512` `def validate_upstream_path(path)` -- Validate an origin-form upstream path without regular expressions.
- `is_safe_path_segment` (function) `core/hardening.py:541` `def is_safe_path_segment(segment)` -- Validate one path segment with a linear charset scan (no regex).
- `is_safe_dir_path` (function) `core/hardening.py:562` `def is_safe_dir_path(raw)` -- Validate a relative directory path with linear scans (no regex).
- `is_safe_yaml_name` (function) `core/hardening.py:588` `def is_safe_yaml_name(name)` -- Validate a YAML filename with linear scans (no regex).
- `safe_join_under` (function) `core/hardening.py:607` `def safe_join_under(base_dir, user_path)` -- Join and resolve ``user_path`` under ``base_dir`` (symlink-safe).
- `safe_open_under` (function) `core/hardening.py:636` `def safe_open_under(base_dir, user_path, mode)` -- Open a file under ``base_dir`` after traversal validation.
- `store_secret_owner_only` (function) `core/hardening.py:663` `def store_secret_owner_only(path, text)` -- Atomically store a secret owner-only (0600, dir 0700).
- `contains_emoji` (function) `core/hardening.py:706` `def contains_emoji(text)` -- Return True when ``text`` carries any emoji codepoint.
- `iter_emoji_spans` (function) `core/hardening.py:721` `def iter_emoji_spans(text)` -- Return ``(offset, char)`` for every emoji char in ``text``.
- `seal_secret` (function) `core/hardening.py:754` `def seal_secret(plaintext)` -- Seal a secret with Fernet (AES-128-CBC + HMAC) for storage.
- `unseal_secret` (function) `core/hardening.py:785` `def unseal_secret(stored)` -- Reveal a secret stored by :func:`seal_secret` (legacy-compatible).
- `redact_text` (function) `core/hardening.py:826` `def redact_text(text)` -- Mask credential-like patterns before persistence or display.

## core/host_policy.py
Imported by: `core/hardening.py`, `core/validators.py`, `tests/test_host_policy.py`
- `rejects_shell_meta` (function) `core/host_policy.py:20` `def rejects_shell_meta(value)` -- Return True when value contains characters usable for shell injection.
- `is_valid_cidr` (function) `core/host_policy.py:32` `def is_valid_cidr(value)` -- Check value is a valid CIDR block.
- `is_valid_host` (function) `core/host_policy.py:48` `def is_valid_host(value)` -- Check value is a plain IP, CIDR, or hostname without shell metacharacters.

## core/http.py
Depends on: `core/console.py`
Imported by: `core/__init__.py`
- `generate_http_req` (function) `core/http.py:18` `def generate_http_req(host, port, uri, custom_header, cmd)` -- Build and send an HTTP GET request.
- `get_banner` (function) `core/http.py:50` `def get_banner(host, port)` -- Fetch a banner by connecting via HTTP to the given host and port.
- `get_command` (function) `core/http.py:69` `def get_command(url, lhost)` -- Fetch a command payload from a remote URL.
- `send_command` (function) `core/http.py:87` `def send_command(cmd, url, lhost)` -- Send a command via HTTP POST.
- `exploitalert` (function) `core/http.py:106` `def exploitalert(content)` -- Parse ExploitAlert search results HTML.
- `packetstormsecurity` (function) `core/http.py:125` `def packetstormsecurity(content)` -- Parse Packet Storm Security search results HTML.
- `nvddb` (function) `core/http.py:143` `def nvddb(content)` -- Parse NVD JSON vulnerability feed.
- `scrape_news` (function) `core/http.py:174` `def scrape_news()` -- Scrape Hacker News top stories.
- `display_news` (function) `core/http.py:198` `def display_news(titles, links, scores)` -- Display scraped news in the console.
- `inject_payloads` (function) `core/http.py:211` `def inject_payloads(urls, payload_url, request_timeout)` -- Attempt to inject a payload URL into a list of target URLs.

## core/llm_budget.py
Imported by: `cli/commands/ai.py`, `modules/llm_factory.py`, `skills/lazyown_mcp.py`, `tests/test_llm_budget.py`
- `LLMBackendLike.generate` (method) `core/llm_budget.py:61` `def generate(self, prompt)`
- `LLMBackendLike.stream_generate` (method) `core/llm_budget.py:63` `def stream_generate(self, prompt)`
- `LLMBackendLike.complete` (method) `core/llm_budget.py:65` `def complete(self, system, user, max_tokens, temperature)`
- `ModelPrice.from_mapping` (method) `core/llm_budget.py:81` `def from_mapping(cls, data)` -- Build a ModelPrice from a JSON friendly mapping.
- `BudgetLedger.record` (method) `core/llm_budget.py:232` `def record(self, entry)` -- Append a charge to the ledger and persist the new state.
- `BudgetLedger.spent_today` (method) `core/llm_budget.py:251` `def spent_today(self)` -- Return the dollar amount the ledger charged for the current day.
- `BudgetLedger.calls_today` (method) `core/llm_budget.py:256` `def calls_today(self)` -- Return the number of calls the ledger recorded for the current day.
- `BudgetLedger.reset` (method) `core/llm_budget.py:261` `def reset(self)` -- Clear the ledger for the current day and persist the empty state.
- `TokenEstimator.__init__` (method) `core/llm_budget.py:278` `def __init__(self, encoding_name)`
- `TokenEstimator.count` (method) `core/llm_budget.py:292` `def count(self, text)` -- Return the number of tokens the input text contains.
- `BudgetGuard.__init__` (method) `core/llm_budget.py:319` `def __init__(self, config, estimator, ledger)`
- `BudgetGuard.price_for` (method) `core/llm_budget.py:329` `def price_for(self, model)` -- Return the price the guard applies to a model identifier.
- `BudgetGuard.estimate_cost` (method) `core/llm_budget.py:343` `def estimate_cost(self, model, input_tokens, output_tokens)` -- Return the dollar cost the guard would charge for a call.
- `BudgetGuard.estimate_and_check` (method) `core/llm_budget.py:356` `def estimate_and_check(self, prompt, model, output_tokens)` -- Check the budget and record a charge when the call fits.
- `BudgetedBackend.__init__` (method) `core/llm_budget.py:417` `def __init__(self, inner, guard, model)`
- `BudgetedBackend.generate` (method) `core/llm_budget.py:422` `def generate(self, prompt)` -- Forward a non streaming call and record a charge.
- `BudgetedBackend.stream_generate` (method) `core/llm_budget.py:430` `def stream_generate(self, prompt)` -- Forward a streaming call.
- `BudgetedBackend.complete` (method) `core/llm_budget.py:435` `def complete(self, system, user, max_tokens, temperature)` -- Forward a role aware call.
- `default_model_prices` (function) `core/llm_budget.py:442` `def default_model_prices()` -- Return the default price table the guard ships with.
- `default_sessions_dir` (function) `core/llm_budget.py:461` `def default_sessions_dir()` -- Return the directory the ledger writes to by default.
- `load_budget_config` (function) `core/llm_budget.py:552` `def load_budget_config(payload, sessions_dir)` -- Build a BudgetConfig from a payload mapping.
- `read_budget_status` (function) `core/llm_budget.py:585` `def read_budget_status(payload, sessions_dir)` -- Return a structured snapshot of the current budget.
- `format_budget_status` (function) `core/llm_budget.py:616` `def format_budget_status(config, ledger)` -- Render the budget status as a human readable block.
- `wrap_backend_with_budget` (function) `core/llm_budget.py:657` `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` -- Wrap a concrete backend with a budgeted proxy.

## core/logging.py
Imported by: `cli/auto_crypto.py`, `cli/chain_mode.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/session_resumer.py`, `cli/tips_engine.py`, `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyhoneypot.py`, `contrib/legacy/lazyopenssh77enum2.py`, `contrib/legacy/lazyphishingai.py`, `contrib/legacy/lazysearch_bot.py`, `contrib/legacy/lazysmbrelay.py`, `contrib/legacy/lazyssh.py`, `core/config.py`, `core/credential_vault.py`, `core/executor.py`, `core/hardening.py`, `core/param_registry.py`, `core/safe_exec.py`, `core/scheduler.py`, `core/security.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/extensions/storage.py`, `lazygui/app.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/settings.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazyown.py`, `modules/addon_updater.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/atomic_cli.py`, `modules/atomic_enricher.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/beacon_recon.py`, `modules/bof_registry.py`, `modules/c2_agent.py`, `modules/c2_profile.py`, `modules/c2_profile_engine.py`, `modules/c2_surfaces.py`, `modules/chain_distill.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/collab_bp.py`, `modules/command_executor.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/config_store.py`, `modules/credential_reuse.py`, `modules/ctf_capture.py`, `modules/cve_matcher.py`, `modules/db.py`, `modules/detection_feed.py`, `modules/detection_oracle.py`, `modules/emulation_runner.py`, `modules/engagement_hooks.py`, `modules/estorides_importer.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/factsio.py`, `modules/golden_path.py`, `modules/gym_matrix_runner.py`, `modules/gym_registry.py`, `modules/harness.py`, `modules/hash_cracker.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/integrations/misp_export.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/integrations/searchsploit.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_rbac.py`, `modules/lazyownerweb.py`, `modules/lesson_ingestor.py`, `modules/lilsplunky.py`, `modules/llm_adapter.py`, `modules/llm_client.py`, `modules/logging_config.py`, `modules/mcp_agent_bridge.py`, `modules/metasploitable_gym.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/moe_router.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/session_rag.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/state_manager.py`, `modules/sudo_tiocsti.py`, `modules/threat_model.py`, `modules/toposwarm_bridge.py`, `modules/trigger_policy.py`, `modules/ttp_coverage.py`, `modules/ttpscope_bridge.py`, `modules/unified_bridge.py`, `modules/unified_dashboard.py`, `modules/verb_catalog.py`, `modules/verb_manifest.py`, `modules/vulnbot.py`, `modules/world_model.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`, `tests/test_security_codeql_batch.py`, `tests/test_structured_logging.py`
- `_JsonLineFormatter.__init__` (method) `core/logging.py:74` `def __init__(self, redacted_fields)`
- `_JsonLineFormatter.format` (method) `core/logging.py:78` `def format(self, record)`
- `_ConsoleFormatter.format` (method) `core/logging.py:132` `def format(self, record)`
- `StructuredLogger.makeRecord` (method) `core/logging.py:148` `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)`
- `get_logger` (function) `core/logging.py:231` `def get_logger(name)` -- Return a cached :class:`StructuredLogger` for *name*.
- `install_json_handler` (function) `core/logging.py:251` `def install_json_handler(name, config)` -- Install a JSON-lines file handler on *name*, preserving existing handlers.
- `reconfigure` (function) `core/logging.py:300` `def reconfigure(config)` -- Replace the cached configuration globally.

## core/network.py
Depends on: `core/console.py`
Imported by: `core/__init__.py`
- `parse_ip_mac` (function) `core/network.py:18` `def parse_ip_mac(input_string)` -- Extract IP and MAC from a formatted string.
- `create_arp_packet` (function) `core/network.py:33` `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` -- Build a raw ARP request/reply packet.
- `send_packet` (function) `core/network.py:66` `def send_packet(packet, iface)` -- Send a raw packet on a given network interface.
- `parse_proc_net_file` (function) `core/network.py:78` `def parse_proc_net_file(file_path)` -- Parse a ``/proc/net/*`` file and extract (ip, port) pairs.
- `get_open_ports` (function) `core/network.py:105` `def get_open_ports()` -- Discover listening TCP ports from ``/proc/net/tcp`` and ``tcp6``.
- `is_port_in_use` (function) `core/network.py:120` `def is_port_in_use(port, host)` -- Check whether a TCP port is already bound.
- `get_banner` (function) `core/network.py:134` `def get_banner(ip, port)` -- Grab a TCP banner from the given host and port.
- `get_network_info` (function) `core/network.py:154` `def get_network_info()` -- Collect local network information.

## core/param_registry.py
Depends on: `core/logging.py`, `core/payload_schema.py`
Imported by: `cli/commands/params_ops.py`, `cli/lazy_orchestrator.py`, `core/payload_schema.py`, `lazyc2/addon_creator.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_orchestrator.py`, `tests/test_param_registry.py`, `tests/test_php2shell_addon.py`
- `OperatorParam.as_entry` (method) `core/param_registry.py:133` `def as_entry(self)` -- Return the YAML mapping stored in ``params/operator.yaml``.
- `OperatorParam.to_spec` (method) `core/param_registry.py:142` `def to_spec(self)` -- Return the payload schema spec for this parameter.
- `registry_path` (function) `core/param_registry.py:158` `def registry_path(root)` -- Return the operator registry file path.
- `normalise_kind` (function) `core/param_registry.py:172` `def normalise_kind(kind)` -- Return the canonical kind name for a user-supplied kind.
- `effective_value` (function) `core/param_registry.py:187` `def effective_value(entry)` -- Return the value a parameter contributes to the shell params.
- `load_entries` (function) `core/param_registry.py:226` `def load_entries(root)` -- Return every operator-declared parameter.
- `list_params` (function) `core/param_registry.py:256` `def list_params(root, include_builtin, keyword)` -- Return the parameters visible to the operator.
- `create_param` (function) `core/param_registry.py:291` `def create_param(name, kind, default, description, category, root)` -- Create an operator parameter and persist it in the registry.
- `update_param` (function) `core/param_registry.py:341` `def update_param(name, default, description, kind, category, root)` -- Update an operator parameter in place.
- `delete_param` (function) `core/param_registry.py:387` `def delete_param(name, root)` -- Delete an operator parameter from the registry.
- `param_value` (function) `core/param_registry.py:411` `def param_value(name, root)` -- Return the effective value of an operator parameter.
- `operator_specs` (function) `core/param_registry.py:425` `def operator_specs(root)` -- Return the payload schema specs of the operator parameters.
- `apply_to_schema` (function) `core/param_registry.py:437` `def apply_to_schema(root)` -- Register the operator parameters in the payload schema.
- `sync_shell_params` (function) `core/param_registry.py:459` `def sync_shell_params(shell, root)` -- Push the operator parameters into a live shell parameter dict.


Next: [API_p7.md](API_p7.md)
