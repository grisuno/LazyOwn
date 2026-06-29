---
name: claude_md_orchestrator
description: "Orchestrate the SDD plus TDD plus BDD plus Boy Scout cycle from a CLAUDE.md. Generates specs, tests, implementations, reviews, and CI pipelines. Halts at red and green. Closes the deploy gate by design."
version: 0.1.0
author: grisun0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [methodology, sdd, tdd, bdd, ci, devops, agent-orchestration]
    homepage: https://github.com/grisuno/LazyOwn
    related_skills: [lazyown, toposwarm]
---

# Claude MD Orchestrator

I read a CLAUDE.md file and walk every contract through six deterministic
stages. The skill produces a spec, a failing test, a passing
implementation, a review report, a documentation block, and a CI
pipeline. The deploy gate is closed by design.

The contract is the unit of work. The skill extracts the contracts
from the markdown, or accepts a seed contract from the operator. The
skill never invents a contract on its own. The skill never opens the
deploy gate without a shared secret the operator set through the
environment.

The skill enforces a strict Definition of Done. The DoD forbids
comments, emojis, hardcoded paths, magic numbers, missing docstrings,
and forbidden markers. The reviewer runs ruff, mypy, bandit, and the
in house DoD validators. The cycle halts on the first blocker when
the reviewer runs in strict mode.

## When to invoke

- The operator wants to convert a CLAUDE.md section into a tested
  implementation.
- The operator wants to enforce a strict pipeline that fails on
  every regression.
- The operator wants a reproducible artifact trail for an audit.

## How to invoke

The skill ships as a Python package under `skills/claude_md_orchestrator`.
The CLI entry point is the orchestrator module. The operator runs
the cycle from a LazyOwn checkout.

```bash
PYTHONPATH=skills python3 -m claude_md_orchestrator.orchestrator \
  --no-parse \
  --seed C-002 \
  --contract-file skills/claude_md_orchestrator/contracts/ci_strict_mode.md
```

The orchestrator writes every artifact under the run directory. The
operator copies the pipeline into `.github/workflows/`. The operator
commits the changes. The operator opens the deploy gate only when
the human reviewer signs off.

## The DoD in five lines

1. English only in identifiers, strings, logs, docstrings.
2. No comments in code. Docstrings only.
3. No emoji in code, logs, or docs.
4. No hardcoded paths, ports, IPs, wordlists, or credentials.
5. No TODO, FIXME, XXX, or HACK markers.

## The first flank

I tightened the CI workflow. The legacy workflow swallowed every
failure through the `|| true` shim and the `continue-on-error: true`
flag. The strict workflow fails on every regression. The contract
test `tests/test_ci_strict.py` pins the behaviour.
