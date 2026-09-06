# Subsystem: tests

## skills/claude_md_orchestrator/tests/conftest.py
- Layer: testing
- Language: py

## skills/claude_md_orchestrator/tests/test_orchestrator.py
- Layer: testing
- Language: py
- Symbols:
  - `tmp_run_dir` (function, line 46) `def tmp_run_dir(tmp_path)`
  - `config` (function, line 54) `def config(tmp_run_dir, tmp_path)`
  - `test_parser_extracts_contract` (function, line 78) `def test_parser_extracts_contract(config)`
  - `test_sdd_agent_writes_spec` (function, line 86) `def test_sdd_agent_writes_spec(config)`
  - `test_tdd_agent_lands_red` (function, line 102) `def test_tdd_agent_lands_red(config)`
  - `test_bdd_agent_lands_green` (function, line 118) `def test_bdd_agent_lands_green(config)`
  - `test_dod_validators_block_emoji` (function, line 133) `def test_dod_validators_block_emoji()`
  - `test_dod_validators_block_inline_comments` (function, line 140) `def test_dod_validators_block_inline_comments()`
  - `test_dod_validators_block_todo_markers` (function, line 147) `def test_dod_validators_block_todo_markers()`
  - `test_dod_validators_block_absolute_paths` (function, line 154) `def test_dod_validators_block_absolute_paths()`
  - `test_dod_validators_require_docstrings` (function, line 161) `def test_dod_validators_require_docstrings()`
  - `test_orchestrator_full_cycle` (function, line 168) `def test_orchestrator_full_cycle(config)`
  - `test_orchestrator_blocks_on_sad_path_shortage` (function, line 190) `def test_orchestrator_blocks_on_sad_path_shortage(config)`
  - `test_orchestrator_blocks_on_missing_contracts` (function, line 206) `def test_orchestrator_blocks_on_missing_contracts(tmp_run_dir, tmp_path)`
  - `test_documentation_agent_emits_fenced_markdown` (function, line 223) `def test_documentation_agent_emits_fenced_markdown(config)`
  - `test_boy_scout_returns_report` (function, line 239) `def test_boy_scout_returns_report(config)`
  - `test_cicd_agent_writes_pipeline` (function, line 262) `def test_cicd_agent_writes_pipeline(config)`
  - `test_models_spec_round_trip` (function, line 296) `def test_models_spec_round_trip()`
