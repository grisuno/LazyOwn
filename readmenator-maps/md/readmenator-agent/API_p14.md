# API (page 14 of 26)
Previous: [API_p13.md](API_p13.md)

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

## modules/lazy_exposure.py
Depends on: `modules/__init__.py`, `modules/lazy_feedmatch.py`, `modules/lazy_heat.py`, `modules/lazy_probes.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/exposure_intel.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_exposure.py`
- `ensure_report` (function) `modules/lazy_exposure.py:56` `def ensure_report(target, entries, refresh)` -- Create the target exposure report if absent (loop bootstrap path).
- `read_sightings` (function) `modules/lazy_exposure.py:97` `def read_sightings(target, state_path)` -- Extract observed service sightings from the encrypted world model.
- `generate_report` (function) `modules/lazy_exposure.py:129` `def generate_report(target, entries, sightings)` -- Build the exposure report for one target.
- `score_report` (function) `modules/lazy_exposure.py:219` `def score_report(entries, bounded_unknown, services)` -- Score a host 0-100 with an audited point breakdown.
- `probe_checks` (function) `modules/lazy_exposure.py:257` `def probe_checks(matches, feed)` -- Render read-only validation checks for the hottest matches.
- `save_report` (function) `modules/lazy_exposure.py:291` `def save_report(report, path)` -- Atomically persist the report for downstream surfaces.
- `publish_report` (function) `modules/lazy_exposure.py:314` `def publish_report(report)` -- Publish one outcome event for the whole report.
- `refresh_if_stale` (function) `modules/lazy_exposure.py:418` `def refresh_if_stale(target, entries)` -- Regenerate the report only when newer evidence exists.

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

## modules/lazy_loop.py
Depends on: `core/config.py`, `core/crypto.py`, `core/hardening.py`, `core/logging.py`, `core/process.py`, `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/auto_loop_memory.py`, `modules/auto_registry.py`, `modules/autonomous_exploit_engine.py`, `modules/custom_tools.py`, `modules/defense_stages.py`, `modules/digest.py`, `modules/finding_lifecycle.py`, `modules/guardrails/__init__.py`, `modules/harness.py`, `modules/intercept.py`, `modules/killchain.py`, `modules/lazy_bridge.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_exposure.py`, `modules/lazy_hostscore.py`, `modules/lazy_installer.py`, `modules/lazy_intel.py`, `modules/lazy_ledger.py`, `modules/lazy_orchestrator_feedback.py`, `modules/lazy_reaper.py`, `modules/lazy_roles.py`, `modules/lazy_skills.py`, `modules/lazy_timeline.py`, `modules/lazy_world_diff.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/loop_ai_bridge.py`, `modules/loop_guardrails.py`, `modules/loop_triggers.py`, `modules/mediation/__init__.py`, `modules/module_registry.py`, `modules/notify.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/progress_ledger.py`, `modules/reaction_bridge.py`, `modules/reactive_engine.py`, `modules/selection/base.py`, `modules/selection/registry.py`, `modules/selfupdate.py`, `modules/sinks/findings.py`, `modules/traffic_recorder.py`, `modules/trigger_policy.py`, `modules/world_model.py`, `skills/lazyown_policy.py`, `utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/lazy_orchestrator.py`, `cli/retry_support.py`, `lazyc2.py`, `lazyown.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_engine.py`, `modules/lazy_ledger.py`, `modules/lazy_mentions.py`, `modules/lazy_osinfer.py`, `modules/lazy_reaper.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/loop_triggers.py`, `modules/mediation/chain_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/reaction_bridge.py`, `modules/sinks/chain_feed.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_asset_gate.py`, `tests/test_auto_crypto.py`, `tests/test_failure_memory_veto.py`, `tests/test_guardrails.py`, `tests/test_harness_mode.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_ledger.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_lazy_worker_safety.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cli_catalog.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_evidence_wiring.py`, `tests/test_loop_fire_pending.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_nmap_guard.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_store_race.py`, `tests/test_loop_supervision.py`, `tests/test_loop_trigger_hints.py`, `tests/test_loop_worker_traces.py`, `tests/test_mcp_auto_loop_wrapper.py`, `tests/test_module_registry_bridge.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_triggers.py`, `tests/test_orchestrator_yaml.py`, `tests/test_pi_leg.py`, `tests/test_policy_planner_signal.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_codeql_batch.py`, `tests/test_session_brief.py`, `tests/test_sink_chain_feed.py`, `tests/test_trigger_policy.py`, `tests/test_world_diff_retest.py`
- `plausible_command` (function) `modules/lazy_loop.py:169` `def plausible_command(command)` -- Reject obvious hallucinations such as ``nmap --block``.
- `looks_like_prose` (function) `modules/lazy_loop.py:193` `def looks_like_prose(command)` -- Return True when a line is natural-language prose, not a shell command.
- `repair_worker_command` (function) `modules/lazy_loop.py:341` `def repair_worker_command(command, target)` -- Normalize one LLM-proposed worker command.
- `loop_exiting` (function) `modules/lazy_loop.py:471` `def loop_exiting()` -- Return True once the shell is tearing the loop runtime down.
- `arm_exit_watchdog` (function) `modules/lazy_loop.py:488` `def arm_exit_watchdog(seconds)` -- Guarantee process death even with threads stuck in socket reads.
- `scrub_secrets` (function) `modules/lazy_loop.py:511` `def scrub_secrets(text)` -- Mask API keys/tokens before a string reaches logs or the panel.
- `wake_task` (function) `modules/lazy_loop.py:607` `def wake_task(task_id)` -- Signal a running engine that new work landed for its task.
- `register_worker` (function) `modules/lazy_loop.py:641` `def register_worker(worker)` -- Track a live Worker so shell exit can close its side channels.
- `unregister_worker` (function) `modules/lazy_loop.py:647` `def unregister_worker(worker)` -- Drop a finished Worker from the shutdown registry.
- `shutdown_loop_runtime` (function) `modules/lazy_loop.py:653` `def shutdown_loop_runtime(reason)` -- Tear down every loop-owned resource; safe on any exit path.
- `record_worker_traces` (function) `modules/lazy_loop.py:804` `def record_worker_traces(task_id, worker, intent_id, transcripts, state, path)` -- Append one trace row per executed step to the shared trace ledger.
- `task_llm_chain` (function) `modules/lazy_loop.py:938` `def task_llm_chain(store, task_id)` -- Return the per-task LLM chain members (empty when unbound).
- `parse_judge_output` (function) `modules/lazy_loop.py:948` `def parse_judge_output(raw)` -- Parse strict judge JSON demanding decision and comment.
- `judge_command` (function) `modules/lazy_loop.py:976` `def judge_command(command, background, fail_action)` -- Ask the pool for a guard verdict, applying the configured fail policy.
- `AssetGraph.__init__` (method) `modules/lazy_loop.py:1069` `def __init__(self)` -- Load persisted assets or start empty.
- `AssetGraph.dedupe_key` (method) `modules/lazy_loop.py:1087` `def dedupe_key(self, kind, value, parent_id)` -- Compute program-owned dedupe key for an asset.
- `AssetGraph.insert` (method) `modules/lazy_loop.py:1091` `def insert(self, kind, value, parent_id, meta, task_id)` -- Insert asset or return existing node with same dedupe key.
- `AssetGraph.get` (method) `modules/lazy_loop.py:1121` `def get(self, asset_id)` -- Return asset by id or None.
- `AssetGraph.list` (method) `modules/lazy_loop.py:1125` `def list(self, kind)` -- List assets optionally filtered by kind.
- `AssetGraph.mark_tested` (method) `modules/lazy_loop.py:1132` `def mark_tested(self, asset_id)` -- Flag asset as tested by a worker intent.
- `AssetGraph.coverage` (method) `modules/lazy_loop.py:1142` `def coverage(self, scope)` -- Compute tested/total coverage, optionally scoped.
- `AssetGraph.scoped` (method) `modules/lazy_loop.py:1158` `def scoped(self, scope, kind)` -- List assets owned by the task scope via ownership matching.
- `AssetGraph.untested` (method) `modules/lazy_loop.py:1171` `def untested(self, limit)` -- Return oldest untested assets up to limit.
- `AssetGraph.coverage_for` (method) `modules/lazy_loop.py:1176` `def coverage_for(self, graph, scope)` -- Compute task-scoped coverage like the planner graph_overview.
- `AssetGraph.untested_for` (method) `modules/lazy_loop.py:1204` `def untested_for(self, graph, scope, limit)` -- Return scope-filtered assets not yet covered by this task.
- `ExplorationGraph.__init__` (method) `modules/lazy_loop.py:1232` `def __init__(self, task_id)` -- Load task graph or start empty.
- `ExplorationGraph.add_node` (method) `modules/lazy_loop.py:1266` `def add_node(self, kind, text, state, priority, meta)` -- Append node and return it.
- `ExplorationGraph.get` (method) `modules/lazy_loop.py:1294` `def get(self, node_id)` -- Return node by id or None.
- `ExplorationGraph.persist` (method) `modules/lazy_loop.py:1298` `def persist(self)` -- Persist in-memory node/edge state to disk (public write path).
- `ExplorationGraph.set_node_state` (method) `modules/lazy_loop.py:1302` `def set_node_state(self, node_id, state)` -- Transition node state, stamp ``updated`` and persist.
- `ExplorationGraph.set_node_meta` (method) `modules/lazy_loop.py:1321` `def set_node_meta(self, node_id, meta)` -- Replace one node's metadata mapping, stamp ``updated``, persist.
- `ExplorationGraph.set_state` (method) `modules/lazy_loop.py:1340` `def set_state(self, node_id, state)` -- Transition node state and persist.
- `ExplorationGraph.add_edge` (method) `modules/lazy_loop.py:1351` `def add_edge(self, src, dst, kind)` -- Link two existing nodes.
- `ExplorationGraph.anchor` (method) `modules/lazy_loop.py:1364` `def anchor(self, node_id, asset_id)` -- Anchor exploration node to a concrete asset.
- `ExplorationGraph.anchors_for` (method) `modules/lazy_loop.py:1375` `def anchors_for(self, node_id)` -- Return asset ids anchored to node.
- `ExplorationGraph.anchored_nodes` (method) `modules/lazy_loop.py:1379` `def anchored_nodes(self, asset_id)` -- Return exploration node ids anchored to asset.
- `ExplorationGraph.list` (method) `modules/lazy_loop.py:1383` `def list(self, kind, state)` -- List nodes optionally filtered by kind/state.
- `ExplorationGraph.children` (method) `modules/lazy_loop.py:1392` `def children(self, node_id, kind)` -- Return destination ids of outgoing edges.
- `ExplorationGraph.parents` (method) `modules/lazy_loop.py:1399` `def parents(self, node_id, kind)` -- Return source ids of incoming edges.
- `ExplorationGraph.overview` (method) `modules/lazy_loop.py:1406` `def overview(self)` -- Return planner-facing state summary like graph overview.
- `ExplorationGraph.reload` (method) `modules/lazy_loop.py:1429` `def reload(self)` -- Reload graph from disk, discarding in-memory state.
- `ExplorationGraph.compare_and_claim` (method) `modules/lazy_loop.py:1453` `def compare_and_claim(self, node_id)` -- CAS claim: reload, verify still open, then mark running.
- `ExplorationGraph.finding_signature` (method) `modules/lazy_loop.py:1481` `def finding_signature(self, text)` -- Normalize finding text into dedupe signature.
- `ExplorationGraph.has_finding` (method) `modules/lazy_loop.py:1487` `def has_finding(self, text)` -- Return existing finding with same signature or None.
- `ExplorationGraph.node_detail` (method) `modules/lazy_loop.py:1497` `def node_detail(self, node_id)` -- Full node view: text, state, meta, edges, anchors, trace tail.
- `ExplorationGraph.list_facts` (method) `modules/lazy_loop.py:1513` `def list_facts(self, query, limit, hot_full)` -- Keyword-filtered facts like list_facts.
- `ExplorationGraph.record_fact` (method) `modules/lazy_loop.py:1529` `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` -- Worker fact write like recordFact: deduped, anchored, done.
- `Frontier.__init__` (method) `modules/lazy_loop.py:1554` `def __init__(self, graph)` -- Bind frontier to a task graph.
- `Frontier.pending` (method) `modules/lazy_loop.py:1559` `def pending(self)` -- Return pending intents ordered by priority then id.
- `Frontier.claim_next` (method) `modules/lazy_loop.py:1564` `def claim_next(self)` -- Atomically claim highest-priority pending intent (cross-process CAS).
- `ActivityLog.__init__` (method) `modules/lazy_loop.py:1582` `def __init__(self, task_id)` -- Bind log to task.
- `ActivityLog.emit` (method) `modules/lazy_loop.py:1587` `def emit(self, worker, kind, text, intent_id, tool_use_id)` -- Append one activity record and return it.
- `ActivityLog.read` (method) `modules/lazy_loop.py:1612` `def read(self, limit)` -- Return most recent records up to limit.
- `ActivityLog.for_intent` (method) `modules/lazy_loop.py:1626` `def for_intent(self, intent_id)` -- Return records for one intent.
- `ActivityLog.trace` (method) `modules/lazy_loop.py:1630` `def trace(self, intent_id, query, step_id, limit)` -- Work-scoped trace view like get_worker_trace.
- `ActivityLog.search_all` (method) `modules/lazy_loop.py:1668` `def search_all(self, query, limit)` -- Global keyword search across every work in this task.
- `ActivityLog.search` (method) `modules/lazy_loop.py:1698` `def search(self, query, exclude_intent)` -- Search worker traces by keyword, excluding one intent like the planner.
- `TrafficLog.digest_of` (method) `modules/lazy_loop.py:1718` `def digest_of(command, output)` -- Deterministic digest binding a command to its exact output.
- `TrafficLog.__init__` (method) `modules/lazy_loop.py:1735` `def __init__(self, task_id)` -- Bind log to task or global stream.
- `TrafficLog.record` (method) `modules/lazy_loop.py:1740` `def record(self, kind, command, output, meta)` -- Append one traffic record and return it.
- `TrafficLog.read` (method) `modules/lazy_loop.py:1762` `def read(self, limit)` -- Return most recent traffic records.
- `TrafficLog.search` (method) `modules/lazy_loop.py:1776` `def search(self, query, limit)` -- Full-text search over command/output like traffic_search.
- `TrafficLog.search_host` (method) `modules/lazy_loop.py:1787` `def search_host(self, host, port, limit)` -- Port-aware host search: same-host/different-port rows never mix.
- `TrafficLog.get` (method) `modules/lazy_loop.py:1815` `def get(self, digest)` -- Fetch one exchange by digest like traffic_get.
- `TrafficLog.recorder_body` (method) `modules/lazy_loop.py:1822` `def recorder_body(self, digest)` -- Return stored request/response bodies for one proxy exchange.
- `TrafficLog.recorder_blob` (method) `modules/lazy_loop.py:1851` `def recorder_blob(self, digest, part, offset, length)` -- Read a proxy body in ranges like the blob API.
- `TrafficLog.templates` (method) `modules/lazy_loop.py:1882` `def templates(self, limit)` -- Group exchanges by URL-template with counts like the proxy index.
- `TrafficLog.by_template` (method) `modules/lazy_loop.py:1891` `def by_template(self, template, limit)` -- Return exchanges matching one template substring.
- `TrafficLog.bind` (method) `modules/lazy_loop.py:1896` `def bind(self, finding_id, digest, graph, role, note)` -- Attach traffic digest to a finding like bind_finding_traffic.
- `TrafficLog.evidence` (method) `modules/lazy_loop.py:1944` `def evidence(self, finding_id, graph)` -- Return a finding's traffic evidences in display order.
- `TrafficLog.reorder_evidence` (method) `modules/lazy_loop.py:1953` `def reorder_evidence(self, finding_id, digests, graph)` -- Sort a finding's evidences; unlisted ones keep their tail order.
- `TrafficLog.export` (method) `modules/lazy_loop.py:1967` `def export(self, path, limit)` -- Dump recent exchanges to a JSON file like traffic archive export.
- `TrafficLog.archive` (method) `modules/lazy_loop.py:1974` `def archive(self, label)` -- Snapshot traffic stream into sessions/lazy/traffic_archive_*.
- `TrafficLog.clear` (method) `modules/lazy_loop.py:1980` `def clear(self)` -- Drop the traffic stream, returning the discarded record count.
- `Guard.__init__` (method) `modules/lazy_loop.py:1993` `def __init__(self, task_id)` -- Load rules and audit trail.
- `Guard.add_rule` (method) `modules/lazy_loop.py:2019` `def add_rule(self, pattern, action, reason, priority)` -- Register an intercept rule; higher priority evaluates first.
- `Guard.remove_rule` (method) `modules/lazy_loop.py:2030` `def remove_rule(self, pattern)` -- Delete rules matching pattern exactly.
- `Guard.set_judge` (method) `modules/lazy_loop.py:2039` `def set_judge(self, enabled, fail_action)` -- Enable/disable the LLM judge fallback for unmatched commands.
- `Guard.check` (method) `modules/lazy_loop.py:2061` `def check(self, tool, command, tool_use_id, source, intent_id)` -- Evaluate tool call and audit it, returning allow/ask/deny.
- `Guard.audit` (method) `modules/lazy_loop.py:2113` `def audit(self, limit, action, source, query)` -- Return recent audit entries with optional status/source/text filters.
- `Guard.lookup` (method) `modules/lazy_loop.py:2141` `def lookup(self, tool_use_id)` -- Jump to the exact execution behind an approval row.
- `Guard.stats` (method) `modules/lazy_loop.py:2183` `def stats(self)` -- Attribution counters over the audit trail.
- `AssetGate.__init__` (method) `modules/lazy_loop.py:2340` `def __init__(self, task_id)` -- Bind global list plus optional per-task lists.
- `AssetGate.add` (method) `modules/lazy_loop.py:2367` `def add(self, kind, pattern, note, action)` -- Register a block (global or task) or allow (task only) rule.
- `AssetGate.remove` (method) `modules/lazy_loop.py:2388` `def remove(self, rule_id, action)` -- Delete a rule by id; returns True when something was removed.
- `AssetGate.list` (method) `modules/lazy_loop.py:2406` `def list(self)` -- Return global block plus per-task block/allow rules.
- `AssetGate.evaluate` (method) `modules/lazy_loop.py:2410` `def evaluate(self, target)` -- Gate one target: allowed flag plus human-readable reason.
- `Budget.__init__` (method) `modules/lazy_loop.py:2428` `def __init__(self, store)` -- Bind budget counters to task store.
- `Budget.limits` (method) `modules/lazy_loop.py:2432` `def limits(self, task_id)` -- Return effective limits for task.
- `Budget.set_limits` (method) `modules/lazy_loop.py:2443` `def set_limits(self, task_id)` -- Persist budget limits for task.
- `Budget.usage` (method) `modules/lazy_loop.py:2456` `def usage(self, task_id)` -- Return consumed toolcalls/findings/rounds.
- `Budget.record_toolcall` (method) `modules/lazy_loop.py:2466` `def record_toolcall(self, task_id, intent_id)` -- Count one executed tool call.
- `Budget.record_round` (method) `modules/lazy_loop.py:2478` `def record_round(self, task_id)` -- Count one orchestrator round.
- `Budget.check` (method) `modules/lazy_loop.py:2496` `def check(self, task_id)` -- Return ok/exceeded decision with reason.
- `RuntimeTracker.__init__` (method) `modules/lazy_loop.py:2512` `def __init__(self, store)` -- Bind runtime to task store.
- `RuntimeTracker.heartbeat` (method) `modules/lazy_loop.py:2516` `def heartbeat(self, task_id)` -- Return live runtime snapshot.
- `RuntimeTracker.beat` (method) `modules/lazy_loop.py:2534` `def beat(self, task_id, workers)` -- Stamp heartbeat.
- `RuntimeTracker.abort` (method) `modules/lazy_loop.py:2549` `def abort(self, task_id, cause, detail)` -- Stamp abort cause like typed AbortCause.
- `RuntimeTracker.note_trigger` (method) `modules/lazy_loop.py:2565` `def note_trigger(self, task_id, trigger_id)` -- Advance scheduler watermark so restarts never re-fire.
- `InterceptQueue.__init__` (method) `modules/lazy_loop.py:2606` `def __init__(self, task_id)` -- Bind queue to task.
- `InterceptQueue.request` (method) `modules/lazy_loop.py:2620` `def request(self, tool, command, reason, tool_use_id)` -- Enqueue one ask decision and return pending entry.
- `InterceptQueue.pending` (method) `modules/lazy_loop.py:2638` `def pending(self)` -- Return pending entries ordered by id.
- `InterceptQueue.history` (method) `modules/lazy_loop.py:2642` `def history(self, page, per_page, states, query)` -- Paginated intercept history; pending stays fully visible.
- `InterceptQueue.decide` (method) `modules/lazy_loop.py:2694` `def decide(self, item_id, verdict)` -- Approve or deny one pending entry and wake its waiter.
- `InterceptQueue.wait` (method) `modules/lazy_loop.py:2708` `def wait(self, item_id, timeout_sec)` -- Block until decided or timeout; timeout denies safely.
- `TodoStore.__init__` (method) `modules/lazy_loop.py:2740` `def __init__(self, task_id)` -- Load persisted todos.
- `TodoStore.add` (method) `modules/lazy_loop.py:2751` `def add(self, text)` -- Append a serial step and return it.
- `TodoStore.complete` (method) `modules/lazy_loop.py:2758` `def complete(self, item_id)` -- Mark step done.
- `TodoStore.next_pending` (method) `modules/lazy_loop.py:2767` `def next_pending(self)` -- Return first pending step.
- `TodoStore.as_list` (method) `modules/lazy_loop.py:2774` `def as_list(self)` -- Return all steps.
- `TaskStore.__init__` (method) `modules/lazy_loop.py:2782` `def __init__(self)` -- Load task registry.
- `TaskStore.create` (method) `modules/lazy_loop.py:2791` `def create(self, goal, description)` -- Create task record and return it.
- `TaskStore.get` (method) `modules/lazy_loop.py:2802` `def get(self, task_id)` -- Return raw task record or None.
- `TaskStore.list` (method) `modules/lazy_loop.py:2806` `def list(self)` -- Return all task records.
- `TaskStore.set_status` (method) `modules/lazy_loop.py:2810` `def set_status(self, task_id, status)` -- Update task status.
- `TaskStore.pause` (method) `modules/lazy_loop.py:2822` `def pause(self, task_id)` -- Pause planner and workers like the planner Engine.Pause.
- `TaskStore.resume` (method) `modules/lazy_loop.py:2826` `def resume(self, task_id)` -- Resume a paused task back to running like the planner resumeTask.
- `TaskStore.delete` (method) `modules/lazy_loop.py:2835` `def delete(self, task_id)` -- Remove task record; per-task graph files are cleaned by caller.
- `TaskStore.active_count` (method) `modules/lazy_loop.py:2844` `def active_count(self, exclude)` -- Return how many tasks are currently running.
- `TaskStore.queue` (method) `modules/lazy_loop.py:2848` `def queue(self)` -- Return queued tasks in FIFO arrival order.
- `TaskStore.enqueue` (method) `modules/lazy_loop.py:2853` `def enqueue(self, task_id)` -- Mark a task queued with its arrival stamp.
- `TaskStore.dequeue_next` (method) `modules/lazy_loop.py:2864` `def dequeue_next(self)` -- Pop the oldest queued task and mark it running.
- `TaskStore.set_llm_chain` (method) `modules/lazy_loop.py:2879` `def set_llm_chain(self, task_id, members, active)` -- Bind a per-task LLM chain with a failover cursor.
- `TaskStore.llm_state` (method) `modules/lazy_loop.py:2907` `def llm_state(self, task_id)` -- Return the task LLM chain state (empty when unbound).
- `TaskStore.advance_llm` (method) `modules/lazy_loop.py:2913` `def advance_llm(self, task_id)` -- Advance the per-task active member after quota exhaustion.
- `TaskStore.set_skills` (method) `modules/lazy_loop.py:2937` `def set_skills(self, task_id, names, auto)` -- Pin skills for prompt injection and optionally toggle auto-match.
- `TaskStore.set_deadline` (method) `modules/lazy_loop.py:2962` `def set_deadline(self, task_id, timeout_sec)` -- Stamp absolute deadline like the planner deadline coordinator.
- `TaskStore.expired` (method) `modules/lazy_loop.py:2972` `def expired(self, task_id)` -- Report whether task deadline passed.
- `TaskStore.add_constraint` (method) `modules/lazy_loop.py:2978` `def add_constraint(self, task_id, ctype, text, scope)` -- Register allow/deny operation constraint like the planner set_constraints.
- `TaskStore.add_scope` (method) `modules/lazy_loop.py:2997` `def add_scope(self, task_id, kind, value, reason)` -- Register authorized asset scope like the planner add_task_scope.
- `TaskStore.steer` (method) `modules/lazy_loop.py:3008` `def steer(self, task_id, intent_id, message)` -- Attach mid-run correction to a running intent like steer_work.
- `TaskStore.kill` (method) `modules/lazy_loop.py:3017` `def kill(self, task_id, intent_id)` -- Flag a running intent for termination like kill_work.
- `TaskStore.steer_for` (method) `modules/lazy_loop.py:3028` `def steer_for(self, task_id, intent_id)` -- Return pending steer message for intent if any.
- `TaskStore.clear_steer` (method) `modules/lazy_loop.py:3033` `def clear_steer(self, task_id, intent_id)` -- Drop the pending steer message for an intent after delivery.
- `TaskStore.killed` (method) `modules/lazy_loop.py:3046` `def killed(self, task_id, intent_id)` -- Report whether intent was flagged for termination.
- `extract_scope_items` (function) `modules/lazy_loop.py:3052` `def extract_scope_items(goal_text, description)` -- Lift explicit asset scope from goal like the planner goalsScopeTail.
- `extract_constraint_items` (function) `modules/lazy_loop.py:3084` `def extract_constraint_items(goal_text, description)` -- Lift explicit allow/deny operation bounds like the planner goals decomposer.
- `load_intel_scores` (function) `modules/lazy_loop.py:3176` `def load_intel_scores()` -- Return host exposure scores for plan prioritisation.
- `resolve_target` (function) `modules/lazy_loop.py:3205` `def resolve_target(task_id, store, graph)` -- Resolve concrete target for worker commands from scope, assets, goal.
- `decompose_goals` (function) `modules/lazy_loop.py:3228` `def decompose_goals(goal_text, description)` -- Split goal text into verifiable objectives like the planner DecomposeGoals.
- `enrich_asset` (function) `modules/lazy_loop.py:3265` `def enrich_asset(value)` -- Synchronously enrich one asset with DNS and HTTP like the planner enrich.
- `Planner.__init__` (method) `modules/lazy_loop.py:3291` `def __init__(self, task_id, assets, graph, activity, store)` -- Bind planner to task collaborators.
- `Planner.plan` (method) `modules/lazy_loop.py:3319` `def plan(self, triggers)` -- Emit 0..N intents from current situation; most wakeups emit zero.
- `Planner.refine` (method) `modules/lazy_loop.py:3398` `def refine(self)` -- Re-plan pending intents against fresh outcomes, like plan refinement.
- `Planner.finalize` (method) `modules/lazy_loop.py:3883` `def finalize(self, reason)` -- Final planner round: park open intents and record the wrap-up.
- `sink` (function) `modules/lazy_loop.py:3903` `def sink(text)`
- `Worker.__init__` (method) `modules/lazy_loop.py:4009` `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` -- Bind worker to task collaborators.
- `Worker.rebind` (method) `modules/lazy_loop.py:4057` `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` -- Point a pooled worker at the collaborators of the current round.
- `Worker.close` (method) `modules/lazy_loop.py:4081` `def close(self)` -- Release the worker's shell session and shutdown registration.
- `Worker.execute` (method) `modules/lazy_loop.py:4177` `def execute(self, intent, executor, timeout_sec)` -- Run one intent to completion and write facts back.
- `run_command` (function) `modules/lazy_loop.py:5186` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/lazy_loop.py:5212` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/lazy_loop.py:5221` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/lazy_loop.py:5232` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/lazy_loop.py:5245` `def graph_state()` -- Compact exploration overview: intents, facts, findings.
- `shell_open` (function) `modules/lazy_loop.py:5260` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/lazy_loop.py:5264` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/lazy_loop.py:5268` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/lazy_loop.py:5276` `def job_output(job_id)` -- Return the tail of one background job's output.
- `sink` (function) `modules/lazy_loop.py:5739` `def sink(text)`
- `Retester.__init__` (method) `modules/lazy_loop.py:6124` `def __init__(self, graph, activity, traffic)` -- Bind retester to task collaborators.
- `Retester.retest` (method) `modules/lazy_loop.py:6130` `def retest(self, finding_id, executor, note)` -- Re-execute finding evidence to reproduced/fixed/inconclusive.
- `Retester.retest_context` (method) `modules/lazy_loop.py:6294` `def retest_context(self, finding_id)` -- Return finding + PoC + assets + constraints like get_finding_retest_context.
- `ColdCompactor.__init__` (method) `modules/lazy_loop.py:6316` `def __init__(self, graph, activity)` -- Bind compactor to task graph.
- `ColdCompactor.noa_archives` (method) `modules/lazy_loop.py:6426` `def noa_archives(self, limit)` -- List NOA raw archives for this task (newest first).
- `ColdCompactor.hot_set` (method) `modules/lazy_loop.py:6485` `def hot_set(self)` -- Compute hot nodes by reverse reachability from live intents.
- `ColdCompactor.structural_cold` (method) `modules/lazy_loop.py:6507` `def structural_cold(self, hot)` -- Return foldable non-hot nodes before debounce.
- `ColdCompactor.covered_members` (method) `modules/lazy_loop.py:6592` `def covered_members(self)` -- Return node ids already folded under active digests.
- `ColdCompactor.on_planner_round` (method) `modules/lazy_loop.py:6604` `def on_planner_round(self)` -- Advance round, maintain stamps, trigger background compaction.
- `ColdCompactor.compact` (method) `modules/lazy_loop.py:6645` `def compact(self, threshold, mode, debounce_sec)` -- Fold cold facts into digests like coldgraph minor/major.
- `ColdCompactor.expand` (method) `modules/lazy_loop.py:6772` `def expand(self, digest_id, role)` -- Restore digest members like expandDigest.
- `ColdCompactor.cold_index` (method) `modules/lazy_loop.py:6796` `def cold_index(self)` -- Group active digests by anchored asset.
- `ColdCompactor.unfolded` (method) `modules/lazy_loop.py:6814` `def unfolded(self, limit)` -- Return cold facts unfolded up to cap with a truncated flag.
- `ColdCompactor.digest_overview` (method) `modules/lazy_loop.py:6830` `def digest_overview(self)` -- Digest index: every digest with expandable members plus cold index.
- `constraint_block` (function) `modules/lazy_loop.py:6877` `def constraint_block(constraints, scope)` -- Render allow/deny bounds as highest-priority prompt block.
- `settlement_prompt` (function) `modules/lazy_loop.py:6911` `def settlement_prompt(agent, reason)` -- Build the wrap-up instruction used when a run budget ends.
- `terminal_hint` (function) `modules/lazy_loop.py:6972` `def terminal_hint(reason, state)` -- Return a one-line operator explanation for a terminal disposition.
- `build_prompt_context` (function) `modules/lazy_loop.py:7002` `def build_prompt_context(task_id, graph, assets, store, budget, top)` -- Assemble a bounded prompt context for planner/worker LLM calls.
- `finding_severity` (function) `modules/lazy_loop.py:7091` `def finding_severity(text, evidence)` -- Rank finding severity like the report renderer (critical first).
- `FindingService.__init__` (method) `modules/lazy_loop.py:7126` `def __init__(self, task_id, graph, activity, store)` -- Bind service to task collaborators.
- `FindingService.report` (method) `modules/lazy_loop.py:7159` `def report(self, name, summary, poc, severity, vulnclass, intent_id, asset_ids, traffic_refs)` -- Register a finding with severity/evidence/dedupe like report_finding.
- `FindingService.apply_drafts` (method) `modules/lazy_loop.py:7359` `def apply_drafts(self)` -- Commit finished background reporter drafts onto their findings.
- `FindingService.set_status` (method) `modules/lazy_loop.py:7396` `def set_status(self, finding_id, status)` -- Transition finding status like the workflow disposition.
- `FindingService.update_report` (method) `modules/lazy_loop.py:7413` `def update_report(self, finding_id, report)` -- Write the narrative report and bump the evidence version.
- `FindingService.ranked` (method) `modules/lazy_loop.py:7435` `def ranked(self)` -- Findings ordered critical-first like the Markdown renderer.
- `EvidenceStore.__init__` (method) `modules/lazy_loop.py:7445` `def __init__(self, task_id)` -- Bind vault to task.
- `EvidenceStore.add` (method) `modules/lazy_loop.py:7454` `def add(self, finding_id, kind, body)` -- Attach evidence to a finding and return the record.
- `EvidenceStore.verify` (method) `modules/lazy_loop.py:7478` `def verify(self)` -- Return ids whose body fails the sha256 integrity check.
- `EvidenceStore.gc` (method) `modules/lazy_loop.py:7498` `def gc(self, valid_findings)` -- Drop evidence for findings no longer present; returns removed.
- `EvidenceStore.for_finding` (method) `modules/lazy_loop.py:7514` `def for_finding(self, finding_id)` -- Return evidence attached to one finding.
- `EvidenceStore.read` (method) `modules/lazy_loop.py:7518` `def read(self, evidence_id, offset, length)` -- Read one evidence body in bounded byte ranges.
- `EvidenceStore.export` (method) `modules/lazy_loop.py:7555` `def export(self, path)` -- Dump vault to a file for the report pipeline.
- `Notifier.__init__` (method) `modules/lazy_loop.py:7566` `def __init__(self, store)` -- Bind optional channel config from task store.
- `Notifier.channels` (method) `modules/lazy_loop.py:7570` `def channels(self)` -- Return configured channels (empty = log only).
- `Notifier.add_channel` (method) `modules/lazy_loop.py:7578` `def add_channel(self, kind, target, min_severity, extra)` -- Register a channel: log|webhook|file|slack|email with severity floor.
- `Notifier.remove_channel` (method) `modules/lazy_loop.py:7625` `def remove_channel(self, index)` -- Remove one channel by its 1-based list position.
- `Notifier.emit` (method) `modules/lazy_loop.py:7676` `def emit(self, task_id, event, data)` -- Fan out finding/status/task events; returns deliveries.
- `LlmPool.__init__` (method) `modules/lazy_loop.py:7749` `def __init__(self)` -- Load member list and usage ledger paths.
- `LlmPool.members` (method) `modules/lazy_loop.py:7784` `def members(self)` -- Return configured chain in order, seeding defaults on first use.
- `LlmPool.add_member` (method) `modules/lazy_loop.py:7789` `def add_member(self, name, model, priority)` -- Append a chain member backed by llm_factory at call time.
- `LlmPool.remove_member` (method) `modules/lazy_loop.py:7798` `def remove_member(self, name)` -- Drop a chain member.
- `LlmPool.set_priority` (method) `modules/lazy_loop.py:7808` `def set_priority(self, name, priority)` -- Change one member's failover rank, keeping the rest untouched.
- `LlmPool.usage` (method) `modules/lazy_loop.py:7821` `def usage(self)` -- Return per-member call ledger like llm_usage.
- `LlmPool.record_call` (method) `modules/lazy_loop.py:7831` `def record_call(self, member, ok, text)` -- Append one ledger row for external failover callers.
- `LlmPool.complete` (method) `modules/lazy_loop.py:7940` `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` -- Fail over across members; empty string when no backend answers.
- `LlmPool.health` (method) `modules/lazy_loop.py:8105` `def health(self)` -- Return per-member health state for lazy_llm health.
- `LlmPool.context_budget` (method) `modules/lazy_loop.py:8116` `def context_budget(self)` -- Return the prompt context character budget (default 2000).
- `LlmPool.record_raw` (method) `modules/lazy_loop.py:8121` `def record_raw(self)` -- Return whether raw prompt/response recording is enabled.
- `LlmPool.set_record_raw` (method) `modules/lazy_loop.py:8126` `def set_record_raw(self, enabled)` -- Toggle raw prompt/response recording in the pool ledger.
- `LlmPool.raw_entries` (method) `modules/lazy_loop.py:8133` `def raw_entries(self, limit)` -- Return the most recent raw LLM exchanges.
- `LlmPool.raw_entries_for_task` (method) `modules/lazy_loop.py:8147` `def raw_entries_for_task(self, task_id, limit)` -- Return the most recent raw LLM exchanges recorded for one task.
- `LlmPool.set_context_budget` (method) `modules/lazy_loop.py:8210` `def set_context_budget(self, chars)` -- Persist the prompt context character budget.
- `ToolCatalog.__init__` (method) `modules/lazy_loop.py:8228` `def __init__(self)` -- Load binding table.
- `ToolCatalog.bindings` (method) `modules/lazy_loop.py:8245` `def bindings(self, agent)` -- Return bindings for one agent or the whole table.
- `ToolCatalog.bind` (method) `modules/lazy_loop.py:8250` `def bind(self, agent, tool)` -- Opt a tool into an agent lane.
- `ToolCatalog.unbind` (method) `modules/lazy_loop.py:8259` `def unbind(self, agent, tool)` -- Remove a tool from an agent lane.
- `SideQuestions.ask` (method) `modules/lazy_loop.py:8279` `def ask(self, task_id, question, pool, session)` -- Answer from graph overview + recent trace within a char budget.
- `SideQuestions.history` (method) `modules/lazy_loop.py:8325` `def history(self, task_id, session, limit)` -- Return persisted side exchanges, optionally one session only.
- `SideQuestions.sessions` (method) `modules/lazy_loop.py:8333` `def sessions(self, task_id)` -- Return side-question session names for a task.
- `CompanyScope.__init__` (method) `modules/lazy_loop.py:8346` `def __init__(self)` -- Load company table.
- `CompanyScope.add` (method) `modules/lazy_loop.py:8354` `def add(self, name, scope)` -- Register a company with an optional scope pattern.
- `CompanyScope.list` (method) `modules/lazy_loop.py:8363` `def list(self)` -- Return companies with asset counts.
- `CompanyScope.match` (method) `modules/lazy_loop.py:8367` `def match(self, value)` -- Return companies whose scope substring hits the value.
- `TaskArchive.save` (method) `modules/lazy_loop.py:8376` `def save(self, task_id)` -- Snapshot task record + graph + activity tail into one archive.
- `TaskArchive.list` (method) `modules/lazy_loop.py:8397` `def list(self)` -- Return archive snapshots with task + node counts.
- `TaskArchive.restore` (method) `modules/lazy_loop.py:8419` `def restore(self, path)` -- Restore one archive as a NEW task; returns the new task id.
- `TaskArchive.stats` (method) `modules/lazy_loop.py:8486` `def stats(self)` -- Aggregate counts across archives like archive aggregate stats.
- `TaskTemplate.__init__` (method) `modules/lazy_loop.py:8495` `def __init__(self)` -- Bind template table.
- `TaskTemplate.list` (method) `modules/lazy_loop.py:8503` `def list(self)` -- Return all templates.
- `TaskTemplate.add` (method) `modules/lazy_loop.py:8507` `def add(self, name, goal)` -- Register a template; names are unique (overwrite on clash).
- `TaskTemplate.remove` (method) `modules/lazy_loop.py:8517` `def remove(self, name)` -- Delete a template by name.
- `TaskTemplate.get` (method) `modules/lazy_loop.py:8527` `def get(self, name)` -- Return one template by name or None.
- `TaskCategory.__init__` (method) `modules/lazy_loop.py:8538` `def __init__(self, store)` -- Bind optional task store.
- `TaskCategory.set` (method) `modules/lazy_loop.py:8543` `def set(self, task_id, category)` -- Label a task; returns the mapping.
- `TaskCategory.get` (method) `modules/lazy_loop.py:8550` `def get(self, task_id)` -- Return the category for a task or empty string.
- `TaskCategory.list` (method) `modules/lazy_loop.py:8554` `def list(self, category)` -- Return task->category rows, optionally filtered.
- `TaskChat.say` (method) `modules/lazy_loop.py:8569` `def say(self, task_id, text, pool, session)` -- Append a human turn and answer from task context; returns both.
- `TaskChat.log` (method) `modules/lazy_loop.py:8612` `def log(self, task_id, limit, session)` -- Return recent conversation turns, optionally one session only.
- `TaskChat.sessions` (method) `modules/lazy_loop.py:8628` `def sessions(self, task_id)` -- Return session names active in a task.
- `TaskChat.clear` (method) `modules/lazy_loop.py:8637` `def clear(self, task_id, session)` -- Drop one session's turns, or the whole log when session is empty.
- `LazyLoopEngine.__init__` (method) `modules/lazy_loop.py:8692` `def __init__(self, shell)` -- Load shared stores.
- `LazyLoopEngine.apply_profile` (method) `modules/lazy_loop.py:8727` `def apply_profile(self, name)` -- Apply one orchestrator profile to this engine.
- `LazyLoopEngine.bind_shell` (method) `modules/lazy_loop.py:8768` `def bind_shell(self, shell)` -- Attach the live shell so workers route auto/addon verbs via it.
- `LazyLoopEngine.ensure_target` (method) `modules/lazy_loop.py:8852` `def ensure_target(self, task_id, target, reason)` -- Register scope + asset for target like lazy_scope/lazy_asset.
- `LazyLoopEngine.orchestrate` (method) `modules/lazy_loop.py:8879` `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` -- Single entry for lazy_loop + auto_loop: create, scope, run, report.
- `LazyLoopEngine.create_task` (method) `modules/lazy_loop.py:8907` `def create_task(self, goal, description)` -- Create task, decompose goals, register scope, return summary.
- `LazyLoopEngine.spawn_task` (method) `modules/lazy_loop.py:8936` `def spawn_task(self, goal, source_task_ids, description)` -- Create a task read-only inheriting assets and findings.
- `LazyLoopEngine.list_tasks` (method) `modules/lazy_loop.py:8986` `def list_tasks(self)` -- Fleet view: every task with live intent/fact/finding counters.
- `LazyLoopEngine.pause_task` (method) `modules/lazy_loop.py:9014` `def pause_task(self, task_id, reason)` -- Pause another task from here (cross-task control).
- `LazyLoopEngine.resume_task` (method) `modules/lazy_loop.py:9025` `def resume_task(self, task_id)` -- Resume a paused task from here (cross-task control).
- `LazyLoopEngine.task_graph` (method) `modules/lazy_loop.py:9035` `def task_graph(self, task_id)` -- Graph overview of another task (get_task_graph parity).
- `LazyLoopEngine.task_findings` (method) `modules/lazy_loop.py:9041` `def task_findings(self, task_id)` -- Findings of another task with severity, status and report size.
- `LazyLoopEngine.task_traces` (method) `modules/lazy_loop.py:9060` `def task_traces(self, task_id, query, limit)` -- Worker traces of another task, keyword-filtered when asked.
- `LazyLoopEngine.task_node_detail` (method) `modules/lazy_loop.py:9069` `def task_node_detail(self, task_id, node_id)` -- Full node view of another task (get_task_node_detail parity).
- `LazyLoopEngine.update_finding_report` (method) `modules/lazy_loop.py:9075` `def update_finding_report(self, task_id, finding_id, report)` -- Write the narrative report of another task's finding.
- `LazyLoopEngine.broadcast_events` (method) `modules/lazy_loop.py:9087` `def broadcast_events(self, task_id, cursor, batch)` -- Return activity records after a line cursor (SSE resume parity).
- `LazyLoopEngine.add_hint` (method) `modules/lazy_loop.py:9120` `def add_hint(self, task_id, text)` -- Inject human steering hint read by the next planner round.
- `LazyLoopEngine.add_intent` (method) `modules/lazy_loop.py:9138` `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` -- Directly inject high-priority intent like the planner main-agent add_intent.
- `LazyLoopEngine.set_goals` (method) `modules/lazy_loop.py:9163` `def set_goals(self, task_id, specs)` -- Replace/append decomposed objectives like set_goals; wakes the task.
- `LazyLoopEngine.edit_goal` (method) `modules/lazy_loop.py:9180` `def edit_goal(self, task_id, goal_id, text)` -- Edit a goal node like the goals manager.
- `LazyLoopEngine.delete_goal` (method) `modules/lazy_loop.py:9192` `def delete_goal(self, task_id, goal_id)` -- Delete a goal node; done tasks with no goals left stay done.
- `LazyLoopEngine.preview_delete_intent` (method) `modules/lazy_loop.py:9203` `def preview_delete_intent(self, task_id, intent_id)` -- Estimate hard-delete cascade without mutating anything.
- `LazyLoopEngine.delete_intent` (method) `modules/lazy_loop.py:9226` `def delete_intent(self, task_id, intent_id, mode, reason)` -- Delete an intent in soft (fake) or hard (true) mode.
- `LazyLoopEngine.pause_intent` (method) `modules/lazy_loop.py:9371` `def pause_intent(self, task_id, intent_id)` -- Pause a runnable intent like the lazy worker interrupt.
- `LazyLoopEngine.resume_intent` (method) `modules/lazy_loop.py:9396` `def resume_intent(self, task_id, intent_id)` -- Resume a paused intent back to the claimable queue.
- `LazyLoopEngine.send_worker_message` (method) `modules/lazy_loop.py:9419` `def send_worker_message(self, task_id, intent_id, message, request_id)` -- Continue a paused worker intent with a human message.
- `LazyLoopEngine.goal_met` (method) `modules/lazy_loop.py:9467` `def goal_met(self, task_id, reason)` -- Declare the whole task complete like goal_met (weighted, audited).
- `LazyLoopEngine.record_fact` (method) `modules/lazy_loop.py:9477` `def record_fact(self, task_id, text, evidence, intent_id)` -- Operator-visible fact write like recordFact.
- `LazyLoopEngine.record_verdict` (method) `modules/lazy_loop.py:9484` `def record_verdict(self, task_id, finding_id, verdict, note)` -- Record an operator retest verdict on one finding.
- `LazyLoopEngine.run_round` (method) `modules/lazy_loop.py:9634` `def run_round(self, task_id, workers, executor, pool)` -- Run one orchestrated round invoking every subsystem in order.
- `stage_enabled` (function) `modules/lazy_loop.py:9685` `def stage_enabled(_name)`
- `LazyLoopEngine.run` (method) `modules/lazy_loop.py:10139` `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` -- Drive rounds until goals met, frontier drains, or budget exhausts.
- `LazyLoopEngine.prove_goal` (method) `modules/lazy_loop.py:10418` `def prove_goal(self, task_id, goal_id, evidence_id, reason)` -- Mark goal met with finding/fact evidence like the planner prove_goal.
- `LazyLoopEngine.delete_task` (method) `modules/lazy_loop.py:10567` `def delete_task(self, task_id)` -- Delete a task record plus every store file scoped to it.
- `LazyLoopEngine.proxy_start` (method) `modules/lazy_loop.py:10601` `def proxy_start(self, host, port, task_id, trust, upstream)` -- Start the shared recorder proxy and apply its trust environment.
- `LazyLoopEngine.proxy_stop` (method) `modules/lazy_loop.py:10637` `def proxy_stop(self)` -- Stop the recorder proxy and clear its trust environment.
- `LazyLoopEngine.proxy_status` (method) `modules/lazy_loop.py:10645` `def proxy_status(self)` -- Return recorder proxy state (running, address, CA, exchanges).
- `LazyLoopEngine.proxy_env` (method) `modules/lazy_loop.py:10651` `def proxy_env(self)` -- Return the environment overrides that route tools via proxy.
- `LazyLoopEngine.set_concurrency` (method) `modules/lazy_loop.py:10660` `def set_concurrency(self, limit)` -- Cap concurrently running tasks; 0 disables admission control.
- `LazyLoopEngine.admission_check` (method) `modules/lazy_loop.py:10681` `def admission_check(self, task_id)` -- Return whether a task may run now, queueing it when capped.
- `LazyLoopEngine.drain_queue` (method) `modules/lazy_loop.py:10700` `def drain_queue(self, max_tasks)` -- Run queued tasks FIFO while the concurrency cap allows.
- `LazyLoopEngine.ingest_proxy_traffic` (method) `modules/lazy_loop.py:10728` `def ingest_proxy_traffic(self, task_id, limit)` -- Mirror new recorder exchanges into the task traffic log.
- `LazyLoopEngine.search_proxy_body` (method) `modules/lazy_loop.py:10782` `def search_proxy_body(self, task_id, query, limit)` -- Full-text search proxy bodies scoped to one task's exchanges.
- `LazyLoopEngine.export_task_traffic` (method) `modules/lazy_loop.py:10874` `def export_task_traffic(self, task_id)` -- Export the task's proxy exchanges next to its archive.
- `LazyLoopEngine.export_evidence` (method) `modules/lazy_loop.py:10903` `def export_evidence(self, task_id, dest)` -- Freeze every task artefact into a hash-manifested zip package.
- `LazyLoopEngine.export_findings_report` (method) `modules/lazy_loop.py:10962` `def export_findings_report(self, task_id, path, fmt)` -- Render the severity-ranked report to Markdown, JSON or CSV.
- `LazyLoopEngine.status` (method) `modules/lazy_loop.py:11077` `def status(self, task_id)` -- Return full inspectable state for one task.
- `LazyLoopEngine.graph_overview` (method) `modules/lazy_loop.py:11097` `def graph_overview(self, task_id)` -- Return planner-facing overview plus coverage and scope.
- `LazyLoopEngine.broadcast` (method) `modules/lazy_loop.py:11159` `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` -- Paginated exploration timeline like the lazy broadcast board.
- `LazyLoopEngine.loop_graph` (method) `modules/lazy_loop.py:11283` `def loop_graph(self, task_id)` -- Return task graphs as ForceGraph-ready nodes/links.
- `LazyLoopEngine.graph_context` (method) `modules/lazy_loop.py:11352` `def graph_context(self, task_id, top)` -- Rank exploration topology to steer planner actions.

## modules/lazy_match_policy.py
Depends on: `modules/lazy_heat.py`
Imported by: `tests/test_lazy_match_policy.py`
- `strand_from_sighting` (function) `modules/lazy_match_policy.py:37` `def strand_from_sighting(sighting)` -- Classify one product sighting per the doctrine.
- `is_os_sighting` (function) `modules/lazy_match_policy.py:79` `def is_os_sighting(product, cpe)` -- Return True when the sighting names an operating system.
- `strand_rank` (function) `modules/lazy_match_policy.py:102` `def strand_rank(strand)` -- Return the merge precedence of a strand.
- `has_standing` (function) `modules/lazy_match_policy.py:107` `def has_standing(match)` -- Return True when humans or durable evidence touched a match.
- `MatchStore.__init__` (method) `modules/lazy_match_policy.py:127` `def __init__(self, sessions_dir)` -- Bind the store file under sessions/lazy.
- `MatchStore.upsert` (method) `modules/lazy_match_policy.py:132` `def upsert(self, identity, sighting, now)` -- Record one sighting under the dedupe identity.
- `MatchStore.rows` (method) `modules/lazy_match_policy.py:177` `def rows(self)` -- Return every stored row.
- `MatchStore.close` (method) `modules/lazy_match_policy.py:181` `def close(self, identity, reason, now)` -- Close one row, keeping its reason and reopening block.
- `MatchStore.closed_reason` (method) `modules/lazy_match_policy.py:196` `def closed_reason(self, identity)` -- Return the persisted closure reason, or '' when open or unknown.

## modules/lazy_mentions.py
Depends on: `modules/lazy_loop.py`
Imported by: `cli/commands/lazyloop.py`, `lazyc2.py`, `skills/lazyown_mcp.py`, `tests/test_security_codeql_batch.py`
- `search_mentions_page` (function) `modules/lazy_mentions.py:193` `def search_mentions_page(kind, query, cursor)` -- Search one scroll page of mention candidates.
- `parse_mentions` (function) `modules/lazy_mentions.py:237` `def parse_mentions(message)` -- Parse @[kind#id] tokens trusting type plus numeric id only.
- `compose_message` (function) `modules/lazy_mentions.py:268` `def compose_message(message)` -- Append server-read snapshots for referenced records as data.

## modules/lazy_netattack.py
Imported by: `tests/test_lazy_netattack.py`
- `AttackVectorVerdict.as_dict` (method) `modules/lazy_netattack.py:107` `def as_dict(self)` -- Return one JSON-safe view.
- `surface_decision` (function) `modules/lazy_netattack.py:184` `def surface_decision(evidence)` -- Grade the Windows network-attack families from evidence bags.
- `hint_text` (function) `modules/lazy_netattack.py:311` `def hint_text(verdict)` -- Shape one loop hint line for a verdict.

## modules/lazy_oob.py
Depends on: `modules/backdoor/server.c`
- `OobHit.as_dict` (method) `modules/lazy_oob.py:51` `def as_dict(self)` -- Return the JSON-serialisable row.
- `_CanaryHandler.do_GET` (method) `modules/lazy_oob.py:92` `def do_GET(self)` -- Record a GET callback.
- `_CanaryHandler.do_POST` (method) `modules/lazy_oob.py:97` `def do_POST(self)` -- Record a POST callback (body discarded).
- `_CanaryHandler.do_HEAD` (method) `modules/lazy_oob.py:102` `def do_HEAD(self)` -- Record a HEAD callback.
- `_CanaryHandler.log_message` (method) `modules/lazy_oob.py:107` `def log_message(self, fmt)` -- Silence the default stderr access log.
- `record_hit` (function) `modules/lazy_oob.py:112` `def record_hit(hit)` -- Store one hit in memory and append it to the JSONL mirror.
- `start` (function) `modules/lazy_oob.py:128` `def start(host, port)` -- Start (or reuse) the canary listener.
- `new_token` (function) `modules/lazy_oob.py:167` `def new_token()` -- Return one URL-safe callback token.
- `url` (function) `modules/lazy_oob.py:184` `def url(token)` -- Return the callback URL for a token (latest when omitted).
- `hits` (function) `modules/lazy_oob.py:204` `def hits(token)` -- Return recorded hits, optionally filtered by token.
- `stop` (function) `modules/lazy_oob.py:220` `def stop()` -- Shut the canary down and report how many hits it saw.
- `reset` (function) `modules/lazy_oob.py:241` `def reset()` -- Clear recorded hits and stop the listener (operator/test utility).
- `is_running` (function) `modules/lazy_oob.py:249` `def is_running()` -- Return whether the canary listener is alive.

## modules/lazy_orchestrator_feedback.py
Depends on: `modules/lazy_cli_bridge.py`, `modules/lazy_intel.py`
Imported by: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/mediation/feedback_mediator.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`
- `adjust_from_usage` (function) `modules/lazy_orchestrator_feedback.py:61` `def adjust_from_usage(limit)` -- Fold routing outcomes into per-(phase, stack, verb) success priors.
- `verb_prior` (function) `modules/lazy_orchestrator_feedback.py:162` `def verb_prior(phase, verb, stack)` -- Return the success prior for one (phase, stack, verb) triple.
- `rank_verbs` (function) `modules/lazy_orchestrator_feedback.py:189` `def rank_verbs(phase, verbs, stack)` -- Order verbs by learned success rate, stable for cold verbs.
- `order_steps` (function) `modules/lazy_orchestrator_feedback.py:213` `def order_steps(steps, stack)` -- Reorder resolved step lines by stack-aware verb priors.
- `export_dataset` (function) `modules/lazy_orchestrator_feedback.py:238` `def export_dataset(out, limit)` -- Export instruction-tuning rows joined from decisions + outcomes.

## modules/lazy_osinfer.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/world_model.py`
- `infer_from_ttl` (function) `modules/lazy_osinfer.py:47` `def infer_from_ttl(ttl)` -- Infer the remote OS family from a reply's TTL value.
- `infer_from_ping_output` (function) `modules/lazy_osinfer.py:72` `def infer_from_ping_output(output)` -- Read ``ttl=``/``TTL=`` from ping output and classify the OS.
- `infer_from_banner` (function) `modules/lazy_osinfer.py:97` `def infer_from_banner(text)` -- Infer the OS family from service names or banner text.
- `merge_os` (function) `modules/lazy_osinfer.py:118` `def merge_os(current, new)` -- Merge two inferred OS hints; a confident value wins.
- `addon_target_os` (function) `modules/lazy_osinfer.py:130` `def addon_target_os(name)` -- Return the ``os:`` field of one lazyaddon manifest.
- `verb_target_os` (function) `modules/lazy_osinfer.py:157` `def verb_target_os(command)` -- Return the OS family one command line targets.
- `os_compatible` (function) `modules/lazy_osinfer.py:194` `def os_compatible(verb_os, host_os)` -- Whether a verb's target OS may run against a host's inferred OS.
- `verb_compatible_with_host` (function) `modules/lazy_osinfer.py:216` `def verb_compatible_with_host(command, host_os)` -- Gate one command line against a host's inferred OS.
- `host_os_for_target` (function) `modules/lazy_osinfer.py:239` `def host_os_for_target(target)` -- Return the remembered OS for one target host.
- `remember_host_os` (function) `modules/lazy_osinfer.py:287` `def remember_host_os(target, os_name, reason)` -- Persist an inferred OS on the asset graph and world model.
- `learn_from_transcripts` (function) `modules/lazy_osinfer.py:330` `def learn_from_transcripts(target, transcripts)` -- Infer and remember the host OS from executed step outputs.


Next: [API_p15.md](API_p15.md)
