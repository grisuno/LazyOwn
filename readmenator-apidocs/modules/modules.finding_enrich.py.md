# `modules.finding_enrich`

> Source: [modules/finding_enrich.py:1](../../modules/finding_enrich.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Idempotent enrichment of a finding's evidence before it is reported.

A finding accrues traffic evidences one bind at a time, in whatever order the
loop happened to prove them: duplicates creep in when the same exchange is
bound twice, and the strongest proof can sit below weaker supporting rows. This
module canonicalises that set once, deterministically, so a report always shows
the proof first and never twice.

The pass is pure and idempotent: it ranks evidences by role, collapses repeated
digests onto their strongest role, and derives a content-only enrichment digest
from the result. Running it again over an already-enriched finding yields the
same ordering and the same digest, so it is safe to call on every bind without
ever compounding. Nothing here imports the loop runtime, keeping it cycle-free
and testable in isolation.

## Contents

- **Functions:** [`enrich_refs`](#enrich_refs), [`enrich_finding`](#enrich_finding)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_finding_enrich_py__enrich_finding(["enrich_finding"])
    n_modules_finding_enrich_py__enrich_refs(["enrich_refs"])
    n_modules_finding_enrich_py__enrich_finding --> n_modules_finding_enrich_py__enrich_refs
```

## Functions

<a id="enrich_refs"></a>

### `enrich_refs`

`function` | [modules/finding_enrich.py:44](../../modules/finding_enrich.py#L44)

```python
def enrich_refs(refs: list[dict[str, Any]]) -> dict[str, Any]
```

Canonicalise evidence refs into a stable, deduplicated ordering.

Duplicate digests are collapsed onto their strongest role, then every
surviving ref is ordered by role strength with the digest as a stable
tie-break, so the same inputs in any order produce one identical result.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `refs` | `list[dict[str, Any]]` |  | Evidence refs as stored on a finding, each carrying at least a `[`digest`](modules.loop.decision_log.py.md#digest)` and optionally ``role``, ``note`` and ``ts``. |

**Returns:** `dict[str, Any]` - A result dict with the canonical `[`refs`](modules.finding_lifecycle.py.md#findingrecord-refs)` list, the `[`digest`](modules.loop.decision_log.py.md#digest)` of that
canonical form, a `[`count`](modules.lazy_creds.py.md#count)` of distinct evidences and ``roles``, a
role-to-count tally.

*Called by:* [`enrich_finding`](#enrich_finding)

---

<a id="enrich_finding"></a>

### `enrich_finding`

`function` | [modules/finding_enrich.py:96](../../modules/finding_enrich.py#L96)

```python
def enrich_finding(traffic_log: Any, finding_id: int, graph: Any) -> dict[str, Any]
```

Enrich one finding's stored evidence in place, idempotently.

The finding's evidence refs are canonicalised and written back only when
the enrichment digest changes, so a finding already in canonical form is
never rewritten and its ``evidence_version`` never churns.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `traffic_log` | `Any` |  | The [`modules.lazy_loop.TrafficLog`](modules.lazy_loop.py.md#trafficlog) owning the refs. |
| `finding_id` | `int` |  | The finding node id to enrich. |
| `graph` | `Any` |  | The exploration graph holding the finding. |

**Returns:** `dict[str, Any]` - A result dict with `[`ok`](scripts.top_tier_check.py.md#ok)`, and either the enrichment summary (`[`digest`](modules.loop.decision_log.py.md#digest)`,
`[`count`](modules.lazy_creds.py.md#count)`, ``roles``, `[`changed`](modules.LazyOwnExplorer.py.md#autocompleteentry-changed)`) or an ``error``.

*Calls:* [`enrich_refs`](#enrich_refs)

---
