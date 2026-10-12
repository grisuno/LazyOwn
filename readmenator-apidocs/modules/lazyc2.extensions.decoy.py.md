# `lazyc2.extensions.decoy`

> Source: [lazyc2/extensions/decoy.py:1](../../lazyc2/extensions/decoy.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Decoy / honeypot page for unauthenticated visitors.

When a request comes from an IP that is not the operator's lhost the
C2 renders a decoy HTML page instead of the real interface.

## Contents

- **Functions:** [`decoy_response`](#decoy_response)

## Functions

<a id="decoy_response"></a>

### `decoy_response`

`function` | [lazyc2/extensions/decoy.py:12](../../lazyc2/extensions/decoy.py#L12)

```python
def decoy_response() -> str | None
```

Return a decoy page when the client IP is not the operator host.

Reads ``lhost`` from ``current_app.config`` and compares it
against ``request.remote_addr``. Returns the rendered ``decoy.html``
template when they differ, or ``None`` when the client is allowed.

**Returns:** `str | None` - Rendered decoy template string or ``None``.

*Called by:* [`create_addon`](lazyc2.blueprints.addons.py.md#create_addon), [`delete_addon`](lazyc2.blueprints.addons.py.md#delete_addon), [`list_addons`](lazyc2.blueprints.addons.py.md#list_addons), [`view_addon`](lazyc2.blueprints.addons.py.md#view_addon), [`admin_tenants`](lazyc2.blueprints.auth.py.md#admin_tenants), [`admin_users`](lazyc2.blueprints.auth.py.md#admin_users), [`login`](lazyc2.blueprints.auth.py.md#login), [`logout`](lazyc2.blueprints.auth.py.md#logout), [`mfa_setup`](lazyc2.blueprints.auth.py.md#mfa_setup), [`mfa_verify`](lazyc2.blueprints.auth.py.md#mfa_verify), [`profile`](lazyc2.blueprints.auth.py.md#profile), [`register`](lazyc2.blueprints.auth.py.md#register) and 12 more

---
