# tests

Automated test suite for the LazyOwn framework. Tests exercise real modules
against fixtures — no mocking of the C2, the autonomous daemon, or the
filesystem layout. Run with `pytest` from the repository root.

## Running the tests

```bash
# All tests
python -m pytest tests/ -v

# Single file
python -m pytest tests/test_core.py -v

# Fast smoke check (exclude slow integration tests)
python -m pytest tests/ -v -m "not slow"

# With coverage
python -m pytest tests/ --cov=. --cov-report=term-missing
```

## Test files

| File | What it covers | Tests |
|------|----------------|-------|
| `test_core.py` | `core/config.py` Config class, validators, protocol interfaces | ~20 |
| `test_core_modules.py` | `obs_parser`, `world_model`, `playbook_engine` integration | ~15 |
| `test_packaging.py` | `pyproject.toml`, `setup.py`, `.pre-commit-config.yaml`, CI workflows, `.gitignore` | ~35 |
| `test_cli_assign.py` | `assign` / `set` command logic, payload write-back | ~10 |
| `test_cli_command_sets.py` | cmd2 `CommandSet` auto-discovery and registration | ~8 |
| `test_cli_enhancements.py` | Fuzzy finder, form validator, status tail, transcript store, addon hot-reloader, payload-aware completer | ~36 |
| `test_command_palette.py` | Phase-aware palette filtering, graph-backed scoring | ~12 |
| `test_banner_config.py` | Prompt segment wizard, segment serialization | ~10 |
| `test_fuzzy_picker.py` | Curses picker scoring, navigation state machine | ~14 |
| `test_graph_advisor.py` | Graph search, neighbour walk, next-step recommendation, cache invalidation | ~20 |
| `test_reactive_hints.py` | Postcmd hook firing, skip-list enforcement, graph-absent no-op | ~10 |
| `test_dashboard_tui.py` | Widget data helpers, `_read_json`, `_read_recent_commands`, beacon count | ~15 |
| `test_mcp_improvements.py` | MCP helper functions: session init format, target context aggregation, tasks cleanup, evidence grep, run_command dry-run | ~25 |
| `test_moe_rl_swan.py` | SWAN MoE routing, RL Q-table update, ensemble synthesis | ~18 |
| `test_aci_planner.py` | ACI plan generation, status reporting, replan logic | ~12 |
| `test_engagement_and_ping.py` | Engagement state hooks, ping result parsing | ~8 |
| `test_lint_quality.py` | Ruff lint, mypy type check, bandit security scan on source files | ~6 |
| `test_security_lazyc2.py` | C2 route validation, path traversal guards, template name validation | ~20 |
| `test_vuln_mitigations.py` | Vulnerability scanner output parsing, NVD integration | ~10 |
| `test_blacksandbeacon_addon.py` | `blacksandbeacon.yaml` and `blacksandbeacon_bof.yaml` YAML structure, params, path safety, command templates, no hardcoded secrets | 59 |
| `test_collab_and_onboarding.py` | `EventBus`, `LockManager`, `OperatorRegistry`, all 8 collab Flask endpoints, `collab.html` template, `QUICKSTART.md` completeness, wizard DIP contract, `collab_join` CLI command | 67 |
| `integration_autonomous_flow.py` | End-to-end autonomous engagement loop against `sessions/` fixtures | ~15 |

## Fixtures and conventions

- Tests that need a `sessions/` directory receive a `tmp_path` fixture and
  point all file reads/writes there.
- Tests that spin up Flask apps use `app.test_client()` — no real HTTP server
  is started.
- No test mocks `payload.json`, the C2, or the autonomous daemon. If a module
  reads `payload.json`, the test either provides a real minimal file or injects
  a `params` dict through the module's constructor.
- The `integration_autonomous_flow.py` file is the only test that touches real
  `sessions/` fixtures. Mark with `@pytest.mark.slow` to exclude from CI fast
  runs.

## Adding a test file

1. Name it `test_<feature>.py`.
2. Add it to `pyproject.toml` under `[tool.pytest.ini_options] testpaths`.
3. One class per logical unit under test, one method per behaviour.
4. Never assert on log output — assert on return values and side effects.
