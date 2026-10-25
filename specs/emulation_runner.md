# Emulation Runner Specification

I define the single path from a MITRE technique or APT playbook to an
executed Atomic test.

## Contract

`modules/emulation_runner.py`:

- `EmulationRunner.run(target, techniques, playbook, platform, lhost,
  per_technique, include_manual, dry_run, executor, exploits_dir,
  scan_dir)` resolves tests, opens one shell primitive when needed,
  executes, normalizes and stages
  `sessions/atomic_emulate_<target>_<ts>.json`.
- `run_steps(steps, target, executor, platform, dry_run, source)` runs
  already-resolved commands for derived playbooks.
- `techniques_for_playbook(playbook)` expands phases in order and
  deduplicates technique IDs.

Each result carries `status` (`executed`, `dry-run`, `skipped`,
`error`), `output`, `shell_output`, `duration_ms` and the command. The
legacy bridge report shape is preserved.

## Safety

- Manual Atomic tests are skipped unless `include_manual=True`.
- `dry_run` resolves and stages without execution.
- One shell primitive per run, closed in `finally`.
- Every result publishes through the outcome bus.
- Missing exploit binaries return a skip from the bridge.

## Migrated callers

- `atomic_exploit_bridge.emulate`
- `playbook_engine.PlaybookEngine.execute` through `run_steps`
- `AutonomousExploitEngine` YAML-first command source and `run_spec`
- `do_atomic_emulate` (`--manual`, `--dry-run`)

## Acceptance

- Playbook and technique resolution agree.
- Manual tests never run without opt-in.
- Dry-run never calls the executor.
- Errors are normalized, not raised.
- Tests: `tests/test_emulation_runner.py`.
- Mutation: `tests/run_mutation_emulation_runner.py`.
