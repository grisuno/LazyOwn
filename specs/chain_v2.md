# Chain v2 Specification

I define the YAML contract for orchestration chains. Version 2 keeps
every version 1 file valid and adds conditions, policy and capture.

## Schema

File: `chains/<name>.yaml`

- `name`: `^[a-z][a-z0-9_]{0,63}$`, equal to the filename.
- `version`: `1` or `2`; omitted means `1`.
- `description`, `enabled`, `extends`, `defaults`, `vars`, `tags`,
  `platforms`.
- `steps`: non-empty unless the chain inherits from `extends`.

Step fields:

- `id`: optional stable identifier, unique per chain.
- `run`: required non-empty command or LazyOwn verb.
- `phase`, `description`: operator metadata.
- `when`: safe expression over `defaults`, `vars`, tokens and captured
  names. Allowed: names, constants, `and`, `or`, `not`, `==`, `!=`,
  `in`, `not in`. Calls and attribute access are rejected.
- `skip_if_exists`: path, tokens allowed.
- `resolve_newest`: `{glob, as}` binds the newest match as an absolute
  path.
- `timeout`: seconds, `0` uses the runner default.
- `retries`: `0-5`.
- `continue_on_error`: boolean.
- `capture`: stores stripped output up to 2000 chars for later steps.
- `expect`: step fails when the text is missing from output.
- `artifacts`, `sinks`: lists carried in the result.

## Execution

`modules/chain_registry.py` validates and resolves.
`modules/chain_runner.py` executes.

- A command whose first token is a live cmd2 verb or alias runs through
  the shell on the calling thread. This is required for interactive
  verbs such as `atomic_shell --interactive`.
- Any other command runs through `core.safe_exec.safe_run_shell` with a
  timeout. A non-zero exit fails the step.
- `retries` re-runs only failed steps.
- A failed step aborts the chain unless `continue_on_error` is true.
- `capture` updates the variable map before the next step.
- `resolve_newest` updates the variable map before rendering.
- `apt_chain <chain> <target> --dry-run` resolves and skips execution.

## Acceptance

- Version 1 chains load unchanged.
- Invalid ids, timeouts, retries, captures, duplicate step ids and
  unknown parent chains are rejected with named errors.
- Raw output is visible to the operator; cmd2 boolean returns never leak
  as text.
- The interactive shell step runs on the main thread.
- Tests: `tests/test_chain_runner.py`, `tests/test_chain_registry.py`,
  `tests/test_apt_chain_integration.py`.
- Mutation: `tests/run_mutation_chain_v2.py` kills every mutant.
