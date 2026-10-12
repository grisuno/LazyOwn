# `lazyc2.blueprints.session_auth`

> Source: [lazyc2/blueprints/session_auth.py:1](../../lazyc2/blueprints/session_auth.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Session-based authentication gate for operator dashboard blueprints.

Some dashboard blueprints (tasks, addons, notes) were previously
protected only by the decoy IP check, so any request arriving from the
operator IP could read operator data without a login session. This
module closes that gap with a single reusable guard: every route on a
guarded blueprint requires an authenticated Flask-Login session, and
unauthenticated requests are redirected to the login page.

Implant-facing blueprints (beacons, phishing redirects, health APIs)
must NOT use this gate.

## Contents

- **Functions:** [`require_operator_session`](#require_operator_session)

## Functions

<a id="require_operator_session"></a>

### `require_operator_session`

`function` | [lazyc2/blueprints/session_auth.py:20](../../lazyc2/blueprints/session_auth.py#L20)

```python
def require_operator_session(blueprint: Blueprint, login_endpoint: str = 'login') -> None
```

Register a ``before_request`` guard on a blueprint.

All routes on the guarded blueprint serve operator-only content, so
the guard treats every method the same way. The per-view decoy and
CSRF layers keep running after the session check.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `blueprint` | `Blueprint` |  | The Flask blueprint to protect. |
| `login_endpoint` | `str` | `'login'` | Endpoint name the login redirect targets. |

---
