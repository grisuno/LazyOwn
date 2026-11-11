# API (page 14 of 28)
Previous: [API_p13.md](API_p13.md)

## modules/lazy_agent.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`
- `model_timeout_sec` (function) `modules/lazy_agent.py:41` `def model_timeout_sec()` -- Return the hard per-turn model timeout from configuration.
- `tool_calling_enabled` (function) `modules/lazy_agent.py:57` `def tool_calling_enabled()` -- Return whether agentic tool calling is enabled by configuration.
- `max_iterations` (function) `modules/lazy_agent.py:72` `def max_iterations()` -- Return the bounded agent step budget from configuration.
- `resolve_agentic_model` (function) `modules/lazy_agent.py:83` `def resolve_agentic_model(exclude)` -- Return a raw tool-calling backend for the best pool member, or None.
- `ObservableAgentRunner.__init__` (method) `modules/lazy_agent.py:148` `def __init__(self, model, system_prompt, max_iterations, on_event)` -- Bind the model and the optional event sink (kind, name, text).
- `ObservableAgentRunner.run` (method) `modules/lazy_agent.py:168` `def run(self, user_input)` -- Base loop plus final-turn persistence for true resume.
- `ConversationStore.__init__` (method) `modules/lazy_agent.py:264` `def __init__(self, task_id)` -- Bind the conversation store for one task (``main`` when empty).
- `ConversationStore.intent_messages` (method) `modules/lazy_agent.py:273` `def intent_messages(self, intent_id)` -- Return the stored messages for one intent (resume seed).
- `ConversationStore.save_intent` (method) `modules/lazy_agent.py:278` `def save_intent(self, intent_id, messages)` -- Persist the tail of one intent conversation.
- `ConversationStore.session` (method) `modules/lazy_agent.py:287` `def session(self, session_id)` -- Return one main-agent session payload (empty when unknown).
- `ConversationStore.sessions` (method) `modules/lazy_agent.py:291` `def sessions(self)` -- List main-agent sessions with title, message count and age.
- `ConversationStore.save_session` (method) `modules/lazy_agent.py:305` `def save_session(self, session_id, messages, title)` -- Persist one main-agent session conversation tail.
- `ConversationStore.reset_intents` (method) `modules/lazy_agent.py:315` `def reset_intents(self)` -- Drop every stored intent conversation (fresh agent start).
- `register_tools` (function) `modules/lazy_agent.py:322` `def register_tools(runner, specs)` -- Register tool specs (name, description, func, parameters, required).
- `run_worker_session` (function) `modules/lazy_agent.py:335` `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` -- Run one agentic intent attempt with resume seeding.
- `run_main_session` (function) `modules/lazy_agent.py:374` `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` -- Run one main-agent turn, resuming the stored session conversation.
- `run_external_opencode` (function) `modules/lazy_agent.py:396` `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` -- Run one headless ``opencode run`` task with MCP tooling.
- `run_external_hermes` (function) `modules/lazy_agent.py:472` `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` -- Run one detached ``hermes chat --oneshot`` task.

## modules/lazy_autofire.py
Depends on: `modules/__init__.py`, `modules/chain_synth.py`, `modules/lazy_probes.py`
Imported by: `tests/test_loop_fire_pending.py`
- `autofire_armed` (function) `modules/lazy_autofire.py:41` `def autofire_armed(payload)` -- Whether the operator armed autofire in ``payload.json``.
- `consider_report` (function) `modules/lazy_autofire.py:53` `def consider_report(report, chains_dir, state_path, armed, now)` -- Turn fire-tier bounded matches into a confirmation chain.
- `fire_from_file` (function) `modules/lazy_autofire.py:105` `def fire_from_file(target, feed_path)` -- Consider the saved exposure report of one target.
- `sweep_state` (function) `modules/lazy_autofire.py:127` `def sweep_state(state_path, now)` -- Drop expired cooldown entries to keep the state file small.
- `status` (function) `modules/lazy_autofire.py:147` `def status(payload, state_path)` -- Summarize autofire for the operator surfaces.

## modules/lazy_blindspot.py
Imported by: `modules/lazy_loop.py`, `tests/test_lazy_blindspot.py`
- `BlindspotFinding.as_hint` (method) `modules/lazy_blindspot.py:70` `def as_hint(self)` -- Render the finding as a hint line the planner consumes.
- `parse_blindspots` (function) `modules/lazy_blindspot.py:82` `def parse_blindspots(raw)` -- Parse blindspot findings from a model reply.
- `build_blindspot_prompt` (function) `modules/lazy_blindspot.py:145` `def build_blindspot_prompt(goal, context)` -- Render the blindspot prompt with fenced untrusted content.
- `BlindspotReview.__init__` (method) `modules/lazy_blindspot.py:171` `def __init__(self, complete, add_hint)` -- Bind the LLM callable and the hint sink.
- `BlindspotReview.run` (method) `modules/lazy_blindspot.py:176` `def run(self, goal, context)` -- Review the task and write one hint per finding.
- `BlindspotReview.apply` (method) `modules/lazy_blindspot.py:200` `def apply(self, findings)` -- Write hints for the findings already parsed.

## modules/lazy_bridge.py
Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/mcp_tools/lazy_status.py`, `skills/mcp_tools/lazy_sync.py`, `tests/conftest.py`, `tests/test_cve_pipeline.py`, `tests/test_lazy_loop.py`
- `lazy_tasks` (function) `modules/lazy_bridge.py:92` `def lazy_tasks()` -- Load LAZY task registry.
- `lazy_assets` (function) `modules/lazy_bridge.py:103` `def lazy_assets()` -- Load LAZY asset nodes.
- `lazy_graph` (function) `modules/lazy_bridge.py:114` `def lazy_graph(task_id)` -- Load experiment graph for a task.
- `lazy_activity` (function) `modules/lazy_bridge.py:127` `def lazy_activity(task_id)` -- Load activity transcript for a task.
- `lazy_traffic` (function) `modules/lazy_bridge.py:139` `def lazy_traffic(task_id)` -- Load traffic log for a task.
- `lazy_guard_audit` (function) `modules/lazy_bridge.py:151` `def lazy_guard_audit(task_id)` -- Load guard audit for a task.
- `bridge_status` (function) `modules/lazy_bridge.py:163` `def bridge_status()` -- Summarize LAZY universe and last sync cursor.
- `pull_to_world_model` (function) `modules/lazy_bridge.py:221` `def pull_to_world_model()` -- Sync LAZY graphs and assets into LazyOwn world model.
- `pull_to_objectives` (function) `modules/lazy_bridge.py:298` `def pull_to_objectives()` -- Inject open LAZY tasks as LazyOwn objectives without duplicates.
- `pull_findings_to_lifecycle` (function) `modules/lazy_bridge.py:333` `def pull_findings_to_lifecycle()` -- Confirm LAZY finding nodes in LazyOwn finding lifecycle.
- `pull_traffic_to_recorder` (function) `modules/lazy_bridge.py:408` `def pull_traffic_to_recorder(progress)` -- Mirror new LAZY traffic rows into the LazyOwn recorder index.
- `push_objective_to_lazy` (function) `modules/lazy_bridge.py:476` `def push_objective_to_lazy(goal, scope)` -- Export a LazyOwn objective as an LAZY-compatible task draft.
- `push_tasks_to_c2` (function) `modules/lazy_bridge.py:501` `def push_tasks_to_c2(only)` -- Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).
- `sync_all` (function) `modules/lazy_bridge.py:566` `def sync_all(progress)` -- Run full bidirectional pull plus lifecycle, traffic and board mirror.

## modules/lazy_checks.py
Depends on: `modules/lazy_heat.py`
Imported by: `tests/test_lazy_checks.py`
- `extract_version` (function) `modules/lazy_checks.py:30` `def extract_version(text)` -- Pull the most version-like token from check output.
- `extract_cve` (function) `modules/lazy_checks.py:51` `def extract_cve(text)` -- Pull the uppercased CVE id from a finding text, or ''.
- `interpret_checks` (function) `modules/lazy_checks.py:57` `def interpret_checks(checks, cve, stored_version, ranges)` -- Re-read check results through the stored version range.

## modules/lazy_cli_bridge.py
Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`
- `cli_verbs` (function) `modules/lazy_cli_bridge.py:106` `def cli_verbs()` -- Return every discovered shell verb, cached by source mtime.
- `is_cli_verb` (function) `modules/lazy_cli_bridge.py:125` `def is_cli_verb(name)` -- Return True when name is a real shell command.
- `phase_for` (function) `modules/lazy_cli_bridge.py:131` `def phase_for(verb)` -- Map a verb to its kill-chain phase via keyword affinity.
- `risk_for` (function) `modules/lazy_cli_bridge.py:140` `def risk_for(verb)` -- Classify a verb as safe, exploit or high risk.
- `needs_target_for` (function) `modules/lazy_cli_bridge.py:150` `def needs_target_for(verb)` -- Return whether the verb usually carries a target argument.
- `build_cli_command` (function) `modules/lazy_cli_bridge.py:158` `def build_cli_command(verb, target)` -- Build a shell line for any CLI verb bound to target.
- `search_cli_verbs` (function) `modules/lazy_cli_bridge.py:185` `def search_cli_verbs(query, phase, limit)` -- Search the full CLI catalog by keyword and phase.
- `cli_catalog_for_phase` (function) `modules/lazy_cli_bridge.py:211` `def cli_catalog_for_phase(phase, limit)` -- Return a compact verb list for LLM prompt injection.
- `catalog_cli_for_phase` (function) `modules/lazy_cli_bridge.py:240` `def catalog_cli_for_phase(limit)` -- Return enabled catalog commands for the current kill-chain phase.
- `full_cli_enabled` (function) `modules/lazy_cli_bridge.py:274` `def full_cli_enabled()` -- Return whether the loop may route any CLI verb.
- `set_full_cli` (function) `modules/lazy_cli_bridge.py:297` `def set_full_cli(enabled)` -- Persist the full-CLI routing flag and return the new value.

## modules/lazy_commander.py
Imported by: `cli/commands/lazyops.py`, `tests/test_lazy_commander.py`
- `parse_commander_decision` (function) `modules/lazy_commander.py:77` `def parse_commander_decision(raw)` -- Parse one commander decision from a model reply.
- `render_board` (function) `modules/lazy_commander.py:119` `def render_board(rows, worked)` -- Render the task board as a compact fenced block body.
- `build_commander_prompt` (function) `modules/lazy_commander.py:145` `def build_commander_prompt(board_rows, time_budget, worked)` -- Render the commander prompt with fenced untrusted board content.
- `format_commander_budget` (function) `modules/lazy_commander.py:161` `def format_commander_budget(deadline, now)` -- Human-readable remaining slot-clock time for the prompt.
- `LazyCommander.__init__` (method) `modules/lazy_commander.py:190` `def __init__(self, board_fn, complete_fn, work_fn, pause_fn, clock, sleep)` -- Bind the injected engine callables and the clock.
- `LazyCommander.run` (method) `modules/lazy_commander.py:207` `def run(self, minutes, max_slices, base_workers)` -- Allocate slices until the deadline, the slice cap or a stop.

## modules/lazy_continuation.py
- `record_path` (function) `modules/lazy_continuation.py:77` `def record_path(target)` -- Return the continuation record path for one target.
- `save` (function) `modules/lazy_continuation.py:89` `def save(target, task_id, goal, status, settlement, findings, next_steps, credentials, deviations)` -- Write one target's continuation record atomically.
- `load` (function) `modules/lazy_continuation.py:144` `def load(target)` -- Read one target's continuation record.
- `handover_brief` (function) `modules/lazy_continuation.py:173` `def handover_brief(target)` -- Render a target's continuation record as a successor-ready playbook.
- `recall_candidates` (function) `modules/lazy_continuation.py:214` `def recall_candidates(target, limit)` -- Return ``(intent_summary, reason)`` wake candidates for one target.

## modules/lazy_creds.py
- `load` (function) `modules/lazy_creds.py:39` `def load()` -- Load the CSV knowledge base once per process.
- `search` (function) `modules/lazy_creds.py:63` `def search(query)` -- Return rows whose vendor or username contains the query.
- `candidates` (function) `modules/lazy_creds.py:79` `def candidates(limit)` -- Return the most repeated (username, password) pairs for spraying.
- `count` (function) `modules/lazy_creds.py:96` `def count()` -- Return the total number of knowledge-base rows.
- `as_lines` (function) `modules/lazy_creds.py:101` `def as_lines(rows)` -- Render rows as aligned ``vendor,username,password`` lines.
- `export_pairs` (function) `modules/lazy_creds.py:106` `def export_pairs(path, limit)` -- Export ``username:password`` pairs for spray tools.

## modules/lazy_cve_feed.py
Depends on: `modules/lazy_heat.py`
Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/lazy_feedmatch.py`, `modules/lazy_hostscore.py`, `tests/test_lazy_checks.py`
- `load_kev` (function) `modules/lazy_cve_feed.py:158` `def load_kev(force)` -- Return ``{cve_id: {product, vendor}}`` from the CISA KEV catalog.
- `load_epss` (function) `modules/lazy_cve_feed.py:192` `def load_epss(force)` -- Return ``{cve_id: epss}`` from the FIRST daily EPSS scores.
- `load_exploit_cves` (function) `modules/lazy_cve_feed.py:233` `def load_exploit_cves(force)` -- Return CVE ids with public exploit code (Exploit-DB index).
- `load_msf_cves` (function) `modules/lazy_cve_feed.py:257` `def load_msf_cves(force)` -- Return CVE ids weaponized as Metasploit modules.
- `fetch_product_advisories` (function) `modules/lazy_cve_feed.py:291` `def fetch_product_advisories(product, force)` -- Fetch OSV advisories naming one product.
- `cve_intel` (function) `modules/lazy_cve_feed.py:360` `def cve_intel(cve_id, feeds, allow_network)` -- Assemble exploitation signals and the heat tier for one CVE.
- `correlate` (function) `modules/lazy_cve_feed.py:438` `def correlate(product, version, allow_network)` -- Version-aware CVE candidates for one service product.
- `convert_osv_ranges` (function) `modules/lazy_cve_feed.py:515` `def convert_osv_ranges(affected)` -- Convert one OSV ``affected`` entry into version-range dicts.
- `range_for_cve` (function) `modules/lazy_cve_feed.py:565` `def range_for_cve(cve_id, allow_network)` -- Return the OSV affected ranges bound to one CVE, offline-first.
- `load_kev_matches` (function) `modules/lazy_cve_feed.py:594` `def load_kev_matches(product, feeds)` -- KEV entries whose vendor/product names match one service product.
- `hot_matches` (function) `modules/lazy_cve_feed.py:636` `def hot_matches(services, allow_network)` -- Hot/warm CVE candidates matching discovered services.
- `refresh_feeds_async` (function) `modules/lazy_cve_feed.py:680` `def refresh_feeds_async(products)` -- Refresh bulk feeds in one background daemon thread.

## modules/lazy_deviations.py
Imported by: `cli/commands/lazyops.py`, `modules/chain_runner.py`, `modules/lazy_loop.py`, `tests/test_lazy_deviations.py`
- `DeviationRecord.as_dict` (method) `modules/lazy_deviations.py:55` `def as_dict(self)` -- Return the record as a JSON-ready dict.
- `DeviationLedger.__init__` (method) `modules/lazy_deviations.py:80` `def __init__(self, path)` -- Bind the ledger file path.
- `DeviationLedger.record` (method) `modules/lazy_deviations.py:84` `def record(self, scope, planned, actual, reason, source)` -- Record one deviation when the plan actually changed.
- `DeviationLedger.list` (method) `modules/lazy_deviations.py:124` `def list(self, scope, limit)` -- Return deviations, newest first, optionally scoped.
- `DeviationLedger.render_markdown` (method) `modules/lazy_deviations.py:140` `def render_markdown(self, records, title)` -- Render records as the sapper-style deviations block.

## modules/lazy_drafts.py
Depends on: `modules/lazy_loop.py`
Imported by: `tests/test_loop_objective_wiring.py`
- `drain` (function) `modules/lazy_drafts.py:34` `def drain(engine)` -- Import every pending draft into the loop task board.

## modules/lazy_exposure.py
Depends on: `modules/__init__.py`, `modules/lazy_feedmatch.py`, `modules/lazy_heat.py`, `modules/lazy_probes.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/exposure_intel.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `skills/mcp_tools/lazy_intel.py`, `tests/test_lazy_exposure.py`
- `ensure_report` (function) `modules/lazy_exposure.py:56` `def ensure_report(target, entries, refresh)` -- Create the target exposure report if absent (loop bootstrap path).
- `read_sightings` (function) `modules/lazy_exposure.py:97` `def read_sightings(target, state_path)` -- Extract observed service sightings from the encrypted world model.
- `generate_report` (function) `modules/lazy_exposure.py:129` `def generate_report(target, entries, sightings)` -- Build the exposure report for one target.
- `score_report` (function) `modules/lazy_exposure.py:219` `def score_report(entries, bounded_unknown, services)` -- Score a host 0-100 with an audited point breakdown.
- `probe_checks` (function) `modules/lazy_exposure.py:257` `def probe_checks(matches, feed)` -- Render read-only validation checks for the hottest matches.
- `save_report` (function) `modules/lazy_exposure.py:291` `def save_report(report, path)` -- Atomically persist the report for downstream surfaces.
- `publish_report` (function) `modules/lazy_exposure.py:314` `def publish_report(report)` -- Publish one outcome event for the whole report.
- `refresh_if_stale` (function) `modules/lazy_exposure.py:418` `def refresh_if_stale(target, entries)` -- Regenerate the report only when newer evidence exists.

## modules/lazy_fallback.py
Depends on: `modules/atomic_exploit_bridge.py`, `modules/failure_verdict.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/lazy_adaptive.py`, `tests/test_lazy_fallback.py`
- `TechniqueFallback.matches` (method) `modules/lazy_fallback.py:61` `def matches(self, command)` -- Return True when the failed command line binds this family.
- `AdaptiveFallbackArbiter.__init__` (method) `modules/lazy_fallback.py:193` `def __init__(self, graph)` -- Bind the fallback graph; the shared graph is the default.
- `AdaptiveFallbackArbiter.suggest` (method) `modules/lazy_fallback.py:203` `def suggest(self, command, verdict, services, has_credentials, catalogue)` -- Return the first viable untried alternative for one failure.
- `AdaptiveFallbackArbiter.tried_count` (method) `modules/lazy_fallback.py:246` `def tried_count(self)` -- Return how many alternatives this arbiter already proposed.
- `catalogue_ids` (function) `modules/lazy_fallback.py:261` `def catalogue_ids()` -- Return every Atomic technique id actually loadable right now.

## modules/lazy_feedmatch.py
Depends on: `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`
Imported by: `modules/lazy_exposure.py`, `modules/lazy_inventory.py`, `modules/lazy_sentinel.py`, `tests/test_lazy_exposure.py`, `tests/test_lazy_feedmatch.py`, `tests/test_lazy_sentinel.py`
- `load_feed` (function) `modules/lazy_feedmatch.py:151` `def load_feed(path)` -- Load raw feed rows from a JSON file.
- `parse_feed` (function) `modules/lazy_feedmatch.py:210` `def parse_feed(entries)` -- Normalize raw feed rows into :class:`FeedEntry` objects.
- `is_os_sighting` (function) `modules/lazy_feedmatch.py:248` `def is_os_sighting(name)` -- Whether a scanner label names an operating system, never an application.
- `entry_matches_product` (function) `modules/lazy_feedmatch.py:262` `def entry_matches_product(entry, product)` -- Whether an advisory and a sighting name the same product.
- `version_in_ranges` (function) `modules/lazy_feedmatch.py:280` `def version_in_ranges(version, ranges)` -- Test a parsed version against an advisory's affected ranges.
- `feed_tier` (function) `modules/lazy_feedmatch.py:325` `def feed_tier(entry)` -- Feed-level heat tier of one advisory via :mod:`modules.lazy_heat`.
- `bind_sighting` (function) `modules/lazy_feedmatch.py:337` `def bind_sighting(sighting, entries)` -- Bind one service sighting to every advisory that names its product.
- `unversioned_leads` (function) `modules/lazy_feedmatch.py:388` `def unversioned_leads(sightings)` -- Products seen with no version, as leads for later promotion.
- `live_bindings` (function) `modules/lazy_feedmatch.py:411` `def live_bindings(sighting, allow_network)` -- Correlate one sighting through the live keyless feed bundle.
- `feed_fingerprint` (function) `modules/lazy_feedmatch.py:486` `def feed_fingerprint(entries)` -- Return a size/mtime fingerprint for feed provenance in reports.

## modules/lazy_finalizer.py
Imported by: `tests/test_chain_finalizer.py`
- `FinalizerDecision.to_dict` (method) `modules/lazy_finalizer.py:58` `def to_dict(self)` -- Return the decision as a JSON-serialisable dict for the verdict map.
- `decide` (function) `modules/lazy_finalizer.py:72` `def decide(status, candidate_verdict, facts, findings, confirmed, tested, pending_approvals, pending_plan_steps)` -- Return the evidence-gated finalization decision for a run.

## modules/lazy_findings.py
Depends on: `core/hardening.py`
Imported by: `tests/test_findings_gate.py`, `tests/test_lazy_findings.py`
- `LedgerLimits.clamped` (method) `modules/lazy_findings.py:81` `def clamped(self)` -- Return a copy with every knob forced into its valid range.
- `engagement_id_valid` (function) `modules/lazy_findings.py:91` `def engagement_id_valid(value)` -- Return True when the engagement id is safe as a path segment.
- `technique_id_valid` (function) `modules/lazy_findings.py:103` `def technique_id_valid(value)` -- Return True when a MITRE technique or tactic id is well formed.
- `severity_tier` (function) `modules/lazy_findings.py:116` `def severity_tier(severity)` -- Map a severity to a starting state and evidence level.
- `level_for_state_uplift` (function) `modules/lazy_findings.py:138` `def level_for_state_uplift(level, state)` -- Return the evidence level after a state transition.
- `evidence_reject_reason` (function) `modules/lazy_findings.py:156` `def evidence_reject_reason(state, evidence, min_output)` -- Reason a ``confirmed`` state is rejected, or an empty string.
- `state_counts` (function) `modules/lazy_findings.py:191` `def state_counts(rows)` -- Count the latest known state per finding reference.
- `metadata_level` (function) `modules/lazy_findings.py:217` `def metadata_level(payload)` -- Return the recorded evidence level of an event, sane default.
- `row_from_event` (function) `modules/lazy_findings.py:230` `def row_from_event(payload, limits)` -- Map one outcome event to a ledger row, or None when unmappable.
- `evidence_supported` (function) `modules/lazy_findings.py:281` `def evidence_supported(evidence, min_output)` -- Return True when evidence backing allows the ``confirmed`` state.
- `discard_row` (function) `modules/lazy_findings.py:382` `def discard_row(reason, command, output, technique_id, engagement_id, target)` -- Build a discarded-vector row so dead routes are recorded permanently.
- `normalize_finding` (function) `modules/lazy_findings.py:429` `def normalize_finding(row, limits)` -- Validate and normalize one row without persisting.
- `build_handoff` (function) `modules/lazy_findings.py:481` `def build_handoff(rows, status, rounds)` -- Shape the operator handoff from durable ledger rows.
- `FindingsLedger.__init__` (method) `modules/lazy_findings.py:542` `def __init__(self, engagement_id, base_dir, limits, scrub)` -- Bind the ledger to one engagement path with injected limits.
- `FindingsLedger.file_path` (method) `modules/lazy_findings.py:569` `def file_path(self)` -- Return the ledger JSONL file path.
- `FindingsLedger.normalize` (method) `modules/lazy_findings.py:573` `def normalize(self, row)` -- Validate and normalize one row before persistence.
- `FindingsLedger.append` (method) `modules/lazy_findings.py:606` `def append(self, row)` -- Append one normalized row atomically and return it.
- `FindingsLedger.read` (method) `modules/lazy_findings.py:636` `def read(self, cursor, limit)` -- Read rows paginated by line index.
- `FindingsLedger.rows` (method) `modules/lazy_findings.py:660` `def rows(self)` -- Return every well-formed row in append order.
- `FindingsLedger.history` (method) `modules/lazy_findings.py:684` `def history(self, finding_ref)` -- Return every transition recorded for one finding reference.
- `FindingsLedger.latest_state` (method) `modules/lazy_findings.py:696` `def latest_state(self, finding_ref)` -- Return the newest known state of one finding reference.

## modules/lazy_heat.py
Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_checks.py`, `modules/lazy_cve_feed.py`, `modules/lazy_exposure.py`, `modules/lazy_feedmatch.py`, `modules/lazy_match_policy.py`, `modules/loop_triggers.py`, `modules/sinks/lazy_intel.py`, `tests/test_lazy_feedmatch.py`
- `classify_heat` (function) `modules/lazy_heat.py:71` `def classify_heat(kev, epss, exploit, cvss)` -- Return the heat tier of one CVE from its exploitation signals.
- `match_heat` (function) `modules/lazy_heat.py:94` `def match_heat(tier, cvss, verdict, distro_status)` -- Return the heat of one CVE *on one host*.
- `parse_version` (function) `modules/lazy_heat.py:121` `def parse_version(value, strict)` -- Parse a dotted version string into a comparable tuple.
- `compare_versions` (function) `modules/lazy_heat.py:157` `def compare_versions(a, b)` -- Compare two version tuples zero-padded so (1, 18) == (1, 18, 0).
- `version_in_range` (function) `modules/lazy_heat.py:165` `def version_in_range(ver, rng)` -- Return True/False/None for ``ver`` inside one affected range.
- `cvss3_base_score` (function) `modules/lazy_heat.py:207` `def cvss3_base_score(vector)` -- Compute the CVSS v3 base score from an inline vector string.
- `product_token` (function) `modules/lazy_heat.py:249` `def product_token(value)` -- Normalise a product name to one comparable token.
- `token_matches` (function) `modules/lazy_heat.py:272` `def token_matches(haystack, needle)` -- Whole-token containment of ``needle`` inside ``haystack``.
- `parse_distro_revision` (function) `modules/lazy_heat.py:306` `def parse_distro_revision(banner)` -- Read the distro family and package release from a service banner.
- `backport_status` (function) `modules/lazy_heat.py:345` `def backport_status(banner, fixed_revision)` -- Classify whether a distro already backported the fix.
- `heat_of_severity` (function) `modules/lazy_heat.py:373` `def heat_of_severity(severity)` -- Map a finding severity (label or numeric 1-4) to a heat tier.
- `heat_rank` (function) `modules/lazy_heat.py:392` `def heat_rank(tier)` -- Rank a heat tier for sorting, hottest first (unknown = 0).
- `host_heat` (function) `modules/lazy_heat.py:404` `def host_heat(tier_values, severity_levels, unscanned)` -- Hottest tier visible on a host once for ordering surfaces.
- `hottest` (function) `modules/lazy_heat.py:424` `def hottest(tier_values)` -- Hottest tier of a list, COLD when empty.
- `label_for` (function) `modules/lazy_heat.py:438` `def label_for(status, fixed_revision)` -- Human-readable label for one backport status.

## modules/lazy_hostscore.py
Depends on: `modules/lazy_cve_feed.py`, `modules/lazy_world_diff.py`, `modules/world_model.py`
Imported by: `modules/lazy_loop.py`, `tests/test_lazy_hostscore.py`
- `score_host` (function) `modules/lazy_hostscore.py:34` `def score_host(inputs)` -- Score one host from plain-dict inputs.
- `rescore` (function) `modules/lazy_hostscore.py:96` `def rescore(sessions_dir, allow_network, now)` -- Score the whole world model and persist the table result.
- `load_scores` (function) `modules/lazy_hostscore.py:193` `def load_scores(sessions_dir)` -- Return the persisted per-host scores.

## modules/lazy_installer.py
Depends on: `core/config.py`, `modules/auto_registry.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`
- `installer_enabled` (function) `modules/lazy_installer.py:41` `def installer_enabled()` -- Return whether the loop may resolve install intents.
- `set_installer_enabled` (function) `modules/lazy_installer.py:58` `def set_installer_enabled(enabled)` -- Persist the installer flag and return the stored value.
- `install_command_for` (function) `modules/lazy_installer.py:70` `def install_command_for(tool)` -- Return the allowlisted install recipe for one tool, or None.
- `intent_for` (function) `modules/lazy_installer.py:75` `def intent_for(tool)` -- Build the canonical install intent summary for one tool.
- `tool_from_intent` (function) `modules/lazy_installer.py:80` `def tool_from_intent(text)` -- Extract the tool name from an install intent, else empty string.
- `steps_for_install` (function) `modules/lazy_installer.py:88` `def steps_for_install(text)` -- Resolve an install intent to its recipe, or None.

## modules/lazy_intel.py
Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/mediation/__init__.py`, `modules/world_model.py`, `utils.py`
Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/mediation/intel_mediator.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`
- `infer_source` (function) `modules/lazy_intel.py:88` `def infer_source(command, intent_text)` -- Classify where a resolved step likely came from.
- `describe_command` (function) `modules/lazy_intel.py:114` `def describe_command(command)` -- Describe a command with phase and risk.
- `record_routing_decision` (function) `modules/lazy_intel.py:129` `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `record_routing_outcome` (function) `modules/lazy_intel.py:169` `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `read_decisions` (function) `modules/lazy_intel.py:211` `def read_decisions(task_id, limit)` -- Read routing records, optionally filtered by task.
- `mask_configured` (function) `modules/lazy_intel.py:237` `def mask_configured(text)` -- Mask only operator-configured credential values in live text.
- `stack_signature` (function) `modules/lazy_intel.py:272` `def stack_signature(assets)` -- Fingerprint the target stack from service assets.
- `fuse_routing_decisions` (function) `modules/lazy_intel.py:303` `def fuse_routing_decisions(task_id)` -- Fuse routing records into the world model as host notes.
- `export_spans` (function) `modules/lazy_intel.py:342` `def export_spans(task_id, out)` -- Export activity records as trace spans for observability.

## modules/lazy_inventory.py
Depends on: `modules/lazy_feedmatch.py`
- `inventory_blob` (function) `modules/lazy_inventory.py:49` `def inventory_blob(platform)` -- Return the read-only collector blob for one platform.
- `parse_blob_output` (function) `modules/lazy_inventory.py:61` `def parse_blob_output(text, platform)` -- Parse the collector output into package entries.
- `to_sightings` (function) `modules/lazy_inventory.py:133` `def to_sightings(entries, host)` -- Project package entries into host-source sightings.
- `os_platform_of` (function) `modules/lazy_inventory.py:157` `def os_platform_of(entries)` -- Detect the inventory platform from the entries' own os tag.

## modules/lazy_ledger.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/lazy_loop.py`, `modules/sinks/routing.py`, `tests/test_lazy_ledger.py`
- `window_for` (function) `modules/lazy_ledger.py:32` `def window_for(verb)` -- Return the freshness window for one verb identity.
- `ledger_key` (function) `modules/lazy_ledger.py:53` `def ledger_key(verb, target)` -- Return the identity key of one verb/target pair.
- `key_from_command` (function) `modules/lazy_ledger.py:58` `def key_from_command(command, target)` -- Derive the ledger key from one executed command line.
- `json_load` (function) `modules/lazy_ledger.py:133` `def json_load(path)` -- Read one JSON document or raise on malformed content.
- `fresh` (function) `modules/lazy_ledger.py:140` `def fresh(verb, target, now, sessions_dir)` -- Return True when one verb/target pair already ran inside its TTL.
- `record` (function) `modules/lazy_ledger.py:164` `def record(verb, target, ok, now, sessions_dir)` -- Upsert one completed run so the pair stops being stale.
- `stale_first` (function) `modules/lazy_ledger.py:191` `def stale_first(catalog, now, sessions_dir)` -- Order verb/target pairs: never-run first, then longest-waiting.


Next: [API_p15.md](API_p15.md)
