# Contract: claude_md_orchestrator

I built this skill to make the SDD + TDD + BDD + Boy Scout cycle reproducible
from a single source of truth, which is the repository CLAUDE.md file.

The goal is mechanical. Given a CLAUDE.md, the skill extracts the actionable
contracts, writes the specs, writes the tests until they are red, writes the
implementation until the tests are green, runs a strict review, and prepares
the PR plus the CI pipeline. The boy-scout pass runs after every cycle so
tech debt and security gaps discovered along the way do not accumulate.

The skill is one script per contract. There are no shared mutable globals.
Every agent reads its inputs from disk and writes its outputs to disk. The
orchestrator wires the agents by passing paths.

The contract below is the DoD. It is enforced by validators. If a validator
fails, the cycle halts and the orchestrator reports the contract that failed.

---

## Agents

1. sdd_agent: produces a YAML spec for each contract. The spec covers the
   trigger, the inputs, the happy path, at least six sad paths, the data
   flow, the exit signal, and the observability.
2. tdd_agent: produces pytest tests that exercise the spec. The cycle halts
   at red. The agent will not advance until pytest reports failure for the
   new tests.
3. bdd_agent: produces the implementation that makes the tests green. The
   cycle halts at green. The agent will not advance until pytest reports
   pass for the new tests.
4. reviewer_agent: runs ruff, mypy, bandit, and the in house DoD
   validators. The cycle halts at approve. The agent will not advance until
   the report shows zero blockers and at most non blocking findings.
5. cicd_agent: cuts a feature branch from dev, commits the changes, writes
   the CI workflow, and prepares a PR body. The cycle halts at deploy gate.
   The agent will not advance until a human signals deploy.
6. documentation_agent: emits first person scientific English. No emoji.
   No em dash. No comments. No textbook format. No grand claims that are
   not backed by tests. The block is wrapped in a markdown code fence and
   signed by grisun0.
7. boy_scout: after a green cycle, scans for tech debt and security gaps
   inside the changed files. Fixes them. Re runs the cycle. Updates the
   docs.

---

## Definition of Done

The following rules bind every artifact produced by any agent. The
reviewer enforces them. A finding is a blocker if it is a DoD violation. A
finding is non blocking if it is a style nit that the boy scout can fix.

1. English only in identifiers, strings, logs, docstrings.
2. No comments in code. Docstrings only.
3. No emoji in code, logs, or docs. The agent may not insert emoji to
   decorate output.
4. Every public function and class carries a docstring with Args, Returns,
   and Raises where applicable.
5. No magic numbers. Constants live in the local config module or in the
   shared config module.
6. No hardcoded paths, ports, IPs, wordlists, or credentials. The skill
   reads them from the repository config or from the test fixture.
7. SOLID: single responsibility, open for extension, Liskov compatible
   selectors, small interfaces, depend on abstractions.
8. No placeholders. No TODOs. No FIXMEs. No XXXs.
9. No partial implementations. The cycle ends only at green plus approve.
10. No back compat shims for unshipped code.
11. Every new directory carries a README.md. The skill writes it.
12. Boy scout: tech debt and security gaps found in scope are fixed in
    the same change. The fixer documents the finding in the PR body.
13. DRY plus SOLID. Two paths that duplicate logic at ten lines or one
    decision tree are consolidated.
14. Tests trend to one hundred percent for the changed module. New public
    surface ships with tests. Skip and xfail are not allowed.
15. Docs follow code. README, CLAUDE, and the skill docs are updated in
    the same cycle.

---

## Outputs per cycle

For each contract, the orchestrator writes the following files inside the
run directory.

| File | Producer | Consumer |
|------|----------|----------|
| `specs/<id>.yaml` | sdd_agent | tdd_agent, bdd_agent |
| `tests/test_<id>.py` | tdd_agent | bdd_agent, reviewer_agent |
| `src/<id>.py` | bdd_agent | reviewer_agent |
| `review/<id>.json` | reviewer_agent | cicd_agent |
| `docs/<id>.md` | documentation_agent | human reviewer |
| `branch.txt` | cicd_agent | human reviewer |
| `pipeline.yml` | cicd_agent | CI |
| `pr_body.md` | cicd_agent | human reviewer |
| `state.json` | orchestrator | resume |

The orchestrator updates state.json after every stage so a crash can
resume the cycle from the last green stage.

---

## Failure modes the orchestrator must handle

1. The parser returns zero contracts. The orchestrator aborts and asks
   the operator to add at least one actionable contract to CLAUDE.md.
2. The spec writer fails the DoD check. The cycle halts at SDD and the
   orchestrator surfaces the violations.
3. The test runner cannot reach red. The cycle halts and the orchestrator
   reports which test is unexpectedly green.
4. The implementation reaches green without touching the spec, or the
   diff shows the test was weakened. The cycle halts and the orchestrator
   flags the integrity breach.
5. The reviewer reports a blocker. The cycle halts. The orchestrator
   produces a fix plan and waits for the operator to call the bdd agent
   again.
6. The git workspace is dirty. The cicd agent refuses to commit.
7. The CI workflow cannot be parsed. The cicd agent halts.
8. The deploy gate is reached without a human signal. The cicd agent
   halts and never calls any deploy tool.

---

## First flank

I will attack the CI hardening gap. The repository has pytest behind
`|| true` and `continue-on-error: true` in ci.yml and test.yml. The
expected outcome is a green CI that fails on a real regression, plus a
new strict job that runs ruff, mypy, and bandit, plus a fixed
test.yml without the swallow.

I will run the cycle on this flank, hand the diff to the operator, and
wait for the go signal before attacking the next gap.
