# `modules.sinks.lazy_intel`

> Source: [modules/sinks/lazy_intel.py:1](../../modules/sinks/lazy_intel.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Lazy intel sink: mirror exploit-intelligence matches into the stores.

Every ``lazy_intel`` outcome event (one per exposure report, from
`[`modules.lazy_exposure.publish_report`](modules.lazy_exposure.py.md#publish_report)`) lands the bounded matches as

- WorldModel vulnerabilities with a CVE id so the ``/intel`` and
  ``/graphattack`` pages (which fuse ``sessions/world_model.json``)
  show the intelligence on the host finding nodes, and
- `[`modules.db`](modules.db.py.md)` workspace vuln rows (with cve, severity, references)
  so ``lazysearch``, ``db vulns`` and every SQLite consumer see it
  without re-running the matcher.

Prevents duplicate rows: a host/cve pair already in either store is
skipped. Sink is best-effort by contract; never raises.

## Contents

- **Functions:** [`apply`](#apply)

## Functions

<a id="apply"></a>

### `apply`

`function` | [modules/sinks/lazy_intel.py:28](../../modules/sinks/lazy_intel.py#L28)

```python
def apply(event: OutcomeEvent) -> bool
```

Mirror one lazy_intel event into the world model and the database.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `OutcomeEvent` |  | Outcome bus event of kind ``lazy_intel``. |

**Returns:** `bool` - True when at least one store accepted a write; False otherwise.

---
