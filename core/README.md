# core

Shared foundation layer imported by both `lazyown.py` and `lazyc2.py`. Contains
the canonical `Config` class, cryptographic utilities, validation helpers, and
low-level protocol constants. Nothing in `core/` imports from `lazyown.py`,
`lazyc2.py`, or `modules/`.

## Files

| File | Purpose |
|------|---------|
| `config.py` | Canonical `Config` class. Wraps the `payload.json` dict and exposes keys as attributes (`cfg.rhost`) and via `__getitem__` (`cfg["rhost"]`). Returns `None` for missing keys. **This is the single definition** — `utils.py` re-exports it for backwards compatibility but must not redefine it. |
| `crypto.py` | Cryptographic primitives: XOR encrypt/decrypt for beacon encoding, AES-256 helpers, and key/IV generation. |
| `validators.py` | Input validation functions: IP address format check, port range check, safe path validation. Used by CLI commands before they touch `payload.json` or the filesystem. |
| `protocols.py` | `typing.Protocol` definitions shared across `cli/`, `modules/`, and `skills/`: `PayloadProvider`, `CommandLister`, `TerminalIO`, `LLMBackend`, `MemoryStore`, `Selector`. Enables Dependency Inversion without circular imports. |
| `console.py` | Rich console singleton and ANSI colour helpers used by `print_msg`, `print_warn`, `print_error`. |
| `__init__.py` | Re-exports `Config`, `load_payload`, and the validators so callers can do `from core import Config`. |

## Usage

```python
from core import Config
from core.validators import check_rhost, check_lhost

cfg = Config({"rhost": "10.10.11.5", "lhost": "10.10.14.3"})
print(cfg.rhost)          # "10.10.11.5"
print(cfg["nonexistent"]) # None

if not check_rhost(cfg.rhost):
    print("rhost is not set")
```

## Rules

- `core/` has no runtime dependencies beyond the Python standard library and
  `rich`. Never add `flask`, `cmd2`, or any framework import here.
- `Config` is defined exactly once in `core/config.py`. The `utils.py`
  re-export exists for backwards compatibility with the large existing codebase
  but adds no new logic.
- All validators return `bool` — they never raise, never print, never log.
  Callers decide what to do on failure.
