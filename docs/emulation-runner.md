# Emulation Runner

I own the path from a MITRE technique or an APT playbook to an executed
Atomic test. The CLI, MCP, APT chains and the loop call this contract
instead of rebuilding the resolve-render-run-normalize loop.

## Contract

`modules/emulation_runner.py` exposes `EmulationRunner`:

- `run(target, techniques=None, playbook="", platform, lhost,
  per_technique, include_manual, dry_run, executor, exploits_dir,
  scan_dir)` resolves techniques, opens one shell primitive when needed,
  executes every test, normalizes results, publishes one outcome per
  test and stages `sessions/atomic_emulate_<target>_<ts>.json`.
- `run_steps(steps, target, executor, platform, dry_run, source)` runs
  already-resolved commands for derived playbooks without opening a
  shell.
- `techniques_for_playbook(playbook)` expands phases in order and
  deduplicates technique IDs.

Results carry `status` (`executed`, `dry-run`, `skipped`, `error`),
`output`, `shell_output`, `duration_ms` and the original command. The
legacy bridge report fields (`target`, `via`, `platform`, `results`,
`executed`, `generated_at`, `staged`) are preserved.

## Safety

- Manual Atomic tests are skipped unless `include_manual=True`.
- `dry_run` resolves and stages commands without execution.
- The shell primitive opens once per run and closes in `finally`.
- No command runs on import; timeouts live in the exploit/bridge layer.
- Every test publishes through the outcome bus, so the world model,
  kill-chain, intel graph, attack graph, C2 surfaces and reports stay
  current.

## Migrated callers

- `modules/atomic_exploit_bridge.emulate` delegates here.
- `modules/playbook_engine.PlaybookEngine.execute` uses `run_steps`.
- `AutonomousExploitEngine` prefers `exploits/*.yaml` commands and
  `run_spec` before its legacy hardcoded map.
- `do_atomic_emulate` accepts `--manual` and `--dry-run`.

## Tests

- `tests/test_emulation_runner.py`: execution, dry-run, manual gating,
  playbook expansion, error normalization, bridge delegation and
  YAML-first command building.
- `tests/run_mutation_emulation_runner.py`: five mutants, all killed.
