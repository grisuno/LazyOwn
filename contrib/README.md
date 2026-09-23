# contrib

Quarantined but fully functional code that is excluded from the default maintained surface.

| Subdir | Role | How it works |
|--------|------|--------------|
| `legacy/` | Deprecated standalone scripts (ex `modules/legacy/`), kept working via symlinks in `modules/legacy/` | Real files live here; `modules/legacy/<name>.py` symlinks preserve every `run_script`, `subprocess ["python3", "modules/legacy/..."]` and `from modules.legacy...` call site without changes |

## How it works

`contrib/` is intentionally outside the packaged import roots in `pyproject.toml`, so quarantined code ships no new API surface. Compatibility is structural: symlinks plus a `__path__`-extending `modules/legacy/__init__.py` shim, not documentation promises.

## Adding X

Do not add maintained code here. To quarantine a module: `git mv <path> contrib/<area>/`, leave a symlink or thin shim at the old path, and document the old and new paths in this table.
