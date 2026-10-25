# CI Hardening

## CONTRACT C-002: ci-strict-mode

The CI workflow must fail when the test suite fails or when a lint rule breaks. The current workflow swallows every failure through the `|| true` shim and the `continue-on-error: true` flag. The orchestrator will replace the workflow with a strict version that runs ruff, mypy, bandit, and pytest without any swallow. The strict workflow runs on every push to main and on every pull request targeting main. The strict workflow installs the dev dependencies from requirements-dev.txt. The strict workflow reports the failing step in the GitHub Actions log.

The trigger is any push to main or pull request targeting main. The inputs are the Python source files in lazyown.py, utils.py, the modules directory, the skills directory, the cli directory, and the requirements-dev.txt file. The happy path is the strict workflow runs on a real change and every step reports pass. The sad paths cover a real test failure, a real lint failure, a missing dependency, a Python interpreter not available, a network failure during pip install, a flake, and a syntax error. The data flow is the workflow runs in GitHub Actions on ubuntu-latest with Python 3.11, then on Python 3.12. The observability is the GitHub Actions log. The out of scope is anything beyond CI strictness, including the actual test suite changes, the test selection, and the release flow.

- ruff check the project
- mypy check the project
- bandit check the project
- pytest run the test suite
- strict workflow file
- no swallow flags
