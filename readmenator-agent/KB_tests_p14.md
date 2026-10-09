# Subsystem: tests (page 14 of 14)
Previous: [KB_tests_p13.md](KB_tests_p13.md)

## tests/test_wizard_llm.py
- Doc: Contract tests for the wizard LLM provider setup step.
- Layer: testing
- Language: py
- Symbols:
  - `_scripted_prompt` (function, line 14) `def _scripted_prompt(answers)`
  - `TestNormalizeProviderAnswer` (class, line 23) `class TestNormalizeProviderAnswer`
  - `TestMaskSecret` (class, line 45) `class TestMaskSecret`
  - `TestAskLlm` (class, line 59) `class TestAskLlm`
  - `TestReadinessLlm` (class, line 123) `class TestReadinessLlm`
  - `_fake` (method, line 17) `def _fake(message)`
  - `test_blank_returns_none` (method, line 24) `def test_blank_returns_none(self)`
  - `test_name_case_insensitive` (method, line 28) `def test_name_case_insensitive(self)`
  - `test_number_selects_backend` (method, line 32) `def test_number_selects_backend(self)`
  - `test_out_of_range_number_returns_none` (method, line 37) `def test_out_of_range_number_returns_none(self)`
  - `test_unknown_name_returns_none` (method, line 41) `def test_unknown_name_returns_none(self)`
  - `test_empty_returns_not_set` (method, line 46) `def test_empty_returns_not_set(self)`
  - `test_long_value_masked_with_tail` (method, line 50) `def test_long_value_masked_with_tail(self)`
  - `test_short_value_never_shown_clear` (method, line 53) `def test_short_value_never_shown_clear(self)`
  - `test_blank_answers_keep_everything` (method, line 60) `def test_blank_answers_keep_everything(self, monkeypatch)`
  - `test_provider_change_by_name` (method, line 65) `def test_provider_change_by_name(self, monkeypatch)`
  - `test_provider_change_by_number` (method, line 70) `def test_provider_change_by_number(self, monkeypatch)`
  - `test_invalid_provider_keeps_current` (method, line 76) `def test_invalid_provider_keeps_current(self, monkeypatch)`
  - `test_model_override_stored_in_provider_slot` (method, line 80) `def test_model_override_stored_in_provider_slot(self, monkeypatch)`
  - `test_ollama_skips_key_prompt` (method, line 91) `def test_ollama_skips_key_prompt(self, monkeypatch)`
  - `test_key_kept_when_blank` (method, line 104) `def test_key_kept_when_blank(self, monkeypatch)`
  - `test_existing_key_prompt_shows_mask` (method, line 108) `def test_existing_key_prompt_shows_mask(self, monkeypatch)`
  - `_row` (method, line 124) `def _row(self, params, label)`
  - `test_cloud_with_key_ok` (method, line 128) `def test_cloud_with_key_ok(self)`
  - `test_cloud_without_key_missing` (method, line 133) `def test_cloud_without_key_missing(self)`
  - `test_ollama_keyless_ok` (method, line 138) `def test_ollama_keyless_ok(self)`
  - `test_invalid_backend_missing_with_fix_hint` (method, line 143) `def test_invalid_backend_missing_with_fix_hint(self)`
  - `test_model_shown_in_value` (method, line 148) `def test_model_shown_in_value(self)`
  - `test_sensitive_values_masked` (method, line 152) `def test_sensitive_values_masked(self)`
  - `_fake` (method, line 94) `def _fake(message)`
  - `_fake` (method, line 111) `def _fake(message)`
- Depends on: `cli/wizard.py`, `modules/llm_factory.py`

## tests/test_world_model_extended.py
- Doc: Tests for extended WorldModel methods: set_os_hint, get_host, get_hosts_summary.
- Layer: testing
- Language: py
- Symbols:
  - `world_model` (function, line 14) `def world_model()`
  - `TestSetOsHint` (class, line 22) `class TestSetOsHint`
  - `TestGetHost` (class, line 44) `class TestGetHost`
  - `TestGetHostsSummary` (class, line 63) `class TestGetHostsSummary`
  - `TestAdvanceHostEdgeCases` (class, line 76) `class TestAdvanceHostEdgeCases`
  - `TestGetPhaseAfterStateChanges` (class, line 94) `class TestGetPhaseAfterStateChanges`
  - `test_set_os_hint_on_new_host` (method, line 24) `def test_set_os_hint_on_new_host(self, world_model)`
  - `test_set_os_hint_on_existing_host` (method, line 30) `def test_set_os_hint_on_existing_host(self, world_model)`
  - `test_set_os_hint_empty_string_is_stored` (method, line 37) `def test_set_os_hint_empty_string_is_stored(self, world_model)`
  - `test_get_host_returns_none_for_unknown` (method, line 46) `def test_get_host_returns_none_for_unknown(self, world_model)`
  - `test_get_host_returns_entry_for_known` (method, line 49) `def test_get_host_returns_entry_for_known(self, world_model)`
  - `test_get_host_is_thread_safe` (method, line 55) `def test_get_host_is_thread_safe(self, world_model)`
  - `test_empty_summary` (method, line 65) `def test_empty_summary(self, world_model)`
  - `test_populated_summary` (method, line 68) `def test_populated_summary(self, world_model)`
  - `test_advance_host_skips_on_same_state` (method, line 78) `def test_advance_host_skips_on_same_state(self, world_model)`
  - `test_advance_host_skips_on_lower_state` (method, line 83) `def test_advance_host_skips_on_lower_state(self, world_model)`
  - `test_advance_host_to_owned_is_allowed_from_exploited` (method, line 88) `def test_advance_host_to_owned_is_allowed_from_exploited(self, world_model)`
  - `test_phase_derived_from_host_state` (method, line 96) `def test_phase_derived_from_host_state(self, world_model)`
  - `test_phase_post_exploitation_on_owned` (method, line 100) `def test_phase_post_exploitation_on_owned(self, world_model)`
  - `test_phase_complete_when_all_owned` (method, line 105) `def test_phase_complete_when_all_owned(self, world_model)`
  - `test_phase_recon_when_no_hosts` (method, line 110) `def test_phase_recon_when_no_hosts(self, world_model)`
- Depends on: `modules/world_model.py`

