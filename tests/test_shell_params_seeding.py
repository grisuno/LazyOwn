"""Regression guard: the shell seeds ``self.params`` from the one config source.

``LazyOwnShell.__init__`` used to hard-code a ~70-key default params dict that
duplicated :data:`core.payload_schema.SCHEMA` and drifted from it (for example
``sleep_start`` was 207 while the schema and ``payload.json`` agreed on 333,
and ``os_id`` was pinned to "2" while ``payload.json`` said "1"). That broke
the CLAUDE.md contract that ``self.params`` mirrors ``payload.json``: operator
values persisted via ``assign`` were silently reset to the literals on the next
shell start.

The shell now seeds params as ``{**default_payload(), **load_payload()}`` so the
schema supplies defaults and ``payload.json`` is authoritative. These tests pin
both the merge contract and the absence of the old literal dict.
"""

from __future__ import annotations

from pathlib import Path

from core.config import load_payload
from core.payload_schema import SCHEMA, default_payload

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_SOURCE = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")


def test_merge_mirrors_payload_over_schema_defaults() -> None:
    """Every payload.json key wins; schema fills the rest."""
    payload = load_payload()
    merged = {**default_payload(), **payload}
    for key, value in payload.items():
        assert merged[key] == value, f"{key} must mirror payload.json"
    for key in SCHEMA:
        assert key in merged, f"{key} must be seeded from the schema defaults"


def test_merge_covers_every_schema_key() -> None:
    """The seed exposes the full schema surface, not a hand-picked subset."""
    merged = {**default_payload(), **load_payload()}
    assert set(SCHEMA).issubset(merged)


def test_shell_seeds_params_from_config_source() -> None:
    """The shell constructs params from the schema+payload merge."""
    assert "self.params = {**default_payload(), **load_payload()}" in LAZYOWN_SOURCE


def test_shell_no_longer_hardcodes_drifted_literals() -> None:
    """The removed literal defaults must not creep back into the shell."""
    for forbidden in ('"sleep_start": 207', '"os_id": "2"', '"c2_malleable_route": "/gmail'):
        assert forbidden not in LAZYOWN_SOURCE, f"stale literal default re-introduced: {forbidden}"
