# API (page 10 of 29)
Previous: [API_p9.md](API_p9.md)

## modules/ad_gym.py
Depends on: `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`
- `load_index` (function) `modules/ad_gym.py:38` `def load_index(path)` -- Load the gym index, returning an empty mapping on failure.
- `vulnerabilities` (function) `modules/ad_gym.py:43` `def vulnerabilities(path)` -- Return every indexed lab vector.
- `get` (function) `modules/ad_gym.py:49` `def get(vuln_id, path)` -- Return one lab vector by id, or None.
- `chain_for` (function) `modules/ad_gym.py:58` `def chain_for(vuln_id, path)` -- Return the resolved chain for one lab vector, or None.
- `exploit_for` (function) `modules/ad_gym.py:68` `def exploit_for(vuln_id, path)` -- Return the exploit spec for one lab vector, or None.
- `validate_matrix` (function) `modules/ad_gym.py:78` `def validate_matrix(path)` -- Validate the index, exploit files and chains as one matrix.
- `summary` (function) `modules/ad_gym.py:127` `def summary(path)` -- Return counts by severity and service for operators.
- `readiness` (function) `modules/ad_gym.py:146` `def readiness()` -- Report whether the AD lab container is attackable right now.
- `main` (function) `modules/ad_gym.py:166` `def main()` -- CLI: list | validate | summary | readiness.

## modules/adcs_attacks.py
Imported by: `cli/commands/exploit_migrated.py`
- `CertificateTemplate.esc_vulnerabilities` (method) `modules/adcs_attacks.py:35` `def esc_vulnerabilities(self)` -- Determine which ESC attack paths apply to this template.
- `ADCSCertipyWrapper.__init__` (method) `modules/adcs_attacks.py:80` `def __init__(self, certipy_path, timeout)`
- `ADCSCertipyWrapper.find_certificate_authorities` (method) `modules/adcs_attacks.py:113` `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` -- Enumerate certificate authorities in an Active Directory domain.
- `ADCSCertipyWrapper.enumerate_templates` (method) `modules/adcs_attacks.py:189` `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` -- Enumerate vulnerable certificate templates.
- `ADCSCertipyWrapper.request_certificate_esc1` (method) `modules/adcs_attacks.py:268` `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` -- ESC1: Request a certificate with a user-supplied subject alternative name.
- `ADCSCertipyWrapper.request_certificate_esc8` (method) `modules/adcs_attacks.py:322` `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` -- ESC8: HTTP-based certificate enrollment (NTLM relay to AD CS).
- `ADCSCertipyWrapper.authenticate_with_certificate` (method) `modules/adcs_attacks.py:367` `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` -- Authenticate to the domain using a certificate and retrieve NT hash.
- `ADCSCertipyWrapper.assess_vulnerability` (method) `modules/adcs_attacks.py:411` `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` -- Run a full AD CS vulnerability assessment.

## modules/addon_updater.py
Depends on: `core/logging.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/marketplace.py`, `tests/test_addon_updater.py`
- `AddonUpdateResult.to_dict` (method) `modules/addon_updater.py:46` `def to_dict(self)` -- Return a JSON-serializable view.
- `load_addons` (function) `modules/addon_updater.py:73` `def load_addons(lazyaddons_dir)` -- Load every lazyaddon with its update metadata.
- `update_addon` (function) `modules/addon_updater.py:166` `def update_addon(name, lazyaddons_dir, root, dry_run)` -- Update one addon through ``git pull --ff-only``.
- `update_all` (function) `modules/addon_updater.py:260` `def update_all(names, lazyaddons_dir, root, dry_run, audit_path)` -- Update every opted-in addon or an explicit name list.

## modules/agent_runner.py
Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/lazy_agent.py`, `modules/vulnbot.py`, `tests/test_lazy_streaming.py`
- `configure_logging` (function) `modules/agent_runner.py:64` `def configure_logging(debug)`
- `AgentTool.__init__` (method) `modules/agent_runner.py:73` `def __init__(self, name, description, func, parameters, required)`
- `AgentTool.to_api_format` (method) `modules/agent_runner.py:81` `def to_api_format(self)`
- `AgentTool.execute` (method) `modules/agent_runner.py:87` `def execute(self)` -- Execute with argument validation and clear formatting.
- `ASTToolExtractor.extract_commands_from_file` (method) `modules/agent_runner.py:142` `def extract_commands_from_file(file_path, prefix)`
- `AgentRunner.__init__` (method) `modules/agent_runner.py:197` `def __init__(self, model, system_prompt, max_iterations)`
- `AgentRunner.register_tool` (method) `modules/agent_runner.py:222` `def register_tool(self, tool)`
- `AgentRunner.register_tool_from_instance` (method) `modules/agent_runner.py:225` `def register_tool_from_instance(self, func)` -- Wrap a plain function as an AgentTool using its signature and docstring.
- `AgentRunner.register_tools_from_metadata` (method) `modules/agent_runner.py:243` `def register_tools_from_metadata(self, commands, executor)`
- `make_executor` (function) `modules/agent_runner.py:247` `def make_executor(cmd_name)`
- `wrapper` (function) `modules/agent_runner.py:248` `def wrapper(command)`
- `AgentRunner.get_tools_for_api` (method) `modules/agent_runner.py:270` `def get_tools_for_api(self)`
- `AgentRunner.run` (method) `modules/agent_runner.py:275` `def run(self, user_input)`
- `LazyOwnShellWrapper.__init__` (method) `modules/agent_runner.py:489` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/agent_runner.py:519` `def execute_command(self, command)` -- Execute a command with a timeout using threading.
- `target` (function) `modules/agent_runner.py:526` `def target()`
- `LazyOwnShellWrapper.get_commands_summary` (method) `modules/agent_runner.py:556` `def get_commands_summary(self)`
- `VulnBotCLI.__init__` (method) `modules/agent_runner.py:564` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.process_request` (method) `modules/agent_runner.py:619` `def process_request(self, user_input)`
- `interactive_mode` (function) `modules/agent_runner.py:624` `def interactive_mode(bot)`
- `parse_args` (function) `modules/agent_runner.py:648` `def parse_args()`
- `main` (function) `modules/agent_runner.py:658` `def main()`

## modules/ai_exploit_chain.py
Depends on: `modules/autonomous_exploit_engine.py`
Imported by: `cli/commands/pwn.py`, `skills/mcp_tools/exploit_chain.py`, `tests/test_engine_mediator.py`
- `AIExploitChainer.__init__` (method) `modules/ai_exploit_chain.py:236` `def __init__(self)`
- `AIExploitChainer.reason` (method) `modules/ai_exploit_chain.py:262` `def reason(self, context)` -- Analyze context failures and produce the next best exploit candidate.
- `AIExploitChainer.evaluate_failure` (method) `modules/ai_exploit_chain.py:283` `def evaluate_failure(result)` -- Classify the reason for an exploit failure by output pattern matching.
- `AIExploitChainer.select_next_strategy` (method) `modules/ai_exploit_chain.py:295` `def select_next_strategy(self, context)` -- Select the next strategy to attempt based on context and failures.
- `AIExploitChainer.estimate_confidence` (method) `modules/ai_exploit_chain.py:326` `def estimate_confidence(self, strategy, profile)` -- Estimate confidence (0.0-1.0) for a strategy against a target profile.
- `AIExploitChainer.build_chain_plan` (method) `modules/ai_exploit_chain.py:368` `def build_chain_plan(self, context)` -- Build a full multi-step exploitation plan following the kill chain.
- `AIExploitChainer.adapt_chain` (method) `modules/ai_exploit_chain.py:405` `def adapt_chain(self, context, new_info)` -- Adapt the chain plan based on newly discovered information.

## modules/ai_fallback.py
Depends on: `core/config.py`, `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`, `tests/test_llm_orchestrator.py`
- `call` (function) `modules/ai_fallback.py:280` `def call(prompt, system, api_key, max_tokens, temperature)` -- Call the orchestrator chain first, then Groq (explicit key only), Ollama, TopoSwarm, and finally return the help...

## modules/ai_model.py
Depends on: `core/logging.py`, `modules/llm_factory.py`
Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_client.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`
- `AIModel.generate` (method) `modules/ai_model.py:60` `def generate(self, prompt)` -- Return a non-streaming completion for ``prompt``.
- `AIModel.stream_generate` (method) `modules/ai_model.py:64` `def stream_generate(self, prompt)` -- Yield streaming completion chunks for ``prompt``.
- `AIModel.complete` (method) `modules/ai_model.py:67` `def complete(self, system, user, max_tokens, temperature)` -- Return a completion conforming to ``core.protocols.LLMBackend``.
- `_LazyImporter.groq` (method) `modules/ai_model.py:109` `def groq(cls)`
- `_LazyImporter.openai` (method) `modules/ai_model.py:117` `def openai(cls)`
- `_LazyImporter.anthropic` (method) `modules/ai_model.py:125` `def anthropic(cls)`
- `GroqModel.__init__` (method) `modules/ai_model.py:141` `def __init__(self, api_key, model)`
- `GroqModel.generate` (method) `modules/ai_model.py:159` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `GroqModel.stream_generate` (method) `modules/ai_model.py:187` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `GroqModel.complete` (method) `modules/ai_model.py:220` `def complete(self, system, user, max_tokens, temperature)` -- Return a chat completion using native role separation.
- `OllamaModel.__init__` (method) `modules/ai_model.py:256` `def __init__(self, model, host)`
- `OllamaModel.generate` (method) `modules/ai_model.py:264` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `OllamaModel.stream_generate` (method) `modules/ai_model.py:285` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `LlamaCppModel.__init__` (method) `modules/ai_model.py:328` `def __init__(self, model, host)`
- `LlamaCppModel.generate` (method) `modules/ai_model.py:366` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `LlamaCppModel.stream_generate` (method) `modules/ai_model.py:386` `def stream_generate(self, prompt)` -- Yield streamed completion deltas for ``prompt``.
- `LlamaCppModel.complete` (method) `modules/ai_model.py:417` `def complete(self, system, user, max_tokens, temperature)` -- Role-aware completion through the chat endpoint.
- `OpenAIModel.__init__` (method) `modules/ai_model.py:444` `def __init__(self, api_key, model)`
- `OpenAIModel.generate` (method) `modules/ai_model.py:448` `def generate(self, prompt)`
- `OpenAIModel.stream_generate` (method) `modules/ai_model.py:459` `def stream_generate(self, prompt)`
- `OpenAIModel.complete` (method) `modules/ai_model.py:474` `def complete(self, system, user, max_tokens, temperature)`
- `AnthropicModel.__init__` (method) `modules/ai_model.py:503` `def __init__(self, api_key, model)`
- `AnthropicModel.generate` (method) `modules/ai_model.py:507` `def generate(self, prompt)`
- `AnthropicModel.stream_generate` (method) `modules/ai_model.py:519` `def stream_generate(self, prompt)`
- `AnthropicModel.complete` (method) `modules/ai_model.py:533` `def complete(self, system, user, max_tokens, temperature)`
- `DeepSeekModel.__init__` (method) `modules/ai_model.py:560` `def __init__(self, api_key, model)`
- `DeepSeekModel.generate` (method) `modules/ai_model.py:567` `def generate(self, prompt)`
- `DeepSeekModel.stream_generate` (method) `modules/ai_model.py:578` `def stream_generate(self, prompt)`
- `DeepSeekModel.complete` (method) `modules/ai_model.py:593` `def complete(self, system, user, max_tokens, temperature)`
- `OpenCodeModel.__init__` (method) `modules/ai_model.py:626` `def __init__(self, api_key, model, base_url)`
- `OpenCodeModel.generate` (method) `modules/ai_model.py:639` `def generate(self, prompt)`
- `OpenCodeModel.stream_generate` (method) `modules/ai_model.py:650` `def stream_generate(self, prompt)`
- `OpenCodeModel.complete` (method) `modules/ai_model.py:665` `def complete(self, system, user, max_tokens, temperature)`

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
Depends on: `core/console.py`, `modules/atomic_resolver.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `cli/orchestrator_assets_tabs.py`, `cli/recommendation_signals.py`, `modules/beacon_kinds.py`, `modules/emulation_runner.py`, `modules/operation.py`, `modules/playbook_chain.py`, `modules/selection/playbook.py`, `tests/test_atomic_loop.py`, `tests/test_emulation_runner.py`, `tests/test_playbook_chain.py`, `tests/test_selectors_capabilities.py`
- `AptPlaybook.from_dict` (method) `modules/apt_playbooks.py:137` `def from_dict(cls, data)`
- `AptPlaybook.to_summary` (method) `modules/apt_playbooks.py:163` `def to_summary(self)`
- `AptPlaybookEngine.__init__` (method) `modules/apt_playbooks.py:179` `def __init__(self, playbook_dir)`
- `AptPlaybookEngine.list_playbooks` (method) `modules/apt_playbooks.py:196` `def list_playbooks(self)`
- `AptPlaybookEngine.get` (method) `modules/apt_playbooks.py:199` `def get(self, name)`
- `AptPlaybookEngine.validate` (method) `modules/apt_playbooks.py:203` `def validate(self, pb, atomic_path)` -- Validate that all referenced atomic tests exist locally.
- `AptPlaybookEngine.generate_attack_plan` (method) `modules/apt_playbooks.py:278` `def generate_attack_plan(self, pb, output_path)` -- Generate a legacy ``attack_plan.yaml`` from an enriched APT playbook.
- `AptPlaybookEngine.report_json` (method) `modules/apt_playbooks.py:295` `def report_json(self, pb, output_path)` -- Write a structured JSON report of the playbook for the operator.

## modules/askpass.py
Depends on: `core/config.py`
Imported by: `lazyown.py`, `tests/test_askpass.py`
- `display_available` (function) `modules/askpass.py:24` `def display_available()` -- Return whether a graphical display server is reachable.
- `find_native_askpass` (function) `modules/askpass.py:36` `def find_native_askpass()` -- Return the first installed native askpass helper, empty when none.
- `create_zenity_askpass` (function) `modules/askpass.py:65` `def create_zenity_askpass()` -- Write a temporary askpass helper backed by zenity or yad.
- `graphical_askpass_path` (function) `modules/askpass.py:96` `def graphical_askpass_path()` -- Return the best graphical askpass helper path, empty when unusable.
- `graphical_sudo_available` (function) `modules/askpass.py:116` `def graphical_sudo_available()` -- Return whether a graphical sudo prompt can be shown right now.
- `graphical_sudo_env` (function) `modules/askpass.py:125` `def graphical_sudo_env()` -- Return the environment variables that route sudo through the GUI.
- `sudo_graphical_requested` (function) `modules/askpass.py:138` `def sudo_graphical_requested(payload)` -- Return whether the operator asked for graphical sudo prompts.

## modules/asset_graph.py
Imported by: `skills/autonomous_daemon.py`
- `coverage_for` (function) `modules/asset_graph.py:12` `def coverage_for(db, workspace_id, scope)` -- Report tested scope assets versus total scope from the campaign db.

## modules/atomic_cli.py
Depends on: `core/autonomous.py`, `core/console.py`, `core/hardening.py`, `core/logging.py`, `modules/atomic_resolver.py`, `modules/bof_delivery.py`, `modules/lazy_osinfer.py`, `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_atomic_headless.py`, `tests/test_atomic_loop.py`, `tests/test_lazy_handoff.py`
- `default_platform_for_target` (function) `modules/atomic_cli.py:39` `def default_platform_for_target(params)` -- Return the OS-aware platform default for the active target.
- `parse_atomic_line` (function) `modules/atomic_cli.py:64` `def parse_atomic_line(line)` -- Parse free-form CLI args into a structured request.
- `run_atomic_tests` (function) `modules/atomic_cli.py:255` `def run_atomic_tests(params, line, shell)` -- Execute the atomic_tests workflow (secure + agent-safe).
- `run_atomic_gen` (function) `modules/atomic_cli.py:466` `def run_atomic_gen(params, line, shell)` -- Generate test + cleanup scripts for one technique or GUID.

## modules/atomic_enricher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_parquet_db.py`, `skills/mcp_tools/atomic_resolve.py`, `skills/mcp_tools/atomic_search.py`, `tests/test_core_modules.py`
- `enrich` (function) `modules/atomic_enricher.py:173` `def enrich(force)` -- Build enriched parquet.
- `load_enriched` (function) `modules/atomic_enricher.py:215` `def load_enriched()` -- Load enriched parquet, building it first if it doesn't exist.
- `query_atomic` (function) `modules/atomic_enricher.py:232` `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team technique catalogue.

## modules/atomic_exploit_bridge.py
Depends on: `core/config.py`, `core/logging.py`, `core/safe_exec.py`, `modules/__init__.py`, `modules/c2_surfaces.py`, `modules/emulation_runner.py`, `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`, `modules/outcome_bus.py`, `modules/shell_session_store.py`, `modules/world_model.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/ad_gym.py`, `modules/autonomous_exploit_engine.py`, `modules/bof_delivery.py`, `modules/c2_agent.py`, `modules/emulation_runner.py`, `modules/lazy_fallback.py`, `modules/lazy_handoff.py`, `modules/lazy_loop.py`, `modules/loop/daemon_reward.py`, `modules/loop_ai_bridge.py`, `modules/metasploitable_gym.py`, `modules/redteam_gym.py`, `modules/shell_session_store.py`, `modules/winbox_gym.py`, `skills/autonomous_daemon.py`, `skills/mcp_tools/atomic_clean.py`, `skills/mcp_tools/atomic_shell.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_c2_surfaces.py`, `tests/test_emulation_runner.py`, `tests/test_gym_cli.py`, `tests/test_lazy_handoff.py`, `tests/test_metasploitable_gym.py`, `tests/test_outcome_bus.py`
- `shell_output_evidence` (function) `modules/atomic_exploit_bridge.py:84` `def shell_output_evidence(output)` -- Return True only when output carries genuine interactive-shell evidence.
- `ExploitSpec.severity_rank` (method) `modules/atomic_exploit_bridge.py:138` `def severity_rank(self)` -- Return numeric severity for ranking (mirrors the engine).
- `ExploitSpec.to_dict` (method) `modules/atomic_exploit_bridge.py:142` `def to_dict(self)` -- Return a JSON-serializable view.
- `validate_spec` (function) `modules/atomic_exploit_bridge.py:171` `def validate_spec(data, filename)` -- Validate raw YAML data against the exploit schema.
- `load_all` (function) `modules/atomic_exploit_bridge.py:247` `def load_all(exploits_dir)` -- Load every enabled, valid exploit YAML (skips the rest loudly).
- `match_score` (function) `modules/atomic_exploit_bridge.py:302` `def match_score(spec, service, product, version, os_hint)` -- Score a spec against one discovered service (0 when no match).
- `parse_scan_xml` (function) `modules/atomic_exploit_bridge.py:335` `def parse_scan_xml(xml_path)` -- Parse open TCP ports from a lazynmap XML file (stdlib only).
- `auto` (function) `modules/atomic_exploit_bridge.py:372` `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)` -- Pwntomate-style sweep: triggers from scan XML, ranked, stop on SHELL.
- `rank` (function) `modules/atomic_exploit_bridge.py:477` `def rank(services, exploits_dir, os_hint)` -- Rank every spec against discovered services (severity, then confidence).
- `build_commands` (function) `modules/atomic_exploit_bridge.py:546` `def build_commands(spec, rhost, lhost, lport, port)` -- Substitute ``{tokens}`` into a spec's commands (no shell involved).
- `detect_shell` (function) `modules/atomic_exploit_bridge.py:564` `def detect_shell(spec, output)` -- Return True when output carries genuine shell evidence.
- `run_spec` (function) `modules/atomic_exploit_bridge.py:613` `def run_spec(spec, rhost, lhost, lport, port)` -- Execute a spec's commands in order; stop at the first SHELL hit.
- `open_shell` (function) `modules/atomic_exploit_bridge.py:706` `def open_shell(target, services, lhost, exploits_dir, attempts, privilege)` -- Return the first exec-capable spec with a live multiplexed session.
- `_ShellSession.__init__` (method) `modules/atomic_exploit_bridge.py:770` `def __init__(self, target, port, sock, owner)`
- `_ShellSession.alive` (method) `modules/atomic_exploit_bridge.py:780` `def alive(self, timeout)` -- Return True when the session answers a no-op probe.
- `_ShellSession.run` (method) `modules/atomic_exploit_bridge.py:787` `def run(self, command, timeout)` -- Run one command, return stdout+stderr (never raises).
- `_ShellSession.close` (method) `modules/atomic_exploit_bridge.py:829` `def close(self)` -- End the remote shell cleanly so its listener dies too.
- `record_shell_outcome` (function) `modules/atomic_exploit_bridge.py:880` `def record_shell_outcome(target, via)` -- Mark one target as compromised after an operator obtains a shell.
- `live_sessions` (function) `modules/atomic_exploit_bridge.py:909` `def live_sessions()` -- Return in-process shell sessions without probing the target.
- `close_sessions` (function) `modules/atomic_exploit_bridge.py:928` `def close_sessions(target)` -- Close cached sessions (all, or one target).
- `cleanup_target` (function) `modules/atomic_exploit_bridge.py:976` `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)` -- Clean up after an engagement (soft default, hard on request).
- `ensure_session` (function) `modules/atomic_exploit_bridge.py:1068` `def ensure_session(spec, target, lhost)` -- Return a live multiplexed session, establishing it when needed.
- `remote_exec` (function) `modules/atomic_exploit_bridge.py:1166` `def remote_exec(spec, target, command, lhost)` -- Run one command through the persistent multiplexed session.
- `interactive_shell` (function) `modules/atomic_exploit_bridge.py:1184` `def interactive_shell(target, lhost, interactive, exploits_dir)` -- Open a multiplexed session; drop into a REPL only when allowed.
- `emulate` (function) `modules/atomic_exploit_bridge.py:1239` `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...` -- Execute emulation tests on the target through one working shell.
- `record_outcome` (function) `modules/atomic_exploit_bridge.py:1273` `def record_outcome(spec, target, shell, output, task_id, intent_id, surfaces_dir, port, service, product, version...` -- Feed one exploit outcome to every shared surface through the bus.
- `main` (function) `modules/atomic_exploit_bridge.py:1361` `def main()` -- CLI: validate | list | rank | run (used by the addon and operators).

## modules/atomic_resolver.py
Depends on: `core/logging.py`, `core/safe_exec.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/apt_playbooks.py`, `modules/atomic_cli.py`, `modules/emulation_runner.py`, `modules/ttpscope_bridge.py`, `skills/mcp_tools/atomic_resolve.py`, `skills/mcp_tools/ttp_chain.py`, `tests/test_atomic_loop.py`, `tests/test_atomic_resolver.py`
- `normalize_mitre_id` (function) `modules/atomic_resolver.py:66` `def normalize_mitre_id(raw)` -- Normalize and validate a MITRE technique ID.
- `is_mitre_id` (function) `modules/atomic_resolver.py:84` `def is_mitre_id(raw)` -- Return True when *raw* looks like a MITRE technique ID.
- `normalize_guid` (function) `modules/atomic_resolver.py:93` `def normalize_guid(raw)` -- Normalize and validate an Atomic test GUID.
- `is_guid` (function) `modules/atomic_resolver.py:109` `def is_guid(raw)` -- Return True when *raw* looks like an Atomic test GUID.
- `normalize_platform` (function) `modules/atomic_resolver.py:118` `def normalize_platform(raw)` -- Validate a platform against the allowlist.
- `AtomicTest.mitre_url` (method) `modules/atomic_resolver.py:147` `def mitre_url(self)` -- Return the ATT&CK URL for this test.
- `AtomicTest.to_dict` (method) `modules/atomic_resolver.py:151` `def to_dict(self)` -- Return a JSON-serializable view.
- `AtomicResolver.__init__` (method) `modules/atomic_resolver.py:226` `def __init__(self, atomics_dir)`
- `AtomicResolver.available` (method) `modules/atomic_resolver.py:233` `def available(self)` -- Return True when the atomics directory exists.
- `AtomicResolver.ensure_repo` (method) `modules/atomic_resolver.py:237` `def ensure_repo(self)` -- Clone or pull the Atomic Red Team repo without shell.
- `AtomicResolver.build_index` (method) `modules/atomic_resolver.py:265` `def build_index(self, force)` -- Build the MITRE -> [GUID] index (cached unless *force*).
- `AtomicResolver.guids_for_technique` (method) `modules/atomic_resolver.py:305` `def guids_for_technique(self, mitre_id)` -- Return GUIDs registered for a technique ID (empty when unknown).
- `AtomicResolver.get_by_guid` (method) `modules/atomic_resolver.py:311` `def get_by_guid(self, guid)` -- Return the test for a GUID, or None when unknown.
- `AtomicResolver.list_for_technique` (method) `modules/atomic_resolver.py:317` `def list_for_technique(self, mitre_id, platform)` -- List tests for a technique, optionally filtered by platform.
- `AtomicResolver.resolve` (method) `modules/atomic_resolver.py:334` `def resolve(self, query, platform)` -- Resolve a MITRE ID, GUID, or prefix to matching tests.
- `AtomicResolver.chain` (method) `modules/atomic_resolver.py:380` `def chain(self, techniques, platform, first_match_only)` -- Translate an ordered APT technique chain to concrete tests.
- `AtomicResolver.stats` (method) `modules/atomic_resolver.py:415` `def stats(self)` -- Return index counters.
- `get_resolver` (function) `modules/atomic_resolver.py:424` `def get_resolver(atomics_dir)` -- Return the module-level resolver singleton.
- `resolve_technique` (function) `modules/atomic_resolver.py:432` `def resolve_technique(mitre_id, platform, atomics_dir)` -- Resolve a technique to JSON-serializable test dicts.
- `resolve_chain` (function) `modules/atomic_resolver.py:442` `def resolve_chain(techniques, platform, atomics_dir)` -- Translate a technique chain to JSON-serializable test dicts.
- `build_variables` (function) `modules/atomic_resolver.py:452` `def build_variables(test, rhost, domain, rport, username, password)` -- Build #{variable} substitution map for a test.
- `render_command` (function) `modules/atomic_resolver.py:488` `def render_command(template, variables)` -- Substitute #{variables} without shell interpretation.
- `technique_env_override` (function) `modules/atomic_resolver.py:496` `def technique_env_override()` -- Return atomics dir override from env (empty when unset).

## modules/attack_surface3d.py
Depends on: `cli/surface_graph.py`, `modules/__init__.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/intel_fusion.py`
Imported by: `cli/commands/surface.py`, `lazyc2.py`, `modules/sinks/attack_graph.py`, `tests/test_attack_surface3d.py`
- `build_attack_graph` (function) `modules/attack_surface3d.py:148` `def build_attack_graph(sessions_dir, payload_path, est_cap)` -- Fuse surface scans with campaign intel into one C2-centred graph.
- `add_edge` (function) `modules/attack_surface3d.py:156` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation between known nodes.
- `tag` (function) `modules/attack_surface3d.py:167` `def tag(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `refresh_summary` (function) `modules/attack_surface3d.py:480` `def refresh_summary(graph, sessions_dir)` -- Score exposure into intel_summary.json for the autonomous loop.

## modules/auto_loop_memory.py
Imported by: `modules/lazy_loop.py`, `modules/loop/worker_memory.py`, `tests/test_auto_loop_memory.py`, `tests/test_failure_memory_veto.py`
- `FailureMemory.__init__` (method) `modules/auto_loop_memory.py:56` `def __init__(self, filepath)`
- `FailureMemory.path` (method) `modules/auto_loop_memory.py:63` `def path(self)` -- Backing file path for administrative inspection.
- `FailureMemory.make_key` (method) `modules/auto_loop_memory.py:68` `def make_key(target, category, command)` -- Build the storage key; raises on empty target or command.
- `FailureMemory.base_of` (method) `modules/auto_loop_memory.py:75` `def base_of(command)` -- Extract the base command from a full command string.
- `FailureMemory.record_failure` (method) `modules/auto_loop_memory.py:79` `def record_failure(self, target, category, command)` -- Increment and persist the failure count; returns the new count.
- `FailureMemory.failure_count` (method) `modules/auto_loop_memory.py:89` `def failure_count(self, target, category, command)` -- Current persisted failure count for the combination.
- `FailureMemory.count_for_base` (method) `modules/auto_loop_memory.py:94` `def count_for_base(self, target, base_command)` -- Failure hits aggregated across exact keys whose base matches.
- `FailureMemory.veto_base` (method) `modules/auto_loop_memory.py:105` `def veto_base(self, target, base_command)` -- Mark a base command as blocked by the stuck-loop detector.
- `FailureMemory.is_blocked` (method) `modules/auto_loop_memory.py:115` `def is_blocked(self, target, base_command, bonus_key)` -- True when the base is vetoed or its failure count hit the threshold.
- `FailureMemory.failure_count_strict` (method) `modules/auto_loop_memory.py:123` `def failure_count_strict(self, target, key)` -- Failure count for a raw storage key already containing separators.
- `FailureMemory.blocked_bases` (method) `modules/auto_loop_memory.py:128` `def blocked_bases(self, target)` -- All blocked base commands for the target (vetoed plus past threshold).
- `FailureMemory.clear_target` (method) `modules/auto_loop_memory.py:140` `def clear_target(self, target)` -- Forget every record for a target (manual reset path).
- `FailureMemory.sanctioned_bases` (method) `modules/auto_loop_memory.py:146` `def sanctioned_bases(self, target)` -- Administrative view: counts above threshold with their last timestamp.
- `FailureMemory.save` (method) `modules/auto_loop_memory.py:166` `def save(self)`
- `DecisionPersistence.__init__` (method) `modules/auto_loop_memory.py:215` `def __init__(self, filepath)`
- `DecisionPersistence.push` (method) `modules/auto_loop_memory.py:220` `def push(self, command, reason)` -- Park one decision for later consumption (newest first).
- `DecisionPersistence.pop` (method) `modules/auto_loop_memory.py:229` `def pop(self)` -- Consume and persist-removal of the newest parked decision.
- `DecisionPersistence.peek` (method) `modules/auto_loop_memory.py:237` `def peek(self)` -- Newest parked decision without consuming it.
- `DecisionPersistence.save` (method) `modules/auto_loop_memory.py:244` `def save(self)`

## modules/auto_pivot.py
Imported by: `modules/autonomous_exploit_engine.py`, `skills/mcp_tools/pivot_status.py`
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
Depends on: `core/config.py`, `core/host_policy.py`, `modules/__init__.py`, `modules/chain_registry.py`, `modules/command_executor.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_installer.py`, `modules/lazy_orchestrator_feedback.py`, `modules/orchestrator_config.py`, `modules/service_aliases.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/lazyops.py`, `modules/chain_loop.py`, `modules/command_executor.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_installer.py`, `modules/lazy_loop.py`, `modules/lazy_osinfer.py`, `modules/lazy_runner.py`, `modules/loop/worker_agentic.py`, `modules/loop/worker_execution.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `modules/verb_catalog.py`, `skills/mcp_tools/lazy_addon.py`, `tests/test_atomic_loop.py`, `tests/test_auto_pwn_success.py`, `tests/test_auto_registry.py`, `tests/test_chain_loop.py`, `tests/test_harness_mode.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_runner.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_fire_pending.py`, `tests/test_planner_initial_access.py`, `tests/test_playbook_chain.py`, `tests/test_poc_registry.py`, `tests/test_selection_lazyscript.py`, `tests/test_selection_module.py`, `tests/test_selection_technique.py`, `tests/test_selection_wiring.py`
- `auto_verb_target` (function) `modules/auto_registry.py:55` `def auto_verb_target(command)` -- Return the target an ``auto <verb> <target>`` line carries, else ''.
- `verb_enabled` (function) `modules/auto_registry.py:340` `def verb_enabled(name)` -- Return whether one auto verb may be proposed or executed.
- `binary_available` (function) `modules/auto_registry.py:458` `def binary_available(name)` -- Return True when a command token can actually execute here.
- `missing_binary` (function) `modules/auto_registry.py:474` `def missing_binary(command)` -- Return the first binary a shell command needs but PATH lacks.
- `verb_gap` (function) `modules/auto_registry.py:486` `def verb_gap(verb)` -- Return a human reason when an automation verb cannot run, else ''.
- `verb_available` (function) `modules/auto_registry.py:498` `def verb_available(verb)` -- Return True when every binary an automation verb needs is installed.
- `service_tokens` (function) `modules/auto_registry.py:503` `def service_tokens(service_text)` -- Normalize a service asset value into matchable tokens.
- `iter_addon_triggers` (function) `modules/auto_registry.py:545` `def iter_addon_triggers()` -- Scan enabled lazyaddons for (name, trigger tokens) pairs.
- `iter_tool_triggers` (function) `modules/auto_registry.py:581` `def iter_tool_triggers()` -- Scan active pwntomate tools for (toolname, trigger tokens) pairs.
- `addon_hits_for` (function) `modules/auto_registry.py:604` `def addon_hits_for(service_text, limit)` -- Rank addon/tool names matching one service value.
- `propose_addon_intents` (function) `modules/auto_registry.py:630` `def propose_addon_intents(service_texts, target, limit)` -- Propose addon intents for discovered services.
- `is_routable_command` (function) `modules/auto_registry.py:674` `def is_routable_command(line)` -- Return True when the loop executor must route via the shell.
- `verbs` (function) `modules/auto_registry.py:692` `def verbs()` -- Return every canonical automation verb name.
- `is_shell_verb` (function) `modules/auto_registry.py:697` `def is_shell_verb(token)` -- Return True when ``token`` names a loop-routable shell verb.
- `cover_all_enabled` (function) `modules/auto_registry.py:721` `def cover_all_enabled()` -- Return whether exploitation should exercise every vector, not just one.
- `build_command` (function) `modules/auto_registry.py:737` `def build_command(verb, target)` -- Build the shell command line for ``verb`` bound to ``target``.
- `verbs_for` (function) `modules/auto_registry.py:750` `def verbs_for(text)` -- Return enabled verbs whose keywords appear in the text.
- `propose_intents` (function) `modules/auto_registry.py:756` `def propose_intents(goal, target, finding_texts)` -- Propose ``auto <verb>`` intent summaries for planner candidates.
- `steps_for` (function) `modules/auto_registry.py:877` `def steps_for(text, target)` -- Translate an intent summary into shell command lines, or None.
- `_TeeCapture.__init__` (method) `modules/auto_registry.py:1056` `def __init__(self, observer)`
- `_TeeCapture.write` (method) `modules/auto_registry.py:1061` `def write(self, data)` -- Capture text and stream the chunk to the observer once.
- `execute_shell_verb` (function) `modules/auto_registry.py:1074` `def execute_shell_verb(shell, command, timeout_sec, on_output)` -- Run a LazyOwn shell verb capturing stdout, with a hard timeout.
- `track_process` (function) `modules/auto_registry.py:1184` `def track_process(process)` -- Register a live child process for global cancellation.
- `untrack_process` (function) `modules/auto_registry.py:1189` `def untrack_process(process)` -- Drop a finished child process from the cancellation registry.
- `cancel_running_commands` (function) `modules/auto_registry.py:1194` `def cancel_running_commands()` -- Kill every live streaming process group (operator Ctrl+C).
- `execute_streaming` (function) `modules/auto_registry.py:1217` `def execute_streaming(command, on_output, timeout_sec)` -- Run a bash command streaming lines while capturing the output.

## modules/autonomous_exploit_engine.py
Depends on: `core/defaults.py`, `core/safe_exec.py`, `modules/atomic_exploit_bridge.py`, `modules/auto_pivot.py`, `modules/ctf_capture.py`, `modules/db.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/pwn.py`, `cli/commands/session_ops.py`, `modules/ai_exploit_chain.py`, `modules/mediation/engine_mediator.py`, `skills/mcp_tools/auto_pwn.py`, `skills/mcp_tools/exploit_chain.py`, `skills/mcp_tools/stealth.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_auto_pwn_coverage.py`, `tests/test_auto_pwn_success.py`, `tests/test_emulation_runner.py`, `tests/test_engine_mediator.py`, `tests/test_phase1_data_gaps.py`
- `AutonomousExploitEngine.__init__` (method) `modules/autonomous_exploit_engine.py:121` `def __init__(self)`
- `AutonomousExploitEngine.get_instance` (method) `modules/autonomous_exploit_engine.py:142` `def get_instance(cls)`
- `AutonomousExploitEngine.hunt` (method) `modules/autonomous_exploit_engine.py:153` `def hunt(self, target, max_exploits, profile, stop_on_first_shell)` -- Execute a full autonomous exploitation chain against a target.
- `AutonomousExploitEngine.retry_with_credentials` (method) `modules/autonomous_exploit_engine.py:199` `def retry_with_credentials(self, target, credentials)` -- Re-execute exploit chain using captured credentials.
- `AutonomousExploitEngine.profile` (method) `modules/autonomous_exploit_engine.py:351` `def profile(self, target)` -- Build a TargetProfile from existing recon data.
- `AutonomousExploitEngine.rank_exploits` (method) `modules/autonomous_exploit_engine.py:412` `def rank_exploits(self, profile)` -- Rank exploit candidates by confidence for a given profile.
- `AutonomousExploitEngine.execute_candidate` (method) `modules/autonomous_exploit_engine.py:446` `def execute_candidate(self, candidate, profile)` -- Execute a single exploit candidate and return the result.
- `AutonomousExploitEngine.scan_vulnerabilities` (method) `modules/autonomous_exploit_engine.py:1822` `def scan_vulnerabilities(self, profile)` -- Scan for vulnerabilities using NSE output and heuristic version matching.
- `AutonomousExploitEngine.chain_privesc` (method) `modules/autonomous_exploit_engine.py:2137` `def chain_privesc(self, profile, session_id)` -- Run privilege escalation checks and attempt escalation techniques.
- `AutonomousExploitEngine.trigger_pivot` (method) `modules/autonomous_exploit_engine.py:2567` `def trigger_pivot(self, profile, session_id)` -- Discover internal interfaces and trigger auto-pivoting through a compromised host.
- `AutonomousExploitEngine.enable_stealth` (method) `modules/autonomous_exploit_engine.py:2693` `def enable_stealth(self, stealth_level)` -- Configure the engine's stealth level for evasion.
- `AutonomousExploitEngine.full_auto_pwn` (method) `modules/autonomous_exploit_engine.py:2757` `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth, cover_all)` -- Execute the full autonomous exploit chain against a target.

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
- `bootRun` (function) `modules/backdoor/backdoor.c:22` `int bootRun()`
- `str_cut` (function) `modules/backdoor/backdoor.c:53` `char *
str_cut(char str[], int slice_from, int slice_to)`
- `Shell` (function) `modules/backdoor/backdoor.c:88` `void Shell()`
- `WinMain` (function) `modules/backdoor/backdoor.c:129` `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`

## modules/backdoor/keylogger.h
Imported by: `modules/backdoor/backdoor.c`
- `logg` (function) `modules/backdoor/keylogger.h:1` `DWORD WINAPI logg(LPVOID lpParam)`

## modules/backdoor/server.c
Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `contrib/legacy/lazygalazy.py`, `contrib/legacy/lazyhttpreverseshell.py`, `lazyc2.py`, `modules/browser_sync.py`, `modules/lazy_oob.py`, `modules/lazy_proxy.py`, `modules/lazyown_bprfuzzer.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_bprfuzzer_identity.py`, `tests/test_lazy_proxy.py`, `utils.py`
- `main` (function) `modules/backdoor/server.c:10` `int main()`

## modules/beacon_config_builder.py
Depends on: `core/config.py`, `core/logging.py`, `modules/c2_profile_engine.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`
Imported by: `modules/bof_delivery.py`, `modules/c2_builder.py`, `tests/test_beacon_config_builder.py`, `tests/test_bof_delivery.py`
- `BeaconConfig.to_gen_beacon_args` (method) `modules/beacon_config_builder.py:119` `def to_gen_beacon_args(self)` -- Produce CLI arguments for gen_beacon.sh.
- `BeaconConfig.to_go_implant_vars` (method) `modules/beacon_config_builder.py:139` `def to_go_implant_vars(self)` -- Produce template variables for the Go implant builder.
- `BeaconConfig.to_config_json` (method) `modules/beacon_config_builder.py:162` `def to_config_json(self)` -- Produce the config.json that beacons fetch on startup.
- `BeaconConfig.to_dict` (method) `modules/beacon_config_builder.py:187` `def to_dict(self)` -- Full serialization of beacon config.
- `BeaconConfigBuilder.__init__` (method) `modules/beacon_config_builder.py:247` `def __init__(self, payload)`
- `BeaconConfigBuilder.build` (method) `modules/beacon_config_builder.py:250` `def build(self, name)` -- Build a complete BeaconConfig.
- `BeaconConfigBuilder.from_payload` (method) `modules/beacon_config_builder.py:405` `def from_payload(cls, payload)` -- Build a BeaconConfigBuilder from a payload dictionary.
- `BeaconConfigBuilder.from_payload_file` (method) `modules/beacon_config_builder.py:410` `def from_payload_file(cls, path)` -- Build a BeaconConfigBuilder by loading payload.json from disk.
- `sanitize_client_id` (function) `modules/beacon_config_builder.py:425` `def sanitize_client_id(client_id)` -- Return a strict beacon client id safe for URLs and file paths.
- `generate_bof_execution_command` (function) `modules/beacon_config_builder.py:449` `def generate_bof_execution_command(bof_name, c2_url, args, bofs_dir)` -- Generate a ``bof:<url>[ <args>]`` command that a beacon executes.

## modules/beacon_history.py
Depends on: `core/logging.py`, `modules/security_sanitizers.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/api_v1.py`, `modules/beacon_loop.py`, `modules/bof_delivery.py`, `modules/lazy_handoff.py`, `tests/test_api_v1.py`, `tests/test_beacon_history.py`, `tests/test_bof_delivery.py`, `tests/test_security_lazyc2.py`
- `BeaconHistoryConfig.sessions_dir` (method) `modules/beacon_history.py:41` `def sessions_dir(self)` -- Return the resolved sessions directory under the base dir.
- `BeaconHistoryConfig.records_path` (method) `modules/beacon_history.py:45` `def records_path(self, client_id)` -- Resolve the history file path for a sanitised beacon client id.
- `append_record` (function) `modules/beacon_history.py:72` `def append_record(record, config)` -- Append one beacon result record to the persistent JSONL history.
- `read_records` (function) `modules/beacon_history.py:106` `def read_records(client_id, config)` -- Read the ordered JSONL history for a beacon client id (oldest first).
- `records_path` (function) `modules/beacon_history.py:135` `def records_path(client_id, config)` -- Resolve the history file path for a beacon client id.

## modules/beacon_kinds.py
Depends on: `core/logging.py`, `modules/apt_playbooks.py`, `modules/bof_registry.py`
Imported by: `lazyc2.py`, `tests/test_beacon_menu.py`
- `detect_beacon_type` (function) `modules/beacon_kinds.py:50` `def detect_beacon_type(safe_id, platform, bsb_clients, sessions_dir)` -- Classify one connected implant by its runtime family.
- `beacon_capabilities` (function) `modules/beacon_kinds.py:83` `def beacon_capabilities(beacon_type)` -- Return the capability flags for one beacon family.
- `beacon_commands` (function) `modules/beacon_kinds.py:121` `def beacon_commands(beacon_type)` -- Return the capability command catalog for one beacon family.
- `beacon_menu_bofs` (function) `modules/beacon_kinds.py:133` `def beacon_menu_bofs(capabilities, sessions_dir)` -- List catalog BOFs compatible with one beacon platform.
- `beacon_menu_playbooks` (function) `modules/beacon_kinds.py:171` `def beacon_menu_playbooks(repo_root)` -- List the APT adversarial playbooks available for chains.

## modules/beacon_loop.py
Depends on: `modules/beacon_history.py`, `modules/killchain.py`, `modules/llm_factory.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/lazy_handoff.py`, `tests/test_beacon_menu.py`, `tests/test_lazy_handoff.py`
- `queue_beacon_command` (function) `modules/beacon_loop.py:211` `def queue_beacon_command(client_id, command, sessions_dir)` -- Append one command to the beacon C2 queue file.
- `summarize_history` (function) `modules/beacon_loop.py:239` `def summarize_history(records, max_chars)` -- Render a bounded text summary of beacon history for the planner.
- `playbook_ladder` (function) `modules/beacon_loop.py:343` `def playbook_ladder(goal, platform)` -- Return the OS-aware progressive playbook phases for one goal.
- `heuristic_plan` (function) `modules/beacon_loop.py:378` `def heuristic_plan(goal, platform, records, sessions_dir)` -- Build the next command batch without an LLM.
- `llm_plan` (function) `modules/beacon_loop.py:429` `def llm_plan(goal, platform, history, model, max_commands)` -- Ask the LLM planner for the next command batch.
- `run_beacon_loop` (function) `modules/beacon_loop.py:494` `def run_beacon_loop(config, log, sleep, sessions_dir, deadline)` -- Run the autonomous beacon loop until rounds or timeout expire.
- `write_report` (function) `modules/beacon_loop.py:587` `def write_report(report, sessions_dir)` -- Persist the loop report as a timestamped JSON artifact.

## modules/beacon_recon.py
Depends on: `core/logging.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `lazyc2.py`, `tests/test_beacon_recon_sink.py`
- `parse_discovered_ips` (function) `modules/beacon_recon.py:50` `def parse_discovered_ips(raw)` -- Extract clean IP strings from a beacon discovery payload.
- `parse_beacon_portscan` (function) `modules/beacon_recon.py:94` `def parse_beacon_portscan(raw, default_host)` -- Normalise any known port-scan payload into ``(host, port)`` pairs.
- `ingest_beacon_recon` (function) `modules/beacon_recon.py:169` `def ingest_beacon_recon(primary_ip, discovered_ips, portscan, hostname, user, client_id, sessions_dir)` -- Fold beacon discovery and port-scan payloads into the state layer.

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

## modules/bof_admin.py
Imported by: `cli/orchestrator_assets_tabs.py`, `modules/bof_registry.py`, `tests/test_bof_admin.py`, `tests/test_bof_repo_contract.py`
- `slugify` (function) `modules/bof_admin.py:72` `def slugify(value)` -- Return a safe BOF filename stem.
- `bof_path` (function) `modules/bof_admin.py:85` `def bof_path(filename, directory)` -- Resolve one BOF file inside the bofs root.
- `load_bof` (function) `modules/bof_admin.py:110` `def load_bof(path)` -- Read one BOF YAML mapping.
- `validate_bof` (function) `modules/bof_admin.py:132` `def validate_bof(data)` -- Validate one BOF mapping against the delivery contract.
- `scan_bofs` (function) `modules/bof_admin.py:179` `def scan_bofs(directory, sessions_dir)` -- Scan the bofs directory, returning admin rows for every file.
- `bof_template` (function) `modules/bof_admin.py:224` `def bof_template(name, description, client)` -- Return a minimal BOF mapping ready for ``yaml.safe_dump``.
- `create_bof` (function) `modules/bof_admin.py:257` `def create_bof(filename)` -- Create one BOF configuration file.
- `update_bof` (function) `modules/bof_admin.py:300` `def update_bof(path, data, directory)` -- Validate and atomically rewrite one BOF configuration.
- `save_bof_yaml` (function) `modules/bof_admin.py:332` `def save_bof_yaml(path, text, directory)` -- Validate raw YAML text and atomically write it to the bofs root.
- `preview_bof` (function) `modules/bof_admin.py:370` `def preview_bof(path, limit)` -- Return a bounded YAML preview for one BOF file.
- `delete_bof` (function) `modules/bof_admin.py:391` `def delete_bof(path, directory)` -- Delete one BOF configuration file after validation.

## modules/bof_delivery.py
Depends on: `core/config.py`, `core/logging.py`, `core/safe_exec.py`, `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/bof_registry.py`
Imported by: `cli/commands/bof_registry.py`, `cli/commands/command_and_control_migrated.py`, `cli/orchestrator_assets_tabs.py`, `lazyc2.py`, `modules/atomic_cli.py`, `modules/lazy_handoff.py`, `tests/test_atomic_headless.py`, `tests/test_atomic_loop.py`, `tests/test_bof_delivery.py`, `tests/test_bof_repo_contract.py`, `tests/test_bsb_fileless_compat.py`
- `load_client_addon` (function) `modules/bof_delivery.py:184` `def load_client_addon(client, config)` -- Resolve one beacon client lazyaddon manifest.
- `staging_dir` (function) `modules/bof_delivery.py:225` `def staging_dir(config)` -- Return (and create) the BOF staging directory.
- `stage_bof` (function) `modules/bof_delivery.py:240` `def stage_bof(name, config)` -- Stage one catalog BOF for delivery through its client.
- `beacon_runtime_config` (function) `modules/bof_delivery.py:259` `def beacon_runtime_config(client, client_id, config, payload)` -- Build the C2-aligned beacon runtime configuration.
- `write_client_config` (function) `modules/bof_delivery.py:336` `def write_client_config(client, client_id, config, payload)` -- Write the generated runtime config into the addon checkout and staging dir.
- `stage_client` (function) `modules/bof_delivery.py:378` `def stage_client(client, config, payload)` -- Compile and stage a beacon client through its lazyaddon tool.
- `key_missing_from_error` (function) `modules/bof_delivery.py:894` `def key_missing_from_error(exc)` -- Return True when the error text points at a missing AES key.
- `delivery_command` (function) `modules/bof_delivery.py:908` `def delivery_command(bof_name, c2_url, args, bofs_dir)` -- Build the ``bof:`` delivery command for one BOF.
- `queue_to_beacon` (function) `modules/bof_delivery.py:956` `def queue_to_beacon(client_id, command, config, payload)` -- Queue one command for a connected beacon through the C2 API.
- `recent_beacons` (function) `modules/bof_delivery.py:1019` `def recent_beacons(config, payload)` -- Return the beacons currently seen by the C2.
- `beacon_for_target` (function) `modules/bof_delivery.py:1085` `def beacon_for_target(target, config, payload)` -- Return the client id of a beacon that reported from ``target``.
- `wait_for_beacon` (function) `modules/bof_delivery.py:1123` `def wait_for_beacon(client_id, since, timeout, config, payload, command)` -- Wait until a beacon answers, then return its latest record.
- `c2_reachable` (function) `modules/bof_delivery.py:1205` `def c2_reachable(config, payload)` -- Return True when the C2 answers an authenticated API query.
- `run_bof` (function) `modules/bof_delivery.py:1240` `def run_bof(bof_name, client_id, args)` -- Queue one BOF execution on a live beacon and optionally await output.
- `run_bof_train` (function) `modules/bof_delivery.py:1279` `def run_bof_train(client_id, names, args)` -- Run a sequence of BOFs over one beacon, waiting for each in turn.
- `deploy_client` (function) `modules/bof_delivery.py:1345` `def deploy_client(client, target)` -- Deliver a staged beacon client onto a target and await check-in.
- `_DockerSession.__init__` (method) `modules/bof_delivery.py:1482` `def __init__(self, container)` -- Bind the adapter to one container name.
- `_DockerSession.alive` (method) `modules/bof_delivery.py:1486` `def alive(self, timeout)` -- Return True while the container answers ``echo``.
- `_DockerSession.run` (method) `modules/bof_delivery.py:1506` `def run(self, command, timeout)` -- Execute one shell line inside the container.
- `config_sessions_dir` (function) `modules/bof_delivery.py:1657` `def config_sessions_dir()` -- Return the sessions directory of the default delivery config.
- `bof_results` (function) `modules/bof_delivery.py:1678` `def bof_results(client_id, limit, config)` -- Read the last beacon history records for one client.


Next: [API_p11.md](API_p11.md)
