# `modules.selection.cred_spray`

> Source: [modules/selection/cred_spray.py:1](../../modules/selection/cred_spray.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Credential-spray selector: reuse known credentials against open services.

Single contract: when usable credentials exist and a service that accepts them
is open, propose the service-appropriate LazyOwn verb (which reads the target
and credentials from ``payload.json``). Gated to post-recon phases where
credential reuse is meaningful. Migrated from the daemon's inline selector so
both autonomous runtimes share one implementation.

## Contents

- **Classes:** [`CredentialSpraySelector`](#credentialsprayselector)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_selection_cred_spray_py__CredentialSpraySelector_propose(["CredentialSpraySelector.propose"])
    n_modules_selection_base_py__ActionDecision["base.ActionDecision"]
    n_modules_selection_cred_spray_py__CredentialSpraySelector_propose -.-> n_modules_selection_base_py__ActionDecision
```

## Classes

<a id="credentialsprayselector"></a>

### `CredentialSpraySelector`

`class` | [modules/selection/cred_spray.py:32](../../modules/selection/cred_spray.py#L32)

```python
class CredentialSpraySelector
```

Propose a credential-reuse verb for an open service when creds exist.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`name`](#credentialsprayselector-name) |  | `'cred_spray'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`propose`](#credentialsprayselector-propose) | method | Return a spray verb for the first matching open service, or None. |

<a id="credentialsprayselector-propose"></a>

#### `CredentialSpraySelector.propose`

`method` | [modules/selection/cred_spray.py:37](../../modules/selection/cred_spray.py#L37)

```python
def propose(self, ctx: SelectionContext) -> ActionDecision | None
```

Return a spray verb for the first matching open service, or None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ctx` | `SelectionContext` |  |  |

**Returns:** `ActionDecision | None`

*Calls:* [`ActionDecision`](modules.selection.base.py.md#actiondecision)

---
