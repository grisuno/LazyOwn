# Symbols (page 15 of 44)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_build_golden_pac` | method | `modules/kerberos_tickets.py:339` | `def _build_golden_pac(self, config)` |
| `_build_kirbi` | method | `modules/kerberos_tickets.py:235` | `def _build_kirbi(self, ticket, enc_part, etype)` |
| `_build_silver_pac` | method | `modules/kerberos_tickets.py:200` | `def _build_silver_pac(self, config, start, end)` |
| `_build_ticket_structure` | method | `modules/kerberos_tickets.py:225` | `def _build_ticket_structure(self, config, flags, enc_part)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:254` | `def _impacket_command(self, config)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:388` | `def _impacket_command(self, config)` |
| `_mimikatz_command` | method | `modules/kerberos_tickets.py:379` | `def _mimikatz_command(self, config)` |
| `_mimikatz_inject_command` | method | `modules/kerberos_tickets.py:244` | `def _mimikatz_inject_command(self, config)` |
| `_resolve_key` | method | `modules/kerberos_tickets.py:190` | `def _resolve_key(self, config)` |
| `_resolve_krbtgt_key` | method | `modules/kerberos_tickets.py:324` | `def _resolve_krbtgt_key(self, config)` |
| `cleanup_command` | method | `modules/kerberos_tickets.py:612` | `def cleanup_command()` |
| `detect_skeleton_key` | method | `modules/kerberos_tickets.py:578` | `def detect_skeleton_key(target_host, domain, dc_ip)` |
| `forge` | method | `modules/kerberos_tickets.py:134` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:275` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:408` | `def forge(self, config)` |
| `forge_rbcd` | method | `modules/kerberos_tickets.py:530` | `def forge_rbcd(self, machine_account_hash, target_service, domain, username)` |
| `forge_s4u2self` | method | `modules/kerberos_tickets.py:472` | `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)` |
| `inject_command` | method | `modules/kerberos_tickets.py:600` | `def inject_command(target_host)` |
| `_build_svg` | function | `modules/kill_chain_viz.py:34` | `def _build_svg(phases)` |
| `_load_phases` | function | `modules/kill_chain_viz.py:20` | `def _load_phases(sessions)` |
| `_read_target` | function | `modules/kill_chain_viz.py:27` | `def _read_target()` |
| `generate_html` | function | `modules/kill_chain_viz.py:69` | `def generate_html(target, sessions)` |
| `generate_svg` | function | `modules/kill_chain_viz.py:102` | `def generate_svg(target, sessions)` |
| `KillChain` | class | `modules/killchain.py:145` | `class KillChain` |
| `KillChainConfig` | class | `modules/killchain.py:38` | `class KillChainConfig` |
| `PhaseStatus` | class | `modules/killchain.py:136` | `class PhaseStatus` |
| `advance_phase` | method | `modules/killchain.py:251` | `def advance_phase(new_phase, world_model_path, host)` |
| `cli_phase_to_host_state` | method | `modules/killchain.py:191` | `def cli_phase_to_host_state(phase)` |
| `compact_progress` | method | `modules/killchain.py:377` | `def compact_progress(current_phase, phases_entered)` |
| `config` | method | `modules/killchain.py:154` | `def config()` |
| `current_phase` | method | `modules/killchain.py:204` | `def current_phase(world_model_path)` |
| `engagement_phase_to_cli` | method | `modules/killchain.py:179` | `def engagement_phase_to_cli(engagement_value)` |
| `get_killchain` | function | `modules/killchain.py:453` | `def get_killchain()` |
| `get_progress` | method | `modules/killchain.py:328` | `def get_progress(world_model_path)` |
| `is_valid_phase` | method | `modules/killchain.py:127` | `def is_valid_phase(self, phase)` |
| `phase_colors` | method | `modules/killchain.py:169` | `def phase_colors()` |
| `phase_index` | method | `modules/killchain.py:120` | `def phase_index(self, phase)` |
| `phase_index` | method | `modules/killchain.py:408` | `def phase_index(phase)` |
| `phase_labels` | method | `modules/killchain.py:164` | `def phase_labels()` |
| `phase_rich_colors` | method | `modules/killchain.py:174` | `def phase_rich_colors()` |
| `phases` | method | `modules/killchain.py:159` | `def phases()` |
| `phases_for_display` | method | `modules/killchain.py:397` | `def phases_for_display()` |
| `snapshot` | method | `modules/killchain.py:413` | `def snapshot(world_model_path)` |
| `world_model_path` | method | `modules/killchain.py:116` | `def world_model_path(self)` |
| `ReverseShellApp` | class | `modules/kivi.py:11` | `class ReverseShellApp(App)` |
| `build` | method | `modules/kivi.py:12` | `def build(self)` |
| `connect_to_server` | method | `modules/kivi.py:27` | `def connect_to_server(self, instance)` |
| `ConversationStore` | class | `modules/lazy_agent.py:261` | `class ConversationStore` |
| `ObservableAgentRunner` | class | `modules/lazy_agent.py:145` | `class ObservableAgentRunner(AgentRunner)` |
| `__init__` | method | `modules/lazy_agent.py:148` | `def __init__(self, model, system_prompt, max_iterations, on_event)` |
| `__init__` | method | `modules/lazy_agent.py:264` | `def __init__(self, task_id)` |
| `_call_model` | method | `modules/lazy_agent.py:174` | `def _call_model(self)` |
| `_deep_clean` | function | `modules/lazy_agent.py:237` | `def _deep_clean(value, _depth)` |
| `_enable_streaming` | function | `modules/lazy_agent.py:123` | `def _enable_streaming(runner, on_event)` |
| `_invoke` | function | `modules/lazy_agent.py:190` | `def _invoke()` |
| `_json_default` | function | `modules/lazy_agent.py:221` | `def _json_default(value)` |
| `_json_safe` | function | `modules/lazy_agent.py:253` | `def _json_safe(messages)` |
| `_kill` | function | `modules/lazy_agent.py:583` | `def _kill()` |
| `_load` | method | `modules/lazy_agent.py:269` | `def _load(self)` |
| `_process_tool_call` | method | `modules/lazy_agent.py:159` | `def _process_tool_call(self, tool_call)` |
| `_process_watchdog` | function | `modules/lazy_agent.py:578` | `def _process_watchdog(timeout_sec, process)` |
| `_session_from_line` | function | `modules/lazy_agent.py:556` | `def _session_from_line(line)` |
| `_tick` | function | `modules/lazy_agent.py:196` | `def _tick()` |
| `intent_messages` | method | `modules/lazy_agent.py:273` | `def intent_messages(self, intent_id)` |
| `max_iterations` | function | `modules/lazy_agent.py:72` | `def max_iterations()` |
| `model_timeout_sec` | function | `modules/lazy_agent.py:41` | `def model_timeout_sec()` |
| `register_tools` | function | `modules/lazy_agent.py:322` | `def register_tools(runner, specs)` |
| `reset_intents` | method | `modules/lazy_agent.py:315` | `def reset_intents(self)` |
| `resolve_agentic_model` | function | `modules/lazy_agent.py:83` | `def resolve_agentic_model(exclude)` |
| `run` | method | `modules/lazy_agent.py:168` | `def run(self, user_input)` |
| `run_external_hermes` | function | `modules/lazy_agent.py:472` | `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` |
| `run_external_opencode` | function | `modules/lazy_agent.py:396` | `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` |
| `run_main_session` | function | `modules/lazy_agent.py:374` | `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` |
| `run_worker_session` | function | `modules/lazy_agent.py:335` | `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` |
| `save_intent` | method | `modules/lazy_agent.py:278` | `def save_intent(self, intent_id, messages)` |
| `save_session` | method | `modules/lazy_agent.py:305` | `def save_session(self, session_id, messages, title)` |
| `session` | method | `modules/lazy_agent.py:287` | `def session(self, session_id)` |
| `sessions` | method | `modules/lazy_agent.py:291` | `def sessions(self)` |
| `tool_calling_enabled` | function | `modules/lazy_agent.py:57` | `def tool_calling_enabled()` |
| `_data_dir` | function | `modules/lazy_bridge.py:35` | `def _data_dir()` |
| `_extract_hosts_from_graph` | function | `modules/lazy_bridge.py:180` | `def _extract_hosts_from_graph(graph)` |
| `_notify` | function | `modules/lazy_bridge.py:351` | `def _notify(progress, text)` |
| `_read_json` | function | `modules/lazy_bridge.py:47` | `def _read_json(path, default)` |
| `_read_jsonl` | function | `modules/lazy_bridge.py:64` | `def _read_jsonl(path)` |
| `_read_new_traffic` | function | `modules/lazy_bridge.py:314` | `def _read_new_traffic(path, offset)` |
| `_record_sync` | function | `modules/lazy_bridge.py:545` | `def _record_sync(action, summary)` |
| `bridge_status` | function | `modules/lazy_bridge.py:159` | `def bridge_status()` |
| `lazy_activity` | function | `modules/lazy_bridge.py:123` | `def lazy_activity(task_id)` |
| `lazy_assets` | function | `modules/lazy_bridge.py:99` | `def lazy_assets()` |
| `lazy_graph` | function | `modules/lazy_bridge.py:110` | `def lazy_graph(task_id)` |
| `lazy_guard_audit` | function | `modules/lazy_bridge.py:147` | `def lazy_guard_audit(task_id)` |
| `lazy_tasks` | function | `modules/lazy_bridge.py:88` | `def lazy_tasks()` |
| `lazy_traffic` | function | `modules/lazy_bridge.py:135` | `def lazy_traffic(task_id)` |
| `pull_findings_to_lifecycle` | function | `modules/lazy_bridge.py:286` | `def pull_findings_to_lifecycle()` |
| `pull_to_objectives` | function | `modules/lazy_bridge.py:251` | `def pull_to_objectives()` |
| `pull_to_world_model` | function | `modules/lazy_bridge.py:206` | `def pull_to_world_model()` |
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:361` | `def pull_traffic_to_recorder(progress)` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:429` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:454` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:519` | `def sync_all(progress)` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `catalog_cli_for_phase` | function | `modules/lazy_cli_bridge.py:219` | `def catalog_cli_for_phase(limit)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:253` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:276` | `def set_full_cli(enabled)` |
| `LazyEngine` | class | `modules/lazy_engine.py:55` | `class LazyEngine(LazyLoopEngine)` |
| `install_command_for` | function | `modules/lazy_installer.py:70` | `def install_command_for(tool)` |
| `installer_enabled` | function | `modules/lazy_installer.py:41` | `def installer_enabled()` |
| `intent_for` | function | `modules/lazy_installer.py:75` | `def intent_for(tool)` |
| `set_installer_enabled` | function | `modules/lazy_installer.py:58` | `def set_installer_enabled(enabled)` |
| `steps_for_install` | function | `modules/lazy_installer.py:88` | `def steps_for_install(text)` |
| `tool_from_intent` | function | `modules/lazy_installer.py:80` | `def tool_from_intent(text)` |
| `_append` | function | `modules/lazy_intel.py:70` | `def _append(record)` |
| `_is_ip_literal` | function | `modules/lazy_intel.py:274` | `def _is_ip_literal(value)` |
| `_log_path` | function | `modules/lazy_intel.py:35` | `def _log_path()` |
| `_mask` | function | `modules/lazy_intel.py:41` | `def _mask(text)` |
| `_now` | function | `modules/lazy_intel.py:30` | `def _now()` |
| `describe_command` | function | `modules/lazy_intel.py:105` | `def describe_command(command)` |
| `export_spans` | function | `modules/lazy_intel.py:324` | `def export_spans(task_id, out)` |
| `fuse_routing_decisions` | function | `modules/lazy_intel.py:285` | `def fuse_routing_decisions(task_id)` |
| `infer_source` | function | `modules/lazy_intel.py:79` | `def infer_source(command, intent_text)` |
| `mask_configured` | function | `modules/lazy_intel.py:228` | `def mask_configured(text)` |
| `read_decisions` | function | `modules/lazy_intel.py:202` | `def read_decisions(task_id, limit)` |
| `record_routing_decision` | function | `modules/lazy_intel.py:120` | `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | function | `modules/lazy_intel.py:160` | `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` |
| `stack_signature` | function | `modules/lazy_intel.py:254` | `def stack_signature(assets)` |
| `ActivityLog` | class | `modules/lazy_loop.py:1424` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2156` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:953` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:928` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2250` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:5324` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7141` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:6331` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:919` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1116` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:905` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6053` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1396` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1815` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2402` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:7465` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:942` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:6603` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:6434` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3035` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5225` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2334` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7067` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7171` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:7333` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:7360` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2604` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:7290` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2562` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:7023` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1557` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:3484` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:956` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1119` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1399` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1427` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1560` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1818` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2165` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2253` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2337` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2431` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2565` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2607` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3038` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3487` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5228` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:5332` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6056` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:6334` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:6437` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:6620` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7026` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7144` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7293` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7336` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7490` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:3894` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4127` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:4153` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:4498` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:4316` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:4530` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:5467` | `def _apply_stored_bodies(self, bodies)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2100` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:4639` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:4962` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:8589` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:8625` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:5535` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:5349` | `def _bodies_path(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:9702` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3227` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:492` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:9022` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:4289` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:5337` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:4953` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3049` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:5527` | `def _content_versions(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:546` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3386` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4852` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3058` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:4628` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:6159` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:6155` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:4142` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:8540` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2426` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:588` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:508` | `def _encrypt_channel_secret(plaintext)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:8680` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2409` | `def _event_for(cls, path, item_id)` |
| `_find` | function | `modules/lazy_loop.py:5556` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:9598` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:3819` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:5495` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:9029` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:5544` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:3945` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_host_from_token` | function | `modules/lazy_loop.py:350` | `def _host_from_token(token)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:8045` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:243` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:5491` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5216` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:429` | `def _kill()` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3400` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:796` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:804` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:4728` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2437` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:6339` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7030` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7148` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7297` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:5353` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:5341` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2172` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:756` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2176` | `def _load_task(self)` |
| `_mask_key` | function | `modules/lazy_loop.py:469` | `def _mask_key(match)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6029` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2121` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:9302` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:9276` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:9322` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:4651` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:5410` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:696` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1752` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:738` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:4218` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3218` | `def _origin_fact(self)` |
| `_parts` | method | `modules/lazy_loop.py:7612` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:970` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1141` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1837` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2572` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2612` | `def _persist(self)` |
| `_prior_steps` | method | `modules/lazy_loop.py:3596` | `def _prior_steps(self, intent)` |
| `_reader` | function | `modules/lazy_loop.py:4240` | `def _reader()` |
| `_record` | method | `modules/lazy_loop.py:6696` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:6771` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:6991` | `def _record_raw(self, member, prompt, reply, ok)` |
| `_refresh` | method | `modules/lazy_loop.py:2700` | `def _refresh(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:407` | `def _register_loop_executor(executor)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:6731` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:6214` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:5361` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:4876` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:484` | `def _restrict_file(path)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:6702` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:4667` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:8395` | `def _run_one(index_node)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:4940` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2441` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:5357` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:5345` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2183` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:766` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2187` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:3567` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:2033` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2023` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:6631` | `def _seed_defaults(self)` |
| `_send_email` | method | `modules/lazy_loop.py:6509` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:4253` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:4816` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3159` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:781` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:8060` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:8859` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3458` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:4186` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:5014` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:743` | `def _store_path(name)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:4890` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:237` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:9140` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:8237` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2083` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:3884` | `def _target_for(self, intent)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:4917` | `def _task_executed_commands(self)` |
| `_traffic_template` | function | `modules/lazy_loop.py:786` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:5562` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:413` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:257` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:578` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:4717` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:4198` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:6193` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:5382` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:8645` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:6230` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5074` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2374` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2669` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2192` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2576` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:6343` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:7152` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:7305` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:6449` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2803` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1196` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:7830` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:7848` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:6660` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1153` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:1844` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2822` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:9149` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2738` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1209` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1224` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1220` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:6248` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:7525` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1799` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:419` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2599` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:7077` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:1938` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2359` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1721` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:7048` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:7558` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:7043` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:9627` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:7797` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:5950` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1716` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:6441` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:1886` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2321` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1237` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1409` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1805` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:7435` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:2858` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:3556` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:5812` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:5661` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1298` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2583` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:6784` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:5893` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:6960` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1029` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1063` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:5608` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2616` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:7617` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2519` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:2975` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:974` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2660` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:7902` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:7936` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:9035` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2689` | `def dequeue_next(self)` |
| `digest_overview` | method | `modules/lazy_loop.py:5846` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:9168` | `def drain_queue(self, max_tasks)` |
| `edit_goal` | method | `modules/lazy_loop.py:7890` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1432` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:6547` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2678` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3012` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:7562` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2235` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1769` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:3620` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:5788` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2797` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1792` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:6426` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:9371` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:9430` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:9342` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:2909` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:2877` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3370` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6039` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1326` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:6385` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1471` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:6369` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1008` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1181` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1640` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2627` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:7325` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:7348` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:8177` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:9820` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:9565` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:4386` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1332` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:6949` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2341` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2467` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:7123` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:5501` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:9196` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:978` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:4417` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:4409` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:863` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:2842` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:2871` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2257` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1012` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1228` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2231` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2631` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7161` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7195` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7301` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7352` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1358` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:7696` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2732` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:2937` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:7410` | `def log(self, task_id, limit, session)` |
| `lookup` | method | `modules/lazy_loop.py:1966` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:402` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:9751` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1019` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:7165` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:6655` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2592` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:5442` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1342` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2390` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:5620` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:7589` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1251` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1244` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:835` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2647` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:8081` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:7724` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1404` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2463` | `def pending(self)` |
| `plan` | method | `modules/lazy_loop.py:3066` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:151` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:7913` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:8989` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:9119` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:9069` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:9113` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:9105` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2673` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:6324` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:6977` | `def raw_entries(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1457` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1587` | `def read(self, limit)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
