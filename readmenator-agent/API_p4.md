# API (page 4 of 20)
Previous: [API_p3.md](API_p3.md)

## cli/lazynmap_post.py
Depends on: `cli/exploration.py`, `cli/recon_plan.py`
Imported by: `cli/commands/recon.py`, `lazyown.py`, `tests/test_lazynmap_post.py`
- `PostScanResult.run_post_scan` (method) `cli/lazynmap_post.py:94` `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` -- Generate the plan, bump the world model and emit an event.

## cli/marketplace_config.py
Imported by: `cli/commands/marketplace.py`, `cli/wizard.py`
- `AddonInfo.from_yaml` (method) `cli/marketplace_config.py:144` `def from_yaml(cls, path)`
- `AddonInfo.toggle_enabled` (method) `cli/marketplace_config.py:164` `def toggle_enabled(self)` -- Flip the enabled state on disk.
- `AddonInfo.set_enabled` (method) `cli/marketplace_config.py:168` `def set_enabled(self, enabled)` -- Set the enabled state and persist to disk.
- `AddonInfo.save_yaml` (method) `cli/marketplace_config.py:185` `def save_yaml(self, data)` -- Rewrite the YAML file with the given data dictionary.
- `AddonRegistry.__init__` (method) `cli/marketplace_config.py:220` `def __init__(self)`
- `AddonRegistry.scan` (method) `cli/marketplace_config.py:235` `def scan(self, tab)`
- `AddonRegistry.rescan` (method) `cli/marketplace_config.py:334` `def rescan(self, tab)`
- `AddonRegistry.tab_order` (method) `cli/marketplace_config.py:338` `def tab_order(self)`
- `AddonRegistry.tab_label` (method) `cli/marketplace_config.py:341` `def tab_label(self, tab)`
- `AddonRegistry.tab_count` (method) `cli/marketplace_config.py:344` `def tab_count(self, tab)`
- `MarketplaceSettings.is_enabled` (method) `cli/marketplace_config.py:354` `def is_enabled(self, kind, name)`
- `MarketplaceSettings.toggle` (method) `cli/marketplace_config.py:357` `def toggle(self, addon)`
- `MarketplaceSettings.enable_all` (method) `cli/marketplace_config.py:367` `def enable_all(self, addons)`
- `MarketplaceSettings.disable_all` (method) `cli/marketplace_config.py:372` `def disable_all(self, addons)`
- `MarketplaceConfigurator.__init__` (method) `cli/marketplace_config.py:381` `def __init__(self, config, registry, initial)`
- `MarketplaceConfigurator.run` (method) `cli/marketplace_config.py:395` `def run(self, start_tab)`
- `MarketplaceConfigurator.configure_marketplace_interactive` (method) `cli/marketplace_config.py:751` `def configure_marketplace_interactive(config, start_tab)` -- Open the multi-tab curses wizard for marketplace management.
- `MarketplaceConfigurator.marketplace_summary` (method) `cli/marketplace_config.py:784` `def marketplace_summary(registry)` -- Return a text summary of enabled/disabled addons across all tabs.

## cli/ops_commands.py
Depends on: `core/console.py`, `modules/killchain.py`, `modules/world_model.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_killchain_unified.py`, `tests/test_ops_loot_phase.py`
- `print_ctx` (function) `cli/ops_commands.py:74` `def print_ctx(payload, sessions_dir)` -- Print a single-line operator context summary.
- `tgrep` (function) `cli/ops_commands.py:115` `def tgrep(pattern)` -- Search past command outputs and session logs for ``pattern``.
- `read_phase` (function) `cli/ops_commands.py:279` `def read_phase()` -- Return the current kill-chain phase from the unified killchain module.
- `write_phase` (function) `cli/ops_commands.py:302` `def write_phase(phase)` -- Set the current kill-chain phase via the unified killchain module.
- `print_phase` (function) `cli/ops_commands.py:317` `def print_phase()` -- Print the current phase and the full kill-chain progress bar.
- `phase_progress` (function) `cli/ops_commands.py:392` `def phase_progress(world, sessions_dir)` -- Return per-phase completion ratios from the unified kill-chain progress.
- `note_add` (function) `cli/ops_commands.py:467` `def note_add(text, rhost, phase)` -- Append a timestamped operator note to sessions/notes.jsonl.
- `note_list` (function) `cli/ops_commands.py:492` `def note_list(rhost, limit)` -- Print recent operator notes, optionally filtered by rhost.
- `LootEntry.value` (method) `cli/ops_commands.py:560` `def value(self)` -- Return the canonical ``user:secret`` credential value.
- `LootEntry.gather_loot` (method) `cli/ops_commands.py:570` `def gather_loot(sessions_dir)` -- Parse every credentials*.txt and hash*.txt under ``sessions_dir``.
- `LootEntry.loot_show` (method) `cli/ops_commands.py:613` `def loot_show(sessions_dir)` -- Print a unified table of all captured credentials and hashes.
- `LootEntry.loot_search` (method) `cli/ops_commands.py:685` `def loot_search(query, sessions_dir)` -- Search captured loot for ``query`` across users and secrets.
- `LootEntry.loot_reuse` (method) `cli/ops_commands.py:762` `def loot_reuse(rhost, sessions_dir)` -- Suggest captured credentials worth trying against ``rhost``.
- `LootEntry.loot_graph` (method) `cli/ops_commands.py:846` `def loot_graph(sessions_dir)` -- Render the credential-centric view of the network graph.
- `LootEntry.resolve_cred_value` (method) `cli/ops_commands.py:916` `def resolve_cred_value(selector, entries)` -- Resolve a user/secret ``selector`` to a canonical credential value.
- `LootEntry.loot_mark` (method) `cli/ops_commands.py:944` `def loot_mark(selector, outcome, host, sessions_dir)` -- Record that a credential worked or was rejected against ``host``.
- `LootEntry.pivot_add` (method) `cli/ops_commands.py:986` `def pivot_add(new_ip, via_ip, note)` -- Record a newly discovered pivot target.
- `LootEntry.pivot_list` (method) `cli/ops_commands.py:1012` `def pivot_list()` -- Print the pivot chain discovered so far.
- `LootEntry.tasks_list` (method) `cli/ops_commands.py:1069` `def tasks_list(status_filter, limit)` -- Print tasks from sessions/tasks.json.
- `LootEntry.tasks_add` (method) `cli/ops_commands.py:1124` `def tasks_add(title, operator)` -- Append a new task to sessions/tasks.json.
- `LootEntry.tasks_done` (method) `cli/ops_commands.py:1145` `def tasks_done(task_id)` -- Mark a task as Done.
- `LootEntry.tasks_start` (method) `cli/ops_commands.py:1165` `def tasks_start(task_id)` -- Mark a task as Started.
- `LootEntry.scans_list` (method) `cli/ops_commands.py:1188` `def scans_list(rhost, sessions_dir)` -- List nmap scan files in sessions/, optionally filtered by rhost.
- `LootEntry.sitrep` (method) `cli/ops_commands.py:1241` `def sitrep(payload, sessions_dir)` -- Print a unified operational situation report.

## cli/output_mode.py
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/ux.py`
- `OutputMode.parse_output_flags` (method) `cli/output_mode.py:43` `def parse_output_flags(args, config)` -- Split output control flags from positional command arguments.
- `OutputMode.strip_ansi` (method) `cli/output_mode.py:65` `def strip_ansi(text)` -- Remove ANSI escape sequences from text.
- `OutputMode.format_output` (method) `cli/output_mode.py:77` `def format_output(data, mode)` -- Render data according to the parsed output mode.
- `OutputMode.dry_run_line` (method) `cli/output_mode.py:98` `def dry_run_line(command)` -- Render the exact shell line that would run without running it.

## cli/palette.py
Imported by: `cli/command_explorer.py`, `cli/command_form.py`, `cli/commands/misc_migrated.py`, `cli/contextual_help.py`, `cli/engagement_hooks.py`, `cli/palette_overlay.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_palette.py`
- `CommandIndexError.load_index` (method) `cli/palette.py:30` `def load_index(path)` -- Return the parsed catalogue as a dict.
- `CommandIndexError.all_commands` (method) `cli/palette.py:55` `def all_commands()` -- Return every command entry, sorted by name.
- `CommandIndexError.all_phases` (method) `cli/palette.py:72` `def all_phases()` -- Return the sorted list of phase identifiers present in the index.
- `CommandIndexError.all_categories` (method) `cli/palette.py:77` `def all_categories()` -- Return the sorted list of cmd2 category labels present in the index.
- `CommandIndexError.filter_by_phase` (method) `cli/palette.py:82` `def filter_by_phase(phase)` -- Return command entries whose ``phase`` matches ``phase``.
- `CommandIndexError.filter_by_category` (method) `cli/palette.py:92` `def filter_by_category(category)` -- Return command entries with the given cmd2 category label.
- `CommandIndexError.search` (method) `cli/palette.py:97` `def search(query)` -- Substring search over ``name`` and ``summary`` (case-insensitive).
- `CommandIndexError.get` (method) `cli/palette.py:114` `def get(name)` -- Return the canonical entry for ``name`` or ``None`` if unknown.
- `CommandIndexError.duplicates` (method) `cli/palette.py:125` `def duplicates()` -- Return the duplicate-method audit list as stored in the index.
- `CommandIndexError.totals` (method) `cli/palette.py:130` `def totals()` -- Return the ``totals`` block (counts of methods, unique names, ...).

## cli/palette_command.py
Depends on: `cli/commands/enum.py`, `cli/palette_graph.py`, `cli/palette_telemetry.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/palette_overlay.py`, `lazyc2.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_palette.py`
- `PaletteRenderConfig.truncate_summary` (method) `cli/palette_command.py:107` `def truncate_summary(self, summary)` -- Trim ``summary`` to :attr:`summary_max_chars` with marker suffix.
- `PaletteArgumentParser.__init__` (method) `cli/palette_command.py:149` `def __init__(self, config)`
- `PaletteArgumentParser.parse` (method) `cli/palette_command.py:152` `def parse(self, line)` -- Return a :class:`PaletteArgs` for ``line``.
- `PaletteIndexQuery.__init__` (method) `cli/palette_command.py:193` `def __init__(self, index)`
- `PaletteIndexQuery.commands` (method) `cli/palette_command.py:197` `def commands(self)` -- Return canonical (non-duplicate) command entries.
- `PaletteIndexQuery.phases` (method) `cli/palette_command.py:203` `def phases(self)` -- Return the sorted list of phase identifiers in the index.
- `PaletteIndexQuery.phase_counts` (method) `cli/palette_command.py:208` `def phase_counts(self)` -- Return ``{phase: command_count}`` for every phase in the index.
- `PaletteIndexQuery.in_phase` (method) `cli/palette_command.py:213` `def in_phase(self, phase)` -- Return commands whose ``phase`` matches ``phase`` (case-insensitive).
- `PaletteIndexQuery.search` (method) `cli/palette_command.py:218` `def search(self, query)` -- Substring search over ``name`` and ``summary`` (case-insensitive).
- `PaletteIndexQuery.detail` (method) `cli/palette_command.py:234` `def detail(self, target)` -- Return the canonical entry for ``target`` or ``None``.
- `PaletteIndexQuery.next_phase` (method) `cli/palette_command.py:249` `def next_phase(self, current)` -- Return the phase that comes after ``current`` in ``ordering``.
- `PaletteRenderer.__init__` (method) `cli/palette_command.py:285` `def __init__(self, config)`
- `PaletteRenderer.render_overview` (method) `cli/palette_command.py:288` `def render_overview(self, phase_counts)` -- Format the multi-phase overview table.
- `PaletteRenderer.render_phase` (method) `cli/palette_command.py:304` `def render_phase(self, phase, rows)` -- Format a phase listing of ``(name, summary)`` pairs.
- `PaletteRenderer.render_search` (method) `cli/palette_command.py:312` `def render_search(self, query, rows)` -- Format the cross-phase search result table.
- `PaletteRenderer.render_detail` (method) `cli/palette_command.py:320` `def render_detail(self, entry)` -- Format the detail view for a single command entry.
- `PaletteRenderer.render_next` (method) `cli/palette_command.py:360` `def render_next(self, phase, rows)` -- Format the recommended-next-phase listing.
- `PaletteRenderer.render` (method) `cli/palette_command.py:447` `def render(index, line)` -- Top-level entry point used by :class:`LazyOwnShell.do_palette`.
- `PaletteJsonResult.to_dict` (method) `cli/palette_command.py:502` `def to_dict(self)` -- Serialise to a plain ``dict`` suitable for ``json.dumps``.
- `PaletteJsonRenderer.__init__` (method) `cli/palette_command.py:522` `def __init__(self, config)`
- `PaletteJsonRenderer.render_overview` (method) `cli/palette_command.py:525` `def render_overview(self, phase_counts)` -- Build a result document for overview mode.
- `PaletteJsonRenderer.render_phase` (method) `cli/palette_command.py:532` `def render_phase(self, phase, query, rows)` -- Build a result document for phase mode.
- `PaletteJsonRenderer.render_search` (method) `cli/palette_command.py:541` `def render_search(self, query, rows)` -- Build a result document for search mode.
- `PaletteJsonRenderer.render_detail` (method) `cli/palette_command.py:549` `def render_detail(self, target, entry)` -- Build a result document for detail mode.
- `PaletteJsonRenderer.render_next` (method) `cli/palette_command.py:557` `def render_next(self, phase, rows)` -- Build a result document for next-phase mode.
- `PaletteJsonRenderer.render_json` (method) `cli/palette_command.py:566` `def render_json(index, line)` -- Structured-data variant of :func:`render`.
- `PaletteViewConfig.build_palette_view` (method) `cli/palette_command.py:619` `def build_palette_view(index)` -- Assemble the template context consumed by the C2 ``/palette`` view.
- `PaletteCompleter.__init__` (method) `cli/palette_command.py:755` `def __init__(self, config)`
- `PaletteCompleter.complete` (method) `cli/palette_command.py:758` `def complete(self, text, line, endidx, index)` -- Return tab-completion candidates given the editor state.

## cli/palette_graph.py
Imported by: `cli/palette_command.py`, `tests/test_command_palette.py`
- `GraphIndex.load_graph` (method) `cli/palette_graph.py:127` `def load_graph(path)` -- Return the parsed graph index, cached per resolved path.
- `GraphIndex.safe_load_graph` (method) `cli/palette_graph.py:149` `def safe_load_graph(path)` -- Best-effort variant of :func:`load_graph`.
- `GraphIndex.callees` (method) `cli/palette_graph.py:179` `def callees(graph, command_name)` -- Return helper-function labels invoked by ``command_name``.
- `GraphIndex.related_commands` (method) `cli/palette_graph.py:226` `def related_commands(graph, command_name)` -- Return ``do_*`` commands that share helper functions with this one.
- `GraphIndex.enrich_detail` (method) `cli/palette_graph.py:287` `def enrich_detail(graph, entry)` -- Attach ``calls`` and ``related`` lists to a palette detail entry.
- `GraphIndex.enrich_commands` (method) `cli/palette_graph.py:309` `def enrich_commands(graph, rows)` -- Enrich every entry of ``rows`` with neighbour data.

## cli/palette_overlay.py
Depends on: `cli/commands/containers.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_telemetry.py`, `cli/themes.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_palette_overlay.py`
- `PaletteOverlayState.set_query` (method) `cli/palette_overlay.py:83` `def set_query(self, value)` -- Replace the active query with ``value`` (trimmed).
- `PaletteOverlayState.rows` (method) `cli/palette_overlay.py:87` `def rows(self)` -- Return the ranked, truncated rows for the current query.
- `PaletteOverlayState.build_state` (method) `cli/palette_overlay.py:162` `def build_state(payload, index, recents, config)` -- Wire the canonical state used by :func:`launch_overlay`.
- `PaletteOverlayState.launch_overlay` (method) `cli/palette_overlay.py:188` `def launch_overlay(payload, state, runner)` -- Open the Textual overlay and return the selected command verb.
- `_PaletteOverlayApp.__init__` (method) `cli/palette_overlay.py:255` `def __init__(self)`
- `_PaletteOverlayApp.compose` (method) `cli/palette_overlay.py:261` `def compose(self)`
- `_PaletteOverlayApp.on_mount` (method) `cli/palette_overlay.py:269` `def on_mount(self)`
- `_PaletteOverlayApp.on_input_changed` (method) `cli/palette_overlay.py:272` `def on_input_changed(self, event)`
- `_PaletteOverlayApp.on_input_submitted` (method) `cli/palette_overlay.py:276` `def on_input_submitted(self, event)`
- `_PaletteOverlayApp.on_list_view_selected` (method) `cli/palette_overlay.py:279` `def on_list_view_selected(self, event)`
- `_PaletteOverlayApp.action_cancel` (method) `cli/palette_overlay.py:282` `def action_cancel(self)`
- `_PaletteOverlayApp.action_select_current` (method) `cli/palette_overlay.py:285` `def action_select_current(self)`

## cli/palette_telemetry.py
Imported by: `cli/palette_command.py`, `cli/palette_overlay.py`, `tests/test_command_palette.py`
- `TelemetryIndex.load_telemetry` (method) `cli/palette_telemetry.py:186` `def load_telemetry(path)` -- Return the parsed telemetry index, cached per resolved path.
- `TelemetryIndex.safe_load_telemetry` (method) `cli/palette_telemetry.py:204` `def safe_load_telemetry(path)` -- Best-effort variant of :func:`load_telemetry`.
- `TelemetryIndex.command_stats` (method) `cli/palette_telemetry.py:216` `def command_stats(telemetry, command_name)` -- Return aggregated stats for ``command_name`` or ``None`` when unseen.
- `TelemetryIndex.runs_after` (method) `cli/palette_telemetry.py:239` `def runs_after(telemetry, command_name)` -- Return commands that frequently run after ``command_name``.
- `TelemetryIndex.recents` (method) `cli/palette_telemetry.py:259` `def recents(telemetry)` -- Return the most-recently invoked unique ``do_*`` commands.
- `TelemetryIndex.enrich_detail` (method) `cli/palette_telemetry.py:275` `def enrich_detail(telemetry, entry)` -- Attach ``runs``, ``last_seen`` and ``runs_after`` to a detail entry.
- `TelemetryIndex.enrich_commands` (method) `cli/palette_telemetry.py:300` `def enrich_commands(telemetry, rows)` -- Enrich every entry of ``rows`` with telemetry data.

## cli/phase_labels.py
Imported by: `cli/contextual_help.py`, `cli/tips_engine.py`, `tests/test_phase_labels.py`
- `phase_label` (function) `cli/phase_labels.py:29` `def phase_label(phase)` -- Return the human label for a phase, falling back to title case.

## cli/plugin_tiers.py
Imported by: `cli/commands/marketplace.py`, `tests/test_input_fuzz.py`, `tests/test_plugin_tiers.py`
- `load_tier_manifest` (function) `cli/plugin_tiers.py:35` `def load_tier_manifest(manifest)` -- Load explicit tier overrides from a ``tiers.yaml`` manifest.
- `tier_of` (function) `cli/plugin_tiers.py:61` `def tier_of(name, manifest_tiers, metadata_tier)` -- Resolve the tier for a plugin name.
- `rate_plugin` (function) `cli/plugin_tiers.py:98` `def rate_plugin(name, stars, store)` -- Record an operator rating and return the new ``(average, count)``.
- `rating_summary` (function) `cli/plugin_tiers.py:121` `def rating_summary(name, store)` -- Return the ``(average, count)`` rating for a plugin name.
- `format_rating` (function) `cli/plugin_tiers.py:137` `def format_rating(average, count)` -- Render a compact rating label for list and info views.
- `default_store` (function) `cli/plugin_tiers.py:144` `def default_store(base_dir)` -- Return the default ratings file under ``<base_dir>/sessions``.
- `read_metadata_tier` (function) `cli/plugin_tiers.py:149` `def read_metadata_tier(path)` -- Read the optional ``tier:`` field from a plugin YAML file.

## cli/protips.py
Depends on: `cli/noise_verbs.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_reactive_hints_expanded.py`
- `ProTip.get_session_tip` (method) `cli/protips.py:301` `def get_session_tip(ctx)` -- Return a single tip to show at session start.
- `ProTip.render_contextual_tip` (method) `cli/protips.py:327` `def render_contextual_tip(last_cmd, ctx)` -- Print a single dim tip line when the last command triggers one.
- `ProTip.print_session_tip` (method) `cli/protips.py:357` `def print_session_tip(ctx)` -- Print the session-start tip (called once after the banner).

## cli/purple_tui.py
Depends on: `cli/commands/containers.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleDashboard.compose` (method) `cli/purple_tui.py:98` `def compose(self)`
- `PurpleDashboard.on_mount` (method) `cli/purple_tui.py:108` `def on_mount(self)`
- `PurpleDashboard.action_refresh` (method) `cli/purple_tui.py:112` `def action_refresh(self)`
- `PurpleDashboard.refresh_data` (method) `cli/purple_tui.py:115` `def refresh_data(self)`
- `PurpleDashboard.launch` (method) `cli/purple_tui.py:233` `def launch()` -- Launch the purple team dashboard TUI.

## cli/reactive_hints.py
Depends on: `cli/graph_advisor.py`, `cli/noise_verbs.py`, `core/console.py`, `core/logging.py`, `core/text_utils.py`
Imported by: `cli/command_chain.py`, `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/recommendation_signals.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_improvements_spec.py`, `tests/test_reactive_hints.py`, `tests/test_reactive_hints_expanded.py`
- `render_inline_hints` (function) `cli/reactive_hints.py:220` `def render_inline_hints(advisor, last_command, limit, enabled)` -- Print a single dim hint line below the command output and return immediately.
- `EvidenceHint.confidence_from_score` (method) `cli/reactive_hints.py:321` `def confidence_from_score(score)` -- Map an unbounded fused recommendation score to a 0-100 display confidence.
- `EvidenceHint.build_evidence_hints` (method) `cli/reactive_hints.py:362` `def build_evidence_hints(recommendations, limit)` -- Convert fused recommendations into display-ready evidence hints.
- `EvidenceHint.render_evidence_hints` (method) `cli/reactive_hints.py:400` `def render_evidence_hints(hints)` -- Print evidence-backed hint lines: verb, confidence, reason, provenance.
- `EvidenceHint.build_evidence_hint_lines` (method) `cli/reactive_hints.py:416` `def build_evidence_hint_lines(hints)` -- Build evidence-backed hint lines as Rich Text objects.
- `EvidenceHint.read_run_commands` (method) `cli/reactive_hints.py:443` `def read_run_commands(sessions_dir)` -- Return the set of command names already executed this session.
- `EvidenceHint.render_command_hints` (method) `cli/reactive_hints.py:514` `def render_command_hints(last_command, phase, sessions_dir, limit, enabled)` -- Print phase-aware, history-filtered command hints after each step.
- `EvidenceHint.command_hints` (method) `cli/reactive_hints.py:549` `def command_hints(last_command, phase, sessions_dir, limit)` -- Return the top next-step command verbs without printing them.

## cli/reasoning_stream.py
Depends on: `core/text_utils.py`
Imported by: `cli/dashboard_tui.py`, `tests/test_reasoning_stream.py`
- `ReasoningEntry.read_raw_events` (method) `cli/reasoning_stream.py:91` `def read_raw_events(path, limit)` -- Return the last ``limit`` well-formed events from the JSONL log.
- `ReasoningEntry.event_to_entry` (method) `cli/reasoning_stream.py:183` `def event_to_entry(event)` -- Convert a raw daemon event into a :class:`ReasoningEntry`.
- `ReasoningEntry.latest_reasoning` (method) `cli/reasoning_stream.py:216` `def latest_reasoning(path, limit)` -- Return the most recent daemon decisions as reasoning entries.

## cli/recommendation.py
Imported by: `cli/commands/misc_migrated.py`, `cli/recommendation_signals.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_gap_signal.py`, `tests/test_recommendation.py`
- `RecommendationSignal.propose` (method) `cli/recommendation.py:187` `def propose(self, ctx)` -- Return zero or more :class:`Proposal` objects for ``ctx``.
- `CategoryResolver.__init__` (method) `cli/recommendation.py:201` `def __init__(self, index_path, loader)` -- Build the resolver from the command index.
- `CategoryResolver.category_for` (method) `cli/recommendation.py:227` `def category_for(self, action)` -- Return the kill-chain category for ``action`` or an empty string.
- `RecommendationEngine.__init__` (method) `cli/recommendation.py:240` `def __init__(self, signals, resolver, weights)` -- Wire the engine with its signals and fusion parameters.
- `RecommendationEngine.recommend` (method) `cli/recommendation.py:258` `def recommend(self, ctx)` -- Return the fused, ranked recommendations for ``ctx``.
- `_Accumulator.add` (method) `cli/recommendation.py:374` `def add(self, source, contribution, proposal)` -- Fold one signal's proposal into the running total.
- `_Accumulator.build` (method) `cli/recommendation.py:386` `def build(self)` -- Freeze the slot into an immutable :class:`Recommendation`.

## cli/recommendation_signals.py
Depends on: `cli/exploration.py`, `cli/graph_advisor.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recon_plan.py`, `core/logging.py`, `modules/apt_playbooks.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `skills/lazyown_mcp.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_gap_signal.py`, `tests/test_phase1_data_gaps.py`, `tests/test_recommendation.py`
- `GraphSignal.__init__` (method) `cli/recommendation_signals.py:115` `def __init__(self, advisor)` -- Store the graph advisor facade.
- `GraphSignal.propose` (method) `cli/recommendation_signals.py:125` `def propose(self, ctx)` -- Return graph-adjacent command proposals for ``ctx``.
- `PolicySignal.__init__` (method) `cli/recommendation_signals.py:153` `def __init__(self, policy)` -- Store the policy integration facade.
- `PolicySignal.propose` (method) `cli/recommendation_signals.py:162` `def propose(self, ctx)` -- Return category-prior proposals for ``ctx``.
- `ReconPlanSignal.__init__` (method) `cli/recommendation_signals.py:190` `def __init__(self, engine, builder)` -- Store the exploration engine and the plan builder callable.
- `ReconPlanSignal.propose` (method) `cli/recommendation_signals.py:200` `def propose(self, ctx)` -- Return trigger-matched addon/tool/command proposals for ``ctx``.
- `KillChainSignal.__init__` (method) `cli/recommendation_signals.py:229` `def __init__(self, next_table, phase_table)` -- Store the adjacency and phase-priority tables.
- `KillChainSignal.propose` (method) `cli/recommendation_signals.py:243` `def propose(self, ctx)` -- Return adjacency- and phase-derived proposals for ``ctx``.
- `KillChainSignal.read_recent_commands` (method) `cli/recommendation_signals.py:275` `def read_recent_commands(sessions_dir, window)` -- Return the last ``window`` command verbs from the session transcript.
- `KillChainSignal.build_context` (method) `cli/recommendation_signals.py:308` `def build_context(payload, sessions_dir, target, limit)` -- Assemble a :class:`RecommendationContext` from live engagement state.
- `PlaybookSignal.__init__` (method) `cli/recommendation_signals.py:346` `def __init__(self, playbook_engine)` -- Store an optional playbook engine facade.
- `PlaybookSignal.propose` (method) `cli/recommendation_signals.py:355` `def propose(self, ctx)` -- Return playbook-based proposals for the current context.
- `KillchainGapSignal.__init__` (method) `cli/recommendation_signals.py:406` `def __init__(self, sessions_dir)`
- `KillchainGapSignal.propose` (method) `cli/recommendation_signals.py:409` `def propose(self, ctx)` -- Return gap-detection proposals for ``ctx``.
- `GraphTopologySignal.__init__` (method) `cli/recommendation_signals.py:542` `def __init__(self, sessions_dir)`
- `GraphTopologySignal.propose` (method) `cli/recommendation_signals.py:545` `def propose(self, ctx)` -- Return lateral movement and topology proposals from network graph.
- `GraphTopologySignal.build_default_engine` (method) `cli/recommendation_signals.py:649` `def build_default_engine(payload, sessions_dir, graph_path, command_index_path, weights)` -- Wire every available deterministic signal into one engine.
- `GraphTopologySignal.recommend_with_evidence` (method) `cli/recommendation_signals.py:705` `def recommend_with_evidence(payload, sessions_dir, target, phase, limit, engine)` -- Return fused, ranked recommendations carrying reason and score for display.

## cli/recon_plan.py
Depends on: `cli/exploration.py`, `modules/killchain.py`
Imported by: `cli/lazynmap_post.py`, `cli/recommendation_signals.py`, `tests/test_lazynmap_post.py`, `tests/test_recon_plan.py`
- `ReconPlan.is_empty` (method) `cli/recon_plan.py:139` `def is_empty(self)` -- Return ``True`` when the plan carries no actionable items.
- `ReconPlan.build_recon_plan` (method) `cli/recon_plan.py:144` `def build_recon_plan(target, engine, payload, config, command_index_loader, clock)` -- Assemble a :class:`ReconPlan` for ``target`` using ``engine``.
- `ReconPlan.render_markdown` (method) `cli/recon_plan.py:207` `def render_markdown(plan)` -- Render ``plan`` as a Markdown document suitable for sessions/.
- `ReconPlan.write_plan` (method) `cli/recon_plan.py:257` `def write_plan(plan, sessions_dir, config)` -- Persist ``plan`` to ``sessions/recon_plan_<target>.md`` atomically.
- `ReconPlan.render_rich` (method) `cli/recon_plan.py:299` `def render_rich(plan, console)` -- Render ``plan`` to the supplied Rich console.

## cli/registry.py
Depends on: `cli/commands/_dormancy.py`
Imported by: `cli/__init__.py`, `lazyown.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `iter_command_sets` (function) `cli/registry.py:41` `def iter_command_sets(include_pending)` -- Yield every ``CommandSet`` subclass found under ``cli.commands.*``.
- `register_command_sets` (function) `cli/registry.py:77` `def register_command_sets(shell)` -- Instantiate and register every active ``CommandSet`` on ``shell``.

## cli/scope_guard.py
Depends on: `cli/commands/enum.py`
Imported by: `lazyown.py`, `tests/test_scope_guard.py`
- `ScopeMode.from_value` (method) `cli/scope_guard.py:84` `def from_value(cls, value)` -- Coerce an arbitrary payload value into a :class:`ScopeMode`.
- `ScopeDecision.build_offensive_commands` (method) `cli/scope_guard.py:126` `def build_offensive_commands(command_categories)` -- Select the command names whose category is offensive.
- `ScopeDecision.normalize_scope` (method) `cli/scope_guard.py:142` `def normalize_scope(entries)` -- Coerce a scope specification into a tuple of entry strings.
- `ScopeDecision.target_in_scope` (method) `cli/scope_guard.py:197` `def target_in_scope(target, entries)` -- Return whether *target* falls within any of the scope *entries*.
- `ScopeGuard.__init__` (method) `cli/scope_guard.py:242` `def __init__(self, scope_entries, mode, is_offensive)` -- Initialise the guard.
- `ScopeGuard.evaluate` (method) `cli/scope_guard.py:262` `def evaluate(self, command, target)` -- Evaluate a single command against the active target.

## cli/session_hud.py
Depends on: `cli/engagement_hooks.py`
Imported by: `cli/commands/ux.py`
- `HudSnapshot.count_lines_in_globs` (method) `cli/session_hud.py:62` `def count_lines_in_globs(root, patterns)` -- Count non-empty lines across every file matching the patterns.
- `HudSnapshot.count_csv_rows` (method) `cli/session_hud.py:83` `def count_csv_rows(path)` -- Count data rows in a CSV file without loading it fully.
- `HudSnapshot.format_elapsed` (method) `cli/session_hud.py:100` `def format_elapsed(seconds)` -- Format a duration as HH:MM:SS.
- `HudSnapshot.phase_bar` (method) `cli/session_hud.py:115` `def phase_bar(phase, width)` -- Render kill-chain progress as filled and empty blocks.
- `HudSnapshot.build_snapshot` (method) `cli/session_hud.py:155` `def build_snapshot(params, config)` -- Build a snapshot from live params, engagement state and session files.
- `HudSnapshot.render_snapshot` (method) `cli/session_hud.py:180` `def render_snapshot(snapshot, config)` -- Render the session counters as two plain lines.

## cli/session_resumer.py
Depends on: `core/console.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`
- `SessionResumer.__init__` (method) `cli/session_resumer.py:58` `def __init__(self, config)`
- `SessionResumer.render_startup_panel` (method) `cli/session_resumer.py:129` `def render_startup_panel(self)` -- Render the resume panel and return the selected target IP, or None.

## cli/sessions_browser.py
Depends on: `cli/commands/containers.py`, `cli/themes.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_sessions_browser.py`
- `SessionsIndex.__init__` (method) `cli/sessions_browser.py:88` `def __init__(self, config, root)` -- Bind to config and resolve the sessions root.
- `SessionsIndex.root` (method) `cli/sessions_browser.py:100` `def root(self)` -- Return the resolved sessions root.
- `SessionsIndex.categories` (method) `cli/sessions_browser.py:104` `def categories(self)` -- Return a mapping ``category_identifier -> [SessionEntry, ...]``.
- `SessionPreview.__init__` (method) `cli/sessions_browser.py:188` `def __init__(self, config, root)` -- Bind to config and the sessions root.
- `SessionPreview.read` (method) `cli/sessions_browser.py:193` `def read(self, relative)` -- Return ``relative`` as text, capped at ``max_preview_bytes``.
- `SessionsBrowserState.grouped_entries` (method) `cli/sessions_browser.py:233` `def grouped_entries(self)` -- Return classified entries, optionally filtered by :attr:`filter_query`.
- `SessionsBrowserState.category_label` (method) `cli/sessions_browser.py:248` `def category_label(self, identifier)` -- Return the human-readable label for ``identifier``.
- `SessionsBrowserState.build_state` (method) `cli/sessions_browser.py:258` `def build_state(payload, sessions_dir, config)` -- Wire the canonical state used by :func:`launch_browser`.
- `SessionsBrowserState.launch_browser` (method) `cli/sessions_browser.py:281` `def launch_browser(payload, state, runner)` -- Open the Textual browser and return the last-viewed relative path.
- `_SessionsBrowserApp.__init__` (method) `cli/sessions_browser.py:340` `def __init__(self)`
- `_SessionsBrowserApp.compose` (method) `cli/sessions_browser.py:346` `def compose(self)`
- `_SessionsBrowserApp.on_mount` (method) `cli/sessions_browser.py:356` `def on_mount(self)`
- `_SessionsBrowserApp.on_input_changed` (method) `cli/sessions_browser.py:359` `def on_input_changed(self, event)`
- `_SessionsBrowserApp.on_tree_node_selected` (method) `cli/sessions_browser.py:363` `def on_tree_node_selected(self, event)`
- `_SessionsBrowserApp.action_refresh` (method) `cli/sessions_browser.py:370` `def action_refresh(self)`
- `_SessionsBrowserApp.action_close` (method) `cli/sessions_browser.py:373` `def action_close(self)`

## cli/show.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `static/js/bootstrap-4.5.2.min.js`, `static/js/bootstrap-5.3.0.bundle.min.js`, `static/js/chart.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/quill-2.0.3.js`, `static/js/tippy-6.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_cli_assign.py`
- `format_payload` (function) `cli/show.py:14` `def format_payload(params)` -- Render ``params`` as a sorted, aligned ``key = value`` block.

## cli/splash.py
Depends on: `cli/style.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_tui_splash.py`
- `SplashEffect.render` (method) `cli/splash.py:71` `def render(self, console, lines, tokens, config)`
- `TypewriterEffect.render` (method) `cli/splash.py:90` `def render(self, console, lines, tokens, config)`
- `InstantEffect.render` (method) `cli/splash.py:150` `def render(self, console, lines, tokens, config)`
- `InstantEffect.render_splash` (method) `cli/splash.py:166` `def render_splash(console, lines, payload, config, effect_name)` -- Render the splash overlay and optionally clear the screen.

## cli/status_bar.py
Depends on: `cli/reactive_hints.py`, `cli/themes.py`
Imported by: `lazyown.py`, `tests/test_improvements_spec.py`, `tests/test_status_bar_operators.py`
- `StatusBarConfig.from_payload` (method) `cli/status_bar.py:99` `def from_payload(cls, payload)` -- Return a config with overrides applied from a ``payload.json`` mapping.
- `IStatusSource.collect` (method) `cli/status_bar.py:146` `def collect(self)` -- Return the field value for this source as a plain string.
- `FileSystemReader.__init__` (method) `cli/status_bar.py:160` `def __init__(self, config, root)` -- Initialise with the active config and optional explicit root.
- `FileSystemReader.root` (method) `cli/status_bar.py:179` `def root(self)` -- Return the resolved root directory backing this reader.
- `FileSystemReader.read_text` (method) `cli/status_bar.py:183` `def read_text(self, relative)` -- Return the contents of ``relative`` truncated to ``max_file_bytes``.
- `FileSystemReader.read_json` (method) `cli/status_bar.py:204` `def read_json(self, relative)` -- Return parsed JSON from ``relative`` or ``None`` on failure.
- `FileSystemReader.glob_latest` (method) `cli/status_bar.py:222` `def glob_latest(self, pattern)` -- Return the most recently modified path matching ``pattern``.
- `PayloadTargetSource.__init__` (method) `cli/status_bar.py:271` `def __init__(self, config, payload)` -- Bind to the live config and a payload mapping.
- `PayloadTargetSource.collect` (method) `cli/status_bar.py:283` `def collect(self)` -- Return the first non-empty target key from ``payload.json``.
- `WorldModelPhaseSource.__init__` (method) `cli/status_bar.py:295` `def __init__(self, config, reader, payload)` -- Bind to config, sessions reader and payload mapping.
- `WorldModelPhaseSource.collect` (method) `cli/status_bar.py:306` `def collect(self)` -- Return the active phase from ``world_model.json`` then payload then default.
- `SessionFindingSource.__init__` (method) `cli/status_bar.py:322` `def __init__(self, config, reader)` -- Bind to config and sessions reader.
- `SessionFindingSource.collect` (method) `cli/status_bar.py:327` `def collect(self)` -- Return a short description of the freshest credential / vuln / note.
- `CommandHintSuggestionSource.__init__` (method) `cli/status_bar.py:426` `def __init__(self, config, reader, phase_provider, hint_provider)` -- Bind to config, reader and the current-phase callable.
- `CommandHintSuggestionSource.collect` (method) `cli/status_bar.py:451` `def collect(self)` -- Return the top kill-chain suggestion or the configured fallback.
- `GraphSuggestionSource.__init__` (method) `cli/status_bar.py:511` `def __init__(self, config, reader, advisor_factory)` -- Bind to config, reader, and an optional advisor factory.
- `GraphSuggestionSource.collect` (method) `cli/status_bar.py:530` `def collect(self)` -- Return a one-token suggestion.
- `CollabPresenceSource.__init__` (method) `cli/status_bar.py:601` `def __init__(self, config, reader, clock)` -- Bind to the active config, reader, and an injectable clock.
- `CollabPresenceSource.collect` (method) `cli/status_bar.py:622` `def collect(self)` -- Return the active-operator count formatted as a short string.
- `StatusBarRenderer.__init__` (method) `cli/status_bar.py:659` `def __init__(self, config)` -- Bind to the active configuration.
- `StatusBarRenderer.render_plain` (method) `cli/status_bar.py:664` `def render_plain(self, ctx)` -- Return the line without ANSI colour or readline markers.
- `StatusBarRenderer.render_prompt` (method) `cli/status_bar.py:687` `def render_prompt(self, ctx, base_prompt, color_open, color_close, readline_safe)` -- Return ``base_prompt`` with the status line prefixed.
- `StatusBarManager.__init__` (method) `cli/status_bar.py:752` `def __init__(self, config, sources, renderer, payload)` -- Bind config, sources, renderer and a payload mapping.
- `StatusBarManager.enabled` (method) `cli/status_bar.py:783` `def enabled(self)` -- Return ``True`` when the bar should render on this shell.
- `StatusBarManager.collect_context` (method) `cli/status_bar.py:798` `def collect_context(self)` -- Return a fresh :class:`StatusContext` by polling every source.
- `StatusBarManager.render_prompt` (method) `cli/status_bar.py:811` `def render_prompt(self, base_prompt, readline_safe)` -- Return the prompt with the status line prefixed when enabled.
- `StatusBarManager.render_plain_line` (method) `cli/status_bar.py:833` `def render_plain_line(self, ctx)` -- Return the rendered status line without ANSI / readline markers.
- `StatusBarManager.set_enabled` (method) `cli/status_bar.py:847` `def set_enabled(self, enabled)` -- Persist a new enabled state in the payload-backed flag.
- `StatusBarManager.install` (method) `cli/status_bar.py:857` `def install(self, shell, base_prompt_attribute, prompt_attribute)` -- Wire the manager into ``shell`` via a precommand hook.
- `StatusBarManager.build_default_manager` (method) `cli/status_bar.py:969` `def build_default_manager(payload, sessions_dir, advisor_factory, config)` -- Wire the canonical multi-source manager used by the live shell.

## cli/style.py
Depends on: `cli/themes.py`
Imported by: `cli/splash.py`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/showdown-2.1.0.min.js`
- `style` (function) `cli/style.py:49` `def style(token, theme)` -- Return the Rich style string for a semantic token.
- `active_tokens` (function) `cli/style.py:68` `def active_tokens(payload)` -- Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function) `cli/style.py:84` `def paint(text, token, payload)` -- Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function) `cli/style.py:98` `def render_prompt(console, segments, payload)` -- Print a themed prompt line composed of ``(text, token)`` pairs.

## cli/surface_graph.py
Imported by: `cli/surface_tui.py`, `tests/test_surface_graph.py`
- `SurfaceNode.to_dict` (method) `cli/surface_graph.py:100` `def to_dict(self)` -- Return a JSON-serialisable view of the node.
- `SurfaceEdge.to_dict` (method) `cli/surface_graph.py:118` `def to_dict(self)` -- Return a JSON-serialisable view of the edge.
- `SurfaceGraph.to_dict` (method) `cli/surface_graph.py:133` `def to_dict(self)` -- Return a JSON-serialisable view (mirrors the web UI payload).
- `SurfaceGraph.stats` (method) `cli/surface_graph.py:144` `def stats(self)` -- Return per-kind node counts plus edge count.
- `SurfaceGraph.children_of` (method) `cli/surface_graph.py:151` `def children_of(self, node_id)` -- Return nodes that ``node_id`` points to via an outgoing edge.
- `SurfaceGraph.get` (method) `cli/surface_graph.py:163` `def get(self, node_id)` -- Return the node with ``node_id`` or ``None``.
- `SurfaceGraphBuilder.__init__` (method) `cli/surface_graph.py:197` `def __init__(self, config)`
- `SurfaceGraphBuilder.build` (method) `cli/surface_graph.py:200` `def build(self)` -- Read every session artefact and return the assembled graph.
- `SurfaceGraphBuilder.build_surface_graph` (method) `cli/surface_graph.py:562` `def build_surface_graph(sessions_dir, payload_path)` -- Convenience factory: build a graph from on-disk artefacts.
- `SurfaceGraphBuilder.iter_descendants` (method) `cli/surface_graph.py:579` `def iter_descendants(graph, root_id)` -- Yield every node reachable from ``root_id`` via outgoing edges.

## cli/surface_tui.py
Depends on: `cli/commands/containers.py`, `cli/surface_graph.py`, `core/console.py`
Imported by: `cli/commands/recon_migrated.py`
- `TextualNotInstalled.render_static` (method) `cli/surface_tui.py:65` `def render_static(graph, sessions_dir, payload_path, console)` -- Render the surface graph as a Rich tree and return it.
- `TextualNotInstalled.render_json` (method) `cli/surface_tui.py:92` `def render_json(graph, sessions_dir, payload_path)` -- Return the surface graph as a JSON string.
- `TextualNotInstalled.launch_tui` (method) `cli/surface_tui.py:112` `def launch_tui(sessions_dir, payload_path)` -- Open the full-screen Textual surface explorer.
- `SurfaceExplorer.__init__` (method) `cli/surface_tui.py:148` `def __init__(self, sessions_dir, payload_path)`
- `SurfaceExplorer.compose` (method) `cli/surface_tui.py:154` `def compose(self)`
- `SurfaceExplorer.on_mount` (method) `cli/surface_tui.py:161` `def on_mount(self)`
- `SurfaceExplorer.action_refresh` (method) `cli/surface_tui.py:164` `def action_refresh(self)`
- `SurfaceExplorer.action_expand_all` (method) `cli/surface_tui.py:168` `def action_expand_all(self)`
- `SurfaceExplorer.action_collapse_all` (method) `cli/surface_tui.py:172` `def action_collapse_all(self)`
- `SurfaceExplorer.on_tree_node_selected` (method) `cli/surface_tui.py:176` `def on_tree_node_selected(self, event)`

## cli/themes.py
Imported by: `cli/command_form.py`, `cli/graph_overlay.py`, `cli/palette_overlay.py`, `cli/sessions_browser.py`, `cli/status_bar.py`, `cli/style.py`, `cli/timeline_browser.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `cli/tui_theme.py`, `tests/test_themes.py`, `tests/test_toast_bus.py`, `tests/test_tui_style.py`, `tests/test_tui_theme_command.py`, `tests/test_tui_themes.py`
- `Theme.get_theme` (method) `cli/themes.py:222` `def get_theme(name)` -- Return the registered :class:`Theme` for ``name`` with safe fallback.
- `Theme.theme_from_payload` (method) `cli/themes.py:238` `def theme_from_payload(payload)` -- Return the theme selected by ``payload["tui_theme"]``.

## cli/timeline_browser.py
Depends on: `cli/commands/containers.py`, `cli/themes.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_timeline_browser.py`
- `TimelineReader.__init__` (method) `cli/timeline_browser.py:75` `def __init__(self, config, root)` -- Bind to config and resolve the sessions root.
- `TimelineReader.root` (method) `cli/timeline_browser.py:81` `def root(self)` -- Return the resolved sessions root.
- `TimelineReader.read` (method) `cli/timeline_browser.py:85` `def read(self)` -- Return the parsed entries, newest last.
- `TimelineState.reload` (method) `cli/timeline_browser.py:130` `def reload(self)` -- Drop the cache so the next :meth:`entries` call re-reads disk.
- `TimelineState.entries` (method) `cli/timeline_browser.py:134` `def entries(self)` -- Return filtered entries; reads disk on the first call.
- `TimelineState.column_value` (method) `cli/timeline_browser.py:148` `def column_value(self, entry, column)` -- Return the first non-empty value among ``column.source_keys``.
- `TimelineState.build_state` (method) `cli/timeline_browser.py:157` `def build_state(payload, sessions_dir, config)` -- Wire the canonical state used by :func:`launch_scrubber`.
- `TimelineState.launch_scrubber` (method) `cli/timeline_browser.py:169` `def launch_scrubber(payload, state, runner)` -- Open the scrubber and return the highlighted row index on exit.
- `_TimelineBrowserApp.__init__` (method) `cli/timeline_browser.py:228` `def __init__(self)`
- `_TimelineBrowserApp.compose` (method) `cli/timeline_browser.py:234` `def compose(self)`
- `_TimelineBrowserApp.on_mount` (method) `cli/timeline_browser.py:242` `def on_mount(self)`
- `_TimelineBrowserApp.on_input_changed` (method) `cli/timeline_browser.py:249` `def on_input_changed(self, event)`
- `_TimelineBrowserApp.on_data_table_row_highlighted` (method) `cli/timeline_browser.py:253` `def on_data_table_row_highlighted(self, event)`
- `_TimelineBrowserApp.action_refresh` (method) `cli/timeline_browser.py:259` `def action_refresh(self)`
- `_TimelineBrowserApp.action_close` (method) `cli/timeline_browser.py:263` `def action_close(self)`

## cli/tips_engine.py
Depends on: `cli/autosuggest.py`, `cli/engagement_hooks.py`, `cli/noise_verbs.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/phase_labels.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/themes.py`, `core/console.py`, `core/logging.py`, `core/text_utils.py`, `modules/cli_auth.py`, `modules/killchain.py`, `modules/lazy_rbac.py`
Imported by: `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_auto_refresh.py`, `tests/test_phase_labels.py`, `tests/test_tips_engine.py`
- `TipsEngine.__init__` (method) `cli/tips_engine.py:193` `def __init__(self, config, autosuggest_engine)` -- Wire the engine with its configuration and optional autosuggest handle.
- `TipsEngine.enabled` (method) `cli/tips_engine.py:220` `def enabled(self)` -- Whether the engine renders any output.
- `TipsEngine.set_enabled` (method) `cli/tips_engine.py:224` `def set_enabled(self, value)` -- Toggle rendering without dropping state.
- `TipsEngine.render` (method) `cli/tips_engine.py:228` `def render(self, cmd, phase)` -- Run all surfaces for the given command.
- `TipsEngine.render_session_start` (method) `cli/tips_engine.py:406` `def render_session_start(self, phase, os_id)` -- Print a single tip at session start (once per boot).
- `TipsEngine.get_state_snapshot` (method) `cli/tips_engine.py:438` `def get_state_snapshot(self)` -- Return a read-only snapshot of current engagement state.
- `TipsEngine.reset_session` (method) `cli/tips_engine.py:453` `def reset_session(self)` -- Reset session counters without clearing cross-session progress.
- `TipsEngine.heal_commands_seen` (method) `cli/tips_engine.py:458` `def heal_commands_seen(self, known)` -- Purge non-command entries from persisted ``commands_seen``.
- `TipsEngine.build_default_tips_config` (method) `cli/tips_engine.py:1238` `def build_default_tips_config()` -- Build a :class:`TipsConfig` populated from the live framework tables.

## cli/toast_bus.py
Depends on: `cli/themes.py`, `core/console.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/ux.py`, `cli/dashboard_tui.py`, `lazyown.py`, `tests/test_toast_bus.py`
- `ToastState.__init__` (method) `cli/toast_bus.py:99` `def __init__(self, config, root)` -- Bind to config and resolve the on-disk state path.
- `ToastState.path` (method) `cli/toast_bus.py:114` `def path(self)` -- Return the resolved state-file path.
- `ToastState.get` (method) `cli/toast_bus.py:118` `def get(self, name)` -- Return the persisted offset for ``name`` or 0.
- `ToastState.set` (method) `cli/toast_bus.py:123` `def set(self, name, offset)` -- Record ``offset`` for ``name`` in memory.
- `ToastState.reset` (method) `cli/toast_bus.py:129` `def reset(self)` -- Forget every persisted offset (force replay on next read).
- `ToastState.flush` (method) `cli/toast_bus.py:134` `def flush(self)` -- Persist the current offsets atomically.
- `ToastReader.__init__` (method) `cli/toast_bus.py:176` `def __init__(self, config, root)` -- Bind to config and resolve the events root directory.
- `ToastReader.root` (method) `cli/toast_bus.py:187` `def root(self)` -- Return the resolved events root directory.
- `ToastReader.read_unseen` (method) `cli/toast_bus.py:191` `def read_unseen(self, name, start_offset)` -- Return events emitted past ``start_offset`` plus the new end offset.
- `ToastFormatter.__init__` (method) `cli/toast_bus.py:281` `def __init__(self, config, theme)` -- Bind to config and the active theme.
- `ToastFormatter.format` (method) `cli/toast_bus.py:286` `def format(self, event)` -- Return a single themed line for ``event``.
- `ToastFormatter.format_many` (method) `cli/toast_bus.py:298` `def format_many(self, events, width)` -- Render several events as one Rich renderable.
- `ToastBus.__init__` (method) `cli/toast_bus.py:359` `def __init__(self, config, state, reader, formatter, console)` -- Bind every collaborator.
- `ToastBus.collect` (method) `cli/toast_bus.py:374` `def collect(self)` -- Return every unseen event across :attr:`ToastConfig.event_files`.
- `ToastBus.render` (method) `cli/toast_bus.py:386` `def render(self, enabled)` -- Collect, render and persist offsets in a single call.
- `ToastBus.mark_all_seen` (method) `cli/toast_bus.py:415` `def mark_all_seen(self)` -- Advance the offset for every configured file to its current size.
- `ToastBus.toasts_enabled` (method) `cli/toast_bus.py:437` `def toasts_enabled(payload, config)` -- Return ``True`` when toast rendering is permitted.
- `ToastBus.build_default_bus` (method) `cli/toast_bus.py:460` `def build_default_bus(payload, sessions_dir, console)` -- Wire the canonical bus used by the shell postcmd hook.
- `ToastBus.render_toasts` (method) `cli/toast_bus.py:525` `def render_toasts(payload, sessions_dir, console, bus_factory)` -- One-shot helper used by the cmd2 postcmd hook.
- `ToastBus.emit_toast` (method) `cli/toast_bus.py:549` `def emit_toast(message, severity, event_type, sessions_dir, config)` -- Append one toast event so the existing render hook displays it.
- `ToastBus.read_recent_toasts` (method) `cli/toast_bus.py:594` `def read_recent_toasts(sessions_dir, limit, config)` -- Return the most recent toast events without touching read offsets.
- `ToastBus.build_toast_renderable` (method) `cli/toast_bus.py:638` `def build_toast_renderable(events, payload, width, config)` -- Render events with the active theme for any surface.

## cli/tui_theme.py
Depends on: `cli/themes.py`
Imported by: `cli/commands/help_ui.py`
- `run` (function) `cli/tui_theme.py:87` `def run(args, payload, save)` -- Execute the ``tui_theme`` command.

## cli/tutorial.py
Depends on: `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `TutorialConfig.is_done` (method) `cli/tutorial.py:83` `def is_done(config)` -- Return True if the tutorial has already been completed.
- `TutorialConfig.mark_done` (method) `cli/tutorial.py:89` `def mark_done(config)` -- Persist the tutorial completion marker.
- `TutorialConfig.render_header` (method) `cli/tutorial.py:96` `def render_header()` -- Print the tutorial welcome banner.
- `TutorialConfig.render_phase_table` (method) `cli/tutorial.py:113` `def render_phase_table()` -- Print the full phase overview before starting.
- `TutorialConfig.run_step` (method) `cli/tutorial.py:128` `def run_step(index, command, description, why, params, command_runner)` -- Execute one tutorial step and return True if the user wants to continue.
- `TutorialConfig.run` (method) `cli/tutorial.py:185` `def run(params, command_runner)` -- Run the interactive tutorial.

## cli/wizard.py
Depends on: `cli/marketplace_config.py`, `core/console.py`, `core/payload_schema.py`, `core/profiles.py`, `modules/cli_auth.py`, `modules/llm_factory.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/doctor.py`, `tests/test_doctor.py`, `tests/test_wizard_llm.py`
- `WizardResult.run` (method) `cli/wizard.py:169` `def run(params, save)` -- Run the interactive setup wizard and return a :class:`WizardResult`.
- `WizardResult.run_non_interactive` (method) `cli/wizard.py:234` `def run_non_interactive(params, save, values)` -- Apply configuration without prompts — Docker/CI/headless first runs.
- `WizardResult.check_binaries` (method) `cli/wizard.py:947` `def check_binaries(specs, which)` -- Return the presence status of every spec without executing it.

## cli/wizard_scope.py
Imported by: `cli/commands/help_ui.py`
- `WizardScope.parse_scope` (method) `cli/wizard_scope.py:38` `def parse_scope(tokens, config)` -- Parse --show and --only=a,b flags from wizard tokens.
- `WizardScope.status_rows` (method) `cli/wizard_scope.py:64` `def status_rows(params)` -- Build display rows for the current configuration state.

## contrib/legacy/lazy_http_bof.py
- `genHeader` (function) `contrib/legacy/lazy_http_bof.py:6` `def genHeader(raw)`
- `exploit` (function) `contrib/legacy/lazy_http_bof.py:29` `def exploit(target, port, payload)`

## contrib/legacy/lazy_packet_image_sniffer.py
- `check_sudo` (function) `contrib/legacy/lazy_packet_image_sniffer.py:23` `def check_sudo()`
- `list_interfaces` (function) `contrib/legacy/lazy_packet_image_sniffer.py:31` `def list_interfaces()`
- `choose_interface` (function) `contrib/legacy/lazy_packet_image_sniffer.py:49` `def choose_interface(interfaces)`
- `get_subnet_from_interface` (function) `contrib/legacy/lazy_packet_image_sniffer.py:61` `def get_subnet_from_interface(interface)`
- `get_ip_addresses` (function) `contrib/legacy/lazy_packet_image_sniffer.py:65` `def get_ip_addresses(interface)`
- `handle_packet` (function) `contrib/legacy/lazy_packet_image_sniffer.py:111` `def handle_packet(packet)`
- `save_image` (function) `contrib/legacy/lazy_packet_image_sniffer.py:161` `def save_image(src_ip, end_idx)`
- `run` (function) `contrib/legacy/lazy_packet_image_sniffer.py:187` `def run()`
- `daemonize` (function) `contrib/legacy/lazy_packet_image_sniffer.py:192` `def daemonize()`

## contrib/legacy/lazyaddon_creator.py
Depends on: `modules/llm_client.py`
- `parse_github_url` (function) `contrib/legacy/lazyaddon_creator.py:49` `def parse_github_url(url)` -- Extrae (owner, repo) de una URL de GitHub.
- `github_api_get` (function) `contrib/legacy/lazyaddon_creator.py:58` `def github_api_get(owner, repo, endpoint)` -- GET a la API pública de GitHub (sin auth, rate-limit 60/hr).
- `fetch_repo_metadata` (function) `contrib/legacy/lazyaddon_creator.py:68` `def fetch_repo_metadata(owner, repo)` -- Devuelve metadata básica del repo.
- `fetch_readme` (function) `contrib/legacy/lazyaddon_creator.py:73` `def fetch_readme(owner, repo)` -- Descarga y decodifica el README.
- `fetch_root_files` (function) `contrib/legacy/lazyaddon_creator.py:85` `def fetch_root_files(owner, repo)` -- Lista nombres de archivos en el directorio raíz.
- `build_llm_prompt` (function) `contrib/legacy/lazyaddon_creator.py:98` `def build_llm_prompt(meta, readme, root_files)` -- Construye el prompt para el LLM.
- `extract_json_from_response` (function) `contrib/legacy/lazyaddon_creator.py:164` `def extract_json_from_response(text)` -- Extrae el primer bloque JSON de una respuesta de LLM.
- `heuristic_install_command` (function) `contrib/legacy/lazyaddon_creator.py:192` `def heuristic_install_command(root_files, language)` -- Infiere un install_command básico a partir de los archivos raíz.
- `heuristic_execute_command` (function) `contrib/legacy/lazyaddon_creator.py:211` `def heuristic_execute_command(name, root_files, language)` -- Infiere un execute_command básico.
- `heuristic_params` (function) `contrib/legacy/lazyaddon_creator.py:245` `def heuristic_params(name, readme, root_files)` -- Infiere parámetros comunes basándose en el nombre y README.
- `fallback_yaml_data` (function) `contrib/legacy/lazyaddon_creator.py:276` `def fallback_yaml_data(meta, readme, root_files)` -- Genera datos de addon usando solo heurísticas locales (sin LLM).
- `build_yaml` (function) `contrib/legacy/lazyaddon_creator.py:300` `def build_yaml(data, repo_url)` -- Construye la estructura de dict que representa el addon YAML.
- `save_yaml` (function) `contrib/legacy/lazyaddon_creator.py:336` `def save_yaml(addon, output_dir)` -- Guarda el dict como archivo YAML en output_dir.
- `main` (function) `contrib/legacy/lazyaddon_creator.py:357` `def main()`


Next: [API_p5.md](API_p5.md)
