# Contract C-002

The CI workflow must fail when the test suite fails or when a lint rule breaks. The current workflow swallows every failure through the `|| true` shim and the `continue-on-error: true` flag. The orchestrator will replace the workflow with a strict version that runs ruff, mypy, bandit, and pytest without any swallow. The strict workflow runs on every push to main and on every pull request targeting main. The strict workflow installs the dev dependencies from requirements-dev.txt. The strict workflow reports the failing step in the GitHub Actions log.

## Spec

ci-strict-mode

## Sad paths covered

- 1. missing input: the agent reports a missing input and exits without writing the spec
- 2. invalid input type: the agent coerces the value or raises a typed error
- 3. external dependency offline: the agent degrades to the template engine
- 4. caller asks to skip validation: the agent refuses and logs a blocker
- 5. concurrent writer: the agent writes to a tmp path and renames atomically
- 6. disk full: the agent raises IOError and the orchestrator stops the cycle

## Review

- approved True; findings 62; blockers 51; pytest exit 0

## Deploy gate

closed until the operator passes the deploy gate token
