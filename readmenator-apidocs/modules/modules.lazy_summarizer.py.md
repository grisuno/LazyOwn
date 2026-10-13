# `modules.lazy_summarizer`

> Source: [modules/lazy_summarizer.py:1](../../modules/lazy_summarizer.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Bounded chain summarizer for the Lazy autonomous loop.

Ports the durable idea behind context-chain summarization: keep the newest
section verbatim, compress older question/answer pairs into a digest, and
mark compressed regions with an explicit prefix so downstream readers know
they are reading a summary. Budgets are characters (cheap, dependency-free)
instead of tokens.

Stdlib only. An optional `[`complete`](modules.llm_factory.py.md#complete)` callable upgrades truncation digests
into model-written ones; without it the summarizer still bounds context.

## Contents

- **Functions:** [`should_compact`](#should_compact), [`summarize_chain`](#summarize_chain)
- **Constants:** [`LAZY_DIGEST_PREFIX`](#lazy_digest_prefix), [`MAX_LAST_SECTION_CHARS`](#max_last_section_chars), [`MAX_SINGLE_PAIR_CHARS`](#max_single_pair_chars), [`MAX_QA_SECTIONS`](#max_qa_sections), [`MAX_QA_CHARS`](#max_qa_chars), [`KEEP_MIN_QA_SECTIONS`](#keep_min_qa_sections), [`RESERVE_FRACTION`](#reserve_fraction)

## Functions

<a id="should_compact"></a>

### `should_compact`

`function` | [modules/lazy_summarizer.py:35](../../modules/lazy_summarizer.py#L35)

```python
def should_compact(used_chars: int, budget_chars: int) -> bool
```

Return True when context exceeds the usable budget.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `used_chars` | `int` |  | Current context size in characters. |
| `budget_chars` | `int` |  | Total context budget in characters. |

**Returns:** `bool` - True when the usable share (budget minus reserve) is exceeded.

---

<a id="summarize_chain"></a>

### `summarize_chain`

`function` | [modules/lazy_summarizer.py:50](../../modules/lazy_summarizer.py#L50)

```python
def summarize_chain(records: Sequence[Mapping], budget_chars: int = MAX_LAST_SECTION_CHARS * 2, complete: Callable[[str], str] | None = None) -> list[dict]
```

Bound a record chain to budget, digesting the oldest pairs.

The newest section (up to `[`MAX_LAST_SECTION_CHARS`](#max_last_section_chars)`) is preserved
verbatim. Older records collapse into digest records prefixed with
[`LAZY_DIGEST_PREFIX`](#lazy_digest_prefix), keeping at most `[`MAX_QA_SECTIONS`](#max_qa_sections)`
sections and `[`MAX_QA_CHARS`](#max_qa_chars)` characters of history.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `records` | `Sequence[Mapping]` |  | Activity records with worker/kind/text keys. |
| `budget_chars` | `int` | `MAX_LAST_SECTION_CHARS * 2` | Total character budget for the returned chain. |
| `complete` | `Callable[[str], str] \| None` | `None` | Optional model callable turning a truncation excerpt into a denser digest. Failures fall back to truncation. |

**Returns:** `list[dict]` - Bounded record list, oldest first, digests marked by prefix.

---

## Constants

<a id="lazy_digest_prefix"></a>

### `LAZY_DIGEST_PREFIX`

`constant` | [modules/lazy_summarizer.py:17](../../modules/lazy_summarizer.py#L17)

```python
LAZY_DIGEST_PREFIX = '[lazy digest]'
```

---

<a id="max_last_section_chars"></a>

### `MAX_LAST_SECTION_CHARS`

`constant` | [modules/lazy_summarizer.py:18](../../modules/lazy_summarizer.py#L18)

```python
MAX_LAST_SECTION_CHARS = 50 * 1024
```

---

<a id="max_single_pair_chars"></a>

### `MAX_SINGLE_PAIR_CHARS`

`constant` | [modules/lazy_summarizer.py:19](../../modules/lazy_summarizer.py#L19)

```python
MAX_SINGLE_PAIR_CHARS = 16 * 1024
```

---

<a id="max_qa_sections"></a>

### `MAX_QA_SECTIONS`

`constant` | [modules/lazy_summarizer.py:20](../../modules/lazy_summarizer.py#L20)

```python
MAX_QA_SECTIONS = 10
```

---

<a id="max_qa_chars"></a>

### `MAX_QA_CHARS`

`constant` | [modules/lazy_summarizer.py:21](../../modules/lazy_summarizer.py#L21)

```python
MAX_QA_CHARS = 64 * 1024
```

---

<a id="keep_min_qa_sections"></a>

### `KEEP_MIN_QA_SECTIONS`

`constant` | [modules/lazy_summarizer.py:22](../../modules/lazy_summarizer.py#L22)

```python
KEEP_MIN_QA_SECTIONS = 1
```

---

<a id="reserve_fraction"></a>

### `RESERVE_FRACTION`

`constant` | [modules/lazy_summarizer.py:23](../../modules/lazy_summarizer.py#L23)

```python
RESERVE_FRACTION = 0.25
```

---
