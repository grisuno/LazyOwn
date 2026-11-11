# Symbols (page 15 of 51)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `is_hard_stop` | method | `modules/failure_verdict.py:126` | `def is_hard_stop(self)` |
| `chown_project_tree` | function | `modules/fast_run_service.sh:310` | `` |
| `cmd_chown_now` | function | `modules/fast_run_service.sh:521` | `` |
| `cmd_logs` | function | `modules/fast_run_service.sh:505` | `` |
| `cmd_restart` | function | `modules/fast_run_service.sh:480` | `` |
| `cmd_start` | function | `modules/fast_run_service.sh:445` | `` |
| `cmd_status` | function | `modules/fast_run_service.sh:486` | `` |
| `cmd_stop` | function | `modules/fast_run_service.sh:465` | `` |
| `config_truthy` | function | `modules/fast_run_service.sh:155` | `` |
| `ensure_log_file` | function | `modules/fast_run_service.sh:211` | `` |
| `is_pid_alive` | function | `modules/fast_run_service.sh:189` | `` |
| `is_service_running` | function | `modules/fast_run_service.sh:194` | `` |
| `load_config` | function | `modules/fast_run_service.sh:139` | `` |
| `log_error` | function | `modules/fast_run_service.sh:81` | `` |
| `log_file_for` | function | `modules/fast_run_service.sh:171` | `` |
| `log_info` | function | `modules/fast_run_service.sh:73` | `` |
| `log_timestamp` | function | `modules/fast_run_service.sh:69` | `` |
| `log_warn` | function | `modules/fast_run_service.sh:77` | `` |
| `main` | function | `modules/fast_run_service.sh:557` | `` |
| `managed_services_in_order` | function | `modules/fast_run_service.sh:429` | `` |
| `pid_file_for` | function | `modules/fast_run_service.sh:166` | `` |
| `prepare_runtime_dirs` | function | `modules/fast_run_service.sh:126` | `` |
| `read_pid_value` | function | `modules/fast_run_service.sh:176` | `` |
| `require_deps` | function | `modules/fast_run_service.sh:97` | `` |
| `require_paths` | function | `modules/fast_run_service.sh:113` | `` |
| `require_root` | function | `modules/fast_run_service.sh:89` | `` |
| `spawn_as_root` | function | `modules/fast_run_service.sh:247` | `` |
| `spawn_as_target_user` | function | `modules/fast_run_service.sh:228` | `` |
| `start_chown_watcher` | function | `modules/fast_run_service.sh:315` | `` |
| `start_cloudflare_service` | function | `modules/fast_run_service.sh:400` | `` |
| `start_discord_service` | function | `modules/fast_run_service.sh:380` | `` |
| `start_lazyc2_service` | function | `modules/fast_run_service.sh:342` | `` |
| `start_ollama_service` | function | `modules/fast_run_service.sh:410` | `` |
| `start_telegram_service` | function | `modules/fast_run_service.sh:390` | `` |
| `start_vpn_service` | function | `modules/fast_run_service.sh:363` | `` |
| `start_www_service` | function | `modules/fast_run_service.sh:356` | `` |
| `stop_named_service` | function | `modules/fast_run_service.sh:292` | `` |
| `terminate_pid_tree` | function | `modules/fast_run_service.sh:264` | `` |
| `usage` | function | `modules/fast_run_service.sh:528` | `` |
| `write_pid_file` | function | `modules/fast_run_service.sh:201` | `` |
| `FindingRecord` | class | `modules/finding_lifecycle.py:218` | `class FindingRecord` |
| `RetestRecord` | class | `modules/finding_lifecycle.py:231` | `class RetestRecord` |
| `_finding_from_row` | function | `modules/finding_lifecycle.py:256` | `def _finding_from_row(row)` |
| `_load` | function | `modules/finding_lifecycle.py:73` | `def _load(sessions_dir)` |
| `_load_retests` | function | `modules/finding_lifecycle.py:328` | `def _load_retests(sessions_dir)` |
| `_retests_path` | function | `modules/finding_lifecycle.py:323` | `def _retests_path(sessions_dir)` |
| `_save` | function | `modules/finding_lifecycle.py:86` | `def _save(sessions_dir, data)` |
| `_save_retests` | function | `modules/finding_lifecycle.py:339` | `def _save_retests(sessions_dir, payload)` |
| `_store_path` | function | `modules/finding_lifecycle.py:68` | `def _store_path(sessions_dir)` |
| `_token_value` | function | `modules/finding_lifecycle.py:241` | `def _token_value(refs, prefix, default)` |
| `_with_token` | function | `modules/finding_lifecycle.py:249` | `def _with_token(refs, prefix, value)` |
| `add_dead_end` | function | `modules/finding_lifecycle.py:137` | `def add_dead_end(kind, value, reason, sessions_dir)` |
| `apply_confirmation` | function | `modules/finding_lifecycle.py:190` | `def apply_confirmation(nodes, sessions_dir)` |
| `classify_retest` | function | `modules/finding_lifecycle.py:420` | `def classify_retest(needle, output)` |
| `confirm` | function | `modules/finding_lifecycle.py:94` | `def confirm(finding_id, evidence, sessions_dir, by)` |
| `evidence_floor` | function | `modules/finding_lifecycle.py:52` | `def evidence_floor(items)` |
| `findings_for` | function | `modules/finding_lifecycle.py:295` | `def findings_for(db, workspace)` |
| `has_running_retest` | function | `modules/finding_lifecycle.py:346` | `def has_running_retest(finding_id, sessions_dir)` |
| `is_dead_end` | function | `modules/finding_lifecycle.py:149` | `def is_dead_end(kind, value, sessions_dir)` |
| `record` | function | `modules/finding_lifecycle.py:270` | `def record(db, workspace, host, title, severity, summary, poc)` |
| `reject` | function | `modules/finding_lifecycle.py:123` | `def reject(finding_id, reason, sessions_dir, by)` |
| `render_markdown` | function | `modules/finding_lifecycle.py:439` | `def render_markdown(db, workspace, title)` |
| `request_retest` | function | `modules/finding_lifecycle.py:354` | `def request_retest(db, finding_id, sessions_dir)` |
| `resolve` | function | `modules/finding_lifecycle.py:162` | `def resolve(node, sessions_dir)` |
| `resolve_retest` | function | `modules/finding_lifecycle.py:374` | `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` |
| `set_status` | function | `modules/finding_lifecycle.py:300` | `def set_status(db, finding_id, status)` |
| `suppressed_values` | function | `modules/finding_lifecycle.py:156` | `def suppressed_values(sessions_dir)` |
| `ForensicCleaner` | class | `modules/forensic_cleaner.py:57` | `class ForensicCleaner` |
| `ForensicCleanerConfig` | class | `modules/forensic_cleaner.py:23` | `class ForensicCleanerConfig` |
| `__init__` | method | `modules/forensic_cleaner.py:67` | `def __init__(self, config)` |
| `amcache_parse` | method | `modules/forensic_cleaner.py:259` | `def amcache_parse(self)` |
| `linux_cleanup` | method | `modules/forensic_cleaner.py:165` | `def linux_cleanup(self)` |
| `macos_cleanup` | method | `modules/forensic_cleaner.py:193` | `def macos_cleanup(self)` |
| `windows_cleanup` | method | `modules/forensic_cleaner.py:70` | `def windows_cleanup(self)` |
| `windows_prefetch_parse` | method | `modules/forensic_cleaner.py:221` | `def windows_prefetch_parse(self, prefetch_path)` |
| `GCPAttackEngine` | class | `modules/gcp_attacks.py:77` | `class GCPAttackEngine` |
| `GCPConfig` | class | `modules/gcp_attacks.py:57` | `class GCPConfig` |
| `__init__` | method | `modules/gcp_attacks.py:90` | `def __init__(self, config)` |
| `cloud_functions_backdoor` | method | `modules/gcp_attacks.py:144` | `def cloud_functions_backdoor(self)` |
| `cloudbuild_abuse` | method | `modules/gcp_attacks.py:230` | `def cloudbuild_abuse(self)` |
| `compute_engine_metadata_exfil` | method | `modules/gcp_attacks.py:173` | `def compute_engine_metadata_exfil(self)` |
| `enumerate_iam_policy` | method | `modules/gcp_attacks.py:93` | `def enumerate_iam_policy(self, resource)` |
| `gcs_enumeration` | method | `modules/gcp_attacks.py:194` | `def gcs_enumeration(self)` |
| `organization_escalation` | method | `modules/gcp_attacks.py:261` | `def organization_escalation(self)` |
| `service_account_impersonation` | method | `modules/gcp_attacks.py:119` | `def service_account_impersonation(self)` |
| `summary` | method | `modules/gcp_attacks.py:297` | `def summary(self)` |
| `extract_cmd2_tools` | function | `modules/generate_tools.py:6` | `def extract_cmd2_tools(script_path)` |
| `GoalSpec` | class | `modules/goals.py:20` | `class GoalSpec` |
| `GoalTracker` | class | `modules/goals.py:117` | `class GoalTracker` |
| `TaskConstraints` | class | `modules/goals.py:29` | `class TaskConstraints` |
| `__init__` | method | `modules/goals.py:120` | `def __init__(self, goals)` |
| `all_achieved` | method | `modules/goals.py:148` | `def all_achieved(self)` |
| `blocked` | method | `modules/goals.py:35` | `def blocked(self, command)` |
| `constraint_block_text` | function | `modules/goals.py:103` | `def constraint_block_text(constraints)` |
| `decompose_rule_based` | function | `modules/goals.py:63` | `def decompose_rule_based(objective_text, max_goals)` |
| `goal_met` | method | `modules/goals.py:140` | `def goal_met(self, opt_in)` |
| `goals` | method | `modules/goals.py:125` | `def goals(self)` |
| `load_constraints` | function | `modules/goals.py:83` | `def load_constraints(payload)` |
| `open_goals` | method | `modules/goals.py:152` | `def open_goals(self)` |
| `prove_goal` | method | `modules/goals.py:129` | `def prove_goal(self, goal_text, evidence)` |
| `_action_for` | function | `modules/golden_path.py:113` | `def _action_for(relation)` |
| `_add` | function | `modules/golden_path.py:167` | `def _add(src, dst, relation, weight, evidence, cost)` |
| `_bare` | function | `modules/golden_path.py:78` | `def _bare(node)` |
| `_cost_for_relation` | function | `modules/golden_path.py:135` | `def _cost_for_relation(relation, weight)` |
| `_diijkstra` | function | `modules/golden_path.py:244` | `def _diijkstra(adjacency, source)` |
| `_host_node` | function | `modules/golden_path.py:66` | `def _host_node(ip)` |
| `_label` | function | `modules/golden_path.py:97` | `def _label(node)` |
| `_persist` | function | `modules/golden_path.py:381` | `def _persist(result, sessions_dir)` |
| `_source_hosts` | function | `modules/golden_path.py:227` | `def _source_hosts(snapshot)` |
| `build` | function | `modules/golden_path.py:350` | `def build(world_model_path, top_k, sessions_dir)` |
| `build_edges` | function | `modules/golden_path.py:155` | `def build_edges(snapshot)` |
| `load_artifact` | function | `modules/golden_path.py:401` | `def load_artifact(sessions_dir)` |
| `priority_for` | function | `modules/golden_path.py:418` | `def priority_for(cost)` |
| `push_objectives` | function | `modules/golden_path.py:433` | `def push_objectives(paths, store_path)` |
| `resolve_paths` | function | `modules/golden_path.py:274` | `def resolve_paths(snapshot, top_k, source)` |
| `GPOAbuseEngine` | class | `modules/gpo_abuse.py:105` | `class GPOAbuseEngine` |
| `GPOAbusePlan` | class | `modules/gpo_abuse.py:83` | `class GPOAbusePlan` |
| `GPOInfo` | class | `modules/gpo_abuse.py:54` | `class GPOInfo` |
| `__init__` | method | `modules/gpo_abuse.py:118` | `def __init__(self, domain, dc_ip)` |
| `detect_risky_gpos` | method | `modules/gpo_abuse.py:406` | `def detect_risky_gpos(self)` |
| `generate_all_plans` | method | `modules/gpo_abuse.py:382` | `def generate_all_plans(self, command, username)` |
| `parse_bloodhound_gpos` | method | `modules/gpo_abuse.py:160` | `def parse_bloodhound_gpos(self, bloodhound_nodes)` |
| `parse_gpo_list` | method | `modules/gpo_abuse.py:124` | `def parse_gpo_list(self, raw_gpo_output)` |
| `plan_local_admin_addition` | method | `modules/gpo_abuse.py:266` | `def plan_local_admin_addition(self, gpo, username, group)` |
| `plan_logon_script` | method | `modules/gpo_abuse.py:238` | `def plan_logon_script(self, gpo, command)` |
| `plan_registry_preference` | method | `modules/gpo_abuse.py:322` | `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` |
| `plan_scheduled_task` | method | `modules/gpo_abuse.py:182` | `def plan_scheduled_task(self, gpo, command, task_name)` |
| `plan_service_installation` | method | `modules/gpo_abuse.py:356` | `def plan_service_installation(self, gpo, service_name, binary_path)` |
| `plan_startup_script` | method | `modules/gpo_abuse.py:208` | `def plan_startup_script(self, gpo, script_content, script_name)` |
| `plan_wmi_filter_abuse` | method | `modules/gpo_abuse.py:293` | `def plan_wmi_filter_abuse(self, gpo, wmi_query)` |
| `summary` | method | `modules/gpo_abuse.py:434` | `def summary(self)` |
| `AdvisoryLedger` | class | `modules/guardrails/advisories.py:17` | `class AdvisoryLedger` |
| `FeatureGate` | class | `modules/guardrails/advisories.py:71` | `class FeatureGate` |
| `__init__` | method | `modules/guardrails/advisories.py:20` | `def __init__(self, limit)` |
| `__init__` | method | `modules/guardrails/advisories.py:74` | `def __init__(self, features)` |
| `clear` | method | `modules/guardrails/advisories.py:54` | `def clear(self)` |
| `describe` | method | `modules/guardrails/advisories.py:61` | `def describe(self)` |
| `describe` | method | `modules/guardrails/advisories.py:125` | `def describe(self)` |
| `is_suspended` | method | `modules/guardrails/advisories.py:115` | `def is_suspended(self, feature)` |
| `notice` | method | `modules/guardrails/advisories.py:31` | `def notice(self, code, message)` |
| `resume` | method | `modules/guardrails/advisories.py:102` | `def resume(self, feature)` |
| `resume_all` | method | `modules/guardrails/advisories.py:108` | `def resume_all(self)` |
| `suspend` | method | `modules/guardrails/advisories.py:84` | `def suspend(self, feature, reason)` |
| `suspended` | method | `modules/guardrails/advisories.py:120` | `def suspended(self)` |
| `tail` | method | `modules/guardrails/advisories.py:49` | `def tail(self, limit)` |
| `tail_locked` | method | `modules/guardrails/advisories.py:66` | `def tail_locked(self, limit)` |
| `CapacityEnvelope` | class | `modules/guardrails/budget.py:25` | `class CapacityEnvelope` |
| `__init__` | method | `modules/guardrails/budget.py:28` | `def __init__(self, capacities, threshold)` |
| `_default_capacities` | method | `modules/guardrails/budget.py:42` | `def _default_capacities()` |
| `_snapshot_locked` | method | `modules/guardrails/budget.py:176` | `def _snapshot_locked(self)` |
| `_usage_ratio` | method | `modules/guardrails/budget.py:171` | `def _usage_ratio(self, tier)` |
| `account` | method | `modules/guardrails/budget.py:109` | `def account(self, task_class, units)` |
| `admit` | method | `modules/guardrails/budget.py:78` | `def admit(self, task_class, units)` |
| `capacity` | method | `modules/guardrails/budget.py:147` | `def capacity(self, task_class)` |
| `configure` | method | `modules/guardrails/budget.py:50` | `def configure(self, capacities, threshold)` |
| `describe` | method | `modules/guardrails/budget.py:166` | `def describe(self)` |
| `purge` | method | `modules/guardrails/budget.py:126` | `def purge(self, task_class)` |
| `reclaim` | method | `modules/guardrails/budget.py:136` | `def reclaim(self)` |
| `release` | method | `modules/guardrails/budget.py:118` | `def release(self, task_class, units)` |
| `saturated` | method | `modules/guardrails/budget.py:154` | `def saturated(self, task_class)` |
| `threshold` | method | `modules/guardrails/budget.py:161` | `def threshold(self)` |
| `usage` | method | `modules/guardrails/budget.py:140` | `def usage(self, task_class)` |
| `CheckpointLedger` | class | `modules/guardrails/checkpoints.py:18` | `class CheckpointLedger` |
| `__init__` | method | `modules/guardrails/checkpoints.py:21` | `def __init__(self, history)` |
| `capture` | method | `modules/guardrails/checkpoints.py:33` | `def capture(self, key, state)` |
| `describe` | method | `modules/guardrails/checkpoints.py:92` | `def describe(self)` |
| `keys` | method | `modules/guardrails/checkpoints.py:59` | `def keys(self)` |
| `restore` | method | `modules/guardrails/checkpoints.py:51` | `def restore(self, key)` |
| `warm_restart` | method | `modules/guardrails/checkpoints.py:64` | `def warm_restart(self, core_key)` |
| `GuardrailContract` | class | `modules/guardrails/contracts.py:49` | `class GuardrailContract(Protocol)` |
| `HarnessAdminPort` | class | `modules/guardrails/contracts.py:73` | `class HarnessAdminPort(Protocol)` |
| `RunTicket` | class | `modules/guardrails/contracts.py:40` | `class RunTicket` |
| `TaskClass` | class | `modules/guardrails/contracts.py:19` | `class TaskClass(IntEnum)` |
| `configure` | method | `modules/guardrails/contracts.py:76` | `def configure(self, settings)` |
| `describe` | method | `modules/guardrails/contracts.py:52` | `def describe(self)` |
| `is_known` | method | `modules/guardrails/contracts.py:31` | `def is_known(cls, value)` |
| `rearm` | method | `modules/guardrails/contracts.py:80` | `def rearm(self)` |
| `run_guarded` | method | `modules/guardrails/contracts.py:56` | `def run_guarded(self, task_class, fn)` |
| `warm_restart` | method | `modules/guardrails/contracts.py:68` | `def warm_restart(self)` |
| `GuardHarness` | class | `modules/guardrails/harness.py:25` | `class GuardHarness` |
| `__init__` | method | `modules/guardrails/harness.py:28` | `def __init__(self, threshold, capacities)` |
| `_on_failure` | method | `modules/guardrails/harness.py:174` | `def _on_failure(self, tier, ticket, key, fn, args, kwargs, exc)` |
| `configure` | method | `modules/guardrails/harness.py:48` | `def configure(self, settings)` |
| `describe` | method | `modules/guardrails/harness.py:165` | `def describe(self)` |
| `global_harness` | function | `modules/guardrails/harness.py:232` | `def global_harness()` |
| `rearm` | method | `modules/guardrails/harness.py:153` | `def rearm(self)` |
| `reset_global_harness` | function | `modules/guardrails/harness.py:241` | `def reset_global_harness()` |
| `run_guarded` | method | `modules/guardrails/harness.py:63` | `def run_guarded(self, task_class, fn)` |
| `suspend` | method | `modules/guardrails/harness.py:138` | `def suspend(self, feature, reason)` |
| `warm_restart` | method | `modules/guardrails/harness.py:124` | `def warm_restart(self, core_key)` |
| `has` | function | `modules/gui_askpass.sh:22` | `` |
| `try_kdialog` | function | `modules/gui_askpass.sh:40` | `` |
| `try_ssh_askpass` | function | `modules/gui_askpass.sh:33` | `` |
| `try_yad` | function | `modules/gui_askpass.sh:28` | `` |
| `try_zenity` | function | `modules/gui_askpass.sh:24` | `` |
| `cleanup_enabled` | function | `modules/gym_cleanup.py:21` | `def cleanup_enabled()` |
| `cleanup_gym_machines` | function | `modules/gym_cleanup.py:35` | `def cleanup_gym_machines(verbose)` |
| `_catalogue` | function | `modules/gym_matrix_runner.py:36` | `def _catalogue(catalogue)` |
| `_persist` | function | `modules/gym_matrix_runner.py:236` | `def _persist(summary_result, sessions_dir)` |
| `_stats` | function | `modules/gym_matrix_runner.py:220` | `def _stats(runs)` |
| `load_matrix` | function | `modules/gym_matrix_runner.py:252` | `def load_matrix(sessions_dir)` |
| `plan_matrix` | function | `modules/gym_matrix_runner.py:49` | `def plan_matrix(target, sessions_dir, only, top_k, catalogue)` |
| `run_matrix` | function | `modules/gym_matrix_runner.py:104` | `def run_matrix(target)` |
| `_empty_state` | function | `modules/gym_registry.py:442` | `def _empty_state()` |
| `_matches` | function | `modules/gym_registry.py:625` | `def _matches(run, selector)` |
| `_merge_legacy` | function | `modules/gym_registry.py:532` | `def _merge_legacy(state)` |
| `_next_run_id` | function | `modules/gym_registry.py:569` | `def _next_run_id(state)` |
| `_normalize_definition` | function | `modules/gym_registry.py:188` | `def _normalize_definition(data)` |
| `_read_yaml` | function | `modules/gym_registry.py:178` | `def _read_yaml(path)` |
| `_sanitize_state` | function | `modules/gym_registry.py:454` | `def _sanitize_state(raw)` |
| `_world_model` | function | `modules/gym_registry.py:447` | `def _world_model()` |
| `_write_yaml` | function | `modules/gym_registry.py:282` | `def _write_yaml(path, data)` |
| `_yaml_module` | function | `modules/gym_registry.py:85` | `def _yaml_module()` |
| `create_definition` | function | `modules/gym_registry.py:300` | `def create_definition(gym_id)` |
| `definition_path` | function | `modules/gym_registry.py:155` | `def definition_path(gym_id, directory)` |
| `delete_definition` | function | `modules/gym_registry.py:402` | `def delete_definition(gym_id, directory)` |
| `get_active_runs` | function | `modules/gym_registry.py:637` | `def get_active_runs(selector, operator)` |
| `load_definitions` | function | `modules/gym_registry.py:207` | `def load_definitions(directory)` |
| `new_run_token` | function | `modules/gym_registry.py:761` | `def new_run_token()` |
| `normalize_operator` | function | `modules/gym_registry.py:495` | `def normalize_operator(value)` |
| `pop_run` | function | `modules/gym_registry.py:724` | `def pop_run(selector)` |
| `read_state` | function | `modules/gym_registry.py:501` | `def read_state()` |
| `scan_definitions` | function | `modules/gym_registry.py:239` | `def scan_definitions(directory)` |
| `select_run` | function | `modules/gym_registry.py:663` | `def select_run(selector)` |
| `slugify` | function | `modules/gym_registry.py:92` | `def slugify(value)` |
| `start_run` | function | `modules/gym_registry.py:579` | `def start_run(challenge_id, definitions)` |
| `state_summary` | function | `modules/gym_registry.py:751` | `def state_summary()` |
| `stop_runs` | function | `modules/gym_registry.py:695` | `def stop_runs(selector)` |
| `update_definition_yaml` | function | `modules/gym_registry.py:369` | `def update_definition_yaml(gym_id, text, directory)` |
| `validate_definition` | function | `modules/gym_registry.py:110` | `def validate_definition(data, filename)` |
| `write_state` | function | `modules/gym_registry.py:520` | `def write_state(state)` |
| `chain_available` | function | `modules/gym_winbox_runner.py:130` | `def chain_available(vuln_id)` |
| `plan_matrix` | function | `modules/gym_winbox_runner.py:21` | `def plan_matrix(target, sessions_dir, only, top_k)` |
| `report` | function | `modules/gym_winbox_runner.py:118` | `def report(sessions_dir)` |
| `run_matrix` | function | `modules/gym_winbox_runner.py:51` | `def run_matrix(target)` |
| `gate` | function | `modules/harness.py:65` | `def gate(name)` |
| `harness_enabled` | function | `modules/harness.py:30` | `def harness_enabled()` |
| `CrackResult` | class | `modules/hash_cracker.py:127` | `class CrackResult` |
| `HashCracker` | class | `modules/hash_cracker.py:151` | `class HashCracker` |
| `HashIdentifier` | class | `modules/hash_cracker.py:140` | `class HashIdentifier` |
| `__init__` | method | `modules/hash_cracker.py:164` | `def __init__(self, wordlist, rules, use_hashcat, timeout)` |
| `_crack_batch_hashcat` | method | `modules/hash_cracker.py:500` | `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_batch_john` | method | `modules/hash_cracker.py:610` | `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_hashcat` | method | `modules/hash_cracker.py:454` | `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_crack_john` | method | `modules/hash_cracker.py:560` | `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_parse_hashcat_output` | method | `modules/hash_cracker.py:671` | `def _parse_hashcat_output(stdout, stderr, original)` |
| `_parse_john_show` | method | `modules/hash_cracker.py:686` | `def _parse_john_show(show_output, original)` |
| `_resolve_wordlist` | method | `modules/hash_cracker.py:178` | `def _resolve_wordlist(self)` |
| `crack_file` | method | `modules/hash_cracker.py:349` | `def crack_file(self, filepath, wordlist, hash_types)` |
| `crack_hash` | method | `modules/hash_cracker.py:295` | `def crack_hash(self, hash_value, hash_type, wordlist)` |
| `crack_secretsdump_output` | function | `modules/hash_cracker.py:695` | `def crack_secretsdump_output(filepath, wordlist, rhost)` |
| `identify` | method | `modules/hash_cracker.py:186` | `def identify(self, line)` |
| `identify_file` | method | `modules/hash_cracker.py:273` | `def identify_file(self, filepath)` |
| `import_to_db` | method | `modules/hash_cracker.py:405` | `def import_to_db(self, results, rhost, workspace_name)` |
| `_find_claude` | function | `modules/hive_invoke.py:115` | `def _find_claude()` |
| `_get_toposwarm` | function | `modules/hive_invoke.py:50` | `def _get_toposwarm()` |
| `_parse_argv` | function | `modules/hive_invoke.py:120` | `def _parse_argv(argv)` |
| `_run_interactive_mode` | function | `modules/hive_invoke.py:172` | `def _run_interactive_mode(prompt, effort, claude_bin)` |
| `_run_print_mode` | function | `modules/hive_invoke.py:150` | `def _run_print_mode(prompt, effort, claude_bin)` |
| `_run_toposwarm_mode` | function | `modules/hive_invoke.py:205` | `def _run_toposwarm_mode(prompt, effort, bridge)` |
| `main` | function | `modules/hive_invoke.py:255` | `def main(argv)` |
| `extract_ips_from_arp` | function | `modules/hostdiscover.sh:21` | `` |
| `extract_listening_ips_from_netstat` | function | `modules/hostdiscover.sh:26` | `` |
| `EventRecord` | class | `modules/hunt_verify.py:48` | `class EventRecord` |
| `Observation` | class | `modules/hunt_verify.py:73` | `class Observation` |
| `StageAssessment` | class | `modules/hunt_verify.py:85` | `class StageAssessment` |
| `StageSpec` | class | `modules/hunt_verify.py:60` | `class StageSpec` |
| `Verification` | class | `modules/hunt_verify.py:116` | `class Verification` |
| `_assess_stage` | function | `modules/hunt_verify.py:310` | `def _assess_stage(spec, observations, events, complete, warnings)` |
| `_field_present` | function | `modules/hunt_verify.py:172` | `def _field_present(event, field_name)` |
| `_scalar_present` | function | `modules/hunt_verify.py:177` | `def _scalar_present(value)` |
| `_stage_matches` | function | `modules/hunt_verify.py:188` | `def _stage_matches(spec, event)` |
| `_unique` | function | `modules/hunt_verify.py:140` | `def _unique(values)` |
| `chain_proven` | method | `modules/hunt_verify.py:124` | `def chain_proven(self)` |
| `field_present` | function | `modules/hunt_verify.py:152` | `def field_present(fields, field_name)` |
| `to_dict` | method | `modules/hunt_verify.py:99` | `def to_dict(self)` |
| `to_dict` | method | `modules/hunt_verify.py:130` | `def to_dict(self)` |
| `validate_specs` | function | `modules/hunt_verify.py:197` | `def validate_specs(specs)` |
| `verify_stages` | function | `modules/hunt_verify.py:232` | `def verify_stages(specs, observations, events, scope_covered)` |
| `CodeAnalyzer` | class | `modules/ia_code_analysis.py:28` | `class CodeAnalyzer` |
| `__init__` | method | `modules/ia_code_analysis.py:33` | `def __init__(self, mode)` |
| `analyze_code_file` | method | `modules/ia_code_analysis.py:49` | `def analyze_code_file(self, file_path)` |
| `analyze_directory` | method | `modules/ia_code_analysis.py:37` | `def analyze_directory(self, directory)` |
| `analyze_with_deepseek` | function | `modules/ia_code_analysis.py:66` | `def analyze_with_deepseek(code_content, file_path, mode)` |
| `parse_args` | function | `modules/ia_code_analysis.py:178` | `def parse_args()` |
| `save_results_to_json` | function | `modules/ia_code_analysis.py:123` | `def save_results_to_json(results, file_path)` |
| `start_analysis` | function | `modules/ia_code_analysis.py:169` | `def start_analysis(code_dir, mode)` |
| `LogFileHandler` | class | `modules/ia_logs_analysis.py:54` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/ia_logs_analysis.py:59` | `def __init__(self, mode)` |
| `analyze_log_file` | method | `modules/ia_logs_analysis.py:75` | `def analyze_log_file(self, file_path)` |
| `analyze_with_deepseek` | function | `modules/ia_logs_analysis.py:94` | `def analyze_with_deepseek(log_content, mode)` |
| `on_modified` | method | `modules/ia_logs_analysis.py:64` | `def on_modified(self, event)` |
| `parse_args` | function | `modules/ia_logs_analysis.py:168` | `def parse_args()` |
| `start_monitoring` | function | `modules/ia_logs_analysis.py:147` | `def start_monitoring(log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/ia_network_analysis.py:39` | `def analyze_with_deepseek(packet_info, mode)` |
| `packet_callback` | function | `modules/ia_network_analysis.py:91` | `def packet_callback(packet, mode)` |
| `parse_args` | function | `modules/ia_network_analysis.py:154` | `def parse_args()` |
| `start_monitoring` | function | `modules/ia_network_analysis.py:130` | `def start_monitoring(interface, timeout, mode)` |
| `imagen_a_binario` | function | `modules/img2bin.py:7` | `def imagen_a_binario(imagen_input, binario_output, block_size)` |
| `main` | function | `modules/img2bin.py:43` | `def main()` |
| `CVEMapper` | class | `modules/integrations/misp_export.py:143` | `class CVEMapper(FindingMapper)` |
| `CredentialMapper` | class | `modules/integrations/misp_export.py:123` | `class CredentialMapper(FindingMapper)` |
| `DomainMapper` | class | `modules/integrations/misp_export.py:163` | `class DomainMapper(FindingMapper)` |
| `FindingMapper` | class | `modules/integrations/misp_export.py:86` | `class FindingMapper(ABC)` |
| `HashMapper` | class | `modules/integrations/misp_export.py:183` | `class HashMapper(FindingMapper)` |
| `IPMapper` | class | `modules/integrations/misp_export.py:103` | `class IPMapper(FindingMapper)` |
| `MISPAttribute` | class | `modules/integrations/misp_export.py:59` | `class MISPAttribute` |
| `MISPEvent` | class | `modules/integrations/misp_export.py:70` | `class MISPEvent` |
| `MISPExporter` | class | `modules/integrations/misp_export.py:254` | `class MISPExporter` |
| `ServiceMapper` | class | `modules/integrations/misp_export.py:218` | `class ServiceMapper(FindingMapper)` |
| `_DictFinding` | class | `modules/integrations/misp_export.py:498` | `class _DictFinding` |
| `__init__` | method | `modules/integrations/misp_export.py:263` | `def __init__(self, mappers)` |
| `__init__` | method | `modules/integrations/misp_export.py:501` | `def __init__(self, data)` |
| `_detect_type` | method | `modules/integrations/misp_export.py:211` | `def _detect_type(value)` |
| `_dict_to_fact_records` | method | `modules/integrations/misp_export.py:457` | `def _dict_to_fact_records(data)` |
| `_dict_to_findings` | method | `modules/integrations/misp_export.py:403` | `def _dict_to_findings(data)` |
| `_is_credential` | method | `modules/integrations/misp_export.py:138` | `def _is_credential(finding)` |
| `_is_cve` | method | `modules/integrations/misp_export.py:158` | `def _is_cve(finding)` |
| `_is_domain` | method | `modules/integrations/misp_export.py:178` | `def _is_domain(finding)` |
| `_is_hash` | method | `modules/integrations/misp_export.py:206` | `def _is_hash(finding)` |
| `_is_ip` | method | `modules/integrations/misp_export.py:118` | `def _is_ip(finding)` |
| `_is_service` | method | `modules/integrations/misp_export.py:233` | `def _is_service(finding)` |
| `_load_events` | method | `modules/integrations/misp_export.py:383` | `def _load_events(self, sdir)` |
| `_load_findings` | method | `modules/integrations/misp_export.py:365` | `def _load_findings(self, sdir)` |
| `_load_policy_facts` | method | `modules/integrations/misp_export.py:372` | `def _load_policy_facts(self, sdir)` |
| `_main` | function | `modules/integrations/misp_export.py:529` | `def _main()` |
| `_map_finding` | method | `modules/integrations/misp_export.py:490` | `def _map_finding(self, finding)` |
| `export_session` | method | `modules/integrations/misp_export.py:268` | `def export_session(self, sessions_dir, target)` |
| `get_exporter` | function | `modules/integrations/misp_export.py:516` | `def get_exporter()` |
| `map` | method | `modules/integrations/misp_export.py:90` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:106` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:126` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:146` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:166` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:192` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:221` | `def map(self, finding)` |
| `push_to_misp` | method | `modules/integrations/misp_export.py:330` | `def push_to_misp(self, event, url, api_key)` |
| `save` | method | `modules/integrations/misp_export.py:322` | `def save(self, event, path)` |
| `to_json` | method | `modules/integrations/misp_export.py:299` | `def to_json(self, event)` |
| `LocalTemplateIndex` | class | `modules/integrations/nuclei_bridge.py:104` | `class LocalTemplateIndex(TemplateSelector)` |
| `NucleiBridge` | class | `modules/integrations/nuclei_bridge.py:389` | `class NucleiBridge` |
| `NucleiRunner` | class | `modules/integrations/nuclei_bridge.py:279` | `class NucleiRunner` |
| `NucleiTemplate` | class | `modules/integrations/nuclei_bridge.py:71` | `class NucleiTemplate` |
| `TemplateSelector` | class | `modules/integrations/nuclei_bridge.py:87` | `class TemplateSelector(ABC)` |
| `_F` | class | `modules/integrations/nuclei_bridge.py:483` | `class _F` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:114` | `def __init__(self, templates_dir)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:288` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:396` | `def __init__(self, selector, runner)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:484` | `def __init__(self, ftype, value)` |
| `_build_command` | method | `modules/integrations/nuclei_bridge.py:343` | `def _build_command(self, target, templates, output_dir)` |
| `_ensure_built` | method | `modules/integrations/nuclei_bridge.py:158` | `def _ensure_built(self)` |
| `_extract_context` | method | `modules/integrations/nuclei_bridge.py:370` | `def _extract_context(findings)` |
| `_extract_cve_from_tags` | method | `modules/integrations/nuclei_bridge.py:246` | `def _extract_cve_from_tags(tags)` |
| `_extract_cve_from_text` | method | `modules/integrations/nuclei_bridge.py:253` | `def _extract_cve_from_text(text)` |
| `_main` | function | `modules/integrations/nuclei_bridge.py:456` | `def _main()` |
| `_matches` | method | `modules/integrations/nuclei_bridge.py:258` | `def _matches(tmpl, service_lower, cve_upper)` |
| `_normalise_tags` | method | `modules/integrations/nuclei_bridge.py:238` | `def _normalise_tags(raw)` |
| `_parse_regex` | method | `modules/integrations/nuclei_bridge.py:201` | `def _parse_regex(self, text, path)` |
| `_parse_template` | method | `modules/integrations/nuclei_bridge.py:162` | `def _parse_template(self, path)` |
| `_parse_yaml` | method | `modules/integrations/nuclei_bridge.py:172` | `def _parse_yaml(self, text, path)` |
| `build` | method | `modules/integrations/nuclei_bridge.py:141` | `def build(self)` |
| `get_bridge` | function | `modules/integrations/nuclei_bridge.py:443` | `def get_bridge()` |
| `list_templates` | method | `modules/integrations/nuclei_bridge.py:427` | `def list_templates(self, services, cves)` |
| `run` | method | `modules/integrations/nuclei_bridge.py:293` | `def run(self, target, templates, output_dir)` |
| `run_for_findings` | method | `modules/integrations/nuclei_bridge.py:326` | `def run_for_findings(self, target, findings, output_dir, selector)` |
| `scan` | method | `modules/integrations/nuclei_bridge.py:404` | `def scan(self, target, findings, dry_run)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:91` | `def select(self, services, cves)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:121` | `def select(self, services, cves)` |
| `NucleiFinding` | class | `modules/integrations/nuclei_parser.py:71` | `class NucleiFinding` |
| `NucleiParser` | class | `modules/integrations/nuclei_parser.py:99` | `class NucleiParser` |
| `__init__` | method | `modules/integrations/nuclei_parser.py:109` | `def __init__(self, sessions_dir)` |
| `_finding_to_dict` | method | `modules/integrations/nuclei_parser.py:504` | `def _finding_to_dict(finding)` |
| `_parse_json_obj` | method | `modules/integrations/nuclei_parser.py:412` | `def _parse_json_obj(self, obj)` |
| `_parse_line` | method | `modules/integrations/nuclei_parser.py:393` | `def _parse_line(self, line)` |
| `_recommend_for_finding` | method | `modules/integrations/nuclei_parser.py:468` | `def _recommend_for_finding(self, finding, rhost)` |
| `_summarize` | method | `modules/integrations/nuclei_parser.py:517` | `def _summarize(findings)` |
| `enrich_world_model` | method | `modules/integrations/nuclei_parser.py:262` | `def enrich_world_model(self, findings, rhost)` |
| `exploit_probability` | method | `modules/integrations/nuclei_parser.py:95` | `def exploit_probability(self)` |
| `generate_recommendations` | method | `modules/integrations/nuclei_parser.py:300` | `def generate_recommendations(self, findings, rhost)` |
| `import_to_db` | method | `modules/integrations/nuclei_parser.py:196` | `def import_to_db(self, findings, rhost, workspace_name)` |
| `mitre_tactic` | method | `modules/integrations/nuclei_parser.py:87` | `def mitre_tactic(self)` |
| `parse_file` | method | `modules/integrations/nuclei_parser.py:177` | `def parse_file(self, filepath)` |
| `parse_json` | method | `modules/integrations/nuclei_parser.py:134` | `def parse_json(self, json_text)` |
| `parse_text` | method | `modules/integrations/nuclei_parser.py:115` | `def parse_text(self, text)` |
| `scan_and_import` | method | `modules/integrations/nuclei_parser.py:328` | `def scan_and_import(self, target, templates, services, cves, workspace_name)` |
| `ExploitDBAPI` | class | `modules/integrations/searchsploit.py:193` | `class ExploitDBAPI(ExploitSource)` |
| `ExploitEntry` | class | `modules/integrations/searchsploit.py:60` | `class ExploitEntry` |
| `ExploitSource` | class | `modules/integrations/searchsploit.py:76` | `class ExploitSource(ABC)` |
| `SearchsploitCLI` | class | `modules/integrations/searchsploit.py:93` | `class SearchsploitCLI(ExploitSource)` |
| `SearchsploitClient` | class | `modules/integrations/searchsploit.py:271` | `class SearchsploitClient` |
| `__init__` | method | `modules/integrations/searchsploit.py:102` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:201` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:278` | `def __init__(self, primary, fallback)` |
| `_extract_cve` | method | `modules/integrations/searchsploit.py:183` | `def _extract_cve(text)` |
| `_main` | function | `modules/integrations/searchsploit.py:356` | `def _main()` |
| `_parse` | method | `modules/integrations/searchsploit.py:133` | `def _parse(self, raw)` |
| `_query` | method | `modules/integrations/searchsploit.py:218` | `def _query(self, cve_id)` |
| `_rate_limit` | method | `modules/integrations/searchsploit.py:258` | `def _rate_limit()` |
| `_row_to_entry` | method | `modules/integrations/searchsploit.py:162` | `def _row_to_entry(self, row)` |
| `_run` | method | `modules/integrations/searchsploit.py:118` | `def _run(self, query)` |
| `enrich_findings` | method | `modules/integrations/searchsploit.py:300` | `def enrich_findings(self, findings)` |
| `get_client` | function | `modules/integrations/searchsploit.py:333` | `def get_client()` |
| `search_cve` | method | `modules/integrations/searchsploit.py:80` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:109` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:207` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:286` | `def search_cve(self, cve_id)` |
| `search_cve` | function | `modules/integrations/searchsploit.py:341` | `def search_cve(cve_id)` |
| `search_service` | method | `modules/integrations/searchsploit.py:84` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:112` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:210` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:293` | `def search_service(self, name, version)` |
| `search_service` | function | `modules/integrations/searchsploit.py:346` | `def search_service(name, version)` |
| `_enrich_readmenator_fields` | function | `modules/intel_fusion.py:593` | `def _enrich_readmenator_fields(nodes, edges)` |
| `_extract_cve_id` | function | `modules/intel_fusion.py:133` | `def _extract_cve_id(vuln)` |
| `_family_color` | function | `modules/intel_fusion.py:181` | `def _family_color(name)` |
| `_fibonacci_sphere` | function | `modules/intel_fusion.py:821` | `def _fibonacci_sphere(count)` |
| `_file_pagerank` | function | `modules/intel_fusion.py:230` | `def _file_pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_ghost_lines` | function | `modules/intel_fusion.py:1279` | `def _ghost_lines(sessions_dir, host_value)` |
| `_host_mentions` | function | `modules/intel_fusion.py:225` | `def _host_mentions(text)` |
| `_load_json` | function | `modules/intel_fusion.py:198` | `def _load_json(path, default)` |
| `_node_doc` | function | `modules/intel_fusion.py:555` | `def _node_doc(node)` |
| `_read_lines` | function | `modules/intel_fusion.py:208` | `def _read_lines(path, limit)` |
| `_recency_lines` | function | `modules/intel_fusion.py:1261` | `def _recency_lines(sessions_dir, host_value)` |
| `_score_lines` | function | `modules/intel_fusion.py:1086` | `def _score_lines(host_value, detail)` |
| `_service_cve_matches` | function | `modules/intel_fusion.py:83` | `def _service_cve_matches(service_name, version_text, svc)` |
| `_split_caps` | function | `modules/intel_fusion.py:837` | `def _split_caps(labels, sizes, points, lattice, out)` |
| `_svg_attr` | function | `modules/intel_fusion.py:1131` | `def _svg_attr(value)` |
| `_svg_host_of` | function | `modules/intel_fusion.py:1182` | `def _svg_host_of(node)` |
| `_svg_place` | function | `modules/intel_fusion.py:1165` | `def _svg_place(ids)` |
| `_svg_rank` | function | `modules/intel_fusion.py:1136` | `def _svg_rank(node)` |
| `_svg_text` | function | `modules/intel_fusion.py:1124` | `def _svg_text(value)` |
| `_symbol_list` | function | `modules/intel_fusion.py:578` | `def _symbol_list(node)` |
| `_unit` | function | `modules/intel_fusion.py:866` | `def _unit(vec)` |
| `add_edge` | function | `modules/intel_fusion.py:284` | `def add_edge(src, dst, kind, evidence, weight)` |
| `add_node` | function | `modules/intel_fusion.py:266` | `def add_node(kind, value, label)` |
| `assign_layout` | function | `modules/intel_fusion.py:1021` | `def assign_layout(graph, mode)` |
| `build_analytics` | function | `modules/intel_fusion.py:787` | `def build_analytics(graph, summary)` |
| `build_bundle_payload` | function | `modules/intel_fusion.py:874` | `def build_bundle_payload(graph)` |
| `build_intel_graph` | function | `modules/intel_fusion.py:260` | `def build_intel_graph(sessions_dir, est_cap)` |
| `bundle_settings` | function | `modules/intel_fusion.py:990` | `def bundle_settings(graph)` |
| `group_colors` | function | `modules/intel_fusion.py:714` | `def group_colors(graph)` |
| `node_id` | function | `modules/intel_fusion.py:192` | `def node_id(kind, value)` |
| `page_settings` | function | `modules/intel_fusion.py:730` | `def page_settings(graph)` |
| `relations_svg` | function | `modules/intel_fusion.py:1187` | `def relations_svg(graph, cap_nodes)` |
| `svg_selection` | function | `modules/intel_fusion.py:1147` | `def svg_selection(graph, cap_nodes)` |
| `tag_source` | function | `modules/intel_fusion.py:300` | `def tag_source(nid, source)` |
| `write_summary` | function | `modules/intel_fusion.py:1296` | `def write_summary(graph, sessions_dir)` |
| `CollectedFact` | class | `modules/intelligence_engine.py:79` | `class CollectedFact` |
| `CounterIntelFinding` | class | `modules/intelligence_engine.py:109` | `class CounterIntelFinding` |
| `IntelligenceAssessment` | class | `modules/intelligence_engine.py:94` | `class IntelligenceAssessment` |
| `IntelligenceConfig` | class | `modules/intelligence_engine.py:58` | `class IntelligenceConfig` |
| `IntelligenceEngine` | class | `modules/intelligence_engine.py:120` | `class IntelligenceEngine` |
| `__init__` | method | `modules/intelligence_engine.py:143` | `def __init__(self, config)` |
| `_collect_from_scan_xml` | method | `modules/intelligence_engine.py:237` | `def _collect_from_scan_xml(self, xml_path, target)` |
| `_correlate_creds_to_hosts` | method | `modules/intelligence_engine.py:736` | `def _correlate_creds_to_hosts(self)` |
| `_correlate_domains_to_infrastructure` | method | `modules/intelligence_engine.py:759` | `def _correlate_domains_to_infrastructure(self)` |
| `_correlate_services_to_vulns` | method | `modules/intelligence_engine.py:604` | `def _correlate_services_to_vulns(self)` |
| `_detect_killchain_gaps` | method | `modules/intelligence_engine.py:815` | `def _detect_killchain_gaps(self)` |
| `_is_placeholder` | method | `modules/intelligence_engine.py:1120` | `def _is_placeholder(value)` |
| `_legacy_match_rows` | method | `modules/intelligence_engine.py:679` | `def _legacy_match_rows(self, fact)` |
| `_map_category_to_mitre` | method | `modules/intelligence_engine.py:871` | `def _map_category_to_mitre(category)` |
| `_match_known_vulns` | method | `modules/intelligence_engine.py:708` | `def _match_known_vulns(fact)` |
| `_match_vulns_versioned` | method | `modules/intelligence_engine.py:649` | `def _match_vulns_versioned(self, fact)` |
| `_newest_scan_xml_with_versions` | method | `modules/intelligence_engine.py:154` | `def _newest_scan_xml_with_versions(self, target)` |
| `_rank_targets` | method | `modules/intelligence_engine.py:775` | `def _rank_targets(self)` |
| `_xml_has_versions` | method | `modules/intelligence_engine.py:193` | `def _xml_has_versions(self, xml_path)` |
| `_xml_scan_weight` | method | `modules/intelligence_engine.py:177` | `def _xml_scan_weight(self, xml_path)` |
| `analyze` | method | `modules/intelligence_engine.py:587` | `def analyze(self)` |
| `collect_from_estorides` | method | `modules/intelligence_engine.py:363` | `def collect_from_estorides(self, target)` |
| `collect_from_factstore` | method | `modules/intelligence_engine.py:486` | `def collect_from_factstore(self)` |
| `collect_from_nuclei` | method | `modules/intelligence_engine.py:405` | `def collect_from_nuclei(self, target)` |
| `collect_from_scan` | method | `modules/intelligence_engine.py:197` | `def collect_from_scan(self, target)` |
| `collect_from_tool` | method | `modules/intelligence_engine.py:326` | `def collect_from_tool(self, output, tool, host)` |
| `collect_from_yara` | method | `modules/intelligence_engine.py:447` | `def collect_from_yara(self, target_path)` |
| `disseminate` | method | `modules/intelligence_engine.py:936` | `def disseminate(self)` |
| `get_intel_report` | method | `modules/intelligence_engine.py:1069` | `def get_intel_report(self)` |
| `get_intelligence_engine` | function | `modules/intelligence_engine.py:1126` | `def get_intelligence_engine(config)` |
| `produce_counter_intelligence` | method | `modules/intelligence_engine.py:886` | `def produce_counter_intelligence(self)` |
| `produce_intelligence` | method | `modules/intelligence_engine.py:856` | `def produce_intelligence(self)` |
| `run_full_cycle` | method | `modules/intelligence_engine.py:1040` | `def run_full_cycle(self, target)` |
| `Guard` | class | `modules/intercept.py:255` | `class Guard` |
| `InterceptAction` | class | `modules/intercept.py:21` | `class InterceptAction(str, Enum)` |
| `InterceptConfig` | class | `modules/intercept.py:33` | `class InterceptConfig` |
| `InterceptRule` | class | `modules/intercept.py:50` | `class InterceptRule` |
| `InterceptVerdict` | class | `modules/intercept.py:92` | `class InterceptVerdict` |
| `Interceptor` | class | `modules/intercept.py:154` | `class Interceptor` |
| `PendingApproval` | class | `modules/intercept.py:77` | `class PendingApproval` |
| `__init__` | method | `modules/intercept.py:157` | `def __init__(self, rules, ask_timeout_sec, timeout_action)` |
| `__init__` | method | `modules/intercept.py:258` | `def __init__(self, interceptor)` |
| `__post_init__` | method | `modules/intercept.py:61` | `def __post_init__(self)` |
| `add_rule` | method | `modules/intercept.py:177` | `def add_rule(self, rule)` |
| `approval_status` | method | `modules/intercept.py:249` | `def approval_status(self, approval_id)` |
| `attribution` | method | `modules/intercept.py:301` | `def attribution(self)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
