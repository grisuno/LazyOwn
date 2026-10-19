# Symbols (page 7 of 43)
Previous: [SYMBOLS_p6.md](SYMBOLS_p6.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `process_packet` | function | `contrib/legacy/lazyhoneypot.py:137` | `def process_packet(packet)` |
| `setup_logging` | function | `contrib/legacy/lazyhoneypot.py:52` | `def setup_logging(log_file)` |
| `RequestHandler` | class | `contrib/legacy/lazyhttpreverseshell.py:51` | `class RequestHandler(BaseHTTPRequestHandler)` |
| `compress` | function | `contrib/legacy/lazyhttpreverseshell.py:20` | `def compress(data)` |
| `decompress` | function | `contrib/legacy/lazyhttpreverseshell.py:23` | `def decompress(data)` |
| `decrypt` | function | `contrib/legacy/lazyhttpreverseshell.py:17` | `def decrypt(data)` |
| `do_GET` | method | `contrib/legacy/lazyhttpreverseshell.py:52` | `def do_GET(self)` |
| `do_POST` | method | `contrib/legacy/lazyhttpreverseshell.py:65` | `def do_POST(self)` |
| `encrypt` | function | `contrib/legacy/lazyhttpreverseshell.py:14` | `def encrypt(data)` |
| `parse_arguments` | function | `contrib/legacy/lazyhttpreverseshell.py:88` | `def parse_arguments(args)` |
| `reverse_http_shell_client` | function | `contrib/legacy/lazyhttpreverseshell.py:26` | `def reverse_http_shell_client(lhost, rhost, rport)` |
| `reverse_http_shell_server` | function | `contrib/legacy/lazyhttpreverseshell.py:50` | `def reverse_http_shell_server(lhost, lport)` |
| `decrypt` | function | `contrib/legacy/lazykeygen.py:17` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazykeygen.py:11` | `def encrypt(plaintext, key)` |
| `generate_key` | function | `contrib/legacy/lazykeygen.py:23` | `def generate_key(length)` |
| `main` | function | `contrib/legacy/lazykeygen.py:26` | `def main()` |
| `pad` | function | `contrib/legacy/lazykeygen.py:8` | `def pad(s)` |
| `check_lfi_success` | function | `contrib/legacy/lazylfi2rce.py:35` | `def check_lfi_success(response_text)` |
| `check_rfi_success` | function | `contrib/legacy/lazylfi2rce.py:39` | `def check_rfi_success(response_text)` |
| `main` | function | `contrib/legacy/lazylfi2rce.py:43` | `def main()` |
| `signal_handler` | function | `contrib/legacy/lazylfi2rce.py:29` | `def signal_handler(sig, frame)` |
| `LLMEngine` | class | `contrib/legacy/lazyllmchat.py:163` | `class LLMEngine` |
| `LazyOwnLLMChat` | class | `contrib/legacy/lazyllmchat.py:234` | `class LazyOwnLLMChat` |
| `LazyOwnPromptRenderer` | class | `contrib/legacy/lazyllmchat.py:198` | `class LazyOwnPromptRenderer` |
| `LazyOwnShellBridge` | class | `contrib/legacy/lazyllmchat.py:22` | `class LazyOwnShellBridge` |
| `PromptBuilder` | class | `contrib/legacy/lazyllmchat.py:123` | `class PromptBuilder` |
| `SessionContextProvider` | class | `contrib/legacy/lazyllmchat.py:104` | `class SessionContextProvider` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:25` | `def __init__(self, script_path)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:105` | `def __init__(self, session_path)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:164` | `def __init__(self)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:235` | `def __init__(self)` |
| `_analyze` | method | `contrib/legacy/lazyllmchat.py:263` | `def _analyze(self, command, output)` |
| `_direct_query` | method | `contrib/legacy/lazyllmchat.py:273` | `def _direct_query(self, query)` |
| `_get_context` | method | `contrib/legacy/lazyllmchat.py:242` | `def _get_context(self)` |
| `_load_model` | method | `contrib/legacy/lazyllmchat.py:170` | `def _load_model(self)` |
| `_load_shell` | method | `contrib/legacy/lazyllmchat.py:31` | `def _load_shell(self)` |
| `_run_shell_command` | method | `contrib/legacy/lazyllmchat.py:245` | `def _run_shell_command(self, command)` |
| `_run_system_command` | method | `contrib/legacy/lazyllmchat.py:251` | `def _run_system_command(self, command)` |
| `ask` | method | `contrib/legacy/lazyllmchat.py:182` | `def ask(self, prompt)` |
| `banner` | method | `contrib/legacy/lazyllmchat.py:223` | `def banner(self)` |
| `execute` | method | `contrib/legacy/lazyllmchat.py:65` | `def execute(self, command)` |
| `for_command_analysis` | method | `contrib/legacy/lazyllmchat.py:133` | `def for_command_analysis(command, output, context, history)` |
| `for_direct_query` | method | `contrib/legacy/lazyllmchat.py:149` | `def for_direct_query(query, context, history)` |
| `get_history_text` | method | `contrib/legacy/lazyllmchat.py:194` | `def get_history_text(self)` |
| `get_last_lines` | method | `contrib/legacy/lazyllmchat.py:108` | `def get_last_lines(self, count)` |
| `is_ready` | method | `contrib/legacy/lazyllmchat.py:179` | `def is_ready(self)` |
| `main` | function | `contrib/legacy/lazyllmchat.py:309` | `def main()` |
| `no_history_init` | function | `contrib/legacy/lazyllmchat.py:38` | `def no_history_init(self_)` |
| `render` | method | `contrib/legacy/lazyllmchat.py:208` | `def render(self)` |
| `run` | method | `contrib/legacy/lazyllmchat.py:280` | `def run(self, initial_query)` |
| `target` | function | `contrib/legacy/lazyllmchat.py:70` | `def target()` |
| `ensure_http_prefix` | function | `contrib/legacy/lazylogpoisoning.py:39` | `def ensure_http_prefix(url)` |
| `main` | function | `contrib/legacy/lazylogpoisoning.py:53` | `def main()` |
| `signal_handler` | function | `contrib/legacy/lazylogpoisoning.py:45` | `def signal_handler(sig, frame)` |
| `errmsg` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:63` | `def errmsg(str)` |
| `info` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:59` | `def info(str)` |
| `shutdown` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:67` | `def shutdown(code)` |
| `get_mac` | function | `contrib/legacy/lazymidm.py:12` | `def get_mac(ip)` |
| `main` | function | `contrib/legacy/lazymidm.py:68` | `def main()` |
| `mitm` | function | `contrib/legacy/lazymidm.py:37` | `def mitm(target_ip, gateway_ip)` |
| `restore` | function | `contrib/legacy/lazymidm.py:27` | `def restore(target_ip, spoof_ip)` |
| `setup_monitor_mode` | function | `contrib/legacy/lazymidm.py:58` | `def setup_monitor_mode(interface)` |
| `spoof` | function | `contrib/legacy/lazymidm.py:18` | `def spoof(target_ip, spoof_ip)` |
| `start_sslstrip` | function | `contrib/legacy/lazymidm.py:50` | `def start_sslstrip(port)` |
| `start_tcpdump` | function | `contrib/legacy/lazymidm.py:54` | `def start_tcpdump(interface, output_file)` |
| `_sudo_run` | function | `contrib/legacy/lazymitmap.py:14` | `def _sudo_run()` |
| `_validate_iface` | function | `contrib/legacy/lazymitmap.py:19` | `def _validate_iface(value, name)` |
| `append_file` | function | `contrib/legacy/lazymitmap.py:67` | `def append_file(path, s)` |
| `backup_file` | function | `contrib/legacy/lazymitmap.py:121` | `def backup_file(filepath)` |
| `cleanup` | function | `contrib/legacy/lazymitmap.py:315` | `def cleanup()` |
| `configure_dnsmasq` | function | `contrib/legacy/lazymitmap.py:163` | `def configure_dnsmasq(ap_iface, ap_ip_range_start, ap_ip_range_end, ap_ip_gateway, dns_ip_1, dns_ip_2, sslstrip)` |
| `configure_hostapd` | function | `contrib/legacy/lazymitmap.py:195` | `def configure_hostapd(ap_iface, ssid, channel, wpa_passphrase)` |
| `create_dir` | function | `contrib/legacy/lazymitmap.py:72` | `def create_dir(directory)` |
| `flush_iptables` | function | `contrib/legacy/lazymitmap.py:145` | `def flush_iptables()` |
| `install_dependencies` | function | `contrib/legacy/lazymitmap.py:84` | `def install_dependencies()` |
| `print_header` | function | `contrib/legacy/lazymitmap.py:45` | `def print_header()` |
| `restart_service` | function | `contrib/legacy/lazymitmap.py:138` | `def restart_service(service)` |
| `restore_file` | function | `contrib/legacy/lazymitmap.py:128` | `def restore_file(filepath)` |
| `run_cmd_write` | function | `contrib/legacy/lazymitmap.py:49` | `def run_cmd_write(cmd_args, s)` |
| `set_permissions` | function | `contrib/legacy/lazymitmap.py:77` | `def set_permissions(directory, permissions)` |
| `set_speed_limit` | function | `contrib/legacy/lazymitmap.py:248` | `def set_speed_limit(ap_iface, speed_up, speed_down)` |
| `setup_iptables` | function | `contrib/legacy/lazymitmap.py:228` | `def setup_iptables(ap_iface, ap_ip, net_iface)` |
| `setup_network_manager` | function | `contrib/legacy/lazymitmap.py:153` | `def setup_network_manager(ap_iface)` |
| `signal_handler` | function | `contrib/legacy/lazymitmap.py:324` | `def signal_handler(sig, frame)` |
| `start_services` | function | `contrib/legacy/lazymitmap.py:254` | `def start_services(ap_iface, script_path, sslstrip, wireshark, driftnet, tshark)` |
| `write_file` | function | `contrib/legacy/lazymitmap.py:63` | `def write_file(path, s)` |
| `check_arp` | function | `contrib/legacy/lazynetbios.py:58` | `def check_arp(ip)` |
| `check_netbios` | function | `contrib/legacy/lazynetbios.py:71` | `def check_netbios(ip)` |
| `check_sudo` | function | `contrib/legacy/lazynetbios.py:30` | `def check_sudo()` |
| `generate_ip_range` | function | `contrib/legacy/lazynetbios.py:115` | `def generate_ip_range(start_ip, end_ip)` |
| `scan_netbios` | function | `contrib/legacy/lazynetbios.py:45` | `def scan_netbios(ip_range)` |
| `send_nbns_spoof` | function | `contrib/legacy/lazynetbios.py:90` | `def send_nbns_spoof(target_ip, target_name, spoof_ip, trans_id)` |
| `signal_handler` | function | `contrib/legacy/lazynetbios.py:38` | `def signal_handler(sig, frame)` |
| `ntlm_relay` | function | `contrib/legacy/lazyntlrelayx.py:52` | `def ntlm_relay(target_ip, credentials)` |
| `parse_hash_file` | function | `contrib/legacy/lazyntlrelayx.py:5` | `def parse_hash_file(file_path)` |
| `InvalidUsername` | class | `contrib/legacy/lazyopenssh77enum2.py:14` | `class InvalidUsername(Exception)` |
| `add_boolean` | function | `contrib/legacy/lazyopenssh77enum2.py:19` | `def add_boolean()` |
| `check_user` | function | `contrib/legacy/lazyopenssh77enum2.py:50` | `def check_user(username)` |
| `invalid_username` | function | `contrib/legacy/lazyopenssh77enum2.py:36` | `def invalid_username()` |
| `service_accept` | function | `contrib/legacy/lazyopenssh77enum2.py:30` | `def service_accept()` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazyphishingai.py:117` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `clean_think` | function | `contrib/legacy/lazyphishingai.py:28` | `def clean_think(texto)` |
| `clean_yaml` | function | `contrib/legacy/lazyphishingai.py:31` | `def clean_yaml(texto)` |
| `configure_logging` | function | `contrib/legacy/lazyphishingai.py:42` | `def configure_logging(debug)` |
| `create_complex_prompt` | function | `contrib/legacy/lazyphishingai.py:46` | `def create_complex_prompt(base_prompt, history, knowledge_base)` |
| `generate` | function | `contrib/legacy/lazyphishingai.py:155` | `def generate()` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazyphishingai.py:122` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazyphishingai.py:101` | `def load_knowledge_base(file_path)` |
| `parse_args` | function | `contrib/legacy/lazyphishingai.py:192` | `def parse_args()` |
| `process_prompt_local_yaml` | function | `contrib/legacy/lazyphishingai.py:132` | `def process_prompt_local_yaml(prompt, debug, mode, output_file)` |
| `save_knowledge_base` | function | `contrib/legacy/lazyphishingai.py:110` | `def save_knowledge_base(knowledge_base, file_path)` |
| `truncate_message` | function | `contrib/legacy/lazyphishingai.py:37` | `def truncate_message(message, max_chars)` |
| `check_sudo` | function | `contrib/legacy/lazyproxy.py:40` | `def check_sudo()` |
| `get_ip_from_url` | function | `contrib/legacy/lazyproxy.py:87` | `def get_ip_from_url(url)` |
| `handle_request` | function | `contrib/legacy/lazyproxy.py:104` | `def handle_request(client_socket, address)` |
| `hexdump` | function | `contrib/legacy/lazyproxy.py:52` | `def hexdump(src, length)` |
| `receive_from` | function | `contrib/legacy/lazyproxy.py:63` | `def receive_from(connection)` |
| `request_handler` | function | `contrib/legacy/lazyproxy.py:77` | `def request_handler(buffer)` |
| `response_handler` | function | `contrib/legacy/lazyproxy.py:82` | `def response_handler(buffer)` |
| `signal_handler` | function | `contrib/legacy/lazyproxy.py:47` | `def signal_handler(sig, frame)` |
| `start_proxy` | function | `contrib/legacy/lazyproxy.py:183` | `def start_proxy()` |
| `BinaryAttacker` | class | `contrib/legacy/lazypwn.py:70` | `class BinaryAttacker` |
| `BinaryFinder` | class | `contrib/legacy/lazypwn.py:24` | `class BinaryFinder` |
| `__init__` | method | `contrib/legacy/lazypwn.py:25` | `def __init__(self)` |
| `__init__` | method | `contrib/legacy/lazypwn.py:71` | `def __init__(self, binary_path)` |
| `analyze_with_ltrace` | method | `contrib/legacy/lazypwn.py:76` | `def analyze_with_ltrace(self)` |
| `exploit_with_pwntools` | method | `contrib/legacy/lazypwn.py:170` | `def exploit_with_pwntools(self)` |
| `extract_strings` | method | `contrib/legacy/lazypwn.py:83` | `def extract_strings(self)` |
| `find_capabilities_binaries` | method | `contrib/legacy/lazypwn.py:36` | `def find_capabilities_binaries(self)` |
| `find_executable_binaries` | method | `contrib/legacy/lazypwn.py:44` | `def find_executable_binaries(self)` |
| `find_specific_name_binaries` | method | `contrib/legacy/lazypwn.py:52` | `def find_specific_name_binaries(self, names)` |
| `find_suid_binaries` | method | `contrib/legacy/lazypwn.py:28` | `def find_suid_binaries(self)` |
| `get_found_binaries` | method | `contrib/legacy/lazypwn.py:67` | `def get_found_binaries(self)` |
| `main` | function | `contrib/legacy/lazypwn.py:181` | `def main()` |
| `prepare_attack` | method | `contrib/legacy/lazypwn.py:90` | `def prepare_attack(self)` |
| `process_output` | method | `contrib/legacy/lazypwn.py:61` | `def process_output(self, output)` |
| `cleanup_exploit_environment` | function | `contrib/legacy/lazypwnkit.py:31` | `def cleanup_exploit_environment()` |
| `create_exploit_environment` | function | `contrib/legacy/lazypwnkit.py:13` | `def create_exploit_environment()` |
| `execute_exploit` | function | `contrib/legacy/lazypwnkit.py:37` | `def execute_exploit(cmd)` |
| `main` | function | `contrib/legacy/lazypwnkit.py:79` | `def main()` |
| `rmrf` | function | `contrib/legacy/lazypwnkit.py:8` | `def rmrf(path)` |
| `parse_hash_file` | function | `contrib/legacy/lazyreversentlmv2.py:11` | `def parse_hash_file(file_path)` |
| `reverse_shell` | function | `contrib/legacy/lazyreversentlmv2.py:58` | `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, callback_port)` |
| `highlight_term` | function | `contrib/legacy/lazysearch.py:29` | `def highlight_term(text, term)` |
| `main` | function | `contrib/legacy/lazysearch.py:44` | `def main()` |
| `search_in_parquet` | function | `contrib/legacy/lazysearch.py:32` | `def search_in_parquet(term, parquet_files)` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazysearch_bot.py:122` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `check_api_key` | function | `contrib/legacy/lazysearch_bot.py:69` | `def check_api_key()` |
| `configure_logging` | function | `contrib/legacy/lazysearch_bot.py:75` | `def configure_logging(debug)` |
| `create_complex_prompt` | function | `contrib/legacy/lazysearch_bot.py:86` | `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)` |
| `execute_command` | function | `contrib/legacy/lazysearch_bot.py:109` | `def execute_command(command)` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazysearch_bot.py:127` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazysearch_bot.py:112` | `def load_knowledge_base(file_path)` |
| `main` | function | `contrib/legacy/lazysearch_bot.py:158` | `def main()` |
| `parse_args` | function | `contrib/legacy/lazysearch_bot.py:79` | `def parse_args()` |
| `save_knowledge_base` | function | `contrib/legacy/lazysearch_bot.py:118` | `def save_knowledge_base(knowledge_base, file_path)` |
| `show_help` | function | `contrib/legacy/lazysearch_bot.py:65` | `def show_help(message)` |
| `signal_handler` | function | `contrib/legacy/lazysearch_bot.py:59` | `def signal_handler(sig, frame)` |
| `transform_knowledge_base` | function | `contrib/legacy/lazysearch_bot.py:135` | `def transform_knowledge_base(client)` |
| `Config` | class | `contrib/legacy/lazyseo.py:14` | `class Config` |
| `__getitem__` | method | `contrib/legacy/lazyseo.py:20` | `def __getitem__(self, key)` |
| `__init__` | method | `contrib/legacy/lazyseo.py:15` | `def __init__(self, config_dict)` |
| `analyze_seo` | function | `contrib/legacy/lazyseo.py:76` | `def analyze_seo(url)` |
| `crawl` | function | `contrib/legacy/lazyseo.py:57` | `def crawl(url)` |
| `ffuf` | function | `contrib/legacy/lazyseo.py:66` | `def ffuf()` |
| `load_payload` | function | `contrib/legacy/lazyseo.py:23` | `def load_payload()` |
| `make_request` | function | `contrib/legacy/lazyseo.py:28` | `def make_request(url, retries, timeout)` |
| `results` | function | `contrib/legacy/lazyseo.py:49` | `def results(file)` |
| `CustomSMBRelayServer` | class | `contrib/legacy/lazysmbrelay.py:41` | `class CustomSMBRelayServer(SMBRelayServer)` |
| `__init__` | method | `contrib/legacy/lazysmbrelay.py:42` | `def __init__(self)` |
| `check_sudo` | function | `contrib/legacy/lazysmbrelay.py:15` | `def check_sudo()` |
| `execute_remote_command` | method | `contrib/legacy/lazysmbrelay.py:50` | `def execute_remote_command(self)` |
| `handleData` | method | `contrib/legacy/lazysmbrelay.py:46` | `def handleData(self)` |
| `start_smb_relay` | function | `contrib/legacy/lazysmbrelay.py:35` | `def start_smb_relay(target, command)` |
| `start_smb_server` | function | `contrib/legacy/lazysmbrelay.py:27` | `def start_smb_server()` |
| `analyze_packet` | function | `contrib/legacy/lazysniff.py:90` | `def analyze_packet(packet)` |
| `capture_packets` | function | `contrib/legacy/lazysniff.py:112` | `def capture_packets(interface, count, filter, pcap_file, packets, win_top, win_bottom)` |
| `check_sudo` | function | `contrib/legacy/lazysniff.py:41` | `def check_sudo()` |
| `main` | function | `contrib/legacy/lazysniff.py:197` | `def main()` |
| `main_curses` | function | `contrib/legacy/lazysniff.py:118` | `def main_curses(stdscr, packets, interface, count, filter, pcap_file)` |
| `parse_arguments` | function | `contrib/legacy/lazysniff.py:188` | `def parse_arguments()` |
| `process_packet` | function | `contrib/legacy/lazysniff.py:80` | `def process_packet(packet, packets, win_top, win_bottom)` |
| `restore_curses` | function | `contrib/legacy/lazysniff.py:66` | `def restore_curses(stdscr)` |
| `setup_curses` | function | `contrib/legacy/lazysniff.py:57` | `def setup_curses()` |
| `show_banner` | function | `contrib/legacy/lazysniff.py:73` | `def show_banner(stdscr, banner)` |
| `signal_handler` | function | `contrib/legacy/lazysniff.py:50` | `def signal_handler(sig, frame)` |
| `main` | function | `contrib/legacy/lazysqli.py:89` | `def main(args)` |
| `send_payload` | function | `contrib/legacy/lazysqli.py:13` | `def send_payload(payload, url, s, sql_time)` |
| `sqli_dichotomie` | function | `contrib/legacy/lazysqli.py:30` | `def sqli_dichotomie(payload_brute, offset, url, s, sql_time)` |
| `sqli_thread` | function | `contrib/legacy/lazysqli.py:51` | `def sqli_thread(url, db, table, col, sql_time, threads)` |
| `execute` | function | `contrib/legacy/lazyssh.py:13` | `def execute(hostname, port, command)` |
| `connect` | function | `contrib/legacy/lazyvsftp.py:7` | `def connect(host, port)` |
| `exploit` | function | `contrib/legacy/lazyvsftp.py:16` | `def exploit(host, port)` |
| `handle_backdoor` | function | `contrib/legacy/lazyvsftp.py:61` | `def handle_backdoor(s)` |
| `def_handler` | function | `contrib/legacy/sql.py:8` | `def def_handler(sig, frame)` |
| `getUnicode` | function | `contrib/legacy/sql.py:15` | `def getUnicode(sqli)` |
| `makeRequest` | function | `contrib/legacy/sql.py:22` | `def makeRequest(sqli_modified)` |
| `ApiAuthzConfig` | class | `core/api_authz.py:54` | `class ApiAuthzConfig` |
| `ApiKey` | class | `core/api_authz.py:75` | `class ApiKey` |
| `ApiKeyStore` | class | `core/api_authz.py:161` | `class ApiKeyStore` |
| `__init__` | method | `core/api_authz.py:170` | `def __init__(self, config)` |
| `_extract_key` | function | `core/api_authz.py:393` | `def _extract_key(request_obj)` |
| `_generate_token_bytes` | function | `core/api_authz.py:147` | `def _generate_token_bytes(nbytes)` |
| `_grace_deadline` | method | `core/api_authz.py:197` | `def _grace_deadline(self, retired_at)` |
| `_hash_secret` | function | `core/api_authz.py:137` | `def _hash_secret(secret)` |
| `_prune_record` | method | `core/api_authz.py:343` | `def _prune_record(self, key_hash)` |
| `_prune_retired` | method | `core/api_authz.py:201` | `def _prune_retired(self, records)` |
| `_read` | method | `core/api_authz.py:180` | `def _read(self)` |
| `_touch_last_used` | method | `core/api_authz.py:351` | `def _touch_last_used(self, key_hash)` |
| `_verify_secret` | function | `core/api_authz.py:142` | `def _verify_secret(secret, stored_hash)` |
| `_write` | method | `core/api_authz.py:191` | `def _write(self, data)` |
| `config` | method | `core/api_authz.py:176` | `def config(self)` |
| `create_api_token` | function | `core/api_authz.py:440` | `def create_api_token(store, tenant_id, label, permissions, expires_in_days)` |
| `create_key` | method | `core/api_authz.py:238` | `def create_key(self, tenant_id, label, permissions, expires_in_days)` |
| `decorated` | function | `core/api_authz.py:407` | `def decorated()` |
| `decorator` | function | `core/api_authz.py:405` | `def decorator(f)` |
| `find_by_hash` | method | `core/api_authz.py:229` | `def find_by_hash(self, key_hash)` |
| `from_dict` | method | `core/api_authz.py:107` | `def from_dict(cls, data)` |
| `has_all_permissions` | method | `core/api_authz.py:130` | `def has_all_permissions(self, permissions)` |
| `has_permission` | method | `core/api_authz.py:127` | `def has_permission(self, permission)` |
| `is_expired` | method | `core/api_authz.py:119` | `def is_expired(self)` |
| `is_retired` | method | `core/api_authz.py:124` | `def is_retired(self)` |
| `list_keys` | method | `core/api_authz.py:217` | `def list_keys(self, tenant_id)` |
| `require_api_auth` | function | `core/api_authz.py:365` | `def require_api_auth(store, permissions, require_tenant)` |
| `revoke_key` | method | `core/api_authz.py:273` | `def revoke_key(self, label, tenant_id)` |
| `rotate_key` | method | `core/api_authz.py:309` | `def rotate_key(self, label, tenant_id)` |
| `to_dict` | method | `core/api_authz.py:94` | `def to_dict(self)` |
| `validate_key` | method | `core/api_authz.py:287` | `def validate_key(self, plaintext)` |
| `_guarded_input` | function | `core/autonomous.py:39` | `def _guarded_input(prompt)` |
| `autonomous_mode` | function | `core/autonomous.py:27` | `def autonomous_mode()` |
| `is_autonomous` | function | `core/autonomous.py:21` | `def is_autonomous()` |
| `CommandBridge` | class | `core/command_bridge.py:15` | `class CommandBridge` |
| `__init__` | method | `core/command_bridge.py:18` | `def __init__(self)` |
| `_ensure_shell` | method | `core/command_bridge.py:34` | `def _ensure_shell(self)` |
| `error` | method | `core/command_bridge.py:30` | `def error(self)` |
| `execute` | method | `core/command_bridge.py:110` | `def execute(self, command)` |
| `get_bridge` | function | `core/command_bridge.py:126` | `def get_bridge()` |
| `one_cmd` | method | `core/command_bridge.py:89` | `def one_cmd(self, command)` |
| `onecmd` | method | `core/command_bridge.py:65` | `def onecmd(self, command)` |
| `ready` | method | `core/command_bridge.py:25` | `def ready(self)` |
| `Config` | class | `core/config.py:206` | `class Config` |
| `__getattr__` | method | `core/config.py:228` | `def __getattr__(self, name)` |
| `__getitem__` | method | `core/config.py:231` | `def __getitem__(self, key)` |
| `__init__` | method | `core/config.py:219` | `def __init__(self, config_dict, sessions_dir)` |
| `_apply_env_overrides` | function | `core/config.py:70` | `def _apply_env_overrides(payload)` |
| `_calling_frame` | function | `core/config.py:168` | `def _calling_frame()` |
| `_coerce_env_value` | function | `core/config.py:103` | `def _coerce_env_value(raw, existing)` |
| `_collect_validation_warnings` | function | `core/config.py:182` | `def _collect_validation_warnings(payload)` |
| `_load_raw_payload` | function | `core/config.py:304` | `def _load_raw_payload(path)` |
| `_log_config_change` | function | `core/config.py:146` | `def _log_config_change(key, old_value, new_value)` |
| `_mask_if_sensitive` | function | `core/config.py:128` | `def _mask_if_sensitive(key, value)` |
| `_migrate_keys` | function | `core/config.py:249` | `def _migrate_keys(config_dict)` |
| `as_params` | method | `core/config.py:234` | `def as_params(self)` |
| `load_and_validate` | function | `core/config.py:345` | `def load_and_validate(path)` |
| `load_payload` | function | `core/config.py:327` | `def load_payload(path)` |
| `overridden_keys` | method | `core/config.py:244` | `def overridden_keys(self)` |
| `resolve_aes_key` | function | `core/config.py:261` | `def resolve_aes_key(config_dict)` |
| `save_payload` | function | `core/config.py:396` | `def save_payload(payload, path)` |
| `_emit` | function | `core/console.py:208` | `def _emit(line)` |
| `_paint` | function | `core/console.py:114` | `def _paint(code, text)` |
| `_sanitize` | function | `core/console.py:93` | `def _sanitize(text)` |
| `colors_enabled` | function | `core/console.py:98` | `def colors_enabled()` |
| `ensure_blocking_stdio` | function | `core/console.py:161` | `def ensure_blocking_stdio()` |
| `format_line` | function | `core/console.py:121` | `def format_line(prefix, message, glyph)` |
| `print_error` | function | `core/console.py:137` | `def print_error(error)` |
| `print_msg` | function | `core/console.py:143` | `def print_msg(msg)` |
| `print_succ` | function | `core/console.py:155` | `def print_succ(msg)` |
| `print_warn` | function | `core/console.py:149` | `def print_warn(warn)` |
| `write_stdout` | function | `core/console.py:180` | `def write_stdout(text)` |
| `_get_aes_key` | function | `core/credential_vault.py:79` | `def _get_aes_key(payload)` |
| `check_dangerous_defaults` | function | `core/credential_vault.py:63` | `def check_dangerous_defaults(payload)` |
| `generate_secure_defaults` | function | `core/credential_vault.py:215` | `def generate_secure_defaults()` |
| `rotate_aes_key` | function | `core/credential_vault.py:186` | `def rotate_aes_key(payload, current_key)` |
| `seal_payload` | function | `core/credential_vault.py:141` | `def seal_payload(payload, key)` |
| `seal_value` | function | `core/credential_vault.py:93` | `def seal_value(plaintext, key)` |
| `unseal_payload` | function | `core/credential_vault.py:164` | `def unseal_payload(payload, key)` |
| `unseal_value` | function | `core/credential_vault.py:112` | `def unseal_value(sealed, key)` |
| `AESdecrypt` | function | `core/crypto.py:123` | `def AESdecrypt(data, key)` |
| `AESencrypt` | function | `core/crypto.py:98` | `def AESencrypt(plaintext, key)` |
| `derive_key` | function | `core/crypto.py:36` | `def derive_key(password, salt)` |
| `dropFile` | function | `core/crypto.py:154` | `def dropFile(key, ciphertext)` |
| `generate_salt` | function | `core/crypto.py:24` | `def generate_salt(length)` |
| `generate_xor_key` | function | `core/crypto.py:83` | `def generate_xor_key(length)` |
| `xor_encrypt_decrypt` | function | `core/crypto.py:67` | `def xor_encrypt_decrypt(data, key)` |
| `clear_cache` | function | `core/defaults.py:44` | `def clear_cache()` |
| `common_wordlists` | function | `core/defaults.py:90` | `def common_wordlists()` |
| `default_lport` | function | `core/defaults.py:63` | `def default_lport()` |
| `default_rport` | function | `core/defaults.py:72` | `def default_rport()` |
| `get` | function | `core/defaults.py:49` | `def get(section, key, default)` |
| `load_defaults` | function | `core/defaults.py:21` | `def load_defaults(path)` |
| `rockyou_wordlist` | function | `core/defaults.py:81` | `def rockyou_wordlist()` |
| `sessions_dir` | function | `core/defaults.py:100` | `def sessions_dir()` |
| `DependencyReport` | class | `core/dependencies.py:268` | `class DependencyReport` |
| `DependencySpec` | class | `core/dependencies.py:66` | `class DependencySpec` |
| `DependencyStatus` | class | `core/dependencies.py:253` | `class DependencyStatus` |
| `MissingDependencyError` | class | `core/dependencies.py:37` | `class MissingDependencyError(ImportError)` |
| `_DeferredImport` | class | `core/dependencies.py:101` | `class _DeferredImport` |
| `__bool__` | method | `core/dependencies.py:152` | `def __bool__(self)` |
| `__call__` | method | `core/dependencies.py:136` | `def __call__(self)` |
| `__getattr__` | method | `core/dependencies.py:132` | `def __getattr__(self, _name)` |
| `__getitem__` | method | `core/dependencies.py:140` | `def __getitem__(self, _key)` |
| `__init__` | method | `core/dependencies.py:45` | `def __init__(self, import_name, pip_package, feature)` |
| `__init__` | method | `core/dependencies.py:115` | `def __init__(self, spec)` |
| `__iter__` | method | `core/dependencies.py:144` | `def __iter__(self)` |
| `__len__` | method | `core/dependencies.py:148` | `def __len__(self)` |
| `_raise` | method | `core/dependencies.py:123` | `def _raise(self)` |
| `_spec_for` | function | `core/dependencies.py:157` | `def _spec_for(import_name, pip_package, feature)` |
| `collect_dependency_report` | function | `core/dependencies.py:312` | `def collect_dependency_report()` |
| `format_report` | function | `core/dependencies.py:323` | `def format_report(report)` |
| `main` | function | `core/dependencies.py:368` | `def main()` |
| `missing` | method | `core/dependencies.py:278` | `def missing(self)` |
| `ok` | method | `core/dependencies.py:283` | `def ok(self)` |
| `optional_attr` | function | `core/dependencies.py:209` | `def optional_attr(import_name, attr)` |
| `optional_import` | function | `core/dependencies.py:183` | `def optional_import(import_name)` |
| `probe_python_dependency` | function | `core/dependencies.py:288` | `def probe_python_dependency(spec)` |
| `ErrorAdvice` | class | `core/error_advice.py:27` | `class ErrorAdvice` |
| `ErrorAdviceConfig` | class | `core/error_advice.py:16` | `class ErrorAdviceConfig` |
| `docs_url` | method | `core/error_advice.py:35` | `def docs_url(self, config)` |
| `get_advice` | function | `core/error_advice.py:74` | `def get_advice(key)` |
| `render_advice` | function | `core/error_advice.py:86` | `def render_advice(key, config)` |
| `AuthError` | class | `core/errors.py:92` | `class AuthError(LazyOwnError)` |
| `ConfigError` | class | `core/errors.py:78` | `class ConfigError(LazyOwnError)` |
| `DatabaseError` | class | `core/errors.py:113` | `class DatabaseError(LazyOwnError)` |
| `ErrorCode` | class | `core/errors.py:10` | `class ErrorCode(IntEnum)` |
| `LazyOwnError` | class | `core/errors.py:58` | `class LazyOwnError(Exception)` |
| `NetworkError` | class | `core/errors.py:120` | `class NetworkError(LazyOwnError)` |
| `PayloadError` | class | `core/errors.py:106` | `class PayloadError(LazyOwnError)` |
| `PermissionError` | class | `core/errors.py:127` | `class PermissionError(LazyOwnError)` |
| `TargetError` | class | `core/errors.py:85` | `class TargetError(LazyOwnError)` |
| `ToolError` | class | `core/errors.py:99` | `class ToolError(LazyOwnError)` |
| `ValidationError` | class | `core/errors.py:134` | `class ValidationError(LazyOwnError)` |
| `__init__` | method | `core/errors.py:61` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:81` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:88` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:95` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:102` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:109` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:116` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:123` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:130` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:137` | `def __init__(self, message, error_code)` |
| `__str__` | method | `core/errors.py:74` | `def __str__(self)` |
| `to_dict` | method | `core/errors.py:66` | `def to_dict(self)` |
| `_validate_input` | function | `core/executor.py:41` | `def _validate_input(command)` |
| `_validate_timeout` | function | `core/executor.py:75` | `def _validate_timeout(timeout)` |
| `run_shell` | function | `core/executor.py:149` | `def run_shell(cmd)` |
| `safe_run` | function | `core/executor.py:96` | `def safe_run(command)` |
| `safe_run` | function | `core/executor.py:98` | `def safe_run(command)` |
| `safe_run` | function | `core/executor.py:101` | `def safe_run(command)` |
| `SecurityViolation` | class | `core/hardening.py:125` | `class SecurityViolation(PermissionError)` |
| `_is_emoji_codepoint` | function | `core/hardening.py:698` | `def _is_emoji_codepoint(code)` |
| `_mask` | function | `core/hardening.py:837` | `def _mask(match)` |
| `_seal_key` | function | `core/hardening.py:740` | `def _seal_key(sessions_dir)` |
| `build_sshpass_command` | function | `core/hardening.py:234` | `def build_sshpass_command(password, ssh_args)` |
| `contains_emoji` | function | `core/hardening.py:706` | `def contains_emoji(text)` |
| `defused_xml_parse` | function | `core/hardening.py:396` | `def defused_xml_parse(source)` |
| `escape_html_content` | function | `core/hardening.py:282` | `def escape_html_content(value)` |
| `escape_powershell_single_quoted` | function | `core/hardening.py:104` | `def escape_powershell_single_quoted(value)` |
| `is_safe_dir_path` | function | `core/hardening.py:562` | `def is_safe_dir_path(raw)` |
| `is_safe_path_segment` | function | `core/hardening.py:541` | `def is_safe_path_segment(segment)` |
| `is_safe_yaml_name` | function | `core/hardening.py:588` | `def is_safe_yaml_name(name)` |
| `iter_emoji_spans` | function | `core/hardening.py:721` | `def iter_emoji_spans(text)` |
| `redact_text` | function | `core/hardening.py:826` | `def redact_text(text)` |
| `reject_option_injection` | function | `core/hardening.py:85` | `def reject_option_injection(argv)` |
| `require_encryption_key` | function | `core/hardening.py:368` | `def require_encryption_key(env_key, secret_file)` |
| `safe_clipboard_copy` | function | `core/hardening.py:195` | `def safe_clipboard_copy(content)` |
| `safe_join_under` | function | `core/hardening.py:607` | `def safe_join_under(base_dir, user_path)` |
| `safe_open_under` | function | `core/hardening.py:636` | `def safe_open_under(base_dir, user_path, mode)` |
| `safe_path_join` | function | `core/hardening.py:294` | `def safe_path_join(base_dir, user_path)` |
| `safe_subprocess_run` | function | `core/hardening.py:150` | `def safe_subprocess_run(argv)` |
| `sanitize_filename` | function | `core/hardening.py:418` | `def sanitize_filename(filename, max_length)` |
| `seal_secret` | function | `core/hardening.py:754` | `def seal_secret(plaintext)` |
| `set_sshpass_env` | function | `core/hardening.py:263` | `def set_sshpass_env(password)` |
| `store_secret_owner_only` | function | `core/hardening.py:663` | `def store_secret_owner_only(path, text)` |
| `terminal_env` | function | `core/hardening.py:129` | `def terminal_env(base)` |
| `tls_lab_fallback_context` | function | `core/hardening.py:490` | `def tls_lab_fallback_context()` |
| `tls_lab_unverified_allowed` | function | `core/hardening.py:463` | `def tls_lab_unverified_allowed(host)` |
| `tls_secure_context` | function | `core/hardening.py:438` | `def tls_secure_context(extra_ca)` |
| `unseal_secret` | function | `core/hardening.py:785` | `def unseal_secret(stored)` |
| `validate_host` | function | `core/hardening.py:348` | `def validate_host(host)` |
| `validate_network_cidr` | function | `core/hardening.py:320` | `def validate_network_cidr(cidr)` |
| `validate_port_spec` | function | `core/hardening.py:332` | `def validate_port_spec(ports)` |
| `validate_upstream_path` | function | `core/hardening.py:512` | `def validate_upstream_path(path)` |
| `is_valid_cidr` | function | `core/host_policy.py:32` | `def is_valid_cidr(value)` |
| `is_valid_host` | function | `core/host_policy.py:48` | `def is_valid_host(value)` |
| `rejects_shell_meta` | function | `core/host_policy.py:20` | `def rejects_shell_meta(value)` |
| `display_news` | function | `core/http.py:198` | `def display_news(titles, links, scores)` |
| `exploitalert` | function | `core/http.py:106` | `def exploitalert(content)` |
| `generate_http_req` | function | `core/http.py:18` | `def generate_http_req(host, port, uri, custom_header, cmd)` |
| `get_banner` | function | `core/http.py:50` | `def get_banner(host, port)` |
| `get_command` | function | `core/http.py:69` | `def get_command(url, lhost)` |
| `inject_payloads` | function | `core/http.py:211` | `def inject_payloads(urls, payload_url, request_timeout)` |
| `nvddb` | function | `core/http.py:143` | `def nvddb(content)` |
| `packetstormsecurity` | function | `core/http.py:125` | `def packetstormsecurity(content)` |
| `scrape_news` | function | `core/http.py:174` | `def scrape_news()` |
| `send_command` | function | `core/http.py:87` | `def send_command(cmd, url, lhost)` |
| `BudgetConfig` | class | `core/llm_budget.py:103` | `class BudgetConfig` |
| `BudgetExceeded` | class | `core/llm_budget.py:54` | `class BudgetExceeded(RuntimeError)` |
| `BudgetGuard` | class | `core/llm_budget.py:310` | `class BudgetGuard` |
| `BudgetLedger` | class | `core/llm_budget.py:176` | `class BudgetLedger` |
| `BudgetedBackend` | class | `core/llm_budget.py:408` | `class BudgetedBackend` |
| `LLMBackendLike` | class | `core/llm_budget.py:58` | `class LLMBackendLike(Protocol)` |
| `LedgerEntry` | class | `core/llm_budget.py:132` | `class LedgerEntry` |
| `ModelPrice` | class | `core/llm_budget.py:69` | `class ModelPrice` |
| `TokenEstimator` | class | `core/llm_budget.py:268` | `class TokenEstimator` |
| `__init__` | method | `core/llm_budget.py:278` | `def __init__(self, encoding_name)` |
| `__init__` | method | `core/llm_budget.py:319` | `def __init__(self, config, estimator, ledger)` |
| `__init__` | method | `core/llm_budget.py:417` | `def __init__(self, inner, guard, model)` |
| `_coerce_bool` | function | `core/llm_budget.py:476` | `def _coerce_bool(value, default)` |
| `_coerce_positive_float` | function | `core/llm_budget.py:520` | `def _coerce_positive_float(value, default)` |
| `_coerce_positive_int` | function | `core/llm_budget.py:536` | `def _coerce_positive_int(value, default)` |
| `_coerce_price_table` | function | `core/llm_budget.py:496` | `def _coerce_price_table(value)` |
| `_empty_state` | method | `core/llm_budget.py:189` | `def _empty_state(self)` |
| `_has_required_methods` | function | `core/llm_budget.py:642` | `def _has_required_methods(backend)` |
| `_load` | method | `core/llm_budget.py:193` | `def _load(self)` |
| `_load_encoding` | method | `core/llm_budget.py:283` | `def _load_encoding(encoding_name)` |
| `_now_iso` | function | `core/llm_budget.py:163` | `def _now_iso(now)` |
| `_save` | method | `core/llm_budget.py:215` | `def _save(self, state)` |
| `_state` | method | `core/llm_budget.py:226` | `def _state(self)` |
| `_today_utc` | function | `core/llm_budget.py:150` | `def _today_utc(now)` |
| `calls_today` | method | `core/llm_budget.py:256` | `def calls_today(self)` |
| `complete` | method | `core/llm_budget.py:65` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `core/llm_budget.py:435` | `def complete(self, system, user, max_tokens, temperature)` |
| `count` | method | `core/llm_budget.py:292` | `def count(self, text)` |
| `default_model_prices` | function | `core/llm_budget.py:442` | `def default_model_prices()` |
| `default_sessions_dir` | function | `core/llm_budget.py:461` | `def default_sessions_dir()` |
| `estimate_and_check` | method | `core/llm_budget.py:356` | `def estimate_and_check(self, prompt, model, output_tokens)` |
| `estimate_cost` | method | `core/llm_budget.py:343` | `def estimate_cost(self, model, input_tokens, output_tokens)` |
| `format_budget_status` | function | `core/llm_budget.py:616` | `def format_budget_status(config, ledger)` |
| `from_mapping` | method | `core/llm_budget.py:81` | `def from_mapping(cls, data)` |
| `generate` | method | `core/llm_budget.py:61` | `def generate(self, prompt)` |
| `generate` | method | `core/llm_budget.py:422` | `def generate(self, prompt)` |
| `load_budget_config` | function | `core/llm_budget.py:552` | `def load_budget_config(payload, sessions_dir)` |
| `price_for` | method | `core/llm_budget.py:329` | `def price_for(self, model)` |
| `read_budget_status` | function | `core/llm_budget.py:585` | `def read_budget_status(payload, sessions_dir)` |
| `record` | method | `core/llm_budget.py:232` | `def record(self, entry)` |
| `reset` | method | `core/llm_budget.py:261` | `def reset(self)` |
| `spent_today` | method | `core/llm_budget.py:251` | `def spent_today(self)` |
| `stream_generate` | method | `core/llm_budget.py:63` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `core/llm_budget.py:430` | `def stream_generate(self, prompt)` |
| `wrap_backend_with_budget` | function | `core/llm_budget.py:657` | `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` |
| `StructuredLogConfig` | class | `core/logging.py:42` | `class StructuredLogConfig` |
| `StructuredLogger` | class | `core/logging.py:139` | `class StructuredLogger(Logger)` |
| `_ConsoleFormatter` | class | `core/logging.py:121` | `class _ConsoleFormatter(Formatter)` |
| `_JsonLineFormatter` | class | `core/logging.py:71` | `class _JsonLineFormatter(Formatter)` |
| `__init__` | method | `core/logging.py:74` | `def __init__(self, redacted_fields)` |
| `_log_factory` | function | `core/logging.py:180` | `def _log_factory(name, config)` |
| `format` | method | `core/logging.py:78` | `def format(self, record)` |
| `format` | method | `core/logging.py:132` | `def format(self, record)` |
| `get_logger` | function | `core/logging.py:231` | `def get_logger(name)` |
| `install_json_handler` | function | `core/logging.py:251` | `def install_json_handler(name, config)` |
| `makeRecord` | method | `core/logging.py:148` | `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)` |
| `reconfigure` | function | `core/logging.py:300` | `def reconfigure(config)` |
| `create_arp_packet` | function | `core/network.py:33` | `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` |
| `get_banner` | function | `core/network.py:134` | `def get_banner(ip, port)` |
| `get_network_info` | function | `core/network.py:154` | `def get_network_info()` |
| `get_open_ports` | function | `core/network.py:105` | `def get_open_ports()` |
| `is_port_in_use` | function | `core/network.py:120` | `def is_port_in_use(port, host)` |
| `parse_ip_mac` | function | `core/network.py:18` | `def parse_ip_mac(input_string)` |
| `parse_proc_net_file` | function | `core/network.py:78` | `def parse_proc_net_file(file_path)` |
| `send_packet` | function | `core/network.py:66` | `def send_packet(packet, iface)` |
| `strip_ansi` | function | `core/parsers.py:15` | `def strip_ansi(text)` |
| `FieldKind` | class | `core/payload_schema.py:73` | `class FieldKind(StrEnum)` |
| `FieldSpec` | class | `core/payload_schema.py:100` | `class FieldSpec` |
| `Severity` | class | `core/payload_schema.py:91` | `class Severity(StrEnum)` |
| `ValidationIssue` | class | `core/payload_schema.py:142` | `class ValidationIssue` |
| `_coerce_bool` | function | `core/payload_schema.py:316` | `def _coerce_bool(raw)` |
| `_coerce_int` | function | `core/payload_schema.py:301` | `def _coerce_int(raw)` |
| `_spec` | function | `core/payload_schema.py:335` | `def _spec(name, kind, default, description)` |
| `_validate_bool` | function | `core/payload_schema.py:195` | `def _validate_bool(value)` |
| `_validate_hex` | function | `core/payload_schema.py:254` | `def _validate_hex(value)` |
| `_validate_hostname` | function | `core/payload_schema.py:220` | `def _validate_hostname(value)` |
| `_validate_int` | function | `core/payload_schema.py:171` | `def _validate_int(value)` |
| `_validate_interface` | function | `core/payload_schema.py:246` | `def _validate_interface(value)` |
| `_validate_ip` | function | `core/payload_schema.py:212` | `def _validate_ip(value)` |
| `_validate_json_blob` | function | `core/payload_schema.py:268` | `def _validate_json_blob(value)` |
| `_validate_opaque` | function | `core/payload_schema.py:280` | `def _validate_opaque(_value)` |
| `_validate_os_id` | function | `core/payload_schema.py:262` | `def _validate_os_id(value)` |
| `_validate_path` | function | `core/payload_schema.py:240` | `def _validate_path(value)` |
| `_validate_port` | function | `core/payload_schema.py:185` | `def _validate_port(value)` |
| `_validate_string` | function | `core/payload_schema.py:165` | `def _validate_string(value)` |
| `_validate_url` | function | `core/payload_schema.py:232` | `def _validate_url(value)` |
| `categories` | function | `core/payload_schema.py:1745` | `def categories()` |
| `coerce_value` | function | `core/payload_schema.py:1587` | `def coerce_value(key, raw)` |
| `default_payload` | function | `core/payload_schema.py:1737` | `def default_payload()` |
| `field_for` | function | `core/payload_schema.py:1582` | `def field_for(key)` |
| `format_issue` | function | `core/payload_schema.py:1719` | `def format_issue(issue)` |
| `validate_payload` | function | `core/payload_schema.py:1684` | `def validate_payload(payload)` |
| `validate_value` | function | `core/payload_schema.py:1610` | `def validate_value(key, value)` |
| `_drain_stderr` | function | `core/process.py:220` | `def _drain_stderr()` |
| `_print_run_command_status` | function | `core/process.py:159` | `def _print_run_command_status(command, elapsed, exit_code)` |
| `activate_server` | function | `core/process.py:271` | `def activate_server(httpd, url, lhost)` |
| `check_go_tool_installed` | function | `core/process.py:34` | `def check_go_tool_installed(tool_name)` |

Next: [SYMBOLS_p8.md](SYMBOLS_p8.md)
