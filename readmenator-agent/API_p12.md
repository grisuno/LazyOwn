# API (page 12 of 24)
Previous: [API_p11.md](API_p11.md)

## modules/exploit_recommender.py
Depends on: `lazygui/version.py`, `modules/world_model.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/pwn.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`
- `parse_version` (function) `modules/exploit_recommender.py:25` `def parse_version(v)`
- `ExploitRecommender.__init__` (method) `modules/exploit_recommender.py:120` `def __init__(self, world_model)`
- `ExploitRecommender.set_world_model` (method) `modules/exploit_recommender.py:129` `def set_world_model(self, world_model)`
- `ExploitRecommender.set_nvd_api_key` (method) `modules/exploit_recommender.py:132` `def set_nvd_api_key(self, key)`
- `ExploitRecommender.match_services` (method) `modules/exploit_recommender.py:244` `def match_services(self, hosts)` -- Match discovered services against known CVEs with confidence scoring.
- `ExploitRecommender.recommend` (method) `modules/exploit_recommender.py:337` `def recommend(self, hosts, top_n)` -- Return top-N recommended exploits as structured dicts for MCP/CLI.
- `ExploitRecommender.persist_recommendations` (method) `modules/exploit_recommender.py:370` `def persist_recommendations(self, matches)` -- Save recommendations to sessions/ for audit and replay.
- `ExploitRecommender.format_for_llm` (method) `modules/exploit_recommender.py:390` `def format_for_llm(self, matches, max_items)` -- Format recommendations as compact text for LLM context injection.

## modules/exploitgym_gym.py
Depends on: `modules/redteam_gym.py`
Imported by: `cli/commands/exploitgym.py`, `skills/lazyown_mcp.py`, `tests/test_exploitgym_gym.py`
- `check_readiness` (function) `modules/exploitgym_gym.py:112` `def check_readiness(params)` -- Report whether the ExploitGym harness can run.
- `list_tasks` (function) `modules/exploitgym_gym.py:178` `def list_tasks(params, domain, limit)` -- List available ExploitGym tasks, optionally filtered by domain.
- `setup_harness` (function) `modules/exploitgym_gym.py:249` `def setup_harness(params, steps)` -- Automate ExploitGym installation (clone, deps, data, firewall, images).
- `pull_task` (function) `modules/exploitgym_gym.py:344` `def pull_task(task_id, params, timeout)` -- Pull the Docker image required by a task.
- `run_task` (function) `modules/exploitgym_gym.py:423` `def run_task(task_id, params, model, mitigations, timeout)` -- Run the agent against an ExploitGym task and capture the outcome.
- `verify_flag` (function) `modules/exploitgym_gym.py:548` `def verify_flag(task_id, params)` -- Verify whether a task flag was captured from a previous run.
- `score_task` (function) `modules/exploitgym_gym.py:565` `def score_task(task_id, success, techniques, params)` -- Award Red Team Gym ELO and leaderboard points for a task outcome.

## modules/factsio.py
Depends on: `core/logging.py`
Imported by: `modules/compliance.py`, `modules/intelligence_engine.py`, `modules/world_model.py`, `tests/test_single_source_of_truth.py`
- `load_policy_facts` (function) `modules/factsio.py:39` `def load_policy_facts(path)` -- Load ``policy_facts.json`` into canonical host-keyed form.
- `canonical_policy_facts` (function) `modules/factsio.py:61` `def canonical_policy_facts(data)` -- Project any legacy or canonical facts document to host-keyed form.
- `iter_host_records` (function) `modules/factsio.py:81` `def iter_host_records(host_keyed)` -- Yield ``(ip, record)`` pairs from canonical host-keyed facts.
- `iter_flat_facts` (function) `modules/factsio.py:93` `def iter_flat_facts(host_keyed)` -- Yield one flat record per fact kind found in the host map.

## modules/fast_run_service.sh
- `log_timestamp` (function) `modules/fast_run_service.sh:69` -- # # Logging primitives.
- `log_info` (function) `modules/fast_run_service.sh:73`
- `log_warn` (function) `modules/fast_run_service.sh:77`
- `log_error` (function) `modules/fast_run_service.sh:81`
- `require_root` (function) `modules/fast_run_service.sh:89` -- # # Pre-flight checks.
- `require_deps` (function) `modules/fast_run_service.sh:97`
- `require_paths` (function) `modules/fast_run_service.sh:113`
- `prepare_runtime_dirs` (function) `modules/fast_run_service.sh:126`
- `load_config` (function) `modules/fast_run_service.sh:139`
- `config_truthy` (function) `modules/fast_run_service.sh:155`
- `pid_file_for` (function) `modules/fast_run_service.sh:166` -- # # PID-file primitives.
- `log_file_for` (function) `modules/fast_run_service.sh:171`
- `read_pid_value` (function) `modules/fast_run_service.sh:176`
- `is_pid_alive` (function) `modules/fast_run_service.sh:189`
- `is_service_running` (function) `modules/fast_run_service.sh:194`
- `write_pid_file` (function) `modules/fast_run_service.sh:201`
- `ensure_log_file` (function) `modules/fast_run_service.sh:211`
- `spawn_as_target_user` (function) `modules/fast_run_service.sh:228` -- # # Process spawn primitives.
- `spawn_as_root` (function) `modules/fast_run_service.sh:247`
- `terminate_pid_tree` (function) `modules/fast_run_service.sh:264`
- `stop_named_service` (function) `modules/fast_run_service.sh:292`
- `chown_project_tree` (function) `modules/fast_run_service.sh:310` -- # # Ownership maintenance.
- `start_chown_watcher` (function) `modules/fast_run_service.sh:315`
- `start_lazyc2_service` (function) `modules/fast_run_service.sh:342` -- # # Concrete service launchers.
- `start_www_service` (function) `modules/fast_run_service.sh:356`
- `start_vpn_service` (function) `modules/fast_run_service.sh:363`
- `start_discord_service` (function) `modules/fast_run_service.sh:380`
- `start_telegram_service` (function) `modules/fast_run_service.sh:390`
- `start_cloudflare_service` (function) `modules/fast_run_service.sh:400`
- `start_ollama_service` (function) `modules/fast_run_service.sh:410`
- `managed_services_in_order` (function) `modules/fast_run_service.sh:429` -- # # Service registry.
- `cmd_start` (function) `modules/fast_run_service.sh:445` -- # # Lifecycle commands.
- `cmd_stop` (function) `modules/fast_run_service.sh:465`
- `cmd_restart` (function) `modules/fast_run_service.sh:480`
- `cmd_status` (function) `modules/fast_run_service.sh:486`
- `cmd_logs` (function) `modules/fast_run_service.sh:505`
- `cmd_chown_now` (function) `modules/fast_run_service.sh:521`
- `usage` (function) `modules/fast_run_service.sh:528`
- `main` (function) `modules/fast_run_service.sh:557` -- # # Entry point. require_root re-executes under sudo and never returns there; # the case-arm dispatch is reached...

## modules/finding_lifecycle.py
Depends on: `modules/osint_enrich.py`
Imported by: `cli/commands/database.py`, `modules/attack_surface3d.py`, `modules/intel_fusion.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`, `tests/test_finding_lifecycle.py`
- `confirm` (function) `modules/finding_lifecycle.py:61` `def confirm(finding_id, evidence, sessions_dir, by)` -- Mark a finding confirmed with linked evidence (CAIRN seed-add).
- `reject` (function) `modules/finding_lifecycle.py:90` `def reject(finding_id, reason, sessions_dir, by)` -- Mark a finding rejected (disproven lead, CAIRN dead-end discipline).
- `add_dead_end` (function) `modules/finding_lifecycle.py:104` `def add_dead_end(kind, value, reason, sessions_dir)` -- Suppress a value campaign-wide with a labeled reason (dead_end_hashes).
- `is_dead_end` (function) `modules/finding_lifecycle.py:116` `def is_dead_end(kind, value, sessions_dir)` -- Return True when a kind/value pair sits on the suppression list.
- `suppressed_values` (function) `modules/finding_lifecycle.py:123` `def suppressed_values(sessions_dir)` -- Return every suppressed value for text-level filtering by the loop.
- `resolve` (function) `modules/finding_lifecycle.py:129` `def resolve(node, sessions_dir)` -- Resolve a finding node's confirmation state.
- `apply_confirmation` (function) `modules/finding_lifecycle.py:154` `def apply_confirmation(nodes, sessions_dir)` -- Stamp ``confirmation``/``status`` on every finding node in place.
- `record` (function) `modules/finding_lifecycle.py:234` `def record(db, workspace, host, title, severity, summary, poc)` -- Record a campaign finding on the DB for one host.
- `findings_for` (function) `modules/finding_lifecycle.py:259` `def findings_for(db, workspace)` -- List campaign findings with parsed status markers.
- `set_status` (function) `modules/finding_lifecycle.py:264` `def set_status(db, finding_id, status)` -- Set the lifecycle status marker on one finding.
- `has_running_retest` (function) `modules/finding_lifecycle.py:310` `def has_running_retest(finding_id, sessions_dir)` -- Return True while a retest for the finding is still running.
- `request_retest` (function) `modules/finding_lifecycle.py:318` `def request_retest(db, finding_id, sessions_dir)` -- Queue a retest; an already-running one is returned unchanged.
- `resolve_retest` (function) `modules/finding_lifecycle.py:338` `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` -- Close a retest, bump the evidence version and apply the verdict.
- `classify_retest` (function) `modules/finding_lifecycle.py:384` `def classify_retest(needle, output)` -- Map retest output onto reproducible / fixed / inconclusive.
- `render_markdown` (function) `modules/finding_lifecycle.py:403` `def render_markdown(db, workspace, title)` -- Render campaign findings as a markdown report.

## modules/forensic_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `ForensicCleaner.__init__` (method) `modules/forensic_cleaner.py:67` `def __init__(self, config)`
- `ForensicCleaner.windows_cleanup` (method) `modules/forensic_cleaner.py:70` `def windows_cleanup(self)` -- Generate Windows forensic artifact cleanup commands.
- `ForensicCleaner.linux_cleanup` (method) `modules/forensic_cleaner.py:165` `def linux_cleanup(self)` -- Generate Linux forensic artifact cleanup commands.
- `ForensicCleaner.macos_cleanup` (method) `modules/forensic_cleaner.py:193` `def macos_cleanup(self)` -- Generate macOS forensic artifact cleanup commands.
- `ForensicCleaner.windows_prefetch_parse` (method) `modules/forensic_cleaner.py:221` `def windows_prefetch_parse(self, prefetch_path)` -- Parse Prefetch files to identify what the attacker should clean.
- `ForensicCleaner.amcache_parse` (method) `modules/forensic_cleaner.py:259` `def amcache_parse(self)` -- Parse Amcache registry entries for evidence of execution.

## modules/gcp_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `GCPAttackEngine.__init__` (method) `modules/gcp_attacks.py:90` `def __init__(self, config)`
- `GCPAttackEngine.enumerate_iam_policy` (method) `modules/gcp_attacks.py:93` `def enumerate_iam_policy(self, resource)` -- Enumerate IAM policies for projects, folders, or organizations.
- `GCPAttackEngine.service_account_impersonation` (method) `modules/gcp_attacks.py:119` `def service_account_impersonation(self)` -- Exploit service account impersonation for privilege escalation.
- `GCPAttackEngine.cloud_functions_backdoor` (method) `modules/gcp_attacks.py:144` `def cloud_functions_backdoor(self)` -- Backdoor Cloud Functions for privilege escalation.
- `GCPAttackEngine.compute_engine_metadata_exfil` (method) `modules/gcp_attacks.py:173` `def compute_engine_metadata_exfil(self)` -- Exfiltrate GCE instance metadata and service account tokens.
- `GCPAttackEngine.gcs_enumeration` (method) `modules/gcp_attacks.py:194` `def gcs_enumeration(self)` -- Enumerate Cloud Storage buckets for sensitive data.
- `GCPAttackEngine.cloudbuild_abuse` (method) `modules/gcp_attacks.py:230` `def cloudbuild_abuse(self)` -- Abuse Cloud Build for privilege escalation.
- `GCPAttackEngine.organization_escalation` (method) `modules/gcp_attacks.py:261` `def organization_escalation(self)` -- Escalate from project-level to organization-level access.
- `GCPAttackEngine.summary` (method) `modules/gcp_attacks.py:297` `def summary(self)`

## modules/generate_tools.py
- `extract_cmd2_tools` (function) `modules/generate_tools.py:6` `def extract_cmd2_tools(script_path)`

## modules/goals.py
Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`
- `TaskConstraints.blocked` (method) `modules/goals.py:35` `def blocked(self, command)` -- Return the blocking constraint or empty string.
- `decompose_rule_based` (function) `modules/goals.py:63` `def decompose_rule_based(objective_text, max_goals)` -- Split objective text into goal specs without an LLM (deterministic).
- `load_constraints` (function) `modules/goals.py:83` `def load_constraints(payload)` -- Build constraints from payload config (deny wins, LAZY parity).
- `constraint_block_text` (function) `modules/goals.py:103` `def constraint_block_text(constraints)` -- Render the constraint block injected at max priority (LAZY parity).
- `GoalTracker.__init__` (method) `modules/goals.py:120` `def __init__(self, goals)` -- Bind to an initial goal list.
- `GoalTracker.goals` (method) `modules/goals.py:125` `def goals(self)` -- Return a copy of tracked goals.
- `GoalTracker.prove_goal` (method) `modules/goals.py:129` `def prove_goal(self, goal_text, evidence)` -- Mark one goal achieved from evidence; return True when found.
- `GoalTracker.goal_met` (method) `modules/goals.py:140` `def goal_met(self, opt_in)` -- End the whole task; requires explicit opt-in (default unbound).
- `GoalTracker.all_achieved` (method) `modules/goals.py:148` `def all_achieved(self)` -- Return True when every goal is achieved.
- `GoalTracker.open_goals` (method) `modules/goals.py:152` `def open_goals(self)` -- Return goals still open.

## modules/golden_path.py
Depends on: `core/logging.py`, `modules/world_model.py`, `skills/lazyown_objective.py`
- `build_edges` (function) `modules/golden_path.py:155` `def build_edges(snapshot)` -- Build the weighted adjacency map from a world-model snapshot.
- `resolve_paths` (function) `modules/golden_path.py:274` `def resolve_paths(snapshot, top_k, source)` -- Solve shortest attack paths toward every reachable host.
- `build` (function) `modules/golden_path.py:350` `def build(world_model_path, top_k, sessions_dir)` -- Load the live world model, solve paths, and persist the result.
- `load_artifact` (function) `modules/golden_path.py:401` `def load_artifact(sessions_dir)` -- Read the persisted attack-path artifact.
- `priority_for` (function) `modules/golden_path.py:418` `def priority_for(cost)` -- Map a path cost to an objective priority band.
- `push_objectives` (function) `modules/golden_path.py:433` `def push_objectives(paths, store_path)` -- Inject one objective per solved path into the objective store.

## modules/gpo_abuse.py
Imported by: `cli/commands/active_directory.py`
- `GPOAbuseEngine.__init__` (method) `modules/gpo_abuse.py:118` `def __init__(self, domain, dc_ip)`
- `GPOAbuseEngine.parse_gpo_list` (method) `modules/gpo_abuse.py:124` `def parse_gpo_list(self, raw_gpo_output)` -- Parse Get-GPO or ldapsearch output for GPO information.
- `GPOAbuseEngine.parse_bloodhound_gpos` (method) `modules/gpo_abuse.py:160` `def parse_bloodhound_gpos(self, bloodhound_nodes)` -- Parse BloodHound GPO nodes for abusable policies.
- `GPOAbuseEngine.plan_scheduled_task` (method) `modules/gpo_abuse.py:182` `def plan_scheduled_task(self, gpo, command, task_name)` -- Plan a GPO-backed scheduled task for immediate code execution.
- `GPOAbuseEngine.plan_startup_script` (method) `modules/gpo_abuse.py:208` `def plan_startup_script(self, gpo, script_content, script_name)` -- Plan a GPO startup script for persistence via SYSVOL.
- `GPOAbuseEngine.plan_logon_script` (method) `modules/gpo_abuse.py:238` `def plan_logon_script(self, gpo, command)` -- Plan a GPO user logon script for user-triggered code execution.
- `GPOAbuseEngine.plan_local_admin_addition` (method) `modules/gpo_abuse.py:266` `def plan_local_admin_addition(self, gpo, username, group)` -- Plan adding a user to the local Administrators group via GPO preferences.
- `GPOAbuseEngine.plan_wmi_filter_abuse` (method) `modules/gpo_abuse.py:293` `def plan_wmi_filter_abuse(self, gpo, wmi_query)` -- Plan WMI filter abuse for targeted GPO scope control.
- `GPOAbuseEngine.plan_registry_preference` (method) `modules/gpo_abuse.py:322` `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` -- Plan a registry modification via GPO preferences.
- `GPOAbuseEngine.plan_service_installation` (method) `modules/gpo_abuse.py:356` `def plan_service_installation(self, gpo, service_name, binary_path)` -- Plan a service installation via GPO for SYSTEM-level persistence.
- `GPOAbuseEngine.generate_all_plans` (method) `modules/gpo_abuse.py:382` `def generate_all_plans(self, command, username)` -- Generate all abuse plans for the discovered GPOs.
- `GPOAbuseEngine.detect_risky_gpos` (method) `modules/gpo_abuse.py:406` `def detect_risky_gpos(self)` -- Identify GPOs with risky configurations for post-compromise cleanup.
- `GPOAbuseEngine.summary` (method) `modules/gpo_abuse.py:434` `def summary(self)` -- Return a summary of GPO abuse capabilities.

## modules/guardrails/advisories.py
Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`
- `AdvisoryLedger.__init__` (method) `modules/guardrails/advisories.py:20` `def __init__(self, limit)` -- Create an empty ledger.
- `AdvisoryLedger.notice` (method) `modules/guardrails/advisories.py:31` `def notice(self, code, message)` -- Record one advisory without blocking the caller.
- `AdvisoryLedger.tail` (method) `modules/guardrails/advisories.py:49` `def tail(self, limit)` -- Return the newest notices up to the limit.
- `AdvisoryLedger.clear` (method) `modules/guardrails/advisories.py:54` `def clear(self)` -- Drop every notice, returning the discarded count.
- `AdvisoryLedger.describe` (method) `modules/guardrails/advisories.py:61` `def describe(self)` -- Return the ledger summary for the admin console.
- `AdvisoryLedger.tail_locked` (method) `modules/guardrails/advisories.py:66` `def tail_locked(self, limit)` -- Tail helper used by describe; caller holds the lock.
- `FeatureGate.__init__` (method) `modules/guardrails/advisories.py:74` `def __init__(self, features)` -- Create a gate limited to the known optional features.
- `FeatureGate.suspend` (method) `modules/guardrails/advisories.py:84` `def suspend(self, feature, reason)` -- Suspend one optional feature.
- `FeatureGate.resume` (method) `modules/guardrails/advisories.py:102` `def resume(self, feature)` -- Resume one suspended feature, returning True when it changed.
- `FeatureGate.resume_all` (method) `modules/guardrails/advisories.py:108` `def resume_all(self)` -- Resume every suspended feature, returning the resumed count.
- `FeatureGate.is_suspended` (method) `modules/guardrails/advisories.py:115` `def is_suspended(self, feature)` -- Return True when the feature is currently suspended.
- `FeatureGate.suspended` (method) `modules/guardrails/advisories.py:120` `def suspended(self)` -- Return the suspended feature map (feature -> reason).
- `FeatureGate.describe` (method) `modules/guardrails/advisories.py:125` `def describe(self)` -- Return the gate state for the admin console.

## modules/guardrails/budget.py
Depends on: `modules/guardrails/contracts.py`
Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`
- `CapacityEnvelope.__init__` (method) `modules/guardrails/budget.py:28` `def __init__(self, capacities, threshold)` -- Seed capacities and the saturation threshold.
- `CapacityEnvelope.configure` (method) `modules/guardrails/budget.py:50` `def configure(self, capacities, threshold)` -- Apply capacity and threshold settings, clamping invalid values.
- `CapacityEnvelope.admit` (method) `modules/guardrails/budget.py:78` `def admit(self, task_class, units)` -- Reserve units for one tier honouring the priority contract.
- `CapacityEnvelope.account` (method) `modules/guardrails/budget.py:109` `def account(self, task_class, units)` -- Record consumed units for one tier (idempotent on refusal).
- `CapacityEnvelope.release` (method) `modules/guardrails/budget.py:118` `def release(self, task_class, units)` -- Return units to a tier ledger once an execution finishes.
- `CapacityEnvelope.purge` (method) `modules/guardrails/budget.py:126` `def purge(self, task_class)` -- Zero one tier ledger, returning the freed unit count.
- `CapacityEnvelope.reclaim` (method) `modules/guardrails/budget.py:136` `def reclaim(self)` -- Purge SUPPORT allocations, returning the freed unit count.
- `CapacityEnvelope.usage` (method) `modules/guardrails/budget.py:140` `def usage(self, task_class)` -- Return current consumed units for one tier.
- `CapacityEnvelope.capacity` (method) `modules/guardrails/budget.py:147` `def capacity(self, task_class)` -- Return configured capacity for one tier.
- `CapacityEnvelope.saturated` (method) `modules/guardrails/budget.py:154` `def saturated(self, task_class)` -- Return True when the tier usage ratio reaches the threshold.
- `CapacityEnvelope.threshold` (method) `modules/guardrails/budget.py:161` `def threshold(self)` -- Return the configured saturation threshold.
- `CapacityEnvelope.describe` (method) `modules/guardrails/budget.py:166` `def describe(self)` -- Return a per-tier usage snapshot for the admin console.

## modules/guardrails/checkpoints.py
Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`
- `CheckpointLedger.__init__` (method) `modules/guardrails/checkpoints.py:21` `def __init__(self, history)` -- Create an empty ledger.
- `CheckpointLedger.capture` (method) `modules/guardrails/checkpoints.py:33` `def capture(self, key, state)` -- Store one immutable snapshot for a key.
- `CheckpointLedger.restore` (method) `modules/guardrails/checkpoints.py:51` `def restore(self, key)` -- Return the latest snapshot for a key, or None when missing.
- `CheckpointLedger.keys` (method) `modules/guardrails/checkpoints.py:59` `def keys(self)` -- Return the tracked checkpoint keys.
- `CheckpointLedger.warm_restart` (method) `modules/guardrails/checkpoints.py:64` `def warm_restart(self, core_key)` -- Purge non-core runtime contexts and restore the core snapshot.
- `CheckpointLedger.describe` (method) `modules/guardrails/checkpoints.py:92` `def describe(self)` -- Return the ledger state for the admin console.

## modules/guardrails/contracts.py
Depends on: `cli/commands/enum.py`
Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/budget.py`, `modules/guardrails/harness.py`
- `TaskClass.is_known` (method) `modules/guardrails/contracts.py:31` `def is_known(cls, value)` -- Return True when the value names a registered class.
- `GuardrailContract.describe` (method) `modules/guardrails/contracts.py:52` `def describe(self)` -- Return tier usage, advisories, suspended features and checkpoints.
- `GuardrailContract.run_guarded` (method) `modules/guardrails/contracts.py:56` `def run_guarded(self, task_class, fn)` -- Execute fn under capacity accounting and warm-restart policy.
- `GuardrailContract.warm_restart` (method) `modules/guardrails/contracts.py:68` `def warm_restart(self)` -- Purge non-critical contexts and restore the last checkpoint.
- `HarnessAdminPort.configure` (method) `modules/guardrails/contracts.py:76` `def configure(self, settings)` -- Apply capacity and threshold settings from the payload.
- `HarnessAdminPort.rearm` (method) `modules/guardrails/contracts.py:80` `def rearm(self)` -- Clear advisories and resume suspended features after an operator review.

## modules/guardrails/harness.py
Depends on: `modules/guardrails/advisories.py`, `modules/guardrails/budget.py`, `modules/guardrails/checkpoints.py`, `modules/guardrails/contracts.py`
Imported by: `modules/guardrails/__init__.py`
- `GuardHarness.__init__` (method) `modules/guardrails/harness.py:28` `def __init__(self, threshold, capacities)` -- Create a harness with payload-driven or default settings.
- `GuardHarness.configure` (method) `modules/guardrails/harness.py:48` `def configure(self, settings)` -- Apply settings from the payload guardrails section.
- `GuardHarness.run_guarded` (method) `modules/guardrails/harness.py:63` `def run_guarded(self, task_class, fn)` -- Execute fn under the tier policy, degrading instead of crashing.
- `GuardHarness.warm_restart` (method) `modules/guardrails/harness.py:124` `def warm_restart(self, core_key)` -- Purge non-critical contexts and restore the core checkpoint.
- `GuardHarness.suspend` (method) `modules/guardrails/harness.py:138` `def suspend(self, feature, reason)` -- Suspend one optional feature until re-arm.
- `GuardHarness.rearm` (method) `modules/guardrails/harness.py:153` `def rearm(self)` -- Resume suspended features, clear advisories and refresh budgets.
- `GuardHarness.describe` (method) `modules/guardrails/harness.py:165` `def describe(self)` -- Return the full harness snapshot for the admin console.
- `global_harness` (function) `modules/guardrails/harness.py:232` `def global_harness()` -- Return the process-wide harness, creating it on first use.
- `reset_global_harness` (function) `modules/guardrails/harness.py:241` `def reset_global_harness()` -- Replace the process-wide harness (tests and warm reloads only).

## modules/gui_askpass.sh
- `has` (function) `modules/gui_askpass.sh:22` -- ── helpers ───────────────────────────────────────────────────────────────────
- `try_zenity` (function) `modules/gui_askpass.sh:24`
- `try_yad` (function) `modules/gui_askpass.sh:28`
- `try_ssh_askpass` (function) `modules/gui_askpass.sh:33`
- `try_kdialog` (function) `modules/gui_askpass.sh:40`

## modules/gym_cleanup.py
Depends on: `core/config.py`, `core/logging.py`, `modules/__init__.py`
Imported by: `lazyown.py`, `tests/test_gym_lifecycle.py`
- `cleanup_enabled` (function) `modules/gym_cleanup.py:21` `def cleanup_enabled()` -- Return whether exit cleanup is enabled (default on).
- `cleanup_gym_machines` (function) `modules/gym_cleanup.py:35` `def cleanup_gym_machines(verbose)` -- Stop every running lab and range machine.

## modules/gym_matrix_runner.py
Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/chain_runner.py`
- `plan_matrix` (function) `modules/gym_matrix_runner.py:36` `def plan_matrix(target, sessions_dir, only, top_k)` -- Build the ordered execution plan for the gym matrix.
- `run_matrix` (function) `modules/gym_matrix_runner.py:89` `def run_matrix(target)` -- Execute every planned chain and verify its CTF capture.
- `load_matrix` (function) `modules/gym_matrix_runner.py:233` `def load_matrix(sessions_dir)` -- Read the persisted matrix summary.

## modules/gym_registry.py
Depends on: `core/logging.py`, `modules/world_model.py`
Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`
- `slugify` (function) `modules/gym_registry.py:92` `def slugify(value)` -- Return a safe gym identifier.
- `validate_definition` (function) `modules/gym_registry.py:110` `def validate_definition(data, filename)` -- Validate one gym definition mapping.
- `definition_path` (function) `modules/gym_registry.py:155` `def definition_path(gym_id, directory)` -- Resolve one gym YAML file inside the gyms directory.
- `load_definitions` (function) `modules/gym_registry.py:207` `def load_definitions(directory)` -- Load every valid gym definition.
- `scan_definitions` (function) `modules/gym_registry.py:239` `def scan_definitions(directory)` -- Return one row per YAML file, including invalid files.
- `create_definition` (function) `modules/gym_registry.py:300` `def create_definition(gym_id)` -- Create one gym definition YAML.
- `update_definition_yaml` (function) `modules/gym_registry.py:369` `def update_definition_yaml(gym_id, text, directory)` -- Parse, validate and atomically rewrite one definition.
- `delete_definition` (function) `modules/gym_registry.py:402` `def delete_definition(gym_id, directory)` -- Delete one definition unless it has active runs.
- `normalize_operator` (function) `modules/gym_registry.py:495` `def normalize_operator(value)` -- Return a bounded operator label.
- `read_state` (function) `modules/gym_registry.py:501` `def read_state()` -- Read the persistent gym state from the world model.
- `write_state` (function) `modules/gym_registry.py:520` `def write_state(state)` -- Persist one state document to the world model.
- `start_run` (function) `modules/gym_registry.py:579` `def start_run(challenge_id, definitions)` -- Start one run and persist it.
- `get_active_runs` (function) `modules/gym_registry.py:637` `def get_active_runs(selector, operator)` -- Return active runs, enriched with elapsed time.
- `select_run` (function) `modules/gym_registry.py:663` `def select_run(selector)` -- Resolve one active run.
- `stop_runs` (function) `modules/gym_registry.py:695` `def stop_runs(selector)` -- Stop one or every active run.
- `pop_run` (function) `modules/gym_registry.py:724` `def pop_run(selector)` -- Resolve and remove one run, returning its final state.
- `state_summary` (function) `modules/gym_registry.py:751` `def state_summary()` -- Return counters used by status output and the TUI.
- `new_run_token` (function) `modules/gym_registry.py:761` `def new_run_token()` -- Return an unguessable token for external integrations.

## modules/harness.py
Depends on: `core/config.py`, `core/logging.py`, `modules/orchestrator_config.py`
Imported by: `modules/lazy_loop.py`, `modules/llm_factory.py`, `skills/lazyown_mcp_opencode.py`
- `harness_enabled` (function) `modules/harness.py:30` `def harness_enabled()` -- Return True when the deterministic harness is active.
- `gate` (function) `modules/harness.py:65` `def gate(name)` -- Return whether one decision surface may remain stochastic.

## modules/hash_cracker.py
Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`
- `HashCracker.__init__` (method) `modules/hash_cracker.py:164` `def __init__(self, wordlist, rules, use_hashcat, timeout)`
- `HashCracker.identify` (method) `modules/hash_cracker.py:186` `def identify(self, line)` -- Identify the hash type of a single line.
- `HashCracker.identify_file` (method) `modules/hash_cracker.py:273` `def identify_file(self, filepath)` -- Parse a hash file and group hashes by type.
- `HashCracker.crack_hash` (method) `modules/hash_cracker.py:295` `def crack_hash(self, hash_value, hash_type, wordlist)` -- Attempt to crack a single hash.
- `HashCracker.crack_file` (method) `modules/hash_cracker.py:349` `def crack_file(self, filepath, wordlist, hash_types)` -- Crack all hashes in a file.
- `HashCracker.import_to_db` (method) `modules/hash_cracker.py:405` `def import_to_db(self, results, rhost, workspace_name)` -- Import cracked results into the LazyOwnDB credentials table.
- `crack_secretsdump_output` (function) `modules/hash_cracker.py:695` `def crack_secretsdump_output(filepath, wordlist, rhost)` -- Convenience function: crack a secretsdump output file and import results.

## modules/hive_invoke.py
Depends on: `modules/toposwarm_bridge.py`
- `main` (function) `modules/hive_invoke.py:255` `def main(argv)`

## modules/hostdiscover.sh
- `extract_ips_from_arp` (function) `modules/hostdiscover.sh:21`
- `extract_listening_ips_from_netstat` (function) `modules/hostdiscover.sh:26`

## modules/hunt_verify.py
Imported by: `modules/chain_runner.py`, `modules/defense_stages.py`, `tests/test_hunt_verify.py`
- `StageAssessment.to_dict` (method) `modules/hunt_verify.py:99` `def to_dict(self)` -- Return a JSON-serializable view.
- `Verification.chain_proven` (method) `modules/hunt_verify.py:124` `def chain_proven(self)` -- Return whether every stage has observed evidence.
- `Verification.to_dict` (method) `modules/hunt_verify.py:130` `def to_dict(self)` -- Return a JSON-serializable view.
- `field_present` (function) `modules/hunt_verify.py:152` `def field_present(fields, field_name)` -- Return whether one required field exists with a present scalar value.
- `validate_specs` (function) `modules/hunt_verify.py:197` `def validate_specs(specs)` -- Validate stage structure: caps, unique ids and known dependencies.
- `verify_stages` (function) `modules/hunt_verify.py:232` `def verify_stages(specs, observations, events, scope_covered)` -- Verify AI observations against retained events per stage.

## modules/ia_code_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `CodeAnalyzer.__init__` (method) `modules/ia_code_analysis.py:33` `def __init__(self, mode)`
- `CodeAnalyzer.analyze_directory` (method) `modules/ia_code_analysis.py:37` `def analyze_directory(self, directory)` -- Recursively analyzes all source code files in the specified directory.
- `CodeAnalyzer.analyze_code_file` (method) `modules/ia_code_analysis.py:49` `def analyze_code_file(self, file_path)` -- Analyzes the content of the source code file.
- `analyze_with_deepseek` (function) `modules/ia_code_analysis.py:66` `def analyze_with_deepseek(code_content, file_path, mode)` -- Sends the code content to DeepSeek for analysis.
- `save_results_to_json` (function) `modules/ia_code_analysis.py:123` `def save_results_to_json(results, file_path)` -- Saves the analysis results to JSON files.
- `start_analysis` (function) `modules/ia_code_analysis.py:169` `def start_analysis(code_dir, mode)` -- Starts the analysis of the specified code directory.
- `parse_args` (function) `modules/ia_code_analysis.py:178` `def parse_args()`

## modules/ia_logs_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `LogFileHandler.__init__` (method) `modules/ia_logs_analysis.py:59` `def __init__(self, mode)`
- `LogFileHandler.on_modified` (method) `modules/ia_logs_analysis.py:64` `def on_modified(self, event)` -- Triggered when a log file is modified.
- `LogFileHandler.analyze_log_file` (method) `modules/ia_logs_analysis.py:75` `def analyze_log_file(self, file_path)` -- Analyzes the content of the modified log file.
- `analyze_with_deepseek` (function) `modules/ia_logs_analysis.py:94` `def analyze_with_deepseek(log_content, mode)` -- Sends log content to DeepSeek for advanced analysis.
- `start_monitoring` (function) `modules/ia_logs_analysis.py:147` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/ia_logs_analysis.py:168` `def parse_args()`

## modules/ia_network_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `analyze_with_deepseek` (function) `modules/ia_network_analysis.py:39` `def analyze_with_deepseek(packet_info, mode)` -- Envía la información del paquete a DeepSeek para análisis avanzado.
- `packet_callback` (function) `modules/ia_network_analysis.py:91` `def packet_callback(packet, mode)` -- Callback para procesar cada paquete capturado.
- `start_monitoring` (function) `modules/ia_network_analysis.py:130` `def start_monitoring(interface, timeout, mode)` -- Inicia el monitoreo del tráfico de red.
- `parse_args` (function) `modules/ia_network_analysis.py:154` `def parse_args()`

## modules/icmp_client.py
- `encrypt_data` (function) `modules/icmp_client.py:18` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_client.py:34` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `check_sudo` (function) `modules/icmp_client.py:57` `def check_sudo()`
- `checksum` (function) `modules/icmp_client.py:64` `def checksum(source_string)`
- `send_icmp_packet` (function) `modules/icmp_client.py:82` `def send_icmp_packet(dest_addr, data, key)`
- `receive_icmp_reply` (function) `modules/icmp_client.py:117` `def receive_icmp_reply(sock)`
- `main` (function) `modules/icmp_client.py:130` `def main()`

## modules/icmp_server.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `check_sudo` (function) `modules/icmp_server.py:44` `def check_sudo()`
- `encrypt_data` (function) `modules/icmp_server.py:55` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_server.py:71` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `execute_command` (function) `modules/icmp_server.py:93` `def execute_command(command)`
- `send_icmp_reply` (function) `modules/icmp_server.py:112` `def send_icmp_reply(sock, addr, data, key)`
- `checksum` (function) `modules/icmp_server.py:132` `def checksum(source_string)`
- `handle_packet` (function) `modules/icmp_server.py:150` `def handle_packet(packet, addr, key, sock)`
- `listen_for_icmp` (function) `modules/icmp_server.py:175` `def listen_for_icmp(interface, key)`
- `main` (function) `modules/icmp_server.py:202` `def main()`

## modules/img2bin.py
- `imagen_a_binario` (function) `modules/img2bin.py:7` `def imagen_a_binario(imagen_input, binario_output, block_size)`
- `main` (function) `modules/img2bin.py:43` `def main()`

## modules/integrations/misp_export.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`, `tests/test_single_source_of_truth.py`
- `FindingMapper.map` (method) `modules/integrations/misp_export.py:90` `def map(self, finding)` -- Convert *finding* to a MISPAttribute.
- `IPMapper.map` (method) `modules/integrations/misp_export.py:106` `def map(self, finding)`
- `CredentialMapper.map` (method) `modules/integrations/misp_export.py:126` `def map(self, finding)`
- `CVEMapper.map` (method) `modules/integrations/misp_export.py:146` `def map(self, finding)`
- `DomainMapper.map` (method) `modules/integrations/misp_export.py:166` `def map(self, finding)`
- `HashMapper.map` (method) `modules/integrations/misp_export.py:192` `def map(self, finding)`
- `ServiceMapper.map` (method) `modules/integrations/misp_export.py:221` `def map(self, finding)`
- `MISPExporter.__init__` (method) `modules/integrations/misp_export.py:263` `def __init__(self, mappers)`
- `MISPExporter.export_session` (method) `modules/integrations/misp_export.py:268` `def export_session(self, sessions_dir, target)` -- Read policy_facts.json and events.jsonl from *sessions_dir*, map all findings, and return a populated MISPEvent.
- `MISPExporter.to_json` (method) `modules/integrations/misp_export.py:299` `def to_json(self, event)` -- Serialise *event* to a MISP-compatible JSON string.
- `MISPExporter.save` (method) `modules/integrations/misp_export.py:322` `def save(self, event, path)` -- Write the MISP event JSON to *path* and return the resolved path.
- `MISPExporter.push_to_misp` (method) `modules/integrations/misp_export.py:330` `def push_to_misp(self, event, url, api_key)` -- HTTP-push the event to a live MISP instance.
- `_DictFinding.__init__` (method) `modules/integrations/misp_export.py:501` `def __init__(self, data)`
- `get_exporter` (function) `modules/integrations/misp_export.py:516` `def get_exporter()` -- Return the module-level MISPExporter singleton.

## modules/integrations/nuclei_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`
- `TemplateSelector.select` (method) `modules/integrations/nuclei_bridge.py:91` `def select(self, services, cves)` -- Return templates relevant to the provided *services* and *cves*.
- `LocalTemplateIndex.__init__` (method) `modules/integrations/nuclei_bridge.py:114` `def __init__(self, templates_dir)`
- `LocalTemplateIndex.select` (method) `modules/integrations/nuclei_bridge.py:121` `def select(self, services, cves)`
- `LocalTemplateIndex.build` (method) `modules/integrations/nuclei_bridge.py:141` `def build(self)` -- Force a (re)build of the template index.
- `NucleiRunner.__init__` (method) `modules/integrations/nuclei_bridge.py:288` `def __init__(self)`
- `NucleiRunner.run` (method) `modules/integrations/nuclei_bridge.py:293` `def run(self, target, templates, output_dir)` -- Execute nuclei against *target* using the provided *templates*.
- `NucleiRunner.run_for_findings` (method) `modules/integrations/nuclei_bridge.py:326` `def run_for_findings(self, target, findings, output_dir, selector)` -- Convenience: extract services/CVEs from *findings*, select templates, run.
- `NucleiBridge.__init__` (method) `modules/integrations/nuclei_bridge.py:396` `def __init__(self, selector, runner)`
- `NucleiBridge.scan` (method) `modules/integrations/nuclei_bridge.py:404` `def scan(self, target, findings, dry_run)` -- Select templates from *findings* and run nuclei against *target*.
- `NucleiBridge.list_templates` (method) `modules/integrations/nuclei_bridge.py:427` `def list_templates(self, services, cves)` -- Return matching templates without running nuclei.
- `get_bridge` (function) `modules/integrations/nuclei_bridge.py:443` `def get_bridge()` -- Return the module-level NucleiBridge singleton.
- `_F.__init__` (method) `modules/integrations/nuclei_bridge.py:484` `def __init__(self, ftype, value)`

## modules/integrations/nuclei_parser.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/integrations/nuclei_bridge.py`, `modules/world_model.py`
Imported by: `modules/intelligence_engine.py`, `tests/test_nuclei_parser.py`
- `NucleiFinding.mitre_tactic` (method) `modules/integrations/nuclei_parser.py:87` `def mitre_tactic(self)`
- `NucleiFinding.exploit_probability` (method) `modules/integrations/nuclei_parser.py:95` `def exploit_probability(self)`
- `NucleiParser.__init__` (method) `modules/integrations/nuclei_parser.py:109` `def __init__(self, sessions_dir)`
- `NucleiParser.parse_text` (method) `modules/integrations/nuclei_parser.py:115` `def parse_text(self, text)` -- Parse raw nuclei text output (table format).
- `NucleiParser.parse_json` (method) `modules/integrations/nuclei_parser.py:134` `def parse_json(self, json_text)` -- Parse nuclei JSON output (``-jsonl`` or ``-json`` format).
- `NucleiParser.parse_file` (method) `modules/integrations/nuclei_parser.py:177` `def parse_file(self, filepath)` -- Parse nuclei output from a file (auto-detects format).
- `NucleiParser.import_to_db` (method) `modules/integrations/nuclei_parser.py:196` `def import_to_db(self, findings, rhost, workspace_name)` -- Import parsed findings into the LazyOwnDB vulnerabilities table.
- `NucleiParser.enrich_world_model` (method) `modules/integrations/nuclei_parser.py:262` `def enrich_world_model(self, findings, rhost)` -- Feed parsed findings into the WorldModel for autonomous decision-making.
- `NucleiParser.generate_recommendations` (method) `modules/integrations/nuclei_parser.py:300` `def generate_recommendations(self, findings, rhost)` -- Generate actionable LazyOwn command recommendations from findings.
- `NucleiParser.scan_and_import` (method) `modules/integrations/nuclei_parser.py:328` `def scan_and_import(self, target, templates, services, cves, workspace_name)` -- Run nuclei scan against target, parse output, and import to DB/WorldModel.

## modules/integrations/searchsploit.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `tests/test_core_modules.py`
- `ExploitSource.search_cve` (method) `modules/integrations/searchsploit.py:80` `def search_cve(self, cve_id)` -- Return exploits matching *cve_id* (e.g. 'CVE-2021-41773').
- `ExploitSource.search_service` (method) `modules/integrations/searchsploit.py:84` `def search_service(self, name, version)` -- Return exploits matching the service *name* and optional *version*.
- `SearchsploitCLI.__init__` (method) `modules/integrations/searchsploit.py:102` `def __init__(self)`
- `SearchsploitCLI.search_cve` (method) `modules/integrations/searchsploit.py:109` `def search_cve(self, cve_id)`
- `SearchsploitCLI.search_service` (method) `modules/integrations/searchsploit.py:112` `def search_service(self, name, version)`
- `ExploitDBAPI.__init__` (method) `modules/integrations/searchsploit.py:201` `def __init__(self)`
- `ExploitDBAPI.search_cve` (method) `modules/integrations/searchsploit.py:207` `def search_cve(self, cve_id)`
- `ExploitDBAPI.search_service` (method) `modules/integrations/searchsploit.py:210` `def search_service(self, name, version)`
- `SearchsploitClient.__init__` (method) `modules/integrations/searchsploit.py:278` `def __init__(self, primary, fallback)`
- `SearchsploitClient.search_cve` (method) `modules/integrations/searchsploit.py:286` `def search_cve(self, cve_id)` -- Return exploits for *cve_id*, trying CLI then API.
- `SearchsploitClient.search_service` (method) `modules/integrations/searchsploit.py:293` `def search_service(self, name, version)` -- Return exploits for *name*/*version*, trying CLI then API.
- `SearchsploitClient.enrich_findings` (method) `modules/integrations/searchsploit.py:300` `def enrich_findings(self, findings)` -- Takes an ObsParser Finding list, extracts CVEs and service_versions, returns ``{cve_or_service: [ExploitEntry, ...]}``.
- `get_client` (function) `modules/integrations/searchsploit.py:333` `def get_client()` -- Return the module-level SearchsploitClient singleton.
- `search_cve` (function) `modules/integrations/searchsploit.py:341` `def search_cve(cve_id)` -- Module-level convenience: search by CVE id.
- `search_service` (function) `modules/integrations/searchsploit.py:346` `def search_service(name, version)` -- Module-level convenience: search by service name and version.

## modules/intel_fusion.py
Depends on: `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/world_model.py`
Imported by: `lazyc2.py`, `modules/attack_surface3d.py`, `modules/sinks/intel_graph.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_intel_fusion.py`
- `node_id` (function) `modules/intel_fusion.py:106` `def node_id(kind, value)` -- Deterministic node id from kind + normalized value.
- `build_intel_graph` (function) `modules/intel_fusion.py:176` `def build_intel_graph(sessions_dir, est_cap)` -- Fuse all session artefacts into one C2-centred intel graph.
- `add_node` (function) `modules/intel_fusion.py:182` `def add_node(kind, value, label)` -- Insert node or merge extra fields into the existing one.
- `add_edge` (function) `modules/intel_fusion.py:200` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation.
- `tag_source` (function) `modules/intel_fusion.py:214` `def tag_source(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `group_colors` (function) `modules/intel_fusion.py:577` `def group_colors(graph)` -- Stable colors for layer/language groupings (ReadMenator contract).
- `page_settings` (function) `modules/intel_fusion.py:593` `def page_settings(graph)` -- Explorer page settings with ReadMenator physics sizes (exact values).
- `build_analytics` (function) `modules/intel_fusion.py:650` `def build_analytics(graph, summary)` -- Side-panel analytics (attribution funnel + intel summary).
- `build_bundle_payload` (function) `modules/intel_fusion.py:737` `def build_bundle_payload(graph)` -- Derive the circular/spherical bundle payload from a fused graph.
- `bundle_settings` (function) `modules/intel_fusion.py:853` `def bundle_settings(graph)` -- Bundle page settings with ReadMenator sizes (exact values).
- `assign_layout` (function) `modules/intel_fusion.py:884` `def assign_layout(graph, mode)` -- Attach x/y/z for radial/spherical modes; force modes stay free.
- `write_summary` (function) `modules/intel_fusion.py:949` `def write_summary(graph, sessions_dir)` -- Score host exposure and suggest intents for the autonomous planner.

## modules/intelligence_engine.py
Depends on: `core/logging.py`, `modules/estorides_importer.py`, `modules/factsio.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`, `tests/test_single_source_of_truth.py`
- `IntelligenceEngine.__init__` (method) `modules/intelligence_engine.py:142` `def __init__(self, config)`
- `IntelligenceEngine.collect_from_scan` (method) `modules/intelligence_engine.py:153` `def collect_from_scan(self, target)` -- Parse nmap XML into structured facts.
- `IntelligenceEngine.collect_from_tool` (method) `modules/intelligence_engine.py:255` `def collect_from_tool(self, output, tool, host)` -- Parse tool output into structured facts using ObsParser.
- `IntelligenceEngine.collect_from_estorides` (method) `modules/intelligence_engine.py:292` `def collect_from_estorides(self, target)` -- Run estorides OSINT aggregator and collect findings.
- `IntelligenceEngine.collect_from_nuclei` (method) `modules/intelligence_engine.py:334` `def collect_from_nuclei(self, target)` -- Run nuclei vulnerability scanner and collect findings.
- `IntelligenceEngine.collect_from_yara` (method) `modules/intelligence_engine.py:376` `def collect_from_yara(self, target_path)` -- Scan with YARA rules and collect IOC matches.
- `IntelligenceEngine.collect_from_factstore` (method) `modules/intelligence_engine.py:415` `def collect_from_factstore(self)` -- Ingest structured facts from FactStore policy_facts.json.
- `IntelligenceEngine.analyze` (method) `modules/intelligence_engine.py:516` `def analyze(self)` -- Correlate collected facts into structured intelligence.
- `IntelligenceEngine.produce_intelligence` (method) `modules/intelligence_engine.py:724` `def produce_intelligence(self)` -- Grade and enrich intelligence assessments with MITRE mappings.
- `IntelligenceEngine.produce_counter_intelligence` (method) `modules/intelligence_engine.py:754` `def produce_counter_intelligence(self)` -- Assess what we exposed and what can detect us.
- `IntelligenceEngine.disseminate` (method) `modules/intelligence_engine.py:804` `def disseminate(self)` -- Write intelligence to WorldModel, killchain, and report file.
- `IntelligenceEngine.run_full_cycle` (method) `modules/intelligence_engine.py:884` `def run_full_cycle(self, target)` -- Execute the complete intelligence cycle for a target.
- `IntelligenceEngine.get_intel_report` (method) `modules/intelligence_engine.py:913` `def get_intel_report(self)` -- Produce a structured JSON intelligence report.
- `get_intelligence_engine` (function) `modules/intelligence_engine.py:970` `def get_intelligence_engine(config)` -- Return the module-level singleton IntelligenceEngine.

## modules/intercept.py
Depends on: `cli/commands/enum.py`
Imported by: `cli/commands/daemon_ctl.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `InterceptRule.matches` (method) `modules/intercept.py:68` `def matches(self, tool, command)` -- Return True when this rule matches the tool call surface.
- `builtin_rules` (function) `modules/intercept.py:101` `def builtin_rules()` -- Return the default destructive and exfiltration guard rules.
- `scope_blocked` (function) `modules/intercept.py:131` `def scope_blocked(target)` -- Return the matching global scope suffix or empty (LAZY parity).
- `observe_post_tool` (function) `modules/intercept.py:144` `def observe_post_tool(output)` -- Classify post-execution output (LAZY Guard.postToolUse parity).
- `Interceptor.__init__` (method) `modules/intercept.py:157` `def __init__(self, rules, ask_timeout_sec, timeout_action)` -- Initialize with rules sorted by descending priority.
- `Interceptor.rules` (method) `modules/intercept.py:172` `def rules(self)` -- Return a copy of the active rule list.
- `Interceptor.add_rule` (method) `modules/intercept.py:177` `def add_rule(self, rule)` -- Add a rule and keep priority ordering.
- `Interceptor.remove_rule` (method) `modules/intercept.py:183` `def remove_rule(self, pattern)` -- Remove the first rule matching pattern text.
- `Interceptor.evaluate` (method) `modules/intercept.py:192` `def evaluate(self, tool, command)` -- Evaluate a tool call and return the verdict.
- `Interceptor.decide` (method) `modules/intercept.py:220` `def decide(self, approval_id, decision)` -- Resolve a pending approval with approve or deny.
- `Interceptor.pending_approvals` (method) `modules/intercept.py:234` `def pending_approvals(self)` -- List unresolved approvals, expiring timed-out ones per policy.
- `Interceptor.approval_status` (method) `modules/intercept.py:249` `def approval_status(self, approval_id)` -- Fetch a single approval record by id.
- `Guard.__init__` (method) `modules/intercept.py:258` `def __init__(self, interceptor)` -- Initialize audit log with an optional interceptor.
- `Guard.interceptor` (method) `modules/intercept.py:266` `def interceptor(self)` -- Expose the underlying interceptor.
- `Guard.check` (method) `modules/intercept.py:270` `def check(self, tool, command)` -- Audit the call then evaluate intercept rules (trace id kept).
- `Guard.observe` (method) `modules/intercept.py:282` `def observe(self, output, source)` -- Classify output and attribute blocked/error counters.
- `Guard.record_failure` (method) `modules/intercept.py:291` `def record_failure(self, source)` -- Attribute a post-execution failure to a source.
- `Guard.audit_log` (method) `modules/intercept.py:296` `def audit_log(self, limit)` -- Return the most recent audit entries.
- `Guard.attribution` (method) `modules/intercept.py:301` `def attribution(self)` -- Return failure attribution counters.

## modules/iptables_portforward.sh
- `display_usage` (function) `modules/iptables_portforward.sh:29`

## modules/jsonl_tail.py
Imported by: `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_runner.py`
- `JsonlTail.__init__` (method) `modules/jsonl_tail.py:17` `def __init__(self, path)` -- Bind the tail to one file path.
- `JsonlTail.read_new` (method) `modules/jsonl_tail.py:22` `def read_new(self, limit)` -- Return new complete records since the last call.

## modules/k8s_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `K8SAttackEngine.__init__` (method) `modules/k8s_attacks.py:87` `def __init__(self, config)`
- `K8SAttackEngine.enumerate_rbac` (method) `modules/k8s_attacks.py:90` `def enumerate_rbac(self)` -- Enumerate RBAC permissions for the current identity.
- `K8SAttackEngine.privileged_pod_escape` (method) `modules/k8s_attacks.py:118` `def privileged_pod_escape(self)` -- Plan a privileged pod escape.
- `K8SAttackEngine.service_account_token_theft` (method) `modules/k8s_attacks.py:173` `def service_account_token_theft(self)` -- Steal service account tokens across namespaces for lateral movement.
- `K8SAttackEngine.kubelet_anonymous_auth_abuse` (method) `modules/k8s_attacks.py:198` `def kubelet_anonymous_auth_abuse(self)` -- Exploit kubelet anonymous authentication.
- `K8SAttackEngine.etcd_access_exploitation` (method) `modules/k8s_attacks.py:222` `def etcd_access_exploitation(self)` -- Exploit etcd database access for complete cluster compromise.
- `K8SAttackEngine.helm_tiller_abuse` (method) `modules/k8s_attacks.py:250` `def helm_tiller_abuse(self)` -- Abuse Helm (v2 Tiller or v3 RBAC) for privilege escalation.
- `K8SAttackEngine.persistence_techniques` (method) `modules/k8s_attacks.py:278` `def persistence_techniques(self)` -- Kubernetes persistence techniques for long-term access.
- `K8SAttackEngine.summary` (method) `modules/k8s_attacks.py:318` `def summary(self)`


Next: [API_p13.md](API_p13.md)
