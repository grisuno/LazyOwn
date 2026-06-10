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
| `dependencies.py` | Graceful optional-import handling. `optional_import` / `optional_attr` bind heavy third-party packages lazily so a missing dependency (for example `pycryptodome`) degrades a single feature instead of crashing the framework at import time. `OPTIONAL_PYTHON_DEPENDENCIES` is the single source of truth for each lazily-imported package's install hint. Standard-library only, so `python3 -m core.dependencies` works even when `rich` or `cmd2` are broken. |
| `__init__.py` | Re-exports `Config`, `load_payload`, the validators, and `optional_import` / `optional_attr` / `MissingDependencyError` so callers can do `from core import Config`. |

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
- Heavy third-party packages must be bound through `optional_import` /
  `optional_attr`, never imported directly at module top level in
  `utils.py`. This keeps a single missing package from crashing the whole
  framework at import time. The dependent feature raises
  `MissingDependencyError` (with a `pip install` hint) only when actually
  used. The operator-facing preflight report — Python version, virtual
  environment, external binaries, certificates, SecLists — lives in
  `cli/doctor.py` (the `doctor` shell command); `core/dependencies.py` owns
  runtime resilience for lazily-imported Python packages only.

## Optional dependencies

```python
from core.dependencies import optional_attr, optional_import

AES = optional_attr("Crypto.Cipher", "AES")   # real class when installed
pandas = optional_import("pandas")             # deferred proxy when missing

if pandas:                                     # proxy is falsy
    frame = pandas.DataFrame(rows)
```

