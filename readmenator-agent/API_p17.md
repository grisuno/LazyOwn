# API (page 17 of 25)
Previous: [API_p16.md](API_p16.md)

## modules/orchestrator_config.py
Depends on: `core/config.py`, `core/logging.py`, `modules/auto_registry.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyops.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/auto_registry.py`, `modules/defense_stages.py`, `modules/harness.py`, `modules/lazy_loop.py`, `modules/llm_orchestrator.py`, `modules/loop_ai_bridge.py`, `modules/trigger_policy.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_harness_mode.py`, `tests/test_lazy_orchestrator.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_yaml.py`, `tests/test_outcome_bus.py`
- `reload` (function) `modules/orchestrator_config.py:113` `def reload()` -- Invalidate every merged view after an external configuration change.
- `profiles` (function) `modules/orchestrator_config.py:232` `def profiles()` -- Return every resolved profile, including inherited values.
- `active_profile` (function) `modules/orchestrator_config.py:257` `def active_profile()` -- Return the profile selected by the payload, falling back safely.
- `profile_config` (function) `modules/orchestrator_config.py:269` `def profile_config(name)` -- Return one resolved profile by name, or the active profile.
- `set_profile` (function) `modules/orchestrator_config.py:276` `def set_profile(name)` -- Persist the active profile name.
- `set_harness` (function) `modules/orchestrator_config.py:300` `def set_harness(enabled)` -- Persist the deterministic-harness toggle in the payload.
- `limits` (function) `modules/orchestrator_config.py:332` `def limits()` -- Return resolved numeric limits for the active profile.
- `budget` (function) `modules/orchestrator_config.py:339` `def budget()` -- Return resolved budgets for the active profile.
- `chain_defaults` (function) `modules/orchestrator_config.py:346` `def chain_defaults()` -- Return the default chain and playbook for the active profile.
- `sinks` (function) `modules/orchestrator_config.py:355` `def sinks()` -- Return outcome sink toggles for the active profile plus payload overrides.
- `stages` (function) `modules/orchestrator_config.py:366` `def stages()` -- Merged stage view: enabled flag, label, firing condition and params.
- `stage_enabled` (function) `modules/orchestrator_config.py:396` `def stage_enabled(name)` -- Return whether one pipeline stage is enabled (unknown = enabled).
- `stage_params` (function) `modules/orchestrator_config.py:402` `def stage_params(name)` -- Return the resolved parameter mapping of one stage.
- `set_stage` (function) `modules/orchestrator_config.py:407` `def set_stage(name, enabled)` -- Persist the enabled flag of one stage.
- `effective_verbs` (function) `modules/orchestrator_config.py:432` `def effective_verbs()` -- Merged auto-verb view: built-ins plus operator overrides, additions and catalog.
- `verb_config` (function) `modules/orchestrator_config.py:524` `def verb_config(name)` -- Return the merged configuration of one auto verb, or None.
- `verb_enabled` (function) `modules/orchestrator_config.py:533` `def verb_enabled(name)` -- Return whether one auto verb may be proposed or executed.
- `upsert_verb` (function) `modules/orchestrator_config.py:539` `def upsert_verb(name)` -- Create or update one auto-verb override in the payload.
- `remove_verb` (function) `modules/orchestrator_config.py:596` `def remove_verb(name)` -- Remove a custom verb, or disable a built-in one.
- `reset` (function) `modules/orchestrator_config.py:617` `def reset()` -- Drop every orchestrator override (back to YAML defaults).
- `validate_config` (function) `modules/orchestrator_config.py:624` `def validate_config(data)` -- Validate one raw orchestration mapping.

## modules/osint_enrich.py
Imported by: `modules/finding_lifecycle.py`, `tests/test_finding_lifecycle.py`
- `cve_lookup` (function) `modules/osint_enrich.py:122` `def cve_lookup(cve_id, sessions_dir)` -- Assemble OSV advisory + KEV flag + EPSS score for one CVE id.
- `reverse_dns` (function) `modules/osint_enrich.py:161` `def reverse_dns(ip, sessions_dir)` -- Best-effort PTR hostname for an IP (HackerTarget, then DoH).
- `host_geo` (function) `modules/osint_enrich.py:183` `def host_geo(ip, sessions_dir)` -- Country/org/ISP for an IP via the keyless ip-api endpoint.
- `domain_exposure` (function) `modules/osint_enrich.py:198` `def domain_exposure(domain, sessions_dir)` -- Count public urlscan.io results for a domain (no key needed).
- `enrich_evidence` (function) `modules/osint_enrich.py:213` `def enrich_evidence(items, sessions_dir)` -- Append keyless OSINT verdicts to CVE mentions inside evidence items.

## modules/outcome_bus.py
Depends on: `core/logging.py`, `modules/__init__.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/atomic_exploit_bridge.py`, `modules/autonomous_exploit_engine.py`, `modules/beacon_recon.py`, `modules/ctf_capture.py`, `modules/emulation_runner.py`, `modules/exploit_chain.py`, `modules/lazy_loop.py`, `modules/redteam_gym.py`, `modules/sinks/attack_graph.py`, `modules/sinks/beacon_dispatch.py`, `modules/sinks/c2_surfaces.py`, `modules/sinks/campaign_db.py`, `modules/sinks/event_bus.py`, `modules/sinks/intel_graph.py`, `modules/sinks/killchain.py`, `modules/sinks/objectives.py`, `modules/sinks/routing.py`, `modules/sinks/world_diff.py`, `modules/sinks/world_model.py`, `tests/test_beacon_recon_sink.py`, `tests/test_gym_cli.py`, `tests/test_gym_lifecycle.py`, `tests/test_gym_registry.py`, `tests/test_lazy_orchestrator.py`, `tests/test_outcome_bus.py`
- `OutcomeEvent.host_value` (method) `modules/outcome_bus.py:103` `def host_value(self)` -- Return the best host identifier available.
- `OutcomeEvent.key` (method) `modules/outcome_bus.py:107` `def key(self)` -- Return the idempotency key for this event.
- `OutcomeEvent.to_dict` (method) `modules/outcome_bus.py:125` `def to_dict(self)` -- Return a JSON-serializable view.
- `OutcomeBus.__init__` (method) `modules/outcome_bus.py:156` `def __init__(self, ledger_path, sink_map)` -- Bind the audit ledger and an optional sink map for tests.
- `OutcomeBus.reset` (method) `modules/outcome_bus.py:169` `def reset(self)` -- Clear the in-process dedupe cache.
- `OutcomeBus.record` (method) `modules/outcome_bus.py:201` `def record(self, event, sinks)` -- Publish one event to every enabled sink.
- `get_bus` (function) `modules/outcome_bus.py:269` `def get_bus()` -- Return the process-wide outcome bus.
- `reset_bus` (function) `modules/outcome_bus.py:278` `def reset_bus()` -- Reset the process-wide bus cache (tests and long-lived operators).
- `record` (function) `modules/outcome_bus.py:283` `def record(event, sinks)` -- Publish one event through the process-wide bus.
- `record_event` (function) `modules/outcome_bus.py:288` `def record_event()` -- Build and publish one event from keyword fields.
- `severity_for_event` (function) `modules/outcome_bus.py:293` `def severity_for_event(severity)` -- Map an outcome severity to the event-bus severity vocabulary.
- `category_for_event` (function) `modules/outcome_bus.py:298` `def category_for_event(kind)` -- Map an outcome kind to the event-bus category vocabulary.

## modules/payload_factory.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/payload_generation.py`, `cli/commands/session_ops.py`, `lazyown.py`, `modules/sinks/beacon_dispatch.py`, `scripts/devtools/core_smoke.py`, `tests/test_payload_factory.py`
- `PayloadTemplate.__init__` (method) `modules/payload_factory.py:222` `def __init__(self, name, platform, arch, description, options)`
- `PayloadTemplate.generate` (method) `modules/payload_factory.py:237` `def generate(self)` -- Generate the raw payload bytes.
- `PayloadTemplate.to_dict` (method) `modules/payload_factory.py:241` `def to_dict(self)`
- `ReverseShellPayload.__init__` (method) `modules/payload_factory.py:254` `def __init__(self)`
- `ReverseShellPayload.generate` (method) `modules/payload_factory.py:272` `def generate(self)`
- `WindowsReverseShellPayload.__init__` (method) `modules/payload_factory.py:293` `def __init__(self)`
- `WindowsReverseShellPayload.generate` (method) `modules/payload_factory.py:305` `def generate(self)`
- `MsfvenomPayload.__init__` (method) `modules/payload_factory.py:325` `def __init__(self, name, platform, arch)`
- `MsfvenomPayload.generate` (method) `modules/payload_factory.py:337` `def generate(self)`
- `ShellcodePayload.__init__` (method) `modules/payload_factory.py:374` `def __init__(self, name, platform, arch, description, escaped_hex, patcher)`
- `ShellcodePayload.generate` (method) `modules/payload_factory.py:397` `def generate(self)` -- Return the shellcode, optionally patching LHOST / LPORT.
- `DynamicShellcodePayload.__init__` (method) `modules/payload_factory.py:416` `def __init__(self, name, platform, arch, description, builder)`
- `DynamicShellcodePayload.generate` (method) `modules/payload_factory.py:436` `def generate(self)`
- `PayloadFactory.__init__` (method) `modules/payload_factory.py:464` `def __init__(self)`
- `PayloadFactory.register` (method) `modules/payload_factory.py:512` `def register(self, template)` -- Register a custom payload template.
- `PayloadFactory.list` (method) `modules/payload_factory.py:516` `def list(self, platform)` -- List all registered payloads, optionally filtered by platform.
- `PayloadFactory.get` (method) `modules/payload_factory.py:525` `def get(self, name)` -- Get a payload template by name.
- `PayloadFactory.generate` (method) `modules/payload_factory.py:529` `def generate(self, name, format, output)` -- Generate a payload by name.
- `PayloadFactory.list_formats` (method) `modules/payload_factory.py:664` `def list_formats()` -- List all available output formats.
- `format_payload_table` (function) `modules/payload_factory.py:672` `def format_payload_table(payloads)` -- Format a list of payload dicts as an aligned table.

## modules/phishing_orchestrator.py
Depends on: `core/crypto.py`, `core/hardening.py`
Imported by: `cli/commands/phishing_wizard.py`, `modules/lazypoophish.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `PhishingOrchestrator.__init__` (method) `modules/phishing_orchestrator.py:399` `def __init__(self)`
- `PhishingOrchestrator.get_instance` (method) `modules/phishing_orchestrator.py:404` `def get_instance(cls)`
- `PhishingOrchestrator.launch` (method) `modules/phishing_orchestrator.py:415` `def launch(self, target_domain, template, mode, targets_file, sender_email, sender_password, smtp_host, smtp_port)` -- Launch a phishing campaign.
- `PhishingOrchestrator.profile_targets` (method) `modules/phishing_orchestrator.py:524` `def profile_targets(self, domain)` -- Profile targets for a domain using OSINT techniques.
- `PhishingOrchestrator.generate_template` (method) `modules/phishing_orchestrator.py:569` `def generate_template(self, name, target_domain, context)` -- Generate or retrieve a phishing template.
- `PhishingOrchestrator.clone_landing_page` (method) `modules/phishing_orchestrator.py:616` `def clone_landing_page(self, url)` -- Clone a target login page for credential harvesting.
- `PhishingOrchestrator.get_results` (method) `modules/phishing_orchestrator.py:643` `def get_results(self, campaign_id)` -- Get campaign results.
- `PhishingOrchestrator.record_click` (method) `modules/phishing_orchestrator.py:667` `def record_click(self, campaign_id, email)` -- Record a link click.
- `PhishingOrchestrator.record_credentials` (method) `modules/phishing_orchestrator.py:688` `def record_credentials(self, campaign_id, email, password)` -- Record harvested credentials.

## modules/pipeline_engine.py
Depends on: `core/logging.py`, `modules/engagement_hooks.py`, `skills/autonomous_daemon.py`
Imported by: `cli/commands/session_ops.py`, `modules/playbook_executor.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_pipeline_engine.py`
- `StepResult.to_context` (method) `modules/pipeline_engine.py:180` `def to_context(self)` -- Render the step result as a dict for template lookups.
- `PipelineRun.to_dict` (method) `modules/pipeline_engine.py:213` `def to_dict(self)` -- Return a JSON-friendly representation of the full run.
- `TemplateResolver.__init__` (method) `modules/pipeline_engine.py:275` `def __init__(self, context)`
- `TemplateResolver.render` (method) `modules/pipeline_engine.py:278` `def render(self, template)`
- `TemplateResolver.resolve` (method) `modules/pipeline_engine.py:289` `def resolve(self, dotted_path)` -- Return the value at dotted_path or None when not found.
- `ConditionEvaluator.is_truthy` (method) `modules/pipeline_engine.py:330` `def is_truthy(rendered)`
- `StepValidator.validate` (method) `modules/pipeline_engine.py:352` `def validate(predicate, output)`
- `StepDerivers.register` (method) `modules/pipeline_engine.py:389` `def register(cls, command, deriver)` -- Bind a deriver to a top-level command name (case-insensitive).
- `StepDerivers.derive` (method) `modules/pipeline_engine.py:396` `def derive(cls, command, output)` -- Run the registered deriver for command on output, defensive.
- `IStepRunner.run` (method) `modules/pipeline_engine.py:513` `def run(self, command, args, target, timeout_s)` -- Execute one command.
- `LazyOwnStepRunner.__init__` (method) `modules/pipeline_engine.py:537` `def __init__(self, runner, onecmd)`
- `LazyOwnStepRunner.run` (method) `modules/pipeline_engine.py:548` `def run(self, command, args, target, timeout_s)`
- `PipelineLoader.__init__` (method) `modules/pipeline_engine.py:638` `def __init__(self, pipelines_dir)`
- `PipelineLoader.pipelines_dir` (method) `modules/pipeline_engine.py:642` `def pipelines_dir(self)`
- `PipelineLoader.list` (method) `modules/pipeline_engine.py:645` `def list(self)` -- Return every pipeline name discoverable in pipelines_dir.
- `PipelineLoader.resolve_path` (method) `modules/pipeline_engine.py:658` `def resolve_path(self, name)` -- Return the absolute path to the YAML file for the given name.
- `PipelineLoader.load` (method) `modules/pipeline_engine.py:683` `def load(self, name)` -- Parse the YAML file for name and return a validated spec.
- `RunArtifactStore.__init__` (method) `modules/pipeline_engine.py:778` `def __init__(self, runs_dir)`
- `RunArtifactStore.runs_dir` (method) `modules/pipeline_engine.py:782` `def runs_dir(self)`
- `RunArtifactStore.open_run` (method) `modules/pipeline_engine.py:785` `def open_run(self, pipeline_name, run_id)` -- Create and return the directory for this run.
- `RunArtifactStore.write_plan` (method) `modules/pipeline_engine.py:797` `def write_plan(self, run_dir, spec)`
- `RunArtifactStore.write_step` (method) `modules/pipeline_engine.py:814` `def write_step(self, run_dir, result)`
- `RunArtifactStore.write_summary` (method) `modules/pipeline_engine.py:828` `def write_summary(self, run_dir, run)`
- `INarratorAdapter.narrate` (method) `modules/pipeline_engine.py:852` `def narrate(self, kind, target, message, payload, severity)` -- Emit one narration event.
- `_SilentNarrator.narrate` (method) `modules/pipeline_engine.py:864` `def narrate(self)`
- `EngagementNarratorAdapter.__init__` (method) `modules/pipeline_engine.py:871` `def __init__(self, narrator)`
- `EngagementNarratorAdapter.narrate` (method) `modules/pipeline_engine.py:881` `def narrate(self, kind, target, message, payload, severity)`
- `PipelineEngine.__init__` (method) `modules/pipeline_engine.py:927` `def __init__(self, runner, loader, artifact_store, narrator, max_nesting)`
- `PipelineEngine.loader` (method) `modules/pipeline_engine.py:942` `def loader(self)`
- `PipelineEngine.validate` (method) `modules/pipeline_engine.py:945` `def validate(self, name)` -- Load and validate without executing.
- `PipelineEngine.run` (method) `modules/pipeline_engine.py:949` `def run(self, name, target, nesting_stack)` -- Execute the pipeline.
- `get_default_engine` (function) `modules/pipeline_engine.py:1300` `def get_default_engine(onecmd)` -- Process-wide default engine for production callers.
- `mcp_pipeline_run` (function) `modules/pipeline_engine.py:1314` `def mcp_pipeline_run(name, target, background, onecmd)` -- Public MCP / CLI entry: run a pipeline.
- `mcp_pipeline_list` (function) `modules/pipeline_engine.py:1368` `def mcp_pipeline_list()` -- Return the list of available pipelines under pipelines/.
- `mcp_pipeline_validate` (function) `modules/pipeline_engine.py:1385` `def mcp_pipeline_validate(name)` -- Validate a pipeline's YAML schema without executing it.
- `mcp_pipeline_status` (function) `modules/pipeline_engine.py:1414` `def mcp_pipeline_status(last_n)` -- Return the N most recent pipeline runs and their summaries.
- `cmd_pipeline` (function) `modules/pipeline_engine.py:1436` `def cmd_pipeline(action, name, target, background)` -- CLI helper bound to the ``pipeline`` daemon subcommand.

## modules/planner.py
Depends on: `core/logging.py`, `modules/llm_client.py`, `modules/obs_parser.py`, `modules/playbook_engine.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`, `cli/commands/session_ops.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_autonomous_ops.py`, `tests/test_daemon_loop.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`
- `Planner.__init__` (method) `modules/planner.py:269` `def __init__(self, world_model, obs_parser, api_key)`
- `Planner.plan` (method) `modules/planner.py:313` `def plan(self, target, max_candidates)` -- Return a ranked list of next-step candidates for *target*.
- `Planner.to_dict` (method) `modules/planner.py:413` `def to_dict(self, result)`
- `get_planner` (function) `modules/planner.py:446` `def get_planner(api_key)` -- Return a fact-based planner with an optional LLM tie-break key.
- `TodoList.__init__` (method) `modules/planner.py:468` `def __init__(self)` -- Initialize an empty todo sequence.
- `TodoList.todo_add` (method) `modules/planner.py:472` `def todo_add(self, name, requires)` -- Append a step and return it.
- `TodoList.todo_done` (method) `modules/planner.py:478` `def todo_done(self, name)` -- Mark a step done when its requirements hold.
- `TodoList.next_ready` (method) `modules/planner.py:489` `def next_ready(self)` -- Return the first pending step whose requirements hold.
- `TodoList.blocks` (method) `modules/planner.py:497` `def blocks(self, tactic)` -- Return True when a tactic must wait for an unfinished chain.
- `Frontier.__init__` (method) `modules/planner.py:514` `def __init__(self, planner, todos)` -- Bind the frontier to a planner and an optional todo list.
- `Frontier.todos` (method) `modules/planner.py:523` `def todos(self)` -- Expose the shared todo list.
- `Frontier.tried` (method) `modules/planner.py:528` `def tried(self)` -- Return the tried technique identifiers.
- `Frontier.refill` (method) `modules/planner.py:532` `def refill(self, target, max_intents)` -- Plan fresh intents, keeping only untried and unblocked ones.
- `Frontier.pop` (method) `modules/planner.py:551` `def pop(self)` -- Claim the oldest queued intent and mark its technique tried.

## modules/playbook_admin.py
Imported by: `cli/orchestrator_assets_tabs.py`, `tests/test_playbook_admin.py`
- `slugify` (function) `modules/playbook_admin.py:62` `def slugify(value)` -- Return a safe playbook filename stem.
- `playbook_path` (function) `modules/playbook_admin.py:75` `def playbook_path(filename, directory)` -- Resolve one playbook file inside the playbooks root.
- `load_playbook` (function) `modules/playbook_admin.py:102` `def load_playbook(path)` -- Read one playbook YAML mapping.
- `playbook_kind` (function) `modules/playbook_admin.py:123` `def playbook_kind(data)` -- Return ``apt``, ``plan``, ``mixed`` or ``unknown`` for one mapping.
- `validate_playbook` (function) `modules/playbook_admin.py:136` `def validate_playbook(data)` -- Validate the minimal shape shared by both playbook formats.
- `summarize` (function) `modules/playbook_admin.py:197` `def summarize(path)` -- Build the admin-table row for one file without raising.
- `scan_playbooks` (function) `modules/playbook_admin.py:231` `def scan_playbooks(directory)` -- Return every ``*.yaml``/``*.yml`` playbook, sorted by file name.
- `preview_playbook` (function) `modules/playbook_admin.py:251` `def preview_playbook(path, limit)` -- Return a bounded, sanitized text preview for the detail pane.
- `playbook_template` (function) `modules/playbook_admin.py:265` `def playbook_template(name, description, platforms)` -- Return a minimal APT playbook mapping ready for ``yaml.safe_dump``.
- `create_playbook` (function) `modules/playbook_admin.py:297` `def create_playbook(filename)` -- Create one APT playbook file.
- `update_playbook` (function) `modules/playbook_admin.py:350` `def update_playbook(path, data, directory)` -- Validate and atomically rewrite one playbook.
- `save_playbook_yaml` (function) `modules/playbook_admin.py:377` `def save_playbook_yaml(path, text, directory)` -- Parse, validate and write a raw YAML document.
- `delete_playbook` (function) `modules/playbook_admin.py:406` `def delete_playbook(path, directory)` -- Delete one playbook confined to the playbooks root.

## modules/playbook_engine.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/emulation_runner.py`, `modules/llm_client.py`, `modules/obs_parser.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`, `cli/commands/mcp_bridge.py`, `modules/operation.py`, `modules/planner.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
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

## modules/r.sh
Imported by: `static/js/quill-2.0.3.js::c`, `static/js/quill-2.0.3.js::h`, `static/js/quill-2.0.3.js::i`, `static/js/quill-2.0.3.js::o`, `static/js/quill-2.0.3.js::s`, `static/js/quill-2.0.3.js::u`, `static/js/xterm.js::a`, `static/js/xterm.js::n`, `static/js/xterm.js::o`
- `download_kernel_sources` (function) `modules/r.sh:10` -- Función para descargar y extraer las fuentes del kernel

## modules/reaction_bridge.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/lazy_loop.py`, `tests/test_reaction_bridge.py`
- `ReactionPick.__init__` (method) `modules/reaction_bridge.py:69` `def __init__(self, command, reason, priority, mitre)`
- `save_decisions` (function) `modules/reaction_bridge.py:80` `def save_decisions(task_id, decisions)` -- Park picks into the per-task buffer; returns the saved count.
- `load_reaction_triggers` (function) `modules/reaction_bridge.py:108` `def load_reaction_triggers(task_id, consumer)` -- Drain the buffer into planner trigger dicts (one-shot, one per round).
- `find_credentials` (function) `modules/reaction_bridge.py:159` `def find_credentials(output)` -- Extract user:pass pairs and hashes; placeholder values are dropped.

## modules/reactive_engine.py
Depends on: `core/config.py`, `core/logging.py`, `modules/session_rag.py`
Imported by: `cli/apt_chain_support.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/toposwarm_autonomous.py`, `tests/test_core_modules.py`, `tests/test_reactive_engine_semantic.py`, `tests/test_reactive_lateral_data.py`
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
Imported by: `skills/lazyown_mcp.py`
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
Depends on: `core/crypto.py`, `lazyown-docker/init.sh`
- `regs_override_return` (function) `modules/rootkit/rootkit.c:54` `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` -- Define regs_override_return function
- `hooked_getdents` (function) `modules/rootkit/rootkit.c:86` `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents function
- `hooked_getdents64` (function) `modules/rootkit/rootkit.c:112` `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents64 function
- `hooked_read` (function) `modules/rootkit/rootkit.c:138` `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked read function to create a backdoor
- `disable_module_signature_verification` (function) `modules/rootkit/rootkit.c:192` `static void disable_module_signature_verification(void)` -- Function to disable module signature verification
- `hook_syscalls` (function) `modules/rootkit/rootkit.c:206` `static int __init hook_syscalls(void)` -- Function to hook system calls
- `unhook_syscalls` (function) `modules/rootkit/rootkit.c:219` `static void __exit unhook_syscalls(void)` -- Function to unhook system calls


Next: [API_p18.md](API_p18.md)
