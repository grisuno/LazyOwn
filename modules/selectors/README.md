# modules/selectors

The shared action-selection brain for the unified autonomous loop. Both
autonomous runtimes (the `LazyLoopEngine` planner in `modules/lazy_loop.py` and
the `autonomous_daemon` in `skills/autonomous_daemon.py`) consult this one
cascade instead of carrying private "pick the next action" logic.

## Files

| File | Contract |
|------|----------|
| `base.py` | The shared vocabulary: `SelectionContext` (live engagement snapshot), `ActionDecision` (one proposed command), and the `Selector` protocol every strategy implements. Pure, no framework imports. |
| `playbook.py` | `PlaybookSelector` - runs an APT actor emulation (`apt_chain apt_<actor>`) when the objective names an actor from `playbooks/`. |
| `adversary.py` | `AdversarySelector` - runs a custom adversary profile (`adversary_yaml <name>`) when the objective names one from `lazyadversaries/`. |
| `atomic.py` | `AtomicSelector` - emulates named MITRE ATT&CK techniques with Atomic Red Team tests (`atomic_emulate --techniques`); both share one execution path. |
| `chain.py` | `ChainSelector` - proposes `apt_chain <name> <target>` via the shared matcher in `modules/chain_match.py`. |
| `registry.py` | `default_selectors()` builds the ordered cascade; `propose_next(ctx)` returns the first concrete decision. |
| `__init__.py` | Package exports. |

`SelectionContext.exclude` is the set of already-taken command strings;
`SelectionContext.extra` carries open inputs such as `{"goal": ...}` or
`{"techniques": [...]}` without widening the shared contract.

## How it works

A runtime builds a `SelectionContext` from what it knows (target, phase,
os_hint, discovered services, creds, already-taken actions) and calls
`registry.propose_next(ctx)`. The cascade tries each `Selector` in order and
returns the first non-`None` `ActionDecision`; a selector returns `None` to
abstain so the next one is tried. Order expresses priority.

## Adding a selector

1. Create `modules/selectors/<name>.py` with one class whose `name` attribute
   is unique and whose `propose(self, ctx) -> ActionDecision | None` honours
   the `Selector` protocol. Keep it single-responsibility and side-effect free
   beyond its own bookkeeping.
2. Add it to `default_selectors()` in `registry.py` at the right priority.
3. Export it from `__init__.py`.
4. Add a test under `tests/` that drives `propose` directly.
