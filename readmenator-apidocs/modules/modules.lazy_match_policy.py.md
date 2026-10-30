# `modules.lazy_match_policy`

> Source: [modules/lazy_match_policy.py:1](../../modules/lazy_match_policy.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Match policy doctrine: what may claim a match and what stays a lead.

Adapted from the evidence-driven matching doctrine: a match needs the
same product and a version inside a bounded affected range; everything
else is a lead, evidence attaches to matches but never creates them,
and anything a human, template or retest touched never auto-closes.

Core state machine:

- ``match`` — version known, inside a bounded range.
- ``lead`` — product seen without any version; dedupe keeps the best
  sighting, OS sightings never name a version.
- ``version_unknown`` — non-bounded evidence (EOL branch, no bound),
  capped score, human closure only.
- Closures persist their reason and reopen only on new evidence.
- `[`has_standing`](#has_standing)` protects remediated/dialed rows: auto-merge skips.

## Contents

- **Classes:** [`MatchStore`](#matchstore)
- **Functions:** [`strand_from_sighting`](#strand_from_sighting), [`is_os_sighting`](#is_os_sighting), [`has_standing`](#has_standing)
- **Constants:** [`MATCH`](#match), [`LEAD`](#lead), [`VERSION_UNKNOWN`](#version_unknown), [`LEAD_SCORE_CAP`](#lead_score_cap), [`MATCH_SCORE_CAP`](#match_score_cap), [`UNKNOWN_SCORE_CAP`](#unknown_score_cap), [`STORE_FILENAME`](#store_filename)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lazy_match_policy_py__MatchStore_upsert(["MatchStore.upsert"])
    n_modules_lazy_match_policy_py__strand_from_sighting(["strand_from_sighting"])
    n_modules_lazy_match_policy_py__MatchStore_upsert --> n_modules_lazy_match_policy_py__strand_from_sighting
```

## Classes

<a id="matchstore"></a>

### `MatchStore`

`class` | [modules/lazy_match_policy.py:124](../../modules/lazy_match_policy.py#L124)

```python
class MatchStore
```

Bounded JSON registry of matches and leads with closure audit.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#matchstore-__init__) | constructor | Bind the store file under sessions/lazy. |
| [`upsert`](#matchstore-upsert) | method | Record one sighting under the dedupe identity. |
| [`rows`](#matchstore-rows) | method | Return every stored row. |
| [`close`](#matchstore-close) | method | Close one row, keeping its reason and reopening block. |
| [`closed_reason`](#matchstore-closed_reason) | method | Return the persisted closure reason, or '' when open or unknown. |

<a id="matchstore-__init__"></a>

#### `MatchStore.__init__`

`constructor` | [modules/lazy_match_policy.py:127](../../modules/lazy_match_policy.py#L127)

```python
def __init__(self, sessions_dir: str | Path | None = None) -> None
```

Bind the store file under sessions/lazy.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_dir` | `str \| Path \| None` | `None` |  |

<a id="matchstore-upsert"></a>

#### `MatchStore.upsert`

`method` | [modules/lazy_match_policy.py:132](../../modules/lazy_match_policy.py#L132)

```python
def upsert(self, identity: dict[str, Any], sighting: dict[str, Any], now: float | None = None) -> dict[str, Any]
```

Record one sighting under the dedupe identity.

Known-version sightings win over bare leads; a better row
replaces a worse one. The operator's standing blocks overwrite.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `identity` | `dict[str, Any]` |  | Match identity fields. |
| `sighting` | `dict[str, Any]` |  | One product sighting shaped for [`strand_from_sighting`](#strand_from_sighting). |
| `now` | `float \| None` | `None` | Reference epoch for timeline stamps. |

**Returns:** `dict[str, Any]` - The row after the update.

*Calls:* [`strand_from_sighting`](#strand_from_sighting)

<a id="matchstore-rows"></a>

#### `MatchStore.rows`

`method` | [modules/lazy_match_policy.py:177](../../modules/lazy_match_policy.py#L177)

```python
def rows(self) -> dict[str, dict[str, Any]]
```

Return every stored row.

**Returns:** `dict[str, dict[str, Any]]`

<a id="matchstore-close"></a>

#### `MatchStore.close`

`method` | [modules/lazy_match_policy.py:181](../../modules/lazy_match_policy.py#L181)

```python
def close(self, identity: dict[str, Any], reason: str, now: float | None = None) -> dict
```

Close one row, keeping its reason and reopening block.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `identity` | `dict[str, Any]` |  |  |
| `reason` | `str` |  |  |
| `now` | `float \| None` | `None` |  |

**Returns:** `dict`

<a id="matchstore-closed_reason"></a>

#### `MatchStore.closed_reason`

`method` | [modules/lazy_match_policy.py:196](../../modules/lazy_match_policy.py#L196)

```python
def closed_reason(self, identity: dict[str, Any]) -> str
```

Return the persisted closure reason, or '' when open or unknown.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `identity` | `dict[str, Any]` |  |  |

**Returns:** `str`

---

## Functions

<a id="strand_from_sighting"></a>

### `strand_from_sighting`

`function` | [modules/lazy_match_policy.py:37](../../modules/lazy_match_policy.py#L37)

```python
def strand_from_sighting(sighting: dict[str, Any]) -> str
```

Classify one product sighting per the doctrine.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sighting` | `dict[str, Any]` |  | ``{"product", "version", "os": bool, "ranges": dict, "kev_nobound": bool}``. |

**Returns:** `str` - One of MATCH, LEAD, VERSION_UNKNOWN.

*Called by:* [`MatchStore.upsert`](#matchstore-upsert)

---

<a id="is_os_sighting"></a>

### `is_os_sighting`

`function` | [modules/lazy_match_policy.py:79](../../modules/lazy_match_policy.py#L79)

```python
def is_os_sighting(product: str, cpe: str = '') -> bool
```

Return True when the sighting names an operating system.

OS names never headline version matches: nmap OS CPE plus a
product name is still an OS sighting.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `product` | `str` |  | Product text. |
| `cpe` | `str` | `''` | Optional CPE string. |

**Returns:** `bool` - True for obvious OS identities.

---

<a id="has_standing"></a>

### `has_standing`

`function` | [modules/lazy_match_policy.py:107](../../modules/lazy_match_policy.py#L107)

```python
def has_standing(match: dict[str, Any]) -> bool
```

Return True when humans or durable evidence touched a match.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `match` | `dict[str, Any]` |  | Match row carrying an ``evidence``/`[`timeline`](modules.operation.py.md#operationmanager-timeline)` list. |

**Returns:** `bool` - True when any standing kind appears in the row.

---

## Constants

<a id="match"></a>

### `MATCH`

`constant` | [modules/lazy_match_policy.py:26](../../modules/lazy_match_policy.py#L26)

```python
MATCH = 'match'
```

---

<a id="lead"></a>

### `LEAD`

`constant` | [modules/lazy_match_policy.py:27](../../modules/lazy_match_policy.py#L27)

```python
LEAD = 'lead'
```

---

<a id="version_unknown"></a>

### `VERSION_UNKNOWN`

`constant` | [modules/lazy_match_policy.py:28](../../modules/lazy_match_policy.py#L28)

```python
VERSION_UNKNOWN = 'version_unknown'
```

---

<a id="lead_score_cap"></a>

### `LEAD_SCORE_CAP`

`constant` | [modules/lazy_match_policy.py:29](../../modules/lazy_match_policy.py#L29)

```python
LEAD_SCORE_CAP = 2
```

---

<a id="match_score_cap"></a>

### `MATCH_SCORE_CAP`

`constant` | [modules/lazy_match_policy.py:30](../../modules/lazy_match_policy.py#L30)

```python
MATCH_SCORE_CAP = 100
```

---

<a id="unknown_score_cap"></a>

### `UNKNOWN_SCORE_CAP`

`constant` | [modules/lazy_match_policy.py:31](../../modules/lazy_match_policy.py#L31)

```python
UNKNOWN_SCORE_CAP = 2
```

---

<a id="store_filename"></a>

### `STORE_FILENAME`

`constant` | [modules/lazy_match_policy.py:32](../../modules/lazy_match_policy.py#L32)

```python
STORE_FILENAME = 'match_policy.json'
```

---
