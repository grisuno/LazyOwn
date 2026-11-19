# API (page 5 of 30)
Previous: [API_p4.md](API_p4.md)

## cli/orchestrator_assets_tabs.py
Depends on: `cli/tui_forms.py`, `core/config.py`, `modules/__init__.py`, `modules/apt_playbooks.py`, `modules/bof_admin.py`, `modules/bof_delivery.py`, `modules/chain_registry.py`, `modules/guardrails/__init__.py`, `modules/gym_registry.py`, `modules/lazy_engine.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `modules/playbook_admin.py`, `modules/redteam_gym.py`, `modules/trigger_policy.py`
Imported by: `cli/lazy_orchestrator.py`, `tests/test_audit_remediation.py`, `tests/test_orchestrator_pacing.py`
- `parse_sleeper_windows` (function) `cli/orchestrator_assets_tabs.py:92` `def parse_sleeper_windows(raw)` -- Parse a comma-separated sleeper-window string.
- `format_sleeper_windows` (function) `cli/orchestrator_assets_tabs.py:121` `def format_sleeper_windows(value)` -- Render stored sleeper windows as an editable comma-separated string.
- `parse_edr_pause_ranges` (function) `cli/orchestrator_assets_tabs.py:128` `def parse_edr_pause_ranges(raw)` -- Parse ``level:low-high`` pause ranges from a compact string.
- `format_edr_pause_ranges` (function) `cli/orchestrator_assets_tabs.py:161` `def format_edr_pause_ranges(value)` -- Render stored EDR pause ranges as an editable compact string.
- `OrchestratorAssetsMixin.playbook_rows` (method) `cli/orchestrator_assets_tabs.py:217` `def playbook_rows(self)` -- Return one row per playbook file, including invalid ones.
- `OrchestratorAssetsMixin.playbook_preview` (method) `cli/orchestrator_assets_tabs.py:241` `def playbook_preview(self, filename, limit)` -- Return a bounded YAML preview for one playbook file.
- `OrchestratorAssetsMixin.create_playbook_file` (method) `cli/orchestrator_assets_tabs.py:250` `def create_playbook_file(self, filename, name, description, platforms)` -- Create one playbook YAML and repaint the table.
- `OrchestratorAssetsMixin.save_playbook_text` (method) `cli/orchestrator_assets_tabs.py:271` `def save_playbook_text(self, filename, text)` -- Validate and persist raw YAML edited by the operator.
- `OrchestratorAssetsMixin.delete_playbook_file` (method) `cli/orchestrator_assets_tabs.py:283` `def delete_playbook_file(self, filename)` -- Delete one playbook YAML after the operator confirms.
- `OrchestratorAssetsMixin.playbook_candidates` (method) `cli/orchestrator_assets_tabs.py:291` `def playbook_candidates(self)` -- Return ``(engine_key, summary)`` pairs for chain generation.
- `OrchestratorAssetsMixin.gym_rows` (method) `cli/orchestrator_assets_tabs.py:374` `def gym_rows(self)` -- Return one row per gym definition with its active-run count.
- `OrchestratorAssetsMixin.gym_preview` (method) `cli/orchestrator_assets_tabs.py:411` `def gym_preview(self, gym_id, limit)` -- Return a bounded YAML preview for one gym definition.
- `OrchestratorAssetsMixin.start_gym` (method) `cli/orchestrator_assets_tabs.py:479` `def start_gym(self, gym_id, target)` -- Start one gym and repaint the table.
- `OrchestratorAssetsMixin.stop_gym` (method) `cli/orchestrator_assets_tabs.py:487` `def stop_gym(self, selector)` -- Stop one gym (or every gym when selector is empty) and repaint.
- `OrchestratorAssetsMixin.toggle_gym` (method) `cli/orchestrator_assets_tabs.py:495` `def toggle_gym(self, gym_id)` -- Start the selected gym, or stop its active runs when already active.
- `OrchestratorAssetsMixin.profile_rows` (method) `cli/orchestrator_assets_tabs.py:537` `def profile_rows(self)` -- Return one row per orchestrator profile with the active marker.
- `OrchestratorAssetsMixin.activate_profile` (method) `cli/orchestrator_assets_tabs.py:562` `def activate_profile(self, name)` -- Persist one profile as active and repaint the profile table.
- `OrchestratorAssetsMixin.bof_rows` (method) `cli/orchestrator_assets_tabs.py:630` `def bof_rows(self)` -- Return one row per BOF YAML configuration file, invalid ones included.
- `OrchestratorAssetsMixin.bof_preview` (method) `cli/orchestrator_assets_tabs.py:654` `def bof_preview(self, filename, limit)` -- Return a bounded YAML preview for one BOF file.
- `OrchestratorAssetsMixin.create_bof_file` (method) `cli/orchestrator_assets_tabs.py:663` `def create_bof_file(self, filename, name, description, client)` -- Create one BOF YAML and repaint the table.
- `OrchestratorAssetsMixin.save_bof_text` (method) `cli/orchestrator_assets_tabs.py:683` `def save_bof_text(self, filename, text)` -- Validate and persist raw YAML edited by the operator.
- `OrchestratorAssetsMixin.delete_bof_file` (method) `cli/orchestrator_assets_tabs.py:695` `def delete_bof_file(self, filename)` -- Delete one BOF YAML after the operator confirms.
- `OrchestratorAssetsMixin.stage_bof_file` (method) `cli/orchestrator_assets_tabs.py:703` `def stage_bof_file(self, filename)` -- Stage the compiled artifact of one BOF for beacon delivery.
- `OrchestratorAssetsMixin.chain_rows` (method) `cli/orchestrator_assets_tabs.py:789` `def chain_rows(self)` -- Return one row per chain file, including disabled ones.
- `OrchestratorAssetsMixin.chain_steps_preview` (method) `cli/orchestrator_assets_tabs.py:798` `def chain_steps_preview(self, name, limit)` -- Return the resolved step lines of a chain for the detail pane.
- `OrchestratorAssetsMixin.toggle_chain` (method) `cli/orchestrator_assets_tabs.py:815` `def toggle_chain(self, name)` -- Flip a chain's enabled flag in its YAML file.
- `OrchestratorAssetsMixin.generate_chain` (method) `cli/orchestrator_assets_tabs.py:826` `def generate_chain(self, playbook_key)` -- Generate chains/apt_<slug>.yaml from a playbook engine key.
- `OrchestratorAssetsMixin.remove_chain` (method) `cli/orchestrator_assets_tabs.py:840` `def remove_chain(self, name)` -- Delete a chain file unless others extend it or it is the base.
- `OrchestratorAssetsMixin.on_data_table_row_highlighted` (method) `cli/orchestrator_assets_tabs.py:896` `def on_data_table_row_highlighted(self, event)` -- Refresh the detail pane when the cursor moves.
- `OrchestratorAssetsMixin.seed_triggers_from_yaml` (method) `cli/orchestrator_assets_tabs.py:939` `def seed_triggers_from_yaml(self)` -- Seed triggers from config/orchestrator.yaml into the store.
- `OrchestratorAssetsMixin.toggle_trigger` (method) `cli/orchestrator_assets_tabs.py:969` `def toggle_trigger(self, trigger_id)` -- Flip one trigger's enabled flag in the store.
- `OrchestratorAssetsMixin.remove_trigger` (method) `cli/orchestrator_assets_tabs.py:979` `def remove_trigger(self, trigger_id)` -- Delete one trigger from the store.
- `OrchestratorAssetsMixin.add_trigger` (method) `cli/orchestrator_assets_tabs.py:987` `def add_trigger(self, kind, every_sec, arg)` -- Add a scheduler trigger entered from the picker form.
- `OrchestratorAssetsMixin.trigger_kind_options` (method) `cli/orchestrator_assets_tabs.py:999` `def trigger_kind_options(self)` -- Return selectable trigger kinds for the add form.
- `OrchestratorAssetsMixin.save_pacing` (method) `cli/orchestrator_assets_tabs.py:1089` `def save_pacing(self, values)` -- Validate and persist the Pacing tab fields through set_pacing.
- `OrchestratorAssetsMixin.save_config` (method) `cli/orchestrator_assets_tabs.py:1134` `def save_config(self, values)` -- Merge the given keys into the payload and persist it.
- `OrchestratorAssetsMixin.add_model_member` (method) `cli/orchestrator_assets_tabs.py:1156` `def add_model_member(self, name, model, priority)` -- Append one LLM chain member; returns the stored name.
- `OrchestratorAssetsMixin.remove_model_member` (method) `cli/orchestrator_assets_tabs.py:1164` `def remove_model_member(self, name)` -- Drop one LLM chain member by name.
- `OrchestratorAssetsMixin.set_model_priority` (method) `cli/orchestrator_assets_tabs.py:1172` `def set_model_priority(self, name, priority)` -- Change one LLM member's failover rank and repaint the table.
- `OrchestratorAssetsMixin.set_harness` (method) `cli/orchestrator_assets_tabs.py:1184` `def set_harness(self, enabled)` -- Toggle the deterministic harness from the orchestrator UI.
- `OrchestratorAssetsMixin.add_guard_rule` (method) `cli/orchestrator_assets_tabs.py:1209` `def add_guard_rule(self, pattern, action, reason)` -- Register one guard intercept rule.
- `OrchestratorAssetsMixin.remove_guard_rule` (method) `cli/orchestrator_assets_tabs.py:1217` `def remove_guard_rule(self, pattern)` -- Delete one guard rule by exact pattern.
- `OrchestratorAssetsMixin.save_guardrails` (method) `cli/orchestrator_assets_tabs.py:1268` `def save_guardrails(self, values)` -- Merge harness settings into payload and reconfigure the harness.
- `OrchestratorAssetsMixin.warm_restart_harness` (method) `cli/orchestrator_assets_tabs.py:1314` `def warm_restart_harness(self)` -- Run the harness warm restart and repaint the table.
- `OrchestratorAssetsMixin.rearm_harness` (method) `cli/orchestrator_assets_tabs.py:1326` `def rearm_harness(self)` -- Re-arm suspended features and clear advisories.

## cli/output_mode.py
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/ux.py`
- `parse_output_flags` (function) `cli/output_mode.py:43` `def parse_output_flags(args, config)` -- Split output control flags from positional command arguments.
- `strip_ansi` (function) `cli/output_mode.py:65` `def strip_ansi(text)` -- Remove ANSI escape sequences from text.
- `format_output` (function) `cli/output_mode.py:77` `def format_output(data, mode)` -- Render data according to the parsed output mode.
- `dry_run_line` (function) `cli/output_mode.py:98` `def dry_run_line(command)` -- Render the exact shell line that would run without running it.

## cli/palette.py
Imported by: `cli/command_explorer.py`, `cli/command_form.py`, `cli/commands/misc_migrated.py`, `cli/contextual_help.py`, `cli/engagement_hooks.py`, `cli/lazy_orchestrator.py`, `cli/palette_overlay.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyown.py`, `skills/mcp_tools/palette.py`, `tests/test_command_palette.py`
- `load_index` (function) `cli/palette.py:30` `def load_index(path)` -- Return the parsed catalogue as a dict.
- `all_commands` (function) `cli/palette.py:55` `def all_commands()` -- Return every command entry, sorted by name.
- `all_phases` (function) `cli/palette.py:72` `def all_phases()` -- Return the sorted list of phase identifiers present in the index.
- `all_categories` (function) `cli/palette.py:77` `def all_categories()` -- Return the sorted list of cmd2 category labels present in the index.
- `filter_by_phase` (function) `cli/palette.py:82` `def filter_by_phase(phase)` -- Return command entries whose ``phase`` matches ``phase``.
- `filter_by_category` (function) `cli/palette.py:92` `def filter_by_category(category)` -- Return command entries with the given cmd2 category label.
- `search` (function) `cli/palette.py:97` `def search(query)` -- Substring search over ``name`` and ``summary`` (case-insensitive).
- `get` (function) `cli/palette.py:114` `def get(name)` -- Return the canonical entry for ``name`` or ``None`` if unknown.
- `duplicates` (function) `cli/palette.py:125` `def duplicates()` -- Return the duplicate-method audit list as stored in the index.
- `totals` (function) `cli/palette.py:130` `def totals()` -- Return the ``totals`` block (counts of methods, unique names, ...).

## cli/palette_command.py
Depends on: `cli/commands/enum.py`, `cli/palette_graph.py`, `cli/palette_telemetry.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/palette_overlay.py`, `lazyc2.py`, `lazyown.py`, `skills/mcp_tools/palette.py`, `tests/test_command_palette.py`
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
- `render` (function) `cli/palette_command.py:447` `def render(index, line)` -- Top-level entry point used by :class:`LazyOwnShell.do_palette`.
- `PaletteJsonResult.to_dict` (method) `cli/palette_command.py:502` `def to_dict(self)` -- Serialise to a plain ``dict`` suitable for ``json.dumps``.
- `PaletteJsonRenderer.__init__` (method) `cli/palette_command.py:522` `def __init__(self, config)`
- `PaletteJsonRenderer.render_overview` (method) `cli/palette_command.py:525` `def render_overview(self, phase_counts)` -- Build a result document for overview mode.
- `PaletteJsonRenderer.render_phase` (method) `cli/palette_command.py:532` `def render_phase(self, phase, query, rows)` -- Build a result document for phase mode.
- `PaletteJsonRenderer.render_search` (method) `cli/palette_command.py:541` `def render_search(self, query, rows)` -- Build a result document for search mode.
- `PaletteJsonRenderer.render_detail` (method) `cli/palette_command.py:549` `def render_detail(self, target, entry)` -- Build a result document for detail mode.
- `PaletteJsonRenderer.render_next` (method) `cli/palette_command.py:557` `def render_next(self, phase, rows)` -- Build a result document for next-phase mode.
- `render_json` (function) `cli/palette_command.py:566` `def render_json(index, line)` -- Structured-data variant of :func:`render`.
- `build_palette_view` (function) `cli/palette_command.py:619` `def build_palette_view(index)` -- Assemble the template context consumed by the C2 ``/palette`` view.
- `PaletteCompleter.__init__` (method) `cli/palette_command.py:755` `def __init__(self, config)`
- `PaletteCompleter.complete` (method) `cli/palette_command.py:758` `def complete(self, text, line, endidx, index)` -- Return tab-completion candidates given the editor state.

## cli/palette_graph.py
Imported by: `cli/palette_command.py`, `tests/test_command_palette.py`
- `load_graph` (function) `cli/palette_graph.py:127` `def load_graph(path)` -- Return the parsed graph index, cached per resolved path.
- `safe_load_graph` (function) `cli/palette_graph.py:149` `def safe_load_graph(path)` -- Best-effort variant of :func:`load_graph`.
- `callees` (function) `cli/palette_graph.py:179` `def callees(graph, command_name)` -- Return helper-function labels invoked by ``command_name``.
- `related_commands` (function) `cli/palette_graph.py:226` `def related_commands(graph, command_name)` -- Return ``do_*`` commands that share helper functions with this one.
- `enrich_detail` (function) `cli/palette_graph.py:287` `def enrich_detail(graph, entry)` -- Attach ``calls`` and ``related`` lists to a palette detail entry.
- `enrich_commands` (function) `cli/palette_graph.py:309` `def enrich_commands(graph, rows)` -- Enrich every entry of ``rows`` with neighbour data.

## cli/palette_overlay.py
Depends on: `cli/commands/containers.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_telemetry.py`, `cli/themes.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_palette_overlay.py`
- `PaletteOverlayState.set_query` (method) `cli/palette_overlay.py:83` `def set_query(self, value)` -- Replace the active query with ``value`` (trimmed).
- `PaletteOverlayState.rows` (method) `cli/palette_overlay.py:87` `def rows(self)` -- Return the ranked, truncated rows for the current query.
- `build_state` (function) `cli/palette_overlay.py:162` `def build_state(payload, index, recents, config)` -- Wire the canonical state used by :func:`launch_overlay`.
- `launch_overlay` (function) `cli/palette_overlay.py:188` `def launch_overlay(payload, state, runner)` -- Open the Textual overlay and return the selected command verb.
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
- `load_telemetry` (function) `cli/palette_telemetry.py:186` `def load_telemetry(path)` -- Return the parsed telemetry index, cached per resolved path.
- `safe_load_telemetry` (function) `cli/palette_telemetry.py:204` `def safe_load_telemetry(path)` -- Best-effort variant of :func:`load_telemetry`.
- `command_stats` (function) `cli/palette_telemetry.py:216` `def command_stats(telemetry, command_name)` -- Return aggregated stats for ``command_name`` or ``None`` when unseen.
- `runs_after` (function) `cli/palette_telemetry.py:239` `def runs_after(telemetry, command_name)` -- Return commands that frequently run after ``command_name``.
- `recents` (function) `cli/palette_telemetry.py:259` `def recents(telemetry)` -- Return the most-recently invoked unique ``do_*`` commands.
- `enrich_detail` (function) `cli/palette_telemetry.py:275` `def enrich_detail(telemetry, entry)` -- Attach ``runs``, ``last_seen`` and ``runs_after`` to a detail entry.
- `enrich_commands` (function) `cli/palette_telemetry.py:300` `def enrich_commands(telemetry, rows)` -- Enrich every entry of ``rows`` with telemetry data.

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
- `get_session_tip` (function) `cli/protips.py:313` `def get_session_tip(ctx)` -- Return a single tip to show at session start.
- `render_contextual_tip` (function) `cli/protips.py:339` `def render_contextual_tip(last_cmd, ctx)` -- Print a single dim tip line when the last command triggers one.
- `print_session_tip` (function) `cli/protips.py:369` `def print_session_tip(ctx)` -- Print the session-start tip (called once after the banner).

## cli/purple_tui.py
Depends on: `cli/commands/containers.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleDashboard.compose` (method) `cli/purple_tui.py:98` `def compose(self)`
- `PurpleDashboard.on_mount` (method) `cli/purple_tui.py:108` `def on_mount(self)`
- `PurpleDashboard.action_refresh` (method) `cli/purple_tui.py:112` `def action_refresh(self)`
- `PurpleDashboard.refresh_data` (method) `cli/purple_tui.py:115` `def refresh_data(self)`
- `launch` (function) `cli/purple_tui.py:233` `def launch()` -- Launch the purple team dashboard TUI.

## cli/reactive_hints.py
Depends on: `cli/graph_advisor.py`, `cli/noise_verbs.py`, `core/console.py`, `core/logging.py`, `core/text_utils.py`
Imported by: `cli/command_chain.py`, `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/recommendation_signals.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_improvements_spec.py`, `tests/test_reactive_hints.py`, `tests/test_reactive_hints_expanded.py`
- `render_inline_hints` (function) `cli/reactive_hints.py:234` `def render_inline_hints(advisor, last_command, limit, enabled)` -- Print a single dim hint line below the command output and return immediately.
- `confidence_from_score` (function) `cli/reactive_hints.py:335` `def confidence_from_score(score)` -- Map an unbounded fused recommendation score to a 0-100 display confidence.
- `build_evidence_hints` (function) `cli/reactive_hints.py:376` `def build_evidence_hints(recommendations, limit)` -- Convert fused recommendations into display-ready evidence hints.
- `render_evidence_hints` (function) `cli/reactive_hints.py:414` `def render_evidence_hints(hints)` -- Print evidence-backed hint lines: verb, confidence, reason, provenance.
- `build_evidence_hint_lines` (function) `cli/reactive_hints.py:430` `def build_evidence_hint_lines(hints)` -- Build evidence-backed hint lines as Rich Text objects.
- `read_run_commands` (function) `cli/reactive_hints.py:457` `def read_run_commands(sessions_dir)` -- Return the set of command names already executed this session.
- `render_command_hints` (function) `cli/reactive_hints.py:528` `def render_command_hints(last_command, phase, sessions_dir, limit, enabled)` -- Print phase-aware, history-filtered command hints after each step.
- `command_hints` (function) `cli/reactive_hints.py:563` `def command_hints(last_command, phase, sessions_dir, limit)` -- Return the top next-step command verbs without printing them.

## cli/reasoning_stream.py
Depends on: `core/text_utils.py`
Imported by: `cli/commands/orchestration.py`, `cli/dashboard_tui.py`, `tests/test_engage_gates.py`, `tests/test_reasoning_stream.py`
- `read_raw_events` (function) `cli/reasoning_stream.py:91` `def read_raw_events(path, limit)` -- Return the last ``limit`` well-formed events from the JSONL log.
- `event_to_entry` (function) `cli/reasoning_stream.py:183` `def event_to_entry(event)` -- Convert a raw daemon event into a :class:`ReasoningEntry`.
- `latest_reasoning` (function) `cli/reasoning_stream.py:216` `def latest_reasoning(path, limit)` -- Return the most recent daemon decisions as reasoning entries.
- `latest_hint` (function) `cli/reasoning_stream.py:229` `def latest_hint(events_path)` -- Return the newest human-readable reasoning line for spinners.

## cli/recommendation.py
Imported by: `cli/commands/misc_migrated.py`, `cli/recommendation_signals.py`, `skills/mcp_tools/recommend_next.py`, `tests/test_killchain_gap_signal.py`, `tests/test_recommendation.py`
- `RecommendationSignal.propose` (method) `cli/recommendation.py:187` `def propose(self, ctx)` -- Return zero or more :class:`Proposal` objects for ``ctx``.
- `CategoryResolver.__init__` (method) `cli/recommendation.py:201` `def __init__(self, index_path, loader)` -- Build the resolver from the command index.
- `CategoryResolver.category_for` (method) `cli/recommendation.py:227` `def category_for(self, action)` -- Return the kill-chain category for ``action`` or an empty string.
- `RecommendationEngine.__init__` (method) `cli/recommendation.py:240` `def __init__(self, signals, resolver, weights)` -- Wire the engine with its signals and fusion parameters.
- `RecommendationEngine.recommend` (method) `cli/recommendation.py:258` `def recommend(self, ctx)` -- Return the fused, ranked recommendations for ``ctx``.
- `_Accumulator.add` (method) `cli/recommendation.py:374` `def add(self, source, contribution, proposal)` -- Fold one signal's proposal into the running total.
- `_Accumulator.build` (method) `cli/recommendation.py:386` `def build(self)` -- Freeze the slot into an immutable :class:`Recommendation`.

## cli/recommendation_signals.py
Depends on: `cli/exploration.py`, `cli/graph_advisor.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recon_plan.py`, `core/logging.py`, `modules/apt_playbooks.py`, `modules/world_model.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `modules/engage_summary.py`, `skills/mcp_tools/recommend_next.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_gap_signal.py`, `tests/test_phase1_data_gaps.py`, `tests/test_recommendation.py`
- `GraphSignal.__init__` (method) `cli/recommendation_signals.py:116` `def __init__(self, advisor)` -- Store the graph advisor facade.
- `GraphSignal.propose` (method) `cli/recommendation_signals.py:126` `def propose(self, ctx)` -- Return graph-adjacent command proposals for ``ctx``.
- `PolicySignal.__init__` (method) `cli/recommendation_signals.py:154` `def __init__(self, policy)` -- Store the policy integration facade.
- `PolicySignal.propose` (method) `cli/recommendation_signals.py:163` `def propose(self, ctx)` -- Return category-prior proposals for ``ctx``.
- `ReconPlanSignal.__init__` (method) `cli/recommendation_signals.py:191` `def __init__(self, engine, builder)` -- Store the exploration engine and the plan builder callable.
- `ReconPlanSignal.propose` (method) `cli/recommendation_signals.py:201` `def propose(self, ctx)` -- Return trigger-matched addon/tool/command proposals for ``ctx``.
- `KillChainSignal.__init__` (method) `cli/recommendation_signals.py:230` `def __init__(self, next_table, phase_table)` -- Store the adjacency and phase-priority tables.
- `KillChainSignal.propose` (method) `cli/recommendation_signals.py:244` `def propose(self, ctx)` -- Return adjacency- and phase-derived proposals for ``ctx``.
- `read_recent_commands` (function) `cli/recommendation_signals.py:276` `def read_recent_commands(sessions_dir, window)` -- Return the last ``window`` command verbs from the session transcript.
- `build_context` (function) `cli/recommendation_signals.py:309` `def build_context(payload, sessions_dir, target, limit)` -- Assemble a :class:`RecommendationContext` from live engagement state.
- `PlaybookSignal.__init__` (method) `cli/recommendation_signals.py:347` `def __init__(self, playbook_engine)` -- Store an optional playbook engine facade.
- `PlaybookSignal.propose` (method) `cli/recommendation_signals.py:356` `def propose(self, ctx)` -- Return playbook-based proposals for the current context.
- `KillchainGapSignal.__init__` (method) `cli/recommendation_signals.py:408` `def __init__(self, sessions_dir)`
- `KillchainGapSignal.propose` (method) `cli/recommendation_signals.py:411` `def propose(self, ctx)` -- Return gap-detection proposals for ``ctx``.
- `GraphTopologySignal.__init__` (method) `cli/recommendation_signals.py:544` `def __init__(self, sessions_dir)`
- `GraphTopologySignal.propose` (method) `cli/recommendation_signals.py:547` `def propose(self, ctx)` -- Return lateral movement and topology proposals from network graph.
- `build_default_engine` (function) `cli/recommendation_signals.py:651` `def build_default_engine(payload, sessions_dir, graph_path, command_index_path, weights)` -- Wire every available deterministic signal into one engine.
- `recommend_with_evidence` (function) `cli/recommendation_signals.py:707` `def recommend_with_evidence(payload, sessions_dir, target, phase, limit, engine)` -- Return fused, ranked recommendations carrying reason and score for display.

## cli/recon_plan.py
Depends on: `cli/exploration.py`, `modules/killchain.py`
Imported by: `cli/lazynmap_post.py`, `cli/recommendation_signals.py`, `tests/test_lazynmap_post.py`, `tests/test_recon_plan.py`
- `ReconPlan.is_empty` (method) `cli/recon_plan.py:139` `def is_empty(self)` -- Return ``True`` when the plan carries no actionable items.
- `build_recon_plan` (function) `cli/recon_plan.py:144` `def build_recon_plan(target, engine, payload, config, command_index_loader, clock)` -- Assemble a :class:`ReconPlan` for ``target`` using ``engine``.
- `render_markdown` (function) `cli/recon_plan.py:207` `def render_markdown(plan)` -- Render ``plan`` as a Markdown document suitable for sessions/.
- `write_plan` (function) `cli/recon_plan.py:257` `def write_plan(plan, sessions_dir, config)` -- Persist ``plan`` to ``sessions/recon_plan_<target>.md`` atomically.
- `render_rich` (function) `cli/recon_plan.py:299` `def render_rich(plan, console)` -- Render ``plan`` to the supplied Rich console.

## cli/registry.py
Depends on: `cli/commands/_dormancy.py`
Imported by: `cli/__init__.py`, `lazyown.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_exploitdb_command_set.py`, `tests/test_exposure_command_sets.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_param_registry.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `iter_command_sets` (function) `cli/registry.py:41` `def iter_command_sets(include_pending)` -- Yield every ``CommandSet`` subclass found under ``cli.commands.*``.
- `register_command_sets` (function) `cli/registry.py:77` `def register_command_sets(shell)` -- Instantiate and register every active ``CommandSet`` on ``shell``.

## cli/retry_support.py
Depends on: `cli/apt_chain_support.py`, `modules/chain_registry.py`, `modules/chain_runner.py`, `modules/chain_state.py`, `modules/lazy_loop.py`, `modules/retry_session.py`, `utils.py`
Imported by: `cli/commands/retry_ops.py`, `tests/test_retry_session.py`
- `looks_like_run_id` (function) `cli/retry_support.py:45` `def looks_like_run_id(token)` -- Return True when the token reads as a chain run id, not a name.
- `LastTask.known` (method) `cli/retry_support.py:76` `def known(self)` -- Return True when a task record exists.
- `last_loop_task` (function) `cli/retry_support.py:81` `def last_loop_task()` -- Return the last non-complete task from the TaskStore.
- `status_snapshot` (function) `cli/retry_support.py:104` `def status_snapshot(limit)` -- Collect retry-relevant state: failed checkpoints + last task.
- `consent_to_elevate` (function) `cli/retry_support.py:129` `def consent_to_elevate(rest, confirmer)` -- Resolve ``--sudo`` for one retry invocation.
- `RetryChainReport.to_dict` (method) `cli/retry_support.py:189` `def to_dict(self)` -- Return a JSON-serializable view.
- `retry_chain` (function) `cli/retry_support.py:204` `def retry_chain(chain_or_run, shell, extra_vars, dry_run)` -- Resume a failed chain, applying user-varied tokens.

## cli/scope_guard.py
Depends on: `cli/commands/enum.py`
Imported by: `lazyown.py`, `sdk/lazymode/runner.py`, `tests/test_scope_guard.py`
- `ScopeMode.from_value` (method) `cli/scope_guard.py:105` `def from_value(cls, value)` -- Coerce an arbitrary payload value into a :class:`ScopeMode`.
- `build_offensive_commands` (function) `cli/scope_guard.py:147` `def build_offensive_commands(command_categories)` -- Select the command names whose category is offensive.
- `normalize_scope` (function) `cli/scope_guard.py:163` `def normalize_scope(entries)` -- Coerce a scope specification into a tuple of entry strings.
- `target_in_scope` (function) `cli/scope_guard.py:218` `def target_in_scope(target, entries)` -- Return whether *target* falls within any of the scope *entries*.
- `target_in_deny` (function) `cli/scope_guard.py:254` `def target_in_deny(target, entries)` -- Return whether *target* is explicitly denied.
- `ScopeGuard.__init__` (method) `cli/scope_guard.py:280` `def __init__(self, scope_entries, mode, is_offensive, deny_entries)` -- Initialise the guard.
- `ScopeGuard.evaluate` (method) `cli/scope_guard.py:304` `def evaluate(self, command, target)` -- Evaluate a single command against the active target.

## cli/session_brief.py
Depends on: `cli/themes.py`, `modules/__init__.py`, `modules/lazy_engine.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`, `modules/world_model.py`
Imported by: `lazyown.py`, `tests/test_session_brief.py`
- `brief_enabled` (function) `cli/session_brief.py:47` `def brief_enabled(payload)` -- Return False when the UI hints continuity suppresses the brief.
- `fetch_task_rows` (function) `cli/session_brief.py:84` `def fetch_task_rows()` -- Read the full task rows from the loop store, never raising.
- `build_session_brief` (function) `cli/session_brief.py:127` `def build_session_brief(payload, tasks)` -- Build the one-startup campaign brief panel.
- `print_session_brief` (function) `cli/session_brief.py:163` `def print_session_brief(console, payload)` -- Render the brief through ``console`` when UI hints allow.

## cli/session_hud.py
Depends on: `cli/engagement_hooks.py`
Imported by: `cli/commands/ux.py`
- `count_lines_in_globs` (function) `cli/session_hud.py:62` `def count_lines_in_globs(root, patterns)` -- Count non-empty lines across every file matching the patterns.
- `count_csv_rows` (function) `cli/session_hud.py:83` `def count_csv_rows(path)` -- Count data rows in a CSV file without loading it fully.
- `format_elapsed` (function) `cli/session_hud.py:100` `def format_elapsed(seconds)` -- Format a duration as HH:MM:SS.
- `phase_bar` (function) `cli/session_hud.py:115` `def phase_bar(phase, width)` -- Render kill-chain progress as filled and empty blocks.
- `build_snapshot` (function) `cli/session_hud.py:155` `def build_snapshot(params, config)` -- Build a snapshot from live params, engagement state and session files.
- `render_snapshot` (function) `cli/session_hud.py:180` `def render_snapshot(snapshot, config)` -- Render the session counters as two plain lines.

## cli/session_resumer.py
Depends on: `core/console.py`, `core/logging.py`, `modules/world_model.py`
Imported by: `cli/commands/session_ops.py`
- `SessionResumer.__init__` (method) `cli/session_resumer.py:57` `def __init__(self, config)`
- `SessionResumer.render_startup_panel` (method) `cli/session_resumer.py:130` `def render_startup_panel(self)` -- Render the resume panel and return the selected target IP, or None.

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
- `build_state` (function) `cli/sessions_browser.py:258` `def build_state(payload, sessions_dir, config)` -- Wire the canonical state used by :func:`launch_browser`.
- `launch_browser` (function) `cli/sessions_browser.py:281` `def launch_browser(payload, state, runner)` -- Open the Textual browser and return the last-viewed relative path.
- `_SessionsBrowserApp.__init__` (method) `cli/sessions_browser.py:340` `def __init__(self)`
- `_SessionsBrowserApp.compose` (method) `cli/sessions_browser.py:346` `def compose(self)`
- `_SessionsBrowserApp.on_mount` (method) `cli/sessions_browser.py:356` `def on_mount(self)`
- `_SessionsBrowserApp.on_input_changed` (method) `cli/sessions_browser.py:359` `def on_input_changed(self, event)`
- `_SessionsBrowserApp.on_tree_node_selected` (method) `cli/sessions_browser.py:363` `def on_tree_node_selected(self, event)`
- `_SessionsBrowserApp.action_refresh` (method) `cli/sessions_browser.py:370` `def action_refresh(self)`
- `_SessionsBrowserApp.action_close` (method) `cli/sessions_browser.py:373` `def action_close(self)`

## cli/show.py
Imported by: `2026-11-18_112624/jquery-1.11.3.min.js`, `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `static/js/bootstrap-4.5.2.min.js`, `static/js/bootstrap-5.3.0.bundle.min.js`, `static/js/chart.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/quill-2.0.3.js`, `static/js/tippy-6.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_cli_assign.py`
- `format_payload` (function) `cli/show.py:14` `def format_payload(params)` -- Render ``params`` as a sorted, aligned ``key = value`` block.

## cli/splash.py
Depends on: `cli/style.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_tui_splash.py`
- `SplashEffect.render` (method) `cli/splash.py:71` `def render(self, console, lines, tokens, config)`
- `TypewriterEffect.render` (method) `cli/splash.py:90` `def render(self, console, lines, tokens, config)`
- `InstantEffect.render` (method) `cli/splash.py:150` `def render(self, console, lines, tokens, config)`
- `render_splash` (function) `cli/splash.py:166` `def render_splash(console, lines, payload, config, effect_name)` -- Render the splash overlay and optionally clear the screen.

## cli/status_bar.py
Depends on: `cli/reactive_hints.py`, `cli/themes.py`, `modules/world_model.py`
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
- `SessionFindingSource.__init__` (method) `cli/status_bar.py:324` `def __init__(self, config, reader)` -- Bind to config and sessions reader.
- `SessionFindingSource.collect` (method) `cli/status_bar.py:329` `def collect(self)` -- Return a short description of the freshest credential / vuln / note.
- `CommandHintSuggestionSource.__init__` (method) `cli/status_bar.py:435` `def __init__(self, config, reader, phase_provider, hint_provider)` -- Bind to config, reader and the current-phase callable.
- `CommandHintSuggestionSource.collect` (method) `cli/status_bar.py:460` `def collect(self)` -- Return the top kill-chain suggestion or the configured fallback.
- `GraphSuggestionSource.__init__` (method) `cli/status_bar.py:520` `def __init__(self, config, reader, advisor_factory)` -- Bind to config, reader, and an optional advisor factory.
- `GraphSuggestionSource.collect` (method) `cli/status_bar.py:539` `def collect(self)` -- Return a one-token suggestion.
- `CollabPresenceSource.__init__` (method) `cli/status_bar.py:610` `def __init__(self, config, reader, clock)` -- Bind to the active config, reader, and an injectable clock.
- `CollabPresenceSource.collect` (method) `cli/status_bar.py:631` `def collect(self)` -- Return the active-operator count formatted as a short string.
- `StatusBarRenderer.__init__` (method) `cli/status_bar.py:668` `def __init__(self, config)` -- Bind to the active configuration.
- `StatusBarRenderer.render_plain` (method) `cli/status_bar.py:673` `def render_plain(self, ctx)` -- Return the line without ANSI colour or readline markers.
- `StatusBarRenderer.render_prompt` (method) `cli/status_bar.py:696` `def render_prompt(self, ctx, base_prompt, color_open, color_close, readline_safe)` -- Return ``base_prompt`` with the status line prefixed.
- `StatusBarManager.__init__` (method) `cli/status_bar.py:761` `def __init__(self, config, sources, renderer, payload)` -- Bind config, sources, renderer and a payload mapping.
- `StatusBarManager.enabled` (method) `cli/status_bar.py:792` `def enabled(self)` -- Return ``True`` when the bar should render on this shell.
- `StatusBarManager.collect_context` (method) `cli/status_bar.py:807` `def collect_context(self)` -- Return a fresh :class:`StatusContext` by polling every source.
- `StatusBarManager.render_prompt` (method) `cli/status_bar.py:820` `def render_prompt(self, base_prompt, readline_safe)` -- Return the prompt with the status line prefixed when enabled.
- `StatusBarManager.render_plain_line` (method) `cli/status_bar.py:842` `def render_plain_line(self, ctx)` -- Return the rendered status line without ANSI / readline markers.
- `StatusBarManager.set_enabled` (method) `cli/status_bar.py:856` `def set_enabled(self, enabled)` -- Persist a new enabled state in the payload-backed flag.
- `StatusBarManager.install` (method) `cli/status_bar.py:866` `def install(self, shell, base_prompt_attribute, prompt_attribute)` -- Wire the manager into ``shell`` via a precommand hook.
- `build_default_manager` (function) `cli/status_bar.py:978` `def build_default_manager(payload, sessions_dir, advisor_factory, config)` -- Wire the canonical multi-source manager used by the live shell.

## cli/style.py
Depends on: `cli/themes.py`
Imported by: `2026-11-18_112624/jquery-1.11.3.min.js`, `cli/splash.py`, `static/js/force-graph-1.43.5.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/showdown-2.1.0.min.js`
- `style` (function) `cli/style.py:49` `def style(token, theme)` -- Return the Rich style string for a semantic token.
- `active_tokens` (function) `cli/style.py:68` `def active_tokens(payload)` -- Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function) `cli/style.py:84` `def paint(text, token, payload)` -- Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function) `cli/style.py:98` `def render_prompt(console, segments, payload)` -- Print a themed prompt line composed of ``(text, token)`` pairs.

## cli/surface_graph.py
Imported by: `cli/surface_tui.py`, `modules/attack_surface3d.py`, `tests/test_surface_graph.py`
- `SurfaceNode.to_dict` (method) `cli/surface_graph.py:102` `def to_dict(self)` -- Return a JSON-serialisable view of the node.
- `SurfaceEdge.to_dict` (method) `cli/surface_graph.py:120` `def to_dict(self)` -- Return a JSON-serialisable view of the edge.
- `SurfaceGraph.to_dict` (method) `cli/surface_graph.py:135` `def to_dict(self)` -- Return a JSON-serialisable view (mirrors the web UI payload).
- `SurfaceGraph.stats` (method) `cli/surface_graph.py:146` `def stats(self)` -- Return per-kind node counts plus edge count.
- `SurfaceGraph.children_of` (method) `cli/surface_graph.py:153` `def children_of(self, node_id)` -- Return nodes that ``node_id`` points to via an outgoing edge.
- `SurfaceGraph.get` (method) `cli/surface_graph.py:165` `def get(self, node_id)` -- Return the node with ``node_id`` or ``None``.
- `SurfaceGraphBuilder.__init__` (method) `cli/surface_graph.py:199` `def __init__(self, config)`
- `SurfaceGraphBuilder.build` (method) `cli/surface_graph.py:202` `def build(self)` -- Read every session artefact and return the assembled graph.
- `build_surface_graph` (function) `cli/surface_graph.py:633` `def build_surface_graph(sessions_dir, payload_path)` -- Convenience factory: build a graph from on-disk artefacts.
- `iter_descendants` (function) `cli/surface_graph.py:650` `def iter_descendants(graph, root_id)` -- Yield every node reachable from ``root_id`` via outgoing edges.

## cli/surface_tui.py
Depends on: `cli/commands/containers.py`, `cli/surface_graph.py`, `core/console.py`
Imported by: `cli/commands/recon_migrated.py`
- `render_static` (function) `cli/surface_tui.py:65` `def render_static(graph, sessions_dir, payload_path, console)` -- Render the surface graph as a Rich tree and return it.
- `render_json` (function) `cli/surface_tui.py:92` `def render_json(graph, sessions_dir, payload_path)` -- Return the surface graph as a JSON string.
- `launch_tui` (function) `cli/surface_tui.py:112` `def launch_tui(sessions_dir, payload_path)` -- Open the full-screen Textual surface explorer.
- `SurfaceExplorer.__init__` (method) `cli/surface_tui.py:148` `def __init__(self, sessions_dir, payload_path)`
- `SurfaceExplorer.compose` (method) `cli/surface_tui.py:154` `def compose(self)`
- `SurfaceExplorer.on_mount` (method) `cli/surface_tui.py:161` `def on_mount(self)`
- `SurfaceExplorer.action_refresh` (method) `cli/surface_tui.py:164` `def action_refresh(self)`
- `SurfaceExplorer.action_expand_all` (method) `cli/surface_tui.py:168` `def action_expand_all(self)`
- `SurfaceExplorer.action_collapse_all` (method) `cli/surface_tui.py:172` `def action_collapse_all(self)`
- `SurfaceExplorer.on_tree_node_selected` (method) `cli/surface_tui.py:176` `def on_tree_node_selected(self, event)`

## cli/themes.py
Imported by: `cli/command_form.py`, `cli/graph_overlay.py`, `cli/palette_overlay.py`, `cli/session_brief.py`, `cli/sessions_browser.py`, `cli/status_bar.py`, `cli/style.py`, `cli/timeline_browser.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `cli/tui_theme.py`, `tests/test_lazy_parity.py`, `tests/test_themes.py`, `tests/test_toast_bus.py`, `tests/test_tui_style.py`, `tests/test_tui_theme_command.py`, `tests/test_tui_themes.py`
- `get_theme` (function) `cli/themes.py:222` `def get_theme(name)` -- Return the registered :class:`Theme` for ``name`` with safe fallback.
- `theme_from_payload` (function) `cli/themes.py:238` `def theme_from_payload(payload)` -- Return the theme selected by ``payload["tui_theme"]``.

## cli/timeline_browser.py
Depends on: `cli/commands/containers.py`, `cli/themes.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_timeline_browser.py`
- `TimelineReader.__init__` (method) `cli/timeline_browser.py:75` `def __init__(self, config, root)` -- Bind to config and resolve the sessions root.
- `TimelineReader.root` (method) `cli/timeline_browser.py:81` `def root(self)` -- Return the resolved sessions root.
- `TimelineReader.read` (method) `cli/timeline_browser.py:85` `def read(self)` -- Return the parsed entries, newest last.
- `TimelineState.reload` (method) `cli/timeline_browser.py:130` `def reload(self)` -- Drop the cache so the next :meth:`entries` call re-reads disk.
- `TimelineState.entries` (method) `cli/timeline_browser.py:134` `def entries(self)` -- Return filtered entries; reads disk on the first call.
- `TimelineState.column_value` (method) `cli/timeline_browser.py:148` `def column_value(self, entry, column)` -- Return the first non-empty value among ``column.source_keys``.
- `build_state` (function) `cli/timeline_browser.py:157` `def build_state(payload, sessions_dir, config)` -- Wire the canonical state used by :func:`launch_scrubber`.
- `launch_scrubber` (function) `cli/timeline_browser.py:169` `def launch_scrubber(payload, state, runner)` -- Open the scrubber and return the highlighted row index on exit.
- `_TimelineBrowserApp.__init__` (method) `cli/timeline_browser.py:228` `def __init__(self)`
- `_TimelineBrowserApp.compose` (method) `cli/timeline_browser.py:234` `def compose(self)`
- `_TimelineBrowserApp.on_mount` (method) `cli/timeline_browser.py:242` `def on_mount(self)`
- `_TimelineBrowserApp.on_input_changed` (method) `cli/timeline_browser.py:249` `def on_input_changed(self, event)`
- `_TimelineBrowserApp.on_data_table_row_highlighted` (method) `cli/timeline_browser.py:253` `def on_data_table_row_highlighted(self, event)`
- `_TimelineBrowserApp.action_refresh` (method) `cli/timeline_browser.py:259` `def action_refresh(self)`
- `_TimelineBrowserApp.action_close` (method) `cli/timeline_browser.py:263` `def action_close(self)`

## cli/tips_engine.py
Depends on: `cli/autosuggest.py`, `cli/engagement_hooks.py`, `cli/noise_verbs.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/phase_labels.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/themes.py`, `core/console.py`, `core/logging.py`, `core/safe_console.py`, `core/text_utils.py`, `modules/cli_auth.py`, `modules/killchain.py`, `modules/lazy_rbac.py`, `modules/world_model.py`
Imported by: `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_auto_refresh.py`, `tests/test_phase_labels.py`, `tests/test_tips_engine.py`
- `TipsEngine.__init__` (method) `cli/tips_engine.py:194` `def __init__(self, config, autosuggest_engine)` -- Wire the engine with its configuration and optional autosuggest handle.
- `TipsEngine.enabled` (method) `cli/tips_engine.py:221` `def enabled(self)` -- Whether the engine renders any output.
- `TipsEngine.set_enabled` (method) `cli/tips_engine.py:225` `def set_enabled(self, value)` -- Toggle rendering without dropping state.
- `TipsEngine.render` (method) `cli/tips_engine.py:229` `def render(self, cmd, phase)` -- Run all surfaces for the given command.
- `TipsEngine.render_session_start` (method) `cli/tips_engine.py:408` `def render_session_start(self, phase, os_id)` -- Print a single tip at session start (once per boot).
- `TipsEngine.get_state_snapshot` (method) `cli/tips_engine.py:440` `def get_state_snapshot(self)` -- Return a read-only snapshot of current engagement state.
- `TipsEngine.reset_session` (method) `cli/tips_engine.py:455` `def reset_session(self)` -- Reset session counters without clearing cross-session progress.
- `TipsEngine.heal_commands_seen` (method) `cli/tips_engine.py:460` `def heal_commands_seen(self, known)` -- Purge non-command entries from persisted ``commands_seen``.
- `build_default_tips_config` (function) `cli/tips_engine.py:1242` `def build_default_tips_config()` -- Build a :class:`TipsConfig` populated from the live framework tables.

## cli/toast_bus.py
Depends on: `cli/themes.py`, `core/console.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/ux.py`, `cli/dashboard_tui.py`, `lazy_sentinel4.py`, `lazyown.py`, `tests/test_lazy_parity.py`, `tests/test_toast_bus.py`, `tests/test_toastr_unify.py`
- `ToastState.__init__` (method) `cli/toast_bus.py:131` `def __init__(self, config, root)` -- Bind to config and resolve the on-disk state path.
- `ToastState.path` (method) `cli/toast_bus.py:146` `def path(self)` -- Return the resolved state-file path.
- `ToastState.get` (method) `cli/toast_bus.py:150` `def get(self, name)` -- Return the persisted offset for ``name`` or 0.
- `ToastState.set` (method) `cli/toast_bus.py:155` `def set(self, name, offset)` -- Record ``offset`` for ``name`` in memory.
- `ToastState.reset` (method) `cli/toast_bus.py:161` `def reset(self)` -- Forget every persisted offset (force replay on next read).
- `ToastState.flush` (method) `cli/toast_bus.py:166` `def flush(self)` -- Persist the current offsets atomically.
- `ToastReader.__init__` (method) `cli/toast_bus.py:208` `def __init__(self, config, root)` -- Bind to config and resolve the events root directory.
- `ToastReader.root` (method) `cli/toast_bus.py:219` `def root(self)` -- Return the resolved events root directory.
- `ToastReader.read_unseen` (method) `cli/toast_bus.py:223` `def read_unseen(self, name, start_offset)` -- Return events emitted past ``start_offset`` plus the new end offset.
- `ToastReader.resolve_sources` (method) `cli/toast_bus.py:255` `def resolve_sources(self, names)` -- Expand glob source entries against the sessions root.
- `toastr_severity_style` (function) `cli/toast_bus.py:449` `def toastr_severity_style(severity)` -- Resolve one severity into the shared border/text style pair.
- `rich_toastr_panel` (function) `cli/toast_bus.py:456` `def rich_toastr_panel(message, severity, terminal_width, config)` -- Build the adaptive toastr panel used by the cmd2 shell.
- `shell_hint_bypass` (function) `cli/toast_bus.py:509` `def shell_hint_bypass(console, message, severity)` -- Print the flat bypass line used when UI hints are off.
- `sentinel_toast_panel` (function) `cli/toast_bus.py:528` `def sentinel_toast_panel(file_name, relevant_info, commands, details, severity)` -- Build the yara sentinel popup with the shared styling.
- `ToastFormatter.__init__` (method) `cli/toast_bus.py:566` `def __init__(self, config, theme)` -- Bind to config and the active theme.
- `ToastFormatter.format` (method) `cli/toast_bus.py:571` `def format(self, event)` -- Return a single themed line for ``event``.
- `ToastFormatter.is_prominent` (method) `cli/toast_bus.py:584` `def is_prominent(self, event)` -- Return True when an event deserves a full toastr panel.
- `ToastFormatter.format_prominent` (method) `cli/toast_bus.py:594` `def format_prominent(self, event)` -- Render an event as a toastr panel with the complete summary.
- `ToastFormatter.format_ephemeral` (method) `cli/toast_bus.py:616` `def format_ephemeral(self, event)` -- Return a single sonner-style line with severity icon for ``event``.
- `ToastFormatter.duration_for` (method) `cli/toast_bus.py:644` `def duration_for(self, event)` -- Return the auto-dismiss delay in seconds for ``event``.
- `ToastFormatter.digest_line` (method) `cli/toast_bus.py:669` `def digest_line(dropped)` -- Summarise over-budget events so none vanish silently.
- `ToastFormatter.format_many` (method) `cli/toast_bus.py:677` `def format_many(self, events, width)` -- Render several events as one Rich renderable.
- `ToastBus.__init__` (method) `cli/toast_bus.py:757` `def __init__(self, config, state, reader, formatter, console)` -- Bind every collaborator.
- `ToastBus.collect` (method) `cli/toast_bus.py:772` `def collect(self)` -- Return every unseen event across :attr:`ToastConfig.event_files`.
- `ToastBus.render` (method) `cli/toast_bus.py:785` `def render(self, enabled)` -- Collect, render and persist offsets in a single call.
- `ToastBus.mark_all_seen` (method) `cli/toast_bus.py:814` `def mark_all_seen(self)` -- Advance the offset for every configured file to its current size.
- `ToastBus.render_ephemeral` (method) `cli/toast_bus.py:822` `def render_ephemeral(self, enabled, duration)` -- Collect unseen events and print each as an auto-expiring line.
- `toasts_enabled` (function) `cli/toast_bus.py:920` `def toasts_enabled(payload, config)` -- Return ``True`` when toast rendering is permitted.
- `build_default_bus` (function) `cli/toast_bus.py:943` `def build_default_bus(payload, sessions_dir, console)` -- Wire the canonical bus used by the shell postcmd hook.
- `render_toasts` (function) `cli/toast_bus.py:972` `def render_toasts(payload, sessions_dir, console, bus_factory)` -- One-shot helper used by the cmd2 postcmd hook.
- `ephemeral_enabled` (function) `cli/toast_bus.py:996` `def ephemeral_enabled(payload, config)` -- Return True when toasts must auto-dismiss like sonner.
- `render_ephemeral_toasts` (function) `cli/toast_bus.py:1012` `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` -- Collect unseen events and print each as an auto-expiring line.
- `emit_toast` (function) `cli/toast_bus.py:1042` `def emit_toast(message, severity, event_type, sessions_dir, config)` -- Append one toast event so the existing render hook displays it.
- `read_recent_toasts` (function) `cli/toast_bus.py:1087` `def read_recent_toasts(sessions_dir, limit, config)` -- Return the most recent toast events without touching read offsets.
- `build_toast_renderable` (function) `cli/toast_bus.py:1131` `def build_toast_renderable(events, payload, width, config)` -- Render events with the active theme for any surface.

## cli/tui_forms.py
Depends on: `cli/commands/containers.py`
Imported by: `cli/lazy_orchestrator.py`, `cli/marketplace_config.py`, `cli/orchestrator_assets_tabs.py`, `tests/test_lazy_orchestrator.py`
- `filter_candidates` (function) `cli/tui_forms.py:27` `def filter_candidates(query, options, limit)` -- Filter ``(value, description)`` pairs by a case-insensitive query.
- `FormModal.__init__` (method) `cli/tui_forms.py:68` `def __init__(self, title, fields, defaults, save_label)` -- Store the title, ``(id, label, placeholder)`` fields and defaults.
- `FormModal.compose` (method) `cli/tui_forms.py:82` `def compose(self)` -- One labeled input per field plus the save button.
- `FormModal.on_button_pressed` (method) `cli/tui_forms.py:102` `def on_button_pressed(self, event)` -- Save closes the modal with every field value.
- `FormModal.on_input_submitted` (method) `cli/tui_forms.py:107` `def on_input_submitted(self, event)` -- Enter commits the form like the save button.
- `SearchSelectModal.__init__` (method) `cli/tui_forms.py:122` `def __init__(self, title, options, placeholder, allow_custom)` -- Store the title, candidate pairs and placeholder.
- `SearchSelectModal.compose` (method) `cli/tui_forms.py:136` `def compose(self)` -- Search box, filtered option list and action buttons.
- `SearchSelectModal.on_mount` (method) `cli/tui_forms.py:147` `def on_mount(self)` -- Render the first page and focus the search box.
- `SearchSelectModal.on_input_changed` (method) `cli/tui_forms.py:201` `def on_input_changed(self, event)` -- Filter as the operator types.
- `SearchSelectModal.on_input_submitted` (method) `cli/tui_forms.py:206` `def on_input_submitted(self, event)` -- Enter accepts the highlighted row or the typed custom value.
- `SearchSelectModal.on_option_list_option_selected` (method) `cli/tui_forms.py:211` `def on_option_list_option_selected(self, event)` -- Clicking or pressing Enter on a row selects it.
- `SearchSelectModal.on_key` (method) `cli/tui_forms.py:220` `def on_key(self, event)` -- Move focus into the list with the arrow keys.
- `SearchSelectModal.on_button_pressed` (method) `cli/tui_forms.py:239` `def on_button_pressed(self, event)` -- Select and cancel buttons.
- `ConfirmModal.__init__` (method) `cli/tui_forms.py:256` `def __init__(self, title, body)` -- Store the prompt.
- `ConfirmModal.compose` (method) `cli/tui_forms.py:262` `def compose(self)` -- Prompt plus yes/no buttons.
- `ConfirmModal.action_answer` (method) `cli/tui_forms.py:272` `def action_answer(self, answer)` -- Dismiss with the operator's answer.
- `ConfirmModal.on_button_pressed` (method) `cli/tui_forms.py:276` `def on_button_pressed(self, event)` -- Wire the two buttons to the same answer action.
- `TextEditorModal.__init__` (method) `cli/tui_forms.py:298` `def __init__(self, title, text, validator, language, save_label)` -- Store the title, initial document, validator and language.
- `TextEditorModal.compose` (method) `cli/tui_forms.py:314` `def compose(self)` -- Editor plus save/cancel buttons and an error line.
- `TextEditorModal.on_button_pressed` (method) `cli/tui_forms.py:338` `def on_button_pressed(self, event)` -- Save and cancel buttons.

## cli/tui_theme.py
Depends on: `cli/themes.py`
Imported by: `cli/commands/help_ui.py`
- `run` (function) `cli/tui_theme.py:87` `def run(args, payload, save)` -- Execute the ``tui_theme`` command.


Next: [API_p6.md](API_p6.md)
