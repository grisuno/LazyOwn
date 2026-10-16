# LazyOwn Test Suite

Production test suite for LazyOwn. One suite, four practices: SDD, TDD,
BDD, and mutation testing. English only, no emojis.

## Layout

| Path | Tier | Command |
|------|------|---------|
| `tests/test_*.py` | Unit and regression (TDD) | `python -m pytest tests/ -q` |
| `tests/contract/` | Specification contracts (SDD) | `python -m pytest tests/contract/ -q` |
| `tests/test_bdd_*.py` | Behaviour scenarios (BDD) | `bash scripts/test_bdd.sh --all` |
| `tests/run_mutation_*.py` | Mutation probes | `python scripts/mutation_gate.py --all` |

Markers registered in `pyproject.toml`: `unit`, `integration`, `bdd`,
`contract`, `mutation`, `sdd`, `tdd`, `slow`.

## SDD

Specifications live as contract tests before implementation. Example:
`tests/contract/test_suite_homologation.py` pins suite naming, markers,
deploy gate, mutation runners, and documentation. `tests/test_boyscout_contracts.py`
and `tests/test_contract_manifest.py` pin product surfaces.

Workflow:

1. Write the contract test that describes the required behaviour.
2. Run it and confirm it fails for the right reason.
3. Implement the smallest change that satisfies the contract.
4. Keep the contract green afterwards.

## TDD

Every fix ships with a regression test. Baseline first: record `pytest`
result before edits. Pre-existing failures stay pre-existing; new failures
block the change. No `skip` or `xfail` without an issue link.

Fast gate:

```bash
python -m pytest tests/ -q
```

Scoped run while working:

```bash
python -m pytest tests/test_<area>.py -q
```

## BDD

Behaviour scenarios state Given, When, Then in the test docstring. The
`scripts/test_bdd.sh` gate discovers modules mentioning BDD.

```bash
bash scripts/test_bdd.sh --list
bash scripts/test_bdd.sh --all
```

Conventions:

- One scenario per test function.
- Docstring starts with the feature area, then Given, When, Then lines.
- Assert on observable behaviour and `sessions/` artefacts, never on logs.

## Mutation

A surviving mutant means the tests are too weak. Each curated runner in
`tests/run_mutation_*.py` introduces targeted faults and requires the
suite to fail. The consolidated gate runs them uniformly:

```bash
python scripts/mutation_gate.py --list
python scripts/mutation_gate.py --all
```

`mutmut.cfg` scopes stochastic mutation to hardening primitives:

```ini
[mutmut]
paths_to_mutate = core/hardening.py
tests_dir = tests/test_security_hardening_v3.py
runner = python -m pytest tests/test_security_hardening_v3.py -x -q --no-header
```

Threshold: 0 survived mutants on the scoped run. Any survivor opens a
follow-up task to strengthen the contract tests before release.

## Deploy gate

`deploynator.toml` defines the release gate:

```toml
[tests]
commands = ["python -m pytest tests/ -q"]
timeout_s = 3600
```

Timeout is 3600 seconds so large repositories finish without retry loops.
`python -m deploynator release --type test --project ~/LazyOwn --dry-run`
validates the gate before a real release.
