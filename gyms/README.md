# gyms

One YAML file per Red Team Gym challenge. `lazy_orchestrator` exposes the
same catalogue in its **Gyms** tab and edits these files in place.

## Schema

```yaml
id: first_blood_web          # lowercase slug, must match the file name
name: First Blood - Web
description: What the operator must do.
scenario: wordpress           # lab scenario or range profile
chain: ""                     # optional APT chain run by the gym
objective: Operator-facing goal.
difficulty: easy              # easy | medium | hard
phases: [enum, exploit]       # kill-chain phases covered
required_techniques: []
bonus_techniques: []
max_points: 1000
speed_bonus_max: 300
stealth_bonus_max: 200
technique_diversity_bonus: 200
hints: []
success_check: Free-form success criterion.
elo_bonus: 150
```

## Runtime state

Definitions are static. Active runs are persisted in
`sessions/world_model.json` under the `gyms` section, so `gym status` and
`gym stop` work across sessions. Run identifiers are stable (`gym0001`).

## Safety

- Ids are slugs; the registry never accepts arbitrary paths.
- YAML is size-capped and validated before writing.
- A definition with active runs cannot be deleted until the runs stop.

## Commands

```text
gym list
gym start <id> [--target <ip>]
gym status [run_id]
gym stop [run_id|gym-id|name]
gym submit [run_id] [--failed] [--techniques t1,t2]
gym leaderboard|top [n]
```

A shell opened with `atomic_shell` is an engagement action, not a gym
run. `gym status` reports live shells and compromised hosts as context
but requires an explicit `gym start` to track and score a challenge.
