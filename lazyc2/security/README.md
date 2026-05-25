# C2 Security Layer

Security utilities and validators for the LazyOwn C2 server (`lazyc2.py`).

## Contents

| File | Purpose |
|------|---------|
| `constants.py` | Security-related constants (token lifetimes, rate-limit buckets, header names). |
| `validators.py` | Input validation helpers for C2 routes (beacon registration, file upload, operator commands). |
| `services.py` | Business-logic security services (JWT minting/verification, CSRF protection, audit logging). |

## Design

All C2 endpoints import from this package instead of embedding security logic inline. This keeps `lazyc2.py` focused on protocol handling while critical controls (authentication, authorization, sanitization) live here.

## Adding a new validator

1. Add the validation function to `validators.py`.
2. Import it in the C2 route module and call it at the top of the handler.
3. Raise `SecurityError` (defined in `services.py`) on failure so the error handler formats a consistent JSON response.
