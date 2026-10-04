## Authorization Scope Guard

A red-team framework that reads its target from `payload.json` has a sharp edge:
a stray `rhost` fires offensive commands at an unauthorized host. The scope guard
is the safety net. Every interactive command flows through a single chokepoint
that checks the active target against your authorized engagement scope before the
command runs.

```bash
(LazyOwn) > scope add 10.10.11.0/24       # CIDR, bare IP, hostname, or *.corp.local wildcard
(LazyOwn) > scope add dc.corp.local
(LazyOwn) > scope mode enforce            # off | warn (default) | enforce
(LazyOwn) > scope                         # show current scope and posture
```

- **Fail-open by design**: dormant while the scope is empty or the mode is `off`,
  so existing campaigns are unaffected until you opt in. Any internal error
  allows the command rather than blocking the operator.
- **`warn`** annotates out-of-scope offensive commands; **`enforce`** blocks them
  pending explicit confirmation (and refuses in non-interactive sessions).
- Only offensive kill-chain categories are gated; reporting, configuration and
  local helpers always run. New offensive `do_*` commands are auto-classified.
- Stored in `payload.json` (`scope`, `scope_enforcement`); pure logic lives in
  `cli/scope_guard.py` with zero coupling to the shell.

## Reproducible installs

Dependencies are declared once in `pyproject.toml` (single source of truth) and
pinned for reproducible installs:

- `requirements.txt` — cross-platform core lock (no CUDA wheels).
- `requirements-ml.txt` — optional, heavy ML stack (torch/CUDA, scikit-learn).
- `install.sh` runs under strict mode and is idempotent. The default install
  is light; opt into extras with `--with-ml` (2 GB ML stack), `--with-ollama`
  (local LLM runtime) and `--with-tools` (common external binaries).
- Developers: `pip install -e .[ml,dev]`.
