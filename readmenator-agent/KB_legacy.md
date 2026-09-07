# Subsystem: legacy

## modules/legacy/__init__.py
- Layer: utility
- Language: py

## modules/legacy/lazy_http_bof.py
- Layer: presentation
- Language: py
- Symbols:
  - `genHeader` (function, line 6) `def genHeader(raw)`
  - `exploit` (function, line 29) `def exploit(target, port, payload)`

## modules/legacy/lazy_packet_image_sniffer.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 23) `def check_sudo()`
  - `list_interfaces` (function, line 31) `def list_interfaces()`
  - `choose_interface` (function, line 49) `def choose_interface(interfaces)`
  - `get_subnet_from_interface` (function, line 61) `def get_subnet_from_interface(interface)`
  - `get_ip_addresses` (function, line 65) `def get_ip_addresses(interface)`
  - `handle_packet` (function, line 111) `def handle_packet(packet)`
  - `save_image` (function, line 161) `def save_image(src_ip, end_idx)`
  - `run` (function, line 187) `def run()`
  - `daemonize` (function, line 192) `def daemonize()`

## modules/legacy/lazyaddon_creator.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_github_url` (function, line 49) `def parse_github_url(url)`
  - `github_api_get` (function, line 58) `def github_api_get(owner, repo, endpoint)`
  - `fetch_repo_metadata` (function, line 68) `def fetch_repo_metadata(owner, repo)`
  - `fetch_readme` (function, line 73) `def fetch_readme(owner, repo)`
  - `fetch_root_files` (function, line 85) `def fetch_root_files(owner, repo)`
  - `build_llm_prompt` (function, line 98) `def build_llm_prompt(meta, readme, root_files)`
  - `extract_json_from_response` (function, line 164) `def extract_json_from_response(text)`
  - `heuristic_install_command` (function, line 192) `def heuristic_install_command(root_files, language)`
  - `heuristic_execute_command` (function, line 211) `def heuristic_execute_command(name, root_files, language)`
  - `heuristic_params` (function, line 245) `def heuristic_params(name, readme, root_files)`
  - `fallback_yaml_data` (function, line 276) `def fallback_yaml_data(meta, readme, root_files)`
  - `build_yaml` (function, line 300) `def build_yaml(data, repo_url)`
  - `save_yaml` (function, line 336) `def save_yaml(addon, output_dir)`
  - `main` (function, line 357) `def main()`
- Depends on: `modules/llm_client.py`

## modules/legacy/lazyarpspoofing.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 26) `def check_sudo()`
  - `enable_ip_forward` (function, line 34) `def enable_ip_forward()`
  - `disable_ip_forward` (function, line 37) `def disable_ip_forward()`
  - `get_local_ip` (function, line 40) `def get_local_ip(ifname)`
  - `get_mac` (function, line 48) `def get_mac(ip, device, retries, timeout)`
  - `spoofer` (function, line 68) `def spoofer(target, spoofed, device)`
  - `main` (function, line 79) `def main()`

## modules/legacy/lazybinenc.py
- Layer: utility
- Language: py
- Symbols:
  - `generate_key_iv` (function, line 12) `def generate_key_iv(sessions_path)`
  - `main` (function, line 54) `def main()`
- Depends on: `cli/commands/pwn.py`, `core/console.py`, `core/prompt.py`

## modules/legacy/lazybotcli.py
- Layer: utility
- Language: py
- Symbols:
  - `encrypt` (function, line 30) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 36) `def decrypt(ciphertext, key)`
  - `main` (function, line 42) `def main()`

## modules/legacy/lazybotnet.py
- Layer: utility
- Language: py
- Symbols:
  - `encrypt` (function, line 46) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 52) `def decrypt(ciphertext, key)`
  - `add_to_botnet` (function, line 58) `def add_to_botnet(ip, port, botnet_file)`
  - `clean_botnet` (function, line 62) `def clean_botnet(ip, port, botnet_file)`
  - `send_to_botnet` (function, line 71) `def send_to_botnet(cmd, key, botnet_file)`
  - `Keylogger` (class, line 89) `class Keylogger`
  - `handle_client` (method, line 144) `def handle_client(conn, key, botnet_file, log_file)`
  - `start_server` (method, line 182) `def start_server(host, port, key, botnet_file, log_file)`
  - `__init__` (method, line 90) `def __init__(self, key, log_file)`
  - `on_press` (method, line 95) `def on_press(self, key)`
  - `start` (method, line 106) `def start(self)`
  - `get_log` (method, line 110) `def get_log(self)`
  - `save_log` (method, line 113) `def save_log(self)`
  - `run` (method, line 120) `def run(self)`
  - `setup_persistence` (method, line 125) `def setup_persistence(self)`
  - `create_shortcut` (method, line 136) `def create_shortcut(self, script_path, shortcut_path)`

## modules/legacy/lazycam.py
- Layer: utility
- Doc: This code is a portion of frigate Event Video Recorder (fEVR)  Copyright (C) 2021-2022  The Bearded Tek (http://www.bear
- Language: py
- Symbols:
  - `RTSPScanner` (class, line 32) `class RTSPScanner`
  - `__init__` (method, line 33) `def __init__(self, verbose, wspace)`
  - `run` (method, line 49) `def run(self)`
  - `resizeImg` (method, line 68) `def resizeImg(self, img, output, height, ratio, fmt)`
  - `splitCSV` (method, line 77) `def splitCSV(self, csv)`
  - `scanner` (method, line 83) `def scanner(self)`
  - `delCameras` (method, line 136) `def delCameras(self)`
  - `addCameras` (method, line 149) `def addCameras(self)`
  - `cla` (method, line 212) `def cla()`
  - `main` (method, line 257) `def main()`

## modules/legacy/lazycreate_webshell.py
- Layer: utility
- Language: py
- Depends on: `modules/lazyencoder_decoder.py`

## modules/legacy/lazydeepseekcli.py
- Layer: presentation
- Language: py
- Symbols:
  - `truncate_message` (function, line 41) `def truncate_message(message, max_chars)`
  - `configure_logging` (function, line 45) `def configure_logging(debug)`
  - `_load_payload_kv` (function, line 50) `def _load_payload_kv()`
  - `_load_report_context` (function, line 68) `def _load_report_context()`
  - `_prompt_redteam` (function, line 79) `def _prompt_redteam(base_prompt, history, knowledge_base)`
  - `_prompt_report` (function, line 118) `def _prompt_report(base_prompt, history, knowledge_base)`
  - `load_knowledge_base` (function, line 167) `def load_knowledge_base(file_path)`
  - `save_knowledge_base` (function, line 174) `def save_knowledge_base(knowledge_base, file_path)`
  - `add_to_knowledge_base` (function, line 179) `def add_to_knowledge_base(prompt, command, file_path)`
  - `get_relevant_knowledge` (function, line 185) `def get_relevant_knowledge(prompt)`
  - `transform_knowledge_base` (function, line 193) `def transform_knowledge_base(prompt_builder)`
  - `_ollama_stream` (function, line 223) `def _ollama_stream(prompt_text, mode)`
  - `process_prompt_local` (function, line 255) `def process_prompt_local(prompt, debug, mode)`
  - `process_prompt_localreport` (function, line 263) `def process_prompt_localreport(prompt, debug, mode)`
  - `parse_args` (function, line 271) `def parse_args()`
  - `generate` (function, line 231) `def generate()`
- Depends on: `core/logging.py`
- Imported by: `modules/llm_adapter.py`

## modules/legacy/lazydisassebler.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `X64Disassembler` (class, line 24) `class X64Disassembler`
  - `main` (method, line 489) `def main()`
  - `__init__` (method, line 34) `def __init__(self)`
  - `read_elf_header` (method, line 79) `def read_elf_header(self, data)`
  - `parse_modrm` (method, line 135) `def parse_modrm(self, modrm, rex)`
  - `parse_sib` (method, line 173) `def parse_sib(self, sib, rex)`
  - `get_operand_str` (method, line 212) `def get_operand_str(self, mod, rm, rex, bytes_data, offset)`
  - `disassemble` (method, line 305) `def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point)`

## modules/legacy/lazyftpsniff.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 21) `def check_sudo()`
  - `signal_handler` (function, line 34) `def signal_handler(sig, frame)`
  - `parse_arguments` (function, line 42) `def parse_arguments()`
  - `sniffer_ftp` (function, line 56) `def sniffer_ftp(pkt)`
  - `main` (function, line 69) `def main()`

## modules/legacy/lazygalazy.py
- Layer: utility
- Language: py
- Symbols:
  - `SamsungKnoxExploitServer` (class, line 8) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`
  - `main` (method, line 97) `def main()`
  - `do_GET` (method, line 11) `def do_GET(self)`
  - `apk_bytes` (method, line 33) `def apk_bytes(self)`
  - `launch_html` (method, line 36) `def launch_html(self)`
  - `exploit_js` (method, line 49) `def exploit_js(self)`
  - `rand_word` (method, line 93) `def rand_word(self)`
- Depends on: `modules/backdoor/server.c`

## modules/legacy/lazygptcli.py
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 66) `def signal_handler(sig, frame)`
  - `show_help` (function, line 73) `def show_help(message)`
  - `check_api_key` (function, line 77) `def check_api_key()`
  - `configure_logging` (function, line 83) `def configure_logging(debug)`
  - `parse_args` (function, line 87) `def parse_args()`
  - `create_complex_prompt` (function, line 94) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
  - `execute_command` (function, line 108) `def execute_command(command)`
  - `load_knowledge_base` (function, line 118) `def load_knowledge_base(file_path)`
  - `save_knowledge_base` (function, line 124) `def save_knowledge_base(knowledge_base, file_path)`
  - `add_to_knowledge_base` (function, line 128) `def add_to_knowledge_base(prompt, command, file_path)`
  - `get_relevant_knowledge` (function, line 133) `def get_relevant_knowledge(prompt)`
  - `transform_knowledge_base` (function, line 141) `def transform_knowledge_base(client)`
  - `cleanup_temp_files` (function, line 164) `def cleanup_temp_files()`
  - `main` (function, line 177) `def main()`
- Depends on: `core/logging.py`, `modules/colors.py`, `modules/legacy/lazygptcli_unified.py`

## modules/legacy/lazygptcli_unified.py
- Layer: utility
- Language: py
- Symbols:
  - `_ret_model` (function, line 45) `def _ret_model()`
  - `truncate_message` (function, line 53) `def truncate_message(message, max_chars)`
  - `_configure_logging` (function, line 57) `def _configure_logging(debug)`
  - `_load_knowledge_base` (function, line 62) `def _load_knowledge_base(file_path)`
  - `_save_knowledge_base` (function, line 70) `def _save_knowledge_base(knowledge_base, file_path)`
  - `_add_to_knowledge_base` (function, line 76) `def _add_to_knowledge_base(prompt, response, file_path)`
  - `_get_relevant_knowledge` (function, line 82) `def _get_relevant_knowledge(prompt, file_path)`
  - `_transform_knowledge_base` (function, line 95) `def _transform_knowledge_base(client, kb_file, improved_file)`
  - `_groq_chat` (function, line 115) `def _groq_chat(client, messages, model, max_tokens)`
  - `_load_payload_kv` (function, line 129) `def _load_payload_kv()`
  - `_load_event_config` (function, line 147) `def _load_event_config()`
  - `_prompt_oneliner` (function, line 159) `def _prompt_oneliner(base_prompt, history, knowledge_base)`
  - `_prompt_script` (function, line 175) `def _prompt_script(base_prompt, history, knowledge_base)`
  - `_prompt_adversary` (function, line 190) `def _prompt_adversary(base_prompt, history, knowledge_base)`
  - `_prompt_general` (function, line 206) `def _prompt_general(base_prompt, history, knowledge_base)`
  - `_prompt_search` (function, line 225) `def _prompt_search(base_prompt, history, knowledge_base)`
  - `_prompt_vuln` (function, line 239) `def _prompt_vuln(base_prompt, history, knowledge_base)`
  - `_prompt_task` (function, line 254) `def _prompt_task(base_prompt, history, knowledge_base)`
  - `_prompt_redop` (function, line 267) `def _prompt_redop(base_prompt, history, knowledge_base)`
  - `_process_groq` (function, line 287) `def _process_groq(client, prompt, debug, prompt_template, kb_file, model)`
  - `process_prompt` (function, line 318) `def process_prompt(client, prompt, debug)`
  - `process_prompt_script` (function, line 323) `def process_prompt_script(client, prompt, debug)`
  - `process_prompt_adversary` (function, line 328) `def process_prompt_adversary(client, prompt, debug)`
  - `process_prompt_general` (function, line 333) `def process_prompt_general(client, prompt, debug)`
  - `process_prompt_search` (function, line 341) `def process_prompt_search(client, prompt, debug)`
  - `process_prompt_task` (function, line 346) `def process_prompt_task(client, prompt, debug)`
  - `process_prompt_vuln` (function, line 356) `def process_prompt_vuln(client, prompt, debug, event)`
  - `process_prompt_redop` (function, line 382) `def process_prompt_redop(client, prompt, debug)`
  - `_deepseek_fallback` (function, line 392) `def _deepseek_fallback(prompt)`
- Depends on: `core/logging.py`, `modules/colors.py`
- Imported by: `modules/legacy/lazygptcli.py`, `modules/legacy/lazygptcli.py`

## modules/legacy/lazyhoneypot.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_args` (function, line 33) `def parse_args()`
  - `setup_logging` (function, line 51) `def setup_logging(log_file)`
  - `generate_rsa_key` (function, line 55) `def generate_rsa_key(key_filename)`
  - `Server` (class, line 59) `class Server(ServerInterface)`
  - `handle_connection` (method, line 73) `def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir)`
  - `handle_file_download` (method, line 109) `def handle_file_download(command, downloads_dir, downloads_log)`
  - `log_command` (method, line 123) `def log_command(command, commands_log)`
  - `log_downloaded_file` (method, line 127) `def log_downloaded_file(filename, url, downloads_log)`
  - `analyze_traffic` (method, line 131) `def analyze_traffic()`
  - `alert_admin` (method, line 142) `def alert_admin(message)`
  - `main` (method, line 160) `def main()`
  - `__init__` (method, line 60) `def __init__(self)`
  - `check_channel_request` (method, line 63) `def check_channel_request(self, kind, chanid)`
  - `check_auth_password` (method, line 68) `def check_auth_password(self, username, password)`
  - `process_packet` (method, line 132) `def process_packet(packet)`
- Depends on: `core/logging.py`

## modules/legacy/lazyhttpreverseshell.py
- Layer: presentation
- Language: py
- Symbols:
  - `encrypt` (function, line 14) `def encrypt(data)`
  - `decrypt` (function, line 17) `def decrypt(data)`
  - `compress` (function, line 20) `def compress(data)`
  - `decompress` (function, line 23) `def decompress(data)`
  - `reverse_http_shell_client` (function, line 26) `def reverse_http_shell_client(lhost, rhost, rport)`
  - `reverse_http_shell_server` (function, line 50) `def reverse_http_shell_server(lhost, lport)`
  - `parse_arguments` (function, line 88) `def parse_arguments(args)`
  - `RequestHandler` (class, line 51) `class RequestHandler(BaseHTTPRequestHandler)`
  - `do_GET` (method, line 52) `def do_GET(self)`
  - `do_POST` (method, line 65) `def do_POST(self)`
- Depends on: `modules/backdoor/server.c`

## modules/legacy/lazykeygen.py
- Layer: utility
- Language: py
- Symbols:
  - `pad` (function, line 8) `def pad(s)`
  - `encrypt` (function, line 11) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 17) `def decrypt(ciphertext, key)`
  - `generate_key` (function, line 23) `def generate_key(length)`
  - `main` (function, line 26) `def main()`

## modules/legacy/lazylfi2rce.py
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 29) `def signal_handler(sig, frame)`
  - `check_lfi_success` (function, line 35) `def check_lfi_success(response_text)`
  - `check_rfi_success` (function, line 39) `def check_rfi_success(response_text)`
  - `main` (function, line 43) `def main()`

## modules/legacy/lazyllmchat.py
- Layer: utility
- Language: py
- Symbols:
  - `LazyOwnShellBridge` (class, line 21) `class LazyOwnShellBridge`
  - `SessionContextProvider` (class, line 105) `class SessionContextProvider`
  - `PromptBuilder` (class, line 124) `class PromptBuilder`
  - `LLMEngine` (class, line 164) `class LLMEngine`
  - `LazyOwnPromptRenderer` (class, line 199) `class LazyOwnPromptRenderer`
  - `LazyOwnLLMChat` (class, line 235) `class LazyOwnLLMChat`
  - `main` (method, line 310) `def main()`
  - `__init__` (method, line 24) `def __init__(self, script_path)`
  - `_load_shell` (method, line 30) `def _load_shell(self)`
  - `execute` (method, line 64) `def execute(self, command)`
  - `__init__` (method, line 106) `def __init__(self, session_path)`
  - `get_last_lines` (method, line 109) `def get_last_lines(self, count)`
  - `for_command_analysis` (method, line 134) `def for_command_analysis(command, output, context, history)`
  - `for_direct_query` (method, line 150) `def for_direct_query(query, context, history)`
  - `__init__` (method, line 165) `def __init__(self)`
  - `_load_model` (method, line 171) `def _load_model(self)`
  - `is_ready` (method, line 180) `def is_ready(self)`
  - `ask` (method, line 183) `def ask(self, prompt)`
  - `get_history_text` (method, line 195) `def get_history_text(self)`
  - `render` (method, line 209) `def render(self)`
  - `banner` (method, line 224) `def banner(self)`
  - `__init__` (method, line 236) `def __init__(self)`
  - `_get_context` (method, line 243) `def _get_context(self)`
  - `_run_shell_command` (method, line 246) `def _run_shell_command(self, command)`
  - `_run_system_command` (method, line 252) `def _run_system_command(self, command)`
  - `_analyze` (method, line 264) `def _analyze(self, command, output)`
  - `_direct_query` (method, line 274) `def _direct_query(self, query)`
  - `run` (method, line 281) `def run(self, initial_query)`
  - `target` (method, line 69) `def target()`
  - `no_history_init` (method, line 37) `def no_history_init(self_)`
- Depends on: `modules/ai_model.py`, `modules/llm_factory.py`

## modules/legacy/lazylogpoisoning.py
- Layer: utility
- Language: py
- Symbols:
  - `ensure_http_prefix` (function, line 39) `def ensure_http_prefix(url)`
  - `signal_handler` (function, line 45) `def signal_handler(sig, frame)`
  - `main` (function, line 53) `def main()`
- Depends on: `modules/lazyencoder_decoder.py`

## modules/legacy/lazymariadb_rce_cve_2016-662.py
- Layer: utility
- Doc: MySQL / MariaDB / Percona -  Remote Root Code Execution / PrivEsc PoC Exploit (CVE-2016-6662) 0ldSQL_MySQL_RCE_exploit.p
- Language: py
- Symbols:
  - `info` (function, line 59) `def info(str)`
  - `errmsg` (function, line 63) `def errmsg(str)`
  - `shutdown` (function, line 67) `def shutdown(code)`

## modules/legacy/lazymidm.py
- Layer: utility
- Language: py
- Symbols:
  - `get_mac` (function, line 12) `def get_mac(ip)`
  - `spoof` (function, line 18) `def spoof(target_ip, spoof_ip)`
  - `restore` (function, line 27) `def restore(target_ip, spoof_ip)`
  - `mitm` (function, line 37) `def mitm(target_ip, gateway_ip)`
  - `start_sslstrip` (function, line 50) `def start_sslstrip(port)`
  - `start_tcpdump` (function, line 54) `def start_tcpdump(interface, output_file)`
  - `setup_monitor_mode` (function, line 58) `def setup_monitor_mode(interface)`
  - `main` (function, line 65) `def main()`

## modules/legacy/lazymitmap.py
- Layer: utility
- Language: py
- Symbols:
  - `print_header` (function, line 29) `def print_header()`
  - `run_cmd_write` (function, line 33) `def run_cmd_write(cmd_args, s)`
  - `write_file` (function, line 47) `def write_file(path, s)`
  - `append_file` (function, line 51) `def append_file(path, s)`
  - `create_dir` (function, line 56) `def create_dir(directory)`
  - `set_permissions` (function, line 61) `def set_permissions(directory, permissions)`
  - `install_dependencies` (function, line 66) `def install_dependencies()`
  - `backup_file` (function, line 92) `def backup_file(filepath)`
  - `restore_file` (function, line 97) `def restore_file(filepath)`
  - `restart_service` (function, line 105) `def restart_service(service)`
  - `flush_iptables` (function, line 110) `def flush_iptables()`
  - `setup_network_manager` (function, line 118) `def setup_network_manager(ap_iface)`
  - `configure_dnsmasq` (function, line 127) `def configure_dnsmasq(ap_iface, ap_ip_range_start, ap_ip_range_end, ap_ip_gateway, dns_ip_1, dns_ip_2, sslstrip)`
  - `configure_hostapd` (function, line 159) `def configure_hostapd(ap_iface, ssid, channel, wpa_passphrase)`
  - `setup_iptables` (function, line 192) `def setup_iptables(ap_iface, ap_ip, net_iface)`
  - `set_speed_limit` (function, line 205) `def set_speed_limit(ap_iface, speed_up, speed_down)`
  - `start_services` (function, line 210) `def start_services(ap_iface, script_path, sslstrip, wireshark, driftnet, tshark)`
  - `cleanup` (function, line 240) `def cleanup()`
  - `signal_handler` (function, line 249) `def signal_handler(sig, frame)`

## modules/legacy/lazynetbios.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 30) `def check_sudo()`
  - `signal_handler` (function, line 38) `def signal_handler(sig, frame)`
  - `scan_netbios` (function, line 45) `def scan_netbios(ip_range)`
  - `check_arp` (function, line 58) `def check_arp(ip)`
  - `check_netbios` (function, line 71) `def check_netbios(ip)`
  - `send_nbns_spoof` (function, line 90) `def send_nbns_spoof(target_ip, target_name, spoof_ip, trans_id)`
  - `generate_ip_range` (function, line 115) `def generate_ip_range(start_ip, end_ip)`

## modules/legacy/lazyntlrelayx.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_hash_file` (function, line 5) `def parse_hash_file(file_path)`
  - `ntlm_relay` (function, line 52) `def ntlm_relay(target_ip, credentials)`

## modules/legacy/lazyopenssh77enum2.py
- Layer: utility
- Doc: CVE-2018-15473 SSH User Enumeration by Leap Security (@LeapSecurity) https://leapsecurity.io Credits: Matthew Daley, Jus
- Language: py
- Symbols:
  - `InvalidUsername` (class, line 14) `class InvalidUsername(Exception)`
  - `add_boolean` (method, line 19) `def add_boolean()`
  - `service_accept` (method, line 30) `def service_accept()`
  - `invalid_username` (method, line 36) `def invalid_username()`
  - `check_user` (method, line 50) `def check_user(username)`
- Depends on: `core/logging.py`

## modules/legacy/lazyphishingai.py
- Layer: presentation
- Language: py
- Symbols:
  - `clean_think` (function, line 28) `def clean_think(texto)`
  - `clean_yaml` (function, line 31) `def clean_yaml(texto)`
  - `truncate_message` (function, line 37) `def truncate_message(message, max_chars)`
  - `configure_logging` (function, line 42) `def configure_logging(debug)`
  - `create_complex_prompt` (function, line 46) `def create_complex_prompt(base_prompt, history, knowledge_base)`
  - `load_knowledge_base` (function, line 101) `def load_knowledge_base(file_path)`
  - `save_knowledge_base` (function, line 110) `def save_knowledge_base(knowledge_base, file_path)`
  - `add_to_knowledge_base` (function, line 117) `def add_to_knowledge_base(prompt, command, file_path)`
  - `get_relevant_knowledge` (function, line 122) `def get_relevant_knowledge(prompt)`
  - `process_prompt_local_yaml` (function, line 132) `def process_prompt_local_yaml(prompt, debug, mode, output_file)`
  - `parse_args` (function, line 192) `def parse_args()`
  - `generate` (function, line 155) `def generate()`
- Depends on: `core/logging.py`
- Imported by: `modules/llm_adapter.py`

## modules/legacy/lazyproxy.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 40) `def check_sudo()`
  - `signal_handler` (function, line 47) `def signal_handler(sig, frame)`
  - `hexdump` (function, line 52) `def hexdump(src, length)`
  - `receive_from` (function, line 63) `def receive_from(connection)`
  - `request_handler` (function, line 77) `def request_handler(buffer)`
  - `response_handler` (function, line 82) `def response_handler(buffer)`
  - `get_ip_from_url` (function, line 87) `def get_ip_from_url(url)`
  - `handle_request` (function, line 104) `def handle_request(client_socket, address)`
  - `start_proxy` (function, line 183) `def start_proxy()`
- Depends on: `modules/colors.py`

## modules/legacy/lazypwn.py
- Layer: utility
- Language: py
- Symbols:
  - `BinaryFinder` (class, line 24) `class BinaryFinder`
  - `BinaryAttacker` (class, line 70) `class BinaryAttacker`
  - `main` (method, line 181) `def main()`
  - `__init__` (method, line 25) `def __init__(self)`
  - `find_suid_binaries` (method, line 28) `def find_suid_binaries(self)`
  - `find_capabilities_binaries` (method, line 36) `def find_capabilities_binaries(self)`
  - `find_executable_binaries` (method, line 44) `def find_executable_binaries(self)`
  - `find_specific_name_binaries` (method, line 52) `def find_specific_name_binaries(self, names)`
  - `process_output` (method, line 61) `def process_output(self, output)`
  - `get_found_binaries` (method, line 67) `def get_found_binaries(self)`
  - `__init__` (method, line 71) `def __init__(self, binary_path)`
  - `analyze_with_ltrace` (method, line 76) `def analyze_with_ltrace(self)`
  - `extract_strings` (method, line 83) `def extract_strings(self)`
  - `prepare_attack` (method, line 90) `def prepare_attack(self)`
  - `exploit_with_pwntools` (method, line 170) `def exploit_with_pwntools(self)`
- Depends on: `cli/commands/pwn.py`

## modules/legacy/lazypwnkit.py
- Layer: utility
- Language: py
- Symbols:
  - `rmrf` (function, line 8) `def rmrf(path)`
  - `create_exploit_environment` (function, line 13) `def create_exploit_environment()`
  - `cleanup_exploit_environment` (function, line 31) `def cleanup_exploit_environment()`
  - `execute_exploit` (function, line 37) `def execute_exploit(cmd)`
  - `main` (function, line 79) `def main()`

## modules/legacy/lazypyautogui.py
- Layer: presentation
- Language: py

## modules/legacy/lazyreversentlmv2.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_hash_file` (function, line 11) `def parse_hash_file(file_path)`
  - `reverse_shell` (function, line 58) `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, callback_port)`
- Depends on: `modules/lazyencoder_decoder.py`

## modules/legacy/lazysearch.py
- Layer: utility
- Language: py
- Symbols:
  - `highlight_term` (function, line 29) `def highlight_term(text, term)`
  - `search_in_parquet` (function, line 32) `def search_in_parquet(term, parquet_files)`
  - `main` (function, line 44) `def main()`

## modules/legacy/lazysearch_bot.py
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 59) `def signal_handler(sig, frame)`
  - `show_help` (function, line 65) `def show_help(message)`
  - `check_api_key` (function, line 69) `def check_api_key()`
  - `configure_logging` (function, line 75) `def configure_logging(debug)`
  - `parse_args` (function, line 79) `def parse_args()`
  - `create_complex_prompt` (function, line 86) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
  - `execute_command` (function, line 109) `def execute_command(command)`
  - `load_knowledge_base` (function, line 112) `def load_knowledge_base(file_path)`
  - `save_knowledge_base` (function, line 118) `def save_knowledge_base(knowledge_base, file_path)`
  - `add_to_knowledge_base` (function, line 122) `def add_to_knowledge_base(prompt, command, file_path)`
  - `get_relevant_knowledge` (function, line 127) `def get_relevant_knowledge(prompt)`
  - `transform_knowledge_base` (function, line 135) `def transform_knowledge_base(client)`
  - `main` (function, line 158) `def main()`
- Depends on: `core/logging.py`

## modules/legacy/lazyseo.py
- Layer: utility
- Language: py
- Symbols:
  - `Config` (class, line 13) `class Config`
  - `load_payload` (method, line 22) `def load_payload()`
  - `make_request` (method, line 27) `def make_request(url, retries, timeout)`
  - `results` (method, line 48) `def results(file)`
  - `crawl` (method, line 56) `def crawl(url)`
  - `ffuf` (method, line 65) `def ffuf()`
  - `analyze_seo` (method, line 75) `def analyze_seo(url)`
  - `__init__` (method, line 14) `def __init__(self, config_dict)`
  - `__getitem__` (method, line 19) `def __getitem__(self, key)`
- Depends on: `modules/colors.py`

## modules/legacy/lazysmbrelay.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 15) `def check_sudo()`
  - `start_smb_server` (function, line 27) `def start_smb_server()`
  - `start_smb_relay` (function, line 35) `def start_smb_relay(target, command)`
  - `CustomSMBRelayServer` (class, line 41) `class CustomSMBRelayServer(SMBRelayServer)`
  - `__init__` (method, line 42) `def __init__(self)`
  - `handleData` (method, line 46) `def handleData(self)`
  - `execute_remote_command` (method, line 50) `def execute_remote_command(self)`
- Depends on: `core/logging.py`, `utils.py`

## modules/legacy/lazysniff.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 41) `def check_sudo()`
  - `signal_handler` (function, line 50) `def signal_handler(sig, frame)`
  - `setup_curses` (function, line 57) `def setup_curses()`
  - `restore_curses` (function, line 66) `def restore_curses(stdscr)`
  - `show_banner` (function, line 73) `def show_banner(stdscr, banner)`
  - `process_packet` (function, line 80) `def process_packet(packet, packets, win_top, win_bottom)`
  - `analyze_packet` (function, line 90) `def analyze_packet(packet)`
  - `capture_packets` (function, line 112) `def capture_packets(interface, count, filter, pcap_file, packets, win_top, win_bottom)`
  - `main_curses` (function, line 118) `def main_curses(stdscr, packets, interface, count, filter, pcap_file)`
  - `parse_arguments` (function, line 188) `def parse_arguments()`
  - `main` (function, line 197) `def main()`

## modules/legacy/lazysqli.py
- Layer: utility
- Doc: AUTHOR: jahman EDITED BY grisun0
- Language: py
- Symbols:
  - `send_payload` (function, line 13) `def send_payload(payload, url, s, sql_time)`
  - `sqli_dichotomie` (function, line 30) `def sqli_dichotomie(payload_brute, offset, url, s, sql_time)`
  - `sqli_thread` (function, line 51) `def sqli_thread(url, db, table, col, sql_time, threads)`
  - `main` (function, line 89) `def main(args)`

## modules/legacy/lazyssh.py
- Layer: utility
- Language: py
- Symbols:
  - `execute` (function, line 13) `def execute(hostname, port, command)`
- Depends on: `core/logging.py`

## modules/legacy/lazyvsftp.py
- Layer: utility
- Language: py
- Symbols:
  - `connect` (function, line 7) `def connect(host, port)`
  - `exploit` (function, line 16) `def exploit(host, port)`
  - `handle_backdoor` (function, line 61) `def handle_backdoor(s)`
- Depends on: `cli/commands/pwn.py`

## modules/legacy/lazywerkzeug.py
- Layer: utility
- Language: py

## modules/legacy/sql.py
- Layer: utility
- Language: py
- Symbols:
  - `def_handler` (function, line 8) `def def_handler(sig, frame)`
  - `getUnicode` (function, line 15) `def getUnicode(sqli)`
  - `makeRequest` (function, line 22) `def makeRequest(sqli_modified)`
- Depends on: `cli/commands/pwn.py`
