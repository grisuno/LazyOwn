# config/

Build-time default constants for the framework, stored as data instead
of literals scattered through commands.

- `defaults.toml` is the single source of truth for fallback ports,
  wordlists and well-known paths. Edit it with any text editor; no
  Python change is required.
- `core/defaults.py` is the only reader. Commands must call its typed
  helpers (`default_lport()`, `rockyou_wordlist()`, ...) instead of
  hardcoding values.
- Live engagement values always win: commands read `payload.json`
  first (via `assign`) and fall back to these defaults only when the
  key is unset. The TOML file itself is never rewritten at runtime;
  the `defaults` CLI command and `GET/POST /api/defaults` inspect and
  override through `payload.json`.
