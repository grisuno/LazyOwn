# LazyOwn autonomous loop — figure

An Anatomy figure that explains how LazyOwn's autonomous loop runs, drawn as a
bench-top rotary indexing machine.

- `model.mjs` — the pure model of one run: phases, round stages, guard
  verdicts, budget, coverage, verdict. Every number on the page comes from it.
- `build.mjs` — the geometry and the page. Writes `autonomous-loop.html` and
  `autonomous-loop-light.html`.
- `shots/` — verification captures (desktop, phone, light, close-ups, line check).

## Build

```bash
node build.mjs           # dark page
node build.mjs --light   # light page
```

The kit comes from the Anatomy skill:

```bash
export ANATOMY_SKILL=~/.config/opencode/skills/anatomy
```

## Verify

```bash
node "$ANATOMY_SKILL/scripts/lines.mjs" autonomous-loop-light.html --out shots/lines-light.png
node "$ANATOMY_SKILL/scripts/lines.mjs" autonomous-loop.html --out shots/lines-dark.png
node "$ANATOMY_SKILL/scripts/capture.mjs" autonomous-loop-light.html --out shots/light.png --width 1440 --scale 2
node audit.mjs
```

Both pages report `line ends: 0`. `audit.mjs` records the real shape of every
part of the machine (base, table, heads, arms, rams) and runs the kit's
ray-cast depth solver over it: `items 75 · overlapping pairs 107 · depth
problems 0`.

## The mapping

| The machine | The loop |
|---|---|
| The block clamped on the turntable | the engagement (target host `10.10.11.5`) |
| One turn of the table | one round of the orchestrator |
| The eight heads around the ring | the eight stages of a round: scope, enrich, trigger, plan, claim, work, record, settle |
| The head over the block | the stage that acts on the target this round |
| The guard switch (allow / ask / deny) | `Guard.check()` on every tool call |
| The dial | asset coverage: tested / total assets in the task scope |
| The pointer on the drum | the kill-chain phase (`modules/killchain.py`) |
| The level in the sight glass | the tool-call budget, 200 calls |
| The cards in the rack | the planner's intents; a worker claims one at a time |
| The groove on the base plate | the target address, engraved once |

## The truth behind the numbers

Every value the figure shows is read from LazyOwn itself.

| Value | Where it comes from |
|---|---|
| 8 phases `recon → report` | `KillChainConfig.phases`, `modules/killchain.py` |
| round stage order | `LazyLoopEngine.run_round` docstring, `modules/lazy_loop.py` |
| ≤ 4 intents per round | `MAX_INTENTS_PER_ROUND` |
| 2 workers (3 engine default) | `DEFAULT_WORKERS`; MCP `workers` clamps 1–5 |
| ≤ 6 steps per intent | `MAX_WORKER_STEPS` |
| 200 tool calls | `DEFAULT_MAX_TOOLCALLS` |
| 50 findings | `DEFAULT_MAX_FINDINGS` |
| 10 rounds | `DEFAULT_MAX_ROUNDS`; MCP `max_steps` clamps 1–20, default 5 |
| allow / ask / deny | `Guard.check`, `modules/lazy_loop.py` |
| coverage % | `AssetGraph.coverage_for` |
| achieved / partial / failed | `LazyLoopEngine._evaluate_goal` |

## Sources in this repository

- `modules/lazy_loop.py` — the loop: planner, frontier, workers, guard, budget, verdict.
- `modules/lazy_engine.py` — `LazyEngine`, the single orchestrator behind `auto_loop`.
- `modules/killchain.py` — the canonical phases and `advance_phase`.
- `modules/world_model.py` — host states and the derived engagement phase.
- `skills/lazyown_mcp.py` — the `lazyown_auto_loop` MCP tool and the legacy
  selector cascade (reactive → parquet → bridge → LLM → static map).
- `skills/lazyown/SKILL.md` — how an agent drives it from the outside.
