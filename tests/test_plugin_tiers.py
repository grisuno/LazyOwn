"""Tests for marketplace plugin tiers and operator ratings."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from cli.plugin_tiers import (
    TIER_COMMUNITY,
    TIER_EXPERIMENTAL,
    TIER_OFFICIAL,
    format_rating,
    load_tier_manifest,
    rate_plugin,
    rating_summary,
    read_metadata_tier,
    tier_of,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_tier_constants() -> None:
    assert (TIER_OFFICIAL, TIER_COMMUNITY, TIER_EXPERIMENTAL) == ("official", "community", "experimental")


def test_manifest_overrides_metadata() -> None:
    assert tier_of("x", {"x": TIER_OFFICIAL}, TIER_EXPERIMENTAL) == TIER_OFFICIAL


def test_metadata_tier_used_without_manifest() -> None:
    assert tier_of("x", {}, TIER_EXPERIMENTAL) == TIER_EXPERIMENTAL


def test_default_tier_is_community() -> None:
    assert tier_of("unknown") == TIER_COMMUNITY
    assert tier_of("unknown", {}, "bogus") == TIER_COMMUNITY


def test_repo_manifest_loads_with_valid_tiers() -> None:
    tiers = load_tier_manifest(REPO_ROOT / "plugins" / "tiers.yaml")
    assert tiers, "tiers.yaml must declare at least one override"
    assert set(tiers.values()) <= {"official", "community", "experimental"}
    for name in tiers:
        assert (REPO_ROOT / "plugins" / f"{name}.yaml").exists() or (REPO_ROOT / "plugins" / f"{name}.lua").exists(), (
            f"tier manifest references missing plugin: {name}"
        )


def test_missing_manifest_returns_empty(tmp_path: Path) -> None:
    assert load_tier_manifest(tmp_path / "nope.yaml") == {}


def test_malformed_manifest_is_ignored(tmp_path: Path) -> None:
    bad = tmp_path / "tiers.yaml"
    bad.write_text("amsi_bypass: godmode\n123: 456\n- justalist\n", encoding="utf-8")
    assert load_tier_manifest(bad) == {}


def test_rate_and_average(tmp_path: Path) -> None:
    store = tmp_path / "ratings.json"
    assert rating_summary("p", store) == (0.0, 0)
    assert rate_plugin("p", 5, store) == (5.0, 1)
    assert rate_plugin("p", 3, store) == (4.0, 2)
    assert rating_summary("p", store) == (4.0, 2)


def test_rate_rejects_bad_input(tmp_path: Path) -> None:
    store = tmp_path / "ratings.json"
    with pytest.raises(ValueError):
        rate_plugin("", 5, store)
    for bad in (0, 6, -1):
        with pytest.raises(ValueError):
            rate_plugin("p", bad, store)


def test_corrupt_store_reads_empty(tmp_path: Path) -> None:
    store = tmp_path / "ratings.json"
    store.write_text("{not json", encoding="utf-8")
    assert rating_summary("p", store) == (0.0, 0)


def test_format_rating() -> None:
    assert format_rating(0.0, 0) == "unrated"
    assert format_rating(4.5, 2) == "4.5/5 (2 votes)"
    assert format_rating(5.0, 1) == "5.0/5 (1 vote)"


def test_read_metadata_tier(tmp_path: Path) -> None:
    plugin = tmp_path / "demo.yaml"
    plugin.write_text(yaml.safe_dump({"name": "demo", "tier": "experimental"}), encoding="utf-8")
    assert read_metadata_tier(plugin) == "experimental"
    plugin.write_text("name: demo\n", encoding="utf-8")
    assert read_metadata_tier(plugin) == ""
