"""Tests for modules.lazypassgen — target-aware weak-password generator.

Covers:
    - Entity splitting and mutant generation
    - Leet and temporal mutations
    - Default-credential seeds from lazycreds
    - Export artefact
    - Empty-target guards
"""

from __future__ import annotations

import pytest


@pytest.fixture
def passgen():
    from modules import lazypassgen

    return lazypassgen


class TestLazyPassGen:
    def test_split_entities(self, passgen):
        words = passgen._split_entities("CORP-Example.local")
        assert "corp" in words and "example" in words

    def test_split_skip_short_words(self, passgen):
        words = passgen._split_entities("ab cd Corp")
        assert words == ("corp",)

    def test_generate_target_words(self, passgen):
        result = passgen.generate("acme")
        assert "acme2026" in result["passwords"]
        assert "Acme" in result["passwords"]

    def test_generate_leet(self, passgen):
        result = passgen.generate("test")
        assert "t3$t" in result["passwords"]

    def test_generate_seasons(self, passgen):
        result = passgen.generate("acme")
        assert "acmesummer" in result["passwords"]

    def test_generate_empty_target(self, passgen):
        result = passgen.generate("!!")
        assert result["total"] == 0
        assert result["passwords"] == ()

    def test_generate_cap(self, passgen):
        result = passgen.generate("very long company name that keeps going and going")
        assert len(result["passwords"]) <= passgen.MAX_MUTATIONS

    def test_seeds_use_lazy_creds(self, passgen):
        result = passgen.generate("acme")
        assert isinstance(result["frequent_seeds"], tuple)

    def test_export(self, passgen, tmp_path):
        destination = tmp_path / "wordlist.txt"
        result = passgen.export("acme", destination)
        assert result["error"] == ""
        lines = destination.read_text(encoding="utf-8").splitlines()
        assert result["written"] == len(lines) > 0

    def test_export_empty(self, passgen, tmp_path):
        destination = tmp_path / "wordlist.txt"
        result = passgen.export("+(", destination)
        assert result["error"] == "empty target"
        assert not destination.exists()
