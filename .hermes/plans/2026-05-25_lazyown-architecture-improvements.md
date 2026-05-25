# LazyOwn Architecture Analysis: Improvement Opportunities Beyond Monolith Decomposition

> Plan mode. No execution. Comprehensive codebase analysis using graphify, documentation, and source metrics.

**Date:** 2026-05-25
**Scope:** Full codebase (~160k LOC Python, 261 prod files, 46 test files)
**Sources:** graphify graph (2498 nodes), CLAUDE.md, README.md, source code, CLI docs, monolith migration playbook

---

## 1. Quantitative Baseline

| Metric | Value | Implication |
|--------|-------|------------|
| Total production lines | 159,736 | Large codebase |
| Test lines | 17,333 | 10.9% coverage -- fragile |
| `lazyown.py` | 28,884 | Single-class cmd2 shell |
| `skills/lazyown_mcp.py` | 9,630 | 124 elif dispatch blocks |
| `lazyc2.py` | 5,430 | Flask monolith |
| `utils.py` | 3,324 | Shared by CLI and C2, 24 internal imports |
| `modules/` | ~50 files | Mixed LLM, exploits, C2, config |
| `cli/commands/` | 9 phase modules | Partial extraction from monolith |
| Hardcoded paths | 7 files | Despite coding standards |
| Graph edges | 0 | Dependency graph has no relationships |
| MCP elif blocks | 124 | Single giant handler function |
| Internal coupling | `utils` (24), `lazyc2` (26) | High coupling hubs |

---

## 2. Improvement Areas (Beyond Monolith Decomposition)

### A. MCP Tool Registry (High Impact / Medium Effort)

**Current State:** The MCP server `skills/lazyown_mcp.py` uses a 124-branch `if/elif/elif...` chain in a single `call_tool` handler. Adding a tool requires editing the handler function and adding another elif block. This violates Open-Closed Principle.

**Target:** Replace the if/elif chain with a dictionary-based tool registry using decorators:

```python
# skills/lazyown_tool_registry.py (new)
_registry: dict[str, ToolHandler] = {}

def register(name: str, schema: dict):
    def decorator(fn):
        _registry[name] = ToolHandler(name=name, schema=schema, handler=fn)
        return fn
    return decorator

@register("lazyown_run_command", RUN_COMMAND_SCHEMA)
async def handle_run_command(args, ctx): ...
```

**Benefits:**
- New MCP tools added without touching the dispatch function.
- Each handler is independently testable.
- Hot-reload: registry can be rebuilt without restart.
- Same pattern applicable to `cli/registry.py` (which already does CommandSet discovery).

**Files to create:**
- `skills/lazyown_tool_registry.py`
- `skills/lazyown_tools/core_config.py`
- `skills/lazyown_tools/intel_recon.py`
- `skills/lazyown_tools/autonomous.py`
- `skills/lazyown_tools/c2_control.py`
- `skills/lazyown_tools/hermes_sync.py`

---

### B. Typed Configuration Layer (High Impact / Medium Effort)

**Current State:** `payload.json` is read as a raw dict everywhere. `core/payload_schema.py` defines field specs but only for documentation/wizard. No runtime type enforcement at the configuration edge.

**Target:** Wrap `payload.json` in a typed `EngagementConfig` class that validates on construction:

```python
# core/config_types.py (new)
@dataclass(frozen=True)
class EngagementConfig:
    rhost: str = ""
    lhost: str = ""
    domain: str = ""
    c2_port: int = 4444
    os_id: int = 2
    # ... all known keys with types and defaults
```

**Benefits:**
- Catch configuration errors at startup, not mid-operation.
- IDE autocompletion for config keys.
- Remove the `get_str`/`get_int`/`get_bool` helpers scattered everywhere (CONSISTENCY).
- Enables diff-based config changes (detect what changed between operator actions).

**Files to create:**
- `core/config_types.py`

---

### C. Event Bus for Session State (High Impact / High Effort)

**Current State:** Components communicate by polling shared files: `payload.json`, `world_model.json`, `objectives.jsonl`, `sessionLazyOwn.json`, `tasks.json`. This is fragile (race conditions, file system latency) and couples components to the filesystem layout.

**Target:** Introduce a lightweight in-process event bus (`EventBus` already exists in `collab_bp` for C2 collab -- generalize it):

```python
# core/event_bus.py (new)
class SessionEventBus:
    def publish(self, event_type: str, payload: dict) -> None: ...
    def subscribe(self, event_type: str, callback: callable) -> None: ...
```

**Benefits:**
- Components react to events instead of polling files.
- Decouples file producers from file consumers (SOLID -- Dependency Inversion).
- Enables audit: every state mutation is an event.
- Existing `collab_bp.EventBus` is the prototype -- lift to `core/`.

**Files to create:**
- `core/event_bus.py`
- `core/events.py` (event type constants)

**Files to modify:**
- `autonomous_daemon.py` -- subscribe instead of polling
- `lazyown_mcp.py` -- publish instead of writing files directly

---

### D. Unified Error Taxonomy and Structured Fallbacks (Medium Impact / Medium Effort)

**Current State:** Error handling is inconsistent. Some code returns strings, some raises generic `Exception`, some uses `print_error`. The CLI hand-re-implements error patterns in every `do_*` method without a shared vocabulary.

**Target:** Define typed error classes and a `Result[T]` pattern:

```python
# core/errors.py (new)
class LazyOwnError(Exception): ...

class ConfigError(LazyOwnError): ...
class NetworkError(LazyOwnError): ...
class BinaryNotFound(LazyOwnError): ...
class OsMismatch(LazyOwnError): ...
class CredentialNotFound(LazyOwnError): ...
class PermissionDenied(LazyOwnError): ...

@dataclass
class Result:
    success: bool
    data: Any = None
    error: LazyOwnError | None = None
    artifacts: list[str] = field(default_factory=list)
```

**Benefits:**
- Every tool returns a `Result`, never a bare string.
- Hermes/caller can pattern-match on error type for intelligent retry.
- Report generator can aggregate errors by type for operator awareness.
- CLI, C2, and MCP all share the same error vocabulary.

**Files to create:**
- `core/errors.py`
- `core/result.py`

---

### E. Session Artifact Lifecycle Management (Medium Impact / Low Effort)

**Current State:** `sessions/` files are created indefinitely. No TTL, no cleanup, no archival. Over a long campaign, hundreds of files accumulate with no garbage collection.

**Target:** Add a `SessionHousekeeper` that:

```python
# core/session_housekeeper.py (new)
class SessionHousekeeper:
    def collect_garbage(self, max_age_days: int = 30) -> list[Path]:
        """Remove partial scans, rotate old logs."""
    def archive_campaign(self, output_tar: Path) -> None:
        """Bundle the active campaign into a portable archive."""
    def stats(self) -> dict:
        """Return size, file count, age distribution."""
```

**Benefits:**
- Prevent disk exhaustion on long campaigns.
- Enable operator handoff via single archive.
- MCP tool `lazyown_session_housekeeping` surfaces to Hermes.

**Files to create:**
- `core/session_housekeeper.py`

---

### F. State Machine for Engagement Phases (Medium Impact / Low Effort)

**Current State:** The kill chain (recon -> enum -> exploit -> ...) is conceptual. No component enforces phase ordering or prevents out-of-order operations.

**Target:** An `EngagementStateMachine` that:

```python
# core/engagement_fsm.py (new)
class EngagementFSM:
    PHASES = [RECON, ENUM, EXPLOIT, POSTEXP, PERSIST, PRIVESC, CRED, LATERAL, EXFIL, C2, REPORT]
    TRANSITIONS = {RECON: [ENUM], ENUM: [EXPLOIT], ...}

    def transition_to(self, new_phase: str) -> Result: ...
    def allowed_in(self, phase: str) -> list[str]: ...
    def is_allowed(self, command_phase: str) -> bool: ...
```

**Benefits:**
- Autonomous daemon can't skip phases.
- Hermes/caller gets a warning when trying to run lateral-movement before recon.
- `world_model.json` phase becomes authoritative and enforced.

**Files to create:**
- `core/engagement_fsm.py`

---

### G. Test Infrastructure Upgrade (Critical / High Effort)

**Current State:** 10.9% test coverage. No `conftest.py`. No test fixtures. No test data factories. Each test module reinvents setup.

**Target:**

```
tests/
├── conftest.py                  # shared fixtures
├── factories.py                 # test data builders
├── fixtures/
│   ├── minimal_payload.json     # known-good config
│   ├── sample_scan.nmap         # known nmap output
│   └── sample_creds.txt         # known credentials
├── unit/
│   ├── test_config_bridge.py
│   ├── test_engagement_fsm.py
│   ├── test_event_bus.py
│   └── test_tool_registry.py
├── integration/
│   ├── test_mcp_tools.py
│   ├── test_cli_commands.py
│   └── test_c2_endpoints.py
└── contract/
    └── test_mcp_schema.py       # validate MCP tool shapes
```

**Priority test targets:**
1. `core/config_bridge.py` (currently untested)
2. `core/engagement_fsm.py` (to be created)
3. `core/event_bus.py` (to be created)
4. `skills/lazyown_tool_registry.py` (to be created)
5. Each extracted `cli/commands/<phase>.py`

**Files to create:**
- `tests/conftest.py`
- `tests/factories.py`
- `tests/fixtures/`
- `tests/unit/`
- `tests/integration/`
- `tests/contract/`

---

### H. Idempotency Guarantees (Low Impact / Low Effort)

**Current State:** `session_init` checks if `scan_*.nmap` exists to avoid re-scanning, but this logic is ad-hoc and duplicated in multiple places.

**Target:** A centralized `ArtifactIdempotencyGuard`:

```python
# core/idempotency.py (new)
class ArtifactIdempotencyGuard:
    def should_skip(self, artifact_type: str, target: str, freshness_s: int) -> bool: ...
    def mark_completed(self, artifact_type: str, target: str) -> None: ...
    def invalidate(self, artifact_type: str, target: str) -> None: ...
```

**Benefits:**
- Single source of truth for "already done?" decisions.
- Respects freshness thresholds (in CLAUDE.md already, but scattered).
- Prevents 30-minute scan re-runs silently.

**Files to create:**
- `core/idempotency.py`

---

### I. Graceful Degradation Layer (Medium Impact / Low Effort)

**Current State:** Optional dependencies (ChromaDB, Groq API, pwntomate tools, graphify graph) are checked with try/except at import time. When unavailable, some tools return `"module unavailable"` strings -- others raise unhandled exceptions.

**Target:** A `CapabilityRegistry`:

```python
# core/capability_registry.py (new)
class CapabilityRegistry:
    def register(self, name: str, checker: callable, fallback: callable) -> None: ...
    def is_available(self, name: str) -> bool: ...
    def execute(self, name: str, *args, **kwargs) -> Result: ...
```

**Benefits:**
- Every optional capability has a declared fallback.
- `lazyown_capability_status` MCP tool: Hermes can query what's available.
- Operator sees "ChromaDB unavailable -- falling back to keyword search" instead of raw errors.

**Files to create:**
- `core/capability_registry.py`

---

### J. MCP Response Size Budgeting (Medium Impact / Low Effort)

**Current State:** The 95-tool MCP server sends all tool declarations to every Hermes turn. This consumes ~15K tokens per turn even when only 3-5 tools are used.

**Target implemented in `skills/hermes-lazyown/`:** Namespaced tools with `enabled_toolsets`. The extension here is automatic budget enforcement:

```python
# In hermes-lazyown: add response_size_budget to all tools
def _budgeted_response(result: str, max_tokens: int = 3000) -> str:
    if len(result) > max_tokens * 4:  # rough char-to-token ratio
        return result[:max_tokens * 4] + "\n[truncated by Hermes budget]"
    return result
```

**Files to modify:**
- `skills/hermes-lazyown/mcp_server.py` (add budget decorator)

---

## 3. Implementation Priority Matrix

| # | Improvement | Impact | Effort | Risk | Phase |
|---|------------|--------|--------|------|-------|
| A | MCP Tool Registry | High | Medium | Medium | 1 |
| B | Typed Config | High | Medium | Low | 1 |
| F | Engagement FSM | Medium | Low | Low | 1 |
| E | Artifact Housekeeping | Medium | Low | Low | 1 |
| I | Graceful Degradation | Medium | Low | Low | 2 |
| H | Idempotency Guards | Low | Low | Low | 2 |
| D | Error Taxonomy | Medium | Medium | High | 2 |
| J | Response Budgeting | Medium | Low | Low | 2 |
| C | Event Bus | High | High | High | 3 |
| G | Test Infrastructure | Critical | High | Low | 3 |

**Phase 1 (this week):** A + B + F -- immediate architectural improvements with low risk.
**Phase 2 (next week):** E + I + H + D + J -- stabilization and hardening.
**Phase 3 (month):** C + G -- foundational upgrades requiring coordinated changes.

---

## 4. Migration Rule: No Breakage

All new modules follow the existing pattern in `skills/hermes-lazyown/`:
- **New file in the appropriate directory** (`core/` for shared, `skills/` for MCP).
- **Zero modification of existing files** during Phase 1.
- **Fallback import pattern**: `try: from core.new_module import X; except ImportError: X = None`.
- **`py_compile` validation** before commit when runtime deps unavailable.

---

## 5. Files Summary

### New (to create):
```
core/
  config_types.py
  errors.py
  result.py
  event_bus.py
  events.py
  engagement_fsm.py
  session_housekeeper.py
  idempotency.py
  capability_registry.py

skills/
  lazyown_tool_registry.py
  lazyown_tools/
    __init__.py
    core_config.py
    intel_recon.py
    autonomous.py
    c2_control.py
    hermes_sync.py

tests/
  conftest.py
  factories.py
  fixtures/
    minimal_payload.json
    sample_scan.nmap
    sample_creds.txt
  unit/
    test_config_types.py
    test_engagement_fsm.py
    test_event_bus.py
    test_tool_registry.py
    test_errors.py
    test_result.py
    test_idempotency.py
    test_capability_registry.py
  integration/
    test_mcp_tools.py
  contract/
    test_mcp_schema.py
```

### Existing (to update -- minimal, backward-compatible):
```
CLAUDE.md                  -- add new core/ modules to repo map
README.md                  -- add new modules to MCP section
skills/lazyown_mcp.py      -- add lazyown_capability_status tool
skills/hermes-lazyown/     -- add response budget decorator
```

---

## 6. Open Questions

1. **Event bus transport:** In-process only, or also support Redis/PostgreSQL for multi-node deployments?
2. **Config immutability:** Should `EngagementConfig` be frozen (read-only after construction) or allow runtime mutations?
3. **Phase enforcement strictness:** Should the FSM block out-of-order commands entirely, or just warn?
4. **Backward compatibility window:** How long should the old if/elif MCP dispatch coexist with the new registry?
