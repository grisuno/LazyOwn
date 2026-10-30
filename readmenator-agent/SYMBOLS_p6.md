# Symbols (page 6 of 48)
Previous: [SYMBOLS_p5.md](SYMBOLS_p5.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `propose` | method | `cli/recommendation_signals.py:244` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:356` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:410` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:546` | `def propose(self, ctx)` |
| `read_recent_commands` | function | `cli/recommendation_signals.py:276` | `def read_recent_commands(sessions_dir, window)` |
| `recommend_with_evidence` | function | `cli/recommendation_signals.py:706` | `def recommend_with_evidence(payload, sessions_dir, target, phase, limit, engine)` |
| `ReconPlan` | class | `cli/recon_plan.py:119` | `class ReconPlan` |
| `ReconPlanConfig` | class | `cli/recon_plan.py:62` | `class ReconPlanConfig` |
| `ReconPlanItem` | class | `cli/recon_plan.py:94` | `class ReconPlanItem` |
| `_addon_items` | function | `cli/recon_plan.py:330` | `def _addon_items(addons, services, payload)` |
| `_command_items` | function | `cli/recon_plan.py:367` | `def _command_items(index, phase, history, limit)` |
| `_default_command_index_loader` | function | `cli/recon_plan.py:494` | `def _default_command_index_loader(path)` |
| `_payload_target` | function | `cli/recon_plan.py:466` | `def _payload_target(payload, config)` |
| `_read_tool_command` | function | `cli/recon_plan.py:449` | `def _read_tool_command(source_path)` |
| `_resolve_phase` | function | `cli/recon_plan.py:474` | `def _resolve_phase(payload, config)` |
| `_safe_filename_component` | function | `cli/recon_plan.py:486` | `def _safe_filename_component(value)` |
| `_service_for_trigger` | function | `cli/recon_plan.py:414` | `def _service_for_trigger(trigger, services)` |
| `_tool_command_preview` | function | `cli/recon_plan.py:428` | `def _tool_command_preview(tool, payload)` |
| `_tool_items` | function | `cli/recon_plan.py:347` | `def _tool_items(tools, services, payload)` |
| `build_recon_plan` | function | `cli/recon_plan.py:144` | `def build_recon_plan(target, engine, payload, config, command_index_loader, clock)` |
| `is_empty` | method | `cli/recon_plan.py:139` | `def is_empty(self)` |
| `render_markdown` | function | `cli/recon_plan.py:207` | `def render_markdown(plan)` |
| `render_rich` | function | `cli/recon_plan.py:299` | `def render_rich(plan, console)` |
| `write_plan` | function | `cli/recon_plan.py:257` | `def write_plan(plan, sessions_dir, config)` |
| `iter_command_sets` | function | `cli/registry.py:41` | `def iter_command_sets(include_pending)` |
| `register_command_sets` | function | `cli/registry.py:77` | `def register_command_sets(shell)` |
| `LastTask` | class | `cli/retry_support.py:62` | `class LastTask` |
| `RetryChainReport` | class | `cli/retry_support.py:164` | `class RetryChainReport` |
| `_chain_state_when_disabled` | function | `cli/retry_support.py:268` | `def _chain_state_when_disabled(chain_name)` |
| `consent_to_elevate` | function | `cli/retry_support.py:129` | `def consent_to_elevate(rest, confirmer)` |
| `known` | method | `cli/retry_support.py:76` | `def known(self)` |
| `last_loop_task` | function | `cli/retry_support.py:81` | `def last_loop_task()` |
| `looks_like_run_id` | function | `cli/retry_support.py:45` | `def looks_like_run_id(token)` |
| `retry_chain` | function | `cli/retry_support.py:204` | `def retry_chain(chain_or_run, shell, extra_vars, dry_run)` |
| `status_snapshot` | function | `cli/retry_support.py:104` | `def status_snapshot(limit)` |
| `to_dict` | method | `cli/retry_support.py:189` | `def to_dict(self)` |
| `ScopeDecision` | class | `cli/scope_guard.py:125` | `class ScopeDecision` |
| `ScopeGuard` | class | `cli/scope_guard.py:271` | `class ScopeGuard` |
| `ScopeMode` | class | `cli/scope_guard.py:90` | `class ScopeMode(StrEnum)` |
| `__init__` | method | `cli/scope_guard.py:280` | `def __init__(self, scope_entries, mode, is_offensive, deny_entries)` |
| `_hostname_match` | function | `cli/scope_guard.py:209` | `def _hostname_match(target, entry)` |
| `_parse_ip` | function | `cli/scope_guard.py:195` | `def _parse_ip(value)` |
| `_parse_network` | function | `cli/scope_guard.py:202` | `def _parse_network(value)` |
| `build_offensive_commands` | function | `cli/scope_guard.py:147` | `def build_offensive_commands(command_categories)` |
| `evaluate` | method | `cli/scope_guard.py:304` | `def evaluate(self, command, target)` |
| `from_value` | method | `cli/scope_guard.py:105` | `def from_value(cls, value)` |
| `normalize_scope` | function | `cli/scope_guard.py:163` | `def normalize_scope(entries)` |
| `target_in_deny` | function | `cli/scope_guard.py:254` | `def target_in_deny(target, entries)` |
| `target_in_scope` | function | `cli/scope_guard.py:218` | `def target_in_scope(target, entries)` |
| `SessionBriefConfig` | class | `cli/session_brief.py:35` | `class SessionBriefConfig` |
| `_redirect_world_model_env` | function | `cli/session_brief.py:55` | `def _redirect_world_model_env(payload)` |
| `_task_line` | function | `cli/session_brief.py:94` | `def _task_line(rows)` |
| `_trigger_line` | function | `cli/session_brief.py:115` | `def _trigger_line()` |
| `_verb_line` | function | `cli/session_brief.py:104` | `def _verb_line()` |
| `_world_line` | function | `cli/session_brief.py:68` | `def _world_line(payload)` |
| `brief_enabled` | function | `cli/session_brief.py:47` | `def brief_enabled(payload)` |
| `build_session_brief` | function | `cli/session_brief.py:127` | `def build_session_brief(payload, tasks)` |
| `fetch_task_rows` | function | `cli/session_brief.py:84` | `def fetch_task_rows()` |
| `print_session_brief` | function | `cli/session_brief.py:163` | `def print_session_brief(console, payload)` |
| `HudConfig` | class | `cli/session_hud.py:25` | `class HudConfig` |
| `HudSnapshot` | class | `cli/session_hud.py:50` | `class HudSnapshot` |
| `_engagement_facts` | function | `cli/session_hud.py:135` | `def _engagement_facts()` |
| `build_snapshot` | function | `cli/session_hud.py:155` | `def build_snapshot(params, config)` |
| `count_csv_rows` | function | `cli/session_hud.py:83` | `def count_csv_rows(path)` |
| `count_lines_in_globs` | function | `cli/session_hud.py:62` | `def count_lines_in_globs(root, patterns)` |
| `format_elapsed` | function | `cli/session_hud.py:100` | `def format_elapsed(seconds)` |
| `phase_bar` | function | `cli/session_hud.py:115` | `def phase_bar(phase, width)` |
| `render_snapshot` | function | `cli/session_hud.py:180` | `def render_snapshot(snapshot, config)` |
| `SessionResumer` | class | `cli/session_resumer.py:50` | `class SessionResumer` |
| `SessionResumerConfig` | class | `cli/session_resumer.py:40` | `class SessionResumerConfig` |
| `SessionSummary` | class | `cli/session_resumer.py:28` | `class SessionSummary` |
| `__init__` | method | `cli/session_resumer.py:57` | `def __init__(self, config)` |
| `_discover_targets` | method | `cli/session_resumer.py:61` | `def _discover_targets(self)` |
| `render_startup_panel` | method | `cli/session_resumer.py:130` | `def render_startup_panel(self)` |
| `CategorySpec` | class | `cli/sessions_browser.py:33` | `class CategorySpec` |
| `SessionEntry` | class | `cli/sessions_browser.py:76` | `class SessionEntry` |
| `SessionPreview` | class | `cli/sessions_browser.py:185` | `class SessionPreview` |
| `SessionsBrowserConfig` | class | `cli/sessions_browser.py:49` | `class SessionsBrowserConfig` |
| `SessionsBrowserState` | class | `cli/sessions_browser.py:225` | `class SessionsBrowserState` |
| `SessionsIndex` | class | `cli/sessions_browser.py:85` | `class SessionsIndex` |
| `_SessionsBrowserApp` | class | `cli/sessions_browser.py:325` | `class _SessionsBrowserApp(App)` |
| `__init__` | method | `cli/sessions_browser.py:88` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/sessions_browser.py:188` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/sessions_browser.py:340` | `def __init__(self)` |
| `_build_app` | function | `cli/sessions_browser.py:314` | `def _build_app(state, theme)` |
| `_build_entry` | method | `cli/sessions_browser.py:160` | `def _build_entry(self, path, relative, category)` |
| `_collect_other` | method | `cli/sessions_browser.py:142` | `def _collect_other(self, claimed)` |
| `_entries_for` | method | `cli/sessions_browser.py:119` | `def _entries_for(self, patterns, spec)` |
| `_label` | method | `cli/sessions_browser.py:172` | `def _label(self, relative)` |
| `_rebuild_tree` | method | `cli/sessions_browser.py:376` | `def _rebuild_tree(self)` |
| `_relative` | method | `cli/sessions_browser.py:178` | `def _relative(self, path)` |
| `_show_preview` | method | `cli/sessions_browser.py:399` | `def _show_preview(self, relative)` |
| `action_close` | method | `cli/sessions_browser.py:373` | `def action_close(self)` |
| `action_refresh` | method | `cli/sessions_browser.py:370` | `def action_refresh(self)` |
| `build_state` | function | `cli/sessions_browser.py:258` | `def build_state(payload, sessions_dir, config)` |
| `categories` | method | `cli/sessions_browser.py:104` | `def categories(self)` |
| `category_label` | method | `cli/sessions_browser.py:248` | `def category_label(self, identifier)` |
| `compose` | method | `cli/sessions_browser.py:346` | `def compose(self)` |
| `grouped_entries` | method | `cli/sessions_browser.py:233` | `def grouped_entries(self)` |
| `launch_browser` | function | `cli/sessions_browser.py:281` | `def launch_browser(payload, state, runner)` |
| `on_input_changed` | method | `cli/sessions_browser.py:359` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/sessions_browser.py:356` | `def on_mount(self)` |
| `on_tree_node_selected` | method | `cli/sessions_browser.py:363` | `def on_tree_node_selected(self, event)` |
| `read` | method | `cli/sessions_browser.py:193` | `def read(self, relative)` |
| `root` | method | `cli/sessions_browser.py:100` | `def root(self)` |
| `format_payload` | function | `cli/show.py:14` | `def format_payload(params)` |
| `InstantEffect` | class | `cli/splash.py:141` | `class InstantEffect` |
| `SplashConfig` | class | `cli/splash.py:37` | `class SplashConfig` |
| `SplashEffect` | class | `cli/splash.py:62` | `class SplashEffect(Protocol)` |
| `TypewriterEffect` | class | `cli/splash.py:80` | `class TypewriterEffect` |
| `_redraw` | function | `cli/splash.py:119` | `def _redraw(console, accumulated, caret, tokens)` |
| `render` | method | `cli/splash.py:71` | `def render(self, console, lines, tokens, config)` |
| `render` | method | `cli/splash.py:90` | `def render(self, console, lines, tokens, config)` |
| `render` | method | `cli/splash.py:150` | `def render(self, console, lines, tokens, config)` |
| `render_splash` | function | `cli/splash.py:166` | `def render_splash(console, lines, payload, config, effect_name)` |
| `CollabPresenceSource` | class | `cli/status_bar.py:592` | `class CollabPresenceSource` |
| `CommandHintSuggestionSource` | class | `cli/status_bar.py:418` | `class CommandHintSuggestionSource` |
| `FileSystemReader` | class | `cli/status_bar.py:151` | `class FileSystemReader` |
| `GraphSuggestionSource` | class | `cli/status_bar.py:510` | `class GraphSuggestionSource` |
| `IStatusSource` | class | `cli/status_bar.py:143` | `class IStatusSource(Protocol)` |
| `PayloadTargetSource` | class | `cli/status_bar.py:268` | `class PayloadTargetSource` |
| `SessionFindingSource` | class | `cli/status_bar.py:321` | `class SessionFindingSource` |
| `StatusBarConfig` | class | `cli/status_bar.py:41` | `class StatusBarConfig` |
| `StatusBarManager` | class | `cli/status_bar.py:746` | `class StatusBarManager` |
| `StatusBarRenderer` | class | `cli/status_bar.py:658` | `class StatusBarRenderer` |
| `StatusContext` | class | `cli/status_bar.py:127` | `class StatusContext` |
| `WorldModelPhaseSource` | class | `cli/status_bar.py:292` | `class WorldModelPhaseSource` |
| `__init__` | method | `cli/status_bar.py:160` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/status_bar.py:271` | `def __init__(self, config, payload)` |
| `__init__` | method | `cli/status_bar.py:295` | `def __init__(self, config, reader, payload)` |
| `__init__` | method | `cli/status_bar.py:324` | `def __init__(self, config, reader)` |
| `__init__` | method | `cli/status_bar.py:428` | `def __init__(self, config, reader, phase_provider, hint_provider)` |
| `__init__` | method | `cli/status_bar.py:513` | `def __init__(self, config, reader, advisor_factory)` |
| `__init__` | method | `cli/status_bar.py:603` | `def __init__(self, config, reader, clock)` |
| `__init__` | method | `cli/status_bar.py:661` | `def __init__(self, config)` |
| `__init__` | method | `cli/status_bar.py:754` | `def __init__(self, config, sources, renderer, payload)` |
| `_build_precmd_hook` | method | `cli/status_bar.py:897` | `def _build_precmd_hook(self, shell, base_prompt, base_prompt_attribute, prompt_attribute)` |
| `_default_provider` | method | `cli/status_bar.py:502` | `def _default_provider()` |
| `_extract_entries` | method | `cli/status_bar.py:638` | `def _extract_entries(payload)` |
| `_extract_vuln_items` | method | `cli/status_bar.py:398` | `def _extract_vuln_items(self, payload)` |
| `_fallback_for` | method | `cli/status_bar.py:940` | `def _fallback_for(self, key)` |
| `_has_traversal` | method | `cli/status_bar.py:261` | `def _has_traversal(value)` |
| `_hook` | function | `cli/status_bar.py:917` | `def _hook(data)` |
| `_is_active` | method | `cli/status_bar.py:648` | `def _is_active(entry, threshold)` |
| `_is_within_root` | method | `cli/status_bar.py:253` | `def _is_within_root(self, candidate)` |
| `_last_line` | method | `cli/status_bar.py:378` | `def _last_line(self, path)` |
| `_latest_command` | method | `cli/status_bar.py:478` | `def _latest_command(self)` |
| `_latest_credential` | method | `cli/status_bar.py:337` | `def _latest_credential(self)` |
| `_latest_note` | method | `cli/status_bar.py:360` | `def _latest_note(self)` |
| `_latest_vuln` | method | `cli/status_bar.py:347` | `def _latest_vuln(self)` |
| `_operator_presence_enabled` | function | `cli/status_bar.py:950` | `def _operator_presence_enabled(payload, config)` |
| `_recent_commands` | method | `cli/status_bar.py:553` | `def _recent_commands(self)` |
| `_resolve_theme_colors` | method | `cli/status_bar.py:825` | `def _resolve_theme_colors(self)` |
| `_safe_collect` | method | `cli/status_bar.py:931` | `def _safe_collect(self, key)` |
| `_safe_path` | method | `cli/status_bar.py:247` | `def _safe_path(self, relative)` |
| `_sanitise` | method | `cli/status_bar.py:726` | `def _sanitise(self, value, max_chars)` |
| `_suggestion_label` | method | `cli/status_bar.py:581` | `def _suggestion_label(entry)` |
| `_summarise_credential` | method | `cli/status_bar.py:391` | `def _summarise_credential(self, filename, line)` |
| `build_default_manager` | function | `cli/status_bar.py:971` | `def build_default_manager(payload, sessions_dir, advisor_factory, config)` |
| `collect` | method | `cli/status_bar.py:146` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:283` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:306` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:329` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:453` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:532` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:624` | `def collect(self)` |
| `collect_context` | method | `cli/status_bar.py:800` | `def collect_context(self)` |
| `enabled` | method | `cli/status_bar.py:785` | `def enabled(self)` |
| `from_payload` | method | `cli/status_bar.py:99` | `def from_payload(cls, payload)` |
| `glob_latest` | method | `cli/status_bar.py:222` | `def glob_latest(self, pattern)` |
| `install` | method | `cli/status_bar.py:859` | `def install(self, shell, base_prompt_attribute, prompt_attribute)` |
| `read_json` | method | `cli/status_bar.py:204` | `def read_json(self, relative)` |
| `read_text` | method | `cli/status_bar.py:183` | `def read_text(self, relative)` |
| `render_plain` | method | `cli/status_bar.py:666` | `def render_plain(self, ctx)` |
| `render_plain_line` | method | `cli/status_bar.py:835` | `def render_plain_line(self, ctx)` |
| `render_prompt` | method | `cli/status_bar.py:689` | `def render_prompt(self, ctx, base_prompt, color_open, color_close, readline_safe)` |
| `render_prompt` | method | `cli/status_bar.py:813` | `def render_prompt(self, base_prompt, readline_safe)` |
| `root` | method | `cli/status_bar.py:179` | `def root(self)` |
| `set_enabled` | method | `cli/status_bar.py:849` | `def set_enabled(self, enabled)` |
| `active_tokens` | function | `cli/style.py:68` | `def active_tokens(payload)` |
| `paint` | function | `cli/style.py:84` | `def paint(text, token, payload)` |
| `render_prompt` | function | `cli/style.py:98` | `def render_prompt(console, segments, payload)` |
| `style` | function | `cli/style.py:49` | `def style(token, theme)` |
| `SurfaceEdge` | class | `cli/surface_graph.py:113` | `class SurfaceEdge` |
| `SurfaceGraph` | class | `cli/surface_graph.py:126` | `class SurfaceGraph` |
| `SurfaceGraphBuilder` | class | `cli/surface_graph.py:196` | `class SurfaceGraphBuilder` |
| `SurfaceGraphConfig` | class | `cli/surface_graph.py:174` | `class SurfaceGraphConfig` |
| `SurfaceNode` | class | `cli/surface_graph.py:87` | `class SurfaceNode` |
| `__init__` | method | `cli/surface_graph.py:199` | `def __init__(self, config)` |
| `_build_c2_node` | method | `cli/surface_graph.py:341` | `def _build_c2_node(self, local_ips, payload)` |
| `_client_label` | method | `cli/surface_graph.py:622` | `def _client_label(client_id, meta)` |
| `_discover_local_ips` | method | `cli/surface_graph.py:359` | `def _discover_local_ips(self)` |
| `_fallback_local_ips` | method | `cli/surface_graph.py:380` | `def _fallback_local_ips()` |
| `_is_ipv4` | method | `cli/surface_graph.py:616` | `def _is_ipv4(value)` |
| `_kind_order` | method | `cli/surface_graph.py:331` | `def _kind_order(kind)` |
| `_load_payload` | method | `cli/surface_graph.py:386` | `def _load_payload(self)` |
| `_parse_implant_row` | method | `cli/surface_graph.py:559` | `def _parse_implant_row(self, row)` |
| `_parse_port_scan` | method | `cli/surface_graph.py:580` | `def _parse_port_scan(self, raw)` |
| `_read_hostsdiscovery` | method | `cli/surface_graph.py:414` | `def _read_hostsdiscovery(self, local_ips)` |
| `_read_implants` | method | `cli/surface_graph.py:525` | `def _read_implants(self)` |
| `_read_last_implant_row` | method | `cli/surface_graph.py:542` | `def _read_last_implant_row(self, path)` |
| `_read_os_hint` | method | `cli/surface_graph.py:399` | `def _read_os_hint(self)` |
| `_read_scan_csv` | method | `cli/surface_graph.py:442` | `def _read_scan_csv(self, local_ips)` |
| `_read_scan_discovery` | method | `cli/surface_graph.py:436` | `def _read_scan_discovery(self, local_ips)` |
| `_read_scan_nmap` | method | `cli/surface_graph.py:467` | `def _read_scan_nmap(self, local_ips)` |
| `_slug_host` | function | `cli/surface_graph.py:75` | `def _slug_host(ip)` |
| `_slug_port` | function | `cli/surface_graph.py:80` | `def _slug_port(host_id, port, protocol)` |
| `build` | method | `cli/surface_graph.py:202` | `def build(self)` |
| `build_surface_graph` | function | `cli/surface_graph.py:633` | `def build_surface_graph(sessions_dir, payload_path)` |
| `children_of` | method | `cli/surface_graph.py:153` | `def children_of(self, node_id)` |
| `get` | method | `cli/surface_graph.py:165` | `def get(self, node_id)` |
| `iter_descendants` | function | `cli/surface_graph.py:650` | `def iter_descendants(graph, root_id)` |
| `stats` | method | `cli/surface_graph.py:146` | `def stats(self)` |
| `to_dict` | method | `cli/surface_graph.py:102` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:120` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:135` | `def to_dict(self)` |
| `SurfaceExplorer` | class | `cli/surface_tui.py:130` | `class SurfaceExplorer(App)` |
| `TextualNotInstalled` | class | `cli/surface_tui.py:61` | `class TextualNotInstalled(RuntimeError)` |
| `__init__` | method | `cli/surface_tui.py:148` | `def __init__(self, sessions_dir, payload_path)` |
| `_add_children` | method | `cli/surface_tui.py:205` | `def _add_children(self, parent_node, graph, parent_id)` |
| `_attach_children` | function | `cli/surface_tui.py:223` | `def _attach_children(parent, graph, parent_id, seen)` |
| `_build_rich_tree` | function | `cli/surface_tui.py:214` | `def _build_rich_tree(graph)` |
| `_reload_graph` | method | `cli/surface_tui.py:185` | `def _reload_graph(self)` |
| `_render_node_detail` | function | `cli/surface_tui.py:260` | `def _render_node_detail(data)` |
| `_stats_table` | function | `cli/surface_tui.py:241` | `def _stats_table(graph)` |
| `_styled_label` | function | `cli/surface_tui.py:232` | `def _styled_label(node)` |
| `action_collapse_all` | method | `cli/surface_tui.py:172` | `def action_collapse_all(self)` |
| `action_expand_all` | method | `cli/surface_tui.py:168` | `def action_expand_all(self)` |
| `action_refresh` | method | `cli/surface_tui.py:164` | `def action_refresh(self)` |
| `compose` | method | `cli/surface_tui.py:154` | `def compose(self)` |
| `launch_tui` | function | `cli/surface_tui.py:112` | `def launch_tui(sessions_dir, payload_path)` |
| `on_mount` | method | `cli/surface_tui.py:161` | `def on_mount(self)` |
| `on_tree_node_selected` | method | `cli/surface_tui.py:176` | `def on_tree_node_selected(self, event)` |
| `render_json` | function | `cli/surface_tui.py:92` | `def render_json(graph, sessions_dir, payload_path)` |
| `render_static` | function | `cli/surface_tui.py:65` | `def render_static(graph, sessions_dir, payload_path, console)` |
| `Theme` | class | `cli/themes.py:31` | `class Theme` |
| `get_theme` | function | `cli/themes.py:222` | `def get_theme(name)` |
| `theme_from_payload` | function | `cli/themes.py:238` | `def theme_from_payload(payload)` |
| `TimelineColumn` | class | `cli/timeline_browser.py:33` | `class TimelineColumn` |
| `TimelineConfig` | class | `cli/timeline_browser.py:43` | `class TimelineConfig` |
| `TimelineEntry` | class | `cli/timeline_browser.py:65` | `class TimelineEntry` |
| `TimelineReader` | class | `cli/timeline_browser.py:72` | `class TimelineReader` |
| `TimelineState` | class | `cli/timeline_browser.py:122` | `class TimelineState` |
| `_TimelineBrowserApp` | class | `cli/timeline_browser.py:213` | `class _TimelineBrowserApp(App)` |
| `__init__` | method | `cli/timeline_browser.py:75` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/timeline_browser.py:228` | `def __init__(self)` |
| `_build_app` | function | `cli/timeline_browser.py:202` | `def _build_app(state, theme)` |
| `_coerce_row` | method | `cli/timeline_browser.py:103` | `def _coerce_row(self, row)` |
| `_rebuild_rows` | method | `cli/timeline_browser.py:266` | `def _rebuild_rows(self)` |
| `_refresh_detail` | method | `cli/timeline_browser.py:278` | `def _refresh_detail(self, row_index)` |
| `action_close` | method | `cli/timeline_browser.py:263` | `def action_close(self)` |
| `action_refresh` | method | `cli/timeline_browser.py:259` | `def action_refresh(self)` |
| `build_state` | function | `cli/timeline_browser.py:157` | `def build_state(payload, sessions_dir, config)` |
| `column_value` | method | `cli/timeline_browser.py:148` | `def column_value(self, entry, column)` |
| `compose` | method | `cli/timeline_browser.py:234` | `def compose(self)` |
| `entries` | method | `cli/timeline_browser.py:134` | `def entries(self)` |
| `launch_scrubber` | function | `cli/timeline_browser.py:169` | `def launch_scrubber(payload, state, runner)` |
| `on_data_table_row_highlighted` | method | `cli/timeline_browser.py:253` | `def on_data_table_row_highlighted(self, event)` |
| `on_input_changed` | method | `cli/timeline_browser.py:249` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/timeline_browser.py:242` | `def on_mount(self)` |
| `read` | method | `cli/timeline_browser.py:85` | `def read(self)` |
| `reload` | method | `cli/timeline_browser.py:130` | `def reload(self)` |
| `root` | method | `cli/timeline_browser.py:81` | `def root(self)` |
| `TipsConfig` | class | `cli/tips_engine.py:137` | `class TipsConfig` |
| `TipsEngine` | class | `cli/tips_engine.py:186` | `class TipsEngine` |
| `__init__` | method | `cli/tips_engine.py:194` | `def __init__(self, config, autosuggest_engine)` |
| `_award_elo` | method | `cli/tips_engine.py:808` | `def _award_elo(self, cmd, first_time, new_phase, phase)` |
| `_check_badges` | method | `cli/tips_engine.py:840` | `def _check_badges(self, cmd, first_time)` |
| `_check_karma_up` | method | `cli/tips_engine.py:819` | `def _check_karma_up(self)` |
| `_collect_killchain_progress` | method | `cli/tips_engine.py:575` | `def _collect_killchain_progress(self, current_phase)` |
| `_commands_in_exploration_phase` | method | `cli/tips_engine.py:707` | `def _commands_in_exploration_phase(self, phase)` |
| `_compute_command_hints` | method | `cli/tips_engine.py:616` | `def _compute_command_hints(self, cmd, phase)` |
| `_compute_evidence_hints` | method | `cli/tips_engine.py:529` | `def _compute_evidence_hints(self, cmd, phase)` |
| `_ensure_state_and_index` | method | `cli/tips_engine.py:928` | `def _ensure_state_and_index(self)` |
| `_fire_vri_reward` | method | `cli/tips_engine.py:879` | `def _fire_vri_reward(self, ctx)` |
| `_flush_suggestions_panel` | method | `cli/tips_engine.py:311` | `def _flush_suggestions_panel(self)` |
| `_get_hints_level` | method | `cli/tips_engine.py:344` | `def _get_hints_level(self)` |
| `_get_karma_name` | method | `cli/tips_engine.py:1047` | `def _get_karma_name(elo)` |
| `_get_rec_engine` | method | `cli/tips_engine.py:505` | `def _get_rec_engine(self)` |
| `_is_recordable_command` | method | `cli/tips_engine.py:989` | `def _is_recordable_command(self, cmd)` |
| `_load_command_index` | method | `cli/tips_engine.py:979` | `def _load_command_index(self)` |
| `_load_payload` | method | `cli/tips_engine.py:492` | `def _load_payload(self)` |
| `_load_state` | method | `cli/tips_engine.py:934` | `def _load_state(self)` |
| `_maybe_auto_show_killchain` | method | `cli/tips_engine.py:272` | `def _maybe_auto_show_killchain(self, phase)` |
| `_maybe_show_full_killchain` | method | `cli/tips_engine.py:605` | `def _maybe_show_full_killchain(self, cmd)` |
| `_next_threshold` | method | `cli/tips_engine.py:1053` | `def _next_threshold(self, current)` |
| `_noop` | function | `cli/tips_engine.py:132` | `def _noop()` |
| `_phase_for_cmd` | method | `cli/tips_engine.py:1030` | `def _phase_for_cmd(self, cmd)` |
| `_pick_weighted` | method | `cli/tips_engine.py:909` | `def _pick_weighted(rewards, weights)` |
| `_print_badge` | method | `cli/tips_engine.py:869` | `def _print_badge(self, name, description)` |
| `_print_separator` | method | `cli/tips_engine.py:836` | `def _print_separator(self, width)` |
| `_read_os_id_from_session` | method | `cli/tips_engine.py:388` | `def _read_os_id_from_session(self)` |
| `_read_recent_commands_for_autosuggest` | method | `cli/tips_engine.py:1012` | `def _read_recent_commands_for_autosuggest(self, limit)` |
| `_read_run_commands` | method | `cli/tips_engine.py:1007` | `def _read_run_commands(self)` |
| `_read_world_model_phase` | method | `cli/tips_engine.py:378` | `def _read_world_model_phase(self)` |
| `_refresh_autosuggest` | method | `cli/tips_engine.py:726` | `def _refresh_autosuggest(self, cmd, phase)` |
| `_render_arsenal_tip` | function | `cli/tips_engine.py:1182` | `def _render_arsenal_tip(ctx, state, config)` |
| `_render_autosuggest_hint` | method | `cli/tips_engine.py:750` | `def _render_autosuggest_hint(self, engine)` |
| `_render_contextual_tip` | method | `cli/tips_engine.py:633` | `def _render_contextual_tip(self, cmd, phase)` |
| `_render_exploration` | function | `cli/tips_engine.py:1126` | `def _render_exploration(ctx, state, config)` |
| `_render_hidden_feature` | function | `cli/tips_engine.py:1162` | `def _render_hidden_feature(ctx, state, config)` |
| `_render_kill_chain_hints` | method | `cli/tips_engine.py:475` | `def _render_kill_chain_hints(self, cmd, phase)` |
| `_render_phase_badge` | function | `cli/tips_engine.py:1144` | `def _render_phase_badge(ctx, state, config)` |
| `_render_streak` | function | `cli/tips_engine.py:1105` | `def _render_streak(ctx, state, config)` |
| `_resolve_phase` | method | `cli/tips_engine.py:355` | `def _resolve_phase(self, cmd, fallback)` |
| `_resolve_theme` | method | `cli/tips_engine.py:300` | `def _resolve_theme(self)` |
| `_run_curiosity_reveal` | method | `cli/tips_engine.py:683` | `def _run_curiosity_reveal(self, cmd, phase)` |
| `_safe_tip_trigger` | method | `cli/tips_engine.py:672` | `def _safe_tip_trigger(tip, ctx)` |
| `_sanitize_seen` | method | `cli/tips_engine.py:993` | `def _sanitize_seen(self, names, known)` |
| `_save_state` | method | `cli/tips_engine.py:954` | `def _save_state(self)` |
| `_summary_for_exploration_cmd` | method | `cli/tips_engine.py:713` | `def _summary_for_exploration_cmd(self, cmd)` |
| `_sync_user_elo` | method | `cli/tips_engine.py:1057` | `def _sync_user_elo(self, delta)` |
| `_truncate` | method | `cli/tips_engine.py:1041` | `def _truncate(value, max_len)` |
| `_update_engagement_state` | method | `cli/tips_engine.py:767` | `def _update_engagement_state(self, cmd, phase)` |
| `build_default_tips_config` | function | `cli/tips_engine.py:1242` | `def build_default_tips_config()` |
| `enabled` | method | `cli/tips_engine.py:221` | `def enabled(self)` |
| `get_state_snapshot` | method | `cli/tips_engine.py:440` | `def get_state_snapshot(self)` |
| `heal_commands_seen` | method | `cli/tips_engine.py:460` | `def heal_commands_seen(self, known)` |
| `render` | method | `cli/tips_engine.py:229` | `def render(self, cmd, phase)` |
| `render_session_start` | method | `cli/tips_engine.py:408` | `def render_session_start(self, phase, os_id)` |
| `reset_session` | method | `cli/tips_engine.py:455` | `def reset_session(self)` |
| `set_enabled` | method | `cli/tips_engine.py:225` | `def set_enabled(self, value)` |
| `ToastBus` | class | `cli/toast_bus.py:750` | `class ToastBus` |
| `ToastConfig` | class | `cli/toast_bus.py:44` | `class ToastConfig` |
| `ToastEvent` | class | `cli/toast_bus.py:112` | `class ToastEvent` |
| `ToastFormatter` | class | `cli/toast_bus.py:563` | `class ToastFormatter` |
| `ToastReader` | class | `cli/toast_bus.py:205` | `class ToastReader` |
| `ToastState` | class | `cli/toast_bus.py:123` | `class ToastState` |
| `ToastrConfig` | class | `cli/toast_bus.py:433` | `class ToastrConfig` |
| `__init__` | method | `cli/toast_bus.py:131` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:208` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:566` | `def __init__(self, config, theme)` |
| `__init__` | method | `cli/toast_bus.py:757` | `def __init__(self, config, state, reader, formatter, console)` |
| `_budget` | function | `cli/toast_bus.py:928` | `def _budget(payload, config)` |
| `_build_event` | method | `cli/toast_bus.py:298` | `def _build_event(self, line, source, offset)` |
| `_coerce_str` | method | `cli/toast_bus.py:325` | `def _coerce_str(value)` |
| `_console_width` | method | `cli/toast_bus.py:731` | `def _console_width(self)` |
| `_ensure_loaded` | method | `cli/toast_bus.py:184` | `def _ensure_loaded(self)` |
| `_erase_lines` | method | `cli/toast_bus.py:871` | `def _erase_lines(stream, rows)` |
| `_is_dumb_stream` | function | `cli/toast_bus.py:900` | `def _is_dumb_stream(stream)` |
| `_is_truthy` | function | `cli/toast_bus.py:886` | `def _is_truthy(value, config, default)` |
| `_parse` | method | `cli/toast_bus.py:283` | `def _parse(self, text, source, base_offset)` |
| `_role_for` | method | `cli/toast_bus.py:738` | `def _role_for(self, severity)` |
| `_schedule_erase` | method | `cli/toast_bus.py:855` | `def _schedule_erase(self, delay)` |
| `_summary` | method | `cli/toast_bus.py:333` | `def _summary(record)` |
| `_truncate` | method | `cli/toast_bus.py:744` | `def _truncate(self, value)` |
| `build_default_bus` | function | `cli/toast_bus.py:943` | `def build_default_bus(payload, sessions_dir, console)` |
| `build_toast_renderable` | function | `cli/toast_bus.py:1131` | `def build_toast_renderable(events, payload, width, config)` |
| `collect` | method | `cli/toast_bus.py:772` | `def collect(self)` |
| `digest_line` | method | `cli/toast_bus.py:669` | `def digest_line(dropped)` |
| `duration_for` | method | `cli/toast_bus.py:644` | `def duration_for(self, event)` |
| `emit_toast` | function | `cli/toast_bus.py:1042` | `def emit_toast(message, severity, event_type, sessions_dir, config)` |
| `ephemeral_enabled` | function | `cli/toast_bus.py:996` | `def ephemeral_enabled(payload, config)` |
| `flush` | method | `cli/toast_bus.py:166` | `def flush(self)` |
| `format` | method | `cli/toast_bus.py:571` | `def format(self, event)` |
| `format_ephemeral` | method | `cli/toast_bus.py:616` | `def format_ephemeral(self, event)` |
| `format_many` | method | `cli/toast_bus.py:677` | `def format_many(self, events, width)` |
| `format_prominent` | method | `cli/toast_bus.py:594` | `def format_prominent(self, event)` |
| `get` | method | `cli/toast_bus.py:150` | `def get(self, name)` |
| `is_prominent` | method | `cli/toast_bus.py:584` | `def is_prominent(self, event)` |
| `mark_all_seen` | method | `cli/toast_bus.py:814` | `def mark_all_seen(self)` |
| `path` | method | `cli/toast_bus.py:146` | `def path(self)` |
| `read_recent_toasts` | function | `cli/toast_bus.py:1087` | `def read_recent_toasts(sessions_dir, limit, config)` |
| `read_unseen` | method | `cli/toast_bus.py:223` | `def read_unseen(self, name, start_offset)` |
| `render` | method | `cli/toast_bus.py:785` | `def render(self, enabled)` |
| `render_ephemeral` | method | `cli/toast_bus.py:822` | `def render_ephemeral(self, enabled, duration)` |
| `render_ephemeral_toasts` | function | `cli/toast_bus.py:1012` | `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` |
| `render_toasts` | function | `cli/toast_bus.py:972` | `def render_toasts(payload, sessions_dir, console, bus_factory)` |
| `reset` | method | `cli/toast_bus.py:161` | `def reset(self)` |
| `resolve_sources` | method | `cli/toast_bus.py:255` | `def resolve_sources(self, names)` |
| `rich_toastr_panel` | function | `cli/toast_bus.py:456` | `def rich_toastr_panel(message, severity, terminal_width, config)` |
| `root` | method | `cli/toast_bus.py:219` | `def root(self)` |
| `sentinel_toast_panel` | function | `cli/toast_bus.py:528` | `def sentinel_toast_panel(file_name, relevant_info, commands, details, severity)` |
| `set` | method | `cli/toast_bus.py:155` | `def set(self, name, offset)` |
| `shell_hint_bypass` | function | `cli/toast_bus.py:509` | `def shell_hint_bypass(console, message, severity)` |
| `toastr_severity_style` | function | `cli/toast_bus.py:449` | `def toastr_severity_style(severity)` |
| `toasts_enabled` | function | `cli/toast_bus.py:920` | `def toasts_enabled(payload, config)` |
| `ConfirmModal` | class | `cli/tui_forms.py:247` | `class ConfirmModal` |
| `FormModal` | class | `cli/tui_forms.py:63` | `class FormModal` |
| `SearchSelectModal` | class | `cli/tui_forms.py:112` | `class SearchSelectModal` |
| `TextEditorModal` | class | `cli/tui_forms.py:284` | `class TextEditorModal` |
| `__init__` | method | `cli/tui_forms.py:68` | `def __init__(self, title, fields, defaults, save_label)` |
| `__init__` | method | `cli/tui_forms.py:122` | `def __init__(self, title, options, placeholder, allow_custom)` |
| `__init__` | method | `cli/tui_forms.py:256` | `def __init__(self, title, body)` |
| `__init__` | method | `cli/tui_forms.py:298` | `def __init__(self, title, text, validator, language, save_label)` |
| `_accept` | method | `cli/tui_forms.py:191` | `def _accept(self)` |
| `_current_text` | method | `cli/tui_forms.py:323` | `def _current_text(self)` |
| `_hint` | method | `cli/tui_forms.py:172` | `def _hint(self, text)` |
| `_render_options` | method | `cli/tui_forms.py:155` | `def _render_options(self, query)` |
| `_save` | method | `cli/tui_forms.py:327` | `def _save(self)` |
| `_selected_value` | method | `cli/tui_forms.py:179` | `def _selected_value(self)` |
| `_values` | method | `cli/tui_forms.py:95` | `def _values(self)` |
| `action_answer` | method | `cli/tui_forms.py:272` | `def action_answer(self, answer)` |
| `compose` | method | `cli/tui_forms.py:82` | `def compose(self)` |
| `compose` | method | `cli/tui_forms.py:136` | `def compose(self)` |
| `compose` | method | `cli/tui_forms.py:262` | `def compose(self)` |
| `compose` | method | `cli/tui_forms.py:314` | `def compose(self)` |
| `filter_candidates` | function | `cli/tui_forms.py:27` | `def filter_candidates(query, options, limit)` |
| `on_button_pressed` | method | `cli/tui_forms.py:102` | `def on_button_pressed(self, event)` |
| `on_button_pressed` | method | `cli/tui_forms.py:239` | `def on_button_pressed(self, event)` |
| `on_button_pressed` | method | `cli/tui_forms.py:276` | `def on_button_pressed(self, event)` |
| `on_button_pressed` | method | `cli/tui_forms.py:338` | `def on_button_pressed(self, event)` |
| `on_input_changed` | method | `cli/tui_forms.py:201` | `def on_input_changed(self, event)` |
| `on_input_submitted` | method | `cli/tui_forms.py:107` | `def on_input_submitted(self, event)` |
| `on_input_submitted` | method | `cli/tui_forms.py:206` | `def on_input_submitted(self, event)` |
| `on_key` | method | `cli/tui_forms.py:220` | `def on_key(self, event)` |
| `on_mount` | method | `cli/tui_forms.py:147` | `def on_mount(self)` |
| `on_option_list_option_selected` | method | `cli/tui_forms.py:211` | `def on_option_list_option_selected(self, event)` |
| `_cycle` | function | `cli/tui_theme.py:65` | `def _cycle(payload, direction)` |
| `_format_listing` | function | `cli/tui_theme.py:45` | `def _format_listing(current)` |
| `_set_theme` | function | `cli/tui_theme.py:30` | `def _set_theme(payload, name)` |
| `run` | function | `cli/tui_theme.py:87` | `def run(args, payload, save)` |
| `TutorialConfig` | class | `cli/tutorial.py:76` | `class TutorialConfig` |
| `is_done` | function | `cli/tutorial.py:83` | `def is_done(config)` |
| `mark_done` | function | `cli/tutorial.py:89` | `def mark_done(config)` |
| `render_header` | function | `cli/tutorial.py:96` | `def render_header()` |
| `render_phase_table` | function | `cli/tutorial.py:113` | `def render_phase_table()` |
| `run` | function | `cli/tutorial.py:185` | `def run(params, command_runner)` |
| `run_step` | function | `cli/tutorial.py:128` | `def run_step(index, command, description, why, params, command_runner)` |
| `BinarySpec` | class | `cli/wizard.py:90` | `class BinarySpec` |
| `BinaryStatus` | class | `cli/wizard.py:141` | `class BinaryStatus` |
| `ReadinessItem` | class | `cli/wizard.py:150` | `class ReadinessItem` |
| `WizardResult` | class | `cli/wizard.py:160` | `class WizardResult` |
| `_ask_device` | function | `cli/wizard.py:537` | `def _ask_device(current)` |
| `_ask_domain` | function | `cli/wizard.py:515` | `def _ask_domain(current)` |
| `_ask_lhost` | function | `cli/wizard.py:484` | `def _ask_lhost(current)` |
| `_ask_llm` | function | `cli/wizard.py:621` | `def _ask_llm(params)` |
| `_ask_marketplace_config` | function | `cli/wizard.py:852` | `def _ask_marketplace_config()` |
| `_ask_operator_login` | function | `cli/wizard.py:724` | `def _ask_operator_login(params)` |
| `_ask_os_id` | function | `cli/wizard.py:563` | `def _ask_os_id(current)` |
| `_ask_rhost` | function | `cli/wizard.py:457` | `def _ask_rhost(current)` |
| `_ask_wordlists` | function | `cli/wizard.py:692` | `def _ask_wordlists(params)` |
| `_build_readiness` | function | `cli/wizard.py:875` | `def _build_readiness(params)` |
| `_check` | function | `cli/wizard.py:878` | `def _check(key, label, hint)` |
| `_check_llm` | function | `cli/wizard.py:887` | `def _check_llm()` |
| `_collect_values` | function | `cli/wizard.py:419` | `def _collect_values(params)` |
| `_detect_device` | function | `cli/wizard.py:1120` | `def _detect_device()` |
| `_detect_lhost` | function | `cli/wizard.py:1098` | `def _detect_lhost()` |
| `_find_seclists_root` | function | `cli/wizard.py:1133` | `def _find_seclists_root()` |
| `_group_by_category` | function | `cli/wizard.py:988` | `def _group_by_category(statuses)` |
| `_info` | function | `cli/wizard.py:1169` | `def _info(msg)` |
| `_is_default` | function | `cli/wizard.py:322` | `def _is_default(value)` |
| `_is_weak` | function | `cli/wizard.py:325` | `def _is_weak(value)` |
| `_mask_secret` | function | `cli/wizard.py:606` | `def _mask_secret(value)` |
| `_normalize_provider_answer` | function | `cli/wizard.py:585` | `def _normalize_provider_answer(raw)` |
| `_ok` | function | `cli/wizard.py:1161` | `def _ok(msg)` |
| `_ping` | function | `cli/wizard.py:1141` | `def _ping(ip)` |
| `_print_binary_report` | function | `cli/wizard.py:997` | `def _print_binary_report(statuses)` |
| `_print_glossary_panel` | function | `cli/wizard.py:379` | `def _print_glossary_panel()` |
| `_print_header` | function | `cli/wizard.py:364` | `def _print_header()` |
| `_print_long_help` | function | `cli/wizard.py:412` | `def _print_long_help(key)` |
| `_print_next_steps` | function | `cli/wizard.py:1035` | `def _print_next_steps(params)` |
| `_print_readiness` | function | `cli/wizard.py:927` | `def _print_readiness(items)` |
| `_print_secret_rotation` | function | `cli/wizard.py:348` | `def _print_secret_rotation(rotated)` |
| `_print_validation_summary` | function | `cli/wizard.py:1059` | `def _print_validation_summary(params)` |
| `_prompt` | function | `cli/wizard.py:1154` | `def _prompt(message)` |
| `_rotate_default_secrets` | function | `cli/wizard.py:300` | `def _rotate_default_secrets(params, save)` |
| `_spec_long_help` | function | `cli/wizard.py:404` | `def _spec_long_help(key)` |
| `_warn` | function | `cli/wizard.py:1165` | `def _warn(msg)` |
| `_wizard_login_flow` | function | `cli/wizard.py:786` | `def _wizard_login_flow()` |
| `_wizard_register_flow` | function | `cli/wizard.py:809` | `def _wizard_register_flow()` |
| `check_binaries` | function | `cli/wizard.py:947` | `def check_binaries(specs, which)` |
| `run` | function | `cli/wizard.py:169` | `def run(params, save)` |
| `run_non_interactive` | function | `cli/wizard.py:234` | `def run_non_interactive(params, save, values)` |
| `WizardScope` | class | `cli/wizard_scope.py:31` | `class WizardScope` |
| `WizardScopeConfig` | class | `cli/wizard_scope.py:17` | `class WizardScopeConfig` |
| `parse_scope` | function | `cli/wizard_scope.py:38` | `def parse_scope(tokens, config)` |
| `status_rows` | function | `cli/wizard_scope.py:64` | `def status_rows(params)` |
| `exploit` | function | `contrib/legacy/lazy_http_bof.py:29` | `def exploit(target, port, payload)` |
| `genHeader` | function | `contrib/legacy/lazy_http_bof.py:6` | `def genHeader(raw)` |
| `check_sudo` | function | `contrib/legacy/lazy_packet_image_sniffer.py:23` | `def check_sudo()` |
| `choose_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:49` | `def choose_interface(interfaces)` |
| `daemonize` | function | `contrib/legacy/lazy_packet_image_sniffer.py:192` | `def daemonize()` |
| `get_ip_addresses` | function | `contrib/legacy/lazy_packet_image_sniffer.py:65` | `def get_ip_addresses(interface)` |
| `get_subnet_from_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:61` | `def get_subnet_from_interface(interface)` |
| `handle_packet` | function | `contrib/legacy/lazy_packet_image_sniffer.py:111` | `def handle_packet(packet)` |
| `list_interfaces` | function | `contrib/legacy/lazy_packet_image_sniffer.py:31` | `def list_interfaces()` |
| `run` | function | `contrib/legacy/lazy_packet_image_sniffer.py:187` | `def run()` |
| `save_image` | function | `contrib/legacy/lazy_packet_image_sniffer.py:161` | `def save_image(src_ip, end_idx)` |
| `build_llm_prompt` | function | `contrib/legacy/lazyaddon_creator.py:98` | `def build_llm_prompt(meta, readme, root_files)` |
| `build_yaml` | function | `contrib/legacy/lazyaddon_creator.py:300` | `def build_yaml(data, repo_url)` |
| `extract_json_from_response` | function | `contrib/legacy/lazyaddon_creator.py:164` | `def extract_json_from_response(text)` |
| `fallback_yaml_data` | function | `contrib/legacy/lazyaddon_creator.py:276` | `def fallback_yaml_data(meta, readme, root_files)` |
| `fetch_readme` | function | `contrib/legacy/lazyaddon_creator.py:73` | `def fetch_readme(owner, repo)` |
| `fetch_repo_metadata` | function | `contrib/legacy/lazyaddon_creator.py:68` | `def fetch_repo_metadata(owner, repo)` |
| `fetch_root_files` | function | `contrib/legacy/lazyaddon_creator.py:85` | `def fetch_root_files(owner, repo)` |
| `github_api_get` | function | `contrib/legacy/lazyaddon_creator.py:58` | `def github_api_get(owner, repo, endpoint)` |
| `heuristic_execute_command` | function | `contrib/legacy/lazyaddon_creator.py:211` | `def heuristic_execute_command(name, root_files, language)` |
| `heuristic_install_command` | function | `contrib/legacy/lazyaddon_creator.py:192` | `def heuristic_install_command(root_files, language)` |
| `heuristic_params` | function | `contrib/legacy/lazyaddon_creator.py:245` | `def heuristic_params(name, readme, root_files)` |
| `main` | function | `contrib/legacy/lazyaddon_creator.py:357` | `def main()` |
| `parse_github_url` | function | `contrib/legacy/lazyaddon_creator.py:49` | `def parse_github_url(url)` |
| `save_yaml` | function | `contrib/legacy/lazyaddon_creator.py:336` | `def save_yaml(addon, output_dir)` |

Next: [SYMBOLS_p7.md](SYMBOLS_p7.md)
