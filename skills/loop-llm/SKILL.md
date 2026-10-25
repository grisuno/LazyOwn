---
name: loop-llm
description: "Add a new LLM leg to LazyOwn loop mode (auto_loop/lazy_loop) in one shot. Knows the pool-member contract, the factory spec-prefix rule, priority/backfill semantics and the validation tests."
trigger: /loop-llm
---

# /loop-llm

Add one LLM leg to loop mode so `auto_loop` / `lazy_loop` fail over through it.
No iteration: follow the contract, wire the leg, update the defaults, run the self-check.

## Usage

```
/loop-llm pi
```

## Step 1 — The contract (read before touching code)

Loop mode asks the pool, never a backend directly:

- `modules/lazy_loop.py` `LlmPool.DEFAULT_MEMBERS` — the 5 legs, each
  `{"name": <unique-id>, "model": "<prefix>:<model-id>", "priority": <int>}`.
  Higher priority tries first; equal priority round-robins via the `rr`
  cursor in `sessions/lazy/llm_pool.json`.
- `LlmPool.complete()` resolves each member's `model` spec through
  `modules.llm_factory.complete(spec, prompt, max_tokens)`.
- `complete()` accepts a `backend:` prefix. Registered factory backends
  (`SUPPORTED_BACKENDS`) plus leg-only prefixes (`toposwarm:`, `pi:`) are
  valid. Leg-only prefixes are the correct choice for agent CLIs and
  routers: they need NO entry in `SUPPORTED_BACKENDS`, NO payload-schema
  key, and NO change to `test_llm_contract.py` (which pins the canonical
  backend tuple).
- Dead legs MUST raise `RuntimeError` (never return `""` on outage):
  the pool catches it, trips the shared health breaker
  (`modules/llm_pool.py`, persisted at `sessions/lazy/llm_health.json`),
  and fails over to the next member. Empty prompt returns `""`
  without calling anything.
- `_seed_defaults()` backfills new `DEFAULT_MEMBERS` by name into
  existing `sessions/lazy/llm_pool.json` files, so operators gain the
  leg without losing their edits. Never rename an existing member.
- Subprocess legs use list-form `argv` with `shell=False` (see
  `core/safe_subprocess.py`). Secrets never travel as placeholders or
  argv; keyless local legs need no credentials at all.

Current legs (`name`, `model`, `priority`):

| name | model | priority | notes |
|------|-------|----------|-------|
| `llamacpp-local` | `llamacpp:local-model` | 10 | raw HTTP to llama.cpp, fastest local |
| `groq-cloud` | `groq:llama-3.3-70b-versatile` | 7 | needs `api_key` |
| `pi-qwen` | `pi:local-model` | 6 | pi CLI agent on local Qwen 27B, keyless, slow |
| `ollama-local` | `ollama:deepseek-r1:1.5b` | 5 | keyless, small |
| `toposwarm-agent` | `toposwarm:router` | 1 | agentic router, keyless, last resort |

## Step 2 — Wire the leg (worked example: `pi:`)

1. In `modules/llm_factory.py` add a private completer following
   `_pi_complete(model, prompt, max_tokens)`: resolve the binary with
   `shutil.which`, run list-form `subprocess.run(..., shell=False)`
   with a bounded timeout (`LAZYOWN_PI_TIMEOUT`, default 300s for
   CPU-served 27B models), raise `RuntimeError` on missing binary,
   timeout, non-zero exit, or empty stdout.
2. Register the prefix in BOTH `complete()` and `stream_complete()`
   spec allowlists. Streaming legs may simply delegate to `complete()`
   (the pool falls back automatically when no streamer exists).
3. Update the `complete()` docstring leg list.
4. Constants live next to the other backend defaults:
   `PI_PROVIDER_ID = "local-qwen"` (must match the provider id that
   `scripts/pi_qwen_setup.sh` registers in `~/.pi/agent/models.json`),
   `PI_DEFAULT_MODEL = "local-model"`.
5. The leg needs NO new `payload.json` / `params/*.yaml` key: it reuses
   `llamacpp_host` + `llm_model_llamacpp`. After
   `assign llamacpp_host <url>`, re-run the `pi_qwen` addon once so the
   setup script re-registers the endpoint URL.

## Step 3 — Register the pool member

Append to `LlmPool.DEFAULT_MEMBERS` in `modules/lazy_loop.py`:

```python
{"name": "pi-qwen", "model": "pi:local-model", "priority": 6},
```

Keep `priority` sorted descending. Placement guidance: raw local
endpoints first (fast), cloud second (needs key), agent CLIs third
(smart but slow: minutes per turn on CPU), tiny/embedded next,
routers last. Operators reorder live with `set_priority()` or by
editing `sessions/lazy/llm_pool.json`.

## Step 4 — Tests (all must pass before shipping)

```bash
env/bin/python -m pytest tests/test_pi_leg.py tests/test_intel_fusion.py \
  tests/test_loop_llm_resilience.py tests/test_placeholder_coverage.py -q
```

Rules:

- New legs ship `tests/test_<leg>_leg.py` with mocked subprocess:
  missing binary, non-zero exit, empty reply, timeout, model
  passthrough, case-insensitive prefix, empty-prompt short-circuit,
  stream fallback, and one pool-level test driving
  `LlmPool.complete(..., members=[...])`.
- `tests/test_intel_fusion.py::test_llm_defaults_seeded` pins the full
  member table: extend it, never weaken it.
- Never add the leg id to `SUPPORTED_BACKENDS`: the canonical-backend
  contract test pins that tuple and leg-only prefixes intentionally
  bypass it (same as `toposwarm:`).

## Step 5 — Verify live

```bash
env/bin/python -c "
from modules.llm_factory import complete
print(complete('pi:local-model', 'Reply with exactly: PI-LEG-OK')[:40])"
```

Expect the exact reply. First call warms the model: allow minutes on
CPU. Then run one loop-mode turn bound to the leg and confirm the
`pi-qwen` row in the usage ledger (`sessions/lazy/llm_usage.json`).
