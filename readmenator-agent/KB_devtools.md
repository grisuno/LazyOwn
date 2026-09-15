# Subsystem: devtools

## scripts/devtools/command_audit.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `AuditConfig` (class, line 25) `class AuditConfig`
  - `argparser_commands` (method, line 40) `def argparser_commands(config)`
  - `audit` (method, line 65) `def audit(config)`
  - `main` (method, line 105) `def main(argv)`
- Depends on: `lazyown.py`

## scripts/devtools/core_smoke.py
- Layer: utility
- Language: py
- Symbols:
  - `SmokeConfig` (class, line 20) `class SmokeConfig`
  - `check_surfaces` (method, line 64) `def check_surfaces(config)`
  - `check_calls` (method, line 81) `def check_calls()`
  - `main` (method, line 118) `def main()`
- Depends on: `core/hardening.py`, `core/payload_schema.py`, `modules/db.py`, `modules/killchain.py`, `modules/payload_factory.py`
