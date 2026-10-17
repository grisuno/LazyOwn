# Orchestrator YAML Contract

I define the operator-editable contract for the autonomous loop. YAML is
the default source for profiles, pipeline stages, limits, budgets, chains
and sink toggles. `payload.json` keeps runtime overrides under
`orchestrator`, and an override always wins over YAML.

## Schema

File: `config/orchestrator.yaml`

- `version`: integer schema version. Only version 1 is accepted.
- `default_profile`: profile used when the payload names none.
- `profiles`: mapping of profile name to profile data.
- `profiles.<name>.description`: operator-facing text.
- `profiles.<name>.stages`: mapping of stage name to stage data.
- `profiles.<name>.stages.<stage>.enabled`: boolean.
- `profiles.<name>.stages.<stage>.label`: display label.
- `profiles.<name>.stages.<stage>.fires_when`: firing condition text.
- `profiles.<name>.stages.<stage>.params`: free-form mapping read by the
  engine. Known keys are `limit`, `cooldown_sec`, `interval_sec`.
- `profiles.<name>.limits`: numeric loop limits. Known keys are `rounds`,
  `workers`, `worker_parallel_cap`, `heartbeat_sec`, `wake_debounce_sec`,
  `intel_sync_sec`, `enrich_limit`, `enrich_cooldown_sec`, `retest_limit`,
  `max_intents_per_round`, `max_worker_steps`, `verb_timeout_sec`,
  `step_delay_sec`.
- `profiles.<name>.budget`: numeric budgets. Known keys are `max_rounds`,
  `max_toolcalls`, `max_findings`.
- `profiles.<name>.chain`: default chain name.
- `profiles.<name>.playbook`: default APT playbook key.
- `profiles.<name>.sinks`: boolean fan-out toggles consumed by the
  outcome bus contract.

## Precedence

1. `payload.json -> orchestrator.profile` selects the active profile.
2. `payload.json -> orchestrator.stages.<name>.enabled` overrides one
   stage flag.
3. `config/orchestrator.yaml` supplies every other default.
4. Missing or invalid YAML falls back to the built-in stage table so the
   loop always starts.

## API

- `profiles()` returns the merged profile mapping.
- `active_profile()` returns the selected profile name.
- `set_profile(name)` persists the selection and raises `KeyError` for an
  unknown profile.
- `profile_config(name="")` returns one resolved profile.
- `limits()` returns the resolved numeric limits.
- `stage_params(name)` returns the resolved stage parameters.
- `chain_defaults()` returns the resolved chain and playbook defaults.
- `validate_config(data)` returns human-readable schema errors.

## Acceptance

- The shipped YAML declares `default`, `stealth`, `lab` and `gym`.
- Every stage in the YAML is exposed by `stages()` with label, firing
  condition and parameters.
- Switching the profile changes the engine limits without touching code.
- Unknown stages and unknown profiles never crash the loop.
- The admin console lists profiles and switches the active one.
- Tests: `tests/test_orchestrator_yaml.py`.
- Mutation: `tests/run_mutation_orchestrator_yaml.py` kills every mutant.
