# Subsystem: tests (page 1 of 22)
Pages: [KB_tests.md](KB_tests.md), [KB_tests_p2.md](KB_tests_p2.md), [KB_tests_p3.md](KB_tests_p3.md), [KB_tests_p4.md](KB_tests_p4.md), [KB_tests_p5.md](KB_tests_p5.md), [KB_tests_p6.md](KB_tests_p6.md), [KB_tests_p7.md](KB_tests_p7.md), [KB_tests_p8.md](KB_tests_p8.md), [KB_tests_p9.md](KB_tests_p9.md), [KB_tests_p10.md](KB_tests_p10.md), [KB_tests_p11.md](KB_tests_p11.md), [KB_tests_p12.md](KB_tests_p12.md), [KB_tests_p13.md](KB_tests_p13.md), [KB_tests_p14.md](KB_tests_p14.md), [KB_tests_p15.md](KB_tests_p15.md), [KB_tests_p16.md](KB_tests_p16.md), [KB_tests_p17.md](KB_tests_p17.md), [KB_tests_p18.md](KB_tests_p18.md), [KB_tests_p19.md](KB_tests_p19.md), [KB_tests_p20.md](KB_tests_p20.md), [KB_tests_p21.md](KB_tests_p21.md), [KB_tests_p22.md](KB_tests_p22.md)

## tests/__init__.py
- Layer: testing
- Language: py

## tests/conftest.py
- Doc: Global pytest isolation hooks.
- Layer: testing
- Language: py
- Symbols:
  - `_isolated_llm_health` (function, line 16) `def _isolated_llm_health(tmp_path, monkeypatch)`
  - `_fast_llm_connect_backoff` (function, line 46) `def _fast_llm_connect_backoff(monkeypatch)`
  - `_reset_world_model_singleton` (function, line 62) `def _reset_world_model_singleton()`
  - `_reset_guard_harness` (function, line 72) `def _reset_guard_harness()`
  - `_offline_llm_for_loop_tests` (function, line 91) `def _offline_llm_for_loop_tests(request, monkeypatch)`
  - `_isolated_path` (function, line 32) `def _isolated_path()`
  - `_offline` (function, line 108) `def _offline(model, prompt, max_tokens)`
  - `_HealthyRegistry` (class, line 113) `class _HealthyRegistry`
  - `healthy` (method, line 116) `def healthy(self, name)`
  - `report_failure` (method, line 119) `def report_failure(self, name, reason)`
  - `report_success` (method, line 122) `def report_success(self, name)`
- Depends on: `modules/guardrails/harness.py`, `modules/lazy_agent.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/loop_ai_bridge.py`, `modules/world_model.py`

## tests/integration_autonomous_flow.py
- Doc: test_autonomous_flow_integration: Simulates a simplified autonomous flow to verify module...
- Layer: testing
- Language: py
- Symbols:
  - `test_autonomous_flow_integration` (function, line 15) `def test_autonomous_flow_integration()`
- Depends on: `modules/moe_router.py`, `modules/obs_parser.py`, `modules/session_rag.py`

## tests/mutation_common.py
- Doc: Shared driver for curated mutation runners.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 20) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 30) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 37) `def run_tests(test_targets)`
  - `title` (function, line 49) `def title(name)`
  - `run_all` (function, line 56) `def run_all(mutations, test_targets)`
- Imported by: `tests/run_mutation_loop_cli_catalog.py`, `tests/run_mutation_trigger_policy.py`, `tests/run_mutation_verb_catalog.py`

## tests/run_mutation_addon_creator.py
- Doc: Manual mutation testing runner for the LazyAddon creator contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 94) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 112) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 125) `def run_tests()`
  - `main` (function, line 140) `def main()`

## tests/run_mutation_addon_updater.py
- Doc: Mutation runner for the lazyaddon update contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 47) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 57) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 64) `def run_tests()`
  - `main` (function, line 76) `def main()`

## tests/run_mutation_api_authz.py
- Doc: Mutation testing runner for core.api_authz and core.logging.
- Layer: presentation
- Language: py
- Symbols:
  - `_apply_mutation` (function, line 64) `def _apply_mutation(source, data)`
  - `_run_mutation_subprocess` (function, line 71) `def _run_mutation_subprocess(test)`
  - `run` (function, line 83) `def run()`

## tests/run_mutation_autonomous_ops.py
- Doc: Manual mutation runner for the LAZY port contracts.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 59) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 69) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 76) `def run_tests()`
  - `main` (function, line 87) `def main()`

## tests/run_mutation_beacon_dispatch.py
- Doc: Mutation runner for the beacon dispatch sink contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 40) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 50) `def restore_files(backups, base_dir, mutations)`
  - `run_scoped_tests` (function, line 56) `def run_scoped_tests(base_dir)`
  - `apply_mutation` (function, line 70) `def apply_mutation(info, base_dir)`
  - `main` (function, line 88) `def main()`

## tests/run_mutation_c2_route_auth.py
- Doc: Mutation gate for C2 route-level auth boundaries.
- Layer: presentation
- Language: py
- Symbols:
  - `_run_tests` (function, line 29) `def _run_tests()`
  - `main` (function, line 40) `def main()`

## tests/run_mutation_chain_v2.py
- Doc: Mutation runner for the chain v2 contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 82) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 92) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 99) `def run_tests()`
  - `main` (function, line 111) `def main()`

## tests/run_mutation_contract_manifest.py
- Doc: Mutation gate for the contract manifest drift checker.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 35) `def _run_tests()`
  - `main` (function, line 47) `def main()`

## tests/run_mutation_emulation_runner.py
- Doc: Mutation runner for the emulation-runner contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 54) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 64) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_infra_report.py
- Doc: Mutation runner for the disposable infra and reporting contracts.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 92) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 110) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 122) `def run_tests()`
  - `main` (function, line 137) `def main()`

## tests/run_mutation_intel_svg.py
- Doc: Mutation runner for the intel relations-svg contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 48) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 58) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 65) `def run_tests()`
  - `main` (function, line 77) `def main()`

## tests/run_mutation_killchain.py
- Doc: Manual mutation testing runner for the unified kill-chain contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 56) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 65) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 81) `def main()`

## tests/run_mutation_lazy_scope.py
- Doc: Mutation runner for the lab-only default scope contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 50) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 60) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 67) `def run_tests()`
  - `main` (function, line 79) `def main()`

## tests/run_mutation_llm.py
- Doc: Mutation runner for the LLM subsystem contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 60) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 69) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 74) `def run_tests()`
  - `main` (function, line 84) `def main()`

## tests/run_mutation_llm_orchestrator.py
- Doc: Mutation runner for the orchestrator-governed LLM failover contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 166) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 184) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 196) `def run_tests()`
  - `main` (function, line 220) `def main()`

## tests/run_mutation_loop_cli_catalog.py
- Doc: Mutation runner for the planner catalog visibility contract.
- Layer: testing
- Language: py
- Symbols:
  - `main` (function, line 50) `def main()`
- Depends on: `tests/mutation_common.py`

## tests/run_mutation_no_shell.py
- Doc: Mutation gate for the no-shell execution contract.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 25) `def _run_tests()`
  - `main` (function, line 37) `def main()`

## tests/run_mutation_opsec.py
- Doc: Mutation runner for the consolidated OPSEC scorer contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 59) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 68) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 73) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_orchestrator_yaml.py
- Doc: Mutation runner for the orchestrator YAML contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 54) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 64) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_outcome_bus.py
- Doc: Mutation runner for the outcome-bus contract.
- Layer: infrastructure
- Language: py
- Symbols:
  - `backup_files` (function, line 47) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 57) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 64) `def run_tests()`
  - `main` (function, line 76) `def main()`

## tests/run_mutation_phase1.py
- Doc: Mutation testing runner for Phase 1 data-gap closure.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 138) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 147) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 153) `def run_tests()`
  - `main` (function, line 164) `def main()`

## tests/run_mutation_shell_semantics.py
- Doc: Mutation gate for shell semantics and colored output.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 41) `def _run_tests()`
  - `main` (function, line 53) `def main()`

## tests/run_mutation_tests.py
- Doc: Manual mutation testing runner for LazyOwn connectivity improvements.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 69) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 78) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 84) `def run_tests()`
  - `main` (function, line 103) `def main()`

## tests/run_mutation_trigger_hints.py
- Doc: Mutation runner for the cve_hot hint fingerprint contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 50) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 60) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 67) `def run_tests()`
  - `main` (function, line 79) `def main()`

## tests/run_mutation_trigger_policy.py
- Doc: Mutation runner for the trigger policy contract.
- Layer: business_logic
- Language: py
- Symbols:
  - `main` (function, line 52) `def main()`
- Depends on: `tests/mutation_common.py`

## tests/run_mutation_ux_usability.py
- Doc: Mutation testing runner for the UX usability contracts.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 60) `def _run_tests()`
  - `_backups` (function, line 71) `def _backups(mutations)`
  - `_restore` (function, line 79) `def _restore(backups, mutations)`
  - `main` (function, line 84) `def main()`

## tests/run_mutation_verb_catalog.py
- Doc: Mutation runner for the verb catalog contract.
- Layer: testing
- Language: py
- Symbols:
  - `main` (function, line 52) `def main()`
- Depends on: `tests/mutation_common.py`

## tests/run_mutation_world_diff.py
- Doc: Mutation runner for the lazy world-diff contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 48) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 58) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 65) `def run_tests()`
  - `main` (function, line 77) `def main()`

## tests/test_aci_planner.py
- Doc: tests/test_aci_planner.py
- Layer: testing
- Language: py
- Symbols:
  - `_make_goal` (function, line 33) `def _make_goal()`
  - `_patched_paths` (function, line 47) `def _patched_paths(tmp_path)`
  - `_start_patches` (function, line 60) `def _start_patches(tmp_path)`
  - `_stop_patches` (function, line 77) `def _stop_patches(patchers)`
  - `_make_planner` (function, line 82) `def _make_planner(tmp_path, api_key)`
  - `_make_engine` (function, line 94) `def _make_engine(tmp_path, api_key)`
  - `TestACIGoal` (class, line 111) `class TestACIGoal`
  - `TestAttackPhase` (class, line 134) `class TestAttackPhase`
  - `TestACIPlan` (class, line 177) `class TestACIPlan`
  - `TestACIPlannerStatic` (class, line 244) `class TestACIPlannerStatic`
  - `TestACIPlannerLLM` (class, line 345) `class TestACIPlannerLLM`
  - `TestACIEngineStatus` (class, line 421) `class TestACIEngineStatus`
  - `TestACIEngineShouldReplan` (class, line 462) `class TestACIEngineShouldReplan`
  - `TestACIEngineReplan` (class, line 522) `class TestACIEngineReplan`
  - `TestACIEngineComplete` (class, line 596) `class TestACIEngineComplete`
  - `TestACIReflector` (class, line 626) `class TestACIReflector`
  - `TestMCPBridges` (class, line 723) `class TestMCPBridges`
  - `TestPersistenceHelpers` (class, line 829) `class TestPersistenceHelpers`
  - `TestCLI` (class, line 914) `class TestCLI`
  - `test_fields` (method, line 112) `def test_fields(self)`
  - `test_defaults` (method, line 122) `def test_defaults(self)`
  - `test_to_dict_round_trip` (method, line 135) `def test_to_dict_round_trip(self)`
  - `test_from_dict_ignores_extra_keys` (method, line 154) `def test_from_dict_ignores_extra_keys(self)`
  - `_make_plan` (method, line 178) `def _make_plan(self, phase_statuses)`
  - `test_completion_pct_all_done` (method, line 204) `def test_completion_pct_all_done(self)`
  - `test_completion_pct_none_done` (method, line 208) `def test_completion_pct_none_done(self)`
  - `test_completion_pct_partial` (method, line 212) `def test_completion_pct_partial(self)`
  - `test_active_phase_returns_first_pending_or_active` (method, line 216) `def test_active_phase_returns_first_pending_or_active(self)`
  - `test_active_phase_none_when_all_done` (method, line 221) `def test_active_phase_none_when_all_done(self)`
  - `test_to_dict_has_completion_pct` (method, line 225) `def test_to_dict_has_completion_pct(self)`
  - `test_round_trip` (method, line 231) `def test_round_trip(self)`
  - `test_plan_creates_file` (method, line 245) `def test_plan_creates_file(self, tmp_path)`
  - `test_plan_has_phases` (method, line 252) `def test_plan_has_phases(self, tmp_path)`
  - `test_first_phase_is_active` (method, line 257) `def test_first_phase_is_active(self, tmp_path)`
  - `test_subsequent_phases_are_pending` (method, line 262) `def test_subsequent_phases_are_pending(self, tmp_path)`
  - `test_objectives_injected_into_file` (method, line 268) `def test_objectives_injected_into_file(self, tmp_path)`
  - `test_objectives_ids_match_phase_objectives` (method, line 276) `def test_objectives_ids_match_phase_objectives(self, tmp_path)`
  - `test_phase_filter_restricts_phases` (method, line 287) `def test_phase_filter_restricts_phases(self, tmp_path)`
  - `test_objective_source_is_aci_planner` (method, line 293) `def test_objective_source_is_aci_planner(self, tmp_path)`
  - `test_plan_status_is_active` (method, line 302) `def test_plan_status_is_active(self, tmp_path)`
  - `test_plan_id_is_unique` (method, line 307) `def test_plan_id_is_unique(self, tmp_path)`
  - `test_plan_target_stored` (method, line 313) `def test_plan_target_stored(self, tmp_path)`
  - `test_plan_domain_stored` (method, line 318) `def test_plan_domain_stored(self, tmp_path)`
  - `test_objectives_contain_target_in_text` (method, line 323) `def test_objectives_contain_target_in_text(self, tmp_path)`
  - `test_plan_roundtrip_from_disk` (method, line 330) `def test_plan_roundtrip_from_disk(self, tmp_path)`
  - `_llm_response` (method, line 346) `def _llm_response(self, phases)`
  - `test_llm_phases_used_when_api_key_set` (method, line 355) `def test_llm_phases_used_when_api_key_set(self, tmp_path)`
  - `test_llm_objectives_injected` (method, line 380) `def test_llm_objectives_injected(self, tmp_path)`
  - `test_llm_failure_falls_back_to_static` (method, line 399) `def test_llm_failure_falls_back_to_static(self, tmp_path)`
  - `test_llm_bad_json_falls_back_to_static` (method, line 407) `def test_llm_bad_json_falls_back_to_static(self, tmp_path)`
  - `test_status_no_plan` (method, line 422) `def test_status_no_plan(self, tmp_path)`
  - `test_status_with_plan` (method, line 427) `def test_status_with_plan(self, tmp_path)`
  - `test_status_has_active_phase` (method, line 437) `def test_status_has_active_phase(self, tmp_path)`
  - `test_status_completion_zero_at_start` (method, line 444) `def test_status_completion_zero_at_start(self, tmp_path)`
  - `test_status_blocked_count_zero_at_start` (method, line 451) `def test_status_blocked_count_zero_at_start(self, tmp_path)`
  - `_write_objectives_blocked` (method, line 463) `def _write_objectives_blocked(self, obj_file, obj_ids)`
  - `test_should_replan_false_when_no_plan` (method, line 483) `def test_should_replan_false_when_no_plan(self, tmp_path)`
  - `test_should_replan_false_below_threshold` (method, line 487) `def test_should_replan_false_below_threshold(self, tmp_path)`
  - `test_should_replan_true_at_threshold` (method, line 496) `def test_should_replan_true_at_threshold(self, tmp_path)`
  - `test_should_replan_false_for_completed_plan` (method, line 507) `def test_should_replan_false_for_completed_plan(self, tmp_path)`
  - `test_replan_no_plan` (method, line 523) `def test_replan_no_plan(self, tmp_path)`
  - `test_replan_increments_count` (method, line 529) `def test_replan_increments_count(self, tmp_path)`
  - `test_replan_records_reason` (method, line 536) `def test_replan_records_reason(self, tmp_path)`
  - `test_replan_injects_new_objectives` (method, line 543) `def test_replan_injects_new_objectives(self, tmp_path)`
  - `test_replan_status_returns_to_active` (method, line 553) `def test_replan_status_returns_to_active(self, tmp_path)`
  - `test_replan_twice_counts_two` (method, line 560) `def test_replan_twice_counts_two(self, tmp_path)`
  - `test_replan_with_llm` (method, line 568) `def test_replan_with_llm(self, tmp_path)`
  - `test_complete_archives_plan` (method, line 597) `def test_complete_archives_plan(self, tmp_path)`
  - `test_complete_marks_plan_as_completed` (method, line 607) `def test_complete_marks_plan_as_completed(self, tmp_path)`
  - `test_complete_no_plan` (method, line 617) `def test_complete_no_plan(self, tmp_path)`
  - `_make_plan_with_statuses` (method, line 627) `def _make_plan_with_statuses(self, phase_statuses, replan_count)`
  - `test_reflect_blocked_phase_generates_lesson` (method, line 655) `def test_reflect_blocked_phase_generates_lesson(self, tmp_path)`
  - `test_reflect_done_after_replan_generates_lesson` (method, line 665) `def test_reflect_done_after_replan_generates_lesson(self, tmp_path)`
  - `test_reflect_no_lessons_clean_plan` (method, line 674) `def test_reflect_no_lessons_clean_plan(self, tmp_path)`
  - `test_reflect_persists_to_file` (method, line 683) `def test_reflect_persists_to_file(self, tmp_path)`
  - `test_reflect_lesson_has_required_fields` (method, line 698) `def test_reflect_lesson_has_required_fields(self, tmp_path)`
  - `test_mcp_aci_status_no_plan` (method, line 724) `def test_mcp_aci_status_no_plan(self, tmp_path)`
  - `test_mcp_aci_plan_returns_json` (method, line 734) `def test_mcp_aci_plan_returns_json(self, tmp_path)`
  - `test_mcp_aci_plan_uses_rhost_from_payload` (method, line 747) `def test_mcp_aci_plan_uses_rhost_from_payload(self, tmp_path)`
  - `test_mcp_aci_plan_static_backend` (method, line 758) `def test_mcp_aci_plan_static_backend(self, tmp_path)`
  - `test_mcp_aci_replan_no_plan` (method, line 769) `def test_mcp_aci_replan_no_plan(self, tmp_path)`
  - `test_mcp_aci_replan_with_plan` (method, line 780) `def test_mcp_aci_replan_with_plan(self, tmp_path)`
  - `test_mcp_aci_status_after_plan` (method, line 793) `def test_mcp_aci_status_after_plan(self, tmp_path)`
  - `test_mcp_aci_plan_phase_filter` (method, line 806) `def test_mcp_aci_plan_phase_filter(self, tmp_path)`
  - `test_save_load_plan_roundtrip` (method, line 830) `def test_save_load_plan_roundtrip(self, tmp_path)`
  - `test_load_plan_returns_none_for_missing` (method, line 845) `def test_load_plan_returns_none_for_missing(self, tmp_path)`
  - `test_load_plan_returns_none_for_corrupt` (method, line 851) `def test_load_plan_returns_none_for_corrupt(self, tmp_path)`
  - `test_archive_plan_appends` (method, line 859) `def test_archive_plan_appends(self, tmp_path)`
  - `test_count_objectives_by_status` (method, line 876) `def test_count_objectives_by_status(self, tmp_path)`
  - `test_count_objectives_returns_empty_for_missing_file` (method, line 904) `def test_count_objectives_returns_empty_for_missing_file(self, tmp_path)`
  - `test_plan_command` (method, line 915) `def test_plan_command(self, tmp_path)`
  - `test_status_command_no_plan` (method, line 926) `def test_status_command_no_plan(self, tmp_path, capsys)`
  - `test_replan_command_no_plan` (method, line 940) `def test_replan_command_no_plan(self, tmp_path, capsys)`
  - `test_no_subcommand_returns_nonzero` (method, line 954) `def test_no_subcommand_returns_nonzero(self, tmp_path)`
  - `test_reflect_command_no_plan` (method, line 960) `def test_reflect_command_no_plan(self, tmp_path, capsys)`
- Depends on: `skills/aci_planner.py`

## tests/test_ad_lab_gym.py
- Doc: Contract tests for the AD lab gym (Docker Samba DC) matrix and capture.
- Layer: testing
- Language: py
- Symbols:
  - `AdLabCatalogueSpec` (class, line 30) `class AdLabCatalogueSpec(TestCase)`
  - `AdLabCaptureSpec` (class, line 57) `class AdLabCaptureSpec(TestCase)`
  - `AdLabRuntimeSpec` (class, line 114) `class AdLabRuntimeSpec(TestCase)`
  - `AdLabGymDefinitionsSpec` (class, line 187) `class AdLabGymDefinitionsSpec(TestCase)`
  - `test_matrix_validates` (method, line 33) `def test_matrix_validates(self)`
  - `test_summary_shape` (method, line 36) `def test_summary_shape(self)`
  - `test_all_vectors_resolve` (method, line 42) `def test_all_vectors_resolve(self)`
  - `test_get_unknown_is_none` (method, line 53) `def test_get_unknown_is_none(self)`
  - `test_kerberos_ticket_checker_direct` (method, line 60) `def test_kerberos_ticket_checker_direct(self)`
  - `test_domain_enum_capture` (method, line 65) `def test_domain_enum_capture(self)`
  - `test_smb_shares_capture` (method, line 77) `def test_smb_shares_capture(self)`
  - `test_credentials_capture_for_default_creds` (method, line 89) `def test_credentials_capture_for_default_creds(self)`
  - `test_samr_enum_capture` (method, line 101) `def test_samr_enum_capture(self)`
  - `test_scenario_targets_samba_image` (method, line 117) `def test_scenario_targets_samba_image(self)`
  - `test_start_rejects_unknown_scenario` (method, line 124) `def test_start_rejects_unknown_scenario(self)`
  - `test_ensure_ad_lab_probe_failure_is_quiet` (method, line 129) `def test_ensure_ad_lab_probe_failure_is_quiet(self)`
  - `test_ensure_ad_lab_creates_fixture_once` (method, line 139) `def test_ensure_ad_lab_creates_fixture_once(self)`
  - `test_ensure_ad_lab_skips_existing_fixture` (method, line 160) `def test_ensure_ad_lab_skips_existing_fixture(self)`
  - `test_readiness_without_docker` (method, line 180) `def test_readiness_without_docker(self)`
  - `test_ad_lab_apt_definition_valid` (method, line 190) `def test_ad_lab_apt_definition_valid(self)`
  - `test_ad_domain_enum_definition_valid` (method, line 196) `def test_ad_domain_enum_definition_valid(self)`
  - `fake_docker` (function, line 143) `def fake_docker()`
  - `fake_docker2` (function, line 148) `def fake_docker2()`
  - `fake_docker` (function, line 164) `def fake_docker()`
  - `fake_docker2` (function, line 171) `def fake_docker2()`
- Depends on: `modules/__init__.py`


Next: [KB_tests_p2.md](KB_tests_p2.md)
