# Subsystem: tests (page 20 of 20)
Previous: [KB_tests_p19.md](KB_tests_p19.md)

## tests/test_world_model_extended.py
- Doc: Tests for extended WorldModel methods: set_os_hint, get_host, get_hosts_summary.
- Layer: testing
- Language: py
- Symbols:
  - `world_model` (function, line 14) `def world_model()`
  - `TestSetOsHint` (class, line 22) `class TestSetOsHint`
  - `TestGetHost` (class, line 43) `class TestGetHost`
  - `TestGetHostsSummary` (class, line 61) `class TestGetHostsSummary`
  - `TestAdvanceHostEdgeCases` (class, line 73) `class TestAdvanceHostEdgeCases`
  - `TestGetPhaseAfterStateChanges` (class, line 90) `class TestGetPhaseAfterStateChanges`
  - `test_remove_host` (function, line 110) `def test_remove_host(tmp_path, monkeypatch)`
  - `test_set_os_hint_on_new_host` (method, line 23) `def test_set_os_hint_on_new_host(self, world_model)`
  - `test_set_os_hint_on_existing_host` (method, line 29) `def test_set_os_hint_on_existing_host(self, world_model)`
  - `test_set_os_hint_empty_string_is_stored` (method, line 36) `def test_set_os_hint_empty_string_is_stored(self, world_model)`
  - `test_get_host_returns_none_for_unknown` (method, line 44) `def test_get_host_returns_none_for_unknown(self, world_model)`
  - `test_get_host_returns_entry_for_known` (method, line 47) `def test_get_host_returns_entry_for_known(self, world_model)`
  - `test_get_host_is_thread_safe` (method, line 53) `def test_get_host_is_thread_safe(self, world_model)`
  - `test_empty_summary` (method, line 62) `def test_empty_summary(self, world_model)`
  - `test_populated_summary` (method, line 65) `def test_populated_summary(self, world_model)`
  - `test_advance_host_skips_on_same_state` (method, line 74) `def test_advance_host_skips_on_same_state(self, world_model)`
  - `test_advance_host_skips_on_lower_state` (method, line 79) `def test_advance_host_skips_on_lower_state(self, world_model)`
  - `test_advance_host_to_owned_is_allowed_from_exploited` (method, line 84) `def test_advance_host_to_owned_is_allowed_from_exploited(self, world_model)`
  - `test_phase_derived_from_host_state` (method, line 91) `def test_phase_derived_from_host_state(self, world_model)`
  - `test_phase_post_exploitation_on_owned` (method, line 95) `def test_phase_post_exploitation_on_owned(self, world_model)`
  - `test_phase_complete_when_all_owned` (method, line 100) `def test_phase_complete_when_all_owned(self, world_model)`
  - `test_phase_recon_when_no_hosts` (method, line 105) `def test_phase_recon_when_no_hosts(self, world_model)`
- Depends on: `modules/world_model.py`

## tests/test_xss_sanitization.py
- Doc: Untrusted data rendered into the DOM must be neutralized.
- Layer: testing
- Language: py
- Symbols:
  - `_src` (function, line 18) `def _src(name)`
  - `TestXssSinks` (class, line 22) `class TestXssSinks`
  - `test_collab_events_escaped` (method, line 23) `def test_collab_events_escaped(self)`
  - `test_yaml_view_loads_purify` (method, line 28) `def test_yaml_view_loads_purify(self)`
  - `test_yaml_view_chatbot_sanitized` (method, line 32) `def test_yaml_view_chatbot_sanitized(self)`
  - `test_new_campaign_chunks_sanitized` (method, line 37) `def test_new_campaign_chunks_sanitized(self)`
  - `test_surface_labels_escaped` (method, line 42) `def test_surface_labels_escaped(self)`
  - `test_index_lazyos_response_sanitized` (method, line 47) `def test_index_lazyos_response_sanitized(self)`

