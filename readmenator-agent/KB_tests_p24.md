# Subsystem: tests (page 24 of 26)
Previous: [KB_tests_p23.md](KB_tests_p23.md)

## tests/test_selection_bridge.py
- Doc: Tests for the shared bridge selector.
- Layer: testing
- Language: py
- Symbols:
  - `_Entry` (class, line 24) `class _Entry`
  - `_Dispatcher` (class, line 31) `class _Dispatcher`
  - `_bind` (function, line 46) `def _bind(monkeypatch, dispatcher)`
  - `_ctx` (function, line 54) `def _ctx()`
  - `test_no_target_abstains` (function, line 61) `def test_no_target_abstains(monkeypatch)`
  - `test_catalogue_hit_becomes_decision` (function, line 67) `def test_catalogue_hit_becomes_decision(monkeypatch)`
  - `test_target_is_passed_to_dispatcher` (function, line 79) `def test_target_is_passed_to_dispatcher(monkeypatch)`
  - `test_burned_verbs_are_excluded` (function, line 87) `def test_burned_verbs_are_excluded(monkeypatch)`
  - `test_returned_burned_command_dropped` (function, line 95) `def test_returned_burned_command_dropped(monkeypatch)`
  - `test_no_catalogue_hit_abstains` (function, line 102) `def test_no_catalogue_hit_abstains(monkeypatch)`
  - `test_dispatcher_error_is_swallowed` (function, line 108) `def test_dispatcher_error_is_swallowed(monkeypatch)`
  - `__init__` (method, line 34) `def __init__(self, result, raise_on)`
  - `suggest` (method, line 39) `def suggest(self)`
- Depends on: `modules/lazyown_bridge.py`, `modules/selection/base.py`, `modules/selection/bridge.py`

## tests/test_selection_lazyscript.py
- Doc: Tests for the LazyscriptSelector.
- Layer: testing
- Language: py
- Symbols:
  - `scripts_dir` (function, line 17) `def scripts_dir(tmp_path)`
  - `_ctx` (function, line 24) `def _ctx(goal, services, target, exclude)`
  - `test_matches_service_token` (function, line 34) `def test_matches_service_token(scripts_dir)`
  - `test_matches_goal_token` (function, line 42) `def test_matches_goal_token(scripts_dir)`
  - `test_abstains_without_match` (function, line 49) `def test_abstains_without_match(scripts_dir)`
  - `test_skips_lifecycle_scripts` (function, line 54) `def test_skips_lifecycle_scripts(scripts_dir)`
  - `test_requires_target` (function, line 60) `def test_requires_target(scripts_dir)`
  - `test_excluded_command_abstains` (function, line 66) `def test_excluded_command_abstains(scripts_dir)`
  - `test_missing_dir_is_safe` (function, line 72) `def test_missing_dir_is_safe(tmp_path)`
  - `test_emitted_command_is_routable` (function, line 77) `def test_emitted_command_is_routable(scripts_dir)`
- Depends on: `modules/auto_registry.py`, `modules/selection/base.py`, `modules/selection/lazyscript.py`

## tests/test_selection_module.py
- Doc: Tests for the ModuleSelector over the shared module registry bridge.
- Layer: testing
- Language: py
- Symbols:
  - `registry` (function, line 18) `def registry(tmp_path, monkeypatch)`
  - `_ctx` (function, line 41) `def _ctx(goal, target, services, exclude)`
  - `TestModuleSelector` (class, line 51) `class TestModuleSelector`
  - `test_goal_token_raises_addon` (method, line 52) `def test_goal_token_raises_addon(self, registry)`
  - `test_playbook_entry_routes_apt_playbook` (method, line 58) `def test_playbook_entry_routes_apt_playbook(self, registry)`
  - `test_lazy_addon_normalised_to_routable_verb` (method, line 64) `def test_lazy_addon_normalised_to_routable_verb(self, registry)`
  - `test_routable_through_loop` (method, line 70) `def test_routable_through_loop(self, registry)`
  - `test_no_match_abstains` (method, line 78) `def test_no_match_abstains(self, registry)`
  - `test_requires_target` (method, line 82) `def test_requires_target(self, registry)`
  - `test_exclude_skips_taken_intent` (method, line 87) `def test_exclude_skips_taken_intent(self, registry)`
- Depends on: `modules/__init__.py`, `modules/auto_registry.py`, `modules/module_registry.py`, `modules/selection/base.py`, `modules/selection/module.py`

## tests/test_selection_parquet.py
- Doc: Tests for the shared parquet (session-history) selector.
- Layer: testing
- Language: py
- Symbols:
  - `_PDB` (class, line 23) `class _PDB`
  - `_bind` (function, line 35) `def _bind(monkeypatch, pdb, blocked)`
  - `_rows` (function, line 41) `def _rows()`
  - `_ctx` (function, line 46) `def _ctx()`
  - `test_no_target_abstains` (function, line 53) `def test_no_target_abstains(monkeypatch)`
  - `test_no_pdb_abstains` (function, line 59) `def test_no_pdb_abstains(monkeypatch)`
  - `test_most_frequent_head_wins` (function, line 65) `def test_most_frequent_head_wins(monkeypatch)`
  - `test_success_only_query` (function, line 75) `def test_success_only_query(monkeypatch)`
  - `test_burned_verb_skipped` (function, line 83) `def test_burned_verb_skipped(monkeypatch)`
  - `test_blacklisted_verb_skipped` (function, line 90) `def test_blacklisted_verb_skipped(monkeypatch)`
  - `test_taken_and_junk_skipped` (function, line 97) `def test_taken_and_junk_skipped(monkeypatch)`
  - `test_multi_category_phase_falls_through` (function, line 104) `def test_multi_category_phase_falls_through(monkeypatch)`
  - `__init__` (method, line 26) `def __init__(self, rows_by_cat)`
  - `query_session` (method, line 30) `def query_session(self, phase, target, success_only, limit)`
- Depends on: `modules/selection/base.py`, `modules/selection/parquet.py`

## tests/test_selection_technique.py
- Doc: Tests for the TechniqueSelector and its playbook_engine helper.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeStore` (class, line 18) `class _FakeStore`
  - `_FakeStix` (class, line 26) `class _FakeStix`
  - `fake_stix` (function, line 67) `def fake_stix(monkeypatch)`
  - `_ctx` (function, line 75) `def _ctx(phase, os_hint, target, exclude)`
  - `TestPhaseTechniques` (class, line 81) `class TestPhaseTechniques`
  - `TestTechniqueSelector` (class, line 114) `class TestTechniqueSelector`
  - `__init__` (method, line 19) `def __init__(self, techniques)`
  - `query` (method, line 22) `def query(self, filters)`
  - `__init__` (method, line 27) `def __init__(self, techniques, available)`
  - `available` (method, line 31) `def available(self)`
  - `store` (method, line 34) `def store(self)`
  - `techniques_for_tactics` (method, line 37) `def techniques_for_tactics(self, tactics, platform)`
  - `test_stix_phase_scoped` (method, line 82) `def test_stix_phase_scoped(self, fake_stix)`
  - `test_unknown_phase_empty` (method, line 88) `def test_unknown_phase_empty(self, fake_stix)`
  - `test_top_n_cap` (method, line 92) `def test_top_n_cap(self, fake_stix, monkeypatch, tmp_path)`
  - `test_atomic_fallback_when_stix_missing` (method, line 104) `def test_atomic_fallback_when_stix_missing(self, monkeypatch, tmp_path)`
  - `test_postexp_phase_proposes_atomic_tests` (method, line 115) `def test_postexp_phase_proposes_atomic_tests(self, fake_stix)`
  - `test_recon_phase_abstains` (method, line 122) `def test_recon_phase_abstains(self, fake_stix)`
  - `test_requires_target` (method, line 126) `def test_requires_target(self)`
  - `test_exclude_skips_to_next_technique` (method, line 131) `def test_exclude_skips_to_next_technique(self, fake_stix, monkeypatch)`
  - `test_routable_through_loop` (method, line 146) `def test_routable_through_loop(self, fake_stix)`
- Depends on: `modules/auto_registry.py`, `modules/playbook_engine.py`, `modules/selection/base.py`, `modules/selection/technique.py`

## tests/test_selection_technique_chain.py
- Doc: Tests for TechniqueChainSelector and the focused technique-chain synth.
- Layer: testing
- Language: py
- Symbols:
  - `_ctx` (function, line 18) `def _ctx(phase, os_hint, target, exclude, extra)`
  - `synth_sandbox` (function, line 29) `def synth_sandbox(monkeypatch)`
  - `TestSynthTechniqueChain` (class, line 42) `class TestSynthTechniqueChain`
  - `TestTechniqueChainSelector` (class, line 68) `class TestTechniqueChainSelector`
  - `_fake_write` (function, line 33) `def _fake_write(data, chains_dir)`
  - `test_builds_ordered_atomic_tests_steps` (method, line 43) `def test_builds_ordered_atomic_tests_steps(self)`
  - `test_drops_malformed_ids_and_dedupes` (method, line 54) `def test_drops_malformed_ids_and_dedupes(self)`
  - `test_under_two_techniques_is_empty` (method, line 59) `def test_under_two_techniques_is_empty(self)`
  - `test_validates_against_registry` (method, line 63) `def test_validates_against_registry(self)`
  - `test_phase_techniques_compile_into_one_chain` (method, line 69) `def test_phase_techniques_compile_into_one_chain(self, synth_sandbox, monkeypatch)`
  - `test_goal_named_ids_win_verbatim` (method, line 86) `def test_goal_named_ids_win_verbatim(self, synth_sandbox, monkeypatch)`
  - `test_recon_phase_abstains` (method, line 97) `def test_recon_phase_abstains(self, synth_sandbox)`
  - `test_single_technique_abstains` (method, line 100) `def test_single_technique_abstains(self, synth_sandbox, monkeypatch)`
  - `test_requires_target` (method, line 107) `def test_requires_target(self, synth_sandbox)`
  - `test_excluded_command_is_not_reproposed` (method, line 111) `def test_excluded_command_is_not_reproposed(self, synth_sandbox, monkeypatch)`
  - `test_already_registered_chain_is_not_rewritten` (method, line 124) `def test_already_registered_chain_is_not_rewritten(self, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/chain_synth.py`, `modules/selection/base.py`, `modules/selection/technique_chain.py`

## tests/test_selection_wiring.py
- Doc: Vertical wiring tests: playbooks, adversaries and apt_chain through the loop.
- Layer: testing
- Language: py
- Symbols:
  - `_ctx` (function, line 15) `def _ctx(goal, target, phase, exclude)`
  - `TestPlaybookWiring` (class, line 20) `class TestPlaybookWiring`
  - `TestAdversaryWiring` (class, line 43) `class TestAdversaryWiring`
  - `TestRouting` (class, line 61) `class TestRouting`
  - `test_cascade_names_actor_by_alias` (method, line 21) `def test_cascade_names_actor_by_alias(self)`
  - `test_cascade_names_actor_slug` (method, line 27) `def test_cascade_names_actor_slug(self)`
  - `test_generator_stubs_not_the_base_chain` (method, line 32) `def test_generator_stubs_not_the_base_chain(self)`
  - `test_unknown_actor_never_runs_a_chain` (method, line 37) `def test_unknown_actor_never_runs_a_chain(self)`
  - `testProfiles_resolve_to_numeric_ids` (method, line 44) `def testProfiles_resolve_to_numeric_ids(self)`
  - `test_inject_shellcode_profile` (method, line 50) `def test_inject_shellcode_profile(self)`
  - `test_adverbial_words_do_not_hijack` (method, line 55) `def test_adverbial_words_do_not_hijack(self)`
  - `test_routable_through_loop` (method, line 62) `def test_routable_through_loop(self)`
  - `test_lab_env_gate` (method, line 71) `def test_lab_env_gate(self, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/auto_registry.py`, `modules/selection/base.py`, `modules/selection/registry.py`

## tests/test_selectors_base.py
- Doc: Shared selector brain contract: base types, chain selector and cascade.
- Layer: testing
- Language: py
- Symbols:
  - `_rows` (function, line 16) `def _rows()`
  - `_patch_registry` (function, line 21) `def _patch_registry(monkeypatch, rows)`
  - `test_chain_selector_honours_protocol` (function, line 29) `def test_chain_selector_honours_protocol()`
  - `test_chain_selector_proposes_for_matching_service` (function, line 35) `def test_chain_selector_proposes_for_matching_service(monkeypatch)`
  - `test_chain_selector_abstains_without_match` (function, line 46) `def test_chain_selector_abstains_without_match(monkeypatch)`
  - `test_chain_selector_respects_exclude` (function, line 53) `def test_chain_selector_respects_exclude(monkeypatch)`
  - `test_cascade_returns_first_decision` (function, line 70) `def test_cascade_returns_first_decision(monkeypatch)`
  - `test_cascade_abstains_when_all_abstain` (function, line 79) `def test_cascade_abstains_when_all_abstain(monkeypatch, tmp_path)`
  - `test_default_selectors_contains_chain` (function, line 98) `def test_default_selectors_contains_chain()`
  - `_Empty` (class, line 85) `class _Empty`
  - `suggest` (method, line 86) `def suggest(self)`
- Depends on: `modules/chain_match.py`, `modules/lazyown_bridge.py`, `modules/selection/base.py`, `modules/selection/chain.py`, `modules/selection/parquet.py`, `modules/selection/registry.py`

## tests/test_selectors_capabilities.py
- Doc: Capability selector contracts: playbook, adversary and atomic strategies.
- Layer: testing
- Language: py
- Symbols:
  - `_ctx` (function, line 16) `def _ctx(goal, phase)`
  - `test_playbook_fires_when_goal_names_actor` (function, line 23) `def test_playbook_fires_when_goal_names_actor(monkeypatch)`
  - `test_playbook_abstains_without_actor` (function, line 39) `def test_playbook_abstains_without_actor(monkeypatch)`
  - `test_adversary_fires_when_goal_names_profile` (function, line 50) `def test_adversary_fires_when_goal_names_profile(monkeypatch)`
  - `test_adversary_abstains_without_profile` (function, line 61) `def test_adversary_abstains_without_profile(monkeypatch)`
  - `test_atomic_fires_on_technique_ids_in_postexp` (function, line 69) `def test_atomic_fires_on_technique_ids_in_postexp()`
  - `test_atomic_honours_explicit_techniques_extra` (function, line 77) `def test_atomic_honours_explicit_techniques_extra()`
  - `test_atomic_abstains_in_recon_phase` (function, line 84) `def test_atomic_abstains_in_recon_phase()`
  - `test_atomic_abstains_without_techniques` (function, line 89) `def test_atomic_abstains_without_techniques()`
  - `test_cred_spray_fires_with_creds_and_service` (function, line 94) `def test_cred_spray_fires_with_creds_and_service()`
  - `test_cred_spray_abstains_without_creds` (function, line 105) `def test_cred_spray_abstains_without_creds()`
  - `test_default_selectors_respects_orchestrator_toggle` (function, line 113) `def test_default_selectors_respects_orchestrator_toggle(monkeypatch)`
- Depends on: `modules/apt_playbooks.py`, `modules/chain_registry.py`, `modules/orchestrator_config.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/base.py`, `modules/selection/cred_spray.py`, `modules/selection/playbook.py`, `modules/selection/registry.py`

## tests/test_session_brief.py
- Doc: BDD tests for the consolidated session-start brief.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 18) `def sandbox(tmp_path, monkeypatch)`
  - `_console_text` (function, line 31) `def _console_text(renderable)`
  - `test_brief_covers_target_phase_and_layers` (function, line 39) `def test_brief_covers_target_phase_and_layers(sandbox)`
  - `test_brief_never_raises_on_empty_stores` (function, line 64) `def test_brief_never_raises_on_empty_stores(tmp_path, monkeypatch)`
  - `test_brief_shows_newest_task` (function, line 76) `def test_brief_shows_newest_task(sandbox)`
  - `test_console_brief_respects_hints_off` (function, line 87) `def test_console_brief_respects_hints_off(tmp_path, monkeypatch)`
- Depends on: `cli/session_brief.py`, `core/console.py`, `modules/__init__.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/verb_catalog.py`, `modules/world_model.py`

## tests/test_session_ops_command_set.py
- Doc: Session ops command set extraction tests.
- Layer: testing
- Language: py
- Symbols:
  - `_add_repo_root_to_syspath` (function, line 32) `def _add_repo_root_to_syspath()`
  - `SessionOpsSuiteConfig` (class, line 38) `class SessionOpsSuiteConfig`
  - `_methods_of` (function, line 82) `def _methods_of(path, class_name)`
  - `test_target_is_active_command_set` (function, line 94) `def test_target_is_active_command_set()`
  - `test_target_exposes_full_session_cluster` (function, line 103) `def test_target_exposes_full_session_cluster()`
  - `test_target_phase_metadata` (function, line 110) `def test_target_phase_metadata()`
  - `test_source_no_longer_defines_cluster` (function, line 116) `def test_source_no_longer_defines_cluster()`
  - `test_registry_registers_target` (function, line 122) `def test_registry_registers_target()`
  - `test_no_command_collisions_with_source` (function, line 129) `def test_no_command_collisions_with_source()`
- Depends on: `cli/commands/_base.py`, `cli/commands/_dormancy.py`, `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/registry.py`

## tests/test_session_secrets.py
- Doc: SessionSecretsSpec: Contract for session-scoped secret rotation.
- Layer: testing
- Language: py
- Symbols:
  - `SessionSecretsSpec` (class, line 12) `class SessionSecretsSpec(TestCase)`
  - `setUp` (method, line 15) `def setUp(self)`
  - `test_rotate_generates_and_persists_all_secrets` (method, line 24) `def test_rotate_generates_and_persists_all_secrets(self)`
  - `test_rotate_replaces_previous_values` (method, line 38) `def test_rotate_replaces_previous_values(self)`
  - `test_ensure_replaces_legacy_placeholders` (method, line 45) `def test_ensure_replaces_legacy_placeholders(self)`
  - `test_ensure_keeps_valid_values` (method, line 56) `def test_ensure_keeps_valid_values(self)`
  - `test_ensure_force_rotation` (method, line 63) `def test_ensure_force_rotation(self)`
  - `test_mirror_updates_config_object` (method, line 68) `def test_mirror_updates_config_object(self)`
- Depends on: `core/config.py`, `core/session_secrets.py`

## tests/test_sessions_browser.py
- Doc: Tests for cli/sessions_browser.py.
- Layer: testing
- Language: py
- Symbols:
  - `_populate` (function, line 24) `def _populate(tmp_path)`
  - `test_index_groups_known_files` (function, line 34) `def test_index_groups_known_files(tmp_path)`
  - `test_index_other_bucket_contains_unmatched_files` (function, line 47) `def test_index_other_bucket_contains_unmatched_files(tmp_path)`
  - `test_preview_returns_text_for_text_files` (function, line 56) `def test_preview_returns_text_for_text_files(tmp_path)`
  - `test_preview_flags_binary_files` (function, line 64) `def test_preview_flags_binary_files(tmp_path)`
  - `test_preview_rejects_path_traversal` (function, line 71) `def test_preview_rejects_path_traversal(tmp_path)`
  - `test_state_filter_keeps_matching_entries` (function, line 79) `def test_state_filter_keeps_matching_entries(tmp_path)`
  - `test_category_label_for_known_identifier` (function, line 89) `def test_category_label_for_known_identifier(tmp_path)`
- Depends on: `cli/sessions_browser.py`

## tests/test_shell_semantics.py
- Doc: Contract tests for shell-semantics detection and colored child output.
- Layer: testing
- Language: py
- Symbols:
  - `test_needs_shell_detects_control_and_expansion` (function, line 17) `def test_needs_shell_detects_control_and_expansion()`
  - `test_needs_shell_accepts_plain_argv` (function, line 32) `def test_needs_shell_accepts_plain_argv()`
  - `test_run_command_interprets_semicolon` (function, line 38) `def test_run_command_interprets_semicolon()`
  - `test_run_command_expands_tilde_and_glob` (function, line 45) `def test_run_command_expands_tilde_and_glob(tmp_path, monkeypatch)`
  - `test_terminal_env_forces_color` (function, line 53) `def test_terminal_env_forces_color(monkeypatch)`
  - `test_terminal_env_respects_no_color` (function, line 61) `def test_terminal_env_respects_no_color(monkeypatch)`
  - `test_linpeas_http_server_is_detached` (function, line 69) `def test_linpeas_http_server_is_detached(monkeypatch)`
  - `test_safe_runner_interprets_shell_syntax` (function, line 87) `def test_safe_runner_interprets_shell_syntax()`
  - `_FakePopen` (class, line 75) `class _FakePopen`
  - `__init__` (method, line 76) `def __init__(self, argv)`
- Depends on: `cli/commands/privilege_escalation.py`, `core/hardening.py`, `core/process.py`, `core/safe_exec.py`, `core/safe_subprocess.py`

## tests/test_shellsys_command_set.py
- Doc: Shell/sys command set extraction tests.
- Layer: testing
- Language: py
- Symbols:
  - `_add_repo_root_to_syspath` (function, line 32) `def _add_repo_root_to_syspath()`
  - `ShellsysSuiteConfig` (class, line 38) `class ShellsysSuiteConfig`
  - `_methods_of` (function, line 61) `def _methods_of(path, class_name)`
  - `test_target_is_active_command_set` (function, line 73) `def test_target_is_active_command_set()`
  - `test_target_exposes_full_shellsys_cluster` (function, line 82) `def test_target_exposes_full_shellsys_cluster()`
  - `test_target_phase_metadata` (function, line 89) `def test_target_phase_metadata()`
  - `test_source_no_longer_defines_cluster` (function, line 95) `def test_source_no_longer_defines_cluster()`
  - `test_registry_registers_target` (function, line 101) `def test_registry_registers_target()`
  - `test_no_command_collisions_with_source` (function, line 108) `def test_no_command_collisions_with_source()`
- Depends on: `cli/commands/_base.py`, `cli/commands/_dormancy.py`, `cli/commands/misc_migrated.py`, `cli/commands/shellsys.py`, `cli/registry.py`

## tests/test_short_url_file_containment.py
- Doc: Containment contract for short-URL file serving.
- Layer: testing
- Language: py
- Symbols:
  - `sessions_dir` (function, line 26) `def sessions_dir(tmp_path, monkeypatch)`
  - `TestContainedPaths` (class, line 36) `class TestContainedPaths`
  - `TestRejectedPaths` (class, line 51) `class TestRejectedPaths`
  - `TestRouteStatusContract` (class, line 78) `class TestRouteStatusContract`
  - `TestBlueprintRouteContainment` (class, line 105) `class TestBlueprintRouteContainment`
  - `test_bare_relative_inside_base` (method, line 37) `def test_bare_relative_inside_base(self, sessions_dir)`
  - `test_absolute_inside_base` (method, line 41) `def test_absolute_inside_base(self, sessions_dir)`
  - `test_file_scheme_inside_base` (method, line 45) `def test_file_scheme_inside_base(self, sessions_dir)`
  - `test_remote_url_rejected` (method, line 52) `def test_remote_url_rejected(self, sessions_dir)`
  - `test_absolute_outside_rejected` (method, line 55) `def test_absolute_outside_rejected(self, sessions_dir)`
  - `test_file_scheme_outside_rejected` (method, line 58) `def test_file_scheme_outside_rejected(self, sessions_dir)`
  - `test_traversal_rejected` (method, line 61) `def test_traversal_rejected(self, sessions_dir)`
  - `test_symlink_escape_rejected` (method, line 64) `def test_symlink_escape_rejected(self, sessions_dir, tmp_path)`
  - `test_empty_rejected` (method, line 74) `def test_empty_rejected(self, sessions_dir)`
  - `test_abort_propagates` (method, line 86) `def test_abort_propagates(self)`
  - `test_blueprint_redirect_uses_contained_resolver` (method, line 112) `def test_blueprint_redirect_uses_contained_resolver(self)`
- Depends on: `lazyc2/security/validators.py`

## tests/test_sidequest.py
- Doc: Tests for read-only side questions over immutable decision checkpoints.
- Layer: testing
- Language: py
- Symbols:
  - `_seed_ledger` (function, line 16) `def _seed_ledger(tmp_path, monkeypatch, rows)`
  - `_row` (function, line 24) `def _row(run_id, step, source, chosen)`
  - `test_checkpoint_id_is_stable_and_position_independent` (function, line 37) `def test_checkpoint_id_is_stable_and_position_independent()`
  - `test_checkpoint_id_differs_per_decision` (function, line 45) `def test_checkpoint_id_differs_per_decision()`
  - `test_list_checkpoints` (function, line 49) `def test_list_checkpoints(tmp_path, monkeypatch)`
  - `test_list_checkpoints_filters_run` (function, line 57) `def test_list_checkpoints_filters_run(tmp_path, monkeypatch)`
  - `test_get_checkpoint_round_trip` (function, line 63) `def test_get_checkpoint_round_trip(tmp_path, monkeypatch)`
  - `test_get_checkpoint_unknown` (function, line 71) `def test_get_checkpoint_unknown(tmp_path, monkeypatch)`
  - `test_ask_empty_question` (function, line 77) `def test_ask_empty_question(tmp_path, monkeypatch)`
  - `test_ask_unknown_checkpoint` (function, line 82) `def test_ask_unknown_checkpoint(tmp_path, monkeypatch)`
  - `test_ask_is_read_only_and_records` (function, line 88) `def test_ask_is_read_only_and_records(tmp_path, monkeypatch)`
  - `test_ask_handles_model_failure` (function, line 103) `def test_ask_handles_model_failure(tmp_path, monkeypatch)`
  - `_boom` (function, line 106) `def _boom()`
- Depends on: `modules/__init__.py`, `modules/loop/__init__.py`

## tests/test_single_implementation.py
- Doc: Single-implementation rule for extracted helpers.
- Layer: testing
- Language: py
- Symbols:
  - `TestDeadForkRemoved` (class, line 54) `class TestDeadForkRemoved`
  - `test_no_divergent_copies_in_core_parsers` (method, line 55) `def test_no_divergent_copies_in_core_parsers(self)`
  - `test_no_divergent_copies_in_core_namespace` (method, line 59) `def test_no_divergent_copies_in_core_namespace(self)`
  - `test_shared_kernel_still_available` (method, line 63) `def test_shared_kernel_still_available(self)`
  - `test_live_utils_implementations_intact` (method, line 68) `def test_live_utils_implementations_intact(self)`
- Depends on: `core/__init__.py`, `core/parsers.py`, `utils.py`

## tests/test_single_source_of_truth.py
- Doc: Single-source-of-truth contract tests.
- Layer: testing
- Language: py
- Symbols:
  - `_write` (function, line 26) `def _write(path, data)`
  - `AdvancePhaseSingleWriterSpec` (class, line 31) `class AdvancePhaseSingleWriterSpec(TestCase)`
  - `LazynmapPostSingleWriterSpec` (class, line 99) `class LazynmapPostSingleWriterSpec(TestCase)`
  - `StateManagerMergeSpec` (class, line 137) `class StateManagerMergeSpec(TestCase)`
  - `FactsIoCanonicalSpec` (class, line 201) `class FactsIoCanonicalSpec(TestCase)`
  - `ConsumePolicyFactsSpec` (class, line 273) `class ConsumePolicyFactsSpec(TestCase)`
  - `IntelligenceFactstoreSpec` (class, line 305) `class IntelligenceFactstoreSpec(TestCase)`
  - `ComplianceFactsSpec` (class, line 337) `class ComplianceFactsSpec(TestCase)`
  - `MispFactRecordsSpec` (class, line 365) `class MispFactRecordsSpec(TestCase)`
  - `_host_map_facts` (function, line 401) `def _host_map_facts()`
  - `test_extras_and_unknown_keys_are_preserved` (method, line 34) `def test_extras_and_unknown_keys_are_preserved(self)`
  - `test_extras_reapplied_after_host_advance` (method, line 56) `def test_extras_reapplied_after_host_advance(self)`
  - `test_invalid_phase_leaves_file_untouched` (method, line 89) `def test_invalid_phase_leaves_file_untouched(self)`
  - `test_post_scan_bumps_phase_via_killchain` (method, line 102) `def test_post_scan_bumps_phase_via_killchain(self)`
  - `_make_manager` (method, line 140) `def _make_manager(self, tmp)`
  - `test_sync_preserves_network_graph_and_campaign_fields` (method, line 153) `def test_sync_preserves_network_graph_and_campaign_fields(self)`
  - `test_canonical_passes_through` (method, line 242) `def test_canonical_passes_through(self)`
  - `test_legacy_wrapped_shape_resolves` (method, line 245) `def test_legacy_wrapped_shape_resolves(self)`
  - `test_flat_records_derive_observables` (method, line 253) `def test_flat_records_derive_observables(self)`
  - `test_load_reads_real_file` (method, line 266) `def test_load_reads_real_file(self)`
  - `test_consume_ingests_real_shape` (method, line 276) `def test_consume_ingests_real_shape(self)`
  - `test_collects_creds_and_vulns_from_canonical` (method, line 308) `def test_collects_creds_and_vulns_from_canonical(self)`
  - `test_findings_from_canonical` (method, line 340) `def test_findings_from_canonical(self)`
  - `test_fact_records_produce_findings` (method, line 368) `def test_fact_records_produce_findings(self)`
  - `test_cve_record` (method, line 373) `def test_cve_record(self)`
  - `test_host_map_resolves_nested_records` (method, line 383) `def test_host_map_resolves_nested_records(self)`
- Depends on: `cli/lazynmap_post.py`, `modules/compliance.py`, `modules/factsio.py`, `modules/integrations/misp_export.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/state_manager.py`, `modules/world_model.py`

## tests/test_sink_chain_feed.py
- Doc: Chain-feed sink contract: live step visibility and unhandled-failure steering.
- Layer: testing
- Language: py
- Symbols:
  - `_store_dir` (function, line 16) `def _store_dir(monkeypatch, tmp_path)`
  - `_step_event` (function, line 27) `def _step_event(steer)`
  - `test_ignores_out_of_scope_events` (function, line 44) `def test_ignores_out_of_scope_events(tmp_path)`
  - `test_rejects_unsafe_task_ids` (function, line 54) `def test_rejects_unsafe_task_ids(tmp_path)`
  - `test_trace_record_wakes_and_appends` (function, line 63) `def test_trace_record_wakes_and_appends(monkeypatch, tmp_path)`
  - `test_unhandled_failure_plants_one_pending_hint` (function, line 77) `def test_unhandled_failure_plants_one_pending_hint(monkeypatch, tmp_path)`
  - `test_steer_hint_dedupe_is_per_run` (function, line 95) `def test_steer_hint_dedupe_is_per_run(monkeypatch, tmp_path)`
  - `test_chain_step_activity_maps_to_planner_trigger` (function, line 111) `def test_chain_step_activity_maps_to_planner_trigger(monkeypatch, tmp_path)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/outcome_bus.py`, `modules/sinks/chain_feed.py`

## tests/test_sink_lazy_intel.py
- Doc: BDD tests for the dedicated lazy_intel sink.
- Layer: testing
- Language: py
- Symbols:
  - `_event` (function, line 15) `def _event(host, cve)`
  - `rigged` (function, line 47) `def rigged(monkeypatch, tmp_path)`
  - `TestSinkRouting` (class, line 61) `class TestSinkRouting`
  - `TestWorldMirror` (class, line 73) `class TestWorldMirror`
  - `TestDbMirror` (class, line 94) `class TestDbMirror`
  - `fake_get_db` (function, line 54) `def fake_get_db(_path)`
  - `test_other_kinds_ignored` (method, line 62) `def test_other_kinds_ignored(self, rigged)`
  - `test_missing_host_ignored` (method, line 66) `def test_missing_host_ignored(self, rigged)`
  - `test_fire_match_becomes_vulnerability` (method, line 74) `def test_fire_match_becomes_vulnerability(self, rigged)`
  - `test_dedupe_second_event` (method, line 84) `def test_dedupe_second_event(self, rigged)`
  - `test_vuln_row_inserted_with_refs` (method, line 95) `def test_vuln_row_inserted_with_refs(self, rigged)`
  - `test_db_dedupe` (method, line 106) `def test_db_dedupe(self, rigged)`
  - `test_severity_follows_tier` (method, line 114) `def test_severity_follows_tier(self, rigged)`
- Depends on: `modules/db.py`, `modules/outcome_bus.py`, `modules/sinks/__init__.py`, `modules/world_model.py`

## tests/test_sleep_obfuscation.py
- Doc: Tests for modules/sleep_obfuscation.py — SleepTechnique, SleepObfuscationConfig...
- Layer: testing
- Language: py
- Symbols:
  - `TestSleepTechnique` (class, line 33) `class TestSleepTechnique`
  - `TestSleepObfuscationConfig` (class, line 71) `class TestSleepObfuscationConfig`
  - `TestSleepTechniqueCatalog` (class, line 114) `class TestSleepTechniqueCatalog`
  - `TestSleepTechniqueValidator` (class, line 164) `class TestSleepTechniqueValidator`
  - `TestSleepObfuscationEngine` (class, line 212) `class TestSleepObfuscationEngine`
  - `TestBedEnumValues` (class, line 307) `class TestBedEnumValues`
  - `test_construction_and_properties` (method, line 34) `def test_construction_and_properties(self)`
  - `test_defaults` (method, line 48) `def test_defaults(self)`
  - `test_immutability` (method, line 60) `def test_immutability(self)`
  - `test_default_construction` (method, line 72) `def test_default_construction(self)`
  - `test_serialization_roundtrip` (method, line 79) `def test_serialization_roundtrip(self)`
  - `test_from_dict_empty` (method, line 102) `def test_from_dict_empty(self)`
  - `test_from_dict_partial` (method, line 107) `def test_from_dict_partial(self)`
  - `test_default_catalog_has_techniques` (method, line 115) `def test_default_catalog_has_techniques(self)`
  - `test_register_and_get` (method, line 120) `def test_register_and_get(self)`
  - `test_get_missing_raises_keyerror` (method, line 131) `def test_get_missing_raises_keyerror(self)`
  - `test_list_all_sorted_by_resistance` (method, line 136) `def test_list_all_sorted_by_resistance(self)`
  - `test_list_by_platform_windows` (method, line 142) `def test_list_by_platform_windows(self)`
  - `test_list_by_platform_linux` (method, line 149) `def test_list_by_platform_linux(self)`
  - `test_list_names` (method, line 156) `def test_list_names(self)`
  - `test_valid_config_passes` (method, line 165) `def test_valid_config_passes(self)`
  - `test_ekko_requires_rop_gadgets` (method, line 173) `def test_ekko_requires_rop_gadgets(self)`
  - `test_excessive_rop_gadget_count` (method, line 181) `def test_excessive_rop_gadget_count(self)`
  - `test_negative_sleep_delay` (method, line 189) `def test_negative_sleep_delay(self)`
  - `test_excessive_sleep_delay` (method, line 197) `def test_excessive_sleep_delay(self)`
  - `test_validate_config_enabled_without_name` (method, line 205) `def test_validate_config_enabled_without_name(self)`
  - `test_default_engine` (method, line 213) `def test_default_engine(self)`
  - `test_select_existing_technique` (method, line 219) `def test_select_existing_technique(self)`
  - `test_select_missing_technique` (method, line 225) `def test_select_missing_technique(self)`
  - `test_configure_updates_config` (method, line 230) `def test_configure_updates_config(self)`
  - `test_configure_without_overrides` (method, line 239) `def test_configure_without_overrides(self)`
  - `test_validate_valid_config` (method, line 246) `def test_validate_valid_config(self)`
  - `test_validate_unknown_technique` (method, line 251) `def test_validate_unknown_technique(self)`
  - `test_recommend_windows` (method, line 257) `def test_recommend_windows(self)`
  - `test_recommend_linux` (method, line 263) `def test_recommend_linux(self)`
  - `test_to_dict` (method, line 270) `def test_to_dict(self)`
  - `test_from_dict_roundtrip` (method, line 278) `def test_from_dict_roundtrip(self)`
  - `test_from_dict_empty` (method, line 288) `def test_from_dict_empty(self)`
  - `test_custom_catalog` (method, line 293) `def test_custom_catalog(self)`
  - `test_os_platform_values` (method, line 308) `def test_os_platform_values(self)`
  - `test_technique_risk_values` (method, line 312) `def test_technique_risk_values(self)`
- Depends on: `modules/sleep_obfuscation.py`


Next: [KB_tests_p25.md](KB_tests_p25.md)
