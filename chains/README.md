# chains/

One YAML per orchestration chain — the same philosophy as `lazyaddons/`
(one file per tool) and `exploits/` (one file per exploit). A chain is
an ordered step list the loop and operators run with a single command
(`apt_chain apt_rocke 172.17.0.2`). Editing the chain means editing the
file, never Python: reorder, skip, or add steps declaratively.

Per-APT chains (`apt_rocke.yaml`, `apt_apt29.yaml`, ...) inherit the
base `apt_chain.yaml` through `extends:` and only pin the playbook
default — steps live in one place. Generate a missing one from the
orchestrator Chains tab or:

```bash
python3 -c "from modules.chain_registry import generate_for_playbook; print(generate_for_playbook('apt29'))"
```

Validate after any change:

```bash
python3 -c "from modules.chain_registry import load_all; print(load_all())"
```

## Schema

```yaml
name: apt_chain              # ^[a-z][a-z0-9_]{0,63}$; MUST equal filename
description: What the chain does.
defaults:                    # token defaults; CLI args override
  playbook: rocke
steps:                       # executed in order through the shell
  - run: assign target {target}
  - run: lazynmap {target}
    skip_if_exists: sessions/scan_{target}.nmap.xml
  - run: atomic_exploit
  - run: apt_playbook validate {playbook}
  - run: apt_playbook run {playbook}
  - run: attack_plan {plan_file}
    resolve_newest:          # glob newest match into a token before running
      glob: playbooks/attack_plan_*.yaml
      as: plan_file
```

Tokens: `{playbook}`, `{target}`, plus any token a `resolve_newest`
step defines. `skip_if_exists` (tokens allowed) skips the step when the
file already exists — how expensive steps like full scans stay
idempotent. Steps run through the shell so every entry must be a
routable command (`is_routable_command`); unknown verbs abort the
chain loudly instead of running halfway.

- `extends: <parent>` inherits the parent's steps; own `steps` replace
  them wholesale when present, `defaults` merge over the parent's.
  Cycles and unknown parents fail validation and never load.
- `enabled: false` unregisters the file without deleting it; the
  orchestrator Chains tab flips this flag, and `scan_all` still lists
  disabled files so they can be re-enabled.

Steps that execute against a target (`atomic_exploit`, `c2_deploy`,
`c2_loot`, `atomic_emulate`) are lab and in-scope only.
