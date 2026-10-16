# Subsystem: contract

## tests/contract/__init__.py
- Layer: testing
- Language: py

## tests/contract/test_suite_homologation.py
- Doc: SDD suite homologation contract for LazyOwn tests.
- Layer: testing
- Language: py
- Symbols:
  - `_test_modules` (function, line 50) `def _test_modules()`
  - `TestSuiteNaming` (class, line 61) `class TestSuiteNaming`
  - `TestPytestMarkers` (class, line 82) `class TestPytestMarkers`
  - `TestDeployGate` (class, line 99) `class TestDeployGate`
  - `TestMutationCoverage` (class, line 120) `class TestMutationCoverage`
  - `TestSuiteDocumentation` (class, line 141) `class TestSuiteDocumentation`
  - `test_at_least_one_test_module_exists` (method, line 64) `def test_at_least_one_test_module_exists(self)`
  - `test_module_names_are_english_snake_case` (method, line 68) `def test_module_names_are_english_snake_case(self)`
  - `test_no_emoji_in_test_module_names` (method, line 74) `def test_no_emoji_in_test_module_names(self)`
  - `test_required_markers_registered` (method, line 85) `def test_required_markers_registered(self)`
  - `test_strict_markers_enabled` (method, line 91) `def test_strict_markers_enabled(self)`
  - `test_deploynator_toml_exists` (method, line 102) `def test_deploynator_toml_exists(self)`
  - `test_deploy_gate_runs_full_suite` (method, line 106) `def test_deploy_gate_runs_full_suite(self)`
  - `test_deploy_timeouts_allow_long_runs` (method, line 111) `def test_deploy_timeouts_allow_long_runs(self)`
  - `test_required_mutation_runners_exist` (method, line 123) `def test_required_mutation_runners_exist(self)`
  - `test_mutation_gate_script_exists` (method, line 128) `def test_mutation_gate_script_exists(self)`
  - `test_mutmut_config_scoped` (method, line 132) `def test_mutmut_config_scoped(self)`
  - `test_suite_guide_exists` (method, line 144) `def test_suite_guide_exists(self)`
  - `test_contract_readme_exists` (method, line 148) `def test_contract_readme_exists(self)`
  - `test_suite_guide_is_english_without_emoji` (method, line 152) `def test_suite_guide_is_english_without_emoji(self)`
