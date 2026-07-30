# Changelog

## [0.2.157] - 2026-07-29

### Added
- Unified dashboard with live topology graph and exploit suggester
- Banners and reports API endpoints
- `engage` one-command fast-path (ping -> lazynmap -> auto_populate -> enum -> exploit)
- `orchestrate` free-text goal routing (daemon, hive, swan backends)
- `hunt` command for active vulnerability hunting
- `chain` command for exploit chaining
- YARA rules for beacon/payload detection (5 rules)
- Dynamic shellcode patch: native x64 reverse shell without msfvenom (~104 bytes, null-free, XOR dynamic)
- DB migration system (v2-v4): indices, cracked_at, performance optimizations
- MCP dispatch table: O(1) tool handler lookup via `_TOOL_HANDLERS` dict
- Cloud attack modules (AWS, Azure, GCP) and Kubernetes attack modules
- Phantom2 stealthy C implant with io_uring, encrypted C2, persistence, keylogger
- fakesystemD: self-contained systemd D-Bus + sd_notify emulation
- TUI themes (solarized, monokai, gruvbox, high_contrast) with `tui_theme` command
- Animated splash overlay for first-run experience
- `doctor` preflight check command
- CommandSet migration framework with dormancy/pending coexistence
- CLI print hygiene: removed C2 credential leak in shell output

### Changed
- Monolith `lazyown.py` deconstructed from ~24,900 to ~4,500 lines via CLI CommandSets
- `lazyc2.py` extracted: `state.py`, `models.py`, `app_factory.py`, security modules
- `utils.py` wildcard import replaced with 66 explicit symbols
- README truncated from 20k to 2.1k lines
- Heavy imports deferred from module-level to `__init__` time for faster startup
- 281 ruff issues auto-fixed in `core/` and `cli/`

### Fixed
- Security advisories: debug data leaks in print statements
- CVE-2026-25089 FortiClient integration
- Payload generation refactors and bug fixes

### Dependencies
- pyarrow 24.0.0 -> 25.0.0
- cffi 2.0.0 -> 2.1.0
- pyelftools 0.32 -> 0.33
- argcomplete 3.6.3 -> 3.7.0
- tqdm 4.67.3 -> 4.69.1
- setuptools 81.0.0 -> 83.0.0
- torch 2.12.1 -> 2.13.0
- Added: mcp>=1.0.0, textual
