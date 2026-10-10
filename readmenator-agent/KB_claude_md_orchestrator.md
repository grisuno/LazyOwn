# Subsystem: claude_md_orchestrator

## skills/claude_md_orchestrator/__init__.py
- Doc: Public API for the claude_md_orchestrator skill.
- Layer: utility
- Language: py
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/orchestrator.py`

## skills/claude_md_orchestrator/bdd_agent.py
- Doc: Behavior-Driven Development agent.
- Layer: utility
- Language: py
- Symbols:
  - `_module_name` (function, line 80) `def _module_name(contract)`
  - `_module_path` (function, line 85) `def _module_path(contract, config)`
  - `_package_init` (function, line 90) `def _package_init(config)`
  - `_compose_implementation` (function, line 95) `def _compose_implementation(spec, contract)`
  - `BddResult` (class, line 113) `class BddResult`
  - `_ensure_init` (method, line 130) `def _ensure_init(config)`
  - `_run_pytest` (method, line 138) `def _run_pytest(test_path, cwd)`
  - `run` (method, line 151) `def run(contract, spec, suite, config)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`

## skills/claude_md_orchestrator/boy_scout.py
- Doc: Boy Scout refactor pass.
- Layer: utility
- Language: py
- Symbols:
  - `ScoutReport` (class, line 30) `class ScoutReport`
  - `_inspect` (method, line 45) `def _inspect(path)`
  - `_render_proposal` (method, line 73) `def _render_proposal(contract, findings)`
  - `run` (method, line 90) `def run(state, config)`
  - `write_report` (method, line 110) `def write_report(report, config)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`

## skills/claude_md_orchestrator/cicd_agent.py
- Doc: CI and CD agent.
- Layer: utility
- Language: py
- Symbols:
  - `CicdResult` (class, line 70) `class CicdResult`
  - `_slug` (method, line 90) `def _slug(contract)`
  - `_git` (method, line 96) `def _git()`
  - `_ensure_branch` (method, line 107) `def _ensure_branch(contract, config)`
  - `_render_pipeline` (method, line 133) `def _render_pipeline(contract, spec, config)`
  - `_render_pr_body` (method, line 143) `def _render_pr_body(contract, spec, report)`
  - `run` (method, line 176) `def run(contract, spec, report, config)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`

## skills/claude_md_orchestrator/config.py
- Doc: Centralized configuration for the claude_md_orchestrator skill.
- Layer: infrastructure
- Language: py
- Symbols:
  - `_repo_root` (function, line 22) `def _repo_root()`
  - `_default_run_dir` (function, line 37) `def _default_run_dir()`
  - `_default_claude_md` (function, line 52) `def _default_claude_md()`
  - `Config` (class, line 67) `class Config`
  - `load_config` (method, line 155) `def load_config()`
  - `resolve_optional` (method, line 164) `def resolve_optional(config, key)`
  - `ensure` (method, line 112) `def ensure(self)`
  - `state_path` (method, line 122) `def state_path(self)`
  - `specs_dir` (method, line 126) `def specs_dir(self)`
  - `tests_dir` (method, line 130) `def tests_dir(self)`
  - `src_dir` (method, line 134) `def src_dir(self)`
  - `review_dir` (method, line 138) `def review_dir(self)`
  - `docs_dir` (method, line 142) `def docs_dir(self)`
  - `logs_dir` (method, line 146) `def logs_dir(self)`
  - `log_path` (method, line 150) `def log_path(self)`
- Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`

## skills/claude_md_orchestrator/documentation_agent.py
- Doc: Documentation agent.
- Layer: utility
- Language: py
- Symbols:
  - `DocResult` (class, line 28) `class DocResult`
  - `_format_inputs` (method, line 40) `def _format_inputs(spec)`
  - `_format_sad_paths` (method, line 47) `def _format_sad_paths(spec)`
  - `_format_review` (method, line 54) `def _format_review(report)`
  - `_render` (method, line 68) `def _render(contract, spec, report)`
  - `_wrap` (method, line 118) `def _wrap(body)`
  - `run` (method, line 123) `def run(contract, spec, report, config)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`

## skills/claude_md_orchestrator/models.py
- Doc: Data models for the claude_md_orchestrator skill.
- Layer: business_logic
- Language: py
- Symbols:
  - `_now_iso` (function, line 19) `def _now_iso()`
  - `Stage` (class, line 28) `class Stage(StrEnum)`
  - `Severity` (class, line 50) `class Severity(StrEnum)`
  - `Contract` (class, line 68) `class Contract`
  - `SadPath` (class, line 109) `class SadPath`
  - `Spec` (class, line 134) `class Spec`
  - `TestSuite` (class, line 217) `class TestSuite`
  - `Finding` (class, line 255) `class Finding`
  - `ReviewReport` (class, line 291) `class ReviewReport`
  - `CicleState` (class, line 348) `class CicleState`
  - `CicleStateFile` (class, line 424) `class CicleStateFile`
  - `write_jsonl` (method, line 480) `def write_jsonl(path, event)`
  - `to_dict` (method, line 91) `def to_dict(self)`
  - `from_dict` (method, line 96) `def from_dict(cls, data)`
  - `to_dict` (method, line 120) `def to_dict(self)`
  - `from_dict` (method, line 125) `def from_dict(cls, data)`
  - `to_dict` (method, line 166) `def to_dict(self)`
  - `from_dict` (method, line 173) `def from_dict(cls, data)`
  - `validate` (method, line 189) `def validate(self, min_sad_paths)`
  - `to_dict` (method, line 236) `def to_dict(self)`
  - `from_dict` (method, line 243) `def from_dict(cls, data)`
  - `to_dict` (method, line 270) `def to_dict(self)`
  - `from_dict` (method, line 280) `def from_dict(cls, data)`
  - `blockers` (method, line 315) `def blockers(self)`
  - `to_dict` (method, line 319) `def to_dict(self)`
  - `from_dict` (method, line 333) `def from_dict(cls, data)`
  - `to_dict` (method, line 383) `def to_dict(self)`
  - `from_dict` (method, line 402) `def from_dict(cls, data)`
  - `to_dict` (method, line 440) `def to_dict(self)`
  - `from_dict` (method, line 450) `def from_dict(cls, data)`
  - `save` (method, line 459) `def save(self, path)`
  - `load` (method, line 467) `def load(cls, path)`
- Depends on: `cli/commands/enum.py`
- Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`

## skills/claude_md_orchestrator/orchestrator.py
- Doc: Orchestrator that wires the agents into a deterministic pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `CycleSummary` (class, line 34) `class CycleSummary`
  - `_banner` (method, line 52) `def _banner(message, config)`
  - `_halt` (method, line 59) `def _halt(summary, contract_id, reason)`
  - `_persist` (method, line 66) `def _persist(state, config)`
  - `_load_state` (method, line 84) `def _load_state(config)`
  - `_seed_state` (method, line 89) `def _seed_state(contracts, state)`
  - `_run_spec` (method, line 97) `def _run_spec(state, config)`
  - `_run_test` (method, line 110) `def _run_test(state, config)`
  - `_run_implementation` (method, line 125) `def _run_implementation(state, config)`
  - `_run_review` (method, line 146) `def _run_review(state, config)`
  - `_run_documentation` (method, line 158) `def _run_documentation(state, config)`
  - `_run_scout` (method, line 174) `def _run_scout(state, config)`
  - `_run_cicd` (method, line 182) `def _run_cicd(state, config)`
  - `_load_spec` (method, line 217) `def _load_spec(path)`
  - `_advance` (method, line 234) `def _advance(state, contract_id, config, options)`
  - `run` (method, line 275) `def run(config, options)`
  - `_print_summary` (method, line 301) `def _print_summary(summary)`
  - `summary_to_dict` (method, line 306) `def summary_to_dict(summary)`
  - `_build_parser` (method, line 324) `def _build_parser()`
  - `_load_seed_contracts` (method, line 365) `def _load_seed_contracts(args, options)`
  - `main` (method, line 393) `def main(argv)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/parser.py`
- Imported by: `skills/claude_md_orchestrator/__init__.py`

## skills/claude_md_orchestrator/parser.py
- Doc: Parser that turns a CLAUDE.md into actionable contracts.
- Layer: utility
- Language: py
- Symbols:
  - `_Section` (class, line 34) `class _Section`
  - `_derive_contract_id` (method, line 56) `def _derive_contract_id(title, fallback_index)`
  - `_strip_contract_marker` (method, line 73) `def _strip_contract_marker(title)`
  - `_walk_sections` (method, line 85) `def _walk_sections(lines)`
  - `_collect_bullets` (method, line 123) `def _collect_bullets(text)`
  - `_collect_paragraphs` (method, line 141) `def _collect_paragraphs(text)`
  - `_is_actionable` (method, line 146) `def _is_actionable(heading)`
  - `_flatten_actionable` (method, line 159) `def _flatten_actionable(root)`
  - `parse_claude_md` (method, line 167) `def parse_claude_md(path)`
  - `_coerce_seed_contract` (method, line 205) `def _coerce_seed_contract(seed)`
  - `load_contracts` (method, line 225) `def load_contracts(config, seeds)`
  - `__post_init__` (method, line 51) `def __post_init__(self)`
  - `flush_body` (method, line 97) `def flush_body()`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- Imported by: `pwntomate.py`, `skills/claude_md_orchestrator/orchestrator.py`, `static/js/xterm.js`, `utils.py`

## skills/claude_md_orchestrator/reviewer_agent.py
- Doc: Code Reviewer and Quality Assurance agent.
- Layer: utility
- Language: py
- Symbols:
  - `AnalyzerResult` (class, line 30) `class AnalyzerResult`
  - `_run` (method, line 46) `def _run(cmd, cwd)`
  - `_resolve_targets` (method, line 72) `def _resolve_targets(state, config)`
  - `_parse_tool_findings` (method, line 88) `def _parse_tool_findings(result, path_prefix)`
  - `_run_ruff` (method, line 121) `def _run_ruff(targets, cwd)`
  - `_run_mypy` (method, line 134) `def _run_mypy(targets, cwd)`
  - `_run_bandit` (method, line 147) `def _run_bandit(targets, cwd)`
  - `_run_pytest` (method, line 160) `def _run_pytest(targets, cwd)`
  - `run` (method, line 171) `def run(state, config)`
  - `write_report` (method, line 225) `def write_report(report, config)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`

## skills/claude_md_orchestrator/sdd_agent.py
- Doc: Spec-Driven Development agent.
- Layer: utility
- Language: py
- Symbols:
  - `SddResult` (class, line 40) `class SddResult`
  - `_coerce_scope` (method, line 56) `def _coerce_scope(scope)`
  - `_compose_spec` (method, line 81) `def _compose_spec(contract, min_sad_paths)`
  - `_render_yaml` (method, line 130) `def _render_yaml(spec)`
  - `_ask_llm` (method, line 148) `def _ask_llm(contract, backend)`
  - `run` (method, line 204) `def run(contract, config)`
- Depends on: `modules/llm_factory.py`, `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`

## skills/claude_md_orchestrator/tdd_agent.py
- Doc: Test-Driven Development agent.
- Layer: utility
- Language: py
- Symbols:
  - `_slug` (function, line 79) `def _slug(value)`
  - `TddResult` (class, line 90) `class TddResult`
  - `_module_name` (method, line 105) `def _module_name(contract)`
  - `_compose_tests` (method, line 110) `def _compose_tests(spec, contract)`
  - `_run_pytest` (method, line 154) `def _run_pytest(test_path, cwd)`
  - `run` (method, line 175) `def run(contract, spec, config)`
  - `read_test_source` (method, line 228) `def read_test_source(test_path)`
- Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- Imported by: `skills/claude_md_orchestrator/bdd_agent.py`

## skills/claude_md_orchestrator/validators.py
- Doc: DoD validators for every artifact the orchestrator produces.
- Layer: utility
- Language: py
- Symbols:
  - `CheckResult` (class, line 65) `class CheckResult`
  - `find_block_comments` (method, line 85) `def find_block_comments(source)`
  - `find_inline_comments` (method, line 107) `def find_inline_comments(source)`
  - `check_no_comments` (method, line 124) `def check_no_comments(source, path)`
  - `check_no_emoji` (method, line 155) `def check_no_emoji(content, path)`
  - `check_no_forbidden_markers` (method, line 177) `def check_no_forbidden_markers(content, path)`
  - `check_english_only` (method, line 194) `def check_english_only(source, path)`
  - `check_docstrings` (method, line 218) `def check_docstrings(source, path)`
  - `check_no_hardcoded_paths_or_ips` (method, line 259) `def check_no_hardcoded_paths_or_ips(source, path)`
  - `check_magic_numbers` (method, line 293) `def check_magic_numbers(source, path, allow)`
  - `check_source` (method, line 328) `def check_source(source, path, allow_numbers)`
  - `check_markdown` (method, line 341) `def check_markdown(content, path)`
  - `check_spec` (method, line 350) `def check_spec(spec, min_sad_paths)`
  - `passed` (method, line 76) `def passed(self)`
  - `blocks` (method, line 80) `def blocks(self)`
- Depends on: `skills/claude_md_orchestrator/models.py`
- Imported by: `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`
