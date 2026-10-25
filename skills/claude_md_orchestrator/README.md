# Claude MD Orchestrator

I orchestrate the Spec-Driven Development plus Test-Driven Development
plus Behavior-Driven Development cycle from a single markdown source
of truth. The skill walks every contract through six stages and halts
on the first blocker. The skill is the production implementation of
the methodology the LazyOwn CLAUDE.md declares.

## The pipeline

```
CLAUDE.md
   |
   v
parser.load_contracts
   |
   v
sdd_agent.run  (writes specs/<id>.yaml)
   |
   v
tdd_agent.run  (writes tests/test_<id>.py)   <- halts at red
   |
   v
bdd_agent.run  (writes src/<id>.py)           <- halts at green
   |
   v
reviewer_agent.run  (writes review/<id>.json)
   |
   v
documentation_agent.run  (writes docs/<id>.md)
   |
   v
boy_scout.run  (writes review/<id>.scout.md)
   |
   v
cicd_agent.run  (writes pipeline.yml, pr_body.md)
   |
   v
human deploy gate  (closed by default)
```

## The agents

| Agent | File | Responsibility |
|-------|------|----------------|
| Spec-Driven Development | `sdd_agent.py` | Lifts a Contract into a Spec. |
| Test-Driven Development | `tdd_agent.py` | Produces a pytest module that fails. |
| Behavior-Driven Development | `bdd_agent.py` | Produces the source that makes the tests pass. |
| Reviewer | `reviewer_agent.py` | Runs ruff, mypy, bandit, and the DoD validators. |
| Documentation | `documentation_agent.py` | Emits first person scientific English. |
| Boy Scout | `boy_scout.py` | Scans the artifacts for tech debt and security gaps. |
| CI and CD | `cicd_agent.py` | Cuts a feature branch, writes the workflow, prepares the PR body. |

## The DoD

The DoD is the contract the reviewer enforces. The full list lives in
`validators.py`. The high level rules follow.

1. English only.
2. No comments in code.
3. No emoji.
4. Docstrings on every public symbol.
5. No hardcoded paths, ports, IPs, or credentials.
6. No magic numbers outside the local config.
7. No TODO, FIXME, XXX, or HACK markers.
8. No partial implementations.
9. No back compat shims for unshipped code.
10. Boy scout: tech debt and security gaps found in scope are fixed
    in the same change.
11. DRY plus SOLID: two paths that duplicate logic consolidate.
12. Tests trend to one hundred percent for the changed module.
13. Docs follow code.

## How to run a contract

```bash
PYTHONPATH=skills python3 -m claude_md_orchestrator.orchestrator \
  --no-parse \
  --seed C-002
```

The orchestrator writes the artifacts under
`skills/claude_md_orchestrator/runs/current/`. The operator copies the
strict pipeline into `.github/workflows/`. The operator commits the
changes. The operator opens the deploy gate only when the human
reviewer signs off.

## How to add a new agent

1. Create a new file under `skills/claude_md_orchestrator/`.
2. Add a public `run` function that takes the cycle state and the
   config and returns a typed result.
3. Wire the agent into `orchestrator._advance` after the previous
   stage.
4. Add tests in `tests/test_orchestrator.py`.
5. Update `SPECS.md` and `SKILL.md` to record the new stage.

## Tests

```bash
PYTHONPATH=skills python3 -m pytest skills/claude_md_orchestrator/tests/ -q
```

The test suite pins the behavior of every agent and the orchestrator
end to end. The tests run in a temporary run directory so they never
touch the real cycle state.
