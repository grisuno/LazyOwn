# skills/claude_md_orchestrator

*Community 12 | 14 files | cohesion 0.79*

## Definition

This community groups 14 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.79). Central symbols: `AnalyzerResult`, `BddResult`, `CheckResult`, `CicdResult`, `CicleState`, `CicleStateFile`, `Config`, `Contract`. Core file: `skills/claude_md_orchestrator/models.py` (32 symbols). Documented purpose: This software must not be used by military or secret service organisations. License: GPL-3.0-only.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `pwntomate.py` | py | utility | 3 | yes |
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/config.py` | py | infrastructure | 15 | yes |
| `skills/claude_md_orchestrator/documentation_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/models.py` | py | business_logic | 32 | yes |
| `skills/claude_md_orchestrator/orchestrator.py` | py | utility | 21 | yes |
| `skills/claude_md_orchestrator/parser.py` | py | utility | 13 | yes |
| `skills/claude_md_orchestrator/reviewer_agent.py` | py | utility | 10 | yes |
| `skills/claude_md_orchestrator/sdd_agent.py` | py | utility | 6 | yes |
| `skills/claude_md_orchestrator/tdd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/validators.py` | py | utility | 21 | yes |

## Key Symbols

- `_build_substitutions` (function, `pwntomate.py:113`) `def _build_substitutions(host_addr, port, toolname_value, basedir_value, tunnel)` - Return the non-credential substitution map for a tool template.
- `_fix_sessions_owner` (function, `pwntomate.py:143`) `def _fix_sessions_owner()` - Best-effort ownership fixup, silent when not permitted.
- `_run_tool` (function, `pwntomate.py:203`) `def _run_tool(cmd)` - Run one auto-job command without shell interpretation.
- `_module_name` (function, `skills/claude_md_orchestrator/bdd_agent.py:80`) `def _module_name(contract)` - Return the python module name the implementation will use.
- `_module_path` (function, `skills/claude_md_orchestrator/bdd_agent.py:85`) `def _module_path(contract, config)` - Return the absolute path of the implementation module.
- `_package_init` (function, `skills/claude_md_orchestrator/bdd_agent.py:90`) `def _package_init(config)` - Return the absolute path of the implementation package init file.
- `_compose_implementation` (function, `skills/claude_md_orchestrator/bdd_agent.py:95`) `def _compose_implementation(spec, contract)` - Render the python source of the implementation module.
- `BddResult` (class, `skills/claude_md_orchestrator/bdd_agent.py:113`) `class BddResult` - Outcome of running the implementation agent.
- `_ensure_init` (function, `skills/claude_md_orchestrator/bdd_agent.py:130`) `def _ensure_init(config)` - Write the package init file the tests import from.
- `_run_pytest` (function, `skills/claude_md_orchestrator/bdd_agent.py:138`) `def _run_pytest(test_path, cwd)` - Run pytest and return the exit code plus the duration.
- `run` (function, `skills/claude_md_orchestrator/bdd_agent.py:151`) `def run(contract, spec, suite, config)` - Run the implementation agent for one contract.
- `ScoutReport` (class, `skills/claude_md_orchestrator/boy_scout.py:30`) `class ScoutReport` - Outcome of a boy scout pass.
- `_inspect` (function, `skills/claude_md_orchestrator/boy_scout.py:45`) `def _inspect(path)` - Run a deeper inspection on one source file.
- `_render_proposal` (function, `skills/claude_md_orchestrator/boy_scout.py:73`) `def _render_proposal(contract, findings)` - Render the human facing proposal text.
- `run` (function, `skills/claude_md_orchestrator/boy_scout.py:90`) `def run(state, config)` - Run the boy scout pass for one contract.
- `write_report` (function, `skills/claude_md_orchestrator/boy_scout.py:110`) `def write_report(report, config)` - Persist the boy scout proposal to disk.
- `CicdResult` (class, `skills/claude_md_orchestrator/cicd_agent.py:71`) `class CicdResult` - Outcome of the CI and CD agent.
- `_slug` (function, `skills/claude_md_orchestrator/cicd_agent.py:91`) `def _slug(contract)` - Return a safe slug for the branch name.
- `_git` (function, `skills/claude_md_orchestrator/cicd_agent.py:97`) `def _git()` - Run a git command and return the captured output.
- `_ensure_branch` (function, `skills/claude_md_orchestrator/cicd_agent.py:108`) `def _ensure_branch(contract, config)` - Create the feature branch from the base branch.
- `_render_pipeline` (function, `skills/claude_md_orchestrator/cicd_agent.py:134`) `def _render_pipeline(contract, spec, config)` - Render the workflow body the agent writes to disk.
- `_render_pr_body` (function, `skills/claude_md_orchestrator/cicd_agent.py:144`) `def _render_pr_body(contract, spec, report)` - Render the PR body the agent writes to disk.
- `run` (function, `skills/claude_md_orchestrator/cicd_agent.py:177`) `def run(contract, spec, report, config)` - Run the CI and CD agent for one contract.
- `_repo_root` (function, `skills/claude_md_orchestrator/config.py:22`) `def _repo_root()` - Return the absolute path of the LazyOwn repository root.
- `_default_run_dir` (function, `skills/claude_md_orchestrator/config.py:37`) `def _default_run_dir()` - Return the absolute path of the orchestrator run directory.
- `_default_claude_md` (function, `skills/claude_md_orchestrator/config.py:52`) `def _default_claude_md()` - Return the absolute path of the CLAUDE.md that the parser consumes.
- `Config` (class, `skills/claude_md_orchestrator/config.py:67`) `class Config` - Runtime configuration for the orchestrator.
- `ensure` (method, `skills/claude_md_orchestrator/config.py:112`) `def ensure(self)` - Create the run subdirectories if they do not exist.
- `state_path` (method, `skills/claude_md_orchestrator/config.py:122`) `def state_path(self)` - Return the absolute path of the cycle state file.
- `specs_dir` (method, `skills/claude_md_orchestrator/config.py:126`) `def specs_dir(self)` - Return the absolute path of the spec directory.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 34
- Cross-boundary resolved imports (EXTRACTED): 8

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [taint high] `cli/banner_config.py` -> `skills/claude_md_orchestrator/parser.py` via `subprocess` (5 hops)
- [cycle] `cli/commands/_base.py` -> `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `cli/commands/_base.py` -> `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.79?

## Sources

- `pwntomate.py`
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
