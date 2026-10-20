# API (page 18 of 23)
Previous: [API_p17.md](API_p17.md)

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

## skills/autonomous_daemon.py
Depends on: `core/logging.py`, `modules/asset_graph.py`, `modules/db.py`, `modules/detection_oracle.py`, `modules/enrich.py`, `modules/event_consumers.py`, `modules/evidence.py`, `modules/finding_lifecycle.py`, `modules/goals.py`, `modules/intercept.py`, `modules/killchain.py`, `modules/llm_pool.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/notify.py`, `modules/obs_parser.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/toolset.py`, `modules/traffic_recorder.py`, `skills/daemon_control.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_helpers.py`, `skills/lazyown_objective.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`
Imported by: `cli/commands/database.py`, `cli/commands/session_ops.py`, `modules/pipeline_engine.py`, `skills/autonomous_replay.py`, `skills/lazyown_mcp.py`, `skills/tests/test_autonomous_daemon.py`, `skills/unified_orchestrator.py`, `tests/test_autonomous_replay.py`, `tests/test_daemon_loop.py`, `tests/test_engage_gates.py`, `tests/test_engage_orchestrator.py`, `tests/test_metrics_aware_selector.py`, `tests/test_moe_rl_swan.py`, `tests/test_pipeline_engine.py`, `tests/test_scope_bound_auto_gate.py`
- `compute_decision_seed` (function) `skills/autonomous_daemon.py:394` `def compute_decision_seed(objective_id, step_n, source)` -- Return a deterministic identifier for a daemon decision.
- `ICommandRunner.run` (method) `skills/autonomous_daemon.py:426` `def run(self, command, timeout)` -- Execute command within timeout seconds.
- `ICommandRunner.name` (method) `skills/autonomous_daemon.py:431` `def name(self)` -- Human-readable identifier for this runner.
- `MCPCommandRunner.name` (method) `skills/autonomous_daemon.py:482` `def name(self)`
- `MCPCommandRunner.run` (method) `skills/autonomous_daemon.py:485` `def run(self, command, timeout)` -- Try to import and call the MCP runner.
- `PTYCommandRunner.name` (method) `skills/autonomous_daemon.py:502` `def name(self)`
- `PTYCommandRunner.run` (method) `skills/autonomous_daemon.py:505` `def run(self, command, timeout)` -- Execute command via PTY.
- `CommandRunnerChain.__init__` (method) `skills/autonomous_daemon.py:592` `def __init__(self, runners)`
- `CommandRunnerChain.name` (method) `skills/autonomous_daemon.py:598` `def name(self)`
- `CommandRunnerChain.run` (method) `skills/autonomous_daemon.py:601` `def run(self, command, timeout)` -- Try each runner in sequence.
- `ICommandSelector.select` (method) `skills/autonomous_daemon.py:689` `def select(self, target, phase, context)` -- Return a CommandDecision or None if this selector has no suggestion.
- `ReactiveSelector.__init__` (method) `skills/autonomous_daemon.py:704` `def __init__(self, reactive_engine)`
- `ReactiveSelector.register_output` (method) `skills/autonomous_daemon.py:708` `def register_output(self, output, command, platform)` -- Feed reactive engine with last command output to generate new decisions.
- `ReactiveSelector.select` (method) `skills/autonomous_daemon.py:735` `def select(self, target, phase, context)` -- Pop and return the pending reactive decision if present.
- `ParquetSelector.__init__` (method) `skills/autonomous_daemon.py:750` `def __init__(self, pdb, fail_counts)`
- `ParquetSelector.select` (method) `skills/autonomous_daemon.py:754` `def select(self, target, phase, context)` -- Return the most-frequent successful command for this phase.
- `BridgeSelector.__init__` (method) `skills/autonomous_daemon.py:796` `def __init__(self, dispatcher, fail_counts)`
- `BridgeSelector.select` (method) `skills/autonomous_daemon.py:800` `def select(self, target, phase, context)` -- Return a bridge catalog suggestion for this phase.
- `LLMSelector.select` (method) `skills/autonomous_daemon.py:866` `def select(self, target, phase, context)` -- Return an LLM-suggested command with catalog context, or None if disabled.
- `SWANSelector.select` (method) `skills/autonomous_daemon.py:988` `def select(self, target, phase, context)` -- Ask the best MoE expert for a command recommendation.
- `FallbackSelector.select` (method) `skills/autonomous_daemon.py:1034` `def select(self, target, phase, context)` -- Return the static fallback command for this phase.
- `MetricsAwareSelector.__init__` (method) `skills/autonomous_daemon.py:1071` `def __init__(self, wrapped, metrics_source, min_success_rate, min_attempts, window_seconds, cache_ttl_s, clock)` -- Initialise the decorator.
- `MetricsAwareSelector.wrapped` (method) `skills/autonomous_daemon.py:1117` `def wrapped(self)` -- Return the underlying selector for introspection in tests.
- `MetricsAwareSelector.select` (method) `skills/autonomous_daemon.py:1203` `def select(self, target, phase, context)` -- Honour the :class:`ICommandSelector` contract.
- `CredentialSpraySelector.__init__` (method) `skills/autonomous_daemon.py:1304` `def __init__(self, fail_counts)`
- `CredentialSpraySelector.select` (method) `skills/autonomous_daemon.py:1308` `def select(self, target, phase, context)` -- Return a spray command when credentials + matching service are available.
- `CascadeStrategy.__init__` (method) `skills/autonomous_daemon.py:1344` `def __init__(self, selectors)`
- `CascadeStrategy.next_command` (method) `skills/autonomous_daemon.py:1347` `def next_command(self, target, phase, context)` -- Try each selector in order.
- `StrategyEngine.__init__` (method) `skills/autonomous_daemon.py:1382` `def __init__(self, runner, selectors)`
- `StrategyEngine.register_output` (method) `skills/autonomous_daemon.py:1409` `def register_output(self, output, command, platform, success)` -- Feed the reactive selector with the last command output.
- `StrategyEngine.next_command` (method) `skills/autonomous_daemon.py:1423` `def next_command(self, target, phase, services, os_hint)` -- Select the next command for target/phase using the cascade.
- `IObjectiveHandler.handle` (method) `skills/autonomous_daemon.py:1457` `def handle(self, objective_id, objective_text, target, context)` -- Execute objective and return a list of step results.
- `ExecutionEngine.__init__` (method) `skills/autonomous_daemon.py:1479` `def __init__(self, strategy, max_steps, world_model, obs_parser, facts, loop)`
- `ExecutionEngine.handle` (method) `skills/autonomous_daemon.py:1495` `def handle(self, objective_id, objective_text, target, context)` -- Synchronous entry point.
- `ExecutionEngine.run_async` (method) `skills/autonomous_daemon.py:1505` `def run_async(self, objective_id, objective_text, target)` -- Asyncio entry point used by objective_loop.
- `DroneCoordinator.__init__` (method) `skills/autonomous_daemon.py:2814` `def __init__(self)`
- `DroneCoordinator.process_findings` (method) `skills/autonomous_daemon.py:2819` `def process_findings(self, findings, target, objective_id, payload_key)` -- Launch drones for relevant findings.
- `EnginePhaseResult.did_switch` (method) `skills/autonomous_daemon.py:3120` `def did_switch(self)` -- True when the orchestrator used a fallback tool.
- `IToolFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3129` `def next_tool(self, failed_command, phase, attempt)` -- Return the next candidate command or None when exhausted.
- `StaticFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3146` `def next_tool(self, failed_command, phase, attempt)`
- `BridgeFallbackResolver.__init__` (method) `skills/autonomous_daemon.py:3168` `def __init__(self, dispatcher)`
- `BridgeFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3193` `def next_tool(self, failed_command, phase, attempt)`
- `_ShellDetector.__init__` (method) `skills/autonomous_daemon.py:3220` `def __init__(self, narrator)`
- `_ShellDetector.poll` (method) `skills/autonomous_daemon.py:3225` `def poll(self, target)` -- Return the newly-detected client_ids since the previous poll.
- `_ShellDetector.detect_in_output` (method) `skills/autonomous_daemon.py:3266` `def detect_in_output(self, output, target)` -- Return True when a shell/root-shell signal appears in command output.
- `EngageOrchestrator.__init__` (method) `skills/autonomous_daemon.py:3312` `def __init__(self, target, runner, narrator, approval_gate, fallback_resolver, shell_detector, plan...`
- `EngageOrchestrator.engagement_id` (method) `skills/autonomous_daemon.py:3357` `def engagement_id(self)` -- Stable id for this engagement (correlates events in logs).
- `EngageOrchestrator.run` (method) `skills/autonomous_daemon.py:3361` `def run(self)` -- Drive the full plan against the configured target.
- `mcp_engage_target` (function) `skills/autonomous_daemon.py:4005` `def mcp_engage_target(target, max_switches_per_step, detach, auto)` -- Public MCP / CLI entry point for the engage verb.
- `mcp_engage_status` (function) `skills/autonomous_daemon.py:4095` `def mcp_engage_status(last_n)` -- Return the last N lines of sessions/engagement.log plus pending approvals.
- `mcp_engage_approve` (function) `skills/autonomous_daemon.py:4121` `def mcp_engage_approve(approval_id, decision, operator)` -- Resolve a pending approval. decision must be 'approved' or 'denied'.
- `mcp_engage_list_pending` (function) `skills/autonomous_daemon.py:4146` `def mcp_engage_list_pending()` -- List every pending approval awaiting an operator decision.
- `cmd_engage` (function) `skills/autonomous_daemon.py:4164` `def cmd_engage(target, max_switches_per_step, detach)` -- CLI helper bound to the `engage <ip>` daemon subcommand.
- `objective_loop` (function) `skills/autonomous_daemon.py:4203` `def objective_loop(max_steps, loop)` -- Root autonomous loop: takes pending objectives from objectives.jsonl and executes them without waiting for Claude...
- `world_model_watcher` (function) `skills/autonomous_daemon.py:4346` `def world_model_watcher(loop)` -- Watch world_model.json.
- `heartbeat_loop` (function) `skills/autonomous_daemon.py:4537` `def heartbeat_loop()` -- Emit heartbeat and write status every HEARTBEAT_S seconds.
- `cmd_run` (function) `skills/autonomous_daemon.py:4664` `def cmd_run(max_steps)` -- Run daemon in foreground (debug mode).
- `cmd_start` (function) `skills/autonomous_daemon.py:4673` `def cmd_start(max_steps)` -- Fork, detach, and run daemon in background.
- `cmd_stop` (function) `skills/autonomous_daemon.py:4703` `def cmd_stop()` -- Send SIGTERM to the running daemon.
- `cmd_status` (function) `skills/autonomous_daemon.py:4720` `def cmd_status()` -- Print current daemon status to stdout.
- `cmd_inject` (function) `skills/autonomous_daemon.py:4736` `def cmd_inject(text, priority)` -- Inject an objective from the CLI, split into verifiable sub-goals.
- `mcp_autonomous_start` (function) `skills/autonomous_daemon.py:4770` `def mcp_autonomous_start(max_steps, backend)` -- Start the autonomous daemon in a background thread (for MCP calls).
- `mcp_autonomous_stop` (function) `skills/autonomous_daemon.py:4812` `def mcp_autonomous_stop()` -- Stop the autonomous daemon.
- `mcp_autonomous_status` (function) `skills/autonomous_daemon.py:4828` `def mcp_autonomous_status()` -- Current daemon state: objectives, steps, drones, phase.
- `mcp_autonomous_inject` (function) `skills/autonomous_daemon.py:4841` `def mcp_autonomous_inject(text, priority, target)` -- Inject an objective into the daemon queue and into sessions/tasks.json.
- `mcp_autonomous_events` (function) `skills/autonomous_daemon.py:4885` `def mcp_autonomous_events(last_n)` -- Read the last N events from autonomous_events.jsonl.

## skills/autonomous_replay.py
Depends on: `core/logging.py`, `skills/autonomous_daemon.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_autonomous_replay.py`
- `ReplayReport.to_dict` (method) `skills/autonomous_replay.py:114` `def to_dict(self)` -- Return the report as a JSON-serialisable dictionary.
- `EventLogReader.__init__` (method) `skills/autonomous_replay.py:136` `def __init__(self, path)` -- Initialise the reader.
- `EventLogReader.path` (method) `skills/autonomous_replay.py:147` `def path(self)` -- Return the source path.
- `EventLogReader.read` (method) `skills/autonomous_replay.py:152` `def read(self)` -- Return every event in the log, oldest first.
- `EventLogReader.slice` (method) `skills/autonomous_replay.py:177` `def slice(self, events, from_event_id, to_event_id)` -- Return the inclusive subrange of *events* by ``id``.
- `ReplayDispatcher.__init__` (method) `skills/autonomous_replay.py:221` `def __init__(self, reader, seed_fn)` -- Initialise the dispatcher.
- `ReplayDispatcher.trace` (method) `skills/autonomous_replay.py:325` `def trace(self, from_event_id, to_event_id)` -- Replay the recorded decision sequence without executing it.
- `ReplayDispatcher.execute` (method) `skills/autonomous_replay.py:357` `def execute(self, from_event_id, to_event_id, runner, timeout)` -- Replay the recorded sequence and re-run each command.
- `replay` (function) `skills/autonomous_replay.py:473` `def replay(from_event_id, to_event_id, mode, events_path, runner, timeout)` -- Convenience entry point used by the MCP tool layer.

## skills/claude_md_orchestrator/bdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/bdd_agent.py:151` `def run(contract, spec, suite, config)` -- Run the implementation agent for one contract.

## skills/claude_md_orchestrator/boy_scout.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/boy_scout.py:90` `def run(state, config)` -- Run the boy scout pass for one contract.
- `write_report` (function) `skills/claude_md_orchestrator/boy_scout.py:110` `def write_report(report, config)` -- Persist the boy scout proposal to disk.

## skills/claude_md_orchestrator/cicd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `run` (function) `skills/claude_md_orchestrator/cicd_agent.py:177` `def run(contract, spec, report, config)` -- Run the CI and CD agent for one contract.

## skills/claude_md_orchestrator/config.py
Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`
- `Config.ensure` (method) `skills/claude_md_orchestrator/config.py:112` `def ensure(self)` -- Create the run subdirectories if they do not exist.
- `Config.state_path` (method) `skills/claude_md_orchestrator/config.py:122` `def state_path(self)` -- Return the absolute path of the cycle state file.
- `Config.specs_dir` (method) `skills/claude_md_orchestrator/config.py:126` `def specs_dir(self)` -- Return the absolute path of the spec directory.
- `Config.tests_dir` (method) `skills/claude_md_orchestrator/config.py:130` `def tests_dir(self)` -- Return the absolute path of the test directory.
- `Config.src_dir` (method) `skills/claude_md_orchestrator/config.py:134` `def src_dir(self)` -- Return the absolute path of the implementation directory.
- `Config.review_dir` (method) `skills/claude_md_orchestrator/config.py:138` `def review_dir(self)` -- Return the absolute path of the review directory.
- `Config.docs_dir` (method) `skills/claude_md_orchestrator/config.py:142` `def docs_dir(self)` -- Return the absolute path of the documentation directory.
- `Config.logs_dir` (method) `skills/claude_md_orchestrator/config.py:146` `def logs_dir(self)` -- Return the absolute path of the log directory.
- `Config.log_path` (method) `skills/claude_md_orchestrator/config.py:150` `def log_path(self)` -- Return the absolute path of the JSONL log for the active run.
- `load_config` (function) `skills/claude_md_orchestrator/config.py:155` `def load_config()` -- Build a Config from environment variables and return it.
- `resolve_optional` (function) `skills/claude_md_orchestrator/config.py:164` `def resolve_optional(config, key)` -- Return the environment value for a key or None when missing.

## skills/claude_md_orchestrator/documentation_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `run` (function) `skills/claude_md_orchestrator/documentation_agent.py:123` `def run(contract, spec, report, config)` -- Run the documentation agent for one contract.

## skills/claude_md_orchestrator/models.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`
- `Contract.to_dict` (method) `skills/claude_md_orchestrator/models.py:91` `def to_dict(self)` -- Return a JSON friendly view of the contract.
- `Contract.from_dict` (method) `skills/claude_md_orchestrator/models.py:96` `def from_dict(cls, data)` -- Build a Contract from a JSON friendly dictionary.
- `SadPath.to_dict` (method) `skills/claude_md_orchestrator/models.py:120` `def to_dict(self)` -- Return a JSON friendly view of the sad path.
- `SadPath.from_dict` (method) `skills/claude_md_orchestrator/models.py:125` `def from_dict(cls, data)` -- Build a SadPath from a JSON friendly dictionary.
- `Spec.to_dict` (method) `skills/claude_md_orchestrator/models.py:166` `def to_dict(self)` -- Return a JSON friendly view of the spec.
- `Spec.from_dict` (method) `skills/claude_md_orchestrator/models.py:173` `def from_dict(cls, data)` -- Build a Spec from a JSON friendly dictionary.
- `Spec.validate` (method) `skills/claude_md_orchestrator/models.py:189` `def validate(self, min_sad_paths)` -- Return the list of DoD violations the spec carries.
- `TestSuite.to_dict` (method) `skills/claude_md_orchestrator/models.py:236` `def to_dict(self)` -- Return a JSON friendly view of the test suite.
- `TestSuite.from_dict` (method) `skills/claude_md_orchestrator/models.py:243` `def from_dict(cls, data)` -- Build a TestSuite from a JSON friendly dictionary.
- `Finding.to_dict` (method) `skills/claude_md_orchestrator/models.py:270` `def to_dict(self)` -- Return a JSON friendly view of the finding.
- `Finding.from_dict` (method) `skills/claude_md_orchestrator/models.py:280` `def from_dict(cls, data)` -- Build a Finding from a JSON friendly dictionary.
- `ReviewReport.blockers` (method) `skills/claude_md_orchestrator/models.py:315` `def blockers(self)` -- Return the list of blocker findings.
- `ReviewReport.to_dict` (method) `skills/claude_md_orchestrator/models.py:319` `def to_dict(self)` -- Return a JSON friendly view of the report.
- `ReviewReport.from_dict` (method) `skills/claude_md_orchestrator/models.py:333` `def from_dict(cls, data)` -- Build a ReviewReport from a JSON friendly dictionary.
- `CicleState.to_dict` (method) `skills/claude_md_orchestrator/models.py:383` `def to_dict(self)` -- Return a JSON friendly view of the state.
- `CicleState.from_dict` (method) `skills/claude_md_orchestrator/models.py:402` `def from_dict(cls, data)` -- Build a CicleState from a JSON friendly dictionary.
- `CicleStateFile.to_dict` (method) `skills/claude_md_orchestrator/models.py:440` `def to_dict(self)` -- Return a JSON friendly view of the state file.
- `CicleStateFile.from_dict` (method) `skills/claude_md_orchestrator/models.py:450` `def from_dict(cls, data)` -- Build a CicleStateFile from a JSON friendly dictionary.
- `CicleStateFile.save` (method) `skills/claude_md_orchestrator/models.py:459` `def save(self, path)` -- Persist the state to disk as pretty JSON.
- `CicleStateFile.load` (method) `skills/claude_md_orchestrator/models.py:467` `def load(cls, path)` -- Read the state from disk.
- `write_jsonl` (function) `skills/claude_md_orchestrator/models.py:480` `def write_jsonl(path, event)` -- Append a single JSONL event to the log file.

## skills/claude_md_orchestrator/orchestrator.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/parser.py`
Imported by: `skills/claude_md_orchestrator/__init__.py`
- `run` (function) `skills/claude_md_orchestrator/orchestrator.py:275` `def run(config, options)` -- Run the orchestrator for the current run directory.
- `summary_to_dict` (function) `skills/claude_md_orchestrator/orchestrator.py:306` `def summary_to_dict(summary)` -- Return a JSON friendly view of the summary.
- `main` (function) `skills/claude_md_orchestrator/orchestrator.py:393` `def main(argv)` -- Run the orchestrator CLI and return the process exit code.

## skills/claude_md_orchestrator/parser.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
Imported by: `pwntomate.py`, `skills/claude_md_orchestrator/orchestrator.py`, `static/js/xterm.js`, `utils.py`
- `flush_body` (function) `skills/claude_md_orchestrator/parser.py:97` `def flush_body()`
- `parse_claude_md` (function) `skills/claude_md_orchestrator/parser.py:167` `def parse_claude_md(path)` -- Parse a CLAUDE.md file and return the list of contracts.
- `load_contracts` (function) `skills/claude_md_orchestrator/parser.py:225` `def load_contracts(config, seeds)` -- Return the contracts the orchestrator should process.

## skills/claude_md_orchestrator/reviewer_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/reviewer_agent.py:171` `def run(state, config)` -- Run the reviewer for one contract.
- `write_report` (function) `skills/claude_md_orchestrator/reviewer_agent.py:225` `def write_report(report, config)` -- Persist the report as JSON inside the run review directory.

## skills/claude_md_orchestrator/sdd_agent.py
Depends on: `modules/llm_factory.py`, `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/sdd_agent.py:204` `def run(contract, config)` -- Run the spec agent for one contract.

## skills/claude_md_orchestrator/tdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
Imported by: `skills/claude_md_orchestrator/bdd_agent.py`
- `run` (function) `skills/claude_md_orchestrator/tdd_agent.py:175` `def run(contract, spec, config)` -- Run the test agent for one contract.
- `read_test_source` (function) `skills/claude_md_orchestrator/tdd_agent.py:228` `def read_test_source(test_path)` -- Return the test source for inspection.


Next: [API_p19.md](API_p19.md)
