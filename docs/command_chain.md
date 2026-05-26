# Command Chain

The command chain answers the two questions that drive every operator (and
the autonomous AI loop) once a session is past the first scan:

- **`prev <command>`** — what should have run before this verb makes sense.
- **`next <command>`** — what to run after it, ranked by signal.

Both views share the same registry, defined in `cli/command_chain.py`, and
are exposed identically through the CLI, the MCP server, and any future
TUI widget — single source of truth.

## CLI

```
prev lazynmap                    # → ping
next lazynmap                    # ordered list with provenance
next                             # uses the most recent command from history
next gobuster 3                  # cap recommendations at 3
```

The CLI commands live in `lazyown.py` (`do_prev` / `do_next`, miscellaneous
category) and delegate every decision to `CommandChain`. They never
duplicate logic from `suggest_next`, `recommend_next` or `explore`;
instead, they expose the chain primitive that those commands already lean
on indirectly through `cli/exploration.py`.

## MCP

The same primitive is published as two MCP tools so the AI loop sees
exactly what the operator sees:

| MCP tool | Returns |
|---|---|
| `lazyown_command_prev(command)` | `{"command": ..., "prev": [verbs]}` |
| `lazyown_command_next(command, target?, phase?, limit?)` | `{"command":..., "next": [{name, source, reason}, ...]}` |

`source` is one of `static`, `service`, `addon`, `tool`, `phase` so the AI
can reason about provenance instead of treating every recommendation the
same way.

## How `next` is built

The dynamic resolver layers four signals in order, dropping anything
already in the session history:

1. **Static kill-chain map** (`cli/reactive_hints._KILL_CHAIN_NEXT`).
   Reused, not copied — single source.
2. **Service follow-ups.** The verb-to-service table in
   `cli.command_chain._DEFAULT_SERVICE_FOLLOWUPS` is consulted with the
   nmap services discovered for the current target. `http` → web fuzzers,
   `smb` → `enum4linux`/`crackmapexec`/`smbclient`, etc.
3. **Unexplored addons** triggered by the scan (`ExplorationEngine.unexplored_addons`).
4. **Unexplored tools** triggered by the scan (`ExplorationEngine.unexplored_tools`).
5. **Phase priority fallback** when none of the above produced anything,
   so the operator always sees *something* sensible.

## How `prev` is built

`prev` is a static map (`_DEFAULT_PREREQUISITES`). Extending it is one
line: add `"<verb>": ("required_prev_verb", ...)`. There is no inference;
deliberate prerequisites are clearer than guessed ones.

`CommandChain.missing_prerequisites(verb, history)` returns the
prerequisites the operator has **not** yet executed, so a wrapper command
or guardrail can prompt before running the verb.

## Adding new entries

| Goal | Where |
|---|---|
| New prerequisite for an existing verb | `_DEFAULT_PREREQUISITES` in `cli/command_chain.py` |
| New service → follow-up mapping | `_DEFAULT_SERVICE_FOLLOWUPS` in `cli/command_chain.py` |
| New verb → static next-hop | `_KILL_CHAIN_NEXT` in `cli/reactive_hints.py` |
| New addon/tool trigger | the addon/tool YAML/JSON file's `trigger` field |

Each change must come with a test in `tests/test_command_chain.py` and,
when a new public surface is introduced, an MCP tool plus a docstring on
the CLI verb. Per `CLAUDE.md` §10.14, tests trend to 100% — the chain
module ships fully covered.

## Design notes

- `ChainConfig` is the only place magic values live (default limit,
  prerequisite map, service-followup table). All other classes accept it
  by construction (dependency injection).
- `PrerequisiteRegistry`, `StaticNextRegistry`, `ServiceNextResolver`,
  `DynamicNextResolver`, and `CommandChain` each have one reason to
  change. SOLID is enforced by review.
- Zero coupling to `cmd2`, `flask`, or `rich`. The module returns plain
  Python types so the CLI, MCP, and tests can consume it without
  mocking.
- The resolver tolerates a missing nmap scan or `sessions/` directory by
  falling back to the static map and, ultimately, the phase priority
  list — so it works on day one of a campaign too.
