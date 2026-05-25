# LazyOwn MCP Tests

Automated tests for the LazyOwn MCP server and skill harness.

## Running

```bash
python3 -m pytest skills/tests/ -v
```

## Test Files

| File | Scope |
|------|-------|
| `test_autonomous_daemon.py` | Lifecycle and event-loop correctness of the autonomous daemon. |
| `test_facts.py` | FactStore parsing, deduplication and confidence scoring. |
| `test_harness_e2e.py` | End-to-end harness permission and hook validation. |
| `test_hive_mind.py` | Drone spawning, memory recall and consensus logic. |
| `test_objectives.py` | Objective injection, priority ordering and completion tracking. |
| `test_parquet_db.py` | Parquet knowledge-base queries and annotation. |

## Adding Tests

1. Name the file `test_<component>.py`.
2. Use `pytest` fixtures for shared setup (see existing tests for patterns).
3. Keep tests hermetic: mock external network calls and file-system side effects.
