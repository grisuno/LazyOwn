# cli

cli groups 115 files (py) around _sanitize, colors_enabled, _paint, format_line, print_error. LazyOwn CLI infrastructure.

```mermaid
graph LR
    cli["cli"]
    core["core"]
    modules["modules"]
    root["root"]
    skills["skills"]
    tests["tests"]
    cli -- "calls into" --> core
    cli -- "calls into" --> tests
    core -- "calls into" --> tests
    modules -- "depends on" --> core
    root -- "calls into" --> cli
    root -- "depends on" --> core
    skills -- "calls into" --> cli
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "calls into" --> skills
```

## cli (4.1)

cli groups 46 files (py) around Theme, get_theme, theme_from_payload, PendingCommandSet, is_pending. LazyOwn CLI infrastructure.

## core (4.2)

core groups 10 files (py) around _sanitize, colors_enabled, _paint, format_line, print_error. Core primitives for the LazyOwn framework.

## modules (4.3)

modules groups 1 files (py) around PrivescVector, SystemProfile, _parse_kernel_version, _parse_version_from_range, parse_linpeas_output. Crystal Ball — privilege escalation vector prediction engine.

## root (4.4)

root groups 1 files (py) around sanitize_content, RAGManager, __init__, initialize_cache_table, get_cache_key. RAGManager: Manages RAG functionality with CAG caching for document processing and...

## skills (4.5)

skills groups 7 files (py) around OrchestratorConfig, from_payload, OrchestratorGoal, with_defaults, OrchestratorResult. MCP tool ``lazyown_graph_neighbors`` (migrated from the call_tool dispatch chain).

## tests (4.6)

tests groups 50 files (py) around _StaticProvider, __init__, suggest, _RaisingProvider, suggest. Unit tests for cli.autosuggest.

**Files**:

- cli/__init__.py
- cli/autosuggest.py
- cli/chain_mode.py
- cli/command_explorer.py
- cli/command_form.py
- cli/commands/__init__.py
- cli/commands/_dormancy.py
- cli/commands/help_ui.py
- cli/commands/misc_migrated.py
- cli/commands/orchestration.py
- cli/commands/recon.py
- cli/config_status.py
- cli/contextual_help.py
- cli/dashboard_layout.py
- cli/dashboard_tui.py
- cli/doctor.py
- cli/exploit_advisor.py
- cli/exploration_view.py
- cli/graph_advisor.py
- cli/graph_overlay.py
- cli/killchain.py
- cli/marketplace_config.py
- cli/noise_verbs.py
- cli/palette.py
- cli/palette_command.py
- cli/palette_graph.py
- cli/palette_overlay.py
- cli/palette_telemetry.py
- cli/phase_labels.py
- cli/protips.py
- cli/reactive_hints.py
- cli/reasoning_stream.py
- cli/recommendation.py
- cli/recommendation_signals.py
- cli/registry.py
- cli/sessions_browser.py
- cli/splash.py
- cli/status_bar.py
- cli/themes.py
- cli/timeline_browser.py
- cli/tips_engine.py
- cli/toast_bus.py
- cli/tui_theme.py
- cli/tutorial.py
- cli/wizard.py
- cli/wizard_scope.py
- core/__init__.py
- core/console.py
- core/dependencies.py
- core/error_advice.py
- core/errors.py
- core/http.py
- core/network.py
- core/profiles.py
- core/safe_console.py
- core/text_utils.py
- lazy_sentinel4.py
- modules/privesc_predictor.py
- skills/mcp_tools/graph_neighbors.py
- skills/mcp_tools/graph_search.py
- skills/mcp_tools/graph_suggest_next.py
- skills/mcp_tools/graph_summary.py
- skills/mcp_tools/palette.py
- skills/mcp_tools/recommend_next.py
- skills/unified_orchestrator.py
- tests/test_autosuggest.py
- tests/test_chain_mode.py
- tests/test_command_form.py
- tests/test_command_palette.py
- tests/test_command_set_migration.py
- tests/test_console_stdio.py
- tests/test_core_defaults.py
- tests/test_daemon_ctl_command_set.py
- tests/test_dashboard_tui.py
- tests/test_dependencies.py
- tests/test_doctor.py
- tests/test_encoding_command_set.py
- tests/test_evidence_hints.py
- tests/test_exploration_and_addons.py
- tests/test_exposure_command_sets.py
- tests/test_graph_advisor.py
- tests/test_graph_overlay.py
- tests/test_help_ui_command_set.py
- tests/test_improvements_spec.py
- tests/test_killchain.py
- tests/test_killchain_auto_refresh.py
- tests/test_killchain_gap_signal.py
- tests/test_marketplace_config.py
- tests/test_nethelpers_command_set.py
- tests/test_palette_overlay.py
- tests/test_phase1_data_gaps.py
- tests/test_phase_labels.py
- tests/test_profiles.py
- tests/test_reactive_hints.py
- tests/test_reactive_hints_expanded.py
- tests/test_reasoning_stream.py
- tests/test_recommendation.py
- tests/test_safe_console.py
- tests/test_scope_deny_priority.py
- tests/test_scope_guard_integration.py
- tests/test_session_ops_command_set.py
- tests/test_sessions_browser.py
- tests/test_shellsys_command_set.py
- tests/test_status_bar_operators.py
- tests/test_themes.py
- tests/test_timeline_browser.py
- tests/test_tips_engine.py
- tests/test_toast_bus.py
- tests/test_toastr_unify.py
- tests/test_tui_splash.py
- tests/test_tui_style.py
- tests/test_tui_theme_command.py
- tests/test_tui_themes.py
- tests/test_wizard_binary_check.py
- tests/test_wizard_llm.py
