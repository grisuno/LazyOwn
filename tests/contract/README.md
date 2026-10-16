# tests/contract

SDD specification contracts for the LazyOwn test suite. These tests pin
suite-level homologation rules so the full `tests/` directory behaves as
one production suite instead of loose scripts.

| File | Role |
|------|------|
| `test_suite_homologation.py` | Suite contract: naming, markers, mutation runners, deploy gate |

## How it works

Homologation tests run with the normal gate (`python -m pytest tests/ -q`).
They inspect the repository layout (file names, `pyproject.toml` markers,
`deploynator.toml`, mutation runners) and fail when a rule is violated.
No network, no sessions state, no C2 mocking.

## Adding a contract

1. Name the file `test_<surface>.py`.
2. Add one class per specification, one method per behaviour.
3. Register any new pytest marker in `pyproject.toml` under
   `[tool.pytest.ini_options] markers`.
4. Assert on return values and repository state, never on log output.
