# API (page 5 of 21)
Previous: [API_p4.md](API_p4.md)

## cli/toast_bus.py
Depends on: `cli/themes.py`, `core/console.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/ux.py`, `cli/dashboard_tui.py`, `lazyown.py`, `tests/test_lazy_parity.py`, `tests/test_toast_bus.py`
- `ToastState.__init__` (method) `cli/toast_bus.py:129` `def __init__(self, config, root)` -- Bind to config and resolve the on-disk state path.
- `ToastState.path` (method) `cli/toast_bus.py:144` `def path(self)` -- Return the resolved state-file path.
- `ToastState.get` (method) `cli/toast_bus.py:148` `def get(self, name)` -- Return the persisted offset for ``name`` or 0.
- `ToastState.set` (method) `cli/toast_bus.py:153` `def set(self, name, offset)` -- Record ``offset`` for ``name`` in memory.
- `ToastState.reset` (method) `cli/toast_bus.py:159` `def reset(self)` -- Forget every persisted offset (force replay on next read).
- `ToastState.flush` (method) `cli/toast_bus.py:164` `def flush(self)` -- Persist the current offsets atomically.
- `ToastReader.__init__` (method) `cli/toast_bus.py:206` `def __init__(self, config, root)` -- Bind to config and resolve the events root directory.
- `ToastReader.root` (method) `cli/toast_bus.py:217` `def root(self)` -- Return the resolved events root directory.
- `ToastReader.read_unseen` (method) `cli/toast_bus.py:221` `def read_unseen(self, name, start_offset)` -- Return events emitted past ``start_offset`` plus the new end offset.
- `ToastFormatter.__init__` (method) `cli/toast_bus.py:319` `def __init__(self, config, theme)` -- Bind to config and the active theme.
- `ToastFormatter.format` (method) `cli/toast_bus.py:324` `def format(self, event)` -- Return a single themed line for ``event``.
- `ToastFormatter.is_prominent` (method) `cli/toast_bus.py:336` `def is_prominent(self, event)` -- Return True when an event deserves a full toastr panel.
- `ToastFormatter.format_prominent` (method) `cli/toast_bus.py:346` `def format_prominent(self, event)` -- Render an event as a toastr panel with the complete summary.
- `ToastFormatter.format_ephemeral` (method) `cli/toast_bus.py:363` `def format_ephemeral(self, event)` -- Return a single sonner-style line with severity icon for ``event``.
- `ToastFormatter.duration_for` (method) `cli/toast_bus.py:391` `def duration_for(self, event)` -- Return the auto-dismiss delay in seconds for ``event``.
- `ToastFormatter.digest_line` (method) `cli/toast_bus.py:409` `def digest_line(dropped)` -- Summarise over-budget events so none vanish silently.
- `ToastFormatter.format_many` (method) `cli/toast_bus.py:417` `def format_many(self, events, width)` -- Render several events as one Rich renderable.
- `ToastBus.__init__` (method) `cli/toast_bus.py:495` `def __init__(self, config, state, reader, formatter, console)` -- Bind every collaborator.
- `ToastBus.collect` (method) `cli/toast_bus.py:510` `def collect(self)` -- Return every unseen event across :attr:`ToastConfig.event_files`.
- `ToastBus.render` (method) `cli/toast_bus.py:522` `def render(self, enabled)` -- Collect, render and persist offsets in a single call.
- `ToastBus.mark_all_seen` (method) `cli/toast_bus.py:551` `def mark_all_seen(self)` -- Advance the offset for every configured file to its current size.
- `ToastBus.render_ephemeral` (method) `cli/toast_bus.py:558` `def render_ephemeral(self, enabled, duration)` -- Collect unseen events and print each as an auto-expiring line.
- `ToastBus.toasts_enabled` (method) `cli/toast_bus.py:656` `def toasts_enabled(payload, config)` -- Return ``True`` when toast rendering is permitted.
- `ToastBus.build_default_bus` (method) `cli/toast_bus.py:679` `def build_default_bus(payload, sessions_dir, console)` -- Wire the canonical bus used by the shell postcmd hook.
- `ToastBus.render_toasts` (method) `cli/toast_bus.py:708` `def render_toasts(payload, sessions_dir, console, bus_factory)` -- One-shot helper used by the cmd2 postcmd hook.
- `ToastBus.ephemeral_enabled` (method) `cli/toast_bus.py:732` `def ephemeral_enabled(payload, config)` -- Return True when toasts must auto-dismiss like sonner.
- `ToastBus.render_ephemeral_toasts` (method) `cli/toast_bus.py:748` `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` -- Collect unseen events and print each as an auto-expiring line.
- `ToastBus.emit_toast` (method) `cli/toast_bus.py:778` `def emit_toast(message, severity, event_type, sessions_dir, config)` -- Append one toast event so the existing render hook displays it.
- `ToastBus.read_recent_toasts` (method) `cli/toast_bus.py:823` `def read_recent_toasts(sessions_dir, limit, config)` -- Return the most recent toast events without touching read offsets.
- `ToastBus.build_toast_renderable` (method) `cli/toast_bus.py:867` `def build_toast_renderable(events, payload, width, config)` -- Render events with the active theme for any surface.

## cli/tui_theme.py
Depends on: `cli/themes.py`
Imported by: `cli/commands/help_ui.py`
- `run` (function) `cli/tui_theme.py:87` `def run(args, payload, save)` -- Execute the ``tui_theme`` command.

## cli/tutorial.py
Depends on: `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `TutorialConfig.is_done` (method) `cli/tutorial.py:83` `def is_done(config)` -- Return True if the tutorial has already been completed.
- `TutorialConfig.mark_done` (method) `cli/tutorial.py:89` `def mark_done(config)` -- Persist the tutorial completion marker.
- `TutorialConfig.render_header` (method) `cli/tutorial.py:96` `def render_header()` -- Print the tutorial welcome banner.
- `TutorialConfig.render_phase_table` (method) `cli/tutorial.py:113` `def render_phase_table()` -- Print the full phase overview before starting.
- `TutorialConfig.run_step` (method) `cli/tutorial.py:128` `def run_step(index, command, description, why, params, command_runner)` -- Execute one tutorial step and return True if the user wants to continue.
- `TutorialConfig.run` (method) `cli/tutorial.py:185` `def run(params, command_runner)` -- Run the interactive tutorial.

## cli/wizard.py
Depends on: `cli/marketplace_config.py`, `core/console.py`, `core/payload_schema.py`, `core/profiles.py`, `modules/cli_auth.py`, `modules/llm_factory.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/doctor.py`, `tests/test_doctor.py`, `tests/test_wizard_llm.py`
- `WizardResult.run` (method) `cli/wizard.py:169` `def run(params, save)` -- Run the interactive setup wizard and return a :class:`WizardResult`.
- `WizardResult.run_non_interactive` (method) `cli/wizard.py:234` `def run_non_interactive(params, save, values)` -- Apply configuration without prompts — Docker/CI/headless first runs.
- `WizardResult.check_binaries` (method) `cli/wizard.py:947` `def check_binaries(specs, which)` -- Return the presence status of every spec without executing it.

## cli/wizard_scope.py
Imported by: `cli/commands/help_ui.py`
- `WizardScope.parse_scope` (method) `cli/wizard_scope.py:38` `def parse_scope(tokens, config)` -- Parse --show and --only=a,b flags from wizard tokens.
- `WizardScope.status_rows` (method) `cli/wizard_scope.py:64` `def status_rows(params)` -- Build display rows for the current configuration state.

## contrib/legacy/lazy_http_bof.py
- `genHeader` (function) `contrib/legacy/lazy_http_bof.py:6` `def genHeader(raw)`
- `exploit` (function) `contrib/legacy/lazy_http_bof.py:29` `def exploit(target, port, payload)`

## contrib/legacy/lazy_packet_image_sniffer.py
- `check_sudo` (function) `contrib/legacy/lazy_packet_image_sniffer.py:23` `def check_sudo()`
- `list_interfaces` (function) `contrib/legacy/lazy_packet_image_sniffer.py:31` `def list_interfaces()`
- `choose_interface` (function) `contrib/legacy/lazy_packet_image_sniffer.py:49` `def choose_interface(interfaces)`
- `get_subnet_from_interface` (function) `contrib/legacy/lazy_packet_image_sniffer.py:61` `def get_subnet_from_interface(interface)`
- `get_ip_addresses` (function) `contrib/legacy/lazy_packet_image_sniffer.py:65` `def get_ip_addresses(interface)`
- `handle_packet` (function) `contrib/legacy/lazy_packet_image_sniffer.py:111` `def handle_packet(packet)`
- `save_image` (function) `contrib/legacy/lazy_packet_image_sniffer.py:161` `def save_image(src_ip, end_idx)`
- `run` (function) `contrib/legacy/lazy_packet_image_sniffer.py:187` `def run()`
- `daemonize` (function) `contrib/legacy/lazy_packet_image_sniffer.py:192` `def daemonize()`

## contrib/legacy/lazyaddon_creator.py
Depends on: `modules/llm_client.py`
- `parse_github_url` (function) `contrib/legacy/lazyaddon_creator.py:49` `def parse_github_url(url)` -- Extrae (owner, repo) de una URL de GitHub.
- `github_api_get` (function) `contrib/legacy/lazyaddon_creator.py:58` `def github_api_get(owner, repo, endpoint)` -- GET a la API pública de GitHub (sin auth, rate-limit 60/hr).
- `fetch_repo_metadata` (function) `contrib/legacy/lazyaddon_creator.py:68` `def fetch_repo_metadata(owner, repo)` -- Devuelve metadata básica del repo.
- `fetch_readme` (function) `contrib/legacy/lazyaddon_creator.py:73` `def fetch_readme(owner, repo)` -- Descarga y decodifica el README.
- `fetch_root_files` (function) `contrib/legacy/lazyaddon_creator.py:85` `def fetch_root_files(owner, repo)` -- Lista nombres de archivos en el directorio raíz.
- `build_llm_prompt` (function) `contrib/legacy/lazyaddon_creator.py:98` `def build_llm_prompt(meta, readme, root_files)` -- Construye el prompt para el LLM.
- `extract_json_from_response` (function) `contrib/legacy/lazyaddon_creator.py:164` `def extract_json_from_response(text)` -- Extrae el primer bloque JSON de una respuesta de LLM.
- `heuristic_install_command` (function) `contrib/legacy/lazyaddon_creator.py:192` `def heuristic_install_command(root_files, language)` -- Infiere un install_command básico a partir de los archivos raíz.
- `heuristic_execute_command` (function) `contrib/legacy/lazyaddon_creator.py:211` `def heuristic_execute_command(name, root_files, language)` -- Infiere un execute_command básico.
- `heuristic_params` (function) `contrib/legacy/lazyaddon_creator.py:245` `def heuristic_params(name, readme, root_files)` -- Infiere parámetros comunes basándose en el nombre y README.
- `fallback_yaml_data` (function) `contrib/legacy/lazyaddon_creator.py:276` `def fallback_yaml_data(meta, readme, root_files)` -- Genera datos de addon usando solo heurísticas locales (sin LLM).
- `build_yaml` (function) `contrib/legacy/lazyaddon_creator.py:300` `def build_yaml(data, repo_url)` -- Construye la estructura de dict que representa el addon YAML.
- `save_yaml` (function) `contrib/legacy/lazyaddon_creator.py:336` `def save_yaml(addon, output_dir)` -- Guarda el dict como archivo YAML en output_dir.
- `main` (function) `contrib/legacy/lazyaddon_creator.py:357` `def main()`

## contrib/legacy/lazyarpspoofing.py
- `check_sudo` (function) `contrib/legacy/lazyarpspoofing.py:27` `def check_sudo()`
- `enable_ip_forward` (function) `contrib/legacy/lazyarpspoofing.py:35` `def enable_ip_forward()`
- `disable_ip_forward` (function) `contrib/legacy/lazyarpspoofing.py:38` `def disable_ip_forward()`
- `get_local_ip` (function) `contrib/legacy/lazyarpspoofing.py:41` `def get_local_ip(ifname)`
- `get_mac` (function) `contrib/legacy/lazyarpspoofing.py:49` `def get_mac(ip, device, retries, timeout)`
- `spoofer` (function) `contrib/legacy/lazyarpspoofing.py:69` `def spoofer(target, spoofed, device)`
- `main` (function) `contrib/legacy/lazyarpspoofing.py:80` `def main()`

## contrib/legacy/lazybinenc.py
Depends on: `cli/commands/pwn.py`, `core/console.py`, `core/prompt.py`
- `generate_key_iv` (function) `contrib/legacy/lazybinenc.py:12` `def generate_key_iv(sessions_path)`
- `main` (function) `contrib/legacy/lazybinenc.py:54` `def main()`

## contrib/legacy/lazybotcli.py
- `encrypt` (function) `contrib/legacy/lazybotcli.py:30` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazybotcli.py:36` `def decrypt(ciphertext, key)`
- `main` (function) `contrib/legacy/lazybotcli.py:42` `def main()`

## contrib/legacy/lazybotnet.py
- `encrypt` (function) `contrib/legacy/lazybotnet.py:46` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazybotnet.py:52` `def decrypt(ciphertext, key)`
- `add_to_botnet` (function) `contrib/legacy/lazybotnet.py:58` `def add_to_botnet(ip, port, botnet_file)`
- `clean_botnet` (function) `contrib/legacy/lazybotnet.py:62` `def clean_botnet(ip, port, botnet_file)`
- `send_to_botnet` (function) `contrib/legacy/lazybotnet.py:71` `def send_to_botnet(cmd, key, botnet_file)`
- `Keylogger.__init__` (method) `contrib/legacy/lazybotnet.py:90` `def __init__(self, key, log_file)`
- `Keylogger.on_press` (method) `contrib/legacy/lazybotnet.py:95` `def on_press(self, key)`
- `Keylogger.start` (method) `contrib/legacy/lazybotnet.py:106` `def start(self)`
- `Keylogger.get_log` (method) `contrib/legacy/lazybotnet.py:110` `def get_log(self)`
- `Keylogger.save_log` (method) `contrib/legacy/lazybotnet.py:113` `def save_log(self)`
- `Keylogger.run` (method) `contrib/legacy/lazybotnet.py:120` `def run(self)`
- `Keylogger.setup_persistence` (method) `contrib/legacy/lazybotnet.py:125` `def setup_persistence(self)`
- `Keylogger.create_shortcut` (method) `contrib/legacy/lazybotnet.py:136` `def create_shortcut(self, script_path, shortcut_path)`
- `Keylogger.handle_client` (method) `contrib/legacy/lazybotnet.py:144` `def handle_client(conn, key, botnet_file, log_file)`
- `Keylogger.start_server` (method) `contrib/legacy/lazybotnet.py:182` `def start_server(host, port, key, botnet_file, log_file)`

## contrib/legacy/lazycam.py
- `RTSPScanner.__init__` (method) `contrib/legacy/lazycam.py:33` `def __init__(self, verbose, wspace)`
- `RTSPScanner.run` (method) `contrib/legacy/lazycam.py:49` `def run(self)`
- `RTSPScanner.resizeImg` (method) `contrib/legacy/lazycam.py:68` `def resizeImg(self, img, output, height, ratio, fmt)`
- `RTSPScanner.splitCSV` (method) `contrib/legacy/lazycam.py:77` `def splitCSV(self, csv)`
- `RTSPScanner.scanner` (method) `contrib/legacy/lazycam.py:83` `def scanner(self)`
- `RTSPScanner.delCameras` (method) `contrib/legacy/lazycam.py:136` `def delCameras(self)`
- `RTSPScanner.addCameras` (method) `contrib/legacy/lazycam.py:149` `def addCameras(self)`
- `RTSPScanner.cla` (method) `contrib/legacy/lazycam.py:212` `def cla()`
- `RTSPScanner.main` (method) `contrib/legacy/lazycam.py:257` `def main()`

## contrib/legacy/lazydeepseekcli.py
Depends on: `core/logging.py`
Imported by: `modules/llm_adapter.py`
- `truncate_message` (function) `contrib/legacy/lazydeepseekcli.py:41` `def truncate_message(message, max_chars)`
- `configure_logging` (function) `contrib/legacy/lazydeepseekcli.py:45` `def configure_logging(debug)`
- `load_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:167` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:174` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:179` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazydeepseekcli.py:185` `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:193` `def transform_knowledge_base(prompt_builder)`
- `generate` (function) `contrib/legacy/lazydeepseekcli.py:231` `def generate()`
- `process_prompt_local` (function) `contrib/legacy/lazydeepseekcli.py:255` `def process_prompt_local(prompt, debug, mode)`
- `process_prompt_localreport` (function) `contrib/legacy/lazydeepseekcli.py:263` `def process_prompt_localreport(prompt, debug, mode)`
- `parse_args` (function) `contrib/legacy/lazydeepseekcli.py:271` `def parse_args()`

## contrib/legacy/lazydisassebler.py
- `X64Disassembler.__init__` (method) `contrib/legacy/lazydisassebler.py:34` `def __init__(self)` -- Initializes the X64Disassembler instance.
- `X64Disassembler.read_elf_header` (method) `contrib/legacy/lazydisassebler.py:79` `def read_elf_header(self, data)` -- Reads the ELF header and finds the code section.
- `X64Disassembler.parse_modrm` (method) `contrib/legacy/lazydisassebler.py:135` `def parse_modrm(self, modrm, rex)` -- Parses the ModR/M byte and extracts mod, reg, and rm fields.
- `X64Disassembler.parse_sib` (method) `contrib/legacy/lazydisassebler.py:173` `def parse_sib(self, sib, rex)` -- Parses the SIB byte and extracts scale, index, and base fields.
- `X64Disassembler.get_operand_str` (method) `contrib/legacy/lazydisassebler.py:212` `def get_operand_str(self, mod, rm, rex, bytes_data, offset)` -- Gets the string representation of the operand based on mod/rm.
- `X64Disassembler.disassemble` (method) `contrib/legacy/lazydisassebler.py:305` `def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point)` -- Main disassembler for x86-64 code.
- `X64Disassembler.main` (method) `contrib/legacy/lazydisassebler.py:489` `def main()` -- Main function for the disassembler.

## contrib/legacy/lazyftpsniff.py
- `check_sudo` (function) `contrib/legacy/lazyftpsniff.py:21` `def check_sudo()`
- `signal_handler` (function) `contrib/legacy/lazyftpsniff.py:34` `def signal_handler(sig, frame)`
- `parse_arguments` (function) `contrib/legacy/lazyftpsniff.py:42` `def parse_arguments()`
- `sniffer_ftp` (function) `contrib/legacy/lazyftpsniff.py:56` `def sniffer_ftp(pkt)`
- `main` (function) `contrib/legacy/lazyftpsniff.py:69` `def main()`

## contrib/legacy/lazygalazy.py
Depends on: `modules/backdoor/server.c`
- `SamsungKnoxExploitServer.do_GET` (method) `contrib/legacy/lazygalazy.py:11` `def do_GET(self)`
- `SamsungKnoxExploitServer.apk_bytes` (method) `contrib/legacy/lazygalazy.py:33` `def apk_bytes(self)`
- `SamsungKnoxExploitServer.launch_html` (method) `contrib/legacy/lazygalazy.py:36` `def launch_html(self)`
- `SamsungKnoxExploitServer.exploit_js` (method) `contrib/legacy/lazygalazy.py:49` `def exploit_js(self)`
- `SamsungKnoxExploitServer.rand_word` (method) `contrib/legacy/lazygalazy.py:93` `def rand_word(self)`
- `SamsungKnoxExploitServer.main` (method) `contrib/legacy/lazygalazy.py:97` `def main()`

## contrib/legacy/lazygptcli.py
Depends on: `contrib/legacy/lazygptcli_unified.py`, `core/logging.py`, `modules/colors.py`
- `signal_handler` (function) `contrib/legacy/lazygptcli.py:66` `def signal_handler(sig, frame)`
- `show_help` (function) `contrib/legacy/lazygptcli.py:73` `def show_help(message)`
- `check_api_key` (function) `contrib/legacy/lazygptcli.py:77` `def check_api_key()`
- `configure_logging` (function) `contrib/legacy/lazygptcli.py:83` `def configure_logging(debug)`
- `parse_args` (function) `contrib/legacy/lazygptcli.py:87` `def parse_args()`
- `create_complex_prompt` (function) `contrib/legacy/lazygptcli.py:94` `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function) `contrib/legacy/lazygptcli.py:108` `def execute_command(command)`
- `load_knowledge_base` (function) `contrib/legacy/lazygptcli.py:118` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazygptcli.py:124` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazygptcli.py:128` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazygptcli.py:133` `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function) `contrib/legacy/lazygptcli.py:141` `def transform_knowledge_base(client)`
- `cleanup_temp_files` (function) `contrib/legacy/lazygptcli.py:164` `def cleanup_temp_files()`
- `main` (function) `contrib/legacy/lazygptcli.py:177` `def main()`

## contrib/legacy/lazygptcli_unified.py
Depends on: `core/logging.py`, `modules/colors.py`
Imported by: `contrib/legacy/lazygptcli.py`
- `truncate_message` (function) `contrib/legacy/lazygptcli_unified.py:53` `def truncate_message(message, max_chars)`
- `process_prompt` (function) `contrib/legacy/lazygptcli_unified.py:318` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `contrib/legacy/lazygptcli_unified.py:323` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `contrib/legacy/lazygptcli_unified.py:328` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `contrib/legacy/lazygptcli_unified.py:333` `def process_prompt_general(client, prompt, debug)` -- General red team assistant with payload.json context and DeepSeek fallback.
- `process_prompt_search` (function) `contrib/legacy/lazygptcli_unified.py:341` `def process_prompt_search(client, prompt, debug)` -- Research and threat intelligence analysis.
- `process_prompt_task` (function) `contrib/legacy/lazygptcli_unified.py:346` `def process_prompt_task(client, prompt, debug)` -- Analyze task assessment JSON for completion status and next commands.
- `process_prompt_vuln` (function) `contrib/legacy/lazygptcli_unified.py:356` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and generate penetration test action plan.
- `process_prompt_redop` (function) `contrib/legacy/lazygptcli_unified.py:382` `def process_prompt_redop(client, prompt, debug)` -- Evaluate Red Team operation status from JSON database params.

## contrib/legacy/lazyhoneypot.py
Depends on: `core/logging.py`
- `parse_args` (function) `contrib/legacy/lazyhoneypot.py:34` `def parse_args()`
- `setup_logging` (function) `contrib/legacy/lazyhoneypot.py:52` `def setup_logging(log_file)`
- `generate_rsa_key` (function) `contrib/legacy/lazyhoneypot.py:56` `def generate_rsa_key(key_filename)`
- `Server.__init__` (method) `contrib/legacy/lazyhoneypot.py:61` `def __init__(self)`
- `Server.check_channel_request` (method) `contrib/legacy/lazyhoneypot.py:64` `def check_channel_request(self, kind, chanid)`
- `Server.check_auth_password` (method) `contrib/legacy/lazyhoneypot.py:69` `def check_auth_password(self, username, password)`
- `Server.handle_connection` (method) `contrib/legacy/lazyhoneypot.py:74` `def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir)`
- `Server.handle_file_download` (method) `contrib/legacy/lazyhoneypot.py:110` `def handle_file_download(command, downloads_dir, downloads_log)`
- `Server.log_command` (method) `contrib/legacy/lazyhoneypot.py:128` `def log_command(command, commands_log)`
- `Server.log_downloaded_file` (method) `contrib/legacy/lazyhoneypot.py:132` `def log_downloaded_file(filename, url, downloads_log)`
- `Server.analyze_traffic` (method) `contrib/legacy/lazyhoneypot.py:136` `def analyze_traffic()`
- `Server.process_packet` (method) `contrib/legacy/lazyhoneypot.py:137` `def process_packet(packet)`
- `Server.alert_admin` (method) `contrib/legacy/lazyhoneypot.py:147` `def alert_admin(message)`
- `Server.main` (method) `contrib/legacy/lazyhoneypot.py:165` `def main()`

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
- `LazyOwnShellBridge.no_history_init` (method) `contrib/legacy/lazyllmchat.py:38` `def no_history_init(self_)`
- `LazyOwnShellBridge.execute` (method) `contrib/legacy/lazyllmchat.py:65` `def execute(self, command)`
- `LazyOwnShellBridge.target` (method) `contrib/legacy/lazyllmchat.py:70` `def target()`
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
- `LazyOwnLLMChat.main` (method) `contrib/legacy/lazyllmchat.py:309` `def main()`

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
- `InvalidUsername.add_boolean` (method) `contrib/legacy/lazyopenssh77enum2.py:19` `def add_boolean()`
- `InvalidUsername.service_accept` (method) `contrib/legacy/lazyopenssh77enum2.py:30` `def service_accept()`
- `InvalidUsername.invalid_username` (method) `contrib/legacy/lazyopenssh77enum2.py:36` `def invalid_username()`
- `InvalidUsername.check_user` (method) `contrib/legacy/lazyopenssh77enum2.py:50` `def check_user(username)`

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
- `BinaryAttacker.main` (method) `contrib/legacy/lazypwn.py:181` `def main()`

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
- `Config.load_payload` (method) `contrib/legacy/lazyseo.py:23` `def load_payload()`
- `Config.make_request` (method) `contrib/legacy/lazyseo.py:28` `def make_request(url, retries, timeout)`
- `Config.results` (method) `contrib/legacy/lazyseo.py:49` `def results(file)`
- `Config.crawl` (method) `contrib/legacy/lazyseo.py:57` `def crawl(url)`
- `Config.ffuf` (method) `contrib/legacy/lazyseo.py:66` `def ffuf()`
- `Config.analyze_seo` (method) `contrib/legacy/lazyseo.py:76` `def analyze_seo(url)`

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
Imported by: `lazyc2/app_factory.py`, `lazyc2/blueprints/api.py`, `tests/test_api_authz.py`, `tests/test_api_v1.py`
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
- `ApiKeyStore.require_api_auth` (method) `core/api_authz.py:365` `def require_api_auth(store, permissions, require_tenant)` -- Flask-route decorator that enforces API-key + tenant authorization.
- `ApiKeyStore.decorator` (method) `core/api_authz.py:405` `def decorator(f)`
- `ApiKeyStore.decorated` (method) `core/api_authz.py:407` `def decorated()`
- `ApiKeyStore.create_api_token` (method) `core/api_authz.py:440` `def create_api_token(store, tenant_id, label, permissions, expires_in_days)` -- Create an API key and return the one-time plaintext token.


Next: [API_p6.md](API_p6.md)
