# skills/claude_md_orchestrator

*Community 19 | 13 files | cohesion 0.85*

## Definition

This community groups 13 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.85). Central symbols: `AnalyzerResult`, `BddResult`, `CheckResult`, `CicdResult`, `CicleState`, `CicleStateFile`, `Config`, `Contract`. Core file: `skills/claude_md_orchestrator/models.py` (32 symbols). Documented purpose: Public API for the claude_md_orchestrator skill.  The package re-exports the classes and the helper functions the CLI and the tests share. The orchestrator modu.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/config.py` | py | infrastructure | 15 | yes |
| `skills/claude_md_orchestrator/documentation_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/models.py` | py | business_logic | 32 | yes |
| `skills/claude_md_orchestrator/orchestrator.py` | py | utility | 21 | yes |
| `skills/claude_md_orchestrator/parser.py` | py | utility | 13 | yes |
| `skills/claude_md_orchestrator/reviewer_agent.py` | py | presentation | 10 | yes |
| `skills/claude_md_orchestrator/sdd_agent.py` | py | utility | 6 | yes |
| `skills/claude_md_orchestrator/tdd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/validators.py` | py | utility | 15 | yes |

## Key Symbols

- `_module_name` (function, `skills/claude_md_orchestrator/bdd_agent.py:80`) `def _module_name(contract)` - Return the python module name the implementation will use.
- `_module_path` (function, `skills/claude_md_orchestrator/bdd_agent.py:85`) `def _module_path(contract, config)` - Return the absolute path of the implementation module.
- `_package_init` (function, `skills/claude_md_orchestrator/bdd_agent.py:90`) `def _package_init(config)` - Return the absolute path of the implementation package init file.
- `_compose_implementation` (function, `skills/claude_md_orchestrator/bdd_agent.py:95`) `def _compose_implementation(spec, contract)` - Render the python source of the implementation module.
- `BddResult` (class, `skills/claude_md_orchestrator/bdd_agent.py:116`) `class BddResult` - Outcome of running the implementation agent.
- `_ensure_init` (method, `skills/claude_md_orchestrator/bdd_agent.py:133`) `def _ensure_init(config)` - Write the package init file the tests import from.
- `_run_pytest` (method, `skills/claude_md_orchestrator/bdd_agent.py:141`) `def _run_pytest(test_path, cwd)` - Run pytest and return the exit code plus the duration.
- `run` (method, `skills/claude_md_orchestrator/bdd_agent.py:154`) `def run(contract, spec, suite, config)` - Run the implementation agent for one contract.
- `ScoutReport` (class, `skills/claude_md_orchestrator/boy_scout.py:30`) `class ScoutReport` - Outcome of a boy scout pass.
- `_inspect` (method, `skills/claude_md_orchestrator/boy_scout.py:45`) `def _inspect(path)` - Run a deeper inspection on one source file.
- `_render_proposal` (method, `skills/claude_md_orchestrator/boy_scout.py:73`) `def _render_proposal(contract, findings)` - Render the human facing proposal text.
- `run` (method, `skills/claude_md_orchestrator/boy_scout.py:90`) `def run(state, config)` - Run the boy scout pass for one contract.
- `write_report` (method, `skills/claude_md_orchestrator/boy_scout.py:110`) `def write_report(report, config)` - Persist the boy scout proposal to disk.
- `CicdResult` (class, `skills/claude_md_orchestrator/cicd_agent.py:70`) `class CicdResult` - Outcome of the CI and CD agent.
- `_slug` (method, `skills/claude_md_orchestrator/cicd_agent.py:90`) `def _slug(contract)` - Return a safe slug for the branch name.
- `_git` (method, `skills/claude_md_orchestrator/cicd_agent.py:96`) `def _git()` - Run a git command and return the captured output.
- `_ensure_branch` (method, `skills/claude_md_orchestrator/cicd_agent.py:107`) `def _ensure_branch(contract, config)` - Create the feature branch from the base branch.
- `_render_pipeline` (method, `skills/claude_md_orchestrator/cicd_agent.py:133`) `def _render_pipeline(contract, spec, config)` - Render the workflow body the agent writes to disk.
- `_render_pr_body` (method, `skills/claude_md_orchestrator/cicd_agent.py:143`) `def _render_pr_body(contract, spec, report)` - Render the PR body the agent writes to disk.
- `run` (method, `skills/claude_md_orchestrator/cicd_agent.py:176`) `def run(contract, spec, report, config)` - Run the CI and CD agent for one contract.
- `_repo_root` (function, `skills/claude_md_orchestrator/config.py:22`) `def _repo_root()` - Return the absolute path of the LazyOwn repository root.
- `_default_run_dir` (function, `skills/claude_md_orchestrator/config.py:37`) `def _default_run_dir()` - Return the absolute path of the orchestrator run directory.
- `_default_claude_md` (function, `skills/claude_md_orchestrator/config.py:52`) `def _default_claude_md()` - Return the absolute path of the CLAUDE.md that the parser consumes.
- `Config` (class, `skills/claude_md_orchestrator/config.py:67`) `class Config` - Runtime configuration for the orchestrator.
- `ensure` (method, `skills/claude_md_orchestrator/config.py:114`) `def ensure(self)` - Create the run subdirectories if they do not exist.
- `state_path` (method, `skills/claude_md_orchestrator/config.py:124`) `def state_path(self)` - Return the absolute path of the cycle state file.
- `specs_dir` (method, `skills/claude_md_orchestrator/config.py:128`) `def specs_dir(self)` - Return the absolute path of the spec directory.
- `tests_dir` (method, `skills/claude_md_orchestrator/config.py:132`) `def tests_dir(self)` - Return the absolute path of the test directory.
- `src_dir` (method, `skills/claude_md_orchestrator/config.py:136`) `def src_dir(self)` - Return the absolute path of the implementation directory.
- `review_dir` (method, `skills/claude_md_orchestrator/config.py:140`) `def review_dir(self)` - Return the absolute path of the review directory.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 33
- Cross-boundary resolved imports (EXTRACTED): 5

## Connections

- [EXTRACTED] depends_on community 4 <-> 19 (strength 0.9): Extracted import edge crosses communities: pwntomate.py imports skills/claude_md_orchestrator/parser.py.

## Risks

- [taint high] `cli/banner_config.py` -> `skills/claude_md_orchestrator/parser.py` via `subprocess` (5 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.85?

## Sources

- `skills/claude_md_orchestrator/__init__.py`
- `skills/claude_md_orchestrator/bdd_agent.py`
- `skills/claude_md_orchestrator/boy_scout.py`
- `skills/claude_md_orchestrator/cicd_agent.py`
- `skills/claude_md_orchestrator/config.py`
- `skills/claude_md_orchestrator/documentation_agent.py`
- `skills/claude_md_orchestrator/models.py`
- `skills/claude_md_orchestrator/orchestrator.py`
- `skills/claude_md_orchestrator/parser.py`
- `skills/claude_md_orchestrator/reviewer_agent.py`
- `skills/claude_md_orchestrator/sdd_agent.py`
- `skills/claude_md_orchestrator/tdd_agent.py`
- `skills/claude_md_orchestrator/validators.py`
