# Subsystem: modules (page 16 of 16)
Previous: [KB_modules_p15.md](KB_modules_p15.md)

## modules/yara_scanner.py
- Doc: YARA integration for malware classification and IOC scanning.
- Layer: utility
- Language: py
- Symbols:
  - `YaraScanner` (class, line 23) `class YaraScanner`
  - `create_default_rules` (function, line 371) `def create_default_rules()`
  - `__init__` (method, line 31) `def __init__(self, rules_dir, auto_compile)`
  - `ensure_directory` (method, line 41) `def ensure_directory(self)`
  - `_load_external_vars` (method, line 45) `def _load_external_vars(self)`
  - `compile_all` (method, line 54) `def compile_all(self)`
  - `scan_file` (method, line 98) `def scan_file(self, filepath, timeout)`
  - `_scan_with_timeout` (method, line 129) `def _scan_with_timeout(self, filepath, externals, timeout)`
  - `_format_match` (method, line 162) `def _format_match(self, match)`
  - `scan_directory` (method, line 187) `def scan_directory(self, directory, recursive, extensions, max_files)`
  - `_sha256` (method, line 250) `def _sha256(filepath)`
  - `add_rule` (method, line 258) `def add_rule(self, name, content)`
  - `list_rules` (method, line 277) `def list_rules(self)`
  - `download_community_rules` (method, line 300) `def download_community_rules(self)`
  - `ioc_scan` (method, line 328) `def ioc_scan(self, target_path, iocs)`
  - `target` (function, line 137) `def target()`
- Imported by: `cli/commands/postexp_migrated.py`, `modules/intelligence_engine.py`

