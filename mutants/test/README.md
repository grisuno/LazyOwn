# Legacy Test Directory

This directory contains the earliest test fixtures. New tests should be added to `tests/` at the repository root, which is the canonical location for the pytest suite.

## Contents

| File | Purpose |
|------|---------|
| `config.py` | Shared pytest configuration and fixtures (legacy). |

## Migration Note

Tests in this directory are kept for backward compatibility. When modifying them, consider migrating the logic to `tests/` and updating any relative imports.
