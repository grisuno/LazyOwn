# API (page 23 of 28)
Previous: [API_p22.md](API_p22.md)

## skills/lazyown_facts.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/mcp_bridge.py`, `lazyc2.py`, `modules/chain_facts.py`, `modules/chain_synth.py`, `modules/chain_tokens.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/create_tool.py`, `skills/mcp_tools/facts_show.py`, `skills/sessions_watcher.py`, `skills/tests/test_facts.py`
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
Depends on: `modules/atomic_enricher.py`, `modules/lazyown_bridge.py`, `modules/reactive_engine.py`, `modules/session_rag.py`, `modules/session_reader.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`
Imported by: `skills/hive_mind.py`, `skills/mcp_tools/groq_agent.py`, `skills/swan_agent.py`, `tests/test_bridge_catalog_filtered.py`
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
Imported by: `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/llm_ask.py`
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
Depends on: `core/config.py`, `core/logging.py`, `modules/backdoor/server.c`, `modules/event_engine.py`, `modules/mcp_agent_bridge.py`, `modules/recommender.py`, `modules/sinks/routing.py`, `modules/timeline_narrator.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_claudemd.py`, `skills/lazyown_context.py`, `skills/lazyown_facts.py`, `skills/lazyown_hooks.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_helpers.py`, `skills/lazyown_objective.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_permissions.py`, `skills/lazyown_policy.py`, `skills/lazyown_session.py`, `skills/mcp_lazy.py`, `skills/mcp_tools/__init__.py`, `skills/mcp_tools/_context.py`
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp_opencode.py`, `skills/tests/test_mcp_smoke.py`, `tests/test_boyscout_contracts.py`, `tests/test_mcp_auto_loop_wrapper.py`, `tests/test_mcp_improvements.py`, `tests/test_rea_mcp.py`
- `register_handler` (function) `skills/lazyown_mcp.py:604` `def register_handler(tool_name)` -- Decorator that registers an async handler for *tool_name*.
- `list_tools` (function) `skills/lazyown_mcp.py:897` `def list_tools()`
- `substitute_playbook_target` (function) `skills/lazyown_mcp.py:921` `def substitute_playbook_target(command, target)` -- Substitute the {target} token in a playbook step command.
- `call_tool` (function) `skills/lazyown_mcp.py:939` `def call_tool(name, arguments)`
- `text` (function) `skills/lazyown_mcp.py:941` `def text(content)`
- `main` (function) `skills/lazyown_mcp.py:1049` `def main()`

## skills/lazyown_mcp_helpers.py
Imported by: `modules/c2_surfaces.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/campaign_sitrep.py`, `skills/mcp_tools/evidence_grep.py`, `skills/mcp_tools/run_command.py`, `skills/mcp_tools/run_command_async.py`, `skills/mcp_tools/session_diff.py`, `skills/mcp_tools/session_init.py`, `skills/mcp_tools/target_context.py`, `skills/mcp_tools/tasks_cleanup.py`, `tests/test_mcp_improvements.py`
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
Depends on: `modules/__init__.py`, `modules/backdoor/server.c`, `modules/harness.py`, `modules/orchestrator_config.py`, `skills/lazyown_mcp.py`
Imported by: `tests/test_opencode_mcp_harness.py`
- `list_tools` (function) `skills/lazyown_mcp_opencode.py:183` `def list_tools()` -- Expose the curated subset under short names, keeping original schemas.
- `call_tool` (function) `skills/lazyown_mcp_opencode.py:203` `def call_tool(name, arguments)` -- Proxy the short name to the full LazyOwn MCP handler.
- `main` (function) `skills/lazyown_mcp_opencode.py:213` `def main()`

## skills/lazyown_objective.py
Imported by: `modules/golden_path.py`, `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/inject_objective.py`, `skills/mcp_tools/next_objective.py`, `skills/mcp_tools/soul.py`, `skills/sessions_watcher.py`, `skills/tests/test_objectives.py`, `tests/test_daemon_loop.py`, `tests/test_golden_path.py`
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
Depends on: `core/logging.py`, `modules/atomic_enricher.py`, `modules/selection/parquet.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/mcp_bridge.py`, `modules/selection/parquet.py`, `modules/ttpscope_bridge.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/parquet_annotate.py`, `skills/mcp_tools/parquet_query.py`, `skills/tests/test_parquet_db.py`, `skills/update_knowledge.py`, `tests/test_core_modules.py`
- `ParquetDB.__init__` (method) `skills/lazyown_parquet_db.py:295` `def __init__(self, lazyown_dir)`
- `ParquetDB.sync` (method) `skills/lazyown_parquet_db.py:316` `def sync(self, csv_path)` -- Ingest sessions/LazyOwn_session_report.csv into session_knowledge.parquet.
- `ParquetDB.annotate` (method) `skills/lazyown_parquet_db.py:405` `def annotate(self, row_id, success, category, outcome)` -- Patch a row in session_knowledge.parquet by its id.
- `ParquetDB.annotate_rich` (method) `skills/lazyown_parquet_db.py:434` `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` -- Full annotation after real execution: stores output snippet + all metadata.
- `ParquetDB.query_session` (method) `skills/lazyown_parquet_db.py:490` `def query_session(self, phase, target, success_only, limit)` -- Query session_knowledge.parquet.
- `ParquetDB.query_knowledge` (method) `skills/lazyown_parquet_db.py:526` `def query_knowledge(self, keyword, parquet_name, columns, limit)` -- Search for keyword across one or all parquets in parquets/.
- `ParquetDB.query_atomic` (method) `skills/lazyown_parquet_db.py:578` `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team catalogue (parquets/techniques_enriched.parquet).
- `ParquetDB.context_for_phase` (method) `skills/lazyown_parquet_db.py:632` `def context_for_phase(self, phase, target, limit)` -- Return a rich context dict for MCP reasoning:
- `ParquetDB.stats` (method) `skills/lazyown_parquet_db.py:731` `def stats(self)`
- `ParquetDB.list_parquets` (method) `skills/lazyown_parquet_db.py:745` `def list_parquets(self)`
- `ParquetDB.train_classifier` (method) `skills/lazyown_parquet_db.py:750` `def train_classifier(self, min_rows)` -- Train a lightweight RandomForest classifier on session_knowledge.parquet.
- `ParquetDB.predict_success` (method) `skills/lazyown_parquet_db.py:845` `def predict_success(self, command, category)` -- Use the trained classifier to estimate probability of success.
- `verify_model_integrity` (function) `skills/lazyown_parquet_db.py:894` `def verify_model_integrity(model_path, encoder_path, hash_path)` -- Verify SHA256 integrity of classifier model and encoder files.
- `get_pdb` (function) `skills/lazyown_parquet_db.py:950` `def get_pdb(lazyown_dir)`
- `main` (function) `skills/lazyown_parquet_db.py:963` `def main()`

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
Imported by: `cli/recommendation_signals.py`, `modules/lazy_loop.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/swan_agent.py`, `tests/test_engage_orchestrator.py`, `tests/test_moe_rl_swan.py`, `tests/test_scope_bound_auto_gate.py`
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
Imported by: `skills/lazyown_mcp.py`, `skills/mcp_tools/session_resume.py`, `skills/mcp_tools/subagent_run.py`, `skills/tests/test_harness_e2e.py`
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

## skills/mcp_tools/__init__.py
Depends on: `skills/mcp_tools/_context.py`
Imported by: `skills/lazyown_mcp.py`
- `iter_tool_modules` (function) `skills/mcp_tools/__init__.py:30` `def iter_tool_modules()` -- Yield every discovered tool module exposing ``TOOL`` and ``handle``.
- `iter_schemas` (function) `skills/mcp_tools/__init__.py:51` `def iter_schemas()` -- Yield the ``types.Tool`` schema of every discovered tool module.
- `register_handlers` (function) `skills/mcp_tools/__init__.py:57` `def register_handlers(handlers, ctx)` -- Bind each discovered tool's handler into the shared dispatch table.

## skills/mcp_tools/aci_plan.py
Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/aci_plan.py:63` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_aci_plan MCP tool.

## skills/mcp_tools/aci_replan.py
Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/aci_replan.py:33` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_aci_replan MCP tool.

## skills/mcp_tools/aci_status.py
Depends on: `skills/aci_planner.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/aci_status.py:26` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_aci_status MCP tool.

## skills/mcp_tools/ack_event.py
Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/ack_event.py:28` `def handle(arguments, tool_name, ctx)` -- Acknowledge one event by id, reporting whether it was found.

## skills/mcp_tools/add_rule.py
Depends on: `modules/event_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/add_rule.py:41` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_add_rule MCP tool.

## skills/mcp_tools/add_target.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/add_target.py:48` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_add_target MCP tool.

## skills/mcp_tools/agent_result.py
Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/agent_result.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_agent_result MCP tool.

## skills/mcp_tools/agent_status.py
Depends on: `modules/mcp_agent_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/agent_status.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_agent_status MCP tool.

## skills/mcp_tools/apt_chain.py
Depends on: `modules/chain_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/apt_chain.py:93` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_apt_chain MCP tool.

## skills/mcp_tools/atomic_clean.py
Depends on: `modules/atomic_exploit_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/atomic_clean.py:45` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_atomic_clean MCP tool.

## skills/mcp_tools/atomic_resolve.py
Depends on: `modules/atomic_enricher.py`, `modules/atomic_resolver.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/atomic_resolve.py:49` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_atomic_resolve MCP tool.

## skills/mcp_tools/atomic_search.py
Depends on: `modules/atomic_enricher.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/atomic_search.py:74` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_atomic_search MCP tool.

## skills/mcp_tools/atomic_shell.py
Depends on: `modules/atomic_exploit_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/atomic_shell.py:34` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_atomic_shell MCP tool.

## skills/mcp_tools/auto_loop.py
Depends on: `modules/lazy_runner.py`, `skills/mcp_tools/_context.py`
Imported by: `tests/test_mcp_auto_loop_wrapper.py`
- `handle` (function) `skills/mcp_tools/auto_loop.py:128` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_auto_loop MCP tool through the shared runner.

## skills/mcp_tools/auto_populate.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/auto_populate.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_auto_populate MCP tool.

## skills/mcp_tools/auto_pwn.py
Depends on: `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/auto_pwn.py:47` `def handle(arguments, tool_name, ctx)` -- Run the full auto-pwn chain and return results with a summary.

## skills/mcp_tools/autonomous_events.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_events.py:28` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_events MCP tool.

## skills/mcp_tools/autonomous_inject.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_inject.py:34` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_inject MCP tool.

## skills/mcp_tools/autonomous_replay.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_replay.py:53` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_replay MCP tool.

## skills/mcp_tools/autonomous_start.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_start.py:40` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_start MCP tool.

## skills/mcp_tools/autonomous_status.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_status.py:21` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_status MCP tool.

## skills/mcp_tools/autonomous_stop.py
Depends on: `skills/autonomous_daemon.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/autonomous_stop.py:18` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_autonomous_stop MCP tool.

## skills/mcp_tools/bridge_suggest.py
Depends on: `modules/lazyown_bridge.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/bridge_suggest.py:104` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_bridge_suggest MCP tool.

## skills/mcp_tools/c2_adversary.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_adversary.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_adversary MCP tool.

## skills/mcp_tools/c2_command.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_command.py:37` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_command MCP tool.

## skills/mcp_tools/c2_notes.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_notes.py:38` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_notes MCP tool.

## skills/mcp_tools/c2_profile.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_profile.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_profile MCP tool.

## skills/mcp_tools/c2_redop.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_redop.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_redop MCP tool.

## skills/mcp_tools/c2_script.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_script.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_script MCP tool.

## skills/mcp_tools/c2_search_agent.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_search_agent.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_search_agent MCP tool.

## skills/mcp_tools/c2_status.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_status.py:20` `def handle(arguments, tool_name, ctx)` -- Query the C2 dashboard endpoint and return its JSON.

## skills/mcp_tools/c2_vuln_analysis.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/c2_vuln_analysis.py:32` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_c2_vuln_analysis MCP tool.

## skills/mcp_tools/campaign.py
Depends on: `skills/lazyown_campaign.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign.py:46` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign MCP tool.

## skills/mcp_tools/campaign_lessons.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_lessons.py:39` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_lessons MCP tool.

## skills/mcp_tools/campaign_sitrep.py
Depends on: `modules/killchain.py`, `skills/lazyown_mcp_helpers.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_sitrep.py:46` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_sitrep MCP tool.

## skills/mcp_tools/campaign_tasks.py
Depends on: `modules/session_reader.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/campaign_tasks.py:66` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_campaign_tasks MCP tool.

## skills/mcp_tools/claudemd.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/claudemd.py:43` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_claudemd MCP tool.

## skills/mcp_tools/collab_publish.py
Depends on: `modules/collab_bp.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/collab_publish.py:41` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_collab_publish MCP tool.

## skills/mcp_tools/command_help.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_help.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_help MCP tool.

## skills/mcp_tools/command_next.py
Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_next.py:45` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_next MCP tool.

## skills/mcp_tools/command_prev.py
Depends on: `cli/command_chain.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/command_prev.py:31` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_command_prev MCP tool.

## skills/mcp_tools/create_addon.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/create_addon.py:115` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_create_addon MCP tool.

## skills/mcp_tools/create_param.py
Depends on: `core/param_registry.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/create_param.py:47` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_create_param MCP tool.

## skills/mcp_tools/create_tool.py
Depends on: `skills/lazyown_facts.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/create_tool.py:55` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_create_tool MCP tool.

## skills/mcp_tools/credentials.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/credentials.py:32` `def handle(arguments, tool_name, ctx)` -- Collect, dedupe and format credentials from all session sources.

## skills/mcp_tools/cron_schedule.py
Depends on: `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/cron_schedule.py:55` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_cron_schedule MCP tool.

## skills/mcp_tools/cve_search.py
Depends on: `modules/cve_matcher.py`, `skills/mcp_tools/_context.py`
- `handle` (function) `skills/mcp_tools/cve_search.py:42` `def handle(arguments, tool_name, ctx)` -- Handle the lazyown_cve_search MCP tool.


Next: [API_p24.md](API_p24.md)
