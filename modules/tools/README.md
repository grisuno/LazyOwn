# modules/tools

Reusable development harnesses for the LazyOwn autonomous loop. They
live in the repo (not `/tmp`) so every future session can rerun them.

| Tool | What it verifies | Run |
|------|------------------|-----|
| `loop_smoke.py` | End-to-end `run_loop()`: bootstrap streams into the panel, verb output is visible, no observer recursion, terminal restored | `python -m modules.tools.loop_smoke` |
| `monitor_smoke.py` | Headless Textual monitor (`lazy_view`): panes render, tabs/keys work, task binding | `python -m modules.tools.monitor_smoke` |

Both tools sandbox `STORE_DIR`/`_store_path` in a temporary directory,
restore the module globals in a `finally` block, and never touch the
network or the real `sessions/lazy` store. Exit code is `0` when every
check passes, `1` otherwise.

They are also exercised by `tests/test_lazy_runner.py` so they cannot
rot silently.
