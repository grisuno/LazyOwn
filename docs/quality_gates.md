# Quality gates

I keep four mechanical gates in the repository. Each one fails on a real
regression and stays quiet otherwise. Three run in CI through
`.github/workflows/ci.yml` and `read-before-write.yml`; all four run from a
checkout when a change lands.

## Contract manifest

`scripts/check_contract_manifest.py` reads the contract tables in
`docs/SECURITY_CONTRACTS.md`, `docs/killchain_contracts.md`, and
`docs/refactor_contracts.md`, then verifies that every cited module and test
file exists. It also reads the public import examples in `CORE.md` and parses
the target module with `ast` to confirm each public symbol is defined. It never
imports the target, so it has no side effects.

```sh
python3 scripts/check_contract_manifest.py
```

The check is conservative. It ignores globs, brace expansions, placeholders,
URLs, and anything under `sessions/`, `external/`, or `mutants/`. The test
suite lives in `tests/test_contract_manifest.py`.

## Mutation gate

`scripts/mutate.sh` runs the curated mutation runners under `tests/`. Each
runner mutates one production module and asserts that the matching test suite
kills the mutant. A survivor fails the gate because the suite does not cover
the behaviour.

```sh
scripts/mutate.sh                              # scoped to changed source files
scripts/mutate.sh --all                        # every runner
scripts/mutate.sh scripts/journal.py           # runners that cite a file
scripts/mutate.sh --list
```

The scoped mode maps a changed file to the runners that reference it. A file
with no runner is reported so a contract can be added. I added
`tests/run_mutation_contract_manifest.py` when I introduced the manifest
checker.

## BDD gate

`scripts/test_bdd.sh` runs the pytest modules that declare behavior-driven
scenarios in their docstrings. It defaults to the changed test modules and
offers a full run for the end of a work unit.

```sh
scripts/test_bdd.sh                            # changed BDD modules
scripts/test_bdd.sh --all                      # every BDD module
scripts/test_bdd.sh tests/test_journal.py      # explicit files
scripts/test_bdd.sh --list
```

## Read before write

`scripts/journal.py` appends one entry per unit of work to a GitHub Discussion
category. `scripts/read_journal.py` prints the recent entries. The
`read-before-write` workflow fails a pull request whose body does not cite an
existing entry as `Journal: #N`. The point is mechanical: a stateless agent
cannot recover the reasoning from the code alone, so the reasoning has to be
read before the next change is written.

```sh
python3 -m scripts.read_journal
python3 -m scripts.journal post --title "contract manifest gate" --body-file notes.md
```

The scripts detect the repository from the `origin` remote and never open a
shell. The runner is injectable, so `tests/test_journal.py` never touches the
network.

## Exit codes

Every gate returns 0 on success and non-zero on a real failure. CI treats a
non-zero exit as a blocked change. The gates never swallow a failure with
`|| true`.
