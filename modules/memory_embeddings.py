"""Hashing-trick text embeddings for episodic memory recall.

Zero-dependency semantic search: every command + output + findings block
is mapped onto a sparse 512-float histogram with an FNV-1a token hash and
pronominal hashing (three token n-gram buckets per token) for light
fuzziness. Vectors are L2-normalised and stored as little-endian floats
in the ``memories.embedding`` BLOB that has been dead weight until now.
Recall compares cosine similarity — no model download, deterministic
across runs, constant memory.
"""

from __future__ import annotations

import array
import math
import re
import struct
from typing import Sequence

_DIM = 512
_TOKEN_MIN_LEN = 2
_BIGRAM_STEP = 1
_FNV_OFFSET = 0x811C9DC5
_FNV_PRIME = 0x01000193
_FLOAT_FMT = "<%df" % _DIM
_CHAR_ANALOG = re.compile(r"[^a-zA-Z0-9_]+")
_MIN_COSINE = 0.10


class EmbeddingError(ValueError):
    """Raised when callers pass unusable text to the embedder."""


def _fnv1a(data: bytes) -> int:
    value = _FNV_OFFSET
    for byte in data:
        value = ((value ^ byte) * _FNV_PRIME) & 0xFFFFFFFF
    return value


def _tokens(text: str) -> list[str]:
    raw = _CHAR_ANALOG.sub(" ", text.lower()).split()
    words = [tok for tok in raw if len(tok) >= _TOKEN_MIN_LEN]
    grams: list[str] = []
    for index in range(0, max(0, len(words) - 1), _BIGRAM_STEP):
        grams.append(f"{words[index]}_{words[index + 1]}")
    return words + grams


def embed(text: str) -> bytes:
    """Map text to a normalised 512-float histogram BLOB.

    Args:
        text: Raw text (command, output snippet, findings...).

    Returns:
        Deterministic little-endian float32 BLOB of exactly _DIM values.

    Raises:
        EmbeddingError: When text is empty or contains no bytes.
    """
    if not isinstance(text, str) or not text.strip():
        raise EmbeddingError("cannot embed empty text")
    vec = [0.0] * _DIM
    tokens = _tokens(text)
    for token in tokens:
        value = _fnv1a(token.encode("utf-8"))
        vec[value % _DIM] += 1.0
        vec[(value >> 11) % _DIM] += 0.5
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    vec = [v / norm for v in vec]
    return struct.pack(_FLOAT_FMT, *vec)


def cosine(a: bytes, b: bytes) -> float:
    """Cosine similarity of two embedding BLOBs; legacy/partial input -> 0.0."""
    try:
        left = struct.unpack(_FLOAT_FMT, a)
        right = struct.unpack(_FLOAT_FMT, b)
    except (struct.error, TypeError, ValueError, AttributeError):
        return 0.0
    return sum(l * r for l, r in zip(left, right))


def semantic_top_k(
    query: str,
    candidates: Sequence[tuple[int, bytes]],
    top_k: int,
) -> list[tuple[int, float]]:
    """Rank candidate (id, embedding) pairs against the query.

    Args:
        query: Natural-language query text.
        candidates: Pairs of row id and stored embedding BLOB.
        top_k: Maximum number of matches to return.

    Returns:
        Matches with cosine >= _MIN_COSINE, best first, capped at top_k.
    """
    if not query.strip() or top_k <= 0:
        return []
    qvec = embed(query)
    scored = [(cid, cosine(qvec, blob)) for cid, blob in candidates if blob]
    scored = [(cid, score) for cid, score in scored if score >= _MIN_COSINE]
    scored.sort(key=lambda item: -item[1])
    return scored[:top_k]


def as_floats(blob: bytes) -> "array.array":
    """Decode a BLOB into a mutable float array (diagnostics/tests)."""
    values = struct.unpack(_FLOAT_FMT, blob)
    out = array.array("f", values)
    return out
