# Symbols (page 6 of 38)
Previous: [SYMBOLS_p5.md](SYMBOLS_p5.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `ephemeral_enabled` | method | `cli/toast_bus.py:732` | `def ephemeral_enabled(payload, config)` |
| `flush` | method | `cli/toast_bus.py:164` | `def flush(self)` |
| `format` | method | `cli/toast_bus.py:324` | `def format(self, event)` |
| `format_ephemeral` | method | `cli/toast_bus.py:363` | `def format_ephemeral(self, event)` |
| `format_many` | method | `cli/toast_bus.py:417` | `def format_many(self, events, width)` |
| `format_prominent` | method | `cli/toast_bus.py:346` | `def format_prominent(self, event)` |
| `get` | method | `cli/toast_bus.py:148` | `def get(self, name)` |
| `is_prominent` | method | `cli/toast_bus.py:336` | `def is_prominent(self, event)` |
| `mark_all_seen` | method | `cli/toast_bus.py:551` | `def mark_all_seen(self)` |
| `path` | method | `cli/toast_bus.py:144` | `def path(self)` |
| `read_recent_toasts` | method | `cli/toast_bus.py:823` | `def read_recent_toasts(sessions_dir, limit, config)` |
| `read_unseen` | method | `cli/toast_bus.py:221` | `def read_unseen(self, name, start_offset)` |
| `render` | method | `cli/toast_bus.py:522` | `def render(self, enabled)` |
| `render_ephemeral` | method | `cli/toast_bus.py:558` | `def render_ephemeral(self, enabled, duration)` |
| `render_ephemeral_toasts` | method | `cli/toast_bus.py:748` | `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` |
| `render_toasts` | method | `cli/toast_bus.py:708` | `def render_toasts(payload, sessions_dir, console, bus_factory)` |
| `reset` | method | `cli/toast_bus.py:159` | `def reset(self)` |
| `root` | method | `cli/toast_bus.py:217` | `def root(self)` |
| `set` | method | `cli/toast_bus.py:153` | `def set(self, name, offset)` |
| `toasts_enabled` | method | `cli/toast_bus.py:656` | `def toasts_enabled(payload, config)` |
| `_cycle` | function | `cli/tui_theme.py:65` | `def _cycle(payload, direction)` |
| `_format_listing` | function | `cli/tui_theme.py:45` | `def _format_listing(current)` |
| `_set_theme` | function | `cli/tui_theme.py:30` | `def _set_theme(payload, name)` |
| `run` | function | `cli/tui_theme.py:87` | `def run(args, payload, save)` |
| `TutorialConfig` | class | `cli/tutorial.py:76` | `class TutorialConfig` |
| `is_done` | method | `cli/tutorial.py:83` | `def is_done(config)` |
| `mark_done` | method | `cli/tutorial.py:89` | `def mark_done(config)` |
| `render_header` | method | `cli/tutorial.py:96` | `def render_header()` |
| `render_phase_table` | method | `cli/tutorial.py:113` | `def render_phase_table()` |
| `run` | method | `cli/tutorial.py:185` | `def run(params, command_runner)` |
| `run_step` | method | `cli/tutorial.py:128` | `def run_step(index, command, description, why, params, command_runner)` |
| `BinarySpec` | class | `cli/wizard.py:90` | `class BinarySpec` |
| `BinaryStatus` | class | `cli/wizard.py:141` | `class BinaryStatus` |
| `ReadinessItem` | class | `cli/wizard.py:150` | `class ReadinessItem` |
| `WizardResult` | class | `cli/wizard.py:160` | `class WizardResult` |
| `_ask_device` | method | `cli/wizard.py:537` | `def _ask_device(current)` |
| `_ask_domain` | method | `cli/wizard.py:515` | `def _ask_domain(current)` |
| `_ask_lhost` | method | `cli/wizard.py:484` | `def _ask_lhost(current)` |
| `_ask_llm` | method | `cli/wizard.py:621` | `def _ask_llm(params)` |
| `_ask_marketplace_config` | method | `cli/wizard.py:852` | `def _ask_marketplace_config()` |
| `_ask_operator_login` | method | `cli/wizard.py:724` | `def _ask_operator_login(params)` |
| `_ask_os_id` | method | `cli/wizard.py:563` | `def _ask_os_id(current)` |
| `_ask_rhost` | method | `cli/wizard.py:457` | `def _ask_rhost(current)` |
| `_ask_wordlists` | method | `cli/wizard.py:692` | `def _ask_wordlists(params)` |
| `_build_readiness` | method | `cli/wizard.py:875` | `def _build_readiness(params)` |
| `_check` | method | `cli/wizard.py:878` | `def _check(key, label, hint)` |
| `_check_llm` | method | `cli/wizard.py:887` | `def _check_llm()` |
| `_collect_values` | method | `cli/wizard.py:419` | `def _collect_values(params)` |
| `_detect_device` | method | `cli/wizard.py:1120` | `def _detect_device()` |
| `_detect_lhost` | method | `cli/wizard.py:1098` | `def _detect_lhost()` |
| `_find_seclists_root` | method | `cli/wizard.py:1133` | `def _find_seclists_root()` |
| `_group_by_category` | method | `cli/wizard.py:988` | `def _group_by_category(statuses)` |
| `_info` | method | `cli/wizard.py:1169` | `def _info(msg)` |
| `_is_default` | method | `cli/wizard.py:322` | `def _is_default(value)` |
| `_is_weak` | method | `cli/wizard.py:325` | `def _is_weak(value)` |
| `_mask_secret` | method | `cli/wizard.py:606` | `def _mask_secret(value)` |
| `_normalize_provider_answer` | method | `cli/wizard.py:585` | `def _normalize_provider_answer(raw)` |
| `_ok` | method | `cli/wizard.py:1161` | `def _ok(msg)` |
| `_ping` | method | `cli/wizard.py:1141` | `def _ping(ip)` |
| `_print_binary_report` | method | `cli/wizard.py:997` | `def _print_binary_report(statuses)` |
| `_print_glossary_panel` | method | `cli/wizard.py:379` | `def _print_glossary_panel()` |
| `_print_header` | method | `cli/wizard.py:364` | `def _print_header()` |
| `_print_long_help` | method | `cli/wizard.py:412` | `def _print_long_help(key)` |
| `_print_next_steps` | method | `cli/wizard.py:1035` | `def _print_next_steps(params)` |
| `_print_readiness` | method | `cli/wizard.py:927` | `def _print_readiness(items)` |
| `_print_secret_rotation` | method | `cli/wizard.py:348` | `def _print_secret_rotation(rotated)` |
| `_print_validation_summary` | method | `cli/wizard.py:1059` | `def _print_validation_summary(params)` |
| `_prompt` | method | `cli/wizard.py:1154` | `def _prompt(message)` |
| `_rotate_default_secrets` | method | `cli/wizard.py:300` | `def _rotate_default_secrets(params, save)` |
| `_spec_long_help` | method | `cli/wizard.py:404` | `def _spec_long_help(key)` |
| `_warn` | method | `cli/wizard.py:1165` | `def _warn(msg)` |
| `_wizard_login_flow` | method | `cli/wizard.py:786` | `def _wizard_login_flow()` |
| `_wizard_register_flow` | method | `cli/wizard.py:809` | `def _wizard_register_flow()` |
| `check_binaries` | method | `cli/wizard.py:947` | `def check_binaries(specs, which)` |
| `run` | method | `cli/wizard.py:169` | `def run(params, save)` |
| `run_non_interactive` | method | `cli/wizard.py:234` | `def run_non_interactive(params, save, values)` |
| `WizardScope` | class | `cli/wizard_scope.py:31` | `class WizardScope` |
| `WizardScopeConfig` | class | `cli/wizard_scope.py:17` | `class WizardScopeConfig` |
| `parse_scope` | method | `cli/wizard_scope.py:38` | `def parse_scope(tokens, config)` |
| `status_rows` | method | `cli/wizard_scope.py:64` | `def status_rows(params)` |
| `exploit` | function | `contrib/legacy/lazy_http_bof.py:29` | `def exploit(target, port, payload)` |
| `genHeader` | function | `contrib/legacy/lazy_http_bof.py:6` | `def genHeader(raw)` |
| `check_sudo` | function | `contrib/legacy/lazy_packet_image_sniffer.py:23` | `def check_sudo()` |
| `choose_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:49` | `def choose_interface(interfaces)` |
| `daemonize` | function | `contrib/legacy/lazy_packet_image_sniffer.py:192` | `def daemonize()` |
| `get_ip_addresses` | function | `contrib/legacy/lazy_packet_image_sniffer.py:65` | `def get_ip_addresses(interface)` |
| `get_subnet_from_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:61` | `def get_subnet_from_interface(interface)` |
| `handle_packet` | function | `contrib/legacy/lazy_packet_image_sniffer.py:111` | `def handle_packet(packet)` |
| `list_interfaces` | function | `contrib/legacy/lazy_packet_image_sniffer.py:31` | `def list_interfaces()` |
| `run` | function | `contrib/legacy/lazy_packet_image_sniffer.py:187` | `def run()` |
| `save_image` | function | `contrib/legacy/lazy_packet_image_sniffer.py:161` | `def save_image(src_ip, end_idx)` |
| `build_llm_prompt` | function | `contrib/legacy/lazyaddon_creator.py:98` | `def build_llm_prompt(meta, readme, root_files)` |
| `build_yaml` | function | `contrib/legacy/lazyaddon_creator.py:300` | `def build_yaml(data, repo_url)` |
| `extract_json_from_response` | function | `contrib/legacy/lazyaddon_creator.py:164` | `def extract_json_from_response(text)` |
| `fallback_yaml_data` | function | `contrib/legacy/lazyaddon_creator.py:276` | `def fallback_yaml_data(meta, readme, root_files)` |
| `fetch_readme` | function | `contrib/legacy/lazyaddon_creator.py:73` | `def fetch_readme(owner, repo)` |
| `fetch_repo_metadata` | function | `contrib/legacy/lazyaddon_creator.py:68` | `def fetch_repo_metadata(owner, repo)` |
| `fetch_root_files` | function | `contrib/legacy/lazyaddon_creator.py:85` | `def fetch_root_files(owner, repo)` |
| `github_api_get` | function | `contrib/legacy/lazyaddon_creator.py:58` | `def github_api_get(owner, repo, endpoint)` |
| `heuristic_execute_command` | function | `contrib/legacy/lazyaddon_creator.py:211` | `def heuristic_execute_command(name, root_files, language)` |
| `heuristic_install_command` | function | `contrib/legacy/lazyaddon_creator.py:192` | `def heuristic_install_command(root_files, language)` |
| `heuristic_params` | function | `contrib/legacy/lazyaddon_creator.py:245` | `def heuristic_params(name, readme, root_files)` |
| `main` | function | `contrib/legacy/lazyaddon_creator.py:357` | `def main()` |
| `parse_github_url` | function | `contrib/legacy/lazyaddon_creator.py:49` | `def parse_github_url(url)` |
| `save_yaml` | function | `contrib/legacy/lazyaddon_creator.py:336` | `def save_yaml(addon, output_dir)` |
| `check_sudo` | function | `contrib/legacy/lazyarpspoofing.py:27` | `def check_sudo()` |
| `disable_ip_forward` | function | `contrib/legacy/lazyarpspoofing.py:38` | `def disable_ip_forward()` |
| `enable_ip_forward` | function | `contrib/legacy/lazyarpspoofing.py:35` | `def enable_ip_forward()` |
| `get_local_ip` | function | `contrib/legacy/lazyarpspoofing.py:41` | `def get_local_ip(ifname)` |
| `get_mac` | function | `contrib/legacy/lazyarpspoofing.py:49` | `def get_mac(ip, device, retries, timeout)` |
| `main` | function | `contrib/legacy/lazyarpspoofing.py:80` | `def main()` |
| `spoofer` | function | `contrib/legacy/lazyarpspoofing.py:69` | `def spoofer(target, spoofed, device)` |
| `generate_key_iv` | function | `contrib/legacy/lazybinenc.py:12` | `def generate_key_iv(sessions_path)` |
| `main` | function | `contrib/legacy/lazybinenc.py:54` | `def main()` |
| `decrypt` | function | `contrib/legacy/lazybotcli.py:36` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazybotcli.py:30` | `def encrypt(plaintext, key)` |
| `main` | function | `contrib/legacy/lazybotcli.py:42` | `def main()` |
| `Keylogger` | class | `contrib/legacy/lazybotnet.py:89` | `class Keylogger` |
| `__init__` | method | `contrib/legacy/lazybotnet.py:90` | `def __init__(self, key, log_file)` |
| `add_to_botnet` | function | `contrib/legacy/lazybotnet.py:58` | `def add_to_botnet(ip, port, botnet_file)` |
| `clean_botnet` | function | `contrib/legacy/lazybotnet.py:62` | `def clean_botnet(ip, port, botnet_file)` |
| `create_shortcut` | method | `contrib/legacy/lazybotnet.py:136` | `def create_shortcut(self, script_path, shortcut_path)` |
| `decrypt` | function | `contrib/legacy/lazybotnet.py:52` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazybotnet.py:46` | `def encrypt(plaintext, key)` |
| `get_log` | method | `contrib/legacy/lazybotnet.py:110` | `def get_log(self)` |
| `handle_client` | method | `contrib/legacy/lazybotnet.py:144` | `def handle_client(conn, key, botnet_file, log_file)` |
| `on_press` | method | `contrib/legacy/lazybotnet.py:95` | `def on_press(self, key)` |
| `run` | method | `contrib/legacy/lazybotnet.py:120` | `def run(self)` |
| `save_log` | method | `contrib/legacy/lazybotnet.py:113` | `def save_log(self)` |
| `send_to_botnet` | function | `contrib/legacy/lazybotnet.py:71` | `def send_to_botnet(cmd, key, botnet_file)` |
| `setup_persistence` | method | `contrib/legacy/lazybotnet.py:125` | `def setup_persistence(self)` |
| `start` | method | `contrib/legacy/lazybotnet.py:106` | `def start(self)` |
| `start_server` | method | `contrib/legacy/lazybotnet.py:182` | `def start_server(host, port, key, botnet_file, log_file)` |
| `RTSPScanner` | class | `contrib/legacy/lazycam.py:32` | `class RTSPScanner` |
| `__init__` | method | `contrib/legacy/lazycam.py:33` | `def __init__(self, verbose, wspace)` |
| `addCameras` | method | `contrib/legacy/lazycam.py:149` | `def addCameras(self)` |
| `cla` | method | `contrib/legacy/lazycam.py:212` | `def cla()` |
| `delCameras` | method | `contrib/legacy/lazycam.py:136` | `def delCameras(self)` |
| `main` | method | `contrib/legacy/lazycam.py:257` | `def main()` |
| `resizeImg` | method | `contrib/legacy/lazycam.py:68` | `def resizeImg(self, img, output, height, ratio, fmt)` |
| `run` | method | `contrib/legacy/lazycam.py:49` | `def run(self)` |
| `scanner` | method | `contrib/legacy/lazycam.py:83` | `def scanner(self)` |
| `splitCSV` | method | `contrib/legacy/lazycam.py:77` | `def splitCSV(self, csv)` |
| `_load_payload_kv` | function | `contrib/legacy/lazydeepseekcli.py:50` | `def _load_payload_kv()` |
| `_load_report_context` | function | `contrib/legacy/lazydeepseekcli.py:68` | `def _load_report_context()` |
| `_ollama_stream` | function | `contrib/legacy/lazydeepseekcli.py:223` | `def _ollama_stream(prompt_text, mode)` |
| `_prompt_redteam` | function | `contrib/legacy/lazydeepseekcli.py:79` | `def _prompt_redteam(base_prompt, history, knowledge_base)` |
| `_prompt_report` | function | `contrib/legacy/lazydeepseekcli.py:118` | `def _prompt_report(base_prompt, history, knowledge_base)` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:179` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `configure_logging` | function | `contrib/legacy/lazydeepseekcli.py:45` | `def configure_logging(debug)` |
| `generate` | function | `contrib/legacy/lazydeepseekcli.py:231` | `def generate()` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazydeepseekcli.py:185` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:167` | `def load_knowledge_base(file_path)` |
| `parse_args` | function | `contrib/legacy/lazydeepseekcli.py:271` | `def parse_args()` |
| `process_prompt_local` | function | `contrib/legacy/lazydeepseekcli.py:255` | `def process_prompt_local(prompt, debug, mode)` |
| `process_prompt_localreport` | function | `contrib/legacy/lazydeepseekcli.py:263` | `def process_prompt_localreport(prompt, debug, mode)` |
| `save_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:174` | `def save_knowledge_base(knowledge_base, file_path)` |
| `transform_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:193` | `def transform_knowledge_base(prompt_builder)` |
| `truncate_message` | function | `contrib/legacy/lazydeepseekcli.py:41` | `def truncate_message(message, max_chars)` |
| `X64Disassembler` | class | `contrib/legacy/lazydisassebler.py:24` | `class X64Disassembler` |
| `__init__` | method | `contrib/legacy/lazydisassebler.py:34` | `def __init__(self)` |
| `disassemble` | method | `contrib/legacy/lazydisassebler.py:305` | `def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point)` |
| `get_operand_str` | method | `contrib/legacy/lazydisassebler.py:212` | `def get_operand_str(self, mod, rm, rex, bytes_data, offset)` |
| `main` | method | `contrib/legacy/lazydisassebler.py:489` | `def main()` |
| `parse_modrm` | method | `contrib/legacy/lazydisassebler.py:135` | `def parse_modrm(self, modrm, rex)` |
| `parse_sib` | method | `contrib/legacy/lazydisassebler.py:173` | `def parse_sib(self, sib, rex)` |
| `read_elf_header` | method | `contrib/legacy/lazydisassebler.py:79` | `def read_elf_header(self, data)` |
| `check_sudo` | function | `contrib/legacy/lazyftpsniff.py:21` | `def check_sudo()` |
| `main` | function | `contrib/legacy/lazyftpsniff.py:69` | `def main()` |
| `parse_arguments` | function | `contrib/legacy/lazyftpsniff.py:42` | `def parse_arguments()` |
| `signal_handler` | function | `contrib/legacy/lazyftpsniff.py:34` | `def signal_handler(sig, frame)` |
| `sniffer_ftp` | function | `contrib/legacy/lazyftpsniff.py:56` | `def sniffer_ftp(pkt)` |
| `SamsungKnoxExploitServer` | class | `contrib/legacy/lazygalazy.py:8` | `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)` |
| `apk_bytes` | method | `contrib/legacy/lazygalazy.py:33` | `def apk_bytes(self)` |
| `do_GET` | method | `contrib/legacy/lazygalazy.py:11` | `def do_GET(self)` |
| `exploit_js` | method | `contrib/legacy/lazygalazy.py:49` | `def exploit_js(self)` |
| `launch_html` | method | `contrib/legacy/lazygalazy.py:36` | `def launch_html(self)` |
| `main` | method | `contrib/legacy/lazygalazy.py:97` | `def main()` |
| `rand_word` | method | `contrib/legacy/lazygalazy.py:93` | `def rand_word(self)` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazygptcli.py:128` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `check_api_key` | function | `contrib/legacy/lazygptcli.py:77` | `def check_api_key()` |
| `cleanup_temp_files` | function | `contrib/legacy/lazygptcli.py:164` | `def cleanup_temp_files()` |
| `configure_logging` | function | `contrib/legacy/lazygptcli.py:83` | `def configure_logging(debug)` |
| `create_complex_prompt` | function | `contrib/legacy/lazygptcli.py:94` | `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)` |
| `execute_command` | function | `contrib/legacy/lazygptcli.py:108` | `def execute_command(command)` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazygptcli.py:133` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazygptcli.py:118` | `def load_knowledge_base(file_path)` |
| `main` | function | `contrib/legacy/lazygptcli.py:177` | `def main()` |
| `parse_args` | function | `contrib/legacy/lazygptcli.py:87` | `def parse_args()` |
| `save_knowledge_base` | function | `contrib/legacy/lazygptcli.py:124` | `def save_knowledge_base(knowledge_base, file_path)` |
| `show_help` | function | `contrib/legacy/lazygptcli.py:73` | `def show_help(message)` |
| `signal_handler` | function | `contrib/legacy/lazygptcli.py:66` | `def signal_handler(sig, frame)` |
| `transform_knowledge_base` | function | `contrib/legacy/lazygptcli.py:141` | `def transform_knowledge_base(client)` |
| `_add_to_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:76` | `def _add_to_knowledge_base(prompt, response, file_path)` |
| `_configure_logging` | function | `contrib/legacy/lazygptcli_unified.py:57` | `def _configure_logging(debug)` |
| `_deepseek_fallback` | function | `contrib/legacy/lazygptcli_unified.py:392` | `def _deepseek_fallback(prompt)` |
| `_get_relevant_knowledge` | function | `contrib/legacy/lazygptcli_unified.py:82` | `def _get_relevant_knowledge(prompt, file_path)` |
| `_groq_chat` | function | `contrib/legacy/lazygptcli_unified.py:115` | `def _groq_chat(client, messages, model, max_tokens)` |
| `_load_event_config` | function | `contrib/legacy/lazygptcli_unified.py:147` | `def _load_event_config()` |
| `_load_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:62` | `def _load_knowledge_base(file_path)` |
| `_load_payload_kv` | function | `contrib/legacy/lazygptcli_unified.py:129` | `def _load_payload_kv()` |
| `_process_groq` | function | `contrib/legacy/lazygptcli_unified.py:287` | `def _process_groq(client, prompt, debug, prompt_template, kb_file, model)` |
| `_prompt_adversary` | function | `contrib/legacy/lazygptcli_unified.py:190` | `def _prompt_adversary(base_prompt, history, knowledge_base)` |
| `_prompt_general` | function | `contrib/legacy/lazygptcli_unified.py:206` | `def _prompt_general(base_prompt, history, knowledge_base)` |
| `_prompt_oneliner` | function | `contrib/legacy/lazygptcli_unified.py:159` | `def _prompt_oneliner(base_prompt, history, knowledge_base)` |
| `_prompt_redop` | function | `contrib/legacy/lazygptcli_unified.py:267` | `def _prompt_redop(base_prompt, history, knowledge_base)` |
| `_prompt_script` | function | `contrib/legacy/lazygptcli_unified.py:175` | `def _prompt_script(base_prompt, history, knowledge_base)` |
| `_prompt_search` | function | `contrib/legacy/lazygptcli_unified.py:225` | `def _prompt_search(base_prompt, history, knowledge_base)` |
| `_prompt_task` | function | `contrib/legacy/lazygptcli_unified.py:254` | `def _prompt_task(base_prompt, history, knowledge_base)` |
| `_prompt_vuln` | function | `contrib/legacy/lazygptcli_unified.py:239` | `def _prompt_vuln(base_prompt, history, knowledge_base)` |
| `_ret_model` | function | `contrib/legacy/lazygptcli_unified.py:45` | `def _ret_model()` |
| `_save_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:70` | `def _save_knowledge_base(knowledge_base, file_path)` |
| `_transform_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:95` | `def _transform_knowledge_base(client, kb_file, improved_file)` |
| `process_prompt` | function | `contrib/legacy/lazygptcli_unified.py:318` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `contrib/legacy/lazygptcli_unified.py:328` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `contrib/legacy/lazygptcli_unified.py:333` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `contrib/legacy/lazygptcli_unified.py:382` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `contrib/legacy/lazygptcli_unified.py:323` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `contrib/legacy/lazygptcli_unified.py:341` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `contrib/legacy/lazygptcli_unified.py:346` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `contrib/legacy/lazygptcli_unified.py:356` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `truncate_message` | function | `contrib/legacy/lazygptcli_unified.py:53` | `def truncate_message(message, max_chars)` |
| `Server` | class | `contrib/legacy/lazyhoneypot.py:60` | `class Server(ServerInterface)` |
| `__init__` | method | `contrib/legacy/lazyhoneypot.py:61` | `def __init__(self)` |
| `alert_admin` | method | `contrib/legacy/lazyhoneypot.py:147` | `def alert_admin(message)` |
| `analyze_traffic` | method | `contrib/legacy/lazyhoneypot.py:136` | `def analyze_traffic()` |
| `check_auth_password` | method | `contrib/legacy/lazyhoneypot.py:69` | `def check_auth_password(self, username, password)` |
| `check_channel_request` | method | `contrib/legacy/lazyhoneypot.py:64` | `def check_channel_request(self, kind, chanid)` |
| `generate_rsa_key` | function | `contrib/legacy/lazyhoneypot.py:56` | `def generate_rsa_key(key_filename)` |
| `handle_connection` | method | `contrib/legacy/lazyhoneypot.py:74` | `def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir)` |
| `handle_file_download` | method | `contrib/legacy/lazyhoneypot.py:110` | `def handle_file_download(command, downloads_dir, downloads_log)` |
| `log_command` | method | `contrib/legacy/lazyhoneypot.py:128` | `def log_command(command, commands_log)` |
| `log_downloaded_file` | method | `contrib/legacy/lazyhoneypot.py:132` | `def log_downloaded_file(filename, url, downloads_log)` |
| `main` | method | `contrib/legacy/lazyhoneypot.py:165` | `def main()` |
| `parse_args` | function | `contrib/legacy/lazyhoneypot.py:34` | `def parse_args()` |
| `process_packet` | method | `contrib/legacy/lazyhoneypot.py:137` | `def process_packet(packet)` |
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
| `main` | method | `contrib/legacy/lazyllmchat.py:309` | `def main()` |
| `no_history_init` | method | `contrib/legacy/lazyllmchat.py:38` | `def no_history_init(self_)` |
| `render` | method | `contrib/legacy/lazyllmchat.py:208` | `def render(self)` |
| `run` | method | `contrib/legacy/lazyllmchat.py:280` | `def run(self, initial_query)` |
| `target` | method | `contrib/legacy/lazyllmchat.py:70` | `def target()` |
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
| `add_boolean` | method | `contrib/legacy/lazyopenssh77enum2.py:19` | `def add_boolean()` |
| `check_user` | method | `contrib/legacy/lazyopenssh77enum2.py:50` | `def check_user(username)` |
| `invalid_username` | method | `contrib/legacy/lazyopenssh77enum2.py:36` | `def invalid_username()` |
| `service_accept` | method | `contrib/legacy/lazyopenssh77enum2.py:30` | `def service_accept()` |
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
| `main` | method | `contrib/legacy/lazypwn.py:181` | `def main()` |
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
| `analyze_seo` | method | `contrib/legacy/lazyseo.py:76` | `def analyze_seo(url)` |
| `crawl` | method | `contrib/legacy/lazyseo.py:57` | `def crawl(url)` |
| `ffuf` | method | `contrib/legacy/lazyseo.py:66` | `def ffuf()` |
| `load_payload` | method | `contrib/legacy/lazyseo.py:23` | `def load_payload()` |
| `make_request` | method | `contrib/legacy/lazyseo.py:28` | `def make_request(url, retries, timeout)` |
| `results` | method | `contrib/legacy/lazyseo.py:49` | `def results(file)` |
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
| `_extract_key` | method | `core/api_authz.py:393` | `def _extract_key(request_obj)` |
| `_generate_token_bytes` | method | `core/api_authz.py:147` | `def _generate_token_bytes(nbytes)` |
| `_grace_deadline` | method | `core/api_authz.py:197` | `def _grace_deadline(self, retired_at)` |
| `_hash_secret` | method | `core/api_authz.py:137` | `def _hash_secret(secret)` |
| `_prune_record` | method | `core/api_authz.py:343` | `def _prune_record(self, key_hash)` |
| `_prune_retired` | method | `core/api_authz.py:201` | `def _prune_retired(self, records)` |
| `_read` | method | `core/api_authz.py:180` | `def _read(self)` |
| `_touch_last_used` | method | `core/api_authz.py:351` | `def _touch_last_used(self, key_hash)` |
| `_verify_secret` | method | `core/api_authz.py:142` | `def _verify_secret(secret, stored_hash)` |
| `_write` | method | `core/api_authz.py:191` | `def _write(self, data)` |
| `config` | method | `core/api_authz.py:176` | `def config(self)` |
| `create_api_token` | method | `core/api_authz.py:440` | `def create_api_token(store, tenant_id, label, permissions, expires_in_days)` |
| `create_key` | method | `core/api_authz.py:238` | `def create_key(self, tenant_id, label, permissions, expires_in_days)` |
| `decorated` | method | `core/api_authz.py:407` | `def decorated()` |
| `decorator` | method | `core/api_authz.py:405` | `def decorator(f)` |
| `find_by_hash` | method | `core/api_authz.py:229` | `def find_by_hash(self, key_hash)` |
| `from_dict` | method | `core/api_authz.py:107` | `def from_dict(cls, data)` |
| `has_all_permissions` | method | `core/api_authz.py:130` | `def has_all_permissions(self, permissions)` |
| `has_permission` | method | `core/api_authz.py:127` | `def has_permission(self, permission)` |
| `is_expired` | method | `core/api_authz.py:119` | `def is_expired(self)` |
| `is_retired` | method | `core/api_authz.py:124` | `def is_retired(self)` |
| `list_keys` | method | `core/api_authz.py:217` | `def list_keys(self, tenant_id)` |
| `require_api_auth` | method | `core/api_authz.py:365` | `def require_api_auth(store, permissions, require_tenant)` |
| `revoke_key` | method | `core/api_authz.py:273` | `def revoke_key(self, label, tenant_id)` |
| `rotate_key` | method | `core/api_authz.py:309` | `def rotate_key(self, label, tenant_id)` |
| `to_dict` | method | `core/api_authz.py:94` | `def to_dict(self)` |
| `validate_key` | method | `core/api_authz.py:287` | `def validate_key(self, plaintext)` |
| `CommandBridge` | class | `core/command_bridge.py:15` | `class CommandBridge` |
| `__init__` | method | `core/command_bridge.py:18` | `def __init__(self)` |
| `_ensure_shell` | method | `core/command_bridge.py:34` | `def _ensure_shell(self)` |
| `error` | method | `core/command_bridge.py:30` | `def error(self)` |
| `execute` | method | `core/command_bridge.py:110` | `def execute(self, command)` |
| `get_bridge` | method | `core/command_bridge.py:126` | `def get_bridge()` |
| `one_cmd` | method | `core/command_bridge.py:89` | `def one_cmd(self, command)` |
| `onecmd` | method | `core/command_bridge.py:65` | `def onecmd(self, command)` |
| `ready` | method | `core/command_bridge.py:25` | `def ready(self)` |
| `Config` | class | `core/config.py:195` | `class Config` |
| `__getattr__` | method | `core/config.py:217` | `def __getattr__(self, name)` |
| `__getitem__` | method | `core/config.py:220` | `def __getitem__(self, key)` |
| `__init__` | method | `core/config.py:208` | `def __init__(self, config_dict, sessions_dir)` |
| `_apply_env_overrides` | function | `core/config.py:70` | `def _apply_env_overrides(payload)` |
| `_coerce_env_value` | function | `core/config.py:103` | `def _coerce_env_value(raw, existing)` |
| `_collect_validation_warnings` | function | `core/config.py:171` | `def _collect_validation_warnings(payload)` |
| `_load_raw_payload` | method | `core/config.py:293` | `def _load_raw_payload(path)` |
| `_log_config_change` | function | `core/config.py:146` | `def _log_config_change(key, old_value, new_value)` |
| `_mask_if_sensitive` | function | `core/config.py:128` | `def _mask_if_sensitive(key, value)` |
| `_migrate_keys` | method | `core/config.py:238` | `def _migrate_keys(config_dict)` |
| `as_params` | method | `core/config.py:223` | `def as_params(self)` |
| `load_and_validate` | method | `core/config.py:334` | `def load_and_validate(path)` |
| `load_payload` | method | `core/config.py:316` | `def load_payload(path)` |
| `overridden_keys` | method | `core/config.py:233` | `def overridden_keys(self)` |
| `resolve_aes_key` | method | `core/config.py:250` | `def resolve_aes_key(config_dict)` |
| `save_payload` | method | `core/config.py:385` | `def save_payload(payload, path)` |
| `_emit` | function | `core/console.py:208` | `def _emit(line)` |
| `_paint` | function | `core/console.py:114` | `def _paint(code, text)` |
| `_sanitize` | function | `core/console.py:93` | `def _sanitize(text)` |
| `colors_enabled` | function | `core/console.py:98` | `def colors_enabled()` |

Next: [SYMBOLS_p7.md](SYMBOLS_p7.md)
