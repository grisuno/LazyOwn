# API (page 20 of 24)
Previous: [API_p19.md](API_p19.md)

## skills/lazyown_facts.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `cli/commands/mcp_bridge.py`, `lazyc2.py`, `modules/chain_synth.py`, `modules/chain_tokens.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`, `skills/tests/test_facts.py`
- `Config.default` (method) `skills/lazyown_facts.py:45` `def default(cls)`
- `HostFacts.highest_access` (method) `skills/lazyown_facts.py:145` `def highest_access(self)`
- `HostFacts.open_ports` (method) `skills/lazyown_facts.py:156` `def open_ports(self)`
- `HostFacts.services_by_name` (method) `skills/lazyown_facts.py:159` `def services_by_name(self, name)`
- `INmapXmlParser.parse` (method) `skills/lazyown_facts.py:169` `def parse(self, xml_path)`
- `ITextOutputParser.can_parse` (method) `skills/lazyown_facts.py:217` `def can_parse(self, filename, content)`
- `ITextOutputParser.parse` (method) `skills/lazyown_facts.py:220` `def parse(self, host, content, source_file)`
- `ITextOutputParser.parse_extended` (method) `skills/lazyown_facts.py:228` `def parse_extended(self, host, content, source_file, port)` -- Extended parse including vulnerabilities and web paths.
- `CrackMapExecParser.can_parse` (method) `skills/lazyown_facts.py:250` `def can_parse(self, filename, content)`
- `CrackMapExecParser.parse` (method) `skills/lazyown_facts.py:257` `def parse(self, host, content, source_file)`
- `Enum4linuxParser.can_parse` (method) `skills/lazyown_facts.py:301` `def can_parse(self, filename, content)`
- `Enum4linuxParser.parse` (method) `skills/lazyown_facts.py:304` `def parse(self, host, content, source_file)`
- `SecretsdumpParser.can_parse` (method) `skills/lazyown_facts.py:341` `def can_parse(self, filename, content)`
- `SecretsdumpParser.parse` (method) `skills/lazyown_facts.py:346` `def parse(self, host, content, source_file)`
- `LdapParser.can_parse` (method) `skills/lazyown_facts.py:374` `def can_parse(self, filename, content)`
- `LdapParser.parse` (method) `skills/lazyown_facts.py:377` `def parse(self, host, content, source_file)`
- `KerbruteParser.can_parse` (method) `skills/lazyown_facts.py:403` `def can_parse(self, filename, content)`
- `KerbruteParser.parse` (method) `skills/lazyown_facts.py:406` `def parse(self, host, content, source_file)`
- `RpcclientParser.can_parse` (method) `skills/lazyown_facts.py:424` `def can_parse(self, filename, content)`
- `RpcclientParser.parse` (method) `skills/lazyown_facts.py:427` `def parse(self, host, content, source_file)`
- `GobusterFfufParser.can_parse` (method) `skills/lazyown_facts.py:447` `def can_parse(self, filename, content)`
- `GobusterFfufParser.parse` (method) `skills/lazyown_facts.py:450` `def parse(self, host, content, source_file)`
- `GobusterFfufParser.parse_extended` (method) `skills/lazyown_facts.py:453` `def parse_extended(self, host, content, source_file, port)`
- `NiktoParser.can_parse` (method) `skills/lazyown_facts.py:502` `def can_parse(self, filename, content)`
- `NiktoParser.parse` (method) `skills/lazyown_facts.py:505` `def parse(self, host, content, source_file)`
- `NiktoParser.parse_extended` (method) `skills/lazyown_facts.py:508` `def parse_extended(self, host, content, source_file, port)`
- `NucleiParser.can_parse` (method) `skills/lazyown_facts.py:545` `def can_parse(self, filename, content)`
- `NucleiParser.parse` (method) `skills/lazyown_facts.py:548` `def parse(self, host, content, source_file)`
- `NucleiParser.parse_extended` (method) `skills/lazyown_facts.py:551` `def parse_extended(self, host, content, source_file, port)`
- `SslscanParser.can_parse` (method) `skills/lazyown_facts.py:581` `def can_parse(self, filename, content)`
- `SslscanParser.parse` (method) `skills/lazyown_facts.py:584` `def parse(self, host, content, source_file)`
- `SslscanParser.parse_extended` (method) `skills/lazyown_facts.py:587` `def parse_extended(self, host, content, source_file, port)`
- `GenericOutputParser.can_parse` (method) `skills/lazyown_facts.py:635` `def can_parse(self, filename, content)`
- `GenericOutputParser.parse` (method) `skills/lazyown_facts.py:638` `def parse(self, host, content, source_file)`
- `FactStore.__init__` (method) `skills/lazyown_facts.py:677` `def __init__(self, cfg)`
- `FactStore.save` (method) `skills/lazyown_facts.py:727` `def save(self)`
- `FactStore.ingest_xml` (method) `skills/lazyown_facts.py:791` `def ingest_xml(self, xml_path)` -- Parse one nmap XML file, merge results, return count of new facts.
- `FactStore.ingest_text` (method) `skills/lazyown_facts.py:803` `def ingest_text(self, txt_path, host_hint)` -- Parse one tool output file, merge credential/share/access facts.
- `FactStore.parse_all` (method) `skills/lazyown_facts.py:859` `def parse_all(self, target)` -- Scan sessions/ for all nmap XML and txt files.
- `FactStore.get_host` (method) `skills/lazyown_facts.py:890` `def get_host(self, host)`
- `FactStore.all_hosts` (method) `skills/lazyown_facts.py:893` `def all_hosts(self)`
- `FactStore.context_for_command` (method) `skills/lazyown_facts.py:896` `def context_for_command(self, host, category)` -- Return a dict of substitution parameters for a command in the given attack category.
- `FactStore.summary` (method) `skills/lazyown_facts.py:986` `def summary(self, host)` -- Return a human-readable summary of stored facts.
- `create_tool_file` (function) `skills/lazyown_facts.py:1025` `def create_tool_file(toolname, command, trigger, active, tools_dir)` -- Write a new pwntomate .tool JSON file.
- `main` (function) `skills/lazyown_facts.py:1074` `def main()`

## skills/lazyown_groq_agents.py
Depends on: `modules/atomic_enricher.py`, `modules/lazyown_bridge.py`, `modules/reactive_engine.py`, `modules/session_rag.py`, `modules/session_reader.py`, `modules/threat_model.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`
Imported by: `skills/hive_mind.py`, `skills/lazyown_mcp.py`, `skills/swan_agent.py`, `tests/test_bridge_catalog_filtered.py`
- `GroqAgentPool.__init__` (method) `skills/lazyown_groq_agents.py:702` `def __init__(self)`
- `GroqAgentPool.spawn` (method) `skills/lazyown_groq_agents.py:706` `def spawn(self, goal, tools_filter, api_key, backend, max_iterations, system_prompt, block)` -- Spawn a new agent.
- `GroqAgentPool.status` (method) `skills/lazyown_groq_agents.py:778` `def status(self, agent_id)`
- `GroqAgentPool.result` (method) `skills/lazyown_groq_agents.py:794` `def result(self, agent_id)`
- `GroqAgentPool.list_all` (method) `skills/lazyown_groq_agents.py:807` `def list_all(self, limit)`
- `get_pool` (function) `skills/lazyown_groq_agents.py:829` `def get_pool()`
- `spawn_agent` (function) `skills/lazyown_groq_agents.py:838` `def spawn_agent(goal, tools_filter, api_key, backend, max_iterations, block)` -- Spawn a new Groq/Ollama agent.
- `agent_status` (function) `skills/lazyown_groq_agents.py:857` `def agent_status(agent_id)`
- `agent_result` (function) `skills/lazyown_groq_agents.py:861` `def agent_result(agent_id)`
- `list_agents` (function) `skills/lazyown_groq_agents.py:865` `def list_agents(limit)`
- `main` (function) `skills/lazyown_groq_agents.py:872` `def main()`

## skills/lazyown_hooks.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `HookRegistry.__init__` (method) `skills/lazyown_hooks.py:47` `def __init__(self)`
- `HookRegistry.register` (method) `skills/lazyown_hooks.py:56` `def register(self, event, handler)`
- `HookRegistry.run` (method) `skills/lazyown_hooks.py:59` `def run(self, event, context)` -- Run all handlers for event, chaining modified contexts.
- `HookRegistry.metrics` (method) `skills/lazyown_hooks.py:79` `def metrics(self)` -- Return aggregate hook execution counts.
- `sandbox_hook` (function) `skills/lazyown_hooks.py:101` `def sandbox_hook(context)` -- PRE_TOOL_USE: block catastrophic shell commands before permission evaluation.
- `rate_limit_hook` (function) `skills/lazyown_hooks.py:116` `def rate_limit_hook(context, window, limit)` -- PRE_TOOL_USE: prevent rapid-fire C2 commands (>5 per 2s).
- `audit_hook` (function) `skills/lazyown_hooks.py:139` `def audit_hook(context, audit_path)` -- AUDIT: append a one-line JSON record of every tool call to the audit log.
- `timing_hook` (function) `skills/lazyown_hooks.py:161` `def timing_hook(context)` -- POST_TOOL_USE: annotate result with wall-clock execution time.
- `start_timer_hook` (function) `skills/lazyown_hooks.py:176` `def start_timer_hook(context)` -- PRE_TOOL_USE: record start time for timing_hook.
- `build_default_registry` (function) `skills/lazyown_hooks.py:187` `def build_default_registry(sessions_dir)` -- Create a HookRegistry with the built-in safety hooks wired up.
- `get_registry` (function) `skills/lazyown_hooks.py:224` `def get_registry(sessions_dir)`

## skills/lazyown_llm.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_facts.py`, `skills/lazyown_mcp.py`, `skills/lazyown_objective.py`
Imported by: `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`
- `LLMTool.openai_schema` (method) `skills/lazyown_llm.py:79` `def openai_schema(self)`
- `LLMBridge.__init__` (method) `skills/lazyown_llm.py:104` `def __init__(self, backend, model, api_key)`
- `LLMBridge.register_tool` (method) `skills/lazyown_llm.py:118` `def register_tool(self, name, description, parameters, func)`
- `LLMBridge.ask` (method) `skills/lazyown_llm.py:127` `def ask(self, goal, context, max_iterations, system_prompt)`
- `run_command` (function) `skills/lazyown_llm.py:346` `def run_command(command)` -- Execute a LazyOwn shell command and return its output.
- `read_nmap` (function) `skills/lazyown_llm.py:352` `def read_nmap(target)` -- Read the nmap scan file for the given target IP.
- `read_plan` (function) `skills/lazyown_llm.py:369` `def read_plan()` -- Read the current attack plan from sessions/plan.txt.
- `read_facts` (function) `skills/lazyown_llm.py:376` `def read_facts(target)` -- Return FactStore structured facts for a target (or all targets).
- `read_objectives` (function) `skills/lazyown_llm.py:389` `def read_objectives(limit)` -- List the next N pending attack objectives.
- `build_bridge` (function) `skills/lazyown_llm.py:438` `def build_bridge(backend, model, api_key, with_default_tools)` -- Create a ready-to-use LLMBridge with optional default LazyOwn tools.
- `llm_ask` (function) `skills/lazyown_llm.py:468` `def llm_ask(goal, context, backend, model, api_key, max_iterations, system_prompt, extra_tools)` -- Single-call entry point for lazyown_mcp.py.
- `main` (function) `skills/lazyown_llm.py:493` `def main()`

## skills/lazyown_mcp.py
Depends on: `cli/command_chain.py`, `cli/graph_advisor.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/recommendation.py`, `cli/recommendation_signals.py`, `core/config.py`, `core/hardening.py`, `core/llm_budget.py`, `core/logging.py`, `core/payload_schema.py`, `modules/__init__.py`, `modules/ai_exploit_chain.py`, `modules/atomic_enricher.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/auto_loop_memory.py`, `modules/auto_pivot.py`, `modules/auto_registry.py`, `modules/autonomous_exploit_engine.py`, `modules/backdoor/server.c`, `modules/chain_registry.py`, `modules/collab_bp.py`, `modules/cve_matcher.py`, `modules/dashboard_engine.py`, `modules/db.py`, `modules/digest.py`, `modules/evasion_engine.py`, `modules/event_engine.py`, `modules/evidence.py`, `modules/exploit_recommender.py`, `modules/exploitgym_gym.py`, `modules/goals.py`, `modules/integrations/misp_export.py`, `modules/intelligence_engine.py`, `modules/intercept.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_mentions.py`, `modules/lazyown_bridge.py`, `modules/llm_client.py`, `modules/llm_evaluator.py`, `modules/llm_pool.py`, `modules/mcp_agent_bridge.py`, `modules/memory_store.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/obs_parser.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/recommender.py`, `modules/selector_manager.py`, `modules/session_rag.py`, `modules/session_reader.py`, `modules/session_state.py`, `modules/sinks/routing.py`, `modules/threat_model.py`, `modules/timeline_narrator.py`, `modules/traffic_recorder.py`, `modules/ttpscope_bridge.py`, `modules/unified_dashboard.py`, `modules/world_model.py`, `scripts/lazy_opencode_config.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/daemon_control.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_claudemd.py`, `skills/lazyown_context.py`, `skills/lazyown_facts.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_hooks.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_helpers.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_permissions.py`, `skills/lazyown_policy.py`, `skills/lazyown_session.py`, `skills/mcp_lazy.py`, `skills/swan_agent.py`
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_opencode.py`, `skills/tests/test_mcp_smoke.py`, `tests/test_boyscout_contracts.py`, `tests/test_mcp_improvements.py`, `tests/test_rea_mcp.py`
- `register_handler` (function) `skills/lazyown_mcp.py:634` `def register_handler(tool_name)` -- Decorator that registers an async handler for *tool_name*.
- `coerce_value` (function) `skills/lazyown_mcp.py:884` `def coerce_value(k, v)`
- `list_tools` (function) `skills/lazyown_mcp.py:2131` `def list_tools()`
- `substitute_playbook_target` (function) `skills/lazyown_mcp.py:6478` `def substitute_playbook_target(command, target)` -- Substitute the {target} token in a playbook step command.
- `call_tool` (function) `skills/lazyown_mcp.py:6496` `def call_tool(name, arguments)`
- `text` (function) `skills/lazyown_mcp.py:6510` `def text(content)`
- `_Proposal.__init__` (method) `skills/lazyown_mcp.py:8948` `def __init__(self, command, args, source, reason, priority)`
- `main` (function) `skills/lazyown_mcp.py:13113` `def main()`

## skills/lazyown_mcp_helpers.py
Imported by: `modules/c2_surfaces.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_mcp_improvements.py`
- `is_likely_credential` (function) `skills/lazyown_mcp_helpers.py:37` `def is_likely_credential(value)` -- Score whether a string is plausibly a real credential.
- `evidence_freshness` (function) `skills/lazyown_mcp_helpers.py:67` `def evidence_freshness(path, threshold_seconds, now)` -- Return age + stale flag for an evidence file.
- `parse_task_value` (function) `skills/lazyown_mcp_helpers.py:125` `def parse_task_value(title)` -- Extract the embedded JSON-ish payload from a task title.
- `audit_tasks` (function) `skills/lazyown_mcp_helpers.py:165` `def audit_tasks(tasks, min_confidence)` -- Classify each task as keep/drop with a reason.
- `find_credential_provenance` (function) `skills/lazyown_mcp_helpers.py:196` `def find_credential_provenance(value, sessions_dir, csv_name)` -- Locate where a credential was first observed.
- `evidence_grep` (function) `skills/lazyown_mcp_helpers.py:297` `def evidence_grep(pattern, sessions_dir, scope, max_matches, max_file_bytes, case_insensitive)` -- Grep through session artefacts.
- `collect_pwntomate_evidence` (function) `skills/lazyown_mcp_helpers.py:376` `def collect_pwntomate_evidence(rhost, sessions_dir)` -- List pwntomate output dirs for a target with per-dir freshness.
- `build_target_context` (function) `skills/lazyown_mcp_helpers.py:414` `def build_target_context(host, port, sessions_dir, payload, world_model)` -- Aggregate everything known about (host, port) into one structure.
- `preflight_command` (function) `skills/lazyown_mcp_helpers.py:575` `def preflight_command(command, payload, sessions_dir)` -- Pre-flight a LazyOwn command without executing it.
- `JobStore.__init__` (method) `skills/lazyown_mcp_helpers.py:689` `def __init__(self, max_jobs)`
- `JobStore.submit` (method) `skills/lazyown_mcp_helpers.py:694` `def submit(self, command, runner, timeout)` -- Start a runner(command, timeout) in a background thread.
- `JobStore.status` (method) `skills/lazyown_mcp_helpers.py:727` `def status(self, job_id)`
- `JobStore.list` (method) `skills/lazyown_mcp_helpers.py:732` `def list(self, limit)`
- `take_snapshot` (function) `skills/lazyown_mcp_helpers.py:747` `def take_snapshot(sessions_dir, payload, world_model, tasks)` -- Capture a lightweight snapshot of the campaign state.
- `diff_snapshot` (function) `skills/lazyown_mcp_helpers.py:792` `def diff_snapshot(sessions_dir, payload, world_model, tasks)` -- Return what changed since the last snapshot.
- `needs_confirmation` (function) `skills/lazyown_mcp_helpers.py:875` `def needs_confirmation(tool_name, arguments)` -- Return True if tool should require an explicit confirm=True flag.

## skills/lazyown_mcp_opencode.py
Depends on: `modules/backdoor/server.c`, `skills/lazyown_mcp.py`
- `list_tools` (function) `skills/lazyown_mcp_opencode.py:62` `def list_tools()` -- Expose the curated subset under short names, keeping original schemas.
- `call_tool` (function) `skills/lazyown_mcp_opencode.py:81` `def call_tool(name, arguments)` -- Proxy the short name to the full LazyOwn MCP handler.
- `main` (function) `skills/lazyown_mcp_opencode.py:89` `def main()`

## skills/lazyown_objective.py
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`, `skills/tests/test_objectives.py`, `tests/test_daemon_loop.py`
- `Objective.sort_key` (method) `skills/lazyown_objective.py:116` `def sort_key(self)`
- `ObjectiveStore.__init__` (method) `skills/lazyown_objective.py:131` `def __init__(self, path)`
- `ObjectiveStore.cleanup` (method) `skills/lazyown_objective.py:163` `def cleanup(self)` -- Expire pending objectives whose TTL has passed.
- `ObjectiveStore.inject` (method) `skills/lazyown_objective.py:193` `def inject(self, text, priority, source, context, notes)`
- `ObjectiveStore.complete` (method) `skills/lazyown_objective.py:243` `def complete(self, obj_id, notes)`
- `ObjectiveStore.block` (method) `skills/lazyown_objective.py:246` `def block(self, obj_id, reason)`
- `ObjectiveStore.skip` (method) `skills/lazyown_objective.py:249` `def skip(self, obj_id, reason)`
- `ObjectiveStore.start` (method) `skills/lazyown_objective.py:252` `def start(self, obj_id)`
- `ObjectiveStore.next_pending` (method) `skills/lazyown_objective.py:255` `def next_pending(self)`
- `ObjectiveStore.list_pending` (method) `skills/lazyown_objective.py:261` `def list_pending(self, limit)`
- `ObjectiveStore.list_all` (method) `skills/lazyown_objective.py:265` `def list_all(self, status, limit)`
- `ObjectiveStore.summary` (method) `skills/lazyown_objective.py:271` `def summary(self)`
- `decompose_goal` (function) `skills/lazyown_objective.py:296` `def decompose_goal(goal_text, target)` -- Split a compound goal into discrete verifiable objectives.
- `read_soul` (function) `skills/lazyown_objective.py:320` `def read_soul()`
- `write_soul` (function) `skills/lazyown_objective.py:326` `def write_soul(content)`
- `current_plan` (function) `skills/lazyown_objective.py:330` `def current_plan()`
- `full_context_for_claude` (function) `skills/lazyown_objective.py:336` `def full_context_for_claude(target)` -- Return a single dict with everything Claude Code needs to reason about the next objective:  soul + pending...
- `SoulUpdater.__init__` (method) `skills/lazyown_objective.py:379` `def __init__(self)`
- `SoulUpdater.update_phase` (method) `skills/lazyown_objective.py:417` `def update_phase(self, phase)` -- Update the `Phase:` line inside ## Current Focus.
- `SoulUpdater.update_target` (method) `skills/lazyown_objective.py:421` `def update_target(self, target)` -- Update the `Target:` line inside ## Current Focus.
- `SoulUpdater.update_os` (method) `skills/lazyown_objective.py:425` `def update_os(self, os_name, target)` -- Record detected operating system for a target.
- `SoulUpdater.update_credentials` (method) `skills/lazyown_objective.py:432` `def update_credentials(self, creds)` -- Replace the ## Known Credentials section with discovered credentials.
- `SoulUpdater.update_access` (method) `skills/lazyown_objective.py:459` `def update_access(self, level, target, method)` -- Update achieved access level for a target.
- `SoulUpdater.update_vulnerabilities` (method) `skills/lazyown_objective.py:466` `def update_vulnerabilities(self, vulns)` -- Replace ## Key Vulnerabilities with the most severe findings.
- `main` (function) `skills/lazyown_objective.py:485` `def main()`

## skills/lazyown_parquet_db.py
Depends on: `core/logging.py`, `modules/atomic_enricher.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/mcp_bridge.py`, `modules/ttpscope_bridge.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/tests/test_parquet_db.py`, `skills/update_knowledge.py`, `tests/test_core_modules.py`
- `ParquetDB.__init__` (method) `skills/lazyown_parquet_db.py:295` `def __init__(self, lazyown_dir)`
- `ParquetDB.sync` (method) `skills/lazyown_parquet_db.py:316` `def sync(self, csv_path)` -- Ingest sessions/LazyOwn_session_report.csv into session_knowledge.parquet.
- `ParquetDB.annotate` (method) `skills/lazyown_parquet_db.py:405` `def annotate(self, row_id, success, category, outcome)` -- Patch a row in session_knowledge.parquet by its id.
- `ParquetDB.annotate_rich` (method) `skills/lazyown_parquet_db.py:434` `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` -- Full annotation after real execution: stores output snippet + all metadata.
- `ParquetDB.query_session` (method) `skills/lazyown_parquet_db.py:490` `def query_session(self, phase, target, success_only, limit)` -- Query session_knowledge.parquet.
- `ParquetDB.query_knowledge` (method) `skills/lazyown_parquet_db.py:526` `def query_knowledge(self, keyword, parquet_name, columns, limit)` -- Search for keyword across one or all parquets in parquets/.
- `ParquetDB.query_atomic` (method) `skills/lazyown_parquet_db.py:576` `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team catalogue (parquets/techniques_enriched.parquet).
- `ParquetDB.context_for_phase` (method) `skills/lazyown_parquet_db.py:630` `def context_for_phase(self, phase, target, limit)` -- Return a rich context dict for MCP reasoning:
- `ParquetDB.stats` (method) `skills/lazyown_parquet_db.py:729` `def stats(self)`
- `ParquetDB.list_parquets` (method) `skills/lazyown_parquet_db.py:743` `def list_parquets(self)`
- `ParquetDB.train_classifier` (method) `skills/lazyown_parquet_db.py:748` `def train_classifier(self, min_rows)` -- Train a lightweight RandomForest classifier on session_knowledge.parquet.
- `ParquetDB.predict_success` (method) `skills/lazyown_parquet_db.py:843` `def predict_success(self, command, category)` -- Use the trained classifier to estimate probability of success.
- `verify_model_integrity` (function) `skills/lazyown_parquet_db.py:892` `def verify_model_integrity(model_path, encoder_path, hash_path)` -- Verify SHA256 integrity of classifier model and encoder files.
- `get_pdb` (function) `skills/lazyown_parquet_db.py:948` `def get_pdb(lazyown_dir)`
- `main` (function) `skills/lazyown_parquet_db.py:961` `def main()`

## skills/lazyown_permissions.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `PermissionRule.to_dict` (method) `skills/lazyown_permissions.py:36` `def to_dict(self)`
- `PermissionSystem.__init__` (method) `skills/lazyown_permissions.py:103` `def __init__(self, sessions_dir)`
- `PermissionSystem.add_rule` (method) `skills/lazyown_permissions.py:145` `def add_rule(self, tool_pattern, action, condition, description)`
- `PermissionSystem.remove_rule` (method) `skills/lazyown_permissions.py:151` `def remove_rule(self, tool_pattern, action)`
- `PermissionSystem.set_mode` (method) `skills/lazyown_permissions.py:157` `def set_mode(self, mode)`
- `PermissionSystem.list_rules` (method) `skills/lazyown_permissions.py:162` `def list_rules(self)`
- `PermissionSystem.evaluate` (method) `skills/lazyown_permissions.py:167` `def evaluate(self, tool_name, arguments)` -- Returns (decision, reason). decision: "allow" | "deny" | "ask"
- `PermissionSystem.metrics` (method) `skills/lazyown_permissions.py:237` `def metrics(self)` -- Aggregate audit log into per-decision and per-tool counts.
- `PermissionSystem.status_text` (method) `skills/lazyown_permissions.py:279` `def status_text(self)`

## skills/lazyown_policy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/detection_oracle.py`, `modules/logging_config.py`
Imported by: `cli/recommendation_signals.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/swan_agent.py`, `tests/test_engage_orchestrator.py`, `tests/test_moe_rl_swan.py`, `tests/test_scope_bound_auto_gate.py`
- `Config.default` (method) `skills/lazyown_policy.py:82` `def default(cls)` -- Construct configuration anchored to this file's repository root.
- `Config.ollama_url` (method) `skills/lazyown_policy.py:123` `def ollama_url(self)` -- Full URL for the Ollama generate endpoint.
- `infer_category` (function) `skills/lazyown_policy.py:267` `def infer_category(command, args)` -- Return the ActionCategory best matching the command and its arguments.
- `ClassificationResult.unknown` (method) `skills/lazyown_policy.py:317` `def unknown(cls, tier)` -- Produce a result indicating the tier could not classify.
- `EpisodeRecord.to_dict` (method) `skills/lazyown_policy.py:357` `def to_dict(self)` -- Serialise to a plain dict suitable for JSON encoding.
- `EpisodeRecord.from_dict` (method) `skills/lazyown_policy.py:362` `def from_dict(cls, d)` -- Deserialise from a dict produced by to_dict.
- `IOutputClassifier.classify` (method) `skills/lazyown_policy.py:376` `def classify(self, command, args, output, exit_code)` -- Classify the outcome of one command execution.
- `ExitCodeClassifier.classify` (method) `skills/lazyown_policy.py:401` `def classify(self, command, args, output, exit_code)` -- Return a low-confidence result based solely on the exit code.
- `HeuristicClassifier.classify` (method) `skills/lazyown_policy.py:444` `def classify(self, command, args, output, exit_code)` -- Scan output for known success or failure signatures.
- `_OllamaClassifierBase.__init__` (method) `skills/lazyown_policy.py:496` `def __init__(self, cfg, model, tier_name)`
- `_OllamaClassifierBase.classify` (method) `skills/lazyown_policy.py:570` `def classify(self, command, args, output, exit_code)` -- Send the command context to Ollama and parse the JSON reply.
- `OllamaSmallClassifier.__init__` (method) `skills/lazyown_policy.py:591` `def __init__(self, cfg)`
- `OllamaLargeClassifier.__init__` (method) `skills/lazyown_policy.py:601` `def __init__(self, cfg)`
- `UserInteractiveClassifier.classify` (method) `skills/lazyown_policy.py:616` `def classify(self, command, args, output, exit_code)` -- Prompt the operator and return their authoritative verdict.
- `CascadeClassifier.__init__` (method) `skills/lazyown_policy.py:666` `def __init__(self, cfg, interactive)`
- `CascadeClassifier.classify` (method) `skills/lazyown_policy.py:677` `def classify(self, command, args, output, exit_code)` -- Return the first sufficiently confident result, or the best available.
- `DetectionRiskAssessor.__init__` (method) `skills/lazyown_policy.py:715` `def __init__(self)`
- `DetectionRiskAssessor.assess_probability` (method) `skills/lazyown_policy.py:733` `def assess_probability(self, command, args, category)` -- Return detection probability in [0.0, 1.0].
- `DetectionRiskAssessor.is_high_risk` (method) `skills/lazyown_policy.py:746` `def is_high_risk(self, command, args, category)` -- Return True when detection probability meets or exceeds the threshold.
- `RewardCalculator.__init__` (method) `skills/lazyown_policy.py:773` `def __init__(self, cfg, risk_assessor)`
- `RewardCalculator.calculate` (method) `skills/lazyown_policy.py:783` `def calculate(self, category, outcome)` -- Return the reward integer for the given (category, outcome) pair.
- `RewardCalculator.calculate_with_detection` (method) `skills/lazyown_policy.py:798` `def calculate_with_detection(self, category, outcome, command, args)` -- Return (reward, detection_probability) for the given execution.
- `CSVSessionReader.__init__` (method) `skills/lazyown_policy.py:850` `def __init__(self, cfg)`
- `CSVSessionReader.read` (method) `skills/lazyown_policy.py:855` `def read(self)` -- Parse the CSV and return all classifiable rows as StepRecord instances.
- `IEpisodeStore.append_step` (method) `skills/lazyown_policy.py:903` `def append_step(self, step)` -- Add a step to the episode for its target, creating the episode if needed.
- `IEpisodeStore.load_all` (method) `skills/lazyown_policy.py:907` `def load_all(self)` -- Load every stored episode.
- `IEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:911` `def get_episode(self, target)` -- Return the episode for the given target, or None.
- `JSONLEpisodeStore.__init__` (method) `skills/lazyown_policy.py:923` `def __init__(self, cfg)`
- `JSONLEpisodeStore.append_step` (method) `skills/lazyown_policy.py:927` `def append_step(self, step)` -- Upsert the step into its target's episode and persist.
- `JSONLEpisodeStore.load_all` (method) `skills/lazyown_policy.py:947` `def load_all(self)` -- Deserialise all episodes from the .jsonl file.
- `JSONLEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:963` `def get_episode(self, target)` -- Return the episode for target, or None if not found.
- `TransitionTable.__init__` (method) `skills/lazyown_policy.py:987` `def __init__(self, cfg)`
- `TransitionTable.record` (method) `skills/lazyown_policy.py:993` `def record(self, from_state, to_category, outcome)` -- Increment the counter for the given transition and persist.
- `TransitionTable.query` (method) `skills/lazyown_policy.py:1003` `def query(self, from_state)` -- Return (next_category, success_rate, total_count) tuples for the given from_state, filtered by min_transition_count...
- `PolicyEngine.__init__` (method) `skills/lazyown_policy.py:1107` `def __init__(self, cfg, transitions)`
- `PolicyEngine.recommend` (method) `skills/lazyown_policy.py:1111` `def recommend(self, recent_steps)` -- Return up to top_k dicts with keys: category, reason, confidence, source.
- `SessionClassificationPipeline.__init__` (method) `skills/lazyown_policy.py:1202` `def __init__(self, cfg, interactive)`
- `SessionClassificationPipeline.process` (method) `skills/lazyown_policy.py:1210` `def process(self, target, command, args, output, exit_code, timestamp)` -- Classify, reward, store, and return a StepRecord for the given execution.
- `PolicyAdvisor.__init__` (method) `skills/lazyown_policy.py:1267` `def __init__(self, cfg)`
- `PolicyAdvisor.advise` (method) `skills/lazyown_policy.py:1272` `def advise(self, target)` -- Return the policy engine's recommendations for the given target.
- `PolicyAdvisor.episode_summary` (method) `skills/lazyown_policy.py:1277` `def episode_summary(self, target)` -- Return a high-level summary dict for the target's episode.
- `LazyOwnPolicyIntegration.__init__` (method) `skills/lazyown_policy.py:1302` `def __init__(self, cfg)`
- `LazyOwnPolicyIntegration.on_command_complete` (method) `skills/lazyown_policy.py:1307` `def on_command_complete(self, target, command, args, output, exit_code)` -- Classify a completed command and record it in the episode store.
- `LazyOwnPolicyIntegration.get_recommendations` (method) `skills/lazyown_policy.py:1318` `def get_recommendations(self, target)` -- Return ranked next-action recommendations for the target.
- `ApprovalOutcome.is_approved` (method) `skills/lazyown_policy.py:1365` `def is_approved(self)` -- True when the gate authorised execution.
- `ApprovalOutcome.is_denied` (method) `skills/lazyown_policy.py:1370` `def is_denied(self)` -- True when the gate denied execution.
- `IApprovalSink.announce` (method) `skills/lazyown_policy.py:1384` `def announce(self, request)` -- Publish the request so operators can see and resolve it.
- `IApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1388` `def resolution_for(self, approval_id)` -- Return the latest resolution for the request or None if pending.
- `FileApprovalSink.__init__` (method) `skills/lazyown_policy.py:1400` `def __init__(self, sessions_dir)`
- `FileApprovalSink.path` (method) `skills/lazyown_policy.py:1405` `def path(self)` -- Absolute path of the underlying JSONL file.
- `FileApprovalSink.announce` (method) `skills/lazyown_policy.py:1409` `def announce(self, request)`
- `FileApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1426` `def resolution_for(self, approval_id)`
- `BroadcastApprovalSink.__init__` (method) `skills/lazyown_policy.py:1463` `def __init__(self, narrator, file_sink)`
- `BroadcastApprovalSink.announce` (method) `skills/lazyown_policy.py:1471` `def announce(self, request)`
- `BroadcastApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1499` `def resolution_for(self, approval_id)`
- `StdinApprovalSink.__init__` (method) `skills/lazyown_policy.py:1513` `def __init__(self, stream)`
- `StdinApprovalSink.announce` (method) `skills/lazyown_policy.py:1523` `def announce(self, request)`
- `StdinApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1552` `def resolution_for(self, approval_id)`
- `CompositeApprovalSink.__init__` (method) `skills/lazyown_policy.py:1564` `def __init__(self, sinks)`
- `CompositeApprovalSink.announce` (method) `skills/lazyown_policy.py:1569` `def announce(self, request)`
- `CompositeApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1576` `def resolution_for(self, approval_id)`
- `ApprovalGate.__init__` (method) `skills/lazyown_policy.py:1634` `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)`
- `ApprovalGate.request` (method) `skills/lazyown_policy.py:1667` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome for the proposed execution.
- `ScopeBoundAutoGate.__init__` (method) `skills/lazyown_policy.py:1850` `def __init__(self, payload_path, in_scope_fn)`
- `ScopeBoundAutoGate.request` (method) `skills/lazyown_policy.py:1866` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome without ever prompting a human.
- `HistoryBootstrapper.__init__` (method) `skills/lazyown_policy.py:1928` `def __init__(self, cfg)`
- `HistoryBootstrapper.run` (method) `skills/lazyown_policy.py:1934` `def run(self)` -- Process all CSV rows and return the total number of steps indexed.
- `main` (function) `skills/lazyown_policy.py:2036` `def main()` -- Parse CLI arguments and dispatch to the appropriate command handler.

## skills/lazyown_session.py
Depends on: `skills/lazyown_context.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `SessionTranscript.__init__` (method) `skills/lazyown_session.py:82` `def __init__(self, sessions_dir, session_id)`
- `SessionTranscript.append` (method) `skills/lazyown_session.py:106` `def append(self, event_type, data)` -- Append a single event.
- `SessionTranscript.get_recent` (method) `skills/lazyown_session.py:143` `def get_recent(self, n)` -- Return the last n events.
- `SessionTranscript.get_all` (method) `skills/lazyown_session.py:161` `def get_all(self)`
- `SessionTranscript.count` (method) `skills/lazyown_session.py:164` `def count(self)`
- `SessionTranscript.maybe_auto_compact` (method) `skills/lazyown_session.py:174` `def maybe_auto_compact(self, threshold)` -- If event count since the last compact_boundary exceeds threshold, generate a template summary of those events and...
- `SessionTranscript.add_compact_boundary` (method) `skills/lazyown_session.py:209` `def add_compact_boundary(self, summary, preserved_uuids)` -- Mark a compaction point.
- `SessionTranscript.fork` (method) `skills/lazyown_session.py:227` `def fork(self, new_id)` -- Create a new transcript forked from this one.
- `SessionTranscript.status_text` (method) `skills/lazyown_session.py:257` `def status_text(self)`
- `get_transcript` (function) `skills/lazyown_session.py:281` `def get_transcript(sessions_dir, session_id)` -- Return the active transcript singleton.
- `reset_transcript` (function) `skills/lazyown_session.py:294` `def reset_transcript(sessions_dir, session_id)` -- Force a new transcript (e.g., after fork or session reset).

## skills/mcp_generated_tools.py
- `get_generated_tool_definitions` (function) `skills/mcp_generated_tools.py:659` `def get_generated_tool_definitions()` -- Return list[types.Tool] entries for all generated tools.
- `register_all_generated_handlers` (function) `skills/mcp_generated_tools.py:684` `def register_all_generated_handlers(register_handler_fn, make_text_fn, run_lazyown_cmd_fn)` -- Register every generated handler via *register_handler_fn*.

## skills/mcp_lazy.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_mcp_lazy.py`
- `ensure_optional` (function) `skills/mcp_lazy.py:18` `def ensure_optional(namespace, flag, loader)` -- Return the cached flag or run ``loader`` once to compute it.

## skills/mcp_tool_generator.py
- `load_command_index` (function) `skills/mcp_tool_generator.py:29` `def load_command_index()`
- `extract_commands` (function) `skills/mcp_tool_generator.py:34` `def extract_commands(index)` -- Return {command_name: summary} for all unique non-duplicate commands.
- `extract_existing_handlers` (function) `skills/mcp_tool_generator.py:55` `def extract_existing_handlers()` -- Parse lazyown_mcp.py for all defined MCP tool names.
- `sanitize_description` (function) `skills/mcp_tool_generator.py:72` `def sanitize_description(summary, max_len)` -- Truncate and clean a command summary for use as a tool description.
- `sanitize_docstring` (function) `skills/mcp_tool_generator.py:85` `def sanitize_docstring(text)` -- Escape backslashes and quotes for triple-quoted docstrings.
- `generate_module` (function) `skills/mcp_tool_generator.py:106` `def generate_module(commands, existing_handlers, limit)` -- Build the complete Python source for mcp_generated_tools.py.
- `verify_coverage` (function) `skills/mcp_tool_generator.py:203` `def verify_coverage(commands, existing_handlers)` -- Compare indexed commands against existing MCP tool coverage.
- `main` (function) `skills/mcp_tool_generator.py:220` `def main()`

## skills/sessions_watcher.py
Depends on: `core/logging.py`, `modules/event_engine.py`, `modules/logging_config.py`, `skills/lazyown_facts.py`, `skills/lazyown_objective.py`
Imported by: `skills/lazyown_daemon.py`
- `_Handler.on_created` (method) `skills/sessions_watcher.py:376` `def on_created(self, event)`
- `_Handler.on_modified` (method) `skills/sessions_watcher.py:380` `def on_modified(self, event)`
- `main` (function) `skills/sessions_watcher.py:430` `def main()`

## skills/setup.sh
- `info` (function) `skills/setup.sh:15`
- `warn` (function) `skills/setup.sh:16`
- `die` (function) `skills/setup.sh:17`
- `paths_for_sudo` (function) `skills/setup.sh:61` -- Collect paths that exist on this system
- `add_nopasswd` (function) `skills/setup.sh:92`

## skills/swan_agent.py
Depends on: `core/logging.py`, `modules/detection_oracle.py`, `modules/logging_config.py`, `modules/moe_router.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_policy.py`
Imported by: `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/unified_orchestrator.py`, `tests/test_moe_rl_swan.py`
- `SwanResult.is_success` (method) `skills/swan_agent.py:167` `def is_success(self)`
- `IResultAggregator.aggregate` (method) `skills/swan_agent.py:209` `def aggregate(self, task_type, goal, votes)` -- Return (synthesis_text, consensus_confidence).
- `ISwanOrchestrator.run` (method) `skills/swan_agent.py:226` `def run(self, task_type, goal, engagement_phase, timeout)` -- Execute with the best single expert and return result.
- `ISwanOrchestrator.ensemble_run` (method) `skills/swan_agent.py:236` `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` -- Execute with top-N experts in parallel and synthesize results.
- `WeightedTextAggregator.aggregate` (method) `skills/swan_agent.py:264` `def aggregate(self, task_type, goal, votes)`
- `ExpertExecutor.execute` (method) `skills/swan_agent.py:351` `def execute(self, expert_id, backend, model, goal, task_type, timeout, api_key)` -- Run the expert and return a SwanResult.
- `OutcomeEvaluator.evaluate` (method) `skills/swan_agent.py:479` `def evaluate(self, result, task_type)` -- Return (reward, detection_prob).
- `SwanOrchestrator.__init__` (method) `skills/swan_agent.py:572` `def __init__(self, executor, evaluator, aggregator, api_key)`
- `SwanOrchestrator.run` (method) `skills/swan_agent.py:592` `def run(self, task_type, goal, engagement_phase, timeout)` -- Execute the task with the best single expert selected by the MoE+RL router.
- `SwanOrchestrator.ensemble_run` (method) `skills/swan_agent.py:680` `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` -- Execute with top-N experts in parallel and synthesize results.
- `SwanOrchestrator.status` (method) `skills/swan_agent.py:763` `def status(self)` -- Return a diagnostic snapshot of the SWAN system.
- `mcp_swan_run` (function) `skills/swan_agent.py:945` `def mcp_swan_run(task_type, goal, phase)` -- Route and execute a task with the best MoE+RL-selected expert.
- `mcp_swan_ensemble` (function) `skills/swan_agent.py:968` `def mcp_swan_ensemble(task_type, goal, n_experts, phase)` -- Run top-N experts in parallel and return a synthesized result.
- `mcp_swan_status` (function) `skills/swan_agent.py:996` `def mcp_swan_status()` -- Return SWAN system status: expert weights, RL epsilon, performance.
- `mcp_swan_route` (function) `skills/swan_agent.py:1003` `def mcp_swan_route(task_type, goal)` -- Show which expert would be selected for a task without executing.
- `get_swan` (function) `skills/swan_agent.py:1039` `def get_swan(api_key)` -- Return (or create) the module-level singleton SwanOrchestrator.

## skills/toposwarm_autonomous.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `modules/reactive_engine.py`, `modules/toposwarm_bridge.py`
- `PentestState.add_finding` (method) `skills/toposwarm_autonomous.py:145` `def add_finding(self, phase_name, text)`
- `PentestState.summary` (method) `skills/toposwarm_autonomous.py:149` `def summary(self)`
- `PentestState.to_dict` (method) `skills/toposwarm_autonomous.py:160` `def to_dict(self)`
- `AutonomousAgent.__init__` (method) `skills/toposwarm_autonomous.py:310` `def __init__(self, state, no_model, verbose, effort, max_phases, json_out)`
- `AutonomousAgent.run` (method) `skills/toposwarm_autonomous.py:432` `def run(self, start_phase)`
- `main` (function) `skills/toposwarm_autonomous.py:489` `def main(argv)`

## skills/unified_orchestrator.py
Depends on: `modules/engage_summary.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `lazyown.py`, `tests/test_improvements_spec.py`
- `OrchestratorConfig.from_payload` (method) `skills/unified_orchestrator.py:111` `def from_payload(cls, payload)` -- Return a config with ``payload.json`` overrides applied.
- `OrchestratorGoal.with_defaults` (method) `skills/unified_orchestrator.py:156` `def with_defaults(self, config)` -- Return a copy with empty fields populated from ``config``.
- `OrchestratorResult.to_dict` (method) `skills/unified_orchestrator.py:197` `def to_dict(self)` -- Return a JSON-serialisable dictionary of the result.
- `IOrchestratorBackend.available` (method) `skills/unified_orchestrator.py:215` `def available(self)` -- Return ``True`` when this backend can satisfy a request.
- `IOrchestratorBackend.run` (method) `skills/unified_orchestrator.py:219` `def run(self, goal)` -- Execute ``goal`` and return a normalised :class:`OrchestratorResult`.
- `EventBus.__init__` (method) `skills/unified_orchestrator.py:233` `def __init__(self, config, root)` -- Bind the bus to the active config.
- `EventBus.path` (method) `skills/unified_orchestrator.py:252` `def path(self)` -- Return the resolved event file path.
- `EventBus.emit` (method) `skills/unified_orchestrator.py:256` `def emit(self, event)` -- Append a single sanitised event to the bus.
- `BackendRegistry.__init__` (method) `skills/unified_orchestrator.py:303` `def __init__(self, backends)` -- Bind the registry to a fixed-order tuple of backends.
- `BackendRegistry.names` (method) `skills/unified_orchestrator.py:327` `def names(self)` -- Return the registered backend names in declaration order.
- `BackendRegistry.get` (method) `skills/unified_orchestrator.py:331` `def get(self, name)` -- Return the backend registered as ``name`` or ``None``.
- `BackendRegistry.available` (method) `skills/unified_orchestrator.py:335` `def available(self)` -- Return every backend that currently reports availability.
- `RouterPolicy.__init__` (method) `skills/unified_orchestrator.py:347` `def __init__(self, config, registry)` -- Bind the policy to config and backend registry.
- `RouterPolicy.choose` (method) `skills/unified_orchestrator.py:352` `def choose(self, goal)` -- Return the backend that should execute ``goal``.
- `DaemonBackend.__init__` (method) `skills/unified_orchestrator.py:413` `def __init__(self, config, factory, payload)` -- Bind to config, optional engine factory and payload mapping.
- `DaemonBackend.available` (method) `skills/unified_orchestrator.py:435` `def available(self)` -- Return ``True`` when the underlying engine can be imported.
- `DaemonBackend.run` (method) `skills/unified_orchestrator.py:445` `def run(self, goal)` -- Execute a single-target kill-chain engagement.
- `DaemonBackend.effective_target` (method) `skills/unified_orchestrator.py:489` `def effective_target(self, goal)` -- Return the daemon target this backend would use for ``goal``.
- `HiveBackend.__init__` (method) `skills/unified_orchestrator.py:610` `def __init__(self, config, factory)` -- Bind to config and an optional queen factory.
- `HiveBackend.available` (method) `skills/unified_orchestrator.py:619` `def available(self)` -- Return ``True`` when the hive engine is importable.
- `HiveBackend.run` (method) `skills/unified_orchestrator.py:629` `def run(self, goal)` -- Plan, dispatch, collect and synthesise via the hive.
- `SwanBackend.__init__` (method) `skills/unified_orchestrator.py:711` `def __init__(self, config, factory)` -- Bind to config and an optional orchestrator factory.
- `SwanBackend.available` (method) `skills/unified_orchestrator.py:720` `def available(self)` -- Return ``True`` when the SWAN engine is importable.
- `SwanBackend.run` (method) `skills/unified_orchestrator.py:730` `def run(self, goal)` -- Execute a single SWAN task and normalise the result.
- `GoalValidator.__init__` (method) `skills/unified_orchestrator.py:814` `def __init__(self, config)` -- Bind the validator to the active configuration.
- `GoalValidator.validate` (method) `skills/unified_orchestrator.py:818` `def validate(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` -- Return a normalised goal or raise :class:`ValueError`.
- `UnifiedOrchestrator.__init__` (method) `skills/unified_orchestrator.py:874` `def __init__(self, config, registry, router, validator, bus)` -- Bind the orchestrator to its collaborators.
- `UnifiedOrchestrator.backends` (method) `skills/unified_orchestrator.py:890` `def backends(self)` -- Return the registered backend names in declaration order.
- `UnifiedOrchestrator.execute` (method) `skills/unified_orchestrator.py:894` `def execute(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` -- Validate, route, execute and emit one goal end-to-end.
- `build_default_orchestrator` (function) `skills/unified_orchestrator.py:995` `def build_default_orchestrator(payload, sessions_dir)` -- Wire the canonical three-backend orchestrator.

## skills/update_knowledge.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_parquet_db.py`
- `main` (function) `skills/update_knowledge.py:40` `def main(argv)`

## slack_c2_bot.py
Depends on: `core/parsers.py`, `lazyown.py`, `modules/llm_adapter.py`, `utils.py`
- `SecureSessionManager.__init__` (method) `slack_c2_bot.py:29` `def __init__(self)`
- `SecureSessionManager.register_failed_attempt` (method) `slack_c2_bot.py:34` `def register_failed_attempt(self, user_id)`
- `SecureSessionManager.check_lockout` (method) `slack_c2_bot.py:42` `def check_lockout(self, user_id)`
- `SecureSessionManager.check_rate_limit` (method) `slack_c2_bot.py:52` `def check_rate_limit(self, user_id)`
- `SecureSessionManager.create_session` (method) `slack_c2_bot.py:63` `def create_session(self, user_id)`
- `SecureSessionManager.validate_session` (method) `slack_c2_bot.py:71` `def validate_session(self, user_id)`
- `SecureSessionManager.set_client` (method) `slack_c2_bot.py:81` `def set_client(self, user_id, client_id)`
- `SecureSessionManager.get_client` (method) `slack_c2_bot.py:85` `def get_client(self, user_id)`
- `capture_shell_output` (function) `slack_c2_bot.py:95` `def capture_shell_output(cmd)`
- `handle_message` (function) `slack_c2_bot.py:113` `def handle_message(event, say, logger)`
- `cmd_addcli` (function) `slack_c2_bot.py:177` `def cmd_addcli(ack, respond, command)`
- `cmd_clients` (function) `slack_c2_bot.py:195` `def cmd_clients(ack, respond, command)`
- `cmd_download` (function) `slack_c2_bot.py:209` `def cmd_download(ack, respond, command)`
- `handle_file` (function) `slack_c2_bot.py:240` `def handle_file(event, say, logger)`
- `mentioned` (function) `slack_c2_bot.py:252` `def mentioned(ack, say, event)`

## static/js/3d-force-graph-1.73.4.min.js
Depends on: `cli/assign.py`, `lazyown-docker/init.sh`, `modules/exp.c`
- `is` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `newNode` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `update` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `insertBodies` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `insert` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `isSamePosition` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `updateBoundingBox` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `resetBoundingBox` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Te` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `c` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Vr` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `l` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `u` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `g` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `c` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `b` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `u` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `differentBody` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `coefficient` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `h` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `v` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `l` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `hh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `a` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Hh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Jh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `uu` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `that` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `i` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `ld` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `pd` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `I` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `Md` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `cf` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `Ef` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...

## static/js/bootstrap-4.5.2.min.js
Depends on: `cli/show.py`
- `r` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `i` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `n` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `s` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `d` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `h` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `i` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !


Next: [API_p21.md](API_p21.md)
