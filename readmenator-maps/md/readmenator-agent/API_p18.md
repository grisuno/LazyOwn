# API (page 18 of 27)
Previous: [API_p17.md](API_p17.md)

## modules/playbook_engine.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/emulation_runner.py`, `modules/llm_client.py`, `modules/obs_parser.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`, `cli/commands/mcp_bridge.py`, `modules/operation.py`, `modules/planner.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`, `skills/mcp_tools/playbook_generate.py`, `skills/mcp_tools/playbook_run.py`, `tests/test_core_modules.py`, `tests/test_selection_technique.py`
- `PlaybookStep.to_dict` (method) `modules/playbook_engine.py:113` `def to_dict(self)`
- `PlaybookStep.from_dict` (method) `modules/playbook_engine.py:128` `def from_dict(cls, d)`
- `Playbook.to_dict` (method) `modules/playbook_engine.py:141` `def to_dict(self)`
- `Playbook.from_dict` (method) `modules/playbook_engine.py:152` `def from_dict(cls, d)`
- `_StixLoader.__init__` (method) `modules/playbook_engine.py:188` `def __init__(self, json_path)`
- `_StixLoader.available` (method) `modules/playbook_engine.py:192` `def available(self)`
- `_StixLoader.store` (method) `modules/playbook_engine.py:195` `def store(self)`
- `_StixLoader.techniques_for_tactics` (method) `modules/playbook_engine.py:210` `def techniques_for_tactics(self, tactic_shortnames, platform)` -- Return ATT&CK techniques matching the given tactic shortnames.
- `_AtomicIndex.__init__` (method) `modules/playbook_engine.py:260` `def __init__(self, atomics_path)`
- `_AtomicIndex.available` (method) `modules/playbook_engine.py:264` `def available(self)`
- `_AtomicIndex.build` (method) `modules/playbook_engine.py:267` `def build(self)`
- `_AtomicIndex.tests_for_technique` (method) `modules/playbook_engine.py:300` `def tests_for_technique(self, technique_id, platform)`
- `_TechniqueSelector.select` (method) `modules/playbook_engine.py:317` `def select(self, candidates, world_context, target, phase, api_key, top_n)`
- `PlaybookEngine.__init__` (method) `modules/playbook_engine.py:387` `def __init__(self, world_model, obs_parser, api_key, top_n)`
- `PlaybookEngine.derive` (method) `modules/playbook_engine.py:427` `def derive(self, target, phase, platform, apt_name)` -- Generate a Playbook for *target* at the given *phase*.
- `PlaybookEngine.execute` (method) `modules/playbook_engine.py:529` `def execute(self, playbook, executor, dry_run)` -- Execute a Playbook step by step.
- `PlaybookEngine.save` (method) `modules/playbook_engine.py:599` `def save(self, playbook, path)` -- Persist playbook to YAML (compatible with existing playbooks/ format).
- `PlaybookEngine.load` (method) `modules/playbook_engine.py:611` `def load(self, path)` -- Load a playbook from YAML.
- `PlaybookEngine.result_summary` (method) `modules/playbook_engine.py:640` `def result_summary(self, result)` -- Return a human-readable / LLM-readable summary of a PlaybookResult.
- `get_engine` (function) `modules/playbook_engine.py:669` `def get_engine(api_key)` -- Return (or create) the module-level singleton PlaybookEngine.
- `phase_techniques` (function) `modules/playbook_engine.py:696` `def phase_techniques(phase, platform, top_n)` -- Return candidate ATT&CK techniques for one canonical loop phase.

## modules/playbook_executor.py
Depends on: `modules/pipeline_engine.py`
- `PlaybookRunResult.to_dict` (method) `modules/playbook_executor.py:74` `def to_dict(self)`
- `ITTPMapper.resolve` (method) `modules/playbook_executor.py:97` `def resolve(self, technique_id, atomic_test, platform)` -- Return a LazyOwn shell command string or None if unmapped.
- `DefaultTTPMapper.register` (method) `modules/playbook_executor.py:180` `def register(cls, technique_id, platform, command)` -- Add a new technique-to-command mapping.
- `DefaultTTPMapper.resolve` (method) `modules/playbook_executor.py:185` `def resolve(self, technique_id, atomic_test, platform)`
- `PlaybookLoader.__init__` (method) `modules/playbook_executor.py:208` `def __init__(self, playbooks_dir)`
- `PlaybookLoader.list` (method) `modules/playbook_executor.py:211` `def list(self)` -- Return every discoverable playbook name.
- `PlaybookLoader.load` (method) `modules/playbook_executor.py:224` `def load(self, name)` -- Load and validate a playbook by name.
- `PlaybookEngine.__init__` (method) `modules/playbook_executor.py:339` `def __init__(self, loader, mapper, pipelines_dir)`
- `PlaybookEngine.loader` (method) `modules/playbook_executor.py:350` `def loader(self)`
- `PlaybookEngine.analyze` (method) `modules/playbook_executor.py:353` `def analyze(self, name, platform)` -- Analyze a playbook: count techniques, automated vs manual, coverage.
- `PlaybookEngine.generate_pipeline` (method) `modules/playbook_executor.py:378` `def generate_pipeline(self, name, platform)` -- Generate a pipeline YAML file from a playbook.
- `PlaybookEngine.run` (method) `modules/playbook_executor.py:390` `def run(self, name, platform, target, onecmd)` -- Generate and execute a pipeline from a playbook.
- `playbook_list` (function) `modules/playbook_executor.py:416` `def playbook_list()` -- Return a JSON array of available playbooks.
- `playbook_analyze` (function) `modules/playbook_executor.py:422` `def playbook_analyze(name, platform)` -- Return a JSON summary of one playbook.
- `playbook_generate` (function) `modules/playbook_executor.py:429` `def playbook_generate(name, platform)` -- Generate a runnable pipeline from a playbook.
- `playbook_run` (function) `modules/playbook_executor.py:436` `def playbook_run(name, platform, target, onecmd)` -- Analyze, generate, and execute a playbook.

## modules/poc_registry.py
- `PocVerb.to_dict` (method) `modules/poc_registry.py:129` `def to_dict(self)` -- Return a JSON-serialisable summary for the orchestrator surfaces.
- `poc_verbs` (function) `modules/poc_registry.py:283` `def poc_verbs(catalog_path)` -- Return the catalogued PoC verbs (cached, fail-safe).
- `get_poc` (function) `modules/poc_registry.py:312` `def get_poc(name, catalog_path)` -- Return one PoC verb by name, or None when unknown/disabled-less.
- `interpreter_argv` (function) `modules/poc_registry.py:325` `def interpreter_argv(verb)` -- Return the ``argv`` prefix that launches the PoC script.
- `render_argv` (function) `modules/poc_registry.py:337` `def render_argv(verb, params, target, overrides)` -- Expand one PoC verb into a safe ``argv`` list.
- `missing_requirements` (function) `modules/poc_registry.py:392` `def missing_requirements(verb)` -- Return the PoC's required binaries that are absent on this host.
- `propose_intents` (function) `modules/poc_registry.py:409` `def propose_intents(service_texts, target, limit, catalog_path)` -- Propose ``lazy_poc run`` intent lines for matching service tokens.
- `verbs_summary` (function) `modules/poc_registry.py:449` `def verbs_summary(catalog_path)` -- Return every PoC verb as a dict for TUI and MCP surfaces.

## modules/polymorphic_engine.py
Imported by: `cli/commands/payload_arsenal.py`
- `PolymorphicEngine.__init__` (method) `modules/polymorphic_engine.py:159` `def __init__(self, config)`
- `PolymorphicEngine.mutate` (method) `modules/polymorphic_engine.py:163` `def mutate(self, shellcode, arch)` -- Apply all configured mutation passes to shellcode.
- `PolymorphicEngine.decode_xor` (method) `modules/polymorphic_engine.py:361` `def decode_xor(data)` -- Decode single-byte XOR encrypted shellcode.
- `PolymorphicEngine.decode_multi_xor` (method) `modules/polymorphic_engine.py:377` `def decode_multi_xor(data)` -- Decode multi-byte XOR encrypted shellcode.
- `PolymorphicEngine.generate_decoder_stub` (method) `modules/polymorphic_engine.py:397` `def generate_decoder_stub(self, arch)` -- Generate a self-decrypting stub shellcode template.
- `PolymorphicEngine.get_audit_summary` (method) `modules/polymorphic_engine.py:422` `def get_audit_summary(self)` -- Return a summary of all mutations applied.

## modules/privesc_predictor.py
Depends on: `core/console.py`, `modules/llm_factory.py`
Imported by: `cli/commands/crystal_ball.py`
- `parse_linpeas_output` (function) `modules/privesc_predictor.py:165` `def parse_linpeas_output(text)` -- Extract a structured SystemProfile from linpeas output text.
- `parse_winpeas_output` (function) `modules/privesc_predictor.py:218` `def parse_winpeas_output(text)` -- Extract a structured SystemProfile from winpeas output text.
- `match_known_cves` (function) `modules/privesc_predictor.py:249` `def match_known_cves(profile)` -- Match kernel version against the built-in CVE database.
- `suid_vectors` (function) `modules/privesc_predictor.py:287` `def suid_vectors(profile)` -- Generate privilege escalation vectors from SUID binaries.
- `capability_vectors` (function) `modules/privesc_predictor.py:361` `def capability_vectors(profile)` -- Generate privilege escalation vectors from Linux capabilities.
- `group_vectors` (function) `modules/privesc_predictor.py:463` `def group_vectors(profile)` -- Generate privilege escalation vectors from group memberships.
- `sudo_vectors` (function) `modules/privesc_predictor.py:501` `def sudo_vectors(profile)` -- Generate privilege escalation vectors from sudo rules.
- `cron_vectors` (function) `modules/privesc_predictor.py:578` `def cron_vectors(profile)` -- Generate vectors from writable cron jobs and PATH manipulation.
- `analyze_privesc` (function) `modules/privesc_predictor.py:742` `def analyze_privesc(filepath, text)` -- Main entry point — analyse a system for privilege escalation vectors.
- `format_crystal_ball_output` (function) `modules/privesc_predictor.py:827` `def format_crystal_ball_output(result)` -- Format the analysis result as a human-readable terminal report.
- `main` (function) `modules/privesc_predictor.py:908` `def main()` -- CLI entry point for crystal ball privesc analysis.

## modules/professional_report.py
Depends on: `modules/llm_factory.py`, `modules/world_model.py`
Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_gym_matrix_ctf.py`, `tests/test_infra_disposable.py`
- `RedTeamReportGenerator.__init__` (method) `modules/professional_report.py:173` `def __init__(self, include_credentials)`
- `RedTeamReportGenerator.collect_data` (method) `modules/professional_report.py:179` `def collect_data(self)` -- Collect all available engagement data from sessions directory.
- `RedTeamReportGenerator.classify_findings` (method) `modules/professional_report.py:219` `def classify_findings(self, data)` -- Classify collected data into structured findings.
- `RedTeamReportGenerator.generate` (method) `modules/professional_report.py:247` `def generate(self, output_dir, output_format, client_name, engagement_type, with_ai, ai_backend)` -- Generate the report in the specified format.
- `RedTeamReportGenerator.collect_command_history` (method) `modules/professional_report.py:912` `def collect_command_history(self, max_entries)` -- Collect operator command history for the engagement timeline.
- `RedTeamReportGenerator.collect_loot_summary` (method) `modules/professional_report.py:936` `def collect_loot_summary(self)` -- Summarize exfiltrated loot without embedding sensitive content.
- `RedTeamReportGenerator.generate_executive_summary` (method) `modules/professional_report.py:982` `def generate_executive_summary(self, data, with_ai, ai_backend)` -- Build the executive summary in business language.

## modules/progress_ledger.py
Imported by: `modules/lazy_loop.py`, `tests/test_progress_ledger.py`
- `StrikePolicy.clamped` (method) `modules/progress_ledger.py:56` `def clamped(self)` -- Return a copy with the strike cap forced into range.
- `RoundSignals.progress` (method) `modules/progress_ledger.py:82` `def progress(self)` -- Return True when any objective-evidence signal fired.
- `ProgressLedger.__init__` (method) `modules/progress_ledger.py:103` `def __init__(self, engagement_id, base_dir, policy)` -- Bind the ledger to one engagement.
- `ProgressLedger.file_path` (method) `modules/progress_ledger.py:128` `def file_path(self)` -- Return the persisted strike state path.
- `ProgressLedger.load` (method) `modules/progress_ledger.py:132` `def load(self)` -- Load persisted state, keeping any file intact on parse failure.
- `ProgressLedger.save` (method) `modules/progress_ledger.py:152` `def save(self)` -- Persist the strike state with owner-only permissions.
- `ProgressLedger.strikes` (method) `modules/progress_ledger.py:167` `def strikes(self)` -- Return the current consecutive no-progress strike count.
- `ProgressLedger.log` (method) `modules/progress_ledger.py:172` `def log(self)` -- Return the recent strike/progress log rows.
- `ProgressLedger.signals_from_brief` (method) `modules/progress_ledger.py:176` `def signals_from_brief(self, brief)` -- Diff one graph/orchestrator brief against the stored previous one.
- `ProgressLedger.observe` (method) `modules/progress_ledger.py:208` `def observe(self, signals, note)` -- Record one round of signals and update the strike counter.
- `ProgressLedger.brief_for_discards` (method) `modules/progress_ledger.py:250` `def brief_for_discards(self)` -- Return durable rows for the finding-ledger discard recorder.

## modules/r.sh
Imported by: `static/js/quill-2.0.3.js::c`, `static/js/quill-2.0.3.js::h`, `static/js/quill-2.0.3.js::i`, `static/js/quill-2.0.3.js::o`, `static/js/quill-2.0.3.js::s`, `static/js/quill-2.0.3.js::u`, `static/js/xterm.js::a`, `static/js/xterm.js::n`, `static/js/xterm.js::o`
- `download_kernel_sources` (function) `modules/r.sh:10` -- Función para descargar y extraer las fuentes del kernel

## modules/reaction_bridge.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/lazy_loop.py`, `modules/loop/worker_memory.py`, `tests/test_reaction_bridge.py`
- `ReactionPick.__init__` (method) `modules/reaction_bridge.py:69` `def __init__(self, command, reason, priority, mitre)`
- `save_decisions` (function) `modules/reaction_bridge.py:80` `def save_decisions(task_id, decisions)` -- Park picks into the per-task buffer; returns the saved count.
- `load_reaction_triggers` (function) `modules/reaction_bridge.py:108` `def load_reaction_triggers(task_id, consumer)` -- Drain the buffer into planner trigger dicts (one-shot, one per round).
- `find_credentials` (function) `modules/reaction_bridge.py:159` `def find_credentials(output)` -- Extract user:pass pairs and hashes; placeholder values are dropped.

## modules/reactive_engine.py
Depends on: `core/config.py`, `core/logging.py`, `modules/session_rag.py`
Imported by: `cli/apt_chain_support.py`, `modules/mediation/engine_mediator.py`, `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/mcp_tools/reactive_suggest.py`, `skills/toposwarm_autonomous.py`, `tests/test_core_modules.py`, `tests/test_engine_mediator.py`, `tests/test_reactive_engine_semantic.py`, `tests/test_reactive_lateral_data.py`
- `AbstractSignalMatcher.match` (method) `modules/reactive_engine.py:99` `def match(self, output, context)`
- `AVBlockedMatcher.match` (method) `modules/reactive_engine.py:128` `def match(self, output, context)`
- `CredentialFoundMatcher.match` (method) `modules/reactive_engine.py:159` `def match(self, output, context)`
- `PrivescHintMatcher.match` (method) `modules/reactive_engine.py:192` `def match(self, output, context)`
- `NewHostMatcher.match` (method) `modules/reactive_engine.py:214` `def match(self, output, context)`
- `ServiceVersionMatcher.match` (method) `modules/reactive_engine.py:247` `def match(self, output, context)`
- `ShellErrorMatcher.match` (method) `modules/reactive_engine.py:276` `def match(self, output, context)`
- `LateralOpportunityMatcher.match` (method) `modules/reactive_engine.py:307` `def match(self, output, context)`
- `DataOfInterestMatcher.match` (method) `modules/reactive_engine.py:349` `def match(self, output, context)`
- `ParquetAdvisor.__init__` (method) `modules/reactive_engine.py:395` `def __init__(self, root)`
- `ParquetAdvisor.gtfobins_for` (method) `modules/reactive_engine.py:421` `def gtfobins_for(self, binary)`
- `ParquetAdvisor.lolbas_for` (method) `modules/reactive_engine.py:434` `def lolbas_for(self, binary)` -- Returns [(function_name, att&ck_technique), ...].
- `ParquetAdvisor.technique_commands_for` (method) `modules/reactive_engine.py:448` `def technique_commands_for(self, platform, keyword)` -- Return atomic test commands for platform matching keyword.
- `EvasionAdvisor.suggest` (method) `modules/reactive_engine.py:504` `def suggest(self, signals, platform)`
- `PrivescAdvisor.suggest` (method) `modules/reactive_engine.py:565` `def suggest(self, signals, platform, parquet)`
- `SemanticContextAdvisor.__init__` (method) `modules/reactive_engine.py:644` `def __init__(self, rag, config_loader, min_score, query_limit)` -- Initialise the advisor.
- `SemanticContextAdvisor.suggest` (method) `modules/reactive_engine.py:734` `def suggest(self, output, command, platform, context)` -- Return semantic next-step hints derived from past sessions.
- `ReactiveEngine.__init__` (method) `modules/reactive_engine.py:810` `def __init__(self, matchers, evasion, privesc, parquet, semantic)`
- `ReactiveEngine.analyse` (method) `modules/reactive_engine.py:835` `def analyse(self, output, command, platform, context)` -- Parse *output* and return prioritised ReactiveDecisions.
- `ReactiveEngine.top_decision` (method) `modules/reactive_engine.py:958` `def top_decision(self, output, command, platform, context)` -- Return only the single highest-priority decision, or None.
- `get_engine` (function) `modules/reactive_engine.py:977` `def get_engine()`

## modules/recommender.py
Depends on: `modules/ai_fallback.py`, `modules/session_state.py`
Imported by: `skills/lazyown_mcp.py`, `skills/mcp_tools/recommend_next.py`
- `recommend` (function) `modules/recommender.py:143` `def recommend(state, api_key)` -- Return ranked recommendations without writing to disk.
- `recommend_and_save` (function) `modules/recommender.py:163` `def recommend_and_save(api_key)` -- Build state → call Groq → write JSON → return recommendations.

## modules/redteam_gym.py
Depends on: `cli/engagement_hooks.py`, `core/config.py`, `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/cli_auth.py`, `modules/gym_registry.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/redteam_gym.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `modules/exploitgym_gym.py`, `tests/test_gym_cli.py`, `tests/test_gym_registry.py`, `tests/test_infra_disposable.py`, `tests/test_lazy_orchestrator.py`
- `reload_challenge_definitions` (function) `modules/redteam_gym.py:300` `def reload_challenge_definitions(directory)` -- Reload YAML definitions, falling back to the embedded catalogue.
- `definition_rows` (function) `modules/redteam_gym.py:394` `def definition_rows()` -- Return one row per gym YAML file, including invalid files.
- `create_gym` (function) `modules/redteam_gym.py:399` `def create_gym(gym_id)` -- Create a gym definition YAML and reload the catalogue.
- `save_gym_yaml` (function) `modules/redteam_gym.py:436` `def save_gym_yaml(gym_id, text)` -- Validate and persist raw YAML for one gym definition.
- `delete_gym` (function) `modules/redteam_gym.py:446` `def delete_gym(gym_id)` -- Delete one gym definition unless it has active runs.
- `list_challenges` (function) `modules/redteam_gym.py:454` `def list_challenges()` -- Return all defined gym challenges with metadata.
- `start_challenge` (function) `modules/redteam_gym.py:495` `def start_challenge(challenge_id, target, spin_lab, notify)` -- Begin a gym challenge and persist the run in the world model.
- `submit_challenge` (function) `modules/redteam_gym.py:648` `def submit_challenge(techniques_used, success, run_id)` -- Submit a completed challenge for scoring.
- `stop_challenges` (function) `modules/redteam_gym.py:756` `def stop_challenges(selector)` -- Stop one gym by id/name/run id, or every gym when selector is empty.
- `engagement_context` (function) `modules/redteam_gym.py:838` `def engagement_context(target)` -- Return in-scope phase, compromised hosts and live shells.
- `get_active_challenges` (function) `modules/redteam_gym.py:898` `def get_active_challenges()` -- Return every active gym run across operators.
- `show_leaderboard` (function) `modules/redteam_gym.py:1057` `def show_leaderboard(top_n)` -- Return the top N players from the leaderboard.
- `get_active_challenge` (function) `modules/redteam_gym.py:1084` `def get_active_challenge(run_id)` -- Return one active challenge, preferring the current operator.
- `record_external_attempt` (function) `modules/redteam_gym.py:1115` `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` -- Record a scored attempt for a challenge not defined in the catalog.
- `main` (function) `modules/redteam_gym.py:1169` `def main()` -- CLI entry point — show gym leaderboard from command line.

## modules/reflective_dll.py
- `PEParser.__init__` (method) `modules/reflective_dll.py:151` `def __init__(self, pe_data)`
- `PEParser.parse_file_header` (method) `modules/reflective_dll.py:166` `def parse_file_header(self)` -- Extract the COFF file header.
- `PEParser.parse_sections` (method) `modules/reflective_dll.py:208` `def parse_sections(self, num_sections)` -- Parse all section headers from the PE.
- `PEParser.parse_data_directories` (method) `modules/reflective_dll.py:243` `def parse_data_directories(self, num_entries)` -- Parse the PE data directory entries.
- `PEParser.rva_to_offset` (method) `modules/reflective_dll.py:265` `def rva_to_offset(self, rva, sections)` -- Convert a relative virtual address to a file offset.
- `PEParser.parse_imports` (method) `modules/reflective_dll.py:280` `def parse_imports(self, import_dir, sections)` -- Parse the import directory to enumerate imported DLLs and functions.
- `PEParser.parse_relocations` (method) `modules/reflective_dll.py:326` `def parse_relocations(self, reloc_dir, sections)` -- Parse base relocation entries.
- `PEParser.parse_exports` (method) `modules/reflective_dll.py:374` `def parse_exports(self, export_dir, sections)` -- Parse the export directory.
- `PEParser.is_64bit` (method) `modules/reflective_dll.py:456` `def is_64bit(self)`
- `PEParser.raw_data` (method) `modules/reflective_dll.py:460` `def raw_data(self)`
- `ReflectiveLoader.__init__` (method) `modules/reflective_dll.py:492` `def __init__(self, pe_data, config)`
- `ReflectiveLoader.sha256` (method) `modules/reflective_dll.py:505` `def sha256(self)` -- SHA-256 hash of the raw PE bytes.
- `ReflectiveLoader.architecture` (method) `modules/reflective_dll.py:510` `def architecture(self)` -- CPU architecture string ('x64' or 'x86').
- `ReflectiveLoader.required_imports` (method) `modules/reflective_dll.py:515` `def required_imports(self)` -- DLL names needed for import resolution.
- `ReflectiveLoader.plan_injection` (method) `modules/reflective_dll.py:526` `def plan_injection(self)` -- Generate an injection plan based on the configured technique.
- `ReflectiveLoader.generate_c_stub` (method) `modules/reflective_dll.py:588` `def generate_c_stub(self)` -- Generate a C stub that implements reflective loading.
- `ReflectiveLoader.generate_powershell_stub` (method) `modules/reflective_dll.py:666` `def generate_powershell_stub(self)` -- Generate PowerShell reflective loader script.
- `ReflectiveLoader.summarize` (method) `modules/reflective_dll.py:685` `def summarize(self)` -- Human-readable summary of the parsed PE for operator review.

## modules/resource_script.py
Depends on: `core/safe_exec.py`
Imported by: `cli/commands/resource_scripting.py`, `tests/test_resource_script.py`, `tests/test_security_hardening_v3.py`
- `ScriptContext.__init__` (method) `modules/resource_script.py:89` `def __init__(self, shell_params, on_command, on_print)`
- `ScriptContext.print` (method) `modules/resource_script.py:138` `def print(self, msg)`
- `ScriptContext.run_command` (method) `modules/resource_script.py:147` `def run_command(self, cmd)`
- `ScriptContext.eval_condition` (method) `modules/resource_script.py:191` `def eval_condition(self, raw_condition)` -- Evaluate an ``if``/``while`` condition expression.
- `ResourceScriptEngine.__init__` (method) `modules/resource_script.py:276` `def __init__(self, context)`
- `ResourceScriptEngine.execute` (method) `modules/resource_script.py:279` `def execute(self, script_path)` -- Load and run a script file.
- `ResourceScriptEngine.execute_lines` (method) `modules/resource_script.py:293` `def execute_lines(self, lines, source)` -- Execute a list of script lines.
- `ResourceScriptEngine.execute_string` (method) `modules/resource_script.py:327` `def execute_string(self, script)` -- Execute a script string (split on newlines).

## modules/retry_session.py
Depends on: `modules/chain_state.py`
Imported by: `cli/retry_support.py`, `tests/test_codeql_alert_fixes.py`, `tests/test_retry_session.py`
- `is_active` (function) `modules/retry_session.py:56` `def is_active()` -- Return True when an elevated retry session is currently armed.
- `secret_enabled_path` (function) `modules/retry_session.py:61` `def secret_enabled_path()` -- Return the askpass helper path advertised via ``SUDO_ASKPASS``.
- `sudo_gate_open` (function) `modules/retry_session.py:79` `def sudo_gate_open()` -- Return True when armed and the on-disk askpass pair is sound.
- `set_sudo_secret` (function) `modules/retry_session.py:94` `def set_sudo_secret(secret)` -- Arm the elevated retry session with one secret.
- `clear_sudo_secret` (function) `modules/retry_session.py:125` `def clear_sudo_secret()` -- Disarm the elevated retry session and wipe the secret from disk.
- `apply_sudo_askpass` (function) `modules/retry_session.py:137` `def apply_sudo_askpass(command)` -- Rewrite bare ``sudo`` tokens to ``sudo -A`` for one command.
- `newest_failed_checkpoint` (function) `modules/retry_session.py:180` `def newest_failed_checkpoint(chain, run_id)` -- Return the freshest unfinished checkpoint of one chain.
- `resolve_sudo_consent` (function) `modules/retry_session.py:204` `def resolve_sudo_consent(confirmer, want_sudo)` -- Gate the elevated mode behind an explicit, warned confirmation.

## modules/reverse-shell.c
Depends on: `modules/selection/module.py`
- `reverse_shell_init` (function) `modules/reverse-shell.c:12` `static int __init reverse_shell_init(void)` -- call_usermodehelper function is used to create user mode processes from kernel space
- `reverse_shell_exit` (function) `modules/reverse-shell.c:16` `static void __exit reverse_shell_exit(void)`

## modules/revshell.c
- `xlAutoOpen` (function) `modules/revshell.c:5` `void __cdecl xlAutoOpen()`
- `DllMain` (function) `modules/revshell.c:10` `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`

## modules/rich_tui.py
Depends on: `core/console.py`, `modules/dashboard_engine.py`
Imported by: `cli/commands/pwn.py`
- `RichDashboard.__init__` (method) `modules/rich_tui.py:74` `def __init__(self, dashboard_engine, refresh_interval, live)` -- Initialize the Rich dashboard.
- `RichDashboard.run` (method) `modules/rich_tui.py:96` `def run(self)` -- Run the dashboard.
- `RichDashboard.stop` (method) `modules/rich_tui.py:132` `def stop(self)` -- Gracefully shut down the dashboard and restore terminal state.

## modules/rl_trainer.py
Depends on: `core/logging.py`
Imported by: `modules/lesson_ingestor.py`, `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/swan_agent.py`, `tests/test_moe_rl_swan.py`
- `IStateEncoder.encode` (method) `modules/rl_trainer.py:105` `def encode(self, task_type, engagement_phase, recent_reward_ema)` -- Return a string key representing the current state.
- `BucketedStateEncoder.encode` (method) `modules/rl_trainer.py:131` `def encode(self, task_type, engagement_phase, recent_reward_ema)`
- `QValueStore.__init__` (method) `modules/rl_trainer.py:156` `def __init__(self, path, optimistic_init)`
- `QValueStore.get` (method) `modules/rl_trainer.py:168` `def get(self, state, action)`
- `QValueStore.set` (method) `modules/rl_trainer.py:172` `def set(self, state, action, value)`
- `QValueStore.max_q` (method) `modules/rl_trainer.py:176` `def max_q(self, state, candidates)` -- Return max Q(state, a) over the given candidate actions.
- `QValueStore.argmax` (method) `modules/rl_trainer.py:182` `def argmax(self, state, candidates)` -- Return the action with highest Q(state, a).
- `QValueStore.save` (method) `modules/rl_trainer.py:188` `def save(self)`
- `EpsilonTracker.__init__` (method) `modules/rl_trainer.py:218` `def __init__(self, start, minimum, decay, path)`
- `EpsilonTracker.epsilon` (method) `modules/rl_trainer.py:233` `def epsilon(self)`
- `EpsilonTracker.step` (method) `modules/rl_trainer.py:236` `def step(self)` -- Apply one decay step and persist.
- `RLTrainer.__init__` (method) `modules/rl_trainer.py:284` `def __init__(self, config, state_encoder, q_store, epsilon_tracker)`
- `RLTrainer.encode_state` (method) `modules/rl_trainer.py:304` `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` -- Convert environment observations into a discrete state key.
- `RLTrainer.select_action` (method) `modules/rl_trainer.py:313` `def select_action(self, state, candidates, force_exploit)` -- Epsilon-greedy expert selection.
- `RLTrainer.update` (method) `modules/rl_trainer.py:347` `def update(self, state, action, reward, next_state, candidates, detection_prob)` -- Apply one Q-learning update.
- `RLTrainer.best_expert_for_state` (method) `modules/rl_trainer.py:389` `def best_expert_for_state(self, state, candidates)` -- Return the highest Q-value expert for the given state (greedy).
- `RLTrainer.q_values_for_state` (method) `modules/rl_trainer.py:393` `def q_values_for_state(self, state, candidates)` -- Return {expert_id: q_value} for diagnostics.
- `RLTrainer.save` (method) `modules/rl_trainer.py:397` `def save(self)` -- Persist Q-table to disk.
- `RLTrainer.epsilon` (method) `modules/rl_trainer.py:402` `def epsilon(self)`
- `get_trainer` (function) `modules/rl_trainer.py:425` `def get_trainer(config)` -- Return (or create) the module-level singleton RLTrainer.

## modules/rootkit/mr.c
- `get_ld_preload` (function) `modules/rootkit/mr.c:84` `char *get_ld_preload()`
- `set_ld_preload` (function) `modules/rootkit/mr.c:87` `void set_ld_preload(const char *ld_preload)`
- `ensure_ld_preload` (function) `modules/rootkit/mr.c:100` `void ensure_ld_preload()`
- `ensure_pid_file_exists` (function) `modules/rootkit/mr.c:117` `void ensure_pid_file_exists()`
- `check_elevate` (function) `modules/rootkit/mr.c:136` `int check_elevate()`
- `write_file` (function) `modules/rootkit/mr.c:145` `void write_file(const char *path, const char *content, mode_t mode)`
- `crontab` (function) `modules/rootkit/mr.c:156` `void crontab(const char *path)`
- `generate_random_string` (function) `modules/rootkit/mr.c:168` `char *generate_random_string()`
- `xdg` (function) `modules/rootkit/mr.c:178` `void xdg(const char *path, int admin)`
- `kde_plasma` (function) `modules/rootkit/mr.c:200` `void kde_plasma(const char *path)`
- `copy_binary` (function) `modules/rootkit/mr.c:215` `void copy_binary(const char *source, const char *destination)`
- `persist` (function) `modules/rootkit/mr.c:234` `void persist(const char *path)`
- `ensure_key_file_exists` (function) `modules/rootkit/mr.c:253` `void ensure_key_file_exists()`
- `ensure_hide_file_exists` (function) `modules/rootkit/mr.c:271` `void ensure_hide_file_exists()`
- `infect_command` (function) `modules/rootkit/mr.c:289` `void infect_command()`
- `load_rootkit` (function) `modules/rootkit/mr.c:303` `void load_rootkit()`
- `unload_rootkit` (function) `modules/rootkit/mr.c:314` `void unload_rootkit()`
- `handle_client` (function) `modules/rootkit/mr.c:321` `void *handle_client(void *client_socket)`
- `mon_shell` (function) `modules/rootkit/mr.c:521` `void *mon_shell(void *data)`
- `signal_handler` (function) `modules/rootkit/mr.c:609` `void signal_handler(int signum)`
- `reboot_system` (function) `modules/rootkit/mr.c:615` `void reboot_system()`
- `main` (function) `modules/rootkit/mr.c:639` `int main()`

## modules/rootkit/mrhyde.c
- `load_hidden_pids` (function) `modules/rootkit/mrhyde.c:77` `void load_hidden_pids()`
- `load_hidden_files` (function) `modules/rootkit/mrhyde.c:97` `void load_hidden_files()`
- `unlink` (function) `modules/rootkit/mrhyde.c:117` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde.c:129` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde.c:149` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde.c:161` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde.c:182` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde.c:201` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde.c:216` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde.c:226` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde.c:287` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde.c:331` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde.c:375` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde.c:419` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde.c:463` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde.c:507` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde.c:561` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde.c:622` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde.c:682` `int main()`

## modules/rootkit/mrhyde2.c
- `load_hidden_pids` (function) `modules/rootkit/mrhyde2.c:67` `void load_hidden_pids()`
- `unlink` (function) `modules/rootkit/mrhyde2.c:87` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde2.c:99` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde2.c:119` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde2.c:131` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde2.c:152` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde2.c:171` `int should_hide_pid(const char* pid)`
- `readdir` (function) `modules/rootkit/mrhyde2.c:186` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde2.c:242` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde2.c:279` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde2.c:316` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde2.c:353` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde2.c:390` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde2.c:427` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde2.c:474` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde2.c:531` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde2.c:587` `int main()`

## modules/rootkit/mrhyde3.c
- `uring_queue_init` (function) `modules/rootkit/mrhyde3.c:89` `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` -- /* Syscalls static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p) { return...
- `uring_get_sqe` (function) `modules/rootkit/mrhyde3.c:134` `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` -- ring->cq.head = (unsigned *)((char *)cq_ring + params.cq_off.head); ring->cq.tail = (unsigned *)((char *)cq_ring +...
- `uring_submit` (function) `modules/rootkit/mrhyde3.c:145` `static int uring_submit(struct io_uring *ring)` -- } /* Obtener SQE static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring) { unsigned head = *ring->sq.head...
- `uring_wait_cqe_timeout` (function) `modules/rootkit/mrhyde3.c:153` `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` -- struct io_uring_sqe *sqe = &ring->sq.sqes[tail & *ring->sq.ring_mask]; memset(sqe, 0, sizeof(*sqe)); return sqe; }...
- `uring_cqe_seen` (function) `modules/rootkit/mrhyde3.c:167` `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)`
- `init_root_ring` (function) `modules/rootkit/mrhyde3.c:180` `static int init_root_ring(void)` -- static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe) { (*ring->cq.head)++; } /* Estado global...
- `uring_read_whole_file` (function) `modules/rootkit/mrhyde3.c:201` `static char *uring_read_whole_file(const char *path)` -- } ring_ok = 1; /* Registrar buffer (opcional) struct iovec iov; iov.iov_base = malloc(IO_URING_BUFFER_SIZE)...
- `traditional_read_file` (function) `modules/rootkit/mrhyde3.c:257` `static char *traditional_read_file(const char *path)` -- if (bytes_read <= 0) break; buf = realloc(buf, total_read + bytes_read + 1); if (!buf) { close(fd)...
- `load_hidden_pids` (function) `modules/rootkit/mrhyde3.c:272` `void load_hidden_pids(void)` -- FILE *f = fopen(path, "rb"); if (!f) return NULL; fseek(f, 0, SEEK_END); long size = ftell(f); fseek(f, 0...
- `load_hidden_files` (function) `modules/rootkit/mrhyde3.c:286` `void load_hidden_files(void)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde3.c:301` `char* get_username_from_pid(pid_t pid)` -- char *data = uring_read_whole_file(FILE_HIDE_PATH); if (!data) data = traditional_read_file(FILE_HIDE_PATH); if...
- `should_hide_pid` (function) `modules/rootkit/mrhyde3.c:324` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde3.c:333` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde3.c:340` `struct dirent* readdir(DIR* dirp)`
- `unlink` (function) `modules/rootkit/mrhyde3.c:371` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde3.c:377` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde3.c:387` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde3.c:393` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `fopen` (function) `modules/rootkit/mrhyde3.c:411` `FILE *fopen(const char *pathname, const char *mode)`
- `open` (function) `modules/rootkit/mrhyde3.c:434` `int open(const char *pathname, int flags, ...)`
- `openat` (function) `modules/rootkit/mrhyde3.c:462` `int openat(int dirfd, const char *pathname, int flags, ...)`
- `stat` (function) `modules/rootkit/mrhyde3.c:491` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde3.c:515` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde3.c:539` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde3.c:573` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde3.c:609` `ssize_t getdents64(int fd, void *dirp, size_t count)`

## modules/rootkit/rootkit.c
Depends on: `core/crypto.py`, `lazyown-docker/init.sh`, `modules/selection/module.py`
- `regs_override_return` (function) `modules/rootkit/rootkit.c:54` `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` -- Define regs_override_return function
- `hooked_getdents` (function) `modules/rootkit/rootkit.c:86` `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents function
- `hooked_getdents64` (function) `modules/rootkit/rootkit.c:112` `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents64 function
- `hooked_read` (function) `modules/rootkit/rootkit.c:138` `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked read function to create a backdoor
- `disable_module_signature_verification` (function) `modules/rootkit/rootkit.c:192` `static void disable_module_signature_verification(void)` -- Function to disable module signature verification
- `hook_syscalls` (function) `modules/rootkit/rootkit.c:206` `static int __init hook_syscalls(void)` -- Function to hook system calls
- `unhook_syscalls` (function) `modules/rootkit/rootkit.c:219` `static void __exit unhook_syscalls(void)` -- Function to unhook system calls

## modules/saas_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `SaaSEnumerationTools.microsoft365_commands` (method) `modules/saas_attacks.py:75` `def microsoft365_commands()`
- `SaaSEnumerationTools.google_workspace_commands` (method) `modules/saas_attacks.py:100` `def google_workspace_commands()`
- `SaaSEnumerationTools.salesforce_commands` (method) `modules/saas_attacks.py:118` `def salesforce_commands()`
- `SaaSEnumerationTools.servicenow_commands` (method) `modules/saas_attacks.py:135` `def servicenow_commands()`
- `SaaSAttackEngine.__init__` (method) `modules/saas_attacks.py:163` `def __init__(self, config)`
- `SaaSAttackEngine.enumerate_all` (method) `modules/saas_attacks.py:166` `def enumerate_all(self)` -- Generate enumeration commands for all supported SaaS platforms.
- `SaaSAttackEngine.m365_ews_mail_search` (method) `modules/saas_attacks.py:179` `def m365_ews_mail_search(self, search_term)` -- Search mailboxes via Exchange Web Services (EWS).
- `SaaSAttackEngine.google_workspace_domain_wide_delegation` (method) `modules/saas_attacks.py:228` `def google_workspace_domain_wide_delegation(self)` -- Abuse Google Workspace Domain-Wide Delegation (DWD).
- `SaaSAttackEngine.salesforce_report_mining` (method) `modules/saas_attacks.py:257` `def salesforce_report_mining(self)` -- Mine Salesforce reports and dashboards for sensitive data.
- `SaaSAttackEngine.slack_data_mining` (method) `modules/saas_attacks.py:286` `def slack_data_mining(self)` -- Mine Slack Enterprise for sensitive conversations and files.
- `SaaSAttackEngine.detect_external_sharing` (method) `modules/saas_attacks.py:327` `def detect_external_sharing(self)` -- Detect external sharing configurations across SaaS platforms.
- `SaaSAttackEngine.summary` (method) `modules/saas_attacks.py:352` `def summary(self)`

## modules/security_sanitizers.py
Imported by: `lazyc2.py`, `lazyc2/blueprints/phishing.py`, `modules/lazyown_bprfuzzer.py`, `pwntomate.py`, `tests/test_security_sanitizers.py`
- `SecurityConfig.from_payload` (method) `modules/security_sanitizers.py:68` `def from_payload(cls, payload)` -- Build a configuration object from a ``payload.json`` mapping.
- `HeaderValueSanitizer.__init__` (method) `modules/security_sanitizers.py:115` `def __init__(self, config)` -- Bind the sanitizer to a configuration instance.
- `HeaderValueSanitizer.is_valid_name` (method) `modules/security_sanitizers.py:129` `def is_valid_name(self, name)` -- Return True iff ``name`` is a syntactically valid header token.
- `HeaderValueSanitizer.sanitize_value` (method) `modules/security_sanitizers.py:139` `def sanitize_value(self, value)` -- Return a header value that cannot smuggle a response split.
- `SessionPathResolver.__init__` (method) `modules/security_sanitizers.py:174` `def __init__(self, base_dir, config)` -- Bind the resolver to an absolute, real base directory.
- `SessionPathResolver.base_dir` (method) `modules/security_sanitizers.py:192` `def base_dir(self)` -- The resolved, absolute base directory.
- `SessionPathResolver.resolve` (method) `modules/security_sanitizers.py:196` `def resolve(self, untrusted_name)` -- Return ``(absolute, relative)`` for a safe filename.
- `SessionPathResolver.file_exists` (method) `modules/security_sanitizers.py:238` `def file_exists(self, untrusted_name)` -- Return True iff ``untrusted_name`` resolves to an existing file.
- `BindAddressResolver.__init__` (method) `modules/security_sanitizers.py:269` `def __init__(self, config, preferred_addresses)` -- Build a resolver with a prioritised list of candidate addresses.
- `BindAddressResolver.resolve` (method) `modules/security_sanitizers.py:298` `def resolve(self)` -- Return the address sockets should bind to.
- `CommandRedactor.__init__` (method) `modules/security_sanitizers.py:333` `def __init__(self, config)` -- Bind the redactor to a configuration instance.
- `CommandRedactor.render` (method) `modules/security_sanitizers.py:359` `def render(self, template, substitutions, username, password)` -- Return ``(executable, display)`` for a templated command.
- `OutputSanitizer.__init__` (method) `modules/security_sanitizers.py:418` `def __init__(self, config)` -- Bind the sanitizer to a configuration instance.
- `OutputSanitizer.sanitize` (method) `modules/security_sanitizers.py:429` `def sanitize(self, value)` -- Return ``value`` projected into a JSON-serialisable form.
- `build_default_config` (function) `modules/security_sanitizers.py:477` `def build_default_config(payload)` -- Return a :class:`SecurityConfig` populated from ``payload``.

## modules/selection/adversary.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`
- `load_profiles` (function) `modules/selection/adversary.py:26` `def load_profiles(adversaries_dir)` -- Load every adversary profile dictionary shipped in the repo.
- `resolve_profile` (function) `modules/selection/adversary.py:80` `def resolve_profile(goal, adversaries_dir)` -- Resolve the adversary profile the goal names, if any.
- `AdversarySelector.__init__` (method) `modules/selection/adversary.py:123` `def __init__(self, adversaries_dir, confirm)` -- Bind the profile directory and the execution confirmation word.
- `AdversarySelector.propose` (method) `modules/selection/adversary.py:136` `def propose(self, ctx)` -- Return the emulation action when the goal names a profile.

## modules/selection/atomic.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`, `tests/test_selectors_capabilities.py`
- `AtomicSelector.propose` (method) `modules/selection/atomic.py:25` `def propose(self, ctx)` -- Return an atomic-emulation action when technique ids are named.

## modules/selection/base.py
Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/edb.py`, `modules/selection/intel.py`, `modules/selection/lazyscript.py`, `modules/selection/module.py`, `modules/selection/playbook.py`, `modules/selection/poc.py`, `modules/selection/registry.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`, `skills/autonomous_daemon.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`, `tests/test_poc_registry.py`, `tests/test_selection_lazyscript.py`, `tests/test_selection_module.py`, `tests/test_selection_technique.py`, `tests/test_selection_technique_chain.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`
- `Selector.propose` (method) `modules/selection/base.py:73` `def propose(self, ctx)` -- Return the next action for this strategy, or None to abstain.

## modules/selection/chain.py
Depends on: `modules/chain_match.py`, `modules/selection/base.py`
Imported by: `modules/exp.c`, `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_base.py`
- `ChainSelector.__init__` (method) `modules/selection/chain.py:18` `def __init__(self, allow_lab)` -- Bind the lab-inclusion policy for the matcher.
- `ChainSelector.propose` (method) `modules/selection/chain.py:27` `def propose(self, ctx)` -- Return a chain action for the context, or None when nothing fits.

## modules/selection/cred_spray.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_capabilities.py`
- `CredentialSpraySelector.propose` (method) `modules/selection/cred_spray.py:37` `def propose(self, ctx)` -- Return a spray verb for the first matching open service, or None.

## modules/selection/edb.py
Depends on: `modules/__init__.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`
- `EDBSelector.propose` (method) `modules/selection/edb.py:11` `def propose(self, ctx)`

## modules/selection/intel.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`
- `intel_report_path` (function) `modules/selection/intel.py:32` `def intel_report_path(target)` -- Return the saved exposure report path for one target.
- `load_report` (function) `modules/selection/intel.py:44` `def load_report(target)` -- Read the saved exposure report of one target.
- `pending_fires` (function) `modules/selection/intel.py:60` `def pending_fires(target)` -- Fire-tier bounded matches of a target not covered by a chain yet.
- `IntelSelector.propose` (method) `modules/selection/intel.py:117` `def propose(self, ctx)` -- Return the next intelligence action, or None when none applies.

## modules/selection/lazyscript.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_lazyscript.py`
- `LazyscriptSelector.__init__` (method) `modules/selection/lazyscript.py:41` `def __init__(self, scripts_dir)` -- Bind the lazyscripts directory (overridable for tests).
- `LazyscriptSelector.propose` (method) `modules/selection/lazyscript.py:56` `def propose(self, ctx)` -- Return a lazyscript action for the context, or None when none fit.

## modules/selection/module.py
Depends on: `modules/module_registry.py`, `modules/selection/base.py`
Imported by: `modules/reverse-shell.c`, `modules/rootkit/rootkit.c`, `modules/selection/registry.py`, `static/js/select2-4.1.0.min.js`, `tests/test_selection_module.py`
- `ModuleSelector.propose` (method) `modules/selection/module.py:21` `def propose(self, ctx)` -- Return the first unproposed registry intent, or None.

## modules/selection/playbook.py
Depends on: `modules/apt_playbooks.py`, `modules/chain_registry.py`, `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`
- `PlaybookSelector.__init__` (method) `modules/selection/playbook.py:79` `def __init__(self, playbook_dir)` -- Bind the playbook directory for summary loading.
- `PlaybookSelector.propose` (method) `modules/selection/playbook.py:128` `def propose(self, ctx)` -- Return an actor-emulation action when the goal names one, else None.

## modules/selection/poc.py
Depends on: `modules/__init__.py`, `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_poc_registry.py`
- `PoCSelector.propose` (method) `modules/selection/poc.py:25` `def propose(self, ctx)` -- Return a PoC action for the context, or None when nothing fits.

## modules/selection/registry.py
Depends on: `modules/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/base.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/edb.py`, `modules/selection/intel.py`, `modules/selection/lazyscript.py`, `modules/selection/module.py`, `modules/selection/playbook.py`, `modules/selection/poc.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`
Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `skills/autonomous_daemon.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`
- `all_selectors` (function) `modules/selection/registry.py:31` `def all_selectors()` -- Return every shared selector in priority order, before admin filtering.
- `default_selectors` (function) `modules/selection/registry.py:61` `def default_selectors()` -- Return the cascade after applying the orchestrator's enable toggles.
- `propose_next` (function) `modules/selection/registry.py:76` `def propose_next(ctx, selectors)` -- Return the best concrete decision from the cascade, or None.

## modules/selection/technique.py
Depends on: `modules/playbook_engine.py`, `modules/selection/atomic.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_technique.py`
- `TechniqueSelector.propose` (method) `modules/selection/technique.py:23` `def propose(self, ctx)` -- Return a technique emulation action, or None when not applicable.

## modules/selection/technique_chain.py
Depends on: `modules/chain_registry.py`, `modules/chain_synth.py`, `modules/playbook_engine.py`, `modules/selection/atomic.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_technique_chain.py`
- `TechniqueChainSelector.propose` (method) `modules/selection/technique_chain.py:53` `def propose(self, ctx)` -- Return a technique-chain action, or None when fewer than two fit.

## modules/selector_manager.py
Imported by: `tests/test_auto_loop_memory.py`
- `select` (function) `modules/selector_manager.py:42` `def select(proposals, is_blocked)` -- Pick the first valid proposal; None when everything is filtered.

## modules/selfupdate.py
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_loop.py`
- `Updater.__init__` (method) `modules/selfupdate.py:47` `def __init__(self, live_path)` -- Bind the updater to the binary that may be replaced.
- `Updater.verify` (method) `modules/selfupdate.py:52` `def verify(self, artifact)` -- Return True when the payload matches its recorded digest.
- `Updater.stage` (method) `modules/selfupdate.py:57` `def stage(self, artifact, directory)` -- Write a verified payload into ``directory``.
- `Updater.rollback` (method) `modules/selfupdate.py:77` `def rollback(self)` -- Restore the ``<name>.old`` snapshot over the live binary.
- `current_branch` (function) `modules/selfupdate.py:96` `def current_branch(runner)` -- Return the checked-out branch name (empty on failure).
- `dirty` (function) `modules/selfupdate.py:102` `def dirty(runner)` -- Return True when the working tree has uncommitted changes.
- `check` (function) `modules/selfupdate.py:108` `def check(branch, runner)` -- Fetch the branch and report ahead/behind counts.
- `apply` (function) `modules/selfupdate.py:140` `def apply(branch, confirm, runner)` -- Fast-forward the tree to origin/<branch> when safe.

## modules/session_cleanup.py
Imported by: `lazyown.py`, `tests/test_infra_disposable.py`
- `find_cloudflared_pids` (function) `modules/session_cleanup.py:28` `def find_cloudflared_pids(ps_output)` -- Extract PIDs of ``cloudflared tunnel`` processes from ps output.
- `stop_cloudflared_processes` (function) `modules/session_cleanup.py:94` `def stop_cloudflared_processes()` -- Terminate stray ``cloudflared tunnel`` host processes.
- `cleanup_ephemeral_infra` (function) `modules/session_cleanup.py:120` `def cleanup_ephemeral_infra()` -- Stop all disposable infrastructure owned by this checkout.


Next: [API_p19.md](API_p19.md)
