# Subsystem: modules (page 6 of 16)
Previous: [KB_modules_p5.md](KB_modules_p5.md)

## modules/fast_run_service.sh
- Doc: LazyOwn service-mode orchestrator.
- Layer: business_logic
- Language: sh
- Symbols:
  - `log_timestamp` (function, line 69)
  - `log_info` (function, line 73)
  - `log_warn` (function, line 77)
  - `log_error` (function, line 81)
  - `require_root` (function, line 89)
  - `require_deps` (function, line 97)
  - `require_paths` (function, line 113)
  - `prepare_runtime_dirs` (function, line 126)
  - `load_config` (function, line 139)
  - `config_truthy` (function, line 155)
  - `pid_file_for` (function, line 166)
  - `log_file_for` (function, line 171)
  - `read_pid_value` (function, line 176)
  - `is_pid_alive` (function, line 189)
  - `is_service_running` (function, line 194)
  - `write_pid_file` (function, line 201)
  - `ensure_log_file` (function, line 211)
  - `spawn_as_target_user` (function, line 228)
  - `spawn_as_root` (function, line 247)
  - `terminate_pid_tree` (function, line 264)
  - `stop_named_service` (function, line 292)
  - `chown_project_tree` (function, line 310)
  - `start_chown_watcher` (function, line 315)
  - `start_lazyc2_service` (function, line 342)
  - `start_www_service` (function, line 356)
  - `start_vpn_service` (function, line 363)
  - `start_discord_service` (function, line 380)
  - `start_telegram_service` (function, line 390)
  - `start_cloudflare_service` (function, line 400)
  - `start_ollama_service` (function, line 410)
  - `managed_services_in_order` (function, line 429)
  - `cmd_start` (function, line 445)
  - `cmd_stop` (function, line 465)
  - `cmd_restart` (function, line 480)
  - `cmd_status` (function, line 486)
  - `cmd_logs` (function, line 505)
  - `cmd_chown_now` (function, line 521)
  - `usage` (function, line 528)
  - `main` (function, line 557)

## modules/finding_lifecycle.py
- Doc: Finding confirmation lifecycle: pending -> confirmed / rejected.
- Layer: utility
- Language: py
- Symbols:
  - `evidence_floor` (function, line 52) `def evidence_floor(items)`
  - `_store_path` (function, line 68) `def _store_path(sessions_dir)`
  - `_load` (function, line 73) `def _load(sessions_dir)`
  - `_save` (function, line 86) `def _save(sessions_dir, data)`
  - `confirm` (function, line 94) `def confirm(finding_id, evidence, sessions_dir, by)`
  - `reject` (function, line 123) `def reject(finding_id, reason, sessions_dir, by)`
  - `add_dead_end` (function, line 137) `def add_dead_end(kind, value, reason, sessions_dir)`
  - `is_dead_end` (function, line 149) `def is_dead_end(kind, value, sessions_dir)`
  - `suppressed_values` (function, line 156) `def suppressed_values(sessions_dir)`
  - `resolve` (function, line 162) `def resolve(node, sessions_dir)`
  - `apply_confirmation` (function, line 190) `def apply_confirmation(nodes, sessions_dir)`
  - `FindingRecord` (class, line 218) `class FindingRecord`
  - `RetestRecord` (class, line 231) `class RetestRecord`
  - `_token_value` (function, line 241) `def _token_value(refs, prefix, default)`
  - `_with_token` (function, line 249) `def _with_token(refs, prefix, value)`
  - `_finding_from_row` (function, line 256) `def _finding_from_row(row)`
  - `record` (function, line 270) `def record(db, workspace, host, title, severity, summary, poc)`
  - `findings_for` (function, line 295) `def findings_for(db, workspace)`
  - `set_status` (function, line 300) `def set_status(db, finding_id, status)`
  - `_retests_path` (function, line 323) `def _retests_path(sessions_dir)`
  - `_load_retests` (function, line 328) `def _load_retests(sessions_dir)`
  - `_save_retests` (function, line 339) `def _save_retests(sessions_dir, payload)`
  - `has_running_retest` (function, line 346) `def has_running_retest(finding_id, sessions_dir)`
  - `request_retest` (function, line 354) `def request_retest(db, finding_id, sessions_dir)`
  - `resolve_retest` (function, line 374) `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)`
  - `classify_retest` (function, line 420) `def classify_retest(needle, output)`
  - `render_markdown` (function, line 439) `def render_markdown(db, workspace, title)`
- Depends on: `modules/osint_enrich.py`
- Imported by: `cli/commands/database.py`, `modules/attack_surface3d.py`, `modules/intel_fusion.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`, `tests/test_finding_lifecycle.py`

## modules/forensic_cleaner.py
- Doc: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- Layer: utility
- Language: py
- Symbols:
  - `ForensicCleanerConfig` (class, line 23) `class ForensicCleanerConfig`
  - `ForensicCleaner` (class, line 57) `class ForensicCleaner`
  - `__init__` (method, line 67) `def __init__(self, config)`
  - `windows_cleanup` (method, line 70) `def windows_cleanup(self)`
  - `linux_cleanup` (method, line 165) `def linux_cleanup(self)`
  - `macos_cleanup` (method, line 193) `def macos_cleanup(self)`
  - `windows_prefetch_parse` (method, line 221) `def windows_prefetch_parse(self, prefetch_path)`
  - `amcache_parse` (method, line 259) `def amcache_parse(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/gcp_attacks.py
- Doc: GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration.
- Layer: utility
- Language: py
- Symbols:
  - `GCPConfig` (class, line 57) `class GCPConfig`
  - `GCPAttackEngine` (class, line 77) `class GCPAttackEngine`
  - `__init__` (method, line 90) `def __init__(self, config)`
  - `enumerate_iam_policy` (method, line 93) `def enumerate_iam_policy(self, resource)`
  - `service_account_impersonation` (method, line 119) `def service_account_impersonation(self)`
  - `cloud_functions_backdoor` (method, line 144) `def cloud_functions_backdoor(self)`
  - `compute_engine_metadata_exfil` (method, line 173) `def compute_engine_metadata_exfil(self)`
  - `gcs_enumeration` (method, line 194) `def gcs_enumeration(self)`
  - `cloudbuild_abuse` (method, line 230) `def cloudbuild_abuse(self)`
  - `organization_escalation` (method, line 261) `def organization_escalation(self)`
  - `summary` (method, line 297) `def summary(self)`
- Imported by: `cli/commands/cloud_attacks.py`

## modules/generate_tools.py
- Layer: utility
- Language: py
- Symbols:
  - `extract_cmd2_tools` (function, line 6) `def extract_cmd2_tools(script_path)`

## modules/goals.py
- Doc: Goal decomposition round-0 with constraints and proof.
- Layer: utility
- Language: py
- Symbols:
  - `GoalSpec` (class, line 20) `class GoalSpec`
  - `TaskConstraints` (class, line 29) `class TaskConstraints`
  - `decompose_rule_based` (function, line 63) `def decompose_rule_based(objective_text, max_goals)`
  - `load_constraints` (function, line 83) `def load_constraints(payload)`
  - `constraint_block_text` (function, line 103) `def constraint_block_text(constraints)`
  - `GoalTracker` (class, line 117) `class GoalTracker`
  - `blocked` (method, line 35) `def blocked(self, command)`
  - `__init__` (method, line 120) `def __init__(self, goals)`
  - `goals` (method, line 125) `def goals(self)`
  - `prove_goal` (method, line 129) `def prove_goal(self, goal_text, evidence)`
  - `goal_met` (method, line 140) `def goal_met(self, opt_in)`
  - `all_achieved` (method, line 148) `def all_achieved(self)`
  - `open_goals` (method, line 152) `def open_goals(self)`
- Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`

## modules/golden_path.py
- Doc: Deterministic attack-path solver over the LazyOwn world model.
- Layer: utility
- Language: py
- Symbols:
  - `_host_node` (function, line 66) `def _host_node(ip)`
  - `_bare` (function, line 78) `def _bare(node)`
  - `_label` (function, line 97) `def _label(node)`
  - `_action_for` (function, line 113) `def _action_for(relation)`
  - `_cost_for_relation` (function, line 135) `def _cost_for_relation(relation, weight)`
  - `build_edges` (function, line 155) `def build_edges(snapshot)`
  - `_source_hosts` (function, line 227) `def _source_hosts(snapshot)`
  - `_diijkstra` (function, line 244) `def _diijkstra(adjacency, source)`
  - `resolve_paths` (function, line 274) `def resolve_paths(snapshot, top_k, source)`
  - `build` (function, line 350) `def build(world_model_path, top_k, sessions_dir)`
  - `_persist` (function, line 381) `def _persist(result, sessions_dir)`
  - `load_artifact` (function, line 401) `def load_artifact(sessions_dir)`
  - `priority_for` (function, line 418) `def priority_for(cost)`
  - `push_objectives` (function, line 433) `def push_objectives(paths, store_path)`
  - `_add` (function, line 167) `def _add(src, dst, relation, weight, evidence, cost)`
- Depends on: `core/logging.py`, `modules/world_model.py`, `skills/lazyown_objective.py`

## modules/gpo_abuse.py
- Doc: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Layer: utility
- Language: py
- Symbols:
  - `GPOInfo` (class, line 54) `class GPOInfo`
  - `GPOAbusePlan` (class, line 83) `class GPOAbusePlan`
  - `GPOAbuseEngine` (class, line 105) `class GPOAbuseEngine`
  - `__init__` (method, line 118) `def __init__(self, domain, dc_ip)`
  - `parse_gpo_list` (method, line 124) `def parse_gpo_list(self, raw_gpo_output)`
  - `parse_bloodhound_gpos` (method, line 160) `def parse_bloodhound_gpos(self, bloodhound_nodes)`
  - `plan_scheduled_task` (method, line 182) `def plan_scheduled_task(self, gpo, command, task_name)`
  - `plan_startup_script` (method, line 208) `def plan_startup_script(self, gpo, script_content, script_name)`
  - `plan_logon_script` (method, line 238) `def plan_logon_script(self, gpo, command)`
  - `plan_local_admin_addition` (method, line 266) `def plan_local_admin_addition(self, gpo, username, group)`
  - `plan_wmi_filter_abuse` (method, line 293) `def plan_wmi_filter_abuse(self, gpo, wmi_query)`
  - `plan_registry_preference` (method, line 322) `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)`
  - `plan_service_installation` (method, line 356) `def plan_service_installation(self, gpo, service_name, binary_path)`
  - `generate_all_plans` (method, line 382) `def generate_all_plans(self, command, username)`
  - `detect_risky_gpos` (method, line 406) `def detect_risky_gpos(self)`
  - `summary` (method, line 434) `def summary(self)`
- Imported by: `cli/commands/active_directory.py`

## modules/gui_askpass.sh
- Doc: — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this...
- Layer: utility
- Language: sh
- Symbols:
  - `has` (function, line 22)
  - `try_zenity` (function, line 24)
  - `try_yad` (function, line 28)
  - `try_ssh_askpass` (function, line 33)
  - `try_kdialog` (function, line 40)

## modules/gym_cleanup.py
- Doc: Gym machine cleanup on LazyOwn exit.
- Layer: utility
- Language: py
- Symbols:
  - `cleanup_enabled` (function, line 21) `def cleanup_enabled()`
  - `cleanup_gym_machines` (function, line 35) `def cleanup_gym_machines(verbose)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/__init__.py`
- Imported by: `lazyown.py`, `tests/test_gym_lifecycle.py`

## modules/gym_matrix_runner.py
- Doc: Ordered Metasploitable 2 gym matrix runner.
- Layer: utility
- Language: py
- Symbols:
  - `_catalogue` (function, line 36) `def _catalogue(catalogue)`
  - `plan_matrix` (function, line 49) `def plan_matrix(target, sessions_dir, only, top_k, catalogue)`
  - `run_matrix` (function, line 104) `def run_matrix(target)`
  - `_stats` (function, line 220) `def _stats(runs)`
  - `_persist` (function, line 236) `def _persist(summary_result, sessions_dir)`
  - `load_matrix` (function, line 252) `def load_matrix(sessions_dir)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/chain_runner.py`

## modules/gym_registry.py
- Doc: Gym definitions and persistent run state.
- Layer: utility
- Language: py
- Symbols:
  - `_yaml_module` (function, line 85) `def _yaml_module()`
  - `slugify` (function, line 92) `def slugify(value)`
  - `validate_definition` (function, line 110) `def validate_definition(data, filename)`
  - `definition_path` (function, line 155) `def definition_path(gym_id, directory)`
  - `_read_yaml` (function, line 178) `def _read_yaml(path)`
  - `_normalize_definition` (function, line 188) `def _normalize_definition(data)`
  - `load_definitions` (function, line 207) `def load_definitions(directory)`
  - `scan_definitions` (function, line 239) `def scan_definitions(directory)`
  - `_write_yaml` (function, line 282) `def _write_yaml(path, data)`
  - `create_definition` (function, line 300) `def create_definition(gym_id)`
  - `update_definition_yaml` (function, line 369) `def update_definition_yaml(gym_id, text, directory)`
  - `delete_definition` (function, line 402) `def delete_definition(gym_id, directory)`
  - `_empty_state` (function, line 442) `def _empty_state()`
  - `_world_model` (function, line 447) `def _world_model()`
  - `_sanitize_state` (function, line 454) `def _sanitize_state(raw)`
  - `normalize_operator` (function, line 495) `def normalize_operator(value)`
  - `read_state` (function, line 501) `def read_state()`
  - `write_state` (function, line 520) `def write_state(state)`
  - `_merge_legacy` (function, line 532) `def _merge_legacy(state)`
  - `_next_run_id` (function, line 569) `def _next_run_id(state)`
  - `start_run` (function, line 579) `def start_run(challenge_id, definitions)`
  - `_matches` (function, line 625) `def _matches(run, selector)`
  - `get_active_runs` (function, line 637) `def get_active_runs(selector, operator)`
  - `select_run` (function, line 663) `def select_run(selector)`
  - `stop_runs` (function, line 695) `def stop_runs(selector)`
  - `pop_run` (function, line 724) `def pop_run(selector)`
  - `state_summary` (function, line 751) `def state_summary()`
  - `new_run_token` (function, line 761) `def new_run_token()`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`, `tests/test_winbox_gym.py`

## modules/gym_winbox_runner.py
- Doc: Ordered WinBox gym matrix runner.
- Layer: utility
- Language: py
- Symbols:
  - `plan_matrix` (function, line 21) `def plan_matrix(target, sessions_dir, only, top_k)`
  - `run_matrix` (function, line 51) `def run_matrix(target)`
  - `report` (function, line 118) `def report(sessions_dir)`
  - `chain_available` (function, line 130) `def chain_available(vuln_id)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_registry.py`

## modules/harness.py
- Doc: Deterministic harness gate for the LazyOwn loop.
- Layer: utility
- Language: py
- Symbols:
  - `harness_enabled` (function, line 30) `def harness_enabled()`
  - `gate` (function, line 65) `def gate(name)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/orchestrator_config.py`
- Imported by: `modules/lazy_loop.py`, `modules/llm_factory.py`, `skills/lazyown_mcp_opencode.py`

## modules/hash_cracker.py
- Doc: Hash cracking pipeline — John the Ripper and Hashcat integration.
- Layer: utility
- Language: py
- Symbols:
  - `CrackResult` (class, line 127) `class CrackResult`
  - `HashIdentifier` (class, line 140) `class HashIdentifier`
  - `HashCracker` (class, line 151) `class HashCracker`
  - `crack_secretsdump_output` (function, line 695) `def crack_secretsdump_output(filepath, wordlist, rhost)`
  - `__init__` (method, line 164) `def __init__(self, wordlist, rules, use_hashcat, timeout)`
  - `_resolve_wordlist` (method, line 178) `def _resolve_wordlist(self)`
  - `identify` (method, line 186) `def identify(self, line)`
  - `identify_file` (method, line 273) `def identify_file(self, filepath)`
  - `crack_hash` (method, line 295) `def crack_hash(self, hash_value, hash_type, wordlist)`
  - `crack_file` (method, line 349) `def crack_file(self, filepath, wordlist, hash_types)`
  - `import_to_db` (method, line 405) `def import_to_db(self, results, rhost, workspace_name)`
  - `_crack_hashcat` (method, line 454) `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_hashcat` (method, line 500) `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)`
  - `_crack_john` (method, line 560) `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_john` (method, line 610) `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)`
  - `_parse_hashcat_output` (method, line 671) `def _parse_hashcat_output(stdout, stderr, original)`
  - `_parse_john_show` (method, line 686) `def _parse_john_show(show_output, original)`
- Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
- Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`

## modules/hive_invoke.py
- Doc: modules/hive_invoke.py
- Layer: utility
- Language: py
- Symbols:
  - `_get_toposwarm` (function, line 50) `def _get_toposwarm()`
  - `_find_claude` (function, line 115) `def _find_claude()`
  - `_parse_argv` (function, line 120) `def _parse_argv(argv)`
  - `_run_print_mode` (function, line 150) `def _run_print_mode(prompt, effort, claude_bin)`
  - `_run_interactive_mode` (function, line 172) `def _run_interactive_mode(prompt, effort, claude_bin)`
  - `_run_toposwarm_mode` (function, line 205) `def _run_toposwarm_mode(prompt, effort, bridge)`
  - `main` (function, line 255) `def main(argv)`
- Depends on: `modules/toposwarm_bridge.py`

## modules/hostdiscover.sh
- Layer: utility
- Language: sh
- Symbols:
  - `extract_ips_from_arp` (function, line 21)
  - `extract_listening_ips_from_netstat` (function, line 26)

## modules/hunt_verify.py
- Doc: Evidence verdict verification for hunting and chain stages.
- Layer: utility
- Language: py
- Symbols:
  - `EventRecord` (class, line 48) `class EventRecord`
  - `StageSpec` (class, line 60) `class StageSpec`
  - `Observation` (class, line 73) `class Observation`
  - `StageAssessment` (class, line 85) `class StageAssessment`
  - `Verification` (class, line 116) `class Verification`
  - `_unique` (function, line 140) `def _unique(values)`
  - `field_present` (function, line 152) `def field_present(fields, field_name)`
  - `_field_present` (function, line 172) `def _field_present(event, field_name)`
  - `_scalar_present` (function, line 177) `def _scalar_present(value)`
  - `_stage_matches` (function, line 188) `def _stage_matches(spec, event)`
  - `validate_specs` (function, line 197) `def validate_specs(specs)`
  - `verify_stages` (function, line 232) `def verify_stages(specs, observations, events, scope_covered)`
  - `_assess_stage` (function, line 310) `def _assess_stage(spec, observations, events, complete, warnings)`
  - `to_dict` (method, line 99) `def to_dict(self)`
  - `chain_proven` (method, line 124) `def chain_proven(self)`
  - `to_dict` (method, line 130) `def to_dict(self)`
- Imported by: `modules/chain_runner.py`, `modules/defense_stages.py`, `tests/test_hunt_verify.py`

## modules/ia_code_analysis.py
- Doc: CodeAnalyzer: Analyzes source code in a directory and its subdirectories.
- Layer: utility
- Language: py
- Symbols:
  - `CodeAnalyzer` (class, line 28) `class CodeAnalyzer`
  - `analyze_with_deepseek` (function, line 66) `def analyze_with_deepseek(code_content, file_path, mode)`
  - `save_results_to_json` (function, line 123) `def save_results_to_json(results, file_path)`
  - `start_analysis` (function, line 169) `def start_analysis(code_dir, mode)`
  - `parse_args` (function, line 178) `def parse_args()`
  - `__init__` (method, line 33) `def __init__(self, mode)`
  - `analyze_directory` (method, line 37) `def analyze_directory(self, directory)`
  - `analyze_code_file` (method, line 49) `def analyze_code_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_logs_analysis.py
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: AGPL v3...
- Layer: utility
- Language: py
- Symbols:
  - `LogFileHandler` (class, line 54) `class LogFileHandler(FileSystemEventHandler)`
  - `analyze_with_deepseek` (function, line 94) `def analyze_with_deepseek(log_content, mode)`
  - `start_monitoring` (function, line 147) `def start_monitoring(log_dir, mode)`
  - `parse_args` (function, line 168) `def parse_args()`
  - `__init__` (method, line 59) `def __init__(self, mode)`
  - `on_modified` (method, line 64) `def on_modified(self, event)`
  - `analyze_log_file` (method, line 75) `def analyze_log_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_network_analysis.py
- Doc: Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: AGPL v3  Descripción: Bot de monitoreo de...
- Layer: utility
- Language: py
- Symbols:
  - `analyze_with_deepseek` (function, line 39) `def analyze_with_deepseek(packet_info, mode)`
  - `packet_callback` (function, line 91) `def packet_callback(packet, mode)`
  - `start_monitoring` (function, line 130) `def start_monitoring(interface, timeout, mode)`
  - `parse_args` (function, line 154) `def parse_args()`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/img2bin.py
- Layer: utility
- Language: py
- Symbols:
  - `imagen_a_binario` (function, line 7) `def imagen_a_binario(imagen_input, binario_output, block_size)`
  - `main` (function, line 43) `def main()`

## modules/intel_fusion.py
- Doc: Sessions attack-intel fusion: data -> information -> intelligence.
- Layer: utility
- Language: py
- Symbols:
  - `_service_cve_matches` (function, line 83) `def _service_cve_matches(service_name, version_text, svc)`
  - `_extract_cve_id` (function, line 133) `def _extract_cve_id(vuln)`
  - `_family_color` (function, line 181) `def _family_color(name)`
  - `node_id` (function, line 192) `def node_id(kind, value)`
  - `_load_json` (function, line 198) `def _load_json(path, default)`
  - `_read_lines` (function, line 208) `def _read_lines(path, limit)`
  - `_host_mentions` (function, line 225) `def _host_mentions(text)`
  - `_file_pagerank` (function, line 230) `def _file_pagerank(ids, pairs, alpha, max_iter, tol)`
  - `build_intel_graph` (function, line 260) `def build_intel_graph(sessions_dir, est_cap)`
  - `_node_doc` (function, line 555) `def _node_doc(node)`
  - `_symbol_list` (function, line 578) `def _symbol_list(node)`
  - `_enrich_readmenator_fields` (function, line 593) `def _enrich_readmenator_fields(nodes, edges)`
  - `group_colors` (function, line 714) `def group_colors(graph)`
  - `page_settings` (function, line 730) `def page_settings(graph)`
  - `build_analytics` (function, line 787) `def build_analytics(graph, summary)`
  - `_fibonacci_sphere` (function, line 821) `def _fibonacci_sphere(count)`
  - `_split_caps` (function, line 837) `def _split_caps(labels, sizes, points, lattice, out)`
  - `_unit` (function, line 866) `def _unit(vec)`
  - `build_bundle_payload` (function, line 874) `def build_bundle_payload(graph)`
  - `bundle_settings` (function, line 990) `def bundle_settings(graph)`
  - `assign_layout` (function, line 1021) `def assign_layout(graph, mode)`
  - `_score_lines` (function, line 1086) `def _score_lines(host_value, detail)`
  - `_recency_lines` (function, line 1109) `def _recency_lines(sessions_dir, host_value)`
  - `_ghost_lines` (function, line 1127) `def _ghost_lines(sessions_dir, host_value)`
  - `write_summary` (function, line 1144) `def write_summary(graph, sessions_dir)`
  - `add_node` (function, line 266) `def add_node(kind, value, label)`
  - `add_edge` (function, line 284) `def add_edge(src, dst, kind, evidence, weight)`
  - `tag_source` (function, line 300) `def tag_source(nid, source)`
- Depends on: `modules/__init__.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`, `modules/lazy_world_diff.py`, `modules/world_model.py`
- Imported by: `lazyc2.py`, `modules/attack_surface3d.py`, `modules/sinks/intel_graph.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_cve_pipeline.py`, `tests/test_intel_fusion.py`

## modules/intelligence_engine.py
- Doc: IntelligenceEngine — unified collection→analysis→intelligence pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `IntelligenceConfig` (class, line 58) `class IntelligenceConfig`
  - `CollectedFact` (class, line 79) `class CollectedFact`
  - `IntelligenceAssessment` (class, line 94) `class IntelligenceAssessment`
  - `CounterIntelFinding` (class, line 109) `class CounterIntelFinding`
  - `IntelligenceEngine` (class, line 120) `class IntelligenceEngine`
  - `get_intelligence_engine` (function, line 1126) `def get_intelligence_engine(config)`
  - `__init__` (method, line 143) `def __init__(self, config)`
  - `_newest_scan_xml_with_versions` (method, line 154) `def _newest_scan_xml_with_versions(self, target)`
  - `_xml_scan_weight` (method, line 177) `def _xml_scan_weight(self, xml_path)`
  - `_xml_has_versions` (method, line 193) `def _xml_has_versions(self, xml_path)`
  - `collect_from_scan` (method, line 197) `def collect_from_scan(self, target)`
  - `_collect_from_scan_xml` (method, line 237) `def _collect_from_scan_xml(self, xml_path, target)`
  - `collect_from_tool` (method, line 326) `def collect_from_tool(self, output, tool, host)`
  - `collect_from_estorides` (method, line 363) `def collect_from_estorides(self, target)`
  - `collect_from_nuclei` (method, line 405) `def collect_from_nuclei(self, target)`
  - `collect_from_yara` (method, line 447) `def collect_from_yara(self, target_path)`
  - `collect_from_factstore` (method, line 486) `def collect_from_factstore(self)`
  - `analyze` (method, line 587) `def analyze(self)`
  - `_correlate_services_to_vulns` (method, line 604) `def _correlate_services_to_vulns(self)`
  - `_match_vulns_versioned` (method, line 649) `def _match_vulns_versioned(self, fact)`
  - `_legacy_match_rows` (method, line 679) `def _legacy_match_rows(self, fact)`
  - `_match_known_vulns` (method, line 708) `def _match_known_vulns(fact)`
  - `_correlate_creds_to_hosts` (method, line 736) `def _correlate_creds_to_hosts(self)`
  - `_correlate_domains_to_infrastructure` (method, line 759) `def _correlate_domains_to_infrastructure(self)`
  - `_rank_targets` (method, line 775) `def _rank_targets(self)`
  - `_detect_killchain_gaps` (method, line 815) `def _detect_killchain_gaps(self)`
  - `produce_intelligence` (method, line 856) `def produce_intelligence(self)`
  - `_map_category_to_mitre` (method, line 871) `def _map_category_to_mitre(category)`
  - `produce_counter_intelligence` (method, line 886) `def produce_counter_intelligence(self)`
  - `disseminate` (method, line 936) `def disseminate(self)`
  - `run_full_cycle` (method, line 1040) `def run_full_cycle(self, target)`
  - `get_intel_report` (method, line 1069) `def get_intel_report(self)`
  - `_is_placeholder` (method, line 1120) `def _is_placeholder(value)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/estorides_importer.py`, `modules/factsio.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/lazy_heat.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
- Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`, `tests/test_single_source_of_truth.py`


Next: [KB_modules_p7.md](KB_modules_p7.md)
