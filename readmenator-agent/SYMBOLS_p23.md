# Symbols (page 23 of 45)
Previous: [SYMBOLS_p22.md](SYMBOLS_p22.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_persist_lessons` | method | `skills/aci_planner.py:854` | `def _persist_lessons(self, lessons)` |
| `_save_plan` | function | `skills/aci_planner.py:235` | `def _save_plan(plan, plan_file)` |
| `_sync_phase_statuses` | method | `skills/aci_planner.py:756` | `def _sync_phase_statuses(self, plan)` |
| `_write_objective` | method | `skills/aci_planner.py:573` | `def _write_objective(self, text, phase, target)` |
| `active_phase` | method | `skills/aci_planner.py:199` | `def active_phase(self)` |
| `complete` | method | `skills/aci_planner.py:743` | `def complete(self)` |
| `completion_pct` | method | `skills/aci_planner.py:207` | `def completion_pct(self)` |
| `from_dict` | method | `skills/aci_planner.py:176` | `def from_dict(cls, d)` |
| `from_dict` | method | `skills/aci_planner.py:221` | `def from_dict(cls, d)` |
| `main` | function | `skills/aci_planner.py:1005` | `def main(argv)` |
| `mcp_aci_plan` | function | `skills/aci_planner.py:867` | `def mcp_aci_plan(goal, target, scope, domain, os_hint, phase_filter)` |
| `mcp_aci_replan` | function | `skills/aci_planner.py:942` | `def mcp_aci_replan(reason)` |
| `mcp_aci_status` | function | `skills/aci_planner.py:925` | `def mcp_aci_status()` |
| `plan` | method | `skills/aci_planner.py:473` | `def plan(self, goal, phase_filter)` |
| `reflect` | method | `skills/aci_planner.py:802` | `def reflect(self, plan)` |
| `replan` | method | `skills/aci_planner.py:673` | `def replan(self, reason)` |
| `should_replan` | method | `skills/aci_planner.py:660` | `def should_replan(self, plan)` |
| `status` | method | `skills/aci_planner.py:620` | `def status(self)` |
| `to_dict` | method | `skills/aci_planner.py:171` | `def to_dict(self)` |
| `to_dict` | method | `skills/aci_planner.py:214` | `def to_dict(self)` |
| `BridgeFallbackResolver` | class | `skills/autonomous_daemon.py:3164` | `class BridgeFallbackResolver(IToolFallbackResolver)` |
| `BridgeSelector` | class | `skills/autonomous_daemon.py:790` | `class BridgeSelector(ICommandSelector)` |
| `CascadeStrategy` | class | `skills/autonomous_daemon.py:1339` | `class CascadeStrategy` |
| `CommandDecision` | class | `skills/autonomous_daemon.py:674` | `class CommandDecision` |
| `CommandRunnerChain` | class | `skills/autonomous_daemon.py:583` | `class CommandRunnerChain(ICommandRunner)` |
| `CredentialSpraySelector` | class | `skills/autonomous_daemon.py:1283` | `class CredentialSpraySelector(ICommandSelector)` |
| `DroneCoordinator` | class | `skills/autonomous_daemon.py:2808` | `class DroneCoordinator` |
| `EngageOrchestrator` | class | `skills/autonomous_daemon.py:3303` | `class EngageOrchestrator` |
| `EnginePhaseResult` | class | `skills/autonomous_daemon.py:3113` | `class EnginePhaseResult` |
| `EnginePhaseStep` | class | `skills/autonomous_daemon.py:3096` | `class EnginePhaseStep` |
| `ExecutionEngine` | class | `skills/autonomous_daemon.py:1469` | `class ExecutionEngine(IObjectiveHandler)` |
| `FallbackSelector` | class | `skills/autonomous_daemon.py:1029` | `class FallbackSelector(ICommandSelector)` |
| `ICommandRunner` | class | `skills/autonomous_daemon.py:422` | `class ICommandRunner(ABC)` |
| `ICommandSelector` | class | `skills/autonomous_daemon.py:685` | `class ICommandSelector(ABC)` |
| `IObjectiveHandler` | class | `skills/autonomous_daemon.py:1455` | `class IObjectiveHandler(ABC)` |
| `IToolFallbackResolver` | class | `skills/autonomous_daemon.py:3130` | `class IToolFallbackResolver(ABC)` |
| `LLMSelector` | class | `skills/autonomous_daemon.py:859` | `class LLMSelector(ICommandSelector)` |
| `MCPCommandRunner` | class | `skills/autonomous_daemon.py:475` | `class MCPCommandRunner(ICommandRunner)` |
| `MetricsAwareSelector` | class | `skills/autonomous_daemon.py:1052` | `class MetricsAwareSelector(ICommandSelector)` |
| `PTYCommandRunner` | class | `skills/autonomous_daemon.py:494` | `class PTYCommandRunner(ICommandRunner)` |
| `ParquetSelector` | class | `skills/autonomous_daemon.py:744` | `class ParquetSelector(ICommandSelector)` |
| `ReactiveSelector` | class | `skills/autonomous_daemon.py:698` | `class ReactiveSelector(ICommandSelector)` |
| `SWANSelector` | class | `skills/autonomous_daemon.py:959` | `class SWANSelector(ICommandSelector)` |
| `StaticFallbackResolver` | class | `skills/autonomous_daemon.py:3143` | `class StaticFallbackResolver(IToolFallbackResolver)` |
| `StepResult` | class | `skills/autonomous_daemon.py:1443` | `class StepResult` |
| `StrategyEngine` | class | `skills/autonomous_daemon.py:1370` | `class StrategyEngine` |
| `_ShellDetector` | class | `skills/autonomous_daemon.py:3212` | `class _ShellDetector` |
| `__init__` | method | `skills/autonomous_daemon.py:592` | `def __init__(self, runners)` |
| `__init__` | method | `skills/autonomous_daemon.py:704` | `def __init__(self, reactive_engine)` |
| `__init__` | method | `skills/autonomous_daemon.py:750` | `def __init__(self, pdb, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:796` | `def __init__(self, dispatcher, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:1073` | `def __init__(self, wrapped, metrics_source, min_success_rate, min_attempts, window_seconds, cache_ttl_s, clock)` |
| `__init__` | method | `skills/autonomous_daemon.py:1306` | `def __init__(self, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:1346` | `def __init__(self, selectors)` |
| `__init__` | method | `skills/autonomous_daemon.py:1384` | `def __init__(self, runner, selectors)` |
| `__init__` | method | `skills/autonomous_daemon.py:1481` | `def __init__(self, strategy, max_steps, world_model, obs_parser, facts, loop)` |
| `__init__` | method | `skills/autonomous_daemon.py:2817` | `def __init__(self)` |
| `__init__` | method | `skills/autonomous_daemon.py:3173` | `def __init__(self, dispatcher)` |
| `__init__` | method | `skills/autonomous_daemon.py:3225` | `def __init__(self, narrator)` |
| `__init__` | method | `skills/autonomous_daemon.py:3317` | `def __init__(self, target, runner, narrator, approval_gate, fallback_resolver, shell_detector, plan...` |
| `_ask_via` | function | `skills/autonomous_daemon.py:928` | `def _ask_via(_backend, _goal, _key)` |
| `_bridge_candidate` | method | `skills/autonomous_daemon.py:811` | `def _bridge_candidate(self, phase, services, tag, os_hint)` |
| `_build_default_runner` | function | `skills/autonomous_daemon.py:613` | `def _build_default_runner()` |
| `_candidates` | method | `skills/autonomous_daemon.py:3178` | `def _candidates(self, primary, phase)` |
| `_clear_pid` | function | `skills/autonomous_daemon.py:4648` | `def _clear_pid()` |
| `_compute_step_reward` | function | `skills/autonomous_daemon.py:1648` | `def _compute_step_reward(output, command, phase, success, findings, prev_cmds)` |
| `_consult_gate` | method | `skills/autonomous_daemon.py:3888` | `def _consult_gate(self, step)` |
| `_credential_worth_task` | function | `skills/autonomous_daemon.py:206` | `def _credential_worth_task(cred)` |
| `_current_bridge_phase` | function | `skills/autonomous_daemon.py:3020` | `def _current_bridge_phase()` |
| `_current_summary` | method | `skills/autonomous_daemon.py:1151` | `def _current_summary(self)` |
| `_daemon_tool` | function | `skills/autonomous_daemon.py:457` | `def _daemon_tool(command)` |
| `_detect_target_os` | function | `skills/autonomous_daemon.py:1721` | `def _detect_target_os(target, loop)` |
| `_dispatch_pipeline` | function | `skills/autonomous_daemon.py:4923` | `def _dispatch_pipeline(args)` |
| `_emit` | function | `skills/autonomous_daemon.py:290` | `def _emit(event_type, payload, severity)` |
| `_engage_run_sync` | function | `skills/autonomous_daemon.py:3967` | `def _engage_run_sync(target, max_switches_per_step, auto)` |
| `_execute` | method | `skills/autonomous_daemon.py:3903` | `def _execute(self, command, timeout_s)` |
| `_get_campaign_blacklist` | function | `skills/autonomous_daemon.py:1638` | `def _get_campaign_blacklist()` |
| `_get_phase_command_catalog` | function | `skills/autonomous_daemon.py:840` | `def _get_phase_command_catalog(phase)` |
| `_inject_to_tasks_json` | function | `skills/autonomous_daemon.py:247` | `def _inject_to_tasks_json(title, description, operator, status)` |
| `_is_running` | function | `skills/autonomous_daemon.py:4660` | `def _is_running()` |
| `_ledger_path` | function | `skills/autonomous_daemon.py:3059` | `def _ledger_path()` |
| `_ledger_write` | function | `skills/autonomous_daemon.py:3069` | `def _ledger_write(engagement_id, intent_id, command, phase, state, reason)` |
| `_llm_candidate` | method | `skills/autonomous_daemon.py:872` | `def _llm_candidate(self, target, phase, context)` |
| `_load_campaign_blacklist` | function | `skills/autonomous_daemon.py:1608` | `def _load_campaign_blacklist()` |
| `_load_payload` | function | `skills/autonomous_daemon.py:1579` | `def _load_payload()` |
| `_main_async` | function | `skills/autonomous_daemon.py:4592` | `def _main_async(max_steps)` |
| `_maybe_generate_report` | function | `skills/autonomous_daemon.py:3941` | `def _maybe_generate_report()` |
| `_notify_finding` | function | `skills/autonomous_daemon.py:328` | `def _notify_finding(title, body, severity)` |
| `_objective_proven` | function | `skills/autonomous_daemon.py:353` | `def _objective_proven(objective_text, world_model, target, credential_found)` |
| `_parquet_candidate` | method | `skills/autonomous_daemon.py:767` | `def _parquet_candidate(self, category, target)` |
| `_planner_fallback_verb` | method | `skills/autonomous_daemon.py:3644` | `def _planner_fallback_verb(self, tried)` |
| `_read_pid` | function | `skills/autonomous_daemon.py:4653` | `def _read_pid()` |
| `_read_recent_csv_commands` | function | `skills/autonomous_daemon.py:1587` | `def _read_recent_csv_commands(limit)` |
| `_record_intent` | function | `skills/autonomous_daemon.py:313` | `def _record_intent(objective_id, step_n, command, state, reason)` |
| `_resolve_source` | method | `skills/autonomous_daemon.py:1124` | `def _resolve_source(self)` |
| `_run` | function | `skills/autonomous_daemon.py:4791` | `def _run()` |
| `_run_lazyown` | function | `skills/autonomous_daemon.py:622` | `def _run_lazyown(command, timeout)` |
| `_run_objective` | function | `skills/autonomous_daemon.py:1768` | `def _run_objective(objective_id, objective_text, target, max_steps, strategy, world_model, obs_parser, facts, loop...` |
| `_run_planner_intents` | method | `skills/autonomous_daemon.py:3525` | `def _run_planner_intents(self, results, fp_before, max_intents, planner)` |
| `_run_step` | method | `skills/autonomous_daemon.py:3668` | `def _run_step(self, step)` |
| `_run_sync` | method | `skills/autonomous_daemon.py:1527` | `def _run_sync(self, objective_id, objective_text, target)` |
| `_settle_state` | function | `skills/autonomous_daemon.py:3083` | `def _settle_state(result)` |
| `_should_skip` | method | `skills/autonomous_daemon.py:1181` | `def _should_skip(self, command)` |
| `_step_succeeded` | method | `skills/autonomous_daemon.py:3909` | `def _step_succeeded(command, output)` |
| `_strip_between_markers` | function | `skills/autonomous_daemon.py:444` | `def _strip_between_markers(output, marker)` |
| `_swan_candidate` | method | `skills/autonomous_daemon.py:996` | `def _swan_candidate(self, target, phase, context)` |
| `_tactic_phase` | function | `skills/autonomous_daemon.py:3054` | `def _tactic_phase(tactic)` |
| `_target_services` | function | `skills/autonomous_daemon.py:3033` | `def _target_services(target)` |
| `_task_title_open` | function | `skills/autonomous_daemon.py:228` | `def _task_title_open(title)` |
| `_try_import` | function | `skills/autonomous_daemon.py:126` | `def _try_import(module, attr)` |
| `_update_task_status` | function | `skills/autonomous_daemon.py:185` | `def _update_task_status(title, new_status)` |
| `_with_markers` | function | `skills/autonomous_daemon.py:435` | `def _with_markers(command, marker)` |
| `_worker` | function | `skills/autonomous_daemon.py:4064` | `def _worker()` |
| `_world_fingerprint` | function | `skills/autonomous_daemon.py:3011` | `def _world_fingerprint()` |
| `_wrap_chain_with_metrics_bias` | function | `skills/autonomous_daemon.py:1245` | `def _wrap_chain_with_metrics_bias(selectors, enabled)` |
| `_write_pid` | function | `skills/autonomous_daemon.py:4643` | `def _write_pid()` |
| `_write_status` | function | `skills/autonomous_daemon.py:4197` | `def _write_status()` |
| `cmd_engage` | function | `skills/autonomous_daemon.py:4169` | `def cmd_engage(target, max_switches_per_step, detach)` |
| `cmd_inject` | function | `skills/autonomous_daemon.py:4743` | `def cmd_inject(text, priority)` |
| `cmd_run` | function | `skills/autonomous_daemon.py:4671` | `def cmd_run(max_steps)` |
| `cmd_start` | function | `skills/autonomous_daemon.py:4680` | `def cmd_start(max_steps)` |
| `cmd_status` | function | `skills/autonomous_daemon.py:4727` | `def cmd_status()` |
| `cmd_stop` | function | `skills/autonomous_daemon.py:4710` | `def cmd_stop()` |
| `compute_decision_seed` | function | `skills/autonomous_daemon.py:394` | `def compute_decision_seed(objective_id, step_n, source)` |
| `detect_in_output` | method | `skills/autonomous_daemon.py:3271` | `def detect_in_output(self, output, target)` |
| `did_switch` | method | `skills/autonomous_daemon.py:3125` | `def did_switch(self)` |
| `engagement_id` | method | `skills/autonomous_daemon.py:3362` | `def engagement_id(self)` |
| `handle` | method | `skills/autonomous_daemon.py:1459` | `def handle(self, objective_id, objective_text, target, context)` |
| `handle` | method | `skills/autonomous_daemon.py:1497` | `def handle(self, objective_id, objective_text, target, context)` |
| `heartbeat_loop` | function | `skills/autonomous_daemon.py:4544` | `def heartbeat_loop()` |
| `mcp_autonomous_events` | function | `skills/autonomous_daemon.py:4892` | `def mcp_autonomous_events(last_n)` |
| `mcp_autonomous_inject` | function | `skills/autonomous_daemon.py:4848` | `def mcp_autonomous_inject(text, priority, target)` |
| `mcp_autonomous_start` | function | `skills/autonomous_daemon.py:4777` | `def mcp_autonomous_start(max_steps, backend)` |
| `mcp_autonomous_status` | function | `skills/autonomous_daemon.py:4835` | `def mcp_autonomous_status()` |
| `mcp_autonomous_stop` | function | `skills/autonomous_daemon.py:4819` | `def mcp_autonomous_stop()` |
| `mcp_engage_approve` | function | `skills/autonomous_daemon.py:4126` | `def mcp_engage_approve(approval_id, decision, operator)` |
| `mcp_engage_list_pending` | function | `skills/autonomous_daemon.py:4151` | `def mcp_engage_list_pending()` |
| `mcp_engage_status` | function | `skills/autonomous_daemon.py:4100` | `def mcp_engage_status(last_n)` |
| `mcp_engage_target` | function | `skills/autonomous_daemon.py:4010` | `def mcp_engage_target(target, max_switches_per_step, detach, auto)` |
| `name` | method | `skills/autonomous_daemon.py:431` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:482` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:502` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:598` | `def name(self)` |
| `next_command` | method | `skills/autonomous_daemon.py:1349` | `def next_command(self, target, phase, context)` |
| `next_command` | method | `skills/autonomous_daemon.py:1425` | `def next_command(self, target, phase, services, os_hint)` |
| `next_tool` | method | `skills/autonomous_daemon.py:3134` | `def next_tool(self, failed_command, phase, attempt)` |
| `next_tool` | method | `skills/autonomous_daemon.py:3151` | `def next_tool(self, failed_command, phase, attempt)` |
| `next_tool` | method | `skills/autonomous_daemon.py:3198` | `def next_tool(self, failed_command, phase, attempt)` |
| `objective_loop` | function | `skills/autonomous_daemon.py:4208` | `def objective_loop(max_steps, loop)` |
| `poll` | method | `skills/autonomous_daemon.py:3230` | `def poll(self, target)` |
| `process_findings` | method | `skills/autonomous_daemon.py:2822` | `def process_findings(self, findings, target, objective_id, payload_key)` |
| `register_output` | method | `skills/autonomous_daemon.py:708` | `def register_output(self, output, command, platform)` |
| `register_output` | method | `skills/autonomous_daemon.py:1411` | `def register_output(self, output, command, platform, success)` |
| `run` | method | `skills/autonomous_daemon.py:426` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:485` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:505` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:601` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:3366` | `def run(self)` |
| `run_async` | method | `skills/autonomous_daemon.py:1507` | `def run_async(self, objective_id, objective_text, target)` |
| `select` | method | `skills/autonomous_daemon.py:689` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:735` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:754` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:800` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:866` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:990` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:1036` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:1205` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:1310` | `def select(self, target, phase, context)` |
| `world_model_watcher` | function | `skills/autonomous_daemon.py:4351` | `def world_model_watcher(loop)` |
| `wrapped` | method | `skills/autonomous_daemon.py:1119` | `def wrapped(self)` |
| `EventLogReader` | class | `skills/autonomous_replay.py:127` | `class EventLogReader` |
| `ReplayDispatcher` | class | `skills/autonomous_replay.py:212` | `class ReplayDispatcher` |
| `ReplayDivergence` | class | `skills/autonomous_replay.py:82` | `class ReplayDivergence` |
| `ReplayReport` | class | `skills/autonomous_replay.py:93` | `class ReplayReport` |
| `ReplayStep` | class | `skills/autonomous_replay.py:53` | `class ReplayStep` |
| `__init__` | method | `skills/autonomous_replay.py:136` | `def __init__(self, path)` |
| `__init__` | method | `skills/autonomous_replay.py:221` | `def __init__(self, reader, seed_fn)` |
| `_build_step` | method | `skills/autonomous_replay.py:278` | `def _build_step(self, event, divergences)` |
| `_collect_step_events` | method | `skills/autonomous_replay.py:261` | `def _collect_step_events(self, from_event_id, to_event_id)` |
| `_default_runner` | method | `skills/autonomous_replay.py:413` | `def _default_runner()` |
| `_default_seed_fn` | method | `skills/autonomous_replay.py:241` | `def _default_seed_fn()` |
| `_invoke_runner` | method | `skills/autonomous_replay.py:441` | `def _invoke_runner(runner, command, timeout)` |
| `execute` | method | `skills/autonomous_replay.py:357` | `def execute(self, from_event_id, to_event_id, runner, timeout)` |
| `path` | method | `skills/autonomous_replay.py:147` | `def path(self)` |
| `read` | method | `skills/autonomous_replay.py:152` | `def read(self)` |
| `replay` | function | `skills/autonomous_replay.py:473` | `def replay(from_event_id, to_event_id, mode, events_path, runner, timeout)` |
| `slice` | method | `skills/autonomous_replay.py:177` | `def slice(self, events, from_event_id, to_event_id)` |
| `to_dict` | method | `skills/autonomous_replay.py:114` | `def to_dict(self)` |
| `trace` | method | `skills/autonomous_replay.py:325` | `def trace(self, from_event_id, to_event_id)` |
| `BddResult` | class | `skills/claude_md_orchestrator/bdd_agent.py:113` | `class BddResult` |
| `_compose_implementation` | function | `skills/claude_md_orchestrator/bdd_agent.py:95` | `def _compose_implementation(spec, contract)` |
| `_ensure_init` | function | `skills/claude_md_orchestrator/bdd_agent.py:130` | `def _ensure_init(config)` |
| `_module_name` | function | `skills/claude_md_orchestrator/bdd_agent.py:80` | `def _module_name(contract)` |
| `_module_path` | function | `skills/claude_md_orchestrator/bdd_agent.py:85` | `def _module_path(contract, config)` |
| `_package_init` | function | `skills/claude_md_orchestrator/bdd_agent.py:90` | `def _package_init(config)` |
| `_run_pytest` | function | `skills/claude_md_orchestrator/bdd_agent.py:138` | `def _run_pytest(test_path, cwd)` |
| `run` | function | `skills/claude_md_orchestrator/bdd_agent.py:151` | `def run(contract, spec, suite, config)` |
| `ScoutReport` | class | `skills/claude_md_orchestrator/boy_scout.py:30` | `class ScoutReport` |
| `_inspect` | function | `skills/claude_md_orchestrator/boy_scout.py:45` | `def _inspect(path)` |
| `_render_proposal` | function | `skills/claude_md_orchestrator/boy_scout.py:73` | `def _render_proposal(contract, findings)` |
| `run` | function | `skills/claude_md_orchestrator/boy_scout.py:90` | `def run(state, config)` |
| `write_report` | function | `skills/claude_md_orchestrator/boy_scout.py:110` | `def write_report(report, config)` |
| `CicdResult` | class | `skills/claude_md_orchestrator/cicd_agent.py:71` | `class CicdResult` |
| `_ensure_branch` | function | `skills/claude_md_orchestrator/cicd_agent.py:108` | `def _ensure_branch(contract, config)` |
| `_git` | function | `skills/claude_md_orchestrator/cicd_agent.py:97` | `def _git()` |
| `_render_pipeline` | function | `skills/claude_md_orchestrator/cicd_agent.py:134` | `def _render_pipeline(contract, spec, config)` |
| `_render_pr_body` | function | `skills/claude_md_orchestrator/cicd_agent.py:144` | `def _render_pr_body(contract, spec, report)` |
| `_slug` | function | `skills/claude_md_orchestrator/cicd_agent.py:91` | `def _slug(contract)` |
| `run` | function | `skills/claude_md_orchestrator/cicd_agent.py:177` | `def run(contract, spec, report, config)` |
| `Config` | class | `skills/claude_md_orchestrator/config.py:67` | `class Config` |
| `_default_claude_md` | function | `skills/claude_md_orchestrator/config.py:52` | `def _default_claude_md()` |
| `_default_run_dir` | function | `skills/claude_md_orchestrator/config.py:37` | `def _default_run_dir()` |
| `_repo_root` | function | `skills/claude_md_orchestrator/config.py:22` | `def _repo_root()` |
| `docs_dir` | method | `skills/claude_md_orchestrator/config.py:142` | `def docs_dir(self)` |
| `ensure` | method | `skills/claude_md_orchestrator/config.py:112` | `def ensure(self)` |
| `load_config` | function | `skills/claude_md_orchestrator/config.py:155` | `def load_config()` |
| `log_path` | method | `skills/claude_md_orchestrator/config.py:150` | `def log_path(self)` |
| `logs_dir` | method | `skills/claude_md_orchestrator/config.py:146` | `def logs_dir(self)` |
| `resolve_optional` | function | `skills/claude_md_orchestrator/config.py:164` | `def resolve_optional(config, key)` |
| `review_dir` | method | `skills/claude_md_orchestrator/config.py:138` | `def review_dir(self)` |
| `specs_dir` | method | `skills/claude_md_orchestrator/config.py:126` | `def specs_dir(self)` |
| `src_dir` | method | `skills/claude_md_orchestrator/config.py:134` | `def src_dir(self)` |
| `state_path` | method | `skills/claude_md_orchestrator/config.py:122` | `def state_path(self)` |
| `tests_dir` | method | `skills/claude_md_orchestrator/config.py:130` | `def tests_dir(self)` |
| `DocResult` | class | `skills/claude_md_orchestrator/documentation_agent.py:28` | `class DocResult` |
| `_format_inputs` | function | `skills/claude_md_orchestrator/documentation_agent.py:40` | `def _format_inputs(spec)` |
| `_format_review` | function | `skills/claude_md_orchestrator/documentation_agent.py:54` | `def _format_review(report)` |
| `_format_sad_paths` | function | `skills/claude_md_orchestrator/documentation_agent.py:47` | `def _format_sad_paths(spec)` |
| `_render` | function | `skills/claude_md_orchestrator/documentation_agent.py:68` | `def _render(contract, spec, report)` |
| `_wrap` | function | `skills/claude_md_orchestrator/documentation_agent.py:118` | `def _wrap(body)` |
| `run` | function | `skills/claude_md_orchestrator/documentation_agent.py:123` | `def run(contract, spec, report, config)` |
| `CicleState` | class | `skills/claude_md_orchestrator/models.py:348` | `class CicleState` |
| `CicleStateFile` | class | `skills/claude_md_orchestrator/models.py:424` | `class CicleStateFile` |
| `Contract` | class | `skills/claude_md_orchestrator/models.py:68` | `class Contract` |
| `Finding` | class | `skills/claude_md_orchestrator/models.py:255` | `class Finding` |
| `ReviewReport` | class | `skills/claude_md_orchestrator/models.py:291` | `class ReviewReport` |
| `SadPath` | class | `skills/claude_md_orchestrator/models.py:109` | `class SadPath` |
| `Severity` | class | `skills/claude_md_orchestrator/models.py:50` | `class Severity(StrEnum)` |
| `Spec` | class | `skills/claude_md_orchestrator/models.py:134` | `class Spec` |
| `Stage` | class | `skills/claude_md_orchestrator/models.py:28` | `class Stage(StrEnum)` |
| `TestSuite` | class | `skills/claude_md_orchestrator/models.py:217` | `class TestSuite` |
| `_now_iso` | function | `skills/claude_md_orchestrator/models.py:19` | `def _now_iso()` |
| `blockers` | method | `skills/claude_md_orchestrator/models.py:315` | `def blockers(self)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:96` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:125` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:173` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:243` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:280` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:333` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:402` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:450` | `def from_dict(cls, data)` |
| `load` | method | `skills/claude_md_orchestrator/models.py:467` | `def load(cls, path)` |
| `save` | method | `skills/claude_md_orchestrator/models.py:459` | `def save(self, path)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:91` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:120` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:166` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:236` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:270` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:319` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:383` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:440` | `def to_dict(self)` |
| `validate` | method | `skills/claude_md_orchestrator/models.py:189` | `def validate(self, min_sad_paths)` |
| `write_jsonl` | function | `skills/claude_md_orchestrator/models.py:480` | `def write_jsonl(path, event)` |
| `CycleSummary` | class | `skills/claude_md_orchestrator/orchestrator.py:34` | `class CycleSummary` |
| `_advance` | function | `skills/claude_md_orchestrator/orchestrator.py:234` | `def _advance(state, contract_id, config, options)` |
| `_banner` | function | `skills/claude_md_orchestrator/orchestrator.py:52` | `def _banner(message, config)` |
| `_build_parser` | function | `skills/claude_md_orchestrator/orchestrator.py:324` | `def _build_parser()` |
| `_halt` | function | `skills/claude_md_orchestrator/orchestrator.py:59` | `def _halt(summary, contract_id, reason)` |
| `_load_seed_contracts` | function | `skills/claude_md_orchestrator/orchestrator.py:365` | `def _load_seed_contracts(args, options)` |
| `_load_spec` | function | `skills/claude_md_orchestrator/orchestrator.py:217` | `def _load_spec(path)` |
| `_load_state` | function | `skills/claude_md_orchestrator/orchestrator.py:84` | `def _load_state(config)` |
| `_persist` | function | `skills/claude_md_orchestrator/orchestrator.py:66` | `def _persist(state, config)` |
| `_print_summary` | function | `skills/claude_md_orchestrator/orchestrator.py:301` | `def _print_summary(summary)` |
| `_run_cicd` | function | `skills/claude_md_orchestrator/orchestrator.py:182` | `def _run_cicd(state, config)` |
| `_run_documentation` | function | `skills/claude_md_orchestrator/orchestrator.py:158` | `def _run_documentation(state, config)` |
| `_run_implementation` | function | `skills/claude_md_orchestrator/orchestrator.py:125` | `def _run_implementation(state, config)` |
| `_run_review` | function | `skills/claude_md_orchestrator/orchestrator.py:146` | `def _run_review(state, config)` |
| `_run_scout` | function | `skills/claude_md_orchestrator/orchestrator.py:174` | `def _run_scout(state, config)` |
| `_run_spec` | function | `skills/claude_md_orchestrator/orchestrator.py:97` | `def _run_spec(state, config)` |
| `_run_test` | function | `skills/claude_md_orchestrator/orchestrator.py:110` | `def _run_test(state, config)` |
| `_seed_state` | function | `skills/claude_md_orchestrator/orchestrator.py:89` | `def _seed_state(contracts, state)` |
| `main` | function | `skills/claude_md_orchestrator/orchestrator.py:393` | `def main(argv)` |
| `run` | function | `skills/claude_md_orchestrator/orchestrator.py:275` | `def run(config, options)` |
| `summary_to_dict` | function | `skills/claude_md_orchestrator/orchestrator.py:306` | `def summary_to_dict(summary)` |
| `_Section` | class | `skills/claude_md_orchestrator/parser.py:34` | `class _Section` |
| `__post_init__` | method | `skills/claude_md_orchestrator/parser.py:51` | `def __post_init__(self)` |
| `_coerce_seed_contract` | function | `skills/claude_md_orchestrator/parser.py:205` | `def _coerce_seed_contract(seed)` |
| `_collect_bullets` | function | `skills/claude_md_orchestrator/parser.py:123` | `def _collect_bullets(text)` |
| `_collect_paragraphs` | function | `skills/claude_md_orchestrator/parser.py:141` | `def _collect_paragraphs(text)` |
| `_derive_contract_id` | function | `skills/claude_md_orchestrator/parser.py:56` | `def _derive_contract_id(title, fallback_index)` |
| `_flatten_actionable` | function | `skills/claude_md_orchestrator/parser.py:159` | `def _flatten_actionable(root)` |
| `_is_actionable` | function | `skills/claude_md_orchestrator/parser.py:146` | `def _is_actionable(heading)` |
| `_strip_contract_marker` | function | `skills/claude_md_orchestrator/parser.py:73` | `def _strip_contract_marker(title)` |
| `_walk_sections` | function | `skills/claude_md_orchestrator/parser.py:85` | `def _walk_sections(lines)` |
| `flush_body` | function | `skills/claude_md_orchestrator/parser.py:97` | `def flush_body()` |
| `load_contracts` | function | `skills/claude_md_orchestrator/parser.py:225` | `def load_contracts(config, seeds)` |
| `parse_claude_md` | function | `skills/claude_md_orchestrator/parser.py:167` | `def parse_claude_md(path)` |
| `AnalyzerResult` | class | `skills/claude_md_orchestrator/reviewer_agent.py:30` | `class AnalyzerResult` |
| `_parse_tool_findings` | function | `skills/claude_md_orchestrator/reviewer_agent.py:88` | `def _parse_tool_findings(result, path_prefix)` |
| `_resolve_targets` | function | `skills/claude_md_orchestrator/reviewer_agent.py:72` | `def _resolve_targets(state, config)` |
| `_run` | function | `skills/claude_md_orchestrator/reviewer_agent.py:46` | `def _run(cmd, cwd)` |
| `_run_bandit` | function | `skills/claude_md_orchestrator/reviewer_agent.py:147` | `def _run_bandit(targets, cwd)` |
| `_run_mypy` | function | `skills/claude_md_orchestrator/reviewer_agent.py:134` | `def _run_mypy(targets, cwd)` |
| `_run_pytest` | function | `skills/claude_md_orchestrator/reviewer_agent.py:160` | `def _run_pytest(targets, cwd)` |
| `_run_ruff` | function | `skills/claude_md_orchestrator/reviewer_agent.py:121` | `def _run_ruff(targets, cwd)` |
| `run` | function | `skills/claude_md_orchestrator/reviewer_agent.py:171` | `def run(state, config)` |
| `write_report` | function | `skills/claude_md_orchestrator/reviewer_agent.py:225` | `def write_report(report, config)` |
| `SddResult` | class | `skills/claude_md_orchestrator/sdd_agent.py:40` | `class SddResult` |
| `_ask_llm` | function | `skills/claude_md_orchestrator/sdd_agent.py:148` | `def _ask_llm(contract, backend)` |
| `_coerce_scope` | function | `skills/claude_md_orchestrator/sdd_agent.py:56` | `def _coerce_scope(scope)` |
| `_compose_spec` | function | `skills/claude_md_orchestrator/sdd_agent.py:81` | `def _compose_spec(contract, min_sad_paths)` |
| `_render_yaml` | function | `skills/claude_md_orchestrator/sdd_agent.py:130` | `def _render_yaml(spec)` |
| `run` | function | `skills/claude_md_orchestrator/sdd_agent.py:204` | `def run(contract, config)` |
| `TddResult` | class | `skills/claude_md_orchestrator/tdd_agent.py:90` | `class TddResult` |
| `_compose_tests` | function | `skills/claude_md_orchestrator/tdd_agent.py:110` | `def _compose_tests(spec, contract)` |
| `_module_name` | function | `skills/claude_md_orchestrator/tdd_agent.py:105` | `def _module_name(contract)` |
| `_run_pytest` | function | `skills/claude_md_orchestrator/tdd_agent.py:154` | `def _run_pytest(test_path, cwd)` |
| `_slug` | function | `skills/claude_md_orchestrator/tdd_agent.py:79` | `def _slug(value)` |
| `read_test_source` | function | `skills/claude_md_orchestrator/tdd_agent.py:228` | `def read_test_source(test_path)` |
| `run` | function | `skills/claude_md_orchestrator/tdd_agent.py:175` | `def run(contract, spec, config)` |
| `config` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:54` | `def config(tmp_run_dir, tmp_path)` |
| `test_bdd_agent_lands_green` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:116` | `def test_bdd_agent_lands_green(config)` |
| `test_boy_scout_returns_report` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:237` | `def test_boy_scout_returns_report(config)` |
| `test_cicd_agent_writes_pipeline` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:260` | `def test_cicd_agent_writes_pipeline(config)` |
| `test_cicd_deploy_gate_checks_secret` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:310` | `def test_cicd_deploy_gate_checks_secret(config)` |
| `test_cicd_deploy_gate_is_timing_safe` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:332` | `def test_cicd_deploy_gate_is_timing_safe()` |
| `test_documentation_agent_emits_fenced_markdown` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:221` | `def test_documentation_agent_emits_fenced_markdown(config)` |
| `test_dod_validators_block_absolute_paths` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:152` | `def test_dod_validators_block_absolute_paths()` |
| `test_dod_validators_block_emoji` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:131` | `def test_dod_validators_block_emoji()` |
| `test_dod_validators_block_inline_comments` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:138` | `def test_dod_validators_block_inline_comments()` |
| `test_dod_validators_block_todo_markers` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:145` | `def test_dod_validators_block_todo_markers()` |
| `test_dod_validators_require_docstrings` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:159` | `def test_dod_validators_require_docstrings()` |
| `test_models_spec_round_trip` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:294` | `def test_models_spec_round_trip()` |
| `test_orchestrator_blocks_on_missing_contracts` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:204` | `def test_orchestrator_blocks_on_missing_contracts(tmp_run_dir, tmp_path)` |
| `test_orchestrator_blocks_on_sad_path_shortage` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:188` | `def test_orchestrator_blocks_on_sad_path_shortage(config)` |
| `test_orchestrator_full_cycle` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:166` | `def test_orchestrator_full_cycle(config)` |
| `test_parser_extracts_contract` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:78` | `def test_parser_extracts_contract(config)` |
| `test_sdd_agent_writes_spec` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:86` | `def test_sdd_agent_writes_spec(config)` |
| `test_tdd_agent_lands_red` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:102` | `def test_tdd_agent_lands_red(config)` |
| `tmp_run_dir` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:46` | `def tmp_run_dir(tmp_path)` |
| `CheckResult` | class | `skills/claude_md_orchestrator/validators.py:96` | `class CheckResult` |
| `_EmojiPattern` | class | `skills/claude_md_orchestrator/validators.py:74` | `class _EmojiPattern` |
| `_EmojiSpan` | class | `skills/claude_md_orchestrator/validators.py:57` | `class _EmojiSpan` |
| `__init__` | method | `skills/claude_md_orchestrator/validators.py:60` | `def __init__(self, start, text)` |
| `blocks` | method | `skills/claude_md_orchestrator/validators.py:111` | `def blocks(self)` |
| `check_docstrings` | function | `skills/claude_md_orchestrator/validators.py:249` | `def check_docstrings(source, path)` |
| `check_english_only` | function | `skills/claude_md_orchestrator/validators.py:225` | `def check_english_only(source, path)` |
| `check_magic_numbers` | function | `skills/claude_md_orchestrator/validators.py:324` | `def check_magic_numbers(source, path, allow)` |
| `check_markdown` | function | `skills/claude_md_orchestrator/validators.py:372` | `def check_markdown(content, path)` |
| `check_no_comments` | function | `skills/claude_md_orchestrator/validators.py:155` | `def check_no_comments(source, path)` |
| `check_no_emoji` | function | `skills/claude_md_orchestrator/validators.py:186` | `def check_no_emoji(content, path)` |
| `check_no_forbidden_markers` | function | `skills/claude_md_orchestrator/validators.py:208` | `def check_no_forbidden_markers(content, path)` |
| `check_no_hardcoded_paths_or_ips` | function | `skills/claude_md_orchestrator/validators.py:290` | `def check_no_hardcoded_paths_or_ips(source, path)` |
| `check_source` | function | `skills/claude_md_orchestrator/validators.py:359` | `def check_source(source, path, allow_numbers)` |
| `check_spec` | function | `skills/claude_md_orchestrator/validators.py:381` | `def check_spec(spec, min_sad_paths)` |
| `find_block_comments` | function | `skills/claude_md_orchestrator/validators.py:116` | `def find_block_comments(source)` |
| `find_inline_comments` | function | `skills/claude_md_orchestrator/validators.py:138` | `def find_inline_comments(source)` |
| `finditer` | method | `skills/claude_md_orchestrator/validators.py:81` | `def finditer(self, content)` |
| `group` | method | `skills/claude_md_orchestrator/validators.py:69` | `def group(self, index)` |
| `passed` | method | `skills/claude_md_orchestrator/validators.py:107` | `def passed(self)` |
| `start` | method | `skills/claude_md_orchestrator/validators.py:65` | `def start(self)` |
| `ControlState` | class | `skills/daemon_control.py:88` | `class ControlState` |
| `DaemonControl` | class | `skills/daemon_control.py:162` | `class DaemonControl` |
| `PendingAction` | class | `skills/daemon_control.py:49` | `class PendingAction` |
| `__init__` | method | `skills/daemon_control.py:171` | `def __init__(self, sessions_dir)` |
| `_first_token` | function | `skills/daemon_control.py:154` | `def _first_token(command)` |
| `add_veto` | method | `skills/daemon_control.py:252` | `def add_veto(self, command_token)` |
| `clear_vetoes` | method | `skills/daemon_control.py:275` | `def clear_vetoes(self)` |
| `consume` | method | `skills/daemon_control.py:343` | `def consume(self, action_id)` |
| `decide` | method | `skills/daemon_control.py:317` | `def decide(self, action_id, decision)` |
| `from_dict` | method | `skills/daemon_control.py:121` | `def from_dict(cls, data)` |
| `is_expired` | method | `skills/daemon_control.py:79` | `def is_expired(self, now)` |
| `is_paused` | method | `skills/daemon_control.py:375` | `def is_paused(self)` |
| `is_vetoed` | method | `skills/daemon_control.py:379` | `def is_vetoed(self, command)` |
| `load` | method | `skills/daemon_control.py:188` | `def load(self)` |
| `path` | method | `skills/daemon_control.py:184` | `def path(self)` |
| `pause` | method | `skills/daemon_control.py:240` | `def pause(self)` |
| `propose` | method | `skills/daemon_control.py:290` | `def propose(self, command)` |
| `remove_veto` | method | `skills/daemon_control.py:267` | `def remove_veto(self, command_token)` |
| `require_approval` | method | `skills/daemon_control.py:248` | `def require_approval(self)` |
| `resume` | method | `skills/daemon_control.py:244` | `def resume(self)` |
| `save` | method | `skills/daemon_control.py:201` | `def save(self, state)` |
| `set_focus` | method | `skills/daemon_control.py:282` | `def set_focus(self, targets)` |
| `set_mode` | method | `skills/daemon_control.py:231` | `def set_mode(self, mode)` |
| `target_in_focus` | method | `skills/daemon_control.py:386` | `def target_in_focus(self, target)` |
| `to_dict` | method | `skills/daemon_control.py:110` | `def to_dict(self)` |
| `wait_for_decision` | function | `skills/daemon_control.py:394` | `def wait_for_decision(control, action)` |
| `wait_until_unpaused` | function | `skills/daemon_control.py:445` | `def wait_until_unpaused(control)` |
| `DaemonHealth` | class | `skills/daemon_health.py:94` | `class DaemonHealth` |
| `__init__` | method | `skills/daemon_health.py:102` | `def __init__(self, interval, health_file)` |
| `_health_path` | function | `skills/daemon_health.py:32` | `def _health_path()` |
| `_loop` | method | `skills/daemon_health.py:147` | `def _loop(self)` |
| `_write_heartbeat` | method | `skills/daemon_health.py:133` | `def _write_heartbeat(self)` |
| `daemon_status` | function | `skills/daemon_health.py:58` | `def daemon_status(timeout)` |
| `error_count` | method | `skills/daemon_health.py:114` | `def error_count(self)` |
| `error_count` | method | `skills/daemon_health.py:119` | `def error_count(self, value)` |
| `increment_cycles` | method | `skills/daemon_health.py:185` | `def increment_cycles(self)` |
| `is_daemon_alive` | function | `skills/daemon_health.py:36` | `def is_daemon_alive(timeout)` |
| `phase` | method | `skills/daemon_health.py:124` | `def phase(self)` |
| `phase` | method | `skills/daemon_health.py:129` | `def phase(self, value)` |
| `record_error` | method | `skills/daemon_health.py:175` | `def record_error(self)` |
| `set_phase` | method | `skills/daemon_health.py:180` | `def set_phase(self, phase)` |
| `start` | method | `skills/daemon_health.py:155` | `def start(self)` |
| `stop` | method | `skills/daemon_health.py:164` | `def stop(self)` |
| `clear_pid` | function | `skills/heartbeat.py:57` | `def clear_pid()` |
| `is_running` | function | `skills/heartbeat.py:62` | `def is_running()` |
| `main` | function | `skills/heartbeat.py:127` | `def main()` |
| `run_loop` | function | `skills/heartbeat.py:74` | `def run_loop(interval, once)` |
| `write_pid` | function | `skills/heartbeat.py:53` | `def write_pid()` |
| `RuleSetBuilder` | class | `skills/hermes-lazyown/claudemd_rules.py:14` | `class RuleSetBuilder` |
| `__init__` | method | `skills/hermes-lazyown/claudemd_rules.py:24` | `def __init__(self)` |
| `_base_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:70` | `def _base_rules(self)` |
| `_credential_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:157` | `def _credential_rules(self)` |
| `_hermes_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:170` | `def _hermes_rules(self)` |
| `_phase_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:82` | `def _phase_rules(self)` |
| `_service_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:138` | `def _service_rules(self)` |
| `build` | method | `skills/hermes-lazyown/claudemd_rules.py:56` | `def build(self)` |
| `generate_rules` | function | `skills/hermes-lazyown/claudemd_rules.py:185` | `def generate_rules(phase, rhost, services, creds_found, is_hermes)` |
| `with_creds` | method | `skills/hermes-lazyown/claudemd_rules.py:46` | `def with_creds(self, found)` |
| `with_hermes` | method | `skills/hermes-lazyown/claudemd_rules.py:51` | `def with_hermes(self, is_hermes)` |
| `with_phase` | method | `skills/hermes-lazyown/claudemd_rules.py:31` | `def with_phase(self, phase)` |
| `with_services` | method | `skills/hermes-lazyown/claudemd_rules.py:41` | `def with_services(self, services)` |
| `with_target` | method | `skills/hermes-lazyown/claudemd_rules.py:36` | `def with_target(self, rhost)` |
| `ConfigBridge` | class | `skills/hermes-lazyown/config_bridge.py:23` | `class ConfigBridge` |
| `ConfigBridgeError` | class | `skills/hermes-lazyown/config_bridge.py:17` | `class ConfigBridgeError(Exception)` |
| `__init__` | method | `skills/hermes-lazyown/config_bridge.py:35` | `def __init__(self, payload_path)` |
| `_from_env` | method | `skills/hermes-lazyown/config_bridge.py:117` | `def _from_env(self, key)` |
| `_from_payload` | method | `skills/hermes-lazyown/config_bridge.py:134` | `def _from_payload(self, key)` |
| `_load_payload` | method | `skills/hermes-lazyown/config_bridge.py:139` | `def _load_payload(self)` |
| `_resolve` | method | `skills/hermes-lazyown/config_bridge.py:105` | `def _resolve(self, key, default)` |
| `active_target` | method | `skills/hermes-lazyown/config_bridge.py:80` | `def active_target(self)` |
| `attacker_context` | method | `skills/hermes-lazyown/config_bridge.py:90` | `def attacker_context(self)` |
| `get` | method | `skills/hermes-lazyown/config_bridge.py:42` | `def get(self, key, default)` |
| `get_bool` | method | `skills/hermes-lazyown/config_bridge.py:66` | `def get_bool(self, key, default)` |
| `get_int` | method | `skills/hermes-lazyown/config_bridge.py:58` | `def get_int(self, key, default)` |
| `get_required` | method | `skills/hermes-lazyown/config_bridge.py:46` | `def get_required(self, key)` |
| `get_str` | method | `skills/hermes-lazyown/config_bridge.py:53` | `def get_str(self, key, default)` |
| `is_hermes_session` | method | `skills/hermes-lazyown/config_bridge.py:99` | `def is_hermes_session(self)` |
| `refresh` | method | `skills/hermes-lazyown/config_bridge.py:75` | `def refresh(self)` |
| `ConfigKeys` | class | `skills/hermes-lazyown/constants.py:12` | `class ConfigKeys` |
| `Defaults` | class | `skills/hermes-lazyown/constants.py:45` | `class Defaults` |
| `EnvKeys` | class | `skills/hermes-lazyown/constants.py:35` | `class EnvKeys` |
| `Paths` | class | `skills/hermes-lazyown/constants.py:102` | `class Paths` |
| `PhaseNames` | class | `skills/hermes-lazyown/constants.py:59` | `class PhaseNames` |
| `claude_md_file` | method | `skills/hermes-lazyown/constants.py:155` | `def claude_md_file()` |
| `lazyown_dir` | method | `skills/hermes-lazyown/constants.py:106` | `def lazyown_dir()` |
| `objectives_file` | method | `skills/hermes-lazyown/constants.py:140` | `def objectives_file()` |
| `payload_file` | method | `skills/hermes-lazyown/constants.py:115` | `def payload_file()` |
| `scan_file` | method | `skills/hermes-lazyown/constants.py:125` | `def scan_file(rhost)` |
| `sessions_dir` | method | `skills/hermes-lazyown/constants.py:120` | `def sessions_dir()` |
| `soul_file` | method | `skills/hermes-lazyown/constants.py:150` | `def soul_file()` |
| `tasks_file` | method | `skills/hermes-lazyown/constants.py:145` | `def tasks_file()` |
| `vulns_file` | method | `skills/hermes-lazyown/constants.py:130` | `def vulns_file(rhost)` |
| `world_model_file` | method | `skills/hermes-lazyown/constants.py:135` | `def world_model_file()` |
| `ExecutionResult` | class | `skills/hermes-lazyown/executor.py:21` | `class ExecutionResult` |
| `LazyOwnExecutor` | class | `skills/hermes-lazyown/executor.py:58` | `class LazyOwnExecutor` |
| `__init__` | method | `skills/hermes-lazyown/executor.py:24` | `def __init__(self, stdout, stderr, returncode, timed_out, duration_ms)` |
| `__init__` | method | `skills/hermes-lazyown/executor.py:66` | `def __init__(self, lazyown_dir, timeout)` |
| `__str__` | method | `skills/hermes-lazyown/executor.py:51` | `def __str__(self)` |
| `_has_pty` | method | `skills/hermes-lazyown/executor.py:229` | `def _has_pty(self)` |
| `_run_via_subprocess` | method | `skills/hermes-lazyown/executor.py:114` | `def _run_via_subprocess(self, command, timeout)` |
| `_run_with_pty` | method | `skills/hermes-lazyown/executor.py:177` | `def _run_with_pty(self, argv, command, timeout, env)` |
| `_run_without_pty` | method | `skills/hermes-lazyown/executor.py:149` | `def _run_without_pty(self, argv, command, timeout, env)` |
| `combined` | method | `skills/hermes-lazyown/executor.py:39` | `def combined(self)` |
| `execute` | method | `skills/hermes-lazyown/executor.py:77` | `def execute(self, command, timeout)` |
| `execute_batch` | method | `skills/hermes-lazyown/executor.py:98` | `def execute_batch(self, commands, timeout)` |
| `success` | method | `skills/hermes-lazyown/executor.py:47` | `def success(self)` |
| `CheckpointSerializer` | class | `skills/hermes-lazyown/hermes_sync.py:27` | `class CheckpointSerializer` |
| `DelegationPlanner` | class | `skills/hermes-lazyown/hermes_sync.py:145` | `class DelegationPlanner` |
| `HermesSyncError` | class | `skills/hermes-lazyown/hermes_sync.py:21` | `class HermesSyncError(Exception)` |
| `ObjectiveTodoSync` | class | `skills/hermes-lazyown/hermes_sync.py:73` | `class ObjectiveTodoSync` |
| `__init__` | method | `skills/hermes-lazyown/hermes_sync.py:33` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `skills/hermes-lazyown/hermes_sync.py:82` | `def __init__(self, objectives_path)` |
| `clear` | method | `skills/hermes-lazyown/hermes_sync.py:64` | `def clear(self)` |
| `inject_objective` | method | `skills/hermes-lazyown/hermes_sync.py:127` | `def inject_objective(self, text, priority, notes)` |
| `mark_done` | method | `skills/hermes-lazyown/hermes_sync.py:106` | `def mark_done(self, objective_text)` |
| `pending_objectives` | method | `skills/hermes-lazyown/hermes_sync.py:85` | `def pending_objectives(self)` |
| `plan_for_credential` | method | `skills/hermes-lazyown/hermes_sync.py:233` | `def plan_for_credential(self, cred_type, value, rhost)` |
| `plan_for_service` | method | `skills/hermes-lazyown/hermes_sync.py:154` | `def plan_for_service(self, service, port, rhost)` |
| `read` | method | `skills/hermes-lazyown/hermes_sync.py:49` | `def read(self)` |
| `write` | method | `skills/hermes-lazyown/hermes_sync.py:37` | `def write(self, state)` |
| `_auto_inject_objective` | function | `skills/hermes-lazyown/mcp_server.py:611` | `def _auto_inject_objective(arguments)` |
| `_auto_loop` | function | `skills/hermes-lazyown/mcp_server.py:591` | `def _auto_loop(arguments)` |
| `_c2_get_beacons` | function | `skills/hermes-lazyown/mcp_server.py:727` | `def _c2_get_beacons()` |
| `_c2_status` | function | `skills/hermes-lazyown/mcp_server.py:706` | `def _c2_status()` |
| `_compact` | function | `skills/hermes-lazyown/mcp_server.py:92` | `def _compact(result, phase, tool_name)` |
| `_core_command_help` | function | `skills/hermes-lazyown/mcp_server.py:480` | `def _core_command_help(arguments)` |
| `_core_run_command` | function | `skills/hermes-lazyown/mcp_server.py:464` | `def _core_run_command(arguments)` |
| `_core_session_init` | function | `skills/hermes-lazyown/mcp_server.py:395` | `def _core_session_init(arguments)` |
| `_core_set_config` | function | `skills/hermes-lazyown/mcp_server.py:441` | `def _core_set_config(arguments)` |
| `_desc` | function | `skills/hermes-lazyown/mcp_server.py:120` | `def _desc(base)` |
| `_get_checkpoint_serializer` | function | `skills/hermes-lazyown/mcp_server.py:68` | `def _get_checkpoint_serializer()` |
| `_get_compactor` | function | `skills/hermes-lazyown/mcp_server.py:52` | `def _get_compactor()` |

Next: [SYMBOLS_p24.md](SYMBOLS_p24.md)
