# Gym Registry Specification

I define the YAML gym catalogue and its persistent run state.

## Definitions

Every gym is one `gyms/<id>.yaml` file:

```yaml
id: first_blood_web
name: First Blood - Web
description: Operator-facing description.
scenario: wordpress
chain: ""
objective: Extract the users table through manual SQL injection.
difficulty: easy
phases: [enum, exploit]
required_techniques: [sqli_manual]
bonus_techniques: [csrf_bypass]
max_points: 1000
speed_bonus_max: 300
stealth_bonus_max: 200
technique_diversity_bonus: 200
hints: []
success_check: users table dumped
elo_bonus: 150
```

- `id` must match the file stem and the `^[a-z0-9][a-z0-9_-]{0,63}$` slug.
- `difficulty` is `easy`, `medium` or `hard`.
- `phases` must be a non-empty subset of the canonical kill-chain phases.
- Numeric fields are non-negative integers.
- The loader is `modules.gym_registry.load_definitions()`. Invalid files
  are logged and skipped; they never stop the CLI.
- Writes are atomic and validate before replacing the file.

## Run state

Active runs live in `sessions/world_model.json` under the `gyms` section.
`WorldModel.read_section()` and `write_section()` allowlist that key, so a
world-model save never drops gym state.

```json
{
  "version": 1,
  "next_id": 2,
  "active": {
    "gym0001": {
      "run_id": "gym0001",
      "challenge_id": "first_blood_web",
      "name": "First Blood - Web",
      "operator": "grisun0",
      "started_at": 1710000000.0,
      "target": "172.17.0.2",
      "status": "active"
    }
  },
  "legacy_imported": ["active_grisun0.json"]
}
```

- Run ids are stable and human-readable (`gym0001`).
- Starting the same gym twice for the same operator returns the existing
  run instead of creating a duplicate.
- `stop` with no selector stops every active run. With a run id, challenge
  id or display name it stops only the matching runs.
- `submit` removes the selected run; with more than one active run the
  caller must pass a run id.
- Legacy `sessions/gym/active_<operator>.json` files are imported once and
  marked in `legacy_imported`.

## Surfaces

- CLI: `gym list`, `gym start`, `gym status`, `gym stop`, `gym submit`,
  `gym hint`, `gym leaderboard`.
- TUI: `lazy_orchestrator` Gyms tab. Space starts/stops the selected gym,
  `a` creates a definition, `e` edits raw YAML, `d` deletes after
  confirmation.
- Code: `modules.redteam_gym` keeps scoring and leaderboard wrappers;
  `modules.gym_registry` owns definitions and state.

## Security

- Definition paths are slugs confined to `gyms/`; arbitrary paths and
  traversal are rejected by construction, and symlinked files are skipped.
- YAML is loaded with `safe_load`, size-capped at 200 KB.
- No shell or subprocess is used to manage definitions or state.
- A definition with active runs cannot be deleted until the runs stop.
- State writes go through the world-model lock; the registry adds a
  process-level lock around read-modify-write sequences.

## Acceptance

- `tests/test_gym_registry.py` pins YAML CRUD, confinement, start/stop,
  duplicate prevention, submit disambiguation and legacy migration.
- `tests/test_gym_cli.py` pins `gym stop` with no arguments, by id and by
  display name.
- `tests/test_lazy_orchestrator.py` pins the Gyms tab start/stop path.
- `tests/test_infra_disposable.py` pins range next steps.
