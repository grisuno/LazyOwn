# API (page 18 of 24)
Previous: [API_p17.md](API_p17.md)

## modules/world_model.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/cli_auth.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/pwn.py`, `cli/ops_commands.py`, `cli/session_brief.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `modules/atomic_exploit_bridge.py`, `modules/exploit_recommender.py`, `modules/gym_registry.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/live_surface.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/redteam_gym.py`, `modules/sinks/world_model.py`, `modules/state_manager.py`, `modules/unified_dashboard.py`, `modules/verb_manifest.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_gym_cli.py`, `tests/test_gym_registry.py`, `tests/test_infra_disposable.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_lazy_orchestrator.py`, `tests/test_loop_cli_catalog.py`, `tests/test_ops_loot_phase.py`, `tests/test_orchestrator_api.py`, `tests/test_phase1_data_gaps.py`, `tests/test_session_brief.py`, `tests/test_world_model_extended.py`
- `read_state_dict` (function) `modules/world_model.py:101` `def read_state_dict(path)` -- Read a world-model state dict, transparently decrypting at rest.
- `write_state_dict` (function) `modules/world_model.py:147` `def write_state_dict(path, data)` -- Atomically write a world-model state dict as plaintext.
- `HostState.rank` (method) `modules/world_model.py:189` `def rank(self)`
- `HostState.can_advance_to` (method) `modules/world_model.py:192` `def can_advance_to(self, next_state)`
- `NetworkGraph.__init__` (method) `modules/world_model.py:296` `def __init__(self)`
- `NetworkGraph.add_relation` (method) `modules/world_model.py:303` `def add_relation(self, relation)` -- Add a directed edge.
- `NetworkGraph.neighbors` (method) `modules/world_model.py:311` `def neighbors(self, node)` -- Return nodes reachable from *node* in one outbound hop.
- `NetworkGraph.in_degree` (method) `modules/world_model.py:315` `def in_degree(self, node)` -- Count edges pointing INTO *node*.
- `NetworkGraph.out_degree` (method) `modules/world_model.py:319` `def out_degree(self, node)` -- Count edges leaving *node*.
- `NetworkGraph.degree_centrality` (method) `modules/world_model.py:323` `def degree_centrality(self)` -- Return (node, centrality_score) pairs sorted descending by score.
- `NetworkGraph.pivot_candidates` (method) `modules/world_model.py:338` `def pivot_candidates(self, top_k)` -- Return the *top_k* highest-centrality nodes as pivot candidates.
- `NetworkGraph.to_dict` (method) `modules/world_model.py:360` `def to_dict(self)`
- `NetworkGraph.from_dict` (method) `modules/world_model.py:377` `def from_dict(cls, data)`
- `HostEntry.add_service` (method) `modules/world_model.py:402` `def add_service(self, svc)`
- `HostEntry.advance` (method) `modules/world_model.py:406` `def advance(self, new_state)` -- Advance state only if new_state is the next valid step.
- `HostEntry.to_dict` (method) `modules/world_model.py:414` `def to_dict(self)`
- `HostEntry.from_dict` (method) `modules/world_model.py:426` `def from_dict(cls, d)`
- `_PhaseDeriver.derive` (method) `modules/world_model.py:459` `def derive(self, hosts)`
- `WorldModel.__init__` (method) `modules/world_model.py:578` `def __init__(self, path)`
- `WorldModel.add_host` (method) `modules/world_model.py:594` `def add_host(self, ip)`
- `WorldModel.reset_host` (method) `modules/world_model.py:602` `def reset_host(self, ip)` -- Clear a single host's state back to UNSCANNED for a fresh scan.
- `WorldModel.remove_host` (method) `modules/world_model.py:612` `def remove_host(self, ip)` -- Remove one host from the model and persist the change.
- `WorldModel.advance_host` (method) `modules/world_model.py:628` `def advance_host(self, ip, new_state)`
- `WorldModel.add_service` (method) `modules/world_model.py:637` `def add_service(self, ip, port, name, version, protocol)`
- `WorldModel.add_note` (method) `modules/world_model.py:654` `def add_note(self, ip, note)`
- `WorldModel.set_os_hint` (method) `modules/world_model.py:661` `def set_os_hint(self, ip, os_hint)` -- Set the operating system hint for a host.
- `WorldModel.get_host` (method) `modules/world_model.py:675` `def get_host(self, ip)` -- Return a host entry by IP, or None if not found.
- `WorldModel.get_hosts_summary` (method) `modules/world_model.py:687` `def get_hosts_summary(self)` -- Return a mapping of IP -> state for all tracked hosts.
- `WorldModel.add_credential` (method) `modules/world_model.py:698` `def add_credential(self, value, host, service)`
- `WorldModel.link_credential_to_success` (method) `modules/world_model.py:730` `def link_credential_to_success(self, value, host)` -- Mark a credential as working for a specific host in the graph.
- `WorldModel.link_credential_to_failure` (method) `modules/world_model.py:751` `def link_credential_to_failure(self, value, host)` -- Mark a credential as rejected by a specific host in the graph.
- `WorldModel.add_vulnerability` (method) `modules/world_model.py:781` `def add_vulnerability(self, description, host, cve, severity)`
- `WorldModel.add_email` (method) `modules/world_model.py:787` `def add_email(self, address, host, context)`
- `WorldModel.add_domain` (method) `modules/world_model.py:793` `def add_domain(self, domain, host, context)`
- `WorldModel.update_from_findings` (method) `modules/world_model.py:807` `def update_from_findings(self, findings)` -- Integrate a list of Finding objects (from obs_parser.ObsParser).
- `WorldModel.consume_policy_facts` (method) `modules/world_model.py:880` `def consume_policy_facts(self, facts_path)` -- Ingest structured facts from FactStore's ``policy_facts.json``.
- `WorldModel.add_relation` (method) `modules/world_model.py:972` `def add_relation(self, source, target, relation, weight)` -- Add an arbitrary directed relationship to the network graph.
- `WorldModel.pivot_candidates` (method) `modules/world_model.py:993` `def pivot_candidates(self, top_k)` -- Return the top_k highest-centrality nodes as pivot candidates.
- `WorldModel.graph_snapshot` (method) `modules/world_model.py:1001` `def graph_snapshot(self)` -- Return the full network graph as a serialisable dict.
- `WorldModel.get_phase` (method) `modules/world_model.py:1008` `def get_phase(self)`
- `WorldModel.get_suggested_tools` (method) `modules/world_model.py:1012` `def get_suggested_tools(self)`
- `WorldModel.to_context_string` (method) `modules/world_model.py:1015` `def to_context_string(self)` -- Compact, LLM-readable summary of the current engagement state.
- `WorldModel.reload` (method) `modules/world_model.py:1123` `def reload(self)` -- Discard in-memory state and re-read from the persisted file.
- `WorldModel.reset` (method) `modules/world_model.py:1139` `def reset(self)` -- Clear all state and delete the persisted file.
- `WorldModel.snapshot` (method) `modules/world_model.py:1150` `def snapshot(self)` -- Return a plain-dict snapshot (for JSON serialisation).
- `WorldModel.read_section` (method) `modules/world_model.py:1166` `def read_section(self, key)` -- Return one allowlisted passthrough section.
- `WorldModel.write_section` (method) `modules/world_model.py:1183` `def write_section(self, key, value)` -- Persist one allowlisted passthrough section atomically.
- `get_world_model` (function) `modules/world_model.py:1211` `def get_world_model(path)` -- Return (or create) the module-level singleton WorldModel.

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

## scripts/migrate_lazyown.py
Imported by: `tests/test_migrate_lazyown_generator.py`
- `extract_method` (function) `scripts/migrate_lazyown.py:88` `def extract_method(source, node)` -- Return the raw source text of a function definition.
- `rewrite_globals` (function) `scripts/migrate_lazyown.py:96` `def rewrite_globals(method_source)` -- Replace bare module-global names with ``self.params[...]``.
- `build_migrated_module` (function) `scripts/migrate_lazyown.py:124` `def build_migrated_module(phase, category, methods)` -- Return the source text of a migrated ``CommandSet`` module.
- `main` (function) `scripts/migrate_lazyown.py:173` `def main()`

## scripts/mutate.sh
- `runners` (function) `scripts/mutate.sh:29`
- `changed_sources` (function) `scripts/mutate.sh:33`
- `usage` (function) `scripts/mutate.sh:40`

## scripts/mutation_gate.py
- `discover_runners` (function) `scripts/mutation_gate.py:25` `def discover_runners()` -- Return sorted curated mutation runners.
- `run_runner` (function) `scripts/mutation_gate.py:34` `def run_runner(path, timeout_s)` -- Execute one mutation runner.
- `main` (function) `scripts/mutation_gate.py:63` `def main(argv)` -- Entry point for the mutation gate.

## scripts/publish_wiki.sh
- `log` (function) `scripts/publish_wiki.sh:37`
- `fail` (function) `scripts/publish_wiki.sh:38`
- `write_home` (function) `scripts/publish_wiki.sh:58`
- `write_installation` (function) `scripts/publish_wiki.sh:92`
- `write_c2_api` (function) `scripts/publish_wiki.sh:150`
- `write_plugins` (function) `scripts/publish_wiki.sh:174`
- `write_sidebar` (function) `scripts/publish_wiki.sh:188`
- `write_footer` (function) `scripts/publish_wiki.sh:207`

## scripts/read_journal.py
Depends on: `scripts/journal.py`
- `main` (function) `scripts/read_journal.py:29` `def main(argv)` -- Print the recent journal entries and return the process exit code.

## scripts/smoke_onboarding.sh
- `check` (function) `scripts/smoke_onboarding.sh:8`

## scripts/sync_doc_stats.py
- `canonical_command_count` (function) `scripts/sync_doc_stats.py:87` `def canonical_command_count(root)` -- Read the canonical command count from the committed command index.
- `project_version` (function) `scripts/sync_doc_stats.py:100` `def project_version(root)` -- Read the package version from pyproject.toml, ``0.0.0`` when absent.
- `measure_stats` (function) `scripts/sync_doc_stats.py:109` `def measure_stats(root)` -- Measure every published count from the live tree.
- `render` (function) `scripts/sync_doc_stats.py:136` `def render(template, stats)` -- Format one replacement template with the measured stats.
- `sync` (function) `scripts/sync_doc_stats.py:141` `def sync(check, stats, root)` -- Apply or verify every replacement; return the list of stale spots.
- `main` (function) `scripts/sync_doc_stats.py:165` `def main()` -- CLI entry point.

## scripts/top_tier_check.py
- `fail` (function) `scripts/top_tier_check.py:23` `def fail(message)`
- `ok` (function) `scripts/top_tier_check.py:28` `def ok(message)`
- `count_cli_commands` (function) `scripts/top_tier_check.py:32` `def count_cli_commands()`
- `count_mcp_tools` (function) `scripts/top_tier_check.py:43` `def count_mcp_tools()`
- `count_addons` (function) `scripts/top_tier_check.py:48` `def count_addons()`
- `check_versions` (function) `scripts/top_tier_check.py:52` `def check_versions()`
- `check_doc_counts` (function) `scripts/top_tier_check.py:70` `def check_doc_counts(commands, mcp, addons)`
- `check_tracked_secrets` (function) `scripts/top_tier_check.py:81` `def check_tracked_secrets()`
- `check_release_inputs` (function) `scripts/top_tier_check.py:108` `def check_release_inputs()`
- `main` (function) `scripts/top_tier_check.py:116` `def main()`

## scripts/update_apt_atomic_ids.py
- `build_technique_index` (function) `scripts/update_apt_atomic_ids.py:22` `def build_technique_index(atomics_path)` -- Map technique_id -> list of {atomic_id, name, description}.
- `update_playbooks` (function) `scripts/update_apt_atomic_ids.py:46` `def update_playbooks(index, playbook_dir)`

## scripts/validate_agent_contract.sh
- `pass` (function) `scripts/validate_agent_contract.sh:23`
- `fail` (function) `scripts/validate_agent_contract.sh:27`
- `check` (function) `scripts/validate_agent_contract.sh:32`
- `check_no_hardcoded_passwords` (function) `scripts/validate_agent_contract.sh:59` -- -- No hardcoded credentials outside payload.json --- Pentest help-text, doc placeholders (<...>), template vars ({{...
- `check_no_hardcoded_wordlists` (function) `scripts/validate_agent_contract.sh:74` -- -- No hardcoded wordlist paths outside payload.json --- Help-text examples, docstrings and filesystem hints are...

## skills/aci_planner.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_aci_planner.py`
- `AttackPhase.to_dict` (method) `skills/aci_planner.py:171` `def to_dict(self)` -- Serialize to dict for JSON persistence.
- `AttackPhase.from_dict` (method) `skills/aci_planner.py:176` `def from_dict(cls, d)` -- Deserialize from dict.
- `ACIPlan.active_phase` (method) `skills/aci_planner.py:199` `def active_phase(self)` -- Return the first phase that is active or pending.
- `ACIPlan.completion_pct` (method) `skills/aci_planner.py:207` `def completion_pct(self)` -- Percentage of phases that are done or skipped.
- `ACIPlan.to_dict` (method) `skills/aci_planner.py:214` `def to_dict(self)` -- Serialize to dict for JSON persistence.
- `ACIPlan.from_dict` (method) `skills/aci_planner.py:221` `def from_dict(cls, d)` -- Deserialize from dict.
- `ACIPlanner.__init__` (method) `skills/aci_planner.py:461` `def __init__(self, api_key, objectives_file, plan_file)`
- `ACIPlanner.plan` (method) `skills/aci_planner.py:471` `def plan(self, goal, phase_filter)` -- Decompose *goal* into an ACIPlan, inject objectives, persist.
- `ACIEngine.__init__` (method) `skills/aci_planner.py:604` `def __init__(self, api_key, plan_file, objectives_file, history_file, replan_threshold)`
- `ACIEngine.status` (method) `skills/aci_planner.py:618` `def status(self)` -- Return a structured status dict for the active plan.
- `ACIEngine.should_replan` (method) `skills/aci_planner.py:658` `def should_replan(self, plan)` -- Return True when the plan is stalled and a replan is warranted.
- `ACIEngine.replan` (method) `skills/aci_planner.py:671` `def replan(self, reason)` -- Generate a new set of objectives for blocked/remaining phases.
- `ACIEngine.complete` (method) `skills/aci_planner.py:741` `def complete(self)` -- Mark the active plan as completed and archive it.
- `ACIReflector.__init__` (method) `skills/aci_planner.py:797` `def __init__(self, lessons_file)`
- `ACIReflector.reflect` (method) `skills/aci_planner.py:800` `def reflect(self, plan)` -- Analyse *plan* and generate lessons.
- `mcp_aci_plan` (function) `skills/aci_planner.py:865` `def mcp_aci_plan(goal, target, scope, domain, os_hint, phase_filter)` -- Plan an engagement goal and return a JSON summary.
- `mcp_aci_status` (function) `skills/aci_planner.py:923` `def mcp_aci_status()` -- Return live status of the active ACI plan as JSON.
- `mcp_aci_replan` (function) `skills/aci_planner.py:940` `def mcp_aci_replan(reason)` -- Force adaptive replanning of the active ACI plan.
- `main` (function) `skills/aci_planner.py:1003` `def main(argv)` -- Entry point for CLI usage.


Next: [API_p19.md](API_p19.md)
