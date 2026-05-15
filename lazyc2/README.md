# lazyc2

Supplementary C2 layer components. This directory contains security validation
helpers and supporting code used by `lazyc2.py` but kept in a separate package
to maintain a clean separation of concerns.

The primary C2 server implementation lives in the root-level `lazyc2.py`.
This directory holds code that `lazyc2.py` imports — it is not a standalone
server.

## Subdirectories

| Directory | Contents |
|-----------|---------|
| `security/` | Input validation, path safety checks, and rate-limiting helpers used by C2 routes. |

## lazyc2/security

| File | Purpose |
|------|---------|
| `validators.py` | Route-level validation: `validate_route_path`, `validate_template_name`, `is_safe_template_path`. Called before any `render_template` or file-serving operation to prevent path traversal. |
| `services.py` | Security service classes: request origin checking (operator vs non-operator IP), token validation, and auth middleware helpers. |
| `constants.py` | Security-related constants: allowed template name patterns, maximum upload sizes, rate-limit defaults. |
| `__init__.py` | Re-exports the validators and services for easy import in `lazyc2.py`. |

## Path safety contract

Every route that renders a user-influenced template name must call:

```python
from lazyc2.security import validate_template_name, is_safe_template_path

if not validate_template_name(name):
    return error_response("invalid template name", 400)
if not is_safe_template_path(name):
    return error_response("path traversal denied", 400)
```

This is enforced in code review. Routes that bypass these checks are
rejected.
