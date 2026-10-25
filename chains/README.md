# chains/

One YAML per orchestration chain — the same philosophy as `lazyaddons/`
(one file per tool) and `exploits/` (one file per exploit). A chain is
an ordered step list the loop and operators run with a single command
(`apt_chain apt_rocke 172.17.0.2`). `chain list [filter]` prints every
chain with state, resolved steps and playbook. Editing the chain means
editing the file, never Python: reorder, skip, or add steps declaratively.

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
version: 2                   # 1 or 2; omitted means 1
description: What the chain does.
tags: [apt, linux]           # operator filters
platforms: [linux]           # victim platforms
defaults:                    # token defaults; CLI args override
  playbook: rocke
vars:                        # chain-local variables
  sleep: "2"
steps:                       # executed in order through the runner
  - id: scope                # stable id for audit and capture
    phase: recon
    description: Bind the target.
    run: assign target {target}
  - id: scan
    phase: recon
    run: lazynmap {target}
    skip_if_exists: sessions/scan_{target}.nmap.xml
    timeout: 900
    retries: 0
  - id: sweep
    phase: exploit
    run: atomic_exploit
    when: playbook != ""     # safe expression over names
    continue_on_error: false
    capture: sweep_output
    expect: "SHELL"
    artifacts: [sessions/atomic_exploit_{target}_*.json]
    sinks: [world_model, intel_graph, c2_surfaces]
  - id: plan
    phase: exploit
    run: attack_plan {plan_file}
    resolve_newest:
      glob: playbooks/attack_plan_*.yaml
      as: plan_file
  - id: loot_grab
    phase: post_exploitation
    run: c2_loot {target} /etc/shadow
    evidence: [sessions/loot_{target}_shadow.txt]
    evidence_sha256:
      sessions/loot_{target}_shadow.txt: "<64-hex digest pin>"
    required_fields: [user, hash]
    benign_alternatives: ["backup script ran first"]
    budget: {attempts: 2, seconds: 120}
  - id: confirm_chain
    phase: post_exploitation
    run: create_session_json
    depends_on: [loot_grab]
```

Tokens: `{playbook}`, `{target}`, plus any token an earlier `capture`
or `resolve_newest` step defines. `when` accepts names, strings,
`and`, `or`, `not`, `==`, `!=`, `in`, `not in`; it never evaluates
Python calls or attributes. `skip_if_exists` (tokens allowed) skips the
step when the file already exists. `timeout` is seconds (0 uses the
runner default), `retries` is 0-5, and `continue_on_error` keeps the
chain moving after a failure. `capture` stores stripped output (up to
2000 chars) for later steps. `expect` fails the step when the text is
missing. `artifacts` and `sinks` travel in the result for reporting and
the outcome bus.

Chain-of-evidence fields (schema v2): `evidence` lists artefact files
that must exist after the step succeeds; `evidence_sha256` pins a file
to a 64-hex digest (re-run integrity); `required_fields` verifies the
fields exist with a present scalar in the captured JSON events
(JSONL or array) or in the step's first JSON object; `benign_alternatives`
annotates benign explanations reviewed before escalation;
`budget` caps total `attempts` (0-6, including retries) and `seconds`
(wall clock, also caps `timeout`). Steps declaring any of these get an
evidence verdict in the result: `evidence_observed` (success with every
required field present), `insufficient_data` (success but fields
missing) or `not_observed` (failure). `depends_on: [id]` skips a step
while a predecessor verdict is not `evidence_observed`, marking the
attack chain unproven; without hunting fields every step behaves as
before.

Steps run through `modules/chain_runner.py`. A first token that matches
a live shell verb (for example `assign`, `lazynmap`, `lazy_sync`) goes
through cmd2; any other command, including
`python3 modules/atomic_exploit_bridge.py ...`, runs through the shared
safe subprocess primitive so output can be captured for `expect` and
`capture`. cmd2 verbs stay on the calling thread, which is required for
interactive verbs such as `atomic_shell --interactive`; raw commands run
with a timeout and a non-zero exit aborts the step. The loop can still
inject its own executor.
Use `apt_chain <chain> <target> --dry-run` to validate resolution and
conditions without executing anything.

- `extends: <parent>` inherits the parent's steps; own `steps` replace
  them wholesale when present, `defaults`, `vars`, `tags` and
  `platforms` merge over the parent's. Cycles and unknown parents fail
  validation and never load.
- `enabled: false` unregisters the file without deleting it; the
  orchestrator Chains tab flips this flag, and `scan_all` still lists
  disabled files so they can be re-enabled.

Steps that execute against a target (`atomic_exploit`, `c2_deploy`,
`c2_loot`, `atomic_emulate`) are lab and in-scope only.
