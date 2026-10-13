# API (page 9 of 22)
Previous: [API_p8.md](API_p8.md)

## modules/agent_runner.py
Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/lazy_agent.py`, `modules/vulnbot.py`, `tests/test_lazy_streaming.py`
- `configure_logging` (function) `modules/agent_runner.py:60` `def configure_logging(debug)`
- `AgentTool.__init__` (method) `modules/agent_runner.py:69` `def __init__(self, name, description, func, parameters, required)`
- `AgentTool.to_api_format` (method) `modules/agent_runner.py:77` `def to_api_format(self)`
- `AgentTool.execute` (method) `modules/agent_runner.py:83` `def execute(self)` -- Ejecuta con validación de argumentos y formato claro
- `ASTToolExtractor.extract_commands_from_file` (method) `modules/agent_runner.py:138` `def extract_commands_from_file(file_path, prefix)`
- `AgentRunner.__init__` (method) `modules/agent_runner.py:176` `def __init__(self, model, system_prompt, max_iterations)`
- `AgentRunner.register_tool` (method) `modules/agent_runner.py:201` `def register_tool(self, tool)`
- `AgentRunner.register_tool_from_instance` (method) `modules/agent_runner.py:204` `def register_tool_from_instance(self, func)` -- Wrap a plain function as an AgentTool using its signature and docstring.
- `AgentRunner.register_tools_from_metadata` (method) `modules/agent_runner.py:222` `def register_tools_from_metadata(self, commands, executor)`
- `make_executor` (function) `modules/agent_runner.py:226` `def make_executor(cmd_name)`
- `wrapper` (function) `modules/agent_runner.py:227` `def wrapper(command)`
- `AgentRunner.get_tools_for_api` (method) `modules/agent_runner.py:249` `def get_tools_for_api(self)`
- `AgentRunner.run` (method) `modules/agent_runner.py:254` `def run(self, user_input)`
- `LazyOwnShellWrapper.__init__` (method) `modules/agent_runner.py:465` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/agent_runner.py:495` `def execute_command(self, command)` -- Ejecuta comando con timeout usando threading
- `target` (function) `modules/agent_runner.py:502` `def target()`
- `LazyOwnShellWrapper.get_commands_summary` (method) `modules/agent_runner.py:532` `def get_commands_summary(self)`
- `VulnBotCLI.__init__` (method) `modules/agent_runner.py:540` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.process_request` (method) `modules/agent_runner.py:595` `def process_request(self, user_input)`
- `interactive_mode` (function) `modules/agent_runner.py:600` `def interactive_mode(bot)`
- `parse_args` (function) `modules/agent_runner.py:624` `def parse_args()`
- `main` (function) `modules/agent_runner.py:634` `def main()`

## modules/ai_exploit_chain.py
Depends on: `modules/autonomous_exploit_engine.py`
Imported by: `cli/commands/pwn.py`, `skills/lazyown_mcp.py`
- `AIExploitChainer.__init__` (method) `modules/ai_exploit_chain.py:259` `def __init__(self)`
- `AIExploitChainer.reason` (method) `modules/ai_exploit_chain.py:285` `def reason(self, context)` -- Analyze context failures and produce the next best exploit candidate.
- `AIExploitChainer.evaluate_failure` (method) `modules/ai_exploit_chain.py:306` `def evaluate_failure(result)` -- Classify the reason for an exploit failure by output pattern matching.
- `AIExploitChainer.select_next_strategy` (method) `modules/ai_exploit_chain.py:318` `def select_next_strategy(self, context)` -- Select the next strategy to attempt based on context and failures.
- `AIExploitChainer.estimate_confidence` (method) `modules/ai_exploit_chain.py:349` `def estimate_confidence(self, strategy, profile)` -- Estimate confidence (0.0-1.0) for a strategy against a target profile.
- `AIExploitChainer.build_chain_plan` (method) `modules/ai_exploit_chain.py:391` `def build_chain_plan(self, context)` -- Build a full multi-step exploitation plan following the kill chain.
- `AIExploitChainer.adapt_chain` (method) `modules/ai_exploit_chain.py:428` `def adapt_chain(self, context, new_info)` -- Adapt the chain plan based on newly discovered information.

## modules/ai_fallback.py
Depends on: `modules/llm_factory.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`
- `call` (function) `modules/ai_fallback.py:254` `def call(prompt, system, api_key, max_tokens, temperature)` -- Call Groq → fallback to Ollama → fallback to TopoSwarm local brain → error.

## modules/ai_model.py
Depends on: `core/logging.py`, `modules/llm_factory.py`
Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_client.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`
- `AIModel.generate` (method) `modules/ai_model.py:56` `def generate(self, prompt)` -- Return a non-streaming completion for ``prompt``.
- `AIModel.stream_generate` (method) `modules/ai_model.py:60` `def stream_generate(self, prompt)` -- Yield streaming completion chunks for ``prompt``.
- `AIModel.complete` (method) `modules/ai_model.py:63` `def complete(self, system, user, max_tokens, temperature)` -- Return a completion conforming to ``core.protocols.LLMBackend``.
- `_LazyImporter.groq` (method) `modules/ai_model.py:105` `def groq(cls)`
- `_LazyImporter.openai` (method) `modules/ai_model.py:113` `def openai(cls)`
- `_LazyImporter.anthropic` (method) `modules/ai_model.py:121` `def anthropic(cls)`
- `GroqModel.__init__` (method) `modules/ai_model.py:137` `def __init__(self, api_key, model)`
- `GroqModel.generate` (method) `modules/ai_model.py:155` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `GroqModel.stream_generate` (method) `modules/ai_model.py:183` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `GroqModel.complete` (method) `modules/ai_model.py:216` `def complete(self, system, user, max_tokens, temperature)` -- Return a chat completion using native role separation.
- `OllamaModel.__init__` (method) `modules/ai_model.py:252` `def __init__(self, model, host)`
- `OllamaModel.generate` (method) `modules/ai_model.py:260` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `OllamaModel.stream_generate` (method) `modules/ai_model.py:281` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `LlamaCppModel.__init__` (method) `modules/ai_model.py:324` `def __init__(self, model, host)`
- `LlamaCppModel.generate` (method) `modules/ai_model.py:362` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `LlamaCppModel.stream_generate` (method) `modules/ai_model.py:382` `def stream_generate(self, prompt)` -- Yield streamed completion deltas for ``prompt``.
- `LlamaCppModel.complete` (method) `modules/ai_model.py:413` `def complete(self, system, user, max_tokens, temperature)` -- Role-aware completion through the chat endpoint.
- `OpenAIModel.__init__` (method) `modules/ai_model.py:440` `def __init__(self, api_key, model)`
- `OpenAIModel.generate` (method) `modules/ai_model.py:444` `def generate(self, prompt)`
- `OpenAIModel.stream_generate` (method) `modules/ai_model.py:455` `def stream_generate(self, prompt)`
- `OpenAIModel.complete` (method) `modules/ai_model.py:470` `def complete(self, system, user, max_tokens, temperature)`
- `AnthropicModel.__init__` (method) `modules/ai_model.py:499` `def __init__(self, api_key, model)`
- `AnthropicModel.generate` (method) `modules/ai_model.py:503` `def generate(self, prompt)`
- `AnthropicModel.stream_generate` (method) `modules/ai_model.py:515` `def stream_generate(self, prompt)`
- `AnthropicModel.complete` (method) `modules/ai_model.py:529` `def complete(self, system, user, max_tokens, temperature)`
- `DeepSeekModel.__init__` (method) `modules/ai_model.py:556` `def __init__(self, api_key, model)`
- `DeepSeekModel.generate` (method) `modules/ai_model.py:563` `def generate(self, prompt)`
- `DeepSeekModel.stream_generate` (method) `modules/ai_model.py:574` `def stream_generate(self, prompt)`
- `DeepSeekModel.complete` (method) `modules/ai_model.py:589` `def complete(self, system, user, max_tokens, temperature)`

## modules/amsi.c
- `LoadNtFunctions` (function) `modules/amsi.c:38` `void LoadNtFunctions()` -- Función para cargar las funciones dinámicamente
- `AMS1patch_OpenSession_jne` (function) `modules/amsi.c:66` `void AMS1patch_OpenSession_jne(HANDLE hproc)` -- Técnica de Saad, también conocido como @D1rkMtr (https://twitter.com/D1rkMtr/)...
- `AMS1patch_OpenSession_ret` (function) `modules/amsi.c:116` `void AMS1patch_OpenSession_ret(HANDLE hproc)`
- `AMS1patch_ScanBuffer_ret` (function) `modules/amsi.c:166` `void AMS1patch_ScanBuffer_ret(HANDLE hproc)`
- `AMS1patch_RastaMouse` (function) `modules/amsi.c:215` `void AMS1patch_RastaMouse(HANDLE hproc)`
- `AMS1patch_E_ACCESSDENIED` (function) `modules/amsi.c:274` `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)`
- `AMS1patch_E_HANDLE` (function) `modules/amsi.c:326` `void AMS1patch_E_HANDLE(HANDLE hproc)`
- `AMS1patch_E_OUTOFMEMORY` (function) `modules/amsi.c:378` `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)`
- `main` (function) `modules/amsi.c:428` `int main(int argc, char** argv)`

## modules/amt_auth_bypass.py
- `start` (function) `modules/amt_auth_bypass.py:4` `def start()`
- `BlankAuthResponse.request` (method) `modules/amt_auth_bypass.py:11` `def request(self, flow)`

## modules/apt_playbooks.py
Depends on: `core/console.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `cli/recommendation_signals.py`, `modules/operation.py`
- `AptPlaybook.from_dict` (method) `modules/apt_playbooks.py:74` `def from_dict(cls, data)`
- `AptPlaybook.to_summary` (method) `modules/apt_playbooks.py:99` `def to_summary(self)`
- `AptPlaybookEngine.__init__` (method) `modules/apt_playbooks.py:114` `def __init__(self, playbook_dir)`
- `AptPlaybookEngine.list_playbooks` (method) `modules/apt_playbooks.py:131` `def list_playbooks(self)`
- `AptPlaybookEngine.get` (method) `modules/apt_playbooks.py:134` `def get(self, name)`
- `AptPlaybookEngine.validate` (method) `modules/apt_playbooks.py:138` `def validate(self, pb, atomic_path)` -- Validate that all referenced atomic tests exist locally.
- `AptPlaybookEngine.generate_attack_plan` (method) `modules/apt_playbooks.py:189` `def generate_attack_plan(self, pb, output_path)` -- Generate a legacy ``attack_plan.yaml`` from an enriched APT playbook.
- `AptPlaybookEngine.report_json` (method) `modules/apt_playbooks.py:204` `def report_json(self, pb, output_path)` -- Write a structured JSON report of the playbook for the operator.

## modules/asset_graph.py
Imported by: `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`
- `asset_key` (function) `modules/asset_graph.py:28` `def asset_key(asset_type, value, parent_key)` -- Compute the stable deduplication key for an asset.
- `AssetGraph.__init__` (method) `modules/asset_graph.py:73` `def __init__(self, config)` -- Initialize empty graphs and anchor indexes.
- `AssetGraph.upsert_asset` (method) `modules/asset_graph.py:82` `def upsert_asset(self, asset_type, value, parent_key, company)` -- Insert or refresh an asset and return the canonical node.
- `AssetGraph.add_node` (method) `modules/asset_graph.py:108` `def add_node(self, task_id, kind, text, parent_id, payload)` -- Append an exploration node to a task chain.
- `AssetGraph.add_fact` (method) `modules/asset_graph.py:123` `def add_fact(self, task_id, text, parent_id, payload)` -- Append a fact node to a task chain.
- `AssetGraph.add_finding` (method) `modules/asset_graph.py:128` `def add_finding(self, task_id, text, parent_id, payload)` -- Append a finding node to a task chain.
- `AssetGraph.anchor` (method) `modules/asset_graph.py:133` `def anchor(self, exploration_id, key)` -- Link an exploration node to an asset key.
- `AssetGraph.assets_for_node` (method) `modules/asset_graph.py:145` `def assets_for_node(self, exploration_id)` -- List assets anchored to one exploration node.
- `AssetGraph.nodes_for_asset` (method) `modules/asset_graph.py:151` `def nodes_for_asset(self, key)` -- List exploration nodes anchored to one asset.
- `AssetGraph.coverage` (method) `modules/asset_graph.py:157` `def coverage(self, task_id)` -- Report tested versus total assets for a task.
- `AssetGraph.mirror_to_campaign` (method) `modules/asset_graph.py:170` `def mirror_to_campaign(self, db, world_model, workspace_id)` -- Mirror graph assets into the campaign database and world model.
- `coverage_for` (function) `modules/asset_graph.py:214` `def coverage_for(db, workspace_id, scope)` -- Report tested scope assets versus total scope from the campaign db.

## modules/atomic_enricher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `tests/test_core_modules.py`
- `enrich` (function) `modules/atomic_enricher.py:173` `def enrich(force)` -- Build enriched parquet.
- `load_enriched` (function) `modules/atomic_enricher.py:215` `def load_enriched()` -- Load enriched parquet, building it first if it doesn't exist.
- `query_atomic` (function) `modules/atomic_enricher.py:232` `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team technique catalogue.

## modules/attack_surface3d.py
Depends on: `cli/surface_graph.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/intel_fusion.py`
Imported by: `cli/commands/surface.py`, `lazyc2.py`, `tests/test_attack_surface3d.py`
- `build_attack_graph` (function) `modules/attack_surface3d.py:147` `def build_attack_graph(sessions_dir, payload_path, est_cap)` -- Fuse surface scans with campaign intel into one C2-centred graph.
- `add_edge` (function) `modules/attack_surface3d.py:155` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation between known nodes.
- `tag` (function) `modules/attack_surface3d.py:166` `def tag(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `refresh_summary` (function) `modules/attack_surface3d.py:460` `def refresh_summary(graph, sessions_dir)` -- Score exposure into intel_summary.json for the autonomous loop.

## modules/auto_pivot.py
Imported by: `modules/autonomous_exploit_engine.py`, `skills/lazyown_mcp.py`
- `AutoPivotEngine.__init__` (method) `modules/auto_pivot.py:73` `def __init__(self, config)`
- `AutoPivotEngine.set_config` (method) `modules/auto_pivot.py:82` `def set_config(self, config)`
- `AutoPivotEngine.add_pivot_node` (method) `modules/auto_pivot.py:90` `def add_pivot_node(self, ip, access_type, credential_id, hostname)`
- `AutoPivotEngine.remove_pivot_node` (method) `modules/auto_pivot.py:120` `def remove_pivot_node(self, ip)`
- `AutoPivotEngine.discover_subnets` (method) `modules/auto_pivot.py:128` `def discover_subnets(self, node_ip, command_output)`
- `AutoPivotEngine.build_chain` (method) `modules/auto_pivot.py:146` `def build_chain(self, target_ip, via_nodes, subnet)`
- `AutoPivotEngine.generate_proxychains_config` (method) `modules/auto_pivot.py:177` `def generate_proxychains_config(self, chain_id)`
- `AutoPivotEngine.generate_sshuttle_command` (method) `modules/auto_pivot.py:203` `def generate_sshuttle_command(self, node_ip, subnet)`
- `AutoPivotEngine.generate_chisel_command` (method) `modules/auto_pivot.py:206` `def generate_chisel_command(self, target_ip, local_port)`
- `AutoPivotEngine.generate_ssh_socks_command` (method) `modules/auto_pivot.py:212` `def generate_ssh_socks_command(self, node_ip, local_port)`
- `AutoPivotEngine.health_check` (method) `modules/auto_pivot.py:216` `def health_check(self, node_ip)`
- `AutoPivotEngine.health_check_all` (method) `modules/auto_pivot.py:237` `def health_check_all(self)`
- `AutoPivotEngine.get_active_routes` (method) `modules/auto_pivot.py:243` `def get_active_routes(self)`
- `AutoPivotEngine.get_reachable_hosts` (method) `modules/auto_pivot.py:259` `def get_reachable_hosts(self, node_ip)`
- `AutoPivotEngine.set_reachable_hosts` (method) `modules/auto_pivot.py:267` `def set_reachable_hosts(self, node_ip, hosts)`
- `AutoPivotEngine.set_route_priority` (method) `modules/auto_pivot.py:272` `def set_route_priority(self, node_ip, priority)`
- `AutoPivotEngine.suggest_next_pivot` (method) `modules/auto_pivot.py:352` `def suggest_next_pivot(self)`

## modules/auto_purple.py
Depends on: `core/config.py`, `core/logging.py`, `core/process.py`, `modules/detection_oracle.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleResult.to_csv_row` (method) `modules/auto_purple.py:146` `def to_csv_row(self)` -- Serialize to a flat dict suitable for CSV writer.
- `PurpleResult.to_dict` (method) `modules/auto_purple.py:160` `def to_dict(self)`
- `IPurpleLoop.execute_and_measure` (method) `modules/auto_purple.py:185` `def execute_and_measure(self, command, args, category)`
- `IPurpleLoop.measure_only` (method) `modules/auto_purple.py:193` `def measure_only(self, command, args, category)`
- `IPurpleLoop.engagement_score` (method) `modules/auto_purple.py:201` `def engagement_score(self)`
- `IPurpleLoop.export_dataset` (method) `modules/auto_purple.py:204` `def export_dataset(self)`
- `IPurpleLoop.export_report` (method) `modules/auto_purple.py:207` `def export_report(self)`
- `IPurpleEvaluator.last_results` (method) `modules/auto_purple.py:214` `def last_results(self, n)`
- `IPurpleEvaluator.category_accuracy` (method) `modules/auto_purple.py:217` `def category_accuracy(self, category)`
- `PurpleTeamLoop.__init__` (method) `modules/auto_purple.py:414` `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)`
- `PurpleTeamLoop.execute_and_measure` (method) `modules/auto_purple.py:443` `def execute_and_measure(self, command, args, category)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamLoop.measure_only` (method) `modules/auto_purple.py:493` `def measure_only(self, command, args, category)` -- Measure without executing — test if BT would detect the command.
- `PurpleTeamLoop.engagement_score` (method) `modules/auto_purple.py:529` `def engagement_score(self)` -- Aggregate detection score from all results in this session.
- `PurpleTeamLoop.export_dataset` (method) `modules/auto_purple.py:567` `def export_dataset(self)` -- Return the path to the CSV dataset file.
- `PurpleTeamLoop.export_report` (method) `modules/auto_purple.py:571` `def export_report(self)` -- Generate a full engagement report.
- `PurpleTeamLoop.last_results` (method) `modules/auto_purple.py:596` `def last_results(self, n)`
- `PurpleTeamLoop.category_accuracy` (method) `modules/auto_purple.py:599` `def category_accuracy(self, category)`
- `get_loop` (function) `modules/auto_purple.py:772` `def get_loop(bt_path, detection_delay, methods, auto_feedback)` -- Return (or create) the module-level PurpleTeamLoop singleton.
- `load_config_from_payload` (function) `modules/auto_purple.py:790` `def load_config_from_payload(params)` -- Extract purple_team config from payload.json params dict.

## modules/auto_registry.py
Depends on: `modules/command_executor.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_installer.py`, `modules/lazy_orchestrator_feedback.py`, `modules/orchestrator_config.py`
Imported by: `cli/commands/lazyops.py`, `modules/command_executor.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_installer.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/orchestrator_config.py`, `skills/lazyown_mcp.py`, `tests/test_auto_registry.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_runner.py`, `tests/test_loop_auto_orchestrator.py`
- `auto_verb_target` (function) `modules/auto_registry.py:35` `def auto_verb_target(command)` -- Return the target an ``auto <verb> <target>`` line carries, else ''.
- `verb_enabled` (function) `modules/auto_registry.py:189` `def verb_enabled(name)` -- Return whether one auto verb may be proposed or executed.
- `binary_available` (function) `modules/auto_registry.py:281` `def binary_available(name)` -- Return True when a command token can actually execute here.
- `missing_binary` (function) `modules/auto_registry.py:297` `def missing_binary(command)` -- Return the first binary a shell command needs but PATH lacks.
- `verb_gap` (function) `modules/auto_registry.py:309` `def verb_gap(verb)` -- Return a human reason when an automation verb cannot run, else ''.
- `verb_available` (function) `modules/auto_registry.py:321` `def verb_available(verb)` -- Return True when every binary an automation verb needs is installed.
- `service_tokens` (function) `modules/auto_registry.py:326` `def service_tokens(service_text)` -- Normalize a service asset value into matchable tokens.
- `iter_addon_triggers` (function) `modules/auto_registry.py:368` `def iter_addon_triggers()` -- Scan enabled lazyaddons for (name, trigger tokens) pairs.
- `iter_tool_triggers` (function) `modules/auto_registry.py:404` `def iter_tool_triggers()` -- Scan active pwntomate tools for (toolname, trigger tokens) pairs.
- `addon_hits_for` (function) `modules/auto_registry.py:427` `def addon_hits_for(service_text, limit)` -- Rank addon/tool names matching one service value.
- `propose_addon_intents` (function) `modules/auto_registry.py:453` `def propose_addon_intents(service_texts, target, limit)` -- Propose addon intents for discovered services.
- `is_routable_command` (function) `modules/auto_registry.py:479` `def is_routable_command(line)` -- Return True when the loop executor must route via the shell.
- `verbs` (function) `modules/auto_registry.py:497` `def verbs()` -- Return every canonical automation verb name.
- `is_shell_verb` (function) `modules/auto_registry.py:502` `def is_shell_verb(token)` -- Return True when ``token`` names a loop-routable shell verb.
- `build_command` (function) `modules/auto_registry.py:524` `def build_command(verb, target)` -- Build the shell command line for ``verb`` bound to ``target``.
- `verbs_for` (function) `modules/auto_registry.py:535` `def verbs_for(text)` -- Return enabled verbs whose keywords appear in the text.
- `propose_intents` (function) `modules/auto_registry.py:541` `def propose_intents(goal, target, finding_texts)` -- Propose ``auto <verb>`` intent summaries for planner candidates.
- `steps_for` (function) `modules/auto_registry.py:558` `def steps_for(text, target)` -- Translate an intent summary into shell command lines, or None.
- `_TeeCapture.__init__` (method) `modules/auto_registry.py:659` `def __init__(self, observer)`
- `_TeeCapture.write` (method) `modules/auto_registry.py:664` `def write(self, data)` -- Capture text and stream the chunk to the observer once.
- `execute_shell_verb` (function) `modules/auto_registry.py:677` `def execute_shell_verb(shell, command, timeout_sec, on_output)` -- Run a LazyOwn shell verb capturing stdout, with a hard timeout.
- `track_process` (function) `modules/auto_registry.py:787` `def track_process(process)` -- Register a live child process for global cancellation.
- `untrack_process` (function) `modules/auto_registry.py:792` `def untrack_process(process)` -- Drop a finished child process from the cancellation registry.
- `cancel_running_commands` (function) `modules/auto_registry.py:797` `def cancel_running_commands()` -- Kill every live streaming process group (operator Ctrl+C).
- `execute_streaming` (function) `modules/auto_registry.py:820` `def execute_streaming(command, on_output, timeout_sec)` -- Run a bash command streaming lines while capturing the output.

## modules/autonomous_exploit_engine.py
Depends on: `core/defaults.py`, `core/safe_exec.py`, `modules/auto_pivot.py`, `modules/db.py`
Imported by: `cli/commands/pwn.py`, `cli/commands/session_ops.py`, `modules/ai_exploit_chain.py`, `skills/lazyown_mcp.py`, `tests/test_phase1_data_gaps.py`
- `AutonomousExploitEngine.__init__` (method) `modules/autonomous_exploit_engine.py:114` `def __init__(self)`
- `AutonomousExploitEngine.get_instance` (method) `modules/autonomous_exploit_engine.py:134` `def get_instance(cls)`
- `AutonomousExploitEngine.hunt` (method) `modules/autonomous_exploit_engine.py:145` `def hunt(self, target, max_exploits, profile)` -- Execute a full autonomous exploitation chain against a target.
- `AutonomousExploitEngine.retry_with_credentials` (method) `modules/autonomous_exploit_engine.py:184` `def retry_with_credentials(self, target, credentials)` -- Re-execute exploit chain using captured credentials.
- `AutonomousExploitEngine.profile` (method) `modules/autonomous_exploit_engine.py:328` `def profile(self, target)` -- Build a TargetProfile from existing recon data.
- `AutonomousExploitEngine.rank_exploits` (method) `modules/autonomous_exploit_engine.py:389` `def rank_exploits(self, profile)` -- Rank exploit candidates by confidence for a given profile.
- `AutonomousExploitEngine.execute_candidate` (method) `modules/autonomous_exploit_engine.py:412` `def execute_candidate(self, candidate, profile)` -- Execute a single exploit candidate and return the result.
- `AutonomousExploitEngine.scan_vulnerabilities` (method) `modules/autonomous_exploit_engine.py:1648` `def scan_vulnerabilities(self, profile)` -- Scan for vulnerabilities using NSE output and heuristic version matching.
- `AutonomousExploitEngine.chain_privesc` (method) `modules/autonomous_exploit_engine.py:1963` `def chain_privesc(self, profile, session_id)` -- Run privilege escalation checks and attempt escalation techniques.
- `AutonomousExploitEngine.trigger_pivot` (method) `modules/autonomous_exploit_engine.py:2393` `def trigger_pivot(self, profile, session_id)` -- Discover internal interfaces and trigger auto-pivoting through a compromised host.
- `AutonomousExploitEngine.enable_stealth` (method) `modules/autonomous_exploit_engine.py:2519` `def enable_stealth(self, stealth_level)` -- Configure the engine's stealth level for evasion.
- `AutonomousExploitEngine.full_auto_pwn` (method) `modules/autonomous_exploit_engine.py:2583` `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` -- Execute the full autonomous exploit chain against a target.

## modules/aws_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `AWSAttackEngine.__init__` (method) `modules/aws_attacks.py:91` `def __init__(self, config)`
- `AWSAttackEngine.enumerate_iam_permissions` (method) `modules/aws_attacks.py:95` `def enumerate_iam_permissions(self)` -- Enumerate IAM permissions for the current user/role.
- `AWSAttackEngine.lambda_backdoor` (method) `modules/aws_attacks.py:127` `def lambda_backdoor(self, function_name)` -- Plan a Lambda backdoor for privilege escalation.
- `AWSAttackEngine.sts_role_chain` (method) `modules/aws_attacks.py:155` `def sts_role_chain(self, target_role_arn)` -- Enumerate and exploit STS AssumeRole privilege escalation chains.
- `AWSAttackEngine.ec2_user_data_exfil` (method) `modules/aws_attacks.py:181` `def ec2_user_data_exfil(self)` -- Extract sensitive data from EC2 instance user data and metadata.
- `AWSAttackEngine.s3_enumeration` (method) `modules/aws_attacks.py:206` `def s3_enumeration(self)` -- Enumerate S3 buckets and their permissions.
- `AWSAttackEngine.cloudformation_drift` (method) `modules/aws_attacks.py:242` `def cloudformation_drift(self)` -- Exploit CloudFormation for privilege escalation.
- `AWSAttackEngine.ec2_ssm_session_abuse` (method) `modules/aws_attacks.py:274` `def ec2_ssm_session_abuse(self)` -- Abuse SSM to gain shell access to EC2 instances.
- `AWSAttackEngine.summary` (method) `modules/aws_attacks.py:293` `def summary(self)`

## modules/backdoor/backdoor.c
Depends on: `modules/backdoor/keylogger.h`
- `bootRun` (function) `modules/backdoor/backdoor.c:18` `int bootRun()`
- `str_cut` (function) `modules/backdoor/backdoor.c:49` `char *
str_cut(char str[], int slice_from, int slice_to)`
- `Shell` (function) `modules/backdoor/backdoor.c:84` `void Shell()`
- `WinMain` (function) `modules/backdoor/backdoor.c:125` `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`

## modules/backdoor/keylogger.h
Imported by: `modules/backdoor/backdoor.c`
- `logg` (function) `modules/backdoor/keylogger.h:1` `DWORD WINAPI logg(LPVOID lpParam)`

## modules/backdoor/server.c
Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `contrib/legacy/lazygalazy.py`, `contrib/legacy/lazyhttpreverseshell.py`, `lazyc2.py`, `modules/lazy_proxy.py`, `modules/lazyown_bprfuzzer.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_lazy_proxy.py`, `utils.py`
- `main` (function) `modules/backdoor/server.c:10` `int main()`

## modules/beacon_config_builder.py
Depends on: `core/config.py`, `core/logging.py`, `modules/c2_profile_engine.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`
Imported by: `cli/commands/bof_registry.py`, `tests/test_beacon_config_builder.py`
- `BeaconConfig.to_gen_beacon_args` (method) `modules/beacon_config_builder.py:117` `def to_gen_beacon_args(self)` -- Produce CLI arguments for gen_beacon.sh.
- `BeaconConfig.to_go_implant_vars` (method) `modules/beacon_config_builder.py:137` `def to_go_implant_vars(self)` -- Produce template variables for the Go implant builder.
- `BeaconConfig.to_config_json` (method) `modules/beacon_config_builder.py:160` `def to_config_json(self)` -- Produce the config.json that beacons fetch on startup.
- `BeaconConfig.to_dict` (method) `modules/beacon_config_builder.py:185` `def to_dict(self)` -- Full serialization of beacon config.
- `BeaconConfigBuilder.__init__` (method) `modules/beacon_config_builder.py:245` `def __init__(self, payload)`
- `BeaconConfigBuilder.build` (method) `modules/beacon_config_builder.py:248` `def build(self, name)` -- Build a complete BeaconConfig.
- `BeaconConfigBuilder.from_payload` (method) `modules/beacon_config_builder.py:403` `def from_payload(cls, payload)` -- Build a BeaconConfigBuilder from a payload dictionary.
- `BeaconConfigBuilder.from_payload_file` (method) `modules/beacon_config_builder.py:408` `def from_payload_file(cls, path)` -- Build a BeaconConfigBuilder by loading payload.json from disk.
- `generate_bof_execution_command` (function) `modules/beacon_config_builder.py:416` `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)` -- Generate a ``bof:<url>`` command that the C beacon executes.

## modules/beacon_history.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/api_v1.py`, `tests/test_api_v1.py`, `tests/test_beacon_history.py`, `tests/test_security_lazyc2.py`
- `BeaconHistoryConfig.sessions_dir` (method) `modules/beacon_history.py:39` `def sessions_dir(self)` -- Return the resolved sessions directory under the base dir.
- `BeaconHistoryConfig.records_path` (method) `modules/beacon_history.py:43` `def records_path(self, client_id)` -- Resolve the history file path for a sanitised beacon client id.
- `sanitize_client_id` (function) `modules/beacon_history.py:70` `def sanitize_client_id(client_id)` -- Sanitise a beacon id to only URL/file-safe characters.
- `append_record` (function) `modules/beacon_history.py:82` `def append_record(record, config)` -- Append one beacon result record to the persistent JSONL history.
- `read_records` (function) `modules/beacon_history.py:116` `def read_records(client_id, config)` -- Read the ordered JSONL history for a beacon client id (oldest first).
- `records_path` (function) `modules/beacon_history.py:145` `def records_path(client_id, config)` -- Resolve the history file path for a beacon client id.

## modules/bin2img.py
- `binario_a_imagen` (function) `modules/bin2img.py:7` `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)`
- `main` (function) `modules/bin2img.py:54` `def main()`

## modules/bitm_engine.py
Imported by: `cli/commands/bitm.py`
- `bitm_start` (function) `modules/bitm_engine.py:257` `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)` -- Start a Browser-in-the-Middle attack.
- `bitm_stop` (function) `modules/bitm_engine.py:481` `def bitm_stop()` -- Stop a running BitM attack and clean up iptables.
- `bitm_status` (function) `modules/bitm_engine.py:539` `def bitm_status()` -- Return the current BitM attack status.
- `bitm_inject` (function) `modules/bitm_engine.py:572` `def bitm_inject(payload_name)` -- Inject an additional JS payload into an active BitM session.
- `bitm_harvest_stats` (function) `modules/bitm_engine.py:607` `def bitm_harvest_stats()` -- Return statistics on harvested credentials from the active/past campaign.
- `bitm_cleanup` (function) `modules/bitm_engine.py:642` `def bitm_cleanup()` -- Force-kill all BitM processes and remove the state file.
- `main` (function) `modules/bitm_engine.py:661` `def main()` -- CLI entry point — display BitM status from command line.

## modules/bof_registry.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/bof_registry.py`, `tests/test_bof_registry.py`
- `BofEntry.to_dict` (method) `modules/bof_registry.py:118` `def to_dict(self)` -- Serialize to dictionary.
- `BofEntry.from_dict` (method) `modules/bof_registry.py:137` `def from_dict(cls, raw)` -- Build from a dictionary.
- `BofCatalog.register` (method) `modules/bof_registry.py:167` `def register(self, entry)` -- Register a BOF entry in the catalog.
- `BofCatalog.register_many` (method) `modules/bof_registry.py:172` `def register_many(self, entries)` -- Register multiple BOF entries at once.
- `BofCatalog.get` (method) `modules/bof_registry.py:177` `def get(self, name)` -- Retrieve a BOF entry by name.
- `BofCatalog.search` (method) `modules/bof_registry.py:188` `def search(self, query)` -- Search catalog by keyword across name, description, and technique.
- `BofCatalog.list_by_category` (method) `modules/bof_registry.py:221` `def list_by_category(self, category)` -- Return all BOFs in a specific category.
- `BofCatalog.list_by_platform` (method) `modules/bof_registry.py:225` `def list_by_platform(self, platform)` -- Return all BOFs for a specific platform.
- `BofCatalog.list_all` (method) `modules/bof_registry.py:229` `def list_all(self)` -- Return all catalog entries sorted by name.
- `BofCatalog.to_dict` (method) `modules/bof_registry.py:233` `def to_dict(self)` -- Serialize the entire catalog to a dictionary.
- `BofCatalog.from_dict` (method) `modules/bof_registry.py:241` `def from_dict(cls, raw)` -- Build a catalog from a dictionary.
- `BofCatalog.load` (method) `modules/bof_registry.py:249` `def load(cls, path)` -- Load a catalog from a JSON file.
- `BofCatalog.save` (method) `modules/bof_registry.py:257` `def save(self, path)` -- Save the catalog to a JSON file.
- `BofValidator.compute_sha256` (method) `modules/bof_registry.py:515` `def compute_sha256(filepath)` -- Compute the SHA-256 hash of a file.
- `BofValidator.verify_entry` (method) `modules/bof_registry.py:524` `def verify_entry(entry, filepath)` -- Verify the SHA-256 of a downloaded BOF source matches the catalog.
- `BofValidator.validate_args` (method) `modules/bof_registry.py:540` `def validate_args(entry, args)` -- Validate that all required arguments are supplied.
- `BofRegistry.__init__` (method) `modules/bof_registry.py:559` `def __init__(self, sessions_dir)`
- `BofRegistry.install_dir` (method) `modules/bof_registry.py:565` `def install_dir(self)` -- Return the BOF installation directory.
- `BofRegistry.is_installed` (method) `modules/bof_registry.py:585` `def is_installed(self, name)` -- Return True if a BOF is installed.
- `BofRegistry.install` (method) `modules/bof_registry.py:590` `def install(self, entry)` -- Register a BOF as installed with current timestamp.
- `BofRegistry.uninstall` (method) `modules/bof_registry.py:611` `def uninstall(self, name, remove_files)` -- Unregister a BOF from the manifest and optionally remove its files.
- `BofRegistry.list_installed` (method) `modules/bof_registry.py:628` `def list_installed(self)` -- Return a list of all installed BOFs with metadata.
- `BofRegistry.get_install_info` (method) `modules/bof_registry.py:633` `def get_install_info(self, name)` -- Return installation metadata for a BOF, or None if not installed.
- `BofMarketplace.__init__` (method) `modules/bof_registry.py:651` `def __init__(self, sessions_dir, catalog)`
- `BofMarketplace.catalog` (method) `modules/bof_registry.py:662` `def catalog(self)` -- Return the catalog.
- `BofMarketplace.registry` (method) `modules/bof_registry.py:667` `def registry(self)` -- Return the registry.
- `BofMarketplace.search` (method) `modules/bof_registry.py:671` `def search(self, query)` -- Search the catalog and return enriched results with install status.
- `BofMarketplace.info` (method) `modules/bof_registry.py:690` `def info(self, name)` -- Get detailed information about a BOF by name.
- `BofMarketplace.install` (method) `modules/bof_registry.py:707` `def install(self, name)` -- Install a BOF from the catalog by name.
- `BofMarketplace.uninstall` (method) `modules/bof_registry.py:736` `def uninstall(self, name)` -- Uninstall a BOF by name.
- `BofMarketplace.list_installed` (method) `modules/bof_registry.py:749` `def list_installed(self)` -- List all installed BOFs with catalog enrichment.
- `BofMarketplace.list_missing_dependencies` (method) `modules/bof_registry.py:761` `def list_missing_dependencies(self, name)` -- Return a list of dependencies for a BOF that are not installed.
- `BofMarketplace.bulk_install` (method) `modules/bof_registry.py:769` `def bulk_install(self, names)` -- Install multiple BOFs at once.

## modules/c2_builder.py
Depends on: `core/validators.py`, `modules/metrics.py`, `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `C2Builder.__init__` (method) `modules/c2_builder.py:395` `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)`
- `C2Builder.run` (method) `modules/c2_builder.py:453` `def run(self, line, choice, use_tunnel)` -- Execute the full C2 build pipeline.

## modules/c2_messaging_base.py
- `SecureSessionManager.__init__` (method) `modules/c2_messaging_base.py:22` `def __init__(self, max_failed_attempts, lockout_duration, rate_limit, session_timeout)`
- `SecureSessionManager.register_failed_attempt` (method) `modules/c2_messaging_base.py:37` `def register_failed_attempt(self, user_id)` -- Record a failed authentication attempt for a user.
- `SecureSessionManager.check_lockout` (method) `modules/c2_messaging_base.py:46` `def check_lockout(self, user_id)` -- Check if a user is currently locked out due to failed attempts.
- `SecureSessionManager.check_rate_limit` (method) `modules/c2_messaging_base.py:61` `def check_rate_limit(self, user_id)` -- Check if a user has exceeded the command rate limit.
- `SecureSessionManager.create_session` (method) `modules/c2_messaging_base.py:79` `def create_session(self, user_id, client_id)` -- Create a new authenticated session for a user.
- `SecureSessionManager.validate_session` (method) `modules/c2_messaging_base.py:89` `def validate_session(self, user_id)` -- Check if a user session is still valid and refresh activity timestamp.
- `SecureSessionManager.set_client` (method) `modules/c2_messaging_base.py:106` `def set_client(self, user_id, client_id)` -- Assign a target C2 client to a user session.
- `SecureSessionManager.get_client` (method) `modules/c2_messaging_base.py:111` `def get_client(self, user_id)` -- Get the target C2 client assigned to a user session.
- `PayloadConfigAdapter.__init__` (method) `modules/c2_messaging_base.py:124` `def __init__(self, config_dict)`
- `PayloadConfigAdapter.get` (method) `modules/c2_messaging_base.py:132` `def get(self, key, default)`

## modules/c2_profile.py
Depends on: `core/logging.py`
- `C2Profile.jitter_delay` (method) `modules/c2_profile.py:101` `def jitter_delay(self)` -- Return the next sleep delay as a float in seconds.
- `C2Profile.get_uri` (method) `modules/c2_profile.py:117` `def get_uri(self, method)` -- Pick a random URI path from the appropriate HttpConfig.
- `C2Profile.build_headers` (method) `modules/c2_profile.py:128` `def build_headers(self, method)` -- Return the headers dict for the given HTTP method.
- `ProfileValidator.validate` (method) `modules/c2_profile.py:162` `def validate(self, profile)`
- `ProfileLoader.from_yaml` (method) `modules/c2_profile.py:200` `def from_yaml(path)` -- Load a C2Profile from a YAML file at *path*.
- `ProfileLoader.from_dict` (method) `modules/c2_profile.py:215` `def from_dict(d)` -- Construct a C2Profile from a plain Python dictionary.
- `ProfileLoader.to_dict` (method) `modules/c2_profile.py:254` `def to_dict(profile)` -- Convert a C2Profile to a plain Python dictionary.
- `ProfileLoader.save` (method) `modules/c2_profile.py:282` `def save(profile, path)` -- Serialise *profile* to a YAML file and return the written path.
- `ProfileRegistry.__init__` (method) `modules/c2_profile.py:457` `def __init__(self)`
- `ProfileRegistry.register` (method) `modules/c2_profile.py:464` `def register(self, name, profile)` -- Register *profile* under *name*, overwriting any previous entry.
- `ProfileRegistry.get` (method) `modules/c2_profile.py:473` `def get(self, name)` -- Return the profile registered under *name*.
- `ProfileRegistry.list_names` (method) `modules/c2_profile.py:485` `def list_names(self)` -- Return a sorted list of all registered profile names.
- `ProfileRegistry.load_from_directory` (method) `modules/c2_profile.py:493` `def load_from_directory(self, path)` -- Scan *path* for *.yaml files and register each as a profile.
- `ProfileApplier.apply_to_response` (method) `modules/c2_profile.py:529` `def apply_to_response(profile, response)` -- Patch the headers of a Flask response object to match the profile.
- `ProfileApplier.apply_to_session` (method) `modules/c2_profile.py:554` `def apply_to_session(profile, session)` -- Configure a requests.Session to mimic the profile's HTTP GET behavior.
- `ProfileApplier.get_beacon_config` (method) `modules/c2_profile.py:567` `def get_beacon_config(profile)` -- Return a JSON-serialisable dict suitable for embedding in a beacon handshake response.
- `get_registry` (function) `modules/c2_profile.py:595` `def get_registry()` -- Return the module-level singleton ProfileRegistry.
- `get_profile` (function) `modules/c2_profile.py:620` `def get_profile(name)` -- Return the named profile from the module singleton registry.
- `list_profiles` (function) `modules/c2_profile.py:625` `def list_profiles()` -- Return a sorted list of all registered profile names.

## modules/c2_profile_engine.py
Depends on: `cli/commands/enum.py`, `core/config.py`, `core/logging.py`
Imported by: `cli/commands/c2_profile.py`, `modules/beacon_config_builder.py`, `tests/test_c2_profile_engine.py`
- `TlsProfile.get_cipher_suites` (method) `modules/c2_profile_engine.py:144` `def get_cipher_suites(self)` -- Return cipher suites, resolving library alias if set.
- `TlsProfile.get_ja3_hash` (method) `modules/c2_profile_engine.py:155` `def get_ja3_hash(self)` -- Compute a JA3 fingerprint hash from the current profile.
- `TlsProfile.from_dict` (method) `modules/c2_profile_engine.py:173` `def from_dict(raw)` -- Build a TlsProfile from a configuration dictionary.
- `TlsProfile.to_dict` (method) `modules/c2_profile_engine.py:188` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `DnsProfile.build_query_subdomain` (method) `modules/c2_profile_engine.py:231` `def build_query_subdomain(self, data, packet_id)` -- Build a DNS query subdomain from encoded data and a packet ID.
- `DnsProfile.from_dict` (method) `modules/c2_profile_engine.py:261` `def from_dict(raw)` -- Build a DnsProfile from a configuration dictionary.
- `DnsProfile.to_dict` (method) `modules/c2_profile_engine.py:274` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `SmbProfile.from_dict` (method) `modules/c2_profile_engine.py:319` `def from_dict(raw)` -- Build an SmbProfile from a configuration dictionary.
- `SmbProfile.to_dict` (method) `modules/c2_profile_engine.py:333` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `WebSocketProfile.from_dict` (method) `modules/c2_profile_engine.py:375` `def from_dict(raw)` -- Build a WebSocketProfile from a configuration dictionary.
- `WebSocketProfile.to_dict` (method) `modules/c2_profile_engine.py:389` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `RotationSlot.is_available` (method) `modules/c2_profile_engine.py:429` `def is_available(self)` -- Return True if the cooldown window has elapsed.
- `RotationSlot.touch` (method) `modules/c2_profile_engine.py:436` `def touch(self)` -- Mark this slot as just used.
- `ProfileRotator.__init__` (method) `modules/c2_profile_engine.py:453` `def __init__(self, slots)`
- `ProfileRotator.current_slot` (method) `modules/c2_profile_engine.py:460` `def current_slot(self)` -- Return the currently active rotation slot.
- `ProfileRotator.transport` (method) `modules/c2_profile_engine.py:465` `def transport(self)` -- Return the transport type of the current slot.
- `ProfileRotator.rotate` (method) `modules/c2_profile_engine.py:469` `def rotate(self)` -- Advance to the next available slot and return it.
- `ProfileRotator.list_slots` (method) `modules/c2_profile_engine.py:487` `def list_slots(self)` -- Return a list of slot states for inspection.
- `ProfileValidator.validate_tls` (method) `modules/c2_profile_engine.py:511` `def validate_tls(profile)` -- Validate a TlsProfile and return error messages.
- `ProfileValidator.validate_dns` (method) `modules/c2_profile_engine.py:536` `def validate_dns(profile)` -- Validate a DnsProfile and return error messages.
- `ProfileValidator.validate_smb` (method) `modules/c2_profile_engine.py:556` `def validate_smb(profile)` -- Validate an SmbProfile and return error messages.
- `ProfileValidator.validate_websocket` (method) `modules/c2_profile_engine.py:576` `def validate_websocket(profile)` -- Validate a WebSocketProfile and return error messages.
- `ProfileValidator.validate_all` (method) `modules/c2_profile_engine.py:591` `def validate_all(self, tls, dns, smb, websocket)` -- Validate all provided profiles and return a dict of transport -> errors.
- `ProfileEngine.__init__` (method) `modules/c2_profile_engine.py:627` `def __init__(self, tls_profile, dns_profile, smb_profile, websocket_profile, rotation_slots)`
- `ProfileEngine.tls_profile` (method) `modules/c2_profile_engine.py:643` `def tls_profile(self)` -- Return the current TLS profile.
- `ProfileEngine.dns_profile` (method) `modules/c2_profile_engine.py:648` `def dns_profile(self)` -- Return the current DNS profile.
- `ProfileEngine.smb_profile` (method) `modules/c2_profile_engine.py:653` `def smb_profile(self)` -- Return the current SMB profile.
- `ProfileEngine.websocket_profile` (method) `modules/c2_profile_engine.py:658` `def websocket_profile(self)` -- Return the current WebSocket profile.
- `ProfileEngine.rotator` (method) `modules/c2_profile_engine.py:663` `def rotator(self)` -- Return the profile rotator.
- `ProfileEngine.active_transport` (method) `modules/c2_profile_engine.py:668` `def active_transport(self)` -- Return the currently active transport type.
- `ProfileEngine.rotate` (method) `modules/c2_profile_engine.py:672` `def rotate(self)` -- Advance to the next transport in the rotation queue.
- `ProfileEngine.validate` (method) `modules/c2_profile_engine.py:676` `def validate(self)` -- Validate all transport profiles and return error dict.
- `ProfileEngine.get_active_profile_dict` (method) `modules/c2_profile_engine.py:685` `def get_active_profile_dict(self)` -- Return a JSON-serializable dict of the active transport config.
- `ProfileEngine.get_all_profiles_dict` (method) `modules/c2_profile_engine.py:699` `def get_all_profiles_dict(self)` -- Return a JSON-serializable dict of all profiles.
- `ProfileEngine.from_dict` (method) `modules/c2_profile_engine.py:747` `def from_dict(cls, raw)` -- Build a ProfileEngine from a configuration dictionary.
- `ProfileEngine.from_payload` (method) `modules/c2_profile_engine.py:766` `def from_payload(cls, payload)` -- Build a ProfileEngine from a LazyOwn payload configuration dict.
- `ProfileEngine.from_config` (method) `modules/c2_profile_engine.py:771` `def from_config(cls, config)` -- Build a ProfileEngine from a LazyOwn Config object.

## modules/cal.sh
- `is_leap_year` (function) `modules/cal.sh:4` -- Función para calcular si un año es bisiesto
- `days_in_month` (function) `modules/cal.sh:14` -- Función para obtener el número de días en un mes
- `first_day_of_month` (function) `modules/cal.sh:31` -- Función para obtener el día de la semana del primer día del mes

## modules/cicd_enumerator.py
Imported by: `cli/commands/cicd.py`
- `CICDEnumerator.__init__` (method) `modules/cicd_enumerator.py:54` `def __init__(self, target_url, sessions_dir)`
- `CICDEnumerator.scan` (method) `modules/cicd_enumerator.py:60` `def scan(self)` -- Run all CI/CD scans.
- `CICDEnumerator.scan_build_log` (method) `modules/cicd_enumerator.py:297` `def scan_build_log(self, log_content, source)` -- Scan a build log for leaked secrets.
- `CICDEnumerator.generate_ci_attack_matrix` (method) `modules/cicd_enumerator.py:322` `def generate_ci_attack_matrix(self)` -- Generate a comprehensive CI/CD attack matrix.
- `CICDEnumerator.export_findings` (method) `modules/cicd_enumerator.py:387` `def export_findings(self)` -- Export CI/CD findings to a JSON file.

## modules/cli_auth.py
Depends on: `cli/engagement_hooks.py`, `core/config.py`, `modules/lazy_rbac.py`
Imported by: `cli/auto_crypto.py`, `cli/banner_config.py`, `cli/commands/cli_auth.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `cli/wizard.py`, `lazyown.py`, `modules/redteam_gym.py`, `tests/test_cli_auth_remember.py`, `tests/test_engagement_elo_and_methodology.py`
- `user_exists` (function) `modules/cli_auth.py:122` `def user_exists(username)` -- Check if a username already exists in users.json or RBAC store.
- `register` (function) `modules/cli_auth.py:145` `def register(username, password)` -- Register a new operator in users.json.
- `verify_password` (function) `modules/cli_auth.py:214` `def verify_password(username, password)` -- Verify a username/password against users.json using werkzeug.
- `login` (function) `modules/cli_auth.py:240` `def login(username, password, remember)` -- Authenticate a CLI operator and optionally persist a remember-me token.
- `logout` (function) `modules/cli_auth.py:293` `def logout()` -- Log out the current CLI operator and clear the remember-me token.
- `try_auto_login` (function) `modules/cli_auth.py:328` `def try_auto_login()` -- Attempt auto-login using the remember-me token from payload.json.
- `whoami` (function) `modules/cli_auth.py:366` `def whoami()` -- Return the currently logged-in CLI operator's identity.
- `get_current_operator` (function) `modules/cli_auth.py:396` `def get_current_operator()` -- Return the current operator username, or None if not logged in.
- `sync_elo_from_session` (function) `modules/cli_auth.py:408` `def sync_elo_from_session(elo)` -- Update the CLI session ELO from engagement state.
- `needs_login` (function) `modules/cli_auth.py:487` `def needs_login()` -- Check if the current session has a logged-in operator.

## modules/cloud_enum.py
Imported by: `cli/commands/cloud.py`
- `CloudEnumerator.__init__` (method) `modules/cloud_enum.py:34` `def __init__(self, provider, session, timeout)`
- `CloudEnumerator.detect_provider` (method) `modules/cloud_enum.py:47` `def detect_provider(self)` -- Auto-detect which cloud provider the host is running on.
- `CloudEnumerator.enumerate_metadata` (method) `modules/cloud_enum.py:75` `def enumerate_metadata(self)` -- Enumerate cloud instance metadata (IMDS).
- `CloudEnumerator.enumerate_storage` (method) `modules/cloud_enum.py:251` `def enumerate_storage(self, target_bucket)` -- Enumerate cloud storage buckets and objects.
- `CloudEnumerator.enumerate_iam` (method) `modules/cloud_enum.py:372` `def enumerate_iam(self)` -- Enumerate IAM roles, users, and policies.
- `CloudEnumerator.full_enumeration` (method) `modules/cloud_enum.py:576` `def full_enumeration(self)` -- Run full cloud enumeration: metadata + storage + IAM.

## modules/collab_bp.py
Depends on: `core/logging.py`, `modules/lazy_rbac.py`
Imported by: `cli/commands/collaboration.py`, `lazyc2.py`, `modules/engagement_hooks.py`, `modules/event_bus.py`, `skills/lazyown_mcp.py`, `tests/test_collab_and_onboarding.py`, `tests/test_core_modules.py`
- `login_required` (function) `modules/collab_bp.py:80` `def login_required(f)` -- No-op decorator when Flask-Login is unavailable.
- `decorated` (function) `modules/collab_bp.py:84` `def decorated()`
- `decorated` (function) `modules/collab_bp.py:124` `def decorated()`
- `decorator` (function) `modules/collab_bp.py:139` `def decorator(f)`
- `decorated` (function) `modules/collab_bp.py:141` `def decorated()`
- `ColabEvent.to_sse` (method) `modules/collab_bp.py:170` `def to_sse(self)`
- `EventBus.__init__` (method) `modules/collab_bp.py:198` `def __init__(self)`
- `EventBus.subscribe` (method) `modules/collab_bp.py:203` `def subscribe(self, subscriber_id)`
- `EventBus.unsubscribe` (method) `modules/collab_bp.py:215` `def unsubscribe(self, subscriber_id)`
- `EventBus.publish` (method) `modules/collab_bp.py:219` `def publish(self, event)`
- `EventBus.recent` (method) `modules/collab_bp.py:234` `def recent(self, n)`
- `EventBus.reset` (method) `modules/collab_bp.py:238` `def reset(self)`
- `LockManager.__init__` (method) `modules/collab_bp.py:263` `def __init__(self)`
- `LockManager.acquire` (method) `modules/collab_bp.py:267` `def acquire(self, target, operator, ttl_secs)`
- `LockManager.release` (method) `modules/collab_bp.py:279` `def release(self, target, operator)`
- `LockManager.status` (method) `modules/collab_bp.py:287` `def status(self, target)`
- `LockManager.all_locks` (method) `modules/collab_bp.py:292` `def all_locks(self)`
- `LockManager.reset` (method) `modules/collab_bp.py:304` `def reset(self)`
- `OperatorRegistry.__init__` (method) `modules/collab_bp.py:319` `def __init__(self)`
- `OperatorRegistry.join` (method) `modules/collab_bp.py:323` `def join(self, name)`
- `OperatorRegistry.heartbeat` (method) `modules/collab_bp.py:334` `def heartbeat(self, name)`
- `OperatorRegistry.leave` (method) `modules/collab_bp.py:340` `def leave(self, name)`
- `OperatorRegistry.active_operators` (method) `modules/collab_bp.py:345` `def active_operators(self)`
- `OperatorRegistry.reset` (method) `modules/collab_bp.py:356` `def reset(self)`
- `get_event_bus` (function) `modules/collab_bp.py:370` `def get_event_bus()`
- `get_lock_manager` (function) `modules/collab_bp.py:374` `def get_lock_manager()`
- `get_operator_registry` (function) `modules/collab_bp.py:378` `def get_operator_registry()`
- `publish_event` (function) `modules/collab_bp.py:382` `def publish_event(type, payload, operator)` -- Module-level convenience for other modules to broadcast events.
- `collab_ui` (function) `modules/collab_bp.py:396` `def collab_ui()`
- `stream` (function) `modules/collab_bp.py:411` `def stream()`
- `generate` (function) `modules/collab_bp.py:424` `def generate()`
- `operators` (function) `modules/collab_bp.py:458` `def operators()`
- `publish` (function) `modules/collab_bp.py:470` `def publish()`
- `lock` (function) `modules/collab_bp.py:483` `def lock()`
- `unlock` (function) `modules/collab_bp.py:504` `def unlock()`
- `locks` (function) `modules/collab_bp.py:522` `def locks()`
- `history` (function) `modules/collab_bp.py:537` `def history()`

## modules/colors.py
Imported by: `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyproxy.py`, `contrib/legacy/lazyseo.py`, `lazyc2.py`, `modules/llm_prompts.py`, `static/js/xterm.js`
- `retModel` (function) `modules/colors.py:40` `def retModel()` -- gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768...
- `delete_lines` (function) `modules/colors.py:68` `def delete_lines(content, to_delete)`
- `no_html` (function) `modules/colors.py:74` `def no_html(content)`


Next: [API_p10.md](API_p10.md)
