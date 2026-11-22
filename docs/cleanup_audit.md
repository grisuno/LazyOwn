# Cleanup audit: dead code, wired modules, and duplication maps

This audit records the dead-code removals, the "looks dead but is wired"
modules that were deliberately kept, and the duplication graphs that are a
major refactor (mapped here rather than consolidated in a cleanup pass, to
avoid breaking contracts with a high-blast-radius change).

## Removed (verified dead)

| Module | Evidence |
|--------|----------|
| `modules/mario.py` | Zero references across `*.py`, `*.yaml`, `*.lua`, `*.ls`, `*.tool`. Its only dependency (`pygame`) had no other consumer. |

## Kept — looks like an experiment, but is wired (do not delete)

| Module / script | Wired by |
|-----------------|----------|
| `modules/kivi.py` | Addon `lazyaddons/kivi_revshell.yaml` and verb `addon:kivi_revshell` in `config/verbs.yaml` run it as a script ("Ejecuta el script kivi.py que se encuentra en la carpeta modules"). Invoked via shell, not imported. |
| `modules/ooficesod0woodo.py` | `config/poc_verbs.yaml` (`script: ooficesod0woodo.py`), which is loaded by `cli/commands/lazy_poc.py`, `modules/poc_registry.py`, `modules/selection/poc.py` and `modules/verb_catalog.py`. |
| `modules/lazypoophish.py` | `modules/lazy_runner.py` imports it and calls `fallback_ready` / `run_fallback` (phishing campaign fallback); covered by `tests/test_lazypoophish.py` and `tests/test_lazy_runner_fallback.py`. |
| `modules/lazygat.sh`, `modules/lazyatack.sh`, `modules/lazyevilwimrm.sh` | Referenced by `lazyown.py`. Spanish comments / informal names are a style nit, not dead code. |

## Duplication maps (major refactor — not consolidated here)

### Logging

| Module | Public surface | Importers |
|--------|----------------|-----------|
| `modules/logging_config.py` | `configure`, `get_logger`, `ColoredFormatter`, `JsonFormatter`, `CorrelationFilter`, `ResilientRotatingFileHandler`, correlation-id helpers | 18 (canonical) |
| `core/logging.py` | `StructuredLogger`, `get_logger`, `install_json_handler`, `reconfigure`, `StructuredLogConfig`, JSON/console formatters | 0 production consumers — only `tests/test_structured_logging.py` |

Overlap is `get_logger` + JSON formatting. `core/logging.py` is unused in
production. Recommendation: either wire `core/logging.py` in as the structured
backend for `logging_config.get_logger` (one delegation point) or retire it
with its test; do not run a 18-importer migration inside a cleanup pass. Note:
`skills/swan_agent.py` and `skills/sessions_watcher.py` import only
`modules.logging_config` (plus stdlib `logging`), not both modules.

### LLM clients

Contracts that must not break: `modules/llm_factory.py`, `modules/llm_prompts.py`,
`modules/llm_adapter.py` (see `docs/refactor_contracts.md`,
`docs/llm_prompt_contract.md`).

| Module | Importers |
|--------|-----------|
| `modules/llm_pool.py` | 15 |
| `modules/llm_orchestrator.py` | 10 |
| `modules/ai_fallback.py` | 9 |
| `modules/llm_client.py` | 7 |

Operational overlap (client/orchestrator/pool/fallback) is real, but each has
7–15 importers. Consolidation is a dedicated refactor behind the factory
facade, not a cleanup edit. Mapped here per the agreed "leave the exact graph
if it is a major refactor" rule.

### Subprocess / hardening

| Module | Importers |
|--------|-----------|
| `core/hardening.py` | 49 |
| `core/safe_exec.py` | 34 |
| `core/safe_subprocess.py` | 15 |

With 49 importers on `core/hardening.py` alone, unifying these into a single
`core/exec.py` is a high-blast-radius refactor requiring its own branch,
contract tests and mutation gates. Mapped, not consolidated.
