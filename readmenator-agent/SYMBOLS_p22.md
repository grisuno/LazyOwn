# Symbols (page 22 of 40)
Previous: [SYMBOLS_p21.md](SYMBOLS_p21.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `receive` | method | `skills/hive_mind.py:746` | `def receive(self, agent_id, max_msgs)` |
| `recover_from_store` | method | `skills/hive_mind.py:1687` | `def recover_from_store(self)` |
| `requeue_interrupted` | method | `skills/hive_mind.py:1741` | `def requeue_interrupted(self, backend, api_key, max_iterations)` |
| `run` | method | `skills/hive_mind.py:175` | `def run(self, command, timeout)` |
| `spawn` | method | `skills/hive_mind.py:1708` | `def spawn(self, role, goal, backend, api_key, model, max_iterations, runner)` |
| `spawn` | method | `skills/hive_mind.py:1829` | `def spawn(self, goal, role, backend, api_key, max_iterations)` |
| `spawn_hive` | method | `skills/hive_mind.py:1846` | `def spawn_hive(self, goal, n_drones, backend, api_key, max_iterations)` |
| `start` | method | `skills/hive_mind.py:1128` | `def start(self)` |
| `stats` | method | `skills/hive_mind.py:322` | `def stats(self)` |
| `stats` | method | `skills/hive_mind.py:694` | `def stats(self)` |
| `status` | method | `skills/hive_mind.py:1863` | `def status(self)` |
| `store` | method | `skills/hive_mind.py:157` | `def store(self, content)` |
| `store` | method | `skills/hive_mind.py:235` | `def store(self, content, agent_id, role, event_type, meta, session_tag)` |
| `store` | method | `skills/hive_mind.py:386` | `def store(self, content, agent_id, role, event_type, meta, session_tag, event_id)` |
| `store` | method | `skills/hive_mind.py:515` | `def store(self, content)` |
| `store` | method | `skills/hive_mind.py:596` | `def store(self, content, agent_id, role, event_type, meta, session_tag)` |
| `synthesize` | method | `skills/hive_mind.py:1447` | `def synthesize(self, drone_ids, original_goal)` |
| `upsert` | method | `skills/hive_mind.py:1523` | `def upsert(self, state)` |
| `AutoMapper` | class | `skills/lazyown_automapper.py:332` | `class AutoMapper` |
| `__init__` | method | `skills/lazyown_automapper.py:341` | `def __init__(self, lazyown_dir)` |
| `_addon_to_mcp_tool` | function | `skills/lazyown_automapper.py:265` | `def _addon_to_mcp_tool(spec)` |
| `_expand_tool_command` | function | `skills/lazyown_automapper.py:247` | `def _expand_tool_command(template, ip, port, ssl, outputdir, toolname)` |
| `_load_addons` | function | `skills/lazyown_automapper.py:142` | `def _load_addons(lazyaddons_dir)` |
| `_load_dottools` | function | `skills/lazyown_automapper.py:173` | `def _load_dottools(tools_dir)` |
| `_load_plugins` | function | `skills/lazyown_automapper.py:214` | `def _load_plugins(plugins_dir)` |
| `_load_yaml` | function | `skills/lazyown_automapper.py:79` | `def _load_yaml(path)` |
| `_params_to_schema` | function | `skills/lazyown_automapper.py:104` | `def _params_to_schema(params)` |
| `_plugin_to_mcp_tool` | function | `skills/lazyown_automapper.py:314` | `def _plugin_to_mcp_tool(spec)` |
| `_run_addon` | method | `skills/lazyown_automapper.py:420` | `def _run_addon(self, spec, arguments, config, run_fn)` |
| `_run_dottool` | method | `skills/lazyown_automapper.py:452` | `def _run_dottool(self, spec, arguments, config)` |
| `_run_plugin` | method | `skills/lazyown_automapper.py:475` | `def _run_plugin(self, spec, arguments, config, run_fn)` |
| `_safe_name` | function | `skills/lazyown_automapper.py:68` | `def _safe_name(raw)` |
| `_scan` | method | `skills/lazyown_automapper.py:350` | `def _scan(self)` |
| `_shell_run` | method | `skills/lazyown_automapper.py:503` | `def _shell_run(cmd, timeout)` |
| `_tool_to_mcp_tool` | function | `skills/lazyown_automapper.py:281` | `def _tool_to_mcp_tool(spec)` |
| `dispatch` | method | `skills/lazyown_automapper.py:389` | `def dispatch(self, name, arguments, config, run_command_fn)` |
| `list_specs` | method | `skills/lazyown_automapper.py:581` | `def list_specs(self)` |
| `mcp_tools` | method | `skills/lazyown_automapper.py:368` | `def mcp_tools(self)` |
| `rescan` | method | `skills/lazyown_automapper.py:364` | `def rescan(self)` |
| `stats` | method | `skills/lazyown_automapper.py:571` | `def stats(self)` |
| `update_skills_md` | method | `skills/lazyown_automapper.py:524` | `def update_skills_md(self, skills_md_path)` |
| `Campaign` | class | `skills/lazyown_campaign.py:105` | `class Campaign` |
| `CampaignStore` | class | `skills/lazyown_campaign.py:375` | `class CampaignStore` |
| `EpisodeReflectionEngine` | class | `skills/lazyown_campaign.py:193` | `class EpisodeReflectionEngine` |
| `LessonLearned` | class | `skills/lazyown_campaign.py:175` | `class LessonLearned` |
| `__init__` | method | `skills/lazyown_campaign.py:256` | `def __init__(self, hive_memory)` |
| `__init__` | method | `skills/lazyown_campaign.py:382` | `def __init__(self, campaign_file)` |
| `_build_parser` | function | `skills/lazyown_campaign.py:623` | `def _build_parser()` |
| `_now_iso` | function | `skills/lazyown_campaign.py:59` | `def _now_iso()` |
| `_persist_lessons` | method | `skills/lazyown_campaign.py:332` | `def _persist_lessons(self, lessons)` |
| `_require` | method | `skills/lazyown_campaign.py:610` | `def _require(self)` |
| `_save` | method | `skills/lazyown_campaign.py:388` | `def _save(self, campaign)` |
| `add_milestone` | method | `skills/lazyown_campaign.py:516` | `def add_milestone(self, host, milestone_type, notes)` |
| `add_to_scope` | method | `skills/lazyown_campaign.py:540` | `def add_to_scope(self, ip_or_cidr)` |
| `complete` | method | `skills/lazyown_campaign.py:445` | `def complete(self, notes, run_reflection, hive_memory)` |
| `create` | method | `skills/lazyown_campaign.py:414` | `def create(self, name, scope, notes)` |
| `from_dict` | method | `skills/lazyown_campaign.py:157` | `def from_dict(cls, data)` |
| `in_scope` | method | `skills/lazyown_campaign.py:559` | `def in_scope(self, ip)` |
| `is_active` | method | `skills/lazyown_campaign.py:148` | `def is_active(self)` |
| `is_ip_in_scope` | function | `skills/lazyown_campaign.py:64` | `def is_ip_in_scope(ip, scope)` |
| `load` | method | `skills/lazyown_campaign.py:395` | `def load(self)` |
| `main` | function | `skills/lazyown_campaign.py:667` | `def main(argv)` |
| `reflect` | method | `skills/lazyown_campaign.py:268` | `def reflect(self, campaign)` |
| `summary` | method | `skills/lazyown_campaign.py:566` | `def summary(self)` |
| `to_dict` | method | `skills/lazyown_campaign.py:152` | `def to_dict(self)` |
| `to_dict` | method | `skills/lazyown_campaign.py:189` | `def to_dict(self)` |
| `update_phase` | method | `skills/lazyown_campaign.py:500` | `def update_phase(self, host, phase)` |
| `ClaudeMdLoader` | class | `skills/lazyown_claudemd.py:24` | `class ClaudeMdLoader` |
| `__init__` | method | `skills/lazyown_claudemd.py:32` | `def __init__(self, cwd)` |
| `add_rule` | method | `skills/lazyown_claudemd.py:127` | `def add_rule(self, rule_name, content)` |
| `create_project_file` | method | `skills/lazyown_claudemd.py:121` | `def create_project_file(self, content, local)` |
| `create_user_file` | method | `skills/lazyown_claudemd.py:115` | `def create_user_file(self, content)` |
| `list_files` | method | `skills/lazyown_claudemd.py:90` | `def list_files(self)` |
| `load` | method | `skills/lazyown_claudemd.py:35` | `def load(self)` |
| `status_text` | method | `skills/lazyown_claudemd.py:135` | `def status_text(self)` |
| `CompactionResult` | class | `skills/lazyown_context.py:50` | `class CompactionResult` |
| `ContextCompactor` | class | `skills/lazyown_context.py:62` | `class ContextCompactor` |
| `__init__` | method | `skills/lazyown_context.py:72` | `def __init__(self, budget_override, snip_threshold, collapse_threshold)` |
| `apply_budget` | method | `skills/lazyown_context.py:84` | `def apply_budget(self, content, tool_name)` |
| `auto_compact_session` | method | `skills/lazyown_context.py:159` | `def auto_compact_session(entries)` |
| `collapse` | method | `skills/lazyown_context.py:136` | `def collapse(self, content, tool_name)` |
| `compact` | method | `skills/lazyown_context.py:203` | `def compact(self, content, tool_name)` |
| `compact_output` | function | `skills/lazyown_context.py:237` | `def compact_output(content, tool_name)` |
| `microcompact` | method | `skills/lazyown_context.py:120` | `def microcompact(self, content)` |
| `snip` | method | `skills/lazyown_context.py:99` | `def snip(self, content)` |
| `summary` | method | `skills/lazyown_context.py:57` | `def summary(self)` |
| `_Handler` | class | `skills/lazyown_daemon.py:197` | `class _Handler(FileSystemEventHandler)` |
| `_append_event` | function | `skills/lazyown_daemon.py:111` | `def _append_event(ev)` |
| `_clear_pid` | function | `skills/lazyown_daemon.py:427` | `def _clear_pid()` |
| `_dispatch` | function | `skills/lazyown_daemon.py:95` | `def _dispatch(path)` |
| `_is_running` | function | `skills/lazyown_daemon.py:439` | `def _is_running()` |
| `_main_async` | function | `skills/lazyown_daemon.py:390` | `def _main_async()` |
| `_poll_watcher_loop` | function | `skills/lazyown_daemon.py:163` | `def _poll_watcher_loop(queue)` |
| `_push` | method | `skills/lazyown_daemon.py:198` | `def _push(self, src)` |
| `_read_pid` | function | `skills/lazyown_daemon.py:432` | `def _read_pid()` |
| `_scan` | function | `skills/lazyown_daemon.py:167` | `def _scan()` |
| `_watchdog_async` | function | `skills/lazyown_daemon.py:193` | `def _watchdog_async(queue)` |
| `_write_pid` | function | `skills/lazyown_daemon.py:422` | `def _write_pid()` |
| `cmd_run` | function | `skills/lazyown_daemon.py:453` | `def cmd_run()` |
| `cmd_start` | function | `skills/lazyown_daemon.py:462` | `def cmd_start()` |
| `cmd_status` | function | `skills/lazyown_daemon.py:513` | `def cmd_status()` |
| `cmd_stop` | function | `skills/lazyown_daemon.py:495` | `def cmd_stop()` |
| `event_engine_loop` | function | `skills/lazyown_daemon.py:240` | `def event_engine_loop()` |
| `file_event_consumer` | function | `skills/lazyown_daemon.py:223` | `def file_event_consumer(queue)` |
| `file_watcher_loop` | function | `skills/lazyown_daemon.py:150` | `def file_watcher_loop(queue)` |
| `heartbeat_loop` | function | `skills/lazyown_daemon.py:280` | `def heartbeat_loop()` |
| `on_created` | method | `skills/lazyown_daemon.py:201` | `def on_created(self, event)` |
| `on_modified` | method | `skills/lazyown_daemon.py:205` | `def on_modified(self, event)` |
| `process_new_rows` | function | `skills/lazyown_daemon.py:108` | `def process_new_rows()` |
| `toposwarm_keepalive_loop` | function | `skills/lazyown_daemon.py:332` | `def toposwarm_keepalive_loop()` |
| `AccessFact` | class | `skills/lazyown_facts.py:97` | `class AccessFact` |
| `Config` | class | `skills/lazyown_facts.py:34` | `class Config` |
| `CrackMapExecParser` | class | `skills/lazyown_facts.py:240` | `class CrackMapExecParser(ITextOutputParser)` |
| `CredentialFact` | class | `skills/lazyown_facts.py:75` | `class CredentialFact` |
| `DiscoveredPath` | class | `skills/lazyown_facts.py:120` | `class DiscoveredPath` |
| `Enum4linuxParser` | class | `skills/lazyown_facts.py:292` | `class Enum4linuxParser(ITextOutputParser)` |
| `FactStore` | class | `skills/lazyown_facts.py:667` | `class FactStore` |
| `GenericOutputParser` | class | `skills/lazyown_facts.py:625` | `class GenericOutputParser(ITextOutputParser)` |
| `GobusterFfufParser` | class | `skills/lazyown_facts.py:435` | `class GobusterFfufParser(ITextOutputParser)` |
| `HostFacts` | class | `skills/lazyown_facts.py:132` | `class HostFacts` |
| `INmapXmlParser` | class | `skills/lazyown_facts.py:166` | `class INmapXmlParser` |
| `ITextOutputParser` | class | `skills/lazyown_facts.py:212` | `class ITextOutputParser` |
| `KerbruteParser` | class | `skills/lazyown_facts.py:395` | `class KerbruteParser(ITextOutputParser)` |
| `LdapParser` | class | `skills/lazyown_facts.py:366` | `class LdapParser(ITextOutputParser)` |
| `NiktoParser` | class | `skills/lazyown_facts.py:494` | `class NiktoParser(ITextOutputParser)` |
| `NucleiParser` | class | `skills/lazyown_facts.py:537` | `class NucleiParser(ITextOutputParser)` |
| `RpcclientParser` | class | `skills/lazyown_facts.py:416` | `class RpcclientParser(ITextOutputParser)` |
| `SecretsdumpParser` | class | `skills/lazyown_facts.py:331` | `class SecretsdumpParser(ITextOutputParser)` |
| `ServiceFact` | class | `skills/lazyown_facts.py:62` | `class ServiceFact` |
| `ShareFact` | class | `skills/lazyown_facts.py:87` | `class ShareFact` |
| `SslscanParser` | class | `skills/lazyown_facts.py:573` | `class SslscanParser(ITextOutputParser)` |
| `ToolDefinition` | class | `skills/lazyown_facts.py:1016` | `class ToolDefinition` |
| `VulnerabilityFact` | class | `skills/lazyown_facts.py:107` | `class VulnerabilityFact` |
| `__init__` | method | `skills/lazyown_facts.py:677` | `def __init__(self, cfg)` |
| `_cmd_clean` | function | `skills/lazyown_facts.py:1065` | `def _cmd_clean(_args)` |
| `_cmd_parse` | function | `skills/lazyown_facts.py:1051` | `def _cmd_parse(args)` |
| `_cmd_show` | function | `skills/lazyown_facts.py:1060` | `def _cmd_show(args)` |
| `_dedup_creds` | method | `skills/lazyown_facts.py:759` | `def _dedup_creds(self, hf)` |
| `_dedup_paths` | method | `skills/lazyown_facts.py:779` | `def _dedup_paths(self, hf)` |
| `_dedup_services` | method | `skills/lazyown_facts.py:749` | `def _dedup_services(self, hf)` |
| `_dedup_vulns` | method | `skills/lazyown_facts.py:769` | `def _dedup_vulns(self, hf)` |
| `_guess_host_from_filename` | method | `skills/lazyown_facts.py:841` | `def _guess_host_from_filename(filename)` |
| `_guess_port_from_path` | method | `skills/lazyown_facts.py:847` | `def _guess_port_from_path(txt_path)` |
| `_host` | method | `skills/lazyown_facts.py:744` | `def _host(self, ip)` |
| `_load` | method | `skills/lazyown_facts.py:702` | `def _load(self)` |
| `all_hosts` | method | `skills/lazyown_facts.py:893` | `def all_hosts(self)` |
| `can_parse` | method | `skills/lazyown_facts.py:217` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:250` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:301` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:341` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:374` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:403` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:424` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:447` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:502` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:545` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:581` | `def can_parse(self, filename, content)` |
| `can_parse` | method | `skills/lazyown_facts.py:635` | `def can_parse(self, filename, content)` |
| `context_for_command` | method | `skills/lazyown_facts.py:896` | `def context_for_command(self, host, category)` |
| `create_tool_file` | function | `skills/lazyown_facts.py:1025` | `def create_tool_file(toolname, command, trigger, active, tools_dir)` |
| `default` | method | `skills/lazyown_facts.py:45` | `def default(cls)` |
| `get_host` | method | `skills/lazyown_facts.py:890` | `def get_host(self, host)` |
| `highest_access` | method | `skills/lazyown_facts.py:145` | `def highest_access(self)` |
| `ingest_text` | method | `skills/lazyown_facts.py:803` | `def ingest_text(self, txt_path, host_hint)` |
| `ingest_xml` | method | `skills/lazyown_facts.py:791` | `def ingest_xml(self, xml_path)` |
| `main` | function | `skills/lazyown_facts.py:1074` | `def main()` |
| `open_ports` | method | `skills/lazyown_facts.py:156` | `def open_ports(self)` |
| `parse` | method | `skills/lazyown_facts.py:169` | `def parse(self, xml_path)` |
| `parse` | method | `skills/lazyown_facts.py:220` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:257` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:304` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:346` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:377` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:406` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:427` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:450` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:505` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:548` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:584` | `def parse(self, host, content, source_file)` |
| `parse` | method | `skills/lazyown_facts.py:638` | `def parse(self, host, content, source_file)` |
| `parse_all` | method | `skills/lazyown_facts.py:859` | `def parse_all(self, target)` |
| `parse_extended` | method | `skills/lazyown_facts.py:228` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:453` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:508` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:551` | `def parse_extended(self, host, content, source_file, port)` |
| `parse_extended` | method | `skills/lazyown_facts.py:587` | `def parse_extended(self, host, content, source_file, port)` |
| `save` | method | `skills/lazyown_facts.py:727` | `def save(self)` |
| `services_by_name` | method | `skills/lazyown_facts.py:159` | `def services_by_name(self, name)` |
| `summary` | method | `skills/lazyown_facts.py:986` | `def summary(self, host)` |
| `GroqAgentPool` | class | `skills/lazyown_groq_agents.py:699` | `class GroqAgentPool` |
| `_AgentState` | class | `skills/lazyown_groq_agents.py:666` | `class _AgentState` |
| `__init__` | method | `skills/lazyown_groq_agents.py:702` | `def __init__(self)` |
| `_agent_system_prompt` | function | `skills/lazyown_groq_agents.py:682` | `def _agent_system_prompt(tool_names)` |
| `_c2_req` | function | `skills/lazyown_groq_agents.py:81` | `def _c2_req(path, method, body)` |
| `_load_payload` | function | `skills/lazyown_groq_agents.py:56` | `def _load_payload()` |
| `_now_utc` | function | `skills/lazyown_groq_agents.py:678` | `def _now_utc()` |
| `_run` | method | `skills/lazyown_groq_agents.py:742` | `def _run(self, state, tools, api_key, max_iterations, system_prompt)` |
| `_run_cmd` | function | `skills/lazyown_groq_agents.py:63` | `def _run_cmd(command, timeout)` |
| `_t_atomic_search` | function | `skills/lazyown_groq_agents.py:442` | `def _t_atomic_search(keyword, mitre_id, platform, scope, complexity, has_prereqs, limit, include_command)` |
| `_t_bridge_catalog` | function | `skills/lazyown_groq_agents.py:125` | `def _t_bridge_catalog(phase, os_hint)` |
| `_t_bridge_suggest` | function | `skills/lazyown_groq_agents.py:98` | `def _t_bridge_suggest(phase, services, tag, os_hint)` |
| `_t_c2_command` | function | `skills/lazyown_groq_agents.py:300` | `def _t_c2_command(client_id, command)` |
| `_t_c2_status` | function | `skills/lazyown_groq_agents.py:295` | `def _t_c2_status()` |
| `_t_command_help` | function | `skills/lazyown_groq_agents.py:390` | `def _t_command_help(command)` |
| `_t_cve_lookup` | function | `skills/lazyown_groq_agents.py:207` | `def _t_cve_lookup(product, version)` |
| `_t_facts_show` | function | `skills/lazyown_groq_agents.py:198` | `def _t_facts_show(target)` |
| `_t_inject_objective` | function | `skills/lazyown_groq_agents.py:333` | `def _t_inject_objective(title, description)` |
| `_t_list_sessions` | function | `skills/lazyown_groq_agents.py:287` | `def _t_list_sessions()` |
| `_t_memory_search` | function | `skills/lazyown_groq_agents.py:228` | `def _t_memory_search(query)` |
| `_t_parquet_context` | function | `skills/lazyown_groq_agents.py:171` | `def _t_parquet_context(phase, target)` |
| `_t_rag_query` | function | `skills/lazyown_groq_agents.py:394` | `def _t_rag_query(query, n)` |
| `_t_reactive_suggest` | function | `skills/lazyown_groq_agents.py:346` | `def _t_reactive_suggest(output, command, platform)` |
| `_t_read_session_file` | function | `skills/lazyown_groq_agents.py:277` | `def _t_read_session_file(filename)` |
| `_t_run_command` | function | `skills/lazyown_groq_agents.py:94` | `def _t_run_command(command)` |
| `_t_searchsploit` | function | `skills/lazyown_groq_agents.py:369` | `def _t_searchsploit(query)` |
| `_t_session_status` | function | `skills/lazyown_groq_agents.py:256` | `def _t_session_status()` |
| `_t_task_add` | function | `skills/lazyown_groq_agents.py:319` | `def _t_task_add(title, description)` |
| `_t_task_list` | function | `skills/lazyown_groq_agents.py:305` | `def _t_task_list(filter_status)` |
| `_t_threat_model` | function | `skills/lazyown_groq_agents.py:415` | `def _t_threat_model(action)` |
| `agent_result` | function | `skills/lazyown_groq_agents.py:861` | `def agent_result(agent_id)` |
| `agent_status` | function | `skills/lazyown_groq_agents.py:857` | `def agent_status(agent_id)` |
| `get_pool` | function | `skills/lazyown_groq_agents.py:829` | `def get_pool()` |
| `list_agents` | function | `skills/lazyown_groq_agents.py:865` | `def list_agents(limit)` |
| `list_all` | method | `skills/lazyown_groq_agents.py:807` | `def list_all(self, limit)` |
| `main` | function | `skills/lazyown_groq_agents.py:872` | `def main()` |
| `result` | method | `skills/lazyown_groq_agents.py:794` | `def result(self, agent_id)` |
| `spawn` | method | `skills/lazyown_groq_agents.py:706` | `def spawn(self, goal, tools_filter, api_key, backend, max_iterations, system_prompt, block)` |
| `spawn_agent` | function | `skills/lazyown_groq_agents.py:838` | `def spawn_agent(goal, tools_filter, api_key, backend, max_iterations, block)` |
| `status` | method | `skills/lazyown_groq_agents.py:778` | `def status(self, agent_id)` |
| `HookEvent` | class | `skills/lazyown_hooks.py:27` | `class HookEvent(Enum)` |
| `HookRegistry` | class | `skills/lazyown_hooks.py:38` | `class HookRegistry` |
| `__init__` | method | `skills/lazyown_hooks.py:47` | `def __init__(self)` |
| `_audit` | function | `skills/lazyown_hooks.py:208` | `def _audit(ctx)` |
| `audit_hook` | function | `skills/lazyown_hooks.py:139` | `def audit_hook(context, audit_path)` |
| `build_default_registry` | function | `skills/lazyown_hooks.py:187` | `def build_default_registry(sessions_dir)` |
| `get_registry` | function | `skills/lazyown_hooks.py:224` | `def get_registry(sessions_dir)` |
| `metrics` | method | `skills/lazyown_hooks.py:79` | `def metrics(self)` |
| `rate_limit_hook` | function | `skills/lazyown_hooks.py:116` | `def rate_limit_hook(context, window, limit)` |
| `register` | method | `skills/lazyown_hooks.py:56` | `def register(self, event, handler)` |
| `run` | method | `skills/lazyown_hooks.py:59` | `def run(self, event, context)` |
| `sandbox_hook` | function | `skills/lazyown_hooks.py:101` | `def sandbox_hook(context)` |
| `start_timer_hook` | function | `skills/lazyown_hooks.py:176` | `def start_timer_hook(context)` |
| `timing_hook` | function | `skills/lazyown_hooks.py:161` | `def timing_hook(context)` |
| `LLMBridge` | class | `skills/lazyown_llm.py:97` | `class LLMBridge` |
| `LLMTool` | class | `skills/lazyown_llm.py:71` | `class LLMTool` |
| `__init__` | method | `skills/lazyown_llm.py:104` | `def __init__(self, backend, model, api_key)` |
| `_ask_groq` | method | `skills/lazyown_llm.py:140` | `def _ask_groq(self, goal, context, max_iterations, system_prompt)` |
| `_ask_ollama_react` | method | `skills/lazyown_llm.py:238` | `def _ask_ollama_react(self, goal, context, max_iterations, system_prompt)` |
| `_call_tool` | method | `skills/lazyown_llm.py:318` | `def _call_tool(self, name, args)` |
| `_default_system_prompt` | function | `skills/lazyown_llm.py:455` | `def _default_system_prompt(tool_names)` |
| `_groq_request` | method | `skills/lazyown_llm.py:201` | `def _groq_request(self, messages, tools)` |
| `_make_default_tools` | function | `skills/lazyown_llm.py:334` | `def _make_default_tools(bridge)` |
| `_ollama_generate` | method | `skills/lazyown_llm.py:305` | `def _ollama_generate(self, prompt)` |
| `ask` | method | `skills/lazyown_llm.py:127` | `def ask(self, goal, context, max_iterations, system_prompt)` |
| `build_bridge` | function | `skills/lazyown_llm.py:438` | `def build_bridge(backend, model, api_key, with_default_tools)` |
| `llm_ask` | function | `skills/lazyown_llm.py:468` | `def llm_ask(goal, context, backend, model, api_key, max_iterations, system_prompt, extra_tools)` |
| `main` | function | `skills/lazyown_llm.py:493` | `def main()` |
| `openai_schema` | method | `skills/lazyown_llm.py:79` | `def openai_schema(self)` |
| `read_facts` | function | `skills/lazyown_llm.py:376` | `def read_facts(target)` |
| `read_nmap` | function | `skills/lazyown_llm.py:352` | `def read_nmap(target)` |
| `read_objectives` | function | `skills/lazyown_llm.py:389` | `def read_objectives(limit)` |
| `read_plan` | function | `skills/lazyown_llm.py:369` | `def read_plan()` |
| `register_tool` | method | `skills/lazyown_llm.py:118` | `def register_tool(self, name, description, parameters, func)` |
| `run_command` | function | `skills/lazyown_llm.py:346` | `def run_command(command)` |
| `_add` | function | `skills/lazyown_mcp.py:1790` | `def _add(user, secret, host, source, confirmed)` |
| `_advance_phase_wm` | function | `skills/lazyown_mcp.py:9923` | `def _advance_phase_wm()` |
| `_blocking_run` | function | `skills/lazyown_mcp.py:10830` | `def _blocking_run()` |
| `_bootstrap_sequence` | function | `skills/lazyown_mcp.py:9114` | `def _bootstrap_sequence()` |
| `_build_command_from_facts` | function | `skills/lazyown_mcp.py:9233` | `def _build_command_from_facts(category, resolved_cmd, resolved_args, tgt)` |
| `_c2_creds` | function | `skills/lazyown_mcp.py:533` | `def _c2_creds()` |
| `_c2_request` | function | `skills/lazyown_mcp.py:543` | `def _c2_request(path, method, body)` |
| `_compact` | function | `skills/lazyown_mcp.py:391` | `def _compact(content, tool_name)` |
| `_compact_output_fn` | function | `skills/lazyown_mcp.py:401` | `def _compact_output_fn(c, t)` |
| `_create_tool_file` | function | `skills/lazyown_mcp.py:193` | `def _create_tool_file()` |
| `_decorator` | function | `skills/lazyown_mcp.py:625` | `def _decorator(func)` |
| `_deploy_beacon_sync` | function | `skills/lazyown_mcp.py:11568` | `def _deploy_beacon_sync()` |
| `_dispatch_perm_check` | function | `skills/lazyown_mcp.py:644` | `def _dispatch_perm_check(name, arguments)` |
| `_do_facts` | function | `skills/lazyown_mcp.py:1853` | `def _do_facts()` |
| `_ensure_aci` | function | `skills/lazyown_mcp.py:310` | `def _ensure_aci()` |
| `_ensure_auto` | function | `skills/lazyown_mcp.py:290` | `def _ensure_auto()` |
| `_ensure_automapper` | function | `skills/lazyown_mcp.py:235` | `def _ensure_automapper()` |
| `_ensure_bridge` | function | `skills/lazyown_mcp.py:92` | `def _ensure_bridge()` |
| `_ensure_engine` | function | `skills/lazyown_mcp.py:74` | `def _ensure_engine()` |
| `_ensure_facts` | function | `skills/lazyown_mcp.py:186` | `def _ensure_facts()` |
| `_ensure_hive` | function | `skills/lazyown_mcp.py:262` | `def _ensure_hive()` |
| `_ensure_llm` | function | `skills/lazyown_mcp.py:224` | `def _ensure_llm()` |
| `_ensure_narrator` | function | `skills/lazyown_mcp.py:165` | `def _ensure_narrator()` |
| `_ensure_objectives` | function | `skills/lazyown_mcp.py:204` | `def _ensure_objectives()` |
| `_ensure_orchestrator` | function | `skills/lazyown_mcp.py:8728` | `def _ensure_orchestrator()` |
| `_ensure_pdb` | function | `skills/lazyown_mcp.py:245` | `def _ensure_pdb()` |
| `_ensure_policy` | function | `skills/lazyown_mcp.py:176` | `def _ensure_policy()` |
| `_ensure_recommender` | function | `skills/lazyown_mcp.py:118` | `def _ensure_recommender()` |
| `_ensure_state` | function | `skills/lazyown_mcp.py:107` | `def _ensure_state()` |
| `_execute_step` | function | `skills/lazyown_mcp.py:9269` | `def _execute_step()` |
| `_fail` | function | `skills/lazyown_mcp.py:1035` | `def _fail(message, remediation)` |
| `_fused_recommendations` | function | `skills/lazyown_mcp.py:8509` | `def _fused_recommendations()` |
| `_gate_command` | function | `skills/lazyown_mcp.py:8801` | `def _gate_command(cmd)` |
| `_generate_tasks_from_sessions` | function | `skills/lazyown_mcp.py:8953` | `def _generate_tasks_from_sessions(tgt, platform, api_key)` |
| `_get_claudemd` | function | `skills/lazyown_mcp.py:407` | `def _get_claudemd()` |
| `_get_hooks` | function | `skills/lazyown_mcp.py:365` | `def _get_hooks()` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:251` | `def _get_pdb(_)` |
| `_get_pdb` | function | `skills/lazyown_mcp.py:331` | `def _get_pdb(_)` |
| `_get_perm_system` | function | `skills/lazyown_mcp.py:352` | `def _get_perm_system()` |
| `_get_transcript` | function | `skills/lazyown_mcp.py:378` | `def _get_transcript()` |
| `_h_ack_event` | function | `skills/lazyown_mcp.py:969` | `def _h_ack_event(arguments, tool_name)` |
| `_h_auto_pwn` | function | `skills/lazyown_mcp.py:1250` | `def _h_auto_pwn(arguments, tool_name)` |
| `_h_c2_status` | function | `skills/lazyown_mcp.py:981` | `def _h_c2_status(arguments, tool_name)` |
| `_h_credentials` | function | `skills/lazyown_mcp.py:1784` | `def _h_credentials(arguments, tool_name)` |
| `_h_dashboard_snapshot` | function | `skills/lazyown_mcp.py:1211` | `def _h_dashboard_snapshot(arguments, tool_name)` |
| `_h_db` | function | `skills/lazyown_mcp.py:690` | `def _h_db(arguments, tool_name)` |
| `_h_evasion_generate` | function | `skills/lazyown_mcp.py:1162` | `def _h_evasion_generate(arguments, tool_name)` |
| `_h_evasion_rotate` | function | `skills/lazyown_mcp.py:1177` | `def _h_evasion_rotate(arguments, tool_name)` |
| `_h_exploit_chain` | function | `skills/lazyown_mcp.py:1283` | `def _h_exploit_chain(arguments, tool_name)` |
| `_h_exploit_recommend` | function | `skills/lazyown_mcp.py:1138` | `def _h_exploit_recommend(arguments, tool_name)` |
| `_h_exploitgym_list` | function | `skills/lazyown_mcp.py:1877` | `def _h_exploitgym_list(arguments, tool_name)` |
| `_h_exploitgym_run` | function | `skills/lazyown_mcp.py:1893` | `def _h_exploitgym_run(arguments, tool_name)` |
| `_h_exploitgym_score` | function | `skills/lazyown_mcp.py:1913` | `def _h_exploitgym_score(arguments, tool_name)` |
| `_h_exploitgym_status` | function | `skills/lazyown_mcp.py:1863` | `def _h_exploitgym_status(arguments, tool_name)` |
| `_h_facts_show` | function | `skills/lazyown_mcp.py:1843` | `def _h_facts_show(arguments, tool_name)` |
| `_h_get_beacons` | function | `skills/lazyown_mcp.py:1244` | `def _h_get_beacons(arguments, tool_name)` |
| `_h_get_config` | function | `skills/lazyown_mcp.py:684` | `def _h_get_config(arguments, tool_name)` |
| `_h_get_llm_budget` | function | `skills/lazyown_mcp.py:822` | `def _h_get_llm_budget(arguments, tool_name)` |
| `_h_inject_objective` | function | `skills/lazyown_mcp.py:1764` | `def _h_inject_objective(arguments, tool_name)` |
| `_h_lazy_addon` | function | `skills/lazyown_mcp.py:1588` | `def _h_lazy_addon(arguments, tool_name)` |
| `_h_lazy_board` | function | `skills/lazyown_mcp.py:1363` | `def _h_lazy_board(arguments, tool_name)` |
| `_h_lazy_compact` | function | `skills/lazyown_mcp.py:1564` | `def _h_lazy_compact(arguments, tool_name)` |
| `_h_lazy_delete` | function | `skills/lazyown_mcp.py:1539` | `def _h_lazy_delete(arguments, tool_name)` |
| `_h_lazy_finding` | function | `skills/lazyown_mcp.py:1468` | `def _h_lazy_finding(arguments, tool_name)` |
| `_h_lazy_hint` | function | `skills/lazyown_mcp.py:1403` | `def _h_lazy_hint(arguments, tool_name)` |
| `_h_lazy_mention` | function | `skills/lazyown_mcp.py:1508` | `def _h_lazy_mention(arguments, tool_name)` |
| `_h_lazy_proxy` | function | `skills/lazyown_mcp.py:1443` | `def _h_lazy_proxy(arguments, tool_name)` |
| `_h_lazy_status` | function | `skills/lazyown_mcp.py:1343` | `def _h_lazy_status(arguments, tool_name)` |
| `_h_lazy_sync` | function | `skills/lazyown_mcp.py:1353` | `def _h_lazy_sync(arguments, tool_name)` |
| `_h_lazy_trace` | function | `skills/lazyown_mcp.py:1386` | `def _h_lazy_trace(arguments, tool_name)` |
| `_h_lazy_workspace` | function | `skills/lazyown_mcp.py:1422` | `def _h_lazy_workspace(arguments, tool_name)` |
| `_h_list_modules` | function | `skills/lazyown_mcp.py:882` | `def _h_list_modules(arguments, tool_name)` |
| `_h_lolbas_list` | function | `skills/lazyown_mcp.py:1616` | `def _h_lolbas_list(arguments, tool_name)` |
| `_h_lolbas_use` | function | `skills/lazyown_mcp.py:1656` | `def _h_lolbas_use(arguments, tool_name)` |
| `_h_loop_smoke` | function | `skills/lazyown_mcp.py:1954` | `def _h_loop_smoke(arguments, tool_name)` |
| `_h_opencode_config` | function | `skills/lazyown_mcp.py:1932` | `def _h_opencode_config(arguments, tool_name)` |
| `_h_pivot_status` | function | `skills/lazyown_mcp.py:1191` | `def _h_pivot_status(arguments, tool_name)` |
| `_h_rea` | function | `skills/lazyown_mcp.py:1023` | `def _h_rea(arguments, tool_name)` |
| `_h_rich_tui_snapshot` | function | `skills/lazyown_mcp.py:1730` | `def _h_rich_tui_snapshot(arguments, tool_name)` |
| `_h_run_command` | function | `skills/lazyown_mcp.py:904` | `def _h_run_command(arguments, tool_name)` |
| `_h_set_config` | function | `skills/lazyown_mcp.py:859` | `def _h_set_config(arguments, tool_name)` |
| `_h_stealth` | function | `skills/lazyown_mcp.py:1706` | `def _h_stealth(arguments, tool_name)` |
| `_h_unified_dashboard` | function | `skills/lazyown_mcp.py:1231` | `def _h_unified_dashboard(arguments, tool_name)` |
| `_handle_messages` | function | `skills/lazyown_mcp.py:12492` | `def _handle_messages(scope, receive, send)` |
| `_handle_sighup` | function | `skills/lazyown_mcp.py:12459` | `def _handle_sighup(signum, frame)` |
| `_handle_sse` | function | `skills/lazyown_mcp.py:12488` | `def _handle_sse(request)` |
| `_has_data` | function | `skills/lazyown_mcp.py:518` | `def _has_data(path)` |
| `_is_lab_target` | function | `skills/lazyown_mcp.py:566` | `def _is_lab_target(name)` |
| `_is_placeholder` | function | `skills/lazyown_mcp.py:9376` | `def _is_placeholder(val)` |
| `_is_placeholder` | function | `skills/lazyown_mcp.py:9742` | `def _is_placeholder(val)` |
| `_isolated_runner` | function | `skills/lazyown_mcp.py:12364` | `def _isolated_runner(cmd)` |
| `_launch` | function | `skills/lazyown_mcp.py:11928` | `def _launch()` |
| `_load` | function | `skills/lazyown_mcp.py:75` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:93` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:108` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:119` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:166` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:177` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:187` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:205` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:225` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:236` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:246` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:263` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:291` | `def _load(ns)` |
| `_load` | function | `skills/lazyown_mcp.py:311` | `def _load(ns)` |
| `_load_category_command_map` | function | `skills/lazyown_mcp.py:462` | `def _load_category_command_map()` |
| `_load_crons` | function | `skills/lazyown_mcp.py:11466` | `def _load_crons()` |
| `_load_payload` | function | `skills/lazyown_mcp.py:509` | `def _load_payload()` |
| `_make_text` | function | `skills/lazyown_mcp.py:632` | `def _make_text(tool_name, content)` |
| `_mark_task_done` | function | `skills/lazyown_mcp.py:9097` | `def _mark_task_done(task_id, outcome)` |
| `_mcp_executor` | function | `skills/lazyown_mcp.py:10227` | `def _mcp_executor(command, target)` |
| `_next_pending_task` | function | `skills/lazyown_mcp.py:9068` | `def _next_pending_task()` |
| `_parquet_candidates` | function | `skills/lazyown_mcp.py:9168` | `def _parquet_candidates(category, tgt)` |
| `_read_docstring` | function | `skills/lazyown_mcp.py:7617` | `def _read_docstring(cmd_name)` |
| `_read_os_json` | function | `skills/lazyown_mcp.py:8921` | `def _read_os_json()` |
| `_read_prompt` | function | `skills/lazyown_mcp.py:10091` | `def _read_prompt()` |
| `_refresh_facts` | function | `skills/lazyown_mcp.py:9225` | `def _refresh_facts(tgt)` |
| `_result` | function | `skills/lazyown_mcp.py:710` | `def _result(payload)` |
| `_run_campaign` | function | `skills/lazyown_mcp.py:11773` | `def _run_campaign()` |
| `_run_daemon` | function | `skills/lazyown_mcp.py:11843` | `def _run_daemon()` |
| `_run_lazyown_command` | function | `skills/lazyown_mcp.py:2010` | `def _run_lazyown_command(command, timeout)` |
| `_run_parquet_query` | function | `skills/lazyown_mcp.py:11707` | `def _run_parquet_query()` |
| `_run_pwntomate_if_xml_ready` | function | `skills/lazyown_mcp.py:9186` | `def _run_pwntomate_if_xml_ready(tgt)` |
| `_run_rea` | function | `skills/lazyown_mcp.py:1110` | `def _run_rea()` |
| `_run_with_fallback` | function | `skills/lazyown_mcp.py:921` | `def _run_with_fallback(cmd, to)` |
| `_runner` | function | `skills/lazyown_mcp.py:6654` | `def _runner(cmd)` |
| `_save_crons` | function | `skills/lazyown_mcp.py:11477` | `def _save_crons(entries)` |
| `_save_payload` | function | `skills/lazyown_mcp.py:523` | `def _save_payload(data)` |
| `_settle_step` | function | `skills/lazyown_mcp.py:8865` | `def _settle_step(cmd, output, via, finding_values)` |
| `_sitrep_recommendations` | function | `skills/lazyown_mcp.py:128` | `def _sitrep_recommendations(limit)` |
| `_trace_append` | function | `skills/lazyown_mcp.py:8836` | `def _trace_append(record)` |
| `_trace_search` | function | `skills/lazyown_mcp.py:8845` | `def _trace_search(query, limit)` |
| `_verified_context` | function | `skills/lazyown_mcp.py:556` | `def _verified_context()` |
| `_wait_for_nmap_xml` | function | `skills/lazyown_mcp.py:8933` | `def _wait_for_nmap_xml(tgt, timeout_s)` |
| `call_tool` | function | `skills/lazyown_mcp.py:6279` | `def call_tool(name, arguments)` |
| `coerce_value` | function | `skills/lazyown_mcp.py:868` | `def coerce_value(k, v)` |
| `list_tools` | function | `skills/lazyown_mcp.py:2113` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp.py:12470` | `def main()` |
| `register_handler` | function | `skills/lazyown_mcp.py:618` | `def register_handler(tool_name)` |
| `substitute_playbook_target` | function | `skills/lazyown_mcp.py:6261` | `def substitute_playbook_target(command, target)` |
| `text` | function | `skills/lazyown_mcp.py:6293` | `def text(content)` |
| `JobRecord` | class | `skills/lazyown_mcp_helpers.py:672` | `class JobRecord` |
| `JobStore` | class | `skills/lazyown_mcp_helpers.py:686` | `class JobStore` |
| `TaskAudit` | class | `skills/lazyown_mcp_helpers.py:153` | `class TaskAudit` |
| `__init__` | method | `skills/lazyown_mcp_helpers.py:689` | `def __init__(self, max_jobs)` |
| `_format_age` | function | `skills/lazyown_mcp_helpers.py:112` | `def _format_age(seconds)` |
| `_worker` | function | `skills/lazyown_mcp_helpers.py:709` | `def _worker()` |
| `audit_tasks` | function | `skills/lazyown_mcp_helpers.py:165` | `def audit_tasks(tasks, min_confidence)` |
| `build_target_context` | function | `skills/lazyown_mcp_helpers.py:414` | `def build_target_context(host, port, sessions_dir, payload, world_model)` |
| `collect_pwntomate_evidence` | function | `skills/lazyown_mcp_helpers.py:376` | `def collect_pwntomate_evidence(rhost, sessions_dir)` |
| `diff_snapshot` | function | `skills/lazyown_mcp_helpers.py:792` | `def diff_snapshot(sessions_dir, payload, world_model, tasks)` |
| `evidence_freshness` | function | `skills/lazyown_mcp_helpers.py:67` | `def evidence_freshness(path, threshold_seconds, now)` |
| `evidence_grep` | function | `skills/lazyown_mcp_helpers.py:297` | `def evidence_grep(pattern, sessions_dir, scope, max_matches, max_file_bytes, case_insensitive)` |
| `find_credential_provenance` | function | `skills/lazyown_mcp_helpers.py:196` | `def find_credential_provenance(value, sessions_dir, csv_name)` |
| `is_likely_credential` | function | `skills/lazyown_mcp_helpers.py:37` | `def is_likely_credential(value)` |
| `list` | method | `skills/lazyown_mcp_helpers.py:732` | `def list(self, limit)` |
| `needs_confirmation` | function | `skills/lazyown_mcp_helpers.py:875` | `def needs_confirmation(tool_name, arguments)` |
| `parse_task_value` | function | `skills/lazyown_mcp_helpers.py:125` | `def parse_task_value(title)` |
| `preflight_command` | function | `skills/lazyown_mcp_helpers.py:575` | `def preflight_command(command, payload, sessions_dir)` |
| `status` | method | `skills/lazyown_mcp_helpers.py:727` | `def status(self, job_id)` |
| `submit` | method | `skills/lazyown_mcp_helpers.py:694` | `def submit(self, command, runner, timeout)` |
| `take_snapshot` | function | `skills/lazyown_mcp_helpers.py:747` | `def take_snapshot(sessions_dir, payload, world_model, tasks)` |
| `call_tool` | function | `skills/lazyown_mcp_opencode.py:76` | `def call_tool(name, arguments)` |
| `list_tools` | function | `skills/lazyown_mcp_opencode.py:57` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp_opencode.py:84` | `def main()` |
| `Objective` | class | `skills/lazyown_objective.py:105` | `class Objective` |
| `ObjectiveStore` | class | `skills/lazyown_objective.py:123` | `class ObjectiveStore` |
| `SoulUpdater` | class | `skills/lazyown_objective.py:359` | `class SoulUpdater` |
| `__init__` | method | `skills/lazyown_objective.py:131` | `def __init__(self, path)` |
| `__init__` | method | `skills/lazyown_objective.py:379` | `def __init__(self)` |
| `_load_all` | method | `skills/lazyown_objective.py:138` | `def _load_all(self)` |
| `_now` | method | `skills/lazyown_objective.py:135` | `def _now(self)` |
| `_patch_line` | method | `skills/lazyown_objective.py:404` | `def _patch_line(self, key, value)` |
| `_patch_section` | method | `skills/lazyown_objective.py:389` | `def _patch_section(self, header, new_body)` |
| `_read` | method | `skills/lazyown_objective.py:384` | `def _read(self)` |
| `_save_all` | method | `skills/lazyown_objective.py:153` | `def _save_all(self, objs)` |
| `_text_hash` | method | `skills/lazyown_objective.py:159` | `def _text_hash(text)` |
| `_update_status` | method | `skills/lazyown_objective.py:229` | `def _update_status(self, obj_id, status, notes)` |
| `block` | method | `skills/lazyown_objective.py:246` | `def block(self, obj_id, reason)` |
| `cleanup` | method | `skills/lazyown_objective.py:163` | `def cleanup(self)` |
| `complete` | method | `skills/lazyown_objective.py:243` | `def complete(self, obj_id, notes)` |
| `current_plan` | function | `skills/lazyown_objective.py:330` | `def current_plan()` |
| `decompose_goal` | function | `skills/lazyown_objective.py:296` | `def decompose_goal(goal_text, target)` |
| `full_context_for_claude` | function | `skills/lazyown_objective.py:336` | `def full_context_for_claude(target)` |
| `inject` | method | `skills/lazyown_objective.py:193` | `def inject(self, text, priority, source, context, notes)` |
| `list_all` | method | `skills/lazyown_objective.py:265` | `def list_all(self, status, limit)` |
| `list_pending` | method | `skills/lazyown_objective.py:261` | `def list_pending(self, limit)` |
| `main` | function | `skills/lazyown_objective.py:485` | `def main()` |
| `next_pending` | method | `skills/lazyown_objective.py:255` | `def next_pending(self)` |
| `read_soul` | function | `skills/lazyown_objective.py:320` | `def read_soul()` |
| `skip` | method | `skills/lazyown_objective.py:249` | `def skip(self, obj_id, reason)` |
| `sort_key` | method | `skills/lazyown_objective.py:116` | `def sort_key(self)` |
| `start` | method | `skills/lazyown_objective.py:252` | `def start(self, obj_id)` |
| `summary` | method | `skills/lazyown_objective.py:271` | `def summary(self)` |
| `update_access` | method | `skills/lazyown_objective.py:459` | `def update_access(self, level, target, method)` |
| `update_credentials` | method | `skills/lazyown_objective.py:432` | `def update_credentials(self, creds)` |
| `update_os` | method | `skills/lazyown_objective.py:425` | `def update_os(self, os_name, target)` |
| `update_phase` | method | `skills/lazyown_objective.py:417` | `def update_phase(self, phase)` |
| `update_target` | method | `skills/lazyown_objective.py:421` | `def update_target(self, target)` |
| `update_vulnerabilities` | method | `skills/lazyown_objective.py:466` | `def update_vulnerabilities(self, vulns)` |
| `write_soul` | function | `skills/lazyown_objective.py:326` | `def write_soul(content)` |
| `ParquetDB` | class | `skills/lazyown_parquet_db.py:244` | `class ParquetDB` |
| `__init__` | method | `skills/lazyown_parquet_db.py:295` | `def __init__(self, lazyown_dir)` |
| `_build_cmd2_category_map` | function | `skills/lazyown_parquet_db.py:146` | `def _build_cmd2_category_map(lazyown_py)` |
| `_classify_row` | function | `skills/lazyown_parquet_db.py:203` | `def _classify_row(command, args, phase_hint)` |
| `_load_session` | method | `skills/lazyown_parquet_db.py:307` | `def _load_session(self)` |
| `_slim` | function | `skills/lazyown_parquet_db.py:930` | `def _slim(row)` |
| `_stable_id` | function | `skills/lazyown_parquet_db.py:178` | `def _stable_id(start, cmd, args, dest_ip)` |
| `annotate` | method | `skills/lazyown_parquet_db.py:405` | `def annotate(self, row_id, success, category, outcome)` |
| `annotate_rich` | method | `skills/lazyown_parquet_db.py:434` | `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` |
| `context_for_phase` | method | `skills/lazyown_parquet_db.py:630` | `def context_for_phase(self, phase, target, limit)` |
| `get_pdb` | function | `skills/lazyown_parquet_db.py:948` | `def get_pdb(lazyown_dir)` |
| `list_parquets` | method | `skills/lazyown_parquet_db.py:743` | `def list_parquets(self)` |
| `main` | function | `skills/lazyown_parquet_db.py:961` | `def main()` |
| `predict_success` | method | `skills/lazyown_parquet_db.py:843` | `def predict_success(self, command, category)` |
| `query_atomic` | method | `skills/lazyown_parquet_db.py:576` | `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `query_knowledge` | method | `skills/lazyown_parquet_db.py:526` | `def query_knowledge(self, keyword, parquet_name, columns, limit)` |
| `query_session` | method | `skills/lazyown_parquet_db.py:490` | `def query_session(self, phase, target, success_only, limit)` |
| `stats` | method | `skills/lazyown_parquet_db.py:729` | `def stats(self)` |
| `sync` | method | `skills/lazyown_parquet_db.py:316` | `def sync(self, csv_path)` |
| `train_classifier` | method | `skills/lazyown_parquet_db.py:748` | `def train_classifier(self, min_rows)` |
| `verify_model_integrity` | function | `skills/lazyown_parquet_db.py:892` | `def verify_model_integrity(model_path, encoder_path, hash_path)` |
| `PermissionMode` | class | `skills/lazyown_permissions.py:18` | `class PermissionMode(Enum)` |
| `PermissionRule` | class | `skills/lazyown_permissions.py:29` | `class PermissionRule` |
| `PermissionSystem` | class | `skills/lazyown_permissions.py:91` | `class PermissionSystem` |
| `__init__` | method | `skills/lazyown_permissions.py:103` | `def __init__(self, sessions_dir)` |
| `_audit` | method | `skills/lazyown_permissions.py:132` | `def _audit(self, tool, decision, reason, args)` |
| `_load` | method | `skills/lazyown_permissions.py:113` | `def _load(self)` |

Next: [SYMBOLS_p23.md](SYMBOLS_p23.md)
