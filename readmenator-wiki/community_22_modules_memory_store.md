# modules: memory_store

*Community 22 | 3 files | cohesion 1.00*

## Definition

This community groups 3 file(s) rooted at `modules` with dominant language py (cohesion 1.00). Central symbols: `EmbeddingError`, `MemoryEntry`, `MemoryStore`, `SQLiteBackend`, `StorageBackend`, `TestHashingEmbedder`, `TestMemoryStoreHybrid`, `TestVectorSQLiteBackend`. Core file: `modules/memory_store.py` (38 symbols). Documented purpose: Hashing-trick text embeddings for episodic memory recall.  Zero-dependency semantic search: every command + output + findings block is mapped onto a sparse 512-.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/memory_embeddings.py` | py | utility | 7 | yes |
| `modules/memory_store.py` | py | data_access | 38 | yes |
| `tests/test_memory_semantics.py` | py | testing | 14 | yes |

## Key Symbols

- `EmbeddingError` (class, `modules/memory_embeddings.py:30`) `class EmbeddingError(ValueError)` - Raised when callers pass unusable text to the embedder.
- `_fnv1a` (function, `modules/memory_embeddings.py:34`) `def _fnv1a(data)`
- `_tokens` (function, `modules/memory_embeddings.py:41`) `def _tokens(text)`
- `embed` (function, `modules/memory_embeddings.py:50`) `def embed(text)` - Map text to a normalised 512-float histogram BLOB.
- `cosine` (function, `modules/memory_embeddings.py:75`) `def cosine(a, b)` - Cosine similarity of two embedding BLOBs; legacy/partial input -> 0.0.
- `semantic_top_k` (function, `modules/memory_embeddings.py:85`) `def semantic_top_k(query, candidates, top_k)` - Rank candidate (id, embedding) pairs against the query.
- `as_floats` (function, `modules/memory_embeddings.py:109`) `def as_floats(blob)` - Decode a BLOB into a mutable float array (diagnostics/tests).
- `MemoryEntry` (class, `modules/memory_store.py:84`) `class MemoryEntry`
- `StorageBackend` (class, `modules/memory_store.py:97`) `class StorageBackend(ABC)`
- `save` (method, `modules/memory_store.py:99`) `def save(self, entry)`
- `search` (method, `modules/memory_store.py:102`) `def search(self, query, top_k)`
- `by_host` (method, `modules/memory_store.py:105`) `def by_host(self, host, top_k)`
- `by_service` (method, `modules/memory_store.py:108`) `def by_service(self, service, top_k)`
- `all_entries` (method, `modules/memory_store.py:111`) `def all_entries(self, limit)`
- `close` (method, `modules/memory_store.py:114`) `def close(self)`
- `_row_to_entry` (function, `modules/memory_store.py:117`) `def _row_to_entry(row)`
- `SQLiteBackend` (class, `modules/memory_store.py:132`) `class SQLiteBackend(StorageBackend)`
- `__init__` (method, `modules/memory_store.py:133`) `def __init__(self, db_path)`
- `_connect` (method, `modules/memory_store.py:139`) `def _connect(self)`
- `save` (method, `modules/memory_store.py:148`) `def save(self, entry)`
- `_fetch` (method, `modules/memory_store.py:175`) `def _fetch(self, sql, params)`
- `search` (method, `modules/memory_store.py:180`) `def search(self, query, top_k)`
- `by_host` (method, `modules/memory_store.py:192`) `def by_host(self, host, top_k)`
- `by_service` (method, `modules/memory_store.py:203`) `def by_service(self, service, top_k)`
- `all_entries` (method, `modules/memory_store.py:215`) `def all_entries(self, limit)`
- `stats_raw` (method, `modules/memory_store.py:225`) `def stats_raw(self)`
- `close` (method, `modules/memory_store.py:232`) `def close(self)`
- `MemoryStore` (class, `modules/memory_store.py:237`) `class MemoryStore`
- `__init__` (method, `modules/memory_store.py:240`) `def __init__(self, backend)`
- `remember` (method, `modules/memory_store.py:243`) `def remember(self, session_id, host, tool, command, output, findings, success)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 3
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: memory_store changed?
- Should modules: memory_store be split, given cohesion 1.00?

## Sources

- `modules/memory_embeddings.py`
- `modules/memory_store.py`
- `tests/test_memory_semantics.py`
