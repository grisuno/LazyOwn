# API (page 5 of 24)
Previous: [API_p4.md](API_p4.md)

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
Imported by: `cli/__init__.py`, `lazyown.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_param_registry.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
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
Imported by: `lazyown.py`, `tests/test_scope_guard.py`
- `ScopeMode.from_value` (method) `cli/scope_guard.py:105` `def from_value(cls, value)` -- Coerce an arbitrary payload value into a :class:`ScopeMode`.
- `build_offensive_commands` (function) `cli/scope_guard.py:147` `def build_offensive_commands(command_categories)` -- Select the command names whose category is offensive.
- `normalize_scope` (function) `cli/scope_guard.py:163` `def normalize_scope(entries)` -- Coerce a scope specification into a tuple of entry strings.
- `target_in_scope` (function) `cli/scope_guard.py:218` `def target_in_scope(target, entries)` -- Return whether *target* falls within any of the scope *entries*.
- `ScopeGuard.__init__` (method) `cli/scope_guard.py:263` `def __init__(self, scope_entries, mode, is_offensive)` -- Initialise the guard.
- `ScopeGuard.evaluate` (method) `cli/scope_guard.py:283` `def evaluate(self, command, target)` -- Evaluate a single command against the active target.

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
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `static/js/bootstrap-4.5.2.min.js`, `static/js/bootstrap-5.3.0.bundle.min.js`, `static/js/chart.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/quill-2.0.3.js`, `static/js/tippy-6.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_cli_assign.py`
- `format_payload` (function) `cli/show.py:14` `def format_payload(params)` -- Render ``params`` as a sorted, aligned ``key = value`` block.

## cli/splash.py
Depends on: `cli/style.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_tui_splash.py`
- `SplashEffect.render` (method) `cli/splash.py:71` `def render(self, console, lines, tokens, config)`
- `TypewriterEffect.render` (method) `cli/splash.py:90` `def render(self, console, lines, tokens, config)`
- `InstantEffect.render` (method) `cli/splash.py:150` `def render(self, console, lines, tokens, config)`
- `render_splash` (function) `cli/splash.py:166` `def render_splash(console, lines, payload, config, effect_name)` -- Render the splash overlay and optionally clear the screen.

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
- `build_default_manager` (function) `cli/status_bar.py:969` `def build_default_manager(payload, sessions_dir, advisor_factory, config)` -- Wire the canonical multi-source manager used by the live shell.

## cli/style.py
Depends on: `cli/themes.py`
Imported by: `cli/splash.py`, `static/js/force-graph-1.43.5.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/showdown-2.1.0.min.js`
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
Depends on: `cli/autosuggest.py`, `cli/engagement_hooks.py`, `cli/noise_verbs.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/phase_labels.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/themes.py`, `core/console.py`, `core/logging.py`, `core/safe_console.py`, `core/text_utils.py`, `modules/cli_auth.py`, `modules/killchain.py`, `modules/lazy_rbac.py`
Imported by: `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_auto_refresh.py`, `tests/test_phase_labels.py`, `tests/test_tips_engine.py`
- `TipsEngine.__init__` (method) `cli/tips_engine.py:194` `def __init__(self, config, autosuggest_engine)` -- Wire the engine with its configuration and optional autosuggest handle.
- `TipsEngine.enabled` (method) `cli/tips_engine.py:221` `def enabled(self)` -- Whether the engine renders any output.
- `TipsEngine.set_enabled` (method) `cli/tips_engine.py:225` `def set_enabled(self, value)` -- Toggle rendering without dropping state.
- `TipsEngine.render` (method) `cli/tips_engine.py:229` `def render(self, cmd, phase)` -- Run all surfaces for the given command.
- `TipsEngine.render_session_start` (method) `cli/tips_engine.py:408` `def render_session_start(self, phase, os_id)` -- Print a single tip at session start (once per boot).
- `TipsEngine.get_state_snapshot` (method) `cli/tips_engine.py:440` `def get_state_snapshot(self)` -- Return a read-only snapshot of current engagement state.
- `TipsEngine.reset_session` (method) `cli/tips_engine.py:455` `def reset_session(self)` -- Reset session counters without clearing cross-session progress.
- `TipsEngine.heal_commands_seen` (method) `cli/tips_engine.py:460` `def heal_commands_seen(self, known)` -- Purge non-command entries from persisted ``commands_seen``.
- `build_default_tips_config` (function) `cli/tips_engine.py:1240` `def build_default_tips_config()` -- Build a :class:`TipsConfig` populated from the live framework tables.

## cli/toast_bus.py
Depends on: `cli/themes.py`, `core/console.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/ux.py`, `cli/dashboard_tui.py`, `lazy_sentinel4.py`, `lazyown.py`, `tests/test_lazy_parity.py`, `tests/test_toast_bus.py`, `tests/test_toastr_unify.py`
- `ToastState.__init__` (method) `cli/toast_bus.py:130` `def __init__(self, config, root)` -- Bind to config and resolve the on-disk state path.
- `ToastState.path` (method) `cli/toast_bus.py:145` `def path(self)` -- Return the resolved state-file path.
- `ToastState.get` (method) `cli/toast_bus.py:149` `def get(self, name)` -- Return the persisted offset for ``name`` or 0.
- `ToastState.set` (method) `cli/toast_bus.py:154` `def set(self, name, offset)` -- Record ``offset`` for ``name`` in memory.
- `ToastState.reset` (method) `cli/toast_bus.py:160` `def reset(self)` -- Forget every persisted offset (force replay on next read).
- `ToastState.flush` (method) `cli/toast_bus.py:165` `def flush(self)` -- Persist the current offsets atomically.
- `ToastReader.__init__` (method) `cli/toast_bus.py:207` `def __init__(self, config, root)` -- Bind to config and resolve the events root directory.
- `ToastReader.root` (method) `cli/toast_bus.py:218` `def root(self)` -- Return the resolved events root directory.
- `ToastReader.read_unseen` (method) `cli/toast_bus.py:222` `def read_unseen(self, name, start_offset)` -- Return events emitted past ``start_offset`` plus the new end offset.
- `toastr_severity_style` (function) `cli/toast_bus.py:373` `def toastr_severity_style(severity)` -- Resolve one severity into the shared border/text style pair.
- `rich_toastr_panel` (function) `cli/toast_bus.py:380` `def rich_toastr_panel(message, severity, terminal_width, config)` -- Build the adaptive toastr panel used by the cmd2 shell.
- `shell_hint_bypass` (function) `cli/toast_bus.py:433` `def shell_hint_bypass(console, message, severity)` -- Print the flat bypass line used when UI hints are off.
- `sentinel_toast_panel` (function) `cli/toast_bus.py:452` `def sentinel_toast_panel(file_name, relevant_info, commands, details, severity)` -- Build the yara sentinel popup with the shared styling.
- `ToastFormatter.__init__` (method) `cli/toast_bus.py:490` `def __init__(self, config, theme)` -- Bind to config and the active theme.
- `ToastFormatter.format` (method) `cli/toast_bus.py:495` `def format(self, event)` -- Return a single themed line for ``event``.
- `ToastFormatter.is_prominent` (method) `cli/toast_bus.py:507` `def is_prominent(self, event)` -- Return True when an event deserves a full toastr panel.
- `ToastFormatter.format_prominent` (method) `cli/toast_bus.py:517` `def format_prominent(self, event)` -- Render an event as a toastr panel with the complete summary.
- `ToastFormatter.format_ephemeral` (method) `cli/toast_bus.py:534` `def format_ephemeral(self, event)` -- Return a single sonner-style line with severity icon for ``event``.
- `ToastFormatter.duration_for` (method) `cli/toast_bus.py:562` `def duration_for(self, event)` -- Return the auto-dismiss delay in seconds for ``event``.
- `ToastFormatter.digest_line` (method) `cli/toast_bus.py:587` `def digest_line(dropped)` -- Summarise over-budget events so none vanish silently.
- `ToastFormatter.format_many` (method) `cli/toast_bus.py:595` `def format_many(self, events, width)` -- Render several events as one Rich renderable.
- `ToastBus.__init__` (method) `cli/toast_bus.py:675` `def __init__(self, config, state, reader, formatter, console)` -- Bind every collaborator.
- `ToastBus.collect` (method) `cli/toast_bus.py:690` `def collect(self)` -- Return every unseen event across :attr:`ToastConfig.event_files`.
- `ToastBus.render` (method) `cli/toast_bus.py:702` `def render(self, enabled)` -- Collect, render and persist offsets in a single call.
- `ToastBus.mark_all_seen` (method) `cli/toast_bus.py:731` `def mark_all_seen(self)` -- Advance the offset for every configured file to its current size.
- `ToastBus.render_ephemeral` (method) `cli/toast_bus.py:738` `def render_ephemeral(self, enabled, duration)` -- Collect unseen events and print each as an auto-expiring line.
- `toasts_enabled` (function) `cli/toast_bus.py:836` `def toasts_enabled(payload, config)` -- Return ``True`` when toast rendering is permitted.
- `build_default_bus` (function) `cli/toast_bus.py:859` `def build_default_bus(payload, sessions_dir, console)` -- Wire the canonical bus used by the shell postcmd hook.
- `render_toasts` (function) `cli/toast_bus.py:888` `def render_toasts(payload, sessions_dir, console, bus_factory)` -- One-shot helper used by the cmd2 postcmd hook.
- `ephemeral_enabled` (function) `cli/toast_bus.py:912` `def ephemeral_enabled(payload, config)` -- Return True when toasts must auto-dismiss like sonner.
- `render_ephemeral_toasts` (function) `cli/toast_bus.py:928` `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` -- Collect unseen events and print each as an auto-expiring line.
- `emit_toast` (function) `cli/toast_bus.py:958` `def emit_toast(message, severity, event_type, sessions_dir, config)` -- Append one toast event so the existing render hook displays it.
- `read_recent_toasts` (function) `cli/toast_bus.py:1003` `def read_recent_toasts(sessions_dir, limit, config)` -- Return the most recent toast events without touching read offsets.
- `build_toast_renderable` (function) `cli/toast_bus.py:1047` `def build_toast_renderable(events, payload, width, config)` -- Render events with the active theme for any surface.

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

## cli/tutorial.py
Depends on: `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `is_done` (function) `cli/tutorial.py:83` `def is_done(config)` -- Return True if the tutorial has already been completed.
- `mark_done` (function) `cli/tutorial.py:89` `def mark_done(config)` -- Persist the tutorial completion marker.
- `render_header` (function) `cli/tutorial.py:96` `def render_header()` -- Print the tutorial welcome banner.
- `render_phase_table` (function) `cli/tutorial.py:113` `def render_phase_table()` -- Print the full phase overview before starting.
- `run_step` (function) `cli/tutorial.py:128` `def run_step(index, command, description, why, params, command_runner)` -- Execute one tutorial step and return True if the user wants to continue.
- `run` (function) `cli/tutorial.py:185` `def run(params, command_runner)` -- Run the interactive tutorial.

## cli/wizard.py
Depends on: `cli/marketplace_config.py`, `core/console.py`, `core/payload_schema.py`, `core/profiles.py`, `modules/cli_auth.py`, `modules/llm_factory.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/doctor.py`, `tests/test_doctor.py`, `tests/test_wizard_llm.py`
- `run` (function) `cli/wizard.py:169` `def run(params, save)` -- Run the interactive setup wizard and return a :class:`WizardResult`.
- `run_non_interactive` (function) `cli/wizard.py:234` `def run_non_interactive(params, save, values)` -- Apply configuration without prompts — Docker/CI/headless first runs.
- `check_binaries` (function) `cli/wizard.py:947` `def check_binaries(specs, which)` -- Return the presence status of every spec without executing it.

## cli/wizard_scope.py
Imported by: `cli/commands/help_ui.py`
- `parse_scope` (function) `cli/wizard_scope.py:38` `def parse_scope(tokens, config)` -- Parse --show and --only=a,b flags from wizard tokens.
- `status_rows` (function) `cli/wizard_scope.py:64` `def status_rows(params)` -- Build display rows for the current configuration state.

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

## contrib/legacy/lazyarpspoofing.py
- `check_sudo` (function) `contrib/legacy/lazyarpspoofing.py:27` `def check_sudo()`
- `enable_ip_forward` (function) `contrib/legacy/lazyarpspoofing.py:35` `def enable_ip_forward()`
- `disable_ip_forward` (function) `contrib/legacy/lazyarpspoofing.py:38` `def disable_ip_forward()`
- `get_local_ip` (function) `contrib/legacy/lazyarpspoofing.py:41` `def get_local_ip(ifname)`
- `get_mac` (function) `contrib/legacy/lazyarpspoofing.py:49` `def get_mac(ip, device, retries, timeout)`
- `spoofer` (function) `contrib/legacy/lazyarpspoofing.py:69` `def spoofer(target, spoofed, device)`
- `main` (function) `contrib/legacy/lazyarpspoofing.py:80` `def main()`

## contrib/legacy/lazybinenc.py
Depends on: `cli/commands/pwn.py`, `core/console.py`, `core/prompt.py`
- `generate_key_iv` (function) `contrib/legacy/lazybinenc.py:12` `def generate_key_iv(sessions_path)`
- `main` (function) `contrib/legacy/lazybinenc.py:54` `def main()`

## contrib/legacy/lazybotcli.py
- `encrypt` (function) `contrib/legacy/lazybotcli.py:30` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazybotcli.py:36` `def decrypt(ciphertext, key)`
- `main` (function) `contrib/legacy/lazybotcli.py:42` `def main()`

## contrib/legacy/lazybotnet.py
- `encrypt` (function) `contrib/legacy/lazybotnet.py:46` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazybotnet.py:52` `def decrypt(ciphertext, key)`
- `add_to_botnet` (function) `contrib/legacy/lazybotnet.py:58` `def add_to_botnet(ip, port, botnet_file)`
- `clean_botnet` (function) `contrib/legacy/lazybotnet.py:62` `def clean_botnet(ip, port, botnet_file)`
- `send_to_botnet` (function) `contrib/legacy/lazybotnet.py:71` `def send_to_botnet(cmd, key, botnet_file)`
- `Keylogger.__init__` (method) `contrib/legacy/lazybotnet.py:90` `def __init__(self, key, log_file)`
- `Keylogger.on_press` (method) `contrib/legacy/lazybotnet.py:95` `def on_press(self, key)`
- `Keylogger.start` (method) `contrib/legacy/lazybotnet.py:106` `def start(self)`
- `Keylogger.get_log` (method) `contrib/legacy/lazybotnet.py:110` `def get_log(self)`
- `Keylogger.save_log` (method) `contrib/legacy/lazybotnet.py:113` `def save_log(self)`
- `Keylogger.run` (method) `contrib/legacy/lazybotnet.py:120` `def run(self)`
- `Keylogger.setup_persistence` (method) `contrib/legacy/lazybotnet.py:125` `def setup_persistence(self)`
- `Keylogger.create_shortcut` (method) `contrib/legacy/lazybotnet.py:136` `def create_shortcut(self, script_path, shortcut_path)`
- `handle_client` (function) `contrib/legacy/lazybotnet.py:144` `def handle_client(conn, key, botnet_file, log_file)`
- `start_server` (function) `contrib/legacy/lazybotnet.py:182` `def start_server(host, port, key, botnet_file, log_file)`

## contrib/legacy/lazycam.py
- `RTSPScanner.__init__` (method) `contrib/legacy/lazycam.py:33` `def __init__(self, verbose, wspace)`
- `RTSPScanner.run` (method) `contrib/legacy/lazycam.py:49` `def run(self)`
- `RTSPScanner.resizeImg` (method) `contrib/legacy/lazycam.py:68` `def resizeImg(self, img, output, height, ratio, fmt)`
- `RTSPScanner.splitCSV` (method) `contrib/legacy/lazycam.py:77` `def splitCSV(self, csv)`
- `RTSPScanner.scanner` (method) `contrib/legacy/lazycam.py:83` `def scanner(self)`
- `RTSPScanner.delCameras` (method) `contrib/legacy/lazycam.py:136` `def delCameras(self)`
- `RTSPScanner.addCameras` (method) `contrib/legacy/lazycam.py:149` `def addCameras(self)`
- `cla` (function) `contrib/legacy/lazycam.py:212` `def cla()`
- `main` (function) `contrib/legacy/lazycam.py:257` `def main()`

## contrib/legacy/lazydeepseekcli.py
Depends on: `core/logging.py`
Imported by: `modules/llm_adapter.py`, `tests/test_c2_surfaces.py`
- `truncate_message` (function) `contrib/legacy/lazydeepseekcli.py:41` `def truncate_message(message, max_chars)`
- `configure_logging` (function) `contrib/legacy/lazydeepseekcli.py:45` `def configure_logging(debug)`
- `load_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:167` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:174` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:179` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazydeepseekcli.py:185` `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function) `contrib/legacy/lazydeepseekcli.py:193` `def transform_knowledge_base(prompt_builder)`
- `generate` (function) `contrib/legacy/lazydeepseekcli.py:232` `def generate()`
- `process_prompt_local` (function) `contrib/legacy/lazydeepseekcli.py:261` `def process_prompt_local(prompt, debug, mode)`
- `process_prompt_localreport` (function) `contrib/legacy/lazydeepseekcli.py:269` `def process_prompt_localreport(prompt, debug, mode)`
- `parse_args` (function) `contrib/legacy/lazydeepseekcli.py:277` `def parse_args()`

## contrib/legacy/lazydisassebler.py
- `X64Disassembler.__init__` (method) `contrib/legacy/lazydisassebler.py:34` `def __init__(self)` -- Initializes the X64Disassembler instance.
- `X64Disassembler.read_elf_header` (method) `contrib/legacy/lazydisassebler.py:79` `def read_elf_header(self, data)` -- Reads the ELF header and finds the code section.
- `X64Disassembler.parse_modrm` (method) `contrib/legacy/lazydisassebler.py:135` `def parse_modrm(self, modrm, rex)` -- Parses the ModR/M byte and extracts mod, reg, and rm fields.
- `X64Disassembler.parse_sib` (method) `contrib/legacy/lazydisassebler.py:173` `def parse_sib(self, sib, rex)` -- Parses the SIB byte and extracts scale, index, and base fields.
- `X64Disassembler.get_operand_str` (method) `contrib/legacy/lazydisassebler.py:212` `def get_operand_str(self, mod, rm, rex, bytes_data, offset)` -- Gets the string representation of the operand based on mod/rm.
- `X64Disassembler.disassemble` (method) `contrib/legacy/lazydisassebler.py:305` `def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point)` -- Main disassembler for x86-64 code.
- `main` (function) `contrib/legacy/lazydisassebler.py:489` `def main()` -- Main function for the disassembler.

## contrib/legacy/lazyftpsniff.py
- `check_sudo` (function) `contrib/legacy/lazyftpsniff.py:21` `def check_sudo()`
- `signal_handler` (function) `contrib/legacy/lazyftpsniff.py:34` `def signal_handler(sig, frame)`
- `parse_arguments` (function) `contrib/legacy/lazyftpsniff.py:42` `def parse_arguments()`
- `sniffer_ftp` (function) `contrib/legacy/lazyftpsniff.py:56` `def sniffer_ftp(pkt)`
- `main` (function) `contrib/legacy/lazyftpsniff.py:69` `def main()`

## contrib/legacy/lazygalazy.py
Depends on: `modules/backdoor/server.c`
- `SamsungKnoxExploitServer.do_GET` (method) `contrib/legacy/lazygalazy.py:11` `def do_GET(self)`
- `SamsungKnoxExploitServer.apk_bytes` (method) `contrib/legacy/lazygalazy.py:33` `def apk_bytes(self)`
- `SamsungKnoxExploitServer.launch_html` (method) `contrib/legacy/lazygalazy.py:36` `def launch_html(self)`
- `SamsungKnoxExploitServer.exploit_js` (method) `contrib/legacy/lazygalazy.py:49` `def exploit_js(self)`
- `SamsungKnoxExploitServer.rand_word` (method) `contrib/legacy/lazygalazy.py:93` `def rand_word(self)`
- `main` (function) `contrib/legacy/lazygalazy.py:97` `def main()`

## contrib/legacy/lazygptcli.py
Depends on: `contrib/legacy/lazygptcli_unified.py`, `core/logging.py`, `modules/colors.py`
- `signal_handler` (function) `contrib/legacy/lazygptcli.py:66` `def signal_handler(sig, frame)`
- `show_help` (function) `contrib/legacy/lazygptcli.py:73` `def show_help(message)`
- `check_api_key` (function) `contrib/legacy/lazygptcli.py:77` `def check_api_key()`
- `configure_logging` (function) `contrib/legacy/lazygptcli.py:83` `def configure_logging(debug)`
- `parse_args` (function) `contrib/legacy/lazygptcli.py:87` `def parse_args()`
- `create_complex_prompt` (function) `contrib/legacy/lazygptcli.py:94` `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function) `contrib/legacy/lazygptcli.py:108` `def execute_command(command)`
- `load_knowledge_base` (function) `contrib/legacy/lazygptcli.py:118` `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function) `contrib/legacy/lazygptcli.py:124` `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function) `contrib/legacy/lazygptcli.py:128` `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function) `contrib/legacy/lazygptcli.py:133` `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function) `contrib/legacy/lazygptcli.py:141` `def transform_knowledge_base(client)`
- `cleanup_temp_files` (function) `contrib/legacy/lazygptcli.py:164` `def cleanup_temp_files()`
- `main` (function) `contrib/legacy/lazygptcli.py:177` `def main()`

## contrib/legacy/lazygptcli_unified.py
Depends on: `core/logging.py`, `modules/colors.py`
Imported by: `contrib/legacy/lazygptcli.py`
- `truncate_message` (function) `contrib/legacy/lazygptcli_unified.py:53` `def truncate_message(message, max_chars)`
- `process_prompt` (function) `contrib/legacy/lazygptcli_unified.py:318` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `contrib/legacy/lazygptcli_unified.py:323` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `contrib/legacy/lazygptcli_unified.py:328` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `contrib/legacy/lazygptcli_unified.py:333` `def process_prompt_general(client, prompt, debug)` -- General red team assistant with payload.json context and DeepSeek fallback.
- `process_prompt_search` (function) `contrib/legacy/lazygptcli_unified.py:341` `def process_prompt_search(client, prompt, debug)` -- Research and threat intelligence analysis.
- `process_prompt_task` (function) `contrib/legacy/lazygptcli_unified.py:346` `def process_prompt_task(client, prompt, debug)` -- Analyze task assessment JSON for completion status and next commands.
- `process_prompt_vuln` (function) `contrib/legacy/lazygptcli_unified.py:356` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and generate penetration test action plan.
- `process_prompt_redop` (function) `contrib/legacy/lazygptcli_unified.py:382` `def process_prompt_redop(client, prompt, debug)` -- Evaluate Red Team operation status from JSON database params.

## contrib/legacy/lazyhoneypot.py
Depends on: `core/logging.py`
- `parse_args` (function) `contrib/legacy/lazyhoneypot.py:34` `def parse_args()`
- `setup_logging` (function) `contrib/legacy/lazyhoneypot.py:52` `def setup_logging(log_file)`
- `generate_rsa_key` (function) `contrib/legacy/lazyhoneypot.py:56` `def generate_rsa_key(key_filename)`
- `Server.__init__` (method) `contrib/legacy/lazyhoneypot.py:61` `def __init__(self)`
- `Server.check_channel_request` (method) `contrib/legacy/lazyhoneypot.py:64` `def check_channel_request(self, kind, chanid)`
- `Server.check_auth_password` (method) `contrib/legacy/lazyhoneypot.py:69` `def check_auth_password(self, username, password)`
- `handle_connection` (function) `contrib/legacy/lazyhoneypot.py:74` `def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir)`
- `handle_file_download` (function) `contrib/legacy/lazyhoneypot.py:110` `def handle_file_download(command, downloads_dir, downloads_log)`
- `log_command` (function) `contrib/legacy/lazyhoneypot.py:128` `def log_command(command, commands_log)`
- `log_downloaded_file` (function) `contrib/legacy/lazyhoneypot.py:132` `def log_downloaded_file(filename, url, downloads_log)`
- `analyze_traffic` (function) `contrib/legacy/lazyhoneypot.py:136` `def analyze_traffic()`
- `process_packet` (function) `contrib/legacy/lazyhoneypot.py:137` `def process_packet(packet)`
- `alert_admin` (function) `contrib/legacy/lazyhoneypot.py:147` `def alert_admin(message)`
- `main` (function) `contrib/legacy/lazyhoneypot.py:165` `def main()`

## contrib/legacy/lazyhttpreverseshell.py
Depends on: `modules/backdoor/server.c`
- `encrypt` (function) `contrib/legacy/lazyhttpreverseshell.py:14` `def encrypt(data)`
- `decrypt` (function) `contrib/legacy/lazyhttpreverseshell.py:17` `def decrypt(data)`
- `compress` (function) `contrib/legacy/lazyhttpreverseshell.py:20` `def compress(data)`
- `decompress` (function) `contrib/legacy/lazyhttpreverseshell.py:23` `def decompress(data)`
- `reverse_http_shell_client` (function) `contrib/legacy/lazyhttpreverseshell.py:26` `def reverse_http_shell_client(lhost, rhost, rport)`
- `reverse_http_shell_server` (function) `contrib/legacy/lazyhttpreverseshell.py:50` `def reverse_http_shell_server(lhost, lport)`
- `RequestHandler.do_GET` (method) `contrib/legacy/lazyhttpreverseshell.py:52` `def do_GET(self)`
- `RequestHandler.do_POST` (method) `contrib/legacy/lazyhttpreverseshell.py:65` `def do_POST(self)`
- `parse_arguments` (function) `contrib/legacy/lazyhttpreverseshell.py:88` `def parse_arguments(args)`

## contrib/legacy/lazykeygen.py
- `pad` (function) `contrib/legacy/lazykeygen.py:8` `def pad(s)`
- `encrypt` (function) `contrib/legacy/lazykeygen.py:11` `def encrypt(plaintext, key)`
- `decrypt` (function) `contrib/legacy/lazykeygen.py:17` `def decrypt(ciphertext, key)`
- `generate_key` (function) `contrib/legacy/lazykeygen.py:23` `def generate_key(length)`
- `main` (function) `contrib/legacy/lazykeygen.py:26` `def main()`

## contrib/legacy/lazylfi2rce.py
- `signal_handler` (function) `contrib/legacy/lazylfi2rce.py:29` `def signal_handler(sig, frame)`
- `check_lfi_success` (function) `contrib/legacy/lazylfi2rce.py:35` `def check_lfi_success(response_text)`
- `check_rfi_success` (function) `contrib/legacy/lazylfi2rce.py:39` `def check_rfi_success(response_text)`
- `main` (function) `contrib/legacy/lazylfi2rce.py:43` `def main()`


Next: [API_p6.md](API_p6.md)
