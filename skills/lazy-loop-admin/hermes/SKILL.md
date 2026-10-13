---
name: lazy-loop-admin
description: Administer the Lazy autonomous loop: widen, add or remove loop commands, stages, tool lanes, LLM chain and guard rules.
version: 1.0.0
author: LazyOwn RedTeam
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [lazyown, lazy-loop-admin]
    homepage: https://github.com/grisuno/LazyOwn
---

# /lazy-loop-admin

Administer what the Lazy autonomous loop may fire. The loop routes shell
verbs through one Guard and scope path; this skill widens, adds or removes
those verbs plus the pipeline stages around them. Prefer the CLI (scriptable,
non-interactive); use the TUI only for live inspection.

## Quick map

| Layer | CLI | TUI tab | Stored in |
|---|---|---|---|
| Auto verbs (widen/add/remove) | `lazy_verb ...` | Verbs | `payload.json` → `orchestrator.auto_verbs` |
| Pipeline stages (on/off) | `lazy_stage ...` | Pipeline | `payload.json` → `orchestrator.stages` |
| Full CLI routing (815 verbs) | `lazy_verb full-cli [on\|off]` | — | `payload.json` → `orchestrator.full_cli` |
| Tool lanes per agent | `lazy_tool list\|bind\|unbind <agent> <tool>` | — | `sessions/lazy/tool_catalog.json` |
| Custom tools | `lazy_tool custom-add\|custom-list\|custom-rm\|custom-run` | — | custom tools store |
| LLM failover chain | `lazy_llm list\|add\|remove` | Models | sessions LLM pool |
| LLM↔role conformance | `lazy_llm conformance [--role R]` | — | `sessions/lazy/llm_conformance.json` |
| Per-task sandbox | `lazy_sandbox status\|up\|down\|build\|exec` + `lazy_loop --sandbox [image]` | — | container `lazy-loop-<task>` |
| Capability installer | `lazy_install <tool> [--dry-run]\|on\|off\|list` | — | `payload.json` → `orchestrator.installer` |
| Guard intercept rules | `lazy_guard rule-add\|rule-del` | Guard | sessions guard store |
| Live view | `lazy_view [task]` | Now | `sessions/lazy/activity_<task>.jsonl` |

## Widen: full CLI routing

```
lazy_verb full-cli        # show state (default: on, 815 shell verbs visible)
lazy_verb full-cli off    # restrict loop to built-in auto verbs only
lazy_verb full-cli on     # loop may route any do_<verb> command
```

With full CLI on, any real shell verb in an intent resolves and executes
through the same scope gate, Guard check, intercept queue and traffic log
as built-ins. Unknown names never route. Verbs claimed by an auto verb
whose tooling is missing stay skipped (no resurrection by raw name).

## Add a loop command

```
lazy_verb list --phase recon --q gobuster   # find candidates
lazy_verb add gobuster --keywords "web recon,dir enum" --phase recon --desc "web path enum"
lazy_tool bind worker bash                  # ensure the lane can run it
lazy_guard check gobuster 10.0.0.5          # preview the Guard verdict
```

Rules: name must match `^[a-z][a-z0-9_]{0,63}$` and be a real `do_<verb>`
shell command (or ship an addon first); `--no-target` when the verb takes
no target; keywords are comma-separated intent signals.

## Remove / disable a loop command

```
lazy_verb disable automsf    # built-in: disables, keeps definition
lazy_verb remove myscan      # custom: deletes definition
lazy_verb enable automsf      # re-enable
lazy_stage disable compact    # pause a pipeline stage
lazy_stage reset              # drop all overrides, back to defaults
```

`remove` on a built-in disables it instead of deleting (same guard as the
TUI). Disabling a verb also blocks its raw CLI form in `steps_for`.

## What the loop learns on its own (no admin needed)

- Every routing decision + outcome lands in
  `sessions/lazy/routing_decisions.jsonl` (`modules/lazy_intel.py`),
  with secrets masked (pattern redaction + live payload credential
  values, so training rows never persist passwords or keys).
- Each round the Planner runs `refine()` after `plan()`: drops duplicate
  pending intents, settles intents covered by terminal work on the same
  assets, blocks intents hit by new deny constraints, caps pending
  overflow at 12 by lowest priority. Counts surface in the round summary
  (`refined: {dupe, covered, denied, capped}`).
- Each `intel_sync` fuses decisions into `world_model.json` notes (feeds
  the intel graph and the attack graph, both derived views over sessions)
  and refreshes `sessions/lazy/verb_priors.json` success rates, which
  re-rank candidate verbs automatically (cold verbs keep default order).
- At terminal status the sync exports `sessions/lazy/orchestrator_dataset.jsonl`
  instruction-tuning rows for TopoSwarm `--finetune`. Usage writes the
  dataset; nobody hand-crafts it. Same pattern as the detection oracle:
  online per-command Q-learning (`record_step`) plus batch priors here.
- Verb timeouts keep the partial output tail (last 1500 chars ride with
  the TIMEOUT message) so evidence is never discarded.
- At terminal status the engine writes an independent verdict
  (`_evaluate_goal`, reporter idea): achieved/partial/failed from graph
  evidence, never from worker self-reports, plus an LLM one-liner when a
  pool exists. Report at `sessions/lazy/report_<task>.md`.
- `export_spans(<task>)` (`modules/lazy_intel.py`) renders activity as
  trace spans (`spans_<task>.jsonl`): task = trace id, `tool_use_id` =
  span id, intent = parent, tool/result pairs joined with duration.
- `lazy_llm conformance [--role R]` probes every pool member under each
  role prompt (provider-tester idea) and stores fastest-healthy affinity
  per role in `sessions/lazy/llm_conformance.json`.
- Repetition watchdog (execution-monitor idea): 3 identical consecutive
  steps settle the intent (`loop-guard` + `mentor` lines, `exhausted`)
  instead of burning the step budget; a `sage` consult fires
  best-effort when a pool exists.
- Stack-aware priors: routing records carry the service-stack
  fingerprint, so `verb_priors.json` learns per (phase, stack, verb)
  with global fallback — repeat engagements against the same stack
  route better automatically.
- `build_prompt_context` masks operator-configured secrets before any
  LLM call (cloud backends never see payload credentials); discovered
  loot stays visible for cracking/reuse reasoning.

## Per-task sandbox

```
lazy_loop --sandbox --rounds 6 <goal>        # default lazyown-sandbox image
lazy_loop --sandbox myimage --task t0001     # explicit image
lazy_sandbox status --task t0001             # readiness + container state
lazy_sandbox exec --task t0001 lazynmap      # one verb inside the container
lazy_sandbox down --task t0001               # stop + remove when done
lazy_sandbox build                            # build image (minutes, never auto)
```

One container per task (`lazy-loop-<task>`, repo mounted at `/app` like
`./run` sandboxed mode). Verbs pipe into the in-container shell; Guard,
scope, traffic and intel see identical transcripts. Profile: no
privileged, caps dropped except `NET_RAW`, memory/CPU caps, selectable
network. Payload knobs: `sandbox_image`, `sandbox_network`,
`sandbox_memory`, `sandbox_cpus`. Missing image/daemon degrades to a
recorded capability error, never a hang. The image is never auto-built
inside a round.

## Capability installer

```
lazy_install list                 # allowlisted recipes (never free-form)
lazy_install chisel --dry-run     # preview
lazy_install on                   # let the loop resolve install intents
lazy_guard rule-add "apt-get install" ask installs-write-to-host
```

Default off. When on, the Planner turns `capability_gap` facts into
`install capability <tool>` intents (priority 7, skipped when the
binary appears). Resolution requires the allowlist
(`modules/lazy_installer.py`); unknown tools yield nothing. Every
install still crosses Guard + intercept — pair with the ask-rule above
so host mutation stays operator-gated.

## Verify

```bash
python3 -m pytest tests/test_auto_registry.py tests/test_lazy_loop.py tests/test_engage_orchestrator.py tests/test_placeholder_coverage.py -q
python3 -c "from modules.lazy_cli_bridge import cli_verbs; print(len(cli_verbs()))"
```
