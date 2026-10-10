# API (page 15 of 20)
Previous: [API_p14.md](API_p14.md)

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
- `LazyOwnTUI.main` (method) `poc_tui/app.py:629` `def main()`

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
- `PluginLoader.__init__` (method) `poc_tui/plugin_loader.py:80` `def __init__(self, config, base_dir)`
- `PluginLoader.wrapper` (method) `poc_tui/plugin_loader.py:106` `def wrapper(arg)`
- `PluginLoader.load_all` (method) `poc_tui/plugin_loader.py:128` `def load_all(self)` -- Load yaml addons, lua plugins, and .tool files.
- `PluginLoader.wrapper` (method) `poc_tui/plugin_loader.py:161` `def wrapper(arg)`
- `PluginLoader.wrapper` (method) `poc_tui/plugin_loader.py:258` `def wrapper(arg)`
- `_LuaAppProxy.__init__` (method) `poc_tui/plugin_loader.py:283` `def __init__(self, config)`
- `_LuaAppProxy.params` (method) `poc_tui/plugin_loader.py:287` `def params(self)`
- `_LuaAppProxy.one_cmd` (method) `poc_tui/plugin_loader.py:290` `def one_cmd(self, cmd)`

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
- `MigrationError.find_migrated_sets` (method) `scripts/activate_migrations.py:32` `def find_migrated_sets()` -- Return paths to all *_migrated.py files using PendingCommandSet.
- `MigrationError.extract_command_names` (method) `scripts/activate_migrations.py:42` `def extract_command_names(migrated_path)` -- Extract do_* method names from a migrated CommandSet file.
- `MigrationError.find_in_lazyown` (method) `scripts/activate_migrations.py:52` `def find_in_lazyown(command_names)` -- Return {name: (start_line, end_line)} for commands in lazyown.py.
- `MigrationError.remove_from_lazyown` (method) `scripts/activate_migrations.py:62` `def remove_from_lazyown(locations, dry_run)` -- Remove the specified do_* methods from lazyown.py.
- `MigrationError.activate_migrated_file` (method) `scripts/activate_migrations.py:75` `def activate_migrated_file(migrated_path, dry_run)` -- Change PendingCommandSet to LazyOwnCommandSet in the migrated file.
- `MigrationError.main` (method) `scripts/activate_migrations.py:88` `def main()`

## scripts/backfill_addon_os_trigger.py
- `classify_os` (function) `scripts/backfill_addon_os_trigger.py:104` `def classify_os(filename)` -- Return a MITRE-platform string for the addon based on filename.
- `known_trigger` (function) `scripts/backfill_addon_os_trigger.py:121` `def known_trigger(name)` -- Return the curated trigger tuple for an addon, or ``()``.
- `render_trigger` (function) `scripts/backfill_addon_os_trigger.py:127` `def render_trigger(trigger)` -- Render the trigger field as inline YAML matching the project style.
- `patch` (function) `scripts/backfill_addon_os_trigger.py:141` `def patch(path)` -- Return the new file content with ``os`` and ``trigger`` inserted.
- `main` (function) `scripts/backfill_addon_os_trigger.py:175` `def main()` -- Walk every addon and rewrite files that need backfilling.

## scripts/check_contract_manifest.py
Imported by: `tests/test_contract_manifest.py`
- `ManifestConfig.check_manifest` (method) `scripts/check_contract_manifest.py:176` `def check_manifest(config)` -- Return the list of documented contracts that are missing on disk.
- `ManifestConfig.main` (method) `scripts/check_contract_manifest.py:229` `def main(argv)` -- Run the manifest check and return the process exit code.

## scripts/devtools/command_audit.py
Depends on: `lazyown.py`
- `AuditConfig.argparser_commands` (method) `scripts/devtools/command_audit.py:40` `def argparser_commands(config)` -- Return the command names decorated with ``@with_argparser``.
- `AuditConfig.audit` (method) `scripts/devtools/command_audit.py:65` `def audit(config)` -- Run the dispatch and parser audit.
- `AuditConfig.main` (method) `scripts/devtools/command_audit.py:105` `def main(argv)` -- Run the audit and return the process exit code.

## scripts/devtools/core_smoke.py
Depends on: `core/hardening.py`, `core/payload_schema.py`, `modules/db.py`, `modules/killchain.py`, `modules/payload_factory.py`
- `SmokeConfig.check_surfaces` (method) `scripts/devtools/core_smoke.py:64` `def check_surfaces(config)` -- Return the dotted names that are missing from the imported modules.
- `SmokeConfig.check_calls` (method) `scripts/devtools/core_smoke.py:81` `def check_calls()` -- Exercise a small safe subset of the public API.
- `SmokeConfig.main` (method) `scripts/devtools/core_smoke.py:118` `def main()` -- Run the smoke check and return the process exit code.

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
- `Journal.main` (method) `scripts/journal.py:264` `def main(argv)` -- Run the journal CLI and return the process exit code.

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
- `ACIReflector.mcp_aci_plan` (method) `skills/aci_planner.py:865` `def mcp_aci_plan(goal, target, scope, domain, os_hint, phase_filter)` -- Plan an engagement goal and return a JSON summary.
- `ACIReflector.mcp_aci_status` (method) `skills/aci_planner.py:923` `def mcp_aci_status()` -- Return live status of the active ACI plan as JSON.
- `ACIReflector.mcp_aci_replan` (method) `skills/aci_planner.py:940` `def mcp_aci_replan(reason)` -- Force adaptive replanning of the active ACI plan.
- `ACIReflector.main` (method) `skills/aci_planner.py:1003` `def main(argv)` -- Entry point for CLI usage.

## skills/autonomous_daemon.py
Depends on: `core/logging.py`, `modules/detection_oracle.py`, `modules/event_consumers.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/obs_parser.py`, `modules/pipeline_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/world_model.py`, `skills/daemon_control.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`
Imported by: `cli/commands/session_ops.py`, `modules/pipeline_engine.py`, `skills/autonomous_replay.py`, `skills/lazyown_mcp.py`, `skills/tests/test_autonomous_daemon.py`, `skills/unified_orchestrator.py`, `tests/test_autonomous_replay.py`, `tests/test_engage_orchestrator.py`, `tests/test_metrics_aware_selector.py`, `tests/test_moe_rl_swan.py`, `tests/test_pipeline_engine.py`, `tests/test_scope_bound_auto_gate.py`
- `compute_decision_seed` (function) `skills/autonomous_daemon.py:272` `def compute_decision_seed(objective_id, step_n, source)` -- Return a deterministic identifier for a daemon decision.
- `ICommandRunner.run` (method) `skills/autonomous_daemon.py:304` `def run(self, command, timeout)` -- Execute command within timeout seconds.
- `ICommandRunner.name` (method) `skills/autonomous_daemon.py:309` `def name(self)` -- Human-readable identifier for this runner.
- `MCPCommandRunner.name` (method) `skills/autonomous_daemon.py:320` `def name(self)`
- `MCPCommandRunner.run` (method) `skills/autonomous_daemon.py:323` `def run(self, command, timeout)` -- Try to import and call the MCP runner.
- `PTYCommandRunner.name` (method) `skills/autonomous_daemon.py:338` `def name(self)`
- `PTYCommandRunner.run` (method) `skills/autonomous_daemon.py:341` `def run(self, command, timeout)` -- Execute command via PTY.
- `CommandRunnerChain.__init__` (method) `skills/autonomous_daemon.py:425` `def __init__(self, runners)`
- `CommandRunnerChain.name` (method) `skills/autonomous_daemon.py:431` `def name(self)`
- `CommandRunnerChain.run` (method) `skills/autonomous_daemon.py:434` `def run(self, command, timeout)` -- Try each runner in sequence.
- `ICommandSelector.select` (method) `skills/autonomous_daemon.py:522` `def select(self, target, phase, context)` -- Return a CommandDecision or None if this selector has no suggestion.
- `ReactiveSelector.__init__` (method) `skills/autonomous_daemon.py:537` `def __init__(self, reactive_engine)`
- `ReactiveSelector.register_output` (method) `skills/autonomous_daemon.py:541` `def register_output(self, output, command, platform)` -- Feed reactive engine with last command output to generate new decisions.
- `ReactiveSelector.select` (method) `skills/autonomous_daemon.py:568` `def select(self, target, phase, context)` -- Pop and return the pending reactive decision if present.
- `ParquetSelector.__init__` (method) `skills/autonomous_daemon.py:583` `def __init__(self, pdb, fail_counts)`
- `ParquetSelector.select` (method) `skills/autonomous_daemon.py:587` `def select(self, target, phase, context)` -- Return the most-frequent successful command for this phase.
- `BridgeSelector.__init__` (method) `skills/autonomous_daemon.py:629` `def __init__(self, dispatcher, fail_counts)`
- `BridgeSelector.select` (method) `skills/autonomous_daemon.py:633` `def select(self, target, phase, context)` -- Return a bridge catalog suggestion for this phase.
- `LLMSelector.select` (method) `skills/autonomous_daemon.py:699` `def select(self, target, phase, context)` -- Return an LLM-suggested command with catalog context, or None if disabled.
- `SWANSelector.select` (method) `skills/autonomous_daemon.py:792` `def select(self, target, phase, context)` -- Ask the best MoE expert for a command recommendation.
- `FallbackSelector.select` (method) `skills/autonomous_daemon.py:838` `def select(self, target, phase, context)` -- Return the static fallback command for this phase.
- `MetricsAwareSelector.__init__` (method) `skills/autonomous_daemon.py:875` `def __init__(self, wrapped, metrics_source, min_success_rate, min_attempts, window_seconds, cache_ttl_s, clock)` -- Initialise the decorator.
- `MetricsAwareSelector.wrapped` (method) `skills/autonomous_daemon.py:921` `def wrapped(self)` -- Return the underlying selector for introspection in tests.
- `MetricsAwareSelector.select` (method) `skills/autonomous_daemon.py:1007` `def select(self, target, phase, context)` -- Honour the :class:`ICommandSelector` contract.
- `CredentialSpraySelector.__init__` (method) `skills/autonomous_daemon.py:1108` `def __init__(self, fail_counts)`
- `CredentialSpraySelector.select` (method) `skills/autonomous_daemon.py:1112` `def select(self, target, phase, context)` -- Return a spray command when credentials + matching service are available.
- `CascadeStrategy.__init__` (method) `skills/autonomous_daemon.py:1148` `def __init__(self, selectors)`
- `CascadeStrategy.next_command` (method) `skills/autonomous_daemon.py:1151` `def next_command(self, target, phase, context)` -- Try each selector in order.
- `StrategyEngine.__init__` (method) `skills/autonomous_daemon.py:1186` `def __init__(self, runner, selectors)`
- `StrategyEngine.register_output` (method) `skills/autonomous_daemon.py:1213` `def register_output(self, output, command, platform, success)` -- Feed the reactive selector with the last command output.
- `StrategyEngine.next_command` (method) `skills/autonomous_daemon.py:1227` `def next_command(self, target, phase, services, os_hint)` -- Select the next command for target/phase using the cascade.
- `IObjectiveHandler.handle` (method) `skills/autonomous_daemon.py:1261` `def handle(self, objective_id, objective_text, target, context)` -- Execute objective and return a list of step results.
- `ExecutionEngine.__init__` (method) `skills/autonomous_daemon.py:1283` `def __init__(self, strategy, max_steps, world_model, obs_parser, facts, loop)`
- `ExecutionEngine.handle` (method) `skills/autonomous_daemon.py:1299` `def handle(self, objective_id, objective_text, target, context)` -- Synchronous entry point.
- `ExecutionEngine.run_async` (method) `skills/autonomous_daemon.py:1309` `def run_async(self, objective_id, objective_text, target)` -- Asyncio entry point used by objective_loop.
- `DroneCoordinator.__init__` (method) `skills/autonomous_daemon.py:2260` `def __init__(self)`
- `DroneCoordinator.process_findings` (method) `skills/autonomous_daemon.py:2265` `def process_findings(self, findings, target, objective_id, payload_key)` -- Launch drones for relevant findings.
- `EnginePhaseResult.did_switch` (method) `skills/autonomous_daemon.py:2469` `def did_switch(self)` -- True when the orchestrator used a fallback tool.
- `IToolFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:2478` `def next_tool(self, failed_command, phase, attempt)` -- Return the next candidate command or None when exhausted.
- `StaticFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:2495` `def next_tool(self, failed_command, phase, attempt)`
- `BridgeFallbackResolver.__init__` (method) `skills/autonomous_daemon.py:2517` `def __init__(self, dispatcher)`
- `BridgeFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:2542` `def next_tool(self, failed_command, phase, attempt)`
- `_ShellDetector.__init__` (method) `skills/autonomous_daemon.py:2569` `def __init__(self, narrator)`
- `_ShellDetector.poll` (method) `skills/autonomous_daemon.py:2574` `def poll(self, target)` -- Return the newly-detected client_ids since the previous poll.
- `_ShellDetector.detect_in_output` (method) `skills/autonomous_daemon.py:2615` `def detect_in_output(self, output, target)` -- Return True when a shell/root-shell signal appears in command output.
- `EngageOrchestrator.__init__` (method) `skills/autonomous_daemon.py:2661` `def __init__(self, target, runner, narrator, approval_gate, fallback_resolver, shell_detector, plan...`
- `EngageOrchestrator.engagement_id` (method) `skills/autonomous_daemon.py:2697` `def engagement_id(self)` -- Stable id for this engagement (correlates events in logs).
- `EngageOrchestrator.run` (method) `skills/autonomous_daemon.py:2701` `def run(self)` -- Drive the full plan against the configured target.
- `EngageOrchestrator.mcp_engage_target` (method) `skills/autonomous_daemon.py:3029` `def mcp_engage_target(target, max_switches_per_step, detach, auto)` -- Public MCP / CLI entry point for the engage verb.
- `EngageOrchestrator.mcp_engage_status` (method) `skills/autonomous_daemon.py:3119` `def mcp_engage_status(last_n)` -- Return the last N lines of sessions/engagement.log plus pending approvals.
- `EngageOrchestrator.mcp_engage_approve` (method) `skills/autonomous_daemon.py:3145` `def mcp_engage_approve(approval_id, decision, operator)` -- Resolve a pending approval. decision must be 'approved' or 'denied'.
- `EngageOrchestrator.mcp_engage_list_pending` (method) `skills/autonomous_daemon.py:3170` `def mcp_engage_list_pending()` -- List every pending approval awaiting an operator decision.
- `EngageOrchestrator.cmd_engage` (method) `skills/autonomous_daemon.py:3188` `def cmd_engage(target, max_switches_per_step, detach)` -- CLI helper bound to the `engage <ip>` daemon subcommand.
- `EngageOrchestrator.objective_loop` (method) `skills/autonomous_daemon.py:3227` `def objective_loop(max_steps, loop)` -- Root autonomous loop: takes pending objectives from objectives.jsonl and executes them without waiting for Claude...
- `EngageOrchestrator.world_model_watcher` (method) `skills/autonomous_daemon.py:3350` `def world_model_watcher(loop)` -- Watch world_model.json.
- `EngageOrchestrator.heartbeat_loop` (method) `skills/autonomous_daemon.py:3535` `def heartbeat_loop()` -- Emit heartbeat and write status every HEARTBEAT_S seconds.
- `EngageOrchestrator.cmd_run` (method) `skills/autonomous_daemon.py:3662` `def cmd_run(max_steps)` -- Run daemon in foreground (debug mode).
- `EngageOrchestrator.cmd_start` (method) `skills/autonomous_daemon.py:3671` `def cmd_start(max_steps)` -- Fork, detach, and run daemon in background.
- `EngageOrchestrator.cmd_stop` (method) `skills/autonomous_daemon.py:3701` `def cmd_stop()` -- Send SIGTERM to the running daemon.
- `EngageOrchestrator.cmd_status` (method) `skills/autonomous_daemon.py:3718` `def cmd_status()` -- Print current daemon status to stdout.
- `EngageOrchestrator.cmd_inject` (method) `skills/autonomous_daemon.py:3734` `def cmd_inject(text, priority)` -- Inject an objective from the CLI.
- `EngageOrchestrator.mcp_autonomous_start` (method) `skills/autonomous_daemon.py:3759` `def mcp_autonomous_start(max_steps, backend)` -- Start the autonomous daemon in a background thread (for MCP calls).
- `EngageOrchestrator.mcp_autonomous_stop` (method) `skills/autonomous_daemon.py:3801` `def mcp_autonomous_stop()` -- Stop the autonomous daemon.
- `EngageOrchestrator.mcp_autonomous_status` (method) `skills/autonomous_daemon.py:3817` `def mcp_autonomous_status()` -- Current daemon state: objectives, steps, drones, phase.
- `EngageOrchestrator.mcp_autonomous_inject` (method) `skills/autonomous_daemon.py:3830` `def mcp_autonomous_inject(text, priority, target)` -- Inject an objective into the daemon queue and into sessions/tasks.json.
- `EngageOrchestrator.mcp_autonomous_events` (method) `skills/autonomous_daemon.py:3874` `def mcp_autonomous_events(last_n)` -- Read the last N events from autonomous_events.jsonl.

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
- `ReplayDispatcher.replay` (method) `skills/autonomous_replay.py:473` `def replay(from_event_id, to_event_id, mode, events_path, runner, timeout)` -- Convenience entry point used by the MCP tool layer.

## skills/claude_md_orchestrator/bdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`
- `BddResult.run` (method) `skills/claude_md_orchestrator/bdd_agent.py:151` `def run(contract, spec, suite, config)` -- Run the implementation agent for one contract.

## skills/claude_md_orchestrator/boy_scout.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `ScoutReport.run` (method) `skills/claude_md_orchestrator/boy_scout.py:90` `def run(state, config)` -- Run the boy scout pass for one contract.
- `ScoutReport.write_report` (method) `skills/claude_md_orchestrator/boy_scout.py:110` `def write_report(report, config)` -- Persist the boy scout proposal to disk.

## skills/claude_md_orchestrator/cicd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `CicdResult.run` (method) `skills/claude_md_orchestrator/cicd_agent.py:176` `def run(contract, spec, report, config)` -- Run the CI and CD agent for one contract.

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
- `Config.load_config` (method) `skills/claude_md_orchestrator/config.py:155` `def load_config()` -- Build a Config from environment variables and return it.
- `Config.resolve_optional` (method) `skills/claude_md_orchestrator/config.py:164` `def resolve_optional(config, key)` -- Return the environment value for a key or None when missing.

## skills/claude_md_orchestrator/documentation_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `DocResult.run` (method) `skills/claude_md_orchestrator/documentation_agent.py:123` `def run(contract, spec, report, config)` -- Run the documentation agent for one contract.

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
- `CicleStateFile.write_jsonl` (method) `skills/claude_md_orchestrator/models.py:480` `def write_jsonl(path, event)` -- Append a single JSONL event to the log file.

## skills/claude_md_orchestrator/orchestrator.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/parser.py`
Imported by: `skills/claude_md_orchestrator/__init__.py`
- `CycleSummary.run` (method) `skills/claude_md_orchestrator/orchestrator.py:275` `def run(config, options)` -- Run the orchestrator for the current run directory.
- `CycleSummary.summary_to_dict` (method) `skills/claude_md_orchestrator/orchestrator.py:306` `def summary_to_dict(summary)` -- Return a JSON friendly view of the summary.
- `CycleSummary.main` (method) `skills/claude_md_orchestrator/orchestrator.py:393` `def main(argv)` -- Run the orchestrator CLI and return the process exit code.

## skills/claude_md_orchestrator/parser.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
Imported by: `pwntomate.py`, `skills/claude_md_orchestrator/orchestrator.py`, `static/js/xterm.js`, `utils.py`
- `_Section.flush_body` (method) `skills/claude_md_orchestrator/parser.py:97` `def flush_body()`
- `_Section.parse_claude_md` (method) `skills/claude_md_orchestrator/parser.py:167` `def parse_claude_md(path)` -- Parse a CLAUDE.md file and return the list of contracts.
- `_Section.load_contracts` (method) `skills/claude_md_orchestrator/parser.py:225` `def load_contracts(config, seeds)` -- Return the contracts the orchestrator should process.

## skills/claude_md_orchestrator/reviewer_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `AnalyzerResult.run` (method) `skills/claude_md_orchestrator/reviewer_agent.py:171` `def run(state, config)` -- Run the reviewer for one contract.
- `AnalyzerResult.write_report` (method) `skills/claude_md_orchestrator/reviewer_agent.py:225` `def write_report(report, config)` -- Persist the report as JSON inside the run review directory.

## skills/claude_md_orchestrator/sdd_agent.py
Depends on: `modules/llm_factory.py`, `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `SddResult.run` (method) `skills/claude_md_orchestrator/sdd_agent.py:204` `def run(contract, config)` -- Run the spec agent for one contract.

## skills/claude_md_orchestrator/tdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
Imported by: `skills/claude_md_orchestrator/bdd_agent.py`
- `TddResult.run` (method) `skills/claude_md_orchestrator/tdd_agent.py:175` `def run(contract, spec, config)` -- Run the test agent for one contract.
- `TddResult.read_test_source` (method) `skills/claude_md_orchestrator/tdd_agent.py:228` `def read_test_source(test_path)` -- Return the test source for inspection.

## skills/claude_md_orchestrator/validators.py
Depends on: `skills/claude_md_orchestrator/models.py`
Imported by: `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`
- `CheckResult.passed` (method) `skills/claude_md_orchestrator/validators.py:76` `def passed(self)` -- Return True when the result has no findings.
- `CheckResult.blocks` (method) `skills/claude_md_orchestrator/validators.py:80` `def blocks(self)` -- Return the blocker findings only.
- `CheckResult.find_block_comments` (method) `skills/claude_md_orchestrator/validators.py:85` `def find_block_comments(source)` -- Return the start and end line of every block comment in source.
- `CheckResult.find_inline_comments` (method) `skills/claude_md_orchestrator/validators.py:107` `def find_inline_comments(source)` -- Return the line numbers of every inline comment in source.
- `CheckResult.check_no_comments` (method) `skills/claude_md_orchestrator/validators.py:124` `def check_no_comments(source, path)` -- Return a finding for every comment in the source code.
- `CheckResult.check_no_emoji` (method) `skills/claude_md_orchestrator/validators.py:155` `def check_no_emoji(content, path)` -- Return a finding for every emoji the content carries.
- `CheckResult.check_no_forbidden_markers` (method) `skills/claude_md_orchestrator/validators.py:177` `def check_no_forbidden_markers(content, path)` -- Return a finding for every TODO, FIXME, XXX, or HACK marker.
- `CheckResult.check_english_only` (method) `skills/claude_md_orchestrator/validators.py:194` `def check_english_only(source, path)` -- Return a finding for every Spanish hint the source carries.
- `CheckResult.check_docstrings` (method) `skills/claude_md_orchestrator/validators.py:218` `def check_docstrings(source, path)` -- Return a finding for every public function or class without a docstring.
- `CheckResult.check_no_hardcoded_paths_or_ips` (method) `skills/claude_md_orchestrator/validators.py:259` `def check_no_hardcoded_paths_or_ips(source, path)` -- Return a finding for every absolute path or IP literal.
- `CheckResult.check_magic_numbers` (method) `skills/claude_md_orchestrator/validators.py:293` `def check_magic_numbers(source, path, allow)` -- Return a finding for every numeric literal that is not in the allow list.
- `CheckResult.check_source` (method) `skills/claude_md_orchestrator/validators.py:328` `def check_source(source, path, allow_numbers)` -- Run every source level DoD check and return the findings.
- `CheckResult.check_markdown` (method) `skills/claude_md_orchestrator/validators.py:341` `def check_markdown(content, path)` -- Run every markdown level DoD check and return the findings.
- `CheckResult.check_spec` (method) `skills/claude_md_orchestrator/validators.py:350` `def check_spec(spec, min_sad_paths)` -- Run the spec level DoD check and return the findings.

## skills/daemon_control.py
Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_daemon_control.py`
- `PendingAction.is_expired` (method) `skills/daemon_control.py:79` `def is_expired(self, now)` -- Return ``True`` when a still-pending action has exceeded its TTL.
- `ControlState.to_dict` (method) `skills/daemon_control.py:110` `def to_dict(self)` -- Serialise the state to a plain JSON-ready dict.
- `ControlState.from_dict` (method) `skills/daemon_control.py:121` `def from_dict(cls, data)` -- Build a state from JSON data, sanitising malformed input.
- `DaemonControl.__init__` (method) `skills/daemon_control.py:171` `def __init__(self, sessions_dir)` -- Pin the control file to ``<sessions_dir>/daemon_control.json``.
- `DaemonControl.path` (method) `skills/daemon_control.py:184` `def path(self)` -- Absolute path of the control file on disk.
- `DaemonControl.load` (method) `skills/daemon_control.py:188` `def load(self)` -- Return the current state or defaults when the file is missing.
- `DaemonControl.save` (method) `skills/daemon_control.py:201` `def save(self, state)` -- Persist ``state`` atomically.
- `DaemonControl.set_mode` (method) `skills/daemon_control.py:231` `def set_mode(self, mode)` -- Switch between :data:`MODE_AUTO`, :data:`MODE_APPROVAL`, :data:`MODE_PAUSED`.
- `DaemonControl.pause` (method) `skills/daemon_control.py:240` `def pause(self)` -- Convenience wrapper for ``set_mode(MODE_PAUSED)``.
- `DaemonControl.resume` (method) `skills/daemon_control.py:244` `def resume(self)` -- Convenience wrapper for ``set_mode(MODE_AUTO)``.
- `DaemonControl.require_approval` (method) `skills/daemon_control.py:248` `def require_approval(self)` -- Convenience wrapper for ``set_mode(MODE_APPROVAL)``.
- `DaemonControl.add_veto` (method) `skills/daemon_control.py:252` `def add_veto(self, command_token)` -- Append a first-token name to the veto list.
- `DaemonControl.remove_veto` (method) `skills/daemon_control.py:267` `def remove_veto(self, command_token)` -- Remove a previously vetoed command from the list.
- `DaemonControl.clear_vetoes` (method) `skills/daemon_control.py:275` `def clear_vetoes(self)` -- Remove every entry from the veto list.
- `DaemonControl.set_focus` (method) `skills/daemon_control.py:282` `def set_focus(self, targets)` -- Replace the focus-target list.
- `DaemonControl.propose` (method) `skills/daemon_control.py:290` `def propose(self, command)` -- Daemon-side: register a pending action awaiting approval.
- `DaemonControl.decide` (method) `skills/daemon_control.py:317` `def decide(self, action_id, decision)` -- Operator-side: approve or veto the pending action.
- `DaemonControl.consume` (method) `skills/daemon_control.py:343` `def consume(self, action_id)` -- Daemon-side: read the final decision and clear the slot.
- `DaemonControl.is_paused` (method) `skills/daemon_control.py:375` `def is_paused(self)` -- Return ``True`` when the daemon must stop before executing.
- `DaemonControl.is_vetoed` (method) `skills/daemon_control.py:379` `def is_vetoed(self, command)` -- Return ``True`` when the command's first token is in the veto list.
- `DaemonControl.target_in_focus` (method) `skills/daemon_control.py:386` `def target_in_focus(self, target)` -- Return ``True`` when no focus is configured or ``target`` is in focus.
- `DaemonControl.wait_for_decision` (method) `skills/daemon_control.py:394` `def wait_for_decision(control, action)` -- Block until the operator decides or the TTL expires.
- `DaemonControl.wait_until_unpaused` (method) `skills/daemon_control.py:445` `def wait_until_unpaused(control)` -- Block while the daemon is paused, returning when it resumes.

## skills/daemon_health.py
Imported by: `lazyc2.py`
- `is_daemon_alive` (function) `skills/daemon_health.py:36` `def is_daemon_alive(timeout)` -- Check whether the autonomous daemon wrote a heartbeat recently.
- `daemon_status` (function) `skills/daemon_health.py:58` `def daemon_status(timeout)` -- Return the full daemon health snapshot.
- `DaemonHealth.__init__` (method) `skills/daemon_health.py:102` `def __init__(self, interval, health_file)`
- `DaemonHealth.error_count` (method) `skills/daemon_health.py:114` `def error_count(self)`
- `DaemonHealth.error_count` (method) `skills/daemon_health.py:119` `def error_count(self, value)`
- `DaemonHealth.phase` (method) `skills/daemon_health.py:124` `def phase(self)`
- `DaemonHealth.phase` (method) `skills/daemon_health.py:129` `def phase(self, value)`
- `DaemonHealth.start` (method) `skills/daemon_health.py:155` `def start(self)` -- Launch the heartbeat thread.
- `DaemonHealth.stop` (method) `skills/daemon_health.py:164` `def stop(self)` -- Stop the heartbeat thread.
- `DaemonHealth.record_error` (method) `skills/daemon_health.py:175` `def record_error(self)` -- Increment the error counter.
- `DaemonHealth.set_phase` (method) `skills/daemon_health.py:180` `def set_phase(self, phase)` -- Update the current daemon phase.
- `DaemonHealth.increment_cycles` (method) `skills/daemon_health.py:185` `def increment_cycles(self)` -- Increment the completed cycles counter.

## skills/heartbeat.py
Depends on: `modules/event_engine.py`, `modules/session_state.py`, `modules/timeline_narrator.py`
- `write_pid` (function) `skills/heartbeat.py:53` `def write_pid()`
- `clear_pid` (function) `skills/heartbeat.py:57` `def clear_pid()`
- `is_running` (function) `skills/heartbeat.py:62` `def is_running()` -- Return (is_running, pid).
- `run_loop` (function) `skills/heartbeat.py:74` `def run_loop(interval, once)`
- `main` (function) `skills/heartbeat.py:127` `def main()`

## skills/hermes-lazyown/claudemd_rules.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `RuleSetBuilder.__init__` (method) `skills/hermes-lazyown/claudemd_rules.py:24` `def __init__(self)`
- `RuleSetBuilder.with_phase` (method) `skills/hermes-lazyown/claudemd_rules.py:31` `def with_phase(self, phase)` -- Set the current engagement phase.
- `RuleSetBuilder.with_target` (method) `skills/hermes-lazyown/claudemd_rules.py:36` `def with_target(self, rhost)` -- Set the active target IP.
- `RuleSetBuilder.with_services` (method) `skills/hermes-lazyown/claudemd_rules.py:41` `def with_services(self, services)` -- Set discovered services (e.g., ['http:80', 'smb:445']).
- `RuleSetBuilder.with_creds` (method) `skills/hermes-lazyown/claudemd_rules.py:46` `def with_creds(self, found)` -- Set whether credentials have been discovered.
- `RuleSetBuilder.with_hermes` (method) `skills/hermes-lazyown/claudemd_rules.py:51` `def with_hermes(self, is_hermes)` -- Set whether running inside a Hermes session.
- `RuleSetBuilder.build` (method) `skills/hermes-lazyown/claudemd_rules.py:56` `def build(self)` -- Build and return the complete rule set markdown.
- `RuleSetBuilder.generate_rules` (method) `skills/hermes-lazyown/claudemd_rules.py:185` `def generate_rules(phase, rhost, services, creds_found, is_hermes)` -- Convenience function: build a rule set from parameters.

## skills/hermes-lazyown/config_bridge.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `ConfigBridge.__init__` (method) `skills/hermes-lazyown/config_bridge.py:35` `def __init__(self, payload_path)`
- `ConfigBridge.get` (method) `skills/hermes-lazyown/config_bridge.py:42` `def get(self, key, default)` -- Return the value for *key*, or *default* if not found anywhere.
- `ConfigBridge.get_required` (method) `skills/hermes-lazyown/config_bridge.py:46` `def get_required(self, key)` -- Return the value for *key*, raising ConfigBridgeError if missing.
- `ConfigBridge.get_str` (method) `skills/hermes-lazyown/config_bridge.py:53` `def get_str(self, key, default)` -- Return the string value for *key*.
- `ConfigBridge.get_int` (method) `skills/hermes-lazyown/config_bridge.py:58` `def get_int(self, key, default)` -- Return the integer value for *key*.
- `ConfigBridge.get_bool` (method) `skills/hermes-lazyown/config_bridge.py:66` `def get_bool(self, key, default)` -- Return the boolean value for *key*.
- `ConfigBridge.refresh` (method) `skills/hermes-lazyown/config_bridge.py:75` `def refresh(self)` -- Invalidate all caches so the next read reloads from disk.
- `ConfigBridge.active_target` (method) `skills/hermes-lazyown/config_bridge.py:80` `def active_target(self)` -- Return a dict with the minimal target context (rhost, domain, os_id).
- `ConfigBridge.attacker_context` (method) `skills/hermes-lazyown/config_bridge.py:90` `def attacker_context(self)` -- Return a dict with the attacker context (lhost, lport, etc.).
- `ConfigBridge.is_hermes_session` (method) `skills/hermes-lazyown/config_bridge.py:99` `def is_hermes_session(self)` -- Return True if running inside a Hermes agent session.


Next: [API_p16.md](API_p16.md)
