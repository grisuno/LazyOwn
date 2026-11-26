# core

Shared foundation layer imported by both `lazyown.py` and `lazyc2.py`. Contains
the canonical `Config` class, cryptographic utilities, validation helpers, and
low-level protocol constants. Nothing in `core/` imports from `lazyown.py`,
`lazyc2.py`, or `modules/`.

## Files

37 modules. The table below lists the ones with a dedicated contract; the rest
are single-concern helpers whose docstrings are the documentation.

| File | Purpose |
|------|---------|
| `config.py` | Canonical `Config` class. Wraps the `payload.json` dict and exposes keys as attributes (`cfg.rhost`) and via `__getitem__` (`cfg["rhost"]`). Returns `None` for missing keys. Atomic merge-save with lock + tmp + `os.replace` + JSONL audit. **This is the single definition** — `utils.py` re-exports it for backwards compatibility but must not redefine it. |
| `payload_schema.py` | Field-spec schema for `payload.json` (defaults, validation, secret marking). |
| `validators.py` | Input validation functions: IP address format check, port range check, safe path validation. Used by CLI commands before they touch `payload.json` or the filesystem. |
| `protocols.py` | `typing.Protocol` definitions shared across `cli/`, `modules/`, and `skills/`: `PayloadProvider`, `CommandLister`, `TerminalIO`, `LLMBackend`, `MemoryStore`, `Selector`. Enables Dependency Inversion without circular imports. |
| `console.py` | Rich console singleton and ANSI colour helpers used by `print_msg`, `print_warn`, `print_error`. |
| `dependencies.py` | Graceful optional-import handling. `optional_import` / `optional_attr` bind heavy third-party packages lazily so a missing dependency (for example `pycryptodome`) degrades a single feature instead of crashing the framework at import time. Standard-library only. |
| `api_authz.py` | Tenant-bound API key authorization. ``ApiKeyStore`` persists SHA-256-hashed keys with atomic writes. ``require_api_auth`` decorator enforces key validation + permission + tenant checks on Flask routes. Keys are never stored in plaintext. |
| `safe_exec.py` | The single subprocess primitive: `safe_system`, `safe_run_argv`, `safe_run_shell` with shell-metachar guard, process-group kill and timeout. |
| `hardening.py` | Facade over the single-concern siblings (`core.paths`, `core.tls`, `core.secrets`, `core.text`) plus subprocess/clipboard/XML helpers and host/port/CIDR validators. Its `safe_subprocess_run` is a deprecated delegate to `safe_exec.safe_run_argv`. |
| `paths.py` | Filesystem containment for untrusted paths: realpath guards, segment/dir/YAML validators, `safe_open_under`, `sanitize_filename`. |
| `tls.py` | Client TLS contexts: verifying default with TLS 1.2 floor and the gated self-signed lab fallback. |
| `secrets.py` | Owner-only secret storage, Fernet sealing, `require_encryption_key`, sshpass `-e` environment contract. |
| `text.py` | HTML escaping, PowerShell quoting, emoji detection, credential redaction. |
| `safe_subprocess.py` | Deprecated `SafeRunner` default-deny wrapper (JSON audit trail). New code uses `safe_exec` or `CommandExecutor`. |
| `command_bridge.py` | Lazy double-checked bridge into the CLI shell for out-of-process consumers (bots, MCP). |
| `autonomous.py` | Autonomous-mode driver for headless/CI runs. |
| `atomic_store.py` | JSON read/append/write helpers with locking shared by engine stores. |
| `crypto.py` | Cryptographic primitives: XOR encrypt/decrypt for beacon encoding, AES-256 helpers, key/IV generation. |
| `session_secrets.py` | Boot-time rotation and validation of `rat_key` / `session_magic` / AES key. |
| `credential_vault.py` | Sealed-at-rest credential store. |
| `errors.py` / `error_advice.py` | Exception taxonomy (9 typed errors + `ErrorCode`) and operator-facing remediation hints. |
| `process.py` | Streaming command runner (`run_command`), sudo helpers, binary/package probes. |
| `network.py` | ARP packet crafting, interface enumeration, socket helpers. |
| `scheduler.py` | Bounded task scheduler with a pluggable backend. |
| `security.py` | Anti-debug/anti-analysis probes for the operator tool (opt-in). |
| `terminal_guard.py` | termios snapshot/restore plus mode-reset sequences for interactive automation. |
| `host_policy.py` | Host/world-model name policy (IP literal or dotted hostname). |
| `http.py` | Small HTTP helpers shared outside the C2. |
| `llm_budget.py` / `llm_key_pool.py` | Token budget tracking and multi-key LLM pool with health registry. |
| `prompt.py` | Prompt template registry for LLM surfaces. |
| `profiles.py` | YAML orchestrator profile loading/merging. |
| `param_registry.py` | Parameter registry backing command forms and wizards. |
| `parsers.py` | Shared output parsers (ANSI strip, tool output normalization). |
| `text_utils.py` | Text normalization helpers. |
| `safe_console.py` | Hardened stdout/stderr writer (blocking stdio, ANSI guard). |
| `safe_import.py` | Guarded dynamic import used by plugin/tool loaders. |
| `reverse_shell_secret.py` | Beacon payload secret derivation. |
| `defaults.py` | Default constants shared by CLI and C2. |
| `__init__.py` | Re-exports `Config`, `load_payload`, the validators, and `optional_import` / `optional_attr` / `MissingDependencyError` so callers can do `from core import Config`. |

## Usage

```python
from core import Config
from core.validators import check_rhost, check_lhost

cfg = Config({"rhost": "10.10.11.5", "lhost": "10.10.14.3"})
print(cfg.rhost)  # "10.10.11.5"
print(cfg["nonexistent"])  # None

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

AES = optional_attr("Crypto.Cipher", "AES")  # real class when installed
pandas = optional_import("pandas")  # deferred proxy when missing

if pandas:  # proxy is falsy
    frame = pandas.DataFrame(rows)
```

## Safe execution wrappers — one home per concern (dedup contract)

Two layers exist; pick by semantics, never reimplement:

| Layer | Semantics | Use when |
|---|---|---|
| `core.safe_exec` (safe_system / safe_run_argv / safe_run_shell) | THE subprocess primitive: shell-metachar guard, process-tree kill, timeout, `extra_env` | Every new code path running a known program or shell string |
| `modules.command_executor.CommandExecutor` | Policy + tee layer on top of the primitive: hooks, live streaming, log tee, thread-local timeout/stdin | Interactive shell command rows (`LazyOwnShell.cmd`) and anything needing output capture + display |

Deprecated wrappers kept as shims until their callers migrate:

- `core.hardening.safe_subprocess_run` — stricter validation contract, delegates execution to `safe_exec.safe_run_argv`; emits `DeprecationWarning`.
- `core.safe_subprocess.SafeRunner` — default-deny gate + JSON audit trail; emits `DeprecationWarning`.

`core/executor.py` and `core/process.run` were deleted as dead code (zero
production consumers, verified). `core/logging.py` was retired earlier:
`modules/logging_config.py` is the only logging bootstrap (18 consumers).
