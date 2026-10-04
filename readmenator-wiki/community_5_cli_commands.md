# cli/commands

*Community 5 | 5 files | cohesion 0.31*

## Definition

This community groups 5 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.31). Central symbols: `BackendAdapterSpec`, `BackendRegistrySpec`, `CmdIntegrationRegressionSpec`, `CollabPresenceSource`, `CommandHintSuggestionSource`, `CommandSetActivationSpec`, `ConfigDedupeSpec`, `DocstringDisciplineSpec`. Core file: `tests/test_improvements_spec.py` (160 symbols). Documented purpose: Phase-scoped CommandSet modules.  Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping commands that share a kill-chain phase or attack do.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/orchestration.py` | py | utility | 13 | yes |
| `cli/status_bar.py` | py | presentation | 64 | yes |
| `tests/test_improvements_spec.py` | py | testing | 160 | yes |
| `tests/test_status_bar_operators.py` | py | testing | 9 | yes |

## Key Symbols

- `OrchestrationConfig` (class, `cli/commands/orchestration.py:37`) `class OrchestrationConfig` - Immutable defaults for the orchestration verbs.
- `_build_status_bar_parser` (method, `cli/commands/orchestration.py:57`) `def _build_status_bar_parser()` - Return the argparse parser used by ``status_bar``.
- `_build_orchestrate_parser` (method, `cli/commands/orchestration.py:70`) `def _build_orchestrate_parser()` - Return the argparse parser used by ``orchestrate``.
- `OrchestrationCommandSet` (class, `cli/commands/orchestration.py:117`) `class OrchestrationCommandSet(LazyOwnCommandSet)` - Operator commands exposing the status bar and unified orchestrator.
- `do_status_bar` (method, `cli/commands/orchestration.py:125`) `def do_status_bar(self, args)` - Inspect, toggle and refresh the prompt status bar.
- `do_orchestrate` (method, `cli/commands/orchestration.py:151`) `def do_orchestrate(self, args)` - Route a goal through the unified orchestrator and print the result.
- `_resolve_shell` (method, `cli/commands/orchestration.py:177`) `def _resolve_shell(self)` - Return the bound cmd2 shell or ``None`` if not yet registered.
- `_status_manager` (method, `cli/commands/orchestration.py:192`) `def _status_manager(self)`
- `_orchestrator` (method, `cli/commands/orchestration.py:198`) `def _orchestrator(self)`
- `_status_bar_show` (method, `cli/commands/orchestration.py:204`) `def _status_bar_show(self, manager)`
- `_status_bar_refresh` (method, `cli/commands/orchestration.py:209`) `def _status_bar_refresh(self, manager)`
- `_status_bar_toggle` (method, `cli/commands/orchestration.py:219`) `def _status_bar_toggle(self, manager, enabled)`
- `_format_text` (method, `cli/commands/orchestration.py:228`) `def _format_text(result)`
- `StatusBarConfig` (class, `cli/status_bar.py:41`) `class StatusBarConfig` - Immutable configuration container for the status bar subsystem.
- `from_payload` (method, `cli/status_bar.py:99`) `def from_payload(cls, payload)` - Return a config with overrides applied from a ``payload.json`` mapping.
- `StatusContext` (class, `cli/status_bar.py:127`) `class StatusContext` - Immutable snapshot of the pieces the bar renders.
- `IStatusSource` (class, `cli/status_bar.py:143`) `class IStatusSource(Protocol)` - One-method protocol that every status source must satisfy.
- `collect` (method, `cli/status_bar.py:146`) `def collect(self)` - Return the field value for this source as a plain string.
- `FileSystemReader` (class, `cli/status_bar.py:151`) `class FileSystemReader` - Path-validated, size-bounded reader for ``sessions/`` artefacts.
- `__init__` (method, `cli/status_bar.py:160`) `def __init__(self, config, root)` - Initialise with the active config and optional explicit root.
- `root` (method, `cli/status_bar.py:179`) `def root(self)` - Return the resolved root directory backing this reader.
- `read_text` (method, `cli/status_bar.py:183`) `def read_text(self, relative)` - Return the contents of ``relative`` truncated to ``max_file_bytes``.
- `read_json` (method, `cli/status_bar.py:204`) `def read_json(self, relative)` - Return parsed JSON from ``relative`` or ``None`` on failure.
- `glob_latest` (method, `cli/status_bar.py:222`) `def glob_latest(self, pattern)` - Return the most recently modified path matching ``pattern``.
- `_safe_path` (method, `cli/status_bar.py:247`) `def _safe_path(self, relative)`
- `_is_within_root` (method, `cli/status_bar.py:253`) `def _is_within_root(self, candidate)`
- `_has_traversal` (method, `cli/status_bar.py:261`) `def _has_traversal(value)`
- `PayloadTargetSource` (class, `cli/status_bar.py:268`) `class PayloadTargetSource` - Status source: active target identifier.
- `__init__` (method, `cli/status_bar.py:271`) `def __init__(self, config, payload)` - Bind to the live config and a payload mapping.
- `collect` (method, `cli/status_bar.py:283`) `def collect(self)` - Return the first non-empty target key from ``payload.json``.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 9
- Cross-boundary resolved imports (EXTRACTED): 12

## Connections

- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/orchestration.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 5 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/status_bar.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 5 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/status_bar.py imports cli/themes.py.

## Risks

- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)
- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)
- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)
- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)
- [layer strict] `tests/test_status_bar_operators.py` (testing) -> `cli/status_bar.py` (presentation)

## Open Questions

- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.31?

## Sources

- `cli/commands/__init__.py`
- `cli/commands/orchestration.py`
- `cli/status_bar.py`
- `tests/test_improvements_spec.py`
- `tests/test_status_bar_operators.py`
