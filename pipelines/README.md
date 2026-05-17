# pipelines/

Declarative composition layer. Each `*.yaml` file in this directory is an
ordered, named sequence of LazyOwn commands. Pipelines are loaded and
executed by `modules/pipeline_engine.py` (Pillar 3 of the framework
roadmap) and exposed through three entry points:

- CLI shell: `pipeline run <name>`, `pipeline list`, `pipeline validate <name>`
- MCP: `lazyown_pipeline_run`, `lazyown_pipeline_list`, `lazyown_pipeline_validate`, `lazyown_pipeline_status`
- Daemon subcommand: `python3 skills/autonomous_daemon.py pipeline run <name>`

Every run is persisted under `sessions/pipelines/<pipeline-name>__<run-id>/`
with the frozen plan, one JSON file per executed step, and a `summary.json`
describing the overall outcome.

## Files

| File                          | Purpose                                                                    |
|-------------------------------|----------------------------------------------------------------------------|
| `README.md`                   | This file — schema reference and authoring guide.                          |
| `linux-initial-access.yaml`   | Canonical Linux kill-chain (ping → nmap → searchsploit → conditional pwn). |
| `recon-quick.yaml`            | Fast recon loop reused as a nested step in larger pipelines.               |
| `post-exploit-loop.yaml`      | Demonstrates nested-pipeline composition and conditional branches.         |

## Schema

```yaml
name: <string>                 # display name; defaults to the file stem
description: <multi-line>      # optional human description
target: <string>               # optional override; defaults to payload.json rhost

steps:
  - name: <string>             # optional; defaults to command/pipeline name
    command: <string>          # LazyOwn shell command (mutually exclusive with pipeline)
    pipeline: <string>         # nested pipeline name (mutually exclusive with command)
    args: <string>             # appended after the command name
    input_from: <template>     # resolved template replaces args when truthy
    validate: <predicate>      # output check; see "Validate predicates"
    condition: <template>      # falsy template skips the step
    on_success: <command>      # extra command executed only when this step succeeded
    on_failure: stop|continue|skip   # default stop
    timeout_s: <integer>       # per-step timeout (default 120)
    with_inputs:               # arbitrary key/values accessible via inputs.<key>
      key: value
```

Either `command` or `pipeline` is required; specifying both is a schema error.

## Template scopes

Templates use the form `{{ scope.path.to.value }}`. The resolver is a
strict dotted-path lookup; there is no expression language, no Python
evaluation, and unknown paths render to the empty string.

| Scope        | Meaning                                                                                 |
|--------------|-----------------------------------------------------------------------------------------|
| `previous.X` | Field `X` from the most recent non-skipped step result.                                 |
| `steps.<name>.X` | Field `X` from the step named `<name>`.                                             |
| `payload.X`  | Value of `X` in `payload.json`, read at template-resolution time.                       |
| `inputs.X`   | Value of `X` from the current step's `with_inputs` mapping.                             |
| `findings.X` | Aggregated derived value across the run (latest write wins).                            |
| `pipeline.name`, `pipeline.target` | Current pipeline metadata.                                        |

Each step result exposes: `command`, `args`, `output`, `success`,
`skipped`, `started`, `finished`, plus every key from the per-command
deriver (for example `previous.has_exploit`, `previous.ttl`,
`previous.findings.services`).

## Validate predicates

| Form           | Meaning                                              |
|----------------|------------------------------------------------------|
| `ttl=64`       | Output must contain the literal substring `ttl=64`.  |
| `re:^foo`      | Output must match the Python regex after `re:`.      |
| `empty`        | Trimmed output must be empty.                        |
| `non_empty`    | Trimmed output must be non-empty.                    |

Validation failure marks the step as failed even if the underlying
command exited cleanly; `on_failure` then decides whether the pipeline
stops, continues, or marks the step skipped.

## Per-command derivers

Derivers turn raw command output into structured fields surfaced under
the step's namespace.

| Command        | Derived keys                                                                                  |
|----------------|-----------------------------------------------------------------------------------------------|
| `ping`         | `ttl`, `alive`, `findings.ttl`, `findings.alive`                                              |
| `lazynmap`, `rustscan`, `masscan`, `nmap` | `has_open_ports`, `open_ports_count`, `findings.ports`, `findings.services` |
| `searchsploit` | `has_exploit`, `findings.exploits_present`                                                    |
| `auto_populate`| `discovered_domain`, `findings.populated`                                                     |
| `facts_show`   | `has_facts`, `findings.facts_present`                                                         |

Add a new deriver by importing `StepDerivers` from
`modules.pipeline_engine` and calling `StepDerivers.register(command,
fn)` where `fn(output: str) -> dict`.

## Adding a pipeline

1. Create `pipelines/<name>.yaml` with a top-level `steps:` list.
2. Run `pipeline validate <name>` to confirm the schema parses cleanly.
3. Run `pipeline run <name>` (or run via MCP `lazyown_pipeline_run`).
4. Inspect artefacts under `sessions/pipelines/<name>__<run-id>/`.

Nested pipelines compose: any step may set `pipeline: <other-name>`
instead of `command:`. The engine detects cycles and refuses to execute
a pipeline already present in the nesting stack, and caps nesting depth
at 4 to keep runs observable.

## Security

- YAML is parsed with `yaml.safe_load` only — no arbitrary object
  instantiation.
- Pipeline names are validated against `^[A-Za-z0-9._-]{1,80}$`, and
  resolved paths must stay inside this directory.
- Templates never execute code; the resolver only walks the typed
  context object.
- Artefact paths are constructed via `Path.resolve` with a containment
  check so the run directory cannot escape `sessions/pipelines/`.

## Live narration

Every step start, success, failure, skip and pipeline-level boundary is
broadcast through the same fabric used by `engage`: a line in
`sessions/engagement.log`, a JSON record in
`sessions/autonomous_events.jsonl`, and a `collab_bp` event so teammates
connected to `/collab/` see the pipeline progress in real time.
