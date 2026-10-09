# API (page 13 of 20)
Previous: [API_p12.md](API_p12.md)

## modules/payload_factory.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/payload_generation.py`, `cli/commands/session_ops.py`, `lazyown.py`, `scripts/devtools/core_smoke.py`, `tests/test_payload_factory.py`
- `PayloadTemplate.__init__` (method) `modules/payload_factory.py:218` `def __init__(self, name, platform, arch, description, options)`
- `PayloadTemplate.generate` (method) `modules/payload_factory.py:233` `def generate(self)` -- Generate the raw payload bytes.
- `PayloadTemplate.to_dict` (method) `modules/payload_factory.py:237` `def to_dict(self)`
- `ReverseShellPayload.__init__` (method) `modules/payload_factory.py:250` `def __init__(self)`
- `ReverseShellPayload.generate` (method) `modules/payload_factory.py:268` `def generate(self)`
- `WindowsReverseShellPayload.__init__` (method) `modules/payload_factory.py:289` `def __init__(self)`
- `WindowsReverseShellPayload.generate` (method) `modules/payload_factory.py:301` `def generate(self)`
- `MsfvenomPayload.__init__` (method) `modules/payload_factory.py:321` `def __init__(self, name, platform, arch)`
- `MsfvenomPayload.generate` (method) `modules/payload_factory.py:333` `def generate(self)`
- `ShellcodePayload.__init__` (method) `modules/payload_factory.py:366` `def __init__(self, name, platform, arch, description, escaped_hex, patcher)`
- `ShellcodePayload.generate` (method) `modules/payload_factory.py:389` `def generate(self)` -- Return the shellcode, optionally patching LHOST / LPORT.
- `DynamicShellcodePayload.__init__` (method) `modules/payload_factory.py:408` `def __init__(self, name, platform, arch, description, builder)`
- `DynamicShellcodePayload.generate` (method) `modules/payload_factory.py:428` `def generate(self)`
- `PayloadFactory.__init__` (method) `modules/payload_factory.py:456` `def __init__(self)`
- `PayloadFactory.register` (method) `modules/payload_factory.py:504` `def register(self, template)` -- Register a custom payload template.
- `PayloadFactory.list` (method) `modules/payload_factory.py:508` `def list(self, platform)` -- List all registered payloads, optionally filtered by platform.
- `PayloadFactory.get` (method) `modules/payload_factory.py:517` `def get(self, name)` -- Get a payload template by name.
- `PayloadFactory.generate` (method) `modules/payload_factory.py:521` `def generate(self, name, format, output)` -- Generate a payload by name.
- `PayloadFactory.list_formats` (method) `modules/payload_factory.py:665` `def list_formats()` -- List all available output formats.
- `PayloadFactory.format_payload_table` (method) `modules/payload_factory.py:673` `def format_payload_table(payloads)` -- Format a list of payload dicts as an aligned table.

## modules/phishing_orchestrator.py
Depends on: `core/crypto.py`, `core/hardening.py`
Imported by: `cli/commands/phishing_wizard.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `PhishingOrchestrator.__init__` (method) `modules/phishing_orchestrator.py:316` `def __init__(self)`
- `PhishingOrchestrator.get_instance` (method) `modules/phishing_orchestrator.py:321` `def get_instance(cls)`
- `PhishingOrchestrator.launch` (method) `modules/phishing_orchestrator.py:332` `def launch(self, target_domain, template, mode, targets_file, sender_email, sender_password, smtp_host, smtp_port)` -- Launch a phishing campaign.
- `PhishingOrchestrator.profile_targets` (method) `modules/phishing_orchestrator.py:441` `def profile_targets(self, domain)` -- Profile targets for a domain using OSINT techniques.
- `PhishingOrchestrator.generate_template` (method) `modules/phishing_orchestrator.py:486` `def generate_template(self, name, target_domain, context)` -- Generate or retrieve a phishing template.
- `PhishingOrchestrator.clone_landing_page` (method) `modules/phishing_orchestrator.py:533` `def clone_landing_page(self, url)` -- Clone a target login page for credential harvesting.
- `PhishingOrchestrator.get_results` (method) `modules/phishing_orchestrator.py:560` `def get_results(self, campaign_id)` -- Get campaign results.
- `PhishingOrchestrator.record_click` (method) `modules/phishing_orchestrator.py:584` `def record_click(self, campaign_id, email)` -- Record a link click.
- `PhishingOrchestrator.record_credentials` (method) `modules/phishing_orchestrator.py:605` `def record_credentials(self, campaign_id, email, password)` -- Record harvested credentials.

## modules/pipeline_engine.py
Depends on: `core/logging.py`, `modules/engagement_hooks.py`, `skills/autonomous_daemon.py`
Imported by: `cli/commands/session_ops.py`, `modules/playbook_executor.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_pipeline_engine.py`
- `StepResult.to_context` (method) `modules/pipeline_engine.py:178` `def to_context(self)` -- Render the step result as a dict for template lookups.
- `PipelineRun.to_dict` (method) `modules/pipeline_engine.py:211` `def to_dict(self)` -- Return a JSON-friendly representation of the full run.
- `TemplateResolver.__init__` (method) `modules/pipeline_engine.py:273` `def __init__(self, context)`
- `TemplateResolver.render` (method) `modules/pipeline_engine.py:276` `def render(self, template)`
- `TemplateResolver.resolve` (method) `modules/pipeline_engine.py:287` `def resolve(self, dotted_path)` -- Return the value at dotted_path or None when not found.
- `ConditionEvaluator.is_truthy` (method) `modules/pipeline_engine.py:328` `def is_truthy(rendered)`
- `StepValidator.validate` (method) `modules/pipeline_engine.py:350` `def validate(predicate, output)`
- `StepDerivers.register` (method) `modules/pipeline_engine.py:387` `def register(cls, command, deriver)` -- Bind a deriver to a top-level command name (case-insensitive).
- `StepDerivers.derive` (method) `modules/pipeline_engine.py:396` `def derive(cls, command, output)` -- Run the registered deriver for command on output, defensive.
- `IStepRunner.run` (method) `modules/pipeline_engine.py:511` `def run(self, command, args, target, timeout_s)` -- Execute one command.
- `LazyOwnStepRunner.__init__` (method) `modules/pipeline_engine.py:531` `def __init__(self, runner, onecmd)`
- `LazyOwnStepRunner.run` (method) `modules/pipeline_engine.py:543` `def run(self, command, args, target, timeout_s)`
- `PipelineLoader.__init__` (method) `modules/pipeline_engine.py:610` `def __init__(self, pipelines_dir)`
- `PipelineLoader.pipelines_dir` (method) `modules/pipeline_engine.py:614` `def pipelines_dir(self)`
- `PipelineLoader.list` (method) `modules/pipeline_engine.py:617` `def list(self)` -- Return every pipeline name discoverable in pipelines_dir.
- `PipelineLoader.resolve_path` (method) `modules/pipeline_engine.py:630` `def resolve_path(self, name)` -- Return the absolute path to the YAML file for the given name.
- `PipelineLoader.load` (method) `modules/pipeline_engine.py:661` `def load(self, name)` -- Parse the YAML file for name and return a validated spec.
- `RunArtifactStore.__init__` (method) `modules/pipeline_engine.py:765` `def __init__(self, runs_dir)`
- `RunArtifactStore.runs_dir` (method) `modules/pipeline_engine.py:769` `def runs_dir(self)`
- `RunArtifactStore.open_run` (method) `modules/pipeline_engine.py:772` `def open_run(self, pipeline_name, run_id)` -- Create and return the directory for this run.
- `RunArtifactStore.write_plan` (method) `modules/pipeline_engine.py:784` `def write_plan(self, run_dir, spec)`
- `RunArtifactStore.write_step` (method) `modules/pipeline_engine.py:801` `def write_step(self, run_dir, result)`
- `RunArtifactStore.write_summary` (method) `modules/pipeline_engine.py:815` `def write_summary(self, run_dir, run)`
- `INarratorAdapter.narrate` (method) `modules/pipeline_engine.py:839` `def narrate(self, kind, target, message, payload, severity)` -- Emit one narration event.
- `_SilentNarrator.narrate` (method) `modules/pipeline_engine.py:851` `def narrate(self)`
- `EngagementNarratorAdapter.__init__` (method) `modules/pipeline_engine.py:858` `def __init__(self, narrator)`
- `EngagementNarratorAdapter.narrate` (method) `modules/pipeline_engine.py:867` `def narrate(self, kind, target, message, payload, severity)`
- `PipelineEngine.__init__` (method) `modules/pipeline_engine.py:913` `def __init__(self, runner, loader, artifact_store, narrator, max_nesting)`
- `PipelineEngine.loader` (method) `modules/pipeline_engine.py:928` `def loader(self)`
- `PipelineEngine.validate` (method) `modules/pipeline_engine.py:931` `def validate(self, name)` -- Load and validate without executing.
- `PipelineEngine.run` (method) `modules/pipeline_engine.py:935` `def run(self, name, target, nesting_stack)` -- Execute the pipeline.
- `PipelineEngine.get_default_engine` (method) `modules/pipeline_engine.py:1288` `def get_default_engine(onecmd)` -- Process-wide default engine for production callers.
- `PipelineEngine.mcp_pipeline_run` (method) `modules/pipeline_engine.py:1302` `def mcp_pipeline_run(name, target, background, onecmd)` -- Public MCP / CLI entry: run a pipeline.
- `PipelineEngine.mcp_pipeline_list` (method) `modules/pipeline_engine.py:1352` `def mcp_pipeline_list()` -- Return the list of available pipelines under pipelines/.
- `PipelineEngine.mcp_pipeline_validate` (method) `modules/pipeline_engine.py:1366` `def mcp_pipeline_validate(name)` -- Validate a pipeline's YAML schema without executing it.
- `PipelineEngine.mcp_pipeline_status` (method) `modules/pipeline_engine.py:1392` `def mcp_pipeline_status(last_n)` -- Return the N most recent pipeline runs and their summaries.
- `PipelineEngine.cmd_pipeline` (method) `modules/pipeline_engine.py:1414` `def cmd_pipeline(action, name, target, background)` -- CLI helper bound to the ``pipeline`` daemon subcommand.

## modules/planner.py
Depends on: `core/logging.py`, `modules/llm_client.py`, `modules/obs_parser.py`, `modules/playbook_engine.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`
- `Planner.__init__` (method) `modules/planner.py:231` `def __init__(self, world_model, obs_parser, api_key)`
- `Planner.plan` (method) `modules/planner.py:273` `def plan(self, target, max_candidates)` -- Return a ranked list of next-step candidates for *target*.
- `Planner.to_dict` (method) `modules/planner.py:373` `def to_dict(self, result)`
- `Planner.get_planner` (method) `modules/planner.py:406` `def get_planner(api_key)`

## modules/playbook_engine.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/llm_client.py`, `modules/obs_parser.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`, `cli/commands/mcp_bridge.py`, `modules/operation.py`, `modules/planner.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `PlaybookStep.to_dict` (method) `modules/playbook_engine.py:108` `def to_dict(self)`
- `PlaybookStep.from_dict` (method) `modules/playbook_engine.py:123` `def from_dict(cls, d)`
- `Playbook.to_dict` (method) `modules/playbook_engine.py:136` `def to_dict(self)`
- `Playbook.from_dict` (method) `modules/playbook_engine.py:147` `def from_dict(cls, d)`
- `_StixLoader.__init__` (method) `modules/playbook_engine.py:182` `def __init__(self, json_path)`
- `_StixLoader.available` (method) `modules/playbook_engine.py:186` `def available(self)`
- `_StixLoader.store` (method) `modules/playbook_engine.py:189` `def store(self)`
- `_StixLoader.techniques_for_tactics` (method) `modules/playbook_engine.py:203` `def techniques_for_tactics(self, tactic_shortnames, platform)` -- Return ATT&CK techniques matching the given tactic shortnames.
- `_AtomicIndex.__init__` (method) `modules/playbook_engine.py:252` `def __init__(self, atomics_path)`
- `_AtomicIndex.available` (method) `modules/playbook_engine.py:256` `def available(self)`
- `_AtomicIndex.build` (method) `modules/playbook_engine.py:259` `def build(self)`
- `_AtomicIndex.tests_for_technique` (method) `modules/playbook_engine.py:290` `def tests_for_technique(self, technique_id, platform)`
- `_TechniqueSelector.select` (method) `modules/playbook_engine.py:307` `def select(self, candidates, world_context, target, phase, api_key, top_n)`
- `PlaybookEngine.__init__` (method) `modules/playbook_engine.py:374` `def __init__(self, world_model, obs_parser, api_key, top_n)`
- `PlaybookEngine.derive` (method) `modules/playbook_engine.py:412` `def derive(self, target, phase, platform, apt_name)` -- Generate a Playbook for *target* at the given *phase*.
- `PlaybookEngine.execute` (method) `modules/playbook_engine.py:508` `def execute(self, playbook, executor, dry_run)` -- Execute a Playbook step by step.
- `PlaybookEngine.save` (method) `modules/playbook_engine.py:573` `def save(self, playbook, path)` -- Persist playbook to YAML (compatible with existing playbooks/ format).
- `PlaybookEngine.load` (method) `modules/playbook_engine.py:586` `def load(self, path)` -- Load a playbook from YAML.
- `PlaybookEngine.result_summary` (method) `modules/playbook_engine.py:613` `def result_summary(self, result)` -- Return a human-readable / LLM-readable summary of a PlaybookResult.
- `PlaybookEngine.get_engine` (method) `modules/playbook_engine.py:648` `def get_engine(api_key)` -- Return (or create) the module-level singleton PlaybookEngine.

## modules/playbook_executor.py
Depends on: `modules/pipeline_engine.py`
- `PlaybookRunResult.to_dict` (method) `modules/playbook_executor.py:74` `def to_dict(self)`
- `ITTPMapper.resolve` (method) `modules/playbook_executor.py:97` `def resolve(self, technique_id, atomic_test, platform)` -- Return a LazyOwn shell command string or None if unmapped.
- `DefaultTTPMapper.register` (method) `modules/playbook_executor.py:180` `def register(cls, technique_id, platform, command)` -- Add a new technique-to-command mapping.
- `DefaultTTPMapper.resolve` (method) `modules/playbook_executor.py:185` `def resolve(self, technique_id, atomic_test, platform)`
- `PlaybookLoader.__init__` (method) `modules/playbook_executor.py:208` `def __init__(self, playbooks_dir)`
- `PlaybookLoader.list` (method) `modules/playbook_executor.py:211` `def list(self)` -- Return every discoverable playbook name.
- `PlaybookLoader.load` (method) `modules/playbook_executor.py:224` `def load(self, name)` -- Load and validate a playbook by name.
- `PlaybookEngine.__init__` (method) `modules/playbook_executor.py:331` `def __init__(self, loader, mapper, pipelines_dir)`
- `PlaybookEngine.loader` (method) `modules/playbook_executor.py:342` `def loader(self)`
- `PlaybookEngine.analyze` (method) `modules/playbook_executor.py:345` `def analyze(self, name, platform)` -- Analyze a playbook: count techniques, automated vs manual, coverage.
- `PlaybookEngine.generate_pipeline` (method) `modules/playbook_executor.py:370` `def generate_pipeline(self, name, platform)` -- Generate a pipeline YAML file from a playbook.
- `PlaybookEngine.run` (method) `modules/playbook_executor.py:382` `def run(self, name, platform, target, onecmd)` -- Generate and execute a pipeline from a playbook.
- `PlaybookEngine.playbook_list` (method) `modules/playbook_executor.py:407` `def playbook_list()` -- Return a JSON array of available playbooks.
- `PlaybookEngine.playbook_analyze` (method) `modules/playbook_executor.py:413` `def playbook_analyze(name, platform)` -- Return a JSON summary of one playbook.
- `PlaybookEngine.playbook_generate` (method) `modules/playbook_executor.py:420` `def playbook_generate(name, platform)` -- Generate a runnable pipeline from a playbook.
- `PlaybookEngine.playbook_run` (method) `modules/playbook_executor.py:427` `def playbook_run(name, platform, target, onecmd)` -- Analyze, generate, and execute a playbook.

## modules/polymorphic_engine.py
Imported by: `cli/commands/payload_arsenal.py`
- `PolymorphicEngine.__init__` (method) `modules/polymorphic_engine.py:159` `def __init__(self, config)`
- `PolymorphicEngine.mutate` (method) `modules/polymorphic_engine.py:163` `def mutate(self, shellcode, arch)` -- Apply all configured mutation passes to shellcode.
- `PolymorphicEngine.decode_xor` (method) `modules/polymorphic_engine.py:363` `def decode_xor(data)` -- Decode single-byte XOR encrypted shellcode.
- `PolymorphicEngine.decode_multi_xor` (method) `modules/polymorphic_engine.py:379` `def decode_multi_xor(data)` -- Decode multi-byte XOR encrypted shellcode.
- `PolymorphicEngine.generate_decoder_stub` (method) `modules/polymorphic_engine.py:399` `def generate_decoder_stub(self, arch)` -- Generate a self-decrypting stub shellcode template.
- `PolymorphicEngine.get_audit_summary` (method) `modules/polymorphic_engine.py:428` `def get_audit_summary(self)` -- Return a summary of all mutations applied.

## modules/privesc_predictor.py
Depends on: `core/console.py`, `modules/llm_factory.py`
Imported by: `cli/commands/crystal_ball.py`
- `SystemProfile.parse_linpeas_output` (method) `modules/privesc_predictor.py:165` `def parse_linpeas_output(text)` -- Extract a structured SystemProfile from linpeas output text.
- `SystemProfile.parse_winpeas_output` (method) `modules/privesc_predictor.py:232` `def parse_winpeas_output(text)` -- Extract a structured SystemProfile from winpeas output text.
- `SystemProfile.match_known_cves` (method) `modules/privesc_predictor.py:265` `def match_known_cves(profile)` -- Match kernel version against the built-in CVE database.
- `SystemProfile.suid_vectors` (method) `modules/privesc_predictor.py:303` `def suid_vectors(profile)` -- Generate privilege escalation vectors from SUID binaries.
- `SystemProfile.capability_vectors` (method) `modules/privesc_predictor.py:377` `def capability_vectors(profile)` -- Generate privilege escalation vectors from Linux capabilities.
- `SystemProfile.group_vectors` (method) `modules/privesc_predictor.py:479` `def group_vectors(profile)` -- Generate privilege escalation vectors from group memberships.
- `SystemProfile.sudo_vectors` (method) `modules/privesc_predictor.py:517` `def sudo_vectors(profile)` -- Generate privilege escalation vectors from sudo rules.
- `SystemProfile.cron_vectors` (method) `modules/privesc_predictor.py:594` `def cron_vectors(profile)` -- Generate vectors from writable cron jobs and PATH manipulation.
- `SystemProfile.analyze_privesc` (method) `modules/privesc_predictor.py:762` `def analyze_privesc(filepath, text)` -- Main entry point — analyse a system for privilege escalation vectors.
- `SystemProfile.format_crystal_ball_output` (method) `modules/privesc_predictor.py:847` `def format_crystal_ball_output(result)` -- Format the analysis result as a human-readable terminal report.
- `SystemProfile.main` (method) `modules/privesc_predictor.py:926` `def main()` -- CLI entry point for crystal ball privesc analysis.

## modules/professional_report.py
Depends on: `modules/llm_factory.py`
Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `RedTeamReportGenerator.__init__` (method) `modules/professional_report.py:173` `def __init__(self, include_credentials)`
- `RedTeamReportGenerator.collect_data` (method) `modules/professional_report.py:179` `def collect_data(self)` -- Collect all available engagement data from sessions directory.
- `RedTeamReportGenerator.classify_findings` (method) `modules/professional_report.py:219` `def classify_findings(self, data)` -- Classify collected data into structured findings.
- `RedTeamReportGenerator.generate` (method) `modules/professional_report.py:248` `def generate(self, output_dir, output_format, client_name, engagement_type, with_ai, ai_backend)` -- Generate the report in the specified format.
- `RedTeamReportGenerator.collect_command_history` (method) `modules/professional_report.py:832` `def collect_command_history(self, max_entries)` -- Collect operator command history for the engagement timeline.
- `RedTeamReportGenerator.collect_loot_summary` (method) `modules/professional_report.py:856` `def collect_loot_summary(self)` -- Summarize exfiltrated loot without embedding sensitive content.
- `RedTeamReportGenerator.generate_executive_summary` (method) `modules/professional_report.py:902` `def generate_executive_summary(self, data, with_ai, ai_backend)` -- Build the executive summary in business language.

## modules/r.sh
Imported by: `static/js/quill-2.0.3.js::c`, `static/js/quill-2.0.3.js::h`, `static/js/quill-2.0.3.js::i`, `static/js/quill-2.0.3.js::o`, `static/js/quill-2.0.3.js::s`, `static/js/quill-2.0.3.js::u`, `static/js/xterm.js::a`, `static/js/xterm.js::n`, `static/js/xterm.js::o`
- `download_kernel_sources` (function) `modules/r.sh:10` -- Función para descargar y extraer las fuentes del kernel

## modules/reactive_engine.py
Depends on: `core/config.py`, `core/logging.py`, `modules/session_rag.py`
Imported by: `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/toposwarm_autonomous.py`, `tests/test_core_modules.py`, `tests/test_reactive_engine_semantic.py`, `tests/test_reactive_lateral_data.py`
- `AbstractSignalMatcher.match` (method) `modules/reactive_engine.py:97` `def match(self, output, context)`
- `AVBlockedMatcher.match` (method) `modules/reactive_engine.py:125` `def match(self, output, context)`
- `CredentialFoundMatcher.match` (method) `modules/reactive_engine.py:157` `def match(self, output, context)`
- `PrivescHintMatcher.match` (method) `modules/reactive_engine.py:188` `def match(self, output, context)`
- `NewHostMatcher.match` (method) `modules/reactive_engine.py:210` `def match(self, output, context)`
- `ServiceVersionMatcher.match` (method) `modules/reactive_engine.py:241` `def match(self, output, context)`
- `ShellErrorMatcher.match` (method) `modules/reactive_engine.py:268` `def match(self, output, context)`
- `LateralOpportunityMatcher.match` (method) `modules/reactive_engine.py:297` `def match(self, output, context)`
- `DataOfInterestMatcher.match` (method) `modules/reactive_engine.py:337` `def match(self, output, context)`
- `ParquetAdvisor.__init__` (method) `modules/reactive_engine.py:376` `def __init__(self, root)`
- `ParquetAdvisor.gtfobins_for` (method) `modules/reactive_engine.py:401` `def gtfobins_for(self, binary)`
- `ParquetAdvisor.lolbas_for` (method) `modules/reactive_engine.py:414` `def lolbas_for(self, binary)` -- Returns [(function_name, att&ck_technique), ...].
- `ParquetAdvisor.technique_commands_for` (method) `modules/reactive_engine.py:428` `def technique_commands_for(self, platform, keyword)` -- Return atomic test commands for platform matching keyword.
- `EvasionAdvisor.suggest` (method) `modules/reactive_engine.py:484` `def suggest(self, signals, platform)`
- `PrivescAdvisor.suggest` (method) `modules/reactive_engine.py:545` `def suggest(self, signals, platform, parquet)`
- `SemanticContextAdvisor.__init__` (method) `modules/reactive_engine.py:618` `def __init__(self, rag, config_loader, min_score, query_limit)` -- Initialise the advisor.
- `SemanticContextAdvisor.suggest` (method) `modules/reactive_engine.py:708` `def suggest(self, output, command, platform, context)` -- Return semantic next-step hints derived from past sessions.
- `ReactiveEngine.__init__` (method) `modules/reactive_engine.py:789` `def __init__(self, matchers, evasion, privesc, parquet, semantic)`
- `ReactiveEngine.analyse` (method) `modules/reactive_engine.py:814` `def analyse(self, output, command, platform, context)` -- Parse *output* and return prioritised ReactiveDecisions.
- `ReactiveEngine.top_decision` (method) `modules/reactive_engine.py:926` `def top_decision(self, output, command, platform, context)` -- Return only the single highest-priority decision, or None.
- `ReactiveEngine.get_engine` (method) `modules/reactive_engine.py:945` `def get_engine()`

## modules/recommender.py
Depends on: `modules/ai_fallback.py`, `modules/session_state.py`
Imported by: `skills/lazyown_mcp.py`
- `recommend` (function) `modules/recommender.py:141` `def recommend(state, api_key)` -- Return ranked recommendations without writing to disk.
- `recommend_and_save` (function) `modules/recommender.py:159` `def recommend_and_save(api_key)` -- Build state → call Groq → write JSON → return recommendations.

## modules/redteam_gym.py
Depends on: `cli/engagement_hooks.py`, `modules/cli_auth.py`
Imported by: `cli/commands/redteam_gym.py`, `modules/exploitgym_gym.py`, `tests/test_infra_disposable.py`
- `GymAttempt.list_challenges` (method) `modules/redteam_gym.py:357` `def list_challenges()` -- Return all defined gym challenges with metadata.
- `GymAttempt.start_challenge` (method) `modules/redteam_gym.py:378` `def start_challenge(challenge_id)` -- Begin a gym challenge and track start time.
- `GymAttempt.submit_challenge` (method) `modules/redteam_gym.py:448` `def submit_challenge(techniques_used, success)` -- Submit a completed challenge for scoring.
- `GymAttempt.show_leaderboard` (method) `modules/redteam_gym.py:679` `def show_leaderboard(top_n)` -- Return the top N players from the leaderboard.
- `GymAttempt.get_active_challenge` (method) `modules/redteam_gym.py:706` `def get_active_challenge()` -- Return the currently active challenge for this operator, if any.
- `GymAttempt.record_external_attempt` (method) `modules/redteam_gym.py:736` `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` -- Record a scored attempt for a challenge not defined in the catalog.
- `GymAttempt.main` (method) `modules/redteam_gym.py:790` `def main()` -- CLI entry point — show gym leaderboard from command line.

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
- `ReflectiveLoader.__init__` (method) `modules/reflective_dll.py:486` `def __init__(self, pe_data, config)`
- `ReflectiveLoader.sha256` (method) `modules/reflective_dll.py:503` `def sha256(self)` -- SHA-256 hash of the raw PE bytes.
- `ReflectiveLoader.architecture` (method) `modules/reflective_dll.py:508` `def architecture(self)` -- CPU architecture string ('x64' or 'x86').
- `ReflectiveLoader.required_imports` (method) `modules/reflective_dll.py:513` `def required_imports(self)` -- DLL names needed for import resolution.
- `ReflectiveLoader.plan_injection` (method) `modules/reflective_dll.py:524` `def plan_injection(self)` -- Generate an injection plan based on the configured technique.
- `ReflectiveLoader.generate_c_stub` (method) `modules/reflective_dll.py:586` `def generate_c_stub(self)` -- Generate a C stub that implements reflective loading.
- `ReflectiveLoader.generate_powershell_stub` (method) `modules/reflective_dll.py:664` `def generate_powershell_stub(self)` -- Generate PowerShell reflective loader script.
- `ReflectiveLoader.summarize` (method) `modules/reflective_dll.py:683` `def summarize(self)` -- Human-readable summary of the parsed PE for operator review.

## modules/resource_script.py
Depends on: `core/safe_exec.py`
Imported by: `cli/commands/resource_scripting.py`, `tests/test_resource_script.py`, `tests/test_security_hardening_v3.py`
- `ScriptContext.__init__` (method) `modules/resource_script.py:88` `def __init__(self, shell_params, on_command, on_print)`
- `ScriptContext.print` (method) `modules/resource_script.py:136` `def print(self, msg)`
- `ScriptContext.run_command` (method) `modules/resource_script.py:145` `def run_command(self, cmd)`
- `ScriptContext.eval_condition` (method) `modules/resource_script.py:189` `def eval_condition(self, raw_condition)` -- Evaluate an ``if``/``while`` condition expression.
- `ResourceScriptEngine.__init__` (method) `modules/resource_script.py:274` `def __init__(self, context)`
- `ResourceScriptEngine.execute` (method) `modules/resource_script.py:277` `def execute(self, script_path)` -- Load and run a script file.
- `ResourceScriptEngine.execute_lines` (method) `modules/resource_script.py:291` `def execute_lines(self, lines, source)` -- Execute a list of script lines.
- `ResourceScriptEngine.execute_string` (method) `modules/resource_script.py:329` `def execute_string(self, script)` -- Execute a script string (split on newlines).

## modules/reverse-shell.c
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
- `RichDashboard.stop` (method) `modules/rich_tui.py:134` `def stop(self)` -- Gracefully shut down the dashboard and restore terminal state.

## modules/rl_trainer.py
Depends on: `core/logging.py`
Imported by: `modules/lesson_ingestor.py`, `skills/autonomous_daemon.py`, `skills/swan_agent.py`, `tests/test_moe_rl_swan.py`
- `IStateEncoder.encode` (method) `modules/rl_trainer.py:104` `def encode(self, task_type, engagement_phase, recent_reward_ema)` -- Return a string key representing the current state.
- `BucketedStateEncoder.encode` (method) `modules/rl_trainer.py:130` `def encode(self, task_type, engagement_phase, recent_reward_ema)`
- `QValueStore.__init__` (method) `modules/rl_trainer.py:155` `def __init__(self, path, optimistic_init)`
- `QValueStore.get` (method) `modules/rl_trainer.py:167` `def get(self, state, action)`
- `QValueStore.set` (method) `modules/rl_trainer.py:171` `def set(self, state, action, value)`
- `QValueStore.max_q` (method) `modules/rl_trainer.py:175` `def max_q(self, state, candidates)` -- Return max Q(state, a) over the given candidate actions.
- `QValueStore.argmax` (method) `modules/rl_trainer.py:181` `def argmax(self, state, candidates)` -- Return the action with highest Q(state, a).
- `QValueStore.save` (method) `modules/rl_trainer.py:187` `def save(self)`
- `EpsilonTracker.__init__` (method) `modules/rl_trainer.py:217` `def __init__(self, start, minimum, decay, path)`
- `EpsilonTracker.epsilon` (method) `modules/rl_trainer.py:232` `def epsilon(self)`
- `EpsilonTracker.step` (method) `modules/rl_trainer.py:235` `def step(self)` -- Apply one decay step and persist.
- `RLTrainer.__init__` (method) `modules/rl_trainer.py:283` `def __init__(self, config, state_encoder, q_store, epsilon_tracker)`
- `RLTrainer.encode_state` (method) `modules/rl_trainer.py:303` `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` -- Convert environment observations into a discrete state key.
- `RLTrainer.select_action` (method) `modules/rl_trainer.py:312` `def select_action(self, state, candidates, force_exploit)` -- Epsilon-greedy expert selection.
- `RLTrainer.update` (method) `modules/rl_trainer.py:346` `def update(self, state, action, reward, next_state, candidates, detection_prob)` -- Apply one Q-learning update.
- `RLTrainer.best_expert_for_state` (method) `modules/rl_trainer.py:387` `def best_expert_for_state(self, state, candidates)` -- Return the highest Q-value expert for the given state (greedy).
- `RLTrainer.q_values_for_state` (method) `modules/rl_trainer.py:391` `def q_values_for_state(self, state, candidates)` -- Return {expert_id: q_value} for diagnostics.
- `RLTrainer.save` (method) `modules/rl_trainer.py:395` `def save(self)` -- Persist Q-table to disk.
- `RLTrainer.epsilon` (method) `modules/rl_trainer.py:400` `def epsilon(self)`
- `RLTrainer.get_trainer` (method) `modules/rl_trainer.py:423` `def get_trainer(config)` -- Return (or create) the module-level singleton RLTrainer.

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
- `load_hidden_pids` (function) `modules/rootkit/mrhyde.c:73` `void load_hidden_pids()`
- `load_hidden_files` (function) `modules/rootkit/mrhyde.c:93` `void load_hidden_files()`
- `unlink` (function) `modules/rootkit/mrhyde.c:113` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde.c:125` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde.c:145` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde.c:157` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde.c:178` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde.c:197` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde.c:212` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde.c:222` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde.c:283` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde.c:327` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde.c:371` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde.c:415` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde.c:459` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde.c:503` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde.c:557` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde.c:618` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde.c:678` `int main()`

## modules/rootkit/mrhyde2.c
- `load_hidden_pids` (function) `modules/rootkit/mrhyde2.c:63` `void load_hidden_pids()`
- `unlink` (function) `modules/rootkit/mrhyde2.c:83` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde2.c:95` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde2.c:115` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde2.c:127` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde2.c:148` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde2.c:167` `int should_hide_pid(const char* pid)`
- `readdir` (function) `modules/rootkit/mrhyde2.c:182` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde2.c:238` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde2.c:275` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde2.c:312` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde2.c:349` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde2.c:386` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde2.c:423` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde2.c:470` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde2.c:527` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde2.c:583` `int main()`

## modules/rootkit/mrhyde3.c
- `uring_queue_init` (function) `modules/rootkit/mrhyde3.c:85` `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` -- /* Syscalls static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p) { return...
- `uring_get_sqe` (function) `modules/rootkit/mrhyde3.c:130` `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` -- ring->cq.head = (unsigned *)((char *)cq_ring + params.cq_off.head); ring->cq.tail = (unsigned *)((char *)cq_ring +...
- `uring_submit` (function) `modules/rootkit/mrhyde3.c:141` `static int uring_submit(struct io_uring *ring)` -- } /* Obtener SQE static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring) { unsigned head = *ring->sq.head...
- `uring_wait_cqe_timeout` (function) `modules/rootkit/mrhyde3.c:149` `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` -- struct io_uring_sqe *sqe = &ring->sq.sqes[tail & *ring->sq.ring_mask]; memset(sqe, 0, sizeof(*sqe)); return sqe; }...
- `uring_cqe_seen` (function) `modules/rootkit/mrhyde3.c:163` `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)`
- `init_root_ring` (function) `modules/rootkit/mrhyde3.c:176` `static int init_root_ring(void)` -- static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe) { (*ring->cq.head)++; } /* Estado global...
- `uring_read_whole_file` (function) `modules/rootkit/mrhyde3.c:197` `static char *uring_read_whole_file(const char *path)` -- } ring_ok = 1; /* Registrar buffer (opcional) struct iovec iov; iov.iov_base = malloc(IO_URING_BUFFER_SIZE)...
- `traditional_read_file` (function) `modules/rootkit/mrhyde3.c:253` `static char *traditional_read_file(const char *path)` -- if (bytes_read <= 0) break; buf = realloc(buf, total_read + bytes_read + 1); if (!buf) { close(fd)...
- `load_hidden_pids` (function) `modules/rootkit/mrhyde3.c:268` `void load_hidden_pids(void)` -- FILE *f = fopen(path, "rb"); if (!f) return NULL; fseek(f, 0, SEEK_END); long size = ftell(f); fseek(f, 0...
- `load_hidden_files` (function) `modules/rootkit/mrhyde3.c:282` `void load_hidden_files(void)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde3.c:297` `char* get_username_from_pid(pid_t pid)` -- char *data = uring_read_whole_file(FILE_HIDE_PATH); if (!data) data = traditional_read_file(FILE_HIDE_PATH); if...
- `should_hide_pid` (function) `modules/rootkit/mrhyde3.c:320` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde3.c:329` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde3.c:336` `struct dirent* readdir(DIR* dirp)`
- `unlink` (function) `modules/rootkit/mrhyde3.c:367` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde3.c:373` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde3.c:383` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde3.c:389` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `fopen` (function) `modules/rootkit/mrhyde3.c:407` `FILE *fopen(const char *pathname, const char *mode)`
- `open` (function) `modules/rootkit/mrhyde3.c:430` `int open(const char *pathname, int flags, ...)`
- `openat` (function) `modules/rootkit/mrhyde3.c:458` `int openat(int dirfd, const char *pathname, int flags, ...)`
- `stat` (function) `modules/rootkit/mrhyde3.c:487` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde3.c:511` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde3.c:535` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde3.c:569` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde3.c:605` `ssize_t getdents64(int fd, void *dirp, size_t count)`

## modules/rootkit/rootkit.c
Depends on: `core/crypto.py`, `lazyown-docker/init.sh`
- `regs_override_return` (function) `modules/rootkit/rootkit.c:43` `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` -- Define regs_override_return function
- `hooked_getdents` (function) `modules/rootkit/rootkit.c:75` `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents function
- `hooked_getdents64` (function) `modules/rootkit/rootkit.c:101` `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents64 function
- `hooked_read` (function) `modules/rootkit/rootkit.c:127` `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked read function to create a backdoor
- `disable_module_signature_verification` (function) `modules/rootkit/rootkit.c:181` `static void disable_module_signature_verification(void)` -- Function to disable module signature verification
- `hook_syscalls` (function) `modules/rootkit/rootkit.c:195` `static int __init hook_syscalls(void)` -- Function to hook system calls
- `unhook_syscalls` (function) `modules/rootkit/rootkit.c:208` `static void __exit unhook_syscalls(void)` -- Function to unhook system calls

## modules/saas_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `SaaSEnumerationTools.microsoft365_commands` (method) `modules/saas_attacks.py:74` `def microsoft365_commands()`
- `SaaSEnumerationTools.google_workspace_commands` (method) `modules/saas_attacks.py:99` `def google_workspace_commands()`
- `SaaSEnumerationTools.salesforce_commands` (method) `modules/saas_attacks.py:117` `def salesforce_commands()`
- `SaaSEnumerationTools.servicenow_commands` (method) `modules/saas_attacks.py:134` `def servicenow_commands()`
- `SaaSAttackEngine.__init__` (method) `modules/saas_attacks.py:162` `def __init__(self, config)`
- `SaaSAttackEngine.enumerate_all` (method) `modules/saas_attacks.py:165` `def enumerate_all(self)` -- Generate enumeration commands for all supported SaaS platforms.
- `SaaSAttackEngine.m365_ews_mail_search` (method) `modules/saas_attacks.py:178` `def m365_ews_mail_search(self, search_term)` -- Search mailboxes via Exchange Web Services (EWS).
- `SaaSAttackEngine.google_workspace_domain_wide_delegation` (method) `modules/saas_attacks.py:227` `def google_workspace_domain_wide_delegation(self)` -- Abuse Google Workspace Domain-Wide Delegation (DWD).
- `SaaSAttackEngine.salesforce_report_mining` (method) `modules/saas_attacks.py:256` `def salesforce_report_mining(self)` -- Mine Salesforce reports and dashboards for sensitive data.
- `SaaSAttackEngine.slack_data_mining` (method) `modules/saas_attacks.py:285` `def slack_data_mining(self)` -- Mine Slack Enterprise for sensitive conversations and files.
- `SaaSAttackEngine.detect_external_sharing` (method) `modules/saas_attacks.py:311` `def detect_external_sharing(self)` -- Detect external sharing configurations across SaaS platforms.
- `SaaSAttackEngine.summary` (method) `modules/saas_attacks.py:336` `def summary(self)`

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
- `OutputSanitizer.build_default_config` (method) `modules/security_sanitizers.py:477` `def build_default_config(payload)` -- Return a :class:`SecurityConfig` populated from ``payload``.

## modules/session_cleanup.py
Imported by: `lazyown.py`, `tests/test_infra_disposable.py`
- `find_cloudflared_pids` (function) `modules/session_cleanup.py:28` `def find_cloudflared_pids(ps_output)` -- Extract PIDs of ``cloudflared tunnel`` processes from ps output.
- `stop_cloudflared_processes` (function) `modules/session_cleanup.py:94` `def stop_cloudflared_processes()` -- Terminate stray ``cloudflared tunnel`` host processes.
- `cleanup_ephemeral_infra` (function) `modules/session_cleanup.py:122` `def cleanup_ephemeral_infra()` -- Stop all disposable infrastructure owned by this checkout.

## modules/session_rag.py
Depends on: `core/logging.py`
Imported by: `cli/commands/mcp_bridge.py`, `modules/reactive_engine.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`
- `_KeywordFallback.__init__` (method) `modules/session_rag.py:104` `def __init__(self)`
- `_KeywordFallback.load` (method) `modules/session_rag.py:108` `def load(self, path)` -- Load index from disk (no-op if file absent or corrupt).
- `_KeywordFallback.save` (method) `modules/session_rag.py:119` `def save(self, path)` -- Atomically persist index to disk.
- `_KeywordFallback.add` (method) `modules/session_rag.py:129` `def add(self, doc_id, text, meta)`
- `_KeywordFallback.query` (method) `modules/session_rag.py:139` `def query(self, query_text, n)`
- `_KeywordFallback.count` (method) `modules/session_rag.py:149` `def count(self)`
- `_KeywordFallback.reset` (method) `modules/session_rag.py:152` `def reset(self)`
- `_RagState.load` (method) `modules/session_rag.py:165` `def load(cls)`
- `_RagState.save` (method) `modules/session_rag.py:174` `def save(self)`
- `SessionRAG.__init__` (method) `modules/session_rag.py:184` `def __init__(self)`
- `SessionRAG.index_new` (method) `modules/session_rag.py:296` `def index_new(self)` -- Incrementally index only new or changed files.
- `SessionRAG.index_parquet_sources` (method) `modules/session_rag.py:317` `def index_parquet_sources(self, force)` -- Index knowledge-base parquets (techniques_enriched, binarios, lolbas_index) into the RAG store.
- `SessionRAG.index_all` (method) `modules/session_rag.py:406` `def index_all(self)` -- Full re-index from scratch.
- `SessionRAG.query` (method) `modules/session_rag.py:434` `def query(self, query_text, n, collection)` -- Return top-n relevant chunks as dicts with keys: text, source, chunk, score.
- `SessionRAG.context_for_step` (method) `modules/session_rag.py:482` `def context_for_step(self, phase, target, cmd, n)` -- Return a compact RAG context string suitable for injection into an LLM prompt.
- `SessionRAG.stats` (method) `modules/session_rag.py:502` `def stats(self)`
- `SessionRAG.get_rag` (method) `modules/session_rag.py:528` `def get_rag()`

## modules/session_reader.py
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ImplantRecord.is_privileged` (method) `modules/session_reader.py:52` `def is_privileged(self)`
- `ImplantRecord.platform` (method) `modules/session_reader.py:57` `def platform(self)`
- `ImplantRecord.ip_list` (method) `modules/session_reader.py:66` `def ip_list(self)`
- `SessionSummary.active_client_ids` (method) `modules/session_reader.py:89` `def active_client_ids(self)`
- `SessionSummary.privileged_sessions` (method) `modules/session_reader.py:96` `def privileged_sessions(self)`
- `SessionSummary.unprivileged_sessions` (method) `modules/session_reader.py:103` `def unprivileged_sessions(self)`
- `SessionSummary.latest_for` (method) `modules/session_reader.py:109` `def latest_for(self, client_id)`
- `SessionSummary.task_by_status` (method) `modules/session_reader.py:113` `def task_by_status(self, status)`
- `AbstractReader.read` (method) `modules/session_reader.py:124` `def read(self, sessions_dir)`
- `ImplantCSVReader.read` (method) `modules/session_reader.py:143` `def read(self, sessions_dir)`
- `CommandOutputReader.read` (method) `modules/session_reader.py:183` `def read(self, sessions_dir)`
- `DiscoveredHostReader.read` (method) `modules/session_reader.py:201` `def read(self, sessions_dir)`
- `TaskReader.read` (method) `modules/session_reader.py:219` `def read(self, sessions_dir)`
- `TaskWriter.__init__` (method) `modules/session_reader.py:242` `def __init__(self, sessions_dir)`
- `TaskWriter.append` (method) `modules/session_reader.py:245` `def append(self, title, description, operator, status)`
- `TaskWriter.update_status` (method) `modules/session_reader.py:264` `def update_status(self, task_id, status)`
- `SessionAggregator.__init__` (method) `modules/session_reader.py:295` `def __init__(self, implant_reader, output_reader, host_reader, task_reader)`
- `SessionAggregator.aggregate` (method) `modules/session_reader.py:307` `def aggregate(self, sessions_dir)`
- `SessionAggregator.get_aggregator` (method) `modules/session_reader.py:323` `def get_aggregator()`

## modules/session_state.py
Imported by: `modules/recommender.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `build_state` (function) `modules/session_state.py:173` `def build_state()` -- Assemble and return the current session state dict.
- `refresh` (function) `modules/session_state.py:223` `def refresh()` -- Build state and persist to sessions/session_state.json.
- `load` (function) `modules/session_state.py:234` `def load()` -- Return the last written state, or build it fresh if stale/missing.

## modules/sleep_obfuscation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/sleep_obfuscation.py`, `modules/beacon_config_builder.py`, `tests/test_sleep_obfuscation.py`
- `SleepObfuscationConfig.to_dict` (method) `modules/sleep_obfuscation.py:129` `def to_dict(self)` -- Serialize to dictionary.
- `SleepObfuscationConfig.from_dict` (method) `modules/sleep_obfuscation.py:146` `def from_dict(cls, raw)` -- Build from dictionary.
- `SleepTechniqueCatalog.__init__` (method) `modules/sleep_obfuscation.py:170` `def __init__(self)`
- `SleepTechniqueCatalog.register` (method) `modules/sleep_obfuscation.py:173` `def register(self, technique)` -- Register a technique in the catalog.
- `SleepTechniqueCatalog.get` (method) `modules/sleep_obfuscation.py:177` `def get(self, name)` -- Retrieve a technique by name.
- `SleepTechniqueCatalog.list_all` (method) `modules/sleep_obfuscation.py:186` `def list_all(self)` -- Return all registered techniques sorted by detection resistance.
- `SleepTechniqueCatalog.list_by_platform` (method) `modules/sleep_obfuscation.py:194` `def list_by_platform(self, platform)` -- Return techniques supported on a given platform.
- `SleepTechniqueCatalog.list_names` (method) `modules/sleep_obfuscation.py:201` `def list_names(self)` -- Return sorted list of technique names.
- `SleepTechniqueValidator.validate` (method) `modules/sleep_obfuscation.py:371` `def validate(config, technique)` -- Validate config against a technique definition.
- `SleepTechniqueValidator.validate_config` (method) `modules/sleep_obfuscation.py:392` `def validate_config(config)` -- Validate the config itself for internal consistency.
- `SleepObfuscationEngine.__init__` (method) `modules/sleep_obfuscation.py:413` `def __init__(self, catalog)`
- `SleepObfuscationEngine.catalog` (method) `modules/sleep_obfuscation.py:422` `def catalog(self)` -- Return the technique catalog.
- `SleepObfuscationEngine.config` (method) `modules/sleep_obfuscation.py:427` `def config(self)` -- Return the active runtime configuration.
- `SleepObfuscationEngine.detection_resistance` (method) `modules/sleep_obfuscation.py:432` `def detection_resistance(self)` -- Return the detection resistance score of the active technique.
- `SleepObfuscationEngine.select` (method) `modules/sleep_obfuscation.py:448` `def select(self, technique_name)` -- Select a technique from the catalog.
- `SleepObfuscationEngine.configure` (method) `modules/sleep_obfuscation.py:455` `def configure(self, technique, overrides)` -- Build a validated SleepObfuscationConfig for a technique.
- `SleepObfuscationEngine.validate` (method) `modules/sleep_obfuscation.py:490` `def validate(self, config)` -- Validate configuration against the active technique.
- `SleepObfuscationEngine.recommend` (method) `modules/sleep_obfuscation.py:506` `def recommend(self, platform)` -- Recommend techniques for a platform sorted by detection resistance.
- `SleepObfuscationEngine.to_dict` (method) `modules/sleep_obfuscation.py:519` `def to_dict(self)` -- Serialize the entire engine state to a dictionary.
- `SleepObfuscationEngine.from_dict` (method) `modules/sleep_obfuscation.py:528` `def from_dict(cls, raw)` -- Build an engine from a serialized state dictionary.


Next: [API_p14.md](API_p14.md)
