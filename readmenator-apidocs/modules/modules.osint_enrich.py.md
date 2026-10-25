# `modules.osint_enrich`

> Source: [modules/osint_enrich.py:1](../../modules/osint_enrich.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Keyless OSINT enrichment for finding evidence.

VirusTotal has no keyless API, so this module assembles the same answers
from sources that need no API key at all:

- CVE advisories: OSV (https://api.osv.dev, no key, POST).
- Exploited in the wild: CISA KEV catalog (public JSON feed, no key).
- Exploit probability: EPSS scores from FIRST (https://api.first.org, no key).
- Host intel: HackerTarget free endpoints + DNS-over-HTTPS + ip-api
  community rate limit (all keyless), urlscan.io public search (no key).

Every lookup is cached under ``sessions/osint_cache.json`` (7-day TTL,
KEV catalog 24h) and fails silent: enrichment must never break the loop.
Stdlib only (urllib).

## Contents

- **Functions:** [`cve_lookup`](#cve_lookup), [`reverse_dns`](#reverse_dns), [`host_geo`](#host_geo), [`domain_exposure`](#domain_exposure), [`enrich_evidence`](#enrich_evidence)
- **Constants:** [`CACHE_FILENAME`](#cache_filename)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_osint_enrich_py__enrich_evidence(["enrich_evidence"])
    n_modules_osint_enrich_py__cve_lookup(["cve_lookup"])
    n_modules_osint_enrich_py__enrich_evidence --> n_modules_osint_enrich_py__cve_lookup
```

## Functions

<a id="cve_lookup"></a>

### `cve_lookup`

`function` | [modules/osint_enrich.py:122](../../modules/osint_enrich.py#L122)

```python
def cve_lookup(cve_id: str, sessions_dir: str | Path = SESSIONS_DIR) -> dict
```

Assemble OSV advisory + KEV flag + EPSS score for one CVE id.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cve_id` | `str` |  |  |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |

**Returns:** `dict`

*Called by:* [`enrich_evidence`](#enrich_evidence)

---

<a id="reverse_dns"></a>

### `reverse_dns`

`function` | [modules/osint_enrich.py:161](../../modules/osint_enrich.py#L161)

```python
def reverse_dns(ip: str, sessions_dir: str | Path = SESSIONS_DIR) -> str
```

Best-effort PTR hostname for an IP (HackerTarget, then DoH).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip` | `str` |  |  |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |

**Returns:** `str`

---

<a id="host_geo"></a>

### `host_geo`

`function` | [modules/osint_enrich.py:183](../../modules/osint_enrich.py#L183)

```python
def host_geo(ip: str, sessions_dir: str | Path = SESSIONS_DIR) -> dict
```

Country/org/ISP for an IP via the keyless ip-api endpoint.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip` | `str` |  |  |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |

**Returns:** `dict`

---

<a id="domain_exposure"></a>

### `domain_exposure`

`function` | [modules/osint_enrich.py:198](../../modules/osint_enrich.py#L198)

```python
def domain_exposure(domain: str, sessions_dir: str | Path = SESSIONS_DIR) -> int
```

Count public urlscan.io results for a domain (no key needed).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `domain` | `str` |  |  |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |

**Returns:** `int`

---

<a id="enrich_evidence"></a>

### `enrich_evidence`

`function` | [modules/osint_enrich.py:213](../../modules/osint_enrich.py#L213)

```python
def enrich_evidence(items: list[str], sessions_dir: str | Path = SESSIONS_DIR) -> list[str]
```

Append keyless OSINT verdicts to CVE mentions inside evidence items.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `items` | `list[str]` |  |  |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |

**Returns:** `list[str]`

*Calls:* [`cve_lookup`](#cve_lookup)

---

## Constants

<a id="cache_filename"></a>

### `CACHE_FILENAME`

`constant` | [modules/osint_enrich.py:26](../../modules/osint_enrich.py#L26)

```python
CACHE_FILENAME = 'osint_cache.json'
```

---
