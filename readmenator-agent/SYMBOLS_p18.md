# Symbols (page 18 of 35)
Previous: [SYMBOLS_p17.md](SYMBOLS_p17.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `__init__` | method | `skills/aci_planner.py:438` | `def __init__(self, api_key, objectives_file, plan_file)` |
| `__init__` | method | `skills/aci_planner.py:581` | `def __init__(self, api_key, plan_file, objectives_file, history_file, replan_threshold)` |
| `__init__` | method | `skills/aci_planner.py:774` | `def __init__(self, lessons_file)` |
| `_archive_plan` | method | `skills/aci_planner.py:239` | `def _archive_plan(plan, history_file)` |
| `_build_parser` | method | `skills/aci_planner.py:955` | `def _build_parser()` |
| `_build_phases_from_llm` | method | `skills/aci_planner.py:486` | `def _build_phases_from_llm(self, raw, goal, phase_filter)` |
| `_build_phases_static` | method | `skills/aci_planner.py:511` | `def _build_phases_static(self, goal, phase_filter)` |
| `_count_blocked` | method | `skills/aci_planner.py:750` | `def _count_blocked(self, plan)` |
| `_count_objectives_by_status` | method | `skills/aci_planner.py:266` | `def _count_objectives_by_status(obj_ids, objectives_file)` |
| `_inject_all_objectives` | method | `skills/aci_planner.py:539` | `def _inject_all_objectives(self, plan)` |
| `_llm_decompose` | method | `skills/aci_planner.py:316` | `def _llm_decompose(goal, api_key)` |
| `_llm_replan` | method | `skills/aci_planner.py:379` | `def _llm_replan(plan, reason, api_key)` |
| `_load_payload` | method | `skills/aci_planner.py:248` | `def _load_payload()` |
| `_load_plan` | method | `skills/aci_planner.py:226` | `def _load_plan(plan_file)` |
| `_load_world_model` | method | `skills/aci_planner.py:257` | `def _load_world_model()` |
| `_now_iso` | method | `skills/aci_planner.py:212` | `def _now_iso()` |
| `_persist_lessons` | method | `skills/aci_planner.py:829` | `def _persist_lessons(self, lessons)` |
| `_save_plan` | method | `skills/aci_planner.py:216` | `def _save_plan(plan, plan_file)` |
| `_sync_phase_statuses` | method | `skills/aci_planner.py:731` | `def _sync_phase_statuses(self, plan)` |
| `_write_objective` | method | `skills/aci_planner.py:548` | `def _write_objective(self, text, phase, target)` |
| `active_phase` | method | `skills/aci_planner.py:179` | `def active_phase(self)` |
| `complete` | method | `skills/aci_planner.py:718` | `def complete(self)` |
| `completion_pct` | method | `skills/aci_planner.py:187` | `def completion_pct(self)` |
| `from_dict` | method | `skills/aci_planner.py:156` | `def from_dict(cls, d)` |
| `from_dict` | method | `skills/aci_planner.py:201` | `def from_dict(cls, d)` |
| `main` | method | `skills/aci_planner.py:980` | `def main(argv)` |
| `mcp_aci_plan` | method | `skills/aci_planner.py:842` | `def mcp_aci_plan(goal, target, scope, domain, os_hint, phase_filter)` |
| `mcp_aci_replan` | method | `skills/aci_planner.py:920` | `def mcp_aci_replan(reason)` |
| `mcp_aci_status` | method | `skills/aci_planner.py:903` | `def mcp_aci_status()` |
| `plan` | method | `skills/aci_planner.py:448` | `def plan(self, goal, phase_filter)` |
| `reflect` | method | `skills/aci_planner.py:777` | `def reflect(self, plan)` |
| `replan` | method | `skills/aci_planner.py:648` | `def replan(self, reason)` |
| `should_replan` | method | `skills/aci_planner.py:635` | `def should_replan(self, plan)` |
| `status` | method | `skills/aci_planner.py:595` | `def status(self)` |
| `to_dict` | method | `skills/aci_planner.py:151` | `def to_dict(self)` |
| `to_dict` | method | `skills/aci_planner.py:194` | `def to_dict(self)` |
| `BridgeFallbackResolver` | class | `skills/autonomous_daemon.py:2417` | `class BridgeFallbackResolver(IToolFallbackResolver)` |
| `BridgeSelector` | class | `skills/autonomous_daemon.py:626` | `class BridgeSelector(ICommandSelector)` |
| `CascadeStrategy` | class | `skills/autonomous_daemon.py:1158` | `class CascadeStrategy` |
| `CommandDecision` | class | `skills/autonomous_daemon.py:511` | `class CommandDecision` |
| `CommandRunnerChain` | class | `skills/autonomous_daemon.py:420` | `class CommandRunnerChain(ICommandRunner)` |
| `CredentialSpraySelector` | class | `skills/autonomous_daemon.py:1102` | `class CredentialSpraySelector(ICommandSelector)` |
| `DroneCoordinator` | class | `skills/autonomous_daemon.py:2170` | `class DroneCoordinator` |
| `EngageOrchestrator` | class | `skills/autonomous_daemon.py:2550` | `class EngageOrchestrator` |
| `EnginePhaseResult` | class | `skills/autonomous_daemon.py:2367` | `class EnginePhaseResult` |
| `EnginePhaseStep` | class | `skills/autonomous_daemon.py:2350` | `class EnginePhaseStep` |
| `ExecutionEngine` | class | `skills/autonomous_daemon.py:1290` | `class ExecutionEngine(IObjectiveHandler)` |
| `FallbackSelector` | class | `skills/autonomous_daemon.py:842` | `class FallbackSelector(ICommandSelector)` |
| `ICommandRunner` | class | `skills/autonomous_daemon.py:305` | `class ICommandRunner(ABC)` |
| `ICommandSelector` | class | `skills/autonomous_daemon.py:521` | `class ICommandSelector(ABC)` |
| `IObjectiveHandler` | class | `skills/autonomous_daemon.py:1276` | `class IObjectiveHandler(ABC)` |
| `IToolFallbackResolver` | class | `skills/autonomous_daemon.py:2383` | `class IToolFallbackResolver(ABC)` |
| `LLMSelector` | class | `skills/autonomous_daemon.py:692` | `class LLMSelector(ICommandSelector)` |
| `MCPCommandRunner` | class | `skills/autonomous_daemon.py:318` | `class MCPCommandRunner(ICommandRunner)` |
| `MetricsAwareSelector` | class | `skills/autonomous_daemon.py:868` | `class MetricsAwareSelector(ICommandSelector)` |
| `PTYCommandRunner` | class | `skills/autonomous_daemon.py:334` | `class PTYCommandRunner(ICommandRunner)` |
| `ParquetSelector` | class | `skills/autonomous_daemon.py:578` | `class ParquetSelector(ICommandSelector)` |
| `ReactiveSelector` | class | `skills/autonomous_daemon.py:534` | `class ReactiveSelector(ICommandSelector)` |
| `SWANSelector` | class | `skills/autonomous_daemon.py:765` | `class SWANSelector(ICommandSelector)` |
| `StaticFallbackResolver` | class | `skills/autonomous_daemon.py:2396` | `class StaticFallbackResolver(IToolFallbackResolver)` |
| `StepResult` | class | `skills/autonomous_daemon.py:1265` | `class StepResult` |
| `StrategyEngine` | class | `skills/autonomous_daemon.py:1189` | `class StrategyEngine` |
| `_ShellDetector` | class | `skills/autonomous_daemon.py:2467` | `class _ShellDetector` |
| `__init__` | method | `skills/autonomous_daemon.py:429` | `def __init__(self, runners)` |
| `__init__` | method | `skills/autonomous_daemon.py:540` | `def __init__(self, reactive_engine)` |
| `__init__` | method | `skills/autonomous_daemon.py:584` | `def __init__(self, pdb, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:632` | `def __init__(self, dispatcher, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:889` | `def __init__(self, wrapped, metrics_source, min_success_rate, min_attempts, window_seconds, cache_ttl_s, clock)` |
| `__init__` | method | `skills/autonomous_daemon.py:1125` | `def __init__(self, fail_counts)` |
| `__init__` | method | `skills/autonomous_daemon.py:1165` | `def __init__(self, selectors)` |
| `__init__` | method | `skills/autonomous_daemon.py:1203` | `def __init__(self, runner, selectors)` |
| `__init__` | method | `skills/autonomous_daemon.py:1302` | `def __init__(self, strategy, max_steps, world_model, obs_parser, facts, loop)` |
| `__init__` | method | `skills/autonomous_daemon.py:2179` | `def __init__(self)` |
| `__init__` | method | `skills/autonomous_daemon.py:2426` | `def __init__(self, dispatcher)` |
| `__init__` | method | `skills/autonomous_daemon.py:2480` | `def __init__(self, narrator)` |
| `__init__` | method | `skills/autonomous_daemon.py:2564` | `def __init__(self, target, runner, narrator, approval_gate, fallback_resolver, shell_detector, plan...` |
| `_bridge_candidate` | method | `skills/autonomous_daemon.py:647` | `def _bridge_candidate(self, phase, services, tag, os_hint)` |
| `_build_default_runner` | method | `skills/autonomous_daemon.py:450` | `def _build_default_runner()` |
| `_candidates` | method | `skills/autonomous_daemon.py:2433` | `def _candidates(self, primary, phase)` |
| `_clear_pid` | method | `skills/autonomous_daemon.py:3475` | `def _clear_pid()` |
| `_compute_step_reward` | method | `skills/autonomous_daemon.py:1467` | `def _compute_step_reward(output, command, phase, success, findings, prev_cmds)` |
| `_consult_gate` | method | `skills/autonomous_daemon.py:2810` | `def _consult_gate(self, step)` |
| `_current_summary` | method | `skills/autonomous_daemon.py:969` | `def _current_summary(self)` |
| `_detect_target_os` | method | `skills/autonomous_daemon.py:1540` | `def _detect_target_os(target, loop)` |
| `_dispatch_pipeline` | method | `skills/autonomous_daemon.py:3729` | `def _dispatch_pipeline(args)` |
| `_emit` | function | `skills/autonomous_daemon.py:255` | `def _emit(event_type, payload, severity)` |
| `_engage_run_sync` | method | `skills/autonomous_daemon.py:2877` | `def _engage_run_sync(target, max_switches_per_step, auto)` |
| `_execute` | method | `skills/autonomous_daemon.py:2825` | `def _execute(self, command, timeout_s)` |
| `_get_campaign_blacklist` | method | `skills/autonomous_daemon.py:1457` | `def _get_campaign_blacklist()` |
| `_get_phase_command_catalog` | method | `skills/autonomous_daemon.py:673` | `def _get_phase_command_catalog(phase)` |
| `_inject_to_tasks_json` | function | `skills/autonomous_daemon.py:214` | `def _inject_to_tasks_json(title, description, operator, status)` |
| `_is_running` | method | `skills/autonomous_daemon.py:3487` | `def _is_running()` |
| `_llm_candidate` | method | `skills/autonomous_daemon.py:705` | `def _llm_candidate(self, target, phase, context)` |
| `_load_campaign_blacklist` | method | `skills/autonomous_daemon.py:1427` | `def _load_campaign_blacklist()` |
| `_load_payload` | method | `skills/autonomous_daemon.py:1398` | `def _load_payload()` |
| `_main_async` | method | `skills/autonomous_daemon.py:3417` | `def _main_async(max_steps)` |
| `_maybe_generate_report` | method | `skills/autonomous_daemon.py:2851` | `def _maybe_generate_report()` |
| `_parquet_candidate` | method | `skills/autonomous_daemon.py:601` | `def _parquet_candidate(self, category, target)` |
| `_read_pid` | method | `skills/autonomous_daemon.py:3480` | `def _read_pid()` |
| `_read_recent_csv_commands` | method | `skills/autonomous_daemon.py:1406` | `def _read_recent_csv_commands(limit)` |
| `_resolve_source` | method | `skills/autonomous_daemon.py:942` | `def _resolve_source(self)` |
| `_run` | method | `skills/autonomous_daemon.py:3610` | `def _run()` |
| `_run_lazyown` | method | `skills/autonomous_daemon.py:459` | `def _run_lazyown(command, timeout)` |
| `_run_objective` | method | `skills/autonomous_daemon.py:1587` | `def _run_objective(objective_id, objective_text, target, max_steps, strategy, world_model, obs_parser, facts, loop)` |
| `_run_step` | method | `skills/autonomous_daemon.py:2679` | `def _run_step(self, step)` |
| `_run_sync` | method | `skills/autonomous_daemon.py:1348` | `def _run_sync(self, objective_id, objective_text, target)` |
| `_should_skip` | method | `skills/autonomous_daemon.py:1003` | `def _should_skip(self, command)` |
| `_step_succeeded` | method | `skills/autonomous_daemon.py:2831` | `def _step_succeeded(command, output)` |
| `_swan_candidate` | method | `skills/autonomous_daemon.py:802` | `def _swan_candidate(self, target, phase, context)` |
| `_try_import` | function | `skills/autonomous_daemon.py:133` | `def _try_import(module, attr)` |
| `_update_task_status` | function | `skills/autonomous_daemon.py:191` | `def _update_task_status(title, new_status)` |
| `_worker` | method | `skills/autonomous_daemon.py:2969` | `def _worker()` |
| `_wrap_chain_with_metrics_bias` | method | `skills/autonomous_daemon.py:1064` | `def _wrap_chain_with_metrics_bias(selectors, enabled)` |
| `_write_pid` | method | `skills/autonomous_daemon.py:3470` | `def _write_pid()` |
| `_write_status` | method | `skills/autonomous_daemon.py:3082` | `def _write_status()` |
| `cmd_engage` | method | `skills/autonomous_daemon.py:3054` | `def cmd_engage(target, max_switches_per_step, detach)` |
| `cmd_inject` | method | `skills/autonomous_daemon.py:3570` | `def cmd_inject(text, priority)` |
| `cmd_run` | method | `skills/autonomous_daemon.py:3498` | `def cmd_run(max_steps)` |
| `cmd_start` | method | `skills/autonomous_daemon.py:3507` | `def cmd_start(max_steps)` |
| `cmd_status` | method | `skills/autonomous_daemon.py:3554` | `def cmd_status()` |
| `cmd_stop` | method | `skills/autonomous_daemon.py:3537` | `def cmd_stop()` |
| `compute_decision_seed` | function | `skills/autonomous_daemon.py:278` | `def compute_decision_seed(objective_id, step_n, source)` |
| `detect_in_output` | method | `skills/autonomous_daemon.py:2525` | `def detect_in_output(self, output, target)` |
| `did_switch` | method | `skills/autonomous_daemon.py:2378` | `def did_switch(self)` |
| `engagement_id` | method | `skills/autonomous_daemon.py:2599` | `def engagement_id(self)` |
| `handle` | method | `skills/autonomous_daemon.py:1280` | `def handle(self, objective_id, objective_text, target, context)` |
| `handle` | method | `skills/autonomous_daemon.py:1318` | `def handle(self, objective_id, objective_text, target, context)` |
| `heartbeat_loop` | method | `skills/autonomous_daemon.py:3379` | `def heartbeat_loop()` |
| `mcp_autonomous_events` | method | `skills/autonomous_daemon.py:3699` | `def mcp_autonomous_events(last_n)` |
| `mcp_autonomous_inject` | method | `skills/autonomous_daemon.py:3664` | `def mcp_autonomous_inject(text, priority, target)` |
| `mcp_autonomous_start` | method | `skills/autonomous_daemon.py:3595` | `def mcp_autonomous_start(max_steps, backend)` |
| `mcp_autonomous_status` | method | `skills/autonomous_daemon.py:3651` | `def mcp_autonomous_status()` |
| `mcp_autonomous_stop` | method | `skills/autonomous_daemon.py:3635` | `def mcp_autonomous_stop()` |
| `mcp_engage_approve` | method | `skills/autonomous_daemon.py:3020` | `def mcp_engage_approve(approval_id, decision, operator)` |
| `mcp_engage_list_pending` | method | `skills/autonomous_daemon.py:3040` | `def mcp_engage_list_pending()` |
| `mcp_engage_status` | method | `skills/autonomous_daemon.py:2998` | `def mcp_engage_status(last_n)` |
| `mcp_engage_target` | method | `skills/autonomous_daemon.py:2920` | `def mcp_engage_target(target, max_switches_per_step, detach, auto)` |
| `name` | method | `skills/autonomous_daemon.py:314` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:325` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:342` | `def name(self)` |
| `name` | method | `skills/autonomous_daemon.py:435` | `def name(self)` |
| `next_command` | method | `skills/autonomous_daemon.py:1168` | `def next_command(self, target, phase, context)` |
| `next_command` | method | `skills/autonomous_daemon.py:1246` | `def next_command(self, target, phase, services, os_hint)` |
| `next_tool` | method | `skills/autonomous_daemon.py:2387` | `def next_tool(self, failed_command, phase, attempt)` |
| `next_tool` | method | `skills/autonomous_daemon.py:2404` | `def next_tool(self, failed_command, phase, attempt)` |
| `next_tool` | method | `skills/autonomous_daemon.py:2453` | `def next_tool(self, failed_command, phase, attempt)` |
| `objective_loop` | method | `skills/autonomous_daemon.py:3094` | `def objective_loop(max_steps, loop)` |
| `poll` | method | `skills/autonomous_daemon.py:2485` | `def poll(self, target)` |
| `process_findings` | method | `skills/autonomous_daemon.py:2184` | `def process_findings(self, findings, target, objective_id, payload_key)` |
| `register_output` | method | `skills/autonomous_daemon.py:544` | `def register_output(self, output, command, platform)` |
| `register_output` | method | `skills/autonomous_daemon.py:1232` | `def register_output(self, output, command, platform, success)` |
| `run` | method | `skills/autonomous_daemon.py:309` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:328` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:345` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:438` | `def run(self, command, timeout)` |
| `run` | method | `skills/autonomous_daemon.py:2603` | `def run(self)` |
| `run_async` | method | `skills/autonomous_daemon.py:1328` | `def run_async(self, objective_id, objective_text, target)` |
| `select` | method | `skills/autonomous_daemon.py:525` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:569` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:588` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:636` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:699` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:796` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:849` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:1027` | `def select(self, target, phase, context)` |
| `select` | method | `skills/autonomous_daemon.py:1129` | `def select(self, target, phase, context)` |
| `world_model_watcher` | method | `skills/autonomous_daemon.py:3219` | `def world_model_watcher(loop)` |
| `wrapped` | method | `skills/autonomous_daemon.py:937` | `def wrapped(self)` |
| `EventLogReader` | class | `skills/autonomous_replay.py:127` | `class EventLogReader` |
| `ReplayDispatcher` | class | `skills/autonomous_replay.py:212` | `class ReplayDispatcher` |
| `ReplayDivergence` | class | `skills/autonomous_replay.py:82` | `class ReplayDivergence` |
| `ReplayReport` | class | `skills/autonomous_replay.py:93` | `class ReplayReport` |
| `ReplayStep` | class | `skills/autonomous_replay.py:53` | `class ReplayStep` |
| `__init__` | method | `skills/autonomous_replay.py:136` | `def __init__(self, path)` |
| `__init__` | method | `skills/autonomous_replay.py:221` | `def __init__(self, reader, seed_fn)` |
| `_build_step` | method | `skills/autonomous_replay.py:281` | `def _build_step(self, event, divergences)` |
| `_collect_step_events` | method | `skills/autonomous_replay.py:261` | `def _collect_step_events(self, from_event_id, to_event_id)` |
| `_default_runner` | method | `skills/autonomous_replay.py:432` | `def _default_runner()` |
| `_default_seed_fn` | method | `skills/autonomous_replay.py:241` | `def _default_seed_fn()` |
| `_invoke_runner` | method | `skills/autonomous_replay.py:460` | `def _invoke_runner(runner, command, timeout)` |
| `execute` | method | `skills/autonomous_replay.py:372` | `def execute(self, from_event_id, to_event_id, runner, timeout)` |
| `path` | method | `skills/autonomous_replay.py:147` | `def path(self)` |
| `read` | method | `skills/autonomous_replay.py:152` | `def read(self)` |
| `replay` | method | `skills/autonomous_replay.py:492` | `def replay(from_event_id, to_event_id, mode, events_path, runner, timeout)` |
| `slice` | method | `skills/autonomous_replay.py:177` | `def slice(self, events, from_event_id, to_event_id)` |
| `to_dict` | method | `skills/autonomous_replay.py:114` | `def to_dict(self)` |
| `trace` | method | `skills/autonomous_replay.py:338` | `def trace(self, from_event_id, to_event_id)` |
| `BddResult` | class | `skills/claude_md_orchestrator/bdd_agent.py:116` | `class BddResult` |
| `_compose_implementation` | function | `skills/claude_md_orchestrator/bdd_agent.py:95` | `def _compose_implementation(spec, contract)` |
| `_ensure_init` | method | `skills/claude_md_orchestrator/bdd_agent.py:133` | `def _ensure_init(config)` |
| `_module_name` | function | `skills/claude_md_orchestrator/bdd_agent.py:80` | `def _module_name(contract)` |
| `_module_path` | function | `skills/claude_md_orchestrator/bdd_agent.py:85` | `def _module_path(contract, config)` |
| `_package_init` | function | `skills/claude_md_orchestrator/bdd_agent.py:90` | `def _package_init(config)` |
| `_run_pytest` | method | `skills/claude_md_orchestrator/bdd_agent.py:141` | `def _run_pytest(test_path, cwd)` |
| `run` | method | `skills/claude_md_orchestrator/bdd_agent.py:154` | `def run(contract, spec, suite, config)` |
| `ScoutReport` | class | `skills/claude_md_orchestrator/boy_scout.py:30` | `class ScoutReport` |
| `_inspect` | method | `skills/claude_md_orchestrator/boy_scout.py:45` | `def _inspect(path)` |
| `_render_proposal` | method | `skills/claude_md_orchestrator/boy_scout.py:73` | `def _render_proposal(contract, findings)` |
| `run` | method | `skills/claude_md_orchestrator/boy_scout.py:90` | `def run(state, config)` |
| `write_report` | method | `skills/claude_md_orchestrator/boy_scout.py:110` | `def write_report(report, config)` |
| `CicdResult` | class | `skills/claude_md_orchestrator/cicd_agent.py:70` | `class CicdResult` |
| `_ensure_branch` | method | `skills/claude_md_orchestrator/cicd_agent.py:107` | `def _ensure_branch(contract, config)` |
| `_git` | method | `skills/claude_md_orchestrator/cicd_agent.py:96` | `def _git()` |
| `_render_pipeline` | method | `skills/claude_md_orchestrator/cicd_agent.py:133` | `def _render_pipeline(contract, spec, config)` |
| `_render_pr_body` | method | `skills/claude_md_orchestrator/cicd_agent.py:143` | `def _render_pr_body(contract, spec, report)` |
| `_slug` | method | `skills/claude_md_orchestrator/cicd_agent.py:90` | `def _slug(contract)` |
| `run` | method | `skills/claude_md_orchestrator/cicd_agent.py:176` | `def run(contract, spec, report, config)` |
| `Config` | class | `skills/claude_md_orchestrator/config.py:67` | `class Config` |
| `_default_claude_md` | function | `skills/claude_md_orchestrator/config.py:52` | `def _default_claude_md()` |
| `_default_run_dir` | function | `skills/claude_md_orchestrator/config.py:37` | `def _default_run_dir()` |
| `_repo_root` | function | `skills/claude_md_orchestrator/config.py:22` | `def _repo_root()` |
| `docs_dir` | method | `skills/claude_md_orchestrator/config.py:144` | `def docs_dir(self)` |
| `ensure` | method | `skills/claude_md_orchestrator/config.py:114` | `def ensure(self)` |
| `load_config` | method | `skills/claude_md_orchestrator/config.py:157` | `def load_config()` |
| `log_path` | method | `skills/claude_md_orchestrator/config.py:152` | `def log_path(self)` |
| `logs_dir` | method | `skills/claude_md_orchestrator/config.py:148` | `def logs_dir(self)` |
| `resolve_optional` | method | `skills/claude_md_orchestrator/config.py:166` | `def resolve_optional(config, key)` |
| `review_dir` | method | `skills/claude_md_orchestrator/config.py:140` | `def review_dir(self)` |
| `specs_dir` | method | `skills/claude_md_orchestrator/config.py:128` | `def specs_dir(self)` |
| `src_dir` | method | `skills/claude_md_orchestrator/config.py:136` | `def src_dir(self)` |
| `state_path` | method | `skills/claude_md_orchestrator/config.py:124` | `def state_path(self)` |
| `tests_dir` | method | `skills/claude_md_orchestrator/config.py:132` | `def tests_dir(self)` |
| `DocResult` | class | `skills/claude_md_orchestrator/documentation_agent.py:28` | `class DocResult` |
| `_format_inputs` | method | `skills/claude_md_orchestrator/documentation_agent.py:40` | `def _format_inputs(spec)` |
| `_format_review` | method | `skills/claude_md_orchestrator/documentation_agent.py:57` | `def _format_review(report)` |
| `_format_sad_paths` | method | `skills/claude_md_orchestrator/documentation_agent.py:47` | `def _format_sad_paths(spec)` |
| `_render` | method | `skills/claude_md_orchestrator/documentation_agent.py:71` | `def _render(contract, spec, report)` |
| `_wrap` | method | `skills/claude_md_orchestrator/documentation_agent.py:121` | `def _wrap(body)` |
| `run` | method | `skills/claude_md_orchestrator/documentation_agent.py:126` | `def run(contract, spec, report, config)` |
| `CicleState` | class | `skills/claude_md_orchestrator/models.py:350` | `class CicleState` |
| `CicleStateFile` | class | `skills/claude_md_orchestrator/models.py:426` | `class CicleStateFile` |
| `Contract` | class | `skills/claude_md_orchestrator/models.py:68` | `class Contract` |
| `Finding` | class | `skills/claude_md_orchestrator/models.py:257` | `class Finding` |
| `ReviewReport` | class | `skills/claude_md_orchestrator/models.py:293` | `class ReviewReport` |
| `SadPath` | class | `skills/claude_md_orchestrator/models.py:109` | `class SadPath` |
| `Severity` | class | `skills/claude_md_orchestrator/models.py:50` | `class Severity(StrEnum)` |
| `Spec` | class | `skills/claude_md_orchestrator/models.py:134` | `class Spec` |
| `Stage` | class | `skills/claude_md_orchestrator/models.py:28` | `class Stage(StrEnum)` |
| `TestSuite` | class | `skills/claude_md_orchestrator/models.py:219` | `class TestSuite` |
| `_now_iso` | function | `skills/claude_md_orchestrator/models.py:19` | `def _now_iso()` |
| `blockers` | method | `skills/claude_md_orchestrator/models.py:317` | `def blockers(self)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:96` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:125` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:173` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:245` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:282` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:335` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:404` | `def from_dict(cls, data)` |
| `from_dict` | method | `skills/claude_md_orchestrator/models.py:452` | `def from_dict(cls, data)` |
| `load` | method | `skills/claude_md_orchestrator/models.py:472` | `def load(cls, path)` |
| `save` | method | `skills/claude_md_orchestrator/models.py:464` | `def save(self, path)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:91` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:120` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:166` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:238` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:272` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:321` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:385` | `def to_dict(self)` |
| `to_dict` | method | `skills/claude_md_orchestrator/models.py:442` | `def to_dict(self)` |
| `validate` | method | `skills/claude_md_orchestrator/models.py:189` | `def validate(self, min_sad_paths)` |
| `write_jsonl` | method | `skills/claude_md_orchestrator/models.py:485` | `def write_jsonl(path, event)` |
| `CycleSummary` | class | `skills/claude_md_orchestrator/orchestrator.py:34` | `class CycleSummary` |
| `_advance` | method | `skills/claude_md_orchestrator/orchestrator.py:257` | `def _advance(state, contract_id, config, options)` |
| `_banner` | method | `skills/claude_md_orchestrator/orchestrator.py:52` | `def _banner(message, config)` |
| `_build_parser` | method | `skills/claude_md_orchestrator/orchestrator.py:347` | `def _build_parser()` |
| `_halt` | method | `skills/claude_md_orchestrator/orchestrator.py:59` | `def _halt(summary, contract_id, reason)` |
| `_load_seed_contracts` | method | `skills/claude_md_orchestrator/orchestrator.py:388` | `def _load_seed_contracts(args, options)` |
| `_load_spec` | method | `skills/claude_md_orchestrator/orchestrator.py:240` | `def _load_spec(path)` |
| `_load_state` | method | `skills/claude_md_orchestrator/orchestrator.py:90` | `def _load_state(config)` |
| `_persist` | method | `skills/claude_md_orchestrator/orchestrator.py:66` | `def _persist(state, config)` |
| `_print_summary` | method | `skills/claude_md_orchestrator/orchestrator.py:324` | `def _print_summary(summary)` |
| `_run_cicd` | method | `skills/claude_md_orchestrator/orchestrator.py:200` | `def _run_cicd(state, config)` |
| `_run_documentation` | method | `skills/claude_md_orchestrator/orchestrator.py:174` | `def _run_documentation(state, config)` |
| `_run_implementation` | method | `skills/claude_md_orchestrator/orchestrator.py:136` | `def _run_implementation(state, config)` |
| `_run_review` | method | `skills/claude_md_orchestrator/orchestrator.py:159` | `def _run_review(state, config)` |
| `_run_scout` | method | `skills/claude_md_orchestrator/orchestrator.py:192` | `def _run_scout(state, config)` |
| `_run_spec` | method | `skills/claude_md_orchestrator/orchestrator.py:103` | `def _run_spec(state, config)` |
| `_run_test` | method | `skills/claude_md_orchestrator/orchestrator.py:119` | `def _run_test(state, config)` |
| `_seed_state` | method | `skills/claude_md_orchestrator/orchestrator.py:95` | `def _seed_state(contracts, state)` |
| `main` | method | `skills/claude_md_orchestrator/orchestrator.py:416` | `def main(argv)` |
| `run` | method | `skills/claude_md_orchestrator/orchestrator.py:298` | `def run(config, options)` |
| `summary_to_dict` | method | `skills/claude_md_orchestrator/orchestrator.py:329` | `def summary_to_dict(summary)` |
| `_Section` | class | `skills/claude_md_orchestrator/parser.py:36` | `class _Section` |
| `__post_init__` | method | `skills/claude_md_orchestrator/parser.py:53` | `def __post_init__(self)` |
| `_coerce_seed_contract` | method | `skills/claude_md_orchestrator/parser.py:209` | `def _coerce_seed_contract(seed)` |
| `_collect_bullets` | method | `skills/claude_md_orchestrator/parser.py:125` | `def _collect_bullets(text)` |
| `_collect_paragraphs` | method | `skills/claude_md_orchestrator/parser.py:143` | `def _collect_paragraphs(text)` |
| `_derive_contract_id` | method | `skills/claude_md_orchestrator/parser.py:58` | `def _derive_contract_id(title, fallback_index)` |
| `_flatten_actionable` | method | `skills/claude_md_orchestrator/parser.py:163` | `def _flatten_actionable(root)` |
| `_is_actionable` | method | `skills/claude_md_orchestrator/parser.py:148` | `def _is_actionable(heading)` |
| `_strip_contract_marker` | method | `skills/claude_md_orchestrator/parser.py:75` | `def _strip_contract_marker(title)` |
| `_walk_sections` | method | `skills/claude_md_orchestrator/parser.py:87` | `def _walk_sections(lines)` |
| `flush_body` | method | `skills/claude_md_orchestrator/parser.py:99` | `def flush_body()` |
| `load_contracts` | method | `skills/claude_md_orchestrator/parser.py:229` | `def load_contracts(config, seeds)` |
| `parse_claude_md` | method | `skills/claude_md_orchestrator/parser.py:171` | `def parse_claude_md(path)` |
| `AnalyzerResult` | class | `skills/claude_md_orchestrator/reviewer_agent.py:30` | `class AnalyzerResult` |
| `_parse_tool_findings` | method | `skills/claude_md_orchestrator/reviewer_agent.py:88` | `def _parse_tool_findings(result, path_prefix)` |
| `_resolve_targets` | method | `skills/claude_md_orchestrator/reviewer_agent.py:72` | `def _resolve_targets(state, config)` |
| `_run` | method | `skills/claude_md_orchestrator/reviewer_agent.py:46` | `def _run(cmd, cwd)` |
| `_run_bandit` | method | `skills/claude_md_orchestrator/reviewer_agent.py:147` | `def _run_bandit(targets, cwd)` |
| `_run_mypy` | method | `skills/claude_md_orchestrator/reviewer_agent.py:134` | `def _run_mypy(targets, cwd)` |
| `_run_pytest` | method | `skills/claude_md_orchestrator/reviewer_agent.py:160` | `def _run_pytest(targets, cwd)` |
| `_run_ruff` | method | `skills/claude_md_orchestrator/reviewer_agent.py:121` | `def _run_ruff(targets, cwd)` |
| `run` | method | `skills/claude_md_orchestrator/reviewer_agent.py:171` | `def run(state, config)` |
| `write_report` | method | `skills/claude_md_orchestrator/reviewer_agent.py:231` | `def write_report(report, config)` |
| `SddResult` | class | `skills/claude_md_orchestrator/sdd_agent.py:40` | `class SddResult` |
| `_ask_llm` | method | `skills/claude_md_orchestrator/sdd_agent.py:154` | `def _ask_llm(contract, backend)` |
| `_coerce_scope` | method | `skills/claude_md_orchestrator/sdd_agent.py:56` | `def _coerce_scope(scope)` |
| `_compose_spec` | method | `skills/claude_md_orchestrator/sdd_agent.py:81` | `def _compose_spec(contract, min_sad_paths)` |
| `_render_yaml` | method | `skills/claude_md_orchestrator/sdd_agent.py:133` | `def _render_yaml(spec)` |
| `run` | method | `skills/claude_md_orchestrator/sdd_agent.py:210` | `def run(contract, config)` |
| `TddResult` | class | `skills/claude_md_orchestrator/tdd_agent.py:90` | `class TddResult` |
| `_compose_tests` | method | `skills/claude_md_orchestrator/tdd_agent.py:110` | `def _compose_tests(spec, contract)` |
| `_module_name` | method | `skills/claude_md_orchestrator/tdd_agent.py:105` | `def _module_name(contract)` |
| `_run_pytest` | method | `skills/claude_md_orchestrator/tdd_agent.py:154` | `def _run_pytest(test_path, cwd)` |
| `_slug` | function | `skills/claude_md_orchestrator/tdd_agent.py:79` | `def _slug(value)` |
| `read_test_source` | method | `skills/claude_md_orchestrator/tdd_agent.py:228` | `def read_test_source(test_path)` |
| `run` | method | `skills/claude_md_orchestrator/tdd_agent.py:175` | `def run(contract, spec, config)` |
| `config` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:54` | `def config(tmp_run_dir, tmp_path)` |
| `test_bdd_agent_lands_green` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:118` | `def test_bdd_agent_lands_green(config)` |
| `test_boy_scout_returns_report` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:239` | `def test_boy_scout_returns_report(config)` |
| `test_cicd_agent_writes_pipeline` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:262` | `def test_cicd_agent_writes_pipeline(config)` |
| `test_documentation_agent_emits_fenced_markdown` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:223` | `def test_documentation_agent_emits_fenced_markdown(config)` |
| `test_dod_validators_block_absolute_paths` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:154` | `def test_dod_validators_block_absolute_paths()` |
| `test_dod_validators_block_emoji` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:133` | `def test_dod_validators_block_emoji()` |
| `test_dod_validators_block_inline_comments` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:140` | `def test_dod_validators_block_inline_comments()` |
| `test_dod_validators_block_todo_markers` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:147` | `def test_dod_validators_block_todo_markers()` |
| `test_dod_validators_require_docstrings` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:161` | `def test_dod_validators_require_docstrings()` |
| `test_models_spec_round_trip` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:296` | `def test_models_spec_round_trip()` |
| `test_orchestrator_blocks_on_missing_contracts` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:206` | `def test_orchestrator_blocks_on_missing_contracts(tmp_run_dir, tmp_path)` |
| `test_orchestrator_blocks_on_sad_path_shortage` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:190` | `def test_orchestrator_blocks_on_sad_path_shortage(config)` |
| `test_orchestrator_full_cycle` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:168` | `def test_orchestrator_full_cycle(config)` |
| `test_parser_extracts_contract` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:78` | `def test_parser_extracts_contract(config)` |
| `test_sdd_agent_writes_spec` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:86` | `def test_sdd_agent_writes_spec(config)` |
| `test_tdd_agent_lands_red` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:102` | `def test_tdd_agent_lands_red(config)` |
| `tmp_run_dir` | function | `skills/claude_md_orchestrator/tests/test_orchestrator.py:46` | `def tmp_run_dir(tmp_path)` |
| `CheckResult` | class | `skills/claude_md_orchestrator/validators.py:70` | `class CheckResult` |
| `blocks` | method | `skills/claude_md_orchestrator/validators.py:85` | `def blocks(self)` |
| `check_docstrings` | method | `skills/claude_md_orchestrator/validators.py:223` | `def check_docstrings(source, path)` |
| `check_english_only` | method | `skills/claude_md_orchestrator/validators.py:199` | `def check_english_only(source, path)` |
| `check_magic_numbers` | method | `skills/claude_md_orchestrator/validators.py:299` | `def check_magic_numbers(source, path, allow)` |
| `check_markdown` | method | `skills/claude_md_orchestrator/validators.py:347` | `def check_markdown(content, path)` |
| `check_no_comments` | method | `skills/claude_md_orchestrator/validators.py:129` | `def check_no_comments(source, path)` |
| `check_no_emoji` | method | `skills/claude_md_orchestrator/validators.py:160` | `def check_no_emoji(content, path)` |
| `check_no_forbidden_markers` | method | `skills/claude_md_orchestrator/validators.py:182` | `def check_no_forbidden_markers(content, path)` |
| `check_no_hardcoded_paths_or_ips` | method | `skills/claude_md_orchestrator/validators.py:265` | `def check_no_hardcoded_paths_or_ips(source, path)` |
| `check_source` | method | `skills/claude_md_orchestrator/validators.py:334` | `def check_source(source, path, allow_numbers)` |
| `check_spec` | method | `skills/claude_md_orchestrator/validators.py:356` | `def check_spec(spec, min_sad_paths)` |
| `find_block_comments` | method | `skills/claude_md_orchestrator/validators.py:90` | `def find_block_comments(source)` |
| `find_inline_comments` | method | `skills/claude_md_orchestrator/validators.py:112` | `def find_inline_comments(source)` |
| `passed` | method | `skills/claude_md_orchestrator/validators.py:81` | `def passed(self)` |
| `ControlState` | class | `skills/daemon_control.py:90` | `class ControlState` |
| `DaemonControl` | class | `skills/daemon_control.py:168` | `class DaemonControl` |
| `PendingAction` | class | `skills/daemon_control.py:51` | `class PendingAction` |
| `__init__` | method | `skills/daemon_control.py:177` | `def __init__(self, sessions_dir)` |
| `_first_token` | method | `skills/daemon_control.py:160` | `def _first_token(command)` |
| `add_veto` | method | `skills/daemon_control.py:260` | `def add_veto(self, command_token)` |
| `clear_vetoes` | method | `skills/daemon_control.py:283` | `def clear_vetoes(self)` |
| `consume` | method | `skills/daemon_control.py:355` | `def consume(self, action_id)` |
| `decide` | method | `skills/daemon_control.py:327` | `def decide(self, action_id, decision)` |
| `from_dict` | method | `skills/daemon_control.py:123` | `def from_dict(cls, data)` |
| `is_expired` | method | `skills/daemon_control.py:81` | `def is_expired(self, now)` |
| `is_paused` | method | `skills/daemon_control.py:387` | `def is_paused(self)` |
| `is_vetoed` | method | `skills/daemon_control.py:391` | `def is_vetoed(self, command)` |
| `load` | method | `skills/daemon_control.py:194` | `def load(self)` |
| `path` | method | `skills/daemon_control.py:190` | `def path(self)` |
| `pause` | method | `skills/daemon_control.py:248` | `def pause(self)` |
| `propose` | method | `skills/daemon_control.py:298` | `def propose(self, command)` |
| `remove_veto` | method | `skills/daemon_control.py:275` | `def remove_veto(self, command_token)` |
| `require_approval` | method | `skills/daemon_control.py:256` | `def require_approval(self)` |
| `resume` | method | `skills/daemon_control.py:252` | `def resume(self)` |
| `save` | method | `skills/daemon_control.py:207` | `def save(self, state)` |
| `set_focus` | method | `skills/daemon_control.py:290` | `def set_focus(self, targets)` |
| `set_mode` | method | `skills/daemon_control.py:237` | `def set_mode(self, mode)` |
| `target_in_focus` | method | `skills/daemon_control.py:398` | `def target_in_focus(self, target)` |
| `to_dict` | method | `skills/daemon_control.py:112` | `def to_dict(self)` |
| `wait_for_decision` | method | `skills/daemon_control.py:406` | `def wait_for_decision(control, action)` |
| `wait_until_unpaused` | method | `skills/daemon_control.py:461` | `def wait_until_unpaused(control)` |
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
| `clear_pid` | function | `skills/heartbeat.py:55` | `def clear_pid()` |
| `is_running` | function | `skills/heartbeat.py:60` | `def is_running()` |
| `main` | function | `skills/heartbeat.py:125` | `def main()` |
| `run_loop` | function | `skills/heartbeat.py:72` | `def run_loop(interval, once)` |
| `write_pid` | function | `skills/heartbeat.py:51` | `def write_pid()` |
| `RuleSetBuilder` | class | `skills/hermes-lazyown/claudemd_rules.py:15` | `class RuleSetBuilder` |
| `__init__` | method | `skills/hermes-lazyown/claudemd_rules.py:25` | `def __init__(self)` |
| `_base_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:71` | `def _base_rules(self)` |
| `_credential_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:146` | `def _credential_rules(self)` |
| `_hermes_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:159` | `def _hermes_rules(self)` |
| `_phase_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:83` | `def _phase_rules(self)` |
| `_service_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:127` | `def _service_rules(self)` |
| `build` | method | `skills/hermes-lazyown/claudemd_rules.py:57` | `def build(self)` |
| `generate_rules` | method | `skills/hermes-lazyown/claudemd_rules.py:174` | `def generate_rules(phase, rhost, services, creds_found, is_hermes)` |
| `with_creds` | method | `skills/hermes-lazyown/claudemd_rules.py:47` | `def with_creds(self, found)` |
| `with_hermes` | method | `skills/hermes-lazyown/claudemd_rules.py:52` | `def with_hermes(self, is_hermes)` |
| `with_phase` | method | `skills/hermes-lazyown/claudemd_rules.py:32` | `def with_phase(self, phase)` |
| `with_services` | method | `skills/hermes-lazyown/claudemd_rules.py:42` | `def with_services(self, services)` |
| `with_target` | method | `skills/hermes-lazyown/claudemd_rules.py:37` | `def with_target(self, rhost)` |
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
| `Paths` | class | `skills/hermes-lazyown/constants.py:91` | `class Paths` |
| `PhaseNames` | class | `skills/hermes-lazyown/constants.py:59` | `class PhaseNames` |
| `claude_md_file` | method | `skills/hermes-lazyown/constants.py:144` | `def claude_md_file()` |
| `lazyown_dir` | method | `skills/hermes-lazyown/constants.py:95` | `def lazyown_dir()` |
| `objectives_file` | method | `skills/hermes-lazyown/constants.py:129` | `def objectives_file()` |
| `payload_file` | method | `skills/hermes-lazyown/constants.py:104` | `def payload_file()` |
| `scan_file` | method | `skills/hermes-lazyown/constants.py:114` | `def scan_file(rhost)` |
| `sessions_dir` | method | `skills/hermes-lazyown/constants.py:109` | `def sessions_dir()` |
| `soul_file` | method | `skills/hermes-lazyown/constants.py:139` | `def soul_file()` |
| `tasks_file` | method | `skills/hermes-lazyown/constants.py:134` | `def tasks_file()` |
| `vulns_file` | method | `skills/hermes-lazyown/constants.py:119` | `def vulns_file(rhost)` |
| `world_model_file` | method | `skills/hermes-lazyown/constants.py:124` | `def world_model_file()` |
| `ExecutionResult` | class | `skills/hermes-lazyown/executor.py:21` | `class ExecutionResult` |
| `LazyOwnExecutor` | class | `skills/hermes-lazyown/executor.py:58` | `class LazyOwnExecutor` |
| `__init__` | method | `skills/hermes-lazyown/executor.py:24` | `def __init__(self, stdout, stderr, returncode, timed_out, duration_ms)` |
| `__init__` | method | `skills/hermes-lazyown/executor.py:66` | `def __init__(self, lazyown_dir, timeout)` |
| `__str__` | method | `skills/hermes-lazyown/executor.py:51` | `def __str__(self)` |
| `_has_pty` | method | `skills/hermes-lazyown/executor.py:233` | `def _has_pty(self)` |
| `_run_via_subprocess` | method | `skills/hermes-lazyown/executor.py:114` | `def _run_via_subprocess(self, command, timeout)` |
| `_run_with_pty` | method | `skills/hermes-lazyown/executor.py:179` | `def _run_with_pty(self, argv, command, timeout, env)` |
| `_run_without_pty` | method | `skills/hermes-lazyown/executor.py:149` | `def _run_without_pty(self, argv, command, timeout, env)` |
| `combined` | method | `skills/hermes-lazyown/executor.py:39` | `def combined(self)` |
| `execute` | method | `skills/hermes-lazyown/executor.py:77` | `def execute(self, command, timeout)` |
| `execute_batch` | method | `skills/hermes-lazyown/executor.py:98` | `def execute_batch(self, commands, timeout)` |
| `success` | method | `skills/hermes-lazyown/executor.py:47` | `def success(self)` |
| `CheckpointSerializer` | class | `skills/hermes-lazyown/hermes_sync.py:27` | `class CheckpointSerializer` |
| `DelegationPlanner` | class | `skills/hermes-lazyown/hermes_sync.py:147` | `class DelegationPlanner` |
| `HermesSyncError` | class | `skills/hermes-lazyown/hermes_sync.py:21` | `class HermesSyncError(Exception)` |
| `ObjectiveTodoSync` | class | `skills/hermes-lazyown/hermes_sync.py:75` | `class ObjectiveTodoSync` |
| `__init__` | method | `skills/hermes-lazyown/hermes_sync.py:33` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `skills/hermes-lazyown/hermes_sync.py:84` | `def __init__(self, objectives_path)` |
| `clear` | method | `skills/hermes-lazyown/hermes_sync.py:66` | `def clear(self)` |
| `inject_objective` | method | `skills/hermes-lazyown/hermes_sync.py:129` | `def inject_objective(self, text, priority, notes)` |
| `mark_done` | method | `skills/hermes-lazyown/hermes_sync.py:108` | `def mark_done(self, objective_text)` |
| `pending_objectives` | method | `skills/hermes-lazyown/hermes_sync.py:87` | `def pending_objectives(self)` |
| `plan_for_credential` | method | `skills/hermes-lazyown/hermes_sync.py:219` | `def plan_for_credential(self, cred_type, value, rhost)` |
| `plan_for_service` | method | `skills/hermes-lazyown/hermes_sync.py:156` | `def plan_for_service(self, service, port, rhost)` |
| `read` | method | `skills/hermes-lazyown/hermes_sync.py:51` | `def read(self)` |
| `write` | method | `skills/hermes-lazyown/hermes_sync.py:37` | `def write(self, state)` |
| `_auto_inject_objective` | function | `skills/hermes-lazyown/mcp_server.py:612` | `def _auto_inject_objective(arguments)` |
| `_auto_loop` | function | `skills/hermes-lazyown/mcp_server.py:592` | `def _auto_loop(arguments)` |
| `_c2_get_beacons` | function | `skills/hermes-lazyown/mcp_server.py:726` | `def _c2_get_beacons()` |
| `_c2_status` | function | `skills/hermes-lazyown/mcp_server.py:705` | `def _c2_status()` |
| `_compact` | function | `skills/hermes-lazyown/mcp_server.py:91` | `def _compact(result, phase, tool_name)` |
| `_core_command_help` | function | `skills/hermes-lazyown/mcp_server.py:484` | `def _core_command_help(arguments)` |
| `_core_run_command` | function | `skills/hermes-lazyown/mcp_server.py:468` | `def _core_run_command(arguments)` |
| `_core_session_init` | function | `skills/hermes-lazyown/mcp_server.py:399` | `def _core_session_init(arguments)` |
| `_core_set_config` | function | `skills/hermes-lazyown/mcp_server.py:445` | `def _core_set_config(arguments)` |
| `_desc` | function | `skills/hermes-lazyown/mcp_server.py:119` | `def _desc(base)` |
| `_get_checkpoint_serializer` | function | `skills/hermes-lazyown/mcp_server.py:68` | `def _get_checkpoint_serializer()` |
| `_get_compactor` | function | `skills/hermes-lazyown/mcp_server.py:52` | `def _get_compactor()` |
| `_get_config` | function | `skills/hermes-lazyown/mcp_server.py:45` | `def _get_config()` |
| `_get_delegation_planner` | function | `skills/hermes-lazyown/mcp_server.py:82` | `def _get_delegation_planner()` |
| `_get_executor` | function | `skills/hermes-lazyown/mcp_server.py:60` | `def _get_executor()` |
| `_get_objective_sync` | function | `skills/hermes-lazyown/mcp_server.py:75` | `def _get_objective_sync()` |
| `_handle_tool` | function | `skills/hermes-lazyown/mcp_server.py:351` | `def _handle_tool(name, arguments)` |
| `_hermes_checkpoint_read` | function | `skills/hermes-lazyown/mcp_server.py:648` | `def _hermes_checkpoint_read()` |
| `_hermes_checkpoint_write` | function | `skills/hermes-lazyown/mcp_server.py:638` | `def _hermes_checkpoint_write(arguments)` |
| `_hermes_delegate_plan` | function | `skills/hermes-lazyown/mcp_server.py:677` | `def _hermes_delegate_plan(arguments)` |
| `_hermes_rules_generate` | function | `skills/hermes-lazyown/mcp_server.py:659` | `def _hermes_rules_generate(arguments)` |
| `_intel_facts_show` | function | `skills/hermes-lazyown/mcp_server.py:514` | `def _intel_facts_show(arguments)` |

Next: [SYMBOLS_p19.md](SYMBOLS_p19.md)
