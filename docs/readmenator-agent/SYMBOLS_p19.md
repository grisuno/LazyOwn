# Symbols (page 19 of 35)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_intel_recommend_next` | function | `skills/hermes-lazyown/mcp_server.py:548` | `def _intel_recommend_next()` |
| `_intel_searchsploit` | function | `skills/hermes-lazyown/mcp_server.py:564` | `def _intel_searchsploit(arguments)` |
| `_try_import_lazyown_module` | function | `skills/hermes-lazyown/mcp_server.py:100` | `def _try_import_lazyown_module(module_name)` |
| `call_tool` | function | `skills/hermes-lazyown/mcp_server.py:340` | `def call_tool(name, arguments)` |
| `list_tools` | function | `skills/hermes-lazyown/mcp_server.py:335` | `def list_tools()` |
| `main` | function | `skills/hermes-lazyown/mcp_server.py:749` | `def main()` |
| `CompactionResult` | class | `skills/hermes-lazyown/output_compactor.py:17` | `class CompactionResult` |
| `CompactionStrategy` | class | `skills/hermes-lazyown/output_compactor.py:39` | `class CompactionStrategy(ABC)` |
| `DefaultCompaction` | class | `skills/hermes-lazyown/output_compactor.py:165` | `class DefaultCompaction(CompactionStrategy)` |
| `EnumCompaction` | class | `skills/hermes-lazyown/output_compactor.py:83` | `class EnumCompaction(CompactionStrategy)` |
| `ExploitCompaction` | class | `skills/hermes-lazyown/output_compactor.py:114` | `class ExploitCompaction(CompactionStrategy)` |
| `OutputCompactor` | class | `skills/hermes-lazyown/output_compactor.py:182` | `class OutputCompactor` |
| `PrivescCompaction` | class | `skills/hermes-lazyown/output_compactor.py:143` | `class PrivescCompaction(CompactionStrategy)` |
| `ReconCompaction` | class | `skills/hermes-lazyown/output_compactor.py:48` | `class ReconCompaction(CompactionStrategy)` |
| `__init__` | method | `skills/hermes-lazyown/output_compactor.py:20` | `def __init__(self, compacted, original_lines, compacted_lines)` |
| `__init__` | method | `skills/hermes-lazyown/output_compactor.py:168` | `def __init__(self, max_lines)` |
| `__init__` | method | `skills/hermes-lazyown/output_compactor.py:199` | `def __init__(self, default_max_lines)` |
| `__str__` | method | `skills/hermes-lazyown/output_compactor.py:32` | `def __str__(self)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:43` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:58` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:96` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:127` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:154` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:171` | `def compact(self, raw_output, tool_name)` |
| `compact` | method | `skills/hermes-lazyown/output_compactor.py:203` | `def compact(self, raw_output, phase, tool_name)` |
| `reduction_ratio` | method | `skills/hermes-lazyown/output_compactor.py:26` | `def reduction_ratio(self)` |
| `ConsensusProtocol` | class | `skills/hive_mind.py:833` | `class ConsensusProtocol` |
| `ConsensusVote` | class | `skills/hive_mind.py:825` | `class ConsensusVote` |
| `DroneAgent` | class | `skills/hive_mind.py:995` | `class DroneAgent` |
| `DronePool` | class | `skills/hive_mind.py:1552` | `class DronePool` |
| `DroneState` | class | `skills/hive_mind.py:979` | `class DroneState` |
| `DroneStateStore` | class | `skills/hive_mind.py:1393` | `class DroneStateStore` |
| `EpisodicStore` | class | `skills/hive_mind.py:184` | `class EpisodicStore(IMemoryStore)` |
| `HiveBus` | class | `skills/hive_mind.py:712` | `class HiveBus` |
| `HiveMemory` | class | `skills/hive_mind.py:559` | `class HiveMemory` |
| `HiveMessage` | class | `skills/hive_mind.py:702` | `class HiveMessage` |
| `HiveMind` | class | `skills/hive_mind.py:1706` | `class HiveMind` |
| `ICommandRunner` | class | `skills/hive_mind.py:167` | `class ICommandRunner(ABC)` |
| `IMemoryStore` | class | `skills/hive_mind.py:157` | `class IMemoryStore(IReadableMemory, IWritableMemory)` |
| `IReadableMemory` | class | `skills/hive_mind.py:141` | `class IReadableMemory(ABC)` |
| `IWritableMemory` | class | `skills/hive_mind.py:149` | `class IWritableMemory(ABC)` |
| `LongtermStore` | class | `skills/hive_mind.py:494` | `class LongtermStore(IMemoryStore)` |
| `QueenBrain` | class | `skills/hive_mind.py:1200` | `class QueenBrain` |
| `SemanticStore` | class | `skills/hive_mind.py:344` | `class SemanticStore(IMemoryStore)` |
| `__init__` | method | `skills/hive_mind.py:210` | `def __init__(self, db_path)` |
| `__init__` | method | `skills/hive_mind.py:353` | `def __init__(self, chroma_dir, episodic_fallback)` |
| `__init__` | method | `skills/hive_mind.py:570` | `def __init__(self, stores, episodic, semantic, longterm)` |
| `__init__` | method | `skills/hive_mind.py:720` | `def __init__(self)` |
| `__init__` | method | `skills/hive_mind.py:865` | `def __init__(self, risk_assessor)` |
| `__init__` | method | `skills/hive_mind.py:1003` | `def __init__(self, drone_id, role, goal, backend, memory, bus, max_iterations, api_key, model, runner, on_state_change)` |
| `__init__` | method | `skills/hive_mind.py:1212` | `def __init__(self, memory, bus, pool, consensus)` |
| `__init__` | method | `skills/hive_mind.py:1425` | `def __init__(self, db_path)` |
| `__init__` | method | `skills/hive_mind.py:1564` | `def __init__(self, memory, bus, state_store)` |
| `__init__` | method | `skills/hive_mind.py:1712` | `def __init__(self)` |
| `_architect_vote` | method | `skills/hive_mind.py:926` | `def _architect_vote(role, goal)` |
| `_build_hive_context` | method | `skills/hive_mind.py:1123` | `def _build_hive_context(self)` |
| `_build_system_prompt` | method | `skills/hive_mind.py:1134` | `def _build_system_prompt(self, tool_names, hive_ctx)` |
| `_classify_objective` | method | `skills/hive_mind.py:1188` | `def _classify_objective(goal)` |
| `_cli` | method | `skills/hive_mind.py:1949` | `def _cli()` |
| `_connect` | method | `skills/hive_mind.py:215` | `def _connect(self)` |
| `_embed` | method | `skills/hive_mind.py:477` | `def _embed(self, text)` |
| `_estimate_detection_risk` | method | `skills/hive_mind.py:945` | `def _estimate_detection_risk(self, role, goal)` |
| `_get_embed_model` | function | `skills/hive_mind.py:107` | `def _get_embed_model()` |
| `_init_chroma` | method | `skills/hive_mind.py:361` | `def _init_chroma(self, chroma_dir)` |
| `_load_payload_key` | method | `skills/hive_mind.py:1151` | `def _load_payload_key()` |
| `_persist` | method | `skills/hive_mind.py:1029` | `def _persist(self)` |
| `_privesc_hunter_vote` | method | `skills/hive_mind.py:911` | `def _privesc_hunter_vote(role, goal)` |
| `_run` | method | `skills/hive_mind.py:1051` | `def _run(self)` |
| `_sanitize_fts` | method | `skills/hive_mind.py:261` | `def _sanitize_fts(query)` |
| `_stealth_vote` | method | `skills/hive_mind.py:897` | `def _stealth_vote(self, detection_risk)` |
| `_weighted_approval` | method | `skills/hive_mind.py:954` | `def _weighted_approval(votes)` |
| `ack_broadcast` | method | `skills/hive_mind.py:738` | `def ack_broadcast(self, agent_id, msg_id)` |
| `active_count` | method | `skills/hive_mind.py:1692` | `def active_count(self)` |
| `available` | method | `skills/hive_mind.py:375` | `def available(self)` |
| `build_default_hive_memory` | method | `skills/hive_mind.py:545` | `def build_default_hive_memory(db_path)` |
| `collect` | method | `skills/hive_mind.py:1329` | `def collect(self, drone_ids, timeout, poll_interval)` |
| `collect_and_synthesize` | method | `skills/hive_mind.py:1786` | `def collect_and_synthesize(self, drone_ids, goal)` |
| `count` | method | `skills/hive_mind.py:466` | `def count(self)` |
| `delete_older_than` | method | `skills/hive_mind.py:1532` | `def delete_older_than(self, days)` |
| `dispatch` | method | `skills/hive_mind.py:1243` | `def dispatch(self, tasks, backend, api_key, max_iterations)` |
| `drone_result` | method | `skills/hive_mind.py:1772` | `def drone_result(self, drone_id)` |
| `evaluate` | method | `skills/hive_mind.py:868` | `def evaluate(self, role, goal)` |
| `forget` | method | `skills/hive_mind.py:323` | `def forget(self, older_than_hours, topic)` |
| `forget` | method | `skills/hive_mind.py:689` | `def forget(self, older_than_hours, topic)` |
| `forget` | method | `skills/hive_mind.py:1790` | `def forget(self, older_than_hours, topic)` |
| `get_hive` | method | `skills/hive_mind.py:1801` | `def get_hive()` |
| `get_state` | method | `skills/hive_mind.py:1658` | `def get_state(self, drone_id)` |
| `join` | method | `skills/hive_mind.py:1046` | `def join(self, timeout)` |
| `list_all` | method | `skills/hive_mind.py:1667` | `def list_all(self, limit)` |
| `load_all` | method | `skills/hive_mind.py:1458` | `def load_all(self, limit)` |
| `load_interrupted` | method | `skills/hive_mind.py:1506` | `def load_interrupted(self)` |
| `mark_interrupted` | method | `skills/hive_mind.py:1485` | `def mark_interrupted(self)` |
| `mcp_hive_collect` | method | `skills/hive_mind.py:1888` | `def mcp_hive_collect(drone_ids_csv, goal)` |
| `mcp_hive_forget` | method | `skills/hive_mind.py:1899` | `def mcp_hive_forget(older_than_hours, topic)` |
| `mcp_hive_plan` | method | `skills/hive_mind.py:1873` | `def mcp_hive_plan(goal, n_drones)` |
| `mcp_hive_recall` | method | `skills/hive_mind.py:1859` | `def mcp_hive_recall(query, top_k)` |
| `mcp_hive_recover` | method | `skills/hive_mind.py:1905` | `def mcp_hive_recover(backend, api_key, max_iterations)` |
| `mcp_hive_result` | method | `skills/hive_mind.py:1882` | `def mcp_hive_result(drone_id)` |
| `mcp_hive_spawn` | method | `skills/hive_mind.py:1816` | `def mcp_hive_spawn(goal, role, n_drones, backend, max_iterations, api_key)` |
| `mcp_hive_status` | method | `skills/hive_mind.py:1854` | `def mcp_hive_status()` |
| `name` | method | `skills/hive_mind.py:176` | `def name(self)` |
| `pending_count` | method | `skills/hive_mind.py:742` | `def pending_count(self, agent_id)` |
| `plan` | method | `skills/hive_mind.py:1224` | `def plan(self, goal, n_drones)` |
| `plan_and_dispatch` | method | `skills/hive_mind.py:1316` | `def plan_and_dispatch(self, goal, n_drones, backend, api_key, max_iterations)` |
| `publish` | method | `skills/hive_mind.py:724` | `def publish(self, msg)` |
| `read_bus` | method | `skills/hive_mind.py:1383` | `def read_bus(self)` |
| `recall` | method | `skills/hive_mind.py:145` | `def recall(self, query, top_k)` |
| `recall` | method | `skills/hive_mind.py:268` | `def recall(self, query, top_k, role, event_type)` |
| `recall` | method | `skills/hive_mind.py:423` | `def recall(self, query, top_k, where)` |
| `recall` | method | `skills/hive_mind.py:507` | `def recall(self, query, top_k)` |
| `recall` | method | `skills/hive_mind.py:653` | `def recall(self, query, top_k)` |
| `recall` | method | `skills/hive_mind.py:1768` | `def recall(self, query, top_k)` |
| `recall_episodic` | method | `skills/hive_mind.py:618` | `def recall_episodic(self, query, top_k, role, event_type)` |
| `recall_longterm` | method | `skills/hive_mind.py:645` | `def recall_longterm(self, query, top_k)` |
| `recall_semantic` | method | `skills/hive_mind.py:632` | `def recall_semantic(self, query, top_k, where)` |
| `receive` | method | `skills/hive_mind.py:730` | `def receive(self, agent_id, max_msgs)` |
| `recover_from_store` | method | `skills/hive_mind.py:1578` | `def recover_from_store(self)` |
| `requeue_interrupted` | method | `skills/hive_mind.py:1632` | `def requeue_interrupted(self, backend, api_key, max_iterations)` |
| `run` | method | `skills/hive_mind.py:171` | `def run(self, command, timeout)` |
| `spawn` | method | `skills/hive_mind.py:1599` | `def spawn(self, role, goal, backend, api_key, model, max_iterations, runner)` |
| `spawn` | method | `skills/hive_mind.py:1723` | `def spawn(self, goal, role, backend, api_key, max_iterations)` |
| `spawn_hive` | method | `skills/hive_mind.py:1737` | `def spawn_hive(self, goal, n_drones, backend, api_key, max_iterations)` |
| `start` | method | `skills/hive_mind.py:1037` | `def start(self)` |
| `stats` | method | `skills/hive_mind.py:312` | `def stats(self)` |
| `stats` | method | `skills/hive_mind.py:679` | `def stats(self)` |
| `status` | method | `skills/hive_mind.py:1751` | `def status(self)` |
| `store` | method | `skills/hive_mind.py:153` | `def store(self, content)` |
| `store` | method | `skills/hive_mind.py:229` | `def store(self, content, agent_id, role, event_type, meta, session_tag)` |
| `store` | method | `skills/hive_mind.py:381` | `def store(self, content, agent_id, role, event_type, meta, session_tag, event_id)` |
| `store` | method | `skills/hive_mind.py:503` | `def store(self, content)` |
| `store` | method | `skills/hive_mind.py:584` | `def store(self, content, agent_id, role, event_type, meta, session_tag)` |
| `synthesize` | method | `skills/hive_mind.py:1359` | `def synthesize(self, drone_ids, original_goal)` |
| `upsert` | method | `skills/hive_mind.py:1436` | `def upsert(self, state)` |
| `AutoMapper` | class | `skills/lazyown_automapper.py:315` | `class AutoMapper` |
| `__init__` | method | `skills/lazyown_automapper.py:324` | `def __init__(self, lazyown_dir)` |
| `_addon_to_mcp_tool` | function | `skills/lazyown_automapper.py:249` | `def _addon_to_mcp_tool(spec)` |
| `_expand_tool_command` | function | `skills/lazyown_automapper.py:231` | `def _expand_tool_command(template, ip, port, ssl, outputdir, toolname)` |
| `_load_addons` | function | `skills/lazyown_automapper.py:133` | `def _load_addons(lazyaddons_dir)` |
| `_load_dottools` | function | `skills/lazyown_automapper.py:162` | `def _load_dottools(tools_dir)` |
| `_load_plugins` | function | `skills/lazyown_automapper.py:201` | `def _load_plugins(plugins_dir)` |
| `_load_yaml` | function | `skills/lazyown_automapper.py:76` | `def _load_yaml(path)` |
| `_params_to_schema` | function | `skills/lazyown_automapper.py:100` | `def _params_to_schema(params)` |
| `_plugin_to_mcp_tool` | function | `skills/lazyown_automapper.py:298` | `def _plugin_to_mcp_tool(spec)` |
| `_run_addon` | method | `skills/lazyown_automapper.py:407` | `def _run_addon(self, spec, arguments, config, run_fn)` |
| `_run_dottool` | method | `skills/lazyown_automapper.py:441` | `def _run_dottool(self, spec, arguments, config)` |
| `_run_plugin` | method | `skills/lazyown_automapper.py:465` | `def _run_plugin(self, spec, arguments, config, run_fn)` |
| `_safe_name` | function | `skills/lazyown_automapper.py:66` | `def _safe_name(raw)` |
| `_scan` | method | `skills/lazyown_automapper.py:333` | `def _scan(self)` |
| `_shell_run` | method | `skills/lazyown_automapper.py:495` | `def _shell_run(cmd, timeout)` |
| `_tool_to_mcp_tool` | function | `skills/lazyown_automapper.py:265` | `def _tool_to_mcp_tool(spec)` |
| `dispatch` | method | `skills/lazyown_automapper.py:376` | `def dispatch(self, name, arguments, config, run_command_fn)` |
| `list_specs` | method | `skills/lazyown_automapper.py:573` | `def list_specs(self)` |
| `mcp_tools` | method | `skills/lazyown_automapper.py:355` | `def mcp_tools(self)` |
| `rescan` | method | `skills/lazyown_automapper.py:351` | `def rescan(self)` |
| `stats` | method | `skills/lazyown_automapper.py:563` | `def stats(self)` |
| `update_skills_md` | method | `skills/lazyown_automapper.py:516` | `def update_skills_md(self, skills_md_path)` |
| `Campaign` | class | `skills/lazyown_campaign.py:105` | `class Campaign` |
| `CampaignStore` | class | `skills/lazyown_campaign.py:375` | `class CampaignStore` |
| `EpisodeReflectionEngine` | class | `skills/lazyown_campaign.py:193` | `class EpisodeReflectionEngine` |
| `LessonLearned` | class | `skills/lazyown_campaign.py:175` | `class LessonLearned` |
| `__init__` | method | `skills/lazyown_campaign.py:256` | `def __init__(self, hive_memory)` |
| `__init__` | method | `skills/lazyown_campaign.py:382` | `def __init__(self, campaign_file)` |
| `_build_parser` | method | `skills/lazyown_campaign.py:628` | `def _build_parser()` |
| `_now_iso` | function | `skills/lazyown_campaign.py:59` | `def _now_iso()` |
| `_persist_lessons` | method | `skills/lazyown_campaign.py:329` | `def _persist_lessons(self, lessons)` |
| `_require` | method | `skills/lazyown_campaign.py:614` | `def _require(self)` |
| `_save` | method | `skills/lazyown_campaign.py:388` | `def _save(self, campaign)` |
| `add_milestone` | method | `skills/lazyown_campaign.py:516` | `def add_milestone(self, host, milestone_type, notes)` |
| `add_to_scope` | method | `skills/lazyown_campaign.py:542` | `def add_to_scope(self, ip_or_cidr)` |
| `complete` | method | `skills/lazyown_campaign.py:445` | `def complete(self, notes, run_reflection, hive_memory)` |
| `create` | method | `skills/lazyown_campaign.py:414` | `def create(self, name, scope, notes)` |
| `from_dict` | method | `skills/lazyown_campaign.py:157` | `def from_dict(cls, data)` |
| `in_scope` | method | `skills/lazyown_campaign.py:561` | `def in_scope(self, ip)` |
| `is_active` | method | `skills/lazyown_campaign.py:148` | `def is_active(self)` |
| `is_ip_in_scope` | function | `skills/lazyown_campaign.py:64` | `def is_ip_in_scope(ip, scope)` |
| `load` | method | `skills/lazyown_campaign.py:395` | `def load(self)` |
| `main` | method | `skills/lazyown_campaign.py:672` | `def main(argv)` |
| `reflect` | method | `skills/lazyown_campaign.py:268` | `def reflect(self, campaign)` |
| `summary` | method | `skills/lazyown_campaign.py:568` | `def summary(self)` |
| `to_dict` | method | `skills/lazyown_campaign.py:152` | `def to_dict(self)` |
| `to_dict` | method | `skills/lazyown_campaign.py:189` | `def to_dict(self)` |
| `update_phase` | method | `skills/lazyown_campaign.py:500` | `def update_phase(self, host, phase)` |
| `ClaudeMdLoader` | class | `skills/lazyown_claudemd.py:24` | `class ClaudeMdLoader` |
| `__init__` | method | `skills/lazyown_claudemd.py:32` | `def __init__(self, cwd)` |
| `add_rule` | method | `skills/lazyown_claudemd.py:128` | `def add_rule(self, rule_name, content)` |
| `create_project_file` | method | `skills/lazyown_claudemd.py:121` | `def create_project_file(self, content, local)` |
| `create_user_file` | method | `skills/lazyown_claudemd.py:115` | `def create_user_file(self, content)` |
| `list_files` | method | `skills/lazyown_claudemd.py:90` | `def list_files(self)` |
| `load` | method | `skills/lazyown_claudemd.py:35` | `def load(self)` |
| `status_text` | method | `skills/lazyown_claudemd.py:136` | `def status_text(self)` |
| `CompactionResult` | class | `skills/lazyown_context.py:49` | `class CompactionResult` |
| `ContextCompactor` | class | `skills/lazyown_context.py:62` | `class ContextCompactor` |
| `__init__` | method | `skills/lazyown_context.py:72` | `def __init__(self, budget_override, snip_threshold, collapse_threshold)` |
| `apply_budget` | method | `skills/lazyown_context.py:84` | `def apply_budget(self, content, tool_name)` |
| `auto_compact_session` | method | `skills/lazyown_context.py:161` | `def auto_compact_session(entries)` |
| `collapse` | method | `skills/lazyown_context.py:138` | `def collapse(self, content, tool_name)` |
| `compact` | method | `skills/lazyown_context.py:205` | `def compact(self, content, tool_name)` |
| `compact_output` | method | `skills/lazyown_context.py:239` | `def compact_output(content, tool_name)` |
| `microcompact` | method | `skills/lazyown_context.py:122` | `def microcompact(self, content)` |
| `snip` | method | `skills/lazyown_context.py:101` | `def snip(self, content)` |
| `summary` | method | `skills/lazyown_context.py:56` | `def summary(self)` |
| `_Handler` | class | `skills/lazyown_daemon.py:191` | `class _Handler(FileSystemEventHandler)` |
| `_append_event` | method | `skills/lazyown_daemon.py:107` | `def _append_event(ev)` |
| `_clear_pid` | function | `skills/lazyown_daemon.py:419` | `def _clear_pid()` |
| `_dispatch` | method | `skills/lazyown_daemon.py:93` | `def _dispatch(path)` |
| `_is_running` | function | `skills/lazyown_daemon.py:431` | `def _is_running()` |
| `_main_async` | function | `skills/lazyown_daemon.py:383` | `def _main_async()` |
| `_poll_watcher_loop` | function | `skills/lazyown_daemon.py:156` | `def _poll_watcher_loop(queue)` |
| `_push` | method | `skills/lazyown_daemon.py:192` | `def _push(self, src)` |
| `_read_pid` | function | `skills/lazyown_daemon.py:424` | `def _read_pid()` |
| `_scan` | function | `skills/lazyown_daemon.py:160` | `def _scan()` |
| `_watchdog_async` | function | `skills/lazyown_daemon.py:187` | `def _watchdog_async(queue)` |
| `_write_pid` | function | `skills/lazyown_daemon.py:414` | `def _write_pid()` |
| `cmd_run` | function | `skills/lazyown_daemon.py:444` | `def cmd_run()` |
| `cmd_start` | function | `skills/lazyown_daemon.py:453` | `def cmd_start()` |
| `cmd_status` | function | `skills/lazyown_daemon.py:504` | `def cmd_status()` |
| `cmd_stop` | function | `skills/lazyown_daemon.py:486` | `def cmd_stop()` |
| `event_engine_loop` | function | `skills/lazyown_daemon.py:235` | `def event_engine_loop()` |
| `file_event_consumer` | function | `skills/lazyown_daemon.py:219` | `def file_event_consumer(queue)` |
| `file_watcher_loop` | function | `skills/lazyown_daemon.py:142` | `def file_watcher_loop(queue)` |
| `heartbeat_loop` | function | `skills/lazyown_daemon.py:274` | `def heartbeat_loop()` |
| `on_created` | method | `skills/lazyown_daemon.py:197` | `def on_created(self, event)` |
| `on_modified` | method | `skills/lazyown_daemon.py:201` | `def on_modified(self, event)` |
| `process_new_rows` | method | `skills/lazyown_daemon.py:104` | `def process_new_rows()` |
| `toposwarm_keepalive_loop` | function | `skills/lazyown_daemon.py:328` | `def toposwarm_keepalive_loop()` |
| `AccessFact` | class | `skills/lazyown_facts.py:97` | `class AccessFact` |
| `Config` | class | `skills/lazyown_facts.py:34` | `class Config` |
| `CrackMapExecParser` | class | `skills/lazyown_facts.py:238` | `class CrackMapExecParser(ITextOutputParser)` |
| `CredentialFact` | class | `skills/lazyown_facts.py:75` | `class CredentialFact` |
| `DiscoveredPath` | class | `skills/lazyown_facts.py:119` | `class DiscoveredPath` |
| `Enum4linuxParser` | class | `skills/lazyown_facts.py:288` | `class Enum4linuxParser(ITextOutputParser)` |
| `FactStore` | class | `skills/lazyown_facts.py:657` | `class FactStore` |
| `GenericOutputParser` | class | `skills/lazyown_facts.py:613` | `class GenericOutputParser(ITextOutputParser)` |
| `GobusterFfufParser` | class | `skills/lazyown_facts.py:445` | `class GobusterFfufParser(ITextOutputParser)` |
| `HostFacts` | class | `skills/lazyown_facts.py:130` | `class HostFacts` |
| `INmapXmlParser` | class | `skills/lazyown_facts.py:164` | `class INmapXmlParser` |
| `ITextOutputParser` | class | `skills/lazyown_facts.py:210` | `class ITextOutputParser` |
| `KerbruteParser` | class | `skills/lazyown_facts.py:393` | `class KerbruteParser(ITextOutputParser)` |
| `LdapParser` | class | `skills/lazyown_facts.py:364` | `class LdapParser(ITextOutputParser)` |
| `NiktoParser` | class | `skills/lazyown_facts.py:492` | `class NiktoParser(ITextOutputParser)` |
| `NucleiParser` | class | `skills/lazyown_facts.py:530` | `class NucleiParser(ITextOutputParser)` |
| `RpcclientParser` | class | `skills/lazyown_facts.py:421` | `class RpcclientParser(ITextOutputParser)` |
| `SecretsdumpParser` | class | `skills/lazyown_facts.py:327` | `class SecretsdumpParser(ITextOutputParser)` |
| `ServiceFact` | class | `skills/lazyown_facts.py:62` | `class ServiceFact` |
| `ShareFact` | class | `skills/lazyown_facts.py:87` | `class ShareFact` |
| `SslscanParser` | class | `skills/lazyown_facts.py:566` | `class SslscanParser(ITextOutputParser)` |
| `ToolDefinition` | class | `skills/lazyown_facts.py:1008` | `class ToolDefinition` |
| `VulnerabilityFact` | class | `skills/lazyown_facts.py:107` | `class VulnerabilityFact` |
| `__init__` | method | `skills/lazyown_facts.py:667` | `def __init__(self, cfg)` |
| `_cmd_clean` | method | `skills/lazyown_facts.py:1057` | `def _cmd_clean(_args)` |
| `_cmd_parse` | method | `skills/lazyown_facts.py:1043` | `def _cmd_parse(args)` |
| `_cmd_show` | method | `skills/lazyown_facts.py:1052` | `def _cmd_show(args)` |
| `_dedup_creds` | method | `skills/lazyown_facts.py:748` | `def _dedup_creds(self, hf)` |
| `_dedup_paths` | method | `skills/lazyown_facts.py:768` | `def _dedup_paths(self, hf)` |
| `_dedup_services` | method | `skills/lazyown_facts.py:738` | `def _dedup_services(self, hf)` |
| `_dedup_vulns` | method | `skills/lazyown_facts.py:758` | `def _dedup_vulns(self, hf)` |
| `_guess_host_from_filename` | method | `skills/lazyown_facts.py:830` | `def _guess_host_from_filename(filename)` |
| `_guess_port_from_path` | method | `skills/lazyown_facts.py:836` | `def _guess_port_from_path(txt_path)` |
| `_host` | method | `skills/lazyown_facts.py:733` | `def _host(self, ip)` |
| `_load` | method | `skills/lazyown_facts.py:691` | `def _load(self)` |
| `all_hosts` | method | `skills/lazyown_facts.py:882` | `def all_hosts(self)` |
| `can_parse` | method | `skills/lazyown_facts.py:215` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:254` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:299` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:339` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:372` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:401` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:429` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:457` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:502` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:538` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:574` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:627` | `def can_parse(self, filename, content)` |
| `context_for_command` | method | `skills/lazyown_facts.py:885` | `def context_for_command(self, host, category)` |
| `create_tool_file` | method | `skills/lazyown_facts.py:1017` | `def create_tool_file(toolname, command, trigger, active, tools_dir)` |
| `default` | method | `skills/lazyown_facts.py:45` | `def default(cls)` |
| `get_host` | method | `skills/lazyown_facts.py:879` | `def get_host(self, host)` |
| `highest_access` | method | `skills/lazyown_facts.py:143` | `def highest_access(self)` |
| `ingest_text` | method | `skills/lazyown_facts.py:792` | `def ingest_text(self, txt_path, host_hint)` |
| `ingest_xml` | method | `skills/lazyown_facts.py:780` | `def ingest_xml(self, xml_path)` |
| `main` | method | `skills/lazyown_facts.py:1066` | `def main()` |
| `open_ports` | method | `skills/lazyown_facts.py:154` | `def open_ports(self)` |
| `parse` | method | `skills/lazyown_facts.py:167` | `def parse(self, xml_path)` |
| `parse` | method | `skills/lazyown_facts.py:218` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:259` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:302` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:344` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:375` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:404` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:432` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:463` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:505` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:543` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:577` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:630` | `def parse(self, host, content, source_file)` |
| `parse_all` | method | `skills/lazyown_facts.py:848` | `def parse_all(self, target)` |
| `parse_extended` | method | `skills/lazyown_facts.py:226` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:466` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:508` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:546` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:580` | `def parse_extended(self, host, content, source_file, port)` |
| `save` | method | `skills/lazyown_facts.py:716` | `def save(self)` |
| `services_by_name` | method | `skills/lazyown_facts.py:157` | `def services_by_name(self, name)` |
| `summary` | method | `skills/lazyown_facts.py:978` | `def summary(self, host)` |
| `GroqAgentPool` | class | `skills/lazyown_groq_agents.py:714` | `class GroqAgentPool` |
| `_AgentState` | class | `skills/lazyown_groq_agents.py:682` | `class _AgentState` |
| `__init__` | method | `skills/lazyown_groq_agents.py:717` | `def __init__(self)` |
| `_agent_system_prompt` | method | `skills/lazyown_groq_agents.py:698` | `def _agent_system_prompt(tool_names)` |
| `_c2_req` | function | `skills/lazyown_groq_agents.py:76` | `def _c2_req(path, method, body)` |
| `_load_payload` | function | `skills/lazyown_groq_agents.py:54` | `def _load_payload()` |
| `_now_utc` | method | `skills/lazyown_groq_agents.py:694` | `def _now_utc()` |
| `_run` | method | `skills/lazyown_groq_agents.py:754` | `def _run(self, state, tools, api_key, max_iterations, system_prompt)` |
| `_run_cmd` | function | `skills/lazyown_groq_agents.py:61` | `def _run_cmd(command, timeout)` |
| `_t_atomic_search` | function | `skills/lazyown_groq_agents.py:442` | `def _t_atomic_search(keyword, mitre_id, platform, scope, complexity, has_prereqs, limit, include_command)` |
| `_t_bridge_catalog` | function | `skills/lazyown_groq_agents.py:118` | `def _t_bridge_catalog(phase, os_hint)` |
| `_t_bridge_suggest` | function | `skills/lazyown_groq_agents.py:91` | `def _t_bridge_suggest(phase, services, tag, os_hint)` |
| `_t_c2_command` | function | `skills/lazyown_groq_agents.py:303` | `def _t_c2_command(client_id, command)` |
| `_t_c2_status` | function | `skills/lazyown_groq_agents.py:298` | `def _t_c2_status()` |
| `_t_command_help` | function | `skills/lazyown_groq_agents.py:392` | `def _t_command_help(command)` |
| `_t_cve_lookup` | function | `skills/lazyown_groq_agents.py:206` | `def _t_cve_lookup(product, version)` |
| `_t_facts_show` | function | `skills/lazyown_groq_agents.py:198` | `def _t_facts_show(target)` |
| `_t_inject_objective` | function | `skills/lazyown_groq_agents.py:336` | `def _t_inject_objective(title, description)` |
| `_t_list_sessions` | function | `skills/lazyown_groq_agents.py:290` | `def _t_list_sessions()` |
| `_t_memory_search` | function | `skills/lazyown_groq_agents.py:229` | `def _t_memory_search(query)` |
| `_t_parquet_context` | function | `skills/lazyown_groq_agents.py:172` | `def _t_parquet_context(phase, target)` |
| `_t_rag_query` | function | `skills/lazyown_groq_agents.py:396` | `def _t_rag_query(query, n)` |
| `_t_reactive_suggest` | function | `skills/lazyown_groq_agents.py:348` | `def _t_reactive_suggest(output, command, platform)` |
| `_t_read_session_file` | function | `skills/lazyown_groq_agents.py:280` | `def _t_read_session_file(filename)` |
| `_t_run_command` | function | `skills/lazyown_groq_agents.py:87` | `def _t_run_command(command)` |
| `_t_searchsploit` | function | `skills/lazyown_groq_agents.py:371` | `def _t_searchsploit(query)` |
| `_t_session_status` | function | `skills/lazyown_groq_agents.py:255` | `def _t_session_status()` |
| `_t_task_add` | function | `skills/lazyown_groq_agents.py:325` | `def _t_task_add(title, description)` |
| `_t_task_list` | function | `skills/lazyown_groq_agents.py:309` | `def _t_task_list(filter_status)` |
| `_t_threat_model` | function | `skills/lazyown_groq_agents.py:416` | `def _t_threat_model(action)` |
| `agent_result` | method | `skills/lazyown_groq_agents.py:872` | `def agent_result(agent_id)` |
| `agent_status` | method | `skills/lazyown_groq_agents.py:868` | `def agent_status(agent_id)` |
| `get_pool` | method | `skills/lazyown_groq_agents.py:844` | `def get_pool()` |
| `list_agents` | method | `skills/lazyown_groq_agents.py:876` | `def list_agents(limit)` |
| `list_all` | method | `skills/lazyown_groq_agents.py:822` | `def list_all(self, limit)` |
| `main` | method | `skills/lazyown_groq_agents.py:882` | `def main()` |
| `result` | method | `skills/lazyown_groq_agents.py:809` | `def result(self, agent_id)` |
| `spawn` | method | `skills/lazyown_groq_agents.py:721` | `def spawn(self, goal, tools_filter, api_key, backend, max_iterations, system_prompt, block)` |
| `spawn_agent` | method | `skills/lazyown_groq_agents.py:853` | `def spawn_agent(goal, tools_filter, api_key, backend, max_iterations, block)` |
| `status` | method | `skills/lazyown_groq_agents.py:793` | `def status(self, agent_id)` |
| `HookEvent` | class | `skills/lazyown_hooks.py:27` | `class HookEvent(Enum)` |
| `HookRegistry` | class | `skills/lazyown_hooks.py:38` | `class HookRegistry` |
| `__init__` | method | `skills/lazyown_hooks.py:47` | `def __init__(self)` |
| `_audit` | method | `skills/lazyown_hooks.py:203` | `def _audit(ctx)` |
| `audit_hook` | method | `skills/lazyown_hooks.py:138` | `def audit_hook(context, audit_path)` |
| `build_default_registry` | method | `skills/lazyown_hooks.py:183` | `def build_default_registry(sessions_dir)` |
| `get_registry` | method | `skills/lazyown_hooks.py:218` | `def get_registry(sessions_dir)` |
| `metrics` | method | `skills/lazyown_hooks.py:79` | `def metrics(self)` |
| `rate_limit_hook` | method | `skills/lazyown_hooks.py:116` | `def rate_limit_hook(context, window, limit)` |
| `register` | method | `skills/lazyown_hooks.py:54` | `def register(self, event, handler)` |
| `run` | method | `skills/lazyown_hooks.py:57` | `def run(self, event, context)` |
| `sandbox_hook` | method | `skills/lazyown_hooks.py:101` | `def sandbox_hook(context)` |
| `start_timer_hook` | method | `skills/lazyown_hooks.py:174` | `def start_timer_hook(context)` |
| `timing_hook` | method | `skills/lazyown_hooks.py:160` | `def timing_hook(context)` |
| `LLMBridge` | class | `skills/lazyown_llm.py:97` | `class LLMBridge` |
| `LLMTool` | class | `skills/lazyown_llm.py:71` | `class LLMTool` |
| `__init__` | method | `skills/lazyown_llm.py:104` | `def __init__(self, backend, model, api_key)` |
| `_ask_groq` | method | `skills/lazyown_llm.py:141` | `def _ask_groq(self, goal, context, max_iterations, system_prompt)` |
| `_ask_ollama_react` | method | `skills/lazyown_llm.py:239` | `def _ask_ollama_react(self, goal, context, max_iterations, system_prompt)` |
| `_call_tool` | method | `skills/lazyown_llm.py:322` | `def _call_tool(self, name, args)` |
| `_default_system_prompt` | method | `skills/lazyown_llm.py:458` | `def _default_system_prompt(tool_names)` |
| `_groq_request` | method | `skills/lazyown_llm.py:202` | `def _groq_request(self, messages, tools)` |
| `_make_default_tools` | method | `skills/lazyown_llm.py:338` | `def _make_default_tools(bridge)` |
| `_ollama_generate` | method | `skills/lazyown_llm.py:308` | `def _ollama_generate(self, prompt)` |
| `ask` | method | `skills/lazyown_llm.py:128` | `def ask(self, goal, context, max_iterations, system_prompt)` |
| `build_bridge` | method | `skills/lazyown_llm.py:441` | `def build_bridge(backend, model, api_key, with_default_tools)` |
| `llm_ask` | method | `skills/lazyown_llm.py:471` | `def llm_ask(goal, context, backend, model, api_key, max_iterations, system_prompt, extra_tools)` |
| `main` | method | `skills/lazyown_llm.py:497` | `def main()` |
| `openai_schema` | method | `skills/lazyown_llm.py:79` | `def openai_schema(self)` |
| `read_facts` | method | `skills/lazyown_llm.py:378` | `def read_facts(target)` |
| `read_nmap` | method | `skills/lazyown_llm.py:355` | `def read_nmap(target)` |
| `read_objectives` | method | `skills/lazyown_llm.py:390` | `def read_objectives(limit)` |
| `read_plan` | method | `skills/lazyown_llm.py:371` | `def read_plan()` |
| `register_tool` | method | `skills/lazyown_llm.py:118` | `def register_tool(self, name, description, parameters, func)` |
| `run_command` | method | `skills/lazyown_llm.py:350` | `def run_command(command)` |
| `_add` | function | `skills/lazyown_mcp.py:1385` | `def _add(user, secret, host, source, confirmed)` |
| `_advance_phase_wm` | function | `skills/lazyown_mcp.py:8748` | `def _advance_phase_wm()` |
| `_blocking_run` | function | `skills/lazyown_mcp.py:9670` | `def _blocking_run()` |
| `_bootstrap_sequence` | function | `skills/lazyown_mcp.py:8107` | `def _bootstrap_sequence()` |
| `_build_command_from_facts` | function | `skills/lazyown_mcp.py:8218` | `def _build_command_from_facts(category, resolved_cmd, resolved_args, tgt)` |
| `_c2_creds` | function | `skills/lazyown_mcp.py:542` | `def _c2_creds()` |
| `_c2_request` | function | `skills/lazyown_mcp.py:552` | `def _c2_request(path, method, body)` |
| `_compact` | function | `skills/lazyown_mcp.py:408` | `def _compact(content, tool_name)` |
| `_compact_output_fn` | function | `skills/lazyown_mcp.py:416` | `def _compact_output_fn(c, t)` |
| `_create_tool_file` | function | `skills/lazyown_mcp.py:179` | `def _create_tool_file()` |
| `_decorator` | function | `skills/lazyown_mcp.py:593` | `def _decorator(func)` |
| `_deploy_beacon_sync` | function | `skills/lazyown_mcp.py:10363` | `def _deploy_beacon_sync()` |
| `_dispatch_perm_check` | function | `skills/lazyown_mcp.py:612` | `def _dispatch_perm_check(name, arguments)` |
| `_do_facts` | function | `skills/lazyown_mcp.py:1448` | `def _do_facts()` |
| `_ensure_aci` | function | `skills/lazyown_mcp.py:325` | `def _ensure_aci()` |
| `_ensure_auto` | function | `skills/lazyown_mcp.py:298` | `def _ensure_auto()` |
| `_ensure_automapper` | function | `skills/lazyown_mcp.py:230` | `def _ensure_automapper()` |
| `_ensure_bridge` | function | `skills/lazyown_mcp.py:94` | `def _ensure_bridge()` |
| `_ensure_engine` | function | `skills/lazyown_mcp.py:72` | `def _ensure_engine()` |
| `_ensure_facts` | function | `skills/lazyown_mcp.py:166` | `def _ensure_facts()` |
| `_ensure_hive` | function | `skills/lazyown_mcp.py:258` | `def _ensure_hive()` |
| `_ensure_llm` | function | `skills/lazyown_mcp.py:216` | `def _ensure_llm()` |
| `_ensure_narrator` | function | `skills/lazyown_mcp.py:139` | `def _ensure_narrator()` |
| `_ensure_objectives` | function | `skills/lazyown_mcp.py:184` | `def _ensure_objectives()` |
| `_ensure_pdb` | function | `skills/lazyown_mcp.py:243` | `def _ensure_pdb()` |
| `_ensure_policy` | function | `skills/lazyown_mcp.py:153` | `def _ensure_policy()` |
| `_ensure_recommender` | function | `skills/lazyown_mcp.py:126` | `def _ensure_recommender()` |
| `_ensure_state` | function | `skills/lazyown_mcp.py:112` | `def _ensure_state()` |
| `_execute_step` | function | `skills/lazyown_mcp.py:8254` | `def _execute_step()` |
| `_fail` | function | `skills/lazyown_mcp.py:936` | `def _fail(message, remediation)` |
| `_fused_recommendations` | function | `skills/lazyown_mcp.py:7709` | `def _fused_recommendations()` |
| `_generate_tasks_from_sessions` | function | `skills/lazyown_mcp.py:7941` | `def _generate_tasks_from_sessions(tgt, platform, api_key)` |
| `_get_claudemd` | function | `skills/lazyown_mcp.py:421` | `def _get_claudemd()` |
| `_get_hooks` | function | `skills/lazyown_mcp.py:384` | `def _get_hooks()` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:253` | `def _get_pdb(_)` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:353` | `def _get_pdb(_)` |
| `_get_perm_system` | function | `skills/lazyown_mcp.py:372` | `def _get_perm_system()` |
| `_get_transcript` | function | `skills/lazyown_mcp.py:396` | `def _get_transcript()` |
| `_h_auto_pwn` | function | `skills/lazyown_mcp.py:1143` | `def _h_auto_pwn(arguments, tool_name)` |
| `_h_credentials` | function | `skills/lazyown_mcp.py:1380` | `def _h_credentials(arguments, tool_name)` |
| `_h_dashboard_snapshot` | function | `skills/lazyown_mcp.py:1104` | `def _h_dashboard_snapshot(arguments, tool_name)` |
| `_h_db` | function | `skills/lazyown_mcp.py:652` | `def _h_db(arguments, tool_name)` |
| `_h_evasion_generate` | function | `skills/lazyown_mcp.py:1061` | `def _h_evasion_generate(arguments, tool_name)` |
| `_h_evasion_rotate` | function | `skills/lazyown_mcp.py:1074` | `def _h_evasion_rotate(arguments, tool_name)` |
| `_h_exploit_chain` | function | `skills/lazyown_mcp.py:1175` | `def _h_exploit_chain(arguments, tool_name)` |
| `_h_exploit_recommend` | function | `skills/lazyown_mcp.py:1039` | `def _h_exploit_recommend(arguments, tool_name)` |
| `_h_exploitgym_list` | function | `skills/lazyown_mcp.py:1472` | `def _h_exploitgym_list(arguments, tool_name)` |
| `_h_exploitgym_run` | function | `skills/lazyown_mcp.py:1488` | `def _h_exploitgym_run(arguments, tool_name)` |
| `_h_exploitgym_score` | function | `skills/lazyown_mcp.py:1508` | `def _h_exploitgym_score(arguments, tool_name)` |
| `_h_exploitgym_status` | function | `skills/lazyown_mcp.py:1458` | `def _h_exploitgym_status(arguments, tool_name)` |
| `_h_facts_show` | function | `skills/lazyown_mcp.py:1438` | `def _h_facts_show(arguments, tool_name)` |
| `_h_get_beacons` | function | `skills/lazyown_mcp.py:1135` | `def _h_get_beacons(arguments, tool_name)` |
| `_h_get_config` | function | `skills/lazyown_mcp.py:646` | `def _h_get_config(arguments, tool_name)` |
| `_h_get_llm_budget` | function | `skills/lazyown_mcp.py:762` | `def _h_get_llm_budget(arguments, tool_name)` |
| `_h_inject_objective` | function | `skills/lazyown_mcp.py:1360` | `def _h_inject_objective(arguments, tool_name)` |
| `_h_list_modules` | function | `skills/lazyown_mcp.py:820` | `def _h_list_modules(arguments, tool_name)` |
| `_h_lolbas_list` | function | `skills/lazyown_mcp.py:1234` | `def _h_lolbas_list(arguments, tool_name)` |
| `_h_lolbas_use` | function | `skills/lazyown_mcp.py:1268` | `def _h_lolbas_use(arguments, tool_name)` |
| `_h_pivot_status` | function | `skills/lazyown_mcp.py:1086` | `def _h_pivot_status(arguments, tool_name)` |
| `_h_rea` | function | `skills/lazyown_mcp.py:924` | `def _h_rea(arguments, tool_name)` |
| `_h_rich_tui_snapshot` | function | `skills/lazyown_mcp.py:1332` | `def _h_rich_tui_snapshot(arguments, tool_name)` |
| `_h_run_command` | function | `skills/lazyown_mcp.py:841` | `def _h_run_command(arguments, tool_name)` |
| `_h_set_config` | function | `skills/lazyown_mcp.py:799` | `def _h_set_config(arguments, tool_name)` |
| `_h_stealth` | function | `skills/lazyown_mcp.py:1309` | `def _h_stealth(arguments, tool_name)` |
| `_h_unified_dashboard` | function | `skills/lazyown_mcp.py:1123` | `def _h_unified_dashboard(arguments, tool_name)` |
| `_handle_messages` | function | `skills/lazyown_mcp.py:11275` | `def _handle_messages(scope, receive, send)` |
| `_handle_sighup` | function | `skills/lazyown_mcp.py:11243` | `def _handle_sighup(signum, frame)` |
| `_handle_sse` | function | `skills/lazyown_mcp.py:11269` | `def _handle_sse(request)` |
| `_has_data` | function | `skills/lazyown_mcp.py:527` | `def _has_data(path)` |
| `_is_placeholder` | function | `skills/lazyown_mcp.py:8316` | `def _is_placeholder(val)` |
| `_is_placeholder` | function | `skills/lazyown_mcp.py:8581` | `def _is_placeholder(val)` |
| `_isolated_runner` | function | `skills/lazyown_mcp.py:11148` | `def _isolated_runner(cmd)` |
| `_launch` | function | `skills/lazyown_mcp.py:10721` | `def _launch()` |
| `_load_category_command_map` | function | `skills/lazyown_mcp.py:473` | `def _load_category_command_map()` |
| `_load_crons` | function | `skills/lazyown_mcp.py:10266` | `def _load_crons()` |
| `_load_payload` | function | `skills/lazyown_mcp.py:518` | `def _load_payload()` |
| `_make_text` | function | `skills/lazyown_mcp.py:600` | `def _make_text(tool_name, content)` |
| `_mark_task_done` | function | `skills/lazyown_mcp.py:8090` | `def _mark_task_done(task_id, outcome)` |
| `_mcp_executor` | function | `skills/lazyown_mcp.py:9058` | `def _mcp_executor(command, target)` |
| `_next_pending_task` | function | `skills/lazyown_mcp.py:8061` | `def _next_pending_task()` |
| `_parquet_candidates` | function | `skills/lazyown_mcp.py:8157` | `def _parquet_candidates(category, tgt)` |
| `_read_docstring` | function | `skills/lazyown_mcp.py:6848` | `def _read_docstring(cmd_name)` |
| `_read_os_json` | function | `skills/lazyown_mcp.py:7910` | `def _read_os_json()` |
| `_read_prompt` | function | `skills/lazyown_mcp.py:8918` | `def _read_prompt()` |
| `_refresh_facts` | function | `skills/lazyown_mcp.py:8210` | `def _refresh_facts(tgt)` |
| `_result` | function | `skills/lazyown_mcp.py:672` | `def _result(payload)` |
| `_run_campaign` | function | `skills/lazyown_mcp.py:10571` | `def _run_campaign()` |
| `_run_daemon` | function | `skills/lazyown_mcp.py:10640` | `def _run_daemon()` |
| `_run_lazyown_command` | function | `skills/lazyown_mcp.py:1526` | `def _run_lazyown_command(command, timeout)` |
| `_run_parquet_query` | function | `skills/lazyown_mcp.py:10505` | `def _run_parquet_query()` |
| `_run_pwntomate_if_xml_ready` | function | `skills/lazyown_mcp.py:8177` | `def _run_pwntomate_if_xml_ready(tgt)` |
| `_run_rea` | function | `skills/lazyown_mcp.py:1012` | `def _run_rea()` |
| `_run_with_fallback` | function | `skills/lazyown_mcp.py:858` | `def _run_with_fallback(cmd, to)` |
| `_run_with_fallback` | function | `skills/lazyown_mcp.py:5626` | `def _run_with_fallback(cmd, to)` |
| `_runner` | function | `skills/lazyown_mcp.py:5959` | `def _runner(cmd)` |
| `_save_crons` | function | `skills/lazyown_mcp.py:10276` | `def _save_crons(entries)` |
| `_save_payload` | function | `skills/lazyown_mcp.py:532` | `def _save_payload(data)` |
| `_wait_for_nmap_xml` | function | `skills/lazyown_mcp.py:7922` | `def _wait_for_nmap_xml(tgt, timeout_s)` |
| `call_tool` | function | `skills/lazyown_mcp.py:5545` | `def call_tool(name, arguments)` |
| `coerce_value` | function | `skills/lazyown_mcp.py:807` | `def coerce_value(k, v)` |
| `list_tools` | function | `skills/lazyown_mcp.py:1627` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp.py:11252` | `def main()` |
| `register_handler` | function | `skills/lazyown_mcp.py:586` | `def register_handler(tool_name)` |
| `substitute_playbook_target` | function | `skills/lazyown_mcp.py:5527` | `def substitute_playbook_target(command, target)` |
| `text` | function | `skills/lazyown_mcp.py:5555` | `def text(content)` |
| `JobRecord` | class | `skills/lazyown_mcp_helpers.py:634` | `class JobRecord` |
| `JobStore` | class | `skills/lazyown_mcp_helpers.py:648` | `class JobStore` |
| `TaskAudit` | class | `skills/lazyown_mcp_helpers.py:153` | `class TaskAudit` |
| `__init__` | method | `skills/lazyown_mcp_helpers.py:651` | `def __init__(self, max_jobs)` |
| `_format_age` | function | `skills/lazyown_mcp_helpers.py:112` | `def _format_age(seconds)` |
| `_worker` | method | `skills/lazyown_mcp_helpers.py:671` | `def _worker()` |
| `audit_tasks` | method | `skills/lazyown_mcp_helpers.py:165` | `def audit_tasks(tasks, min_confidence)` |
| `build_target_context` | method | `skills/lazyown_mcp_helpers.py:395` | `def build_target_context(host, port, sessions_dir, payload, world_model)` |
| `collect_pwntomate_evidence` | method | `skills/lazyown_mcp_helpers.py:359` | `def collect_pwntomate_evidence(rhost, sessions_dir)` |

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
