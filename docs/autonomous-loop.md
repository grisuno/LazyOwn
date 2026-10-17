# Autonomous Loop

The LazyOwn autonomous loop is the orchestrator behind `auto_loop` and
`lazy_loop`: one command drives a full engagement round by round, with
every step persisted, auditable and reversible. It is a LazyOwn-native
reimplementation: no external branding, no hidden state.

## Quick start

```bash
auto_loop --target 10.10.10.5 --rounds 6 --workers 2 "gain initial access"
lazy_loop --task t0001 --view          # resume a task in the live worker monitor
lazy_view t0001                        # attach the monitor from another terminal
lazy_orchestrator                      # admin console for the loop core
```

`Ctrl+C` cancels in place: running children are killed, shell sessions
are closed, the task is paused and everything is resumable with
`lazy_loop --task T`. `qa`, `exit`, EOF/Ctrl+D and `atexit` run the same
teardown.

## Pipeline stages

Each round invokes the same ordered chain; every stage has an explicit
firing condition and can be enabled or disabled at runtime from the
`lazy_orchestrator` Pipeline tab (persisted under `payload.json` ->
`orchestrator.stages`):

| Stage | Fires when |
|-------|------------|
| `enrich` | every round: first untested scoped assets, 300s cooldown per asset |
| `scheduler` | every round: interval, service, task_create and timeout triggers |
| `planner` | every round unless paused, expired or over budget |
| `workers` | every round while open intents exist (up to `--workers`) |
| `traffic_ingest` | every round while the recorder proxy is on |
| `retest` | every round, up to 3 pending findings |
| `reporter` | every round when a background report draft is ready |
| `compact` | every planner round; threshold and cooldown gated |
| `intel_sync` | throttled every 15s; forced on terminal status |
| `wrapup` | on exhausted or timeout status |
| `archive` | on terminal status |
| `report` | on terminal status when findings exist |
| `notify` | on finding creation and terminal status |
| `ai_bus` | every activity line except raw stream kinds: publishes to the unified event bus and Hive Mind |
| `detection_oracle` | before every executed command: oracle probability written into the traffic log |
| `rl_feedback` | after each LLM reply, each executed command and at terminal: MoE/RL outcome learning |
| `swan_ensemble` | planner step when enabled and SWAN experts are available (off by default) |
| `llm_stream` | every pool and agent LLM call: model deltas appear as throttled `[stream]` activity lines |

## Auto verbs registry

The loop can propose and execute the `auto_*` family (`auto_pwn`,
`autopivot`, `automsf`, `autoblody`, `auto_populate`, `pyautomate`,
`exfil_auto`) plus any operator-defined verb. Manage them from the
`lazy_orchestrator` Verbs tab: `space` toggles, `a` adds a custom verb,
`d` deletes a custom verb or disables a built-in one. Overrides live in
`payload.json` -> `orchestrator.auto_verbs`.

A custom verb is any shell command; declare its keywords so the planner
can propose `auto <verb> <target>` when the goal or findings match. The
Verbs tab opens a searchable picker over every auto verb and every shell
command, so the verb name is selected instead of typed:

```
lazy_orchestrator        # Verbs tab -> a -> search command/verb -> configure keywords
```

## Playbooks tab

`lazy_orchestrator` owns the YAML playbooks under `playbooks/`:

- the table lists every `*.yaml`/`*.yml` file with its shape (`apt` or
  `plan`), step count, phases and validation state;
- the detail pane previews the YAML;
- `a` creates a new APT playbook from a template, `e` edits the raw YAML
  in-place with validation before saving, `d` deletes after confirmation;
- `r` reloads the table after editing files outside the TUI.

All writes are validated and atomic; the table never hides an invalid
file, it flags it instead.

Execution binds the payload `rhost` to the intent target for the
duration of the verb (under a lock), restores it afterwards, and runs
loop-side children with stdin detached so sudo prompts can never hijack
the terminal.

## Loop guardrails

The worker normalizes every model-proposed command before execution:

- absolute paths to shell verbs are reduced to the verb
  (`/usr/bin/lazynmap` -> `lazynmap`);
- invalid nmap port slots are repaired (`nmap -sV -p <target>` ->
  `nmap -sV <target>`) and a missing target is restored;
- duplicate steps for the same intent are dropped.

Kill-chain phase changes advance only the host that produced the
outcome (`advance_phase(..., host=...)`); unrelated or stale world-model
hosts are never marked `exploited`/`owned` by a global phase change.

Open ports from a scan are assets, not findings. The retester never
replays long-running scanners (`nmap`, `masscan`, `gobuster`, `ffuf`,
`nikto`, `nuclei`, ...): such findings become terminal `inconclusive`
instead of triggering another full scan every round. The stall watchdog
derives its warning/dump thresholds from the configured verb timeout, so
a long but bounded scan is not reported as a dead loop.

## Observability


Every step is narrated live on the terminal and persisted:

- `[kind] worker: text` activity lines: claims, planner wakes, LLM
  calls/replies/retries, guard decisions, steer, jobs, shell sessions,
  findings, intel sync;
- heartbeats every 15s with tools/results/idle counters;
- a stall watchdog: a warning after 45s without activity and a full
  thread-stack dump to stderr at 120s, so a runaway loop is visible and
  killable;
- `lazy_view` for the split-pane monitor and `lazy_orchestrator` for the
  admin console.

## Configuration

`config/orchestrator.yaml` is the default source for profiles, pipeline
stages, numeric limits, budgets, the default chain/playbook and outcome
sink toggles. `payload.json` keeps runtime overrides under
`orchestrator`; an override always wins. The shipped profiles are
`default`, `stealth`, `lab` and `gym`.

```bash
lazy_loop --profile gym --target 172.17.0.2 "root the gym"
auto_loop --profile stealth "map the perimeter"
```

`lazy_orchestrator` exposes the Profiles tab: Enter or Space activates
one profile, and the Config tab keeps editing the payload knobs the
runner reads (heartbeat seconds, verb timeout, agentic flags, NOA
archiving, proxy settings, agent backend). Additional per-run flags:
`--profile`, `--rounds`, `--workers`, `--timeout`, `--step-delay`,
`--no-bootstrap`, `--view`, `--plain`.

Explicit `--rounds` and `--workers` win over the profile. Without them,
the active profile supplies both values.

## Gym administration

The Gyms tab manages the YAML gym catalogue under `gyms/` and the active
runs persisted in the world model. Space starts the selected gym when it
is idle and stops its active runs when it is running; `a`, `e` and `d`
create, edit and delete definitions. Runs keep stable ids (`gym0001`), so
`gym status <run_id>` and `gym stop <run_id>` work from any session.
A shell opened with `atomic_shell` is engagement context, not a gym run;
scoring starts only with `gym start`.

```bash
gym status                 # every active gym with run ids
gym stop                   # stop all active gyms
gym stop gym0001           # stop one run
gym stop first_implant     # stop every run of one gym
```

See [`metasploitable-gym.md`](metasploitable-gym.md) and
[`../specs/gym_registry.md`](../specs/gym_registry.md).

## Artifacts and audit trail


Everything lands under `sessions/lazy/`:

| File | Content |
|------|---------|
| `activity_<task>.jsonl` | every step with worker, kind, text, tool_use_id |
| `traffic_<task>.jsonl` | every command with output, digest and truncation flag |
| `guard_audit_<task>.jsonl` | allow/ask/deny decisions correlated by tool_use_id |
| `intercept_<task>.json` | pending approvals and their decisions |
| `exp_<task>.json`, `assets.json` | exploration and attack graphs |
| `evidence_<task>.json`, `drafts_ready_<task>.json` | evidence vault and reporter drafts |
| `report_<task>.md/json/csv` | findings reports |
| `archive_<task>_<ts>.json` | terminal snapshot for restore |

Each round (throttled) and each terminal status, the loop fuses its
output into the world model, the findings lifecycle, `objectives.jsonl`,
the traffic recorder index and the C2 board via `lazy_bridge.sync_all`,
so logs become information and information becomes intel without manual
steps.

## AI stack integration

The loop is wired to the framework's AI stack through one bridge
(`modules/loop_ai_bridge.py`); nothing is reimplemented:

- every meaningful activity is published to the unified event bus
  (`sessions/events.jsonl`) and stored in Hive Mind episodic memory
  (`ai_bus` stage);
- the detection oracle annotates each executed command with a detection
  probability and Sigma rule names, recorded in the traffic log and the
  activity stream (`detection_oracle` stage);
- the MoE router proposes the preferred expert for the LLM chain and
  the RL trainer learns from outcomes: per-reply for the pool, per-command
  for executed steps, persisted at terminal (`rl_feedback` stage);
- SWAN can produce the planner reply as an ensemble when enabled
  (`swan_ensemble` stage, off by default).

All of these are stage toggles in the `lazy_orchestrator` Pipeline tab,
so an operator can disable any of them without touching code, and an
unavailable dependency degrades to a no-op instead of failing the loop.

### Token streaming

With `llm_stream` on, pool replies and agent turns stream token deltas:
the terminal shows throttled `[stream] model streaming... N chars` lines
while the reply is generated, and agent reasoning models surface their
thinking as one `[agent-think]` activity line. A backend without
streaming support silently falls back to the plain completion path.

### Long-lived workers

Worker identities and their persistent bash sessions survive across
rounds: the engine keeps one `Worker` object per slot, rebinds it to the
fresh graph/log views each round and closes it only when the run ends.
Resume, steering, background jobs and intercept approvals therefore keep
working on the same worker across the whole run.

### Command hygiene

Before a step runs it passes three filters: the sanitizer retargets
foreign hostnames to the intent target (and repairs target-less scans
such as `nmap -p 75`), foreign IP literals stay as-is so the scope
enforcement blocks them, and a task-wide dedupe drops commands already
executed under another intent. Tools that abort because passwordless
sudo is unavailable are marked `[block]` skipped instead of failing the
step, and `lazynmap` itself detects the unattended run (`LAZYOWN_AUTONOMOUS=1`) and exits cleanly instead of trying to prompt, while interactive sessions still get the normal sudo password prompt.

### Evidence package

At terminal status the `archive` stage also freezes a hash-manifested
zip (`sessions/lazy/evidence_<task>.zip`) with the task registry,
exploration graph, activity trace, tool traffic, rendered report and the
proxy traffic archive. `lazy_evidence package <task>` rebuilds it on
demand, `lazy_evidence search <query>` queries captured bodies through
the trigram full-text index (matching mid-token strings such as API
keys and hashes), and `add`/`list`/`verify`/`gc` manage the
per-finding evidence vault.

## Cancellation and teardown

- `Ctrl+C` during a run: children killed by process group, task paused,
  state saved, terminal restored;
- `qa`, `exit`, EOF/Ctrl+D and process `atexit`: `shutdown_loop_runtime`
  kills tracked child processes, closes persistent shell sessions,
  pauses running/queued tasks, stops the recorder proxy and releases
  wake waiters; the same paths encrypt session files protected by
  `cli/auto_crypto.py` when an operator credential exists, and print a
  visible warning when encryption is skipped;
- resume at any time with `lazy_loop --task T` or `lazy_view T`.

## Troubleshooting

- No output after start: check `activity_<task>.jsonl`; the stall
  watchdog will dump thread stacks if the loop is wedged.
- `lazynmap` needs sudo: authenticate once (`sudo -v`) before the run;
  loop-side children run without a tty by design. Interactive commands
  you type yourself are unaffected: the normal shell keeps the operator
  terminal, so sudo prompts work as always.
- Session encryption did not run at exit: it requires the operator login
  or `LAZYOWN_MASTER_PASSWORD`; the reason (no credential, no protected
  files, failure) is printed on exit.
- A stage floods the log: disable it from the Pipeline tab while you
  investigate; re-enable when done.
- Worker suggestions look wrong: inspect `[llm]` activity lines and pin
  skills or hints (`lazy_hint`, `lazy_steer`, `lazy_agent` for the main
  agent).
